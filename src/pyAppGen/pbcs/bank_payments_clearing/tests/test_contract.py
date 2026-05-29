"""Focused package contract and gate tests for bank_payments_clearing."""

from __future__ import annotations

from pathlib import Path

from .. import PBC_KEY
from .. import capability_assurance
from .. import config
from .. import events
from .. import handlers
from .. import implementation_contract
from .. import package_discovery_plan
from .. import package_metadata_manifest
from .. import register_pbc
from .. import registration_plan
from .. import validate_package_metadata
from .. import release_evidence
from .. import routes
from .. import seed_data
from .. import services
from .. import smoke_test
from .. import standalone
from .. import ui
from ..agent import chatbot_interface_contract, composed_agent_contribution, datastore_crud_plan, document_instruction_plan
from ..models import database_model_contract, model_manifest
from ..permissions import permission_manifest, smoke_test as permissions_smoke_test
from ..schema_contract import build_schema_contract, validate_schema_contract
from ..service_contract import SERVICE_CONTRACT, validate_service_contract


PACKAGE_DIR = Path(__file__).resolve().parents[1]


def test_generated_schema_service_and_release_evidence():
    assert build_schema_contract()["pbc"] == PBC_KEY
    assert validate_schema_contract()["ok"] is True
    assert model_manifest()["ok"] is True
    assert database_model_contract()["ok"] is True
    assert SERVICE_CONTRACT["pbc"] == PBC_KEY
    assert SERVICE_CONTRACT["ok"] is True
    assert validate_service_contract()["ok"] is True
    assert release_evidence.build_release_evidence()["ok"] is True
    assert release_evidence.validate_release_evidence()["ok"] is True
    assert release_evidence.smoke_test()["ok"] is True


def test_manifest_event_and_package_metadata_are_consistent():
    manifest = events.event_contract_manifest()
    validation = events.validate_event_contract()
    metadata = package_metadata_manifest()
    discovery = package_discovery_plan()
    impl = implementation_contract()
    assert register_pbc()["pbc"] == PBC_KEY
    assert manifest["ok"] is True
    assert validation["ok"] is True
    assert metadata["ok"] is True
    assert discovery["ok"] is True
    assert impl["standalone_app_contract"]["ok"] is True
    assert metadata["event_contract"] == "AppGen-X"
    assert metadata["stream_engine_picker_visible"] is False


def test_registration_plan_is_side_effect_free():
    plan = registration_plan()
    assert plan["ok"] is True
    assert plan["catalog_patch"]
    assert validate_package_metadata()["ok"] is True


def test_service_and_route_surface_are_executable():
    service_smoke = services.smoke_test()
    route_validation = routes.validate_api_route_contracts()
    route_smoke = routes.smoke_test()
    assert service_smoke["ok"] is True
    assert services.service_operation_contracts()["ok"] is True
    assert route_validation["ok"] is True
    assert route_smoke["ok"] is True
    assert not route_validation["service_mismatches"]
    assert not route_validation["missing_idempotency"]
    assert not route_validation["invalid_table_scope"]


def test_configuration_permissions_seed_and_ui_are_executable():
    assert config.smoke_test()["ok"] is True
    assert config.governance_smoke_test()["ok"] is True
    assert permission_manifest()["ok"] is True
    assert permissions_smoke_test()["ok"] is True
    assert seed_data.smoke_test()["ok"] is True
    assert ui.smoke_test()["ok"] is True
    assert standalone.workbench_smoke_test()["ok"] is True


def test_event_handlers_agent_and_capability_assurance_are_executable():
    handler_smoke = handlers.smoke_test()
    assurance = capability_assurance.smoke_test()
    document_plan = document_instruction_plan(
        "instruction_id=pay_test participant_bank_id=bank_test rail=ach amount=250 currency=USD external_reference=EXT-TEST",
        "release the payment after validation",
    )
    crud_plan = datastore_crud_plan("create", "bank_payments_clearing_payment_instruction", {"state": "validated"})
    delete_plan = datastore_crud_plan("delete", "bank_payments_clearing_payment_instruction")
    assert handler_smoke["ok"] is True
    assert assurance["ok"] is True
    assert chatbot_interface_contract()["ok"] is True
    assert composed_agent_contribution()["ok"] is True
    assert document_plan["ok"] is True
    assert document_plan["mutation_preview"]
    assert crud_plan["ok"] is True
    assert crud_plan["event_contract"] == "AppGen-X"
    assert delete_plan["supported"] is False


def test_release_repo_gates_are_present_and_passing():
    evidence = release_evidence.build_release_evidence()
    assert set(evidence["repo_gate_results"]) == {
        "pbc_source_artifact_contract",
        "pbc_implementation_release_audit",
        "pbc_generation_smoke_audit",
    }
    assert all(evidence["repo_gate_results"].values()) is True
    assert PACKAGE_DIR.joinpath("standalone.py").exists()
    assert smoke_test()["ok"] is True
