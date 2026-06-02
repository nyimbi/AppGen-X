"""Executable cross-border trade controls for improve1 execution.

Every function here is side-effect free and maps one improve1 trade capability to
owned trade tables, AppGen-X event metadata, UI/API surfaces, agent skills,
configuration handles, retry/dead-letter evidence, and traceability artifacts.
"""
from __future__ import annotations

import hashlib
import json
from typing import Callable, Mapping

from .improve1_capabilities import IMPROVE1_CAPABILITIES

PBC_KEY = "cross_border_trade"
EVENT_CONTRACT = "AppGen-X"
REQUIRED_EVENT_TOPIC = "appgen.cross_border_trade.events"
ALLOWED_DATABASE_BACKENDS = ("postgresql", "mysql", "mariadb")
OWNED_TABLES = (
    "hs_classification", "landed_cost_quote", "export_control_check", "customs_declaration", "denied_party_screening",
    "trade_document_packet", "broker_handoff", "carrier_handoff", "trade_compliance_hold", "country_restriction_policy",
    "trade_rule", "trade_parameter", "trade_configuration", "trade_schema_extension", "trade_audit_evidence",
    "cross_border_trade_appgen_outbox_event", "cross_border_trade_appgen_inbox_event", "cross_border_trade_dead_letter_event",
)
TRADE_CONTROL_CAPABILITIES = tuple(capability.slug for capability in IMPROVE1_CAPABILITIES)
SLUG_BY_NUMBER = {capability.feature_number: capability.slug for capability in IMPROVE1_CAPABILITIES}
CAPABILITY_BY_SLUG = {capability.slug: capability for capability in IMPROVE1_CAPABILITIES}
FIELD_SETS: tuple[tuple[str, ...], ...] = (
    ("item_identity", "description", "composition", "origin", "destination"),
    ("classification_id", "state", "reviewer", "legal_basis", "effective_window"),
    ("graph_id", "attributes", "materials", "rulings", "audit_hash"),
    ("variant_id", "destination", "local_code", "tariff_source", "effective_date"),
    ("quote_id", "goods_value", "freight", "insurance", "incoterm"),
    ("calc_id", "customs_value", "duty_rate", "tax_rate", "rounding_rule"),
    ("incoterm", "duty_payer", "risk_transfer", "document_obligations", "disclosure"),
    ("threshold_id", "country", "currency", "shipment_value", "excluded_goods"),
    ("screening_id", "party_roles", "list_sources", "match_strength", "reviewer"),
    ("match_id", "candidates", "similarity_factors", "reviewer_outcome", "override_reason"),
    ("check_id", "classification", "destination", "end_use", "end_user"),
    ("license_id", "jurisdiction", "item_class", "destination", "expiry"),
    ("policy_id", "country", "product_scope", "restriction_type", "source_reference"),
    ("hold_id", "state", "source", "severity", "release_conditions"),
    ("packet_id", "country", "incoterm", "required_documents", "completeness_score"),
    ("document_id", "document_type", "candidate_facts", "confidence", "review_state"),
    ("declaration_id", "state", "broker_status", "carrier_status", "idempotency_key"),
    ("release_gate_id", "hs_status", "screening_status", "document_status", "hold_status"),
    ("handoff_id", "broker_route", "payload_hash", "submission_state", "retry_policy"),
    ("handoff_id", "carrier_service", "route", "customs_reference", "acknowledgement"),
    ("provider_id", "acceptance_rate", "correction_rate", "clearance_time", "compliance_score"),
    ("routing_id", "route_emissions", "deadline", "cost", "override_evidence"),
    ("simulation_id", "origin", "destination", "incoterm", "total_landed_cost"),
    ("forecast_id", "country", "product", "fx_rate", "policy_change"),
    ("program_id", "origin_rules", "documentation", "certification", "expiry"),
    ("origin_id", "origin_source", "supplier_evidence", "transformation_rationale", "certificate"),
    ("valuation_id", "transaction_value", "assists", "royalties", "variance_threshold"),
    ("exception_id", "category", "severity", "owner", "closure_proof"),
    ("recommendation_id", "exception_type", "rationale", "approval_requirement", "next_action"),
    ("anomaly_id", "signal", "pattern", "risk", "review_state"),
    ("exposure_id", "shipment", "distribution", "party_risk", "mitigation"),
    ("model_id", "purpose", "feature_lineage", "validation_metrics", "approval_status"),
    ("proof_id", "proof_type", "verifier", "expiry", "selective_disclosure"),
    ("audit_id", "hash_chain", "decision_records", "event_deliveries", "replay_pointer"),
    ("screening_policy_id", "classification_policy", "document_policy", "release_policy", "compiled_hash"),
    ("inbox_id", "schema_version", "idempotency_key", "retry_evidence", "dead_letter_policy"),
    ("outbox_id", "ordering_group", "payload_hash", "retry_attempts", "delivery_proof"),
    ("boundary_id", "dependency", "dependency_mode", "freshness_rule", "retention_rule"),
    ("parameter_id", "bounds", "impact_simulation", "approver", "rollback_plan"),
    ("extension_id", "owned_table", "field_validation", "ui_preview", "api_review"),
    ("workbench_id", "panels", "events", "rules", "release_evidence"),
    ("review_id", "confidence", "candidate_codes", "evidence_snippets", "approval_action"),
    ("cockpit_id", "declaration_state", "broker_response", "carrier_readiness", "release_gates"),
    ("panel_id", "party_roles", "match_candidates", "source_lists", "decision"),
    ("assertion_id", "control_population", "failure_type", "owner", "release_gate"),
    ("drill_id", "failure_mode", "recovery_action", "dead_letter_recovery", "degraded_mode"),
    ("crypto_id", "crypto_epoch", "signing_profile", "key_rotation", "revocation"),
    ("plan_id", "command", "owned_tables", "expected_event", "human_confirmation"),
    ("score_id", "classification_ready", "event_health", "boundary_proof", "agent_safety"),
    ("proof_id", "event_intake", "classification_to_release", "ui_evidence", "boundary_verification"),
)
REQUIRED_FIELDS: dict[str, tuple[str, ...]] = dict(zip(TRADE_CONTROL_CAPABILITIES, FIELD_SETS))
CAPABILITY_TABLES = {
    **{SLUG_BY_NUMBER[i]: OWNED_TABLES[0] for i in (1, 2, 3, 4, 42)},
    **{SLUG_BY_NUMBER[i]: OWNED_TABLES[1] for i in (5, 6, 7, 8, 23, 24, 25, 27)},
    **{SLUG_BY_NUMBER[i]: OWNED_TABLES[4] for i in (9, 10, 44)},
    **{SLUG_BY_NUMBER[i]: OWNED_TABLES[2] for i in (11, 12, 30, 31)},
    **{SLUG_BY_NUMBER[i]: OWNED_TABLES[9] for i in (13, 35)},
    **{SLUG_BY_NUMBER[i]: OWNED_TABLES[8] for i in (14, 28, 29, 45)},
    **{SLUG_BY_NUMBER[i]: OWNED_TABLES[5] for i in (15, 16, 26)},
    **{SLUG_BY_NUMBER[i]: OWNED_TABLES[3] for i in (17, 18, 43, 50)},
    **{SLUG_BY_NUMBER[i]: OWNED_TABLES[6] for i in (19, 21, 22)},
    SLUG_BY_NUMBER[20]: OWNED_TABLES[7], SLUG_BY_NUMBER[32]: OWNED_TABLES[14], SLUG_BY_NUMBER[33]: OWNED_TABLES[14],
    SLUG_BY_NUMBER[34]: OWNED_TABLES[14], SLUG_BY_NUMBER[36]: OWNED_TABLES[16], SLUG_BY_NUMBER[37]: OWNED_TABLES[15],
    SLUG_BY_NUMBER[38]: OWNED_TABLES[14], SLUG_BY_NUMBER[39]: OWNED_TABLES[11], SLUG_BY_NUMBER[40]: OWNED_TABLES[13],
    SLUG_BY_NUMBER[41]: OWNED_TABLES[12], SLUG_BY_NUMBER[46]: OWNED_TABLES[17], SLUG_BY_NUMBER[47]: OWNED_TABLES[14],
    SLUG_BY_NUMBER[48]: OWNED_TABLES[14], SLUG_BY_NUMBER[49]: OWNED_TABLES[14],
}
CAPABILITY_EVENTS = {capability: "CrossBorderTrade" + "".join(part.capitalize() for part in capability.split("_")) for capability in TRADE_CONTROL_CAPABILITIES}
ALLOWED_CLASSIFICATION_STATES = {"draft", "reviewed", "approved", "superseded", "disputed", "expired", "blocked"}
DECLARED_DEPENDENCY_MODES = {"api", "event", "projection", "package_metadata"}
SUPPORTED_INCOTERMS = {"EXW", "FCA", "FOB", "CIF", "DAP", "DDP"}


def _digest(value: object) -> str:
    return hashlib.sha256(json.dumps(value, sort_keys=True, default=str).encode("utf-8")).hexdigest()


def _to_float(value: object, default: float = 0.0) -> float:
    try: return float(value)
    except (TypeError, ValueError): return default


def _invalid_references(references: object) -> tuple[str, ...]:
    if not references: return ()
    refs = (references,) if isinstance(references, str) else tuple(str(item) for item in references)
    return tuple(ref for ref in refs if ref.endswith("_table") and ref not in OWNED_TABLES and not ref.startswith(f"{PBC_KEY}_"))


def _base_checks(capability: str, payload: Mapping[str, object]) -> tuple[bool, tuple[str, ...], tuple[str, ...]]:
    missing = tuple(field for field in REQUIRED_FIELDS[capability] if payload.get(field) in (None, "", (), []))
    invalid = _invalid_references(payload.get("referenced_tables", ()))
    return not missing and not invalid, missing, invalid


def _domain_findings(capability: str, payload: Mapping[str, object]) -> tuple[str, ...]:
    findings: list[str] = []
    if capability == SLUG_BY_NUMBER[1] and _to_float(payload.get("confidence"), 1.0) < 0.7:
        findings.append("hs_classification_requires_review_threshold")
    if capability == SLUG_BY_NUMBER[2] and payload.get("state") not in ALLOWED_CLASSIFICATION_STATES:
        findings.append("classification_lifecycle_state_invalid")
    if capability == SLUG_BY_NUMBER[5] and payload.get("incoterm") not in SUPPORTED_INCOTERMS:
        findings.append("landed_cost_requires_supported_incoterm")
    if capability == SLUG_BY_NUMBER[9] and not payload.get("list_sources"):
        findings.append("denied_party_screening_requires_list_sources")
    if capability == SLUG_BY_NUMBER[11] and not payload.get("end_use"):
        findings.append("export_control_check_requires_end_use")
    if capability == SLUG_BY_NUMBER[14] and payload.get("state") == "released" and payload.get("release_conditions") != "satisfied":
        findings.append("compliance_hold_release_requires_satisfied_conditions")
    if capability == SLUG_BY_NUMBER[15] and _to_float(payload.get("completeness_score")) < 0.95:
        findings.append("document_packet_incomplete_for_customs")
    if capability == SLUG_BY_NUMBER[17] and payload.get("state") == "released" and payload.get("idempotency_key") in (None, ""):
        findings.append("declaration_release_requires_idempotency_key")
    if capability == SLUG_BY_NUMBER[18] and payload.get("hold_status") != "resolved":
        findings.append("declaration_release_gate_blocks_open_hold")
    if capability == SLUG_BY_NUMBER[36] and not payload.get("idempotency_key"):
        findings.append("inbox_reliability_requires_idempotency_key")
    if capability == SLUG_BY_NUMBER[38] and payload.get("dependency_mode") not in DECLARED_DEPENDENCY_MODES:
        findings.append("cross_pbc_boundary_must_use_api_event_or_projection")
    if capability == SLUG_BY_NUMBER[40] and str(payload.get("owned_table", "")).endswith("_table") and payload.get("owned_table") not in OWNED_TABLES:
        findings.append("schema_extension_must_target_owned_trade_table")
    if capability == SLUG_BY_NUMBER[45] and payload.get("failure_type") == "agent_preview_bypass":
        findings.append("continuous_control_blocks_agent_preview_bypass")
    if capability == SLUG_BY_NUMBER[48] and payload.get("human_confirmation") is not True:
        findings.append("agent_trade_plan_requires_human_confirmation")
    if capability == SLUG_BY_NUMBER[49] and payload.get("agent_safety") is not True:
        findings.append("readiness_score_requires_agent_safety")
    if capability == SLUG_BY_NUMBER[50] and payload.get("boundary_verification") is not True:
        findings.append("end_to_end_release_requires_boundary_verification")
    return tuple(findings)


def evaluate_trade_control(capability: str, payload: Mapping[str, object] | None = None) -> dict:
    if capability not in TRADE_CONTROL_CAPABILITIES:
        return {"ok": False, "pbc": PBC_KEY, "reason": "unknown_trade_control", "side_effects": ()}
    payload = dict(payload or {})
    base_ok, missing, invalid = _base_checks(capability, payload)
    findings = _domain_findings(capability, payload)
    table = CAPABILITY_TABLES[capability]
    meta = CAPABILITY_BY_SLUG[capability]
    return {"ok": base_ok, "pbc": PBC_KEY, "capability": capability, "feature_number": meta.feature_number, "title": meta.title, "status": "ready" if base_ok and not findings else "review_required", "target_table": table, "owned_tables": (table,), "read_tables": (), "invalid_references": invalid, "missing_required_fields": missing, "domain_findings": findings, "event": {"event_type": CAPABILITY_EVENTS[capability], "event_contract": EVENT_CONTRACT, "topic": REQUIRED_EVENT_TOPIC, "idempotency_key": _digest((capability, payload))}, "ui_surface": f"{PBC_KEY}.ui.improve1.{capability}", "service_api": f"{PBC_KEY}.services.{capability}", "route": f"/workbench/pbcs/{PBC_KEY}/improve1/{capability.replace('_', '-')}", "permission": f"{PBC_KEY}.{capability}.operate", "configuration": {"rule_id": f"{capability}_policy", "parameter_id": f"{capability}_parameter", "database_backends": ALLOWED_DATABASE_BACKENDS}, "agent_skill": f"{PBC_KEY}_skills.{capability}", "requires_human_confirmation": bool(findings or "agent" in capability or "release" in capability), "retry_dead_letter_evidence": {"inbox_table": "cross_border_trade_appgen_inbox_event", "dead_letter_table": "cross_border_trade_dead_letter_event", "max_attempts": 5}, "release_evidence": {"code_artifact": "cross_border_trade/trade_control.py", "ui_artifact": "cross_border_trade/ui.py", "service_artifact": "cross_border_trade/services.py", "test_artifact": "cross_border_trade/tests/test_domain_behavior.py", "traceability": "cross_border_trade/IMPROVE1_TRACEABILITY.md"}, "stream_engine_picker_visible": False, "shared_table_access": False, "side_effects": ()}


def sample_payload_for(capability: str) -> dict:
    if capability not in TRADE_CONTROL_CAPABILITIES: raise KeyError(capability)
    payload = {field: f"{field}_evidence" for field in REQUIRED_FIELDS[capability]}
    payload["referenced_tables"] = (CAPABILITY_TABLES[capability],)
    if capability == SLUG_BY_NUMBER[1]: payload["confidence"] = 0.9
    if capability == SLUG_BY_NUMBER[2]: payload["state"] = "approved"
    if capability == SLUG_BY_NUMBER[5]: payload.update({"incoterm": "DDP", "goods_value": 1000, "freight": 80, "insurance": 20})
    if capability == SLUG_BY_NUMBER[9]: payload["list_sources"] = ("OFAC", "UN", "EU")
    if capability == SLUG_BY_NUMBER[11]: payload["end_use"] = "commercial resale"
    if capability == SLUG_BY_NUMBER[14]: payload.update({"state": "reviewed", "release_conditions": "satisfied"})
    if capability == SLUG_BY_NUMBER[15]: payload["completeness_score"] = 1.0
    if capability == SLUG_BY_NUMBER[17]: payload.update({"state": "filed", "idempotency_key": "decl-1"})
    if capability == SLUG_BY_NUMBER[18]: payload.update({"hold_status": "resolved", "document_status": "complete"})
    if capability == SLUG_BY_NUMBER[36]: payload["idempotency_key"] = "order-evt-1"
    if capability == SLUG_BY_NUMBER[38]: payload["dependency_mode"] = "event"
    if capability == SLUG_BY_NUMBER[40]: payload["owned_table"] = "customs_declaration"
    if capability == SLUG_BY_NUMBER[45]: payload["failure_type"] = "none"
    if capability == SLUG_BY_NUMBER[48]: payload["human_confirmation"] = True
    if capability == SLUG_BY_NUMBER[49]: payload["agent_safety"] = True
    if capability == SLUG_BY_NUMBER[50]: payload["boundary_verification"] = True
    return payload


def _make_runner(capability: str) -> Callable[[Mapping[str, object] | None], dict]:
    def runner(payload: Mapping[str, object] | None = None) -> dict:
        return evaluate_trade_control(capability, payload)
    runner.__name__ = f"run_{capability}"
    return runner

for _capability in TRADE_CONTROL_CAPABILITIES:
    globals()[f"run_{_capability}"] = _make_runner(_capability)

TRADE_CONTROL_FUNCTIONS: Mapping[str, Callable[[Mapping[str, object] | None], dict]] = {capability: globals()[f"run_{capability}"] for capability in TRADE_CONTROL_CAPABILITIES}


def improve1_trade_control_contract() -> dict:
    samples = tuple(TRADE_CONTROL_FUNCTIONS[capability](sample_payload_for(capability)) for capability in TRADE_CONTROL_CAPABILITIES)
    return {"format": "appgen.cross-border-trade.improve1-trade-control.v1", "ok": len(samples) == 50 and all(item["ok"] for item in samples), "pbc": PBC_KEY, "capability_count": len(TRADE_CONTROL_CAPABILITIES), "capabilities": TRADE_CONTROL_CAPABILITIES, "owned_tables": OWNED_TABLES, "event_contract": EVENT_CONTRACT, "database_backends": ALLOWED_DATABASE_BACKENDS, "stream_engine_picker_visible": False, "shared_table_access": False, "samples": samples, "side_effects": ()}
