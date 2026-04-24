# Profile Declaration and Discovery Interoperability

## Status

This document defines a minimum interoperable declaration model for readiness profiles and standardized discovery signaling for readiness support states.

It builds on:

- `spec/compliance/compliance-and-readiness-profiles.md`
- `spec/compliance/profile-evolution-and-progressive-adoption.md`
- `spec/discovery/capability-discovery-and-negotiation.md`
- `spec/governance/artifact-governance-and-registry-policy.md`
- `spec/deprecation/deprecation-and-sunset-policy.md`

## Scope

This document is normative for:

- minimum interoperable readiness profile declaration metadata
- standard readiness support-state values for discovery and catalogs
- steward disambiguation and profile replacement signaling

It is not normative for:

- one mandatory registry backend
- one mandatory discovery endpoint shape
- centralized approval of profile identifiers

## Purpose

Earlier readiness documents define what readiness profiles are and how they evolve.

This document defines the minimum information that must be preserved if readiness profile declarations are to remain interoperable across different stewards, catalogs, and discovery mechanisms.

It also defines a bounded set of support-state values so consumers can distinguish full profile support from progressive adoption or future plans.

## Minimum Declaration Metadata

An interoperable readiness profile declaration should include at least:

- `profileId`
- `stewardId`
- `revision`
- `supportState`
- `status`

If the declaration replaces or updates another declaration, it should also include:

- `supersedes`
- `compatibilityClass`

If the declaration is a progressive-adoption declaration rather than a full profile declaration, it should also include:

- `targetProfileId`
- `targetRevision`

If `targetProfileId` references a profile stewarded elsewhere, the declaration should preserve that external steward identity rather than rewriting the target as locally originated.

## Field Meaning

The minimum fields have these meanings:

- `profileId`: the stable readiness profile identifier
- `stewardId`: the organization, namespace steward, or other accountable publisher of the declaration
- `revision`: a monotonic revision token for the declared profile meaning
- `supportState`: the currently advertised readiness support state (distinct from `status`; `supportState` describes how the profile is positioned — `supported`, `planned`, `deprecated`, `replaced`, or `adopting` — while `status` describes the standing of the declaration artifact itself)
- `status`: lifecycle standing of the declaration itself — `active`, `deprecated`, or `replaced`. A declaration whose `status` is `replaced` must name its successor through `supersedes`.
- `supersedes`: the immediately prior declaration or profile revision being replaced; required when `status` is `replaced` and otherwise optional
- `compatibilityClass`: whether the replacement is compatible or incompatible for claim purposes
- `baseConformance`: the baseline conformance anchor beneath this readiness layer — the named conformance baseline (for example, `baseline`) that the profile builds on. `baseConformance` is not a synonym for profile support; a declaration may name a baseline it builds on without itself offering `supported` status.
- `additionalRequirements`: profile-shaping requirements this declaration adds on top of its `baseConformance`. Not every declaration carries additional requirements; the field is optional and describes only what this profile layers.
- `evidenceExpectations`: profile-shaping evidence references this declaration expects claims to attach. Also optional; its absence does not imply claims need no evidence, only that this declaration does not name specific expectations.
- `forbiddenBehaviors`: profile-shaping behaviors this declaration explicitly disallows, even where the baseline permits them. Optional; a profile may be positioned purely additively without forbidding anything.
- `unsatisfiedMandatoryRequirements`: requirements named by the profile that the declaring implementation currently does not satisfy. Permitted on declarations whose `supportState` is anything other than `supported`, and forbidden on declarations whose `supportState` is `supported`, reflecting the schema structure: a `supported` declaration asserts the profile is met, so unsatisfied requirements cannot coexist with that support state. Presence without unsatisfied items carries no additional meaning.

The `unsatisfiedMandatoryRequirements` field is forbidden on declarations whose `supportState` is `supported`, permitted but not required on declarations whose `supportState` is `planned`, `deprecated`, or `replaced`, and expected on declarations whose `supportState` is `adopting` when mandatory requirements remain unsatisfied. Its presence alone does not invalidate a declaration; a `supported` declaration that includes it is invalid because the support state and the existence of unsatisfied mandatory requirements contradict one another.

These fields may be expressed in any wire representation so long as their semantics remain clear.

## Steward Identifier Guidance

`stewardId` should be stable, globally distinguishable within the intended ecosystem, and bound to an accountable publisher.

Examples include:

- a protocol-defined steward identifier
- a delegated namespace identifier
- an organization-qualified identifier such as `org.example`

A steward should not publish declarations under multiple ambiguous identifiers if that would make cross-catalog reconciliation unreliable.

## Revision Token Guidance

This document does not require one universal revision syntax, but a steward should use a revision format that is:

- monotonic within that steward's declaration stream for the same conceptual profile
- stable enough for catalog comparison
- unambiguous in textual form

Examples include incrementing integers or semantic-version-like strings.

A steward should not mix unrelated revision schemes for the same profile if doing so makes ordering unclear.

## Standard Support-State Values

Discovery systems and catalogs should use a bounded set of support-state values:

- `supported`
- `adopting`
- `planned`
- `deprecated`
- `replaced`

These values are intentionally narrow to keep discovery interpretation stable across different implementations.

## Support-State Meaning

The standard support-state values mean:

- `supported`: the implementation currently satisfies the referenced readiness profile and may honestly claim it
- `adopting`: the implementation is progressing toward the referenced profile but may not yet claim full support
- `planned`: the implementation intends to target the profile later but has not yet reached progressive adoption worth advertising as current work
- `deprecated`: the implementation or steward is signaling that this profile declaration should be retired in favor of a newer declaration or profile
- `replaced`: the declaration is no longer current because a successor declaration or profile now stands in its place

An implementation must not use `supported` unless all mandatory requirements for the referenced profile are satisfied.

## Relationship To Progressive Adoption

`adopting` is the interoperable discovery value for progressive adoption.

When a declaration uses `adopting`, it should make clear:

- which target profile is being adopted
- which revision is being targeted
- whether mandatory requirements remain unsatisfied

Discovery mechanisms may summarize this state, but they should not blur it into `supported`.

If `supportState` is `adopting`, interoperable exchange should include both:

- `targetProfileId`
- `targetRevision`

## Declaration Status

`supportState` describes the current support posture being advertised.

`status` describes the lifecycle standing of the declaration artifact itself.

For example, a declaration artifact may be `deprecated` in lifecycle status while still documenting that an earlier implementation state had once been `supported`.

Implementations should keep these concerns distinct.

## Compatibility-Class Values

If `compatibilityClass` is present, the interoperable values should be:

- `compatible`
- `incompatible`

An implementation should not invent local synonyms for these values in interoperable exchange unless an enclosing profile schema maps them back to these meanings without ambiguity.

## Steward Disambiguation

If multiple stewards publish similar or colliding profile names, consumers should distinguish them by the pair:

- `stewardId`
- `profileId`

A consumer should not assume that identical or nearly identical local profile names from different stewards refer to the same readiness meaning.

If a steward adopts another steward's profile by reference, the declaration should preserve the original `stewardId` rather than silently relabeling the profile as locally originated.

## Conflict Handling Guidance

If similar identifiers create ambiguity across stewards:

- the steward should publish a namespaced `profileId`
- catalogs should retain `stewardId` alongside `profileId`
- discovery consumers should prefer exact steward-qualified matches over fuzzy label matching

A catalog or implementation should not merge different steward declarations into one logical profile unless an explicit normative mapping says they are equivalent.

If the same steward publishes multiple simultaneously active declarations for the same `profileId` and revision, discovery systems and catalogs should treat that as a conflict rather than as independent valid declarations.

## Replacement Workflow Guidance

When a readiness profile declaration is replaced, the replacement should:

- identify the older declaration through `supersedes`
- identify whether the replacement is compatible or incompatible
- preserve the original `profileId` only if the meaning remains claim-compatible
- move the older declaration to `deprecated` or `replaced` status as appropriate

If the replacement is incompatible for claim purposes, the steward should prefer a new `profileId` or an explicit successor declaration that makes the incompatibility visible.

## Discovery Presentation Guidance

If readiness profile declarations appear in discovery output, the discovery surface should make visible:

- the steward-qualified profile identity
- the advertised `supportState`
- the currently relevant revision

If a declaration is `adopting` or `planned`, discovery should avoid presenting it as equivalent to a fully supported readiness claim.

## Minimal Validation Guidance

A readiness declaration should be considered invalid for interoperable exchange if it:

- omits `profileId`
- omits `stewardId`
- omits `revision`
- omits `supportState`
- omits `status`
- uses `supported` while simultaneously declaring unsatisfied mandatory requirements
- uses `adopting` without both `targetProfileId` and `targetRevision`
- uses `compatibilityClass` with a value other than `compatible` or `incompatible`
- uses an empty or ambiguous `stewardId` that cannot reliably distinguish the publisher from other stewards in the same ecosystem
- publishes multiple active declarations for the same `stewardId`, `profileId`, and `revision` without an explicit differentiator defined by a higher-level profile schema
- marks a declaration as replaced without naming or otherwise identifying the replacement target

This document does not define a universal validation engine, but these rules provide a minimum interoperability floor.

## Example Role

Examples under `examples/` are non-normative illustrations of:

- an interoperable readiness profile declaration
- a discovery advertisement that distinguishes support states

They do not define a mandatory registry schema or endpoint protocol.
