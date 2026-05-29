from pyAppGen.pbcs.customer_success_management.slice_app import (
    BUSINESS_TABLES,
    EVENT_TABLES,
    build_release_evidence,
    build_standalone_app,
    dispatch_route,
    pbc_generation_smoke_audit,
    pbc_implementation_release_audit,
    pbc_source_artifact_contract,
    slice_app_smoke_test,
    verify_owned_table_boundary,
)


def test_slice_app_bootstraps_owned_tables_and_creates_account_flow():
    app = build_standalone_app()
    result = app.create_success_account(
        {
            "tenant": "tenant-a",
            "code": "CS-001",
            "customer_name": "Acme Corp",
            "segment": "enterprise",
            "lifecycle_stage": "onboarding",
            "owner": "csm-acme",
            "renewal_date": "2026-12-01",
        }
    )
    assert result["ok"] is True
    workbench = app.query_workbench("tenant-a")
    assert workbench["summary"]["account_count"] == 1
    assert result["success_plan"]["success_account_id"] == result["record"]["id"]
    assert result["onboarding_milestone"]["success_account_id"] == result["record"]["id"]
    assert result["touchpoint"]["success_account_id"] == result["record"]["id"]
    assert workbench["summary"]["touchpoint_count"] == 1


def test_health_playbook_route_and_events_flow_is_executable():
    app = build_standalone_app()
    account = app.create_success_account(
        {
            "tenant": "tenant-b",
            "code": "CS-002",
            "customer_name": "Globex",
            "segment": "mid-market",
            "lifecycle_stage": "active",
            "owner": "csm-globex",
            "renewal_date": "2026-10-15",
        }
    )
    health = app.calculate_health_score(
        {
            "tenant": "tenant-b",
            "success_account_id": account["record"]["id"],
            "adoption": 0.9,
            "support": 0.7,
            "billing": 0.8,
            "engagement": 0.85,
            "value": 0.75,
            "renewal": 0.8,
        }
    )
    touchpoint = dispatch_route(
        "POST",
        "/touchpoints",
        {
            "tenant": "tenant-b",
            "success_account_id": account["record"]["id"],
            "owner": "csm-globex",
            "channel": "email",
            "purpose": "health_follow_up",
            "outcome": "response_pending",
        },
        app=app,
    )
    playbook = app.launch_playbook(
        {"tenant": "tenant-b", "success_account_id": account["record"]["id"], "owner": "csm-globex"}
    )
    route = dispatch_route(
        "GET",
        "/customer-success-workbench",
        {"tenant": "tenant-b"},
        app=app,
    )
    assert health["ok"] is True
    assert touchpoint["ok"] is True
    assert playbook["ok"] is True
    assert route["ok"] is True
    assert len(health["components"]) == 6
    assert playbook["tasks"]
    assert route["result"]["summary"]["touchpoint_count"] >= 2


def test_event_idempotency_and_boundary_enforcement_hold():
    app = build_standalone_app()
    account = app.create_success_account(
        {
            "tenant": "tenant-c",
            "code": "CS-003",
            "customer_name": "Initech",
            "segment": "enterprise",
            "lifecycle_stage": "active",
            "owner": "csm-initech",
            "renewal_date": "2026-09-30",
        }
    )
    handled = app.receive_event(
        {
            "event_type": "PaymentFailed",
            "tenant": "tenant-c",
            "success_account_id": account["record"]["id"],
            "idempotency_key": "evt-1",
        }
    )
    duplicate = app.receive_event(
        {
            "event_type": "PaymentFailed",
            "tenant": "tenant-c",
            "success_account_id": account["record"]["id"],
            "idempotency_key": "evt-1",
        }
    )
    unknown = app.receive_event({"event_type": "UnexpectedEvent", "tenant": "tenant-c", "idempotency_key": "evt-2"})
    assert handled["ok"] is True
    assert duplicate["duplicate"] is True
    assert unknown["ok"] is False
    assert verify_owned_table_boundary(BUSINESS_TABLES + EVENT_TABLES)["ok"] is True
    assert verify_owned_table_boundary(("foreign_table",))["ok"] is False


def test_release_audits_and_smoke_bundle_pass():
    assert slice_app_smoke_test()["ok"] is True
    assert pbc_source_artifact_contract()["ok"] is True
    assert pbc_implementation_release_audit()["ok"] is True
    assert pbc_generation_smoke_audit()["ok"] is True
    evidence = build_release_evidence()
    assert evidence["ok"] is True
    assert {check["id"] for check in evidence["checks"]} >= {
        "pbc_source_artifact_contract",
        "pbc_implementation_release_audit",
        "pbc_generation_smoke_audit",
    }
