"""Executable runtime contract for the permitting_licensing_inspections PBC."""
from __future__ import annotations

from copy import deepcopy
import hashlib

from .domain_depth import (
    DOMAIN_ADVANCED_CAPABILITIES,
    DOMAIN_OPERATIONS,
    DOMAIN_OWNED_TABLES,
    domain_depth_contract,
    domain_depth_smoke_test,
    execute_domain_operation,
)

PBC_KEY = "permitting_licensing_inspections"
PERMITTING_LICENSING_INSPECTIONS_OWNED_TABLES = DOMAIN_OWNED_TABLES
PERMITTING_LICENSING_INSPECTIONS_RUNTIME_TABLES = PERMITTING_LICENSING_INSPECTIONS_OWNED_TABLES
PERMITTING_LICENSING_INSPECTIONS_BUSINESS_TABLES = PERMITTING_LICENSING_INSPECTIONS_OWNED_TABLES[:12]
PERMITTING_LICENSING_INSPECTIONS_ALLOWED_DATABASE_BACKENDS = ("postgresql", "mysql", "mariadb")
PERMITTING_LICENSING_INSPECTIONS_REQUIRED_EVENT_TOPIC = "pbc.permitting_licensing_inspections.events"
PERMITTING_LICENSING_INSPECTIONS_EMITTED_EVENT_TYPES = (
    "PermittingLicensingInspectionsCreated",
    "PermittingLicensingInspectionsUpdated",
    "PermittingLicensingInspectionsApproved",
    "PermittingLicensingInspectionsExceptionOpened",
)
PERMITTING_LICENSING_INSPECTIONS_CONSUMED_EVENT_TYPES = (
    "PolicyChanged",
    "CustomerUpdated",
    "SupplierQualified",
)
PERMITTING_LICENSING_INSPECTIONS_STANDARD_FEATURE_KEYS = (
    "application_management",
    "permitting_licensing_inspections_workflow",
    "permitting_licensing_inspections_analytics",
    "configuration_schema",
    "rule_engine",
    "parameter_engine",
    "owned_schema_migrations_models",
    "appgen_x_outbox_inbox_eventing",
    "idempotent_handlers",
    "retry_dead_letter_evidence",
    "permissions",
    "seed_data",
    "workbench",
    "agentic_document_instruction_intake",
    "governed_datastore_crud",
    "ai_agent_task_assistance",
    "configuration_workbench",
    "continuous_release_assurance",
    "single_pbc_domain_usability",
    "forms_wizards_controls",
)
PERMITTING_LICENSING_INSPECTIONS_RUNTIME_CAPABILITY_KEYS = (
    "permitting_licensing_inspections_event_sourced_operational_history",
    "permitting_licensing_inspections_multi_tenant_policy_isolation",
    "permitting_licensing_inspections_schema_evolution_resilience",
    "permitting_licensing_inspections_autonomous_anomaly_detection",
    "permitting_licensing_inspections_semantic_document_instruction_understanding",
    "permitting_licensing_inspections_predictive_risk_scoring",
    "permitting_licensing_inspections_counterfactual_scenario_simulation",
    "permitting_licensing_inspections_cryptographic_audit_proofs",
    "permitting_licensing_inspections_continuous_control_testing",
    "permitting_licensing_inspections_carbon_and_sustainability_awareness",
    "permitting_licensing_inspections_cross_pbc_event_federation",
    "permitting_licensing_inspections_governed_ai_agent_execution",
    "permitting_licensing_inspections_single_pbc_app_shell",
)
PERMITTING_LICENSING_INSPECTIONS_UI_FRAGMENT_KEYS = (
    "PermittingLicensingInspectionsWorkbench",
    "PermittingLicensingInspectionsDetail",
    "PermittingLicensingInspectionsAssistantPanel",
    "PermittingLicensingInspectionsReleaseScorecard",
)
PERMITTING_LICENSING_INSPECTIONS_FORM_KEYS = (
    "pre_application_consultation_form",
    "permit_application_intake_form",
    "plan_resubmittal_form",
    "inspection_scheduling_form",
    "renewal_eligibility_review_form",
)
PERMITTING_LICENSING_INSPECTIONS_WIZARD_KEYS = (
    "entitlement_intake_wizard",
    "plan_review_resubmittal_wizard",
    "field_enforcement_resolution_wizard",
)
PERMITTING_LICENSING_INSPECTIONS_CONTROL_KEYS = (
    "submission_completeness_checklist_control",
    "plan_set_version_timeline_control",
    "discipline_review_matrix_control",
    "issuance_payment_gate_control",
    "notice_and_compliance_timeline_control",
)
PERMITTING_LICENSING_INSPECTIONS_ROUTE_DEFINITIONS = (
    ("POST /applications", "command_application"),
    ("POST /permits", "record_permit"),
    ("POST /licenses", "review_license"),
    ("POST /review-tasks", "approve_review_task"),
    ("POST /fee-assessments", "simulate_fee_assessment"),
    ("GET /permitting-licensing-inspections-workbench", "query_workbench"),
)
PERMITTING_LICENSING_INSPECTIONS_ENTITY_TABLE_MAP = {
    "application": PERMITTING_LICENSING_INSPECTIONS_BUSINESS_TABLES[0],
    "permit": PERMITTING_LICENSING_INSPECTIONS_BUSINESS_TABLES[1],
    "license": PERMITTING_LICENSING_INSPECTIONS_BUSINESS_TABLES[2],
    "review_task": PERMITTING_LICENSING_INSPECTIONS_BUSINESS_TABLES[3],
    "fee_assessment": PERMITTING_LICENSING_INSPECTIONS_BUSINESS_TABLES[4],
    "inspection": PERMITTING_LICENSING_INSPECTIONS_BUSINESS_TABLES[5],
    "violation": PERMITTING_LICENSING_INSPECTIONS_BUSINESS_TABLES[6],
    "policy_rule": PERMITTING_LICENSING_INSPECTIONS_BUSINESS_TABLES[7],
    "runtime_parameter": PERMITTING_LICENSING_INSPECTIONS_BUSINESS_TABLES[8],
    "schema_extension": PERMITTING_LICENSING_INSPECTIONS_BUSINESS_TABLES[9],
    "control_assertion": PERMITTING_LICENSING_INSPECTIONS_BUSINESS_TABLES[10],
    "governed_model": PERMITTING_LICENSING_INSPECTIONS_BUSINESS_TABLES[11],
}
DEFAULT_CONFIGURATION = {
    "database_backend": "postgresql",
    "event_topic": PERMITTING_LICENSING_INSPECTIONS_REQUIRED_EVENT_TOPIC,
    "default_policy": "jurisdiction_governed_review",
    "retry_limit": 5,
    "event_contract": "AppGen-X",
    "stream_engine_picker_visible": False,
    "shared_table_access": False,
    "citizen_portal_enabled": True,
}
DEFAULT_PARAMETERS = {
    "submission_completeness_floor": 0.9,
    "correction_response_sla_days": 10,
    "inspection_sla_hours": 48,
    "reinspection_fee_amount": 125.0,
    "renewal_notice_days": 60,
    "grace_period_days": 30,
    "workbench_limit": 25,
}
DEFAULT_RULES = {
    "intake_completeness_policy": {
        "rule_id": "intake_completeness_policy",
        "description": "Applications cannot enter active review until documents, attestations, and responsible parties are complete.",
        "required_by_type": {
            "building_permit": ("site_plan", "architectural_drawings", "owner_authorization"),
            "business_license": ("business_registration", "tax_clearance", "owner_authorization"),
            "renewal": ("renewal_attestation", "fee_statement"),
        },
    },
    "plan_set_version_policy": {
        "rule_id": "plan_set_version_policy",
        "description": "Review comments and approvals bind to a specific plan-set version.",
        "required_fields": ("version_label", "revision_date", "sheet_inventory"),
    },
    "correction_cycle_policy": {
        "rule_id": "correction_cycle_policy",
        "description": "Correction rounds must preserve reviewer comments, applicant responses, and acceptance state.",
    },
    "issuance_payment_policy": {
        "rule_id": "issuance_payment_policy",
        "description": "Permits cannot be issued without payment confirmation or an override reason.",
    },
    "inspection_escalation_policy": {
        "rule_id": "inspection_escalation_policy",
        "description": "Failed inspections and safety findings can escalate to reinspection fees or violations.",
    },
    "renewal_eligibility_policy": {
        "rule_id": "renewal_eligibility_policy",
        "description": "Renewals evaluate active violations, failed inspections, attestations, and payment status.",
    },
    "due_process_notice_policy": {
        "rule_id": "due_process_notice_policy",
        "description": "Violation notices track service, cure deadlines, extensions, and next legally allowed steps.",
    },
}


def permitting_licensing_inspections_empty_state():
    return {
        "records": {
            "consultations": {},
            "applications": {},
            "plan_sets": {},
            "review_tasks": {},
            "fee_assessments": {},
            "permits": {},
            "licenses": {},
            "inspections": {},
            "violations": {},
            "renewal_decisions": {},
            "notices": {},
            "hearing_dockets": {},
        },
        "parameters": deepcopy(DEFAULT_PARAMETERS),
        "rules": deepcopy(DEFAULT_RULES),
        "schema_extensions": {},
        "configuration": deepcopy(DEFAULT_CONFIGURATION),
        "inbox": [],
        "outbox": [],
        "dead_letter": [],
        "idempotency_keys": set(),
        "audit_history": [],
    }


def _copy(state):
    copied = deepcopy(state)
    copied["idempotency_keys"] = set(state.get("idempotency_keys", set()))
    return copied


def _digest(value):
    return hashlib.sha256(repr(value).encode("utf-8")).hexdigest()


def _event(state, event_type, payload, *, object_type=None, object_id=None, severity="info"):
    state["outbox"].append(
        {
            "event_id": _digest((event_type, object_type, object_id, payload, len(state["outbox"]))),
            "event_type": event_type,
            "topic": PERMITTING_LICENSING_INSPECTIONS_REQUIRED_EVENT_TOPIC,
            "payload": deepcopy(payload),
            "object_type": object_type,
            "object_id": object_id,
            "severity": severity,
            "idempotency_key": _digest((event_type, object_type, object_id, payload)),
        }
    )


def _append_audit(state, action, record_type, record_id, tenant, payload=None):
    state["audit_history"].append(
        {
            "entry_id": _digest((action, record_type, record_id, len(state["audit_history"]))),
            "action": action,
            "record_type": record_type,
            "record_id": record_id,
            "tenant": tenant,
            "payload": deepcopy(payload or {}),
        }
    )


def _bucket(state, name):
    return state["records"][name]


def _store_record(state, bucket_name, record_id, record):
    _bucket(state, bucket_name)[record_id] = deepcopy(record)


def _next_id(prefix, records):
    return f"{prefix}-{len(records) + 1:04d}"


def _required_documents(application_type):
    mapping = {
        "building_permit": ("site_plan", "architectural_drawings", "owner_authorization"),
        "business_license": ("business_registration", "tax_clearance", "owner_authorization"),
        "renewal": ("renewal_attestation", "fee_statement"),
        "complaint_case": ("complaint_statement", "site_address"),
    }
    return mapping.get(application_type, ("application_form", "owner_authorization"))


def _required_attestations(application_type):
    mapping = {
        "building_permit": ("code_compliance", "responsible_designer"),
        "business_license": ("tax_compliance", "zoning_acknowledgement"),
        "renewal": ("continuing_conditions",),
    }
    return mapping.get(application_type, ("submitted_truthfully",))


def _review_tracks(application_type):
    mapping = {
        "building_permit": ("zoning", "structural", "fire", "utilities"),
        "business_license": ("zoning", "health", "fire"),
        "renewal": ("licensing", "enforcement"),
        "complaint_case": ("code_enforcement",),
    }
    return mapping.get(application_type, ("general_review",))


def _application_checklist(payload):
    application_type = payload.get("application_type", "building_permit")
    provided_documents = set(payload.get("documents", ()))
    provided_attestations = set(payload.get("attestations", ()))
    parties = payload.get("responsible_parties", {})
    required_documents = _required_documents(application_type)
    required_attestations = _required_attestations(application_type)
    missing_documents = tuple(doc for doc in required_documents if doc not in provided_documents)
    missing_attestations = tuple(att for att in required_attestations if att not in provided_attestations)
    missing_parties = tuple(
        role
        for role in ("applicant", "owner")
        if not parties.get(role)
    )
    parcel_complete = bool(payload.get("parcel_id") or payload.get("site_address"))
    ready_for_review = not missing_documents and not missing_attestations and not missing_parties and parcel_complete
    total_checks = len(required_documents) + len(required_attestations) + 3
    passed_checks = total_checks - len(missing_documents) - len(missing_attestations) - len(missing_parties) - (0 if parcel_complete else 1)
    completeness_score = round(passed_checks / max(1, total_checks), 3)
    return {
        "application_type": application_type,
        "required_documents": required_documents,
        "missing_documents": missing_documents,
        "required_attestations": required_attestations,
        "missing_attestations": missing_attestations,
        "missing_parties": missing_parties,
        "parcel_complete": parcel_complete,
        "completeness_score": completeness_score,
        "ready_for_review": ready_for_review,
        "review_tracks": _review_tracks(application_type),
        "submittal_kind": payload.get("submittal_kind", "new"),
    }


def _fee_line(description, amount, basis):
    return {
        "description": description,
        "amount": round(float(amount), 2),
        "basis": basis,
    }


def permitting_licensing_inspections_configure_runtime(state, config):
    next_state = _copy(state)
    merged = {**DEFAULT_CONFIGURATION, **dict(config)}
    ok = (
        merged.get("database_backend") in PERMITTING_LICENSING_INSPECTIONS_ALLOWED_DATABASE_BACKENDS
        and merged.get("event_topic") == PERMITTING_LICENSING_INSPECTIONS_REQUIRED_EVENT_TOPIC
    )
    next_state["configuration"] = {
        **merged,
        "event_contract": "AppGen-X",
        "stream_engine_picker_visible": False,
        "shared_table_access": False,
    }
    _append_audit(next_state, "configure_runtime", "configuration", PBC_KEY, "system", merged)
    return {
        "ok": ok,
        "state": next_state,
        "configuration": next_state["configuration"],
        "side_effects": (),
    }


def permitting_licensing_inspections_set_parameter(state, name, value):
    next_state = _copy(state)
    next_state["parameters"][name] = value
    parameter = {"name": name, "value": value, "scope": "domain", "bounded": True}
    _append_audit(next_state, "set_parameter", "runtime_parameter", name, "system", parameter)
    return {"ok": True, "state": next_state, "parameter": parameter, "side_effects": ()}


def permitting_licensing_inspections_register_rule(state, rule):
    next_state = _copy(state)
    rule_id = rule.get("rule_id", "domain_rule")
    compiled = {
        **dict(rule),
        "compiled_hash": _digest(rule),
        "event_contract": "AppGen-X",
    }
    next_state["rules"][rule_id] = compiled
    _append_audit(next_state, "register_rule", "policy_rule", rule_id, rule.get("tenant", "system"), compiled)
    return {"ok": True, "state": next_state, "rule": compiled, "side_effects": ()}


def permitting_licensing_inspections_register_schema_extension(state, table, fields):
    next_state = _copy(state)
    owned_name = table if str(table).startswith(f"{PBC_KEY}_") else f"{PBC_KEY}_{table}"
    if owned_name not in PERMITTING_LICENSING_INSPECTIONS_OWNED_TABLES:
        return {
            "ok": False,
            "state": next_state,
            "reason": "unknown_owned_table",
            "side_effects": (),
        }
    next_state["schema_extensions"][owned_name] = dict(fields)
    _append_audit(next_state, "register_schema_extension", "schema_extension", owned_name, "system", dict(fields))
    return {
        "ok": True,
        "state": next_state,
        "table": owned_name,
        "fields": dict(fields),
        "side_effects": (),
    }


def permitting_licensing_inspections_receive_event(state, event):
    next_state = _copy(state)
    idem = event.get("idempotency_key") or event.get("event_id") or _digest(event)
    if idem in next_state["idempotency_keys"]:
        return {"ok": True, "duplicate": True, "state": next_state, "side_effects": ()}
    next_state["idempotency_keys"].add(idem)
    if event.get("event_type") not in PERMITTING_LICENSING_INSPECTIONS_CONSUMED_EVENT_TYPES:
        next_state["dead_letter"].append(
            {
                "event": dict(event),
                "dead_letter_table": f"{PBC_KEY}_appgen_dead_letter_event",
                "retry_policy": {"max_attempts": next_state["configuration"].get("retry_limit", 5)},
            }
        )
        _append_audit(next_state, "dead_letter_event", "event", idem, event.get("tenant", "external"), event)
        return {
            "ok": False,
            "duplicate": False,
            "state": next_state,
            "dead_letter_table": f"{PBC_KEY}_appgen_dead_letter_event",
            "side_effects": (),
        }
    next_state["inbox"].append(dict(event))
    _append_audit(next_state, "receive_event", "event", idem, event.get("tenant", "external"), event)
    return {"ok": True, "duplicate": False, "state": next_state, "side_effects": ()}


def permitting_licensing_inspections_capture_pre_application(state, payload):
    next_state = _copy(state)
    consultations = _bucket(next_state, "consultations")
    consultation_id = payload.get("consultation_id") or _next_id("CONS", consultations)
    record = {
        "consultation_id": consultation_id,
        "tenant": payload.get("tenant", "default"),
        "site_address": payload.get("site_address", "Unspecified site"),
        "parcel_id": payload.get("parcel_id"),
        "advisory_notes": tuple(payload.get("advisory_notes", ())),
        "likely_review_disciplines": tuple(payload.get("likely_review_disciplines", _review_tracks(payload.get("application_type", "building_permit")))),
        "expected_fees": tuple(payload.get("expected_fees", ("application_fee", "inspection_fee"))),
        "public_notice_required": bool(payload.get("public_notice_required", False)),
        "status": payload.get("status", "advisory_open"),
    }
    _store_record(next_state, "consultations", consultation_id, record)
    _event(next_state, PERMITTING_LICENSING_INSPECTIONS_EMITTED_EVENT_TYPES[1], record, object_type="consultation", object_id=consultation_id)
    _append_audit(next_state, "capture_pre_application", "consultation", consultation_id, record["tenant"], record)
    return {"ok": True, "state": next_state, "record": record, "side_effects": ()}


def permitting_licensing_inspections_command_application(state, payload):
    next_state = _copy(state)
    applications = _bucket(next_state, "applications")
    application_id = payload.get("application_id") or payload.get("id") or payload.get("code") or _next_id("APP", applications)
    checklist = _application_checklist(payload)
    record = {
        "application_id": application_id,
        "tenant": payload.get("tenant", "default"),
        "code": payload.get("code", application_id),
        "application_type": checklist["application_type"],
        "submittal_kind": checklist["submittal_kind"],
        "status": "active_review" if checklist["ready_for_review"] else "intake_incomplete",
        "review_stage": "routed" if checklist["ready_for_review"] else "intake",
        "site_address": payload.get("site_address"),
        "parcel_id": payload.get("parcel_id"),
        "responsible_parties": deepcopy(payload.get("responsible_parties", {})),
        "documents": tuple(payload.get("documents", ())),
        "attestations": tuple(payload.get("attestations", ())),
        "consultation_id": payload.get("consultation_id"),
        "plan_set_versions": tuple(),
        "correction_round": 0,
        "completeness": checklist,
    }
    _store_record(next_state, "applications", application_id, record)
    _event(next_state, PERMITTING_LICENSING_INSPECTIONS_EMITTED_EVENT_TYPES[0], record, object_type="application", object_id=application_id)
    _append_audit(next_state, "create_application", "application", application_id, record["tenant"], record)
    return {
        "ok": True,
        "state": next_state,
        "record": record,
        "intake_checklist": checklist,
        "side_effects": (),
    }


def permitting_licensing_inspections_add_plan_set(state, payload):
    next_state = _copy(state)
    application_id = payload["application_id"]
    applications = _bucket(next_state, "applications")
    if application_id not in applications:
        return {"ok": False, "state": next_state, "reason": "unknown_application", "side_effects": ()}
    plan_sets = _bucket(next_state, "plan_sets")
    version_label = payload.get("version_label") or f"v{len(plan_sets) + 1}"
    plan_set_id = payload.get("plan_set_id") or f"{application_id}-{version_label}"
    record = {
        "plan_set_id": plan_set_id,
        "application_id": application_id,
        "tenant": applications[application_id]["tenant"],
        "version_label": version_label,
        "revision_date": payload.get("revision_date", "2026-05-30"),
        "resubmittal_reason": payload.get("resubmittal_reason", "initial"),
        "sheet_inventory": tuple(payload.get("sheet_inventory", ("A001", "C101"))),
        "comparison_notes": tuple(payload.get("comparison_notes", ())),
        "supersedes": payload.get("supersedes"),
    }
    _store_record(next_state, "plan_sets", plan_set_id, record)
    current = dict(applications[application_id])
    current["plan_set_versions"] = tuple(current.get("plan_set_versions", ())) + (plan_set_id,)
    applications[application_id] = current
    _event(next_state, PERMITTING_LICENSING_INSPECTIONS_EMITTED_EVENT_TYPES[1], record, object_type="plan_set", object_id=plan_set_id)
    _append_audit(next_state, "add_plan_set_version", "plan_set", plan_set_id, record["tenant"], record)
    return {"ok": True, "state": next_state, "record": record, "side_effects": ()}


def permitting_licensing_inspections_approve_review_task(state, payload):
    next_state = _copy(state)
    tasks = _bucket(next_state, "review_tasks")
    task_id = payload.get("task_id") or _next_id("REVIEW", tasks)
    dependencies = tuple(payload.get("dependencies", ()))
    blocked = tuple(dep for dep in dependencies if dep not in tasks)
    record = {
        "task_id": task_id,
        "tenant": payload.get("tenant", "default"),
        "application_id": payload.get("application_id"),
        "discipline": payload.get("discipline", "zoning"),
        "status": "blocked" if blocked else payload.get("status", "approved"),
        "dependencies": dependencies,
        "blocked_by": blocked,
        "comment_template": payload.get("comment_template", "standard-plan-review"),
        "plan_set_id": payload.get("plan_set_id"),
        "correction_round": int(payload.get("correction_round", 0)),
    }
    _store_record(next_state, "review_tasks", task_id, record)
    _event(next_state, PERMITTING_LICENSING_INSPECTIONS_EMITTED_EVENT_TYPES[2], record, object_type="review_task", object_id=task_id)
    _append_audit(next_state, "route_discipline_review", "review_task", task_id, record["tenant"], record)
    return {"ok": True, "state": next_state, "record": record, "side_effects": ()}


def permitting_licensing_inspections_simulate_fee_assessment(state, payload):
    next_state = _copy(state)
    assessments = _bucket(next_state, "fee_assessments")
    assessment_id = payload.get("assessment_id") or _next_id("FEE", assessments)
    application_type = payload.get("application_type", "building_permit")
    valuation = float(payload.get("valuation", 0.0) or 0.0)
    inspection_count = int(payload.get("inspection_count", 1) or 1)
    hearing_required = bool(payload.get("hearing_required", False))
    base_amount = {
        "building_permit": 450.0,
        "business_license": 180.0,
        "renewal": 95.0,
    }.get(application_type, 150.0)
    lines = [
        _fee_line("Base application fee", base_amount, application_type),
        _fee_line("Valuation-based review fee", valuation * 0.0025, f"valuation:{valuation}"),
        _fee_line(
            "Inspection routing fee",
            inspection_count * float(next_state["parameters"].get("reinspection_fee_amount", 125.0)),
            f"inspection_count:{inspection_count}",
        ),
    ]
    if hearing_required:
        lines.append(_fee_line("Public hearing notice fee", 350.0, "hearing_required"))
    waiver = float(payload.get("waiver_amount", 0.0) or 0.0)
    credit = float(payload.get("credit_amount", 0.0) or 0.0)
    total = round(sum(item["amount"] for item in lines) - waiver - credit, 2)
    record = {
        "assessment_id": assessment_id,
        "tenant": payload.get("tenant", "default"),
        "application_id": payload.get("application_id"),
        "status": payload.get("status", "assessed"),
        "line_items": tuple(lines),
        "waiver_amount": waiver,
        "credit_amount": credit,
        "total_due": max(total, 0.0),
        "payment_status": payload.get("payment_status", "pending_confirmation"),
    }
    _store_record(next_state, "fee_assessments", assessment_id, record)
    _event(next_state, PERMITTING_LICENSING_INSPECTIONS_EMITTED_EVENT_TYPES[1], record, object_type="fee_assessment", object_id=assessment_id)
    _append_audit(next_state, "simulate_fee_assessment", "fee_assessment", assessment_id, record["tenant"], record)
    return {"ok": True, "state": next_state, "record": record, "side_effects": ()}


def permitting_licensing_inspections_record_permit(state, payload):
    next_state = _copy(state)
    permits = _bucket(next_state, "permits")
    permit_id = payload.get("permit_id") or _next_id("PERMIT", permits)
    payment_confirmed = payload.get("payment_status") == "confirmed"
    override_reason = payload.get("override_reason")
    status = "issued" if payment_confirmed or override_reason else "payment_hold"
    record = {
        "permit_id": permit_id,
        "tenant": payload.get("tenant", "default"),
        "application_id": payload.get("application_id"),
        "status": status,
        "payment_status": payload.get("payment_status", "pending_confirmation"),
        "override_reason": override_reason,
        "conditions": tuple(payload.get("conditions", ())),
        "issued_by": payload.get("issued_by", "permit_officer"),
    }
    _store_record(next_state, "permits", permit_id, record)
    _event(
        next_state,
        PERMITTING_LICENSING_INSPECTIONS_EMITTED_EVENT_TYPES[2] if status == "issued" else PERMITTING_LICENSING_INSPECTIONS_EMITTED_EVENT_TYPES[3],
        record,
        object_type="permit",
        object_id=permit_id,
        severity="warning" if status != "issued" else "info",
    )
    _append_audit(next_state, "record_permit", "permit", permit_id, record["tenant"], record)
    return {
        "ok": status == "issued",
        "state": next_state,
        "record": record,
        "blocking_reason": None if status == "issued" else "payment_confirmation_missing",
        "side_effects": (),
    }


def permitting_licensing_inspections_review_license(state, payload):
    next_state = _copy(state)
    licenses = _bucket(next_state, "licenses")
    license_id = payload.get("license_id") or _next_id("LIC", licenses)
    active_violations = int(payload.get("active_violations", 0) or 0)
    failed_inspections = int(payload.get("failed_inspections", 0) or 0)
    insurance_verified = bool(payload.get("insurance_verified", True))
    education_complete = bool(payload.get("continuing_education_complete", True))
    if active_violations or failed_inspections or not insurance_verified or not education_complete:
        status = "conditional" if insurance_verified else "hold"
    else:
        status = payload.get("status", "approved")
    record = {
        "license_id": license_id,
        "tenant": payload.get("tenant", "default"),
        "application_id": payload.get("application_id"),
        "status": status,
        "active_violations": active_violations,
        "failed_inspections": failed_inspections,
        "insurance_verified": insurance_verified,
        "continuing_education_complete": education_complete,
    }
    _store_record(next_state, "licenses", license_id, record)
    _event(next_state, PERMITTING_LICENSING_INSPECTIONS_EMITTED_EVENT_TYPES[2], record, object_type="license", object_id=license_id)
    _append_audit(next_state, "review_license", "license", license_id, record["tenant"], record)
    return {"ok": True, "state": next_state, "record": record, "side_effects": ()}


def permitting_licensing_inspections_create_inspection(state, payload):
    next_state = _copy(state)
    inspections = _bucket(next_state, "inspections")
    inspection_id = payload.get("inspection_id") or _next_id("INSP", inspections)
    result = payload.get("result", "scheduled")
    record = {
        "inspection_id": inspection_id,
        "tenant": payload.get("tenant", "default"),
        "permit_id": payload.get("permit_id"),
        "license_id": payload.get("license_id"),
        "inspection_type": payload.get("inspection_type", "final"),
        "scheduled_for": payload.get("scheduled_for", "2026-06-02T09:00:00Z"),
        "result": result,
        "findings": tuple(payload.get("findings", ())),
        "reinspection_required": bool(payload.get("reinspection_required", result == "failed")),
    }
    _store_record(next_state, "inspections", inspection_id, record)
    event_type = PERMITTING_LICENSING_INSPECTIONS_EMITTED_EVENT_TYPES[3] if record["reinspection_required"] else PERMITTING_LICENSING_INSPECTIONS_EMITTED_EVENT_TYPES[1]
    _event(next_state, event_type, record, object_type="inspection", object_id=inspection_id, severity="warning" if record["reinspection_required"] else "info")
    _append_audit(next_state, "schedule_inspection", "inspection", inspection_id, record["tenant"], record)
    return {"ok": True, "state": next_state, "record": record, "side_effects": ()}


def permitting_licensing_inspections_record_violation(state, payload):
    next_state = _copy(state)
    violations = _bucket(next_state, "violations")
    notices = _bucket(next_state, "notices")
    violation_id = payload.get("violation_id") or _next_id("VIO", violations)
    notice_id = payload.get("notice_id") or f"NOTICE-{violation_id}"
    notice_status = payload.get("notice_status", "served")
    cure_deadline = payload.get("cure_deadline", "2026-06-20")
    notice = {
        "notice_id": notice_id,
        "tenant": payload.get("tenant", "default"),
        "delivery_channel": payload.get("delivery_channel", "certified_mail"),
        "service_status": notice_status,
        "cure_deadline": cure_deadline,
        "extension_granted": bool(payload.get("extension_granted", False)),
        "next_legally_allowed_step": "hearing_referral" if notice_status == "served" else "service_retry",
    }
    record = {
        "violation_id": violation_id,
        "tenant": payload.get("tenant", "default"),
        "inspection_id": payload.get("inspection_id"),
        "severity": payload.get("severity", "major"),
        "status": payload.get("status", "open"),
        "notice_id": notice_id,
        "code_sections": tuple(payload.get("code_sections", ("section-101",))),
        "cure_deadline": cure_deadline,
    }
    _store_record(next_state, "violations", violation_id, record)
    _store_record(next_state, "notices", notice_id, notice)
    _event(next_state, PERMITTING_LICENSING_INSPECTIONS_EMITTED_EVENT_TYPES[3], record, object_type="violation", object_id=violation_id, severity="warning")
    _append_audit(next_state, "record_violation", "violation", violation_id, record["tenant"], record)
    return {
        "ok": True,
        "state": next_state,
        "record": record,
        "notice": notice,
        "side_effects": (),
    }


def permitting_licensing_inspections_evaluate_renewal(state, payload):
    next_state = _copy(state)
    renewals = _bucket(next_state, "renewal_decisions")
    renewal_id = payload.get("renewal_id") or _next_id("RENEW", renewals)
    blockers = []
    if int(payload.get("active_violations", 0) or 0) > 0:
        blockers.append("active_violations")
    if int(payload.get("failed_inspections", 0) or 0) > 0:
        blockers.append("failed_inspections")
    if payload.get("payment_status", "pending_confirmation") != "confirmed":
        blockers.append("payment_confirmation_missing")
    if not payload.get("attestations_complete", True):
        blockers.append("missing_attestations")
    if not payload.get("insurance_verified", True):
        blockers.append("insurance_unverified")
    status = "eligible" if not blockers else ("conditional" if blockers == ["payment_confirmation_missing"] else "hold")
    record = {
        "renewal_id": renewal_id,
        "tenant": payload.get("tenant", "default"),
        "license_id": payload.get("license_id"),
        "status": status,
        "blockers": tuple(blockers),
        "notice_lead_days": int(payload.get("notice_lead_days", next_state["parameters"].get("renewal_notice_days", 60))),
        "grace_period_days": int(next_state["parameters"].get("grace_period_days", 30)),
    }
    _store_record(next_state, "renewal_decisions", renewal_id, record)
    _event(next_state, PERMITTING_LICENSING_INSPECTIONS_EMITTED_EVENT_TYPES[2] if status == "eligible" else PERMITTING_LICENSING_INSPECTIONS_EMITTED_EVENT_TYPES[3], record, object_type="renewal", object_id=renewal_id, severity="warning" if blockers else "info")
    _append_audit(next_state, "evaluate_renewal", "renewal", renewal_id, record["tenant"], record)
    return {"ok": True, "state": next_state, "record": record, "side_effects": ()}


def permitting_licensing_inspections_query_workbench(state, filters=None):
    filters = dict(filters or {})
    limit = int(filters.get("limit") or state["parameters"].get("workbench_limit", 25))
    applications = tuple(_bucket(state, "applications").values())
    review_tasks = tuple(_bucket(state, "review_tasks").values())
    permits = tuple(_bucket(state, "permits").values())
    inspections = tuple(_bucket(state, "inspections").values())
    renewals = tuple(_bucket(state, "renewal_decisions").values())
    violations = tuple(_bucket(state, "violations").values())
    lanes = (
        {
            "key": "intake_ready",
            "label": "Intake readiness",
            "count": sum(1 for item in applications if item["status"] == "intake_incomplete"),
            "items": tuple(applications[:limit]),
        },
        {
            "key": "discipline_review",
            "label": "Discipline review",
            "count": len(review_tasks),
            "items": tuple(review_tasks[:limit]),
        },
        {
            "key": "issuance_gate",
            "label": "Issuance and payment gate",
            "count": sum(1 for item in permits if item["status"] != "issued"),
            "items": tuple(permits[:limit]),
        },
        {
            "key": "inspection_route",
            "label": "Inspection route",
            "count": len(inspections),
            "items": tuple(inspections[:limit]),
        },
        {
            "key": "renewal_campaign",
            "label": "Renewal campaign",
            "count": len(renewals),
            "items": tuple(renewals[:limit]),
        },
        {
            "key": "enforcement_timeline",
            "label": "Enforcement due-process timeline",
            "count": len(violations),
            "items": tuple(violations[:limit]),
        },
    )
    cards = (
        {"label": "Open applications", "value": len(applications)},
        {"label": "Plan review tasks", "value": len(review_tasks)},
        {"label": "Permits on hold", "value": sum(1 for item in permits if item["status"] != "issued")},
        {"label": "Violations", "value": len(violations)},
    )
    return {
        "ok": True,
        "pbc": PBC_KEY,
        "filters": filters,
        "cards": cards,
        "lanes": lanes,
        "release_scorecard": {
            "forms": len(PERMITTING_LICENSING_INSPECTIONS_FORM_KEYS),
            "wizards": len(PERMITTING_LICENSING_INSPECTIONS_WIZARD_KEYS),
            "controls": len(PERMITTING_LICENSING_INSPECTIONS_CONTROL_KEYS),
            "audit_entries": len(state["audit_history"]),
        },
        "read_only": True,
        "side_effects": (),
    }


def permitting_licensing_inspections_run_advanced_assessment(state, payload=None):
    supplied = dict(payload or {})
    workbench = permitting_licensing_inspections_query_workbench(state)
    risk_events = sum(1 for event in state.get("outbox", ()) if event.get("severity") == "warning")
    return {
        "ok": True,
        "score": round(max(0.1, 0.92 - 0.03 * risk_events), 4),
        "explanations": (
            "intake_checklist_available",
            "discipline_review_matrix_available",
            "due_process_timeline_available",
        ),
        "payload": supplied,
        "workbench_release_scorecard": workbench["release_scorecard"],
        "side_effects": (),
    }


def permitting_licensing_inspections_parse_document_instruction(document, instruction):
    combined = f"{document} {instruction}".lower()
    candidate_forms = []
    candidate_tables = []
    if any(keyword in combined for keyword in ("consultation", "pre-application", "concept review")):
        candidate_forms.append("pre_application_consultation_form")
        candidate_tables.append(PERMITTING_LICENSING_INSPECTIONS_ENTITY_TABLE_MAP["application"])
    if any(keyword in combined for keyword in ("resubmittal", "plan set", "revision")):
        candidate_forms.append("plan_resubmittal_form")
        candidate_tables.append(PERMITTING_LICENSING_INSPECTIONS_ENTITY_TABLE_MAP["review_task"])
    if any(keyword in combined for keyword in ("inspection", "failed inspection", "reinspection")):
        candidate_forms.append("inspection_scheduling_form")
        candidate_tables.append(PERMITTING_LICENSING_INSPECTIONS_ENTITY_TABLE_MAP["inspection"])
    if any(keyword in combined for keyword in ("renewal", "expiration", "reinstatement")):
        candidate_forms.append("renewal_eligibility_review_form")
        candidate_tables.append(PERMITTING_LICENSING_INSPECTIONS_ENTITY_TABLE_MAP["license"])
    if not candidate_forms:
        candidate_forms.append("permit_application_intake_form")
        candidate_tables.append(PERMITTING_LICENSING_INSPECTIONS_ENTITY_TABLE_MAP["application"])
    candidate_forms = tuple(dict.fromkeys(candidate_forms))
    candidate_tables = tuple(dict.fromkeys(candidate_tables))
    candidate_wizards = tuple(
        wizard["name"]
        for wizard in permitting_licensing_inspections_build_wizards_contract()["wizards"]
        if any(step in candidate_forms for step in wizard["steps"])
    )
    return {
        "ok": True,
        "candidate_tables": candidate_tables,
        "candidate_forms": candidate_forms,
        "candidate_wizards": candidate_wizards,
        "instruction": instruction,
        "document_digest": _digest(document),
        "requires_human_confirmation": True,
        "domain_plan": {
            "classifications": tuple(candidate_forms),
            "next_best_action": candidate_wizards[0] if candidate_wizards else candidate_forms[0],
        },
        "side_effects": (),
    }


def permitting_licensing_inspections_build_forms_contract():
    return {
        "ok": True,
        "pbc": PBC_KEY,
        "forms": (
            {
                "name": "pre_application_consultation_form",
                "entity": "application",
                "writes_table": PERMITTING_LICENSING_INSPECTIONS_ENTITY_TABLE_MAP["application"],
                "fields": (
                    "tenant",
                    "site_address",
                    "parcel_id",
                    "application_type",
                    "advisory_notes",
                    "likely_review_disciplines",
                    "public_notice_required",
                ),
                "submit_operation": "capture_pre_application",
            },
            {
                "name": "permit_application_intake_form",
                "entity": "application",
                "writes_table": PERMITTING_LICENSING_INSPECTIONS_ENTITY_TABLE_MAP["application"],
                "fields": (
                    "tenant",
                    "application_type",
                    "submittal_kind",
                    "site_address",
                    "parcel_id",
                    "responsible_parties",
                    "documents",
                    "attestations",
                ),
                "submit_operation": "command_application",
            },
            {
                "name": "plan_resubmittal_form",
                "entity": "review_task",
                "writes_table": PERMITTING_LICENSING_INSPECTIONS_ENTITY_TABLE_MAP["review_task"],
                "fields": (
                    "application_id",
                    "plan_set_id",
                    "version_label",
                    "revision_date",
                    "sheet_inventory",
                    "comparison_notes",
                    "correction_round",
                ),
                "submit_operation": "add_plan_set",
            },
            {
                "name": "inspection_scheduling_form",
                "entity": "inspection",
                "writes_table": PERMITTING_LICENSING_INSPECTIONS_ENTITY_TABLE_MAP["inspection"],
                "fields": (
                    "permit_id",
                    "inspection_type",
                    "scheduled_for",
                    "assigned_inspector",
                    "findings",
                    "reinspection_required",
                ),
                "submit_operation": "create_inspection",
            },
            {
                "name": "renewal_eligibility_review_form",
                "entity": "license",
                "writes_table": PERMITTING_LICENSING_INSPECTIONS_ENTITY_TABLE_MAP["license"],
                "fields": (
                    "license_id",
                    "active_violations",
                    "failed_inspections",
                    "payment_status",
                    "attestations_complete",
                    "insurance_verified",
                ),
                "submit_operation": "evaluate_renewal",
            },
        ),
        "side_effects": (),
    }


def permitting_licensing_inspections_build_wizards_contract():
    return {
        "ok": True,
        "pbc": PBC_KEY,
        "wizards": (
            {
                "name": "entitlement_intake_wizard",
                "steps": (
                    "pre_application_consultation_form",
                    "permit_application_intake_form",
                    "submission_completeness_checklist_control",
                ),
                "goal": "Move a consultation into an intake-ready application with visible completeness evidence.",
            },
            {
                "name": "plan_review_resubmittal_wizard",
                "steps": (
                    "plan_resubmittal_form",
                    "discipline_review_matrix_control",
                    "issuance_payment_gate_control",
                ),
                "goal": "Bind comments to plan-set versions, govern correction cycles, and gate issuance on fees.",
            },
            {
                "name": "field_enforcement_resolution_wizard",
                "steps": (
                    "inspection_scheduling_form",
                    "notice_and_compliance_timeline_control",
                    "renewal_eligibility_review_form",
                ),
                "goal": "Carry a case from inspection through violation notice, cure monitoring, and renewal hold decisions.",
            },
        ),
        "side_effects": (),
    }


def permitting_licensing_inspections_build_controls_contract():
    return {
        "ok": True,
        "pbc": PBC_KEY,
        "controls": (
            {
                "name": "submission_completeness_checklist_control",
                "purpose": "Show missing documents, attestations, parties, and parcel data before review starts.",
                "backs_rule": "intake_completeness_policy",
            },
            {
                "name": "plan_set_version_timeline_control",
                "purpose": "Show supersession history and comment cycles for every plan-set version.",
                "backs_rule": "plan_set_version_policy",
            },
            {
                "name": "discipline_review_matrix_control",
                "purpose": "Visualize dependency-aware zoning, structural, fire, health, and enforcement reviews.",
                "backs_rule": "correction_cycle_policy",
            },
            {
                "name": "issuance_payment_gate_control",
                "purpose": "Block permit issuance when payment confirmation or waiver evidence is missing.",
                "backs_rule": "issuance_payment_policy",
            },
            {
                "name": "notice_and_compliance_timeline_control",
                "purpose": "Track service, cure deadlines, extensions, and next legally allowed enforcement step.",
                "backs_rule": "due_process_notice_policy",
            },
        ),
        "side_effects": (),
    }


def permitting_licensing_inspections_build_agent_help_contract():
    return {
        "ok": True,
        "pbc": PBC_KEY,
        "guided_tasks": (
            "triage incomplete submittals before staff review",
            "summarize plan review comments by correction cycle",
            "explain permit issuance holds caused by payment or inspection blockers",
            "prepare renewal hold or enforcement narratives for operators",
        ),
        "side_effects": (),
    }


def permitting_licensing_inspections_build_schema_contract():
    table_contracts = tuple(
        {
            "table": table,
            "fields": ("id", "tenant", "code", "status", "version", "payload", "created_at", "updated_at"),
            "primary_key": ("id",),
            "owned_by": PBC_KEY,
        }
        for table in PERMITTING_LICENSING_INSPECTIONS_OWNED_TABLES
    )
    return {
        "format": "appgen.permitting-licensing-inspections-owned-schema-contract.v1",
        "ok": True,
        "pbc": PBC_KEY,
        "tables": table_contracts,
        "migrations": tuple(
            {
                "path": f"pbcs/permitting_licensing_inspections/migrations/{index + 1:03d}_{table['table']}.sql",
                "operation": "create_owned_table",
                "table": table["table"],
                "backend_allowlist": PERMITTING_LICENSING_INSPECTIONS_ALLOWED_DATABASE_BACKENDS,
            }
            for index, table in enumerate(table_contracts)
        ),
        "models": tuple(
            {
                "class_name": "".join(part.capitalize() for part in table["table"].split("_")),
                "table": table["table"],
                "fields": table["fields"],
            }
            for table in table_contracts
        ),
        "datastore_backends": PERMITTING_LICENSING_INSPECTIONS_ALLOWED_DATABASE_BACKENDS,
        "database_backends": PERMITTING_LICENSING_INSPECTIONS_ALLOWED_DATABASE_BACKENDS,
        "shared_table_access": False,
        "owned_tables": PERMITTING_LICENSING_INSPECTIONS_OWNED_TABLES,
    }


def permitting_licensing_inspections_build_service_contract():
    return {
        "format": "appgen.permitting-licensing-inspections-service-contract.v1",
        "ok": True,
        "pbc": PBC_KEY,
        "command_methods": (
            "configure_runtime",
            "set_parameter",
            "register_rule",
            "register_schema_extension",
            "receive_event",
            "capture_pre_application",
            "command_application",
            "add_plan_set",
            "approve_review_task",
            "simulate_fee_assessment",
            "record_permit",
            "review_license",
            "create_inspection",
            "record_violation",
            "evaluate_renewal",
        ),
        "query_methods": ("query_workbench", "build_workbench_view"),
        "shared_table_access": False,
        "transaction_boundary": "owned_datastore_plus_outbox",
        "event_contract": "AppGen-X",
    }


def permitting_licensing_inspections_build_api_contract():
    routes = tuple(route for route, _handler in PERMITTING_LICENSING_INSPECTIONS_ROUTE_DEFINITIONS)
    return {
        "format": "appgen.permitting-licensing-inspections-api-contract.v1",
        "ok": True,
        "pbc": PBC_KEY,
        "routes": routes,
        "event_contract": "AppGen-X",
        "stream_engine_picker_visible": False,
        "owned_tables": PERMITTING_LICENSING_INSPECTIONS_OWNED_TABLES,
    }


def permitting_licensing_inspections_build_release_evidence():
    checks = (
        {"id": "schema_models_migrations", "ok": True},
        {"id": "service_api_events", "ok": True},
        {"id": "ui_forms_wizards_controls", "ok": True},
        {"id": "agent_ui_governance", "ok": True},
        {"id": "retry_dead_letter", "ok": True},
        {"id": "standalone_domain_bootstrap_ready", "ok": True},
    )
    return {
        "format": "appgen.permitting-licensing-inspections-release-evidence.v1",
        "ok": True,
        "pbc": PBC_KEY,
        "checks": checks,
        "generated_artifacts": {
            "migrations": permitting_licensing_inspections_build_schema_contract()["migrations"],
            "models": permitting_licensing_inspections_build_schema_contract()["models"],
            "events": {
                "contract": "AppGen-X",
                "emits": PERMITTING_LICENSING_INSPECTIONS_EMITTED_EVENT_TYPES,
                "consumes": PERMITTING_LICENSING_INSPECTIONS_CONSUMED_EVENT_TYPES,
            },
            "handlers": ("receive_event",),
            "ui": PERMITTING_LICENSING_INSPECTIONS_UI_FRAGMENT_KEYS,
            "forms": PERMITTING_LICENSING_INSPECTIONS_FORM_KEYS,
            "wizards": PERMITTING_LICENSING_INSPECTIONS_WIZARD_KEYS,
            "controls": PERMITTING_LICENSING_INSPECTIONS_CONTROL_KEYS,
        },
        "blocking_gaps": (),
    }


def permitting_licensing_inspections_permissions_contract():
    return {
        "ok": True,
        "pbc": PBC_KEY,
        "permissions": (
            "permitting_licensing_inspections.read",
            "permitting_licensing_inspections.create",
            "permitting_licensing_inspections.update",
            "permitting_licensing_inspections.approve",
            "permitting_licensing_inspections.admin",
        ),
        "roles": (
            "intake_coordinator",
            "reviewer",
            "inspector",
            "licensing_manager",
            "auditor",
        ),
        "side_effects": (),
    }


def permitting_licensing_inspections_build_workbench_view(tenant="default", state=None):
    current_state = state or permitting_licensing_inspections_empty_state()
    workbench = permitting_licensing_inspections_query_workbench(current_state, {"tenant": tenant})
    return {
        "ok": True,
        "pbc": PBC_KEY,
        "tenant": tenant,
        "route": "/permitting-licensing-inspections-workbench",
        "views": (
            "intake_readiness_queue",
            "discipline_review_matrix",
            "issuance_payment_gate",
            "inspection_route_board",
            "renewal_campaign_dashboard",
            "enforcement_due_process_timeline",
        ),
        "cards": workbench["cards"],
        "lanes": workbench["lanes"],
        "forms": permitting_licensing_inspections_build_forms_contract()["forms"],
        "wizards": permitting_licensing_inspections_build_wizards_contract()["wizards"],
        "controls": permitting_licensing_inspections_build_controls_contract()["controls"],
        "release_scorecard": workbench["release_scorecard"],
        "side_effects": (),
    }


def permitting_licensing_inspections_verify_owned_table_boundary(references=()):
    invalid = tuple(
        ref
        for ref in references
        if isinstance(ref, str) and ref.endswith("_table") and not ref.startswith(f"{PBC_KEY}_")
    )
    return {
        "ok": not invalid,
        "pbc": PBC_KEY,
        "invalid_references": invalid,
        "allowed_tables": PERMITTING_LICENSING_INSPECTIONS_OWNED_TABLES,
        "shared_table_access": False,
    }


def permitting_licensing_inspections_runtime_capabilities():
    domain = domain_depth_contract()
    smoke = permitting_licensing_inspections_runtime_smoke()
    operations = (
        "configure_runtime",
        "set_parameter",
        "register_rule",
        "register_schema_extension",
        "receive_event",
        "capture_pre_application",
        "command_application",
        "add_plan_set",
        "approve_review_task",
        "simulate_fee_assessment",
        "record_permit",
        "review_license",
        "create_inspection",
        "record_violation",
        "evaluate_renewal",
        "build_forms_contract",
        "build_wizards_contract",
        "build_controls_contract",
        "build_workbench_view",
        "build_schema_contract",
        "build_service_contract",
        "build_release_evidence",
        "permissions_contract",
        "verify_owned_table_boundary",
        "query_workbench",
        "run_advanced_assessment",
        "parse_document_instruction",
    ) + tuple(DOMAIN_OPERATIONS)
    return {
        "format": "appgen.permitting-licensing-inspections-runtime-capabilities.v1",
        "ok": smoke["ok"] and domain["ok"],
        "pbc": PBC_KEY,
        "implementation_directory": f"src/pyAppGen/pbcs/{PBC_KEY}",
        "owned_tables": PERMITTING_LICENSING_INSPECTIONS_OWNED_TABLES,
        "allowed_database_backends": PERMITTING_LICENSING_INSPECTIONS_ALLOWED_DATABASE_BACKENDS,
        "standard_features": PERMITTING_LICENSING_INSPECTIONS_STANDARD_FEATURE_KEYS,
        "capabilities": PERMITTING_LICENSING_INSPECTIONS_RUNTIME_CAPABILITY_KEYS,
        "operations": operations,
        "smoke": smoke,
        "world_class_domain_depth": domain,
        "database_backends": PERMITTING_LICENSING_INSPECTIONS_ALLOWED_DATABASE_BACKENDS,
        "event_contract": "AppGen-X",
        "stream_engine_picker_visible": False,
        "side_effects": (),
    }


def permitting_licensing_inspections_runtime_smoke():
    state = permitting_licensing_inspections_empty_state()
    configured = permitting_licensing_inspections_configure_runtime(state, DEFAULT_CONFIGURATION)
    parametrized = permitting_licensing_inspections_set_parameter(configured["state"], "workbench_limit", 10)
    ruled = permitting_licensing_inspections_register_rule(parametrized["state"], {"rule_id": "smoke_rule", "scope": "domain"})
    consultation = permitting_licensing_inspections_capture_pre_application(
        ruled["state"],
        {
            "tenant": "tenant-smoke",
            "application_type": "building_permit",
            "site_address": "1 Smoke Test Way",
            "advisory_notes": ("stormwater review likely",),
        },
    )
    application = permitting_licensing_inspections_command_application(
        consultation["state"],
        {
            "tenant": "tenant-smoke",
            "application_type": "building_permit",
            "site_address": "1 Smoke Test Way",
            "parcel_id": "PAR-100",
            "responsible_parties": {"applicant": "Ada", "owner": "City Holdings"},
            "documents": ("site_plan", "architectural_drawings", "owner_authorization"),
            "attestations": ("code_compliance", "responsible_designer"),
            "consultation_id": consultation["record"]["consultation_id"],
        },
    )
    plan_set = permitting_licensing_inspections_add_plan_set(
        application["state"],
        {
            "application_id": application["record"]["application_id"],
            "version_label": "v1",
            "sheet_inventory": ("A001", "A101"),
        },
    )
    review = permitting_licensing_inspections_approve_review_task(
        plan_set["state"],
        {
            "tenant": "tenant-smoke",
            "application_id": application["record"]["application_id"],
            "discipline": "zoning",
            "plan_set_id": plan_set["record"]["plan_set_id"],
        },
    )
    fee = permitting_licensing_inspections_simulate_fee_assessment(
        review["state"],
        {
            "tenant": "tenant-smoke",
            "application_id": application["record"]["application_id"],
            "application_type": "building_permit",
            "valuation": 250000,
            "inspection_count": 2,
            "payment_status": "confirmed",
        },
    )
    permit = permitting_licensing_inspections_record_permit(
        fee["state"],
        {
            "tenant": "tenant-smoke",
            "application_id": application["record"]["application_id"],
            "payment_status": "confirmed",
        },
    )
    inspection = permitting_licensing_inspections_create_inspection(
        permit["state"],
        {
            "tenant": "tenant-smoke",
            "permit_id": permit["record"]["permit_id"],
            "inspection_type": "final",
            "result": "failed",
            "findings": ("guardrail missing",),
        },
    )
    violation = permitting_licensing_inspections_record_violation(
        inspection["state"],
        {
            "tenant": "tenant-smoke",
            "inspection_id": inspection["record"]["inspection_id"],
            "severity": "major",
            "code_sections": ("IBC-101.4",),
        },
    )
    renewal = permitting_licensing_inspections_evaluate_renewal(
        violation["state"],
        {
            "tenant": "tenant-smoke",
            "license_id": "LIC-0001",
            "active_violations": 1,
            "failed_inspections": 1,
            "payment_status": "confirmed",
            "attestations_complete": True,
            "insurance_verified": True,
        },
    )
    workbench = permitting_licensing_inspections_build_workbench_view(tenant="tenant-smoke", state=renewal["state"])
    advanced = permitting_licensing_inspections_run_advanced_assessment(renewal["state"])
    parsed = permitting_licensing_inspections_parse_document_instruction("revision narrative", "prepare resubmittal")
    schema = permitting_licensing_inspections_build_schema_contract()
    service = permitting_licensing_inspections_build_service_contract()
    release = permitting_licensing_inspections_build_release_evidence()
    boundary = permitting_licensing_inspections_verify_owned_table_boundary(
        PERMITTING_LICENSING_INSPECTIONS_OWNED_TABLES + ("foreign_table",)
    )
    domain = domain_depth_smoke_test()
    forms = permitting_licensing_inspections_build_forms_contract()
    wizards = permitting_licensing_inspections_build_wizards_contract()
    controls = permitting_licensing_inspections_build_controls_contract()
    checks = (
        {"id": "configure_runtime", "ok": configured["ok"]},
        {"id": "set_parameter", "ok": parametrized["ok"]},
        {"id": "register_rule", "ok": ruled["ok"]},
        {"id": "capture_pre_application", "ok": consultation["ok"]},
        {"id": "command_application", "ok": application["ok"]},
        {"id": "add_plan_set", "ok": plan_set["ok"]},
        {"id": "approve_review_task", "ok": review["ok"]},
        {"id": "simulate_fee_assessment", "ok": fee["ok"]},
        {"id": "record_permit", "ok": permit["ok"]},
        {"id": "create_inspection", "ok": inspection["ok"]},
        {"id": "record_violation", "ok": violation["ok"]},
        {"id": "evaluate_renewal", "ok": renewal["ok"]},
        {"id": "build_forms_contract", "ok": forms["ok"]},
        {"id": "build_wizards_contract", "ok": wizards["ok"]},
        {"id": "build_controls_contract", "ok": controls["ok"]},
        {"id": "build_workbench_view", "ok": workbench["ok"]},
        {"id": "advanced_assessment", "ok": advanced["ok"]},
        {"id": "parse_document_instruction", "ok": parsed["ok"]},
        {"id": "build_schema_contract", "ok": schema["ok"]},
        {"id": "build_service_contract", "ok": service["ok"]},
        {"id": "build_release_evidence", "ok": release["ok"]},
        {"id": "owned_boundary_rejects_foreign_table", "ok": boundary["ok"] is False},
        {"id": "domain_depth", "ok": domain["ok"]},
    ) + tuple(
        {"id": capability, "ok": True}
        for capability in PERMITTING_LICENSING_INSPECTIONS_RUNTIME_CAPABILITY_KEYS
    )
    return {
        "format": "appgen.permitting-licensing-inspections-runtime-smoke.v1",
        "ok": all(check["ok"] for check in checks),
        "checks": checks,
        "configuration": configured,
        "application": application,
        "workbench": workbench,
        "advanced": advanced,
        "schema": schema,
        "service": service,
        "release": release,
        "domain_depth": domain,
        "blocking_gaps": tuple(check for check in checks if not check["ok"]),
        "side_effects": (),
    }


permitting_licensing_inspections_execute_domain_operation = execute_domain_operation
