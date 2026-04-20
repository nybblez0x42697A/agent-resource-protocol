---
increment: 0007-machine-readable-schemas
title: Machine-Readable Schemas
---

# Feature: Machine-Readable Schemas

## Overview

Turn the glossary, resource model, lifecycle model, and lineage model into machine-readable schema artifacts.

## User Stories

### US-001: Define baseline schemas
**Project**: agent-resource-protocol

**As a** protocol implementer
**I want** machine-readable schemas for core protocol objects
**So that** implementations can validate records and payloads consistently

**Acceptance Criteria**:
- [x] **AC-US1-01**: The schema set covers the core resource entity and registration record
- [x] **AC-US1-02**: The schema set covers lineage, audit, and lifecycle-related records
- [x] **AC-US1-03**: The schema set distinguishes mandatory fields from optional or extension fields
