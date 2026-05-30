"""Release evidence for the insurance_claims_policy PBC."""

from __future__ import annotations

from pathlib import Path

from . import agent
from . import config
from . import events
from . import handlers
from . import routes
from . import schema_contract
from . import service_contract
from . import services
from . import ui
from .models import OWNED_TABLES
from .standalone import standalone_manifest
from .standalone import smoke_test as standalone_smoke_test

PBC_KEY = "insurance_claims_policy"
PACKAGE_DIR = Path(__file__).resolve().parent


def build_release_evidence() -> dict:
    docs = ("README.md", "implementation-status.md", "RELEASE_EVIDENCE.md", "SPECIFICATION.md", "improve1.md")
    docs_present = tuple(name for name in docs if (PACKAGE_DIR / name).exists())
    schema = schema_contract.build_schema_contract()
    service = service_contract.build_service_contract()
    route_contract = routes.validate_api_route_contracts()
    event_contract = events.validate_event_contract()
    handler_contract = handlers.smoke_test()
    governance = config.governance_smoke_test()
    agent_contract = agent.smoke_test()
    ui_contract = ui.smoke_test()
    standalone = standalone_manifest()
    standalone_smoke = standalone_smoke_test()
    checks = (
        {"id": "docs_materialized", "ok": len(docs_present) == len(docs)},
        {"id": "schema_models_migration_alignment", "ok": schema["ok"] and len(schema["owned_tables"]) == len(OWNED_TABLES)},
        {"id": "service_route_runtime_surface", "ok": service["ok"] and route_contract["ok"]},
        {"id": "appgen_x_eventing", "ok": event_contract["ok"] and handler_contract["ok"]},
        {"id": "governance_defaults", "ok": governance["ok"]},
        {"id": "ui_forms_wizards_controls", "ok": ui_contract["ok"]},
        {"id": "agent_skills", "ok": agent_contract["ok"]},
        {"id": "standalone_application", "ok": standalone["ok"] and standalone_smoke["ok"]},
    )
    return {
        "format": "appgen.insurance-claims-policy-release-evidence.v1",
        "ok": all(check["ok"] for check in checks),
        "pbc": PBC_KEY,
        "checks": checks,
        "docs_present": docs_present,
        "schema": schema,
        "service": service,
        "routes": route_contract,
        "events": event_contract,
        "handlers": handler_contract,
        "governance": governance,
        "agent": agent_contract,
        "ui": ui_contract,
        "standalone": standalone,
        "standalone_smoke": standalone_smoke,
        "blocking_gaps": tuple(check for check in checks if not check["ok"]),
        "boundary_gaps": tuple(route_contract.get("invalid_table_scope", ())),
        "side_effects": (),
    }


def release_readiness_manifest() -> dict:
    evidence = build_release_evidence()
    return {
        "ok": evidence["ok"],
        "pbc": PBC_KEY,
        "sections": ("schema", "service", "api", "events", "handlers", "ui", "agent", "governance", "standalone", "tests"),
        "checks": evidence["checks"],
        "blocking_gaps": evidence["blocking_gaps"],
        "boundary_gaps": evidence["boundary_gaps"],
        "side_effects": (),
    }


def validate_release_evidence() -> dict:
    evidence = build_release_evidence()
    failed = tuple(check for check in evidence["checks"] if not check["ok"])
    missing_sections = tuple(section for section in ("schema", "service", "ui", "standalone") if section not in release_readiness_manifest()["sections"])
    return {
        "ok": evidence["ok"] and not failed and not evidence["boundary_gaps"] and not missing_sections,
        "missing_sections": missing_sections,
        "failed_checks": failed,
        "boundary_gaps": evidence["boundary_gaps"],
        "blocking_gaps": failed,
        "side_effects": (),
    }


def smoke_test() -> dict:
    validation = validate_release_evidence()
    return {"ok": validation["ok"], "validation": validation, "side_effects": ()}


def insurance_claims_policy_build_release_evidence() -> dict:
    return build_release_evidence()
