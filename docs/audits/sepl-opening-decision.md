# SEPL Opening Decision

This document is the load-bearing closure artifact of the 0052 SEPL scope audit. It is short and quotable by design: downstream release-planning increments and follow-up adaptation increments cite this document directly. The longer reasoning lives in `docs/audits/sepl-scope-audit.md` (audit narrative) and the row-level evidence in `docs/audits/sepl-coverage-matrix.md` (coverage matrix).

A terminology note that this document and the audit narrative both honor on first use: matrix rows in `docs/audits/sepl-coverage-matrix.md` use a four-term **disposition** vocabulary (`sharpen-defer`, `open-via-release-boundary`, `needs-targeted-adaptation`, `narrow-and-defer`) describing what should happen with that single concern. This decision document §1 below uses a three-term **closure-state** vocabulary (`sharpened-defer`, `open-via-release-boundary`, `hybrid`) summarizing the dispositional shape across all eight concerns. Per-row dispositions vary across the inventory; the whole-audit closure state describes the overall posture.

## 1. Decision

The audit closes with the closure state **`hybrid`**.

Concrete meaning: SEPL-08 (operator extension model) opens via a downstream release-boundary increment that honors `spec/charter/sepl-v1-deferral.md:49-55`. SEPL-02, SEPL-03, SEPL-05, and SEPL-06 stay deferred under the existing `sepl-v1-deferral.md` framework, with audit-anchored sharpening text added by a charter-amendment increment. SEPL-01, SEPL-04, and SEPL-07 stay deferred pending a targeted third reference adaptation that surfaces existing-protocol evidence for those concerns; a follow-up audit re-runs the matrix once that adaptation ships.

## 2. Rationale

The hybrid decision is anchored to `docs/audits/sepl-scope-audit.md` §8, which records three reasons grounded in specific coverage-matrix rows. The summary is reproduced here so the decision is self-quotable:

- **SEPL-08 (operator extension model)** is the matrix's only `direct-evidenced` row. Both adaptations advertise extension lists at `#/extensions` on their capability-advertisement artifacts with namespaced, semantically-versioned identifiers — a pattern concrete enough to specify in normative SEPL form. Treating SEPL-08 as `open-via-release-boundary` honors that evidence; folding it into a wholesale `sharpened-defer` would set the evidence aside without using it.

- **SEPL-02 (evaluation criterion declaration), SEPL-03 (commit semantics with rollback provenance), SEPL-05 (approval / policy gate), and SEPL-06 (trace granularity and retention)** each carry `adjacent-evidenced` verdicts and `narrow-and-defer` dispositions in the matrix. Their evidence — refresh-SLA policy reference, audit-record `#/evidenceRefs` provenance, profile-declaration `#/forbiddenBehaviors` policy expression, freshness-window retention pattern — is real and reusable, but each row's broader load-bearing surface is too wide to open as a single slice. Sharpened-defer with charter amendment names what is currently deferred and why, anchored to those evidence cells.

- **SEPL-01 (candidate-change proposal envelope), SEPL-04 (operator-contract preconditions and failure modes), and SEPL-07 (privacy / redaction boundaries for self-evolution traces)** each carry `needs-targeted-adaptation` dispositions. Their adjacent evidence is too far from the SEPL-specific load-bearing surface to narrow without further adaptation. A third reference adaptation would generate the missing evidence; opening these rows without that evidence would be premature.

The release-boundary gate at `spec/charter/sepl-v1-deferral.md:49-55` is honored under hybrid: the SEPL-08 slice travels through a downstream release-planning increment that names artifacts, classifies compatibility, and declares posture; the four `narrow-and-defer` rows stay under the existing deferral framework with audit-backed sharpening; the three `needs-targeted-adaptation` rows get a targeted-adaptation route rather than a premature opening.

## 3. Follow-up increment slate

Three coordinated follow-up increments fall out of the hybrid decision. The slug list below is identical (by strict equality) to `docs/audits/sepl-scope-audit.md` §9 — the audit narrative may add context around each slug, but the named slug set is the same in both locations.

- **`0053-agrp-sepl-operator-extension-release-boundary-decision`** — Release-planning increment that opens the SEPL-08 (operator extension model) slice via the release-boundary path defined at `spec/charter/sepl-v1-deferral.md:49-55`.

- **`0054-agrp-sepl-deferral-charter-sharpening`** — Charter-amendment increment that updates `spec/charter/sepl-v1-deferral.md` with audit-anchored sharpening text naming the four `narrow-and-defer` concerns (SEPL-02, SEPL-03, SEPL-05, SEPL-06) explicitly.

- **`0055-agrp-sepl-targeted-adaptation-third-domain`** — Targeted third reference adaptation against a self-evolution-shaped synthetic domain, designed to evidence SEPL-01, SEPL-04, and SEPL-07 before any release-boundary work on those rows.

Slug numbers are placeholders and may shift if other increments are scheduled before them; any future renumbering propagates to both this document and `docs/audits/sepl-scope-audit.md` §9 together.
