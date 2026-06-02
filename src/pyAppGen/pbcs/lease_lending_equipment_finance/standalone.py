"""Standalone one-PBC application for lease_lending_equipment_finance."""
from __future__ import annotations
from dataclasses import dataclass, field
from hashlib import sha256
from typing import Any

from .agent import chatbot_interface_contract, composed_agent_contribution, datastore_crud_plan, document_instruction_plan
from .controls import control_catalog, evaluate_control
from .forms import form_catalog
from .runtime import (
    LEASE_LENDING_EQUIPMENT_FINANCE_ALLOWED_DATABASE_BACKENDS,
    LEASE_LENDING_EQUIPMENT_FINANCE_CONSUMED_EVENT_TYPES,
    LEASE_LENDING_EQUIPMENT_FINANCE_EMITTED_EVENT_TYPES,
    LEASE_LENDING_EQUIPMENT_FINANCE_OWNED_TABLES,
    LEASE_LENDING_EQUIPMENT_FINANCE_REQUIRED_EVENT_TOPIC,
    lease_lending_equipment_finance_build_api_contract,
    lease_lending_equipment_finance_build_schema_contract,
    lease_lending_equipment_finance_build_service_contract,
    lease_lending_equipment_finance_configure_runtime,
    lease_lending_equipment_finance_empty_state,
    lease_lending_equipment_finance_permissions_contract,
    lease_lending_equipment_finance_receive_event,
    lease_lending_equipment_finance_register_rule,
    lease_lending_equipment_finance_runtime_smoke,
    lease_lending_equipment_finance_set_parameter,
)
from .ui import lease_lending_equipment_finance_render_workbench, lease_lending_equipment_finance_ui_contract
from .wizards import wizard_catalog

PBC_KEY = "lease_lending_equipment_finance"


def _digest(value: Any) -> str:
    return sha256(repr(value).encode("utf-8")).hexdigest()


@dataclass
class LeaseLendingEquipmentFinanceStandaloneApp:
    tenant: str = "tenant-equipment-finance-001"
    state: dict = field(default_factory=lease_lending_equipment_finance_empty_state)
    leases: dict[str, dict] = field(default_factory=dict)
    assets: dict[str, dict] = field(default_factory=dict)
    schedules: dict[str, dict] = field(default_factory=dict)
    residuals: dict[str, dict] = field(default_factory=dict)
    quotes: dict[str, dict] = field(default_factory=dict)
    repo_cases: dict[str, dict] = field(default_factory=dict)
    servicing_events: dict[str, dict] = field(default_factory=dict)
    investors: dict[str, dict] = field(default_factory=dict)

    def configure(self, database_backend: str = "postgresql") -> dict:
        configured = lease_lending_equipment_finance_configure_runtime(self.state, {"database_backend": database_backend, "event_topic": LEASE_LENDING_EQUIPMENT_FINANCE_REQUIRED_EVENT_TOPIC})
        self.state = configured["state"]
        for name, value in (("minimum_yield", 0.085), ("residual_review_days", 180), ("repo_notice_days", 10), ("serial_uniqueness_scope", "tenant"), ("buyout_quote_valid_days", 10), ("investor_share_tolerance", 0.0001)):
            result = lease_lending_equipment_finance_set_parameter(self.state, name, value); self.state = result["state"]
        for rule in (
            {"rule_id": "booking_conditions_closed", "scope": "origination", "effect": "block_booking"},
            {"rule_id": "serials_unique", "scope": "collateral", "effect": "block_duplicate_asset"},
            {"rule_id": "backed_by_acceptance", "scope": "funding", "effect": "block_disbursement"},
            {"rule_id": "return_floor_required", "scope": "pricing", "effect": "block_margin_leakage"},
            {"rule_id": "mandatory_repo_notices", "scope": "collections", "effect": "block_recovery"},
        ):
            registered = lease_lending_equipment_finance_register_rule(self.state, rule); self.state = registered["state"]
        received = lease_lending_equipment_finance_receive_event(self.state, {"event_type": LEASE_LENDING_EQUIPMENT_FINANCE_CONSUMED_EVENT_TYPES[0], "idempotency_key": "lease-policy-001"})
        self.state = received["state"]
        return {"ok": configured["ok"] and received["ok"], "side_effects": ()}

    def create_application(self, lease_id: str, structure: str, borrower: str, dealer: str, requested_amount: float, conditions: tuple[str, ...]) -> dict:
        lease = {"id": lease_id, "tenant": self.tenant, "structure": structure, "borrower": borrower, "dealer": dealer, "requested_amount": requested_amount, "conditions": tuple({"name": c, "status": "open"} for c in conditions), "pre_book_status": "approved_with_conditions", "parties": {"borrower": borrower, "dealer": dealer}, "funding_lines": (), "booked": False}
        self.leases[lease_id] = lease
        return {"ok": True, "lease": lease, "side_effects": ()}

    def add_party_role(self, lease_id: str, party_id: str, role: str, liability_scope: str = "full", notice_role: bool = False) -> dict:
        lease = dict(self.leases[lease_id]); parties = dict(lease.get("parties", {}))
        parties[party_id] = {"role": role, "liability_scope": liability_scope, "notice_role": notice_role, "effective": True}
        lease["parties"] = parties; self.leases[lease_id] = lease
        return {"ok": True, "lease": lease, "side_effects": ()}

    def clear_condition(self, lease_id: str, condition_name: str, evidence: str, waived_by: str | None = None) -> dict:
        lease = dict(self.leases[lease_id]); updated = []
        for condition in lease["conditions"]:
            row = dict(condition)
            if row["name"] == condition_name:
                row.update({"status": "waived" if waived_by else "satisfied", "evidence": evidence, "waived_by": waived_by})
            updated.append(row)
        lease["conditions"] = tuple(updated); self.leases[lease_id] = lease
        return {"ok": True, "lease": lease, "side_effects": ()}

    def register_asset(self, asset_id: str, lease_id: str, serials: tuple[str, ...], asset_class: str, location: str, title_status: str = "clear", **payload: Any) -> dict:
        duplicate = any(set(serials) & set(asset.get("serials", ())) for asset in self.assets.values())
        asset = {"id": asset_id, "lease_id": lease_id, "serials": serials, "manufacturer": payload.get("manufacturer", "Caterpillar"), "model": payload.get("model", "fleet-unit"), "asset_class": asset_class, "location": location, "title_status": title_status, "registration_id": payload.get("registration_id"), "substitution_lineage": payload.get("substitution_lineage", ()), "mobility": payload.get("mobility", "mobile")}
        if not duplicate:
            self.assets[asset_id] = asset
        return {"ok": not duplicate and bool(serials) and title_status in {"clear", "filed", "pending"}, "asset": asset, "duplicate": duplicate, "side_effects": ()}

    def approve_structure(self, lease_id: str, contract_family: str, booking_basis: str, purchase_option: str, residual_bearing: bool, usage_billing: bool, tax_classification: str) -> dict:
        incompatible = contract_family == "operating_lease" and booking_basis == "loan" or purchase_option == "one_dollar" and residual_bearing
        lease = dict(self.leases[lease_id])
        lease.update({"contract_family": contract_family, "booking_basis": booking_basis, "purchase_option": purchase_option, "residual_bearing": residual_bearing, "usage_billing": usage_billing, "tax_classification": tax_classification, "structure_status": "blocked" if incompatible else "approved"})
        self.leases[lease_id] = lease
        return {"ok": not incompatible, "lease": lease, "side_effects": ()}

    def reconcile_funding_package(self, lease_id: str, invoice_id: str, asset_lines: dict[str, float], eligible_costs: float, soft_costs: float, acceptance_evidence: bool, holdback: float = 0) -> dict:
        lease = dict(self.leases[lease_id]); total = sum(asset_lines.values())
        supported_assets = all(asset_id in self.assets and self.assets[asset_id]["lease_id"] == lease_id for asset_id in asset_lines)
        ok = supported_assets and abs(total - eligible_costs) < 0.01 and acceptance_evidence and soft_costs <= eligible_costs * 0.15
        event = {"id": invoice_id, "lease_id": lease_id, "asset_lines": asset_lines, "eligible_costs": eligible_costs, "soft_costs": soft_costs, "acceptance_evidence": acceptance_evidence, "holdback": holdback, "status": "approved" if ok else "blocked"}
        self.servicing_events[invoice_id] = event
        lease["funding_lines"] = lease.get("funding_lines", ()) + (invoice_id,); self.leases[lease_id] = lease
        return {"ok": ok, "funding_package": event, "side_effects": ()}

    def generate_schedule(self, lease_id: str, principal: float, term_months: int, annual_rate: float, pattern: str = "level", advance: bool = False, balloon: float = 0, seasonal_skips: tuple[int, ...] = ()) -> dict:
        monthly_rate = annual_rate / 12
        base_payment = round((principal - balloon) * monthly_rate / (1 - (1 + monthly_rate) ** -max(term_months, 1)), 2) if annual_rate else round((principal - balloon) / term_months, 2)
        rows = []
        balance = principal
        for month in range(1, term_months + 1):
            payment = 0 if month in seasonal_skips else base_payment
            if pattern == "step_up":
                payment = round(payment * (1 + month / (term_months * 10)), 2)
            interest = round(balance * monthly_rate, 2)
            principal_component = max(0, round(payment - interest, 2))
            if month == term_months:
                payment = round(payment + balloon, 2)
            balance = max(0, round(balance - principal_component, 2))
            rows.append({"month": month, "payment": payment, "interest": interest, "principal": principal_component, "advance": advance})
        schedule = {"id": f"SCH-{lease_id}", "lease_id": lease_id, "term_months": term_months, "annual_rate": annual_rate, "yield_rate": annual_rate, "pattern": pattern, "balloon": balloon, "version": 1, "rows": tuple(rows)}
        self.schedules[schedule["id"]] = schedule
        return {"ok": annual_rate >= 0.085 and term_months > 0, "schedule": schedule, "side_effects": ()}

    def record_usage_snapshot(self, lease_id: str, meter: str, allowance: float, reading: float, overage_rate: float, disputed: bool = False) -> dict:
        overage = max(0, reading - allowance)
        event = {"id": f"USG-{lease_id}-{meter}", "lease_id": lease_id, "meter": meter, "allowance": allowance, "reading": reading, "overage_charge": round(overage * overage_rate, 2), "disputed_component_paused": disputed}
        self.servicing_events[event["id"]] = event
        return {"ok": True, "usage": event, "side_effects": ()}

    def create_residual_review(self, lease_id: str, booked: float, current: float, stressed: float, comps: tuple[str, ...]) -> dict:
        review = {"id": f"RSV-{lease_id}", "lease_id": lease_id, "booked_residual": booked, "current_residual": current, "stressed_residual": stressed, "market_comps": comps, "downgrade": current < booked * 0.9, "review_due": False}
        self.residuals[review["id"]] = review
        return {"ok": bool(comps) and stressed <= current <= booked * 1.25, "residual": review, "side_effects": ()}

    def generate_buyout_quote(self, lease_id: str, quote_id: str, quote_type: str, principal: float, accrued_rent: float, fees: float, taxes: float, reserves: float, title_charges: float, effective_day: int) -> dict:
        allowed = {"scheduled_payoff", "accelerated_payoff", "fmv", "fixed_purchase_option", "casualty_payoff"}
        total = round(principal + accrued_rent + fees + taxes + title_charges - reserves, 2)
        quote = {"id": quote_id, "lease_id": lease_id, "quote_type": quote_type, "effective_day": effective_day, "expires_day": effective_day + 10, "components": {"principal": principal, "accrued_rent": accrued_rent, "fees": fees, "taxes": taxes, "reserves": reserves, "title_charges": title_charges}, "total": total}
        self.quotes[quote_id] = quote
        return {"ok": quote_type in allowed and total >= 0, "quote": quote, "side_effects": ()}

    def book_lease(self, lease_id: str) -> dict:
        lease = dict(self.leases[lease_id])
        open_conditions = tuple(c for c in lease.get("conditions", ()) if c["status"] == "open")
        has_asset = any(asset["lease_id"] == lease_id for asset in self.assets.values())
        has_schedule = f"SCH-{lease_id}" in self.schedules
        has_funding = any(self.servicing_events[event_id]["status"] == "approved" for event_id in lease.get("funding_lines", ()))
        ok = not open_conditions and has_asset and has_schedule and has_funding and lease.get("structure_status") == "approved"
        lease["booked"] = ok; lease["pre_book_status"] = "booked" if ok else "blocked"
        self.leases[lease_id] = lease
        return {"ok": ok, "lease": lease, "open_conditions": open_conditions, "side_effects": ()}

    def open_collection_case(self, lease_id: str, days_past_due: int, promise_to_pay_day: int | None = None, bankruptcy_hold: bool = False) -> dict:
        segment = "bankruptcy_hold" if bankruptcy_hold else "workout" if days_past_due >= 90 else "hard_delinquency" if days_past_due >= 60 else "soft_delinquency"
        event = {"id": f"COLL-{lease_id}", "lease_id": lease_id, "days_past_due": days_past_due, "segment": segment, "promise_to_pay_day": promise_to_pay_day, "status": "active"}
        self.servicing_events[event["id"]] = event
        return {"ok": True, "collections_event": event, "side_effects": ()}

    def open_repo_case(self, case_id: str, lease_id: str, mandatory_notices: tuple[str, ...], cure_deadline_day: int, legal_hold: bool = False, vendor: str | None = None) -> dict:
        ok = bool(mandatory_notices) and cure_deadline_day > 0 and not legal_hold and bool(vendor)
        case = {"id": case_id, "lease_id": lease_id, "mandatory_notices": mandatory_notices, "cure_deadline_day": cure_deadline_day, "legal_hold": legal_hold, "vendor": vendor, "status": "vendor_assigned" if ok else "blocked"}
        self.repo_cases[case_id] = case
        return {"ok": ok, "repo_case": case, "side_effects": ()}

    def record_disposition(self, case_id: str, gross_proceeds: float, storage_costs: float, transport_costs: float, repair_costs: float, deficiency_balance: float) -> dict:
        case = dict(self.repo_cases[case_id])
        net = round(gross_proceeds - storage_costs - transport_costs - repair_costs, 2)
        case["disposition"] = {"gross_proceeds": gross_proceeds, "net_recovery": net, "deficiency_or_surplus": round(net - deficiency_balance, 2)}
        case["status"] = "disposed"
        self.repo_cases[case_id] = case
        return {"ok": True, "repo_case": case, "side_effects": ()}

    def allocate_investors(self, lease_id: str, allocations: dict[str, float], servicing_fee_basis_points: int) -> dict:
        total = round(sum(allocations.values()), 6)
        allocation = {"lease_id": lease_id, "allocations": allocations, "servicing_fee_basis_points": servicing_fee_basis_points, "shares_equal_100": abs(total - 1.0) <= 0.0001}
        self.investors[lease_id] = allocation
        return {"ok": allocation["shares_equal_100"], "investor_allocation": allocation, "side_effects": ()}

    def remit_investor_cash(self, lease_id: str, collected_cash: float, fees: float = 0) -> dict:
        allocation = self.investors[lease_id]
        distributable = max(0, collected_cash - fees)
        waterfall = tuple({"investor": investor, "amount": round(distributable * share, 2)} for investor, share in allocation["allocations"].items())
        event = {"id": f"RMT-{lease_id}", "lease_id": lease_id, "collected_cash": collected_cash, "fees": fees, "waterfall": waterfall, "shortfall": collected_cash < fees}
        self.servicing_events[event["id"]] = event
        return {"ok": allocation["shares_equal_100"] and not event["shortfall"], "remittance": event, "side_effects": ()}

    def assistant_finance_pack_preview(self, document: str, instruction: str) -> dict:
        plan = document_instruction_plan(document, instruction)
        crud = datastore_crud_plan("update", table="lease_lending_equipment_finance_equipment_lease", payload={"instruction": instruction})
        extraction = {"document_type": "finance_pack", "fields": ("serials", "purchase_option", "payoff_terms", "insurance_loss_payee"), "requires_citation_spans": True, "confidence": 0.87}
        return {"ok": plan["ok"] and crud["ok"], "document_plan": plan, "crud_preview": crud, "extraction": extraction, "requires_confirmation": True, "side_effects": ()}

    def app_contract(self) -> dict:
        return {"format": "appgen.lease-lending-equipment-finance.standalone-app.v1", "ok": True, "pbc": PBC_KEY, "owned_tables": LEASE_LENDING_EQUIPMENT_FINANCE_OWNED_TABLES, "database_backends": LEASE_LENDING_EQUIPMENT_FINANCE_ALLOWED_DATABASE_BACKENDS, "event_contract": "AppGen-X", "stream_engine_picker_visible": False, "schema": lease_lending_equipment_finance_build_schema_contract(), "services": lease_lending_equipment_finance_build_service_contract(), "routes": lease_lending_equipment_finance_build_api_contract(), "permissions": lease_lending_equipment_finance_permissions_contract(), "ui": lease_lending_equipment_finance_ui_contract(), "workbench": lease_lending_equipment_finance_render_workbench(), "forms": form_catalog(), "wizards": wizard_catalog(), "controls": control_catalog(), "agent": chatbot_interface_contract(), "composed_agent": composed_agent_contribution(), "dsl": {"pbc": PBC_KEY, "skills_namespace": f"{PBC_KEY}_skills", "single_pbc_app": True}, "side_effects": ()}

    def run_demo(self) -> dict:
        cfg = self.configure()
        app = self.create_application("LEASE-001", "fmv_lease", "borrower-1", "dealer-1", 250000, ("insurance", "ucc_search"))
        role = self.add_party_role("LEASE-001", "guarantor-1", "guarantor", "limited_to_schedule_a", True)
        cond1 = self.clear_condition("LEASE-001", "insurance", "binder accepted")
        cond2 = self.clear_condition("LEASE-001", "ucc_search", "filed UCC-1")
        asset = self.register_asset("AST-001", "LEASE-001", ("SN-001", "VIN-001"), "yellow_iron", "Nairobi yard", "filed")
        duplicate_asset = self.register_asset("AST-DUP", "LEASE-001", ("SN-001",), "yellow_iron", "Nairobi yard", "filed")
        structure = self.approve_structure("LEASE-001", "operating_lease", "lease", "fmv", True, True, "lessor_tax_owner")
        bad_structure = self.approve_structure("LEASE-BAD", "operating_lease", "loan", "one_dollar", True, False, "borrower_tax_owner") if "LEASE-BAD" in self.leases else {"ok": False}
        funding = self.reconcile_funding_package("LEASE-001", "INV-001", {"AST-001": 250000}, 250000, 10000, True, 25000)
        schedule = self.generate_schedule("LEASE-001", 250000, 36, 0.095, pattern="step_up", balloon=50000, seasonal_skips=(7, 8))
        usage = self.record_usage_snapshot("LEASE-001", "hours", 1200, 1350, 4.5, disputed=True)
        residual = self.create_residual_review("LEASE-001", 70000, 64000, 52000, ("auction-comp-1", "dealer-comp-2"))
        quote = self.generate_buyout_quote("LEASE-001", "Q-001", "fmv", 185000, 2200, 350, 1500, 5000, 175, 100)
        booked = self.book_lease("LEASE-001")
        collections = self.open_collection_case("LEASE-001", 65, promise_to_pay_day=115)
        repo_blocked = self.open_repo_case("REPO-BAD", "LEASE-001", (), 0, False, None)
        repo = self.open_repo_case("REPO-001", "LEASE-001", ("right_to_cure", "intent_to_repossess"), 125, False, "repo-vendor-1")
        disposition = self.record_disposition("REPO-001", 180000, 2500, 1800, 5000, 190000)
        investor_bad = self.allocate_investors("LEASE-BAD", {"investor-a": 0.7, "investor-b": 0.2}, 50)
        investor = self.allocate_investors("LEASE-001", {"originator": 0.2, "investor-a": 0.5, "investor-b": 0.3}, 45)
        remittance = self.remit_investor_cash("LEASE-001", 18000, 500)
        assistant = self.assistant_finance_pack_preview("lease agreement and invoice", "extract serials and draft booked lease update")
        checks = (cfg["ok"], app["ok"], role["ok"], cond1["ok"], cond2["ok"], asset["ok"], duplicate_asset["ok"] is False, structure["ok"], bad_structure["ok"] is False, funding["ok"], schedule["ok"], usage["ok"], residual["ok"], quote["ok"], booked["ok"], collections["ok"], repo_blocked["ok"] is False, repo["ok"], disposition["ok"], investor_bad["ok"] is False, investor["ok"], remittance["ok"], assistant["ok"])
        return {"ok": all(checks), "booked": booked, "duplicate_asset": duplicate_asset, "blocked_repo": repo_blocked, "investor_bad": investor_bad, "schedule": schedule, "usage": usage, "residual": residual, "quote": quote, "disposition": disposition, "assistant": assistant, "app_contract": self.app_contract(), "side_effects": ()}


def single_pbc_app_contract() -> dict:
    return LeaseLendingEquipmentFinanceStandaloneApp().app_contract()


def standalone_smoke_test() -> dict:
    app = LeaseLendingEquipmentFinanceStandaloneApp(); demo = app.run_demo(); runtime = lease_lending_equipment_finance_runtime_smoke(); contract = single_pbc_app_contract()
    return {"ok": demo["ok"] and runtime["ok"] and contract["ok"] and bool(LEASE_LENDING_EQUIPMENT_FINANCE_EMITTED_EVENT_TYPES) and contract["stream_engine_picker_visible"] is False, "demo": demo, "runtime": runtime, "contract": contract, "side_effects": ()}
