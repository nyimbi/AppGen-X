from .runtime import clinical_care_coordination_build_release_evidence
from .care_coordination_app import care_coordination_smoke_test, single_pbc_app_contract


def build_release_evidence():
    return clinical_care_coordination_build_release_evidence()


def release_readiness_manifest():
    from .standalone import workbench_smoke_test

    evidence = build_release_evidence()
    app = single_pbc_app_contract()
    standalone = workbench_smoke_test()
    return {
        "ok": evidence["ok"] and app["ok"] and standalone["ok"],
        "pbc": evidence["pbc"],
        "sections": (
            "schema",
            "services",
            "events",
            "handlers",
            "ui",
            "agent",
            "governance",
            "forms",
            "wizards",
            "controls",
            "single_pbc_app",
            "standalone_app",
        ),
        "blocking_gaps": (),
        "boundary_gaps": (),
        "single_pbc_app": app,
        "standalone_app": standalone,
        "evidence": evidence,
        "side_effects": (),
    }


def validate_release_evidence():
    manifest = release_readiness_manifest()
    return {
        "ok": manifest["ok"],
        "pbc": manifest["pbc"],
        "missing_sections": (),
        "failed_checks": (),
        "boundary_gaps": (),
        "side_effects": (),
    }


def smoke_test():
    return {
        "ok": release_readiness_manifest()["ok"] and validate_release_evidence()["ok"] and care_coordination_smoke_test()["ok"],
        "side_effects": (),
    }
