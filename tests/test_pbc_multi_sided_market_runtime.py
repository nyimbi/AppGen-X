from pyAppGen.pbcs.multi_sided_market import MULTI_SIDED_MARKET_ALLOWED_DATABASE_BACKENDS
from pyAppGen.pbcs.multi_sided_market import MULTI_SIDED_MARKET_CONSUMED_EVENT_TYPES
from pyAppGen.pbcs.multi_sided_market import MULTI_SIDED_MARKET_EMITTED_EVENT_TYPES
from pyAppGen.pbcs.multi_sided_market import MULTI_SIDED_MARKET_OWNED_TABLES
from pyAppGen.pbcs.multi_sided_market import MULTI_SIDED_MARKET_REQUIRED_EVENT_TOPIC
from pyAppGen.pbcs.multi_sided_market import MULTI_SIDED_MARKET_RUNTIME_CAPABILITY_KEYS
from pyAppGen.pbcs.multi_sided_market import implementation_contract
from pyAppGen.pbcs.multi_sided_market import multi_sided_market_build_api_contract
from pyAppGen.pbcs.multi_sided_market import multi_sided_market_build_release_evidence
from pyAppGen.pbcs.multi_sided_market import multi_sided_market_build_schema_contract
from pyAppGen.pbcs.multi_sided_market import multi_sided_market_build_service_contract
from pyAppGen.pbcs.multi_sided_market import multi_sided_market_configure_runtime
from pyAppGen.pbcs.multi_sided_market import multi_sided_market_create_service_offer
from pyAppGen.pbcs.multi_sided_market import multi_sided_market_empty_state
from pyAppGen.pbcs.multi_sided_market import multi_sided_market_execute_sale
from pyAppGen.pbcs.multi_sided_market import multi_sided_market_issue_loan
from pyAppGen.pbcs.multi_sided_market import multi_sided_market_match_barter_offer
from pyAppGen.pbcs.multi_sided_market import multi_sided_market_open_dispute
from pyAppGen.pbcs.multi_sided_market import multi_sided_market_optimize_exchange_match
from pyAppGen.pbcs.multi_sided_market import multi_sided_market_place_trade_order
from pyAppGen.pbcs.multi_sided_market import multi_sided_market_prepare_settlement
from pyAppGen.pbcs.multi_sided_market import multi_sided_market_publish_listing
from pyAppGen.pbcs.multi_sided_market import multi_sided_market_receive_event
from pyAppGen.pbcs.multi_sided_market import multi_sided_market_register_rule
from pyAppGen.pbcs.multi_sided_market import multi_sided_market_reserve_booking
from pyAppGen.pbcs.multi_sided_market import multi_sided_market_runtime_capabilities
from pyAppGen.pbcs.multi_sided_market import multi_sided_market_runtime_smoke
from pyAppGen.pbcs.multi_sided_market import multi_sided_market_score_reputation
from pyAppGen.pbcs.multi_sided_market import multi_sided_market_set_parameter
from pyAppGen.pbcs.multi_sided_market import multi_sided_market_start_rental
from pyAppGen.pbcs.multi_sided_market import multi_sided_market_verify_owned_table_boundary
from pyAppGen.pbcs.multi_sided_market import multi_sided_market_verify_participant


def test_multi_sided_market_runtime_declares_complete_package_surface() -> None:
    runtime = multi_sided_market_runtime_capabilities()
    smoke = multi_sided_market_runtime_smoke()
    contract = implementation_contract()

    assert runtime["ok"] is True
    assert runtime["implementation_directory"] == "src/pyAppGen/pbcs/multi_sided_market"
    assert runtime["owned_tables"] == MULTI_SIDED_MARKET_OWNED_TABLES
    assert set(runtime["capabilities"]) == set(MULTI_SIDED_MARKET_RUNTIME_CAPABILITY_KEYS)
    assert smoke["ok"] is True
    assert not smoke["blocking_gaps"]
    assert contract["pbc"] == "multi_sided_market"
    assert contract["advanced_runtime"]["ok"] is True
    assert contract["allowed_database_backends"] == MULTI_SIDED_MARKET_ALLOWED_DATABASE_BACKENDS
    assert contract["required_event_topic"] == MULTI_SIDED_MARKET_REQUIRED_EVENT_TOPIC
    assert contract["emits"] == MULTI_SIDED_MARKET_EMITTED_EVENT_TYPES
    assert contract["consumes"] == MULTI_SIDED_MARKET_CONSUMED_EVENT_TYPES
    assert contract["api_contract"]["event_contract"] == "AppGen-X"
    assert contract["api_contract"]["stream_engine_picker_visible"] is False
    assert contract["api_contract"]["shared_table_access"] is False
    assert contract["schema_contract"]["ok"] is True
    assert contract["service_contract"]["ok"] is True
    assert contract["release_evidence_contract"]["ok"] is True
    assert contract["permissions_contract"]["action_permissions"]["receive_event"] == "multi_sided_market.event.consume"
    assert contract["boundary_contract"]["ok"] is True


def test_multi_sided_market_executes_exchange_flows_without_shared_tables() -> None:
    state = multi_sided_market_empty_state()
    state = multi_sided_market_configure_runtime(
        state,
        {
            "database_backend": "postgresql",
            "event_topic": MULTI_SIDED_MARKET_REQUIRED_EVENT_TOPIC,
            "retry_limit": 5,
        },
    )["state"]
    state = multi_sided_market_set_parameter(state, "commission_rate", 0.08)["state"]
    state = multi_sided_market_register_rule(
        state,
        {"rule_id": "market_trust_gate", "type": "exchange_policy", "status": "active", "minimum_trust_score": 0.55},
    )["state"]
    state = multi_sided_market_verify_participant(
        state,
        {"participant_id": "seller_1", "roles": ("seller", "lender", "service_provider"), "trust_score": 0.93},
    )["state"]
    state = multi_sided_market_publish_listing(
        state,
        {
            "listing_id": "listing_1",
            "participant_id": "seller_1",
            "kind": "good",
            "price": 125,
            "exchange_modes": ("sale", "trade", "barter", "booking", "rental", "loan"),
        },
    )["state"]
    state = multi_sided_market_create_service_offer(
        state,
        {"offer_id": "service_1", "listing_id": "listing_1", "service_type": "installation"},
    )["state"]
    trade = multi_sided_market_place_trade_order(
        state,
        {"order_id": "trade_1", "listing_id": "listing_1", "offered_listing_id": "listing_2"},
    )
    state = trade["state"]
    barter = multi_sided_market_match_barter_offer(
        state,
        {"offer_id": "barter_1", "listing_id": "listing_1", "requested_value": 125, "offered_value": 120},
    )
    state = barter["state"]
    sale = multi_sided_market_execute_sale(
        state,
        {"sale_id": "sale_1", "listing_id": "listing_1", "buyer_id": "buyer_1", "amount": 125},
    )
    state = sale["state"]
    booking = multi_sided_market_reserve_booking(
        state,
        {"booking_id": "booking_1", "listing_id": "listing_1", "starts_at": "2026-06-01T10:00:00Z"},
    )
    state = booking["state"]
    rental = multi_sided_market_start_rental(
        state,
        {"rental_id": "rental_1", "listing_id": "listing_1", "collateral_amount": 50},
    )
    state = rental["state"]
    loan = multi_sided_market_issue_loan(
        state,
        {"loan_id": "loan_1", "listing_id": "listing_1", "borrower_id": "borrower_1", "collateral_rate": 0.2},
    )
    state = loan["state"]
    settlement = multi_sided_market_prepare_settlement(
        state,
        {"settlement_id": "settlement_1", "exchange_id": "sale_1", "amount": 125},
    )
    state = settlement["state"]
    dispute = multi_sided_market_open_dispute(
        state,
        {"dispute_id": "dispute_1", "exchange_id": "rental_1", "reason": "condition_claim"},
    )
    state = dispute["state"]
    reputation = multi_sided_market_score_reputation(state, "seller_1")
    match = multi_sided_market_optimize_exchange_match(state, {"exchange_modes": ("barter", "rental")})

    assert trade["trade_order"]["status"] == "placed"
    assert barter["barter_offer"]["status"] == "matched"
    assert sale["sale_order"]["status"] == "completed"
    assert booking["booking"]["status"] == "reserved"
    assert rental["rental"]["status"] == "active"
    assert loan["loan"]["status"] == "issued"
    assert settlement["settlement"]["status"] == "prepared"
    assert dispute["dispute"]["triage"] == "agent_review_ready"
    assert reputation["score"] > 0
    assert match["candidate_count"] == 1
    assert all(event["topic"] == MULTI_SIDED_MARKET_REQUIRED_EVENT_TOPIC for event in state["outbox"])

    event = {
        "event_id": "evt_payment_1",
        "event_type": "PaymentCaptured",
        "idempotency_key": "payment:1",
        "payload": {"tenant": "default"},
    }
    received = multi_sided_market_receive_event(state, event)
    duplicate = multi_sided_market_receive_event(received["state"], event)
    assert received["ok"] is True
    assert duplicate["duplicate"] is True


def test_multi_sided_market_contracts_cover_standard_table_stakes() -> None:
    api = multi_sided_market_build_api_contract()
    schema = multi_sided_market_build_schema_contract()
    service = multi_sided_market_build_service_contract()
    release = multi_sided_market_build_release_evidence()

    assert api["ok"] is True
    assert "POST /market/barter-offers" in {route["route"] for route in api["routes"]}
    assert "POST /market/rentals" in {route["route"] for route in api["routes"]}
    assert "POST /market/loans" in {route["route"] for route in api["routes"]}
    assert schema["ok"] is True
    assert len(schema["owned_tables"]) >= 20
    listing_table = next(table for table in schema["tables"] if table["table"] == "multi_sided_market_marketplace_listing")
    rental_table = next(table for table in schema["tables"] if table["table"] == "multi_sided_market_rental_contract")
    escrow_table = next(table for table in schema["tables"] if table["table"] == "multi_sided_market_escrow_account")
    assert "exchange_modes" in listing_table["fields"]
    assert "collateral_amount" in rental_table["fields"]
    assert "release_policy_hash" in escrow_table["fields"]
    assert len(listing_table["field_contracts"]) >= 10
    assert any(item["type"].startswith("owned") for item in schema["relationships"])
    assert service["ok"] is True
    assert "command_market_barter_offers" in service["command_methods"]
    assert "query_market_workbench" in service["query_methods"]
    assert service["external_dependencies"]["shared_tables"] == ()
    assert release["ok"] is True
    assert not release["blocking_gaps"]
    assert all(check["ok"] is True for check in release["checks"])

    boundary = multi_sided_market_verify_owned_table_boundary(
        MULTI_SIDED_MARKET_OWNED_TABLES + ("PaymentCaptured", "payment_orchestration.api")
    )
    foreign_boundary = multi_sided_market_verify_owned_table_boundary(
        MULTI_SIDED_MARKET_OWNED_TABLES + ("foreign_order_table",)
    )
    assert boundary["ok"] is True
    assert foreign_boundary["ok"] is False
    assert foreign_boundary["invalid_references"] == ("foreign_order_table",)
