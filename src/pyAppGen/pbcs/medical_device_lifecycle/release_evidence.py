"""Release evidence for the medical_device_lifecycle PBC."""

from __future__ import annotations

from pathlib import Path

from . import agent
from . import controls
from . import forms
from . import standalone
from . import ui
from . import wizards
from .runtime import medical_device_lifecycle_build_api_contract
from .runtime import medical_device_lifecycle_build_release_evidence as runtime_build_release_evidence
from .runtime import medical_device_lifecycle_build_schema_contract
from .runtime import medical_device_lifecycle_build_service_contract
from .runtime import medical_device_lifecycle_permissions_contract

PBC_KEY = "medical_device_lifecycle"
PACKAGE_DIR = Path(__file__).parent


def build_release_evidence() -> dict:
    """Return generated release audit evidence for this PBC."""
    runtime_evidence = runtime_build_release_evidence()
    return {
        **runtime_evidence,
        "pbc": PBC_KEY,
        "schema": medical_device_lifecycle_build_schema_contract(),
        "service": medical_device_lifecycle_build_service_contract(),
        "api": medical_device_lifecycle_build_api_contract(),
        "permissions": medical_device_lifecycle_permissions_contract(),
        "ui": ui.medical_device_lifecycle_ui_contract(),
        "forms": forms.medical_device_lifecycle_form_catalog(),
        "wizards": wizards.medical_device_lifecycle_wizard_catalog(),
        "controls": controls.medical_device_lifecycle_control_catalog(),
        "assistant": agent.composed_agent_contribution(),
        "standalone_app": standalone.medical_device_lifecycle_standalone_app_contract(),
        "docs_present": {
            "SPECIFICATION.md": PACKAGE_DIR.joinpath("SPECIFICATION.md").exists(),
            "RELEASE_EVIDENCE.md": PACKAGE_DIR.joinpath("RELEASE_EVIDENCE.md").exists(),
            "implementation-plan.md": PACKAGE_DIR.joinpath("implementation-plan.md").exists(),
            "forms.py": PACKAGE_DIR.joinpath("forms.py").exists(),
            "wizards.py": PACKAGE_DIR.joinpath("wizards.py").exists(),
            "controls.py": PACKAGE_DIR.joinpath("controls.py").exists(),
            "standalone.py": PACKAGE_DIR.joinpath("standalone.py").exists(),
        },
    }


def release_readiness_manifest() -> dict:
    """Return side-effect-free release evidence coverage and gate metadata."""
    evidence = build_release_evidence()
    sections = tuple(
        name
        for name in ("schema", "service", "api", "permissions", "ui", "forms", "wizards", "controls", "assistant", "standalone_app")
        if isinstance(evidence.get(name), dict)
    )
    checks = tuple(evidence.get("checks", ()))
    docs_present = evidence.get("docs_present", {})
    blocking_gaps = tuple(evidence.get("blocking_gaps", ())) + tuple(name for name, present in docs_present.items() if not present)
    return {
        "ok": evidence.get("ok") is True and bool(checks) and not blocking_gaps,
        "pbc": PBC_KEY,
        "format": evidence.get("format"),
        "sections": sections,
        "checks": checks,
        "blocking_gaps": blocking_gaps,
        "required_sections": ("schema", "service", "api", "permissions", "ui", "forms", "wizards", "controls", "assistant", "standalone_app"),
        "docs_present": docs_present,
        "side_effects": (),
    }


def validate_release_evidence() -> dict:
    """Validate release evidence, blocking gaps, and owned-boundary proof."""
    evidence = build_release_evidence()
    manifest = release_readiness_manifest()
    missing_sections = tuple(section for section in manifest["required_sections"] if section not in manifest["sections"])
    failed_checks = tuple(check for check in manifest["checks"] if check.get("ok") is not True)
    schema = evidence.get("schema", {})
    service = evidence.get("service", {})
    standalone_app = evidence.get("standalone_app", {})
    boundary_gaps = tuple(
        gap
        for gap, failed in (
            ("schema_shared_table_access", schema.get("shared_table_access") is not False),
            ("service_shared_table_access", service.get("shared_table_access") is True),
            ("missing_forms", not evidence.get("forms", {}).get("ok")),
            ("missing_wizards", not evidence.get("wizards", {}).get("ok")),
            ("missing_controls", not evidence.get("controls", {}).get("ok")),
            ("missing_assistant", not evidence.get("assistant", {}).get("ok")),
            ("missing_standalone_app", not standalone_app.get("ok")),
            ("invalid_standalone_boundary", not standalone_app.get("owned_boundary", {}).get("ok")),
        )
        if failed
    )
    return {
        "ok": manifest["ok"]
        and evidence.get("pbc", PBC_KEY) == manifest["pbc"]
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


def smoke_test() -> dict:
    validation = validate_release_evidence()
    evidence = build_release_evidence()
    return {"ok": validation["ok"] and evidence.get("ok") is True, "validation": validation, "evidence": evidence, "side_effects": ()}


# Improve1 medical device control release evidence extension.
from .medical_device_control import improve1_medical_device_control_contract as _medical_device_control_contract

_MEDICAL_DEVICE_LIFECYCLE_BASE_BUILD_RELEASE_EVIDENCE = build_release_evidence
_MEDICAL_DEVICE_LIFECYCLE_BASE_RELEASE_READINESS_MANIFEST = release_readiness_manifest
_MEDICAL_DEVICE_LIFECYCLE_BASE_VALIDATE_RELEASE_EVIDENCE = validate_release_evidence


def build_release_evidence():
    evidence = dict(_MEDICAL_DEVICE_LIFECYCLE_BASE_BUILD_RELEASE_EVIDENCE())
    control = _medical_device_control_contract()
    checks = tuple(evidence.get("checks", ())) + ({"id": "medical_device_control_contract", "ok": control["ok"]}, {"id": "medical_device_control_traceability", "ok": control["capability_count"] == 50})
    evidence.update({"medical_device_control": control, "medical_device_lifecycle_controls": tuple(item["evidence"] for item in control["capabilities"]), "checks": checks, "blocking_gaps": tuple(check for check in checks if check.get("ok") is not True)})
    evidence["ok"] = not evidence["blocking_gaps"]
    return evidence


def release_readiness_manifest():
    manifest = dict(_MEDICAL_DEVICE_LIFECYCLE_BASE_RELEASE_READINESS_MANIFEST())
    evidence = build_release_evidence()
    manifest.update({"ok": evidence["ok"], "evidence": evidence, "sections": tuple(dict.fromkeys(tuple(manifest.get("sections", ())) + ("medical_device_control", "improve1_traceability"))), "blocking_gaps": evidence["blocking_gaps"]})
    return manifest


def validate_release_evidence():
    base = dict(_MEDICAL_DEVICE_LIFECYCLE_BASE_VALIDATE_RELEASE_EVIDENCE())
    evidence = build_release_evidence(); control = evidence["medical_device_control"]
    failed = tuple(check for check in evidence["checks"] if check.get("ok") is not True)
    base.update({"ok": base.get("ok") is True and evidence["ok"] and control["ok"] and not failed, "failed_checks": tuple(base.get("failed_checks", ())) + failed, "medical_device_control": control})
    return base
