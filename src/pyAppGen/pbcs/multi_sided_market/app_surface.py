"""One-PBC application surface for multi-sided market operations."""

from __future__ import annotations

import hashlib

PBC_KEY = "multi_sided_market"
OWNED_TABLES = (
    "multi_sided_market_participant_profile", "multi_sided_market_marketplace_listing",
    "multi_sided_market_listing_asset", "multi_sided_market_service_offer",
    "multi_sided_market_availability_window", "multi_sided_market_booking_reservation",
    "multi_sided_market_rental_contract", "multi_sided_market_loan_agreement",
    "multi_sided_market_barter_offer", "multi_sided_market_trade_order",
    "multi_sided_market_sale_order", "multi_sided_market_exchange_proposal",
    "multi_sided_market_escrow_account", "multi_sided_market_settlement_instruction",
    "multi_sided_market_dispute_case", "multi_sided_market_reputation_signal",
    "multi_sided_market_market_rule", "multi_sided_market_market_parameter",
    "multi_sided_market_schema_extension", "multi_sided_market_governed_model",
)


def _digest(*parts: object) -> str:
    return hashlib.sha256(repr(parts).encode("utf-8")).hexdigest()


def multi_sided_market_forms_contract() -> dict:
    """Return database-backed forms for a one-PBC market exchange app."""
    forms = (
        {"form_id": "participant_onboarding_form", "writes_table": "multi_sided_market_participant_profile", "command": "verify_participant", "fields": ("tenant", "participant_id", "role", "legal_name", "trust_tier", "kyc_status", "status"), "validations": ("role_supported", "kyc_required", "trust_tier_in_range", "policy_acknowledged")},
        {"form_id": "goods_listing_form", "writes_table": "multi_sided_market_marketplace_listing", "command": "publish_listing", "fields": ("tenant", "listing_id", "participant_id", "listing_type", "title", "currency", "price", "status"), "validations": ("participant_verified", "price_or_barter_terms_required", "category_policy_checked")},
        {"form_id": "listing_asset_form", "writes_table": "multi_sided_market_listing_asset", "command": "register_listing_asset", "fields": ("tenant", "asset_id", "listing_id", "asset_type", "condition_grade", "collateral_value", "status"), "validations": ("listing_exists", "condition_grade_required", "ownership_evidence_required")},
        {"form_id": "service_offer_form", "writes_table": "multi_sided_market_service_offer", "command": "create_service_offer", "fields": ("tenant", "service_offer_id", "listing_id", "provider_id", "skills", "duration_minutes", "service_area", "status"), "validations": ("provider_verified", "skills_declared", "service_area_supported")},
        {"form_id": "availability_window_form", "writes_table": "multi_sided_market_availability_window", "command": "publish_availability_window", "fields": ("tenant", "window_id", "listing_id", "starts_at", "ends_at", "capacity", "booking_policy", "status"), "validations": ("time_range_valid", "capacity_positive", "calendar_overlap_checked")},
        {"form_id": "trade_order_form", "writes_table": "multi_sided_market_trade_order", "command": "place_trade_order", "fields": ("tenant", "trade_order_id", "buyer_id", "listing_id", "quantity", "limit_price", "fulfillment_preference", "status"), "validations": ("buyer_verified", "inventory_or_capacity_available", "price_policy_checked")},
        {"form_id": "barter_offer_form", "writes_table": "multi_sided_market_barter_offer", "command": "match_barter_offer", "fields": ("tenant", "barter_offer_id", "offeror_id", "requested_listing_id", "offered_asset_id", "equivalence_value", "status"), "validations": ("asset_ownership_evidence", "equivalence_value_explained", "counterparty_policy_checked")},
        {"form_id": "exchange_proposal_form", "writes_table": "multi_sided_market_exchange_proposal", "command": "prepare_exchange_proposal", "fields": ("tenant", "proposal_id", "party_a", "party_b", "exchange_type", "terms", "risk_score", "status"), "validations": ("parties_verified", "terms_complete", "risk_score_in_range", "human_confirmation_required")},
        {"form_id": "sale_order_form", "writes_table": "multi_sided_market_sale_order", "command": "execute_sale", "fields": ("tenant", "sale_order_id", "buyer_id", "seller_id", "listing_id", "gross_amount", "payment_reference", "status"), "validations": ("payment_handoff_bound", "tax_projection_bound", "seller_verified")},
        {"form_id": "booking_reservation_form", "writes_table": "multi_sided_market_booking_reservation", "command": "reserve_booking", "fields": ("tenant", "booking_id", "listing_id", "participant_id", "window_id", "reserved_from", "reserved_until", "status"), "validations": ("window_available", "double_booking_prevented", "cancellation_policy_attached")},
        {"form_id": "rental_contract_form", "writes_table": "multi_sided_market_rental_contract", "command": "start_rental", "fields": ("tenant", "rental_id", "listing_id", "renter_id", "deposit_amount", "condition_in", "starts_at", "ends_at"), "validations": ("deposit_policy_met", "condition_documented", "max_rental_days_checked")},
        {"form_id": "loan_agreement_form", "writes_table": "multi_sided_market_loan_agreement", "command": "issue_loan", "fields": ("tenant", "loan_id", "asset_id", "borrower_id", "lender_id", "term_days", "collateral_value", "status"), "validations": ("borrower_verified", "collateral_sufficient", "return_terms_complete")},
        {"form_id": "escrow_account_form", "writes_table": "multi_sided_market_escrow_account", "command": "open_escrow", "fields": ("tenant", "escrow_id", "proposal_id", "amount", "currency", "hold_until", "release_policy_id", "status"), "validations": ("currency_supported", "release_policy_compiled", "funds_reference_required")},
        {"form_id": "settlement_instruction_form", "writes_table": "multi_sided_market_settlement_instruction", "command": "prepare_settlement", "fields": ("tenant", "settlement_id", "escrow_id", "payee_id", "amount", "fees", "tax_amount", "status"), "validations": ("escrow_releasable", "fees_disclosed", "tax_projection_bound")},
        {"form_id": "dispute_case_form", "writes_table": "multi_sided_market_dispute_case", "command": "open_dispute", "fields": ("tenant", "dispute_id", "proposal_id", "opened_by", "reason", "evidence_hash", "priority", "status"), "validations": ("evidence_hash_required", "proposal_exists", "resolution_sla_started")},
        {"form_id": "market_governance_form", "writes_table": "multi_sided_market_market_rule", "command": "register_rule", "fields": ("tenant", "rule_id", "scope", "listing_policy", "escrow_policy", "dispute_policy", "trust_policy", "status"), "validations": ("rule_compiles_to_hash", "market_impact_simulated", "rollback_plan_required")},
    )
    return {"ok": True, "pbc": PBC_KEY, "forms": forms, "side_effects": ()}


def multi_sided_market_wizards_contract() -> dict:
    wizards = (
        {"wizard_id": "participant_go_live_wizard", "steps": ("capture_profile", "verify_identity", "assign_roles", "set_trust_tier", "activate_participant"), "completion_event": "MarketParticipantVerified"},
        {"wizard_id": "listing_publish_wizard", "steps": ("create_listing", "attach_assets_or_service", "set_price_or_terms", "publish_availability", "publish_listing"), "completion_event": "MarketListingPublished"},
        {"wizard_id": "trade_and_sale_wizard", "steps": ("place_order", "check_inventory_or_capacity", "open_escrow", "capture_payment_reference", "execute_sale"), "completion_event": "SaleCompleted"},
        {"wizard_id": "barter_exchange_wizard", "steps": ("capture_offer", "score_equivalence", "match_counterparty", "prepare_proposal", "confirm_exchange"), "completion_event": "ExchangeProposalPrepared"},
        {"wizard_id": "booking_rental_wizard", "steps": ("select_window", "reserve_booking", "capture_deposit", "record_condition_in", "start_rental"), "completion_event": "RentalStarted"},
        {"wizard_id": "loan_agreement_wizard", "steps": ("select_asset", "verify_borrower", "value_collateral", "compile_return_terms", "issue_loan"), "completion_event": "LoanIssued"},
        {"wizard_id": "escrow_settlement_wizard", "steps": ("open_escrow", "compile_release_policy", "verify_completion", "release_escrow", "prepare_settlement"), "completion_event": "MarketSettlementPrepared"},
        {"wizard_id": "dispute_resolution_wizard", "steps": ("open_dispute", "collect_evidence", "triage_fault", "propose_resolution", "record_reputation_signal"), "completion_event": "MarketDisputeResolved"},
    )
    return {"ok": True, "pbc": PBC_KEY, "wizards": wizards, "side_effects": ()}


def multi_sided_market_controls_contract() -> dict:
    controls = (
        {"control_id": "participant_trust_and_kyc_gate", "blocks_on_failure": True, "table_scope": ("multi_sided_market_participant_profile", "multi_sided_market_reputation_signal")},
        {"control_id": "listing_ownership_and_policy_gate", "blocks_on_failure": True, "table_scope": ("multi_sided_market_marketplace_listing", "multi_sided_market_listing_asset")},
        {"control_id": "availability_double_booking_gate", "blocks_on_failure": True, "table_scope": ("multi_sided_market_availability_window", "multi_sided_market_booking_reservation")},
        {"control_id": "barter_equivalence_gate", "blocks_on_failure": True, "table_scope": ("multi_sided_market_barter_offer", "multi_sided_market_exchange_proposal")},
        {"control_id": "rental_condition_and_deposit_gate", "blocks_on_failure": True, "table_scope": ("multi_sided_market_rental_contract", "multi_sided_market_escrow_account")},
        {"control_id": "loan_collateral_and_return_terms_gate", "blocks_on_failure": True, "table_scope": ("multi_sided_market_loan_agreement", "multi_sided_market_listing_asset")},
        {"control_id": "payment_tax_settlement_gate", "blocks_on_failure": True, "table_scope": ("multi_sided_market_sale_order", "multi_sided_market_settlement_instruction")},
        {"control_id": "dispute_reputation_feedback_gate", "blocks_on_failure": True, "table_scope": ("multi_sided_market_dispute_case", "multi_sided_market_reputation_signal")},
        {"control_id": "appgen_event_replay_gate", "blocks_on_failure": True, "table_scope": ("multi_sided_market_appgen_outbox_event", "multi_sided_market_appgen_inbox_event", "multi_sided_market_dead_letter_event")},
        {"control_id": "owned_boundary_and_no_shared_tables_gate", "blocks_on_failure": True, "table_scope": OWNED_TABLES},
    )
    return {"ok": True, "pbc": PBC_KEY, "controls": controls, "side_effects": ()}


def single_pbc_multi_sided_market_app_contract() -> dict:
    forms = multi_sided_market_forms_contract()["forms"]
    wizards = multi_sided_market_wizards_contract()["wizards"]
    controls = multi_sided_market_controls_contract()["controls"]
    return {"ok": bool(forms) and bool(wizards) and bool(controls), "pbc": PBC_KEY, "single_pbc_app": True, "database_backed": True, "allowed_database_backends": ("postgresql", "mysql", "mariadb"), "owned_tables": OWNED_TABLES, "forms": forms, "wizards": wizards, "controls": controls, "workbench": "MarketExchangeWorkbench", "assistant_panel": "MultiSidedMarketAgent", "event_contract": "AppGen-X", "stream_engine_picker_visible": False, "side_effects": ()}


def document_instruction_multi_sided_market_plan(document: str, instructions: str) -> dict:
    text = f"{document} {instructions}".lower()
    if "participant" in text or "seller" in text or "provider" in text or "borrower" in text:
        operation, table = "verify_participant", "multi_sided_market_participant_profile"
    elif "barter" in text or "swap" in text:
        operation, table = "match_barter_offer", "multi_sided_market_barter_offer"
    elif "booking" in text or "reserve" in text or "calendar" in text:
        operation, table = "reserve_booking", "multi_sided_market_booking_reservation"
    elif "rental" in text or "rent" in text or "deposit" in text:
        operation, table = "start_rental", "multi_sided_market_rental_contract"
    elif "loan" in text or "borrow" in text or "lend" in text:
        operation, table = "issue_loan", "multi_sided_market_loan_agreement"
    elif "escrow" in text:
        operation, table = "open_escrow", "multi_sided_market_escrow_account"
    elif "settlement" in text or "payout" in text:
        operation, table = "prepare_settlement", "multi_sided_market_settlement_instruction"
    elif "dispute" in text or "refund" in text:
        operation, table = "open_dispute", "multi_sided_market_dispute_case"
    elif "service" in text:
        operation, table = "create_service_offer", "multi_sided_market_service_offer"
    elif "rule" in text or "policy" in text:
        operation, table = "register_rule", "multi_sided_market_market_rule"
    else:
        operation, table = "publish_listing", "multi_sided_market_marketplace_listing"
    return {"ok": True, "pbc": PBC_KEY, "document_digest": _digest(document, instructions), "proposed_operation": operation, "target_table": table, "requires_human_confirmation": True, "crud_datastore_mutation": True, "event_contract": "AppGen-X", "side_effects": ()}


def app_surface_smoke_test() -> dict:
    app = single_pbc_multi_sided_market_app_contract()
    rental = document_instruction_multi_sided_market_plan("equipment rental", "capture deposit and start rental")
    barter = document_instruction_multi_sided_market_plan("swap goods", "match barter offer")
    checks = (app["ok"], len(app["forms"]) >= 16, len(app["wizards"]) >= 8, len(app["controls"]) >= 10, rental["target_table"] == "multi_sided_market_rental_contract", barter["target_table"] == "multi_sided_market_barter_offer", all(table.startswith("multi_sided_market_") for control in app["controls"] for table in control["table_scope"]))
    return {"ok": all(checks), "single_pbc_app": app, "document_plans": (rental, barter), "side_effects": ()}
