"""Generated release evidence for the dom PBC."""

from __future__ import annotations

from pathlib import Path

from . import agent
from . import audit
from . import events
from . import schema_contract
from . import seed_data
from . import services
from . import standalone
from . import ui


def build_release_evidence():
    """Return generated release audit evidence for this PBC."""
    docs_base = Path(__file__).resolve().parent
    documentation = tuple(
        {
            "path": name,
            "exists": (docs_base / name).exists(),
        }
        for name in ("README.md", "implementation-plan.md", "implementation-status.md", "RELEASE_EVIDENCE.md")
    )
    standalone_manifest = standalone.standalone_manifest()
    standalone_snapshot = standalone.standalone_release_snapshot()
    service_manifest = services.standalone_service_manifest()
    service_descriptor = services.service_operation_manifest()
    event_manifest = events.event_contract_manifest()
    permission_contract = ui.dom_ui_contract()["binding_evidence"]["rbac_permissions"]
    seed_validation = seed_data.validate_seed_data()
    checks = (
        {"id": "owned_schema_depth", "ok": schema_contract.SCHEMA_CONTRACT.get("ok") is True},
        {"id": "standalone_application", "ok": standalone_manifest["ok"]},
        {"id": "standalone_service_methods", "ok": service_manifest["ok"] and len(service_manifest["service_methods"]) >= 12},
        {"id": "ui_forms_wizards_controls", "ok": bool(ui.dom_ui_contract().get("forms")) and bool(ui.dom_ui_contract().get("wizards")) and bool(ui.dom_ui_contract().get("controls"))},
        {"id": "agent_document_intake", "ok": agent.smoke_test()["ok"]},
        {"id": "api_event_contract", "ok": event_manifest["ok"] and event_manifest["topic"] == standalone_manifest["event_topic"]},
        {"id": "permissions_cover_commands", "ok": {"dom.create", "dom.verify", "dom.plan", "dom.cancel", "dom.audit"} <= set(permission_contract)},
        {"id": "documentation_present", "ok": all(item["exists"] for item in documentation)},
        {"id": "repository_read_models", "ok": standalone_snapshot["ok"] and standalone_snapshot["repository"]["dashboard"]["counts"]["orders"] >= 2 and len(standalone_snapshot["read_models"]["orders"]) >= 2},
        {"id": "realistic_seed_bundle", "ok": seed_validation["ok"] and seed_validation["plan"]["standalone_bundle"]["order_count"] >= 2},
        {"id": "package_audit", "ok": audit.run_dom_pbc_audit()["ok"]},
    )
    return {
        "format": "appgen.dom-release-evidence.v1",
        "ok": all(check["ok"] for check in checks),
        "checks": checks,
        "schema": schema_contract.build_schema_contract(),
        "service": {
            **service_manifest,
            "command_methods": tuple(
                method
                for method in service_manifest.get("service_methods", ())
                if method not in set(service_manifest.get("query_methods", ()))
            ),
            "query_methods": tuple(service_manifest.get("query_methods", ())),
            "shared_table_access": False,
            "transaction_boundary": "owned_datastore_plus_outbox",
            "operation_contracts": service_descriptor.get("operation_contracts", ()),
            "descriptor_surface": service_descriptor,
        },
        "api": {
            "routes": tuple(item["path"] for item in services.service_operation_contracts()["contracts"]),
            "event_contract": "AppGen-X",
            "event_topic": standalone_manifest["event_topic"],
            "shared_table_access": False,
        },
        "permissions": {
            "permissions": permission_contract,
            "action_permissions": ui.dom_ui_contract()["action_permissions"],
        },
        "ui": ui.dom_ui_contract(),
        "events": event_manifest,
        "agent": {
            "skill_manifest": agent.agent_skill_manifest(),
            "chatbot": agent.chatbot_interface_contract(),
        },
        "standalone": {
            **standalone_manifest,
            "release_snapshot": standalone_snapshot,
        },
        "seed_data": seed_validation,
        "documentation": documentation,
        "audit": audit.run_dom_pbc_audit(),
        "blocking_gaps": tuple(check for check in checks if not check["ok"]),
        "pbc": "dom",
    }


RELEASE_EVIDENCE = build_release_evidence()


def release_readiness_manifest():
    """Return side-effect-free release evidence coverage and gate metadata."""
    evidence = build_release_evidence()
    sections = tuple(
        name
        for name in ("schema", "service", "api", "permissions", "ui", "events", "agent", "standalone", "seed_data", "documentation", "audit")
        if isinstance(evidence.get(name), (dict, tuple))
    )
    checks = tuple(evidence.get("checks", ()))
    return {
        "ok": evidence.get("ok") is True and bool(checks),
        "pbc": "dom",
        "format": evidence.get("format"),
        "sections": sections,
        "checks": checks,
        "blocking_gaps": tuple(evidence.get("blocking_gaps", ())),
        "required_sections": ("schema", "service", "api", "ui", "agent", "standalone", "seed_data"),
        "side_effects": (),
    }


def validate_release_evidence():
    """Validate release evidence, blocking gaps, and owned-boundary proof."""
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
            ("missing_service_methods", not bool(evidence.get("service", {}).get("service_methods"))),
            ("bad_event_topic", evidence.get("events", {}).get("topic") != standalone.standalone_manifest()["event_topic"]),
            ("missing_read_models", len(evidence.get("standalone", {}).get("release_snapshot", {}).get("read_models", {}).get("orders", ())) < 2),
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
        "pbc": "dom",
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
