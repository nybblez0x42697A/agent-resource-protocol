# Getting Started With AGRP v1

`AGRP v1.0.0` is published. This document shows you, the adopter,
how to validate the protocol corpus and the three reference
adaptations in one command — and how to validate your own
adaptation bundle the same way.

## What this is

`AGRP v1` ships a normative artifact set (charter, glossary, RSPL,
control-plane, schemas, conformance vectors), three reference
adaptations (Northstar tool registry, Pinecrest data products,
Helios governance registry), and a conformance harness. This
quickstart walks you through running the unified validator and
reading the output, then points you at the design docs and the
conformance-claim shape for your own adoption.

## Requirements

- Python 3.7 or newer.
- A clone of this repository.
- No external dependencies. The validation tooling uses only the
  Python 3 standard library.

## Quickstart

From the repository root, run:

    python3 tools/validate-all.py

This runs four stages in order:

1. The conformance harness (19 schema-conformance vectors).
2. The Northstar tool registry bundle (15 artifacts).
3. The Pinecrest data products bundle (16 artifacts).
4. The Helios governance registry bundle (19 artifacts).

On a clean clone of the v1 corpus you will see something like:

    === Stage 1/4: Conformance vectors ===
    ok audit-record.missing-action.invalid
    ok audit-record.valid
    ... (17 more vector lines)
    Stage 1/4 (Conformance vectors): 19 ok / 0 failed

    === Stage 2/4: Northstar bundle ===
    ok northstar-tool-registry/00-tool-resource.v1.example.json
    ok northstar-tool-registry/01-register-resource-version.v1.request.json
    ... (10 more schema-validated lines)
    ok-prose northstar-tool-registry/12-evidence-attestation.preview-to-ga.example.json (prose: spec/compliance/evidence-freshness-and-attestation.md:60-89)
    ok northstar-tool-registry/13-audit-record.transition.example.json
    ok northstar-tool-registry/14-capability-advertisement.example.json
    northstar-tool-registry: 15 ok / 0 failed (14 schema-validated + 1 prose-validated)
    Stage 2/4 (Northstar bundle): 15 ok / 0 failed

    === Stage 3/4: Pinecrest bundle ===
    ok pinecrest-data-products/00-data-product-resource.v1.example.json
    ... (15 more lines including 1 ok-prose)
    Stage 3/4 (Pinecrest bundle): 16 ok / 0 failed

    === Stage 4/4: Helios bundle ===
    ok helios-governance-registry/00-policy-revision-resource.v1.example.json
    ... (18 more lines including 3 ok-prose)
    Stage 4/4 (Helios bundle): 19 ok / 0 failed

    === SUMMARY ===
    Stage 1/4 (Conformance vectors): 19 ok / 0 failed
    Stage 2/4 (Northstar bundle): 15 ok / 0 failed (14 schema-validated + 1 prose-validated)
    Stage 3/4 (Pinecrest bundle): 16 ok / 0 failed (15 schema-validated + 1 prose-validated)
    Stage 4/4 (Helios bundle): 19 ok / 0 failed (16 schema-validated + 3 prose-validated)
    BUNDLE TOTAL: 50 ok / 0 failed (45 schema-validated + 5 prose-validated)
    TOTAL: 69 ok / 0 failed

The runner exits 0 when every stage reports zero failures.

## Two output verbs: `ok` and `ok-prose`

The bundle stages distinguish two passing outcomes:

- **`ok <bundle>/<file>`** — the artifact validated cleanly against
  a JSON Schema under `models/schemas/`.
- **`ok-prose <bundle>/<file> (prose: <ref>)`** — the artifact has
  no JSON Schema in the `AGRP v1` artifact set; it conforms to a
  prose-defined field shape, currently
  `spec/compliance/evidence-freshness-and-attestation.md:60-89`.
  Five evidence-attestation files across the three bundles use
  this validation pathway.

The two verbs are deliberately distinct so that prose-validated
artifacts are not mistaken for schema-covered JSON. The unified
summary preserves the same distinction (`45 schema-validated + 5
prose-validated`) so the breakdown is visible at a glance.

A `not ok` line means an artifact failed validation; the runner
walks every artifact in every stage before exiting non-zero, so
all failures surface in one run.

## What gets validated

| Stage | Source | Count |
|---|---|---|
| Conformance vectors | `examples/conformance-vectors/*.json` | 19 |
| Northstar bundle | `examples/adaptations/northstar-tool-registry/` | 15 (14 schema + 1 prose) |
| Pinecrest bundle | `examples/adaptations/pinecrest-data-products/` | 16 (15 schema + 1 prose) |
| Helios bundle | `examples/adaptations/helios-governance-registry/` | 19 (16 schema + 3 prose) |
| **Total** | — | **69** |

Each bundle's design narrative lives at:

- `docs/adaptations/northstar-tool-registry.md`
- `docs/adaptations/pinecrest-data-products.md`
- `docs/adaptations/helios-governance-registry.md`

Each bundle's `manifest.json` declares the artifact-to-schema (or
artifact-to-prose-ref) mapping; the bundle validator reads that
manifest and walks the artifacts in declaration order.

## Validating your own bundle

`tools/validate-adaptation-bundle.py <bundle-dir>` works against
any directory that contains a `manifest.json` of the same shape
as the three reference manifests. To validate your own adaptation:

1. Place your bundle's JSON artifacts in a directory.
2. Author a `manifest.json` in that directory, listing each
   artifact with either `"validation": "schema"` plus
   `"schema": "<path>"` (for JSON-Schema-validated artifacts) or
   `"validation": "prose"` plus `"proseRef": "<path>"` (for
   prose-shape artifacts).
3. Run `python3 tools/validate-adaptation-bundle.py <your-dir>/`.

The three reference manifests at
`examples/adaptations/<bundle>/manifest.json` are worked examples
of the manifest shape.

## Known limitations

Two are worth knowing up front.

**Stage 1/4 (the conformance harness) fails-fast within itself.**
The harness predates this unified runner. If a conformance vector
fails, the harness prints up to the first failure and exits; the
runner still continues to Stages 2-4 (full-walk at the stage
level), so bundle-level failures are still surfaced. Refactoring
the harness to also walk all vectors before exiting is a deferred
follow-up. In practice the conformance harness is a known-green
corpus invariant and rarely fails; if it ever does, that is
itself a serious finding.

**No CI is wired up in this repository yet.** The conformance
harness and bundle validator pass on a clean clone today, and
each producing increment closed with the corresponding proof in
its `reports/` directory, but the green state is not enforced
on every commit through GitHub Actions or similar. Adding CI is
a deferred follow-up.

One smaller item is also deferred: per-bundle replay scripts for
Pinecrest and Helios mirroring `tools/adaptations/replay-northstar.py`
(the existing Northstar replay walks the lifecycle in memory and
checks eight invariants, deeper than the generic shape validator).
The previously-deferred adopter conformance-claim template is now
shipped at `spec/conformance/conformance-claim-template.md` with
a JSON schema at `models/schemas/conformance-claim.schema.json`
and three worked examples under `examples/conformance-claims/`.

## Where to go next

- `docs/adaptations/northstar-tool-registry.md` — the simplest of
  the three reference adaptations; good first read.
- `docs/adaptations/pinecrest-data-products.md` — exercises lifecycle
  transitions and the consumer-trust profile-declaration.
- `docs/adaptations/helios-governance-registry.md` — exercises the
  propose / review / commit governance flow plus the privacy-tier
  profile-declaration.
- `spec/conformance/baseline-conformance.md` — the AGRP v1
  baseline-conformance claim shape.
- `spec/conformance/conformance-claim-template.md` — the
  supplementary adopter-facing template for publishing a
  conformance claim alongside your bundle. Optional; see
  `examples/conformance-claims/` for three worked examples
  (Northstar, Pinecrest, Helios).
- `docs/release-publication/agrp-v1.0.0-announcement.md` — the v1
  release notes and artifact-set summary.
- `tools/adaptations/replay-northstar.py` — the deeper narrative
  replay for the Northstar bundle (lifecycle replay + 8 locked
  invariants), as a worked example of bespoke per-bundle proof.
