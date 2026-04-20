---
increment: 0032-conformance-vectors-and-negative-cases
title: Conformance Vectors And Negative Cases
---

# Feature: Conformance Vectors And Negative Cases

## Overview

Add a compact, executable conformance-fixture pack for `AGRP v1` so implementers have positive and negative examples that check schema validity and expected baseline failure outcomes.

## User Stories

### US-001: Publish executable conformance vectors
**Project**: agent-resource-protocol

**As a** protocol implementer or validator author
**I want** positive and negative conformance vectors with expected outcomes
**So that** I can verify baseline shapes and common failure cases without inferring test cases only from prose

**Acceptance Criteria**:
- [x] **AC-US1-01**: The repo adds a dedicated conformance-fixtures area with both valid and invalid vectors for baseline `AGRP v1` surfaces
- [x] **AC-US1-02**: Each vector records its expected outcome, including schema-valid success or expected failure class/category for negative cases
- [x] **AC-US1-03**: A local script can execute the vector pack and report whether the observed outcomes match the expected outcomes
