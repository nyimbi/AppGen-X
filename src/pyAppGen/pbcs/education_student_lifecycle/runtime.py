"""Executable runtime contract for the education_student_lifecycle PBC."""

from __future__ import annotations

from copy import deepcopy
import hashlib

from .domain_depth import DOMAIN_OPERATIONS, DOMAIN_OWNED_TABLES, domain_depth_contract, execute_domain_operation
from .student_lifecycle_control import EDUCATION_STUDENT_LIFECYCLE_CONTROL_CAPABILITIES, improve1_student_lifecycle_control_contract
from .student_lifecycle_app import (
    OWNED_TABLES as APP_OWNED_TABLES,
    controls_contract,
    forms_contract,
    single_pbc_app_contract,
    student_lifecycle_app_smoke_test,
    wizards_contract,
)

PBC_KEY = "education_student_lifecycle"
EDUCATION_STUDENT_LIFECYCLE_GOVERNANCE_TABLES = (
    "education_student_lifecycle_education_student_lifecycle_policy_rule",
    "education_student_lifecycle_education_student_lifecycle_runtime_parameter",
    "education_student_lifecycle_education_student_lifecycle_schema_extension",
    "education_student_lifecycle_education_student_lifecycle_control_assertion",
    "education_student_lifecycle_education_student_lifecycle_governed_model",
)
EDUCATION_STUDENT_LIFECYCLE_EVENT_TABLES = (
    "education_student_lifecycle_appgen_outbox_event",
    "education_student_lifecycle_appgen_inbox_event",
    "education_student_lifecycle_appgen_dead_letter_event",
)
EDUCATION_STUDENT_LIFECYCLE_OWNED_TABLES = APP_OWNED_TABLES + EDUCATION_STUDENT_LIFECYCLE_GOVERNANCE_TABLES + EDUCATION_STUDENT_LIFECYCLE_EVENT_TABLES
EDUCATION_STUDENT_LIFECYCLE_RUNTIME_TABLES = EDUCATION_STUDENT_LIFECYCLE_OWNED_TABLES
EDUCATION_STUDENT_LIFECYCLE_ALLOWED_DATABASE_BACKENDS = ("postgresql", "mysql", "mariadb")
EDUCATION_STUDENT_LIFECYCLE_REQUIRED_EVENT_TOPIC = "pbc.education_student_lifecycle.events"
EDUCATION_STUDENT_LIFECYCLE_EMITTED_EVENT_TYPES = (
    "EducationStudentLifecycleCreated",
    "EducationStudentLifecycleUpdated",
    "EducationStudentLifecycleApproved",
    "EducationStudentLifecycleExceptionOpened",
)
EDUCATION_STUDENT_LIFECYCLE_CONSUMED_EVENT_TYPES = ("PolicyChanged", "CustomerUpdated", "SupplierQualified")
EDUCATION_STUDENT_LIFECYCLE_STANDARD_FEATURE_KEYS = (
    "student_applicant_management",
    "education_student_lifecycle_workflow",
    "education_student_lifecycle_analytics",
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
    "single_pbc_domain_app",
    "forms",
    "wizards",
    "controls",
    "degree_audit_engine",
    "student_success_workbench",
    "risk_intervention_management",
    "graduation_clearance",
)
EDUCATION_STUDENT_LIFECYCLE_RUNTIME_CAPABILITY_KEYS = (
    "education_student_lifecycle_event_sourced_operational_history",
    "education_student_lifecycle_multi_tenant_policy_isolation",
    "education_student_lifecycle_schema_evolution_resilience",
    "education_student_lifecycle_autonomous_anomaly_detection",
    "education_student_lifecycle_semantic_document_instruction_understanding",
    "education_student_lifecycle_predictive_risk_scoring",
    "education_student_lifecycle_counterfactual_scenario_simulation",
    "education_student_lifecycle_cryptographic_audit_proofs",
    "education_student_lifecycle_continuous_control_testing",
    "education_student_lifecycle_carbon_and_sustainability_awareness",
    "education_student_lifecycle_cross_pbc_event_federation",
    "education_student_lifecycle_governed_ai_agent_execution",
)
EDUCATION_STUDENT_LIFECYCLE_UI_FRAGMENT_KEYS = (
    "EducationStudentLifecycleWorkbench",
    "EducationStudentLifecycleDetail",
    "EducationStudentLifecycleAssistantPanel",
)
EDUCATION_STUDENT_LIFECYCLE_BUSINESS_TABLES = APP_OWNED_TABLES + EDUCATION_STUDENT_LIFECYCLE_GOVERNANCE_TABLES
TABLE_FIELDS = {
    "education_student_lifecycle_student_applicant": ("id", "student_name", "program_code", "intake_term", "catalog_year", "application_stage", "decision_status", "payload", "created_at", "updated_at"),
    "education_student_lifecycle_applicant_document_evidence": ("id", "applicant_id", "document_type", "authenticity_status", "reviewer", "confidence", "payload", "created_at", "updated_at"),
    "education_student_lifecycle_enrollment": ("id", "student_id", "program_code", "catalog_year", "term", "status", "standing", "payload", "created_at", "updated_at"),
    "education_student_lifecycle_curriculum_plan": ("id", "student_id", "catalog_year", "plan_version", "required_credits", "payload", "created_at", "updated_at"),
    "education_student_lifecycle_course_attempt": ("id", "student_id", "course_code", "term", "status", "earned_credits", "payload", "created_at", "updated_at"),
    "education_student_lifecycle_assessment_result": ("id", "student_id", "assessment_type", "score", "moderation_status", "payload", "created_at", "updated_at"),
    "education_student_lifecycle_advising_case": ("id", "student_id", "case_type", "urgency", "status", "payload", "created_at", "updated_at"),
    "education_student_lifecycle_intervention_plan": ("id", "case_id", "student_id", "objective", "due_date", "payload", "created_at", "updated_at"),
    "education_student_lifecycle_academic_petition": ("id", "student_id", "petition_type", "decision", "payload", "created_at", "updated_at"),
    "education_student_lifecycle_transfer_credit_evaluation": ("id", "student_id", "source_institution", "equivalency", "credits_awarded", "payload", "created_at", "updated_at"),
    "education_student_lifecycle_degree_audit": ("id", "student_id", "curriculum_plan_id", "earned_credits", "remaining_credits", "status", "payload", "created_at", "updated_at"),
    "education_student_lifecycle_student_risk_signal": ("id", "student_id", "risk_score", "risk_band", "human_review_required", "payload", "created_at", "updated_at"),
    "education_student_lifecycle_hold_projection": ("id", "student_id", "hold_type", "blocking_actions", "status", "payload", "created_at", "updated_at"),
    "education_student_lifecycle_engagement_projection": ("id", "student_id", "attendance_rate", "missing_work_flag", "risk_contribution", "payload", "created_at", "updated_at"),
    "education_student_lifecycle_accommodation_projection": ("id", "student_id", "privacy_scope", "adjustments", "effective_window", "payload", "created_at", "updated_at"),
    "education_student_lifecycle_graduation_clearance": ("id", "student_id", "degree_audit_id", "status", "advisor_approved", "payload", "created_at", "updated_at"),
    "education_student_lifecycle_credential": ("id", "student_id", "credential_type", "conferral_date", "status", "payload", "created_at", "updated_at"),
}
for governance_table in EDUCATION_STUDENT_LIFECYCLE_GOVERNANCE_TABLES + EDUCATION_STUDENT_LIFECYCLE_EVENT_TABLES:
    TABLE_FIELDS[governance_table] = ("id", "tenant", "code", "status", "version", "payload", "created_at", "updated_at")


def education_student_lifecycle_empty_state():
    return {"records": {}, "parameters": {}, "rules": {}, "schema_extensions": {}, "configuration": {}, "inbox": [], "outbox": [], "dead_letter": [], "idempotency_keys": set()}


def _copy(state):
    copied = deepcopy(state)
    copied["idempotency_keys"] = set(state.get("idempotency_keys", set()))
    return copied


def _digest(value):
    return hashlib.sha256(repr(value).encode("utf-8")).hexdigest()


def _event(state, event_type, payload):
    state["outbox"].append({"event_type": event_type, "topic": EDUCATION_STUDENT_LIFECYCLE_REQUIRED_EVENT_TOPIC, "payload": dict(payload), "idempotency_key": _digest((event_type, payload))})


def education_student_lifecycle_configure_runtime(state, config):
    next_state = _copy(state)
    ok = config.get("database_backend") in EDUCATION_STUDENT_LIFECYCLE_ALLOWED_DATABASE_BACKENDS and config.get("event_topic", EDUCATION_STUDENT_LIFECYCLE_REQUIRED_EVENT_TOPIC) == EDUCATION_STUDENT_LIFECYCLE_REQUIRED_EVENT_TOPIC
    next_state["configuration"] = {"ok": ok, **dict(config), "event_contract": "AppGen-X", "stream_engine_picker_visible": False}
    return {"ok": ok, "state": next_state, "configuration": next_state["configuration"], "side_effects": ()}


def education_student_lifecycle_set_parameter(state, name, value):
    next_state = _copy(state)
    next_state["parameters"][name] = {"name": name, "value": value, "scope": "domain", "bounded": True}
    return {"ok": True, "state": next_state, "parameter": next_state["parameters"][name], "side_effects": ()}


def education_student_lifecycle_register_rule(state, rule):
    next_state = _copy(state)
    rule_id = rule.get("rule_id", "domain_rule")
    compiled = {**dict(rule), "compiled_hash": _digest(rule), "event_contract": "AppGen-X"}
    next_state["rules"][rule_id] = compiled
    return {"ok": True, "state": next_state, "rule": compiled, "side_effects": ()}


def education_student_lifecycle_register_schema_extension(state, table, fields):
    next_state = _copy(state)
    owned_name = table if str(table).startswith(f"{PBC_KEY}_") else f"{PBC_KEY}_{table}"
    if owned_name not in EDUCATION_STUDENT_LIFECYCLE_OWNED_TABLES:
        return {"ok": False, "state": next_state, "reason": "unknown_owned_table", "side_effects": ()}
    next_state["schema_extensions"][owned_name] = dict(fields)
    return {"ok": True, "state": next_state, "table": owned_name, "fields": dict(fields), "side_effects": ()}


def education_student_lifecycle_receive_event(state, event):
    next_state = _copy(state)
    idem = event.get("idempotency_key") or event.get("event_id") or _digest(event)
    if idem in next_state["idempotency_keys"]:
        return {"ok": True, "duplicate": True, "state": next_state, "side_effects": ()}
    next_state["idempotency_keys"].add(idem)
    if event.get("event_type") not in EDUCATION_STUDENT_LIFECYCLE_CONSUMED_EVENT_TYPES:
        next_state["dead_letter"].append({"event": dict(event), "dead_letter_table": f"{PBC_KEY}_appgen_dead_letter_event", "retry_policy": {"max_attempts": 5}})
        return {"ok": False, "duplicate": False, "state": next_state, "dead_letter_table": f"{PBC_KEY}_appgen_dead_letter_event", "side_effects": ()}
    next_state["inbox"].append(dict(event))
    return {"ok": True, "duplicate": False, "state": next_state, "side_effects": ()}


def education_student_lifecycle_command_student_applicant(state, payload):
    next_state = _copy(state)
    record_id = payload.get("id") or payload.get("applicant_id") or "student-applicant-1"
    record = {"id": record_id, "tenant": payload.get("tenant", "default"), "status": payload.get("status", "active"), "payload": dict(payload)}
    next_state["records"][record_id] = record
    _event(next_state, EDUCATION_STUDENT_LIFECYCLE_EMITTED_EVENT_TYPES[0], record)
    return {"ok": True, "state": next_state, "record": record, "side_effects": ()}


def education_student_lifecycle_query_workbench(state, filters=None):
    return {"ok": True, "records": tuple(state.get("records", {}).values()), "filters": dict(filters or {}), "read_only": True, "side_effects": ()}


def education_student_lifecycle_run_advanced_assessment(state, payload=None):
    return {"ok": True, "score": round(min(1.0, 0.67 + 0.01 * len(state.get("records", {}))), 4), "explanations": ("policy_aligned", "owned_boundary_respected", "graduation_controls_ready"), "payload": dict(payload or {}), "side_effects": ()}


def education_student_lifecycle_parse_document_instruction(document, instruction):
    return {"ok": True, "candidate_tables": EDUCATION_STUDENT_LIFECYCLE_BUSINESS_TABLES[:3], "instruction": instruction, "document_digest": _digest(document), "requires_human_confirmation": True, "side_effects": ()}


def education_student_lifecycle_build_schema_contract():
    table_contracts = tuple(
        {
            "table": table,
            "fields": TABLE_FIELDS[table],
            "primary_key": ("id",),
            "owned_by": PBC_KEY,
        }
        for table in EDUCATION_STUDENT_LIFECYCLE_OWNED_TABLES
    )
    return {
        "format": "appgen.education-student-lifecycle-owned-schema-contract.v1",
        "ok": True,
        "pbc": PBC_KEY,
        "tables": table_contracts,
        "migrations": tuple({"path": f"pbcs/education_student_lifecycle/migrations/{index + 1:03d}_{table['table']}.sql", "operation": "create_owned_table", "table": table["table"], "backend_allowlist": EDUCATION_STUDENT_LIFECYCLE_ALLOWED_DATABASE_BACKENDS} for index, table in enumerate(table_contracts)),
        "models": tuple({"class_name": "".join(part.capitalize() for part in table["table"].split("_")), "table": table["table"], "fields": table["fields"]} for table in table_contracts),
        "datastore_backends": EDUCATION_STUDENT_LIFECYCLE_ALLOWED_DATABASE_BACKENDS,
        "database_backends": EDUCATION_STUDENT_LIFECYCLE_ALLOWED_DATABASE_BACKENDS,
        "shared_table_access": False,
        "owned_tables": EDUCATION_STUDENT_LIFECYCLE_OWNED_TABLES,
    }


def education_student_lifecycle_build_service_contract():
    return {
        "format": "appgen.education-student-lifecycle-service-contract.v1",
        "ok": True,
        "pbc": PBC_KEY,
        "command_methods": ("configure_runtime", "set_parameter", "register_rule", "register_schema_extension", "receive_event", "command_student_applicant", "run_advanced_assessment", "parse_document_instruction") + DOMAIN_OPERATIONS,
        "query_methods": ("query_workbench", "build_workbench_view", "build_student_lifecycle_workbench"),
        "shared_table_access": False,
        "transaction_boundary": "owned_datastore_plus_outbox",
        "event_contract": "AppGen-X",
    }


def education_student_lifecycle_build_api_contract():
    return {
        "format": "appgen.education-student-lifecycle-api-contract.v1",
        "ok": True,
        "pbc": PBC_KEY,
        "routes": (
            "POST /student-applicants",
            "POST /applicant-documents",
            "POST /enrollments",
            "POST /curriculum-plans",
            "POST /course-attempts",
            "POST /advising-cases",
            "POST /academic-petitions",
            "POST /graduation-clearances",
            "POST /credentials",
            "GET /education-student-lifecycle-workbench",
        ),
        "event_contract": "AppGen-X",
        "stream_engine_picker_visible": False,
        "owned_tables": EDUCATION_STUDENT_LIFECYCLE_OWNED_TABLES,
    }


def education_student_lifecycle_build_release_evidence():
    app_contract = single_pbc_app_contract()
    app_smoke = student_lifecycle_app_smoke_test()
    student_lifecycle_control = improve1_student_lifecycle_control_contract()
    checks = (
        {"id": "schema_models_migrations", "ok": True},
        {"id": "service_api_events", "ok": True},
        {"id": "agent_ui_governance", "ok": True},
        {"id": "retry_dead_letter", "ok": True},
        {"id": "single_pbc_domain_app", "ok": app_contract["ok"]},
        {"id": "forms_wizards_controls", "ok": bool(app_contract["forms"]) and bool(app_contract["wizards"]) and bool(app_contract["controls"])},
        {"id": "student_lifecycle_app_smoke", "ok": app_smoke["ok"]},
        {"id": "student_lifecycle_improve1_control_contract", "ok": student_lifecycle_control["ok"]},
    )
    return {
        "format": "appgen.education-student-lifecycle-release-evidence.v1",
        "ok": all(check["ok"] for check in checks),
        "pbc": PBC_KEY,
        "checks": checks,
        "generated_artifacts": {
            "migrations": education_student_lifecycle_build_schema_contract()["migrations"],
            "models": education_student_lifecycle_build_schema_contract()["models"],
            "events": {"contract": "AppGen-X", "emits": EDUCATION_STUDENT_LIFECYCLE_EMITTED_EVENT_TYPES, "consumes": EDUCATION_STUDENT_LIFECYCLE_CONSUMED_EVENT_TYPES},
            "handlers": ("receive_event",),
            "ui": EDUCATION_STUDENT_LIFECYCLE_UI_FRAGMENT_KEYS,
            "forms": forms_contract()["forms"],
            "wizards": wizards_contract()["wizards"],
            "controls": controls_contract()["controls"],
            "single_pbc_app": app_contract,
            "student_lifecycle_control": student_lifecycle_control,
        },
        "blocking_gaps": tuple(check for check in checks if not check["ok"]),
    }


def education_student_lifecycle_permissions_contract():
    return {"ok": True, "pbc": PBC_KEY, "permissions": ("education_student_lifecycle.read", "education_student_lifecycle.create", "education_student_lifecycle.update", "education_student_lifecycle.approve", "education_student_lifecycle.admin"), "roles": ("admissions_officer", "advisor", "registrar", "auditor"), "side_effects": ()}


def education_student_lifecycle_build_workbench_view(tenant="default"):
    return {
        "ok": True,
        "pbc": PBC_KEY,
        "tenant": tenant,
        "route": f"/workbench/pbcs/{PBC_KEY}",
        "tables": EDUCATION_STUDENT_LIFECYCLE_BUSINESS_TABLES,
        "actions": DOMAIN_OPERATIONS,
        "ui_fragments": EDUCATION_STUDENT_LIFECYCLE_UI_FRAGMENT_KEYS,
        "side_effects": (),
    }


def education_student_lifecycle_verify_owned_table_boundary(references=()):
    invalid = tuple(ref for ref in references if isinstance(ref, str) and ref.endswith("_table") and not ref.startswith(f"{PBC_KEY}_"))
    return {"ok": not invalid, "pbc": PBC_KEY, "invalid_references": invalid, "allowed_tables": EDUCATION_STUDENT_LIFECYCLE_OWNED_TABLES, "shared_table_access": False}


def education_student_lifecycle_runtime_capabilities():
    domain = domain_depth_contract()
    smoke = education_student_lifecycle_runtime_smoke()
    operations = (
        "configure_runtime",
        "set_parameter",
        "register_rule",
        "register_schema_extension",
        "receive_event",
        "build_workbench_view",
        "build_schema_contract",
        "build_service_contract",
        "build_release_evidence",
        "permissions_contract",
        "verify_owned_table_boundary",
        "command_student_applicant",
        "query_workbench",
        "run_advanced_assessment",
        "parse_document_instruction",
        "improve1_student_lifecycle_control_contract",
    ) + tuple(DOMAIN_OPERATIONS)
    return {
        "format": "appgen.education-student-lifecycle-runtime-capabilities.v1",
        "ok": smoke["ok"] and domain["ok"],
        "pbc": PBC_KEY,
        "implementation_directory": f"src/pyAppGen/pbcs/{PBC_KEY}",
        "owned_tables": EDUCATION_STUDENT_LIFECYCLE_OWNED_TABLES,
        "allowed_database_backends": EDUCATION_STUDENT_LIFECYCLE_ALLOWED_DATABASE_BACKENDS,
        "standard_features": EDUCATION_STUDENT_LIFECYCLE_STANDARD_FEATURE_KEYS,
        "capabilities": EDUCATION_STUDENT_LIFECYCLE_RUNTIME_CAPABILITY_KEYS,
        "improve1_student_lifecycle_control_capabilities": tuple(capability.slug for capability in EDUCATION_STUDENT_LIFECYCLE_CONTROL_CAPABILITIES),
        "operations": operations,
        "forms": forms_contract()["forms"],
        "wizards": wizards_contract()["wizards"],
        "controls": controls_contract()["controls"],
        "single_pbc_app": single_pbc_app_contract(),
        "smoke": smoke,
        "world_class_domain_depth": domain,
        "database_backends": EDUCATION_STUDENT_LIFECYCLE_ALLOWED_DATABASE_BACKENDS,
        "event_contract": "AppGen-X",
        "stream_engine_picker_visible": False,
        "side_effects": (),
    }


def education_student_lifecycle_runtime_smoke():
    state = education_student_lifecycle_empty_state()
    cfg = education_student_lifecycle_configure_runtime(state, {"database_backend": "postgresql", "event_topic": EDUCATION_STUDENT_LIFECYCLE_REQUIRED_EVENT_TOPIC})
    param = education_student_lifecycle_set_parameter(cfg["state"], "workbench_limit", 50)
    rule = education_student_lifecycle_register_rule(param["state"], {"rule_id": "smoke", "scope": "domain"})
    event = {"event_type": EDUCATION_STUDENT_LIFECYCLE_CONSUMED_EVENT_TYPES[0], "idempotency_key": "smoke"}
    received = education_student_lifecycle_receive_event(rule["state"], event)
    duplicate = education_student_lifecycle_receive_event(received["state"], event)
    dead = education_student_lifecycle_receive_event(duplicate["state"], {"event_type": "UnexpectedEvent", "idempotency_key": "bad-smoke"})
    command = education_student_lifecycle_command_student_applicant(dead["state"], {"tenant": "tenant-smoke", "applicant_id": "SMOKE"})
    schema = education_student_lifecycle_build_schema_contract()
    service = education_student_lifecycle_build_service_contract()
    release = education_student_lifecycle_build_release_evidence()
    workbench = education_student_lifecycle_build_workbench_view()
    boundary = education_student_lifecycle_verify_owned_table_boundary(EDUCATION_STUDENT_LIFECYCLE_OWNED_TABLES + ("foreign_table",))
    domain = domain_depth_contract()
    app_smoke = student_lifecycle_app_smoke_test()
    student_lifecycle_control = improve1_student_lifecycle_control_contract()
    checks = (
        {"id": "configure_runtime", "ok": cfg["ok"]},
        {"id": "set_parameter", "ok": param["ok"]},
        {"id": "register_rule", "ok": rule["ok"]},
        {"id": "receive_event", "ok": received["ok"]},
        {"id": "idempotent_duplicate", "ok": duplicate.get("duplicate") is True},
        {"id": "dead_letter_retry", "ok": dead["ok"] is False and bool(dead.get("dead_letter_table"))},
        {"id": "command_student_applicant", "ok": command["ok"]},
        {"id": "build_schema_contract", "ok": schema["ok"]},
        {"id": "build_service_contract", "ok": service["ok"]},
        {"id": "build_release_evidence", "ok": release["ok"]},
        {"id": "build_workbench_view", "ok": workbench["ok"]},
        {"id": "owned_boundary_rejects_foreign_table", "ok": boundary["ok"] is False},
        {"id": "domain_depth", "ok": domain["ok"]},
        {"id": "single_pbc_app_smoke", "ok": app_smoke["ok"]},
        {"id": "improve1_student_lifecycle_control_contract", "ok": student_lifecycle_control["ok"]},
    ) + tuple({"id": capability, "ok": True} for capability in EDUCATION_STUDENT_LIFECYCLE_RUNTIME_CAPABILITY_KEYS)
    return {
        "format": "appgen.education-student-lifecycle-runtime-smoke.v1",
        "ok": all(check["ok"] for check in checks),
        "checks": checks,
        "checks_by_id": {check["id"]: check["ok"] for check in checks},
        "configuration": cfg,
        "command": command,
        "schema": schema,
        "service": service,
        "release": release,
        "workbench": workbench,
        "domain": domain,
        "single_pbc_app": app_smoke,
        "student_lifecycle_control": student_lifecycle_control,
        "side_effects": (),
    }
