"""Dynamic release evidence for the enterprise_search_vector PBC."""

from __future__ import annotations

import re
from pathlib import Path

from . import agent
from . import events
from . import permissions
from . import routes
from . import seed_data
from . import service_contract
from . import schema_contract
from . import ui


PBC_KEY = "enterprise_search_vector"
PACKAGE_DIR = Path(__file__).resolve().parent
MIGRATION_FILE = PACKAGE_DIR / "migrations" / "001_initial.sql"
REQUIRED_DOCS = (
    "SPECIFICATION.md",
    "RELEASE_EVIDENCE.md",
    "implementation-plan.md",
    "implementation-status.md",
    "README.md",
)
TABLE_PATTERN = re.compile(r"CREATE\s+TABLE\s+([a-zA-Z0-9_]+)", re.IGNORECASE)


def _migration_tables() -> tuple[str, ...]:
    if not MIGRATION_FILE.exists():
        return ()
    return tuple(dict.fromkeys(TABLE_PATTERN.findall(MIGRATION_FILE.read_text(encoding="utf-8"))))


def _doc_status() -> dict:
    present = tuple(name for name in REQUIRED_DOCS if (PACKAGE_DIR / name).exists())
    missing = tuple(name for name in REQUIRED_DOCS if name not in present)
    return {"present": present, "missing": missing}


def build_release_evidence():
    """Return package-derived release audit evidence for this PBC."""
    schema = schema_contract.build_schema_contract()
    service = service_contract.build_service_contract()
    api_routes = routes.api_route_contracts()
    permission_manifest = permissions.permission_manifest()
    ui_contract = ui.enterprise_search_vector_ui_contract()
    event_manifest = events.event_contract_manifest()
    seed_manifest = seed_data.seed_plan()
    agent_manifest = agent.composed_agent_contribution()
    migration_tables = _migration_tables()
    docs = _doc_status()
    required_tables = tuple(table["owned_table"] for table in schema.get("tables", ()))
    checks = (
        {"id": "owned_schema_depth", "ok": len(required_tables) >= 18},
        {"id": "migration_artifact_present", "ok": MIGRATION_FILE.exists()},
        {
            "id": "migration_covers_all_owned_tables",
            "ok": bool(required_tables) and set(required_tables) <= set(migration_tables),
        },
        {"id": "service_contract_depth", "ok": len(service.get("command_methods", ())) >= 20},
        {"id": "api_routes_cover_commands", "ok": len(api_routes.get("contracts", ())) >= 10},
        {"id": "permissions_cover_governance", "ok": len(permission_manifest.get("action_permissions", {})) >= 10},
        {"id": "appgen_event_contract_only", "ok": event_manifest.get("contract") == "appgen_event_contract"},
        {"id": "ui_forms_and_wizards", "ok": bool(ui_contract.get("forms")) and bool(ui_contract.get("wizards"))},
        {"id": "agent_contribution", "ok": agent_manifest.get("ok") is True},
        {"id": "seed_bundle", "ok": seed_manifest.get("ok") is True},
        {"id": "documentation_coverage", "ok": not docs["missing"]},
        {
            "id": "no_shared_table_access",
            "ok": schema.get("shared_table_access") is False and service.get("shared_table_access") is False,
        },
    )
    blocking = tuple(check for check in checks if not check["ok"])
    return {
        "format": "appgen.enterprise-search-vector-release-evidence.v2",
        "ok": not blocking,
        "pbc": PBC_KEY,
        "checks": checks,
        "blocking_gaps": blocking,
        "schema": schema,
        "service": service,
        "api": api_routes,
        "permissions": permission_manifest,
        "ui": ui_contract,
        "events": event_manifest,
        "agent": agent_manifest,
        "seed": seed_manifest,
        "migration_artifact": {
            "path": "migrations/001_initial.sql",
            "table_count": len(migration_tables),
            "tables": migration_tables,
        },
        "documentation": docs,
    }


RELEASE_EVIDENCE = build_release_evidence()


def release_readiness_manifest():
    """Return side-effect-free release evidence coverage and gate metadata."""
    evidence = build_release_evidence()
    sections = tuple(
        name
        for name in ("schema", "service", "api", "permissions", "ui", "events", "agent", "seed")
        if isinstance(evidence.get(name), dict)
    )
    checks = tuple(evidence.get("checks", ()))
    return {
        "ok": evidence.get("ok") is True and bool(checks),
        "pbc": PBC_KEY,
        "format": evidence.get("format"),
        "sections": sections,
        "checks": checks,
        "blocking_gaps": tuple(evidence.get("blocking_gaps", ())),
        "required_sections": ("schema", "service", "api", "permissions", "ui", "events"),
        "side_effects": (),
    }


def validate_release_evidence():
    """Validate release evidence, blocking gaps, documentation, and ownership proof."""
    evidence = build_release_evidence()
    manifest = release_readiness_manifest()
    missing_sections = tuple(section for section in manifest["required_sections"] if section not in manifest["sections"])
    failed_checks = tuple(check for check in manifest["checks"] if check.get("ok") is not True)
    schema = evidence.get("schema", {}) if isinstance(evidence.get("schema"), dict) else {}
    service = evidence.get("service", {}) if isinstance(evidence.get("service"), dict) else {}
    documentation = evidence.get("documentation", {})
    boundary_gaps = tuple(
        gap
        for gap, failed in (
            ("schema_shared_table_access", schema.get("shared_table_access") is not False),
            ("service_shared_table_access", service.get("shared_table_access") is True),
            ("service_missing_command_methods", not bool(service.get("command_methods"))),
            ("documentation_missing", bool(documentation.get("missing"))),
        )
        if failed
    )
    return {
        "ok": manifest["ok"]
        and evidence.get("pbc") == manifest["pbc"]
        and not manifest["blocking_gaps"]
        and not missing_sections
        and not failed_checks
        and not boundary_gaps,
        "pbc": PBC_KEY,
        "manifest": manifest,
        "missing_sections": missing_sections,
        "failed_checks": failed_checks,
        "boundary_gaps": boundary_gaps,
        "side_effects": (),
    }


def smoke_test():
    """Exercise release evidence readiness validation side-effect-free."""
    validation = validate_release_evidence()
    evidence = build_release_evidence()
    return {
        "ok": validation["ok"] and evidence.get("ok") is True,
        "validation": validation,
        "evidence": evidence,
        "side_effects": (),
    }
