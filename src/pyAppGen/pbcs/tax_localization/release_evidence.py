"""Generated release evidence for the tax_localization PBC."""

from __future__ import annotations

from pathlib import Path

from . import agent
from . import app_surface
from . import controls
from . import forms
from . import repository
from . import runtime
from . import ui
from . import wizards


PACKAGE_DIR = Path(__file__).resolve().parent
_REQUIRED_DOCS = (
    "README.md",
    "SPECIFICATION.md",
    "RELEASE_EVIDENCE.md",
    "implementation-plan.md",
    "implementation-status.md",
)


RELEASE_EVIDENCE = {
    **runtime.tax_localization_build_release_evidence(),
    "pbc": "tax_localization",
}


def build_release_evidence() -> dict:
    base = dict(runtime.tax_localization_build_release_evidence())
    docs_present = {name: (PACKAGE_DIR / name).exists() for name in _REQUIRED_DOCS}
    forms_smoke = forms.smoke_test()
    wizards_smoke = wizards.smoke_test()
    controls_smoke = controls.smoke_test()
    ui_smoke = ui.smoke_test()
    agent_smoke = agent.smoke_test()
    repository_smoke = repository.smoke_test()
    app = app_surface.single_pbc_tax_localization_contract()
    boundary = runtime.tax_localization_verify_owned_table_boundary(("tax_jurisdiction", "GET /products/taxability"))
    checks = tuple(base.get("checks", ())) + (
        {"id": "forms_surface", "ok": forms_smoke["ok"]},
        {"id": "wizards_surface", "ok": wizards_smoke["ok"]},
        {"id": "controls_surface", "ok": controls_smoke["ok"]},
        {"id": "ui_surface", "ok": ui_smoke["ok"]},
        {"id": "assistant_surface", "ok": agent_smoke["ok"]},
        {"id": "repository_backed", "ok": repository_smoke["ok"]},
        {"id": "single_pbc_app", "ok": app["ok"] and app["single_pbc_app"]},
        {"id": "documentation_present", "ok": all(docs_present.values())},
        {"id": "boundary_evidence", "ok": boundary["ok"]},
    )
    return {
        **base,
        "pbc": "tax_localization",
        "ok": all(check["ok"] for check in checks),
        "checks": checks,
        "forms": forms_smoke,
        "wizards": wizards_smoke,
        "controls": controls_smoke,
        "ui": ui_smoke,
        "assistant": agent_smoke,
        "repository": repository_smoke,
        "single_pbc_app": app,
        "documentation": {"required": _REQUIRED_DOCS, "docs_present": docs_present},
        "boundary": boundary,
        "blocking_gaps": tuple(check for check in checks if not check["ok"]),
    }


def release_readiness_manifest() -> dict:
    evidence = build_release_evidence()
    sections = tuple(
        name
        for name in (
            "schema",
            "service",
            "api",
            "permissions",
            "ui",
            "assistant",
            "repository",
            "single_pbc_app",
            "documentation",
            "forms",
            "wizards",
            "controls",
        )
        if isinstance(evidence.get(name), dict)
    )
    checks = tuple(evidence.get("checks", ()))
    return {
        "ok": evidence.get("ok") is True and bool(checks),
        "pbc": "tax_localization",
        "format": evidence.get("format"),
        "sections": sections,
        "checks": checks,
        "blocking_gaps": tuple(evidence.get("blocking_gaps", ())),
        "required_sections": ("schema", "service", "assistant", "single_pbc_app", "documentation"),
        "side_effects": (),
    }


def validate_release_evidence() -> dict:
    evidence = build_release_evidence()
    manifest = release_readiness_manifest()
    missing_sections = tuple(section for section in manifest["required_sections"] if section not in manifest["sections"])
    failed_checks = tuple(check for check in manifest["checks"] if check.get("ok") is not True)
    documentation = evidence.get("documentation", {})
    boundary = evidence.get("boundary", {})
    boundary_gaps = tuple(
        gap
        for gap, failed in (
            ("missing_docs", not all(documentation.get("docs_present", {}).values())),
            ("boundary_violation", boundary.get("ok") is not True),
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
        "pbc": "tax_localization",
        "manifest": manifest,
        "missing_sections": missing_sections,
        "failed_checks": failed_checks,
        "boundary_gaps": boundary_gaps,
        "side_effects": (),
    }


def smoke_test() -> dict:
    validation = validate_release_evidence()
    evidence = build_release_evidence()
    return {
        "ok": validation["ok"] and evidence.get("ok") is True,
        "validation": validation,
        "evidence": evidence,
        "side_effects": (),
    }
