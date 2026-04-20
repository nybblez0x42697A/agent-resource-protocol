---
title: Repository Charter
charterVersion: 1.2.0
effectiveDate: 2026-04-20
---

# Repository Charter

## Purpose

This repository is the canonical specification workspace for the Agent Resource Protocol effort.

Its purpose is to define a neutral, implementation-independent protocol for describing, registering, inspecting, versioning, and evolving agent resources. The repository exists to make the protocol reviewable, portable, and implementable across multiple systems without binding the core design to any single runtime, product, or operating model.

## Mission

The mission of this repository is to:

- define the protocol's core concepts, terms, and boundaries
- publish normative protocol specifications and machine-checkable models
- separate protocol semantics from adopter-specific implementation choices
- provide non-normative examples that clarify intended usage without constraining implementations

## Audience

This repository serves:

- protocol authors defining shared semantics and conformance boundaries
- implementers building registries, control planes, runtimes, and tooling against the protocol
- reviewers assessing model clarity, versioning semantics, and evolvability guarantees
- adopters mapping the protocol into concrete systems without rewriting the core standard

## Repository Scope

In scope for this repository:

- protocol charter, glossary, and architectural decisions
- normative protocol specifications under `spec/`
- formal models and schema artifacts under `models/`
- non-normative examples under `examples/`
- adopter mappings under `adopters/`, provided they remain outside the core specification

Out of scope for this repository:

- production services, registries, SDKs, or deployment automation
- adopter-specific product architecture presented as protocol requirements
- implementation lock-in to a single paper, vendor, runtime, or control-plane design
- reference code treated as normative unless the specification explicitly says so

## Repository Taxonomy

The top-level repository structure expresses artifact ownership and must be interpreted consistently:

- `spec/`: normative protocol text and protocol-area drafts
- `spec/charter/`: the repository charter and other root protocol-governance documents
- `spec/decisions/`: decision records that are normative only when they establish or amend mandatory protocol boundaries and are explicitly linked from applicable normative specifications
- `spec/sepl/`: reserved future protocol area for self-evolution semantics and not part of `AGRP v1` unless a later release explicitly adds normative artifacts from it
- `models/`: formal models, schemas, and machine-readable artifacts derived from the protocol
- `docs/`: supporting analysis, decisions, glossary work, and background material that informs but does not define the protocol unless explicitly incorporated
- `examples/`: illustrative, non-normative examples of payloads, flows, and deployment shapes
- `adopters/`: adopter-specific mappings, profiles, or adaptation templates that must not redefine the core protocol

This structure is not just organizational. It is part of the repository's boundary discipline. Material should be placed where its authority is obvious from its location.

## Normative And Non-Normative Boundaries

The repository distinguishes between material that defines the protocol and material that only explains or illustrates it.

Normative content:

- files under `spec/`
- machine-readable definitions under `models/` when explicitly referenced by the specification as authoritative
- decision records under `spec/decisions/` that define mandatory protocol boundaries or interpretation rules and are explicitly incorporated by normative specifications

Non-normative content:

- files under `docs/` unless explicitly incorporated by a normative specification
- files under `examples/`
- adopter mappings under `adopters/`
- research notes, paper decompositions, and exploratory analysis

If prose in a non-normative document conflicts with `spec/`, the `spec/` document wins. If a machine-readable model in `models/` conflicts with normative prose, the conflict must be resolved explicitly by updating the relevant normative specification rather than inferred ad hoc.

If two normative documents under `spec/` conflict, the more specific document wins only when it explicitly scopes or amends the more general rule. Otherwise, the conflict must be resolved by updating the affected normative documents rather than relying on implication, document age, or local interpretation.

## Core Neutrality Rules

The protocol must remain neutral with respect to any one implementation or source document.

The following rules apply:

1. Core protocol terms must describe transferable semantics rather than product-specific mechanisms.
2. A paper, reference architecture, or adopter implementation may inspire the protocol, but it does not define the protocol by default.
3. Adopter-specific names, workflows, and assumptions must stay outside the core unless they can be stated as general protocol concepts.
4. Optional extensions must be labeled as provisional or adopter-specific rather than blended into mandatory core semantics.
5. Examples may illustrate one implementation style, but they must not silently redefine the standard.

## Terminology Policy

This repository may draw from historical papers or reference-system terminology, but source vocabulary is not automatically elevated to protocol vocabulary.

The following terminology policy applies:

- source-material terms are admissible as references, not as default protocol primitives
- stable repository terms must be defined in neutral language before they are treated as protocol concepts
- mappings from paper-specific terms into protocol terms should be explicit and reviewable
- terms that remain meaningful only inside one source system should stay in analysis or adopter material rather than the core specification

The canonical location for stable term definitions is the normative glossary once it exists. Until that glossary is established, provisional definitions must live in the relevant normative specification and be migrated into the glossary when the glossary is created.

## Anti-Drift Rules

To prevent the repository from collapsing into implementation-specific design, changes must follow these anti-drift constraints:

1. New terms must be introduced in neutral vocabulary before being used as protocol primitives.
2. Every normative addition must state whether it is required core behavior, an optional extension point, or a non-normative example.
3. If a concept only makes sense inside one reference system, it belongs in analysis, examples, or adopter mappings until generalized.
4. Control-plane, deployment, and operator behavior must be defined in terms of protocol-visible contracts, not internal architecture of one implementation.
5. When a paper-specific term is retained for traceability, it must be mapped to the repository's stable terminology rather than adopted uncritically.

## Expected Outputs

This repository should converge on:

- a stable glossary for protocol terms
- a core resource model
- registration, lineage, restore, and audit semantics
- control-plane and deployment specifications layered on top of the core model
- machine-checkable schemas and example payloads derived from the normative documents

For `AGRP v1`, these expected outputs do not include a standardized self-evolution layer. `SEPL` remains a future protocol area until a later release explicitly adds it to the normative artifact set.

## Sequencing Discipline

Core protocol work should proceed in dependency order:

1. charter and scope
2. glossary and neutral terminology
3. core resource model
4. registration and lineage semantics
5. control-plane and deployment layers built on top of the stabilized model

This sequencing exists to keep later protocol layers from importing undefined terms or adopter-specific assumptions into the core.

## Expansion Discipline

New protocol areas should enter the repository only when they can be stated as general, cross-adopter concerns.

A proposed addition belongs in the core only if it:

- extends the shared protocol model rather than one implementation architecture
- can be described in neutral terminology
- has a clear relation to existing normative boundaries
- can be represented in both prose and machine-checkable artifacts when appropriate

If those conditions are not met, the material should start life as analysis, example content, or adopter-specific guidance instead of core protocol text.

## Change Discipline

Changes to this repository should preserve the separation between semantics and implementation.

When proposing a change, authors should be able to answer:

- what protocol problem is being solved
- whether the change is normative or non-normative
- whether the concept is general across adopters
- what existing term or boundary the change extends or modifies
- whether the same result could be achieved with a narrower example or adopter mapping instead

## Governance And Amendments

This charter is itself normative and may be amended only through an increment that explicitly identifies the charter change, the reason for the change, and the affected normative boundaries.

An amendment is acceptable only when it:

- preserves or clarifies repository neutrality and boundary discipline
- resolves a demonstrated ambiguity, conflict, or governance gap
- states whether existing specifications or models must be updated to remain aligned

Charter amendments require explicit reviewer approval in the same way as other normative protocol changes. A change must not be treated as adopted merely because related implementation work exists or because adjacent documents imply the same outcome.

At least two reviewers must approve a substantive charter amendment before it is considered accepted. If a separate governance policy later defines a stricter quorum or review window, that policy supersedes this minimum.

## Charter Versioning

This charter governs the repository from its effective version forward.

- the charter version must be recorded in the document metadata or frontmatter
- any substantive charter amendment must increment that version
- normative specifications may reference the governing charter version when the repository needs to make compatibility or interpretation boundaries explicit

Until a separate versioning policy exists, the charter uses semantic versioning in `major.minor.patch` form.

- increment `major` for incompatible changes to governance, normative authority, or repository taxonomy
- increment `minor` for substantive additions or clarifications that preserve existing charter meaning
- increment `patch` for editorial fixes that do not change normative meaning

The charter version must change whenever governance, normative authority, taxonomy, or anti-drift rules materially change.

## Non-Goals

This repository does not attempt to:

- standardize one complete product architecture
- bless one registry or runtime as the canonical implementation
- encode every possible operational workflow in the first version of the protocol
- optimize for one deployment substrate at the expense of protocol portability
- turn research source material into normative text without explicit design review
