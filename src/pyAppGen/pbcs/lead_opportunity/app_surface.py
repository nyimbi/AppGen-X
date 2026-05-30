"""One-PBC application surface for enterprise lead and opportunity management."""

from __future__ import annotations

import hashlib

PBC_KEY = "lead_opportunity"
OWNED_TABLES = (
    "lead_opportunity_lead",
    "lead_opportunity_lead_enrichment_snapshot",
    "lead_opportunity_lead_dedup_case",
    "lead_opportunity_lead_score_snapshot",
    "lead_opportunity_lead_assignment",
    "lead_opportunity_qualification_decision",
    "lead_opportunity_opportunity",
    "lead_opportunity_opportunity_stage_history",
    "lead_opportunity_pipeline_forecast_snapshot",
    "lead_opportunity_quote_proposal_handoff",
    "lead_opportunity_opportunity_outcome",
    "lead_opportunity_account_hierarchy",
    "lead_opportunity_sales_activity",
    "lead_opportunity_sales_coaching_insight",
    "lead_opportunity_lead_opportunity_rule",
    "lead_opportunity_lead_opportunity_parameter",
    "lead_opportunity_lead_opportunity_configuration",
)


def _digest(*parts: object) -> str:
    return hashlib.sha256(repr(parts).encode("utf-8")).hexdigest()


def lead_opportunity_forms_contract() -> dict:
    """Return database-backed forms for a one-PBC revenue pipeline app."""
    forms = (
        {
            "form_id": "account_hierarchy_form",
            "writes_table": "lead_opportunity_account_hierarchy",
            "command": "create_account_hierarchy",
            "fields": ("tenant", "account_id", "name", "parent_account_id", "customer_id", "region", "owner", "status"),
            "validations": ("account_id_required", "region_supported", "owner_required", "parent_account_cycle_check"),
        },
        {
            "form_id": "lead_capture_form",
            "writes_table": "lead_opportunity_lead",
            "command": "create_lead",
            "fields": ("tenant", "lead_id", "account_id", "customer_id", "email", "company", "source", "region", "currency", "estimated_value"),
            "validations": ("lead_id_required", "email_or_company_required", "source_required", "currency_supported"),
        },
        {
            "form_id": "lead_enrichment_form",
            "writes_table": "lead_opportunity_lead_enrichment_snapshot",
            "command": "command_lead_enrichment",
            "fields": ("tenant", "snapshot_id", "lead_id", "segment_fit_score", "firmographic_fit", "intent_summary", "evidence_source"),
            "validations": ("lead_exists", "segment_score_between_zero_and_one", "evidence_source_required", "governed_model_required"),
        },
        {
            "form_id": "dedup_resolution_form",
            "writes_table": "lead_opportunity_lead_dedup_case",
            "command": "resolve_lead_dedup_case",
            "fields": ("tenant", "case_id", "lead_id", "duplicate_lead_id", "match_hash", "resolution_status", "survivorship_notes"),
            "validations": ("duplicate_pair_required", "match_hash_required", "survivorship_notes_required_for_merge"),
        },
        {
            "form_id": "qualification_decision_form",
            "writes_table": "lead_opportunity_qualification_decision",
            "command": "qualify_lead",
            "fields": ("tenant", "lead_id", "minimum_score", "actual_score", "decision", "assigned_owner", "disqualification_reason"),
            "validations": ("score_threshold_applied", "owner_required_for_qualified_lead", "reason_required_for_rejected_lead"),
        },
        {
            "form_id": "opportunity_creation_form",
            "writes_table": "lead_opportunity_opportunity",
            "command": "create_opportunity",
            "fields": ("tenant", "opportunity_id", "lead_id", "account_id", "name", "amount", "currency", "stage", "close_date", "win_probability"),
            "validations": ("qualified_lead_required", "positive_amount", "stage_supported", "close_date_required"),
        },
        {
            "form_id": "sales_activity_form",
            "writes_table": "lead_opportunity_sales_activity",
            "command": "record_sales_activity",
            "fields": ("tenant", "activity_id", "opportunity_id", "activity_type", "subject", "sentiment", "occurred_at", "owner", "next_best_action"),
            "validations": ("opportunity_exists", "activity_type_supported", "owner_required", "next_best_action_trace_required"),
        },
        {
            "form_id": "stage_and_forecast_form",
            "writes_table": "lead_opportunity_pipeline_forecast_snapshot",
            "command": "advance_opportunity",
            "fields": ("tenant", "opportunity_id", "from_stage", "to_stage", "forecast_amount", "confidence_floor", "slippage_risk"),
            "validations": ("valid_stage_transition", "forecast_amount_non_negative", "slippage_risk_between_zero_and_one"),
        },
        {
            "form_id": "quote_proposal_handoff_form",
            "writes_table": "lead_opportunity_quote_proposal_handoff",
            "command": "create_quote_proposal_handoff",
            "fields": ("tenant", "handoff_id", "opportunity_id", "proposal_reference", "handoff_owner", "required_products", "pricing_context"),
            "validations": ("proposal_reference_required", "handoff_owner_required", "opportunity_stage_allows_quote"),
        },
        {
            "form_id": "win_loss_outcome_form",
            "writes_table": "lead_opportunity_opportunity_outcome",
            "command": "win_opportunity_or_lose_opportunity",
            "fields": ("tenant", "opportunity_id", "outcome", "reason", "competitor_context", "customer_update_required", "closed_at"),
            "validations": ("outcome_reason_required", "customer_update_handoff_required_for_win", "forecast_snapshot_required"),
        },
        {
            "form_id": "sales_governance_form",
            "writes_table": "lead_opportunity_lead_opportunity_rule",
            "command": "register_rule",
            "fields": ("tenant", "rule_id", "scope", "allowed_regions", "allowed_currencies", "allowed_segments", "qualification_policy", "assignment_policy", "status"),
            "validations": ("required_rule_fields_present", "rule_compiles_to_hash", "impact_simulation_required"),
        },
    )
    return {"ok": True, "pbc": PBC_KEY, "forms": forms, "side_effects": ()}


def lead_opportunity_wizards_contract() -> dict:
    """Return guided workflows for revenue operators."""
    wizards = (
        {
            "wizard_id": "lead_intake_to_qualification_wizard",
            "steps": ("capture_lead", "enrich_lead", "deduplicate", "score_fit_and_engagement", "assign_owner", "qualify_or_reject"),
            "completion_event": "LeadQualified",
        },
        {
            "wizard_id": "account_based_selling_wizard",
            "steps": ("map_account_hierarchy", "link_customer_projection", "apply_segment_context", "assign_territory_owner", "open_target_opportunities"),
            "completion_event": "AccountHierarchyPrepared",
        },
        {
            "wizard_id": "opportunity_progression_wizard",
            "steps": ("create_opportunity", "record_discovery_activity", "advance_stage", "refresh_forecast", "produce_next_best_action"),
            "completion_event": "OpportunityAdvanced",
        },
        {
            "wizard_id": "proposal_handoff_wizard",
            "steps": ("validate_stage_readiness", "collect_products_and_pricing_context", "request_quote_proposal", "track_handoff_status", "update_pipeline_forecast"),
            "completion_event": "QuoteProposalRequested",
        },
        {
            "wizard_id": "win_loss_close_wizard",
            "steps": ("verify_close_evidence", "capture_outcome_reason", "publish_customer_update", "update_forecast", "record_coaching_insights"),
            "completion_event": "OpportunityWonOrLost",
        },
        {
            "wizard_id": "pipeline_governance_wizard",
            "steps": ("draft_rule_change", "compile_parameter_and_rule_hash", "simulate_open_pipeline_impact", "approve_activation", "monitor_post_change_anomalies"),
            "completion_event": "PipelinePolicyChanged",
        },
    )
    return {"ok": True, "pbc": PBC_KEY, "wizards": wizards, "side_effects": ()}


def lead_opportunity_controls_contract() -> dict:
    """Return controls for pipeline quality, compliance, and release readiness."""
    controls = (
        {"control_id": "lead_identity_and_dedup_gate", "blocks_on_failure": True, "table_scope": ("lead_opportunity_lead", "lead_opportunity_lead_dedup_case")},
        {"control_id": "qualification_score_evidence_gate", "blocks_on_failure": True, "table_scope": ("lead_opportunity_lead_score_snapshot", "lead_opportunity_qualification_decision")},
        {"control_id": "owner_assignment_and_territory_gate", "blocks_on_failure": True, "table_scope": ("lead_opportunity_lead_assignment", "lead_opportunity_account_hierarchy")},
        {"control_id": "stage_transition_integrity_gate", "blocks_on_failure": True, "table_scope": ("lead_opportunity_opportunity", "lead_opportunity_opportunity_stage_history")},
        {"control_id": "forecast_confidence_and_slippage_gate", "blocks_on_failure": True, "table_scope": ("lead_opportunity_pipeline_forecast_snapshot",)},
        {"control_id": "quote_handoff_readiness_gate", "blocks_on_failure": True, "table_scope": ("lead_opportunity_quote_proposal_handoff",)},
        {"control_id": "win_loss_customer_update_gate", "blocks_on_failure": True, "table_scope": ("lead_opportunity_opportunity_outcome", "lead_opportunity_opportunity")},
        {"control_id": "appgen_event_replay_gate", "blocks_on_failure": True, "table_scope": ("lead_opportunity_appgen_outbox_event", "lead_opportunity_appgen_inbox_event", "lead_opportunity_dead_letter_event")},
        {"control_id": "owned_boundary_and_no_shared_tables_gate", "blocks_on_failure": True, "table_scope": OWNED_TABLES},
    )
    return {"ok": True, "pbc": PBC_KEY, "controls": controls, "side_effects": ()}


def single_pbc_lead_opportunity_app_contract() -> dict:
    """Return evidence that this PBC can stand alone as a revenue pipeline app."""
    forms = lead_opportunity_forms_contract()["forms"]
    wizards = lead_opportunity_wizards_contract()["wizards"]
    controls = lead_opportunity_controls_contract()["controls"]
    return {
        "ok": bool(forms) and bool(wizards) and bool(controls),
        "pbc": PBC_KEY,
        "single_pbc_app": True,
        "database_backed": True,
        "allowed_database_backends": ("postgresql", "mysql", "mariadb"),
        "owned_tables": OWNED_TABLES,
        "forms": forms,
        "wizards": wizards,
        "controls": controls,
        "workbench": "LeadOpportunityWorkbench",
        "assistant_panel": "LeadOpportunityAgent",
        "event_contract": "AppGen-X",
        "stream_engine_picker_visible": False,
        "side_effects": (),
    }


def document_instruction_lead_opportunity_plan(document: str, instructions: str) -> dict:
    """Map sales documents and instructions to governed CRUD previews."""
    text = f"{document} {instructions}".lower()
    if "account" in text or "hierarchy" in text or "territory" in text:
        operation = "create_account_hierarchy"
        table = "lead_opportunity_account_hierarchy"
    elif "enrich" in text or "firmographic" in text or "intent" in text:
        operation = "command_lead_enrichment"
        table = "lead_opportunity_lead_enrichment_snapshot"
    elif "duplicate" in text or "dedup" in text or "merge" in text:
        operation = "resolve_lead_dedup_case"
        table = "lead_opportunity_lead_dedup_case"
    elif "qualify" in text or "score" in text or "mql" in text:
        operation = "qualify_lead"
        table = "lead_opportunity_qualification_decision"
    elif "quote" in text or "proposal" in text:
        operation = "create_quote_proposal_handoff"
        table = "lead_opportunity_quote_proposal_handoff"
    elif "win" in text or "loss" in text or "lost" in text or "close" in text:
        operation = "win_opportunity_or_lose_opportunity"
        table = "lead_opportunity_opportunity_outcome"
    elif "activity" in text or "call" in text or "meeting" in text or "email" in text:
        operation = "record_sales_activity"
        table = "lead_opportunity_sales_activity"
    elif "opportunity" in text or "deal" in text or "pipeline" in text:
        operation = "create_opportunity"
        table = "lead_opportunity_opportunity"
    elif "rule" in text or "parameter" in text or "policy" in text:
        operation = "register_rule"
        table = "lead_opportunity_lead_opportunity_rule"
    else:
        operation = "create_lead"
        table = "lead_opportunity_lead"
    return {
        "ok": True,
        "pbc": PBC_KEY,
        "document_digest": _digest(document, instructions),
        "proposed_operation": operation,
        "target_table": table,
        "requires_human_confirmation": True,
        "crud_datastore_mutation": True,
        "event_contract": "AppGen-X",
        "side_effects": (),
    }


def app_surface_smoke_test() -> dict:
    """Exercise standalone lead-opportunity app contracts."""
    app = single_pbc_lead_opportunity_app_contract()
    quote_plan = document_instruction_lead_opportunity_plan("proposal request", "create quote handoff")
    win_plan = document_instruction_lead_opportunity_plan("closed won note", "record win outcome")
    checks = (
        app["ok"],
        len(app["forms"]) >= 10,
        len(app["wizards"]) >= 6,
        len(app["controls"]) >= 9,
        quote_plan["target_table"] == "lead_opportunity_quote_proposal_handoff",
        win_plan["target_table"] == "lead_opportunity_opportunity_outcome",
        all(table.startswith("lead_opportunity_") for control in app["controls"] for table in control["table_scope"]),
    )
    return {"ok": all(checks), "single_pbc_app": app, "document_plans": (quote_plan, win_plan), "side_effects": ()}
