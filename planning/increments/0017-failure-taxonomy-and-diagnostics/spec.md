---
increment: 0017-failure-taxonomy-and-diagnostics
title: Failure Taxonomy and Diagnostics
---

# Feature: Failure Taxonomy and Diagnostics

## Overview

Define a unified failure taxonomy and diagnostic model so protocol errors are categorized consistently and surfaced with actionable, bounded detail.

## User Stories

### US-001: Define unified failure taxonomy and diagnostics
**Project**: agent-resource-protocol

**As a** protocol implementer
**I want** a clear cross-cutting failure and diagnostics model
**So that** I can surface actionable errors consistently across security, negotiation, composition, and control-plane operations

**Acceptance Criteria**:
- [x] **AC-US1-01**: The repo defines a baseline failure taxonomy spanning validation, compatibility, policy, access, lifecycle, composition, and internal failures
- [x] **AC-US1-02**: The repo defines baseline diagnostic fields and disclosure rules for actionable but bounded error reporting
- [x] **AC-US1-03**: The repo includes non-normative examples showing a compatibility failure diagnostic and a bounded internal failure diagnostic
