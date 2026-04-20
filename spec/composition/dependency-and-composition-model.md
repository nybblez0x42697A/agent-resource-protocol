# Dependency and Composition Model

## Status

This document defines the baseline dependency and composition model for protocol artifacts.

It builds on:

- `spec/discovery/capability-discovery-and-negotiation.md`
- `spec/versioning/versioning-and-evolution-policy.md`
- `spec/deprecation/deprecation-and-sunset-policy.md`
- `spec/extensions/extension-and-profile-model.md`

## Scope

This document is normative for:

- baseline dependency types
- required versus optional dependency rules
- composition compatibility and failure expectations

It is not normative for:

- execution scheduling
- deployment topology
- runtime orchestration internals

## Purpose

Protocol artifacts often rely on other artifacts.

The dependency model exists so implementations can state:

- what another artifact requires
- what is optional
- how compatibility should be determined across the composed set
- what failure or fallback behavior is acceptable

## Dependency Model

A dependency declaration should identify:

- the dependent artifact
- the target artifact
- dependency type
- whether the dependency is required or optional
- compatibility expectation

This document does not mandate a single wire format for dependency declarations.

## Baseline Dependency Types

The baseline dependency types are:

- `requires`
- `prefers`
- `extends`
- `replaces`

### `requires`

`requires` means the dependent artifact is not semantically valid without the target artifact or a compatible substitute.

### `prefers`

`prefers` means the dependent artifact can operate correctly without the target artifact, but the target improves behavior or capability.

### `extends`

`extends` means the dependent artifact adds compatible behavior on top of a target artifact while preserving the target's baseline meaning.

### `replaces`

`replaces` means the dependent artifact is intended to supersede another artifact as the migration target or successor.

## Required Dependencies

A required dependency must be satisfiable before the composed artifact is treated as compatible for the relevant use.

If a required dependency is:

- unavailable
- incompatible
- sunset without supported exception

then the composition should be treated as incompatible.

## Optional Dependencies

An optional dependency may be absent without invalidating the baseline correctness of the composed artifact.

Optional dependency absence may result in:

- reduced functionality
- dropped optimization
- profile fallback

An implementation should state fallback behavior clearly when optional dependencies are not available.

## Composition Compatibility

A composition is baseline-compatible only if:

1. all required dependencies are compatible
2. all selected extensions and profiles remain baseline-compatible
3. no dependency introduces incompatible semantic redefinition
4. any deprecated or sunset dependency is handled according to the deprecation policy

Compatibility must be evaluated across the composed set, not only per artifact in isolation.

## Dependency Resolution Rules

The baseline dependency resolution rules are:

1. required dependencies are resolved first
2. optional dependencies are selected only after required compatibility is satisfied
3. deprecated dependencies may still resolve if they remain supported
4. sunset dependencies do not resolve unless an explicit compatibility exception is declared

An implementation must not treat an unresolved required dependency as a successful composition.

## Failure Expectations

When a required dependency cannot be satisfied, the implementation should report:

- which dependency failed
- whether the failure was due to absence, incompatibility, or sunset
- whether any baseline-safe substitute exists

The exact error encoding is transport-specific, but the reason should be specific enough to diagnose the composition failure.

## Fallback Expectations

Fallback is permitted only when:

- the dependency was optional, or
- a declared compatible substitute exists for a required dependency

Fallback is not permitted when it would:

- change mandatory baseline semantics
- silently ignore a required dependency
- bypass required security, policy, or lifecycle obligations

## Interaction With Discovery

Capability discovery should expose enough information for another party to understand the composed artifact's relevant dependencies.

Negotiation should treat required dependencies as part of compatibility selection when they affect:

- binding choice
- profile choice
- extension choice
- capability availability

## Interaction With Versioning and Deprecation

Dependency compatibility must account for:

- version compatibility class
- deprecation state
- sunset state

An artifact should not declare a required dependency on a known incompatible major version without also declaring the migration or compatibility exception rules.

## Replacement Guidance

If a dependency is retired or replaced, the composed artifact should identify:

- the preferred replacement
- whether migration is breaking or additive
- whether the old dependency remains supported temporarily

## Example Role

Examples under `examples/` are non-normative illustrations of:

- a composed artifact with required and optional dependencies
- the difference between composition failure and optional fallback

They do not define a mandatory composition registry format.
