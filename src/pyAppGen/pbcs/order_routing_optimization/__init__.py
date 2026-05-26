"""Order Routing Optimization PBC implementation package."""

from ..source_contract import source_pbc_package_contract
from .runtime import ORDER_ROUTING_OPTIMIZATION_RUNTIME_CAPABILITY_KEYS
from .runtime import ORDER_ROUTING_OPTIMIZATION_STANDARD_FEATURE_KEYS
from .runtime import order_routing_optimization_build_api_contract
from .runtime import order_routing_optimization_build_workbench_view
from .runtime import order_routing_optimization_clear_capacity_auction
from .runtime import order_routing_optimization_configure_runtime
from .runtime import order_routing_optimization_detect_routing_anomaly
from .runtime import order_routing_optimization_empty_state
from .runtime import order_routing_optimization_federate_routing_view
from .runtime import order_routing_optimization_forecast_capacity
from .runtime import order_routing_optimization_generate_routing_proof
from .runtime import order_routing_optimization_handle_event
from .runtime import order_routing_optimization_ingest_capacity_snapshot
from .runtime import order_routing_optimization_optimize_route_network
from .runtime import order_routing_optimization_parse_route_request
from .runtime import order_routing_optimization_recommend_exception_resolution
from .runtime import order_routing_optimization_register_governed_model
from .runtime import order_routing_optimization_register_rule
from .runtime import order_routing_optimization_register_schema_extension
from .runtime import order_routing_optimization_reserve_node_capacity
from .runtime import order_routing_optimization_rotate_crypto_epoch
from .runtime import order_routing_optimization_route_orders
from .runtime import order_routing_optimization_run_control_tests
from .runtime import order_routing_optimization_run_resilience_drill
from .runtime import order_routing_optimization_runtime_capabilities
from .runtime import order_routing_optimization_runtime_smoke
from .runtime import order_routing_optimization_schedule_carbon_aware_route
from .runtime import order_routing_optimization_score_fulfillment_risk
from .runtime import order_routing_optimization_screen_policy
from .runtime import order_routing_optimization_self_heal_route_selection
from .runtime import order_routing_optimization_set_parameter
from .runtime import order_routing_optimization_simulate_counterfactual
from .runtime import order_routing_optimization_model_stochastic_exposure
from .runtime import order_routing_optimization_upsert_route_candidate
from .ui import ORDER_ROUTING_OPTIMIZATION_UI_FRAGMENT_KEYS
from .ui import order_routing_optimization_render_workbench
from .ui import order_routing_optimization_ui_contract

PBC_KEY = "order_routing_optimization"


def implementation_contract() -> dict:
    runtime = order_routing_optimization_runtime_capabilities()
    contract = source_pbc_package_contract(PBC_KEY, tuple(runtime["capabilities"]))
    return {
        **contract,
        "standard_features": runtime["standard_features"],
        "advanced_runtime": runtime,
        "ui_contract": order_routing_optimization_ui_contract(),
    }
