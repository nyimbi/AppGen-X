"""One-PBC application surface for cross-border trade operations."""

from __future__ import annotations

import hashlib

PBC_KEY = "cross_border_trade"
OWNED_TABLES = (
    "cross_border_trade_hs_classification",
    "cross_border_trade_landed_cost_quote",
    "cross_border_trade_export_control_check",
    "cross_border_trade_customs_declaration",
    "cross_border_trade_denied_party_screening",
    "cross_border_trade_trade_document_packet",
    "cross_border_trade_broker_handoff",
    "cross_border_trade_carrier_handoff",
    "cross_border_trade_trade_compliance_hold",
    "cross_border_trade_country_restriction_policy",
)


def _digest(*parts: object) -> str:
    return hashlib.sha256(repr(parts).encode("utf-8")).hexdigest()


def trade_forms_contract() -> dict:
    """Return the form inventory a single-PBC trade app can render."""
    forms = (
        {
            "form_id": "hs_classification_readiness_form",
            "writes_table": "cross_border_trade_hs_classification",
            "command": "classify_product",
            "fields": (
                "tenant",
                "product_id",
                "description",
                "material_facts",
                "country_of_origin",
                "destination_country",
                "end_use",
                "confidence",
                "reviewer",
            ),
            "validations": (
                "description_required",
                "origin_destination_required",
                "manual_review_below_threshold",
                "evidence_hash_required",
            ),
        },
        {
            "form_id": "landed_cost_quote_form",
            "writes_table": "cross_border_trade_landed_cost_quote",
            "command": "quote_landed_cost",
            "fields": (
                "tenant",
                "order_id",
                "classification_id",
                "incoterm",
                "origin_country",
                "destination_country",
                "goods_value",
                "shipping_cost",
                "insurance",
                "broker_fee",
                "currency",
            ),
            "validations": (
                "incoterm_supported",
                "positive_goods_value",
                "duty_tax_trace_required",
                "quote_expiry_required",
            ),
        },
        {
            "form_id": "restricted_party_screening_form",
            "writes_table": "cross_border_trade_denied_party_screening",
            "command": "screen_denied_party",
            "fields": (
                "tenant",
                "entity_id",
                "party_role",
                "legal_name",
                "aliases",
                "address",
                "list_sources",
                "match_strength",
                "reviewer",
            ),
            "validations": (
                "all_trade_parties_screened",
                "match_strength_review_threshold",
                "override_reason_required",
            ),
        },
        {
            "form_id": "export_control_check_form",
            "writes_table": "cross_border_trade_export_control_check",
            "command": "screen_export_control",
            "fields": (
                "tenant",
                "order_id",
                "classification_id",
                "destination_country",
                "end_use_statement",
                "end_user_risk",
                "license_id",
                "license_exception",
            ),
            "validations": (
                "classification_must_be_approved",
                "end_use_required",
                "license_required_when_policy_triggers",
            ),
        },
        {
            "form_id": "customs_declaration_form",
            "writes_table": "cross_border_trade_customs_declaration",
            "command": "file_customs_declaration",
            "fields": (
                "tenant",
                "declaration_id",
                "order_id",
                "quote_id",
                "check_id",
                "documents",
                "broker_id",
                "carrier_ref",
                "release_reference",
            ),
            "validations": (
                "documents_complete",
                "broker_payload_ready",
                "carrier_handoff_ready",
                "release_gate_clear",
            ),
        },
        {
            "form_id": "trade_compliance_hold_form",
            "writes_table": "cross_border_trade_trade_compliance_hold",
            "command": "open_trade_compliance_hold",
            "fields": (
                "tenant",
                "entity_id",
                "reason",
                "severity",
                "owner",
                "sla_due_at",
                "release_conditions",
            ),
            "validations": (
                "release_conditions_required",
                "owner_required_for_blocking_hold",
                "resolution_evidence_required",
            ),
        },
    )
    return {"ok": True, "pbc": PBC_KEY, "forms": forms, "side_effects": ()}


def trade_wizards_contract() -> dict:
    """Return guided workflows for specialist trade operators."""
    wizards = (
        {
            "wizard_id": "classification_approval_wizard",
            "steps": (
                "collect_product_facts",
                "compare_prior_rulings",
                "score_hs_candidates",
                "review_jurisdiction_variance",
                "approve_or_hold_classification",
            ),
            "completion_event": "HSClassified",
        },
        {
            "wizard_id": "landed_cost_scenario_wizard",
            "steps": (
                "select_trade_lane",
                "choose_incoterm",
                "calculate_duty_tax_fee_lines",
                "simulate_counterfactuals",
                "publish_customer_quote",
            ),
            "completion_event": "LandedCostQuoted",
        },
        {
            "wizard_id": "restricted_party_resolution_wizard",
            "steps": (
                "screen_all_parties",
                "review_fuzzy_matches",
                "capture_identity_evidence",
                "adjudicate_false_positive_or_block",
                "schedule_rescreen",
            ),
            "completion_event": "DeniedPartyScreened",
        },
        {
            "wizard_id": "declaration_release_wizard",
            "steps": (
                "verify_classification_quote_and_export_control",
                "assemble_document_packet",
                "queue_broker_handoff",
                "prepare_carrier_handoff",
                "resolve_holds",
                "release_declaration",
            ),
            "completion_event": "CustomsDeclarationReleased",
        },
        {
            "wizard_id": "policy_change_impact_wizard",
            "steps": (
                "register_country_restriction_policy",
                "compile_rule_hash",
                "simulate_open_orders",
                "identify_blocked_declarations",
                "activate_or_rollback_policy",
            ),
            "completion_event": "CountryRestrictionPolicyRegistered",
        },
    )
    return {"ok": True, "pbc": PBC_KEY, "wizards": wizards, "side_effects": ()}


def trade_controls_contract() -> dict:
    """Return release and operator controls exposed in the single-PBC app."""
    controls = (
        {
            "control_id": "hs_classification_readiness_gate",
            "blocks_on_failure": True,
            "table_scope": ("cross_border_trade_hs_classification",),
        },
        {
            "control_id": "landed_cost_trace_completeness_gate",
            "blocks_on_failure": True,
            "table_scope": ("cross_border_trade_landed_cost_quote",),
        },
        {
            "control_id": "restricted_party_release_gate",
            "blocks_on_failure": True,
            "table_scope": ("cross_border_trade_denied_party_screening", "cross_border_trade_trade_compliance_hold"),
        },
        {
            "control_id": "export_license_requirement_gate",
            "blocks_on_failure": True,
            "table_scope": ("cross_border_trade_export_control_check",),
        },
        {
            "control_id": "customs_document_packet_gate",
            "blocks_on_failure": True,
            "table_scope": ("cross_border_trade_trade_document_packet", "cross_border_trade_customs_declaration"),
        },
        {
            "control_id": "broker_carrier_handoff_gate",
            "blocks_on_failure": True,
            "table_scope": ("cross_border_trade_broker_handoff", "cross_border_trade_carrier_handoff"),
        },
        {
            "control_id": "customs_release_blocking_hold_gate",
            "blocks_on_failure": True,
            "table_scope": ("cross_border_trade_customs_declaration", "cross_border_trade_trade_compliance_hold"),
        },
        {
            "control_id": "owned_boundary_and_appgen_event_gate",
            "blocks_on_failure": True,
            "table_scope": OWNED_TABLES,
        },
    )
    return {"ok": True, "pbc": PBC_KEY, "controls": controls, "side_effects": ()}


def single_pbc_trade_app_contract() -> dict:
    """Return evidence that this PBC can form a standalone domain app."""
    forms = trade_forms_contract()["forms"]
    wizards = trade_wizards_contract()["wizards"]
    controls = trade_controls_contract()["controls"]
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
        "workbench": "CrossBorderTradeWorkbench",
        "assistant_panel": "CrossBorderTradeAgent",
        "event_contract": "AppGen-X",
        "stream_engine_picker_visible": False,
        "side_effects": (),
    }


def document_instruction_trade_plan(document: str, instructions: str) -> dict:
    """Map trade documents and instructions to governed CRUD previews."""
    text = f"{document} {instructions}".lower()
    if "denied" in text or "sanction" in text or "restricted party" in text:
        operation = "screen_denied_party"
        table = "cross_border_trade_denied_party_screening"
    elif "license" in text or "export" in text or "end use" in text:
        operation = "screen_export_control"
        table = "cross_border_trade_export_control_check"
    elif "invoice" in text or "packing" in text or "certificate" in text or "documents" in text:
        operation = "prepare_trade_document_packet"
        table = "cross_border_trade_trade_document_packet"
    elif "broker" in text:
        operation = "queue_broker_handoff"
        table = "cross_border_trade_broker_handoff"
    elif "carrier" in text:
        operation = "prepare_carrier_handoff"
        table = "cross_border_trade_carrier_handoff"
    elif "declaration" in text or "customs" in text or "release" in text:
        operation = "file_customs_declaration"
        table = "cross_border_trade_customs_declaration"
    elif "cost" in text or "duty" in text or "tax" in text or "incoterm" in text:
        operation = "quote_landed_cost"
        table = "cross_border_trade_landed_cost_quote"
    else:
        operation = "classify_product"
        table = "cross_border_trade_hs_classification"
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
    """Exercise the standalone app contracts."""
    app = single_pbc_trade_app_contract()
    invoice_plan = document_instruction_trade_plan("commercial invoice and packing list", "prepare documents")
    license_plan = document_instruction_trade_plan("end use statement", "check export license")
    checks = (
        app["ok"],
        len(app["forms"]) >= 6,
        len(app["wizards"]) >= 5,
        len(app["controls"]) >= 8,
        invoice_plan["proposed_operation"] == "prepare_trade_document_packet",
        license_plan["target_table"] == "cross_border_trade_export_control_check",
        all(table.startswith("cross_border_trade_") for control in app["controls"] for table in control["table_scope"]),
    )
    return {
        "ok": all(checks),
        "single_pbc_app": app,
        "document_plans": (invoice_plan, license_plan),
        "side_effects": (),
    }
