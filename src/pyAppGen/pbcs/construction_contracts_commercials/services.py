"""Service layer for the construction_contracts_commercials PBC."""
from __future__ import annotations

from .core import (
    EVENT_CONTRACT,
    PBC_KEY,
    SERVICE_COMMAND_OPERATIONS as COMMAND_OPERATIONS,
    SERVICE_QUERY_OPERATIONS as QUERY_OPERATIONS,
    _operation_contract,
    construction_contracts_commercials_approve_variation_order,
    construction_contracts_commercials_assess_notice_timeliness,
    construction_contracts_commercials_build_final_account_packet,
    construction_contracts_commercials_build_payment_certificate,
    construction_contracts_commercials_build_workbench_view,
    construction_contracts_commercials_certify_pay_application,
    construction_contracts_commercials_command_construction_contract,
    construction_contracts_commercials_configure_runtime,
    construction_contracts_commercials_create_lien_waiver,
    construction_contracts_commercials_empty_state,
    construction_contracts_commercials_generate_cash_flow_forecast,
    construction_contracts_commercials_generate_contractor_scorecard,
    construction_contracts_commercials_progress_contract_lifecycle,
    construction_contracts_commercials_query_workbench,
    construction_contracts_commercials_receive_event,
    construction_contracts_commercials_record_pay_application,
    construction_contracts_commercials_record_subcontract_package,
    construction_contracts_commercials_register_commercial_claim,
    construction_contracts_commercials_register_rule,
    construction_contracts_commercials_register_schema_extension,
    construction_contracts_commercials_release_retainage,
    construction_contracts_commercials_replay_dead_letter_event,
    construction_contracts_commercials_review_retainage,
    construction_contracts_commercials_run_change_impact_simulation,
    construction_contracts_commercials_set_parameter,
    construction_contracts_commercials_settle_commercial_claim,
)
from .models import ConstructionContractsCommercialsStandaloneStore, standalone_model_contract

_COMMAND_HANDLERS = {
    "configure_runtime": construction_contracts_commercials_configure_runtime,
    "set_parameter": lambda state, payload: construction_contracts_commercials_set_parameter(state, payload["name"], payload["value"]),
    "register_rule": construction_contracts_commercials_register_rule,
    "register_schema_extension": lambda state, payload: construction_contracts_commercials_register_schema_extension(
        state, payload["table"], payload["fields"]
    ),
    "receive_event": construction_contracts_commercials_receive_event,
    "command_construction_contract": construction_contracts_commercials_command_construction_contract,
    "create_construction_contract": construction_contracts_commercials_command_construction_contract,
    "progress_contract_lifecycle": construction_contracts_commercials_progress_contract_lifecycle,
    "record_pay_application": construction_contracts_commercials_record_pay_application,
    "certify_pay_application": construction_contracts_commercials_certify_pay_application,
    "review_retainage": construction_contracts_commercials_review_retainage,
    "release_retainage": construction_contracts_commercials_release_retainage,
    "approve_variation_order": construction_contracts_commercials_approve_variation_order,
    "assess_notice_timeliness": construction_contracts_commercials_assess_notice_timeliness,
    "register_commercial_claim": construction_contracts_commercials_register_commercial_claim,
    "settle_commercial_claim": construction_contracts_commercials_settle_commercial_claim,
    "create_lien_waiver": construction_contracts_commercials_create_lien_waiver,
    "record_subcontract_package": construction_contracts_commercials_record_subcontract_package,
    "run_change_impact_simulation": construction_contracts_commercials_run_change_impact_simulation,
    "replay_dead_letter_event": construction_contracts_commercials_replay_dead_letter_event,
}
_QUERY_HANDLERS = {
    "query_workbench": construction_contracts_commercials_query_workbench,
    "build_workbench_view": lambda state, payload: {
        "ok": True,
        "workbench": construction_contracts_commercials_build_workbench_view(
            state=state,
            tenant=payload.get("tenant", "default"),
            actor=payload.get("actor"),
        ),
        "side_effects": (),
    },
    "build_payment_certificate": construction_contracts_commercials_build_payment_certificate,
    "build_final_account_packet": construction_contracts_commercials_build_final_account_packet,
    "generate_cash_flow_forecast": construction_contracts_commercials_generate_cash_flow_forecast,
    "generate_contractor_scorecard": construction_contracts_commercials_generate_contractor_scorecard,
}


class ConstructionContractsCommercialsService:
    def __init__(self, state: dict | None = None):
        self.state = state or construction_contracts_commercials_empty_state()

    def __getattr__(self, name):
        if name in COMMAND_OPERATIONS:
            return lambda payload=None, _name=name: self._command(_name, payload or {})
        if name in QUERY_OPERATIONS:
            return lambda payload=None, _name=name: self._query(_name, payload or {})
        raise AttributeError(name)

    def _command(self, name: str, payload: dict) -> dict:
        result = _COMMAND_HANDLERS[name](self.state, dict(payload))
        if "state" in result:
            self.state = result["state"]
        return {
            **result,
            "operation": name,
            "operation_kind": "command",
            "read_only": False,
            "payload": dict(payload),
            "operation_contract": _operation_contract(name, "command"),
            "outbox_table": EVENT_CONTRACT["outbox_table"],
            "emits": (result.get("operation_contract", {}) or {}).get("emitted_event", _operation_contract(name, "command")["emitted_event"]),
            "transaction_boundary": "owned_datastore_plus_outbox",
        }

    def _query(self, name: str, payload: dict) -> dict:
        result = _QUERY_HANDLERS[name](self.state, dict(payload))
        return {
            **result,
            "operation": name,
            "operation_kind": "query",
            "read_only": True,
            "payload": dict(payload),
            "operation_contract": _operation_contract(name, "query"),
            "outbox_table": None,
            "emits": (),
        }


def service_operation_manifest() -> dict:
    return {
        "ok": True,
        "pbc": PBC_KEY,
        "service_class": "ConstructionContractsCommercialsService",
        "command_operations": COMMAND_OPERATIONS,
        "query_operations": QUERY_OPERATIONS,
        "event_contract": EVENT_CONTRACT,
        "side_effects": (),
    }


def service_operation_contracts() -> dict:
    contracts = tuple(_operation_contract(name, "command") for name in COMMAND_OPERATIONS) + tuple(
        _operation_contract(name, "query") for name in QUERY_OPERATIONS
    )
    return {
        "ok": True,
        "pbc": PBC_KEY,
        "contracts": contracts,
        "operation_contract": contracts[0],
        "side_effects": (),
    }


def operation_plan(operation: str, payload: dict | None = None) -> dict:
    manifest = service_operation_manifest()
    all_operations = manifest["command_operations"] + manifest["query_operations"]
    kind = "query" if operation in manifest["query_operations"] else "command"
    return {
        "ok": operation in all_operations,
        "operation": operation,
        "operation_kind": kind,
        "payload": dict(payload or {}),
        "side_effects": (),
    }


STANDALONE_OPERATION_CONTRACTS = (
    {
        "operation": "create_contract",
        "operation_kind": "command",
        "method": "POST",
        "path": "/app/construction-contracts-commercials/contracts",
        "handler": "create_contract",
        "permission": "construction_contracts_commercials.create",
        "table": "construction_contracts_commercials_construction_contract",
        "form": "construction_contract_create_form",
        "wizard": "contract_award_wizard",
    },
    {
        "operation": "progress_contract_lifecycle",
        "operation_kind": "command",
        "method": "POST",
        "path": "/app/construction-contracts-commercials/contracts/lifecycle",
        "handler": "progress_contract_lifecycle",
        "permission": "construction_contracts_commercials.update",
        "table": "construction_contracts_commercials_construction_contract",
        "form": "construction_contract_create_form",
        "wizard": "contract_award_wizard",
    },
    {
        "operation": "record_pay_application",
        "operation_kind": "command",
        "method": "POST",
        "path": "/app/construction-contracts-commercials/pay-applications",
        "handler": "record_pay_application",
        "permission": "construction_contracts_commercials.create",
        "table": "construction_contracts_commercials_pay_application",
        "form": "pay_application_intake_form",
        "wizard": "pay_application_certification_wizard",
    },
    {
        "operation": "create_lien_waiver",
        "operation_kind": "command",
        "method": "POST",
        "path": "/app/construction-contracts-commercials/lien-waivers",
        "handler": "create_lien_waiver",
        "permission": "construction_contracts_commercials.accept_waiver",
        "table": "construction_contracts_commercials_lien_waiver",
        "form": "lien_waiver_review_form",
        "wizard": "pay_application_certification_wizard",
    },
    {
        "operation": "certify_pay_application",
        "operation_kind": "command",
        "method": "POST",
        "path": "/app/construction-contracts-commercials/pay-applications/certify",
        "handler": "certify_pay_application",
        "permission": "construction_contracts_commercials.certify_pay_application",
        "table": "construction_contracts_commercials_pay_application",
        "form": "pay_application_intake_form",
        "wizard": "pay_application_certification_wizard",
    },
    {
        "operation": "review_retainage",
        "operation_kind": "command",
        "method": "POST",
        "path": "/app/construction-contracts-commercials/retainage/hold",
        "handler": "review_retainage",
        "permission": "construction_contracts_commercials.update",
        "table": "construction_contracts_commercials_retainage",
        "form": "retainage_release_form",
        "wizard": "final_account_closeout_wizard",
    },
    {
        "operation": "release_retainage",
        "operation_kind": "command",
        "method": "POST",
        "path": "/app/construction-contracts-commercials/retainage/release",
        "handler": "release_retainage",
        "permission": "construction_contracts_commercials.release_retainage",
        "table": "construction_contracts_commercials_retainage",
        "form": "retainage_release_form",
        "wizard": "final_account_closeout_wizard",
    },
    {
        "operation": "approve_variation_order",
        "operation_kind": "command",
        "method": "POST",
        "path": "/app/construction-contracts-commercials/variation-orders",
        "handler": "approve_variation_order",
        "permission": "construction_contracts_commercials.approve_variation",
        "table": "construction_contracts_commercials_variation_order",
        "form": "variation_order_review_form",
        "wizard": "variation_negotiation_wizard",
    },
    {
        "operation": "register_commercial_claim",
        "operation_kind": "command",
        "method": "POST",
        "path": "/app/construction-contracts-commercials/commercial-claims",
        "handler": "register_commercial_claim",
        "permission": "construction_contracts_commercials.assess_claim",
        "table": "construction_contracts_commercials_commercial_claim",
        "form": "commercial_claim_notice_form",
        "wizard": "claim_entitlement_wizard",
    },
    {
        "operation": "record_subcontract_package",
        "operation_kind": "command",
        "method": "POST",
        "path": "/app/construction-contracts-commercials/subcontract-packages",
        "handler": "record_subcontract_package",
        "permission": "construction_contracts_commercials.update",
        "table": "construction_contracts_commercials_subcontract_package",
        "form": "subcontract_package_compliance_form",
        "wizard": "final_account_closeout_wizard",
    },
    {
        "operation": "build_workbench",
        "operation_kind": "query",
        "method": "GET",
        "path": "/app/construction-contracts-commercials/workbench",
        "handler": "build_workbench",
        "permission": "construction_contracts_commercials.read",
        "table": "construction_contracts_commercials_construction_contract",
        "form": None,
        "wizard": None,
    },
    {
        "operation": "build_payment_certificate",
        "operation_kind": "query",
        "method": "GET",
        "path": "/app/construction-contracts-commercials/payment-certificate",
        "handler": "build_payment_certificate",
        "permission": "construction_contracts_commercials.read",
        "table": "construction_contracts_commercials_pay_application",
        "form": None,
        "wizard": None,
    },
    {
        "operation": "build_final_account_packet",
        "operation_kind": "query",
        "method": "GET",
        "path": "/app/construction-contracts-commercials/final-account",
        "handler": "build_final_account_packet",
        "permission": "construction_contracts_commercials.close_final_account",
        "table": "construction_contracts_commercials_construction_contract",
        "form": None,
        "wizard": None,
    },
    {
        "operation": "generate_cash_flow_forecast",
        "operation_kind": "query",
        "method": "GET",
        "path": "/app/construction-contracts-commercials/forecast",
        "handler": "generate_cash_flow_forecast",
        "permission": "construction_contracts_commercials.read",
        "table": "construction_contracts_commercials_pay_application",
        "form": None,
        "wizard": None,
    },
    {
        "operation": "generate_contractor_scorecard",
        "operation_kind": "query",
        "method": "GET",
        "path": "/app/construction-contracts-commercials/scorecard",
        "handler": "generate_contractor_scorecard",
        "permission": "construction_contracts_commercials.read",
        "table": "construction_contracts_commercials_construction_contract",
        "form": None,
        "wizard": None,
    },
)


class ConstructionContractsCommercialsStandaloneService:
    """Executable standalone one-PBC service backed by the package-local store."""

    def __init__(self, store: ConstructionContractsCommercialsStandaloneStore | None = None):
        self.store = store or ConstructionContractsCommercialsStandaloneStore()

    def create_contract(self, payload=None):
        return self.store.create_contract(payload or {})

    def progress_contract_lifecycle(self, payload=None):
        return self.store.progress_contract_lifecycle(payload or {})

    def record_pay_application(self, payload=None):
        return self.store.record_pay_application(payload or {})

    def create_lien_waiver(self, payload=None):
        return self.store.create_lien_waiver(payload or {})

    def certify_pay_application(self, payload=None):
        return self.store.certify_pay_application(payload or {})

    def review_retainage(self, payload=None):
        return self.store.review_retainage(payload or {})

    def release_retainage(self, payload=None):
        return self.store.release_retainage(payload or {})

    def approve_variation_order(self, payload=None):
        return self.store.approve_variation_order(payload or {})

    def register_commercial_claim(self, payload=None):
        return self.store.register_commercial_claim(payload or {})

    def record_subcontract_package(self, payload=None):
        return self.store.record_subcontract_package(payload or {})

    def build_workbench(self, payload=None):
        payload = dict(payload or {})
        return self.store.build_workbench(payload.get("tenant", "default"), actor=payload.get("actor"))

    def build_payment_certificate(self, payload=None):
        return self.store.build_payment_certificate(payload or {})

    def build_final_account_packet(self, payload=None):
        return self.store.build_final_account_packet(payload or {})

    def generate_cash_flow_forecast(self, payload=None):
        return self.store.generate_cash_flow_forecast(payload or {})

    def generate_contractor_scorecard(self, payload=None):
        return self.store.generate_contractor_scorecard(payload or {})

    def close(self) -> None:
        self.store.close()


def standalone_service_operation_contracts() -> dict:
    return {
        "format": "appgen.construction-contracts-commercials-standalone-service-contract.v1",
        "ok": standalone_model_contract()["ok"] and bool(STANDALONE_OPERATION_CONTRACTS),
        "pbc": PBC_KEY,
        "service_class": "ConstructionContractsCommercialsStandaloneService",
        "contracts": STANDALONE_OPERATION_CONTRACTS,
        "operations": tuple(item["operation"] for item in STANDALONE_OPERATION_CONTRACTS),
        "command_operations": tuple(item["operation"] for item in STANDALONE_OPERATION_CONTRACTS if item["operation_kind"] == "command"),
        "query_operations": tuple(item["operation"] for item in STANDALONE_OPERATION_CONTRACTS if item["operation_kind"] == "query"),
        "side_effects": (),
    }


def standalone_operation_plan(operation: str, payload: dict | None = None) -> dict:
    contract = next((item for item in STANDALONE_OPERATION_CONTRACTS if item["operation"] == operation), None)
    return {
        "ok": contract is not None,
        "pbc": PBC_KEY,
        "operation": operation,
        "payload": dict(payload or {}),
        "contract": contract,
        "side_effects": (),
    }


def smoke_test() -> dict:
    service = ConstructionContractsCommercialsService()
    contract = service.command_construction_contract(
        {
            "tenant": "tenant-smoke",
            "contract_code": "SMOKE-001",
            "contract_value": 1000.0,
            "schedule_of_values": (
                {"line_code": "S1", "work_package": "Prelims", "original_value": 600.0},
                {"line_code": "S2", "work_package": "Works", "original_value": 400.0},
            ),
        }
    )
    query = service.query_workbench({"tenant": "tenant-smoke"})
    standalone = standalone_service_smoke_test()
    return {
        "ok": contract["ok"] and query["ok"] and service_operation_contracts()["ok"] and standalone["ok"],
        "command": contract,
        "query": query,
        "standalone": standalone,
        "side_effects": (),
    }


def standalone_service_smoke_test() -> dict:
    service = ConstructionContractsCommercialsStandaloneService()
    try:
        contract = service.create_contract(
            {
                "tenant": "tenant-standalone",
                "contract_code": "CCC-SVC-001",
                "contract_value": 90000.0,
                "schedule_of_values": (
                    {"line_code": "S1", "work_package": "Groundworks", "original_value": 50000.0},
                    {"line_code": "S2", "work_package": "Concrete", "original_value": 40000.0},
                ),
            }
        )
        package = service.record_subcontract_package(
            {
                "contract_code": "CCC-SVC-001",
                "package_code": "PKG-001",
                "subcontractor_name": "Crest Build Ltd",
                "contract_value": 20000.0,
                "insurance_status": "compliant",
                "bond_status": "compliant",
            }
        )
        workbench = service.build_workbench({"tenant": "tenant-standalone"})
        return {
            "ok": standalone_service_operation_contracts()["ok"] and contract["ok"] and package["ok"] and workbench["ok"],
            "contract": contract,
            "package": package,
            "workbench": workbench,
            "side_effects": (),
        }
    finally:
        service.close()
