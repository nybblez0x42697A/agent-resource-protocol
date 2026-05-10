# SEPL Next-Opening Sequencing Decision

This document records, per `SEPL` concern, whether the post-0056
evidence base is sufficient to route the slice through a
release-boundary increment that mirrors the `SEPL-08` opening
shape established by 0053. It does not open any `SEPL` slice;
actual openings would travel through separate release-boundary
increments shaped on the precedent codified in
`spec/sepl/operator-extension-model.md`. It complements
`docs/audits/sepl-opening-decision.md`, whose §1 hybrid closure
of the 0052 audit (executed by 0053 / 0054 / 0055 and refreshed
by 0056) is unchanged here.

A terminology note: matrix rows in
`docs/audits/sepl-coverage-matrix.md` use a four-term
**disposition** vocabulary; `sepl-opening-decision.md` §1 uses a
three-term **closure-state** vocabulary; this document uses a
three-term **sequencing-assessment** vocabulary
(`ready` / `not-yet-ready` / `stay-in-sharpened-defer`). The
sequencing vocabulary describes per-concern readiness for a
release-boundary increment; it does not replace the prior two,
which continue to govern matrix rows and the whole-audit closure
state respectively.

## 1. Decision

No `SEPL` slice is ready for release-boundary opening on the
basis of the post-0056 evidence base.

Of the seven concerns remaining after `SEPL-08` opened: three
(`SEPL-01`, `SEPL-04`, `SEPL-07`) are `not-yet-ready` — Helios
surfaces direct evidence but each rests on a single synthetic
witness whose carrier choice is one of several valid shapes per
the Helios design-doc §9 implementation-defined edges. Four
(`SEPL-02`, `SEPL-03`, `SEPL-05`, `SEPL-06`) remain in the
sharpened-defer state codified by
`spec/charter/sepl-v1-deferral.md:57-66`; no post-0054 evidence
warrants posture change. The 0052 hybrid closure at
`docs/audits/sepl-opening-decision.md` §1 is unchanged.

## 2. Rationale

The `not-yet-ready` ruling rests on two grounds, both surfaced
in the Helios design-doc itself.

**Single-synthetic-witness ground.** Helios is one synthetic
governance-registry adaptation: per
`docs/adaptations/helios-governance-registry.md` §11 it
exercises a single policy revision, a single lifecycle
transition, and no multi-revision or supersession or
rejection-then-archive flows. The `SEPL-08` opening rested on
three direct-evidence witnesses (Northstar, Pinecrest, Helios
slot 15). For `SEPL-01`, `SEPL-04`, and `SEPL-07`, only Helios
surfaces direct evidence.

**Carrier-shape ground.** Helios design-doc §9 explicitly labels
its carrier choices as implementation-defined edges: the
`SEPL-01` URN convention on `actor`, the `SEPL-04` proposer-scope
tuple dimensionality, and the `SEPL-07` redaction-marker shape
are each "one expressible carrier among several." A
release-boundary opening following the `SEPL-08` precedent would
name a specific carrier as the included `v1` artifact; for
`SEPL-01`, `SEPL-04`, and `SEPL-07` the path to that opening
would benefit from either a second-domain witness exercising the
same shape via a different carrier or a normative carrier-shape
decision authored on a different basis.

The `stay-in-sharpened-defer` ruling for `SEPL-02`, `SEPL-03`,
`SEPL-05`, and `SEPL-06` rests on a simpler ground: the 0054
charter sharpening at `spec/charter/sepl-v1-deferral.md:57-66`
already states the deferral surface for each concern, and Helios
deliberately does not exercise any of them per design-doc §11.

## 3. Per-SEPL sequencing assessments

Evidence anchors below follow the C5-permitted types: Helios
bundle paths under `examples/adaptations/helios-governance-registry/`;
sections of `docs/adaptations/helios-governance-registry.md`;
`spec/charter/sepl-v1-deferral.md:57-66`; rows in
`docs/audits/sepl-coverage-matrix.md`. Rationales rest on the
grounds established in §2; per-concern entries identify the
specific carrier or §11 gap rather than restating the grounds.

### 3.1 `SEPL-01` — Candidate-change proposal envelope

Assessment: `not-yet-ready`. Anchor: Helios slots 01 / 02 / 03 /
04 / 06 / 09 / 11 / 14 (§11 "SEPL surfaces exercised here") plus
§9 "The `<org>:<role>:<id>` URN convention for `actor`
identifiers." Single synthetic carrier; §9 calls the URN-encoded
proposer-vs-registrar role split "one expressible carrier among
several." Path to opening would benefit from a second-domain
witness or a normative carrier-shape decision.

### 3.2 `SEPL-02` — Evaluation criterion declaration

Assessment: `stay-in-sharpened-defer`. Anchor: charter `:57-66`
plus §11 "SEPL surfaces deliberately not covered." Helios
attaches criterion *references* (slot 03's
`metadata.evaluationCriteriaRefs[]`; slot 06's
criterion-attestation) but per §11 "does not declare the
criterion *taxonomy*." 0054 sharpening posture unchanged.

### 3.3 `SEPL-03` — Commit semantics with rollback provenance

Assessment: `stay-in-sharpened-defer`. Anchor: charter `:57-66`
plus §11. Helios's commit audit-record names the steward
(slot 09) but per §11 "does not exercise the role distinction
between a *proposing* operator and a *steward / approver*
operator at the schema level"; rollback provenance is not
exercised either. 0054 sharpening posture unchanged.

### 3.4 `SEPL-04` — Operator-contract preconditions and failure modes

Assessment: `not-yet-ready`. Anchor: Helios slots 16 and 18
(§11) plus §9 "The `subjectArea` / `severityTier` /
`jurisdiction` field tuple." Single synthetic three-dimension
carrier; §9 records "other registries may carry one dimension or
four and still surface SEPL-04 evidence." Path to opening would
benefit from a second-domain witness or a normative
carrier-shape decision.

### 3.5 `SEPL-05` — Approval / policy gate

Assessment: `stay-in-sharpened-defer`. Anchor: charter `:57-66`
plus §11. Helios models the steward decision as a single
`audit-record` (slot 09) but per §11 "does not model a per-change
approval gate as a separate registry transaction." 0054
sharpening posture unchanged.

### 3.6 `SEPL-06` — Trace granularity and retention

Assessment: `stay-in-sharpened-defer`. Anchor: charter `:57-66`
plus §11. Helios includes per-stage records but per §11 "does
not exercise SEPL evidence retention policy (per-proposal vs
per-evaluation granularity; freshness-window semantics;
retention-policy declarations)." 0054 sharpening posture
unchanged.

### 3.7 `SEPL-07` — Privacy / redaction boundaries for self-evolution traces

Assessment: `not-yet-ready`. Anchor: Helios slots 07 / 08 / 09 /
17 (§11) plus §9 "The `metadata.redacted` and
`metadata.redactionPolicyRef` extension fields," "The
redaction-aware decision rationale," and "The absence of real
cryptographic redaction." Single synthetic structural-only
carrier; §9 records both that other implementations may use
different redaction shapes (for example, a `<security:>`
JSON-pointer namespace or detached metadata) and that "real
registries handling sensitive policy content would layer a real
redaction algorithm ... below this shape." Path to opening would
benefit from a second-domain witness, a normative carrier-shape
decision, and a separate decision on the
structural-vs-cryptographic boundary.

## 4. Relationship to existing audit closure decisions

The 0052 hybrid closure at
`docs/audits/sepl-opening-decision.md` §1 is unchanged: SEPL-08
opened (executed by 0053); the four `narrow-and-defer` concerns
continue under sharpened framing (executed by 0054); the three
`needs-targeted-adaptation` concerns continue deferred under the
`Future Introduction Rule`. The 0056 audit-layer refresh
addenda (matrix `## Post-opening evidence refresh`; scope-audit
`## 10.`; opening-decision `## 4.`) are the primary input to
this sequencing assessment; this document extends the rationale
base without redefining terms or revising prior disposition or
verdict values.
