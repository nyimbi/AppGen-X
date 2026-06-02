"""Release evidence for the data_product_catalog PBC."""
from __future__ import annotations

from pathlib import Path

from .agent import agent_skill_manifest, chatbot_interface_contract
from .blueprint import EXPECTED_ARTIFACT_FILES, OWNED_TABLES, PBC_KEY
from .capability_assurance import validate_table_stakes_capability_coverage
from .config import configuration_manifest, governance_smoke_test, parameter_manifest, rule_manifest
from .domain_depth import domain_depth_contract, domain_depth_smoke_test
from .events import event_contract_manifest, validate_event_contract
from .handlers import handler_manifest
from .permissions import permission_manifest
from .routes import api_route_contracts, validate_api_route_contracts
from .schema_contract import build_schema_contract
from .seed_data import seed_plan, validate_seed_data
from .service_contract import build_service_contract
from .services import service_operation_contracts
from .ui import data_product_catalog_ui_contract

PACKAGE_DIR = Path(__file__).resolve().parent


def pbc_source_artifact_contract() -> dict:
    missing_files = tuple(path for path in EXPECTED_ARTIFACT_FILES if not (PACKAGE_DIR / path).exists())
    schema = build_schema_contract()
    service = build_service_contract()
    routes = api_route_contracts()
    return {
        "ok": not missing_files and schema["ok"] and service["ok"] and routes["ok"],
        "gate": "pbc_source_artifact_contract",
        "pbc": PBC_KEY,
        "expected_files": EXPECTED_ARTIFACT_FILES,
        "missing_files": missing_files,
        "owned_table_count": len(OWNED_TABLES),
        "operation_count": len(domain_depth_contract()["operations"]),
        "side_effects": (),
    }


def build_release_evidence() -> dict:
    source_artifact = pbc_source_artifact_contract()
    schema = build_schema_contract()
    service = build_service_contract()
    routes = validate_api_route_contracts()
    events = validate_event_contract()
    handlers = handler_manifest()
    ui = data_product_catalog_ui_contract()
    agent = agent_skill_manifest()
    chatbot = chatbot_interface_contract()
    config = configuration_manifest()
    parameters = parameter_manifest()
    rules = rule_manifest()
    permissions = permission_manifest()
    seed = validate_seed_data()
    capability = validate_table_stakes_capability_coverage()
    domain = domain_depth_contract()
    domain_smoke = domain_depth_smoke_test()
    checks = (
        {"id": "source_artifacts", "ok": source_artifact["ok"]},
        {"id": "schema_models_migrations", "ok": schema["ok"] and len(schema["tables"]) >= 20},
        {"id": "service_contract", "ok": service["ok"] and len(service["command_methods"]) >= 15},
        {"id": "api_routes", "ok": routes["ok"] and len(routes["contracts"]["contracts"]) >= 20},
        {"id": "appgen_x_events", "ok": events["ok"]},
        {"id": "idempotent_handlers", "ok": handlers["ok"]},
        {"id": "ui_workbench_forms_wizards_controls", "ok": ui["ok"] and bool(ui["forms"]) and bool(ui["wizards"]) and bool(ui["controls"])},
        {"id": "agent_crud_document_planning", "ok": agent["ok"] and chatbot["ok"]},
        {"id": "configuration_rules_parameters", "ok": config["ok"] and parameters["ok"] and rules["ok"]},
        {"id": "permissions", "ok": permissions["ok"]},
        {"id": "seed_data", "ok": seed["ok"]},
        {"id": "table_stakes_capability_coverage", "ok": capability["ok"]},
        {"id": "world_class_domain_depth", "ok": domain["ok"] and domain_smoke["ok"]},
    )
    return {
        "format": "appgen.data-product-catalog-release-evidence.v1",
        "ok": all(check["ok"] for check in checks),
        "pbc": PBC_KEY,
        "checks": checks,
        "blocking_gaps": tuple(check for check in checks if not check["ok"]),
        "boundary_gaps": (),
        "source_artifact_contract": source_artifact,
        "side_effects": (),
    }


def release_readiness_manifest() -> dict:
    evidence = build_release_evidence()
    return {
        "ok": evidence["ok"],
        "pbc": PBC_KEY,
        "sections": (
            "schema",
            "service",
            "api",
            "events",
            "handlers",
            "ui",
            "agent",
            "governance",
            "tests",
            "release_gates",
        ),
        "checks": evidence["checks"],
        "blocking_gaps": tuple(evidence.get("blocking_gaps", ())),
        "boundary_gaps": tuple(evidence.get("boundary_gaps", ())),
        "side_effects": (),
    }


def validate_release_evidence() -> dict:
    evidence = build_release_evidence()
    failed = tuple(check for check in evidence["checks"] if not check["ok"])
    return {
        "ok": evidence["ok"] and not failed and not evidence["boundary_gaps"],
        "missing_sections": (),
        "failed_checks": failed,
        "boundary_gaps": evidence["boundary_gaps"],
        "blocking_gaps": failed,
        "side_effects": (),
    }


def pbc_implementation_release_audit() -> dict:
    evidence = build_release_evidence()
    validation = validate_release_evidence()
    governance = governance_smoke_test()
    service = service_operation_contracts()
    return {
        "ok": evidence["ok"] and validation["ok"] and governance["ok"] and service["ok"],
        "gate": "pbc_implementation_release_audit",
        "release_evidence": evidence,
        "validation": validation,
        "governance": governance,
        "service": service,
        "side_effects": (),
    }


def pbc_generation_smoke_audit() -> dict:
    from .runtime import pbc_generation_smoke_audit as runtime_generation_smoke_audit

    return runtime_generation_smoke_audit()


def smoke_test() -> dict:
    validation = validate_release_evidence()
    return {"ok": validation["ok"], "validation": validation, "side_effects": ()}


def data_product_catalog_build_release_evidence() -> dict:
    return build_release_evidence()
