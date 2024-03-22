import asyncio
import re
from re import Pattern

import math
from openai import BaseModel
from opentelemetry import trace
from opentelemetry.sdk.trace import ReadableSpan
from opentelemetry.sdk.trace import TracerProvider, SpanProcessor
from starlette.responses import JSONResponse

from eidolon_ai_client.util.logger import logger
from eidolon_ai_client.util.request_context import RequestContext
from eidolon_ai_sdk.security.user import User
from eidolon_ai_sdk.system.dynamic_middleware import Middleware
from eidolon_ai_sdk.system.reference_model import AnnotatedReference
from eidolon_ai_usage_client.client import UsageClient, UsageLimitExceeded
from eidolon_ai_usage_client.models import UsageDelta

default_cost_pattern: Pattern[str] = re.compile(r"^POST /processes/([^/]+)/agent/([^/]+)/actions/([^\s/]+)$")
default_refund_pattern: Pattern[str] = re.compile(r"tool\scalls")


class UsageMiddleware(BaseModel, Middleware):
    cost_regex: str = None
    refund_regex: str = None
    usage_client: AnnotatedReference[UsageClient]

    def __init__(self):
        super().__init__()
        UsageSpanProcessor.register(
            client=self.usage_client.instantiate(),
            cost_pattern=self.cost_pattern(),
            refund_pattern=self.refund_pattern(),
        )

    def cost_pattern(self):
        return re.compile(self.cost_regex) if self.cost_regex else default_cost_pattern

    def refund_pattern(self):
        return re.compile(self.refund_regex) if self.refund_regex else default_refund_pattern

    async def dispatch(self, request, call_next):
        if self.cost_pattern().search(f"{request.method} {request.url.path}"):
            trace.get_current_span().set_attribute("usage_subject", User.get_current().id)
            client: UsageClient = self.usage_client.instantiate()
            subject = User.get_current().id
            try:
                await client.get_summary(subject)
            except UsageLimitExceeded as e:
                return JSONResponse(
                    status_code=429,
                    content={"detail": "Usage limit exceeded", "used": e.summary.used, "allowed": e.summary.allowed},
                )
            except Exception as e:
                logger.exception("Error checking usage")
                return JSONResponse(status_code=502, content={"detail": "Error checking usage", "error": str(e)})
        return await call_next(request)


async def _billing(client, subject, amount):
    try:
        await client.record_transaction(subject, UsageDelta(used_delta=amount))
        logger.info(f"Recorded Usage: {amount}")
    except Exception:
        logger.exception("Error recording usage")
        raise


class UsageSpanProcessor(SpanProcessor):
    _added = False
    usage_client: UsageClient
    cost_pattern: Pattern[str]
    refund_pattern: Pattern[str]

    def __init__(self, client, cost_pattern, refund_pattern):
        self.usage_client = client
        self.cost_pattern = cost_pattern
        self.refund_pattern = refund_pattern

    @staticmethod
    def register(**kwargs):
        if not UsageSpanProcessor._added:
            UsageSpanProcessor._added = True
            trace_provider: TracerProvider = trace.get_tracer_provider()
            trace_provider.add_span_processor(UsageSpanProcessor(**kwargs))

    def on_start(self, *args, **kwargs):
        pass

    def on_end(self, span: ReadableSpan):
        try:
            units_per_second = 1000000000
            if self.cost_pattern.search(span.name):
                cost = (span.end_time - span.start_time) / units_per_second
                refund = RequestContext.get("eidolon_refund", 0)
                to_pay = max(0, math.ceil(cost - refund))
                subject = span.attributes["usage_subject"]
                asyncio.create_task(_billing(self.usage_client, subject, to_pay))
            elif self.refund_pattern.search(span.name):
                duration = (span.end_time - span.start_time) / units_per_second
                refunded = RequestContext.get("eidolon_refund", 0)
                RequestContext.set("eidolon_refund", refunded + duration)
        except Exception:
            logger.exception("Error billing usage")

    def shutdown(self):
        pass
