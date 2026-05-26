from pyAppGen.pbc import QUALITY_ASSURANCE_ADVANCED_CAPABILITY_KEYS
from pyAppGen.pbc import pbc_implemented_capability_audit
from pyAppGen.pbc import pbc_implementation_contract
from pyAppGen.pbc import pbc_implementation_release_audit
from pyAppGen.pbc import quality_assurance_build_workbench_view
from pyAppGen.pbc import quality_assurance_configure_runtime
from pyAppGen.pbc import quality_assurance_create_inspection_plan
from pyAppGen.pbc import quality_assurance_create_quality_hold
from pyAppGen.pbc import quality_assurance_disposition_nonconformance
from pyAppGen.pbc import quality_assurance_empty_state
from pyAppGen.pbc import quality_assurance_raise_nonconformance
from pyAppGen.pbc import quality_assurance_record_inspection_result
from pyAppGen.pbc import quality_assurance_register_rule
from pyAppGen.pbc import quality_assurance_release_quality_hold
from pyAppGen.pbc import quality_assurance_render_workbench
from pyAppGen.pbc import quality_assurance_runtime_capabilities
from pyAppGen.pbc import quality_assurance_runtime_smoke
from pyAppGen.pbc import quality_assurance_set_parameter
from pyAppGen.pbc import quality_assurance_ui_contract


def test_quality_assurance_runtime_executes_standard_and_advanced_capabilities() -> None:
    runtime = quality_assurance_runtime_capabilities()
    smoke = quality_assurance_runtime_smoke()

    assert runtime["format"] == "appgen.quality-assurance-runtime-capabilities.v1"
    assert runtime["ok"] is True
    assert runtime["implementation_directory"] == "src/pyAppGen/pbcs/quality_assurance"
    assert len(runtime["standard_features"]) >= 22
    assert "rule_engine" in runtime["standard_features"]
    assert "parameter_engine" in runtime["standard_features"]
    assert "configuration_schema" in runtime["standard_features"]
    assert "workbench" in runtime["standard_features"]
    assert smoke["ok"] is True
    assert set(QUALITY_ASSURANCE_ADVANCED_CAPABILITY_KEYS) == {check["id"] for check in smoke["checks"]}
    assert not smoke["blocking_gaps"]

    contract = pbc_implementation_contract("quality_assurance")
    assert contract["source_package"]["ok"] is True
    assert contract["advanced_runtime"]["ok"] is True
    assert contract["source_package"]["ui_contract"]["ok"] is True
    assert "QualityConfigurationPanel" in contract["source_package"]["ui_contract"]["fragments"]
    assert set(contract["advanced_runtime"]["capabilities"]) == set(QUALITY_ASSURANCE_ADVANCED_CAPABILITY_KEYS)
    assert pbc_implementation_release_audit(("quality_assurance",))["ok"] is True
    assert pbc_implemented_capability_audit(("quality_assurance",))["ok"] is True


def test_quality_assurance_runtime_applies_rules_parameters_configuration_and_ui() -> None:
    state = quality_assurance_empty_state()
    state = quality_assurance_configure_runtime(
        state,
        {
            "database_backend": "postgresql",
            "event_topic": "appgen.quality.events",
            "retry_limit": 3,
            "allowed_sites": ("factory_ops",),
            "allowed_inspection_sources": ("production",),
            "allowed_hold_reasons": ("defect",),
            "allowed_dispositions": ("rework", "release"),
            "default_timezone": "UTC",
            "workbench_limit": 50,
        },
    )["state"]
    state = quality_assurance_set_parameter(state, "default_sample_size", 5)["state"]
    state = quality_assurance_set_parameter(state, "defect_threshold", 1)["state"]
    state = quality_assurance_set_parameter(state, "cpk_minimum", 1.0)["state"]
    state = quality_assurance_set_parameter(state, "hold_severity_threshold", 0.7)["state"]
    state = quality_assurance_set_parameter(state, "capa_due_days", 14)["state"]
    state = quality_assurance_register_rule(
        state,
        {
            "rule_id": "rule_ops",
            "tenant": "tenant_ops",
            "rule_type": "quality",
            "eligible_sources": ("production",),
            "allowed_sites": ("factory_ops",),
            "sampling_methods": ("fixed",),
            "required_measurements": ("length", "torque"),
            "critical_defect_classes": ("safety",),
            "release_dispositions": ("release", "rework"),
            "status": "active",
        },
    )["state"]
    plan = quality_assurance_create_inspection_plan(
        state,
        {
            "plan_id": "plan_ops",
            "tenant": "tenant_ops",
            "item": "machine_kit",
            "site": "factory_ops",
            "source": "production",
            "sampling_method": "fixed",
            "sample_size": 5,
            "revision": "A",
            "status": "released",
        },
    )
    state = plan["state"]
    assert plan["inspection_plan"]["status"] == "active"

    result = quality_assurance_record_inspection_result(
        state,
        {
            "result_id": "result_ops",
            "tenant": "tenant_ops",
            "plan_id": "plan_ops",
            "lot_id": "lot_ops",
            "order_id": "order_ops",
            "measurements": {"length": (10.0, 10.1, 9.9), "torque": (5.0, 5.1, 4.9)},
            "defects": ("scratch",),
            "inspector": "qa_ops",
        },
    )
    state = result["state"]
    assert result["decision"] in {"pass", "fail"}
    assert result["spc"]["cpk"] > 0

    hold = quality_assurance_create_quality_hold(
        state,
        {"hold_id": "hold_ops", "tenant": "tenant_ops", "item": "machine_kit", "lot_id": "lot_ops", "site": "factory_ops", "reason": "defect", "severity": 0.8},
    )
    state = hold["state"]
    assert hold["hold"]["status"] == "active"

    nc = quality_assurance_raise_nonconformance(
        state,
        {"nonconformance_id": "nc_ops", "tenant": "tenant_ops", "result_id": "result_ops", "defect_class": "safety", "severity": 0.8, "root_cause": "assembly_variation"},
    )
    state = nc["state"]
    assert nc["nonconformance"]["severity_class"] == "critical"

    disposition = quality_assurance_disposition_nonconformance(state, "nc_ops", disposition="rework", approved_by="qa_mgr")
    state = disposition["state"]
    assert disposition["nonconformance"]["status"] == "dispositioned"

    release = quality_assurance_release_quality_hold(state, "hold_ops", released_by="qa_mgr")
    state = release["state"]
    assert release["hold"]["status"] == "released"
    assert release["handoffs"] == ("inventory_release_projection", "production_quality_projection", "supplier_score_projection")
    assert state["outbox"][-1]["idempotency_key"] == "quality_assurance:QualityHoldReleased:quality_evt_000006"

    workbench = quality_assurance_build_workbench_view(state, tenant="tenant_ops")
    assert workbench["plan_count"] == 1
    assert workbench["inspection_count"] == 1
    assert workbench["hold_count"] == 1
    assert workbench["released_hold_count"] == 1
    assert workbench["nonconformance_count"] == 1
    assert workbench["critical_nonconformance_count"] == 1

    ui_contract = quality_assurance_ui_contract()
    assert ui_contract["configuration_editor"]["allowed_database_backends"] == ("postgresql", "mysql", "mariadb")
    assert "default_sample_size" in ui_contract["parameter_editor"]["numeric_parameters"]
    assert "rule_id" in ui_contract["rule_editor"]["required_fields"]
    rendered = quality_assurance_render_workbench(
        state,
        tenant="tenant_ops",
        principal_permissions=(
            "quality_assurance.inspect",
            "quality_assurance.hold",
            "quality_assurance.disposition",
            "quality_assurance.configure",
            "quality_assurance.audit",
        ),
    )
    assert rendered["ok"] is True
    assert rendered["configuration_bound"] is True
    assert rendered["event_outbox_count"] == 6
    assert set(rendered["visible_actions"]) == set(ui_contract["action_permissions"])
    assert not rendered["locked_actions"]
