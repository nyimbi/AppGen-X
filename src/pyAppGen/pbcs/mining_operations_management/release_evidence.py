"""Generated release evidence for the Mining Operations Management PBC."""

from __future__ import annotations

from pathlib import Path

from .controls import mining_operations_management_control_catalog
from .forms import mining_operations_management_form_catalog
from .runtime import mining_operations_management_build_release_evidence
from .runtime import mining_operations_management_build_schema_contract
from .runtime import mining_operations_management_build_service_contract
from .standalone import mining_operations_management_standalone_app_contract
from .ui import mining_operations_management_ui_contract
from .wizards import mining_operations_management_wizard_catalog


def _documentation_artifacts():
    base = Path(__file__).parent
    artifacts = (
        {"name": "SPECIFICATION.md", "exists": (base / "SPECIFICATION.md").exists()},
        {"name": "improve1.md", "exists": (base / "improve1.md").exists()},
        {"name": "implementation-plan.md", "exists": (base / "implementation-plan.md").exists()},
        {"name": "RELEASE_EVIDENCE.md", "exists": (base / "RELEASE_EVIDENCE.md").exists()},
    )
    missing = tuple(item["name"] for item in artifacts if not item["exists"])
    return {"ok": not missing, "artifacts": artifacts, "missing": missing}


def build_release_evidence():
    evidence = dict(mining_operations_management_build_release_evidence())
    schema_contract = mining_operations_management_build_schema_contract()
    service_contract = mining_operations_management_build_service_contract()
    ui_contract = mining_operations_management_ui_contract()
    form_catalog = mining_operations_management_form_catalog()
    wizard_catalog = mining_operations_management_wizard_catalog()
    control_catalog = mining_operations_management_control_catalog()
    standalone_app = mining_operations_management_standalone_app_contract()
    documentation = _documentation_artifacts()
    extra_checks = (
        {"id": "standalone_app_surface", "ok": standalone_app["ok"]},
        {"id": "ui_forms_wizards_controls", "ok": ui_contract["ok"] and form_catalog["ok"] and wizard_catalog["ok"] and control_catalog["ok"]},
        {"id": "package_documentation_present", "ok": documentation["ok"]},
    )
    evidence["schema"] = schema_contract
    evidence["service"] = service_contract
    evidence["ui"] = ui_contract
    evidence["forms"] = form_catalog
    evidence["wizards"] = wizard_catalog
    evidence["controls"] = control_catalog
    evidence["standalone_app"] = standalone_app
    evidence["documentation"] = documentation
    evidence["checks"] = tuple(evidence.get("checks", ())) + extra_checks
    evidence["blocking_gaps"] = tuple(check for check in evidence["checks"] if check.get("ok") is not True)
    evidence["ok"] = not evidence["blocking_gaps"]
    return evidence


def release_readiness_manifest():
    evidence = build_release_evidence()
    sections = tuple(
        name
        for name in ("schema", "service", "ui", "forms", "wizards", "controls", "standalone_app", "documentation")
        if evidence.get(name) is not None
    )
    return {
        "ok": evidence["ok"],
        "pbc": evidence["pbc"],
        "sections": sections,
        "blocking_gaps": tuple(evidence.get("blocking_gaps", ())),
        "boundary_gaps": (),
        "evidence": evidence,
        "side_effects": (),
    }


def validate_release_evidence():
    manifest = release_readiness_manifest()
    evidence = manifest["evidence"]
    missing_sections = tuple(
        section
        for section in ("schema", "service", "standalone_app", "documentation")
        if section not in manifest["sections"]
    )
    failed_checks = tuple(check for check in manifest["evidence"]["checks"] if check.get("ok") is not True)
    boundary_gaps = tuple(
        gap
        for gap, failed in (
            ("schema_shared_table_access", evidence["schema"].get("shared_table_access") is True),
            ("service_missing_commands", not bool(evidence["service"].get("command_methods"))),
            ("ui_shared_table_access", evidence["ui"]["binding_evidence"].get("shared_table_access") is True),
            ("missing_forms", not bool(evidence["forms"]["forms"])),
            ("missing_wizards", not bool(evidence["wizards"]["wizards"])),
            ("missing_controls", not bool(evidence["controls"]["controls"])),
        )
        if failed
    )
    return {
        "ok": manifest["ok"] and not missing_sections and not failed_checks and not boundary_gaps,
        "pbc": manifest["pbc"],
        "missing_sections": missing_sections,
        "failed_checks": failed_checks,
        "boundary_gaps": boundary_gaps,
        "side_effects": (),
    }


def smoke_test():
    validation = validate_release_evidence()
    return {
        "ok": release_readiness_manifest()["ok"] and validation["ok"],
        "validation": validation,
        "side_effects": (),
    }

# Improve1 mining operations control release evidence extension.
from .mining_operations_control import improve1_mining_operations_control_contract as _mining_operations_control_contract

_MINING_OPERATIONS_MANAGEMENT_BASE_BUILD_RELEASE_EVIDENCE = build_release_evidence
_MINING_OPERATIONS_MANAGEMENT_BASE_RELEASE_READINESS_MANIFEST = release_readiness_manifest
_MINING_OPERATIONS_MANAGEMENT_BASE_VALIDATE_RELEASE_EVIDENCE = validate_release_evidence


def build_release_evidence():
    evidence = dict(_MINING_OPERATIONS_MANAGEMENT_BASE_BUILD_RELEASE_EVIDENCE())
    control = _mining_operations_control_contract()
    checks = tuple(evidence.get("checks", ())) + ({"id": "mining_operations_control_contract", "ok": control["ok"]}, {"id": "mining_operations_control_traceability", "ok": control["capability_count"] == 50})
    evidence.update({"mining_operations_control": control, "mining_operations_management_controls": tuple(item["evidence"] for item in control["capabilities"]), "checks": checks, "blocking_gaps": tuple(check for check in checks if check.get("ok") is not True)})
    evidence["ok"] = not evidence["blocking_gaps"]
    return evidence


def release_readiness_manifest():
    manifest = dict(_MINING_OPERATIONS_MANAGEMENT_BASE_RELEASE_READINESS_MANIFEST())
    evidence = build_release_evidence()
    manifest.update({"ok": evidence["ok"], "evidence": evidence, "sections": tuple(dict.fromkeys(tuple(manifest.get("sections", ())) + ("mining_operations_control", "improve1_traceability"))), "blocking_gaps": evidence["blocking_gaps"]})
    return manifest


def validate_release_evidence():
    base = dict(_MINING_OPERATIONS_MANAGEMENT_BASE_VALIDATE_RELEASE_EVIDENCE())
    evidence = build_release_evidence()
    control = evidence["mining_operations_control"]
    failed = tuple(check for check in evidence["checks"] if check.get("ok") is not True)
    base.update({"ok": base.get("ok") is True and evidence["ok"] and control["ok"] and not failed, "failed_checks": tuple(base.get("failed_checks", ())) + failed, "mining_operations_control": control})
    return base
