"""World-class domain depth contract for the food_safety_quality_compliance PBC."""

from .slice_app import DOMAIN_ADVANCED_CAPABILITIES
from .slice_app import DOMAIN_EDGE_CASES
from .slice_app import DOMAIN_OPERATIONS
from .slice_app import DOMAIN_PARAMETERS
from .slice_app import DOMAIN_RULES
from .slice_app import OWNED_TABLES as DOMAIN_OWNED_TABLES
from .slice_app import WORKBENCH_VIEWS as DOMAIN_WORKBENCH_VIEWS
from .slice_app import domain_capability_surface_contract
from .slice_app import domain_depth_contract
from .slice_app import execute_domain_operation

DOMAIN_EVENTS = (
    "FoodSafetyQualityComplianceCreated",
    "FoodSafetyQualityComplianceUpdated",
    "FoodSafetyQualityComplianceApproved",
    "FoodSafetyQualityComplianceExceptionOpened",
)
DOMAIN_CONSUMED_EVENTS = ("PolicyChanged", "AuditEventSealed", "OperationalKpiChanged")


def domain_depth_smoke_test() -> dict:
    contract = domain_depth_contract()
    executions = tuple(execute_domain_operation(operation, {"tenant": "tenant-smoke"}) for operation in DOMAIN_OPERATIONS[:5])
    return {
        "ok": contract["ok"] and len(contract["owned_tables"]) >= contract["minimum_owned_domain_tables"] and all(item["ok"] for item in executions),
        "contract": contract,
        "executions": executions,
        "side_effects": (),
    }


DOMAIN_SPECIALIST_CAPABILITIES = tuple(dict.fromkeys(DOMAIN_ADVANCED_CAPABILITIES + tuple(f"specialist_{operation}" for operation in DOMAIN_OPERATIONS)))
