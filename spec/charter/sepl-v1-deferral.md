# SEPL v1 Deferral

## Status

This document defines the `AGRP v1` decision to defer self-evolution protocol standardization from the initial release boundary.

It builds on:

- `spec/charter/repository-charter.md`
- `spec/charter/agrp-v1-artifact-set.md`
- `spec/versioning/versioning-and-evolution-policy.md`

## Scope

This document is normative for:

- the decision that `SEPL` is not part of `AGRP v1`
- the rule that `spec/sepl/` remains a future protocol area until a later release explicitly adds it
- the requirement that future `SEPL` standardization be introduced through a later normative release boundary

It is not normative for:

- the content of any future `SEPL` specification
- a roadmap date for self-evolution standardization
- temporary research notes or exploratory design work that remain outside the `v1` boundary

## Purpose

The repository taxonomy reserves space for self-evolution protocol work under `spec/sepl/`.

This document makes explicit that the existence of that directory does not mean self-evolution semantics are already part of the initial protocol release.

`AGRP v1` standardizes the resource substrate and its surrounding operational envelope, not the self-evolution layer.

## Deferral Decision

`SEPL` is not part of `AGRP v1`.

No claim of `AGRP v1` conformance, readiness, or interoperable declaration support should be interpreted as including standardized self-evolution semantics.

## Repository Interpretation Rule

The presence of `spec/sepl/` in the repository expresses future design space, not inclusion in the `v1` release boundary.

A protocol-area directory becomes part of a released standard only when a normative release-boundary document explicitly includes its artifacts.

## Future Introduction Rule

Any future `SEPL` standardization must be introduced through a later normative release that:

- identifies the included `SEPL` artifacts explicitly
- classifies compatibility impact using the protocol versioning rules
- states whether `SEPL` is optional, additive, or release-boundary-defining for that later release

Until such a release exists, `SEPL` remains deferred from the protocol standard even if exploratory material appears in the repository.

## Sharpened Deferral For Specific SEPL Concerns

The `Future Introduction Rule` defers `SEPL` standardization wholesale. Four `SEPL` concerns are named here so that the surface remaining deferred is explicit:

- `SEPL-02` — declaration of evaluation criteria a candidate-change proposal must satisfy before commit, including criterion taxonomy, scope, and verification mechanism
- `SEPL-03` — commit semantics for accepted self-mutation, including the role distinction between proposing and approving operators and the rollback provenance carried with such commits
- `SEPL-05` — the per-change approval and policy gate between candidate proposal and commit, including the policy-expression mechanism and the audit shape of approve/reject decisions
- `SEPL-06` — trace granularity and retention semantics for evolution evidence, including per-proposal granularity and retention policy

These four concerns remain deferred from the protocol standard. All other `SEPL` concerns likewise remain deferred under the `Future Introduction Rule` above; this section sharpens the deferral surface for the four concerns named here without altering that rule.

## SEPL-08 Operator Extension Model Opened Via Release Boundary

This section discharges the `Future Introduction Rule` at lines 49 to 55 above for one specific `SEPL` concern: `SEPL-08`, the operator extension model.

`AGRP v1` opens `SEPL-08` — named at `docs/audits/sepl-coverage-matrix.md:48` and routed to the release-boundary path at `docs/audits/sepl-opening-decision.md:29` and `docs/audits/sepl-scope-audit.md:133` — by identifying `models/schemas/capability-advertisement.schema.json#/extensions` (the `extensions` array declared at line 22 and listed in the schema's required array at line 55) as the `SEPL-08 v1` included artifact.

The compatibility class for this opening is `additive` per `spec/versioning/versioning-and-evolution-policy.md:121, :131-139`. This opening is not `release-boundary-defining`.

Pre-existing `AGRP v1` implementations remain conformant: implementations that emit no `extensions` field content, that emit an empty `extensions: []` array, or that emit any prior namespaced extension identifier are unchanged by this opening, and no prior `AGRP v1` conformance claim is invalidated.

The normative declaration shape for `SEPL-08` operator extensions, together with the direct evidence already present in the corpus, is codified in `spec/sepl/operator-extension-model.md`. Direct evidence is exhibited by:

- `examples/adaptations/northstar-tool-registry/14-capability-advertisement.example.json#/extensions`
- `examples/adaptations/pinecrest-data-products/14-capability-advertisement.example.json#/extensions`
- `examples/adaptations/helios-governance-registry/15-capability-advertisement.example.json#/extensions`

This opening is scoped to `SEPL-08` only. All other `SEPL` concerns remain deferred under the `Future Introduction Rule` above and the `Sharpened Deferral For Specific SEPL Concerns` section between this section and that rule; this opening does not alter their disposition.

## Relationship To AGRP v1

`AGRP v1` should be interpreted as:

- the `AGRP v1` artifact set
- excluding deferred areas such as `SEPL` unless those areas are explicitly listed in the artifact-set definition

## Example Role

This deferral decision exists to prevent accidental scope expansion.

It does not prevent future `SEPL` design work, but it requires that such work be introduced deliberately through later normative release decisions rather than by implication.
