---
increment: 0025-compliance-precedence-and-integration-policy
title: Compliance Precedence and Integration Policy
---

# Feature: Compliance Precedence and Integration Policy

## Overview

Define how the compliance sub-specifications compose, which document wins when they overlap, and how consumers should move from baseline conformance through readiness, declaration interoperability, and resolution outcomes.

## User Stories

### US-001: Define compliance precedence and integration
**Project**: agent-resource-protocol

**As a** protocol implementer, evaluator, or catalog operator
**I want** explicit precedence and integration rules across the compliance sub-specs
**So that** I can apply the compliance model consistently without guessing which document governs a given readiness or declaration situation

**Acceptance Criteria**:
- [x] **AC-US1-01**: The repo defines the role of each compliance sub-spec and the order in which they should be applied
- [x] **AC-US1-02**: The repo defines precedence rules for overlapping concerns such as readiness claims, declaration validity, and resolution outcomes
- [x] **AC-US1-03**: The repo defines how resolution outcomes interact with baseline conformance and readiness support claims
- [x] **AC-US1-04**: The repo includes non-normative examples showing integrated compliance evaluation and a conflict case with explicit precedence
