"""Dynamic release evidence for hotel_revenue_management."""

from __future__ import annotations

from pathlib import Path

from . import agent
from . import events
from . import handlers
from . import routes
from . import seed_data
from . import services
from . import ui
from .config import governance_smoke_test
from .domain_depth import domain_depth_contract
from .domain_depth import domain_depth_smoke_test
from .runtime import PBC_KEY
from .runtime import hotel_revenue_management_build_release_evidence as runtime_release_evidence
from .runtime import hotel_revenue_management_build_schema_contract
from .runtime import hotel_revenue_management_runtime_smoke


PACKAGE_DIR = Path(__file__).resolve().parent
REQUIRED_DOCS = (
    "SPECIFICATION.md",
    "RELEASE_EVIDENCE.md",
    "README.md",
    "implementation-status.md",
)
REQUIRED_TESTS = ("tests/test_contract.py", "tests/test_standalone.py")


def build_release_evidence() -> dict:
    runtime_evidence = runtime_release_evidence()
    docs_present = tuple(path for path in REQUIRED_DOCS if (PACKAGE_DIR / path).exists())
    tests_present = tuple(path for path in REQUIRED_TESTS if (PACKAGE_DIR / path).exists())
    domain_contract = domain_depth_contract()
    domain_smoke = domain_depth_smoke_test()
    runtime_smoke = hotel_revenue_management_runtime_smoke()
    checks = tuple(runtime_evidence.get("checks", ())) + (
        {"id": "docs_present", "ok": len(docs_present) == len(REQUIRED_DOCS)},
        {"id": "tests_present", "ok": len(tests_present) == len(REQUIRED_TESTS)},
        {"id": "runtime_smoke", "ok": runtime_smoke["ok"]},
        {"id": "domain_depth_contract", "ok": domain_contract["ok"]},
        {"id": "domain_depth_smoke", "ok": domain_smoke["ok"]},
        {"id": "agent_contract", "ok": agent.smoke_test()["ok"]},
        {"id": "ui_contract", "ok": ui.smoke_test()["ok"]},
        {"id": "event_contract", "ok": events.smoke_test()["ok"]},
        {"id": "handler_contract", "ok": handlers.smoke_test()["ok"]},
        {"id": "service_contract", "ok": services.smoke_test()["ok"]},
        {"id": "route_contract", "ok": routes.smoke_test()["ok"]},
        {"id": "governance_contract", "ok": governance_smoke_test()["ok"]},
        {"id": "seed_bundle", "ok": seed_data.smoke_test()["ok"]},
    )
    return {
        "format": "appgen.hotel-revenue-management-release-evidence.v3",
        "ok": all(check["ok"] for check in checks),
        "pbc": PBC_KEY,
        "checks": checks,
        "schema_contract": hotel_revenue_management_build_schema_contract(),
        "documentation": {
            "required": REQUIRED_DOCS,
            "present": docs_present,
        },
        "tests": {
            "required": REQUIRED_TESTS,
            "present": tests_present,
        },
        "runtime_smoke": runtime_smoke,
        "world_class_domain_depth": domain_contract,
        "domain_depth_smoke": domain_smoke,
        "blocking_gaps": tuple(check for check in checks if not check["ok"]),
        "boundary_gaps": tuple(runtime_evidence.get("boundary_gaps", ())),
        "side_effects": (),
    }


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
            "standalone",
            "tests",
            "documentation",
        ),
        "checks": evidence["checks"],
        "blocking_gaps": evidence["blocking_gaps"],
        "boundary_gaps": evidence["boundary_gaps"],
        "evidence": evidence,
        "side_effects": (),
    }


def validate_release_evidence() -> dict:
    evidence = build_release_evidence()
    failed_checks = tuple(check for check in evidence["checks"] if not check["ok"])
    return {
        "ok": evidence["ok"] and not failed_checks and not evidence["boundary_gaps"],
        "pbc": evidence["pbc"],
        "missing_sections": (),
        "failed_checks": failed_checks,
        "boundary_gaps": evidence["boundary_gaps"],
        "blocking_gaps": evidence["blocking_gaps"],
        "side_effects": (),
    }


def smoke_test() -> dict:
    validation = validate_release_evidence()
    return {"ok": validation["ok"], "validation": validation, "side_effects": ()}
