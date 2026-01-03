from core.shared.infrastructure.messaging.schemas.loader import load_schema


class IncompatibleSchemaError(Exception):
    pass


def check_compatibility(event_type: str, version: int, payload: dict):
    """
    Ensures the incoming payload is compatible with the consumer's expected schema.
    """

    schema = load_schema(event_type, version)

    # REQUIRED fields check
    for field in schema.required_fields:
        if field not in payload:
            raise IncompatibleSchemaError(
                f"Missing required field '{field}' for {event_type} v{version}"
            )

    # TYPE safety (soft check, not strict Avro yet)
    for field, expected_type in schema.field_types.items():
        if field in payload and not isinstance(payload[field], expected_type):
            raise IncompatibleSchemaError(
                f"Field '{field}' has wrong type for {event_type} v{version}"
            )

    return True
