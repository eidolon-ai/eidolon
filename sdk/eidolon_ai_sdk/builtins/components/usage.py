import asyncio
import re
from re import Pattern

import math
from openai import BaseModel
from opentelemetry import trace
from opentelemetry.sdk.trace import SpanProcessor, ReadableSpan
from starlette.responses import JSONResponse

from eidolon_ai_client.util.logger import logger
from eidolon_ai_client.util.request_context import RequestContext
from eidolon_ai_sdk.security.user import User
from eidolon_ai_sdk.system.dynamic_middleware import Middleware
from eidolon_ai_sdk.system.reference_model import AnnotatedReference, Specable
from usage_client.client import UsageClient, UsageLimitExceeded
from usage_client.models import UsageDelta

action_pattern: Pattern[str] = re.compile(r"^POST /processes/([^/]+)/agent/([^/]+)/actions/([^\s/]+)$")


class UsageMiddleware(Middleware, BaseModel):
    path_regex: str = None
    usage_client: AnnotatedReference[UsageClient]

    async def dispatch(self, request, call_next):
        search_pattern = re.compile(self.path_regex) if self.path_regex else action_pattern
        if search_pattern.search(f"{request.method} {request.url.path}"):
            trace.get_current_span().set_attribute("usage_subject", User.get_current().id)
            client: UsageClient = self.usage_client.instantiate()
            subject = User.get_current().id
            try:
                await client.get_summary(subject)
            except UsageLimitExceeded as e:
                return JSONResponse(status_code=429, content={
                    "detail": "Usage limit exceeded",
                    "used": e.summary.used,
                    "allowed": e.summary.allowed
                })
            except Exception as e:
                return JSONResponse(status_code=502, content={
                    "detail": "Error checking usage",
                    "error": str(e)
                })
        return await call_next(request)


async def _billing(client, subject, amount):
    try:
        await client.record_transaction(subject, UsageDelta(used_delta=amount))
        logger.info(f"Billed Usage: {amount}")
    except Exception:
        logger.exception("Error recording usage")
        raise


class UsageSpanProcessorConfig(BaseModel):
    usage_client: AnnotatedReference[UsageClient]
    wrapped: AnnotatedReference[SpanProcessor]
    refund_regex: str = "tool\scalls"


class UsageSpanProcessor(SpanProcessor, Specable[UsageSpanProcessorConfig]):
    wrapped: SpanProcessor
    cost_pattern = Pattern[str]
    refund_pattern = Pattern[str]

    def __init__(self, *args, spec, **kwargs):
        SpanProcessor.__init__(self)
        Specable.__init__(self, spec)
        self.wrapped = spec.wrapped.instantiate(*args, **kwargs)
        self.usage_client = spec.usage_client.instantiate()
        self.cost_pattern = action_pattern
        self.refund_pattern = re.compile(spec.refund_regex)

    def on_start(self, *args, **kwargs):
        return self.wrapped.on_start(*args, **kwargs)

    def on_end(self, span: ReadableSpan):
        try:
            units_per_second = 1000000000
            if self.cost_pattern.search(span.name):
                cost = (span.end_time - span.start_time) / units_per_second
                refund = RequestContext.get("eidolon_refund", 0)
                to_pay = max(0, math.ceil(cost - refund))
                subject = span.attributes['usage_subject']
                asyncio.create_task(_billing(self.usage_client, subject, to_pay))
            elif self.refund_pattern.search(span.name):
                duration = (span.end_time - span.start_time) / units_per_second
                refunded = RequestContext.get("eidolon_refund", 0)
                RequestContext.set("eidolon_refund", refunded + duration)
        except Exception:
            logger.exception("Error billing usage")
        return self.wrapped.on_end(span)

    def shutdown(self):
        return self.wrapped.shutdown()
