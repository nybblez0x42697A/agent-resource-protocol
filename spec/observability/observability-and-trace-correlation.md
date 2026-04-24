# Observability and Trace Correlation

## Status

This document defines the baseline observability and trace correlation model for protocol interactions.

It builds on:

- `spec/control-plane/control-plane-contracts.md`
- `spec/rspl/registration-and-lineage-model.md`
- `spec/diagnostics/failure-taxonomy-and-diagnostics.md`
- `spec/security/security-and-policy-model.md`

## Scope

This document is normative for:

- baseline correlation identifiers
- baseline trace continuity expectations
- protocol-visible support reference guidance

It is not normative for:

- telemetry storage backends
- tracing vendor formats
- metrics aggregation pipelines

## Purpose

Protocol interactions often span multiple visible artifacts:

- request envelopes
- registration records
- lineage nodes
- audit records
- diagnostics
- support references

The observability model exists so these artifacts can be correlated consistently without mandating a specific telemetry product or backend.

## Correlation Identifiers

The baseline protocol-visible correlation identifiers are:

- `requestId`
- `resourceId`
- `versionId`
- `commitId` or audit event identifier
- support reference when one is exposed

These identifiers serve different roles and should not be conflated.

## Identifier Roles

### `requestId`

`requestId` correlates a caller-visible request and its immediate responses.

It should remain stable across retries or follow-on processing only when the implementation intends them to represent the same logical request attempt.

### `resourceId`

`resourceId` correlates artifacts belonging to the same logical managed resource.

### `versionId`

`versionId` correlates artifacts attached to a specific version of a managed resource.

### `commitId`

`commitId` or equivalent audit event identifier correlates a specific mutation or auditable event across lineage, audit, and diagnostics where applicable.

### Support Reference

A support reference is an implementation-controlled identifier exposed to assist operator support without disclosing raw internal traces.

## Baseline Correlation Rules

An implementation should preserve the relevant identifiers consistently across:

- control-plane request and response envelopes
- lineage and audit artifacts
- diagnostics when a failure is tied to a specific request or mutation

If a failure occurs before a resource or version is resolved, the diagnostic may omit those identifiers while still preserving `requestId`.

## Trace Continuity

Trace continuity means a protocol-visible event can be followed from request initiation to state change or failure using stable identifiers.

At minimum, an implementation should make it possible to correlate:

1. the original request
2. any resulting audit or lineage event
3. any resulting diagnostic or support reference

## Mutation Correlation

When a successful mutation creates or changes a versioned artifact, the implementation should preserve enough information to correlate:

- `requestId`
- `resourceId`
- `versionId`
- `commitId` or audit event identifier

This does not require all fields to appear in every artifact, but the set must be sufficient for cross-reference.

## Failure Correlation

When a request fails, the implementation should preserve:

- `requestId`
- `operation`
- the most specific resolved artifact identifier available
- support reference when available

If a mutation partially progressed before failure, the implementation should ensure any resulting audit or support artifacts can still be correlated to the failed request.

## Support References

If an implementation exposes a support reference, it should be:

- stable enough for operator lookup
- safe to expose to the caller
- distinct from any secret or raw internal trace identifier

A support reference should not require the implementation to expose:

- raw exception stacks
- internal hostnames
- sensitive topology

## Trace Disclosure Boundaries

Protocol-visible observability should remain bounded.

Implementations must not be required to expose internal trace spans, internal queue topology, or infrastructure identifiers if those details are not needed for interoperability or support.

An implementation may correlate those internally, but the protocol-visible model only requires bounded identifiers and references.

## Interaction With Diagnostics

Diagnostics should include:

- `requestId` when available
- relevant artifact identifiers when resolved
- support reference when available and useful

Diagnostics should not invent incompatible identifiers that cannot be reconciled with the rest of the protocol-visible artifacts.

## Interaction With Security

Correlation and observability must respect the bounded disclosure rules from the diagnostics and security model.

An implementation should avoid exposing support references or artifact correlations that would create a security risk for unauthorized parties.

## Conformance Notes

A baseline-conformant implementation must:

- preserve `requestId` semantics across protocol-visible request and response handling
- make successful mutations correlatable to their audit records or lineage nodes
- make failures correlatable to diagnostics and support references when those are exposed

It may:

- use additional internal correlation identifiers
- emit richer telemetry internally than what the protocol exposes

## Example Role

Examples under `examples/` are non-normative illustrations of:

- a successful correlated request lifecycle
- a correlated failure with support reference

They do not define a mandatory tracing backend or storage format.
