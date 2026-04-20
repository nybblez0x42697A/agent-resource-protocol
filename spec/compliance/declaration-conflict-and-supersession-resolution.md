# Declaration Conflict and Supersession Resolution

## Status

This document defines how consumers resolve conflicting readiness declarations and detect invalid supersession chains when interoperable declaration metadata is incomplete, inconsistent, or ambiguous.

It builds on:

- `spec/compliance/profile-declaration-and-discovery-interoperability.md`
- `spec/compliance/profile-evolution-and-progressive-adoption.md`
- `spec/discovery/capability-discovery-and-negotiation.md`
- `spec/deprecation/deprecation-and-sunset-policy.md`

## Scope

This document is normative for:

- duplicate declaration conflict handling
- supersession-chain validity checks
- fallback ordering guidance for ambiguous declarations

It is not normative for:

- one global conflict-resolution service
- automatic repair of malformed declaration graphs
- historical reconstruction beyond the declaration set available to the consumer

## Purpose

Interoperable declaration metadata is enough for common readiness exchange, but consumers also need bounded behavior when the declaration set is inconsistent.

This document defines when a consumer should treat the declaration set as conflicting, when it should treat the supersession graph as invalid, and what limited ordering hints it may use before giving up on selecting a single current declaration.

These rules prioritize honest ambiguity over hidden inference.

## Resolution Workflow

A consumer evaluating one declaration identity scope should apply this workflow:

1. collect declarations within the same `stewardId` and `profileId`
2. reject cross-steward ordering or merge attempts unless a higher-level mapping explicitly permits them
3. validate supersession references and detect cycles
4. determine whether valid supersession links choose a unique current declaration
5. if not, apply allowed revision ordering only when the steward's revision scheme makes comparison meaningful
6. if still not unique, apply an optional schema-defined timestamp hint when available
7. if no unique current declaration emerges, classify the set as `conflicted` or `unresolved` according to the rules below

This workflow is normative at the level of decision order, not implementation language or data structure.

## Identity Scope For Resolution

Conflict and supersession resolution are evaluated within the declaration identity scope:

- `stewardId`
- `profileId`

Consumers should not attempt to merge or order declarations across different stewards unless an explicit higher-level mapping says they are equivalent.

## Duplicate-Current Conflict

A duplicate-current conflict exists when the same steward publishes multiple declarations that all appear current for the same identity scope and a consumer cannot select exactly one of them using the allowed ordering rules in this document.

Examples include:

- multiple `supported` declarations for the same `stewardId`, `profileId`, and incompatible revisions
- multiple active declarations that do not supersede each other
- multiple declarations that all claim to replace the same predecessor while remaining simultaneously current

When a duplicate-current conflict exists, the consumer should report the declaration set as conflicted rather than silently selecting one declaration.

## Supersession Reference Validity

A declaration's `supersedes` reference is valid only if the referenced predecessor can be identified unambiguously within the same identity scope.

If the predecessor is missing, duplicated, or outside the declared steward-qualified identity scope, the `supersedes` reference should be treated as unresolved.

An unresolved `supersedes` reference does not become valid through fuzzy matching.

## Circular Supersession

A supersession graph is invalid if any declaration participates in a cycle such as:

- A supersedes B
- B supersedes A

or any longer chain that loops back to an earlier declaration.

If a cycle exists, consumers should treat every declaration participating in that cycle as unresolved for current-selection purposes.

## Broken Replacement Chains

A replacement chain is broken if:

- a declaration marked `replaced` does not identify a valid replacement target
- a declaration claims to supersede a predecessor that cannot be found
- the chain forks into multiple simultaneously current successors without an explicit higher-level rule for choosing among them

When a replacement chain is broken, discovery systems and catalogs should preserve the declarations for inspection but should not present the chain as a clean, ordered lineage.

## Current-Selection Goal

If the declaration set is valid enough to choose a single current declaration for an identity scope, a consumer should do so.

If it is not valid enough, the consumer should surface one of:

- `conflicted`
- `unresolved`

along with enough bounded diagnostic context to explain why no unique current declaration was selected.

## Mixed Validity Sets

Some declaration sets may contain both:

- declarations that are internally valid
- declarations that are malformed, cyclic, or otherwise unresolved

If one uniquely current declaration can still be chosen using only valid ordering inputs, the consumer may surface that declaration as current while also surfacing bounded diagnostics about the invalid remainder of the set.

If invalid declarations prevent unique current-selection, the consumer should surface `conflicted` or `unresolved` rather than silently dropping the problematic declarations.

## Allowed Ordering Inputs

Before declaring conflict or unresolved status, a consumer may use only these ordering inputs:

- valid supersession links
- revision comparison within the same steward and profile identity
- an optional declaration timestamp if the enclosing profile schema explicitly defines that timestamp as an ordering hint

Consumers should not use ad hoc heuristics such as lexical title ordering, local file name ordering, or arbitrary ingestion order as interoperable current-selection rules.

## Revision Ordering Fallback

If valid supersession links do not determine the current declaration, a consumer may compare revisions only if the steward's declared revision scheme makes that comparison meaningful.

If revision comparison is not meaningful or cannot produce a unique winner, the consumer should not invent an ordering.

## Optional Timestamp Hint

An enclosing profile schema may define an optional timestamp field as a tiebreaking hint when:

- declarations share the same identity scope
- revision comparison alone is insufficient
- no valid supersession path chooses a unique current declaration

If such a timestamp hint is not explicitly defined by the enclosing schema, consumers should not treat arbitrary timestamps as interoperable ordering inputs.

## Conflict Resolution Outcome

If the allowed ordering inputs still leave multiple plausible current declarations, the consumer should:

- classify the declaration set as `conflicted`
- avoid advertising any of the candidates as uniquely current
- preserve the conflicting declarations for operator review or later repair

The minimum bounded diagnostic context for a `conflicted` outcome should include:

- the affected `stewardId`
- the affected `profileId`
- the candidate declarations that remained simultaneously current
- the reason unique selection failed

## Unresolved Outcome

If the declaration set cannot be evaluated because required predecessors or ordering hints are missing, the consumer should:

- classify the declaration set as `unresolved`
- avoid promoting any declaration as the unique current declaration
- expose bounded diagnostics describing the missing or invalid references

The minimum bounded diagnostic context for an `unresolved` outcome should include:

- the affected `stewardId`
- the affected `profileId`
- the invalid or missing reference that prevented resolution
- the declaration or declarations directly affected

## Discovery Presentation Guidance

If discovery surfaces declaration-resolution outcomes, they should distinguish:

- `supported`, `adopting`, `planned`, `deprecated`, and `replaced` as declaration support states
- `conflicted` and `unresolved` as resolution outcomes about the declaration set

Discovery should not blur a resolution failure into a readiness support claim.

## Example Role

Examples under `examples/` are non-normative illustrations of:

- duplicate-current declaration conflicts
- invalid supersession chains

They do not define a mandatory graph database or repair workflow.
