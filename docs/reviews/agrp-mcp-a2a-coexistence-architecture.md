# AGRP, MCP, and A2A Coexistence Architecture

## Status

This document is non-normative.

It describes a deeply researched coexistence architecture for `AGRP`, `MCP`, and `A2A` grounded in:

- the current `AGRP v1.0.0` release boundary
- the current official `MCP` specification
- the current official `A2A` documentation and specification

Review date: 2026-04-21

## Design Question

If one deployed system wants:

- governed, versioned agent resources
- model-facing tool and context access
- agent-to-agent delegation and collaboration

where should `AGRP`, `MCP`, and `A2A` sit relative to one another?

## Short Answer

The most defensible current architecture is:

- use `AGRP` for managed resource identity, version lineage, lifecycle, restore, governance, conformance, and release claims
- use `MCP` for exposing tools, prompts, and resources to model applications and agent runtimes
- use `A2A` for delegation and collaboration between independently operating agents

In that architecture, `AGRP` is the resource-governance substrate, `MCP` is the capability-access protocol, and `A2A` is the inter-agent collaboration protocol.

## Why This Layering Is Defensible

### AGRP boundary

The current repo defines `AGRP v1.0.0` as:

- the `AGRP v1` artifact set
- explicitly excluding deferred areas such as `SEPL`
- centered on managed resources and their operational envelope

That means the current `AGRP` layer is strongest for:

- registration records
- lifecycle transitions
- lineage and restore behavior
- audit and observability anchors
- release and conformance boundaries

It is not yet a standardized self-evolution loop protocol.

### MCP boundary

The official `MCP` spec defines a protocol for:

- sharing contextual information with language models
- exposing tools and capabilities to AI systems
- using JSON-RPC between hosts, clients, and servers
- negotiating server and client capabilities

That makes `MCP` the natural protocol for:

- tool invocation
- prompt exposure
- resource access in model-facing applications
- session-level capability negotiation

### A2A boundary

The official `A2A` materials define a protocol for:

- communication and collaboration between AI agents
- task-centric interactions
- agent discovery through agent cards
- asynchronous and streaming interaction patterns

The A2A documentation also explicitly positions A2A and MCP as complementary:

- `MCP` for agent-to-tool communication
- `A2A` for agent-to-agent communication

That means `A2A` is the natural protocol for:

- delegation to remote agents
- federated agent collaboration
- exchanging task state and outputs

## Baseline Coexistence Architecture

### Components

The clean baseline architecture contains six logical layers:

1. User-facing application layer
2. Local agent runtime layer
3. `MCP` client and server integration layer
4. `A2A` collaboration layer
5. `AGRP` resource authority and control-plane layer
6. Underlying resource stores, audit systems, and governance data

### Responsibilities by layer

#### 1. User-facing application layer

Examples:

- chat UX
- IDE plugin
- workflow console
- operator dashboard

Responsibility:

- accept user requests
- display tool results, task progress, and approvals
- present trust and consent decisions where needed

Protocols:

- may speak directly to local orchestration services
- may host an `MCP` host component
- may invoke or monitor `A2A` tasks indirectly

#### 2. Local agent runtime layer

Examples:

- planner agent
- assistant agent
- coordinator runtime
- internal policy or review agent

Responsibility:

- decide whether to use local tools, ask remote agents, or consult governed resources
- coordinate execution flow
- translate user intent into protocol calls

Protocols:

- uses `MCP` to reach capabilities
- uses `A2A` to delegate to remote agents
- may use `AGRP` control-plane access to inspect or modify registered resources when its authority permits

#### 3. MCP client and server integration layer

Responsibility:

- expose tools, prompts, and contextual resources in a model-facing protocol
- negotiate what server and client features are available
- enforce consent and tool-safety flows at the application boundary

What belongs here:

- tool invocation
- prompt retrieval
- model-facing contextual resource access
- session-level feature negotiation

What does not belong here:

- canonical cross-version lineage semantics for managed resources
- release-boundary claims about protocol conformance
- durable restore semantics as a first-class governance rule

#### 4. A2A collaboration layer

Responsibility:

- let one agent discover another and delegate work
- exchange messages, task state, and output artifacts
- support asynchronous, streaming, or long-running collaboration

What belongs here:

- agent cards
- task creation and updates
- remote specialist invocation
- multi-agent coordination across trust boundaries

What does not belong here:

- canonical managed-resource registration
- shared audit lineage for resource versions
- protocol release-boundary semantics

#### 5. AGRP resource authority and control-plane layer

Responsibility:

- define and protect the managed-resource system of record
- provide versioned registration records
- control lifecycle transitions
- preserve lineage and restore rules
- support auditability, governance, and compliance semantics

What belongs here:

- `RegisterResourceVersion`
- `GetRegistrationRecord`
- `ListResourceVersions`
- `TransitionLifecycleState`
- `RestoreResourceVersion`
- `GetLineage`
- `GetAuditRecord`
- capability advertisement for `AGRP` bindings, profiles, extensions, operations, and resource kinds

What does not belong here today:

- standardized proposal and evaluation loops for self-evolution
- standardized operator phase orchestration
- a mandatory deployment or service topology

#### 6. Underlying stores and authority systems

Responsibility:

- persist resource versions
- persist audit records
- enforce organization-local policy and access controls
- host actual tools, prompts, and runtime assets

These are implementation concerns, not primary protocol surfaces.

## Recommended Interaction Pattern

### Pattern A: Managed local agent with remote delegation

This is the most realistic baseline coexistence pattern for the current repo.

Flow:

1. A user request enters the application.
2. A local coordinating agent decides whether to:
   - use an `MCP` tool or prompt
   - delegate a subtask over `A2A`
   - inspect or mutate a governed resource via `AGRP`
3. If the agent needs tool use or model-facing context, it uses `MCP`.
4. If the agent needs an independent remote specialist, it uses `A2A`.
5. If a tool, prompt, policy profile, or other governed asset needs lifecycle-aware inspection or update, the runtime consults the `AGRP` authority.
6. If a resource changes, `AGRP` records the new version, lineage, lifecycle effect, and audit link.
7. Observability and support references may correlate the user-visible interaction with governed resource changes, but the collaboration and tool layers remain distinct.

### Why this pattern works

It respects all three protocol boundaries:

- `MCP` handles access to capabilities
- `A2A` handles collaboration between agents
- `AGRP` handles durable resource governance

No protocol is forced to pretend to be another.

## Concrete Subsystem Mapping

### Example system

Imagine a multi-agent support platform with:

- one operator console
- one orchestrating support agent
- several specialist remote agents
- internal tool servers
- a governed registry of prompts, tools, and policy resources

### Mapping

#### MCP subsystem

Use `MCP` for:

- customer-data lookup tool
- case-history retrieval tool
- ticket-writing tool
- prompt templates for common support flows
- contextual resource reads needed by the local agent

#### A2A subsystem

Use `A2A` for:

- escalating to a billing specialist agent
- asking a diagnostics agent to run deep triage
- coordinating with an external vendor agent
- receiving asynchronous task updates from remote agents

#### AGRP subsystem

Use `AGRP` for:

- versioning the support prompt pack
- registering approved tool definitions as managed resources
- moving a prompt version from preview to active
- restoring an earlier prompt after a bad release
- auditing which governed version was active when a support incident occurred
- expressing compliance or readiness evidence about the managed-resource estate

## Handoff Points

### MCP to AGRP

An `MCP` server may expose a capability that is backed by an `AGRP`-governed resource.

Example:

- an `MCP` prompt may be served from the currently active `AGRP`-registered prompt version

Important boundary rule:

`MCP` exposure does not replace `AGRP` governance.

The prompt's durable identity, version history, restoreability, and lifecycle state still belong to the `AGRP` layer.

### A2A to AGRP

An agent collaborating over `A2A` may depend on governed resources.

Example:

- a remote agent reports a recommendation
- a local authority then decides whether to register a new governed prompt or tool version in `AGRP`

Important boundary rule:

`A2A` collaboration output is not itself a governed resource mutation until the `AGRP` authority accepts and records it through the control-plane semantics.

### A2A to MCP

A remote agent reached through `A2A` may itself use `MCP` internally.

That is consistent with the A2A documentation's own framing:

- agents can be equipped with `MCP`
- `A2A` then connects those agents to other agents

Important boundary rule:

`A2A` should not be modeled as a wrapper over `MCP`.

It is a collaboration protocol at a different layer.

## Common Misuse Patterns

### Mistake 1: Treating MCP resources as AGRP-managed resources by default

Why this is wrong:

- `MCP` resources are exposed protocol features in a client-server session
- `AGRP` managed resources are governed entities with lineage, lifecycle, and release-boundary meaning

Correct interpretation:

Some `MCP` resources may be backed by `AGRP` resources, but the two are not automatically identical.

### Mistake 2: Treating A2A task state as AGRP lineage

Why this is wrong:

- `A2A` task state tracks collaborative work progress
- `AGRP` lineage tracks the history of managed resource versions and restore-safe changes

Correct interpretation:

An `A2A` task may result in a recommendation or artifact that later becomes input to an `AGRP` resource update, but that does not make task state itself the resource-lineage system of record.

### Mistake 3: Treating AGRP as a replacement for either MCP or A2A

Why this is wrong:

`AGRP v1.0.0` currently does not standardize:

- model-facing tool and prompt session protocols at MCP depth
- agent-to-agent task exchange at A2A depth
- self-evolution orchestration at future `SEPL` depth

Correct interpretation:

`AGRP` is the governed substrate and policy layer, not the universal protocol for every agent interaction surface.

## Deployment Shapes

### Shape 1: Single organization, single authority

Characteristics:

- one organization runs the agent runtime, MCP servers, A2A gateway, and AGRP authority
- remote `A2A` collaboration may still happen, but most governed resources are local

Best use:

- enterprise agent platforms with strong internal governance requirements

### Shape 2: Federated agent ecosystem with local governance

Characteristics:

- agents collaborate across organizational boundaries with `A2A`
- each organization retains its own local `AGRP` authority for governed resources
- `MCP` remains local or selectively exposed depending on trust policy

Best use:

- ecosystems where agents need to collaborate but cannot share internal registries or resource stores

### Shape 3: Shared capability marketplace with governed release discipline

Characteristics:

- `MCP` servers expose tool and context capabilities to many clients
- `AGRP` governs the versioned definitions, policy states, and release progression of those capabilities
- `A2A` coordinates specialist agents that consume those capabilities

Best use:

- platforms that need both integration agility and strong release or rollback discipline

## What Current AGRP v1 Constrains

The current release boundary matters.

Because `SEPL` is deferred, this note must not claim that `AGRP v1.0.0` standardizes:

- proposal-generation protocols
- evaluator contracts
- operator phase choreography
- approval-gate workflows for self-improving agents
- autonomous commit loops

So the coexistence architecture today should treat:

- orchestration logic as an implementation concern
- remote task collaboration as `A2A`
- tool and context access as `MCP`
- governed durable resource semantics as `AGRP`

## What Future SEPL Could Add

If a later `SEPL` release is standardized, the coexistence picture would become richer.

Possible additions:

- standardized proposal artifacts generated from observations or traces
- evaluator result contracts
- approval-gate semantics for candidate changes
- operator phase handoffs between observing, selecting, proposing, evaluating, and committing

If that happens:

- `AGRP` would extend upward from governed resource substrate into standardized change-loop control
- some orchestration patterns now treated as implementation-local could become protocol-visible
- the handoff between `A2A` collaboration results and governed `AGRP` mutations could become more structured

Even then, `SEPL` still would not eliminate the need for:

- `MCP` as a capability access protocol
- `A2A` as a collaboration protocol

## Recommended Language

Use language like:

- `AGRP provides the governed resource substrate and lifecycle semantics.`
- `MCP provides model-facing capability access.`
- `A2A provides agent-to-agent collaboration.`
- `A deployed system may use all three together without collapsing their responsibilities.`

Avoid language like:

- `AGRP already subsumes A2A`
- `AGRP is a replacement transport for MCP`
- `A2A task flow is the same as AGRP resource lineage`
- `AGRP v1 already defines the autonomous improvement loop`

## Bottom Line

The right coexistence architecture today is layered, not competitive.

`AGRP v1.0.0` should be treated as the governed managed-resource substrate.

`MCP` should be treated as the capability-access protocol.

`A2A` should be treated as the agent-collaboration protocol.

That architecture is the most defensible reading of the current official sources and the current repo boundary.
