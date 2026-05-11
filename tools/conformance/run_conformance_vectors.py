#!/usr/bin/env python3
import json
from pathlib import Path

from _validator import ValidationError, load_json, resolve_ref, type_matches, validate


ROOT = Path(__file__).resolve().parents[2]
SCHEMA_DIR = ROOT / "models" / "schemas"
VECTOR_DIR = ROOT / "examples" / "conformance-vectors"


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
