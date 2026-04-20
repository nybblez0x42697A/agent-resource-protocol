---
increment: 0010-http-json-binding
title: HTTP JSON Binding
---

# Feature: HTTP JSON Binding

## Overview

Define a concrete HTTP and JSON transport binding for the existing control-plane contracts without changing protocol semantics.

## User Stories

### US-001: Define an HTTP JSON binding for the control plane
**Project**: agent-resource-protocol

**As a** protocol implementer
**I want** a concrete HTTP and JSON mapping for the control-plane operations
**So that** I can expose interoperable endpoints without inventing transport semantics from scratch

**Acceptance Criteria**:
- [x] **AC-US1-01**: The repo defines URI, method, and JSON envelope mappings for the baseline control-plane operations
- [x] **AC-US1-02**: The repo defines how protocol error categories map onto HTTP status codes and JSON error bodies
- [x] **AC-US1-03**: The repo includes non-normative HTTP request and response examples that align with the binding
