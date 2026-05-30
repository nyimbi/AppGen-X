"""Database-backed form contracts for the schema_registry standalone PBC."""

from __future__ import annotations


PBC_KEY = "schema_registry"

FORM_CATALOG = (
    {
        "key": "runtime_configuration_form",
        "title": "Runtime Configuration",
        "command": "configure_runtime",
        "route": "/api/pbc/schema_registry/runtime/configuration",
        "permission": "schema_registry.configure",
        "repository_method": "configure_runtime",
        "writes": ("schema_registry_schema_configuration",),
        "required_fields": ("database_backend", "event_topic", "retry_limit"),
        "fields": (
            {"name": "database_backend", "type": "select"},
            {"name": "event_topic", "type": "text"},
            {"name": "retry_limit", "type": "integer"},
            {"name": "default_compatibility", "type": "text"},
            {"name": "namespace_policy", "type": "text"},
            {"name": "default_timezone", "type": "text"},
        ),
    },
    {
        "key": "subject_registration_form",
        "title": "Schema Subject Registration",
        "command": "register_subject",
        "route": "/api/pbc/schema_registry/subjects",
        "permission": "schema_registry.register",
        "repository_method": "register_subject",
        "writes": ("schema_registry_schema_subject",),
        "required_fields": ("subject_id", "tenant", "owner_pbc", "name", "channel", "format", "namespace"),
        "fields": (
            {"name": "subject_id", "type": "text"},
            {"name": "tenant", "type": "text"},
            {"name": "owner_pbc", "type": "text"},
            {"name": "name", "type": "text"},
            {"name": "channel", "type": "select"},
            {"name": "format", "type": "select"},
            {"name": "namespace", "type": "text"},
        ),
    },
    {
        "key": "schema_version_form",
        "title": "Schema Version Submission",
        "command": "submit_schema_version",
        "route": "/api/pbc/schema_registry/versions",
        "permission": "schema_registry.register",
        "repository_method": "submit_schema_version",
        "writes": ("schema_registry_schema_version", "schema_registry_validation_run"),
        "required_fields": ("version_id", "tenant", "subject_id", "semantic_version", "schema"),
        "fields": (
            {"name": "version_id", "type": "text"},
            {"name": "tenant", "type": "text"},
            {"name": "subject_id", "type": "text"},
            {"name": "semantic_version", "type": "text"},
            {"name": "schema", "type": "json"},
        ),
    },
    {
        "key": "consumer_binding_form",
        "title": "Consumer Binding",
        "command": "register_consumer_binding",
        "route": "/api/pbc/schema_registry/consumer-bindings",
        "permission": "schema_registry.register",
        "repository_method": "register_consumer_binding",
        "writes": ("schema_registry_consumer_binding",),
        "required_fields": ("binding_id", "tenant", "subject_id", "consumer_pbc", "consumer_type", "min_version"),
        "fields": (
            {"name": "binding_id", "type": "text"},
            {"name": "tenant", "type": "text"},
            {"name": "subject_id", "type": "text"},
            {"name": "consumer_pbc", "type": "text"},
            {"name": "consumer_type", "type": "text"},
            {"name": "min_version", "type": "text"},
        ),
    },
    {
        "key": "compatibility_check_form",
        "title": "Compatibility Check",
        "command": "run_compatibility_check",
        "route": "/api/pbc/schema_registry/compatibility-checks",
        "permission": "schema_registry.validate",
        "repository_method": "run_compatibility_check",
        "writes": ("schema_registry_validation_run", "schema_registry_contract_violation"),
        "required_fields": ("subject_id", "proposed_schema"),
        "fields": (
            {"name": "subject_id", "type": "text"},
            {"name": "proposed_schema", "type": "json"},
        ),
    },
    {
        "key": "payload_validation_form",
        "title": "Payload Validation",
        "command": "validate_payload",
        "route": "/api/pbc/schema_registry/payload-validations",
        "permission": "schema_registry.validate",
        "repository_method": "validate_payload",
        "writes": ("schema_registry_validation_run", "schema_registry_payload_validation_error"),
        "required_fields": ("subject_id", "payload"),
        "fields": (
            {"name": "subject_id", "type": "text"},
            {"name": "payload", "type": "json"},
        ),
    },
    {
        "key": "violation_triage_form",
        "title": "Violation Triage",
        "command": "record_contract_violation",
        "route": "/api/pbc/schema_registry/violations",
        "permission": "schema_registry.triage",
        "repository_method": "record_contract_violation",
        "writes": ("schema_registry_contract_violation", "schema_registry_contract_remediation"),
        "required_fields": (
            "violation_id",
            "tenant",
            "subject_id",
            "producer_pbc",
            "consumer_pbc",
            "severity",
            "reason",
            "status",
        ),
        "fields": (
            {"name": "violation_id", "type": "text"},
            {"name": "tenant", "type": "text"},
            {"name": "subject_id", "type": "text"},
            {"name": "producer_pbc", "type": "text"},
            {"name": "consumer_pbc", "type": "text"},
            {"name": "severity", "type": "select"},
            {"name": "reason", "type": "textarea"},
            {"name": "status", "type": "select"},
        ),
    },
    {
        "key": "projection_publish_form",
        "title": "Projection Publication",
        "command": "publish_contract_projection",
        "route": "/api/pbc/schema_registry/projections",
        "permission": "schema_registry.publish",
        "repository_method": "publish_contract_projection",
        "writes": ("schema_registry_contract_projection", "schema_registry_appgen_outbox_event"),
        "required_fields": ("subject_id", "systems"),
        "fields": (
            {"name": "subject_id", "type": "text"},
            {"name": "systems", "type": "multiselect"},
        ),
    },
    {
        "key": "assistant_intake_form",
        "title": "Assistant Intake",
        "command": "document_instruction_plan",
        "route": "/assistant/pbc/schema_registry",
        "permission": "schema_registry.read",
        "repository_method": "none",
        "writes": (),
        "required_fields": ("document", "instructions"),
        "fields": (
            {"name": "document", "type": "textarea"},
            {"name": "instructions", "type": "textarea"},
        ),
    },
)


def schema_registry_form_catalog() -> tuple[dict, ...]:
    return FORM_CATALOG


def schema_registry_form_keys() -> tuple[str, ...]:
    return tuple(form["key"] for form in FORM_CATALOG)


def schema_registry_form_submission_plan(form_key: str, payload: dict | None = None) -> dict:
    form = next((item for item in FORM_CATALOG if item["key"] == form_key), None)
    if form is None:
        return {
            "ok": False,
            "pbc": PBC_KEY,
            "form_key": form_key,
            "reason": "unknown_form",
            "side_effects": (),
        }
    supplied = dict(payload or {})
    missing = tuple(field for field in form["required_fields"] if field not in supplied)
    return {
        "ok": not missing,
        "pbc": PBC_KEY,
        "form_key": form_key,
        "title": form["title"],
        "command": form["command"],
        "route": form["route"],
        "permission": form["permission"],
        "repository_method": form["repository_method"],
        "writes": form["writes"],
        "payload_keys": tuple(sorted(supplied)),
        "missing_fields": missing,
        "event_contract": "AppGen-X",
        "side_effects": (),
    }


def smoke_test() -> dict:
    """Exercise one mutation form and one assistant intake form."""
    subject_plan = schema_registry_form_submission_plan(
        "subject_registration_form",
        {
            "subject_id": "subject_smoke",
            "tenant": "tenant_smoke",
            "owner_pbc": "schema_registry",
            "name": "tenant_smoke.order.created",
            "channel": "event",
            "format": "json",
            "namespace": "tenant_smoke.orders",
        },
    )
    assistant_plan = schema_registry_form_submission_plan(
        "assistant_intake_form",
        {"document": "Need a schema for order.created", "instructions": "Draft additive migration plan"},
    )
    return {
        "ok": bool(FORM_CATALOG) and subject_plan["ok"] and assistant_plan["ok"],
        "forms": FORM_CATALOG,
        "subject_plan": subject_plan,
        "assistant_plan": assistant_plan,
        "side_effects": (),
    }
