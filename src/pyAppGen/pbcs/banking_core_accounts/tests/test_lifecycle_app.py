from pyAppGen.pbcs.banking_core_accounts.runtime import (
    banking_core_accounts_build_app_surface,
    banking_core_accounts_build_workbench_view,
    banking_core_accounts_build_workflow_surface,
    banking_core_accounts_empty_state,
    banking_core_accounts_open_deposit_account,
    banking_core_accounts_query_account_detail,
    banking_core_accounts_query_workbench,
    banking_core_accounts_transition_deposit_account,
)
from pyAppGen.pbcs.banking_core_accounts.services import BankingCoreAccountsService


def test_deposit_account_lifecycle_valid_path_and_detail_query():
    state = banking_core_accounts_empty_state()
    opened = banking_core_accounts_open_deposit_account(
        state,
        {
            "tenant": "tenant-a",
            "account_id": "ACC-100",
            "account_number": "000100",
            "customer_id": "CUST-100",
            "product_code": "SAVINGS",
            "currency": "KES",
            "actor_id": "maker-1",
            "source_reference": "open-100",
        },
    )
    approved = banking_core_accounts_transition_deposit_account(
        opened["state"],
        {
            "account_id": "ACC-100",
            "target_state": "approved",
            "actor_id": "maker-1",
            "approver_id": "checker-1",
            "reason": "kyc_verified",
            "source_reference": "approve-100",
        },
    )
    activated = banking_core_accounts_transition_deposit_account(
        approved["state"],
        {
            "account_id": "ACC-100",
            "target_state": "active",
            "actor_id": "ops-1",
            "reason": "initial_funding_received",
            "source_reference": "activate-100",
        },
    )
    detail = banking_core_accounts_query_account_detail(activated["state"], "ACC-100")

    assert opened["ok"] is True
    assert approved["ok"] is True
    assert activated["ok"] is True
    assert detail["ok"] is True
    assert detail["account"]["lifecycle_state"] == "active"
    assert detail["account"]["allowed_next_states"] == ("restricted", "dormant", "closed")
    assert detail["account"]["transition_count"] == 3


def test_invalid_transition_and_maker_checker_controls_are_enforced():
    state = banking_core_accounts_empty_state()
    opened = banking_core_accounts_open_deposit_account(
        state,
        {
            "tenant": "tenant-a",
            "account_id": "ACC-200",
            "account_number": "000200",
            "customer_id": "CUST-200",
            "product_code": "CURRENT",
            "currency": "KES",
            "actor_id": "maker-1",
            "source_reference": "open-200",
        },
    )

    invalid = banking_core_accounts_transition_deposit_account(
        opened["state"],
        {
            "account_id": "ACC-200",
            "target_state": "active",
            "actor_id": "maker-1",
            "reason": "skip_approval_attempt",
            "source_reference": "invalid-200",
        },
    )
    self_approved = banking_core_accounts_transition_deposit_account(
        opened["state"],
        {
            "account_id": "ACC-200",
            "target_state": "approved",
            "actor_id": "maker-1",
            "approver_id": "maker-1",
            "reason": "self_approve_attempt",
            "source_reference": "self-approve-200",
        },
    )

    assert invalid["ok"] is False
    assert invalid["reason"] == "invalid_lifecycle_transition"
    assert self_approved["ok"] is False
    assert self_approved["reason"] == "maker_checker_violation"


def test_idempotent_opening_and_workbench_filters():
    state = banking_core_accounts_empty_state()
    payload = {
        "tenant": "tenant-b",
        "account_id": "ACC-300",
        "account_number": "000300",
        "customer_id": "CUST-300",
        "product_code": "SALARY",
        "currency": "KES",
        "actor_id": "maker-1",
        "source_reference": "open-300",
        "idempotency_key": "idem-open-300",
    }
    opened = banking_core_accounts_open_deposit_account(state, payload)
    duplicate = banking_core_accounts_open_deposit_account(opened["state"], payload)
    workbench = banking_core_accounts_query_workbench(
        opened["state"], {"tenant": "tenant-b", "lifecycle_state": "pending"}
    )

    assert opened["ok"] is True
    assert duplicate["ok"] is True
    assert duplicate["duplicate"] is True
    assert workbench["summary"]["total_accounts"] == 1
    assert workbench["summary"]["lifecycle_counts"] == (
        {"lifecycle_state": "pending", "count": 1},
    )


def test_single_pbc_app_surface_exposes_forms_wizards_controls_and_service_flow():
    service = BankingCoreAccountsService()
    opened = service.open_deposit_account(
        {
            "tenant": "tenant-c",
            "account_id": "ACC-400",
            "account_number": "000400",
            "customer_id": "CUST-400",
            "product_code": "YOUTH",
            "currency": "KES",
            "actor_id": "maker-1",
            "source_reference": "open-400",
        }
    )
    app_surface = banking_core_accounts_build_app_surface(service.state, tenant="tenant-c")
    workbench = banking_core_accounts_build_workbench_view(service.state, tenant="tenant-c")
    workflows = banking_core_accounts_build_workflow_surface(service.state, tenant="tenant-c")

    assert opened["ok"] is True
    assert app_surface["ok"] is True
    assert app_surface["single_pbc_app"] is True
    assert len(app_surface["forms"]) >= 2
    assert len(app_surface["wizards"]) >= 2
    assert len(app_surface["controls"]) >= 3
    assert len(app_surface["workflows"]) == 3
    assert workflows["ok"] is True
    assert workflows["workflow_state_coverage"][0]["visible_account_count"] == 1
    assert workbench["summary"]["total_accounts"] == 1
