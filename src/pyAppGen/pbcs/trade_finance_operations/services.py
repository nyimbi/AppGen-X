"""Service layer for the trade_finance_operations PBC."""

from __future__ import annotations

from copy import deepcopy

from .domain_depth import DOMAIN_OPERATIONS as DOMAIN_DEPTH_COMMAND_OPERATIONS
from .domain_depth import DOMAIN_OWNED_TABLES as DOMAIN_DEPTH_OWNED_TABLES
from .domain_depth import execute_domain_operation as execute_domain_depth_operation
from . import runtime

PBC_KEY = "trade_finance_operations"
EVENT_CONTRACT = {
    "outbox_table": f"{PBC_KEY}_appgen_outbox_event",
    "inbox_table": f"{PBC_KEY}_appgen_inbox_event",
    "dead_letter_table": f"{PBC_KEY}_appgen_dead_letter_event",
    "event_contract": "AppGen-X",
}
COMMAND_OPERATIONS = (
    "configure_runtime",
    "set_parameter",
    "register_rule",
    "register_schema_extension",
    "receive_event",
    "command_letter_of_credit",
) + tuple(DOMAIN_DEPTH_COMMAND_OPERATIONS)
QUERY_OPERATIONS = (
    "query_workbench",
    "build_workbench_view",
    "build_case_detail",
    "build_release_evidence_pack",
    "run_advanced_assessment",
    "parse_document_instruction",
)
OWNED_TABLES = DOMAIN_DEPTH_OWNED_TABLES

_BASE_COMMAND_TABLES = {
    "configure_runtime": ("trade_finance_operations_trade_finance_operations_runtime_parameter",),
    "set_parameter": ("trade_finance_operations_trade_finance_operations_runtime_parameter",),
    "register_rule": ("trade_finance_operations_trade_finance_operations_policy_rule",),
    "register_schema_extension": ("trade_finance_operations_trade_finance_operations_schema_extension",),
    "receive_event": ("trade_finance_operations_appgen_inbox_event",),
    "command_letter_of_credit": ("trade_finance_operations_letter_of_credit",),
}


def _operation_contract(name: str, kind: str) -> dict:
    if name in DOMAIN_DEPTH_COMMAND_OPERATIONS:
        domain_plan = execute_domain_depth_operation(name, {})
        owned = tuple(domain_plan.get("owned_tables", ()))
        emitted = domain_plan.get("emitted_event")
    elif kind == "command":
        owned = _BASE_COMMAND_TABLES.get(name, OWNED_TABLES[:1])
        emitted = runtime.TRADE_FINANCE_OPERATIONS_EMITTED_EVENT_TYPES[0]
    else:
        owned = ()
        emitted = None
    read_tables = OWNED_TABLES[:6] if kind == "query" else ()
    return {
        "operation": name,
        "operation_kind": kind,
        "owned_tables": owned,
        "read_tables": read_tables,
        "emitted_event": emitted,
        "transaction_boundary": "owned_datastore_plus_outbox" if kind == "command" else "read_only_projection",
        "event_contract": "AppGen-X",
        "permission": f"{PBC_KEY}.operate",
    }


class TradeFinanceOperationsService:
    def __getattr__(self, name: str):
        if name in COMMAND_OPERATIONS:
            return lambda payload=None, _name=name: self._command(_name, payload or {})
        if name in QUERY_OPERATIONS:
            return lambda payload=None, _name=name: self._query(_name, payload or {})
        raise AttributeError(name)

    def _command(self, name: str, payload: dict) -> dict:
        if name in DOMAIN_DEPTH_COMMAND_OPERATIONS:
            plan = execute_domain_depth_operation(name, payload)
            return {
                "ok": plan["ok"],
                "operation": name,
                "operation_kind": "command",
                "read_only": False,
                "payload": dict(payload),
                "operation_contract": _operation_contract(name, "command"),
                "outbox_table": EVENT_CONTRACT["outbox_table"],
                "emits": (plan.get("emitted_event"),),
                "transaction_boundary": "owned_datastore_plus_outbox",
                "domain_depth": plan,
                "side_effects": (),
            }
        handler = getattr(runtime, f"{PBC_KEY}_{name}")
        state_result = handler(runtime.trade_finance_operations_empty_state(), payload) if name != "receive_event" else handler(runtime.trade_finance_operations_empty_state(), payload)
        return {
            "ok": state_result["ok"],
            "operation": name,
            "operation_kind": "command",
            "read_only": False,
            "payload": dict(payload),
            "operation_contract": _operation_contract(name, "command"),
            "outbox_table": EVENT_CONTRACT["outbox_table"],
            "emits": (_operation_contract(name, "command")["emitted_event"],),
            "transaction_boundary": "owned_datastore_plus_outbox",
            "result": state_result,
            "side_effects": (),
        }

    def _query(self, name: str, payload: dict) -> dict:
        if name == "query_workbench":
            result = runtime.trade_finance_operations_query_workbench(runtime.trade_finance_operations_empty_state(), payload)
        elif name == "build_workbench_view":
            result = runtime.trade_finance_operations_build_workbench_view(tenant=payload.get("tenant", "default"))
        elif name == "build_case_detail":
            result = runtime.trade_finance_operations_build_case_detail(payload.get("case_id", "TFO-SAMPLE"))
        elif name == "build_release_evidence_pack":
            result = runtime.trade_finance_operations_build_release_evidence_pack()
        elif name == "run_advanced_assessment":
            result = runtime.trade_finance_operations_run_advanced_assessment(runtime.trade_finance_operations_empty_state(), payload)
        else:
            result = runtime.trade_finance_operations_parse_document_instruction(payload.get("document", ""), payload.get("instruction", ""))
        return {
            "ok": result["ok"],
            "operation": name,
            "operation_kind": "query",
            "read_only": True,
            "payload": dict(payload),
            "operation_contract": _operation_contract(name, "query"),
            "outbox_table": None,
            "emits": (),
            "result": result,
            "side_effects": (),
        }


def service_operation_manifest() -> dict:
    return {
        "ok": True,
        "pbc": PBC_KEY,
        "service_class": "TradeFinanceOperationsService",
        "command_operations": COMMAND_OPERATIONS,
        "query_operations": QUERY_OPERATIONS,
        "operations": COMMAND_OPERATIONS + QUERY_OPERATIONS,
        "event_contract": EVENT_CONTRACT,
        "owned_tables": OWNED_TABLES,
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
        "command_operations": COMMAND_OPERATIONS,
        "query_operations": QUERY_OPERATIONS,
        "side_effects": (),
    }


def operation_plan(operation: str, payload: dict | None = None) -> dict:
    manifest = service_operation_manifest()
    kind = "query" if operation in manifest["query_operations"] else "command"
    return {
        "ok": operation in manifest["query_operations"] + manifest["command_operations"],
        "operation": operation,
        "operation_kind": kind,
        "payload": dict(payload or {}),
        "side_effects": (),
    }


def standalone_service_operation_contracts() -> dict:
    contracts = (
        {"method": "POST", "path": "/app/trade-finance/letters-of-credit", "operation": "issue_letter_of_credit", "operation_kind": "command", "table": "trade_finance_operations_letter_of_credit", "wizard": "TradeLetterOfCreditIssuanceWizard", "form": "TradeLetterOfCreditIssuanceForm", "permission": "trade_finance_operations.create", "event_contract": "AppGen-X"},
        {"method": "POST", "path": "/app/trade-finance/guarantees", "operation": "issue_bank_guarantee", "operation_kind": "command", "table": "trade_finance_operations_bank_guarantee", "wizard": "GuaranteeAndSBLCWizard", "form": "TradeGuaranteeStandbyForm", "permission": "trade_finance_operations.create", "event_contract": "AppGen-X"},
        {"method": "POST", "path": "/app/trade-finance/collections", "operation": "lodge_documentary_collection", "operation_kind": "command", "table": "trade_finance_operations_documentary_collection", "wizard": "DocumentaryCollectionWizard", "form": "TradeDocumentaryCollectionForm", "permission": "trade_finance_operations.create", "event_contract": "AppGen-X"},
        {"method": "POST", "path": "/app/trade-finance/bills", "operation": "register_trade_bill", "operation_kind": "command", "table": "trade_finance_operations_trade_bill", "wizard": "DocumentaryCollectionWizard", "form": "TradeBillCaptureForm", "permission": "trade_finance_operations.update", "event_contract": "AppGen-X"},
        {"method": "POST", "path": "/app/trade-finance/loans", "operation": "link_trade_loan", "operation_kind": "command", "table": "trade_finance_operations_trade_loan", "wizard": "TradeLoanAndSettlementWizard", "form": "TradeLoanLinkForm", "permission": "trade_finance_operations.update", "event_contract": "AppGen-X"},
        {"method": "POST", "path": "/app/trade-finance/document-packages", "operation": "record_shipment_documents", "operation_kind": "command", "table": "trade_finance_operations_trade_document", "wizard": "PresentationExaminationWizard", "form": "ShipmentDocumentPackageForm", "permission": "trade_finance_operations.update", "event_contract": "AppGen-X"},
        {"method": "POST", "path": "/app/trade-finance/sanctions-screenings", "operation": "run_sanctions_screening", "operation_kind": "command", "table": "trade_finance_operations_sanctions_check", "wizard": "PresentationExaminationWizard", "form": "SanctionsComplianceReviewForm", "permission": "trade_finance_operations.approve", "event_contract": "AppGen-X"},
        {"method": "POST", "path": "/app/trade-finance/examinations", "operation": "examine_document_package", "operation_kind": "command", "table": "trade_finance_operations_discrepancy_case", "wizard": "PresentationExaminationWizard", "form": "DiscrepancyDecisionForm", "permission": "trade_finance_operations.update", "event_contract": "AppGen-X"},
        {"method": "POST", "path": "/app/trade-finance/discrepancies", "operation": "request_discrepancy_waiver", "operation_kind": "command", "table": "trade_finance_operations_discrepancy_case", "wizard": "PresentationExaminationWizard", "form": "DiscrepancyDecisionForm", "permission": "trade_finance_operations.approve", "event_contract": "AppGen-X"},
        {"method": "POST", "path": "/app/trade-finance/collateral", "operation": "post_collateral_margin", "operation_kind": "command", "table": "trade_finance_operations_collateral_margin", "wizard": "TradeLoanAndSettlementWizard", "form": "CollateralMarginForm", "permission": "trade_finance_operations.update", "event_contract": "AppGen-X"},
        {"method": "POST", "path": "/app/trade-finance/limits", "operation": "reserve_limit_exposure", "operation_kind": "command", "table": "trade_finance_operations_limit_reservation", "wizard": "TradeLetterOfCreditIssuanceWizard", "form": "LimitReservationForm", "permission": "trade_finance_operations.approve", "event_contract": "AppGen-X"},
        {"method": "POST", "path": "/app/trade-finance/fees", "operation": "assess_case_fees", "operation_kind": "command", "table": "trade_finance_operations_fee_accrual", "wizard": "TradeLoanAndSettlementWizard", "form": "FeeSettlementForm", "permission": "trade_finance_operations.update", "event_contract": "AppGen-X"},
        {"method": "POST", "path": "/app/trade-finance/settlements", "operation": "settle_trade_case", "operation_kind": "command", "table": "trade_finance_operations_trade_settlement", "wizard": "TradeLoanAndSettlementWizard", "form": "SettlementReleaseForm", "permission": "trade_finance_operations.approve", "event_contract": "AppGen-X"},
        {"method": "POST", "path": "/app/trade-finance/swift-evidence", "operation": "generate_swift_message_evidence", "operation_kind": "command", "table": "trade_finance_operations_swift_message_evidence", "wizard": "ReleaseEvidenceReviewWizard", "form": "SwiftEvidenceForm", "permission": "trade_finance_operations.update", "event_contract": "AppGen-X"},
        {"method": "POST", "path": "/app/trade-finance/simulations", "operation": "simulate_case_amendment", "operation_kind": "command", "table": "trade_finance_operations_trade_document", "wizard": "ReleaseEvidenceReviewWizard", "form": "ShipmentDocumentPackageForm", "permission": "trade_finance_operations.read", "event_contract": "AppGen-X"},
        {"method": "GET", "path": "/app/trade-finance/workbench", "operation": "workbench", "operation_kind": "query", "table": "trade_finance_operations_letter_of_credit", "wizard": None, "form": None, "permission": "trade_finance_operations.read", "event_contract": "AppGen-X"},
        {"method": "GET", "path": "/app/trade-finance/case-detail", "operation": "case_detail", "operation_kind": "query", "table": "trade_finance_operations_letter_of_credit", "wizard": None, "form": None, "permission": "trade_finance_operations.read", "event_contract": "AppGen-X"},
        {"method": "GET", "path": "/app/trade-finance/release-evidence", "operation": "release_evidence", "operation_kind": "query", "table": "trade_finance_operations_trade_finance_operations_control_assertion", "wizard": None, "form": None, "permission": "trade_finance_operations.read", "event_contract": "AppGen-X"},
    )
    return {
        "format": "appgen.trade-finance-operations-standalone-service-contract.v1",
        "ok": True,
        "pbc": PBC_KEY,
        "contracts": contracts,
        "routes": tuple(f"{item['method']} {item['path']}" for item in contracts),
        "side_effects": (),
    }


class TradeFinanceOperationsStandaloneService:
    def __init__(self, tenant: str = "default") -> None:
        from .standalone import TradeFinanceOperationsStandaloneApp

        self.tenant = tenant
        self.app = TradeFinanceOperationsStandaloneApp(tenant=tenant)

    def close(self) -> None:
        return None

    def configure(self, configuration: dict | None = None) -> dict:
        return self.app.configure(configuration)

    def register_defaults(self) -> dict:
        return self.app.register_defaults()

    def issue_letter_of_credit(self, payload: dict) -> dict:
        return self.app.issue_letter_of_credit(payload)

    def issue_bank_guarantee(self, payload: dict) -> dict:
        return self.app.issue_bank_guarantee(payload)

    def lodge_documentary_collection(self, payload: dict) -> dict:
        return self.app.lodge_documentary_collection(payload)

    def register_trade_bill(self, payload: dict) -> dict:
        return self.app.register_trade_bill(payload)

    def link_trade_loan(self, payload: dict) -> dict:
        return self.app.link_trade_loan(payload)

    def record_shipment_documents(self, payload: dict) -> dict:
        return self.app.record_shipment_documents(payload)

    def run_sanctions_screening(self, payload: dict) -> dict:
        return self.app.run_sanctions_screening(payload)

    def examine_document_package(self, payload: dict) -> dict:
        return self.app.examine_document_package(payload)

    def request_discrepancy_waiver(self, payload: dict) -> dict:
        return self.app.request_discrepancy_waiver(payload)

    def post_collateral_margin(self, payload: dict) -> dict:
        return self.app.post_collateral_margin(payload)

    def reserve_limit_exposure(self, payload: dict) -> dict:
        return self.app.reserve_limit_exposure(payload)

    def assess_case_fees(self, payload: dict) -> dict:
        return self.app.assess_case_fees(payload)

    def settle_trade_case(self, payload: dict) -> dict:
        return self.app.settle_trade_case(payload)

    def generate_swift_message_evidence(self, payload: dict) -> dict:
        return self.app.generate_swift_message_evidence(payload)

    def simulate_case_amendment(self, payload: dict) -> dict:
        return self.app.simulate_case_amendment(payload)

    def workbench(self, tenant: str | None = None) -> dict:
        return self.app.build_workbench(tenant=tenant or self.tenant)

    def case_detail(self, case_id: str) -> dict:
        return self.app.build_case_detail(case_id)

    def release_evidence(self) -> dict:
        return self.app.build_release_evidence_pack()


def smoke_test() -> dict:
    service = TradeFinanceOperationsService()
    command = getattr(service, COMMAND_OPERATIONS[0])({"database_backend": "postgresql", "event_topic": runtime.TRADE_FINANCE_OPERATIONS_REQUIRED_EVENT_TOPIC})
    query = getattr(service, QUERY_OPERATIONS[0])({"tenant": "tenant-smoke"})
    standalone = TradeFinanceOperationsStandaloneService("tenant-smoke")
    standalone.configure()
    standalone.register_defaults()
    issue = standalone.issue_letter_of_credit({"case_id": "TFO-STANDALONE", "tenant": "tenant-smoke", "applicant": "Importer", "beneficiary": "Exporter", "currency": "USD", "face_amount": 100000})
    standalone.reserve_limit_exposure({"case_id": "TFO-STANDALONE", "facility_id": "FAC-1", "headroom": 150000, "requested_exposure": 100000})
    standalone.assess_case_fees({"case_id": "TFO-STANDALONE", "face_amount": 100000, "fee_rate_bps": 40, "swift_fee": 75})
    settlement = standalone.settle_trade_case({"case_id": "TFO-STANDALONE", "settlement_id": "SET-SMOKE", "gross_amount": 100000, "currency": "USD"})
    swift = standalone.generate_swift_message_evidence({"case_id": "TFO-STANDALONE", "message_type": "MT700"})
    release = standalone.release_evidence()
    return {
        "ok": command["ok"] and query["ok"] and issue["ok"] and settlement["ok"] and swift["ok"] and release["ok"] and service_operation_contracts()["ok"] and standalone_service_operation_contracts()["ok"],
        "command": command,
        "query": query,
        "issue": issue,
        "settlement": settlement,
        "swift": swift,
        "release": release,
        "side_effects": (),
    }
