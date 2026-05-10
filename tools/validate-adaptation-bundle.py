#!/usr/bin/env python3
"""Validate an AGRP adaptation bundle against its declared manifest.

Reads <bundle-dir>/manifest.json, walks each artifact in declaration
order, and validates per-artifact according to its `validation` field:

  - "schema": JSON-Schema-validate against the manifest-declared schema
  - "prose":  confirm file exists and is parseable JSON; the artifact's
              shape is governed by a prose specification (e.g.,
              spec/compliance/evidence-freshness-and-attestation.md)
              that this validator does not parse

Output (stdout, deterministic order):
  ok <bundle>/<file>                                      (schema PASS)
  ok-prose <bundle>/<file> (prose: <proseRef>)            (prose PASS)
  not ok <bundle>/<file>: <single-line reason>            (any FAIL)

After the full walk:
  <bundle>: <K> ok / <F> failed (<S> schema-validated + <P> prose-validated)

Exit 0 if every artifact PASS; exit 1 only after the full walk
completes and the summary line is printed.

Runtime: Python 3 stdlib only (no external dependencies).

Citation: the JSON-Schema validator below is a Draft-2020-12 subset
copy of the implementation in
  tools/conformance/run_conformance_vectors.py
which is also duplicated in
  tools/adaptations/replay-northstar.py
per the duplicate-with-citation strategy locked at increment 0048.
Extraction is deferred to a follow-up increment.
"""

import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent


# --- Draft-2020-12 subset validator (duplicate-with-citation; see header) ---

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
        "object": dict, "array": list, "string": str,
        "boolean": bool, "null": type(None),
        "number": (int, float), "integer": int,
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


# --- Per-bundle walk ---

def validate_artifact(entry, bundle_dir, bundle_name):
    """Validate a single manifest entry. Return (status, line) tuple.

    status: "ok" | "ok-prose" | "fail"
    line:   the single output line for this artifact
    """
    file_rel = entry.get("file")
    if not file_rel:
        return ("fail", f"not ok {bundle_name}/<unknown>: manifest entry missing 'file'")

    artifact_path = bundle_dir / file_rel
    label = f"{bundle_name}/{file_rel}"

    validation_type = entry.get("validation")
    if validation_type not in ("schema", "prose"):
        return ("fail", f"not ok {label}: manifest entry missing/invalid 'validation' (must be 'schema' or 'prose')")

    if not artifact_path.exists():
        return ("fail", f"not ok {label}: artifact file not found")

    try:
        artifact = load_json(artifact_path)
    except json.JSONDecodeError as exc:
        return ("fail", f"not ok {label}: invalid JSON ({exc.msg} at line {exc.lineno})")

    if validation_type == "prose":
        prose_ref = entry.get("proseRef")
        if not prose_ref:
            return ("fail", f"not ok {label}: validation=prose but 'proseRef' missing")
        return ("ok-prose", f"ok-prose {label} (prose: {prose_ref})")

    # validation_type == "schema"
    schema_rel = entry.get("schema")
    if not schema_rel:
        return ("fail", f"not ok {label}: validation=schema but 'schema' missing")

    schema_path = ROOT / schema_rel
    if not schema_path.exists():
        return ("fail", f"not ok {label}: schema not found at {schema_rel}")

    try:
        schema = load_json(schema_path)
    except json.JSONDecodeError as exc:
        return ("fail", f"not ok {label}: schema is invalid JSON ({exc.msg})")

    try:
        validate(artifact, schema, schema_path)
    except ValidationError as exc:
        return ("fail", f"not ok {label}: {exc}")

    return ("ok", f"ok {label}")


def main(argv):
    if len(argv) != 2:
        print("usage: validate-adaptation-bundle.py <bundle-dir>", file=sys.stderr)
        return 1

    bundle_dir = Path(argv[1]).resolve()
    if not bundle_dir.is_dir():
        print(f"not ok {argv[1]}: not a directory", file=sys.stderr)
        return 1

    manifest_path = bundle_dir / "manifest.json"
    if not manifest_path.exists():
        print(f"not ok {bundle_dir}/manifest.json: not found", file=sys.stderr)
        return 1

    try:
        manifest = load_json(manifest_path)
    except json.JSONDecodeError as exc:
        print(f"not ok {manifest_path}: invalid JSON ({exc.msg} at line {exc.lineno})", file=sys.stderr)
        return 1

    bundle_name = manifest.get("bundle") or bundle_dir.name
    artifacts = manifest.get("artifacts") or []
    if not artifacts:
        print(f"not ok {manifest_path}: 'artifacts' missing or empty", file=sys.stderr)
        return 1

    schema_ok = 0
    prose_ok = 0
    failed = 0

    for entry in artifacts:
        status, line = validate_artifact(entry, bundle_dir, bundle_name)
        print(line)
        if status == "ok":
            schema_ok += 1
        elif status == "ok-prose":
            prose_ok += 1
        else:
            failed += 1

    total_ok = schema_ok + prose_ok
    print(f"{bundle_name}: {total_ok} ok / {failed} failed ({schema_ok} schema-validated + {prose_ok} prose-validated)")

    return 0 if failed == 0 else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv))
