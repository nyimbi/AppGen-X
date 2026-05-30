"""Standalone one-PBC legal matter management application."""
from __future__ import annotations
from dataclasses import dataclass, field
from hashlib import sha256
from typing import Any
from .agent import chatbot_interface_contract, composed_agent_contribution, datastore_crud_plan, document_instruction_plan
from .controls import control_catalog, evaluate_control
from .forms import form_catalog
from .runtime import (
    LEGAL_MATTER_MANAGEMENT_ALLOWED_DATABASE_BACKENDS, LEGAL_MATTER_MANAGEMENT_CONSUMED_EVENT_TYPES,
    LEGAL_MATTER_MANAGEMENT_EMITTED_EVENT_TYPES, LEGAL_MATTER_MANAGEMENT_OWNED_TABLES,
    LEGAL_MATTER_MANAGEMENT_REQUIRED_EVENT_TOPIC, legal_matter_management_build_api_contract,
    legal_matter_management_build_schema_contract, legal_matter_management_build_service_contract,
    legal_matter_management_configure_runtime, legal_matter_management_empty_state,
    legal_matter_management_permissions_contract, legal_matter_management_receive_event,
    legal_matter_management_register_rule, legal_matter_management_runtime_smoke,
    legal_matter_management_set_parameter,
)
from .ui import legal_matter_management_render_workbench, legal_matter_management_ui_contract
from .wizards import wizard_catalog
PBC_KEY = "legal_matter_management"

def _digest(value: Any) -> str:
    return sha256(repr(value).encode("utf-8")).hexdigest()

@dataclass
class LegalMatterManagementStandaloneApp:
    tenant: str = "tenant-legal-001"
    state: dict = field(default_factory=legal_matter_management_empty_state)
    matters: dict[str, dict] = field(default_factory=dict)
    counsel: dict[str, dict] = field(default_factory=dict)
    holds: dict[str, dict] = field(default_factory=dict)
    deadlines: dict[str, dict] = field(default_factory=dict)
    documents: dict[str, dict] = field(default_factory=dict)
    budgets: dict[str, dict] = field(default_factory=dict)
    invoices: dict[str, dict] = field(default_factory=dict)
    outcomes: dict[str, dict] = field(default_factory=dict)

    def configure(self, database_backend: str = "postgresql") -> dict:
        configured = legal_matter_management_configure_runtime(self.state, {"database_backend": database_backend, "event_topic": LEGAL_MATTER_MANAGEMENT_REQUIRED_EVENT_TOPIC})
        self.state = configured["state"]
        for name, value in (("critical_deadline_reviewers", 2), ("invoice_variance_threshold", 0.1), ("settlement_exec_threshold", 500000), ("hold_ack_hours", 72), ("privilege_sample_rate", 0.05)):
            result = legal_matter_management_set_parameter(self.state, name, value); self.state = result["state"]
        for rule in (
            {"rule_id": "matter_taxonomy_required", "scope": "intake"},
            {"rule_id": "conflict_clearance_before_counsel", "scope": "counsel"},
            {"rule_id": "critical_deadline_dual_control", "scope": "deadline"},
            {"rule_id": "privilege_review_before_production", "scope": "document"},
            {"rule_id": "settlement_matrix_required", "scope": "outcome"},
        ):
            registered = legal_matter_management_register_rule(self.state, rule); self.state = registered["state"]
        received = legal_matter_management_receive_event(self.state, {"event_type": LEGAL_MATTER_MANAGEMENT_CONSUMED_EVENT_TYPES[0], "idempotency_key": "legal-policy-001"})
        self.state = received["state"]
        return {"ok": configured["ok"] and received["ok"], "side_effects": ()}

    def open_matter(self, matter_id: str, matter_type: str, jurisdiction: str, urgency: str, privilege_sensitive: bool, related_parties: tuple[str, ...]) -> dict:
        duplicate = any(m["matter_type"] == matter_type and set(m.get("related_parties", ())) & set(related_parties) for m in self.matters.values())
        score = {"low": 1, "medium": 2, "high": 3, "critical": 4}.get(urgency, 1) + (1 if privilege_sensitive else 0)
        matter = {"id": matter_id, "matter_type": matter_type, "jurisdiction": jurisdiction, "urgency": urgency, "privilege_sensitive": privilege_sensitive, "related_parties": related_parties, "classification_confidence": 0.91, "duplicate_candidate": duplicate, "risk_score": score, "status": "open", "timeline": (("opened", matter_type),)}
        self.matters[matter_id] = matter
        return {"ok": not duplicate, "matter": matter, "side_effects": ()}

    def screen_conflicts(self, matter_id: str, party_aliases: tuple[str, ...], former_client: bool = False, waiver: str | None = None, wall_required: bool = False) -> dict:
        unresolved = former_client and not waiver
        decision = {"matter_id": matter_id, "party_aliases": party_aliases, "former_client": former_client, "waiver": waiver, "wall_required": wall_required, "clearance": "blocked" if unresolved else "cleared"}
        self.matters[matter_id]["conflict_screen"] = decision
        return {"ok": not unresolved, "conflict_screen": decision, "side_effects": ()}

    def assign_counsel(self, counsel_id: str, matter_id: str, firm: str, jurisdiction_admitted: bool, conflict_cleared: bool, rate_card: dict[str, float], scope: tuple[str, ...]) -> dict:
        ok = jurisdiction_admitted and conflict_cleared and bool(scope) and bool(rate_card)
        record = {"id": counsel_id, "matter_id": matter_id, "firm": firm, "jurisdiction_admitted": jurisdiction_admitted, "conflict_cleared": conflict_cleared, "rate_card": rate_card, "scope": scope, "status": "active" if ok else "blocked"}
        self.counsel[counsel_id] = record
        return {"ok": ok, "counsel": record, "side_effects": ()}

    def issue_legal_hold(self, hold_id: str, matter_id: str, custodians: tuple[str, ...], systems: tuple[str, ...], date_range: tuple[str, str], keywords: tuple[str, ...]) -> dict:
        event_hash = _digest((hold_id, matter_id, custodians, systems, date_range, keywords))
        hold = {"id": hold_id, "matter_id": matter_id, "custodians": custodians, "systems": systems, "date_range": date_range, "keywords": keywords, "acknowledgements": tuple({"custodian": c, "status": "pending"} for c in custodians), "hash_chain": (event_hash,), "status": "issued" if custodians and systems else "blocked"}
        self.holds[hold_id] = hold
        return {"ok": hold["status"] == "issued", "hold": hold, "emitted_event": "LegalHoldIssued", "side_effects": ()}

    def acknowledge_hold(self, hold_id: str, custodian: str) -> dict:
        hold = dict(self.holds[hold_id]); rows = []
        for ack in hold["acknowledgements"]:
            row = dict(ack)
            if row["custodian"] == custodian: row["status"] = "acknowledged"
            rows.append(row)
        hold["acknowledgements"] = tuple(rows); hold["hash_chain"] = hold["hash_chain"] + (_digest((hold_id, custodian, "ack")),)
        self.holds[hold_id] = hold
        return {"ok": True, "hold": hold, "side_effects": ()}

    def compute_deadline(self, deadline_id: str, matter_id: str, trigger_day: int, rule_days: int, jurisdiction_calendar: str, critical: bool, reviewers: tuple[str, ...]) -> dict:
        due_day = trigger_day + rule_days
        ok = bool(jurisdiction_calendar) and (not critical or len(reviewers) >= 2)
        deadline = {"id": deadline_id, "matter_id": matter_id, "trigger_day": trigger_day, "rule_days": rule_days, "due_day": due_day, "jurisdiction_calendar": jurisdiction_calendar, "critical": critical, "reviewers": reviewers, "status": "tracked" if ok else "blocked"}
        self.deadlines[deadline_id] = deadline
        return {"ok": ok, "deadline": deadline, "emitted_event": "MatterDeadlineTracked", "side_effects": ()}

    def record_filing(self, filing_id: str, matter_id: str, exhibits: tuple[str, ...], signatures_complete: bool, service_list: tuple[str, ...], fee_paid: bool, confidentiality: str) -> dict:
        ok = bool(exhibits) and signatures_complete and bool(service_list) and fee_paid
        filing = {"id": filing_id, "matter_id": matter_id, "exhibits": exhibits, "signatures_complete": signatures_complete, "service_list": service_list, "fee_paid": fee_paid, "confidentiality": confidentiality, "status": "accepted" if ok else "not_ready"}
        self.documents[filing_id] = filing
        return {"ok": ok, "filing": filing, "emitted_event": "FilingRecorded", "side_effects": ()}

    def attach_document(self, document_id: str, matter_id: str, document_set: str, privilege_basis: str | None, confidentiality: str, bates: str, source_hash: str) -> dict:
        doc = {"id": document_id, "matter_id": matter_id, "document_set": document_set, "privilege_basis": privilege_basis, "confidentiality": confidentiality, "bates": bates, "source_hash": source_hash, "custody_events": (("collected", source_hash),), "production_ready": False}
        self.documents[document_id] = doc
        return {"ok": True, "document": doc, "side_effects": ()}

    def review_privilege(self, document_id: str, reviewer: str, basis: str | None, redactions: tuple[str, ...] = ()) -> dict:
        doc = dict(self.documents[document_id]); privileged = bool(basis)
        doc.update({"privilege_basis": basis, "reviewer": reviewer, "redactions": redactions, "production_ready": not privileged or bool(redactions), "privilege_log_required": privileged})
        self.documents[document_id] = doc
        return {"ok": True, "document": doc, "side_effects": ()}

    def approve_budget(self, budget_id: str, matter_id: str, phase_caps: dict[str, float], reserve_estimate: float) -> dict:
        budget = {"id": budget_id, "matter_id": matter_id, "phase_caps": phase_caps, "reserve_estimate": reserve_estimate, "approved_spend": 0.0, "status": "approved" if phase_caps else "blocked"}
        self.budgets[budget_id] = budget
        return {"ok": budget["status"] == "approved", "budget": budget, "side_effects": ()}

    def review_invoice(self, invoice_id: str, budget_id: str, counsel_id: str, lines: tuple[dict, ...]) -> dict:
        counsel = self.counsel[counsel_id]; findings = []
        total = 0.0
        for line in lines:
            total += line["hours"] * line["rate"]
            if line["timekeeper"] not in counsel["rate_card"] or line["rate"] > counsel["rate_card"].get(line["timekeeper"], 0): findings.append("rate_mismatch")
            if len(line.get("narrative", "")) < 16: findings.append("poor_narrative")
            if line.get("block_billing"): findings.append("block_billing")
        invoice = {"id": invoice_id, "budget_id": budget_id, "counsel_id": counsel_id, "total": round(total, 2), "findings": tuple(dict.fromkeys(findings)), "status": "adjustment_required" if findings else "approved"}
        self.invoices[invoice_id] = invoice
        return {"ok": not findings, "invoice": invoice, "side_effects": ()}

    def simulate_exposure(self, matter_id: str, damages: float, defense_offset: float, insurance_recovery: float, venue_risk: float) -> dict:
        base = max(0, damages - defense_offset - insurance_recovery)
        exposure = {"matter_id": matter_id, "best": round(base * 0.25, 2), "base": round(base * venue_risk, 2), "worst": round(base * 1.6, 2), "drivers": ("damages", "defense_offset", "insurance", "venue_risk")}
        self.matters[matter_id]["exposure"] = exposure
        return {"ok": True, "exposure": exposure, "emitted_event": "MatterRiskChanged", "side_effects": ()}

    def record_settlement_offer(self, outcome_id: str, matter_id: str, amount: float, authority_limit: float, approvals: tuple[str, ...], release_terms: tuple[str, ...]) -> dict:
        required = 3 if amount >= 500000 else 2 if amount >= 100000 else 1
        ok = amount <= authority_limit and len(approvals) >= required and bool(release_terms)
        outcome = {"id": outcome_id, "matter_id": matter_id, "amount": amount, "authority_limit": authority_limit, "approvals": approvals, "release_terms": release_terms, "status": "settlement_approved" if ok else "blocked"}
        self.outcomes[outcome_id] = outcome
        return {"ok": ok, "outcome": outcome, "side_effects": ()}

    def close_matter(self, matter_id: str, outcome_id: str) -> dict:
        matter = dict(self.matters[matter_id]); outcome = self.outcomes[outcome_id]
        matter["status"] = "closed" if outcome["status"] == "settlement_approved" else "blocked"
        matter["timeline"] = matter["timeline"] + (("closed", outcome_id),)
        self.matters[matter_id] = matter
        return {"ok": matter["status"] == "closed", "matter": matter, "emitted_event": "MatterClosed", "side_effects": ()}

    def assistant_legal_work_preview(self, document: str, instruction: str) -> dict:
        plan = document_instruction_plan(document, instruction)
        crud = datastore_crud_plan("update", table="legal_matter_management_legal_matter", payload={"instruction": instruction})
        return {"ok": plan["ok"] and crud["ok"], "document_plan": plan, "crud_preview": crud, "requires_confirmation": True, "legal_notice": "draft_not_legal_advice_until_approved", "side_effects": ()}

    def app_contract(self) -> dict:
        return {"format": "appgen.legal-matter-management.standalone-app.v1", "ok": True, "pbc": PBC_KEY, "owned_tables": LEGAL_MATTER_MANAGEMENT_OWNED_TABLES, "database_backends": LEGAL_MATTER_MANAGEMENT_ALLOWED_DATABASE_BACKENDS, "event_contract": "AppGen-X", "stream_engine_picker_visible": False, "schema": legal_matter_management_build_schema_contract(), "services": legal_matter_management_build_service_contract(), "routes": legal_matter_management_build_api_contract(), "permissions": legal_matter_management_permissions_contract(), "ui": legal_matter_management_ui_contract(), "workbench": legal_matter_management_render_workbench(), "forms": form_catalog(), "wizards": wizard_catalog(), "controls": control_catalog(), "agent": chatbot_interface_contract(), "composed_agent": composed_agent_contribution(), "dsl": {"pbc": PBC_KEY, "skills_namespace": f"{PBC_KEY}_skills", "single_pbc_app": True}, "side_effects": ()}

    def run_demo(self) -> dict:
        cfg = self.configure()
        matter = self.open_matter("MAT-001", "litigation", "KE-Commercial-Court", "critical", True, ("counterparty-a",))
        duplicate = self.open_matter("MAT-DUP", "litigation", "KE-Commercial-Court", "medium", False, ("counterparty-a",))
        conflict_block = self.screen_conflicts("MAT-001", ("counterparty-a",), former_client=True)
        conflict = self.screen_conflicts("MAT-001", ("counterparty-a",), former_client=True, waiver="GC waiver", wall_required=True)
        counsel_bad = self.assign_counsel("OC-BAD", "MAT-001", "Firm Bad", False, True, {"partner": 500}, ("pleadings",))
        counsel = self.assign_counsel("OC-001", "MAT-001", "Firm A", True, True, {"partner": 500, "associate": 250}, ("pleadings", "discovery"))
        hold = self.issue_legal_hold("HOLD-001", "MAT-001", ("custodian-1", "custodian-2"), ("email", "drive"), ("2025-01-01", "2026-05-30"), ("project alpha",))
        ack = self.acknowledge_hold("HOLD-001", "custodian-1")
        deadline_bad = self.compute_deadline("DL-BAD", "MAT-001", 10, 14, "KE", True, ("lawyer-1",))
        deadline = self.compute_deadline("DL-001", "MAT-001", 10, 14, "KE", True, ("lawyer-1", "lawyer-2"))
        filing = self.record_filing("FIL-001", "MAT-001", ("pleading.pdf", "exhibit-a.pdf"), True, ("party-a",), True, "confidential")
        doc = self.attach_document("DOC-001", "MAT-001", "evidence", None, "confidential", "BATES-1", "hash-1")
        privilege = self.review_privilege("DOC-001", "reviewer-1", "attorney_client", ("legal advice paragraph",))
        budget = self.approve_budget("BUD-001", "MAT-001", {"pleadings": 25000, "discovery": 60000}, 120000)
        invoice_bad = self.review_invoice("INV-BAD", "BUD-001", "OC-001", ({"timekeeper": "partner", "hours": 2, "rate": 700, "narrative": "call", "block_billing": True},))
        invoice = self.review_invoice("INV-001", "BUD-001", "OC-001", ({"timekeeper": "associate", "hours": 4, "rate": 250, "narrative": "Drafted motion and reviewed exhibits", "block_billing": False},))
        exposure = self.simulate_exposure("MAT-001", 900000, 150000, 200000, 0.55)
        settlement_bad = self.record_settlement_offer("OUT-BAD", "MAT-001", 600000, 550000, ("gc",), ("release",))
        settlement = self.record_settlement_offer("OUT-001", "MAT-001", 450000, 550000, ("gc", "cfo"), ("release", "confidentiality"))
        closed = self.close_matter("MAT-001", "OUT-001")
        assistant = self.assistant_legal_work_preview("complaint and hold memo", "draft matter update and hold scope")
        checks = (cfg["ok"], matter["ok"], duplicate["ok"] is False, conflict_block["ok"] is False, conflict["ok"], counsel_bad["ok"] is False, counsel["ok"], hold["ok"], ack["ok"], deadline_bad["ok"] is False, deadline["ok"], filing["ok"], doc["ok"], privilege["ok"], budget["ok"], invoice_bad["ok"] is False, invoice["ok"], exposure["ok"], settlement_bad["ok"] is False, settlement["ok"], closed["ok"], assistant["ok"])
        return {"ok": all(checks), "duplicate": duplicate, "conflict_block": conflict_block, "deadline_bad": deadline_bad, "invoice_bad": invoice_bad, "settlement_bad": settlement_bad, "closed": closed, "assistant": assistant, "app_contract": self.app_contract(), "side_effects": ()}

def single_pbc_app_contract() -> dict:
    return LegalMatterManagementStandaloneApp().app_contract()

def standalone_smoke_test() -> dict:
    app = LegalMatterManagementStandaloneApp(); demo = app.run_demo(); runtime = legal_matter_management_runtime_smoke(); contract = single_pbc_app_contract()
    return {"ok": demo["ok"] and runtime["ok"] and contract["ok"] and bool(LEGAL_MATTER_MANAGEMENT_EMITTED_EVENT_TYPES) and contract["stream_engine_picker_visible"] is False, "demo": demo, "runtime": runtime, "contract": contract, "side_effects": ()}
