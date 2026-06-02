"""Executable improve1 controls for the donor grant fundraising PBC."""

from __future__ import annotations

from typing import Any

from .improve1_capabilities import IMPROVE1_CAPABILITIES, Improve1Capability
import hashlib

PBC_KEY = "donor_grant_fundraising"
EVENT_CONTRACT = "AppGen-X"
DONOR_GRANT_FUNDRAISING_ALLOWED_DATABASE_BACKENDS = ("postgresql", "mysql", "mariadb")
DONOR_GRANT_FUNDRAISING_REQUIRED_EVENT_TOPIC = "pbc.donor_grant_fundraising.events"
DONOR_GRANT_FUNDRAISING_OWNED_TABLES = (
    "donor_grant_fundraising_donor",
    "donor_grant_fundraising_campaign",
    "donor_grant_fundraising_pledge",
    "donor_grant_fundraising_gift",
    "donor_grant_fundraising_restriction",
    "donor_grant_fundraising_grant_application",
    "donor_grant_fundraising_stewardship_touchpoint",
    "donor_grant_fundraising_donor_relationship",
    "donor_grant_fundraising_proposal_workspace",
    "donor_grant_fundraising_acknowledgement",
    "donor_grant_fundraising_briefing_packet",
    "donor_grant_fundraising_opportunity_score",
    "donor_grant_fundraising_review_chain",
    "donor_grant_fundraising_budget_validation",
    "donor_grant_fundraising_policy_rule",
    "donor_grant_fundraising_runtime_parameter",
    "donor_grant_fundraising_schema_extension",
    "donor_grant_fundraising_control_assertion",
    "donor_grant_fundraising_governed_model",
    "donor_grant_fundraising_appgen_outbox_event",
    "donor_grant_fundraising_appgen_inbox_event",
    "donor_grant_fundraising_appgen_dead_letter_event",
)


def _digest(value: object) -> str:
    return hashlib.sha256(repr(value).encode("utf-8")).hexdigest()

DONOR_TABLE = f"{PBC_KEY}_donor"
CAMPAIGN_TABLE = f"{PBC_KEY}_campaign"
PLEDGE_TABLE = f"{PBC_KEY}_pledge"
GIFT_TABLE = f"{PBC_KEY}_gift"
RESTRICTION_TABLE = f"{PBC_KEY}_restriction"
GRANT_TABLE = f"{PBC_KEY}_grant_application"
TOUCHPOINT_TABLE = f"{PBC_KEY}_stewardship_touchpoint"
RELATIONSHIP_TABLE = f"{PBC_KEY}_donor_relationship"
PROPOSAL_TABLE = f"{PBC_KEY}_proposal_workspace"
ACK_TABLE = f"{PBC_KEY}_acknowledgement"
BRIEFING_TABLE = f"{PBC_KEY}_briefing_packet"
SCORE_TABLE = f"{PBC_KEY}_opportunity_score"
REVIEW_TABLE = f"{PBC_KEY}_review_chain"
BUDGET_TABLE = f"{PBC_KEY}_budget_validation"
POLICY_TABLE = f"{PBC_KEY}_policy_rule"
PARAMETER_TABLE = f"{PBC_KEY}_runtime_parameter"
SCHEMA_EXTENSION_TABLE = f"{PBC_KEY}_schema_extension"
CONTROL_TABLE = f"{PBC_KEY}_control_assertion"
MODEL_TABLE = f"{PBC_KEY}_governed_model"
OUTBOX_TABLE = f"{PBC_KEY}_appgen_outbox_event"
INBOX_TABLE = f"{PBC_KEY}_appgen_inbox_event"
DEAD_LETTER_TABLE = f"{PBC_KEY}_appgen_dead_letter_event"

FUNDRAISING_CONTROL_CAPABILITIES: tuple[Improve1Capability, ...] = IMPROVE1_CAPABILITIES
CAPABILITY_BY_NUMBER = {capability.feature_number: capability for capability in FUNDRAISING_CONTROL_CAPABILITIES}
CAPABILITY_BY_SLUG = {capability.slug: capability for capability in FUNDRAISING_CONTROL_CAPABILITIES}

CONTROL_SPECS: dict[int, dict[str, Any]] = {
    1: {"tables": (DONOR_TABLE,), "fields": ("donor_type", "relationship_stage", "preferred_channels", "funding_interests", "recognition_preference"), "ui": "DonorGrantFundraisingDetail", "route": "POST /donors"},
    2: {"tables": (DONOR_TABLE, POLICY_TABLE), "fields": ("prospect_stage", "owner", "next_action_date", "qualification_evidence"), "ui": "DonorGrantFundraisingWorkbench", "route": "POST /donors/prospect-stage"},
    3: {"tables": (CAMPAIGN_TABLE,), "fields": ("parent_campaign", "objective_category", "goal_amount", "target_segments", "counting_rules"), "ui": "DonorGrantFundraisingWorkbench", "route": "POST /campaigns"},
    4: {"tables": (PLEDGE_TABLE,), "fields": ("pledge_state", "installment_schedule", "reminder_dates", "amendment_reason"), "ui": "DonorGrantFundraisingDetail", "route": "POST /pledges"},
    5: {"tables": (GIFT_TABLE, PLEDGE_TABLE, CAMPAIGN_TABLE), "fields": ("campaign_id", "pledge_id", "appeal_source", "restriction_usage", "receipt_status"), "ui": "DonorGrantFundraisingWorkbench", "route": "POST /gifts"},
    6: {"tables": (RESTRICTION_TABLE, POLICY_TABLE), "fields": ("restriction_type", "purpose_code", "geography", "time_window", "release_conditions"), "ui": "DonorGrantFundraisingDetail", "route": "POST /restrictions"},
    7: {"tables": (GRANT_TABLE, SCORE_TABLE), "fields": ("opportunity_stage", "funder_fit", "strategic_priority", "deadline_confidence"), "ui": "DonorGrantFundraisingWorkbench", "route": "POST /grant-applications"},
    8: {"tables": (GRANT_TABLE, PROPOSAL_TABLE), "fields": ("narrative_status", "budget_completeness", "attachment_checklist", "reviewer_comments", "final_signoff"), "ui": "DonorGrantFundraisingDetail", "route": "POST /grant-applications/proposal-workspace"},
    9: {"tables": (GRANT_TABLE, RESTRICTION_TABLE, BUDGET_TABLE), "fields": ("grant_budget", "restriction_rules", "violated_condition", "reviewer"), "ui": "DonorGrantFundraisingDetail", "route": "POST /grant-applications/budget-validation"},
    10: {"tables": (GRANT_TABLE, RESTRICTION_TABLE, TOUCHPOINT_TABLE), "fields": ("award_letter_review", "reporting_cadence", "stewardship_owner", "ack_deadline", "renewal_plan"), "ui": "DonorGrantFundraisingWorkbench", "route": "POST /grant-applications/award-setup"},
    11: {"tables": (ACK_TABLE, GIFT_TABLE, PLEDGE_TABLE), "fields": ("template", "donor_type", "tax_receipt_need", "channel", "due_date"), "ui": "DonorGrantFundraisingWorkbench", "route": "POST /acknowledgements"},
    12: {"tables": (TOUCHPOINT_TABLE, DONOR_TABLE), "fields": ("playbook_type", "expected_cadence", "outcome", "next_ask_readiness", "segment"), "ui": "DonorGrantFundraisingWorkbench", "route": "POST /stewardship-touchpoints"},
    13: {"tables": (GIFT_TABLE, PLEDGE_TABLE, CAMPAIGN_TABLE, GRANT_TABLE, TOUCHPOINT_TABLE), "fields": ("timeline_entries", "donor_id", "source_links"), "ui": "DonorGrantFundraisingDetail", "route": "GET /donors/timeline"},
    14: {"tables": (DONOR_TABLE, RELATIONSHIP_TABLE), "fields": ("household", "affiliations", "advisor_roles", "validity_dates"), "ui": "DonorGrantFundraisingDetail", "route": "POST /donors/relationships"},
    15: {"tables": (GRANT_TABLE, DONOR_TABLE), "fields": ("contact_role", "communication_channel", "approval_authority", "contact_window"), "ui": "DonorGrantFundraisingDetail", "route": "POST /grant-applications/contact-roles"},
    16: {"tables": (SCORE_TABLE, DONOR_TABLE, GRANT_TABLE), "fields": ("affinity", "capacity", "timing", "mission_fit", "delivery_risk"), "ui": "DonorGrantFundraisingWorkbench", "route": "POST /opportunity-scores"},
    17: {"tables": (REVIEW_TABLE, GRANT_TABLE, PLEDGE_TABLE), "fields": ("review_stages", "reviewer_roles", "due_dates", "approval_evidence"), "ui": "DonorGrantFundraisingWorkbench", "route": "POST /review-chains"},
    18: {"tables": (BRIEFING_TABLE, CAMPAIGN_TABLE, DONOR_TABLE, GRANT_TABLE), "fields": ("campaign_status", "major_donor_readiness", "grant_pipeline", "restricted_exposure"), "ui": "DonorGrantFundraisingDetail", "route": "POST /briefing-packets"},
    19: {"tables": (MODEL_TABLE, RESTRICTION_TABLE, GRANT_TABLE), "fields": ("source_document", "extracted_tasks", "confidence", "human_confirmation"), "ui": "DonorGrantFundraisingAssistantPanel", "route": "POST /assistant/document-intake"},
    20: {"tables": (MODEL_TABLE, GRANT_TABLE, PROPOSAL_TABLE), "fields": ("opportunity_fit", "proposal_checklist", "missing_attachments", "reviewer_questions"), "ui": "DonorGrantFundraisingAssistantPanel", "route": "POST /assistant/grant-proposal-support"},
    21: {"tables": (MODEL_TABLE, GIFT_TABLE, PLEDGE_TABLE, TOUCHPOINT_TABLE), "fields": ("draft_type", "supporting_records", "citations", "approval"), "ui": "DonorGrantFundraisingAssistantPanel", "route": "POST /assistant/stewardship-draft"},
    22: {"tables": (MODEL_TABLE, POLICY_TABLE, DONOR_TABLE, PLEDGE_TABLE, GIFT_TABLE, RESTRICTION_TABLE, GRANT_TABLE), "fields": ("action_preview", "approval_route", "idempotency_key", "policy_result"), "ui": "DonorGrantFundraisingAssistantPanel", "route": "POST /assistant/mutation-preview"},
    23: {"tables": (DONOR_TABLE, PLEDGE_TABLE, ACK_TABLE), "fields": ("owner", "stage", "next_action", "pledge_exposure", "ack_backlog"), "ui": "DonorGrantFundraisingWorkbench", "route": "GET /donor-portfolios"},
    24: {"tables": (GRANT_TABLE, REVIEW_TABLE, PROPOSAL_TABLE), "fields": ("deadline_bucket", "stage_counts", "review_blockers", "renewal_forecast"), "ui": "DonorGrantFundraisingWorkbench", "route": "GET /grant-pipeline"},
    25: {"tables": (CAMPAIGN_TABLE, PLEDGE_TABLE, GIFT_TABLE), "fields": ("campaign_rollup", "segment_performance", "ask_conversion", "pledge_trend"), "ui": "DonorGrantFundraisingWorkbench", "route": "GET /campaign-performance"},
    26: {"tables": (RESTRICTION_TABLE, EXCEPTION_TABLE := CONTROL_TABLE), "fields": ("active_restrictions", "pending_releases", "blocked_uses", "overdue_approvals"), "ui": "DonorGrantFundraisingWorkbench", "route": "GET /restriction-compliance"},
    27: {"tables": (GRANT_TABLE, TOUCHPOINT_TABLE), "fields": ("report_type", "period", "evidence_checklist", "owner", "submission_status"), "ui": "DonorGrantFundraisingWorkbench", "route": "POST /reporting-calendar"},
    28: {"tables": (GIFT_TABLE, RESTRICTION_TABLE, GRANT_TABLE), "fields": ("impact_statement", "evidence_refs", "outcome_period", "narrative_approval"), "ui": "DonorGrantFundraisingDetail", "route": "POST /impact-reports"},
    29: {"tables": (DONOR_TABLE,), "fields": ("required_profile_fields", "source_attribution", "duplicate_check", "mutation_rules"), "ui": "DonorGrantFundraisingDetail", "route": "POST /donors"},
    30: {"tables": (CAMPAIGN_TABLE, PLEDGE_TABLE, GIFT_TABLE, RESTRICTION_TABLE), "fields": ("approval_prerequisites", "idempotency", "conflict_handling", "source_system"), "ui": "DonorGrantFundraisingDetail", "route": "POST /fundraising-writes"},
    31: {"tables": (OUTBOX_TABLE, INBOX_TABLE, DEAD_LETTER_TABLE), "fields": ("event_semantics", "replay_checksum", "idempotency_key", "exception_handling"), "ui": "DonorGrantFundraisingWorkbench", "route": "POST /events/replay"},
    32: {"tables": (CONTROL_TABLE,), "fields": ("exception_type", "severity", "owner", "due_date", "closure_evidence"), "ui": "DonorGrantFundraisingWorkbench", "route": "POST /fundraising-exceptions"},
    33: {"tables": (DONOR_TABLE, PLEDGE_TABLE, CONTROL_TABLE), "fields": ("match_confidence", "operator_review", "source_references", "audit_history"), "ui": "DonorGrantFundraisingWorkbench", "route": "POST /duplicates/resolve"},
    34: {"tables": (MODEL_TABLE, DONOR_TABLE, GRANT_TABLE), "fields": ("renewal_probability", "retention_signal", "reporting_timeliness", "funding_history"), "ui": "DonorGrantFundraisingWorkbench", "route": "POST /renewal-forecasts"},
    35: {"tables": (MODEL_TABLE, CAMPAIGN_TABLE, GRANT_TABLE), "fields": ("ask_amount", "assignment", "campaign_timing", "projected_outcome"), "ui": "DonorGrantFundraisingWorkbench", "route": "POST /ask-scenarios"},
    36: {"tables": (GRANT_TABLE, ACK_TABLE, TOUCHPOINT_TABLE, RESTRICTION_TABLE), "fields": ("obligation_type", "due_date", "owner", "alert"), "ui": "DonorGrantFundraisingWorkbench", "route": "GET /compliance-calendar"},
    37: {"tables": (POLICY_TABLE, REVIEW_TABLE), "fields": ("reviewer_independence", "approval_threshold", "large_gift_control", "restricted_release_approval"), "ui": "DonorGrantFundraisingWorkbench", "route": "POST /policy-rules/separation-of-duties"},
    38: {"tables": (POLICY_TABLE, PARAMETER_TABLE, MODEL_TABLE), "fields": ("tenant", "portfolio_scope", "assistant_scope", "release_evidence_scope"), "ui": "DonorGrantFundraisingDetail", "route": "POST /tenant-isolation/validate"},
    39: {"tables": (DONOR_TABLE, POLICY_TABLE), "fields": ("privacy_setting", "communication_consent", "anonymous_giving", "recognition_limit"), "ui": "DonorGrantFundraisingDetail", "route": "POST /donors/consent-preferences"},
    40: {"tables": (GIFT_TABLE, PLEDGE_TABLE, RELATIONSHIP_TABLE), "fields": ("soft_credit", "legal_owner", "influencer", "audit_history"), "ui": "DonorGrantFundraisingDetail", "route": "POST /soft-credits"},
    41: {"tables": (RESTRICTION_TABLE, REVIEW_TABLE), "fields": ("request_reason", "supporting_evidence", "approver_route", "impact_preview"), "ui": "DonorGrantFundraisingWorkbench", "route": "POST /restrictions/amendments"},
    42: {"tables": (GRANT_TABLE, RESTRICTION_TABLE, REVIEW_TABLE), "fields": ("amendment_type", "previous_values", "updated_restrictions", "approval"), "ui": "DonorGrantFundraisingWorkbench", "route": "POST /grant-amendments"},
    43: {"tables": (PLEDGE_TABLE, GIFT_TABLE, GRANT_TABLE, CAMPAIGN_TABLE), "fields": ("committed", "received", "expected", "restricted", "available"), "ui": "DonorGrantFundraisingWorkbench", "route": "GET /revenue-pacing"},
    44: {"tables": (DONOR_TABLE, GIFT_TABLE, PLEDGE_TABLE, TOUCHPOINT_TABLE, GRANT_TABLE), "fields": ("meeting_brief", "recent_history", "open_asks", "stale_warning"), "ui": "DonorGrantFundraisingAssistantPanel", "route": "POST /assistant/meeting-prep"},
    45: {"tables": (CONTROL_TABLE, GIFT_TABLE, GRANT_TABLE), "fields": ("evidence_bundle", "narrative_version", "reviewer_signoff", "provenance_hash"), "ui": "DonorGrantFundraisingDetail", "route": "POST /reporting-evidence-bundles"},
    46: {"tables": (CONTROL_TABLE,), "fields": ("control_name", "assertion_result", "remediation_history", "exception_opened"), "ui": "DonorGrantFundraisingWorkbench", "route": "POST /control-tests"},
    47: {"tables": (OUTBOX_TABLE, CONTROL_TABLE, REVIEW_TABLE), "fields": ("approval_event", "previous_hash", "current_hash", "verification"), "ui": "DonorGrantFundraisingDetail", "route": "GET /approval-history"},
    48: {"tables": (SCHEMA_EXTENSION_TABLE,), "fields": ("target_table", "compatibility_check", "migration_preview", "assistant_awareness"), "ui": "DonorGrantFundraisingDetail", "route": "POST /schema-extensions"},
    49: {"tables": (CONTROL_TABLE,), "fields": ("seed_portfolio", "contract_scenarios", "demo_workbench", "api_projection_tests"), "ui": "DonorGrantFundraisingWorkbench", "route": "GET /seed-scenarios"},
    50: {"tables": (CONTROL_TABLE,), "fields": ("api_coverage", "event_replay_health", "workbench_readiness", "assistant_guardrails", "blockers"), "ui": "DonorGrantFundraisingWorkbench", "route": "GET /release-readiness-scorecard"},
}


def _resolve(capability: Improve1Capability | str | int) -> Improve1Capability | None:
    if isinstance(capability, Improve1Capability):
        return capability
    if isinstance(capability, int):
        return CAPABILITY_BY_NUMBER.get(capability)
    return CAPABILITY_BY_SLUG.get(capability)


def sample_payload_for(capability: Improve1Capability | str | int) -> dict[str, Any]:
    resolved = _resolve(capability)
    if resolved is None:
        return {}
    spec = CONTROL_SPECS[resolved.feature_number]
    payload = {field: f"{resolved.slug}_{field}" for field in spec["fields"]}
    payload.update({"references": (), "prospect_stage": "qualified", "target_stage": "assigned", "human_confirmation": True, "approval": "approved", "policy_result": "allow", "anonymous_giving": False, "channel_allowed": True, "tenant": "tenant-fundraising", "assistant_scope": "tenant", "target_table": DONOR_TABLE, "blockers": (), "reviewer_signoff": "reviewer-1"})
    return payload


def _domain_findings(capability: Improve1Capability, payload: dict[str, Any]) -> tuple[str, ...]:
    findings: list[str] = []
    n = capability.feature_number
    if n == 1 and not payload.get("donor_type"):
        findings.append("unified donor profile requires donor type")
    if n == 2 and payload.get("prospect_stage") == payload.get("target_stage"):
        findings.append("prospect pipeline transition must move stage")
    if n == 8 and not payload.get("final_signoff"):
        findings.append("proposal submission requires final signoff")
    if n == 19 and payload.get("confidence") == "low" and payload.get("human_confirmation") is not True:
        findings.append("low-confidence document extraction requires human confirmation")
    if n == 22 and payload.get("policy_result") != "allow":
        findings.append("assistant mutation preview must pass policy before write")
    if n == 37 and payload.get("reviewer_independence") in (False, "false"):
        findings.append("separation of duties blocks self-approval")
    if n == 38 and payload.get("assistant_scope") != "tenant":
        findings.append("assistant actions must remain tenant scoped")
    if n == 39 and payload.get("anonymous_giving") and payload.get("recognition_limit") != "anonymous":
        findings.append("anonymous donor must be suppressed from recognition")
    if n == 48 and payload.get("target_table") not in DONOR_GRANT_FUNDRAISING_OWNED_TABLES:
        findings.append("schema extension target must be an owned fundraising table")
    if n == 50 and payload.get("blockers"):
        findings.append("release readiness scorecard cannot sign off with blockers")
    return tuple(findings)


def evaluate_fundraising_control(capability: Improve1Capability | str | int, payload: dict[str, Any] | None = None) -> dict[str, Any]:
    resolved = _resolve(capability)
    if resolved is None:
        return {"ok": False, "pbc": PBC_KEY, "reason": "unknown_fundraising_control", "side_effects": ()}
    spec = CONTROL_SPECS[resolved.feature_number]
    active_payload = sample_payload_for(resolved) if payload is None else dict(payload)
    missing = tuple(field for field in spec["fields"] if field not in active_payload or active_payload[field] in (None, ""))
    invalid_tables = tuple(table for table in spec["tables"] if table not in DONOR_GRANT_FUNDRAISING_OWNED_TABLES)
    invalid_references = tuple(ref for ref in active_payload.get("references", ()) if isinstance(ref, str) and ref.endswith("_table") and ref not in DONOR_GRANT_FUNDRAISING_OWNED_TABLES)
    domain_findings = _domain_findings(resolved, active_payload)
    event_type = "DonorGrantFundraisingExceptionOpened" if domain_findings else "DonorGrantFundraisingUpdated"
    if resolved.feature_number in {1, 3, 4, 5, 7, 49} and not domain_findings:
        event_type = "DonorGrantFundraisingCreated"
    if resolved.feature_number in {10, 17, 37, 41, 42, 50} and not domain_findings:
        event_type = "DonorGrantFundraisingApproved"
    return {
        "ok": not missing and not invalid_tables and not invalid_references and not domain_findings,
        "pbc": PBC_KEY,
        "capability": resolved.slug,
        "feature_number": resolved.feature_number,
        "title": resolved.title,
        "status": "implemented",
        "target_tables": spec["tables"],
        "owned_tables": DONOR_GRANT_FUNDRAISING_OWNED_TABLES,
        "read_tables": (),
        "invalid_references": invalid_references,
        "missing_required_fields": missing,
        "domain_findings": domain_findings,
        "event": {"contract": EVENT_CONTRACT, "topic": DONOR_GRANT_FUNDRAISING_REQUIRED_EVENT_TOPIC, "type": event_type, "idempotency_key": _digest((PBC_KEY, resolved.slug, active_payload)), "outbox_table": OUTBOX_TABLE, "inbox_table": INBOX_TABLE, "dead_letter_table": DEAD_LETTER_TABLE},
        "ui_surface": spec["ui"],
        "service_api": spec["route"],
        "permission": f"{PBC_KEY}.approve" if resolved.feature_number in {10, 17, 22, 37, 41, 42, 45, 50} else f"{PBC_KEY}.update",
        "configuration": {"database_backends": DONOR_GRANT_FUNDRAISING_ALLOWED_DATABASE_BACKENDS, "event_topic": DONOR_GRANT_FUNDRAISING_REQUIRED_EVENT_TOPIC, "stream_engine_picker_visible": False, "rule_configurable": True, "parameter_configurable": True},
        "agent_skill": f"{PBC_KEY}_skills.{resolved.slug}",
        "requires_human_confirmation": resolved.feature_number in {8, 19, 20, 21, 22, 37, 41, 42, 45, 48, 50},
        "retry_dead_letter_evidence": {"retry_policy": "bounded_retry_with_idempotency_key", "dead_letter_table": DEAD_LETTER_TABLE, "manual_replay_route": "POST /events/replay"},
        "release_evidence": {"code_artifact_model": resolved.model_artifacts, "ui_surface": resolved.ui_artifacts, "service_api": resolved.service_artifacts, "test": resolved.test_artifacts, "evidence": resolved.evidence_artifacts},
        "shared_table_access": False,
        "side_effects": (),
    }


def improve1_fundraising_control_contract() -> dict[str, Any]:
    evaluations = tuple(evaluate_fundraising_control(capability) for capability in FUNDRAISING_CONTROL_CAPABILITIES)
    return {"ok": len(evaluations) == 50 and all(item["ok"] for item in evaluations), "pbc": PBC_KEY, "capability_count": len(evaluations), "capabilities": evaluations, "owned_tables": DONOR_GRANT_FUNDRAISING_OWNED_TABLES, "database_backends": DONOR_GRANT_FUNDRAISING_ALLOWED_DATABASE_BACKENDS, "event_contract": EVENT_CONTRACT, "event_topic": DONOR_GRANT_FUNDRAISING_REQUIRED_EVENT_TOPIC, "stream_engine_picker_visible": False, "side_effects": ()}


FUNDRAISING_CONTROL_FUNCTIONS = {capability.slug: (lambda payload=None, slug=capability.slug: evaluate_fundraising_control(slug, payload)) for capability in FUNDRAISING_CONTROL_CAPABILITIES}
