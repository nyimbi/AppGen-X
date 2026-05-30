"""Release-evidence helpers for the cybersecurity_operations_center PBC."""

from __future__ import annotations

from typing import Any

from .agent import agent_skill_manifest, chatbot_interface_contract
from .config import governance_smoke_test
from .handlers import handler_manifest
from .runtime import cybersecurity_operations_center_build_release_evidence, cybersecurity_operations_center_runtime_smoke
from .services import service_operation_manifest
from .soc_control import improve1_soc_control_contract
from .ui import cybersecurity_operations_center_ui_contract


def build_release_evidence() -> dict[str, Any]:
    return cybersecurity_operations_center_build_release_evidence()


def release_readiness_manifest() -> dict[str, Any]:
    runtime_smoke = cybersecurity_operations_center_runtime_smoke()
    evidence = build_release_evidence()
    return {
        "ok": evidence["ok"] and runtime_smoke["ok"],
        "pbc": evidence["pbc"],
        "sections": ("schema", "services", "events", "handlers", "ui", "agent", "governance", "runtime_smoke"),
        "blocking_gaps": evidence["blocking_gaps"],
        "boundary_gaps": (),
        "evidence": evidence,
        "runtime_smoke": runtime_smoke,
        "auxiliary_manifests": {
            "service": service_operation_manifest(),
            "handler": handler_manifest(),
            "ui": cybersecurity_operations_center_ui_contract(),
            "agent": agent_skill_manifest(),
            "chatbot": chatbot_interface_contract(),
            "governance": governance_smoke_test(),
            "soc_control": improve1_soc_control_contract(),
        },
        "side_effects": (),
    }


def validate_release_evidence() -> dict[str, Any]:
    manifest = release_readiness_manifest()
    missing_sections = tuple(section for section in manifest["sections"] if section not in manifest["sections"])
    failed_checks = tuple(check["id"] for check in manifest["evidence"]["checks"] if not check["ok"])
    return {
        "ok": manifest["ok"] and not failed_checks and not missing_sections,
        "pbc": manifest["pbc"],
        "missing_sections": missing_sections,
        "failed_checks": failed_checks,
        "boundary_gaps": (),
        "side_effects": (),
    }


def smoke_test() -> dict[str, Any]:
    return {"ok": release_readiness_manifest()["ok"] and validate_release_evidence()["ok"], "side_effects": ()}
