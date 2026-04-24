# HTTP JSON Binding

## Status

This document defines a normative HTTP and JSON binding for the baseline control-plane contracts.

It builds on:

- `spec/control-plane/control-plane-contracts.md`
- `spec/rspl/core-resource-model.md`
- `spec/rspl/registration-and-lineage-model.md`
- `spec/rspl/lifecycle-and-transition-semantics.md`

## Scope

This document is normative for:

- URI and method mappings for the baseline control-plane operations
- JSON request and response envelope structure
- HTTP status code mapping for baseline error categories

It is not normative for:

- authentication mechanisms
- deployment topology
- caching, retries, or gateway policy
- any serialization other than JSON

## Binding Principles

The HTTP binding must preserve the operation meaning defined in `spec/control-plane/control-plane-contracts.md`.

An HTTP implementation must not:

- change the required operation-specific fields
- introduce transport-visible state transitions that do not exist in the protocol
- redefine protocol error categories

An HTTP implementation may:

- add transport headers for authentication, tracing, or observability
- add pagination query parameters for collection reads
- add implementation-specific metadata fields inside `extensions`

## Media Type

Requests and responses in this binding use JSON.

Implementations should use:

- `Content-Type: application/json`
- `Accept: application/json`

## Shared Envelope Rules

### Request Envelope

Every HTTP request body for an operation in this binding must contain the transport-neutral request fields required by that operation.

The `operation` field remains present in the JSON body even when the URI already implies the operation. This preserves contract consistency across transports.

The `requestId` field remains part of the JSON body. An implementation may also copy it into an HTTP header for tracing, but the JSON field remains canonical for protocol purposes.

### Success Response Envelope

Every successful HTTP response body must contain:

- `operation`
- `requestId`
- `result`

### Error Response Envelope

Every failed HTTP response body must contain:

- `operation` when available
- `requestId` when available
- `error`

The `error` object must contain:

- `code`
- `category`
- `message`
- `retryable`

The `error` object may contain:

- `details`
- `conflictingVersionId`

## Resource Addressing Model

This binding uses the following baseline URI patterns:

- `/v1/resources`
- `/v1/resources/{resourceId}`
- `/v1/resources/{resourceId}/versions`
- `/v1/resources/{resourceId}/versions/{versionId}`
- `/v1/resources/{resourceId}/lineage`
- `/v1/audit/{auditEventId}`

The `/v1/` prefix is the binding version for this HTTP document, not the protocol semantic version.

## Operation Bindings

### `RegisterResourceVersion`

HTTP mapping:

- Method: `POST`
- URI: `/v1/resources/{resourceId}/versions`

Request body:

- `operation`
- `requestId`
- `actor`
- `registrationRecord`
- `auditRecord`
- `expectedVersionId` when optimistic concurrency is used

Success response:

- Status: `201 Created`
- Body: success envelope with `resourceId`, `versionId`, `registrationRecord`, and `lineageNode`

### `GetRegistrationRecord`

HTTP mapping:

- Method: `GET`
- URI: `/v1/resources/{resourceId}/versions/{versionId}`

Request body:

- no request body is required

Required query parameters or headers:

- `requestId`
- actor identity as defined by the implementation

Success response:

- Status: `200 OK`
- Body: success envelope with `registrationRecord`

### `ListResourceVersions`

HTTP mapping:

- Method: `GET`
- URI: `/v1/resources/{resourceId}/versions`

Request body:

- no request body is required

Optional query parameters:

- `statusFilter`

Required query parameters or headers:

- `requestId`
- actor identity as defined by the implementation

Success response:

- Status: `200 OK`
- Body: success envelope with `resourceId` and `versions`

### `TransitionLifecycleState`

HTTP mapping:

- Method: `POST`
- URI: `/v1/resources/{resourceId}/versions/{versionId}/transitions`

Request body:

- `operation`
- `requestId`
- `actor`
- `expectedVersionId`
- `fromState`
- `toState`
- `rationale`
- `evidenceRefs` when provided

Success response:

- Status: `200 OK`
- Body: success envelope with `resourceId`, `versionId`, `fromState`, `toState`, and `effectiveRegistrationRecord`

### `RestoreResourceVersion`

HTTP mapping:

- Method: `POST`
- URI: `/v1/resources/{resourceId}/versions/{versionId}:restore`

In this binding, `{versionId}` is the version being restored from.

Request body:

- `operation`
- `requestId`
- `actor`
- `expectedVersionId`
- `rationale`
- `evidenceRefs`

Success response:

- Status: `201 Created`
- Body: success envelope with `resourceId`, newly created `versionId`, `registrationRecord`, and `lineageNode`

### `GetLineage`

HTTP mapping:

- Method: `GET`
- URI: `/v1/resources/{resourceId}/lineage`

Optional query parameters:

- `versionId`

Required query parameters or headers:

- `requestId`
- actor identity as defined by the implementation

Success response:

- Status: `200 OK`
- Body: success envelope with `resourceId` and `lineage`

### `GetAuditRecord`

HTTP mapping:

- Method: `GET`
- URI: `/v1/audit/{auditEventId}`

Required query parameters or headers:

- `requestId`
- actor identity as defined by the implementation

Success response:

- Status: `200 OK`
- Body: success envelope with `auditRecord`

## HTTP Error Binding

The protocol error categories map to HTTP status codes as follows:

| Protocol error category | HTTP status |
|-------------------------|-------------|
| `validation_error` | `400 Bad Request` |
| `access_denied` | `403 Forbidden` |
| `not_found` | `404 Not Found` |
| `conflict` | `409 Conflict` |
| `policy_denied` | `422 Unprocessable Entity` |
| `unsupported_operation` | `501 Not Implemented` |
| `internal_error` | `500 Internal Server Error` |

This mapping is normative for the baseline binding.

An implementation may include more specific transport diagnostics in `error.details`, but it must preserve the protocol error category.

## HTTP Query and Header Rules

For `GET` operations, actor identity and request correlation may be conveyed through headers or query parameters because a request body is not required by this binding.

Implementations should prefer headers for:

- actor identity
- request correlation

If an implementation chooses query parameters for these values, it must document that choice and preserve the same logical fields defined by the transport-neutral contract.

## Versioning and Compatibility

An HTTP implementation that claims baseline binding support must:

- implement the URI patterns and methods defined in this document
- preserve the JSON envelope shape
- preserve the HTTP status mapping for baseline error categories

An implementation may add new endpoints for extensions, but it must not redefine the baseline endpoint meanings in this document.
