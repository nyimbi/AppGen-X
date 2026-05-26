"""UI contract for the Schema Registry PBC."""

from __future__ import annotations

from .runtime import SCHEMA_REGISTRY_ALLOWED_DATABASE_BACKENDS
from .runtime import SCHEMA_REGISTRY_CONSUMED_EVENT_TYPES
from .runtime import SCHEMA_REGISTRY_EMITTED_EVENT_TYPES
from .runtime import SCHEMA_REGISTRY_OWNED_TABLES
from .runtime import SCHEMA_REGISTRY_REQUIRED_EVENT_TOPIC
from .runtime import schema_registry_permissions_contract


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


def schema_registry_ui_contract() -> dict:
    return {
        "format": "appgen.schema-registry-ui-contract.v1",
        "ok": True,
        "pbc": "schema_registry",
        "implementation_directory": "src/pyAppGen/pbcs/schema_registry",
        "fragments": SCHEMA_REGISTRY_UI_FRAGMENT_KEYS,
        "routes": (
            "/workbench/pbcs/schema_registry",
            "/workbench/pbcs/schema_registry/subjects",
            "/workbench/pbcs/schema_registry/versions",
            "/workbench/pbcs/schema_registry/compatibility",
            "/workbench/pbcs/schema_registry/consumers",
            "/workbench/pbcs/schema_registry/validations",
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
        "format": "appgen.schema-registry-workbench-render.v1",
        "ok": True,
        "tenant": tenant,
        "route": "/workbench/pbcs/schema_registry",
        "fragments": contract["fragments"],
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
        },
    }
