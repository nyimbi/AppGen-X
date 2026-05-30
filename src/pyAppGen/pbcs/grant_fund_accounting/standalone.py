"""Standalone one-PBC application surface for grant_fund_accounting."""
from __future__ import annotations
from dataclasses import dataclass, field
from hashlib import sha256
from typing import Any
from .agent import chatbot_interface_contract, composed_agent_contribution, datastore_crud_plan, document_instruction_plan
from .controls import control_catalog, evaluate_control
from .domain_depth import DOMAIN_OWNED_TABLES
from .forms import form_catalog
from .runtime import (
    GRANT_FUND_ACCOUNTING_ALLOWED_DATABASE_BACKENDS,
    GRANT_FUND_ACCOUNTING_REQUIRED_EVENT_TOPIC,
    grant_fund_accounting_build_api_contract,
    grant_fund_accounting_build_schema_contract,
    grant_fund_accounting_build_service_contract,
    grant_fund_accounting_configure_runtime,
    grant_fund_accounting_empty_state,
    grant_fund_accounting_permissions_contract,
    grant_fund_accounting_receive_event,
    grant_fund_accounting_register_rule,
    grant_fund_accounting_runtime_smoke,
    grant_fund_accounting_set_parameter,
)
from .ui import grant_fund_accounting_render_workbench, grant_fund_accounting_ui_contract
from .wizards import wizard_catalog
PBC_KEY = "grant_fund_accounting"
def _digest(value: Any) -> str: return sha256(repr(value).encode("utf-8")).hexdigest()

@dataclass
class GrantFundAccountingStandaloneApp:
    tenant: str = "tenant-grants-001"
    state: dict = field(default_factory=grant_fund_accounting_empty_state)
    awards: dict[str, dict] = field(default_factory=dict)
    restrictions: dict[str, dict] = field(default_factory=dict)
    budgets: dict[str, dict] = field(default_factory=dict)
    costs: dict[str, dict] = field(default_factory=dict)
    draws: dict[str, dict] = field(default_factory=dict)
    match_requirements: dict[str, dict] = field(default_factory=dict)
    match_contributions: dict[str, dict] = field(default_factory=dict)
    reports: dict[str, dict] = field(default_factory=dict)
    evidence: dict[str, dict] = field(default_factory=dict)
    exceptions: dict[str, dict] = field(default_factory=dict)

    def configure(self) -> dict:
        cfg = grant_fund_accounting_configure_runtime(self.state, {"database_backend": "postgresql", "event_topic": GRANT_FUND_ACCOUNTING_REQUIRED_EVENT_TOPIC})
        self.state = cfg["state"]
        for name, value in (("drawdown_lead_days", 7), ("match_warning_threshold", 0.9), ("reporting_warning_days", 14), ("retention_years", 7)):
            param = grant_fund_accounting_set_parameter(self.state, name, value); self.state = param["state"]
        for rule in (("allowable_cost_period_category", "cost"), ("match_not_double_counted", "match"), ("report_to_ledger_reconciles", "report"), ("closeout_requires_acceptance", "closeout")):
            registered = grant_fund_accounting_register_rule(self.state, {"rule_id": rule[0], "scope": rule[1], "effect": "block_on_failure"}); self.state = registered["state"]
        received = grant_fund_accounting_receive_event(self.state, {"event_type": "JournalPosted", "event_id": "journal-001"})
        self.state = received["state"]
        return {"ok": cfg["ok"] and received["ok"], "side_effects": ()}

    def activate_award(self, award_id: str, **payload: Any) -> dict:
        required = ("funder", "award_number", "period_start", "period_end", "funding_amount", "source_document_uri")
        missing = tuple(field for field in required if not payload.get(field))
        award = {"id": award_id, "tenant": self.tenant, "status": "blocked" if missing else "active", "missing_fields": missing, "funder": payload.get("funder"), "award_number": payload.get("award_number"), "period": (payload.get("period_start"), payload.get("period_end")), "funding_amount": payload.get("funding_amount", 0), "assistance_listing": payload.get("assistance_listing"), "source_document_uri": payload.get("source_document_uri"), "lifecycle": ("pre_award", "awarded", "active") if not missing else ("pre_award",)}
        self.awards[award_id] = award
        return {"ok": not missing, "award": award, "side_effects": ()}

    def define_restriction(self, restriction_id: str, award_id: str, restriction_type: str, clause: str) -> dict:
        restriction = {"id": restriction_id, "award_id": award_id, "restriction_type": restriction_type, "source_clause": clause, "effective": True, "release_criteria": "funder approval or closeout acceptance"}
        self.restrictions[restriction_id] = restriction
        return {"ok": award_id in self.awards and bool(clause), "restriction": restriction, "side_effects": ()}

    def approve_budget(self, budget_id: str, award_id: str, lines: tuple[dict, ...], version: int = 1) -> dict:
        total = sum(line.get("amount", 0) for line in lines)
        award = self.awards[award_id]
        budget = {"id": budget_id, "award_id": award_id, "version": version, "lines": lines, "total": total, "status": "approved" if total <= award["funding_amount"] else "blocked", "burn_rate_warning": False}
        self.budgets[budget_id] = budget
        return {"ok": budget["status"] == "approved", "budget": budget, "side_effects": ()}

    def record_cost(self, cost_id: str, award_id: str, budget_id: str, category: str, amount: float, evidence_uri: str | None = None, paid: bool = True) -> dict:
        award = self.awards[award_id]; budget = self.budgets[budget_id]
        category_limit = sum(line.get("amount", 0) for line in budget["lines"] if line.get("category") == category)
        existing = sum(cost["amount"] for cost in self.costs.values() if cost["award_id"] == award_id and cost["category"] == category and cost["allowable"])
        blockers = []
        if award["status"] != "active": blockers.append("award_not_active")
        if not evidence_uri: blockers.append("missing_evidence")
        if existing + amount > category_limit: blockers.append("budget_exceeded")
        cost = {"id": cost_id, "award_id": award_id, "budget_id": budget_id, "category": category, "amount": amount, "paid": paid, "evidence_uri": evidence_uri, "allowable": not blockers, "blockers": tuple(blockers)}
        self.costs[cost_id] = cost
        if blockers: self.exceptions[f"EX-{cost_id}"] = {"type": "unallowable_cost", "cost_id": cost_id, "blockers": tuple(blockers), "status": "open"}
        return {"ok": not blockers, "cost": cost, "side_effects": ()}

    def prepare_drawdown(self, draw_id: str, award_id: str, cost_ids: tuple[str, ...]) -> dict:
        selected = tuple(self.costs[cid] for cid in cost_ids)
        blockers = tuple(cost["id"] for cost in selected if not cost["allowable"] or not cost["paid"])
        draw = {"id": draw_id, "award_id": award_id, "cost_ids": cost_ids, "requested_amount": sum(cost["amount"] for cost in selected if cost["id"] not in blockers), "status": "blocked" if blockers else "ready", "blocked_costs": blockers, "cash_simulation": {"lead_days": 7, "shortfall_risk": "low" if not blockers else "high"}}
        self.draws[draw_id] = draw
        return {"ok": not blockers, "drawdown": draw, "side_effects": ()}

    def track_match_requirement(self, requirement_id: str, award_id: str, amount: float) -> dict:
        req = {"id": requirement_id, "award_id": award_id, "required_amount": amount, "satisfied_amount": 0, "status": "shortfall"}
        self.match_requirements[requirement_id] = req
        return {"ok": True, "match_requirement": req, "side_effects": ()}

    def record_match_contribution(self, contribution_id: str, requirement_id: str, amount: float, evidence_uri: str, valuation_method: str = "cash") -> dict:
        double_counted = any(item.get("evidence_uri") == evidence_uri for item in self.match_contributions.values())
        contribution = {"id": contribution_id, "requirement_id": requirement_id, "amount": amount, "evidence_uri": evidence_uri, "valuation_method": valuation_method, "double_counted": double_counted, "eligible": not double_counted and bool(evidence_uri)}
        self.match_contributions[contribution_id] = contribution
        req = self.match_requirements[requirement_id]
        if contribution["eligible"]: req["satisfied_amount"] += amount
        req["status"] = "satisfied" if req["satisfied_amount"] >= req["required_amount"] else "shortfall"
        return {"ok": contribution["eligible"], "contribution": contribution, "requirement": req, "side_effects": ()}

    def build_report(self, report_id: str, award_id: str, draw_ids: tuple[str, ...], match_requirement_id: str) -> dict:
        draws = tuple(self.draws[did] for did in draw_ids)
        match = self.match_requirements[match_requirement_id]
        blockers = []
        if any(draw["status"] != "ready" for draw in draws): blockers.append("draw_not_ready")
        if match["status"] != "satisfied": blockers.append("match_shortfall")
        report = {"id": report_id, "award_id": award_id, "draw_ids": draw_ids, "match_requirement_id": match_requirement_id, "total_reported": sum(draw["requested_amount"] for draw in draws), "status": "blocked" if blockers else "ready_for_submission", "blockers": tuple(blockers), "variance_explanations": ()}
        self.reports[report_id] = report
        return {"ok": not blockers, "report": report, "side_effects": ()}

    def attach_evidence(self, evidence_id: str, award_id: str, document_type: str, source_uri: str) -> dict:
        record = {"id": evidence_id, "award_id": award_id, "document_type": document_type, "source_uri": source_uri, "retention_years": 7, "reviewer": "grant_controller", "cryptographic_proof": _digest((award_id, document_type, source_uri))}
        self.evidence[evidence_id] = record
        return {"ok": True, "evidence": record, "side_effects": ()}

    def close_grant(self, closeout_id: str, award_id: str, report_id: str) -> dict:
        report = self.reports[report_id]
        evidence_ok = any(item["award_id"] == award_id for item in self.evidence.values())
        closeout = {"id": closeout_id, "award_id": award_id, "report_id": report_id, "status": "closed" if report["status"] == "ready_for_submission" and evidence_ok else "blocked", "funder_acceptance": report["status"] == "ready_for_submission" and evidence_ok}
        return {"ok": closeout["status"] == "closed", "closeout": closeout, "side_effects": ()}

    def assistant_award_preview(self, document: str, instruction: str) -> dict:
        plan = document_instruction_plan(document, instruction)
        crud = datastore_crud_plan("create", table=f"{PBC_KEY}_grant_award", payload={"instruction": instruction})
        return {"ok": plan["ok"] and crud["ok"], "document_plan": plan, "crud_preview": crud, "requires_confirmation": True, "side_effects": ()}

    def app_contract(self) -> dict:
        return {"format": "appgen.grant-fund-accounting.standalone-app.v1", "ok": True, "pbc": PBC_KEY, "owned_tables": tuple(dict.fromkeys(DOMAIN_OWNED_TABLES)), "database_backends": GRANT_FUND_ACCOUNTING_ALLOWED_DATABASE_BACKENDS, "event_contract": "AppGen-X", "stream_engine_picker_visible": False, "schema": grant_fund_accounting_build_schema_contract(), "services": grant_fund_accounting_build_service_contract(), "routes": grant_fund_accounting_build_api_contract(), "permissions": grant_fund_accounting_permissions_contract(), "ui": grant_fund_accounting_ui_contract(), "workbench": grant_fund_accounting_render_workbench(), "forms": form_catalog(), "wizards": wizard_catalog(), "controls": control_catalog(), "agent": chatbot_interface_contract(), "composed_agent": composed_agent_contribution(), "dsl": {"pbc": PBC_KEY, "skills_namespace": f"{PBC_KEY}_skills", "single_pbc_app": True}, "side_effects": ()}

    def run_demo(self) -> dict:
        cfg = self.configure()
        award = self.activate_award("AWD-001", funder="USAID", award_number="A-2026-001", period_start="2026-01-01", period_end="2026-12-31", funding_amount=100000, source_document_uri="evidence://award")
        restriction = self.define_restriction("RES-001", "AWD-001", "purpose", "Only health outreach costs are allowable")
        budget = self.approve_budget("BUD-001", "AWD-001", ({"category": "personnel", "amount": 50000}, {"category": "supplies", "amount": 20000}))
        cost = self.record_cost("COST-001", "AWD-001", "BUD-001", "personnel", 12000, evidence_uri="evidence://payroll", paid=True)
        blocked_cost = self.record_cost("COST-002", "AWD-001", "BUD-001", "supplies", 25000, paid=True)
        draw = self.prepare_drawdown("DRAW-001", "AWD-001", ("COST-001",))
        req = self.track_match_requirement("MATCH-001", "AWD-001", 5000)
        contribution = self.record_match_contribution("MATCHC-001", "MATCH-001", 5000, "evidence://match", "cash")
        report = self.build_report("RPT-001", "AWD-001", ("DRAW-001",), "MATCH-001")
        evidence = self.attach_evidence("EVID-001", "AWD-001", "award_packet", "evidence://packet")
        closeout = self.close_grant("CLOSE-001", "AWD-001", "RPT-001")
        assistant = self.assistant_award_preview("award notice", "extract award, restrictions, budget, reports, and match")
        checks = (cfg["ok"], award["ok"], restriction["ok"], budget["ok"], cost["ok"], blocked_cost["ok"] is False, draw["ok"], req["ok"], contribution["ok"], report["ok"], evidence["ok"], closeout["ok"], assistant["ok"])
        return {"ok": all(checks), "blocked_cost": blocked_cost, "drawdown": draw, "report": report, "closeout": closeout, "assistant": assistant, "app_contract": self.app_contract(), "side_effects": ()}

def single_pbc_app_contract() -> dict:
    return GrantFundAccountingStandaloneApp().app_contract()
def standalone_smoke_test() -> dict:
    app = GrantFundAccountingStandaloneApp(); demo = app.run_demo(); runtime = grant_fund_accounting_runtime_smoke(); contract = single_pbc_app_contract()
    return {"ok": demo["ok"] and runtime["ok"] and contract["ok"] and contract["stream_engine_picker_visible"] is False, "demo": demo, "runtime": runtime, "contract": contract, "side_effects": ()}
