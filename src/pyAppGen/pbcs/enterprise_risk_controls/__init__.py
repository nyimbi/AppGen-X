"""Enterprise Risk and Controls PBC implementation package."""

from .manifest import PBC_MANIFEST
from ..source_contract import source_pbc_package_contract
from ..source_contract import source_package_metadata
from ..source_contract import source_registration_plan
from ..source_contract import validate_source_package_metadata
from .agent import enterprise_risk_controls_assistant_preview
from .controls import enterprise_risk_controls_control_catalog
from .controls import enterprise_risk_controls_control_center
from .events import CONSUMED as PACKAGE_CONSUMED_EVENTS
from .events import EMITTED as PACKAGE_EMITTED_EVENTS
from .forms import enterprise_risk_controls_form_catalog
from .permissions import permission_manifest
from .release_evidence import build_release_evidence as package_release_evidence
from .routes import api_route_contracts as package_api_contract
from .runtime import *
from .service_contract import build_service_contract as package_service_contract
from .ui import enterprise_risk_controls_render_workbench
from .ui import enterprise_risk_controls_ui_contract
from .wizards import enterprise_risk_controls_wizard_catalog

PBC_KEY = "enterprise_risk_controls"


def implementation_contract() -> dict:
    runtime = enterprise_risk_controls_runtime_capabilities()
    contract = source_pbc_package_contract(PBC_KEY, tuple(runtime["capabilities"]))
    return {
        **contract,
        "standard_features": runtime["standard_features"],
        "advanced_runtime": runtime,
        "ui_contract": enterprise_risk_controls_ui_contract(),
        "api_contract": package_api_contract(),
        "schema_contract": enterprise_risk_controls_build_schema_contract(),
        "service_contract": package_service_contract(),
        "release_evidence_contract": package_release_evidence(),
        "permissions_contract": permission_manifest(),
        "forms": enterprise_risk_controls_form_catalog(),
        "wizards": enterprise_risk_controls_wizard_catalog(),
        "controls": enterprise_risk_controls_control_catalog(),
        "control_center": enterprise_risk_controls_control_center(),
        "assistant_preview": enterprise_risk_controls_assistant_preview(
            {
                "document_text": "Review the evidence retention policy.",
                "instructions": "Read the risk runtime parameter and summarize the impact.",
                "target_entity": "risk_runtime_parameter",
                "requested_action": "read",
            }
        ),
        "owned_tables": ENTERPRISE_RISK_CONTROLS_OWNED_TABLES,
        "runtime_tables": ENTERPRISE_RISK_CONTROLS_RUNTIME_TABLES,
        "allowed_database_backends": ENTERPRISE_RISK_CONTROLS_ALLOWED_DATABASE_BACKENDS,
        "required_event_topic": ENTERPRISE_RISK_CONTROLS_REQUIRED_EVENT_TOPIC,
        "emits": PACKAGE_EMITTED_EVENTS,
        "consumes": PACKAGE_CONSUMED_EVENTS,
        "boundary_contract": enterprise_risk_controls_verify_owned_table_boundary(
            ENTERPRISE_RISK_CONTROLS_OWNED_TABLES + ("PolicyChanged", "projection_dependency")
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
    runtime = enterprise_risk_controls_runtime_smoke()
    return {
        "ok": discovery["ok"] and runtime["ok"],
        "discovery": discovery,
        "runtime": runtime,
        "side_effects": (),
    }
