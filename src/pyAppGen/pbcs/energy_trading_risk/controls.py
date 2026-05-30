"""Package-local controls for the Energy Trading and Risk workbench."""

from __future__ import annotations

from .runtime import energy_trading_risk_build_release_evidence
from .runtime import energy_trading_risk_empty_state
from .runtime import energy_trading_risk_runtime_smoke
from .runtime import energy_trading_risk_verify_owned_table_boundary
from .risk_engine import build_workbench_summary


ENERGY_TRADING_RISK_CONTROLS = (
    {
        "control_id": "trade_capture_safety_case",
        "title": "Trade capture safety case",
        "description": "Blocks trades missing book, strategy, delivery, pricing, counterparty, or approval evidence.",
        "permission": "energy_trading_risk.create",
    },
    {
        "control_id": "net_exposure_monitor",
        "title": "Net exposure monitor",
        "description": "Tracks bucketed net exposure and projected MTM by commodity, hub, tenor, and book.",
        "permission": "energy_trading_risk.read",
    },
    {
        "control_id": "nomination_cutoff_monitor",
        "title": "Nomination cutoff monitor",
        "description": "Flags post-cutoff nominations and lineage exceptions.",
        "permission": "energy_trading_risk.update",
    },
    {
        "control_id": "curve_quality_gate",
        "title": "Curve quality gate",
        "description": "Verifies curve freshness and price boundaries before mark-to-market or limit review.",
        "permission": "energy_trading_risk.admin",
    },
    {
        "control_id": "release_readiness",
        "title": "Release readiness",
        "description": "Collects release evidence, boundary proofs, and app-surface readiness.",
        "permission": "energy_trading_risk.admin",
    },
)



def energy_trading_risk_control_catalog() -> dict:
    return {
        "ok": bool(ENERGY_TRADING_RISK_CONTROLS),
        "pbc": "energy_trading_risk",
        "controls": ENERGY_TRADING_RISK_CONTROLS,
        "control_ids": tuple(item["control_id"] for item in ENERGY_TRADING_RISK_CONTROLS),
        "side_effects": (),
    }



def energy_trading_risk_control_center(state: dict | None = None) -> dict:
    source_state = state or energy_trading_risk_runtime_smoke()["state"]
    trades = tuple(source_state.get("trade_positions", {}).values())
    nominations = tuple(source_state.get("nominations", {}).values())
    schedules = tuple(source_state.get("schedules", {}).values())
    settlements = tuple(source_state.get("settlements", {}).values())
    curves = tuple(source_state.get("market_price_curves", {}).values())
    limits = tuple(source_state.get("exposure_limits", {}).values())
    release = energy_trading_risk_build_release_evidence()
    summary = build_workbench_summary(trades, nominations, schedules, settlements, curves, limits)
    accepted_boundary = energy_trading_risk_verify_owned_table_boundary(("trade_position", "nomination", "market_price_curve"))
    rejected_boundary = energy_trading_risk_verify_owned_table_boundary(("foreign_shared_table",))
    curve_gate = {
        "fresh_curves": summary["stale_curves"] == 0,
        "stale_curve_count": summary["stale_curves"],
    }
    safety_case = {
        "blocked_trades": summary["blocked_trades"],
        "ready_trades": summary["ready_trades"],
    }
    nomination_monitor = {
        "nomination_exceptions": summary["nomination_exceptions"],
        "schedule_exceptions": summary["schedule_exceptions"],
    }
    return {
        "ok": release["ok"] and accepted_boundary["ok"] and not rejected_boundary["ok"],
        "pbc": "energy_trading_risk",
        "controls": energy_trading_risk_control_catalog()["controls"],
        "release": release,
        "summary": summary,
        "safety_case": safety_case,
        "curve_gate": curve_gate,
        "nomination_monitor": nomination_monitor,
        "accepted_boundary": accepted_boundary,
        "rejected_boundary": rejected_boundary,
        "side_effects": (),
    }



def energy_trading_risk_mutation_preview(action: str, table: str, payload: dict | None = None) -> dict:
    normalized = str(action).lower()
    boundary = energy_trading_risk_verify_owned_table_boundary((table,))
    return {
        "ok": boundary["ok"] and normalized in {"create", "read", "update", "delete"},
        "pbc": "energy_trading_risk",
        "action": normalized,
        "table": table,
        "payload_keys": tuple(sorted(dict(payload or {}))),
        "requires_confirmation": normalized != "read",
        "boundary": boundary,
        "side_effects": (),
    }



def smoke_test() -> dict:
    preview = energy_trading_risk_mutation_preview("read", "trade_position", {})
    control_center = energy_trading_risk_control_center(energy_trading_risk_empty_state() | energy_trading_risk_runtime_smoke()["state"])
    return {"ok": preview["ok"] and control_center["ok"], "preview": preview, "control_center": control_center, "side_effects": ()}
