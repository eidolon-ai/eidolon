from opentelemetry import trace

from eidolon_ai_client.util.logger import logger
from eidolon_ai_client.util.request_context import RequestContext


def refund(millis: int):
    logger.debug("Refunding amount:", millis)
    current_span = trace.get_current_span()
    span_id = current_span.get_span_context().span_id
    refund_key = f"refund_{span_id}"
    refund_amount = RequestContext.get(refund_key, None)
    if refund_amount:
        refund_amount += millis
    RequestContext.set(refund_key, refund_amount)

    current_span.set_attribute("usage.refund", refund_amount)
