# Pinecrest Data Products — Reference Adaptation Bundle

**Status**: Non-normative supporting material per
`spec/charter/agrp-v1-artifact-set.md:85-92`.
**Companion design doc**: [`docs/adaptations/pinecrest-data-products.md`](../../../docs/adaptations/pinecrest-data-products.md).

This bundle shows the concrete JSON artifacts a synthetic
catalog implementation ("Pinecrest Data Products") would emit
when registering one focal data product through one
schema-version evolution and one lifecycle transition. Pinecrest
is fictional; nothing here imitates a real product. The bundle is
disciplined to a single end-to-end story so each file is small
enough to read in full.

The focal data product is **`pinecrest/customer-orders-daily`**.
It composes two synthetic upstream products that are referenced
by ID only and are not authored as separate artifacts:
`pinecrest/customer-master@v3` and
`pinecrest/order-events-stream@v7`.

## How to read this bundle

Read the files in order — the two-digit step prefix is the
intended read order, not just a filename convention. Each step
either emits a standalone resource artifact or carries a
control-plane envelope request/response (with one standalone
lifecycle event in step 11). Pair this bundle with the
companion design doc's §8 walkthrough for narrative context.

## File inventory

| # | File | Schema | Role |
|---|------|--------|------|
| 00 | `00-data-product-resource.v1.example.json` | `models/schemas/resource-entity.schema.json` | v1 of the focal data product. Composition deps live in `metadata.compositionDependencies`. |
| 01 | `01-register-resource-version.v1.request.json` | `models/schemas/control-plane-envelope.schema.json` (RegisterResourceVersion request branch) | Owner registers v1 via control-plane envelope. |
| 02 | `02-register-resource-version.v1.response.json` | `models/schemas/control-plane-envelope.schema.json` (RegisterResourceVersion response branch) | Catalog returns the registration record + initial lineage node. |
| 03 | `03-registration-record.v1.example.json` | `models/schemas/registration-record.schema.json` | Standalone view of the v1 registration record. |
| 04 | `04-audit-record.create.v1.example.json` | `models/schemas/audit-record.schema.json` | Audit entry for the v1 create action. |
| 05 | `05-lineage-node.v1.example.json` | `models/schemas/lineage-node.schema.json` | v1 lineage node — `parentVersionId: null`. No composition deps (schema has `additionalProperties: false`). |
| 06 | `06-data-product-resource.v2.example.json` | `models/schemas/resource-entity.schema.json` | v2 with a non-breaking column add (`customer_segment`, nullable). Composition deps preserved. |
| 07 | `07-register-resource-version.v2.request.json` | `models/schemas/control-plane-envelope.schema.json` (RegisterResourceVersion request branch) | Owner registers v2; envelope-level `expectedVersionId: "1.0.0"` carries the optimistic-lock check. |
| 08 | `08-lineage-node.v2.example.json` | `models/schemas/lineage-node.schema.json` | v2 lineage node — `parentVersionId: "1.0.0"`, `mutationType: "update"`. No composition deps. |
| 09 | `09-audit-record.update.v2.example.json` | `models/schemas/audit-record.schema.json` | Audit entry for the v2 update action. |
| 10 | `10-lifecycle-transition.draft-to-active.request.json` | `models/schemas/control-plane-envelope.schema.json` (TransitionLifecycleState request branch) | Steward transitions v2 from draft to active under the envelope. |
| 11 | `11-lifecycle-transition.draft-to-active.event.json` | `models/schemas/lifecycle-transition.schema.json` (standalone, NOT envelope-wrapped) | Standalone state-transition event payload — no `operation`, no `requestId`. |
| 12 | `12-evidence-attestation.refresh-sla.example.json` | spec-prose: `spec/compliance/evidence-freshness-and-attestation.md:60-89` | Refresh-SLA attestation backing the transition. No dedicated schema. |
| 13 | `13-audit-record.transition.example.json` | `models/schemas/audit-record.schema.json` | Audit entry for the lifecycle transition (`action: "update"` — `transition` is not in the audit-action enum). |
| 14 | `14-capability-advertisement.example.json` | `models/schemas/capability-advertisement.schema.json` | Catalog advertises baseline conformance + Pinecrest extensions and the focal product's recommended version. |
| 15 | `15-profile-declaration.consumer-trust.example.json` | `models/schemas/profile-declaration.schema.json` (`supportedDeclaration` branch) | Consumer trust profile that AGRP-v1-baseline implementations and consumers operate under for this catalog. |

Total: 16 JSON artifacts. This `README.md` is an index, not an
artifact, and is not counted in the 16.

## Schema-mapping notes

- All envelope-wrapped operation messages
  (files 01, 02, 07, 10) validate against
  `control-plane-envelope.schema.json`. There is no separate
  `register-resource-version.schema.json` — the envelope's
  per-operation request/response branches are selected by the
  `operation` discriminator (a `const` field inside each
  `oneOf` branch). Values used by this bundle are
  `RegisterResourceVersion` and `TransitionLifecycleState`.
- File 11 is the **standalone** lifecycle-transition event
  payload, not the envelope-wrapped form. It carries no
  `operation` or `requestId` field. This mirrors the 0047
  Northstar bundle's pattern.
- File 12 has no dedicated JSON Schema. Its shape is validated
  by citation match against
  `spec/compliance/evidence-freshness-and-attestation.md:60-89`,
  which describes the evidence fields this bundle preserves.
- Composition dependencies appear ONLY on the resource-entity
  artifacts (files 00 and 06) inside
  `metadata.compositionDependencies`. The `lineage-node` schema
  has `additionalProperties: false`, so composition deps are
  deliberately not placed there. See the design doc's §7 for
  the rationale.

## Identifier conventions used in this bundle

- **Focal product `resourceId`**:
  `pinecrest/customer-orders-daily` (stable across every file
  in the bundle).
- **Focal product `versionId`**: SemVer-style — `1.0.0` for v1
  (files 00, 03, 04, 05) and `1.1.0` for v2 (files 06, 08, 09,
  10, 11, 12, 13).
- **Upstream synthetic-referenced products**: identified by
  `pinecrest/customer-master@v3` and
  `pinecrest/order-events-stream@v7`. These IDs use a `@vN`
  pin shorthand. Pinecrest's choice for upstream pins is
  deliberately distinct from the focal product's SemVer
  pattern — upstream products are referenced, not authored
  here. The design doc's §10 (Implementation-defined edges)
  notes this is an adaptation choice, not an AGRP convention.
- **Actors**:
  - `pinecrest:owner:customer-orders-team` — registers v1 and
    v2 of the focal product.
  - `pinecrest:steward:catalog-governance` — performs the
    draft→active lifecycle transition and stewards the
    consumer trust profile.
  - `pinecrest:attestor:refresh-sla-signer` — signs the
    refresh-SLA attestation backing the transition.
- **Profile**:
  `pinecrest:profile:consumer-trust:marketing-analytics`.
- **Commit IDs**: ULID-shaped, prefixed with synthetic
  `urn:pinecrest:commit:` markers for visual distinctness
  per stage (`...AAAA...` for v1 register,
  `...BBBB...` for v2 register, `...CCCC...` for the
  lifecycle transition).
- **Evidence ID**: `urn:pinecrest:evidence:refresh-sla:`
  followed by `<resourceId>/<versionId>/<observation-date>`,
  yielding
  `urn:pinecrest:evidence:refresh-sla:pinecrest/customer-orders-daily/1.1.0/2026-05-06`.

## Cross-coherence summary

The validation reports in
`.specweave/increments/0051-agrp-data-product-catalog-reference-adaptation/reports/`
record the per-stage and bundle-wide cross-coherence checks.
At a glance:

- Focal `resourceId` is identical across all 14 files where it
  appears.
- v1 `versionId` (`1.0.0`) and v2 `versionId` (`1.1.0`) match
  between resource-entity, registration-record, lineage-node,
  audit-record, lifecycle-transition, and capability-
  advertisement.
- `parentVersionId` on file 08 references file 00's `versionId`.
- `evidenceRefs[0]` on file 13 equals `evidenceId` on file 12.
- `profiles[0]` on file 14 equals `profileId` on file 15.
- Composition dependencies on files 00 and 06 match the
  upstream-product IDs cited in the design doc's §7
  (Composition).

## What this bundle does NOT cover

- No second focal data product (only `pinecrest/customer-orders-daily`
  is authored as full artifacts; upstream products are
  referenced by ID only).
- No supersession, deprecation, or archive walkthrough.
- No conflict-resolution / error walkthrough.
- No consumer-side subscription flow (the consumer trust
  profile is declared, but no subscribe / consume operations
  are walked).
- No replay-tool / executable state-machine claim — by design
  per the increment's locked plan-of-record. If the bundle's
  state machine becomes load-bearing enough to justify
  executable proof, a follow-up increment opens for it
  (mirroring 0047 → 0048).

For the design rationale and the
implementation-defined edges, see the companion design doc.
