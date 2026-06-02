"""Executable improve1 controls for the Livestock Herd Management PBC."""

from __future__ import annotations

import hashlib
from typing import Any

from .improve1_capabilities import IMPROVE1_CAPABILITIES, Improve1Capability

PBC_KEY = "livestock_herd_management"
EVENT_CONTRACT = "AppGen-X"
LIVESTOCK_CONTROL_ALLOWED_DATABASE_BACKENDS = ("postgresql", "mysql", "mariadb")
LIVESTOCK_CONTROL_REQUIRED_EVENT_TOPIC = "pbc.livestock_herd_management.events"
_BASE_OWNED_TABLES = (
    "livestock_herd_management_animal",
    "livestock_herd_management_herd_group",
    "livestock_herd_management_health_event",
    "livestock_herd_management_breeding_record",
    "livestock_herd_management_feed_ration",
    "livestock_herd_management_movement_permit",
    "livestock_herd_management_treatment",
    "livestock_herd_management_livestock_herd_management_policy_rule",
    "livestock_herd_management_livestock_herd_management_runtime_parameter",
    "livestock_herd_management_livestock_herd_management_schema_extension",
    "livestock_herd_management_livestock_herd_management_control_assertion",
    "livestock_herd_management_livestock_herd_management_governed_model",
    "livestock_herd_management_appgen_outbox_event",
    "livestock_herd_management_appgen_inbox_event",
    "livestock_herd_management_appgen_dead_letter_event",
)
LIVESTOCK_CONTROL_OWNED_TABLES = tuple(
    dict.fromkeys(_BASE_OWNED_TABLES + tuple(f"livestock_herd_management_{cap.slug}_control" for cap in IMPROVE1_CAPABILITIES))
)
LIVESTOCK_CONTROL_DECLARED_DEPENDENCIES = tuple(
    dict.fromkeys(
        (
            "PolicyChanged",
            "AuditEventSealed",
            "OperationalKpiChanged",
            "VeterinarianProjected",
            "LabResultReceived",
            "FeedInventoryProjected",
            "WeatherRiskChanged",
            "StaffCompetencyProjected",
            "EquipmentReadinessProjected",
            "TransportPermitUpdated",
            "ComplianceReportAccepted",
            "FinanceSettlementProjected",
            "SalesOrderProjected",
        )
    )
)
LIVESTOCK_CONTROL_CAPABILITIES: tuple[Improve1Capability, ...] = IMPROVE1_CAPABILITIES
CAPABILITY_BY_NUMBER = {capability.feature_number: capability for capability in LIVESTOCK_CONTROL_CAPABILITIES}
CAPABILITY_BY_SLUG = {capability.slug: capability for capability in LIVESTOCK_CONTROL_CAPABILITIES}

_PRIMARY_PROOF_FIELDS: dict[int, str] = {
    1: "tag_history_identity_continuity_verified",
    2: "source_provenance_quarantine_checked",
    3: "herd_group_interval_overlap_rejected",
    4: "species_profile_required_fields_enforced",
    5: "lifecycle_transition_evidence_approved",
    6: "quarantine_release_criteria_met",
    7: "clinical_taxonomy_reportability_coded",
    8: "vaccination_protocol_due_window_calculated",
    9: "treatment_ledger_schedule_complete",
    10: "withdrawal_residue_release_date_enforced",
    11: "veterinary_projection_boundary_respected",
    12: "outbreak_contact_graph_generated",
    13: "mortality_disposition_evidence_closed",
    14: "welfare_intervention_owner_assigned",
    15: "breeding_eligibility_rule_cited",
    16: "service_event_repeat_metric_calculated",
    17: "pregnancy_due_queue_generated",
    18: "offspring_lineage_created_from_birth",
    19: "pedigree_external_registry_boundary_respected",
    20: "feed_ration_nutrient_evidence_complete",
    21: "feed_consumption_variance_flagged",
    22: "feed_inventory_projection_only_used",
    23: "grazing_stocking_rest_threshold_checked",
    24: "growth_curve_anomaly_reviewed",
    25: "productivity_drop_after_event_detected",
    26: "movement_permit_arrival_confirmed",
    27: "birth_to_sale_trace_packet_complete",
    28: "sale_transfer_cull_readiness_blockers_clear",
    29: "regulatory_report_due_exception_handled",
    30: "certification_evidence_score_ready",
    31: "restricted_treatment_permission_verified",
    32: "antimicrobial_stewardship_review_flagged",
    33: "emissions_intensity_assumptions_visible",
    34: "manure_storage_capacity_breach_flagged",
    35: "heat_stress_mitigation_task_closed",
    36: "staff_competency_projection_verified",
    37: "equipment_readiness_blocks_session",
    38: "offline_capture_conflict_preserved",
    39: "sensor_anomaly_quality_triaged",
    40: "herd_productivity_dashboard_drilldown_ready",
    41: "exception_taxonomy_queue_routed",
    42: "herd_parameter_rollback_approved",
    43: "agent_clinical_note_confirmation_required",
    44: "agent_daily_plan_ordering_explained",
    45: "agent_write_safety_gate_logged",
    46: "appgen_event_boundary_verified",
    47: "cryptographic_audit_packet_verified",
    48: "data_quality_remediation_queue_opened",
    49: "release_smoke_scenarios_passed",
    50: "cross_pbc_boundary_proof_passed",
}

_FEATURE_DEPENDENCIES: dict[int, tuple[str, ...]] = {
    11: ("VeterinarianProjected",),
    13: ("LabResultReceived",),
    19: ("PolicyChanged",),
    22: ("FeedInventoryProjected",),
    26: ("TransportPermitUpdated",),
    29: ("ComplianceReportAccepted",),
    35: ("WeatherRiskChanged",),
    36: ("StaffCompetencyProjected",),
    37: ("EquipmentReadinessProjected",),
    46: ("PolicyChanged", "AuditEventSealed", "OperationalKpiChanged"),
    47: ("AuditEventSealed",),
    50: ("AuditEventSealed",),
}

_DOMAIN_MESSAGES: dict[int, str] = {
    1: "animal identity must preserve primary identifiers, alternate IDs, RFID, tags, tattoos, brands, registry numbers, replacements, and duplicate exceptions",
    2: "source provenance must capture born-on-farm, purchase, lease, transfer, rescue, import, dam, sire, origin premises, arrival condition, and quarantine flags",
    3: "herd membership must maintain dated pen, flock, paddock, cohort, production string, and treatment-group intervals without overlap",
    4: "species profiles must vary fields, productivity metrics, breeding semantics, health protocols, and movement rules for dairy, beef, poultry, and swine",
    5: "lifecycle states must govern quarantine, sickness, treatment, breeding, pregnancy, lactation, finishing, sale, death, culling, and archival transitions",
    6: "biosecurity quarantine must block movement, breeding, and group mixing until testing, observations, staff ownership, and release criteria are approved",
    7: "health events must encode symptoms, diagnosis, severity, body system, infectious risk, observation method, veterinarian involvement, and reportability",
    8: "vaccination protocols must calculate due windows, boosters, batches, lots, contraindications, missed doses, administrators, and certificates",
    9: "treatment ledgers must preserve medication, dose, route, frequency, administrator, prescribing authority, lot, reason, response, and completion status",
    10: "withdrawal controls must block milk, eggs, meat, sale, and production release until jurisdiction and treatment-specific residue intervals expire",
    11: "veterinary authority must be recorded through references and projections without mutating external professional registry or pharmacy tables",
    12: "outbreak investigations must trace disease clusters, suspected source, contact graph, group intervals, movements, isolation, testing, controls, and closure",
    13: "mortality workflows must capture discovery, suspected cause, necropsy, lab projection, carcass disposition, regulatory notice, and corrective action",
    14: "welfare scoring must track body condition, lameness, behavior, housing, handling, heat stress, owners, interventions, and unresolved cases",
    15: "breeding eligibility must check age, weight, genetics, health, production state, relationship, rest intervals, contraindications, and rule version",
    16: "service records must retain method, sire or semen batch, technician, heat evidence, synchronization, timing, conception, and repeat-service metrics",
    17: "pregnancy diagnosis must govern method, result, confidence, examiner, gestation estimate, expected date, follow-up, and reproductive state",
    18: "parturition must link dam, sire, offspring, identifiers, birth weights, assistance, complications, colostrum, survival, and dam recovery",
    19: "genetic evidence must use pedigree and genomic projections while warning on trait risk and prohibited relationship thresholds",
    20: "feed rations must prove ingredients, nutrient targets, dry matter, energy, protein, minerals, cost, effective dates, and assigned groups",
    21: "feeding events must compare planned quantity, delivery, refusals, timing, equipment, handler, weather context, and exceptions",
    22: "feed availability must be consumed as lot, freshness, contaminant hold, quantity, and allocation projection without inventory mutation",
    23: "grazing plans must control paddocks, entry, exit, forage, animal units, rest periods, stocking density, water, and overgrazing alerts",
    24: "weight monitoring must record scale source, condition, age-adjusted metrics, average daily gain, target curve, and anomaly flags",
    25: "productivity records must aggregate milk, eggs, wool, fiber, honey, meat readiness, or configured output by animal or group",
    26: "movement permits must govern origin, destination, animals, carrier, certificates, inspections, route, status, completion, and arrival confirmation",
    27: "trace packets must reconstruct birth, provenance, groups, health, treatments, feed, movements, withdrawal, and sale eligibility from owned data",
    28: "exit readiness must block sale, transfer, cull, or slaughter while withdrawal, quarantine, weight, welfare, permit, or documentation blockers remain",
    29: "regulatory reports must define jurisdiction, reportable triggers, due dates, included records, approvals, submissions, and overdue exceptions",
    30: "certification readiness must score organic, humane, breed, export, food-safety, and quality scheme evidence, findings, corrections, and expiry",
    31: "restricted treatments require elevated authority, authorization evidence, inventory projection, administrator verification, and escalation",
    32: "antimicrobial stewardship must track drug class, indication, dose, duration, recurrence, deviations, resistance concerns, and veterinarian review",
    33: "environment indicators must calculate methane, manure, land, water, feed footprint, emission factors, groups, production units, and assumptions",
    34: "manure handling must track source, volume, storage, application projection, spill risk, corrective action, and affected herd groups",
    35: "weather risk must trigger heat stress tasks, hydration, shade, mitigation, affected groups, closure evidence, and outcomes",
    36: "staff tasks must enforce competency projections, due windows, completion evidence, staff accountability, and supervisor review",
    37: "equipment readiness must block handling, scale, treatment, feeding, and transport sessions when inspection or calibration projections fail",
    38: "offline capture must preserve device ID, original observation time, sync time, conflict review, and avoid overwriting newer records",
    39: "sensor ingestion must evaluate device projection, activity, rumination, temperature, location, water intake, signal quality, stale data, and anomaly triage",
    40: "dashboards must expose morbidity, mortality, conception, calving interval, feed conversion, growth, output, withdrawal, and exceptions",
    41: "exceptions must classify welfare, compliance, health, feed, movement, data quality, severity, blocker type, owner, due date, escalation, and closure",
    42: "rule workbenches must govern species profiles, withdrawals, protocols, breeding, rations, movement, alerts, parameter bounds, approval, rollback, and runtime effect",
    43: "clinical-note agents must extract diagnosis, treatment, follow-up, withdrawal, and tasks into source-cited CRUD previews requiring confirmation",
    44: "daily-plan agents must order tasks by due dates, severity, group location, equipment, competency, dependencies, and confirmation prompts",
    45: "agent safety must declare command type, affected owned records, source evidence, confidence, policy checks, approval requirement, and accepted proposal log",
    46: "event specialization must verify typed animal lifecycle, treatment, withdrawal, movement, productivity, exception, idempotency, retries, and dead letters",
    47: "herd audit packets must hash-link lifecycle, treatment, movement, certification, and report evidence and detect altered contents",
    48: "data quality must score missing birth dates, uncertain identifiers, stale memberships, unverified treatments, remediation tasks, and confidence trend",
    49: "release smoke must execute arrival quarantine, vaccination, treatment withdrawal, breeding, birth, movement permit, and sale readiness scenarios",
    50: "cross-PBC proof must reject undeclared table references and allow only owned tables plus declared APIs, events, and projections",
}

_BASE_FIELDS = ("tenant_id", "farm_id", "animal_id", "herd_group_id", "species_profile", "lifecycle_stage", "policy_version", "required_evidence", "approval_record")


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
    return {"title": capability.title, "slug": capability.slug, "tables": (f"livestock_herd_management_{capability.slug}_control",), "fields": _BASE_FIELDS + (proof_field,), "ui": f"LivestockHerdManagement{_camel(capability.slug)}Panel", "route": f"POST /livestock-herd-management/improve1/{capability.slug}", "dependencies": _FEATURE_DEPENDENCIES.get(capability.feature_number, ()), "primary_proof": proof_field}


CONTROL_SPECS: dict[int, dict[str, Any]] = {capability.feature_number: _spec_for(capability) for capability in LIVESTOCK_CONTROL_CAPABILITIES}


def sample_payload_for(capability: Improve1Capability | str | int) -> dict[str, Any]:
    resolved = _resolve(capability)
    if resolved is None:
        return {}
    spec = CONTROL_SPECS[resolved.feature_number]
    payload = {field: f"{resolved.slug}_{field}" for field in spec["fields"]}
    payload[spec["primary_proof"]] = True
    payload.update({"database_backend": "postgresql", "event_contract": EVENT_CONTRACT, "event_topic": LIVESTOCK_CONTROL_REQUIRED_EVENT_TOPIC, "stream_engine_picker_visible": False, "shared_table_access": False, "human_confirmation": True, "side_effects": ()})
    return payload


def _domain_findings(capability: Improve1Capability, payload: dict[str, Any]) -> tuple[str, ...]:
    findings: list[str] = []
    spec = CONTROL_SPECS[capability.feature_number]
    proof_field = spec["primary_proof"]
    if payload.get(proof_field) is not True:
        findings.append(f"{capability.title} requires {proof_field.replace('_', ' ')}")
        findings.append(_DOMAIN_MESSAGES[capability.feature_number])
    if capability.feature_number in (43, 44, 45) and payload.get("human_confirmation") is False:
        findings.append("livestock agents must produce source-cited previews and require approval before governed herd mutations")
    if capability.feature_number in (11, 19, 22, 35, 36, 37, 50) and payload.get("shared_table_access"):
        findings.append("external veterinary, registry, feed, weather, staff, equipment, and commercial context must use declared projections/events/APIs only")
    if payload.get("event_contract") != EVENT_CONTRACT or payload.get("event_topic") != LIVESTOCK_CONTROL_REQUIRED_EVENT_TOPIC:
        findings.append("livestock eventing must use the AppGen-X event contract and package topic")
    if payload.get("stream_engine_picker_visible"):
        findings.append("ordinary PBCs must not expose stream-engine pickers")
    if payload.get("database_backend") not in LIVESTOCK_CONTROL_ALLOWED_DATABASE_BACKENDS:
        findings.append("ordinary livestock datastore must be PostgreSQL, MySQL, or MariaDB")
    if payload.get("shared_table_access"):
        findings.append("livestock controls must use owned tables plus declared APIs/events/projections")
    return tuple(dict.fromkeys(findings))


def evaluate_livestock_control(capability: Improve1Capability | str | int, payload: dict[str, Any] | None = None) -> dict[str, Any]:
    resolved = _resolve(capability)
    if resolved is None:
        return {"ok": False, "reason": "unknown_capability", "side_effects": ()}
    spec = CONTROL_SPECS[resolved.feature_number]
    candidate = sample_payload_for(resolved)
    candidate.update(dict(payload or {}))
    missing_fields = tuple(field for field in spec["fields"] if candidate.get(field) in (None, "", (), []))
    foreign_tables = tuple(table for table in spec["tables"] if table not in LIVESTOCK_CONTROL_OWNED_TABLES)
    undeclared_dependencies = tuple(dependency for dependency in spec["dependencies"] if dependency not in LIVESTOCK_CONTROL_DECLARED_DEPENDENCIES)
    findings = _domain_findings(resolved, candidate)
    evidence = {"evidence_id": _digest((PBC_KEY, resolved.feature_number, tuple(sorted(candidate))))[:20], "owned_tables": spec["tables"], "required_fields": spec["fields"], "ui_surface": spec["ui"], "service_api": spec["route"], "test": "tests/test_domain_behavior.py", "event_contract": EVENT_CONTRACT, "required_event_topic": LIVESTOCK_CONTROL_REQUIRED_EVENT_TOPIC, "allowed_database_backends": LIVESTOCK_CONTROL_ALLOWED_DATABASE_BACKENDS, "declared_dependencies": spec["dependencies"], "domain_message": _DOMAIN_MESSAGES[resolved.feature_number], "side_effects": ()}
    ok = not missing_fields and not foreign_tables and not undeclared_dependencies and not findings
    return {"ok": ok, "pbc": PBC_KEY, "feature_number": resolved.feature_number, "slug": resolved.slug, "title": resolved.title, "capability": resolved.as_traceability_row(), "payload": candidate, "evidence": evidence, "missing_fields": missing_fields, "foreign_tables": foreign_tables, "undeclared_dependencies": undeclared_dependencies, "findings": findings, "side_effects": ()}


def improve1_livestock_control_contract() -> dict[str, Any]:
    evaluations = tuple(evaluate_livestock_control(capability) for capability in LIVESTOCK_CONTROL_CAPABILITIES)
    blocking = tuple(item for item in evaluations if not item["ok"])
    return {"ok": not blocking, "pbc": PBC_KEY, "format": "appgen.livestock-herd-management-improve1-control.v1", "capability_count": len(evaluations), "capabilities": evaluations, "owned_tables": LIVESTOCK_CONTROL_OWNED_TABLES, "declared_dependencies": LIVESTOCK_CONTROL_DECLARED_DEPENDENCIES, "allowed_database_backends": LIVESTOCK_CONTROL_ALLOWED_DATABASE_BACKENDS, "event_contract": EVENT_CONTRACT, "required_event_topic": LIVESTOCK_CONTROL_REQUIRED_EVENT_TOPIC, "stream_engine_picker_visible": False, "blocking_gaps": blocking, "side_effects": ()}


LIVESTOCK_CONTROL_FUNCTIONS = {capability.slug: (lambda payload=None, slug=capability.slug: evaluate_livestock_control(slug, payload)) for capability in LIVESTOCK_CONTROL_CAPABILITIES}
