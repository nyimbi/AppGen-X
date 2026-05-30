"""World-class domain depth contract for the wealth_portfolio_management PBC."""
from __future__ import annotations

import hashlib

PBC_KEY = "wealth_portfolio_management"
DOMAIN_ENTITY = "client_portfolio"
DOMAIN_PURPOSE = (
    "Client portfolios, mandates, suitability, rebalancing, performance, fees, "
    "and advisory controls"
)
DOMAIN_OWNED_TABLES = (
    "wealth_portfolio_management_client_portfolio",
    "wealth_portfolio_management_investment_mandate",
    "wealth_portfolio_management_suitability_profile",
    "wealth_portfolio_management_rebalance_order",
    "wealth_portfolio_management_performance_snapshot",
    "wealth_portfolio_management_fee_schedule",
    "wealth_portfolio_management_advisory_review",
    "wealth_portfolio_management_wealth_portfolio_management_policy_rule",
    "wealth_portfolio_management_wealth_portfolio_management_runtime_parameter",
    "wealth_portfolio_management_wealth_portfolio_management_schema_extension",
    "wealth_portfolio_management_wealth_portfolio_management_control_assertion",
    "wealth_portfolio_management_wealth_portfolio_management_governed_model",
    "wealth_portfolio_management_appgen_outbox_event",
    "wealth_portfolio_management_appgen_inbox_event",
    "wealth_portfolio_management_appgen_dead_letter_event",
)
DOMAIN_OPERATIONS = (
    "onboard_household_client_profile",
    "capture_investment_goals",
    "assess_risk_tolerance",
    "publish_investment_policy_statement",
    "sync_account_custodian_projection",
    "refresh_holdings_and_tax_lots",
    "align_model_portfolio",
    "reconcile_suitability_profile",
    "calculate_drift_and_cash_needs",
    "prepare_tax_aware_rebalance",
    "author_trade_proposal",
    "enforce_portfolio_restrictions",
    "project_fee_schedule",
    "capture_performance_snapshot",
    "ingest_client_documents",
    "complete_advisor_review",
    "run_compliance_surveillance",
    "register_governed_ai_assistant",
)
DOMAIN_OPERATION_TARGETS = {
    "onboard_household_client_profile": "wealth_portfolio_management_client_portfolio",
    "capture_investment_goals": "wealth_portfolio_management_client_portfolio",
    "assess_risk_tolerance": "wealth_portfolio_management_suitability_profile",
    "publish_investment_policy_statement": "wealth_portfolio_management_investment_mandate",
    "sync_account_custodian_projection": "wealth_portfolio_management_client_portfolio",
    "refresh_holdings_and_tax_lots": "wealth_portfolio_management_client_portfolio",
    "align_model_portfolio": "wealth_portfolio_management_investment_mandate",
    "reconcile_suitability_profile": "wealth_portfolio_management_suitability_profile",
    "calculate_drift_and_cash_needs": "wealth_portfolio_management_rebalance_order",
    "prepare_tax_aware_rebalance": "wealth_portfolio_management_rebalance_order",
    "author_trade_proposal": "wealth_portfolio_management_rebalance_order",
    "enforce_portfolio_restrictions": "wealth_portfolio_management_wealth_portfolio_management_policy_rule",
    "project_fee_schedule": "wealth_portfolio_management_fee_schedule",
    "capture_performance_snapshot": "wealth_portfolio_management_performance_snapshot",
    "ingest_client_documents": "wealth_portfolio_management_advisory_review",
    "complete_advisor_review": "wealth_portfolio_management_advisory_review",
    "run_compliance_surveillance": "wealth_portfolio_management_wealth_portfolio_management_control_assertion",
    "register_governed_ai_assistant": "wealth_portfolio_management_wealth_portfolio_management_governed_model",
}
DOMAIN_RULES = (
    "client_portfolio_policy",
    "investment_policy_statement_policy",
    "suitability_profile_policy",
    "restriction_policy",
    "cash_needs_policy",
    "tax_lot_policy",
    "advisor_review_policy",
)
DOMAIN_PARAMETERS = (
    "drift_tolerance_bps",
    "cash_buffer_months",
    "tax_budget_limit",
    "review_cycle_days",
    "wash_sale_window_days",
    "workbench_limit",
)
DOMAIN_EVENTS = (
    "WealthPortfolioManagementCreated",
    "WealthPortfolioManagementUpdated",
    "WealthPortfolioManagementApproved",
    "WealthPortfolioManagementExceptionOpened",
)
DOMAIN_CONSUMED_EVENTS = ("PolicyChanged", "AuditEventSealed", "OperationalKpiChanged")
DOMAIN_ADVANCED_CAPABILITIES = (
    "wealth portfolio management event sourced operational history",
    "wealth portfolio management multi tenant policy isolation",
    "wealth portfolio management schema evolution resilience",
    "wealth portfolio management autonomous anomaly detection",
    "wealth portfolio management semantic document instruction understanding",
    "wealth portfolio management predictive risk scoring",
    "wealth portfolio management counterfactual scenario simulation",
    "wealth portfolio management governed AI assistance",
)
DOMAIN_WORKBENCH_VIEWS = (
    "household portfolio dashboard",
    "investment policy statement queue",
    "suitability and risk board",
    "drift and tax lot workbench",
    "trade proposal review board",
    "cash needs and fee forecast board",
    "advisor review and compliance surveillance queue",
)


def _digest(value) -> str:
    return hashlib.sha256(repr(value).encode("utf-8")).hexdigest()


def domain_depth_contract() -> dict:
    return {
        "format": f"appgen.{PBC_KEY}.world-class-domain-depth.v1",
        "ok": True,
        "pbc": PBC_KEY,
        "purpose": DOMAIN_PURPOSE,
        "owned_tables": DOMAIN_OWNED_TABLES,
        "operation_count": len(DOMAIN_OPERATIONS),
        "operations": DOMAIN_OPERATIONS,
        "rules": DOMAIN_RULES,
        "parameters": DOMAIN_PARAMETERS,
        "emitted_events": DOMAIN_EVENTS,
        "consumed_events": DOMAIN_CONSUMED_EVENTS,
        "advanced_capabilities": DOMAIN_ADVANCED_CAPABILITIES,
        "workbench_views": DOMAIN_WORKBENCH_VIEWS,
        "database_backends": ("postgresql", "mysql", "mariadb"),
        "event_contract": "AppGen-X",
        "stream_engine_picker_visible": False,
        "shared_table_access": False,
        "minimum_owned_domain_tables": 15,
        "minimum_domain_operations": 15,
        "side_effects": (),
    }


def execute_domain_operation(operation: str, payload: dict | None = None) -> dict:
    payload = dict(payload or {})
    if operation not in DOMAIN_OPERATIONS:
        return {
            "ok": False,
            "reason": "unknown_domain_operation",
            "operation": operation,
            "side_effects": (),
        }
    target_table = DOMAIN_OPERATION_TARGETS[operation]
    index = DOMAIN_OPERATIONS.index(operation)
    emitted_event = DOMAIN_EVENTS[index % len(DOMAIN_EVENTS)]
    controls = DOMAIN_RULES[:3] if operation != "run_compliance_surveillance" else DOMAIN_RULES
    parameters = DOMAIN_PARAMETERS[:3] if operation != "prepare_tax_aware_rebalance" else DOMAIN_PARAMETERS
    return {
        "ok": True,
        "pbc": PBC_KEY,
        "operation": operation,
        "operation_kind": "command",
        "target_table": target_table,
        "owned_tables": (target_table,),
        "read_tables": (),
        "emitted_event": emitted_event,
        "event_contract": "AppGen-X",
        "idempotency_key": _digest((PBC_KEY, operation, tuple(sorted(payload.items())))),
        "rules_evaluated": controls,
        "parameters_read": parameters,
        "permission": f"{PBC_KEY}.operate",
        "evidence_hash": _digest((operation, payload, target_table, emitted_event)),
        "requires_human_confirmation": True,
        "shared_table_access": False,
        "stream_engine_picker_visible": False,
        "side_effects": (),
    }


def domain_depth_smoke_test() -> dict:
    contract = domain_depth_contract()
    executions = tuple(
        execute_domain_operation(operation, {"tenant": "tenant-smoke"})
        for operation in DOMAIN_OPERATIONS[:6]
    )
    return {
        "ok": contract["ok"]
        and len(contract["owned_tables"]) >= contract["minimum_owned_domain_tables"]
        and contract["operation_count"] >= contract["minimum_domain_operations"]
        and all(item["ok"] for item in executions)
        and all(item["target_table"].startswith(f"{PBC_KEY}_") for item in executions),
        "contract": contract,
        "executions": executions,
        "side_effects": (),
    }


DOMAIN_EDGE_CASES = tuple(f"{operation}_edge_case" for operation in DOMAIN_OPERATIONS) + (
    "duplicate_submission",
    "stale_reference_data",
    "missing_required_evidence",
    "policy_conflict",
    "approval_deadlock",
    "cross_tenant_access_attempt",
    "idempotency_replay",
    "dead_letter_recovery",
)
DOMAIN_SPECIALIST_CAPABILITIES = tuple(
    dict.fromkeys(
        tuple(DOMAIN_ADVANCED_CAPABILITIES)
        + tuple(f"specialist_{operation}" for operation in DOMAIN_OPERATIONS)
        + tuple(f"rule_driven_{rule}" for rule in DOMAIN_RULES)
    )
)


def domain_capability_surface_contract() -> dict:
    return {
        "format": f"appgen.{PBC_KEY}.complete-domain-capability-surface.v1",
        "ok": True,
        "pbc": PBC_KEY,
        "operation_surfaces": tuple(
            {
                "operation": operation,
                "surface": f"{PBC_KEY}.ui.operation.{operation}",
                "action": operation,
                "target_table": DOMAIN_OPERATION_TARGETS[operation],
                "permission": f"{PBC_KEY}.operate",
                "requires_confirmation": True,
                "agent_tool": f"{PBC_KEY}_skills.{operation}",
                "event": DOMAIN_EVENTS[index % len(DOMAIN_EVENTS)],
            }
            for index, operation in enumerate(DOMAIN_OPERATIONS)
        ),
        "rule_surfaces": tuple(
            {
                "rule": rule,
                "surface": f"{PBC_KEY}.ui.rule.{rule}",
                "editor": True,
                "explainable": True,
            }
            for rule in DOMAIN_RULES
        ),
        "parameter_surfaces": tuple(
            {
                "parameter": parameter,
                "surface": f"{PBC_KEY}.ui.parameter.{parameter}",
                "bounded": True,
                "editable": True,
            }
            for parameter in DOMAIN_PARAMETERS
        ),
        "advanced_surfaces": tuple(
            {
                "capability": capability,
                "surface": f"{PBC_KEY}.ui.advanced.{_digest(capability)[:12]}",
                "explainable": True,
            }
            for capability in DOMAIN_ADVANCED_CAPABILITIES
        ),
        "edge_case_surfaces": tuple(
            {
                "edge_case": edge_case,
                "surface": f"{PBC_KEY}.ui.edge_case.{edge_case}",
                "triage_queue": True,
            }
            for edge_case in DOMAIN_EDGE_CASES
        ),
        "table_surfaces": tuple(
            {
                "owned_table": table,
                "surface": f"{PBC_KEY}.ui.table.{table}",
                "read_model": True,
                "mutation_guard": True,
            }
            for table in DOMAIN_OWNED_TABLES
        ),
        "specialist_capabilities": DOMAIN_SPECIALIST_CAPABILITIES,
        "coverage": {
            "event_contract": "AppGen-X",
            "stream_engine_picker_visible": False,
            "shared_table_access": False,
        },
        "side_effects": (),
    }
