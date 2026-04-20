---
increment: 0035-deployment-topology-and-trust-boundaries
title: Deployment Topology and Trust Boundaries
---

# Feature: Deployment Topology and Trust Boundaries

## Overview

Define the deployment layer for `AGRP v1` so implementations can reason about shared versus split deployment shapes, trust boundaries, and externally visible responsibilities without turning one hosting architecture into a mandatory standard.

## User Stories

### US-001: Define deployment-visible roles and trust boundaries
**Project**: agent-resource-protocol

**As a** protocol implementer or adopter
**I want** a normative deployment-layer description for `AGRP v1`
**So that** I can map the protocol onto real service boundaries and trust zones without inferring hidden topology requirements from other documents

**Acceptance Criteria**:
- [x] **AC-US1-01**: The repo adds a normative deployment document under `spec/deployment/` for `AGRP v1`
- [x] **AC-US1-02**: The deployment document defines deployment-visible roles, trust boundaries, and supported topology patterns without mandating one implementation architecture
- [x] **AC-US1-03**: The repo adds non-normative examples showing at least two distinct deployment shapes that preserve the same protocol semantics
- [x] **AC-US1-04**: `spec/README.md` and `examples/README.md` reflect the new deployment materials
