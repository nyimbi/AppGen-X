"""Focused standalone one-PBC tests for policy_administration_insurance."""

from pathlib import Path

from .. import agent, release_evidence, standalone, ui



def test_standalone_application_executes_policy_lifecycle_surface():
    bundle = standalone.bootstrap_policy_administration_insurance_standalone_app(
        tenant="tenant_test"
    )
    app = bundle["application"]
    created = app.create_policy(
        {
            "code": "POLICY-TEST-001",
            "product_code": "COMMERCIAL_PROPERTY",
            "insured_name": "Test Insured",
        }
    )
    coverage = app.run_domain_operation(
        "record_coverage_item",
        {"policy_id": "POLICY-TEST-001", "coverage_type": "property"},
    )
    endorsement = app.run_domain_operation(
        "review_endorsement",
        {"policy_id": "POLICY-TEST-001", "change_type": "limit_increase"},
    )
    received = app.receive_event({"idempotency_key": "policy-standalone-test"})
    workbench = app.workbench_summary()
    rendered = app.render_workbench()
    document = app.document_intake_plan(
        "endorsement packet",
        "review endorsement and assemble policy documents",
    )
    crud = app.datastore_crud_plan(
        "create",
        "policy_administration_insurance_policy_document",
        {"policy_document_id": "DOC-TEST-001"},
    )
    evidence = app.release_snapshot()

    assert bundle["ok"] is True
    assert created["ok"] is True
    assert coverage["ok"] is True
    assert endorsement["ok"] is True
    assert received["ok"] is True
    assert workbench["ok"] is True
    assert rendered["ok"] is True
    assert document["ok"] is True
    assert crud["ok"] is True
    assert evidence["ok"] is True
    assert rendered["rendered"]["forms"]
    assert document["wizard_candidates"]
    assert crud["form_candidates"]
    assert evidence["standalone_app"]["ok"] is True
    assert evidence["documentation"]["ok"] is True



def test_standalone_contract_ui_agent_and_release_surfaces_are_wired():
    contract = standalone.policy_administration_insurance_standalone_app_contract()
    smoke = standalone.policy_administration_insurance_standalone_smoke()
    workspace = agent.standalone_agent_workspace_contract()
    ui_contract = ui.policy_administration_insurance_ui_contract()
    standalone_workbench = ui.policy_administration_insurance_standalone_workbench_blueprint()
    validation = release_evidence.validate_release_evidence()

    assert contract["ok"] is True
    assert smoke["ok"] is True
    assert workspace["ok"] is True
    assert ui_contract["forms"]
    assert ui_contract["wizards"]
    assert ui_contract["controls"]
    assert standalone_workbench["ok"] is True
    assert validation["ok"] is True



def test_package_local_docs_exist_for_release_evidence():
    base = Path(__file__).resolve().parent.parent
    for name in (
        "README.md",
        "implementation-plan.md",
        "implementation-status.md",
        "SPECIFICATION.md",
        "RELEASE_EVIDENCE.md",
    ):
        assert (base / name).exists() is True
