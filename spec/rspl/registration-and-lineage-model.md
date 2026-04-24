# RSPL Registration And Lineage Model

## Status

This document defines the initial RSPL registration record, version identity rules, lineage model, restore semantics, and audit minimums.

It builds directly on `spec/rspl/core-resource-model.md`.

## Scope

This document is normative for:

- the registration record shape
- resource and version identity rules
- lineage and mutation-history semantics
- rollback-safe restore behavior
- minimum audit information for commit and restore events

It does not yet define transport, APIs, or operator workflows for how these records are exchanged.

## Registration Record

Every managed resource version must be represented by a registration record.

Conceptually:

`RegistrationRecord = (resourceId, versionId, resourceKind, status, implementationRef, interfaceRef, config, stateDigest, metadata, lineageRef, auditRef, extensions)`

The registration record binds the RSPL resource to a concrete versioned registry entry.

## Registration Record Fields

### `resourceId`

Stable identifier for the logical resource across all of its versions.

Rules:

1. `resourceId` must remain stable across all versions in the same resource lineage
2. `resourceId` must not be reused for a different logical resource
3. forked or imported resources that establish a new logical identity must receive a new `resourceId`

### `versionId`

Identifier for a specific registered version of a resource.

Rules:

1. `versionId` must be unique within the scope of its `resourceId`
2. a materially distinct resource revision must receive a new `versionId`
3. restoring an earlier state must create a new `versionId`; it must not silently reactivate a prior version as if no intervening history existed

### `resourceKind`

The registered resource class as defined by the RSPL core resource model.

### `status`

The current registry status of the versioned record.

Allowed baseline values:

- `active`
- `deprecated`
- `archived`
- `superseded`
- `restored`

These values describe registry visibility and lineage position, not transport-level execution state.

### `implementationRef`

Reference to the executable, interpretable, or otherwise realizable form of the registered resource version.

### `interfaceRef`

Reference to the exported interface associated with the registered resource version.

### `config`

The effective configuration associated with the registered version.

### `stateDigest`

A stable digest or equivalent integrity reference for the evolvable state associated with the registered version.

This field exists so a registration record can identify the registered state without requiring the full state object to be copied into every lineage operation.

### `metadata`

Descriptive or administrative metadata for the registered version.

### `lineageRef`

Reference to the lineage node associated with the registered version.

### `auditRef`

Reference to the audit record associated with creation of the registered version.

### `extensions`

Provisional extension data that must not redefine mandatory registration semantics.

## Material Version Change Rule

A new `versionId` is required when any of the following change in a way that alters the behavior or meaning of the resource:

- `implementationRef`
- `interfaceRef`
- any semantically meaningful part of `config`
- any semantically meaningful part of the registered evolvable state represented by `stateDigest`

Purely descriptive metadata edits may remain within the same version only if they do not affect behavior, interface meaning, policy interpretation, or audit interpretation.

If there is uncertainty about whether a change is material, it must be treated as material and assigned a new `versionId`.

## Lineage Model

Each registered version must be part of a lineage history.

Conceptually:

`LineageNode = (resourceId, versionId, parentVersionId, mutationType, commitId, createdAt, changeSummary, restoredFromVersionId, supersedesVersionId)`

## Lineage Node Fields

### `parentVersionId`

The immediately preceding version from which the current version was derived.

For the initial version of a resource, this value is absent.

### `mutationType`

The kind of change that produced the version.

Allowed baseline values:

- `create`
- `update`
- `restore`
- `fork`
- `import`

### `commitId`

Identifier for the commit event that registered the version into lineage.

### `createdAt`

Timestamp at which the lineage event was committed.

### `changeSummary`

A protocol-visible summary of what materially changed.

### `restoredFromVersionId`

When `mutationType = restore`, identifies the earlier version whose state was used as the restore target.

### `supersedesVersionId`

Identifies the immediately superseded prior active version, if any.

## Mutation History Semantics

The lineage history for a single `resourceId` forms an append-only version history.

Rules:

1. each new version appends a new lineage node
2. lineage nodes must not be rewritten to hide prior versions
3. restore operations append history; they do not erase it
4. imports and forks may create a new root under a new `resourceId`, but must preserve provenance through audit and change summary fields

## Restore And Rollback Semantics

Rollback-safe behavior means that a restore must be explicit, reviewable, and non-destructive.

Rules:

1. a restore operation creates a new registered version
2. the new restored version must reference the earlier target through `restoredFromVersionId`
3. the intervening versions remain part of history and must stay auditable
4. a restore may supersede the currently active version, but it must not delete or overwrite it
5. partial rollback behavior, when supported later, must still create explicit new lineage entries rather than mutating history in place

## Minimum Audit Information

Every commit event that creates a registered version must have an audit record.

Conceptually:

`AuditRecord = (commitId, resourceId, versionId, action, actor, rationale, evidenceRefs, createdAt)`

### Required Audit Fields

#### `commitId`

Stable identifier for the commit or restore event.

#### `resourceId`

Logical resource affected by the event.

#### `versionId`

Version created by the event.

#### `action`

Allowed baseline values:

- `create`
- `update`
- `restore`
- `fork`
- `import`

#### `actor`

The protocol-visible actor responsible for the event. This may later be realized as a human, service, or agent identity.

#### `rationale`

Human-readable or machine-reviewable explanation of why the event occurred.

#### `evidenceRefs`

References to traces, evaluations, approvals, or other evidence supporting the event.

#### `createdAt`

Timestamp for the audit event.

## Commit And Restore Requirements

For a normal commit:

- a new registration record must be created
- a new lineage node must be appended
- a new audit record must be written

For a restore:

- a new registration record must be created with a new `versionId`
- the lineage node must use `mutationType = restore`
- the lineage node must point to `restoredFromVersionId`
- the audit record must state the rationale and evidence for the restore decision

## Conformance Implications

An implementation conforms to this document if:

1. every registered version has a registration record with the mandatory fields defined here
2. version identity is append-only and material changes create new versions
3. lineage history preserves prior versions rather than overwriting them
4. restore operations create explicit new versions and lineage entries
5. every create, update, fork, import, or restore event has the minimum audit information defined here
