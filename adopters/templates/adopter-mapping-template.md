# Adopter Mapping Template

This template is non-normative.

Its purpose is to help an adopting team describe how an existing system maps to `AGRP v1` without treating local implementation structure as part of the protocol standard.

## How To Use This Template

- keep normative protocol requirements in the left column or section
- describe only local equivalents, gaps, and deviations on the adopter side
- do not rewrite the protocol requirement in adopter-specific terms
- do not present local architecture as if it were required by `AGRP`
- mark unresolved items explicitly rather than smoothing them over

## 1. Adopter Context

- Adopter name:
- System or platform name:
- Mapping author:
- Date:
- AGRP release target:
- Binding target:
- Claimed conformance target:

## 2. Scope Of This Mapping

- In scope:
- Out of scope:
- Assumptions:
- Known constraints:

## 3. Resource Identity Mapping

| AGRP concept | Normative expectation | Local equivalent | Status | Notes |
| --- | --- | --- | --- | --- |
| `resourceId` | Stable logical identifier for a managed resource |  | `mapped` / `partial` / `gap` |  |
| `versionId` | Stable version identifier within a logical resource |  | `mapped` / `partial` / `gap` |  |
| `resourceKind` | One of the baseline resource kinds or explicit rejection of unsupported kinds |  | `mapped` / `partial` / `gap` |  |
| `implementationRef` | Pointer to the executable or concrete implementation artifact |  | `mapped` / `partial` / `gap` |  |
| `interfaceRef` | Pointer to the public contract or interface identity |  | `mapped` / `partial` / `gap` |  |

## 4. Registration And Lineage Mapping

| AGRP concept | Normative expectation | Local equivalent | Status | Notes |
| --- | --- | --- | --- | --- |
| Registration record | Versioned record describing the managed resource |  | `mapped` / `partial` / `gap` |  |
| Append-only lineage | Historical lineage is preserved, not overwritten |  | `mapped` / `partial` / `gap` |  |
| Audit record | Mutation events retain actor, rationale, and timing |  | `mapped` / `partial` / `gap` |  |
| Restore semantics | Restore creates a new version rather than in-place overwrite |  | `mapped` / `partial` / `gap` |  |

## 5. Lifecycle Mapping

| AGRP concept | Normative expectation | Local equivalent | Status | Notes |
| --- | --- | --- | --- | --- |
| Lifecycle states | Baseline states are preserved or unsupported states are rejected explicitly |  | `mapped` / `partial` / `gap` |  |
| Transition rules | Only allowed transitions succeed |  | `mapped` / `partial` / `gap` |  |
| Conflict handling | Stale or conflicting transitions fail clearly |  | `mapped` / `partial` / `gap` |  |

## 6. Control-Plane Mapping

| AGRP operation | Normative expectation | Local equivalent | Status | Notes |
| --- | --- | --- | --- | --- |
| `RegisterResourceVersion` | New version registration |  | `mapped` / `partial` / `gap` |  |
| `GetRegistrationRecord` | Read a specific registration record |  | `mapped` / `partial` / `gap` |  |
| `ListResourceVersions` | Enumerate versions for a resource |  | `mapped` / `partial` / `gap` |  |
| `TransitionLifecycleState` | Perform a valid lifecycle transition |  | `mapped` / `partial` / `gap` |  |
| `RestoreResourceVersion` | Create a restored version |  | `mapped` / `partial` / `gap` |  |
| `GetLineage` | Read lineage history |  | `mapped` / `partial` / `gap` |  |
| `GetAuditRecord` | Read audit history |  | `mapped` / `partial` / `gap` |  |

## 7. Diagnostics And Failure Mapping

| AGRP concept | Normative expectation | Local equivalent | Status | Notes |
| --- | --- | --- | --- | --- |
| Validation failures | Invalid payloads or malformed requests fail clearly |  | `mapped` / `partial` / `gap` |  |
| Conflict or lifecycle failures | Stale or invalid lifecycle actions surface bounded diagnostics |  | `mapped` / `partial` / `gap` |  |
| Policy and access failures | Policy and authorization denials stay distinct |  | `mapped` / `partial` / `gap` |  |
| Retry guidance | Failures indicate whether retry is meaningful |  | `mapped` / `partial` / `gap` |  |

## 8. Discovery, Profiles, And Extensions

| AGRP concept | Normative expectation | Local equivalent | Status | Notes |
| --- | --- | --- | --- | --- |
| Capability advertisement | Advertised support is truthful |  | `mapped` / `partial` / `gap` |  |
| Readiness profiles | Additional readiness claims stay layered above baseline conformance |  | `mapped` / `partial` / `gap` |  |
| Extensions | Local extensions do not redefine baseline semantics |  | `mapped` / `partial` / `gap` |  |

## 9. Explicit Deviations

List any intentional deviations from `AGRP v1` here.

For each deviation include:

- affected protocol area
- reason for deviation
- whether it is temporary or permanent
- whether a local extension or profile is being used instead

## 10. Open Gaps

List unresolved adoption gaps here.

For each gap include:

- blocking severity
- likely remediation path
- whether the gap should be handled locally, by an extension, or by a future protocol increment

## 11. Adoption Verdict

- Baseline conformance outlook:
- Binding outlook:
- Profile or extension outlook:
- Recommended next step:
