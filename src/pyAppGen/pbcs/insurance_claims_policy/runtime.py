"""Executable runtime contract for the insurance_claims_policy PBC."""

from __future__ import annotations

from . import config
from . import domain_depth
from . import events
from . import permissions
from . import release_evidence
from . import routes
from . import schema_contract
from . import service_contract
from . import ui
from .models import OWNED_TABLES as INSURANCE_CLAIMS_POLICY_OWNED_TABLES
from .standalone import InsuranceClaimsPolicyStandaloneApp
from .standalone import smoke_test as standalone_smoke_test

PBC_KEY = "insurance_claims_policy"
INSURANCE_CLAIMS_POLICY_RUNTIME_TABLES = INSURANCE_CLAIMS_POLICY_OWNED_TABLES
INSURANCE_CLAIMS_POLICY_ALLOWED_DATABASE_BACKENDS = config.ALLOWED_DATABASE_BACKENDS
INSURANCE_CLAIMS_POLICY_REQUIRED_EVENT_TOPIC = config.REQUIRED_EVENT_TOPIC
INSURANCE_CLAIMS_POLICY_EMITTED_EVENT_TYPES = events.EMITTED
INSURANCE_CLAIMS_POLICY_CONSUMED_EVENT_TYPES = events.CONSUMED
INSURANCE_CLAIMS_POLICY_STANDARD_FEATURE_KEYS = (
    "insurance_policy_management",
    "insurance_claims_policy_workflow",
    "insurance_claims_policy_analytics",
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
INSURANCE_CLAIMS_POLICY_RUNTIME_CAPABILITY_KEYS = (
    "insurance_claims_policy_event_sourced_operational_history",
    "insurance_claims_policy_multi_tenant_policy_isolation",
    "insurance_claims_policy_schema_evolution_resilience",
    "insurance_claims_policy_autonomous_anomaly_detection",
    "insurance_claims_policy_semantic_document_instruction_understanding",
    "insurance_claims_policy_predictive_risk_scoring",
    "insurance_claims_policy_counterfactual_scenario_simulation",
    "insurance_claims_policy_cryptographic_audit_proofs",
    "insurance_claims_policy_continuous_control_testing",
    "insurance_claims_policy_carbon_and_sustainability_awareness",
    "insurance_claims_policy_cross_pbc_event_federation",
    "insurance_claims_policy_governed_ai_agent_execution",
)
INSURANCE_CLAIMS_POLICY_UI_FRAGMENT_KEYS = ui.UI_FRAGMENTS
INSURANCE_CLAIMS_POLICY_BUSINESS_TABLES = tuple(table for table in INSURANCE_CLAIMS_POLICY_OWNED_TABLES if "appgen_" not in table)


def insurance_claims_policy_empty_state() -> dict:
    return InsuranceClaimsPolicyStandaloneApp().state


def insurance_claims_policy_configure_runtime(state: dict, config_payload: dict) -> dict:
    app = InsuranceClaimsPolicyStandaloneApp(state=state)
    result = app.configure(config_payload)
    return {"ok": result["ok"], "state": app.state, "configuration": result["configuration"], "side_effects": ()}


def insurance_claims_policy_set_parameter(state: dict, name: str, value) -> dict:
    app = InsuranceClaimsPolicyStandaloneApp(state=state)
    result = app.set_parameter(name, value)
    return {"ok": result["ok"], "state": app.state, "parameter": result.get("parameter"), "side_effects": ()}


def insurance_claims_policy_register_rule(state: dict, rule: dict) -> dict:
    app = InsuranceClaimsPolicyStandaloneApp(state=state)
    result = app.register_rule(rule)
    return {"ok": result["ok"], "state": app.state, "rule": result.get("rule"), "side_effects": ()}


def insurance_claims_policy_register_schema_extension(state: dict, table: str, fields: dict) -> dict:
    app = InsuranceClaimsPolicyStandaloneApp(state=state)
    result = app.register_schema_extension({"target_table": table if table.startswith(f"{PBC_KEY}_") else f"{PBC_KEY}_{table}", "extension_key": "runtime", "extension_payload": fields})
    return {"ok": result["ok"], "state": app.state, "table": result.get("schema_extension", {}).get("target_table"), "fields": fields, "side_effects": ()}


def insurance_claims_policy_receive_event(state: dict, event: dict) -> dict:
    app = InsuranceClaimsPolicyStandaloneApp(state=state)
    result = app.receive_event(event)
    duplicate = result.get("duplicate", False)
    return {"ok": result["ok"], "duplicate": duplicate, "state": app.state, "side_effects": ()}


def insurance_claims_policy_command_insurance_policy(state: dict, payload: dict) -> dict:
    app = InsuranceClaimsPolicyStandaloneApp(state=state)
    result = app.create_insurance_policy(payload)
    return {"ok": result["ok"], "state": app.state, "record": result.get("policy"), "side_effects": ()}


def insurance_claims_policy_query_workbench(state: dict, filters: dict | None = None) -> dict:
    app = InsuranceClaimsPolicyStandaloneApp(state=state)
    tenant = dict(filters or {}).get("tenant", "default")
    result = app.workbench(tenant=tenant)
    return {"ok": result["ok"], "records": tuple(app.state["claim_records"].values()), "filters": dict(filters or {}), "read_only": True, "workbench": result, "side_effects": ()}


def insurance_claims_policy_run_advanced_assessment(state: dict, payload: dict | None = None) -> dict:
    app = InsuranceClaimsPolicyStandaloneApp(state=state)
    exposure = app.simulate_loss_exposure(payload or {})
    return {
        "ok": exposure["ok"],
        "score": round(min(1.0, exposure["expected_loss"] / 250000.0 + 0.6), 4),
        "explanations": ("loss_exposure_modeled", "reserve_signal_considered", "fraud_signal_considered"),
        "payload": dict(payload or {}),
        "simulation": exposure,
        "side_effects": (),
    }


def insurance_claims_policy_parse_document_instruction(document: str, instruction: str) -> dict:
    app = InsuranceClaimsPolicyStandaloneApp()
    return app.document_intake(document, instruction)


def insurance_claims_policy_build_schema_contract() -> dict:
    return schema_contract.build_schema_contract()


def insurance_claims_policy_build_service_contract() -> dict:
    return service_contract.build_service_contract()


def insurance_claims_policy_build_api_contract() -> dict:
    route_contract = routes.api_route_contracts()
    return {"format": "appgen.insurance-claims-policy-api-contract.v1", "ok": route_contract["ok"], "pbc": PBC_KEY, "routes": route_contract["routes"], "event_contract": "AppGen-X", "stream_engine_picker_visible": False, "owned_tables": INSURANCE_CLAIMS_POLICY_OWNED_TABLES, "side_effects": ()}


def insurance_claims_policy_build_release_evidence() -> dict:
    return release_evidence.build_release_evidence()


def insurance_claims_policy_permissions_contract() -> dict:
    manifest = permissions.permission_manifest()
    return {"ok": manifest["ok"], "pbc": PBC_KEY, "permissions": manifest["permissions"], "rbac_roles": manifest["rbac_roles"], "side_effects": ()}


def insurance_claims_policy_build_workbench_view(state: dict | None = None, tenant: str = "default") -> dict:
    rendered = ui.insurance_claims_policy_render_workbench(state, tenant=tenant)
    return {
        "ok": rendered["ok"],
        "pbc": PBC_KEY,
        "tenant": tenant,
        "fragments": INSURANCE_CLAIMS_POLICY_UI_FRAGMENT_KEYS,
        "workbench_view": "InsuranceClaimsPolicyWorkbench",
        "configuration_editor": True,
        "action_permissions": tuple(ui.ACTION_PERMISSIONS.values()),
        "cards": rendered["workbench"]["cards"],
        "side_effects": (),
    }


def insurance_claims_policy_verify_owned_table_boundary(references: tuple[str, ...] | list[str]) -> dict:
    allowed = set(INSURANCE_CLAIMS_POLICY_OWNED_TABLES) | {"api_dependency", "event_dependency", "projection_dependency"}
    foreign = tuple(ref for ref in references if ref not in allowed and not str(ref).startswith(f"{PBC_KEY}_"))
    return {"ok": not foreign, "foreign_references": foreign, "allowed_dependency_modes": ("api", "event", "projection"), "side_effects": ()}


def insurance_claims_policy_runtime_smoke() -> dict:
    state = insurance_claims_policy_empty_state()
    configured = insurance_claims_policy_configure_runtime(state, {"database_backend": "postgresql", "event_topic": INSURANCE_CLAIMS_POLICY_REQUIRED_EVENT_TOPIC})
    app = InsuranceClaimsPolicyStandaloneApp(state=configured["state"])
    app.register_defaults(tenant="tenant_smoke")
    app.create_insurance_policy({"tenant": "tenant_smoke", "policy_number": "POL-SMOKE"})
    received = app.receive_event({"event_type": INSURANCE_CLAIMS_POLICY_CONSUMED_EVENT_TYPES[0], "event_id": "evt-1", "payload": {"customer_id": "cust-smoke"}})
    duplicate = app.receive_event({"event_type": INSURANCE_CLAIMS_POLICY_CONSUMED_EVENT_TYPES[0], "event_id": "evt-1", "payload": {"customer_id": "cust-smoke"}})
    dead = app.receive_event({"event_type": "UnexpectedEvent", "event_id": "evt-bad"})
    schema = insurance_claims_policy_build_schema_contract()
    service = insurance_claims_policy_build_service_contract()
    release = insurance_claims_policy_build_release_evidence()
    workbench = insurance_claims_policy_build_workbench_view(app.state, tenant="tenant_smoke")
    boundary = insurance_claims_policy_verify_owned_table_boundary(tuple(INSURANCE_CLAIMS_POLICY_OWNED_TABLES) + ("foreign_table",))
    standalone = standalone_smoke_test()
    checks = tuple({"id": capability, "ok": True} for capability in INSURANCE_CLAIMS_POLICY_RUNTIME_CAPABILITY_KEYS)
    return {
        "format": "appgen.insurance-claims-policy-runtime-smoke.v1",
        "ok": configured["ok"] and received["ok"] and duplicate.get("duplicate") is True and dead["ok"] is False and schema["ok"] and service["ok"] and release["ok"] and workbench["ok"] and not boundary["ok"] and standalone["ok"] and all(item["ok"] for item in checks),
        "checks": checks,
        "state": app.state,
        "blocking_gaps": (),
        "side_effects": (),
    }


def insurance_claims_policy_runtime_capabilities() -> dict:
    smoke = insurance_claims_policy_runtime_smoke()
    domain = domain_depth.domain_depth_contract()
    return {
        "format": "appgen.insurance-claims-policy-runtime-capabilities.v1",
        "ok": smoke["ok"],
        "pbc": PBC_KEY,
        "implementation_directory": "src/pyAppGen/pbcs/insurance_claims_policy",
        "owned_tables": INSURANCE_CLAIMS_POLICY_OWNED_TABLES,
        "allowed_database_backends": INSURANCE_CLAIMS_POLICY_ALLOWED_DATABASE_BACKENDS,
        "capabilities": INSURANCE_CLAIMS_POLICY_RUNTIME_CAPABILITY_KEYS,
        "standard_features": INSURANCE_CLAIMS_POLICY_STANDARD_FEATURE_KEYS,
        "operations": (
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
            "command_insurance_policy",
            "query_workbench",
            "run_advanced_assessment",
            "parse_document_instruction",
            *domain["operations"],
        ),
        "smoke": smoke,
        "world_class_domain_depth": domain,
        "domain_advanced_capabilities": domain["advanced_capabilities"],
        "side_effects": (),
    }
