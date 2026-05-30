"""Standalone research grants management application contract."""
from __future__ import annotations

from dataclasses import dataclass, field
from hashlib import sha256
from typing import Any

from .agent import chatbot_interface_contract, composed_agent_contribution, datastore_crud_plan, document_instruction_plan
from .controls import control_catalog, evaluate_control
from .forms import form_catalog
from .runtime import (
    RESEARCH_GRANTS_MANAGEMENT_ALLOWED_DATABASE_BACKENDS,
    RESEARCH_GRANTS_MANAGEMENT_CONSUMED_EVENT_TYPES,
    RESEARCH_GRANTS_MANAGEMENT_EMITTED_EVENT_TYPES,
    RESEARCH_GRANTS_MANAGEMENT_OWNED_TABLES,
    RESEARCH_GRANTS_MANAGEMENT_REQUIRED_EVENT_TOPIC,
    research_grants_management_build_api_contract,
    research_grants_management_build_schema_contract,
    research_grants_management_build_service_contract,
    research_grants_management_configure_runtime,
    research_grants_management_empty_state,
    research_grants_management_permissions_contract,
    research_grants_management_receive_event,
    research_grants_management_register_rule,
    research_grants_management_runtime_smoke,
    research_grants_management_set_parameter,
)
from .ui import research_grants_management_render_workbench, research_grants_management_ui_contract
from .wizards import wizard_catalog

PBC_KEY = "research_grants_management"


def _digest(value: Any) -> str:
    return sha256(repr(value).encode("utf-8")).hexdigest()


@dataclass
class ResearchGrantsManagementStandaloneApp:
    tenant: str = "tenant-research-001"
    state: dict = field(default_factory=research_grants_management_empty_state)
    opportunities: dict[str, dict] = field(default_factory=dict)
    proposals: dict[str, dict] = field(default_factory=dict)
    budgets: dict[str, dict] = field(default_factory=dict)
    compliance: dict[str, dict] = field(default_factory=dict)
    awards: dict[str, dict] = field(default_factory=dict)
    amendments: dict[str, list[dict]] = field(default_factory=dict)
    subawards: dict[str, dict] = field(default_factory=dict)
    reports: dict[str, dict] = field(default_factory=dict)
    effort: dict[str, dict] = field(default_factory=dict)

    def configure(self, database_backend="postgresql"):
        cfg = research_grants_management_configure_runtime(self.state, {"database_backend": database_backend, "event_topic": RESEARCH_GRANTS_MANAGEMENT_REQUIRED_EVENT_TOPIC})
        self.state = cfg["state"]
        for name, value in (("proposal_routing_sla_hours", 72), ("budget_variance_tolerance", 0.01), ("compliance_status_max_age_days", 14), ("agent_confirmation_required", True)):
            result = research_grants_management_set_parameter(self.state, name, value)
            self.state = result["state"]
        for rule_id in ("opportunity_has_traceable_notice", "eligibility_pass_or_justified_override", "limited_submission_slot_available", "proposal_sections_submission_ready", "budget_line_allowable_or_justified", "award_readiness_gates_clear", "subaward_prime_alignment", "agent_mutations_require_confirmation"):
            result = research_grants_management_register_rule(self.state, {"rule_id": rule_id, "scope": "sponsored_research"})
            self.state = result["state"]
        inbound = research_grants_management_receive_event(self.state, {"event_type": RESEARCH_GRANTS_MANAGEMENT_CONSUMED_EVENT_TYPES[0], "idempotency_key": "research-policy-001"})
        self.state = inbound["state"]
        return {"ok": cfg["ok"] and inbound["ok"], "side_effects": ()}

    def register_opportunity(self, opportunity_id, sponsor, program_code, sponsor_deadline, source_archive_digest, **extra):
        facts = {"sponsor": sponsor, "program_code": program_code, "sponsor_deadline": sponsor_deadline, "source_archive_digest": source_archive_digest}
        ctl = evaluate_control("opportunity_has_traceable_notice", facts)
        row = {"id": opportunity_id, "tenant": self.tenant, **facts, **extra, "status": "registered" if ctl["ok"] else "incomplete", "blockers": ctl["failures"]}
        self.opportunities[opportunity_id] = row
        return {"ok": ctl["ok"], "opportunity": row, "side_effects": ()}

    def evaluate_eligibility(self, proposal_id, opportunity_id, result, override_justification=None, investigator="pi-1"):
        ctl = evaluate_control("eligibility_pass_or_justified_override", {"result": result, "override_justification": override_justification})
        row = {"id": proposal_id, "tenant": self.tenant, "opportunity_id": opportunity_id, "investigator": investigator, "eligibility_result": result, "override_justification": override_justification, "status": "eligible" if ctl["ok"] else "blocked", "blockers": ctl["failures"]}
        self.proposals[proposal_id] = row
        return {"ok": opportunity_id in self.opportunities and ctl["ok"], "proposal": row, "side_effects": ()}

    def allocate_limited_submission_slot(self, proposal_id, selected_count, slot_count, committee_evidence=None):
        ctl = evaluate_control("limited_submission_slot_available", {"selected_count": selected_count, "slot_count": slot_count})
        proposal = self.proposals.setdefault(proposal_id, {"id": proposal_id, "tenant": self.tenant})
        proposal.update({"limited_submission": True, "selected_count": selected_count, "slot_count": slot_count, "committee_evidence": committee_evidence, "slot_status": "allocated" if ctl["ok"] and committee_evidence else "blocked", "blockers": ctl["failures"] + (() if committee_evidence else ("committee_evidence_missing",))})
        return {"ok": ctl["ok"] and bool(committee_evidence), "proposal": proposal, "side_effects": ()}

    def build_deadline_calendar(self, proposal_id, **deadlines):
        ctl = evaluate_control("deadline_calendar_complete", deadlines)
        proposal = self.proposals.setdefault(proposal_id, {"id": proposal_id, "tenant": self.tenant})
        proposal["deadlines"] = dict(deadlines)
        proposal["deadline_status"] = "complete" if ctl["ok"] else "incomplete"
        proposal["deadline_blockers"] = ctl["failures"]
        return {"ok": ctl["ok"], "proposal": proposal, "side_effects": ()}

    def assemble_proposal_sections(self, proposal_id, sections: dict[str, str]):
        ctl = evaluate_control("proposal_sections_submission_ready", {"sections": sections})
        proposal = self.proposals.setdefault(proposal_id, {"id": proposal_id, "tenant": self.tenant})
        proposal.update({"sections": dict(sections), "submission_status": "ready" if ctl["ok"] else "incomplete", "section_blockers": ctl["failures"]})
        return {"ok": ctl["ok"], "proposal": proposal, "side_effects": ()}

    def validate_budget_line(self, budget_id, proposal_id, category, amount, allowability="allowable", justification=None, prior_approval_reference=None):
        ctl = evaluate_control("budget_line_allowable_or_justified", {"allowability": allowability, "justification": justification, "prior_approval_required": allowability == "restricted", "prior_approval_reference": prior_approval_reference})
        row = {"id": budget_id, "tenant": self.tenant, "proposal_id": proposal_id, "category": category, "amount": amount, "allowability": allowability, "justification": justification, "prior_approval_reference": prior_approval_reference, "status": "cleared" if ctl["ok"] else "blocked", "blockers": ctl["failures"]}
        self.budgets[budget_id] = row
        return {"ok": proposal_id in self.proposals and ctl["ok"], "budget_line": row, "side_effects": ()}

    def approve_cost_share(self, commitment_id, proposal_id, commitment_type, source_account=None, responsible_unit=None, approval_chain=None, amount=0):
        ctl = evaluate_control("cost_share_backed_by_approval", {"commitment_type": commitment_type, "source_account": source_account, "responsible_unit": responsible_unit, "approval_chain": approval_chain})
        row = {"id": commitment_id, "tenant": self.tenant, "proposal_id": proposal_id, "commitment_type": commitment_type, "source_account": source_account, "responsible_unit": responsible_unit, "approval_chain": tuple(approval_chain or ()), "amount": amount, "status": "approved" if ctl["ok"] else "blocked", "blockers": ctl["failures"]}
        self.budgets[commitment_id] = row
        return {"ok": proposal_id in self.proposals and ctl["ok"], "cost_share": row, "side_effects": ()}

    def calculate_indirect_cost(self, budget_id, direct_cost, standard_rate, used_rate, waiver_approver=None, waiver_reason=None, sponsor_citation=None):
        ctl = evaluate_control("indirect_waiver_authorized", {"standard_rate": standard_rate, "used_rate": used_rate, "waiver_approver": waiver_approver, "waiver_reason": waiver_reason, "sponsor_citation": sponsor_citation})
        row = {"id": budget_id, "tenant": self.tenant, "direct_cost": direct_cost, "standard_rate": standard_rate, "used_rate": used_rate, "indirect_cost": round(direct_cost * used_rate, 2), "status": "calculated" if ctl["ok"] else "waiver_blocked", "blockers": ctl["failures"]}
        self.budgets[budget_id] = row
        return {"ok": ctl["ok"], "indirect": row, "side_effects": ()}

    def classify_compliance_dependency(self, requirement_id, proposal_or_award_id, required=True, status="pending", expired=False, stale=False, dependency_type="irb"):
        ctl = evaluate_control("compliance_dependency_current", {"required": required, "status": status, "expired": expired, "stale": stale})
        row = {"id": requirement_id, "tenant": self.tenant, "proposal_or_award_id": proposal_or_award_id, "dependency_type": dependency_type, "status": status, "boundary": "tracks_status_not_protocol_adjudication", "blockers": ctl["failures"]}
        self.compliance[requirement_id] = row
        return {"ok": ctl["ok"], "requirement": row, "side_effects": ()}

    def resolve_restricted_research(self, screening_id, proposal_or_award_id, flagged, resolution=None, clause=None):
        ctl = evaluate_control("restricted_research_resolved", {"flagged": flagged, "resolution": resolution})
        row = {"id": screening_id, "tenant": self.tenant, "proposal_or_award_id": proposal_or_award_id, "flagged": flagged, "resolution": resolution, "triggering_clause": clause, "status": "resolved" if ctl["ok"] else "routed", "blockers": ctl["failures"]}
        self.compliance[screening_id] = row
        return {"ok": ctl["ok"], "screening": row, "side_effects": ()}

    def extract_award_notice(self, award_id, **terms):
        ctl = evaluate_control("award_notice_terms_complete", terms)
        row = {"id": award_id, "tenant": self.tenant, **terms, "status": "terms_extracted" if ctl["ok"] else "redline_or_missing_terms", "blockers": ctl["failures"]}
        self.awards[award_id] = row
        return {"ok": ctl["ok"], "award": row, "side_effects": ()}

    def activate_award(self, award_id, gates: dict[str, bool], authorized_exception=False):
        ctl = evaluate_control("award_readiness_gates_clear", {"gates": gates, "authorized_exception": authorized_exception})
        award = self.awards.setdefault(award_id, {"id": award_id, "tenant": self.tenant})
        award.update({"readiness_gates": dict(gates), "status": "active" if ctl["ok"] else "setup_blocked", "readiness_blockers": ctl["failures"]})
        return {"ok": ctl["ok"], "award": award, "side_effects": ()}

    def append_amendment(self, award_id, amendment_type, effective_date, financial_impact=0, compliance_impact=None, sponsor_document_digest="doc"):
        row = {"award_id": award_id, "sequence": len(self.amendments.get(award_id, ())) + 1, "amendment_type": amendment_type, "effective_date": effective_date, "financial_impact": financial_impact, "compliance_impact": compliance_impact, "sponsor_document_digest": sponsor_document_digest, "evidence_hash": _digest((award_id, amendment_type, effective_date, financial_impact, compliance_impact))}
        self.amendments.setdefault(award_id, []).append(row)
        return {"ok": award_id in self.awards and bool(sponsor_document_digest), "amendment": row, "side_effects": ()}

    def issue_subaward(self, subaward_id, award_id, scope_dates_match, budget_matches, terms_flow_down, monitoring_tier, audit_status="current"):
        ctl = evaluate_control("subaward_prime_alignment", {"scope_dates_match": scope_dates_match, "budget_matches": budget_matches, "terms_flow_down": terms_flow_down, "monitoring_tier": monitoring_tier})
        row = {"id": subaward_id, "tenant": self.tenant, "award_id": award_id, "scope_dates_match": scope_dates_match, "budget_matches": budget_matches, "terms_flow_down": terms_flow_down, "monitoring_tier": monitoring_tier, "audit_status": audit_status, "monitoring_cadence": "monthly" if monitoring_tier == "high" else "quarterly", "status": "issued" if ctl["ok"] else "blocked", "blockers": ctl["failures"]}
        self.subawards[subaward_id] = row
        return {"ok": award_id in self.awards and ctl["ok"], "subaward": row, "side_effects": ()}

    def generate_report_pack(self, report_id, award_id, reported_total, expected_total, basis="sponsor_defined", tolerance=0.01, report_type="technical"):
        ctl = evaluate_control("report_pack_reconciles", {"reported_total": reported_total, "expected_total": expected_total, "basis": basis, "tolerance": tolerance})
        row = {"id": report_id, "tenant": self.tenant, "award_id": award_id, "report_type": report_type, "reported_total": reported_total, "expected_total": expected_total, "basis": basis, "status": "ready" if ctl["ok"] else "reconcile_exception", "blockers": ctl["failures"]}
        self.reports[report_id] = row
        return {"ok": award_id in self.awards and ctl["ok"], "report_pack": row, "side_effects": ()}

    def certify_effort(self, certification_id, award_id, committed_effort, charged_effort, mutates_payroll=False, exception_reason=None):
        over = charged_effort > committed_effort
        ctl = evaluate_control("effort_boundary_respected", {"mutates_payroll": mutates_payroll, "over_commitment": over, "exception_reason": exception_reason})
        row = {"id": certification_id, "tenant": self.tenant, "award_id": award_id, "committed_effort": committed_effort, "charged_effort": charged_effort, "boundary": "award_obligation_only", "status": "certified" if ctl["ok"] else "exception", "blockers": ctl["failures"]}
        self.effort[certification_id] = row
        return {"ok": award_id in self.awards and ctl["ok"], "effort": row, "side_effects": ()}

    def simulate_no_cost_extension(self, award_id, current_end, requested_end, unobligated_balance, justification):
        return {"ok": award_id in self.awards and bool(justification), "mutates_live_records": False, "award_id": award_id, "current_end": current_end, "requested_end": requested_end, "unobligated_balance": unobligated_balance, "schedule_reflow_hash": _digest((award_id, current_end, requested_end, unobligated_balance, justification)), "side_effects": ()}

    def assistant_document_action_preview(self, document, instruction, confirmed=False):
        ctl = evaluate_control("agent_mutations_require_confirmation", {"confirmed": confirmed})
        doc = document_instruction_plan(document, instruction)
        crud = datastore_crud_plan("create", table="research_grants_management_grant_proposal", payload={"instruction": instruction})
        return {"ok": doc["ok"] and crud["ok"] and ctl["ok"], "document_plan": doc, "crud_preview": crud, "control": ctl, "requires_confirmation": not confirmed, "side_effects": ()}

    def app_contract(self):
        return {"format": "appgen.research-grants-management.standalone-app.v1", "ok": True, "pbc": PBC_KEY, "owned_tables": RESEARCH_GRANTS_MANAGEMENT_OWNED_TABLES, "database_backends": RESEARCH_GRANTS_MANAGEMENT_ALLOWED_DATABASE_BACKENDS, "event_contract": "AppGen-X", "stream_engine_picker_visible": False, "schema": research_grants_management_build_schema_contract(), "services": research_grants_management_build_service_contract(), "routes": research_grants_management_build_api_contract(), "permissions": research_grants_management_permissions_contract(), "ui": research_grants_management_ui_contract(), "workbench": research_grants_management_render_workbench(), "forms": form_catalog(), "wizards": wizard_catalog(), "controls": control_catalog(), "agent": chatbot_interface_contract(), "composed_agent": composed_agent_contribution(), "dsl": {"pbc": PBC_KEY, "skills_namespace": f"{PBC_KEY}_skills", "single_pbc_app": True}, "side_effects": ()}

    def run_demo(self):
        cfg = self.configure()
        bad_opp = self.register_opportunity("O0", "NIH", None, "2026-07-01", None)
        opp = self.register_opportunity("O1", "NIH", "R01", "2026-07-01", "notice-hash", limited_submission_slots=1)
        bad_elig = self.evaluate_eligibility("P0", "O1", "blocked")
        elig = self.evaluate_eligibility("P1", "O1", "pass")
        bad_slot = self.allocate_limited_submission_slot("P1", 2, 1, "minutes")
        slot = self.allocate_limited_submission_slot("P1", 1, 1, "minutes")
        bad_deadline = self.build_deadline_calendar("P1", sponsor_submission="2026-07-01")
        deadline = self.build_deadline_calendar("P1", sponsor_submission="2026-07-01", institutional_routing="2026-06-20", compliance_review="2026-06-15", budget_final="2026-06-18", collaborator_packet="2026-06-12", narrative_freeze="2026-06-22")
        bad_sections = self.assemble_proposal_sections("P1", {"abstract": "approved", "aims": "draft"})
        sections = self.assemble_proposal_sections("P1", {"abstract": "approved", "aims": "approved", "narrative": "approved", "budget_justification": "approved", "biosketches": "approved", "data_plan": "approved"})
        bad_budget = self.validate_budget_line("B0", "P1", "participant_support", 5000, allowability="restricted")
        budget = self.validate_budget_line("B1", "P1", "participant_support", 5000, allowability="restricted", justification="sponsor allowed", prior_approval_reference="PA-1")
        bad_share = self.approve_cost_share("CS0", "P1", "mandatory", source_account="A")
        share = self.approve_cost_share("CS1", "P1", "mandatory", source_account="A", responsible_unit="School", approval_chain=("dean",), amount=10000)
        bad_indirect = self.calculate_indirect_cost("IDC0", 100000, .55, .20)
        indirect = self.calculate_indirect_cost("IDC1", 100000, .55, .20, waiver_approver="vp-research", waiver_reason="sponsor cap", sponsor_citation="RFA")
        bad_comp = self.classify_compliance_dependency("C0", "P1", required=True, status="pending")
        comp = self.classify_compliance_dependency("C1", "P1", required=True, status="approved")
        bad_restrict = self.resolve_restricted_research("X0", "P1", True)
        restrict = self.resolve_restricted_research("X1", "P1", True, resolution="export office approved", clause="publication review")
        bad_award = self.extract_award_notice("A0", total_amount=100000)
        award = self.extract_award_notice("A1", total_amount=100000, obligated_amount=50000, project_start="2026-09-01", project_end="2027-08-31", reporting_schedule="annual")
        bad_active = self.activate_award("A1", {"account_setup": True, "budget_activation": False})
        active = self.activate_award("A1", {"account_setup": True, "budget_activation": True, "compliance_dependencies_clear": True, "effort_allocations": True, "subaward_readiness": True, "deliverable_schedule": True})
        amendment = self.append_amendment("A1", "no_cost_extension", "2027-08-01", sponsor_document_digest="nce-doc")
        bad_sub = self.issue_subaward("S0", "A1", True, False, True, "high")
        sub = self.issue_subaward("S1", "A1", True, True, True, "high")
        bad_report = self.generate_report_pack("R0", "A1", 90, 100)
        report = self.generate_report_pack("R1", "A1", 100, 100)
        bad_effort = self.certify_effort("E0", "A1", .20, .30)
        effort = self.certify_effort("E1", "A1", .20, .30, exception_reason="approved rebudget")
        scenario = self.simulate_no_cost_extension("A1", "2027-08-31", "2028-02-28", 12000, "field work delayed")
        agent_bad = self.assistant_document_action_preview("notice", "create proposal", False)
        agent = self.assistant_document_action_preview("notice", "create proposal", True)
        checks = (cfg["ok"], bad_opp["ok"] is False, opp["ok"], bad_elig["ok"] is False, elig["ok"], bad_slot["ok"] is False, slot["ok"], bad_deadline["ok"] is False, deadline["ok"], bad_sections["ok"] is False, sections["ok"], bad_budget["ok"] is False, budget["ok"], bad_share["ok"] is False, share["ok"], bad_indirect["ok"] is False, indirect["ok"], bad_comp["ok"] is False, comp["ok"], bad_restrict["ok"] is False, restrict["ok"], bad_award["ok"] is False, award["ok"], bad_active["ok"] is False, active["ok"], amendment["ok"], bad_sub["ok"] is False, sub["ok"], bad_report["ok"] is False, report["ok"], bad_effort["ok"] is False, effort["ok"], scenario["mutates_live_records"] is False, agent_bad["ok"] is False, agent["ok"])
        return {"ok": all(checks), "app_contract": self.app_contract(), "side_effects": ()}


def single_pbc_app_contract():
    return ResearchGrantsManagementStandaloneApp().app_contract()


def standalone_smoke_test():
    app = ResearchGrantsManagementStandaloneApp()
    demo = app.run_demo()
    runtime = research_grants_management_runtime_smoke()
    contract = single_pbc_app_contract()
    return {"ok": demo["ok"] and runtime["ok"] and contract["ok"] and bool(RESEARCH_GRANTS_MANAGEMENT_EMITTED_EVENT_TYPES), "demo": demo, "runtime": runtime, "contract": contract, "side_effects": ()}
