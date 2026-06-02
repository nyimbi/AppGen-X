"""Standalone one-PBC lending origination and servicing application."""
from __future__ import annotations
from dataclasses import dataclass, field
from hashlib import sha256
from typing import Any
from .agent import chatbot_interface_contract, composed_agent_contribution, datastore_crud_plan, document_instruction_plan
from .controls import control_catalog, evaluate_control
from .forms import form_catalog
from .runtime import (
    LENDING_ORIGINATION_SERVICING_ALLOWED_DATABASE_BACKENDS, LENDING_ORIGINATION_SERVICING_CONSUMED_EVENT_TYPES,
    LENDING_ORIGINATION_SERVICING_EMITTED_EVENT_TYPES, LENDING_ORIGINATION_SERVICING_OWNED_TABLES,
    LENDING_ORIGINATION_SERVICING_REQUIRED_EVENT_TOPIC, lending_origination_servicing_build_api_contract,
    lending_origination_servicing_build_schema_contract, lending_origination_servicing_build_service_contract,
    lending_origination_servicing_configure_runtime, lending_origination_servicing_empty_state,
    lending_origination_servicing_permissions_contract, lending_origination_servicing_receive_event,
    lending_origination_servicing_register_rule, lending_origination_servicing_runtime_smoke,
    lending_origination_servicing_set_parameter,
)
from .ui import lending_origination_servicing_render_workbench, lending_origination_servicing_ui_contract
from .wizards import wizard_catalog
PBC_KEY = "lending_origination_servicing"

def _digest(value: Any) -> str:
    return sha256(repr(value).encode("utf-8")).hexdigest()

@dataclass
class LendingOriginationServicingStandaloneApp:
    tenant: str = "tenant-lending-001"
    state: dict = field(default_factory=lending_origination_servicing_empty_state)
    applications: dict[str, dict] = field(default_factory=dict)
    borrowers: dict[str, dict] = field(default_factory=dict)
    decisions: dict[str, dict] = field(default_factory=dict)
    offers: dict[str, dict] = field(default_factory=dict)
    disbursements: dict[str, dict] = field(default_factory=dict)
    schedules: dict[str, dict] = field(default_factory=dict)
    cases: dict[str, dict] = field(default_factory=dict)

    def configure(self, database_backend: str = "postgresql") -> dict:
        configured = lending_origination_servicing_configure_runtime(self.state, {"database_backend": database_backend, "event_topic": LENDING_ORIGINATION_SERVICING_REQUIRED_EVENT_TOPIC})
        self.state = configured["state"]
        for name, value in (("max_dti", 0.43), ("min_dscr", 1.25), ("offer_valid_days", 10), ("grace_days", 10), ("payoff_quote_days", 15), ("complaint_response_days", 30)):
            result = lending_origination_servicing_set_parameter(self.state, name, value); self.state = result["state"]
        for rule in (
            {"rule_id": "consent_before_bureau", "scope": "intake"}, {"rule_id": "kyc_fraud_before_decision", "scope": "underwriting"}, {"rule_id": "conditions_before_funding", "scope": "closing"}, {"rule_id": "boarding_reconciliation_required", "scope": "servicing"}, {"rule_id": "restricted_contact_respected", "scope": "collections"},
        ):
            registered = lending_origination_servicing_register_rule(self.state, rule); self.state = registered["state"]
        received = lending_origination_servicing_receive_event(self.state, {"event_type": LENDING_ORIGINATION_SERVICING_CONSUMED_EVENT_TYPES[0], "idempotency_key": "lending-policy-001"})
        self.state = received["state"]
        return {"ok": configured["ok"] and received["ok"], "side_effects": ()}

    def create_application(self, application_id: str, borrower_id: str, roles: tuple[str, ...], purpose: str, amount: float, consents: tuple[str, ...], beneficial_owners: tuple[str, ...] = ()) -> dict:
        ok = "applicant" in roles and "credit_pull" in consents and "privacy" in consents
        app = {"id": application_id, "borrower_id": borrower_id, "roles": roles, "purpose": purpose, "requested_amount": amount, "consents": consents, "beneficial_owners": beneficial_owners, "status": "intake_complete" if ok else "blocked", "stipulations": ()}
        self.applications[application_id] = app
        return {"ok": ok, "application": app, "side_effects": ()}

    def add_stipulation(self, application_id: str, stip_id: str, stage: str, document_type: str, owner: str, received: bool = False, waived_by: str | None = None) -> dict:
        app = dict(self.applications[application_id])
        stip = {"id": stip_id, "stage": stage, "document_type": document_type, "owner": owner, "status": "waived" if waived_by else "received" if received else "open", "waived_by": waived_by}
        app["stipulations"] = app.get("stipulations", ()) + (stip,)
        self.applications[application_id] = app
        return {"ok": True, "stipulation": stip, "application": app, "side_effects": ()}

    def verify_borrower(self, borrower_id: str, declared_income: float, verified_income: float, obligations: float, identity_passed: bool, fraud_signals: tuple[str, ...], bureau_score: int, bureau_disputed: bool = False) -> dict:
        stable_income = min(declared_income, verified_income)
        dti = round(obligations / max(stable_income / 12, 1), 4)
        borrower = {"id": borrower_id, "declared_income": declared_income, "verified_income": verified_income, "stable_income": stable_income, "obligations": obligations, "dti": dti, "identity_passed": identity_passed, "fraud_signals": fraud_signals, "bureau_score": bureau_score, "bureau_disputed": bureau_disputed, "verification_status": "clear" if identity_passed and not fraud_signals and not bureau_disputed else "review"}
        self.borrowers[borrower_id] = borrower
        return {"ok": borrower["verification_status"] == "clear", "borrower": borrower, "side_effects": ()}

    def capture_collateral(self, application_id: str, collateral_type: str, identifier: str, valuation: float, haircut: float, lien_position: int, title_clear: bool) -> dict:
        app = dict(self.applications[application_id])
        collateral = {"type": collateral_type, "identifier": identifier, "valuation": valuation, "haircut": haircut, "lendable_value": round(valuation * (1 - haircut), 2), "lien_position": lien_position, "title_clear": title_clear}
        app["collateral"] = collateral; self.applications[application_id] = app
        return {"ok": title_clear and lien_position == 1, "collateral": collateral, "side_effects": ()}

    def underwrite(self, decision_id: str, application_id: str, product: str, policy_version: str) -> dict:
        app = self.applications[application_id]; borrower = self.borrowers[app["borrower_id"]]
        open_pre = tuple(s for s in app.get("stipulations", ()) if s["stage"] == "pre_underwriting" and s["status"] == "open")
        dti_pass = borrower["dti"] <= 0.43
        bureau_pass = borrower["bureau_score"] >= 660
        collateral_pass = not app.get("collateral") or app["collateral"]["lendable_value"] >= app["requested_amount"] * 0.8
        approved = not open_pre and borrower["verification_status"] == "clear" and dti_pass and bureau_pass and collateral_pass
        reasons = tuple(reason for reason, failed in (("open_stipulations", bool(open_pre)), ("identity_or_fraud_review", borrower["verification_status"] != "clear"), ("dti_exceeds_policy", not dti_pass), ("bureau_score_below_policy", not bureau_pass), ("collateral_shortfall", not collateral_pass)) if failed)
        decision = {"id": decision_id, "application_id": application_id, "product": product, "policy_version": policy_version, "outcome": "approved" if approved else "declined", "reason_codes": reasons, "lineage": {"policy_version": policy_version, "dti": borrower["dti"], "bureau_score": borrower["bureau_score"]}}
        self.decisions[decision_id] = decision
        return {"ok": approved, "decision": decision, "side_effects": ()}

    def build_offer(self, offer_id: str, decision_id: str, amount: float, term_months: int, rate: float, fees: float, lock_day: int, conditions: tuple[str, ...]) -> dict:
        decision = self.decisions[decision_id]
        ok = decision["outcome"] == "approved" and rate >= 0.055 and amount <= self.applications[decision["application_id"]]["requested_amount"]
        offer = {"id": offer_id, "decision_id": decision_id, "amount": amount, "term_months": term_months, "rate": rate, "fees": fees, "lock_day": lock_day, "expiration_day": lock_day + 10, "conditions": tuple({"name": c, "status": "open"} for c in conditions), "status": "issued" if ok else "blocked"}
        self.offers[offer_id] = offer
        return {"ok": ok, "offer": offer, "side_effects": ()}

    def clear_offer_condition(self, offer_id: str, condition: str) -> dict:
        offer = dict(self.offers[offer_id]); rows=[]
        for row in offer["conditions"]:
            item=dict(row)
            if item["name"] == condition: item["status"] = "cleared"
            rows.append(item)
        offer["conditions"] = tuple(rows); self.offers[offer_id] = offer
        return {"ok": True, "offer": offer, "side_effects": ()}

    def fund_disbursement(self, disbursement_id: str, offer_id: str, gross: float, payoffs: float, reserves: float, fees: float, settlement_ack: bool) -> dict:
        offer = self.offers[offer_id]
        open_conditions = tuple(c for c in offer["conditions"] if c["status"] == "open")
        net = round(gross - payoffs - reserves - fees, 2)
        ok = not open_conditions and settlement_ack and abs(gross - offer["amount"]) < 0.01 and net >= 0
        disb = {"id": disbursement_id, "offer_id": offer_id, "gross": gross, "payoffs": payoffs, "reserves": reserves, "fees": fees, "net_proceeds": net, "settlement_ack": settlement_ack, "status": "funded" if ok else "blocked"}
        self.disbursements[disbursement_id] = disb
        return {"ok": ok, "disbursement": disb, "side_effects": ()}

    def board_schedule(self, schedule_id: str, disbursement_id: str, note_terms_match: bool, method: str, day_count: str, escrow: dict[str, float] | None = None) -> dict:
        disb = self.disbursements[disbursement_id]
        amount = disb["gross"]
        months = self.offers[disb["offer_id"]]["term_months"]
        rate = self.offers[disb["offer_id"]]["rate"] / 12
        payment = round(amount * rate / (1 - (1 + rate) ** -months), 2)
        schedule = {"id": schedule_id, "disbursement_id": disbursement_id, "note_terms_match": note_terms_match, "method": method, "day_count": day_count, "escrow": escrow or {}, "payment": payment, "status": "active" if note_terms_match and disb["status"] == "funded" else "blocked", "balance": amount, "days_past_due": 0}
        self.schedules[schedule_id] = schedule
        return {"ok": schedule["status"] == "active", "schedule": schedule, "side_effects": ()}

    def post_payment(self, schedule_id: str, amount: float, allocation: tuple[str, ...] = ("interest", "escrow", "fees", "principal")) -> dict:
        schedule = dict(self.schedules[schedule_id])
        principal = max(0, amount - 100)
        schedule["balance"] = max(0, round(schedule["balance"] - principal, 2))
        schedule["last_payment"] = {"amount": amount, "allocation": allocation, "principal": principal}
        self.schedules[schedule_id] = schedule
        return {"ok": True, "schedule": schedule, "side_effects": ()}

    def open_servicing_case(self, case_id: str, schedule_id: str, days_past_due: int, case_type: str, special_status: str | None = None) -> dict:
        bucket = "current" if days_past_due == 0 else "grace" if days_past_due <= 10 else "early" if days_past_due < 60 else "late" if days_past_due < 90 else "default"
        case = {"id": case_id, "schedule_id": schedule_id, "days_past_due": days_past_due, "bucket": bucket, "case_type": case_type, "special_status": special_status, "restricted_actions": special_status in {"bankruptcy", "legal_hold", "deceased"}, "status": "open"}
        self.cases[case_id] = case
        return {"ok": True, "case": case, "side_effects": ()}

    def record_promise_to_pay(self, case_id: str, promised_amount: float, due_day: int, paid_day: int | None = None) -> dict:
        case = dict(self.cases[case_id]); kept = paid_day is not None and paid_day <= due_day
        case["promise_to_pay"] = {"amount": promised_amount, "due_day": due_day, "paid_day": paid_day, "status": "kept" if kept else "broken"}
        self.cases[case_id] = case
        return {"ok": kept, "case": case, "side_effects": ()}

    def approve_modification(self, case_id: str, capitalized_interest: float, forgiven_fees: float, new_rate: float, approvals: tuple[str, ...]) -> dict:
        ok = len(approvals) >= 2 and new_rate > 0
        case = dict(self.cases[case_id]); case["modification"] = {"capitalized_interest": capitalized_interest, "forgiven_fees": forgiven_fees, "new_rate": new_rate, "approvals": approvals, "status": "approved" if ok else "blocked"}
        self.cases[case_id] = case
        return {"ok": ok, "case": case, "side_effects": ()}

    def generate_payoff_quote(self, quote_id: str, schedule_id: str, good_through_day: int, accrued_interest: float, fees: float, escrow_surplus: float) -> dict:
        schedule = self.schedules[schedule_id]
        total = round(schedule["balance"] + accrued_interest + fees - escrow_surplus, 2)
        quote = {"id": quote_id, "schedule_id": schedule_id, "good_through_day": good_through_day, "principal": schedule["balance"], "accrued_interest": accrued_interest, "fees": fees, "escrow_surplus": escrow_surplus, "total": total, "assumption_hash": _digest((schedule_id, good_through_day, total))}
        self.cases[quote_id] = quote
        return {"ok": total >= 0, "payoff_quote": quote, "side_effects": ()}

    def record_complaint_or_covenant(self, case_id: str, schedule_id: str, case_type: str, due_day: int, owner: str, breached: bool = False) -> dict:
        case = {"id": case_id, "schedule_id": schedule_id, "case_type": case_type, "due_day": due_day, "owner": owner, "breached": breached, "status": "breach_workflow" if breached else "tracking"}
        self.cases[case_id] = case
        return {"ok": True, "case": case, "side_effects": ()}

    def assistant_lending_file_preview(self, document: str, instruction: str) -> dict:
        plan = document_instruction_plan(document, instruction)
        crud = datastore_crud_plan("update", table="lending_origination_servicing_loan_application", payload={"instruction": instruction})
        return {"ok": plan["ok"] and crud["ok"], "document_plan": plan, "crud_preview": crud, "requires_confirmation": True, "extraction": {"document_type": "lending_file", "fields": ("income", "stipulations", "collateral", "note_terms"), "citation_spans_required": True}, "side_effects": ()}

    def app_contract(self) -> dict:
        return {"format": "appgen.lending-origination-servicing.standalone-app.v1", "ok": True, "pbc": PBC_KEY, "owned_tables": LENDING_ORIGINATION_SERVICING_OWNED_TABLES, "database_backends": LENDING_ORIGINATION_SERVICING_ALLOWED_DATABASE_BACKENDS, "event_contract": "AppGen-X", "stream_engine_picker_visible": False, "schema": lending_origination_servicing_build_schema_contract(), "services": lending_origination_servicing_build_service_contract(), "routes": lending_origination_servicing_build_api_contract(), "permissions": lending_origination_servicing_permissions_contract(), "ui": lending_origination_servicing_ui_contract(), "workbench": lending_origination_servicing_render_workbench(), "forms": form_catalog(), "wizards": wizard_catalog(), "controls": control_catalog(), "agent": chatbot_interface_contract(), "composed_agent": composed_agent_contribution(), "dsl": {"pbc": PBC_KEY, "skills_namespace": f"{PBC_KEY}_skills", "single_pbc_app": True}, "side_effects": ()}

    def run_demo(self) -> dict:
        cfg = self.configure()
        app = self.create_application("APP-001", "BOR-001", ("applicant",), "working_capital", 100000, ("credit_pull", "privacy"), ("owner-1",))
        bad_app = self.create_application("APP-BAD", "BOR-002", ("guarantor",), "working_capital", 50000, ("privacy",))
        stip = self.add_stipulation("APP-001", "STIP-001", "pre_underwriting", "bank_statements", "borrower", received=True)
        borrower = self.verify_borrower("BOR-001", 180000, 168000, 4200, True, (), 720)
        fraud = self.verify_borrower("BOR-FRAUD", 100000, 90000, 2000, False, ("watchlist",), 700)
        collateral = self.capture_collateral("APP-001", "vehicle", "VIN-001", 150000, 0.25, 1, True)
        decision = self.underwrite("DEC-001", "APP-001", "secured_term", "2026.05")
        offer = self.build_offer("OFF-001", "DEC-001", 95000, 36, 0.095, 900, 10, ("insurance", "signed_note"))
        blocked_funding = self.fund_disbursement("DISB-BAD", "OFF-001", 95000, 0, 0, 900, True)
        self.clear_offer_condition("OFF-001", "insurance"); self.clear_offer_condition("OFF-001", "signed_note")
        disb = self.fund_disbursement("DISB-001", "OFF-001", 95000, 5000, 2000, 900, True)
        bad_board = self.board_schedule("SCH-BAD", "DISB-001", False, "level_pay", "actual_365")
        schedule = self.board_schedule("SCH-001", "DISB-001", True, "level_pay", "actual_365", {"tax": 1200, "insurance": 800})
        payment = self.post_payment("SCH-001", 3500)
        case = self.open_servicing_case("CASE-001", "SCH-001", 65, "collections")
        promise_broken = self.record_promise_to_pay("CASE-001", 1000, 30, None)
        mod_bad = self.approve_modification("CASE-001", 300, 50, 0.07, ("collector",))
        mod = self.approve_modification("CASE-001", 300, 50, 0.07, ("collector", "manager"))
        payoff = self.generate_payoff_quote("PAY-001", "SCH-001", 45, 500, 150, 200)
        special = self.open_servicing_case("CASE-BK", "SCH-001", 30, "bankruptcy", "bankruptcy")
        covenant = self.record_complaint_or_covenant("COV-001", "SCH-001", "covenant", 60, "portfolio-manager", breached=True)
        assistant = self.assistant_lending_file_preview("application and note package", "extract stipulations and update application")
        checks = (cfg["ok"], app["ok"], bad_app["ok"] is False, stip["ok"], borrower["ok"], fraud["ok"] is False, collateral["ok"], decision["ok"], offer["ok"], blocked_funding["ok"] is False, disb["ok"], bad_board["ok"] is False, schedule["ok"], payment["ok"], case["ok"], promise_broken["ok"] is False, mod_bad["ok"] is False, mod["ok"], payoff["ok"], special["case"]["restricted_actions"] is True, covenant["case"]["status"] == "breach_workflow", assistant["ok"])
        return {"ok": all(checks), "bad_app": bad_app, "fraud": fraud, "blocked_funding": blocked_funding, "bad_board": bad_board, "promise_broken": promise_broken, "mod_bad": mod_bad, "payoff": payoff, "assistant": assistant, "app_contract": self.app_contract(), "side_effects": ()}

def single_pbc_app_contract() -> dict:
    return LendingOriginationServicingStandaloneApp().app_contract()

def standalone_smoke_test() -> dict:
    app = LendingOriginationServicingStandaloneApp(); demo = app.run_demo(); runtime = lending_origination_servicing_runtime_smoke(); contract = single_pbc_app_contract()
    return {"ok": demo["ok"] and runtime["ok"] and contract["ok"] and bool(LENDING_ORIGINATION_SERVICING_EMITTED_EVENT_TYPES) and contract["stream_engine_picker_visible"] is False, "demo": demo, "runtime": runtime, "contract": contract, "side_effects": ()}
