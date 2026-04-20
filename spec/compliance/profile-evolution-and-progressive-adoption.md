# Profile Evolution and Progressive Adoption

## Status

This document defines the baseline model for how readiness profiles evolve and how implementations may communicate partial adoption without overstating profile support.

It builds on:

- `spec/compliance/compliance-and-readiness-profiles.md`
- `spec/versioning/versioning-and-evolution-policy.md`
- `spec/governance/artifact-governance-and-registry-policy.md`
- `spec/discovery/capability-discovery-and-negotiation.md`

## Scope

This document is normative for:

- readiness profile identifier stability
- readiness profile compatible and incompatible evolution
- partial adoption and in-progress readiness declarations

It is not normative for:

- centralized certification workflows
- audit scoring formulas
- product marketing language

## Purpose

The readiness profile model defines what a readiness profile is.

This document defines how a readiness profile stays understandable over time and how an implementation may describe progress toward a profile before full satisfaction.

These rules prevent namespace drift, silent profile repurposing, and inflated readiness claims.

## Stable Profile Identity

A readiness profile should use a stable `profileId` that remains bound to one conceptual profile over time.

A profile identifier should:

- be human-readable
- remain stable across compatible revisions
- avoid ambiguous local nicknames when used in cross-organization declarations
- follow the namespace stewardship rules defined by artifact governance

Examples of stable identifier patterns include names such as:

- `readiness.basic-ops`
- `readiness.higher-assurance`
- `org.example.readiness.partner-grade`

An implementation or ecosystem steward should not reuse an existing `profileId` for an incompatible meaning.

## Naming Guidance

Profile identifiers should avoid:

- generic names that collide with unrelated ecosystems
- version numbers embedded in the base conceptual identifier
- names that imply baseline protocol invalidity for implementations that do not claim the profile

If multiple organizations define profiles in the same general area, namespaced identifiers should be preferred.

## Compatible Profile Evolution

A readiness profile may evolve compatibly when a later revision:

- clarifies existing requirements without changing their meaning
- adds optional explanatory metadata
- improves evidence examples without changing the minimum expectation
- tightens declaration structure in ways that do not invalidate previously honest claims

Compatible evolution should preserve the same `profileId`.

If a profile publishes explicit revision metadata, the revision should be monotonic.

## Incompatible Profile Evolution

A readiness profile evolves incompatibly when a later revision:

- changes the meaning of an existing requirement
- adds a new mandatory requirement that materially changes the operational bar
- changes forbidden behavior in a way that makes previously valid claims misleading
- reinterprets the profile as a different operational tier

Incompatible evolution should not silently replace the earlier profile meaning.

Instead, the steward should do one of the following:

- mint a new `profileId`
- define a successor profile and mark the older profile deprecated
- declare explicit incompatibility between revisions if a registry or catalog supports that expression

## Profile Revision Metadata

A readiness profile declaration should make evolution legible through metadata such as:

- `profileId`
- `revision`
- `supersedes`
- `compatibilityClass`
- `status`

This document does not require one universal schema, but declarations should be clear enough that an evaluator can tell whether two declarations refer to the same conceptual profile and whether one replaces the other compatibly.

## Relationship To Versioning Policy

The general versioning and evolution policy still governs classification of clarifying, additive, tightening, and breaking changes.

For readiness profiles, the critical distinction is whether an implementation that previously made an honest claim could still make that same claim honestly after the revision.

If the answer is no, the evolution should be treated as incompatible for claim purposes.

## Progressive Adoption Concept

An implementation may be progressing toward a readiness profile before it can honestly claim full support.

That state is progressive adoption, not profile conformance.

Progressive adoption exists to support rollout planning, partner communication, and internal readiness tracking without diluting claim integrity.

## What Progressive Adoption May Communicate

A progressive adoption declaration may communicate:

- the target `profileId`
- the revision being targeted
- requirements already satisfied
- requirements not yet satisfied
- blockers, rollout stage, or expected completion state

These declarations may appear in documentation, ecosystem catalogs, or discovery artifacts where non-final capability information is appropriate.

## What Progressive Adoption May Not Claim

A progressive adoption declaration may not:

- claim full support for a readiness profile before all mandatory requirements are met
- imply that partial adoption is equivalent to conformance
- hide unsatisfied mandatory requirements behind vague labels such as "mostly compliant"
- reinterpret a preview or work-in-progress state as a readiness profile tier

If an implementation has not yet satisfied all mandatory requirements, the implementation must not advertise the profile as fully supported.

## Partial Satisfaction Guidance

If an implementation satisfies some but not all readiness requirements, it should express that state as one of:

- progress toward `profileId`
- targeted revision under adoption
- satisfied and unsatisfied requirement sets

It should not collapse partial satisfaction into a binary supported/unsupported claim if doing so would mislead downstream consumers about current operational maturity.

## Discovery And Catalog Interaction

If readiness claims appear in discovery or registry contexts, an implementation should distinguish between:

- fully supported readiness profiles
- profiles under adoption
- profiles planned but not yet implemented

A consumer should be able to tell whether a profile is claimable now or only targeted for later.

## Deprecation And Replacement Interaction

When a readiness profile is superseded, stewards should make clear:

- whether the replacement is compatible or incompatible
- whether prior claims remain valid for a transition period
- whether progressive adoption declarations should target the old or new profile

This keeps adoption signaling consistent during profile turnover.

## Example Role

Examples under `examples/` are non-normative illustrations of:

- readiness profile revision metadata
- progressive adoption declarations

They do not define a mandatory catalog or certification workflow.
