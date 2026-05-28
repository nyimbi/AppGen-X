from datetime import date, timedelta

from pyAppGen.pbcs.construction_contracts_commercials import (
    construction_contracts_commercials_build_api_contract,
    construction_contracts_commercials_build_release_evidence,
    construction_contracts_commercials_build_schema_contract,
    construction_contracts_commercials_empty_state,
    construction_contracts_commercials_progress_contract_lifecycle,
    implementation_contract,
    package_discovery_plan,
    package_metadata_manifest,
    validate_package_metadata,
)
from pyAppGen.pbcs.construction_contracts_commercials.agent import (
    agent_skill_manifest,
    chatbot_interface_contract,
    datastore_crud_plan,
    document_instruction_plan,
)
from pyAppGen.pbcs.construction_contracts_commercials.config import governance_smoke_test
from pyAppGen.pbcs.construction_contracts_commercials.core import (
    CONSTRUCTION_CONTRACTS_COMMERCIALS_EMITTED_EVENT_TYPES,
    construction_contracts_commercials_build_workbench_view,
)
from pyAppGen.pbcs.construction_contracts_commercials.events import event_contract_manifest, validate_event_contract
from pyAppGen.pbcs.construction_contracts_commercials.handlers import dispatch_event, handler_manifest
from pyAppGen.pbcs.construction_contracts_commercials.release_evidence import (
    release_readiness_manifest,
    validate_release_evidence,
)
from pyAppGen.pbcs.construction_contracts_commercials.routes import api_route_contracts, dispatch_route, validate_api_route_contracts
from pyAppGen.pbcs.construction_contracts_commercials.services import ConstructionContractsCommercialsService, service_operation_contracts


def _contract_payload():
    return {
        "tenant": "tenant-a",
        "contract_code": "CCC-001",
        "title": "Commercial Tower Envelope",
        "contract_value": 100000.0,
        "pricing_basis": "lump_sum",
        "jurisdiction": "KE",
        "schedule_of_values": (
            {"line_code": "SOV-01", "work_package": "Envelope", "original_value": 60000.0},
            {"line_code": "SOV-02", "work_package": "Fitout", "original_value": 40000.0},
        ),
        "guarantees": (
            {"type": "performance_bond", "expiry": (date.today() + timedelta(days=14)).isoformat()},
        ),
    }


def _service_with_contract():
    service = ConstructionContractsCommercialsService()
    created = service.command_construction_contract(_contract_payload())
    assert created["ok"] is True
    return service, created["record"]


def test_generated_schema_service_and_release_evidence():
    schema = construction_contracts_commercials_build_schema_contract()
    release = construction_contracts_commercials_build_release_evidence()
    assert schema["ok"] is True
    assert construction_contracts_commercials_build_api_contract()["ok"] is True
    assert release["ok"] is True
    assert "commercial_lifecycle_controls" in {check["id"] for check in release["checks"]}
    assert release_readiness_manifest()["ok"] is True
    assert validate_release_evidence()["ok"] is True


def test_manifest_and_event_contract():
    assert implementation_contract()["pbc"] == "construction_contracts_commercials"
    assert event_contract_manifest()["ok"] is True
    assert validate_event_contract()["ok"] is True


def test_invalid_contract_lifecycle_transition_is_rejected():
    service, contract = _service_with_contract()
    result = service.progress_contract_lifecycle({"contract_id": contract["id"], "next_stage": "closed"})
    assert result["ok"] is False
    assert result["reason"] == "invalid_transition"


def test_pay_application_overclaim_is_rejected():
    service, _contract = _service_with_contract()
    result = service.record_pay_application(
        {
            "contract_code": "CCC-001",
            "application_number": "APP-OVER",
            "period_start": date.today().replace(day=1).isoformat(),
            "period_end": date.today().isoformat(),
            "attachments": ("claim.pdf",),
            "lines": (
                {"line_code": "SOV-01", "current_claimed": 70000.0, "evidence_refs": ("site-walk",)},
            ),
        }
    )
    assert result["ok"] is False
    assert result["reason"] == "overclaimed_schedule_line"


def test_certification_requires_valid_waiver_then_succeeds():
    service, _contract = _service_with_contract()
    pay_app = service.record_pay_application(
        {
            "contract_code": "CCC-001",
            "application_number": "APP-001",
            "period_start": date.today().replace(day=1).isoformat(),
            "period_end": date.today().isoformat(),
            "attachments": ("payapp.pdf", "photos.zip"),
            "lines": (
                {"line_code": "SOV-01", "current_claimed": 25000.0, "evidence_refs": ("inspection-001",)},
            ),
        }
    )
    blocked = service.certify_pay_application({"pay_application_id": pay_app["record"]["id"]})
    assert blocked["ok"] is False
    assert blocked["reason"] == "missing_valid_waiver"

    waiver = service.create_lien_waiver(
        {
            "contract_code": "CCC-001",
            "pay_application_id": pay_app["record"]["id"],
            "waiver_number": "LW-001",
            "covered_amount": 25000.0,
            "signed_date": date.today().isoformat(),
        }
    )
    certified = service.certify_pay_application({"pay_application_id": pay_app["record"]["id"]})
    assert waiver["ok"] is True
    assert certified["ok"] is True
    assert certified["record"]["intake_status"] == "certified"
    assert certified["record"]["certified_amount"] == 22500.0


def test_variation_only_changes_contract_value_when_approved():
    service, contract = _service_with_contract()
    pending = service.approve_variation_order(
        {
            "contract_code": "CCC-001",
            "variation_number": "VO-PEND",
            "event_date": date.today().isoformat(),
            "notice_date": date.today().isoformat(),
            "quoted_amount": 10000.0,
            "approved": False,
        }
    )
    approved = service.approve_variation_order(
        {
            "contract_code": "CCC-001",
            "variation_number": "VO-APP",
            "event_date": date.today().isoformat(),
            "notice_date": date.today().isoformat(),
            "quoted_amount": 12000.0,
            "approved_amount": 8000.0,
            "approved": True,
        }
    )
    contract_after = service.state["tables"]["construction_contracts_commercials_construction_contract"][contract["id"]]
    assert pending["ok"] is True
    assert approved["ok"] is True
    assert contract_after["approved_change_value"] == 8000.0
    assert contract_after["current_contract_value"] == 108000.0


def test_claim_timeliness_and_workbench_queues_are_domain_specific():
    service, _contract = _service_with_contract()
    pay_app = service.record_pay_application(
        {
            "contract_code": "CCC-001",
            "application_number": "APP-MISS",
            "period_start": date.today().replace(day=1).isoformat(),
            "period_end": date.today().isoformat(),
            "attachments": ("payapp.pdf",),
            "lines": (
                {"line_code": "SOV-01", "current_claimed": 10000.0, "evidence_refs": ("inspection-001",)},
            ),
        }
    )
    claim = service.register_commercial_claim(
        {
            "contract_code": "CCC-001",
            "claim_number": "CL-001",
            "claim_type": "delay",
            "event_date": date.today().isoformat(),
            "notice_date": (date.today() + timedelta(days=20)).isoformat(),
            "claimed_amount": 14000.0,
        }
    )
    workbench = construction_contracts_commercials_build_workbench_view(state=service.state, tenant="tenant-a")
    assert pay_app["ok"] is True
    assert claim["ok"] is True
    assert claim["record"]["time_bar_status"] == "late"
    assert workbench["queues"]["missing_waivers"][0]["id"] == pay_app["record"]["id"]
    assert workbench["queues"]["active_claims"][0]["id"] == claim["record"]["id"]
    assert workbench["queues"]["expiring_guarantees"]


def test_agent_chatbot_and_crud_previews_require_governance():
    document_plan = document_instruction_plan("Pay application amount 25,000", "create pay application preview")
    allowed = datastore_crud_plan("create", payload={"contract_code": "CCC-001"})
    blocked = datastore_crud_plan("update", table="foreign_table", payload={"id": "x"})
    assert agent_skill_manifest()["ok"] is True
    assert chatbot_interface_contract()["ok"] is True
    assert document_plan["ok"] is True
    assert document_plan["requires_human_confirmation"] is True
    assert document_plan["requires_citations"] is True
    assert allowed["ok"] is True
    assert blocked["ok"] is False


def test_registration_plan_is_side_effect_free():
    assert package_metadata_manifest()["pbc"] == "construction_contracts_commercials"
    assert validate_package_metadata()["ok"] is True
    assert package_discovery_plan()["ok"] is True
    assert package_discovery_plan()["side_effects"] == ()


def test_service_and_route_surface_are_executable():
    service = ConstructionContractsCommercialsService()
    create = dispatch_route("POST /construction-contracts", _contract_payload(), service=service)
    workbench = dispatch_route("GET /construction-contracts-commercials-workbench", {"tenant": "tenant-a"}, service=service)
    assert api_route_contracts()["ok"] is True
    assert validate_api_route_contracts()["ok"] is True
    assert create["ok"] is True
    assert workbench["ok"] is True
    assert service_operation_contracts()["ok"] is True
    assert handler_manifest()["ok"] is True
    assert dispatch_event({"event_type": "PolicyChanged", "idempotency_key": "idem-1"})["ok"] is True
    assert dispatch_event({"event_type": "Unexpected", "idempotency_key": "idem-2"})["dead_letter_table"].endswith("dead_letter_event")


def test_configuration_permissions_and_seed_hooks_are_executable():
    assert governance_smoke_test()["ok"] is True
    assert construction_contracts_commercials_empty_state()["configuration"]["event_topic"]
    assert CONSTRUCTION_CONTRACTS_COMMERCIALS_EMITTED_EVENT_TYPES[0] == "ConstructionContractsCommercialsCreated"


def test_event_handlers_are_idempotent_and_retryable():
    manifest = handler_manifest()
    first = dispatch_event({"event_type": "PolicyChanged", "idempotency_key": "idem-audit-1"})
    duplicate = dispatch_event({"event_type": "PolicyChanged", "idempotency_key": "idem-audit-1"})
    failed = dispatch_event({"event_type": "Unexpected", "idempotency_key": "idem-audit-2"})
    assert manifest["ok"] is True
    assert first["ok"] is True
    assert duplicate["duplicate"] is True
    assert failed["dead_letter_table"].endswith("dead_letter_event")
