"""Release evidence and focused audits for standalone master_data_governance."""
from __future__ import annotations

from pathlib import Path

from .agent import smoke_test as agent_smoke_test
from .routes import smoke_test as route_smoke_test
from .schema_contract import build_schema_contract
from .seed_data import seed_plan, smoke_test as seed_smoke_test
from .service_contract import build_service_contract
from .standalone import master_data_governance_standalone_app_contract
from .standalone import master_data_governance_standalone_app_smoke
from .standalone import standalone_route_smoke_test
from .standalone import standalone_store_smoke_test
from .ui import smoke_test as ui_smoke_test
from . import capability_assurance

PBC_KEY = "master_data_governance"
PACKAGE_DIR = Path(__file__).resolve().parent
_REQUIRED_SPEC_TOKENS = (
    "domain registry",
    "golden records",
    "survivorship",
    "match/merge",
    "stewardship workflow",
    "data quality rules",
    "hierarchy management",
    "reference data",
    "lineage",
    "policy approvals",
    "remediation queue",
    "audit proof",
    "standalone",
)



def specification_audit() -> dict:
    text = (PACKAGE_DIR / "SPECIFICATION.md").read_text(encoding="utf-8").lower()
    missing = tuple(token for token in _REQUIRED_SPEC_TOKENS if token not in text)
    return {
        "ok": not missing,
        "pbc": PBC_KEY,
        "document": "SPECIFICATION.md",
        "missing_tokens": missing,
        "side_effects": (),
    }



def documentation_presence() -> dict:
    artifacts = (
        {"name": "SPECIFICATION.md", "exists": (PACKAGE_DIR / "SPECIFICATION.md").exists()},
        {"name": "RELEASE_EVIDENCE.md", "exists": (PACKAGE_DIR / "RELEASE_EVIDENCE.md").exists()},
        {"name": "standalone.py", "exists": (PACKAGE_DIR / "standalone.py").exists()},
        {"name": "tests/test_contract.py", "exists": (PACKAGE_DIR / "tests" / "test_contract.py").exists()},
        {"name": "tests/test_standalone_app.py", "exists": (PACKAGE_DIR / "tests" / "test_standalone_app.py").exists()},
    )
    missing = tuple(item["name"] for item in artifacts if not item["exists"])
    return {"ok": not missing, "artifacts": artifacts, "missing": missing, "side_effects": ()}



def source_package_audit() -> dict:
    schema = build_schema_contract()
    service = build_service_contract()
    standalone = master_data_governance_standalone_app_contract()
    seed = seed_plan()
    return {
        "ok": schema["ok"] and service["ok"] and standalone["ok"] and seed["ok"],
        "pbc": PBC_KEY,
        "schema": schema,
        "service": service,
        "standalone": standalone,
        "seed": seed,
        "side_effects": (),
    }



def generation_smoke_audit() -> dict:
    standalone = master_data_governance_standalone_app_smoke()
    store = standalone_store_smoke_test()
    routes = standalone_route_smoke_test()
    ui = ui_smoke_test()
    agent = agent_smoke_test()
    seed = seed_smoke_test()
    capability = capability_assurance.smoke_test()
    return {
        "ok": standalone["ok"] and store["ok"] and routes["ok"] and ui["ok"] and agent["ok"] and seed["ok"] and capability["ok"],
        "standalone": standalone,
        "store": store,
        "routes": routes,
        "ui": ui,
        "agent": agent,
        "seed": seed,
        "capability": capability,
        "side_effects": (),
    }



def build_release_evidence():
    schema = build_schema_contract()
    service = build_service_contract()
    spec = specification_audit()
    docs = documentation_presence()
    source = source_package_audit()
    generation = generation_smoke_audit()
    route = route_smoke_test()
    checks = (
        {"id": "specification_traceability", "ok": spec["ok"]},
        {"id": "documentation_presence", "ok": docs["ok"]},
        {"id": "standalone_app_surface", "ok": source["standalone"]["ok"]},
        {"id": "schema_contract", "ok": schema["ok"]},
        {"id": "service_contract", "ok": service["ok"]},
        {"id": "seed_bundle", "ok": source["seed"]["ok"]},
        {"id": "route_smoke", "ok": route["ok"]},
        {"id": "generation_smoke", "ok": generation["ok"]},
    )
    blocking = tuple(check for check in checks if not check["ok"])
    return {
        "format": "appgen.master-data-governance-release-evidence.v1",
        "ok": not blocking,
        "pbc": PBC_KEY,
        "checks": checks,
        "blocking_gaps": blocking,
        "boundary_gaps": (),
        "schema": schema,
        "service": service,
        "specification": spec,
        "documentation": docs,
        "source_audit": source,
        "generation_smoke": generation,
        "route_smoke": route,
        "standalone_app": source["standalone"],
        "side_effects": (),
    }



def release_readiness_manifest():
    evidence = build_release_evidence()
    return {
        "ok": evidence["ok"],
        "pbc": PBC_KEY,
        "sections": (
            "schema",
            "service",
            "standalone_app",
            "specification",
            "documentation",
            "source_audit",
            "generation_smoke",
        ),
        "checks": evidence["checks"],
        "blocking_gaps": evidence["blocking_gaps"],
        "boundary_gaps": evidence["boundary_gaps"],
        "side_effects": (),
    }



def validate_release_evidence():
    evidence = build_release_evidence()
    failed = tuple(check for check in evidence["checks"] if not check["ok"])
    return {
        "ok": evidence["ok"] and not failed and not evidence["boundary_gaps"],
        "missing_sections": (),
        "failed_checks": failed,
        "boundary_gaps": evidence["boundary_gaps"],
        "blocking_gaps": failed,
        "side_effects": (),
    }



def smoke_test():
    validation = validate_release_evidence()
    return {"ok": validation["ok"], "validation": validation, "side_effects": (),}



def master_data_governance_build_release_evidence():
    return build_release_evidence()
