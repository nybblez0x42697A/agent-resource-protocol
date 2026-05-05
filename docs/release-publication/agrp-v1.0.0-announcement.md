---
Title: AGRP v1.0.0 — Release Announcement
Date: 2026-05-03
Status: published; non-normative supporting material per `spec/charter/agrp-v1-artifact-set.md` lines 85-92
---

# AGRP v1.0.0 — Release Announcement

## 1. What this is

This release publishes **AGRP v1.0.0**, the first numbered release of the Agent Resource Protocol. The release boundary is the artifact set declared at `spec/charter/agrp-v1-artifact-set.md` lines 41-67. The publication manifest at `docs/release-publication/agrp-v1.0.0-publication-manifest.example.json` enumerates included normative artifacts, supporting materials, deferred areas, the per-increment release history, and editorial notes.

This document is itself non-normative supporting material per `spec/charter/agrp-v1-artifact-set.md` lines 85-92. It walks the v1 artifact set, summarizes deferred areas, names the conformance entry points, and points to the reference adaptation. It does not introduce normative claims; where this document surfaces something AGRP says, it cites the spec file and a line range.

## 2. What AGRP v1 covers

The v1 artifact set is 27 files enumerated at `spec/charter/agrp-v1-artifact-set.md` lines 41-67. Grouped by topic:

- **Charter and glossary**: `spec/charter/repository-charter.md` (mission, scope, non-goals) and `spec/glossary/protocol-glossary.md` (neutral terminology, including the 10 load-bearing terms added during the program: Resource Authority, Trust Boundary, Capability Advertisement / Capability Negotiation, Attestation, Evidence, Control-Plane, Transport Binding, Readiness Profile, Conformance Claim, Failure Taxonomy / Diagnostic Code).
- **RSPL — resource model, registration, lineage, lifecycle**: `spec/rspl/core-resource-model.md`, `spec/rspl/registration-and-lineage-model.md`, `spec/rspl/lifecycle-and-transition-semantics.md`. The lifecycle baseline names six states — `draft`, `active`, `deprecated`, `archived`, `superseded`, `restored` — with transition semantics defined at `spec/rspl/lifecycle-and-transition-semantics.md`.
- **Control plane and binding**: `spec/control-plane/control-plane-contracts.md` defines the request/response/event envelope and the operation set; `spec/bindings/http-json-binding.md` carries the HTTP/JSON binding.
- **Security, extensions, discovery**: `spec/security/security-and-policy-model.md`, `spec/extensions/extension-and-profile-model.md`, `spec/discovery/capability-discovery-and-negotiation.md`.
- **Versioning, deprecation, composition**: `spec/versioning/versioning-and-evolution-policy.md`, `spec/versioning/agrp-v1-release-definition.md`, `spec/deprecation/deprecation-and-sunset-policy.md`, `spec/composition/dependency-and-composition-model.md`.
- **Diagnostics, observability, rollout**: `spec/diagnostics/failure-taxonomy-and-diagnostics.md`, `spec/observability/observability-and-trace-correlation.md`, `spec/rollout/rollout-and-stage-policy.md`.
- **Deployment, governance**: `spec/deployment/deployment-topology-and-trust-boundaries.md`, `spec/governance/artifact-governance-and-registry-policy.md`.
- **Compliance and readiness profiles** (seven files): `spec/compliance/compliance-and-readiness-profiles.md`, `spec/compliance/profile-evolution-and-progressive-adoption.md`, `spec/compliance/profile-declaration-and-discovery-interoperability.md`, `spec/compliance/declaration-conflict-and-supersession-resolution.md`, `spec/compliance/compliance-precedence-and-integration-policy.md`, `spec/compliance/compliance-partial-failure-handling.md`, `spec/compliance/evidence-freshness-and-attestation.md`.

The conformance baseline lives at `spec/conformance/baseline-conformance.md`.

## 3. What's not in v1

Per `spec/charter/agrp-v1-artifact-set.md` lines 88-100, an area present in the repository is part of v1 only if it is enumerated in the artifact set. Two categories sit outside the v1 boundary:

- **Deferred protocol layers**: `spec/sepl/` (the self-evolution protocol layer) is the largest deferred area. The directory exists in the repo, but no SEPL document is enumerated in the v1 artifact set. SEPL is intentionally held out of v1 and will be addressed in a later numbered release.
- **Future binding profiles**: only the HTTP/JSON binding ships in v1. Additional transport bindings are deferred and have no v1 normative shape.
- **Adopter mappings**: directories under `adopters/` exist as templates. Concrete adopter mappings are not part of v1; they live as supporting material per `spec/charter/agrp-v1-artifact-set.md` lines 85-92.

## 4. Conformance posture

The conformance entry point is the harness at `tools/conformance/run_conformance_vectors.py`, which validates each fixture under `examples/conformance-vectors/` against its declared schema. At v1.0.0, the corpus carries 19 vectors covering the standalone artifact shapes (`audit-record`, `lineage-node`, `registration-record`, `resource-entity`, `lifecycle-transition`, `profile-declaration`, `capability-advertisement`, `register-resource-version`, `transition-lifecycle-state`, `conflict-error`).

Two representative entry points:

- `examples/conformance-vectors/registration-record.valid.json` — a positive vector demonstrating a well-formed registration record.
- `examples/conformance-vectors/profile-declaration.replaced-missing-supersedes.invalid.json` — a negative vector that a v1-conformant validator must reject (the `status=replaced => supersedes required` conditional is in the schema).

The harness exits 0 on all 19 vectors at the v1.0.0 closing commit. The 0049 publication increment runs the harness at C1, C6, and C7 with green output captured each time. An adopter implementing AGRP v1 can use this harness as a starting point for their own conformance suite; the baseline definition lives at `spec/conformance/baseline-conformance.md`.

## 5. Reference adaptation — Northstar Tool Registry

Two non-normative deliverables ship alongside the v1 artifact set as a worked end-to-end mapping:

- **Design narrative**: `docs/adaptations/northstar-tool-registry.md` is a 209-line walkthrough of how a synthetic tool registry maps onto the v1 control plane, lifecycle states, and lineage model. It deliberately uses a synthetic system (Northstar) rather than a named real product so the mapping can be complete instead of apologizing for fidelity gaps.
- **Concrete bundle**: `examples/adaptations/northstar-tool-registry/` carries 15 JSON artifacts (a tool resource at v1, the registration request/response envelope, the registration record, an audit record, a lineage node, the same set for v2, a lifecycle transition request and event, an evidence attestation, an audit record for the transition, and a capability advertisement) plus a bundle README that indexes them.

A third deliverable demonstrates that the bundle is internally consistent and replayable:

- **Replay tool**: `python3 tools/adaptations/replay-northstar.py` walks the 15 artifacts in lifecycle order through an in-memory state machine, asserts 8 invariants (first-registration shape, lineage parent resolution, standalone-vs-envelope agreement, transition `fromState` matching, post-transition active-state count, evidence cross-reference, capability-advertisement recommendation, monotonic timestamps), and exits non-zero on any violation. A negative-test mode corrupts the lineage parent reference and verifies the tool detects the corruption. The tool produces a final-state snapshot for human inspection.

These three artifacts are non-normative supporting material per `spec/charter/agrp-v1-artifact-set.md` lines 85-92. They are intended to give an adopter something concrete to compare their own system against without having to re-derive the lifecycle dance from prose alone.

## 6. What comes next

This section is forward-looking but explicitly non-committing. No dates, no roadmap promises.

- **SEPL** (self-evolution protocol layer) is the largest deferred area. The directory exists in the repository, but its v1 normative shape is not yet defined.
- **Additional transport bindings** beyond HTTP/JSON are not in v1.
- **Adopter mappings** under `adopters/` are templates only at v1.0.0. Concrete mappings against existing tool registries, marketplaces, or runtime catalogs are future work.
- **Additional reference adaptations** beyond Northstar are possible if the program continues; the 0047 + 0048 increments establish the pattern.

The maintainer reserves the right to revise scope between releases. v1.0.0's commitment is anchored to the artifact set at `spec/charter/agrp-v1-artifact-set.md` lines 41-67 and not to a future-features inventory.

## 7. How to reference v1.0.0

Anchor identifiers for citation:

- **Tag**: `agrp-v1.0.0` (annotated, unsigned)
- **Release definition**: `spec/versioning/agrp-v1-release-definition.md`
- **Artifact set**: `spec/charter/agrp-v1-artifact-set.md` (lines 41-67 for the enumeration; lines 70-83 for the scope-claim semantics)
- **Publication manifest**: `docs/release-publication/agrp-v1.0.0-publication-manifest.example.json`
- **CHANGELOG**: `CHANGELOG.md` at the repository root

An adopter or implementation claiming "AGRP v1" support is claiming conformance to the artifact set declared at `spec/charter/agrp-v1-artifact-set.md` lines 41-67, not to "every file in the repository". The artifact-set document is explicit about this at lines 70-83: the v1 claim is anchored to the enumerated set, and material under `examples/`, `docs/`, `models/`, and `adopters/` is supporting material per lines 85-92.

The publication manifest carries a `releaseHistory` array recording the 8 increments (0041 through 0048) whose closing commits comprise the v1.0.0 program. Each entry carries `{ id, title, closingCommit, mergedAt }`.

## 8. Status

v1.0.0 is published as an annotated, unsigned git tag (`agrp-v1.0.0`) on the 0049 closing commit. Tag verification:

```
git tag -l agrp-v1.0.0
git show agrp-v1.0.0
git for-each-ref refs/tags/agrp-v1.0.0 --format='%(objecttype) %(taggername) %(subject)'
```

`git tag -v` is excluded by construction — the tag carries no GPG signature.

The canonical anchors for v1.0.0 are the release definition at `spec/versioning/agrp-v1-release-definition.md`, the artifact set at `spec/charter/agrp-v1-artifact-set.md`, the conformance baseline at `spec/conformance/baseline-conformance.md`, and the conformance harness at `tools/conformance/run_conformance_vectors.py`.

This announcement is supporting material per `spec/charter/agrp-v1-artifact-set.md` lines 85-92 and is not normative.
