# Protocol Glossary

## Purpose

This glossary defines stable protocol vocabulary for the repository.

It has three jobs:

- define the core neutral terms used by the protocol
- map paper-specific AGP/AGS vocabulary into those neutral terms where needed
- identify implementation-specific terms that must not be treated as core protocol language unless later generalized

## Core Protocol Terms

### Resource

A protocol-managed component with stable identity, explicit representation, and protocol-visible lifecycle semantics.

### Resource Kind

A protocol-level category of resource. Examples may include prompt, agent, tool, environment, and memory, but the protocol must treat resource kinds as an extensible taxonomy rather than a permanently closed paper-derived set.

### Managed Resource

A concrete resource instance that is registered, versioned, and addressable through protocol-defined structures.

### Registration Record

The canonical protocol record that describes a managed resource instance, including its identity, version reference, implementation reference, instantiation data, and exported interaction surfaces.

### Implementation Reference

A protocol-visible description of where the executable or interpretable form of a resource comes from. This may later be realized as source text, import path, artifact digest, endpoint, or other implementation locator, but the glossary term remains neutral.

### Exported Interface

A protocol-visible representation of how other components may inspect, invoke, configure, or reason about a managed resource.

### Resource Lifecycle

The set of protocol-defined state transitions and operational constraints governing how a managed resource is created, registered, instantiated, updated, deprecated, archived, restored, or otherwise changed over time.

### Version Identity

The protocol-level identifier for a specific revision or immutable state of a managed resource.

### Lineage

The recorded relationship between resource versions and mutations over time, including parentage, derivation, and restore history where applicable.

### Restore

A protocol-governed operation that returns a managed resource to an earlier approved state or reconstructs a new version from prior lineage.

### Audit Record

The minimum protocol-visible evidence associated with a resource change, evaluation, restore, or commit event.

### Trace Artifact

An execution-derived record, such as outputs, intermediate observations, or reasoning-related evidence, that may later inform evaluation or change decisions.

### Core Protocol Layer

The normative layer that defines managed resources, registration records, lifecycle semantics, identity, lineage, and other shared substrate rules that do not depend on a specific optimization or control strategy.

### Higher-Layer Protocol

A protocol layer built on top of the core protocol layer that adds operator workflows, evaluation policy, approval gates, or other evolution-control semantics.

### Evolution Loop

A higher-layer protocol pattern in which traces or observations are used to propose, assess, and potentially commit changes to managed resources.

### Operator Phase

A named stage in a higher-layer change loop, such as observing, selecting, proposing, evaluating, or committing. The exact operator set belongs to later specifications, but the glossary establishes the neutral category now.

### Policy Gate

A protocol-visible approval, validation, or safety boundary that must be satisfied before a change can advance from one operator phase to the next. Examples may include schema validation, policy review, evaluation thresholds, or explicit human approval.

### Extension Point

A place where the protocol explicitly allows additional resource kinds, metadata, operators, or profiles without redefining core semantics. Examples may include additional resource profiles, optional metadata blocks, or adopter-defined operator sets that preserve core contracts.

## AGP/AGS Mapping

The following mappings convert paper-native terms into stable repository terminology.

| Paper Term | Neutral Protocol Vocabulary | Mapping Notes |
| --- | --- | --- |
| AGP | protocol architecture | Use when referring to the paper’s overall proposed protocol framing; do not treat the paper name as a protocol primitive. |
| AGS | reference system | Use for the paper’s concrete multi-agent runtime and implementation shape. |
| RSPL | resource substrate layer | Use for the conceptual layer that defines managed resources and their protocol-visible contracts. |
| SEPL | evolution control layer | Use for the conceptual layer that governs proposal, evaluation, and commit behavior over managed resources. |
| protocol-registered resource | managed resource | The neutral term emphasizes protocol management rather than paper branding. |
| resource registration record | registration record | Keep the record concept, drop paper-specific phrasing. |
| resource entity | resource or resource kind | Use `resource` for instances and `resource kind` for type/category discussion. |
| evolvable variable set | changeable resource state | Use when discussing the portion of protocol-managed state that may be proposed for change under protocol rules. |
| trainable marker | mutability policy | The paper’s binary marker should be restated as a neutral policy or constraint, not inherited as exact structure. |
| context manager | reserved implementation term | Keep this out of core normative writing unless a later spec defines a generalized protocol role for it. |
| server-exposed interface | exported interface | Neutral term for the protocol-visible surface exposed to other participants. |
| closed-loop evolution | evolution loop | Preserve the loop idea without paper-specific branding. |
| reflect / select / improve / evaluate / commit | operator phases | Treat these as candidate named phases rather than final protocol keywords until later specs define them. |
| execution artifacts `y` | trace artifacts | Use when referring to outputs, traces, and similar evidence. |

## Reserved Implementation-Specific Terms

The following terms are reserved as source-paper or implementation-specific language. They should stay out of core normative writing unless later generalized and explicitly redefined.

### Paper Or Branding Terms

- Autogenesis
- AGP
- AGS

### Reference-System Architecture Terms

- planning agent
- deep researcher agent
- deep analyzer agent
- tool generator agent
- browser use agent
- reporter agent
- planning tool
- orchestrator topology

### Paper-Specific Infrastructure Terms

- version manager
- lifecycle manager
- dynamic manager
- model manager
- tracer module
- context manager

### Paper-Specific Formalism Terms

- entity tuple notation
- registration tuple notation
- `g` trainable marker
- `Vevo`
- `H`, `D`, `Z`, and similar paper-local symbol names when used as protocol primitives

## Usage Rules

When writing normative protocol text in this repository:

1. Prefer the core protocol terms in this glossary over paper-native names.
2. Use AGP/AGS names only when discussing source analysis, provenance, or adopter mappings.
3. Do not introduce implementation-specific architecture terms into core specs unless they are first generalized and added to this glossary.
4. If a later spec needs a new stable term, add it here before treating it as canonical protocol vocabulary.
