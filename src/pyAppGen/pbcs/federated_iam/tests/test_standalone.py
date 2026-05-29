"""Focused standalone package tests for federated_iam."""

from .. import agent
from .. import permissions
from .. import release_evidence
from .. import routes
from .. import seed_data
from .. import services
from .. import standalone
from .. import ui


def test_standalone_app_bootstrap_and_route_dispatch_are_executable():
    app = standalone.create_standalone_app()
    manifest = standalone.standalone_manifest()
    dispatch = routes.dispatch_route(
        "GET",
        "/iam-workbench",
        {"tenant": "tenant_seed_alpha"},
        granted_permissions=tuple(app["manifest"]["permissions"]),
    )

    assert app["ok"] is True
    assert manifest["ok"] is True
    assert app["seed"]["summary"]["principal_count"] >= 2
    assert app["workbench"]["ok"] is True
    assert dispatch["ok"] is True
    assert dispatch["result"]["result"]["tenant"] == "tenant_seed_alpha"


def test_seeded_service_and_ui_governance_surface_are_consistent():
    service = services.create_seeded_service()
    command = service.execute("set_parameter", {"name": "token_ttl_minutes", "value": 120})
    query = service.execute("build_workbench_view", {"tenant": "tenant_seed_alpha"})
    contract = ui.federated_iam_ui_contract()
    render = ui.federated_iam_render_workbench(
        service.state,
        tenant="tenant_seed_alpha",
        principal_permissions=tuple(permissions.permission_manifest()["permissions"]),
    )

    assert command["ok"] is True
    assert query["ok"] is True
    assert contract["forms"]
    assert contract["wizards"]
    assert contract["controls"]
    assert render["visible_forms"]
    assert render["visible_wizards"]


def test_release_evidence_agent_and_seed_state_cover_standalone_surface():
    seed = seed_data.build_seed_state()
    evidence = release_evidence.build_release_evidence()
    agent_manifest = agent.agent_skill_manifest()

    assert seed["ok"] is True
    assert evidence["ok"] is True
    assert evidence["standalone"]["ok"] is True
    assert evidence["agent"]["ok"] is True
    assert all(item["exists"] for item in evidence["docs"])
    assert agent_manifest["ok"] is True
    assert not any(table.startswith("federated_iam_federated_iam_") for table in agent_manifest["skills"][0]["owned_tables"])
