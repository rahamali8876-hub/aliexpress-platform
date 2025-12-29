# from opentelemetry import trace

# tracer = trace.get_tracer("aliexpress-clone")


# def start_span(name: str):
#     return tracer.start_as_current_span(name)


from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import (
    OTLPSpanExporter,
)


def setup_tracing() -> None:
    provider = TracerProvider()
    trace.set_tracer_provider(provider)

    exporter = OTLPSpanExporter(
        endpoint="http://otel-collector:4317",
        insecure=True,
    )

    processor = BatchSpanProcessor(exporter)
    provider.add_span_processor(processor)


tracer = trace.get_tracer("aliexpress-clone")


def start_span(name: str):
    return tracer.start_as_current_span(name)
