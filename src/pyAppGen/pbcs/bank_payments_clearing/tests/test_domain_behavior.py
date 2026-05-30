"""Executable domain behavior tests for the bank_payments_clearing PBC."""

from __future__ import annotations

from pyAppGen.pbcs.bank_payments_clearing import implementation_contract, smoke_test
from pyAppGen.pbcs.bank_payments_clearing import payment_control as pc
from pyAppGen.pbcs.bank_payments_clearing import runtime
from pyAppGen.pbcs.bank_payments_clearing.agent import agent_skill_manifest, chatbot_interface_contract, composed_agent_contribution, datastore_crud_plan, document_instruction_plan
from pyAppGen.pbcs.bank_payments_clearing.capability_assurance import validate_table_stakes_capability_coverage
from pyAppGen.pbcs.bank_payments_clearing.domain_depth import DOMAIN_OPERATIONS, domain_capability_surface_contract, domain_depth_contract, execute_domain_operation
from pyAppGen.pbcs.bank_payments_clearing.payment_operations import assemble_clearing_batch, build_payment_operations_release_evidence, build_payment_operations_workbench, create_payment_instruction, empty_operations_state, generate_settlement_file, handle_settlement_acknowledgement, process_return_item, reconcile_bank_statement, register_participant_bank, release_payment_instruction, validate_payment_instruction
from pyAppGen.pbcs.bank_payments_clearing.release_evidence import build_release_evidence, release_readiness_manifest, validate_release_evidence
from pyAppGen.pbcs.bank_payments_clearing.routes import api_route_contracts, dispatch_route, validate_api_route_contracts
from pyAppGen.pbcs.bank_payments_clearing.services import BankPaymentsClearingService, service_operation_contracts, service_operation_manifest
from pyAppGen.pbcs.bank_payments_clearing.ui import bank_payments_clearing_render_workbench, bank_payments_clearing_single_pbc_app_contract, bank_payments_clearing_ui_contract


TENANT = "tenant_alpha"
PARTICIPANT = {"participant_bank_id": "bank_a", "routing_identifier": "021000021", "supported_rails": ("ach", "wire", "instant", "cross_border"), "status": "active"}
PAYMENT = {"instruction_id": "PAY-100", "tenant": TENANT, "rail": "ach", "participant_bank_id": "bank_a", "amount": 1250.0, "currency": "USD", "beneficiary_account": "123456789", "beneficiary_name": "Supplier One", "originator_authorized": True, "originator_id": "ORG-1", "external_reference": "EXT-100", "purpose": "supplier", "value_date": "2026-05-30", "effective_date": "2026-05-30", "screening_evidence": {"decision": "clear", "freshness": "current"}, "state": "released"}
POLICY_EVENT = {"event_type": "PolicyChanged", "event_id": "policy-alpha-001", "idempotency_key": "policy:alpha:001", "payload": {"tenant": TENANT, "policy_id": "payments-release"}}


def _operations_state() -> dict:
    state = register_participant_bank(empty_operations_state(), PARTICIPANT)["state"]
    state = create_payment_instruction(state, PAYMENT)["state"]
    return release_payment_instruction(state, "PAY-100", maker="maker", checker="checker", liquidity={"available": 5000, "buffer": 250, "freshness": "current"})["state"]


def test_bank_payment_control_primitives_cover_all_improve1_capabilities() -> None:
    transition = pc.evaluate_payment_state_transition("validated", "approved")
    rail = pc.classify_payment_rail(PAYMENT)
    participant = pc.evaluate_participant_bank(PARTICIPANT, rail="ach")
    party = pc.validate_party_details(PAYMENT)
    limits = pc.enforce_limits_velocity(PAYMENT, {"daily_amount": 9000}, {"transaction_limit": 5000, "daily_limit": 10000})
    screening = pc.evaluate_screening_boundary({"decision": "hold", "freshness": "stale"}, ("screening_decision_event", "fraud_case_table"))
    batch = pc.assemble_batch_plan((PAYMENT,), rail="ach", participant_bank_id="bank_a")
    cutoff = pc.calculate_next_clearing_window("2026-05-30T18:00:00", {"cutoff": "17:00"})
    file_control = pc.build_settlement_file_control({"batch_id": "BATCH-1", "item_count": 1, "total_amount": 1250.0, "hash_total": batch["hash_total"]}, sequence=1, encryption={"encrypted": True, "signature": True})
    ack = pc.process_acknowledgement_control({"item_count": 2}, {"acknowledgement_id": "ACK-1", "accepted_count": 1, "rejected_count": 1})
    returned = pc.process_return_lifecycle({"return_id": "RET-1", "reason_code": "closed_account"}, PAYMENT)
    exception = pc.route_exception_case({"exception_type": "liquidity", "severity": "high"})
    repair = pc.plan_repair_workflow(PAYMENT, {**PAYMENT, "beneficiary_account": "987654321"}, ({"role": "maker"}, {"role": "checker"}))
    recall = pc.evaluate_cancellation_recall({**PAYMENT, "state": "settled"})
    liquidity = pc.evaluate_liquidity_funding(PAYMENT, {"available": 1000, "buffer": 500, "freshness": "current"})
    reconciliation = pc.match_bank_reconciliation((PAYMENT,), ({"external_reference": "EXT-100", "amount": 1250.0}, {"line_type": "fee", "amount": 2.5}))
    account_boundary = pc.validate_account_projection_boundary(("balance_projection_api", "gl_entry_table"))
    fees = pc.build_fee_charge_evidence(({"fee_type": "explicit", "amount": 2.5}, {"fee_type": "deducted", "amount": 1.0}))
    controls = pc.evaluate_operational_risk_controls(({"maker": "same", "checker": "same"}, {"state": "breaks_open"}), {"maker_checker_conflicts": 0, "reconciliation_breaks": 0})
    maker_checker = pc.enforce_maker_checker({"maker": "maker", "checker": "checker", "required_role": "approver"}, ("approver",))
    message = pc.validate_payment_message(PAYMENT, {"version": "pacs.008.001.09", "required_fields": ("instruction_id", "beneficiary_account"), "conditional_rules": ({"when": "rail", "then": "currency"},)})
    duplicate = pc.score_duplicate_payment(PAYMENT, ({**PAYMENT, "instruction_id": "PAY-OLD"},))
    instant = pc.evaluate_realtime_finality({**PAYMENT, "rail": "instant"}, {"status": "timeout"})
    card = pc.reconcile_card_settlement_cycle({"presentment_total": 1000, "interchange": 10, "scheme_fees": 5, "chargebacks": 20, "settlement_amount": 960})
    cross_border = pc.evaluate_cross_border_controls({**PAYMENT, "rail": "cross_border", "correspondent_chain": ("BANK-X",), "purpose_code": "GDS", "charge_bearer": "SHA", "country": "KE", "regulatory_report_flag": True})
    fx = pc.evaluate_fx_projection({"quote_id": "FX-1", "expiry": "2026-05-30T10:00:00"}, as_of="2026-05-30T12:00:00")
    notification = pc.build_notification_event(PAYMENT, "payment_returned")
    workbench = pc.build_operations_workbench_queues(({**PAYMENT, "state": "repair_required"}, {**PAYMENT, "instruction_id": "PAY-2", "state": "returned"}))
    investigation = pc.build_payment_investigation_summary(PAYMENT, ({"evidence_id": "EV-1", "detail": "ack accepted"},))
    agent_command = pc.plan_governed_agent_command("release_batch", {"payment_id": "PAY-100", "evidence": "EV-1", "confirmation": True}, {"authority": "approver"})
    health = pc.evaluate_participant_health({"outage_state": "degraded", "reject_rate": 0.01, "ack_latency_minutes": 5, "fallback_rule": "reroute_next_window"})
    forecast = pc.forecast_clearing_window_risk({"pending_items": 4, "approval_backlog": 2, "screening_holds": 1, "liquidity_shortage": True})
    analytics = pc.compute_payment_risk_analytics((PAYMENT, {**PAYMENT, "instruction_id": "PAY-2", "rail": "wire", "exception_type": "return"}))
    trends = pc.analyze_return_reason_trends(({"reason_code": "closed_account"}, {"reason_code": "closed_account"}))
    aging = pc.age_reconciliation_breaks(({"break_id": "BR-1", "opened_date": "2026-05-01", "amount": 5000},), as_of="2026-05-30")
    security = pc.evaluate_file_security_controls({"encrypted": True, "signature": "sig", "key_version": "v1", "checksum": "abc"})
    investigation_event = pc.build_investigation_boundary_event(PAYMENT, ("velocity", "beneficiary_change"))
    report = pc.create_regulatory_report_candidate({**PAYMENT, "amount": 15000})
    root_causes = pc.analyze_exception_root_causes(({"root_cause": "participant_outage"}, {"root_cause": "participant_outage"}))
    idem = pc.apply_idempotency_guard("release", PAYMENT, ())
    retry = pc.plan_dead_letter_retry({"retry_count": 4, "max_attempts": 3, "risk": "medium", "checkpoint": "ACK-1"})
    proof = pc.build_payment_proof_chain(({"event_id": "E1", "payload": PAYMENT}, {"event_id": "E2", "payload": {"state": "released"}}))
    privacy = pc.apply_privacy_view(PAYMENT, "operator")
    impact = pc.simulate_configuration_impact({"parameter": "transaction_limit", "new_value": 1000}, (PAYMENT,))
    seeds = pc.seeded_payments_scenario_library()
    permission = pc.evaluate_role_permission("release", {"roles": ("approver",)})
    finance = pc.build_finance_handoff_events({"settlement_id": "SET-1", "evidence_reference": "EV-1"})
    simulation = pc.run_full_payments_release_simulation()
    overlap = pc.evaluate_overlap_guardrails(("account_balance_projection_api", "gl_entry_table"))
    dsl = pc.build_composition_dsl_agent_exposure()
    contract = pc.improve1_payment_control_contract()

    results = (transition, rail, participant, party, limits, screening, batch, cutoff, file_control, ack, returned, exception, repair, recall, liquidity, reconciliation, account_boundary, fees, controls, maker_checker, message, duplicate, instant, card, cross_border, fx, notification, workbench, investigation, agent_command, health, forecast, analytics, trends, aging, security, investigation_event, report, root_causes, idem, retry, proof, privacy, impact, seeds, permission, finance, simulation, overlap, dsl, contract)

    assert len(pc.PAYMENT_CONTROL_CAPABILITIES) == 50
    assert all(result["ok"] is True for result in results if result is not overlap)
    assert transition["allowed"] is True
    assert rail["valid"] is True
    assert participant["routable"] is True
    assert limits["override_required"] is True
    assert screening["hold_required"] is True and screening["forbidden_references"] == ("fraud_case_table",)
    assert batch["finalization_lock"] is True
    assert cutoff["reason"] == "missed_cutoff"
    assert ack["ack_type"] == "partial"
    assert returned["repair_eligible"] is True
    assert recall["outcome"] == "too_late"
    assert liquidity["hold"] is True
    assert reconciliation["reconciled"] is True
    assert account_boundary["boundary_ok"] is False
    assert duplicate["block_release"] is True
    assert instant["finality_state"] == "timeout_unknown"
    assert fx["block_payment"] is True
    assert health["route_hold"] is True
    assert forecast["cutoff_risk"] is True
    assert aging["escalations"]
    assert security["transmission_blocked"] is True
    assert retry["manual_release_gate"] is True
    assert privacy["view"]["beneficiary_account"] == "REDACTED"
    assert impact["activation_requires_review"] is True
    assert simulation["complete"] is True
    assert overlap["forbidden_references"] == ("gl_entry_table",)
    assert dsl["dsl"]["stream_engine_picker_visible"] is False
    assert contract["capability_count"] == 50
    assert all(result["stream_engine_picker_visible"] is False for result in results)


def test_bank_payment_operations_runtime_services_routes_ui_and_agent_are_executable() -> None:
    ops_state = _operations_state()
    batch = assemble_clearing_batch(ops_state, "batch_1", rail="ach", participant_bank_id="bank_a", cutoff_context={"missed_cutoff": False})
    file_result = generate_settlement_file(batch["state"], "file_1", "batch_1", sequence=1, channel="host_to_host")
    ack = handle_settlement_acknowledgement(file_result["state"], {"acknowledgement_id": "ack_1", "file_id": "file_1", "accepted_count": 1, "rejected_count": 0})
    returned = process_return_item(ack["state"], {"return_id": "return_1", "instruction_id": "PAY-100", "reason_code": "closed_account"})
    recon = reconcile_bank_statement(returned["state"], "recon_1", ({"external_reference": "EXT-100", "amount": 1250.0}, {"line_type": "fee", "amount": 2.5}))
    payment_workbench = build_payment_operations_workbench(recon["state"])

    state = runtime.bank_payments_clearing_empty_state()
    state = runtime.bank_payments_clearing_configure_runtime(state, {"database_backend": "postgresql", "event_topic": runtime.BANK_PAYMENTS_CLEARING_REQUIRED_EVENT_TOPIC})["state"]
    state = runtime.bank_payments_clearing_set_parameter(state, "workbench_limit", 50)["state"]
    state = runtime.bank_payments_clearing_register_rule(state, {"rule_id": "maker_checker_required", "scope": "release"})["state"]
    state = runtime.bank_payments_clearing_register_schema_extension(state, "payment_instruction", {"rail_profile_hash": "text"})["state"]
    received = runtime.bank_payments_clearing_receive_event(state, POLICY_EVENT)
    duplicate = runtime.bank_payments_clearing_receive_event(received["state"], POLICY_EVENT)
    dead = runtime.bank_payments_clearing_receive_event(duplicate["state"], {"event_type": "UnexpectedEvent", "idempotency_key": "bad-event"})
    command = runtime.bank_payments_clearing_command_payment_instruction(dead["state"], {"tenant": TENANT, "code": "PAY-RUNTIME"})
    bad_extension = runtime.bank_payments_clearing_register_schema_extension(command["state"], "shared_payment_table", {"x": "jsonb"})
    service = BankPaymentsClearingService()
    service_bank = service.register_participant_bank(PARTICIPANT)
    service_command = service.create_validated_payment_instruction(PAYMENT)
    service_query = service.query_workbench({"tenant": TENANT})
    route_dispatch = dispatch_route("POST", "/participant-banks", PARTICIPANT)
    ui_contract = bank_payments_clearing_ui_contract()
    rendered = bank_payments_clearing_render_workbench(recon["state"])
    single_app = bank_payments_clearing_single_pbc_app_contract()
    doc_plan = document_instruction_plan("payment return notice", "release payment and open exception")
    crud = datastore_crud_plan("create", "bank_payments_clearing_payment_instruction", {"instruction_id": "PAY-200"})
    rejected_crud = datastore_crud_plan("update", "gl_entry_table", {})

    assert validate_payment_instruction(ops_state, PAYMENT)["ok"] is True
    assert batch["ok"] is True and batch["batch"]["finalization_lock"] is True
    assert file_result["settlement_file"]["signature"].startswith("appgen_payment_file_sig_")
    assert ack["acknowledgement"]["ack_type"] == "accepted"
    assert returned["return_item"]["notification_required"] is True
    assert recon["ok"] is True
    assert payment_workbench["ok"] is True and payment_workbench["stream_engine_picker_visible"] is False
    assert duplicate["duplicate"] is True
    assert dead["ok"] is False and dead["dead_letter_table"] == "bank_payments_clearing_appgen_dead_letter_event"
    assert command["ok"] is True
    assert bad_extension["ok"] is False and bad_extension["reason"] == "unknown_owned_table"
    assert runtime.bank_payments_clearing_build_schema_contract()["database_backends"] == ("postgresql", "mysql", "mariadb")
    assert runtime.bank_payments_clearing_build_api_contract()["stream_engine_picker_visible"] is False
    assert runtime.bank_payments_clearing_build_release_evidence()["generated_artifacts"]["improve1_payment_control"]["capability_count"] == 50
    assert runtime.bank_payments_clearing_runtime_smoke()["ok"] is True
    assert service_operation_manifest()["ok"] is True
    assert service_operation_contracts()["ok"] is True
    assert service_bank["ok"] is True
    assert service_command["ok"] is True
    assert service_query["operation_kind"] == "query"
    assert validate_api_route_contracts()["ok"] is True
    assert api_route_contracts()["ok"] is True
    assert route_dispatch["ok"] is True
    assert ui_contract["ok"] is True and len(ui_contract["payment_control_panels"]) == 50
    assert rendered["ok"] is True
    assert single_app["ok"] is True and single_app["database_backing"]["database_backends"] == ("postgresql", "mysql", "mariadb")
    assert agent_skill_manifest()["ok"] is True
    assert chatbot_interface_contract()["single_agent_contribution"] == "bank_payments_clearing_skills"
    assert doc_plan["requires_human_confirmation"] is True
    assert crud["ok"] is True and crud["requires_confirmation"] is True
    assert rejected_crud["ok"] is False
    assert composed_agent_contribution()["ok"] is True


def test_bank_payment_release_evidence_and_package_contract_are_executable() -> None:
    payment_evidence = build_payment_operations_release_evidence()
    release_build = build_release_evidence()
    release_manifest = release_readiness_manifest()
    release_validation = validate_release_evidence()
    capability_validation = validate_table_stakes_capability_coverage()
    package_contract = implementation_contract()
    package_smoke = smoke_test()
    domain = domain_depth_contract()
    surface = domain_capability_surface_contract()
    executed = tuple(execute_domain_operation(operation, {"tenant": TENANT}) for operation in DOMAIN_OPERATIONS[:6])

    assert payment_evidence["ok"] is True
    assert release_build["ok"] is True
    assert any(check["id"] == "payment_operations_execution" for check in release_build["checks"])
    assert release_manifest["ok"] is True
    assert release_validation["ok"] is True
    assert capability_validation["ok"] is True
    assert package_contract["advanced_runtime"]["ok"] is True
    assert package_contract["ui_contract"]["payment_control_contract"]["capability_count"] == 50
    assert package_smoke["ok"] is True
    assert domain["ok"] is True and domain["event_contract"] == "AppGen-X"
    assert surface["ok"] is True and surface["coverage"]["shared_table_access"] is False
    assert all(item["ok"] is True for item in executed)
    assert all(item["target_table"].startswith("bank_payments_clearing_") for item in executed)
