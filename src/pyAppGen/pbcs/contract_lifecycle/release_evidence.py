"""Release evidence for the contract_lifecycle PBC."""

from .app_surface import app_surface_smoke_test, single_pbc_contract_lifecycle_app_contract
from .application import PBC_KEY, release_evidence
from .domain_depth import domain_depth_contract, domain_depth_smoke_test


def build_release_evidence():
    evidence = release_evidence()
    domain = domain_depth_contract()
    smoke = domain_depth_smoke_test()
    app_surface = app_surface_smoke_test()
    standalone = single_pbc_contract_lifecycle_app_contract()
    checks = tuple(evidence["checks"]) + (
        {"id": "world_class_domain_depth", "ok": domain["ok"]},
        {"id": "domain_depth_smoke", "ok": smoke["ok"]},
        {"id": "standalone_app_surface", "ok": app_surface["ok"]},
        {"id": "standalone_forms_wizards_controls", "ok": standalone["forms"]["ok"] and standalone["wizards"]["ok"] and standalone["controls"]["ok"]},
    )
    return {
        **evidence,
        "ok": evidence["ok"] and domain["ok"] and smoke["ok"] and app_surface["ok"] and standalone["ok"],
        "checks": checks,
        "world_class_domain_depth": domain,
        "domain_depth_smoke": smoke,
        "standalone_app": standalone,
        "standalone_app_smoke": app_surface,
        "blocking_gaps": tuple(check for check in checks if not check["ok"]),
    }


def contract_lifecycle_build_release_evidence():
    return build_release_evidence()


def release_readiness_manifest():
    evidence = build_release_evidence()
    return {
        "ok": evidence["ok"],
        "pbc": PBC_KEY,
        "sections": (
            "schema",
            "services",
            "routes",
            "events",
            "handlers",
            "ui",
            "agent",
            "governance",
            "release_scenario",
            "tests",
        ),
        "checks": evidence["checks"],
        "blocking_gaps": evidence["blocking_gaps"],
        "boundary_gaps": evidence["boundary_gaps"],
    }


def validate_release_evidence():
    evidence = build_release_evidence()
    failed = tuple(check for check in evidence["checks"] if not check["ok"])
    return {
        "ok": evidence["ok"] and not failed,
        "failed_checks": failed,
        "boundary_gaps": evidence["boundary_gaps"],
        "blocking_gaps": evidence["blocking_gaps"],
    }


def smoke_test():
    validation = validate_release_evidence()
    return {"ok": validation["ok"], "validation": validation}
