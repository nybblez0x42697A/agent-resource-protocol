# 0002. profile-declaration replaced => supersedes Conditional Uses Branch-Local allOf+if/then

## Status

`Accepted`

Decided: 2026-04-23 by the AGRP maintainer during increment 0041 checkpoint C2.

## Context

The schema at `models/schemas/profile-declaration.schema.json` is a top-level `oneOf`
over three branches: `supportedDeclaration`, `standardDeclaration`, and
`adoptingDeclaration`. Each branch has `status` with an enum including `"replaced"`, and
each branch declares `supersedes` as an optional property.

The prose rule at
`spec/compliance/profile-declaration-and-discovery-interoperability.md:215` required
`supersedes` (or equivalent target identification) when `status: "replaced"`, but no
schema enforced this. Adopters relying on schema validation alone would silently accept
declarations that prose forbids: a profile declaration could announce itself as replaced
without naming what replaced it, and the validator would not catch the gap.

## Decision

Branch-local `allOf` + `if`/`then` blocks were added to each of the three
`$defs/*Declaration` sub-schemas, as a sibling to the existing `required` array. The
exact shape is:

```json
"allOf": [
  {
    "if": {
      "properties": { "status": { "const": "replaced" } },
      "required": ["status"]
    },
    "then": {
      "required": ["supersedes"]
    }
  }
]
```

The `required: ["status"]` inside the `if` is the idiomatic guard against JSON Schema's
vacuous-truth behavior: an `if` block with `properties` alone evaluates true when the
property is absent (because `properties` does not require existence). Including
`required: ["status"]` inside the `if` ensures the conditional only fires when `status`
is present with value `"replaced"`. Each branch already has `status` in its outer
`required` array, so this inner requirement is defensive redundancy — but it is the
idiomatic pattern and future-proofs the conditional if the branch `required` sets are
ever relaxed.

The argument made at decision time, recorded in 0041 plan.md §1.4, considered three
options:

- **Option (a) — Lift `supersedes` into each branch's unconditional `required`**:
  rejected because `supersedes` is not required when `status` is `active` or
  `deprecated`; making it universally required would invalidate the existing
  `profile-declaration.valid.json` vector (which is `status: active` with a `supersedes`
  field voluntarily provided).
- **Option (b) — Branch-local `allOf` + `if`/`then`**: selected. Works with Draft
  2020-12 (which the schemas already target per `$schema`). Scopes the conditional to
  each branch so the error surface is precise, and composes cleanly inside an `oneOf`
  because `if` has no effect when its branch is not selected.
- **Option (c) — `dependentRequired: { status: ... }`**: rejected because
  `dependentRequired` takes an array of property names to require when a *property is
  present*, not when it has a specific *value*. It cannot express "required only when
  `status` equals `replaced`".

## Consequences

The schema now enforces what prose required. The conditional was added to all three
branch sub-schemas in `models/schemas/profile-declaration.schema.json` and is invariant
across them — every declaration shape rejects `status: "replaced"` without `supersedes`.

The C2 checkpoint included a regression run against the 8 pre-existing conformance
vectors; all still passed (AC-US2-03 satisfied). The strictest case
(`supportedDeclaration` with `status: "replaced"` and no `supersedes`) was confirmed
correctly rejected via independent `jsonschema 4.25.1` validation across six targeted
inputs covering all three branches and both the conformant and conflict directions.

A regression-guard fixture
`examples/conformance-vectors/profile-declaration.replaced-missing-supersedes.invalid.json`
was added during 0041 WS7 (originally noted in plan.md §1.4 as an optional vector;
landed as a regular invalid vector because AC-US2-01 required demonstrable enforcement).
The presence of this vector in the harness suite ensures any future schema edit that
weakens the conditional surfaces immediately.

The conditional choice has a downstream effect on the conformance harness: the in-repo
hand-rolled validator at the time of decision did not implement `allOf` or `if`/`then`,
which made the new vector silently pass under the existing harness. That gap is recorded
separately in ADR 0003.

## References

- Source records: `.specweave/increments/0041-agrp-spec-drift-remediation/plan.md` §1.4
- Affected artifacts:
  `models/schemas/profile-declaration.schema.json:70-80, 144-154, 221-231` (the three
  branch-local `allOf` blocks);
  `examples/conformance-vectors/profile-declaration.replaced-missing-supersedes.invalid.json`
  (regression-guard vector)
- Commits: `7f34a71` (0041 closure)
- Related ADRs: 0003 (harness extension required to enforce this conditional in the
  in-repo regression suite)
