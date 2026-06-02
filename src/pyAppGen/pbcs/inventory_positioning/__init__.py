"""Inventory Positioning PBC implementation package."""

from __future__ import annotations

from .agent import chatbot_interface_contract
from .agent import composed_agent_contribution
from .agent import datastore_crud_plan
from .agent import document_instruction_plan
from .manifest import PBC_MANIFEST
from .permissions import permission_manifest
from .release_evidence import build_release_evidence
from .routes import api_route_contracts
from .routes import dispatch_route
from .runtime import INVENTORY_POSITIONING_ALLOWED_DATABASE_BACKENDS
from .runtime import INVENTORY_POSITIONING_CONSUMED_EVENT_TYPES
from .runtime import INVENTORY_POSITIONING_EMITTED_EVENT_TYPES
from .runtime import INVENTORY_POSITIONING_OWNED_TABLES
from .runtime import INVENTORY_POSITIONING_REQUIRED_EVENT_TOPIC
from .runtime import INVENTORY_POSITIONING_RUNTIME_CAPABILITY_KEYS
from .runtime import INVENTORY_POSITIONING_STANDARD_FEATURE_KEYS
from .runtime import inventory_positioning_allocate_competing_channels
from .runtime import inventory_positioning_allocate_inventory
from .runtime import inventory_positioning_apply_quality_hold
from .runtime import inventory_positioning_build_api_contract
from .runtime import inventory_positioning_build_release_evidence
from .runtime import inventory_positioning_build_schema_contract
from .runtime import inventory_positioning_build_service_contract
from .runtime import inventory_positioning_build_workbench_view
from .runtime import inventory_positioning_calculate_availability
from .runtime import inventory_positioning_configure_runtime
from .runtime import inventory_positioning_detect_inventory_anomaly
from .runtime import inventory_positioning_empty_state
from .runtime import inventory_positioning_federate_inventory_view
from .runtime import inventory_positioning_forecast_stockout
from .runtime import inventory_positioning_generate_replenishment_signal
from .runtime import inventory_positioning_generate_stock_proof
from .runtime import inventory_positioning_model_stochastic_stock_exposure
from .runtime import inventory_positioning_optimize_allocation
from .runtime import inventory_positioning_parse_inventory_event
from .runtime import inventory_positioning_permissions_contract
from .runtime import inventory_positioning_post_adjustment
from .runtime import inventory_positioning_post_goods_receipt
from .runtime import inventory_positioning_receive_event
from .runtime import inventory_positioning_reconcile_inventory
from .runtime import inventory_positioning_register_governed_model
from .runtime import inventory_positioning_register_item
from .runtime import inventory_positioning_register_node
from .runtime import inventory_positioning_register_rule
from .runtime import inventory_positioning_register_schema_extension
from .runtime import inventory_positioning_release_allocation
from .runtime import inventory_positioning_route_allocation
from .runtime import inventory_positioning_rotate_crypto_epoch
from .runtime import inventory_positioning_run_control_tests
from .runtime import inventory_positioning_run_resilience_drill
from .runtime import inventory_positioning_runtime_capabilities
from .runtime import inventory_positioning_runtime_smoke
from .runtime import inventory_positioning_schedule_carbon_aware_fulfillment
from .runtime import inventory_positioning_score_stock_risk
from .runtime import inventory_positioning_screen_inventory_policy
from .runtime import inventory_positioning_set_parameter
from .runtime import inventory_positioning_simulate_allocation_policy
from .runtime import inventory_positioning_verify_formal_invariants
from .runtime import inventory_positioning_verify_node_identity
from .runtime import inventory_positioning_verify_owned_table_boundary
from .schema_contract import build_schema_contract
from .service_contract import build_service_contract
from .standalone import standalone_app_contract
from .ui import INVENTORY_POSITIONING_UI_FRAGMENT_KEYS
from .ui import inventory_positioning_render_workbench
from .ui import inventory_positioning_ui_contract

from ..source_contract import source_pbc_package_contract
from ..source_contract import source_package_metadata
from ..source_contract import source_registration_plan
from ..source_contract import validate_source_package_metadata


PBC_KEY = "inventory_positioning"


def implementation_contract() -> dict:
    runtime_capabilities = inventory_positioning_runtime_capabilities()
    contract = source_pbc_package_contract(PBC_KEY, tuple(runtime_capabilities["capabilities"]))
    return {
        **contract,
        "standard_features": runtime_capabilities["standard_features"],
        "owned_tables": INVENTORY_POSITIONING_OWNED_TABLES,
        "allowed_database_backends": INVENTORY_POSITIONING_ALLOWED_DATABASE_BACKENDS,
        "api_contract": api_route_contracts(),
        "schema_contract": build_schema_contract(),
        "service_contract": build_service_contract(),
        "release_evidence_contract": build_release_evidence(),
        "permissions_contract": permission_manifest(),
        "required_event_topic": INVENTORY_POSITIONING_REQUIRED_EVENT_TOPIC,
        "consumes": INVENTORY_POSITIONING_CONSUMED_EVENT_TYPES,
        "emits": INVENTORY_POSITIONING_EMITTED_EVENT_TYPES,
        "advanced_runtime": runtime_capabilities,
        "ui_contract": inventory_positioning_ui_contract(),
        "agent_contract": chatbot_interface_contract(),
        "agent_contribution": composed_agent_contribution(),
        "standalone_contract": standalone_app_contract(),
    }


def register_pbc() -> dict:
    return dict(PBC_MANIFEST)


def registration_plan(existing_catalog: dict | None = None) -> dict:
    return source_registration_plan(PBC_KEY, register_pbc(), existing_catalog=existing_catalog)


def package_metadata_manifest() -> dict:
    return source_package_metadata(PBC_KEY, register_pbc(), implementation_contract())


def validate_package_metadata() -> dict:
    return validate_source_package_metadata(package_metadata_manifest())


def package_discovery_plan(existing_catalog: dict | None = None) -> dict:
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
    discovery = package_discovery_plan()
    standalone = standalone_app_contract()
    return {
        "ok": discovery["ok"] and standalone["ok"],
        "discovery": discovery,
        "standalone": standalone,
        "side_effects": (),
    }
