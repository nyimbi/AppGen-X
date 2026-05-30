"""Nonprofit Program Impact PBC implementation package."""

from .agent import composed_agent_contribution
from .controls import nonprofit_program_impact_control_catalog
from .controls import nonprofit_program_impact_control_center
from .forms import nonprofit_program_impact_form_catalog
from .manifest import PBC_MANIFEST
from .runtime import *
from .standalone import nonprofit_program_impact_bootstrap_standalone_app
from .standalone import nonprofit_program_impact_standalone_app_contract
from .standalone import nonprofit_program_impact_standalone_app_smoke
from .ui import nonprofit_program_impact_render_workbench
from .ui import nonprofit_program_impact_ui_contract
from .wizards import nonprofit_program_impact_wizard_catalog
from ..source_contract import source_package_metadata
from ..source_contract import source_pbc_package_contract
from ..source_contract import source_registration_plan
from ..source_contract import validate_source_package_metadata

PBC_KEY = "nonprofit_program_impact"


def implementation_contract() -> dict:
    runtime = nonprofit_program_impact_runtime_capabilities()
    contract = source_pbc_package_contract(PBC_KEY, tuple(runtime["capabilities"]))
    return {
        **contract,
        "standard_features": runtime["standard_features"],
        "advanced_runtime": runtime,
        "ui_contract": nonprofit_program_impact_ui_contract(),
        "api_contract": nonprofit_program_impact_build_api_contract(),
        "schema_contract": nonprofit_program_impact_build_schema_contract(),
        "service_contract": nonprofit_program_impact_build_service_contract(),
        "release_evidence_contract": nonprofit_program_impact_build_release_evidence(),
        "permissions_contract": nonprofit_program_impact_permissions_contract(),
        "forms_contract": nonprofit_program_impact_form_catalog(),
        "wizard_contract": nonprofit_program_impact_wizard_catalog(),
        "control_contract": nonprofit_program_impact_control_catalog(),
        "control_center": nonprofit_program_impact_control_center(),
        "assistant_contract": composed_agent_contribution(),
        "standalone_app_contract": nonprofit_program_impact_standalone_app_contract(),
        "owned_tables": NONPROFIT_PROGRAM_IMPACT_OWNED_TABLES,
        "runtime_tables": NONPROFIT_PROGRAM_IMPACT_RUNTIME_TABLES,
        "allowed_database_backends": NONPROFIT_PROGRAM_IMPACT_ALLOWED_DATABASE_BACKENDS,
        "required_event_topic": NONPROFIT_PROGRAM_IMPACT_REQUIRED_EVENT_TOPIC,
        "emits": NONPROFIT_PROGRAM_IMPACT_EMITTED_EVENT_TYPES,
        "consumes": NONPROFIT_PROGRAM_IMPACT_CONSUMED_EVENT_TYPES,
        "boundary_contract": nonprofit_program_impact_verify_owned_table_boundary(
            ("program", "beneficiary", "service_episode", "outcome_measure", "impact_evidence", "donor_report")
        ),
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
    runtime = nonprofit_program_impact_runtime_smoke()
    standalone = nonprofit_program_impact_standalone_app_smoke()
    return {
        "ok": discovery["ok"] and runtime["ok"] and standalone["ok"],
        "discovery": discovery,
        "runtime": runtime,
        "standalone": standalone,
        "side_effects": (),
    }
