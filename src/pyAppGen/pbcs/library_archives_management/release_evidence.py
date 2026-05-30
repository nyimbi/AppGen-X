"""Release evidence wrappers for the Library and Archives Management PBC."""

from __future__ import annotations

import importlib.util
from pathlib import Path

from .runtime import library_archives_management_build_release_evidence as _runtime_build_release_evidence

PBC_KEY = "library_archives_management"



def _load_sibling_module(module_name: str):
    """Load a sibling module when imported directly outside the package context."""
    path = Path(__file__).with_name(f"{module_name}.py")
    spec = importlib.util.spec_from_file_location(f"_pbc_release_{module_name}", path)
    module = importlib.util.module_from_spec(spec)
    if spec.loader is None:
        raise ImportError(module_name)
    spec.loader.exec_module(module)
    return module



def _build_schema_contract():
    try:
        from .schema_contract import build_schema_contract
    except ImportError:
        return _load_sibling_module("schema_contract").build_schema_contract()
    return build_schema_contract()



def _build_service_contract():
    try:
        from .service_contract import build_service_contract
    except ImportError:
        return _load_sibling_module("service_contract").build_service_contract()
    return build_service_contract()



def _build_ui_contract():
    try:
        from .ui import library_archives_management_ui_contract
    except ImportError:
        return _load_sibling_module("ui").library_archives_management_ui_contract()
    return library_archives_management_ui_contract()



def _build_forms_contract():
    try:
        from .forms import library_archives_management_form_catalog
    except ImportError:
        return _load_sibling_module("forms").library_archives_management_form_catalog()
    return library_archives_management_form_catalog()



def _build_wizard_contract():
    try:
        from .wizards import library_archives_management_wizard_catalog
    except ImportError:
        return _load_sibling_module("wizards").library_archives_management_wizard_catalog()
    return library_archives_management_wizard_catalog()



def _build_control_contract():
    try:
        from .controls import library_archives_management_control_catalog
    except ImportError:
        return _load_sibling_module("controls").library_archives_management_control_catalog()
    return library_archives_management_control_catalog()



def _build_standalone_contract():
    try:
        from .standalone import library_archives_management_standalone_app_contract
    except ImportError:
        return _load_sibling_module("standalone").library_archives_management_standalone_app_contract()
    return library_archives_management_standalone_app_contract()



def _documentation_artifacts() -> dict:
    base = Path(__file__).parent
    artifacts = (
        {"name": "README.md", "exists": (base / "README.md").exists()},
        {"name": "implementation-plan.md", "exists": (base / "implementation-plan.md").exists()},
        {"name": "implementation-status.md", "exists": (base / "implementation-status.md").exists()},
        {"name": "RELEASE_EVIDENCE.md", "exists": (base / "RELEASE_EVIDENCE.md").exists()},
    )
    missing = tuple(item["name"] for item in artifacts if not item["exists"])
    return {
        "ok": not missing,
        "artifacts": artifacts,
        "missing": missing,
    }



def build_release_evidence() -> dict:
    """Return executable release evidence for the standalone package slice."""
    evidence = dict(_runtime_build_release_evidence())
    evidence["schema"] = _build_schema_contract()
    evidence["service"] = _build_service_contract()
    evidence["ui"] = _build_ui_contract()
    evidence["forms"] = _build_forms_contract()
    evidence["wizards"] = _build_wizard_contract()
    evidence["controls"] = _build_control_contract()
    evidence["standalone_app"] = _build_standalone_contract()
    evidence["documentation"] = _documentation_artifacts()
    extra_checks = (
        {"id": "ui_contract_surface", "ok": evidence["ui"].get("ok") is True},
        {"id": "forms_surface", "ok": evidence["forms"].get("ok") is True},
        {"id": "wizard_surface", "ok": evidence["wizards"].get("ok") is True},
        {"id": "control_surface", "ok": evidence["controls"].get("ok") is True},
        {"id": "standalone_app_surface", "ok": evidence["standalone_app"].get("ok") is True},
        {"id": "package_documentation_present", "ok": evidence["documentation"].get("ok") is True},
    )
    evidence["checks"] = tuple(evidence.get("checks", ())) + extra_checks
    evidence["blocking_gaps"] = tuple(check for check in evidence["checks"] if check.get("ok") is not True)
    evidence["ok"] = not evidence["blocking_gaps"]
    return evidence



def release_readiness_manifest() -> dict:
    """Return side-effect-free release readiness metadata."""
    evidence = build_release_evidence()
    sections = tuple(
        section
        for section in (
            "schema",
            "service",
            "ui",
            "forms",
            "wizards",
            "controls",
            "standalone_app",
            "documentation",
        )
        if isinstance(evidence.get(section), dict)
    )
    return {
        "ok": evidence.get("ok") is True and bool(evidence.get("checks")),
        "pbc": PBC_KEY,
        "sections": sections,
        "blocking_gaps": tuple(evidence.get("blocking_gaps", ())),
        "checks": tuple(evidence.get("checks", ())),
        "side_effects": (),
    }



def validate_release_evidence() -> dict:
    """Validate release evidence, required sections, and boundary claims."""
    evidence = build_release_evidence()
    manifest = release_readiness_manifest()
    missing_sections = tuple(
        section
        for section in ("schema", "service", "ui", "forms", "wizards", "controls", "standalone_app")
        if section not in manifest["sections"]
    )
    failed_checks = tuple(check for check in manifest["checks"] if check.get("ok") is not True)
    boundary_gaps = tuple(
        gap
        for gap, failed in (
            ("schema_shared_table_access", evidence["schema"].get("shared_table_access") is not False),
            ("service_missing_commands", not bool(evidence["service"].get("command_methods"))),
            ("standalone_missing_domain_coverage", bool(evidence["standalone_app"].get("missing_domain_areas"))),
        )
        if failed
    )
    return {
        "ok": manifest["ok"] and not missing_sections and not failed_checks and not boundary_gaps,
        "pbc": PBC_KEY,
        "manifest": manifest,
        "missing_sections": missing_sections,
        "failed_checks": failed_checks,
        "boundary_gaps": boundary_gaps,
        "side_effects": (),
    }



def smoke_test() -> dict:
    """Exercise release evidence validation side-effect-free."""
    evidence = build_release_evidence()
    validation = validate_release_evidence()
    return {
        "ok": evidence["ok"] and validation["ok"],
        "evidence": evidence,
        "validation": validation,
        "side_effects": (),
    }
