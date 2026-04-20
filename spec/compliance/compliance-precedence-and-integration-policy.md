# Compliance Precedence and Integration Policy

## Status

This document defines how the compliance sub-specifications compose and which document governs when their concerns overlap.

It builds on:

- `spec/conformance/baseline-conformance.md`
- `spec/compliance/compliance-and-readiness-profiles.md`
- `spec/compliance/profile-evolution-and-progressive-adoption.md`
- `spec/compliance/profile-declaration-and-discovery-interoperability.md`
- `spec/compliance/declaration-conflict-and-supersession-resolution.md`

## Scope

This document is normative for:

- the role of each compliance sub-specification
- the order in which compliance questions should be evaluated
- precedence rules when readiness, declaration, and resolution concerns overlap

It is not normative for:

- certification programs
- commercial scoring models
- local UI presentation of compliance outcomes

## Purpose

The repo now defines multiple layers of compliance behavior:

- baseline protocol conformance
- readiness profiles above baseline
- evolution and progressive adoption of readiness profiles
- interoperable declaration metadata
- conflict and supersession resolution for declaration sets

This document defines how those layers fit together so consumers do not invent their own precedence rules.

## Compliance Layers

The compliance stack is:

1. baseline conformance
2. readiness profile semantics
3. readiness profile evolution and progressive adoption
4. declaration interoperability
5. declaration conflict and supersession resolution

Each later layer depends on the earlier layers but does not replace them.

## Role Of Each Document

The documents in this stack answer different questions:

- `baseline-conformance.md`: does the implementation preserve protocol semantics at all
- `compliance-and-readiness-profiles.md`: what higher operational maturity claims exist above baseline
- `profile-evolution-and-progressive-adoption.md`: how readiness profiles evolve over time and how partial adoption is represented honestly
- `profile-declaration-and-discovery-interoperability.md`: what minimum metadata and support-state values interoperable declarations must carry
- `declaration-conflict-and-supersession-resolution.md`: whether a declaration set can be resolved into a unique current declaration

## Evaluation Order

A consumer evaluating compliance information should use this order:

1. evaluate baseline conformance
2. if baseline conformance is absent or invalid, do not treat readiness support claims as valid
3. identify which readiness profile is being claimed or targeted
4. interpret that profile using the readiness semantics and evolution rules
5. validate any declaration metadata used to publish the claim
6. if multiple declarations exist, run declaration conflict and supersession resolution
7. only after a unique current declaration exists may a consumer treat the declaration as the current interoperable statement of support

## Baseline Precedence

Baseline conformance always takes precedence over any readiness or declaration-layer claim.

If an implementation is not baseline conformant, it may not be treated as validly supporting a readiness profile even if a declaration claims otherwise.

## Readiness Semantics Precedence

The readiness profile documents govern:

- what a profile means
- what counts as progressive adoption
- when full support may be claimed

The declaration documents do not change readiness semantics. They only govern how those claims are represented and resolved across interoperable systems.

If a declaration conflicts with readiness semantics, readiness semantics take precedence and the declaration should be treated as invalid or misleading.

## Declaration Validity Precedence

Interoperable declaration rules govern whether a claim is representable in interoperable exchange.

If a declaration omits required metadata, uses invalid support-state combinations, or violates declaration validation rules, the declaration should not be treated as a valid interoperable claim even if the underlying implementation might still be baseline conformant.

## Resolution Outcome Precedence

Resolution outcomes govern whether a declaration set yields a unique current declaration.

If declaration resolution yields:

- `conflicted`
- `unresolved`

then consumers should not promote any declaration in that set as the unique current interoperable claim.

This does not by itself prove that the implementation lacks baseline conformance or lacks readiness capability. It only means the interoperable declaration set failed to establish a unique current claim.

## Readiness Support Versus Resolution Outcome

Readiness support and declaration resolution are different questions:

- readiness support asks whether the implementation satisfies the profile semantics
- declaration resolution asks whether the published declaration set establishes a unique current interoperable statement of that support

An implementation may therefore be:

- baseline conformant
- semantically ready for a profile
- but operationally `conflicted` or `unresolved` at the declaration layer

Consumers should not collapse those questions into one status.

## Progressive Adoption Interaction

If a declaration uses progressive-adoption semantics such as `adopting`, the progressive-adoption rules determine whether the declaration is honest.

The resolution rules then determine whether that declaration is the unique current interoperable statement for the relevant identity scope.

## Overlap Resolution Rules

If multiple compliance documents appear to speak to the same situation, precedence should be:

1. baseline conformance semantics
2. readiness profile semantics
3. readiness evolution and progressive adoption semantics
4. declaration interoperability constraints
5. declaration conflict and supersession resolution outcomes

Later items may refine representational or selection behavior, but they may not redefine the meaning of an earlier layer.

## Discovery Interpretation Guidance

Discovery consumers should interpret compliance information in this order:

- first determine whether a unique current declaration exists
- then read the declaration support state
- then interpret that support state according to readiness semantics

If no unique current declaration exists, discovery should surface the resolution failure rather than pretending a current declaration was selected.

## Example Role

Examples under `examples/` are non-normative illustrations of:

- integrated compliance evaluation
- explicit precedence in the presence of declaration conflicts

They do not define a mandatory UI or reporting format.
