from pyAppGen.pbcs.banking_core_accounts import account_control as ac
from pyAppGen.pbcs.banking_core_accounts import agent, routes, runtime, ui
from pyAppGen.pbcs.banking_core_accounts.release_evidence import release_readiness_manifest, validate_release_evidence
from pyAppGen.pbcs.banking_core_accounts.services import BankingCoreAccountsService


def test_account_control_primitives_cover_all_improve1_capabilities():
    results = [
        ac.evaluate_lifecycle_transition("pending", "approved", maker="maker", checker="checker", reason="kyc"),
        ac.build_customer_account_projection(
            "C-1",
            ({"customer_id": "C-1", "account_id": "A-1", "product_code": "SAV"},),
            ({"account_id": "A-1", "hold_id": "H-1", "status": "active", "amount": 15},),
            ({"account_id": "A-1", "case_id": "CASE-1", "status": "open"},),
            ({"account_id": "A-1", "statement_id": "ST-1"},),
        ),
        ac.resolve_product_parameter(
            {"rate": 0.02, "statement_cycle": "monthly"},
            ({"tenant": "t1", "product": "SAV", "parameter": "rate", "value": 0.03, "reason": "promo"},),
            {"tenant": "t1", "product": "SAV", "branch": "001"},
        ),
        ac.decompose_balance(1000, ({"amount": 125, "status": "active"},), uncleared=75, overdraft_limit=200, accrued_interest=2.5),
        ac.replay_value_dated_balance(
            ({"event_id": "2", "value_date": "2026-05-29", "amount": -50}, {"event_id": "1", "value_date": "2026-05-28", "amount": 500}),
            "2026-05-29",
        ),
        ac.rank_holds(({"hold_type": "fraud", "hold_id": "H2", "amount": 50, "blocks": ("debit",)}, {"hold_type": "legal", "hold_id": "H1", "amount": 100, "blocks": ("debit", "closure")})),
        ac.release_hold_waterfall(({"hold_type": "fraud", "hold_id": "H2", "amount": 50}, {"hold_type": "legal", "hold_id": "H1", "amount": 100}), 60),
        ac.evaluate_overdraft_status({"ledger": -120}, {"limit": 100, "grace_deadline": "2026-06-02"}),
        ac.plan_overdraft_reversal({"item_id": "FEE-1", "amount": 25}, {"bank_error": True}),
        ac.calculate_interest_accrual(2000, ({"minimum_balance": 0, "rate": 0.01}, {"minimum_balance": 1000, "rate": 0.03}), 30),
        ac.plan_interest_posting({"amount": 5.0}, {"interest_mode": "capitalize", "lifecycle_state": "active"}),
        ac.assess_fee_schedule("monthly_service", {"balance": 200}, ({"schedule_id": "FS-1", "trigger": "monthly_service", "max_balance": 500, "amount": 3, "rule_version": "v1"},)),
        ac.govern_fee_waiver({"amount": 75}, {"reason_code": "bank_error", "approved_by": "sup-1"}, ({"fee_id": "F1"},)),
        ac.evaluate_statement_cutover({"cycle_id": "CYC-1"}, ({"item_type": "posting", "status": "pending"},)),
        ac.prove_statement_balance_forward(100, ({"amount": 25}, {"amount": -10}), 115),
        ac.evaluate_mandate(({"signatory_id": "S1", "status": "active"}, {"signatory_id": "S2", "status": "active"}), {"signed_by": ("S1", "S2"), "signing_rule": "two"}),
        ac.schedule_mandate_change({}, {"effective_date": "2026-05-01", "approved": True}, as_of="2026-05-30"),
        ac.evaluate_compliance_restriction({"blocked_capabilities": ("debit",), "source": "sanctions"}, "credit"),
        ac.open_compliance_case("A-1", "source_of_funds", ("kyc_doc",)),
        ac.evaluate_dormancy({"opened_date": "2025-01-01"}, ({"activity_date": "2025-05-01"},), 365, as_of="2026-05-30"),
        ac.evaluate_closure_checklist({}, {"ledger": 0}, (), ({"status": "generated"},)),
        ac.evaluate_reopening({"account_id": "A-1", "lifecycle_state": "closed"}, "erroneous_closure"),
        ac.evaluate_linked_account_relationship({}, {"permissions": ("sweep",), "status": "active"}, "sweep"),
        ac.reconcile_subledger_balances(({"account_id": "A-1", "ledger": 100},), ({"account_id": "A-1", "amount": 100},)),
        ac.classify_posting_boundary({"posting_boundary": "backdated_correction"}),
        ac.build_typed_event_catalog(),
        ac.evaluate_idempotent_command("open", {"idempotency_key": "IDEM-1"}, ("IDEM-0",)),
        ac.build_dead_letter_recovery_view(({"account_id": "A-1", "poison": False},)),
        ac.build_operational_query_api_contract(),
        ac.build_role_workbench("supervisor", ({"account_id": "A-1"},)),
        ac.build_account_timeline(({"event_id": "E2", "effective_at": "2026-05-02"}, {"event_id": "E1", "effective_at": "2026-05-01"})),
        ac.plan_assistant_servicing_instruction("waive the duplicate fee", {"account_id": "A-1"}),
        ac.explain_statement_fee("why was I charged?", {"fee_assessment": {"amount": 3}, "statement_cycle": {"id": "S1"}}),
        ac.age_exception_cases(({"case_id": "C1", "opened_date": "2026-05-20", "severity": "medium"},), as_of="2026-05-30"),
        ac.evaluate_policy_rule_version({"rule_id": "R1", "effective_from": "2026-01-01", "approval_evidence": "APP-1"}, as_of="2026-05-30"),
        ac.detect_parameter_drift(({"name": "rate", "value": 0.03, "scope": "product"},), {"rate": 0.02}),
        ac.evaluate_control_assertions(({"action_id": "ACT-1", "maker": "u1", "checker": "u2", "materiality": 2000, "second_checker": "u3"},)),
        ac.build_core_banking_release_pack({key: True for key in ("lifecycle", "balance_components", "holds", "overdraft", "interest", "fees", "statements", "mandates", "compliance", "reconciliation", "control_assertions")}),
        ac.enforce_tenant_jurisdiction({"tenant": "t1", "jurisdiction": "KE"}, {"tenant": "t1", "jurisdiction": "KE"}),
        ac.validate_schema_extension({"field_name": "student_id", "owner": "product", "validation_rule": "required", "display_rule": "masked", "migration_plan": "online", "table": "banking_core_accounts_deposit_account"}),
        ac.compute_product_branch_analytics(({"account_id": "A-1", "product_code": "SAV", "branch": "001", "ledger": 300, "active_holds": True, "fee_waiver_count": 1},)),
        ac.seal_account_evidence({"account_id": "A-1", "event_id": "E1"}),
        ac.simulate_policy_change({"type": "interest_rate"}, ({"account_id": "A-1", "ledger": 300},)),
        ac.detect_balance_fee_anomalies(({"account_id": "A-1", "fee_burst": True},)),
        ac.normalize_account_identifier({"account_number": "1234567890", "alias": "rent"}, "customer_service"),
        ac.evaluate_negative_balance_handoff({"ledger": -10, "negative_days": 31, "handoff_threshold_days": 30}),
        ac.adjust_for_operational_calendar("2026-05-31", {"holidays": ("2026-06-01",)}),
        ac.plan_correction_restatement({"balance": 100}, {"balance": 90, "reason_code": "posting_error", "approved_by": "checker", "customer_impact_note": "refund"}),
        ac.build_event_api_boundary_map(),
        ac.build_structural_release_gate({key: True for key in ("lifecycle", "balances", "holds", "overdraft", "interest", "fees", "statements", "mandates", "compliance", "reconciliation", "assistant", "workbench", "evidence_sealing")}),
    ]

    assert len(ac.ACCOUNT_CONTROL_CAPABILITIES) == 50
    assert len(results) == 50
    assert all(result["ok"] is True for result in results)
    assert {result["capability"] for result in results} == set(ac.ACCOUNT_CONTROL_CAPABILITIES)
    assert results[3]["components"]["available"] == 800.0
    assert results[14]["proof_passed"] is True
    assert results[25]["events"][0] == "DepositAccountOpened"
    assert results[41]["verified"] is True
    assert results[48]["rejects_undeclared_coupling"] is True
    assert results[49]["release_ready"] is True


def test_banking_runtime_ui_agent_and_boundaries_surface_account_controls():
    service = BankingCoreAccountsService()
    opened = service.open_deposit_account(
        {
            "tenant": "tenant-a",
            "account_id": "ACC-900",
            "account_number": "000900",
            "customer_id": "CUST-900",
            "product_code": "SAVINGS",
            "currency": "KES",
            "actor_id": "maker-1",
            "source_reference": "open-900",
        }
    )
    workbench = service.build_workbench_view({"tenant": "tenant-a"})
    ui_contract = ui.banking_core_accounts_ui_contract()
    release = runtime.banking_core_accounts_build_release_evidence()
    route = routes.dispatch_route("POST /deposit-accounts", {"account_id": "ACC-901"})
    assistant = agent.document_instruction_plan("bank letter", "waive the monthly fee after bank error", action="update")
    forbidden = agent.datastore_crud_plan("update", table="customer_master_table")
    boundary = runtime.banking_core_accounts_verify_owned_table_boundary(("banking_core_accounts_deposit_account", "customer_master_table"))

    assert opened["ok"] is True
    assert workbench["ok"] is True
    assert route["ok"] is True
    assert assistant["ok"] is True
    assert forbidden["ok"] is False
    assert boundary["ok"] is False
    assert runtime.BANKING_CORE_ACCOUNTS_ALLOWED_DATABASE_BACKENDS == ("postgresql", "mysql", "mariadb")
    assert ui_contract["stream_engine_picker_visible"] is False
    assert len(ui_contract["full_capability_surface"]["account_control_panels"]) == 50
    assert release["generated_artifacts"]["improve1_account_control"]["capability_count"] == 50
    assert any(check["id"] == "improve1_account_control" and check["ok"] for check in release["checks"])


def test_banking_release_readiness_and_runtime_smoke_include_account_control_evidence():
    readiness = release_readiness_manifest()
    validation = validate_release_evidence()
    smoke = runtime.banking_core_accounts_runtime_smoke()
    capabilities = runtime.banking_core_accounts_runtime_capabilities()
    contract = ac.improve1_account_control_contract()

    assert readiness["ok"] is True
    assert validation["ok"] is True
    assert smoke["ok"] is True
    assert capabilities["ok"] is True
    assert contract["capability_count"] == 50
    assert contract["shared_table_access"] is False
    assert contract["stream_engine_picker_visible"] is False
