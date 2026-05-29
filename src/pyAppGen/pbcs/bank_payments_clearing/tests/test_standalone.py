"""Standalone app tests for bank_payments_clearing."""

from __future__ import annotations

from .. import routes, standalone
from ..agent import datastore_crud_plan, document_instruction_plan
from ..services import BankPaymentsClearingService


def test_bootstrap_and_demo_workflow_expose_one_pbc_app_surface():
    app = standalone.bank_payments_clearing_bootstrap_app()
    demo = standalone.bank_payments_clearing_run_demo_workflow()
    release = standalone.bank_payments_clearing_release_snapshot()
    assert app["ok"] is True
    assert app["standalone_app"]["ok"] is True
    assert demo["ok"] is True
    assert demo["workbench"]["route"] == "/bank-payments-clearing-workbench"
    assert release["ok"] is True


def test_route_dispatch_executes_release_flow():
    service = BankPaymentsClearingService()
    routes.dispatch_route(
        "POST",
        "/runtime/configuration",
        {
            "configuration": {
                "database_backend": "postgresql",
                "event_topic": "pbc.bank_payments_clearing.events",
                "retry_limit": 5,
                "default_policy": "balanced",
            }
        },
        service=service,
    )
    bank = routes.dispatch_route(
        "POST",
        "/participant-banks",
        {
            "participant_bank": {
                "participant_bank_id": "bank_route_test",
                "routing_identifier": "021000021",
                "supported_rails": ("ach",),
                "status": "active",
            }
        },
        service=service,
    )
    create = routes.dispatch_route(
        "POST",
        "/payment-instructions",
        {
            "instruction": {
                "instruction_id": "pay_route_test",
                "tenant": "tenant_route_test",
                "rail": "ach",
                "participant_bank_id": "bank_route_test",
                "amount": 200.0,
                "currency": "USD",
                "beneficiary_account": "123456789",
                "beneficiary_name": "Route Test",
                "originator_authorized": True,
                "external_reference": "ROUTE-T-1",
                "screening_evidence": {"decision": "clear", "freshness": "current"},
            }
        },
        service=service,
    )
    release = routes.dispatch_route(
        "POST",
        "/payment-instructions/release",
        {
            "instruction_id": "pay_route_test",
            "maker": "maker",
            "checker": "checker",
            "liquidity": {"available": 1000.0, "buffer": 250.0},
        },
        service=service,
    )
    workbench = routes.dispatch_route("GET", "/bank-payments-clearing-workbench", {}, service=service)
    assert bank["ok"] is True
    assert create["ok"] is True
    assert release["ok"] is True
    assert workbench["ok"] is True


def test_agent_plans_document_and_crud_previews_for_standalone_flow():
    document_plan = document_instruction_plan(
        "instruction_id=pay_ai_1 participant_bank_id=bank_ai_1 rail=ach amount=99.5 currency=USD external_reference=AI-1",
        "validate then release the instruction",
    )
    crud_plan = datastore_crud_plan("update", "bank_payments_clearing_payment_instruction", {"instruction_id": "pay_ai_1"})
    assert document_plan["ok"] is True
    assert document_plan["mutation_preview"]
    assert crud_plan["ok"] is True
    assert crud_plan["operation_preview"]["operation"] == "release_payment_instruction"
