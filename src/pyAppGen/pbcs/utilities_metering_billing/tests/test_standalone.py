"""Standalone Utilities Metering and Billing PBC tests."""
from pyAppGen.pbcs.utilities_metering_billing.controls import control_catalog, evaluate_control
from pyAppGen.pbcs.utilities_metering_billing.forms import form_catalog, form_for
from pyAppGen.pbcs.utilities_metering_billing.slice_app import ALLOWED_DATABASE_BACKENDS, APPGEN_X_TOPIC, build_standalone_app
from pyAppGen.pbcs.utilities_metering_billing.standalone import single_pbc_app_contract, standalone_smoke_test
from pyAppGen.pbcs.utilities_metering_billing.wizards import wizard_catalog, wizard_for


def test_single_pbc_app_contract_surfaces_executable_runtime_ui_agent_and_dsl():
    contract = single_pbc_app_contract()
    assert contract["ok"] is True
    assert contract["pbc"] == "utilities_metering_billing"
    assert contract["event_contract"] == "AppGen-X"
    assert contract["stream_engine_picker_visible"] is False
    assert "postgresql" in ALLOWED_DATABASE_BACKENDS
    assert contract["schema"]["ok"] is True
    assert contract["services"]["ok"] is True
    assert contract["routes"]["ok"] is True
    assert contract["ui"]["stream_engine_picker_visible"] is False
    assert contract["agent"]["ok"] is True
    assert contract["release_evidence"]["ok"] is True
    assert contract["dsl"]["single_pbc_app"] is True


def test_forms_wizards_and_controls_cover_utility_billing_table_stakes():
    forms = {item["id"] for item in form_catalog()["forms"]}
    wizards = {item["id"] for item in wizard_catalog()["wizards"]}
    controls = set(control_catalog()["controls"])
    assert {"service-point-intake", "meter-read-capture", "tariff-version-review", "billing-cycle-run", "adjustment-maker-checker", "dispute-case-form"}.issubset(forms)
    assert {"meter-exchange-wizard", "estimate-review-wizard", "bill-run-approval-wizard", "disconnect-reconnect-wizard", "regulatory-report-wizard"}.issubset(wizards)
    assert {"owned-boundary-control", "read-provenance-control", "estimate-streak-control", "maker-checker-control", "protected-customer-control", "appgen-event-control", "confirmation-gate-control", "release-evidence-control"}.issubset(controls)
    assert form_for("meter-read-capture")["ok"] is True
    assert wizard_for("bill-run-approval-wizard")["ok"] is True


def test_meter_to_bill_positive_and_negative_paths_execute():
    app = build_standalone_app()
    assert app.configure_runtime({"database_backend":"postgresql", "event_topic":APPGEN_X_TOPIC})["ok"] is True
    assert app.configure_runtime({"database_backend":"sqlite", "event_topic":APPGEN_X_TOPIC})["ok"] is False
    assert app.create_service_point({"service_point_id":"sp-1", "premise_code":"PREM-1"})["ok"] is True
    assert app.register_meter_asset({"meter_asset_id":"meter-1", "serial_number":"MTR-1"})["ok"] is True
    bad_read = app.create_meter_read({"meter_read_id":"read-bad", "service_point_id":"sp-1", "meter_asset_id":"meter-1", "read_value":10})
    assert bad_read["ok"] is False
    good_read = app.create_meter_read({"meter_read_id":"read-1", "service_point_id":"sp-1", "meter_asset_id":"meter-1", "read_value":1450.0, "read_source":"ami", "collector_id":"ami", "device_session":"sess", "acquisition_time":"2026-01-31T10:00:00Z"})
    assert good_read["ok"] is True
    assert app.validate_meter_read({"read_value":1450.0, "previous_read_value":1320.0, "service_point_status":"live", "read_at":"2026-01-31", "cycle_start":"2026-01-01", "cycle_end":"2026-01-31", "historical_average":150.0})["ok"] is True
    assert app.record_usage_interval({"expected_interval_count":48, "actual_interval_count":47, "timezone_name":"Africa/Nairobi"})["ok"] is False
    assert app.record_usage_interval({"expected_interval_count":48, "actual_interval_count":48, "timezone_name":"Africa/Nairobi"})["ok"] is True
    assert app.estimate_usage_gap({"adjacent_actual_reads":True, "quantity":120.0})["ok"] is True
    assert app.review_tariff({"tariff_code":"ELEC", "effective_start":"2026-01-01", "effective_end":"2026-12-31"})["ok"] is True
    assert app.approve_service_order({"order_type":"disconnect_non_payment", "protected_status":True, "moratorium_enabled":True})["ok"] is False
    assert app.create_billing_cycle({"cycle_code":"CYCLE-1"})["ok"] is True
    assert app.simulate_utility_bill({"service_point_id":"sp-1", "import_quantity":130.0, "export_quantity":10.0, "peak_demand_kw":6.0})["ok"] is True
    assert app.create_billing_adjustment({"approval_state":"approved", "maker":"same", "checker":"same"})["ok"] is False
    assert app.create_billing_adjustment({"approval_state":"approved", "maker":"maker", "checker":"checker"})["ok"] is True
    assert app.open_dispute_case({"utility_bill_id":"bill-1"})["ok"] is True
    assert app.datastore_crud_plan("create", table="foreign_table", payload={})["ok"] is False
    assert app.datastore_crud_plan("create", table="utilities_metering_billing_meter_read", payload={})["requires_confirmation"] is True


def test_controls_fail_closed_for_unknown_and_protected_actions():
    assert evaluate_control("unknown", {})["ok"] is False
    assert evaluate_control("confirmation-gate-control", {})["ok"] is True
    assert evaluate_control("agent_mutation_confirmation", {"confirmed":False})["missing"] == ("known_control",)
    assert evaluate_control("disconnect_moratorium_guard", {"moratorium_enabled":True, "protected_customer":True})["ok"] is False


def test_standalone_smoke_test_runs_without_side_effects():
    smoke = standalone_smoke_test()
    assert smoke["ok"] is True
    assert smoke["side_effects"] == ()
    assert smoke["slice_app"]["ok"] is True
    assert smoke["contract"]["schema"]["ok"] is True
