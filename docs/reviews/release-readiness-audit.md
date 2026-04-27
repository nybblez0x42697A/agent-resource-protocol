# AGRP v1 Release Readiness Audit

## Status

**Date**: 2026-04-26
**Auditors**: per-thread Explore subagents + maintainer review at C2a/b/c (Increment 0045)
**Scope**: investigation-first audit covering three open questions deferred from increments 0041-0044 of the v1-readiness pass. No remediation in this report; per-thread recommendations route to follow-up increments only when the maintainer rules them in.

## Summary

The v1 corpus is **substantively ready for publication**. Of the three audit threads:

- **Thread 1 (Lifecycle file placement)**: `spec/rspl/lifecycle-and-transition-semantics.md` is correctly positioned. The four cross-layer citations from `control-plane/`, `bindings/`, `security/`, and `conformance/` are dependency invocations of RSPL semantics, not evidence that the file is a cross-cutting concern. Verdict: **keep**.
- **Thread 2 (v1 artifact-set verification)**: 24 of 24 declared artifacts present at their declared paths. Three undeclared files in normative-category directories (`spec/deployment/`, `spec/versioning/`, `spec/compliance/`) sit outside the charter's declared artifact-set boundary. The audit isolates these three rows but reserves judgment on whether the resolution is to amend the charter or to relocate/defer the files; that ruling belongs to a follow-up increment. Verdict: **flagged for follow-up, judgment reserved**.
- **Thread 3 (SEPL deferral status)**: the `sepl-v1-deferral.md` note remains accurate. All 20 SEPL/self-evolution/evolution-loop/operator-phase references in the corpus are either correctly-aligned forward references to a future release boundary (14) or vocabulary persistence in the glossary (6); zero stale forward references. Verdict: **deferral note remains accurate**.

**Overall: ready-with-known-deferrals.** The only follow-up candidate surfaced by this audit is a charter/spec inventory reconciliation increment for the three files identified in Thread 2.

---

## Thread 1 — Lifecycle File Placement

### Question

Should `spec/rspl/lifecycle-and-transition-semantics.md` (192 lines) move from `spec/rspl/` to a new top-level `spec/lifecycle/` directory, given that its content is referenced from multiple layers (control-plane, bindings, security, conformance, glossary, charter)?

### Method

`git grep -l "lifecycle-and-transition-semantics" spec/ docs/` was run to enumerate every citing file. Each cite was inspected with 2-3 lines of surrounding context and classified as RSPL-internal, cross-cutting, or reference-only. Cross-cutting cites were further evaluated: was the file's content load-bearing for the citing file's normative claims, or was the citing file invoking RSPL semantics from the lifecycle file's RSPL-scoped contract?

### Findings

| File | Layer | Line(s) | Citation context | Class |
|---|---|---|---|---|
| `spec/control-plane/control-plane-contracts.md` | control-plane | 11 | "Builds on" — defines `TransitionLifecycleState` operation requiring lifecycle semantics for state definitions | Cross-cutting (RSPL invocation) |
| `spec/bindings/http-json-binding.md` | bindings | 12 | "Builds on" — maps `TransitionLifecycleState` to HTTP, requires lifecycle transition semantics to preserve operation meaning | Cross-cutting (RSPL invocation) |
| `spec/security/security-and-policy-model.md` | security | 10 | "Builds on" — policy evaluation considers requested lifecycle transition as input to authorization decisions | Cross-cutting (RSPL invocation) |
| `spec/conformance/baseline-conformance.md` | conformance | 34 | Mandates implementations enforce baseline lifecycle transition rules for RSPL behavior | Cross-cutting (RSPL invocation) |
| `spec/glossary/protocol-glossary.md` | glossary | 69 | Supersession definition cites lifecycle file as the authoritative source | Reference-only |
| `spec/charter/agrp-v1-artifact-set.md` | charter | 46 | Enumeration entry; lifecycle file listed as part of v1 normative artifact set | Reference-only (manifest) |
| `docs/release-publication/agrp-v1.0.0-publication-manifest.example.json` | docs | 14 | Publication manifest example; lifecycle file listed in `includedNormativeArtifacts` | Reference-only (manifest) |

**Score**:
- internal_weight: 0 (the file is itself the canonical RSPL lifecycle source — nothing inside `spec/rspl/` cites it because it IS the source)
- cross_cutting_weight: 4
- reference_only: 3

### Recommendation

**KEEP** in `spec/rspl/`.

The four cross-layer cites are dependency invocations of RSPL semantics, not evidence of cross-cutting concern. The file's opening declaration explicitly scopes its content: "baseline lifecycle states, allowed transitions, restore and supersession transitions, and conflict rules for registered RSPL resources." `control-plane-contracts.md` cites it because `TransitionLifecycleState` operates on RSPL resources; `bindings/http-json-binding.md` cites it to map RSPL operations; `security-and-policy-model.md` cites it for policy on RSPL state transitions; `baseline-conformance.md` cites it to mandate RSPL behavior support. Each citing file consumes RSPL semantics — that's correct dependency direction.

Moving the file to `spec/lifecycle/` would dis-anchor it from its semantic home and require updating every cross-layer citation's path without changing the underlying dependency relationship. No follow-up increment is recommended.

---

## Thread 2 — v1 Artifact-Set Verification

### Question

Does the actual repo state match what `spec/charter/agrp-v1-artifact-set.md` declares as the v1 artifact set?

### Method

The charter's enumeration scope was read in full and quoted verbatim before any classification. The declared artifact list was extracted (24 specific document paths). Actual repo state was inventoried across `spec/`, `models/schemas/`, `examples/conformance-vectors/`, `tools/`, `docs/decisions/`, `docs/reviews/`, `adopters/`, `planning/`. Each artifact (declared or present) was classified into one of six classes: match, drift / charter update needed, drift / artifact missing, renamed, out-of-scope-of-charter, scope-ambiguity-flag.

### Charter scope (verbatim)

From `spec/charter/agrp-v1-artifact-set.md`:

- **Lines 37-64 (Normative Artifact Set)**: enumerates 24 specific document paths from `spec/charter/repository-charter.md` through `spec/compliance/compliance-partial-failure-handling.md`.
- **Lines 82-89 (Non-Normative and Supporting Material)**: "The following repository material supports `AGRP v1` but is not itself part of the normative `v1` artifact set: files under `examples/`, analysis under `docs/`, machine-readable artifacts under `models/` unless a normative specification explicitly elevates a specific model artifact to authoritative status, adopter mappings under `adopters/`."
- **Lines 91-98 (Deferred and Future Areas)**: "Only the documents explicitly listed in this artifact-set document are part of the `v1` standard boundary. Directories or protocol areas with no included artifact-set entries are outside `AGRP v1` until a later normative release explicitly adds them."

The charter's exclusion of `examples/`, `docs/`, `models/`, and `adopters/` from the normative artifact set is explicit. `tools/` and `planning/` are not enumerated and fall under the line 91-98 "outside `v1` until explicitly added" rule.

### Findings — Gap table

The full audit produced 37 rows (24 declared, 13 present-but-undeclared classified by charter scope). Rows summarized by class:

| Class | Count | Notes |
|---|---|---|
| match | 24 | All declared artifacts present at declared paths |
| drift / charter update needed | **3** | See below |
| drift / artifact missing | 0 | |
| renamed | 0 | |
| out-of-scope-of-charter | 10 | Per the charter's explicit exclusions: `models/schemas/`, `examples/conformance-vectors/`, `tools/`, `docs/decisions/`, `docs/reviews/`, `adopters/`, `planning/`, `spec/charter/agrp-v1-artifact-set.md` (the charter file itself), `spec/charter/sepl-v1-deferral.md`, `spec/README.md` |
| scope-ambiguity-flag | 0 | Charter's enumeration scope is unambiguous |

**The three drift / charter-update-needed rows**:

| File | Layer | Why this is class 2 |
|---|---|---|
| `spec/deployment/deployment-topology-and-trust-boundaries.md` | deployment | In a `spec/<layer>/` directory; same artifact category as declared items; charter does not enumerate it |
| `spec/versioning/agrp-v1-release-definition.md` | versioning | Same category as declared `spec/versioning/versioning-and-evolution-policy.md`; charter does not enumerate it |
| `spec/compliance/evidence-freshness-and-attestation.md` | compliance | Same category as 6 declared `spec/compliance/*.md` files; charter does not enumerate it |

Each is a normative-category file in a directory whose other files ARE declared. The charter's line 91-98 rule explicitly says that presence in a normative directory does not auto-imply v1 inclusion — only explicit listing does. So these three files are presently **outside the v1 standard boundary** despite living alongside declared v1 artifacts.

### Recommendation

**Flagged for follow-up, judgment reserved.**

Each of the three drift rows could resolve in one of two directions:

- **(A) Amend the charter** to add the file to the declared artifact list, accepting it as a v1 normative document.
- **(B) Relocate or defer** the file outside the v1 boundary (move it under a v2-staging directory, or accept-with-note that the file is non-normative supporting material).

This audit deliberately does not pre-judge which direction applies for each file. That ruling requires per-file maintainer review of (i) whether the file's content is normative for v1 publication, and (ii) whether the charter's enumeration was deliberate or simply not updated when the file was added.

A **follow-up increment** is recommended to make those per-file rulings and execute whichever path applies. The follow-up's scope:

- Read each of the three files in full to determine its normative status.
- Per file, rule (A) amend or (B) relocate/defer.
- If (A) for any file: add the file to `spec/charter/agrp-v1-artifact-set.md`'s declared list (and to `docs/release-publication/agrp-v1.0.0-publication-manifest.example.json` if applicable).
- If (B) for any file: relocate the file or add a deferral note.
- Run the conformance harness as a regression check.

This audit makes no ruling in either direction.

---

## Thread 3 — SEPL Deferral Status

### Question

Does `spec/charter/sepl-v1-deferral.md` accurately reflect SEPL's current state in the corpus, and does anything need to be tracked for v2?

### Method

The deferral note was read in full; load-bearing claims were quoted verbatim. SEPL/self-evolution/evolution-loop/operator-phase references were inventoried across `spec/` and `docs/`. Each reference was classified into one of three classes: forward-reference to v2/SEPL still accurate (1), glossary-defined neutral term not load-bearing (2), or stale forward-reference (3).

### Deferral note's claims (verbatim)

From `spec/charter/sepl-v1-deferral.md`:

- Line 5: "This document defines the `AGRP v1` decision to defer self-evolution protocol standardization from the initial release boundary."
- Line 17: "the decision that `SEPL` is not part of `AGRP v1`"
- Line 19: "the requirement that future `SEPL` standardization be introduced through a later normative release boundary"
- Line 37: "`SEPL` is not part of `AGRP v1`."
- Lines 49-53: "Any future `SEPL` standardization must be introduced through a later normative release that: identifies the included `SEPL` artifacts explicitly; classifies compatibility impact using the protocol versioning rules; states whether `SEPL` is optional, additive, or release-boundary-defining for that later release"
- Line 55: "Until such a release exists, `SEPL` remains deferred from the protocol standard even if exploratory material appears in the repository."

The note makes explicit forward commitments: SEPL will be standardized through a future release boundary (not indefinitely deferred), and that introduction must follow versioning and artifact-set protocols.

### Findings — Reference inventory

20 references across 7 files. Classified:

| Class | Count | Representative examples |
|---|---|---|
| 1 — forward-reference to v2/SEPL (still accurate) | 14 | `spec/charter/repository-charter.md:131` ("`SEPL` remains a future protocol area until a later release explicitly adds it"); `spec/versioning/agrp-v1-release-definition.md:81` ("Any future release that introduces `SEPL` must do so explicitly and must classify the compatibility impact under the versioning rules"); `docs/papers/autogenesis-agp-decomposition.md` (non-normative analysis correctly identifying SEPL as future protocol layer) |
| 2 — glossary-defined neutral term (not load-bearing) | 6 | `Evolution Loop` glossary entry; `Operator Phase` glossary entry; `SEPL`/`closed-loop evolution`/`reflect/select/improve...` AGP/AGS mapping entries; `core-resource-model.md:22` scope-exclusion ("operator workflows for evaluation or self-evolution") |
| 3 — stale forward-reference | **0** | None found |

### Recommendation

**Deferral note remains accurate.**

The C2c watch-item ("distinguish neutral glossary/vocabulary persistence from real SEPL forward commitments") is satisfied by the classification: the 6 Class-2 references are vocabulary-persistence items, not promises about v2 protocol completeness. The deferral note's requirement that "future `SEPL` standardization be introduced through a later normative release boundary" does not prevent vocabulary work today; the glossary entries for `Evolution Loop` and `Operator Phase` exist precisely so future SEPL specs have neutral terminology to use.

The 14 Class-1 references all consistently align with the deferral: SEPL is deferred from v1, future standardization must follow explicit release-boundary rules, and exploratory material in the repository is not equivalent to inclusion in the standard.

No update to `sepl-v1-deferral.md` is warranted. No `next-version-tracking.md` is needed at this time — the autogenesis decomposition paper already documents what SEPL work should pick up (operator contracts, trace model, extension rules), and the deferral note's forward-commitment language correctly reserves that work for a future increment.

---

## Cross-thread observations

The three threads run independently but produce a coherent overall picture:

- **Thread 1's KEEP verdict and Thread 2's drift findings do not collide.** The lifecycle file (Thread 1) is row #6 of Thread 2's declared-artifact list — it's a match, not a drift. The two threads make compatible claims about the v1 corpus.
- **Thread 2's three drift rows are isolated to a single follow-up increment.** None of the three files are referenced by Thread 1's evidence (no cross-cutting cite goes to `deployment/`, `versioning/`, or `compliance/evidence-freshness-and-attestation.md`). Whatever direction the follow-up rules per file, it doesn't perturb Thread 1's verdict.
- **Thread 3's deferral-accuracy verdict is independent of both other threads.** None of Thread 2's three drift files are SEPL-flavored; none of Thread 1's cross-cutting cites engage SEPL vocabulary. The three threads produce three orthogonal verdicts.
- **The charter is the single artifact most actively cited across threads.** Thread 1 cites it as a reference-only manifest entry; Thread 2 audits it as the source of truth for the artifact set; Thread 3 cites it for the SEPL forward commitments at line 131. None of the citations contradict each other; the charter's content is internally consistent.

---

## Release-readiness verdict

**Overall: ready-with-known-deferrals.**

The v1 corpus is substantively ready for publication. The audit surfaces exactly **one follow-up candidate**:

> **Charter/spec inventory reconciliation** — a follow-up increment to make per-file rulings on `spec/deployment/deployment-topology-and-trust-boundaries.md`, `spec/versioning/agrp-v1-release-definition.md`, and `spec/compliance/evidence-freshness-and-attestation.md`. Each file resolves either by charter amendment (adding the file to the declared artifact list) or by relocation/deferral (moving it outside the v1 boundary). This audit reserves judgment on which direction applies per file.

No other follow-up is recommended. Threads 1 and 3 produce verdicts requiring no action.

If the maintainer wants the charter/spec boundary fully reconciled before publication, the next path is:

1. Open the follow-up increment for charter/spec inventory reconciliation.
2. Make per-file (A/B) rulings.
3. Execute the chosen path for each file (charter amendment or relocation/deferral).
4. Once the three rows are resolved, v1 is publication-ready.

This audit's role ends here. Any subsequent increments are out-of-scope for the audit's discipline gate.
