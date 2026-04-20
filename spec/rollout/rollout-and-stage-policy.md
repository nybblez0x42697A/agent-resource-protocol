# Rollout and Stage Policy

## Status

This document defines the baseline rollout and staged enablement policy for protocol artifacts.

It builds on:

- `spec/discovery/capability-discovery-and-negotiation.md`
- `spec/versioning/versioning-and-evolution-policy.md`
- `spec/deprecation/deprecation-and-sunset-policy.md`
- `spec/extensions/extension-and-profile-model.md`

## Scope

This document is normative for:

- baseline rollout stages
- stage meanings for protocol-visible artifacts
- interaction between rollout stage, discovery, and compatibility claims

It is not normative for:

- release automation
- deployment rings or traffic percentages
- organization-specific launch process

## Purpose

Not every artifact should become generally available at the moment it first appears.

The rollout model exists so implementations can expose staged availability clearly while preserving compatibility expectations and avoiding ambiguous support signals.

## Baseline Rollout Stages

The baseline rollout stages are:

- `preview`
- `limited`
- `general_availability`
- `withdrawn`

### `preview`

`preview` means the artifact is exposed for early evaluation and may change more rapidly than stable generally available artifacts.

Preview artifacts should not be implied as baseline-required.

### `limited`

`limited` means the artifact is available for constrained use or selected adopters, but is not yet generally available for all compatible implementations.

### `general_availability`

`general_availability` means the artifact is available for normal supported use under the current baseline policy.

### `withdrawn`

`withdrawn` means the staged artifact is no longer being offered as part of the rollout path.

Withdrawn is distinct from deprecation or sunset. A staged artifact may be withdrawn before ever reaching general availability.

## Stage Meaning

Rollout stage communicates support posture, not semantic truth.

An artifact's stage does not change:

- the meaning of a baseline operation
- the meaning of a profile, binding, or extension identifier
- the version compatibility rules already defined elsewhere

## Discovery Interaction

If an implementation advertises an artifact, it should also advertise its rollout stage when that stage is not `general_availability`.

Discovery should make it possible to distinguish:

- a generally available artifact
- a staged preview or limited artifact
- a withdrawn artifact that is no longer offered

An artifact in `preview` or `limited` may be advertised, but the advertisement should not imply universal support.

## Compatibility Claims

Preview and limited artifacts may still be compatible within their declared scope, but they should not be treated as baseline-required.

An implementation must not claim that another party is non-conformant merely because it does not support a `preview` or `limited` artifact.

Only `general_availability` artifacts may reasonably be treated as candidates for broad interoperable expectation.

## Interaction With Profiles and Extensions

Profiles and extensions may move through rollout stages independently.

A profile or extension in `preview`:

- may be negotiated only when both parties support it
- should not be assumed by default
- should be discoverable as staged rather than stable

A profile or extension in `general_availability` may still remain optional unless separately required by conformance or deployment context.

## Interaction With Versioning

Rollout stage is not a substitute for versioning.

An implementation must not use rollout stage to hide breaking semantic change under a stable version or identifier.

If a preview artifact changes incompatibly, it should still follow the versioning and identifier rules defined elsewhere.

## Interaction With Deprecation

Rollout stage and retirement state are separate concepts.

Typical patterns include:

- `preview` to `limited`
- `limited` to `general_availability`
- `general_availability` to `deprecated`
- `preview` to `withdrawn`

An artifact may be withdrawn before it is deprecated if it never achieved stable support expectations.

## Stage Progression Expectations

When an artifact changes rollout stage, the publisher should communicate:

- artifact identifier
- new stage
- effective date
- compatibility notes when relevant

If a stage change implies changed support expectations, those expectations should be stated explicitly.

## Withdrawal Expectations

When an artifact is withdrawn:

- it should no longer be advertised as available unless retained under an explicit exception
- negotiation should not select it unless a compatibility exception is declared
- any recommended replacement should be identified when one exists

## Conformance Notes

A baseline-conformant implementation must:

- avoid implying that `preview` or `limited` artifacts are universally required
- advertise staged artifacts truthfully when it advertises them at all
- keep rollout stage signals distinct from deprecation and versioning semantics

It may:

- choose not to expose staged artifacts in discovery
- retain implementation-specific stage names internally, so long as the baseline meanings remain clear when exposed

## Example Role

Examples under `examples/` are non-normative illustrations of:

- a staged preview artifact
- a completed rollout to general availability

They do not define a mandatory publication or discovery format.
