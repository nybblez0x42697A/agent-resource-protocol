# Versioning and Evolution Policy

## Status

This document defines the baseline versioning and evolution policy for protocol artifacts.

It builds on:

- `spec/charter/repository-charter.md`
- `spec/conformance/baseline-conformance.md`
- `spec/extensions/extension-and-profile-model.md`
- `spec/discovery/capability-discovery-and-negotiation.md`

## Scope

This document is normative for:

- versioning rules for protocol artifacts
- compatibility classes for protocol evolution
- baseline rules for additive, tightening, and breaking changes

It is not normative for:

- release process automation
- repository branching strategy
- external package manager version syntax

## Versioning Principle

Protocol artifacts must evolve in a way that makes compatibility impact explicit.

The baseline versioning model uses:

- `major.minor.patch`

This document defines how that model applies across normative specifications, bindings, profiles, extensions, and capability identifiers.

## Artifact Classes

The baseline artifact classes are:

- normative specifications
- transport bindings
- profiles
- extensions
- capability identifiers

Each class may publish its own version, but compatibility claims must remain understandable relative to baseline conformance.

## Normative Specification Versioning

Normative documents should use `major.minor.patch` semantics:

- `major`: breaking semantic change
- `minor`: additive or compatibility-preserving change
- `patch`: clarification or non-semantic correction

A breaking semantic change includes any change that would require a baseline-conformant implementation to change behavior in order to remain conformant.

## Binding Versioning

Bindings should use their own version identifiers.

A binding major version must change when:

- required endpoints or methods change incompatibly
- required envelope fields change incompatibly
- required error mappings change incompatibly

A binding minor version may change when:

- optional fields are added
- optional headers or query parameters are documented
- clarification or additive guidance is introduced without changing baseline semantics

## Profile Versioning

Profiles should version independently from the baseline protocol.

A profile major version must change when:

- the profile's required behavior changes incompatibly
- the set of mandatory requirements changes in a way that invalidates prior profile-conformant implementations

A profile minor version may change when:

- additional optional guidance is introduced
- additive compatible constraints are introduced that do not invalidate prior profile-conformant implementations

## Extension Versioning

Extensions should version independently.

An extension major version must change when:

- the extension changes meaning incompatibly
- the extension changes required fields incompatibly
- the extension's fallback behavior changes incompatibly

An extension minor version may change when:

- optional compatible fields are added
- additive capabilities are introduced without changing prior meaning

## Capability Identifier Versioning

Capability identifiers should be stable and explicit enough to distinguish incompatible generations.

If a capability changes incompatibly, the identifier should also change in a visible way, for example by:

- embedding an explicit major version suffix
- publishing a distinct identifier for the incompatible generation

An implementation must not reuse the same capability identifier for incompatible meanings.

## Compatibility Classes

The baseline compatibility classes are:

- `clarification`
- `additive`
- `tightening`
- `breaking`

### `clarification`

A clarification changes wording, examples, or structure without changing required behavior.

Clarifications are patch-compatible.

### `additive`

An additive change introduces optional or compatibility-preserving capability.

Examples:

- new optional field in an extension location
- new optional binding guidance
- new optional extension or profile

Additive changes are minor-compatible.

### `tightening`

A tightening change narrows valid behavior or strengthens requirements.

Tightening may be:

- minor-compatible if all previously conformant implementations already satisfy the stronger rule in practice
- breaking if previously conformant behavior would become invalid

A tightening change must be classified conservatively. If compatibility is uncertain, it should be treated as breaking.

### `breaking`

A breaking change alters required behavior, meaning, or compatibility expectations in a way that invalidates previously conformant implementations or negotiated behavior.

Breaking changes require a major version increment.

## Evolution Rules

The baseline evolution rules are:

1. preserve baseline semantics unless intentionally publishing a major-version break
2. classify changes explicitly before release
3. use new identifiers for incompatible capabilities
4. document fallback behavior when additive change introduces optional capability
5. avoid silent semantic drift under stable identifiers

## Compatibility Expectations

An implementation may interoperate across artifact versions only when the selected versions are compatible under the rules in this document.

If compatibility cannot be determined confidently, implementations should treat the interaction as incompatible rather than guessing.

## Upgrade Guidance

When publishing a new artifact version, authors should document:

- prior version
- compatibility class
- expected upgrade impact
- required migration actions when breaking

For additive changes, authors should document how older implementations can ignore or reject the new capability safely.

For breaking changes, authors should document:

- new identifier or major version
- migration boundary
- deprecated prior behavior

## Relationship To Discovery

Capability discovery should advertise versions or stable identifiers clearly enough to support compatibility decisions.

Negotiation must not treat two versions as compatible unless that compatibility is justified by the published evolution rules.

## Relationship To Conformance

Baseline conformance is anchored to the applicable normative artifact versions.

An implementation claiming conformance should be able to state which versions of:

- the baseline specification set
- bindings
- profiles
- extensions

it supports.

## Example Role

Examples under `examples/` are non-normative illustrations of:

- a compatible additive evolution
- a breaking major-version evolution

They do not define mandatory publication formats.
