# 0003. Conformance Harness Extended for Draft 2020-12 Conditional Keywords

## Status

`Accepted`

Decided: 2026-04-23 by the AGRP maintainer during increment 0041 closure as a narrow,
explicitly-approved exception to a stated non-goal.

## Context

Increment 0041 listed "No changes to the Python conformance harness" as an explicit
non-goal. The harness at the time lived at
`.specweave/increments/0032-conformance-vectors-and-negative-cases/scripts/run_conformance_vectors.py`
and implemented a deliberate Draft 2020-12 subset: `$ref`, `oneOf`, `const`, `enum`,
`type`, `minLength`, `required`, `properties`, `additionalProperties`, and `items`. It
did not implement `allOf`, `if`, `then`, or `else`.

While authoring WS7 conformance vectors, the 11th vector
`profile-declaration.replaced-missing-supersedes.invalid.json` was added to demonstrate
the new schema conditional landed in WS1 / C2 (recorded separately in ADR 0002). The
vector was expected to fail validation. It silently passed.

The cause: the schema conditional was a branch-local `allOf` + `if`/`then` block, and
the harness ignored those keywords entirely. The conditional was therefore enforced by
any compliant Draft 2020-12 validator — confirmed independently via `jsonschema` during
C2 — but was invisible to this repository's own regression suite.

Leaving the harness unchanged would have given the repo false confidence for any current
or future `allOf` / `if`/`then` constraints — exactly the kind of drift risk increment
0041 existed to eliminate. The user was surfaced this finding and approved a narrow
exception to the non-goal.

## Decision

The harness's `validate()` function was extended with minimal `allOf` and
`if`/`then`/`else` support — approximately fifteen lines, inserted between the existing
`minLength` check and the `isinstance(data, dict)` branch:

- `allOf`: iterate sub-schemas and validate against each; any failure propagates.
- `if` / `then` / `else`: validate against `if`; on pass select `then`, on fail select
  `else`; validate against the selected branch if present.

No other harness behavior was modified. No refactor. The sibling keywords already
implemented (`required`, `properties`, `additionalProperties`, `enum`, `const`, `type`,
`minLength`, `$ref`, `oneOf`, `items`) were untouched.

The exception was framed as narrow because the alternative was a silent
regression-coverage hole that would have undermined 0041's "fix the drift" intent.

## Consequences

The harness now matches a compliant Draft 2020-12 validator for every keyword the AGRP
schemas actually use. The 11th vector
`profile-declaration.replaced-missing-supersedes.invalid.json` now correctly fails
validation as its filename claims; the harness rerun after the patch reported `19/19
vectors passed as labeled (exit=0)`.

The harness remains a deliberate Draft 2020-12 subset rather than a full implementation.
If future schemas use `dependentRequired`, `dependentSchemas`, `not`, `patternProperties`,
or `anyOf`, the harness will need further extension. The "Scope" section of
`tools/conformance/README.md` documents this limitation explicitly so future authors
know to extend the validator before introducing schemas that rely on these keywords.

This decision created a small precedent: stated non-goals can be revisited mid-flight
when a verification-coverage gap is discovered, provided the user is surfaced the
finding and explicitly approves a scoped exception. Future increments that encounter
similar gaps should follow the same surface-and-approve pattern rather than treating
the non-goal as inviolable or as a silent license to skip the verification.

After increment 0041 closed, increment 0043 relocated the harness from the gitignored
`.specweave/increments/0032-.../scripts/` path to the tracked
`tools/conformance/run_conformance_vectors.py` path so adopters cloning the repo could
run validation. The conditional-support extension moved with the file; both the original
`.specweave/` snapshot and the tracked tooling location now contain the same `allOf` +
`if`/`then`/`else` implementation. The relocation is unrelated to this ADR's scope but
explains why later readers will find the extension at `tools/conformance/...` rather
than at the original `.specweave/...` path named in 0041's records.

**Alternatives considered in closure conversation but not formally recorded in the
contemporaneous plan/log:**

- **Leave the harness unchanged and remove the regression vector**: would have undone
  the regression coverage that the WS1 / C2 schema conditional required to be testable
  in-repo, defeating the increment's quality-floor goal.
- **Replace the hand-rolled harness with a `jsonschema` library dependency**: would
  have had a much larger blast radius and would have introduced an external Python
  dependency that the repo otherwise has none of.

These options surfaced during the surface-and-approve exchange but were not enumerated
in `harness-extension-note.md` or in plan.md. They are recorded here for future readers
without overstating their documentary status.

## References

- Source records:
  `.specweave/increments/0041-agrp-spec-drift-remediation/logs/harness-extension-note.md`
- Affected artifacts: `tools/conformance/run_conformance_vectors.py:91-105` (post-0043
  relocation; same code originally added to
  `.specweave/increments/0032-conformance-vectors-and-negative-cases/scripts/run_conformance_vectors.py`
  in 0041);
  `examples/conformance-vectors/profile-declaration.replaced-missing-supersedes.invalid.json`
  (the vector whose silent pass triggered the discovery)
- Commits: `7f34a71` (0041 closure, original extension); `83a7980` (0043 closure, harness
  relocation)
- Related ADRs: 0002 (the schema conditional whose enforcement required this harness
  extension)
