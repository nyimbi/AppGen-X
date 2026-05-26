import pytest

from pyAppGen.pbcs.asset_lifecycle import ASSET_LIFECYCLE_ALLOWED_DATABASE_BACKENDS
from pyAppGen.pbcs.asset_lifecycle import ASSET_LIFECYCLE_CONSUMED_EVENT_TYPES
from pyAppGen.pbcs.asset_lifecycle import ASSET_LIFECYCLE_EMITTED_EVENT_TYPES
from pyAppGen.pbcs.asset_lifecycle import ASSET_LIFECYCLE_OWNED_TABLES
from pyAppGen.pbcs.asset_lifecycle import ASSET_LIFECYCLE_REQUIRED_EVENT_TOPIC
from pyAppGen.pbcs.asset_lifecycle import asset_lifecycle_build_api_contract
from pyAppGen.pbcs.asset_lifecycle import asset_lifecycle_permissions_contract
from pyAppGen.pbcs.asset_lifecycle import asset_lifecycle_receive_event
from pyAppGen.pbcs.asset_lifecycle import asset_lifecycle_register_schema_extension
from pyAppGen.pbcs.asset_lifecycle import asset_lifecycle_verify_owned_table_boundary
from pyAppGen.pbc import ASSET_LIFECYCLE_ADVANCED_CAPABILITY_KEYS
from pyAppGen.pbc import asset_lifecycle_build_depreciation_schedule
from pyAppGen.pbc import asset_lifecycle_build_workbench_view
from pyAppGen.pbc import asset_lifecycle_configure_runtime
from pyAppGen.pbc import asset_lifecycle_empty_state
from pyAppGen.pbc import asset_lifecycle_place_asset_in_service
from pyAppGen.pbc import asset_lifecycle_register_asset
from pyAppGen.pbc import asset_lifecycle_register_rule
from pyAppGen.pbc import asset_lifecycle_render_workbench
from pyAppGen.pbc import asset_lifecycle_retire_asset
from pyAppGen.pbc import asset_lifecycle_run_depreciation
from pyAppGen.pbc import asset_lifecycle_runtime_capabilities
from pyAppGen.pbc import asset_lifecycle_runtime_smoke
from pyAppGen.pbc import asset_lifecycle_set_parameter
from pyAppGen.pbc import asset_lifecycle_transfer_asset
from pyAppGen.pbc import asset_lifecycle_ui_contract
from pyAppGen.pbc import pbc_implemented_capability_audit
from pyAppGen.pbc import pbc_implementation_contract
from pyAppGen.pbc import pbc_implementation_release_audit


def test_asset_lifecycle_runtime_executes_standard_and_advanced_capabilities() -> None:
    runtime = asset_lifecycle_runtime_capabilities()
    smoke = asset_lifecycle_runtime_smoke()

    assert runtime["format"] == "appgen.asset-lifecycle-runtime-capabilities.v1"
    assert runtime["ok"] is True
    assert runtime["implementation_directory"] == "src/pyAppGen/pbcs/asset_lifecycle"
    assert runtime["owned_tables"] == ASSET_LIFECYCLE_OWNED_TABLES
    assert "configuration_schema" in runtime["standard_features"]
    assert "rule_engine" in runtime["standard_features"]
    assert "parameter_engine" in runtime["standard_features"]
    assert "workbench" in runtime["standard_features"]
    assert len(runtime["standard_features"]) >= 18
    assert smoke["ok"] is True
    assert set(ASSET_LIFECYCLE_ADVANCED_CAPABILITY_KEYS) == {check["id"] for check in smoke["checks"]}
    assert not smoke["blocking_gaps"]

    contract = pbc_implementation_contract("asset_lifecycle")
    assert contract["source_package"]["ok"] is True
    assert contract["advanced_runtime"]["ok"] is True
    assert contract["source_package"]["owned_tables"] == ASSET_LIFECYCLE_OWNED_TABLES
    assert contract["source_package"]["allowed_database_backends"] == ASSET_LIFECYCLE_ALLOWED_DATABASE_BACKENDS
    assert contract["source_package"]["api_contract"]["event_contract"] == "AppGen-X"
    assert contract["source_package"]["api_contract"]["stream_engine_picker_visible"] is False
    assert contract["source_package"]["permissions_contract"]["action_permissions"]["receive_event"] == "asset_lifecycle.event"
    assert contract["source_package"]["ui_contract"]["ok"] is True
    assert "AssetConfigurationPanel" in contract["source_package"]["ui_contract"]["fragments"]
    assert set(contract["advanced_runtime"]["capabilities"]) == set(ASSET_LIFECYCLE_ADVANCED_CAPABILITY_KEYS)
    assert pbc_implementation_release_audit(("asset_lifecycle",))["ok"] is True
    assert pbc_implemented_capability_audit(("asset_lifecycle",))["ok"] is True

    api = asset_lifecycle_build_api_contract()
    permissions = asset_lifecycle_permissions_contract()
    assert api["format"] == "appgen.asset-lifecycle-api-contract.v1"
    assert api["owned_tables"] == ASSET_LIFECYCLE_OWNED_TABLES
    assert api["database_backends"] == ASSET_LIFECYCLE_ALLOWED_DATABASE_BACKENDS
    assert api["emits"] == ASSET_LIFECYCLE_EMITTED_EVENT_TYPES
    assert api["consumes"] == ASSET_LIFECYCLE_CONSUMED_EVENT_TYPES
    assert api["shared_table_access"] is False
    assert {route["route"] for route in api["routes"]} >= {"POST /assets", "POST /assets/events/inbox", "GET /assets"}
    assert all(isinstance(route, dict) and (route.get("command") or route.get("query")) for route in api["routes"])
    assert permissions["roles"]["asset_lifecycle_auditor"] == ("asset_lifecycle.read", "asset_lifecycle.audit")


def test_asset_lifecycle_runtime_handles_core_fixed_asset_workflows() -> None:
    state = asset_lifecycle_empty_state()
    state = asset_lifecycle_configure_runtime(
        state,
        {
            "database_backend": "postgresql",
            "event_topic": ASSET_LIFECYCLE_REQUIRED_EVENT_TOPIC,
            "retry_limit": 3,
            "default_currency": "USD",
            "default_timezone": "UTC",
            "default_book": "corporate",
            "workbench_limit": 50,
        },
    )["state"]
    state = asset_lifecycle_set_parameter(state, "capitalization_threshold", 500)["state"]
    state = asset_lifecycle_set_parameter(state, "impairment_indicator_threshold", 0.65)["state"]
    state = asset_lifecycle_register_rule(
        state,
        {
            "rule_id": "rule_ops",
            "tenant": "tenant_ops",
            "scope": "capitalization",
            "capitalization_threshold": 500,
            "approval_required": True,
            "status": "active",
        },
    )["state"]
    extension = asset_lifecycle_register_schema_extension(state, "fixed_asset", {"carbon_payload": "jsonb"})
    state = extension["state"]
    assert extension["ok"] is True
    assert state["schema_extensions"]["fixed_asset"]["carbon_payload"] == "jsonb"
    receipt_event = asset_lifecycle_receive_event(
        state,
        {
            "event_id": "evt_receipt_asset_ops",
            "event_type": "PurchaseReceiptCapitalized",
            "payload": {"tenant": "tenant_ops", "receipt_id": "rcpt_1", "asset_id": "asset_ops", "amount": 6000},
        },
    )
    state = receipt_event["state"]
    assert receipt_event["handler"]["status"] == "processed"
    duplicate = asset_lifecycle_receive_event(
        state,
        {
            "event_id": "evt_receipt_asset_ops",
            "event_type": "PurchaseReceiptCapitalized",
            "payload": {"tenant": "tenant_ops", "receipt_id": "rcpt_1", "asset_id": "asset_ops", "amount": 6000},
        },
    )
    assert duplicate["duplicate"] is True
    assert state["projections"]["purchase_receipts"]["asset_ops"]["payload"]["amount"] == 6000
    state = asset_lifecycle_register_asset(
        state,
        {
            "asset_id": "asset_ops",
            "tenant": "tenant_ops",
            "legal_entity": "entity_ops",
            "description": "Packaging Robot",
            "category": "equipment",
            "cost": 6000,
            "residual_value": 600,
            "currency": "USD",
            "book": "corporate",
            "useful_life_months": 36,
            "location": "plant_1",
            "custodian": "ops_manager",
            "cost_center": "manufacturing",
            "components": ("arm", "controller"),
            "identity": {"did": "did:appgen:asset-ops", "issuer": "asset_registry", "status": "active"},
        },
    )["state"]
    state = asset_lifecycle_place_asset_in_service(state, "asset_ops", service_date="2026-05-26")["state"]

    schedule = asset_lifecycle_build_depreciation_schedule(state, "asset_ops", method="straight_line")
    state = schedule["state"]
    assert schedule["schedule"]["lines"][0]["amount"] == 150

    depreciation = asset_lifecycle_run_depreciation(state, run_id="dep_ops", period="2026-06")
    state = depreciation["state"]
    assert depreciation["journals"][0]["amount"] == 150
    assert state["assets"]["asset_ops"]["book_value"] == 5850
    assert state["outbox"][-1]["idempotency_key"] == "asset_lifecycle:DepreciationCalculated:asset_evt_000003"

    state = asset_lifecycle_transfer_asset(
        state,
        "asset_ops",
        location="plant_2",
        cost_center="maintenance",
        approved_by="controller",
    )["state"]
    assert state["assets"]["asset_ops"]["location"] == "plant_2"
    assert state["assets"]["asset_ops"]["cost_center"] == "maintenance"

    retirement = asset_lifecycle_retire_asset(state, "asset_ops", proceeds=5000, approved_by="controller")
    state = retirement["state"]
    assert retirement["asset"]["status"] == "retired"
    assert retirement["asset"]["disposal_gain_loss"] == -850

    workbench = asset_lifecycle_build_workbench_view(state, tenant="tenant_ops")
    assert workbench["asset_count"] == 1
    assert workbench["retired_count"] == 1
    assert workbench["configuration_bound"] is True
    assert workbench["rule_count"] == 1
    assert workbench["parameter_count"] == 2
    assert workbench["inbox_count"] == 1
    assert workbench["dead_letter_count"] == 0
    assert workbench["binding_evidence"]["owned_tables"] == ASSET_LIFECYCLE_OWNED_TABLES
    assert workbench["binding_evidence"]["configuration"]["event_contract"] == "AppGen-X"

    ui_contract = asset_lifecycle_ui_contract()
    assert ui_contract["configuration_editor"]["allowed_database_backends"] == ASSET_LIFECYCLE_ALLOWED_DATABASE_BACKENDS
    assert ui_contract["configuration_editor"]["fixed_event_topic"] == ASSET_LIFECYCLE_REQUIRED_EVENT_TOPIC
    assert ui_contract["configuration_editor"]["stream_engine_picker_visible"] is False
    assert "capitalization_threshold" in ui_contract["parameter_editor"]["numeric_parameters"]
    assert "rule_id" in ui_contract["rule_editor"]["required_fields"]
    assert ui_contract["workbench_binding_evidence"]["owned_tables"] == ASSET_LIFECYCLE_OWNED_TABLES
    rendered = asset_lifecycle_render_workbench(
        state,
        tenant="tenant_ops",
        principal_permissions=(
            "asset_lifecycle.register",
            "asset_lifecycle.service",
            "asset_lifecycle.depreciation",
            "asset_lifecycle.transfer",
            "asset_lifecycle.valuation",
            "asset_lifecycle.maintenance",
            "asset_lifecycle.retirement",
            "asset_lifecycle.audit",
            "asset_lifecycle.configure",
            "asset_lifecycle.event",
        ),
    )
    assert rendered["ok"] is True
    assert rendered["configuration_bound"] is True
    assert rendered["event_outbox_count"] == 5
    assert rendered["event_inbox_count"] == 1
    assert rendered["dead_letter_count"] == 0
    assert rendered["binding_evidence"]["configuration"]["event_contract"] == "AppGen-X"
    assert set(rendered["visible_actions"]) == set(ui_contract["action_permissions"])
    assert not rendered["locked_actions"]


def test_asset_lifecycle_rejects_unsupported_database_backends_and_unknown_parameters() -> None:
    state = asset_lifecycle_empty_state()

    with pytest.raises(ValueError, match="PostgreSQL, MySQL, or MariaDB"):
        asset_lifecycle_configure_runtime(
            state,
            {
                "database_backend": "stream_store",
                "event_topic": ASSET_LIFECYCLE_REQUIRED_EVENT_TOPIC,
                "retry_limit": 3,
                "default_currency": "USD",
                "default_timezone": "UTC",
            },
        )

    with pytest.raises(ValueError, match="Unsupported Asset Lifecycle parameter"):
        asset_lifecycle_set_parameter(state, "stream_engine", "hidden_picker")

    with pytest.raises(ValueError, match="AppGen-X event topic"):
        asset_lifecycle_configure_runtime(
            state,
            {
                "database_backend": "postgresql",
                "event_topic": "custom.asset.events",
                "retry_limit": 3,
                "default_currency": "USD",
                "default_timezone": "UTC",
            },
        )

    with pytest.raises(ValueError, match="stream-engine picker"):
        asset_lifecycle_configure_runtime(
            state,
            {
                "database_backend": "postgresql",
                "event_topic": ASSET_LIFECYCLE_REQUIRED_EVENT_TOPIC,
                "retry_limit": 3,
                "default_currency": "USD",
                "default_timezone": "UTC",
                "stream_engine": "user_choice",
            },
        )

    extension = asset_lifecycle_register_schema_extension(state, "ledger_entry", {"memo": "text"})
    assert extension["ok"] is False
    assert extension["error"] == "non_owned_table"

    state = asset_lifecycle_configure_runtime(
        state,
        {
            "database_backend": "postgresql",
            "event_topic": ASSET_LIFECYCLE_REQUIRED_EVENT_TOPIC,
            "retry_limit": 2,
            "default_currency": "USD",
            "default_timezone": "UTC",
        },
    )["state"]
    retry = asset_lifecycle_receive_event(state, {"event_id": "evt_unknown_1", "event_type": "UnknownEvent", "payload": {"x": 1}, "attempts": 1})
    assert retry["ok"] is False
    assert retry["handler"]["status"] == "retrying"
    dead = asset_lifecycle_receive_event(retry["state"], {"event_id": "evt_unknown_2", "event_type": "UnknownEvent", "payload": {"x": 1}, "attempts": 2})
    assert dead["dead_lettered"] is True
    assert dead["state"]["dead_letters"][-1]["reason"] == "unsupported_event_type"

    boundary = asset_lifecycle_verify_owned_table_boundary(
        (
            "fixed_asset",
            "asset_lifecycle_appgen_outbox_event",
            "purchase_receipt_projection",
            "PurchaseReceiptCapitalized",
        )
    )
    assert boundary["ok"] is True
    violation = asset_lifecycle_verify_owned_table_boundary(("fixed_asset", "general_ledger_entry"))
    assert violation["ok"] is False
    assert violation["violations"] == ("general_ledger_entry",)
