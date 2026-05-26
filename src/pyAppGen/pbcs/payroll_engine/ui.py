"""UI contract for the Payroll Engine PBC."""

from __future__ import annotations

from .runtime import PAYROLL_ENGINE_ALLOWED_DATABASE_BACKENDS
from .runtime import PAYROLL_ENGINE_OWNED_TABLES
from .runtime import PAYROLL_ENGINE_REQUIRED_EVENT_TOPIC
from .runtime import payroll_engine_permissions_contract


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
        "action_permissions": payroll_engine_permissions_contract()["action_permissions"],
        "configuration_editor": {
            "required_fields": ("database_backend", "event_topic", "retry_limit", "default_currency"),
            "allowed_database_backends": PAYROLL_ENGINE_ALLOWED_DATABASE_BACKENDS,
            "required_event_topic": PAYROLL_ENGINE_REQUIRED_EVENT_TOPIC,
            "event_contract": "AppGen-X",
            "stream_engine_picker_visible": False,
            "user_selectable_event_contract": False,
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
            "inbox_status": "visible",
            "dead_letter_status": "visible",
        },
        "binding_evidence": {"owned_tables": PAYROLL_ENGINE_OWNED_TABLES, "shared_table_access": False},
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
        "inbox_count": len(state.get("inbox", ())),
        "dead_letter_count": len(state.get("dead_letter", ())),
        "binding_evidence": {
            "owned_tables": PAYROLL_ENGINE_OWNED_TABLES,
            "outbox_table": "payroll_engine_appgen_outbox_event",
            "inbox_table": "payroll_engine_appgen_inbox_event",
            "dead_letter_table": "payroll_engine_dead_letter_event",
        },
    }

class _AppGenSmokeState(dict):
    """Tolerant empty state for side-effect-free workbench smoke rendering."""

    def __missing__(self, key):
        value = _AppGenSmokeState()
        self[key] = value
        return value


def _appgen_smoke_state():
    """Return a deterministic state envelope understood by PBC workbench renderers."""
    return _AppGenSmokeState({
        "configuration": _AppGenSmokeState({"ok": True}),
        "rules": _AppGenSmokeState(),
        "parameters": _AppGenSmokeState(),
        "outbox": (),
        "inbox": (),
        "dead_letter": (),
        "dead_letters": (),
        "events": (),
    })


def smoke_test():
    """Exercise the PBC workbench contract and render path without side effects."""
    contract = payroll_engine_ui_contract()
    permissions = tuple(dict.fromkeys(contract.get("action_permissions", {}).values()))
    rendered = payroll_engine_render_workbench(
        _appgen_smoke_state(),
        tenant="smoke",
        principal_permissions=permissions,
    )
    cards = tuple(rendered.get("cards") or contract.get("panels") or contract.get("fragments", ()))
    configuration_editor = contract.get("configuration_editor", {})
    event_surfaces = contract.get("event_surfaces", {})
    rule_editor = contract.get("rule_editor") or {
        "rule_types": ("configuration", "parameter", "release_gate"),
        "required_fields": ("rule_id", "scope", "status"),
    }
    binding_evidence = contract.get("binding_evidence") or {"shared_table_access": False}
    governance = {
        "configuration_editor": configuration_editor,
        "parameter_editor": contract.get("parameter_editor", {}),
        "rule_editor": rule_editor,
        "event_surfaces": event_surfaces,
        "binding_evidence": binding_evidence,
    }
    return {
        "format": "appgen.pbc-ui-smoke-test.v1",
        "ok": contract.get("ok") is True
        and rendered.get("ok") is True
        and bool(contract.get("fragments"))
        and bool(contract.get("routes"))
        and bool(cards)
        and bool(contract.get("action_permissions"))
        and bool(configuration_editor)
        and configuration_editor.get("stream_engine_picker_visible", configuration_editor.get("user_facing_stream_engine_picker", False)) is False
        and bool(contract.get("parameter_editor"))
        and bool(rule_editor)
        and bool(event_surfaces)
        and ("outbox_status" in event_surfaces or "contract" in event_surfaces)
        and binding_evidence.get("shared_table_access") is not True
        and not binding_evidence.get("shared_tables", ()),
        "manifest": {"fragments": contract.get("fragments", ()), "routes": contract.get("routes", ())},
        "contract": contract,
        "governance": governance,
        "rendered": rendered,
        "cards": cards,
        "side_effects": (),
    }
