---
increment: 0036-evidence-freshness-and-attestation
title: Evidence Freshness and Attestation
---

# Feature: Evidence Freshness and Attestation

## Overview

Define the baseline evidence freshness and attestation model for readiness and compliance claims so consumers can distinguish current, stale, expired, and unauthenticated support evidence without inventing incompatible local rules.

## User Stories

### US-001: Define evidence freshness and attestation semantics
**Project**: agent-resource-protocol

**As a** protocol consumer or readiness-profile steward
**I want** a normative model for support evidence age and attestation status
**So that** compliance and readiness claims can be evaluated consistently across catalogs, declarations, and local policy contexts

**Acceptance Criteria**:
- [x] **AC-US1-01**: The repo adds a normative evidence and attestation document within the compliance layer
- [x] **AC-US1-02**: The document defines baseline freshness states and minimum attestation fields without mandating one credential or signature format
- [x] **AC-US1-03**: The repo adds non-normative examples showing current and stale or expired evidence assessments
- [x] **AC-US1-04**: `spec/README.md` and `examples/README.md` reflect the new evidence materials
