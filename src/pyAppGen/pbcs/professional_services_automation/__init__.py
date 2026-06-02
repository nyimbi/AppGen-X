"""Professional Services Automation PBC implementation package."""

from . import release_evidence as release_evidence
from . import standalone as standalone
from .manifest import PBC_MANIFEST

from ..source_contract import source_pbc_package_contract
from ..source_contract import source_package_metadata
from ..source_contract import source_registration_plan
from ..source_contract import validate_source_package_metadata
from .controls import professional_services_automation_control_catalog
from .forms import professional_services_automation_form_catalog
from .release_evidence import build_release_evidence as package_build_release_evidence
from .runtime import *
from .standalone import ProfessionalServicesAutomationStandaloneApp
from .standalone import bootstrap_standalone_state
from .standalone import professional_services_automation_standalone_app_contract
from .standalone import professional_services_automation_standalone_workflow_catalog
from .standalone import validate_standalone_application
from .ui import professional_services_automation_render_standalone_app
from .ui import professional_services_automation_render_workbench
from .ui import professional_services_automation_standalone_app_contract as professional_services_automation_ui_standalone_app_contract
from .ui import professional_services_automation_ui_contract
from .wizards import professional_services_automation_wizard_catalog

professional_services_automation_build_release_evidence = package_build_release_evidence

PBC_KEY = "professional_services_automation"



def implementation_contract() -> dict:
    runtime = professional_services_automation_runtime_capabilities()
    contract = source_pbc_package_contract(PBC_KEY, tuple(runtime["capabilities"]))
    return {
        **contract,
        "standard_features": runtime["standard_features"],
        "advanced_runtime": runtime,
        "ui_contract": professional_services_automation_ui_contract(),
        "api_contract": professional_services_automation_build_api_contract(),
        "schema_contract": professional_services_automation_build_schema_contract(),
        "service_contract": professional_services_automation_build_service_contract(),
        "release_evidence_contract": package_build_release_evidence(),
        "permissions_contract": professional_services_automation_permissions_contract(),
        "owned_tables": PROFESSIONAL_SERVICES_AUTOMATION_OWNED_TABLES,
        "runtime_tables": PROFESSIONAL_SERVICES_AUTOMATION_RUNTIME_TABLES,
        "allowed_database_backends": PROFESSIONAL_SERVICES_AUTOMATION_ALLOWED_DATABASE_BACKENDS,
        "required_event_topic": PROFESSIONAL_SERVICES_AUTOMATION_REQUIRED_EVENT_TOPIC,
        "emits": PROFESSIONAL_SERVICES_AUTOMATION_EMITTED_EVENT_TYPES,
        "consumes": PROFESSIONAL_SERVICES_AUTOMATION_CONSUMED_EVENT_TYPES,
        "boundary_contract": professional_services_automation_verify_owned_table_boundary(
            PROFESSIONAL_SERVICES_AUTOMATION_OWNED_TABLES + ("api_dependency",)
        ),
        "forms": professional_services_automation_form_catalog(),
        "wizards": professional_services_automation_wizard_catalog(),
        "controls": professional_services_automation_control_catalog(),
        "standalone_app_contract": professional_services_automation_standalone_app_contract(),
        "standalone_ui_shell": professional_services_automation_ui_standalone_app_contract(),
        "standalone_workflows": professional_services_automation_standalone_workflow_catalog(),
        "standalone_validation": validate_standalone_application(),
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
    runtime = professional_services_automation_runtime_smoke()
    standalone_validation = validate_standalone_application()
    return {
        "ok": discovery["ok"] and runtime["ok"] and standalone_validation["ok"],
        "discovery": discovery,
        "runtime": runtime,
        "standalone": standalone_validation,
        "side_effects": (),
    }
