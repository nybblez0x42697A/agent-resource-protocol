# Core Resource Model

## Purpose

This document mirrors the normative RSPL core resource model in a compact model-oriented form for later schema work.

Normative meaning lives in `spec/rspl/core-resource-model.md`. This file is a formal companion artifact.

## Baseline Resource Kinds

```yaml
baselineResourceKinds:
  - prompt
  - agent
  - tool
  - environment
  - memory
```

## Shared Entity Shape

```yaml
resourceEntity:
  resourceKind:
    category: identity
    required: true
    extensionAllowed: true
  resourceId:
    category: identity
    required: true
  versionId:
    category: identity
    required: true
  implementationRef:
    category: evolvableState
    required: true
  interfaceRef:
    category: evolvableState
    required: true
  config:
    category: configuration
    required: true
  state:
    category: evolvableState
    required: true
  metadata:
    category: metadata
    required: true
  extensions:
    category: extension
    required: false
```

## Category Rules

```yaml
categoryRules:
  identity:
    purpose: stable resource and version identity
    fields:
      - resourceKind
      - resourceId
      - versionId
  configuration:
    purpose: parameterization without changing logical identity
    fields:
      - config
  metadata:
    purpose: descriptive or administrative context
    fields:
      - metadata
    constraints:
      - mustNotRedefineCoreSemantics
  evolvableState:
    purpose: state that may change across reviewed versions
    fields:
      - implementationRef
      - interfaceRef
      - state
  extension:
    purpose: provisional or adopter-specific additions
    fields:
      - extensions
    constraints:
      - mustNotRedefineMandatoryFields
      - mustNotBeRequiredForBaselineInteroperability
```

## Per-Kind Emphasis

```yaml
kindProfiles:
  prompt:
    emphasizes:
      - implementationRef
      - state
      - config
  agent:
    emphasizes:
      - interfaceRef
      - config
      - state
  tool:
    emphasizes:
      - interfaceRef
      - config
      - implementationRef
  environment:
    emphasizes:
      - config
      - implementationRef
  memory:
    emphasizes:
      - state
      - interfaceRef
```

## Notes For Later Schemas

- `resourceKind` is extensible but baseline interoperability starts with the five baseline kinds.
- `extensions` is the only top-level provisional field in the shared entity shape.
- later schemas may refine nested field requirements by resource kind, but may not collapse the category boundaries defined here.
