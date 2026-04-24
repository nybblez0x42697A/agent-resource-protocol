# Compliance Partial Failure Handling

## Status

This document defines how consumers interpret and report mixed outcomes across the compliance stack when some layers succeed and others fail, remain unresolved, or are only partially evidenced.

It builds on:

- `spec/conformance/baseline-conformance.md`
- `spec/compliance/compliance-precedence-and-integration-policy.md`
- `spec/compliance/compliance-and-readiness-profiles.md`
- `spec/compliance/profile-declaration-and-discovery-interoperability.md`
- `spec/compliance/declaration-conflict-and-supersession-resolution.md`

## Scope

This document is normative for:

- common mixed compliance outcome patterns
- summary rules for multi-layer partial failures
- evidence incompleteness handling at the compliance layer

It is not normative for:

- scoring systems
- audit-provider workflows
- one mandatory UI vocabulary

## Purpose

The compliance stack distinguishes:

- baseline conformance
- readiness semantics
- declaration validity
- declaration-resolution outcomes

Real systems can satisfy some of those layers while failing others.

This document defines how to preserve that distinction when outcomes are mixed, rather than collapsing them into one misleading status.

## Main Partial-Failure Scenarios

The main mixed-outcome scenarios include:

- baseline conformance passes, but no valid readiness declaration exists
- baseline conformance passes, readiness semantics would support a profile, but the published declaration is invalid
- baseline conformance passes, declaration is valid, but the declaration set is `conflicted` or `unresolved`
- baseline conformance passes, readiness claim exists, but required supporting evidence is incomplete or missing
- baseline conformance fails, while higher-layer declarations still claim readiness support

## Baseline Failure Dominance

If baseline conformance fails, higher-layer readiness claims must not be treated as validly supported, regardless of declaration contents.

In that case, partial-failure reporting should preserve the fact that a readiness declaration may have been published, but the consumer must not elevate it into a valid support claim.

## Semantic Support Versus Declaration Failure

If a consumer has reason to believe that semantic readiness requirements are met, but the interoperable declaration is invalid or absent, the consumer may report:

- semantic readiness appears satisfied
- interoperable declaration support is invalid, absent, or incomplete

The consumer must not collapse those into a single `supported` claim for interoperable exchange.

## Resolution Failure Without Semantic Failure

If a declaration set is `conflicted` or `unresolved`, that outcome means the declaration layer failed to establish a unique current interoperable claim.

It does not by itself prove:

- baseline non-conformance
- semantic non-support of the readiness profile

Consumers should therefore preserve both facts when known:

- the semantic support assessment
- the declaration-resolution failure

## Missing Or Incomplete Evidence

If a readiness or declaration claim depends on evidence that is missing, stale, or incomplete, the consumer should distinguish between:

- claim semantics
- claim evidence sufficiency

An evidence failure does not automatically rewrite the meaning of the readiness profile, but it may prevent the consumer from accepting the claim as sufficiently substantiated for its own context.

## Evidence Interaction Rule

If required evidence is missing or incomplete, a consumer may report the claim as:

- semantically plausible but insufficiently evidenced
- interoperably declared but insufficiently evidenced

The consumer should not treat missing evidence as equivalent to a declaration conflict unless the evidence gap itself invalidates a required declaration field or resolution input.

## Summary Rule

When mixed outcomes exist, the consumer should summarize them by preserving at least:

- baseline conformance status
- readiness semantic status
- declaration validity status
- declaration-resolution status
- evidence sufficiency status, when evidence is relevant

A consumer should not collapse those statuses into a single yes/no claim unless a higher-level profile explicitly defines such a collapse.

## Overstatement Prohibition

If any higher-layer is invalid, unresolved, or insufficiently evidenced, the consumer must not summarize the system as fully and uniquely supported at that higher-layer.

For example:

- semantic readiness plus invalid declaration is not the same as interoperable supported readiness
- valid declaration plus unresolved declaration set is not the same as uniquely current declaration support
- valid semantics plus missing evidence is not the same as sufficiently substantiated readiness support

## Minimal Mixed-Outcome Vocabulary

Consumers should preserve distinct mixed-outcome labels or equivalent concepts for at least:

- `baseline_failed`
- `semantically_supported`
- `declaration_invalid`
- `declaration_absent`
- `declaration_conflicted`
- `declaration_unresolved`
- `evidence_incomplete`

This document does not require those exact strings on the wire, but it requires preservation of those distinctions.

## Example Role

Examples under `examples/` are non-normative illustrations of:

- a semantically supported profile with invalid declaration metadata
- a valid declaration set with incomplete evidence

They do not define a mandatory reporting schema.
