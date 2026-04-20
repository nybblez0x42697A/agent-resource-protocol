# Lifecycle And Transition Semantics

## Purpose

This document mirrors the normative lifecycle and transition semantics in a compact model-oriented form for later schema and control-plane work.

Normative meaning lives in `spec/rspl/lifecycle-and-transition-semantics.md`.

## Lifecycle States

```yaml
lifecycleStates:
  - draft
  - active
  - deprecated
  - archived
  - superseded
  - restored
```

## Allowed Transitions

```yaml
allowedTransitions:
  draft:
    - active
    - archived
  active:
    - deprecated
    - superseded
  deprecated:
    - archived
    - active
  superseded:
    - archived
  archived: []
  restored:
    - active
```

## Activation Rules

```yaml
activationRules:
  singleActiveVersionPerResourceId: true
  activationSupersedesPreviousActive: true
```

## Restore Rules

```yaml
restoreRules:
  createsNewVersion: true
  createdLifecycleState: restored
  requiresRestoredFromVersionId: true
  requiresTransitionToActiveForSelection: true
  supersedesPreviousActiveWhenSelected: true
  inPlaceReactivationAllowed: false
  provenanceRemainsInLineageNotLifecycleState: true
```

## Conflict Rules

```yaml
conflictRules:
  optimisticConcurrency: true
  requiresExpectedBaseVersion: true
  staleBaseVersionMustFail: true
  competingTransitionsMayNotBothCommit: true
  retryRequiresNewAttempt: true
  perResourceCommitLinearization: true
```

## Invalid Transition Conditions

```yaml
invalidTransitionConditions:
  - unrecognizedStateTransition
  - staleExpectedBaseVersion
  - inPlaceRestoreAttempt
  - multipleSimultaneousActiveVersions
```
