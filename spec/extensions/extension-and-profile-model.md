# Extension and Profile Model

## Status

This document defines the baseline model for protocol extensions and stricter profiles.

It builds on:

- `spec/conformance/baseline-conformance.md`
- `spec/glossary/protocol-glossary.md`
- `spec/rspl/core-resource-model.md`
- `spec/control-plane/control-plane-contracts.md`
- `spec/security/security-and-policy-model.md`

## Scope

This document is normative for:

- compatible extension rules
- stricter profile rules
- preservation constraints for baseline semantics

It is not normative for:

- profile registry governance
- extension marketplace or packaging
- certification branding

## Compatibility Principle

An extension or profile is baseline-compatible only if it preserves the meaning of all mandatory baseline fields, states, operations, and error categories.

An extension or profile must add constraints, capabilities, or optional structures. It must not redefine baseline semantics.

## Extension Surfaces

The baseline extension surfaces are:

- `extensions` objects in published record shapes
- additional resource kinds
- additional control-plane operations
- additional lifecycle states
- additional metadata or configuration fields

Extensions outside these surfaces are not baseline-compatible unless a later normative document defines them explicitly.

## Field Extension Rules

An implementation may add fields only within designated extension locations or within clearly isolated profile declarations.

An extension field must not:

- shadow a mandatory baseline field name
- change the meaning of a mandatory baseline field
- make a baseline optional field mandatory for all baseline implementations

An implementation that does not understand an extension field should reject it explicitly or ignore it explicitly according to the surrounding artifact rules. It must not silently reinterpret it as baseline meaning.

## Resource Kind Extensions

An implementation may define additional resource kinds.

Additional resource kinds must:

- use distinct identifiers
- preserve baseline identity, versioning, lineage, and audit rules
- be explicitly declared as extensions or profile-specific features

A baseline-conformant implementation is not required to support additional resource kinds.

## Operation Extensions

An implementation may define additional control-plane operations.

Additional operations must not:

- change the meaning of baseline operations
- require baseline callers to use the extension operation in order to remain conformant

An extension operation should declare:

- operation name
- required inputs
- success outputs
- error categories
- compatibility expectations

## Lifecycle State Extensions

An implementation may define additional lifecycle states or state profiles.

Additional states must not invalidate the baseline meaning of:

- `draft`
- `active`
- `deprecated`
- `archived`
- `superseded`
- `restored`

If an implementation adds a state, it must document how that state maps to or preserves baseline lifecycle guarantees.

## Profile Model

A profile is a named, stricter contract layered on top of baseline conformance.

A profile may:

- require a subset of extensions
- forbid certain optional behaviors
- require stronger validation or security rules
- require support for additional operations or resource kinds

A profile must not:

- relax a mandatory baseline rule
- redefine the meaning of a baseline field, operation, state, or error category

## Profile Declaration Rules

A profile declaration should identify:

- `profileId`
- `baseConformance`
- `requiredExtensions`
- `additionalRequirements`
- `forbiddenBehaviors`

If a profile depends on an extension, the dependency must be explicit.

If a profile is incompatible with another profile, that incompatibility should be declared explicitly rather than inferred.

## Conformance Relationship

Baseline conformance and profile conformance relate as follows:

- every profile-conformant implementation must also satisfy baseline conformance
- not every baseline-conformant implementation satisfies a stricter profile

An implementation may claim profile conformance only if it satisfies both:

- the baseline conformance requirements
- the additional profile-specific requirements

## Extension Declaration Guidance

An extension declaration should identify:

- extension identifier
- extension surface
- added fields, kinds, operations, or states
- compatibility notes
- fallback behavior for unsupported implementations

Unsupported extensions should fail clearly rather than degrade silently when semantic correctness would otherwise be lost.

## Preservation Rules

An extension or profile must preserve:

- resource and version identity rules
- append-only lineage semantics
- restore-as-new-version semantics
- baseline error category meaning
- baseline authorization and policy ordering

These preservation rules are non-negotiable for baseline compatibility.

## Example Role

Declarations under `examples/` are non-normative illustrations of how an implementation may describe:

- a compatible extension
- a stricter profile

Their role is descriptive only. They do not create mandatory registry formats.
