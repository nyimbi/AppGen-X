from pyAppGen.pbcs.claims_adjudication_healthcare.agent import document_instruction_crud_support
from pyAppGen.pbcs.claims_adjudication_healthcare.routes import dispatch_route
from pyAppGen.pbcs.claims_adjudication_healthcare.runtime import claims_adjudication_healthcare_approve_benefit_rule
from pyAppGen.pbcs.claims_adjudication_healthcare.runtime import claims_adjudication_healthcare_command_health_claim
from pyAppGen.pbcs.claims_adjudication_healthcare.runtime import claims_adjudication_healthcare_create_appeal
from pyAppGen.pbcs.claims_adjudication_healthcare.runtime import claims_adjudication_healthcare_empty_state
from pyAppGen.pbcs.claims_adjudication_healthcare.runtime import claims_adjudication_healthcare_query_workbench
from pyAppGen.pbcs.claims_adjudication_healthcare.runtime import claims_adjudication_healthcare_record_claim_line
from pyAppGen.pbcs.claims_adjudication_healthcare.runtime import claims_adjudication_healthcare_simulate_denial
from pyAppGen.pbcs.claims_adjudication_healthcare.services import ClaimsAdjudicationHealthcareService


def _state_with_benefit_rule():
    state = claims_adjudication_healthcare_empty_state()
    result = claims_adjudication_healthcare_approve_benefit_rule(
        state,
        {
            "tenant": "payer-a",
            "plan_id": "commercial-a",
            "service_code": "99213",
            "description": "Office visit",
            "covered": True,
            "auth_required": False,
            "allowed_percentage": 0.8,
            "copay_amount": 25,
            "deductible_apply": True,
            "max_units": 4,
            "effective_from": "2026-01-01",
            "effective_to": "2026-12-31",
        },
    )
    return result["state"]


def test_paid_claim_line_updates_workbench_metrics():
    state = _state_with_benefit_rule()
    claim = claims_adjudication_healthcare_command_health_claim(
        state,
        {
            "tenant": "payer-a",
            "claim_number": "HC-2001",
            "member_id": "MEM-1",
            "provider_id": "PRV-1",
            "plan_id": "commercial-a",
            "received_date": "2026-05-29",
            "total_charge": 300,
            "eligibility_projection_hours": 2,
            "provider_projection_hours": 2,
        },
    )
    line = claims_adjudication_healthcare_record_claim_line(
        claim["state"],
        {
            "claim_id": claim["claim"]["claim_id"],
            "line_number": 1,
            "service_date": "2026-05-28",
            "procedure_code": "99213",
            "diagnosis_code": "J10.1",
            "place_of_service": "11",
            "units": 1,
            "charge_amount": 300,
            "accumulator_remaining": 50,
        },
    )
    workbench = claims_adjudication_healthcare_query_workbench(line["state"], {"tenant": "payer-a"})

    assert line["claim_line"]["status"] == "paid"
    assert line["claim_line"]["allowed_amount"] == 240.0
    assert workbench["metrics"]["claim_count"] == 1
    assert workbench["metrics"]["line_count"] == 1
    assert workbench["metrics"]["denial_count"] == 0


def test_stale_projection_pends_claim_and_replay_is_duplicate():
    state = _state_with_benefit_rule()
    payload = {
        "tenant": "payer-a",
        "claim_number": "HC-2002",
        "member_id": "MEM-2",
        "provider_id": "PRV-2",
        "plan_id": "commercial-a",
        "received_date": "2026-05-29",
        "total_charge": 100,
        "eligibility_projection_hours": 30,
        "provider_projection_hours": 10,
    }
    created = claims_adjudication_healthcare_command_health_claim(state, payload)
    replay = claims_adjudication_healthcare_command_health_claim(created["state"], payload)

    assert created["claim"]["status"] == "pended"
    assert created["claim"]["pend_reason"] == "stale_projection"
    assert replay["duplicate"] is True
    assert replay["claim"]["claim_id"] == created["claim"]["claim_id"]


def test_denial_and_appeal_overturn_flow():
    state = claims_adjudication_healthcare_approve_benefit_rule(
        claims_adjudication_healthcare_empty_state(),
        {
            "tenant": "payer-a",
            "plan_id": "commercial-a",
            "service_code": "73721",
            "description": "MRI",
            "covered": True,
            "auth_required": True,
            "allowed_percentage": 0.75,
            "copay_amount": 50,
            "deductible_apply": True,
            "max_units": 1,
            "effective_from": "2026-01-01",
            "effective_to": "2026-12-31",
        },
    )["state"]
    claim = claims_adjudication_healthcare_command_health_claim(
        state,
        {
            "tenant": "payer-a",
            "claim_number": "HC-2003",
            "member_id": "MEM-3",
            "provider_id": "PRV-3",
            "plan_id": "commercial-a",
            "received_date": "2026-05-29",
        },
    )
    line = claims_adjudication_healthcare_record_claim_line(
        claim["state"],
        {
            "claim_id": claim["claim"]["claim_id"],
            "line_number": 1,
            "service_date": "2026-05-28",
            "procedure_code": "73721",
            "diagnosis_code": "M25.561",
            "place_of_service": "22",
            "units": 1,
            "charge_amount": 1200,
        },
    )
    denial = claims_adjudication_healthcare_simulate_denial(
        line["state"],
        {
            "claim_id": claim["claim"]["claim_id"],
            "line_ids": (line["claim_line"]["line_id"],),
            "denial_code": "AUTH-001",
            "rationale": "Authorization missing",
            "policy_rule_id": "auth-rule",
        },
    )
    appeal = claims_adjudication_healthcare_create_appeal(
        denial["state"],
        {
            "denial_id": denial["denial"]["denial_id"],
            "level": "first_level",
            "requester": "provider",
            "evidence_summary": "Authorization located after initial denial.",
            "determination": "overturned",
        },
    )

    assert line["claim_line"]["status"] == "denied"
    assert denial["denial"]["denial_code"] == "AUTH-001"
    assert appeal["appeal"]["determination"] == "overturned"
    assert appeal["state"]["claims"][claim["claim"]["claim_id"]]["status"] == "adjudicated"


def test_route_dispatch_and_document_instruction_support():
    service = ClaimsAdjudicationHealthcareService()
    service.approve_benefit_rule(
        {
            "tenant": "payer-a",
            "plan_id": "commercial-a",
            "service_code": "99213",
            "description": "Office visit",
            "effective_from": "2026-01-01",
            "effective_to": "2026-12-31",
        }
    )
    create = dispatch_route(
        "POST /health-claims",
        {
            "tenant": "payer-a",
            "claim_number": "HC-2004",
            "member_id": "MEM-4",
            "provider_id": "PRV-4",
            "plan_id": "commercial-a",
            "received_date": "2026-05-29",
        },
        service=service,
    )
    instruction = document_instruction_crud_support(
        "coverage memo",
        "Create a benefit rule for procedure 99213 and update the copay threshold.",
    )

    assert create["ok"] is True
    assert create["result"]["claim"]["claim_number"] == "HC-2004"
    assert instruction["document_plan"]["target_table"].endswith("benefit_rule")
    assert instruction["crud_plan"]["action"] in {"create", "update"}
