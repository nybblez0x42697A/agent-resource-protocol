---
increment: 0024-declaration-conflict-and-supersession-resolution
title: Declaration Conflict and Supersession Resolution
---

# Feature: Declaration Conflict and Supersession Resolution

## Overview

Define how catalogs and discovery systems resolve conflicting readiness declarations, malformed supersession chains, and ordering ambiguity when revision comparison alone is insufficient.

## User Stories

### US-001: Define declaration conflict and supersession resolution
**Project**: agent-resource-protocol

**As a** catalog operator, discovery consumer, or ecosystem steward
**I want** clear rules for resolving conflicting declarations and broken supersession chains
**So that** readiness profile state remains interpretable even when declarations are duplicated, malformed, or partially inconsistent

**Acceptance Criteria**:
- [x] **AC-US1-01**: The repo defines resolution rules for conflicting declarations published by the same steward for the same profile identity
- [x] **AC-US1-02**: The repo defines how consumers should treat malformed, circular, or unresolved supersession chains
- [x] **AC-US1-03**: The repo defines fallback ordering guidance when revision comparison alone cannot determine the current declaration
- [x] **AC-US1-04**: The repo includes non-normative examples showing a conflict case and an invalid supersession case
