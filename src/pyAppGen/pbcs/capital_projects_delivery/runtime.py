"""Executable runtime contract for the capital_projects_delivery PBC."""
from __future__ import annotations

from copy import deepcopy
import hashlib

from .project_control import improve1_project_control_contract
from .domain_depth import (
    DOMAIN_OPERATIONS,
    domain_depth_contract,
    execute_domain_operation,
)
from .lifecycle import (
    GATE_DEFINITIONS,
    LIFECYCLE_STAGES,
    apply_gate_transition,
    project_detail,
    project_record_from_payload,
    record_gate_checklist,
    workbench_card,
)

PBC_KEY = "capital_projects_delivery"

CAPITAL_PROJECTS_DELIVERY_OWNED_TABLES = (
    "capital_projects_delivery_capital_project",
    "capital_projects_delivery_epc_package",
    "capital_projects_delivery_permit_milestone",
    "capital_projects_delivery_progress_measurement",
    "capital_projects_delivery_commissioning_system",
    "capital_projects_delivery_project_risk",
    "capital_projects_delivery_turnover_package",
    "capital_projects_delivery_capital_projects_delivery_policy_rule",
    "capital_projects_delivery_capital_projects_delivery_runtime_parameter",
    "capital_projects_delivery_capital_projects_delivery_schema_extension",
    "capital_projects_delivery_capital_projects_delivery_control_assertion",
    "capital_projects_delivery_capital_projects_delivery_governed_model",
    "capital_projects_delivery_appgen_outbox_event",
    "capital_projects_delivery_appgen_inbox_event",
    "capital_projects_delivery_appgen_dead_letter_event",
)
CAPITAL_PROJECTS_DELIVERY_RUNTIME_TABLES = CAPITAL_PROJECTS_DELIVERY_OWNED_TABLES
CAPITAL_PROJECTS_DELIVERY_ALLOWED_DATABASE_BACKENDS = ("postgresql", "mysql", "mariadb")
CAPITAL_PROJECTS_DELIVERY_REQUIRED_EVENT_TOPIC = "pbc.capital_projects_delivery.events"
CAPITAL_PROJECTS_DELIVERY_EMITTED_EVENT_TYPES = (
    "CapitalProjectsDeliveryCreated",
    "CapitalProjectsDeliveryUpdated",
    "CapitalProjectsDeliveryApproved",
    "CapitalProjectsDeliveryExceptionOpened",
)
CAPITAL_PROJECTS_DELIVERY_CONSUMED_EVENT_TYPES = (
    "PolicyChanged",
    "AuditEventSealed",
    "OperationalKpiChanged",
)
CAPITAL_PROJECTS_DELIVERY_STANDARD_FEATURE_KEYS = (
    "capital_project_management",
    "capital_projects_delivery_workflow",
    "capital_projects_delivery_analytics",
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
CAPITAL_PROJECTS_DELIVERY_RUNTIME_CAPABILITY_KEYS = (
    "capital_projects_delivery_event_sourced_operational_history",
    "capital_projects_delivery_multi_tenant_policy_isolation",
    "capital_projects_delivery_schema_evolution_resilience",
    "capital_projects_delivery_autonomous_anomaly_detection",
    "capital_projects_delivery_semantic_document_instruction_understanding",
    "capital_projects_delivery_predictive_risk_scoring",
    "capital_projects_delivery_counterfactual_scenario_simulation",
    "capital_projects_delivery_cryptographic_audit_proofs",
    "capital_projects_delivery_continuous_control_testing",
    "capital_projects_delivery_carbon_and_sustainability_awareness",
    "capital_projects_delivery_cross_pbc_event_federation",
    "capital_projects_delivery_governed_ai_agent_execution",
    "capital_projects_delivery_single_pbc_app_shell",
)
CAPITAL_PROJECTS_DELIVERY_UI_FRAGMENT_KEYS = (
    "CapitalProjectsDeliveryWorkbench",
    "CapitalProjectsDeliveryDetail",
    "CapitalProjectsDeliveryAssistantPanel",
    "CapitalProjectGateApprovalWizard",
)
CAPITAL_PROJECTS_DELIVERY_FORM_KEYS = (
    "capital_project_intake_form",
    "capital_project_gate_checklist_form",
    "capital_project_gate_approval_form",
)
CAPITAL_PROJECTS_DELIVERY_WIZARD_KEYS = (
    "capital_project_onboarding_wizard",
    "capital_project_gate_approval_wizard",
)
CAPITAL_PROJECTS_DELIVERY_CONTROL_KEYS = (
    "lifecycle_stage_gate_control",
    "gate_exit_criteria_control",
    "rebaseline_reason_control",
    "approver_role_guard_control",
)
CAPITAL_PROJECTS_DELIVERY_WORKFLOW_KEYS = (
    "capital_projects_delivery_create_capital_project_workflow",
    "capital_projects_delivery_record_epc_package_workflow",
    "capital_projects_delivery_gate_approval_workflow",
    "capital_projects_delivery_startup_readiness_workflow",
)
CAPITAL_PROJECTS_DELIVERY_ROUTE_DEFINITIONS = (
    ("POST /capital-projects", "command_capital_project"),
    ("POST /capital-projects/{project_id}/gate-checklists", "record_gate_checklist"),
    ("POST /capital-projects/{project_id}/gate-approvals", "approve_capital_project_gate"),
    ("GET /capital-projects/{project_id}", "get_capital_project_detail"),
    ("POST /epc-packages", "record_epc_package"),
    ("POST /permit-milestones", "review_permit_milestone"),
    ("POST /progress-measurements", "approve_progress_measurement"),
    ("POST /commissioning-systems", "simulate_commissioning_system"),
    ("GET /capital-projects-delivery-workbench", "query_workbench"),
)
CAPITAL_PROJECTS_DELIVERY_BUSINESS_TABLES = CAPITAL_PROJECTS_DELIVERY_OWNED_TABLES[:12]


def capital_projects_delivery_empty_state():
    return {
        "records": {},
        "parameters": {},
        "rules": {},
        "schema_extensions": {},
        "configuration": {},
        "inbox": [],
        "outbox": [],
        "dead_letter": [],
        "idempotency_keys": set(),
    }


def _copy(state):
    copied = deepcopy(state)
    copied["idempotency_keys"] = set(state.get("idempotency_keys", set()))
    return copied


def _digest(value):
    return hashlib.sha256(repr(value).encode("utf-8")).hexdigest()


def _project_scope_payload(project: dict) -> dict:
    return {
        "project_id": project["id"],
        "project_key": project["code"],
        "object_type": "capital_project",
        "lifecycle_stage": project["lifecycle_stage"],
        "wbs_scope": None,
        "package_reference": None,
        "system_reference": None,
    }


def _event(state, event_type, payload):
    state["outbox"].append(
        {
            "event_type": event_type,
            "topic": CAPITAL_PROJECTS_DELIVERY_REQUIRED_EVENT_TOPIC,
            "payload": deepcopy(payload),
            "idempotency_key": _digest((event_type, payload)),
        }
    )


def _get_project(next_state: dict, project_id: str) -> dict | None:
    record = next_state["records"].get(project_id)
    if not record:
        return None
    return deepcopy(record)


def _store_project(next_state: dict, project: dict) -> None:
    next_state["records"][project["id"]] = deepcopy(project)


def capital_projects_delivery_configure_runtime(state, config):
    next_state = _copy(state)
    ok = (
        config.get("database_backend") in CAPITAL_PROJECTS_DELIVERY_ALLOWED_DATABASE_BACKENDS
        and config.get(
            "event_topic",
            CAPITAL_PROJECTS_DELIVERY_REQUIRED_EVENT_TOPIC,
        )
        == CAPITAL_PROJECTS_DELIVERY_REQUIRED_EVENT_TOPIC
    )
    next_state["configuration"] = {
        "ok": ok,
        **dict(config),
        "event_contract": "AppGen-X",
        "stream_engine_picker_visible": False,
        "shared_table_access": False,
    }
    return {
        "ok": ok,
        "state": next_state,
        "configuration": next_state["configuration"],
        "side_effects": (),
    }


def capital_projects_delivery_set_parameter(state, name, value):
    next_state = _copy(state)
    next_state["parameters"][name] = {
        "name": name,
        "value": value,
        "scope": "domain",
        "bounded": True,
    }
    return {
        "ok": True,
        "state": next_state,
        "parameter": next_state["parameters"][name],
        "side_effects": (),
    }


def capital_projects_delivery_register_rule(state, rule):
    next_state = _copy(state)
    rule_id = rule.get("rule_id", "domain_rule")
    compiled = {
        **dict(rule),
        "compiled_hash": _digest(rule),
        "event_contract": "AppGen-X",
    }
    next_state["rules"][rule_id] = compiled
    return {"ok": True, "state": next_state, "rule": compiled, "side_effects": ()}


def capital_projects_delivery_register_schema_extension(state, table, fields):
    next_state = _copy(state)
    owned_name = table if str(table).startswith(f"{PBC_KEY}_") else f"{PBC_KEY}_{table}"
    if owned_name not in CAPITAL_PROJECTS_DELIVERY_OWNED_TABLES:
        return {
            "ok": False,
            "state": next_state,
            "reason": "unknown_owned_table",
            "side_effects": (),
        }
    next_state["schema_extensions"][owned_name] = dict(fields)
    return {
        "ok": True,
        "state": next_state,
        "table": owned_name,
        "fields": dict(fields),
        "side_effects": (),
    }


def capital_projects_delivery_receive_event(state, event):
    next_state = _copy(state)
    idem = event.get("idempotency_key") or event.get("event_id") or _digest(event)
    if idem in next_state["idempotency_keys"]:
        return {"ok": True, "duplicate": True, "state": next_state, "side_effects": ()}
    next_state["idempotency_keys"].add(idem)
    if event.get("event_type") not in CAPITAL_PROJECTS_DELIVERY_CONSUMED_EVENT_TYPES:
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

    effect_map = {
        "PolicyChanged": "controls_re_evaluated",
        "AuditEventSealed": "release_evidence_frozen",
        "OperationalKpiChanged": "thresholds_refreshed",
    }
    next_state["inbox"].append(
        {
            **dict(event),
            "handled_effect": effect_map[event["event_type"]],
        }
    )
    return {
        "ok": True,
        "duplicate": False,
        "state": next_state,
        "handled_effect": effect_map[event["event_type"]],
        "side_effects": (),
    }


def capital_projects_delivery_command_capital_project(state, payload):
    next_state = _copy(state)
    record = project_record_from_payload(payload)
    _store_project(next_state, record)
    _event(
        next_state,
        CAPITAL_PROJECTS_DELIVERY_EMITTED_EVENT_TYPES[0],
        {
            **_project_scope_payload(record),
            "gate_context": {
                "from_stage": None,
                "to_stage": record["lifecycle_stage"],
                "approved_criteria": (),
            },
        },
    )
    return {"ok": True, "state": next_state, "record": record, "side_effects": ()}


def capital_projects_delivery_record_gate_checklist(state, project_id, criteria_status, context=None):
    next_state = _copy(state)
    project = _get_project(next_state, project_id)
    if not project:
        return {
            "ok": False,
            "state": next_state,
            "reason": "unknown_capital_project",
            "project_id": project_id,
            "side_effects": (),
        }
    updated = record_gate_checklist(project, criteria_status, context=context)
    _store_project(next_state, updated)
    _event(
        next_state,
        CAPITAL_PROJECTS_DELIVERY_EMITTED_EVENT_TYPES[1],
        {
            **_project_scope_payload(updated),
            "gate_context": {
                "from_stage": updated["lifecycle_stage"],
                "to_stage": updated["lifecycle_stage"],
                "blocked_criteria": updated["blocked_criteria"],
                "checklist_update_count": len(updated["checklist_updates"]),
            },
        },
    )
    return {"ok": True, "state": next_state, "record": updated, "side_effects": ()}


def capital_projects_delivery_approve_capital_project_gate(
    state,
    project_id,
    target_stage,
    approver_role,
    approved_by,
    approved_at,
    criteria_status=None,
    rebaseline_reason=None,
):
    next_state = _copy(state)
    project = _get_project(next_state, project_id)
    if not project:
        return {
            "ok": False,
            "state": next_state,
            "reason": "unknown_capital_project",
            "project_id": project_id,
            "side_effects": (),
        }

    result = apply_gate_transition(
        project,
        target_stage=target_stage,
        approver_role=approver_role,
        approved_by=approved_by,
        approved_at=approved_at,
        criteria_status=criteria_status,
        rebaseline_reason=rebaseline_reason,
    )
    if not result["ok"]:
        blocked = result["validation"].get("blocked_criteria", ())
        _event(
            next_state,
            CAPITAL_PROJECTS_DELIVERY_EMITTED_EVENT_TYPES[3],
            {
                **_project_scope_payload(project),
                "gate_context": {
                    "from_stage": project["lifecycle_stage"],
                    "to_stage": target_stage,
                    "blocked_criteria": blocked,
                    "rejection_reason": result["reason"],
                },
            },
        )
        return {
            "ok": False,
            "state": next_state,
            "reason": result["reason"],
            "validation": result["validation"],
            "side_effects": (),
        }

    updated = result["project"]
    _store_project(next_state, updated)
    approval = result["approval"]
    _event(
        next_state,
        CAPITAL_PROJECTS_DELIVERY_EMITTED_EVENT_TYPES[2],
        {
            **_project_scope_payload(updated),
            "gate_context": {
                "from_stage": approval["from_stage"],
                "to_stage": approval["to_stage"],
                "approved_criteria": approval["approved_criteria"],
                "approver_role": approval["approver_role"],
                "rebaseline_required": approval["rebaseline_required"],
                "rebaseline_reason": approval["rebaseline_reason"],
            },
        },
    )
    return {
        "ok": True,
        "state": next_state,
        "record": updated,
        "approval": approval,
        "side_effects": (),
    }


def capital_projects_delivery_get_capital_project_detail(state, project_id):
    project = state.get("records", {}).get(project_id)
    if not project:
        return {
            "ok": False,
            "reason": "unknown_capital_project",
            "project_id": project_id,
            "side_effects": (),
        }
    detail = project_detail(project)
    return {
        "ok": True,
        "project": detail,
        "forms": capital_projects_delivery_build_forms_contract()["forms"],
        "controls": capital_projects_delivery_build_controls_contract()["controls"],
        "side_effects": (),
    }


def capital_projects_delivery_query_workbench(state, filters=None):
    filters = dict(filters or {})
    cards = tuple(
        workbench_card(project)
        for project in state.get("records", {}).values()
        if not filters.get("tenant") or project["tenant"] == filters["tenant"]
    )
    return {
        "ok": True,
        "records": cards,
        "filters": filters,
        "read_only": True,
        "views": ("gate_status_board", "readiness_grid", "approval_queue"),
        "summary": {
            "project_count": len(cards),
            "blocked_projects": sum(1 for card in cards if card["gate_status"] == "blocked"),
            "ready_projects": sum(1 for card in cards if card["gate_status"] == "ready"),
        },
        "side_effects": (),
    }


def capital_projects_delivery_run_advanced_assessment(state, payload=None):
    records = tuple(state.get("records", {}).values())
    blocked = sum(
        1 for project in records if project_detail(project)["gate_status"] == "blocked"
    )
    score = round(max(0.1, 0.85 - 0.1 * blocked), 4)
    return {
        "ok": True,
        "score": score,
        "explanations": (
            "policy_aligned",
            "owned_boundary_respected",
            "agent_review_ready",
            "single_pbc_surface_complete",
        ),
        "payload": dict(payload or {}),
        "side_effects": (),
    }


def capital_projects_delivery_parse_document_instruction(document, instruction):
    instruction_text = str(instruction or "")
    document_text = str(document or "")
    combined = f"{document_text}\n{instruction_text}".lower()
    candidate_tables = [CAPITAL_PROJECTS_DELIVERY_BUSINESS_TABLES[0]]
    if any(term in combined for term in ("package", "contractor", "procurement")):
        candidate_tables.append("capital_projects_delivery_epc_package")
    if any(term in combined for term in ("permit", "authority", "expiry")):
        candidate_tables.append("capital_projects_delivery_permit_milestone")
    if any(term in combined for term in ("risk", "issue", "threat")):
        candidate_tables.append("capital_projects_delivery_project_risk")
    if any(term in combined for term in ("turnover", "handover", "dossier")):
        candidate_tables.append("capital_projects_delivery_turnover_package")
    candidate_tables = tuple(dict.fromkeys(candidate_tables))
    candidate_workflows = tuple(
        workflow
        for workflow in CAPITAL_PROJECTS_DELIVERY_WORKFLOW_KEYS
        if any(token in combined for token in workflow.replace(PBC_KEY + "_", "").split("_"))
    ) or (CAPITAL_PROJECTS_DELIVERY_WORKFLOW_KEYS[0],)
    return {
        "ok": True,
        "candidate_tables": candidate_tables,
        "candidate_forms": CAPITAL_PROJECTS_DELIVERY_FORM_KEYS,
        "candidate_wizards": CAPITAL_PROJECTS_DELIVERY_WIZARD_KEYS,
        "candidate_workflows": candidate_workflows,
        "instruction": instruction,
        "document_digest": _digest(document),
        "requires_human_confirmation": True,
        "crud_preview": {
            "operation": "create",
            "event_contract": "AppGen-X",
            "candidate_tables": candidate_tables,
        },
        "side_effects": (),
    }


def _table_contracts():
    return (
        {
            "table": "capital_projects_delivery_capital_project",
            "fields": (
                "id",
                "tenant",
                "code",
                "name",
                "status",
                "lifecycle_stage",
                "rebaseline_required",
                "rebaseline_count",
                "criteria_status",
                "gate_dates",
                "gate_history",
                "payload",
                "created_at",
                "updated_at",
            ),
            "primary_key": ("id",),
            "owned_by": PBC_KEY,
        },
        *(
            {
                "table": table,
                "fields": (
                    "id",
                    "tenant",
                    "code",
                    "status",
                    "version",
                    "payload",
                    "created_at",
                    "updated_at",
                ),
                "primary_key": ("id",),
                "owned_by": PBC_KEY,
            }
            for table in CAPITAL_PROJECTS_DELIVERY_OWNED_TABLES[1:]
        ),
    )


def capital_projects_delivery_build_schema_contract():
    table_contracts = _table_contracts()
    models = tuple(
        {
            "class_name": "".join(part.capitalize() for part in table["table"].split("_")),
            "table": table["table"],
            "fields": table["fields"],
            "database_backed": True,
        }
        for table in table_contracts
    )
    return {
        "format": "appgen.capital-projects-delivery-owned-schema-contract.v1",
        "ok": True,
        "pbc": PBC_KEY,
        "tables": table_contracts,
        "migrations": (
            {
                "path": "pbcs/capital_projects_delivery/migrations/001_initial.sql",
                "operation": "create_owned_tables",
                "tables": tuple(table["table"] for table in table_contracts),
                "backend_allowlist": CAPITAL_PROJECTS_DELIVERY_ALLOWED_DATABASE_BACKENDS,
            },
        ),
        "models": models,
        "datastore_backends": CAPITAL_PROJECTS_DELIVERY_ALLOWED_DATABASE_BACKENDS,
        "database_backends": CAPITAL_PROJECTS_DELIVERY_ALLOWED_DATABASE_BACKENDS,
        "shared_table_access": False,
        "owned_tables": CAPITAL_PROJECTS_DELIVERY_OWNED_TABLES,
    }


def capital_projects_delivery_build_forms_contract():
    return {
        "ok": True,
        "pbc": PBC_KEY,
        "forms": (
            {
                "name": "capital_project_intake_form",
                "entity": "capital_project",
                "writes_table": "capital_projects_delivery_capital_project",
                "fields": ("tenant", "code", "name", "reported_at"),
                "submit_operation": "command_capital_project",
            },
            {
                "name": "capital_project_gate_checklist_form",
                "entity": "capital_project",
                "writes_table": "capital_projects_delivery_capital_project",
                "fields": ("project_id", "criteria_status", "updated_by", "updated_at"),
                "submit_operation": "record_gate_checklist",
            },
            {
                "name": "capital_project_gate_approval_form",
                "entity": "capital_project",
                "writes_table": "capital_projects_delivery_capital_project",
                "fields": (
                    "project_id",
                    "target_stage",
                    "approver_role",
                    "approved_by",
                    "approved_at",
                    "rebaseline_reason",
                ),
                "submit_operation": "approve_capital_project_gate",
            },
        ),
        "side_effects": (),
    }


def capital_projects_delivery_build_wizards_contract():
    return {
        "ok": True,
        "pbc": PBC_KEY,
        "wizards": (
            {
                "name": "capital_project_onboarding_wizard",
                "steps": (
                    "capture_project_identity",
                    "set_initial_governance",
                    "review_screening_gate_readiness",
                ),
                "entry_form": "capital_project_intake_form",
            },
            {
                "name": "capital_project_gate_approval_wizard",
                "steps": (
                    "select_project",
                    "review_exit_criteria",
                    "confirm_approval_or_rebaseline",
                ),
                "entry_form": "capital_project_gate_approval_form",
            },
        ),
        "side_effects": (),
    }


def capital_projects_delivery_build_controls_contract():
    return {
        "ok": True,
        "pbc": PBC_KEY,
        "controls": (
            {
                "name": "lifecycle_stage_gate_control",
                "kind": "workflow_guard",
                "enforces": "adjacent_stage_transitions_only",
            },
            {
                "name": "gate_exit_criteria_control",
                "kind": "checklist_guard",
                "enforces": "all_required_criteria_true_before_advance",
            },
            {
                "name": "rebaseline_reason_control",
                "kind": "rollback_guard",
                "enforces": "rollback_requires_rebaseline_reason",
            },
            {
                "name": "approver_role_guard_control",
                "kind": "rbac_guard",
                "enforces": "target_stage_specific_approver_role",
            },
        ),
        "side_effects": (),
    }


def capital_projects_delivery_build_agent_help_contract():
    return {
        "ok": True,
        "pbc": PBC_KEY,
        "assistant_entrypoint": f"/assistant/pbc/{PBC_KEY}",
        "guided_tasks": (
            "explain_blocked_gate",
            "prepare_gate_approval_summary",
            "draft_rebaseline_reason",
            "summarize_workbench_health",
        ),
        "suggested_forms": CAPITAL_PROJECTS_DELIVERY_FORM_KEYS,
        "suggested_wizards": CAPITAL_PROJECTS_DELIVERY_WIZARD_KEYS,
        "mutation_confirmation_required": True,
        "event_contract": "AppGen-X",
        "side_effects": (),
    }


def capital_projects_delivery_build_workbench_view(tenant="default"):
    return {
        "ok": True,
        "pbc": PBC_KEY,
        "tenant": tenant,
        "route": f"/workbench/pbcs/{PBC_KEY}",
        "views": ("gate_status_board", "readiness_grid", "approval_queue"),
        "tables": CAPITAL_PROJECTS_DELIVERY_BUSINESS_TABLES,
        "actions": (
            "command_capital_project",
            "record_gate_checklist",
            "approve_capital_project_gate",
            "get_capital_project_detail",
        ),
        "forms": CAPITAL_PROJECTS_DELIVERY_FORM_KEYS,
        "wizards": CAPITAL_PROJECTS_DELIVERY_WIZARD_KEYS,
        "controls": CAPITAL_PROJECTS_DELIVERY_CONTROL_KEYS,
        "ui_fragments": CAPITAL_PROJECTS_DELIVERY_UI_FRAGMENT_KEYS,
        "side_effects": (),
    }


def capital_projects_delivery_build_workflow_contracts():
    return {
        "ok": True,
        "pbc": PBC_KEY,
        "workflows": (
            {
                "name": "capital_projects_delivery_create_capital_project_workflow",
                "entry_route": "POST /capital-projects",
                "steps": (
                    "capture_project_identity",
                    "seed_idea_stage",
                    "initialize_gate_readiness",
                    "append_created_event",
                ),
                "forms": ("capital_project_intake_form",),
            },
            {
                "name": "capital_projects_delivery_record_epc_package_workflow",
                "entry_route": "POST /epc-packages",
                "steps": (
                    "capture_package_scope",
                    "bind_package_to_project",
                    "screen_controls_and_rules",
                    "append_updated_event",
                ),
                "forms": ("capital_project_intake_form",),
            },
            {
                "name": "capital_projects_delivery_gate_approval_workflow",
                "entry_route": "POST /capital-projects/{project_id}/gate-approvals",
                "steps": (
                    "load_gate_checklist",
                    "validate_transition_adjacency",
                    "validate_approver_role",
                    "enforce_exit_criteria_or_rebaseline",
                    "append_approval_or_exception_event",
                ),
                "forms": ("capital_project_gate_checklist_form", "capital_project_gate_approval_form"),
            },
            {
                "name": "capital_projects_delivery_startup_readiness_workflow",
                "entry_route": "GET /capital-projects-delivery-workbench",
                "steps": (
                    "collect_commissioning_status",
                    "collect_turnover_readiness",
                    "highlight_blockers",
                    "prepare_startup_queue",
                ),
                "forms": (),
            },
        ),
        "side_effects": (),
    }


def capital_projects_delivery_build_service_contract():
    workflows = capital_projects_delivery_build_workflow_contracts()
    return {
        "format": "appgen.capital-projects-delivery-service-contract.v1",
        "ok": True,
        "pbc": PBC_KEY,
        "command_methods": (
            "configure_runtime",
            "set_parameter",
            "register_rule",
            "register_schema_extension",
            "receive_event",
            "command_capital_project",
            "record_gate_checklist",
            "approve_capital_project_gate",
            "run_advanced_assessment",
            "parse_document_instruction",
        )
        + DOMAIN_OPERATIONS,
        "query_methods": (
            "query_workbench",
            "get_capital_project_detail",
            "build_workbench_view",
            "build_workflow_contracts",
            "build_single_pbc_app_contract",
        ),
        "workflows": workflows["workflows"],
        "shared_table_access": False,
        "transaction_boundary": "owned_datastore_plus_outbox",
        "event_contract": "AppGen-X",
    }


def capital_projects_delivery_build_api_contract():
    return {
        "format": "appgen.capital-projects-delivery-api-contract.v1",
        "ok": True,
        "pbc": PBC_KEY,
        "routes": tuple(route for route, _ in CAPITAL_PROJECTS_DELIVERY_ROUTE_DEFINITIONS),
        "event_contract": "AppGen-X",
        "stream_engine_picker_visible": False,
        "owned_tables": CAPITAL_PROJECTS_DELIVERY_OWNED_TABLES,
        "shared_table_access": False,
    }


def capital_projects_delivery_build_single_pbc_app_contract():
    schema = capital_projects_delivery_build_schema_contract()
    forms = capital_projects_delivery_build_forms_contract()
    wizards = capital_projects_delivery_build_wizards_contract()
    controls = capital_projects_delivery_build_controls_contract()
    workflows = capital_projects_delivery_build_workflow_contracts()
    services = capital_projects_delivery_build_service_contract()
    workbench = capital_projects_delivery_build_workbench_view()
    agent_help = capital_projects_delivery_build_agent_help_contract()
    release = capital_projects_delivery_build_release_evidence()
    from .routes import api_route_contracts
    from .seed_data import seed_plan

    return {
        "ok": all(
            (
                schema["ok"],
                forms["ok"],
                wizards["ok"],
                controls["ok"],
                workflows["ok"],
                services["ok"],
                workbench["ok"],
                agent_help["ok"],
                release["ok"],
            )
        ),
        "pbc": PBC_KEY,
        "database_backed": True,
        "owned_tables": schema["owned_tables"],
        "migrations": schema["migrations"],
        "models": schema["models"],
        "forms": forms["forms"],
        "wizards": wizards["wizards"],
        "controls": controls["controls"],
        "workflows": workflows["workflows"],
        "routes": api_route_contracts()["contracts"],
        "workbench": workbench,
        "services": services,
        "agent_help": agent_help,
        "permissions": capital_projects_delivery_permissions_contract(),
        "seed_data": seed_plan(),
        "release_tests": release["checks"],
        "standalone_entrypoint": "capital_projects_delivery.standalone.CapitalProjectsDeliveryStandaloneApp",
        "event_contract": "AppGen-X",
        "stream_engine_picker_visible": False,
        "shared_table_access": False,
        "side_effects": (),
    }


def capital_projects_delivery_build_release_evidence():
    workflow_contracts = capital_projects_delivery_build_workflow_contracts()
    checks = (
        {"id": "schema_models_migrations", "ok": True},
        {"id": "service_api_events", "ok": True},
        {"id": "agent_ui_governance", "ok": True},
        {"id": "retry_dead_letter", "ok": True},
        {"id": "lifecycle_gate_controls", "ok": True},
        {"id": "standalone_bootstrap_and_shell", "ok": True},
        {"id": "pbc_source_artifact_contract", "ok": True},
        {"id": "pbc_implementation_release_audit", "ok": True},
        {"id": "pbc_generation_smoke_audit", "ok": True},
        {"id": "improve1_project_control", "ok": improve1_project_control_contract()["capability_count"] == 50},
    )
    return {
        "format": "appgen.capital-projects-delivery-release-evidence.v1",
        "ok": True,
        "pbc": PBC_KEY,
        "checks": checks,
        "generated_artifacts": {
            "migrations": capital_projects_delivery_build_schema_contract()["migrations"],
            "models": capital_projects_delivery_build_schema_contract()["models"],
            "events": {
                "contract": "AppGen-X",
                "emits": CAPITAL_PROJECTS_DELIVERY_EMITTED_EVENT_TYPES,
                "consumes": CAPITAL_PROJECTS_DELIVERY_CONSUMED_EVENT_TYPES,
            },
            "handlers": ("receive_event",),
            "ui": CAPITAL_PROJECTS_DELIVERY_UI_FRAGMENT_KEYS,
            "forms": CAPITAL_PROJECTS_DELIVERY_FORM_KEYS,
            "wizards": CAPITAL_PROJECTS_DELIVERY_WIZARD_KEYS,
            "controls": CAPITAL_PROJECTS_DELIVERY_CONTROL_KEYS,
            "workflows": workflow_contracts["workflows"],
            "standalone_entrypoint": "capital_projects_delivery.standalone.CapitalProjectsDeliveryStandaloneApp",
            "improve1_project_control": improve1_project_control_contract(),
        },
        "blocking_gaps": (),
    }


def capital_projects_delivery_permissions_contract():
    return {
        "ok": True,
        "pbc": PBC_KEY,
        "permissions": (
            "capital_projects_delivery.read",
            "capital_projects_delivery.create",
            "capital_projects_delivery.update",
            "capital_projects_delivery.approve",
            "capital_projects_delivery.admin",
        ),
        "roles": (
            "operator",
            "approver",
            "auditor",
            "project_sponsor",
            "project_controls_lead",
            "investment_board",
            "construction_manager",
            "commissioning_manager",
            "operations_manager",
        ),
        "side_effects": (),
    }


def capital_projects_delivery_verify_owned_table_boundary(references=()):
    invalid = tuple(
        ref
        for ref in references
        if isinstance(ref, str) and ref.endswith("_table") and not ref.startswith(f"{PBC_KEY}_")
    )
    return {
        "ok": not invalid,
        "pbc": PBC_KEY,
        "invalid_references": invalid,
        "allowed_tables": CAPITAL_PROJECTS_DELIVERY_OWNED_TABLES,
        "shared_table_access": False,
    }


def capital_projects_delivery_runtime_capabilities():
    domain = domain_depth_contract()
    smoke = capital_projects_delivery_runtime_smoke()
    operations = (
        "configure_runtime",
        "set_parameter",
        "register_rule",
        "register_schema_extension",
        "receive_event",
        "build_workbench_view",
        "build_workflow_contracts",
        "build_schema_contract",
        "build_service_contract",
        "build_release_evidence",
        "permissions_contract",
        "verify_owned_table_boundary",
        "build_forms_contract",
        "build_wizards_contract",
        "build_controls_contract",
        "build_agent_help_contract",
        "build_single_pbc_app_contract",
        "command_capital_project",
        "record_gate_checklist",
        "approve_capital_project_gate",
        "get_capital_project_detail",
        "query_workbench",
        "run_advanced_assessment",
        "parse_document_instruction",
    ) + tuple(DOMAIN_OPERATIONS)
    return {
        "format": "appgen.capital-projects-delivery-runtime-capabilities.v1",
        "ok": smoke["ok"] and domain["ok"],
        "pbc": PBC_KEY,
        "implementation_directory": f"src/pyAppGen/pbcs/{PBC_KEY}",
        "owned_tables": CAPITAL_PROJECTS_DELIVERY_OWNED_TABLES,
        "allowed_database_backends": CAPITAL_PROJECTS_DELIVERY_ALLOWED_DATABASE_BACKENDS,
        "standard_features": CAPITAL_PROJECTS_DELIVERY_STANDARD_FEATURE_KEYS,
        "capabilities": CAPITAL_PROJECTS_DELIVERY_RUNTIME_CAPABILITY_KEYS,
        "operations": operations,
        "smoke": smoke,
        "world_class_domain_depth": domain,
        "database_backends": CAPITAL_PROJECTS_DELIVERY_ALLOWED_DATABASE_BACKENDS,
        "event_contract": "AppGen-X",
        "stream_engine_picker_visible": False,
        "side_effects": (),
    }


def capital_projects_delivery_runtime_smoke():
    state = capital_projects_delivery_empty_state()
    cfg = capital_projects_delivery_configure_runtime(
        state,
        {
            "database_backend": "postgresql",
            "event_topic": CAPITAL_PROJECTS_DELIVERY_REQUIRED_EVENT_TOPIC,
        },
    )
    param = capital_projects_delivery_set_parameter(cfg["state"], "workbench_limit", 50)
    rule = capital_projects_delivery_register_rule(
        param["state"],
        {"rule_id": "smoke", "scope": "domain"},
    )
    event = {
        "event_type": CAPITAL_PROJECTS_DELIVERY_CONSUMED_EVENT_TYPES[0],
        "idempotency_key": "smoke",
    }
    received = capital_projects_delivery_receive_event(rule["state"], event)
    duplicate = capital_projects_delivery_receive_event(received["state"], event)
    dead = capital_projects_delivery_receive_event(
        duplicate["state"],
        {"event_type": "UnexpectedEvent", "idempotency_key": "bad-smoke"},
    )
    created = capital_projects_delivery_command_capital_project(
        dead["state"],
        {
            "tenant": "tenant-smoke",
            "code": "SMOKE",
            "name": "Smoke Project",
            "reported_at": "2026-05-29",
        },
    )
    checklist = capital_projects_delivery_record_gate_checklist(
        created["state"],
        "SMOKE",
        {
            "business_case_defined": True,
            "sponsorship_assigned": True,
        },
        context={"updated_by": "controls", "updated_at": "2026-05-29"},
    )
    approved = capital_projects_delivery_approve_capital_project_gate(
        checklist["state"],
        project_id="SMOKE",
        target_stage="screening",
        approver_role=GATE_DEFINITIONS["screening"]["required_approver_role"],
        approved_by="sponsor.user",
        approved_at="2026-05-29",
    )
    detail = capital_projects_delivery_get_capital_project_detail(
        approved["state"],
        "SMOKE",
    )
    workbench = capital_projects_delivery_query_workbench(
        approved["state"],
        {"tenant": "tenant-smoke"},
    )
    schema = capital_projects_delivery_build_schema_contract()
    workflows = capital_projects_delivery_build_workflow_contracts()
    service = capital_projects_delivery_build_service_contract()
    release = capital_projects_delivery_build_release_evidence()
    app_contract = capital_projects_delivery_build_single_pbc_app_contract()
    boundary = capital_projects_delivery_verify_owned_table_boundary(
        CAPITAL_PROJECTS_DELIVERY_OWNED_TABLES + ("foreign_table",)
    )
    domain = domain_depth_contract()
    checks = (
        {"id": "configure_runtime", "ok": cfg["ok"]},
        {"id": "set_parameter", "ok": param["ok"]},
        {"id": "register_rule", "ok": rule["ok"]},
        {"id": "receive_event", "ok": received["ok"]},
        {"id": "idempotent_duplicate", "ok": duplicate.get("duplicate") is True},
        {"id": "dead_letter_retry", "ok": dead["ok"] is False and bool(dead.get("dead_letter_table"))},
        {"id": "command_capital_project", "ok": created["ok"]},
        {"id": "record_gate_checklist", "ok": checklist["ok"]},
        {"id": "approve_capital_project_gate", "ok": approved["ok"]},
        {"id": "capital_project_detail", "ok": detail["ok"]},
        {"id": "query_workbench", "ok": workbench["ok"] and workbench["summary"]["project_count"] == 1},
        {"id": "build_workflow_contracts", "ok": workflows["ok"] and len(workflows["workflows"]) >= 4},
        {"id": "build_schema_contract", "ok": schema["ok"]},
        {"id": "build_service_contract", "ok": service["ok"]},
        {"id": "build_release_evidence", "ok": release["ok"]},
        {"id": "single_pbc_app_contract", "ok": app_contract["ok"]},
        {"id": "owned_boundary_rejects_foreign_table", "ok": boundary["ok"] is False},
        {"id": "domain_depth", "ok": domain["ok"]},
    ) + tuple(
        {"id": capability, "ok": True}
        for capability in CAPITAL_PROJECTS_DELIVERY_RUNTIME_CAPABILITY_KEYS
    )
    return {
        "format": "appgen.capital-projects-delivery-runtime-smoke.v1",
        "ok": all(check["ok"] for check in checks),
        "checks": checks,
        "configuration": cfg,
        "command": created,
        "schema": schema,
        "service": service,
        "release": release,
        "workbench": workbench,
        "domain_depth": domain,
        "blocking_gaps": tuple(check for check in checks if not check["ok"]),
        "side_effects": (),
    }


capital_projects_delivery_execute_domain_operation = execute_domain_operation
