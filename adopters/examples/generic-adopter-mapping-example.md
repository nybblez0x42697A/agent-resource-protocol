# Generic Adopter Mapping Example

This example is non-normative.

It demonstrates how an adopter might fill out the mapping template using neutral placeholders instead of a real product.

## 1. Adopter Context

- Adopter name: Example Platform Team
- System or platform name: Example Managed Resource Registry
- Mapping author: Example Protocol Working Group
- Date: 2026-04-20
- AGRP release target: `AGRP v1.0.0`
- Binding target: `binding.http-json.v1`
- Claimed conformance target: baseline

## 2. Scope Of This Mapping

- In scope: managed tool and prompt resources, version registration, lifecycle transitions, lineage queries
- Out of scope: deployment automation, non-HTTP transports, future `SEPL`
- Assumptions: the local registry already maintains immutable version snapshots
- Known constraints: the local platform currently lacks a first-class readiness profile publication surface

## 3. Resource Identity Mapping

| AGRP concept | Normative expectation | Local equivalent | Status | Notes |
| --- | --- | --- | --- | --- |
| `resourceId` | Stable logical identifier for a managed resource | `resource.slug` | mapped | Existing slug is already stable across versions |
| `versionId` | Stable version identifier within a logical resource | `release.version` | mapped | Existing release version is immutable once published |
| `resourceKind` | One of the baseline resource kinds or explicit rejection of unsupported kinds | `type` | partial | Only `tool` and `prompt` are currently supported |
| `implementationRef` | Pointer to the executable or concrete implementation artifact | `artifact_uri` | mapped | Stored as an OCI or git artifact reference |
| `interfaceRef` | Pointer to the public contract or interface identity | `contract_ref` | mapped | Existing contract registry identifier |

## 4. Registration And Lineage Mapping

| AGRP concept | Normative expectation | Local equivalent | Status | Notes |
| --- | --- | --- | --- | --- |
| Registration record | Versioned record describing the managed resource | `resource_release_record` | mapped | Current local record already contains required identity and metadata fields |
| Append-only lineage | Historical lineage is preserved, not overwritten | `release_history` | mapped | Prior releases remain queryable |
| Audit record | Mutation events retain actor, rationale, and timing | `change_log_entry` | partial | Actor and timing exist; rationale is required only for manual review flows |
| Restore semantics | Restore creates a new version rather than in-place overwrite | `rollback_clone` | partial | Current implementation clones a prior release, but naming is inconsistent |

## 5. Lifecycle Mapping

| AGRP concept | Normative expectation | Local equivalent | Status | Notes |
| --- | --- | --- | --- | --- |
| Lifecycle states | Baseline states are preserved or unsupported states are rejected explicitly | `draft`, `active`, `archived` | partial | `deprecated`, `restored`, and `superseded` need explicit surfaced states |
| Transition rules | Only allowed transitions succeed | workflow guard rules | mapped | Local review checks already enforce draft-to-active gating |
| Conflict handling | Stale or conflicting transitions fail clearly | optimistic version check | mapped | Conflict response needs AGRP-aligned error category wording |

## 6. Control-Plane Mapping

| AGRP operation | Normative expectation | Local equivalent | Status | Notes |
| --- | --- | --- | --- | --- |
| `RegisterResourceVersion` | New version registration | `POST /releases` | mapped | Existing request shape needs minor envelope normalization |
| `GetRegistrationRecord` | Read a specific registration record | `GET /releases/{version}` | mapped |  |
| `ListResourceVersions` | Enumerate versions for a resource | `GET /resources/{id}/releases` | mapped |  |
| `TransitionLifecycleState` | Perform a valid lifecycle transition | `POST /releases/{version}/state` | partial | Existing payload lacks explicit `fromState` |
| `RestoreResourceVersion` | Create a restored version | `POST /releases/{version}/restore` | partial | Response should expose restored lineage link explicitly |
| `GetLineage` | Read lineage history | `GET /resources/{id}/lineage` | mapped |  |
| `GetAuditRecord` | Read audit history | `GET /audit/{commitId}` | partial | Current API exposes audit only for administrators |

## 7. Diagnostics And Failure Mapping

| AGRP concept | Normative expectation | Local equivalent | Status | Notes |
| --- | --- | --- | --- | --- |
| Validation failures | Invalid payloads or malformed requests fail clearly | `400 invalid_request` | mapped |  |
| Conflict or lifecycle failures | Stale or invalid lifecycle actions surface bounded diagnostics | `409 stale_version` | partial | Retry guidance not currently surfaced |
| Policy and access failures | Policy and authorization denials stay distinct | `403 policy_denied` / `403 access_denied` | partial | Codes are separate internally but not in public API bodies |
| Retry guidance | Failures indicate whether retry is meaningful | none | gap | Needs explicit protocol-visible field |

## 8. Discovery, Profiles, And Extensions

| AGRP concept | Normative expectation | Local equivalent | Status | Notes |
| --- | --- | --- | --- | --- |
| Capability advertisement | Advertised support is truthful | `/.well-known/capabilities` | partial | Surface exists internally but is not yet published |
| Readiness profiles | Additional readiness claims stay layered above baseline conformance | internal launch checklist | gap | Not yet expressed as interoperable declarations |
| Extensions | Local extensions do not redefine baseline semantics | custom metadata hints | partial | Need clearer extension namespace discipline |

## 9. Explicit Deviations

- Diagnostics currently do not expose `retryable` explicitly in all failure responses
- Lifecycle state names are partially normalized but not yet fully aligned to all baseline AGRP states

## 10. Open Gaps

- Gap: no published readiness declaration surface
  - Severity: medium
  - Likely remediation: add capability and readiness advertisement endpoint
  - Path: local implementation plus possible future readiness-profile adoption
- Gap: restore response does not expose lineage details explicitly
  - Severity: low
  - Likely remediation: response-shape update
  - Path: local implementation

## 11. Adoption Verdict

- Baseline conformance outlook: feasible with moderate response-shape and lifecycle-surface adjustments
- Binding outlook: HTTP JSON binding is close
- Profile or extension outlook: extension namespace and readiness declarations need follow-on work
- Recommended next step: compare the local surface against the published AGRP schemas and conformance vectors, then document any remaining protocol-facing gaps
