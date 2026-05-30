"""Package-local controls for trade finance operations."""

from __future__ import annotations

PBC_KEY = "trade_finance_operations"


def trade_finance_operations_control_catalog() -> dict:
    contracts = (
        {
            "key": "TradeOperationsQueueCards",
            "type": "cards",
            "binds_to": ("open_cases", "sanctions_holds", "active_discrepancies", "due_settlements"),
        },
        {
            "key": "DocumentMatrixCompareControl",
            "type": "matrix_compare",
            "binds_to": ("trade_document", "discrepancy_case", "shipment_evidence"),
        },
        {
            "key": "SanctionsBoundaryControl",
            "type": "policy_guardrail",
            "binds_to": ("sanctions_check", "trade_document", "shipment_evidence"),
        },
        {
            "key": "CollateralLimitCoverageControl",
            "type": "coverage_rail",
            "binds_to": ("collateral_margin", "limit_reservation", "trade_loan"),
        },
        {
            "key": "FeeWaterfallControl",
            "type": "waterfall",
            "binds_to": ("fee_accrual", "trade_settlement"),
        },
        {
            "key": "SwiftEvidenceConsole",
            "type": "message_console",
            "binds_to": ("swift_message_evidence", "trade_settlement"),
        },
        {
            "key": "ReleaseEvidenceGateControl",
            "type": "release_gate",
            "binds_to": ("trade_finance_operations_control_assertion", "trade_settlement", "swift_message_evidence"),
        },
    )
    return {
        "format": "appgen.trade-finance-operations-control-catalog.v1",
        "ok": True,
        "pbc": PBC_KEY,
        "contracts": contracts,
        "side_effects": (),
    }


def smoke_test() -> dict:
    catalog = trade_finance_operations_control_catalog()
    return {
        "ok": catalog["ok"] and len(catalog["contracts"]) >= 5,
        "catalog": catalog,
        "side_effects": (),
    }
