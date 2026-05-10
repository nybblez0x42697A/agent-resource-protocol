# SEPL Coverage Matrix

This matrix is the source-anchored evidence map produced by the 0052
SEPL scope audit. Each row corresponds to one of the eight SEPL-intent
concerns locked at C2 (see `docs/audits/sepl-scope-audit.md` §4 for the
abridged inventory). The columns and conventions are locked at C3 (see
`.specweave/increments/0052-agrp-sepl-scope-audit-and-opening-decision/spec.md`
"Audit Deliverable Layout" section).

**Cell conventions** (per C3 lock):

- Evidence cells (Northstar / Pinecrest) cite a real artifact file with a
  JSON-pointer-style field path (`<file-path>#/<field-path>`) when not
  `(none)`.
- Spec/paper anchor cells cite a real file with a real line range
  (`<file-path>:NN-MM`) when not `(none)`.
- Empty cells use the literal string `(none)` — never blank.
- Disposition rationale references at least one evidence cell from the
  same row.

**Coverage-verdict vocabulary** (3-term, per C3):
`direct-evidenced` (load-bearing surface exercised) /
`adjacent-evidenced` (structural neighborhood exercised, load-bearing
surface not) / `unevidenced` (no evidence at any depth).

**Disposition vocabulary** (4-term, per C3):
`sharpen-defer` /
`open-via-release-boundary` /
`needs-targeted-adaptation` /
`narrow-and-defer`.

The matrix terminology — per-concern dispositions — is intentionally
distinct from the whole-audit closure-state vocabulary used in
`docs/audits/sepl-opening-decision.md`. See `sepl-scope-audit.md` §3
for the clarifying note on that split.

## Rows

| Concern | Description | Northstar evidence | Pinecrest evidence | Spec/paper anchor | Coverage verdict | Disposition | Disposition rationale |
|---------|-------------|--------------------|--------------------|-------------------|------------------|-------------|------------------------|
| **SEPL-01** Candidate-change proposal envelope | The structured envelope by which a SEPL operator proposes a candidate change to a managed resource. Defines proposal payload shape, target resource reference, and proposing operator identity. Independent of any particular evaluation criterion. | `examples/adaptations/northstar-tool-registry/01-register-resource-version.v1.request.json#/operation` and `examples/adaptations/northstar-tool-registry/01-register-resource-version.v1.request.json#/registrationRecord/resourceId` | `examples/adaptations/pinecrest-data-products/01-register-resource-version.v1.request.json#/operation` and `examples/adaptations/pinecrest-data-products/07-register-resource-version.v2.request.json#/expectedVersionId` | `docs/papers/autogenesis-agp-decomposition.md:82-88` (§6 Operatorized loop) and `docs/papers/autogenesis-agp-decomposition.md:181-191` (§5 Underspec / Operator contracts) | `adjacent-evidenced` | `needs-targeted-adaptation` | Both adaptations exercise the envelope structural pattern (`#/operation` discriminator + payload of resource entity + audit record). The envelope shape is reusable for SEPL proposals, but neither adaptation distinguishes a *proposing* operator role from the *registering* operator, and neither exercises the SEPL-specific attachment of evaluation-criterion references at proposal time. The structural neighborhood is evidenced; the SEPL-specific role and criterion attachment surface needs an adaptation that actually exercises a propose-then-evaluate-then-commit flow before normative authoring. |
| **SEPL-02** Evaluation criterion declaration | How a SEPL implementation declares what evaluation criteria a candidate-change proposal must satisfy before commit. Covers criterion taxonomy, scope (per-resource / per-class / global), and verification mechanism. | `(none)` | `examples/adaptations/pinecrest-data-products/12-evidence-attestation.refresh-sla.example.json#/freshness/policyContext` and `examples/adaptations/pinecrest-data-products/15-profile-declaration.consumer-trust.example.json#/evidenceExpectations` | `docs/papers/autogenesis-agp-decomposition.md:80-88` (§6 "evaluating candidates") and `docs/papers/autogenesis-agp-decomposition.md:181-191` (§5 "preconditions and postconditions") | `adjacent-evidenced` | `narrow-and-defer` | Pinecrest exercises a policy-reference pattern at `#/freshness/policyContext` (`pinecrest:refresh-sla-policy:v1`) and an evidence-expectation list at the consumer-side profile (`#/evidenceExpectations`). These show one criterion taxonomy slice — SLA-style freshness criteria — but not the broader SEPL surface (per-resource / per-class / global scope, criterion-composition rules, verification mechanism declaration). Northstar contributes no evidence here. The narrow slice (policy-reference + evidence-expectation) is reusable for one disposition; the broader criterion taxonomy is too wide to open without targeted adaptation. |
| **SEPL-03** Commit semantics for accepted self-mutation, with rollback provenance | The protocol semantics for committing an accepted candidate change AND the rollback provenance associated with self-mutation. Rollback as a primitive belongs to the protocol layer broadly; SEPL's contribution is the evolution-specific provenance — proposing operator, evaluation evidence, approval chain. | `examples/adaptations/northstar-tool-registry/13-audit-record.transition.example.json#/evidenceRefs` and `examples/adaptations/northstar-tool-registry/13-audit-record.transition.example.json#/actor` | `examples/adaptations/pinecrest-data-products/13-audit-record.transition.example.json#/evidenceRefs` and `examples/adaptations/pinecrest-data-products/12-evidence-attestation.refresh-sla.example.json#/subject/transition` | `docs/papers/autogenesis-agp-decomposition.md:80-88` (§6 "committing accepted updates") and `docs/papers/autogenesis-agp-decomposition.md:246-250` (Bottom-line "lifecycle, lineage, auditability, and rollback belong in the protocol layer") | `adjacent-evidenced` | `narrow-and-defer` | Both adaptations exercise an evidence-provenance pattern at commit: the audit record's `#/evidenceRefs` array points at attestation IDs that back the transition, and Pinecrest's evidence record explicitly carries `#/subject/transition` linking the evidence to the version transition. This evidences the *provenance shape* SEPL needs. What neither adaptation exercises is the role distinction between a *proposing* operator and a *steward / approver* operator — both adaptations collapse the roles into a single audit-record `#/actor`. The provenance shape can be narrowed to specify in normative SEPL form; the multi-role distinction is broader and benefits from deferral. |
| **SEPL-04** Operator-contract preconditions and failure modes | The set of preconditions a SEPL operator must satisfy to propose a change, and the failure modes the protocol enumerates when those preconditions don't hold. Covers operator-side declared invariants and the protocol's required failure-response shape. | `(none)` | `examples/adaptations/pinecrest-data-products/07-register-resource-version.v2.request.json#/expectedVersionId` (precondition: prior version `1.0.0` expected before registering `1.1.0`) | `docs/papers/autogenesis-agp-decomposition.md:181-191` (§5 Underspec "preconditions and postconditions, failure modes") | `adjacent-evidenced` | `needs-targeted-adaptation` | The optimistic-lock precondition pattern is exercised in Pinecrest's v2 register request (`#/expectedVersionId = "1.0.0"`). Northstar contributes register/update adjacency but does not carry an `expectedVersionId` field on its v2 register request, so this row's evidence is Pinecrest-only. Pinecrest's slice is a single-field optimistic-lock check — one corner of the precondition surface. Neither adaptation exercises operator-side declared invariants (e.g., "this operator only proposes changes within scope X"), and the adaptations deliberately exclude conflict/error walkthroughs, so failure-mode response shapes are not authored here. The operator-side invariant surface needs a targeted adaptation that actually exercises operator-declared scope before the SEPL-specific precondition vocabulary can be opened. |
| **SEPL-05** Approval / policy gate | The approval/review gate between candidate-change proposal and commit. Defines who/what authorizes a candidate to commit, the policy-expression mechanism, and the audit shape of approve/reject decisions. | `examples/adaptations/northstar-tool-registry/13-audit-record.transition.example.json#/actor` (steward as implicit approver) | `examples/adaptations/pinecrest-data-products/15-profile-declaration.consumer-trust.example.json#/forbiddenBehaviors` and `examples/adaptations/pinecrest-data-products/14-capability-advertisement.example.json#/profiles` | `docs/papers/autogenesis-agp-decomposition.md:181-191` (§5 Underspec "approval and policy gates") and `docs/papers/autogenesis-agp-decomposition.md:84-88` (§6 "operator boundaries make self-evolution reviewable and auditable") | `adjacent-evidenced` | `narrow-and-defer` | Pinecrest's profile-declaration carries a policy expression — `#/forbiddenBehaviors` enumerates policy items, and the capability advertisement at `#/profiles` declares which policies an implementation operates under. This is a one-shot policy-declaration pattern: implementations declare profile adherence at advertisement time. What neither adaptation exercises is a per-change approval gate — both treat the audit-record `#/actor` as an implicit approver without a separate proposal-vs-approval boundary. The profile-as-policy-gate slice is narrowable; per-change approval semantics are broader and benefit from deferral. |
| **SEPL-06** Trace granularity and retention for evolution evidence | The protocol's stance on what trace data SEPL operators emit during proposal/evaluation/commit, and how long that data is retained for evidence purposes. Distinguished from RSPL observability because traces here are evidentiary inputs to the evaluation criterion. | `(none)` | `examples/adaptations/pinecrest-data-products/12-evidence-attestation.refresh-sla.example.json#/freshness/freshnessWindowDays` and `examples/adaptations/pinecrest-data-products/12-evidence-attestation.refresh-sla.example.json#/supportingEvidenceRefs` | `docs/papers/autogenesis-agp-decomposition.md:193-202` (§6 Underspec / Trace and Observability Model — "trace granularity, retention policy") | `adjacent-evidenced` | `narrow-and-defer` | Pinecrest's evidence-attestation carries a retention-window pattern at `#/freshness/freshnessWindowDays` (31 days) and a multi-reference evidence chain at `#/supportingEvidenceRefs` (the attestation cites four supporting evidence records). This is structurally close to what SEPL evidence retention would need — a freshness window plus a multi-record evidentiary chain. What neither adaptation exercises is *granularity*: both Pinecrest's freshness pattern and Northstar's lineage are coarse-grained (per-version), whereas SEPL evidence may need per-proposal or per-evaluation granularity. Northstar contributes no evidence in this row. The retention-window pattern is narrowable; the granularity question benefits from deferral. |
| **SEPL-07** Privacy / redaction boundaries for self-evolution traces | How SEPL traces handle sensitive data that evolution operators encounter during candidate evaluation. Covers redaction policy, privacy-tier declaration, and the audit shape when redacted trace data feeds an evaluation decision. | `(none)` | `examples/adaptations/pinecrest-data-products/15-profile-declaration.consumer-trust.example.json#/additionalRequirements` (privacy posture: aggregation-only, pii-redacted feature flag) and `examples/adaptations/pinecrest-data-products/15-profile-declaration.consumer-trust.example.json#/forbiddenBehaviors` (re-identification ban) | `docs/papers/autogenesis-agp-decomposition.md:193-202` (§6 Underspec — "privacy or redaction boundaries") | `adjacent-evidenced` | `needs-targeted-adaptation` | Pinecrest's consumer-trust profile carries a privacy-posture declaration at `#/additionalRequirements` (aggregation-only access, pii-redacted feature flag) and a redaction-adjacent policy at `#/forbiddenBehaviors` (no row-level join bypassing aggregation thresholds, no re-identification by external join). This evidences a privacy-policy *declaration* pattern. What neither adaptation exercises is redaction *in the trace data itself* — there are no examples of evaluation evidence carrying redaction markers, no audit shape for redacted-evidence-fed decisions, and no privacy-tier vocabulary attached to evidence records. Northstar contributes no evidence here. A targeted adaptation that actually exercises evidence-with-redaction-markers is needed before the SEPL-specific surface can be opened. |
| **SEPL-08** Operator extension model (alternate operators / strategies) | How additional SEPL operators or alternate operator strategies extend the protocol without fragmenting interoperability. Centered on operator-kind taxonomy and operator-side compatibility classification. The paper's mention of resource kinds and custom metadata appears as compatibility pressure from the source text only — RSPL extension policy ownership remains with RSPL. | `examples/adaptations/northstar-tool-registry/14-capability-advertisement.example.json#/extensions` (declares `northstar:extension:northstar-stage-metadata:v1`) | `examples/adaptations/pinecrest-data-products/14-capability-advertisement.example.json#/extensions` (declares two named extensions with `:v1` versioning: `pinecrest:extension:composition-deps-on-resource-entity:v1`, `pinecrest:extension:refresh-sla-policy:v1`) | `docs/papers/autogenesis-agp-decomposition.md:204-206` (§7 Underspec / Extension Model) | `direct-evidenced` | `open-via-release-boundary` | Both adaptations exercise the extension-declaration pattern directly. Northstar's `#/extensions` advertises one extension; Pinecrest's `#/extensions` advertises two, each with `:v1` semantic versioning baked into the extension identifier. This is structurally exactly what SEPL operator-extension declarations would carry — a list of namespaced, versioned extension identifiers advertised at capability time, classified by the surrounding `conformance` posture (`baseline`). The pattern is concrete enough to specify in normative SEPL artifacts: SEPL operator extensions can reuse this shape, namespaced under operator-kind rather than feature-extension. The release-boundary increment can declare the SEPL-operator-extension subset of this surface as a tightly scoped first slice. |

## Summary

| Verdict | Count | Concerns |
|---------|------:|----------|
| `direct-evidenced` | 1 | SEPL-08 |
| `adjacent-evidenced` | 7 | SEPL-01, SEPL-02, SEPL-03, SEPL-04, SEPL-05, SEPL-06, SEPL-07 |
| `unevidenced` | 0 | — |

| Disposition | Count | Concerns |
|-------------|------:|----------|
| `sharpen-defer` | 0 | — |
| `open-via-release-boundary` | 1 | SEPL-08 |
| `needs-targeted-adaptation` | 3 | SEPL-01, SEPL-04, SEPL-07 |
| `narrow-and-defer` | 4 | SEPL-02, SEPL-03, SEPL-05, SEPL-06 |

The dispositional shape (1 open / 4 narrow-and-defer / 3 needs-targeted-adaptation / 0 sharpen-defer) is what `docs/audits/sepl-scope-audit.md` §6 walks narratively, and what §7 + §8 + the closure-state decision document use to recommend a whole-audit closure state.

## Post-opening evidence refresh

As of 2026-05-10, three normative changes have shipped that extend the evidence base reflected in §2 above. Disposition values and coverage verdicts in the table at line 39 are unchanged by this refresh; this section extends the rationale base by recording what evidence has been added to the corpus since the original audit closure on 2026-05-07.

### 4.1 SEPL-01, SEPL-04, SEPL-07 — Helios bundle direct evidence

The 0055 increment authored a third reference adaptation, `docs/adaptations/helios-governance-registry.md`, with a 19-artifact bundle under `examples/adaptations/helios-governance-registry/`. Per the design doc's `## 11. Gaps and limitations` section, the bundle exercises three SEPL surfaces:

- SEPL-01 (candidate-change proposal envelope) — surfaced by bundle slots 01 / 02 / 03 / 04 / 06 (proposal arc with proposer URN on `actor`, criterion-reference attachment at proposal time) plus slots 09 / 11 / 14 (commit and transition with steward URN, demonstrating the propose-vs-registrar role split).
- SEPL-04 (operator-contract preconditions and failure modes) — surfaced by slot 16 (`profile-declaration.proposer-scope.example.json` with scope tuple in `additionalRequirements` and negative invariants in `forbiddenBehaviors`) plus slot 18 (`audit-record.rejection.example.json` with concrete out-of-scope reason in `rationale`).
- SEPL-07 (privacy / redaction boundaries for self-evolution traces) — surfaced by slot 08 (`evidence-attestation.review.redacted.example.json` with `metadata.redacted: true` and `metadata.redactionPolicyRef`), slot 17 (`profile-declaration.privacy-tier.example.json`), slot 09 (commit `audit-record.rationale` describing the decision in non-content terms), and slot 07 (reviewer audit-record).

### 4.2 SEPL-02, SEPL-03, SEPL-05, SEPL-06 — charter sharpening

The 0054 increment added a new section to `spec/charter/sepl-v1-deferral.md`, `Sharpened Deferral For Specific SEPL Concerns`, naming SEPL-02, SEPL-03, SEPL-05, and SEPL-06 explicitly as concerns whose deferral surface is now sharpened under the existing wholesale framework. The four concerns retain the `narrow-and-defer` disposition shown in the table; the sharpening codifies what each concern's deferred surface includes.

### 4.3 SEPL-08 — release-boundary opening

The 0053 increment opened the SEPL-08 slice via the release-boundary path at `spec/charter/sepl-v1-deferral.md:49-55`. Two normative artifacts landed: a charter section `SEPL-08 Operator Extension Model Opened Via Release Boundary` (which identifies `models/schemas/capability-advertisement.schema.json#/extensions` as the SEPL-08 v1 included artifact and classifies the change as `additive`) and a new spec/sepl/ file `spec/sepl/operator-extension-model.md` (which codifies the operator-extension declaration shape). The Helios bundle's slot 15 capability-advertisement carries two `:v1` extensions, joining the Northstar and Pinecrest direct evidence already cited in the row at line 48.

### 4.4 Verdict + disposition status

| Concern | Verdict | Disposition | Execution status |
|---------|---------|-------------|------------------|
| SEPL-01 | `adjacent-evidenced` | `needs-targeted-adaptation` | Helios direct evidence shipped 2026-05-09 (0055) |
| SEPL-02 | `adjacent-evidenced` | `narrow-and-defer` | charter sharpening shipped 2026-05-08 (0054) |
| SEPL-03 | `adjacent-evidenced` | `narrow-and-defer` | charter sharpening shipped 2026-05-08 (0054) |
| SEPL-04 | `adjacent-evidenced` | `needs-targeted-adaptation` | Helios direct evidence shipped 2026-05-09 (0055) |
| SEPL-05 | `adjacent-evidenced` | `narrow-and-defer` | charter sharpening shipped 2026-05-08 (0054) |
| SEPL-06 | `adjacent-evidenced` | `narrow-and-defer` | charter sharpening shipped 2026-05-08 (0054) |
| SEPL-07 | `adjacent-evidenced` | `needs-targeted-adaptation` | Helios direct evidence shipped 2026-05-09 (0055) |
| SEPL-08 | `direct-evidenced` | `open-via-release-boundary` | release-boundary opening shipped 2026-05-10 (0053) |

Verdict and disposition values are unchanged from the table at line 39. The execution-status column above is the new content this refresh adds.
