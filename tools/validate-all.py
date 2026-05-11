#!/usr/bin/env python3
"""Unified validation runner for the AGRP v1 corpus.

Single command for adopters: validates conformance vectors plus all
three reference adaptation bundles, then emits a unified summary.

Stage order (deterministic):
  1/4 Conformance vectors    (tools/conformance/run_conformance_vectors.py)
  2/4 Northstar bundle       (examples/adaptations/northstar-tool-registry/)
  3/4 Pinecrest bundle       (examples/adaptations/pinecrest-data-products/)
  4/4 Helios bundle          (examples/adaptations/helios-governance-registry/)

Full-walk at the stage level: all four stages run regardless of any
earlier stage's exit. Each child's stdout is captured and forwarded
verbatim, then a per-stage summary line is appended. After all four
stages complete, a unified SUMMARY block is printed that preserves
the schema-validated vs prose-validated artifact distinction across
the three bundle stages.

Exit 0 if every stage reported zero failures; exit 1 only after all
four stages have run, the unified summary has been printed, and at
least one failure was recorded.

Known limitation (documented in docs/getting-started.md):
  Stage 1/4 invokes the existing run_conformance_vectors.py harness,
  which fails-fast on first vector failure (existing behavior; not
  edited per increment 0058 Locked Decision 4 / "no extraction").
  If a conformance vector fails, Stage 1 will print only up to that
  first failure within itself; Stages 2-4 still run to completion
  (full-walk at the stage level) and surface all bundle-level
  failures. The unified summary aggregates the per-stage outcomes.

Runtime: Python 3 stdlib only.
"""

import re
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent

# TAP-style result-line classifiers. Anchored patterns require result-line
# shape (TAP-numbered, bundle-path slash form, or conformance bare-token
# form), so child-tool summary lines (`<bundle>: K ok / F failed (...)`)
# and stage headers cannot collide with result counts.
_SCHEMA_OK_RE = re.compile(r"^ok \d+ - .+|^ok [^:\s]+/.+|^ok [^:\s]+$")
_PROSE_OK_RE = re.compile(r"^ok-prose [^:\s]+/.+")
_FAIL_RE = re.compile(r"^not ok \d+ - .+|^not ok [^:\s]+/.+: .+")

STAGES = [
    {
        "name": "Conformance vectors",
        "kind": "conformance",
        "argv": [sys.executable, str(ROOT / "tools" / "conformance" / "run_conformance_vectors.py")],
    },
    {
        "name": "Northstar bundle",
        "kind": "bundle",
        "argv": [sys.executable, str(ROOT / "tools" / "validate-adaptation-bundle.py"),
                 str(ROOT / "examples" / "adaptations" / "northstar-tool-registry")],
    },
    {
        "name": "Pinecrest bundle",
        "kind": "bundle",
        "argv": [sys.executable, str(ROOT / "tools" / "validate-adaptation-bundle.py"),
                 str(ROOT / "examples" / "adaptations" / "pinecrest-data-products")],
    },
    {
        "name": "Helios bundle",
        "kind": "bundle",
        "argv": [sys.executable, str(ROOT / "tools" / "validate-adaptation-bundle.py"),
                 str(ROOT / "examples" / "adaptations" / "helios-governance-registry")],
    },
]


def run_stage(index, stage):
    """Run one stage; return result dict with counts."""
    total = len(STAGES)
    print(f"=== Stage {index}/{total}: {stage['name']} ===")

    proc = subprocess.run(
        stage["argv"],
        capture_output=True,
        text=True,
        cwd=str(ROOT),
    )

    # Forward child stdout verbatim so per-artifact lines remain visible.
    if proc.stdout:
        sys.stdout.write(proc.stdout)
        if not proc.stdout.endswith("\n"):
            sys.stdout.write("\n")
    if proc.stderr:
        sys.stderr.write(proc.stderr)

    # Count line types from stdout using anchored TAP-style patterns.
    # Summary lines (`<bundle>: K ok / F failed (...)`) and stage headers
    # do not match these patterns and are correctly excluded.
    schema_ok = 0
    prose_ok = 0
    fail = 0
    for line in (proc.stdout or "").splitlines():
        if _PROSE_OK_RE.match(line):
            prose_ok += 1
        elif _SCHEMA_OK_RE.match(line):
            schema_ok += 1
        elif _FAIL_RE.match(line):
            fail += 1

    # If a child exited non-zero but no `not ok` lines were captured
    # (e.g., the conformance harness raises SystemExit with a one-line
    # message to stderr), surface a stage-level failure so the unified
    # summary reflects it.
    if proc.returncode != 0 and fail == 0:
        fail = 1
        print(f"Stage {index}/{total} ({stage['name']}): exited {proc.returncode} (see stderr)")

    ok = schema_ok + prose_ok
    print(f"Stage {index}/{total} ({stage['name']}): {ok} ok / {fail} failed")
    print()

    return {
        "name": stage["name"],
        "kind": stage["kind"],
        "ok": ok,
        "schema_ok": schema_ok,
        "prose_ok": prose_ok,
        "fail": fail,
    }


def main():
    results = []
    for index, stage in enumerate(STAGES, start=1):
        results.append(run_stage(index, stage))

    total_ok = sum(r["ok"] for r in results)
    total_fail = sum(r["fail"] for r in results)
    total_schema = sum(r["schema_ok"] for r in results if r["kind"] == "bundle")
    total_prose = sum(r["prose_ok"] for r in results if r["kind"] == "bundle")
    bundle_ok = sum(r["ok"] for r in results if r["kind"] == "bundle")
    bundle_fail = sum(r["fail"] for r in results if r["kind"] == "bundle")

    print("=== SUMMARY ===")
    for index, r in enumerate(results, start=1):
        if r["kind"] == "bundle":
            print(
                f"Stage {index}/{len(STAGES)} ({r['name']}): "
                f"{r['ok']} ok / {r['fail']} failed "
                f"({r['schema_ok']} schema-validated + {r['prose_ok']} prose-validated)"
            )
        else:
            print(f"Stage {index}/{len(STAGES)} ({r['name']}): {r['ok']} ok / {r['fail']} failed")
    print(
        f"BUNDLE TOTAL: {bundle_ok} ok / {bundle_fail} failed "
        f"({total_schema} schema-validated + {total_prose} prose-validated)"
    )
    print(f"TOTAL: {total_ok} ok / {total_fail} failed")

    return 0 if total_fail == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
