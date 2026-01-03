from core.shared.infrastructure.messaging.consumers.schema_compatibility import (
    check_compatibility,
    IncompatibleSchemaError,
)


class BaseConsumer:
    def handle_message(self, envelope: dict):
        event_type = envelope["event_type"]
        version = envelope["version"]
        payload = envelope["payload"]

        try:
            check_compatibility(event_type, version, payload)
        except IncompatibleSchemaError as e:
            self.on_schema_error(envelope, e)
            return

        self.process(payload)

    def process(self, payload: dict):
        raise NotImplementedError

    def on_schema_error(self, envelope: dict, error: Exception):
        # DLQ comes later — for now we log loudly
        print(f"[SCHEMA ERROR] {error}")
