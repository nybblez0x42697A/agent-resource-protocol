---
increment: 0011-security-and-policy-model
title: Security and Policy Model
---

# Feature: Security and Policy Model

## Overview

Define baseline security and policy responsibilities for protocol operations, including actor identity, authorization, policy evaluation, and auditable denial behavior.

## User Stories

### US-001: Define a baseline security and policy model
**Project**: agent-resource-protocol

**As a** protocol implementer
**I want** clear baseline rules for identity, authorization, and policy decisions
**So that** control-plane operations can be protected consistently without changing protocol semantics

**Acceptance Criteria**:
- [x] **AC-US1-01**: The repo defines a baseline actor and authorization model for control-plane operations
- [x] **AC-US1-02**: The repo defines how policy evaluation interacts with lifecycle and control-plane operations, including denial behavior
- [x] **AC-US1-03**: The repo includes non-normative examples for access denial and policy denial flows that align with the baseline error model
