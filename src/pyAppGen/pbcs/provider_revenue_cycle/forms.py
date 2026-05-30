"""Package-local forms for the Provider Revenue Cycle workbench."""

from __future__ import annotations

FORM_DEFINITIONS = (
    {
        "form_id": "patient_account_intake",
        "title": "Register patient account",
        "route": "POST /patient-accounts",
        "operation": "command_patient_account_intake",
        "permission": "provider_revenue_cycle.create",
        "owned_tables": ("provider_revenue_cycle_patient_account",),
        "fields": (
            {"name": "tenant", "type": "string", "required": True},
            {"name": "account_id", "type": "string", "required": True},
            {"name": "patient_id", "type": "string", "required": True},
            {"name": "encounter_id", "type": "string", "required": True},
            {"name": "coverage_priority", "type": "enum", "choices": ("primary", "secondary", "self_pay"), "required": True},
            {"name": "financial_class", "type": "enum", "choices": ("commercial", "medicare", "medicaid", "self_pay"), "required": True},
            {"name": "registration_status", "type": "enum", "choices": ("preregistered", "registered", "ready"), "required": True},
        ),
    },
    {
        "form_id": "eligibility_benefits_review",
        "title": "Review eligibility and benefits",
        "route": "POST /eligibility-benefits",
        "operation": "command_eligibility_benefits_review",
        "permission": "provider_revenue_cycle.update",
        "owned_tables": ("provider_revenue_cycle_patient_account",),
        "fields": (
            {"name": "account_id", "type": "string", "required": True},
            {"name": "payer_id", "type": "string", "required": True},
            {"name": "coverage_active", "type": "boolean", "required": True},
            {"name": "benefit_summary", "type": "string", "required": True},
            {"name": "patient_responsibility_estimate", "type": "number", "required": True},
        ),
    },
    {
        "form_id": "prior_authorization_link",
        "title": "Link prior authorization",
        "route": "POST /prior-authorizations",
        "operation": "command_prior_authorization_link",
        "permission": "provider_revenue_cycle.update",
        "owned_tables": ("provider_revenue_cycle_patient_account",),
        "fields": (
            {"name": "account_id", "type": "string", "required": True},
            {"name": "authorization_id", "type": "string", "required": True},
            {"name": "service_code", "type": "string", "required": True},
            {"name": "status", "type": "enum", "choices": ("submitted", "approved", "denied", "expired"), "required": True},
            {"name": "units_remaining", "type": "integer", "required": True},
        ),
    },
    {
        "form_id": "charge_capture",
        "title": "Capture charge",
        "route": "POST /charge-captures",
        "operation": "command_charge_capture",
        "permission": "provider_revenue_cycle.update",
        "owned_tables": ("provider_revenue_cycle_charge_capture",),
        "fields": (
            {"name": "account_id", "type": "string", "required": True},
            {"name": "charge_id", "type": "string", "required": True},
            {"name": "service_date", "type": "string", "required": True},
            {"name": "charge_code", "type": "string", "required": True},
            {"name": "expected_amount", "type": "number", "required": True},
            {"name": "captured_amount", "type": "number", "required": True},
        ),
    },
    {
        "form_id": "coding_cdi_review",
        "title": "Review coding and CDI",
        "route": "POST /coding-workqueues",
        "operation": "command_coding_review",
        "permission": "provider_revenue_cycle.update",
        "owned_tables": ("provider_revenue_cycle_coding_workqueue",),
        "fields": (
            {"name": "account_id", "type": "string", "required": True},
            {"name": "coding_case_id", "type": "string", "required": True},
            {"name": "case_type", "type": "enum", "choices": ("professional", "facility", "ed", "surgery"), "required": True},
            {"name": "documentation_status", "type": "enum", "choices": ("missing", "in_query", "complete"), "required": True},
            {"name": "diagnosis_codes", "type": "tuple", "required": True},
            {"name": "procedure_codes", "type": "tuple", "required": True},
        ),
    },
    {
        "form_id": "payer_contract_editor",
        "title": "Edit payer contract",
        "route": "POST /payer-contracts",
        "operation": "command_payer_contract_edit",
        "permission": "provider_revenue_cycle.admin",
        "owned_tables": ("provider_revenue_cycle_provider_revenue_cycle_policy_rule",),
        "fields": (
            {"name": "contract_id", "type": "string", "required": True},
            {"name": "payer_id", "type": "string", "required": True},
            {"name": "expected_rate", "type": "number", "required": True},
            {"name": "timely_filing_days", "type": "integer", "required": True},
            {"name": "status", "type": "enum", "choices": ("draft", "active", "retired"), "required": False},
        ),
    },
    {
        "form_id": "claim_scrub_submission",
        "title": "Create, scrub, or submit claim",
        "route": "POST /claims",
        "operation": "command_claim_create",
        "permission": "provider_revenue_cycle.update",
        "owned_tables": ("provider_revenue_cycle_claim_batch",),
        "fields": (
            {"name": "account_id", "type": "string", "required": True},
            {"name": "claim_id", "type": "string", "required": False},
            {"name": "batch_type", "type": "enum", "choices": ("professional", "institutional"), "required": False},
            {"name": "submit_after_scrub", "type": "boolean", "required": False},
        ),
    },
    {
        "form_id": "remit_era_posting",
        "title": "Post remit or ERA",
        "route": "POST /payment-postings/era",
        "operation": "command_remit_era_posting",
        "permission": "provider_revenue_cycle.update",
        "owned_tables": ("provider_revenue_cycle_payment_posting",),
        "fields": (
            {"name": "claim_id", "type": "string", "required": True},
            {"name": "payment_posting_id", "type": "string", "required": True},
            {"name": "allowed_amount", "type": "number", "required": True},
            {"name": "payment_amount", "type": "number", "required": True},
            {"name": "adjustment_amount", "type": "number", "required": True},
            {"name": "patient_responsibility_amount", "type": "number", "required": True},
        ),
    },
    {
        "form_id": "denial_appeal_work",
        "title": "Work denial or appeal",
        "route": "POST /denial-appeals",
        "operation": "command_denial_appeal",
        "permission": "provider_revenue_cycle.approve",
        "owned_tables": ("provider_revenue_cycle_denial_case",),
        "fields": (
            {"name": "denial_case_id", "type": "string", "required": True},
            {"name": "appeal_level", "type": "integer", "required": True},
            {"name": "packet_complete", "type": "boolean", "required": True},
            {"name": "submission_proof", "type": "string", "required": False},
        ),
    },
    {
        "form_id": "patient_balance_resolution",
        "title": "Resolve patient balance",
        "route": "POST /patient-billing",
        "operation": "command_patient_balance_resolution",
        "permission": "provider_revenue_cycle.update",
        "owned_tables": ("provider_revenue_cycle_collection_account",),
        "fields": (
            {"name": "account_id", "type": "string", "required": True},
            {"name": "statement_id", "type": "string", "required": False},
            {"name": "plan_id", "type": "string", "required": False},
            {"name": "assistance_id", "type": "string", "required": False},
            {"name": "refund_id", "type": "string", "required": False},
        ),
    },
    {
        "form_id": "close_reconciliation",
        "title": "Close and reconcile account",
        "route": "POST /reconcile-close",
        "operation": "command_reconcile_close",
        "permission": "provider_revenue_cycle.approve",
        "owned_tables": ("provider_revenue_cycle_collection_account",),
        "fields": (
            {"name": "account_id", "type": "string", "required": True},
            {"name": "expected_close_state", "type": "enum", "choices": ("zero_balance", "approved_writeoff"), "required": True},
            {"name": "reconciled_by", "type": "string", "required": True},
        ),
    },
    {
        "form_id": "assistant_document_instruction_preview",
        "title": "Preview assistant-guided CRUD change",
        "route": "POST /assistant/document-preview",
        "operation": "query_provider_revenue_cycle_assistant_preview",
        "permission": "provider_revenue_cycle.read",
        "owned_tables": ("provider_revenue_cycle_provider_revenue_cycle_control_assertion",),
        "fields": (
            {"name": "document_text", "type": "string", "required": True},
            {"name": "instructions", "type": "string", "required": True},
            {"name": "target_entity", "type": "string", "required": False},
            {"name": "requested_action", "type": "string", "required": False},
        ),
    },
)


def provider_revenue_cycle_form_catalog() -> dict:
    form_ids = tuple(form["form_id"] for form in FORM_DEFINITIONS)
    return {
        "ok": bool(FORM_DEFINITIONS),
        "pbc": "provider_revenue_cycle",
        "forms": FORM_DEFINITIONS,
        "form_ids": form_ids,
        "side_effects": (),
    }


def smoke_test() -> dict:
    catalog = provider_revenue_cycle_form_catalog()
    return {
        "ok": catalog["ok"] and len(catalog["forms"]) >= 10,
        "catalog": catalog,
        "side_effects": (),
    }
