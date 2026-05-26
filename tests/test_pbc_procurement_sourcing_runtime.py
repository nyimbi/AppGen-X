import pytest

from pyAppGen.pbc import PROCUREMENT_SOURCING_ADVANCED_CAPABILITY_KEYS
from pyAppGen.pbc import pbc_implemented_capability_audit
from pyAppGen.pbc import pbc_implementation_contract
from pyAppGen.pbc import pbc_implementation_release_audit
from pyAppGen.pbc import procurement_sourcing_approve_requisition
from pyAppGen.pbc import procurement_sourcing_build_workbench_view
from pyAppGen.pbc import procurement_sourcing_capture_bid
from pyAppGen.pbc import procurement_sourcing_configure_runtime
from pyAppGen.pbc import procurement_sourcing_create_contract
from pyAppGen.pbc import procurement_sourcing_create_requisition
from pyAppGen.pbc import procurement_sourcing_create_rfq
from pyAppGen.pbc import procurement_sourcing_empty_state
from pyAppGen.pbc import procurement_sourcing_issue_purchase_order
from pyAppGen.pbc import procurement_sourcing_register_rule
from pyAppGen.pbc import procurement_sourcing_render_workbench
from pyAppGen.pbc import procurement_sourcing_runtime_capabilities
from pyAppGen.pbc import procurement_sourcing_runtime_smoke
from pyAppGen.pbc import procurement_sourcing_score_suppliers
from pyAppGen.pbc import procurement_sourcing_select_supplier
from pyAppGen.pbc import procurement_sourcing_set_parameter
from pyAppGen.pbc import procurement_sourcing_ui_contract
from pyAppGen.pbcs.procurement_sourcing import PROCUREMENT_SOURCING_ALLOWED_DATABASE_BACKENDS
from pyAppGen.pbcs.procurement_sourcing import PROCUREMENT_SOURCING_CONSUMED_EVENT_TYPES
from pyAppGen.pbcs.procurement_sourcing import PROCUREMENT_SOURCING_EMITTED_EVENT_TYPES
from pyAppGen.pbcs.procurement_sourcing import PROCUREMENT_SOURCING_OWNED_TABLES
from pyAppGen.pbcs.procurement_sourcing import PROCUREMENT_SOURCING_REQUIRED_EVENT_TOPIC
from pyAppGen.pbcs.procurement_sourcing import implementation_contract as procurement_sourcing_package_contract
from pyAppGen.pbcs.procurement_sourcing import procurement_sourcing_build_api_contract
from pyAppGen.pbcs.procurement_sourcing import procurement_sourcing_build_release_evidence
from pyAppGen.pbcs.procurement_sourcing import procurement_sourcing_build_schema_contract
from pyAppGen.pbcs.procurement_sourcing import procurement_sourcing_build_service_contract
from pyAppGen.pbcs.procurement_sourcing import procurement_sourcing_permissions_contract
from pyAppGen.pbcs.procurement_sourcing import procurement_sourcing_receive_event
from pyAppGen.pbcs.procurement_sourcing import procurement_sourcing_register_schema_extension
from pyAppGen.pbcs.procurement_sourcing import procurement_sourcing_verify_owned_table_boundary


def test_procurement_sourcing_runtime_executes_standard_and_advanced_capabilities() -> None:
    runtime = procurement_sourcing_runtime_capabilities()
    smoke = procurement_sourcing_runtime_smoke()

    assert runtime["format"] == "appgen.procurement-sourcing-runtime-capabilities.v1"
    assert runtime["ok"] is True
    assert runtime["implementation_directory"] == "src/pyAppGen/pbcs/procurement_sourcing"
    assert runtime["owned_tables"] == PROCUREMENT_SOURCING_OWNED_TABLES
    assert len(runtime["owned_tables"]) >= 40
    assert len(runtime["standard_features"]) >= 40
    assert "rule_engine" in runtime["standard_features"]
    assert "parameter_engine" in runtime["standard_features"]
    assert "configuration_schema" in runtime["standard_features"]
    assert "appgen_x_outbox" in runtime["standard_features"]
    assert "retry_dead_letter_evidence" in runtime["standard_features"]
    assert smoke["ok"] is True
    assert set(PROCUREMENT_SOURCING_ADVANCED_CAPABILITY_KEYS) == {check["id"] for check in smoke["checks"]}
    assert not smoke["blocking_gaps"]

    contract = pbc_implementation_contract("procurement_sourcing")
    assert contract["source_package"]["ok"] is True
    assert contract["advanced_runtime"]["ok"] is True
    assert contract["source_package"]["ui_contract"]["ok"] is True
    assert "ProcurementConfigurationPanel" in contract["source_package"]["ui_contract"]["fragments"]
    assert set(contract["advanced_runtime"]["capabilities"]) == set(PROCUREMENT_SOURCING_ADVANCED_CAPABILITY_KEYS)

    package_contract = procurement_sourcing_package_contract()
    assert package_contract["api_contract"]["event_contract"] == "AppGen-X"
    assert package_contract["schema_contract"]["ok"] is True
    assert package_contract["service_contract"]["ok"] is True
    assert package_contract["release_evidence_contract"]["ok"] is True
    assert package_contract["permissions_contract"]["action_permissions"]["receive_event"] == "procurement_sourcing.event"
    assert package_contract["owned_tables"] == PROCUREMENT_SOURCING_OWNED_TABLES
    assert package_contract["allowed_database_backends"] == PROCUREMENT_SOURCING_ALLOWED_DATABASE_BACKENDS
    assert package_contract["required_event_topic"] == PROCUREMENT_SOURCING_REQUIRED_EVENT_TOPIC
    assert package_contract["consumes"] == PROCUREMENT_SOURCING_CONSUMED_EVENT_TYPES
    assert package_contract["emits"] == PROCUREMENT_SOURCING_EMITTED_EVENT_TYPES
    assert pbc_implementation_release_audit(("procurement_sourcing",))["ok"] is True
    assert pbc_implemented_capability_audit(("procurement_sourcing",))["ok"] is True


def test_procurement_sourcing_runtime_applies_rules_parameters_and_configuration() -> None:
    state = procurement_sourcing_empty_state()
    state = procurement_sourcing_configure_runtime(
        state,
        {
            "database_backend": "postgresql",
            "event_topic": PROCUREMENT_SOURCING_REQUIRED_EVENT_TOPIC,
            "retry_limit": 3,
            "default_currency": "USD",
            "allowed_categories": ("maintenance",),
            "workbench_limit": 50,
        },
    )["state"]
    state = procurement_sourcing_set_parameter(state, "approval_limit", 2000)["state"]
    state = procurement_sourcing_set_parameter(state, "minimum_bid_count", 2)["state"]
    state = procurement_sourcing_set_parameter(state, "supplier_risk_threshold", 0.4)["state"]
    state = procurement_sourcing_register_rule(
        state,
        {
            "rule_id": "rule_maintenance",
            "tenant": "tenant_ops",
            "rule_type": "sourcing",
            "category": "maintenance",
            "preferred_suppliers": ("supplier_fast",),
            "restricted_suppliers": ("supplier_blocked",),
            "score_weights": {"price": 0.45, "lead_time": 0.2, "risk": 0.2, "quality": 0.15},
            "allow_split_award": True,
            "status": "active",
        },
    )["state"]
    requisition = procurement_sourcing_create_requisition(
        state,
        {
            "requisition_id": "req_ops",
            "tenant": "tenant_ops",
            "legal_entity": "entity_ops",
            "category": "maintenance",
            "item_id": "filter_ops",
            "quantity": 20,
            "estimated_amount": 1800,
            "currency": "USD",
            "cost_center": "ops",
            "requested_by": "planner_ops",
        },
    )
    state = requisition["state"]
    assert requisition["requisition"]["policy_ok"] is True

    approval = procurement_sourcing_approve_requisition(state, "req_ops", approver="manager_ops")
    state = approval["state"]
    assert approval["requisition"]["status"] == "approved"

    state = procurement_sourcing_create_rfq(
        state,
        "rfq_ops",
        requisition_id="req_ops",
        suppliers=("supplier_fast", "supplier_low"),
    )["state"]
    state = procurement_sourcing_capture_bid(
        state,
        "rfq_ops",
        {"supplier_id": "supplier_fast", "price": 1700, "lead_time_days": 5, "risk": 0.1, "quality": 0.95, "carbon": 140},
    )["state"]
    state = procurement_sourcing_capture_bid(
        state,
        "rfq_ops",
        {"supplier_id": "supplier_low", "price": 1600, "lead_time_days": 10, "risk": 0.2, "quality": 0.88, "carbon": 90},
    )["state"]

    scores = procurement_sourcing_score_suppliers(state, "rfq_ops")
    assert scores["scores"][0]["supplier_id"] == "supplier_fast"

    selection = procurement_sourcing_select_supplier(state, "rfq_ops", award_id="award_ops")
    state = selection["state"]
    assert selection["award"]["supplier_id"] == "supplier_fast"

    state = procurement_sourcing_create_contract(state, "contract_ops", award_id="award_ops", term_months=12)["state"]
    purchase_order = procurement_sourcing_issue_purchase_order(
        state,
        "po_ops",
        contract_id="contract_ops",
        quantity=20,
        amount=1700,
    )
    state = purchase_order["state"]
    assert purchase_order["purchase_order"]["status"] == "issued"
    assert state["outbox"][-1]["idempotency_key"] == "procurement_sourcing:PurchaseOrderIssued:procurement_evt_000006"

    workbench = procurement_sourcing_build_workbench_view(state, tenant="tenant_ops")
    assert workbench["requisition_count"] == 1
    assert workbench["rfq_count"] == 1
    assert workbench["contract_count"] == 1
    assert workbench["po_amount"] == 1700
    assert workbench["configuration_bound"] is True
    assert workbench["rule_count"] == 1
    assert workbench["parameter_count"] == 3
    assert workbench["owned_tables"] == PROCUREMENT_SOURCING_OWNED_TABLES
    assert workbench["inbox_table"] == "procurement_sourcing_appgen_inbox_event"

    ui_contract = procurement_sourcing_ui_contract()
    assert ui_contract["configuration_editor"]["allowed_database_backends"] == PROCUREMENT_SOURCING_ALLOWED_DATABASE_BACKENDS
    assert ui_contract["configuration_editor"]["required_event_topic"] == PROCUREMENT_SOURCING_REQUIRED_EVENT_TOPIC
    assert ui_contract["configuration_editor"]["stream_engine_picker_visible"] is False
    assert ui_contract["event_surfaces"]["emits"] == PROCUREMENT_SOURCING_EMITTED_EVENT_TYPES
    assert ui_contract["event_surfaces"]["consumes"] == PROCUREMENT_SOURCING_CONSUMED_EVENT_TYPES
    assert ui_contract["binding_evidence"]["shared_table_access"] is False
    assert "approval_limit" in ui_contract["parameter_editor"]["numeric_parameters"]
    assert "rule_id" in ui_contract["rule_editor"]["required_fields"]
    rendered = procurement_sourcing_render_workbench(
        state,
        tenant="tenant_ops",
        principal_permissions=(
            "procurement_sourcing.request",
            "procurement_sourcing.approve",
            "procurement_sourcing.source",
            "procurement_sourcing.bid",
            "procurement_sourcing.award",
            "procurement_sourcing.contract",
            "procurement_sourcing.order",
            "procurement_sourcing.event",
            "procurement_sourcing.audit",
            "procurement_sourcing.configure",
        ),
    )
    assert rendered["ok"] is True
    assert rendered["configuration_bound"] is True
    assert rendered["event_outbox_count"] == 6
    assert rendered["inbox_count"] == 0
    assert rendered["dead_letter_count"] == 0
    assert rendered["binding_evidence"]["owned_tables"] == PROCUREMENT_SOURCING_OWNED_TABLES
    assert set(rendered["visible_actions"]) == set(ui_contract["action_permissions"])
    assert not rendered["locked_actions"]


def test_procurement_sourcing_rejects_unsupported_database_backends_and_unknown_parameters() -> None:
    state = procurement_sourcing_empty_state()

    with pytest.raises(ValueError, match="PostgreSQL, MySQL, or MariaDB"):
        procurement_sourcing_configure_runtime(
            state,
            {
                "database_backend": "stream_store",
                "event_topic": PROCUREMENT_SOURCING_REQUIRED_EVENT_TOPIC,
                "retry_limit": 3,
                "default_currency": "USD",
            },
        )

    with pytest.raises(ValueError, match="Unsupported Procurement Sourcing parameter"):
        procurement_sourcing_set_parameter(state, "stream_engine", "hidden_picker")

    with pytest.raises(ValueError, match=PROCUREMENT_SOURCING_REQUIRED_EVENT_TOPIC):
        procurement_sourcing_configure_runtime(
            state,
            {
                "database_backend": "postgresql",
                "event_topic": "appgen.procurement.events",
                "retry_limit": 3,
                "default_currency": "USD",
            },
        )

    with pytest.raises(ValueError, match="stream-engine picker"):
        procurement_sourcing_configure_runtime(
            state,
            {
                "database_backend": "postgresql",
                "event_topic": PROCUREMENT_SOURCING_REQUIRED_EVENT_TOPIC,
                "retry_limit": 3,
                "default_currency": "USD",
                "stream_engine": "user_selected_queue",
            },
        )

    with pytest.raises(ValueError, match="owned tables"):
        procurement_sourcing_register_schema_extension(state, "inventory_position", {"supplier_rank": "decimal"})


def test_procurement_sourcing_hardened_event_api_permission_and_boundary_contracts() -> None:
    state = procurement_sourcing_empty_state()
    state = procurement_sourcing_configure_runtime(
        state,
        {
            "database_backend": "mysql",
            "event_topic": PROCUREMENT_SOURCING_REQUIRED_EVENT_TOPIC,
            "retry_limit": 2,
            "default_currency": "USD",
            "allowed_categories": ("maintenance",),
            "workbench_limit": 50,
        },
    )["state"]
    extension = procurement_sourcing_register_schema_extension(
        state,
        "procurement_sourcing_rfq",
        {"sustainability_payload": "jsonb"},
    )
    state = extension["state"]
    assert extension["fields"]["sustainability_payload"] == "jsonb"

    received = procurement_sourcing_receive_event(
        state,
        {
            "event_id": "shortage_ops",
            "event_type": "MaterialShortageDetected",
            "payload": {"tenant": "tenant_ops", "shortage_id": "shortage_ops", "item_id": "filter_ops"},
        },
    )
    state = received["state"]
    assert received["ok"] is True
    assert state["material_shortage_projections"]["shortage_ops"]["item_id"] == "filter_ops"

    duplicate = procurement_sourcing_receive_event(
        state,
        {
            "event_id": "shortage_ops",
            "event_type": "MaterialShortageDetected",
            "payload": {"tenant": "tenant_ops", "shortage_id": "shortage_ops", "item_id": "filter_ops"},
        },
    )
    assert duplicate["duplicate"] is True
    assert len(duplicate["state"]["inbox"]) == 1

    retrying = procurement_sourcing_receive_event(
        state,
        {
            "event_id": "unsupported_ops",
            "event_type": "UndeclaredEvent",
            "payload": {"tenant": "tenant_ops"},
        },
    )
    assert retrying["ok"] is False
    assert retrying["handler"]["status"] == "retrying"
    dead_letter = procurement_sourcing_receive_event(
        retrying["state"],
        {
            "event_id": "unsupported_ops",
            "event_type": "UndeclaredEvent",
            "payload": {"tenant": "tenant_ops"},
        },
    )
    assert dead_letter["handler"]["status"] == "dead_letter"
    assert dead_letter["state"]["dead_letter"][-1]["reason"] == "unsupported_or_failed_procurement_event"

    api = procurement_sourcing_build_api_contract()
    assert api["owned_tables"] == PROCUREMENT_SOURCING_OWNED_TABLES
    assert api["database_backends"] == PROCUREMENT_SOURCING_ALLOWED_DATABASE_BACKENDS
    assert api["shared_table_access"] is False
    assert api["stream_engine_picker_visible"] is False
    assert api["events"]["consumes"] == PROCUREMENT_SOURCING_CONSUMED_EVENT_TYPES
    assert any(route["command"] == "receive_event" for route in api["routes"])

    schema = procurement_sourcing_build_schema_contract()
    service = procurement_sourcing_build_service_contract()
    release = procurement_sourcing_build_release_evidence()
    assert schema["format"] == "appgen.procurement-sourcing-owned-schema-contract.v1"
    assert schema["ok"] is True
    assert len(schema["tables"]) == len(PROCUREMENT_SOURCING_OWNED_TABLES)
    assert len(schema["migrations"]) == len(PROCUREMENT_SOURCING_OWNED_TABLES)
    assert {
        "procurement_sourcing_purchase_requisition_line",
        "procurement_sourcing_supplier_profile",
        "procurement_sourcing_rfq_line",
        "procurement_sourcing_purchase_order_line",
        "procurement_sourcing_governed_model",
    } <= {item["table"] for item in schema["tables"]}
    assert schema["shared_table_access"] is False
    assert service["format"] == "appgen.procurement-sourcing-service-contract.v1"
    assert service["ok"] is True
    assert len(service["command_methods"]) >= 25
    assert service["external_dependencies"]["shared_tables"] == ()
    assert release["format"] == "appgen.procurement-sourcing-release-evidence.v1"
    assert release["ok"] is True
    assert not release["blocking_gaps"]

    permissions = procurement_sourcing_permissions_contract()
    assert permissions["action_permissions"]["register_schema_extension"] == "procurement_sourcing.configure"
    assert permissions["action_permissions"]["receive_event"] == "procurement_sourcing.event"

    valid_boundary = procurement_sourcing_verify_owned_table_boundary(
        (
            "procurement_sourcing_purchase_order",
            "procurement_sourcing_appgen_inbox_event",
            "MaterialShortageDetected",
            "budget_projection",
            "GET /identity/policies",
        ),
    )
    assert valid_boundary["ok"] is True
    assert not valid_boundary["declared_dependencies"]["shared_tables"]

    invalid_boundary = procurement_sourcing_verify_owned_table_boundary(("inventory_position", "gl_core_journal_entry"))
    assert invalid_boundary["ok"] is False
    assert invalid_boundary["violations"] == ("inventory_position", "gl_core_journal_entry")
