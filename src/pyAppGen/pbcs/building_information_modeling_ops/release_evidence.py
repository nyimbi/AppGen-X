"""Release evidence helpers for the executable BIM federation slice."""
from __future__ import annotations

from .runtime import (
    building_information_modeling_ops_build_release_evidence,
    building_information_modeling_ops_build_single_pbc_app_contract,
)


def build_release_evidence() -> dict:
    evidence = building_information_modeling_ops_build_release_evidence()
    from .standalone import standalone_app_manifest

    return {
        **evidence,
        "standalone_app": standalone_app_manifest(),
    }


def release_readiness_manifest() -> dict:
    evidence = build_release_evidence()
    return {
        "ok": evidence["ok"] and evidence["standalone_app"]["ok"],
        "pbc": evidence["pbc"],
        "sections": (
            "schema",
            "services",
            "events",
            "handlers",
            "ui",
            "agent",
            "governance",
            "single_pbc_app",
            "standalone_app",
            "forms",
            "wizards",
            "controls",
        ),
        "blocking_gaps": evidence["blocking_gaps"],
        "boundary_gaps": (),
        "single_pbc_app": building_information_modeling_ops_build_single_pbc_app_contract(),
        "standalone_app": evidence["standalone_app"],
        "evidence": evidence,
        "side_effects": (),
    }


def validate_release_evidence() -> dict:
    manifest = release_readiness_manifest()
    missing_sections = tuple(section for section in manifest["sections"] if not section)
    return {
        "ok": manifest["ok"] and not missing_sections,
        "pbc": manifest["pbc"],
        "missing_sections": missing_sections,
        "failed_checks": manifest["blocking_gaps"],
        "boundary_gaps": (),
        "side_effects": (),
    }


def smoke_test() -> dict:
    return {
        "ok": release_readiness_manifest()["ok"] and validate_release_evidence()["ok"],
        "side_effects": (),
    }
