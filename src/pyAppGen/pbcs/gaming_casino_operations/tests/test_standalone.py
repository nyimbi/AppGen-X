"""Focused standalone tests for gaming_casino_operations."""

from pathlib import Path

from .. import agent, release_evidence, routes, services, standalone, ui


def test_duplicate_patron_review_and_table_close_controls():
    service = services.GamingCasinoOperationsStandaloneService()
    service.register_defaults()
    first = service.create_player_profile(
        {
            "tenant": "tenant-test",
            "player_number": "P-100",
            "legal_name": "Ada Patron",
            "date_of_birth": "1990-01-01",
            "government_id": "ID-100",
            "identity_confidence": 0.98,
            "age_verified": True,
        }
    )
    duplicate = service.create_player_profile(
        {
            "tenant": "tenant-test",
            "player_number": "P-101",
            "legal_name": "Ada Patron",
            "date_of_birth": "1990-01-01",
            "government_id": "ID-100",
            "identity_confidence": 0.98,
            "age_verified": True,
        }
    )
    table = service.handle_table_game(
        {
            "tenant": "tenant-test",
            "table_number": "BJ-10",
            "opening_bankroll": 15000.0,
            "dealer_id": "dealer-1",
            "supervisor_id": "sup-1",
        }
    )
    blocked_close = service.handle_table_game({"action": "close", "table_id": table["record"]["id"], "closing_bankroll": 15000.0})
    allowed_close = service.handle_table_game(
        {
            "action": "close",
            "table_id": table["record"]["id"],
            "closing_bankroll": 15000.0,
            "supervisor_signed": True,
            "reconciliation_complete": True,
        }
    )
    assert first["ok"] is True
    assert duplicate["review_required"] is True
    assert duplicate["duplicate_candidates"] == (first["record"]["id"],)
    assert blocked_close["ok"] is False
    assert allowed_close["ok"] is True


def test_slot_session_payout_and_responsible_gaming_flow():
    service = services.GamingCasinoOperationsStandaloneService()
    service.register_defaults()
    player = service.create_player_profile(
        {
            "tenant": "tenant-flow",
            "player_number": "P-200",
            "legal_name": "Risk Patron",
            "date_of_birth": "1985-04-04",
            "identity_confidence": 0.99,
            "age_verified": True,
        }
    )
    slot = service.handle_slot_machine(
        {
            "tenant": "tenant-flow",
            "asset_code": "SL-200",
            "bank_location": "bank-b",
            "denomination": 2.0,
            "paytable_version": "v2",
        }
    )
    session = service.handle_wager_session(
        {
            "tenant": "tenant-flow",
            "player_profile_id": player["record"]["id"],
            "asset_kind": "slot",
            "asset_id": slot["record"]["id"],
        }
    )
    payout = service.handle_payout(
        {
            "tenant": "tenant-flow",
            "source_id": session["record"]["id"],
            "amount": 2500.0,
        }
    )
    approved = service.handle_payout(
        {
            "action": "approve",
            "payout_id": payout["record"]["id"],
            "approved_by": "sup-200",
            "witness_id": "wit-200",
        }
    )
    rg_case = service.open_responsible_gaming_case(
        {
            "tenant": "tenant-flow",
            "player_profile_id": player["record"]["id"],
            "owner_id": "rg-1",
            "cooling_off_hours": 96,
        }
    )
    assert slot["ok"] is True
    assert session["ok"] is True
    assert payout["approval_required"] is True
    assert approved["ok"] is True
    assert rg_case["ok"] is True
    assert service.snapshot()["player_profiles"][player["record"]["id"]]["restriction_state"] == "cooling_off"


def test_standalone_routes_ui_agent_and_release_surface():
    service = services.GamingCasinoOperationsStandaloneService()
    service.register_defaults()
    create = routes.dispatch_standalone_route(
        "POST",
        "/app/gaming-casino-operations/player-profiles",
        {
            "tenant": "tenant-route",
            "player_number": "P-ROUTE",
            "legal_name": "Route Patron",
            "date_of_birth": "1988-08-08",
            "identity_confidence": 0.96,
            "age_verified": True,
        },
        service=service,
    )
    workbench = routes.dispatch_standalone_route(
        "GET",
        "/app/gaming-casino-operations/workbench",
        {"tenant": "tenant-route"},
        service=service,
    )
    rendered = ui.gaming_casino_operations_render_standalone_workbench(workbench["result"])
    document_plan = agent.document_instruction_plan("jackpot note", "approve handpay for player")
    crud_plan = agent.datastore_crud_plan("create", "gaming_casino_operations_player_profile", {"player_number": "P-ROUTE"})
    smoke = standalone.gaming_casino_operations_standalone_app_smoke()
    evidence = release_evidence.build_release_evidence()
    assert create["ok"] is True
    assert workbench["ok"] is True
    assert rendered["ok"] is True
    assert document_plan["wizard_candidates"]
    assert crud_plan["route_candidates"]
    assert smoke["ok"] is True
    assert evidence["documentation"]["ok"] is True
    assert evidence["standalone_app"]["ok"] is True


def test_package_docs_exist():
    base = Path(__file__).resolve().parent.parent
    for name in ("README.md", "implementation-plan.md", "implementation-status.md", "RELEASE_EVIDENCE.md"):
        assert (base / name).exists() is True
