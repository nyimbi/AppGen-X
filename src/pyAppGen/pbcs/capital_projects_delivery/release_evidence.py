from __future__ import annotations

from .runtime import capital_projects_delivery_build_release_evidence


def build_release_evidence():
    return capital_projects_delivery_build_release_evidence()


def release_readiness_manifest():
    evidence = build_release_evidence()
    sections = ("schema", "services", "events", "handlers", "ui", "agent", "workflows", "standalone", "governance")
    return {
        "ok": evidence["ok"],
        "pbc": evidence["pbc"],
        "sections": sections,
        "blocking_gaps": tuple(evidence.get("blocking_gaps", ())),
        "boundary_gaps": (),
        "evidence": evidence,
        "side_effects": (),
    }


def validate_release_evidence():
    manifest = release_readiness_manifest()
    checks = tuple(manifest["evidence"].get("checks", ()))
    required = {
        "schema_models_migrations",
        "service_api_events",
        "agent_ui_governance",
        "retry_dead_letter",
        "lifecycle_gate_controls",
        "standalone_bootstrap_and_shell",
        "pbc_source_artifact_contract",
        "pbc_implementation_release_audit",
        "pbc_generation_smoke_audit",
    }
    present = {check["id"] for check in checks}
    return {
        "ok": manifest["ok"] and required <= present and not manifest["blocking_gaps"],
        "pbc": manifest["pbc"],
        "missing_sections": (),
        "failed_checks": tuple(check for check in checks if not check["ok"]),
        "boundary_gaps": manifest["boundary_gaps"],
        "side_effects": (),
    }


def smoke_test():
    return {
        "ok": release_readiness_manifest()["ok"] and validate_release_evidence()["ok"],
        "side_effects": (),
    }
