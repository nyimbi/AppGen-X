"""Domain schema metadata for the multi_sided_market PBC."""

PBC_KEY = "multi_sided_market"
TABLE_PREFIX = f"{PBC_KEY}_"

BASE_FIELDS = (
    {"name": "id", "type": "integer", "primary_key": True},
    {"name": "tenant", "type": "string", "required": True},
    {"name": "status", "type": "string", "required": True},
    {"name": "version", "type": "integer", "required": True},
    {"name": "created_at", "type": "datetime", "required": True},
    {"name": "updated_at", "type": "datetime", "required": True},
)

DOMAIN_FIELDS = {
    "participant_profile": (
        {"name": "participant_id", "type": "string", "required": True, "unique": True},
        {"name": "roles", "type": "json", "required": True},
        {"name": "verification_level", "type": "string", "required": True},
        {"name": "trust_score", "type": "decimal", "required": True},
        {"name": "default_currency", "type": "string", "required": True},
        {"name": "policy_context", "type": "json", "required": False},
    ),
    "marketplace_listing": (
        {"name": "listing_id", "type": "string", "required": True, "unique": True},
        {"name": "participant_id", "type": "string", "required": True},
        {"name": "title", "type": "string", "required": True},
        {"name": "kind", "type": "string", "required": True},
        {"name": "exchange_modes", "type": "json", "required": True},
        {"name": "price", "type": "decimal", "required": False},
        {"name": "currency", "type": "string", "required": False},
        {"name": "published_at", "type": "datetime", "required": False},
    ),
    "listing_asset": (
        {"name": "asset_id", "type": "string", "required": True, "unique": True},
        {"name": "listing_id", "type": "string", "required": True},
        {"name": "asset_type", "type": "string", "required": True},
        {"name": "quantity", "type": "decimal", "required": True},
        {"name": "condition_grade", "type": "string", "required": False},
        {"name": "location", "type": "json", "required": False},
        {"name": "attributes", "type": "json", "required": False},
    ),
    "service_offer": (
        {"name": "offer_id", "type": "string", "required": True, "unique": True},
        {"name": "listing_id", "type": "string", "required": True},
        {"name": "provider_id", "type": "string", "required": True},
        {"name": "service_type", "type": "string", "required": True},
        {"name": "duration_minutes", "type": "integer", "required": True},
        {"name": "service_area", "type": "json", "required": False},
    ),
    "availability_window": (
        {"name": "window_id", "type": "string", "required": True, "unique": True},
        {"name": "listing_id", "type": "string", "required": True},
        {"name": "starts_at", "type": "datetime", "required": True},
        {"name": "ends_at", "type": "datetime", "required": True},
        {"name": "capacity", "type": "integer", "required": True},
        {"name": "reserved_count", "type": "integer", "required": True},
    ),
    "booking_reservation": (
        {"name": "booking_id", "type": "string", "required": True, "unique": True},
        {"name": "listing_id", "type": "string", "required": True},
        {"name": "participant_id", "type": "string", "required": True},
        {"name": "starts_at", "type": "datetime", "required": True},
        {"name": "ends_at", "type": "datetime", "required": True},
        {"name": "hold_expires_at", "type": "datetime", "required": False},
    ),
    "rental_contract": (
        {"name": "rental_id", "type": "string", "required": True, "unique": True},
        {"name": "listing_id", "type": "string", "required": True},
        {"name": "renter_id", "type": "string", "required": True},
        {"name": "condition_out", "type": "json", "required": True},
        {"name": "condition_in", "type": "json", "required": False},
        {"name": "collateral_amount", "type": "decimal", "required": True},
        {"name": "return_due_at", "type": "datetime", "required": False},
    ),
    "loan_agreement": (
        {"name": "loan_id", "type": "string", "required": True, "unique": True},
        {"name": "listing_id", "type": "string", "required": True},
        {"name": "borrower_id", "type": "string", "required": True},
        {"name": "return_due_at", "type": "datetime", "required": True},
        {"name": "collateral_rate", "type": "decimal", "required": True},
        {"name": "risk_score", "type": "decimal", "required": False},
    ),
    "barter_offer": (
        {"name": "offer_id", "type": "string", "required": True, "unique": True},
        {"name": "listing_id", "type": "string", "required": True},
        {"name": "offered_listing_id", "type": "string", "required": True},
        {"name": "requested_value", "type": "decimal", "required": True},
        {"name": "offered_value", "type": "decimal", "required": True},
        {"name": "valuation_delta", "type": "decimal", "required": True},
    ),
    "trade_order": (
        {"name": "order_id", "type": "string", "required": True, "unique": True},
        {"name": "listing_id", "type": "string", "required": True},
        {"name": "offered_listing_id", "type": "string", "required": True},
        {"name": "quantity", "type": "decimal", "required": True},
        {"name": "clearing_score", "type": "decimal", "required": False},
    ),
    "sale_order": (
        {"name": "sale_id", "type": "string", "required": True, "unique": True},
        {"name": "listing_id", "type": "string", "required": True},
        {"name": "buyer_id", "type": "string", "required": True},
        {"name": "amount", "type": "decimal", "required": True},
        {"name": "currency", "type": "string", "required": True},
        {"name": "payment_reference", "type": "string", "required": False},
    ),
    "exchange_proposal": (
        {"name": "proposal_id", "type": "string", "required": True, "unique": True},
        {"name": "source_listing_id", "type": "string", "required": True},
        {"name": "target_listing_id", "type": "string", "required": True},
        {"name": "exchange_mode", "type": "string", "required": True},
        {"name": "score", "type": "decimal", "required": True},
        {"name": "explanation", "type": "json", "required": False},
    ),
    "escrow_account": (
        {"name": "escrow_id", "type": "string", "required": True, "unique": True},
        {"name": "exchange_id", "type": "string", "required": True},
        {"name": "amount", "type": "decimal", "required": True},
        {"name": "currency", "type": "string", "required": True},
        {"name": "hold_until", "type": "datetime", "required": False},
        {"name": "release_policy_hash", "type": "string", "required": True},
    ),
    "settlement_instruction": (
        {"name": "settlement_id", "type": "string", "required": True, "unique": True},
        {"name": "exchange_id", "type": "string", "required": True},
        {"name": "amount", "type": "decimal", "required": True},
        {"name": "currency", "type": "string", "required": True},
        {"name": "destination_account", "type": "string", "required": True},
        {"name": "settlement_policy", "type": "json", "required": False},
    ),
    "dispute_case": (
        {"name": "dispute_id", "type": "string", "required": True, "unique": True},
        {"name": "exchange_id", "type": "string", "required": True},
        {"name": "reason", "type": "string", "required": True},
        {"name": "triage", "type": "string", "required": True},
        {"name": "evidence", "type": "json", "required": False},
        {"name": "resolution", "type": "json", "required": False},
    ),
    "reputation_signal": (
        {"name": "signal_id", "type": "string", "required": True, "unique": True},
        {"name": "participant_id", "type": "string", "required": True},
        {"name": "source_exchange_id", "type": "string", "required": True},
        {"name": "score_delta", "type": "decimal", "required": True},
        {"name": "reason", "type": "string", "required": True},
        {"name": "proof_hash", "type": "string", "required": False},
    ),
    "market_rule": (
        {"name": "rule_id", "type": "string", "required": True, "unique": True},
        {"name": "rule_type", "type": "string", "required": True},
        {"name": "policy_body", "type": "json", "required": True},
        {"name": "compiled_hash", "type": "string", "required": True},
        {"name": "effective_from", "type": "datetime", "required": False},
    ),
    "market_parameter": (
        {"name": "parameter_id", "type": "string", "required": True, "unique": True},
        {"name": "name", "type": "string", "required": True},
        {"name": "value", "type": "json", "required": True},
        {"name": "bounds", "type": "json", "required": False},
        {"name": "changed_by", "type": "string", "required": False},
    ),
    "schema_extension": (
        {"name": "extension_id", "type": "string", "required": True, "unique": True},
        {"name": "table_name", "type": "string", "required": True},
        {"name": "fields", "type": "json", "required": True},
        {"name": "schema_version", "type": "integer", "required": True},
        {"name": "compatibility", "type": "string", "required": True},
    ),
    "governed_model": (
        {"name": "model_id", "type": "string", "required": True, "unique": True},
        {"name": "name", "type": "string", "required": True},
        {"name": "purpose", "type": "string", "required": True},
        {"name": "model_version", "type": "string", "required": True},
        {"name": "metrics", "type": "json", "required": False},
        {"name": "governance_status", "type": "string", "required": True},
    ),
}

RELATIONSHIPS = (
    {"from": "marketplace_listing.participant_id", "to": "participant_profile.participant_id", "type": "owned_reference"},
    {"from": "listing_asset.listing_id", "to": "marketplace_listing.listing_id", "type": "owned_reference"},
    {"from": "service_offer.listing_id", "to": "marketplace_listing.listing_id", "type": "owned_reference"},
    {"from": "availability_window.listing_id", "to": "marketplace_listing.listing_id", "type": "owned_reference"},
    {"from": "booking_reservation.listing_id", "to": "marketplace_listing.listing_id", "type": "owned_reference"},
    {"from": "rental_contract.listing_id", "to": "marketplace_listing.listing_id", "type": "owned_reference"},
    {"from": "loan_agreement.listing_id", "to": "marketplace_listing.listing_id", "type": "owned_reference"},
    {"from": "barter_offer.listing_id", "to": "marketplace_listing.listing_id", "type": "owned_reference"},
    {"from": "trade_order.listing_id", "to": "marketplace_listing.listing_id", "type": "owned_reference"},
    {"from": "sale_order.listing_id", "to": "marketplace_listing.listing_id", "type": "owned_reference"},
    {"from": "escrow_account.exchange_id", "to": "exchange_proposal.proposal_id", "type": "owned_exchange_reference"},
    {"from": "settlement_instruction.exchange_id", "to": "exchange_proposal.proposal_id", "type": "owned_exchange_reference"},
    {"from": "dispute_case.exchange_id", "to": "exchange_proposal.proposal_id", "type": "owned_exchange_reference"},
    {"from": "reputation_signal.participant_id", "to": "participant_profile.participant_id", "type": "owned_reference"},
)


def owned_table(logical_table: str) -> str:
    return logical_table if logical_table.startswith(TABLE_PREFIX) else f"{TABLE_PREFIX}{logical_table}"


def logical_table(table: str) -> str:
    return table.removeprefix(TABLE_PREFIX)


def fields_for(logical_name: str) -> tuple[dict, ...]:
    return BASE_FIELDS + DOMAIN_FIELDS[logical_table(logical_name)]


def relationships_for(logical_name: str) -> tuple[dict, ...]:
    logical = logical_table(logical_name)
    return tuple(item for item in RELATIONSHIPS if item["from"].startswith(f"{logical}."))


def class_name_for(table: str) -> str:
    return "".join(part.capitalize() for part in owned_table(table).split("_"))

