import pytest

from pyAppGen.pbc import COMPOSITION_ENGINE_ADVANCED_CAPABILITY_KEYS
from pyAppGen.pbc import composition_engine_bind_layout
from pyAppGen.pbc import composition_engine_build_workbench_view
from pyAppGen.pbc import composition_engine_configure_runtime
from pyAppGen.pbc import composition_engine_create_workspace
from pyAppGen.pbc import composition_engine_empty_state
from pyAppGen.pbc import composition_engine_generate_composition_dsl
from pyAppGen.pbc import composition_engine_publish_composition
from pyAppGen.pbc import composition_engine_register_component
from pyAppGen.pbc import composition_engine_register_rule
from pyAppGen.pbc import composition_engine_register_ui_fragment
from pyAppGen.pbc import composition_engine_render_workbench
from pyAppGen.pbc import composition_engine_runtime_capabilities
from pyAppGen.pbc import composition_engine_runtime_smoke
from pyAppGen.pbc import composition_engine_select_pbc
from pyAppGen.pbc import composition_engine_set_parameter
from pyAppGen.pbc import composition_engine_ui_contract
from pyAppGen.pbc import pbc_implemented_capability_audit
from pyAppGen.pbc import pbc_implementation_contract
from pyAppGen.pbc import pbc_implementation_release_audit
from pyAppGen.pbcs.composition_engine import COMPOSITION_ENGINE_ALLOWED_DATABASE_BACKENDS
from pyAppGen.pbcs.composition_engine import COMPOSITION_ENGINE_CONSUMED_EVENT_TYPES
from pyAppGen.pbcs.composition_engine import COMPOSITION_ENGINE_EMITTED_EVENT_TYPES
from pyAppGen.pbcs.composition_engine import COMPOSITION_ENGINE_OWNED_TABLES
from pyAppGen.pbcs.composition_engine import COMPOSITION_ENGINE_REQUIRED_EVENT_TOPIC
from pyAppGen.pbcs.composition_engine import COMPOSITION_ENGINE_RUNTIME_TABLES
from pyAppGen.pbcs.composition_engine import composition_engine_build_api_contract
from pyAppGen.pbcs.composition_engine import composition_engine_build_release_evidence
from pyAppGen.pbcs.composition_engine import composition_engine_build_schema_contract
from pyAppGen.pbcs.composition_engine import composition_engine_build_service_contract
from pyAppGen.pbcs.composition_engine import implementation_contract as composition_engine_implementation_contract
from pyAppGen.pbcs.composition_engine import composition_engine_permissions_contract
from pyAppGen.pbcs.composition_engine import composition_engine_plan_package_registration
from pyAppGen.pbcs.composition_engine import composition_engine_receive_event
from pyAppGen.pbcs.composition_engine import composition_engine_register_schema_extension
from pyAppGen.pbcs.composition_engine import composition_engine_validate_composition_plan
from pyAppGen.pbcs.composition_engine import composition_engine_verify_owned_table_boundary


def test_composition_engine_runtime_executes_standard_and_advanced_capabilities() -> None:
    runtime = composition_engine_runtime_capabilities()
    smoke = composition_engine_runtime_smoke()

    assert runtime["format"] == "appgen.composition-engine-runtime-capabilities.v1"
    assert runtime["ok"] is True
    assert runtime["implementation_directory"] == "src/pyAppGen/pbcs/composition_engine"
    assert runtime["owned_tables"] == COMPOSITION_ENGINE_OWNED_TABLES
    assert len(runtime["standard_features"]) >= 25
    assert "rule_engine" in runtime["standard_features"]
    assert "parameter_engine" in runtime["standard_features"]
    assert "configuration_schema" in runtime["standard_features"]
    assert "workbench" in runtime["standard_features"]
    assert smoke["ok"] is True
    assert set(COMPOSITION_ENGINE_ADVANCED_CAPABILITY_KEYS) == {check["id"] for check in smoke["checks"]}
    assert not smoke["blocking_gaps"]

    contract = pbc_implementation_contract("composition_engine")
    assert contract["source_package"]["ok"] is True
    assert contract["advanced_runtime"]["ok"] is True
    assert contract["source_package"]["owned_tables"] == COMPOSITION_ENGINE_OWNED_TABLES
    assert contract["source_package"]["runtime_tables"] == COMPOSITION_ENGINE_RUNTIME_TABLES
    assert contract["source_package"]["allowed_database_backends"] == COMPOSITION_ENGINE_ALLOWED_DATABASE_BACKENDS
    assert contract["source_package"]["required_event_topic"] == COMPOSITION_ENGINE_REQUIRED_EVENT_TOPIC
    assert contract["source_package"]["api_contract"]["event_contract"] == "AppGen-X"
    assert contract["source_package"]["schema_contract"]["ok"] is True
    assert contract["source_package"]["service_contract"]["ok"] is True
    assert contract["source_package"]["release_evidence_contract"]["ok"] is True
    assert contract["source_package"]["permissions_contract"]["action_permissions"]["receive_event"] == "composition_engine.event"
    assert contract["source_package"]["ui_contract"]["ok"] is True
    assert "CompositionConfigurationPanel" in contract["source_package"]["ui_contract"]["fragments"]
    assert contract["source_package"]["release_evidence_contract"]["ui"]["binding_evidence"]["runtime_tables"] == COMPOSITION_ENGINE_RUNTIME_TABLES
    assert set(contract["advanced_runtime"]["capabilities"]) == set(COMPOSITION_ENGINE_ADVANCED_CAPABILITY_KEYS)
    assert pbc_implementation_release_audit(("composition_engine",))["ok"] is True
    assert pbc_implemented_capability_audit(("composition_engine",))["ok"] is True

    api = composition_engine_build_api_contract()
    permissions = composition_engine_permissions_contract()
    assert api["owned_tables"] == COMPOSITION_ENGINE_OWNED_TABLES
    assert api["runtime_tables"] == COMPOSITION_ENGINE_RUNTIME_TABLES
    assert api["database_backends"] == COMPOSITION_ENGINE_ALLOWED_DATABASE_BACKENDS
    assert api["emits"] == COMPOSITION_ENGINE_EMITTED_EVENT_TYPES
    assert api["consumes"] == COMPOSITION_ENGINE_CONSUMED_EVENT_TYPES
    assert api["shared_table_access"] is False
    assert api["required_event_topic"] == COMPOSITION_ENGINE_REQUIRED_EVENT_TOPIC
    assert api["stream_engine_picker_visible"] is False
    assert api["user_selectable_event_contract"] is False
    assert {route["route"] for route in api["routes"]} >= {
        "POST /composition-workspaces",
        "POST /composition/events/inbox",
        "GET /composition-workbench",
        "GET /composition/schema-contract",
        "GET /composition/service-contract",
        "GET /composition/release-evidence",
    }
    assert all(isinstance(route, dict) and (route.get("command") or route.get("query")) for route in api["routes"])
    assert permissions["action_permissions"]["plan_package_registration"] == "composition_engine.publish"
    assert permissions["action_permissions"]["build_schema_contract"] == "composition_engine.audit"
    assert permissions["action_permissions"]["build_service_contract"] == "composition_engine.audit"
    assert permissions["action_permissions"]["build_release_evidence"] == "composition_engine.audit"


def test_composition_engine_runtime_applies_rules_parameters_configuration_and_ui() -> None:
    state = composition_engine_empty_state()
    state = composition_engine_configure_runtime(
        state,
        {
            "database_backend": "postgresql",
            "event_topic": COMPOSITION_ENGINE_REQUIRED_EVENT_TOPIC,
            "retry_limit": 3,
            "allowed_targets": ("web", "admin"),
            "allowed_layout_modes": ("grid", "flow"),
            "publication_mode": "side_effect_free_plan",
            "default_timezone": "UTC",
            "workbench_limit": 50,
        },
    )["state"]
    state = composition_engine_set_parameter(state, "max_fragments_per_page", 12)["state"]
    state = composition_engine_set_parameter(state, "release_risk_threshold", 0.35)["state"]
    state = composition_engine_set_parameter(state, "layout_density_target", 0.72)["state"]
    state = composition_engine_set_parameter(state, "route_budget", 24)["state"]
    state = composition_engine_set_parameter(state, "preview_batch_limit", 50)["state"]
    state = composition_engine_register_rule(
        state,
        {
            "rule_id": "rule_ops",
            "tenant": "tenant_ops",
            "scope": "workspace",
            "required_fragments": ("CustomerConfigurationPanel",),
            "allowed_meshes": ("platform", "relationship"),
            "route_policy": "schema_validated",
            "requires_approval": True,
            "severity": "blocking",
            "status": "active",
        },
    )["state"]
    extension = composition_engine_register_schema_extension(state, "layout_binding", {"responsive_rules": "jsonb", "composition_metadata": "jsonb"})
    state = extension["state"]
    assert extension["ok"] is True
    assert state["schema_extensions"]["layout_binding"]["composition_metadata"] == "jsonb"

    schema_event = composition_engine_receive_event(
        state,
        {"event_id": "evt_schema_ops", "event_type": "SchemaAccepted", "payload": {"tenant": "tenant_ops", "schema_id": "CustomerUpdated", "owner_pbc": "customer_360"}},
    )
    state = schema_event["state"]
    assert schema_event["handler"]["status"] == "processed"
    duplicate = composition_engine_receive_event(
        state,
        {"event_id": "evt_schema_ops", "event_type": "SchemaAccepted", "payload": {"tenant": "tenant_ops", "schema_id": "CustomerUpdated", "owner_pbc": "customer_360"}},
    )
    assert duplicate["duplicate"] is True

    workspace = composition_engine_create_workspace(
        state,
        {"workspace_id": "ws_ops", "tenant": "tenant_ops", "name": "Ops Console", "owner": "ops_user", "target": "web"},
    )
    state = workspace["state"]
    assert workspace["workspace"]["status"] == "draft"

    selection = composition_engine_select_pbc(state, "ws_ops", {"pbc": "customer_360", "mesh": "relationship", "reason": "customer workspace"})
    state = selection["state"]
    assert selection["selection"]["pbc"] == "customer_360"

    component = composition_engine_register_component(
        state,
        {"component_id": "cmp_customer", "tenant": "tenant_ops", "pbc": "customer_360", "fragment": "CustomerConfigurationPanel", "permissions": ("customer_360.configure",), "schemas": ("CustomerUpdated",)},
    )
    state = component["state"]
    assert component["component"]["status"] == "registered"

    fragment = composition_engine_register_ui_fragment(
        state,
        {"fragment_id": "frag_customer", "tenant": "tenant_ops", "component_id": "cmp_customer", "route": "/customers", "slots": ("main",), "events": ("CustomerUpdated",)},
    )
    state = fragment["state"]
    assert fragment["fragment"]["status"] == "available"

    binding = composition_engine_bind_layout(
        state,
        {"binding_id": "bind_main", "tenant": "tenant_ops", "workspace_id": "ws_ops", "page": "home", "slot": "main", "fragment_id": "frag_customer", "projection": "customer_profile_projection"},
    )
    state = binding["state"]
    assert binding["binding"]["status"] == "valid"

    validation = composition_engine_validate_composition_plan(state, "ws_ops")
    state = validation["state"]
    assert validation["validation"]["decision"] == "accepted"
    assert validation["validation"]["route_count"] == 1

    package_plan = composition_engine_plan_package_registration(state, "ws_ops", requested_by="ops_user")
    assert package_plan["ok"] is True
    assert package_plan["state"] is state
    assert package_plan["plan"]["side_effect_free"] is True
    assert package_plan["plan"]["writes_performed"] == ()
    assert state["package_registration_plans"] == {}
    assert state["package_index_entries"] == {}
    assert package_plan["plan"]["index_entries"] == (
        {"entry_type": "pbc", "key": "customer_360", "source": "workspace_selection"},
    )

    dsl = composition_engine_generate_composition_dsl(state, "ws_ops")
    state = dsl["state"]
    assert dsl["artifact"]["ok"] is True
    assert dsl["artifact"]["route_count"] == 1
    assert dsl["artifact"]["dsl"]["event_contract"] == "AppGen-X"
    assert dsl["artifact"]["dsl"]["dependency_boundaries"]["shared_tables"] == ()

    publication = composition_engine_publish_composition(state, "ws_ops")
    state = publication["state"]
    assert publication["publication"]["status"] == "published"
    assert publication["publication"]["package_registration_plan"]["side_effect_free"] is True
    assert state["outbox"][-3]["idempotency_key"] == "composition_engine:PackageRegistrationPlanned:composition_evt_000007"
    assert state["outbox"][-2]["idempotency_key"] == "composition_engine:CompositionPublished:composition_evt_000008"
    assert state["outbox"][-1]["idempotency_key"] == "composition_engine:PbcDeployed:composition_evt_000009"

    workbench = composition_engine_build_workbench_view(state, tenant="tenant_ops")
    assert workbench["workspace_count"] == 1
    assert workbench["published_count"] == 1
    assert workbench["component_count"] == 1
    assert workbench["fragment_count"] == 1
    assert workbench["binding_count"] == 1
    assert workbench["validation_count"] == 1
    assert workbench["package_plan_count"] == 1
    assert workbench["configuration_bound"] is True
    assert workbench["rule_count"] == 1
    assert workbench["parameter_count"] == 5
    assert workbench["inbox_count"] == 1
    assert workbench["binding_evidence"]["owned_tables"] == COMPOSITION_ENGINE_OWNED_TABLES
    assert workbench["binding_evidence"]["configuration"]["event_contract"] == "AppGen-X"

    ui_contract = composition_engine_ui_contract()
    assert ui_contract["configuration_editor"]["allowed_database_backends"] == COMPOSITION_ENGINE_ALLOWED_DATABASE_BACKENDS
    assert ui_contract["configuration_editor"]["required_event_topic"] == COMPOSITION_ENGINE_REQUIRED_EVENT_TOPIC
    assert ui_contract["configuration_editor"]["stream_engine_picker_visible"] is False
    assert ui_contract["configuration_editor"]["required_fields"] == (
        "database_backend",
        "event_topic",
        "retry_limit",
        "allowed_targets",
        "allowed_layout_modes",
        "publication_mode",
        "default_timezone",
        "workbench_limit",
    )
    assert ui_contract["binding_evidence"]["owned_tables"] == COMPOSITION_ENGINE_OWNED_TABLES
    assert ui_contract["binding_evidence"]["runtime_tables"] == COMPOSITION_ENGINE_RUNTIME_TABLES
    assert "max_fragments_per_page" in ui_contract["parameter_editor"]["numeric_parameters"]
    assert "rule_id" in ui_contract["rule_editor"]["required_fields"]
    assert "requires_approval" in ui_contract["rule_editor"]["required_fields"]
    rendered = composition_engine_render_workbench(
        state,
        tenant="tenant_ops",
        principal_permissions=(
            "composition_engine.compose",
            "composition_engine.publish",
            "composition_engine.approve",
            "composition_engine.event",
            "composition_engine.configure",
            "composition_engine.audit",
        ),
    )
    assert rendered["ok"] is True
    assert rendered["configuration_bound"] is True
    assert rendered["event_outbox_count"] == 9
    assert rendered["inbox_count"] == 1
    assert set(rendered["visible_actions"]) == set(ui_contract["action_permissions"])
    assert not rendered["locked_actions"]
    assert rendered["binding_evidence"]["owned_tables"] == COMPOSITION_ENGINE_OWNED_TABLES
    assert rendered["binding_evidence"]["runtime_tables"] == COMPOSITION_ENGINE_RUNTIME_TABLES
    assert rendered["binding_evidence"]["shared_table_access"] is False

    boundary = composition_engine_verify_owned_table_boundary(
        ("composition_workspace", "SchemaAccepted", "gateway_composition_projection", "POST /audit/composition-events", "composition_engine_appgen_outbox_event")
    )
    assert boundary["ok"] is True
    assert boundary["declared_dependencies"]["shared_tables"] == ()
    violation_boundary = composition_engine_verify_owned_table_boundary(("gl_core_journal_entry",))
    assert violation_boundary["ok"] is False
    assert violation_boundary["violations"] == ("gl_core_journal_entry",)


def test_composition_engine_package_contract_builders_publish_release_ui_and_boundary_evidence() -> None:
    schema = composition_engine_build_schema_contract()
    service = composition_engine_build_service_contract()
    release = composition_engine_build_release_evidence()
    package_contract = composition_engine_implementation_contract()

    assert schema["ok"] is True
    assert tuple(item["table"] for item in schema["runtime_tables"]) == COMPOSITION_ENGINE_RUNTIME_TABLES
    assert schema["datastore_backends"] == COMPOSITION_ENGINE_ALLOWED_DATABASE_BACKENDS
    assert schema["required_event_topic"] == COMPOSITION_ENGINE_REQUIRED_EVENT_TOPIC
    assert schema["event_contract"] == "AppGen-X"
    assert schema["shared_table_access"] is False
    assert len(schema["tables"]) == len(COMPOSITION_ENGINE_OWNED_TABLES)
    assert len(schema["migrations"]) == len(COMPOSITION_ENGINE_OWNED_TABLES)

    assert service["ok"] is True
    assert service["mutates_only"] == COMPOSITION_ENGINE_OWNED_TABLES
    assert service["runtime_tables"] == COMPOSITION_ENGINE_RUNTIME_TABLES
    assert service["eventing"] == {
        "contract": "AppGen-X",
        "topic": COMPOSITION_ENGINE_REQUIRED_EVENT_TOPIC,
        "stream_engine_picker_visible": False,
        "user_selectable_event_contract": False,
    }
    assert service["external_dependencies"]["shared_tables"] == ()
    assert service["side_effect_free_commands"] == ("plan_package_registration",)
    assert service["retry_dead_letter_evidence"]["outbox_table"] == COMPOSITION_ENGINE_RUNTIME_TABLES[0]
    assert service["retry_dead_letter_evidence"]["inbox_table"] == COMPOSITION_ENGINE_RUNTIME_TABLES[1]
    assert service["retry_dead_letter_evidence"]["dead_letter_table"] == COMPOSITION_ENGINE_RUNTIME_TABLES[2]

    assert release["ok"] is True
    assert not release["blocking_gaps"]
    assert release["schema"]["datastore_backends"] == COMPOSITION_ENGINE_ALLOWED_DATABASE_BACKENDS
    assert release["api"]["required_event_topic"] == COMPOSITION_ENGINE_REQUIRED_EVENT_TOPIC
    assert release["api"]["event_contract"] == "AppGen-X"
    assert release["ui"]["binding_evidence"]["runtime_tables"] == COMPOSITION_ENGINE_RUNTIME_TABLES
    assert release["ui"]["binding_evidence"]["shared_table_access"] is False
    assert release["workbench"]["binding_evidence"]["configuration"]["event_topic"] == COMPOSITION_ENGINE_REQUIRED_EVENT_TOPIC
    assert release["boundary"]["ok"] is True
    assert release["boundary"]["declared_dependencies"]["shared_tables"] == ()
    assert {check["id"] for check in release["checks"]} >= {
        "owned_schema_depth",
        "service_contract_depth",
        "api_event_contract",
        "ui_binding_evidence",
        "boundary_contract",
    }

    assert package_contract["schema_contract"]["ok"] is True
    assert package_contract["service_contract"]["ok"] is True
    assert package_contract["release_evidence_contract"]["ok"] is True
    assert package_contract["runtime_tables"] == COMPOSITION_ENGINE_RUNTIME_TABLES
    assert package_contract["required_event_topic"] == COMPOSITION_ENGINE_REQUIRED_EVENT_TOPIC
    assert package_contract["consumes"] == COMPOSITION_ENGINE_CONSUMED_EVENT_TYPES
    assert package_contract["emits"] == COMPOSITION_ENGINE_EMITTED_EVENT_TYPES


def test_composition_engine_rejects_unsupported_database_backends_eventing_and_boundaries() -> None:
    state = composition_engine_empty_state()

    with pytest.raises(ValueError, match="PostgreSQL, MySQL, or MariaDB"):
        composition_engine_configure_runtime(
            state,
            {
                "database_backend": "stream_store",
                "event_topic": COMPOSITION_ENGINE_REQUIRED_EVENT_TOPIC,
                "retry_limit": 3,
                "default_timezone": "UTC",
            },
        )

    with pytest.raises(ValueError, match="unsupported eventing fields"):
        composition_engine_configure_runtime(
            state,
            {
                "database_backend": "postgresql",
                "event_topic": COMPOSITION_ENGINE_REQUIRED_EVENT_TOPIC,
                "retry_limit": 3,
                "default_timezone": "UTC",
                "stream_engine": "hidden_picker",
            },
        )

    with pytest.raises(ValueError, match="requires AppGen-X event topic"):
        composition_engine_configure_runtime(
            state,
            {
                "database_backend": "postgresql",
                "event_topic": "appgen.user.selected.topic",
                "retry_limit": 3,
                "default_timezone": "UTC",
            },
        )

    with pytest.raises(ValueError, match="Unsupported Composition Engine parameter"):
        composition_engine_set_parameter(state, "stream_engine", "hidden_picker")

    with pytest.raises(ValueError, match="schema extensions must target owned tables"):
        composition_engine_register_schema_extension(state, "gl_core_journal_entry", {"composition_ref": "jsonb"})

    invalid = composition_engine_register_schema_extension(state, "composition_workspace", {"BadField": "jsonb"})
    assert invalid["ok"] is False

    configured = composition_engine_configure_runtime(
        state,
        {
            "database_backend": "postgresql",
            "event_topic": COMPOSITION_ENGINE_REQUIRED_EVENT_TOPIC,
            "retry_limit": 2,
            "allowed_targets": ("web", "admin"),
            "allowed_layout_modes": ("grid", "flow"),
            "publication_mode": "side_effect_free_plan",
            "default_timezone": "UTC",
            "workbench_limit": 50,
        },
    )["state"]
    retrying = composition_engine_receive_event(
        configured,
        {"event_id": "evt_bad", "event_type": "UnsupportedEvent", "payload": {"tenant": "tenant_ops"}},
        simulate_failure=True,
    )
    dead_letter = composition_engine_receive_event(
        retrying["state"],
        {"event_id": "evt_bad", "event_type": "UnsupportedEvent", "payload": {"tenant": "tenant_ops"}},
        simulate_failure=True,
    )
    assert retrying["handler"]["status"] == "retrying"
    assert dead_letter["handler"]["status"] == "dead_letter"
    assert len(dead_letter["state"]["dead_letter"]) == 1
