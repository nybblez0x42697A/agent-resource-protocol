---
increment: 0019-rollout-and-stage-policy
title: Rollout and Stage Policy
---

# Feature: Rollout and Stage Policy

## Overview

Define a baseline rollout and staged enablement policy for protocol artifacts so implementations can introduce new capabilities gradually without ambiguous compatibility behavior.

## User Stories

### US-001: Define rollout and stage rules
**Project**: agent-resource-protocol

**As a** protocol implementer
**I want** clear rollout and staging rules
**So that** I can expose preview, limited, and general availability behavior without inventing incompatible lifecycle or discovery signals

**Acceptance Criteria**:
- [x] **AC-US1-01**: The repo defines baseline rollout stages and their meaning for protocol artifacts
- [x] **AC-US1-02**: The repo defines how rollout stage interacts with discovery, profiles, deprecation, and compatibility claims
- [x] **AC-US1-03**: The repo includes non-normative examples showing a staged preview artifact and a generally available artifact after rollout completion
