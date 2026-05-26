import pytest

from pyAppGen.pbcs.returns_reverse_logistics import RETURNS_REVERSE_LOGISTICS_ALLOWED_DATABASE_BACKENDS
from pyAppGen.pbcs.returns_reverse_logistics import RETURNS_REVERSE_LOGISTICS_CONSUMED_EVENT_TYPES
from pyAppGen.pbcs.returns_reverse_logistics import RETURNS_REVERSE_LOGISTICS_EMITTED_EVENT_TYPES
from pyAppGen.pbcs.returns_reverse_logistics import RETURNS_REVERSE_LOGISTICS_OWNED_TABLES
from pyAppGen.pbcs.returns_reverse_logistics import RETURNS_REVERSE_LOGISTICS_REQUIRED_EVENT_TOPIC
from pyAppGen.pbcs.returns_reverse_logistics import RETURNS_REVERSE_LOGISTICS_RUNTIME_TABLES
from pyAppGen.pbcs.returns_reverse_logistics import RETURNS_REVERSE_LOGISTICS_RUNTIME_CAPABILITY_KEYS
from pyAppGen.pbcs.returns_reverse_logistics import implementation_contract as package_implementation_contract
from pyAppGen.pbcs.returns_reverse_logistics import returns_reverse_logistics_authorize_return
from pyAppGen.pbcs.returns_reverse_logistics import returns_reverse_logistics_build_api_contract
from pyAppGen.pbcs.returns_reverse_logistics import returns_reverse_logistics_build_release_evidence
from pyAppGen.pbcs.returns_reverse_logistics import returns_reverse_logistics_build_schema_contract
from pyAppGen.pbcs.returns_reverse_logistics import returns_reverse_logistics_build_service_contract
from pyAppGen.pbcs.returns_reverse_logistics import returns_reverse_logistics_build_workbench_view
from pyAppGen.pbcs.returns_reverse_logistics import returns_reverse_logistics_configure_runtime
from pyAppGen.pbcs.returns_reverse_logistics import returns_reverse_logistics_create_return_label
from pyAppGen.pbcs.returns_reverse_logistics import returns_reverse_logistics_empty_state
from pyAppGen.pbcs.returns_reverse_logistics import returns_reverse_logistics_issue_credit_adjustment
from pyAppGen.pbcs.returns_reverse_logistics import returns_reverse_logistics_permissions_contract
from pyAppGen.pbcs.returns_reverse_logistics import returns_reverse_logistics_receive_event
from pyAppGen.pbcs.returns_reverse_logistics import returns_reverse_logistics_record_inspection_grade
from pyAppGen.pbcs.returns_reverse_logistics import returns_reverse_logistics_register_rule
from pyAppGen.pbcs.returns_reverse_logistics import returns_reverse_logistics_register_schema_extension
from pyAppGen.pbcs.returns_reverse_logistics import returns_reverse_logistics_render_workbench
from pyAppGen.pbcs.returns_reverse_logistics import returns_reverse_logistics_runtime_capabilities
from pyAppGen.pbcs.returns_reverse_logistics import returns_reverse_logistics_runtime_smoke
from pyAppGen.pbcs.returns_reverse_logistics import returns_reverse_logistics_set_parameter
from pyAppGen.pbcs.returns_reverse_logistics import returns_reverse_logistics_ui_contract
from pyAppGen.pbcs.returns_reverse_logistics import returns_reverse_logistics_verify_owned_table_boundary


def test_returns_reverse_logistics_runtime_executes_standard_and_advanced_capabilities() -> None:
    runtime = returns_reverse_logistics_runtime_capabilities()
    smoke = returns_reverse_logistics_runtime_smoke()

    assert runtime["format"] == "appgen.returns-reverse-logistics-runtime-capabilities.v1"
    assert runtime["ok"] is True
    assert runtime["implementation_directory"] == "src/pyAppGen/pbcs/returns_reverse_logistics"
    assert runtime["required_event_topic"] == RETURNS_REVERSE_LOGISTICS_REQUIRED_EVENT_TOPIC
    assert runtime["runtime_tables"] == RETURNS_REVERSE_LOGISTICS_RUNTIME_TABLES
    assert len(runtime["owned_tables"]) >= 35
    assert len(runtime["standard_features"]) >= 25
    assert "configuration_schema" in runtime["standard_features"]
    assert "rule_engine" in runtime["standard_features"]
    assert "schema_contract" in runtime["standard_features"]
    assert "service_contract" in runtime["standard_features"]
    assert "release_gate" in runtime["standard_features"]
    assert "workbench" in runtime["standard_features"]
    assert {"build_schema_contract", "build_service_contract", "build_release_evidence"} <= set(
        runtime["operations"]
    )
    assert smoke["ok"] is True
    assert {check["id"] for check in smoke["checks"]} == set(RETURNS_REVERSE_LOGISTICS_RUNTIME_CAPABILITY_KEYS)
    assert not smoke["blocking_gaps"]

    package_contract = package_implementation_contract()
    assert package_contract["format"] == "appgen.pbc-source-package.v1"
    assert package_contract["pbc"] == "returns_reverse_logistics"
    assert package_contract["advanced_runtime"]["ok"] is True
    assert package_contract["ui_contract"]["ok"] is True
    assert "ReturnConfigurationPanel" in package_contract["ui_contract"]["fragments"]
    assert package_contract["api_contract"]["ok"] is True
    assert package_contract["schema_contract"]["ok"] is True
    assert package_contract["service_contract"]["ok"] is True
    assert package_contract["release_evidence_contract"]["ok"] is True
    assert package_contract["permissions_contract"]["ok"] is True
    assert package_contract["owned_tables"] == RETURNS_REVERSE_LOGISTICS_OWNED_TABLES
    assert package_contract["runtime_tables"] == RETURNS_REVERSE_LOGISTICS_RUNTIME_TABLES
    assert package_contract["allowed_database_backends"] == (
        RETURNS_REVERSE_LOGISTICS_ALLOWED_DATABASE_BACKENDS
    )
    assert package_contract["required_event_topic"] == RETURNS_REVERSE_LOGISTICS_REQUIRED_EVENT_TOPIC
    assert package_contract["emits"] == RETURNS_REVERSE_LOGISTICS_EMITTED_EVENT_TYPES
    assert package_contract["consumes"] == RETURNS_REVERSE_LOGISTICS_CONSUMED_EVENT_TYPES
    assert package_contract["boundary_contract"]["ok"] is True
    assert package_contract["shared_table_access"] is False
    assert package_contract["api_contract"]["event_contract"] == "AppGen-X"
    assert package_contract["permissions_contract"]["action_permissions"]["receive_event"] == (
        "returns_reverse_logistics.event.consume"
    )


def test_returns_reverse_logistics_runtime_applies_rules_parameters_configuration_and_ui() -> None:
    state = returns_reverse_logistics_empty_state()
    state = returns_reverse_logistics_configure_runtime(
        state,
        {
            "database_backend": "postgresql",
            "event_topic": "appgen.returns.events",
            "retry_limit": 3,
            "default_currency": "USD",
            "supported_carriers": ("parcel_green", "parcel_one"),
            "supported_dispositions": ("restock", "refurbish", "scrap"),
            "workbench_limit": 50,
        },
    )["state"]
    for name, value in (
        ("eligibility_window_days", 30),
        ("fraud_threshold", 0.72),
        ("recovery_floor", 0.35),
        ("carbon_weight", 0.25),
        ("route_switch_threshold", 0.12),
    ):
        state = returns_reverse_logistics_set_parameter(state, name, value)["state"]
    rule = returns_reverse_logistics_register_rule(
        state,
        {
            "rule_id": "rule_ops",
            "tenant": "tenant_ops",
            "scope": "return_policy",
            "status": "active",
            "eligibility_policy": {"max_days_since_shipment": 30, "blocked_reasons": ("final_sale",), "minimum_payment_capture_ratio": 1.0},
            "label_policy": {"preferred_carriers": ("parcel_green",), "max_cost": 15.0},
            "inspection_policy": {"restock_min": 0.85, "refurbish_min": 0.55},
            "credit_policy": {"restock_factor": 0.9, "refurbish_factor": 0.65, "scrap_factor": 0.25},
        },
    )
    state = rule["state"]
    assert rule["rule"]["compiled_hash"]
    extension = returns_reverse_logistics_register_schema_extension(
        state,
        "return_authorization",
        {"policy_evidence": "jsonb"},
    )
    state = extension["state"]
    assert extension["schema_extension"]["table"] == "return_authorization"

    state = returns_reverse_logistics_receive_event(
        state,
        {
            "event_id": "evt_ship_ops",
            "event_type": "OrderShipped",
            "idempotency_key": "order:ops:v1",
            "payload": {
                "tenant": "tenant_ops",
                "order_id": "order_ops",
                "payment_id": "pay_ops",
                "customer_id": "cust_ops",
                "shipped_at": "2026-05-20",
                "days_since_shipped": 5,
                "return_window_days": 30,
                "final_sale": False,
                "items": ({"sku": "sku_ops", "quantity": 1, "unit_price": 120.0},),
            },
        },
    )["state"]
    state = returns_reverse_logistics_receive_event(
        state,
        {
            "event_id": "evt_pay_ops",
            "event_type": "PaymentCaptured",
            "idempotency_key": "payment:ops:v1",
            "payload": {"tenant": "tenant_ops", "payment_id": "pay_ops", "order_id": "order_ops", "captured_amount": 120.0, "currency": "USD", "ledger_account": "refund_liability"},
        },
    )["state"]
    authorization = returns_reverse_logistics_authorize_return(
        state,
        {
            "return_id": "ret_ops",
            "rma": "RMA-OPS",
            "tenant": "tenant_ops",
            "order_id": "order_ops",
            "payment_id": "pay_ops",
            "customer_id": "cust_ops",
            "reason": "damaged",
            "requested_at": "2026-05-25",
            "days_since_shipped": 5,
            "items": ({"sku": "sku_ops", "quantity": 1},),
        },
    )
    state = authorization["state"]
    assert authorization["return_authorization"]["status"] == "authorized"
    state = returns_reverse_logistics_create_return_label(
        state,
        {
            "label_id": "lbl_ops",
            "return_id": "ret_ops",
            "tenant": "tenant_ops",
            "origin": "Boston",
            "destination": "New York",
            "package_weight_kg": 1.2,
            "candidate_carriers": (
                {"carrier_id": "parcel_green", "availability": True, "cost": 9.0, "carbon_intensity": 50.0, "eta_hours": 20.0, "route_health": 0.9},
            ),
        },
    )["state"]
    state = returns_reverse_logistics_record_inspection_grade(
        state,
        {"inspection_id": "insp_ops", "return_id": "ret_ops", "tenant": "tenant_ops", "condition_score": 0.9, "completeness_score": 1.0, "packaging_intact": True},
    )["state"]
    adjustment = returns_reverse_logistics_issue_credit_adjustment(state, {"adjustment_id": "adj_ops", "return_id": "ret_ops", "tenant": "tenant_ops"})
    state = adjustment["state"]
    assert adjustment["credit_adjustment"]["status"] == "issued"
    assert state["outbox"][-1]["idempotency_key"].startswith("returns_reverse_logistics:CreditAdjustmentIssued")

    workbench = returns_reverse_logistics_build_workbench_view(state, tenant="tenant_ops")
    assert workbench["return_count"] == 1
    assert workbench["label_count"] == 1
    assert workbench["receipt_count"] == 1
    assert workbench["inspection_count"] == 1
    assert workbench["credit_count"] == 1
    assert workbench["customer_status_count"] == 1
    assert workbench["configuration_bound"] is True
    assert workbench["rule_count"] == 1
    assert workbench["parameter_count"] == 5
    assert workbench["binding_evidence"]["owned_tables"] == RETURNS_REVERSE_LOGISTICS_OWNED_TABLES
    assert workbench["binding_evidence"]["runtime_tables"] == RETURNS_REVERSE_LOGISTICS_RUNTIME_TABLES
    assert workbench["binding_evidence"]["shared_table_access"] is False
    assert workbench["binding_evidence"]["required_event_topic"] == (
        RETURNS_REVERSE_LOGISTICS_REQUIRED_EVENT_TOPIC
    )

    ui_contract = returns_reverse_logistics_ui_contract()
    api_contract = returns_reverse_logistics_build_api_contract()
    permissions_contract = returns_reverse_logistics_permissions_contract()
    assert ui_contract["configuration_editor"]["allowed_database_backends"] == (
        RETURNS_REVERSE_LOGISTICS_ALLOWED_DATABASE_BACKENDS
    )
    assert ui_contract["configuration_editor"]["required_event_topic"] == (
        RETURNS_REVERSE_LOGISTICS_REQUIRED_EVENT_TOPIC
    )
    assert ui_contract["configuration_editor"]["stream_engine_picker_visible"] is False
    assert ui_contract["configuration_editor"]["user_eventing_choice"] is False
    assert ui_contract["event_surfaces"]["event_contract"] == "AppGen-X"
    assert ui_contract["event_surfaces"]["required_event_topic"] == (
        RETURNS_REVERSE_LOGISTICS_REQUIRED_EVENT_TOPIC
    )
    assert ui_contract["binding_evidence"]["runtime_tables"] == RETURNS_REVERSE_LOGISTICS_RUNTIME_TABLES
    assert ui_contract["action_permissions"]["receive_event"] == (
        "returns_reverse_logistics.event.consume"
    )
    assert api_contract["shared_table_access"] is False
    assert api_contract["owned_tables"] == RETURNS_REVERSE_LOGISTICS_OWNED_TABLES
    assert api_contract["runtime_tables"] == RETURNS_REVERSE_LOGISTICS_RUNTIME_TABLES
    assert api_contract["required_event_topic"] == RETURNS_REVERSE_LOGISTICS_REQUIRED_EVENT_TOPIC
    assert api_contract["stream_engine_picker_visible"] is False
    assert any(route.get("command") == "configure_runtime" for route in api_contract["routes"])
    assert any(route.get("command") == "receive_event" for route in api_contract["routes"])
    assert any(route.get("query") == "build_schema_contract" for route in api_contract["routes"])
    assert any(route.get("query") == "build_service_contract" for route in api_contract["routes"])
    assert any(route.get("query") == "build_release_evidence" for route in api_contract["routes"])
    assert permissions_contract["action_permissions"]["register_schema_extension"] == (
        "returns_reverse_logistics.configure"
    )
    assert permissions_contract["action_permissions"]["build_schema_contract"] == (
        "returns_reverse_logistics.audit"
    )
    assert permissions_contract["action_permissions"]["build_service_contract"] == (
        "returns_reverse_logistics.audit"
    )
    assert permissions_contract["action_permissions"]["build_release_evidence"] == (
        "returns_reverse_logistics.audit"
    )
    rendered = returns_reverse_logistics_render_workbench(
        state,
        tenant="tenant_ops",
        principal_permissions=(
            "returns_reverse_logistics.authorize",
            "returns_reverse_logistics.label",
            "returns_reverse_logistics.inspect",
            "returns_reverse_logistics.adjust",
            "returns_reverse_logistics.event.consume",
            "returns_reverse_logistics.audit",
            "returns_reverse_logistics.configure",
            "returns_reverse_logistics.claim",
        ),
    )
    assert rendered["ok"] is True
    assert rendered["configuration_bound"] is True
    assert rendered["binding_evidence"]["dead_letter_table"] == (
        "returns_reverse_logistics_dead_letter_event"
    )
    assert rendered["binding_evidence"]["runtime_tables"] == RETURNS_REVERSE_LOGISTICS_RUNTIME_TABLES
    assert not rendered["locked_actions"]


def test_returns_reverse_logistics_package_schema_service_and_release_contracts() -> None:
    schema = returns_reverse_logistics_build_schema_contract()
    service = returns_reverse_logistics_build_service_contract()
    release = returns_reverse_logistics_build_release_evidence()
    api = returns_reverse_logistics_build_api_contract()

    assert schema["format"] == "appgen.returns-reverse-logistics-owned-schema-contract.v1"
    assert schema["ok"] is True
    assert schema["owned_tables"] == RETURNS_REVERSE_LOGISTICS_OWNED_TABLES
    assert len(schema["tables"]) == len(RETURNS_REVERSE_LOGISTICS_OWNED_TABLES)
    assert len(schema["migrations"]) == len(RETURNS_REVERSE_LOGISTICS_OWNED_TABLES)
    assert schema["runtime_tables"] == (
        {
            "table": RETURNS_REVERSE_LOGISTICS_RUNTIME_TABLES[0],
            "fields": ("tenant", "event_id", "event_type", "topic", "payload", "idempotency_key", "published_at", "audit_hash"),
        },
        {
            "table": RETURNS_REVERSE_LOGISTICS_RUNTIME_TABLES[1],
            "fields": ("tenant", "event_id", "event_type", "payload", "idempotency_key", "attempts", "status", "audit_hash"),
        },
        {
            "table": RETURNS_REVERSE_LOGISTICS_RUNTIME_TABLES[2],
            "fields": ("tenant", "event_id", "event_type", "payload", "idempotency_key", "attempts", "reason", "audit_hash"),
        },
    )
    assert schema["required_event_topic"] == RETURNS_REVERSE_LOGISTICS_REQUIRED_EVENT_TOPIC
    assert schema["shared_table_access"] is False

    assert service["format"] == "appgen.returns-reverse-logistics-service-contract.v1"
    assert service["ok"] is True
    assert service["mutates_only_owned_tables"] is True
    assert service["shared_table_access"] is False
    assert service["event_contract"]["contract"] == "AppGen-X"
    assert service["event_contract"]["required_topic"] == RETURNS_REVERSE_LOGISTICS_REQUIRED_EVENT_TOPIC
    assert "open_carrier_claim" in service["command_methods"]
    assert "build_release_evidence" in service["query_methods"]
    assert service["retry_dead_letter_evidence"]["dead_letter_table"] == (
        RETURNS_REVERSE_LOGISTICS_RUNTIME_TABLES[2]
    )

    assert api["dependencies"]["shared_tables"] == ()
    assert api["events"] == {
        "emits": RETURNS_REVERSE_LOGISTICS_EMITTED_EVENT_TYPES,
        "consumes": RETURNS_REVERSE_LOGISTICS_CONSUMED_EVENT_TYPES,
    }

    assert release["format"] == "appgen.returns-reverse-logistics-release-evidence.v1"
    assert release["ok"] is True
    assert not release["blocking_gaps"]
    assert release["schema"]["format"] == schema["format"]
    assert release["service"]["format"] == service["format"]
    assert release["api"]["required_event_topic"] == RETURNS_REVERSE_LOGISTICS_REQUIRED_EVENT_TOPIC
    assert release["control"]["summary"]["duplicate_status"] == "duplicate"
    assert release["control"]["summary"]["retry_status"] == "retrying"
    assert release["control"]["summary"]["dead_letter_status"] == "dead_letter"
    assert release["control"]["workbench"]["binding_evidence"]["runtime_tables"] == (
        RETURNS_REVERSE_LOGISTICS_RUNTIME_TABLES
    )


def test_returns_reverse_logistics_enforces_owned_table_only_boundary() -> None:
    allowed = returns_reverse_logistics_verify_owned_table_boundary(
        (
            "return_authorization",
            "returns_reverse_logistics_inbox_event",
            "OrderShipped",
            "order_projection",
            "POST /refunds",
            "POST /exchange-orders",
        )
    )
    blocked = returns_reverse_logistics_verify_owned_table_boundary(
        ("return_authorization", "shared_orders", "customer_master")
    )

    assert allowed["ok"] is True
    assert allowed["violations"] == ()
    assert blocked["ok"] is False
    assert blocked["violations"] == ("shared_orders", "customer_master")

    state = returns_reverse_logistics_empty_state()
    with pytest.raises(ValueError, match="owned tables"):
        returns_reverse_logistics_register_schema_extension(
            state,
            "shared_orders",
            {"foreign_status": "text"},
        )


def test_returns_reverse_logistics_rejects_invalid_runtime_inputs_and_records_dead_letters() -> None:
    state = returns_reverse_logistics_empty_state()
    with pytest.raises(ValueError, match="PostgreSQL, MySQL, or MariaDB"):
        returns_reverse_logistics_configure_runtime(
            state,
            {
                "database_backend": "stream_store",
                "event_topic": RETURNS_REVERSE_LOGISTICS_REQUIRED_EVENT_TOPIC,
                "retry_limit": 3,
                "default_currency": "USD",
                "supported_carriers": ("parcel_green",),
                "supported_dispositions": ("restock",),
            },
        )
    state = returns_reverse_logistics_configure_runtime(
        state,
        {
            "database_backend": "postgresql",
            "event_topic": RETURNS_REVERSE_LOGISTICS_REQUIRED_EVENT_TOPIC,
            "retry_limit": 2,
            "default_currency": "USD",
            "supported_carriers": ("parcel_green",),
            "supported_dispositions": ("restock",),
        },
    )["state"]
    with pytest.raises(ValueError, match="requires event topic"):
        returns_reverse_logistics_configure_runtime(
            returns_reverse_logistics_empty_state(),
            {
                "database_backend": "postgresql",
                "event_topic": "custom.returns.events",
                "retry_limit": 2,
                "default_currency": "USD",
                "supported_carriers": ("parcel_green",),
                "supported_dispositions": ("restock",),
            },
        )
    with pytest.raises(ValueError, match="Unsupported Returns Reverse Logistics parameter"):
        returns_reverse_logistics_set_parameter(state, "stream_engine", 1)
    with pytest.raises(ValueError, match="stream-engine or user eventing fields"):
        returns_reverse_logistics_register_rule(
            state,
            {
                "rule_id": "rule_bad",
                "tenant": "tenant_ops",
                "scope": "return_policy",
                "status": "active",
                "eligibility_policy": {"max_days_since_shipment": 30},
                "label_policy": {"preferred_carriers": ("parcel_green",)},
                "inspection_policy": {"restock_min": 0.8, "refurbish_min": 0.5},
                "credit_policy": {
                    "restock_factor": 0.9,
                    "refurbish_factor": 0.65,
                    "scrap_factor": 0.25,
                },
                "stream_engine_picker": "hidden",
            },
        )
    accepted = returns_reverse_logistics_receive_event(
        state,
        {
            "event_id": "evt_ship_once",
            "event_type": "OrderShipped",
            "idempotency_key": "order:once:v1",
            "payload": {
                "tenant": "tenant_ops",
                "order_id": "order_once",
                "payment_id": "pay_once",
                "customer_id": "cust_once",
                "shipped_at": "2026-05-20",
                "days_since_shipped": 2,
                "return_window_days": 30,
                "final_sale": False,
                "items": ({"sku": "sku_once", "quantity": 1, "unit_price": 80.0},),
            },
        },
    )
    state = accepted["state"]
    duplicate = returns_reverse_logistics_receive_event(
        state,
        {
            "event_id": "evt_ship_once",
            "event_type": "OrderShipped",
            "idempotency_key": "order:once:v1",
            "payload": {
                "tenant": "tenant_ops",
                "order_id": "order_once",
                "payment_id": "pay_once",
                "customer_id": "cust_once",
                "shipped_at": "2026-05-20",
                "days_since_shipped": 2,
                "return_window_days": 30,
                "final_sale": False,
                "items": ({"sku": "sku_once", "quantity": 1, "unit_price": 80.0},),
            },
        },
    )
    retrying = returns_reverse_logistics_receive_event(
        state,
        {
            "event_id": "evt_unknown_retry",
            "event_type": "UnknownEvent",
            "idempotency_key": "unknown:retry",
            "attempts": 1,
            "payload": {"tenant": "tenant_ops"},
        },
    )
    state = retrying["state"]
    failed = returns_reverse_logistics_receive_event(
        state,
        {
            "event_id": "evt_unknown_dead",
            "event_type": "UnknownEvent",
            "idempotency_key": "unknown:dead",
            "attempts": 2,
            "payload": {"tenant": "tenant_ops"},
        },
    )
    assert accepted["inbox_record"]["status"] == "handled"
    assert duplicate["duplicate"] is True
    assert duplicate["dead_lettered"] is False
    assert len(state["inbox"]) == 2
    assert retrying["ok"] is False
    assert retrying["dead_lettered"] is False
    assert retrying["retry_evidence"]["status"] == "retrying"
    assert failed["ok"] is False
    assert failed["dead_lettered"] is True
    assert len(failed["state"]["dead_letter"]) == 1
    assert failed["dead_letter_record"]["dead_letter_table"] == (
        "returns_reverse_logistics_dead_letter_event"
    )
