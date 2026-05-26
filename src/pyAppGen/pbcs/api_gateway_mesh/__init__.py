"""API Gateway Mesh PBC implementation package."""

from ..source_contract import source_pbc_package_contract
from .runtime import API_GATEWAY_MESH_RUNTIME_CAPABILITY_KEYS
from .runtime import API_GATEWAY_MESH_STANDARD_FEATURE_KEYS
from .runtime import api_gateway_mesh_apply_rate_limit
from .runtime import api_gateway_mesh_build_service_map
from .runtime import api_gateway_mesh_build_workbench_view
from .runtime import api_gateway_mesh_configure_runtime
from .runtime import api_gateway_mesh_empty_state
from .runtime import api_gateway_mesh_publish_route
from .runtime import api_gateway_mesh_record_health
from .runtime import api_gateway_mesh_record_traffic_sample
from .runtime import api_gateway_mesh_register_mtls_identity
from .runtime import api_gateway_mesh_register_rule
from .runtime import api_gateway_mesh_register_service
from .runtime import api_gateway_mesh_runtime_capabilities
from .runtime import api_gateway_mesh_runtime_smoke
from .runtime import api_gateway_mesh_set_parameter
from .ui import API_GATEWAY_MESH_UI_FRAGMENT_KEYS
from .ui import api_gateway_mesh_render_workbench
from .ui import api_gateway_mesh_ui_contract

PBC_KEY = "api_gateway_mesh"


def implementation_contract() -> dict:
    runtime = api_gateway_mesh_runtime_capabilities()
    contract = source_pbc_package_contract(PBC_KEY, tuple(runtime["capabilities"]))
    return {
        **contract,
        "standard_features": runtime["standard_features"],
        "advanced_runtime": runtime,
        "ui_contract": api_gateway_mesh_ui_contract(),
    }
