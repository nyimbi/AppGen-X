"""Release evidence for the inventory_positioning standalone PBC."""

from __future__ import annotations

from .agent import composed_agent_contribution
from .events import event_contract_manifest
from .permissions import permission_manifest
from .routes import api_route_contracts
from .schema_contract import build_schema_contract
from .seed_data import seed_plan
from .service_contract import build_service_contract
from .ui import inventory_positioning_ui_contract


PBC_KEY = "inventory_positioning"


def build_release_evidence() -> dict:
    schema = build_schema_contract()
    service = build_service_contract()
    api = api_route_contracts()
    permissions = permission_manifest()
    ui = inventory_positioning_ui_contract()
    events = event_contract_manifest()
    agent = composed_agent_contribution()
    seeds = seed_plan()
    checks = (
        {"id": "owned_schema_depth", "ok": schema["ok"] and len(schema["owned_tables"]) >= 40},
        {"id": "migration_coverage", "ok": schema["migration_sql_present"] and not schema["missing_from_migration"]},
        {"id": "service_surface", "ok": service["ok"] and len(service["command_methods"]) >= 8},
        {"id": "api_contract", "ok": api["ok"] and len(api["contracts"]) == 10},
        {"id": "appgen_event_contract", "ok": events["ok"] and events["contract"] == "appgen_event_contract"},
        {"id": "permission_coverage", "ok": permissions["ok"] and "register_item" in permissions["action_permissions"]},
        {"id": "ui_workbench_coverage", "ok": ui["ok"] and bool(ui["forms"]) and bool(ui["wizards"]) and bool(ui["controls"])},
        {"id": "seed_bootstrap", "ok": seeds["ok"] and bool(seeds["standalone_bootstrap"])},
        {"id": "agent_contract", "ok": agent["ok"] and agent["chatbot"]["ok"]},
        {"id": "shared_table_isolation", "ok": schema["shared_table_access"] is False and service["external_dependencies"]["shared_tables"] == ()},
    )
    return {
        "format": "appgen.inventory-positioning-release-evidence.v1",
        "ok": all(check["ok"] for check in checks),
        "pbc": PBC_KEY,
        "checks": checks,
        "schema": schema,
        "service": service,
        "api": api,
        "permissions": permissions,
        "ui": ui,
        "events": events,
        "agent": agent,
        "seed_data": seeds,
        "blocking_gaps": tuple(check for check in checks if not check["ok"]),
    }


RELEASE_EVIDENCE = build_release_evidence()


def release_readiness_manifest() -> dict:
    evidence = build_release_evidence()
    return {
        "ok": evidence["ok"] and bool(evidence["checks"]),
        "pbc": PBC_KEY,
        "format": evidence["format"],
        "sections": ("schema", "service", "api", "permissions", "ui", "events", "agent", "seed_data"),
        "checks": evidence["checks"],
        "blocking_gaps": evidence["blocking_gaps"],
        "required_sections": ("schema", "service", "api", "permissions", "ui", "events"),
        "side_effects": (),
    }


def validate_release_evidence() -> dict:
    evidence = build_release_evidence()
    manifest = release_readiness_manifest()
    missing_sections = tuple(section for section in manifest["required_sections"] if section not in evidence)
    failed_checks = tuple(check for check in manifest["checks"] if check["ok"] is not True)
    boundary_gaps = tuple(
        name
        for name, failed in (
            ("schema_shared_table_access", evidence["schema"]["shared_table_access"] is not False),
            ("service_shared_table_access", evidence["service"]["external_dependencies"]["shared_tables"] != ()),
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
