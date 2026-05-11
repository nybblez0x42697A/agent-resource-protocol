# Conformance Claim Template

## Status

This document is **supplementary adopter-support material** for
the protocol's baseline conformance model defined at
`spec/conformance/baseline-conformance.md`.

It defines a publishable artifact shape — a *conformance claim
document* — that an adopter MAY publish alongside their bundle to
declare AGRP v1 conformance posture in a machine-readable form.

Three properties of this document are explicit and load-bearing:

1. **Claim publication is optional.** Adopters MAY publish a
   claim document; they are not required to do so by AGRP v1.
2. **Absence of a claim does not make an otherwise-conforming
   implementation non-conforming.** v1 conformance is determined
   by the contents of `baseline-conformance.md`, not by whether a
   claim document exists.
3. **The v1 artifact set remains unchanged.** This document is
   not listed in `spec/charter/agrp-v1-artifact-set.md`. No
   amendment to v1.0.0 is implied or required.

A future v1.x amendment MAY graduate this template into the
normative artifact set after adopter feedback. Until that
happens, this document is an adopter-facing template, not a
protocol requirement.

## Scope

This document defines:

- the publishable claim-document shape (prose + JSON schema)
- the meaning of each claim field
- the relationship between a claim and the existing baseline
  conformance model at `spec/conformance/baseline-conformance.md`

It does not redefine:

- what AGRP v1 conformance requires (see
  `spec/conformance/baseline-conformance.md §Conformance Claim`)
- which artifacts an implementation must support (see
  `spec/conformance/baseline-conformance.md §Baseline Artifact Set`)
- the in-scope schema set (see
  `spec/conformance/baseline-conformance.md §Schema Conformance`)
- the operation set (see
  `spec/conformance/baseline-conformance.md §Operation Conformance`)
- the error-category set (see
  `spec/conformance/baseline-conformance.md §Error Conformance`)

## Claim Document Shape

The machine-readable form of a claim is defined by the JSON Schema
at `models/schemas/conformance-claim.schema.json`. The prose
description below covers the same shape for adopters who want to
understand the field set before consulting the schema.

A claim document is a JSON object with ten required top-level
fields and one optional top-level field.

### Required Fields

| Field | Type | Description |
|---|---|---|
| `claimVersion` | string | Pins the version of this claim shape. The initial value is `"1"`. Allows future evolution of the claim shape without ambiguity. |
| `claimedBy` | object | Identifies the claimant. Required nested keys: `system` (string), `organization` (string). |
| `claimedAt` | string | ISO-8601 timestamp of the claim. |
| `agrpVersion` | string | The AGRP release the claim is made against (initial `"v1"`). |
| `conformanceLevel` | string | The level claimed. Matches a value defined in `spec/conformance/baseline-conformance.md §Conformance Levels` (currently `"baseline"`). |
| `claimElements` | array | Four objects, one per element listed in `spec/conformance/baseline-conformance.md §Conformance Claim`. Each object MUST include `element` (one of the four named elements) and `evidence` (a short pointer to where the claimant believes the element is satisfied — typically a file path or a doc reference). |
| `schemasInScope` | array of strings | Schema paths the claim depends on. Corresponds to the set listed in `spec/conformance/baseline-conformance.md §Schema Conformance`. Adopters list the actual schemas their bundle exercises. |
| `operationsInScope` | array of strings | Operation names the claim implements. Corresponds to `spec/conformance/baseline-conformance.md §Operation Conformance`. |
| `errorCategoriesInScope` | array of strings | Error categories the claim emits. Corresponds to `spec/conformance/baseline-conformance.md §Error Conformance`. |
| `bundleReference` | object | Pointer to the adopter's adaptation bundle. Required nested keys: `path` (string, e.g., `examples/adaptations/northstar-tool-registry`), `designDoc` (string, path to the bundle's design narrative). Optional nested key: `manifest` (string, path to the bundle's `manifest.json` if one exists). |

### Optional Field

| Field | Type | Description |
|---|---|---|
| `attestation` | object | Evidence-attestation block whose shape is defined by `spec/compliance/evidence-freshness-and-attestation.md §Minimum Evidence Description`. **Optional at the top level.** Adopters MAY omit it entirely. If included, the nested shape is validated: the schema requires the minimum evidence fields (`evidenceId`, `subject`, `evidenceType`, `attestationStatus`, and one of `observedAt`/`collectedAt`). |

The `attestation` field is intentionally optional at the top
level. An adopter who has no attested evidence simply omits the
field; their claim document still validates. An adopter who
includes the field must populate it correctly; the schema rejects
empty or malformed attestation blocks.

### Validation

A claim document validates by passing the JSON Schema at
`models/schemas/conformance-claim.schema.json`. The existing
inline Draft-2020-12 subset validator (the one at
`tools/validate-adaptation-bundle.py`) supports the schema
features used. Adopters MAY validate their own claim with a
one-off invocation that loads the schema and the claim and runs
the same validation function the bundle validator uses
internally. See `examples/conformance-claims/` for worked
examples.

The schema is not registered in `tools/validate-all.py`; the
adopter command surface remains the conformance harness + bundle
validation. Claim validation is a separate, opt-in step the
adopter runs once per published claim.

## Publishing a Claim

Adopters who choose to publish a claim:

1. Author a `claim.json` file conforming to
   `models/schemas/conformance-claim.schema.json`.
2. Validate the file locally (see Validation above).
3. Publish the file alongside their bundle — either committed in
   the adopter's repository or hosted at a stable URL the bundle
   references.

The repository ships three worked examples at
`examples/conformance-claims/`, one per existing reference
adaptation (Northstar, Pinecrest, Helios). Adopters MAY copy and
modify any of them as a starting point.

## Relationship to Other v1 Artifacts

The claim document is a forward reference to the existing v1
artifact set. Each top-level field corresponds to a section in
`baseline-conformance.md`:

| Claim field | baseline-conformance.md section |
|---|---|
| `conformanceLevel` | `§Conformance Levels` |
| `claimElements` | `§Conformance Claim` |
| `schemasInScope` | `§Schema Conformance` |
| `operationsInScope` | `§Operation Conformance` |
| `errorCategoriesInScope` | `§Error Conformance` |

A claim is *coherent* with v1 if every field's value is drawn
from the corresponding section's enumeration. A claim is *valid*
(per JSON Schema) if the document's structure matches the
schema. Coherence is a stronger condition than validity:
adopters SHOULD ensure coherence by hand; the schema enforces
validity automatically.

## Future Evolution

This document is intentionally minimal. Plausible future
extensions, not in scope for v1.x:

- additional profile-specific conformance levels beyond
  `baseline`
- machine-readable `claimElements.evidence` schemas tied to
  specific evidence-type taxonomies
- federated claim signing / cryptographic attestation
- a normative requirement that v1.x adopters publish a claim
  (graduation into the normative artifact set)

Each of these would be a separate AGRP increment with its own
versioning analysis.

## Non-Goals

This template does not:

- impose a publication channel or registry
- mandate any specific transport, signing, or distribution
  mechanism
- create a certification or branding pathway
- modify what AGRP v1 conformance requires
