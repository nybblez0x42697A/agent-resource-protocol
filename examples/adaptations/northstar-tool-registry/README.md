# Northstar Tool Registry — Artifact Bundle

This directory contains the concrete JSON artifacts that accompany the design document at [`docs/adaptations/northstar-tool-registry.md`](../../../docs/adaptations/northstar-tool-registry.md). The artifacts walk one synthetic tool (`northstar/example-search-tool`) end-to-end through AGRP v1: creation of two versions, registration, lineage, audit, lifecycle transition (`draft → active`) with attestation, and capability advertisement.

## Status

Non-normative supporting material under `spec/charter/agrp-v1-artifact-set.md:85-92`. These artifacts are illustrative; the AGRP spec corpus governs where any wording or shape conflicts.

## Reading order

The 15 JSON files use a two-digit step prefix (`00-` through `14-`) to enforce read-order. Read them in numeric order with the design document open alongside; section 7 of the design doc narrates the walkthrough step-by-step and links each step to its file here.

| # | File | Validates against | What it shows |
|---|---|---|---|
| 0 | `00-tool-resource.v1.example.json` | `models/schemas/resource-entity.schema.json` | Publisher constructs v1's resource entity (`metadata.northstarStage = "preview"`; capabilities = `[search]`) |
| 1 | `01-register-resource-version.v1.request.json` | `models/schemas/control-plane-envelope.schema.json` (`RegisterResourceVersion` request branch) | Publisher submits v1 wrapped in a control-plane envelope |
| 2 | `02-register-resource-version.v1.response.json` | `control-plane-envelope.schema.json` (success branch) | Registry responds with the resulting `registrationRecord` and `lineageNode` |
| 3 | `03-registration-record.v1.example.json` | `models/schemas/registration-record.schema.json` | Standalone view of v1's registration record (`status = active` even though `lifecycleState = draft`) |
| 4 | `04-audit-record.create.v1.example.json` | `models/schemas/audit-record.schema.json` | Audit record for v1's creation (publisher in `actor`) |
| 5 | `05-lineage-node.v1.example.json` | `models/schemas/lineage-node.schema.json` | v1's lineage node — root of its chain (no parent) |
| 6 | `06-tool-resource.v2.example.json` | `resource-entity.schema.json` | v2 with capability change (`capabilities = [search, summarize]`) |
| 7 | `07-register-resource-version.v2.request.json` | envelope (request branch) | Publisher submits v2 |
| 8 | `08-lineage-node.v2.example.json` | `lineage-node.schema.json` | v2's lineage node parented to v1 |
| 9 | `09-audit-record.update.v2.example.json` | `audit-record.schema.json` | Audit record for v2's registration |
| 10 | `10-lifecycle-transition.preview-to-ga.request.json` | envelope (`TransitionLifecycleState` request branch) | Steward initiates `draft → active` for v2 |
| 11 | `11-lifecycle-transition.preview-to-ga.event.json` | `models/schemas/lifecycle-transition.schema.json` | Registry-persisted transition event |
| 12 | `12-evidence-attestation.preview-to-ga.example.json` | `spec/compliance/evidence-freshness-and-attestation.md:60-89` (no schema; prose-defined shape) | Attestation authority signs evidence backing the GA promotion |
| 13 | `13-audit-record.transition.example.json` | `audit-record.schema.json` | Audit record for the transition (steward in `actor`) |
| 14 | `14-capability-advertisement.example.json` | `models/schemas/capability-advertisement.schema.json` | Registry's catalog-level advertisement, post-promotion |

## Conventions used across the bundle

- **Identifiers**: `resourceId = "northstar/example-search-tool"` is constant across both versions. v1 has `versionId = "0.1.0"`; v2 has `versionId = "0.2.0"`. The same ids appear in every file that references the tool.
- **Timestamps**: monotonically increasing across the read-order. v1 creation precedes v2 creation; both precede the transition; the transition precedes the capability advertisement.
- **Actors**:
  - Publisher: `urn:northstar:actor:publisher:tools-team`
  - Registry steward: `urn:northstar:actor:steward:registry-governance`
  - Attestation authority: `urn:northstar:actor:attestor:release-engineering`
- **Implementation references**: OCI-style URIs of the form `oci://registry.northstar.example/tools/example-search-tool@sha256:<digest>`; the `<digest>` differs between v1 and v2 (different content).
- **Northstar-specific surface info** lives in `metadata` on the resource entity (`northstarStage`, `displayName`, `description`, `publisher`, `license`, etc.).

## Schema validation

Every JSON artifact validates against the schema named in the table above. For `12-evidence-attestation.preview-to-ga.example.json`, no AGRP schema exists today; the artifact's structure is verified by citation match against `spec/compliance/evidence-freshness-and-attestation.md:60-89`.

The validation report is captured at the increment level under `.specweave/increments/0047-agrp-northstar-tool-registry-reference-adaptation/reports/schema-validation-output.txt` after C6 runs.

## How this bundle relates to other repository material

- The **design document** at `docs/adaptations/northstar-tool-registry.md` is the narrative explaining what these artifacts are doing and why.
- The **conformance vectors** at `examples/conformance-vectors/` are the machine-checkable complement: this bundle is explanatory material; the vectors are the conformance test corpus.
- The **`adopters/`** directory holds mappings against named real-world systems. This bundle lives at `examples/adaptations/` because Northstar is intentionally synthetic.
