"""Shared Draft-2020-12 subset JSON Schema validator for AGRP tooling.

Single internal module home for the validator logic that was previously
duplicated in tools/conformance/run_conformance_vectors.py and
tools/validate-adaptation-bundle.py (the "duplicate-with-citation"
strategy locked at increment 0048). Increment 0061 retires that
deferral for the stdlib-subset copies.

Public surface (5 symbols, used by both callers):

    class ValidationError(Exception): ...
    def load_json(path) -> object
    def resolve_ref(ref, base_path) -> (Path, object)
    def type_matches(data, expected) -> bool
    def validate(data, schema, base_path) -> None

Supports the Draft-2020-12 subset actually used by AGRP schemas:
$ref, oneOf, const, enum, type (incl. type-list), minLength, allOf,
if/then/else, required, properties, additionalProperties, items.

Runtime: Python 3 stdlib only. Import-safe — no top-level side effects.

Note: tools/adaptations/replay-northstar.py is intentionally NOT
migrated to this module. That script uses the external jsonschema +
referencing library stack (a separate validation surface) and remains
out of scope for the 0061 extraction.
"""

import json
from pathlib import Path


class ValidationError(Exception):
    pass


def load_json(path):
    return json.loads(Path(path).read_text())


def resolve_ref(ref, base_path):
    if ref.startswith("#/"):
        node = load_json(base_path)
        for part in ref[2:].split("/"):
            node = node[part]
        return base_path, node
    if "#" in ref:
        file_part, fragment = ref.split("#", 1)
    else:
        file_part, fragment = ref, ""
    target_path = (base_path.parent / file_part).resolve()
    target = load_json(target_path)
    if fragment.startswith("/"):
        node = target
        for part in fragment[1:].split("/"):
            node = node[part]
        return target_path, node
    return target_path, target


def type_matches(data, expected):
    mapping = {
        "object": dict,
        "array": list,
        "string": str,
        "boolean": bool,
        "null": type(None),
        "number": (int, float),
        "integer": int
    }
    if expected == "number":
        return isinstance(data, (int, float)) and not isinstance(data, bool)
    if expected == "integer":
        return isinstance(data, int) and not isinstance(data, bool)
    return isinstance(data, mapping[expected])


def validate(data, schema, base_path):
    if "$ref" in schema:
        ref_path, target = resolve_ref(schema["$ref"], base_path)
        return validate(data, target, ref_path or base_path)

    if "oneOf" in schema:
        matches = 0
        last_error = None
        for option in schema["oneOf"]:
            try:
                validate(data, option, base_path)
                matches += 1
            except ValidationError as exc:
                last_error = exc
        if matches != 1:
            raise ValidationError(f"oneOf mismatch: {last_error}")
        return

    if "const" in schema and data != schema["const"]:
        raise ValidationError(f"expected const {schema['const']!r}, got {data!r}")

    if "enum" in schema and data not in schema["enum"]:
        raise ValidationError(f"expected one of {schema['enum']!r}, got {data!r}")

    if "type" in schema:
        expected = schema["type"]
        if isinstance(expected, list):
            if not any(type_matches(data, item) for item in expected):
                raise ValidationError(f"expected types {expected!r}, got {type(data).__name__}")
        elif not type_matches(data, expected):
            raise ValidationError(f"expected type {expected!r}, got {type(data).__name__}")

    if isinstance(data, str) and "minLength" in schema and len(data) < schema["minLength"]:
        raise ValidationError(f"string shorter than minLength {schema['minLength']}")

    # Draft 2020-12 conditional support (minimal: allOf + if/then/else).
    # Added to detect schema conditionals used by repo schemas
    # (e.g., profile-declaration's "status: replaced => supersedes required" rule).
    if "allOf" in schema:
        for sub in schema["allOf"]:
            validate(data, sub, base_path)

    if "if" in schema:
        try:
            validate(data, schema["if"], base_path)
            branch = schema.get("then")
        except ValidationError:
            branch = schema.get("else")
        if branch is not None:
            validate(data, branch, base_path)

    if isinstance(data, dict):
        for key in schema.get("required", []):
            if key not in data:
                raise ValidationError(f"missing required key {key!r}")
        properties = schema.get("properties", {})
        for key, value in data.items():
            if key in properties:
                validate(value, properties[key], base_path)
            elif schema.get("additionalProperties") is False:
                raise ValidationError(f"unexpected property {key!r}")
        return

    if isinstance(data, list) and "items" in schema:
        for item in data:
            validate(item, schema["items"], base_path)
