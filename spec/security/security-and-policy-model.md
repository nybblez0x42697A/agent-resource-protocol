# Security and Policy Model

## Status

This document defines the baseline security and policy model for control-plane operations.

It builds on:

- `spec/control-plane/control-plane-contracts.md`
- `spec/rspl/lifecycle-and-transition-semantics.md`
- `spec/conformance/baseline-conformance.md`
- `spec/bindings/http-json-binding.md`

## Scope

This document is normative for:

- baseline actor identity requirements for control-plane operations
- the distinction between authentication, authorization, and policy evaluation
- denial behavior for `access_denied` and `policy_denied`
- minimum audit expectations for denied operations

It is not normative for:

- concrete identity providers or credential formats
- cryptographic algorithms
- network perimeter design
- tenant model or organization hierarchy

## Security Model Goals

The baseline security model exists to ensure that protocol-visible operations:

- are attributable to an actor
- are authorized before they mutate or reveal protected protocol state
- are evaluated against policy before protected transitions are committed
- emit denial outcomes in a way that remains consistent across transports

## Actor Model

Every control-plane operation must execute in the context of a protocol-visible actor.

At minimum, an actor must be representable as:

- a stable actor identifier
- an actor type

The baseline actor types are:

- `user`
- `service`
- `delegate`

Implementations may define additional actor types, but they must not redefine the meaning of these baseline types.

## Authentication Boundary

Authentication establishes the identity bound to the protocol-visible actor.

This protocol does not standardize how authentication is performed. An implementation may use any credential or trust mechanism so long as the resulting actor identity is established before authorization and policy evaluation occur.

If actor identity cannot be established, the operation must not proceed.

This document does not define a protocol-specific unauthenticated error category. Transport bindings may represent unauthenticated requests using transport-specific behavior, but once a protocol-visible denial is emitted, it must preserve the baseline error categories defined by the control-plane contract.

## Authorization Model

Authorization answers whether the actor may attempt the operation against the addressed protocol object.

Authorization is evaluated against:

- operation type
- resource identity
- version identity when applicable
- actor identity and actor type

Authorization must happen before any state-changing operation is committed.

If the actor is not permitted to attempt the operation, the operation must fail with:

- error category: `access_denied`

An `access_denied` result means the actor lacks permission to perform or read the targeted operation at all.

## Policy Model

Policy evaluation answers whether a permitted operation is allowed under contextual or governance rules.

Policy may consider:

- requested lifecycle transition
- evidence references
- rationale quality
- environment or deployment constraints
- change-management requirements
- organizational risk controls

Policy evaluation occurs after the actor is authorized to attempt the operation and before the operation is committed.

If policy rejects the operation, the operation must fail with:

- error category: `policy_denied`

A `policy_denied` result means the actor was permitted to attempt the operation, but the requested action was blocked by higher-level rules or evaluation criteria.

## Denial Ordering

The baseline denial ordering is:

1. establish actor identity
2. evaluate authorization
3. evaluate policy when the operation is otherwise permitted
4. commit the operation only if all prior checks succeed

An implementation must not emit `policy_denied` for an actor that was not authorized to attempt the operation in the first place.

## Interaction With Lifecycle Operations

Lifecycle-affecting operations such as `TransitionLifecycleState` and `RestoreResourceVersion` are security-sensitive.

For these operations, implementations should evaluate policy at least on:

- activation to `active`
- deprecation
- archival
- restore requests

The policy model may require:

- rationale text
- evidence references
- human review or delegated approval

Such requirements are baseline-compatible so long as the operation semantics and denial categories remain unchanged.

## Interaction With Read Operations

Read operations such as `GetRegistrationRecord`, `ListResourceVersions`, `GetLineage`, and `GetAuditRecord` must also evaluate authorization.

If the actor may not view the addressed data, the operation must fail with `access_denied`.

Policy evaluation for reads is optional in the baseline model. If an implementation applies policy to reads and a permitted read is blocked by policy, the denial must use `policy_denied`.

## Denial Audit Requirements

A denied operation must be auditable even when it does not create or mutate a versioned resource.

At minimum, a denial audit record should preserve:

- actor identity
- attempted operation
- addressed resource identity when known
- denial category
- rationale or denial explanation
- timestamp

The denial audit artifact may be transport-specific or implementation-specific, but the denial category must remain consistent with the baseline error model.

## Error Surface Requirements

When a protocol-visible denial is returned, the structured error object must contain:

- `category`
- `message`

It should also contain enough detail to distinguish:

- permission failure
- policy failure
- retryable versus non-retryable policy conditions

Implementations must not leak security-sensitive internals in denial details when doing so would create a security risk.

## Binding Guidance

Transport bindings may encode authentication and actor propagation differently, but they must preserve:

- the protocol-visible actor identity used for authorization and policy
- the distinction between `access_denied` and `policy_denied`
- the requirement that denials happen before commit

For the HTTP JSON binding, a transport may use headers or other transport-native credential mechanisms, but the resulting actor identity remains the security subject for protocol evaluation.

## Conformance Notes

A baseline-conformant implementation must:

- establish actor identity before protected operations proceed
- evaluate authorization for all protected reads and writes
- use `access_denied` for authorization failures
- use `policy_denied` for policy failures after authorization succeeds
- preserve auditable denial outcomes
