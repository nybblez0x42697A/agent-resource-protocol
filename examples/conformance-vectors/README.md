# Conformance Vectors

These fixtures are non-normative test inputs for `AGRP v1` validation work.

Each vector contains:

- `fixtureId`
- `targetSchema`
- `expected`
- `payload`

The expected outcome is either:

- `pass`
- `fail`

Negative vectors may also record the expected baseline `failureClass` and `errorCategory`.

## Validating these fixtures

The conformance harness lives at `tools/conformance/run_conformance_vectors.py`. From the repository root:

```sh
python3 tools/conformance/run_conformance_vectors.py
```

See `tools/conformance/README.md` for full usage details and harness scope.
