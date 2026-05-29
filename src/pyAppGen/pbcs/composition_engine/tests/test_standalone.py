"""Standalone app tests for the Composition Engine slice."""

from __future__ import annotations

from ..standalone import CompositionEngineStandaloneApp
from ..standalone import smoke_test
from ..standalone import standalone_app_manifest


def test_standalone_manifest_and_smoke() -> None:
    manifest = standalone_app_manifest()
    smoke = smoke_test()
    assert manifest["ok"] is True
    assert manifest["repository"]["ok"] is True
    assert manifest["forms"]
    assert manifest["wizards"]
    assert manifest["controls"]
    assert smoke["ok"] is True


def test_standalone_app_bootstrap_wizard_and_repository_sync() -> None:
    app = CompositionEngineStandaloneApp(bootstrap=True)
    wizard = app.run_wizard(
        "bootstrap_composition",
        {
            "workspace": {
                "tenant": "tenant_standalone",
                "workspace_id": "ws_standalone",
                "name": "Standalone Customer Console",
                "owner": "ops_user",
                "target": "web",
            },
            "select_pbc": {
                "pbc": "customer_360",
                "mesh": "relationship",
                "reason": "customer-facing composition",
            },
            "register_component": {
                "tenant": "tenant_standalone",
                "component_id": "cmp_standalone",
                "pbc": "customer_360",
                "fragment": "CompositionWorkbench",
                "permissions": ("composition_engine.compose",),
                "schemas": ("CustomerProfile",),
                "fragment_id": "frag_standalone",
                "route": "/customers/standalone",
                "slots": ("main",),
                "events": ("CustomerProfile",),
            },
            "bind_layout": {
                "tenant": "tenant_standalone",
                "binding_id": "bind_standalone",
                "page": "home",
                "slot": "main",
                "fragment_id": "frag_standalone",
                "projection": "customer_profile_projection",
            },
            "validate": {
                "workspace_id": "ws_standalone",
            },
        },
    )
    rendered = app.render_workbench(tenant="tenant_standalone")
    assistant = app.submit_form(
        "assistant_document_intake",
        {
            "document_text": "Compose a governed customer operations workbench.",
            "instructions": "Preview an update to the composition workspace only.",
            "requested_action": "update",
            "target_table": "composition_engine_composition_workspace",
        },
    )
    controls = app.submit_form("control_center_request", {"workspace_id": "ws_standalone"})
    repository_workspace = app.repository.fetch_workspace("ws_standalone")
    repository_summary = app.repository.workspace_summary(tenant="tenant_standalone")

    assert wizard["ok"] is True
    assert wizard["workspace_id"] == "ws_standalone"
    assert rendered["ok"] is True
    assert rendered["shell"]["app_id"] == "composition_engine_one_pbc_app"
    assert rendered["workbench"]["cards"][0]["value"] >= 1
    assert assistant["ok"] is True
    assert assistant["result"]["requires_human_confirmation"] is True
    assert controls["ok"] is True
    assert controls["result"]["assistant_guardrails"]["ok"] is True
    assert repository_workspace is not None
    assert repository_workspace["workspace_id"] == "ws_standalone"
    assert repository_summary["workspace_count"] == 1

    app.close()
