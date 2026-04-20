### T-001: Add conformance vectors, negative cases, and a local runner
**User Story**: US-001
**Satisfies ACs**: AC-US1-01, AC-US1-02, AC-US1-03
**Status**: [x] completed

**Test Plan** (BDD):
- Given the current `AGRP v1` schemas and baseline failure model → When the conformance vector runner is executed → Then valid fixtures pass, intentionally invalid fixtures fail as expected, and the runner reports outcome mismatches explicitly
