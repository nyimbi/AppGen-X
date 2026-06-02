"""Release evidence gates for the standalone aviation maintenance repair slice."""
from __future__ import annotations

from .agent import assistant_planning_contract
from .config import governance_smoke_test
from .events import smoke_test as events_smoke_test
from .handlers import smoke_test as handlers_smoke_test
from .permissions import permission_manifest
from .routes import api_route_contracts, validate_api_route_contracts
from .runtime import aviation_maintenance_repair_build_release_evidence, aviation_maintenance_repair_runtime_smoke
from .services import service_operation_contracts
from .ui import aviation_maintenance_repair_ui_contract
from .workflows import workflow_catalog


def build_release_evidence():
    runtime = aviation_maintenance_repair_runtime_smoke()
    service = service_operation_contracts()
    routes = api_route_contracts()
    ui = aviation_maintenance_repair_ui_contract()
    agent = assistant_planning_contract()
    permissions = permission_manifest()
    workflows = workflow_catalog()
    return {
        "ok": all((runtime["ok"], service["ok"], routes["ok"], ui["ok"], agent["ok"], permissions["ok"], workflows["ok"])),
        "pbc": runtime["release_pack"]["release_pack"]["pbc"],
        "gates": (
            {"gate": "runtime_smoke", "ok": runtime["ok"]},
            {"gate": "service_contracts", "ok": service["ok"]},
            {"gate": "route_contracts", "ok": routes["ok"]},
            {"gate": "ui_forms_wizards_controls", "ok": ui["ok"] and bool(ui["forms"]) and bool(ui["wizards"]) and bool(ui["controls"])},
            {"gate": "assistant_planning", "ok": agent["ok"]},
            {"gate": "permissions_matrix", "ok": permissions["ok"]},
            {"gate": "workflow_catalog", "ok": workflows["ok"]},
        ),
        "runtime_release_evidence": aviation_maintenance_repair_build_release_evidence(),
        "side_effects": (),
    }


def release_readiness_manifest():
    evidence = build_release_evidence()
    return {
        "ok": evidence["ok"],
        "pbc": evidence["pbc"],
        "sections": ("schema", "services", "routes", "events", "handlers", "ui", "agent", "governance", "workflows"),
        "blocking_gaps": tuple(gate["gate"] for gate in evidence["gates"] if not gate["ok"]),
        "boundary_gaps": (),
        "evidence": evidence,
        "side_effects": (),
    }


def validate_release_evidence():
    manifest = release_readiness_manifest()
    validation_checks = (
        validate_api_route_contracts()["ok"],
        governance_smoke_test()["ok"],
        events_smoke_test()["ok"],
        handlers_smoke_test()["ok"],
    )
    return {
        "ok": manifest["ok"] and all(validation_checks),
        "pbc": manifest["pbc"],
        "missing_sections": (),
        "failed_checks": tuple(index for index, passed in enumerate(validation_checks, start=1) if not passed),
        "boundary_gaps": (),
        "side_effects": (),
    }


def smoke_test():
    return {"ok": release_readiness_manifest()["ok"] and validate_release_evidence()["ok"], "side_effects": ()}
