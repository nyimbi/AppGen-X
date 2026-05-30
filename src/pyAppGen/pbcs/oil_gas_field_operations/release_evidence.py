"""Release evidence for the oil_gas_field_operations PBC."""

from __future__ import annotations

from pathlib import Path

from .agent import oil_gas_field_operations_assistant_preview
from .controls import oil_gas_field_operations_control_center
from .forms import oil_gas_field_operations_form_catalog
from .runtime import oil_gas_field_operations_build_release_evidence as runtime_release_evidence
from .standalone import documentation_presence
from .standalone import oil_gas_field_operations_standalone_app_contract
from .standalone import oil_gas_field_operations_standalone_app_smoke
from .wizards import oil_gas_field_operations_wizard_catalog


def build_release_evidence():
    base = runtime_release_evidence()
    forms = oil_gas_field_operations_form_catalog()
    wizards = oil_gas_field_operations_wizard_catalog()
    controls = oil_gas_field_operations_control_center()
    assistant = oil_gas_field_operations_assistant_preview(
        {
            "document_text": "Prepare a read-only ROUTE-7 morning review.",
            "instructions": "Preview the production review flow.",
            "target_entity": "production_reading",
            "requested_action": "read",
            "payload": {"well_id": "OG-7H", "production_date": "2026-05-29"},
        }
    )
    standalone_contract = oil_gas_field_operations_standalone_app_contract()
    standalone_smoke = oil_gas_field_operations_standalone_app_smoke()
    docs_present = documentation_presence()["docs"]
    checks = tuple(base["checks"]) + (
        {"id": "forms", "ok": forms["ok"]},
        {"id": "wizards", "ok": wizards["ok"]},
        {"id": "controls", "ok": controls["ok"]},
        {"id": "assistant_preview", "ok": assistant["ok"]},
        {"id": "standalone_app_contract", "ok": standalone_contract["ok"]},
        {"id": "standalone_app_smoke", "ok": standalone_smoke["ok"]},
        {"id": "docs_present", "ok": all(docs_present.values())},
    )
    return {
        **base,
        "ok": base["ok"] and forms["ok"] and wizards["ok"] and controls["ok"] and assistant["ok"] and standalone_contract["ok"] and standalone_smoke["ok"] and all(docs_present.values()),
        "checks": checks,
        "forms": forms,
        "wizards": wizards,
        "controls": controls,
        "assistant": assistant,
        "standalone_app": standalone_contract,
        "standalone_smoke": standalone_smoke,
        "docs_present": docs_present,
    }


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
            "forms",
            "wizards",
            "controls",
            "standalone_app",
            "agent",
            "governance",
            "docs",
        ),
        "blocking_gaps": (),
        "boundary_gaps": () if evidence["controls"]["assistant_guardrails"]["boundary_ok"] else ("assistant_boundary",),
        "evidence": evidence,
        "side_effects": (),
    }


def validate_release_evidence():
    manifest = release_readiness_manifest()
    evidence = manifest["evidence"]
    missing_sections = tuple(section for section in manifest["sections"] if section == "docs" and not all(evidence["docs_present"].values()))
    failed_checks = tuple(check["id"] for check in evidence["checks"] if not check["ok"])
    return {
        "ok": manifest["ok"] and not missing_sections and not failed_checks,
        "pbc": manifest["pbc"],
        "missing_sections": missing_sections,
        "failed_checks": failed_checks,
        "boundary_gaps": manifest["boundary_gaps"],
        "side_effects": (),
    }


def smoke_test():
    return {
        "ok": release_readiness_manifest()["ok"] and validate_release_evidence()["ok"],
        "side_effects": (),
    }
