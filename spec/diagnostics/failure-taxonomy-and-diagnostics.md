# Failure Taxonomy and Diagnostics

## Status

This document defines the baseline failure taxonomy and diagnostics model for protocol artifacts and operations.

It builds on:

- `spec/control-plane/control-plane-contracts.md`
- `spec/security/security-and-policy-model.md`
- `spec/discovery/capability-discovery-and-negotiation.md`
- `spec/composition/dependency-and-composition-model.md`

## Scope

This document is normative for:

- baseline failure classes
- baseline diagnostic fields
- disclosure and redaction rules for bounded diagnostics

It is not normative for:

- transport-specific logging systems
- implementation-internal tracing formats
- observability product integration

## Purpose

The failure taxonomy exists to make cross-cutting failures understandable and comparable across protocol layers.

The diagnostics model exists to ensure that failures are:

- actionable to implementers
- consistent across transports
- bounded enough to avoid unnecessary disclosure

## Failure Classes

The baseline failure classes are:

- `validation_failure`
- `compatibility_failure`
- `policy_failure`
- `access_failure`
- `lifecycle_failure`
- `composition_failure`
- `internal_failure`

### `validation_failure`

The request or artifact shape is invalid, incomplete, or semantically malformed before compatibility or policy can be evaluated.

### `compatibility_failure`

The required binding, profile, extension, version, or capability set cannot be satisfied.

### `policy_failure`

The actor was authorized to attempt the action, but policy evaluation denied it.

### `access_failure`

The actor was not permitted to attempt or read the requested operation or artifact.

### `lifecycle_failure`

The requested state transition, restore, or mutation conflicts with lifecycle rules or the currently selected version state.

### `composition_failure`

Required dependencies or composed artifact expectations cannot be satisfied.

### `internal_failure`

The implementation encountered an internal condition that prevented correct completion, and the failure is not more specifically classifiable above.

## Relationship To Existing Error Categories

Transport or operation-specific error categories may continue to exist, but they should map clearly to the failure classes in this document.

For example:

- `validation_error` maps to `validation_failure`
- `conflict` may map to `lifecycle_failure`, `compatibility_failure`, or `composition_failure` depending on the cause
- `policy_denied` maps to `policy_failure`
- `access_denied` maps to `access_failure`
- `internal_error` maps to `internal_failure`

## Diagnostic Fields

A diagnostic object should preserve the following fields when available:

- `failureClass`
- `message`
- `requestId`
- `operation`
- `artifactId` or `resourceId`
- `reasonCode`
- `retryable`

It may also preserve:

- `versionId`
- `bindingId`
- `profileId`
- `extensionId`
- `dependencyId`
- `details`

## Reason Codes

Implementations should use stable reason codes for machine-usable failure interpretation.

A reason code should:

- be stable within the implementation or profile
- identify the immediate cause category
- avoid embedding sensitive data directly

Examples include:

- `missing_required_capability`
- `deprecated_artifact_required`
- `policy_evidence_missing`
- `lifecycle_transition_not_allowed`
- `dependency_incompatible`

## Actionability Rules

Diagnostics should be actionable enough that an interoperating party can determine:

- whether retry is meaningful
- whether a different capability or fallback can be chosen
- whether migration is required
- whether the failure is likely caller-correctable

## Disclosure Rules

Diagnostics must not disclose more implementation detail than necessary to support interoperability and debugging.

An implementation should avoid exposing:

- secrets or credentials
- internal topology that is not needed for diagnosis
- sensitive policy internals that would create a security risk
- raw stack traces in protocol-visible error bodies

## Bounded Internal Failure Reporting

For `internal_failure`, the protocol-visible diagnostic should remain bounded.

It should include:

- a stable reason code
- request correlation
- whether retry may help
- an implementation-controlled support reference when available

It should not require the implementation to expose raw internal traces or exception dumps.

## Compatibility Failure Reporting

For `compatibility_failure`, the diagnostic should identify:

- what required capability or version could not be satisfied
- whether a baseline-safe fallback exists
- which category of capability failed, such as binding, profile, extension, or version

## Composition Failure Reporting

For `composition_failure`, the diagnostic should identify:

- which required dependency failed
- whether the failure was absence, incompatibility, or sunset
- whether an optional fallback path exists

## Retry Guidance

The `retryable` field should indicate whether retrying the same request without meaningful change is likely to succeed.

Examples:

- `policy_failure` due to missing evidence is not retryable until inputs change
- transient `internal_failure` may be retryable
- `compatibility_failure` is not retryable unless capability selection changes

## Conformance Notes

A baseline-conformant implementation must:

- classify failures consistently enough to preserve the meanings above
- include bounded actionable diagnostics for protocol-visible failures
- avoid exposing sensitive internal detail in protocol-visible error bodies

It may:

- add transport-specific or implementation-specific fields
- map finer-grained local errors into the baseline failure classes

## Example Role

Examples under `examples/` are non-normative illustrations of:

- a compatibility failure diagnostic
- a bounded internal failure diagnostic

They do not define a mandatory wire format beyond the principles in this document.
