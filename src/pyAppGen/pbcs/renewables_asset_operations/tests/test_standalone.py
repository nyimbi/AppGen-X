from pyAppGen.pbcs.renewables_asset_operations.controls import evaluate_control
from pyAppGen.pbcs.renewables_asset_operations.forms import form_catalog, form_for
from pyAppGen.pbcs.renewables_asset_operations.standalone import (
    RenewablesAssetOperationsStandaloneApp,
    single_pbc_app_contract,
    standalone_smoke_test,
)
from pyAppGen.pbcs.renewables_asset_operations.wizards import wizard_catalog, wizard_for


def test_single_pbc_app_contract_exposes_renewables_surface():
    contract = single_pbc_app_contract()
    assert contract["ok"] is True
    assert contract["database_backends"] == ("postgresql", "mysql", "mariadb")
    assert contract["event_contract"] == "AppGen-X"
    assert contract["stream_engine_picker_visible"] is False
    assert contract["dsl"]["skills_namespace"] == "renewables_asset_operations_skills"
    assert len(contract["forms"]["forms"]) >= 12
    assert len(contract["wizards"]["wizards"]) >= 10
    assert len(contract["controls"]["controls"]) >= 13


def test_forms_and_wizards_cover_asset_operations_specialties():
    assert form_catalog()["ok"] is True
    assert form_for("telemetry_meter_reconciliation")["form"]["owned_table"] == "renewables_asset_operations_generation_reading"
    assert form_for("safety_lockout")["ok"] is True
    assert wizard_catalog()["ok"] is True
    assert wizard_for("curtailment_recovery")["ok"] is True
    assert wizard_for("performance_rca")["ok"] is True


def test_controls_block_safety_commercial_and_data_quality_failures():
    assert evaluate_control("asset_hierarchy_complete", {"site": "S"})["ok"] is False
    assert evaluate_control("meter_reconciliation_within_tolerance", {"variance": 0.1, "tolerance": 0.5})["ok"] is True
    assert evaluate_control("remote_reset_not_allowed_during_lockout", {"lockout": True, "remote_reset": True})["ok"] is False
    assert evaluate_control("storage_dispatch_compliant", {"delivered": 8, "committed": 10})["ok"] is False
    assert evaluate_control("agent_mutations_require_confirmation", {"confirmed": False})["ok"] is False


def test_standalone_renewables_workflow_is_executable_and_guarded():
    app = RenewablesAssetOperationsStandaloneApp()
    assert app.configure()["ok"] is True
    assert app.register_asset("A0", "Site", None, None)["ok"] is False
    assert app.register_asset("A1", "Site", "solar", "POI-1", nameplate_mw=50)["ok"] is True
    assert app.reconcile_reading("G0", "A1", 10, 8, tolerance=0.5)["ok"] is False
    assert app.reconcile_reading("G1", "A1", 10, 9.8, tolerance=0.5)["ok"] is True
    assert app.classify_curtailment("C0", "A1", "grid", 20, 10, evidence=None)["ok"] is False
    assert app.classify_curtailment("C1", "A1", "grid", 20, 10, evidence="dispatch")["ok"] is True
    assert app.lock_availability_pack("AV0", "A1", .98, .95, exclusion=True, approved=False)["ok"] is False
    assert app.lock_availability_pack("AV1", "A1", .98, .95, exclusion=True, approved=True)["ok"] is True
    assert app.track_ppa_obligation("P0", "A1", .95, late=True)["ok"] is False
    assert app.track_ppa_obligation("P1", "A1", .95, late=True, waiver=True)["ok"] is True
    assert app.release_work_order("W0", "A1", "inverter", 8, permit=False)["ok"] is False
    assert app.release_work_order("W1", "A1", "inverter", 8, permit=True)["ok"] is True
    assert app.enforce_safety_hold("H0", "A1", lockout=True, remote_reset=True)["ok"] is False
    assert app.enforce_safety_hold("H1", "A1", lockout=True, remote_reset=False)["ok"] is True
    assert app.record_inspection("I1", "A1", "solar walk", ("photo",), ("hotspot",))["ok"] is True
    assert app.prepare_warranty_claim("WC0", "A1", recurrence=1, threshold=2, evidence="faults")["ok"] is False
    assert app.prepare_warranty_claim("WC1", "A1", recurrence=3, threshold=2, evidence="faults")["ok"] is True
    assert app.close_performance_rca("R0", "A1", 100, 80, "soiling")["ok"] is False
    assert app.close_performance_rca("R1", "A1", 100, 80, "soiling", "recovered")["ok"] is True
    assert app.review_storage_dispatch("S0", "A1", 8, 10, 12, 10)["ok"] is False
    assert app.review_storage_dispatch("S1", "A1", 10, 10, 12, 10)["ok"] is True
    assert app.record_environmental_evidence("E0", "A1", regulated=True)["ok"] is False
    assert app.record_environmental_evidence("E1", "A1", regulated=True, permit="water")["ok"] is True
    assert app.simulate_curtailment_recovery("grid", 100, .85)["mutates_live_records"] is False
    assert app.assistant_operator_action_preview("ppa", "create", False)["ok"] is False
    assert app.assistant_operator_action_preview("ppa", "create", True)["ok"] is True


def test_standalone_smoke_proves_single_pbc_readiness():
    smoke = standalone_smoke_test()
    assert smoke["ok"] is True
    assert smoke["contract"]["routes"]["stream_engine_picker_visible"] is False
