---
increment: 0015-deprecation-and-sunset-policy
title: Deprecation and Sunset Policy
---

# Feature: Deprecation and Sunset Policy

## Overview

Define how protocol artifacts are deprecated, what compatibility obligations remain during deprecation, and how sunset is communicated and completed.

## User Stories

### US-001: Define deprecation and sunset rules
**Project**: agent-resource-protocol

**As a** protocol implementer
**I want** clear deprecation and sunset rules
**So that** I can retire old artifacts predictably without surprising interoperable clients or services

**Acceptance Criteria**:
- [x] **AC-US1-01**: The repo defines baseline deprecation states and obligations for bindings, profiles, extensions, and capability identifiers
- [x] **AC-US1-02**: The repo defines baseline sunset expectations, notice requirements, and post-sunset behavior
- [x] **AC-US1-03**: The repo includes non-normative examples showing a deprecation notice and a completed sunset transition
