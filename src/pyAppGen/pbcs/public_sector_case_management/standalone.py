"""Standalone public-sector case-management application contract.

This is an in-memory, side-effect-free implementation used by release audits to
prove a single-PBC composed application can operate the public-sector case domain
with forms, workflows, controls, AI assistant previews, and owned datastore
contracts.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from hashlib import sha256
from typing import Any

from .agent import chatbot_interface_contract, composed_agent_contribution, datastore_crud_plan, document_instruction_plan
from .controls import control_catalog, evaluate_control
from .forms import form_catalog
from .runtime import (
    PUBLIC_SECTOR_CASE_MANAGEMENT_ALLOWED_DATABASE_BACKENDS,
    PUBLIC_SECTOR_CASE_MANAGEMENT_CONSUMED_EVENT_TYPES,
    PUBLIC_SECTOR_CASE_MANAGEMENT_EMITTED_EVENT_TYPES,
    PUBLIC_SECTOR_CASE_MANAGEMENT_OWNED_TABLES,
    PUBLIC_SECTOR_CASE_MANAGEMENT_REQUIRED_EVENT_TOPIC,
    public_sector_case_management_build_api_contract,
    public_sector_case_management_build_schema_contract,
    public_sector_case_management_build_service_contract,
    public_sector_case_management_configure_runtime,
    public_sector_case_management_empty_state,
    public_sector_case_management_permissions_contract,
    public_sector_case_management_receive_event,
    public_sector_case_management_register_rule,
    public_sector_case_management_runtime_smoke,
    public_sector_case_management_set_parameter,
)
from .ui import public_sector_case_management_render_workbench, public_sector_case_management_ui_contract
from .wizards import wizard_catalog

PBC_KEY = "public_sector_case_management"


def _digest(value: Any) -> str:
    return sha256(repr(value).encode("utf-8")).hexdigest()


@dataclass
class PublicSectorCaseManagementStandaloneApp:
    tenant: str = "tenant-public-case-001"
    state: dict = field(default_factory=public_sector_case_management_empty_state)
    intakes: dict[str, dict] = field(default_factory=dict)
    cases: dict[str, dict] = field(default_factory=dict)
    households: dict[str, dict] = field(default_factory=dict)
    screenings: dict[str, dict] = field(default_factory=dict)
    evidence: dict[str, dict] = field(default_factory=dict)
    checklists: dict[str, dict] = field(default_factory=dict)
    determinations: dict[str, dict] = field(default_factory=dict)
    notices: dict[str, dict] = field(default_factory=dict)
    referrals: dict[str, dict] = field(default_factory=dict)
    appeals: dict[str, dict] = field(default_factory=dict)
    hearings: dict[str, dict] = field(default_factory=dict)
    slas: dict[str, dict] = field(default_factory=dict)
    privacy_events: dict[str, dict] = field(default_factory=dict)
    overrides: dict[str, dict] = field(default_factory=dict)
    fraud_handoffs: dict[str, dict] = field(default_factory=dict)

    def configure(self, database_backend: str = "postgresql") -> dict:
        configured = public_sector_case_management_configure_runtime(
            self.state,
            {"database_backend": database_backend, "event_topic": PUBLIC_SECTOR_CASE_MANAGEMENT_REQUIRED_EVENT_TOPIC},
        )
        self.state = configured["state"]
        for name, value in (
            ("default_intake_sla_hours", 24),
            ("eligibility_sla_days", 30),
            ("notice_lead_days", 10),
            ("appeal_window_days", 30),
            ("privacy_purpose_required", True),
            ("agent_confirmation_required", True),
        ):
            result = public_sector_case_management_set_parameter(self.state, name, value)
            self.state = result["state"]
        for rule_id in (
            "intake_envelope_complete",
            "jurisdiction_determined",
            "evidence_sufficient_for_rule",
            "notice_has_rule_citation",
            "appeal_timeliness_and_standing",
            "purpose_based_access_declared",
            "manual_override_governed",
            "agent_mutations_require_confirmation",
        ):
            result = public_sector_case_management_register_rule(self.state, {"rule_id": rule_id, "scope": "case"})
            self.state = result["state"]
        inbound = public_sector_case_management_receive_event(
            self.state,
            {"event_type": PUBLIC_SECTOR_CASE_MANAGEMENT_CONSUMED_EVENT_TYPES[0], "idempotency_key": "public-case-policy-001"},
        )
        self.state = inbound["state"]
        return {"ok": configured["ok"] and inbound["ok"], "side_effects": ()}

    def capture_intake(self, intake_id: str, channel: str, language: str, program: str, contactability: str, urgency: str = "standard") -> dict:
        control = evaluate_control("intake_envelope_complete", {"channel": channel, "language": language, "program": program, "contactability": contactability})
        intake = {"id": intake_id, "tenant": self.tenant, "channel": channel, "language": language, "program": program, "contactability": contactability, "urgency": urgency, "status": "accepted" if control["ok"] else "rejected", "blockers": control["failures"]}
        self.intakes[intake_id] = intake
        return {"ok": control["ok"], "intake": intake, "side_effects": ()}

    def open_case(self, case_id: str, intake_id: str, applicant: str, jurisdiction: str | None, confidential: bool = False) -> dict:
        control = evaluate_control("jurisdiction_determined", {"jurisdiction": jurisdiction})
        ok = intake_id in self.intakes and bool(applicant) and control["ok"]
        case = {"id": case_id, "tenant": self.tenant, "intake_id": intake_id, "applicant": applicant, "jurisdiction": jurisdiction, "confidential": confidential, "status": "open" if ok else "routing_blocked", "blockers": control["failures"]}
        self.cases[case_id] = case
        return {"ok": ok, "case": case, "side_effects": ()}

    def record_household(self, household_id: str, case_id: str, members: tuple[str, ...], representative: str | None = None, verified: bool = False) -> dict:
        control = evaluate_control("representative_authority_verified", {"representative": representative, "verified": verified})
        ok = case_id in self.cases and bool(members) and control["ok"]
        household = {"id": household_id, "tenant": self.tenant, "case_id": case_id, "members": tuple(members), "representative": representative, "verified": verified, "recalculation_required": True, "status": "current" if ok else "review", "blockers": control["failures"]}
        self.households[household_id] = household
        return {"ok": ok, "household": household, "side_effects": ()}

    def screen_programs(self, screening_id: str, case_id: str, needs: tuple[str, ...]) -> dict:
        candidates = tuple(f"{need}_program" for need in needs) or ("general_assistance",)
        screening = {"id": screening_id, "tenant": self.tenant, "case_id": case_id, "needs": tuple(needs), "candidate_programs": candidates, "confidence": 0.82 if needs else 0.45, "incompatibilities": (), "status": "ready" if case_id in self.cases else "blocked"}
        self.screenings[screening_id] = screening
        return {"ok": case_id in self.cases, "screening": screening, "side_effects": ()}

    def ingest_evidence(self, evidence_id: str, case_id: str, document_class: str, asserted_facts: tuple[str, ...], confidence: float, linked_question: str) -> dict:
        sufficiency = "satisfied" if confidence >= 0.75 and asserted_facts else "manual_review"
        control = evaluate_control("evidence_sufficient_for_rule", {"sufficiency": sufficiency})
        evidence = {"id": evidence_id, "tenant": self.tenant, "case_id": case_id, "document_class": document_class, "asserted_facts": tuple(asserted_facts), "confidence": confidence, "linked_question": linked_question, "sufficiency": sufficiency, "scan_hash": _digest((document_class, asserted_facts)), "blockers": control["failures"]}
        self.evidence[evidence_id] = evidence
        return {"ok": case_id in self.cases and control["ok"], "evidence": evidence, "side_effects": ()}

    def generate_checklist(self, checklist_id: str, case_id: str, items: tuple[str, ...], expired: bool = False, tolled: bool = False) -> dict:
        control = evaluate_control("missing_information_due_date_valid", {"expired": expired, "tolled": tolled})
        checklist = {"id": checklist_id, "tenant": self.tenant, "case_id": case_id, "items": tuple(items), "expired": expired, "tolled": tolled, "status": "active" if control["ok"] else "exception", "blockers": control["failures"]}
        self.checklists[checklist_id] = checklist
        return {"ok": case_id in self.cases and control["ok"], "checklist": checklist, "side_effects": ()}

    def determine_eligibility(self, determination_id: str, case_id: str, evidence_state: str, effective_start: str, retroactive_start: str | None = None) -> dict:
        control = evaluate_control("evidence_sufficient_for_rule", {"sufficiency": evidence_state})
        ok = case_id in self.cases and control["ok"] and bool(effective_start)
        determination = {"id": determination_id, "tenant": self.tenant, "case_id": case_id, "evidence_state": evidence_state, "effective_start": effective_start, "retroactive_start": retroactive_start, "status": "eligible" if ok else "blocked", "blockers": control["failures"]}
        self.determinations[determination_id] = determination
        return {"ok": ok, "determination": determination, "side_effects": ()}

    def render_notice(self, notice_id: str, case_id: str, notice_type: str, citation: str | None, fact_snapshot: dict | None, delivery_channel: str) -> dict:
        control = evaluate_control("notice_has_rule_citation", {"citation": citation, "fact_snapshot": fact_snapshot})
        notice = {"id": notice_id, "tenant": self.tenant, "case_id": case_id, "notice_type": notice_type, "citation": citation, "fact_snapshot": dict(fact_snapshot or {}), "delivery_channel": delivery_channel, "barcode": _digest((case_id, notice_id))[:12], "status": "ready" if control["ok"] else "blocked", "blockers": control["failures"]}
        self.notices[notice_id] = notice
        return {"ok": case_id in self.cases and control["ok"], "notice": notice, "side_effects": ()}

    def create_referral(self, referral_id: str, case_id: str, service: str, organization: str, includes_restricted: bool = False, override: bool = False) -> dict:
        control = evaluate_control("referral_packet_privacy_safe", {"includes_restricted": includes_restricted, "override": override})
        referral = {"id": referral_id, "tenant": self.tenant, "case_id": case_id, "service": service, "organization": organization, "privacy_safe": control["ok"], "status": "pending" if control["ok"] else "blocked", "blockers": control["failures"]}
        self.referrals[referral_id] = referral
        return {"ok": case_id in self.cases and control["ok"], "referral": referral, "side_effects": ()}

    def intake_appeal(self, appeal_id: str, case_id: str, standing: bool, timely: bool, requested_remedy: str, rejection_reason: str | None = None) -> dict:
        control = evaluate_control("appeal_timeliness_and_standing", {"standing": standing, "timely": timely, "rejection_reason": rejection_reason})
        appeal = {"id": appeal_id, "tenant": self.tenant, "case_id": case_id, "standing": standing, "timely": timely, "requested_remedy": requested_remedy, "status": "accepted" if control["ok"] else "rejected", "rejection_reason": rejection_reason, "blockers": control["failures"]}
        self.appeals[appeal_id] = appeal
        return {"ok": case_id in self.cases and control["ok"], "appeal": appeal, "side_effects": ()}

    def assemble_hearing_packet(self, packet_id: str, appeal_id: str, issue: str | None, chronology: tuple[str, ...], evidence_index: tuple[str, ...], notice_history: tuple[str, ...], rule_basis: str | None) -> dict:
        control = evaluate_control("hearing_packet_complete", {"issue": issue, "chronology": chronology, "evidence_index": evidence_index, "notice_history": notice_history, "rule_basis": rule_basis})
        packet = {"id": packet_id, "tenant": self.tenant, "appeal_id": appeal_id, "issue": issue, "chronology": tuple(chronology), "evidence_index": tuple(evidence_index), "notice_history": tuple(notice_history), "rule_basis": rule_basis, "served_hash": _digest((appeal_id, issue, chronology, evidence_index, notice_history, rule_basis)), "status": "served" if control["ok"] else "incomplete", "blockers": control["failures"]}
        self.hearings[packet_id] = packet
        return {"ok": appeal_id in self.appeals and control["ok"], "packet": packet, "side_effects": ()}

    def manage_sla(self, sla_id: str, case_id: str, expired: bool, pause_reason: str | None = None) -> dict:
        control = evaluate_control("sla_clock_not_expired", {"expired": expired, "pause_reason": pause_reason})
        sla = {"id": sla_id, "tenant": self.tenant, "case_id": case_id, "expired": expired, "pause_reason": pause_reason, "status": "on_track" if control["ok"] else "late_exception", "blockers": control["failures"]}
        self.slas[sla_id] = sla
        return {"ok": case_id in self.cases and control["ok"], "sla": sla, "side_effects": ()}

    def declare_purpose_access(self, access_id: str, case_id: str, sensitive: bool, purpose: str | None, marker: str | None = None, masked: bool = True) -> dict:
        purpose_control = evaluate_control("purpose_based_access_declared", {"sensitive": sensitive, "purpose": purpose})
        marker_control = evaluate_control("confidentiality_marker_enforced", {"marker": marker, "masked": masked})
        ok = case_id in self.cases and purpose_control["ok"] and marker_control["ok"]
        access = {"id": access_id, "tenant": self.tenant, "case_id": case_id, "sensitive": sensitive, "purpose": purpose, "marker": marker, "masked": masked, "status": "allowed" if ok else "denied", "blockers": purpose_control["failures"] + marker_control["failures"]}
        self.privacy_events[access_id] = access
        return {"ok": ok, "access": access, "side_effects": ()}

    def approve_override(self, override_id: str, case_id: str, override_type: str, justification: str | None, approver: str | None, expiry: str | None) -> dict:
        control = evaluate_control("manual_override_governed", {"override": True, "justification": justification, "approver": approver, "expiry": expiry})
        override = {"id": override_id, "tenant": self.tenant, "case_id": case_id, "override_type": override_type, "justification": justification, "approver": approver, "expiry": expiry, "status": "approved" if control["ok"] else "blocked", "blockers": control["failures"]}
        self.overrides[override_id] = override
        return {"ok": case_id in self.cases and control["ok"], "override": override, "side_effects": ()}

    def prepare_fraud_handoff(self, handoff_id: str, case_id: str, reason_code: str, approved_evidence: tuple[str, ...], investigative_notes_visible: bool = False) -> dict:
        control = evaluate_control("fraud_handoff_boundary", {"investigative_notes_visible": investigative_notes_visible})
        handoff = {"id": handoff_id, "tenant": self.tenant, "case_id": case_id, "reason_code": reason_code, "approved_evidence": tuple(approved_evidence), "originating_case_disclosure": "referral_occurred_only", "status": "ready" if control["ok"] else "boundary_violation", "blockers": control["failures"]}
        self.fraud_handoffs[handoff_id] = handoff
        return {"ok": case_id in self.cases and control["ok"], "handoff": handoff, "side_effects": ()}

    def assistant_case_action_preview(self, document: str, instruction: str, confirmed: bool = False) -> dict:
        control = evaluate_control("agent_mutations_require_confirmation", {"confirmed": confirmed})
        document_plan = document_instruction_plan(document, instruction)
        crud_preview = datastore_crud_plan("update", table="public_sector_case_management_citizen_case", payload={"instruction": instruction})
        return {"ok": document_plan["ok"] and crud_preview["ok"] and control["ok"], "document_plan": document_plan, "crud_preview": crud_preview, "control": control, "requires_confirmation": not confirmed, "side_effects": ()}

    def app_contract(self) -> dict:
        return {"format": "appgen.public-sector-case-management.standalone-app.v1", "ok": True, "pbc": PBC_KEY, "owned_tables": PUBLIC_SECTOR_CASE_MANAGEMENT_OWNED_TABLES, "database_backends": PUBLIC_SECTOR_CASE_MANAGEMENT_ALLOWED_DATABASE_BACKENDS, "event_contract": "AppGen-X", "stream_engine_picker_visible": False, "schema": public_sector_case_management_build_schema_contract(), "services": public_sector_case_management_build_service_contract(), "routes": public_sector_case_management_build_api_contract(), "permissions": public_sector_case_management_permissions_contract(), "ui": public_sector_case_management_ui_contract(), "workbench": public_sector_case_management_render_workbench(), "forms": form_catalog(), "wizards": wizard_catalog(), "controls": control_catalog(), "agent": chatbot_interface_contract(), "composed_agent": composed_agent_contribution(), "dsl": {"pbc": PBC_KEY, "skills_namespace": f"{PBC_KEY}_skills", "single_pbc_app": True}, "side_effects": ()}

    def run_demo(self) -> dict:
        configured = self.configure()
        weak_intake = self.capture_intake("IN0", "portal", "en", "housing", "")
        intake = self.capture_intake("IN1", "portal", "en", "housing", "reachable")
        blocked_case = self.open_case("C0", "IN1", "Amina", None)
        case = self.open_case("C1", "IN1", "Amina", "north", confidential=True)
        unverified_rep = self.record_household("H0", "C1", ("Amina",), "Legal Aid", False)
        household = self.record_household("H1", "C1", ("Amina", "Child"), "Legal Aid", True)
        screening = self.screen_programs("S1", "C1", ("housing", "food"))
        weak_evidence = self.ingest_evidence("E0", "C1", "pay_stub", (), 0.40, "income")
        evidence = self.ingest_evidence("E1", "C1", "lease", ("residency",), 0.90, "residency")
        expired_checklist = self.generate_checklist("CL0", "C1", ("id",), expired=True, tolled=False)
        checklist = self.generate_checklist("CL1", "C1", ("id",), expired=True, tolled=True)
        blocked_determination = self.determine_eligibility("D0", "C1", "manual_review", "2026-01-01")
        determination = self.determine_eligibility("D1", "C1", "satisfied", "2026-01-01", "2025-12-01")
        bad_notice = self.render_notice("N0", "C1", "denial", None, {}, "mail")
        notice = self.render_notice("N1", "C1", "approval", "housing-101", {"eligible": True}, "mail")
        bad_referral = self.create_referral("R0", "C1", "housing navigation", "Partner", includes_restricted=True)
        referral = self.create_referral("R1", "C1", "housing navigation", "Partner")
        bad_appeal = self.intake_appeal("A0", "C1", standing=True, timely=False, requested_remedy="approve")
        appeal = self.intake_appeal("A1", "C1", standing=True, timely=True, requested_remedy="approve")
        bad_packet = self.assemble_hearing_packet("HP0", "A1", None, (), (), (), None)
        packet = self.assemble_hearing_packet("HP1", "A1", "denial", ("intake",), ("E1",), ("N1",), "housing-101")
        late_sla = self.manage_sla("SLA0", "C1", expired=True)
        sla = self.manage_sla("SLA1", "C1", expired=True, pause_reason="citizen response window")
        bad_access = self.declare_purpose_access("P0", "C1", sensitive=True, purpose=None)
        access = self.declare_purpose_access("P1", "C1", sensitive=True, purpose="eligibility processing", marker="protected_address", masked=True)
        bad_override = self.approve_override("O0", "C1", "hardship", None, "supervisor", "2026-12-31")
        override = self.approve_override("O1", "C1", "hardship", "emergency shelter", "supervisor", "2026-12-31")
        bad_fraud = self.prepare_fraud_handoff("F0", "C1", "identity_conflict", ("E1",), investigative_notes_visible=True)
        fraud = self.prepare_fraud_handoff("F1", "C1", "identity_conflict", ("E1",))
        agent_bad = self.assistant_case_action_preview("packet", "update case", False)
        agent = self.assistant_case_action_preview("packet", "update case", True)
        checks = (configured["ok"], weak_intake["ok"] is False, intake["ok"], blocked_case["ok"] is False, case["ok"], unverified_rep["ok"] is False, household["ok"], screening["ok"], weak_evidence["ok"] is False, evidence["ok"], expired_checklist["ok"] is False, checklist["ok"], blocked_determination["ok"] is False, determination["ok"], bad_notice["ok"] is False, notice["ok"], bad_referral["ok"] is False, referral["ok"], bad_appeal["ok"] is False, appeal["ok"], bad_packet["ok"] is False, packet["ok"], late_sla["ok"] is False, sla["ok"], bad_access["ok"] is False, access["ok"], bad_override["ok"] is False, override["ok"], bad_fraud["ok"] is False, fraud["ok"], agent_bad["ok"] is False, agent["ok"])
        return {"ok": all(checks), "app_contract": self.app_contract(), "side_effects": ()}


def single_pbc_app_contract() -> dict:
    return PublicSectorCaseManagementStandaloneApp().app_contract()


def standalone_smoke_test() -> dict:
    app = PublicSectorCaseManagementStandaloneApp()
    demo = app.run_demo()
    runtime = public_sector_case_management_runtime_smoke()
    contract = single_pbc_app_contract()
    return {"ok": demo["ok"] and runtime["ok"] and contract["ok"] and bool(PUBLIC_SECTOR_CASE_MANAGEMENT_EMITTED_EVENT_TYPES), "demo": demo, "runtime": runtime, "contract": contract, "side_effects": ()}
