# Autogenesis AGP/AGS Decomposition

## Purpose

This memo decomposes the paper *Autogenesis: A Self-Evolving Agent Protocol* into:

- protocol-core claims that may be reusable in a neutral standard
- AGS-specific assumptions or implementation choices that should not be treated as protocol requirements
- underspecified areas that need fresh protocol design work in this repository

This document is a non-normative paper-analysis artifact under `docs/papers/`. It informs later protocol increments but does not define the protocol.

## Source

- Paper: *Autogenesis: A Self-Evolving Agent Protocol*, arXiv:2604.15034, April 16, 2026
- Primary claims reviewed from the abstract, protocol sections, resource definitions, and protocol comparison appendix

## Executive Read

The paper contributes a useful framing: self-evolving agent systems need protocol support for resource identity, lifecycle, mutation safety, lineage, rollback, and operatorized improvement loops. That framing is reusable.

The paper also mixes protocol ideas with one reference-system architecture. In particular, the AGS multi-agent runtime, infrastructure managers, benchmark story, and some operator details are examples of how a system might use the protocol, not proof that the protocol must standardize those choices.

The repository should therefore extract RSPL and SEPL as candidate protocol layers, then restate them in neutral vocabulary without inheriting AGS architecture or paper-specific assumptions by default.

## Protocol-Core Concepts

The following claims appear suitable for protocol-core treatment, subject to neutral restatement and later specification work.

### 1. Resource Externalization

Prompts, agents, tools, environments, and memory are treated as explicit resources rather than opaque internal agent wiring. The reusable protocol idea is not the exact set of five forever, but the principle that evolvable agent components should be externally identifiable and managed through protocol-visible contracts.

Why it is reusable:

- it decouples agent policy from task-specific capability bundles
- it enables inspection, substitution, and controlled mutation across heterogeneous components
- it creates a stable substrate for versioning and lineage semantics

### 2. Resource Registration

The paper’s registration-record idea is protocol-relevant. A standard likely needs a canonical registration object for each managed resource, including identity, version, implementation reference, instantiation parameters, and exported interaction surfaces.

Why it is reusable:

- registries need a transportable unit of record
- mutation and rollback require concrete version identity
- interoperable control planes need a common representation of what is being managed

### 3. Lifecycle And State Management

The paper correctly identifies lifecycle control as a missing layer in invocation-centric protocols such as MCP and A2A. A reusable protocol claim is that managed resources need explicit lifecycle operations and state-access rules, not just invocation surfaces.

Why it is reusable:

- evolution-safe mutation depends on controlled create, update, instantiate, deprecate, and restore behavior
- audit and observability require protocol-visible state transitions
- lifecycle contracts are necessary even outside self-evolution scenarios

### 4. Version Lineage, Auditability, And Rollback

Version tracking, reversible change history, and auditable commits are core protocol concerns. This is one of the strongest transferable ideas in the paper.

Why it is reusable:

- unsafe mutation without rollback is operationally brittle
- audit trails are needed to explain why a resource changed and what it affected
- lineage semantics can be standardized independently of any one optimizer or runtime

### 5. Separation Of Substrate From Evolution Logic

The RSPL/SEPL split is reusable as a protocol design principle. A resource substrate layer can define what managed resources are and how they are addressed, while a higher layer can define how candidate changes are proposed, evaluated, and committed.

Why it is reusable:

- it prevents resource identity and mutation semantics from being coupled to one optimization algorithm
- it allows multiple improvement strategies to target the same managed substrate
- it aligns with this repo’s intended sequencing: resource model first, evolution/control semantics later

### 6. Operatorized Improvement Loop

The paper’s closed-loop operator framing is probably protocol-relevant at a high level. A protocol may need named phases or operations for observing traces, selecting targets, proposing changes, evaluating candidates, and committing accepted updates.

Why it is reusable:

- operator boundaries make self-evolution reviewable and auditable
- explicit phases support policy enforcement and safety checks
- different systems can implement the same operator contract with different internal methods

## AGS-Specific Or Reference-System Assumptions

The following items should be treated as paper or reference-system choices unless and until they are generalized.

### 1. The Exact Five-Entity Resource Set

The paper presents prompt, agent, tool, environment, and memory as a minimal substrate. That is a useful starting point, but not necessarily the final protocol taxonomy. The protocol should preserve extensibility rather than freezing the paper’s entity list as exhaustive truth.

### 2. The Exact Resource Tuple Shapes

Definitions such as the paper’s entity tuple and registration-record tuple are informative, but they are not yet protocol-ready schemas. They express design intent, not a reviewed standard.

Examples of paper-specific structure that should not be imported verbatim:

- the exact tuple field ordering
- the exact symbol set and mathematical notation
- the specific `g` trainable-marker encoding
- the exact decomposition of exported forms into `F`

### 3. AGS Runtime Architecture

The paper’s multi-agent runtime, planning agent, researcher agent, tool generator, browser agent, planner tool, dynamic managers, and tracer modules belong to the AGS reference system, not to the protocol core.

These may be valid adopters or examples, but the protocol should not assume:

- a specific orchestrator topology
- a specific set of specialized agents
- a specific planning artifact shape
- a specific control-plane module layout

### 4. Benchmark-Driven System Design

Performance claims on GPQA, AIME, GAIA, and LeetCode support the value of the approach, but benchmark outcomes are not protocol semantics. They should not influence normative resource or control-plane requirements directly.

### 5. Protocol Comparison Framing

The paper compares Autogenesis to A2A and MCP in a way that is directionally useful, but still authored from the paper’s perspective. The protocol repo should preserve the underlying gap analysis while avoiding overclaiming incompatibility or treating the appendix comparison table as normative evidence.

### 6. Specific Optimization Method Assumptions

The paper references reflection, proposal generation, evaluation, and commit loops, and situates them near particular optimization approaches. The protocol should define operator contracts and safety boundaries, not hard-code one optimizer family, reward model, or search strategy.

## Underspecified Areas Requiring New Protocol Design

These are the main places where the paper provides strong motivation but not enough detail for a protocol standard.

### 1. Canonical Identity Rules

The paper motivates versioned resources but does not fully specify:

- stable resource identifiers versus version identifiers
- namespace rules
- rename and alias behavior
- identity behavior across forks, imports, or migrations

This repo will need explicit identity and naming rules.

### 2. Registration Schema And Validation

The registration-record idea is strong, but the paper leaves open:

- required versus optional fields
- schema validation rules
- compatibility between implementation descriptors and exported interfaces
- integrity constraints across versions

This repo will need a concrete machine-checkable schema.

### 3. Lifecycle Operation Semantics

The paper argues for lifecycle control but does not fully define operation contracts such as:

- create versus register versus instantiate
- mutable versus immutable fields
- deprecate, disable, archive, and restore semantics
- concurrency and conflict handling for updates

These need protocol-level semantics, not just motivation.

### 4. Lineage And Rollback Semantics

The paper names lineage and rollback as core properties, but key details remain open:

- what exactly constitutes a commit
- what metadata is required for an auditable change
- how parent/child relationships are encoded
- whether rollback creates a new version or reactivates an old one
- how partial rollback or dependent-resource rollback should work

This repo will need explicit history and restore rules.

### 5. Operator Contracts For SEPL

The paper defines high-level operators, but a standard still needs:

- operator inputs and outputs
- preconditions and postconditions
- failure modes
- approval and policy gates
- safe interaction with registries and lifecycle controls

Without this, SEPL remains a conceptual loop rather than a protocol.

### 6. Trace And Observability Model

The paper treats traces and outputs as part of the evolvable state space, but does not precisely standardize:

- trace granularity
- retention policy
- privacy or redaction boundaries
- how traces reference resource versions and executions

This matters because traces become evidence for evaluation and change decisions.

### 7. Extension Model

The paper does not clearly define how additional resource kinds, custom metadata, or alternate operators extend the protocol without fragmenting interoperability. This repo will need an extension policy and compatibility story.

## Extraction Guidance For Later Increments

This decomposition should shape the next design increments as follows.

### For `0003-glossary-and-neutral-terminology`

Translate paper-native terms into neutral vocabulary and keep explicit mappings for:

- AGP
- AGS
- RSPL
- SEPL
- protocol-registered resource
- registration record
- evolvable variables

### For `0004-rspl-core-resource-model`

Keep the resource-substrate insight, but redesign the model neutrally:

- resource kinds should be explicit and extensible
- registration records should be schema-first
- lifecycle and exported interfaces should be formalized without assuming AGS internals

### For `0005-registration-record-and-lineage-model`

Lean heavily on the paper’s motivation, but specify what the paper leaves open:

- identity rules
- commit metadata
- lineage graph structure
- rollback semantics
- audit minimums

## Bottom Line

The paper is valuable mainly as a protocol motivation and decomposition source, not as a normative design to import whole.

The durable protocol contributions are:

- resources should be first-class, registered, and versioned
- lifecycle, lineage, auditability, and rollback belong in the protocol layer
- the managed substrate should be separated from the evolution loop

The parts that should remain non-normative or adopter-specific are:

- the AGS runtime architecture
- the exact entity set and tuple forms
- benchmark-driven system claims
- any optimizer-specific realization of the self-evolution loop
