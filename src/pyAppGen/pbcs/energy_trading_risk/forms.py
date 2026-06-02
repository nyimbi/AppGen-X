"""Package-local forms for the Energy Trading and Risk workbench."""

from __future__ import annotations


ENERGY_TRADING_RISK_FORM_DEFINITIONS = (
    {
        "form_id": "energy_trade_capture",
        "title": "Capture trade position",
        "route": "POST /trade-positions",
        "operation": "command_trade_position",
        "permission": "energy_trading_risk.create",
        "owned_tables": ("energy_trading_risk_trade_position",),
        "fields": (
            {"name": "tenant", "type": "string", "required": True},
            {"name": "commodity", "type": "enum", "required": True, "choices": ("power", "gas", "lng", "carbon")},
            {"name": "market_hub", "type": "string", "required": True},
            {"name": "book", "type": "string", "required": True},
            {"name": "trader", "type": "string", "required": True},
            {"name": "strategy", "type": "string", "required": True},
            {"name": "counterparty", "type": "string", "required": True},
            {"name": "side", "type": "enum", "required": True, "choices": ("BUY", "SELL")},
            {"name": "position_type", "type": "enum", "required": True, "choices": ("physical", "financial", "linked")},
            {"name": "delivery_start", "type": "date", "required": True},
            {"name": "delivery_end", "type": "date", "required": True},
            {"name": "delivery_profile", "type": "enum", "required": True, "choices": ("baseload", "peak", "offpeak", "shaped")},
            {"name": "pricing_formula", "type": "string", "required": True},
            {"name": "volume_mwh", "type": "number", "required": True},
            {"name": "fixed_price", "type": "number", "required": True},
            {"name": "submitted_at", "type": "datetime", "required": True},
            {"name": "approval_state", "type": "enum", "required": False, "choices": ("pending", "approved")},
        ),
    },
    {
        "form_id": "nomination_submission",
        "title": "Submit nomination",
        "route": "POST /nominations",
        "operation": "command_nomination",
        "permission": "energy_trading_risk.update",
        "owned_tables": ("energy_trading_risk_nomination",),
        "fields": (
            {"name": "tenant", "type": "string", "required": True},
            {"name": "trade_id", "type": "string", "required": True},
            {"name": "delivery_period", "type": "string", "required": True},
            {"name": "interval_start", "type": "datetime", "required": True},
            {"name": "interval_end", "type": "datetime", "required": True},
            {"name": "volume_mwh", "type": "number", "required": True},
            {"name": "submitted_at", "type": "datetime", "required": True},
            {"name": "operator", "type": "string", "required": True},
            {"name": "reason_code", "type": "string", "required": False},
        ),
    },
    {
        "form_id": "schedule_submission",
        "title": "Approve schedule",
        "route": "POST /schedules",
        "operation": "command_schedule",
        "permission": "energy_trading_risk.update",
        "owned_tables": ("energy_trading_risk_schedule",),
        "fields": (
            {"name": "tenant", "type": "string", "required": True},
            {"name": "nomination_id", "type": "string", "required": True},
            {"name": "trade_id", "type": "string", "required": True},
            {"name": "delivery_period", "type": "string", "required": True},
            {"name": "scheduled_volume_mwh", "type": "number", "required": True},
            {"name": "path_status", "type": "enum", "required": True, "choices": ("feasible", "manual_override")},
            {"name": "submitted_at", "type": "datetime", "required": True},
        ),
    },
    {
        "form_id": "price_curve_publish",
        "title": "Publish market curve",
        "route": "POST /energy-trading-risk/internal/market-curves",
        "operation": "command_market_price_curve",
        "permission": "energy_trading_risk.admin",
        "owned_tables": ("energy_trading_risk_market_price_curve",),
        "fields": (
            {"name": "tenant", "type": "string", "required": True},
            {"name": "commodity", "type": "enum", "required": True, "choices": ("power", "gas", "lng", "carbon")},
            {"name": "market_hub", "type": "string", "required": True},
            {"name": "delivery_period", "type": "string", "required": True},
            {"name": "strip_start", "type": "date", "required": True},
            {"name": "strip_end", "type": "date", "required": True},
            {"name": "curve_price", "type": "number", "required": True},
            {"name": "as_of", "type": "datetime", "required": True},
            {"name": "source_name", "type": "string", "required": True},
        ),
    },
    {
        "form_id": "exposure_limit_setup",
        "title": "Configure exposure limit",
        "route": "POST /energy-trading-risk/internal/exposure-limits",
        "operation": "command_exposure_limit",
        "permission": "energy_trading_risk.admin",
        "owned_tables": ("energy_trading_risk_exposure_limit",),
        "fields": (
            {"name": "tenant", "type": "string", "required": True},
            {"name": "commodity", "type": "string", "required": True},
            {"name": "market_hub", "type": "string", "required": True},
            {"name": "book", "type": "string", "required": True},
            {"name": "max_net_exposure_mwh", "type": "number", "required": True},
            {"name": "max_projected_mtm", "type": "number", "required": True},
            {"name": "severity", "type": "enum", "required": True, "choices": ("warning", "hard_stop")},
            {"name": "owner", "type": "string", "required": True},
            {"name": "effective_from", "type": "datetime", "required": True},
        ),
    },
    {
        "form_id": "settlement_capture",
        "title": "Record settlement",
        "route": "POST /settlements",
        "operation": "command_settlement",
        "permission": "energy_trading_risk.update",
        "owned_tables": ("energy_trading_risk_settlement",),
        "fields": (
            {"name": "tenant", "type": "string", "required": True},
            {"name": "trade_id", "type": "string", "required": True},
            {"name": "delivery_period", "type": "string", "required": True},
            {"name": "realized_volume_mwh", "type": "number", "required": True},
            {"name": "realized_price", "type": "number", "required": True},
            {"name": "settled_at", "type": "datetime", "required": True},
        ),
    },
)



def energy_trading_risk_form_catalog() -> dict:
    forms = tuple(ENERGY_TRADING_RISK_FORM_DEFINITIONS)
    return {
        "ok": bool(forms),
        "pbc": "energy_trading_risk",
        "forms": forms,
        "form_ids": tuple(item["form_id"] for item in forms),
        "side_effects": (),
    }



def energy_trading_risk_get_form(form_id: str) -> dict:
    form = next((item for item in ENERGY_TRADING_RISK_FORM_DEFINITIONS if item["form_id"] == form_id), None)
    return {"ok": form is not None, "pbc": "energy_trading_risk", "form": form, "side_effects": ()}



def energy_trading_risk_validate_form_payload(form_id: str, payload: dict | None = None) -> dict:
    form = energy_trading_risk_get_form(form_id).get("form")
    if form is None:
        return {"ok": False, "accepted": False, "reason": "unknown_form", "form_id": form_id, "side_effects": ()}
    supplied = dict(payload or {})
    missing = tuple(
        field["name"]
        for field in form["fields"]
        if field.get("required") and supplied.get(field["name"]) in {None, ""}
    )
    invalid_choices = tuple(
        field["name"]
        for field in form["fields"]
        if field.get("type") == "enum" and supplied.get(field["name"]) not in {None, *field.get("choices", ())}
    )
    return {
        "ok": not missing and not invalid_choices,
        "accepted": not missing and not invalid_choices,
        "pbc": "energy_trading_risk",
        "form_id": form_id,
        "missing": missing,
        "invalid_choices": invalid_choices,
        "payload_keys": tuple(sorted(supplied)),
        "side_effects": (),
    }



def smoke_test() -> dict:
    catalog = energy_trading_risk_form_catalog()
    validation = energy_trading_risk_validate_form_payload(
        "price_curve_publish",
        {
            "tenant": "tenant-smoke",
            "commodity": "power",
            "market_hub": "PJM",
            "delivery_period": "2026-06",
            "strip_start": "2026-06-01",
            "strip_end": "2026-06-30",
            "curve_price": 41.5,
            "as_of": "2026-05-29T08:00:00Z",
            "source_name": "ICE",
        },
    )
    return {"ok": catalog["ok"] and validation["ok"], "catalog": catalog, "validation": validation, "side_effects": ()}
