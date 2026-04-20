---
increment: 0014-versioning-and-evolution-policy
title: Versioning and Evolution Policy
---

# Feature: Versioning and Evolution Policy

## Overview

Define a unified versioning and evolution policy for protocol documents, bindings, profiles, extensions, and capability identifiers.

## User Stories

### US-001: Define unified versioning and evolution rules
**Project**: agent-resource-protocol

**As a** protocol implementer
**I want** a clear versioning and evolution policy
**So that** I can reason about compatibility, breaking changes, and upgrade paths across the protocol stack

**Acceptance Criteria**:
- [x] **AC-US1-01**: The repo defines baseline versioning rules for normative documents, bindings, profiles, extensions, and capability identifiers
- [x] **AC-US1-02**: The repo defines compatibility classes and evolution rules for additive, tightening, and breaking changes
- [x] **AC-US1-03**: The repo includes non-normative examples showing a compatible additive evolution and a breaking major-version evolution
