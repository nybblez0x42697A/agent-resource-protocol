### T-001: Add deployment topology and trust-boundary semantics
**User Story**: US-001
**Satisfies ACs**: AC-US1-01, AC-US1-02, AC-US1-03, AC-US1-04
**Status**: [x] completed

**Test Plan** (BDD):
- Given the existing AGRP v1 control-plane, security, observability, and rollout documents → When an implementer reads the deployment layer → Then they can distinguish protocol-visible deployment responsibilities and trust boundaries from non-normative internal architecture choices
