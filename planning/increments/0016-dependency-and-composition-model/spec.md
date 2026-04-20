---
increment: 0016-dependency-and-composition-model
title: Dependency and Composition Model
---

# Feature: Dependency and Composition Model

## Overview

Define how protocol artifacts depend on and compose with each other, including compatibility expectations and failure behavior across composed dependencies.

## User Stories

### US-001: Define dependency and composition rules
**Project**: agent-resource-protocol

**As a** protocol implementer
**I want** clear dependency and composition rules
**So that** I can model compound capabilities and reason about compatibility or failure when artifacts rely on one another

**Acceptance Criteria**:
- [x] **AC-US1-01**: The repo defines baseline dependency types and composition rules across protocol artifacts
- [x] **AC-US1-02**: The repo defines compatibility and failure expectations when required or optional dependencies are unavailable or incompatible
- [x] **AC-US1-03**: The repo includes non-normative examples showing a composed artifact with required and optional dependencies
