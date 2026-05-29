"""Generated release evidence for the EAM PBC."""

from __future__ import annotations

from pathlib import Path

from . import agent
from . import config
from . import events
from . import handlers
from . import permissions
from . import routes
from . import seed_data
from . import services
from . import ui
from .runtime import eam_build_api_contract
from .runtime import eam_build_release_evidence as runtime_release_evidence
from .runtime import eam_build_service_contract
from .runtime import eam_verify_owned_table_boundary
from .schema_contract import build_schema_contract


_DOC_FILES = ("SPECIFICATION.md", "RELEASE_EVIDENCE.md", "implementation-plan.md", "implementation-status.md", "README.md")


def _doc_status() -> dict:
    base = Path(__file__).resolve().parent
    present = tuple(name for name in _DOC_FILES if (base / name).exists())
    missing = tuple(name for name in _DOC_FILES if name not in present)
    return {"present": present, "missing": missing}


def build_release_evidence():
    """Return generated release audit evidence for this PBC."""
    schema = build_schema_contract()
    service = eam_build_service_contract()
    api = eam_build_api_contract()
    permissions_manifest = permissions.permission_manifest()
    ui_smoke = ui.smoke_test()
    event_validation = events.validate_event_contract()
    handler_smoke = handlers.smoke_test()
    config_smoke = config.smoke_test()
    seed_smoke = seed_data.smoke_test()
    agent_smoke = agent.smoke_test()
    route_validation = routes.validate_api_route_contracts()
    service_smoke = services.smoke_test()
    logical_owned_tables = schema.get("logical_owned_tables") or tuple(table.get("table") for table in schema.get("tables", ()))
    boundary = eam_verify_owned_table_boundary(logical_owned_tables)
    runtime_evidence = runtime_release_evidence()
    docs = _doc_status()
    checks = (
        {"id": "owned_schema_depth", "ok": schema["ok"] and len(schema["owned_tables"]) >= 16},
        {"id": "migration_artifact", "ok": "migrations/001_initial.sql" in schema.get("migrations", ())},
        {"id": "service_command_depth", "ok": service["ok"] and len(service["command_methods"]) >= 16},
        {"id": "api_event_contract", "ok": api["ok"] and api["event_contract"] == "AppGen-X"},
        {"id": "permissions_cover_commands", "ok": permissions_manifest["ok"] and "register_equipment" in permissions_manifest["action_permissions"]},
        {"id": "ui_workbench_evidence", "ok": ui_smoke["ok"] and "AgentPlanningStudio" in ui_smoke["contract"]["fragments"]},
        {"id": "event_outbox_inbox", "ok": event_validation["ok"]},
        {"id": "idempotent_handlers", "ok": handler_smoke["ok"]},
        {"id": "configuration_schema", "ok": config_smoke["ok"]},
        {"id": "seed_data", "ok": seed_smoke["ok"]},
        {"id": "agent_planning", "ok": agent_smoke["ok"]},
        {"id": "route_validation", "ok": route_validation["ok"]},
        {"id": "service_smoke", "ok": service_smoke["ok"]},
        {"id": "owned_boundary_proof", "ok": boundary["ok"]},
        {"id": "runtime_release_checks", "ok": runtime_evidence["ok"]},
        {"id": "package_docs", "ok": not docs["missing"]},
    )
    return {
        "format": "appgen.eam-release-evidence.v1",
        "ok": all(check["ok"] for check in checks),
        "checks": checks,
        "schema": schema,
        "service": service,
        "api": api,
        "permissions": permissions_manifest,
        "ui": ui_smoke,
        "events": event_validation,
        "handlers": handler_smoke,
        "configuration": config_smoke,
        "seed_data": seed_smoke,
        "agent": agent_smoke,
        "routes": route_validation,
        "service_smoke": service_smoke,
        "boundary": boundary,
        "runtime_release_evidence": runtime_evidence,
        "docs": docs,
        "blocking_gaps": tuple(check for check in checks if not check["ok"]),
        "pbc": "eam",
    }


RELEASE_EVIDENCE = build_release_evidence()


def release_readiness_manifest():
    """Return side-effect-free release evidence coverage and gate metadata."""
    evidence = build_release_evidence()
    sections = tuple(
        name
        for name in ("schema", "service", "api", "permissions", "ui", "events", "handlers", "configuration", "seed_data", "agent")
        if isinstance(evidence.get(name), dict)
    )
    checks = tuple(evidence.get("checks", ()))
    return {
        "ok": evidence.get("ok") is True and bool(checks),
        "pbc": "eam",
        "format": evidence.get("format"),
        "sections": sections,
        "checks": checks,
        "blocking_gaps": tuple(evidence.get("blocking_gaps", ())),
        "required_sections": ("schema", "service", "api", "permissions", "ui", "events", "handlers", "agent"),
        "side_effects": (),
    }


def validate_release_evidence():
    """Validate release evidence, blocking gaps, docs, and owned-boundary proof."""
    evidence = build_release_evidence()
    manifest = release_readiness_manifest()
    missing_sections = tuple(section for section in manifest["required_sections"] if section not in manifest["sections"])
    failed_checks = tuple(check for check in manifest["checks"] if check.get("ok") is not True)
    schema = evidence.get("schema", {}) if isinstance(evidence.get("schema"), dict) else {}
    service = evidence.get("service", {}) if isinstance(evidence.get("service"), dict) else {}
    boundary_gaps = tuple(
        gap
        for gap, failed in (
            ("schema_shared_table_access", schema.get("shared_table_access") is not False),
            ("service_shared_table_access", service.get("shared_table_access") is True),
            ("service_missing_command_methods", not bool(service.get("command_methods"))),
            ("missing_docs", bool(evidence.get("docs", {}).get("missing"))),
            ("boundary_violation", evidence.get("boundary", {}).get("ok") is not True),
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
        "pbc": "eam",
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
