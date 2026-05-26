from pyAppGen.pbc import EAM_ADVANCED_CAPABILITY_KEYS
from pyAppGen.pbc import eam_build_workbench_view
from pyAppGen.pbc import eam_complete_work_order
from pyAppGen.pbc import eam_configure_runtime
from pyAppGen.pbc import eam_create_maintenance_plan
from pyAppGen.pbc import eam_create_safety_permit
from pyAppGen.pbc import eam_create_work_order
from pyAppGen.pbc import eam_empty_state
from pyAppGen.pbc import eam_issue_spare_part
from pyAppGen.pbc import eam_record_condition_reading
from pyAppGen.pbc import eam_record_meter_reading
from pyAppGen.pbc import eam_register_equipment
from pyAppGen.pbc import eam_register_rule
from pyAppGen.pbc import eam_render_workbench
from pyAppGen.pbc import eam_runtime_capabilities
from pyAppGen.pbc import eam_runtime_smoke
from pyAppGen.pbc import eam_schedule_work_order
from pyAppGen.pbc import eam_set_parameter
from pyAppGen.pbc import eam_ui_contract
from pyAppGen.pbc import pbc_implemented_capability_audit
from pyAppGen.pbc import pbc_implementation_contract
from pyAppGen.pbc import pbc_implementation_release_audit


def test_eam_runtime_executes_standard_and_advanced_capabilities() -> None:
    runtime = eam_runtime_capabilities()
    smoke = eam_runtime_smoke()

    assert runtime["format"] == "appgen.eam-runtime-capabilities.v1"
    assert runtime["ok"] is True
    assert runtime["implementation_directory"] == "src/pyAppGen/pbcs/eam"
    assert len(runtime["standard_features"]) >= 25
    assert "rule_engine" in runtime["standard_features"]
    assert "parameter_engine" in runtime["standard_features"]
    assert "configuration_schema" in runtime["standard_features"]
    assert "workbench" in runtime["standard_features"]
    assert smoke["ok"] is True
    assert set(EAM_ADVANCED_CAPABILITY_KEYS) == {check["id"] for check in smoke["checks"]}
    assert not smoke["blocking_gaps"]

    contract = pbc_implementation_contract("eam")
    assert contract["source_package"]["ok"] is True
    assert contract["advanced_runtime"]["ok"] is True
    assert contract["source_package"]["ui_contract"]["ok"] is True
    assert "MaintenanceConfigurationPanel" in contract["source_package"]["ui_contract"]["fragments"]
    assert set(contract["advanced_runtime"]["capabilities"]) == set(EAM_ADVANCED_CAPABILITY_KEYS)
    assert pbc_implementation_release_audit(("eam",))["ok"] is True
    assert pbc_implemented_capability_audit(("eam",))["ok"] is True


def test_eam_runtime_applies_rules_parameters_configuration_and_ui() -> None:
    state = eam_empty_state()
    state = eam_configure_runtime(
        state,
        {
            "database_backend": "postgresql",
            "event_topic": "appgen.maintenance.events",
            "retry_limit": 3,
            "allowed_sites": ("plant_ops",),
            "allowed_priorities": ("low", "medium", "high", "critical"),
            "allowed_work_types": ("preventive", "predictive", "corrective"),
            "allowed_permit_types": ("electrical",),
            "default_timezone": "UTC",
            "workbench_limit": 50,
        },
    )["state"]
    state = eam_set_parameter(state, "default_pm_interval_days", 30)["state"]
    state = eam_set_parameter(state, "failure_risk_threshold", 0.65)["state"]
    state = eam_set_parameter(state, "mttr_target_hours", 6)["state"]
    state = eam_set_parameter(state, "criticality_weight", 0.4)["state"]
    state = eam_set_parameter(state, "safety_risk_threshold", 0.7)["state"]
    state = eam_register_rule(
        state,
        {
            "rule_id": "rule_ops",
            "tenant": "tenant_ops",
            "rule_type": "maintenance",
            "eligible_work_types": ("preventive", "predictive", "corrective"),
            "allowed_sites": ("plant_ops",),
            "criticality_classes": ("A", "B"),
            "required_permits": ("electrical",),
            "failure_codes": ("bearing", "overheat"),
            "status": "active",
        },
    )["state"]
    equipment = eam_register_equipment(
        state,
        {
            "equipment_id": "eq_ops",
            "tenant": "tenant_ops",
            "site": "plant_ops",
            "asset_tag": "compressor_ops",
            "criticality": "A",
            "location": "line_ops",
            "parent_equipment_id": None,
            "warranty_until": "2027-12-31",
        },
    )
    state = equipment["state"]
    assert equipment["equipment"]["status"] == "active"

    plan = eam_create_maintenance_plan(
        state,
        {
            "plan_id": "plan_ops",
            "tenant": "tenant_ops",
            "equipment_id": "eq_ops",
            "strategy": "predictive",
            "interval_days": 30,
            "meter_threshold": 500,
            "condition_threshold": 0.7,
            "status": "released",
        },
    )
    state = plan["state"]
    assert plan["maintenance_plan"]["status"] == "active"

    condition = eam_record_condition_reading(
        state,
        {
            "reading_id": "cond_ops",
            "tenant": "tenant_ops",
            "equipment_id": "eq_ops",
            "sensor": "vibration",
            "value": 0.8,
            "unit": "ips",
            "captured_at": "2026-05-26T08:00:00Z",
        },
    )
    state = condition["state"]
    assert condition["condition_reading"]["alarm"] is True

    meter = eam_record_meter_reading(
        state,
        {"meter_id": "meter_ops", "tenant": "tenant_ops", "equipment_id": "eq_ops", "meter_name": "runtime_hours", "value": 560, "unit": "hours"},
    )
    state = meter["state"]
    assert meter["meter_reading"]["triggered_plans"] == ("plan_ops",)

    permit = eam_create_safety_permit(
        state,
        {"permit_id": "permit_ops", "tenant": "tenant_ops", "equipment_id": "eq_ops", "permit_type": "electrical", "risk_score": 0.6, "approved_by": "safety_ops"},
    )
    state = permit["state"]
    assert permit["permit"]["status"] == "approved"

    work_order = eam_create_work_order(
        state,
        {
            "work_order_id": "wo_ops",
            "tenant": "tenant_ops",
            "equipment_id": "eq_ops",
            "plan_id": "plan_ops",
            "work_type": "predictive",
            "priority": "critical",
            "failure_code": "bearing",
            "estimated_hours": 4,
            "required_skill": "mechanic",
            "permit_id": "permit_ops",
        },
    )
    state = work_order["state"]
    assert work_order["work_order"]["status"] == "planned"

    scheduled = eam_schedule_work_order(
        state,
        "wo_ops",
        window={"start": "2026-05-27T02:00:00Z", "carbon": 80},
        technician="tech_ops",
    )
    state = scheduled["state"]
    assert scheduled["work_order"]["status"] == "scheduled"

    spare = eam_issue_spare_part(
        state,
        {"usage_id": "spare_ops", "tenant": "tenant_ops", "work_order_id": "wo_ops", "part_number": "bearing_kit", "quantity": 2, "unit_cost": 125},
    )
    state = spare["state"]
    assert spare["cost"] == 250

    complete = eam_complete_work_order(
        state,
        "wo_ops",
        completed_by="tech_ops",
        actual_hours=5,
        downtime_hours=3,
        resolution="bearing_replaced",
    )
    state = complete["state"]
    assert complete["work_order"]["status"] == "completed"
    assert complete["handoffs"] == (
        "production_uptime_projection",
        "inventory_spares_projection",
        "procurement_vendor_projection",
        "quality_reliability_projection",
    )
    assert state["outbox"][-1]["idempotency_key"] == "eam:MaintenanceCompleted:eam_evt_000009"

    workbench = eam_build_workbench_view(state, tenant="tenant_ops")
    assert workbench["equipment_count"] == 1
    assert workbench["plan_count"] == 1
    assert workbench["work_order_count"] == 1
    assert workbench["completed_work_order_count"] == 1
    assert workbench["critical_work_order_count"] == 1
    assert workbench["spare_cost"] == 250

    ui_contract = eam_ui_contract()
    assert ui_contract["configuration_editor"]["allowed_database_backends"] == ("postgresql", "mysql", "mariadb")
    assert "failure_risk_threshold" in ui_contract["parameter_editor"]["numeric_parameters"]
    assert "rule_id" in ui_contract["rule_editor"]["required_fields"]
    rendered = eam_render_workbench(
        state,
        tenant="tenant_ops",
        principal_permissions=(
            "eam.equipment",
            "eam.plan",
            "eam.execute",
            "eam.safety",
            "eam.configure",
            "eam.audit",
        ),
    )
    assert rendered["ok"] is True
    assert rendered["configuration_bound"] is True
    assert rendered["event_outbox_count"] == 9
    assert set(rendered["visible_actions"]) == set(ui_contract["action_permissions"])
    assert not rendered["locked_actions"]
