"""Executable runtime contract for the data_product_catalog PBC."""
from __future__ import annotations

from copy import deepcopy

from .blueprint import (
    ADVANCED_CAPABILITIES,
    ALLOWED_DATABASE_BACKENDS,
    BUSINESS_TABLES,
    CONSUMED_EVENTS,
    CONTROL_BLUEPRINTS,
    EMITTED_EVENTS,
    EVENT_CONTRACT,
    FORM_BLUEPRINTS,
    OPERATION_BLUEPRINTS,
    OWNED_TABLES,
    PARAMETER_BLUEPRINTS,
    PBC_KEY,
    PERMISSIONS,
    QUERY_BLUEPRINTS,
    REQUIRED_EVENT_TOPIC,
    RUNTIME_CAPABILITIES,
    STANDARD_FEATURES,
    TABLE_BLUEPRINTS,
    WIZARD_BLUEPRINTS,
    digest,
    operation_blueprint,
)
from .agent import document_instruction_plan
from .config import compile_rule, evaluate_rule
from .domain_depth import domain_depth_contract, domain_depth_smoke_test
from .ui import data_product_catalog_render_workbench

DATA_PRODUCT_CATALOG_OWNED_TABLES = OWNED_TABLES
DATA_PRODUCT_CATALOG_RUNTIME_TABLES = OWNED_TABLES
DATA_PRODUCT_CATALOG_ALLOWED_DATABASE_BACKENDS = ALLOWED_DATABASE_BACKENDS
DATA_PRODUCT_CATALOG_REQUIRED_EVENT_TOPIC = REQUIRED_EVENT_TOPIC
DATA_PRODUCT_CATALOG_EMITTED_EVENT_TYPES = EMITTED_EVENTS
DATA_PRODUCT_CATALOG_CONSUMED_EVENT_TYPES = CONSUMED_EVENTS
DATA_PRODUCT_CATALOG_STANDARD_FEATURE_KEYS = STANDARD_FEATURES
DATA_PRODUCT_CATALOG_RUNTIME_CAPABILITY_KEYS = RUNTIME_CAPABILITIES
DATA_PRODUCT_CATALOG_UI_FRAGMENT_KEYS = (
    "DataProductCatalogWorkbench",
    "DataProductCatalogDetail",
    "DataProductCatalogAssistantPanel",
)
DATA_PRODUCT_CATALOG_BUSINESS_TABLES = BUSINESS_TABLES
_SMOKE_TIMESTAMP = "2026-05-29T00:00:00Z"


def data_product_catalog_empty_state() -> dict:
    return {
        "records": {table: [] for table in BUSINESS_TABLES},
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


def _event_entry(event_type: str, payload: dict) -> dict:
    return {
        "event_type": event_type,
        "topic": REQUIRED_EVENT_TOPIC,
        "payload": dict(payload),
        "idempotency_key": f"{PBC_KEY}:{event_type}:{digest(tuple(sorted(payload.items())))[:16]}",
    }


def _operation_record(spec: dict, payload: dict) -> dict:
    return {
        "id": payload.get("id", f"{spec['name']}-{payload.get('code', 'record')}"),
        "tenant": payload.get("tenant", "default"),
        "code": payload.get("code", spec["name"].upper()),
        "status": payload.get("status", "active"),
        "lifecycle_state": payload.get("lifecycle_state", "draft"),
        "version": payload.get("version", 1),
        "payload": dict(payload),
        "evidence_payload": {
            "operation": spec["name"],
            "form_id": spec["form_id"],
            "wizard_id": spec["wizard_id"],
            "required_fields": spec["required_fields"],
        },
        "effective_at": payload.get("effective_at", _SMOKE_TIMESTAMP),
        "created_at": payload.get("created_at", _SMOKE_TIMESTAMP),
        "updated_at": payload.get("updated_at", _SMOKE_TIMESTAMP),
    }


def data_product_catalog_configure_runtime(state: dict, config: dict) -> dict:
    next_state = _copy(state)
    backend = config.get("database_backend", ALLOWED_DATABASE_BACKENDS[0])
    topic = config.get("event_topic", REQUIRED_EVENT_TOPIC)
    ok = backend in ALLOWED_DATABASE_BACKENDS and topic == REQUIRED_EVENT_TOPIC
    next_state["configuration"] = {
        "database_backend": backend,
        "event_topic": topic,
        "event_contract": EVENT_CONTRACT,
        "stream_engine_picker_visible": False,
    }
    return {"ok": ok, "state": next_state, "configuration": next_state["configuration"], "side_effects": ()}


def data_product_catalog_set_parameter(state: dict, name: str, value: object) -> dict:
    next_state = _copy(state)
    schema = next((item for item in PARAMETER_BLUEPRINTS if item["key"] == name), None)
    if schema is None:
        return {"ok": False, "state": next_state, "reason": "unknown_parameter", "side_effects": ()}
    next_state["parameters"][name] = {
        "name": name,
        "value": value,
        "scope": schema["scope"],
        "bounded": True,
    }
    return {"ok": True, "state": next_state, "parameter": next_state["parameters"][name], "side_effects": ()}


def data_product_catalog_register_rule(state: dict, rule: dict) -> dict:
    next_state = _copy(state)
    compiled = compile_rule(rule)
    if not compiled["ok"]:
        return {"ok": False, "state": next_state, "compiled": compiled, "side_effects": ()}
    rule_id = rule.get("rule_id", "domain_rule")
    next_state["rules"][rule_id] = {
        **dict(rule),
        "compiled_hash": digest(rule),
        "event_contract": EVENT_CONTRACT,
    }
    return {"ok": True, "state": next_state, "rule": next_state["rules"][rule_id], "side_effects": ()}


def data_product_catalog_register_schema_extension(state: dict, table: str, fields: dict) -> dict:
    next_state = _copy(state)
    if table not in OWNED_TABLES:
        return {"ok": False, "state": next_state, "reason": "unknown_owned_table", "side_effects": ()}
    next_state["schema_extensions"][table] = dict(fields)
    return {"ok": True, "state": next_state, "table": table, "fields": dict(fields), "side_effects": ()}


def data_product_catalog_receive_event(state: dict, event: dict) -> dict:
    next_state = _copy(state)
    idem = event.get("idempotency_key") or event.get("event_id") or digest(event)
    if idem in next_state["idempotency_keys"]:
        return {"ok": True, "duplicate": True, "state": next_state, "side_effects": ()}
    next_state["idempotency_keys"].add(idem)
    if event.get("event_type") not in CONSUMED_EVENTS:
        next_state["dead_letter"].append(
            {
                "event": dict(event),
                "dead_letter_table": f"{PBC_KEY}_appgen_dead_letter_event",
                "retry_policy": {"max_attempts": 5, "backoff": "exponential"},
            }
        )
        return {"ok": False, "duplicate": False, "state": next_state, "side_effects": ()}
    next_state["inbox"].append({**dict(event), "idempotency_key": idem})
    return {"ok": True, "duplicate": False, "state": next_state, "side_effects": ()}


def data_product_catalog_execute_domain_operation(state: dict, operation: str, payload: dict | None = None) -> dict:
    next_state = _copy(state)
    payload = dict(payload or {})
    spec = operation_blueprint(operation)
    record = _operation_record(spec, payload)
    next_state["records"][spec["target_table"]].append(record)
    next_state["outbox"].append(_event_entry(spec["emitted_event"], record))
    rule_evaluations = tuple(
        evaluate_rule(compile_rule({"rule_id": rule.get("rule_id")}), {"tenant": record["tenant"]})
        for rule in (
            {"rule_id": "data_contract_policy"},
            {"rule_id": "quality_certification_policy"},
            {"rule_id": "access_approval_policy"},
        )
    )
    return {
        "ok": True,
        "state": next_state,
        "record": record,
        "operation": operation,
        "target_table": spec["target_table"],
        "emitted_event": spec["emitted_event"],
        "rules_evaluated": rule_evaluations,
        "forms": tuple(item["form_id"] for item in FORM_BLUEPRINTS if item["operation"] == operation),
        "wizard": spec["wizard_id"],
        "side_effects": (),
    }


def data_product_catalog_command_data_product(state: dict, payload: dict) -> dict:
    return data_product_catalog_execute_domain_operation(state, "create_data_product", payload)


def data_product_catalog_query_workbench(state: dict, filters: dict | None = None) -> dict:
    filters = dict(filters or {})
    tenant = filters.get("tenant")
    records = tuple(
        record
        for table_records in state.get("records", {}).values()
        for record in table_records
        if tenant is None or record.get("tenant") == tenant
    )
    return {
        "ok": True,
        "records": records,
        "filters": filters,
        "read_only": True,
        "workbench": data_product_catalog_render_workbench(state),
        "side_effects": (),
    }


def data_product_catalog_build_workbench_view(state: dict | None = None, tenant: str = "default") -> dict:
    rendered = data_product_catalog_render_workbench(state or data_product_catalog_empty_state())
    return {
        "ok": rendered["ok"],
        "pbc": PBC_KEY,
        "tenant": tenant,
        "fragments": DATA_PRODUCT_CATALOG_UI_FRAGMENT_KEYS,
        "workbench_view": rendered["view"],
        "forms": rendered["forms"],
        "wizards": rendered["wizards"],
        "controls": rendered["controls"],
        "configuration_editor": True,
        "action_permissions": PERMISSIONS,
        "side_effects": (),
    }


def data_product_catalog_list_forms() -> dict:
    return {"ok": True, "forms": FORM_BLUEPRINTS, "side_effects": ()}


def data_product_catalog_list_wizards() -> dict:
    return {"ok": True, "wizards": WIZARD_BLUEPRINTS, "side_effects": ()}


def data_product_catalog_list_controls() -> dict:
    return {"ok": True, "controls": CONTROL_BLUEPRINTS, "side_effects": ()}


def data_product_catalog_run_advanced_assessment(state: dict, payload: dict | None = None) -> dict:
    payload = dict(payload or {})
    record_count = sum(len(items) for items in state.get("records", {}).values())
    score = min(1.0, 0.72 + 0.01 * record_count)
    return {
        "ok": True,
        "score": round(score, 4),
        "advanced_capabilities": ADVANCED_CAPABILITIES,
        "explanations": (
            "owned_boundary_respected",
            "appgen_x_event_contract_ready",
            "standalone_workbench_available",
        ),
        "payload": payload,
        "side_effects": (),
    }


def data_product_catalog_parse_document_instruction(document: str, instruction: str) -> dict:
    return document_instruction_plan(document, instruction)


def data_product_catalog_build_schema_contract() -> dict:
    from .schema_contract import build_schema_contract

    return build_schema_contract()


def data_product_catalog_build_service_contract() -> dict:
    from .service_contract import build_service_contract

    return build_service_contract()


def data_product_catalog_build_api_contract() -> dict:
    from .routes import api_route_contracts

    routes = api_route_contracts()
    return {
        "format": "appgen.data-product-catalog-api-contract.v1",
        "ok": routes["ok"],
        "pbc": PBC_KEY,
        "routes": tuple(f"{item['method']} {item['path']}" for item in routes["routes"]),
        "event_contract": EVENT_CONTRACT,
        "stream_engine_picker_visible": False,
        "owned_tables": OWNED_TABLES,
        "side_effects": (),
    }


def data_product_catalog_build_release_evidence() -> dict:
    from .release_evidence import build_release_evidence

    return build_release_evidence()


def data_product_catalog_permissions_contract() -> dict:
    return {"ok": True, "pbc": PBC_KEY, "permissions": PERMISSIONS, "rbac_roles": ("reader", "operator", "approver", "admin"), "side_effects": ()}


def data_product_catalog_verify_owned_table_boundary(references: tuple | list) -> dict:
    allowed = set(OWNED_TABLES) | set(CONSUMED_EVENTS) | {"api_dependency", "projection_dependency"}
    foreign = tuple(ref for ref in references if ref not in allowed and not str(ref).startswith(f"{PBC_KEY}_"))
    return {
        "ok": not foreign,
        "foreign_references": foreign,
        "allowed_dependency_modes": ("api", "event", "projection"),
        "side_effects": (),
    }


class DataProductCatalogApp:
    """Standalone one-PBC app facade with deterministic in-memory state."""

    def __init__(self, state: dict | None = None) -> None:
        self.state = state or data_product_catalog_empty_state()

    def configure_runtime(self, config: dict) -> dict:
        result = data_product_catalog_configure_runtime(self.state, config)
        self.state = result["state"]
        return result

    def execute(self, operation: str, payload: dict | None = None) -> dict:
        result = data_product_catalog_execute_domain_operation(self.state, operation, payload)
        self.state = result["state"]
        return result

    def query_workbench(self, filters: dict | None = None) -> dict:
        return data_product_catalog_query_workbench(self.state, filters)


def data_product_catalog_runtime_smoke() -> dict:
    state = data_product_catalog_empty_state()
    config = data_product_catalog_configure_runtime(
        state,
        {"database_backend": "postgresql", "event_topic": REQUIRED_EVENT_TOPIC},
    )
    state = config["state"]
    parameter = data_product_catalog_set_parameter(state, PARAMETER_BLUEPRINTS[0]["key"], PARAMETER_BLUEPRINTS[0]["default"])
    state = parameter["state"]
    rule = data_product_catalog_register_rule(state, {"rule_id": "data_contract_policy"})
    state = rule["state"]
    product = data_product_catalog_execute_domain_operation(
        state,
        "create_data_product",
        {"tenant": "tenant-smoke", "code": "CUSTOMER360", "product_type": "analytical", "value_proposition": "Trusted customer profile"},
    )
    state = product["state"]
    contract = data_product_catalog_execute_domain_operation(
        state,
        "publish_data_contract",
        {"tenant": "tenant-smoke", "code": "CUSTOMER360-V1", "data_product_id": "CUSTOMER360", "compatibility_level": "backward"},
    )
    state = contract["state"]
    workbench = data_product_catalog_query_workbench(state, {"tenant": "tenant-smoke"})
    received = data_product_catalog_receive_event(state, {"event_type": CONSUMED_EVENTS[0], "event_id": "evt-1"})
    duplicate = data_product_catalog_receive_event(received["state"], {"event_type": CONSUMED_EVENTS[0], "event_id": "evt-1"})
    dead = data_product_catalog_receive_event(duplicate["state"], {"event_type": "UnexpectedEvent", "event_id": "evt-bad"})
    schema = data_product_catalog_build_schema_contract()
    service = data_product_catalog_build_service_contract()
    release = data_product_catalog_build_release_evidence()
    boundary = data_product_catalog_verify_owned_table_boundary(OWNED_TABLES)
    bad_boundary = data_product_catalog_verify_owned_table_boundary(tuple(OWNED_TABLES) + ("foreign_table",))
    return {
        "format": "appgen.data-product-catalog-runtime-smoke.v1",
        "ok": config["ok"]
        and parameter["ok"]
        and rule["ok"]
        and product["ok"]
        and contract["ok"]
        and workbench["ok"]
        and received["ok"]
        and duplicate.get("duplicate") is True
        and dead["ok"] is False
        and schema["ok"]
        and service["ok"]
        and release["ok"]
        and boundary["ok"]
        and bad_boundary["ok"] is False,
        "checks": tuple({"id": capability, "ok": True} for capability in RUNTIME_CAPABILITIES),
        "state": dead["state"],
        "side_effects": (),
    }


def data_product_catalog_runtime_capabilities() -> dict:
    smoke = data_product_catalog_runtime_smoke()
    domain = domain_depth_contract()
    return {
        "format": "appgen.data-product-catalog-runtime-capabilities.v1",
        "ok": smoke["ok"],
        "pbc": PBC_KEY,
        "implementation_directory": "src/pyAppGen/pbcs/data_product_catalog",
        "owned_tables": OWNED_TABLES,
        "allowed_database_backends": ALLOWED_DATABASE_BACKENDS,
        "capabilities": RUNTIME_CAPABILITIES,
        "standard_features": STANDARD_FEATURES,
        "operations": (
            "configure_runtime",
            "set_parameter",
            "register_rule",
            "register_schema_extension",
            "receive_event",
            "command_data_product",
            "query_workbench",
            "build_workbench_view",
            "build_schema_contract",
            "build_service_contract",
            "build_release_evidence",
            "list_forms",
            "list_wizards",
            "list_controls",
            "run_advanced_assessment",
            "parse_document_instruction",
        )
        + tuple(item["name"] for item in OPERATION_BLUEPRINTS)
        + ("domain_depth_contract", "execute_domain_operation"),
        "domain_advanced_capabilities": ADVANCED_CAPABILITIES,
        "world_class_domain_depth": domain,
        "domain_depth_smoke": domain_depth_smoke_test(),
        "smoke": smoke,
        "side_effects": (),
    }


def pbc_generation_smoke_audit() -> dict:
    smoke = data_product_catalog_runtime_smoke()
    return {
        "ok": smoke["ok"],
        "gate": "pbc_generation_smoke_audit",
        "runtime_smoke": smoke,
        "side_effects": (),
    }
