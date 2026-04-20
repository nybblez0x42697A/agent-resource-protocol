---
increment: 0008-control-plane-contracts
title: Control-Plane Contracts
---

# Feature: Control-Plane Contracts

## Overview

Define protocol-visible operations, request and response contracts, and error surfaces for resource registry and control-plane interactions.

## User Stories

### US-001: Define control-plane operations
**Project**: agent-resource-protocol

**As a** protocol implementer
**I want** stable control-plane contracts
**So that** registries and controllers can interoperate around resource lifecycle, registration, and restore operations

**Acceptance Criteria**:
- [x] **AC-US1-01**: The design defines baseline control-plane operations and request/response contracts
- [x] **AC-US1-02**: The design defines error categories and failure surfaces for lifecycle and registration operations
- [x] **AC-US1-03**: The design preserves separation between control-plane contracts and implementation-specific architecture
