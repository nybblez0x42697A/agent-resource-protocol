# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.0] - 2026-05-03

First numbered release of the Agent Resource Protocol (AGRP). The release boundary
is the artifact set declared at `spec/charter/agrp-v1-artifact-set.md` lines 41-67.
The publication manifest at `docs/release-publication/agrp-v1.0.0-publication-manifest.example.json`
enumerates included normative artifacts, supporting materials, deferred areas, and
the per-increment release history.

### Added

- AGRP v1 normative artifact set: 27 files enumerated under `spec/charter/agrp-v1-artifact-set.md` lines 41-67, covering charter, glossary, RSPL (resource model + lineage + lifecycle), control-plane envelope, HTTP/JSON binding, security, extensions, discovery, versioning, deprecation, composition, diagnostics, observability, rollout, deployment, governance, and the seven compliance documents. Final v1 enumeration was reconciled at this increment (incr 0046, commit 902f769).
- 11 conformance vectors added under `examples/conformance-vectors/`: fixtures for `audit-record`, `lineage-node`, `registration-record`, `resource-entity`, and standalone `lifecycle-transition` (valid + invalid pairs), plus a `profile-declaration.replaced-missing-supersedes.invalid` regression guard. Vector total at v1.0.0: 19 (incr 0041, commit 7f34a71).
- Conformance harness `tools/conformance/run_conformance_vectors.py` validating the AGRP v1 vector corpus; harness exits 0 on all 19 vectors throughout the 0043..0048 program (incr 0043, commit 83a7980).
- 10 load-bearing glossary terms added to `spec/glossary/protocol-glossary.md`: Resource Authority, Trust Boundary, Capability Advertisement / Capability Negotiation, Attestation, Evidence, Control-Plane, Transport Binding, Readiness Profile, Conformance Claim, Failure Taxonomy / Diagnostic Code (incr 0041, commit 7f34a71).
- Retrospective ADRs documenting v1 readiness decisions: ADRs under `docs/decisions/` covering charter scope, supporting-material classification, conformance-harness conditional support, profile-declaration `status=replaced` conditional, and control-plane `statusFilter` resolution (incr 0044, commit 2d7e128).
- Release readiness audit document at `docs/reviews/release-readiness-audit.md` enforcing the "exactly one new file, zero edits elsewhere" discipline; the audit's Thread 2 finding became the entire scope of 0046 (incr 0045, commit 69bf3ae).
- Northstar Tool Registry reference adaptation: design narrative at `docs/adaptations/northstar-tool-registry.md` and concrete artifact bundle at `examples/adaptations/northstar-tool-registry/` (15 JSON artifacts plus a bundle README), demonstrating an end-to-end mapping of a synthetic tool registry onto AGRP v1 (incr 0047, commit fc0d7bf).
- Northstar adaptation replay tool at `tools/adaptations/replay-northstar.py`: executable verification of the 0047 bundle (15-step state-machine replay, 8 invariants, negative test); produces a final-state snapshot and exits non-zero on any invariant violation (incr 0048, commit 3ee0801).

### Changed

- Tightened four schemas under `models/schemas/`: `lifecycle-transition.schema.json` (versionId and actor required, evidenceRefs optional), `control-plane-envelope.schema.json` error model (`code` required, `additionalProperties: false`), `ListResourceVersions.statusFilter` resolved against `registrationStatus`, `profile-declaration.schema.json` enforces `status=replaced => supersedes required` via per-branch `if/then` (incr 0041, commit 7f34a71).
- Aligned normative prose across four spec files: `profile-declaration-and-discovery-interoperability.md` documents `unsatisfiedMandatoryRequirements`, `baseConformance`, `additionalRequirements`, `evidenceExpectations`, and `forbiddenBehaviors`; `control-plane-contracts.md` clarifies `statusFilter` semantics; `http-json-binding.md` reconciles its error model with the tightened envelope schema; deprecated "resource entity" replaced with formal artifact references at four sites under `spec/rspl/` (incr 0041, commit 7f34a71).
- Hyphenation canonicalized across the corpus: control-plane (hyphenated), trust boundary (no "trust domain"), managed resource, higher-layer protocol (incr 0041, commit 7f34a71).
- Resolved post-audit deferrals from 0041's audit log; spec-only follow-ups with no schema, vector, or harness changes (incr 0042, commit 6c00cca).
- v1 readiness pass cleanup across spec and tooling; first of three readiness-pass increments. No schema, vector, or harness-logic changes (incr 0043, commit 83a7980).
- Charter/spec inventory reconciled to surface previously-undeclared spec files into `spec/charter/agrp-v1-artifact-set.md`'s enumeration; closes the open question surfaced by 0045's Thread 2 (incr 0046, commit 902f769).

### Notes

- Deferred areas not in v1.0.0: `spec/sepl/` (self-evolution protocol layer) per `spec/charter/agrp-v1-artifact-set.md` lines 88-100. Future binding profiles beyond HTTP/JSON are also deferred. Adopter mappings under `adopters/` are templates only at v1.0.0 (incr 0046, commit 902f769).
- Conformance scope: an adopter claiming "AGRP v1" support is claiming conformance to the artifact set enumerated at `spec/charter/agrp-v1-artifact-set.md` lines 41-67, not to "every file in the repo". Supporting materials under `docs/`, `examples/`, `tools/`, and `adopters/` are non-normative per `spec/charter/agrp-v1-artifact-set.md` lines 85-92 (incr 0046, commit 902f769).
