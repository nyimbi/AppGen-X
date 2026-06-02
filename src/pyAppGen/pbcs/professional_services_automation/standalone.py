"""Standalone one-PBC application composition for professional_services_automation."""

from __future__ import annotations

from . import agent
from . import controls
from . import forms
from . import permissions
from . import routes
from . import services
from . import ui
from . import wizards
from .manifest import PBC_MANIFEST
from .runtime import PROFESSIONAL_SERVICES_AUTOMATION_REQUIRED_EVENT_TOPIC
from .runtime import professional_services_automation_build_workbench_view
from .runtime import professional_services_automation_command_client_engagement
from .runtime import professional_services_automation_configure_runtime
from .runtime import professional_services_automation_empty_state
from .runtime import professional_services_automation_parse_document_instruction
from .runtime import professional_services_automation_receive_event
from .runtime import professional_services_automation_register_rule
from .runtime import professional_services_automation_run_advanced_assessment
from .runtime import professional_services_automation_set_parameter
from .runtime import professional_services_automation_verify_owned_table_boundary
from .domain_depth import DOMAIN_OPERATIONS
from .domain_depth import execute_domain_operation


PBC_KEY = "professional_services_automation"
DEFAULT_CONFIGURATION = {
    "database_backend": "postgresql",
    "event_topic": PROFESSIONAL_SERVICES_AUTOMATION_REQUIRED_EVENT_TOPIC,
    "retry_limit": 3,
    "default_policy": "balanced_margin_governance",
    "workbench_limit": 50,
    "confirmation_required_for_mutations": True,
    "tenant_isolation_mode": "strict",
}
DEFAULT_PARAMETERS = {
    "target_utilization_percent": 78,
    "minimum_margin_percent": 28,
    "time_submission_sla_hours": 24,
    "billing_cutoff_days": 3,
    "risk_threshold": 0.62,
    "workbench_limit": 50,
}
DEFAULT_RULES = (
    {
        "rule_id": "psa.staffing_policy",
        "tenant": "tenant_demo",
        "scope": "staffing",
        "status": "active",
        "minimum_skill_matches": 3,
        "max_overallocation_percent": 110,
    },
    {
        "rule_id": "psa.billing_readiness_policy",
        "tenant": "tenant_demo",
        "scope": "billing_readiness",
        "status": "active",
        "required_acceptance": True,
        "required_time_approval": True,
    },
)



def professional_services_automation_standalone_workflow_catalog() -> tuple[dict, ...]:
    """Return executable standalone workflow definitions for this PBC app."""
    return (
        {
            "workflow_id": "bootstrap_psa_app",
            "label": "Bootstrap PSA App",
            "steps": ("configure_runtime", "set_parameter", "register_rule", "create_engagement"),
            "outcome": "runtime_ready",
        },
        {
            "workflow_id": "launch_client_engagement",
            "label": "Launch Client Engagement",
            "steps": ("create_engagement", "register_statement_of_work", "open_staffing_request", "assign_staff"),
            "outcome": "engagement_staffed",
        },
        {
            "workflow_id": "recover_margin_leakage",
            "label": "Recover Margin Leakage",
            "steps": ("capture_time_entry", "run_billing_readiness", "forecast_margin", "simulate_margin_leakage"),
            "outcome": "margin_guardrail_recovered",
        },
        {
            "workflow_id": "triage_delivery_risk",
            "label": "Triage Delivery Risk",
            "steps": ("track_milestone", "score_delivery_risk", "record_client_acceptance", "resolve_engagement_exception"),
            "outcome": "risk_actionable",
        },
    )



def bootstrap_standalone_state() -> dict:
    """Build a deterministic standalone app state using package-local defaults."""
    state = professional_services_automation_empty_state()
    state = professional_services_automation_configure_runtime(state, DEFAULT_CONFIGURATION)["state"]
    for key, value in DEFAULT_PARAMETERS.items():
        state = professional_services_automation_set_parameter(state, key, value)["state"]
    for rule in DEFAULT_RULES:
        state = professional_services_automation_register_rule(state, rule)["state"]
    state = professional_services_automation_command_client_engagement(
        state,
        {
            "tenant": "tenant_demo",
            "code": "ENG-DEMO-001",
            "status": "mobilization",
            "client_name": "Northwind Advisory",
            "engagement_archetype": "fixed_price_implementation",
            "delivery_manager": "manager_demo",
        },
    )["state"]
    state = professional_services_automation_receive_event(
        state,
        {
            "event_type": "ContractApproved",
            "event_id": "evt_contract_demo",
            "payload": {
                "tenant": "tenant_demo",
                "consultant_id": "consultant_demo",
                "contract_id": "contract_demo",
            },
        },
    )["state"]
    state = professional_services_automation_receive_event(
        state,
        {
            "event_type": "InvoiceIssued",
            "event_id": "evt_invoice_demo",
            "payload": {
                "tenant": "tenant_demo",
                "invoice_id": "invoice_demo",
                "engagement_id": "ENG-DEMO-001",
            },
        },
    )["state"]
    return state



def _domain_execution_bundle() -> tuple[dict, ...]:
    return tuple(
        execute_domain_operation(
            operation,
            {"tenant": "tenant_demo", "engagement_id": "ENG-DEMO-001", "requested_by": "standalone_app"},
        )
        for operation in (
            "create_engagement",
            "register_statement_of_work",
            "open_staffing_request",
            "assign_staff",
            "run_billing_readiness",
            "forecast_margin",
            "score_delivery_risk",
            "simulate_margin_leakage",
        )
    )



def _workspace_summary(state: dict) -> dict:
    preview = professional_services_automation_parse_document_instruction(
        "Client requests an additional reporting stream and revised milestone cadence.",
        "Preview change-control and staffing impact for the current engagement.",
    )
    assessment = professional_services_automation_run_advanced_assessment(
        state,
        {"scenario": "billing_readiness_and_margin_review"},
    )
    domain_bundle = _domain_execution_bundle()
    workbench = professional_services_automation_build_workbench_view(state, tenant="tenant_demo")
    return {
        "tenant": "tenant_demo",
        "record_count": len(state.get("records", {})),
        "parameter_count": len(state.get("parameters", {})),
        "rule_count": len(state.get("rules", {})),
        "inbox_count": len(state.get("inbox", ())),
        "outbox_count": len(state.get("outbox", ())),
        "dead_letter_count": len(state.get("dead_letter", ())),
        "workbench": workbench,
        "document_preview": preview,
        "advanced_assessment": assessment,
        "domain_execution_bundle": domain_bundle,
    }



def professional_services_automation_standalone_app_contract() -> dict:
    """Return the standalone one-PBC app composition contract."""
    state = bootstrap_standalone_state()
    summary = _workspace_summary(state)
    return {
        "format": "appgen.professional-services-automation-standalone-app.v1",
        "ok": True,
        "pbc": PBC_KEY,
        "mode": "standalone_one_pbc_app",
        "manifest": PBC_MANIFEST,
        "routes": routes.api_route_contracts(),
        "services": services.service_operation_manifest(),
        "permissions": permissions.permission_manifest(),
        "ui": ui.professional_services_automation_standalone_app_contract(),
        "forms": forms.professional_services_automation_form_catalog(),
        "wizards": wizards.professional_services_automation_wizard_catalog(),
        "controls": controls.professional_services_automation_control_catalog(),
        "agent": agent.composed_agent_contribution(),
        "assistant_preview": agent.document_instruction_plan(
            "Add two-week stabilization support for the finance workstream.",
            "Preview the change-control and governed CRUD impact.",
        ),
        "workflows": professional_services_automation_standalone_workflow_catalog(),
        "bootstrap": summary,
        "boundary": professional_services_automation_verify_owned_table_boundary(
            (
                "professional_services_automation_engagement",
                "professional_services_automation_billing_readiness_check",
                "projection_dependency",
            )
        ),
        "side_effects": (),
    }



def validate_standalone_application() -> dict:
    """Validate standalone app completeness and bootstrap evidence."""
    app = professional_services_automation_standalone_app_contract()
    bootstrap = app["bootstrap"]
    workflow_ids = tuple(item["workflow_id"] for item in app["workflows"])
    required_workflows = (
        "bootstrap_psa_app",
        "launch_client_engagement",
        "recover_margin_leakage",
        "triage_delivery_risk",
    )
    missing_workflows = tuple(workflow for workflow in required_workflows if workflow not in workflow_ids)
    missing_sections = tuple(
        section
        for section in ("routes", "services", "permissions", "ui", "forms", "wizards", "controls", "agent")
        if not app.get(section)
    )
    return {
        "ok": app["ok"]
        and not missing_workflows
        and not missing_sections
        and app["boundary"]["ok"]
        and bootstrap["record_count"] >= 1
        and bootstrap["outbox_count"] >= 1
        and bootstrap["advanced_assessment"]["ok"] is True
        and all(item["ok"] for item in bootstrap["domain_execution_bundle"]),
        "pbc": PBC_KEY,
        "missing_workflows": missing_workflows,
        "missing_sections": missing_sections,
        "app": app,
        "side_effects": (),
    }


class ProfessionalServicesAutomationStandaloneApp:
    """Package-local standalone app that owns the PSA runtime state."""

    def __init__(self, state: dict | None = None):
        self.state = state or bootstrap_standalone_state()

    def bootstrap(self) -> dict:
        self.state = bootstrap_standalone_state()
        return {"ok": True, "pbc": PBC_KEY, "state": self.state, "side_effects": ()}

    def load_demo_workspace(self) -> dict:
        if not self.state.get("records"):
            self.bootstrap()
        summary = _workspace_summary(self.state)
        return {
            "ok": True,
            "pbc": PBC_KEY,
            "summary": summary,
            "rendered": self.render_workbench(tenant=summary["tenant"]),
            "side_effects": (),
        }

    def render_workbench(self, *, tenant: str, principal_permissions: tuple[str, ...] | None = None) -> dict:
        permissions_granted = principal_permissions or tuple(sorted(set(permissions.permission_manifest()["permissions"])))
        return ui.professional_services_automation_render_standalone_app(
            self.state,
            tenant=tenant,
            principal_permissions=permissions_granted,
        )

    def release_snapshot(self) -> dict:
        from . import release_evidence

        return release_evidence.build_release_evidence()



def smoke_test() -> dict:
    """Exercise the standalone app composition contract."""
    validation = validate_standalone_application()
    app = validation["app"]
    return {
        "ok": validation["ok"]
        and app["agent"]["ok"]
        and bool(app["forms"]["forms"])
        and bool(app["wizards"]["wizards"])
        and bool(app["controls"]["controls"])
        and bool(app["bootstrap"]["workbench"]["fragments"]),
        "validation": validation,
        "side_effects": (),
    }
