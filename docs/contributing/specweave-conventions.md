# SpecWeave Conventions

## Purpose

This file documents repository-local conventions for using SpecWeave on the
Agent Resource Protocol (AGRP) codebase. It is non-normative — it describes
process, not protocol — and exists for contributors who run the
`/sw:increment`, `/sw:do`, and `/sw:done` skills against this repo. Nothing
here changes what AGRP says.

## Increment Slug Naming

SpecWeave's `specweave complete <id>` command validates the increment slug
against the regex `^[0-9]{4}E?-[a-z0-9-]+$` before doing any other work. A
slug that does not match this pattern is rejected with the error message
`Invalid increment ID format`, and closure cannot proceed via the CLI.

The practical implication is that increment slugs in this repository must
contain only lowercase letters, digits, and hyphens after the four-digit
prefix. Dots are the most common way to violate the pattern, especially when
the increment title includes a SemVer string.

Correct form for future increments:

    0049-agrp-v1-0-0-publication
    0050-agrp-v1-0-0-post-publication-hygiene

Incorrect form (rejected by the validator):

    0049-agrp-v1.0.0-publication
    0050-agrp-v1.0.0-post-publication-hygiene

The canonical incident is increment 0049, which was scaffolded with a
dotted slug and could not be closed via the CLI even though the substantive
release work (commits, tag, push) was complete. Increment 0047 hit the same
failure mode earlier in the program.

When a SemVer-style identifier needs to appear in a slug, replace dots with
hyphens (`v1.0.0` becomes `v1-0-0`). Public artifacts that need the dotted
form (CHANGELOG entries, manifest fields, announcement text) are unaffected
— those live inside file contents, not in the increment slug.

## Substantive Closure Under Option A

When the slug validator blocks `specweave complete` on a legacy dotted
slug, the increment may still be substantively closed. The convention is
**Option A**: leave `metadata.json` at `"status": "planned"`, accept that
the SpecWeave bookkeeping cannot transition, and treat the substantive
work (commits on `origin/main`, tag pushed, all release artifacts public,
quality gates green) as the actual closure.

The maintainer's reasoning at 0049 was: the public release is the
deliverable; the metadata transition is bookkeeping. A renamed local
folder would create provenance skew with already-pushed public artifacts
that cite the original slug. A direct `metadata.json` edit would bypass
the post-closure hooks. Option A keeps the public state clean and
documents the limitation honestly.

Two evidence files record the precedents in detail. Both follow the same
structure (attempted commands, root cause, substantive state, ruling):

- `.specweave/increments/0047-agrp-northstar-tool-registry-reference-adaptation/reports/closure-cli-blocker.txt`
- `.specweave/increments/0049-agrp-v1.0.0-publication/reports/closure-cli-blocker.txt`

Future contributors who hit a closure-time CLI failure on a dot-free slug
should add a new closure-blocker report under their increment's
`reports/` folder rather than working around the issue silently.

## Manual-Approve Checkpoint Discipline

The 0041–0050 program has been executed in `mode: manual-approve`
(0050 still in flight at the time of writing). The pattern is: each
`/sw:do` task that
materially changes the working tree (or commits, pushes, or tags) is a
checkpoint. The agent runs the task to a clean stopping point, captures
evidence to `.specweave/increments/<id>/reports/<checkpoint>.txt`, and
STOPs explicitly. The maintainer reviews evidence and either approves
the next checkpoint or rules an Option B / amendment / rollback.

Every increment under this discipline keeps the same `reports/`
structure. Typical files include:

    reports/c1-baseline.txt          # kickoff and pre-work conformance
    reports/c2-decisions.txt         # locked maintainer rulings
    reports/c3-*.txt                 # design / draft approvals
    reports/c4-staging.txt           # explicit-path staging audit
    reports/c4-commit.txt            # HEREDOC commit + SHA
    reports/discipline-gate.txt      # post-commit C2-lock equality check
    reports/closure-cli-blocker.txt  # only if closure hit Option A

The discipline relies on three rules: (1) deferred-to-staging — drafts
live in `reports/` and only move to their final tracked path at the
materialization step; (2) explicit-path staging — never `git add -A`,
`git add .`, or `git add <directory>/`; (3) HEREDOC commit messages
without a `Co-Authored-By` trailer.

When in doubt, mirror the report layout in
`.specweave/increments/0049-agrp-v1.0.0-publication/reports/` — that
increment carries the most thorough evidence trail of any closed
program in the repo.
