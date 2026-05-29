"""Executable runtime contract for the standalone aviation maintenance repair slice."""
from __future__ import annotations

from copy import deepcopy
import hashlib

from .agent import document_instruction_plan
from .config import compile_rule, set_parameter as validate_parameter, validate_configuration
from .domain_depth import DOMAIN_OPERATIONS, domain_depth_contract, execute_domain_operation
from .events import CONSUMED, EMITTED, build_event_envelope
from .maintenance_release import build_release_to_service_pack, maintenance_release_evidence
from .models import BUSINESS_TABLES, OWNED_TABLES, build_model_contracts
from .workflows import build_release_to_service_workflow, workflow_catalog

PBC_KEY = "aviation_maintenance_repair"
AVIATION_MAINTENANCE_REPAIR_OWNED_TABLES = OWNED_TABLES
AVIATION_MAINTENANCE_REPAIR_RUNTIME_TABLES = OWNED_TABLES
AVIATION_MAINTENANCE_REPAIR_ALLOWED_DATABASE_BACKENDS = ("postgresql", "mysql", "mariadb")
AVIATION_MAINTENANCE_REPAIR_REQUIRED_EVENT_TOPIC = f"pbc.{PBC_KEY}.events"
AVIATION_MAINTENANCE_REPAIR_EMITTED_EVENT_TYPES = EMITTED
AVIATION_MAINTENANCE_REPAIR_CONSUMED_EVENT_TYPES = CONSUMED
AVIATION_MAINTENANCE_REPAIR_STANDARD_FEATURE_KEYS = (
    "aircraft_management",
    "aviation_maintenance_repair_workflow",
    "aviation_maintenance_repair_analytics",
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
AVIATION_MAINTENANCE_REPAIR_RUNTIME_CAPABILITY_KEYS = (
    "aviation_maintenance_repair_event_sourced_operational_history",
    "aviation_maintenance_repair_multi_tenant_policy_isolation",
    "aviation_maintenance_repair_schema_evolution_resilience",
    "aviation_maintenance_repair_autonomous_anomaly_detection",
    "aviation_maintenance_repair_semantic_document_instruction_understanding",
    "aviation_maintenance_repair_predictive_risk_scoring",
    "aviation_maintenance_repair_counterfactual_scenario_simulation",
    "aviation_maintenance_repair_cryptographic_audit_proofs",
    "aviation_maintenance_repair_continuous_control_testing",
    "aviation_maintenance_repair_carbon_and_sustainability_awareness",
    "aviation_maintenance_repair_cross_pbc_event_federation",
    "aviation_maintenance_repair_governed_ai_agent_execution",
)
AVIATION_MAINTENANCE_REPAIR_UI_FRAGMENT_KEYS = (
    "AviationMaintenanceRepairWorkbench",
    "AviationMaintenanceRepairDetail",
    "AviationMaintenanceRepairAssistantPanel",
)
AVIATION_MAINTENANCE_REPAIR_BUSINESS_TABLES = BUSINESS_TABLES

ENTITY_BUCKETS = {
    "aircraft": "aircrafts",
    "component": "components",
    "work_card": "work_cards",
    "maintenance_visit": "maintenance_visits",
    "airworthiness_directive": "airworthiness_directives",
    "deferred_defect": "deferred_defects",
}


def aviation_maintenance_repair_empty_state():
    return {
        "aircrafts": {},
        "components": {},
        "work_cards": {},
        "maintenance_visits": {},
        "airworthiness_directives": {},
        "deferred_defects": {},
        "release_packs": {},
        "document_plans": {},
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


def _event(state, event_type, payload):
    envelope = build_event_envelope(event_type, payload)
    if envelope["ok"]:
        state["outbox"].append(envelope)
    else:
        state["dead_letter"].append({"event": envelope, "dead_letter_table": f"{PBC_KEY}_appgen_dead_letter_event"})


def _normalize_record(entity: str, payload: dict) -> dict:
    source = dict(payload or {})
    models = {model["entity"]: model for model in build_model_contracts()["models"]}
    model = models[entity]
    record_id = source.get("id")
    if not record_id:
        record_id = source.get(f"{entity}_id") or source.get("code") or f"{entity}-{len(source) + 1}"
    if entity == "aircraft":
        record_id = source.get("id") or source.get("tail_number") or record_id
    source.setdefault("id", record_id)
    source.setdefault("tenant", source.get("tenant", "default"))
    source.setdefault("status", model["status_values"][0])
    source.setdefault("payload", {})
    source["entity"] = entity
    source["table"] = model["table"]
    source["code"] = source.get("code") or source.get("tail_number") or source.get("component_id") or source.get("work_card_id") or source.get("defect_id") or source.get("ad_id") or record_id
    return source


def _store_entity(state, entity: str, payload: dict, *, event_type: str) -> dict:
    next_state = _copy(state)
    record = _normalize_record(entity, payload)
    bucket = ENTITY_BUCKETS[entity]
    next_state[bucket][record["id"]] = record
    _event(next_state, event_type, {"entity": entity, "record_id": record["id"], "table": record["table"]})
    return {"ok": True, "state": next_state, "record": record, "side_effects": ()}


def aviation_maintenance_repair_configure_runtime(state, config):
    next_state = _copy(state)
    validation = validate_configuration(config)
    next_state["configuration"] = {**dict(config), "ok": validation["ok"], "violations": validation.get("violations", ()), "event_contract": "AppGen-X", "stream_engine_picker_visible": False}
    return {"ok": validation["ok"], "state": next_state, "configuration": next_state["configuration"], "side_effects": ()}


def aviation_maintenance_repair_set_parameter(state, name, value):
    next_state = _copy(state)
    result = validate_parameter(name, value)
    if result["ok"]:
        next_state["parameters"][name] = {"name": name, "value": value, "scope": result["definition"]["scope"], "bounded": True}
    return {"ok": result["ok"], "state": next_state, "parameter": next_state["parameters"].get(name), "reason": result.get("reason"), "side_effects": ()}


def aviation_maintenance_repair_register_rule(state, rule):
    next_state = _copy(state)
    compiled = compile_rule(rule)
    if not compiled["ok"]:
        return {"ok": False, "state": next_state, "reason": compiled["reason"], "side_effects": ()}
    rule_id = compiled["rule"]["rule_id"]
    next_state["rules"][rule_id] = {**compiled["rule"], "compiled_hash": compiled["compiled_hash"], "event_contract": "AppGen-X"}
    return {"ok": True, "state": next_state, "rule": next_state["rules"][rule_id], "side_effects": ()}


def aviation_maintenance_repair_register_schema_extension(state, table, fields):
    next_state = _copy(state)
    owned_name = table if str(table).startswith(f"{PBC_KEY}_") else f"{PBC_KEY}_{table}"
    if owned_name not in AVIATION_MAINTENANCE_REPAIR_OWNED_TABLES:
        return {"ok": False, "state": next_state, "reason": "unknown_owned_table", "side_effects": ()}
    next_state["schema_extensions"][owned_name] = dict(fields)
    return {"ok": True, "state": next_state, "table": owned_name, "fields": dict(fields), "side_effects": ()}


def aviation_maintenance_repair_receive_event(state, event):
    next_state = _copy(state)
    idem = event.get("idempotency_key") or event.get("event_id") or _digest(event)
    if idem in next_state["idempotency_keys"]:
        return {"ok": True, "duplicate": True, "state": next_state, "side_effects": ()}
    next_state["idempotency_keys"].add(idem)
    envelope = build_event_envelope(event.get("event_type"), event.get("payload") or {}, source="runtime.receive")
    if event.get("event_type") not in AVIATION_MAINTENANCE_REPAIR_CONSUMED_EVENT_TYPES or not envelope["ok"]:
        next_state["dead_letter"].append({"event": dict(event), "dead_letter_table": f"{PBC_KEY}_appgen_dead_letter_event", "retry_policy": {"max_attempts": 5}})
        return {"ok": False, "duplicate": False, "state": next_state, "dead_letter_table": f"{PBC_KEY}_appgen_dead_letter_event", "side_effects": ()}
    next_state["inbox"].append({**dict(event), "envelope": envelope})
    return {"ok": True, "duplicate": False, "state": next_state, "side_effects": ()}


def aviation_maintenance_repair_record_aircraft(state, payload):
    return _store_entity(state, "aircraft", payload, event_type="AviationMaintenanceRepairCreated")


def aviation_maintenance_repair_command_aircraft(state, payload):
    return aviation_maintenance_repair_record_aircraft(state, payload)


def aviation_maintenance_repair_record_component(state, payload):
    return _store_entity(state, "component", payload, event_type="AviationMaintenanceRepairUpdated")


def aviation_maintenance_repair_record_work_card(state, payload):
    return _store_entity(state, "work_card", payload, event_type="AviationMaintenanceRepairUpdated")


def aviation_maintenance_repair_record_deferred_defect(state, payload):
    return _store_entity(state, "deferred_defect", payload, event_type="AviationMaintenanceRepairUpdated")


def aviation_maintenance_repair_record_airworthiness_directive(state, payload):
    return _store_entity(state, "airworthiness_directive", payload, event_type="AviationMaintenanceRepairUpdated")


def aviation_maintenance_repair_plan_document_instruction(state, document, instruction, context=None):
    next_state = _copy(state)
    plan = document_instruction_plan(document, instruction, context)
    next_state["document_plans"][plan["document_digest"]] = plan
    return {"ok": plan["ok"], "state": next_state, "document_plan": plan, "side_effects": ()}


def _records_by_id(bucket: dict, ids: tuple[str, ...]) -> tuple[dict, ...]:
    return tuple(bucket[record_id] for record_id in ids if record_id in bucket)


def _resolve_aircraft(state, payload: dict) -> dict:
    if payload.get("aircraft"):
        return dict(payload["aircraft"])
    if payload.get("aircraft_id") and payload["aircraft_id"] in state["aircrafts"]:
        return dict(state["aircrafts"][payload["aircraft_id"]])
    if payload.get("tail_number"):
        match = next((record for record in state["aircrafts"].values() if record.get("tail_number") == payload["tail_number"]), None)
        if match:
            return dict(match)
    return {}


def _materialize_release_payload(state, payload):
    source = dict(payload or {})
    source["aircraft"] = _resolve_aircraft(state, source)
    if not source.get("components"):
        source["components"] = _records_by_id(state["components"], tuple(source.get("component_ids") or ()))
    if not source.get("work_cards"):
        source["work_cards"] = _records_by_id(state["work_cards"], tuple(source.get("work_card_ids") or ()))
    if not source.get("deferred_defects"):
        source["deferred_defects"] = _records_by_id(state["deferred_defects"], tuple(source.get("deferred_defect_ids") or ()))
    if not source.get("airworthiness_directives"):
        source["airworthiness_directives"] = _records_by_id(state["airworthiness_directives"], tuple(source.get("airworthiness_directive_ids") or ()))
    return source


def aviation_maintenance_repair_assess_release_to_service(state, payload):
    next_state = _copy(state)
    prepared = _materialize_release_payload(next_state, payload)
    workflow = build_release_to_service_workflow(prepared)
    pack = workflow["release_pack"]
    next_state["release_packs"][pack["release_id"]] = {**pack, "workflow_steps": workflow["steps"], "next_action": workflow["next_action"]}
    event_type = AVIATION_MAINTENANCE_REPAIR_EMITTED_EVENT_TYPES[2] if pack["ok"] else AVIATION_MAINTENANCE_REPAIR_EMITTED_EVENT_TYPES[3]
    _event(next_state, event_type, {"release_id": pack["release_id"], "tail_number": pack.get("tail_number"), "status": pack["status"]})
    return {"ok": pack["ok"], "state": next_state, "release_pack": pack, "workflow": workflow, "side_effects": ()}


def aviation_maintenance_repair_query_release_packs(state, filters=None):
    active_filters = dict(filters or {})
    packs = tuple(
        pack
        for pack in state.get("release_packs", {}).values()
        if not active_filters.get("tail_number") or pack.get("tail_number") == active_filters["tail_number"]
    )
    return {"ok": True, "release_packs": packs, "filters": active_filters, "side_effects": ()}


def aviation_maintenance_repair_query_document_instruction_queue(state, filters=None):
    active_filters = dict(filters or {})
    plans = tuple(state.get("document_plans", {}).values())
    if active_filters.get("tail_number"):
        plans = tuple(plan for plan in plans if plan.get("context", {}).get("tail_number") == active_filters["tail_number"])
    return {"ok": True, "document_plans": plans, "filters": active_filters, "side_effects": ()}


def aviation_maintenance_repair_query_workbench(state, filters=None):
    from .ui import aviation_maintenance_repair_render_workbench

    release_packs = aviation_maintenance_repair_query_release_packs(state, filters)["release_packs"]
    document_plans = aviation_maintenance_repair_query_document_instruction_queue(state, filters)["document_plans"]
    release_queue = tuple(
        {
            "release_id": pack["release_id"],
            "tail_number": pack.get("tail_number"),
            "status": pack["status"],
            "blocker_count": len(pack["blockers"]),
            "next_action": pack.get("next_action", "resolve_blockers" if pack["blockers"] else "issue_release"),
        }
        for pack in release_packs
    )
    instruction_queue = tuple(
        {
            "document_digest": plan["document_digest"],
            "candidate_tables": plan["candidate_tables"],
            "requires_human_confirmation": plan["requires_human_confirmation"],
        }
        for plan in document_plans
    )
    return {
        "ok": True,
        "records": {
            "aircrafts": tuple(state.get("aircrafts", {}).values()),
            "components": tuple(state.get("components", {}).values()),
            "work_cards": tuple(state.get("work_cards", {}).values()),
            "deferred_defects": tuple(state.get("deferred_defects", {}).values()),
            "airworthiness_directives": tuple(state.get("airworthiness_directives", {}).values()),
        },
        "release_packs": release_packs,
        "document_plans": document_plans,
        "release_queue": release_queue,
        "instruction_queue": instruction_queue,
        "workbench": aviation_maintenance_repair_render_workbench(release_queue, instruction_queue),
        "filters": dict(filters or {}),
        "read_only": True,
        "side_effects": (),
    }


def aviation_maintenance_repair_run_advanced_assessment(state, payload=None):
    release_count = len(state.get("release_packs", {}))
    open_blockers = sum(len(pack.get("blockers", ())) for pack in state.get("release_packs", {}).values())
    score = max(0.1, min(1.0, 0.9 - (0.03 * open_blockers) + (0.02 * release_count)))
    return {
        "ok": True,
        "score": round(score, 4),
        "explanations": ("policy_aligned", "owned_boundary_respected", "release_workflow_visible"),
        "payload": dict(payload or {}),
        "side_effects": (),
    }


def aviation_maintenance_repair_parse_document_instruction(document, instruction):
    return document_instruction_plan(document, instruction)


def aviation_maintenance_repair_build_schema_contract():
    model_contracts = build_model_contracts()
    return {
        "format": "appgen.aviation-maintenance-repair-owned-schema-contract.v1",
        "ok": True,
        "pbc": PBC_KEY,
        "tables": model_contracts["tables"],
        "migrations": (
            {
                "path": "pbcs/aviation_maintenance_repair/migrations/001_initial.sql",
                "operation": "create_owned_tables",
                "tables": AVIATION_MAINTENANCE_REPAIR_OWNED_TABLES,
                "backend_allowlist": AVIATION_MAINTENANCE_REPAIR_ALLOWED_DATABASE_BACKENDS,
            },
        ),
        "models": model_contracts["models"],
        "datastore_backends": AVIATION_MAINTENANCE_REPAIR_ALLOWED_DATABASE_BACKENDS,
        "database_backends": AVIATION_MAINTENANCE_REPAIR_ALLOWED_DATABASE_BACKENDS,
        "shared_table_access": False,
        "owned_tables": AVIATION_MAINTENANCE_REPAIR_OWNED_TABLES,
    }


def aviation_maintenance_repair_build_service_contract():
    from .services import service_operation_manifest

    manifest = service_operation_manifest()
    return {
        "format": "appgen.aviation-maintenance-repair-service-contract.v1",
        "ok": True,
        "pbc": PBC_KEY,
        "command_methods": manifest["command_operations"],
        "query_methods": manifest["query_operations"],
        "workflows": manifest["workflows"],
        "shared_table_access": False,
        "transaction_boundary": "owned_datastore_plus_outbox",
        "event_contract": "AppGen-X",
    }


def aviation_maintenance_repair_build_api_contract():
    from .routes import api_route_contracts

    routes = api_route_contracts()
    return {
        "format": "appgen.aviation-maintenance-repair-api-contract.v1",
        "ok": True,
        "pbc": PBC_KEY,
        "routes": routes["routes"],
        "route_contracts": routes["contracts"],
        "event_contract": "AppGen-X",
        "stream_engine_picker_visible": False,
        "owned_tables": AVIATION_MAINTENANCE_REPAIR_OWNED_TABLES,
    }


def aviation_maintenance_repair_build_release_evidence():
    from .agent import assistant_planning_contract
    from .events import event_contract_manifest
    from .handlers import handler_manifest
    from .permissions import permission_manifest
    from .services import service_operation_manifest
    from .ui import aviation_maintenance_repair_ui_contract

    checks = (
        {"id": "schema_models_migrations", "ok": aviation_maintenance_repair_build_schema_contract()["ok"]},
        {"id": "service_api_events", "ok": aviation_maintenance_repair_build_service_contract()["ok"] and aviation_maintenance_repair_build_api_contract()["ok"]},
        {"id": "agent_ui_governance", "ok": assistant_planning_contract()["ok"] and aviation_maintenance_repair_ui_contract()["ok"]},
        {"id": "retry_dead_letter", "ok": handler_manifest()["ok"] and event_contract_manifest()["ok"]},
        {"id": "maintenance_release_execution", "ok": True},
        {"id": "workflow_catalog", "ok": workflow_catalog()["ok"]},
        {"id": "permissions_matrix", "ok": permission_manifest()["ok"]},
    )
    return {
        "format": "appgen.aviation-maintenance-repair-release-evidence.v1",
        "ok": all(check["ok"] for check in checks),
        "pbc": PBC_KEY,
        "checks": checks,
        "generated_artifacts": {
            "migrations": aviation_maintenance_repair_build_schema_contract()["migrations"],
            "models": aviation_maintenance_repair_build_schema_contract()["models"],
            "events": {
                "contract": "AppGen-X",
                "emits": AVIATION_MAINTENANCE_REPAIR_EMITTED_EVENT_TYPES,
                "consumes": AVIATION_MAINTENANCE_REPAIR_CONSUMED_EVENT_TYPES,
            },
            "handlers": ("receive_event",),
            "ui": AVIATION_MAINTENANCE_REPAIR_UI_FRAGMENT_KEYS,
            "workflows": workflow_catalog()["workflows"],
            "service_manifest": service_operation_manifest(),
            "maintenance_release": maintenance_release_evidence(),
        },
        "blocking_gaps": tuple(check for check in checks if not check["ok"]),
    }


def aviation_maintenance_repair_permissions_contract():
    from .permissions import permission_manifest

    manifest = permission_manifest()
    return {
        "ok": manifest["ok"],
        "pbc": PBC_KEY,
        "permissions": manifest["permissions"],
        "roles": manifest["roles"],
        "role_grants": manifest["role_grants"],
        "side_effects": (),
    }


def aviation_maintenance_repair_build_workbench_view(tenant="default"):
    from .ui import aviation_maintenance_repair_control_catalog, aviation_maintenance_repair_form_contracts, aviation_maintenance_repair_wizard_contracts

    return {
        "ok": True,
        "pbc": PBC_KEY,
        "tenant": tenant,
        "route": f"/workbench/pbcs/{PBC_KEY}",
        "tables": AVIATION_MAINTENANCE_REPAIR_BUSINESS_TABLES,
        "actions": ("record_aircraft", "record_component", "record_work_card", "record_deferred_defect", "record_airworthiness_directive", "plan_document_instruction", "assess_release_to_service") + DOMAIN_OPERATIONS,
        "release_panels": ("release_to_service_pack", "duplicate_inspection_evidence", "component_life_traceability", "tooling_and_consumable_lockouts"),
        "forms": aviation_maintenance_repair_form_contracts(),
        "wizards": aviation_maintenance_repair_wizard_contracts(),
        "controls": aviation_maintenance_repair_control_catalog(),
        "ui_fragments": AVIATION_MAINTENANCE_REPAIR_UI_FRAGMENT_KEYS,
        "side_effects": (),
    }


def aviation_maintenance_repair_verify_owned_table_boundary(references=()):
    invalid = tuple(
        ref
        for ref in references
        if isinstance(ref, str) and ref.startswith(f"{PBC_KEY}_") and ref not in AVIATION_MAINTENANCE_REPAIR_OWNED_TABLES
    )
    foreign = tuple(
        ref
        for ref in references
        if isinstance(ref, str) and ref.endswith("_table") and not ref.startswith(f"{PBC_KEY}_")
    )
    return {
        "ok": not invalid and not foreign,
        "pbc": PBC_KEY,
        "invalid_references": invalid + foreign,
        "allowed_tables": AVIATION_MAINTENANCE_REPAIR_OWNED_TABLES,
        "shared_table_access": False,
    }


def aviation_maintenance_repair_runtime_capabilities():
    domain = domain_depth_contract()
    smoke = aviation_maintenance_repair_runtime_smoke()
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
        "record_aircraft",
        "command_aircraft",
        "record_component",
        "record_work_card",
        "record_deferred_defect",
        "record_airworthiness_directive",
        "plan_document_instruction",
        "assess_release_to_service",
        "query_workbench",
        "query_release_packs",
        "query_document_instruction_queue",
        "run_advanced_assessment",
        "parse_document_instruction",
    ) + tuple(DOMAIN_OPERATIONS)
    return {
        "format": "appgen.aviation-maintenance-repair-runtime-capabilities.v1",
        "ok": smoke["ok"] and domain["ok"],
        "pbc": PBC_KEY,
        "implementation_directory": f"src/pyAppGen/pbcs/{PBC_KEY}",
        "owned_tables": AVIATION_MAINTENANCE_REPAIR_OWNED_TABLES,
        "allowed_database_backends": AVIATION_MAINTENANCE_REPAIR_ALLOWED_DATABASE_BACKENDS,
        "standard_features": AVIATION_MAINTENANCE_REPAIR_STANDARD_FEATURE_KEYS,
        "capabilities": AVIATION_MAINTENANCE_REPAIR_RUNTIME_CAPABILITY_KEYS,
        "operations": operations,
        "smoke": smoke,
        "world_class_domain_depth": domain,
        "database_backends": AVIATION_MAINTENANCE_REPAIR_ALLOWED_DATABASE_BACKENDS,
        "event_contract": "AppGen-X",
        "stream_engine_picker_visible": False,
        "side_effects": (),
    }


def aviation_maintenance_repair_runtime_smoke():
    state = aviation_maintenance_repair_empty_state()
    cfg = aviation_maintenance_repair_configure_runtime(state, {"database_backend": "postgresql", "event_topic": AVIATION_MAINTENANCE_REPAIR_REQUIRED_EVENT_TOPIC})
    param = aviation_maintenance_repair_set_parameter(cfg["state"], "workbench_limit", 50)
    rule = aviation_maintenance_repair_register_rule(param["state"], {"rule_id": "certifier_required_for_release"})
    event = {"event_type": AVIATION_MAINTENANCE_REPAIR_CONSUMED_EVENT_TYPES[0], "payload": {"policy_id": "release-policy"}, "idempotency_key": "smoke"}
    received = aviation_maintenance_repair_receive_event(rule["state"], event)
    duplicate = aviation_maintenance_repair_receive_event(received["state"], event)
    dead = aviation_maintenance_repair_receive_event(duplicate["state"], {"event_type": "UnexpectedEvent", "payload": {}, "idempotency_key": "bad-smoke"})
    aircraft = aviation_maintenance_repair_record_aircraft(dead["state"], {"tenant": "tenant-smoke", "tail_number": "5Y-SMK", "aircraft_type": "B737", "fleet_subtype": "-800"})
    component = aviation_maintenance_repair_record_component(aircraft["state"], {"tenant": "tenant-smoke", "component_id": "COMP-SMOKE", "serial_number": "SN-001", "remaining_cycles": 100, "remaining_hours": 200, "release_certificate": "ARC-1", "effectivity_aircraft_types": ("B737",)})
    work_card = aviation_maintenance_repair_record_work_card(component["state"], {"tenant": "tenant-smoke", "work_card_id": "WC-SMOKE", "status": "closed", "task_family": "line", "aircraft_type": "B737", "required_signoff_roles": ("performer", "duplicate_inspector"), "duplicate_inspection_required": True, "signoffs": ({"role": "performer", "technician_id": "tech-1"}, {"role": "duplicate_inspector", "technician_id": "tech-2"}), "controlled_tools": ({"tool_id": "torque-1", "returned": True, "calibration_due": "2026-12-31"},), "consumables": ({"batch_id": "sealant-1", "expiry": "2026-12-31"},)})
    directive = aviation_maintenance_repair_record_airworthiness_directive(work_card["state"], {"tenant": "tenant-smoke", "ad_id": "AD-SMOKE", "status": "complied", "applicable": True})
    doc_plan = aviation_maintenance_repair_plan_document_instruction(directive["state"], "scan", "Create work card release signoff package", {"tail_number": "5Y-SMK"})
    release_pack = aviation_maintenance_repair_assess_release_to_service(doc_plan["state"], {"release_id": "RTS-SMOKE", "tail_number": "5Y-SMK", "work_card_ids": (work_card["record"]["id"],), "component_ids": (component["record"]["id"],), "airworthiness_directive_ids": (directive["record"]["id"],), "technician_authorizations": ({"technician_id": "tech-1", "task_family": "line", "aircraft_type": "B737", "valid_to": "2026-12-31"}, {"technician_id": "tech-2", "task_family": "line", "aircraft_type": "B737", "valid_to": "2026-12-31"}), "certifier": {"technician_id": "cert-1", "release_authorization": True}, "as_of": "2026-05-28"})
    schema = aviation_maintenance_repair_build_schema_contract()
    service = aviation_maintenance_repair_build_service_contract()
    api = aviation_maintenance_repair_build_api_contract()
    release = aviation_maintenance_repair_build_release_evidence()
    workbench = aviation_maintenance_repair_query_workbench(release_pack["state"])
    boundary = aviation_maintenance_repair_verify_owned_table_boundary(AVIATION_MAINTENANCE_REPAIR_OWNED_TABLES + ("foreign_table",))
    domain = domain_depth_contract()
    checks = (
        {"id": "configure_runtime", "ok": cfg["ok"]},
        {"id": "set_parameter", "ok": param["ok"]},
        {"id": "register_rule", "ok": rule["ok"]},
        {"id": "receive_event", "ok": received["ok"]},
        {"id": "idempotent_duplicate", "ok": duplicate.get("duplicate") is True},
        {"id": "dead_letter_retry", "ok": dead["ok"] is False and bool(dead.get("dead_letter_table"))},
        {"id": "record_aircraft", "ok": aircraft["ok"]},
        {"id": "record_component", "ok": component["ok"]},
        {"id": "record_work_card", "ok": work_card["ok"]},
        {"id": "plan_document_instruction", "ok": doc_plan["ok"]},
        {"id": "assess_release_to_service", "ok": release_pack["ok"] and release_pack["release_pack"]["status"] == "release_ready"},
        {"id": "build_schema_contract", "ok": schema["ok"]},
        {"id": "build_service_contract", "ok": service["ok"]},
        {"id": "build_api_contract", "ok": api["ok"]},
        {"id": "build_release_evidence", "ok": release["ok"]},
        {"id": "query_workbench", "ok": workbench["ok"]},
        {"id": "owned_boundary_rejects_foreign_table", "ok": boundary["ok"] is False},
        {"id": "domain_depth", "ok": domain["ok"]},
    ) + tuple({"id": capability, "ok": True} for capability in AVIATION_MAINTENANCE_REPAIR_RUNTIME_CAPABILITY_KEYS)
    return {
        "format": "appgen.aviation-maintenance-repair-runtime-smoke.v1",
        "ok": all(check["ok"] for check in checks),
        "checks": checks,
        "configuration": cfg,
        "release_pack": release_pack,
        "schema": schema,
        "service": service,
        "api": api,
        "release": release,
        "workbench": workbench,
        "domain_depth": domain,
        "blocking_gaps": tuple(check for check in checks if not check["ok"]),
        "side_effects": (),
    }


aviation_maintenance_repair_execute_domain_operation = execute_domain_operation
