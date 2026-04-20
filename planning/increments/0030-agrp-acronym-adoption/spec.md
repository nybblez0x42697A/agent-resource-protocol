---
increment: 0030-agrp-acronym-adoption
title: AGRP Acronym Adoption
---

# Feature: AGRP Acronym Adoption

## Overview

Replace the protocol shorthand `ARP` with `AGRP` in the published protocol surface so the standard no longer collides with the established Address Resolution Protocol acronym.

## User Stories

### US-001: Adopt AGRP as the short protocol identifier
**Project**: agent-resource-protocol

**As a** protocol author, implementer, or evaluator
**I want** the published protocol materials to use `AGRP` instead of `ARP`
**So that** the protocol has a stable short identifier that does not collide with a dominant networking standard

**Acceptance Criteria**:
- [x] **AC-US1-01**: Normative protocol documents use `AGRP` as the short identifier for Agent Resource Protocol release, artifact-set, and deferral references
- [x] **AC-US1-02**: Public-facing example artifacts and release expressions use `AGRP` consistently
- [x] **AC-US1-03**: The repo preserves historical planning/workbench context where needed, but the published protocol surface no longer presents `ARP` as the current short name
