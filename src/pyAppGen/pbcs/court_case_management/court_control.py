"""Executable court operations controls for improve1 execution.

Every function here is side-effect free and maps one improve1 court capability to
owned court tables, AppGen-X event metadata, UI/API surfaces, agent skills,
configuration handles, retry/dead-letter evidence, and traceability artifacts.
"""
from __future__ import annotations

import hashlib
import json
from typing import Callable, Mapping

from .improve1_capabilities import IMPROVE1_CAPABILITIES
PBC_KEY = "court_case_management"
EVENT_CONTRACT = "AppGen-X"
COURT_CASE_MANAGEMENT_ALLOWED_DATABASE_BACKENDS = ("postgresql", "mysql", "mariadb")
COURT_CASE_MANAGEMENT_REQUIRED_EVENT_TOPIC = "pbc.court_case_management.events"
COURT_CASE_MANAGEMENT_OWNED_TABLES = (
    "court_case_management_court_case",
    "court_case_management_filing",
    "court_case_management_evidence_item",
    "court_case_management_hearing",
    "court_case_management_case_task",
    "court_case_management_docket_entry",
    "court_case_management_party",
    "court_case_management_judgment",
    "court_case_management_court_order",
    "court_case_management_court_case_management_policy_rule",
    "court_case_management_court_case_management_runtime_parameter",
    "court_case_management_court_case_management_schema_extension",
    "court_case_management_court_case_management_control_assertion",
    "court_case_management_court_case_management_governed_model",
    "court_case_management_appgen_outbox_event",
    "court_case_management_appgen_inbox_event",
    "court_case_management_appgen_dead_letter_event",
)
COURT_CONTROL_CAPABILITIES = tuple(capability.slug for capability in IMPROVE1_CAPABILITIES)
SLUG_BY_NUMBER = {capability.feature_number: capability.slug for capability in IMPROVE1_CAPABILITIES}
CAPABILITY_BY_SLUG = {capability.slug: capability for capability in IMPROVE1_CAPABILITIES}
FIELD_SETS: tuple[tuple[str, ...], ...] = (
    ("court", "division", "case_year", "sequence", "venue"),
    ("party_id", "role", "representation_status", "lead_counsel", "appearance_date"),
    ("filing_id", "intake_state", "deficiency_codes", "cure_deadline", "clerk_reviewer"),
    ("filing_id", "parent_filing_id", "amendment_type", "supersedes", "docket_note"),
    ("entry_id", "sequence_number", "entry_source", "linked_record", "correction_reason"),
    ("motion_id", "motion_type", "opposition_due", "reply_due", "ruling_status"),
    ("order_id", "order_state", "signature_metadata", "entered_version", "effective_date"),
    ("hearing_id", "courtroom", "session_block", "assigned_judge", "calendar_status"),
    ("continuance_id", "requested_by", "outcome", "old_date", "new_date"),
    ("deadline_id", "rule_id", "trigger_date", "calculated_due_date", "calendar_policy"),
    ("service_id", "served_party", "service_method", "completed_date", "proof_document"),
    ("instrument_id", "instrument_type", "issued_to_party", "issue_date", "expiration_date"),
    ("exhibit_id", "exhibit_number", "custody_event", "admission_status", "storage_location"),
    ("record_id", "access_class", "view_policy", "export_policy", "audit_reason"),
    ("projection_id", "projection_scope", "seal_filter", "publication_rule", "freshness_state"),
    ("hearing_id", "minute_status", "appearances", "bench_rulings", "transcript_status"),
    ("judgment_id", "disposition_category", "relief_terms", "effective_date", "appealability"),
    ("appeal_id", "notice_date", "stay_status", "record_packet_status", "mandate_date"),
    ("case_id", "related_case_id", "relation_type", "order_reference", "separation_history"),
    ("assignment_id", "assigned_judge", "reassignment_reason", "recusal_indicator", "handoff_time"),
    ("queue_id", "intake_batch", "deficiency_queue", "fee_status", "issuance_tasks"),
    ("queue_id", "ruling_queue", "draft_orders", "hearing_packets", "overdue_alerts"),
    ("calendar_id", "courtroom", "check_in_status", "interpreter_ready", "minute_capture"),
    ("case_id", "timeline_events", "procedural_filters", "sealed_markers", "source_links"),
    ("assistant_session", "filing_packet", "triage_result", "source_citations", "confirmation_state"),
    ("assistant_session", "hearing_id", "packet_sections", "source_records", "role_scope"),
    ("assistant_session", "motion_id", "briefing_history", "draft_summary", "approval_boundary"),
    ("assistant_session", "unserved_parties", "notice_text", "review_date", "triggering_defect"),
    ("api_surface", "canonical_routes", "legacy_routes", "query_filters", "compatibility_notes"),
    ("event_type", "schema_version", "payload_fields", "idempotency_key", "topic"),
    ("inbound_event", "handler", "projection_target", "relevance_check", "idempotency_key"),
    ("submission_id", "idempotency_key", "document_hash", "matched_prior_record", "duplicate_reason"),
    ("policy_id", "local_rule", "standing_order", "approver", "preview_result"),
    ("dependency_graph", "blockers", "hearing_id", "motion_id", "readiness_state"),
    ("reservation_id", "hearing_id", "resource_type", "capacity_constraint", "conflict_status"),
    ("policy_id", "role", "case_sensitivity", "record_class", "allowed_actions"),
    ("proof_id", "sealed_record", "access_actor", "access_time", "proof_hash"),
    ("release_pack_id", "scenario_matrix", "event_samples", "api_verification", "assistant_governance"),
    ("metric_id", "queue", "aging_bucket", "risk_driver", "drillthrough_case"),
    ("exception_id", "exception_class", "owner", "sla_due", "escalation_state"),
    ("correction_id", "target_records", "preview", "partial_success_policy", "lineage"),
    ("search_id", "query_scope", "indexed_fields", "saved_filter", "access_scope"),
    ("match_id", "party_alias", "confidence", "review_state", "merge_safeguard"),
    ("document_id", "document_type", "extracted_fields", "source_spans", "confidence"),
    ("archive_id", "record_type", "retention_schedule", "destruction_hold", "retrieval_audit"),
    ("tenant_id", "court_boundary", "policy_scope", "analytics_scope", "release_scope"),
    ("extension_id", "motion_table", "service_table", "exhibit_table", "appellate_packet_table"),
    ("simulation_id", "scenario", "before_after_impact", "exportable_output", "mutation_guard"),
    ("assertion_id", "procedural_path", "assistant_check", "event_replay", "release_gate"),
    ("tracking_id", "judgment_id", "compliance_obligations", "stay_period", "closure_readiness"),
)
REQUIRED_FIELDS: dict[str, tuple[str, ...]] = dict(zip(COURT_CONTROL_CAPABILITIES, FIELD_SETS))
CAPABILITY_TABLES = {
    **{SLUG_BY_NUMBER[i]: COURT_CASE_MANAGEMENT_OWNED_TABLES[0] for i in (1, 18, 19, 20, 24, 46)},
    **{SLUG_BY_NUMBER[i]: COURT_CASE_MANAGEMENT_OWNED_TABLES[6] for i in (2, 11, 12, 28, 43)},
    **{SLUG_BY_NUMBER[i]: COURT_CASE_MANAGEMENT_OWNED_TABLES[1] for i in (3, 4, 6, 25, 32)},
    **{SLUG_BY_NUMBER[i]: COURT_CASE_MANAGEMENT_OWNED_TABLES[5] for i in (5, 15, 16, 42)},
    **{SLUG_BY_NUMBER[i]: COURT_CASE_MANAGEMENT_OWNED_TABLES[8] for i in (7, 27, 50)},
    **{SLUG_BY_NUMBER[i]: COURT_CASE_MANAGEMENT_OWNED_TABLES[3] for i in (8, 9, 23, 26, 34, 35, 48)},
    **{SLUG_BY_NUMBER[i]: COURT_CASE_MANAGEMENT_OWNED_TABLES[9] for i in (10, 33, 36)},
    **{SLUG_BY_NUMBER[i]: COURT_CASE_MANAGEMENT_OWNED_TABLES[2] for i in (13, 44, 47)},
    SLUG_BY_NUMBER[14]: COURT_CASE_MANAGEMENT_OWNED_TABLES[12],
    SLUG_BY_NUMBER[17]: COURT_CASE_MANAGEMENT_OWNED_TABLES[7],
    SLUG_BY_NUMBER[21]: COURT_CASE_MANAGEMENT_OWNED_TABLES[13],
    SLUG_BY_NUMBER[22]: COURT_CASE_MANAGEMENT_OWNED_TABLES[4],
    SLUG_BY_NUMBER[29]: COURT_CASE_MANAGEMENT_OWNED_TABLES[13],
    SLUG_BY_NUMBER[30]: COURT_CASE_MANAGEMENT_OWNED_TABLES[14],
    SLUG_BY_NUMBER[31]: COURT_CASE_MANAGEMENT_OWNED_TABLES[15],
    SLUG_BY_NUMBER[37]: COURT_CASE_MANAGEMENT_OWNED_TABLES[12],
    SLUG_BY_NUMBER[38]: COURT_CASE_MANAGEMENT_OWNED_TABLES[12],
    SLUG_BY_NUMBER[39]: COURT_CASE_MANAGEMENT_OWNED_TABLES[12],
    SLUG_BY_NUMBER[40]: COURT_CASE_MANAGEMENT_OWNED_TABLES[12],
    SLUG_BY_NUMBER[41]: COURT_CASE_MANAGEMENT_OWNED_TABLES[12],
    SLUG_BY_NUMBER[45]: COURT_CASE_MANAGEMENT_OWNED_TABLES[11],
    SLUG_BY_NUMBER[49]: COURT_CASE_MANAGEMENT_OWNED_TABLES[12],
}
CAPABILITY_EVENTS = {capability: "CourtCaseManagement" + "".join(part.capitalize() for part in capability.split("_")) for capability in COURT_CONTROL_CAPABILITIES}
ALLOWED_INTAKE_STATES = {"received", "under_clerk_review", "deficient", "cured", "accepted", "rejected", "stricken"}
ALLOWED_ORDER_STATES = {"draft", "under_review", "signed", "entered", "corrected", "vacated"}
DECLARED_DEPENDENCY_MODES = {"api", "event", "projection", "package_metadata"}
AUTHORIZED_ACCESS_CLASSES = {"public", "redacted", "restricted", "sealed"}


def _digest(value: object) -> str:
    return hashlib.sha256(json.dumps(value, sort_keys=True, default=str).encode("utf-8")).hexdigest()


def _to_float(value: object, default: float = 0.0) -> float:
    try:
        return float(value)
    except (TypeError, ValueError):
        return default


def _invalid_references(references: object) -> tuple[str, ...]:
    if not references:
        return ()
    refs = (references,) if isinstance(references, str) else tuple(str(item) for item in references)
    return tuple(ref for ref in refs if ref.endswith("_table") and not ref.startswith(f"{PBC_KEY}_"))


def _base_checks(capability: str, payload: Mapping[str, object]) -> tuple[bool, tuple[str, ...], tuple[str, ...]]:
    missing = tuple(field for field in REQUIRED_FIELDS[capability] if payload.get(field) in (None, "", (), []))
    invalid = _invalid_references(payload.get("referenced_tables", ()))
    return not missing and not invalid, missing, invalid


def _domain_findings(capability: str, payload: Mapping[str, object]) -> tuple[str, ...]:
    findings: list[str] = []
    if capability == SLUG_BY_NUMBER[1] and (_to_float(payload.get("sequence")) <= 0 or not payload.get("venue")):
        findings.append("case_numbering_requires_positive_sequence_and_venue")
    if capability == SLUG_BY_NUMBER[3] and payload.get("intake_state") not in ALLOWED_INTAKE_STATES:
        findings.append("filing_intake_state_invalid")
    if capability == SLUG_BY_NUMBER[4] and payload.get("parent_filing_id") == payload.get("filing_id"):
        findings.append("amended_filing_cannot_supersede_itself")
    if capability == SLUG_BY_NUMBER[5] and _to_float(payload.get("sequence_number")) <= 0:
        findings.append("docket_entry_requires_positive_sequence")
    if capability == SLUG_BY_NUMBER[7] and payload.get("order_state") == "entered" and not payload.get("signature_metadata"):
        findings.append("entered_order_requires_signature_metadata")
    if capability == SLUG_BY_NUMBER[8] and payload.get("conflict_status") == "double_booked":
        findings.append("hearing_schedule_blocks_double_booked_courtroom")
    if capability == SLUG_BY_NUMBER[10] and not payload.get("calendar_policy"):
        findings.append("deadline_engine_requires_calendar_policy")
    if capability == SLUG_BY_NUMBER[11] and not payload.get("proof_document"):
        findings.append("service_completion_requires_proof_document")
    if capability == SLUG_BY_NUMBER[14] and payload.get("access_class") not in AUTHORIZED_ACCESS_CLASSES:
        findings.append("record_access_class_invalid")
    if capability == SLUG_BY_NUMBER[15] and payload.get("projection_scope") == "public" and payload.get("seal_filter") is not True:
        findings.append("public_docket_projection_requires_seal_filter")
    if capability == SLUG_BY_NUMBER[18] and payload.get("stay_status") == "active" and payload.get("record_packet_status") == "enforcement_ready":
        findings.append("appeal_stay_blocks_enforcement")
    if capability == SLUG_BY_NUMBER[25] and payload.get("confirmation_state") != "requires_human_confirmation":
        findings.append("filing_triage_agent_must_not_auto_commit")
    if capability == SLUG_BY_NUMBER[29] and not payload.get("canonical_routes"):
        findings.append("court_api_surface_requires_canonical_routes")
    if capability == SLUG_BY_NUMBER[30] and payload.get("topic") != COURT_CASE_MANAGEMENT_REQUIRED_EVENT_TOPIC:
        findings.append("procedural_event_must_use_appgen_x_topic")
    if capability == SLUG_BY_NUMBER[31] and not payload.get("idempotency_key"):
        findings.append("inbound_handler_requires_idempotency_key")
    if capability == SLUG_BY_NUMBER[32] and not payload.get("document_hash"):
        findings.append("duplicate_filing_detection_requires_document_hash")
    if capability == SLUG_BY_NUMBER[34] and payload.get("readiness_state") == "confirmed" and payload.get("blockers") not in (None, "", (), []):
        findings.append("hearing_confirmation_blocked_by_open_dependencies")
    if capability == SLUG_BY_NUMBER[36] and payload.get("case_sensitivity") == "sealed" and "view_sealed" not in tuple(payload.get("allowed_actions", ())):
        findings.append("sealed_case_policy_requires_explicit_action")
    if capability == SLUG_BY_NUMBER[37] and not payload.get("proof_hash"):
        findings.append("sealed_access_requires_cryptographic_proof")
    if capability == SLUG_BY_NUMBER[42] and payload.get("query_scope") == "public" and payload.get("access_scope") != "public_only":
        findings.append("public_search_scope_must_exclude_restricted_records")
    if capability == SLUG_BY_NUMBER[44] and _to_float(payload.get("confidence")) < 0.8:
        findings.append("court_document_understanding_requires_review_threshold")
    if capability == SLUG_BY_NUMBER[45] and payload.get("destruction_hold") == "active" and payload.get("retrieval_audit") == "destroy_requested":
        findings.append("destruction_hold_blocks_archive_destruction")
    if capability == SLUG_BY_NUMBER[46] and payload.get("policy_scope") != payload.get("court_boundary"):
        findings.append("court_policy_scope_must_match_tenant_boundary")
    if capability == SLUG_BY_NUMBER[47] and any(str(payload.get(field, "")).endswith("_table") and not str(payload.get(field)).startswith(PBC_KEY) for field in REQUIRED_FIELDS[capability]):
        findings.append("owned_schema_expansion_must_stay_inside_pbc_namespace")
    if capability == SLUG_BY_NUMBER[48] and payload.get("mutation_guard") is not True:
        findings.append("simulation_sandbox_must_be_side_effect_free")
    if capability == SLUG_BY_NUMBER[50] and payload.get("closure_readiness") == "ready" and payload.get("compliance_obligations") not in (None, "", (), []):
        findings.append("case_closure_blocked_by_open_post_judgment_obligations")
    return tuple(findings)


def evaluate_court_control(capability: str, payload: Mapping[str, object] | None = None) -> dict:
    if capability not in COURT_CONTROL_CAPABILITIES:
        return {"ok": False, "pbc": PBC_KEY, "reason": "unknown_court_control", "side_effects": ()}
    payload = dict(payload or {})
    base_ok, missing, invalid = _base_checks(capability, payload)
    findings = _domain_findings(capability, payload)
    table = CAPABILITY_TABLES[capability]
    meta = CAPABILITY_BY_SLUG[capability]
    requires_review = bool(findings or "agent" in capability or "sealed" in capability or "approval" in capability or payload.get("requires_review"))
    return {
        "ok": base_ok,
        "pbc": PBC_KEY,
        "capability": capability,
        "feature_number": meta.feature_number,
        "title": meta.title,
        "status": "ready" if base_ok and not findings else "review_required",
        "target_table": table,
        "owned_tables": (table,),
        "read_tables": (),
        "invalid_references": invalid,
        "missing_required_fields": missing,
        "domain_findings": findings,
        "event": {"event_type": CAPABILITY_EVENTS[capability], "event_contract": EVENT_CONTRACT, "topic": COURT_CASE_MANAGEMENT_REQUIRED_EVENT_TOPIC, "idempotency_key": _digest((capability, payload))},
        "ui_surface": f"{PBC_KEY}.ui.improve1.{capability}",
        "service_api": f"{PBC_KEY}.services.{capability}",
        "route": f"/workbench/pbcs/{PBC_KEY}/improve1/{capability.replace('_', '-')}",
        "permission": f"{PBC_KEY}.{capability}.operate",
        "configuration": {"rule_id": f"{capability}_policy", "parameter_id": f"{capability}_parameter", "database_backends": COURT_CASE_MANAGEMENT_ALLOWED_DATABASE_BACKENDS},
        "agent_skill": f"{PBC_KEY}_skills.{capability}",
        "requires_human_confirmation": requires_review,
        "retry_dead_letter_evidence": {"inbox_table": "court_case_management_appgen_inbox_event", "dead_letter_table": "court_case_management_appgen_dead_letter_event", "max_attempts": 5},
        "release_evidence": {"code_artifact": "court_case_management/court_control.py", "ui_artifact": "court_case_management/ui.py", "service_artifact": "court_case_management/services.py", "test_artifact": "court_case_management/tests/test_domain_behavior.py", "traceability": "court_case_management/IMPROVE1_TRACEABILITY.md"},
        "stream_engine_picker_visible": False,
        "shared_table_access": False,
        "side_effects": (),
    }


def sample_payload_for(capability: str) -> dict:
    if capability not in COURT_CONTROL_CAPABILITIES:
        raise KeyError(capability)
    payload = {field: f"{field}_evidence" for field in REQUIRED_FIELDS[capability]}
    payload["referenced_tables"] = (CAPABILITY_TABLES[capability],)
    if capability == SLUG_BY_NUMBER[1]: payload.update({"sequence": 1, "venue": "civil-division"})
    if capability == SLUG_BY_NUMBER[3]: payload["intake_state"] = "accepted"
    if capability == SLUG_BY_NUMBER[4]: payload.update({"parent_filing_id": "F-1", "filing_id": "F-2"})
    if capability == SLUG_BY_NUMBER[5]: payload["sequence_number"] = 1
    if capability == SLUG_BY_NUMBER[7]: payload.update({"order_state": "signed", "signature_metadata": {"signed_by": "judge"}})
    if capability == SLUG_BY_NUMBER[8]: payload["conflict_status"] = "clear"
    if capability == SLUG_BY_NUMBER[10]: payload["calendar_policy"] = "local-rule-calendar"
    if capability == SLUG_BY_NUMBER[11]: payload["proof_document"] = "proof-of-service.pdf"
    if capability == SLUG_BY_NUMBER[14]: payload["access_class"] = "restricted"
    if capability == SLUG_BY_NUMBER[15]: payload.update({"projection_scope": "public", "seal_filter": True})
    if capability == SLUG_BY_NUMBER[18]: payload.update({"stay_status": "none", "record_packet_status": "assembled"})
    if capability == SLUG_BY_NUMBER[25]: payload["confirmation_state"] = "requires_human_confirmation"
    if capability == SLUG_BY_NUMBER[29]: payload["canonical_routes"] = ("GET /court-cases/{id}/docket", "GET /hearings/calendar")
    if capability == SLUG_BY_NUMBER[30]: payload["topic"] = COURT_CASE_MANAGEMENT_REQUIRED_EVENT_TOPIC
    if capability == SLUG_BY_NUMBER[31]: payload["idempotency_key"] = "inbound-policy-1"
    if capability == SLUG_BY_NUMBER[32]: payload["document_hash"] = "sha256:filing"
    if capability == SLUG_BY_NUMBER[34]: payload.update({"readiness_state": "tentative", "blockers": ("service",)})
    if capability == SLUG_BY_NUMBER[36]: payload.update({"case_sensitivity": "sealed", "allowed_actions": ("view_sealed", "audit_access")})
    if capability == SLUG_BY_NUMBER[37]: payload["proof_hash"] = "sha256:sealed-access"
    if capability == SLUG_BY_NUMBER[42]: payload.update({"query_scope": "public", "access_scope": "public_only"})
    if capability == SLUG_BY_NUMBER[44]: payload["confidence"] = 0.93
    if capability == SLUG_BY_NUMBER[45]: payload.update({"destruction_hold": "none", "retrieval_audit": "retrieved"})
    if capability == SLUG_BY_NUMBER[46]: payload.update({"court_boundary": "court-a", "policy_scope": "court-a"})
    if capability == SLUG_BY_NUMBER[47]: payload.update({"motion_table": "court_case_management_motion", "service_table": "court_case_management_service_record", "exhibit_table": "court_case_management_exhibit_record", "appellate_packet_table": "court_case_management_appellate_packet"})
    if capability == SLUG_BY_NUMBER[48]: payload["mutation_guard"] = True
    if capability == SLUG_BY_NUMBER[50]: payload.update({"closure_readiness": "blocked", "compliance_obligations": ("payment_due",)})
    return payload


def _make_runner(capability: str) -> Callable[[Mapping[str, object] | None], dict]:
    def runner(payload: Mapping[str, object] | None = None) -> dict:
        return evaluate_court_control(capability, payload)
    runner.__name__ = f"run_{capability}"
    return runner

for _capability in COURT_CONTROL_CAPABILITIES:
    globals()[f"run_{_capability}"] = _make_runner(_capability)

COURT_CONTROL_FUNCTIONS: Mapping[str, Callable[[Mapping[str, object] | None], dict]] = {capability: globals()[f"run_{capability}"] for capability in COURT_CONTROL_CAPABILITIES}


def improve1_court_control_contract() -> dict:
    samples = tuple(COURT_CONTROL_FUNCTIONS[capability](sample_payload_for(capability)) for capability in COURT_CONTROL_CAPABILITIES)
    return {"format": "appgen.court-case-management.improve1-court-control.v1", "ok": len(samples) == 50 and all(item["ok"] for item in samples), "pbc": PBC_KEY, "capability_count": len(COURT_CONTROL_CAPABILITIES), "capabilities": COURT_CONTROL_CAPABILITIES, "owned_tables": COURT_CASE_MANAGEMENT_OWNED_TABLES, "event_contract": EVENT_CONTRACT, "database_backends": COURT_CASE_MANAGEMENT_ALLOWED_DATABASE_BACKENDS, "stream_engine_picker_visible": False, "shared_table_access": False, "samples": samples, "side_effects": ()}
