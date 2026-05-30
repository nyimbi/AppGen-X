CREATE TABLE donor_grant_fundraising_donor (
    id TEXT PRIMARY KEY,
    tenant TEXT NOT NULL,
    donor_code TEXT,
    name TEXT NOT NULL,
    donor_type TEXT NOT NULL,
    relationship_stage TEXT NOT NULL,
    owner TEXT,
    recognition_preference TEXT NOT NULL,
    next_action_date TEXT,
    preferred_channels JSON,
    funding_interests JSON,
    restriction_preferences JSON,
    compliance_requirements JSON,
    qualification_evidence JSON,
    created_at TEXT,
    updated_at TEXT
);

CREATE TABLE donor_grant_fundraising_campaign (
    id TEXT PRIMARY KEY,
    tenant TEXT NOT NULL,
    campaign_code TEXT,
    name TEXT NOT NULL,
    parent_campaign_id TEXT,
    objective_category TEXT NOT NULL,
    goal_amount DECIMAL(14,2) NOT NULL,
    target_segments JSON,
    gift_counting_rules JSON,
    linked_grant_themes JSON,
    start_date TEXT,
    end_date TEXT,
    current_amount DECIMAL(14,2) NOT NULL,
    created_at TEXT,
    updated_at TEXT
);

CREATE TABLE donor_grant_fundraising_pledge (
    id TEXT PRIMARY KEY,
    tenant TEXT NOT NULL,
    pledge_code TEXT,
    donor_id TEXT,
    campaign_id TEXT,
    amount DECIMAL(14,2) NOT NULL,
    paid_amount DECIMAL(14,2) NOT NULL,
    remaining_balance DECIMAL(14,2) NOT NULL,
    status TEXT NOT NULL,
    installments JSON,
    reminder_dates JSON,
    amendment_reason TEXT,
    created_at TEXT,
    updated_at TEXT
);

CREATE TABLE donor_grant_fundraising_gift (
    id TEXT PRIMARY KEY,
    tenant TEXT NOT NULL,
    gift_code TEXT,
    donor_id TEXT,
    campaign_id TEXT,
    pledge_id TEXT,
    restriction_id TEXT,
    amount DECIMAL(14,2) NOT NULL,
    appeal_source TEXT,
    purpose_code TEXT,
    receipt_status TEXT,
    posting_date TEXT,
    created_at TEXT,
    updated_at TEXT
);

CREATE TABLE donor_grant_fundraising_restriction (
    id TEXT PRIMARY KEY,
    tenant TEXT NOT NULL,
    restriction_code TEXT,
    restriction_type TEXT NOT NULL,
    purpose_code TEXT NOT NULL,
    geography TEXT,
    time_window TEXT,
    beneficiary_class TEXT,
    required_approvals JSON,
    release_conditions JSON,
    sunset_date TEXT,
    created_at TEXT,
    updated_at TEXT
);

CREATE TABLE donor_grant_fundraising_grant_application (
    id TEXT PRIMARY KEY,
    tenant TEXT NOT NULL,
    grant_code TEXT,
    funder_id TEXT,
    stage TEXT NOT NULL,
    fit_score DECIMAL(8,4) NOT NULL,
    strategic_priority TEXT,
    deadline TEXT,
    deadline_confidence DECIMAL(8,4) NOT NULL,
    proposal_complete BOOLEAN NOT NULL,
    proposal_workspace JSON,
    budget JSON,
    review_signoffs JSON,
    post_award_setup JSON,
    created_at TEXT,
    updated_at TEXT
);

CREATE TABLE donor_grant_fundraising_stewardship_touchpoint (
    id TEXT PRIMARY KEY,
    tenant TEXT NOT NULL,
    donor_id TEXT,
    playbook_type TEXT,
    expected_cadence TEXT,
    outcome TEXT,
    next_ask_readiness TEXT,
    segment TEXT,
    acknowledgement_status TEXT,
    created_at TEXT,
    updated_at TEXT
);

CREATE TABLE donor_grant_fundraising_donor_relationship (
    id TEXT PRIMARY KEY,
    tenant TEXT NOT NULL,
    donor_id TEXT,
    related_donor_id TEXT,
    relationship_type TEXT,
    influence_level TEXT,
    recognition_visibility TEXT,
    valid_from TEXT,
    valid_to TEXT,
    created_at TEXT,
    updated_at TEXT
);

CREATE TABLE donor_grant_fundraising_proposal_workspace (
    id TEXT PRIMARY KEY,
    tenant TEXT NOT NULL,
    grant_application_id TEXT,
    narrative_status TEXT,
    budget_status TEXT,
    attachment_checklist JSON,
    reviewer_comments JSON,
    submission_package_version TEXT,
    final_signoff BOOLEAN NOT NULL,
    proposal_complete BOOLEAN NOT NULL,
    created_at TEXT,
    updated_at TEXT
);

CREATE TABLE donor_grant_fundraising_acknowledgement (
    id TEXT PRIMARY KEY,
    tenant TEXT NOT NULL,
    donor_id TEXT,
    gift_id TEXT,
    pledge_id TEXT,
    channel TEXT,
    template_key TEXT,
    due_date TEXT,
    status TEXT,
    completed_at TEXT,
    created_at TEXT,
    updated_at TEXT
);

CREATE TABLE donor_grant_fundraising_briefing_packet (
    id TEXT PRIMARY KEY,
    tenant TEXT NOT NULL,
    packet_code TEXT,
    audience TEXT,
    generated_for_date TEXT,
    campaign_summary JSON,
    major_donor_summary JSON,
    grant_pipeline_summary JSON,
    restricted_fund_summary JSON,
    created_at TEXT,
    updated_at TEXT
);

CREATE TABLE donor_grant_fundraising_opportunity_score (
    id TEXT PRIMARY KEY,
    tenant TEXT NOT NULL,
    donor_id TEXT,
    grant_application_id TEXT,
    potential_value DECIMAL(14,2) NOT NULL,
    likelihood DECIMAL(8,4) NOT NULL,
    urgency DECIMAL(8,4) NOT NULL,
    delivery_risk DECIMAL(8,4) NOT NULL,
    priority_score DECIMAL(14,2) NOT NULL,
    explanation TEXT,
    created_at TEXT,
    updated_at TEXT
);

CREATE TABLE donor_grant_fundraising_review_chain (
    id TEXT PRIMARY KEY,
    tenant TEXT NOT NULL,
    entity_type TEXT NOT NULL,
    entity_id TEXT NOT NULL,
    required_roles JSON,
    completed_roles JSON,
    due_date TEXT,
    status TEXT NOT NULL,
    evidence JSON,
    created_at TEXT,
    updated_at TEXT
);

CREATE TABLE donor_grant_fundraising_budget_validation (
    id TEXT PRIMARY KEY,
    tenant TEXT NOT NULL,
    grant_application_id TEXT,
    restriction_id TEXT,
    status TEXT NOT NULL,
    violated_conditions JSON,
    reviewed_by TEXT,
    reviewed_at TEXT,
    budget_total DECIMAL(14,2) NOT NULL,
    created_at TEXT,
    updated_at TEXT
);

CREATE TABLE donor_grant_fundraising_policy_rule (
    id TEXT PRIMARY KEY,
    tenant TEXT NOT NULL,
    rule_code TEXT,
    scope TEXT,
    status TEXT,
    payload JSON,
    created_at TEXT,
    updated_at TEXT
);

CREATE TABLE donor_grant_fundraising_runtime_parameter (
    id TEXT PRIMARY KEY,
    tenant TEXT NOT NULL,
    parameter_name TEXT,
    parameter_value TEXT,
    scope TEXT,
    bounded BOOLEAN NOT NULL,
    created_at TEXT,
    updated_at TEXT
);

CREATE TABLE donor_grant_fundraising_schema_extension (
    id TEXT PRIMARY KEY,
    tenant TEXT NOT NULL,
    target_table TEXT,
    fields JSON,
    status TEXT,
    payload JSON,
    created_at TEXT,
    updated_at TEXT
);

CREATE TABLE donor_grant_fundraising_control_assertion (
    id TEXT PRIMARY KEY,
    tenant TEXT NOT NULL,
    control_id TEXT,
    status TEXT,
    assertion_payload JSON,
    evidence_hash TEXT,
    created_at TEXT,
    updated_at TEXT
);

CREATE TABLE donor_grant_fundraising_governed_model (
    id TEXT PRIMARY KEY,
    tenant TEXT NOT NULL,
    model_name TEXT,
    status TEXT,
    version TEXT,
    payload JSON,
    created_at TEXT,
    updated_at TEXT
);

CREATE TABLE donor_grant_fundraising_appgen_outbox_event (
    id TEXT PRIMARY KEY,
    tenant TEXT NOT NULL,
    event_type TEXT,
    topic TEXT,
    idempotency_key TEXT,
    payload JSON,
    status TEXT,
    created_at TEXT
);

CREATE TABLE donor_grant_fundraising_appgen_inbox_event (
    id TEXT PRIMARY KEY,
    tenant TEXT NOT NULL,
    event_type TEXT,
    topic TEXT,
    idempotency_key TEXT,
    payload JSON,
    status TEXT,
    created_at TEXT
);

CREATE TABLE donor_grant_fundraising_appgen_dead_letter_event (
    id TEXT PRIMARY KEY,
    tenant TEXT NOT NULL,
    event_type TEXT,
    topic TEXT,
    idempotency_key TEXT,
    payload JSON,
    status TEXT,
    created_at TEXT
);
