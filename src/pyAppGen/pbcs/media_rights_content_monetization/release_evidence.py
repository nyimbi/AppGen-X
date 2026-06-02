"""Generated release evidence for the media_rights_content_monetization PBC."""

from __future__ import annotations

from pathlib import Path

from . import agent
from . import controls
from . import forms
from . import standalone
from . import ui
from . import wizards
from .runtime import media_rights_content_monetization_build_api_contract
from .runtime import media_rights_content_monetization_build_release_evidence as runtime_build_release_evidence
from .runtime import media_rights_content_monetization_build_schema_contract
from .runtime import media_rights_content_monetization_build_service_contract
from .runtime import media_rights_content_monetization_permissions_contract

PBC_KEY = "media_rights_content_monetization"
PACKAGE_DIR = Path(__file__).parent



def build_release_evidence():
    runtime_evidence = runtime_build_release_evidence()
    return {
        **runtime_evidence,
        "pbc": PBC_KEY,
        "schema": media_rights_content_monetization_build_schema_contract(),
        "service": media_rights_content_monetization_build_service_contract(),
        "api": media_rights_content_monetization_build_api_contract(),
        "permissions": media_rights_content_monetization_permissions_contract(),
        "ui": ui.media_rights_content_monetization_ui_contract(),
        "forms": forms.media_rights_content_monetization_form_catalog(),
        "wizards": wizards.media_rights_content_monetization_wizard_catalog(),
        "controls": controls.media_rights_content_monetization_control_catalog(),
        "assistant": agent.composed_agent_contribution(),
        "standalone": standalone.media_rights_content_monetization_standalone_app_contract(),
        "standalone_smoke": standalone.media_rights_content_monetization_standalone_smoke(),
        "docs_present": {
            "implementation-plan.md": PACKAGE_DIR.joinpath("implementation-plan.md").exists(),
            "RELEASE_EVIDENCE.md": PACKAGE_DIR.joinpath("RELEASE_EVIDENCE.md").exists(),
        },
        "artifact_presence": {
            "standalone.py": PACKAGE_DIR.joinpath("standalone.py").exists(),
            "forms.py": PACKAGE_DIR.joinpath("forms.py").exists(),
            "wizards.py": PACKAGE_DIR.joinpath("wizards.py").exists(),
            "controls.py": PACKAGE_DIR.joinpath("controls.py").exists(),
        },
    }


RELEASE_EVIDENCE = build_release_evidence()



def release_readiness_manifest():
    evidence = build_release_evidence()
    sections = tuple(
        name
        for name in ("schema", "service", "api", "permissions", "ui", "forms", "wizards", "controls", "assistant", "standalone")
        if isinstance(evidence.get(name), dict)
    )
    checks = tuple(evidence.get("checks", ()))
    docs_present = evidence.get("docs_present", {})
    artifacts = evidence.get("artifact_presence", {})
    blocking_gaps = (
        tuple(evidence.get("blocking_gaps", ()))
        + tuple(name for name, present in docs_present.items() if not present)
        + tuple(name for name, present in artifacts.items() if not present)
    )
    return {
        "ok": evidence.get("ok") is True and bool(checks) and not blocking_gaps,
        "pbc": evidence["pbc"],
        "sections": sections,
        "checks": checks,
        "blocking_gaps": blocking_gaps,
        "boundary_gaps": (),
        "docs_present": docs_present,
        "artifact_presence": artifacts,
        "evidence": evidence,
        "side_effects": (),
    }



def validate_release_evidence():
    manifest = release_readiness_manifest()
    evidence = manifest["evidence"]
    missing_sections = tuple(
        section
        for section in ("schema", "service", "api", "permissions", "ui", "forms", "wizards", "controls", "assistant", "standalone")
        if section not in manifest["sections"]
    )
    failed_checks = tuple(check for check in manifest["checks"] if check.get("ok") is not True)
    standalone_contract = evidence.get("standalone", {})
    required_methods = {
        "create_rights_asset",
        "record_license_agreement",
        "review_distribution_window",
        "approve_usage_record",
        "simulate_royalty_statement",
        "assistant_preview",
        "workbench",
    }
    boundary_gaps = tuple(
        gap
        for gap, failed in (
            ("missing_forms", not evidence.get("forms", {}).get("ok")),
            ("missing_wizards", not evidence.get("wizards", {}).get("ok")),
            ("missing_controls", not evidence.get("controls", {}).get("ok")),
            ("missing_assistant", not evidence.get("assistant", {}).get("ok")),
            ("missing_standalone_contract", not standalone_contract.get("ok")),
            (
                "standalone_missing_required_methods",
                not required_methods <= set(standalone_contract.get("service_methods", ())),
            ),
            (
                "standalone_smoke_failed",
                not evidence.get("standalone_smoke", {}).get("ok"),
            ),
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
    return {
        "ok": release_readiness_manifest()["ok"] and validate_release_evidence()["ok"],
        "side_effects": (),
    }


# Improve1 rights control release evidence extension.
from .rights_control import improve1_rights_control_contract as _rights_control_contract

_MEDIA_RIGHTS_CONTENT_MONETIZATION_BASE_BUILD_RELEASE_EVIDENCE = build_release_evidence
_MEDIA_RIGHTS_CONTENT_MONETIZATION_BASE_RELEASE_READINESS_MANIFEST = release_readiness_manifest
_MEDIA_RIGHTS_CONTENT_MONETIZATION_BASE_VALIDATE_RELEASE_EVIDENCE = validate_release_evidence


def build_release_evidence():
    evidence = dict(_MEDIA_RIGHTS_CONTENT_MONETIZATION_BASE_BUILD_RELEASE_EVIDENCE())
    control = _rights_control_contract()
    checks = tuple(evidence.get("checks", ())) + ({"id": "rights_control_contract", "ok": control["ok"]}, {"id": "rights_control_traceability", "ok": control["capability_count"] == 50})
    evidence.update({"rights_control": control, "media_rights_content_monetization_controls": tuple(item["evidence"] for item in control["capabilities"]), "checks": checks, "blocking_gaps": tuple(check for check in checks if check.get("ok") is not True)})
    evidence["ok"] = not evidence["blocking_gaps"]
    return evidence


def release_readiness_manifest():
    manifest = dict(_MEDIA_RIGHTS_CONTENT_MONETIZATION_BASE_RELEASE_READINESS_MANIFEST())
    evidence = build_release_evidence()
    manifest.update({"ok": evidence["ok"], "evidence": evidence, "sections": tuple(dict.fromkeys(tuple(manifest.get("sections", ())) + ("rights_control", "improve1_traceability"))), "blocking_gaps": evidence["blocking_gaps"]})
    return manifest


def validate_release_evidence():
    base = dict(_MEDIA_RIGHTS_CONTENT_MONETIZATION_BASE_VALIDATE_RELEASE_EVIDENCE())
    evidence = build_release_evidence(); control = evidence["rights_control"]
    failed = tuple(check for check in evidence["checks"] if check.get("ok") is not True)
    base.update({"ok": base.get("ok") is True and evidence["ok"] and control["ok"] and not failed, "failed_checks": tuple(base.get("failed_checks", ())) + failed, "rights_control": control})
    return base
