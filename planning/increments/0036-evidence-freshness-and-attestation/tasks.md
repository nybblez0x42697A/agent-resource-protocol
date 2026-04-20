### T-001: Add evidence freshness and attestation semantics
**User Story**: US-001
**Satisfies ACs**: AC-US1-01, AC-US1-02, AC-US1-03, AC-US1-04
**Status**: [x] completed

**Test Plan** (BDD):
- Given the existing readiness, declaration, and partial-failure specifications → When a consumer evaluates supporting evidence for a profile claim → Then the consumer can distinguish attested current evidence from stale, expired, missing, or unauthenticated evidence without changing baseline protocol meaning
