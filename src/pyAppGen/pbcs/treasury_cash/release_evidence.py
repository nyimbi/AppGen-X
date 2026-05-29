"""Release evidence for the standalone treasury_cash PBC slice."""

from __future__ import annotations

from . import agent
from . import events
from . import handlers
from . import repository
from . import routes
from . import seed_data
from . import services
from . import ui
from .runtime import treasury_cash_build_release_evidence



def build_release_evidence():
    """Return executable release audit evidence for the treasury_cash slice."""
    base = dict(treasury_cash_build_release_evidence())
    repository_manifest = repository.repository_manifest()
    route_manifest = routes.api_route_contracts()
    ui_smoke = ui.smoke_test()
    agent_contribution = agent.composed_agent_contribution()
    seed_manifest = seed_data.validate_seed_data()
    execution_service = services.treasury_cash_execution_service_manifest()
    event_smoke = events.smoke_test()
    handler_smoke = handlers.smoke_test()
    single_pbc_app = ui.treasury_cash_single_pbc_app_contract()
    checks = tuple(base.get("checks", ())) + (
        {"id": "repository_surface_bound", "ok": repository_manifest["ok"]},
        {"id": "single_pbc_app_forms_wizards_controls", "ok": single_pbc_app["ok"]},
        {"id": "ui_contract_bound", "ok": ui_smoke["ok"]},
        {"id": "agent_contribution_bound", "ok": agent_contribution["ok"]},
        {"id": "execution_service_bound", "ok": execution_service["ok"]},
        {"id": "route_contract_bound", "ok": route_manifest["ok"]},
        {"id": "seed_plan_bound", "ok": seed_manifest["ok"]},
        {"id": "event_contract_bound", "ok": event_smoke["ok"]},
        {"id": "handler_contract_bound", "ok": handler_smoke["ok"]},
    )
    evidence = {
        **base,
        "format": "appgen.treasury-cash-release-evidence.v2",
        "repository": repository_manifest,
        "routes": route_manifest,
        "ui": ui_smoke,
        "agent": agent_contribution,
        "seed": seed_manifest,
        "events": event_smoke,
        "handlers": handler_smoke,
        "execution_service": execution_service,
        "single_pbc_app": single_pbc_app,
        "checks": checks,
    }
    evidence["ok"] = all(check["ok"] for check in checks)
    evidence["blocking_gaps"] = tuple(check for check in checks if not check["ok"])
    evidence.setdefault("pbc", "treasury_cash")
    return evidence



def release_readiness_manifest():
    """Return side-effect-free release evidence coverage and gate metadata."""
    evidence = build_release_evidence()
    sections = tuple(
        name
        for name in ("schema", "service", "api", "permissions", "repository", "routes", "ui", "agent", "seed", "events", "handlers", "execution_service", "single_pbc_app")
        if name in evidence
    )
    return {
        "ok": evidence["ok"],
        "pbc": evidence["pbc"],
        "sections": sections,
        "checks": evidence["checks"],
        "blocking_gaps": evidence["blocking_gaps"],
        "required_sections": ("schema", "service", "repository", "ui", "agent", "single_pbc_app"),
        "side_effects": (),
    }



def validate_release_evidence():
    """Validate release evidence, blocking gaps, and owned-boundary proof."""
    evidence = build_release_evidence()
    manifest = release_readiness_manifest()
    missing_sections = tuple(section for section in manifest["required_sections"] if section not in manifest["sections"])
    failed_checks = tuple(check for check in manifest["checks"] if check["ok"] is not True)
    boundary_gaps = tuple(
        gap
        for gap, failed in (
            ("repository_shared_table_access", evidence["repository"].get("shared_table_access") is True),
            ("routes_shared_table_access", evidence["routes"].get("ok") is not True),
            ("single_pbc_event_contract", evidence["single_pbc_app"].get("event_contract") != "AppGen-X"),
        )
        if failed
    )
    return {
        "ok": evidence["ok"] and not missing_sections and not failed_checks and not boundary_gaps,
        "pbc": evidence["pbc"],
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
        "ok": validation["ok"] and evidence["ok"],
        "validation": validation,
        "evidence": evidence,
        "side_effects": (),
    }


RELEASE_EVIDENCE = build_release_evidence()
