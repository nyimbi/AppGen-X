"""Standalone app smoke tests for workflow_orchestration."""

from __future__ import annotations

from pathlib import Path

from .. import agent, release_evidence, routes, services, standalone, ui


PACKAGE_DIR = Path(__file__).resolve().parent.parent


def test_standalone_manifest_and_smoke():
    contract = ui.workflow_orchestration_standalone_app_contract()
    app_smoke = standalone.smoke_test()
    assert contract["ok"] is True
    assert app_smoke["ok"] is True
    assert contract["forms"]
    assert contract["wizards"]
    assert contract["controls"]



def test_standalone_app_can_bootstrap_and_render():
    app = standalone.WorkflowOrchestrationStandaloneApp()
    app.load_demo_workspace(tenant="tenant_standalone")
    rendered = app.render_workbench(tenant="tenant_standalone")
    assert rendered["ok"] is True
    assert rendered["workbench"]["cards"][0]["value"] >= 1
    assert rendered["shell"]["app_id"] == "workflow_orchestration_one_pbc_app"
    assert rendered["workbench"]["repository"]["non_empty_tables"]



def test_standalone_service_routes_ui_agent_and_release_surface():
    service = services.WorkflowOrchestrationService()
    try:
        configured = routes.dispatch_route(
            "PUT",
            "/api/pbc/workflow_orchestration/workflows/configuration",
            {
                "configuration": {
                    "database_backend": "postgresql",
                    "event_topic": "appgen.workflow.events",
                    "retry_limit": 3,
                    "allowed_signal_sources": ("invoice_management",),
                    "default_versioning": "semantic",
                    "default_timezone": "UTC",
                    "workbench_limit": 100,
                }
            },
            service=service,
        )
        workbench = routes.dispatch_route(
            "GET",
            "/api/pbc/workflow_orchestration/workflows/workbench",
            {"tenant": "tenant_demo"},
            service=service,
        )
        rendered = ui.workflow_orchestration_render_standalone_app(
            service.state,
            tenant="tenant_demo",
            principal_permissions=tuple(sorted(set(ui.workflow_orchestration_ui_contract()["action_permissions"].values()))),
        )
        document_plan = agent.document_instruction_plan(
            "workflow invoice_recovery",
            "create an approval workflow with 4 hours timer and compensation",
        )
        crud_plan = agent.datastore_crud_plan(
            "create",
            "workflow_orchestration_workflow_definition",
            {"workflow_id": "invoice_recovery"},
        )
        app_contract = standalone.standalone_app_manifest()
        evidence = release_evidence.build_release_evidence()
        assert configured["ok"] is True
        assert workbench["ok"] is True
        assert rendered["ok"] is True
        assert app_contract["ok"] is True
        assert document_plan["wizard_candidates"]
        assert crud_plan["route_candidates"]
        assert evidence["repository"]["ok"] is True
        assert evidence["standalone_smoke"]["ok"] is True
    finally:
        pass



def test_package_local_docs_exist_for_release_evidence():
    for name in ("README.md", "implementation-plan.md", "implementation-status.md", "RELEASE_EVIDENCE.md"):
        assert (PACKAGE_DIR / name).exists() is True
