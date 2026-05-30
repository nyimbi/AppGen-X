"""Focused standalone application tests for trade_finance_operations."""

from pyAppGen.pbcs.trade_finance_operations import standalone
from pyAppGen.pbcs.trade_finance_operations import ui
from pyAppGen.pbcs.trade_finance_operations.agent import document_instruction_plan
from pyAppGen.pbcs.trade_finance_operations.routes import dispatch_standalone_route
from pyAppGen.pbcs.trade_finance_operations.services import TradeFinanceOperationsStandaloneService


def _service():
    service = TradeFinanceOperationsStandaloneService(tenant="tenant_alpha")
    service.configure()
    service.register_defaults()
    return service


def test_trade_finance_case_journey_runs_end_to_end():
    service = _service()
    lc = service.issue_letter_of_credit(
        {
            "case_id": "TFO-100",
            "tenant": "tenant_alpha",
            "applicant": "Importer Ltd",
            "beneficiary": "Exporter PLC",
            "currency": "USD",
            "face_amount": 250000,
            "required_documents": ("invoice", "bill_of_lading", "insurance_certificate"),
        }
    )
    guarantee = service.issue_bank_guarantee(
        {
            "case_id": "TFO-200",
            "tenant": "tenant_alpha",
            "applicant": "Contractor Ltd",
            "beneficiary": "Project Owner",
            "currency": "USD",
            "face_amount": 100000,
            "guarantee_type": "standby_lc",
        }
    )
    collection = service.lodge_documentary_collection(
        {
            "case_id": "TFO-300",
            "tenant": "tenant_alpha",
            "drawer": "Exporter PLC",
            "drawee": "Buyer Co",
            "currency": "EUR",
            "face_amount": 75000,
        }
    )
    bill = service.register_trade_bill({"case_id": "TFO-100", "bill_id": "BILL-1", "bill_type": "usance_bill", "amount": 250000, "currency": "USD"})
    loan = service.link_trade_loan({"case_id": "TFO-100", "loan_id": "LOAN-1", "facility_id": "FAC-1", "financed_amount": 180000, "currency": "USD", "margin_pct": 0.12})
    docs = service.record_shipment_documents({"case_id": "TFO-100", "package_id": "PKG-1", "documents": ("invoice", "bill_of_lading"), "presentation_date": "2026-06-02"})
    screen = service.run_sanctions_screening({"case_id": "TFO-100", "screening_id": "SCR-1", "triggered_terms": (), "destination_country": "KE"})
    examination = service.examine_document_package({"case_id": "TFO-100", "package_id": "PKG-1", "presentation_deadline": "2026-06-30"})
    waiver = service.request_discrepancy_waiver({"discrepancy_id": examination["examination"]["discrepancy_id"], "decision": "accepted", "requested_by": "applicant", "reason": "acceptable reserve"})
    collateral = service.post_collateral_margin({"case_id": "TFO-100", "collateral_id": "COL-1", "market_value": 60000, "required_margin": 50000, "haircut_pct": 0.1})
    limit_reservation = service.reserve_limit_exposure({"case_id": "TFO-100", "facility_id": "FAC-1", "headroom": 300000, "requested_exposure": 250000})
    fees = service.assess_case_fees({"case_id": "TFO-100", "face_amount": 250000, "fee_rate_bps": 45, "swift_fee": 110, "tax_amount": 16})
    settlement = service.settle_trade_case({"case_id": "TFO-100", "settlement_id": "SET-1", "gross_amount": 250000, "currency": "USD"})
    swift = service.generate_swift_message_evidence({"case_id": "TFO-100", "message_type": "MT700", "sender_bic": "AAAABBCCXXX", "receiver_bic": "DDDDEEFFXXX"})
    release = service.release_evidence()

    assert lc["ok"] is True
    assert guarantee["guarantee"]["is_sblc"] is True
    assert collection["ok"] is True
    assert bill["trade_bill"]["bill_type"] == "usance_bill"
    assert loan["trade_loan"]["repayment_source"] == "settlement_proceeds"
    assert docs["ok"] is True
    assert screen["screening"]["decision"] == "clear"
    assert examination["examination"]["status"] == "open"
    assert waiver["discrepancy"]["status"] == "waived"
    assert collateral["collateral"]["eligible_value"] == 54000.0
    assert limit_reservation["ok"] is True
    assert fees["fee_assessment"]["net_fee"] > 0
    assert settlement["settlement"]["status"] == "completed"
    assert swift["swift_message"]["message_type"] == "MT700"
    assert release["ok"] is True


def test_sanctions_block_and_simulation_are_governed():
    service = _service()
    service.issue_letter_of_credit(
        {
            "case_id": "TFO-400",
            "tenant": "tenant_alpha",
            "applicant": "Importer Ltd",
            "beneficiary": "Exporter PLC",
            "currency": "USD",
            "face_amount": 50000,
        }
    )
    screen = service.run_sanctions_screening({"case_id": "TFO-400", "screening_id": "SCR-2", "triggered_terms": ("sanctioned_party",), "destination_country": "IRAN"})
    service.reserve_limit_exposure({"case_id": "TFO-400", "facility_id": "FAC-2", "headroom": 100000, "requested_exposure": 50000})
    simulation = service.simulate_case_amendment({"case_id": "TFO-400", "proposed_face_amount": 65000, "change_destination_country": True})
    blocked = service.settle_trade_case({"case_id": "TFO-400", "settlement_id": "SET-2", "gross_amount": 50000, "currency": "USD"})

    assert screen["screening"]["decision"] == "blocked"
    assert simulation["mutated"] is False
    assert simulation["impact"]["requires_rescreening"] is True
    assert blocked["ok"] is False
    assert blocked["reason"] == "settlement_blocked"


def test_ui_agent_routes_and_docs_expose_standalone_surface():
    service = _service()
    dispatch = dispatch_standalone_route(
        service,
        "POST",
        "/app/trade-finance/letters-of-credit",
        {
            "case_id": "TFO-500",
            "tenant": "tenant_alpha",
            "applicant": "Importer Ltd",
            "beneficiary": "Exporter PLC",
            "currency": "USD",
            "face_amount": 99000,
        },
    )
    intake = document_instruction_plan(
        "MT700 application with beneficiary Exporter PLC and applicant Importer Ltd",
        "create the issuance draft, show sanctions guidance, and prepare the release workbench",
    )
    workbench = service.workbench("tenant_alpha")
    rendered = ui.trade_finance_operations_render_workbench()
    docs = standalone.documentation_presence()
    smoke = standalone.standalone_smoke_test()

    assert dispatch["ok"] is True
    assert intake["ok"] is True
    assert intake["requires_human_confirmation"] is True
    assert workbench["ok"] is True
    assert workbench["forms"]
    assert workbench["wizards"]
    assert workbench["controls"]
    assert rendered["ok"] is True
    assert docs["ok"] is True
    assert smoke["ok"] is True
