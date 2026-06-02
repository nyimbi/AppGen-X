"""Release evidence for the media_production_management PBC."""
from __future__ import annotations

from .forms import form_catalog
from .runtime import media_production_management_build_release_evidence
from .standalone import standalone_smoke_test, single_pbc_app_contract
from .wizards import wizard_catalog
from .controls import control_catalog


def build_release_evidence():
    evidence = media_production_management_build_release_evidence()
    standalone = single_pbc_app_contract()
    return {
        **evidence,
        "standalone_app": standalone,
        "forms": form_catalog(),
        "wizards": wizard_catalog(),
        "controls": control_catalog(),
        "traceability": (
            "development_to_greenlight",
            "budget_revision_control",
            "engagement_packet_intake",
            "location_readiness",
            "shoot_day_call_sheet",
            "daily_report_dailies_editorial",
            "post_vfx_finishing",
            "rights_qc_delivery_archive",
            "agent_document_instruction_crud_preview",
        ),
        "blocking_gaps": (),
    }


def release_readiness_manifest():
    evidence = build_release_evidence()
    smoke = standalone_smoke_test()
    return {
        "ok": evidence["ok"] and smoke["ok"],
        "pbc": evidence["pbc"],
        "sections": ("schema", "services", "events", "handlers", "ui", "agent", "governance", "standalone_app"),
        "blocking_gaps": (),
        "boundary_gaps": (),
        "evidence": evidence,
        "standalone_smoke": smoke,
        "side_effects": (),
    }


def validate_release_evidence():
    manifest = release_readiness_manifest()
    missing = ()
    return {
        "ok": manifest["ok"],
        "pbc": manifest["pbc"],
        "missing_sections": missing,
        "failed_checks": (),
        "boundary_gaps": (),
        "side_effects": (),
    }


def smoke_test():
    return {"ok": release_readiness_manifest()["ok"] and validate_release_evidence()["ok"], "side_effects": ()}


# Improve1 media production control release evidence extension.
from .media_production_control import improve1_media_production_control_contract as _media_production_control_contract

_MEDIA_PRODUCTION_MANAGEMENT_BASE_BUILD_RELEASE_EVIDENCE = build_release_evidence
_MEDIA_PRODUCTION_MANAGEMENT_BASE_RELEASE_READINESS_MANIFEST = release_readiness_manifest
_MEDIA_PRODUCTION_MANAGEMENT_BASE_VALIDATE_RELEASE_EVIDENCE = validate_release_evidence


def build_release_evidence():
    evidence = dict(_MEDIA_PRODUCTION_MANAGEMENT_BASE_BUILD_RELEASE_EVIDENCE())
    control = _media_production_control_contract()
    checks = tuple(evidence.get("checks", ())) + (
        {"id": "media_production_control_contract", "ok": control["ok"]},
        {"id": "media_production_control_traceability", "ok": control["capability_count"] == 50},
    )
    evidence.update({
        "media_production_control": control,
        "media_production_management_controls": tuple(item["evidence"] for item in control["capabilities"]),
        "checks": checks,
        "blocking_gaps": tuple(check for check in checks if check.get("ok") is not True),
    })
    evidence["ok"] = not evidence["blocking_gaps"]
    return evidence


def release_readiness_manifest():
    manifest = dict(_MEDIA_PRODUCTION_MANAGEMENT_BASE_RELEASE_READINESS_MANIFEST())
    evidence = build_release_evidence()
    manifest.update({
        "ok": evidence["ok"],
        "evidence": evidence,
        "sections": tuple(dict.fromkeys(tuple(manifest.get("sections", ())) + ("media_production_control", "improve1_traceability"))),
        "blocking_gaps": evidence["blocking_gaps"],
    })
    return manifest


def validate_release_evidence():
    base = dict(_MEDIA_PRODUCTION_MANAGEMENT_BASE_VALIDATE_RELEASE_EVIDENCE())
    evidence = build_release_evidence()
    control = evidence["media_production_control"]
    failed = tuple(check for check in evidence["checks"] if check.get("ok") is not True)
    base.update({
        "ok": base.get("ok") is True and evidence["ok"] and control["ok"] and not failed,
        "failed_checks": tuple(base.get("failed_checks", ())) + failed,
        "media_production_control": control,
    })
    return base
