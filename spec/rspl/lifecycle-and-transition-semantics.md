# RSPL Lifecycle And Transition Semantics

## Status

This document defines baseline lifecycle states, allowed transitions, restore and supersession transitions, and conflict rules for registered RSPL resources.

It builds on:

- `spec/rspl/core-resource-model.md`
- `spec/rspl/registration-and-lineage-model.md`

## Scope

This document is normative for:

- baseline lifecycle states
- allowed state transitions
- restore and supersession transition behavior
- competing-transition conflict rules

It does not define transport APIs, request formats, or implementation-specific orchestration.

## Lifecycle State Model

Every registered resource version must be in exactly one baseline lifecycle state.

Baseline lifecycle states:

- `draft`
- `active`
- `deprecated`
- `archived`
- `superseded`
- `restored`

These are registry and protocol states, not runtime execution states.

## State Meanings

### `draft`

A version exists but is not yet the active version for normal protocol use.

### `active`

The version is the current selected version for normal protocol use.

### `deprecated`

The version remains addressable but is no longer recommended for new use.

### `archived`

The version remains part of history but is no longer intended for routine active selection.

### `superseded`

The version was previously active and has been replaced by a newer active or restored version.

### `restored`

A version created by a restore transition and recorded as such before any later activation decision.

## Allowed Baseline Transitions

The following baseline transitions are allowed:

1. `draft -> active`
2. `active -> deprecated`
3. `active -> superseded`
4. `deprecated -> archived`
5. `deprecated -> active`
6. `superseded -> archived`
7. `draft -> archived`
8. `restored -> active`
9. `active -> restored` is not allowed directly; restore creates a new version whose initial state is `restored`

Transitions not listed here are invalid unless added by a later explicit extension or revision.

## Transition Rules

### Activation

Activating a version makes it the current active version for the `resourceId`.

Rules:

1. at most one version may be `active` for a given `resourceId` at a time
2. activating a new version must transition the previously active version to `superseded`, unless there was no previously active version

### Deprecation

Deprecation marks a version as still addressable but discouraged for new use.

Rules:

1. deprecation does not remove the version from lineage
2. deprecated versions may later be reactivated if policy allows and no conflict rule forbids it

### Archival

Archival removes a version from routine active selection while preserving history.

Rules:

1. archived versions must remain auditable
2. archiving must not erase lineage or audit records
3. an archived version is not eligible to become active again unless a later spec explicitly allows reactivation from archive

### Supersession

Supersession occurs when an active version is replaced by another version of the same `resourceId`.

Rules:

1. a superseded version remains part of append-only history
2. supersession does not imply deletion or invalidation of audit evidence
3. supersession must be reflected in lineage through `supersedesVersionId`

## Restore Transition Semantics

A restore is a transition that creates a new version by using an earlier version as the restore target.

Rules:

1. a restore does not transition an old version in place
2. a restore creates a new registration record with a new `versionId`
3. the new version must have lifecycle state `restored` at creation
4. the new version must record `restoredFromVersionId`
5. if the restored version becomes the selected version for normal use, it must transition from `restored` to `active`
6. when a restored version becomes `active`, the previously active version must transition to `superseded`
7. restore provenance must remain visible through `mutationType = restore` and `restoredFromVersionId`; it must not depend on the version remaining forever in lifecycle state `restored`

## Supersession Transition Semantics

Supersession is operationally coupled to activation and restore.

Rules:

1. any successful activation of a new current version must supersede the previous active version
2. any successful restore that becomes current must supersede the previous active version
3. supersession must be explicit in both lifecycle state and lineage metadata

## Competing Transition Rules

Competing transitions are two or more transition attempts that target the same `resourceId` and depend on the same prior active or prior known state.

The protocol uses optimistic conflict rules by default.

Rules:

1. a transition request must identify the expected current `versionId` or equivalent base version
2. if the actual current version differs from the expected base version, the transition must fail with a conflict rather than applying silently
3. conflicting transitions must not both succeed against the same expected base version
4. a losing transition may be retried against the new current version as a new transition attempt

## Restore Conflict Rules

Restore operations follow the same conflict discipline as updates.

Rules:

1. a restore must declare the version it intends to supersede or replace as current
2. if another transition changes the active version first, the restore must fail with conflict and be reevaluated
3. a restore must not silently displace a newer active version that was committed after the restore candidate was prepared

## Concurrency Safety Rule

For a given `resourceId`, lifecycle transitions must be linearized at commit time.

This means the protocol may permit concurrent proposals or evaluations, but the registry-visible state transition for a single resource must resolve to one committed next version at a time.

## Invalid Transition Handling

When a transition is invalid, an implementation must reject it without mutating lifecycle state, lineage state, or audit history.

An invalid transition includes:

- unrecognized state transitions
- transitions that assume a stale current version
- attempts to restore in place rather than by new version creation
- attempts to create multiple simultaneous active versions for one `resourceId`

## Conformance Implications

An implementation conforms to this document if:

1. it supports the baseline lifecycle states defined here
2. it enforces the allowed transition rules and rejects invalid transitions
3. it performs restore through new version creation rather than in-place reactivation
4. it prevents conflicting transitions from silently succeeding against the same expected base version
5. it preserves append-only lineage and audit semantics across all lifecycle transitions
