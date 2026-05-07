# AGRP Data Product Catalog — Reference Adaptation

## 1. Status

**Date**: 2026-05-06.

**Classification**: This document is a non-normative reference adaptation example for AGRP v1 — illustrative, not authoritative. It walks one synthetic system through the AGRP lifecycle to give adopters something concrete to compare their own implementations against. It does not introduce normative claims; where the document surfaces something AGRP says, it cites the spec file and a line range. Per `spec/charter/agrp-v1-artifact-set.md:85-92`, content under `docs/adaptations/` and `examples/adaptations/` is supporting material, not part of the v1 normative artifact set.

This is the second adaptation in a series. The first — the Northstar Tool Registry adaptation at `docs/adaptations/northstar-tool-registry.md` (increment 0047) — demonstrated AGRP v1 against a capability-rollout-shaped tool registry. This one stresses different surfaces.

## 2. Overview

Pinecrest Data Products is a fictional data catalog used as a worked example. The mapping shown here would apply, with reasonable modification, to real data catalogs that register schema-versioned data products, declare cross-product dependencies, and serve consumers under trust-profile contracts.

Northstar exercised AGRP's capability-rollout path — one tool, version evolution that added a capability, lifecycle transition from preview to general-availability. Pinecrest is shape-different on purpose: schema-version evolution instead of capability-rollout, cross-product composition instead of single-resource lineage, and consumer trust profiles instead of registry discoverability. The intent is to surface whether the v1 artifact set carries adopter value across structurally different domains, and to give a second concrete reference for implementers whose systems are not tool-registry-shaped.

A companion artifact bundle at `examples/adaptations/pinecrest-data-products/` carries 16 concrete JSON artifacts emitted across the walkthrough plus a bundle README. Section 8 walks the focal product through those 16 steps; section 9 indexes them.

## 3. The Pinecrest Data Catalog

Pinecrest is a synthetic-but-disciplined catalog: not modeled on any specific real product, so the mapping can be complete instead of apologizing for fidelity gaps in someone else's API. The system shape is intentionally minimal — one focal data product walked end to end through one schema-version evolution and one lifecycle transition.

The catalog manages **data products**: addressable, schema-versioned collections of curated data emitted by upstream sources (datasets, materialized views, change-data-capture streams). A data product is identified by a stable `resourceId` (e.g., `pinecrest/customer-orders-daily`); each registered version carries a `versionId` (treated here as a schema-version identifier), a declared schema (column list with types and a partition key), a refresh policy (cron expression plus an SLA window), and a list of upstream **composition dependencies** — references to other Pinecrest products that this product is built from.

Pinecrest interprets the AGRP `resource-entity` shape directly for data products; the resource-kind choice is discussed in section 5 and in section 10.

The scale of ambition for this adaptation is single-target and single-walkthrough. Multi-product catalogs, supersession flows, deprecation walkthroughs, and consumer-side subscription mechanics are out of scope; section 12 lists what is intentionally not covered.

## 4. Operator roles

Pinecrest names four operator roles and maps each to AGRP actor concepts as referenced in the bundle's `actor` identifiers:

| Pinecrest role | Description | AGRP `actor` identifier (example) |
|----------------|-------------|-----------------------------------|
| Data product owner | The team or individual who registers the data product, defines its schema, and owns its evolution | `pinecrest:owner:customer-orders-team` |
| Data steward | Curates the catalog as a whole; governs naming, deprecation timing, and adherence to compliance policy | `pinecrest:steward:catalog-governance` |
| Attestation authority | Signs refresh-SLA attestations confirming that the data product was refreshed within its declared SLA window | `pinecrest:attestor:refresh-sla-signer` |
| Consumer | Declares a trust profile and reads data products under that profile's contract | `pinecrest:consumer:marketing-analytics` |

These role names are local to Pinecrest. The AGRP `actor` field appears on the bundle's request envelopes, audit records, and event payloads; Pinecrest populates it from this role table. Different adaptations would use different role taxonomies.

## 5. Data product resource model

Pinecrest maps each data product onto a single AGRP `resource-entity` artifact. The mapping is direct, with two notable choices.

**`resourceKind`**: Pinecrest sets `resourceKind: "memory"` for every data product. The AGRP enum at `models/schemas/common.schema.json#/$defs/resourceKind` defines five values (`prompt`, `agent`, `tool`, `environment`, `memory`); Pinecrest reads `memory` as the closest semantic anchor for "addressable, persistent, queryable curated state" — which is what a data product is. Section 10 returns to this choice; it is an adaptation decision, not a recommendation that AGRP redefine data products as memory in general.

**`metadata` fields**: Pinecrest puts the data-product-specific shape inside `metadata`, which `resource-entity.schema.json` declares as a `common.schema.json#/$defs/objectMap` with `additionalProperties: true`. The fields used:

| Field | Purpose |
|-------|---------|
| `metadata.pinecrestSubKind` | Disambiguates this `memory` resource as a data product (vs agent-memory uses) |
| `metadata.declaredSchema` | Column list, types, partition key |
| `metadata.refreshPolicy` | Cron expression + SLA window |
| `metadata.capabilityFeatures` | Tags such as `pii-redacted`, `partitioned-by-day`, `streaming-cdc` |
| `metadata.compositionDependencies` | Array of upstream-product references — see section 7 |

The standard `resource-entity` fields (`resourceId`, `versionId`, `implementationRef`, `interfaceRef`, `config`, `state`) carry their schema-defined meanings. v1 and v2 of the focal product share the same `resourceId`; they differ only in `versionId`, `metadata.declaredSchema` (v2 adds the `customer_segment` column), and any timestamp fields.

## 6. Schema-version lifecycle

Pinecrest data products use the AGRP baseline lifecycle vocabulary directly. The baseline at `spec/rspl/lifecycle-and-transition-semantics.md:25-34` enumerates six states:

- `draft`
- `active`
- `deprecated`
- `archived`
- `superseded`
- `restored`

Pinecrest does not introduce any overlay vocabulary. A schema version moves through these states the same way any AGRP resource version would.

This walkthrough demonstrates exactly **one transition**: `draft → active`. The remaining four states (deprecated, archived, superseded, restored) are part of the available vocabulary; their semantics are documented in the spec, and a real Pinecrest implementation would exercise them when versions are deprecated or replaced. They are simply not shown in this bundle. Section 12 lists them under gaps.

## 7. Composition: cross-product dependencies

Data products in Pinecrest are typically built from other data products. The focal product `pinecrest/customer-orders-daily` v1 depends on two upstream products: `pinecrest/customer-master@v3` (a slowly-changing customer dimension) and `pinecrest/order-events-stream@v7` (a CDC stream of order events). Both v1 and v2 of the focal product carry the same upstream pinning.

Pinecrest places these dependency declarations inside `resource-entity.metadata.compositionDependencies`. This is an implementation-defined choice, made under two constraints.

**Spec-side latitude**: The AGRP composition spec at `spec/composition/dependency-and-composition-model.md:39-49` defines what a dependency declaration should identify (dependent artifact, target artifact, dependency type, required-or-optional, compatibility expectation), and at `spec/composition/dependency-and-composition-model.md:51-74` defines the baseline dependency types (`requires`, `prefers`, `extends`, `replaces`). The same spec at line 49 explicitly states it does not mandate a single wire format. Pinecrest is therefore free to choose where the declaration lives.

**Schema-side constraint**: `models/schemas/lineage-node.schema.json` has `additionalProperties: false`, so attempting to put composition dependencies on a lineage-node artifact would fail schema validation. Pinecrest reserves lineage-node for its declared purpose (version-lineage: `parentVersionId`, `mutationType`, `changeSummary`, etc.) and places composition declarations on the resource-entity instead, where the `metadata` objectMap accepts the extension by construction.

A Pinecrest composition-dependency entry uses this shape:

```json
{
  "dependentArtifact": "pinecrest/customer-orders-daily@1.0.0",
  "targetArtifact": "pinecrest/customer-master@v3",
  "dependencyType": "requires",
  "required": true,
  "compatibilityExpectation": "schema-stable-pinned"
}
```

The `dependencyType` value is drawn from the baseline vocabulary at `spec/composition/dependency-and-composition-model.md:51-74`. The remaining keys are Pinecrest's own; a different adaptation could use a different field set under the same `metadata.compositionDependencies` key, or place the declaration somewhere else entirely.

**Observability implication**: Because composition dependencies form a directed graph across data products, observability traces emitted by data-refresh runs propagate naturally along that graph. A consumer reading `pinecrest/customer-orders-daily` and tracing back to `customer-master@v3` and `order-events-stream@v7` exercises the trace-continuity surface defined at `spec/observability/observability-and-trace-correlation.md:87-96` — correlating the original request, the resulting audit and lineage events, and any diagnostic references along the dependency chain. Section 11 returns to this in the conformance discussion.

## 8. End-to-end walkthrough

The 16 artifacts in `examples/adaptations/pinecrest-data-products/` walk the focal product `pinecrest/customer-orders-daily` from initial creation through a schema-version evolution and a lifecycle transition. Each step names the corresponding bundle file.

1. The owner creates the v1 data product resource → `00-data-product-resource.v1.example.json`. The artifact carries `resourceKind: "memory"`, `metadata.pinecrestSubKind: "data-product"`, the v1 column list, and a `metadata.compositionDependencies` array referencing the two upstream products.
2. The owner registers v1 with the catalog → `01-register-resource-version.v1.request.json` (envelope, `operation: "RegisterResourceVersion"`).
3. The catalog returns the registration response → `02-register-resource-version.v1.response.json`.
4. The resulting registration record is persisted standalone → `03-registration-record.v1.example.json`.
5. The catalog emits a creation audit record → `04-audit-record.create.v1.example.json`.
6. The catalog records v1's lineage as a root node → `05-lineage-node.v1.example.json`. The file carries only the nine schema-allowed fields per `models/schemas/lineage-node.schema.json`; it does not (and cannot) carry a composition extension, per section 7.
7. The owner publishes a non-breaking schema change as v2 (adds the `customer_segment` column) → `06-data-product-resource.v2.example.json`. Same composition pinning as v1; same `resourceId`; new `versionId`.
8. The owner registers v2 → `07-register-resource-version.v2.request.json`.
9. The catalog records v2's lineage with `parentVersionId` referencing v1 → `08-lineage-node.v2.example.json`. Again, no composition extension.
10. The catalog emits an update audit record → `09-audit-record.update.v2.example.json`.
11. The owner requests a lifecycle transition `draft → active` → `10-lifecycle-transition.draft-to-active.request.json` (envelope, `operation: "TransitionLifecycleState"`).
12. The catalog applies and emits the transition event → `11-lifecycle-transition.draft-to-active.event.json` (standalone `lifecycle-transition.schema.json`, not envelope-wrapped — the same pattern Northstar's bundle uses).
13. The attestation authority signs a refresh-SLA attestation backing the transition → `12-evidence-attestation.refresh-sla.example.json`. The artifact has no dedicated schema; its shape matches the field-list at `spec/compliance/evidence-freshness-and-attestation.md:60-89`.
14. The catalog emits a transition audit record → `13-audit-record.transition.example.json`.
15. The catalog updates its capability advertisement to recommend v2 → `14-capability-advertisement.example.json`.
16. The consumer publishes a trust-profile declaration declaring eligibility to subscribe → `15-profile-declaration.consumer-trust.example.json`.

The `actor` field on every operation is populated from the role table in section 4.

## 9. Concrete artifacts (index)

The 16 JSON files in `examples/adaptations/pinecrest-data-products/`:

| # | File | One-line description |
|---|------|----------------------|
| 00 | `00-data-product-resource.v1.example.json` | v1 resource-entity (`resourceKind: "memory"`, composition deps in metadata) |
| 01 | `01-register-resource-version.v1.request.json` | `RegisterResourceVersion` request envelope for v1 |
| 02 | `02-register-resource-version.v1.response.json` | `RegisterResourceVersion` response envelope for v1 |
| 03 | `03-registration-record.v1.example.json` | Standalone registration record persisted from the v1 response |
| 04 | `04-audit-record.create.v1.example.json` | Audit record for v1 creation |
| 05 | `05-lineage-node.v1.example.json` | Root lineage node for v1 (no parent, no composition extension) |
| 06 | `06-data-product-resource.v2.example.json` | v2 resource-entity (adds `customer_segment` column; same composition pinning) |
| 07 | `07-register-resource-version.v2.request.json` | `RegisterResourceVersion` request envelope for v2 |
| 08 | `08-lineage-node.v2.example.json` | Lineage node for v2 with `parentVersionId` to v1 |
| 09 | `09-audit-record.update.v2.example.json` | Audit record for v2 update |
| 10 | `10-lifecycle-transition.draft-to-active.request.json` | `TransitionLifecycleState` request envelope (`draft → active`) |
| 11 | `11-lifecycle-transition.draft-to-active.event.json` | Standalone lifecycle-transition event (not envelope-wrapped) |
| 12 | `12-evidence-attestation.refresh-sla.example.json` | Refresh-SLA attestation backing the transition (no dedicated schema) |
| 13 | `13-audit-record.transition.example.json` | Audit record for the lifecycle transition |
| 14 | `14-capability-advertisement.example.json` | Updated capability advertisement recommending v2 |
| 15 | `15-profile-declaration.consumer-trust.example.json` | Consumer trust-profile declaration (`marketing-analytics`) |

A bundle-local `README.md` indexes the same set with reading-order guidance.

## 10. Implementation-defined edges

Several places in this adaptation are Pinecrest's invention — AGRP leaves the choice to the implementer, and a different adaptation could choose differently.

- **`resourceKind` selection**. Pinecrest uses `resourceKind: "memory"` with `metadata.pinecrestSubKind: "data-product"`. The AGRP enum at `models/schemas/common.schema.json#/$defs/resourceKind` does not include `"data-product"`; Pinecrest reads `memory` as the closest semantic anchor for "addressable, persistent, queryable curated state". This is an adaptation decision, not a recommendation that AGRP redefine data products as memory in general. A different adaptation could pick `environment` (data products as environmental context) or could justify `tool` if the catalog's data products are accessed primarily through executable query interfaces.

- **Composition-deps placement**. Pinecrest puts composition declarations on `resource-entity.metadata.compositionDependencies`. The AGRP composition spec at `spec/composition/dependency-and-composition-model.md:39-49` does not mandate a wire format, leaving the choice open. A different adaptation could place declarations on a sibling artifact, or on a per-version `extensions` object, or in a separate registry call.

- **Refresh-policy semantics**. `metadata.refreshPolicy` carries a cron expression and an SLA window. The cron-syntax flavor (5-field, 6-field, Quartz-style), the SLA-window unit (minutes vs duration ISO-8601), and the timezone interpretation are all Pinecrest-internal. AGRP does not constrain refresh-policy fields.

- **Partition-key semantics**. `metadata.declaredSchema.partitionKey` is treated as a hint about physical layout; Pinecrest does not enforce it at the protocol layer. A storage-tier implementation might use it, or might ignore it.

- **Schema-feature taxonomy**. `metadata.capabilityFeatures` (`pii-redacted`, `partitioned-by-day`, `streaming-cdc`, etc.) is Pinecrest-local vocabulary. A real catalog would publish its taxonomy as part of operator documentation.

- **Consumer trust-profile contents**. The fields inside the `marketing-analytics` profile declaration are minimum-declaration-metadata-shaped per `spec/compliance/profile-declaration-and-discovery-interoperability.md:37-58`, but the trust-tier vocabulary (`baseline-pii-safe`, `aggregated-only`, etc.) is Pinecrest-internal.

## 11. Conformance posture

A real Pinecrest implementation could make a baseline AGRP v1 conformance claim per `spec/conformance/baseline-conformance.md:19-25` (Conformance Levels) by:

1. Emitting the required artifacts the bundle illustrates (`resource-entity`, `registration-record`, `audit-record`, `lineage-node`, `lifecycle-transition`, `capability-advertisement`, `profile-declaration`).
2. Using only operations from the envelope's `operation` enum (`RegisterResourceVersion`, `TransitionLifecycleState`, `GetRegistrationRecord`, `GetLineage`, `GetAuditRecord`, `ListResourceVersions`, `RestoreResourceVersion`).
3. Honoring the six-state baseline lifecycle vocabulary at `spec/rspl/lifecycle-and-transition-semantics.md:25-34`.
4. Carrying `actor`, `resourceId`, and `versionId` on every operation that needs provenance.
5. Validating its emitted JSON against the schemas in `models/schemas/`.

A readiness profile per `spec/compliance/compliance-and-readiness-profiles.md:45-55` (Readiness Profile Concept) could narrow this claim — for example, requiring refresh-SLA attestations for every lifecycle transition. The consumer trust profile in file 15 follows the minimum declaration metadata pattern at `spec/compliance/profile-declaration-and-discovery-interoperability.md:37-58`.

The trace-continuity surface from section 7 also forms part of the conformance posture: an implementation that emits resource-entities with composition dependencies but does not propagate trace IDs across the dependency graph would still validate schema-wise, but would not satisfy the trace-continuity expectation at `spec/observability/observability-and-trace-correlation.md:87-96`.

## 12. Gaps and limitations

This adaptation deliberately does NOT cover:

- **Multiple focal data products**. Only `pinecrest/customer-orders-daily` gets full artifact treatment; the two upstream products are referenced by ID only.
- **Supersession**. The `superseded` and `restored` lifecycle states are not exercised; no `supersedesVersionId` artifact appears in the bundle.
- **Deprecation walkthrough**. The `deprecated → archived` transition is not shown; only `draft → active`.
- **Conflict-error walkthrough**. No `conflict-error` artifact is emitted; the catalog's conflict-handling behavior is out of scope.
- **Consumer subscription flow**. The trust-profile declaration is included, but the subscribe / read / consume mechanics are not walked.
- **Multi-stage attestation chain**. A single refresh-SLA attestation backs the transition; chained or threshold-based attestation is not shown.
- **Executable replay tool**. No companion tool replays the bundle through an in-memory state machine. (Northstar's bundle has one at `tools/adaptations/replay-northstar.py`. If state-machine invariants emerge from Pinecrest's bundle, a follow-up increment may add an analogous replay tool.)

A future adaptation increment could pick any of these up. The pattern established by 0047 → 0048 (design doc + bundle, then a follow-up replay-tool increment) is the model.

## 13. How to read this example

**Reading order**: top-to-bottom in this file, then the bundle files in their step order (00 through 15). Section 8 names each file at its step.

**Prerequisites**: familiarity with the AGRP charter at `spec/charter/repository-charter.md` and at least skimming `spec/rspl/core-resource-model.md` and `spec/control-plane/control-plane-contracts.md`. Reading the schema files in `models/schemas/` for `resource-entity`, `lineage-node`, and `control-plane-envelope` makes the bundle artifacts directly comprehensible.

**Relationship to conformance vectors**: the bundle is NOT a conformance test. The canonical conformance test set is the harness fixtures at `examples/conformance-vectors/`, validated by `python3 tools/conformance/run_conformance_vectors.py`. The Pinecrest bundle is an adoption walkthrough — it shows how an implementer could shape their own artifacts.

**Relationship to the Northstar adaptation**: Northstar (at `docs/adaptations/northstar-tool-registry.md`) walks a tool-registry-shaped system; Pinecrest walks a data-catalog-shaped system. They are complementary; an implementer whose system matches neither shape can compare both to find the closest fit.
