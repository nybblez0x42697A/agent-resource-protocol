# Artifact Governance and Registry Policy

## Status

This document defines the baseline governance and registry policy for protocol artifact identifiers and namespaces.

It builds on:

- `spec/charter/repository-charter.md`
- `spec/extensions/extension-and-profile-model.md`
- `spec/versioning/versioning-and-evolution-policy.md`
- `spec/rollout/rollout-and-stage-policy.md`

## Scope

This document is normative for:

- baseline identifier stewardship rules
- namespace reservation and delegation concepts
- the distinction between protocol governance and ecosystem-specific registry operation

It is not normative for:

- operation of a mandatory central registry service
- commercial approval programs
- vendor-specific marketplace policy

## Purpose

The protocol now defines multiple artifact classes that need stable identifiers:

- bindings
- profiles
- extensions
- capability identifiers

This policy exists to prevent identifier collision and ambiguity while avoiding unnecessary centralization of implementation ownership.

## Governance Principle

Protocol governance is responsible for:

- defining identifier rules
- reserving core namespaces
- documenting delegation boundaries

Protocol governance is not required to operate every ecosystem registry or marketplace that may use those identifiers.

## Baseline Artifact Identifier Scope

The baseline governed identifier surfaces are:

- binding identifiers
- profile identifiers
- extension identifiers
- capability identifiers when they are standardized or widely reused

Identifiers that are purely local to one implementation may remain implementation-specific, but they should avoid collision with reserved protocol namespaces when exposed externally.

## Reserved Namespaces

The protocol should reserve namespaces for:

- core protocol artifacts
- officially documented example or reference identifiers
- future standards-track identifiers

Reserved namespaces should not be reused for unrelated implementation-local identifiers.

## Delegated Namespaces

The protocol may delegate a namespace to an organization, community, or ecosystem steward.

Delegation should identify:

- delegated namespace prefix
- responsible steward
- stewardship scope
- whether subdelegation is permitted

Delegation does not transfer the meaning of core reserved namespaces.

## Reservation Rules

A reserved identifier should:

- be stable
- identify one artifact meaning clearly
- not be repurposed for incompatible semantics

If an artifact changes incompatibly, the identifier or its visible major-version component should change according to the versioning policy.

## Publication Boundaries

This repository may define:

- reserved namespace rules
- delegated namespace rules
- example identifiers
- standards-track artifact identifiers

This repository does not need to define:

- every ecosystem-specific artifact listing
- every vendor-specific identifier policy
- every deployment-specific registry instance

## Delegation Boundaries

Delegated stewards may define identifiers within their delegated namespace so long as they do not:

- collide with reserved core namespaces
- redefine baseline semantics under a conflicting identifier
- claim standards-track status without the relevant protocol governance process

## Standards-Track Versus Ecosystem-Specific

The baseline distinction is:

- standards-track identifiers: governed directly by this protocol's published rules
- ecosystem-specific identifiers: governed by delegated or external ecosystems

An ecosystem-specific artifact may still be baseline-compatible, but that does not automatically make it standards-track.

## Registry Policy Versus Registry Service

Registry policy defines the rules for names, ownership, reservation, and delegation.

Registry service operation is implementation-specific unless a later normative document standardizes one.

This document standardizes the policy layer, not the service layer.

## Conflict Handling

If two artifacts attempt to claim the same externally visible identifier with incompatible meaning, the conflict should be resolved by the relevant namespace steward.

If the conflict occurs under a core reserved namespace, protocol governance should treat it as invalid and require one of the claims to change.

## Conformance Notes

A baseline-conformant implementation must:

- avoid reusing reserved identifiers for incompatible meanings
- distinguish standards-track and ecosystem-specific identifiers honestly
- respect delegated namespace boundaries when publishing externally visible identifiers

It may:

- maintain private local identifiers internally
- operate ecosystem-specific registries or catalogs under delegated namespaces

## Example Role

Examples under `examples/` are non-normative illustrations of:

- a reserved identifier declaration
- a delegated namespace policy

They do not define a mandatory registry backend or approval workflow.
