"""Port Terminal Operations PBC implementation package."""

from .manifest import PBC_MANIFEST
from ..source_contract import source_package_metadata
from ..source_contract import source_pbc_package_contract
from ..source_contract import source_registration_plan
from ..source_contract import validate_source_package_metadata
from .controls import port_terminal_operations_control_catalog
from .forms import port_terminal_operations_form_contracts
from .release_evidence import build_release_evidence
from .release_evidence import release_readiness_manifest
from .release_evidence import validate_release_evidence
from .runtime import *
from .ui import port_terminal_operations_render_standalone_workbench
from .ui import port_terminal_operations_render_workbench
from .ui import port_terminal_operations_standalone_workbench_blueprint
from .ui import port_terminal_operations_ui_contract
from .standalone import dispatch_standalone_route
from .standalone import port_terminal_operations_bootstrap_standalone_app
from .standalone import port_terminal_operations_standalone_app_contract
from .standalone import port_terminal_operations_standalone_app_smoke
from .wizards import port_terminal_operations_wizard_contracts

PBC_KEY = "port_terminal_operations"


def implementation_contract() -> dict:
    runtime = port_terminal_operations_runtime_capabilities()
    contract = source_pbc_package_contract(PBC_KEY, tuple(runtime["capabilities"]))
    return {
        **contract,
        "standard_features": runtime["standard_features"],
        "advanced_runtime": runtime,
        "ui_contract": port_terminal_operations_ui_contract(),
        "api_contract": port_terminal_operations_build_api_contract(),
        "schema_contract": port_terminal_operations_build_schema_contract(),
        "service_contract": port_terminal_operations_build_service_contract(),
        "release_evidence_contract": build_release_evidence(),
        "permissions_contract": port_terminal_operations_permissions_contract(),
        "owned_tables": PORT_TERMINAL_OPERATIONS_OWNED_TABLES,
        "runtime_tables": PORT_TERMINAL_OPERATIONS_RUNTIME_TABLES,
        "allowed_database_backends": PORT_TERMINAL_OPERATIONS_ALLOWED_DATABASE_BACKENDS,
        "required_event_topic": PORT_TERMINAL_OPERATIONS_REQUIRED_EVENT_TOPIC,
        "emits": PORT_TERMINAL_OPERATIONS_EMITTED_EVENT_TYPES,
        "consumes": PORT_TERMINAL_OPERATIONS_CONSUMED_EVENT_TYPES,
        "boundary_contract": port_terminal_operations_verify_owned_table_boundary(PORT_TERMINAL_OPERATIONS_OWNED_TABLES),
        "standalone_app_contract": port_terminal_operations_standalone_app_contract(),
    }


def register_pbc() -> dict:
    return dict(PBC_MANIFEST)


def registration_plan(existing_catalog: dict | None = None) -> dict:
    return source_registration_plan(PBC_KEY, register_pbc(), existing_catalog=existing_catalog)


def package_metadata_manifest() -> dict:
    return source_package_metadata(PBC_KEY, register_pbc(), implementation_contract())


def validate_package_metadata() -> dict:
    return validate_source_package_metadata(package_metadata_manifest())


def package_discovery_plan(existing_catalog: dict | None = None) -> dict:
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
    discovery = package_discovery_plan()
    runtime = port_terminal_operations_runtime_smoke()
    standalone = port_terminal_operations_standalone_app_smoke()
    release = validate_release_evidence()
    return {
        "ok": discovery["ok"] and runtime["ok"] and standalone["ok"] and release["ok"],
        "discovery": discovery,
        "runtime": runtime,
        "standalone": standalone,
        "release": release,
        "side_effects": (),
    }
