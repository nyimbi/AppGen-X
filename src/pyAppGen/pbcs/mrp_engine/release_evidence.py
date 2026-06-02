"""Generated release evidence for the mrp_engine PBC."""

from __future__ import annotations

from pathlib import Path

from .runtime import mrp_engine_build_api_contract
from .runtime import mrp_engine_build_release_evidence
from .runtime import mrp_engine_build_schema_contract
from .runtime import mrp_engine_build_service_contract
from .runtime import mrp_engine_permissions_contract

RELEASE_EVIDENCE = {
    **mrp_engine_build_release_evidence(),
    "pbc": "mrp_engine",
    "schema": mrp_engine_build_schema_contract(),
    "service": mrp_engine_build_service_contract(),
    "api": mrp_engine_build_api_contract(),
    "permissions": mrp_engine_permissions_contract(),
}


def build_release_evidence():
    """Return generated release audit evidence for this PBC."""
    return dict(RELEASE_EVIDENCE)


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
        "pbc": "mrp_engine",
        "format": evidence.get("format"),
        "sections": sections,
        "checks": checks,
        "blocking_gaps": tuple(evidence.get("blocking_gaps", ())),
        "required_sections": ("schema", "service", "api", "permissions"),
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
        and evidence.get("pbc") == manifest["pbc"]
        and not manifest["blocking_gaps"]
        and not missing_sections
        and not failed_checks
        and not boundary_gaps,
        "pbc": "mrp_engine",
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
    base = Path(__file__).resolve().parent
    required = ('README.md', 'SPECIFICATION.md', 'RELEASE_EVIDENCE.md', 'repository.py', 'standalone.py')
    docs = tuple({'path': name, 'exists': (base / name).exists()} for name in required)
    return {'ok': all(item['exists'] for item in docs), 'docs': docs, 'side_effects': ()}


_original_mrp_engine_build_release_evidence = build_release_evidence

def build_release_evidence():
    evidence = dict(_original_mrp_engine_build_release_evidence())
    from . import standalone
    from .repository import standalone_repository_smoke_test
    evidence['documentation'] = _standalone_documentation_evidence()
    evidence['standalone_app'] = standalone.mrp_engine_standalone_app_smoke()
    evidence['standalone_repository'] = standalone_repository_smoke_test()
    evidence['ok'] = evidence.get('ok') is True and evidence['documentation']['ok'] and evidence['standalone_app']['ok'] and evidence['standalone_repository']['ok']
    return evidence

# Improve1 MRP engine control release evidence extension.
from .mrp_engine_control import improve1_mrp_engine_control_contract as _mrp_engine_control_contract

_MRP_ENGINE_BASE_BUILD_RELEASE_EVIDENCE = build_release_evidence
_MRP_ENGINE_BASE_RELEASE_READINESS_MANIFEST = release_readiness_manifest
_MRP_ENGINE_BASE_VALIDATE_RELEASE_EVIDENCE = validate_release_evidence


def build_release_evidence():
    evidence = dict(_MRP_ENGINE_BASE_BUILD_RELEASE_EVIDENCE())
    control = _mrp_engine_control_contract()
    checks = tuple(evidence.get("checks", ())) + ({"id": "mrp_engine_control_contract", "ok": control["ok"]}, {"id": "mrp_engine_control_traceability", "ok": control["capability_count"] == 50})
    evidence.update({"mrp_engine_control": control, "mrp_engine_controls": tuple(item["evidence"] for item in control["capabilities"]), "checks": checks, "blocking_gaps": tuple(check for check in checks if check.get("ok") is not True)})
    evidence["ok"] = not evidence["blocking_gaps"]
    return evidence


def release_readiness_manifest():
    manifest = dict(_MRP_ENGINE_BASE_RELEASE_READINESS_MANIFEST())
    evidence = build_release_evidence()
    manifest.update({"ok": evidence["ok"], "evidence": evidence, "sections": tuple(dict.fromkeys(tuple(manifest.get("sections", ())) + ("mrp_engine_control", "improve1_traceability"))), "blocking_gaps": evidence["blocking_gaps"]})
    return manifest


def validate_release_evidence():
    base = dict(_MRP_ENGINE_BASE_VALIDATE_RELEASE_EVIDENCE())
    evidence = build_release_evidence()
    control = evidence["mrp_engine_control"]
    failed = tuple(check for check in evidence["checks"] if check.get("ok") is not True)
    base.update({"ok": base.get("ok") is True and evidence["ok"] and control["ok"] and not failed, "failed_checks": tuple(base.get("failed_checks", ())) + failed, "mrp_engine_control": control})
    return base
