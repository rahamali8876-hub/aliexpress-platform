import json
from pathlib import Path


class LoadedSchema:
    def __init__(self, required_fields, field_types):
        self.required_fields = required_fields
        self.field_types = field_types


def load_schema(event_type: str, version: int) -> LoadedSchema:
    """
    Example:
    event_type = product.created
    file = product/product_created.v2.json
    """

    domain, name = event_type.split(".")
    file_name = f"{name.replace('.', '_')}.v{version}.json"

    path = Path(f"core/shared/infrastructure/messaging/schemas/{domain}/{file_name}")

    if not path.exists():
        raise FileNotFoundError(f"Schema not found: {path}")

    with open(path) as f:
        schema = json.load(f)

    required = schema.get("required", [])
    properties = schema.get("properties", {})

    python_types = {
        "string": str,
        "integer": int,
        "number": (int, float),
        "object": dict,
        "array": list,
        "boolean": bool,
    }

    field_types = {
        k: python_types[v["type"]] for k, v in properties.items() if "type" in v
    }

    return LoadedSchema(required, field_types)
