# Agent Resource Protocol

A neutral protocol/spec workspace for versioned agent resources, lifecycle-managed control-plane interfaces, and self-evolution operator contracts.

## Why this repository exists

This work lives in its own repository because the goal is to design a protocol that can stand on its own instead of inheriting the assumptions of any single runtime.

Starting separately is the cleaner choice than contributing directly into the existing SkyworkAI/DeepResearchAgent repository because:
- that repository began as a hierarchical multi-agent runtime and only later evolved into protocol language
- its abstractions are already shaped by one implementation history and one concrete codebase
- a protocol effort needs neutral terminology, explicit boundaries, and space to define what is normative versus what is implementation-specific
- the protocol should be able to compare against existing systems without being silently controlled by one of them

This repository treats existing implementations and papers as inputs and reference points, not as the source of truth by default.

## Scope

This repository is for:
- protocol charter and glossary
- normative spec drafts
- formal models and schemas
- non-normative examples
- adopter mappings kept outside the core spec

This repository is not for:
- embedding a specific runtime as the protocol definition
- product-specific adapters in the core spec folders
- implementation-first design that backfills protocol language afterward

## Layout

- `docs/`
  - `papers/`: paper analysis and extraction notes
  - `glossary/`: neutral terminology and mappings
  - `decisions/`: protocol design records
- `spec/`
  - `charter/`: mission, scope, non-goals
  - `rspl/`: resource-substrate protocol drafts
  - `sepl/`: self-evolution protocol drafts
  - `control-plane/`: operations and interfaces
  - `deployment/`: shared/external deployment design
- `models/`
  - `resource-model/`: resource/entity definitions
  - `lifecycle-model/`: state transitions and lifecycle rules
  - `lineage-model/`: versioning, rollback, and history
  - `operator-model/`: Reflect/Select/Improve/Evaluate/Commit contracts
  - `schemas/`: machine-readable schemas
- `examples/`
  - non-normative examples only
- `adopters/`
  - templates and future adopter mappings kept out of the core spec
- `planning/`
  - committed planning increments and associated artifacts for the protocol effort

## Initial Increment Order

1. `0001-repo-charter-and-scope`
2. `0002-agp-paper-decomposition`
3. `0003-glossary-and-neutral-terminology`
4. `0004-rspl-core-resource-model`
5. `0005-registration-record-and-lineage-model`

## Upstream References

The protocol work here should study existing systems without letting them define the spec by default:
- `Autogenesis: A Self-Evolving Agent Protocol` (`2604.15034`)
- `AgentOrchestra` (`2506.12508`)
- `SkyworkAI/DeepResearchAgent` as a reference implementation lineage
