"""Release evidence for the asset_lifecycle PBC."""

from __future__ import annotations

from . import events
from . import runtime
from . import services
from . import ui


RELEASE_EVIDENCE = {
    "format": "appgen.asset-lifecycle-release-evidence.v1",
    "ok": True,
    "pbc": "asset_lifecycle",
}


def build_release_evidence():
    """Return executable release audit evidence for this PBC."""
    runtime_evidence = runtime.asset_lifecycle_build_release_evidence()
    event_manifest = events.event_contract_manifest()
    service_manifest = services.service_operation_manifest()
    ui_contract = ui.asset_lifecycle_ui_contract()
    checks = tuple(runtime_evidence.get("checks", ())) + (
        {
            "id": "appgen_event_alignment",
            "ok": event_manifest["topic"] == runtime.ASSET_LIFECYCLE_REQUIRED_EVENT_TOPIC
            and event_manifest["dead_letter_table"] == "asset_lifecycle_dead_letter_event",
        },
        {
            "id": "depreciation_preview_surface",
            "ok": "preview_depreciation_plan" in service_manifest.get("scenario_methods", ()),
        },
        {
            "id": "depreciation_revision_ui_surface",
            "ok": "DepreciationRevisionConsole" in ui_contract.get("fragments", ()),
        },
    )
    return {
        **runtime_evidence,
        "checks": checks,
        "ok": runtime_evidence.get("ok") is True and all(check["ok"] for check in checks),
        "pbc": "asset_lifecycle",
        "events": event_manifest,
        "ui": ui_contract,
        "service_manifest": service_manifest,
        "blocking_gaps": tuple(check for check in checks if not check["ok"]),
    }


def release_readiness_manifest():
    """Return side-effect-free release evidence coverage and gate metadata."""
    evidence = build_release_evidence()
    sections = tuple(
        name
        for name in ("schema", "service", "api", "permissions", "ui", "events")
        if isinstance(evidence.get(name), dict)
    )
    checks = tuple(evidence.get("checks", ()))
    return {
        "ok": evidence.get("ok") is True and bool(checks),
        "pbc": "asset_lifecycle",
        "format": evidence.get("format"),
        "sections": sections,
        "checks": checks,
        "blocking_gaps": tuple(evidence.get("blocking_gaps", ())),
        "required_sections": ("schema", "service", "api", "permissions", "ui", "events"),
        "side_effects": (),
    }


def validate_release_evidence():
    """Validate release evidence, blocking gaps, and owned-boundary proof."""
    evidence = build_release_evidence()
    manifest = release_readiness_manifest()
    missing_sections = tuple(section for section in manifest["required_sections"] if section not in manifest["sections"])
    failed_checks = tuple(check for check in manifest["checks"] if check.get("ok") is not True)
    schema = evidence.get("schema", {}) if isinstance(evidence.get("schema"), dict) else {}
    service = evidence.get("service", {}) if isinstance(evidence.get("service"), dict) else {}
    api = evidence.get("api", {}) if isinstance(evidence.get("api"), dict) else {}
    boundary_gaps = tuple(
        gap
        for gap, failed in (
            ("schema_shared_table_access", schema.get("shared_table_access") is not False),
            ("service_shared_table_access", service.get("external_dependencies", {}).get("shared_tables") not in ((), None)),
            ("api_shared_table_access", api.get("shared_table_access") is not False),
            ("service_missing_query_review", "review_depreciation_plan" not in service.get("query_methods", ())),
        )
        if failed
    )
    return {
        "ok": manifest["ok"]
        and evidence.get("pbc") == manifest["pbc"]
        and not manifest["blocking_gaps"]
        and not missing_sections
        and not failed_checks
        and not boundary_gaps,
        "pbc": "asset_lifecycle",
        "manifest": manifest,
        "missing_sections": missing_sections,
        "failed_checks": failed_checks,
        "boundary_gaps": boundary_gaps,
        "side_effects": (),
    }


def smoke_test():
    """Exercise release evidence readiness validation side-effect-free."""
    validation = validate_release_evidence()
    evidence = build_release_evidence()
    return {
        "ok": validation["ok"] and evidence.get("ok") is True,
        "validation": validation,
        "evidence": evidence,
        "side_effects": (),
    }



def _standalone_documentation_evidence():
    from pathlib import Path
    base=Path(__file__).resolve().parent; required=('README.md','SPECIFICATION.md','RELEASE_EVIDENCE.md','repository.py','standalone.py'); docs=tuple({'path':n,'exists':(base/n).exists()} for n in required)
    return {'ok':all(i['exists'] for i in docs),'docs':docs,'side_effects':()}
_original_asset_lifecycle_build_release_evidence=build_release_evidence
def build_release_evidence():
    evidence=dict(_original_asset_lifecycle_build_release_evidence())
    from . import standalone
    from .repository import standalone_repository_smoke_test
    evidence['documentation']=_standalone_documentation_evidence(); evidence['standalone_app']=standalone.asset_lifecycle_standalone_app_smoke(); evidence['standalone_repository']=standalone_repository_smoke_test(); evidence['ok']=evidence.get('ok') is True and evidence['documentation']['ok'] and evidence['standalone_app']['ok'] and evidence['standalone_repository']['ok']; return evidence
