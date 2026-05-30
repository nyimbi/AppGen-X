"""Executable contract lifecycle controls for improve1 execution.

Every function here is side-effect free and maps one improve1 CLM capability to
owned contract tables, AppGen-X events, UI/API surfaces, agent skills,
configuration handles, retry/dead-letter evidence, and traceability artifacts.
"""

from __future__ import annotations

import hashlib
import json
from typing import Callable, Mapping

from .application import ALLOWED_DATABASE_BACKENDS, OWNED_TABLES, PBC_KEY, REQUIRED_EVENT_TOPIC
from .improve1_capabilities import IMPROVE1_CAPABILITIES

EVENT_CONTRACT = "AppGen-X"
CONTRACT_CONTROL_CAPABILITIES = tuple(capability.slug for capability in IMPROVE1_CAPABILITIES)
SLUG_BY_NUMBER = {capability.feature_number: capability.slug for capability in IMPROVE1_CAPABILITIES}
CAPABILITY_BY_SLUG = {capability.slug: capability for capability in IMPROVE1_CAPABILITIES}
FIELD_SETS: tuple[tuple[str, ...], ...] = (
    ("request_purpose", "counterparty", "contract_type", "jurisdiction", "source_documents"),
    ("current_state", "target_state", "required_evidence", "owner", "permission"),
    ("contract_type", "category", "jurisdiction", "taxonomy_version", "mandatory_clauses"),
    ("party_role", "legal_identity", "authority_state", "jurisdiction", "projection_source"),
    ("signer", "title", "identity_verified", "authority_evidence", "delegation_state"),
    ("clause_family", "approved_language", "jurisdiction", "effective_date", "owner"),
    ("variant_code", "risk_tier", "fallback_text", "approval_requirement", "boundary_status"),
    ("document_id", "clause_families", "source_citations", "confidence", "reviewer"),
    ("clause_family", "semantic_distance", "risk_category", "financial_exposure", "approval_route"),
    ("packet_id", "file_fingerprints", "exhibits", "cross_reference_status", "final_hash"),
    ("workspace_id", "template_lineage", "clause_set", "collaborators", "locked_sections"),
    ("template_code", "contract_type", "jurisdiction", "risk_flags", "selection_rationale"),
    ("round_id", "sender", "receiver", "document_version", "response_due_date"),
    ("redline_id", "changed_clause", "semantic_effect", "risk_score", "fallback_status"),
    ("policy_id", "thresholds", "approver_roles", "rule_version", "route_rationale"),
    ("task_id", "approver", "due_date", "sla_hours", "escalation_path"),
    ("requester", "approver", "signer", "conflict_check", "override_evidence"),
    ("packet_id", "final_document_hash", "signers", "routing_order", "authentication_evidence"),
    ("proof_id", "document_hash", "approval_hash", "signature_hash", "verifier_export"),
    ("obligation_code", "contract_id", "owner", "due_date", "evidence_requirement"),
    ("performance_id", "obligation_id", "evidence_artifact", "reviewer", "completeness"),
    ("assertion_id", "obligation_population", "overdue_count", "missing_evidence", "exception_owner"),
    ("milestone_id", "owner", "lead_time_days", "notice_requirement", "completion_evidence"),
    ("renewal_id", "recommendation", "value_snapshot", "risk_score", "notice_window"),
    ("notice_id", "earliest_notice_date", "latest_notice_date", "recipient", "proof_requirement"),
    ("amendment_id", "affected_clauses", "changed_obligations", "value_impact", "signature_requirement"),
    ("check_id", "check_type", "population", "pass_fail", "evidence"),
    ("counterparty", "financial_risk", "sanctions_flag", "performance_score", "recommended_protection"),
    ("simulation_id", "failure_scenario", "obligation_impact", "financial_exposure", "mitigation"),
    ("snapshot_id", "amount", "currency", "term", "confidence"),
    ("index_id", "extracted_clauses", "metadata", "permissions", "legal_hold_filter"),
    ("anomaly_id", "signal", "template", "counterparty", "exception_case"),
    ("retention_id", "retention_category", "legal_hold_state", "destruction_eligibility", "approval"),
    ("privacy_clause", "data_transfer", "security_control", "breach_notice", "specialist_approval"),
    ("insurance_requirement", "certificate_due_date", "coverage_amount", "indemnity_cap", "renewal_need"),
    ("commercial_term", "amount", "currency", "payment_timing", "source_citation"),
    ("playbook_id", "governing_law", "mandatory_clauses", "fallback_positions", "local_counsel_route"),
    ("language_variant", "controlling_language", "translation_certification", "alignment_status", "reviewer"),
    ("case_id", "exception_type", "severity", "owner", "closure_proof"),
    ("policy_change_id", "affected_contracts", "active_obligations", "renewal_impact", "required_action"),
    ("event_type", "schema_version", "idempotency_key", "retry_envelope", "dead_letter_taxonomy"),
    ("dependency", "dependency_mode", "cached_field", "freshness_rule", "retention_rule"),
    ("intake_document", "proposed_record", "source_citations", "confidence", "approval_required"),
    ("redline_packet", "approved_variant", "material_deviations", "negotiation_position", "authorized_confirmation"),
    ("obligation_extract", "owner_suggestion", "recurrence", "performance_proof", "review_state"),
    ("command_center", "queue_status", "approval_bottlenecks", "signature_failures", "dead_letters"),
    ("surface_id", "domain_operations", "ui_fragments", "agent_tools", "coverage_result"),
    ("drill_id", "failure_mode", "recovery_time_minutes", "affected_contracts", "replay_plan"),
    ("score_id", "template_coverage", "event_health", "boundary_proof", "agent_safety"),
    ("proof_id", "intake_to_signature", "obligation_to_renewal", "amendment_path", "boundary_verification"),
)
REQUIRED_FIELDS: dict[str, tuple[str, ...]] = dict(zip(CONTRACT_CONTROL_CAPABILITIES, FIELD_SETS))
CAPABILITY_TABLES = {
    **{SLUG_BY_NUMBER[i]: OWNED_TABLES[0] for i in (1, 2, 3, 12, 24, 29, 30, 33, 40, 42, 43, 49, 50)},
    **{SLUG_BY_NUMBER[i]: OWNED_TABLES[1] for i in (4, 5, 28)},
    **{SLUG_BY_NUMBER[i]: OWNED_TABLES[2] for i in (6, 8, 34, 35, 36, 37, 38)},
    SLUG_BY_NUMBER[7]: OWNED_TABLES[3],
    SLUG_BY_NUMBER[9]: OWNED_TABLES[7],
    SLUG_BY_NUMBER[10]: OWNED_TABLES[4],
    SLUG_BY_NUMBER[11]: OWNED_TABLES[5],
    SLUG_BY_NUMBER[13]: OWNED_TABLES[6],
    SLUG_BY_NUMBER[14]: OWNED_TABLES[7],
    SLUG_BY_NUMBER[15]: OWNED_TABLES[8],
    SLUG_BY_NUMBER[16]: OWNED_TABLES[9],
    SLUG_BY_NUMBER[17]: OWNED_TABLES[24],
    SLUG_BY_NUMBER[18]: OWNED_TABLES[10],
    SLUG_BY_NUMBER[19]: OWNED_TABLES[24],
    SLUG_BY_NUMBER[20]: OWNED_TABLES[11],
    SLUG_BY_NUMBER[21]: OWNED_TABLES[12],
    SLUG_BY_NUMBER[22]: OWNED_TABLES[24],
    SLUG_BY_NUMBER[23]: OWNED_TABLES[13],
    SLUG_BY_NUMBER[25]: OWNED_TABLES[14],
    SLUG_BY_NUMBER[26]: OWNED_TABLES[15],
    SLUG_BY_NUMBER[27]: OWNED_TABLES[16],
    SLUG_BY_NUMBER[31]: OWNED_TABLES[19],
    SLUG_BY_NUMBER[32]: OWNED_TABLES[20],
    SLUG_BY_NUMBER[39]: OWNED_TABLES[20],
    SLUG_BY_NUMBER[41]: OWNED_TABLES[27],
    SLUG_BY_NUMBER[44]: OWNED_TABLES[25],
    SLUG_BY_NUMBER[45]: OWNED_TABLES[25],
    SLUG_BY_NUMBER[46]: OWNED_TABLES[20],
    SLUG_BY_NUMBER[47]: OWNED_TABLES[24],
    SLUG_BY_NUMBER[48]: OWNED_TABLES[28],
}
CAPABILITY_EVENTS = {
    capability: "ContractLifecycle" + "".join(part.capitalize() for part in capability.split("_"))
    for capability in CONTRACT_CONTROL_CAPABILITIES
}
ALLOWED_STATES = {"draft", "intake_ready", "authoring", "negotiation", "approval_pending", "approved", "active", "renewal_pending", "amended", "expired", "terminated", "archived"}
DECLARED_DEPENDENCY_MODES = {"api", "event", "projection", "package_metadata"}
AUTHORIZED_CONFIRMATIONS = {True, "authorized", "approved"}


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
    if capability == SLUG_BY_NUMBER[1] and not payload.get("source_documents"):
        findings.append("intake_requires_source_documents")
    if capability == SLUG_BY_NUMBER[2] and payload.get("target_state") not in ALLOWED_STATES:
        findings.append("invalid_contract_lifecycle_transition_target")
    if capability == SLUG_BY_NUMBER[5] and payload.get("identity_verified") is not True:
        findings.append("signing_authority_requires_verified_identity")
    if capability == SLUG_BY_NUMBER[8] and (_to_float(payload.get("confidence")) < 0.8 or not payload.get("source_citations")):
        findings.append("semantic_clause_extraction_requires_citations_and_confidence")
    if capability == SLUG_BY_NUMBER[9] and _to_float(payload.get("risk_score")) > 0.75 and payload.get("approval_route") in (None, "standard"):
        findings.append("material_clause_deviation_requires_specialist_approval")
    if capability == SLUG_BY_NUMBER[10] and not payload.get("final_hash"):
        findings.append("document_packet_requires_final_integrity_hash")
    if capability == SLUG_BY_NUMBER[15] and not payload.get("route_rationale"):
        findings.append("approval_policy_requires_route_rationale")
    if capability == SLUG_BY_NUMBER[17] and payload.get("requester") == payload.get("approver") and not payload.get("override_evidence"):
        findings.append("segregation_of_duty_blocks_self_approval")
    if capability == SLUG_BY_NUMBER[18] and not payload.get("final_document_hash"):
        findings.append("signature_packet_requires_final_document_hash")
    if capability == SLUG_BY_NUMBER[20] and not payload.get("evidence_requirement"):
        findings.append("obligation_activation_requires_evidence_requirement")
    if capability == SLUG_BY_NUMBER[22] and _to_float(payload.get("overdue_count")) > 0 and not payload.get("exception_owner"):
        findings.append("overdue_obligations_require_exception_owner")
    if capability == SLUG_BY_NUMBER[25] and not payload.get("proof_requirement"):
        findings.append("renewal_notice_requires_proof_requirement")
    if capability == SLUG_BY_NUMBER[26] and payload.get("signature_requirement") == "missing":
        findings.append("amendment_signature_requirement_unresolved")
    if capability == SLUG_BY_NUMBER[31] and payload.get("legal_hold_filter") is not True:
        findings.append("search_must_enforce_legal_hold_filter")
    if capability == SLUG_BY_NUMBER[33] and payload.get("legal_hold_state") == "active" and payload.get("destruction_eligibility") is True:
        findings.append("legal_hold_blocks_destruction")
    if capability == SLUG_BY_NUMBER[38] and payload.get("alignment_status") not in {"aligned", "reviewed"}:
        findings.append("multilanguage_contract_requires_clause_alignment")
    if capability == SLUG_BY_NUMBER[41] and (not payload.get("idempotency_key") or not payload.get("dead_letter_taxonomy")):
        findings.append("event_reliability_requires_idempotency_and_dead_letter_taxonomy")
    if capability == SLUG_BY_NUMBER[42] and payload.get("dependency_mode") not in DECLARED_DEPENDENCY_MODES:
        findings.append("cross_pbc_boundary_must_use_api_event_or_projection")
    if capability == SLUG_BY_NUMBER[43] and (_to_float(payload.get("confidence")) < 0.8 or payload.get("approval_required") is not True):
        findings.append("agent_intake_requires_confidence_and_approval")
    if capability == SLUG_BY_NUMBER[44] and payload.get("authorized_confirmation") not in AUTHORIZED_CONFIRMATIONS:
        findings.append("agent_redline_review_cannot_accept_without_authorized_confirmation")
    if capability == SLUG_BY_NUMBER[45] and payload.get("review_state") != "review_ready":
        findings.append("agent_obligation_activation_remains_reviewable")
    if capability == SLUG_BY_NUMBER[48] and _to_float(payload.get("recovery_time_minutes")) > 60:
        findings.append("resilience_drill_exceeds_recovery_target")
    if capability == SLUG_BY_NUMBER[49] and payload.get("agent_safety") is not True:
        findings.append("readiness_score_requires_agent_safety")
    if capability == SLUG_BY_NUMBER[50] and payload.get("boundary_verification") is not True:
        findings.append("end_to_end_release_proof_requires_boundary_verification")
    return tuple(findings)


def evaluate_contract_control(capability: str, payload: Mapping[str, object] | None = None) -> dict:
    if capability not in CONTRACT_CONTROL_CAPABILITIES:
        return {"ok": False, "pbc": PBC_KEY, "reason": "unknown_contract_control", "side_effects": ()}
    payload = dict(payload or {})
    base_ok, missing, invalid = _base_checks(capability, payload)
    findings = _domain_findings(capability, payload)
    table = CAPABILITY_TABLES[capability]
    meta = CAPABILITY_BY_SLUG[capability]
    requires_review = bool(findings or "agent" in capability or "approval" in capability or "signature" in capability or payload.get("requires_review"))
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
        "event": {
            "event_type": CAPABILITY_EVENTS[capability],
            "event_contract": EVENT_CONTRACT,
            "topic": REQUIRED_EVENT_TOPIC,
            "idempotency_key": _digest((capability, payload)),
        },
        "ui_surface": f"{PBC_KEY}.ui.improve1.{capability}",
        "service_api": f"{PBC_KEY}.services.{capability}",
        "route": f"/workbench/pbcs/{PBC_KEY}/improve1/{capability.replace('_', '-')}",
        "permission": f"{PBC_KEY}.{capability}.operate",
        "configuration": {
            "rule_id": f"{capability}_policy",
            "parameter_id": f"{capability}_parameter",
            "database_backends": ALLOWED_DATABASE_BACKENDS,
        },
        "agent_skill": f"{PBC_KEY}_skills.{capability}",
        "requires_human_confirmation": requires_review,
        "retry_dead_letter_evidence": {
            "inbox_table": "contract_lifecycle_appgen_inbox_event",
            "dead_letter_table": "contract_lifecycle_appgen_dead_letter_event",
            "max_attempts": 5,
        },
        "release_evidence": {
            "code_artifact": "contract_lifecycle/contract_control.py",
            "ui_artifact": "contract_lifecycle/ui.py",
            "service_artifact": "contract_lifecycle/services.py",
            "test_artifact": "contract_lifecycle/tests/test_domain_behavior.py",
            "traceability": "contract_lifecycle/IMPROVE1_TRACEABILITY.md",
        },
        "stream_engine_picker_visible": False,
        "shared_table_access": False,
        "side_effects": (),
    }


def sample_payload_for(capability: str) -> dict:
    if capability not in CONTRACT_CONTROL_CAPABILITIES:
        raise KeyError(capability)
    payload = {field: f"{field}_evidence" for field in REQUIRED_FIELDS[capability]}
    payload["referenced_tables"] = (CAPABILITY_TABLES[capability],)
    if capability == SLUG_BY_NUMBER[1]:
        payload.update({"source_documents": ("msa.docx",), "contract_type": "MSA", "jurisdiction": "UK"})
    if capability == SLUG_BY_NUMBER[2]:
        payload.update({"current_state": "draft", "target_state": "intake_ready"})
    if capability == SLUG_BY_NUMBER[5]:
        payload.update({"identity_verified": True, "authority_evidence": "board-resolution"})
    if capability == SLUG_BY_NUMBER[8]:
        payload.update({"confidence": 0.94, "source_citations": ("page:2",)})
    if capability == SLUG_BY_NUMBER[9]:
        payload.update({"risk_score": 0.3, "approval_route": "standard"})
    if capability == SLUG_BY_NUMBER[10]:
        payload["final_hash"] = "sha256:packet"
    if capability == SLUG_BY_NUMBER[15]:
        payload["route_rationale"] = "value and risk based"
    if capability == SLUG_BY_NUMBER[17]:
        payload.update({"requester": "sales.ops", "approver": "legal.manager", "override_evidence": "not_required"})
    if capability == SLUG_BY_NUMBER[18]:
        payload["final_document_hash"] = "sha256:final"
    if capability == SLUG_BY_NUMBER[20]:
        payload["evidence_requirement"] = "certificate_required"
    if capability == SLUG_BY_NUMBER[22]:
        payload.update({"overdue_count": 0, "exception_owner": "legal.ops"})
    if capability == SLUG_BY_NUMBER[25]:
        payload["proof_requirement"] = "certified_notice"
    if capability == SLUG_BY_NUMBER[26]:
        payload["signature_requirement"] = "required"
    if capability == SLUG_BY_NUMBER[31]:
        payload["legal_hold_filter"] = True
    if capability == SLUG_BY_NUMBER[33]:
        payload.update({"legal_hold_state": "none", "destruction_eligibility": False})
    if capability == SLUG_BY_NUMBER[38]:
        payload["alignment_status"] = "aligned"
    if capability == SLUG_BY_NUMBER[41]:
        payload.update({"idempotency_key": "evt-clm-1", "dead_letter_taxonomy": "unknown_event|schema_error|retry_exhausted"})
    if capability == SLUG_BY_NUMBER[42]:
        payload.update({"dependency_mode": "projection", "freshness_rule": "24h"})
    if capability == SLUG_BY_NUMBER[43]:
        payload.update({"confidence": 0.93, "approval_required": True, "source_citations": ("page:1",)})
    if capability == SLUG_BY_NUMBER[44]:
        payload["authorized_confirmation"] = True
    if capability == SLUG_BY_NUMBER[45]:
        payload["review_state"] = "review_ready"
    if capability == SLUG_BY_NUMBER[48]:
        payload["recovery_time_minutes"] = 20
    if capability == SLUG_BY_NUMBER[49]:
        payload["agent_safety"] = True
    if capability == SLUG_BY_NUMBER[50]:
        payload["boundary_verification"] = True
    return payload


def _make_runner(capability: str) -> Callable[[Mapping[str, object] | None], dict]:
    def runner(payload: Mapping[str, object] | None = None) -> dict:
        return evaluate_contract_control(capability, payload)

    runner.__name__ = f"run_{capability}"
    return runner


for _capability in CONTRACT_CONTROL_CAPABILITIES:
    globals()[f"run_{_capability}"] = _make_runner(_capability)

CONTRACT_CONTROL_FUNCTIONS: Mapping[str, Callable[[Mapping[str, object] | None], dict]] = {
    capability: globals()[f"run_{capability}"] for capability in CONTRACT_CONTROL_CAPABILITIES
}


def improve1_contract_control_contract() -> dict:
    samples = tuple(CONTRACT_CONTROL_FUNCTIONS[capability](sample_payload_for(capability)) for capability in CONTRACT_CONTROL_CAPABILITIES)
    return {
        "format": "appgen.contract-lifecycle.improve1-contract-control.v1",
        "ok": len(samples) == 50 and all(item["ok"] for item in samples),
        "pbc": PBC_KEY,
        "capability_count": len(CONTRACT_CONTROL_CAPABILITIES),
        "capabilities": CONTRACT_CONTROL_CAPABILITIES,
        "owned_tables": OWNED_TABLES,
        "event_contract": EVENT_CONTRACT,
        "database_backends": ALLOWED_DATABASE_BACKENDS,
        "stream_engine_picker_visible": False,
        "shared_table_access": False,
        "samples": samples,
        "side_effects": (),
    }
