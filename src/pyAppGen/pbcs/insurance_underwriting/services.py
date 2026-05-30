"""Service surfaces for the insurance_underwriting PBC."""

from __future__ import annotations

from .models import InsuranceUnderwritingStandaloneStore, standalone_model_contract
from .workflows import (
    run_quote_to_bind_workflow,
    run_submission_intake_workflow,
    underwriting_workflow_catalog,
)


PBC_KEY = "insurance_underwriting"
EVENT_CONTRACT = {
    "contract": "AppGen-X",
    "topic": "pbc.insurance_underwriting.events",
    "outbox_table": f"{PBC_KEY}_appgen_outbox_event",
    "inbox_table": f"{PBC_KEY}_appgen_inbox_event",
    "dead_letter_table": f"{PBC_KEY}_appgen_dead_letter_event",
}
OPERATION_CONTRACTS = (
    {
        "operation": "command_underwriting_submission",
        "operation_kind": "command",
        "method": "POST",
        "path": "/underwriting-submissions",
        "permission": "insurance_underwriting.submission.write",
        "owned_tables": ("insurance_underwriting_underwriting_submission",),
        "read_tables": (),
        "emitted_event": "InsuranceUnderwritingCreated",
        "transaction_boundary": "owned_datastore_plus_outbox",
        "event_contract": "AppGen-X",
    },
    {
        "operation": "command_risk_profile",
        "operation_kind": "command",
        "method": "POST",
        "path": "/risk-profiles",
        "permission": "insurance_underwriting.submission.write",
        "owned_tables": ("insurance_underwriting_risk_profile",),
        "read_tables": (),
        "emitted_event": "InsuranceUnderwritingUpdated",
        "transaction_boundary": "owned_datastore_plus_outbox",
        "event_contract": "AppGen-X",
    },
    {
        "operation": "command_rating_factor",
        "operation_kind": "command",
        "method": "POST",
        "path": "/rating-factors",
        "permission": "insurance_underwriting.quote.write",
        "owned_tables": ("insurance_underwriting_rating_factor",),
        "read_tables": (),
        "emitted_event": "InsuranceUnderwritingUpdated",
        "transaction_boundary": "owned_datastore_plus_outbox",
        "event_contract": "AppGen-X",
    },
    {
        "operation": "command_quote",
        "operation_kind": "command",
        "method": "POST",
        "path": "/quotes",
        "permission": "insurance_underwriting.quote.write",
        "owned_tables": ("insurance_underwriting_quote",),
        "read_tables": (),
        "emitted_event": "InsuranceUnderwritingUpdated",
        "transaction_boundary": "owned_datastore_plus_outbox",
        "event_contract": "AppGen-X",
    },
    {
        "operation": "command_underwriting_decision",
        "operation_kind": "command",
        "method": "POST",
        "path": "/underwriting-decisions",
        "permission": "insurance_underwriting.decision.approve",
        "owned_tables": ("insurance_underwriting_underwriting_decision",),
        "read_tables": (),
        "emitted_event": "InsuranceUnderwritingApproved",
        "transaction_boundary": "owned_datastore_plus_outbox",
        "event_contract": "AppGen-X",
    },
    {
        "operation": "query_workbench",
        "operation_kind": "query",
        "method": "GET",
        "path": "/insurance-underwriting-workbench",
        "permission": "insurance_underwriting.read",
        "owned_tables": (),
        "read_tables": (
            "insurance_underwriting_underwriting_submission",
            "insurance_underwriting_quote",
            "insurance_underwriting_underwriting_decision",
            "insurance_underwriting_bind_package",
        ),
        "emitted_event": None,
        "transaction_boundary": "read_only_projection",
        "event_contract": "AppGen-X",
    },
)
STANDALONE_OPERATION_CONTRACTS = (
    {
        "operation": "create_submission",
        "operation_kind": "command",
        "method": "POST",
        "path": "/app/insurance-underwriting/submissions",
        "handler": "create_submission",
        "permission": "insurance_underwriting.submission.write",
        "table": "insurance_underwriting_underwriting_submission",
        "form": "SubmissionIntakeForm",
        "wizard": "UnderwritingIntakeWizard",
    },
    {
        "operation": "build_risk_profile",
        "operation_kind": "command",
        "method": "POST",
        "path": "/app/insurance-underwriting/risk-profiles",
        "handler": "build_risk_profile",
        "permission": "insurance_underwriting.submission.write",
        "table": "insurance_underwriting_risk_profile",
        "form": "RiskProfileForm",
        "wizard": "UnderwritingIntakeWizard",
    },
    {
        "operation": "review_rating_factor",
        "operation_kind": "command",
        "method": "POST",
        "path": "/app/insurance-underwriting/rating-factors",
        "handler": "review_rating_factor",
        "permission": "insurance_underwriting.quote.write",
        "table": "insurance_underwriting_rating_factor",
        "form": "RatingWorksheetForm",
        "wizard": "QuoteApprovalWizard",
    },
    {
        "operation": "generate_quote",
        "operation_kind": "command",
        "method": "POST",
        "path": "/app/insurance-underwriting/quotes",
        "handler": "generate_quote",
        "permission": "insurance_underwriting.quote.write",
        "table": "insurance_underwriting_quote",
        "form": "QuoteScenarioForm",
        "wizard": "QuoteApprovalWizard",
    },
    {
        "operation": "issue_underwriting_decision",
        "operation_kind": "command",
        "method": "POST",
        "path": "/app/insurance-underwriting/decisions",
        "handler": "issue_underwriting_decision",
        "permission": "insurance_underwriting.decision.approve",
        "table": "insurance_underwriting_underwriting_decision",
        "form": "DecisionReviewForm",
        "wizard": "QuoteApprovalWizard",
    },
    {
        "operation": "assemble_bind_package",
        "operation_kind": "command",
        "method": "POST",
        "path": "/app/insurance-underwriting/bind-packages",
        "handler": "assemble_bind_package",
        "permission": "insurance_underwriting.bind.approve",
        "table": "insurance_underwriting_bind_package",
        "form": "BindReadinessForm",
        "wizard": "BindReadinessWizard",
    },
    {
        "operation": "record_exclusion",
        "operation_kind": "command",
        "method": "POST",
        "path": "/app/insurance-underwriting/exclusions",
        "handler": "record_exclusion",
        "permission": "insurance_underwriting.quote.write",
        "table": "insurance_underwriting_exclusion",
        "form": "ExclusionForm",
        "wizard": "QuoteApprovalWizard",
    },
    {
        "operation": "register_rule",
        "operation_kind": "command",
        "method": "POST",
        "path": "/app/insurance-underwriting/rules",
        "handler": "register_rule",
        "permission": "insurance_underwriting.admin",
        "table": "insurance_underwriting_insurance_underwriting_policy_rule",
        "form": "RuleEditorForm",
        "wizard": "GovernanceTuningWizard",
    },
    {
        "operation": "set_parameter",
        "operation_kind": "command",
        "method": "POST",
        "path": "/app/insurance-underwriting/parameters",
        "handler": "set_parameter",
        "permission": "insurance_underwriting.admin",
        "table": "insurance_underwriting_insurance_underwriting_runtime_parameter",
        "form": "ParameterTuningForm",
        "wizard": "GovernanceTuningWizard",
    },
    {
        "operation": "receive_event",
        "operation_kind": "command",
        "method": "POST",
        "path": "/app/insurance-underwriting/events/inbox",
        "handler": "receive_event",
        "permission": "insurance_underwriting.admin",
        "table": "insurance_underwriting_appgen_inbox_event",
        "form": "EventInboxForm",
        "wizard": "AssistantDocumentIntakeWizard",
    },
    {
        "operation": "run_submission_intake_workflow",
        "operation_kind": "command",
        "method": "POST",
        "path": "/app/insurance-underwriting/workflows/intake",
        "handler": "run_submission_intake_workflow",
        "permission": "insurance_underwriting.submission.write",
        "table": "insurance_underwriting_underwriting_submission",
        "form": "SubmissionIntakeForm",
        "wizard": "UnderwritingIntakeWizard",
    },
    {
        "operation": "run_quote_to_bind_workflow",
        "operation_kind": "command",
        "method": "POST",
        "path": "/app/insurance-underwriting/workflows/quote-to-bind",
        "handler": "run_quote_to_bind_workflow",
        "permission": "insurance_underwriting.bind.approve",
        "table": "insurance_underwriting_bind_package",
        "form": "BindReadinessForm",
        "wizard": "BindReadinessWizard",
    },
    {
        "operation": "get_workbench",
        "operation_kind": "query",
        "method": "GET",
        "path": "/app/insurance-underwriting/workbench",
        "handler": "get_workbench",
        "permission": "insurance_underwriting.read",
        "table": "insurance_underwriting_underwriting_submission",
        "form": None,
        "wizard": None,
    },
    {
        "operation": "get_submission_detail",
        "operation_kind": "query",
        "method": "GET",
        "path": "/app/insurance-underwriting/submissions/detail",
        "handler": "get_submission_detail",
        "permission": "insurance_underwriting.read",
        "table": "insurance_underwriting_underwriting_submission",
        "form": None,
        "wizard": None,
    },
    {
        "operation": "get_submission_timeline",
        "operation_kind": "query",
        "method": "GET",
        "path": "/app/insurance-underwriting/timeline",
        "handler": "get_submission_timeline",
        "permission": "insurance_underwriting.read",
        "table": "insurance_underwriting_appgen_outbox_event",
        "form": None,
        "wizard": None,
    },
)


def service_operation_contracts() -> dict:
    commands = tuple(item for item in OPERATION_CONTRACTS if item["operation_kind"] == "command")
    queries = tuple(item for item in OPERATION_CONTRACTS if item["operation_kind"] == "query")
    return {
        "ok": bool(OPERATION_CONTRACTS),
        "pbc": PBC_KEY,
        "contracts": OPERATION_CONTRACTS,
        "command_operations": tuple(item["operation"] for item in commands),
        "query_operations": tuple(item["operation"] for item in queries),
        "operation_contract": OPERATION_CONTRACTS[0],
        "event_contract": EVENT_CONTRACT,
        "side_effects": (),
    }


def service_operation_manifest() -> dict:
    contracts = service_operation_contracts()
    return {
        "ok": contracts["ok"],
        "pbc": PBC_KEY,
        "service_class": "InsuranceUnderwritingService",
        "command_operations": contracts["command_operations"],
        "query_operations": contracts["query_operations"],
        "event_contract": EVENT_CONTRACT,
        "side_effects": (),
    }


def standalone_service_operation_contracts() -> dict:
    return {
        "format": "appgen.insurance-underwriting-standalone-service-contract.v1",
        "ok": True,
        "pbc": PBC_KEY,
        "contracts": STANDALONE_OPERATION_CONTRACTS,
        "command_operations": tuple(
            item["operation"] for item in STANDALONE_OPERATION_CONTRACTS if item["operation_kind"] == "command"
        ),
        "query_operations": tuple(
            item["operation"] for item in STANDALONE_OPERATION_CONTRACTS if item["operation_kind"] == "query"
        ),
        "workflow_catalog": underwriting_workflow_catalog(),
        "side_effects": (),
    }


def operation_plan(operation: str, payload: dict | None = None) -> dict:
    contract = next((item for item in OPERATION_CONTRACTS if item["operation"] == operation), None)
    if contract is None:
        return {"ok": False, "reason": "unknown_operation", "operation": operation, "side_effects": ()}
    return {
        "ok": True,
        "pbc": PBC_KEY,
        "operation": operation,
        "operation_kind": contract["operation_kind"],
        "route": {"method": contract["method"], "path": contract["path"]},
        "permission": contract["permission"],
        "owned_tables": contract["owned_tables"],
        "read_tables": contract["read_tables"],
        "payload_keys": tuple(sorted(dict(payload or {}))),
        "emitted_event": contract["emitted_event"],
        "transaction_boundary": contract["transaction_boundary"],
        "event_contract": contract["event_contract"],
        "side_effects": (),
    }


class InsuranceUnderwritingService:
    """Side-effect-free source package facade used by repo-level audits."""

    def _execute(self, operation: str, payload: dict | None = None) -> dict:
        plan = operation_plan(operation, payload)
        return {
            "ok": plan["ok"],
            "operation": operation,
            "payload": dict(payload or {}),
            "operation_contract": plan,
            "read_only": plan["operation_kind"] == "query",
            "outbox_table": EVENT_CONTRACT["outbox_table"] if plan["operation_kind"] == "command" else None,
            "emits": (plan["emitted_event"],) if plan.get("emitted_event") else (),
            "side_effects": (),
        }

    def command_underwriting_submission(self, payload: dict | None = None) -> dict:
        return self._execute("command_underwriting_submission", payload)

    def command_risk_profile(self, payload: dict | None = None) -> dict:
        return self._execute("command_risk_profile", payload)

    def command_rating_factor(self, payload: dict | None = None) -> dict:
        return self._execute("command_rating_factor", payload)

    def command_quote(self, payload: dict | None = None) -> dict:
        return self._execute("command_quote", payload)

    def command_underwriting_decision(self, payload: dict | None = None) -> dict:
        return self._execute("command_underwriting_decision", payload)

    def query_workbench(self, payload: dict | None = None) -> dict:
        return self._execute("query_workbench", payload)


class InsuranceUnderwritingStandaloneService:
    """Executable service wrapper around the sqlite-backed standalone store."""

    def __init__(self, store: InsuranceUnderwritingStandaloneStore | None = None) -> None:
        self.store = store or InsuranceUnderwritingStandaloneStore()

    def close(self) -> None:
        self.store.close()

    def create_submission(self, payload: dict | None = None) -> dict:
        return self.store.create_submission(dict(payload or {}))

    def build_risk_profile(self, payload: dict | None = None) -> dict:
        return self.store.build_risk_profile(dict(payload or {}))

    def review_rating_factor(self, payload: dict | None = None) -> dict:
        return self.store.review_rating_factor(dict(payload or {}))

    def generate_quote(self, payload: dict | None = None) -> dict:
        return self.store.generate_quote(dict(payload or {}))

    def issue_underwriting_decision(self, payload: dict | None = None) -> dict:
        return self.store.issue_underwriting_decision(dict(payload or {}))

    def assemble_bind_package(self, payload: dict | None = None) -> dict:
        return self.store.assemble_bind_package(dict(payload or {}))

    def record_exclusion(self, payload: dict | None = None) -> dict:
        return self.store.record_exclusion(dict(payload or {}))

    def register_rule(self, payload: dict | None = None) -> dict:
        return self.store.register_rule(dict(payload or {}))

    def set_parameter(self, payload: dict | None = None) -> dict:
        return self.store.set_parameter(dict(payload or {}))

    def receive_event(self, payload: dict | None = None) -> dict:
        return self.store.receive_event(dict(payload or {}))

    def run_submission_intake_workflow(self, payload: dict | None = None) -> dict:
        return run_submission_intake_workflow(self, dict(payload or {}))

    def run_quote_to_bind_workflow(self, payload: dict | None = None) -> dict:
        return run_quote_to_bind_workflow(self, dict(payload or {}))

    def get_workbench(self, payload: dict | None = None) -> dict:
        tenant = dict(payload or {}).get("tenant", "default")
        return {"ok": True, "result": self.store.build_workbench(tenant), "side_effects": ()}

    def get_submission_detail(self, payload: dict | None = None) -> dict:
        submission_id = dict(payload or {}).get("submission_id", "")
        return {"ok": True, "result": self.store.get_submission_detail(submission_id), "side_effects": ()}

    def get_submission_timeline(self, payload: dict | None = None) -> dict:
        submission_id = dict(payload or {}).get("submission_id", "")
        return {"ok": True, "result": self.store.build_timeline(submission_id), "side_effects": ()}


def smoke_test() -> dict:
    manifest = service_operation_manifest()
    service = InsuranceUnderwritingService()
    command = service.command_underwriting_submission({"tenant": "tenant-smoke"})
    query = service.query_workbench({"tenant": "tenant-smoke"})
    standalone = InsuranceUnderwritingStandaloneService()
    try:
        live = standalone.run_submission_intake_workflow(
            {
                "submission_id": "svc-smoke",
                "tenant": "tenant-smoke",
                "product_line": "property",
                "applicant_name": "Service Smoke",
                "jurisdiction": "US-CA",
                "requested_limit": 800000.0,
                "declared_revenue": 2000000.0,
                "effective_date": "2026-06-01",
                "exposure_locations": ("Los Angeles",),
                "documents": ("app.pdf",),
                "prior_losses": (),
            }
        )
        return {
            "ok": manifest["ok"] and command["ok"] and query["ok"] and live["ok"] and standalone_model_contract()["ok"],
            "manifest": manifest,
            "command": command,
            "query": query,
            "standalone": live,
            "side_effects": (),
        }
    finally:
        standalone.close()
