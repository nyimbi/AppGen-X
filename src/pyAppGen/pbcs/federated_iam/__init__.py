"""Federated Identity and Access PBC implementation package."""

from ..source_contract import source_pbc_package_contract
from .runtime import FEDERATED_IAM_RUNTIME_CAPABILITY_KEYS
from .runtime import FEDERATED_IAM_STANDARD_FEATURE_KEYS
from .runtime import federated_iam_approve_privileged_access
from .runtime import federated_iam_assign_role
from .runtime import federated_iam_build_workbench_view
from .runtime import federated_iam_configure_runtime
from .runtime import federated_iam_empty_state
from .runtime import federated_iam_evaluate_policy
from .runtime import federated_iam_grant_token
from .runtime import federated_iam_link_identity
from .runtime import federated_iam_provision_tenant
from .runtime import federated_iam_register_identity_provider
from .runtime import federated_iam_register_principal
from .runtime import federated_iam_register_rule
from .runtime import federated_iam_runtime_capabilities
from .runtime import federated_iam_runtime_smoke
from .runtime import federated_iam_set_parameter
from .runtime import federated_iam_verify_credential
from .ui import FEDERATED_IAM_UI_FRAGMENT_KEYS
from .ui import federated_iam_render_workbench
from .ui import federated_iam_ui_contract

PBC_KEY = "federated_iam"


def implementation_contract() -> dict:
    runtime = federated_iam_runtime_capabilities()
    contract = source_pbc_package_contract(PBC_KEY, tuple(runtime["capabilities"]))
    return {
        **contract,
        "standard_features": runtime["standard_features"],
        "advanced_runtime": runtime,
        "ui_contract": federated_iam_ui_contract(),
    }
