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


def test_composition_engine_runtime_executes_standard_and_advanced_capabilities() -> None:
    runtime = composition_engine_runtime_capabilities()
    smoke = composition_engine_runtime_smoke()

    assert runtime["format"] == "appgen.composition-engine-runtime-capabilities.v1"
    assert runtime["ok"] is True
    assert runtime["implementation_directory"] == "src/pyAppGen/pbcs/composition_engine"
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
    assert contract["source_package"]["ui_contract"]["ok"] is True
    assert "CompositionConfigurationPanel" in contract["source_package"]["ui_contract"]["fragments"]
    assert set(contract["advanced_runtime"]["capabilities"]) == set(COMPOSITION_ENGINE_ADVANCED_CAPABILITY_KEYS)
    assert pbc_implementation_release_audit(("composition_engine",))["ok"] is True
    assert pbc_implemented_capability_audit(("composition_engine",))["ok"] is True


def test_composition_engine_runtime_applies_rules_parameters_configuration_and_ui() -> None:
    state = composition_engine_empty_state()
    state = composition_engine_configure_runtime(
        state,
        {
            "database_backend": "postgresql",
            "event_topic": "appgen.composition.events",
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

    dsl = composition_engine_generate_composition_dsl(state, "ws_ops")
    state = dsl["state"]
    assert dsl["artifact"]["ok"] is True
    assert dsl["artifact"]["route_count"] == 1

    publication = composition_engine_publish_composition(state, "ws_ops")
    state = publication["state"]
    assert publication["publication"]["status"] == "published"
    assert state["outbox"][-2]["idempotency_key"] == "composition_engine:CompositionPublished:composition_evt_000006"
    assert state["outbox"][-1]["idempotency_key"] == "composition_engine:PbcDeployed:composition_evt_000007"

    workbench = composition_engine_build_workbench_view(state, tenant="tenant_ops")
    assert workbench["workspace_count"] == 1
    assert workbench["published_count"] == 1
    assert workbench["component_count"] == 1
    assert workbench["fragment_count"] == 1
    assert workbench["binding_count"] == 1

    ui_contract = composition_engine_ui_contract()
    assert ui_contract["configuration_editor"]["allowed_database_backends"] == ("postgresql", "mysql", "mariadb")
    assert "max_fragments_per_page" in ui_contract["parameter_editor"]["numeric_parameters"]
    assert "rule_id" in ui_contract["rule_editor"]["required_fields"]
    rendered = composition_engine_render_workbench(
        state,
        tenant="tenant_ops",
        principal_permissions=(
            "composition_engine.compose",
            "composition_engine.publish",
            "composition_engine.configure",
            "composition_engine.audit",
        ),
    )
    assert rendered["ok"] is True
    assert rendered["configuration_bound"] is True
    assert rendered["event_outbox_count"] == 7
    assert set(rendered["visible_actions"]) == set(ui_contract["action_permissions"])
    assert not rendered["locked_actions"]
