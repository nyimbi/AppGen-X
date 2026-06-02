"""Domain behavior checks for expense_management improve1 controls."""

from pyAppGen.pbcs.expense_management.expense_control import (
    EXPENSE_CONTROL_ALLOWED_DATABASE_BACKENDS,
    EXPENSE_CONTROL_DECLARED_DEPENDENCIES,
    EXPENSE_CONTROL_OWNED_TABLES,
    EXPENSE_CONTROL_REQUIRED_EVENT_TOPIC,
    evaluate_expense_control,
    improve1_expense_control_contract,
)
from pyAppGen.pbcs.expense_management.release_evidence import build_release_evidence, validate_release_evidence
from pyAppGen.pbcs.expense_management.runtime import (
    expense_management_build_release_evidence,
    expense_management_runtime_capabilities,
    expense_management_runtime_smoke,
)
from pyAppGen.pbcs.expense_management.ui import expense_management_ui_contract


def test_all_improve1_controls_have_executable_expense_evidence():
    contract = improve1_expense_control_contract()
    assert contract["ok"] is True
    assert contract["capability_count"] == 50
    assert contract["allowed_database_backends"] == EXPENSE_CONTROL_ALLOWED_DATABASE_BACKENDS == ("postgresql", "mysql", "mariadb")
    assert contract["event_contract"] == "AppGen-X"
    assert contract["required_event_topic"] == EXPENSE_CONTROL_REQUIRED_EVENT_TOPIC
    assert contract["stream_engine_picker_visible"] is False
    for capability in contract["capabilities"]:
        evidence = capability["evidence"]
        assert capability["ok"] is True
        assert evidence["owned_tables"]
        assert all(table in EXPENSE_CONTROL_OWNED_TABLES for table in evidence["owned_tables"])
        assert evidence["required_fields"]
        assert evidence["ui_surface"]
        assert evidence["service_api"]
        assert evidence["test"] == "tests/test_domain_behavior.py"
        assert all(dependency in EXPENSE_CONTROL_DECLARED_DEPENDENCIES for dependency in evidence["declared_dependencies"])
        assert evidence["event_contract"] == "AppGen-X"
        assert evidence["side_effects"] == ()


def test_expense_control_contract_is_visible_in_runtime_release_and_ui_surfaces():
    runtime = expense_management_runtime_capabilities()
    runtime_release = expense_management_build_release_evidence()
    smoke = expense_management_runtime_smoke()
    release = build_release_evidence()
    ui = expense_management_ui_contract()
    assert runtime["ok"] is True
    assert runtime["expense_control"]["ok"] is True
    assert "improve1_expense_control_contract" in runtime["operations"]
    assert len(runtime["improve1_expense_control_capabilities"]) == 50
    assert runtime_release["expense_control"]["ok"] is True
    assert release["expense_control"]["ok"] is True
    assert validate_release_evidence()["ok"] is True
    assert smoke["ok"] is True
    assert ui["expense_control_contract"]["ok"] is True
    assert len(ui["full_capability_surface"]["expense_control_panels"]) == 50


def test_readiness_lifecycle_policy_reimbursement_and_payment_controls_are_gated():
    assert evaluate_expense_control(1, {"line_completeness": "incomplete"})["ok"] is False
    assert evaluate_expense_control(2, {"reimbursement_effect": "scheduled_before_approval"})["ok"] is False
    assert evaluate_expense_control(5, {"integrity_check": "failed"})["ok"] is False
    assert evaluate_expense_control(6, {"field_confidence": 0.4, "confirmation_required": False})["ok"] is False
    assert evaluate_expense_control(8, {"feed_idempotency_key": ""})["ok"] is False
    assert evaluate_expense_control(10, {"compiled_hash": ""})["ok"] is False
    assert evaluate_expense_control(16, {"submitter": "employee-1", "approver": "employee-1"})["ok"] is False
    assert evaluate_expense_control(18, {"approval_status": "submitted"})["ok"] is False
    assert evaluate_expense_control(19, {"failure_classification": "unclassified"})["ok"] is False


def test_specialist_expense_controls_block_domain_edge_cases():
    assert evaluate_expense_control(20, {"advance_state": "open", "issued_amount": 500, "applied_amounts": 100})["ok"] is False
    assert evaluate_expense_control(21, {"commute_deduction": -5})["ok"] is False
    assert evaluate_expense_control(22, {"deduction_explanation": ""})["ok"] is False
    assert evaluate_expense_control(23, {"per_person_spend": 150, "attendees": ()})["ok"] is False
    assert evaluate_expense_control(26, {"reviewer_disposition": ""})["ok"] is False
    assert evaluate_expense_control(29, {"audit_decision": "undecided"})["ok"] is False
    assert evaluate_expense_control(34, {"percentage_total": 99})["ok"] is False
    assert evaluate_expense_control(35, {"rounding_delta": 2})["ok"] is False
    assert evaluate_expense_control(39, {"missing_receipt_assertion": "failed"})["ok"] is False


def test_agent_event_boundary_resilience_and_release_controls_are_enforced():
    assert evaluate_expense_control(42, {"hash_chain": ()})["ok"] is False
    assert evaluate_expense_control(43, {"duplicate_card_post_test": "failed"})["ok"] is False
    assert evaluate_expense_control(44, {"foreign_table_access": ("hr_employee",)})["ok"] is False
    assert evaluate_expense_control(45, {"human_confirmation": False})["ok"] is False
    assert evaluate_expense_control(46, {"no_auto_approve": False})["ok"] is False
    assert evaluate_expense_control(48, {"dead_letter_recovery_drill": "failed"})["ok"] is False
    assert evaluate_expense_control(49, {"blocking_gaps": ("card feed degraded",)})["ok"] is False
    assert evaluate_expense_control(50, {"payment_reconciliation": "missing"})["ok"] is False
    assert evaluate_expense_control(50)["ok"] is True
