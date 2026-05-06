# AGRP vs MCP vs A2A Comparison Memo

## Status

This document is non-normative.

It compares the current `AGRP v1.0.0` release boundary to the current public `MCP` and `A2A` specifications.

Review date: 2026-04-21

## Purpose

The goal of this memo is to make three distinctions clear:

1. `AGRP`, `MCP`, and `A2A` do not standardize the same layer.
2. They have some overlap, but they are more often complementary than interchangeable.
3. The current `AGRP v1.0.0` boundary is still centered on the managed-resource substrate rather than on a standardized self-evolution loop.

## Sources

### AGRP sources

- `spec/versioning/agrp-v1-release-definition.md`
- `spec/charter/agrp-v1-artifact-set.md`
- `spec/charter/sepl-v1-deferral.md`
- `spec/conformance/baseline-conformance.md`
- `spec/control-plane/control-plane-contracts.md`
- `spec/discovery/capability-discovery-and-negotiation.md`

### MCP sources

- Model Context Protocol specification: <https://modelcontextprotocol.io/specification/>
- Current MCP specification overview, revision `2025-06-18`: <https://modelcontextprotocol.io/specification/2025-06-18/basic/>
- Anthropic launch framing for MCP: <https://www.anthropic.com/news/model-context-protocol>

### A2A sources

- A2A specification overview: <https://a2a-protocol.org/dev/specification/>
- A2A project overview: <https://a2a-protocol.org/dev/>

## One-Sentence Positioning

- `AGRP`: a protocol for managed agent resources, their identity, lifecycle, lineage, governance, conformance, and release boundaries.
- `MCP`: a protocol for exposing tools, resources, prompts, and related capabilities between clients and servers in model-integrated applications.
- `A2A`: a protocol for communication and task collaboration between independent agents.

## Core Comparison Table

| Dimension | AGRP v1.0.0 | MCP | A2A |
| --- | --- | --- | --- |
| Primary problem | Standardizing managed resource semantics and operational governance | Standardizing access to tools, prompts, resources, and related context features for model applications | Standardizing collaboration between independent agents |
| Primary unit of standardization | Versioned managed resource and related control-plane artifacts | Client-server protocol messages and server or client features | Agent cards, tasks, messages, artifacts, and protocol bindings |
| Core interaction model | Resource registration, lifecycle control, lineage inspection, restore, policy, compliance, and release-boundary interpretation | JSON-RPC-based lifecycle plus negotiated client and server capabilities | Task-oriented agent-to-agent collaboration with async-first workflows |
| Current transport stance | One concrete HTTP JSON binding layered on transport-neutral contracts | JSON-RPC base protocol with multiple transports and current authorization guidance | Protocol-agnostic layered model with concrete bindings including JSON-RPC, gRPC, and HTTP/REST |
| Versioning center | Release-boundary, artifact-set, binding, extension, and profile versioning | Date-based protocol revisions with negotiated session version | Released protocol versions plus binding-specific mappings |
| Lifecycle depth | Strong: lifecycle transitions, restore, lineage, audit, rollback-safe history | Session lifecycle is strong; managed-resource lifecycle is not its primary focus | Task lifecycle is strong; managed-resource version lifecycle is not its primary focus |
| Discovery or capability model | Capability discovery for bindings, profiles, and extensions | Capability negotiation during initialization between clients and servers | Capability discovery via agent cards and negotiation of modalities |
| Current non-goal | Standardized self-evolution loop in `v1` | Managed-resource lineage, rollback, and release-governance semantics at AGRP depth | Managed resource registry semantics and release-boundary governance at AGRP depth |

## What Each Protocol Is Really Standardizing

### AGRP

`AGRP v1.0.0` standardizes a managed-resource substrate and its operational envelope.

Its center of gravity is:

- resource identity
- versioned registration records
- lifecycle transitions
- lineage and restore behavior
- auditability
- governance and namespace rules
- conformance and release-boundary clarity

That makes `AGRP` strongest where a system needs durable, reviewable semantics for resources that evolve over time.

### MCP

`MCP` standardizes a client-server integration protocol for model applications and external capabilities.

Its center of gravity is:

- session initialization and lifecycle
- capability negotiation
- exposure of tools, resources, and prompts
- client or server feature modularity
- transport-level interoperability

That makes `MCP` strongest where a model-enabled application needs a common wire protocol for using external context and tools.

### A2A

`A2A` standardizes agent-to-agent collaboration around tasks and exchanged information.

Its center of gravity is:

- agent discovery
- task creation and progression
- message exchange
- streaming and asynchronous work
- collaboration without exposing internal implementation details

That makes `A2A` strongest where multiple agents need to coordinate work across organizational or system boundaries.

## Where They Overlap

### AGRP and MCP

Overlap exists in these areas:

- both care about protocol-visible resources
- both care about capability surfaces rather than hidden internals
- both define negotiation or compatibility-relevant behavior
- both want interoperable, implementation-neutral contracts

But the overlap is limited.

`MCP` treats resources, prompts, and tools as exposed features in an interaction protocol.

`AGRP` treats managed resources as governed, versioned entities with lifecycle, lineage, and release-boundary semantics.

### AGRP and A2A

Overlap exists in these areas:

- both want cross-system interoperability without forcing one runtime architecture
- both are concerned with externally visible contracts rather than internal reasoning traces
- both can participate in larger agent ecosystems

But the overlap is also limited.

`A2A` is task-collaboration-first.

`AGRP` is resource-governance-first.

### MCP and A2A

These protocols are already explicitly framed by A2A as complementary.

That framing is directionally useful for `AGRP` too:

- `MCP` is good for tool and context access
- `A2A` is good for agent collaboration
- `AGRP` is good for governed, versioned resource management

## Where They Are Complementary

The cleanest way to think about the three protocols together is by layer.

### A practical layered picture

- `MCP` can expose usable tools, prompts, and contextual resources to an agent or host application.
- `A2A` can let independent agents delegate and collaborate on tasks.
- `AGRP` can provide durable semantics for the resources those systems register, version, restore, govern, and assess for compliance.

In that layered picture:

- `MCP` is not a substitute for `AGRP` lineage or restore rules
- `A2A` is not a substitute for `AGRP` resource identity or release-boundary rules
- `AGRP` is not a substitute for `A2A` task collaboration or for `MCP` tool invocation surfaces

## Where They Are Not Equivalent

### AGRP is not “MCP plus versioning”

That description understates the repo's scope.

`AGRP v1.0.0` also includes:

- release-boundary semantics
- governance and namespace stewardship
- compliance and readiness layers
- evidence freshness and attestation
- deployment topology and trust-boundary guidance

### AGRP is not “A2A for resources”

That description misses the protocol's emphasis on:

- canonical registration records
- lifecycle transitions
- append-only lineage
- restore as new-version creation
- artifact-set and release claims

### MCP and A2A are not “missing pieces of AGRP”

They target different primary surfaces:

- `MCP` centers integration with capabilities and context
- `A2A` centers inter-agent collaboration

Their existence does not imply that `AGRP` should absorb their scopes into `v1`.

## Current AGRP Position

The current repo should position `AGRP v1.0.0` as:

- a managed-resource protocol
- a resource-governance and lifecycle protocol
- a compliance and release-boundary protocol

It should not position `AGRP v1.0.0` today as:

- a replacement for `MCP`
- a replacement for `A2A`
- a complete self-evolving agent-loop standard

## Future SEPL Impact

The comparison may change if the repo later standardizes `SEPL`.

If future `SEPL` work defines:

- proposal artifacts
- evaluation semantics
- approval gates
- operator phases
- commit-selection behavior

then `AGRP` would move closer to parts of the practical orchestration space now occupied by agent harnesses and adjacent protocols.

Even then, `SEPL` would still not automatically make `AGRP` equivalent to `MCP` or `A2A`.

At most, it would make `AGRP` cover a broader portion of agent evolution and control semantics on top of its current substrate.

## Practical Guidance For Repo Language

Good positioning claims:

- `AGRP v1.0.0 standardizes governed, versioned agent-resource semantics and related operational policy layers.`
- `MCP and A2A are adjacent protocols that solve different interoperability layers.`
- `AGRP can be complementary to MCP-style capability exposure and A2A-style agent collaboration.`

Avoid these claims:

- `AGRP replaces MCP`
- `AGRP replaces A2A`
- `AGRP is just another agent messaging protocol`
- `AGRP v1 already standardizes self-evolving agent loops`

## Bottom Line

`MCP`, `A2A`, and `AGRP` belong in the same ecosystem conversation, but they do not currently standardize the same thing.

Today:

- `MCP` is primarily about model-facing capability integration
- `A2A` is primarily about agent-to-agent task collaboration
- `AGRP v1.0.0` is primarily about managed-resource lifecycle, lineage, governance, conformance, and release boundaries

That means the right default stance is complementarity with clear boundary discipline, not equivalence.
