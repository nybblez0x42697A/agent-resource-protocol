# tools/conformance/

Conformance vector validation harness for AGRP.

## Usage

From the repository root:

```sh
python3 tools/conformance/run_conformance_vectors.py
```

## What it does

The harness walks `examples/conformance-vectors/` in sorted order and validates each fixture against its declared `targetSchema` (relative to repo root). For each vector it:

1. Loads the fixture JSON and resolves `targetSchema` to a schema under `models/schemas/`.
2. Validates `payload` against the schema using a hand-rolled Draft 2020-12 validator (subset: `$ref`, `oneOf`, `const`, `enum`, `type`, `minLength`, `required`, `properties`, `additionalProperties`, `items`, `allOf`, `if` / `then` / `else`).
3. Compares the observed outcome against `expected.outcome`. For payloads that themselves carry an `error` envelope (e.g., `conflict-error.valid.json`), it also confirms the payload's `error.category` maps to the expected `failureClass` via the baseline mapping.

## Output

One line per vector — `ok <fixtureId>` for each successful validation. The harness exits non-zero on the first mismatch with a `SystemExit` message naming the fixture and the discrepancy.

Expected behavior for the current 19-vector set: all 19 emit `ok <fixtureId>`, exit code 0.

## Conventions

- `*.valid.json` fixtures must validate against their `targetSchema`.
- `*.<reason>.invalid.json` fixtures must fail validation; the `<reason>` slug in the filename is informational.
- Vectors carrying an `error` envelope (e.g., `conflict-error.valid.json`) declare `errorCategory` in `expected` so the harness can confirm category-to-failure-class mapping consistency.

## Dependencies

None. Uses only the Python 3 standard library (`json`, `pathlib`).

## Scope

This harness is a deliberate Draft 2020-12 subset — it implements only the validation features actually used by the AGRP schemas. If a future schema relies on `dependentRequired`, `dependentSchemas`, `not`, `patternProperties`, or `anyOf`, the harness will need to be extended (see the in-source comment near the conditional-support block).

## Related

- Fixtures: `examples/conformance-vectors/`
- Schemas: `models/schemas/`
