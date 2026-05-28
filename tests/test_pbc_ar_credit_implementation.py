from pyAppGen.pbcs.ar_credit import AR_CREDIT_IMPLEMENTED_BACKLOG_ITEMS
from pyAppGen.pbcs.ar_credit import AR_CREDIT_WORKFLOW_OPERATIONS
from pyAppGen.pbcs.ar_credit import ar_credit_configure_runtime
from pyAppGen.pbcs.ar_credit import ar_credit_empty_state
from pyAppGen.pbcs.ar_credit import ar_credit_register_rule
from pyAppGen.pbcs.ar_credit import ar_credit_set_parameter
from pyAppGen.pbcs.ar_credit.agent import agent_skill_manifest
from pyAppGen.pbcs.ar_credit.agent import cash_application_preview
from pyAppGen.pbcs.ar_credit.agent import collections_follow_up_preview
from pyAppGen.pbcs.ar_credit.agent import credit_onboarding_preview
from pyAppGen.pbcs.ar_credit.agent import document_instruction_plan
from pyAppGen.pbcs.ar_credit.agent import invoice_readiness_preview
from pyAppGen.pbcs.ar_credit.release_evidence import build_release_evidence
from pyAppGen.pbcs.ar_credit.release_evidence import release_readiness_manifest
from pyAppGen.pbcs.ar_credit.receivables_workflows import ar_credit_workflow_release_evidence
from pyAppGen.pbcs.ar_credit.services import ArCreditService
from pyAppGen.pbcs.ar_credit.services import service_operation_manifest
from pyAppGen.pbcs.ar_credit.ui import ar_credit_render_workbench
from pyAppGen.pbcs.ar_credit.ui import ar_credit_ui_contract


def test_credit_onboarding_preview_and_service_execution():
    state = _configured_state()
    preview = credit_onboarding_preview(
        {
            "customer_id": "cust-credit",
            "tenant": "tenant-ar",
            "name": "Credit Buyer",
            "terms": {"net_days": 30},
            "risk_signals": {"payment_latency": 0.04, "industry_stress": 0.03},
            "identity": {"did": "did:appgen:cust-credit", "issuer": "trusted_registry", "status": "active"},
            "requested_limit": 1200,
        }
    )

    assert preview["ok"] is True
    assert preview["review"]["ready"] is True
    assert preview["review"]["activation_decision"] == "approve"
    assert preview["review"]["recommended_limit"] > 0

    service = ArCreditService()
    executed = service.command_ar_customers(
        {
            "state": state,
            "customer": {
                "customer_id": "cust-credit",
                "tenant": "tenant-ar",
                "name": "Credit Buyer",
                "terms": {"net_days": 30},
                "risk_signals": {"payment_latency": 0.04, "industry_stress": 0.03},
                "identity": {"did": "did:appgen:cust-credit", "issuer": "trusted_registry", "status": "active"},
                "requested_limit": 1200,
            },
        }
    )

    assert executed["ok"] is True
    assert executed["customer"]["status"] == "active"
    assert executed["customer"]["credit_limit"] == executed["review"]["recommended_limit"]
    assert executed["state"]["outbox"][-1]["event_type"] == "CustomerOnboarded"
    assert executed["operation_contract"]["event_contract"] == "AppGen-X"


def test_invoice_readiness_blocks_credit_breach_then_allows_issue():
    state = _configured_state()
    service = ArCreditService()
    onboarded = service.command_ar_customers(
        {
            "state": state,
            "customer": {
                "customer_id": "cust-limit",
                "tenant": "tenant-ar",
                "name": "Limit Buyer",
                "terms": {"net_days": 30},
                "risk_signals": {"payment_latency": 0.02},
                "identity": {"did": "did:appgen:cust-limit", "issuer": "trusted_registry", "status": "active"},
                "requested_limit": 300,
            },
        }
    )
    state = onboarded["state"]

    blocked_preview = invoice_readiness_preview(
        {
            "state": state,
            "invoice": {
                "invoice_id": "ar_inv_blocked",
                "tenant": "tenant-ar",
                "customer_id": "cust-limit",
                "currency": "USD",
                "invoice_date": "2026-05-28",
                "due_date": "2026-06-27",
                "tax": {"jurisdiction": "US-NY", "amount": 40},
                "performance_obligations": ({"obligation": "service", "allocation": 400, "satisfied": True},),
                "lines": ({"sku": "service", "quantity": 1, "unit_price": 400, "account": "revenue"},),
            },
        }
    )
    assert blocked_preview["readiness"]["ready"] is False
    assert any(blocker["code"] == "credit_limit_available" for blocker in blocked_preview["readiness"]["blockers"])

    issued = service.command_ar_invoices(
        {
            "state": state,
            "invoice": {
                "invoice_id": "ar_inv_ready",
                "tenant": "tenant-ar",
                "customer_id": "cust-limit",
                "currency": "USD",
                "invoice_date": "2026-05-28",
                "due_date": "2026-06-27",
                "tax": {"jurisdiction": "US-NY", "amount": 16},
                "performance_obligations": ({"obligation": "service", "allocation": 100, "satisfied": True},),
                "lines": ({"sku": "service", "quantity": 1, "unit_price": 100, "account": "revenue"},),
            },
        }
    )

    assert issued["ok"] is True
    assert issued["readiness"]["ready"] is True
    assert issued["invoice"]["total"] == 116
    assert issued["state"]["outbox"][-1]["event_type"] == "InvoiceIssued"


def test_receipt_application_handles_overpayment_and_unmatched_cash():
    service = ArCreditService()
    state = _configured_state()
    state = service.command_ar_customers(
        {
            "state": state,
            "customer": {
                "customer_id": "cust-cash",
                "tenant": "tenant-ar",
                "name": "Cash Buyer",
                "terms": {"net_days": 30},
                "risk_signals": {"payment_latency": 0.01},
                "identity": {"did": "did:appgen:cust-cash", "issuer": "trusted_registry", "status": "active"},
                "requested_limit": 1500,
            },
        }
    )["state"]
    state = service.command_ar_invoices(
        {
            "state": state,
            "invoice": {
                "invoice_id": "ar_inv_cash",
                "tenant": "tenant-ar",
                "customer_id": "cust-cash",
                "currency": "USD",
                "invoice_date": "2026-05-28",
                "due_date": "2026-06-27",
                "tax": {"jurisdiction": "US-NY", "amount": 20},
                "performance_obligations": ({"obligation": "service", "allocation": 200, "satisfied": True},),
                "lines": ({"sku": "service", "quantity": 1, "unit_price": 200, "account": "revenue"},),
            },
        }
    )["state"]

    applied = service.command_ar_cash_applications(
        {
            "state": state,
            "receipt": {
                "receipt_id": "rcpt-over",
                "tenant": "tenant-ar",
                "amount": 260,
                "currency": "USD",
                "remittance_text": "PAY ar_inv_cash amount 260 bank_ref BAI-200",
            },
        }
    )

    assert applied["ok"] is True
    assert applied["decision"] == "apply_and_record_excess"
    assert applied["applied"]["application"]["applied_amount"] == 220
    assert applied["state"]["invoices"]["ar_inv_cash"]["status"] == "cleared"
    assert applied["excess_unapplied_cash"]["reason"] == "overpayment"

    unmatched_preview = cash_application_preview(
        {
            "state": applied["state"],
            "receipt": {
                "receipt_id": "rcpt-unmatched",
                "tenant": "tenant-ar",
                "amount": 75,
                "currency": "USD",
                "remittance_text": "payment with no invoice reference",
            },
        }
    )
    assert unmatched_preview["ok"] is True
    assert unmatched_preview["preview"]["decision"] == "record_unapplied_cash"
    assert unmatched_preview["preview"]["unapplied_cash"]["reason"] == "missing_or_unmatched_remittance"


def test_collections_follow_up_and_release_surfaces_expose_workflow_slice():
    service = ArCreditService()
    state = _configured_state()
    state = service.command_ar_customers(
        {
            "state": state,
            "customer": {
                "customer_id": "cust-collections",
                "tenant": "tenant-ar",
                "name": "Collections Buyer",
                "terms": {"net_days": 30},
                "risk_signals": {"payment_latency": 0.03},
                "identity": {"did": "did:appgen:cust-collections", "issuer": "trusted_registry", "status": "active"},
                "requested_limit": 2000,
            },
        }
    )["state"]
    state = service.command_ar_invoices(
        {
            "state": state,
            "invoice": {
                "invoice_id": "ar_inv_collect",
                "tenant": "tenant-ar",
                "customer_id": "cust-collections",
                "currency": "USD",
                "invoice_date": "2026-04-01",
                "due_date": "2026-04-30",
                "tax": {"jurisdiction": "US-NY", "amount": 12},
                "performance_obligations": ({"obligation": "service", "allocation": 150, "satisfied": True},),
                "lines": ({"sku": "service", "quantity": 1, "unit_price": 150, "account": "revenue"},),
            },
        }
    )["state"]

    follow_up = collections_follow_up_preview(
        {
            "state": state,
            "customer_id": "cust-collections",
            "as_of": "2026-07-30",
        }
    )
    workbench = service.query_ar_workbench(
        {
            "state": state,
            "tenant": "tenant-ar",
            "customer_id": "cust-collections",
            "as_of": "2026-07-30",
        }
    )
    rendered = ar_credit_render_workbench(
        state,
        tenant="tenant-ar",
        principal_permissions=("ar_credit.audit", "ar_credit.collection", "ar_credit.customer"),
    )
    ui_contract = ar_credit_ui_contract()
    service_manifest = service_operation_manifest()
    workflow_evidence = ar_credit_workflow_release_evidence()
    release = build_release_evidence()
    manifest = release_readiness_manifest()
    agent_manifest = agent_skill_manifest()
    instruction = document_instruction_plan("statement request", "prepare collections statement and dunning follow-up")

    assert follow_up["ok"] is True
    assert follow_up["follow_up"]["recommended_action"] == "schedule_collections_call"
    assert follow_up["follow_up"]["dunning_notices"][0]["level"] == "final"

    assert workbench["ok"] is True
    assert workbench["follow_up"]["recommended_action"] == "schedule_collections_call"
    assert "build_collections_follow_up" in rendered["workflow_actions"]
    assert rendered["focus_workflows"][3]["ready_count"] == 1

    assert service_manifest["workflow_operations"] == AR_CREDIT_WORKFLOW_OPERATIONS
    assert ui_contract["workflow_actions"] == AR_CREDIT_WORKFLOW_OPERATIONS
    assert workflow_evidence["implemented_backlog_items"] == AR_CREDIT_IMPLEMENTED_BACKLOG_ITEMS
    assert any(skill["name"].endswith("collections_follow_up_preview") for skill in agent_manifest["skills"])
    assert any(item["operation"] == "build_collections_follow_up" for item in instruction["workflow_suggestions"])
    assert release["workflow_slice"]["ok"] is True
    assert any(check["id"] == "service_workflow_surface" and check["ok"] for check in release["checks"])
    assert manifest["ok"] is True
    assert "workflow_slice" in manifest["sections"]


def _configured_state():
    state = ar_credit_empty_state()
    state = ar_credit_configure_runtime(
        state,
        {
            "database_backend": "postgresql",
            "event_topic": "appgen.ar.events",
            "retry_limit": 2,
            "default_currency": "USD",
            "default_timezone": "UTC",
            "allowed_collection_channels": ("portal", "api", "email"),
            "workbench_limit": 50,
        },
    )["state"]
    state = ar_credit_set_parameter(state, "auto_cash_threshold", 0.95)["state"]
    state = ar_credit_set_parameter(state, "credit_limit_buffer", 0.05)["state"]
    state = ar_credit_register_rule(
        state,
        {
            "rule_id": "rule-collections",
            "tenant": "tenant-ar",
            "scope": "cash_application",
            "auto_cash_threshold": 0.95,
            "status": "active",
        },
    )["state"]
    return state
