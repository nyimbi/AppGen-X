"""UI contract for the Schema Registry PBC."""

from __future__ import annotations


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
        "action_permissions": {
            "register_subject": "schema_registry.register",
            "submit_schema_version": "schema_registry.register",
            "define_compatibility_rule": "schema_registry.approve",
            "register_consumer_binding": "schema_registry.register",
            "run_compatibility_check": "schema_registry.validate",
            "validate_payload": "schema_registry.validate",
            "record_contract_violation": "schema_registry.triage",
            "publish_contract_projection": "schema_registry.publish",
            "register_rule": "schema_registry.configure",
            "set_parameter": "schema_registry.configure",
            "configure_runtime": "schema_registry.configure",
            "run_control_tests": "schema_registry.audit",
        },
        "configuration_editor": {
            "required_fields": ("database_backend", "event_topic", "retry_limit", "default_compatibility", "default_timezone"),
            "allowed_database_backends": ("postgresql", "mysql", "mariadb"),
            "event_contract": "AppGen-X",
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
            "emits": ("SchemaSubjectRegistered", "SchemaAccepted", "BreakingSchemaBlocked", "PayloadValidated", "ContractViolationRecorded", "ContractProjectionPublished"),
            "consumes": ("PbcDeployed", "EventContractProposed", "RoutePublished", "AccessPolicyChanged", "PackageRegistrationRequested"),
            "outbox_status": "visible",
            "dead_letter_status": "visible",
        },
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
    }
