---
increment: 0033-adopter-mapping-template
title: Adopter Mapping Template
---

# Feature: Adopter Mapping Template

## Overview

Add a neutral adopter mapping template under `adopters/` so external teams can translate an existing system into `AGRP v1` terms without treating their local architecture as normative protocol text.

## User Stories

### US-001: Publish a reusable adopter mapping template
**Project**: agent-resource-protocol

**As a** design partner or adopting team
**I want** a concrete mapping template that tells me what to document when relating my system to `AGRP v1`
**So that** I can evaluate fit, identify gaps, and describe local adaptations without redefining the core protocol

**Acceptance Criteria**:
- [x] **AC-US1-01**: The repo adds a reusable adopter mapping template under `adopters/` that covers resource identity, operations, lifecycle, diagnostics, and declared deviations or extensions
- [x] **AC-US1-02**: The template clearly separates normative AGRP requirements from adopter-local implementation details and gaps
- [x] **AC-US1-03**: The repo includes one filled example or illustrative skeleton showing how an adopter would use the template without making product-specific behavior normative
