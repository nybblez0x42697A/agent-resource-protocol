### T-001: Define the ARP v1.0.0 release boundary and example expression
**User Story**: US-001
**Satisfies ACs**: AC-US1-01, AC-US1-02, AC-US1-03
**Status**: [x] completed

**Test Plan** (BDD):
- Given the `ARP v1` artifact set and the existing versioning rules → When the `ARP v1.0.0` release definition is published → Then implementations can anchor release and conformance claims to one named protocol release without guessing which repository files are in scope
