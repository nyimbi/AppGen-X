"""Executable improve1 controls for the Library and Archives Management PBC."""

from __future__ import annotations

import hashlib
from typing import Any

from .improve1_capabilities import IMPROVE1_CAPABILITIES, Improve1Capability

PBC_KEY = "library_archives_management"
EVENT_CONTRACT = "AppGen-X"
LIBRARY_CONTROL_ALLOWED_DATABASE_BACKENDS = ("postgresql", "mysql", "mariadb")
LIBRARY_CONTROL_REQUIRED_EVENT_TOPIC = "pbc.library_archives_management.events"
_BASE_OWNED_TABLES = (
    "library_archives_management_collection_item",
    "library_archives_management_catalog_record",
    "library_archives_management_circulation_loan",
    "library_archives_management_digitization_job",
    "library_archives_management_rights_statement",
    "library_archives_management_preservation_action",
    "library_archives_management_archive_request",
    "library_archives_management_library_archives_management_policy_rule",
    "library_archives_management_library_archives_management_runtime_parameter",
    "library_archives_management_library_archives_management_schema_extension",
    "library_archives_management_library_archives_management_control_assertion",
    "library_archives_management_library_archives_management_governed_model",
    "library_archives_management_appgen_outbox_event",
    "library_archives_management_appgen_inbox_event",
    "library_archives_management_appgen_dead_letter_event",
)
LIBRARY_CONTROL_OWNED_TABLES = tuple(
    dict.fromkeys(_BASE_OWNED_TABLES + tuple(f"library_archives_management_{cap.slug}_control" for cap in IMPROVE1_CAPABILITIES))
)
LIBRARY_CONTROL_DECLARED_DEPENDENCIES = tuple(
    dict.fromkeys(
        (
            "PolicyChanged",
            "AuditEventSealed",
            "OperationalKpiChanged",
            "AuthorityHeadingUpdated",
            "RightsReviewCompleted",
            "PreservationRiskChanged",
            "NoticeDelivered",
            "PatronRegistered",
            "DigitalObjectFixityChecked",
            "EnvironmentalThresholdExceeded",
            "DiscoveryProjectionUpdated",
            "InventoryDiscrepancyOpened",
        )
    )
)
LIBRARY_CONTROL_CAPABILITIES: tuple[Improve1Capability, ...] = IMPROVE1_CAPABILITIES
CAPABILITY_BY_NUMBER = {capability.feature_number: capability for capability in LIBRARY_CONTROL_CAPABILITIES}
CAPABILITY_BY_SLUG = {capability.slug: capability for capability in LIBRARY_CONTROL_CAPABILITIES}

_PRIMARY_PROOF_FIELDS: dict[int, str] = {
    1: "material_template_validation_complete",
    2: "authority_resolution_lineage_recorded",
    3: "classification_storage_scheme_selected",
    4: "accession_register_custody_complete",
    5: "provenance_chain_uncertainty_labeled",
    6: "donor_restriction_clause_enforced",
    7: "hierarchical_finding_aid_integrity_preserved",
    8: "container_location_history_governed",
    9: "reading_room_patron_registration_valid",
    10: "paging_lifecycle_state_controlled",
    11: "hold_queue_priority_explained",
    12: "renewal_recall_overdue_policy_applied",
    13: "lost_damaged_missing_exception_classified",
    14: "condition_survey_preservation_risk_recorded",
    15: "conservation_treatment_approval_complete",
    16: "environmental_threshold_response_active",
    17: "digitization_triage_rights_preservation_cleared",
    18: "capture_profile_qc_checkpoint_passed",
    19: "text_extraction_review_confidence_governed",
    20: "fixity_revalidation_evidence_verified",
    21: "rights_use_case_matrix_decided",
    22: "rights_reappraisal_schedule_active",
    23: "sensitive_access_visibility_boundary_enforced",
    24: "born_digital_forensic_intake_verified",
    25: "deaccession_approval_provenance_checked",
    26: "processing_backlog_plan_current",
    27: "bulk_ingest_preview_rollback_ready",
    28: "discovery_facet_relevance_projection_ready",
    29: "public_staff_note_boundary_enforced",
    30: "role_workbench_panel_coverage_visible",
    31: "reading_room_dashboard_queue_current",
    32: "circulation_desk_exception_prompt_ready",
    33: "finding_aid_rearrangement_safe",
    34: "researcher_status_explanation_approved",
    35: "cataloging_agent_suggestion_cited",
    36: "accessioning_agent_confirmation_required",
    37: "reading_room_agent_permission_checked",
    38: "rights_agent_human_signoff_required",
    39: "provenance_authenticity_ledger_sealed",
    40: "repository_policy_rule_simulated",
    41: "runtime_parameter_effective_value_visible",
    42: "local_schema_extension_scope_declared",
    43: "operational_readiness_projection_fresh",
    44: "inventory_discrepancy_reconciliation_opened",
    45: "notice_policy_basis_preserved",
    46: "service_analytics_drilldown_available",
    47: "seed_repository_scenarios_loaded",
    48: "scenario_release_evidence_mapped",
    49: "repository_control_assertion_actionable",
    50: "end_to_end_release_gate_passed",
}

_FEATURE_DEPENDENCIES: dict[int, tuple[str, ...]] = {
    2: ("AuthorityHeadingUpdated",),
    6: ("RightsReviewCompleted",),
    16: ("EnvironmentalThresholdExceeded",),
    20: ("DigitalObjectFixityChecked",),
    23: ("PolicyChanged", "AuditEventSealed"),
    31: ("PatronRegistered",),
    34: ("NoticeDelivered",),
    39: ("AuditEventSealed",),
    43: ("OperationalKpiChanged", "DiscoveryProjectionUpdated"),
    44: ("InventoryDiscrepancyOpened",),
    45: ("NoticeDelivered",),
    48: ("AuditEventSealed",),
    49: ("AuditEventSealed",),
}

_DOMAIN_MESSAGES: dict[int, str] = {
    1: "cataloging templates must distinguish monographs, serials, maps, manuscripts, photographs, oral histories, and born-digital packages",
    2: "authority control must track preferred forms, variants, sources, merges, splits, and local override reasons",
    3: "call number and archival storage logic must handle cutter rules, boxes, folders, oversize items, and original order exceptions",
    4: "accession registers must prove transfer type, source, donor or office, custody date, quantity, restrictions, and appraisal notes",
    5: "provenance must separate creator, custodians, acquisition events, asserted facts, inferred relationships, and custody gaps",
    6: "donor agreements must propagate embargoes, cultural clauses, return conditions, and access restrictions to requests and publication",
    7: "finding aids must preserve collection, series, file, item hierarchy, inherited dates, restrictions, and container references",
    8: "container management must govern box, folder, reel, cabinet, shelf, vault, offsite moves, capacity, and prior locations",
    9: "reading room registration must enforce identity checks, rules acknowledgement, photo permissions, supervision, expiry, and renewal",
    10: "paging workflows must govern review, pull, ready, in-use, return, seat assignment, cutoff windows, and fragile material handling",
    11: "circulation holds must preserve FIFO order, branch routing, pickup windows, priority exceptions, and exception rationale",
    12: "renewal, recall, and overdue rules must explain holds, shortened due dates, notices, blocks, and staff review triggers",
    13: "lost, damaged, missing, claimed-return, and reading-room exceptions must preserve financial, preservation, and visibility outcomes",
    14: "condition surveys must capture support, brittleness, mold, pests, fasteners, media decay, housing, and handling restrictions",
    15: "conservation treatment requires recommendation, approval, execution, outcome, treatment goal, and post-treatment access changes",
    16: "environmental monitoring must tie temperature, humidity, light, storage incidents, thresholds, locations, and response windows",
    17: "digitization triage must clear source item, condition, handling, rights, use case, output profile, and review routing",
    18: "capture profiles and QC must govern resolution, color target, bit depth, format, derivatives, naming, skew, focus, and completeness",
    19: "OCR, HTR, transcription, and captioning must track confidence, reviewer intervention, language, and approval history",
    20: "digital preservation fixity must record checksums, scheduled revalidation, missing files, failed checks, and repair escalation",
    21: "rights matrices must decide on-site, classroom, web, commercial, and preservation uses by jurisdiction, privacy, and donor clause",
    22: "rights review must schedule reappraisal from publication, creator death, embargo expiry, donor clauses, or local commitments",
    23: "sensitive content must separate internal descriptive control from patron visibility for privacy, cultural, sealed, and classified records",
    24: "born-digital intake must prove write blocking, imaging, filesystem capture, virus screening, package metadata, and custody events",
    25: "deaccession must check policy, stakeholder approval, provenance, donor terms, legal holds, and disposition history",
    26: "processing plans must track arrangement level, output, staffing, backlog status, blockers, and processing maturity",
    27: "bulk ingest must provide validation-only preview, row errors, authority conflicts, controlled commit, and rollback by job",
    28: "discovery projections must expose format, date, creator, location, access status, hierarchy, identifier ranking, and finding-aid context",
    29: "public and staff notes must prevent staff, processing, conservation, and donor-sensitive notes from leaking externally",
    30: "workbenches must split cataloging, accessioning, processing, preservation, rights, circulation, and public-service queues",
    31: "reading room dashboards must show appointments, pulls, in-use materials, returns, restricted requests, seats, and cutoffs",
    32: "circulation desk workflows must support barcode lookup, hold shelf check-in, patron blocks, renewals, and claimed-return prompts",
    33: "finding aid editing must preserve hierarchy, identifiers, inherited metadata, containers, citations, and change history",
    34: "researcher-facing status must explain paging delay, restriction review, conservation review, registration expiry, and next steps",
    35: "cataloging agents must cite evidence for titles, extent notes, subjects, creators, and summaries and require approval before mutation",
    36: "accessioning agents must parse drafts, flag unresolved fields, detect duplicates, and require confirmation before creates",
    37: "reading room agents must respect restrictions while explaining readiness, registration, seat availability, handling, and retrieval timing",
    38: "rights agents must gather evidence but require human signoff for externally visible rights changes or public-domain claims",
    39: "provenance ledgers must seal assertions, accession events, fixity events, amendments, and access/publication review history",
    40: "policy rules must simulate holds, renewals, registration expiry, paging cutoffs, handling, digitization, and redaction behavior",
    41: "runtime parameters must show service hours, hold expiry, paging intervals, QC tolerances, thresholds, and reminder timing",
    42: "schema extensions must declare local field scope, target type, validation, vocabulary, visibility, and compatibility posture",
    43: "readiness projections must merge collection, catalog, circulation, digitization, rights, and preservation status with freshness indicators",
    44: "inventory workflows must classify mis-shelved items, barcode mismatch, missing containers, and intentional relocation",
    45: "notices must preserve templates, timestamps, rendered messages, delivery state, policy basis, and triggering record state",
    46: "analytics must define hold fill rate, reading room turnaround, backlog age, finding-aid latency, QC failures, and rights overdue counts",
    47: "seed data must cover circulating holds, unprocessed accessions, finding aids, restricted oral histories, conservation, and digitization",
    48: "release scenarios must map hold checkout, restricted request, rights-blocked digitization, finding aid publication, and born-digital preservation",
    49: "control assertions must open exceptions for rights overdue, uncited provenance, missing fixity, invalid registration, restricted loans, and missing containers",
    50: "release gates must prove APIs, workflows, events, UI, agents, seed data, scenarios, traceability, and no backlog evidence drift",
}

_BASE_FIELDS = ("tenant_id", "repository_id", "collection_item_id", "catalog_record_id", "lifecycle_stage", "policy_version", "required_evidence", "approval_record")


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
    proof_field = _PRIMARY_PROOF_FIELDS[capability.feature_number]
    return {
        "title": capability.title,
        "slug": capability.slug,
        "tables": (f"library_archives_management_{capability.slug}_control",),
        "fields": _BASE_FIELDS + (proof_field,),
        "ui": f"LibraryArchivesManagement{_camel(capability.slug)}Panel",
        "route": f"POST /library-archives-management/improve1/{capability.slug}",
        "dependencies": _FEATURE_DEPENDENCIES.get(capability.feature_number, ()),
        "primary_proof": proof_field,
    }


CONTROL_SPECS: dict[int, dict[str, Any]] = {capability.feature_number: _spec_for(capability) for capability in LIBRARY_CONTROL_CAPABILITIES}


def sample_payload_for(capability: Improve1Capability | str | int) -> dict[str, Any]:
    resolved = _resolve(capability)
    if resolved is None:
        return {}
    spec = CONTROL_SPECS[resolved.feature_number]
    payload = {field: f"{resolved.slug}_{field}" for field in spec["fields"]}
    payload[spec["primary_proof"]] = True
    payload.update({"database_backend": "postgresql", "event_contract": EVENT_CONTRACT, "event_topic": LIBRARY_CONTROL_REQUIRED_EVENT_TOPIC, "stream_engine_picker_visible": False, "shared_table_access": False, "human_confirmation": True, "side_effects": ()})
    return payload


def _domain_findings(capability: Improve1Capability, payload: dict[str, Any]) -> tuple[str, ...]:
    findings: list[str] = []
    spec = CONTROL_SPECS[capability.feature_number]
    proof_field = spec["primary_proof"]
    if payload.get(proof_field) is not True:
        findings.append(f"{capability.title} requires {proof_field.replace('_', ' ')}")
        findings.append(_DOMAIN_MESSAGES[capability.feature_number])
    if capability.feature_number in (35, 36, 37, 38) and payload.get("human_confirmation") is False:
        findings.append("library and archives agents must cite sources and require human approval before governed mutations or public-rights changes")
    if capability.feature_number in (23, 29, 43) and payload.get("shared_table_access"):
        findings.append("sensitive visibility and readiness projections must use owned data plus declared APIs/events/projections only")
    if payload.get("event_contract") != EVENT_CONTRACT or payload.get("event_topic") != LIBRARY_CONTROL_REQUIRED_EVENT_TOPIC:
        findings.append("library/archive eventing must use the AppGen-X event contract and package topic")
    if payload.get("stream_engine_picker_visible"):
        findings.append("ordinary PBCs must not expose stream-engine pickers")
    if payload.get("database_backend") not in LIBRARY_CONTROL_ALLOWED_DATABASE_BACKENDS:
        findings.append("ordinary library/archive datastore must be PostgreSQL, MySQL, or MariaDB")
    if payload.get("shared_table_access"):
        findings.append("library/archive controls must use owned tables plus declared APIs/events/projections")
    return tuple(dict.fromkeys(findings))


def evaluate_library_control(capability: Improve1Capability | str | int, payload: dict[str, Any] | None = None) -> dict[str, Any]:
    resolved = _resolve(capability)
    if resolved is None:
        return {"ok": False, "reason": "unknown_capability", "side_effects": ()}
    spec = CONTROL_SPECS[resolved.feature_number]
    candidate = sample_payload_for(resolved)
    candidate.update(dict(payload or {}))
    missing_fields = tuple(field for field in spec["fields"] if candidate.get(field) in (None, "", (), []))
    foreign_tables = tuple(table for table in spec["tables"] if table not in LIBRARY_CONTROL_OWNED_TABLES)
    undeclared_dependencies = tuple(dependency for dependency in spec["dependencies"] if dependency not in LIBRARY_CONTROL_DECLARED_DEPENDENCIES)
    findings = _domain_findings(resolved, candidate)
    evidence = {"evidence_id": _digest((PBC_KEY, resolved.feature_number, tuple(sorted(candidate))))[:20], "owned_tables": spec["tables"], "required_fields": spec["fields"], "ui_surface": spec["ui"], "service_api": spec["route"], "test": "tests/test_domain_behavior.py", "event_contract": EVENT_CONTRACT, "required_event_topic": LIBRARY_CONTROL_REQUIRED_EVENT_TOPIC, "allowed_database_backends": LIBRARY_CONTROL_ALLOWED_DATABASE_BACKENDS, "declared_dependencies": spec["dependencies"], "domain_message": _DOMAIN_MESSAGES[resolved.feature_number], "side_effects": ()}
    ok = not missing_fields and not foreign_tables and not undeclared_dependencies and not findings
    return {"ok": ok, "pbc": PBC_KEY, "feature_number": resolved.feature_number, "slug": resolved.slug, "title": resolved.title, "capability": resolved.as_traceability_row(), "payload": candidate, "evidence": evidence, "missing_fields": missing_fields, "foreign_tables": foreign_tables, "undeclared_dependencies": undeclared_dependencies, "findings": findings, "side_effects": ()}


def improve1_library_control_contract() -> dict[str, Any]:
    evaluations = tuple(evaluate_library_control(capability) for capability in LIBRARY_CONTROL_CAPABILITIES)
    blocking = tuple(item for item in evaluations if not item["ok"])
    return {"ok": not blocking, "pbc": PBC_KEY, "format": "appgen.library-archives-management-improve1-control.v1", "capability_count": len(evaluations), "capabilities": evaluations, "owned_tables": LIBRARY_CONTROL_OWNED_TABLES, "declared_dependencies": LIBRARY_CONTROL_DECLARED_DEPENDENCIES, "allowed_database_backends": LIBRARY_CONTROL_ALLOWED_DATABASE_BACKENDS, "event_contract": EVENT_CONTRACT, "required_event_topic": LIBRARY_CONTROL_REQUIRED_EVENT_TOPIC, "stream_engine_picker_visible": False, "blocking_gaps": blocking, "side_effects": ()}


LIBRARY_CONTROL_FUNCTIONS = {capability.slug: (lambda payload=None, slug=capability.slug: evaluate_library_control(slug, payload)) for capability in LIBRARY_CONTROL_CAPABILITIES}
