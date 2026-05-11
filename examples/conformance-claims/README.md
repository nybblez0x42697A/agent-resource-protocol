# Conformance Claim Examples

This directory holds worked examples of adopter conformance
claims for AGRP v1.

## What These Are

Each `*-claim.example.json` file is a complete, schema-valid
example of an adopter conformance claim — the publishable artifact
shape defined at `spec/conformance/conformance-claim-template.md`
and `models/schemas/conformance-claim.schema.json`.

Claims are **supplementary adopter-support material**, not part
of the AGRP v1 normative artifact set. An implementation does not
need to publish a claim to be v1-conformant; these examples exist
so adopters who choose to publish one have a concrete starting
point.

## What These Are Not

- These examples are **not part of the AGRP v1 normative artifact
  set** at `spec/charter/agrp-v1-artifact-set.md`.
- They are **not walked by** `tools/validate-all.py`. The
  adopter command surface remains the conformance harness +
  bundle validation; claim validation is a separate, opt-in
  step.
- They are **not** a certification or branding mechanism. AGRP
  defines no certification body; claims are self-published.

## Examples

| File | Bundle referenced | Attestation? | Distinctive feature |
|---|---|---|---|
| `northstar-claim.example.json` | Northstar tool registry (`examples/adaptations/northstar-tool-registry/`) | Yes — self-attested | Demonstrates the optional `attestation` block populated with concrete evidence-attestation values per `spec/compliance/evidence-freshness-and-attestation.md §Minimum Evidence Description`. |
| `pinecrest-claim.example.json` | Pinecrest data products (`examples/adaptations/pinecrest-data-products/`) | No | Demonstrates that `attestation` is genuinely optional at the top level — the claim validates with the field entirely absent. Use this pattern when no attested evidence is available. |
| `helios-claim.example.json` | Helios governance registry (`examples/adaptations/helios-governance-registry/`) | No | Demonstrates a privacy/redaction posture: the bundle's design doc and artifacts include redacted review evidence and privacy-tier profile declarations. The claim's `claimElements` evidence pointers reference those bundle artifacts (slots 08 and 17) without re-shipping their contents. |

Each example is intentionally written to a different combination
of claim shape and bundle posture, so collectively they exercise:

- the optional `attestation` block when present (Northstar)
- the optional `attestation` block when absent (Pinecrest + Helios)
- claim coherence with a bundle that has privacy-redaction
  evidence as a domain-specific concern (Helios)

## Using an Example

To use one of these as a starting point for your own claim:

1. Copy the example file into your own repository alongside your
   adopter bundle.
2. Edit `claimedBy`, `claimedAt`, `bundleReference`, and the
   `claimElements` evidence pointers to reflect your system.
3. Adjust `schemasInScope`, `operationsInScope`, and
   `errorCategoriesInScope` to match what your bundle actually
   exercises.
4. Include or omit the `attestation` block based on whether you
   have attested evidence; if you include it, populate the
   minimum required fields per
   `spec/compliance/evidence-freshness-and-attestation.md §Minimum Evidence Description`.
5. Validate the result against
   `models/schemas/conformance-claim.schema.json`. See the
   "Validation" section of
   `spec/conformance/conformance-claim-template.md` for the
   one-off validation pattern.

## Why These Live Here, Not in `examples/adaptations/`

`examples/adaptations/` holds adopter *bundles* — the evidence
artifacts a bundle ships (resources, registration records,
audit records, lifecycle transitions, etc.). A *claim* is a
separate artifact: it points at a bundle and describes the
claimant's conformance posture relative to v1. Keeping claims in
a sibling directory makes that boundary explicit and avoids
inflating bundle manifest counts.
