"""Standalone models and sqlite harness for wealth_portfolio_management."""
from __future__ import annotations

import hashlib
import json
import sqlite3
import tempfile
import uuid
from datetime import datetime, timezone
from pathlib import Path

from .runtime import (
    PBC_KEY,
    WEALTH_PORTFOLIO_MANAGEMENT_ALLOWED_DATABASE_BACKENDS,
    WEALTH_PORTFOLIO_MANAGEMENT_CONSUMED_EVENT_TYPES,
    WEALTH_PORTFOLIO_MANAGEMENT_EMITTED_EVENT_TYPES,
    WEALTH_PORTFOLIO_MANAGEMENT_REQUIRED_EVENT_TOPIC,
    wealth_portfolio_management_build_schema_contract,
)

OWNED_BUSINESS_TABLES = (
    "wealth_portfolio_management_client_portfolio",
    "wealth_portfolio_management_investment_mandate",
    "wealth_portfolio_management_suitability_profile",
    "wealth_portfolio_management_rebalance_order",
    "wealth_portfolio_management_performance_snapshot",
    "wealth_portfolio_management_fee_schedule",
    "wealth_portfolio_management_advisory_review",
)
STANDALONE_ONLY_TABLES = (
    "wealth_portfolio_management_document_package",
    "wealth_portfolio_management_compliance_surveillance",
)
BUSINESS_TABLES = OWNED_BUSINESS_TABLES + STANDALONE_ONLY_TABLES
EVENT_TABLES = (
    "wealth_portfolio_management_appgen_outbox_event",
    "wealth_portfolio_management_appgen_inbox_event",
    "wealth_portfolio_management_appgen_dead_letter_event",
)
ALL_STANDALONE_TABLES = BUSINESS_TABLES + EVENT_TABLES
RISK_BAND_ORDER = {
    "capital_preservation": 0,
    "conservative": 1,
    "moderate": 2,
    "growth": 3,
    "aggressive": 4,
}


def model_contracts():
    return wealth_portfolio_management_build_schema_contract()["models"]


def standalone_model_contract() -> dict:
    return {
        "ok": True,
        "pbc": PBC_KEY,
        "business_tables": BUSINESS_TABLES,
        "event_tables": EVENT_TABLES,
        "deployment_database_backends": WEALTH_PORTFOLIO_MANAGEMENT_ALLOWED_DATABASE_BACKENDS,
        "local_dev_harness_backend": "sqlite",
        "event_contract": "AppGen-X",
        "required_event_topic": WEALTH_PORTFOLIO_MANAGEMENT_REQUIRED_EVENT_TOPIC,
        "stream_engine_picker_visible": False,
        "shared_table_access": False,
        "side_effects": (),
    }


def _now() -> str:
    return datetime.now(timezone.utc).isoformat()


def _dumps(value) -> str:
    return json.dumps(value, sort_keys=True)


def _loads(value: str | None):
    return json.loads(value) if value else {}


def _digest(value) -> str:
    return hashlib.sha256(repr(value).encode("utf-8")).hexdigest()


def _as_float(value, default: float = 0.0) -> float:
    try:
        return float(value)
    except (TypeError, ValueError):
        return default


def _risk_band_value(label: str | None) -> int:
    return RISK_BAND_ORDER.get(str(label or "").lower(), 0)


def _asset_totals(holdings: list[dict], cash_balance: float) -> tuple[dict[str, float], float]:
    totals: dict[str, float] = {}
    invested = 0.0
    for holding in holdings:
        asset_class = str(holding.get("asset_class") or "other")
        market_value = _as_float(holding.get("market_value"))
        invested += market_value
        totals[asset_class] = totals.get(asset_class, 0.0) + market_value
    if cash_balance > 0:
        totals["cash"] = totals.get("cash", 0.0) + cash_balance
    return totals, invested + max(cash_balance, 0.0)


def _calculate_drift(holdings: list[dict], targets: dict, cash_balance: float, tolerance: float) -> dict:
    totals, denominator = _asset_totals(holdings, cash_balance)
    denominator = denominator or 1.0
    rows = []
    max_abs_drift = 0.0
    breached = False
    for asset_class in sorted(set(totals) | set(targets)):
        actual_weight = totals.get(asset_class, 0.0) / denominator
        target_weight = _as_float(targets.get(asset_class))
        drift = actual_weight - target_weight
        max_abs_drift = max(max_abs_drift, abs(drift))
        row = {
            "asset_class": asset_class,
            "actual_weight": round(actual_weight, 4),
            "target_weight": round(target_weight, 4),
            "drift": round(drift, 4),
            "breached": abs(drift) > tolerance,
        }
        breached = breached or row["breached"]
        rows.append(row)
    return {
        "rows": tuple(rows),
        "max_abs_drift": round(max_abs_drift, 4),
        "breached": breached,
        "tolerance": tolerance,
    }


def _restriction_conflicts(holdings: list[dict], restrictions: list[dict]) -> tuple[dict, ...]:
    conflicts = []
    for holding in holdings:
        for restriction in restrictions:
            restriction_type = str(restriction.get("type") or "").lower()
            value = str(restriction.get("value") or "").lower()
            severity = str(restriction.get("severity") or "soft").lower()
            hit = False
            if restriction_type == "security" and value == str(holding.get("security") or "").lower():
                hit = True
            if restriction_type == "asset_class" and value == str(holding.get("asset_class") or "").lower():
                hit = True
            if restriction_type == "sector" and value == str(holding.get("sector") or "").lower():
                hit = True
            if restriction_type == "geography" and value == str(holding.get("geography") or "").lower():
                hit = True
            if hit:
                conflicts.append(
                    {
                        "security": holding.get("security"),
                        "asset_class": holding.get("asset_class"),
                        "restriction": dict(restriction),
                        "severity": severity,
                    }
                )
    return tuple(conflicts)


def _tax_lot_summary(holdings: list[dict]) -> dict:
    lot_count = 0
    unrealized_gain = 0.0
    unrealized_loss = 0.0
    wash_sale_candidates = []
    for holding in holdings:
        for lot in holding.get("tax_lots", ()):
            lot_count += 1
            market_value = _as_float(lot.get("market_value", holding.get("market_value")))
            cost_basis = _as_float(lot.get("cost_basis", holding.get("cost_basis")))
            pnl = market_value - cost_basis
            if pnl >= 0:
                unrealized_gain += pnl
            else:
                unrealized_loss += abs(pnl)
                if _as_float(lot.get("days_held")) < 31 or lot.get("recent_sale"):
                    wash_sale_candidates.append(
                        {
                            "security": holding.get("security"),
                            "lot_id": lot.get("lot_id"),
                            "days_held": lot.get("days_held"),
                        }
                    )
    return {
        "lot_count": lot_count,
        "unrealized_gain": round(unrealized_gain, 2),
        "unrealized_loss": round(unrealized_loss, 2),
        "wash_sale_candidates": tuple(wash_sale_candidates),
    }


def _fee_projection(assets: float, fee_schedule: dict) -> dict:
    advisory_fee_bps = _as_float(fee_schedule.get("advisory_fee_bps"), 100.0)
    annual_fee = round(assets * advisory_fee_bps / 10000.0, 2)
    quarterly_fee = round(annual_fee / 4.0, 2)
    return {
        "advisory_fee_bps": advisory_fee_bps,
        "annual_fee": annual_fee,
        "quarterly_fee": quarterly_fee,
        "billing_frequency": fee_schedule.get("billing_frequency", "quarterly"),
    }


class WealthPortfolioManagementStandaloneStore:
    """Package-local sqlite store for one-PBC wealth portfolio workflows."""

    def __init__(self, database_path: str = ":memory:") -> None:
        self._tempdir: tempfile.TemporaryDirectory[str] | None = None
        self.database_path = database_path
        if database_path == "":
            self._tempdir = tempfile.TemporaryDirectory(prefix="wealth-portfolio-management-")
            self.database_path = str(Path(self._tempdir.name) / "wealth_portfolio_management.sqlite3")
        self.connection = sqlite3.connect(self.database_path)
        self.connection.row_factory = sqlite3.Row
        self._create_schema()

    def close(self) -> None:
        self.connection.close()
        if self._tempdir is not None:
            self._tempdir.cleanup()

    def _create_schema(self) -> None:
        for table in BUSINESS_TABLES:
            self.connection.execute(
                f"""
                CREATE TABLE IF NOT EXISTS {table} (
                    id TEXT PRIMARY KEY,
                    tenant TEXT NOT NULL,
                    code TEXT NOT NULL,
                    status TEXT NOT NULL,
                    payload TEXT NOT NULL,
                    created_at TEXT NOT NULL,
                    updated_at TEXT NOT NULL
                )
                """
            )
        for table in EVENT_TABLES:
            self.connection.execute(
                f"""
                CREATE TABLE IF NOT EXISTS {table} (
                    event_id TEXT PRIMARY KEY,
                    tenant TEXT NOT NULL,
                    event_type TEXT NOT NULL,
                    payload TEXT NOT NULL,
                    idempotency_key TEXT NOT NULL UNIQUE,
                    status TEXT NOT NULL,
                    created_at TEXT NOT NULL
                )
                """
            )
        self.connection.commit()

    def _fetch_record(self, table: str, record_id: str) -> dict | None:
        row = self.connection.execute(
            f"SELECT id, tenant, code, status, payload, created_at, updated_at FROM {table} WHERE id = ?",
            (record_id,),
        ).fetchone()
        if row is None:
            return None
        return {
            "id": row["id"],
            "tenant": row["tenant"],
            "code": row["code"],
            "status": row["status"],
            "payload": _loads(row["payload"]),
            "created_at": row["created_at"],
            "updated_at": row["updated_at"],
        }

    def _fetch_latest_by_code(self, table: str, code: str) -> dict | None:
        row = self.connection.execute(
            f"SELECT id, tenant, code, status, payload, created_at, updated_at FROM {table} WHERE code = ? ORDER BY updated_at DESC, created_at DESC LIMIT 1",
            (code,),
        ).fetchone()
        if row is None:
            return None
        return {
            "id": row["id"],
            "tenant": row["tenant"],
            "code": row["code"],
            "status": row["status"],
            "payload": _loads(row["payload"]),
            "created_at": row["created_at"],
            "updated_at": row["updated_at"],
        }

    def _fetch_all(self, table: str, tenant: str | None = None, code: str | None = None) -> list[dict]:
        clauses = []
        params: list[str] = []
        if tenant is not None:
            clauses.append("tenant = ?")
            params.append(tenant)
        if code is not None:
            clauses.append("code = ?")
            params.append(code)
        where = f" WHERE {' AND '.join(clauses)}" if clauses else ""
        rows = self.connection.execute(
            f"SELECT id, tenant, code, status, payload, created_at, updated_at FROM {table}{where} ORDER BY updated_at DESC, created_at DESC",
            tuple(params),
        ).fetchall()
        return [
            {
                "id": row["id"],
                "tenant": row["tenant"],
                "code": row["code"],
                "status": row["status"],
                "payload": _loads(row["payload"]),
                "created_at": row["created_at"],
                "updated_at": row["updated_at"],
            }
            for row in rows
        ]

    def _write_record(self, table: str, record_id: str, tenant: str, code: str, status: str, payload: dict) -> dict:
        timestamp = _now()
        existing = self._fetch_record(table, record_id)
        created_at = existing["created_at"] if existing else timestamp
        self.connection.execute(
            f"""
            INSERT INTO {table} (id, tenant, code, status, payload, created_at, updated_at)
            VALUES (?, ?, ?, ?, ?, ?, ?)
            ON CONFLICT(id) DO UPDATE SET
                tenant = excluded.tenant,
                code = excluded.code,
                status = excluded.status,
                payload = excluded.payload,
                updated_at = excluded.updated_at
            """,
            (record_id, tenant, code, status, _dumps(payload), created_at, timestamp),
        )
        self.connection.commit()
        return self._fetch_record(table, record_id) or {}

    def _record_event(self, table: str, tenant: str, event_type: str, payload: dict, *, status: str, idempotency_key: str | None = None) -> dict:
        key = idempotency_key or _digest((event_type, payload, table))
        existing = self.connection.execute(
            f"SELECT event_id, event_type, payload, idempotency_key, status FROM {table} WHERE idempotency_key = ?",
            (key,),
        ).fetchone()
        if existing is not None:
            return {
                "ok": True,
                "duplicate": True,
                "event_id": existing["event_id"],
                "event_type": existing["event_type"],
                "payload": _loads(existing["payload"]),
                "idempotency_key": existing["idempotency_key"],
                "status": existing["status"],
                "table": table,
            }
        event_id = uuid.uuid4().hex
        self.connection.execute(
            f"INSERT INTO {table} (event_id, tenant, event_type, payload, idempotency_key, status, created_at) VALUES (?, ?, ?, ?, ?, ?, ?)",
            (event_id, tenant, event_type, _dumps(payload), key, status, _now()),
        )
        self.connection.commit()
        return {
            "ok": True,
            "duplicate": False,
            "event_id": event_id,
            "event_type": event_type,
            "payload": dict(payload),
            "idempotency_key": key,
            "status": status,
            "table": table,
        }

    def create_client_portfolio(self, payload: dict) -> dict:
        portfolio_id = str(payload.get("portfolio_id") or payload.get("id") or uuid.uuid4().hex)
        tenant = str(payload.get("tenant") or "default")
        household = dict(payload.get("household") or {})
        client = dict(payload.get("client") or {})
        goals = list(payload.get("goals") or [])
        risk_tolerance = dict(payload.get("risk_tolerance") or {})
        accounts = list(payload.get("accounts") or [])
        holdings = list(payload.get("holdings") or [])
        restrictions = list(payload.get("restrictions") or [])
        cash_needs = dict(payload.get("cash_needs") or {})
        model_portfolio = dict(payload.get("model_portfolio") or {})
        actual_cash = round(sum(_as_float(account.get("cash")) for account in accounts), 2)
        holdings_value = round(sum(_as_float(holding.get("market_value")) for holding in holdings), 2)
        total_assets = round(actual_cash + holdings_value, 2)
        drift = _calculate_drift(holdings, dict(model_portfolio.get("targets") or {}), actual_cash, _as_float(model_portfolio.get("tolerance"), 0.05))
        restriction_conflicts = _restriction_conflicts(holdings, restrictions)
        cash_gap = round(max((_as_float(cash_needs.get("minimum_cash_reserve")) + _as_float(cash_needs.get("near_term_need"))) - actual_cash, 0.0), 2)
        tax_summary = _tax_lot_summary(holdings)
        required_documents = tuple(payload.get("required_documents") or ("ips_signed", "suitability_attestation"))
        record_payload = {
            "portfolio_id": portfolio_id,
            "household": household,
            "client": client,
            "goals": goals,
            "risk_tolerance": risk_tolerance,
            "accounts": accounts,
            "holdings": holdings,
            "model_portfolio": model_portfolio,
            "restrictions": restrictions,
            "cash_needs": cash_needs,
            "required_documents": required_documents,
            "summary": {
                "actual_cash": actual_cash,
                "holdings_value": holdings_value,
                "total_assets": total_assets,
                "goal_count": len(goals),
                "drift": drift,
                "restriction_conflicts": restriction_conflicts,
                "cash_gap": cash_gap,
                "tax_lots": tax_summary,
            },
        }
        record = self._write_record(OWNED_BUSINESS_TABLES[0], portfolio_id, tenant, portfolio_id, str(payload.get("status") or "onboarding"), record_payload)
        event = self._record_event(EVENT_TABLES[0], tenant, WEALTH_PORTFOLIO_MANAGEMENT_EMITTED_EVENT_TYPES[0], {"portfolio_id": portfolio_id, "status": record["status"], "total_assets": total_assets, "event_contract": "AppGen-X"}, status="pending")
        return {"ok": True, "portfolio_id": portfolio_id, "record": record, "event": event, "summary": record_payload["summary"], "side_effects": ()}

    def record_investment_mandate(self, payload: dict) -> dict:
        portfolio_id = str(payload.get("portfolio_id"))
        tenant = str(payload.get("tenant") or "default")
        record_id = str(payload.get("mandate_id") or uuid.uuid4().hex)
        model_portfolio = dict(payload.get("model_portfolio") or {})
        consent_evidence = tuple(payload.get("consent_evidence") or ())
        status = "approved" if consent_evidence else "draft"
        record_payload = {
            "portfolio_id": portfolio_id,
            "ips_name": payload.get("ips_name") or "Core household IPS",
            "benchmark": payload.get("benchmark") or "60_40_blend",
            "time_horizon_years": _as_float(payload.get("time_horizon_years"), 10),
            "liquidity_reserve": _as_float(payload.get("liquidity_reserve"), 0.05),
            "tax_treatment": payload.get("tax_treatment", "tax_sensitive"),
            "allowed_asset_classes": tuple(payload.get("allowed_asset_classes") or tuple(model_portfolio.get("targets", {}).keys())),
            "model_portfolio": model_portfolio,
            "consent_evidence": consent_evidence,
            "review_cycle_days": int(payload.get("review_cycle_days") or 180),
        }
        record = self._write_record(OWNED_BUSINESS_TABLES[1], record_id, tenant, portfolio_id, status, record_payload)
        event_type = WEALTH_PORTFOLIO_MANAGEMENT_EMITTED_EVENT_TYPES[2] if status == "approved" else WEALTH_PORTFOLIO_MANAGEMENT_EMITTED_EVENT_TYPES[1]
        event = self._record_event(EVENT_TABLES[0], tenant, event_type, {"portfolio_id": portfolio_id, "mandate_id": record_id, "status": status}, status="pending")
        return {"ok": True, "record": record, "event": event, "side_effects": ()}

    def record_suitability_profile(self, payload: dict) -> dict:
        portfolio_id = str(payload.get("portfolio_id"))
        tenant = str(payload.get("tenant") or "default")
        record_id = str(payload.get("suitability_id") or uuid.uuid4().hex)
        required_fields = ("knowledge_level", "experience_years", "liquidity_needs", "time_horizon_years", "risk_capacity")
        missing = tuple(field for field in required_fields if payload.get(field) in (None, "", ()))
        tolerance_band = str(payload.get("risk_tolerance_band") or "moderate").lower()
        capacity_band = str(payload.get("risk_capacity") or "conservative").lower()
        mismatch = _risk_band_value(tolerance_band) > _risk_band_value(capacity_band)
        status = "approved" if not missing and not mismatch else "needs_review"
        record_payload = {
            "portfolio_id": portfolio_id,
            "risk_tolerance_band": tolerance_band,
            "risk_capacity": capacity_band,
            "knowledge_level": payload.get("knowledge_level"),
            "experience_years": payload.get("experience_years"),
            "liquidity_needs": payload.get("liquidity_needs"),
            "time_horizon_years": payload.get("time_horizon_years"),
            "advisor_attestation": bool(payload.get("advisor_attestation", True)),
            "missing_fields": missing,
            "risk_mismatch": mismatch,
            "override_rationale": payload.get("override_rationale"),
        }
        record = self._write_record(OWNED_BUSINESS_TABLES[2], record_id, tenant, portfolio_id, status, record_payload)
        event_type = WEALTH_PORTFOLIO_MANAGEMENT_EMITTED_EVENT_TYPES[1] if status == "approved" else WEALTH_PORTFOLIO_MANAGEMENT_EMITTED_EVENT_TYPES[3]
        event = self._record_event(EVENT_TABLES[0], tenant, event_type, {"portfolio_id": portfolio_id, "suitability_id": record_id, "status": status}, status="pending")
        return {"ok": True, "record": record, "event": event, "side_effects": ()}

    def record_fee_schedule(self, payload: dict) -> dict:
        portfolio_id = str(payload.get("portfolio_id"))
        tenant = str(payload.get("tenant") or "default")
        record_id = str(payload.get("fee_schedule_id") or uuid.uuid4().hex)
        portfolio = self._fetch_record(OWNED_BUSINESS_TABLES[0], portfolio_id) or {}
        assets = _as_float((portfolio.get("payload") or {}).get("summary", {}).get("total_assets"))
        projection = _fee_projection(assets, payload)
        record_payload = {
            "portfolio_id": portfolio_id,
            "household_billing": bool(payload.get("household_billing", True)),
            "minimum_fee": _as_float(payload.get("minimum_fee"), 0.0),
            "waiver_reason": payload.get("waiver_reason"),
            "projection": projection,
        }
        record = self._write_record(OWNED_BUSINESS_TABLES[5], record_id, tenant, portfolio_id, "active", record_payload)
        event = self._record_event(EVENT_TABLES[0], tenant, WEALTH_PORTFOLIO_MANAGEMENT_EMITTED_EVENT_TYPES[1], {"portfolio_id": portfolio_id, "fee_schedule_id": record_id}, status="pending")
        return {"ok": True, "record": record, "projection": projection, "event": event, "side_effects": ()}

    def record_document_package(self, payload: dict) -> dict:
        portfolio_id = str(payload.get("portfolio_id"))
        tenant = str(payload.get("tenant") or "default")
        record_id = str(payload.get("document_package_id") or uuid.uuid4().hex)
        documents = tuple(payload.get("documents") or ())
        required = tuple(payload.get("required_documents") or ())
        present_types = {str(item.get("type")) for item in documents}
        missing_required = tuple(doc for doc in required if doc not in present_types)
        record_payload = {
            "portfolio_id": portfolio_id,
            "documents": documents,
            "required_documents": required,
            "missing_required": missing_required,
            "client_acknowledged": bool(payload.get("client_acknowledged", False)),
        }
        status = "complete" if not missing_required else "incomplete"
        record = self._write_record(STANDALONE_ONLY_TABLES[0], record_id, tenant, portfolio_id, status, record_payload)
        event = self._record_event(EVENT_TABLES[0], tenant, WEALTH_PORTFOLIO_MANAGEMENT_EMITTED_EVENT_TYPES[1], {"portfolio_id": portfolio_id, "document_package_id": record_id, "status": status}, status="pending")
        return {"ok": True, "record": record, "missing_required": missing_required, "event": event, "side_effects": ()}

    def generate_trade_proposal(self, payload: dict) -> dict:
        portfolio_id = str(payload.get("portfolio_id"))
        tenant = str(payload.get("tenant") or "default")
        record_id = str(payload.get("trade_proposal_id") or uuid.uuid4().hex)
        detail = self.build_portfolio_detail(portfolio_id)
        if not detail["ok"]:
            return {"ok": False, "reason": "unknown_portfolio", "portfolio_id": portfolio_id, "side_effects": ()}
        profile = detail["portfolio"]
        mandate = detail["mandate"] or {"payload": {}}
        suitability = detail["suitability"] or {"status": "missing"}
        holdings = list(profile["payload"].get("holdings", ()))
        accounts = list(profile["payload"].get("accounts", ()))
        actual_cash = round(sum(_as_float(account.get("cash")) for account in accounts), 2)
        targets = dict((mandate.get("payload") or {}).get("model_portfolio", {}).get("targets") or {})
        tolerance = _as_float((mandate.get("payload") or {}).get("model_portfolio", {}).get("tolerance"), 0.05)
        drift = _calculate_drift(holdings, targets, actual_cash, tolerance)
        restriction_conflicts = _restriction_conflicts(holdings, list(profile["payload"].get("restrictions", ())))
        cash_gap = _as_float(profile["payload"].get("summary", {}).get("cash_gap"))
        total_assets = _as_float(profile["payload"].get("summary", {}).get("total_assets"), 1.0)
        proposals = []
        for row in drift["rows"]:
            if not row["breached"]:
                continue
            proposals.append(
                {
                    "asset_class": row["asset_class"],
                    "action": "buy" if row["drift"] < 0 else "sell",
                    "trade_amount": round(abs(row["drift"]) * total_assets, 2),
                    "rationale": "rebalance_to_model_and_cash_policy",
                }
            )
        blockers = []
        if suitability.get("status") != "approved":
            blockers.append("suitability_incomplete_or_override_required")
        if any(item["restriction"].get("severity") == "hard" for item in restriction_conflicts):
            blockers.append("hard_restriction_conflict")
        if cash_gap > 0:
            blockers.append("cash_reserve_gap")
        status = "blocked" if blockers else "proposed"
        record_payload = {
            "portfolio_id": portfolio_id,
            "drift": drift,
            "tax_summary": _tax_lot_summary(holdings),
            "restriction_conflicts": restriction_conflicts,
            "trade_proposals": tuple(proposals),
            "cash_gap": cash_gap,
            "blockers": tuple(blockers),
            "advisor_rationale": payload.get("advisor_rationale"),
        }
        record = self._write_record(OWNED_BUSINESS_TABLES[3], record_id, tenant, portfolio_id, status, record_payload)
        event_type = WEALTH_PORTFOLIO_MANAGEMENT_EMITTED_EVENT_TYPES[3] if blockers else WEALTH_PORTFOLIO_MANAGEMENT_EMITTED_EVENT_TYPES[1]
        event = self._record_event(EVENT_TABLES[0], tenant, event_type, {"portfolio_id": portfolio_id, "trade_proposal_id": record_id, "status": status, "blockers": blockers}, status="pending")
        return {"ok": True, "record": record, "event": event, "side_effects": ()}

    def record_performance_snapshot(self, payload: dict) -> dict:
        portfolio_id = str(payload.get("portfolio_id"))
        tenant = str(payload.get("tenant") or "default")
        record_id = str(payload.get("performance_snapshot_id") or uuid.uuid4().hex)
        detail = self.build_portfolio_detail(portfolio_id)
        profile = detail.get("portfolio") or {"payload": {"summary": {}}}
        fee_schedule = detail.get("fee_schedule") or {"payload": {"projection": {}}}
        current_assets = _as_float(profile["payload"].get("summary", {}).get("total_assets"), 1.0)
        fees_paid = _as_float(payload.get("fees_paid"), _as_float((fee_schedule.get("payload") or {}).get("projection", {}).get("quarterly_fee")))
        beginning_value = _as_float(payload.get("beginning_value"), max(current_assets - 25000.0, 1.0))
        ending_value = _as_float(payload.get("ending_value"), current_assets)
        net_flows = _as_float(payload.get("net_flows"), 0.0)
        gross_return = round((ending_value - beginning_value - net_flows) / beginning_value, 4)
        net_return = round((ending_value - beginning_value - net_flows - fees_paid) / beginning_value, 4)
        record_payload = {
            "portfolio_id": portfolio_id,
            "benchmark": payload.get("benchmark") or (detail.get("mandate") or {"payload": {}})["payload"].get("benchmark", "60_40_blend"),
            "period": payload.get("period", "quarter_to_date"),
            "beginning_value": beginning_value,
            "ending_value": ending_value,
            "net_flows": net_flows,
            "fees_paid": fees_paid,
            "gross_return": gross_return,
            "net_return": net_return,
        }
        record = self._write_record(OWNED_BUSINESS_TABLES[4], record_id, tenant, portfolio_id, "final", record_payload)
        event = self._record_event(EVENT_TABLES[0], tenant, WEALTH_PORTFOLIO_MANAGEMENT_EMITTED_EVENT_TYPES[1], {"portfolio_id": portfolio_id, "performance_snapshot_id": record_id}, status="pending")
        return {"ok": True, "record": record, "event": event, "side_effects": ()}

    def record_advisor_review(self, payload: dict) -> dict:
        portfolio_id = str(payload.get("portfolio_id"))
        tenant = str(payload.get("tenant") or "default")
        record_id = str(payload.get("advisor_review_id") or uuid.uuid4().hex)
        document_package = self._fetch_latest_by_code(STANDALONE_ONLY_TABLES[0], portfolio_id)
        missing_docs = tuple((document_package or {"payload": {}})["payload"].get("missing_required", ()))
        recommendations = tuple(payload.get("recommendations") or ())
        findings = tuple(payload.get("findings") or ())
        status = "complete" if findings and not missing_docs else "pending"
        record_payload = {
            "portfolio_id": portfolio_id,
            "review_type": payload.get("review_type", "quarterly"),
            "client_contact_evidence": payload.get("client_contact_evidence"),
            "findings": findings,
            "recommendations": recommendations,
            "next_review_due": payload.get("next_review_due") or "2026-12-31",
            "missing_required_documents": missing_docs,
        }
        record = self._write_record(OWNED_BUSINESS_TABLES[6], record_id, tenant, portfolio_id, status, record_payload)
        event_type = WEALTH_PORTFOLIO_MANAGEMENT_EMITTED_EVENT_TYPES[2] if status == "complete" else WEALTH_PORTFOLIO_MANAGEMENT_EMITTED_EVENT_TYPES[1]
        event = self._record_event(EVENT_TABLES[0], tenant, event_type, {"portfolio_id": portfolio_id, "advisor_review_id": record_id, "status": status}, status="pending")
        return {"ok": True, "record": record, "event": event, "side_effects": ()}

    def run_compliance_surveillance(self, payload: dict) -> dict:
        portfolio_id = str(payload.get("portfolio_id"))
        tenant = str(payload.get("tenant") or "default")
        record_id = str(payload.get("surveillance_id") or uuid.uuid4().hex)
        detail = self.build_portfolio_detail(portfolio_id)
        if not detail["ok"]:
            return {"ok": False, "reason": "unknown_portfolio", "portfolio_id": portfolio_id, "side_effects": ()}
        alerts = []
        if detail["suitability"] and detail["suitability"]["status"] != "approved":
            alerts.append({"type": "suitability", "severity": "high", "message": "Suitability profile needs review before trading."})
        if detail["trade_proposal"] and detail["trade_proposal"]["status"] == "blocked":
            alerts.append({"type": "rebalancing", "severity": "high", "message": "Trade proposal is blocked by policy or cash constraints."})
        if detail["documents"] and detail["documents"]["status"] != "complete":
            alerts.append({"type": "documents", "severity": "medium", "message": "Required disclosures or attestations are missing."})
        if detail["summary"]["cash_gap"] > 0:
            alerts.append({"type": "cash_needs", "severity": "high", "message": "Minimum cash reserve is below required near-term need."})
        if detail["summary"]["max_drift"] > detail["summary"]["drift_tolerance"]:
            alerts.append({"type": "drift", "severity": "medium", "message": "Portfolio drift exceeds the mandate tolerance band."})
        record_payload = {
            "portfolio_id": portfolio_id,
            "alerts": tuple(alerts),
            "alert_count": len(alerts),
            "monitoring_scope": ("suitability", "restrictions", "cash_needs", "drift", "documents", "reviews"),
        }
        status = "clean" if not alerts else "exception_open"
        record = self._write_record(STANDALONE_ONLY_TABLES[1], record_id, tenant, portfolio_id, status, record_payload)
        event_type = WEALTH_PORTFOLIO_MANAGEMENT_EMITTED_EVENT_TYPES[2] if not alerts else WEALTH_PORTFOLIO_MANAGEMENT_EMITTED_EVENT_TYPES[3]
        event = self._record_event(EVENT_TABLES[0], tenant, event_type, {"portfolio_id": portfolio_id, "surveillance_id": record_id, "status": status, "alert_count": len(alerts)}, status="pending")
        return {"ok": True, "record": record, "alerts": tuple(alerts), "event": event, "side_effects": ()}

    def receive_event(self, event: dict) -> dict:
        tenant = str(event.get("tenant") or "default")
        event_type = str(event.get("event_type") or "")
        payload = dict(event.get("payload") or {})
        idempotency_key = event.get("idempotency_key") or event.get("event_id") or _digest(event)
        if event_type not in WEALTH_PORTFOLIO_MANAGEMENT_CONSUMED_EVENT_TYPES:
            dead = self._record_event(EVENT_TABLES[2], tenant, event_type or "UnknownEvent", payload, status="dead_letter", idempotency_key=idempotency_key)
            return {"ok": False, "duplicate": False, "dead_letter_table": EVENT_TABLES[2], "event": dead, "side_effects": ()}
        inbox = self._record_event(EVENT_TABLES[1], tenant, event_type, payload, status="processed", idempotency_key=idempotency_key)
        return {"ok": True, "duplicate": inbox.get("duplicate", False), "event": inbox, "side_effects": ()}

    def build_portfolio_detail(self, portfolio_id: str) -> dict:
        portfolio = self._fetch_record(OWNED_BUSINESS_TABLES[0], portfolio_id)
        if portfolio is None:
            return {"ok": False, "reason": "unknown_portfolio", "portfolio_id": portfolio_id, "side_effects": ()}
        mandate = self._fetch_latest_by_code(OWNED_BUSINESS_TABLES[1], portfolio_id)
        suitability = self._fetch_latest_by_code(OWNED_BUSINESS_TABLES[2], portfolio_id)
        trade_proposal = self._fetch_latest_by_code(OWNED_BUSINESS_TABLES[3], portfolio_id)
        performance = self._fetch_latest_by_code(OWNED_BUSINESS_TABLES[4], portfolio_id)
        fee_schedule = self._fetch_latest_by_code(OWNED_BUSINESS_TABLES[5], portfolio_id)
        advisor_review = self._fetch_latest_by_code(OWNED_BUSINESS_TABLES[6], portfolio_id)
        documents = self._fetch_latest_by_code(STANDALONE_ONLY_TABLES[0], portfolio_id)
        surveillance = self._fetch_latest_by_code(STANDALONE_ONLY_TABLES[1], portfolio_id)
        summary = dict(portfolio["payload"].get("summary", {}))
        summary.update(
            {
                "max_drift": _as_float(summary.get("drift", {}).get("max_abs_drift")),
                "drift_tolerance": _as_float(summary.get("drift", {}).get("tolerance"), 0.05),
                "open_alerts": len((surveillance or {"payload": {}})["payload"].get("alerts", ())),
                "missing_documents": tuple((documents or {"payload": {}})["payload"].get("missing_required", ())),
            }
        )
        return {
            "ok": True,
            "pbc": PBC_KEY,
            "portfolio_id": portfolio_id,
            "portfolio": portfolio,
            "mandate": mandate,
            "suitability": suitability,
            "trade_proposal": trade_proposal,
            "performance": performance,
            "fee_schedule": fee_schedule,
            "advisor_review": advisor_review,
            "documents": documents,
            "surveillance": surveillance,
            "summary": summary,
            "side_effects": (),
        }

    def build_workbench(self, tenant: str) -> dict:
        portfolios = self._fetch_all(OWNED_BUSINESS_TABLES[0], tenant=tenant)
        rows = [self.build_portfolio_detail(item["id"]) for item in portfolios]
        total_assets = round(sum(_as_float(row["summary"].get("total_assets")) for row in rows if row["ok"]), 2)
        open_alerts = sum(int(row["summary"].get("open_alerts", 0)) for row in rows if row["ok"])
        pending_rebalances = sum(1 for row in rows if row["ok"] and row.get("trade_proposal") and row["trade_proposal"]["status"] in {"proposed", "blocked"})
        return {
            "ok": True,
            "pbc": PBC_KEY,
            "tenant": tenant,
            "portfolio_count": len(rows),
            "total_assets": total_assets,
            "open_alert_count": open_alerts,
            "pending_rebalance_count": pending_rebalances,
            "portfolio_rows": tuple(
                {
                    "portfolio_id": row["portfolio_id"],
                    "client_name": row["portfolio"]["payload"].get("client", {}).get("display_name"),
                    "household_name": row["portfolio"]["payload"].get("household", {}).get("household_name"),
                    "total_assets": row["summary"].get("total_assets"),
                    "max_drift": row["summary"].get("max_drift"),
                    "cash_gap": row["summary"].get("cash_gap"),
                    "open_alerts": row["summary"].get("open_alerts"),
                }
                for row in rows
                if row["ok"]
            ),
            "side_effects": (),
        }


def standalone_store_smoke_test() -> dict:
    store = WealthPortfolioManagementStandaloneStore()
    try:
        portfolio = store.create_client_portfolio(
            {
                "portfolio_id": "portfolio-smoke",
                "tenant": "tenant-smoke",
                "household": {"household_name": "Smoke Household"},
                "client": {"display_name": "Smoke Client"},
                "goals": [{"name": "Retirement", "target_amount": 2500000}],
                "risk_tolerance": {"band": "moderate", "score": 64},
                "accounts": [{"account_id": "acct-1", "custodian": "Schwab", "cash": 125000}],
                "holdings": [{"security": "BND", "asset_class": "fixed_income", "market_value": 400000, "cost_basis": 390000, "tax_lots": [{"lot_id": "lot-1", "market_value": 400000, "cost_basis": 390000, "days_held": 365}]}],
                "model_portfolio": {"targets": {"fixed_income": 0.4, "cash": 0.05}, "tolerance": 0.05},
                "cash_needs": {"minimum_cash_reserve": 50000, "near_term_need": 10000},
            }
        )
        mandate = store.record_investment_mandate({"portfolio_id": "portfolio-smoke", "tenant": "tenant-smoke", "consent_evidence": ("signed_pdf",), "model_portfolio": {"targets": {"fixed_income": 0.4, "cash": 0.05}, "tolerance": 0.05}})
        suitability = store.record_suitability_profile({"portfolio_id": "portfolio-smoke", "tenant": "tenant-smoke", "knowledge_level": "advanced", "experience_years": 12, "liquidity_needs": "medium", "time_horizon_years": 15, "risk_tolerance_band": "moderate", "risk_capacity": "moderate"})
        fees = store.record_fee_schedule({"portfolio_id": "portfolio-smoke", "tenant": "tenant-smoke", "advisory_fee_bps": 85})
        documents = store.record_document_package({"portfolio_id": "portfolio-smoke", "tenant": "tenant-smoke", "required_documents": ("ips_signed",), "documents": ({"type": "ips_signed", "name": "IPS.pdf"},)})
        trade = store.generate_trade_proposal({"portfolio_id": "portfolio-smoke", "tenant": "tenant-smoke"})
        performance = store.record_performance_snapshot({"portfolio_id": "portfolio-smoke", "tenant": "tenant-smoke", "ending_value": 540000, "beginning_value": 500000, "fees_paid": 850})
        review = store.record_advisor_review({"portfolio_id": "portfolio-smoke", "tenant": "tenant-smoke", "findings": ("Portfolio aligned with goals",), "recommendations": ("Keep quarterly review cadence",)})
        surveillance = store.run_compliance_surveillance({"portfolio_id": "portfolio-smoke", "tenant": "tenant-smoke"})
        inbox = store.receive_event({"event_type": WEALTH_PORTFOLIO_MANAGEMENT_CONSUMED_EVENT_TYPES[0], "idempotency_key": "smoke-event", "tenant": "tenant-smoke", "payload": {"policy": "updated"}})
        workbench = store.build_workbench("tenant-smoke")
        detail = store.build_portfolio_detail("portfolio-smoke")
        checks = (portfolio, mandate, suitability, fees, documents, trade, performance, review, surveillance, inbox, workbench, detail)
        return {
            "ok": all(item["ok"] for item in checks),
            "checks": checks,
            "side_effects": (),
        }
    finally:
        store.close()
