---
increment: 0013-capability-discovery-and-negotiation
title: Capability Discovery and Negotiation
---

# Feature: Capability Discovery and Negotiation

## Overview

Define a baseline capability discovery and negotiation model so implementations can advertise supported bindings, profiles, and extensions and choose compatible interactions.

## User Stories

### US-001: Define capability discovery and negotiation
**Project**: agent-resource-protocol

**As a** protocol implementer
**I want** a clear discovery and negotiation model
**So that** clients and services can identify compatible protocol features before attempting operations

**Acceptance Criteria**:
- [x] **AC-US1-01**: The repo defines a baseline capability advertisement model for conformance level, bindings, extensions, and profiles
- [x] **AC-US1-02**: The repo defines a baseline negotiation model for selecting compatible capabilities without redefining operation semantics
- [x] **AC-US1-03**: The repo includes non-normative examples showing a capability advertisement and a successful negotiation outcome
