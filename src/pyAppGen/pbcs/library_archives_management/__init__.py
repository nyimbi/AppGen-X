"""Library and Archives Management PBC implementation package."""

from __future__ import annotations

from ..source_contract import source_package_metadata
from ..source_contract import source_pbc_package_contract
from ..source_contract import source_registration_plan
from ..source_contract import validate_source_package_metadata
from .controls import library_archives_management_control_catalog
from .forms import library_archives_management_form_catalog
from .manifest import PBC_MANIFEST
from .release_evidence import build_release_evidence as library_archives_management_release_evidence
from .runtime import *
from .standalone import library_archives_management_standalone_app_contract
from .ui import library_archives_management_render_workbench
from .ui import library_archives_management_ui_contract
from .wizards import library_archives_management_wizard_catalog

PBC_KEY = "library_archives_management"



def implementation_contract() -> dict:
    runtime = library_archives_management_runtime_capabilities()
    forms = library_archives_management_form_catalog()
    wizards = library_archives_management_wizard_catalog()
    controls = library_archives_management_control_catalog()
    standalone = library_archives_management_standalone_app_contract()
    contract = source_pbc_package_contract(PBC_KEY, tuple(runtime["capabilities"]))
    return {
        **contract,
        "standard_features": runtime["standard_features"],
        "advanced_runtime": runtime,
        "ui_contract": library_archives_management_ui_contract(),
        "api_contract": library_archives_management_build_api_contract(),
        "schema_contract": library_archives_management_build_schema_contract(),
        "service_contract": library_archives_management_build_service_contract(),
        "release_evidence_contract": library_archives_management_release_evidence(),
        "permissions_contract": library_archives_management_permissions_contract(),
        "forms_contract": forms,
        "wizards_contract": wizards,
        "controls_contract": controls,
        "standalone_contract": standalone,
        "owned_tables": LIBRARY_ARCHIVES_MANAGEMENT_OWNED_TABLES,
        "runtime_tables": LIBRARY_ARCHIVES_MANAGEMENT_RUNTIME_TABLES,
        "allowed_database_backends": LIBRARY_ARCHIVES_MANAGEMENT_ALLOWED_DATABASE_BACKENDS,
        "required_event_topic": LIBRARY_ARCHIVES_MANAGEMENT_REQUIRED_EVENT_TOPIC,
        "emits": LIBRARY_ARCHIVES_MANAGEMENT_EMITTED_EVENT_TYPES,
        "consumes": LIBRARY_ARCHIVES_MANAGEMENT_CONSUMED_EVENT_TYPES,
        "boundary_contract": library_archives_management_verify_owned_table_boundary(
            LIBRARY_ARCHIVES_MANAGEMENT_OWNED_TABLES + ("api_dependency",)
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
    runtime = library_archives_management_runtime_smoke()
    standalone = library_archives_management_standalone_app_contract()
    return {
        "ok": discovery["ok"] and runtime["ok"] and standalone["ok"],
        "discovery": discovery,
        "runtime": runtime,
        "standalone": standalone,
        "side_effects": (),
    }
