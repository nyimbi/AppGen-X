"""Release evidence for the ar_credit PBC."""

from __future__ import annotations

from .agent import agent_skill_manifest
from .agent import chatbot_interface_contract
from .controls import ar_credit_control_catalog
from .controls import ar_credit_control_center
from .forms import ar_credit_form_catalog
from .repository import ArCreditRepository
from .runtime import ar_credit_build_release_evidence as runtime_release_evidence
from .runtime import ar_credit_empty_state
from .receivables_workflows import ar_credit_workflow_release_evidence
from .seed_data import load_demo_state
from .services import service_operation_manifest
from .standalone import standalone_app_manifest
from .ui import ar_credit_standalone_app_contract
from .ui import ar_credit_ui_contract
from .wizards import ar_credit_wizard_catalog


def build_release_evidence() -> dict:
    runtime_evidence = runtime_release_evidence()
    workflow = ar_credit_workflow_release_evidence()
    service_surface = service_operation_manifest()
    ui_surface = ar_credit_ui_contract()
    standalone_surface = ar_credit_standalone_app_contract()
    forms = ar_credit_form_catalog()
    wizards = ar_credit_wizard_catalog()
    controls = ar_credit_control_catalog()
    agent_surface = {
        "skills": agent_skill_manifest(),
        "chatbot": chatbot_interface_contract(),
    }
    repository = ArCreditRepository()
    repository_manifest = repository.database_manifest()
    repository.apply_migrations()
    seeded = load_demo_state()
    repository.save_state("tenant_demo", seeded["state"], snapshot_kind="latest", captured_at="2026-05-29T00:00:00Z")
    repository.record_workflow_run(
        run_id="tenant_demo-release-evidence",
        tenant="tenant_demo",
        workflow_name="release_evidence",
        status="completed",
        summary={"implemented_backlog_items": workflow["implemented_backlog_items"]},
        created_at="2026-05-29T00:00:00Z",
    )
    control_center = ar_credit_control_center(seeded["state"], tenant="tenant_demo", as_of="2026-06-30")
    repository.close()
    checks = tuple(runtime_evidence.get("checks", ())) + (
        {"id": "service_workflow_surface", "ok": "execute_receipt_application" in service_surface.get("workflow_operations", ())},
        {"id": "ui_workflow_surface", "ok": "build_collections_follow_up" in ui_surface.get("workflow_actions", ())},
        {"id": "agent_preview_surface", "ok": any(skill["name"].endswith("cash_application_preview") for skill in agent_surface["skills"].get("skills", ()))},
        {"id": "forms_present", "ok": forms["ok"] and len(forms.get("form_ids", ())) >= 4},
        {"id": "wizards_present", "ok": wizards["ok"] and len(wizards.get("wizard_ids", ())) >= 4},
        {"id": "controls_present", "ok": controls["ok"] and len(controls.get("control_ids", ())) >= 4},
        {"id": "standalone_surface", "ok": standalone_surface["ok"] and standalone_app_manifest()["ok"]},
        {"id": "repository_surface", "ok": repository_manifest["ok"] and not repository_manifest["shared_table_access"]},
        {"id": "control_center_surface", "ok": control_center["ok"]},
    )
    evidence = {
        **runtime_evidence,
        "format": "appgen.ar-credit-release-evidence.v1",
        "pbc": "ar_credit",
        "workflow_slice": workflow,
        "service_surface": service_surface,
        "ui": ui_surface,
        "standalone_app": standalone_surface,
        "agent": agent_surface,
        "forms": forms,
        "wizards": wizards,
        "controls": controls,
        "repository": repository_manifest,
        "control_center": control_center,
        "checks": checks,
        "seeded_demo": {"ok": seeded["ok"], "tenant": seeded["tenant"], "customer_id": seeded["customer"]["customer_id"], "invoice_id": seeded["invoice"]["invoice_id"]},
    }
    evidence["ok"] = all(check.get("ok") is True for check in checks)
    evidence["blocking_gaps"] = tuple(check for check in checks if check.get("ok") is not True)
    return evidence


RELEASE_EVIDENCE = build_release_evidence()


def release_readiness_manifest() -> dict:
    evidence = build_release_evidence()
    sections = tuple(
        name
        for name in ("schema", "service", "api", "permissions", "ui", "agent", "workflow_slice", "service_surface", "forms", "wizards", "controls", "repository", "standalone_app")
        if isinstance(evidence.get(name), dict)
    )
    checks = tuple(evidence.get("checks", ()))
    return {
        "ok": evidence.get("ok") is True and bool(checks),
        "pbc": "ar_credit",
        "format": evidence.get("format"),
        "sections": sections,
        "checks": checks,
        "blocking_gaps": tuple(evidence.get("blocking_gaps", ())),
        "required_sections": ("schema", "service", "repository", "standalone_app"),
        "side_effects": (),
    }


def validate_release_evidence() -> dict:
    evidence = build_release_evidence()
    manifest = release_readiness_manifest()
    missing_sections = tuple(section for section in manifest["required_sections"] if section not in manifest["sections"])
    failed_checks = tuple(check for check in manifest["checks"] if check.get("ok") is not True)
    schema = evidence.get("schema", {}) if isinstance(evidence.get("schema"), dict) else {}
    service = evidence.get("service", {}) if isinstance(evidence.get("service"), dict) else {}
    workflow = evidence.get("workflow_slice", {}) if isinstance(evidence.get("workflow_slice"), dict) else {}
    service_surface = evidence.get("service_surface", {}) if isinstance(evidence.get("service_surface"), dict) else {}
    repository = evidence.get("repository", {}) if isinstance(evidence.get("repository"), dict) else {}
    standalone = evidence.get("standalone_app", {}) if isinstance(evidence.get("standalone_app"), dict) else {}
    boundary_gaps = tuple(
        gap
        for gap, failed in (
            ("schema_shared_table_access", schema.get("shared_table_access") is not False),
            ("service_shared_table_access", service.get("shared_table_access") is True),
            ("service_missing_command_methods", not bool(service.get("command_methods"))),
            ("workflow_shared_table_access", workflow.get("shared_table_access") is not False),
            ("workflow_not_appgen_x", workflow.get("event_contract") != "AppGen-X"),
            ("service_workflow_not_exposed", not bool(service_surface.get("workflow_operations"))),
            ("repository_shared_table_access", repository.get("shared_table_access") is not False),
            ("standalone_not_ok", standalone.get("ok") is not True),
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
        "pbc": "ar_credit",
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
