"""Payroll Engine PBC implementation package."""

from .manifest import PBC_MANIFEST

from ..source_contract import source_pbc_package_contract
from ..source_contract import source_registration_plan
from .runtime import PAYROLL_ENGINE_ALLOWED_DATABASE_BACKENDS
from .runtime import PAYROLL_ENGINE_CONSUMED_EVENT_TYPES
from .runtime import PAYROLL_ENGINE_EMITTED_EVENT_TYPES
from .runtime import PAYROLL_ENGINE_OWNED_TABLES
from .runtime import PAYROLL_ENGINE_REQUIRED_EVENT_TOPIC
from .runtime import PAYROLL_ENGINE_RUNTIME_CAPABILITY_KEYS
from .runtime import PAYROLL_ENGINE_STANDARD_FEATURE_KEYS
from .runtime import payroll_engine_allocate_benefit
from .runtime import payroll_engine_apply_deduction
from .runtime import payroll_engine_build_api_contract
from .runtime import payroll_engine_build_release_evidence
from .runtime import payroll_engine_build_schema_contract
from .runtime import payroll_engine_build_service_contract
from .runtime import payroll_engine_build_workbench_view
from .runtime import payroll_engine_calculate_payslip
from .runtime import payroll_engine_configure_runtime
from .runtime import payroll_engine_create_payroll_run
from .runtime import payroll_engine_empty_state
from .runtime import payroll_engine_ingest_labor_hours
from .runtime import payroll_engine_post_payroll_run
from .runtime import payroll_engine_prepare_payroll_filing
from .runtime import payroll_engine_permissions_contract
from .runtime import payroll_engine_receive_event
from .runtime import payroll_engine_register_rule
from .runtime import payroll_engine_register_schema_extension
from .runtime import payroll_engine_runtime_capabilities
from .runtime import payroll_engine_runtime_smoke
from .runtime import payroll_engine_set_parameter
from .runtime import payroll_engine_upsert_worker_projection
from .runtime import payroll_engine_verify_owned_table_boundary
from .ui import PAYROLL_ENGINE_UI_FRAGMENT_KEYS
from .ui import payroll_engine_render_workbench
from .ui import payroll_engine_ui_contract

PBC_KEY = "payroll_engine"


def implementation_contract() -> dict:
    runtime = payroll_engine_runtime_capabilities()
    contract = source_pbc_package_contract(PBC_KEY, tuple(runtime["capabilities"]))
    return {
        **contract,
        "standard_features": runtime["standard_features"],
        "advanced_runtime": runtime,
        "ui_contract": payroll_engine_ui_contract(),
        "api_contract": payroll_engine_build_api_contract(),
        "schema_contract": payroll_engine_build_schema_contract(),
        "service_contract": payroll_engine_build_service_contract(),
        "release_evidence_contract": payroll_engine_build_release_evidence(),
        "permissions_contract": payroll_engine_permissions_contract(),
        "owned_tables": PAYROLL_ENGINE_OWNED_TABLES,
        "allowed_database_backends": PAYROLL_ENGINE_ALLOWED_DATABASE_BACKENDS,
        "required_event_topic": PAYROLL_ENGINE_REQUIRED_EVENT_TOPIC,
        "consumes": PAYROLL_ENGINE_CONSUMED_EVENT_TYPES,
        "emits": PAYROLL_ENGINE_EMITTED_EVENT_TYPES,
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
