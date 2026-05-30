"""Focused standalone one-PBC tests for medical_device_lifecycle."""

from pathlib import Path

from .. import agent, controls, release_evidence, standalone, ui


def test_forms_wizards_and_controls_are_executable():
    from .. import forms, wizards

    form_catalog = forms.medical_device_lifecycle_form_catalog()
    wizard_catalog = wizards.medical_device_lifecycle_wizard_catalog()
    control_catalog = controls.medical_device_lifecycle_control_catalog()

    assert form_catalog["ok"] is True
    assert wizard_catalog["ok"] is True
    assert control_catalog["ok"] is True
    assert "medical_device_registry_intake" in form_catalog["form_ids"]
    assert "recall_containment_and_notification" in wizard_catalog["wizard_ids"]
    assert "assignment_safety_gate" in control_catalog["control_ids"]


def test_standalone_assignment_blocks_recalled_or_overdue_devices():
    app = standalone.MedicalDeviceLifecycleStandaloneApp()
    try:
        created = app.register_device(
            {
                "tenant": "tenant-test",
                "device_id": "MD-BLOCKED",
                "udi": "UDI-BLOCKED",
                "manufacturer": "Acme",
                "model": "Pump-X",
                "serial_number": "SN-BLOCKED",
                "risk_class": "II",
                "implantable": False,
                "department": "ICU",
                "location": "ICU-STORE",
                "qualification_status": "qualified",
                "calibration_due_at": "2026-01-01",
            }
        )
        blocked = app.assign_device(
            {
                "tenant": "tenant-test",
                "assignment_id": "ASN-BLOCKED",
                "device_id": "MD-BLOCKED",
                "assignment_type": "room",
                "assignee_ref": "ICU-RM2",
                "responsible_role": "nurse_manager",
                "privacy_scope": "operational",
                "today": "2026-02-01",
            }
        )
        recall = app.launch_recall(
            {
                "tenant": "tenant-test",
                "recall_id": "REC-BLOCKED",
                "manufacturer_notice": "FSN-BLOCKED",
                "recall_class": "I",
                "device_ids": ["MD-BLOCKED"],
                "required_action": "remove from service",
            }
        )
        blocked_after_recall = app.assign_device(
            {
                "tenant": "tenant-test",
                "assignment_id": "ASN-BLOCKED-2",
                "device_id": "MD-BLOCKED",
                "assignment_type": "room",
                "assignee_ref": "ICU-RM3",
                "responsible_role": "nurse_manager",
                "privacy_scope": "operational",
                "today": "2025-12-31",
            }
        )

        assert created["ok"] is True
        assert blocked["ok"] is False
        assert "calibration_overdue" in blocked["blocked_by"]
        assert recall["ok"] is True
        assert blocked_after_recall["ok"] is False
        assert "active_recall" in blocked_after_recall["blocked_by"]
    finally:
        app.close()


def test_standalone_routes_ui_agent_and_release_surface():
    smoke = standalone.medical_device_lifecycle_standalone_app_smoke()
    rendered = ui.medical_device_lifecycle_render_workbench(smoke["workbench"])
    workspace = agent.standalone_agent_workspace_contract()
    document_plan = agent.document_instruction_plan(
        "Field safety notice for infusion device",
        "quarantine the recalled device and attach recall evidence",
    )
    crud_plan = agent.datastore_crud_plan(
        "update",
        "medical_device_lifecycle_recall_notice",
        {"status": "open"},
    )
    evidence = release_evidence.build_release_evidence()
    manifest = release_evidence.release_readiness_manifest()
    validation = release_evidence.validate_release_evidence()

    assert smoke["ok"] is True
    assert rendered["ok"] is True
    assert workspace["ok"] is True
    assert document_plan["ok"] is True
    assert "recall_containment_and_notification" in document_plan["wizard_candidates"]
    assert crud_plan["ok"] is True
    assert crud_plan["route_candidates"]
    assert evidence["standalone_app"]["ok"] is True
    assert evidence["forms"]["ok"] is True
    assert evidence["controls"]["ok"] is True
    assert manifest["ok"] is True
    assert validation["ok"] is True


def test_control_center_and_package_local_docs_exist():
    smoke = standalone.medical_device_lifecycle_standalone_app_smoke()
    center = controls.medical_device_lifecycle_control_center(smoke["workbench"])
    base = Path(__file__).resolve().parent.parent

    assert center["ok"] is True
    assert center["assistant_guardrails"]["boundary_ok"] is True
    for name in ("SPECIFICATION.md", "RELEASE_EVIDENCE.md", "implementation-plan.md", "forms.py", "wizards.py", "controls.py", "standalone.py"):
        assert (base / name).exists() is True
