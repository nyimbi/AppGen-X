"""Package-local capability assurance for the multi_sided_market PBC."""
from .manifest import PBC_MANIFEST
from .runtime import MULTI_SIDED_MARKET_ALLOWED_DATABASE_BACKENDS, multi_sided_market_runtime_capabilities

PBC_KEY = "multi_sided_market"

STANDARD_FEATURE_OPERATION_COVERAGE = {
    "participant_onboarding": ("verify_participant", "command_market_participants"),
    "seller_buyer_provider_borrower_roles": ("verify_participant",),
    "goods_listing": ("publish_listing", "register_listing_asset", "command_market_listings"),
    "service_listing": ("create_service_offer", "command_market_service_offers"),
    "availability_calendar": ("publish_availability_window", "command_market_availability_windows"),
    "booking_reservation": ("reserve_booking", "command_market_bookings"),
    "rental_contracting": ("start_rental", "command_market_rentals"),
    "loan_agreement_management": ("issue_loan", "command_market_loans"),
    "barter_negotiation": ("match_barter_offer", "command_market_barter_offers"),
    "trade_order_management": ("place_trade_order", "command_market_trade_orders"),
    "direct_sale_checkout_handoff": ("execute_sale", "command_market_sale_orders"),
    "escrow_hold_and_release": ("open_escrow", "compile_escrow_release_policy", "release_escrow"),
    "settlement_instruction": ("prepare_settlement", "command_market_settlements"),
    "reputation_scoring": ("record_reputation_signal", "score_reputation"),
    "dispute_resolution": ("open_dispute", "resolve_dispute"),
    "policy_rule_engine": ("register_rule",),
    "runtime_parameter_engine": ("set_parameter",),
    "configuration_schema": ("configure_runtime",),
    "owned_schema_migrations_models": ("build_schema_contract",),
    "appgen_x_outbox_inbox_eventing": ("receive_event",),
    "idempotent_handlers": ("receive_event",),
    "retry_dead_letter_evidence": ("receive_event",),
    "permissions": ("permissions_contract",),
    "seed_data": ("build_release_evidence",),
    "workbench": ("build_workbench_view", "query_market_workbench"),
    "agentic_document_instruction_intake": ("parse_market_instruction",),
    "governed_datastore_crud": ("build_service_contract",),
}

ADVANCED_CAPABILITY_OPERATION_COVERAGE = {
    "multi_party_exchange_graph_matching": ("optimize_exchange_match", "prepare_exchange_proposal"),
    "barter_equivalence_valuation": ("match_barter_offer", "simulate_counterfactual_terms"),
    "combinatorial_trade_optimization": ("optimize_exchange_match", "publish_market_clearing_projection"),
    "dynamic_liquidity_and_trust_scoring": ("score_reputation", "publish_market_clearing_projection"),
    "availability_aware_booking_optimization": ("publish_availability_window", "reserve_booking"),
    "rental_condition_and_collateral_modeling": ("start_rental", "simulate_counterfactual_terms"),
    "loan_term_risk_simulation": ("issue_loan", "simulate_counterfactual_terms"),
    "escrow_release_policy_compilation": ("compile_escrow_release_policy", "release_escrow"),
    "real_time_market_clearing_projection": ("publish_market_clearing_projection",),
    "counterfactual_price_and_slot_simulation": ("simulate_counterfactual_terms",),
    "semantic_listing_instruction_understanding": ("parse_market_instruction",),
    "autonomous_dispute_triage_with_audit_trail": ("open_dispute", "resolve_dispute"),
    "fraud_and_collusion_anomaly_detection": ("detect_collusion_anomaly",),
    "privacy_preserving_reputation_proofs": ("generate_reputation_proof",),
    "carbon_aware_fulfillment_and_meetup_selection": ("select_carbon_fulfillment",),
    "cross_pbc_catalog_inventory_payment_tax_integration": ("receive_event", "verify_owned_table_boundary"),
}


def _missing_coverage(features: tuple[str, ...], coverage: dict[str, tuple[str, ...]], operations: set[str]) -> tuple[dict, ...]:
    gaps = []
    for feature in features:
        required_operations = coverage.get(feature, ())
        missing_operations = tuple(operation for operation in required_operations if operation not in operations)
        if not required_operations or missing_operations:
            gaps.append(
                {
                    "feature": feature,
                    "required_operations": required_operations,
                    "missing_operations": missing_operations,
                }
            )
    return tuple(gaps)


def table_stakes_capability_manifest():
    runtime = multi_sided_market_runtime_capabilities()
    return {
        'ok': runtime['ok'],
        'pbc': PBC_KEY,
        'standard_features': PBC_MANIFEST['standard_features'],
        'advanced_capabilities': PBC_MANIFEST['advanced_capabilities'],
        'runtime_operations': tuple(runtime['operations']),
        'owned_tables': tuple(runtime['owned_tables']),
        'event_contract': 'AppGen-X',
        'stream_picker_visible': False,
        'stream_engine_picker_visible': False,
        'allowed_database_backends': MULTI_SIDED_MARKET_ALLOWED_DATABASE_BACKENDS,
        'side_effects': (),
    }


def validate_table_stakes_capability_coverage():
    manifest = table_stakes_capability_manifest()
    runtime_operations = set(manifest['runtime_operations'])
    invalid_backends = tuple(backend for backend in (PBC_MANIFEST['datastore_backend'],) if backend not in manifest['allowed_database_backends'])
    invalid_tables = tuple(table for table in manifest['owned_tables'] if not table.startswith(f"{PBC_KEY}_"))
    missing_standard = _missing_coverage(manifest['standard_features'], STANDARD_FEATURE_OPERATION_COVERAGE, runtime_operations)
    missing_advanced = _missing_coverage(manifest['advanced_capabilities'], ADVANCED_CAPABILITY_OPERATION_COVERAGE, runtime_operations)
    covered_standard = tuple(feature for feature in manifest['standard_features'] if feature not in {gap['feature'] for gap in missing_standard})
    covered_advanced = tuple(feature for feature in manifest['advanced_capabilities'] if feature not in {gap['feature'] for gap in missing_advanced})
    missing_operations = tuple(
        sorted(
            {
                operation
                for gap in missing_standard + missing_advanced
                for operation in gap['missing_operations']
            }
        )
    )
    return {
        'ok': manifest['ok']
        and not invalid_backends
        and not invalid_tables
        and not missing_standard
        and not missing_advanced
        and bool(covered_standard)
        and bool(covered_advanced),
        'manifest': manifest,
        'covered_standard': covered_standard,
        'covered_advanced': covered_advanced,
        'missing_standard': missing_standard,
        'missing_advanced': missing_advanced,
        'missing_operations': missing_operations,
        'uncovered_features': (),
        'invalid_tables': invalid_tables,
        'invalid_backends': invalid_backends,
        'event_contract': 'AppGen-X',
        'stream_picker_visible': False,
        'stream_engine_picker_visible': False,
        'side_effects': (),
    }


def smoke_test():
    coverage = validate_table_stakes_capability_coverage()
    runtime = multi_sided_market_runtime_capabilities()
    return {'ok': coverage['ok'] and runtime['ok'], 'coverage': coverage, 'runtime': runtime, 'side_effects': ()}
