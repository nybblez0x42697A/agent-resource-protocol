# AGRP v1.0.0 Release Definition

## Status

This document defines the first named protocol release for the Agent Resource Protocol.

It builds on:

- `spec/charter/repository-charter.md`
- `spec/charter/agrp-v1-artifact-set.md`
- `spec/charter/sepl-v1-deferral.md`
- `spec/conformance/baseline-conformance.md`
- `spec/versioning/versioning-and-evolution-policy.md`

## Scope

This document is normative for:

- the definition of `AGRP v1.0.0` as a named protocol release
- the rule that `AGRP v1.0.0` is anchored to the `AGRP v1` artifact set
- the interpretation of `AGRP v1.0.0` release claims relative to conformance and later version classification

It is not normative for:

- one mandatory publication manifest format
- repository branching strategy or tag automation
- package-manager release metadata

## Purpose

The repository now defines:

- a normative `AGRP v1` artifact set
- explicit deferral of `SEPL` from `AGRP v1`
- a baseline versioning policy for later changes

This document defines the first named protocol release that binds those decisions into a single release designation.

## Release Definition

`AGRP v1.0.0` is the first named release of the Agent Resource Protocol.

`AGRP v1.0.0` means:

- the `AGRP v1` normative artifact set
- interpreted under the repository charter
- excluding deferred areas such as `SEPL` unless they are explicitly added by a later release

`AGRP v1.0.0` does not mean every file currently present in the repository.

## Release Anchor

The normative anchor for `AGRP v1.0.0` is `spec/charter/agrp-v1-artifact-set.md`.

A claim that references `AGRP v1.0.0` should therefore be interpreted as a claim against:

- the full artifact set listed there
- the artifact-set validity rules defined there
- the related conformance and versioning rules that govern that set

If the artifact set changes, the release meaning changes only through an explicit later versioning decision.

## Relationship To Conformance

Baseline conformance claims made against `AGRP v1.0.0` are anchored to the `AGRP v1` artifact set and the applicable in-scope conformance documents.

An implementation claiming `AGRP v1.0.0` support should therefore be able to say:

- which release it supports: `AGRP v1.0.0`
- which binding, profile, extension, or capability versions it supports in relation to that release
- whether it claims full baseline conformance or a narrower, explicitly named profile layered on top of that release

A subset claim must not be presented as unconstrained `AGRP v1.0.0` support unless a narrower profile or release designation makes that narrower scope explicit.

## Relationship To Deferred Areas

`SEPL` is deferred from `AGRP v1.0.0`.

The existence of `spec/sepl/`, `models/operator-model/`, or exploratory self-evolution material elsewhere in the repository does not add self-evolution semantics to `AGRP v1.0.0`.

Any future release that introduces `SEPL` must do so explicitly and must classify the compatibility impact under the versioning rules.

## Later Version Classification

Later protocol releases must classify their relationship to `AGRP v1.0.0` using the compatibility classes and semantic versioning rules already defined by the protocol.

At minimum:

- clarifications or non-semantic corrections remain patch-level relative to `v1.0.0`
- additive, compatibility-preserving protocol surface may justify a minor release after explicit classification
- breaking semantic changes require a major release

Adding a new normative artifact area to the release boundary is not allowed by implication. It must be classified explicitly as part of the later release definition.

## Release Claim Guidance

When a protocol release is referenced in conformance statements, discovery material, or external documentation, the claim should make the release identifier explicit.

Examples of acceptable claim shapes include:

- `Supports AGRP v1.0.0 baseline semantics`
- `Conformant with AGRP v1.0.0 over the HTTP JSON binding`
- `Implements AGRP v1.0.0 with additional non-core extensions`

Examples of unacceptable claim shapes include:

- `Supports the current repository`
- `Implements AGRP` with no release designation when release-specific meaning matters

## Acronym Transition Note

This release adopts `AGRP` as the short identifier for Agent Resource Protocol in order to avoid collision with the established networking meaning of `ARP`.

Older repository history, planning artifacts, or informal notes may still contain `ARP` as a shorthand for the same protocol work.

Within the published protocol surface, those older shorthand references should be interpreted as historical references to what is now designated `AGRP`, not as a distinct protocol.

## Publication Flexibility

The protocol may be published or mirrored in multiple ways, including tagged releases, release manifests, or external registries.

This document does not require a single publication mechanism.

What is required is that any publication of `AGRP v1.0.0` preserve:

- the release identifier
- the normative anchor to the `AGRP v1` artifact set
- the exclusion of deferred areas unless explicitly added by a later release

## Example Role

Examples under `examples/protocol-releases/` may illustrate one way to express the `AGRP v1.0.0` release boundary.

Those examples are non-normative and exist only to clarify release expression.
