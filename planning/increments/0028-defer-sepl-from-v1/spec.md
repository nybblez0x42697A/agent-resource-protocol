---
increment: 0028-defer-sepl-from-v1
title: Defer SEPL From v1
---

# Feature: Defer SEPL From v1

## Overview

Make it explicit that self-evolution protocol work is outside the `ARP v1` standard boundary and remains a future protocol area rather than an implied part of the initial release.

## User Stories

### US-001: Defer SEPL from ARP v1
**Project**: agent-resource-protocol

**As a** protocol author, implementer, or evaluator
**I want** the repository to say explicitly that `SEPL` is not part of `ARP v1`
**So that** the initial release boundary is clear and no adopter assumes self-evolution semantics are already standardized in `v1`

**Acceptance Criteria**:
- [x] **AC-US1-01**: The repo defines `SEPL` as a deferred or future protocol area rather than part of `ARP v1`
- [x] **AC-US1-02**: The repository charter and spec index are updated so the `v1` boundary and the deferred `SEPL` area do not conflict
- [x] **AC-US1-03**: The repo clarifies that future `SEPL` work must be introduced through a later normative release rather than implied by the current repository structure
