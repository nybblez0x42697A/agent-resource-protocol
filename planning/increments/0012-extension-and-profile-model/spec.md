---
increment: 0012-extension-and-profile-model
title: Extension and Profile Model
---

# Feature: Extension and Profile Model

## Overview

Define baseline rules for protocol extensions and stricter profiles so implementations can evolve safely without redefining core semantics.

## User Stories

### US-001: Define extension and profile rules
**Project**: agent-resource-protocol

**As a** protocol implementer
**I want** clear rules for extensions and profiles
**So that** I can add capabilities or stricter requirements without fragmenting interoperability

**Acceptance Criteria**:
- [x] **AC-US1-01**: The repo defines baseline extension rules for fields, resource kinds, operations, and states
- [x] **AC-US1-02**: The repo defines how stricter profiles relate to baseline conformance and extension compatibility
- [x] **AC-US1-03**: The repo includes non-normative examples showing a valid extension and a valid stricter profile declaration
