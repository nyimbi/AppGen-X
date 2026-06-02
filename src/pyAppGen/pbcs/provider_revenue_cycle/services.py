"""Service layer for the provider_revenue_cycle PBC."""

from __future__ import annotations

from typing import Any

from . import standalone
from .agent import provider_revenue_cycle_assistant_preview
from .controls import provider_revenue_cycle_control_center
from .runtime import PBC_KEY
from .runtime import PROVIDER_REVENUE_CYCLE_REQUIRED_EVENT_TOPIC

EVENT_CONTRACT = {
    "contract": "appgen_event_contract",
    "topic": PROVIDER_REVENUE_CYCLE_REQUIRED_EVENT_TOPIC,
    "outbox_table": "provider_revenue_cycle_appgen_outbox_event",
    "inbox_table": "provider_revenue_cycle_appgen_inbox_event",
    "dead_letter_table": "provider_revenue_cycle_appgen_dead_letter_event",
    "event_contract": "AppGen-X",
    "retry_policy": {"max_attempts": 5, "backoff": "exponential"},
}

OPERATION_CONTRACTS = (
    {
        "operation": "command_patient_account_intake",
        "operation_kind": "command",
        "service_method": "intake_patient_account",
        "method": "POST",
        "path": "/patient-accounts",
        "permission": "provider_revenue_cycle.create",
        "owned_tables": ("provider_revenue_cycle_patient_account", "provider_revenue_cycle_appgen_outbox_event"),
        "read_tables": (),
        "emitted_event": "ProviderRevenueCycleCreated",
        "transaction_boundary": "owned_datastore_plus_outbox",
    },
    {
        "operation": "command_eligibility_benefits_review",
        "operation_kind": "command",
        "service_method": "review_eligibility_and_benefits",
        "method": "POST",
        "path": "/eligibility-benefits",
        "permission": "provider_revenue_cycle.update",
        "owned_tables": ("provider_revenue_cycle_patient_account",),
        "read_tables": (),
        "emitted_event": "ProviderRevenueCycleUpdated",
        "transaction_boundary": "owned_datastore_plus_outbox",
    },
    {
        "operation": "command_prior_authorization_link",
        "operation_kind": "command",
        "service_method": "link_prior_authorization",
        "method": "POST",
        "path": "/prior-authorizations",
        "permission": "provider_revenue_cycle.update",
        "owned_tables": ("provider_revenue_cycle_patient_account",),
        "read_tables": (),
        "emitted_event": "ProviderRevenueCycleUpdated",
        "transaction_boundary": "owned_datastore_plus_outbox",
    },
    {
        "operation": "command_charge_capture",
        "operation_kind": "command",
        "service_method": "capture_charge",
        "method": "POST",
        "path": "/charge-captures",
        "permission": "provider_revenue_cycle.update",
        "owned_tables": ("provider_revenue_cycle_charge_capture",),
        "read_tables": (),
        "emitted_event": "ProviderRevenueCycleUpdated",
        "transaction_boundary": "owned_datastore_plus_outbox",
    },
    {
        "operation": "command_coding_review",
        "operation_kind": "command",
        "service_method": "review_coding",
        "method": "POST",
        "path": "/coding-workqueues",
        "permission": "provider_revenue_cycle.update",
        "owned_tables": ("provider_revenue_cycle_coding_workqueue",),
        "read_tables": (),
        "emitted_event": "ProviderRevenueCycleUpdated",
        "transaction_boundary": "owned_datastore_plus_outbox",
    },
    {
        "operation": "command_payer_contract_edit",
        "operation_kind": "command",
        "service_method": "upsert_payer_contract",
        "method": "POST",
        "path": "/payer-contracts",
        "permission": "provider_revenue_cycle.admin",
        "owned_tables": ("provider_revenue_cycle_provider_revenue_cycle_policy_rule",),
        "read_tables": (),
        "emitted_event": "ProviderRevenueCycleUpdated",
        "transaction_boundary": "owned_datastore_plus_outbox",
    },
    {
        "operation": "command_claim_create",
        "operation_kind": "command",
        "service_method": "create_claim",
        "method": "POST",
        "path": "/claims",
        "permission": "provider_revenue_cycle.update",
        "owned_tables": ("provider_revenue_cycle_claim_batch",),
        "read_tables": (),
        "emitted_event": "ProviderRevenueCycleCreated",
        "transaction_boundary": "owned_datastore_plus_outbox",
    },
    {
        "operation": "command_claim_scrub",
        "operation_kind": "command",
        "service_method": "scrub_claim",
        "method": "POST",
        "path": "/claims/scrub",
        "permission": "provider_revenue_cycle.update",
        "owned_tables": ("provider_revenue_cycle_claim_batch",),
        "read_tables": (),
        "emitted_event": "ProviderRevenueCycleUpdated",
        "transaction_boundary": "owned_datastore_plus_outbox",
    },
    {
        "operation": "command_claim_submission",
        "operation_kind": "command",
        "service_method": "submit_claim",
        "method": "POST",
        "path": "/claims/submit",
        "permission": "provider_revenue_cycle.approve",
        "owned_tables": ("provider_revenue_cycle_claim_batch", "provider_revenue_cycle_appgen_outbox_event"),
        "read_tables": (),
        "emitted_event": "ProviderRevenueCycleApproved",
        "transaction_boundary": "owned_datastore_plus_outbox",
    },
    {
        "operation": "command_remit_era_posting",
        "operation_kind": "command",
        "service_method": "post_remittance_era",
        "method": "POST",
        "path": "/payment-postings/era",
        "permission": "provider_revenue_cycle.update",
        "owned_tables": ("provider_revenue_cycle_payment_posting", "provider_revenue_cycle_denial_case"),
        "read_tables": (),
        "emitted_event": "ProviderRevenueCycleUpdated",
        "transaction_boundary": "owned_datastore_plus_outbox",
    },
    {
        "operation": "command_denial_open",
        "operation_kind": "command",
        "service_method": "open_denial_case",
        "method": "POST",
        "path": "/denial-cases",
        "permission": "provider_revenue_cycle.approve",
        "owned_tables": ("provider_revenue_cycle_denial_case",),
        "read_tables": (),
        "emitted_event": "ProviderRevenueCycleExceptionOpened",
        "transaction_boundary": "owned_datastore_plus_outbox",
    },
    {
        "operation": "command_denial_appeal",
        "operation_kind": "command",
        "service_method": "appeal_denial",
        "method": "POST",
        "path": "/denial-appeals",
        "permission": "provider_revenue_cycle.approve",
        "owned_tables": ("provider_revenue_cycle_denial_case",),
        "read_tables": (),
        "emitted_event": "ProviderRevenueCycleApproved",
        "transaction_boundary": "owned_datastore_plus_outbox",
    },
    {
        "operation": "command_patient_statement_issue",
        "operation_kind": "command",
        "service_method": "generate_patient_statement",
        "method": "POST",
        "path": "/patient-billing",
        "permission": "provider_revenue_cycle.update",
        "owned_tables": ("provider_revenue_cycle_collection_account",),
        "read_tables": (),
        "emitted_event": "ProviderRevenueCycleUpdated",
        "transaction_boundary": "owned_datastore_plus_outbox",
    },
    {
        "operation": "command_payment_plan_enroll",
        "operation_kind": "command",
        "service_method": "enroll_payment_plan",
        "method": "POST",
        "path": "/payment-plans",
        "permission": "provider_revenue_cycle.update",
        "owned_tables": ("provider_revenue_cycle_collection_account",),
        "read_tables": (),
        "emitted_event": "ProviderRevenueCycleUpdated",
        "transaction_boundary": "owned_datastore_plus_outbox",
    },
    {
        "operation": "command_refund_credit_issue",
        "operation_kind": "command",
        "service_method": "issue_refund_or_credit",
        "method": "POST",
        "path": "/refunds-credits",
        "permission": "provider_revenue_cycle.approve",
        "owned_tables": ("provider_revenue_cycle_payment_posting",),
        "read_tables": (),
        "emitted_event": "ProviderRevenueCycleApproved",
        "transaction_boundary": "owned_datastore_plus_outbox",
    },
    {
        "operation": "command_financial_assistance",
        "operation_kind": "command",
        "service_method": "evaluate_financial_assistance",
        "method": "POST",
        "path": "/financial-assistance",
        "permission": "provider_revenue_cycle.approve",
        "owned_tables": ("provider_revenue_cycle_collection_account",),
        "read_tables": (),
        "emitted_event": "ProviderRevenueCycleApproved",
        "transaction_boundary": "owned_datastore_plus_outbox",
    },
    {
        "operation": "command_reconcile_close",
        "operation_kind": "command",
        "service_method": "reconcile_close",
        "method": "POST",
        "path": "/reconcile-close",
        "permission": "provider_revenue_cycle.approve",
        "owned_tables": ("provider_revenue_cycle_collection_account",),
        "read_tables": (),
        "emitted_event": "ProviderRevenueCycleApproved",
        "transaction_boundary": "owned_datastore_plus_outbox",
    },
    {
        "operation": "query_provider_revenue_cycle_workbench",
        "operation_kind": "query",
        "service_method": "build_ar_workqueue",
        "method": "GET",
        "path": "/provider-revenue-cycle-workbench",
        "permission": "provider_revenue_cycle.read",
        "owned_tables": (),
        "read_tables": ("provider_revenue_cycle_patient_account", "provider_revenue_cycle_collection_account", "provider_revenue_cycle_denial_case"),
        "emitted_event": None,
        "transaction_boundary": "read_only_projection",
    },
    {
        "operation": "query_provider_revenue_cycle_account_snapshot",
        "operation_kind": "query",
        "service_method": "account_snapshot",
        "method": "GET",
        "path": "/patient-account-snapshot",
        "permission": "provider_revenue_cycle.read",
        "owned_tables": (),
        "read_tables": ("provider_revenue_cycle_patient_account", "provider_revenue_cycle_claim_batch", "provider_revenue_cycle_payment_posting"),
        "emitted_event": None,
        "transaction_boundary": "read_only_projection",
    },
    {
        "operation": "query_provider_revenue_cycle_assistant_preview",
        "operation_kind": "query",
        "service_method": "assistant_preview",
        "method": "POST",
        "path": "/assistant/document-preview",
        "permission": "provider_revenue_cycle.read",
        "owned_tables": (),
        "read_tables": ("provider_revenue_cycle_provider_revenue_cycle_control_assertion",),
        "emitted_event": None,
        "transaction_boundary": "read_only_projection",
    },
    {
        "operation": "query_provider_revenue_cycle_controls",
        "operation_kind": "query",
        "service_method": "control_center",
        "method": "GET",
        "path": "/controls",
        "permission": "provider_revenue_cycle.admin",
        "owned_tables": (),
        "read_tables": ("provider_revenue_cycle_provider_revenue_cycle_control_assertion",),
        "emitted_event": None,
        "transaction_boundary": "read_only_projection",
    },
)


def service_operation_contracts() -> dict:
    operations = tuple(item["operation"] for item in OPERATION_CONTRACTS)
    command_contracts = tuple(item for item in OPERATION_CONTRACTS if item["operation_kind"] == "command")
    query_contracts = tuple(item for item in OPERATION_CONTRACTS if item["operation_kind"] == "query")
    return {
        "ok": bool(OPERATION_CONTRACTS)
        and all(item["transaction_boundary"] in {"owned_datastore_plus_outbox", "read_only_projection"} for item in OPERATION_CONTRACTS)
        and all(item["owned_tables"] and not item["read_tables"] for item in command_contracts)
        and all(item["read_tables"] and not item["owned_tables"] for item in query_contracts),
        "pbc": PBC_KEY,
        "operations": operations,
        "command_operations": tuple(item["operation"] for item in command_contracts),
        "query_operations": tuple(item["operation"] for item in query_contracts),
        "contracts": OPERATION_CONTRACTS,
        "side_effects": (),
    }


def operation_plan(operation_name: str, payload: dict | None = None) -> dict:
    contract = next((item for item in OPERATION_CONTRACTS if item["operation"] == operation_name), None)
    if contract is None:
        return {"ok": False, "reason": "unknown_operation", "operation": operation_name, "side_effects": ()}
    supplied = dict(payload or {})
    return {
        "ok": True,
        "pbc": PBC_KEY,
        "operation": operation_name,
        "operation_kind": contract["operation_kind"],
        "service_method": contract["service_method"],
        "route": {"method": contract["method"], "path": contract["path"]},
        "permission": contract["permission"],
        "owned_tables": contract["owned_tables"],
        "read_tables": contract["read_tables"],
        "emitted_event": contract["emitted_event"],
        "payload_keys": tuple(sorted(supplied)),
        "transaction_boundary": contract["transaction_boundary"],
        "event_contract": "AppGen-X",
        "side_effects": (),
    }


class ProviderRevenueCycleService:
    """Descriptor-only service facade kept for contract compatibility."""

    def _execute(self, operation_name: str, payload: dict[str, Any]) -> dict[str, Any]:
        plan = operation_plan(operation_name, payload)
        return {
            "ok": plan["ok"],
            "pbc": PBC_KEY,
            "operation": operation_name,
            "operation_kind": plan["operation_kind"],
            "payload": dict(payload),
            "operation_contract": plan,
            "transaction_boundary": plan.get("transaction_boundary"),
            "side_effects": (),
        }

    def __getattr__(self, name: str):
        if any(item["operation"] == name for item in OPERATION_CONTRACTS):
            return lambda payload=None, _name=name: self._execute(_name, payload or {})
        raise AttributeError(name)


class ProviderRevenueCycleStandaloneService:
    """Executable standalone service wrapper for the provider revenue cycle PBC."""

    def __init__(self, tenant: str = "default") -> None:
        self.app = standalone.ProviderRevenueCycleStandaloneApplication(tenant=tenant)

    def configure(self, config: dict[str, Any] | None = None) -> dict[str, Any]:
        return self.app.configure(config)

    def register_defaults(self) -> dict[str, Any]:
        return self.app.register_defaults()

    def intake_patient_account(self, payload: dict[str, Any]) -> dict[str, Any]:
        return self.app.intake_patient_account(payload)

    def review_eligibility_and_benefits(self, account_id: str, payload: dict[str, Any]) -> dict[str, Any]:
        return self.app.review_eligibility_and_benefits(account_id, payload)

    def link_prior_authorization(self, account_id: str, payload: dict[str, Any]) -> dict[str, Any]:
        return self.app.link_prior_authorization(account_id, payload)

    def capture_charge(self, account_id: str, payload: dict[str, Any]) -> dict[str, Any]:
        return self.app.capture_charge(account_id, payload)

    def review_coding(self, account_id: str, payload: dict[str, Any]) -> dict[str, Any]:
        return self.app.review_coding(account_id, payload)

    def upsert_payer_contract(self, payload: dict[str, Any]) -> dict[str, Any]:
        return self.app.upsert_payer_contract(payload)

    def create_claim(self, account_id: str) -> dict[str, Any]:
        return self.app.create_claim(account_id)

    def scrub_claim(self, claim_id: str) -> dict[str, Any]:
        return self.app.scrub_claim(claim_id)

    def submit_claim(self, claim_id: str) -> dict[str, Any]:
        return self.app.submit_claim(claim_id)

    def post_remittance_era(self, claim_id: str, payload: dict[str, Any]) -> dict[str, Any]:
        return self.app.post_remittance_era(claim_id, payload)

    def open_denial_case(self, claim_id: str, payload: dict[str, Any]) -> dict[str, Any]:
        return self.app.open_denial_case(claim_id, payload)

    def appeal_denial(self, denial_case_id: str, payload: dict[str, Any]) -> dict[str, Any]:
        return self.app.appeal_denial(denial_case_id, payload)

    def detect_underpayment(self, claim_id: str) -> dict[str, Any]:
        return self.app.detect_underpayment(claim_id)

    def generate_patient_statement(self, account_id: str, payload: dict[str, Any]) -> dict[str, Any]:
        return self.app.generate_patient_statement(account_id, payload)

    def enroll_payment_plan(self, account_id: str, payload: dict[str, Any]) -> dict[str, Any]:
        return self.app.enroll_payment_plan(account_id, payload)

    def issue_refund_or_credit(self, account_id: str, payload: dict[str, Any]) -> dict[str, Any]:
        return self.app.issue_refund_or_credit(account_id, payload)

    def evaluate_financial_assistance(self, account_id: str, payload: dict[str, Any]) -> dict[str, Any]:
        return self.app.evaluate_financial_assistance(account_id, payload)

    def build_ar_workqueue(self, tenant: str | None = None) -> dict[str, Any]:
        return self.app.build_ar_workqueue(tenant)

    def reconcile_close(self, account_id: str, payload: dict[str, Any] | None = None) -> dict[str, Any]:
        return self.app.reconcile_close(account_id, payload)

    def account_snapshot(self, account_id: str) -> dict[str, Any]:
        return self.app.account_snapshot(account_id)

    def assistant_preview(self, payload: dict[str, Any] | None = None) -> dict[str, Any]:
        return provider_revenue_cycle_assistant_preview(payload or {})

    def control_center(self, tenant: str | None = None) -> dict[str, Any]:
        return provider_revenue_cycle_control_center(self.app.state, tenant=tenant or self.app.tenant)


def standalone_service_manifest() -> dict[str, Any]:
    manifest = standalone.standalone_manifest()
    return {
        "ok": manifest["ok"],
        "pbc": PBC_KEY,
        "service_class": "ProviderRevenueCycleStandaloneService",
        "service_methods": manifest["service_methods"],
        "query_methods": (
            "build_ar_workqueue",
            "account_snapshot",
            "assistant_preview",
            "control_center",
        ),
        "event_contract": "AppGen-X",
        "event_topic": EVENT_CONTRACT["topic"],
        "transaction_boundary": "owned_datastore_plus_outbox",
        "stream_engine_picker_visible": False,
        "side_effects": (),
    }


def service_operation_manifest() -> dict:
    contracts = service_operation_contracts()
    return {
        "ok": contracts["ok"],
        "pbc": PBC_KEY,
        "service_class": "ProviderRevenueCycleService",
        "command_operations": contracts["command_operations"],
        "query_operations": contracts["query_operations"],
        "event_contract": EVENT_CONTRACT,
        "operation_contracts": contracts["contracts"],
        "standalone_service": standalone_service_manifest(),
        "side_effects": (),
    }


def smoke_test() -> dict:
    descriptor = ProviderRevenueCycleService()
    plan = descriptor.command_patient_account_intake({"tenant": "tenant-smoke"})
    service = ProviderRevenueCycleStandaloneService(tenant="tenant-smoke")
    service.configure()
    service.register_defaults()
    account = service.intake_patient_account(
        {
            "tenant": "tenant-smoke",
            "account_id": "acct_200",
            "patient_id": "patient_200",
            "encounter_id": "enc_200",
            "registration_status": "ready",
            "coverage_priority": "primary",
            "financial_class": "commercial",
            "guarantor": {"name": "Ada"},
        }
    )
    workbench = service.build_ar_workqueue()
    return {
        "ok": plan["ok"] and account["ok"] and workbench["ok"] and service_operation_manifest()["ok"],
        "plan": plan,
        "workbench": workbench,
        "side_effects": (),
    }
