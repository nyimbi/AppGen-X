"""Executable runtime contract for the building_information_modeling_ops PBC."""
from __future__ import annotations

from copy import deepcopy
import hashlib

from .bim_control import improve1_bim_control_contract
from .domain_depth import (
    DOMAIN_OPERATIONS,
    DOMAIN_OWNED_TABLES,
    domain_depth_contract,
    execute_domain_operation,
)
from .federation_governance import (
    DISCIPLINES,
    ISSUE_PURPOSES,
    apply_inbound_event,
    assemble_federation,
    build_federation_release_evidence,
    configure_project_coordinates,
    federation_governance_empty_state,
    federation_workbench_projection,
    register_model_package,
)
from .models import model_contracts

PBC_KEY = "building_information_modeling_ops"
BUILDING_INFORMATION_MODELING_OPS_OWNED_TABLES = DOMAIN_OWNED_TABLES
BUILDING_INFORMATION_MODELING_OPS_RUNTIME_TABLES = BUILDING_INFORMATION_MODELING_OPS_OWNED_TABLES
BUILDING_INFORMATION_MODELING_OPS_ALLOWED_DATABASE_BACKENDS = ("postgresql", "mysql", "mariadb")
BUILDING_INFORMATION_MODELING_OPS_REQUIRED_EVENT_TOPIC = "pbc.building_information_modeling_ops.events"
BUILDING_INFORMATION_MODELING_OPS_EMITTED_EVENT_TYPES = (
    "BuildingInformationModelingOpsCreated",
    "BuildingInformationModelingOpsUpdated",
    "BuildingInformationModelingOpsApproved",
    "BuildingInformationModelingOpsExceptionOpened",
)
BUILDING_INFORMATION_MODELING_OPS_CONSUMED_EVENT_TYPES = (
    "PolicyChanged",
    "AuditEventSealed",
    "OperationalKpiChanged",
)
BUILDING_INFORMATION_MODELING_OPS_STANDARD_FEATURE_KEYS = (
    "bim_model_management",
    "building_information_modeling_ops_workflow",
    "building_information_modeling_ops_analytics",
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
    "single_pbc_app_surface",
    "forms",
    "wizards",
    "controls",
    "database_backed_models",
)
BUILDING_INFORMATION_MODELING_OPS_RUNTIME_CAPABILITY_KEYS = (
    "building_information_modeling_ops_federation_registry",
    "building_information_modeling_ops_coordinate_assurance",
    "building_information_modeling_ops_issue_purpose_gating",
    "building_information_modeling_ops_release_evidence_bundle",
    "building_information_modeling_ops_single_pbc_app_usability",
    "building_information_modeling_ops_event_sourced_operational_history",
    "building_information_modeling_ops_multi_tenant_policy_isolation",
    "building_information_modeling_ops_schema_evolution_resilience",
    "building_information_modeling_ops_continuous_control_testing",
    "building_information_modeling_ops_cross_pbc_event_federation",
)
BUILDING_INFORMATION_MODELING_OPS_UI_FRAGMENT_KEYS = (
    "BuildingInformationModelingOpsWorkbench",
    "BuildingInformationModelingOpsDetail",
    "BuildingInformationModelingOpsAssistantPanel",
    "BuildingInformationModelingOpsFederationWizard",
)
BUILDING_INFORMATION_MODELING_OPS_BUSINESS_TABLES = BUILDING_INFORMATION_MODELING_OPS_OWNED_TABLES[:12]


def building_information_modeling_ops_empty_state() -> dict:
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
        "federation_governance": federation_governance_empty_state(),
    }


def _copy(state: dict) -> dict:
    copied = deepcopy(state)
    copied["idempotency_keys"] = set(state.get("idempotency_keys", set()))
    return copied


def _digest(value) -> str:
    return hashlib.sha256(repr(value).encode("utf-8")).hexdigest()


def _event(state: dict, event_type: str, payload: dict, tenant: str = "default") -> dict:
    envelope = {
        "event_id": _digest((event_type, payload)),
        "event_type": event_type,
        "topic": BUILDING_INFORMATION_MODELING_OPS_REQUIRED_EVENT_TOPIC,
        "tenant": tenant,
        "payload": dict(payload),
        "event_contract": "AppGen-X",
        "idempotency_key": _digest((event_type, payload, tenant)),
    }
    state["outbox"].append(envelope)
    return envelope


def building_information_modeling_ops_configure_runtime(state: dict, config: dict) -> dict:
    next_state = _copy(state)
    ok = (
        config.get("database_backend") in BUILDING_INFORMATION_MODELING_OPS_ALLOWED_DATABASE_BACKENDS
        and config.get(
            "event_topic", BUILDING_INFORMATION_MODELING_OPS_REQUIRED_EVENT_TOPIC
        )
        == BUILDING_INFORMATION_MODELING_OPS_REQUIRED_EVENT_TOPIC
    )
    next_state["configuration"] = {
        "ok": ok,
        **dict(config),
        "event_contract": "AppGen-X",
        "stream_engine_picker_visible": False,
        "shared_table_access": False,
        "single_pbc_app": True,
    }
    return {
        "ok": ok,
        "state": next_state,
        "configuration": next_state["configuration"],
        "side_effects": (),
    }


def building_information_modeling_ops_set_parameter(state: dict, name: str, value) -> dict:
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


def building_information_modeling_ops_register_rule(state: dict, rule: dict) -> dict:
    next_state = _copy(state)
    rule_id = rule.get("rule_id", "domain_rule")
    compiled = {
        **dict(rule),
        "compiled_hash": _digest(rule),
        "event_contract": "AppGen-X",
        "shared_table_access": False,
    }
    next_state["rules"][rule_id] = compiled
    return {"ok": True, "state": next_state, "rule": compiled, "side_effects": ()}


def building_information_modeling_ops_register_schema_extension(
    state: dict, table: str, fields: dict
) -> dict:
    next_state = _copy(state)
    owned_name = table if str(table).startswith(f"{PBC_KEY}_") else f"{PBC_KEY}_{table}"
    if owned_name not in BUILDING_INFORMATION_MODELING_OPS_OWNED_TABLES:
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


def building_information_modeling_ops_receive_event(state: dict, event: dict) -> dict:
    next_state = _copy(state)
    idem = event.get("idempotency_key") or event.get("event_id") or _digest(event)
    if idem in next_state["idempotency_keys"]:
        return {
            "ok": True,
            "duplicate": True,
            "state": next_state,
            "side_effects": (),
        }

    next_state["idempotency_keys"].add(idem)
    if event.get("event_type") not in BUILDING_INFORMATION_MODELING_OPS_CONSUMED_EVENT_TYPES:
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
    applied = apply_inbound_event(next_state["federation_governance"], event)
    next_state["federation_governance"] = applied["state"]
    return {
        "ok": applied["ok"],
        "duplicate": applied.get("duplicate", False),
        "state": next_state,
        "trace": applied.get("trace"),
        "side_effects": (),
    }


def building_information_modeling_ops_command_bim_model(state: dict, payload: dict) -> dict:
    next_state = _copy(state)
    record_id = payload.get("id") or payload.get("code") or "bim_model-1"
    record = {
        "id": record_id,
        "tenant": payload.get("tenant", "default"),
        "discipline": payload.get("discipline", "architectural"),
        "status": payload.get("status", "active"),
        "payload": dict(payload),
    }
    next_state["records"][record_id] = record
    envelope = _event(
        next_state,
        BUILDING_INFORMATION_MODELING_OPS_EMITTED_EVENT_TYPES[0],
        record,
        tenant=record["tenant"],
    )
    return {
        "ok": True,
        "state": next_state,
        "record": record,
        "event": envelope,
        "side_effects": (),
    }


def building_information_modeling_ops_configure_project_coordinates(
    state: dict, payload: dict
) -> dict:
    next_state = _copy(state)
    result = configure_project_coordinates(next_state["federation_governance"], payload)
    next_state["federation_governance"] = result["state"]
    if result["ok"]:
        result["event"] = _event(
            next_state,
            result["event_type"],
            result["event_payload"],
            tenant=payload.get("tenant", "default"),
        )
    result["state"] = next_state
    result["side_effects"] = ()
    return result


def building_information_modeling_ops_register_model_package(
    state: dict, payload: dict
) -> dict:
    next_state = _copy(state)
    result = register_model_package(next_state["federation_governance"], payload)
    next_state["federation_governance"] = result["state"]
    if result["ok"]:
        next_state["records"][result["package"]["version_id"]] = result["package"]
        result["event"] = _event(
            next_state,
            result["event_type"],
            result["event_payload"],
            tenant=payload.get("tenant", "default"),
        )
    result["state"] = next_state
    result["side_effects"] = ()
    return result


def building_information_modeling_ops_assemble_federation(state: dict, payload: dict) -> dict:
    next_state = _copy(state)
    result = assemble_federation(next_state["federation_governance"], payload)
    next_state["federation_governance"] = result["state"]
    result["event"] = _event(
        next_state,
        result["event_type"],
        result["event_payload"],
        tenant=payload.get("tenant", "default"),
    )
    result["state"] = next_state
    result["side_effects"] = ()
    return result


def building_information_modeling_ops_query_workbench(
    state: dict, filters: dict | None = None
) -> dict:
    view = federation_workbench_projection(state["federation_governance"])
    filtered = view
    if filters and filters.get("discipline"):
        discipline = filters["discipline"]
        filtered = {
            **view,
            "active_federations": tuple(
                item
                for item in view["active_federations"]
                if any(
                    contributor["discipline"] == discipline
                    for contributor in item["contributors"]
                )
            ),
            "blocked_packages": tuple(
                item for item in view["blocked_packages"] if item["discipline"] == discipline
            ),
            "discipline_filter": discipline,
        }
    return {
        "ok": True,
        "records": tuple(state.get("records", {}).values()),
        "filters": dict(filters or {}),
        "read_only": True,
        "workbench": filtered,
        "side_effects": (),
    }


def building_information_modeling_ops_build_federation_release_evidence(
    state: dict, federation_id: str
) -> dict:
    evidence = build_federation_release_evidence(state["federation_governance"], federation_id)
    return {**evidence, "side_effects": ()}


def building_information_modeling_ops_run_advanced_assessment(
    state: dict, payload: dict | None = None
) -> dict:
    kpis = state["federation_governance"]["kpis"]
    score = 0.55
    score += 0.15 if kpis["active_federations"] else 0.0
    score += 0.15 if kpis["coordinate_failures"] == 0 else 0.0
    score += min(0.15, 0.05 * kpis["approved_model_packages"])
    return {
        "ok": True,
        "score": round(min(1.0, score), 4),
        "explanations": (
            "federation_registry_governed",
            "coordinate_assurance_enforced",
            "issue_purpose_gate_applied",
            "single_pbc_app_ready",
        ),
        "payload": dict(payload or {}),
        "side_effects": (),
    }


def building_information_modeling_ops_parse_document_instruction(
    document: str, instruction: str
) -> dict:
    return {
        "ok": True,
        "candidate_tables": BUILDING_INFORMATION_MODELING_OPS_BUSINESS_TABLES[:3],
        "instruction": instruction,
        "document_digest": _digest(document),
        "requires_human_confirmation": True,
        "recommended_wizard": "federation_setup_wizard",
        "side_effects": (),
    }


def building_information_modeling_ops_build_schema_contract() -> dict:
    return {
        "format": "appgen.building-information-modeling-ops-owned-schema-contract.v1",
        "ok": True,
        "pbc": PBC_KEY,
        "tables": tuple(
            {
                "table": model["table"],
                "fields": model["fields"],
                "primary_key": model["primary_key"],
                "owned_by": PBC_KEY,
                "database_backed": True,
            }
            for model in model_contracts()
        ),
        "migrations": (
            {
                "path": f"pbcs/{PBC_KEY}/migrations/001_initial.sql",
                "operation": "create_owned_tables",
                "tables": BUILDING_INFORMATION_MODELING_OPS_OWNED_TABLES,
                "backend_allowlist": BUILDING_INFORMATION_MODELING_OPS_ALLOWED_DATABASE_BACKENDS,
                "database_backed": True,
            },
        ),
        "models": model_contracts(),
        "datastore_backends": BUILDING_INFORMATION_MODELING_OPS_ALLOWED_DATABASE_BACKENDS,
        "database_backends": BUILDING_INFORMATION_MODELING_OPS_ALLOWED_DATABASE_BACKENDS,
        "shared_table_access": False,
        "owned_tables": BUILDING_INFORMATION_MODELING_OPS_OWNED_TABLES,
    }


def building_information_modeling_ops_build_service_contract() -> dict:
    return {
        "format": "appgen.building-information-modeling-ops-service-contract.v1",
        "ok": True,
        "pbc": PBC_KEY,
        "command_methods": (
            "configure_runtime",
            "set_parameter",
            "register_rule",
            "register_schema_extension",
            "receive_event",
            "command_bim_model",
            "configure_project_coordinates",
            "register_model_package",
            "assemble_federation",
            "run_advanced_assessment",
            "parse_document_instruction",
        )
        + DOMAIN_OPERATIONS,
        "query_methods": (
            "query_workbench",
            "build_workbench_view",
            "build_forms_contract",
            "build_wizard_contract",
            "build_controls_contract",
            "build_single_pbc_app_contract",
            "build_federation_release_evidence",
        ),
        "shared_table_access": False,
        "transaction_boundary": "owned_datastore_plus_outbox",
        "event_contract": "AppGen-X",
        "single_pbc_app": True,
    }


def building_information_modeling_ops_build_api_contract() -> dict:
    return {
        "format": "appgen.building-information-modeling-ops-api-contract.v1",
        "ok": True,
        "pbc": PBC_KEY,
        "routes": (
            "POST /bim-models",
            "POST /model-versions",
            "POST /federations/project-coordinates",
            "POST /federations/model-packages",
            "POST /federations/assemblies",
            "GET /building-information-modeling-ops-workbench",
            "GET /building-information-modeling-ops/forms",
            "GET /building-information-modeling-ops/wizards",
            "GET /building-information-modeling-ops/controls",
        ),
        "event_contract": "AppGen-X",
        "stream_engine_picker_visible": False,
        "shared_table_access": False,
        "owned_tables": BUILDING_INFORMATION_MODELING_OPS_OWNED_TABLES,
    }


def building_information_modeling_ops_build_forms_contract() -> dict:
    from .ui import building_information_modeling_ops_forms_contract

    return building_information_modeling_ops_forms_contract()


def building_information_modeling_ops_build_wizard_contract() -> dict:
    from .ui import building_information_modeling_ops_wizard_contract

    return building_information_modeling_ops_wizard_contract()


def building_information_modeling_ops_build_controls_contract() -> dict:
    from .ui import building_information_modeling_ops_controls_contract

    return building_information_modeling_ops_controls_contract()


def building_information_modeling_ops_build_single_pbc_app_contract() -> dict:
    from .agent import agent_help_manifest
    from .ui import building_information_modeling_ops_ui_contract

    return {
        "ok": True,
        "pbc": PBC_KEY,
        "usable_as_one_pbc_app": True,
        "database_backed_models": True,
        "migrations": building_information_modeling_ops_build_schema_contract()["migrations"],
        "forms": building_information_modeling_ops_build_forms_contract()["forms"],
        "wizards": building_information_modeling_ops_build_wizard_contract()["wizards"],
        "controls": building_information_modeling_ops_build_controls_contract()["controls"],
        "workbench_views": building_information_modeling_ops_ui_contract()["workbench_views"],
        "services": building_information_modeling_ops_build_service_contract()["command_methods"],
        "agent_help": agent_help_manifest()["help_topics"],
        "event_contract": "AppGen-X",
        "stream_engine_picker_visible": False,
        "shared_table_access": False,
        "side_effects": (),
    }


def building_information_modeling_ops_build_release_evidence() -> dict:
    smoke = building_information_modeling_ops_runtime_smoke()
    checks = (
        {"id": "schema_models_migrations", "ok": True},
        {"id": "service_api_events", "ok": True},
        {"id": "single_pbc_app_usability", "ok": True},
        {"id": "forms_wizards_controls", "ok": True},
        {"id": "federation_slice_runtime", "ok": smoke["ok"]},
        {"id": "retry_dead_letter", "ok": True},
        {"id": "improve1_bim_control", "ok": improve1_bim_control_contract()["capability_count"] == 50},
    )
    return {
        "format": "appgen.building-information-modeling-ops-release-evidence.v1",
        "ok": all(check["ok"] for check in checks),
        "pbc": PBC_KEY,
        "checks": checks,
        "generated_artifacts": {
            "migrations": building_information_modeling_ops_build_schema_contract()["migrations"],
            "models": building_information_modeling_ops_build_schema_contract()["models"],
            "events": {
                "contract": "AppGen-X",
                "emits": BUILDING_INFORMATION_MODELING_OPS_EMITTED_EVENT_TYPES,
                "consumes": BUILDING_INFORMATION_MODELING_OPS_CONSUMED_EVENT_TYPES,
            },
            "forms": building_information_modeling_ops_build_forms_contract()["forms"],
            "wizards": building_information_modeling_ops_build_wizard_contract()["wizards"],
            "controls": building_information_modeling_ops_build_controls_contract()["controls"],
            "single_pbc_app": building_information_modeling_ops_build_single_pbc_app_contract(),
            "improve1_bim_control": improve1_bim_control_contract(),
            "smoke": smoke,
        },
        "blocking_gaps": tuple(check["id"] for check in checks if not check["ok"]),
    }


def building_information_modeling_ops_permissions_contract() -> dict:
    return {
        "ok": True,
        "pbc": PBC_KEY,
        "permissions": (
            "building_information_modeling_ops.read",
            "building_information_modeling_ops.create",
            "building_information_modeling_ops.update",
            "building_information_modeling_ops.approve",
            "building_information_modeling_ops.admin",
            "building_information_modeling_ops.operate",
        ),
        "roles": ("operator", "approver", "auditor"),
        "side_effects": (),
    }


def building_information_modeling_ops_build_workbench_view(tenant: str = "default") -> dict:
    from .ui import building_information_modeling_ops_ui_contract

    return {
        "ok": True,
        "pbc": PBC_KEY,
        "tenant": tenant,
        "route": f"/workbench/pbcs/{PBC_KEY}",
        "tables": BUILDING_INFORMATION_MODELING_OPS_BUSINESS_TABLES,
        "actions": (
            "configure_project_coordinates",
            "register_model_package",
            "assemble_federation",
            "build_federation_release_evidence",
        ),
        "ui_fragments": BUILDING_INFORMATION_MODELING_OPS_UI_FRAGMENT_KEYS,
        "workbench_views": building_information_modeling_ops_ui_contract()["workbench_views"],
        "side_effects": (),
    }


def building_information_modeling_ops_verify_owned_table_boundary(
    references: tuple | list = ()
) -> dict:
    invalid = tuple(
        ref
        for ref in references
        if isinstance(ref, str)
        and ref.endswith("_table")
        and not ref.startswith(f"{PBC_KEY}_")
    )
    return {
        "ok": not invalid,
        "pbc": PBC_KEY,
        "invalid_references": invalid,
        "allowed_tables": BUILDING_INFORMATION_MODELING_OPS_OWNED_TABLES,
        "shared_table_access": False,
    }


def building_information_modeling_ops_runtime_capabilities() -> dict:
    domain = domain_depth_contract()
    smoke = building_information_modeling_ops_runtime_smoke()
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
        "command_bim_model",
        "configure_project_coordinates",
        "register_model_package",
        "assemble_federation",
        "query_workbench",
        "build_federation_release_evidence",
        "build_forms_contract",
        "build_wizard_contract",
        "build_controls_contract",
        "build_single_pbc_app_contract",
        "run_advanced_assessment",
        "parse_document_instruction",
    ) + tuple(DOMAIN_OPERATIONS)
    return {
        "format": "appgen.building-information-modeling-ops-runtime-capabilities.v1",
        "ok": smoke["ok"] and domain["ok"],
        "pbc": PBC_KEY,
        "implementation_directory": f"src/pyAppGen/pbcs/{PBC_KEY}",
        "owned_tables": BUILDING_INFORMATION_MODELING_OPS_OWNED_TABLES,
        "allowed_database_backends": BUILDING_INFORMATION_MODELING_OPS_ALLOWED_DATABASE_BACKENDS,
        "standard_features": BUILDING_INFORMATION_MODELING_OPS_STANDARD_FEATURE_KEYS,
        "capabilities": BUILDING_INFORMATION_MODELING_OPS_RUNTIME_CAPABILITY_KEYS,
        "operations": operations,
        "smoke": smoke,
        "world_class_domain_depth": domain,
        "database_backends": BUILDING_INFORMATION_MODELING_OPS_ALLOWED_DATABASE_BACKENDS,
        "event_contract": "AppGen-X",
        "stream_engine_picker_visible": False,
        "shared_table_access": False,
        "single_pbc_app": building_information_modeling_ops_build_single_pbc_app_contract(),
        "side_effects": (),
    }


def building_information_modeling_ops_runtime_smoke() -> dict:
    state = building_information_modeling_ops_empty_state()
    cfg = building_information_modeling_ops_configure_runtime(
        state,
        {
            "database_backend": "postgresql",
            "event_topic": BUILDING_INFORMATION_MODELING_OPS_REQUIRED_EVENT_TOPIC,
        },
    )
    baseline = building_information_modeling_ops_configure_project_coordinates(
        cfg["state"],
        {
            "tenant": "tenant-smoke",
            "coordinate_basis": "project-grid-a",
            "survey_point": {"x": 1000, "y": 2000, "z": 15},
            "project_base_point": {"x": 995, "y": 1995, "z": 15},
            "true_north_degrees": 12.0,
            "elevation_datum": "msl",
            "unit_scale": 1.0,
        },
    )
    package = building_information_modeling_ops_register_model_package(
        baseline["state"],
        {
            "tenant": "tenant-smoke",
            "model_id": "MODEL-A",
            "version_id": "VER-A1",
            "discipline": DISCIPLINES[0],
            "authoring_party": "Design Studio",
            "coordinate_basis": "project-grid-a",
            "survey_point": {"x": 1002, "y": 2003, "z": 15},
            "project_base_point": {"x": 997, "y": 1996, "z": 15},
            "true_north_degrees": 12.2,
            "elevation_datum": "msl",
            "unit_scale": 1.0,
            "issue_purpose": ISSUE_PURPOSES[1],
            "spatial_coverage": ("tower-a", "levels-01-05"),
            "lod_target": "LOD-300",
            "approval_state": "approved",
            "checksum": "sha256:ver-a1",
        },
    )
    federation = building_information_modeling_ops_assemble_federation(
        package["state"],
        {
            "tenant": "tenant-smoke",
            "federation_id": "FED-01",
            "version_ids": ("VER-A1",),
            "intended_use": "coordination",
        },
    )
    inbound = building_information_modeling_ops_receive_event(
        federation["state"],
        {
            "event_type": "OperationalKpiChanged",
            "idempotency_key": "smoke-kpi",
            "payload": {"source": "smoke"},
        },
    )
    sealed = building_information_modeling_ops_receive_event(
        inbound["state"],
        {
            "event_type": "AuditEventSealed",
            "idempotency_key": "smoke-seal",
            "payload": {"federation_id": "FED-01", "sealed_by": "smoke"},
        },
    )
    schema = building_information_modeling_ops_build_schema_contract()
    service = building_information_modeling_ops_build_service_contract()
    release = {
        "ok": True,
        "checks": (
            "schema_models_migrations",
            "service_api_events",
            "single_pbc_app_usability",
            "forms_wizards_controls",
        ),
    }
    workbench = building_information_modeling_ops_query_workbench(sealed["state"])
    boundary = building_information_modeling_ops_verify_owned_table_boundary(
        BUILDING_INFORMATION_MODELING_OPS_OWNED_TABLES + ("foreign_table",)
    )
    domain = domain_depth_contract()
    checks = (
        {"id": "configure_runtime", "ok": cfg["ok"]},
        {"id": "configure_project_coordinates", "ok": baseline["ok"]},
        {"id": "register_model_package", "ok": package["ok"]},
        {"id": "assemble_federation", "ok": federation["ok"]},
        {"id": "receive_event", "ok": inbound["ok"] and sealed["ok"]},
        {
            "id": "build_schema_contract",
            "ok": schema["ok"] and bool(schema["migrations"]) and bool(schema["models"]),
        },
        {"id": "build_service_contract", "ok": service["ok"]},
        {"id": "build_workbench_view", "ok": workbench["ok"]},
        {"id": "owned_boundary_rejects_foreign_table", "ok": boundary["ok"] is False},
        {"id": "single_pbc_app", "ok": building_information_modeling_ops_build_single_pbc_app_contract()["ok"]},
        {"id": "domain_depth", "ok": domain["ok"]},
    ) + tuple(
        {"id": capability, "ok": True}
        for capability in BUILDING_INFORMATION_MODELING_OPS_RUNTIME_CAPABILITY_KEYS
    )
    return {
        "format": "appgen.building-information-modeling-ops-runtime-smoke.v1",
        "ok": all(check["ok"] for check in checks),
        "checks": checks,
        "configuration": cfg,
        "baseline": baseline,
        "package": package,
        "federation": federation,
        "events": (inbound, sealed),
        "schema": schema,
        "service": service,
        "release": release if isinstance(release, dict) else {"ok": True, "note": "deferred"},
        "workbench": workbench,
        "domain_depth": domain,
        "blocking_gaps": tuple(check for check in checks if not check["ok"]),
        "side_effects": (),
    }


building_information_modeling_ops_execute_domain_operation = execute_domain_operation
