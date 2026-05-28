"""Release evidence for the contract_lifecycle PBC."""

from .application import PBC_KEY, release_evidence
from .domain_depth import domain_depth_contract, domain_depth_smoke_test


def build_release_evidence():
    evidence = release_evidence()
    domain = domain_depth_contract()
    smoke = domain_depth_smoke_test()
    checks = tuple(evidence["checks"]) + (
        {"id": "world_class_domain_depth", "ok": domain["ok"]},
        {"id": "domain_depth_smoke", "ok": smoke["ok"]},
    )
    return {
        **evidence,
        "ok": evidence["ok"] and domain["ok"] and smoke["ok"],
        "checks": checks,
        "world_class_domain_depth": domain,
        "domain_depth_smoke": smoke,
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
