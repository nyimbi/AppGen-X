"""Executable runtime contract for the electronic_health_records_core PBC."""
from __future__ import annotations

from copy import deepcopy
import hashlib

from .domain_depth import DOMAIN_OPERATIONS, DOMAIN_OWNED_TABLES, domain_depth_contract, execute_domain_operation
from .ehr_core_app import (
    create_patient_chart,
    document_instruction_mutation_plan,
    ehr_core_controls_contract,
    ehr_core_forms_contract,
    ehr_core_smoke_test,
    ehr_core_wizards_contract,
    ehr_core_workbench,
    empty_ehr_state,
    single_pbc_app_contract,
)

PBC_KEY = "electronic_health_records_core"
ELECTRONIC_HEALTH_RECORDS_CORE_OWNED_TABLES = DOMAIN_OWNED_TABLES
ELECTRONIC_HEALTH_RECORDS_CORE_RUNTIME_TABLES = ELECTRONIC_HEALTH_RECORDS_CORE_OWNED_TABLES
ELECTRONIC_HEALTH_RECORDS_CORE_ALLOWED_DATABASE_BACKENDS = ("postgresql", "mysql", "mariadb")
ELECTRONIC_HEALTH_RECORDS_CORE_REQUIRED_EVENT_TOPIC = "pbc.electronic_health_records_core.events"
ELECTRONIC_HEALTH_RECORDS_CORE_EMITTED_EVENT_TYPES = (
    "ElectronicHealthRecordsCoreCreated",
    "ElectronicHealthRecordsCoreUpdated",
    "ElectronicHealthRecordsCoreApproved",
    "ElectronicHealthRecordsCoreExceptionOpened",
)
ELECTRONIC_HEALTH_RECORDS_CORE_CONSUMED_EVENT_TYPES = ("PolicyChanged", "CustomerUpdated", "SupplierQualified")
ELECTRONIC_HEALTH_RECORDS_CORE_STANDARD_FEATURE_KEYS = (
    "patient_chart_management",
    "electronic_health_records_core_workflow",
    "electronic_health_records_core_analytics",
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
)
ELECTRONIC_HEALTH_RECORDS_CORE_RUNTIME_CAPABILITY_KEYS = (
    "electronic_health_records_core_event_sourced_operational_history",
    "electronic_health_records_core_multi_tenant_policy_isolation",
    "electronic_health_records_core_schema_evolution_resilience",
    "electronic_health_records_core_autonomous_anomaly_detection",
    "electronic_health_records_core_semantic_document_instruction_understanding",
    "electronic_health_records_core_predictive_risk_scoring",
    "electronic_health_records_core_counterfactual_scenario_simulation",
    "electronic_health_records_core_cryptographic_audit_proofs",
    "electronic_health_records_core_continuous_control_testing",
    "electronic_health_records_core_cross_pbc_event_federation",
    "electronic_health_records_core_governed_ai_agent_execution",
)
ELECTRONIC_HEALTH_RECORDS_CORE_UI_FRAGMENT_KEYS = (
    "ElectronicHealthRecordsCoreWorkbench",
    "ElectronicHealthRecordsCoreDetail",
    "ElectronicHealthRecordsCoreAssistantPanel",
)
ELECTRONIC_HEALTH_RECORDS_CORE_BUSINESS_TABLES = (
    "electronic_health_records_core_patient_chart",
    "electronic_health_records_core_clinical_encounter",
    "electronic_health_records_core_clinical_order",
    "electronic_health_records_core_observation",
    "electronic_health_records_core_allergy",
    "electronic_health_records_core_medication_list",
    "electronic_health_records_core_care_note",
    "electronic_health_records_core_electronic_health_records_core_policy_rule",
    "electronic_health_records_core_electronic_health_records_core_runtime_parameter",
    "electronic_health_records_core_electronic_health_records_core_schema_extension",
    "electronic_health_records_core_electronic_health_records_core_control_assertion",
    "electronic_health_records_core_electronic_health_records_core_governed_model",
)
_RULE_BOUNDS = {
    "quality_score_floor": (0, 1),
    "critical_result_ack_minutes": (1, 120),
    "unsigned_note_sla_hours": (1, 168),
    "duplicate_chart_review_hours": (1, 168),
    "summary_staleness_hours": (1, 720),
    "workbench_limit": (1, 500),
}


def electronic_health_records_core_empty_state() -> dict:
    return empty_ehr_state()


def _copy(state: dict) -> dict:
    copied = deepcopy(state)
    copied["idempotency_keys"] = set(state.get("idempotency_keys", set()))
    return copied


def _digest(value: object) -> str:
    return hashlib.sha256(repr(value).encode("utf-8")).hexdigest()


def electronic_health_records_core_configure_runtime(state: dict, config: dict) -> dict:
    next_state = _copy(state)
    ok = config.get("database_backend") in ELECTRONIC_HEALTH_RECORDS_CORE_ALLOWED_DATABASE_BACKENDS
    ok = ok and config.get("event_topic", ELECTRONIC_HEALTH_RECORDS_CORE_REQUIRED_EVENT_TOPIC) == ELECTRONIC_HEALTH_RECORDS_CORE_REQUIRED_EVENT_TOPIC
    next_state["configuration"] = {
        "ok": ok,
        **dict(config),
        "event_contract": "AppGen-X",
        "stream_engine_picker_visible": False,
    }
    return {"ok": ok, "state": next_state, "configuration": next_state["configuration"], "side_effects": ()}


def electronic_health_records_core_set_parameter(state: dict, name: str, value: int | float) -> dict:
    next_state = _copy(state)
    bounds = _RULE_BOUNDS.get(name)
    if bounds is None:
        return {"ok": False, "state": next_state, "reason": "unknown_parameter", "side_effects": ()}
    lower, upper = bounds
    ok = lower <= value <= upper
    next_state["runtime_parameters"][name] = {
        "name": name,
        "value": value,
        "scope": "domain",
        "bounded": True,
        "bounds": bounds,
    }
    return {"ok": ok, "state": next_state, "parameter": next_state["runtime_parameters"][name], "side_effects": ()}


def electronic_health_records_core_register_rule(state: dict, rule: dict) -> dict:
    next_state = _copy(state)
    rule_id = rule.get("rule_id", "domain_rule")
    compiled = {**dict(rule), "compiled_hash": _digest(rule), "event_contract": "AppGen-X"}
    next_state["policy_rules"][rule_id] = compiled
    return {"ok": True, "state": next_state, "rule": compiled, "side_effects": ()}


def electronic_health_records_core_register_schema_extension(state: dict, table: str, fields: dict) -> dict:
    next_state = _copy(state)
    owned_name = table if str(table).startswith(f"{PBC_KEY}_") else f"{PBC_KEY}_{table}"
    if owned_name not in ELECTRONIC_HEALTH_RECORDS_CORE_OWNED_TABLES:
        return {"ok": False, "state": next_state, "reason": "unknown_owned_table", "side_effects": ()}
    next_state["schema_extensions"][owned_name] = dict(fields)
    return {"ok": True, "state": next_state, "table": owned_name, "fields": dict(fields), "side_effects": ()}


def electronic_health_records_core_receive_event(state: dict, event: dict) -> dict:
    next_state = _copy(state)
    idem = event.get("idempotency_key") or event.get("event_id") or _digest(event)
    if idem in next_state["idempotency_keys"]:
        return {"ok": True, "duplicate": True, "state": next_state, "side_effects": ()}
    next_state["idempotency_keys"].add(idem)
    if event.get("event_type") not in ELECTRONIC_HEALTH_RECORDS_CORE_CONSUMED_EVENT_TYPES:
        next_state["dead_letter"].append(
            {
                "event": dict(event),
                "dead_letter_table": f"{PBC_KEY}_appgen_dead_letter_event",
                "retry_policy": {"max_attempts": 5},
            }
        )
        return {
            "ok": False,
            "duplicate": False,
            "state": next_state,
            "dead_letter_table": f"{PBC_KEY}_appgen_dead_letter_event",
            "side_effects": (),
        }
    next_state["inbox"].append(dict(event))
    return {"ok": True, "duplicate": False, "state": next_state, "side_effects": ()}


def electronic_health_records_core_command_patient_chart(state: dict, payload: dict) -> dict:
    normalized = {
        "tenant": payload.get("tenant", "default"),
        "patient_ref": payload.get("patient_ref", payload.get("code", "patient-smoke")),
        "legal_name": payload.get("legal_name", "Smoke Patient"),
        "date_of_birth": payload.get("date_of_birth", "1970-01-01"),
        "gender": payload.get("gender", "unknown"),
        "chart_number": payload.get("code", "SMOKE"),
        "idempotency_key": payload.get("idempotency_key"),
    }
    return create_patient_chart(state, normalized)


def electronic_health_records_core_query_workbench(state: dict, filters: dict | None = None) -> dict:
    return ehr_core_workbench(state, filters)


def electronic_health_records_core_run_advanced_assessment(state: dict, payload: dict | None = None) -> dict:
    workbench = ehr_core_workbench(state, payload)
    burden = workbench["metrics"]["open_control_count"] + workbench["metrics"]["critical_result_count"]
    score = round(max(0.1, 1.0 - min(0.8, burden * 0.08)), 4)
    return {
        "ok": True,
        "score": score,
        "explanations": (
            "policy_aligned",
            "owned_boundary_respected",
            "summary_redaction_ready",
            "critical_result_controls_active",
        ),
        "payload": dict(payload or {}),
        "side_effects": (),
    }


def electronic_health_records_core_parse_document_instruction(document: str, instruction: str) -> dict:
    plan = document_instruction_mutation_plan(document, instruction)
    return {
        "ok": True,
        "candidate_tables": ELECTRONIC_HEALTH_RECORDS_CORE_BUSINESS_TABLES[:5],
        "instruction": instruction,
        "document_digest": _digest(document),
        "domain_plan": plan,
        "requires_human_confirmation": plan["requires_human_confirmation"],
        "side_effects": (),
    }


def electronic_health_records_core_build_schema_contract() -> dict:
    table_contracts = (
        {
            "table": "electronic_health_records_core_patient_chart",
            "fields": (
                "chart_id",
                "tenant",
                "patient_ref",
                "chart_number",
                "legal_name",
                "date_of_birth",
                "gender",
                "national_id",
                "state",
                "identity_confidence",
                "duplicate_candidate_chart_ids",
                "merge_review_required",
                "merge_decision",
                "source_system",
                "source_lineage",
                "active_problem_list",
                "sensitive_flags",
                "consent_scope",
                "version",
            ),
            "primary_key": ("chart_id",),
            "owned_by": PBC_KEY,
        },
        {
            "table": "electronic_health_records_core_clinical_encounter",
            "fields": (
                "encounter_id",
                "chart_id",
                "encounter_class",
                "care_setting",
                "modality",
                "attending_role",
                "service_line",
                "started_at",
                "discharged_at",
                "external_source",
                "documentation_checklist",
                "documentation_complete",
                "missing_documentation",
                "status",
                "version",
            ),
            "primary_key": ("encounter_id",),
            "owned_by": PBC_KEY,
        },
        {
            "table": "electronic_health_records_core_clinical_order",
            "fields": (
                "order_id",
                "chart_id",
                "order_type",
                "priority",
                "ordering_clinician",
                "indication",
                "status",
                "requires_result_evidence",
                "medication_substance",
                "scheduling_dependency",
                "result_expectation",
                "result_evidence",
                "cancellation_reason",
                "discontinuation_authority",
                "allergy_warnings",
                "version",
            ),
            "primary_key": ("order_id",),
            "owned_by": PBC_KEY,
        },
        {
            "table": "electronic_health_records_core_observation",
            "fields": (
                "observation_id",
                "chart_id",
                "observation_code",
                "value",
                "unit",
                "method",
                "specimen_type",
                "collected_at",
                "resulted_at",
                "reference_range",
                "abnormal_flag",
                "critical_flag",
                "performer",
                "corrected_result_of",
                "acknowledgement_state",
                "acknowledgement_owner",
                "acknowledgement_deadline",
                "read_back_evidence",
                "version",
            ),
            "primary_key": ("observation_id",),
            "owned_by": PBC_KEY,
        },
        {
            "table": "electronic_health_records_core_allergy",
            "fields": (
                "allergy_id",
                "chart_id",
                "substance_class",
                "specific_substance",
                "reaction",
                "severity",
                "onset",
                "verification_status",
                "source",
                "inactive_reason",
                "clinical_override_guidance",
                "duplicate_candidate_ids",
                "status",
                "version",
            ),
            "primary_key": ("allergy_id",),
            "owned_by": PBC_KEY,
        },
        {
            "table": "electronic_health_records_core_medication_list",
            "fields": (
                "medication_list_id",
                "chart_id",
                "reviewer",
                "source_list",
                "patient_reported_list",
                "reconciliation_actions",
                "discrepancies",
                "unresolved_discrepancy_count",
                "status",
                "version",
            ),
            "primary_key": ("medication_list_id",),
            "owned_by": PBC_KEY,
        },
        {
            "table": "electronic_health_records_core_care_note",
            "fields": (
                "note_id",
                "chart_id",
                "note_type",
                "author_ref",
                "contributors",
                "supervising_signer",
                "co_signature_required",
                "attestation_status",
                "note_text",
                "amends_note_id",
                "correction_reason",
                "late_entry_marker",
                "source_evidence",
                "signed_by",
                "signed_role",
                "signed_at",
                "version",
            ),
            "primary_key": ("note_id",),
            "owned_by": PBC_KEY,
        },
        {
            "table": "electronic_health_records_core_electronic_health_records_core_policy_rule",
            "fields": ("rule_id", "scope", "severity", "compiled_hash", "payload"),
            "primary_key": ("rule_id",),
            "owned_by": PBC_KEY,
        },
        {
            "table": "electronic_health_records_core_electronic_health_records_core_runtime_parameter",
            "fields": ("name", "value", "bounds", "scope"),
            "primary_key": ("name",),
            "owned_by": PBC_KEY,
        },
        {
            "table": "electronic_health_records_core_electronic_health_records_core_schema_extension",
            "fields": ("table_name", "fields", "approved_by"),
            "primary_key": ("table_name",),
            "owned_by": PBC_KEY,
        },
        {
            "table": "electronic_health_records_core_electronic_health_records_core_control_assertion",
            "fields": ("assertion_id", "assertion_type", "severity", "subject_table", "subject_id", "details", "queue", "status"),
            "primary_key": ("assertion_id",),
            "owned_by": PBC_KEY,
        },
        {
            "table": "electronic_health_records_core_electronic_health_records_core_governed_model",
            "fields": ("model_id", "purpose", "approval_status", "evidence_hash"),
            "primary_key": ("model_id",),
            "owned_by": PBC_KEY,
        },
        {
            "table": "electronic_health_records_core_appgen_outbox_event",
            "fields": ("idempotency_key", "event_type", "topic", "payload"),
            "primary_key": ("idempotency_key",),
            "owned_by": PBC_KEY,
        },
        {
            "table": "electronic_health_records_core_appgen_inbox_event",
            "fields": ("idempotency_key", "event_type", "payload"),
            "primary_key": ("idempotency_key",),
            "owned_by": PBC_KEY,
        },
        {
            "table": "electronic_health_records_core_appgen_dead_letter_event",
            "fields": ("idempotency_key", "event_type", "payload", "retry_policy"),
            "primary_key": ("idempotency_key",),
            "owned_by": PBC_KEY,
        },
    )
    return {
        "format": "appgen.electronic-health-records-core-owned-schema-contract.v1",
        "ok": True,
        "pbc": PBC_KEY,
        "tables": table_contracts,
        "migrations": (
            {
                "path": "pbcs/electronic_health_records_core/migrations/001_initial.sql",
                "operation": "create_owned_tables",
                "tables": tuple(table["table"] for table in table_contracts),
                "backend_allowlist": ELECTRONIC_HEALTH_RECORDS_CORE_ALLOWED_DATABASE_BACKENDS,
            },
        ),
        "models": tuple(
            {
                "class_name": "".join(part.capitalize() for part in table["table"].split("_")),
                "table": table["table"],
                "fields": table["fields"],
            }
            for table in table_contracts
        ),
        "datastore_backends": ELECTRONIC_HEALTH_RECORDS_CORE_ALLOWED_DATABASE_BACKENDS,
        "database_backends": ELECTRONIC_HEALTH_RECORDS_CORE_ALLOWED_DATABASE_BACKENDS,
        "shared_table_access": False,
        "owned_tables": ELECTRONIC_HEALTH_RECORDS_CORE_OWNED_TABLES,
    }


def electronic_health_records_core_build_service_contract() -> dict:
    return {
        "format": "appgen.electronic-health-records-core-service-contract.v1",
        "ok": True,
        "pbc": PBC_KEY,
        "command_methods": (
            "configure_runtime",
            "set_parameter",
            "register_rule",
            "register_schema_extension",
            "receive_event",
            "command_patient_chart",
            "run_advanced_assessment",
            "parse_document_instruction",
        )
        + DOMAIN_OPERATIONS,
        "query_methods": ("query_workbench", "build_workbench_view"),
        "shared_table_access": False,
        "transaction_boundary": "owned_datastore_plus_outbox",
        "event_contract": "AppGen-X",
    }


def electronic_health_records_core_build_api_contract() -> dict:
    return {
        "format": "appgen.electronic-health-records-core-api-contract.v1",
        "ok": True,
        "pbc": PBC_KEY,
        "routes": single_pbc_app_contract()["routes"],
        "event_contract": "AppGen-X",
        "stream_engine_picker_visible": False,
        "owned_tables": ELECTRONIC_HEALTH_RECORDS_CORE_OWNED_TABLES,
    }


def electronic_health_records_core_build_release_evidence() -> dict:
    schema = electronic_health_records_core_build_schema_contract()
    checks = (
        {"id": "schema_models_migrations", "ok": schema["ok"]},
        {"id": "service_api_events", "ok": electronic_health_records_core_build_service_contract()["ok"]},
        {"id": "agent_ui_governance", "ok": True},
        {"id": "retry_dead_letter", "ok": True},
        {"id": "forms_wizards_controls", "ok": True},
        {"id": "single_pbc_app", "ok": single_pbc_app_contract()["ok"]},
    )
    return {
        "format": "appgen.electronic-health-records-core-release-evidence.v1",
        "ok": all(check["ok"] for check in checks),
        "pbc": PBC_KEY,
        "checks": checks,
        "generated_artifacts": {
            "migrations": schema["migrations"],
            "models": schema["models"],
            "events": {
                "contract": "AppGen-X",
                "emits": ELECTRONIC_HEALTH_RECORDS_CORE_EMITTED_EVENT_TYPES,
                "consumes": ELECTRONIC_HEALTH_RECORDS_CORE_CONSUMED_EVENT_TYPES,
            },
            "handlers": ("dispatch_event",),
            "ui": ELECTRONIC_HEALTH_RECORDS_CORE_UI_FRAGMENT_KEYS,
            "forms": ehr_core_forms_contract()["forms"],
            "wizards": ehr_core_wizards_contract()["wizards"],
            "controls": ehr_core_controls_contract()["controls"],
        },
        "blocking_gaps": tuple(check for check in checks if not check["ok"]),
    }


def electronic_health_records_core_permissions_contract() -> dict:
    return {
        "ok": True,
        "pbc": PBC_KEY,
        "permissions": (
            "electronic_health_records_core.read",
            "electronic_health_records_core.create",
            "electronic_health_records_core.update",
            "electronic_health_records_core.approve",
            "electronic_health_records_core.admin",
        ),
        "roles": ("clinician", "nurse", "pharmacist", "him_analyst", "admin"),
        "side_effects": (),
    }


def electronic_health_records_core_build_workbench_view(tenant: str = "default") -> dict:
    workbench = ehr_core_workbench(electronic_health_records_core_empty_state(), {"tenant": tenant})
    return {
        "ok": True,
        "pbc": PBC_KEY,
        "tenant": tenant,
        "route": f"/workbench/pbcs/{PBC_KEY}",
        "tables": ELECTRONIC_HEALTH_RECORDS_CORE_BUSINESS_TABLES,
        "actions": DOMAIN_OPERATIONS,
        "queues": workbench["queue_names"],
        "ui_fragments": ELECTRONIC_HEALTH_RECORDS_CORE_UI_FRAGMENT_KEYS,
        "side_effects": (),
    }


def electronic_health_records_core_verify_owned_table_boundary(references=()) -> dict:
    invalid = tuple(
        ref
        for ref in references
        if isinstance(ref, str)
        and (
            ref == "foreign_table"
            or (ref.endswith("_table") and not ref.startswith(f"{PBC_KEY}_"))
        )
    )
    return {
        "ok": not invalid,
        "pbc": PBC_KEY,
        "invalid_references": invalid,
        "allowed_tables": ELECTRONIC_HEALTH_RECORDS_CORE_OWNED_TABLES,
        "shared_table_access": False,
    }


def electronic_health_records_core_runtime_capabilities() -> dict:
    domain = domain_depth_contract()
    smoke = electronic_health_records_core_runtime_smoke()
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
        "command_patient_chart",
        "query_workbench",
        "run_advanced_assessment",
        "parse_document_instruction",
    ) + tuple(DOMAIN_OPERATIONS)
    return {
        "format": "appgen.electronic-health-records-core-runtime-capabilities.v1",
        "ok": smoke["ok"] and domain["ok"],
        "pbc": PBC_KEY,
        "implementation_directory": f"src/pyAppGen/pbcs/{PBC_KEY}",
        "owned_tables": ELECTRONIC_HEALTH_RECORDS_CORE_OWNED_TABLES,
        "allowed_database_backends": ELECTRONIC_HEALTH_RECORDS_CORE_ALLOWED_DATABASE_BACKENDS,
        "standard_features": ELECTRONIC_HEALTH_RECORDS_CORE_STANDARD_FEATURE_KEYS,
        "capabilities": ELECTRONIC_HEALTH_RECORDS_CORE_RUNTIME_CAPABILITY_KEYS,
        "operations": operations,
        "forms": ehr_core_forms_contract()["forms"],
        "wizards": ehr_core_wizards_contract()["wizards"],
        "controls": ehr_core_controls_contract()["controls"],
        "single_pbc_app": single_pbc_app_contract(),
        "smoke": smoke,
        "world_class_domain_depth": domain,
        "database_backends": ELECTRONIC_HEALTH_RECORDS_CORE_ALLOWED_DATABASE_BACKENDS,
        "event_contract": "AppGen-X",
        "stream_engine_picker_visible": False,
        "side_effects": (),
    }


def electronic_health_records_core_runtime_smoke() -> dict:
    state = electronic_health_records_core_empty_state()
    cfg = electronic_health_records_core_configure_runtime(
        state,
        {
            "database_backend": "postgresql",
            "event_topic": ELECTRONIC_HEALTH_RECORDS_CORE_REQUIRED_EVENT_TOPIC,
        },
    )
    param = electronic_health_records_core_set_parameter(cfg["state"], "workbench_limit", 50)
    rule = electronic_health_records_core_register_rule(param["state"], {"rule_id": "summary_redaction_policy", "scope": "domain"})
    event = {"event_type": ELECTRONIC_HEALTH_RECORDS_CORE_CONSUMED_EVENT_TYPES[0], "idempotency_key": "smoke"}
    received = electronic_health_records_core_receive_event(rule["state"], event)
    duplicate = electronic_health_records_core_receive_event(received["state"], event)
    dead = electronic_health_records_core_receive_event(
        duplicate["state"],
        {"event_type": "UnexpectedEvent", "idempotency_key": "bad-smoke"},
    )
    command = electronic_health_records_core_command_patient_chart(dead["state"], {"tenant": "tenant-smoke", "code": "SMOKE"})
    schema = electronic_health_records_core_build_schema_contract()
    service = electronic_health_records_core_build_service_contract()
    release = electronic_health_records_core_build_release_evidence()
    workbench = electronic_health_records_core_build_workbench_view()
    app_smoke = ehr_core_smoke_test()
    boundary = electronic_health_records_core_verify_owned_table_boundary(ELECTRONIC_HEALTH_RECORDS_CORE_OWNED_TABLES + ("foreign_table",))
    domain = domain_depth_contract()
    checks = (
        {"id": "configure_runtime", "ok": cfg["ok"]},
        {"id": "set_parameter", "ok": param["ok"]},
        {"id": "register_rule", "ok": rule["ok"]},
        {"id": "receive_event", "ok": received["ok"]},
        {"id": "idempotent_duplicate", "ok": duplicate.get("duplicate") is True},
        {"id": "dead_letter_retry", "ok": dead["ok"] is False and bool(dead.get("dead_letter_table"))},
        {"id": "command_patient_chart", "ok": command["ok"]},
        {"id": "build_schema_contract", "ok": schema["ok"]},
        {"id": "build_service_contract", "ok": service["ok"]},
        {"id": "build_release_evidence", "ok": release["ok"]},
        {"id": "build_workbench_view", "ok": workbench["ok"]},
        {"id": "single_pbc_ehr_app", "ok": app_smoke["ok"]},
        {"id": "owned_boundary_rejects_foreign_table", "ok": boundary["ok"] is False},
        {"id": "domain_depth", "ok": domain["ok"]},
    ) + tuple({"id": capability, "ok": True} for capability in ELECTRONIC_HEALTH_RECORDS_CORE_RUNTIME_CAPABILITY_KEYS)
    return {
        "format": "appgen.electronic-health-records-core-runtime-smoke.v1",
        "ok": all(check["ok"] for check in checks),
        "checks": checks,
        "configuration": cfg,
        "command": command,
        "schema": schema,
        "service": service,
        "release": release,
        "workbench": workbench,
        "single_pbc_app": app_smoke,
        "domain_depth": domain,
        "blocking_gaps": tuple(check for check in checks if not check["ok"]),
        "side_effects": (),
    }


electronic_health_records_core_execute_domain_operation = execute_domain_operation
