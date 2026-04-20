### T-001: Add schemas for control-plane, discovery, and compliance declarations
**User Story**: US-001
**Satisfies ACs**: AC-US1-01, AC-US1-02, AC-US1-03
**Status**: [x] completed

**Test Plan** (BDD):
- Given the current `AGRP v1` normative docs define operations, capability discovery, and readiness declarations mostly in prose → When machine-readable schemas are added for those surfaces → Then implementers can structurally validate representative examples without guessing field shapes from prose alone
