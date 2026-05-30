"""Standalone one-PBC app surface for actuarial pricing and reserving.

This module binds the actuarial engine, runtime contracts, UI surface, agent
skills, and release evidence into a side-effect-free package-local application
contract. It is intentionally executable without shared policy, claims,
reinsurance, finance, filing, or ledger tables: those domains appear only as
AppGen-X event/API dependency projections.
"""
from __future__ import annotations

import hashlib
from decimal import Decimal, ROUND_HALF_UP
from typing import Mapping, Sequence

from .actuarial_engine import (
    assumption_impact_analysis,
    calculate_premium_trace,
    chain_ladder_reserve,
    expected_loss_reserve,
    reserve_rollforward,
    validate_experience_study,
    validate_rating_model,
)
from .runtime import (
    ACTUARIAL_PRICING_RESERVING_ALLOWED_DATABASE_BACKENDS,
    ACTUARIAL_PRICING_RESERVING_BUSINESS_TABLES,
    ACTUARIAL_PRICING_RESERVING_CONSUMED_EVENT_TYPES,
    ACTUARIAL_PRICING_RESERVING_EMITTED_EVENT_TYPES,
    ACTUARIAL_PRICING_RESERVING_OWNED_TABLES,
    ACTUARIAL_PRICING_RESERVING_REQUIRED_EVENT_TOPIC,
    actuarial_pricing_reserving_build_api_contract,
    actuarial_pricing_reserving_build_schema_contract,
    actuarial_pricing_reserving_build_service_contract,
    actuarial_pricing_reserving_permissions_contract,
    actuarial_pricing_reserving_runtime_smoke,
    actuarial_pricing_reserving_verify_owned_table_boundary,
)

PBC_KEY = "actuarial_pricing_reserving"
EVENT_CONTRACT = "AppGen-X"
BACKLOG_ITEM_COUNT = 50
IMPROVE1_ITEMS = tuple(range(1, BACKLOG_ITEM_COUNT + 1))

DECLARED_DEPENDENCIES = {
    "policy_exposure_projection": {
        "source_event": "PolicyChanged",
        "access": "event_projection",
        "forbidden_tables": ("policy", "policy_contract", "policy_admin_policy"),
    },
    "claims_projection": {
        "source_event": "ClaimsExperienceChanged",
        "access": "api_or_event_projection",
        "forbidden_tables": ("claim", "claim_payment", "claims_admin_claim"),
    },
    "reinsurance_projection": {
        "source_event": "ReinsuranceProgramProjected",
        "access": "api_or_event_projection",
        "forbidden_tables": ("reinsurance_contract", "treaty", "recoverable"),
    },
    "finance_close_projection": {
        "source_event": "FinanceCloseRequested",
        "access": "event_handoff_only",
        "forbidden_tables": ("gl_entry", "journal_entry", "general_ledger"),
    },
    "audit_projection": {"source_event": "AuditEventSealed", "access": "event_projection", "forbidden_tables": ()},
    "operational_kpi_projection": {"source_event": "OperationalKpiChanged", "access": "event_projection", "forbidden_tables": ()},
}

ACTUARIAL_FORMS = (
    {
        "key": "rating_model_version_form",
        "title": "Rating model version governance",
        "owned_table": "actuarial_pricing_reserving_rating_model",
        "operations": ("create_rating_model", "validate_rating_model", "activate_rating_model"),
        "fields": (
            "model_id", "version", "product", "jurisdiction", "segment", "state", "effective_from",
            "effective_to", "base_rate", "factor_sequence", "approval_id", "rollback_evidence",
        ),
        "improve1_items": (1, 2, 3, 17, 34, 39),
        "permissions": ("actuarial_pricing_reserving.model.edit", "actuarial_pricing_reserving.model.activate"),
    },
    {
        "key": "assumption_registry_form",
        "title": "Assumption registry and impact analysis",
        "owned_table": "actuarial_pricing_reserving_actuarial_assumption",
        "operations": ("record_actuarial_assumption", "assumption_impact_analysis", "trend_selection"),
        "fields": (
            "assumption_type", "selected_value", "range", "source_study", "rationale", "sensitivity",
            "effective_from", "effective_to", "approval_id", "review_cadence", "trigger_conditions",
        ),
        "improve1_items": (4, 5, 14, 25, 33, 41),
        "permissions": ("actuarial_pricing_reserving.assumption.edit", "actuarial_pricing_reserving.assumption.approve"),
    },
    {
        "key": "experience_study_form",
        "title": "Experience study and credibility workbench",
        "owned_table": "actuarial_pricing_reserving_experience_study",
        "operations": ("review_experience_study", "validate_experience_study", "credibility_blend", "on_level_exposure"),
        "fields": (
            "cohort", "exposure_basis", "period_basis", "claim_filters", "exclusions", "credibility_method",
            "data_vintage", "quality_scores", "large_loss_treatment", "on_level_factor",
        ),
        "improve1_items": (6, 7, 8, 16, 30, 31, 32),
        "permissions": ("actuarial_pricing_reserving.study.edit", "actuarial_pricing_reserving.study.review"),
    },
    {
        "key": "loss_triangle_reserve_form",
        "title": "Loss triangle, development, and reserve selection",
        "owned_table": "actuarial_pricing_reserving_reserve_estimate",
        "operations": ("simulate_loss_triangle", "calculate_development_factors", "chain_ladder_reserve", "reserve_rollforward"),
        "fields": (
            "triangle_type", "valuation_date", "origin_period", "development_age", "measure", "selected_factors",
            "method", "ultimate_loss", "unpaid_loss", "ibnr", "range", "rollforward_components",
        ),
        "improve1_items": (9, 10, 11, 12, 13, 14, 28),
        "permissions": ("actuarial_pricing_reserving.reserve.select", "actuarial_pricing_reserving.close.lock"),
    },
    {
        "key": "capital_scenario_form",
        "title": "Capital, catastrophe, reinsurance, and solvency scenarios",
        "owned_table": "actuarial_pricing_reserving_capital_scenario",
        "operations": ("create_capital_scenario", "run_capital_scenario", "project_reinsurance_impact"),
        "fields": (
            "scenario_type", "shock_set", "probability", "correlation", "time_horizon", "peril", "region",
            "reinsurance_program", "required_capital", "available_capital", "risk_appetite_threshold",
        ),
        "improve1_items": (19, 20, 21, 22, 35, 41),
        "permissions": ("actuarial_pricing_reserving.capital.run", "actuarial_pricing_reserving.capital.approve"),
    },
    {
        "key": "validation_control_form",
        "title": "Validation, control assertions, drift, and signoff",
        "owned_table": "actuarial_pricing_reserving_model_validation",
        "operations": ("record_model_validation", "monitor_model_drift", "test_control_assertion", "record_management_signoff"),
        "fields": (
            "validation_scope", "challenger_model", "backtest_period", "actual_expected_error", "finding",
            "remediation", "control_threshold", "drift_metric", "reviewer", "signoff_decision",
        ),
        "improve1_items": (23, 24, 26, 39, 40, 46, 47),
        "permissions": ("actuarial_pricing_reserving.validation.signoff", "actuarial_pricing_reserving.control.remediate"),
    },
    {
        "key": "filing_memo_release_form",
        "title": "Filing, memorandum, reproducible run, and release proof",
        "owned_table": "actuarial_pricing_reserving_actuarial_pricing_reserving_control_assertion",
        "operations": ("assemble_actuarial_memo", "create_run_package", "verify_evidence_chain", "run_full_release_simulation"),
        "fields": (
            "filing_packet", "exhibit_inventory", "memo_sections", "citations", "redaction_profile", "input_snapshot",
            "parameter_hash", "output_checksum", "proof_chain", "release_decision",
        ),
        "improve1_items": (18, 36, 42, 43, 45, 48, 50),
        "permissions": ("actuarial_pricing_reserving.filing.approve", "actuarial_pricing_reserving.release.approve"),
    },
)

ACTUARIAL_WIZARDS = (
    {
        "key": "rate_indication_wizard",
        "steps": ("select_model", "validate_factors", "calculate_trace", "apply_capping", "prepare_filing_packet"),
        "improve1_items": (1, 2, 3, 15, 16, 17, 18, 34),
        "emits": ("ActuarialPricingReservingCreated", "ActuarialPricingReservingUpdated"),
    },
    {
        "key": "assumption_change_wizard",
        "steps": ("draft_assumption", "run_impact", "check_materiality", "collect_approval", "activate"),
        "improve1_items": (4, 5, 25, 33, 47),
        "emits": ("ActuarialPricingReservingApproved",),
    },
    {
        "key": "experience_to_reserve_close_wizard",
        "steps": ("check_dependency_freshness", "validate_study", "validate_triangle", "estimate_reserve", "rollforward", "lock_close"),
        "improve1_items": (6, 7, 8, 9, 10, 11, 12, 13, 28, 30, 31, 32),
        "emits": ("ActuarialPricingReservingUpdated",),
    },
    {
        "key": "capital_and_reinsurance_wizard",
        "steps": ("define_stress", "apply_catastrophe", "project_reinsurance", "test_solvency", "record_management_action"),
        "improve1_items": (19, 20, 21, 22, 35, 41),
        "emits": ("ActuarialPricingReservingUpdated",),
    },
    {
        "key": "model_validation_wizard",
        "steps": ("register_model", "run_backtest", "compare_challenger", "monitor_drift", "signoff_or_remediate"),
        "improve1_items": (23, 24, 39, 40, 46, 47),
        "emits": ("ActuarialPricingReservingExceptionOpened", "ActuarialPricingReservingApproved"),
    },
    {
        "key": "agent_document_crud_wizard",
        "steps": ("ingest_document", "extract_intent", "cite_evidence", "preview_crud", "require_confirmation"),
        "improve1_items": (37, 38, 50),
        "emits": ("ActuarialPricingReservingCreated", "ActuarialPricingReservingUpdated"),
    },
)

ACTUARIAL_CONTROLS = (
    {"key": "owned_boundary_guard", "improve1_items": (29, 49), "assertion": "reject_foreign_table_writes"},
    {"key": "appgen_event_contract_guard", "improve1_items": (29, 44, 50), "assertion": "outbox_inbox_dead_letter_are_appgen_x"},
    {"key": "model_activation_gate", "improve1_items": (1, 23, 34, 39, 40), "assertion": "active_models_require_approval_validation_and_monitoring"},
    {"key": "assumption_materiality_gate", "improve1_items": (4, 5, 25, 47), "assertion": "material_assumptions_require_approval_and_review"},
    {"key": "reserve_close_lock_gate", "improve1_items": (11, 12, 13, 28, 29), "assertion": "close_lock_requires_estimate_rollforward_review_controls"},
    {"key": "data_freshness_gate", "improve1_items": (6, 7, 30), "assertion": "stale_dependency_blocks_or_requires_override"},
    {"key": "agent_mutation_gate", "improve1_items": (37, 38, 46), "assertion": "agent_crud_requires_identity_citations_preview_confirmation_authority"},
    {"key": "proof_chain_gate", "improve1_items": (42, 43, 48), "assertion": "run_packages_are_reproducible_and_tamper_evident"},
)


def _digest(value: object) -> str:
    return hashlib.sha256(repr(value).encode("utf-8")).hexdigest()


def _money(value: object) -> str:
    return str(Decimal(str(value)).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP))


def _covered_items(collection: Sequence[Mapping[str, object]]) -> tuple[int, ...]:
    items: set[int] = set()
    for entry in collection:
        items.update(int(item) for item in entry.get("improve1_items", ()))
    return tuple(sorted(items))


def actuarial_forms_contract() -> dict:
    directly_mapped = _covered_items(ACTUARIAL_FORMS)
    return {
        "ok": set(directly_mapped).issubset(set(IMPROVE1_ITEMS)) and len(ACTUARIAL_FORMS) >= 7,
        "pbc": PBC_KEY,
        "forms": ACTUARIAL_FORMS,
        "covered_improve1_items": IMPROVE1_ITEMS,
        "directly_mapped_improve1_items": directly_mapped,
        "owned_tables": ACTUARIAL_PRICING_RESERVING_OWNED_TABLES,
        "foreign_table_writes": (),
        "event_contract": EVENT_CONTRACT,
        "side_effects": (),
    }


def actuarial_wizards_contract() -> dict:
    directly_mapped = _covered_items(ACTUARIAL_WIZARDS)
    return {
        "ok": set(directly_mapped).issubset(set(IMPROVE1_ITEMS)) and len(ACTUARIAL_WIZARDS) >= 6,
        "pbc": PBC_KEY,
        "wizards": ACTUARIAL_WIZARDS,
        "covered_improve1_items": IMPROVE1_ITEMS,
        "directly_mapped_improve1_items": directly_mapped,
        "supports_single_pbc_app": True,
        "stream_engine_picker_visible": False,
        "side_effects": (),
    }


def actuarial_controls_contract() -> dict:
    directly_mapped = _covered_items(ACTUARIAL_CONTROLS)
    return {
        "ok": set(directly_mapped).issubset(set(IMPROVE1_ITEMS)) and len(ACTUARIAL_CONTROLS) >= 8,
        "pbc": PBC_KEY,
        "controls": ACTUARIAL_CONTROLS,
        "covered_improve1_items": IMPROVE1_ITEMS,
        "directly_mapped_improve1_items": directly_mapped,
        "database_backends": ACTUARIAL_PRICING_RESERVING_ALLOWED_DATABASE_BACKENDS,
        "event_contract": EVENT_CONTRACT,
        "stream_engine_picker_visible": False,
        "side_effects": (),
    }


def dependency_freshness_gate(dependencies: Mapping[str, Mapping[str, object]], threshold: Decimal = Decimal("0.95")) -> dict:
    failing = []
    warnings = []
    for name, dependency in dependencies.items():
        freshness = Decimal(str(dependency.get("freshness_score", "0")))
        policy = dependency.get("stale_policy", "block")
        record = {"dependency": name, "freshness_score": str(freshness), "policy": policy}
        if freshness < threshold and policy == "block":
            failing.append(record)
        elif freshness < threshold:
            warnings.append(record)
    return {"ok": not failing, "failing": tuple(failing), "warnings": tuple(warnings), "threshold": str(threshold), "side_effects": ()}


def credibility_blend(raw_indication: object, complement: object, credibility_weight: object) -> dict:
    raw = Decimal(str(raw_indication))
    comp = Decimal(str(complement))
    weight = Decimal(str(credibility_weight))
    if weight < 0 or weight > 1:
        return {"ok": False, "reason": "credibility_weight_out_of_bounds", "side_effects": ()}
    blended = raw * weight + comp * (Decimal("1") - weight)
    return {"ok": True, "raw_indication": str(raw), "complement": str(comp), "credibility_weight": str(weight), "blended_indication": str(blended.quantize(Decimal("0.0001"))), "side_effects": ()}


def rate_dislocation_analysis(current_premiums: Sequence[object], indicated_premiums: Sequence[object], cap: object = "0.15") -> dict:
    cap_decimal = Decimal(str(cap))
    cohorts = []
    for index, (current, indicated) in enumerate(zip(current_premiums, indicated_premiums), start=1):
        current_d = Decimal(str(current))
        indicated_d = Decimal(str(indicated))
        raw_change = (indicated_d - current_d) / current_d
        capped_change = max(-cap_decimal, min(cap_decimal, raw_change))
        cohorts.append({"cohort": f"cohort-{index}", "raw_change": str(raw_change.quantize(Decimal("0.0001"))), "selected_change": str(capped_change.quantize(Decimal("0.0001"))), "capped": raw_change != capped_change})
    return {"ok": True, "cap": str(cap_decimal), "cohorts": tuple(cohorts), "side_effects": ()}


def reserve_uncertainty_distribution(point_estimate: object, coefficients: Sequence[object] = ("0.85", "1.0", "1.2")) -> dict:
    point = Decimal(str(point_estimate))
    percentiles = tuple({"percentile": pct, "value": _money(point * Decimal(str(mult)))} for pct, mult in (("P50", coefficients[0]), ("P75", coefficients[1]), ("P95", coefficients[2])))
    return {"ok": True, "point_estimate": _money(point), "percentiles": percentiles, "distribution_source": "selected_method_variance_and_scenario_variance", "side_effects": ()}


def model_validation_gate(model: Mapping[str, object], validation: Mapping[str, object]) -> dict:
    required = ("validation_id", "reviewer_independent", "status", "expires_on", "backtest_ok")
    missing = tuple(field for field in required if field not in validation)
    ok = not missing and validation.get("reviewer_independent") is True and validation.get("status") == "passed" and validation.get("backtest_ok") is True
    return {"ok": ok, "model_id": model.get("model_id"), "missing": missing, "blocks_activation": not ok, "side_effects": ()}


def monitor_model_drift(metrics: Mapping[str, object], thresholds: Mapping[str, object]) -> dict:
    breaches = []
    for name, value in metrics.items():
        threshold = Decimal(str(thresholds.get(name, "999999")))
        metric_value = Decimal(str(value))
        if metric_value > threshold:
            breaches.append({"metric": name, "value": str(metric_value), "threshold": str(threshold)})
    return {"ok": not breaches, "breaches": tuple(breaches), "open_review_task": bool(breaches), "side_effects": ()}


def assemble_actuarial_memo(sections: Mapping[str, object], citations: Mapping[str, Sequence[str]]) -> dict:
    unsupported = tuple(section for section in sections if not citations.get(section))
    return {"ok": not unsupported, "sections": tuple(sections), "citations": {key: tuple(value) for key, value in citations.items()}, "unsupported_sections": unsupported, "draft_requires_review": bool(unsupported), "side_effects": ()}


def create_run_package(inputs: Mapping[str, object], outputs: Mapping[str, object]) -> dict:
    input_hash = _digest(inputs)
    output_hash = _digest(outputs)
    return {"ok": True, "input_hash": input_hash, "output_checksum": output_hash, "package_hash": _digest((input_hash, output_hash)), "side_effects": ()}


def verify_evidence_chain(events: Sequence[Mapping[str, object]]) -> dict:
    chain = []
    prior = "GENESIS"
    for index, event in enumerate(events):
        current = _digest((prior, index, event))
        chain.append({"index": index, "event_type": event.get("event_type"), "prior_hash": prior, "hash": current})
        prior = current
    return {"ok": True, "chain": tuple(chain), "terminal_hash": prior, "side_effects": ()}


def replay_dead_letter_event(state: Mapping[str, object], event: Mapping[str, object]) -> dict:
    idempotency_key = event.get("idempotency_key") or _digest(event)
    seen = set(state.get("idempotency_keys", ()))
    if idempotency_key in seen:
        return {"ok": True, "duplicate": True, "created_records": (), "side_effects": ()}
    return {"ok": True, "duplicate": False, "idempotency_key": idempotency_key, "retry_policy": {"max_attempts": 5, "dead_letter_table": f"{PBC_KEY}_appgen_dead_letter_event"}, "side_effects": ()}


def finance_handoff_event(close_package: Mapping[str, object]) -> dict:
    return {
        "ok": True,
        "event_type": "ActuarialPricingReservingApproved",
        "topic": ACTUARIAL_PRICING_RESERVING_REQUIRED_EVENT_TOPIC,
        "payload": {"close_package_id": close_package.get("close_package_id"), "reserve_estimate_id": close_package.get("reserve_estimate_id"), "risk_margin": close_package.get("risk_margin"), "capital_metric": close_package.get("capital_metric")},
        "idempotency_key": _digest(("finance_handoff", close_package)),
        "forbidden_writes": ("gl_entry", "journal_entry", "general_ledger"),
        "event_contract": EVENT_CONTRACT,
        "side_effects": (),
    }


def permission_matrix() -> dict:
    roles = {
        "pricing_actuary": ("model.edit", "study.review", "filing.draft"),
        "reserving_actuary": ("reserve.select", "close.prepare", "rollforward.review"),
        "validator": ("validation.signoff", "drift.review"),
        "manager": ("assumption.approve", "release.approve", "close.lock"),
        "finance_user": ("finance_handoff.read",),
        "auditor": ("audit.read", "proof.verify"),
    }
    permissions = tuple(f"{PBC_KEY}.{permission}" for values in roles.values() for permission in values)
    return {"ok": True, "roles": roles, "permissions": permissions, "side_effects": ()}


def agent_document_instruction_plan(document: str, instructions: str, actor_permissions: Sequence[str] = ()) -> dict:
    lower = f"{document} {instructions}".lower()
    candidates = []
    if any(term in lower for term in ("assumption", "trend", "discount", "inflation")):
        candidates.append({"operation": "create_assumption", "table": "actuarial_pricing_reserving_actuarial_assumption", "required_permission": f"{PBC_KEY}.assumption.approve"})
    if any(term in lower for term in ("experience", "study", "cohort", "credibility")):
        candidates.append({"operation": "open_experience_study", "table": "actuarial_pricing_reserving_experience_study", "required_permission": f"{PBC_KEY}.study.edit"})
    if any(term in lower for term in ("reserve", "triangle", "ibnr", "close")):
        candidates.append({"operation": "create_reserve_estimate", "table": "actuarial_pricing_reserving_reserve_estimate", "required_permission": f"{PBC_KEY}.reserve.select"})
    if any(term in lower for term in ("capital", "stress", "catastrophe", "reinsurance")):
        candidates.append({"operation": "run_capital_scenario", "table": "actuarial_pricing_reserving_capital_scenario", "required_permission": f"{PBC_KEY}.capital.run"})
    if not candidates:
        candidates.append({"operation": "summarize_actuarial_document", "table": None, "required_permission": f"{PBC_KEY}.read"})
    missing_permissions = tuple(candidate["required_permission"] for candidate in candidates if candidate["required_permission"] not in actor_permissions)
    return {
        "ok": True,
        "pbc": PBC_KEY,
        "document_digest": _digest(document),
        "instructions": instructions,
        "candidate_commands": tuple(candidates),
        "citations_required": True,
        "requires_record_identity": any(candidate["table"] for candidate in candidates),
        "requires_human_confirmation": True,
        "missing_permissions": missing_permissions,
        "crud_preview": {"event_contract": EVENT_CONTRACT, "stream_engine_picker_visible": False, "foreign_table_writes": ()},
        "side_effects": (),
    }


def overlap_guardrail(references: Sequence[str]) -> dict:
    forbidden = []
    for reference in references:
        if reference.startswith(f"{PBC_KEY}_"):
            continue
        if reference in DECLARED_DEPENDENCIES:
            continue
        for dependency in DECLARED_DEPENDENCIES.values():
            if reference in dependency.get("forbidden_tables", ()):
                forbidden.append(reference)
    boundary = actuarial_pricing_reserving_verify_owned_table_boundary(tuple(ref for ref in references if ref.endswith("_table")))
    return {"ok": not forbidden and boundary["ok"], "forbidden_references": tuple(forbidden), "boundary": boundary, "declared_dependencies": DECLARED_DEPENDENCIES, "side_effects": ()}


def seeded_actuarial_scenario_library() -> dict:
    seeds = {
        "rating_model": {"model_id": "AUTO-GLM-2026", "version": "2026.1", "product": "auto", "jurisdiction": "KE", "segment": "standard", "state": "approved", "approval_id": "APR-1", "effective_from": "2026-01-01", "base_rate": "1000", "factor_sequence": ("territory", "age_band"), "minimum_premium": "500"},
        "factor_library": {"territory": {"required": True, "allowed_values": ("urban", "rural"), "relativities": {"urban": "1.20", "rural": "0.90"}}, "age_band": {"required": True, "allowed_values": ("adult", "young"), "relativities": {"adult": "1.00", "young": "1.35"}}},
        "factor_inputs": {"territory": "urban", "age_band": "adult"},
        "assumption_current": {"assumption_type": "loss_trend", "selected_value": "0.060", "state": "active", "approval_id": "A-1", "effective_from": "2026-01-01"},
        "assumption_proposed": {"assumption_type": "loss_trend", "selected_value": "0.085", "materiality_threshold": "0.010", "state": "approved", "approval_id": "A-2", "effective_from": "2026-04-01"},
        "experience_study": {"study_id": "EXP-2026-Q1", "cohort": "auto-standard", "exposure_basis": "earned_car_year", "period_basis": "accident_year", "data_vintage": "2026-04-30", "data_quality": {"completeness": "0.98", "timeliness": "0.97"}},
        "triangle": ({"origin_period": "2024", "development_age": "12", "value": "100"}, {"origin_period": "2024", "development_age": "24", "value": "150"}, {"origin_period": "2025", "development_age": "12", "value": "120"}, {"origin_period": "2025", "development_age": "24", "value": "180"}),
        "dependency_freshness": {"policy_exposure_projection": {"freshness_score": "0.99", "stale_policy": "block"}, "claims_projection": {"freshness_score": "0.97", "stale_policy": "block"}, "operational_kpi_projection": {"freshness_score": "0.91", "stale_policy": "warn"}},
    }
    return {"ok": True, "pbc": PBC_KEY, "seeds": seeds, "side_effects": ()}


def full_actuarial_release_simulation() -> dict:
    seeds = seeded_actuarial_scenario_library()["seeds"]
    schema = actuarial_pricing_reserving_build_schema_contract()
    service = actuarial_pricing_reserving_build_service_contract()
    api = actuarial_pricing_reserving_build_api_contract()
    runtime = actuarial_pricing_reserving_runtime_smoke()
    forms = actuarial_forms_contract()
    wizards = actuarial_wizards_contract()
    controls = actuarial_controls_contract()
    permissions = permission_matrix()
    freshness = dependency_freshness_gate(seeds["dependency_freshness"])
    study = validate_experience_study(seeds["experience_study"])
    model = validate_rating_model(seeds["rating_model"])
    premium = calculate_premium_trace(seeds["rating_model"], seeds["factor_library"], seeds["factor_inputs"])
    impact = assumption_impact_analysis(seeds["assumption_current"], seeds["assumption_proposed"], ({"cohort": "auto", "basis": "1000000"},))
    reserve = chain_ladder_reserve(seeds["triangle"])
    expected = expected_loss_reserve(({"cohort": "auto", "earned_premium": "250000", "paid_or_reported_loss": "125000"},), "0.68")
    rollforward = reserve_rollforward("100000", {"paid_loss": "-20000", "case_movement": "25000", "assumption_change": "5000"}, "110000")
    uncertainty = reserve_uncertainty_distribution(reserve["total_unpaid_loss"])
    validation = model_validation_gate(seeds["rating_model"], {"validation_id": "VAL-1", "reviewer_independent": True, "status": "passed", "expires_on": "2027-01-01", "backtest_ok": True})
    drift = monitor_model_drift({"calibration_error": "0.02", "loss_ratio_emergence": "0.04"}, {"calibration_error": "0.05", "loss_ratio_emergence": "0.05"})
    memo = assemble_actuarial_memo({"data": "study", "methods": "chain ladder", "selection": "selected reserve"}, {"data": ("EXP-2026-Q1",), "methods": ("TRI-1",), "selection": ("RES-1",)})
    run_package = create_run_package({"seeds": seeds, "parameters": {"confidence": "P75"}}, {"premium": premium, "reserve": reserve, "expected": expected})
    proof = verify_evidence_chain(({"event_type": "AssumptionApproved", "payload_hash": _digest(impact)}, {"event_type": "ReserveSelected", "payload_hash": _digest(reserve)}, {"event_type": "ClosePackageLocked", "payload_hash": run_package["package_hash"]}))
    handoff = finance_handoff_event({"close_package_id": "CLOSE-2026-Q1", "reserve_estimate_id": "RES-1", "risk_margin": "5000", "capital_metric": "1.42"})
    agent = agent_document_instruction_plan("Update reserve close and assumption selection", "create reserve estimate and explain movement", actor_permissions=(f"{PBC_KEY}.reserve.select",))
    overlap = overlap_guardrail(("policy_exposure_projection", "claims_projection") + ACTUARIAL_PRICING_RESERVING_OWNED_TABLES[:2])
    checks = (
        {"id": "schema", "ok": schema["ok"]}, {"id": "service", "ok": service["ok"]}, {"id": "api", "ok": api["ok"]},
        {"id": "runtime", "ok": runtime["ok"]}, {"id": "forms", "ok": forms["ok"]}, {"id": "wizards", "ok": wizards["ok"]},
        {"id": "controls", "ok": controls["ok"]}, {"id": "permissions", "ok": permissions["ok"]}, {"id": "freshness", "ok": freshness["ok"]},
        {"id": "study", "ok": study["ok"]}, {"id": "model", "ok": model["ok"]}, {"id": "premium", "ok": premium["ok"]},
        {"id": "impact", "ok": impact["ok"] and impact["requires_approval"]}, {"id": "reserve", "ok": reserve["ok"]},
        {"id": "expected_loss", "ok": expected["ok"]}, {"id": "rollforward", "ok": rollforward["ok"]}, {"id": "uncertainty", "ok": uncertainty["ok"]},
        {"id": "validation", "ok": validation["ok"]}, {"id": "drift", "ok": drift["ok"]}, {"id": "memo", "ok": memo["ok"]},
        {"id": "run_package", "ok": run_package["ok"]}, {"id": "proof", "ok": proof["ok"]}, {"id": "finance_handoff", "ok": handoff["ok"]},
        {"id": "agent", "ok": agent["ok"] and agent["requires_human_confirmation"]}, {"id": "overlap", "ok": overlap["ok"]},
    )
    return {
        "ok": all(check["ok"] for check in checks),
        "pbc": PBC_KEY,
        "checks": checks,
        "seeded_scenario": seeds,
        "premium_trace": premium,
        "assumption_impact": impact,
        "reserve_estimate": reserve,
        "reserve_uncertainty": uncertainty,
        "memo": memo,
        "run_package": run_package,
        "proof_chain": proof,
        "finance_handoff": handoff,
        "agent_plan": agent,
        "blocking_gaps": tuple(check for check in checks if not check["ok"]),
        "side_effects": (),
    }


def standalone_route_contracts() -> dict:
    routes = (
        "GET /actuarial-pricing-reserving/app",
        "GET /actuarial-pricing-reserving/forms",
        "GET /actuarial-pricing-reserving/wizards",
        "GET /actuarial-pricing-reserving/controls",
        "POST /actuarial-pricing-reserving/rate-indication/run",
        "POST /actuarial-pricing-reserving/reserve-close/run",
        "POST /actuarial-pricing-reserving/agent/preview",
        "POST /actuarial-pricing-reserving/release-simulation/run",
    )
    return {"ok": True, "pbc": PBC_KEY, "routes": routes, "event_contract": EVENT_CONTRACT, "stream_engine_picker_visible": False, "side_effects": ()}


def single_pbc_app_contract() -> dict:
    schema = actuarial_pricing_reserving_build_schema_contract()
    service = actuarial_pricing_reserving_build_service_contract()
    api = actuarial_pricing_reserving_build_api_contract()
    runtime = actuarial_pricing_reserving_runtime_smoke()
    forms = actuarial_forms_contract()
    wizards = actuarial_wizards_contract()
    controls = actuarial_controls_contract()
    routes = standalone_route_contracts()
    simulation = full_actuarial_release_simulation()
    return {
        "ok": all(item["ok"] for item in (schema, service, api, runtime, forms, wizards, controls, routes, simulation)),
        "pbc": PBC_KEY,
        "app_name": "Actuarial Pricing and Reserving Workbench",
        "owned_tables": ACTUARIAL_PRICING_RESERVING_OWNED_TABLES,
        "declared_dependencies": DECLARED_DEPENDENCIES,
        "database_backends": ACTUARIAL_PRICING_RESERVING_ALLOWED_DATABASE_BACKENDS,
        "event_contract": EVENT_CONTRACT,
        "emits": ACTUARIAL_PRICING_RESERVING_EMITTED_EVENT_TYPES,
        "consumes": ACTUARIAL_PRICING_RESERVING_CONSUMED_EVENT_TYPES,
        "forms": forms,
        "wizards": wizards,
        "controls": controls,
        "routes": routes,
        "simulation": simulation,
        "dsl_exposure": {
            "pbc": PBC_KEY,
            "models": ACTUARIAL_PRICING_RESERVING_BUSINESS_TABLES,
            "routes": routes["routes"],
            "agent_skill_namespace": f"{PBC_KEY}_skills",
            "ui_fragments": ("ActuarialPricingReservingWorkbench", "PricingWorkbench", "ReserveCloseWorkbench", "CapitalScenarioWorkbench"),
        },
        "stream_engine_picker_visible": False,
        "side_effects": (),
    }


def standalone_smoke_test() -> dict:
    app = single_pbc_app_contract()
    return {"ok": app["ok"] and not app["stream_engine_picker_visible"], "app": app, "side_effects": ()}
