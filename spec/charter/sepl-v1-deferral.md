# SEPL v1 Deferral

## Status

This document defines the `AGRP v1` decision to defer self-evolution protocol standardization from the initial release boundary.

It builds on:

- `spec/charter/repository-charter.md`
- `spec/charter/agrp-v1-artifact-set.md`
- `spec/versioning/versioning-and-evolution-policy.md`

## Scope

This document is normative for:

- the decision that `SEPL` is not part of `AGRP v1`
- the rule that `spec/sepl/` remains a future protocol area until a later release explicitly adds it
- the requirement that future `SEPL` standardization be introduced through a later normative release boundary

It is not normative for:

- the content of any future `SEPL` specification
- a roadmap date for self-evolution standardization
- temporary research notes or exploratory design work that remain outside the `v1` boundary

## Purpose

The repository taxonomy reserves space for self-evolution protocol work under `spec/sepl/`.

This document makes explicit that the existence of that directory does not mean self-evolution semantics are already part of the initial protocol release.

`AGRP v1` standardizes the resource substrate and its surrounding operational envelope, not the self-evolution layer.

## Deferral Decision

`SEPL` is not part of `AGRP v1`.

No claim of `AGRP v1` conformance, readiness, or interoperable declaration support should be interpreted as including standardized self-evolution semantics.

## Repository Interpretation Rule

The presence of `spec/sepl/` in the repository expresses future design space, not inclusion in the `v1` release boundary.

A protocol-area directory becomes part of a released standard only when a normative release-boundary document explicitly includes its artifacts.

## Future Introduction Rule

Any future `SEPL` standardization must be introduced through a later normative release that:

- identifies the included `SEPL` artifacts explicitly
- classifies compatibility impact using the protocol versioning rules
- states whether `SEPL` is optional, additive, or release-boundary-defining for that later release

Until such a release exists, `SEPL` remains deferred from the protocol standard even if exploratory material appears in the repository.

## Relationship To AGRP v1

`AGRP v1` should be interpreted as:

- the `AGRP v1` artifact set
- excluding deferred areas such as `SEPL` unless those areas are explicitly listed in the artifact-set definition

## Example Role

This deferral decision exists to prevent accidental scope expansion.

It does not prevent future `SEPL` design work, but it requires that such work be introduced deliberately through later normative release decisions rather than by implication.
