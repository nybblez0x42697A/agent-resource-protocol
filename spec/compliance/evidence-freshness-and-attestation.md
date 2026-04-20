# Evidence Freshness and Attestation

## Status

This document defines the baseline evidence freshness and attestation model for readiness and compliance claims.

It builds on:

- `spec/compliance/compliance-and-readiness-profiles.md`
- `spec/compliance/profile-declaration-and-discovery-interoperability.md`
- `spec/compliance/compliance-partial-failure-handling.md`
- `spec/observability/observability-and-trace-correlation.md`

## Scope

This document is normative for:

- baseline freshness-state meanings for supporting evidence
- minimum attestation fields for interoperable evidence descriptions
- interaction between evidence age, attestation status, and compliance outcomes

It is not normative for:

- one evidence repository
- one cryptographic signature format
- auditor accreditation
- one mandatory evidence scoring model

## Purpose

Earlier compliance documents allow readiness or support claims to depend on evidence.

Without a shared model, different consumers may interpret the same evidence inconsistently when it is:

- recent
- stale
- expired
- missing provenance
- not attested by any accountable source

This document creates a baseline model so those distinctions remain interoperable without mandating one evidence product or signature system.

## Evidence Concept

For the purposes of this protocol, evidence is any bounded artifact or reference used to support a readiness, declaration, or compliance claim.

Examples include:

- test results
- diagnostic samples
- rollout records
- governance records
- support references tied to observed behavior
- audit artifacts linked to a profile requirement

Evidence may be stored internally or externally so long as its protocol-visible meaning remains clear when referenced.

## Minimum Evidence Description

An interoperable evidence description should preserve at least:

- `evidenceId`
- `subject`
- `evidenceType`
- `attestationStatus`
- `observedAt` or `collectedAt`
- freshness information, whether directly stated or derivable from policy context

If the evidence is attested, it should also preserve:

- `attestorId`
- `attestedAt`

If the evidence has an explicit expiration or review horizon, it should also preserve:

- `validUntil` or equivalent freshness bound

## Field Meaning

The minimum fields have these meanings:

- `evidenceId`: stable identifier for the evidence artifact or reference
- `subject`: the profile, declaration, capability, implementation surface, or operation being supported
- `evidenceType`: bounded class of evidence such as diagnostic sample, test result, rollout record, or governance record
- `attestationStatus`: whether the evidence is unattested, self-attested, or externally attested
- `observedAt` or `collectedAt`: when the underlying evidence was produced or observed
- `attestorId`: accountable identity of the attesting party when attestation exists
- `attestedAt`: when attestation was issued
- `validUntil`: the timestamp after which the evidence must be treated as expired for the declared context

This document does not require one wire format, only preservation of these meanings.

## Freshness States

The baseline freshness states are:

- `current`
- `stale`
- `expired`
- `undated`

These states may be computed locally from timestamps and policy context or declared directly by a higher-level profile so long as the meanings remain preserved.

### `current`

`current` means the evidence falls within the acceptable freshness window for the relevant claim or consumer policy.

### `stale`

`stale` means the evidence still exists and may remain informative, but it is older than the preferred freshness window for the relevant claim.

Stale evidence does not automatically become invalid, but a consumer may treat it as insufficient for evidence-sensitive decisions.

### `expired`

`expired` means the evidence has passed an explicit validity bound or review horizon and must not be treated as presently sufficient for the affected claim unless a later policy explicitly allows it.

### `undated`

`undated` means the consumer cannot establish when the evidence was collected, observed, or attested.

Undated evidence may still be informative, but it is weak for interoperability-sensitive or assurance-sensitive evaluation.

## Attestation Status

The baseline attestation statuses are:

- `unattested`
- `self_attested`
- `externally_attested`

### `unattested`

`unattested` means no accountable attesting party has been identified for the evidence artifact.

### `self_attested`

`self_attested` means the publishing implementation or steward attests to the evidence using its own accountable identity.

### `externally_attested`

`externally_attested` means an accountable attesting party distinct from the publishing implementation or steward attests to the evidence.

This document does not require that external attestation be superior in every local policy context. It only preserves the distinction.

## Evidence Sufficiency Interaction

Evidence sufficiency depends on:

- the semantics of the claim
- the required evidence type
- the freshness state
- the attestation status
- local policy or profile expectations

This document does not collapse those into one universal sufficiency score.

A consumer may therefore conclude:

- semantically relevant but stale
- current but only self-attested
- externally attested but expired
- present but undated

## Baseline Interpretation Rules

The baseline interpretation rules are:

1. freshness state and attestation status must remain distinct
2. stale evidence must not be silently treated as current evidence
3. expired evidence must not be silently treated as presently sufficient
4. unattested evidence must not be silently presented as externally attested
5. missing or undated timestamps must not be silently replaced with inferred freshness

## Subject Binding

Evidence descriptions should bind clearly to the claim or subject they support.

At minimum, a consumer should be able to determine whether evidence supports:

- baseline conformance
- a readiness profile
- a declaration state
- a specific capability or deployment claim
- an operational event or observed behavior

Evidence should not be reused across unrelated subjects without an explicit mapping.

## Interaction With Readiness Profiles

Readiness profiles may define stricter evidence expectations, including:

- required evidence types
- maximum acceptable evidence age
- required attestation status for some claims

Such stricter requirements are allowed so long as they do not redefine the baseline meanings in this document.

## Interaction With Partial-Failure Handling

When evidence is relevant, partial-failure reporting should preserve at least:

- evidence availability
- freshness state
- attestation status

For example:

- current but unattested evidence
- stale but externally attested evidence
- missing evidence
- expired evidence with otherwise valid declarations

These outcomes must not be collapsed into one generic evidence failure if the distinctions matter to the claim.

## Interaction With Observability

If evidence references include support references, audit identifiers, or diagnostic samples, the implementation should preserve enough identifier continuity to let consumers relate the evidence back to the supporting protocol-visible event.

This does not require exposure of raw internal telemetry.

## Minimal Invalidity Guidance

An interoperable evidence description should be treated as invalid for exchange if it:

- omits `evidenceId`
- omits `subject`
- omits `evidenceType`
- omits `attestationStatus`
- uses `self_attested` or `externally_attested` without an `attestedAt`
- uses `externally_attested` without an `attestorId`
- declares an impossible freshness state transition such as `current` after a passed `validUntil` bound under the same evaluation context

This document does not require one universal validation engine.

## Conformance Notes

A baseline-conformant compliance implementation that uses evidence must:

- preserve the distinction between freshness and attestation
- avoid silently upgrading stale, expired, undated, or unattested evidence into stronger states
- preserve enough metadata for a consumer to evaluate evidence policy in context

It may:

- use stricter local freshness windows
- require stronger attestation for some profiles
- retain richer internal evidence metadata than what is exchanged interoperably

## Example Role

Examples under `examples/evidence-attestations/` are non-normative illustrations of:

- current self-attested evidence
- stale externally attested evidence
- expired evidence for a formerly valid claim

They do not define a mandatory evidence store or signature format.
