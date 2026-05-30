"""Package-local forms for trade finance operations."""

from __future__ import annotations

PBC_KEY = "trade_finance_operations"


def trade_finance_operations_form_contracts() -> dict:
    contracts = (
        {
            "key": "TradeLetterOfCreditIssuanceForm",
            "table": "trade_finance_operations_letter_of_credit",
            "operation": "issue_letter_of_credit",
            "fields": (
                "case_id",
                "tenant",
                "instrument_type",
                "applicant",
                "beneficiary",
                "issuing_bank",
                "currency",
                "face_amount",
                "availability",
                "expiry_date",
            ),
        },
        {
            "key": "TradeGuaranteeStandbyForm",
            "table": "trade_finance_operations_bank_guarantee",
            "operation": "issue_bank_guarantee",
            "fields": (
                "case_id",
                "tenant",
                "guarantee_type",
                "applicant",
                "beneficiary",
                "currency",
                "face_amount",
                "claim_expiry_date",
            ),
        },
        {
            "key": "TradeDocumentaryCollectionForm",
            "table": "trade_finance_operations_documentary_collection",
            "operation": "lodge_documentary_collection",
            "fields": (
                "case_id",
                "tenant",
                "collection_mode",
                "drawer",
                "drawee",
                "collecting_bank",
                "currency",
                "face_amount",
            ),
        },
        {
            "key": "TradeBillCaptureForm",
            "table": "trade_finance_operations_trade_bill",
            "operation": "register_trade_bill",
            "fields": ("bill_id", "case_id", "bill_type", "amount", "currency", "due_date"),
        },
        {
            "key": "TradeLoanLinkForm",
            "table": "trade_finance_operations_trade_loan",
            "operation": "link_trade_loan",
            "fields": (
                "loan_id",
                "case_id",
                "facility_id",
                "financed_amount",
                "currency",
                "margin_pct",
                "repayment_source",
            ),
        },
        {
            "key": "ShipmentDocumentPackageForm",
            "table": "trade_finance_operations_trade_document",
            "operation": "record_shipment_documents",
            "fields": (
                "case_id",
                "package_id",
                "presentation_date",
                "documents",
                "shipment_date",
                "shipment_country",
            ),
        },
        {
            "key": "SanctionsComplianceReviewForm",
            "table": "trade_finance_operations_sanctions_check",
            "operation": "run_sanctions_screening",
            "fields": (
                "case_id",
                "screening_id",
                "screening_scope",
                "triggered_terms",
                "destination_country",
                "manual_override_reason",
            ),
        },
        {
            "key": "DiscrepancyDecisionForm",
            "table": "trade_finance_operations_discrepancy_case",
            "operation": "request_discrepancy_waiver",
            "fields": (
                "case_id",
                "discrepancy_code",
                "decision",
                "requested_by",
                "reason",
                "waiver_deadline",
            ),
        },
        {
            "key": "CollateralMarginForm",
            "table": "trade_finance_operations_collateral_margin",
            "operation": "post_collateral_margin",
            "fields": (
                "case_id",
                "collateral_id",
                "collateral_type",
                "market_value",
                "haircut_pct",
                "required_margin",
            ),
        },
        {
            "key": "LimitReservationForm",
            "table": "trade_finance_operations_limit_reservation",
            "operation": "reserve_limit_exposure",
            "fields": (
                "case_id",
                "facility_id",
                "facility_limit",
                "headroom",
                "requested_exposure",
                "approval_required",
            ),
        },
        {
            "key": "FeeSettlementForm",
            "table": "trade_finance_operations_fee_accrual",
            "operation": "assess_case_fees",
            "fields": (
                "case_id",
                "fee_rate_bps",
                "swift_fee",
                "discrepancy_fee",
                "amendment_fee",
                "tax_amount",
            ),
        },
        {
            "key": "SettlementReleaseForm",
            "table": "trade_finance_operations_trade_settlement",
            "operation": "settle_trade_case",
            "fields": (
                "case_id",
                "settlement_id",
                "gross_amount",
                "currency",
                "value_date",
                "nostro_account",
                "beneficiary_account",
            ),
        },
        {
            "key": "SwiftEvidenceForm",
            "table": "trade_finance_operations_swift_message_evidence",
            "operation": "generate_swift_message_evidence",
            "fields": (
                "case_id",
                "message_type",
                "sender_bic",
                "receiver_bic",
                "reference",
                "narrative",
            ),
        },
    )
    return {
        "format": "appgen.trade-finance-operations-form-contract.v1",
        "ok": True,
        "pbc": PBC_KEY,
        "contracts": contracts,
        "side_effects": (),
    }


def smoke_test() -> dict:
    contracts = trade_finance_operations_form_contracts()
    return {
        "ok": contracts["ok"] and len(contracts["contracts"]) >= 10,
        "contracts": contracts,
        "side_effects": (),
    }
