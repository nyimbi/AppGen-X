from pyAppGen.pbcs.court_case_management.agent import document_instruction_plan
from pyAppGen.pbcs.court_case_management.court_operations_app import (
    add_docket_entry,
    add_party,
    controls_contract,
    court_operations_smoke_test,
    court_workbench,
    create_court_case,
    cure_filing,
    draft_order,
    empty_court_state,
    forms_contract,
    receive_filing,
    schedule_hearing,
    sign_and_enter_order,
    single_pbc_app_contract,
    wizards_contract,
)
from pyAppGen.pbcs.court_case_management.routes import dispatch_route
from pyAppGen.pbcs.court_case_management.services import CourtCaseManagementService
from pyAppGen.pbcs.court_case_management.ui import court_case_management_ui_contract


def _case_payload(**overrides):
    payload = {
        "court": "CIV",
        "division": "LAW",
        "filing_year": 2026,
        "case_type": "civil",
        "caption": "Roe v. Example",
        "assigned_judge": "Judge Lane",
    }
    payload.update(overrides)
    return payload


def test_case_numbering_is_unique_and_preserves_venue():
    created = create_court_case(empty_court_state(), _case_payload())
    assert created["ok"] is True
    assert created["court_case"]["case_number"] == "CIV-LAW-2026-000001"
    duplicate = create_court_case(created["state"], _case_payload(sequence=1))
    assert duplicate["ok"] is False
    assert duplicate["reason"] == "duplicate_case_number"


def test_party_representation_and_filing_deficiency_flow_create_docket_entry_after_cure():
    created = create_court_case(empty_court_state(), _case_payload())
    party = add_party(
        created["state"],
        {
            "case_id": created["court_case"]["id"],
            "party_name": "Jane Roe",
            "role": "plaintiff",
            "lead_counsel": "A. Counsel",
            "service_addresses": ("100 Main",),
        },
    )
    assert party["party"]["self_represented"] is False
    filing = receive_filing(
        party["state"],
        {
            "case_id": created["court_case"]["id"],
            "filing_type": "motion",
            "document_title": "Motion to Compel",
            "received_at": "2026-01-02",
            "deficiency_codes": ("missing_signature",),
            "cure_deadline": "2026-01-09",
        },
    )
    assert filing["filing"]["state"] == "deficient"
    cured = cure_filing(filing["state"], filing["filing"]["id"], {"defects_cured": True, "evidence": "signed"})
    assert cured["filing"]["state"] == "accepted"
    assert len(cured["state"]["docket_entries"]) == 1


def test_docket_sequence_and_hearing_calendar_controls_block_bad_operations():
    created = create_court_case(empty_court_state(), _case_payload())
    bad_sequence = add_docket_entry(created["state"], {"case_id": created["court_case"]["id"], "sequence": 3, "entry_text": "bad"})
    assert bad_sequence["ok"] is False
    assert bad_sequence["reason"] == "docket_sequence_gap"

    hearing = schedule_hearing(
        created["state"],
        {
            "case_id": created["court_case"]["id"],
            "hearing_type": "motion",
            "scheduled_at": "2026-01-20T09:00:00",
            "courtroom": "4A",
            "session_block": "AM",
            "assigned_judge": "Judge Lane",
        },
    )
    assert hearing["ok"] is True
    conflict = schedule_hearing(
        hearing["state"],
        {
            "case_id": created["court_case"]["id"],
            "hearing_type": "status",
            "scheduled_at": "2026-01-20T09:00:00",
            "courtroom": "4A",
            "session_block": "AM",
            "assigned_judge": "Judge Lane",
        },
    )
    assert conflict["ok"] is False
    assert conflict["reason"] == "courtroom_double_booked"


def test_order_entry_requires_signature_and_dockets_entered_order():
    created = create_court_case(empty_court_state(), _case_payload())
    order = draft_order(created["state"], {"case_id": created["court_case"]["id"], "title": "Scheduling Order", "draft_text": "Set deadlines."})
    blocked = sign_and_enter_order(order["state"], order["court_order"]["id"], {"signed_at": "2026-01-03"})
    assert blocked["ok"] is False
    assert blocked["reason"] == "signature_required"
    entered = sign_and_enter_order(order["state"], order["court_order"]["id"], {"judge_signature": "Judge Lane", "signed_at": "2026-01-03"})
    assert entered["ok"] is True
    assert entered["court_order"]["state"] == "entered"
    assert entered["docket_entry"]["source_type"] == "court_order"


def test_single_pbc_app_services_routes_ui_and_agent_are_executable():
    app = single_pbc_app_contract()
    assert app["ok"] is True
    assert app["database_backed"] is True
    assert len(app["forms"]) >= 5
    assert len(app["wizards"]) >= 4
    assert len(app["controls"]) >= 6

    service = CourtCaseManagementService()
    created = service.create_court_case(_case_payload())
    assert created["ok"] is True
    assert service.query_workbench({})["queue_counts"]["open_cases"] == 1
    assert dispatch_route("POST /court-cases", _case_payload())["operation"] == "create_court_case"
    assert court_case_management_ui_contract()["single_pbc_app"]["single_pbc_app"] is True
    assert document_instruction_plan("Motion packet", "triage filing")["domain_plan"]["proposed_action"] == "receive_filing"


def test_release_smoke_contracts_are_green():
    assert forms_contract()["ok"] is True
    assert wizards_contract()["ok"] is True
    assert controls_contract()["ok"] is True
    assert court_operations_smoke_test()["ok"] is True
    assert court_workbench(court_operations_smoke_test()["state"])["ok"] is True
