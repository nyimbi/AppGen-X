"""Focused standalone tests for provider_revenue_cycle."""

from __future__ import annotations

from pyAppGen.pbcs.provider_revenue_cycle import agent
from pyAppGen.pbcs.provider_revenue_cycle import audit
from pyAppGen.pbcs.provider_revenue_cycle import routes
from pyAppGen.pbcs.provider_revenue_cycle import services
from pyAppGen.pbcs.provider_revenue_cycle import standalone
from pyAppGen.pbcs.provider_revenue_cycle import ui


def _service():
    service = services.ProviderRevenueCycleStandaloneService(tenant="tenant_alpha")
    service.configure()
    service.register_defaults()
    return service


def test_standalone_clean_claim_to_era_and_patient_balance_journey():
    service = _service()
    account = service.intake_patient_account(
        {
            "tenant": "tenant_alpha",
            "account_id": "acct_400",
            "patient_id": "patient_400",
            "encounter_id": "enc_400",
            "registration_status": "ready",
            "coverage_priority": "primary",
            "financial_class": "commercial",
            "guarantor": {"name": "Ada"},
        }
    )
    eligibility = service.review_eligibility_and_benefits(
        "acct_400",
        {
            "payer_id": "payer_alpha",
            "coverage_active": True,
            "benefit_summary": "Office and ancillary visits covered",
            "patient_responsibility_estimate": 120.0,
        },
    )
    authorization = service.link_prior_authorization(
        "acct_400",
        {"authorization_id": "auth_400", "service_code": "99213", "status": "approved", "units_remaining": 4},
    )
    charge = service.capture_charge(
        "acct_400",
        {
            "charge_id": "chg_400",
            "service_date": "2026-05-30",
            "charge_code": "99213",
            "expected_amount": 180.0,
            "captured_amount": 180.0,
            "department": "clinic",
            "performing_clinician": "dr_smith",
        },
    )
    coding = service.review_coding(
        "acct_400",
        {
            "coding_case_id": "coding_400",
            "case_type": "professional",
            "documentation_status": "complete",
            "diagnosis_codes": ("I10",),
            "procedure_codes": ("99213",),
            "modifiers": ("25",),
        },
    )
    contract = service.upsert_payer_contract({"contract_id": "contract_400", "payer_id": "payer_alpha", "expected_rate": 150.0, "timely_filing_days": 90})
    claim = service.create_claim("acct_400")
    scrub = service.scrub_claim(claim["claim"]["claim_id"])
    submit = service.submit_claim(claim["claim"]["claim_id"])
    remit = service.post_remittance_era(
        claim["claim"]["claim_id"],
        {
            "payment_posting_id": "post_400",
            "allowed_amount": 150.0,
            "payment_amount": 140.0,
            "adjustment_amount": 10.0,
            "patient_responsibility_amount": 20.0,
        },
    )
    statement = service.generate_patient_statement("acct_400", {"statement_id": "stmt_400"})
    plan = service.enroll_payment_plan("acct_400", {"plan_id": "plan_400", "monthly_amount": 10.0, "term_months": 2})
    assistance = service.evaluate_financial_assistance("acct_400", {"assistance_id": "assist_400", "status": "approved", "discount_percent": 50.0})
    refund = service.issue_refund_or_credit("acct_400", {"refund_id": "refund_400", "type": "credit_balance", "amount": 5.0})
    snapshot = service.account_snapshot("acct_400")

    assert account["ok"] is True
    assert eligibility["account"]["eligibility_status"] == "verified"
    assert authorization["authorization"]["status"] == "approved"
    assert charge["charge"]["variance_amount"] == 0.0
    assert coding["coding_case"]["coding_status"] == "final"
    assert contract["contract"]["expected_rate"] == 150.0
    assert scrub["ok"] is True
    assert submit["ok"] is True
    assert remit["ok"] is True
    assert remit["underpayment"]["variance"] == 10.0
    assert statement["statement"]["status"] == "issued"
    assert plan["payment_plan"]["status"] == "active"
    assert assistance["assistance"]["status"] == "approved"
    assert refund["refund"]["status"] == "pending_approval"
    assert snapshot["account"]["patient_balance"] == 10.0


def test_denial_appeal_controls_routes_and_assistant_preview_are_executable():
    service = _service()
    service.intake_patient_account(
        {
            "tenant": "tenant_alpha",
            "account_id": "acct_500",
            "patient_id": "patient_500",
            "encounter_id": "enc_500",
            "registration_status": "ready",
            "coverage_priority": "primary",
            "financial_class": "commercial",
            "guarantor": {"name": "Ada"},
        }
    )
    service.review_eligibility_and_benefits(
        "acct_500",
        {"payer_id": "payer_beta", "coverage_active": True, "benefit_summary": "Covered", "patient_responsibility_estimate": 0.0},
    )
    service.link_prior_authorization("acct_500", {"authorization_id": "auth_500", "service_code": "99214", "status": "approved", "units_remaining": 2})
    service.capture_charge(
        "acct_500",
        {
            "charge_id": "chg_500",
            "service_date": "2026-05-30",
            "charge_code": "99214",
            "expected_amount": 200.0,
            "captured_amount": 200.0,
            "department": "clinic",
            "performing_clinician": "dr_jones",
        },
    )
    service.review_coding(
        "acct_500",
        {
            "coding_case_id": "coding_500",
            "case_type": "professional",
            "documentation_status": "complete",
            "diagnosis_codes": ("E11.9",),
            "procedure_codes": ("99214",),
        },
    )
    service.upsert_payer_contract({"contract_id": "contract_500", "payer_id": "payer_beta", "expected_rate": 180.0, "timely_filing_days": 90})
    claim = service.create_claim("acct_500")
    service.scrub_claim(claim["claim"]["claim_id"])
    service.submit_claim(claim["claim"]["claim_id"])
    denial = service.open_denial_case(
        claim["claim"]["claim_id"],
        {"denial_case_id": "denial_500", "category": "authorization", "payer_reason": "Missing auth detail", "root_cause": "registration", "preventable": True, "amount": 180.0},
    )
    appeal = service.appeal_denial("denial_500", {"appeal_level": 1, "packet_complete": True, "submission_proof": "fax-confirmation-500"})
    controls = service.control_center()
    dispatch = routes.dispatch_standalone_route(
        service,
        "POST",
        "/assistant/document-preview",
        {
            "document_text": "Appeal packet for denial_500 missing prior auth reference",
            "instructions": "update the denial appeal preview and show the clean claim controls",
            "requested_action": "update",
        },
    )
    agent_preview = agent.provider_revenue_cycle_assistant_preview(
        {
            "document_text": "Please revise the payer contract to catch underpayments",
            "instructions": "update the payer contract preview",
            "requested_action": "update",
        }
    )
    workbench = service.build_ar_workqueue("tenant_alpha")
    ui_smoke = ui.smoke_test()
    audit_result = audit.run_provider_revenue_cycle_pbc_audit()
    standalone_smoke = standalone.standalone_smoke_test()

    assert denial["ok"] is True
    assert appeal["denial"]["status"] == "appealed"
    assert controls["ok"] is True
    assert controls["assistant_guardrails"]["ok"] is True
    assert dispatch["ok"] is True
    assert agent_preview["ok"] is True
    assert workbench["ok"] is True
    assert any(queue["queue"] == "denials_and_underpayments" for queue in workbench["queues"])
    assert ui_smoke["ok"] is True
    assert audit_result["ok"] is True
    assert standalone_smoke["ok"] is True
