"""Release evidence helpers for the executable healthcare claims adjudication slice."""

from __future__ import annotations

from typing import Any

from .agent import agent_skill_manifest
from .events import event_contract_manifest
from .handlers import handler_manifest
from .routes import api_route_contracts
from .runtime import claims_adjudication_healthcare_build_release_evidence
from .standalone import full_claims_adjudication_simulation, single_pbc_app_contract, standalone_smoke_test
from .ui import claims_adjudication_healthcare_ui_contract


def build_release_evidence() -> dict[str, Any]:
    evidence = claims_adjudication_healthcare_build_release_evidence()
    app = single_pbc_app_contract()
    smoke = standalone_smoke_test()
    simulation = full_claims_adjudication_simulation()
    checks = tuple(evidence.get('checks', ())) + (
        {'id': 'standalone_single_pbc_app', 'ok': app['ok']},
        {'id': 'standalone_smoke', 'ok': smoke['ok']},
        {'id': 'full_claims_adjudication_simulation', 'ok': simulation['ok']},
        {'id': 'improve1_complete_surface', 'ok': app['forms']['covered_improve1_items'] == tuple(range(1, 51))},
    )
    ok = evidence['ok'] and app['ok'] and smoke['ok'] and simulation['ok']
    return {**evidence, 'ok': ok, 'checks': checks, 'single_pbc_app': app, 'standalone_smoke': smoke, 'full_simulation': simulation, 'blocking_gaps': tuple(check for check in checks if not check['ok'])}


def release_readiness_manifest() -> dict[str, Any]:
    evidence = build_release_evidence()
    sections = {
        "runtime": evidence["ok"],
        "events": event_contract_manifest()["ok"],
        "handlers": handler_manifest()["ok"],
        "routes": api_route_contracts()["ok"],
        "ui": claims_adjudication_healthcare_ui_contract()["ok"],
        "agent": agent_skill_manifest()["ok"],
    }
    return {
        "ok": all(sections.values()),
        "pbc": evidence["pbc"],
        "sections": tuple(sections.keys()),
        "blocking_gaps": tuple(name for name, ok in sections.items() if not ok),
        "boundary_gaps": (),
        "evidence": evidence,
        "side_effects": (),
    }


def validate_release_evidence() -> dict[str, Any]:
    manifest = release_readiness_manifest()
    return {
        "ok": manifest["ok"],
        "pbc": manifest["pbc"],
        "missing_sections": tuple(),
        "failed_checks": manifest["blocking_gaps"],
        "boundary_gaps": manifest["boundary_gaps"],
        "side_effects": (),
    }


def smoke_test() -> dict[str, Any]:
    return {
        "ok": release_readiness_manifest()["ok"] and validate_release_evidence()["ok"],
        "side_effects": (),
    }
