---
increment: 0006-lifecycle-and-transition-semantics
title: Lifecycle and Transition Semantics
---

# Feature: Lifecycle and Transition Semantics

## Overview

Define lifecycle states, allowed transitions, restore transitions, and conflict rules for registered protocol resources.

## User Stories

### US-001: Define lifecycle and transition rules
**Project**: agent-resource-protocol

**As a** protocol architect
**I want** explicit lifecycle semantics for registered resources
**So that** create, update, deprecate, archive, restore, and conflicting transitions are safe and interoperable

**Acceptance Criteria**:
- [x] **AC-US1-01**: The design defines baseline lifecycle states and allowed transitions
- [x] **AC-US1-02**: The design defines restore and supersession transitions in operational terms
- [x] **AC-US1-03**: The design defines concurrency or conflict rules for competing transitions
