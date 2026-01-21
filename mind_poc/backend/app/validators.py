import json
from pathlib import Path

from jsonschema import Draft7Validator

SCHEMA_DIR = Path(__file__).resolve().parents[2] / "contracts"


class SchemaValidationError(Exception):
    def __init__(self, message):
        super().__init__(message)
        self.message = message


def _load_schema(schema_name):
    schema_path = SCHEMA_DIR / schema_name
    with schema_path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def validate_schema(payload, schema_name):
    schema = _load_schema(schema_name)
    validator = Draft7Validator(schema)
    errors = sorted(validator.iter_errors(payload), key=lambda error: error.path)
    if errors:
        error = errors[0]
        path = ".".join([str(entry) for entry in error.path])
        message = f"Schema validation error at '{path}': {error.message}"
        raise SchemaValidationError(message)
