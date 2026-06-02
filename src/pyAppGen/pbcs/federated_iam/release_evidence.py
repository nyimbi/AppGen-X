"""Generated release evidence for the federated_iam PBC."""

from __future__ import annotations

from pathlib import Path

from . import agent
from . import events
from . import permissions
from . import routes
from . import schema_contract
from . import seed_data
from . import service_contract
from . import standalone
from . import ui
from .runtime import federated_iam_build_release_evidence as runtime_release_evidence
from .runtime import federated_iam_runtime_smoke


_DOC_FILES = (
    "README.md",
    "SPECIFICATION.md",
    "RELEASE_EVIDENCE.md",
    "implementation-plan.md",
    "implementation-status.md",
)


def _doc_status() -> tuple[dict, ...]:
    base = Path(__file__).parent
    return tuple(
        {"path": name, "exists": (base / name).exists()}
        for name in _DOC_FILES
    )


def build_release_evidence() -> dict:
    """Return package-local release audit evidence for this PBC."""
    runtime_evidence = runtime_release_evidence()
    schema = schema_contract.build_schema_contract()
    service = service_contract.build_service_contract()
    api = routes.route_catalog_contract()
    permission_manifest = permissions.permission_manifest()
    ui_contract = ui.federated_iam_ui_contract()
    event_contract = events.event_contract_manifest()
    seed = seed_data.build_seed_state()
    standalone_app = standalone.standalone_manifest()
    agent_manifest = agent.composed_agent_contribution()
    docs = _doc_status()
    runtime_smoke = federated_iam_runtime_smoke()
    checks = (
        {"id": "runtime_release_evidence", "ok": runtime_evidence.get("ok") is True},
        {"id": "schema_contract", "ok": schema.get("ok") is True and bool(schema.get("owned_tables"))},
        {"id": "service_contract", "ok": service.get("ok") is True and bool(service.get("command_methods"))},
        {"id": "api_route_catalog", "ok": api.get("ok") is True and bool(api.get("routes"))},
        {"id": "permissions_manifest", "ok": permission_manifest.get("ok") is True and bool(permission_manifest.get("action_permissions"))},
        {"id": "ui_contract", "ok": ui_contract.get("ok") is True and bool(ui_contract.get("forms")) and bool(ui_contract.get("wizards"))},
        {"id": "event_contract", "ok": event_contract.get("ok") is True and event_contract.get("stream_engine_picker_visible") is False},
        {"id": "seed_state", "ok": seed.get("ok") is True and seed["summary"]["principal_count"] >= 2},
        {"id": "standalone_manifest", "ok": standalone_app.get("ok") is True and bool(standalone_app.get("routes"))},
        {"id": "agent_surface", "ok": agent_manifest.get("ok") is True and bool(agent_manifest.get("skills"))},
        {"id": "docs_present", "ok": all(item["exists"] for item in docs)},
        {"id": "runtime_smoke", "ok": runtime_smoke.get("ok") is True},
    )
    blocking_gaps = tuple(check for check in checks if not check["ok"])
    return {
        "format": "appgen.federated-iam-release-evidence.v2",
        "ok": not blocking_gaps,
        "pbc": "federated_iam",
        "checks": checks,
        "blocking_gaps": blocking_gaps,
        "schema": schema,
        "service": service,
        "api": api,
        "permissions": permission_manifest,
        "ui": ui_contract,
        "events": event_contract,
        "seed": seed,
        "standalone": standalone_app,
        "agent": agent_manifest,
        "docs": docs,
        "runtime_evidence": runtime_evidence,
        "runtime_smoke": runtime_smoke,
    }


RELEASE_EVIDENCE = build_release_evidence()


def release_readiness_manifest() -> dict:
    """Return side-effect-free release evidence coverage and gate metadata."""
    evidence = build_release_evidence()
    sections = tuple(
        name
        for name in ("schema", "service", "api", "permissions", "ui", "events", "seed", "standalone", "agent")
        if isinstance(evidence.get(name), dict)
    )
    return {
        "ok": evidence.get("ok") is True and bool(evidence.get("checks")),
        "pbc": "federated_iam",
        "format": evidence.get("format"),
        "sections": sections,
        "checks": tuple(evidence.get("checks", ())),
        "blocking_gaps": tuple(evidence.get("blocking_gaps", ())),
        "required_sections": ("schema", "service", "api", "permissions", "ui", "events", "standalone"),
        "side_effects": (),
    }


def validate_release_evidence() -> dict:
    """Validate release evidence, blocking gaps, and owned-boundary proof."""
    evidence = build_release_evidence()
    manifest = release_readiness_manifest()
    missing_sections = tuple(section for section in manifest["required_sections"] if section not in manifest["sections"])
    failed_checks = tuple(check for check in manifest["checks"] if check.get("ok") is not True)
    boundary_gaps = tuple(
        gap
        for gap, failed in (
            ("schema_shared_table_access", evidence["schema"].get("shared_table_access") is not False),
            ("service_shared_table_access", evidence["service"].get("shared_table_access") is True),
            ("route_catalog_missing", not bool(evidence["api"].get("routes"))),
        )
        if failed
    )
    return {
        "ok": manifest["ok"]
        and not missing_sections
        and not failed_checks
        and not boundary_gaps,
        "pbc": "federated_iam",
        "manifest": manifest,
        "missing_sections": missing_sections,
        "failed_checks": failed_checks,
        "boundary_gaps": boundary_gaps,
        "side_effects": (),
    }


def smoke_test() -> dict:
    """Exercise release evidence readiness validation side-effect-free."""
    validation = validate_release_evidence()
    evidence = build_release_evidence()
    return {
        "ok": validation["ok"] and evidence.get("ok") is True,
        "validation": validation,
        "evidence": evidence,
        "side_effects": (),
    }
