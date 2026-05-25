"""UI contract for the Payroll Engine PBC."""

from __future__ import annotations


PAYROLL_ENGINE_UI_FRAGMENT_KEYS = (
    "PayrollEngineWorkbench",
    "PayrollRunConsole",
    "PayslipReviewBoard",
    "DeductionEditor",
    "BenefitAllocationPanel",
    "PayrollFilingConsole",
    "PayrollRuleStudio",
    "PayrollParameterConsole",
    "PayrollConfigurationPanel",
)


def payroll_engine_ui_contract() -> dict:
    return {
        "format": "appgen.payroll-engine-ui-contract.v1",
        "ok": True,
        "pbc": "payroll_engine",
        "implementation_directory": "src/pyAppGen/pbcs/payroll_engine",
        "fragments": PAYROLL_ENGINE_UI_FRAGMENT_KEYS,
        "routes": (
            "/workbench/pbcs/payroll_engine",
            "/workbench/pbcs/payroll_engine/runs",
            "/workbench/pbcs/payroll_engine/payslips",
            "/workbench/pbcs/payroll_engine/deductions",
            "/workbench/pbcs/payroll_engine/benefits",
            "/workbench/pbcs/payroll_engine/filings",
            "/workbench/pbcs/payroll_engine/rules",
            "/workbench/pbcs/payroll_engine/parameters",
            "/workbench/pbcs/payroll_engine/configuration",
        ),
        "panels": (
            {
                "key": "run_console",
                "fragment": "PayrollRunConsole",
                "binds_to": ("payroll_run", "worker_projection", "labor_hours"),
                "commands": ("create_payroll_run", "calculate_payslip", "post_payroll_run"),
            },
            {
                "key": "payslip_review",
                "fragment": "PayslipReviewBoard",
                "binds_to": ("payslip", "deduction", "benefit_allocation"),
                "commands": ("calculate_payslip", "apply_deduction", "allocate_benefit"),
            },
            {
                "key": "filing_console",
                "fragment": "PayrollFilingConsole",
                "binds_to": ("payroll_run", "payslip", "outbox"),
                "commands": ("prepare_payroll_filing", "generate_payroll_proof"),
            },
            {
                "key": "governance_studio",
                "fragment": "PayrollRuleStudio",
                "binds_to": ("rule", "parameter", "configuration"),
                "commands": ("register_rule", "set_parameter", "configure_runtime", "run_control_tests"),
            },
        ),
        "action_permissions": {
            "create_payroll_run": "payroll_engine.run",
            "calculate_payslip": "payroll_engine.run",
            "apply_deduction": "payroll_engine.run",
            "allocate_benefit": "payroll_engine.run",
            "post_payroll_run": "payroll_engine.approve",
            "prepare_payroll_filing": "payroll_engine.file",
            "register_rule": "payroll_engine.configure",
            "set_parameter": "payroll_engine.configure",
            "configure_runtime": "payroll_engine.configure",
            "run_control_tests": "payroll_engine.audit",
        },
        "configuration_editor": {
            "required_fields": ("database_backend", "event_topic", "retry_limit", "default_currency"),
            "allowed_database_backends": ("postgresql", "mysql", "mariadb"),
            "event_contract": "AppGen-X",
        },
        "parameter_editor": {
            "numeric_parameters": (
                "standard_period_hours",
                "overtime_multiplier",
                "supplemental_rate",
                "net_pay_floor",
                "approval_amount_threshold",
            ),
        },
        "rule_editor": {
            "rule_types": ("pay", "deduction", "benefit", "approval", "filing", "off_cycle"),
            "required_fields": ("rule_id", "tenant", "rule_type", "eligible_worker_types", "allowed_countries", "status"),
        },
        "event_surfaces": {
            "emits": ("PayrollPosted", "PayrollFilingPrepared"),
            "consumes": ("LaborHoursApproved", "TaxCalculated"),
            "outbox_status": "visible",
            "dead_letter_status": "visible",
        },
    }


def payroll_engine_render_workbench(
    state: dict,
    *,
    tenant: str,
    principal_permissions: tuple[str, ...],
) -> dict:
    contract = payroll_engine_ui_contract()
    permissions = set(principal_permissions)
    action_permissions = contract["action_permissions"]
    visible_actions = tuple(
        action
        for action, required_permission in action_permissions.items()
        if required_permission in permissions
    )
    tenant_runs = tuple(run for run in state["payroll_runs"].values() if run["tenant"] == tenant)
    tenant_payslips = tuple(payslip for payslip in state["payslips"].values() if payslip["tenant"] == tenant)
    tenant_filings = tuple(filing for filing in state["filings"].values() if filing["tenant"] == tenant)
    tenant_deductions = tuple(deduction for deduction in state["deductions"].values() if deduction["tenant"] == tenant)
    tenant_benefits = tuple(benefit for benefit in state["benefit_allocations"].values() if benefit["tenant"] == tenant)
    cards = (
        {"key": "payroll_runs", "value": len(tenant_runs), "fragment": "PayrollRunConsole"},
        {"key": "gross_pay_total", "value": round(sum(payslip["gross_pay"] for payslip in tenant_payslips), 2), "fragment": "PayslipReviewBoard"},
        {"key": "net_pay_total", "value": round(sum(payslip["net_pay"] for payslip in tenant_payslips), 2), "fragment": "PayslipReviewBoard"},
        {"key": "deductions", "value": len(tenant_deductions), "fragment": "DeductionEditor"},
        {"key": "benefits", "value": len(tenant_benefits), "fragment": "BenefitAllocationPanel"},
        {"key": "filings", "value": len(tenant_filings), "fragment": "PayrollFilingConsole"},
    )
    return {
        "format": "appgen.payroll-engine-workbench-render.v1",
        "ok": True,
        "tenant": tenant,
        "route": "/workbench/pbcs/payroll_engine",
        "fragments": contract["fragments"],
        "cards": cards,
        "visible_actions": visible_actions,
        "locked_actions": tuple(action for action in action_permissions if action not in visible_actions),
        "configuration_bound": bool(state["configuration"].get("ok")),
        "rules_bound": tuple(sorted(state["rules"])),
        "parameters_bound": tuple(sorted(state["parameters"])),
        "event_outbox_count": len(state["outbox"]),
    }
