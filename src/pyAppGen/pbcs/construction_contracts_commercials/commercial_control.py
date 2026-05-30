"""Executable construction commercial controls for improve1 execution.

Every function here is side-effect free and maps one improve1 capability to
owned commercial tables, AppGen-X event metadata, UI/API surfaces, agent skills,
configuration handles, retry/dead-letter evidence, and traceability artifacts.
"""

from __future__ import annotations

from datetime import date, datetime
import hashlib
import json
from typing import Callable, Mapping

PBC_KEY = "construction_contracts_commercials"
EVENT_CONTRACT = "AppGen-X"
OWNED_TABLES = (
    "construction_contracts_commercials_construction_contract",
    "construction_contracts_commercials_pay_application",
    "construction_contracts_commercials_retainage",
    "construction_contracts_commercials_variation_order",
    "construction_contracts_commercials_commercial_claim",
    "construction_contracts_commercials_lien_waiver",
    "construction_contracts_commercials_subcontract_package",
    "construction_contracts_commercials_construction_contracts_commercials_policy_rule",
    "construction_contracts_commercials_construction_contracts_commercials_runtime_parameter",
    "construction_contracts_commercials_construction_contracts_commercials_schema_extension",
    "construction_contracts_commercials_construction_contracts_commercials_control_assertion",
    "construction_contracts_commercials_construction_contracts_commercials_governed_model",
    "construction_contracts_commercials_appgen_outbox_event",
    "construction_contracts_commercials_appgen_inbox_event",
    "construction_contracts_commercials_appgen_dead_letter_event",
)
COMMERCIAL_CONTROL_CAPABILITIES = (
    "contract_commercial_lifecycle",
    "contract_type_and_pricing_basis",
    "scope_and_schedule_of_values",
    "pay_application_intake",
    "progress_measurement_evidence",
    "retainage_rules",
    "advance_payment_and_recovery",
    "variation_order_lifecycle",
    "change_notice_timeliness",
    "commercial_claim_register",
    "delay_and_time_impact_boundary",
    "quantum_calculation",
    "subcontract_package_lifecycle",
    "lien_waiver_governance",
    "bonds_and_guarantees",
    "insurance_compliance",
    "backcharge_and_contra_charge",
    "liquidated_damages_and_incentives",
    "provisional_sums_and_allowances",
    "escalation_and_price_adjustment",
    "tax_and_withholding_boundary",
    "payment_certificate_generation",
    "final_account_workflow",
    "dispute_and_determination_tracking",
    "commercial_correspondence_evidence",
    "contract_clause_obligation_register",
    "commercial_risk_register",
    "forecast_final_cost_boundary",
    "cash_flow_forecast",
    "contractor_performance_scorecard",
    "commercial_controls_workbench",
    "agent_assisted_contract_review",
    "governed_agent_crud_commands",
    "commercial_document_ingestion",
    "change_impact_simulation",
    "continuous_control_assertions",
    "dead_letter_and_retry_operations",
    "cryptographic_commercial_evidence",
    "role_based_permission_model",
    "contractor_portal_contract",
    "lien_and_statutory_compliance_localization",
    "commercial_claim_analytics",
    "variation_trend_analytics",
    "final_account_evidence_packet",
    "financial_handoff_boundary",
    "sustainability_and_local_content_clauses",
    "seeded_commercial_scenario_library",
    "full_commercial_release_simulation",
    "package_overlap_guardrails",
    "composition_dsl_and_unified_agent_exposure",
)
REQUIRED_FIELDS: dict[str, tuple[str, ...]] = {
    "contract_commercial_lifecycle": ("current_stage", "target_stage", "effective_date", "responsible_party", "required_evidence"),
    "contract_type_and_pricing_basis": ("contract_type", "pricing_basis", "measurement_rule", "risk_allocation", "escalation_rule"),
    "scope_and_schedule_of_values": ("work_package", "original_value", "approved_changes", "current_claimed", "remaining_balance"),
    "pay_application_intake": ("intake_state", "application_number", "attachments", "claimed_amount", "certification_state"),
    "progress_measurement_evidence": ("measurement_method", "progress_evidence", "certifier", "field_verification", "variance_reason"),
    "retainage_rules": ("retainage_percent", "cap", "withheld_amount", "release_trigger", "waiver_requirement"),
    "advance_payment_and_recovery": ("advance_amount", "guarantee_evidence", "recovery_percent", "recovered_to_date", "guarantee_expiry"),
    "variation_order_lifecycle": ("instruction_source", "cost_impact", "time_impact", "approval_route", "executed_amount"),
    "change_notice_timeliness": ("notice_date", "event_date", "contractual_deadline", "waiver_status", "entitlement_risk"),
    "commercial_claim_register": ("claim_type", "causation_event", "notice_evidence", "quantum_basis", "settlement_state"),
    "delay_and_time_impact_boundary": ("schedule_projection", "critical_path_evidence", "delay_window", "concurrent_delay", "freshness"),
    "quantum_calculation": ("cost_category", "rate", "quantity", "source_evidence", "negotiated_amount"),
    "subcontract_package_lifecycle": ("package_scope", "subcontractor_projection", "contract_value", "insurance_status", "bond_status"),
    "lien_waiver_governance": ("waiver_type", "covered_amount", "covered_period", "party", "conditional_status"),
    "bonds_and_guarantees": ("guarantee_type", "issuer", "value", "expiry", "beneficiary"),
    "insurance_compliance": ("coverage_type", "limit", "deductible", "expiry", "endorsement"),
    "backcharge_and_contra_charge": ("case_number", "responsible_party", "notice", "cost_evidence", "dispute_state"),
    "liquidated_damages_and_incentives": ("rule", "trigger_evidence", "grace_period", "cap", "assessed_amount"),
    "provisional_sums_and_allowances": ("allowance_code", "original_value", "committed_amount", "approved_draw", "remaining_balance"),
    "escalation_and_price_adjustment": ("formula", "index_projection", "base_date", "calculation_period", "assessed_amount"),
    "tax_and_withholding_boundary": ("tax_projection", "withholding_status", "exemption_evidence", "freshness", "payment_certification"),
    "payment_certificate_generation": ("contract_value", "previous_payments", "variations", "retainage", "net_due"),
    "final_account_workflow": ("final_account_checklist", "agreed_contract_sum", "outstanding_matters", "settlement_terms", "signoff"),
    "dispute_and_determination_tracking": ("forum", "disputed_amount", "issues", "decision", "financial_impact"),
    "commercial_correspondence_evidence": ("source_document", "sender", "recipient", "contract_clause", "reviewer"),
    "contract_clause_obligation_register": ("clause", "responsible_party", "due_date", "trigger", "noncompliance_consequence"),
    "commercial_risk_register": ("exposure_value", "probability", "driver", "owner", "mitigation"),
    "forecast_final_cost_boundary": ("cost_forecast_projection", "committed_value", "approved_changes", "pending_changes", "confidence"),
    "cash_flow_forecast": ("contract", "period", "certified_amount", "expected_payment_date", "confidence"),
    "contractor_performance_scorecard": ("variation_cycle_time", "claim_substantiation", "pay_app_rejection_rate", "compliance_holds", "closeout_aging"),
    "commercial_controls_workbench": ("pay_app_queue", "missing_waivers", "expiring_guarantees", "notice_deadlines", "final_account_blockers"),
    "agent_assisted_contract_review": ("summary_type", "citations", "source_records", "human_approval", "commercial_decision_flag"),
    "governed_agent_crud_commands": ("intent", "contract_identity", "evidence", "preview", "confirmation"),
    "commercial_document_ingestion": ("document_type", "source_spans", "extracted_fields", "confidence", "reviewer"),
    "change_impact_simulation": ("rule_change", "affected_payments", "retained_cash", "claims_exposure", "approval_tier"),
    "continuous_control_assertions": ("population", "threshold", "failing_records", "owner", "remediation"),
    "dead_letter_and_retry_operations": ("retry_reason", "risk", "idempotency_key", "replay_checkpoint", "remediation_action"),
    "cryptographic_commercial_evidence": ("contract_hash", "certificate_hash", "variation_hash", "claim_hash", "final_account_hash"),
    "role_based_permission_model": ("role", "certify_permission", "variation_permission", "claim_permission", "closeout_permission"),
    "contractor_portal_contract": ("portal_scope", "submission_type", "contract_scope", "status_view", "internal_notes_redaction"),
    "lien_and_statutory_compliance_localization": ("jurisdiction", "waiver_rule", "prompt_payment_rule", "retention_limit", "policy_version"),
    "commercial_claim_analytics": ("claim_type", "root_cause", "substantiation_quality", "settlement_ratio", "cycle_time"),
    "variation_trend_analytics": ("variation_source", "value_growth", "cycle_time", "pending_exposure", "threshold"),
    "final_account_evidence_packet": ("contract_summary", "payment_history", "variations", "claims", "signoffs"),
    "financial_handoff_boundary": ("payable_event", "retainage_event", "deduction_event", "settlement_event", "idempotency_key"),
    "sustainability_and_local_content_clauses": ("clause_obligation", "measurement_evidence", "reporting_cadence", "noncompliance_consequence", "commercial_impact"),
    "seeded_commercial_scenario_library": ("pay_application_seed", "retainage_release_seed", "variation_seed", "delay_claim_seed", "final_account_seed"),
    "full_commercial_release_simulation": ("contract_activation", "pay_certification", "retainage_withheld", "variation_approved", "final_account_closed"),
    "package_overlap_guardrails": ("project_status_dependency", "schedule_dependency", "cost_dependency", "finance_dependency", "document_dependency"),
    "composition_dsl_and_unified_agent_exposure": ("models", "routes", "services", "event_contracts", "assistant_skills"),
}
CAPABILITY_TABLES = {
    "contract_commercial_lifecycle": OWNED_TABLES[0],
    "contract_type_and_pricing_basis": OWNED_TABLES[0],
    "scope_and_schedule_of_values": OWNED_TABLES[0],
    "pay_application_intake": OWNED_TABLES[1],
    "progress_measurement_evidence": OWNED_TABLES[1],
    "retainage_rules": OWNED_TABLES[2],
    "advance_payment_and_recovery": OWNED_TABLES[2],
    "variation_order_lifecycle": OWNED_TABLES[3],
    "change_notice_timeliness": OWNED_TABLES[3],
    "commercial_claim_register": OWNED_TABLES[4],
    "delay_and_time_impact_boundary": OWNED_TABLES[4],
    "quantum_calculation": OWNED_TABLES[4],
    "subcontract_package_lifecycle": OWNED_TABLES[6],
    "lien_waiver_governance": OWNED_TABLES[5],
    "bonds_and_guarantees": OWNED_TABLES[0],
    "insurance_compliance": OWNED_TABLES[6],
    "backcharge_and_contra_charge": OWNED_TABLES[4],
    "liquidated_damages_and_incentives": OWNED_TABLES[0],
    "provisional_sums_and_allowances": OWNED_TABLES[0],
    "escalation_and_price_adjustment": OWNED_TABLES[1],
    "tax_and_withholding_boundary": OWNED_TABLES[12],
    "payment_certificate_generation": OWNED_TABLES[1],
    "final_account_workflow": OWNED_TABLES[0],
    "dispute_and_determination_tracking": OWNED_TABLES[4],
    "commercial_correspondence_evidence": OWNED_TABLES[9],
    "contract_clause_obligation_register": OWNED_TABLES[10],
    "commercial_risk_register": OWNED_TABLES[10],
    "forecast_final_cost_boundary": OWNED_TABLES[12],
    "cash_flow_forecast": OWNED_TABLES[10],
    "contractor_performance_scorecard": OWNED_TABLES[10],
    "commercial_controls_workbench": OWNED_TABLES[10],
    "agent_assisted_contract_review": OWNED_TABLES[11],
    "governed_agent_crud_commands": OWNED_TABLES[11],
    "commercial_document_ingestion": OWNED_TABLES[9],
    "change_impact_simulation": OWNED_TABLES[7],
    "continuous_control_assertions": OWNED_TABLES[10],
    "dead_letter_and_retry_operations": OWNED_TABLES[14],
    "cryptographic_commercial_evidence": OWNED_TABLES[10],
    "role_based_permission_model": OWNED_TABLES[7],
    "contractor_portal_contract": OWNED_TABLES[0],
    "lien_and_statutory_compliance_localization": OWNED_TABLES[7],
    "commercial_claim_analytics": OWNED_TABLES[10],
    "variation_trend_analytics": OWNED_TABLES[10],
    "final_account_evidence_packet": OWNED_TABLES[10],
    "financial_handoff_boundary": OWNED_TABLES[12],
    "sustainability_and_local_content_clauses": OWNED_TABLES[0],
    "seeded_commercial_scenario_library": OWNED_TABLES[10],
    "full_commercial_release_simulation": OWNED_TABLES[10],
    "package_overlap_guardrails": OWNED_TABLES[10],
    "composition_dsl_and_unified_agent_exposure": OWNED_TABLES[11],
}
CAPABILITY_EVENTS = {capability: "ConstructionCommercial" + "".join(part.capitalize() for part in capability.split("_")) for capability in COMMERCIAL_CONTROL_CAPABILITIES}
ALLOWED_CONTRACT_STAGES = {"tender", "award", "execution", "variation", "suspension", "practical_completion", "final_account", "defects", "closeout"}
ALLOWED_PRICING_BASES = {"lump_sum", "unit_rate", "cost_plus", "guaranteed_maximum", "target_cost", "framework", "reimbursable"}
DECLARED_DEPENDENCY_MODES = {"api", "event", "projection", "package_metadata"}
AUTHORIZED_ROLES = {"contract_admin", "quantity_surveyor", "commercial_manager", "project_manager", "finance_user", "legal_user", "auditor"}


def _digest(value: object) -> str:
    return hashlib.sha256(json.dumps(value, sort_keys=True, default=str).encode("utf-8")).hexdigest()


def _age_days(value: object) -> int | None:
    if not value:
        return None
    if isinstance(value, datetime):
        parsed = value.date()
    elif isinstance(value, date):
        parsed = value
    else:
        try:
            parsed = date.fromisoformat(str(value)[:10])
        except ValueError:
            return None
    return (date(2026, 5, 30) - parsed).days


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
    if capability == "contract_commercial_lifecycle" and payload.get("target_stage") not in ALLOWED_CONTRACT_STAGES:
        findings.append("invalid_contract_lifecycle_stage")
    if capability == "contract_type_and_pricing_basis" and payload.get("pricing_basis") not in ALLOWED_PRICING_BASES:
        findings.append("unsupported_pricing_basis")
    if capability == "scope_and_schedule_of_values" and float(payload.get("current_claimed", 0) or 0) > float(payload.get("remaining_balance", 0) or 0):
        findings.append("schedule_of_values_overclaim")
    if capability == "pay_application_intake" and payload.get("certification_state") != "certified" and payload.get("payment_event_requested") is True:
        findings.append("payment_event_blocked_until_certified")
    if capability == "progress_measurement_evidence" and payload.get("progress_evidence") == "missing":
        findings.append("progress_evidence_required_for_certification")
    if capability == "retainage_rules" and payload.get("release_trigger") == "final" and payload.get("waiver_requirement") != "satisfied":
        findings.append("retainage_release_blocked_by_waiver")
    if capability == "advance_payment_and_recovery" and _age_days(payload.get("guarantee_expiry")) not in (None,) and _age_days(payload.get("guarantee_expiry")) > 0:
        findings.append("advance_guarantee_expired")
    if capability == "variation_order_lifecycle" and payload.get("approval_route") != "approved" and float(payload.get("executed_amount", 0) or 0) > 0:
        findings.append("unapproved_variation_cannot_increase_contract_value")
    if capability == "change_notice_timeliness":
        event_age = _age_days(payload.get("event_date"))
        notice_age = _age_days(payload.get("notice_date"))
        deadline = int(payload.get("contractual_deadline", 0) or 0)
        if event_age is not None and notice_age is not None and notice_age < event_age - deadline and payload.get("waiver_status") != "waived":
            findings.append("notice_time_bar_risk")
    if capability == "lien_waiver_governance" and payload.get("conditional_status") not in {"valid", "not_required"}:
        findings.append("payment_blocked_by_invalid_lien_waiver")
    if capability == "bonds_and_guarantees" and _age_days(payload.get("expiry")) not in (None,) and _age_days(payload.get("expiry")) > 0:
        findings.append("guarantee_expired_or_expiring")
    if capability == "insurance_compliance" and _age_days(payload.get("expiry")) not in (None,) and _age_days(payload.get("expiry")) > 0:
        findings.append("insurance_expired")
    if capability in {"delay_and_time_impact_boundary", "tax_and_withholding_boundary", "forecast_final_cost_boundary"}:
        if payload.get("dependency_contract") not in (None, *DECLARED_DEPENDENCY_MODES):
            findings.append("undeclared_dependency_contract")
    if capability == "agent_assisted_contract_review" and (not payload.get("citations") or payload.get("human_approval") is not True):
        findings.append("agent_review_requires_citations_and_approval")
    if capability == "governed_agent_crud_commands" and payload.get("confirmation") is not True:
        findings.append("agent_crud_requires_confirmation")
    if capability == "commercial_document_ingestion" and float(payload.get("confidence", 1) or 0) < 0.8:
        findings.append("low_confidence_document_extraction_requires_review")
    if capability == "role_based_permission_model" and payload.get("role") not in AUTHORIZED_ROLES:
        findings.append("unauthorized_commercial_role")
    if capability == "contractor_portal_contract" and payload.get("internal_notes_redaction") is False:
        findings.append("portal_must_redact_internal_assessment_notes")
    if capability == "package_overlap_guardrails" and any(str(payload.get(key, "")).endswith("_table") for key in REQUIRED_FIELDS[capability]):
        findings.append("overlap_guardrail_blocks_foreign_table_ownership")
    return tuple(findings)


def evaluate_commercial_control(capability: str, payload: Mapping[str, object] | None = None) -> dict:
    if capability not in COMMERCIAL_CONTROL_CAPABILITIES:
        return {"ok": False, "pbc": PBC_KEY, "reason": "unknown_commercial_control", "side_effects": ()}
    payload = dict(payload or {})
    base_ok, missing, invalid = _base_checks(capability, payload)
    findings = _domain_findings(capability, payload)
    table = CAPABILITY_TABLES[capability]
    requires_review = bool(findings or "agent" in capability or "claim" in capability or "dispute" in capability or payload.get("requires_review"))
    return {
        "ok": base_ok,
        "pbc": PBC_KEY,
        "capability": capability,
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
            "topic": f"pbc.{PBC_KEY}.events",
            "idempotency_key": _digest((capability, payload)),
        },
        "ui_surface": f"{PBC_KEY}.ui.improve1.{capability}",
        "service_api": f"{PBC_KEY}.services.{capability}",
        "route": f"/workbench/pbcs/{PBC_KEY}/improve1/{capability.replace('_', '-')}",
        "permission": f"{PBC_KEY}.{capability}.operate",
        "configuration": {
            "rule_id": f"{capability}_policy",
            "parameter_id": f"{capability}_threshold",
            "database_backends": ("postgresql", "mysql", "mariadb"),
        },
        "agent_skill": f"{PBC_KEY}_skills.{capability}",
        "requires_human_confirmation": requires_review,
        "retry_dead_letter_evidence": {
            "inbox_table": "construction_contracts_commercials_appgen_inbox_event",
            "dead_letter_table": "construction_contracts_commercials_appgen_dead_letter_event",
            "max_attempts": 5,
        },
        "release_evidence": {
            "code_artifact": "construction_contracts_commercials/commercial_control.py",
            "ui_artifact": "construction_contracts_commercials/ui.py",
            "service_artifact": "construction_contracts_commercials/core.py",
            "test_artifact": "construction_contracts_commercials/tests/test_domain_behavior.py",
            "traceability": "construction_contracts_commercials/IMPROVE1_TRACEABILITY.md",
        },
        "stream_engine_picker_visible": False,
        "shared_table_access": False,
        "side_effects": (),
    }


def sample_payload_for(capability: str) -> dict:
    if capability not in COMMERCIAL_CONTROL_CAPABILITIES:
        raise KeyError(capability)
    payload = {field: f"{field}_evidence" for field in REQUIRED_FIELDS[capability]}
    payload["referenced_tables"] = (CAPABILITY_TABLES[capability],)
    if capability == "contract_commercial_lifecycle":
        payload["target_stage"] = "execution"
    if capability == "contract_type_and_pricing_basis":
        payload["pricing_basis"] = "lump_sum"
    if capability == "scope_and_schedule_of_values":
        payload.update({"current_claimed": 10, "remaining_balance": 100})
    if capability == "pay_application_intake":
        payload.update({"certification_state": "certified", "payment_event_requested": False})
    if capability == "progress_measurement_evidence":
        payload["progress_evidence"] = "field_certificate"
    if capability == "retainage_rules":
        payload["waiver_requirement"] = "satisfied"
    if capability in {"advance_payment_and_recovery", "bonds_and_guarantees", "insurance_compliance"}:
        payload["guarantee_expiry" if capability == "advance_payment_and_recovery" else "expiry"] = "2026-12-31"
    if capability == "variation_order_lifecycle":
        payload.update({"approval_route": "approved", "executed_amount": 100})
    if capability == "change_notice_timeliness":
        payload.update({"event_date": "2026-05-25", "notice_date": "2026-05-27", "contractual_deadline": 7, "waiver_status": "not_required"})
    if capability == "lien_waiver_governance":
        payload["conditional_status"] = "valid"
    if capability in {"delay_and_time_impact_boundary", "tax_and_withholding_boundary", "forecast_final_cost_boundary"}:
        payload["dependency_contract"] = "projection"
    if capability == "agent_assisted_contract_review":
        payload.update({"citations": ("source-1",), "human_approval": True})
    if capability == "governed_agent_crud_commands":
        payload["confirmation"] = True
    if capability == "commercial_document_ingestion":
        payload["confidence"] = 0.95
    if capability == "role_based_permission_model":
        payload["role"] = "commercial_manager"
    if capability == "contractor_portal_contract":
        payload["internal_notes_redaction"] = True
    return payload


def _make_runner(capability: str) -> Callable[[Mapping[str, object] | None], dict]:
    def runner(payload: Mapping[str, object] | None = None) -> dict:
        return evaluate_commercial_control(capability, payload)

    runner.__name__ = f"run_{capability}"
    return runner


for _capability in COMMERCIAL_CONTROL_CAPABILITIES:
    globals()[f"run_{_capability}"] = _make_runner(_capability)

COMMERCIAL_CONTROL_FUNCTIONS: Mapping[str, Callable[[Mapping[str, object] | None], dict]] = {
    capability: globals()[f"run_{capability}"] for capability in COMMERCIAL_CONTROL_CAPABILITIES
}


def improve1_commercial_control_contract() -> dict:
    samples = tuple(COMMERCIAL_CONTROL_FUNCTIONS[capability](sample_payload_for(capability)) for capability in COMMERCIAL_CONTROL_CAPABILITIES)
    return {
        "format": "appgen.construction-contracts-commercials.improve1-commercial-control.v1",
        "ok": len(samples) == 50 and all(item["ok"] for item in samples),
        "pbc": PBC_KEY,
        "capability_count": len(COMMERCIAL_CONTROL_CAPABILITIES),
        "capabilities": COMMERCIAL_CONTROL_CAPABILITIES,
        "owned_tables": OWNED_TABLES,
        "event_contract": EVENT_CONTRACT,
        "database_backends": ("postgresql", "mysql", "mariadb"),
        "stream_engine_picker_visible": False,
        "shared_table_access": False,
        "samples": samples,
        "side_effects": (),
    }
