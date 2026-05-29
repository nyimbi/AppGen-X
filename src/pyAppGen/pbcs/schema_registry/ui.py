"""UI contract for the Schema Registry standalone PBC."""

from __future__ import annotations

from .forms import schema_registry_form_catalog
from .forms import schema_registry_form_keys
from .runtime import SCHEMA_REGISTRY_ALLOWED_DATABASE_BACKENDS
from .runtime import SCHEMA_REGISTRY_CONSUMED_EVENT_TYPES
from .runtime import SCHEMA_REGISTRY_EMITTED_EVENT_TYPES
from .runtime import SCHEMA_REGISTRY_OWNED_TABLES
from .runtime import SCHEMA_REGISTRY_REQUIRED_EVENT_TOPIC
from .runtime import schema_registry_permissions_contract
from .wizards import schema_registry_wizard_catalog
from .wizards import schema_registry_wizard_keys


SCHEMA_REGISTRY_UI_FRAGMENT_KEYS = (
    "SchemaRegistryWorkbench",
    "SubjectCatalog",
    "SchemaVersionEditor",
    "CompatibilityStudio",
    "ConsumerImpactMap",
    "PayloadValidationConsole",
    "ContractViolationBoard",
    "ContractProjectionPublisher",
    "SchemaAuditEvidenceView",
    "SchemaRuleStudio",
    "SchemaParameterConsole",
    "SchemaConfigurationPanel",
)
SCHEMA_REGISTRY_FORM_KEYS = schema_registry_form_keys()
SCHEMA_REGISTRY_WIZARD_KEYS = schema_registry_wizard_keys()
SCHEMA_REGISTRY_CONTROL_KEYS = (
    "tenant_scope_picker",
    "compatibility_heatmap",
    "consumer_blast_radius_graph",
    "validation_timeline",
    "assistant_guidance_drawer",
    "release_gate_banner",
)


def schema_registry_control_catalog() -> tuple[dict, ...]:
    return (
        {"key": "tenant_scope_picker", "type": "selector", "binds_to": "tenant"},
        {"key": "compatibility_heatmap", "type": "matrix", "binds_to": "validation_runs"},
        {"key": "consumer_blast_radius_graph", "type": "graph", "binds_to": "consumer_bindings"},
        {"key": "validation_timeline", "type": "timeline", "binds_to": "events"},
        {"key": "assistant_guidance_drawer", "type": "drawer", "binds_to": "agent"},
        {"key": "release_gate_banner", "type": "banner", "binds_to": "release_evidence"},
    )


def schema_registry_standalone_app_contract() -> dict:
    return {
        "ok": True,
        "pbc": "schema_registry",
        "app_id": "schema_registry_one_pbc_app",
        "workbench_route": "/workbench/pbcs/schema_registry",
        "navigation": (
            {"key": "subjects", "route": "/workbench/pbcs/schema_registry/subjects"},
            {"key": "versions", "route": "/workbench/pbcs/schema_registry/versions"},
            {"key": "compatibility", "route": "/workbench/pbcs/schema_registry/compatibility"},
            {"key": "consumers", "route": "/workbench/pbcs/schema_registry/consumers"},
            {"key": "validations", "route": "/workbench/pbcs/schema_registry/validations"},
            {"key": "release", "route": "/workbench/pbcs/schema_registry/release"},
        ),
        "forms": SCHEMA_REGISTRY_FORM_KEYS,
        "wizards": SCHEMA_REGISTRY_WIZARD_KEYS,
        "controls": SCHEMA_REGISTRY_CONTROL_KEYS,
        "single_agent_namespace": "schema_registry_skills",
        "side_effects": (),
    }


def schema_registry_ui_contract() -> dict:
    return {
        "format": "appgen.schema-registry-ui-contract.v2",
        "ok": True,
        "pbc": "schema_registry",
        "implementation_directory": "src/pyAppGen/pbcs/schema_registry",
        "fragments": SCHEMA_REGISTRY_UI_FRAGMENT_KEYS,
        "routes": tuple(item["route"] for item in schema_registry_standalone_app_contract()["navigation"]) + (
            "/workbench/pbcs/schema_registry",
            "/workbench/pbcs/schema_registry/violations",
            "/workbench/pbcs/schema_registry/projections",
            "/workbench/pbcs/schema_registry/rules",
            "/workbench/pbcs/schema_registry/parameters",
            "/workbench/pbcs/schema_registry/configuration",
        ),
        "panels": (
            {
                "key": "registry",
                "fragment": "SubjectCatalog",
                "binds_to": ("schema_subject", "schema_version", "consumer_binding"),
                "commands": ("register_subject", "submit_schema_version", "register_consumer_binding"),
            },
            {
                "key": "compatibility",
                "fragment": "CompatibilityStudio",
                "binds_to": ("compatibility_rule", "validation_run", "contract_violation"),
                "commands": ("define_compatibility_rule", "run_compatibility_check", "record_contract_violation"),
            },
            {
                "key": "validation",
                "fragment": "PayloadValidationConsole",
                "binds_to": ("schema_version", "validation_run", "outbox"),
                "commands": ("validate_payload", "publish_contract_projection", "run_control_tests"),
            },
            {
                "key": "governance",
                "fragment": "SchemaRuleStudio",
                "binds_to": ("rule", "parameter", "configuration"),
                "commands": ("register_rule", "set_parameter", "configure_runtime"),
            },
        ),
        "forms": schema_registry_form_catalog(),
        "wizards": schema_registry_wizard_catalog(),
        "controls": schema_registry_control_catalog(),
        "standalone_app": schema_registry_standalone_app_contract(),
        "action_permissions": schema_registry_permissions_contract()["action_permissions"],
        "configuration_editor": {
            "required_fields": ("database_backend", "event_topic", "retry_limit", "default_compatibility", "default_timezone"),
            "allowed_database_backends": SCHEMA_REGISTRY_ALLOWED_DATABASE_BACKENDS,
            "required_event_topic": SCHEMA_REGISTRY_REQUIRED_EVENT_TOPIC,
            "event_contract": "AppGen-X",
            "stream_engine_picker_visible": False,
            "user_selectable_event_contract": False,
        },
        "parameter_editor": {
            "numeric_parameters": (
                "compatibility_threshold",
                "max_schema_fields",
                "semantic_similarity_floor",
                "violation_risk_threshold",
                "review_sla_hours",
                "retention_days",
            ),
        },
        "rule_editor": {
            "rule_types": ("compatibility", "classification", "payload", "consumer", "projection", "release_gate"),
            "required_fields": ("rule_id", "tenant", "scope", "mode", "classification", "severity", "status"),
        },
        "event_surfaces": {
            "emits": SCHEMA_REGISTRY_EMITTED_EVENT_TYPES,
            "consumes": SCHEMA_REGISTRY_CONSUMED_EVENT_TYPES,
            "outbox_status": "visible",
            "inbox_status": "visible",
            "dead_letter_status": "visible",
        },
        "binding_evidence": {"owned_tables": SCHEMA_REGISTRY_OWNED_TABLES, "shared_table_access": False},
    }


def schema_registry_render_workbench(
    state: dict,
    *,
    tenant: str,
    principal_permissions: tuple[str, ...],
) -> dict:
    contract = schema_registry_ui_contract()
    shell = schema_registry_standalone_app_contract()
    permissions = set(principal_permissions)
    visible_actions = tuple(action for action, required in contract["action_permissions"].items() if required in permissions)
    subjects = tuple(subject for subject in state["subjects"].values() if subject["tenant"] == tenant)
    subject_ids = {subject["subject_id"] for subject in subjects}
    versions = tuple(version for version in state["versions"].values() if version["subject_id"] in subject_ids)
    validations = tuple(run for run in state["validation_runs"].values() if run["subject_id"] in subject_ids)
    violations = tuple(violation for violation in state["violations"].values() if violation["tenant"] == tenant)
    cards = (
        {"key": "subjects", "value": len(subjects), "fragment": "SubjectCatalog"},
        {"key": "versions", "value": len(versions), "fragment": "SchemaVersionEditor"},
        {"key": "validations", "value": len(validations), "fragment": "PayloadValidationConsole"},
        {"key": "violations", "value": len(violations), "fragment": "ContractViolationBoard"},
        {"key": "release_blocking", "value": len(tuple(item for item in violations if item["release_blocking"])), "fragment": "ContractViolationBoard"},
    )
    return {
        "format": "appgen.schema-registry-workbench-render.v2",
        "ok": True,
        "tenant": tenant,
        "route": shell["workbench_route"],
        "fragments": contract["fragments"],
        "navigation": shell["navigation"],
        "forms": contract["forms"],
        "wizards": contract["wizards"],
        "controls": contract["controls"],
        "cards": cards,
        "visible_actions": visible_actions,
        "locked_actions": tuple(action for action in contract["action_permissions"] if action not in visible_actions),
        "configuration_bound": bool(state["configuration"].get("ok")),
        "rules_bound": tuple(sorted(state["rules"])),
        "parameters_bound": tuple(sorted(state["parameters"])),
        "event_outbox_count": len(state["outbox"]),
        "inbox_count": len(state.get("inbox", ())),
        "dead_letter_count": len(state.get("dead_letter", state.get("dead_letters", ()))),
        "binding_evidence": {
            "owned_tables": SCHEMA_REGISTRY_OWNED_TABLES,
            "outbox_table": "schema_registry_appgen_outbox_event",
            "inbox_table": "schema_registry_appgen_inbox_event",
            "dead_letter_table": "schema_registry_dead_letter_event",
            "shared_table_access": False,
            "required_event_topic": SCHEMA_REGISTRY_REQUIRED_EVENT_TOPIC,
        },
    }


def schema_registry_render_standalone_app(
    state: dict,
    *,
    tenant: str,
    principal_permissions: tuple[str, ...],
) -> dict:
    return {
        "ok": True,
        "pbc": "schema_registry",
        "shell": schema_registry_standalone_app_contract(),
        "workbench": schema_registry_render_workbench(
            state,
            tenant=tenant,
            principal_permissions=principal_permissions,
        ),
        "side_effects": (),
    }


class _AppGenSmokeState(dict):
    """Tolerant empty state for side-effect-free workbench smoke rendering."""

    def __missing__(self, key):
        value = _AppGenSmokeState()
        self[key] = value
        return value


def _appgen_smoke_state():
    """Return a deterministic state envelope understood by PBC workbench renderers."""
    return _AppGenSmokeState({
        "configuration": _AppGenSmokeState({"ok": True}),
        "rules": _AppGenSmokeState(),
        "parameters": _AppGenSmokeState(),
        "outbox": (),
        "inbox": (),
        "dead_letter": (),
        "dead_letters": (),
        "events": (),
        "subjects": {},
        "versions": {},
        "validation_runs": {},
        "violations": {},
        "consumer_bindings": {},
    })


def smoke_test():
    """Exercise the PBC workbench contract and render path without side effects."""
    contract = schema_registry_ui_contract()
    permissions = tuple(dict.fromkeys(contract.get("action_permissions", {}).values()))
    rendered = schema_registry_render_standalone_app(
        _appgen_smoke_state(),
        tenant="smoke",
        principal_permissions=permissions,
    )
    workbench = rendered["workbench"]
    cards = tuple(workbench.get("cards") or contract.get("panels") or contract.get("fragments", ()))
    configuration_editor = contract.get("configuration_editor", {})
    event_surfaces = contract.get("event_surfaces", {})
    rule_editor = contract.get("rule_editor") or {
        "rule_types": ("configuration", "parameter", "release_gate"),
        "required_fields": ("rule_id", "scope", "status"),
    }
    binding_evidence = contract.get("binding_evidence") or {"shared_table_access": False}
    governance = {
        "configuration_editor": configuration_editor,
        "parameter_editor": contract.get("parameter_editor", {}),
        "rule_editor": rule_editor,
        "event_surfaces": event_surfaces,
        "binding_evidence": binding_evidence,
    }
    return {
        "format": "appgen.pbc-ui-smoke-test.v2",
        "ok": contract.get("ok") is True
        and rendered.get("ok") is True
        and bool(contract.get("fragments"))
        and bool(contract.get("routes"))
        and bool(cards)
        and bool(contract.get("forms"))
        and bool(contract.get("wizards"))
        and bool(contract.get("controls"))
        and bool(contract.get("action_permissions"))
        and bool(configuration_editor)
        and configuration_editor.get("stream_engine_picker_visible", configuration_editor.get("user_facing_stream_engine_picker", False)) is False
        and bool(contract.get("parameter_editor"))
        and bool(rule_editor)
        and bool(event_surfaces)
        and ("outbox_status" in event_surfaces or "contract" in event_surfaces)
        and binding_evidence.get("shared_table_access") is not True
        and not binding_evidence.get("shared_tables", ()),
        "manifest": {"fragments": contract.get("fragments", ()), "routes": contract.get("routes", ())},
        "contract": contract,
        "governance": governance,
        "rendered": workbench,
        "cards": cards,
        "side_effects": (),
    }
