"""Package-local wizards for trade finance operations."""

from __future__ import annotations

PBC_KEY = "trade_finance_operations"


def trade_finance_operations_wizard_contracts() -> dict:
    contracts = (
        {
            "key": "TradeLetterOfCreditIssuanceWizard",
            "steps": ("instrument_setup", "party_roles", "document_matrix", "limits_and_fees", "swift_evidence"),
            "forms": (
                "TradeLetterOfCreditIssuanceForm",
                "LimitReservationForm",
                "FeeSettlementForm",
                "SwiftEvidenceForm",
            ),
            "keywords": ("letter of credit", "lc", "issue credit", "mt700"),
        },
        {
            "key": "GuaranteeAndSBLCWizard",
            "steps": ("guarantee_terms", "claim_rules", "collateral", "swift_evidence"),
            "forms": (
                "TradeGuaranteeStandbyForm",
                "CollateralMarginForm",
                "SwiftEvidenceForm",
            ),
            "keywords": ("guarantee", "sblc", "standby", "claim"),
        },
        {
            "key": "DocumentaryCollectionWizard",
            "steps": ("collection_terms", "bill_capture", "shipment_docs", "release_conditions"),
            "forms": (
                "TradeDocumentaryCollectionForm",
                "TradeBillCaptureForm",
                "ShipmentDocumentPackageForm",
            ),
            "keywords": ("collection", "documents against payment", "documents against acceptance"),
        },
        {
            "key": "PresentationExaminationWizard",
            "steps": ("document_intake", "sanctions_screening", "examination", "discrepancy_disposition"),
            "forms": (
                "ShipmentDocumentPackageForm",
                "SanctionsComplianceReviewForm",
                "DiscrepancyDecisionForm",
            ),
            "keywords": ("presentation", "examination", "discrepancy", "waiver"),
        },
        {
            "key": "TradeLoanAndSettlementWizard",
            "steps": ("loan_linkage", "collateral", "fees", "settlement"),
            "forms": (
                "TradeLoanLinkForm",
                "CollateralMarginForm",
                "FeeSettlementForm",
                "SettlementReleaseForm",
            ),
            "keywords": ("trade loan", "settlement", "financing", "liquidation"),
        },
        {
            "key": "ReleaseEvidenceReviewWizard",
            "steps": ("workflow_checks", "event_checks", "assistant_checks", "signoff"),
            "forms": ("SettlementReleaseForm", "SwiftEvidenceForm"),
            "keywords": ("release evidence", "go live", "smoke checks", "signoff"),
        },
    )
    return {
        "format": "appgen.trade-finance-operations-wizard-contract.v1",
        "ok": True,
        "pbc": PBC_KEY,
        "contracts": contracts,
        "side_effects": (),
    }


def smoke_test() -> dict:
    contracts = trade_finance_operations_wizard_contracts()
    return {
        "ok": contracts["ok"] and len(contracts["contracts"]) >= 5,
        "contracts": contracts,
        "side_effects": (),
    }
