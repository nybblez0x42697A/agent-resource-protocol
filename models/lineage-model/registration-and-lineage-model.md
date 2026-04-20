# Registration And Lineage Model

## Purpose

This document mirrors the normative registration and lineage model in a compact model-oriented form for later schema work.

Normative meaning lives in `spec/rspl/registration-and-lineage-model.md`.

## Registration Record Shape

```yaml
registrationRecord:
  resourceId:
    required: true
    category: identity
  versionId:
    required: true
    category: identity
  resourceKind:
    required: true
    category: identity
  status:
    required: true
    category: registryStatus
    allowedValues:
      - active
      - deprecated
      - archived
      - superseded
      - restored
  implementationRef:
    required: true
    category: evolvableState
  interfaceRef:
    required: true
    category: evolvableState
  config:
    required: true
    category: configuration
  stateDigest:
    required: true
    category: integrity
  metadata:
    required: true
    category: metadata
  lineageRef:
    required: true
    category: lineage
  auditRef:
    required: true
    category: audit
  extensions:
    required: false
    category: extension
```

## Identity Rules

```yaml
identityRules:
  resourceId:
    stableAcrossVersions: true
    reusableForDifferentLogicalResource: false
    newIdRequiredFor:
      - forkedResourceWithNewLogicalIdentity
      - importedResourceWithNewLogicalIdentity
  versionId:
    uniqueWithinResourceId: true
    newVersionRequiredForMaterialChange: true
    restoreCreatesNewVersion: true
```

## Material Change Triggers

```yaml
materialChangeTriggers:
  - implementationRef
  - interfaceRef
  - semanticallyMeaningfulConfigChange
  - semanticallyMeaningfulStateChange
materialityDefault:
  uncertainChangesAreMaterial: true
```

## Lineage Node Shape

```yaml
lineageNode:
  resourceId:
    required: true
  versionId:
    required: true
  parentVersionId:
    required: false
  mutationType:
    required: true
    allowedValues:
      - create
      - update
      - restore
      - fork
      - import
  commitId:
    required: true
  createdAt:
    required: true
  changeSummary:
    required: true
  restoredFromVersionId:
    required: false
  supersedesVersionId:
    required: false
```

## History Rules

```yaml
historyRules:
  appendOnly: true
  priorVersionsMutableInPlace: false
  restoreErasesHistory: false
  restoreCreatesNewLineageNode: true
  importsAndForksPreserveProvenance: true
```

## Audit Record Shape

```yaml
auditRecord:
  commitId:
    required: true
  resourceId:
    required: true
  versionId:
    required: true
  action:
    required: true
    allowedValues:
      - create
      - update
      - restore
      - fork
      - import
  actor:
    required: true
  rationale:
    required: true
  evidenceRefs:
    required: true
  createdAt:
    required: true
```

## Restore Rules

```yaml
restoreRules:
  createsNewVersion: true
  requiresRestoredFromVersionId: true
  maySupersedeCurrentVersion: true
  mayDeleteInterveningVersions: false
  mayOverwriteHistoryInPlace: false
```
