# Helios Governance Registry — Artifact Bundle

## Status

Non-normative supporting material per `spec/charter/agrp-v1-artifact-set.md:85-92`. This bundle accompanies the design document at `docs/adaptations/helios-governance-registry.md` and demonstrates one synthetic registry's end-to-end use of AGRP v1 schemas across a propose → committee-review → commit operator flow.

The bundle and the design document are illustrative. Where any wording or shape in this bundle conflicts with the AGRP v1 spec corpus, the corpus is authoritative.

## Reading order

The 19 artifacts walk one focal policy revision (`helios/example-policy-revision`, version `1.0.0`) through the full propose → review → commit arc, plus a representative out-of-scope rejection example. Read them in numerical order to follow the narrative; cross-references resolve to sibling files.

| # | File | Validates against | Phase / purpose |
|---|------|-------------------|-----------------|
| 00 | `00-policy-revision-resource.v1.example.json` | `models/schemas/resource-entity.schema.json` | Pre-proposal: the focal resource entity. |
| 01 | `01-register-resource-version.v1.proposal.request.json` | `models/schemas/control-plane-envelope.schema.json` (RegisterResourceVersion request branch) | Phase 2 — Propose: proposer registers the draft via control-plane envelope; `actor: "helios:proposer:..."` (SEPL-01 surface). |
| 02 | `02-register-resource-version.v1.proposal.response.json` | `models/schemas/control-plane-envelope.schema.json` (response branch) | Phase 2 — Propose: registry response carrying registration-record + initial lineage node. |
| 03 | `03-registration-record.v1.proposal.example.json` | `models/schemas/registration-record.schema.json` | Phase 2 — Propose: standalone registration-record view; `metadata.evaluationCriteriaRefs[]` carries the proposal's criterion claims (SEPL-01 surface). |
| 04 | `04-audit-record.proposal.example.json` | `models/schemas/audit-record.schema.json` | Phase 2 — Propose: proposer-stage audit-record naming the proposer URN. |
| 05 | `05-lineage-node.v1.draft.example.json` | `models/schemas/lineage-node.schema.json` | Phase 2 — Propose: initial draft-state lineage node (`parentVersionId: null`). |
| 06 | `06-evidence-attestation.proposal-criterion.example.json` | prose shape at `spec/compliance/evidence-freshness-and-attestation.md:60-89` | Phase 2 — Propose: proposer-side criterion-attestation evidence (SEPL-01 surface). |
| 07 | `07-audit-record.review.example.json` | `models/schemas/audit-record.schema.json` | Phase 3 — Review: reviewer-stage audit-record naming the reviewer URN. |
| 08 | `08-evidence-attestation.review.redacted.example.json` | prose shape at `spec/compliance/evidence-freshness-and-attestation.md:60-89` plus the `metadata.redacted` and `metadata.redactionPolicyRef` extension fields | Phase 3 — Review: reviewer evidence-attestation carrying in-trace redaction markers (SEPL-07 surface). |
| 09 | `09-audit-record.commit.example.json` | `models/schemas/audit-record.schema.json` | Phase 4 — Steward decision: commit audit-record naming the steward URN; cites the redacted reviewer evidence by `evidenceId` and describes the redaction-aware decision in `rationale` (SEPL-07 surface). |
| 10 | `10-lineage-node.v1.committed.example.json` | `models/schemas/lineage-node.schema.json` | Phase 5 — Commit transition: committed-state lineage node entry. |
| 11 | `11-lifecycle-transition.draft-to-active.request.json` | `models/schemas/control-plane-envelope.schema.json` (TransitionLifecycleState request branch) | Phase 5 — Commit transition: steward-issued envelope-wrapped transition request. |
| 12 | `12-lifecycle-transition.draft-to-active.event.json` | `models/schemas/lifecycle-transition.schema.json` (standalone, not envelope-wrapped) | Phase 5 — Commit transition: standalone transition event payload (no `operation` field). |
| 13 | `13-evidence-attestation.commit.example.json` | prose shape at `spec/compliance/evidence-freshness-and-attestation.md:60-89` | Phase 5 — Commit transition: commit-stage governance evidence-attestation. |
| 14 | `14-audit-record.transition.example.json` | `models/schemas/audit-record.schema.json` | Phase 5 — Commit transition: transition audit-record (`action: "update"`, matching the precedent set by Northstar slot 13 and Pinecrest slot 13 because `transition` is not in the audit-action enum). |
| 15 | `15-capability-advertisement.example.json` | `models/schemas/capability-advertisement.schema.json` | Phase 6 — Post-commit advertisement: registry capability advertisement listing the active policy revision. |
| 16 | `16-profile-declaration.proposer-scope.example.json` | `models/schemas/profile-declaration.schema.json` (`oneOf` → `adoptingDeclaration` variant) | Phase 1 — Pre-proposal: proposer-scope profile declaring scope tuple in `additionalRequirements` and negative invariants in `forbiddenBehaviors` (SEPL-04 surface). |
| 17 | `17-profile-declaration.privacy-tier.example.json` | `models/schemas/profile-declaration.schema.json` (`oneOf` → `adoptingDeclaration` variant) | Bundle-level: privacy-tier profile declaring redaction-policy vocabulary and surfacing-prohibition invariants (SEPL-07 surface). |
| 18 | `18-audit-record.rejection.example.json` | `models/schemas/audit-record.schema.json` | Concrete failure-mode example: out-of-scope rejection on a hypothetical proposal, with `rationale` carrying the violated invariant (SEPL-04 surface). |

## Conventions

- **Identifiers** use a `helios:<role>:<id>` URN form for actor-bearing fields (proposer, reviewer, steward; attestor where attested) and `helios:<kind>:<name>` URNs for non-actor identifiers (criterion refs, redaction-policy URN, profile profileIds, evidenceIds).
- **Timestamps** are formatted with timezone designators in standard format. Sample timestamps within the bundle are internally consistent: proposal at `2026-05-09T10:00:00Z`, review at `2026-05-09T11:30:00Z`, steward decision at `2026-05-09T13:00:00Z`, transition at `2026-05-09T13:05:00Z`.
- **Cross-references** between sibling files use `evidenceRefs`, `auditRef`, `lineageRef`, and the registration-record / lineage-node `parentVersionId` field. Every URN that points at a sibling-file `evidenceId` resolves within the bundle; URNs that name resources outside the bundle (e.g., `urn:helios:evidence:scope-self-check:...`) are illustrative supporting evidence the registry would maintain separately.
- **Implementation-defined extensions** (e.g., `metadata.redacted`, `metadata.redactionPolicyRef`, the `helios:<role>:<id>` URN convention) are described in `docs/adaptations/helios-governance-registry.md` §9 (Implementation-defined edges); their presence in this bundle is illustrative and not part of the AGRP v1 normative surface.

## Schema validation

Each artifact above is paired with its validation pathway (a JSON Schema under `models/schemas/` for 16 of the 19 artifacts; the prose-defined evidence-attestation field shape at `spec/compliance/evidence-freshness-and-attestation.md:60-89` for slots 06, 08, and 13). The producing increment (0055-agrp-sepl-targeted-adaptation-third-domain) verifies bundle conformance via two complementary checks at C6:

1. The AGRP v1 conformance harness at `tools/conformance/run_conformance_vectors.py` runs against the spec-corpus vector set and must remain 19 ok / 0 not_ok at C1 baseline and at C7 final (this confirms the bundle has not regressed the spec corpus).
2. A bundle-specific schema-validation pass walks every artifact in this bundle against its mapped schema (or, for evidence-attestation files, against the prose-defined field shape) and emits a per-artifact PASS / FAIL line. ZERO failures are required.

Both checks are recorded in the producing increment's `reports/` directory.

## Relationship to repository material

- `docs/adaptations/helios-governance-registry.md` — the design document that walks this bundle in narrative form. Sections 7 (End-to-end walkthrough), 8 (Concrete artifacts), and 11 (Gaps and limitations) are the most actionable for adopters.
- `docs/audits/sepl-coverage-matrix.md` — rows SEPL-01, SEPL-04, and SEPL-07 anchor the three SEPL surfaces this bundle surfaces evidence for.
- `docs/audits/sepl-scope-audit.md` — §6.2 prose groupings ("Envelope and precondition adjacency", "Evaluation, trace, and privacy adjacency") supply the audit-side rationale for `needs-targeted-adaptation` disposition.
- `examples/adaptations/northstar-tool-registry/` and `examples/adaptations/pinecrest-data-products/` — the two prior reference adaptations. Their bundle READMEs cover overlapping conventions in greater depth.
