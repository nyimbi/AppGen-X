"""Clinical Trials Management PBC implementation package."""

from .agent import composed_agent_contribution
from .controls import clinical_trials_management_control_catalog
from .forms import clinical_trials_management_form_catalog
from .manifest import PBC_MANIFEST
from .runtime import *
from .ui import clinical_trials_management_render_workbench
from .ui import clinical_trials_management_ui_contract
from .wizards import clinical_trials_management_wizard_catalog
from ..source_contract import source_package_metadata
from ..source_contract import source_pbc_package_contract
from ..source_contract import source_registration_plan
from ..source_contract import validate_source_package_metadata

PBC_KEY = "clinical_trials_management"


def implementation_contract() -> dict:
    runtime = clinical_trials_management_runtime_capabilities()
    contract = source_pbc_package_contract(PBC_KEY, tuple(runtime["capabilities"]))
    return {
        **contract,
        "standard_features": runtime["standard_features"],
        "advanced_runtime": runtime,
        "ui_contract": clinical_trials_management_ui_contract(),
        "api_contract": clinical_trials_management_build_api_contract(),
        "schema_contract": clinical_trials_management_build_schema_contract(),
        "service_contract": clinical_trials_management_build_service_contract(),
        "release_evidence_contract": clinical_trials_management_build_release_evidence(),
        "permissions_contract": clinical_trials_management_permissions_contract(),
        "owned_tables": CLINICAL_TRIALS_MANAGEMENT_OWNED_TABLES,
        "runtime_tables": CLINICAL_TRIALS_MANAGEMENT_RUNTIME_TABLES,
        "allowed_database_backends": CLINICAL_TRIALS_MANAGEMENT_ALLOWED_DATABASE_BACKENDS,
        "required_event_topic": CLINICAL_TRIALS_MANAGEMENT_REQUIRED_EVENT_TOPIC,
        "emits": CLINICAL_TRIALS_MANAGEMENT_EMITTED_EVENT_TYPES,
        "consumes": CLINICAL_TRIALS_MANAGEMENT_CONSUMED_EVENT_TYPES,
        "boundary_contract": clinical_trials_management_verify_owned_table_boundary(("trial_protocol", "study_site", "subject")),
        "forms_contract": clinical_trials_management_form_catalog(),
        "wizard_contract": clinical_trials_management_wizard_catalog(),
        "control_contract": clinical_trials_management_control_catalog(),
        "assistant_contract": composed_agent_contribution(),
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
    runtime = clinical_trials_management_runtime_smoke()
    return {"ok": discovery["ok"] and runtime["ok"], "discovery": discovery, "runtime": runtime, "side_effects": ()}
