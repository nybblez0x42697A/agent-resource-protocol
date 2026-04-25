# Control-Plane Contracts

## Status

This document defines baseline protocol-visible control-plane operations, request and response contracts, and error categories for RSPL resource management.

It builds on:

- `spec/rspl/core-resource-model.md`
- `spec/rspl/registration-and-lineage-model.md`
- `spec/rspl/lifecycle-and-transition-semantics.md`

## Scope

This document is normative for:

- baseline control-plane operation names and responsibilities
- request and response contract structure
- error categories and failure surfaces

It is not normative for:

- transport bindings such as HTTP, RPC, messaging, or CLI
- service topology or deployment architecture
- internal implementation modules

## Contract Style

All operations in this document are protocol-level contracts.

An implementation may realize them through any transport or deployment architecture so long as it preserves:

- operation meaning
- required request fields
- required response fields
- error semantics

## Baseline Operations

The baseline control-plane operations are:

- `RegisterResourceVersion`
- `GetRegistrationRecord`
- `ListResourceVersions`
- `TransitionLifecycleState`
- `RestoreResourceVersion`
- `GetLineage`
- `GetAuditRecord`

## Shared Request Contract

Every control-plane request must provide:

- `operation`: the protocol operation name
- `requestId`: caller-supplied or implementation-generated correlation identifier
- `actor`: protocol-visible caller or delegated actor identity
- `resourceId`: when the operation targets an existing logical resource

Additional operation-specific fields are defined below.

## Shared Response Contract

Every successful control-plane response must provide:

- `operation`: the operation that was executed
- `requestId`: the request correlation identifier
- `result`: operation-specific payload

Every failed control-plane response must provide:

- `operation`
- `requestId`
- `error`: structured error object as defined in the error model below

## Operation Contracts

### `RegisterResourceVersion`

Purpose:

Create a new versioned registration record for a managed resource.

Required request fields:

- `operation`
- `requestId`
- `actor`
- `registrationRecord`
- `auditRecord`

Optional request fields:

- `expectedVersionId`

Success result fields:

- `resourceId`
- `versionId`
- `registrationRecord`
- `lineageNode`

Failure surfaces:

- invalid registration payload
- stale expected version
- duplicate version identity
- policy rejection

### `GetRegistrationRecord`

Purpose:

Read a specific registration record.

Required request fields:

- `operation`
- `requestId`
- `actor`
- `resourceId`
- `versionId`

Success result fields:

- `registrationRecord`

Failure surfaces:

- record not found
- access denied

### `ListResourceVersions`

Purpose:

List versions for a logical resource.

Required request fields:

- `operation`
- `requestId`
- `actor`
- `resourceId`

Optional request fields:

- `statusFilter`

`statusFilter`, when present, matches against `registrationStatus` values; `draft` versions are not discoverable through this operation. Workflow-state concerns (including `draft`) are handled through `TransitionLifecycleState`.

Success result fields:

- `resourceId`
- `versions`

Failure surfaces:

- resource not found
- access denied

### `TransitionLifecycleState`

Purpose:

Perform an allowed lifecycle transition for an existing version.

Required request fields:

- `operation`
- `requestId`
- `actor`
- `resourceId`
- `versionId`
- `expectedVersionId`
- `fromState`
- `toState`
- `rationale`

Optional request fields:

- `evidenceRefs`

Success result fields:

- `resourceId`
- `versionId`
- `fromState`
- `toState`
- `effectiveRegistrationRecord`

Failure surfaces:

- invalid transition
- stale expected version
- conflicting concurrent transition
- policy rejection

### `RestoreResourceVersion`

Purpose:

Create a new version by restoring an earlier version and, if selected, superseding the currently active version.

Required request fields:

- `operation`
- `requestId`
- `actor`
- `resourceId`
- `restoredFromVersionId`
- `expectedVersionId`
- `rationale`
- `evidenceRefs`

Success result fields:

- `resourceId`
- `versionId`
- `registrationRecord`
- `lineageNode`

Failure surfaces:

- restore target not found
- stale expected version
- conflicting concurrent transition
- policy rejection

### `GetLineage`

Purpose:

Read lineage history for a logical resource or specific version.

Required request fields:

- `operation`
- `requestId`
- `actor`
- `resourceId`

Optional request fields:

- `versionId`

Success result fields:

- `resourceId`
- `lineage`

Failure surfaces:

- lineage not found
- access denied

### `GetAuditRecord`

Purpose:

Read audit information for a specific commit or version event.

Required request fields:

- `operation`
- `requestId`
- `actor`

One of:

- `commitId`
- `resourceId` and `versionId`

Success result fields:

- `auditRecord`

Failure surfaces:

- audit record not found
- access denied

## Error Model

Every failed response must include:

- `code`
- `category`
- `message`
- `retryable`

Optional error fields:

- `resourceId`
- `versionId`
- `expectedVersionId`
- `actualVersionId`
- `details`
- `conflictingVersionId`

`actualVersionId`, when present, identifies the version actually observed in the registry at the time of the failed operation; it pairs with `expectedVersionId` to make optimistic-concurrency mismatches diagnosable without re-fetching state.

`details`, when present, carries an open-ended object map of error-context fields the implementation chooses to expose (such as the offending field path, conflicting identifier values, or a structured policy reason); the canonical example is the `details` block in `examples/conformance-vectors/conflict-error.valid.json`.

`conflictingVersionId`, when present, identifies the version that already occupies the version slot or lifecycle position the request expected to write to or transition through. It appears at the top of the `error` object (sibling to `retryable`) for lifecycle-conflict scenarios such as an `expectedVersionId` mismatch — the canonical example is `examples/conformance-vectors/conflict-error.valid.json`.

## Error Categories

Baseline error categories:

- `validation_error`
- `not_found`
- `conflict`
- `policy_denied`
- `access_denied`
- `unsupported_operation`
- `internal_error`

### `validation_error`

The request payload is structurally invalid, semantically incomplete, or violates required field rules.

### `not_found`

The addressed resource, version, lineage entry, or audit record does not exist.

### `conflict`

The request could not be applied because the expected current version or lifecycle base state is stale or has been superseded by another committed transition.

### `policy_denied`

The request is valid but not permitted by policy, approval, or governance rules.

### `access_denied`

The caller is not permitted to inspect or mutate the requested object.

### `unsupported_operation`

The implementation does not support the addressed operation or requested transition.

### `internal_error`

The implementation encountered an unexpected failure while processing an otherwise valid request.

## Separation Rules

To preserve implementation neutrality:

1. operations must be defined by protocol meaning, not by controller module names
2. request and response contracts must not assume a specific transport envelope
3. error categories must remain portable across transports and implementations
4. internal orchestration agents, background jobs, queues, or services must not appear as normative protocol roles unless later standardized explicitly

## Conformance Implications

An implementation conforms to this document if:

1. it exposes the baseline operations or clear equivalent bindings that preserve the same contract meaning
2. it returns the required result fields for successful operations
3. it returns structured errors using the baseline error model and categories
4. it preserves separation between protocol contracts and internal architecture
