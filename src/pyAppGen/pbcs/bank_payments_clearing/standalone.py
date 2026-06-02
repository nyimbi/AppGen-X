"""Standalone one-PBC app surface for bank_payments_clearing."""

from __future__ import annotations

from . import routes, ui
from .services import BankPaymentsClearingService
from .runtime import BANK_PAYMENTS_CLEARING_REQUIRED_EVENT_TOPIC


PBC_KEY = "bank_payments_clearing"


def _default_configuration() -> dict:
    return {
        "database_backend": "postgresql",
        "event_topic": BANK_PAYMENTS_CLEARING_REQUIRED_EVENT_TOPIC,
        "retry_limit": 5,
        "default_policy": "balanced",
        "agent_confirmation_required": True,
        "stream_engine_picker_visible": False,
    }


def bank_payments_clearing_bootstrap_app() -> dict:
    service = BankPaymentsClearingService()
    configure = service.configure_runtime({"configuration": _default_configuration()})
    service.set_parameter({"name": "workbench_limit", "value": 100})
    service.set_parameter({"name": "liquidity_buffer_amount", "value": 250.0})
    service.register_rule({"rule_id": "maker_checker_policy", "scope": "release"})
    service.receive_event(
        {
            "event_type": "PolicyChanged",
            "idempotency_key": "bootstrap-policy-change",
            "payload": {"policy": "balanced"},
        }
    )
    service.register_participant_bank(
        {
            "participant_bank": {
                "participant_bank_id": "bank_demo",
                "routing_identifier": "021000021",
                "supported_rails": ("ach", "wire"),
                "status": "active",
            }
        }
    )
    workbench = service.build_workbench_view({"tenant": "tenant_demo"})["result"]
    return {
        "ok": configure["ok"] and workbench["ok"],
        "pbc": PBC_KEY,
        "service": service,
        "service_state": service.snapshot(),
        "standalone_app": ui.bank_payments_clearing_standalone_app_contract(),
        "workbench": workbench,
        "routes": routes.api_route_contracts(),
        "side_effects": (),
    }


def bank_payments_clearing_run_demo_workflow() -> dict:
    app = bank_payments_clearing_bootstrap_app()
    service: BankPaymentsClearingService = app["service"]
    created = service.create_validated_payment_instruction(
        {
            "instruction": {
                "instruction_id": "pay_demo_1",
                "tenant": "tenant_demo",
                "rail": "ach",
                "participant_bank_id": "bank_demo",
                "amount": 1250.0,
                "currency": "USD",
                "beneficiary_account": "123456789",
                "beneficiary_name": "Demo Supplier",
                "originator_authorized": True,
                "external_reference": "DEMO-001",
                "screening_evidence": {"decision": "clear", "freshness": "current"},
            }
        }
    )
    released = service.release_payment_instruction(
        {
            "instruction_id": "pay_demo_1",
            "maker": "maker_demo",
            "checker": "checker_demo",
            "liquidity": {"available": 5000.0, "buffer": 250.0},
        }
    )
    batch = service.assemble_clearing_batch(
        {
            "batch_id": "batch_demo_1",
            "rail": "ach",
            "participant_bank_id": "bank_demo",
            "cutoff_context": {"missed_cutoff": False, "window": "same_day"},
        }
    )
    settlement = service.generate_settlement_file(
        {
            "file_id": "file_demo_1",
            "batch_id": "batch_demo_1",
            "sequence": 1,
            "channel": "host_to_host",
        }
    )
    workbench = service.build_workbench_view({"tenant": "tenant_demo"})["result"]
    return {
        "ok": created["ok"] and released["ok"] and batch["ok"] and settlement["ok"] and workbench["ok"],
        "app": app["standalone_app"],
        "service_state": service.snapshot(),
        "created": created,
        "released": released,
        "batch": batch,
        "settlement": settlement,
        "workbench": workbench,
        "side_effects": (),
    }


def bank_payments_clearing_release_snapshot() -> dict:
    from .release_evidence import build_release_evidence

    return build_release_evidence()


def bank_payments_clearing_standalone_app_contract() -> dict:
    return ui.bank_payments_clearing_standalone_app_contract()


def workbench_smoke_test() -> dict:
    app = bank_payments_clearing_bootstrap_app()
    demo = bank_payments_clearing_run_demo_workflow()
    return {
        "ok": app["ok"] and demo["ok"] and demo["app"]["ok"],
        "bootstrap": {
            "ok": app["ok"],
            "workbench": app["workbench"],
            "routes": app["routes"],
        },
        "demo": demo,
        "side_effects": (),
    }
