# RSPL Core Resource Model

## Status

This document defines the initial RSPL core resource model.

It is normative for:

- the starting resource classes
- the shared resource tuple
- field-boundary categories used by later registration, lifecycle, and lineage specifications

## Scope

This model defines what a managed resource is at the protocol layer.

It does not yet define:

- full registration-record lifecycle semantics
- version-history graph rules
- rollback behavior
- operator workflows for evaluation or self-evolution

Those belong to later increments.

## Design Constraints

The resource model follows these constraints:

1. resource kinds must be extensible
2. the starting classes are a protocol baseline, not a permanently closed universe
3. identity fields must be clearly separable from mutable fields
4. metadata must not silently redefine semantics carried by core protocol fields
5. provisional extensions must be isolated from mandatory core meaning

## Starting Resource Classes

The protocol starts with the following resource classes:

- `prompt`
- `agent`
- `tool`
- `environment`
- `memory`

These classes are the initial RSPL baseline because they cover the paper’s motivating substrate and provide enough structure for registration, inspection, and later lineage work.

These classes are not exhaustive. Additional resource classes may be introduced through explicit extension points rather than by changing the meaning of the baseline classes.

## Shared Resource Entity Tuple

Every managed resource must conform to the following conceptual entity tuple:

`ResourceEntity = (resourceKind, resourceId, versionId, implementationRef, interfaceRef, config, state, metadata, extensions)`

The tuple is conceptual, not positional wire syntax. Later schemas may represent the same structure as objects, records, or typed documents.

## Tuple Field Semantics

### `resourceKind`

The protocol category of the resource.

It must be one of the baseline classes or an explicitly declared extension kind.

### `resourceId`

The stable identifier for the logical resource across versions.

It identifies the continuing resource, not a single revision of that resource.

### `versionId`

The identifier for a specific resource version.

Each materially distinct revision of a managed resource must have its own `versionId`.

### `implementationRef`

A protocol-visible reference to the executable, interpretable, or otherwise realizable form of the resource.

Examples may later include source text, artifact digest, import path, endpoint, or packaged asset reference.

### `interfaceRef`

A protocol-visible description of the resource’s exported interface.

It identifies how the resource may be inspected, invoked, configured, or otherwise interacted with through protocol-visible means.

### `config`

Configuration values that parameterize how the resource is instantiated or operated without changing its logical identity.

### `state`

The changeable resource state that may be evolved, reviewed, or versioned under later protocol rules.

### `metadata`

Descriptive or administrative information about the resource that does not alter the meaning of core protocol fields.

### `extensions`

Structured extension data that carries provisional or adopter-specific additions without changing the semantics of the mandatory core tuple.

## Field Boundary Categories

Each field in the shared tuple belongs to one of the following categories.

### Identity Fields

Identity fields define what resource is being referred to and which version is in view.

Identity fields:

- `resourceKind`
- `resourceId`
- `versionId`

Identity fields are mandatory core protocol fields.

### Configuration Fields

Configuration fields describe how a resource is configured or parameterized in use.

Configuration fields:

- `config`

Configuration fields are mandatory at the category level, though individual configuration subfields may later be optional by resource kind.

### Metadata Fields

Metadata fields carry descriptive, administrative, or auxiliary context.

Metadata fields:

- `metadata`

Metadata must not be used to smuggle core identity, lifecycle, or version semantics that belong in mandatory protocol fields.

### Evolvable State Fields

Evolvable state fields represent the portion of the resource that may change across versions or be proposed for controlled mutation.

Evolvable state fields:

- `implementationRef`
- `interfaceRef`
- `state`

The precise mutability rules for each of these fields are deferred to later lifecycle and lineage specifications. This document only establishes that they belong to the evolvable surface rather than the stable identity surface.

## Mandatory Core Fields

The following fields are mandatory in every RSPL resource:

- `resourceKind`
- `resourceId`
- `versionId`
- `implementationRef`
- `interfaceRef`
- `config`
- `state`
- `metadata`

Mandatory means these fields must exist in the conceptual model for every managed resource, even if later schemas allow an empty object, null-like encoding, or resource-kind-specific minimal values for some fields.

## Provisional Extensions

`extensions` is the only top-level provisional field in the shared tuple.

Rules for `extensions`:

1. extensions must not redefine the semantics of mandatory core fields
2. extensions must not be required for baseline interoperability
3. extensions may add adopter-specific or future protocol data so long as the core tuple remains valid without them
4. if an extension becomes necessary for baseline interoperability, it must be promoted into the core through explicit specification change

## Resource-Class Notes

The shared tuple applies to all baseline classes, but each class emphasizes different parts of the tuple.

### `prompt`

Usually emphasizes `implementationRef`, `state`, and prompt-specific `config`.

### `agent`

Usually emphasizes `interfaceRef`, orchestration-related `config`, and versioned agent state.

### `tool`

Usually emphasizes `interfaceRef`, invocation-related configuration, and implementation binding.

### `environment`

Usually emphasizes runtime or contextual dependencies represented through configuration and implementation references.

### `memory`

Usually emphasizes durable or queryable state and the interfaces by which that state is accessed or mutated.

These notes are explanatory only. Later schemas may define stricter per-kind requirements.

## Conformance Implications

An RSPL resource model implementation conforms to this document if:

1. it represents each managed resource using the shared tuple semantics defined here
2. it preserves the distinction between identity, configuration, metadata, and evolvable state
3. it treats the baseline resource classes as the starting interoperable set
4. it isolates adopter-specific additions inside explicit extension mechanisms rather than redefining mandatory fields
