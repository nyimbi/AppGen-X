"""Payment Orchestration PBC implementation package."""

from .manifest import PBC_MANIFEST

from ..source_contract import source_pbc_package_contract
from ..source_contract import source_package_metadata
from ..source_contract import validate_source_package_metadata
from ..source_contract import source_registration_plan
from .runtime import PAYMENT_ORCHESTRATION_ALLOWED_DATABASE_BACKENDS
from .runtime import PAYMENT_ORCHESTRATION_CONSUMED_EVENT_TYPES
from .runtime import PAYMENT_ORCHESTRATION_EMITTED_EVENT_TYPES
from .runtime import PAYMENT_ORCHESTRATION_OWNED_TABLES
from .runtime import PAYMENT_ORCHESTRATION_REQUIRED_EVENT_TOPIC
from .runtime import PAYMENT_ORCHESTRATION_RUNTIME_CAPABILITY_KEYS
from .runtime import PAYMENT_ORCHESTRATION_STANDARD_FEATURE_KEYS
from .runtime import payment_orchestration_build_api_contract
from .runtime import payment_orchestration_build_release_evidence
from .runtime import payment_orchestration_build_schema_contract
from .runtime import payment_orchestration_build_service_contract
from .runtime import payment_orchestration_build_workbench_view
from .runtime import payment_orchestration_authorize_payment
from .runtime import payment_orchestration_capture_payment
from .runtime import payment_orchestration_configure_runtime
from .runtime import payment_orchestration_create_payment_intent
from .runtime import payment_orchestration_empty_state
from .runtime import payment_orchestration_open_dispute
from .runtime import payment_orchestration_permissions_contract
from .runtime import payment_orchestration_receive_event
from .runtime import payment_orchestration_refund_payment
from .runtime import payment_orchestration_register_gateway
from .runtime import payment_orchestration_register_rule
from .runtime import payment_orchestration_register_schema_extension
from .runtime import payment_orchestration_request_fraud_check
from .runtime import payment_orchestration_resolve_dispute
from .runtime import payment_orchestration_route_gateway
from .runtime import payment_orchestration_runtime_capabilities
from .runtime import payment_orchestration_runtime_smoke
from .runtime import payment_orchestration_schedule_payout
from .runtime import payment_orchestration_set_parameter
from .runtime import payment_orchestration_settle_payment
from .runtime import payment_orchestration_tokenize_payment_method
from .runtime import payment_orchestration_verify_owned_table_boundary
from .runtime import payment_orchestration_void_payment
from .ui import PAYMENT_ORCHESTRATION_UI_FRAGMENT_KEYS
from .ui import payment_orchestration_render_workbench
from .ui import payment_orchestration_ui_contract

PBC_KEY = "payment_orchestration"


def implementation_contract() -> dict:
    runtime = payment_orchestration_runtime_capabilities()
    contract = source_pbc_package_contract(PBC_KEY, tuple(runtime["capabilities"]))
    return {
        **contract,
        "standard_features": runtime["standard_features"],
        "advanced_runtime": runtime,
        "ui_contract": payment_orchestration_ui_contract(),
        "api_contract": payment_orchestration_build_api_contract(),
        "schema_contract": payment_orchestration_build_schema_contract(),
        "service_contract": payment_orchestration_build_service_contract(),
        "release_evidence_contract": payment_orchestration_build_release_evidence(),
        "permissions_contract": payment_orchestration_permissions_contract(),
        "owned_tables": PAYMENT_ORCHESTRATION_OWNED_TABLES,
        "allowed_database_backends": PAYMENT_ORCHESTRATION_ALLOWED_DATABASE_BACKENDS,
        "required_event_topic": PAYMENT_ORCHESTRATION_REQUIRED_EVENT_TOPIC,
        "consumes": PAYMENT_ORCHESTRATION_CONSUMED_EVENT_TYPES,
        "emits": PAYMENT_ORCHESTRATION_EMITTED_EVENT_TYPES,
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


def package_metadata_manifest() -> dict:
    """Return package identity, artifacts, and discovery metadata."""
    return source_package_metadata(PBC_KEY, register_pbc(), implementation_contract())


def validate_package_metadata() -> dict:
    """Validate package metadata without mutating catalog state."""
    return validate_source_package_metadata(package_metadata_manifest())


def package_discovery_plan(existing_catalog: dict | None = None) -> dict:
    """Return side-effect-free package discovery and registration evidence."""
    metadata_validation = validate_package_metadata()
    registration = registration_plan(existing_catalog=existing_catalog)
    return {
        "format": "appgen.pbc-source-package-discovery-plan.v1",
        "ok": metadata_validation["ok"] and registration["ok"],
        "pbc": PBC_KEY,
        "metadata_validation": metadata_validation,
        "registration": registration,
        "side_effects": (),
    }


def smoke_test() -> dict:
    """Exercise package metadata validation and discovery planning."""
    discovery = package_discovery_plan()
    return {
        "ok": discovery["ok"],
        "discovery": discovery,
        "side_effects": (),
    }
