#!/usr/bin/env python3
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
SCHEMA_DIR = ROOT / "models" / "schemas"
VECTOR_DIR = ROOT / "examples" / "conformance-vectors"


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


def classify_failure(payload):
    error = payload.get("error")
    if not isinstance(error, dict):
        return None, None
    category = error.get("category")
    mapping = {
        "validation_error": "validation_failure",
        "not_found": "validation_failure",
        "conflict": "lifecycle_failure",
        "policy_denied": "policy_failure",
        "access_denied": "access_failure",
        "unsupported_operation": "compatibility_failure",
        "internal_error": "internal_failure"
    }
    return mapping.get(category), category


def run_fixture(path):
    fixture = load_json(path)
    schema_path = ROOT / fixture["targetSchema"]
    schema = load_json(schema_path)
    payload = fixture["payload"]
    expected = fixture["expected"]

    try:
        validate(payload, schema, schema_path)
        observed_outcome = "pass"
    except ValidationError as exc:
        observed_outcome = "fail"
        observed_error = str(exc)

    if observed_outcome != expected["outcome"]:
        raise SystemExit(
            f"{fixture['fixtureId']}: expected {expected['outcome']} but observed {observed_outcome}"
        )

    if observed_outcome == "pass" and "errorCategory" in expected:
        failure_class, error_category = classify_failure(payload)
        if failure_class != expected.get("failureClass") or error_category != expected.get("errorCategory"):
            raise SystemExit(
                f"{fixture['fixtureId']}: expected ({expected.get('failureClass')}, {expected.get('errorCategory')}) "
                f"but observed ({failure_class}, {error_category})"
            )

    if observed_outcome == "fail":
        if expected.get("failureClass") != "validation_failure" or expected.get("errorCategory") != "validation_error":
            raise SystemExit(
                f"{fixture['fixtureId']}: schema failure only supports validation_failure/validation_error expectations"
            )

    print(f"ok {fixture['fixtureId']}")


def main():
    for path in sorted(VECTOR_DIR.glob("*.json")):
        run_fixture(path)


if __name__ == "__main__":
    main()
