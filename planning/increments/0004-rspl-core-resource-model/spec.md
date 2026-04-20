---
increment: 0004-rspl-core-resource-model
title: RSPL Core Resource Model
---

# Feature: RSPL Core Resource Model

## Overview

Define the initial protocol resource classes, entity tuple, metadata boundaries, and evolvability markers.

## User Stories

### US-001: Define resource entities
**Project**: agent-resource-protocol

**As a** protocol designer
**I want** a formal resource model
**So that** heterogeneous agent resources can be registered, inspected, versioned, and evolved consistently

**Acceptance Criteria**:
- [x] **AC-US1-01**: The resource model defines the starting resource classes and shared entity tuple
- [x] **AC-US1-02**: The resource model defines which fields are identity, configuration, metadata, or evolvable state
- [x] **AC-US1-03**: The resource model distinguishes mandatory protocol fields from provisional extensions
