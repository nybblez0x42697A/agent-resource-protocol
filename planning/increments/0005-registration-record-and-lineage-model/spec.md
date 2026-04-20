# Feature: Registration Record and Lineage Model

## Overview

Define versioned registration records, lineage, restore semantics, and rollback-safe history for protocol resources.

## User Stories

### US-001: Define resource registration and lineage
**Project**: agent-resource-protocol

**As a** protocol architect
**I want** a formal registration and lineage model
**So that** resources can be versioned, traced, restored, and audited safely

**Acceptance Criteria**:
- [ ] The design defines the registration record fields and version identity rules
- [ ] The design defines lineage, mutation history, and rollback semantics
- [ ] The design defines the minimum audit information required for commits and restores
