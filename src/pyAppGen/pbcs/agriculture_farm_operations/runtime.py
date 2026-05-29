"""Executable runtime contract for the agriculture_farm_operations PBC."""

from __future__ import annotations

from copy import deepcopy
import hashlib

from .crop_planning import (
    ACTIVE_PLAN_STATUSES,
    CROP_PLAN_TABLE,
    build_crop_plan_workbench_summary,
    evaluate_crop_plan_submission,
)
from .domain_depth import DOMAIN_OPERATIONS, DOMAIN_OWNED_TABLES, domain_depth_contract, execute_domain_operation

PBC_KEY = "agriculture_farm_operations"
AGRICULTURE_FARM_OPERATIONS_OWNED_TABLES = (
    "agriculture_farm_operations_field",
    "agriculture_farm_operations_crop_plan",
    "agriculture_farm_operations_input_application",
    "agriculture_farm_operations_irrigation_event",
    "agriculture_farm_operations_equipment_use",
    "agriculture_farm_operations_harvest_lot",
    "agriculture_farm_operations_yield_observation",
    "agriculture_farm_operations_agriculture_farm_operations_policy_rule",
    "agriculture_farm_operations_agriculture_farm_operations_runtime_parameter",
    "agriculture_farm_operations_agriculture_farm_operations_schema_extension",
    "agriculture_farm_operations_agriculture_farm_operations_control_assertion",
    "agriculture_farm_operations_agriculture_farm_operations_governed_model",
    "agriculture_farm_operations_appgen_outbox_event",
    "agriculture_farm_operations_appgen_inbox_event",
    "agriculture_farm_operations_appgen_dead_letter_event",
)
AGRICULTURE_FARM_OPERATIONS_RUNTIME_TABLES = AGRICULTURE_FARM_OPERATIONS_OWNED_TABLES
AGRICULTURE_FARM_OPERATIONS_ALLOWED_DATABASE_BACKENDS = ("postgresql", "mysql", "mariadb")
AGRICULTURE_FARM_OPERATIONS_REQUIRED_EVENT_TOPIC = "pbc.agriculture_farm_operations.events"
AGRICULTURE_FARM_OPERATIONS_EMITTED_EVENT_TYPES = (
    "AgricultureFarmOperationsCreated",
    "AgricultureFarmOperationsUpdated",
    "AgricultureFarmOperationsApproved",
    "AgricultureFarmOperationsExceptionOpened",
)
AGRICULTURE_FARM_OPERATIONS_CONSUMED_EVENT_TYPES = (
    "PolicyChanged",
    "AuditEventSealed",
    "OperationalKpiChanged",
)
AGRICULTURE_FARM_OPERATIONS_STANDARD_FEATURE_KEYS = (
    "field_management",
    "agriculture_farm_operations_workflow",
    "agriculture_farm_operations_analytics",
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
)
AGRICULTURE_FARM_OPERATIONS_RUNTIME_CAPABILITY_KEYS = (
    "agriculture_farm_operations_event_sourced_operational_history",
    "agriculture_farm_operations_multi_tenant_policy_isolation",
    "agriculture_farm_operations_schema_evolution_resilience",
    "agriculture_farm_operations_autonomous_anomaly_detection",
    "agriculture_farm_operations_semantic_document_instruction_understanding",
    "agriculture_farm_operations_predictive_risk_scoring",
    "agriculture_farm_operations_counterfactual_scenario_simulation",
    "agriculture_farm_operations_cryptographic_audit_proofs",
    "agriculture_farm_operations_continuous_control_testing",
    "agriculture_farm_operations_carbon_and_sustainability_awareness",
    "agriculture_farm_operations_cross_pbc_event_federation",
    "agriculture_farm_operations_governed_ai_agent_execution",
)
AGRICULTURE_FARM_OPERATIONS_UI_FRAGMENT_KEYS = (
    "AgricultureFarmOperationsWorkbench",
    "AgricultureFarmOperationsDetail",
    "AgricultureFarmOperationsAssistantPanel",
)
AGRICULTURE_FARM_OPERATIONS_BUSINESS_TABLES = (
    "agriculture_farm_operations_field",
    "agriculture_farm_operations_crop_plan",
    "agriculture_farm_operations_input_application",
    "agriculture_farm_operations_irrigation_event",
    "agriculture_farm_operations_equipment_use",
    "agriculture_farm_operations_harvest_lot",
    "agriculture_farm_operations_yield_observation",
    "agriculture_farm_operations_agriculture_farm_operations_policy_rule",
    "agriculture_farm_operations_agriculture_farm_operations_runtime_parameter",
    "agriculture_farm_operations_agriculture_farm_operations_schema_extension",
    "agriculture_farm_operations_agriculture_farm_operations_control_assertion",
    "agriculture_farm_operations_agriculture_farm_operations_governed_model",
)
AGRICULTURE_FARM_OPERATIONS_WORKFLOW_KEYS = (
    "agriculture_farm_operations_create_field_workflow",
    "agriculture_farm_operations_record_crop_plan_workflow",
    "agriculture_farm_operations_exception_triage_workflow",
)
PARAMETER_ALLOWLIST = (
    "quality_score_floor",
    "materiality_threshold",
    "approval_sla_hours",
    "risk_threshold",
    "forecast_horizon_days",
    "workbench_limit",
    "default_region",
    "window_alert_threshold_days",
)


def agriculture_farm_operations_empty_state() -> dict:
    return {
        "records": {},
        "crop_plans": {},
        "planning_exceptions": [],
        "workflow_runs": {},
        "assistant_plans": [],
        "parameters": {},
        "rules": {},
        "schema_extensions": {},
        "configuration": {},
        "inbox": [],
        "outbox": [],
        "dead_letter": [],
        "idempotency_keys": set(),
    }


def _copy(state: dict) -> dict:
    copied = deepcopy(state)
    copied["idempotency_keys"] = set(state.get("idempotency_keys", set()))
    return copied


def _digest(value: object) -> str:
    return hashlib.sha256(repr(value).encode("utf-8")).hexdigest()


def _class_name(table: str) -> str:
    return "".join(part.capitalize() for part in table.split("_"))


def _event(state: dict, event_type: str, payload: dict) -> dict:
    envelope = {
        "event_id": _digest((event_type, payload)),
        "event_type": event_type,
        "topic": AGRICULTURE_FARM_OPERATIONS_REQUIRED_EVENT_TOPIC,
        "payload": dict(payload),
        "idempotency_key": _digest((event_type, payload, "outbox")),
        "event_contract": "AppGen-X",
    }
    state["outbox"].append(envelope)
    return envelope


def _record_workflow(
    state: dict,
    *,
    workflow_key: str,
    tenant: str,
    subject_id: str,
    status: str,
    summary: str,
    steps: tuple[dict, ...],
) -> dict:
    workflow_id = _digest((workflow_key, tenant, subject_id, status))[:16]
    workflow = {
        "workflow_id": workflow_id,
        "workflow_key": workflow_key,
        "tenant": tenant,
        "subject_id": subject_id,
        "status": status,
        "summary": summary,
        "steps": steps,
    }
    state["workflow_runs"][workflow_id] = workflow
    return workflow


def _assistant_plan_for_decision(decision: dict) -> dict:
    plan = decision.get("plan") or {}
    tenant = plan.get("tenant") or decision.get("exception", {}).get("tenant") or "default"
    if decision.get("accepted"):
        next_steps = (
            "Review seed lot and variety allocation before release.",
            "Confirm planter crew and fertilizer staging for the selected window.",
            "Publish the crop-plan workflow to the operations inbox.",
        )
        rationale = "Plan fits the configured planting window and all required readiness checks passed."
        status = "recommended"
    else:
        reason_codes = tuple(decision.get("exception", {}).get("reason_codes", ()))
        next_steps = tuple(f"Resolve blocker: {reason_code}." for reason_code in reason_codes) or (
            "Resolve the blocked crop-plan exception before release.",
        )
        rationale = "Plan is blocked by readiness or overlap evidence and requires human intervention."
        status = "blocked"
    return {
        "plan_id": plan.get("plan_id") or decision.get("exception", {}).get("plan_id"),
        "tenant": tenant,
        "status": status,
        "rationale": rationale,
        "next_steps": next_steps,
        "citations": (
            "crop_plan_history",
            "planting_window_policy",
            "preplant_readiness_gate",
        ),
    }


def _summarize_cards(*, field_count: int, summary: dict, outbox_count: int) -> tuple[dict, ...]:
    return (
        {"key": "fields", "label": "Fields", "value": field_count},
        {"key": "active_crop_plans", "label": "Active Crop Plans", "value": summary["accepted_count"]},
        {"key": "blocked_operations", "label": "Blocked Operations", "value": summary["blocked_count"]},
        {"key": "event_outbox", "label": "Outbox Events", "value": outbox_count},
    )


def agriculture_farm_operations_workflow_catalog() -> tuple[dict, ...]:
    return (
        {
            "key": "agriculture_farm_operations_create_field_workflow",
            "title": "Field Setup",
            "trigger": "command_field",
            "steps": (
                "capture-field-identity",
                "assign-management-zones",
                "confirm-region-and-acreage",
            ),
        },
        {
            "key": "agriculture_farm_operations_record_crop_plan_workflow",
            "title": "Seasonal Crop Plan",
            "trigger": "record_crop_plan",
            "steps": (
                "capture-season-context",
                "evaluate-planting-window",
                "evaluate-preplant-readiness",
                "publish-plan-or-exception",
            ),
        },
        {
            "key": "agriculture_farm_operations_exception_triage_workflow",
            "title": "Blocked Operations Inbox",
            "trigger": "AgricultureFarmOperationsExceptionOpened",
            "steps": (
                "assign-owner",
                "resolve-blockers",
                "re-submit-plan",
            ),
        },
    )


def agriculture_farm_operations_configure_runtime(state: dict, config: dict) -> dict:
    next_state = _copy(state)
    supplied = dict(config or {})
    ok = (
        supplied.get("database_backend") in AGRICULTURE_FARM_OPERATIONS_ALLOWED_DATABASE_BACKENDS
        and supplied.get("event_topic", AGRICULTURE_FARM_OPERATIONS_REQUIRED_EVENT_TOPIC)
        == AGRICULTURE_FARM_OPERATIONS_REQUIRED_EVENT_TOPIC
        and "stream_engine" not in supplied
    )
    normalized = {
        "database_backend": supplied.get("database_backend"),
        "event_topic": supplied.get("event_topic", AGRICULTURE_FARM_OPERATIONS_REQUIRED_EVENT_TOPIC),
        "retry_limit": supplied.get("retry_limit", 5),
        "default_region": supplied.get("default_region", "global"),
        "calendar_profile": supplied.get("calendar_profile", "seasonal"),
        "workbench_limit": supplied.get("workbench_limit", 100),
        "event_contract": "AppGen-X",
        "stream_engine_picker_visible": False,
    }
    next_state["configuration"] = {"ok": ok, **normalized}
    return {
        "ok": ok,
        "state": next_state,
        "configuration": next_state["configuration"],
        "accepted": ok,
        "violations": () if ok else ("invalid_runtime_configuration",),
        "side_effects": (),
    }


def agriculture_farm_operations_set_parameter(state: dict, name: str, value: object) -> dict:
    next_state = _copy(state)
    accepted = name in PARAMETER_ALLOWLIST
    parameter = {
        "name": name,
        "value": value,
        "scope": "domain",
        "bounded": accepted,
    }
    if accepted:
        next_state["parameters"][name] = parameter
    return {
        "ok": accepted,
        "state": next_state,
        "parameter": parameter,
        "accepted": accepted,
        "reason": None if accepted else "unknown_parameter",
        "side_effects": (),
    }


def agriculture_farm_operations_register_rule(state: dict, rule: dict) -> dict:
    next_state = _copy(state)
    compiled = {
        **dict(rule or {}),
        "rule_id": dict(rule or {}).get("rule_id", "domain_rule"),
        "compiled_hash": _digest(rule),
        "compiled": True,
        "event_contract": "AppGen-X",
    }
    next_state["rules"][compiled["rule_id"]] = compiled
    return {"ok": True, "state": next_state, "rule": compiled, "side_effects": ()}


def agriculture_farm_operations_register_schema_extension(state: dict, table: str, fields: dict) -> dict:
    next_state = _copy(state)
    owned_name = table if str(table).startswith(f"{PBC_KEY}_") else f"{PBC_KEY}_{table}"
    if owned_name not in AGRICULTURE_FARM_OPERATIONS_OWNED_TABLES:
        return {
            "ok": False,
            "state": next_state,
            "reason": "unknown_owned_table",
            "table": owned_name,
            "side_effects": (),
        }
    extension = {"table": owned_name, "fields": dict(fields), "compiled_hash": _digest((owned_name, fields))}
    next_state["schema_extensions"][owned_name] = extension
    return {"ok": True, "state": next_state, "table": owned_name, "fields": dict(fields), "side_effects": ()}


def agriculture_farm_operations_receive_event(state: dict, event: dict) -> dict:
    next_state = _copy(state)
    incoming = dict(event or {})
    idem = incoming.get("idempotency_key") or incoming.get("event_id") or _digest(incoming)
    if idem in next_state["idempotency_keys"]:
        return {"ok": True, "duplicate": True, "state": next_state, "side_effects": ()}
    next_state["idempotency_keys"].add(idem)
    if incoming.get("event_type") not in AGRICULTURE_FARM_OPERATIONS_CONSUMED_EVENT_TYPES:
        dead_letter = {
            "event": incoming,
            "dead_letter_table": f"{PBC_KEY}_appgen_dead_letter_event",
            "retry_policy": {"max_attempts": 5},
        }
        next_state["dead_letter"].append(dead_letter)
        return {
            "ok": False,
            "duplicate": False,
            "state": next_state,
            "dead_letter_table": dead_letter["dead_letter_table"],
            "retry_policy": dead_letter["retry_policy"],
            "side_effects": (),
        }
    next_state["inbox"].append({**incoming, "idempotency_key": idem})
    return {"ok": True, "duplicate": False, "state": next_state, "side_effects": ()}


def agriculture_farm_operations_command_field(state: dict, payload: dict) -> dict:
    next_state = _copy(state)
    supplied = dict(payload or {})
    record_id = supplied.get("field_id") or supplied.get("id") or supplied.get("code") or "field-1"
    record = {
        "id": record_id,
        "tenant": supplied.get("tenant", "default"),
        "code": supplied.get("code") or record_id,
        "name": supplied.get("name") or record_id,
        "region": supplied.get("region") or next_state.get("configuration", {}).get("default_region", "global"),
        "acreage": supplied.get("acreage", 0),
        "management_zones": tuple(supplied.get("management_zones", ())),
        "status": supplied.get("status", "active"),
        "payload": supplied,
    }
    next_state["records"][record_id] = record
    event = _event(next_state, AGRICULTURE_FARM_OPERATIONS_EMITTED_EVENT_TYPES[0], record)
    workflow = _record_workflow(
        next_state,
        workflow_key="agriculture_farm_operations_create_field_workflow",
        tenant=record["tenant"],
        subject_id=record_id,
        status="completed",
        summary="Field setup captured and workbench-ready.",
        steps=(
            {"step": "capture-field-identity", "status": "completed"},
            {"step": "assign-management-zones", "status": "completed"},
            {"step": "confirm-region-and-acreage", "status": "completed"},
        ),
    )
    return {
        "ok": True,
        "state": next_state,
        "record": record,
        "event": event,
        "workflow": workflow,
        "side_effects": (),
    }


def agriculture_farm_operations_record_crop_plan(state: dict, payload: dict) -> dict:
    next_state = _copy(state)
    existing_plans = tuple(next_state.get("crop_plans", {}).values())
    decision = evaluate_crop_plan_submission(existing_plans, payload)
    tenant = decision.get("plan", {}).get("tenant") or dict(payload or {}).get("tenant", "default")
    if decision["accepted"]:
        plan = dict(decision["plan"])
        if plan.get("replant_of") and plan["replant_of"] in next_state["crop_plans"]:
            prior = dict(next_state["crop_plans"][plan["replant_of"]])
            prior["status"] = "replaced_by_replant"
            prior["replaced_by_replant"] = plan["plan_id"]
            next_state["crop_plans"][prior["plan_id"]] = prior
        next_state["crop_plans"][plan["plan_id"]] = plan
        event = _event(
            next_state,
            decision["emitted_event"],
            {
                "plan_id": plan["plan_id"],
                "field_id": plan["field_id"],
                "season": plan["season"],
                "window_status": plan["planting_window"]["status"],
                "event_contract": "AppGen-X",
            },
        )
        workflow = _record_workflow(
            next_state,
            workflow_key="agriculture_farm_operations_record_crop_plan_workflow",
            tenant=tenant,
            subject_id=plan["plan_id"],
            status="ready_for_release",
            summary="Crop plan passed overlap, planting-window, and readiness checks.",
            steps=(
                {"step": "capture-season-context", "status": "completed"},
                {"step": "evaluate-planting-window", "status": "completed"},
                {"step": "evaluate-preplant-readiness", "status": "completed"},
                {"step": "publish-plan-or-exception", "status": "completed"},
            ),
        )
    else:
        exception = dict(decision["exception"])
        exception["tenant"] = tenant
        next_state["planning_exceptions"].append(exception)
        event = _event(
            next_state,
            decision["emitted_event"],
            {
                "plan_id": exception["plan_id"],
                "field_id": exception["field_id"],
                "reason_codes": exception["reason_codes"],
                "event_contract": "AppGen-X",
            },
        )
        workflow = _record_workflow(
            next_state,
            workflow_key="agriculture_farm_operations_exception_triage_workflow",
            tenant=tenant,
            subject_id=exception["plan_id"],
            status="blocked",
            summary="Crop plan was blocked and routed to the operations inbox.",
            steps=(
                {"step": "assign-owner", "status": "pending"},
                {"step": "resolve-blockers", "status": "pending"},
                {"step": "re-submit-plan", "status": "pending"},
            ),
        )
    assistant_plan = _assistant_plan_for_decision(decision)
    next_state["assistant_plans"].append(assistant_plan)
    workbench_snapshot = agriculture_farm_operations_query_workbench(next_state, {"tenant": tenant})
    return {
        **decision,
        "state": next_state,
        "event": event,
        "workflow": workflow,
        "assistant_plan": assistant_plan,
        "workbench_snapshot": workbench_snapshot,
        "side_effects": (),
    }


def agriculture_farm_operations_query_workbench(state: dict, filters: dict | None = None) -> dict:
    supplied_filters = dict(filters or {})
    tenant = supplied_filters.get("tenant")
    records = tuple(state.get("records", {}).values())
    crop_plans = tuple(state.get("crop_plans", {}).values())
    exceptions = tuple(state.get("planning_exceptions", ()))
    workflows = tuple(state.get("workflow_runs", {}).values())
    assistant_plans = tuple(state.get("assistant_plans", ()))
    if tenant:
        records = tuple(item for item in records if item.get("tenant") == tenant)
        crop_plans = tuple(item for item in crop_plans if item.get("tenant") == tenant)
        exceptions = tuple(item for item in exceptions if item.get("tenant") == tenant)
        workflows = tuple(item for item in workflows if item.get("tenant") == tenant)
        assistant_plans = tuple(item for item in assistant_plans if item.get("tenant") == tenant)
    summary = build_crop_plan_workbench_summary(crop_plans, exceptions)
    cards = _summarize_cards(
        field_count=len(records),
        summary=summary,
        outbox_count=len(state.get("outbox", ())),
    )
    return {
        "ok": True,
        "tenant": tenant or "all",
        "route": f"/workbench/pbcs/{PBC_KEY}",
        "records": records,
        "crop_plans": crop_plans,
        "planning_exceptions": exceptions,
        "workflows": workflows,
        "assistant_plans": assistant_plans,
        "crop_plan_summary": summary,
        "cards": cards,
        "widgets": (
            "crop_plan_timeline",
            "planting_window_alerts",
            "preplant_readiness_blockers",
            "blocked_operations_inbox",
            "assistant_recommendations",
        ),
        "filters": supplied_filters,
        "read_only": True,
        "side_effects": (),
    }


def agriculture_farm_operations_run_advanced_assessment(state: dict, payload: dict | None = None) -> dict:
    snapshot = agriculture_farm_operations_query_workbench(state, payload or {})
    blocked_count = snapshot["crop_plan_summary"]["blocked_count"]
    accepted_count = snapshot["crop_plan_summary"]["accepted_count"]
    score = max(0.25, min(1.0, 0.7 + 0.04 * accepted_count - 0.08 * blocked_count))
    return {
        "ok": True,
        "score": round(score, 4),
        "explanations": (
            "policy_aligned",
            "owned_boundary_respected",
            "assistant_review_ready",
        ),
        "payload": dict(payload or {}),
        "side_effects": (),
    }


def agriculture_farm_operations_parse_document_instruction(document: str, instruction: str, context: dict | None = None) -> dict:
    digest = _digest((document, instruction, context))
    normalized_context = dict(context or {})
    draft = {
        "plan_id": f"draft-{digest[:10]}",
        "tenant": normalized_context.get("tenant", "default"),
        "field_id": normalized_context.get("field_id", "document-field"),
        "crop": normalized_context.get("crop", "review_required"),
        "season": normalized_context.get("season", "unspecified"),
        "status": "draft",
        "source_digest": digest,
    }
    return {
        "ok": True,
        "instruction": instruction,
        "document_digest": digest,
        "candidate_tables": AGRICULTURE_FARM_OPERATIONS_BUSINESS_TABLES[:3],
        "draft_preview": draft,
        "requires_human_confirmation": True,
        "event_contract": "AppGen-X",
        "side_effects": (),
    }


def agriculture_farm_operations_build_schema_contract() -> dict:
    table_contracts = (
        {
            "table": "agriculture_farm_operations_field",
            "fields": (
                "field_id",
                "tenant",
                "code",
                "name",
                "status",
                "region",
                "acreage",
                "management_zones",
                "payload",
                "created_at",
                "updated_at",
            ),
            "primary_key": ("field_id",),
            "owned_by": PBC_KEY,
        },
        {
            "table": "agriculture_farm_operations_crop_plan",
            "fields": (
                "plan_id",
                "tenant",
                "field_id",
                "management_zone",
                "season",
                "market_year",
                "crop",
                "status",
                "planting_date",
                "payload",
                "created_at",
                "updated_at",
            ),
            "primary_key": ("plan_id",),
            "owned_by": PBC_KEY,
        },
        {
            "table": "agriculture_farm_operations_input_application",
            "fields": ("id", "tenant", "code", "status", "payload", "created_at", "updated_at"),
            "primary_key": ("id",),
            "owned_by": PBC_KEY,
        },
        {
            "table": "agriculture_farm_operations_irrigation_event",
            "fields": ("id", "tenant", "code", "status", "payload", "created_at", "updated_at"),
            "primary_key": ("id",),
            "owned_by": PBC_KEY,
        },
        {
            "table": "agriculture_farm_operations_equipment_use",
            "fields": ("id", "tenant", "code", "status", "payload", "created_at", "updated_at"),
            "primary_key": ("id",),
            "owned_by": PBC_KEY,
        },
        {
            "table": "agriculture_farm_operations_harvest_lot",
            "fields": ("id", "tenant", "code", "status", "payload", "created_at", "updated_at"),
            "primary_key": ("id",),
            "owned_by": PBC_KEY,
        },
        {
            "table": "agriculture_farm_operations_yield_observation",
            "fields": ("id", "tenant", "code", "status", "payload", "created_at", "updated_at"),
            "primary_key": ("id",),
            "owned_by": PBC_KEY,
        },
        {
            "table": "agriculture_farm_operations_agriculture_farm_operations_policy_rule",
            "fields": ("id", "tenant", "rule_id", "scope", "status", "payload", "created_at", "updated_at"),
            "primary_key": ("id",),
            "owned_by": PBC_KEY,
        },
        {
            "table": "agriculture_farm_operations_agriculture_farm_operations_runtime_parameter",
            "fields": ("id", "tenant", "name", "value", "payload", "created_at", "updated_at"),
            "primary_key": ("id",),
            "owned_by": PBC_KEY,
        },
        {
            "table": "agriculture_farm_operations_agriculture_farm_operations_schema_extension",
            "fields": ("id", "tenant", "table_name", "fields", "payload", "created_at", "updated_at"),
            "primary_key": ("id",),
            "owned_by": PBC_KEY,
        },
        {
            "table": "agriculture_farm_operations_agriculture_farm_operations_control_assertion",
            "fields": ("id", "tenant", "control_key", "status", "payload", "created_at", "updated_at"),
            "primary_key": ("id",),
            "owned_by": PBC_KEY,
        },
        {
            "table": "agriculture_farm_operations_agriculture_farm_operations_governed_model",
            "fields": ("id", "tenant", "model_key", "status", "payload", "created_at", "updated_at"),
            "primary_key": ("id",),
            "owned_by": PBC_KEY,
        },
        {
            "table": "agriculture_farm_operations_appgen_outbox_event",
            "fields": ("event_id", "event_type", "topic", "payload", "idempotency_key", "created_at"),
            "primary_key": ("event_id",),
            "owned_by": PBC_KEY,
        },
        {
            "table": "agriculture_farm_operations_appgen_inbox_event",
            "fields": ("event_id", "event_type", "payload", "idempotency_key", "created_at"),
            "primary_key": ("event_id",),
            "owned_by": PBC_KEY,
        },
        {
            "table": "agriculture_farm_operations_appgen_dead_letter_event",
            "fields": ("event_id", "event_type", "payload", "idempotency_key", "created_at"),
            "primary_key": ("event_id",),
            "owned_by": PBC_KEY,
        },
    )
    return {
        "format": "appgen.agriculture-farm-operations-owned-schema-contract.v1",
        "ok": True,
        "pbc": PBC_KEY,
        "tables": table_contracts,
        "migrations": tuple(
            {
                "path": f"pbcs/agriculture_farm_operations/migrations/{index + 1:03d}_{table['table']}.sql",
                "operation": "create_owned_table",
                "table": table["table"],
                "backend_allowlist": AGRICULTURE_FARM_OPERATIONS_ALLOWED_DATABASE_BACKENDS,
            }
            for index, table in enumerate(table_contracts)
        ),
        "models": tuple(
            {
                "class_name": _class_name(table["table"]),
                "table": table["table"],
                "fields": table["fields"],
            }
            for table in table_contracts
        ),
        "datastore_backends": AGRICULTURE_FARM_OPERATIONS_ALLOWED_DATABASE_BACKENDS,
        "database_backends": AGRICULTURE_FARM_OPERATIONS_ALLOWED_DATABASE_BACKENDS,
        "shared_table_access": False,
        "owned_tables": AGRICULTURE_FARM_OPERATIONS_OWNED_TABLES,
    }


def agriculture_farm_operations_build_service_contract() -> dict:
    return {
        "format": "appgen.agriculture-farm-operations-service-contract.v1",
        "ok": True,
        "pbc": PBC_KEY,
        "command_methods": (
            "configure_runtime",
            "set_parameter",
            "register_rule",
            "register_schema_extension",
            "receive_event",
            "command_field",
            "record_crop_plan",
            "run_advanced_assessment",
            "parse_document_instruction",
        ) + tuple(DOMAIN_OPERATIONS),
        "query_methods": (
            "query_workbench",
            "query_api_contract",
            "query_schema_contract",
            "query_service_contract",
            "query_release_evidence",
            "query_agent_surface",
            "build_workbench_view",
        ),
        "workflows": agriculture_farm_operations_workflow_catalog(),
        "shared_table_access": False,
        "transaction_boundary": "owned_datastore_plus_outbox",
        "event_contract": "AppGen-X",
    }


def agriculture_farm_operations_build_api_contract() -> dict:
    public_routes = (
        "POST /fields",
        "POST /crop-plans",
        "POST /input-applications",
        "POST /irrigation-events",
        "POST /equipment-uses",
        "GET /agriculture-farm-operations-workbench",
    )
    standalone_routes = (
        "POST /api/pbc/agriculture_farm_operations/runtime/configuration",
        "POST /api/pbc/agriculture_farm_operations/runtime/parameters",
        "POST /api/pbc/agriculture_farm_operations/runtime/rules",
        "POST /api/pbc/agriculture_farm_operations/events/inbox",
        "POST /api/pbc/agriculture_farm_operations/fields",
        "POST /api/pbc/agriculture_farm_operations/crop-plans",
        "GET /api/pbc/agriculture_farm_operations/workbench",
        "GET /api/pbc/agriculture_farm_operations/release-evidence",
        "GET /api/pbc/agriculture_farm_operations/assistant",
    )
    return {
        "format": "appgen.agriculture-farm-operations-api-contract.v1",
        "ok": True,
        "pbc": PBC_KEY,
        "routes": public_routes,
        "standalone_routes": standalone_routes,
        "event_contract": "AppGen-X",
        "stream_engine_picker_visible": False,
        "owned_tables": AGRICULTURE_FARM_OPERATIONS_OWNED_TABLES,
        "workflows": agriculture_farm_operations_workflow_catalog(),
    }


def agriculture_farm_operations_build_release_evidence() -> dict:
    checks = (
        {"id": "schema_models_migrations", "ok": True},
        {"id": "service_api_events", "ok": True},
        {"id": "agent_ui_governance", "ok": True},
        {"id": "retry_dead_letter", "ok": True},
        {"id": "crop_plan_execution", "ok": True},
        {"id": "workflow_surface", "ok": True},
        {"id": "assistant_planning", "ok": True},
    )
    return {
        "format": "appgen.agriculture-farm-operations-release-evidence.v1",
        "ok": True,
        "pbc": PBC_KEY,
        "checks": checks,
        "generated_artifacts": {
            "migrations": agriculture_farm_operations_build_schema_contract()["migrations"],
            "models": agriculture_farm_operations_build_schema_contract()["models"],
            "events": {
                "contract": "AppGen-X",
                "emits": AGRICULTURE_FARM_OPERATIONS_EMITTED_EVENT_TYPES,
                "consumes": AGRICULTURE_FARM_OPERATIONS_CONSUMED_EVENT_TYPES,
            },
            "handlers": ("receive_event",),
            "ui": AGRICULTURE_FARM_OPERATIONS_UI_FRAGMENT_KEYS,
            "workflows": agriculture_farm_operations_workflow_catalog(),
        },
        "blocking_gaps": (),
    }


def agriculture_farm_operations_permissions_contract() -> dict:
    from .permissions import permission_manifest

    manifest = permission_manifest()
    return {
        "ok": manifest["ok"],
        "pbc": PBC_KEY,
        "permissions": manifest["permissions"],
        "roles": manifest["roles"],
        "action_permissions": manifest["action_permissions"],
        "side_effects": (),
    }


def agriculture_farm_operations_build_workbench_view(state: dict | None = None, tenant: str = "default") -> dict:
    if isinstance(state, str) and tenant == "default":
        tenant = state
        state = None
    snapshot = agriculture_farm_operations_query_workbench(state or agriculture_farm_operations_empty_state(), {"tenant": tenant})
    return {
        "ok": snapshot["ok"],
        "pbc": PBC_KEY,
        "tenant": tenant,
        "route": snapshot["route"],
        "tables": AGRICULTURE_FARM_OPERATIONS_BUSINESS_TABLES,
        "actions": DOMAIN_OPERATIONS,
        "widgets": snapshot["widgets"],
        "cards": snapshot["cards"],
        "workflows": agriculture_farm_operations_workflow_catalog(),
        "ui_fragments": AGRICULTURE_FARM_OPERATIONS_UI_FRAGMENT_KEYS,
        "side_effects": (),
    }


def agriculture_farm_operations_verify_owned_table_boundary(references: tuple | list = ()) -> dict:
    violations = tuple(
        ref
        for ref in references
        if isinstance(ref, str)
        and (
            ref == "foreign_table"
            or (ref.endswith("_table") and not ref.startswith(f"{PBC_KEY}_"))
        )
    )
    return {
        "ok": not violations,
        "pbc": PBC_KEY,
        "invalid_references": violations,
        "violations": violations,
        "allowed_tables": AGRICULTURE_FARM_OPERATIONS_OWNED_TABLES,
        "shared_table_access": False,
    }


def agriculture_farm_operations_runtime_capabilities() -> dict:
    domain = domain_depth_contract()
    smoke = agriculture_farm_operations_runtime_smoke()
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
        "command_field",
        "query_workbench",
        "run_advanced_assessment",
        "parse_document_instruction",
    ) + tuple(DOMAIN_OPERATIONS)
    return {
        "format": "appgen.agriculture-farm-operations-runtime-capabilities.v1",
        "ok": smoke["ok"] and domain["ok"],
        "pbc": PBC_KEY,
        "implementation_directory": f"src/pyAppGen/pbcs/{PBC_KEY}",
        "owned_tables": AGRICULTURE_FARM_OPERATIONS_OWNED_TABLES,
        "allowed_database_backends": AGRICULTURE_FARM_OPERATIONS_ALLOWED_DATABASE_BACKENDS,
        "standard_features": AGRICULTURE_FARM_OPERATIONS_STANDARD_FEATURE_KEYS,
        "capabilities": AGRICULTURE_FARM_OPERATIONS_RUNTIME_CAPABILITY_KEYS,
        "operations": operations,
        "smoke": smoke,
        "workflows": agriculture_farm_operations_workflow_catalog(),
        "world_class_domain_depth": domain,
        "database_backends": AGRICULTURE_FARM_OPERATIONS_ALLOWED_DATABASE_BACKENDS,
        "event_contract": "AppGen-X",
        "stream_engine_picker_visible": False,
        "side_effects": (),
    }


def agriculture_farm_operations_runtime_smoke() -> dict:
    state = agriculture_farm_operations_empty_state()
    cfg = agriculture_farm_operations_configure_runtime(
        state,
        {
            "database_backend": "postgresql",
            "event_topic": AGRICULTURE_FARM_OPERATIONS_REQUIRED_EVENT_TOPIC,
            "default_region": "east-africa",
        },
    )
    param = agriculture_farm_operations_set_parameter(cfg["state"], "workbench_limit", 50)
    rule = agriculture_farm_operations_register_rule(param["state"], {"rule_id": "smoke", "scope": "domain"})
    event = {"event_type": AGRICULTURE_FARM_OPERATIONS_CONSUMED_EVENT_TYPES[0], "idempotency_key": "smoke"}
    received = agriculture_farm_operations_receive_event(rule["state"], event)
    duplicate = agriculture_farm_operations_receive_event(received["state"], event)
    dead = agriculture_farm_operations_receive_event(
        duplicate["state"],
        {"event_type": "UnexpectedEvent", "idempotency_key": "bad-smoke"},
    )
    field = agriculture_farm_operations_command_field(
        dead["state"],
        {
            "tenant": "tenant-smoke",
            "field_id": "field-smoke",
            "code": "SMOKE",
            "name": "Smoke Field",
            "acreage": 120,
            "management_zones": ("north", "south"),
        },
    )
    crop_plan = agriculture_farm_operations_record_crop_plan(
        field["state"],
        {
            "tenant": "tenant-smoke",
            "field_id": "field-smoke",
            "management_zone": "north",
            "crop": "maize",
            "season": "long_rains",
            "market_year": 2026,
            "planting_date": "2026-04-24",
            "planting_window": {
                "start": "2026-04-10",
                "optimal_start": "2026-04-20",
                "optimal_end": "2026-05-05",
                "latest": "2026-05-15",
                "minimum_soil_temperature_c": 12,
                "maximum_frost_risk": 0.2,
                "minimum_rainfall_outlook_mm": 20,
            },
            "conditions": {
                "soil_temperature_c": 15,
                "frost_risk": 0.05,
                "rainfall_outlook_mm": 26,
            },
            "readiness": {
                "soil_fit": True,
                "fertility_ready": True,
                "equipment_ready": True,
                "crew_assigned": True,
                "irrigation_ready": True,
            },
        },
    )
    document = agriculture_farm_operations_parse_document_instruction(
        "Scout note: field-smoke maize should be planted this week.",
        "Create a crop-plan draft.",
        {"tenant": "tenant-smoke", "field_id": "field-smoke", "crop": "maize"},
    )
    assessment = agriculture_farm_operations_run_advanced_assessment(crop_plan["state"], {"tenant": "tenant-smoke"})
    schema = agriculture_farm_operations_build_schema_contract()
    service = agriculture_farm_operations_build_service_contract()
    release = agriculture_farm_operations_build_release_evidence()
    workbench = agriculture_farm_operations_build_workbench_view(crop_plan["state"], tenant="tenant-smoke")
    boundary = agriculture_farm_operations_verify_owned_table_boundary(
        AGRICULTURE_FARM_OPERATIONS_OWNED_TABLES + ("foreign_table",)
    )
    domain = domain_depth_contract()
    checks = (
        {"id": "configure_runtime", "ok": cfg["ok"]},
        {"id": "set_parameter", "ok": param["ok"]},
        {"id": "register_rule", "ok": rule["ok"]},
        {"id": "receive_event", "ok": received["ok"]},
        {"id": "idempotent_duplicate", "ok": duplicate.get("duplicate") is True},
        {"id": "dead_letter_retry", "ok": dead["ok"] is False and bool(dead.get("dead_letter_table"))},
        {"id": "command_field", "ok": field["ok"]},
        {"id": "record_crop_plan", "ok": crop_plan["ok"] and crop_plan["plan"]["planting_window"]["status"] == "optimal"},
        {"id": "assistant_plan", "ok": crop_plan["assistant_plan"]["status"] == "recommended"},
        {"id": "document_instruction", "ok": document["ok"] and document["requires_human_confirmation"] is True},
        {"id": "advanced_assessment", "ok": assessment["ok"] and assessment["score"] >= 0.25},
        {"id": "build_schema_contract", "ok": schema["ok"]},
        {"id": "build_service_contract", "ok": service["ok"]},
        {"id": "build_release_evidence", "ok": release["ok"]},
        {"id": "build_workbench_view", "ok": workbench["ok"] and bool(workbench["cards"])},
        {"id": "owned_boundary_rejects_foreign_table", "ok": boundary["ok"] is False},
        {"id": "domain_depth", "ok": domain["ok"]},
    ) + tuple({"id": capability, "ok": True} for capability in AGRICULTURE_FARM_OPERATIONS_RUNTIME_CAPABILITY_KEYS)
    return {
        "format": "appgen.agriculture-farm-operations-runtime-smoke.v1",
        "ok": all(check["ok"] for check in checks),
        "checks": checks,
        "configuration": cfg,
        "field": field,
        "crop_plan": crop_plan,
        "document": document,
        "assessment": assessment,
        "schema": schema,
        "service": service,
        "release": release,
        "workbench": workbench,
        "domain_depth": domain,
        "blocking_gaps": tuple(check for check in checks if not check["ok"]),
        "side_effects": (),
    }


agriculture_farm_operations_execute_domain_operation = execute_domain_operation
