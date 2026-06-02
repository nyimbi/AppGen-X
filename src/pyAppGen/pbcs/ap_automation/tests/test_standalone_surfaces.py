"""Focused standalone-surface tests for the AP Automation PBC."""

from .. import control_contract, form_contract, implementation_contract, repository_contract, wizard_contract
from ..controls import evaluate_controls
from ..forms import render_form
from ..release_evidence import build_release_evidence
from ..repository import ApAutomationRepository, build_demo_state
from ..wizards import execute_wizard



def test_repository_and_forms_are_database_backed_and_owned_only():
    state = build_demo_state(include_release=False)
    repository = ApAutomationRepository()
    snapshot = repository.tenant_snapshot(state, "tenant_repo")
    rendered = render_form(
        "invoice_capture",
        state,
        tenant="tenant_repo",
        principal_permissions=("ap_automation.invoice",),
    )

    contract = implementation_contract()
    assert repository_contract()["ok"] is True
    assert form_contract()["ok"] is True
    assert snapshot["record_counts"]["vendors"] == 1
    assert rendered["ok"] is True
    assert rendered["defaults"]["candidate_purchase_orders"] == ("po_repo",)
    assert rendered["defaults"]["candidate_receipts"] == ("gr_repo",)
    assert contract["repository_contract"]["shared_table_access"] is False
    assert contract["forms_contract"]["database_backed"] is True



def test_payment_release_wizard_executes_batch_payment_and_advice():
    state = build_demo_state(include_release=False)
    result = execute_wizard(
        "payment_release_wizard",
        state,
        {
            "tenant": "tenant_repo",
            "liquidity_forecast": (5000, 4900, 4800),
            "risk_limit": 0.7,
            "batch_id": "batch_test_repo",
            "delivery_channel": "portal",
            "rails": (
                {"rail": "instant_bank_api", "cost": 5, "latency": 2, "fx_rate": 1.0, "available": False},
                {"rail": "ach", "cost": 1, "latency": 24, "fx_rate": 1.0, "available": True},
            ),
        },
    )

    payment = result["result"]["payment"]["payment"]
    advice = result["result"]["advice"]["advice"]
    assert wizard_contract()["ok"] is True
    assert result["ok"] is True
    assert payment["status"] == "executed"
    assert payment["batch_id"] == "batch_test_repo"
    assert advice["delivery_channel"] == "portal"



def test_controls_and_release_evidence_cover_standalone_surfaces():
    state = build_demo_state(include_release=True)
    controls = evaluate_controls(state, tenant="tenant_repo")
    evidence = build_release_evidence()

    assert control_contract()["ok"] is True
    assert controls["ok"] is True
    assert evidence["ok"] is True
    assert evidence["repository"]["ok"] is True
    assert evidence["forms"]["ok"] is True
    assert evidence["wizards"]["ok"] is True
    assert evidence["controls"]["ok"] is True
    assert {"repository_bound", "forms_bound", "wizards_bound", "controls_bound"} <= {
        check["id"] for check in evidence["checks"]
    }
