"""Package manifest for the federated_iam PBC."""

from __future__ import annotations

from .runtime import FEDERATED_IAM_CONSUMED_EVENT_TYPES
from .runtime import FEDERATED_IAM_EMITTED_EVENT_TYPES
from .runtime import FEDERATED_IAM_OWNED_TABLES
from .runtime import FEDERATED_IAM_RUNTIME_CAPABILITY_KEYS
from .runtime import FEDERATED_IAM_RUNTIME_TABLES
from .runtime import FEDERATED_IAM_STANDARD_FEATURE_KEYS
from .runtime import federated_iam_build_api_contract
from .ui import FEDERATED_IAM_UI_FRAGMENT_KEYS


_API_CONTRACT = federated_iam_build_api_contract()

PBC_MANIFEST = {
    "pbc": "federated_iam",
    "label": "Federated Identity and Access Management",
    "mesh": "platform",
    "description": "Tenant, principal, identity provider, identity link, role, policy, token, session, credential verification, privileged access, standalone workbench, agent/chatbot, and AppGen-X identity event orchestration.",
    "datastore_backend": "postgresql",
    "tables": FEDERATED_IAM_OWNED_TABLES + FEDERATED_IAM_RUNTIME_TABLES,
    "apis": tuple(route["route"] for route in _API_CONTRACT["routes"]),
    "emits": FEDERATED_IAM_EMITTED_EVENT_TYPES,
    "consumes": FEDERATED_IAM_CONSUMED_EVENT_TYPES,
    "template": None,
    "ui_fragments": FEDERATED_IAM_UI_FRAGMENT_KEYS,
    "permissions": (
        "federated_iam.read",
        "federated_iam.tenant",
        "federated_iam.principal",
        "federated_iam.policy",
        "federated_iam.token",
        "federated_iam.privileged",
        "federated_iam.event",
        "federated_iam.configure",
        "federated_iam.audit",
    ),
    "configuration": (
        "FEDERATED_IAM_DATABASE_URL",
        "FEDERATED_IAM_EVENT_TOPIC",
        "FEDERATED_IAM_RETRY_LIMIT",
        "FEDERATED_IAM_DEFAULT_TIMEZONE",
        "FEDERATED_IAM_ALLOWED_REGIONS",
        "FEDERATED_IAM_ALLOWED_PROVIDER_TYPES",
        "FEDERATED_IAM_ALLOWED_GRANT_TYPES",
    ),
    "capabilities": tuple(f"federated_iam.{table}" for table in FEDERATED_IAM_OWNED_TABLES + FEDERATED_IAM_RUNTIME_TABLES),
    "standard_features": FEDERATED_IAM_STANDARD_FEATURE_KEYS,
    "workflows": (
        "tenant_onboarding",
        "provider_linking",
        "credential_verification",
        "role_assignment",
        "policy_decisioning",
        "token_grant",
        "privileged_access_approval",
        "event_inbox_processing",
        "workbench_query",
        "assistant_document_planning",
    ),
    "analytics": (
        "policy_latency",
        "access_risk",
        "tenant_isolation_health",
        "token_grant_rate",
        "privileged_access_risk",
        "principal_verified_throughput",
        "access_policy_changed_throughput",
    ),
    "advanced_capabilities": FEDERATED_IAM_RUNTIME_CAPABILITY_KEYS,
    "migrations": ("migrations/001_initial.sql",),
    "seed_data": ("seed_data.py",),
    "tests": (
        "tests/test_contract.py",
        "tests/test_runtime_capabilities.py",
        "tests/test_standalone.py",
    ),
    "docs": (
        "README.md",
        "RELEASE_EVIDENCE.md",
        "SPECIFICATION.md",
        "implementation-plan.md",
        "implementation-status.md",
    ),
}
