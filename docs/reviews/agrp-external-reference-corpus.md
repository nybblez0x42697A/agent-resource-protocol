# AGRP External Reference Corpus and Bibliography

## Status

This document is non-normative.

It captures the primary external references currently most relevant to the Agent Resource Protocol effort and explains how each source relates to the current `AGRP v1.0.0` boundary.

Review date: 2026-04-20

## Purpose

The repository already has a strong internal specification surface, but its explicit external source corpus is still thin.

This document exists to:

- identify the main external references that currently matter for protocol review
- distinguish seed input from adjacent protocols and implementation-adjacent ecosystem references
- explain whether each source is aligned with current `AGRP v1.0.0`, merely complementary, or more relevant to deferred `SEPL` work
- give future increments a clearer research backlog

## Source Categories

### 1. Seed Input

These sources directly motivated the original protocol effort.

### 2. Adjacent Protocol References

These are not the source of `AGRP`, but they define neighboring interoperability surfaces that `AGRP` should compare against carefully.

### 3. Implementation-Adjacent Ecosystem References

These sources describe practical agent harnesses, orchestration primitives, or tool-integration patterns that are relevant to protocol adoption and future `SEPL` design, but they are not themselves current conformance targets for `AGRP v1.0.0`.

## Reference Inventory

| Category | Source | Primary scope | Relationship to current AGRP scope | Priority |
| --- | --- | --- | --- | --- |
| Seed input | [Autogenesis: A Self-Evolving Agent Protocol](https://arxiv.org/abs/2604.15034) | Proposes `AGP` with `RSPL` and `SEPL`, versioned resources, lifecycle, lineage, rollback, and a self-evolution loop | Foundational input. `AGRP v1.0.0` substantially covers the substrate-side concerns, but intentionally does not standardize the `SEPL` loop yet | High |
| Seed input | [In-repo decomposition of Autogenesis](../papers/autogenesis-agp-decomposition.md) | Repository's own extraction of protocol-core claims, AGS-specific assumptions, and underspecified areas | Canonical internal bridge from the paper into the repo. This is not an external source, but it is the main traceability artifact currently linking the paper to implemented increments | High |
| Adjacent protocol | [Model Context Protocol specification](https://modelcontextprotocol.io/specification/) | Standardizes model and agent access to context, prompts, resources, tools, and related client or server features over MCP | Complementary, not substitutive. MCP is strongest on tool and context integration; `AGRP v1.0.0` is stronger on managed resource lifecycle, version lineage, restore, governance, and protocol release boundaries | High |
| Adjacent protocol | [Introducing the Model Context Protocol](https://www.anthropic.com/news/model-context-protocol) | Original launch framing for MCP as an open standard for connecting AI assistants to external systems | Useful historical framing for why MCP exists, but less authoritative than the current MCP spec for protocol comparison | Medium |
| Adjacent protocol | [A2A Protocol specification](https://a2a-protocol.org/dev/specification/) | Standardizes communication and task collaboration between independent agents, including agent cards, tasks, streaming, and async delivery | Complementary, not substitutive. A2A is strongest on peer-agent collaboration and task exchange; `AGRP v1.0.0` is strongest on managed resource identity, lifecycle, lineage, and compliance semantics | High |
| Adjacent protocol | [A2A appendix on relationship to MCP](https://a2a-protocol.org/dev/specification/) | Explicitly states that A2A and MCP solve different layers and can work together | Helpful reference for a three-way `AGRP` positioning exercise, because it already frames adjacent-layer complementarity instead of forced protocol replacement narratives | Medium |
| Implementation-adjacent | [OpenAI Agents SDK docs](https://developers.openai.com/api/docs/guides/agents) | Agent orchestration, handoffs, guardrails, observability, MCP integration, sandboxed execution, and agent workflow evaluation | Not a wire protocol and not a conformance peer to `AGRP v1.0.0`. Still relevant as an implementation-adjacent ecosystem reference for orchestration, tracing, approvals, and future `SEPL` discussions | Medium |
| Implementation-adjacent | [New tools for building agents](https://openai.com/index/new-tools-for-building-agents/) | Public overview of Agents SDK primitives including handoffs, guardrails, and tracing | Useful ecosystem framing, but secondary to the actual SDK docs. Supports future research around practical evolution-loop orchestration rather than current `AGRP v1.0.0` semantics | Low |

## Relationship Notes

### Autogenesis

Autogenesis remains the single most important seed source for the repository.

Its most durable contributions to the current repo are:

- managed resources as first-class protocol objects
- explicit lifecycle and version semantics
- lineage, rollback, and auditable commits
- separation of substrate concerns from self-evolution concerns

Its main unresolved contribution is `SEPL`.

That means Autogenesis is both:

- already reflected in the current `RSPL`-heavy `AGRP v1.0.0` surface
- still relevant for future work because the repository has intentionally deferred the standardized self-evolution layer

### Model Context Protocol

MCP is an adjacent tool and context integration protocol, not a managed-resource substrate protocol.

The current MCP specification describes:

- a JSON-RPC-based protocol
- hosts, clients, and servers
- server features like resources, prompts, and tools
- client features like sampling, roots, and elicitation
- explicit security and user-consent guidance

MCP is most relevant to `AGRP` in these ways:

- it is a strong comparison point for tool and resource exposure
- it demonstrates a successful modular capability-negotiation ecosystem
- it provides a real external reference for how agent systems expose usable capabilities without standardizing deep lifecycle and lineage semantics

MCP is less aligned with the current repo in these ways:

- it does not center version lineage, restore semantics, or resource governance the way `AGRP v1.0.0` does
- it is oriented toward live integration with model applications rather than toward canonical registration records and release-boundary discipline

### A2A

A2A is an adjacent peer-agent communication protocol, not a managed-resource registry protocol.

The current A2A specification centers:

- agent discovery through agent cards
- stateful tasks and task lifecycle
- message exchange, streaming, and asynchronous notifications
- peer collaboration between independent agents

A2A is most relevant to `AGRP` in these ways:

- it is a strong comparison point for task-oriented inter-agent workflows
- it provides a useful external model for collaboration semantics that do not require sharing internal implementation details
- it already positions itself as complementary to MCP, which makes it a useful anchor for a broader ecosystem comparison that also includes `AGRP`

A2A is less aligned with the current repo in these ways:

- it does not focus on registered resource versions, rollback-safe history, or restore semantics as the primary unit of standardization
- its core object is a stateful task, whereas `AGRP v1.0.0` is fundamentally organized around managed resources and their lifecycle

### OpenAI Agents SDK

The OpenAI Agents SDK is not a protocol peer in the same sense as MCP or A2A.

It is still relevant because it captures implementation-adjacent primitives that matter when thinking about future `SEPL` work:

- orchestration and handoffs
- guardrails and human review
- tracing and observability
- MCP integration
- sandboxed agent execution

Its relevance to the current repo is therefore mostly future-facing:

- it helps illustrate what practical agent control loops look like in deployed systems
- it reinforces that observability, approvals, and orchestrated handoffs are ecosystem-level concerns worth comparing against future `SEPL` work

It should not be treated as a normative source for `AGRP v1.0.0`.

## Current AGRP Scope Versus Reference Coverage

### Already Well Grounded

The current repo is already well grounded for:

- resource-substrate semantics
- identity, registration, lineage, rollback, and lifecycle management
- control-plane and binding design
- compliance and evidence layering
- release-boundary discipline

This grounding comes primarily from:

- the Autogenesis seed paper
- the repository's own neutralization and expansion of that seed material

### Only Partially Grounded

The current repo is only partially grounded externally for:

- observability and evaluation loops beyond the current compliance layer
- explicit ecosystem positioning relative to MCP and A2A
- the practical shape of future self-evolution operator workflows

### Not Yet Adequately Grounded

The current repo is not yet adequately grounded externally for:

- a deeper `SEPL` bibliography
- a structured comparison against multiple self-improving or agent-control-loop systems
- an explicit external research corpus for approvals, evaluators, or evolution-policy semantics

## Recommended Follow-On Review Order

### Priority 1

1. MCP versus AGRP comparison memo
2. A2A versus AGRP comparison memo

These would make the current `AGRP v1.0.0` position much clearer and reduce the risk of fuzzy “similar to MCP” or “similar to A2A” claims.

### Priority 2

1. `SEPL` candidate-source bibliography
2. comparative review of orchestration, evaluation, and approval-loop references

These are the sources most likely to matter once the repo moves beyond the `RSPL`-centered `v1` boundary.

### Priority 3

1. implementation-adjacent survey of agent harnesses and tracing systems
2. adoption-facing guidance showing how MCP, A2A, and `AGRP` may coexist in one system

These would help adoption and implementation clarity, but they are less urgent than the protocol-comparison and `SEPL`-research backlog.

## Bibliography

1. Wentao Zhang, *Autogenesis: A Self-Evolving Agent Protocol*, arXiv:2604.15034, submitted April 16, 2026. URL: <https://arxiv.org/abs/2604.15034>
2. Model Context Protocol, *Specification*, latest public specification site reviewed on April 20, 2026. URL: <https://modelcontextprotocol.io/specification/>
3. Anthropic, *Introducing the Model Context Protocol*, November 25, 2024. URL: <https://www.anthropic.com/news/model-context-protocol>
4. Agent2Agent Protocol, *Specification*, latest released version `1.0.0` visible on the public specification site reviewed on April 20, 2026. URL: <https://a2a-protocol.org/dev/specification/>
5. Agent2Agent Protocol, *Relationship to MCP (Model Context Protocol)* appendix within the public specification. URL: <https://a2a-protocol.org/dev/specification/>
6. OpenAI, *Agents SDK* developer docs, reviewed April 20, 2026. URL: <https://developers.openai.com/api/docs/guides/agents>
7. OpenAI, *New tools for building agents*, public product post. URL: <https://openai.com/index/new-tools-for-building-agents/>

## Bottom Line

The external reference corpus is now strong enough to support the next round of protocol review, but it is still not broad enough to claim a complete future-looking research base for `SEPL`.

Right now the repo has:

- one strong seed paper
- two strong adjacent protocol comparators
- one useful implementation-adjacent ecosystem reference family

That is enough to improve review quality immediately.

It is not yet enough to fully ground future self-evolution standardization work.
