# Northstar Tool Registry — AGRP v1 Reference Adaptation

## 1. Status

**Classification**: Non-normative supporting material under `spec/charter/agrp-v1-artifact-set.md:85-92` ("files under `examples/`" and "analysis under `docs/`"). This document does not amend, extend, or override any normative AGRP v1 artifact.

**Date**: 2026-04-30.

**Scope**: A reference adaptation example for `AGRP v1` — illustrative, not authoritative. The walkthrough demonstrates one synthetic system mapped end-to-end against AGRP's resource, registration, lineage, lifecycle, and capability-advertisement surfaces. Where this document's wording diverges from a spec passage, the spec passage governs.

**Reading order**: Section 7 ("End-to-end walkthrough") is the main act. Sections 1-6 set up the system; sections 8-12 close the loop on artifacts, edges, and limits. Section 12 gives an explicit reading guide for adopters.

## 2. Overview

`AGRP v1` defines a control-plane vocabulary for registering versioned agent resources, recording lineage, transitioning lifecycle state with evidence, and advertising capabilities. The corpus is normative — it tells implementers what an AGRP-conformant artifact must look like — but it does not, on its own, demonstrate what a complete adopter integration feels like end-to-end.

This document fills that gap with a single worked example. The fictional **Northstar Tool Registry** is an agent tool registry that publishes versioned tools through staged releases. Northstar is not a real product; the system shape is engineered specifically to exercise the AGRP surfaces that an adopter would encounter on day one.

The deliverables are paired:

- **This design doc** (`docs/adaptations/northstar-tool-registry.md`) explains the mapping decisions, lifecycle interpretation, and conformance posture.
- **The artifact bundle** (`examples/adaptations/northstar-tool-registry/`) contains 15 concrete JSON artifacts plus a `README.md` index — the exact protocol-shape outputs Northstar would emit at each lifecycle step. Every JSON file validates against an AGRP schema (or, for `evidence-attestation`, against the spec-prose field shape at `spec/compliance/evidence-freshness-and-attestation.md:60-89`).

This adaptation is the first in a hypothetical series. It deliberately covers a narrow path through the protocol — one tool, two versions, one lifecycle transition — so the demonstration can be complete instead of broad-and-shallow. Multi-tool, supersession, conflict-resolution, and deprecation/sunset walkthroughs are out of scope; they are appropriate territory for follow-up adaptations.

## 3. The Northstar Tool Registry

Northstar is a synthetic system: a registry that hosts agent-callable tools (think MCP-server-style tool packages, but generic — not modeled on the MCP specification or any other named real-world product). Tool publishers submit versioned tools; the registry steward governs the catalog; an attestation authority signs evidence backing stage promotions; adopters discover and consume tools via a capability advertisement.

**Why synthetic instead of a named real product?** A named reference target (a public package marketplace, a container registry, a real MCP registry implementation) carries fidelity obligations: the mapping has to be honest about that product's actual API, which often diverges from AGRP in ways that obscure the demonstration. By engineering a fictional system specifically to exercise AGRP surfaces, this adaptation avoids the "almost-but-not-quite" framing that would otherwise dominate the document. Adopters mapping a real system are expected to encounter rougher edges; section 11 ("Gaps and limitations") is explicit about which parts of the demonstration depend on Northstar's synthetic nature.

**Scale of ambition**: one tool (`northstar/example-search-tool`), two versions (`0.1.0` and `0.2.0` with a capability change between them), one lifecycle transition (v2's `draft → active` promotion, with an attestation backing it). Every other AGRP feature exists in the spec corpus and the conformance vectors, but is not exercised here.

**System purpose** (Northstar-internal terms): publishers iterate on tool capabilities and publish each significant version into the registry. The registry tracks per-version state (development → preview → general-availability → deprecated → sunset). Consumers query the registry for the current generally-available version of a tool and consume it through the registry-provided capability descriptor. Section 6 maps Northstar's stage vocabulary onto AGRP's six baseline lifecycle states; the mapping is one of the load-bearing implementation-defined edges and is called out in section 9.

## 4. Operator roles

Northstar has four operator roles. Three appear as `actor` or `attestorId` values in the bundle's artifacts; the fourth is a passive consumer.

| Role | AGRP field mapping | Walkthrough activity |
|---|---|---|
| **Tool publisher** | `actor` on register / audit records when a publisher initiates the action | Submits v1 and v2 of `northstar/example-search-tool`; named in the v1 and v2 audit records |
| **Registry steward** | `actor` on the lifecycle-transition request and its associated audit record | Approves the v2 `draft → active` promotion; named in the transition event's `actor` field |
| **Attestation authority** | `attestorId` on the `evidence-attestation` artifact | Signs the evidence package backing the GA promotion |
| **Adopter / consumer** | (passive in this walkthrough) | Reads the published capability advertisement; not named in any audit record |

The role-to-field mapping is locked at the [Northstar System Design](../../.specweave/increments/0047-agrp-northstar-tool-registry-reference-adaptation/spec.md) C2 ruling and is consistent across the bundle's artifact files. Real implementations may use different role partitions (for example, separating publisher and steward roles by team, or merging attestation into the steward role); section 9 discusses the tradeoffs.

## 5. Tool resource model

A Northstar tool maps onto AGRP's `resource-entity` (schema: `models/schemas/resource-entity.schema.json`; spec: `spec/rspl/core-resource-model.md`). The mapping is total: every Northstar-internal field has either a direct `resource-entity` slot or a place inside the schema's structured `metadata` object. No Northstar field is dropped; no `resource-entity` requirement is left unfilled.

| `resource-entity` field | Northstar value (example) | Notes |
|---|---|---|
| `resourceKind` | `"tool"` | The `resourceKind` enum at `models/schemas/common.schema.json:6-15` allows `prompt / agent / tool / environment / memory`; `tool` is the right kind for a callable tool package |
| `resourceId` | `"northstar/example-search-tool"` | Stable across all versions of the same tool |
| `versionId` | `"0.1.0"` (v1) and `"0.2.0"` (v2) | Distinct per version; semver-shaped by Northstar convention. The schema constrains only that `versionId` be a non-empty string |
| `implementationRef` | `"oci://registry.northstar.example/tools/example-search-tool@sha256:<digest>"` | OCI-style URI with a content-digest fragment. The schema accepts any non-empty string or an objectMap (`resource-entity.schema.json:16-26`); the spec prose at `spec/rspl/core-resource-model.md:80-82` lists "artifact digest, import path, endpoint, or packaged asset reference" as accepted shapes. The OCI URI is one such packaged-asset reference. Section 9 discusses why Northstar chose this shape over alternatives. |
| `interfaceRef` | `"https://registry.northstar.example/tools/example-search-tool/interfaces/v1.json"` | URL pointing to the tool's capability descriptor (the same descriptor surfaced in file 14, the capability advertisement) |
| `config` | `{}` for v1; small parameter map for v2 | Per-version configuration object; default values live here |
| `state` | `{}` | Required by the schema; tools in this walkthrough have no inherent runtime state at registration time, so an empty object is structurally sufficient |
| `metadata` | `{ northstarStage, displayName, description, publisher, license, createdAt, capabilities, runtimeRequirements, contentDigest }` | All Northstar-specific surface information lives here. `northstarStage` carries the implementation-defined pre-release distinction (see section 6) |
| `extensions` | `{}` (empty default) | Reserved for future Northstar fields without breaking the schema contract |

The `metadata.capabilities` array is the load-bearing field that changes between v1 and v2: v1 advertises only `search`; v2 advertises `search` and `summarize`. This is the "capability change" referenced throughout the document.

## 6. Lifecycle stages

Northstar uses a five-stage surface vocabulary for tool versions: **development → preview → general-availability → deprecated → sunset**. AGRP defines six baseline `lifecycleState` values at `spec/rspl/lifecycle-and-transition-semantics.md:27-34`: `draft`, `active`, `deprecated`, `archived`, `superseded`, `restored`. Northstar's surface stages map onto AGRP's baseline as follows:

| Northstar surface stage | AGRP `lifecycleState` | AGRP `registrationStatus` | Notes |
|---|---|---|---|
| `development` | `draft` | `active` | Publisher-only iteration; the version exists in the registry but is not advertised to consumers |
| `preview` | `draft` | `active` | Shared with selected consumers; still pre-release. The preview/development distinction lives in `metadata.northstarStage`, not in `lifecycleState` |
| `general-availability` | `active` | `active` | Promoted; default selectable version for adopter discovery |
| `deprecated` | `deprecated` | `deprecated` | Not recommended; still addressable |
| `sunset` | `archived` | `archived` | History-only; out of scope for this walkthrough |

Two subtleties surface here and recur across the artifact bundle:

**`lifecycleState` vs `registrationStatus`**: per `models/schemas/common.schema.json:16-25`, `registrationStatus` does not include `draft` — its values are `active / superseded / deprecated / archived / removed`. `lifecycleState` (lines 26-36 of the same schema) does include `draft`. On registration of a draft version, `registration-record.status` is `active` (the *registration record itself* is current and valid) while the *version's* `lifecycleState` is `draft`. ADR 0001 at `docs/decisions/0001-control-plane-statusfilter-resolution.md` is the spec-side reference for this distinction. The bundle's registration records honor it: every `registration-record.status` is `active`, even for v1 which never leaves `draft` lifecycle.

**The `northstarStage` metadata escape hatch**: AGRP's six baseline states do not natively distinguish pre-release stages — `development` and `preview` both map to `draft`. Northstar carries the surface distinction in `metadata.northstarStage` so the `draft → active` transition can render to consumers as the surface promotion `preview → general-availability`. This is an implementation-defined edge (section 9) and is not load-bearing for any AGRP conformance claim.

## 7. End-to-end walkthrough

The walkthrough threads `northstar/example-search-tool` through 15 bundle steps. Each step lists the artifact file in `examples/adaptations/northstar-tool-registry/` that captures the on-the-wire or registry-persisted shape at that moment.

**Phase 1 — Publisher creates and registers v1 (initial draft).**

1. **Publisher constructs v1's resource entity** — `00-tool-resource.v1.example.json`. The publisher fills out `resourceKind=tool`, the resource and version identifiers, the OCI implementationRef, an interface URL, and the metadata block. `metadata.northstarStage` is `"preview"`; `metadata.capabilities` contains only `search`.

2. **Publisher submits the register-resource-version request** — `01-register-resource-version.v1.request.json`. The request is wrapped in a `control-plane-envelope` with `operation=RegisterResourceVersion`, a fresh `requestId`, the publisher's `actor`, and the inline `registrationRecord` and `auditRecord` payloads (envelope schema branch at `control-plane-envelope.schema.json:48-80`).

3. **Registry returns the success response** — `02-register-resource-version.v1.response.json`. The success envelope carries `result.{resourceId, versionId, registrationRecord, lineageNode}` per the response branch at `control-plane-envelope.schema.json:378-418`.

4. **Standalone view of v1's registration record** — `03-registration-record.v1.example.json`. Same record content as the response, persisted independently. `registration-record.status` is `active` even though `lifecycleState` is `draft` (per the section-6 distinction).

5. **Audit record for v1's creation** — `04-audit-record.create.v1.example.json`. The publisher is named in the `actor` field; the operation is `RegisterResourceVersion`.

6. **v1's lineage node** — `05-lineage-node.v1.example.json`. v1 is the root of its lineage; the node has no parent. `versionId` matches the registration record.

**Phase 2 — Publisher iterates and registers v2 (capability change, still draft).**

7. **Publisher constructs v2's resource entity** — `06-tool-resource.v2.example.json`. Same `resourceId`; new `versionId=0.2.0`. `metadata.northstarStage` is `"preview"`; `metadata.capabilities` is now `[search, summarize]`. The `implementationRef` points to a new OCI digest.

8. **Publisher submits v2's register-resource-version request** — `07-register-resource-version.v2.request.json`. Same envelope shape as step 2, with the new payload.

9. **v2's lineage node** — `08-lineage-node.v2.example.json`. `parentVersionId` is set to v1's `versionId`, establishing the lineage chain `v1 → v2`.

10. **Audit record for v2's creation** — `09-audit-record.update.v2.example.json`. Publisher named in `actor`; operation is `RegisterResourceVersion`.

**Phase 3 — Steward promotes v2 with an attestation (the AGRP `draft → active` transition).**

11. **Steward submits the lifecycle-transition request** — `10-lifecycle-transition.preview-to-ga.request.json`. Envelope branch is `TransitionLifecycleState` (`control-plane-envelope.schema.json:137-184`); `fromState=draft`, `toState=active` — this is allowed-transition #1 at `spec/rspl/lifecycle-and-transition-semantics.md:65-72`. The surface label change `preview → general-availability` is recorded only in `metadata.northstarStage` updates; the AGRP state machine sees a single `draft → active` step.

12. **Registry persists the transition event** — `11-lifecycle-transition.preview-to-ga.event.json`. Standalone artifact validating against `lifecycle-transition.schema.json`; distinct from the wire request because Northstar persists transitions for audit replay.

13. **Attestation authority signs the evidence package** — `12-evidence-attestation.preview-to-ga.example.json`. No dedicated AGRP schema for this artifact today; the field shape comes from `spec/compliance/evidence-freshness-and-attestation.md:60-89`. The attestation references the transition's evidence (test results, security review, compatibility check) and is signed by the attestation authority's `attestorId`.

14. **Audit record for the transition** — `13-audit-record.transition.example.json`. The steward is named in `actor`; the operation is `TransitionLifecycleState`.

**Phase 4 — Adopter discovery surface.**

15. **Capability advertisement** — `14-capability-advertisement.example.json`. The registry's catalog-level advertisement listing `northstar/example-search-tool` as discoverable; the entry points at v2 (now `active`) as the recommended version. v1 remains in the lineage chain but is not surfaced as the recommended choice.

By the end of the walkthrough, v1 remains a draft pre-release lineage ancestor and v2 is the first generally available version of the tool. Adopters consuming the registry see v2 through the capability advertisement; auditors replaying the event log can reconstruct the full lineage and transition history from the bundle's persisted records.

## 8. Concrete artifacts (index)

The bundle at `examples/adaptations/northstar-tool-registry/` contains 15 JSON artifacts plus a `README.md` table-of-contents. Files use a two-digit step prefix (`00-` through `14-`) to enforce read-order; suffixes vary by file role (`.example.json` for standalone artifacts, `.request.json` / `.response.json` for envelope-wrapped wire messages, `.event.json` for registry-persisted events).

| # | File | Validates against | Walkthrough role |
|---|---|---|---|
| — | `README.md` | (markdown index — not counted) | Bundle table-of-contents |
| 0 | `00-tool-resource.v1.example.json` | `models/schemas/resource-entity.schema.json` | v1 initial creation |
| 1 | `01-register-resource-version.v1.request.json` | `control-plane-envelope.schema.json` (request branch) | publisher submits v1 |
| 2 | `02-register-resource-version.v1.response.json` | `control-plane-envelope.schema.json` (success branch) | registry's response |
| 3 | `03-registration-record.v1.example.json` | `models/schemas/registration-record.schema.json` | standalone view of v1's record |
| 4 | `04-audit-record.create.v1.example.json` | `models/schemas/audit-record.schema.json` | audit for v1 creation |
| 5 | `05-lineage-node.v1.example.json` | `models/schemas/lineage-node.schema.json` | v1 lineage (root, no parent) |
| 6 | `06-tool-resource.v2.example.json` | `resource-entity.schema.json` | v2 with capability change |
| 7 | `07-register-resource-version.v2.request.json` | envelope (request branch) | publisher submits v2 |
| 8 | `08-lineage-node.v2.example.json` | `lineage-node.schema.json` | v2 parented to v1 |
| 9 | `09-audit-record.update.v2.example.json` | `audit-record.schema.json` | audit for v2 registration |
| 10 | `10-lifecycle-transition.preview-to-ga.request.json` | envelope (`TransitionLifecycleState` request branch) | steward initiates promotion |
| 11 | `11-lifecycle-transition.preview-to-ga.event.json` | `models/schemas/lifecycle-transition.schema.json` | persisted transition event |
| 12 | `12-evidence-attestation.preview-to-ga.example.json` | `spec/compliance/evidence-freshness-and-attestation.md:60-89` (no schema; prose-defined shape) | evidence backing GA promotion |
| 13 | `13-audit-record.transition.example.json` | `audit-record.schema.json` | audit for the transition |
| 14 | `14-capability-advertisement.example.json` | `models/schemas/capability-advertisement.schema.json` | discovery surface post-promotion |

The bundle's `README.md` mirrors this index in adopter-friendly form and is the recommended entry point when reading the bundle without this design doc open.

## 9. Implementation-defined edges

This adaptation makes a number of decisions that AGRP leaves to implementations. Each one is a place where a real adopter mapping could legitimately diverge from Northstar without losing conformance.

- **Surface stage names beyond AGRP's six.** Northstar names five surface stages (`development`, `preview`, `general-availability`, `deprecated`, `sunset`) where AGRP defines six baseline `lifecycleState` values. The two pre-release surface stages (`development`, `preview`) both map onto AGRP's `draft`. A different registry could use only AGRP's baseline names, or could define a different surface vocabulary with a different mapping. Section 6 and the `northstarStage` metadata field are how Northstar carries the surface distinction without leaking it into AGRP state.

- **`lifecycleState` vs `registrationStatus` reconciliation.** Northstar chooses to set `registration-record.status` to `active` for draft versions (the record is current/valid) while the version's `lifecycleState` remains `draft`. ADR 0001 (`docs/decisions/0001-control-plane-statusfilter-resolution.md`) is the supporting context for this distinction; the underlying schema constraints are at `models/schemas/common.schema.json:16-25` (`registrationStatus`) and `:26-36` (`lifecycleState`). A registry that filters its `StatusFilter` differently could legitimately make different choices here.

- **OCI-URI shape for `implementationRef`.** Northstar uses `oci://registry.northstar.example/tools/example-search-tool@sha256:<digest>`. The `resource-entity` schema accepts any non-empty string or an objectMap (`resource-entity.schema.json:16-26`); `spec/rspl/core-resource-model.md:80-82` lists "artifact digest, import path, endpoint, or packaged asset reference" as valid shapes. An adopter using a different distribution channel (npm, Helm, an HTTP endpoint, an in-repo path) would pick a different `implementationRef` shape.

- **Single-actor vs multi-actor modeling.** Northstar names one `actor` per audit and transition record. A registry that records joint approvals (e.g., two stewards co-signing a promotion) could either split the workflow into two transitions or extend the audit-record `metadata` with secondary signers. This walkthrough does not exercise either approach.

- **Attestation scope.** Northstar attaches one evidence-attestation to the GA promotion. Northstar could model separate security, compatibility, and load-test attestations, but this walkthrough keeps them together.

- **Version-string format.** Northstar uses semver. The schema constrains only that `versionId` be a non-empty string; calendar-versioning, monotonic integers, or content-digest-as-version are equally schema-valid choices.

These choices are the ones an adopter is most likely to encounter when mapping their own system. Section 11 lists what this adaptation does *not* exercise at all.

## 10. Conformance posture

A real Northstar implementation could make the following conformance claim against AGRP v1:

- **Baseline-conformance claim** (`spec/conformance/baseline-conformance.md:123-130`): the registry honors the resource-entity, registration-record, lineage-node, audit-record, lifecycle-transition, and capability-advertisement schemas; supports the `RegisterResourceVersion` and `TransitionLifecycleState` control-plane operations; and persists evidence attestations matching the field shape at `spec/compliance/evidence-freshness-and-attestation.md:60-89`. The four claim elements at lines 123-130 (semantic alignment, schema compatibility, lifecycle/lineage/restore/audit preservation, transport-neutral contract preservation) are each demonstrated by the bundle: schema-valid artifacts, lineage chain v1 → v2, audit records at each step, and JSON-on-the-wire envelopes that are transport-neutral.

- **Profile claim** (`spec/compliance/compliance-and-readiness-profiles.md:45-55`): a readiness profile is "a named set of additional operational expectations" — observability, diagnostics, rollout discipline, deprecation communication, governance transparency. A Northstar implementation modeled on this adaptation would target a profile covering single-tool registration, draft → active promotion with attestation, and capability-advertisement publication. Profiles covering supersession, deprecation, conflict resolution, and multi-binding scenarios are out of scope for this adaptation; an implementation claiming those profiles would need to demonstrate the corresponding artifacts and walkthroughs.

- **Bindings**: this adaptation does not pin a transport binding. The artifacts are JSON-on-the-wire shapes; an implementation can transport them over HTTP, gRPC, message-queue, or any other binding without affecting the AGRP-side conformance claim. Where binding-specific concerns arise (idempotency tokens, transport-level retries, authentication), they live below the AGRP control-plane layer.

The conformance vectors at `examples/conformance-vectors/` are the machine-checkable complement to this human-readable walkthrough; this adaptation is explanatory material, not an additional conformance requirement.

## 11. Gaps and limitations

This adaptation deliberately limits its scope so the demonstration can be complete on a narrow path. The following AGRP surfaces are **not** exercised here:

- **Multiple tools.** Only `northstar/example-search-tool` is registered. A multi-tool registry would surface inter-tool dependency and capability-overlap concerns that a single-tool walkthrough cannot show.
- **Supersession.** v2 promotes alongside v1; v1 is not marked superseded. A supersession walkthrough would exercise the `superseded` lifecycle state and the `superseded-by` lineage edge.
- **Conflict resolution.** No conflicting registrations, version collisions, or contested transitions are demonstrated.
- **Deprecation and sunset.** v2 stops at `active`. A full lifecycle walkthrough would continue through `deprecated` and `archived` (Northstar's `deprecated` and `sunset` surface stages), exercising the `deprecate` and `archive` transitions.
- **Multi-binding.** Only the JSON-on-the-wire shapes are shown; no transport binding is exercised.
- **Attestation-failure paths.** The single attestation in this walkthrough succeeds. A full demonstration would also show what happens when an attestation is missing, expired, or rejected — and how the registry refuses or rolls back the corresponding transition.
- **Capability-advertisement evolution.** Only the post-GA advertisement is shown. Pre-promotion advertisement, deprecation notices, and superseded-version handling are not demonstrated.

Each of these is appropriate territory for a follow-up adaptation. A second adaptation focused on multi-tool supersession would, for example, exercise the lineage-chain and superseded-by surfaces that this walkthrough does not. The maintainer's call at the time of authoring was to ship one complete narrow walkthrough rather than a broader-but-shallower demonstration.

## 12. How to read this example

**Reading order**:

1. Skim section 1 (Status) and section 2 (Overview) for context.
2. Read section 7 (End-to-end walkthrough) — this is the main act. Have the bundle directory open alongside; click into each artifact file as the walkthrough names it.
3. Refer back to sections 3-6 (system shape, roles, resource model, lifecycle stages) when the walkthrough surfaces a mapping decision you want to understand.
4. Read sections 9-11 (implementation-defined edges, conformance posture, gaps) once the walkthrough is clear; these explain *why* Northstar made the choices it made and *what is not* demonstrated.

**Prerequisites**: familiarity with the AGRP v1 spec corpus (resource model, registration, lineage, lifecycle, capability advertisement, evidence and attestation). This adaptation does not re-explain the spec; it shows one disciplined mapping against it.

**Relationship to other repository material**: the conformance vectors at `examples/conformance-vectors/` exercise machine-checkable edge cases; this adaptation exercises a human-readable end-to-end narrative. The `adopters/` directory holds mappings against named real-world systems. This Northstar adaptation is intentionally synthetic — it lives at `docs/adaptations/` and `examples/adaptations/` rather than `adopters/` because the system is fictional.
