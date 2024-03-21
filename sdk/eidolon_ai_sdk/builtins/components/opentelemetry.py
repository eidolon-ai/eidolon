from opentelemetry import trace
from opentelemetry.sdk.resources import SERVICE_NAME, Resource
from opentelemetry.sdk.trace import TracerProvider, SpanProcessor
from opentelemetry.sdk.trace.export import SpanExporter
from opentelemetry.sdk.trace.sampling import Sampler, SamplingResult, Decision
from pydantic import BaseModel

from eidolon_ai_client.util.logger import logger
from eidolon_ai_sdk.system.reference_model import Specable, AnnotatedReference


class NoopSpanExporter(SpanExporter):
    def export(self, spans):
        logger.debug(f"Exporting spans: {spans}")

    def shutdown(self):
        pass


class OpenTelemetryConfig(BaseModel):
    service_name: str = "eidolon"
    exporter: AnnotatedReference[SpanExporter]
    sampler: AnnotatedReference[Sampler]
    span_processor: AnnotatedReference[SpanProcessor]


class OpenTelemetryManager(Specable[OpenTelemetryConfig]):
    exporter: SpanExporter

    async def start(self):
        self.exporter = self.spec.exporter.instantiate()
        sampler = self.spec.sampler.instantiate()
        provider_resource = Resource.create({SERVICE_NAME: self.spec.service_name})
        provider = TracerProvider(sampler=sampler, resource=provider_resource)
        trace.set_tracer_provider(provider)
        provider.add_span_processor(self.spec.span_processor.instantiate(span_exporter=self.exporter))

    async def stop(self):
        self.exporter.shutdown()


class CustomSampler(Sampler):
    def __init__(self, prune_receive: bool = True, prune_send: bool = True):
        self.prune_receive = prune_receive
        self.prune_send = prune_send

    def should_sample(
        self, parent_context, trace_id: int, name: str, kind=None, attributes=None, links=None, trace_state=None
    ):
        # http receive / send are verbose with streaming, but should be recorded since they record http status
        if self.prune_send and name.endswith("http send"):
            return SamplingResult(Decision.RECORD_ONLY)
        if self.prune_receive and name.endswith("http receive"):
            return SamplingResult(Decision.RECORD_ONLY)
        return SamplingResult(Decision.RECORD_AND_SAMPLE)

    def get_description(self):
        return "CustomSampler"
