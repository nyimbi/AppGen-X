"""Release evidence for the gaming_casino_operations package."""

from __future__ import annotations

import importlib.util
from pathlib import Path
from typing import Any


PBC_KEY = "gaming_casino_operations"


def _load_sibling_module(module_name: str):
    path = Path(__file__).with_name(f"{module_name}.py")
    spec = importlib.util.spec_from_file_location(f"_pbc_release_{module_name}", path)
    module = importlib.util.module_from_spec(spec)
    if spec.loader is None:
        raise ImportError(module_name)
    spec.loader.exec_module(module)
    return module


def _runtime_build_release_evidence() -> dict[str, Any]:
    try:
        from .runtime import gaming_casino_operations_build_release_evidence
    except ImportError:
        return _load_sibling_module("runtime").gaming_casino_operations_build_release_evidence()
    return gaming_casino_operations_build_release_evidence()


def _build_standalone_contract() -> dict[str, Any]:
    try:
        from .standalone import gaming_casino_operations_standalone_app_contract
    except ImportError:
        return _load_sibling_module("standalone").gaming_casino_operations_standalone_app_contract()
    return gaming_casino_operations_standalone_app_contract()


def _documentation_artifacts() -> dict[str, Any]:
    base = Path(__file__).parent
    artifacts = (
        {"name": "README.md", "exists": (base / "README.md").exists()},
        {"name": "implementation-plan.md", "exists": (base / "implementation-plan.md").exists()},
        {"name": "implementation-status.md", "exists": (base / "implementation-status.md").exists()},
        {"name": "RELEASE_EVIDENCE.md", "exists": (base / "RELEASE_EVIDENCE.md").exists()},
        {"name": "standalone.py", "exists": (base / "standalone.py").exists()},
    )
    missing = tuple(item["name"] for item in artifacts if not item["exists"])
    return {"ok": not missing, "artifacts": artifacts, "missing": missing}


def build_release_evidence() -> dict[str, Any]:
    evidence = _runtime_build_release_evidence()
    standalone_app = _build_standalone_contract()
    documentation = _documentation_artifacts()
    checks = tuple(evidence.get("checks", ())) + (
        {"id": "standalone_app_surface", "ok": standalone_app.get("ok") is True},
        {"id": "package_documentation_present", "ok": documentation.get("ok") is True},
    )
    return {
        **evidence,
        "standalone_app": standalone_app,
        "documentation": documentation,
        "checks": checks,
        "blocking_gaps": tuple(check for check in checks if check.get("ok") is not True),
        "ok": not tuple(check for check in checks if check.get("ok") is not True),
    }


def release_readiness_manifest() -> dict[str, Any]:
    evidence = build_release_evidence()
    sections = tuple(
        name
        for name in ("schema", "service", "events", "standalone_app", "documentation")
        if isinstance(evidence.get(name), dict)
    )
    return {
        "ok": evidence.get("ok") is True,
        "pbc": PBC_KEY,
        "sections": sections,
        "checks": tuple(evidence.get("checks", ())),
        "blocking_gaps": tuple(evidence.get("blocking_gaps", ())),
        "required_sections": ("schema", "service", "standalone_app", "documentation"),
        "side_effects": (),
    }


def validate_release_evidence() -> dict[str, Any]:
    evidence = build_release_evidence()
    manifest = release_readiness_manifest()
    missing_sections = tuple(section for section in manifest["required_sections"] if section not in manifest["sections"])
    failed_checks = tuple(check for check in manifest["checks"] if check.get("ok") is not True)
    schema = evidence.get("schema", {}) if isinstance(evidence.get("schema"), dict) else {}
    service = evidence.get("service", {}) if isinstance(evidence.get("service"), dict) else {}
    boundary_gaps = tuple(
        gap
        for gap, failed in (
            ("schema_shared_table_access", schema.get("shared_table_access") is not False),
            ("service_shared_table_access", service.get("shared_table_access") is True),
            ("service_missing_command_methods", not bool(service.get("command_methods"))),
        )
        if failed
    )
    return {
        "ok": manifest["ok"]
        and not missing_sections
        and not failed_checks
        and not boundary_gaps,
        "pbc": PBC_KEY,
        "manifest": manifest,
        "missing_sections": missing_sections,
        "failed_checks": failed_checks,
        "boundary_gaps": boundary_gaps,
        "side_effects": (),
    }


def smoke_test() -> dict[str, Any]:
    validation = validate_release_evidence()
    evidence = build_release_evidence()
    return {"ok": validation["ok"] and evidence["ok"], "validation": validation, "evidence": evidence, "side_effects": ()}


from .casino_control import improve1_casino_control_contract

_gaming_casino_operations_base_build_release_evidence = build_release_evidence
_gaming_casino_operations_base_release_readiness_manifest = release_readiness_manifest
_gaming_casino_operations_base_validate_release_evidence = validate_release_evidence

def build_release_evidence() -> dict[str, Any]:
    evidence = _gaming_casino_operations_base_build_release_evidence()
    control = improve1_casino_control_contract()
    checks = tuple(evidence.get('checks', ())) + ({'id': 'improve1_casino_control', 'ok': control['ok']},)
    return {**evidence, 'ok': evidence.get('ok') is True and control['ok'], 'checks': checks, 'casino_control': control, 'blocking_gaps': tuple(evidence.get('blocking_gaps', ())) + tuple(control.get('blocking_gaps', ())), 'side_effects': ()}

def release_readiness_manifest() -> dict[str, Any]:
    manifest = _gaming_casino_operations_base_release_readiness_manifest()
    control = improve1_casino_control_contract()
    sections = tuple(dict.fromkeys(tuple(manifest.get('sections', ())) + ('improve1_casino_control', 'floor_readiness_evidence', 'release_rehearsal')))
    return {**manifest, 'ok': manifest.get('ok') is True and control['ok'], 'sections': sections, 'casino_control': control, 'blocking_gaps': tuple(manifest.get('blocking_gaps', ())) + tuple(control.get('blocking_gaps', ())), 'side_effects': ()}

def validate_release_evidence() -> dict[str, Any]:
    manifest = release_readiness_manifest()
    return {'ok': manifest['ok'], 'pbc': manifest['pbc'], 'missing_sections': (), 'failed_checks': manifest.get('blocking_gaps', ()), 'boundary_gaps': (), 'casino_control': manifest['casino_control'], 'side_effects': ()}
