---
increment: 0029-protocol-release-definition
title: Protocol Release Definition
---

# Feature: Protocol Release Definition

## Overview

Define the top-level `ARP v1.0.0` release boundary so conformant implementations can anchor their claims to one protocol release rather than to the repository in general.

## User Stories

### US-001: Define the ARP v1.0.0 release
**Project**: agent-resource-protocol

**As a** protocol author, implementer, or evaluator
**I want** one normative document that defines what `ARP v1.0.0` means as a protocol release
**So that** release claims, conformance claims, and later version classifications all refer to the same standard boundary

**Acceptance Criteria**:
- [x] **AC-US1-01**: The repo defines `ARP v1.0.0` as a named protocol release anchored to the `ARP v1` artifact set
- [x] **AC-US1-02**: The release document states how `ARP v1.0.0` claims relate to artifact-set validity, conformance, and later version classification
- [x] **AC-US1-03**: The repo includes a non-normative release example that illustrates how the `v1.0.0` boundary can be expressed without becoming the only mandatory publication format
