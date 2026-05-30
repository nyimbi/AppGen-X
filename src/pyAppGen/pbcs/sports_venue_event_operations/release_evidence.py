from . import runtime
from .agent import composed_agent_contribution
from .services import standalone_service_manifest
from .standalone import documentation_presence, standalone_manifest, standalone_smoke_test
from .ui import sports_venue_event_operations_standalone_workbench_blueprint


def build_release_evidence():
    runtime_evidence = runtime.sports_venue_event_operations_build_release_evidence()
    docs = documentation_presence()
    standalone = standalone_manifest()
    smoke = standalone_smoke_test()
    services = standalone_service_manifest()
    ui = sports_venue_event_operations_standalone_workbench_blueprint()
    agent = composed_agent_contribution()
    checks = (
        {"id": "runtime_contract", "ok": runtime_evidence["ok"]},
        {"id": "documentation", "ok": docs["ok"]},
        {"id": "standalone_manifest", "ok": standalone["ok"]},
        {"id": "standalone_smoke", "ok": smoke["ok"]},
        {"id": "service_surface", "ok": services["ok"]},
        {"id": "ui_surface", "ok": ui["ok"]},
        {"id": "agent_surface", "ok": agent["ok"]},
    )
    return {
        "ok": all(check["ok"] for check in checks),
        "pbc": "sports_venue_event_operations",
        "checks": checks,
        "runtime": runtime_evidence,
        "documentation": docs,
        "standalone_app": standalone,
        "smoke": smoke,
        "services": services,
        "ui": ui,
        "agent": agent,
        "side_effects": (),
    }


def release_readiness_manifest():
    evidence = build_release_evidence()
    return {
        "ok": evidence["ok"],
        "pbc": evidence["pbc"],
        "sections": (
            "schema",
            "services",
            "events",
            "handlers",
            "ui",
            "agent",
            "governance",
            "standalone_app",
            "documentation",
        ),
        "blocking_gaps": tuple(check["id"] for check in evidence["checks"] if not check["ok"]),
        "boundary_gaps": (),
        "evidence": evidence,
        "side_effects": (),
    }


def validate_release_evidence():
    manifest = release_readiness_manifest()
    return {
        "ok": manifest["ok"],
        "pbc": manifest["pbc"],
        "missing_sections": (),
        "failed_checks": tuple(manifest["blocking_gaps"]),
        "boundary_gaps": (),
        "side_effects": (),
    }


def smoke_test():
    return {"ok": release_readiness_manifest()["ok"] and validate_release_evidence()["ok"], "side_effects": ()}
