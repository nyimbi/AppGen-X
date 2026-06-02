"""Release evidence for the case_knowledge_management PBC."""

from __future__ import annotations

from .agent import smoke_test as agent_smoke_test
from .config import governance_smoke_test
from .events import validate_event_contract
from .handlers import smoke_test as handler_smoke_test
from .routes import validate_api_route_contracts
from .runtime import case_knowledge_management_build_release_evidence as runtime_release_evidence
from .schema_contract import validate_schema_contract
from .service_contract import validate_service_contract
from .ui import smoke_test as ui_smoke_test
from .app_surface import app_surface_smoke_test, single_pbc_case_knowledge_management_app_contract


PBC_KEY = "case_knowledge_management"


def build_release_evidence() -> dict:
    runtime = runtime_release_evidence()
    checks = tuple(runtime["checks"]) + (
        {"id": "schema_contract", "ok": validate_schema_contract()["ok"]},
        {"id": "service_contract", "ok": validate_service_contract()["ok"]},
        {"id": "route_contract", "ok": validate_api_route_contracts()["ok"]},
        {"id": "event_contract", "ok": validate_event_contract()["ok"]},
        {"id": "handler_smoke", "ok": handler_smoke_test()["ok"]},
        {"id": "governance_smoke", "ok": governance_smoke_test()["ok"]},
        {"id": "agent_smoke", "ok": agent_smoke_test()["ok"]},
        {"id": "ui_smoke", "ok": ui_smoke_test()["ok"]},
        {"id": "standalone_app_surface", "ok": app_surface_smoke_test()["ok"]},
        {"id": "standalone_forms_wizards_controls", "ok": single_pbc_case_knowledge_management_app_contract()["forms"]["ok"] and single_pbc_case_knowledge_management_app_contract()["wizards"]["ok"] and single_pbc_case_knowledge_management_app_contract()["controls"]["ok"]},
    )
    failed = tuple(check for check in checks if not check["ok"])
    return {
        "format": "appgen.case-knowledge-management-release-evidence.v2",
        "ok": not failed,
        "pbc": PBC_KEY,
        "checks": checks,
        "blocking_gaps": failed,
        "boundary_gaps": (),
        "runtime": runtime,
        "standalone_app": single_pbc_case_knowledge_management_app_contract(),
        "standalone_app_smoke": app_surface_smoke_test(),
        "side_effects": (),
    }


def release_readiness_manifest() -> dict:
    evidence = build_release_evidence()
    return {
        "ok": evidence["ok"],
        "pbc": PBC_KEY,
        "sections": (
            "schema",
            "services",
            "api",
            "events",
            "handlers",
            "ui",
            "agent",
            "governance",
            "release",
            "tests",
        ),
        "checks": evidence["checks"],
        "blocking_gaps": evidence["blocking_gaps"],
        "boundary_gaps": evidence["boundary_gaps"],
        "module": __name__,
        "side_effects": (),
    }


def validate_release_evidence() -> dict:
    evidence = build_release_evidence()
    failed = tuple(check for check in evidence["checks"] if not check["ok"])
    return {
        "ok": evidence["ok"] and not failed,
        "missing_sections": (),
        "failed_checks": failed,
        "boundary_gaps": evidence["boundary_gaps"],
        "blocking_gaps": failed,
        "side_effects": (),
    }


def smoke_test() -> dict:
    validation = validate_release_evidence()
    return {"ok": validation["ok"], "validation": validation, "side_effects": ()}
