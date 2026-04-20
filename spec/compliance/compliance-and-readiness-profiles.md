# Compliance and Readiness Profiles

## Status

This document defines the baseline model for higher-level readiness profiles layered above baseline conformance.

It builds on:

- `spec/conformance/baseline-conformance.md`
- `spec/observability/observability-and-trace-correlation.md`
- `spec/diagnostics/failure-taxonomy-and-diagnostics.md`
- `spec/rollout/rollout-and-stage-policy.md`
- `spec/governance/artifact-governance-and-registry-policy.md`

## Scope

This document is normative for:

- readiness profile concepts
- allowed readiness requirements
- guardrails that keep readiness profiles distinct from baseline protocol semantics

It is not normative for:

- centralized certification programs
- audit-provider accreditation
- commercial assessment offerings

## Purpose

Baseline conformance answers whether an implementation preserves protocol semantics.

Readiness profiles answer whether an implementation also satisfies higher operational expectations that matter for broader deployment confidence.

These two concerns must remain distinct.

## Relationship To Baseline Conformance

Every readiness profile is layered on top of baseline conformance.

An implementation may not claim a readiness profile unless it already satisfies baseline conformance.

Readiness profile support does not replace or weaken baseline conformance requirements.

## Readiness Profile Concept

A readiness profile is a named set of additional operational expectations such as:

- observability practices
- diagnostics quality
- rollout discipline
- deprecation communication
- governance transparency

Readiness profiles are about operational maturity, not alternate protocol semantics.

## What A Readiness Profile May Require

A readiness profile may require:

- stronger observability or support-reference discipline
- clearer failure diagnostics
- documented rollout stages for non-general-availability artifacts
- deprecation and sunset communication practices
- documented governance or namespace stewardship rules
- stronger compatibility declaration discipline

These requirements may be stricter than baseline expectations so long as they remain semantically compatible.

## What A Readiness Profile May Not Redefine

A readiness profile may not:

- redefine the meaning of baseline operations
- redefine baseline error classes or lifecycle semantics
- change baseline version compatibility rules
- reinterpret reserved artifact identifiers incompatibly
- claim that non-support of a profile is baseline non-conformance

## Example Readiness Levels

This document does not mandate a single universal ladder, but readiness profiles may commonly describe levels such as:

- basic operational readiness
- higher-assurance operational readiness

The exact names are profile identifiers, not implied protocol constants.

## Profile Declaration Guidance

A readiness profile declaration should identify:

- `profileId`
- `baseConformance`
- `additionalRequirements`
- `evidenceExpectations`
- `forbiddenBehaviors`

The declaration should make clear that the profile is layered above baseline conformance rather than replacing it.

## Evidence Expectations

A readiness profile may require that an implementation be able to produce evidence for profile claims, such as:

- diagnostic examples
- trace correlation behavior
- rollout disclosures
- governance or namespace documentation

This document does not mandate a centralized evidence repository.

## Compatibility Claims

An implementation may claim:

- baseline conformance only
- baseline conformance plus one or more readiness profiles

An implementation must not imply that a readiness profile is baseline-mandatory unless a later normative conformance document explicitly says so.

## Readiness Profile Failure

Failure to satisfy a readiness profile does not imply baseline protocol invalidity unless the failure also violates baseline conformance.

Readiness assessment is therefore stricter than baseline conformance, but it is not a substitute for it.

## Governance Interaction

Readiness profiles themselves should follow the artifact governance and versioning rules already defined elsewhere.

A readiness profile should use a stable identifier and should not be repurposed for incompatible meaning.

## Example Role

Examples under `examples/` are non-normative illustrations of:

- a basic readiness profile
- a higher-assurance readiness profile

They do not define a mandatory certification or audit process.
