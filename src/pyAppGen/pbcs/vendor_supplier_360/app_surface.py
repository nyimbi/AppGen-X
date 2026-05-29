"""One-PBC application surface for vendor and supplier 360 operations."""

from __future__ import annotations

import hashlib

PBC_KEY = "vendor_supplier_360"
OWNED_TABLES = (
    "vendor_supplier_360_supplier_profile", "vendor_supplier_360_supplier_site",
    "vendor_supplier_360_supplier_certification", "vendor_supplier_360_supplier_bank_validation",
    "vendor_supplier_360_supplier_risk_signal", "vendor_supplier_360_supplier_esg_disclosure",
    "vendor_supplier_360_supplier_scorecard", "vendor_supplier_360_supplier_onboarding_case",
)


def _digest(*parts: object) -> str:
    return hashlib.sha256(repr(parts).encode("utf-8")).hexdigest()


def vendor_supplier_360_forms_contract() -> dict:
    forms = (
        {"form_id": "supplier_profile_form", "writes_table": "vendor_supplier_360_supplier_profile", "command": "create_supplier_profile", "fields": ("tenant", "supplier_id", "legal_name", "tax_id", "supplier_type", "risk_tier", "status"), "validations": ("legal_name_required", "tax_id_validated", "duplicate_supplier_checked", "sanctions_screened")},
        {"form_id": "supplier_site_form", "writes_table": "vendor_supplier_360_supplier_site", "command": "create_supplier_site", "fields": ("tenant", "site_id", "supplier_id", "address", "country", "fulfillment_role", "status"), "validations": ("supplier_exists", "country_supported", "site_role_declared", "address_verified")},
        {"form_id": "certification_form", "writes_table": "vendor_supplier_360_supplier_certification", "command": "record_certification", "fields": ("tenant", "certification_id", "supplier_id", "certification_type", "issuer", "valid_from", "valid_until", "status"), "validations": ("issuer_required", "expiry_in_future", "document_hash_required")},
        {"form_id": "bank_validation_form", "writes_table": "vendor_supplier_360_supplier_bank_validation", "command": "validate_bank_account", "fields": ("tenant", "validation_id", "supplier_id", "bank_country", "account_hash", "validation_status", "proof_hash"), "validations": ("account_hash_required", "dual_control_required", "payment_fraud_screened")},
        {"form_id": "risk_signal_form", "writes_table": "vendor_supplier_360_supplier_risk_signal", "command": "record_risk_signal", "fields": ("tenant", "risk_signal_id", "supplier_id", "signal_type", "severity", "source", "evidence_hash", "status"), "validations": ("severity_supported", "source_required", "evidence_hash_required", "risk_score_recalculated")},
        {"form_id": "esg_disclosure_form", "writes_table": "vendor_supplier_360_supplier_esg_disclosure", "command": "record_esg_disclosure", "fields": ("tenant", "disclosure_id", "supplier_id", "framework", "emissions_scope", "score", "assurance_status", "status"), "validations": ("framework_supported", "score_in_range", "assurance_evidence_required")},
        {"form_id": "scorecard_form", "writes_table": "vendor_supplier_360_supplier_scorecard", "command": "publish_scorecard", "fields": ("tenant", "scorecard_id", "supplier_id", "quality_score", "delivery_score", "risk_score", "esg_score", "status"), "validations": ("component_scores_in_range", "source_metrics_bound", "approval_required")},
        {"form_id": "onboarding_case_form", "writes_table": "vendor_supplier_360_supplier_onboarding_case", "command": "open_onboarding_case", "fields": ("tenant", "case_id", "supplier_id", "stage", "owner", "missing_evidence", "decision", "status"), "validations": ("owner_required", "stage_supported", "evidence_checklist_tracked", "decision_auditable")},
        {"form_id": "supplier_policy_form", "writes_table": "vendor_supplier_360_supplier_risk_signal", "command": "register_rule", "fields": ("tenant", "rule_id", "scope", "qualification_policy", "bank_policy", "esg_policy", "risk_policy", "status"), "validations": ("rule_compiles_to_hash", "impact_simulated", "rollback_plan_required")},
    )
    return {"ok": True, "pbc": PBC_KEY, "forms": forms, "side_effects": ()}


def vendor_supplier_360_wizards_contract() -> dict:
    wizards = (
        {"wizard_id": "supplier_onboarding_wizard", "steps": ("capture_profile", "screen_sanctions", "validate_tax", "collect_sites", "open_onboarding_case"), "completion_event": "SupplierOnboarded"},
        {"wizard_id": "qualification_wizard", "steps": ("collect_certifications", "validate_documents", "score_capability", "approve_qualification", "publish_status"), "completion_event": "SupplierQualified"},
        {"wizard_id": "bank_change_control_wizard", "steps": ("capture_account_hash", "dual_control_review", "fraud_screen", "validate_bank", "publish_bank_event"), "completion_event": "SupplierBankValidated"},
        {"wizard_id": "risk_review_wizard", "steps": ("record_signal", "recalculate_risk", "trigger_mitigation", "assign_owner", "monitor_recovery"), "completion_event": "SupplierRiskChanged"},
        {"wizard_id": "esg_assurance_wizard", "steps": ("collect_disclosure", "map_framework", "verify_evidence", "score_esg", "publish_scorecard"), "completion_event": "SupplierEsgUpdated"},
        {"wizard_id": "supplier_exit_wizard", "steps": ("freeze_new_orders", "review_open_liabilities", "notify_procurement", "archive_profile", "retain_audit_evidence"), "completion_event": "SupplierOffboarded"},
    )
    return {"ok": True, "pbc": PBC_KEY, "wizards": wizards, "side_effects": ()}


def vendor_supplier_360_controls_contract() -> dict:
    controls = (
        {"control_id": "duplicate_sanctions_tax_gate", "blocks_on_failure": True, "table_scope": ("vendor_supplier_360_supplier_profile", "vendor_supplier_360_supplier_onboarding_case")},
        {"control_id": "site_country_role_gate", "blocks_on_failure": True, "table_scope": ("vendor_supplier_360_supplier_site", "vendor_supplier_360_supplier_profile")},
        {"control_id": "certification_expiry_gate", "blocks_on_failure": True, "table_scope": ("vendor_supplier_360_supplier_certification", "vendor_supplier_360_supplier_scorecard")},
        {"control_id": "bank_dual_control_gate", "blocks_on_failure": True, "table_scope": ("vendor_supplier_360_supplier_bank_validation", "vendor_supplier_360_supplier_risk_signal")},
        {"control_id": "risk_signal_mitigation_gate", "blocks_on_failure": True, "table_scope": ("vendor_supplier_360_supplier_risk_signal", "vendor_supplier_360_supplier_onboarding_case")},
        {"control_id": "esg_assurance_gate", "blocks_on_failure": True, "table_scope": ("vendor_supplier_360_supplier_esg_disclosure", "vendor_supplier_360_supplier_scorecard")},
        {"control_id": "scorecard_source_metric_gate", "blocks_on_failure": True, "table_scope": ("vendor_supplier_360_supplier_scorecard", "vendor_supplier_360_supplier_profile")},
        {"control_id": "appgen_event_replay_gate", "blocks_on_failure": True, "table_scope": ("vendor_supplier_360_appgen_outbox_event", "vendor_supplier_360_appgen_inbox_event", "vendor_supplier_360_appgen_dead_letter_event")},
        {"control_id": "owned_boundary_and_no_shared_tables_gate", "blocks_on_failure": True, "table_scope": OWNED_TABLES},
    )
    return {"ok": True, "pbc": PBC_KEY, "controls": controls, "side_effects": ()}


def single_pbc_vendor_supplier_360_app_contract() -> dict:
    forms = vendor_supplier_360_forms_contract()["forms"]
    wizards = vendor_supplier_360_wizards_contract()["wizards"]
    controls = vendor_supplier_360_controls_contract()["controls"]
    return {"ok": bool(forms) and bool(wizards) and bool(controls), "pbc": PBC_KEY, "single_pbc_app": True, "database_backed": True, "allowed_database_backends": ("postgresql", "mysql", "mariadb"), "owned_tables": OWNED_TABLES, "forms": forms, "wizards": wizards, "controls": controls, "workbench": "VendorSupplier360Workbench", "assistant_panel": "VendorSupplier360AssistantPanel", "event_contract": "AppGen-X", "stream_engine_picker_visible": False, "side_effects": ()}


def document_instruction_vendor_supplier_360_plan(document: str, instructions: str) -> dict:
    text = f"{document} {instructions}".lower()
    if "bank" in text or "account" in text:
        operation, table = "validate_bank_account", "vendor_supplier_360_supplier_bank_validation"
    elif "cert" in text or "insurance" in text or "license" in text:
        operation, table = "record_certification", "vendor_supplier_360_supplier_certification"
    elif "site" in text or "address" in text or "plant" in text:
        operation, table = "create_supplier_site", "vendor_supplier_360_supplier_site"
    elif "risk" in text or "sanction" in text or "incident" in text:
        operation, table = "record_risk_signal", "vendor_supplier_360_supplier_risk_signal"
    elif "esg" in text or "carbon" in text or "sustain" in text:
        operation, table = "record_esg_disclosure", "vendor_supplier_360_supplier_esg_disclosure"
    elif "scorecard" in text or "performance" in text:
        operation, table = "publish_scorecard", "vendor_supplier_360_supplier_scorecard"
    elif "onboard" in text or "case" in text or "approve" in text:
        operation, table = "open_onboarding_case", "vendor_supplier_360_supplier_onboarding_case"
    else:
        operation, table = "create_supplier_profile", "vendor_supplier_360_supplier_profile"
    return {"ok": True, "pbc": PBC_KEY, "document_digest": _digest(document, instructions), "proposed_operation": operation, "target_table": table, "requires_human_confirmation": True, "crud_datastore_mutation": True, "event_contract": "AppGen-X", "side_effects": ()}


def app_surface_smoke_test() -> dict:
    app = single_pbc_vendor_supplier_360_app_contract()
    bank = document_instruction_vendor_supplier_360_plan("new bank account", "validate supplier bank")
    esg = document_instruction_vendor_supplier_360_plan("carbon disclosure", "record ESG evidence")
    checks = (app["ok"], len(app["forms"]) >= 9, len(app["wizards"]) >= 6, len(app["controls"]) >= 9, bank["target_table"] == "vendor_supplier_360_supplier_bank_validation", esg["target_table"] == "vendor_supplier_360_supplier_esg_disclosure", all(table.startswith("vendor_supplier_360_") for control in app["controls"] for table in control["table_scope"]))
    return {"ok": all(checks), "single_pbc_app": app, "document_plans": (bank, esg), "side_effects": ()}
