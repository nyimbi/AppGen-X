"""Focused contract smoke tests for loyalty_rewards."""

from ..manifest import PBC_MANIFEST
from ..events import EVENT_CONTRACT
from ..schema_contract import SCHEMA_CONTRACT
from ..service_contract import SERVICE_CONTRACT
from ..release_evidence import RELEASE_EVIDENCE


def test_generated_schema_service_and_release_evidence():
    from .. import models, release_evidence, schema_contract

    assert SCHEMA_CONTRACT["pbc"] == "loyalty_rewards"
    assert SCHEMA_CONTRACT["ok"] is True
    assert SCHEMA_CONTRACT["owned_tables"]
    schema_smoke = schema_contract.smoke_test()
    model_smoke = models.smoke_test()
    release_manifest = release_evidence.release_readiness_manifest()
    release_validation = release_evidence.validate_release_evidence()
    release_smoke = release_evidence.smoke_test()

    assert schema_smoke["ok"] is True
    assert model_smoke["ok"] is True
    assert SERVICE_CONTRACT["pbc"] == "loyalty_rewards"
    assert SERVICE_CONTRACT["ok"] is True
    assert RELEASE_EVIDENCE["pbc"] == "loyalty_rewards"
    assert RELEASE_EVIDENCE["ok"] is True
    assert release_manifest["ok"] is True
    assert release_validation["ok"] is True
    assert release_smoke["ok"] is True
    assert not release_manifest["blocking_gaps"]
    assert not release_validation["missing_sections"]
    assert not release_validation["failed_checks"]
    assert not release_validation["boundary_gaps"]


def test_manifest_and_event_contract():
    from .. import events

    assert PBC_MANIFEST["pbc"] == "loyalty_rewards"
    assert PBC_MANIFEST["template"] == "standalone_one_pbc_app"
    assert PBC_MANIFEST["standard_features"]
    assert PBC_MANIFEST["advanced_capabilities"]
    assert EVENT_CONTRACT["contract"] == "appgen_event_contract"
    manifest = events.event_contract_manifest()
    validation = events.validate_event_contract()
    smoke = events.smoke_test()

    assert manifest["ok"] is True
    assert validation["ok"] is True
    assert smoke["ok"] is True
    assert manifest["stream_engine_picker_visible"] is False
    assert not validation["invalid_tables"]
    assert not validation["invalid_emitted"]
    assert not validation["invalid_consumed"]


def test_registration_plan_is_side_effect_free():
    from .. import package_discovery_plan, package_metadata_manifest, register_pbc, registration_plan, validate_package_metadata

    assert register_pbc()["pbc"] == "loyalty_rewards"
    plan = registration_plan()
    metadata = package_metadata_manifest()
    metadata_validation = validate_package_metadata()
    discovery = package_discovery_plan()

    assert plan["ok"] is True
    assert plan["catalog_patch"]
    assert metadata["ok"] is True
    assert metadata_validation["ok"] is True
    assert discovery["ok"] is True
    assert metadata["event_contract"] == "AppGen-X"
    assert metadata["stream_engine_picker_visible"] is False
    assert not metadata_validation["missing_entrypoints"]
    assert not metadata_validation["missing_publish_artifacts"]
    assert not metadata_validation["missing_capability_evidence"]
    assert not metadata_validation["invalid"]


def test_service_and_route_surface_are_executable():
    from .. import routes, services

    service_smoke = services.smoke_test()
    operation_contracts = services.service_operation_contracts()
    route_contracts = routes.api_route_contracts()
    route_validation = routes.validate_api_route_contracts()
    route_smoke = routes.smoke_test()

    assert service_smoke["ok"] is True
    assert operation_contracts["ok"] is True
    assert route_contracts["ok"] is True
    assert route_validation["ok"] is True
    assert route_contracts["contracts"]
    assert all(item["permission"] for item in route_contracts["contracts"])
    assert all(item["event_contract"] == "AppGen-X" for item in route_contracts["contracts"])
    assert all(item["stream_engine_picker_visible"] is False for item in route_contracts["contracts"])
    assert all(item["shared_table_access"] is False for item in route_contracts["contracts"])
    assert not route_validation["service_mismatches"]
    assert not route_validation["missing_idempotency"]
    assert not route_validation["invalid_table_scope"]
    assert route_smoke["ok"] is True


def test_configuration_permissions_and_seed_hooks_are_executable():
    from .. import config, permissions, seed_data

    config_smoke = config.smoke_test()
    governance_smoke = config.governance_smoke_test()
    permission_smoke = permissions.smoke_test()
    seed_smoke = seed_data.smoke_test()

    assert config_smoke["ok"] is True
    assert governance_smoke["ok"] is True
    assert governance_smoke["parameter"]["accepted"] is True
    assert governance_smoke["compiled_rule"]["compiled"] is True
    assert governance_smoke["rule_decision"]["allowed"] is True
    assert permission_smoke["ok"] is True
    assert seed_smoke["ok"] is True
    assert seed_smoke["validation"]["plan"]["standalone_bundle"]["members"]


def test_ui_workbench_surface_is_executable():
    from .. import ui

    smoke = ui.smoke_test()

    assert smoke["ok"] is True
    assert smoke["contract"]["forms"]
    assert smoke["contract"]["wizards"]
    assert smoke["contract"]["controls"]
    assert smoke["rendered"]["cards"]


def test_event_handlers_are_idempotent_and_retryable():
    from .. import handlers

    smoke = handlers.smoke_test()

    assert smoke["ok"] is True
    assert smoke["manifest"]["handlers"]
    assert smoke["first_result"]["retry_policy"]
    assert smoke["first_result"]["dead_letter_table"].startswith("loyalty_rewards_")
    assert smoke["duplicate_result"]["duplicate"] is True
    assert smoke["unknown_result"]["handled"] is False


def test_table_stakes_and_advanced_capability_assurance_is_executable():
    from .. import capability_assurance

    manifest = capability_assurance.table_stakes_capability_manifest()
    validation = capability_assurance.validate_table_stakes_capability_coverage()
    smoke = capability_assurance.smoke_test()

    assert manifest["ok"] is True
    assert validation["ok"] is True
    assert smoke["ok"] is True
    assert manifest["standard_features"]
    assert manifest["advanced_capabilities"]
    assert not validation["missing_standard"]
    assert not validation["missing_advanced"]
    assert not validation["missing_operations"]
    assert not validation["uncovered_features"]
    assert not validation["invalid_tables"]
    assert not validation["invalid_backends"]
    assert validation["stream_picker_visible"] is False
    assert validation["event_contract"] == "AppGen-X"
    assert validation["owned_boundary_rejection"]["ok"] is False
    assert validation["owned_boundary_rejection"]["violations"]


def test_advanced_loyalty_rewards_runtime_surface_is_executable():
    from ..runtime import LOYALTY_REWARDS_OWNED_TABLES
    from ..runtime import loyalty_rewards_build_api_contract
    from ..runtime import loyalty_rewards_build_service_contract
    from ..runtime import loyalty_rewards_runtime_smoke

    required_tables = {
        "reward_tier",
        "tier_benefit",
        "referral_reward",
        "partner_accrual",
        "offer_eligibility",
        "liability_snapshot",
        "fraud_review",
        "churn_risk_score",
        "breakage_forecast",
        "offer_simulation",
        "loyalty_exception",
        "balance_reconciliation",
        "reward_balance_proof",
        "loyalty_audit_entry",
        "rewards_policy_screening",
        "liability_control_assertion",
        "loyalty_federation_view",
        "loyalty_governed_model",
    }
    required_commands = {
        "qualify_tier",
        "grant_referral_reward",
        "record_partner_accrual",
        "evaluate_offer_eligibility",
        "snapshot_liability",
        "review_fraud_risk",
        "forecast_breakage",
        "simulate_offer",
        "resolve_loyalty_exception",
        "reconcile_balance",
        "generate_balance_proof",
        "run_liability_controls",
        "register_governed_model",
    }
    smoke = loyalty_rewards_runtime_smoke()
    service = loyalty_rewards_build_service_contract()
    api = loyalty_rewards_build_api_contract()

    assert smoke["ok"] is True
    assert required_tables <= set(LOYALTY_REWARDS_OWNED_TABLES)
    assert required_commands <= set(service["command_methods"])
    assert service["configuration_schema"]["event_contract"] == "AppGen-X"
    assert service["external_dependencies"]["shared_tables"] == ()
    assert api["shared_table_access"] is False
    assert api["stream_engine_picker_visible"] is False


def test_agent_and_standalone_application_surfaces_are_executable():
    from .. import agent, standalone

    agent_smoke = agent.smoke_test()
    standalone_manifest = standalone.standalone_application_manifest()
    standalone_validation = standalone.validate_standalone_application()
    standalone_smoke = standalone.smoke_test()

    assert agent_smoke["ok"] is True
    assert standalone_manifest["ok"] is True
    assert standalone_validation["ok"] is True
    assert standalone_smoke["ok"] is True
    assert standalone_manifest["mode"] == "standalone_one_pbc_app"
    assert standalone_manifest["bootstrap"]["account_count"] >= 1
    assert standalone_manifest["ui"]["forms"]
    assert standalone_manifest["ui"]["wizards"]
    assert standalone_manifest["ui"]["controls"]
    assert standalone_manifest["agent"]["skills"]
    assert not standalone_validation["missing_workflows"]
    assert not standalone_validation["missing_sections"]


def test_package_repo_gate_audits_are_true():
    from .. import release_evidence

    evidence = release_evidence.build_release_evidence()

    assert evidence["repo_gate_results"]["pbc_spec_source_audit"] is True
    assert evidence["repo_gate_results"]["pbc_implementation_release_audit"] is True
    assert evidence["repo_gate_results"]["pbc_generation_smoke_audit"] is True
