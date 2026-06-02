"""Standalone app smoke tests for clinical_care_coordination."""

from __future__ import annotations

from pyAppGen.pbcs.clinical_care_coordination.routes import dispatch_route
from pyAppGen.pbcs.clinical_care_coordination.services import ClinicalCareCoordinationService
from pyAppGen.pbcs.clinical_care_coordination.standalone import ClinicalCareCoordinationStandaloneApp
from pyAppGen.pbcs.clinical_care_coordination.standalone import smoke_test
from pyAppGen.pbcs.clinical_care_coordination.ui import clinical_care_coordination_standalone_app_contract


def test_standalone_manifest_and_smoke():
    contract = clinical_care_coordination_standalone_app_contract()
    app_smoke = smoke_test()
    assert contract["ok"] is True
    assert app_smoke["ok"] is True
    assert contract["forms"]
    assert contract["wizards"]
    assert contract["controls"]


def test_standalone_app_can_bootstrap_and_render():
    app = ClinicalCareCoordinationStandaloneApp()
    app.load_demo_workspace(patient_ref="patient-standalone")
    rendered = app.render_workbench()
    assert rendered["ok"] is True
    assert rendered["queue_counts"]["high_risk_patients"] >= 1
    assert rendered["shell"]["app_id"] == "clinical_care_coordination_one_pbc_app"


def test_route_dispatch_executes_with_live_service():
    service = ClinicalCareCoordinationService()
    created = dispatch_route(
        "POST /patient-care-plans",
        {
            "patient_ref": "patient-route",
            "problem": "care coordination route check",
            "goal": "confirm dispatch execution",
            "responsible_role": "primary_coordinator",
            "review_cadence_days": 5,
            "state": "active",
        },
        service=service,
    )
    forms = dispatch_route("GET /clinical-care-coordination/forms", service=service)
    workbench = dispatch_route("GET /clinical-care-coordination-workbench", service=service)
    assert created["ok"] is True
    assert created["result"]["care_plan"]["patient_ref"] == "patient-route"
    assert forms["result"]["ok"] is True
    assert workbench["result"]["queue_counts"]["care_team_coverage_gaps"] == 1
