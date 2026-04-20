# Baseline Conformance

## Status

This document defines the baseline conformance model for the current protocol artifacts in this repository.

It builds on the normative specifications and machine-readable schemas already published in the repository.

## Scope

This document is normative for:

- the minimum artifact set an implementation must support to claim baseline conformance
- the distinction between mandatory protocol support and optional extensions
- the role of non-normative examples in conformance evaluation

It is not normative for certification process, branding, or test harness implementation.

## Conformance Levels

The protocol currently defines one baseline level:

- `baseline`

Future profiles may define stricter or more specialized conformance levels, but this document only defines baseline interoperability.

## Baseline Artifact Set

An implementation claiming baseline conformance must support the semantics of the following repository artifacts:

- `spec/glossary/protocol-glossary.md`
- `spec/rspl/core-resource-model.md`
- `spec/rspl/registration-and-lineage-model.md`
- `spec/rspl/lifecycle-and-transition-semantics.md`
- `spec/control-plane/control-plane-contracts.md`

It must also be able to process the corresponding machine-readable schema artifacts under `models/schemas/` where applicable.

## Mandatory Support Requirements

A baseline-conformant implementation must:

1. represent managed resources according to the shared resource entity semantics
2. support the baseline resource kinds or reject unsupported kinds explicitly without redefining them
3. preserve resource and version identity rules
4. preserve append-only lineage semantics
5. implement restore as new-version creation rather than in-place overwrite
6. enforce the baseline lifecycle transition rules or return structured conflict or validation errors
7. expose control-plane operations or equivalent bindings that preserve the documented contract meaning
8. validate or emit records that conform to the published machine-readable schemas, except where an extension is explicitly declared

## Optional And Extension Support

An implementation may:

- support additional resource kinds
- support additional metadata fields
- support additional control-plane operations
- support additional lifecycle states or profiles

Only if:

1. the baseline required fields and semantics remain intact
2. the extension does not redefine the meaning of a mandatory field
3. unsupported extensions are rejected or ignored explicitly rather than interpreted silently

## Schema Conformance

For baseline conformance, the following schema artifacts are in scope:

- `models/schemas/resource-entity.schema.json`
- `models/schemas/registration-record.schema.json`
- `models/schemas/lineage-node.schema.json`
- `models/schemas/audit-record.schema.json`
- `models/schemas/lifecycle-transition.schema.json`

Schema conformance means:

1. required fields are present when records are emitted
2. optional fields are not treated as mandatory baseline requirements
3. additional fields outside published extension locations are rejected or isolated explicitly

## Operation Conformance

A baseline-conformant implementation must preserve the meaning of the following operations:

- `RegisterResourceVersion`
- `GetRegistrationRecord`
- `ListResourceVersions`
- `TransitionLifecycleState`
- `RestoreResourceVersion`
- `GetLineage`
- `GetAuditRecord`

The implementation may rename or transport-bind these operations differently, but the contract meaning, required inputs, required outputs, and error semantics must remain equivalent.

## Error Conformance

A baseline-conformant implementation must expose error behavior equivalent to the baseline error categories:

- `validation_error`
- `not_found`
- `conflict`
- `policy_denied`
- `access_denied`
- `unsupported_operation`
- `internal_error`

Equivalent transport-specific encodings are allowed so long as the category meaning is preserved.

## Example Artifacts

Example payloads under `examples/` are non-normative.

Their role is to:

- illustrate valid shapes
- clarify intended field usage
- provide sample payloads for implementer orientation

An implementation is not required to reproduce example values exactly, but example payloads should validate against the corresponding schemas unless an example explicitly states otherwise.

## Conformance Claim

An implementation may claim `baseline` conformance only if it can demonstrate:

1. semantic alignment with the baseline normative artifacts
2. compatibility with the in-scope schema set
3. preservation of required lifecycle, lineage, restore, and audit behavior
4. preservation of transport-neutral control-plane contract meaning
