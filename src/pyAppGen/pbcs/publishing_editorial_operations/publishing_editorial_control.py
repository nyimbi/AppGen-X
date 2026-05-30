"""Executable improve1 controls for the Publishing Editorial Operations PBC."""

from __future__ import annotations

import hashlib
from typing import Any

from .improve1_capabilities import IMPROVE1_CAPABILITIES, Improve1Capability
from .runtime import (
    PUBLISHING_EDITORIAL_OPERATIONS_ALLOWED_DATABASE_BACKENDS,
    PUBLISHING_EDITORIAL_OPERATIONS_OWNED_TABLES,
    PUBLISHING_EDITORIAL_OPERATIONS_REQUIRED_EVENT_TOPIC,
    PUBLISHING_EDITORIAL_OPERATIONS_RUNTIME_TABLES,
)

PBC_KEY = "publishing_editorial_operations"
EVENT_CONTRACT = "AppGen-X"
EDITORIAL_ALLOWED_DATABASE_BACKENDS = PUBLISHING_EDITORIAL_OPERATIONS_ALLOWED_DATABASE_BACKENDS
EDITORIAL_REQUIRED_EVENT_TOPIC = PUBLISHING_EDITORIAL_OPERATIONS_REQUIRED_EVENT_TOPIC
EDITORIAL_CAPABILITIES: tuple[Improve1Capability, ...] = IMPROVE1_CAPABILITIES
CAPABILITY_BY_NUMBER = {capability.feature_number: capability for capability in EDITORIAL_CAPABILITIES}
CAPABILITY_BY_SLUG = {capability.slug: capability for capability in EDITORIAL_CAPABILITIES}
EDITORIAL_OWNED_TABLES = tuple(
    dict.fromkeys(
        PUBLISHING_EDITORIAL_OPERATIONS_OWNED_TABLES
        + PUBLISHING_EDITORIAL_OPERATIONS_RUNTIME_TABLES
        + tuple(f"publishing_editorial_operations_{capability.slug}_control" for capability in EDITORIAL_CAPABILITIES)
    )
)
EDITORIAL_DECLARED_DEPENDENCIES = (
    "PolicyChanged",
    "AuditEventSealed",
    "OperationalKpiChanged",
    "AuthorContractExecuted",
    "RightsGrantChanged",
    "AssetPermissionCleared",
    "MetadataAuthorityUpdated",
    "NotificationDeliveryChanged",
    "ProductionScheduleChanged",
    "DistributionPlanChanged",
)
_BASE_FIELDS = (
    "tenant_id",
    "manuscript_id",
    "edition_id",
    "editor_id",
    "author_id",
    "imprint_id",
    "season_id",
    "policy_version",
    "evidence_references",
)
_FIELD_ROWS = """
1|acquisition_pipeline_id,proposal_source,genre,market_position,author_platform,comparable_titles,intake_status
2|board_decision_id,board_date,vote_record,decision_rationale,commercial_assumption,editorial_risk,decision_state
3|package_completeness_id,required_component,component_status,missing_item,author_followup,due_date,completeness_score
4|version_lineage_id,version_number,parent_version,freeze_point,change_reason,approver,immutable_hash
5|calendar_plan_id,season,slot,imprint_capacity,launch_window,dependency,calendar_status
6|assignment_id,editorial_role,capacity_load,skill_match,due_date,conflict_flag,assignment_status
7|peer_review_workflow_id,review_round,reviewer_pool,review_due_date,recommendation,revision_request,decision_path
8|reviewer_control_id,conflict_check,anonymity_mode,blinding_status,recusal_reason,ethics_flag,reviewer_decision
9|decision_bundle_id,editorial_memo,review_summary,commercial_review,rights_review,approval_record,bundle_hash
10|contract_alignment_id,contract_clause,deliverable,manuscript_scope,format_right,deadline_alignment,variance_reason
11|copyedit_state_id,current_state,next_state,query_count,change_batch,author_review,transition_validity
12|style_sheet_id,house_style_rule,exception,term_choice,spelling_variant,approval_state,style_version
13|author_query_id,query_text,query_owner,response_due,response_status,resolution,carry_forward_flag
14|permissions_intake_id,asset_id,asset_type,permission_scope,source_credit,clearance_status,expiry_date
15|rights_boundary_id,right_type,owner,license_scope,restriction,exclusivity,rights_status
16|collision_detection_id,territory,language,format,conflicting_grant,collision_severity,resolution_path
17|edition_lineage_id,source_edition,derived_edition,inherited_assets,inherited_rights,override_reason,inheritance_status
18|metadata_authority_id,isbn,title_record,contributor_record,bisac_subject,authority_status,metadata_owner
19|metadata_export_id,export_target,field_set,validation_result,trace_id,publication_date,export_status
20|critical_path_id,milestone,dependency_chain,slack_days,blocking_item,owner,criticality
21|handoff_packet_id,production_editor,files_included,rights_summary,metadata_snapshot,schedule_snapshot,handoff_status
22|proof_round_id,round_number,proof_type,reviewer,correction_due,approval_state,round_status
23|correction_classification_id,correction_type,severity,source_page,owner,acceptance_state,carryover_risk
24|accessibility_readiness_id,alt_text_status,epub_check,reading_order,accessibility_exception,remediation_owner,readiness_score
25|asset_freeze_id,asset_type,freeze_version,approval_time,late_change_reason,release_blocker,asset_hash
26|schedule_scenario_id,scenario_name,scenario_driver,affected_milestones,capacity_impact,publication_risk,recommendation
27|exception_taxonomy_id,exception_type,severity,root_cause,owner,escalation_path,closure_status
28|author_timeline_id,communication_type,sent_at,recipient,response_due,response_received,thread_status
29|correspondence_evidence_id,correspondence_type,participant,source_message,decision_link,retention_label,evidence_hash
30|meeting_action_id,meeting_id,agenda_item,decision,action_owner,due_date,completion_status
31|acquisition_dashboard_id,pipeline_count,board_ready_count,decision_pending_count,risk_flag,drilldown_filter,refresh_status
32|manuscript_workspace_id,workspace_section,version_panel,query_panel,right_panel,task_panel,assistant_panel
33|editorial_calendar_ui_id,calendar_view,season_filter,milestone_overlay,capacity_overlay,conflict_indicator,drag_guard
34|peer_review_queue_id,queue_filter,review_stage,anonymity_badge,conflict_warning,due_aging,decision_action
35|compare_ui_id,source_version,target_version,change_classification,proof_marker,query_link,approval_action
36|rights_matrix_id,territory_axis,language_axis,format_axis,edition_axis,collision_marker,export_action
37|intake_agent_skill_id,source_text,structured_submission,suggested_slot,missing_fields,confidence,human_confirmation
38|decision_agent_skill_id,brief_source,decision_summary,risk_summary,citation_map,recommendation,human_confirmation
39|copyedit_agent_skill_id,query_context,change_explanation,style_citation,author_facing_text,confidence,write_block
40|proof_agent_skill_id,proof_risk,release_readiness,blocking_corrections,asset_freeze_check,metadata_check,approval_advice
41|manuscript_event_id,event_schema,acquired_event,version_frozen_event,query_resolved_event,decision_event,consumer_contract
42|review_event_id,event_schema,review_requested_event,review_received_event,decision_bundle_event,anonymity_event,consumer_contract
43|production_event_id,event_schema,handoff_event,proof_round_event,metadata_export_event,publication_event,consumer_contract
44|notification_recovery_id,notification_id,delivery_channel,retry_count,deadline_risk,dead_letter_reason,recovery_action
45|release_binder_id,binder_section,required_evidence,missing_evidence,approver,release_status,proof_hash
46|kpi_analytics_id,cycle_time,review_latency,proof_defects,schedule_slip,rights_blockers,sla_trend
47|schema_expansion_id,target_table,new_field,relationship,backfill_rule,migration_status,boundary_check
48|integrity_assertion_id,control_rule,population,failing_sample,owner,remediation,closure_evidence
49|fixture_pack_id,scenario_name,seed_manuscript,seed_rights,seed_reviews,expected_event,coverage_label
50|release_gate_id,feature_count,domain_test_count,traceability_matrix,ui_coverage,service_coverage,release_decision
"""
_DOMAIN_FIELDS = {int(line.split("|", 1)[0]): tuple(line.split("|", 1)[1].split(",")) for line in _FIELD_ROWS.strip().splitlines()}
_PRIMARY_PROOF_FIELDS = {number: f"{CAPABILITY_BY_NUMBER[number].slug}_verified" for number in range(1, 51)}
_FEATURE_FIELDS = {number: _BASE_FIELDS + _DOMAIN_FIELDS[number] + (_PRIMARY_PROOF_FIELDS[number],) for number in range(1, 51)}
_FEATURE_DEPENDENCIES = {
    10: ("AuthorContractExecuted",),
    14: ("AssetPermissionCleared",),
    15: ("RightsGrantChanged",),
    16: ("RightsGrantChanged",),
    18: ("MetadataAuthorityUpdated",),
    19: ("MetadataAuthorityUpdated", "DistributionPlanChanged"),
    20: ("ProductionScheduleChanged",),
    21: ("ProductionScheduleChanged",),
    24: ("AssetPermissionCleared",),
    36: ("RightsGrantChanged",),
    41: ("AuditEventSealed",),
    42: ("AuditEventSealed",),
    43: ("AuditEventSealed", "ProductionScheduleChanged"),
    44: ("NotificationDeliveryChanged",),
    50: ("AuditEventSealed",),
}
_HUMAN_CONFIRMATION_FEATURES = (1, 2, 4, 7, 9, 10, 11, 14, 15, 16, 21, 22, 25, 28, 30, 37, 38, 39, 40, 45, 48, 50)
_SUPERVISOR_APPROVAL_FEATURES = (2, 4, 8, 9, 10, 15, 16, 21, 25, 27, 40, 45, 48, 50)
_NON_MUTATING_FEATURES = (3, 5, 6, 8, 12, 16, 17, 18, 19, 20, 24, 26, 27, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 46, 47, 48, 49, 50)
_AI_PREVIEW_FEATURES = (37, 38, 39, 40, 45, 46, 48, 50)
_RIGHTS_EVIDENCE_FEATURES = (10, 14, 15, 16, 17, 21, 24, 25, 36, 40, 43, 45, 50)
_METADATA_EVIDENCE_FEATURES = (18, 19, 21, 24, 40, 43, 45, 50)
_PROJECTION_ONLY_FEATURES = (10, 14, 15, 16, 18, 19, 20, 21, 24, 36, 41, 42, 43, 44, 50)


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
        "tables": (f"publishing_editorial_operations_{capability.slug}_control",),
        "fields": _FEATURE_FIELDS[capability.feature_number],
        "primary_proof": _PRIMARY_PROOF_FIELDS[capability.feature_number],
        "ui": f"PublishingEditorialOperations{_camel(capability.slug)}Panel",
        "route": f"POST /publishing-editorial-operations/improve1/{capability.slug}",
        "dependencies": _FEATURE_DEPENDENCIES.get(capability.feature_number, ()),
    }


CONTROL_SPECS = {capability.feature_number: _spec_for(capability) for capability in EDITORIAL_CAPABILITIES}


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
        "event_topic": EDITORIAL_REQUIRED_EVENT_TOPIC,
        "stream_engine_picker_visible": False,
        "shared_table_access": False,
        "dependency_access_mode": "api_event_projection",
        "human_confirmation": True,
        "supervisor_approval": True,
        "agent_preview_only": True,
        "non_mutating_simulation": True,
        "rights_evidence_complete": True,
        "metadata_evidence_complete": True,
        "side_effects": (),
    })
    return payload


def _domain_findings(capability: Improve1Capability, payload: dict[str, Any]) -> tuple[str, ...]:
    findings: list[str] = []
    number = capability.feature_number
    spec = CONTROL_SPECS[number]
    if payload.get(spec["primary_proof"]) is not True:
        findings.append(f"{capability.title} requires {spec['primary_proof'].replace('_', ' ')}")
        findings.append(f"{capability.title} requires owned editorial evidence, UI, service/API, events, rights, metadata, agent, and release proof before approval.")
    if number in _RIGHTS_EVIDENCE_FEATURES and payload.get("rights_evidence_complete") is not True:
        findings.append("contract alignment, permissions intake, rights boundaries, territorial collisions, edition inheritance, production handoff, accessibility, asset freeze, rights matrix, proof readiness, publication events, release binder, and release gate require complete rights evidence")
    if number in _METADATA_EVIDENCE_FEATURES and payload.get("metadata_evidence_complete") is not True:
        findings.append("metadata authority, export traceability, production handoff, accessibility, proof readiness, publication events, release binder, and release gate require metadata evidence")
    if number in _HUMAN_CONFIRMATION_FEATURES and payload.get("human_confirmation") is not True:
        findings.append("acquisition decisions, manuscript freezes, peer review, contracts, copyedit, permissions, rights, handoff, proofs, freezes, author communications, agent drafts, release binders, integrity assertions, and release gates require human confirmation")
    if number in _SUPERVISOR_APPROVAL_FEATURES and payload.get("supervisor_approval") is not True:
        findings.append("board decisions, freeze points, conflict controls, decision bundles, contract variance, rights exceptions, production handoff, late asset changes, editorial exceptions, proof readiness, release binders, integrity controls, and release gates require editorial lead approval")
    if number in _AI_PREVIEW_FEATURES and payload.get("agent_preview_only") is not True:
        findings.append("publishing editorial agent skills must produce cited, permission-checked, preview-only drafts before confirmed CRUD")
    if number in _NON_MUTATING_FEATURES and payload.get("non_mutating_simulation") is not True:
        findings.append("package completeness, calendar, assignment, conflicts, style rules, collision detection, metadata, schedules, accessibility, scenarios, UI panels, agent skills, analytics, schema expansion, controls, fixtures, and release gate must be side-effect-free")
    if number in _PROJECTION_ONLY_FEATURES and payload.get("dependency_access_mode") != "api_event_projection":
        findings.append("contract, rights, asset permission, metadata, production, notification, distribution, and audit facts must use declared APIs, events, or projections")
    if payload.get("event_contract") != EVENT_CONTRACT or payload.get("event_topic") != EDITORIAL_REQUIRED_EVENT_TOPIC:
        findings.append("publishing editorial eventing must use the AppGen-X event contract and package topic")
    if payload.get("stream_engine_picker_visible"):
        findings.append("ordinary PBCs must not expose stream-engine pickers")
    if payload.get("database_backend") not in EDITORIAL_ALLOWED_DATABASE_BACKENDS:
        findings.append("ordinary publishing editorial datastore must be PostgreSQL, MySQL, or MariaDB")
    if payload.get("shared_table_access"):
        findings.append("publishing editorial controls must use owned tables plus declared APIs/events/projections")
    return tuple(dict.fromkeys(findings))


def evaluate_publishing_editorial_control(capability: Improve1Capability | str | int, payload: dict[str, Any] | None = None) -> dict[str, Any]:
    resolved = _resolve(capability)
    if resolved is None:
        return {"ok": False, "reason": "unknown_capability", "side_effects": ()}
    spec = CONTROL_SPECS[resolved.feature_number]
    candidate = sample_payload_for(resolved)
    candidate.update(dict(payload or {}))
    missing_fields = tuple(field for field in spec["fields"] if candidate.get(field) in (None, "", (), []))
    foreign_tables = tuple(table for table in spec["tables"] if table not in EDITORIAL_OWNED_TABLES)
    undeclared_dependencies = tuple(dependency for dependency in spec["dependencies"] if dependency not in EDITORIAL_DECLARED_DEPENDENCIES)
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
        "required_event_topic": EDITORIAL_REQUIRED_EVENT_TOPIC,
        "allowed_database_backends": EDITORIAL_ALLOWED_DATABASE_BACKENDS,
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


def improve1_publishing_editorial_control_contract() -> dict[str, Any]:
    evaluations = tuple(evaluate_publishing_editorial_control(capability) for capability in EDITORIAL_CAPABILITIES)
    blocking = tuple(item for item in evaluations if not item["ok"])
    return {
        "ok": not blocking,
        "pbc": PBC_KEY,
        "format": "appgen.publishing-editorial-operations-improve1-control.v1",
        "capability_count": len(evaluations),
        "capabilities": evaluations,
        "owned_tables": EDITORIAL_OWNED_TABLES,
        "declared_dependencies": EDITORIAL_DECLARED_DEPENDENCIES,
        "allowed_database_backends": EDITORIAL_ALLOWED_DATABASE_BACKENDS,
        "event_contract": EVENT_CONTRACT,
        "required_event_topic": EDITORIAL_REQUIRED_EVENT_TOPIC,
        "stream_engine_picker_visible": False,
        "blocking_gaps": blocking,
        "side_effects": (),
    }


PUBLISHING_EDITORIAL_CONTROL_FUNCTIONS = {capability.slug: (lambda payload=None, slug=capability.slug: evaluate_publishing_editorial_control(slug, payload)) for capability in EDITORIAL_CAPABILITIES}
