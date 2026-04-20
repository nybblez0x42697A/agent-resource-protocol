---
increment: 0026-compliance-partial-failure-handling
title: Compliance Partial Failure Handling
---

# Feature: Compliance Partial Failure Handling

## Overview

Define how consumers handle mixed outcomes across the compliance stack when some layers succeed and others fail, remain unresolved, or produce incomplete evidence.

## User Stories

### US-001: Define compliance partial failure handling
**Project**: agent-resource-protocol

**As a** protocol implementer, evaluator, or catalog operator
**I want** explicit rules for mixed compliance outcomes across baseline, readiness, declaration validity, and resolution
**So that** I can report partial failures honestly without collapsing distinct failure modes into one misleading status

**Acceptance Criteria**:
- [x] **AC-US1-01**: The repo defines the main partial-failure scenarios across the compliance layers
- [x] **AC-US1-02**: The repo defines how consumers should summarize and preserve mixed outcomes without overstating readiness claims
- [x] **AC-US1-03**: The repo defines how incomplete or missing evidence interacts with otherwise valid claims
- [x] **AC-US1-04**: The repo includes non-normative examples showing mixed layer outcomes and the resulting consumer interpretation
