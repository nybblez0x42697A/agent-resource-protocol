---
increment: 0022-profile-evolution-and-progressive-adoption
title: Profile Evolution and Progressive Adoption
---

# Feature: Profile Evolution and Progressive Adoption

## Overview

Define how readiness profiles evolve over time, how profile identifiers stay stable, and how implementations can communicate in-progress adoption without falsely claiming full profile satisfaction.

## User Stories

### US-001: Define profile evolution and progressive adoption
**Project**: agent-resource-protocol

**As a** protocol implementer, evaluator, or ecosystem steward
**I want** readiness profiles to have stable naming, explicit evolution rules, and a way to communicate partial adoption
**So that** readiness claims remain interoperable and honest as profiles mature over time

**Acceptance Criteria**:
- [x] **AC-US1-01**: The repo defines naming and identifier stability guidance for readiness profiles
- [x] **AC-US1-02**: The repo defines how readiness profiles evolve compatibly or incompatibly over time
- [x] **AC-US1-03**: The repo defines how implementations may communicate partial adoption or in-progress readiness without claiming unsupported full profile conformance
- [x] **AC-US1-04**: The repo includes non-normative examples showing profile evolution metadata and progressive adoption declarations
