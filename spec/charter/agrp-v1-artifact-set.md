# AGRP v1 Artifact Set

## Status

This document defines the normative artifact set that constitutes `Agent Resource Protocol v1`.

It builds on:

- `spec/charter/repository-charter.md`
- `spec/conformance/baseline-conformance.md`
- `spec/versioning/versioning-and-evolution-policy.md`

## Scope

This document is normative for:

- the list of normative documents that constitute `AGRP v1`
- the distinction between the `AGRP v1` artifact set and non-normative support material
- the rule that `v1` conformance claims anchor to this artifact set

It is not normative for:

- packaging or distribution automation
- one mandatory publication manifest format
- future protocol areas that are not part of `AGRP v1`

## Purpose

The repository contains many protocol-area documents.

This document defines which of those documents together constitute `AGRP v1` so that:

- conformance claims have a stable target
- later releases can classify additions and breaks explicitly
- deferred protocol areas are not accidentally treated as part of the initial standard

## AGRP v1 Normative Artifact Set

`AGRP v1` consists of the following normative artifacts:

- `spec/charter/repository-charter.md`
- `spec/glossary/protocol-glossary.md`
- `spec/conformance/baseline-conformance.md`
- `spec/rspl/core-resource-model.md`
- `spec/rspl/registration-and-lineage-model.md`
- `spec/rspl/lifecycle-and-transition-semantics.md`
- `spec/control-plane/control-plane-contracts.md`
- `spec/bindings/http-json-binding.md`
- `spec/security/security-and-policy-model.md`
- `spec/extensions/extension-and-profile-model.md`
- `spec/discovery/capability-discovery-and-negotiation.md`
- `spec/versioning/versioning-and-evolution-policy.md`
- `spec/versioning/agrp-v1-release-definition.md`
- `spec/deprecation/deprecation-and-sunset-policy.md`
- `spec/composition/dependency-and-composition-model.md`
- `spec/diagnostics/failure-taxonomy-and-diagnostics.md`
- `spec/observability/observability-and-trace-correlation.md`
- `spec/rollout/rollout-and-stage-policy.md`
- `spec/deployment/deployment-topology-and-trust-boundaries.md`
- `spec/governance/artifact-governance-and-registry-policy.md`
- `spec/compliance/compliance-and-readiness-profiles.md`
- `spec/compliance/profile-evolution-and-progressive-adoption.md`
- `spec/compliance/profile-declaration-and-discovery-interoperability.md`
- `spec/compliance/declaration-conflict-and-supersession-resolution.md`
- `spec/compliance/compliance-precedence-and-integration-policy.md`
- `spec/compliance/compliance-partial-failure-handling.md`
- `spec/compliance/evidence-freshness-and-attestation.md`

## Normative Role Of The Artifact Set

The `AGRP v1` artifact set is the normative document bundle for `v1` conformance.

A consumer or implementation claiming `AGRP v1` support should interpret the claim as anchored to this set, rather than to every document present anywhere in the repository.

## Artifact-Set Validity

The `AGRP v1` artifact set is valid only if every listed normative artifact:

- exists at the declared location
- is accessible to the consumer evaluating the release boundary
- has not been silently replaced by a different document under the same path without an accompanying normative versioning decision

If a listed artifact is missing or inaccessible, a consumer should treat the `AGRP v1` artifact-set claim as incomplete rather than guessing a substitute.

## Non-Normative And Supporting Material

The following repository material supports `AGRP v1` but is not itself part of the normative `v1` artifact set:

- files under `examples/`
- analysis under `docs/`
- machine-readable artifacts under `models/` unless a normative specification explicitly elevates a specific model artifact to authoritative status
- adopter mappings under `adopters/`

## Deferred And Future Areas

A protocol-area directory listed elsewhere in the repository does not automatically become part of `AGRP v1`.

Only the documents explicitly listed in this artifact-set document are part of the `v1` standard boundary.

Directories or protocol areas with no included artifact-set entries are outside `AGRP v1` until a later normative release explicitly adds them.

An implementation should not claim conformance to only a subset of this artifact set while still presenting that claim as `AGRP v1` conformance in general.

If a narrower profile or subset claim is needed, it should be expressed under an explicitly narrower profile or release designation rather than as full `AGRP v1`.

## Relationship To Conformance

Baseline conformance and higher-layer readiness or declaration claims are all interpreted relative to this artifact set when the claim is made against `AGRP v1`.

An implementation should therefore be able to say that its `AGRP v1` claim refers to this document bundle, not merely to the repository in general.

## Relationship To Later Versions

Later protocol releases may:

- clarify artifacts already in this set
- add new artifacts to the standard boundary
- revise or replace artifacts in this set

Those later releases must classify compatibility impact using the applicable protocol versioning rules rather than silently redefining what `AGRP v1` meant.

## Artifact-Set Amendment Rule

Adding, removing, or replacing a normative artifact in this set is itself a normative release-boundary change.

Such a change must therefore:

- be made through an explicit normative increment
- identify the affected artifact-set entry or entries
- classify the compatibility impact using the applicable protocol versioning rules
- update this artifact-set document rather than relying on repository structure alone

## Example Role

Examples under `examples/` may illustrate the `AGRP v1` artifact set in a manifest-like form.

Those examples are non-normative and exist only to help implementers understand the release boundary.
