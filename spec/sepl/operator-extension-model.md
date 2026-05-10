# Operator Extension Model

## Status

This file is normative for `AGRP v1`. It is the `SEPL-08 v1` opening artifact, named explicitly under the release-boundary gate at the `spec/charter/sepl-v1-deferral.md` section titled `SEPL-08 Operator Extension Model Opened Via Release Boundary`. That charter section discharges the `Future Introduction Rule` for `SEPL-08`; this file codifies the corresponding declaration shape.

This file's normative authority is bounded by the `Scope` section below.

## Scope

This file is normative for the operator-extension declaration shape only.

It is not normative for:

- any `SEPL` operator-kind taxonomy
- any `SEPL` evaluation, proposal, review, or commit semantics
- any `SEPL` concern other than operator extensions

The deferral framework at `spec/charter/sepl-v1-deferral.md` continues to govern the concerns listed above; this file does not alter their disposition.

## Operator extension declaration

An operator extension is declared by a string entry in the `extensions` array of a `capability-advertisement` document.

The carrier field is `models/schemas/capability-advertisement.schema.json#/extensions`, declared at line 22 as a `stringArray` and listed in the schema's required array at line 55. The carrier-field shape is unchanged by this opening.

Each entry takes the namespaced, versioned identifier shape `<org>:extension:<name>:vN`, where:

- `<org>` is a producer-chosen organization namespace
- `<name>` is a producer-chosen extension name
- `vN` is a producer-chosen integer version suffix (`v1`, `v2`, ...)

This shape is the normative `SEPL-08 v1` operator-extension declaration shape. No other identifier shape is normative under `SEPL-08 v1`.

## Conformance posture

This opening is classified `additive` per `spec/versioning/versioning-and-evolution-policy.md:121, :131-139`.

This classification is NOT `release-boundary-defining`. No prior `AGRP v1` conformance claim is invalidated.

Implementations that emit no `extensions` field content, an empty `extensions: []` array, or any prior namespaced extension identifier are unchanged by this opening and remain `AGRP v1` conformant.

## Direct evidence

The following corpus artifacts exhibit the operator-extension declaration shape and conform to the `<org>:extension:<name>:vN` identifier convention:

- `examples/adaptations/northstar-tool-registry/14-capability-advertisement.example.json#/extensions`
- `examples/adaptations/pinecrest-data-products/14-capability-advertisement.example.json#/extensions`
- `examples/adaptations/helios-governance-registry/15-capability-advertisement.example.json#/extensions`

The carrier-field shape is fixed by `models/schemas/capability-advertisement.schema.json:22, :55`.
