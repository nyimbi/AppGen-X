"""Release evidence for the enterprise_pim standalone package."""

from __future__ import annotations

from pathlib import Path

from . import agent
from . import events
from . import handlers
from . import permissions
from . import routes
from . import seed_data
from . import services
from . import standalone
from . import ui
from .schema_contract import build_schema_contract
from .schema_contract import validate_schema_contract
from .service_contract import build_service_contract
from .pim_control import improve1_pim_control_contract


PACKAGE_DIR = Path(__file__).resolve().parent


def _relative_paths(pattern: str) -> tuple[str, ...]:
    return tuple(sorted(str(path.relative_to(PACKAGE_DIR)) for path in PACKAGE_DIR.glob(pattern) if path.is_file()))


def build_release_evidence():
    """Return package-local release evidence based on actual artifacts."""
    schema = build_schema_contract()
    schema_validation = validate_schema_contract()
    service = build_service_contract()
    api = routes.api_route_contracts()
    route_validation = routes.validate_api_route_contracts()
    permission_manifest = permissions.permission_manifest()
    ui_smoke = ui.smoke_test()
    event_smoke = events.smoke_test()
    handler_smoke = handlers.smoke_test()
    seed_validation = seed_data.validate_seed_data()
    agent_smoke = agent.smoke_test()
    standalone_smoke = standalone.smoke_test()
    pim_control = improve1_pim_control_contract()
    migration_files = _relative_paths("migrations/*.sql")
    test_files = _relative_paths("tests/*.py")
    docs = tuple(
        path
        for path in (
            "SPECIFICATION.md",
            "RELEASE_EVIDENCE.md",
            "implementation-plan.md",
            "implementation-status.md",
            "README.md",
        )
        if (PACKAGE_DIR / path).exists()
    )
    checks = (
        {"id": "schema_contract", "ok": schema_validation["ok"]},
        {"id": "service_contract", "ok": service.get("ok") is True},
        {"id": "route_contract", "ok": api["ok"] and route_validation["ok"]},
        {"id": "permission_contract", "ok": permission_manifest["ok"]},
        {"id": "ui_workbench", "ok": ui_smoke["ok"]},
        {"id": "event_contract", "ok": event_smoke["ok"]},
        {"id": "event_handlers", "ok": handler_smoke["ok"]},
        {"id": "seed_bundle", "ok": seed_validation["ok"]},
        {"id": "agent_planning", "ok": agent_smoke["ok"]},
        {"id": "standalone_app", "ok": standalone_smoke["ok"]},
        {"id": "migration_artifacts", "ok": bool(migration_files)},
        {"id": "documentation_set", "ok": len(docs) >= 4},
        {"id": "focused_tests", "ok": bool(test_files)},
        {"id": "pim_improve1_control_contract", "ok": pim_control["ok"]},
    )
    blocking_gaps = tuple(check["id"] for check in checks if not check["ok"])
    return {
        "format": "appgen.enterprise-pim-release-evidence.v2",
        "ok": not blocking_gaps,
        "pbc": "enterprise_pim",
        "checks": checks,
        "blocking_gaps": blocking_gaps,
        "schema": schema,
        "service": service,
        "api": api,
        "permissions": permission_manifest,
        "ui": ui_smoke,
        "events": event_smoke,
        "handlers": handler_smoke,
        "seed": seed_validation,
        "agent": agent_smoke,
        "standalone": standalone_smoke,
        "pim_control": pim_control,
        "artifacts": {
            "migrations": migration_files,
            "tests": test_files,
            "docs": docs,
            "runtime_modules": (
                "runtime.py",
                "services.py",
                "routes.py",
                "events.py",
                "handlers.py",
                "permissions.py",
                "seed_data.py",
                "standalone.py",
                "pim_control.py",
            ),
        },
    }


def release_readiness_manifest():
    """Return side-effect-free release evidence coverage and gate metadata."""
    evidence = build_release_evidence()
    sections = tuple(
        name
        for name in ("schema", "service", "api", "permissions", "ui", "events", "handlers", "seed", "agent", "standalone", "pim_control")
        if isinstance(evidence.get(name), dict)
    )
    checks = tuple(evidence.get("checks", ()))
    return {
        "ok": evidence.get("ok") is True and bool(checks),
        "pbc": "enterprise_pim",
        "format": evidence.get("format"),
        "sections": sections,
        "checks": checks,
        "blocking_gaps": tuple(evidence.get("blocking_gaps", ())),
        "required_sections": ("schema", "service", "standalone", "pim_control"),
        "side_effects": (),
    }


def validate_release_evidence():
    """Validate release evidence, blocking gaps, and owned-boundary proof."""
    evidence = build_release_evidence()
    manifest = release_readiness_manifest()
    missing_sections = tuple(section for section in manifest["required_sections"] if section not in manifest["sections"])
    failed_checks = tuple(check["id"] for check in manifest["checks"] if check.get("ok") is not True)
    schema = evidence.get("schema", {})
    service = evidence.get("service", {})
    api = evidence.get("api", {})
    boundary_gaps = tuple(
        gap
        for gap, failed in (
            ("schema_shared_table_access", schema.get("shared_table_access") is not False),
            ("service_shared_table_access", service.get("shared_table_access") is True),
            ("api_shared_table_access", api.get("ok") is not True),
        )
        if failed
    )
    return {
        "ok": manifest["ok"]
        and not missing_sections
        and not failed_checks
        and not boundary_gaps,
        "pbc": "enterprise_pim",
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


RELEASE_EVIDENCE = build_release_evidence()
