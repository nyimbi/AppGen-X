"""Repository-backed standalone app tests for dom."""

from __future__ import annotations

from .. import release_evidence, seed_data, standalone, ui


ALL_PERMISSIONS = tuple(ui.dom_ui_contract()["binding_evidence"]["rbac_permissions"])


def _order_bundle(seed_bundle: dict, order_id: str) -> dict:
    return next(item for item in seed_bundle["orders"] if item["order"]["order_id"] == order_id)


def test_standalone_manifest_and_release_snapshot_are_database_backed():
    manifest = standalone.standalone_manifest()
    snapshot = standalone.standalone_release_snapshot()

    assert manifest["ok"] is True
    assert manifest["database_backed_ui"] is True
    assert manifest["repository_class"] == "DomStandaloneRepository"
    assert snapshot["ok"] is True
    assert snapshot["repository"]["dashboard"]["counts"]["orders"] >= 2
    assert len(snapshot["read_models"]["orders"]) >= 2
    assert snapshot["workbench"]["forms"]
    assert snapshot["workbench"]["wizards"]
    assert snapshot["workbench"]["controls"]


def test_load_demo_workspace_persists_state_and_read_models(tmp_path):
    seed_bundle = seed_data.standalone_seed_bundle()
    database_path = tmp_path / "dom-standalone.sqlite3"
    app = standalone.DomStandaloneApplication(tenant=seed_bundle["tenant"], database_path=str(database_path))
    try:
        loaded = app.load_demo_workspace(seed_bundle=seed_bundle)
        repository_manifest = app.repository_manifest()
        read_models = app.read_model_snapshot()

        assert loaded["ok"] is True
        assert repository_manifest["dashboard"]["counts"]["forms"] >= 3
        assert repository_manifest["dashboard"]["counts"]["workflows"] >= 2
        assert repository_manifest["dashboard"]["counts"]["controls"] >= 2
        assert read_models["orders"]
        assert any(item["status"] == "shipped" for item in read_models["orders"])
    finally:
        app.close()

    reopened = standalone.DomStandaloneApplication(tenant=seed_bundle["tenant"], database_path=str(database_path))
    try:
        snapshot = reopened.snapshot()
        read_models = reopened.read_model_snapshot()

        assert snapshot["orders"]["order_100"]["status"] == "shipped"
        assert snapshot["orders"]["order_200"]["status"] == "cancelled"
        assert any(item["order_id"] == "order_100" for item in read_models["orders"])
        assert any(item["order_id"] == "order_200" for item in read_models["orders"])
        assert read_models["dashboard"]["counts"]["exceptions"] >= 1
    finally:
        reopened.close()


def test_forms_wizards_controls_and_agent_skill_runs_are_logged(tmp_path):
    seed_bundle = seed_data.standalone_seed_bundle()
    order_100 = _order_bundle(seed_bundle, "order_100")
    database_path = tmp_path / "dom-interactions.sqlite3"
    app = standalone.DomStandaloneApplication(tenant=seed_bundle["tenant"], database_path=str(database_path))
    try:
        app.configure(seed_bundle["configuration"])
        app.register_defaults(tenant=seed_bundle["tenant"])
        customer = app.submit_form(
            "customer_projection_form",
            seed_bundle["customers"][0],
            principal_permissions=ALL_PERMISSIONS,
        )
        intake = app.run_wizard(
            "order_intake_wizard",
            {
                "order": order_100["order"],
                "tax_projection": order_100["tax_projection"],
                "fraud_signals": order_100["fraud_signals"],
            },
            principal_permissions=ALL_PERMISSIONS,
        )
        fulfillment = app.run_wizard(
            "fulfillment_wizard",
            {
                "order_id": "order_100",
                "allocations": order_100["allocations"],
                "rails": order_100["rails"],
                "shipment_id": order_100["shipment_id"],
            },
            principal_permissions=ALL_PERMISSIONS,
        )
        control = app.execute_control(
            "generate_order_verification_proof",
            {"order_id": "order_100"},
            principal_permissions=ALL_PERMISSIONS,
        )
        agent_result = app.run_agent_skill(
            "dom.document_instruction_intake",
            {
                "document": order_100["document"],
                "instructions": order_100["instructions"],
                "scope": "test",
            },
            principal_permissions=ALL_PERMISSIONS,
        )
        dashboard = app.repository.activity_dashboard(seed_bundle["tenant"], limit=10)
        read_models = app.read_model_snapshot()

        assert customer["ok"] is True
        assert intake["ok"] is True
        assert fulfillment["ok"] is True
        assert control["ok"] is True
        assert agent_result["ok"] is True
        assert dashboard["counts"]["forms"] >= 1
        assert dashboard["counts"]["workflows"] >= 2
        assert dashboard["counts"]["controls"] >= 1
        assert dashboard["counts"]["agent_sessions"] >= 1
        assert len(read_models["orders"]) == 1
        assert read_models["orders"][0]["status"] == "shipped"
    finally:
        app.close()


def test_release_evidence_captures_seed_and_repository_proof():
    evidence = release_evidence.build_release_evidence()
    validation = release_evidence.validate_release_evidence()
    smoke = release_evidence.smoke_test()

    assert evidence["ok"] is True
    assert validation["ok"] is True
    assert smoke["ok"] is True
    assert evidence["seed_data"]["ok"] is True
    assert evidence["standalone"]["release_snapshot"]["ok"] is True
    assert any(check["id"] == "repository_read_models" and check["ok"] for check in evidence["checks"])
    assert evidence["standalone"]["release_snapshot"]["repository"]["dashboard"]["counts"]["controls"] >= 2
