---
increment: 0031-v1-schema-expansion
title: v1 Schema Expansion
---

# Feature: v1 Schema Expansion

## Overview

Expand machine-readable schema coverage beyond the original RSPL record set so the current `AGRP v1` protocol surface has stronger implementation anchors for operations, discovery, and compliance declarations.

## User Stories

### US-001: Add schemas for adoption-critical v1 surfaces
**Project**: agent-resource-protocol

**As a** protocol implementer or validator author
**I want** machine-readable schemas for newer `AGRP v1` surfaces beyond the original RSPL records
**So that** I can validate requests, advertisements, and declarations without reconstructing them only from prose

**Acceptance Criteria**:
- [x] **AC-US1-01**: The repo adds machine-readable schemas for control-plane envelopes, capability advertisements, and readiness/profile declarations
- [x] **AC-US1-02**: The new schemas are aligned to the corresponding normative specs and fit the existing `models/schemas/` structure
- [x] **AC-US1-03**: Public examples or sample artifacts validate structurally against the new schemas
