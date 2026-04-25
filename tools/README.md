# tools/

Non-normative tooling supporting the AGRP protocol corpus. Scripts here validate or assist work against the normative artifacts in `spec/`, `models/`, and `examples/` but are not themselves part of the protocol definition.

## Layout

- `tools/conformance/` — conformance vector validation harness (Python 3, no dependencies).

## Adding new tooling

New tools belong here when they (a) operate on the AGRP corpus rather than instantiating it, (b) require no protocol-level normative status, and (c) are useful to adopters cloning the repo. Anything that takes external dependencies, runs in CI only, or is implementation-specific should live with the implementation rather than under `tools/`.
