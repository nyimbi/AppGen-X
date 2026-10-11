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


# The evidence sections this package is expected to carry. `sections` is read
# off the evidence the package actually builds, so dropping one here fails the
# manifest rather than silently shrinking the requirement to match.
REQUIRED_SECTIONS = (
    "scenario",
    "workbench",
    "world_class_domain_depth",
    "domain_depth_smoke",
)


def release_readiness_manifest():
    evidence = build_release_evidence()
    sections = tuple(
        name for name in REQUIRED_SECTIONS if isinstance(evidence.get(name), dict)
    )
    return {
        "ok": evidence["ok"] and bool(evidence["checks"]),
        "pbc": PBC_KEY,
        "format": evidence.get("format"),
        "sections": sections,
        "required_sections": REQUIRED_SECTIONS,
        "checks": evidence["checks"],
        "blocking_gaps": evidence["blocking_gaps"],
        "boundary_gaps": evidence["boundary_gaps"],
        "side_effects": (),
    }


def validate_release_evidence():
    evidence = build_release_evidence()
    manifest = release_readiness_manifest()
    missing_sections = tuple(
        section for section in manifest["required_sections"] if section not in manifest["sections"]
    )
    failed = tuple(check for check in evidence["checks"] if not check["ok"])
    return {
        "ok": evidence["ok"] and not failed and not missing_sections,
        "pbc": PBC_KEY,
        "manifest": manifest,
        "missing_sections": missing_sections,
        "failed_checks": failed,
        "boundary_gaps": evidence["boundary_gaps"],
        "blocking_gaps": evidence["blocking_gaps"],
        "side_effects": (),
    }


def smoke_test():
    validation = validate_release_evidence()
    return {"ok": validation["ok"], "validation": validation, "side_effects": ()}
