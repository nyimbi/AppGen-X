"""Standalone one-PBC application surface for the policy_administration_insurance package."""

from __future__ import annotations

from copy import deepcopy
from typing import Any

from . import agent
from . import runtime
from . import ui
from .domain_depth import execute_domain_operation

DEFAULT_CONFIGURATION = {
    "database_backend": "postgresql",
    "event_topic": runtime.POLICY_ADMINISTRATION_INSURANCE_REQUIRED_EVENT_TOPIC,
    "retry_limit": 3,
    "default_policy_status": "draft",
    "workbench_limit": 50,
}
DEFAULT_PARAMETERS = {
    "quality_score_floor": 0.82,
    "materiality_threshold": 1000,
    "approval_sla_hours": 24,
    "risk_threshold": 0.65,
    "forecast_horizon_days": 30,
    "workbench_limit": 50,
}
DEFAULT_RULES = (
    {
        "rule_id": "policy.issue.readiness",
        "scope": "issuance",
        "status": "active",
        "required_documents": (
            "declarations",
            "required_forms",
            "billing_projection",
        ),
    },
    {
        "rule_id": "policy.cancellation.notice",
        "scope": "cancellation",
        "status": "active",
        "requires_notice_deadline": True,
        "requires_billing_projection": True,
    },
)
STANDALONE_SERVICE_METHODS = (
    {
        "method": "configure",
        "operation_kind": "command",
        "operation": "configure_runtime",
        "table": "policy_administration_insurance_policy_administration_insurance_runtime_parameter",
        "wizard": None,
    },
    {
        "method": "register_defaults",
        "operation_kind": "command",
        "operation": "set_parameter",
        "table": "policy_administration_insurance_policy_administration_insurance_runtime_parameter",
        "wizard": None,
    },
    {
        "method": "create_policy",
        "operation_kind": "command",
        "operation": "command_insurance_policy",
        "table": "policy_administration_insurance_insurance_policy",
        "wizard": "PolicyIssuanceWizard",
    },
    {
        "method": "run_domain_operation",
        "operation_kind": "command",
        "operation": "record_coverage_item",
        "table": "policy_administration_insurance_coverage_item",
        "wizard": "MidTermEndorsementWizard",
    },
    {
        "method": "receive_event",
        "operation_kind": "command",
        "operation": "receive_event",
        "table": "policy_administration_insurance_appgen_inbox_event",
        "wizard": "PolicyDocumentAssemblyWizard",
    },
    {
        "method": "document_intake_plan",
        "operation_kind": "query",
        "operation": "parse_document_instruction",
        "table": "policy_administration_insurance_policy_document",
        "wizard": "PolicyDocumentAssemblyWizard",
    },
    {
        "method": "datastore_crud_plan",
        "operation_kind": "query",
        "operation": "query_workbench",
        "table": "policy_administration_insurance_insurance_policy",
        "wizard": "PolicyIssuanceWizard",
    },
    {
        "method": "workbench_summary",
        "operation_kind": "query",
        "operation": "build_workbench_view",
        "table": "policy_administration_insurance_insurance_policy",
        "wizard": None,
    },
    {
        "method": "render_workbench",
        "operation_kind": "query",
        "operation": "query_workbench",
        "table": "policy_administration_insurance_insurance_policy",
        "wizard": None,
    },
    {
        "method": "release_snapshot",
        "operation_kind": "query",
        "operation": "build_release_evidence",
        "table": "policy_administration_insurance_policy_administration_insurance_control_assertion",
        "wizard": None,
    },
)


def _clone(value: Any) -> Any:
    return deepcopy(value)


class PolicyAdministrationInsuranceStandaloneApplication:
    """Package-local standalone harness over the existing runtime contract."""

    def __init__(self, *, tenant: str = "default") -> None:
        self.tenant = tenant
        self.state = runtime.policy_administration_insurance_empty_state()
        self.domain_operations: list[dict[str, Any]] = []
        self.document_plans: list[dict[str, Any]] = []

    def configure(self, config: dict[str, Any] | None = None) -> dict[str, Any]:
        payload = dict(DEFAULT_CONFIGURATION)
        payload.update(dict(config or {}))
        result = runtime.policy_administration_insurance_configure_runtime(self.state, payload)
        self.state = result["state"]
        return result

    def register_defaults(
        self,
        *,
        parameters: dict[str, Any] | None = None,
        rules: tuple[dict[str, Any], ...] | None = None,
    ) -> dict[str, Any]:
        active_parameters = dict(DEFAULT_PARAMETERS)
        active_parameters.update(dict(parameters or {}))
        active_rules = tuple(rules or DEFAULT_RULES)
        results = []
        for name, value in active_parameters.items():
            result = runtime.policy_administration_insurance_set_parameter(self.state, name, value)
            self.state = result["state"]
            results.append(result)
        for rule in active_rules:
            result = runtime.policy_administration_insurance_register_rule(self.state, rule)
            self.state = result["state"]
            results.append(result)
        return {
            "ok": all(item["ok"] for item in results),
            "results": tuple(results),
            "side_effects": (),
        }

    def create_policy(self, payload: dict[str, Any] | None = None) -> dict[str, Any]:
        policy_payload = {
            "tenant": self.tenant,
            "code": "POLICY-STANDALONE-001",
            "status": "issued",
        }
        policy_payload.update(dict(payload or {}))
        result = runtime.policy_administration_insurance_command_insurance_policy(self.state, policy_payload)
        self.state = result["state"]
        return result

    def receive_event(self, event: dict[str, Any] | None = None) -> dict[str, Any]:
        candidate = {
            "event_type": runtime.POLICY_ADMINISTRATION_INSURANCE_CONSUMED_EVENT_TYPES[0],
            "idempotency_key": "standalone-event-1",
        }
        candidate.update(dict(event or {}))
        result = runtime.policy_administration_insurance_receive_event(self.state, candidate)
        self.state = result["state"]
        return result

    def run_domain_operation(self, operation: str, payload: dict[str, Any] | None = None) -> dict[str, Any]:
        candidate = {"tenant": self.tenant}
        candidate.update(dict(payload or {}))
        result = execute_domain_operation(operation, candidate)
        if result["ok"]:
            self.domain_operations.append(_clone(result))
        return result

    def document_intake_plan(self, document=None, instruction=None) -> dict[str, Any]:
        runtime_plan = runtime.policy_administration_insurance_parse_document_instruction(
            document or "policy packet",
            instruction or "prepare issuance review",
        )
        agent_plan = agent.document_instruction_plan(document, instruction)
        result = {
            "ok": runtime_plan["ok"] and agent_plan["ok"],
            "pbc": runtime.PBC_KEY,
            "runtime_plan": runtime_plan,
            "agent_plan": agent_plan,
            "wizard_candidates": agent_plan["wizard_candidates"],
            "form_candidates": agent_plan["form_candidates"],
            "side_effects": (),
        }
        self.document_plans.append(_clone(result))
        return result

    def datastore_crud_plan(
        self,
        action: str = "read",
        table: str | None = None,
        payload: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        return agent.datastore_crud_plan(action, table=table, payload=payload)

    def workbench_summary(self, *, tenant: str | None = None) -> dict[str, Any]:
        active_tenant = tenant or self.tenant
        query = runtime.policy_administration_insurance_query_workbench(self.state, {"tenant": active_tenant})
        view = runtime.policy_administration_insurance_build_workbench_view(active_tenant)
        return {
            "ok": query["ok"] and view["ok"],
            "tenant": active_tenant,
            "policy_count": len(query["records"]),
            "domain_operation_count": len(self.domain_operations),
            "document_plan_count": len(self.document_plans),
            "outbox_count": len(self.state.get("outbox", ())),
            "inbox_count": len(self.state.get("inbox", ())),
            "dead_letter_count": len(self.state.get("dead_letter", ())),
            "view": view,
            "records": query["records"],
            "side_effects": (),
        }

    def render_workbench(self, *, tenant: str | None = None) -> dict[str, Any]:
        summary = self.workbench_summary(tenant=tenant)
        rendered = ui.policy_administration_insurance_render_standalone_workbench(summary)
        return {
            "ok": summary["ok"] and rendered["ok"],
            "summary": summary,
            "rendered": rendered,
            "side_effects": (),
        }

    def release_snapshot(self) -> dict[str, Any]:
        from .release_evidence import build_release_evidence

        return build_release_evidence()


def policy_administration_insurance_standalone_app_contract() -> dict[str, Any]:
    workspace = agent.standalone_agent_workspace_contract()
    standalone_ui = ui.policy_administration_insurance_standalone_workbench_blueprint()
    runtime_smoke = runtime.policy_administration_insurance_runtime_smoke()
    return {
        "format": "appgen.policy-administration-insurance-standalone-app.v1",
        "ok": workspace["ok"] and standalone_ui["ok"] and runtime_smoke["ok"],
        "pbc": "policy_administration_insurance",
        "app_class": "PolicyAdministrationInsuranceStandaloneApplication",
        "implementation_directory": "src/pyAppGen/pbcs/policy_administration_insurance",
        "service_methods": STANDALONE_SERVICE_METHODS,
        "ui": standalone_ui,
        "agent": workspace,
        "runtime_smoke": runtime_smoke,
        "side_effects": (),
    }


def bootstrap_policy_administration_insurance_standalone_app(
    *, tenant: str = "default"
) -> dict[str, Any]:
    app = PolicyAdministrationInsuranceStandaloneApplication(tenant=tenant)
    configured = app.configure()
    defaults = app.register_defaults()
    return {
        "ok": configured["ok"] and defaults["ok"],
        "pbc": "policy_administration_insurance",
        "application": app,
        "configured": configured,
        "defaults": defaults,
        "contract": policy_administration_insurance_standalone_app_contract(),
        "side_effects": (),
    }


def policy_administration_insurance_standalone_smoke() -> dict[str, Any]:
    bundle = bootstrap_policy_administration_insurance_standalone_app(tenant="tenant-standalone")
    app = bundle["application"]
    created = app.create_policy(
        {
            "code": "POLICY-001",
            "product_code": "COMMERCIAL_AUTO",
            "insured_name": "M. Insurance Ltd",
        }
    )
    coverage = app.run_domain_operation(
        "record_coverage_item",
        {"policy_id": "POLICY-001", "coverage_type": "liability"},
    )
    endorsement = app.run_domain_operation(
        "review_endorsement",
        {"policy_id": "POLICY-001", "change_type": "vehicle_add"},
    )
    received = app.receive_event({"idempotency_key": "standalone-policy-changed"})
    document = app.document_intake_plan(
        "renewal packet",
        "prepare renewal notice and supporting documents",
    )
    crud = app.datastore_crud_plan(
        "create",
        "policy_administration_insurance_policy_document",
        {"policy_document_id": "DOC-001"},
    )
    workbench = app.workbench_summary()
    rendered = app.render_workbench()
    release = app.release_snapshot()
    return {
        "ok": bundle["ok"]
        and created["ok"]
        and coverage["ok"]
        and endorsement["ok"]
        and received["ok"]
        and document["ok"]
        and crud["ok"]
        and workbench["ok"]
        and rendered["ok"]
        and release["ok"],
        "bundle": {key: value for key, value in bundle.items() if key != "application"},
        "created": created,
        "coverage": coverage,
        "endorsement": endorsement,
        "received": received,
        "document": document,
        "crud": crud,
        "workbench": workbench,
        "rendered": rendered,
        "release": release,
        "side_effects": (),
    }
