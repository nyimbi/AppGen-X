"""General Ledger Core PBC implementation package."""

from ..source_contract import source_pbc_package_contract
from .runtime import GL_CORE_STANDARD_FEATURE_KEYS
from .runtime import gl_core_append_ledger_event
from .runtime import gl_core_build_federated_view
from .runtime import gl_core_build_projection
from .runtime import gl_core_compile_regulatory_rules
from .runtime import gl_core_consolidate_private_balances
from .runtime import gl_core_create_continuous_close_snapshot
from .runtime import gl_core_derive_account_from_semantics
from .runtime import gl_core_empty_state
from .runtime import gl_core_evaluate_policy
from .runtime import gl_core_generate_audit_proof
from .runtime import gl_core_measure_information_auditability
from .runtime import gl_core_predict_posting_validation
from .runtime import gl_core_query_temporal_ledger
from .runtime import gl_core_register_financial_model
from .runtime import gl_core_register_schema_extension
from .runtime import gl_core_replicate_consensus
from .runtime import gl_core_resolve_reconciliation_game
from .runtime import gl_core_rotate_crypto_epoch
from .runtime import gl_core_run_causal_scenario
from .runtime import gl_core_run_control_tests
from .runtime import gl_core_run_resilience_drill
from .runtime import gl_core_runtime_capabilities
from .runtime import gl_core_runtime_smoke
from .runtime import gl_core_schedule_carbon_aware_execution
from .runtime import gl_core_simulate_probabilistic_posting
from .runtime import gl_core_suggest_reconciliation
from .runtime import gl_core_verify_formal_invariants
from .runtime import gl_core_verify_identity_credential

PBC_KEY = "gl_core"


def implementation_contract() -> dict:
    runtime = gl_core_runtime_capabilities()
    contract = source_pbc_package_contract(PBC_KEY, tuple(runtime["capabilities"]))
    return {
        **contract,
        "standard_features": runtime["standard_features"],
        "advanced_runtime": runtime,
    }
