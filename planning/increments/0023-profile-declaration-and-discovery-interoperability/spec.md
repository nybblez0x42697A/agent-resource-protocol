---
increment: 0023-profile-declaration-and-discovery-interoperability
title: Profile Declaration and Discovery Interoperability
---

# Feature: Profile Declaration and Discovery Interoperability

## Overview

Define a minimum interoperable declaration model for readiness profiles and standard discovery signaling for fully supported, in-progress, and planned profile states across different stewards.

## User Stories

### US-001: Define interoperable profile declarations and discovery signaling
**Project**: agent-resource-protocol

**As a** protocol implementer, catalog operator, or ecosystem steward
**I want** a minimum interoperable readiness profile declaration model and standardized discovery states
**So that** readiness profile claims and adoption progress can be exchanged consistently across tools, registries, and organizations

**Acceptance Criteria**:
- [x] **AC-US1-01**: The repo defines minimum required metadata fields for interoperable readiness profile declarations
- [x] **AC-US1-02**: The repo defines standard readiness signaling states for fully supported, in-progress, planned, deprecated, and replaced profile declarations
- [x] **AC-US1-03**: The repo defines conflict-handling guidance for similar identifiers across different stewards and replacement workflow guidance for superseded profiles
- [x] **AC-US1-04**: The repo includes non-normative examples showing an interoperable profile declaration and a discovery advertisement that distinguishes support states
