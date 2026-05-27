"""Package manifest for the schema_registry PBC."""

from .runtime import SCHEMA_REGISTRY_CONSUMED_EVENT_TYPES
from .runtime import SCHEMA_REGISTRY_EMITTED_EVENT_TYPES
from .runtime import SCHEMA_REGISTRY_OWNED_TABLES
from .runtime import SCHEMA_REGISTRY_RUNTIME_CAPABILITY_KEYS
from .runtime import SCHEMA_REGISTRY_STANDARD_FEATURE_KEYS
from .runtime import schema_registry_build_api_contract


PBC_MANIFEST = {
    "pbc": 'schema_registry',
    "label": "Schema Registry and Contract Validation",
    "mesh": "platform",
    "description": "Contract-first subject catalog, schema versioning, compatibility gates, payload validation, impact analysis, projection publication, and governed schema evolution.",
    "datastore_backend": "postgresql",
    "tables": SCHEMA_REGISTRY_OWNED_TABLES,
    "apis": tuple(route["route"] for route in schema_registry_build_api_contract()["routes"]),
    "emits": SCHEMA_REGISTRY_EMITTED_EVENT_TYPES,
    "consumes": SCHEMA_REGISTRY_CONSUMED_EVENT_TYPES,
    "template": None,
    "ui_fragments": (
        "SchemaRegistryWorkbench",
        "SubjectCatalogConsole",
        "SchemaVersionWorkbench",
        "CompatibilityPolicyPanel",
        "PayloadValidationConsole",
        "ConsumerImpactBoard",
        "ContractViolationTriage",
        "ProjectionPublicationPanel",
        "SchemaGovernancePanel",
    ),
    "permissions": (
        "schema_registry.register",
        "schema_registry.approve",
        "schema_registry.validate",
        "schema_registry.triage",
        "schema_registry.publish",
        "schema_registry.event",
        "schema_registry.configure",
        "schema_registry.audit",
        "schema_registry.read",
    ),
    "configuration": (
        "SCHEMA_REGISTRY_DATABASE_URL",
        "SCHEMA_REGISTRY_EVENT_TOPIC",
        "SCHEMA_REGISTRY_RETRY_LIMIT",
        "SCHEMA_REGISTRY_DEFAULT_TIMEZONE",
        "SCHEMA_REGISTRY_ALLOWED_FORMATS",
        "SCHEMA_REGISTRY_DEFAULT_COMPATIBILITY",
        "SCHEMA_REGISTRY_NAMESPACE_POLICY",
    ),
    "capabilities": tuple(f"schema_registry.{table}" for table in SCHEMA_REGISTRY_OWNED_TABLES),
    "standard_features": SCHEMA_REGISTRY_STANDARD_FEATURE_KEYS,
    "workflows": (
        "command_subject_registration",
        "command_schema_version_submission",
        "command_compatibility_checks",
        "command_payload_validation",
        "command_contract_violations",
        "command_contract_projections",
        "command_event_inbox",
        "query_schema_registry_workbench",
    ),
    "analytics": (
        "schema_acceptance_rate",
        "breaking_change_block_rate",
        "payload_validation_latency",
        "consumer_impact_exposure",
        "contract_violation_age",
        "projection_publish_latency",
        "policy_screening_clearance",
        "schema_accepted_throughput",
        "breaking_schema_blocked_throughput",
    ),
    "advanced_capabilities": SCHEMA_REGISTRY_RUNTIME_CAPABILITY_KEYS,
    "migrations": ("migrations/001_initial.sql",),
    "seed_data": ("seed_data.py",),
    "tests": ("tests/test_contract.py",),
    "docs": ("RELEASE_EVIDENCE.md", "SPECIFICATION.md"),
}
