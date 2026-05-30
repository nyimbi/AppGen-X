"""Executable improve1 controls for the Research Grants Management PBC."""

from __future__ import annotations

import hashlib
from typing import Any

from .improve1_capabilities import IMPROVE1_CAPABILITIES, Improve1Capability
from .runtime import (
    RESEARCH_GRANTS_MANAGEMENT_ALLOWED_DATABASE_BACKENDS,
    RESEARCH_GRANTS_MANAGEMENT_CONSUMED_EVENT_TYPES,
    RESEARCH_GRANTS_MANAGEMENT_OWNED_TABLES,
    RESEARCH_GRANTS_MANAGEMENT_REQUIRED_EVENT_TOPIC,
    RESEARCH_GRANTS_MANAGEMENT_RUNTIME_TABLES,
)

PBC_KEY = "research_grants_management"
EVENT_CONTRACT = "AppGen-X"
RESEARCH_ALLOWED_DATABASE_BACKENDS = RESEARCH_GRANTS_MANAGEMENT_ALLOWED_DATABASE_BACKENDS
RESEARCH_REQUIRED_EVENT_TOPIC = RESEARCH_GRANTS_MANAGEMENT_REQUIRED_EVENT_TOPIC
RESEARCH_CAPABILITIES: tuple[Improve1Capability, ...] = IMPROVE1_CAPABILITIES
CAPABILITY_BY_NUMBER = {capability.feature_number: capability for capability in RESEARCH_CAPABILITIES}
CAPABILITY_BY_SLUG = {capability.slug: capability for capability in RESEARCH_CAPABILITIES}
RESEARCH_OWNED_TABLES = tuple(
    dict.fromkeys(
        RESEARCH_GRANTS_MANAGEMENT_OWNED_TABLES
        + RESEARCH_GRANTS_MANAGEMENT_RUNTIME_TABLES
        + tuple(f"research_grants_management_{capability.slug}_control" for capability in RESEARCH_CAPABILITIES)
    )
)
RESEARCH_DECLARED_DEPENDENCIES = tuple(
    dict.fromkeys(
        RESEARCH_GRANTS_MANAGEMENT_CONSUMED_EVENT_TYPES
        + (
            "PolicyChanged",
            "AuditEventSealed",
            "OperationalKpiChanged",
            "SponsorOpportunityPublished",
            "InstitutionalHolidayChanged",
            "ProtocolStatusChanged",
            "DisclosureStatusChanged",
            "ExportControlReviewUpdated",
            "PayrollEffortSummaryUpdated",
            "ProcurementApprovalUpdated",
            "SubrecipientProfileUpdated",
            "SponsorCorrespondenceReceived",
            "DocumentStored",
            "FinancialActualsSummarized",
            "TrainingStatusChanged",
        )
    )
)
_BASE_FIELDS = (
    "tenant_id",
    "sponsor_id",
    "opportunity_id",
    "proposal_id",
    "award_id",
    "principal_investigator_id",
    "unit_id",
    "operator_id",
    "policy_version",
    "evidence_references",
)
_FIELD_ROWS = """
1|opportunity_source_id,program_identifier,notice_version,internal_deadline,sponsor_deadline,sponsor_type,archived_source_file
2|eligibility_rule_id,investigator_status,organization_type,career_stage,limited_submission_flag,fit_result,override_justification
3|nomination_workflow_id,internal_call,nominee_packet,committee_decision,alternate_rank,slot_allocation,bypass_exception
4|deadline_calendar_id,sponsor_submission_date,routing_cutoff,compliance_review_due,budget_finalization_due,collaborator_packet_due,narrative_freeze
5|proposal_workspace_id,section_type,section_status,section_owner,due_date,attachment_integrity,submission_blocker
6|compliance_matrix_id,requirement_type,source_clause,disposition,cleared_by,cleared_at,unresolved_check
7|budget_template_id,sponsor_mechanism,budget_period_structure,currency,policy_era,effective_date,template_version
8|budget_line_rule_id,cost_category,allowability_status,restriction_reason,prior_approval_required,justification,rule_explanation
9|cost_share_id,source_account,responsible_unit,approval_chain,commitment_type,timing_expectation,delivered_match_amount
10|indirect_cost_id,rate_base,exclusion_basis,period_split,off_campus_flag,waiver_reason,calculated_amount
11|ethics_boundary_id,review_type,dependency_system,due_date,gating_effect,status_source,boundary_mode
12|protocol_status_projection_id,source_system,status_timestamp,expiration_date,exception_note,staleness_warning,award_setup_gate
13|key_person_roster_id,roster_version,disclosure_status,training_status,sponsor_requirement,submission_named_state,amendment_named_state
14|restricted_research_screen_id,sponsor_clause,foreign_participation,controlled_technology,publication_restriction,review_queue,resolution_state
15|compliance_schedule_id,obligation_type,due_date_rule,escalation_window,owner_assignment,recurrence,generated_requirement
16|award_notice_extraction_id,award_amount,project_period,reporting_schedule,publication_constraint,data_rights,redline_issue
17|award_readiness_checklist_id,account_setup,budget_activation,compliance_dependency,effort_allocation,subaward_readiness,activation_gate
18|amendment_chain_id,amendment_type,sponsor_document,effective_date,changed_terms,financial_impact,compliance_impact
19|pre_award_spending_id,justification,allowable_cost_window,approver,resolution_state,conversion_award_id,loss_decision
20|rebudget_detector_id,transfer_category,threshold_rule,scope_change_flag,participant_support_movement,salary_cap_effect,prior_approval_case
21|no_cost_extension_id,unobligated_balance,scientific_justification,revised_end_date,remaining_deliverable,sponsor_notice_timing,closeout_reflow
22|subrecipient_profile_id,legal_name_history,identifier_set,audit_status,monitoring_tier,foreign_status,document_expiration
23|subaward_reconciliation_id,scope_dates,budget_category_match,indirect_treatment,reporting_date_match,compliance_term_match,issuance_blocker
24|subrecipient_monitoring_id,risk_tier,invoice_pattern,audit_followup,monitoring_outcome,overdue_action,escalation_event
25|deliverable_graph_id,deliverable_type,predecessor_task,gating_condition,contingency_path,owner_role,critical_path_state
26|technical_report_pack_id,accomplishment,project_deviation,publication_update,personnel_update,future_work,submission_state
27|financial_report_pack_id,reportable_expenditure,commitment_amount,cost_share_amount,program_income,unobligated_balance,line_mapping
28|effort_boundary_id,effort_commitment_snapshot,certification_period,certifier,exception_flag,certification_status,boundary_mode
29|payroll_reconciliation_id,labor_summary,planned_effort,salary_cap_rule,certification_window,reason_code,risk_indicator
30|cost_transfer_id,transfer_date,original_charge_context,corrected_destination,justification_narrative,lateness_reason,approval_chain
31|participant_support_id,restricted_category,balance,rebudget_block,sponsor_monitoring_flag,proposal_link,closeout_trace
32|equipment_approval_id,equipment_type,sponsor_approval_required,justification,location,award_link,boundary_mode
33|human_subjects_event_link_id,event_type,impact_award,reporting_obligation,internal_review_queue,sensitive_detail_excluded,continuation_gate
34|data_biosafety_obligation_id,obligation_type,data_use_dependency,controlled_data_rule,repository_deposit,training_prerequisite,gating_effect
35|timeline_ui_id,timeline_level,proposal_event,award_version,amendment_effective_date,deliverable_due_date,drill_through_link
36|role_workbench_id,role_name,queue_preset,layout_variant,record_warning,allowed_action,permission_check
37|calendar_alert_id,deadline_type,aging_bucket,saved_filter,alert_event,role_scope,portfolio_view
38|opportunity_triage_skill_id,announcement_summary,eligibility_fact,deadline_fact,unusual_term,draft_opportunity,human_confirmation
39|proposal_compliance_skill_id,attachment_check,clause_reference,missing_item_finding,accepted_disposition,rejected_disposition,audit_trail
40|budget_assistant_skill_id,draft_budget_period,fringe_estimate,indirect_cost_estimate,flagged_category,rebudget_scenario,draft_status
41|award_summary_skill_id,source_snippet,money_summary,period_summary,reporting_obligation,risky_clause,regeneration_key
42|grant_event_catalog_id,event_type,event_version,payload_contract,outbox_scenario,consumer_projection,sequence_marker
43|outbox_replay_id,deterministic_key,duplicate_delivery_result,projection_rebuild,handler_status,audit_seal,replay_log
44|risk_score_id,risk_category,driver_factor,driver_history,score_value,trend,intervention_queue
45|correspondence_ledger_id,communication_date,sender_role,recipient_role,topic,commitment_made,schedule_impact
46|closeout_readiness_id,final_deliverable_status,subaward_invoice_status,financial_reconciliation,invention_obligation,certification_completion,readiness_score
47|closeout_pack_id,technical_report_status,financial_report_status,subaward_confirmation,equipment_disposition,invention_status,sponsor_acceptance_state
48|retention_audit_id,retention_rule,audit_package_manifest,freeze_state,corrective_amendment,artifact_set,verification_hash
49|release_scenario_id,scenario_name,fixture_id,expected_event_sequence,ui_snapshot,handler_assertion,release_check
50|go_live_gate_id,permission_gate,migration_quality,event_replay_safety,assistant_guardrail,reporting_accuracy,runbook_reference
"""
_DOMAIN_FIELDS = {int(line.split("|", 1)[0]): tuple(line.split("|", 1)[1].split(",")) for line in _FIELD_ROWS.strip().splitlines()}
_PRIMARY_PROOF_FIELDS = {number: f"{CAPABILITY_BY_NUMBER[number].slug}_verified" for number in range(1, 51)}
_FEATURE_FIELDS = {number: _BASE_FIELDS + _DOMAIN_FIELDS[number] + (_PRIMARY_PROOF_FIELDS[number],) for number in range(1, 51)}
_FEATURE_DEPENDENCIES = {
    1: ("SponsorOpportunityPublished", "DocumentStored"),
    4: ("InstitutionalHolidayChanged",),
    11: ("ProtocolStatusChanged",),
    12: ("ProtocolStatusChanged",),
    13: ("DisclosureStatusChanged", "TrainingStatusChanged"),
    14: ("ExportControlReviewUpdated",),
    16: ("DocumentStored",),
    22: ("SubrecipientProfileUpdated",),
    28: ("PayrollEffortSummaryUpdated",),
    29: ("PayrollEffortSummaryUpdated",),
    32: ("ProcurementApprovalUpdated",),
    38: ("SponsorOpportunityPublished", "DocumentStored"),
    41: ("DocumentStored",),
    43: ("AuditEventSealed",),
    45: ("SponsorCorrespondenceReceived",),
    49: ("AuditEventSealed",),
}
_HUMAN_CONFIRMATION_FEATURES = (2, 3, 5, 6, 8, 9, 10, 14, 16, 17, 18, 19, 20, 21, 23, 30, 32, 38, 39, 40, 41, 45, 47, 48, 50)
_APPROVAL_REQUIRED_FEATURES = (2, 3, 6, 8, 9, 10, 14, 16, 17, 18, 19, 20, 21, 23, 30, 31, 32, 38, 39, 40, 45, 47, 48, 50)
_NON_MUTATING_FEATURES = (1, 2, 4, 6, 7, 8, 10, 11, 12, 13, 14, 15, 20, 22, 23, 25, 27, 28, 29, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 46, 48, 49, 50)
_AI_PREVIEW_FEATURES = (5, 6, 8, 16, 20, 26, 27, 35, 38, 39, 40, 41, 44, 49, 50)
_PRE_AWARD_FEATURES = (1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 38, 39, 40)
_COMPLIANCE_FEATURES = (6, 11, 12, 13, 14, 15, 17, 23, 24, 28, 31, 32, 33, 34, 43, 48, 50)
_FINANCIAL_FEATURES = (7, 8, 9, 10, 19, 20, 21, 27, 29, 30, 31, 32, 40, 46, 47, 50)
_PROJECTION_ONLY_FEATURES = (1, 4, 11, 12, 13, 14, 16, 22, 28, 29, 32, 38, 41, 43, 45, 49)


def _digest(value: object) -> str:
    return hashlib.sha256(repr(value).encode("utf-8")).hexdigest()


def _camel(slug: str) -> str:
    return "".join(part.capitalize() for part in slug.split("_"))


def _resolve(capability: Improve1Capability | str | int) -> Improve1Capability | None:
    if isinstance(capability, Improve1Capability):
        return capability
    if isinstance(capability, int):
        return CAPABILITY_BY_NUMBER.get(capability)
    return CAPABILITY_BY_SLUG.get(capability)


def _spec_for(capability: Improve1Capability) -> dict[str, Any]:
    return {
        "title": capability.title,
        "slug": capability.slug,
        "tables": (f"research_grants_management_{capability.slug}_control",),
        "fields": _FEATURE_FIELDS[capability.feature_number],
        "primary_proof": _PRIMARY_PROOF_FIELDS[capability.feature_number],
        "ui": f"ResearchGrantsManagement{_camel(capability.slug)}Panel",
        "route": f"POST /research-grants-management/improve1/{capability.slug}",
        "dependencies": _FEATURE_DEPENDENCIES.get(capability.feature_number, ()),
    }


CONTROL_SPECS = {capability.feature_number: _spec_for(capability) for capability in RESEARCH_CAPABILITIES}


def sample_payload_for(capability: Improve1Capability | str | int) -> dict[str, Any]:
    resolved = _resolve(capability)
    if resolved is None:
        return {}
    spec = CONTROL_SPECS[resolved.feature_number]
    payload = {field: f"{resolved.slug}_{field}" for field in spec["fields"]}
    payload[spec["primary_proof"]] = True
    payload.update({
        "database_backend": "postgresql",
        "event_contract": EVENT_CONTRACT,
        "event_topic": RESEARCH_REQUIRED_EVENT_TOPIC,
        "stream_engine_picker_visible": False,
        "shared_table_access": False,
        "dependency_access_mode": "api_event_projection",
        "human_confirmation": True,
        "approver_separate_from_initiator": True,
        "agent_preview_only": True,
        "non_mutating_simulation": True,
        "pre_award_evidence_complete": True,
        "compliance_evidence_complete": True,
        "financial_evidence_complete": True,
        "side_effects": (),
    })
    return payload


def _domain_findings(capability: Improve1Capability, payload: dict[str, Any]) -> tuple[str, ...]:
    findings: list[str] = []
    number = capability.feature_number
    spec = CONTROL_SPECS[number]
    if payload.get(spec["primary_proof"]) is not True:
        findings.append(f"{capability.title} requires {spec['primary_proof'].replace('_', ' ')}")
        findings.append(f"{capability.title} requires owned grants model, UI, service/API, event, agent, test, and release evidence before approval.")
    if number in _PRE_AWARD_FEATURES and payload.get("pre_award_evidence_complete") is not True:
        findings.append("funding opportunities, eligibility, limited submissions, deadlines, proposal sections, compliance matrices, budget templates, allowability, cost share, indirect cost, and assistant proposal/budget workflows require pre-award evidence")
    if number in _COMPLIANCE_FEATURES and payload.get("compliance_evidence_complete") is not True:
        findings.append("proposal compliance, ethics/protocol boundaries, disclosures, export control, compliance schedules, award readiness, subaward monitoring, effort, restricted categories, equipment, human subjects flags, data/biosafety obligations, replay, audit freeze, and go-live require compliance evidence")
    if number in _FINANCIAL_FEATURES and payload.get("financial_evidence_complete") is not True:
        findings.append("budget templates, line allowability, cost share, indirect costs, pre-award spending, rebudgeting, extensions, financial reports, labor reconciliation, cost transfers, participant support, equipment obligations, budget assistant drafts, closeout, and go-live require financial evidence")
    if number in _HUMAN_CONFIRMATION_FEATURES and payload.get("human_confirmation") is not True:
        findings.append("eligibility overrides, limited submissions, proposal package status, compliance clearance, budget exceptions, cost share, F&A waivers, restricted research, award terms, activation, amendments, spending exceptions, rebudgeting, extensions, subawards, transfers, equipment approvals, assistant actions, correspondence changes, closeout, audit freeze, and go-live require human confirmation")
    if number in _APPROVAL_REQUIRED_FEATURES and payload.get("approver_separate_from_initiator") is not True:
        findings.append("grant routing, budget, compliance, award, amendment, subaward, spending, reporting, closeout, audit, and go-live decisions require separated approval")
    if number in _AI_PREVIEW_FEATURES and payload.get("agent_preview_only") is not True:
        findings.append("research grants assistant skills must be cited, permission-checked, and preview-only until confirmed by research administration staff")
    if number in _NON_MUTATING_FEATURES and payload.get("non_mutating_simulation") is not True:
        findings.append("opportunity review, eligibility, calendars, matrices, templates, rules, boundaries, schedules, detectors, graphs, reports, effort, risk, UI, assistant previews, events, replay, closeout scores, audit packs, scenarios, and go-live gates must be side-effect-free")
    if number in _PROJECTION_ONLY_FEATURES and payload.get("dependency_access_mode") != "api_event_projection":
        findings.append("sponsor opportunity, holiday, protocol, disclosure, export control, payroll, procurement, subrecipient, correspondence, document, financial actual, training, audit, policy, and KPI facts must use declared APIs, events, or projections")
    if payload.get("event_contract") != EVENT_CONTRACT or payload.get("event_topic") != RESEARCH_REQUIRED_EVENT_TOPIC:
        findings.append("research grants eventing must use the AppGen-X event contract and package topic")
    if payload.get("stream_engine_picker_visible"):
        findings.append("ordinary PBCs must not expose stream-engine pickers")
    if payload.get("database_backend") not in RESEARCH_ALLOWED_DATABASE_BACKENDS:
        findings.append("ordinary research grants datastore must be PostgreSQL, MySQL, or MariaDB")
    if payload.get("shared_table_access"):
        findings.append("research grants controls must use owned tables plus declared APIs/events/projections")
    return tuple(dict.fromkeys(findings))


def evaluate_research_grants_management_control(capability: Improve1Capability | str | int, payload: dict[str, Any] | None = None) -> dict[str, Any]:
    resolved = _resolve(capability)
    if resolved is None:
        return {"ok": False, "reason": "unknown_capability", "side_effects": ()}
    spec = CONTROL_SPECS[resolved.feature_number]
    candidate = sample_payload_for(resolved)
    candidate.update(dict(payload or {}))
    missing_fields = tuple(field for field in spec["fields"] if candidate.get(field) in (None, "", (), []))
    foreign_tables = tuple(table for table in spec["tables"] if table not in RESEARCH_OWNED_TABLES)
    undeclared_dependencies = tuple(dependency for dependency in spec["dependencies"] if dependency not in RESEARCH_DECLARED_DEPENDENCIES)
    findings = _domain_findings(resolved, candidate)
    evidence = {
        "evidence_id": _digest((PBC_KEY, resolved.feature_number, tuple(sorted(candidate))))[:20],
        "owned_tables": spec["tables"],
        "required_fields": spec["fields"],
        "primary_proof": spec["primary_proof"],
        "ui_surface": spec["ui"],
        "service_api": spec["route"],
        "test": "tests/test_domain_behavior.py",
        "event_contract": EVENT_CONTRACT,
        "required_event_topic": RESEARCH_REQUIRED_EVENT_TOPIC,
        "allowed_database_backends": RESEARCH_ALLOWED_DATABASE_BACKENDS,
        "declared_dependencies": spec["dependencies"],
        "side_effects": (),
    }
    ok = not missing_fields and not foreign_tables and not undeclared_dependencies and not findings
    return {
        "ok": ok,
        "pbc": PBC_KEY,
        "feature_number": resolved.feature_number,
        "slug": resolved.slug,
        "title": resolved.title,
        "capability": resolved.as_traceability_row(),
        "payload": candidate,
        "evidence": evidence,
        "missing_fields": missing_fields,
        "foreign_tables": foreign_tables,
        "undeclared_dependencies": undeclared_dependencies,
        "findings": findings,
        "side_effects": (),
    }


def improve1_research_grants_management_control_contract() -> dict[str, Any]:
    evaluations = tuple(evaluate_research_grants_management_control(capability) for capability in RESEARCH_CAPABILITIES)
    blocking = tuple(item for item in evaluations if not item["ok"])
    return {
        "ok": not blocking,
        "pbc": PBC_KEY,
        "format": "appgen.research-grants-management-improve1-control.v1",
        "capability_count": len(evaluations),
        "capabilities": evaluations,
        "owned_tables": RESEARCH_OWNED_TABLES,
        "declared_dependencies": RESEARCH_DECLARED_DEPENDENCIES,
        "allowed_database_backends": RESEARCH_ALLOWED_DATABASE_BACKENDS,
        "event_contract": EVENT_CONTRACT,
        "required_event_topic": RESEARCH_REQUIRED_EVENT_TOPIC,
        "stream_engine_picker_visible": False,
        "blocking_gaps": blocking,
        "side_effects": (),
    }


RESEARCH_GRANTS_MANAGEMENT_CONTROL_FUNCTIONS = {
    capability.slug: (lambda payload=None, slug=capability.slug: evaluate_research_grants_management_control(slug, payload))
    for capability in RESEARCH_CAPABILITIES
}
