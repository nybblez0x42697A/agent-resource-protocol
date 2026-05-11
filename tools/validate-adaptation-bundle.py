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

The Draft-2020-12 subset JSON-Schema validator is imported from
tools/conformance/_validator.py, the shared module extracted in
increment 0061. The previous inline copy here was retired in 0061.
"""

import json
import sys
from pathlib import Path

# Reach the sibling tools/conformance/ directory for _validator.py.
sys.path.insert(0, str(Path(__file__).resolve().parent / "conformance"))
from _validator import ValidationError, load_json, resolve_ref, type_matches, validate


ROOT = Path(__file__).resolve().parent.parent


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
