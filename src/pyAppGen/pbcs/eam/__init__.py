"""Enterprise Asset Management PBC implementation package."""

from .manifest import PBC_MANIFEST

from ..source_contract import source_pbc_package_contract
from ..source_contract import source_registration_plan
from .runtime import EAM_ALLOWED_DATABASE_BACKENDS
from .runtime import EAM_CONSUMED_EVENT_TYPES
from .runtime import EAM_EMITTED_EVENT_TYPES
from .runtime import EAM_OWNED_TABLES
from .runtime import EAM_REQUIRED_RULE_FIELDS
from .runtime import EAM_REQUIRED_EVENT_TOPIC
from .runtime import EAM_RUNTIME_CAPABILITY_KEYS
from .runtime import EAM_STANDARD_FEATURE_KEYS
from .runtime import eam_build_api_contract
from .runtime import eam_build_release_evidence
from .runtime import eam_build_schema_contract
from .runtime import eam_build_service_contract
from .runtime import eam_build_workbench_view
from .runtime import eam_complete_work_order
from .runtime import eam_configure_runtime
from .runtime import eam_create_maintenance_plan
from .runtime import eam_create_safety_permit
from .runtime import eam_create_work_order
from .runtime import eam_empty_state
from .runtime import eam_issue_spare_part
from .runtime import eam_generate_compliance_proof
from .runtime import eam_allocate_labor_and_spares
from .runtime import eam_detect_failure_anomaly
from .runtime import eam_federate_maintenance_view
from .runtime import eam_forecast_failures
from .runtime import eam_model_stochastic_maintenance_exposure
from .runtime import eam_optimize_maintenance_schedule
from .runtime import eam_parse_maintenance_instruction
from .runtime import eam_permissions_contract
from .runtime import eam_recommend_exception_resolution
from .runtime import eam_record_condition_reading
from .runtime import eam_record_meter_reading
from .runtime import eam_receive_event
from .runtime import eam_register_equipment
from .runtime import eam_register_governed_model
from .runtime import eam_register_rule
from .runtime import eam_register_schema_extension
from .runtime import eam_rotate_crypto_epoch
from .runtime import eam_route_maintenance
from .runtime import eam_run_control_tests
from .runtime import eam_run_resilience_drill
from .runtime import eam_runtime_capabilities
from .runtime import eam_runtime_smoke
from .runtime import eam_schedule_work_order
from .runtime import eam_schedule_carbon_aware_maintenance
from .runtime import eam_score_maintenance_risk
from .runtime import eam_screen_policy
from .runtime import eam_set_parameter
from .runtime import eam_simulate_strategy
from .runtime import eam_verify_owned_table_boundary
from .runtime import eam_verify_equipment_identity
from .ui import EAM_UI_FRAGMENT_KEYS
from .ui import eam_render_workbench
from .ui import eam_ui_contract

PBC_KEY = "eam"


def implementation_contract() -> dict:
    runtime = eam_runtime_capabilities()
    contract = source_pbc_package_contract(PBC_KEY, tuple(runtime["capabilities"]))
    return {
        **contract,
        "standard_features": runtime["standard_features"],
        "owned_tables": EAM_OWNED_TABLES,
        "allowed_database_backends": EAM_ALLOWED_DATABASE_BACKENDS,
        "api_contract": eam_build_api_contract(),
        "schema_contract": eam_build_schema_contract(),
        "service_contract": eam_build_service_contract(),
        "release_evidence_contract": eam_build_release_evidence(),
        "permissions_contract": eam_permissions_contract(),
        "required_event_topic": EAM_REQUIRED_EVENT_TOPIC,
        "consumes": EAM_CONSUMED_EVENT_TYPES,
        "emits": EAM_EMITTED_EVENT_TYPES,
        "advanced_runtime": runtime,
        "ui_contract": eam_ui_contract(),
    }


def register_pbc() -> dict:
    """Return this PBC manifest without mutating global catalog state."""
    return dict(PBC_MANIFEST)


def registration_plan(existing_catalog: dict | None = None) -> dict:
    """Return a side-effect-free registration plan for this PBC package."""
    return source_registration_plan(
        PBC_KEY,
        register_pbc(),
        existing_catalog=existing_catalog,
    )
