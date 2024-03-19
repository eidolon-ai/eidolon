from abc import abstractmethod

from opentelemetry import trace
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter
from opentelemetry.sdk.resources import SERVICE_NAME, Resource, logger
from opentelemetry.sdk.trace import TracerProvider, SpanProcessor
from opentelemetry.sdk.trace.sampling import Sampler, SamplingResult, Decision
from pydantic import BaseModel

from eidolon_ai_sdk.system.reference_model import Specable, AnnotatedReference


class OpenTelemetryManager:
    @abstractmethod
    def setup(self):
        raise NotImplementedError


class NoopOpenTelemetry(OpenTelemetryManager):
    def setup(self):
        logger.info("OpenTelemetry is disabled")


class OpenTelemetryConfig(BaseModel):
    service_name: str = "eidolon"
    exporter_args: dict = {"endpoint": "http://localhost:4317", "insecure": True}
    sampler: AnnotatedReference[Sampler]
    span_processor: AnnotatedReference[SpanProcessor]


class BatchOpenTelemetry(Specable[OpenTelemetryConfig], OpenTelemetryManager):
    def setup(self):
        sampler = self.spec.sampler.instantiate()
        provider_resource = Resource.create({SERVICE_NAME: self.spec.service_name})
        provider = TracerProvider(sampler=sampler, resource=provider_resource)
        trace.set_tracer_provider(provider)
        exporter = OTLPSpanExporter(**self.spec.exporter_args)
        provider.add_span_processor(self.spec.span_processor.instantiate(span_exporter=exporter))


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
