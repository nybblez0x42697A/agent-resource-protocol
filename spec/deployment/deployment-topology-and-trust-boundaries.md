# Deployment Topology and Trust Boundaries

## Status

This document defines the baseline deployment topology and trust boundary model for `AGRP v1`.

It builds on:

- `spec/control-plane/control-plane-contracts.md`
- `spec/security/security-and-policy-model.md`
- `spec/observability/observability-and-trace-correlation.md`
- `spec/rollout/rollout-and-stage-policy.md`

## Scope

This document is normative for:

- deployment-visible roles that may be distributed across one or more runtime components
- trust boundaries that affect protocol-visible behavior
- baseline invariants that must hold across different deployment topologies

It is not normative for:

- container, process, or host layout
- orchestration platforms
- deployment automation
- scaling, failover, or traffic-management products
- one mandatory service topology

## Purpose

`AGRP` defines protocol-visible semantics, not one product architecture.

Implementations still need a common way to reason about:

- where protocol requests enter the system
- which deployment element is authoritative for protocol-visible decisions
- where trust boundaries exist
- how internal decomposition must not change the caller-visible contract

This document provides that deployment layer without standardizing one hosting pattern.

## Deployment-Visible Roles

The baseline deployment-visible roles are:

- `protocolEndpoint`
- `resourceAuthority`
- `policyAuthority`
- `auditTraceAuthority`
- `externalDependency`

An implementation may realize multiple roles in one runtime unit or split one role across multiple cooperating units, so long as the protocol-visible invariants remain preserved.

### `protocolEndpoint`

`protocolEndpoint` is the deployment-visible entry point that accepts caller traffic for one or more protocol bindings.

It is responsible for ensuring that the request presented to the rest of the protocol flow preserves:

- operation identity
- actor identity
- request correlation
- binding-specific security context when applicable

### `resourceAuthority`

`resourceAuthority` is the deployment-visible authority that determines the protocol-visible result of resource reads and writes.

The `resourceAuthority` may be implemented by:

- a single registry service
- a controller paired with registry storage
- a gateway that delegates to one or more internal authorities

Regardless of shape, the caller-visible result must remain consistent with the control-plane and lifecycle specifications.

### `policyAuthority`

`policyAuthority` evaluates policy-denial conditions or approval requirements that occur after authorization and before commit when such policy is applied.

`policyAuthority` may be colocated with `resourceAuthority` or delegated to a separate service.

If policy is delegated, the resulting protocol-visible denial semantics must still preserve:

- `access_denied` versus `policy_denied`
- denial ordering
- auditability requirements

### `auditTraceAuthority`

`auditTraceAuthority` is the deployment-visible source of truth for protocol-correlatable audit or support records.

This role does not require one centralized trace backend.

It does require that successful mutations and protocol-visible failures remain correlatable through the identifiers defined by the observability model.

### `externalDependency`

`externalDependency` is any deployment-visible system outside the direct `AGRP` implementation trust boundary that materially affects protocol processing.

Examples include:

- external policy engines
- delegated identity services
- external stores for managed resource material
- upstream service dependencies used to fulfill protocol reads or writes

This role exists to clarify trust and failure boundaries, not to require exposure of internal vendor details.

## Trust Boundaries

The baseline trust boundaries are:

- caller boundary
- internal service boundary
- delegated authority boundary
- external dependency boundary

### Caller Boundary

The caller boundary separates the external client or peer implementation from the first protocol endpoint.

Across this boundary, the implementation must preserve:

- authenticated or otherwise established actor context
- request identity
- binding-visible request integrity

### Internal Service Boundary

The internal service boundary separates cooperating components inside one deployment trust boundary.

Crossing this boundary is allowed to change implementation mechanics, but it must not change:

- operation meaning
- lifecycle semantics
- error category semantics
- correlation semantics

### Delegated Authority Boundary

The delegated authority boundary exists when the deployment relies on a separately operated authority for identity, policy, or other protocol-relevant decisions.

When this boundary is crossed, the implementation must preserve:

- clear attribution of the resulting decision
- bounded failure reporting
- caller-visible semantics defined by the relevant protocol layer

### External Dependency Boundary

The external dependency boundary exists when fulfillment of a request depends on a system that is outside the implementing trust boundary or outside the protocol authority path.

Failures across this boundary may influence diagnostics or retry behavior, but they must not silently redefine protocol meaning.

## Topology Neutrality

This protocol does not require:

- one process per role
- one database per role
- one control-plane per deployment
- a centralized registry service for all adopters

The same deployment may:

- colocate all roles
- split endpoint and authority roles
- shard authorities by namespace or tenant
- front one or more authorities with gateways

These are deployment choices, not compatibility claims by themselves.

## Baseline Deployment Invariants

Regardless of topology, a conformant implementation must preserve the following invariants.

### Operation Invariance

An operation must have the same protocol meaning regardless of whether it is served by one colocated component or a distributed chain of components.

### Authority Invariance

There must be a determinable authority for the protocol-visible outcome of a request.

An implementation must not return mutually inconsistent protocol results for the same addressed operation merely because multiple internal components participated.

### Identity and Correlation Invariance

Actor identity, `requestId`, and resolved resource identifiers must remain stable enough across trusted internal hops to preserve audit and trace continuity.

### Denial and Error Invariance

Topology must not collapse or relabel the baseline distinction between:

- authorization failure
- policy failure
- conflict
- unavailable dependency
- invalid request

Bindings may encode them differently, but the protocol category must remain consistent.

### Bounded Disclosure

An implementation must not be required to expose:

- internal hostnames
- orchestration details
- internal queue or fan-out topology
- vendor-specific infrastructure identities

unless some such detail is already part of a bounded protocol-visible diagnostic or support reference.

## Supported Deployment Patterns

The following baseline patterns are explicitly compatible with `AGRP v1`.

### Colocated Authority Pattern

One deployment unit acts as:

- `protocolEndpoint`
- `resourceAuthority`
- `policyAuthority`
- `auditTraceAuthority`

This pattern is useful for minimal or early-stage implementations.

### Split Control and Registry Pattern

One deployment unit accepts requests and orchestrates workflow, while another authoritative unit persists or resolves registration, lineage, or lifecycle state.

This pattern is compatible so long as the split does not alter control-plane semantics.

### Gateway and Delegated Authority Pattern

A gateway or façade accepts requests and delegates evaluation or fulfillment to one or more downstream authorities.

This pattern is compatible so long as:

- the gateway does not overclaim authority it does not possess
- caller-visible identifiers remain stable enough for correlation
- failure categories remain bounded and truthful

## Interaction With Security

Deployment shape may affect where authentication, authorization, and policy checks occur.

It must not affect:

- the requirement that actor identity is established before protected operations proceed
- the ordering between authorization and policy evaluation
- the denial categories exposed by the protocol

## Interaction With Observability

Distributed deployments may use internal trace systems, but the protocol only requires bounded correlation continuity.

If internal fan-out or delegation occurs, the deployment should still make it possible to correlate:

- incoming request
- resulting mutation or denial
- resulting audit, lineage, or support record

without requiring exposure of the full internal topology.

## Interaction With Rollout and Compliance

Deployment context may impose stricter local requirements on:

- which profiles are required
- which stages may be exposed
- which bindings are permitted

Such stricter deployment requirements are allowed, but they must not redefine the baseline meaning of `AGRP v1` artifacts.

## Conformance Notes

A baseline-conformant deployment must:

- expose a determinable protocol endpoint for supported bindings
- preserve one authoritative protocol-visible outcome per request
- preserve actor, correlation, and error semantics across internal boundaries
- avoid implying that one topology pattern is mandatory for protocol compatibility

It may:

- colocate or distribute deployment-visible roles
- use multiple internal authorities behind one external endpoint
- apply stricter local deployment controls so long as baseline semantics remain intact

## Example Role

Examples under `examples/deployment-topologies/` are non-normative illustrations of:

- a colocated deployment
- a split control and registry deployment

They do not define the only valid deployment shapes for `AGRP`.
