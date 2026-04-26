# Decisions

Architecture decision records for the Agent Resource Protocol (AGRP).

This directory holds protocol-architecture decisions readable by adopters: choices about
schema shape, conformance scope, prose canon, deployment topology, and other surfaces that
implementers depend on. Each ADR captures the context that prompted a decision, what was
chosen, the alternatives that were rejected, and the consequences observed after the
decision shipped.

## Format

ADRs follow the Nygard four-section structure:

1. **Status** — `Proposed`, `Accepted`, `Superseded by 00NN`, or `Deprecated`. ADRs are
   generally treated as immutable once `Accepted`; supersession adds a new ADR rather than
   rewriting history.
2. **Context** — the situation when the decision was made, written in past tense from
   the decision moment. Cite verifiable source records (plan.md sections, log files,
   commits) so future readers can trace the original argument.
3. **Decision** — what was chosen, plus the alternatives considered and why each was
   rejected. Stay anchored to decision-time rationale; later justifications belong in
   Consequences.
4. **Consequences** — what changed because of the decision: positive outcomes, negative
   trade-offs, and any post-hoc observations. This is the only section where post-shipping
   analysis belongs.

## Naming

`XXXX-decision-title.md`

- Four-digit zero-padded prefix (`0001`, `0002`, ...).
- Hyphen-separated lowercase title.
- No `adr-` or `ADR-` prefix.
- `_template.md` (leading underscore, not numbered) is the scaffold for new ADRs.

This convention is adopted verbatim from `.specweave/docs/internal/architecture/adr/README.md`,
the SpecWeave-internal ADR location, so that both ADR directories share identical
filename rules.

## Authoring a new ADR

1. Copy `_template.md` to the next available number.
2. Fill in each section against the source records you can cite. If a clause cannot be
   traced to a source, move it to Consequences or drop it — ADRs are decision archaeology,
   not retroactive marketing.
3. Cross-reference the affected artifact paths and any relevant commit hashes so the
   decision remains locatable as the corpus evolves.

## Scope split with `.specweave/`

Two ADR locations exist in this repository, with a deliberate divide:

- **`docs/decisions/`** (this directory) — protocol-architecture decisions adopters need
  to read: schema shape, conformance harness scope, prose canon, deployment trust
  boundaries, etc.
- **`.specweave/docs/internal/architecture/adr/`** — SpecWeave/process decisions about how
  this repository organizes its own work: increment lifecycle, planning conventions,
  internal tooling. That directory is gitignored and carries no normative weight outside
  the SpecWeave workflow.

If a decision materially affects AGRP implementers, it lives here.
