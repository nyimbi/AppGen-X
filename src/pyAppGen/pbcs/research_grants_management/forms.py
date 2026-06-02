"""Domain forms for the research grants management standalone PBC."""
from __future__ import annotations

PBC_KEY = "research_grants_management"


def _field(name, kind="text", required=True, **extra):
    return {"name": name, "type": kind, "required": required, **extra}


FORMS = (
    {
        "key": "funding_opportunity",
        "title": "Funding opportunity registry",
        "owned_table": "research_grants_management_grant_proposal",
        "fields": (
            _field("sponsor"), _field("program_code"), _field("notice_version"),
            _field("sponsor_deadline", "date"), _field("internal_routing_deadline", "date"),
            _field("sponsor_type", "select", options=("federal", "foundation", "industry", "state")),
            _field("limited_submission_slots", "number", required=False), _field("source_archive_digest"),
        ),
    },
    {
        "key": "eligibility_review",
        "title": "Opportunity eligibility and institutional fit",
        "owned_table": "research_grants_management_grant_proposal",
        "fields": (
            _field("investigator_status"), _field("career_stage"), _field("institution_type"),
            _field("institution_location"), _field("cost_share_available", "boolean"),
            _field("limited_submission_nomination", "boolean", required=False), _field("override_justification", required=False),
        ),
    },
    {
        "key": "limited_submission_nomination",
        "title": "Limited submission nomination",
        "owned_table": "research_grants_management_grant_proposal",
        "fields": (
            _field("opportunity_id"), _field("nominee"), _field("rank", "number"),
            _field("committee_decision", "select", options=("selected", "alternate", "declined", "pending")),
            _field("slot_count", "number"), _field("review_minutes_digest"),
        ),
    },
    {
        "key": "proposal_sections",
        "title": "Proposal assembly workspace",
        "owned_table": "research_grants_management_grant_proposal",
        "fields": (
            _field("abstract_status", "select", options=("missing", "draft", "review", "approved", "blocked")),
            _field("aims_status", "select", options=("missing", "draft", "review", "approved", "blocked")),
            _field("narrative_status", "select", options=("missing", "draft", "review", "approved", "blocked")),
            _field("budget_justification_status", "select", options=("missing", "draft", "review", "approved", "blocked")),
            _field("biosketches_status", "select", options=("missing", "draft", "review", "approved", "blocked")),
            _field("data_plan_status", "select", options=("missing", "draft", "review", "approved", "blocked")),
        ),
    },
    {
        "key": "budget_line_allowability",
        "title": "Budget line-item allowability",
        "owned_table": "research_grants_management_sponsor_budget",
        "fields": (
            _field("proposal_id"), _field("category", "select", options=("personnel", "fringe", "travel", "equipment", "supplies", "participant_support", "subaward", "tuition", "publication", "patient_care")),
            _field("amount", "money"), _field("sponsor_rule"), _field("justification", required=False),
            _field("prior_approval_required", "boolean", required=False),
        ),
    },
    {
        "key": "cost_share_commitment",
        "title": "Cost share and matching commitment",
        "owned_table": "research_grants_management_sponsor_budget",
        "fields": (
            _field("proposal_id"), _field("commitment_type", "select", options=("mandatory", "voluntary_committed", "prohibited")),
            _field("source_account"), _field("responsible_unit"), _field("amount", "money"),
            _field("approval_chain", "json"),
        ),
    },
    {
        "key": "indirect_cost_waiver",
        "title": "Indirect cost and waiver governance",
        "owned_table": "research_grants_management_sponsor_budget",
        "fields": (
            _field("budget_id"), _field("rate_base", "select", options=("mtDC", "total_direct", "off_campus", "de_minimis")),
            _field("rate", "percentage"), _field("excluded_costs", "json", required=False),
            _field("waiver_approver", required=False), _field("waiver_reason", required=False), _field("sponsor_citation", required=False),
        ),
    },
    {
        "key": "compliance_dependency",
        "title": "IRB ethics and compliance boundary",
        "owned_table": "research_grants_management_compliance_requirement",
        "fields": (
            _field("proposal_or_award_id"), _field("dependency_type", "select", options=("irb", "exempt", "iacuc", "export_control", "coi", "training", "none")),
            _field("source_system"), _field("status"), _field("status_timestamp", "datetime"),
            _field("expiration_date", "date", required=False), _field("gating_effect", "select", options=("blocks_submission", "blocks_activation", "monitor_only")),
        ),
    },
    {
        "key": "award_notice_extraction",
        "title": "Award notice extraction and negotiation redlines",
        "owned_table": "research_grants_management_research_award",
        "fields": (
            _field("award_id"), _field("sponsor_notice_digest"), _field("total_amount", "money"),
            _field("obligated_amount", "money"), _field("project_start", "date"), _field("project_end", "date"),
            _field("publication_constraints", required=False), _field("data_rights", required=False), _field("unresolved_redlines", "json", required=False),
        ),
    },
    {
        "key": "award_readiness",
        "title": "Award setup readiness checklist",
        "owned_table": "research_grants_management_research_award",
        "fields": (
            _field("account_setup", "boolean"), _field("budget_activation", "boolean"),
            _field("compliance_dependencies_clear", "boolean"), _field("effort_allocations", "boolean"),
            _field("subaward_readiness", "boolean"), _field("deliverable_schedule", "boolean"),
            _field("authorized_exception", "boolean", required=False),
        ),
    },
    {
        "key": "award_amendment",
        "title": "Amendment and modification chain",
        "owned_table": "research_grants_management_research_award",
        "fields": (
            _field("award_id"), _field("amendment_type", "select", options=("supplement", "carryforward", "rebudget", "no_cost_extension", "term_change")),
            _field("effective_date", "date"), _field("financial_impact", "money", required=False),
            _field("compliance_impact", required=False), _field("sponsor_document_digest"),
        ),
    },
    {
        "key": "subaward_profile_monitoring",
        "title": "Subrecipient risk and monitoring",
        "owned_table": "research_grants_management_subaward",
        "fields": (
            _field("subrecipient_name"), _field("legal_identifiers", "json"), _field("foreign_status", "boolean"),
            _field("audit_status"), _field("monitoring_tier", "select", options=("low", "moderate", "high")),
            _field("scope_dates_match_prime", "boolean"), _field("budget_matches_prime", "boolean"),
            _field("monitoring_evidence_digest", required=False),
        ),
    },
    {
        "key": "sponsor_report_pack",
        "title": "Technical and financial sponsor report pack",
        "owned_table": "research_grants_management_milestone_report",
        "fields": (
            _field("award_id"), _field("report_type", "select", options=("technical", "financial", "closeout")),
            _field("reporting_period_start", "date"), _field("reporting_period_end", "date"),
            _field("accomplishments", required=False), _field("expenditures", "money", required=False),
            _field("cost_share_delivered", "money", required=False), _field("unobligated_balance", "money", required=False),
        ),
    },
    {
        "key": "effort_certification",
        "title": "Effort certification boundary",
        "owned_table": "research_grants_management_effort_certification",
        "fields": (
            _field("award_id"), _field("key_person"), _field("committed_effort", "percentage"),
            _field("charged_effort", "percentage"), _field("certification_period"),
            _field("certifier"), _field("payroll_source_reference", required=False), _field("exception_reason", required=False),
        ),
    },
)


def form_catalog() -> dict:
    return {"ok": True, "pbc": PBC_KEY, "forms": FORMS, "side_effects": ()}


def form_for(key: str) -> dict:
    for form in FORMS:
        if form["key"] == key:
            return {"ok": True, "form": form, "side_effects": ()}
    return {"ok": False, "reason": "unknown_form", "key": key, "side_effects": ()}


def smoke_test() -> dict:
    return {"ok": len(FORMS) >= 14 and all(form["owned_table"].startswith(f"{PBC_KEY}_") for form in FORMS), "side_effects": ()}
