from pyAppGen.pbcs.hotel_revenue_management import implementation_contract
from pyAppGen.pbcs.hotel_revenue_management import package_discovery_plan
from pyAppGen.pbcs.hotel_revenue_management import package_metadata_manifest
from pyAppGen.pbcs.hotel_revenue_management import validate_package_metadata
from pyAppGen.pbcs.hotel_revenue_management.agent import agent_skill_manifest
from pyAppGen.pbcs.hotel_revenue_management.agent import chatbot_interface_contract
from pyAppGen.pbcs.hotel_revenue_management.agent import datastore_crud_plan
from pyAppGen.pbcs.hotel_revenue_management.agent import document_instruction_plan
from pyAppGen.pbcs.hotel_revenue_management.config import governance_smoke_test
from pyAppGen.pbcs.hotel_revenue_management.events import event_contract_manifest
from pyAppGen.pbcs.hotel_revenue_management.events import validate_event_contract
from pyAppGen.pbcs.hotel_revenue_management.handlers import dispatch_event
from pyAppGen.pbcs.hotel_revenue_management.handlers import handler_manifest
from pyAppGen.pbcs.hotel_revenue_management.release_evidence import build_release_evidence
from pyAppGen.pbcs.hotel_revenue_management.release_evidence import release_readiness_manifest
from pyAppGen.pbcs.hotel_revenue_management.release_evidence import validate_release_evidence
from pyAppGen.pbcs.hotel_revenue_management.routes import api_route_contracts
from pyAppGen.pbcs.hotel_revenue_management.routes import dispatch_route
from pyAppGen.pbcs.hotel_revenue_management.routes import validate_api_route_contracts
from pyAppGen.pbcs.hotel_revenue_management.schema_contract import build_schema_contract
from pyAppGen.pbcs.hotel_revenue_management.service_contract import build_service_contract
from pyAppGen.pbcs.hotel_revenue_management.services import HotelRevenueManagementService
from pyAppGen.pbcs.hotel_revenue_management.services import service_operation_contracts


def test_generated_schema_service_and_release_evidence():
    assert build_schema_contract()["ok"] is True
    assert build_service_contract()["ok"] is True
    assert build_release_evidence()["ok"] is True
    assert release_readiness_manifest()["ok"] is True
    assert validate_release_evidence()["ok"] is True


def test_manifest_and_event_contract():
    assert implementation_contract()["pbc"] == "hotel_revenue_management"
    assert event_contract_manifest()["ok"] is True
    assert validate_event_contract()["ok"] is True


def test_agent_chatbot_skills_are_executable():
    assert agent_skill_manifest()["ok"] is True
    assert chatbot_interface_contract()["ok"] is True
    assert document_instruction_plan("forecast sheet", "update bar and inventory")["ok"] is True
    assert datastore_crud_plan("create")["ok"] is True
    assert datastore_crud_plan("update", table="foreign_table")["ok"] is False


def test_registration_plan_is_side_effect_free():
    assert package_metadata_manifest()["pbc"] == "hotel_revenue_management"
    assert validate_package_metadata()["ok"] is True
    assert package_discovery_plan()["ok"] is True
    assert package_discovery_plan()["side_effects"] == ()


def test_service_and_route_surface_are_executable():
    service = HotelRevenueManagementService()
    room = service.create_room_type(
        {
            "tenant": "tenant-test",
            "hotel_id": "hotel-test",
            "code": "DLX",
            "physical_rooms": 10,
            "maintenance_holdback": 1,
            "complimentary_allotment": 0,
            "capacity_adults": 2,
            "capacity_children": 1,
        }
    )
    rate = service.record_rate_plan(
        {
            "tenant": "tenant-test",
            "hotel_id": "hotel-test",
            "room_type_id": room["record"]["id"],
            "code": "BAR",
            "base_rate": 170.0,
            "currency": "USD",
            "member_fence": "public",
            "cancellation_policy": "24h-flex",
        }
    )
    route = dispatch_route(
        "GET /hotel-revenue-management-workbench",
        {"tenant": "tenant-test"},
        state=service.state,
    )
    assert service_operation_contracts()["ok"] is True
    assert api_route_contracts()["ok"] is True
    assert validate_api_route_contracts()["ok"] is True
    assert room["ok"] is True
    assert rate["ok"] is True
    assert route["ok"] is True
    assert route["result"]["metrics"]["room_types"] == 1


def test_configuration_permissions_and_seed_hooks_are_executable():
    assert governance_smoke_test()["ok"] is True


def test_event_handlers_are_idempotent_and_retryable():
    manifest = handler_manifest()
    assert manifest["ok"] is True
    assert dispatch_event({"event_type": ("PolicyChanged", "AuditEventSealed", "OperationalKpiChanged")[0], "idempotency_key": "idem-hotel-revenue-management"})["ok"] is True
    assert dispatch_event({"event_type": "Unexpected", "idempotency_key": "bad-hotel-revenue-management"})["dead_letter_table"].endswith("dead_letter_event")
