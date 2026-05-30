"""Release evidence for the wealth_portfolio_management PBC."""
from __future__ import annotations

from pathlib import Path

from .agent import chatbot_interface_contract, smoke_test as agent_smoke_test
from .config import governance_smoke_test
from .events import smoke_test as event_smoke_test
from .handlers import smoke_test as handler_smoke_test
from .routes import api_route_contracts, standalone_route_smoke_test, validate_api_route_contracts
from .runtime import wealth_portfolio_management_build_release_evidence as runtime_build_release_evidence
from .services import smoke_test as service_smoke_test
from .standalone import (
    wealth_portfolio_management_standalone_app_contract,
    wealth_portfolio_management_standalone_app_smoke,
)
from .ui import standalone_ui_smoke_test, wealth_portfolio_management_ui_contract


DOC_FILES = ("README.md", "implementation-plan.md", "implementation-status.md", "RELEASE_EVIDENCE.md")


def build_release_evidence() -> dict:
    base = Path(__file__).resolve().parent
    runtime = runtime_build_release_evidence()
    documentation = {
        "ok": all((base / name).is_file() for name in DOC_FILES),
        "files": tuple(str(base / name) for name in DOC_FILES),
    }
    standalone_contract = wealth_portfolio_management_standalone_app_contract()
    standalone_smoke = wealth_portfolio_management_standalone_app_smoke()
    checks = (
        {"id": "runtime_release_contract", "ok": runtime["ok"]},
        {"id": "service_route_surface", "ok": service_smoke_test()["ok"] and api_route_contracts()["ok"] and validate_api_route_contracts()["ok"]},
        {"id": "events_and_handlers", "ok": event_smoke_test()["ok"] and handler_smoke_test()["ok"]},
        {"id": "ui_and_agent", "ok": wealth_portfolio_management_ui_contract()["ok"] and standalone_ui_smoke_test()["ok"] and chatbot_interface_contract()["ok"] and agent_smoke_test()["ok"]},
        {"id": "governance", "ok": governance_smoke_test()["ok"]},
        {"id": "documentation", "ok": documentation["ok"]},
        {"id": "standalone_app", "ok": standalone_contract["ok"] and standalone_smoke["ok"] and standalone_route_smoke_test()["ok"]},
    )
    return {
        "ok": all(check["ok"] for check in checks),
        "pbc": "wealth_portfolio_management",
        "checks": checks,
        "blocking_gaps": tuple(check for check in checks if not check["ok"]),
        "boundary_gaps": (),
        "runtime": runtime,
        "documentation": documentation,
        "standalone_app": standalone_smoke,
        "side_effects": (),
    }


def wealth_portfolio_management_build_release_evidence() -> dict:
    return build_release_evidence()


def release_readiness_manifest() -> dict:
    evidence = build_release_evidence()
    return {
        "ok": evidence["ok"],
        "pbc": evidence["pbc"],
        "sections": (
            "schema",
            "services",
            "events",
            "handlers",
            "ui",
            "agent",
            "governance",
            "documentation",
            "standalone_app",
        ),
        "checks": evidence["checks"],
        "blocking_gaps": tuple(evidence.get("blocking_gaps", ())),
        "boundary_gaps": tuple(evidence.get("boundary_gaps", ())),
        "evidence": evidence,
        "side_effects": (),
    }


def validate_release_evidence() -> dict:
    evidence = build_release_evidence()
    failed = tuple(check for check in evidence["checks"] if not check["ok"])
    return {
        "ok": evidence["ok"] and not failed and not evidence["boundary_gaps"],
        "pbc": evidence["pbc"],
        "missing_sections": (),
        "failed_checks": failed,
        "boundary_gaps": evidence["boundary_gaps"],
        "blocking_gaps": evidence["blocking_gaps"],
        "side_effects": (),
    }


def smoke_test() -> dict:
    validation = validate_release_evidence()
    return {"ok": validation["ok"], "validation": validation, "side_effects": ()}
