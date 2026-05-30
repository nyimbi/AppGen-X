"""Executable improve1 controls for the Multi-Sided Market PBC."""

from __future__ import annotations

import hashlib
from typing import Any

from .improve1_capabilities import IMPROVE1_CAPABILITIES, Improve1Capability

PBC_KEY = "multi_sided_market"
EVENT_CONTRACT = "AppGen-X"
MARKET_CONTROL_ALLOWED_DATABASE_BACKENDS = ("postgresql", "mysql", "mariadb")
MARKET_CONTROL_REQUIRED_EVENT_TOPIC = "pbc.multi_sided_market.events"
_BASE_OWNED_TABLES = (
    "multi_sided_market_participant_profile",
    "multi_sided_market_marketplace_listing",
    "multi_sided_market_listing_asset",
    "multi_sided_market_service_offer",
    "multi_sided_market_availability_window",
    "multi_sided_market_booking_reservation",
    "multi_sided_market_rental_contract",
    "multi_sided_market_loan_agreement",
    "multi_sided_market_barter_offer",
    "multi_sided_market_trade_order",
    "multi_sided_market_sale_order",
    "multi_sided_market_exchange_proposal",
    "multi_sided_market_escrow_account",
    "multi_sided_market_settlement_instruction",
    "multi_sided_market_dispute_case",
    "multi_sided_market_reputation_signal",
    "multi_sided_market_market_rule",
    "multi_sided_market_market_parameter",
    "multi_sided_market_schema_extension",
    "multi_sided_market_governed_model",
    "multi_sided_market_appgen_outbox_event",
    "multi_sided_market_appgen_inbox_event",
    "multi_sided_market_dead_letter_event",
)
MARKET_CONTROL_OWNED_TABLES = tuple(dict.fromkeys(_BASE_OWNED_TABLES + tuple(f"multi_sided_market_{capability.slug}_control" for capability in IMPROVE1_CAPABILITIES)))
MARKET_CONTROL_DECLARED_DEPENDENCIES = tuple(dict.fromkeys((
    "PolicyChanged",
    "AuditEventSealed",
    "OperationalKpiChanged",
    "IdentityVerificationChanged",
    "CatalogItemProjectionChanged",
    "InventoryAvailabilityChanged",
    "PaymentCaptureChanged",
    "TaxCalculationChanged",
    "FraudRiskProjectionChanged",
    "SustainabilityProjectionChanged",
    "FulfillmentProjectionChanged",
)))
MARKET_CONTROL_CAPABILITIES: tuple[Improve1Capability, ...] = IMPROVE1_CAPABILITIES
CAPABILITY_BY_NUMBER = {capability.feature_number: capability for capability in MARKET_CONTROL_CAPABILITIES}
CAPABILITY_BY_SLUG = {capability.slug: capability for capability in MARKET_CONTROL_CAPABILITIES}
_BASE_FIELDS = ("tenant_id", "market_id", "participant_id", "exchange_id", "listing_id", "policy_version", "actor_id", "audit_trail", "evidence_references")
_PRIMARY_PROOF_FIELDS: dict[int, str] = {
    1: 'participant_role_and_capability_graph_verified',
    2: 'participant_verification_and_trust_onboarding_verified',
    3: 'listing_taxonomy_and_exchange_mode_eligibility_verified',
    4: 'listing_asset_condition_and_provenance_verified',
    5: 'service_offer_scope_and_fulfillment_definition_verified',
    6: 'availability_window_capacity_semantics_verified',
    7: 'hold_expiry_and_reservation_consistency_verified',
    8: 'booking_optimization_and_rescheduling_verified',
    9: 'rental_contract_lifecycle_verified',
    10: 'loan_agreement_and_return_obligation_modeling_verified',
    11: 'barter_equivalence_valuation_verified',
    12: 'multi_party_exchange_graph_matching_verified',
    13: 'combinatorial_trade_optimization_verified',
    14: 'exchange_proposal_negotiation_ledger_verified',
    15: 'direct_sale_checkout_handoff_verified',
    16: 'escrow_account_state_machine_verified',
    17: 'escrow_release_policy_compiler_verified',
    18: 'settlement_instruction_governance_verified',
    19: 'commission_and_fee_rule_management_verified',
    20: 'reputation_signal_provenance_verified',
    21: 'privacy_preserving_reputation_proofs_verified',
    22: 'dispute_case_typology_and_evidence_verified',
    23: 'autonomous_dispute_triage_with_human_review_verified',
    24: 'remedy_and_resolution_catalog_verified',
    25: 'collusion_and_market_manipulation_detection_verified',
    26: 'liquidity_and_market_health_metrics_verified',
    27: 'market_clearing_projection_verified',
    28: 'dynamic_pricing_and_counterfactual_terms_verified',
    29: 'availability_aware_service_marketplace_verified',
    30: 'rental_condition_and_damage_workflow_verified',
    31: 'loan_recall_and_extension_handling_verified',
    32: 'fulfillment_and_meetup_optimization_verified',
    33: 'carbon_aware_exchange_selection_verified',
    34: 'participant_safety_and_conduct_controls_verified',
    35: 'regulated_goods_and_services_controls_verified',
    36: 'insurance_and_collateral_requirement_modeling_verified',
    37: 'tax_and_fee_evidence_integration_verified',
    38: 'fraud_risk_aware_market_operations_verified',
    39: 'inventory_and_asset_availability_boundary_verified',
    40: 'exchange_policy_and_parameter_studio_verified',
    41: 'semantic_listing_and_document_intake_verified',
    42: 'market_agent_negotiation_assistance_verified',
    43: 'accessibility_and_inclusion_for_market_participation_verified',
    44: 'market_abuse_and_policy_enforcement_workflow_verified',
    45: 'exchange_time_travel_and_audit_reconstruction_verified',
    46: 'market_release_evidence_packs_verified',
    47: 'cross_pbc_boundary_proofs_verified',
    48: 'dead_letter_and_replay_operations_verified',
    49: 'marketplace_operations_metrics_verified',
    50: 'complete_multi_sided_market_workbench_coverage_verified',
}
_DOMAIN_FIELDS: dict[int, tuple[str, ...]] = {
    1: ('participant_id', 'role_graph', 'verified_capabilities', 'jurisdiction', 'service_area', 'trust_tier', 'policy_restrictions', 'payout_eligibility', 'borrowing_eligibility', 'lending_authority', 'role_effective_dates'),
    2: ('verification_id', 'identity_evidence', 'business_documents', 'payment_readiness_projection', 'fraud_risk_projection', 'address_region_check', 'role_document_requirements', 'trust_tier_assignment'),
    3: ('listing_id', 'exchange_mode_matrix', 'listing_taxonomy', 'prohibited_category_check', 'required_disclosures', 'consideration_types', 'regulated_status', 'settlement_paths', 'eligibility_blockers'),
    4: ('asset_id', 'condition_record', 'photo_evidence', 'inspection_status', 'ownership_proof', 'authenticity_evidence', 'serial_number', 'defect_disclosures', 'custody_holder', 'location'),
    5: ('service_offer_id', 'deliverable_template', 'provider_credentials', 'duration', 'service_radius', 'service_mode', 'prerequisites', 'cancellation_window', 'acceptance_criteria', 'capacity'),
    6: ('availability_window_id', 'capacity_units', 'reserved_count', 'pending_holds', 'setup_buffer', 'turnaround_buffer', 'location_constraint', 'provider_dependency', 'asset_dependency', 'overbooking_policy'),
    7: ('reservation_hold_id', 'hold_state', 'expiry_timer', 'release_reason', 'waitlist_position', 'replacement_offer', 'conflict_resolution', 'availability_event'),
    8: ('booking_optimization_id', 'preferred_slots', 'alternate_providers', 'alternate_assets', 'split_booking_option', 'waitlist_promotion', 'reschedule_option', 'counterfactual_simulation', 'displacement_approval'),
    9: ('rental_contract_id', 'handoff_checklist', 'return_checklist', 'deposit', 'collateral', 'allowed_use', 'late_fee_rule', 'extension_process', 'condition_delta', 'damage_adjudication'),
    10: ('loan_agreement_id', 'lender_duties', 'borrower_duties', 'due_date', 'collateral_requirement', 'usage_restrictions', 'renewal_terms', 'recall_rights', 'return_evidence', 'breach_outcomes'),
    11: ('barter_valuation_id', 'market_price_projection', 'condition_factor', 'service_effort', 'scarcity_factor', 'timing_factor', 'location_factor', 'trust_factor', 'carbon_cost', 'counteroffer'),
    12: ('exchange_graph_id', 'participant_nodes', 'want_edges', 'offer_edges', 'asset_nodes', 'service_nodes', 'availability_constraints', 'trust_constraints', 'candidate_proposals', 'settlement_complexity'),
    13: ('combinatorial_match_id', 'bundle_id', 'substitutions', 'minimum_acceptance_set', 'partial_fill_rule', 'linked_conditions', 'objective_function', 'constraints', 'winners', 'counterfactual_outcomes'),
    14: ('proposal_id', 'term_sheet', 'counteroffers', 'expiry', 'conditions', 'included_assets', 'included_services', 'availability_slots', 'settlement_path', 'acknowledgements'),
    15: ('sale_order_id', 'price_check', 'buyer_eligibility', 'seller_eligibility', 'inventory_projection', 'fraud_score', 'tax_projection', 'payment_capture_reference', 'fulfillment_terms'),
    16: ('escrow_account_id', 'escrow_state', 'payment_evidence', 'fulfillment_confirmation', 'dispute_status', 'policy_hash', 'release_window', 'refund_path'),
    17: ('release_policy_id', 'payment_check', 'condition_check', 'delivery_check', 'service_acceptance_check', 'tax_check', 'fraud_check', 'dispute_check', 'time_window_check', 'evaluation_trace'),
    18: ('settlement_instruction_id', 'beneficiaries', 'fee_schedule', 'currency', 'tax_reference', 'payment_reference', 'escrow_source', 'split_percentages', 'holdbacks', 'approval_evidence'),
    19: ('fee_schedule_id', 'rule_type', 'applicability', 'cap', 'minimum', 'currency', 'tax_handling', 'promotional_override', 'effective_dates', 'impact_simulation'),
    20: ('reputation_signal_id', 'exchange_id', 'role', 'signal_source', 'evidence', 'weight', 'decay', 'dispute_adjustment', 'privacy_level', 'confidence'),
    21: ('reputation_proof_id', 'trust_band', 'verified_milestones', 'dispute_rate', 'recency', 'cryptographic_evidence', 'redaction_policy'),
    22: ('dispute_case_id', 'dispute_type', 'exchange_context', 'policy_reference', 'evidence_checklist', 'involved_roles', 'timeline', 'requested_remedy', 'severity', 'resolution_path'),
    23: ('triage_id', 'evidence_summary', 'dispute_classification', 'missing_proof_flags', 'policy_outcome_estimate', 'proposed_next_actions', 'human_confirmation'),
    24: ('remedy_id', 'remedy_type', 'eligibility_rules', 'authority', 'financial_impact', 'reputation_impact', 'required_evidence', 'participant_notification', 'appeal_window'),
    25: ('collusion_case_id', 'exchange_graph_cycles', 'repeated_counterparties', 'reputation_pattern', 'price_anomaly', 'dispute_cluster', 'timing_signal', 'risk_case_projection'),
    26: ('market_health_id', 'fill_rate', 'match_latency', 'inventory_depth', 'service_availability', 'booking_utilization', 'price_spread', 'barter_imbalance', 'dispute_rate', 'trust_weighted_supply'),
    27: ('clearing_projection_id', 'unmatched_demand', 'constrained_supply', 'expected_matches', 'escrow_capacity', 'settlement_blockers', 'risk_exclusions', 'recommendations', 'confidence', 'assumptions'),
    28: ('term_simulation_id', 'price', 'slot', 'deposit', 'collateral', 'trust_threshold', 'fulfillment_method', 'commission', 'expected_conversion', 'risk_effect', 'fee_effect'),
    29: ('service_market_match_id', 'provider_skills', 'travel_radius', 'setup_time', 'recurring_schedule', 'waitlist', 'reschedule_policy', 'slot_feasibility'),
    30: ('rental_damage_id', 'handoff_media', 'return_media', 'inspection_checklist', 'damage_category', 'repair_estimate', 'deposit_impact', 'dispute_linkage', 'condition_delta'),
    31: ('loan_change_id', 'recall_right', 'extension_request', 'renewal_approval', 'replacement_obligation', 'due_date_change', 'late_return_penalty', 'risk_exposure'),
    32: ('fulfillment_option_id', 'location', 'time_window', 'cost', 'carbon_estimate', 'safety_rating', 'custody_transfer', 'confirmation_evidence', 'recommendation_basis'),
    33: ('carbon_exchange_id', 'delivery_emissions', 'meetup_emissions', 'provider_travel_emissions', 'rental_return_emissions', 'alternative_match', 'time_tradeoff', 'cost_tradeoff'),
    34: ('safety_control_id', 'safety_policy', 'conduct_report', 'blocked_counterparty', 'safe_meetup_recommendation', 'age_eligibility_rule', 'incident_escalation', 'role_restriction'),
    35: ('regulated_category_id', 'required_credentials', 'region_rules', 'prohibited_items', 'disclosure_requirements', 'compliance_evidence', 'publication_block'),
    36: ('collateral_model_id', 'collateral_rule', 'insurance_evidence', 'replacement_value', 'deposit_amount', 'guarantee_projection', 'release_condition', 'risk_cost_simulation'),
    37: ('tax_evidence_id', 'tax_reference_projection', 'taxable_classification', 'settlement_tax_evidence', 'participant_tax_responsibility', 'blocked_settlement_explanation'),
    38: ('fraud_risk_decision_id', 'fraud_projection_freshness', 'score_band', 'reason_bands', 'allowed_use', 'policy_decision', 'explanation_reference'),
    39: ('inventory_boundary_id', 'inventory_projection_freshness', 'reservation_reference', 'quantity_available', 'asset_eligibility', 'fallback_behavior', 'confirmation_check'),
    40: ('policy_studio_id', 'listing_eligibility_rule', 'exchange_rule', 'escrow_duration', 'trust_threshold', 'commission_rule', 'max_rental_days', 'collateral_rate', 'simulation', 'rollback'),
    41: ('semantic_intake_id', 'document_source', 'proposed_listing', 'proposed_asset', 'proposed_service_offer', 'proposed_availability', 'proposed_rental', 'proposed_loan', 'citations', 'confidence', 'owned_table_preview'),
    42: ('negotiation_assist_id', 'counteroffer_draft', 'term_tradeoff', 'escrow_structure', 'settlement_structure', 'missing_evidence', 'participant_confirmation'),
    43: ('accessibility_id', 'listing_attributes', 'service_attributes', 'location_attributes', 'communication_preference', 'booking_requirement', 'accommodation_disclosure'),
    44: ('abuse_case_id', 'policy_type', 'evidence', 'participant_history', 'enforcement_action', 'appeal', 'expiry', 'reputation_impact', 'listing_visibility'),
    45: ('audit_reconstruction_id', 'listing_terms_snapshot', 'availability_snapshot', 'reputation_snapshot', 'rule_snapshot', 'escrow_snapshot', 'settlement_snapshot', 'effective_time', 'transaction_time'),
    46: ('release_pack_id', 'schema_hashes', 'migration_manifest', 'service_contracts', 'route_contracts', 'event_schemas', 'handler_idempotency_proofs', 'dead_letter_tests', 'market_simulations', 'ui_coverage', 'agent_manifest'),
    47: ('boundary_proof_id', 'projection_contracts', 'owned_table_check', 'service_mutation_check', 'route_mutation_check', 'handler_mutation_check', 'agent_command_check', 'declared_dependency_reference'),
    48: ('replay_operation_id', 'inbox_status', 'outbox_status', 'retry_count', 'dead_letter_id', 'quarantine_reason', 'idempotency_key', 'payload_lineage', 'replay_eligibility', 'dependency_health'),
    49: ('market_metrics_id', 'participant_activation', 'listing_quality', 'booking_conversion', 'rental_returns', 'loan_lateness', 'barter_match_rate', 'escrow_release_time', 'settlement_success', 'dispute_rate', 'clearing_efficiency'),
    50: ('workbench_coverage_id', 'participant_surface', 'operator_surface', 'moderator_surface', 'matching_surface', 'escrow_settlement_surface', 'dispute_surface', 'trust_safety_surface', 'executive_surface', 'agent_panels', 'release_evidence'),
}
_FEATURE_FIELDS: dict[int, tuple[str, ...]] = {feature_number: _BASE_FIELDS + _DOMAIN_FIELDS[feature_number] + (primary_proof,) for feature_number, primary_proof in _PRIMARY_PROOF_FIELDS.items()}
_FEATURE_DEPENDENCIES: dict[int, tuple[str, ...]] = {
    2: ("IdentityVerificationChanged", "FraudRiskProjectionChanged"),
    15: ("InventoryAvailabilityChanged", "PaymentCaptureChanged", "TaxCalculationChanged", "FraudRiskProjectionChanged"),
    25: ("FraudRiskProjectionChanged",),
    32: ("FulfillmentProjectionChanged",),
    33: ("SustainabilityProjectionChanged",),
    37: ("TaxCalculationChanged",),
    38: ("FraudRiskProjectionChanged",),
    39: ("InventoryAvailabilityChanged", "CatalogItemProjectionChanged"),
    47: ("PolicyChanged", "AuditEventSealed"),
    48: ("AuditEventSealed",),
}
_DOMAIN_MESSAGES: dict[int, str] = {
    1: 'Expand participant profiles with role graph, verified capabilities, jurisdiction, service area, trust tier, policy restrictions, payout eligibility, borrowing eligibility, lending authority, business identity, and role-effective dates. Commands should validate role permissions before listings, bookings, loans, or settlements.',
    2: 'Add verification workflows with identity evidence, business documents, payment readiness projection, fraud risk projection, address/region checks, role-specific document requirements, and trust tier assignment. Emit `MarketParticipantVerified` only when evidence and policy requirements are met.',
    3: 'Expand marketplace listings with exchange mode matrix, listing taxonomy, prohibited category checks, required disclosures, price/consideration types, service/goods distinction, regulated status, and supported settlement paths. The listing console should show eligibility blockers by mode.',
    4: 'Add asset condition records, photos, inspection status, ownership proof, authenticity evidence, serial numbers, defect disclosures, custody holder, location, and depreciation assumptions. Use condition evidence for rentals, loans, disputes, collateral, and reputation.',
    5: 'Expand service offers with deliverable templates, provider credentials, duration, service radius, remote/on-site mode, prerequisites, cancellation windows, acceptance criteria, recurrence, and capacity. Booking and dispute workflows should cite the offer scope.',
    6: 'Upgrade availability windows with capacity units, reserved count, pending holds, setup/turnaround buffers, location, provider/asset dependency, recurrence, blackout reason, and overbooking policy. Reservations should reserve capacity atomically with idempotency.',
    7: 'Add reservation hold states, expiry timers, release reasons, waitlists, replacement offers, and conflict resolution. Publish availability changes when holds expire or reservations become confirmed.',
    8: 'Add booking optimization that recommends time slots, alternate providers/assets, split bookings, waitlist promotion, and reschedule options. Store counterfactual slot simulations and require approval for changes that displace confirmed bookings.',
    9: 'Expand rental contracts with handoff checklist, return checklist, deposit/collateral, allowed use, late fee rules, extension process, condition deltas, maintenance obligations, and damage adjudication. Link rental state to escrow and dispute workflows.',
    10: 'Add loan agreements with lender/borrower duties, due date, collateral requirement, usage restrictions, renewal, recall rights, return evidence, and breach outcomes. Simulate borrower risk before `LoanIssued`.',
    11: 'Add barter valuation models using market price projections, condition, service effort, scarcity, timing, location, trust, and carbon/fulfillment cost. Explain equivalence, imbalance, and suggested counteroffers.',
    12: 'Build exchange graph matching over participants, wants, offers, assets, services, availability, trust, location, and constraints. Generate candidate two-party and multi-party proposals with feasibility, fairness, and settlement complexity.',
    13: 'Add combinatorial matching that supports bundles, substitutions, minimum acceptance sets, partial fills, and linked conditions. Show objective function, constraints, winners, losers, and counterfactual outcomes.',
    14: 'Expand exchange proposals with term sheets, counteroffers, expiry, conditions, included assets/services, availability slots, settlement path, escrow requirement, and participant acknowledgements. Store every revision in a negotiation timeline.',
    15: 'Add sale order readiness checks for price, buyer/seller eligibility, inventory projection, fraud score, tax calculation projection, payment capture reference, and fulfillment terms. Use AppGen-X events and projections only.',
    16: 'Expand escrow accounts with opened, funded, partially releasable, locked, disputed, released, expired, refunded, and forfeited states. Link each state to payment evidence, fulfillment confirmation, dispute status, and policy hash.',
    17: 'Compile escrow release policies into auditable checks for payment, condition, delivery, service acceptance, tax, fraud, dispute, and time windows. Store release evaluation traces before any release event.',
    18: 'Expand settlement instructions with beneficiaries, fee schedule, currency, tax reference, payment reference, escrow source, split percentages, holdbacks, refund paths, and approval evidence. Publish settlement events only after all prerequisites are satisfied.',
    19: 'Add fee schedules with rule type, applicability, caps, minimums, currency, tax handling, promotional overrides, and effective dates. Simulate fee impact on proposed exchanges.',
    20: 'Expand reputation signals with exchange id, role, signal source, evidence, weight, decay, dispute adjustment, privacy level, and confidence. Explain reputation changes without exposing private transaction details.',
    21: 'Add reputation proofs that disclose trust bands, verified milestones, dispute rates, and recency without revealing full transaction history. Support proof exports with cryptographic evidence and role-based redaction.',
    22: 'Expand dispute cases with type, exchange context, policy reference, evidence checklist, involved roles, timeline, requested remedy, severity, and resolution path. The board should guide evidence collection by dispute type.',
    23: 'Add agent-assisted dispute triage that summarizes evidence, classifies dispute type, flags missing proof, estimates policy outcome, and proposes next actions. Require human confirmation for remedies, refunds, releases, or penalties.',
    24: 'Add a remedy catalog with eligibility rules, authority, financial impact, reputation impact, required evidence, and participant notification. Store remedy rationale and appeal windows.',
    25: 'Add collusion anomaly detection using exchange graph cycles, repeated counterparties, abnormal reputation patterns, price anomalies, dispute clusters, and timing. Route suspicious clusters to risk cases through declared fraud projections.',
    26: 'Add liquidity metrics for fill rate, match latency, inventory depth, service availability, booking utilization, price spread, barter imbalance, dispute rate, and trust-weighted supply. Show health by category, geography, and exchange mode.',
    27: 'Expand clearing projections with unmatched demand, constrained supply, expected matches, escrow capacity, settlement blockers, risk exclusions, and recommendations. Emit `MarketClearingProjected` with confidence and assumptions.',
    28: 'Add counterfactual term simulation for price, slot, deposit, collateral, trust threshold, fulfillment method, and commission. Show expected conversion, risk, fee, and dispute effects.',
    29: 'Add service availability constraints, provider skills, travel/service radius, setup time, recurring schedules, waitlists, and reschedule policies. Match services by both skill and slot feasibility.',
    30: 'Add condition capture at handoff and return, media evidence, inspection checklist, damage category, repair estimate, deposit impact, and dispute linkage. Use condition deltas in reputation and escrow release.',
    31: 'Add recall rights, extension requests, renewal approvals, replacement obligations, due-date changes, and late-return penalties. Notify participants and update risk exposure before changing loan terms.',
    32: 'Add fulfillment options with location, time, cost, carbon estimate, safety rating, custody transfer, and confirmation evidence. Recommend options based on trust, distance, value, and policy.',
    33: 'Add carbon estimates for delivery, meetup, provider travel, rental return, and alternative matches. Let participants choose lower-carbon viable proposals with explicit time/cost tradeoffs.',
    34: 'Add safety policies, conduct reports, blocked counterparties, safe-meetup recommendations, age/eligibility rules, incident escalation, and role-based restrictions. Use safety state in matching and booking recommendations.',
    35: 'Add regulated category definitions, required credentials, region rules, prohibited items, disclosure requirements, and compliance evidence. Block listing publication or exchange proposals that violate active policy.',
    36: 'Add collateral rules, insurance evidence, replacement value, deposit amount, guarantee provider projection, and release conditions. Simulate risk and cost before transaction confirmation.',
    37: 'Add tax reference projections, taxable exchange classification, settlement tax evidence, participant tax responsibility, and blocked settlement explanations. Integrate only through declared tax events/APIs.',
    38: 'Consume fraud risk projections with freshness, score, reason bands, and allowed use. Apply risk to policy decisions, but store only market-owned decisions and explanation references.',
    39: 'Add inventory projection freshness, reservation reference, quantity available, asset eligibility, and fallback behavior. Validate availability before sale, rental, loan, or barter confirmation.',
    40: 'Expand market rules and parameters into a studio with simulations, test cases, approvals, effective dates, rollback, impact analysis, and agent explanations before activation.',
    41: 'Give the PBC agent skills to parse documents/instructions into proposed listings, assets, service offers, availability, rentals, loans, barter offers, and policy disclosures. Require citations, confidence, owned-table preview, and confirmation.',
    42: 'Add assistant skills that draft counteroffers, explain term tradeoffs, propose safer escrow/settlement structures, and identify missing evidence. All proposals remain side-effect-free until participant confirmation.',
    43: 'Add accessibility attributes for listings, service offers, locations, communications, and booking requirements. Match participants to accessible options and enforce accommodation disclosures where required.',
    44: 'Add abuse cases with policy type, evidence, participant history, enforcement action, appeal, expiry, and reputation impact. Link abuse enforcement to listing visibility and participant role eligibility.',
    45: 'Add temporal reconstruction across listings, availability, proposals, orders, escrow, settlements, disputes, and reputation using transaction time and effective time.',
    46: 'Generate release evidence packs with schema hashes, migration manifests, service contracts, route contracts, event schemas, handler idempotency proofs, retry/dead-letter tests, market simulations, escrow checks, UI coverage, and agent manifests.',
    47: 'Add projection contracts and tests proving services mutate only `multi_sided_market_` tables plus AppGen-X runtime tables. External facts must flow through APIs, events, or read-only projections.',
    48: 'Add operations views for inbox, outbox, retry, dead-letter, quarantine, idempotency keys, payload lineage, replay eligibility, and dependency health. Unknown consumed events must not mutate market state.',
    49: 'Add governed metrics for participant activation, listing quality, booking conversion, rental returns, loan lateness, barter match rate, escrow release time, settlement success, disputes, reputation movement, and clearing efficiency.',
    50: 'Expand the workbench into role-specific surfaces for participant, marketplace operator, listing moderator, matching analyst, escrow/settlement analyst, dispute resolver, trust/safety reviewer, and executive sponsor. Cover participants, listings, assets, services, availability, bookings, rentals, loans, barter, trades, sales, proposals, escrow, settlements, disputes, reputation, rules, parameters, agent panels, and release evidence.',
}
_HUMAN_CONFIRMATION_FEATURES = (8, 14, 16, 17, 18, 23, 24, 28, 30, 31, 36, 40, 41, 42, 44, 50)
_PROJECTION_ONLY_FEATURES = (2, 15, 25, 32, 33, 37, 38, 39, 47, 48)
_AGENT_PREVIEW_FEATURES = (23, 41, 42, 50)
_NON_MUTATING_FEATURES = (8, 11, 12, 13, 21, 25, 27, 28, 33, 36, 45, 46, 47, 49)
MONEY_OR_TRUST_IMPACT_FEATURES = (2, 9, 10, 11, 15, 16, 17, 18, 19, 20, 21, 23, 24, 25, 34, 35, 36, 37, 38, 44, 50)


def _digest(value: object) -> str:
    return hashlib.sha256(repr(value).encode("utf-8")).hexdigest()


def _camel(slug: str) -> str:
    return "".join(part.capitalize() for part in slug.split("_"))


def _resolve(capability: Improve1Capability | str | int) -> Improve1Capability | None:
    if isinstance(capability, Improve1Capability):
        return capability
    if isinstance(capability, int):
        return CAPABILITY_BY_NUMBER.get(capability)
    return CAPABILITY_BY_SLUG.get(capability)


def _spec_for(capability: Improve1Capability) -> dict[str, Any]:
    proof = _PRIMARY_PROOF_FIELDS[capability.feature_number]
    return {
        "title": capability.title,
        "slug": capability.slug,
        "tables": (f"multi_sided_market_{capability.slug}_control",),
        "fields": _FEATURE_FIELDS[capability.feature_number],
        "primary_proof": proof,
        "ui": f"MultiSidedMarket{_camel(capability.slug)}Panel",
        "route": f"POST /multi-sided-market/improve1/{capability.slug}",
        "dependencies": _FEATURE_DEPENDENCIES.get(capability.feature_number, ()),
    }


CONTROL_SPECS: dict[int, dict[str, Any]] = {capability.feature_number: _spec_for(capability) for capability in MARKET_CONTROL_CAPABILITIES}


def sample_payload_for(capability: Improve1Capability | str | int) -> dict[str, Any]:
    resolved = _resolve(capability)
    if resolved is None:
        return {}
    spec = CONTROL_SPECS[resolved.feature_number]
    payload = {field: f"{resolved.slug}_{field}" for field in spec["fields"]}
    payload[spec["primary_proof"]] = True
    payload.update({
        "database_backend": "postgresql",
        "event_contract": EVENT_CONTRACT,
        "event_topic": MARKET_CONTROL_REQUIRED_EVENT_TOPIC,
        "stream_engine_picker_visible": False,
        "shared_table_access": False,
        "dependency_access_mode": "api_event_projection",
        "human_confirmation": True,
        "agent_preview_only": True,
        "non_mutating_simulation": True,
        "money_or_trust_evidence_complete": True,
        "side_effects": (),
    })
    return payload


def _domain_findings(capability: Improve1Capability, payload: dict[str, Any]) -> tuple[str, ...]:
    findings: list[str] = []
    feature_number = capability.feature_number
    spec = CONTROL_SPECS[feature_number]
    if payload.get(spec["primary_proof"]) is not True:
        findings.append(f"{capability.title} requires {spec['primary_proof'].replace('_', ' ')}")
        findings.append(_DOMAIN_MESSAGES[feature_number])
    if feature_number in MONEY_OR_TRUST_IMPACT_FEATURES and payload.get("money_or_trust_evidence_complete") is not True:
        findings.append("money, escrow, settlement, safety, reputation, or trust-impacting market actions require complete policy, evidence, and approval context")
    if feature_number in _HUMAN_CONFIRMATION_FEATURES and payload.get("human_confirmation") is False:
        findings.append("market decisions that alter confirmed bookings, escrow, settlement, reputation, remedies, or participant obligations require human approval before mutation")
    if feature_number in _AGENT_PREVIEW_FEATURES and payload.get("agent_preview_only") is not True:
        findings.append("market assistant skills must produce source-cited, side-effect-free previews with participant confirmation gates")
    if feature_number in _NON_MUTATING_FEATURES and payload.get("non_mutating_simulation") is not True:
        findings.append("market simulations, proofs, metrics, release evidence, reconstruction, and boundary checks must be side-effect-free artifacts")
    if feature_number in _PROJECTION_ONLY_FEATURES and payload.get("dependency_access_mode") != "api_event_projection":
        findings.append("identity, catalog, inventory, payment, tax, fraud, fulfillment, sustainability, policy, and audit context must use declared APIs, events, or projections")
    if payload.get("event_contract") != EVENT_CONTRACT or payload.get("event_topic") != MARKET_CONTROL_REQUIRED_EVENT_TOPIC:
        findings.append("multi-sided market eventing must use the AppGen-X event contract and package topic")
    if payload.get("stream_engine_picker_visible"):
        findings.append("ordinary PBCs must not expose stream-engine pickers")
    if payload.get("database_backend") not in MARKET_CONTROL_ALLOWED_DATABASE_BACKENDS:
        findings.append("ordinary multi-sided market datastore must be PostgreSQL, MySQL, or MariaDB")
    if payload.get("shared_table_access"):
        findings.append("multi-sided market controls must use owned tables plus declared APIs/events/projections")
    return tuple(dict.fromkeys(findings))


def evaluate_market_control(capability: Improve1Capability | str | int, payload: dict[str, Any] | None = None) -> dict[str, Any]:
    resolved = _resolve(capability)
    if resolved is None:
        return {"ok": False, "reason": "unknown_capability", "side_effects": ()}
    spec = CONTROL_SPECS[resolved.feature_number]
    candidate = sample_payload_for(resolved)
    candidate.update(dict(payload or {}))
    missing_fields = tuple(field for field in spec["fields"] if candidate.get(field) in (None, "", (), []))
    foreign_tables = tuple(table for table in spec["tables"] if table not in MARKET_CONTROL_OWNED_TABLES)
    undeclared_dependencies = tuple(dependency for dependency in spec["dependencies"] if dependency not in MARKET_CONTROL_DECLARED_DEPENDENCIES)
    findings = _domain_findings(resolved, candidate)
    evidence = {
        "evidence_id": _digest((PBC_KEY, resolved.feature_number, tuple(sorted(candidate))))[:20],
        "owned_tables": spec["tables"],
        "required_fields": spec["fields"],
        "primary_proof": spec["primary_proof"],
        "ui_surface": spec["ui"],
        "service_api": spec["route"],
        "test": "tests/test_domain_behavior.py",
        "event_contract": EVENT_CONTRACT,
        "required_event_topic": MARKET_CONTROL_REQUIRED_EVENT_TOPIC,
        "allowed_database_backends": MARKET_CONTROL_ALLOWED_DATABASE_BACKENDS,
        "declared_dependencies": spec["dependencies"],
        "side_effects": (),
    }
    ok = not missing_fields and not foreign_tables and not undeclared_dependencies and not findings
    return {"ok": ok, "pbc": PBC_KEY, "feature_number": resolved.feature_number, "slug": resolved.slug, "title": resolved.title, "capability": resolved.as_traceability_row(), "payload": candidate, "evidence": evidence, "missing_fields": missing_fields, "foreign_tables": foreign_tables, "undeclared_dependencies": undeclared_dependencies, "findings": findings, "side_effects": ()}


def improve1_market_control_contract() -> dict[str, Any]:
    evaluations = tuple(evaluate_market_control(capability) for capability in MARKET_CONTROL_CAPABILITIES)
    blocking = tuple(item for item in evaluations if not item["ok"])
    return {"ok": not blocking, "pbc": PBC_KEY, "format": "appgen.multi-sided-market-improve1-control.v1", "capability_count": len(evaluations), "capabilities": evaluations, "owned_tables": MARKET_CONTROL_OWNED_TABLES, "declared_dependencies": MARKET_CONTROL_DECLARED_DEPENDENCIES, "allowed_database_backends": MARKET_CONTROL_ALLOWED_DATABASE_BACKENDS, "event_contract": EVENT_CONTRACT, "required_event_topic": MARKET_CONTROL_REQUIRED_EVENT_TOPIC, "stream_engine_picker_visible": False, "blocking_gaps": blocking, "side_effects": ()}


MARKET_CONTROL_FUNCTIONS = {capability.slug: (lambda payload=None, slug=capability.slug: evaluate_market_control(slug, payload)) for capability in MARKET_CONTROL_CAPABILITIES}
