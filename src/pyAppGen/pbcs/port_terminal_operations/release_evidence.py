"""Generated release evidence for the Port Terminal Operations PBC."""

from __future__ import annotations

from pathlib import Path

from . import agent
from . import events
from . import ui
from .schema_contract import build_schema_contract
from .service_contract import build_service_contract
from .standalone import port_terminal_operations_standalone_app_contract
from .standalone import standalone_manifest

PBC_KEY = "port_terminal_operations"
_DOCS = (
    "README.md",
    "SPECIFICATION.md",
    "implementation-plan.md",
    "implementation-status.md",
    "RELEASE_EVIDENCE.md",
)


def _documentation_artifacts() -> dict:
    base = Path(__file__).resolve().parent
    artifacts = tuple({"path": name, "exists": (base / name).exists()} for name in _DOCS)
    missing = tuple(item["path"] for item in artifacts if not item["exists"])
    return {"ok": not missing, "artifacts": artifacts, "missing": missing}


def build_release_evidence() -> dict:
    schema = build_schema_contract()
    service = build_service_contract()
    event_manifest = events.event_contract_manifest()
    ui_contract = ui.port_terminal_operations_ui_contract()
    standalone_contract = port_terminal_operations_standalone_app_contract()
    docs = _documentation_artifacts()
    checks = (
        {"id": "schema_contract", "ok": schema.get("ok") is True},
        {"id": "service_contract", "ok": service.get("ok") is True},
        {"id": "event_contract", "ok": event_manifest.get("ok") is True},
        {
            "id": "ui_forms_wizards_controls",
            "ok": bool(ui_contract.get("forms")) and bool(ui_contract.get("wizards")) and bool(ui_contract.get("controls")),
        },
        {"id": "agent_surface", "ok": agent.smoke_test().get("ok") is True},
        {"id": "standalone_app_surface", "ok": standalone_contract.get("ok") is True},
        {"id": "documentation_present", "ok": docs.get("ok") is True},
        {"id": "event_topic_fixed", "ok": standalone_manifest().get("event_topic") == f"pbc.{PBC_KEY}.events"},
        {
            "id": "owned_boundary_preserved",
            "ok": ui_contract.get("binding_evidence", {}).get("shared_table_access") is False,
        },
    )
    blocking_gaps = tuple(check for check in checks if check.get("ok") is not True)
    return {
        "format": "appgen.port-terminal-operations-release-evidence.v1",
        "ok": not blocking_gaps,
        "pbc": PBC_KEY,
        "checks": checks,
        "schema": schema,
        "service": service,
        "events": event_manifest,
        "ui": ui_contract,
        "agent": {
            "skill_manifest": agent.agent_skill_manifest(),
            "chatbot": agent.chatbot_interface_contract(),
            "workspace": agent.standalone_agent_workspace_contract(),
        },
        "standalone_app": standalone_contract,
        "documentation": docs,
        "blocking_gaps": blocking_gaps,
        "side_effects": (),
    }


def release_readiness_manifest() -> dict:
    evidence = build_release_evidence()
    sections = tuple(
        name
        for name in ("schema", "service", "events", "ui", "agent", "standalone_app", "documentation")
        if isinstance(evidence.get(name), dict)
    )
    return {
        "ok": evidence["ok"] and bool(evidence.get("checks")),
        "pbc": PBC_KEY,
        "format": evidence["format"],
        "sections": sections,
        "checks": evidence["checks"],
        "blocking_gaps": evidence["blocking_gaps"],
        "required_sections": ("schema", "service", "ui", "standalone_app", "documentation"),
        "side_effects": (),
    }


def validate_release_evidence() -> dict:
    evidence = build_release_evidence()
    manifest = release_readiness_manifest()
    missing_sections = tuple(section for section in manifest["required_sections"] if section not in manifest["sections"])
    failed_checks = tuple(check for check in manifest["checks"] if check.get("ok") is not True)
    boundary_gaps = tuple(
        gap
        for gap, failed in (
            ("missing_forms", not bool(evidence.get("ui", {}).get("forms"))),
            ("missing_wizards", not bool(evidence.get("ui", {}).get("wizards"))),
            ("missing_controls", not bool(evidence.get("ui", {}).get("controls"))),
            ("missing_documentation", not evidence.get("documentation", {}).get("ok")),
            ("standalone_surface_invalid", evidence.get("standalone_app", {}).get("ok") is not True),
        )
        if failed
    )
    return {
        "ok": manifest["ok"] and not missing_sections and not failed_checks and not boundary_gaps,
        "pbc": PBC_KEY,
        "manifest": manifest,
        "missing_sections": missing_sections,
        "failed_checks": failed_checks,
        "boundary_gaps": boundary_gaps,
        "side_effects": (),
    }


def smoke_test() -> dict:
    validation = validate_release_evidence()
    evidence = build_release_evidence()
    return {
        "ok": validation["ok"] and evidence["ok"],
        "validation": validation,
        "evidence": evidence,
        "side_effects": (),
    }
