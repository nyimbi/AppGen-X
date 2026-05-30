from pyAppGen.pbcs.capital_markets_trading_ops import routes, runtime, ui
from pyAppGen.pbcs.capital_markets_trading_ops import trading_control as tc
from pyAppGen.pbcs.capital_markets_trading_ops.release_evidence import release_readiness_manifest, validate_release_evidence
from pyAppGen.pbcs.capital_markets_trading_ops.services import CapitalMarketsTradingOpsService


def test_trading_control_primitives_cover_all_improve1_capabilities():
    order = {
        "order_id": "ORD-1",
        "instrument_id": "IBM",
        "product_type": "equity",
        "trading_account": "ACC-1",
        "account": "ACC-1",
        "desk": "EQD",
        "trader": "alice",
        "book": "EQ-BOOK",
        "broker": "Broker-A",
        "venue": "XNYS",
        "settlement_model": "DVP",
        "regulatory_classification": "REG-S",
        "quantity": 100,
        "notional": 1000,
        "maker": "u1",
        "checker": "u2",
        "market": "US",
        "trade_date": "2026-05-29",
    }
    results = [
        tc.evaluate_order_lifecycle("validated", "risk_passed", "u1", "u2"),
        tc.build_cancel_replace_lineage(({"order_id": "O1", "version": 1}, {"order_id": "O2", "version": 2, "replaces": "O1", "changed_fields": ("quantity",)})),
        tc.validate_reference_data(order),
        tc.evaluate_pre_trade_risk(order, {"notional_limit": 5000, "quantity_limit": 200, "four_eyes_required": True}),
        tc.freeze_market_data_snapshot(order, {"quote_time": "2026-05-29T09:00:00Z", "source": "md-ref", "currency": "USD", "price": 10, "age_seconds": 30, "max_age_seconds": 120}),
        tc.capture_partial_fills(order, ({"execution_id": "E1", "quantity": 40, "price": 10}, {"execution_id": "E2", "quantity": 60, "price": 11})),
        tc.handle_execution_correction({"execution_id": "E1", "quantity": 100}, ({"correction_type": "quantity_correction", "quantity_delta": -5},)),
        tc.validate_allocation_eligibility(({"allocation_id": "A1", "account": "ACC-1", "product_type": "equity", "quantity": 50},), {"ACC-1": {"allowed_products": ("equity",), "hard_limit": 100}}),
        tc.simulate_residual_allocation(101, ({"account": "A", "weight": 0.5}, {"account": "B", "weight": 0.5}), {"method": "designated_account", "designated_account": "A"}),
        tc.audit_block_trade_split({"execution_id": "B1", "quantity": 100}, ({"allocation_id": "A1", "quantity": 60, "allocator": "ops"}, {"allocation_id": "A2", "quantity": 40, "allocator": "ops"})),
        tc.normalize_confirmation("api", {"price": 10, "quantity": 100, "side": "BUY", "account": "ACC-1", "settlement_date": "2026-06-01", "commission": 1, "counterparty": "Broker-A"}),
        tc.affirm_economics({"price": 10, "quantity": 100, "commission": 1, "side": "BUY", "account": "ACC-1", "settlement_date": "2026-06-01", "counterparty": "Broker-A"}, {"price": 10.01, "quantity": 100, "commission": 1, "side": "BUY", "account": "ACC-1", "settlement_date": "2026-06-01", "counterparty": "Broker-A"}, {"price": 0.02, "quantity": 0, "commission": 0}),
        tc.govern_settlement_instruction(({"instruction_id": "SSI-1", "account": "ACC-1", "market": "US", "effective_from": "2026-01-01", "effective_to": "2026-12-31", "approval_state": "approved"},), order),
        tc.enrich_market_settlement({"market": "US", "place_of_settlement": "DTC", "custodian": "C1"}, {"US": ("place_of_settlement", "custodian")}),
        tc.track_settlement_fail({"status": "failed", "failed_date": "2026-05-27", "penalty_rate": 0.001, "notional": 1000, "buy_in_trigger_days": 2, "owner": "custodian"}, as_of="2026-05-30"),
        tc.classify_trade_break({"category": "confirmation", "severity": "high", "root_cause": "price"}),
        tc.link_break_lineage({"break_id": "BR1"}, {"event_id": "E1", "type": "ConfirmationMismatchOpened"}, {"action": "amend_confirmation"}),
        tc.build_position_snapshot_provenance({"source_cut": "allocations", "valuation_time": "2026-05-30T16:00:00Z", "data_completeness": "complete", "view_type": "eod", "correction_status": "clean"}),
        tc.protect_corporate_action_boundary({"event_type": "stock_split", "external_event_id": "CA-1"}),
        tc.normalize_trading_calendar({"trade_date": "2026-05-30", "venue_timezone": "America/New_York", "desk_timezone": "Africa/Nairobi"}, {"holidays": ("2026-06-01",), "cutoff": "16:00"}),
        tc.apply_asset_class_booking_rules({**order, "product_type": "equity"}, {"equity": {"required_fields": ("instrument_id", "side", "quantity")}}),
        tc.compare_charges({"commission": 1, "tax": 0.2}, {"commission": 1.01, "tax": 0.2}, {"commission": 0.05, "tax": 0.01}),
        tc.model_external_party_roles(({"role": "executing_broker", "name": "B"}, {"role": "venue", "name": "XNYS"}, {"role": "clearing_broker", "name": "CB"}, {"role": "custodian", "name": "C"}, {"role": "settlement_agent", "name": "SA"})),
        tc.enforce_compliance_holds(order, (), "settle"),
        tc.attach_best_execution_evidence(order, ({"type": "venue_choice", "ref": "R1"}, {"type": "quote_context", "ref": "Q1"}, {"type": "routing_notes", "ref": "N1"})),
        tc.build_surveillance_handoff(({"pattern": "wash_trade_like", "record_id": "O1"},)),
        tc.build_lifecycle_event_vocabulary(),
        tc.guard_idempotent_intake("execution_api", {"idempotency_key": "K1"}, ("K0",)),
        tc.build_bulk_operations_workbench(({"id": "O1"}, {"id": "O2"}), "bulk_approve", {"roles": ("supervisor",)}),
        tc.build_supervisor_approval_cockpit(({"id": "O1", "desk": "EQD", "legal_entity": "LE1", "notional": 1000, "settlement_urgency": "high"},)),
        tc.plan_governed_agent_task("triage this break", {"break_id": "BR1"}),
        tc.parse_semantic_document({"price": 10, "quantity": 100, "commission": 1, "counterparty": "B"}, "broker_confirm"),
        tc.explain_dead_letter({"code": "missing_ssi"}),
        tc.plan_projection_rebuild(({"name": "positions", "count": 10},), {"checkpoint_id": "CP1"}),
        tc.evaluate_continuous_controls(({"action_id": "ACT1", "maker": "u1", "checker": "u2", "break_age_days": 1, "sla_days": 5, "live_trade": True, "active_ssi": True},)),
        tc.enforce_tenant_legal_entity({"tenant": "t1", "legal_entity": "LE1"}, {"tenant": "t1", "legal_entity": "LE1"}),
        tc.build_release_evidence_pack({"contract_tests": True, "lifecycle_coverage": True, "break_resolution": True, "permission_proofs": True, "projection_rebuild": True, "workbench_snapshots": True}),
        tc.compute_workbench_metrics(({"id": "O1", "age_days": 3, "confirmation_mismatch": True, "settlement_failed": False, "manual_override": False},)),
        tc.simulate_disruption_scenario({"orders": 10, "settlements": 5, "breaks": 2}, {"holiday_days": 1, "agent_outage_factor": 0.2, "policy_tightening_factor": 0.5}),
        tc.annotate_sustainability_boundary({"id": "O1"}, {"venue_sustainability_tag": "low_carbon"}),
        tc.build_cross_pbc_event_contracts(),
        tc.build_extended_api_surface(),
        tc.authorize_action({"roles": ("trader_supervisor",), "desks": ("EQD",)}, "release_order", {"desk": "EQD"}),
        tc.redact_evidence_for_export({"created_date": "2026-05-30", "client_id": "C1", "price": 10}, {"masked_fields": ("client_id",), "retention_years": 7}),
        tc.evaluate_fx_price_tolerances({"price": 10, "fx_rate": 1.2}, {"price": 10.01, "fx_rate": 1.2001}, {"price_auto_match": 0.02, "fx_auto_match": 0.001, "price_review": 0.1, "fx_review": 0.01}),
        tc.track_external_settlement_status(({"party": "custodian", "status": "acknowledged", "at": "2026-05-30T10:00:00Z"},)),
        tc.evaluate_cutoff_escalation({"blocking": True, "value_date": "2026-05-30"}, {"cutoff_minutes_remaining": 20, "urgent_window_minutes": 30}),
        tc.govern_manual_override({"reason_code": "client_instruction", "approver": "sup", "expires_at": "2026-05-31", "post_review_owner": "ops"}),
        tc.build_seed_runbook_scenarios(),
        tc.build_continuous_release_assurance({"contract_tests": True, "lifecycle_scenarios": True, "permission_checks": True, "event_contract_validation": True, "projection_rebuild": True, "ui_evidence": True}),
    ]

    assert len(tc.TRADING_CONTROL_CAPABILITIES) == 50
    assert len(results) == 50
    assert all(result["ok"] is True for result in results)
    assert {result["capability"] for result in results} == set(tc.TRADING_CONTROL_CAPABILITIES)
    assert results[0]["transition_allowed"] is True
    assert results[5]["order_status"] == "fully_filled"
    assert results[11]["affirmed"] is True
    assert results[36]["release_ready"] is True
    assert results[49]["release_allowed"] is True


def test_trading_runtime_ui_service_routes_and_release_evidence_surface_controls():
    service = CapitalMarketsTradingOpsService()
    command = service.command_trade_order(
        {
            "tenant": "tenant-a",
            "instrument_id": "IBM",
            "product_type": "equity",
            "trading_account": "ACC-1",
            "desk": "EQD",
            "trader": "alice",
            "book": "EQ-BOOK",
            "broker": "Broker-A",
            "venue": "XNYS",
            "settlement_model": "DVP",
            "regulatory_classification": "REG-S",
            "side": "BUY",
            "quantity": 100,
            "limit_price": 10.5,
            "submitted_at": "2026-05-29T09:00:00Z",
            "approval_state": "approved",
        }
    )
    workbench = service.query_workbench({"tenant": "tenant-a"})
    route = routes.dispatch_route("GET /capital-markets-trading-ops-workbench", {"tenant": "tenant-a"}, service=service)
    release = runtime.capital_markets_trading_ops_build_release_evidence()
    ui_contract = ui.capital_markets_trading_ops_ui_contract()
    boundary = runtime.capital_markets_trading_ops_verify_owned_table_boundary(("capital_markets_trading_ops_trade_order", "customer_table"))

    assert command["ok"] is True
    assert workbench["ok"] is True
    assert route["ok"] is True
    assert runtime.CAPITAL_MARKETS_TRADING_OPS_ALLOWED_DATABASE_BACKENDS == ("postgresql", "mysql", "mariadb")
    assert boundary["ok"] is False
    assert ui_contract["stream_engine_picker_visible"] is False
    assert len(ui_contract["full_capability_surface"]["trading_control_panels"]) == 50
    assert release["generated_artifacts"]["improve1_trading_control"]["capability_count"] == 50
    assert any(check["id"] == "improve1_trading_control" and check["ok"] for check in release["checks"])


def test_trading_release_readiness_and_runtime_smoke_include_control_contract():
    readiness = release_readiness_manifest()
    validation = validate_release_evidence()
    smoke = runtime.capital_markets_trading_ops_runtime_smoke()
    capabilities = runtime.capital_markets_trading_ops_runtime_capabilities()
    contract = tc.improve1_trading_control_contract()

    assert readiness["ok"] is True
    assert validation["ok"] is True
    assert smoke["ok"] is True
    assert capabilities["ok"] is True
    assert contract["capability_count"] == 50
    assert contract["shared_table_access"] is False
    assert contract["stream_engine_picker_visible"] is False
