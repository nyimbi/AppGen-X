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


PAYROLL_ENGINE_FORM_KEYS=("payroll_run_form","worker_pay_profile_form","payslip_calculation_form","deduction_benefit_form","filing_payment_form","payroll_governance_form")
PAYROLL_ENGINE_WIZARD_KEYS=("gross_to_net_wizard","off_cycle_payment_wizard","filing_payment_wizard","retro_correction_wizard")
PAYROLL_ENGINE_CONTROL_KEYS=("tenant_scope_picker","payroll_run_status_control","gross_net_reconciliation_grid","deduction_benefit_editor","filing_readiness_drawer","assistant_skill_panel")
def payroll_engine_form_catalog()->tuple[dict,...]:
 return ({"key":"payroll_run_form","title":"Payroll Run","command":"create_payroll_run","owned_table":"payroll_run","fields":("run_id","tenant","period","country","legal_entity","pay_group")},{"key":"worker_pay_profile_form","title":"Worker Pay Profile","command":"upsert_worker_projection","owned_table":"worker_pay_profile","fields":("employee_id","worker_type","country","salary_per_period","hourly_rate","currency","identity")},{"key":"payslip_calculation_form","title":"Payslip Calculation","command":"calculate_payslip","owned_table":"payslip","fields":("run_id","employee_id","approved_hours","overtime_hours")},{"key":"deduction_benefit_form","title":"Deduction and Benefit","command":"apply_deduction","owned_table":"deduction","fields":("payslip_id","deduction_id","deduction_type","amount","benefit_type","employee_amount","employer_amount")},{"key":"filing_payment_form","title":"Filing and Payment","command":"prepare_payroll_filing","owned_table":"payroll_filing","fields":("filing_id","run_id","jurisdiction","channel","payment_rail")},{"key":"payroll_governance_form","title":"Payroll Governance","command":"register_rule","owned_table":"payroll_rule","fields":("rule_id","tenant","rule_type","allowed_countries","benefit_classes","deduction_limit_percent","status")})
def payroll_engine_wizard_catalog()->tuple[dict,...]:
 return ({"key":"gross_to_net_wizard","steps":("worker_pay_profile_form","payroll_run_form","payslip_calculation_form","deduction_benefit_form"),"goal":"Calculate payroll from worker/labor data through net pay."},{"key":"off_cycle_payment_wizard","steps":("payroll_run_form","payslip_calculation_form","filing_payment_form"),"goal":"Run governed off-cycle payment with approvals."},{"key":"filing_payment_wizard","steps":("payslip_calculation_form","filing_payment_form"),"goal":"Prepare tax filing and payment handoff evidence."},{"key":"retro_correction_wizard","steps":("payroll_run_form","payslip_calculation_form"),"goal":"Create retro correction and audit evidence."})
def payroll_engine_control_catalog()->tuple[dict,...]:
 return ({"key":"tenant_scope_picker","type":"selector","binds_to":"tenant"},{"key":"payroll_run_status_control","type":"timeline","binds_to":"payroll_run"},{"key":"gross_net_reconciliation_grid","type":"grid","binds_to":"payslip"},{"key":"deduction_benefit_editor","type":"editor","binds_to":"deduction"},{"key":"filing_readiness_drawer","type":"drawer","binds_to":"payroll_filing"},{"key":"assistant_skill_panel","type":"assistant","binds_to":"payroll_engine_skills"})
def payroll_engine_standalone_app_contract()->dict:
 return {"ok":True,"pbc":"payroll_engine","app_id":"payroll_engine_one_pbc_app","workbench_route":"/workbench/pbcs/payroll_engine","navigation":({"key":"runs","route":"/workbench/pbcs/payroll_engine/runs"},{"key":"workers","route":"/workbench/pbcs/payroll_engine/workers"},{"key":"payslips","route":"/workbench/pbcs/payroll_engine/payslips"},{"key":"deductions","route":"/workbench/pbcs/payroll_engine/deductions"},{"key":"filings","route":"/workbench/pbcs/payroll_engine/filings"},{"key":"governance","route":"/workbench/pbcs/payroll_engine/configuration"}),"forms":PAYROLL_ENGINE_FORM_KEYS,"wizards":PAYROLL_ENGINE_WIZARD_KEYS,"controls":PAYROLL_ENGINE_CONTROL_KEYS,"single_agent_namespace":"payroll_engine_skills","side_effects":()}
def payroll_engine_ui_contract()->dict:
 shell=payroll_engine_standalone_app_contract(); return {"format":"appgen.payroll-engine-ui-contract.v1","ok":True,"pbc":"payroll_engine","implementation_directory":"src/pyAppGen/pbcs/payroll_engine","fragments":PAYROLL_ENGINE_UI_FRAGMENT_KEYS,"routes":tuple(i["route"] for i in shell["navigation"])+(shell["workbench_route"],),"panels":({"key":"run_console","fragment":"PayrollRunConsole","binds_to":("payroll_run","worker_projection","labor_hours"),"commands":("create_payroll_run","calculate_payslip","post_payroll_run")},{"key":"payslip_review","fragment":"PayslipReviewBoard","binds_to":("payslip","deduction","benefit_allocation"),"commands":("calculate_payslip","apply_deduction","allocate_benefit")},{"key":"filing_console","fragment":"PayrollFilingConsole","binds_to":("payroll_run","payslip","outbox"),"commands":("prepare_payroll_filing","generate_payroll_proof")},{"key":"governance_studio","fragment":"PayrollRuleStudio","binds_to":("rule","parameter","configuration"),"commands":("register_rule","set_parameter","configure_runtime","run_control_tests")}),"forms":payroll_engine_form_catalog(),"wizards":payroll_engine_wizard_catalog(),"controls":payroll_engine_control_catalog(),"standalone_app":shell,"action_permissions":payroll_engine_permissions_contract()["action_permissions"],"configuration_editor":{"required_fields":("database_backend","event_topic","retry_limit","default_currency"),"allowed_database_backends":PAYROLL_ENGINE_ALLOWED_DATABASE_BACKENDS,"required_event_topic":PAYROLL_ENGINE_REQUIRED_EVENT_TOPIC,"event_contract":"AppGen-X","stream_engine_picker_visible":False,"user_selectable_event_contract":False},"parameter_editor":{"numeric_parameters":("standard_period_hours","overtime_multiplier","supplemental_rate","net_pay_floor","approval_amount_threshold"),"bounded_supported_parameters":True},"rule_editor":{"rule_types":("pay","deduction","benefit","approval","filing","off_cycle"),"required_fields":("rule_id","tenant","rule_type","eligible_worker_types","allowed_countries","status"),"compiled_evidence_required":True},"event_surfaces":{"emits":("PayrollPosted","PayrollFilingPrepared"),"consumes":("LaborHoursApproved","TaxCalculated"),"outbox_status":"visible","inbox_status":"visible","dead_letter_status":"visible"},"binding_evidence":{"owned_tables":PAYROLL_ENGINE_OWNED_TABLES,"outbox_table":"payroll_engine_appgen_outbox_event","inbox_table":"payroll_engine_appgen_inbox_event","dead_letter_table":"payroll_engine_dead_letter_event","shared_table_access":False,"required_event_topic":PAYROLL_ENGINE_REQUIRED_EVENT_TOPIC,"rbac_permissions":payroll_engine_permissions_contract()["permissions"]}}
def payroll_engine_render_workbench(state:dict,*,tenant:str,principal_permissions:tuple[str,...])->dict:
 contract=payroll_engine_ui_contract(); snapshot=__import__("pyAppGen.pbcs.payroll_engine.runtime",fromlist=["payroll_engine_build_workbench_view"]).payroll_engine_build_workbench_view(state,tenant=tenant); perms=set(principal_permissions); visible=tuple(a for a,p in contract["action_permissions"].items() if p in perms); return {"format":"appgen.payroll-engine-workbench-render.v1","ok":True,"tenant":tenant,"route":"/workbench/pbcs/payroll_engine","fragments":contract["fragments"],"navigation":contract["standalone_app"]["navigation"],"forms":contract["forms"],"wizards":contract["wizards"],"controls":contract["controls"],"cards":({"key":"payroll_runs","value":snapshot["run_count"],"fragment":"PayrollRunConsole"},{"key":"gross_pay_total","value":snapshot["gross_pay_total"],"fragment":"PayslipReviewBoard"},{"key":"net_pay_total","value":snapshot["net_pay_total"],"fragment":"PayslipReviewBoard"},{"key":"deductions","value":snapshot["deduction_count"],"fragment":"DeductionEditor"},{"key":"benefits","value":snapshot["benefit_count"],"fragment":"BenefitAllocationPanel"},{"key":"filings","value":snapshot["filing_count"],"fragment":"PayrollFilingConsole"}),"visible_actions":visible,"locked_actions":tuple(a for a in contract["action_permissions"] if a not in visible),"configuration_bound":snapshot["configuration_bound"],"rules_bound":tuple(sorted(state.get("rules",{}))),"parameters_bound":tuple(sorted(state.get("parameters",{}))),"event_outbox_count":len(state.get("outbox",())),"inbox_count":snapshot["inbox_count"],"dead_letter_count":snapshot["dead_letter_count"],"binding_evidence":contract["binding_evidence"],"workbench":snapshot}
def payroll_engine_render_standalone_app(state:dict,*,tenant:str,principal_permissions:tuple[str,...]|None=None)->dict:
 contract=payroll_engine_ui_contract(); perms=principal_permissions or tuple(sorted(set(contract["action_permissions"].values()))); rendered=payroll_engine_render_workbench(state,tenant=tenant,principal_permissions=perms); return {"ok":rendered["ok"],"pbc":"payroll_engine","shell":payroll_engine_standalone_app_contract(),"workbench":rendered,"side_effects":()}
