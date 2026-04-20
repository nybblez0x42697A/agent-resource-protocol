# AGRP v1.0.0 Publication Checklist

This checklist is non-normative.

Use it when preparing a public or internal publication of `AGRP v1.0.0`.

## Identity

- Confirm the published release identifier is exactly `AGRP v1.0.0`
- Confirm the publication does not refer to the release as generic `AGRP` without a release designation where precision is required
- Confirm any historical `ARP` references are either removed from the published surface or explained as historical shorthand only

## Normative Anchors

- Include or link the normative release definition: `spec/versioning/agrp-v1-release-definition.md`
- Include or link the normative artifact set: `spec/charter/agrp-v1-artifact-set.md`
- Confirm the publication preserves the rule that `AGRP v1.0.0` is anchored to the `AGRP v1` artifact set
- Confirm deferred areas such as `SEPL` are not implied to be part of the release

## Artifact Completeness

- Verify every normative artifact listed in the artifact-set document exists at the published location or is otherwise accessible from the publication record
- Verify no listed artifact has been silently replaced with materially different content under the same path
- Verify non-normative supporting materials are labeled as non-normative where publication packaging could blur the distinction

## Supporting Materials

- Optionally include schemas from `models/schemas/`
- Optionally include examples from `examples/`
- Optionally include adopter templates from `adopters/`
- If included, label these materials as supportive or illustrative rather than as the normative definition of the release

## Conformance Visibility

- Point readers to the applicable conformance anchor: `spec/conformance/baseline-conformance.md`
- If the publication includes binding, profile, or extension claims, identify them as layered on top of `AGRP v1.0.0` rather than replacements for it

## Sanity Checks

- Confirm the publication does not say or imply that every repository file is part of `AGRP v1.0.0`
- Confirm the publication does not invent a different release boundary than the one defined in the normative release documents
- Confirm the publication mechanism remains illustrative if it is being documented for reuse
