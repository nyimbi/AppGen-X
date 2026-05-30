"""Focused standalone one-PBC tests for laboratory_information_management."""

from pathlib import Path

from .. import release_evidence, standalone, ui
from ..controls import laboratory_information_management_control_center, laboratory_information_management_mutation_preview


def _bootstrap() -> standalone.LaboratoryInformationManagementStandaloneApp:
    app = standalone.LaboratoryInformationManagementStandaloneApp(tenant="tenant_test")
    app.configure()
    app.register_defaults()
    return app


def test_standalone_lims_release_journey_runs_end_to_end():
    app = _bootstrap()
    accession = app.accession_sample(
        {
            "tenant": "tenant_test",
            "sample_id": "SMP-100",
            "accession_number": "ACC-100",
            "sample_type": "retain",
            "collected_at": "2026-05-29T08:00:00Z",
            "received_at": "2026-05-29T09:00:00Z",
            "collector": "collector_01",
            "received_by": "accessioner_01",
            "container": "amber_vial",
            "identity_confidence": 0.99,
            "storage_condition": "25C",
            "stability_expiry": "2026-08-31",
        }
    )
    custody = app.record_chain_of_custody(
        {
            "tenant": "tenant_test",
            "sample_id": "SMP-100",
            "from_actor": "accessioner_01",
            "to_actor": "analyst_ada",
            "location": "Chemistry Bench 4",
            "condition": "acceptable",
            "seal_status": "intact",
            "accepted": True,
        }
    )
    order = app.place_test_order(
        {
            "tenant": "tenant_test",
            "order_id": "ORD-100",
            "sample_id": "SMP-100",
            "ordered_by": "qa_release",
            "priority": "routine",
            "specimen_type": "retain",
            "tests": ("assay",),
        }
    )
    batch = app.create_batch_run(
        {
            "tenant": "tenant_test",
            "batch_run_id": "RUN-100",
            "order_id": "ORD-100",
            "sample_ids": ("SMP-100",),
            "method_id": standalone.DEFAULT_METHOD["method_id"],
            "instrument_id": standalone.DEFAULT_INSTRUMENT["instrument_id"],
            "analyst_id": standalone.DEFAULT_COMPETENCY["analyst_id"],
            "qc_lot_id": standalone.DEFAULT_QC_LOT["qc_lot_id"],
            "reagent_lot_ids": (standalone.DEFAULT_REAGENT_LOT["reagent_lot_id"],),
        }
    )
    qc = app.record_qc_measurement("RUN-100", 100.0, "qa_supervisor")
    result = app.import_result(
        {
            "tenant": "tenant_test",
            "result_id": "RES-100",
            "batch_run_id": "RUN-100",
            "sample_id": "SMP-100",
            "analyte": "assay",
            "value": 100.1,
        }
    )
    review = app.review_batch_run("RUN-100", "supervisor_a")
    released = app.release_result(
        "RES-100",
        technical_reviewer="supervisor_a",
        approver="qualified_person",
        signature_purpose="batch_release",
        signature_meaning="I certify the released result.",
    )
    coa = app.generate_certificate_of_analysis("ORD-100", "COA-100", "qualified_person")
    workbench = app.workbench("tenant_test")
    rendered = ui.laboratory_information_management_render_standalone_workbench(workbench)

    assert accession["ok"] is True
    assert custody["ok"] is True
    assert order["ok"] is True
    assert batch["ok"] is True
    assert qc["qc_result"]["passed"] is True
    assert result["result"]["status"] == "preliminary"
    assert review["ok"] is True
    assert released["result"]["status"] == "final"
    assert coa["certificate"]["result_ids"] == ("RES-100",)
    assert workbench["queue_counts"]["coa_ready"] >= 1
    assert rendered["ok"] is True
    assert rendered["control_center"]["audit_integrity_ok"] is True


def test_oos_stability_inventory_and_assistant_previews_are_governed():
    app = _bootstrap()
    app.adjust_reagent_inventory(
        {
            "reagent_lot_id": standalone.DEFAULT_REAGENT_LOT["reagent_lot_id"],
            "expiry_date": "2026-12-31",
            "storage_condition": "ambient",
            "qualification_status": "qualified",
            "quantity_on_hand": 9,
            "reorder_point": 10,
        }
    )
    accession = app.accession_sample(
        {
            "tenant": "tenant_test",
            "sample_id": "SMP-200",
            "accession_number": "ACC-200",
            "sample_type": "retain",
            "collected_at": "2026-05-29T08:00:00Z",
            "received_at": "2026-05-29T09:00:00Z",
            "collector": "collector_02",
            "received_by": "accessioner_02",
            "container": "amber_vial",
            "identity_confidence": 0.99,
            "storage_condition": "25C",
            "stability_expiry": "2026-08-31",
        }
    )
    order = app.place_test_order(
        {
            "tenant": "tenant_test",
            "order_id": "ORD-200",
            "sample_id": "SMP-200",
            "ordered_by": "qa_release",
            "priority": "stat",
            "specimen_type": "retain",
            "tests": ("assay",),
        }
    )
    batch = app.create_batch_run(
        {
            "tenant": "tenant_test",
            "batch_run_id": "RUN-200",
            "order_id": "ORD-200",
            "sample_ids": ("SMP-200",),
            "method_id": standalone.DEFAULT_METHOD["method_id"],
            "instrument_id": standalone.DEFAULT_INSTRUMENT["instrument_id"],
            "analyst_id": standalone.DEFAULT_COMPETENCY["analyst_id"],
            "qc_lot_id": standalone.DEFAULT_QC_LOT["qc_lot_id"],
            "reagent_lot_ids": (standalone.DEFAULT_REAGENT_LOT["reagent_lot_id"],),
        }
    )
    qc = app.record_qc_measurement("RUN-200", 100.4, "qa_supervisor")
    result = app.import_result(
        {
            "tenant": "tenant_test",
            "result_id": "RES-200",
            "batch_run_id": "RUN-200",
            "sample_id": "SMP-200",
            "analyte": "assay",
            "value": 103.5,
        }
    )
    review = app.review_batch_run("RUN-200", "supervisor_b")
    blocked_release = app.release_result(
        "RES-200",
        technical_reviewer="supervisor_b",
        approver="qualified_person",
        signature_purpose="batch_release",
        signature_meaning="Attempt release of OOS result.",
    )
    oos = app.open_oos_investigation("RES-200", "Assay above specification", "qa_owner")
    resolved = app.resolve_oos_investigation(
        "RES-200",
        disposition="report_with_comment",
        approver="qa_owner",
        conclusion="Confirmed assignable cause and batch impact documented.",
    )
    released = app.release_result(
        "RES-200",
        technical_reviewer="supervisor_b",
        approver="qualified_person",
        signature_purpose="exception_release",
        signature_meaning="Approved after documented OOS disposition.",
    )
    study = app.create_stability_study(
        {
            "study_id": "STAB-200",
            "sample_id": "SMP-200",
            "protocol_id": "PROT-200",
            "storage_condition": "25C/60RH",
            "timepoints": ("T0", "M1", "M3"),
        }
    )
    pull = app.schedule_stability_pull("STAB-200", "M1", "2026-06-30")
    done = app.complete_stability_pull(pull["pull"]["pull_id"], "2026-06-30", "Stable at M1.")
    preview = app.document_instruction_preview(
        "Prepare CoA for order ORD-200.\nReview reagent lot REAGENT-MOBILE-PHASE-01.\nAnalyst competency renewal needed.",
        "create a preview for certificate issuance and reagent follow-up",
        requested_action="create",
    )
    mutation = laboratory_information_management_mutation_preview(
        "update",
        "laboratory_information_management_result",
        {"result_id": "RES-200"},
    )
    control_center = laboratory_information_management_control_center(app.workbench("tenant_test"))

    assert accession["ok"] is True
    assert order["ok"] is True
    assert batch["ok"] is True
    assert qc["ok"] is True
    assert result["result"]["status"] == "oos_hold"
    assert review["ok"] is True
    assert blocked_release["ok"] is False
    assert blocked_release["reason"] == "release_blocked"
    assert oos["ok"] is True
    assert resolved["ok"] is True
    assert released["ok"] is True
    assert study["ok"] is True
    assert pull["ok"] is True
    assert done["pull"]["status"] == "completed"
    assert preview["preview"]["requires_confirmation"] is True
    assert preview["preview"]["citations"]
    assert mutation["ok"] is True
    assert control_center["assistant_guardrails"]["requires_confirmation_for_mutation"] is True
    assert "inventory_watch" in app.workbench("tenant_test")["queue_counts"]


def test_standalone_smoke_release_evidence_and_docs_exist():
    smoke = standalone.standalone_smoke_test()
    evidence = release_evidence.build_release_evidence()
    validation = release_evidence.validate_release_evidence()
    base = Path(__file__).resolve().parent.parent

    assert smoke["ok"] is True
    assert evidence["standalone_app"]["ok"] is True
    assert evidence["documentation"]["ok"] is True
    assert validation["ok"] is True
    for name in ("README.md", "implementation-plan.md", "implementation-status.md", "RELEASE_EVIDENCE.md"):
        assert (base / name).exists() is True
