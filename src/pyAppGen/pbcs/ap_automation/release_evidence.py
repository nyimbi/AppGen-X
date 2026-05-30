"""Generated release evidence for the ap_automation PBC."""

import importlib.util
from pathlib import Path


RELEASE_EVIDENCE = {
    "format": "appgen.ap-automation-release-evidence.v1",
    "ok": True,
    "checks": (
        {"id": "owned_schema_depth", "ok": True},
        {"id": "migration_per_owned_table", "ok": True},
        {"id": "service_command_depth", "ok": True},
        {"id": "api_event_contract", "ok": True},
        {"id": "permissions_cover_commands", "ok": True},
        {"id": "backend_allowlist", "ok": True},
        {"id": "no_shared_table_access", "ok": True},
    ),
    "pbc": "ap_automation",
}



def _load_sibling_module(module_name):
    """Load a sibling generated module when this file is imported directly."""
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



def build_release_evidence():
    """Return generated release audit evidence for this PBC."""
    evidence = dict(RELEASE_EVIDENCE)
    evidence.setdefault("schema", _build_schema_contract())
    evidence.setdefault("service", _build_service_contract())
    evidence.setdefault("pbc", "ap_automation")
    try:
        from . import agent, services, ui
        from .controls import smoke_test as controls_smoke_test
        from .forms import smoke_test as forms_smoke_test
        from .repository import smoke_test as repository_smoke_test
        from .wizards import smoke_test as wizards_smoke_test
    except ImportError:
        agent = _load_sibling_module("agent")
        services = _load_sibling_module("services")
        ui = _load_sibling_module("ui")
        repository_smoke_test = _load_sibling_module("repository").smoke_test
        forms_smoke_test = _load_sibling_module("forms").smoke_test
        wizards_smoke_test = _load_sibling_module("wizards").smoke_test
        controls_smoke_test = _load_sibling_module("controls").smoke_test
    evidence["execution_service"] = services.execution_service_manifest()
    evidence["ui"] = ui.smoke_test()
    evidence["agent"] = agent.smoke_test()
    evidence["repository"] = repository_smoke_test()
    evidence["forms"] = forms_smoke_test()
    evidence["wizards"] = wizards_smoke_test()
    evidence["controls"] = controls_smoke_test()
    live_checks = tuple(evidence.get("checks", ())) + (
        {"id": "execution_service_bound", "ok": evidence["execution_service"]["ok"]},
        {"id": "ui_contract_bound", "ok": evidence["ui"]["ok"]},
        {"id": "agent_contribution_bound", "ok": evidence["agent"]["ok"]},
        {"id": "repository_bound", "ok": evidence["repository"]["ok"]},
        {"id": "forms_bound", "ok": evidence["forms"]["ok"]},
        {"id": "wizards_bound", "ok": evidence["wizards"]["ok"]},
        {"id": "controls_bound", "ok": evidence["controls"]["ok"]},
    )
    evidence["checks"] = live_checks
    evidence["ok"] = evidence.get("ok") is True and all(check.get("ok") is True for check in live_checks)
    return evidence



def release_readiness_manifest():
    """Return side-effect-free release evidence coverage and gate metadata."""
    evidence = build_release_evidence()
    sections = tuple(
        name
        for name in (
            "schema",
            "service",
            "api",
            "permissions",
            "ui",
            "events",
            "agent",
            "execution_service",
            "repository",
            "forms",
            "wizards",
            "controls",
        )
        if isinstance(evidence.get(name), dict)
    )
    checks = tuple(evidence.get("checks", ()))
    return {
        "ok": evidence.get("ok") is True and bool(checks),
        "pbc": "ap_automation",
        "format": evidence.get("format"),
        "sections": sections,
        "checks": checks,
        "blocking_gaps": tuple(evidence.get("blocking_gaps", ())),
        "required_sections": ("schema", "service", "repository", "forms", "wizards", "controls"),
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
    repository = evidence.get("repository", {}) if isinstance(evidence.get("repository"), dict) else {}
    boundary_gaps = tuple(
        gap
        for gap, failed in (
            ("schema_shared_table_access", schema.get("shared_table_access") is not False),
            ("service_shared_table_access", service.get("shared_table_access") is True),
            ("service_missing_command_methods", not bool(service.get("command_methods"))),
            ("repository_shared_table_access", repository.get("contract", {}).get("shared_table_access") is not False),
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
        "pbc": "ap_automation",
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
