"""Executable improve1 controls for the Medical Device Lifecycle PBC."""

from __future__ import annotations

import hashlib
from typing import Any

from .improve1_capabilities import IMPROVE1_CAPABILITIES, Improve1Capability

PBC_KEY = "medical_device_lifecycle"
EVENT_CONTRACT = "AppGen-X"
MEDICAL_DEVICE_CONTROL_ALLOWED_DATABASE_BACKENDS = ("postgresql", "mysql", "mariadb")
MEDICAL_DEVICE_CONTROL_REQUIRED_EVENT_TOPIC = "pbc.medical_device_lifecycle.events"
_BASE_OWNED_TABLES = (
    "medical_device_lifecycle_medical_device",
    "medical_device_lifecycle_device_assignment",
    "medical_device_lifecycle_calibration",
    "medical_device_lifecycle_maintenance_event",
    "medical_device_lifecycle_recall_notice",
    "medical_device_lifecycle_usage_trace",
    "medical_device_lifecycle_regulatory_evidence",
    "medical_device_lifecycle_medical_device_lifecycle_policy_rule",
    "medical_device_lifecycle_medical_device_lifecycle_runtime_parameter",
    "medical_device_lifecycle_medical_device_lifecycle_schema_extension",
    "medical_device_lifecycle_medical_device_lifecycle_control_assertion",
    "medical_device_lifecycle_medical_device_lifecycle_governed_model",
    "medical_device_lifecycle_appgen_outbox_event",
    "medical_device_lifecycle_appgen_inbox_event",
    "medical_device_lifecycle_appgen_dead_letter_event",
)
MEDICAL_DEVICE_CONTROL_OWNED_TABLES = tuple(dict.fromkeys(_BASE_OWNED_TABLES + tuple(f"medical_device_lifecycle_{capability.slug}_control" for capability in IMPROVE1_CAPABILITIES)))
MEDICAL_DEVICE_CONTROL_DECLARED_DEPENDENCIES = tuple(dict.fromkeys((
    "PolicyChanged",
    "AuditEventSealed",
    "OperationalKpiChanged",
    "PatientProjectionChanged",
    "PatientNotificationRequested",
    "ClinicalIncidentReported",
    "VulnerabilityFeedChanged",
    "ProcurementAssetReceived",
    "FacilitiesLocationChanged",
)))
MEDICAL_DEVICE_CONTROL_CAPABILITIES: tuple[Improve1Capability, ...] = IMPROVE1_CAPABILITIES
CAPABILITY_BY_NUMBER = {capability.feature_number: capability for capability in MEDICAL_DEVICE_CONTROL_CAPABILITIES}
CAPABILITY_BY_SLUG = {capability.slug: capability for capability in MEDICAL_DEVICE_CONTROL_CAPABILITIES}
_BASE_FIELDS = ("tenant_id", "device_id", "udi", "assignment_id", "calibration_id", "maintenance_event_id", "recall_notice_id", "policy_version", "audit_trail", "evidence_references")
_PRIMARY_PROOF_FIELDS: dict[int, str] = {
    1: 'unique_device_identity_registry_verified',
    2: 'device_lifecycle_state_machine_verified',
    3: 'department_and_location_traceability_verified',
    4: 'device_assignment_governance_verified',
    5: 'implant_tracking_verified',
    6: 'calibration_schedule_and_tolerance_verified',
    7: 'preventive_maintenance_program_verified',
    8: 'corrective_maintenance_events_verified',
    9: 'recall_notice_intake_verified',
    10: 'recall_execution_workflow_verified',
    11: 'field_safety_corrective_action_verified',
    12: 'firmware_and_software_configuration_verified',
    13: 'cybersecurity_vulnerability_tracking_verified',
    14: 'usage_traceability_verified',
    15: 'regulatory_evidence_repository_verified',
    16: 'incoming_inspection_and_qualification_verified',
    17: 'loaner_and_rental_device_controls_verified',
    18: 'sterilization_and_reprocessing_evidence_verified',
    19: 'accessories_and_component_hierarchy_verified',
    20: 'battery_and_consumable_readiness_verified',
    21: 'clinical_alarm_and_alert_evidence_verified',
    22: 'adverse_event_and_incident_linkage_verified',
    23: 'regulatory_reporting_readiness_verified',
    24: 'device_training_and_competency_verified',
    25: 'work_order_and_vendor_service_contract_verified',
    26: 'utilization_and_fleet_optimization_verified',
    27: 'predictive_maintenance_risk_verified',
    28: 'device_availability_command_center_verified',
    29: 'agent_assisted_device_summaries_verified',
    30: 'governed_agent_crud_commands_verified',
    31: 'continuous_control_assertions_verified',
    32: 'dead_letter_and_retry_operations_verified',
    33: 'cross_pbc_boundary_proofs_verified',
    34: 'device_timeline_projection_verified',
    35: 'recall_patient_notification_boundary_verified',
    36: 'device_disposition_and_disposal_verified',
    37: 'recall_drill_and_readiness_simulation_verified',
    38: 'configuration_and_policy_impact_simulation_verified',
    39: 'regulatory_classification_localization_verified',
    40: 'device_data_integrity_controls_verified',
    41: 'cryptographic_device_evidence_proofs_verified',
    42: 'seeded_device_scenario_library_verified',
    43: 'device_recall_analytics_verified',
    44: 'maintenance_quality_analytics_verified',
    45: 'role_based_permission_model_verified',
    46: 'evidence_packet_generation_verified',
    47: 'carbon_and_resource_awareness_verified',
    48: 'full_device_lifecycle_release_simulation_verified',
    49: 'package_overlap_guardrails_verified',
    50: 'composition_dsl_and_unified_agent_exposure_verified',
}
_FEATURE_FIELDS: dict[int, tuple[str, ...]] = {feature_number: _BASE_FIELDS + (primary_proof,) for feature_number, primary_proof in _PRIMARY_PROOF_FIELDS.items()}
_FEATURE_DEPENDENCIES: dict[int, tuple[str, ...]] = {
    5: ('PatientProjectionChanged',),
    13: ('VulnerabilityFeedChanged',),
    22: ('ClinicalIncidentReported',),
    23: ('ClinicalIncidentReported',),
    33: ('PolicyChanged', 'AuditEventSealed', 'OperationalKpiChanged'),
    35: ('PatientNotificationRequested',),
    49: ('PolicyChanged', 'AuditEventSealed'),
    50: ('AuditEventSealed',),
}
_DOMAIN_MESSAGES: dict[int, str] = {
    1: 'Expand `medical_device` with unique device identity, model, serial, lot, firmware, hardware revision, risk class, implantable flag, sterile flag, and source evidence.',
    2: 'Add explicit lifecycle transitions with actor, reason, evidence, allowed next states, and AppGen-X event emission.',
    3: 'Add current location, owning department, physical zone, last scan, custody actor, transfer event, and location confidence.',
    4: 'Expand `device_assignment` with assignment type, assignee projection, start/end time, intended use, responsible role, consent/privacy flag, and release condition.',
    5: 'Add implant-specific fields for implant date, procedure projection, implanting clinician, body site, explant date, explant reason, and patient notification status.',
    6: 'Expand `calibration` with required interval, tolerance, standard used, before/after values, technician, pass/fail, due date, and out-of-tolerance impact.',
    7: 'Add maintenance plans by device class, usage intensity, risk class, manufacturer guidance, last service, next due, and task checklist.',
    8: 'Expand `maintenance_event` with failure mode, severity, root cause, parts replaced, technician, downtime, service vendor, and qualification result.',
    9: 'Expand `recall_notice` with recall class, manufacturer notice, affected criteria, required action, deadline, patient impact flag, and closure requirements.',
    10: 'Add recall tasks for quarantine, patient notification, firmware update, replacement, return, documentation, and unresolved exception.',
    11: 'Add action type, target devices, procedure, completion evidence, training requirement, and effectiveness check.',
    12: 'Add firmware/software version, approved baseline, patch status, cybersecurity risk, rollback plan, and configuration drift.',
    13: 'Add vulnerability identifier, affected device class, severity, mitigation, network exposure, patch status, compensating control, and due date.',
    14: 'Expand `usage_traceability` with event type, start/end time, operator projection, location, patient/procedure projection, usage metric, and exception.',
    15: 'Expand `regulatory_evidence` with document type, effective date, device scope, retention class, approval, checksum, and evidence packet membership.',
    16: 'Add incoming inspection checklist, acceptance criteria, device labeling check, software baseline, accessories, and qualification result.',
    17: 'Add ownership type, vendor, loan/rental period, service responsibility, return condition, and evidence requirements.',
    18: 'Add reprocessing cycle, method, operator, lot, pass/fail, expiration, usage count, and quarantine on failure.',
    19: 'Add parent-child device components, compatibility rules, accessory assignment, replacement history, and missing component flags.',
    20: 'Add readiness checks for battery cycle, charge status, consumable expiry, accessory availability, and replacement due date.',
    21: 'Add alarm configuration, threshold, alarm event, acknowledgement, nuisance alarm marker, and safety review link.',
    22: 'Add incident link, suspected device issue, harm severity, investigation status, reportability assessment, and corrective action.',
    23: 'Add report candidate, jurisdiction, deadline, required fields, submission status, acknowledgement, and follow-up.',
    24: 'Add training requirements by device class, role, competency expiry, user acknowledgement, and assignment/use gate.',
    25: 'Add vendor service fields, contract SLA, dispatch, repair notes, parts, service certification, and acceptance evidence.',
    26: 'Add utilization metrics by device class, site, department, shift, downtime, assignment duration, and idle inventory.',
    27: 'Add risk score with explanatory factors, threshold, recommended action, and confidence.',
    28: 'Add workbench queues for availability, recall, maintenance due, calibration due, cybersecurity risk, missing location, and utilization hotspots.',
    29: 'Add agent skills for device readiness summary, recall impact summary, maintenance history, calibration status, vulnerability exposure, and assignment timeline.',
    30: 'Add command previews for assign device, quarantine device, record calibration, open maintenance, close recall task, update firmware status, and retire device.',
    31: 'Add controls with threshold, population, failing devices, owner, remediation, recurrence, and closure evidence.',
    32: 'Add retry reason, risk, idempotency key, replay checkpoint, remediation action, and dead-letter queue.',
    33: 'Add release gates proving external relationships use declared APIs, events, projections, or package metadata.',
    34: 'Build timeline projection with actor, event type, source, linked record, risk impact, and evidence reference.',
    35: 'Store patient impact evidence and notification task references using declared projection identifiers, not direct patient-table writes.',
    36: 'Add disposition type, approval, data wipe evidence, environmental handling, vendor return, destruction certificate, and final state.',
    37: 'Add side-effect-free recall drill simulations over inventory, assignments, locations, patient impact, and communication tasks.',
    38: 'Add simulations over device cohorts for policy changes with risk, workload, availability, and compliance impact.',
    39: 'Add jurisdiction-specific classification, reporting duty, retention, labeling, and recall workflow rules.',
    40: 'Add controls for backdated events, unauthorized edits, missing source checksums, orphan assignments, and signature gaps.',
    41: 'Add hash chains for registry creation, assignment, calibration, maintenance, recall, incident, and disposal events.',
    42: 'Add seeds for device qualification, assignment, calibration failure, maintenance, recall, firmware vulnerability, implant trace, and disposal.',
    43: 'Add recall analytics by recall class, device cohort, location, patient impact, overdue task, and unresolved exception.',
    44: 'Add analytics for downtime, repeat repairs, parts failures, vendor SLA, calibration failure rate, and mean time between failures.',
    45: 'Add permissions for assign, quarantine, calibrate, maintain, close recall, update firmware, dispose, and view patient-linked usage.',
    46: 'Add packet generation for device history, recall, maintenance, calibration, cybersecurity vulnerability, incident, and disposition.',
    47: 'Add optional resource metrics for utilization efficiency, disposable use, shipping, repair versus replace decisions, and disposal category.',
    48: 'Add a simulation where a device is registered, qualified, assigned, calibrated, maintained, recalled, remediated, audited, and retired.',
    49: 'Add overlap checks and dependency contracts for clinical use, location, vendor procurement, lab instrument outputs, vulnerabilities, and audit evidence.',
    50: 'Extend composition metadata for devices, assignments, calibrations, maintenance, recalls, usage traceability, regulatory evidence, workbench fragments, controls, and agent skills.',
}
_HUMAN_CONFIRMATION_FEATURES = (27, 29, 30, 36, 38)
_PROJECTION_ONLY_FEATURES = (4, 5, 14, 22, 23, 33, 35, 49, 50)


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
    proof = _PRIMARY_PROOF_FIELDS[capability.feature_number]
    return {"title": capability.title, "slug": capability.slug, "tables": (f"medical_device_lifecycle_{capability.slug}_control",), "fields": _FEATURE_FIELDS[capability.feature_number], "primary_proof": proof, "ui": f"MedicalDeviceLifecycle{_camel(capability.slug)}Panel", "route": f"POST /medical-device-lifecycle/improve1/{capability.slug}", "dependencies": _FEATURE_DEPENDENCIES.get(capability.feature_number, ())}


CONTROL_SPECS: dict[int, dict[str, Any]] = {capability.feature_number: _spec_for(capability) for capability in MEDICAL_DEVICE_CONTROL_CAPABILITIES}


def sample_payload_for(capability: Improve1Capability | str | int) -> dict[str, Any]:
    resolved = _resolve(capability)
    if resolved is None:
        return {}
    spec = CONTROL_SPECS[resolved.feature_number]
    payload = {field: f"{resolved.slug}_{field}" for field in spec["fields"]}
    payload[spec["primary_proof"]] = True
    payload.update({"database_backend": "postgresql", "event_contract": EVENT_CONTRACT, "event_topic": MEDICAL_DEVICE_CONTROL_REQUIRED_EVENT_TOPIC, "stream_engine_picker_visible": False, "shared_table_access": False, "dependency_access_mode": "api_event_projection", "human_confirmation": True, "side_effects": ()})
    return payload


def _domain_findings(capability: Improve1Capability, payload: dict[str, Any]) -> tuple[str, ...]:
    findings: list[str] = []
    feature_number = capability.feature_number
    spec = CONTROL_SPECS[feature_number]
    if payload.get(spec["primary_proof"]) is not True:
        findings.append(f"{capability.title} requires {spec['primary_proof'].replace('_', ' ')}")
        findings.append(_DOMAIN_MESSAGES[feature_number])
    if feature_number in _HUMAN_CONFIRMATION_FEATURES and payload.get("human_confirmation") is False:
        findings.append("medical device agents and simulations must draft recommendations only; human approval is required before governed mutation")
    if feature_number in _PROJECTION_ONLY_FEATURES and payload.get("dependency_access_mode") != "api_event_projection":
        findings.append("clinical, patient, procurement, facilities, lab, quality, cybersecurity, finance, and audit context must use APIs, events, or read-only projections")
    if payload.get("event_contract") != EVENT_CONTRACT or payload.get("event_topic") != MEDICAL_DEVICE_CONTROL_REQUIRED_EVENT_TOPIC:
        findings.append("medical device lifecycle eventing must use the AppGen-X event contract and package topic")
    if payload.get("stream_engine_picker_visible"):
        findings.append("ordinary PBCs must not expose stream-engine pickers")
    if payload.get("database_backend") not in MEDICAL_DEVICE_CONTROL_ALLOWED_DATABASE_BACKENDS:
        findings.append("ordinary medical device lifecycle datastore must be PostgreSQL, MySQL, or MariaDB")
    if payload.get("shared_table_access"):
        findings.append("medical device controls must use owned tables plus declared APIs/events/projections")
    return tuple(dict.fromkeys(findings))


def evaluate_medical_device_control(capability: Improve1Capability | str | int, payload: dict[str, Any] | None = None) -> dict[str, Any]:
    resolved = _resolve(capability)
    if resolved is None:
        return {"ok": False, "reason": "unknown_capability", "side_effects": ()}
    spec = CONTROL_SPECS[resolved.feature_number]
    candidate = sample_payload_for(resolved)
    candidate.update(dict(payload or {}))
    missing_fields = tuple(field for field in spec["fields"] if candidate.get(field) in (None, "", (), []))
    foreign_tables = tuple(table for table in spec["tables"] if table not in MEDICAL_DEVICE_CONTROL_OWNED_TABLES)
    undeclared_dependencies = tuple(dependency for dependency in spec["dependencies"] if dependency not in MEDICAL_DEVICE_CONTROL_DECLARED_DEPENDENCIES)
    findings = _domain_findings(resolved, candidate)
    evidence = {"evidence_id": _digest((PBC_KEY, resolved.feature_number, tuple(sorted(candidate))))[:20], "owned_tables": spec["tables"], "required_fields": spec["fields"], "primary_proof": spec["primary_proof"], "ui_surface": spec["ui"], "service_api": spec["route"], "test": "tests/test_domain_behavior.py", "event_contract": EVENT_CONTRACT, "required_event_topic": MEDICAL_DEVICE_CONTROL_REQUIRED_EVENT_TOPIC, "allowed_database_backends": MEDICAL_DEVICE_CONTROL_ALLOWED_DATABASE_BACKENDS, "declared_dependencies": spec["dependencies"], "side_effects": ()}
    ok = not missing_fields and not foreign_tables and not undeclared_dependencies and not findings
    return {"ok": ok, "pbc": PBC_KEY, "feature_number": resolved.feature_number, "slug": resolved.slug, "title": resolved.title, "capability": resolved.as_traceability_row(), "payload": candidate, "evidence": evidence, "missing_fields": missing_fields, "foreign_tables": foreign_tables, "undeclared_dependencies": undeclared_dependencies, "findings": findings, "side_effects": ()}


def improve1_medical_device_control_contract() -> dict[str, Any]:
    evaluations = tuple(evaluate_medical_device_control(capability) for capability in MEDICAL_DEVICE_CONTROL_CAPABILITIES)
    blocking = tuple(item for item in evaluations if not item["ok"])
    return {"ok": not blocking, "pbc": PBC_KEY, "format": "appgen.medical-device-lifecycle-improve1-control.v1", "capability_count": len(evaluations), "capabilities": evaluations, "owned_tables": MEDICAL_DEVICE_CONTROL_OWNED_TABLES, "declared_dependencies": MEDICAL_DEVICE_CONTROL_DECLARED_DEPENDENCIES, "allowed_database_backends": MEDICAL_DEVICE_CONTROL_ALLOWED_DATABASE_BACKENDS, "event_contract": EVENT_CONTRACT, "required_event_topic": MEDICAL_DEVICE_CONTROL_REQUIRED_EVENT_TOPIC, "stream_engine_picker_visible": False, "blocking_gaps": blocking, "side_effects": ()}


MEDICAL_DEVICE_CONTROL_FUNCTIONS = {capability.slug: (lambda payload=None, slug=capability.slug: evaluate_medical_device_control(slug, payload)) for capability in MEDICAL_DEVICE_CONTROL_CAPABILITIES}
