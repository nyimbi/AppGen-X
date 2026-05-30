"""Federated Identity and Access PBC implementation package."""

from __future__ import annotations

from .manifest import PBC_MANIFEST
from .release_evidence import build_release_evidence as package_build_release_evidence
from .schema_contract import build_schema_contract as package_build_schema_contract
from .service_contract import build_service_contract as package_build_service_contract
from .standalone import create_standalone_app
from .standalone import standalone_manifest

from ..source_contract import source_package_metadata
from ..source_contract import source_pbc_package_contract
from ..source_contract import source_registration_plan
from ..source_contract import validate_source_package_metadata
from .runtime import FEDERATED_IAM_ALLOWED_DATABASE_BACKENDS
from .runtime import FEDERATED_IAM_CONSUMED_EVENT_TYPES
from .runtime import FEDERATED_IAM_EMITTED_EVENT_TYPES
from .runtime import FEDERATED_IAM_OWNED_TABLES
from .runtime import FEDERATED_IAM_REQUIRED_EVENT_TOPIC
from .runtime import FEDERATED_IAM_RUNTIME_CAPABILITY_KEYS
from .runtime import FEDERATED_IAM_RUNTIME_TABLES
from .runtime import FEDERATED_IAM_STANDARD_FEATURE_KEYS
from .runtime import federated_iam_approve_privileged_access
from .runtime import federated_iam_assign_role
from .runtime import federated_iam_build_api_contract
from .runtime import federated_iam_build_workbench_view
from .runtime import federated_iam_configure_runtime
from .runtime import federated_iam_empty_state
from .runtime import federated_iam_evaluate_policy
from .runtime import federated_iam_grant_token
from .runtime import federated_iam_link_identity
from .runtime import federated_iam_permissions_contract
from .runtime import federated_iam_provision_tenant
from .runtime import federated_iam_receive_event
from .runtime import federated_iam_register_identity_provider
from .runtime import federated_iam_register_principal
from .runtime import federated_iam_register_rule
from .runtime import federated_iam_register_schema_extension
from .runtime import federated_iam_runtime_capabilities
from .runtime import federated_iam_runtime_smoke
from .runtime import federated_iam_set_parameter
from .runtime import federated_iam_verify_credential
from .runtime import federated_iam_verify_owned_table_boundary
from .ui import FEDERATED_IAM_UI_FRAGMENT_KEYS
from .ui import federated_iam_render_workbench
from .ui import federated_iam_ui_contract

PBC_KEY = "federated_iam"


def federated_iam_build_schema_contract() -> dict:
    """Return the package-local schema contract while preserving legacy exports."""
    return package_build_schema_contract()


def federated_iam_build_service_contract() -> dict:
    """Return the package-local service contract while preserving legacy exports."""
    return package_build_service_contract()


def federated_iam_build_release_evidence() -> dict:
    """Return the package-local release evidence while preserving legacy exports."""
    return package_build_release_evidence()


def implementation_contract() -> dict:
    runtime = federated_iam_runtime_capabilities()
    contract = source_pbc_package_contract(PBC_KEY, tuple(runtime["capabilities"]))
    return {
        **contract,
        "standard_features": runtime["standard_features"],
        "advanced_runtime": runtime,
        "ui_contract": federated_iam_ui_contract(),
        "api_contract": federated_iam_build_api_contract(),
        "schema_contract": federated_iam_build_schema_contract(),
        "service_contract": federated_iam_build_service_contract(),
        "release_evidence_contract": federated_iam_build_release_evidence(),
        "permissions_contract": federated_iam_permissions_contract(),
        "standalone_manifest": standalone_manifest(),
        "owned_tables": FEDERATED_IAM_OWNED_TABLES,
        "runtime_tables": FEDERATED_IAM_RUNTIME_TABLES,
        "allowed_database_backends": FEDERATED_IAM_ALLOWED_DATABASE_BACKENDS,
        "required_event_topic": FEDERATED_IAM_REQUIRED_EVENT_TOPIC,
        "consumes": FEDERATED_IAM_CONSUMED_EVENT_TYPES,
        "emits": FEDERATED_IAM_EMITTED_EVENT_TYPES,
    }


def register_pbc() -> dict:
    """Return this PBC manifest without mutating global catalog state."""
    return dict(PBC_MANIFEST)


def registration_plan(existing_catalog: dict | None = None) -> dict:
    """Return a side-effect-free registration plan for this PBC package."""
    return source_registration_plan(
        PBC_KEY,
        register_pbc(),
        existing_catalog=existing_catalog,
    )


def package_metadata_manifest() -> dict:
    """Return package identity, artifacts, and discovery metadata."""
    return source_package_metadata(PBC_KEY, register_pbc(), implementation_contract())


def validate_package_metadata() -> dict:
    """Validate package metadata without mutating catalog state."""
    return validate_source_package_metadata(package_metadata_manifest())


def package_discovery_plan(existing_catalog: dict | None = None) -> dict:
    """Return side-effect-free package discovery and registration evidence."""
    metadata_validation = validate_package_metadata()
    registration = registration_plan(existing_catalog=existing_catalog)
    return {
        "format": "appgen.pbc-source-package-discovery-plan.v1",
        "ok": metadata_validation["ok"] and registration["ok"],
        "pbc": PBC_KEY,
        "metadata_validation": metadata_validation,
        "registration": registration,
        "side_effects": (),
    }


def smoke_test() -> dict:
    """Exercise package metadata validation, standalone manifest, and discovery planning."""
    discovery = package_discovery_plan()
    standalone = standalone_manifest()
    return {
        "ok": discovery["ok"] and standalone["ok"],
        "discovery": discovery,
        "standalone": standalone,
        "side_effects": (),
    }
