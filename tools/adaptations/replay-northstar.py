#!/usr/bin/env python3
"""Replay proof for the Northstar Tool Registry reference adaptation.

Reads the 15 JSON artifacts in `examples/adaptations/northstar-tool-registry/`
in step-prefix order (00 through 14), validates each against its declared
schema, then replays the AGRP lifecycle in memory: register v1 (draft) →
register v2 (draft) with v1 lineage parent → transition v2 (draft → active)
backed by an evidence attestation → publish capability advertisement.

After replay, prints a final-state snapshot showing both versions, the
recommended/active version, capability set, lineage chain, and ledger
counts. Exits 0 on a successful replay where every locked invariant holds;
exits non-zero with an `INVARIANT VIOLATED [#N]: …` message on stderr if
any invariant fails.

This script is non-normative supporting tooling per
spec/charter/agrp-v1-artifact-set.md:85-92. It is read-only with respect to
the bundle; the bundle is never mutated.

Run from repo root:

    python3 tools/adaptations/replay-northstar.py
    python3 tools/adaptations/replay-northstar.py --verbose
    python3 tools/adaptations/replay-northstar.py --bundle-path /tmp/copy

The replay reads from the bundle named by --bundle-path (default: the
canonical bundle at `examples/adaptations/northstar-tool-registry/`).

----------------------------------------------------------------------------
Validation logic — duplicate-with-citation
----------------------------------------------------------------------------

The schema-mapping table, schema-registry construction, and the
evidence-attestation prose-shape check below are duplicated from increment
0047's validation script. The duplicate-with-citation strategy was locked
at 0048 plan approval because the source path lives under .specweave/,
which is gitignored — committed tooling cannot depend on workbench
scaffolding.

Source of duplicated logic:
    .specweave/increments/0047-agrp-northstar-tool-registry-reference-adaptation/scripts/validate-bundle.py
    (Validation report: .specweave/increments/0047-…/reports/schema-validation-output.txt)

The duplicated blocks are marked with "# [DUP-FROM-0047]" comments so
future reviewers can locate them. If 0047's logic ever changes, update
both copies.
"""
from __future__ import annotations

import argparse
import json
import sys
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
from typing import Any

# `jsonschema` is used for validation. It is the same library 0047 used.
import jsonschema
from referencing import Registry, Resource
from referencing.jsonschema import DRAFT202012


# ---------------------------------------------------------------------------
# Path resolution — works from any CWD.
# parents[0] = tools/adaptations, parents[1] = tools, parents[2] = repo root
# ---------------------------------------------------------------------------
REPO_ROOT = Path(__file__).resolve().parents[2]
DEFAULT_BUNDLE = REPO_ROOT / "examples/adaptations/northstar-tool-registry"
SCHEMA_DIR = REPO_ROOT / "models/schemas"


# ===========================================================================
# Schema registry + artifact-to-schema mapping
# [DUP-FROM-0047] — see header for citation rationale
# ===========================================================================

# [DUP-FROM-0047] SCHEMA_FILES
SCHEMA_FILES = {
    "common.schema.json": "https://agent-resource-protocol.dev/schemas/common.schema.json",
    "resource-entity.schema.json": "https://agent-resource-protocol.dev/schemas/resource-entity.schema.json",
    "registration-record.schema.json": "https://agent-resource-protocol.dev/schemas/registration-record.schema.json",
    "audit-record.schema.json": "https://agent-resource-protocol.dev/schemas/audit-record.schema.json",
    "lineage-node.schema.json": "https://agent-resource-protocol.dev/schemas/lineage-node.schema.json",
    "lifecycle-transition.schema.json": "https://agent-resource-protocol.dev/schemas/lifecycle-transition.schema.json",
    "capability-advertisement.schema.json": "https://agent-resource-protocol.dev/schemas/capability-advertisement.schema.json",
    "control-plane-envelope.schema.json": "https://agent-resource-protocol.dev/schemas/control-plane-envelope.schema.json",
}


# [DUP-FROM-0047] build_registry()
def build_registry() -> Registry:
    """Build a referencing Registry that resolves the relative ./common.schema.json
    refs used by the AGRP schemas.
    """
    contents: dict[str, Any] = {}
    for filename in SCHEMA_FILES:
        path = SCHEMA_DIR / filename
        contents[filename] = json.loads(path.read_text())

    registry = Registry()
    for filename, schema in contents.items():
        resource = Resource.from_contents(schema, default_specification=DRAFT202012)
        if "$id" in schema:
            registry = registry.with_resource(uri=schema["$id"], resource=resource)
        registry = registry.with_resource(uri=f"./{filename}", resource=resource)
        registry = registry.with_resource(uri=filename, resource=resource)
    return registry


# [DUP-FROM-0047] ARTIFACT_SCHEMA — maps each bundle file to its validation target.
# Note: file 12 (evidence-attestation) has no AGRP schema today; its shape is
# defined by spec prose at spec/compliance/evidence-freshness-and-attestation.md:60-89,
# so it's validated by a separate prose-shape function below.
# Note: envelope-wrapped wire artifacts validate against control-plane-envelope.schema.json
# only — the envelope's oneOf operation-branch fans out per-operation field
# requirements internally. There is no separate per-operation payload schema.
ARTIFACT_SCHEMA = [
    ("00-tool-resource.v1.example.json", "resource-entity.schema.json"),
    ("01-register-resource-version.v1.request.json", "control-plane-envelope.schema.json"),
    ("02-register-resource-version.v1.response.json", "control-plane-envelope.schema.json"),
    ("03-registration-record.v1.example.json", "registration-record.schema.json"),
    ("04-audit-record.create.v1.example.json", "audit-record.schema.json"),
    ("05-lineage-node.v1.example.json", "lineage-node.schema.json"),
    ("06-tool-resource.v2.example.json", "resource-entity.schema.json"),
    ("07-register-resource-version.v2.request.json", "control-plane-envelope.schema.json"),
    ("08-lineage-node.v2.example.json", "lineage-node.schema.json"),
    ("09-audit-record.update.v2.example.json", "audit-record.schema.json"),
    ("10-lifecycle-transition.preview-to-ga.request.json", "control-plane-envelope.schema.json"),
    ("11-lifecycle-transition.preview-to-ga.event.json", "lifecycle-transition.schema.json"),
    # 12 — evidence-attestation: prose-shape only, no schema
    ("13-audit-record.transition.example.json", "audit-record.schema.json"),
    ("14-capability-advertisement.example.json", "capability-advertisement.schema.json"),
]


# [DUP-FROM-0047] EVIDENCE_REQUIRED_FIELDS + validate_evidence_attestation()
EVIDENCE_REQUIRED_FIELDS = [
    "evidenceId",
    "subject",
    "evidenceType",
    "attestationStatus",
]


def validate_evidence_attestation(path: Path) -> tuple[bool, str]:
    """Validate file 12 against the prose-defined shape at
    spec/compliance/evidence-freshness-and-attestation.md:60-89.
    Returns (ok, message_or_empty).
    """
    artifact = json.loads(path.read_text())
    missing: list[str] = []
    for field_name in EVIDENCE_REQUIRED_FIELDS:
        if field_name not in artifact:
            missing.append(field_name)
    if "observedAt" not in artifact and "collectedAt" not in artifact:
        missing.append("observedAt|collectedAt")
    if artifact.get("attestationStatus") in ("self-attested", "externally attested"):
        for field_name in ("attestorId", "attestedAt"):
            if field_name not in artifact:
                missing.append(field_name)
    if "validUntil" not in artifact and "freshness" not in artifact:
        missing.append("validUntil|freshness")
    if missing:
        return False, f"missing fields: {', '.join(missing)}"
    return True, ""


# ===========================================================================
# State machine
# ===========================================================================


@dataclass
class Version:
    versionId: str
    lifecycleState: str  # draft|active|deprecated|archived|superseded|restored
    registrationStatus: str  # active|deprecated|archived|superseded|restored (no draft)
    capabilities: list[str] = field(default_factory=list)
    parentVersionId: str | None = None
    auditRefs: list[str] = field(default_factory=list)
    evidenceRefs: list[str] = field(default_factory=list)
    northstarStage: str | None = None
    # Cached for invariant 3 — set when the envelope's registrationRecord is read.
    _envelope_registration: dict[str, Any] | None = None


@dataclass
class Tool:
    resourceId: str
    resourceKind: str
    versions: dict[str, Version] = field(default_factory=dict)
    recommendedVersionId: str | None = None


@dataclass
class RegistryState:
    tools: dict[str, Tool] = field(default_factory=dict)
    audits: list[dict[str, Any]] = field(default_factory=list)
    evidence: dict[str, dict[str, Any]] = field(default_factory=dict)
    capability_adverts: list[dict[str, Any]] = field(default_factory=list)
    events_seen: list[str] = field(default_factory=list)
    pending_transition: dict[str, Any] | None = None
    last_timestamp: datetime | None = None  # for invariant 8


# ===========================================================================
# Invariant violations — locked-at-C3 message strings
# ===========================================================================


class InvariantViolation(Exception):
    """Raised when any locked invariant fails. The message is the locked
    `INVARIANT VIOLATED [#N]: ...` string. See reports/c3-decisions.txt for
    the canonical wording per invariant.
    """


def _violate(num: int, body: str) -> None:
    raise InvariantViolation(f"INVARIANT VIOLATED [#{num}]: {body}")


# ===========================================================================
# Per-step handlers
# ===========================================================================


def _parse_ts(ts: str) -> datetime:
    return datetime.fromisoformat(ts.replace("Z", "+00:00"))


def _check_timestamp(state: RegistryState, ts_str: str, step_label: str) -> None:
    """Invariant #8: timestamps non-decreasing across timestamped events."""
    if not ts_str:
        return
    this = _parse_ts(ts_str)
    if state.last_timestamp is not None and this < state.last_timestamp:
        _violate(
            8,
            f"timestamp regression (step {step_label}, prev: {state.last_timestamp.isoformat()}, this: {this.isoformat()})",
        )
    state.last_timestamp = this


def load_tool_resource(state: RegistryState, artifact: dict, step_label: str) -> str:
    """Files 00 and 06: declare the resource entity for a version."""
    resource_id = artifact["resourceId"]
    resource_kind = artifact["resourceKind"]
    version_id = artifact["versionId"]
    metadata = artifact.get("metadata", {})

    tool = state.tools.setdefault(
        resource_id, Tool(resourceId=resource_id, resourceKind=resource_kind)
    )
    # Initialize the version skeleton; lifecycleState/registrationStatus
    # land when the registration request is processed.
    if version_id not in tool.versions:
        tool.versions[version_id] = Version(
            versionId=version_id,
            lifecycleState="draft",
            registrationStatus="active",
            capabilities=list(metadata.get("capabilities", [])),
            northstarStage=metadata.get("northstarStage"),
        )
    if metadata.get("createdAt"):
        _check_timestamp(state, metadata["createdAt"], step_label)
    return f"tool={resource_id} version={version_id} added (capabilities={tool.versions[version_id].capabilities})"


def apply_register_request(
    state: RegistryState, envelope: dict, step_label: str
) -> str:
    """Files 01 and 07: RegisterResourceVersion request envelope.

    The envelope's RegisterResourceVersion request branch (per
    control-plane-envelope.schema.json:48-80) carries `registrationRecord`
    and `auditRecord` as top-level fields of the envelope, NOT under a
    `payload` object. There is no separate register-resource-version
    payload schema. Read top-level directly.
    """
    rr = envelope["registrationRecord"]
    ar = envelope["auditRecord"]
    resource_id = rr["resourceId"]
    version_id = rr["versionId"]
    tool = state.tools.setdefault(
        resource_id, Tool(resourceId=resource_id, resourceKind=rr["resourceKind"])
    )
    version = tool.versions.setdefault(
        version_id,
        Version(
            versionId=version_id,
            lifecycleState=rr.get("metadata", {}).get("lifecycleState", "draft"),
            registrationStatus=rr["status"],
        ),
    )
    # Record/refresh from the registration record (the envelope view).
    version.lifecycleState = rr.get("metadata", {}).get("lifecycleState", "draft")
    version.registrationStatus = rr["status"]
    version.northstarStage = rr.get("metadata", {}).get("northstarStage")
    version.capabilities = list(rr.get("metadata", {}).get("capabilities", version.capabilities))
    version._envelope_registration = rr
    # Use the envelope's auditRecord ONLY to set the version's auditRef linkage
    # and to advance the timestamp invariant. Do NOT append it to state.audits —
    # the audit ledger is the persisted-standalone-records ledger; the
    # embedded copy here is a wire-format duplicate of file 04 (or 09).
    # Persisted standalone audits land via consume_audit_record (files 04/09/13).
    if ar["commitId"] not in version.auditRefs:
        version.auditRefs.append(ar["commitId"])
    _check_timestamp(state, ar["createdAt"], step_label)

    # Invariant 1 (file 01) / 2-state-and-status (file 07).
    expected = ("draft", "active")
    observed = (version.lifecycleState, version.registrationStatus)
    if version_id == "0.1.0":
        if observed != expected:
            _violate(
                1,
                f"v1 first registration not (draft, active) "
                f"(artifact: {step_label}, expected: draft/active, observed: {observed[0]}/{observed[1]})",
            )
    elif version_id == "0.2.0":
        if observed != expected:
            _violate(
                2,
                f"v2 first registration not (draft, active) "
                f"(artifact: {step_label}, expected: draft/active, observed: {observed[0]}/{observed[1]})",
            )
    return f"version {version_id} added ({version.lifecycleState}, {version.registrationStatus})"


def apply_register_response(
    state: RegistryState, envelope: dict, step_label: str
) -> str:
    """File 02: RegisterResourceVersion success response. Confirms acceptance.

    The success branch (per envelope schema lines 378-418) contains
    result.{resourceId, versionId, registrationRecord, lineageNode}.
    """
    result = envelope["result"]
    rr = result["registrationRecord"]
    if rr["status"] != "active":
        _violate(
            1,
            f"v1 acceptance response status not 'active' "
            f"(artifact: {step_label}, observed: {rr['status']})",
        )
    return f"v{rr['versionId']} acceptance confirmed (status={rr['status']})"


def consume_registration_record(
    state: RegistryState, artifact: dict, step_label: str
) -> str:
    """File 03: standalone registration-record. Invariant 3."""
    resource_id = artifact["resourceId"]
    version_id = artifact["versionId"]
    tool = state.tools.get(resource_id)
    if tool is None or version_id not in tool.versions:
        _violate(
            3,
            f"standalone registration record for unknown version "
            f"(artifact: {step_label}, resourceId: {resource_id}, versionId: {version_id})",
        )
    version = tool.versions[version_id]
    envelope_rr = version._envelope_registration
    if envelope_rr is None:
        _violate(
            3,
            f"standalone registration record loaded before envelope view "
            f"(artifact: {step_label})",
        )
    # Compare load-bearing fields between the standalone record and the
    # envelope-wrapped one.
    fields_to_check = (
        "resourceId",
        "versionId",
        "resourceKind",
        "status",
        "implementationRef",
        "interfaceRef",
        "auditRef",
    )
    for field_name in fields_to_check:
        env_val = envelope_rr.get(field_name)
        std_val = artifact.get(field_name)
        if env_val != std_val:
            _violate(
                3,
                f"standalone registration record diverges from envelope "
                f"(artifact: {step_label}, field: {field_name}, "
                f"expected: {env_val!r}, observed: {std_val!r})",
            )
    return f"invariant 3 OK (matches envelope on {len(fields_to_check)} fields)"


def consume_audit_record(state: RegistryState, artifact: dict, step_label: str) -> str:
    """Files 04, 09, 13: append an audit-record."""
    state.audits.append(artifact)
    _check_timestamp(state, artifact["createdAt"], step_label)
    resource_id = artifact["resourceId"]
    version_id = artifact["versionId"]
    tool = state.tools.get(resource_id)
    if tool and version_id in tool.versions:
        if artifact["commitId"] not in tool.versions[version_id].auditRefs:
            tool.versions[version_id].auditRefs.append(artifact["commitId"])

    # Invariant 6 — only checked for file 13 (transition audit), once
    # transition request (10) and evidence-attestation (12) have both
    # landed. Also: attach the transition's evidenceRefs to the
    # corresponding version so the final-state snapshot reflects the
    # evidence linkage. (Per C4 review: file 13 is the cleanest place
    # to do this because it is the persisted audit linkage.)
    if "transition" in step_label:
        ev_refs = artifact.get("evidenceRefs", [])
        # Pull the transition request's evidenceRefs from pending_transition.
        # pending_transition is staged at file 10 by apply_transition_request
        # and is NOT cleared by apply_transition_event (file 11), so it is
        # still available here at file 13 for the cross-check against the
        # original wire request's evidenceRefs.
        pending = state.pending_transition or {}
        request_refs = list(pending.get("evidenceRefs", []))
        # Cross-check that every evidenceId in the audit's evidenceRefs
        # appears in both the transition request's refs and in the
        # evidence ledger.
        for evid in ev_refs:
            if evid not in state.evidence:
                _violate(
                    6,
                    f"evidence cross-reference missing "
                    f"(evidenceId: {evid}, missing-from: evidence-ledger; expected from file 12)",
                )
            if request_refs and evid not in request_refs:
                _violate(
                    6,
                    f"evidence cross-reference missing "
                    f"(evidenceId: {evid}, missing-from: 10-...request.evidenceRefs)",
                )
        # Attach the evidence to the version (idempotent).
        if tool and version_id in tool.versions:
            for evid in ev_refs:
                if evid not in tool.versions[version_id].evidenceRefs:
                    tool.versions[version_id].evidenceRefs.append(evid)

    return f"audit ledger += 1 (commitId={artifact['commitId']})"


def consume_lineage_node(state: RegistryState, artifact: dict, step_label: str) -> str:
    """Files 05, 08: lineage edge."""
    resource_id = artifact["resourceId"]
    version_id = artifact["versionId"]
    parent_id = artifact.get("parentVersionId")
    tool = state.tools.get(resource_id)
    if tool is None or version_id not in tool.versions:
        _violate(
            2,
            f"lineage node for unknown version "
            f"(artifact: {step_label}, resourceId: {resource_id}, versionId: {version_id})",
        )
    version = tool.versions[version_id]
    version.parentVersionId = parent_id
    _check_timestamp(state, artifact.get("createdAt", ""), step_label)

    # Invariant 2 lineage check (only for v2 — v1 is the root with parent=None).
    if version_id == "0.2.0":
        if parent_id is None:
            _violate(
                2,
                f"v2 lineage parent does not resolve to v1.versionId "
                f"(artifact: {step_label}, expected: 0.1.0, observed: null)",
            )
        if parent_id not in tool.versions:
            _violate(
                2,
                f"v2 lineage parent does not resolve to v1.versionId "
                f"(artifact: {step_label}, expected: 0.1.0, observed: {parent_id!r})",
            )
        if parent_id != "0.1.0":
            _violate(
                2,
                f"v2 lineage parent does not resolve to v1.versionId "
                f"(artifact: {step_label}, expected: 0.1.0, observed: {parent_id!r})",
            )
    return f"v{version_id} lineage parent={parent_id}"


def apply_transition_request(
    state: RegistryState, envelope: dict, step_label: str
) -> str:
    """File 10: TransitionLifecycleState request envelope.

    The envelope's TransitionLifecycleState request branch (per
    envelope schema lines 137-184) carries operation fields directly at
    the envelope top level (resourceId, versionId, fromState, toState,
    rationale, evidenceRefs).
    """
    resource_id = envelope["resourceId"]
    version_id = envelope["versionId"]
    from_state = envelope["fromState"]
    to_state = envelope["toState"]
    tool = state.tools[resource_id]
    version = tool.versions[version_id]

    # Invariant 4: fromState matches v2's current state before apply.
    if version.lifecycleState != from_state:
        _violate(
            4,
            f"transition fromState mismatch "
            f"(artifact: {step_label}, expected: {version.lifecycleState}, observed: {from_state})",
        )
    state.pending_transition = {
        "resourceId": resource_id,
        "versionId": version_id,
        "fromState": from_state,
        "toState": to_state,
        "evidenceRefs": list(envelope.get("evidenceRefs", [])),
    }
    return f"staged transition v{version_id} {from_state}->{to_state}"


def apply_transition_event(
    state: RegistryState, artifact: dict, step_label: str
) -> str:
    """File 11: persisted lifecycle-transition event. Apply the staged transition."""
    pending = state.pending_transition
    if pending is None:
        _violate(
            5,
            f"transition event without staged request "
            f"(artifact: {step_label})",
        )
    if (
        artifact["resourceId"] != pending["resourceId"]
        or artifact["versionId"] != pending["versionId"]
        or artifact["fromState"] != pending["fromState"]
        or artifact["toState"] != pending["toState"]
    ):
        _violate(
            5,
            f"transition event diverges from staged request "
            f"(artifact: {step_label})",
        )
    tool = state.tools[pending["resourceId"]]
    version = tool.versions[pending["versionId"]]
    version.lifecycleState = pending["toState"]

    # Invariant 5: v2 lifecycleState=active AND exactly one version is active.
    if version.lifecycleState != "active":
        _violate(
            5,
            f"post-transition active-state invariant failed "
            f"(artifact: {step_label}, observed: v2.state={version.lifecycleState}, "
            f"active-count={sum(1 for v in tool.versions.values() if v.lifecycleState == 'active')})",
        )
    active_count = sum(1 for v in tool.versions.values() if v.lifecycleState == "active")
    if active_count != 1:
        _violate(
            5,
            f"post-transition active-state invariant failed "
            f"(artifact: {step_label}, observed: v2.state={version.lifecycleState}, "
            f"active-count={active_count})",
        )
    # Update northstarStage (surface label change preview -> general-availability).
    if version.northstarStage == "preview":
        version.northstarStage = "general-availability"
    return f"applied: v{version.versionId} lifecycleState={version.lifecycleState}"


def consume_evidence_attestation(
    state: RegistryState, artifact: dict, step_label: str
) -> str:
    """File 12: evidence-attestation (prose-shape; no schema)."""
    evid = artifact["evidenceId"]
    state.evidence[evid] = artifact
    if "attestedAt" in artifact:
        _check_timestamp(state, artifact["attestedAt"], step_label)
    elif "collectedAt" in artifact:
        _check_timestamp(state, artifact["collectedAt"], step_label)
    return f"evidence ledger += 1 (evidenceId={evid})"


def consume_capability_advertisement(
    state: RegistryState, artifact: dict, step_label: str
) -> str:
    """File 14: capability advertisement. Sets recommendedVersionId; checks invariant 7."""
    state.capability_adverts.append(artifact)
    notes = artifact.get("notes", {})
    if "publishedAt" in notes:
        _check_timestamp(state, notes["publishedAt"], step_label)

    advertised = notes.get("currentlyAdvertisedTools") or []
    if not advertised:
        _violate(
            7,
            f"capability advertisement does not name v2 / lineage incomplete "
            f"(artifact: {step_label}, observed-recommended: <none>, observed-lineage: <none>)",
        )
    entry = advertised[0]
    rec_version = entry.get("recommendedVersionId")
    lineage_list = entry.get("lineageVersionIds", [])
    if rec_version != "0.2.0":
        _violate(
            7,
            f"capability advertisement does not name v2 / lineage incomplete "
            f"(artifact: {step_label}, observed-recommended: {rec_version!r}, observed-lineage: {lineage_list})",
        )
    if "0.1.0" not in lineage_list or "0.2.0" not in lineage_list:
        _violate(
            7,
            f"capability advertisement does not name v2 / lineage incomplete "
            f"(artifact: {step_label}, observed-recommended: {rec_version!r}, observed-lineage: {lineage_list})",
        )
    tool = state.tools[entry["resourceId"]]
    tool.recommendedVersionId = rec_version
    return f"recommended=v{rec_version}; lineageVersionIds={lineage_list}"


# ===========================================================================
# Validation pass — runs once at load time, before replay
# ===========================================================================


def load_and_validate_bundle(bundle_path: Path) -> list[tuple[str, dict]]:
    """Load every JSON artifact in `bundle_path`, validate against its
    schema (or prose shape for evidence-attestation), and return the
    ordered list of (filename, parsed-dict) tuples in step-prefix order.

    Validation failure exits non-zero before replay starts.
    """
    registry = build_registry()
    out: list[tuple[str, dict]] = []
    failed = False

    for filename, schema_name in ARTIFACT_SCHEMA:
        path = bundle_path / filename
        if not path.exists():
            print(
                f"FAIL load: {filename} -> {schema_name} :: file missing at {path}",
                file=sys.stderr,
            )
            failed = True
            continue
        try:
            artifact = json.loads(path.read_text())
        except json.JSONDecodeError as exc:
            print(
                f"FAIL load: {filename} -> {schema_name} :: JSON parse error: {exc}",
                file=sys.stderr,
            )
            failed = True
            continue
        schema = json.loads((SCHEMA_DIR / schema_name).read_text())
        validator = jsonschema.Draft202012Validator(schema, registry=registry)
        errors = sorted(validator.iter_errors(artifact), key=lambda e: e.path)
        if errors:
            err_summary = "; ".join(
                f"{list(e.absolute_path)}: {e.message[:120]}" for e in errors[:3]
            )
            print(
                f"FAIL validate: {filename} -> models/schemas/{schema_name} :: {err_summary}",
                file=sys.stderr,
            )
            failed = True
            continue
        out.append((filename, artifact))

    # Evidence-attestation prose-shape (file 12).
    evidence_filename = "12-evidence-attestation.preview-to-ga.example.json"
    evidence_path = bundle_path / evidence_filename
    if not evidence_path.exists():
        print(
            f"FAIL load: {evidence_filename} :: file missing at {evidence_path}",
            file=sys.stderr,
        )
        failed = True
    else:
        ok, msg = validate_evidence_attestation(evidence_path)
        if not ok:
            print(
                f"FAIL validate: {evidence_filename} -> "
                f"spec/compliance/evidence-freshness-and-attestation.md:60-89 :: {msg}",
                file=sys.stderr,
            )
            failed = True
        else:
            out.append((evidence_filename, json.loads(evidence_path.read_text())))

    if failed:
        print("Bundle validation failed. Replay aborted.", file=sys.stderr)
        sys.exit(2)

    # Re-sort by filename so the replay processes 00..14 in step order.
    out.sort(key=lambda pair: pair[0])
    return out


# ===========================================================================
# Replay driver
# ===========================================================================


HANDLERS: dict[str, callable] = {
    "00-tool-resource.v1.example.json": load_tool_resource,
    "01-register-resource-version.v1.request.json": apply_register_request,
    "02-register-resource-version.v1.response.json": apply_register_response,
    "03-registration-record.v1.example.json": consume_registration_record,
    "04-audit-record.create.v1.example.json": consume_audit_record,
    "05-lineage-node.v1.example.json": consume_lineage_node,
    "06-tool-resource.v2.example.json": load_tool_resource,
    "07-register-resource-version.v2.request.json": apply_register_request,
    "08-lineage-node.v2.example.json": consume_lineage_node,
    "09-audit-record.update.v2.example.json": consume_audit_record,
    "10-lifecycle-transition.preview-to-ga.request.json": apply_transition_request,
    "11-lifecycle-transition.preview-to-ga.event.json": apply_transition_event,
    "12-evidence-attestation.preview-to-ga.example.json": consume_evidence_attestation,
    "13-audit-record.transition.example.json": consume_audit_record,
    "14-capability-advertisement.example.json": consume_capability_advertisement,
}


# Short op-name shown in the per-step trace.
OP_LABELS = {
    "00-tool-resource.v1.example.json": "load tool-resource v1",
    "01-register-resource-version.v1.request.json": "register-resource-version v1 request",
    "02-register-resource-version.v1.response.json": "register-resource-version v1 response",
    "03-registration-record.v1.example.json": "registration-record v1 (standalone)",
    "04-audit-record.create.v1.example.json": "audit-record create v1",
    "05-lineage-node.v1.example.json": "lineage-node v1",
    "06-tool-resource.v2.example.json": "load tool-resource v2",
    "07-register-resource-version.v2.request.json": "register-resource-version v2 request",
    "08-lineage-node.v2.example.json": "lineage-node v2",
    "09-audit-record.update.v2.example.json": "audit-record update v2",
    "10-lifecycle-transition.preview-to-ga.request.json": "transition v2 draft->active request",
    "11-lifecycle-transition.preview-to-ga.event.json": "transition v2 draft->active event",
    "12-evidence-attestation.preview-to-ga.example.json": "evidence-attestation",
    "13-audit-record.transition.example.json": "audit-record transition",
    "14-capability-advertisement.example.json": "capability-advertisement",
}


def replay(state: RegistryState, artifacts: list[tuple[str, dict]], verbose: bool) -> None:
    for filename, artifact in artifacts:
        step = filename[:2]
        handler = HANDLERS[filename]
        op_label = OP_LABELS[filename]
        delta = handler(state, artifact, filename)
        print(f"[{step}] {op_label:<44s} -> {delta}")
        if verbose:
            _print_state_delta(state)
        state.events_seen.append(filename)


def _print_state_delta(state: RegistryState) -> None:
    for tool in state.tools.values():
        for v in tool.versions.values():
            print(
                f"     v{v.versionId}: state={v.lifecycleState} "
                f"status={v.registrationStatus} stage={v.northstarStage} "
                f"caps={v.capabilities} parent={v.parentVersionId}"
            )
    print(
        f"     audits={len(state.audits)} evidence={len(state.evidence)} "
        f"adverts={len(state.capability_adverts)}"
    )


# ===========================================================================
# Final-state snapshot
# ===========================================================================


def _bracket(items: list[str]) -> str:
    return "[" + ", ".join(items) + "]"


def print_final_state(state: RegistryState) -> None:
    print()
    print("=== Northstar Tool Registry — Replay Final State ===")
    print()
    print("Tools:")
    for tool in state.tools.values():
        print(f"  {tool.resourceId} (kind={tool.resourceKind})")
        print("    Versions:")
        for vid in sorted(tool.versions.keys()):
            v = tool.versions[vid]
            parent = v.parentVersionId if v.parentVersionId else "<none — lineage root>"
            audit_str = _bracket(v.auditRefs)
            evid_str = _bracket(v.evidenceRefs)
            print(f"      {v.versionId}:")
            print(f"        lifecycleState:     {v.lifecycleState}")
            print(f"        registrationStatus: {v.registrationStatus}")
            print(f"        northstarStage:     {v.northstarStage}")
            print(f"        capabilities:       {_bracket(v.capabilities)}")
            print(f"        parentVersionId:    {parent}")
            print(f"        auditRefs:          {audit_str}")
            print(f"        evidenceRefs:       {evid_str}")
        rec = tool.recommendedVersionId or "<unset>"
        print(f"    RecommendedVersion:     {rec}")
    print()
    # Lineage chain summary
    if state.tools:
        tool = next(iter(state.tools.values()))
        chain = []
        for vid in sorted(tool.versions.keys()):
            v = tool.versions[vid]
            tag = "draft, root" if v.parentVersionId is None else f"{v.lifecycleState}"
            if v.versionId == tool.recommendedVersionId:
                tag += ", recommended"
            chain.append(f"{v.versionId} ({tag})")
        print(f"Lineage chain: {' -> '.join(chain)}")
        print()
    # Capability advertisement summary
    if state.capability_adverts:
        ad = state.capability_adverts[-1]
        notes = ad.get("notes", {})
        published = notes.get("publishedAt", "<unknown>")
        advertised = (notes.get("currentlyAdvertisedTools") or [{}])[0]
        rid = advertised.get("resourceId", "<unknown>")
        rec_v = advertised.get("recommendedVersionId", "<unknown>")
        lin = advertised.get("lineageVersionIds", [])
        print("Capability advertisement:")
        print(f"  publishedAt:              {published}")
        print(f"  advertised:               {rid} @ {rec_v}")
        print(f"  lineageVersionIds:        {lin}")
        print()
    print(f"Audit ledger entries:       {len(state.audits)}")
    print(f"Evidence ledger entries:    {len(state.evidence)}")
    print()
    print("=== All 8 invariants OK ===")
    print()
    print("Replay complete. Exit 0.")


# ===========================================================================
# Entry point
# ===========================================================================


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        prog="replay-northstar",
        description="Replay proof for the Northstar Tool Registry reference adaptation.",
    )
    parser.add_argument(
        "--bundle-path",
        type=Path,
        default=DEFAULT_BUNDLE,
        help=(
            "Path to the bundle directory to replay. "
            f"Default: {DEFAULT_BUNDLE} (repo-root-relative)."
        ),
    )
    parser.add_argument(
        "--verbose",
        action="store_true",
        help="Print per-step state deltas in addition to the trace lines.",
    )
    args = parser.parse_args(argv)

    bundle_path: Path = args.bundle_path.resolve()
    if not bundle_path.is_dir():
        print(f"--bundle-path is not a directory: {bundle_path}", file=sys.stderr)
        return 2

    artifacts = load_and_validate_bundle(bundle_path)
    state = RegistryState()
    try:
        replay(state, artifacts, args.verbose)
    except InvariantViolation as exc:
        print(str(exc), file=sys.stderr)
        return 1
    print_final_state(state)
    return 0


if __name__ == "__main__":
    sys.exit(main())
