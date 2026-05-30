from __future__ import annotations

from pathlib import Path

from .core import construction_contracts_commercials_build_release_evidence
from .schema_contract import build_schema_contract
from .service_contract import build_service_contract
from .standalone import construction_contracts_commercials_standalone_app_contract


PACKAGE_DOCS = ("README.md", "implementation-plan.md", "implementation-status.md", "RELEASE_EVIDENCE.md")


def build_release_evidence():
    evidence = dict(construction_contracts_commercials_build_release_evidence())
    documentation = {
        "ok": True,
        "artifacts": tuple(
            {
                "name": name,
                "exists": (Path(__file__).parent / name).exists(),
            }
            for name in PACKAGE_DOCS
        ),
    }
    documentation["missing"] = tuple(item["name"] for item in documentation["artifacts"] if not item["exists"])
    documentation["ok"] = not documentation["missing"]
    standalone = construction_contracts_commercials_standalone_app_contract()
    extra_checks = (
        {"id": "standalone_app_surface", "ok": standalone["ok"]},
        {"id": "package_documentation_present", "ok": documentation["ok"]},
    )
    evidence["schema"] = build_schema_contract()
    evidence["service"] = build_service_contract()
    evidence["standalone_app"] = standalone
    evidence["documentation"] = documentation
    evidence["checks"] = tuple(evidence.get("checks", ())) + extra_checks
    evidence["blocking_gaps"] = tuple(check["id"] for check in evidence["checks"] if not check["ok"])
    evidence["ok"] = not evidence["blocking_gaps"]
    return evidence


def release_readiness_manifest():
    evidence = build_release_evidence()
    return {
        "ok": evidence["ok"],
        "pbc": evidence["pbc"],
        "sections": (
            "schema",
            "services",
            "events",
            "handlers",
            "ui",
            "agent",
            "governance",
            "simulation",
            "standalone_app",
            "documentation",
        ),
        "blocking_gaps": evidence["blocking_gaps"],
        "boundary_gaps": (),
        "evidence": evidence,
        "side_effects": (),
    }


def validate_release_evidence():
    manifest = release_readiness_manifest()
    failed_checks = tuple(check["id"] for check in manifest["evidence"]["checks"] if not check["ok"])
    boundary_gaps = []
    schema = manifest["evidence"].get("schema", {})
    service = manifest["evidence"].get("service", {})
    standalone = manifest["evidence"].get("standalone_app", {})
    if schema.get("shared_table_access") is not False:
        boundary_gaps.append("schema_shared_table_access")
    if service.get("shared_table_access") is True:
        boundary_gaps.append("service_shared_table_access")
    if standalone.get("ok") is not True:
        boundary_gaps.append("standalone_surface_incomplete")
    return {
        "ok": manifest["ok"] and not failed_checks and not boundary_gaps,
        "pbc": manifest["pbc"],
        "missing_sections": (),
        "failed_checks": failed_checks,
        "boundary_gaps": tuple(boundary_gaps),
        "side_effects": (),
    }


def smoke_test():
    manifest = release_readiness_manifest()
    validation = validate_release_evidence()
    return {"ok": manifest["ok"] and validation["ok"], "side_effects": ()}
