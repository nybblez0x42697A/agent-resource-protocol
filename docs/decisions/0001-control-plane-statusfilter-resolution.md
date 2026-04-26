# 0001. Control-Plane statusFilter Resolves to registrationStatus

## Status

`Accepted`

Decided: 2026-04-23 by the AGRP maintainer during increment 0041 checkpoint C1.

## Context

Increment 0041 inherited an ambiguity in `ListResourceVersions.statusFilter`. The schema
at `models/schemas/control-plane-envelope.schema.json:124-126` referenced
`./common.schema.json#/$defs/lifecycleState`, an enum of six values:
`["draft", "active", "deprecated", "archived", "superseded", "restored"]`. The sibling
enum `registrationStatus` carried the same set minus `draft`. Prose at
`spec/control-plane/control-plane-contracts.md:132-157` described `ListResourceVersions`
as "List versions for a logical resource" with `statusFilter` as an optional request
field, but offered no guidance on which status domain the filter was supposed to operate
over. Adopters validating against the schema and adopters reading the prose would each
arrive at compatible interpretations only by accident.

The 0041 audit recorded this as Open Question OQ-01 with three candidate resolutions:
(a) split `statusFilter` into two filters along the two domains, (b) constrain the
existing field to one domain via `enum` plus rename, (c) annotation-only clarification
keeping `lifecycleState` as the typed domain.

## Decision

`statusFilter` was resolved to `registrationStatus` (the discovery-visible status,
excluding `draft`). The change shipped as a single `$ref` swap from `lifecycleState`
to `registrationStatus` plus an inline `description` annotation, with a one-sentence
prose clarification appended to `control-plane-contracts.md` immediately after the
`ListResourceVersions` optional-fields block.

The argument made at decision time, recorded in 0041 plan.md §1.3, was:

1. `ListResourceVersions` is a discovery/enumeration operation. Callers listing "the
   versions that exist" do not typically want to enumerate `draft` versions they have
   not yet transitioned to `active` — those are work-in-progress artifacts of the
   caller's own workflow, not part of the discoverable version history.
2. The `registrationStatus` enum (which lacks `draft`) exactly matches the set of states
   that describe "what a version *is* in the registry" vs. `lifecycleState` which
   describes "what state a version is *transitioning through* in its workflow".
3. The only sibling operation that accepts lifecycle states is
   `TransitionLifecycleState`, where `fromState`/`toState` must include `draft` because
   transitions from draft are the primary creation path. That operation takes the
   lifecycle domain legitimately; `ListResourceVersions` should not.
4. The chosen action — a `$ref` swap plus a `description` annotation — is the minimum
   change that makes the schema unambiguous to a reader.

Alternatives, as enumerated in 0041 spec.md OQ-01:

- **Option (a) — Split `statusFilter` into two filters** (`registrationStatusFilter` +
  `lifecycleStateFilter`): rejected because point (4) above showed a single
  unambiguously-typed field was sufficient; splitting added schema and binding surface
  for an ambiguity that points (1)–(3) resolved at the semantic layer.
- **Option (b) — Constrain to one domain via enum plus rename** (e.g., rename
  `statusFilter` to `registrationStatusFilter`): the rename portion was not adopted
  because it would have churned every binding and adopter that already referenced
  `statusFilter` by name.
- **Option (c) — Annotation-only clarification** (keep `lifecycleState`, add prose
  only): rejected because the ambiguity was operational, not purely documentary;
  relying on reader attention would not constrain validators.

## Consequences

The schema and prose now agree. The change required two edits:

- `models/schemas/control-plane-envelope.schema.json:124-127` — `$ref` swapped to
  `registrationStatus`; an inline `description` annotation makes the discovery-only
  semantics explicit at the field.
- `spec/control-plane/control-plane-contracts.md:148-149` — one-sentence prose
  clarification added directly under the `ListResourceVersions` optional-fields block.

`draft` versions are no longer discoverable through `ListResourceVersions`, which matches
the operation's discovery semantics. `TransitionLifecycleState` retains the lifecycle
domain (necessary because `fromState=draft` is the primary creation path). The minimum
change shipped — a single `$ref` swap plus one description annotation; no operation was
renamed, split, or reshaped.

A regression check during 0041 closure confirmed no pre-existing conformance vector
relied on the previous `lifecycleState`-typed filter.

Viewed retrospectively, the shipped action combined the constrain-to-one-domain intent
of option (b) without the rename churn, and the clarifying-annotation aspect of option
(c) without keeping `lifecycleState` as the typed domain. This synthesis was not part of
the recorded decision-time rationale in 0041 plan.md §1.3, but is a useful framing for
future readers comparing the shipped action against the rejected alternatives.

**Note for future readers**: 0041 plan.md §1.3 line 98 contains a small labeling error
— it refers to "renaming" as "option c" when spec.md OQ-01 line 187 (the original
formulation) labels rename as option (b) and annotation-only as option (c). This ADR
follows spec.md OQ-01's labels because they are the canonical formulation; the plan.md
slip is corrected here without rewriting the source.

## References

- Source records: `.specweave/increments/0041-agrp-spec-drift-remediation/plan.md` §1.3;
  `.specweave/increments/0041-agrp-spec-drift-remediation/spec.md` OQ-01 (line 187)
- Affected artifacts: `models/schemas/control-plane-envelope.schema.json:124-127`,
  `spec/control-plane/control-plane-contracts.md:148-149`
- Commits: `7f34a71` (0041 closure)
- Related ADRs: none yet
