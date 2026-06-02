"""Standalone one-PBC application surface for workflow_orchestration."""

from __future__ import annotations

from . import routes
from . import ui
from .repository import repository_snapshot
from .runtime import WORKFLOW_ORCHESTRATION_REQUIRED_EVENT_TOPIC
from .services import WorkflowOrchestrationService
from .services import service_operation_manifest


DEFAULT_CONFIGURATION = {
    "database_backend": "postgresql",
    "event_topic": WORKFLOW_ORCHESTRATION_REQUIRED_EVENT_TOPIC,
    "retry_limit": 3,
    "allowed_signal_sources": ("api_gateway_mesh", "schema_registry", "invoice_management"),
    "default_versioning": "semantic",
    "default_timezone": "UTC",
    "workbench_limit": 100,
}
DEFAULT_PARAMETERS = {
    "default_retry_limit": 3,
    "timer_jitter_seconds": 30,
    "sla_breach_threshold": 0.3,
    "compensation_risk_threshold": 0.5,
    "max_parallel_steps": 4,
    "review_sla_hours": 24,
}
DEFAULT_RULE = {
    "rule_id": "workflow_orchestration.release_readiness",
    "tenant": "tenant_demo",
    "scope": "release_gate",
    "trigger": "publish",
    "allowed_signals": ("submit", "approve", "recover"),
    "requires_compensation": True,
    "severity": "blocking",
    "status": "active",
}
DEFAULT_WORKFLOW = {
    "workflow_id": "invoice_recovery",
    "tenant": "tenant_demo",
    "owner_pbc": "invoice_management",
    "version": "1.0.0",
    "states": ("draft", "awaiting_approval", "recovery_in_progress", "completed", "compensating"),
    "transitions": (
        ("draft", "submit", "awaiting_approval"),
        ("awaiting_approval", "recover", "recovery_in_progress"),
        ("recovery_in_progress", "complete", "completed"),
    ),
    "participants": ("invoice_management", "collections_ops", "payment_orchestration"),
}


def standalone_app_manifest() -> dict:
    """Return the executable standalone-app contribution from the package."""
    service_manifest = service_operation_manifest()
    return {
        "ok": True,
        "pbc": "workflow_orchestration",
        "app": ui.workflow_orchestration_standalone_app_contract(),
        "routes": routes.api_route_contracts()["routes"],
        "service": service_manifest,
        "repository": repository_snapshot()["repository"],
        "side_effects": (),
    }


class WorkflowOrchestrationStandaloneApp:
    """Package-local standalone app that owns workflow orchestration state."""

    def __init__(self, state: dict | None = None):
        self.service = WorkflowOrchestrationService(state=state)

    @property
    def state(self) -> dict:
        return self.service.state

    def dispatch(self, method: str, path: str, payload: dict | None = None) -> dict:
        return routes.dispatch_route(method, path, payload, service=self.service)

    def bootstrap(self, *, tenant: str = "tenant_demo") -> dict:
        self.dispatch(
            "PUT",
            "/api/pbc/workflow_orchestration/workflows/configuration",
            {"configuration": DEFAULT_CONFIGURATION},
        )
        for name, value in DEFAULT_PARAMETERS.items():
            self.dispatch(
                "POST",
                "/api/pbc/workflow_orchestration/workflows/parameters",
                {"name": name, "value": value},
            )
        self.dispatch(
            "POST",
            "/api/pbc/workflow_orchestration/workflows/rules",
            {"rule": {**DEFAULT_RULE, "tenant": tenant}},
        )
        self.dispatch(
            "POST",
            "/api/pbc/workflow_orchestration/workflows/definitions",
            {"workflow": {**DEFAULT_WORKFLOW, "tenant": tenant}},
        )
        self.dispatch(
            "POST",
            "/api/pbc/workflow_orchestration/workflows/versions",
            {
                "version": {
                    "version_id": f"invoice_recovery_{tenant}_v1",
                    "tenant": tenant,
                    "workflow_id": DEFAULT_WORKFLOW["workflow_id"],
                    "semantic_version": DEFAULT_WORKFLOW["version"],
                    "status": "published",
                }
            },
        )
        self.dispatch(
            "POST",
            "/api/pbc/workflow_orchestration/workflows/transition-guards",
            {
                "guard": {
                    "guard_id": f"invoice_guard_{tenant}",
                    "tenant": tenant,
                    "workflow_id": DEFAULT_WORKFLOW["workflow_id"],
                    "from_state": "awaiting_approval",
                    "signal": "recover",
                    "expression": "context.amount_due > 0",
                    "status": "active",
                }
            },
        )
        self.dispatch(
            "POST",
            "/api/pbc/workflow_orchestration/workflows/retry-policies",
            {
                "policy": {
                    "policy_id": f"retry_{tenant}",
                    "tenant": tenant,
                    "workflow_id": DEFAULT_WORKFLOW["workflow_id"],
                    "max_attempts": 3,
                    "backoff": "exponential",
                    "status": "active",
                }
            },
        )
        self.dispatch(
            "POST",
            "/api/pbc/workflow_orchestration/workflows/sla-policies",
            {
                "policy": {
                    "policy_id": f"sla_{tenant}",
                    "tenant": tenant,
                    "workflow_id": DEFAULT_WORKFLOW["workflow_id"],
                    "threshold_seconds": 14400,
                    "severity": "blocking",
                    "status": "active",
                }
            },
        )
        self.dispatch(
            "POST",
            "/api/pbc/workflow_orchestration/workflows/escalation-rules",
            {
                "rule": {
                    "escalation_id": f"escalation_{tenant}",
                    "tenant": tenant,
                    "workflow_id": DEFAULT_WORKFLOW["workflow_id"],
                    "trigger": "sla_breach",
                    "target_group": "collections_ops",
                    "status": "active",
                }
            },
        )
        self.dispatch(
            "POST",
            "/api/pbc/workflow_orchestration/workflows/integration-endpoints",
            {
                "endpoint": {
                    "endpoint_id": f"invoice_endpoint_{tenant}",
                    "tenant": tenant,
                    "participant_pbc": "invoice_management",
                    "route": "POST /invoices/recover",
                    "status": "active",
                }
            },
        )
        self.dispatch(
            "POST",
            "/api/pbc/workflow_orchestration/workflows/events/inbox",
            {
                "envelope": {
                    "event_id": f"schema-{tenant}",
                    "event_type": "SchemaAccepted",
                    "payload": {"tenant": tenant, "subject_id": "InvoiceApproved", "version": 1},
                }
            },
        )
        return {"ok": True, "tenant": tenant, "state": self.state, "side_effects": ()}

    def load_demo_workspace(self, *, tenant: str = "tenant_demo") -> dict:
        self.bootstrap(tenant=tenant)
        self.dispatch(
            "POST",
            "/api/pbc/workflow_orchestration/workflows/instances",
            {
                "instance": {
                    "instance_id": f"invoice_recovery_instance_{tenant}",
                    "tenant": tenant,
                    "workflow_id": DEFAULT_WORKFLOW["workflow_id"],
                    "correlation_id": f"invoice-{tenant}",
                    "context": {"invoice_id": f"invoice-{tenant}", "amount_due": 1500, "customer_tier": "priority"},
                }
            },
        )
        self.dispatch(
            "POST",
            "/api/pbc/workflow_orchestration/workflows/event-correlations",
            {
                "correlation": {
                    "correlation_id": f"corr_{tenant}",
                    "tenant": tenant,
                    "instance_id": f"invoice_recovery_instance_{tenant}",
                    "source_event": "InvoiceApproved",
                    "business_key": f"invoice-{tenant}",
                }
            },
        )
        self.dispatch(
            "POST",
            "/api/pbc/workflow_orchestration/workflows/instances/{id}/signals",
            {
                "instance_id": f"invoice_recovery_instance_{tenant}",
                "signal": {
                    "signal": "submit",
                    "source_pbc": "invoice_management",
                    "payload": {"submitted_by": "collections_agent"},
                },
            },
        )
        self.dispatch(
            "POST",
            "/api/pbc/workflow_orchestration/workflows/timers",
            {
                "timer": {
                    "timer_id": f"timer_{tenant}",
                    "tenant": tenant,
                    "instance_id": f"invoice_recovery_instance_{tenant}",
                    "deadline_seconds": 3600,
                    "action": "recover",
                }
            },
        )
        self.dispatch(
            "POST",
            "/api/pbc/workflow_orchestration/workflows/human-task-assignments",
            {
                "assignment": {
                    "assignment_id": f"assignment_{tenant}",
                    "tenant": tenant,
                    "task_id": f"approval_task_{tenant}",
                    "instance_id": f"invoice_recovery_instance_{tenant}",
                    "assignee_group": "collections_ops",
                    "status": "assigned",
                }
            },
        )
        self.dispatch(
            "POST",
            "/api/pbc/workflow_orchestration/workflows/approval-decisions",
            {
                "decision": {
                    "decision_id": f"decision_{tenant}",
                    "tenant": tenant,
                    "task_id": f"approval_task_{tenant}",
                    "decision": "approved",
                    "decided_by": "collections_lead",
                    "status": "final",
                }
            },
        )
        self.dispatch(
            "POST",
            "/api/pbc/workflow_orchestration/workflows/instances/{id}/steps",
            {
                "step": {
                    "step_id": f"step_{tenant}",
                    "tenant": tenant,
                    "instance_id": f"invoice_recovery_instance_{tenant}",
                    "participant_pbc": "invoice_management",
                    "command": "recover_invoice",
                    "status": "completed",
                    "duration_ms": 420,
                }
            },
        )
        self.dispatch(
            "POST",
            "/api/pbc/workflow_orchestration/workflows/instances/{id}/compensations",
            {
                "compensation": {
                    "compensation_id": f"compensation_{tenant}",
                    "tenant": tenant,
                    "instance_id": f"invoice_recovery_instance_{tenant}",
                    "step_id": f"step_{tenant}",
                    "command": "reverse_invoice_recovery",
                    "reason": "participant_timeout",
                }
            },
        )
        self.dispatch(
            "POST",
            "/api/pbc/workflow_orchestration/workflows/exception-cases",
            {
                "case": {
                    "case_id": f"case_{tenant}",
                    "tenant": tenant,
                    "instance_id": f"invoice_recovery_instance_{tenant}",
                    "case_type": "participant_timeout",
                    "severity": "blocking",
                    "status": "open",
                }
            },
        )
        self.dispatch(
            "POST",
            "/api/pbc/workflow_orchestration/workflows/metric-snapshots",
            {
                "snapshot": {
                    "snapshot_id": f"metrics_{tenant}",
                    "tenant": tenant,
                    "workflow_id": DEFAULT_WORKFLOW["workflow_id"],
                    "instance_count": 1,
                    "completed_count": 0,
                    "compensation_count": 1,
                }
            },
        )
        self.dispatch(
            "POST",
            "/api/pbc/workflow_orchestration/workflows/policy-screenings",
            {
                "screening": {
                    "screening_id": f"screening_{tenant}",
                    "tenant": tenant,
                    "workflow_id": DEFAULT_WORKFLOW["workflow_id"],
                    "decision": "clear",
                    "status": "final",
                }
            },
        )
        self.dispatch(
            "POST",
            "/api/pbc/workflow_orchestration/workflows/completion-proofs",
            {
                "proof": {
                    "proof_id": f"proof_{tenant}",
                    "tenant": tenant,
                    "instance_id": f"invoice_recovery_instance_{tenant}",
                    "proof_hash": f"proof-hash-{tenant}",
                    "proof_type": "terminal-state",
                    "status": "sealed",
                }
            },
        )
        self.dispatch(
            "POST",
            "/api/pbc/workflow_orchestration/workflows/audit-entries",
            {
                "action": "load_demo_workspace",
                "entry_payload": {"tenant": tenant, "workflow_id": DEFAULT_WORKFLOW["workflow_id"]},
            },
        )
        self.dispatch(
            "POST",
            "/api/pbc/workflow_orchestration/workflows/governed-model-evidence",
            {
                "evidence": {
                    "evidence_id": f"evidence_{tenant}",
                    "tenant": tenant,
                    "model_id": "workflow_risk_model",
                    "auc": 0.91,
                    "drift_score": 0.04,
                    "status": "monitored",
                }
            },
        )
        self.dispatch(
            "POST",
            "/api/pbc/workflow_orchestration/workflows/instances/{id}/signals",
            {
                "instance_id": f"invoice_recovery_instance_{tenant}",
                "signal": {
                    "signal": "recover",
                    "source_pbc": "collections_ops",
                    "payload": {"approved_by": "collections_lead"},
                },
            },
        )
        self.service.complete_workflow({"instance_id": f"invoice_recovery_instance_{tenant}"})
        return {
            "ok": True,
            "tenant": tenant,
            "workbench": self.render_workbench(tenant=tenant),
            "repository": repository_snapshot(self.state, tenant=tenant),
            "side_effects": (),
        }

    def render_workbench(self, *, tenant: str, principal_permissions: tuple[str, ...] | None = None) -> dict:
        permissions = principal_permissions or tuple(sorted(set(ui.workflow_orchestration_ui_contract()["action_permissions"].values())))
        return ui.workflow_orchestration_render_standalone_app(self.state, tenant=tenant, principal_permissions=permissions)

    def release_snapshot(self) -> dict:
        from . import release_evidence

        return release_evidence.build_release_evidence()


def smoke_test() -> dict:
    """Exercise the standalone app surface end-to-end."""
    app = WorkflowOrchestrationStandaloneApp()
    loaded = app.load_demo_workspace()
    rendered = app.render_workbench(tenant="tenant_demo")
    release_snapshot = app.release_snapshot()
    return {
        "ok": loaded["ok"]
        and rendered["ok"]
        and rendered["workbench"]["cards"][0]["value"] >= 1
        and release_snapshot["ok"],
        "manifest": standalone_app_manifest(),
        "loaded": loaded,
        "rendered": rendered,
        "release_snapshot": release_snapshot,
        "side_effects": (),
    }


def workbench_smoke_test() -> dict:
    """Exercise bootstrap, route dispatch, and rendering without release recursion."""
    app = WorkflowOrchestrationStandaloneApp()
    loaded = app.load_demo_workspace()
    rendered = app.render_workbench(tenant="tenant_demo")
    return {
        "ok": loaded["ok"] and rendered["ok"] and rendered["workbench"]["cards"][0]["value"] >= 1,
        "manifest": standalone_app_manifest(),
        "loaded": loaded,
        "rendered": rendered,
        "side_effects": (),
    }
