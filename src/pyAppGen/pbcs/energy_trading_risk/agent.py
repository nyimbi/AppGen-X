PBC_KEY = "energy_trading_risk"
OWNED_TABLES = (
    "energy_trading_risk_energy_contract",
    "energy_trading_risk_trade_position",
    "energy_trading_risk_nomination",
    "energy_trading_risk_schedule",
    "energy_trading_risk_settlement",
    "energy_trading_risk_exposure_limit",
    "energy_trading_risk_market_price_curve",
    "energy_trading_risk_energy_trading_risk_policy_rule",
    "energy_trading_risk_energy_trading_risk_runtime_parameter",
    "energy_trading_risk_energy_trading_risk_schema_extension",
    "energy_trading_risk_energy_trading_risk_control_assertion",
    "energy_trading_risk_energy_trading_risk_governed_model",
    "energy_trading_risk_appgen_outbox_event",
    "energy_trading_risk_appgen_inbox_event",
    "energy_trading_risk_appgen_dead_letter_event",
)



def agent_skill_manifest():
    skills = tuple(
        {
            "name": name,
            "scope": PBC_KEY,
            "description": f"{name} for {PBC_KEY}",
            "requires_confirmation_for_mutation": True,
            "uses_appgen_event_contract": True,
            "stream_engine_picker_visible": False,
        }
        for name in (
            f"{PBC_KEY}_guide_user",
            f"{PBC_KEY}_read_records",
            f"{PBC_KEY}_create_record",
            f"{PBC_KEY}_update_record",
            f"{PBC_KEY}_triage_risk_exceptions",
        )
    )
    return {"ok": True, "pbc": PBC_KEY, "skills": skills, "side_effects": ()}



def chatbot_interface_contract():
    return {
        "ok": True,
        "pbc": PBC_KEY,
        "entrypoint": f"/assistant/pbc/{PBC_KEY}",
        "single_agent_contribution": f"{PBC_KEY}_skills",
        "capabilities": (
            "task_guidance",
            "document_instruction_intake",
            "governed_datastore_crud",
            "mutation_preview",
            "operator_help",
        ),
        "side_effects": (),
    }



def assistant_help_manifest():
    return {
        "ok": True,
        "pbc": PBC_KEY,
        "topics": (
            "trade_capture_safety_case",
            "net_exposure_buckets",
            "nomination_cutoff_exceptions",
            "curve_quality_gate",
            "settlement_close_review",
        ),
        "suggested_prompts": (
            "Explain why this trade is blocked",
            "Show the next remediation step for this nomination",
            "Summarize the current net exposure buckets",
        ),
        "requires_confirmation_for_mutation": True,
        "event_contract": "AppGen-X",
        "side_effects": (),
    }



def build_operator_guidance(record=None, workbench=None):
    record = dict(record or {})
    workbench = dict(workbench or {})
    summary = workbench.get("summary", {}) if isinstance(workbench, dict) else {}
    remediation = tuple(record.get("actionable_remediation", ()) or ())
    if remediation:
        headline = "Record requires remediation before release."
        next_actions = remediation
    elif record.get("status") == "risk_passed":
        headline = "Trade is ready for supervised release."
        next_actions = ("Review the net exposure bucket.", "Confirm approval evidence.")
    elif summary:
        headline = f"Workbench has {summary.get('blocked_trades', 0)} blocked trades and {summary.get('nomination_exceptions', 0)} nomination exceptions."
        next_actions = ("Inspect the trade exception queue.", "Refresh curve quality controls.")
    else:
        headline = "Energy trading and risk workbench is ready for review."
        next_actions = ("Open the trade capture wizard.",)
    return {
        "ok": True,
        "pbc": PBC_KEY,
        "summary": headline,
        "next_actions": next_actions,
        "topics": assistant_help_manifest()["topics"],
        "record_id": record.get("id"),
        "side_effects": (),
    }



def document_instruction_plan(document, instruction):
    return {
        "ok": True,
        "pbc": PBC_KEY,
        "document_digest": str(abs(hash(document))),
        "instruction": instruction,
        "candidate_tables": OWNED_TABLES[:4],
        "requires_human_confirmation": True,
        "crud_preview": {"operation": "create", "event_contract": "AppGen-X"},
        "side_effects": (),
    }



def datastore_crud_plan(action, table=None, payload=None):
    target = table or OWNED_TABLES[0]
    short_names = tuple(name.removeprefix(f"{PBC_KEY}_") for name in OWNED_TABLES)
    if str(target) not in OWNED_TABLES and str(target) not in short_names:
        return {"ok": False, "reason": "foreign_table_rejected", "table": target, "side_effects": ()}
    normalized_table = target if str(target).startswith(f"{PBC_KEY}_") else f"{PBC_KEY}_{target}"
    return {
        "ok": True,
        "pbc": PBC_KEY,
        "action": action,
        "table": normalized_table,
        "payload": dict(payload or {}),
        "requires_confirmation": action in ("create", "update", "delete"),
        "event_contract": "AppGen-X",
        "side_effects": (),
    }



def composed_agent_contribution():
    namespace = f"{PBC_KEY}_skills"
    return {
        "ok": True,
        "pbc": PBC_KEY,
        "single_agent_skill_namespace": namespace,
        "dsl_tools": (namespace, f"{PBC_KEY}_crud", f"{PBC_KEY}_documents", f"{PBC_KEY}_operator_help"),
        "side_effects": (),
    }



def smoke_test():
    return {
        "ok": agent_skill_manifest()["ok"]
        and chatbot_interface_contract()["ok"]
        and assistant_help_manifest()["ok"]
        and build_operator_guidance({"id": "TRADE-1", "actionable_remediation": ("Populate missing field: strategy",)})["ok"]
        and document_instruction_plan("doc", "create")["ok"]
        and datastore_crud_plan("create")["ok"]
        and datastore_crud_plan("update", table="foreign_table")["ok"] is False
        and composed_agent_contribution()["ok"],
        "side_effects": (),
    }
