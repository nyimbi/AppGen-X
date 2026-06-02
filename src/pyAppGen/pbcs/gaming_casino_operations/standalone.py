"""Standalone one-PBC app surface for gaming_casino_operations."""

from __future__ import annotations

from typing import Any

from . import agent, models, release_evidence, routes, services, ui


class GamingCasinoOperationsStandaloneApplication:
    """Minimal one-PBC application shell for local execution and tests."""

    def __init__(self, state: dict[str, Any] | None = None):
        self.service = services.GamingCasinoOperationsStandaloneService(state)

    def dispatch(self, method: str, path: str, payload: dict[str, Any] | None = None) -> dict[str, Any]:
        return routes.dispatch_standalone_route(method, path, payload, service=self.service)

    def contract(self) -> dict[str, Any]:
        return gaming_casino_operations_standalone_app_contract()


def gaming_casino_operations_standalone_app_contract() -> dict[str, Any]:
    model_contract = models.standalone_model_contract()
    service_contract = services.standalone_service_operation_contracts()
    route_contract = routes.standalone_route_contracts()
    ui_contract = ui.gaming_casino_operations_standalone_workbench_blueprint()
    agent_contract = agent.standalone_agent_workspace_contract()
    return {
        "format": "appgen.gaming-casino-operations-standalone-app.v1",
        "ok": all(item.get("ok") is True for item in (model_contract, service_contract, route_contract, ui_contract, agent_contract)),
        "pbc": "gaming_casino_operations",
        "models": model_contract,
        "services": service_contract,
        "routes": route_contract,
        "ui": ui_contract,
        "agent": agent_contract,
        "side_effects": (),
    }


def gaming_casino_operations_bootstrap_standalone_app() -> dict[str, Any]:
    app = GamingCasinoOperationsStandaloneApplication()
    return {
        "ok": True,
        "pbc": "gaming_casino_operations",
        "app": app,
        "service": app.service,
        "contract": gaming_casino_operations_standalone_app_contract(),
        "side_effects": (),
    }


def gaming_casino_operations_standalone_app_smoke() -> dict[str, Any]:
    bundle = gaming_casino_operations_bootstrap_standalone_app()
    app = bundle["app"]
    service = bundle["service"]
    service.register_defaults()
    player = app.dispatch(
        "POST",
        "/app/gaming-casino-operations/player-profiles",
        {
            "tenant": "tenant-standalone",
            "player_number": "P-APP-01",
            "legal_name": "Standalone Patron",
            "date_of_birth": "1986-06-01",
            "identity_confidence": 0.99,
            "age_verified": True,
        },
    )
    table = app.dispatch(
        "POST",
        "/app/gaming-casino-operations/table-games",
        {
            "tenant": "tenant-standalone",
            "table_number": "BJ-77",
            "pit": "vip",
            "opening_bankroll": 30000.0,
            "dealer_id": "dealer-standalone",
            "supervisor_id": "supervisor-standalone",
        },
    )
    session = app.dispatch(
        "POST",
        "/app/gaming-casino-operations/wager-sessions",
        {
            "tenant": "tenant-standalone",
            "player_profile_id": player["result"]["record"]["id"],
            "asset_kind": "table",
            "asset_id": table["result"]["record"]["id"],
        },
    )
    payout = app.dispatch(
        "POST",
        "/app/gaming-casino-operations/payouts",
        {
            "tenant": "tenant-standalone",
            "source_id": session["result"]["record"]["id"],
            "amount": 1250.0,
            "approved_by": "supervisor-standalone",
            "witness_id": "witness-standalone",
        },
    )
    workbench = app.dispatch(
        "GET",
        "/app/gaming-casino-operations/workbench",
        {"tenant": "tenant-standalone"},
    )
    rendered = ui.gaming_casino_operations_render_standalone_workbench(workbench["result"])
    evidence = release_evidence.build_release_evidence()
    return {
        "ok": bundle["contract"]["ok"] and player["ok"] and table["ok"] and session["ok"] and payout["ok"] and workbench["ok"] and rendered["ok"] and evidence["ok"],
        "contract": bundle["contract"],
        "player": player,
        "table": table,
        "session": session,
        "payout": payout,
        "workbench": workbench,
        "rendered": rendered,
        "evidence": evidence,
        "side_effects": (),
    }
