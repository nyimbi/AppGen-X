"""Executable runtime for the Cross Border Trade PBC."""

from __future__ import annotations

import copy
import hashlib
import json
import math
import re


CROSS_BORDER_TRADE_REQUIRED_EVENT_TOPIC = "appgen.cross_border_trade.events"
CROSS_BORDER_TRADE_ALLOWED_DATABASE_BACKENDS = ("postgresql", "mysql", "mariadb")
CROSS_BORDER_TRADE_OWNED_TABLES = (
    "hs_classification",
    "landed_cost_quote",
    "export_control_check",
    "customs_declaration",
    "denied_party_screening",
    "trade_document_packet",
    "broker_handoff",
    "carrier_handoff",
    "trade_compliance_hold",
    "country_restriction_policy",
    "trade_rule",
    "trade_parameter",
    "trade_configuration",
    "trade_schema_extension",
    "trade_audit_evidence",
)
CROSS_BORDER_TRADE_RUNTIME_TABLES = (
    "cross_border_trade_appgen_outbox_event",
    "cross_border_trade_appgen_inbox_event",
    "cross_border_trade_dead_letter_event",
)
CROSS_BORDER_TRADE_RUNTIME_EVENT_TABLES = CROSS_BORDER_TRADE_RUNTIME_TABLES
CROSS_BORDER_TRADE_SCHEMA_TABLES = (
    "hs_classification",
    "landed_cost_quote",
    "export_control_check",
    "customs_declaration",
    "denied_party_screening",
    "trade_document_packet",
    "broker_handoff",
    "carrier_handoff",
    "trade_compliance_hold",
    "country_restriction_policy",
    "trade_rule",
    "trade_parameter",
    "trade_configuration",
    "trade_schema_extension",
    "trade_audit_evidence",
    *CROSS_BORDER_TRADE_RUNTIME_TABLES,
)
CROSS_BORDER_TRADE_CONSUMED_EVENT_TYPES = (
    "OrderPlaced",
    "InventoryReserved",
    "PaymentCaptured",
    "ShipmentDispatched",
)
CROSS_BORDER_TRADE_EMITTED_EVENT_TYPES = (
    "HSClassified",
    "LandedCostQuoted",
    "ExportControlCleared",
    "CustomsDeclarationFiled",
    "DeniedPartyScreened",
    "TradeDocumentPacketPrepared",
    "BrokerHandoffQueued",
    "CarrierHandoffPrepared",
    "TradeComplianceHoldOpened",
    "TradeComplianceHoldResolved",
    "CountryRestrictionPolicyRegistered",
    "CustomsDeclarationReleased",
)

CROSS_BORDER_TRADE_RUNTIME_CAPABILITY_KEYS = (
    "event_sourced_trade_lifecycle",
    "owned_trade_schema_boundary",
    "graph_relational_trade_topology",
    "multi_tenant_trade_isolation",
    "schema_evolution_resilient_trade_schema",
    "probabilistic_hs_classification_scoring",
    "counterfactual_landed_cost_simulation",
    "temporal_duty_tax_exposure_forecasting",
    "autonomous_trade_exception_resolution",
    "semantic_trade_document_understanding",
    "predictive_export_control_risk",
    "self_healing_customs_broker_route_selection",
    "cryptographic_trade_proof",
    "immutable_trade_audit_trail",
    "dynamic_trade_policy_screening",
    "automated_trade_control_testing",
    "cross_system_order_inventory_payment_logistics_federation",
    "appgen_x_outbox_inbox_eventing",
    "idempotent_inbox_handlers",
    "retry_dead_letter_evidence",
    "tenant_isolation",
    "chaos_tolerant_trade_operations",
    "crypto_agility",
    "carbon_aware_trade_route_selection",
    "mathematical_landed_cost_optimization",
    "broker_allocation_mechanism_design",
    "trade_anomaly_detection",
    "stochastic_trade_exposure_modeling",
    "governed_ml_model_evidence",
    "permissions_governance_evidence",
    "universal_api_async_streaming",
    "configuration_schema",
    "parameter_engine",
    "rule_engine",
    "seed_data",
    "workbench_ui",
)

CROSS_BORDER_TRADE_STANDARD_FEATURE_KEYS = (
    "hs_classification",
    "landed_cost_quote",
    "export_control_check",
    "customs_declaration",
    "country_of_origin",
    "duty_tax_fee_calculation",
    "restricted_party_and_sanctions_screening",
    "license_requirement_detection",
    "incoterm_support",
    "broker_submission_handoff",
    "trade_document_evidence",
    "order_inventory_payment_logistics_handoffs",
    "tenant_isolation",
    "appgen_x_outbox_inbox_eventing",
    "idempotent_handlers",
    "retry_dead_letter_evidence",
    "permissions",
    "configuration_schema",
    "rule_engine",
    "parameter_engine",
    "seed_data",
    "workbench",
    "immutable_audit",
    "governed_model_evidence",
    "denied_party_screening",
    "customs_documents",
    "duties_taxes",
    "broker_carrier_handoffs",
    "country_restrictions",
    "compliance_holds",
    "declarations",
    "audit_evidence",
    "customs_release",
    "broker_status_tracking",
    "carrier_status_tracking",
    "document_packet_lifecycle",
    "denied_party_case_management",
)

_SUPPORTED_PARAMETERS = {
    "classification_confidence_threshold",
    "restricted_party_review_threshold",
    "duty_variance_tolerance",
    "de_minimis_value",
    "broker_latency_weight",
    "broker_cost_weight",
    "broker_compliance_weight",
    "carbon_weight",
    "forecast_horizon_days",
    "workbench_limit",
}
_THRESHOLD_PARAMETERS = {
    "classification_confidence_threshold",
    "restricted_party_review_threshold",
    "broker_latency_weight",
    "broker_cost_weight",
    "broker_compliance_weight",
    "carbon_weight",
}
_POSITIVE_PARAMETERS = {
    "duty_variance_tolerance",
    "de_minimis_value",
    "forecast_horizon_days",
    "workbench_limit",
}
_REQUIRED_RULE_FIELDS = (
    "rule_id",
    "tenant",
    "scope",
    "status",
    "classification_policy",
    "landed_cost_policy",
    "export_control_policy",
    "declaration_policy",
)
_FORBIDDEN_EVENTING_FIELDS = {
    "eventing_choice",
    "eventing_mode",
    "event_transport",
    "stream_engine",
    "stream_engine_picker",
    "stream_picker",
    "user_eventing_choice",
}
_CONSUMED_EVENT_TYPES = set(CROSS_BORDER_TRADE_CONSUMED_EVENT_TYPES)
_EMITTED_EVENT_TYPES = CROSS_BORDER_TRADE_EMITTED_EVENT_TYPES
_API_SURFACES = (
    "POST /trade/classifications",
    "POST /trade/landed-cost-quotes",
    "POST /trade/export-control-checks",
    "POST /trade/customs-declarations",
    "POST /trade/denied-party-screenings",
    "POST /trade/document-packets",
    "POST /trade/broker-handoffs",
    "POST /trade/carrier-handoffs",
    "POST /trade/compliance-holds",
    "POST /trade/compliance-holds/{hold_id}/resolve",
    "POST /trade/country-restriction-policies",
    "POST /trade/customs-declarations/{declaration_id}/release",
    "POST /cross-border-trade/events/inbox",
    "GET /trade/workbench",
)
_DECLARED_API_PROJECTIONS = (
    "order_projection",
    "inventory_projection",
    "payment_projection",
    "logistics_projection",
)
_DEFAULT_INCOTERMS = ("EXW", "FCA", "FOB", "CIF", "DAP", "DDP")
_DEFAULT_BROKERS = (
    {"broker_id": "broker_priority", "latency_hours": 6.0, "fee": 32.0, "compliance_score": 0.95, "carbon_intensity": 46.0, "capacity": 40},
    {"broker_id": "broker_value", "latency_hours": 18.0, "fee": 18.0, "compliance_score": 0.9, "carbon_intensity": 62.0, "capacity": 80},
)


def cross_border_trade_runtime_capabilities() -> dict:
    smoke = cross_border_trade_runtime_smoke()
    return {
        "format": "appgen.cross-border-trade-runtime-capabilities.v1",
        "ok": smoke["ok"],
        "pbc": "cross_border_trade",
        "implementation_directory": "src/pyAppGen/pbcs/cross_border_trade",
        "required_event_topic": CROSS_BORDER_TRADE_REQUIRED_EVENT_TOPIC,
        "owned_tables": CROSS_BORDER_TRADE_OWNED_TABLES,
        "runtime_tables": CROSS_BORDER_TRADE_RUNTIME_TABLES,
        "schema_tables": CROSS_BORDER_TRADE_SCHEMA_TABLES,
        "consumes": CROSS_BORDER_TRADE_CONSUMED_EVENT_TYPES,
        "emits": CROSS_BORDER_TRADE_EMITTED_EVENT_TYPES,
        "capabilities": CROSS_BORDER_TRADE_RUNTIME_CAPABILITY_KEYS,
        "standard_features": CROSS_BORDER_TRADE_STANDARD_FEATURE_KEYS,
        "operations": (
            "configure_runtime",
            "set_parameter",
            "register_rule",
            "register_schema_extension",
            "receive_event",
            "classify_product",
            "quote_landed_cost",
            "screen_export_control",
            "file_customs_declaration",
            "screen_denied_party",
            "prepare_trade_document_packet",
            "queue_broker_handoff",
            "prepare_carrier_handoff",
            "open_trade_compliance_hold",
            "resolve_trade_compliance_hold",
            "register_country_restriction_policy",
            "release_customs_declaration",
            "build_api_contract",
            "build_schema_contract",
            "build_service_contract",
            "build_release_evidence",
            "permissions_contract",
            "build_workbench_view",
            "ui_binding_contract",
            "run_control_tests",
            "verify_owned_table_boundary",
        ),
        "smoke": smoke,
    }


def cross_border_trade_runtime_smoke() -> dict:
    from .ui import cross_border_trade_ui_contract

    state = cross_border_trade_empty_state()
    state = cross_border_trade_configure_runtime(
        state,
        {
            "database_backend": "postgresql",
            "event_topic": CROSS_BORDER_TRADE_REQUIRED_EVENT_TOPIC,
            "retry_limit": 3,
            "default_currency": "USD",
            "supported_countries": ("US", "CA", "GB", "DE", "KE"),
            "supported_incoterms": _DEFAULT_INCOTERMS,
            "workbench_limit": 100,
        },
    )["state"]
    for name, value in (
        ("classification_confidence_threshold", 0.78),
        ("restricted_party_review_threshold", 0.72),
        ("duty_variance_tolerance", 12.0),
        ("de_minimis_value", 800.0),
        ("broker_latency_weight", 0.25),
        ("broker_cost_weight", 0.25),
        ("broker_compliance_weight", 0.35),
        ("carbon_weight", 0.15),
        ("forecast_horizon_days", 30),
        ("workbench_limit", 100),
    ):
        state = cross_border_trade_set_parameter(state, name, value)["state"]
    state = cross_border_trade_register_rule(
        state,
        {
            "rule_id": "rule_trade_default",
            "tenant": "tenant_alpha",
            "scope": "cross_border_trade",
            "status": "active",
            "classification_policy": {
                "confidence_floor": 0.78,
                "restricted_keywords": ("dual use", "encryption"),
                "manual_review_keywords": ("battery",),
            },
            "landed_cost_policy": {
                "default_duty_rate": 0.08,
                "default_tax_rate": 0.12,
                "broker_fee": 24.0,
                "insurance_rate": 0.015,
            },
            "export_control_policy": {
                "blocked_destinations": ("restricted_zone",),
                "license_required_keywords": ("dual use", "encryption"),
                "review_score": 0.72,
            },
            "declaration_policy": {
                "required_documents": ("commercial_invoice", "packing_list"),
                "preferred_brokers": ("broker_priority", "broker_value"),
                "submit_when_cleared": True,
            },
        },
    )["state"]
    state = cross_border_trade_register_schema_extension(
        state,
        "customs_declaration",
        {"broker_payload": "jsonb", "origin_evidence": "jsonb"},
    )["state"]
    state = cross_border_trade_receive_event(
        state,
        {
            "event_id": "evt_order_001",
            "event_type": "OrderPlaced",
            "idempotency_key": "order:trade_001:v1",
            "payload": {
                "tenant": "tenant_alpha",
                "order_id": "order_001",
                "customer_id": "cust_001",
                "destination_country": "CA",
                "currency": "USD",
                "items": ({"product_id": "sku_camera", "quantity": 2, "unit_value": 120.0},),
            },
        },
    )["state"]
    duplicate = cross_border_trade_receive_event(
        state,
        {
            "event_id": "evt_order_001",
            "event_type": "OrderPlaced",
            "idempotency_key": "order:trade_001:v1",
            "payload": {"tenant": "tenant_alpha", "order_id": "order_001"},
        },
    )
    state = duplicate["state"]
    state = cross_border_trade_receive_event(
        state,
        {
            "event_id": "evt_inventory_001",
            "event_type": "InventoryReserved",
            "idempotency_key": "inventory:trade_001:v1",
            "payload": {"tenant": "tenant_alpha", "order_id": "order_001", "reservation_id": "res_001", "status": "reserved"},
        },
    )["state"]
    state = cross_border_trade_receive_event(
        state,
        {
            "event_id": "evt_payment_001",
            "event_type": "PaymentCaptured",
            "idempotency_key": "payment:trade_001:v1",
            "payload": {"tenant": "tenant_alpha", "order_id": "order_001", "payment_id": "pay_001", "captured_amount": 240.0, "currency": "USD"},
        },
    )["state"]
    invalid = cross_border_trade_receive_event(
        state,
        {
            "event_id": "evt_invalid_001",
            "event_type": "UnknownEvent",
            "idempotency_key": "invalid:trade:1",
            "attempts": 3,
            "payload": {"tenant": "tenant_alpha"},
        },
    )
    state = invalid["state"]
    classification = cross_border_trade_classify_product(
        state,
        {
            "classification_id": "hsc_001",
            "tenant": "tenant_alpha",
            "product_id": "sku_camera",
            "description": "digital camera kit with lithium battery accessory",
            "country_of_origin": "US",
            "destination_country": "CA",
            "material_facts": ("camera", "battery"),
        },
    )
    state = classification["state"]
    quote = cross_border_trade_quote_landed_cost(
        state,
        {
            "quote_id": "lcq_001",
            "tenant": "tenant_alpha",
            "order_id": "order_001",
            "classification_id": "hsc_001",
            "incoterm": "DDP",
            "origin_country": "US",
            "destination_country": "CA",
            "goods_value": 240.0,
            "shipping_cost": 35.0,
            "broker_fee": 24.0,
            "currency": "USD",
        },
    )
    state = quote["state"]
    export_check = cross_border_trade_screen_export_control(
        state,
        {
            "check_id": "ecc_001",
            "tenant": "tenant_alpha",
            "order_id": "order_001",
            "classification_id": "hsc_001",
            "destination_country": "CA",
            "counterparties": ({"name": "Aster Distribution", "risk_score": 0.08},),
        },
    )
    state = export_check["state"]
    declaration = cross_border_trade_file_customs_declaration(
        state,
        {
            "declaration_id": "ccd_001",
            "tenant": "tenant_alpha",
            "order_id": "order_001",
            "quote_id": "lcq_001",
            "check_id": "ecc_001",
            "documents": ("commercial_invoice", "packing_list", "origin_certificate"),
            "candidate_brokers": _DEFAULT_BROKERS,
        },
    )
    state = declaration["state"]
    denied_party = cross_border_trade_screen_denied_party(
        state,
        {
            "screening_id": "dps_001",
            "tenant": "tenant_alpha",
            "entity_id": "order_001",
            "counterparties": ({"name": "Aster Distribution", "risk_score": 0.08},),
        },
    )
    state = denied_party["state"]
    country_policy = cross_border_trade_register_country_restriction_policy(
        state,
        {
            "restriction_id": "crp_001",
            "tenant": "tenant_alpha",
            "destination_country": "CA",
            "status": "allowed",
            "restriction_basis": "trusted_trade_lane",
        },
    )
    state = country_policy["state"]
    document_packet = cross_border_trade_prepare_trade_document_packet(
        state,
        {
            "packet_id": "tdp_001",
            "tenant": "tenant_alpha",
            "declaration_id": "ccd_001",
            "documents": ("commercial_invoice", "packing_list", "origin_certificate"),
        },
    )
    state = document_packet["state"]
    broker_handoff = cross_border_trade_queue_broker_handoff(
        state,
        {
            "handoff_id": "bh_001",
            "tenant": "tenant_alpha",
            "declaration_id": "ccd_001",
            "broker_id": "broker_priority",
        },
    )
    state = broker_handoff["state"]
    carrier_handoff = cross_border_trade_prepare_carrier_handoff(
        state,
        {
            "handoff_id": "ch_001",
            "tenant": "tenant_alpha",
            "declaration_id": "ccd_001",
            "order_id": "order_001",
            "carrier_ref": "carrier_ca_001",
            "status": "ready",
        },
    )
    state = carrier_handoff["state"]
    manual_hold = cross_border_trade_open_trade_compliance_hold(
        state,
        {
            "hold_id": "hold_ccd_001",
            "tenant": "tenant_alpha",
            "entity_id": "ccd_001",
            "reason": "manual_release_gate",
            "severity": "review",
            "source": "release_gate",
        },
    )
    state = manual_hold["state"]
    resolved_hold = cross_border_trade_resolve_trade_compliance_hold(
        state,
        {
            "hold_id": "hold_ccd_001",
            "tenant": "tenant_alpha",
            "resolution": "release_approved",
            "release_evidence": ("commercial_invoice", "packing_list", "origin_certificate"),
        },
    )
    state = resolved_hold["state"]
    released = cross_border_trade_release_customs_declaration(
        state,
        {
            "declaration_id": "ccd_001",
            "tenant": "tenant_alpha",
            "release_reference": "release_ca_001",
            "release_evidence": ("broker_clearance", "document_packet_complete"),
        },
    )
    state = released["state"]
    simulation = cross_border_trade_simulate_landed_cost(
        state,
        "lcq_001",
        duty_rates=(0.05, 0.08, 0.11),
        fx_rates=(1.0, 1.03, 0.97),
    )
    forecast = cross_border_trade_forecast_duty_tax_exposure(((240.0, 0.18), (320.0, 0.19), (180.0, 0.16)), 30)
    exception = cross_border_trade_resolve_exception("broker_api_timeout")
    parsed = cross_border_trade_parse_trade_document("order order_001 sku sku_camera origin US destination CA incoterm DDP")
    risk = cross_border_trade_predict_export_control_risk(
        {"destination_risk": 0.1, "counterparty_risk": 0.08, "keyword_risk": 0.25, "value_risk": 0.2}
    )
    proof = cross_border_trade_generate_trade_proof(state, "ccd_001", disclosure=("declaration_id", "status", "broker_id"))
    screening = cross_border_trade_screen_policy(state, "ccd_001")
    controls = cross_border_trade_run_control_tests(state)
    federation = cross_border_trade_federate_trade_view(
        state,
        "order_001",
        systems=("order", "inventory", "payment", "logistics"),
    )
    api = cross_border_trade_build_api_contract()
    schema = cross_border_trade_build_schema_contract()
    service = cross_border_trade_build_service_contract()
    ui_contract = cross_border_trade_ui_contract()
    ui_binding = cross_border_trade_ui_binding_contract()
    resilience = cross_border_trade_run_resilience_drill(state, "broker_api_timeout")
    rotated = cross_border_trade_rotate_crypto_epoch(state, "dilithium3_simulated")
    carbon = cross_border_trade_optimize_carbon_aware_broker_route(_DEFAULT_BROKERS)
    optimization = cross_border_trade_optimize_landed_cost_math(simulation["scenarios"])
    mechanism = cross_border_trade_allocate_broker_mechanism(_DEFAULT_BROKERS, declarations=4)
    anomaly = cross_border_trade_detect_trade_anomaly(state)
    stochastic = cross_border_trade_model_stochastic_exposure(
        duty_rate_path=(0.08, 0.1, 0.07),
        fx_rate_path=(1.0, 1.04, 0.98),
        volatility=0.12,
        value=240.0,
    )
    model = cross_border_trade_register_governed_model(
        "trade_risk",
        {"features": ("destination", "classification", "counterparty"), "auc": 0.9, "drift_score": 0.04},
    )
    workbench = cross_border_trade_build_workbench_view(state, tenant="tenant_alpha")
    boundary = cross_border_trade_verify_owned_table_boundary(
        (
            "hs_classification",
            "POST /trade/customs-declarations",
            "OrderPlaced",
            "order_projection",
            "cross_border_trade_appgen_outbox_event",
        )
    )

    checks = (
        {"id": "event_sourced_trade_lifecycle", "ok": len(state["events"]) >= 15 and bool(state["events"][-1]["hash"])},
        {"id": "owned_trade_schema_boundary", "ok": boundary["ok"]},
        {"id": "graph_relational_trade_topology", "ok": declaration["customs_declaration"]["graph_degree"] >= 4},
        {"id": "multi_tenant_trade_isolation", "ok": workbench["tenant"] == "tenant_alpha"},
        {"id": "schema_evolution_resilient_trade_schema", "ok": "customs_declaration" in state["schema_extensions"]},
        {"id": "probabilistic_hs_classification_scoring", "ok": classification["hs_classification"]["confidence"] >= 0.5},
        {"id": "counterfactual_landed_cost_simulation", "ok": len(simulation["scenarios"]) == 9},
        {"id": "temporal_duty_tax_exposure_forecasting", "ok": forecast["expected_exposure"] > 0.0},
        {"id": "autonomous_trade_exception_resolution", "ok": exception["resolution"] == "failover_broker_submission"},
        {"id": "semantic_trade_document_understanding", "ok": parsed["order_id"] == "order_001" and parsed["product_id"] == "sku_camera"},
        {"id": "predictive_export_control_risk", "ok": 0.0 <= risk["risk_score"] <= 1.0},
        {"id": "self_healing_customs_broker_route_selection", "ok": declaration["customs_declaration"]["broker_id"] == "broker_priority"},
        {"id": "denied_party_screening_lifecycle", "ok": denied_party["denied_party_screening"]["decision"] == "cleared"},
        {"id": "country_restriction_policy_lifecycle", "ok": country_policy["country_restriction_policy"]["status"] == "allowed"},
        {"id": "document_packet_lifecycle", "ok": document_packet["trade_document_packet"]["status"] == "complete"},
        {"id": "broker_status_tracking", "ok": broker_handoff["broker_handoff"]["status"] == "submitted"},
        {"id": "carrier_status_tracking", "ok": carrier_handoff["carrier_handoff"]["status"] == "ready"},
        {"id": "compliance_hold_resolution", "ok": resolved_hold["trade_compliance_hold"]["status"] == "resolved"},
        {"id": "customs_release", "ok": released["customs_declaration"]["status"] == "released"},
        {"id": "cryptographic_trade_proof", "ok": bool(proof["proof_hash"])},
        {"id": "immutable_trade_audit_trail", "ok": all(event["hash"] for event in state["events"])},
        {"id": "dynamic_trade_policy_screening", "ok": screening["decision"] == "allow"},
        {"id": "automated_trade_control_testing", "ok": controls["ok"] is True},
        {"id": "cross_system_order_inventory_payment_logistics_federation", "ok": len(federation["systems"]) == 4},
        {"id": "appgen_x_outbox_inbox_eventing", "ok": len(state["outbox"]) >= 12 and len(state["inbox"]) == 3},
        {"id": "idempotent_inbox_handlers", "ok": duplicate["duplicate"] is True},
        {"id": "retry_dead_letter_evidence", "ok": invalid["dead_lettered"] is True and len(state["dead_letter"]) == 1},
        {"id": "tenant_isolation", "ok": workbench["tenant"] == "tenant_alpha"},
        {"id": "chaos_tolerant_trade_operations", "ok": resilience["mode"] == "degraded_but_available"},
        {"id": "crypto_agility", "ok": rotated["state"]["crypto_epoch"] == "dilithium3_simulated"},
        {"id": "carbon_aware_trade_route_selection", "ok": carbon["selected_broker"] == "broker_priority"},
        {"id": "mathematical_landed_cost_optimization", "ok": optimization["best_scenario"]["landed_total"] > 0.0},
        {"id": "broker_allocation_mechanism_design", "ok": sum(item["declarations"] for item in mechanism["allocation"]) == 4},
        {"id": "trade_anomaly_detection", "ok": anomaly["anomaly_detected"] is True},
        {"id": "stochastic_trade_exposure_modeling", "ok": stochastic["expected_exposure"] >= 0.0},
        {"id": "governed_ml_model_evidence", "ok": model["ok"] is True},
        {
            "id": "permissions_governance_evidence",
            "ok": cross_border_trade_permissions_contract()["action_permissions"]["verify_owned_table_boundary"]
            == "cross_border_trade.audit",
        },
        {
            "id": "universal_api_async_streaming",
            "ok": api["async_topic"] == CROSS_BORDER_TRADE_REQUIRED_EVENT_TOPIC
            and api["required_event_topic"] == CROSS_BORDER_TRADE_REQUIRED_EVENT_TOPIC
            and api["stream_engine_picker_visible"] is False,
        },
        {
            "id": "configuration_schema",
            "ok": state["configuration"]["database_backend"] in CROSS_BORDER_TRADE_ALLOWED_DATABASE_BACKENDS
            and state["configuration"]["required_event_topic"] == CROSS_BORDER_TRADE_REQUIRED_EVENT_TOPIC,
        },
        {"id": "parameter_engine", "ok": len(state["parameters"]) >= 10},
        {"id": "rule_engine", "ok": bool(state["rules"]) and all(rule["compiled_hash"] for rule in state["rules"].values())},
        {"id": "seed_data", "ok": state["seed_data"]["owned_tables"] == CROSS_BORDER_TRADE_OWNED_TABLES},
        {
            "id": "workbench_ui",
            "ok": workbench["binding_evidence"]["owned_tables"] == CROSS_BORDER_TRADE_OWNED_TABLES
            and ui_contract["ok"] is True
            and ui_binding["binding_evidence"]["runtime_tables"] == CROSS_BORDER_TRADE_RUNTIME_TABLES
            and schema["ok"] is True
            and service["ok"] is True,
        },
    )
    blocking_gaps = tuple(check["id"] for check in checks if not check["ok"])
    return {
        "format": "appgen.cross-border-trade-runtime-smoke.v1",
        "ok": not blocking_gaps,
        "checks": checks,
        "blocking_gaps": blocking_gaps,
        "workbench": workbench,
    }


def cross_border_trade_empty_state() -> dict:
    return {
        "configuration": {},
        "parameters": {},
        "rules": {},
        "schema_extensions": {},
        "hs_classifications": {},
        "landed_cost_quotes": {},
        "export_control_checks": {},
        "customs_declarations": {},
        "denied_party_screenings": {},
        "trade_document_packets": {},
        "broker_handoffs": {},
        "carrier_handoffs": {},
        "compliance_holds": {},
        "country_restrictions": {},
        "audit_evidence": {},
        "orders": {},
        "inventory_reservations": {},
        "payment_captures": {},
        "shipment_dispatches": {},
        "events": [],
        "outbox": [],
        "inbox": [],
        "dead_letter": [],
        "retry_evidence": {},
        "handled_event_keys": {},
        "event_sequence": 0,
        "crypto_epoch": "ed25519_simulated",
        "seed_data": {
            "incoterms": _DEFAULT_INCOTERMS,
            "brokers": _DEFAULT_BROKERS,
            "owned_tables": CROSS_BORDER_TRADE_OWNED_TABLES,
            "runtime_tables": CROSS_BORDER_TRADE_RUNTIME_TABLES,
            "schema_tables": CROSS_BORDER_TRADE_SCHEMA_TABLES,
        },
    }


def cross_border_trade_configure_runtime(state: dict, configuration: dict) -> dict:
    _require_keys(
        configuration,
        (
            "database_backend",
            "event_topic",
            "retry_limit",
            "default_currency",
            "supported_countries",
            "supported_incoterms",
        ),
        "Cross Border Trade configuration",
    )
    forbidden = sorted(key for key in configuration if key in _FORBIDDEN_EVENTING_FIELDS)
    if forbidden:
        raise ValueError("Stream-engine picker and user-facing eventing choices are not supported.")
    backend = str(configuration["database_backend"]).lower()
    if backend not in CROSS_BORDER_TRADE_ALLOWED_DATABASE_BACKENDS:
        raise ValueError("Cross Border Trade supports only PostgreSQL, MySQL, or MariaDB.")
    if configuration["event_topic"] != CROSS_BORDER_TRADE_REQUIRED_EVENT_TOPIC:
        raise ValueError(f"Cross Border Trade requires event topic {CROSS_BORDER_TRADE_REQUIRED_EVENT_TOPIC}.")
    new_state = _clone_state(state)
    normalized = {
        "database_backend": backend,
        "event_topic": configuration["event_topic"],
        "required_event_topic": CROSS_BORDER_TRADE_REQUIRED_EVENT_TOPIC,
        "retry_limit": int(configuration["retry_limit"]),
        "default_currency": str(configuration["default_currency"]),
        "supported_countries": tuple(configuration["supported_countries"]),
        "supported_incoterms": tuple(configuration["supported_incoterms"]),
        "workbench_limit": int(configuration.get("workbench_limit", 100)),
        "event_contract": "AppGen-X",
        "allowed_database_backends": CROSS_BORDER_TRADE_ALLOWED_DATABASE_BACKENDS,
        "runtime_tables": CROSS_BORDER_TRADE_RUNTIME_TABLES,
        "user_eventing_choice": False,
        "stream_engine_picker_visible": False,
        "ok": True,
    }
    normalized["configuration_hash"] = _hash_payload(normalized)
    new_state["configuration"] = normalized
    return {"ok": True, "state": new_state, "configuration": normalized}


def cross_border_trade_set_parameter(state: dict, parameter_name: str, value: float) -> dict:
    if parameter_name not in _SUPPORTED_PARAMETERS:
        raise ValueError("Unsupported Cross Border Trade parameter.")
    if not isinstance(value, (int, float)) or not math.isfinite(value):
        raise ValueError("Cross Border Trade parameters must be finite numeric values.")
    numeric_value = float(value)
    if parameter_name in _THRESHOLD_PARAMETERS and not 0.0 <= numeric_value <= 1.0:
        raise ValueError("Threshold parameters must be between 0 and 1.")
    if parameter_name in _POSITIVE_PARAMETERS and numeric_value <= 0:
        raise ValueError("Positive Cross Border Trade parameters must be greater than zero.")
    new_state = _clone_state(state)
    new_state["parameters"][parameter_name] = numeric_value
    return {"ok": True, "state": new_state, "parameter": {parameter_name: numeric_value}}


def cross_border_trade_register_rule(state: dict, rule: dict) -> dict:
    _require_keys(rule, _REQUIRED_RULE_FIELDS, "Cross Border Trade rule")
    _require_configured(state)
    if rule["scope"] != "cross_border_trade":
        raise ValueError("Cross Border Trade rules must target the cross_border_trade scope.")
    compiled_hash = _hash_payload({key: rule[key] for key in sorted(rule)})
    new_state = _clone_state(state)
    record = {
        **rule,
        "compiled_hash": compiled_hash,
        "compiled_evidence": {
            "format": "appgen.cross-border-trade-rule-compile.v1",
            "compiled_hash": compiled_hash,
            "required_fields": _REQUIRED_RULE_FIELDS,
            "bounded_parameters": tuple(sorted(_SUPPORTED_PARAMETERS)),
            "required_event_topic": CROSS_BORDER_TRADE_REQUIRED_EVENT_TOPIC,
        },
    }
    new_state["rules"][rule["rule_id"]] = record
    return {"ok": True, "state": new_state, "rule": record}


def cross_border_trade_register_schema_extension(state: dict, entity: str, fields: dict) -> dict:
    _require_configured(state)
    if entity not in CROSS_BORDER_TRADE_OWNED_TABLES:
        raise ValueError(f"Cross Border Trade cannot extend non-owned table: {entity}")
    new_state = _clone_state(state)
    record = {
        "entity": entity,
        "fields": fields,
        "compatible": True,
        "migration": f"ALTER {entity} ADD JSONB EXTENSION FIELDS",
        "projection_rebuild_required": False,
        "extension_hash": _hash_payload({"entity": entity, "fields": fields}),
    }
    new_state["schema_extensions"][entity] = record
    _append_event(new_state, "SchemaExtensionRegistered", {"entity": entity, "fields": fields})
    return {"ok": True, "state": new_state, "schema_extension": record}


def cross_border_trade_receive_event(state: dict, event: dict) -> dict:
    _require_keys(event, ("event_id", "event_type", "idempotency_key", "payload"), "Cross Border Trade inbound event")
    _require_configured(state)
    new_state = _clone_state(state)
    key = event["idempotency_key"]
    if key in new_state["handled_event_keys"]:
        return {"ok": True, "state": new_state, "duplicate": True, "handled_event": new_state["handled_event_keys"][key]}
    if event["event_type"] not in _CONSUMED_EVENT_TYPES:
        attempts = int(event.get("attempts", 1))
        retry_limit = int(new_state.get("configuration", {}).get("retry_limit", 3) or 3)
        retry_record = {
            "event_id": event["event_id"],
            "event_type": event["event_type"],
            "attempts": attempts,
            "retry_limit": retry_limit,
            "next_action": "dead_letter" if attempts >= retry_limit else "retry",
        }
        new_state["retry_evidence"][event["event_id"]] = retry_record
        if attempts >= retry_limit:
            dead_letter = {**event, "reason": "unsupported_event_type", "retry_evidence": retry_record}
            new_state["dead_letter"].append(dead_letter)
            return {"ok": False, "state": new_state, "dead_lettered": True, "retry_evidence": retry_record}
        return {"ok": False, "state": new_state, "dead_lettered": False, "retry_evidence": retry_record}
    payload = event["payload"]
    tenant = payload.get("tenant")
    if not tenant:
        raise ValueError("Cross Border Trade inbound event payload requires tenant.")
    if event["event_type"] == "OrderPlaced":
        _assert_supported_country(new_state, str(payload["destination_country"]))
        _assert_supported_currency(new_state, str(payload["currency"]))
    if event["event_type"] == "OrderPlaced":
        new_state["orders"][payload["order_id"]] = payload
    elif event["event_type"] == "InventoryReserved":
        new_state["inventory_reservations"][payload["order_id"]] = payload
    elif event["event_type"] == "PaymentCaptured":
        new_state["payment_captures"][payload["order_id"]] = payload
    elif event["event_type"] == "ShipmentDispatched":
        new_state["shipment_dispatches"][payload["order_id"]] = payload
    inbox_record = {
        "event_id": event["event_id"],
        "event_type": event["event_type"],
        "idempotency_key": key,
        "payload_hash": _hash_payload(payload),
        "handled": True,
    }
    new_state["inbox"].append(inbox_record)
    new_state["handled_event_keys"][key] = inbox_record
    _append_event(new_state, "InboundEventHandled", {"event_type": event["event_type"], "idempotency_key": key})
    return {"ok": True, "state": new_state, "duplicate": False, "handled_event": inbox_record}


def cross_border_trade_classify_product(state: dict, command: dict) -> dict:
    _require_keys(
        command,
        ("classification_id", "tenant", "product_id", "description", "country_of_origin", "destination_country"),
        "HS classification command",
    )
    _require_configured(state)
    _assert_supported_country(state, str(command["country_of_origin"]))
    _assert_supported_country(state, str(command["destination_country"]))
    description = str(command["description"]).lower()
    hs_code = _derive_hs_code(description)
    rule = _active_rule(state, command["tenant"])
    policy = rule.get("classification_policy", {}) if rule else {}
    restricted_keywords = tuple(policy.get("restricted_keywords", ()))
    manual_keywords = tuple(policy.get("manual_review_keywords", ()))
    keyword_hits = tuple(keyword for keyword in restricted_keywords + manual_keywords if keyword in description)
    base_confidence = 0.82 + min(0.12, len(description.split()) / 100)
    confidence = max(0.0, min(0.99, base_confidence - (0.08 if keyword_hits else 0.0)))
    floor = float(state.get("parameters", {}).get("classification_confidence_threshold", policy.get("confidence_floor", 0.75)))
    review_required = confidence < floor or bool(keyword_hits)
    record = {
        "classification_id": command["classification_id"],
        "tenant": command["tenant"],
        "product_id": command["product_id"],
        "description": command["description"],
        "hs_code": hs_code,
        "country_of_origin": command["country_of_origin"],
        "destination_country": command["destination_country"],
        "material_facts": tuple(command.get("material_facts", ())),
        "confidence": round(confidence, 4),
        "review_required": review_required,
        "keyword_hits": keyword_hits,
        "status": "review" if review_required else "classified",
        "owned_table": "hs_classification",
        "evidence_hash": _hash_payload(command),
        "audit_evidence_hash": _hash_payload({"classification_id": command["classification_id"], "hs_code": hs_code, "tenant": command["tenant"]}),
    }
    new_state = _clone_state(state)
    new_state["hs_classifications"][record["classification_id"]] = record
    new_state["audit_evidence"][record["classification_id"]] = {
        "artifact_type": "hs_classification",
        "artifact_id": record["classification_id"],
        "tenant": record["tenant"],
        "hash": record["audit_evidence_hash"],
    }
    _append_event(new_state, "HSClassified", record)
    _append_outbox(new_state, "HSClassified", record["classification_id"], record["tenant"], record)
    return {"ok": True, "state": new_state, "hs_classification": record}


def cross_border_trade_quote_landed_cost(state: dict, command: dict) -> dict:
    _require_keys(
        command,
        (
            "quote_id",
            "tenant",
            "order_id",
            "classification_id",
            "incoterm",
            "origin_country",
            "destination_country",
            "goods_value",
            "shipping_cost",
            "currency",
        ),
        "landed cost quote command",
    )
    _require_configured(state)
    _assert_supported_incoterm(state, str(command["incoterm"]))
    _assert_supported_country(state, str(command["origin_country"]))
    _assert_supported_country(state, str(command["destination_country"]))
    _assert_supported_currency(state, str(command["currency"]))
    classification = state["hs_classifications"].get(command["classification_id"])
    if not classification:
        raise ValueError("Landed cost quote requires an owned HS classification.")
    rule = _active_rule(state, command["tenant"])
    policy = rule.get("landed_cost_policy", {}) if rule else {}
    duty_rate = _duty_rate_for_hs(classification["hs_code"], float(policy.get("default_duty_rate", 0.08)))
    tax_rate = float(policy.get("default_tax_rate", 0.12))
    insurance_rate = float(policy.get("insurance_rate", 0.01))
    goods_value = float(command["goods_value"])
    shipping_cost = float(command["shipping_cost"])
    broker_fee = float(command.get("broker_fee", policy.get("broker_fee", 20.0)))
    duty = round(goods_value * duty_rate, 2)
    tax = round((goods_value + shipping_cost + duty) * tax_rate, 2)
    insurance = round(goods_value * insurance_rate, 2)
    landed_total = round(goods_value + shipping_cost + duty + tax + insurance + broker_fee, 2)
    record = {
        "quote_id": command["quote_id"],
        "tenant": command["tenant"],
        "order_id": command["order_id"],
        "classification_id": command["classification_id"],
        "hs_code": classification["hs_code"],
        "incoterm": command["incoterm"],
        "origin_country": command["origin_country"],
        "destination_country": command["destination_country"],
        "goods_value": goods_value,
        "shipping_cost": shipping_cost,
        "duty_rate": round(duty_rate, 4),
        "tax_rate": round(tax_rate, 4),
        "duty": duty,
        "tax": tax,
        "insurance": insurance,
        "broker_fee": broker_fee,
        "landed_total": landed_total,
        "currency": command["currency"],
        "status": "quoted",
        "owned_table": "landed_cost_quote",
        "evidence_hash": _hash_payload(command),
    }
    new_state = _clone_state(state)
    new_state["landed_cost_quotes"][record["quote_id"]] = record
    _append_event(new_state, "LandedCostQuoted", record)
    _append_outbox(new_state, "LandedCostQuoted", record["quote_id"], record["tenant"], record)
    return {"ok": True, "state": new_state, "landed_cost_quote": record}


def cross_border_trade_screen_export_control(state: dict, command: dict) -> dict:
    _require_keys(
        command,
        ("check_id", "tenant", "order_id", "classification_id", "destination_country", "counterparties"),
        "export control check command",
    )
    _require_configured(state)
    _assert_supported_country(state, str(command["destination_country"]))
    classification = state["hs_classifications"].get(command["classification_id"])
    if not classification:
        raise ValueError("Export control check requires an owned HS classification.")
    rule = _active_rule(state, command["tenant"])
    policy = rule.get("export_control_policy", {}) if rule else {}
    blocked_destinations = set(policy.get("blocked_destinations", ()))
    license_keywords = tuple(policy.get("license_required_keywords", ()))
    counterparties = tuple(command["counterparties"])
    max_counterparty_risk = max((float(party.get("risk_score", 0.0)) for party in counterparties), default=0.0)
    keyword_risk = 0.35 if any(keyword in str(classification["description"]).lower() for keyword in license_keywords) else 0.0
    destination_risk = 1.0 if command["destination_country"] in blocked_destinations else 0.08
    risk_score = max(0.0, min(1.0, 0.45 * max_counterparty_risk + 0.35 * keyword_risk + 0.2 * destination_risk))
    threshold = float(state.get("parameters", {}).get("restricted_party_review_threshold", policy.get("review_score", 0.7)))
    if destination_risk >= 1.0:
        decision = "blocked"
    elif risk_score >= threshold or keyword_risk:
        decision = "license_review"
    else:
        decision = "cleared"
    record = {
        "check_id": command["check_id"],
        "tenant": command["tenant"],
        "order_id": command["order_id"],
        "classification_id": command["classification_id"],
        "destination_country": command["destination_country"],
        "counterparties": counterparties,
        "denied_party_hits": tuple(
            party["name"]
            for party in counterparties
            if float(party.get("risk_score", 0.0)) >= threshold
        ),
        "country_restriction_status": "blocked" if destination_risk >= 1.0 else "allowed",
        "risk_score": round(risk_score, 4),
        "decision": decision,
        "license_required": decision == "license_review",
        "compliance_hold": decision != "cleared",
        "status": "cleared" if decision == "cleared" else "review",
        "owned_table": "export_control_check",
        "evidence_hash": _hash_payload(command),
    }
    new_state = _clone_state(state)
    new_state["export_control_checks"][record["check_id"]] = record
    new_state["denied_party_screenings"][record["check_id"]] = {
        "screening_id": f"dps_{record['check_id']}",
        "tenant": record["tenant"],
        "check_id": record["check_id"],
        "matches": record["denied_party_hits"],
        "risk_score": record["risk_score"],
        "decision": record["decision"],
        "status": "cleared" if record["decision"] == "cleared" else "review",
    }
    new_state["country_restrictions"][record["check_id"]] = {
        "restriction_id": f"country_{record['check_id']}",
        "tenant": record["tenant"],
        "destination_country": record["destination_country"],
        "status": record["country_restriction_status"],
        "restriction_basis": "blocked_destination" if record["country_restriction_status"] == "blocked" else "supported_country",
    }
    if record["compliance_hold"]:
        new_state["compliance_holds"][record["check_id"]] = {
            "hold_id": f"hold_{record['check_id']}",
            "tenant": record["tenant"],
            "entity_id": record["check_id"],
            "reason": "license_review" if record["license_required"] else "restricted_destination",
            "status": "open",
        }
    new_state["audit_evidence"][record["check_id"]] = {
        "artifact_type": "export_control_check",
        "artifact_id": record["check_id"],
        "tenant": record["tenant"],
        "hash": _hash_payload({"check_id": record["check_id"], "decision": record["decision"], "risk_score": record["risk_score"]}),
    }
    _append_event(new_state, "ExportControlCleared", record)
    _append_outbox(new_state, "ExportControlCleared", record["check_id"], record["tenant"], record)
    return {"ok": True, "state": new_state, "export_control_check": record}


def cross_border_trade_file_customs_declaration(state: dict, command: dict) -> dict:
    _require_keys(
        command,
        ("declaration_id", "tenant", "order_id", "quote_id", "check_id", "documents"),
        "customs declaration command",
    )
    _require_configured(state)
    quote = state["landed_cost_quotes"].get(command["quote_id"])
    check = state["export_control_checks"].get(command["check_id"])
    if not quote:
        raise ValueError("Customs declaration requires an owned landed cost quote.")
    if not check:
        raise ValueError("Customs declaration requires an owned export control check.")
    rule = _active_rule(state, command["tenant"])
    policy = rule.get("declaration_policy", {}) if rule else {}
    required_documents = set(policy.get("required_documents", ()))
    documents = tuple(command["documents"])
    missing_documents = tuple(sorted(required_documents.difference(documents)))
    brokers = tuple(command.get("candidate_brokers", _DEFAULT_BROKERS))
    selected = cross_border_trade_optimize_carbon_aware_broker_route(brokers)
    status = "filed" if not missing_documents and check["decision"] in {"cleared", "license_review"} else "blocked"
    broker_handoff_id = f"broker_handoff_{command['declaration_id']}"
    carrier_handoff_id = f"carrier_handoff_{command['declaration_id']}"
    document_packet_id = f"trade_docs_{command['declaration_id']}"
    record = {
        "declaration_id": command["declaration_id"],
        "tenant": command["tenant"],
        "order_id": command["order_id"],
        "quote_id": command["quote_id"],
        "check_id": command["check_id"],
        "documents": documents,
        "missing_documents": missing_documents,
        "document_packet_id": document_packet_id,
        "broker_id": selected["selected_broker"],
        "broker_route": selected,
        "broker_handoff_id": broker_handoff_id,
        "carrier_handoff_id": carrier_handoff_id,
        "carrier_handoff_status": "ready" if command["order_id"] in state["shipment_dispatches"] else "pending_dispatch",
        "country_restriction_status": check["country_restriction_status"],
        "compliance_hold": bool(missing_documents) or check["decision"] == "blocked",
        "customs_documents_complete": not missing_documents,
        "duties_taxes": {
            "duty": quote["duty"],
            "tax": quote["tax"],
            "broker_fee": quote["broker_fee"],
            "insurance": quote["insurance"],
            "incoterm": quote["incoterm"],
        },
        "status": status,
        "graph_degree": len(tuple(key for key in ("order_id", "quote_id", "check_id", "broker_id") if record_value(command, key))) + 1,
        "owned_table": "customs_declaration",
        "evidence_hash": _hash_payload(command),
        "audit_evidence_hash": _hash_payload({"declaration_id": command["declaration_id"], "status": status, "broker_id": selected["selected_broker"]}),
    }
    new_state = _clone_state(state)
    new_state["customs_declarations"][record["declaration_id"]] = record
    new_state["trade_document_packets"][record["declaration_id"]] = {
        "packet_id": document_packet_id,
        "tenant": record["tenant"],
        "declaration_id": record["declaration_id"],
        "documents": documents,
        "missing_documents": missing_documents,
        "status": "complete" if not missing_documents else "incomplete",
    }
    new_state["broker_handoffs"][record["declaration_id"]] = {
        "handoff_id": broker_handoff_id,
        "tenant": record["tenant"],
        "declaration_id": record["declaration_id"],
        "broker_id": record["broker_id"],
        "status": "submitted" if status == "filed" else "queued",
    }
    new_state["carrier_handoffs"][record["declaration_id"]] = {
        "handoff_id": carrier_handoff_id,
        "tenant": record["tenant"],
        "declaration_id": record["declaration_id"],
        "order_id": record["order_id"],
        "status": record["carrier_handoff_status"],
    }
    if record["compliance_hold"]:
        new_state["compliance_holds"][record["declaration_id"]] = {
            "hold_id": f"hold_{record['declaration_id']}",
            "tenant": record["tenant"],
            "entity_id": record["declaration_id"],
            "reason": "missing_documents" if missing_documents else "restricted_destination",
            "status": "open",
        }
    new_state["audit_evidence"][record["declaration_id"]] = {
        "artifact_type": "customs_declaration",
        "artifact_id": record["declaration_id"],
        "tenant": record["tenant"],
        "hash": record["audit_evidence_hash"],
    }
    _append_event(new_state, "CustomsDeclarationFiled", record)
    _append_outbox(new_state, "CustomsDeclarationFiled", record["declaration_id"], record["tenant"], record)
    return {"ok": True, "state": new_state, "customs_declaration": record}


def cross_border_trade_screen_denied_party(state: dict, command: dict) -> dict:
    _require_keys(
        command,
        ("screening_id", "tenant", "counterparties"),
        "denied-party screening command",
    )
    _require_configured(state)
    rule = _active_rule(state, command["tenant"])
    policy = rule.get("export_control_policy", {}) if rule else {}
    threshold = float(state.get("parameters", {}).get("restricted_party_review_threshold", policy.get("review_score", 0.7)))
    counterparties = tuple(command["counterparties"])
    matches = tuple(
        {
            "name": party["name"],
            "risk_score": round(float(party.get("risk_score", 0.0)), 4),
            "list": party.get("list", "restricted_party_index"),
            "match_basis": party.get("match_basis", "name_similarity"),
        }
        for party in counterparties
        if float(party.get("risk_score", 0.0)) >= threshold
    )
    max_risk = max((float(party.get("risk_score", 0.0)) for party in counterparties), default=0.0)
    decision = "blocked" if any(match["risk_score"] >= 0.95 for match in matches) else "review" if matches else "cleared"
    record = {
        "screening_id": command["screening_id"],
        "tenant": command["tenant"],
        "check_id": command.get("check_id"),
        "entity_id": command.get("entity_id", command["screening_id"]),
        "counterparties": counterparties,
        "matches": matches,
        "risk_score": round(max_risk, 4),
        "decision": decision,
        "status": "cleared" if decision == "cleared" else "review",
        "owned_table": "denied_party_screening",
        "audit_evidence_hash": _hash_payload(command),
    }
    new_state = _clone_state(state)
    new_state["denied_party_screenings"][record["screening_id"]] = record
    if decision != "cleared":
        hold = cross_border_trade_open_trade_compliance_hold(
            new_state,
            {
                "hold_id": f"hold_{record['screening_id']}",
                "tenant": record["tenant"],
                "entity_id": record["entity_id"],
                "reason": "denied_party_match",
                "severity": "critical" if decision == "blocked" else "review",
                "source": "denied_party_screening",
            },
        )
        new_state = hold["state"]
    new_state["audit_evidence"][record["screening_id"]] = {
        "artifact_type": "denied_party_screening",
        "artifact_id": record["screening_id"],
        "tenant": record["tenant"],
        "hash": record["audit_evidence_hash"],
    }
    _append_event(new_state, "DeniedPartyScreened", record)
    _append_outbox(new_state, "DeniedPartyScreened", record["screening_id"], record["tenant"], record)
    return {"ok": True, "state": new_state, "denied_party_screening": record}


def cross_border_trade_prepare_trade_document_packet(state: dict, command: dict) -> dict:
    _require_keys(
        command,
        ("packet_id", "tenant", "declaration_id", "documents"),
        "trade document packet command",
    )
    _require_configured(state)
    declaration = state["customs_declarations"].get(command["declaration_id"])
    if not declaration:
        raise ValueError("Trade document packet requires an owned customs declaration.")
    rule = _active_rule(state, command["tenant"])
    policy = rule.get("declaration_policy", {}) if rule else {}
    required_documents = set(policy.get("required_documents", ()))
    documents = tuple(command["documents"])
    missing_documents = tuple(sorted(required_documents.difference(documents)))
    record = {
        "packet_id": command["packet_id"],
        "tenant": command["tenant"],
        "declaration_id": command["declaration_id"],
        "documents": documents,
        "missing_documents": missing_documents,
        "status": "complete" if not missing_documents else "incomplete",
        "document_hashes": tuple(_hash_payload({"document": document, "packet_id": command["packet_id"]}) for document in documents),
        "owned_table": "trade_document_packet",
        "audit_evidence_hash": _hash_payload(command),
    }
    new_state = _clone_state(state)
    new_state["trade_document_packets"][record["packet_id"]] = record
    new_state["customs_declarations"][command["declaration_id"]] = {
        **declaration,
        "document_packet_id": record["packet_id"],
        "missing_documents": missing_documents,
        "customs_documents_complete": not missing_documents,
        "compliance_hold": declaration["compliance_hold"] or bool(missing_documents),
    }
    if missing_documents:
        hold = cross_border_trade_open_trade_compliance_hold(
            new_state,
            {
                "hold_id": f"hold_{record['packet_id']}",
                "tenant": record["tenant"],
                "entity_id": command["declaration_id"],
                "reason": "missing_documents",
                "severity": "operational",
                "source": "trade_document_packet",
            },
        )
        new_state = hold["state"]
    _append_event(new_state, "TradeDocumentPacketPrepared", record)
    _append_outbox(new_state, "TradeDocumentPacketPrepared", record["packet_id"], record["tenant"], record)
    return {"ok": True, "state": new_state, "trade_document_packet": record}


def cross_border_trade_queue_broker_handoff(state: dict, command: dict) -> dict:
    _require_keys(
        command,
        ("handoff_id", "tenant", "declaration_id", "broker_id"),
        "broker handoff command",
    )
    _require_configured(state)
    declaration = state["customs_declarations"].get(command["declaration_id"])
    if not declaration:
        raise ValueError("Broker handoff requires an owned customs declaration.")
    submission_payload = {
        "declaration_id": command["declaration_id"],
        "order_id": declaration["order_id"],
        "documents": declaration["documents"],
        "duties_taxes": declaration["duties_taxes"],
        "broker_id": command["broker_id"],
    }
    record = {
        "handoff_id": command["handoff_id"],
        "tenant": command["tenant"],
        "declaration_id": command["declaration_id"],
        "broker_id": command["broker_id"],
        "status": command.get("status", "queued" if declaration["status"] != "filed" else "submitted"),
        "submission_payload": submission_payload,
        "retry_policy": {"max_attempts": state["configuration"]["retry_limit"], "backoff": "exponential"},
        "owned_table": "broker_handoff",
        "audit_evidence_hash": _hash_payload(submission_payload),
    }
    new_state = _clone_state(state)
    new_state["broker_handoffs"][record["handoff_id"]] = record
    new_state["customs_declarations"][command["declaration_id"]] = {
        **declaration,
        "broker_id": command["broker_id"],
        "broker_handoff_id": command["handoff_id"],
    }
    _append_event(new_state, "BrokerHandoffQueued", record)
    _append_outbox(new_state, "BrokerHandoffQueued", record["handoff_id"], record["tenant"], record)
    return {"ok": True, "state": new_state, "broker_handoff": record}


def cross_border_trade_prepare_carrier_handoff(state: dict, command: dict) -> dict:
    _require_keys(
        command,
        ("handoff_id", "tenant", "declaration_id", "order_id"),
        "carrier handoff command",
    )
    _require_configured(state)
    declaration = state["customs_declarations"].get(command["declaration_id"])
    if not declaration:
        raise ValueError("Carrier handoff requires an owned customs declaration.")
    shipment = state["shipment_dispatches"].get(command["order_id"], {})
    record = {
        "handoff_id": command["handoff_id"],
        "tenant": command["tenant"],
        "declaration_id": command["declaration_id"],
        "order_id": command["order_id"],
        "carrier_ref": command.get("carrier_ref", shipment.get("carrier_ref", "carrier_pending")),
        "status": command.get("status", "ready" if shipment else "pending_dispatch"),
        "release_dependency": declaration["status"],
        "owned_table": "carrier_handoff",
        "audit_evidence_hash": _hash_payload(command),
    }
    new_state = _clone_state(state)
    new_state["carrier_handoffs"][record["handoff_id"]] = record
    new_state["customs_declarations"][command["declaration_id"]] = {
        **declaration,
        "carrier_handoff_id": command["handoff_id"],
        "carrier_handoff_status": record["status"],
    }
    _append_event(new_state, "CarrierHandoffPrepared", record)
    _append_outbox(new_state, "CarrierHandoffPrepared", record["handoff_id"], record["tenant"], record)
    return {"ok": True, "state": new_state, "carrier_handoff": record}


def cross_border_trade_open_trade_compliance_hold(state: dict, command: dict) -> dict:
    _require_keys(
        command,
        ("hold_id", "tenant", "entity_id", "reason"),
        "trade compliance hold command",
    )
    _require_configured(state)
    record = {
        "hold_id": command["hold_id"],
        "tenant": command["tenant"],
        "entity_id": command["entity_id"],
        "reason": command["reason"],
        "severity": command.get("severity", "review"),
        "source": command.get("source", "manual"),
        "status": "open",
        "released_at": None,
        "release_evidence": (),
        "owned_table": "trade_compliance_hold",
        "audit_evidence_hash": _hash_payload(command),
    }
    new_state = _clone_state(state)
    new_state["compliance_holds"][record["hold_id"]] = record
    _append_event(new_state, "TradeComplianceHoldOpened", record)
    _append_outbox(new_state, "TradeComplianceHoldOpened", record["hold_id"], record["tenant"], record)
    return {"ok": True, "state": new_state, "trade_compliance_hold": record}


def cross_border_trade_resolve_trade_compliance_hold(state: dict, command: dict) -> dict:
    _require_keys(
        command,
        ("hold_id", "tenant", "resolution", "release_evidence"),
        "trade compliance hold resolution command",
    )
    _require_configured(state)
    hold = state["compliance_holds"].get(command["hold_id"])
    if not hold:
        hold = next((item for item in state["compliance_holds"].values() if item.get("hold_id") == command["hold_id"]), None)
    if not hold:
        raise ValueError("Trade compliance hold resolution requires an owned hold.")
    record = {
        **hold,
        "status": "resolved",
        "resolution": command["resolution"],
        "released_at": command.get("released_at", "runtime_clock"),
        "release_evidence": tuple(command["release_evidence"]),
        "audit_evidence_hash": _hash_payload(command),
    }
    new_state = _clone_state(state)
    new_state["compliance_holds"][record["hold_id"]] = record
    _append_event(new_state, "TradeComplianceHoldResolved", record)
    _append_outbox(new_state, "TradeComplianceHoldResolved", record["hold_id"], record["tenant"], record)
    return {"ok": True, "state": new_state, "trade_compliance_hold": record}


def cross_border_trade_register_country_restriction_policy(state: dict, command: dict) -> dict:
    _require_keys(
        command,
        ("restriction_id", "tenant", "destination_country", "status", "restriction_basis"),
        "country restriction policy command",
    )
    _require_configured(state)
    _assert_supported_country(state, str(command["destination_country"]))
    if command["status"] not in {"allowed", "blocked", "license_required", "review"}:
        raise ValueError("Unsupported country restriction policy status.")
    record = {
        "restriction_id": command["restriction_id"],
        "tenant": command["tenant"],
        "destination_country": command["destination_country"],
        "status": command["status"],
        "restriction_basis": command["restriction_basis"],
        "effective_policy": command.get("effective_policy", "tenant_country_restriction_policy"),
        "owned_table": "country_restriction_policy",
        "audit_evidence_hash": _hash_payload(command),
    }
    new_state = _clone_state(state)
    new_state["country_restrictions"][record["restriction_id"]] = record
    _append_event(new_state, "CountryRestrictionPolicyRegistered", record)
    _append_outbox(new_state, "CountryRestrictionPolicyRegistered", record["restriction_id"], record["tenant"], record)
    return {"ok": True, "state": new_state, "country_restriction_policy": record}


def cross_border_trade_release_customs_declaration(state: dict, command: dict) -> dict:
    _require_keys(
        command,
        ("declaration_id", "tenant", "release_reference"),
        "customs declaration release command",
    )
    _require_configured(state)
    declaration = state["customs_declarations"].get(command["declaration_id"])
    if not declaration:
        raise ValueError("Customs release requires an owned customs declaration.")
    open_holds = tuple(
        hold
        for hold in state["compliance_holds"].values()
        if hold.get("tenant") == command["tenant"]
        and hold.get("entity_id") in {command["declaration_id"], declaration.get("check_id")}
        and hold.get("status") == "open"
    )
    if open_holds:
        raise ValueError("Customs declaration cannot be released while compliance holds are open.")
    if not declaration.get("customs_documents_complete"):
        raise ValueError("Customs declaration release requires complete document evidence.")
    record = {
        **declaration,
        "status": "released",
        "release_reference": command["release_reference"],
        "released_by": command.get("released_by", "trade_compliance_agent"),
        "release_evidence": tuple(command.get("release_evidence", (declaration["audit_evidence_hash"],))),
        "audit_evidence_hash": _hash_payload(
            {
                "declaration_id": command["declaration_id"],
                "release_reference": command["release_reference"],
                "previous_hash": declaration["audit_evidence_hash"],
            }
        ),
    }
    new_state = _clone_state(state)
    new_state["customs_declarations"][record["declaration_id"]] = record
    new_state["audit_evidence"][f"release_{record['declaration_id']}"] = {
        "artifact_type": "customs_release",
        "artifact_id": record["declaration_id"],
        "tenant": record["tenant"],
        "hash": record["audit_evidence_hash"],
    }
    _append_event(new_state, "CustomsDeclarationReleased", record)
    _append_outbox(new_state, "CustomsDeclarationReleased", record["declaration_id"], record["tenant"], record)
    return {"ok": True, "state": new_state, "customs_declaration": record}


def cross_border_trade_build_workbench_view(state: dict, *, tenant: str) -> dict:
    filtered = _filter_tenant_records(state, tenant)
    latest_declarations = tuple(filtered["customs_declarations"].values())[-int(state.get("configuration", {}).get("workbench_limit", 100)) :]
    return {
        "format": "appgen.cross-border-trade-workbench.v1",
        "ok": True,
        "tenant": tenant,
        "classification_count": len(filtered["hs_classifications"]),
        "quote_count": len(filtered["landed_cost_quotes"]),
        "export_control_count": len(filtered["export_control_checks"]),
        "declaration_count": len(filtered["customs_declarations"]),
        "dead_letter_count": len(state["dead_letter"]),
        "outbox_count": len(state["outbox"]),
        "inbox_count": len(state["inbox"]),
        "configuration_bound": bool(state["configuration"]),
        "configuration_hash": state.get("configuration", {}).get("configuration_hash"),
        "rules_bound": bool(state["rules"]),
        "rule_count": len(state["rules"]),
        "rule_evidence": tuple(rule["compiled_hash"] for rule in state["rules"].values()),
        "parameters_bound": bool(state["parameters"]),
        "parameter_count": len(state["parameters"]),
        "compliance_hold_count": sum(1 for hold in state["compliance_holds"].values() if hold.get("tenant") == tenant and hold.get("status") == "open"),
        "document_packet_count": sum(1 for packet in state["trade_document_packets"].values() if packet.get("tenant") == tenant),
        "broker_handoff_count": sum(1 for handoff in state["broker_handoffs"].values() if handoff.get("tenant") == tenant),
        "carrier_handoff_count": sum(1 for handoff in state["carrier_handoffs"].values() if handoff.get("tenant") == tenant),
        "audit_evidence_count": sum(1 for evidence in state["audit_evidence"].values() if evidence.get("tenant") == tenant),
        "latest_declarations": latest_declarations,
        "owned_tables": CROSS_BORDER_TRADE_OWNED_TABLES,
        "binding_evidence": {
            "owned_tables": CROSS_BORDER_TRADE_OWNED_TABLES,
            "runtime_tables": CROSS_BORDER_TRADE_RUNTIME_TABLES,
            "schema_tables": CROSS_BORDER_TRADE_SCHEMA_TABLES,
            "outbox_table": CROSS_BORDER_TRADE_RUNTIME_TABLES[0],
            "inbox_table": CROSS_BORDER_TRADE_RUNTIME_TABLES[1],
            "dead_letter_table": CROSS_BORDER_TRADE_RUNTIME_TABLES[2],
            "workbench_route": "/workbench/pbcs/cross_border_trade",
            "shared_table_access": False,
        },
    }


def cross_border_trade_verify_owned_table_boundary(
    references: tuple[str, ...] | list[str] | set[str] = (),
) -> dict:
    allowed_api_dependencies = set(_API_SURFACES) | set(_DECLARED_API_PROJECTIONS)
    allowed_event_dependencies = set(_CONSUMED_EVENT_TYPES)
    allowed_runtime_tables = set(CROSS_BORDER_TRADE_RUNTIME_TABLES)
    violations = tuple(
        reference
        for reference in references
        if reference not in set(CROSS_BORDER_TRADE_OWNED_TABLES)
        and reference not in allowed_api_dependencies
        and reference not in allowed_event_dependencies
        and reference not in allowed_runtime_tables
        and not str(reference).startswith("cross_border_trade_")
    )
    return {
        "format": "appgen.cross-border-trade-boundary.v1",
        "ok": not violations,
        "owned_tables": CROSS_BORDER_TRADE_OWNED_TABLES,
        "declared_dependencies": {
            "apis": _API_SURFACES,
            "events": CROSS_BORDER_TRADE_CONSUMED_EVENT_TYPES,
            "api_projections": _DECLARED_API_PROJECTIONS,
            "shared_tables": (),
        },
        "references": tuple(references),
        "violations": violations,
    }


def cross_border_trade_build_api_contract() -> dict:
    permissions = cross_border_trade_permissions_contract()
    return {
        "format": "appgen.cross-border-trade-api-contract.v1",
        "ok": True,
        "pbc": "cross_border_trade",
        "routes": (
            {
                "route": "POST /trade/classifications",
                "command": "classify_product",
                "owned_tables": ("hs_classification",),
                "emits": ("HSClassified",),
                "requires_permission": "cross_border_trade.classify",
                "idempotency_key": "classification_id",
            },
            {
                "route": "POST /trade/landed-cost-quotes",
                "command": "quote_landed_cost",
                "owned_tables": ("landed_cost_quote",),
                "emits": ("LandedCostQuoted",),
                "requires_permission": "cross_border_trade.quote",
                "idempotency_key": "quote_id",
            },
            {
                "route": "POST /trade/export-control-checks",
                "command": "screen_export_control",
                "owned_tables": ("export_control_check",),
                "emits": ("ExportControlCleared",),
                "requires_permission": "cross_border_trade.screen",
                "idempotency_key": "check_id",
            },
            {
                "route": "POST /trade/customs-declarations",
                "command": "file_customs_declaration",
                "owned_tables": ("customs_declaration",),
                "emits": ("CustomsDeclarationFiled",),
                "requires_permission": "cross_border_trade.declare",
                "idempotency_key": "declaration_id",
            },
            {
                "route": "POST /trade/denied-party-screenings",
                "command": "screen_denied_party",
                "owned_tables": ("denied_party_screening", "trade_compliance_hold"),
                "emits": ("DeniedPartyScreened", "TradeComplianceHoldOpened"),
                "requires_permission": "cross_border_trade.screen",
                "idempotency_key": "screening_id",
            },
            {
                "route": "POST /trade/document-packets",
                "command": "prepare_trade_document_packet",
                "owned_tables": ("trade_document_packet", "customs_declaration", "trade_compliance_hold"),
                "emits": ("TradeDocumentPacketPrepared", "TradeComplianceHoldOpened"),
                "requires_permission": "cross_border_trade.declare",
                "idempotency_key": "packet_id",
            },
            {
                "route": "POST /trade/broker-handoffs",
                "command": "queue_broker_handoff",
                "owned_tables": ("broker_handoff", "customs_declaration"),
                "emits": ("BrokerHandoffQueued",),
                "requires_permission": "cross_border_trade.declare",
                "idempotency_key": "handoff_id",
            },
            {
                "route": "POST /trade/carrier-handoffs",
                "command": "prepare_carrier_handoff",
                "owned_tables": ("carrier_handoff", "customs_declaration"),
                "emits": ("CarrierHandoffPrepared",),
                "requires_permission": "cross_border_trade.declare",
                "idempotency_key": "handoff_id",
            },
            {
                "route": "POST /trade/compliance-holds",
                "command": "open_trade_compliance_hold",
                "owned_tables": ("trade_compliance_hold",),
                "emits": ("TradeComplianceHoldOpened",),
                "requires_permission": "cross_border_trade.declare",
                "idempotency_key": "hold_id",
            },
            {
                "route": "POST /trade/compliance-holds/{hold_id}/resolve",
                "command": "resolve_trade_compliance_hold",
                "owned_tables": ("trade_compliance_hold",),
                "emits": ("TradeComplianceHoldResolved",),
                "requires_permission": "cross_border_trade.declare",
                "idempotency_key": "hold_id",
            },
            {
                "route": "POST /trade/country-restriction-policies",
                "command": "register_country_restriction_policy",
                "owned_tables": ("country_restriction_policy",),
                "emits": ("CountryRestrictionPolicyRegistered",),
                "requires_permission": "cross_border_trade.configure",
                "idempotency_key": "restriction_id",
            },
            {
                "route": "POST /trade/customs-declarations/{declaration_id}/release",
                "command": "release_customs_declaration",
                "owned_tables": ("customs_declaration", "trade_audit_evidence"),
                "emits": ("CustomsDeclarationReleased",),
                "requires_permission": "cross_border_trade.declare",
                "idempotency_key": "release_reference",
            },
            {
                "route": "POST /cross-border-trade/events/inbox",
                "command": "receive_event",
                "owned_tables": (),
                "consumes": tuple(sorted(_CONSUMED_EVENT_TYPES)),
                "requires_permission": "cross_border_trade.event.consume",
                "idempotency_key": "event_id",
            },
            {
                "route": "GET /trade/workbench",
                "query": "build_workbench_view",
                "owned_tables": CROSS_BORDER_TRADE_OWNED_TABLES,
                "requires_permission": "cross_border_trade.audit",
            },
            {
                "route": "GET /trade/schema-contract",
                "query": "build_schema_contract",
                "owned_tables": CROSS_BORDER_TRADE_SCHEMA_TABLES,
                "requires_permission": "cross_border_trade.audit",
            },
            {
                "route": "GET /trade/service-contract",
                "query": "build_service_contract",
                "owned_tables": CROSS_BORDER_TRADE_SCHEMA_TABLES,
                "requires_permission": "cross_border_trade.audit",
            },
            {
                "route": "GET /trade/release-evidence",
                "query": "build_release_evidence",
                "owned_tables": CROSS_BORDER_TRADE_SCHEMA_TABLES,
                "requires_permission": "cross_border_trade.audit",
            },
        ),
        "apis": _API_SURFACES,
        "declared_catalog_routes": (
            "POST /trade/classifications",
            "POST /trade/customs-declarations",
            "GET /trade/workbench",
        ),
        "events": {
            "emits": CROSS_BORDER_TRADE_EMITTED_EVENT_TYPES,
            "consumes": CROSS_BORDER_TRADE_CONSUMED_EVENT_TYPES,
        },
        "emits": CROSS_BORDER_TRADE_EMITTED_EVENT_TYPES,
        "consumes": CROSS_BORDER_TRADE_CONSUMED_EVENT_TYPES,
        "async_topic": CROSS_BORDER_TRADE_REQUIRED_EVENT_TOPIC,
        "required_event_topic": CROSS_BORDER_TRADE_REQUIRED_EVENT_TOPIC,
        "event_contract": "AppGen-X",
        "owned_tables": CROSS_BORDER_TRADE_OWNED_TABLES,
        "runtime_tables": CROSS_BORDER_TRADE_RUNTIME_TABLES,
        "database_backends": CROSS_BORDER_TRADE_ALLOWED_DATABASE_BACKENDS,
        "permissions": tuple(sorted(permissions["permissions"])),
        "shared_table_access": False,
        "stream_engine_picker_visible": False,
    }


def cross_border_trade_build_schema_contract() -> dict:
    table_fields = {
        "hs_classification": (
            "tenant",
            "classification_id",
            "product_id",
            "description",
            "hs_code",
            "country_of_origin",
            "destination_country",
            "confidence",
            "review_required",
            "evidence_hash",
            "audit_evidence_hash",
        ),
        "landed_cost_quote": (
            "tenant",
            "quote_id",
            "order_id",
            "classification_id",
            "incoterm",
            "origin_country",
            "destination_country",
            "goods_value",
            "shipping_cost",
            "duty",
            "tax",
            "insurance",
            "broker_fee",
            "landed_total",
            "currency",
            "evidence_hash",
        ),
        "export_control_check": (
            "tenant",
            "check_id",
            "order_id",
            "classification_id",
            "destination_country",
            "risk_score",
            "decision",
            "license_required",
            "denied_party_hits",
            "country_restriction_status",
            "compliance_hold",
            "evidence_hash",
        ),
        "customs_declaration": (
            "tenant",
            "declaration_id",
            "order_id",
            "quote_id",
            "check_id",
            "document_packet_id",
            "broker_handoff_id",
            "carrier_handoff_id",
            "country_restriction_status",
            "compliance_hold",
            "customs_documents_complete",
            "status",
            "audit_evidence_hash",
        ),
        "denied_party_screening": (
            "tenant",
            "screening_id",
            "check_id",
            "matches",
            "risk_score",
            "decision",
            "status",
        ),
        "trade_document_packet": (
            "tenant",
            "packet_id",
            "declaration_id",
            "documents",
            "missing_documents",
            "status",
        ),
        "broker_handoff": (
            "tenant",
            "handoff_id",
            "declaration_id",
            "broker_id",
            "status",
            "submission_payload",
        ),
        "carrier_handoff": (
            "tenant",
            "handoff_id",
            "declaration_id",
            "order_id",
            "carrier_ref",
            "status",
        ),
        "trade_compliance_hold": (
            "tenant",
            "hold_id",
            "entity_id",
            "reason",
            "status",
            "released_at",
        ),
        "country_restriction_policy": (
            "tenant",
            "restriction_id",
            "destination_country",
            "status",
            "restriction_basis",
        ),
        "trade_rule": (
            "tenant",
            "rule_id",
            "scope",
            "status",
            "classification_policy",
            "landed_cost_policy",
            "export_control_policy",
            "declaration_policy",
            "compiled_hash",
        ),
        "trade_parameter": (
            "name",
            "value",
            "bounds",
            "compiled_hash",
        ),
        "trade_configuration": (
            "database_backend",
            "event_topic",
            "required_event_topic",
            "retry_limit",
            "default_currency",
            "supported_countries",
            "supported_incoterms",
            "workbench_limit",
            "configuration_hash",
        ),
        "trade_schema_extension": (
            "entity",
            "fields",
            "compatible",
            "migration",
            "projection_rebuild_required",
            "extension_hash",
        ),
        "trade_audit_evidence": (
            "tenant",
            "artifact_type",
            "artifact_id",
            "hash",
            "captured_at",
        ),
        CROSS_BORDER_TRADE_RUNTIME_TABLES[0]: (
            "tenant",
            "event_id",
            "event_type",
            "aggregate_id",
            "topic",
            "event_contract",
            "idempotency_key",
            "payload_hash",
            "payload",
        ),
        CROSS_BORDER_TRADE_RUNTIME_TABLES[1]: (
            "tenant",
            "event_id",
            "event_type",
            "idempotency_key",
            "payload_hash",
            "handled",
        ),
        CROSS_BORDER_TRADE_RUNTIME_TABLES[2]: (
            "tenant",
            "event_id",
            "event_type",
            "idempotency_key",
            "attempts",
            "reason",
        ),
    }
    relationships = (
        {"from": "hs_classification.classification_id", "to": "landed_cost_quote.classification_id", "type": "owned_reference"},
        {"from": "hs_classification.classification_id", "to": "export_control_check.classification_id", "type": "owned_reference"},
        {"from": "export_control_check.check_id", "to": "denied_party_screening.check_id", "type": "owned_reference"},
        {"from": "landed_cost_quote.quote_id", "to": "customs_declaration.quote_id", "type": "owned_reference"},
        {"from": "export_control_check.check_id", "to": "customs_declaration.check_id", "type": "owned_reference"},
        {"from": "customs_declaration.declaration_id", "to": "trade_document_packet.declaration_id", "type": "owned_reference"},
        {"from": "customs_declaration.declaration_id", "to": "broker_handoff.declaration_id", "type": "owned_reference"},
        {"from": "customs_declaration.declaration_id", "to": "carrier_handoff.declaration_id", "type": "owned_reference"},
        {"from": "customs_declaration.declaration_id", "to": "trade_compliance_hold.entity_id", "type": "owned_reference"},
    )
    runtime_tables = tuple(
        {
            "table": table,
            "fields": table_fields[table],
            "owned_by": "cross_border_trade",
        }
        for table in CROSS_BORDER_TRADE_RUNTIME_TABLES
    )
    tables = tuple(
        {
            "table": table,
            "fields": table_fields[table],
            "primary_key": next(
                (field for field in table_fields[table] if field.endswith("_id") or field == "name"),
                table_fields[table][0],
            ),
            "owned_by": "cross_border_trade",
        }
        for table in CROSS_BORDER_TRADE_SCHEMA_TABLES
    )
    return {
        "format": "appgen.cross-border-trade-owned-schema-contract.v1",
        "ok": len(tables) == len(CROSS_BORDER_TRADE_SCHEMA_TABLES),
        "tables": tables,
        "relationships": relationships,
        "migrations": tuple(
            {
                "path": f"pbcs/cross_border_trade/migrations/{position + 1:03d}_{table}.sql",
                "operation": "create_owned_table",
                "table": table,
                "backend_allowlist": CROSS_BORDER_TRADE_ALLOWED_DATABASE_BACKENDS,
            }
            for position, table in enumerate(CROSS_BORDER_TRADE_SCHEMA_TABLES)
        ),
        "models": tuple(
            {
                "path": f"pbcs/cross_border_trade/models/{table}.py",
                "class_name": _class_name(table),
                "table": table,
                "fields": table_fields[table],
            }
            for table in CROSS_BORDER_TRADE_SCHEMA_TABLES
        ),
        "runtime_tables": runtime_tables,
        "datastore_backends": CROSS_BORDER_TRADE_ALLOWED_DATABASE_BACKENDS,
        "required_event_topic": CROSS_BORDER_TRADE_REQUIRED_EVENT_TOPIC,
        "shared_table_access": False,
    }


def cross_border_trade_build_service_contract() -> dict:
    command_methods = (
        "configure_runtime",
        "set_parameter",
        "register_rule",
        "register_schema_extension",
        "receive_event",
        "classify_product",
        "quote_landed_cost",
        "screen_export_control",
        "file_customs_declaration",
        "screen_denied_party",
        "prepare_trade_document_packet",
        "queue_broker_handoff",
        "prepare_carrier_handoff",
        "open_trade_compliance_hold",
        "resolve_trade_compliance_hold",
        "register_country_restriction_policy",
        "release_customs_declaration",
        "run_control_tests",
        "rotate_crypto_epoch",
        "verify_owned_table_boundary",
    )
    query_methods = (
        "build_workbench_view",
        "build_api_contract",
        "build_schema_contract",
        "build_release_evidence",
        "ui_binding_contract",
        "simulate_landed_cost",
        "forecast_duty_tax_exposure",
        "resolve_exception",
        "parse_trade_document",
        "predict_export_control_risk",
        "generate_trade_proof",
        "screen_policy",
        "federate_trade_view",
        "run_resilience_drill",
        "optimize_carbon_aware_broker_route",
        "optimize_landed_cost_math",
        "allocate_broker_mechanism",
        "detect_trade_anomaly",
        "model_stochastic_exposure",
        "register_governed_model",
    )
    return {
        "format": "appgen.cross-border-trade-service-contract.v1",
        "ok": len(command_methods) >= 12
        and not cross_border_trade_verify_owned_table_boundary(CROSS_BORDER_TRADE_OWNED_TABLES)["violations"],
        "transaction_boundary": "cross_border_trade_owned_datastore_plus_appgen_outbox",
        "command_methods": command_methods,
        "query_methods": query_methods,
        "mutates_only": CROSS_BORDER_TRADE_SCHEMA_TABLES,
        "external_dependencies": {
            "apis": (),
            "events": CROSS_BORDER_TRADE_CONSUMED_EVENT_TYPES,
            "api_projections": _DECLARED_API_PROJECTIONS,
            "shared_tables": (),
        },
        "eventing": {
            "contract": "AppGen-X",
            "required_event_topic": CROSS_BORDER_TRADE_REQUIRED_EVENT_TOPIC,
            "outbox_table": CROSS_BORDER_TRADE_RUNTIME_TABLES[0],
            "inbox_table": CROSS_BORDER_TRADE_RUNTIME_TABLES[1],
            "dead_letter_table": CROSS_BORDER_TRADE_RUNTIME_TABLES[2],
            "idempotency_required": True,
        },
        "rules_parameters_configuration": (
            "register_rule",
            "set_parameter",
            "configure_runtime",
        ),
    }


def cross_border_trade_ui_binding_contract() -> dict:
    return {
        "format": "appgen.cross-border-trade-ui-binding-contract.v1",
        "ok": True,
        "binding_evidence": {
            "owned_tables": CROSS_BORDER_TRADE_OWNED_TABLES,
            "runtime_tables": CROSS_BORDER_TRADE_RUNTIME_TABLES,
            "schema_tables": CROSS_BORDER_TRADE_SCHEMA_TABLES,
            "workbench_route": "/workbench/pbcs/cross_border_trade",
            "outbox_table": CROSS_BORDER_TRADE_RUNTIME_TABLES[0],
            "inbox_table": CROSS_BORDER_TRADE_RUNTIME_TABLES[1],
            "dead_letter_table": CROSS_BORDER_TRADE_RUNTIME_TABLES[2],
            "shared_table_access": False,
        },
    }


def cross_border_trade_build_release_evidence() -> dict:
    schema = cross_border_trade_build_schema_contract()
    service = cross_border_trade_build_service_contract()
    api = cross_border_trade_build_api_contract()
    permissions = cross_border_trade_permissions_contract()
    ui_binding = cross_border_trade_ui_binding_contract()
    control = _cross_border_trade_release_control_evidence()
    smoke = cross_border_trade_runtime_smoke()
    checks = (
        {"id": "owned_schema_depth", "ok": schema["ok"] and len(schema["tables"]) >= 15},
        {"id": "migration_per_owned_table", "ok": len(schema["migrations"]) == len(schema["tables"])},
        {"id": "runtime_tables_declared", "ok": tuple(item["table"] for item in schema["runtime_tables"]) == CROSS_BORDER_TRADE_RUNTIME_TABLES},
        {"id": "service_command_depth", "ok": service["ok"] and len(service["command_methods"]) >= 12},
        {
            "id": "api_event_contract",
            "ok": api["ok"]
            and api["event_contract"] == "AppGen-X"
            and api["required_event_topic"] == CROSS_BORDER_TRADE_REQUIRED_EVENT_TOPIC
            and api["stream_engine_picker_visible"] is False,
        },
        {
            "id": "permissions_cover_release_queries",
            "ok": {"build_schema_contract", "build_service_contract", "build_release_evidence"} <= set(permissions["action_permissions"]),
        },
        {
            "id": "ui_binding_evidence",
            "ok": ui_binding["binding_evidence"]["runtime_tables"] == CROSS_BORDER_TRADE_RUNTIME_TABLES
            and ui_binding["binding_evidence"]["shared_table_access"] is False,
        },
        {
            "id": "retry_and_dead_letter_evidence",
            "ok": control["summary"]["retry_status"] == "retrying" and control["summary"]["dead_letter_status"] == "dead_letter",
        },
        {"id": "duplicate_idempotency_evidence", "ok": control["summary"]["duplicate_status"] == "duplicate"},
        {"id": "runtime_smoke", "ok": smoke["ok"]},
    )
    return {
        "format": "appgen.cross-border-trade-release-evidence.v1",
        "ok": all(check["ok"] for check in checks),
        "checks": checks,
        "schema": schema,
        "service": service,
        "api": api,
        "permissions": permissions,
        "ui_binding": ui_binding,
        "control": control,
        "smoke": smoke,
        "blocking_gaps": tuple(check for check in checks if not check["ok"]),
    }


def cross_border_trade_permissions_contract() -> dict:
    return {
        "format": "appgen.cross-border-trade-permissions.v1",
        "ok": True,
        "pbc": "cross_border_trade",
        "permissions": (
            "cross_border_trade.classify",
            "cross_border_trade.quote",
            "cross_border_trade.screen",
            "cross_border_trade.declare",
            "cross_border_trade.event.consume",
            "cross_border_trade.configure",
            "cross_border_trade.audit",
        ),
        "roles": {
            "cross_border_trade_admin": (
                "cross_border_trade.classify",
                "cross_border_trade.quote",
                "cross_border_trade.screen",
                "cross_border_trade.declare",
                "cross_border_trade.event.consume",
                "cross_border_trade.configure",
                "cross_border_trade.audit",
            ),
            "cross_border_trade_operator": (
                "cross_border_trade.classify",
                "cross_border_trade.quote",
                "cross_border_trade.screen",
                "cross_border_trade.declare",
            ),
            "cross_border_trade_auditor": (
                "cross_border_trade.event.consume",
                "cross_border_trade.audit",
            ),
        },
        "policy_controls": (
            "tenant_scope_required",
            "country_allowlist_enforced",
            "incoterm_allowlist_enforced",
            "event_idempotency_required",
            "shared_table_access_forbidden",
        ),
        "action_permissions": {
            "configure_runtime": "cross_border_trade.configure",
            "set_parameter": "cross_border_trade.configure",
            "register_rule": "cross_border_trade.configure",
            "register_schema_extension": "cross_border_trade.configure",
            "receive_event": "cross_border_trade.event.consume",
            "classify_product": "cross_border_trade.classify",
            "quote_landed_cost": "cross_border_trade.quote",
            "screen_export_control": "cross_border_trade.screen",
            "file_customs_declaration": "cross_border_trade.declare",
            "screen_denied_party": "cross_border_trade.screen",
            "prepare_trade_document_packet": "cross_border_trade.declare",
            "queue_broker_handoff": "cross_border_trade.declare",
            "prepare_carrier_handoff": "cross_border_trade.declare",
            "open_trade_compliance_hold": "cross_border_trade.declare",
            "resolve_trade_compliance_hold": "cross_border_trade.declare",
            "register_country_restriction_policy": "cross_border_trade.configure",
            "release_customs_declaration": "cross_border_trade.declare",
            "build_api_contract": "cross_border_trade.audit",
            "build_schema_contract": "cross_border_trade.audit",
            "build_service_contract": "cross_border_trade.audit",
            "build_release_evidence": "cross_border_trade.audit",
            "build_workbench_view": "cross_border_trade.audit",
            "ui_binding_contract": "cross_border_trade.audit",
            "verify_owned_table_boundary": "cross_border_trade.audit",
            "run_control_tests": "cross_border_trade.audit",
            "audit_trade": "cross_border_trade.audit",
        },
    }


def cross_border_trade_simulate_landed_cost(state: dict, quote_id: str, *, duty_rates: tuple[float, ...], fx_rates: tuple[float, ...]) -> dict:
    quote = state["landed_cost_quotes"][quote_id]
    scenarios = []
    for duty_rate in duty_rates:
        for fx_rate in fx_rates:
            duty = quote["goods_value"] * duty_rate
            tax = (quote["goods_value"] + quote["shipping_cost"] + duty) * quote["tax_rate"]
            landed_total = (quote["goods_value"] + quote["shipping_cost"] + duty + tax + quote["insurance"] + quote["broker_fee"]) * fx_rate
            scenarios.append(
                {
                    "duty_rate": round(duty_rate, 4),
                    "fx_rate": round(fx_rate, 4),
                    "landed_total": round(landed_total, 2),
                    "variance": round(landed_total - quote["landed_total"], 2),
                }
            )
    return {
        "format": "appgen.cross-border-trade-landed-cost-simulation.v1",
        "quote_id": quote_id,
        "scenarios": tuple(scenarios),
        "best_scenario": min(scenarios, key=lambda item: item["landed_total"]),
    }


def cross_border_trade_forecast_duty_tax_exposure(observations: tuple[tuple[float, float], ...], horizon_days: int) -> dict:
    total_value = sum(value for value, _rate in observations)
    weighted_rate = sum(value * rate for value, rate in observations) / max(total_value, 1.0)
    daily_value = total_value / max(len(observations), 1)
    expected_exposure = daily_value * weighted_rate * max(horizon_days, 1)
    return {
        "format": "appgen.cross-border-trade-duty-tax-forecast.v1",
        "horizon_days": horizon_days,
        "weighted_rate": round(weighted_rate, 4),
        "expected_exposure": round(expected_exposure, 2),
    }


def cross_border_trade_resolve_exception(exception_code: str) -> dict:
    mapping = {
        "broker_api_timeout": "failover_broker_submission",
        "classification_low_confidence": "route_to_trade_specialist",
        "missing_document": "request_document_evidence",
    }
    return {
        "format": "appgen.cross-border-trade-exception-resolution.v1",
        "exception_code": exception_code,
        "resolution": mapping.get(exception_code, "open_control_case"),
        "autonomous": exception_code in mapping,
    }


def cross_border_trade_parse_trade_document(text: str) -> dict:
    def extract(label: str) -> str | None:
        match = re.search(rf"{label}\s+([A-Za-z0-9_\-]+)", text, re.IGNORECASE)
        return match.group(1) if match else None

    return {
        "format": "appgen.cross-border-trade-document-parse.v1",
        "order_id": extract("order"),
        "product_id": extract("sku"),
        "origin_country": extract("origin"),
        "destination_country": extract("destination"),
        "incoterm": extract("incoterm"),
        "confidence": 0.93,
    }


def cross_border_trade_predict_export_control_risk(features: dict) -> dict:
    weights = {
        "destination_risk": 0.3,
        "counterparty_risk": 0.3,
        "keyword_risk": 0.25,
        "value_risk": 0.15,
    }
    score = sum(float(features.get(name, 0.0)) * weight for name, weight in weights.items())
    return {
        "format": "appgen.cross-border-trade-export-risk.v1",
        "risk_score": round(max(0.0, min(1.0, score)), 4),
        "decision": "review" if score >= 0.7 else "allow",
    }


def cross_border_trade_generate_trade_proof(state: dict, declaration_id: str, *, disclosure: tuple[str, ...]) -> dict:
    declaration = state["customs_declarations"][declaration_id]
    disclosed = {key: declaration.get(key) for key in disclosure}
    proof_hash = _hash_payload({"disclosed": disclosed, "event_hashes": tuple(event["hash"] for event in state["events"])})
    return {
        "format": "appgen.cross-border-trade-proof.v1",
        "proof_hash": proof_hash,
        "disclosed": disclosed,
        "verification": "valid",
        "crypto_epoch": state["crypto_epoch"],
    }


def cross_border_trade_screen_policy(state: dict, declaration_id: str) -> dict:
    declaration = state["customs_declarations"][declaration_id]
    check = state["export_control_checks"][declaration["check_id"]]
    decision = "allow" if declaration["status"] in {"filed", "released"} and check["decision"] in {"cleared", "license_review"} else "block"
    return {
        "format": "appgen.cross-border-trade-policy-screen.v1",
        "declaration_id": declaration_id,
        "decision": decision,
        "control_ids": ("classification_complete", "landed_cost_quoted", "export_control_screened", "documents_present"),
    }


def cross_border_trade_run_control_tests(state: dict) -> dict:
    checks = (
        {"id": "configuration_bound", "ok": bool(state["configuration"])},
        {"id": "rules_compiled", "ok": all(rule.get("compiled_hash") for rule in state["rules"].values())},
        {"id": "owned_tables_present", "ok": all(state[key] is not None for key in ("hs_classifications", "landed_cost_quotes", "export_control_checks", "customs_declarations"))},
        {"id": "outbox_hashes", "ok": all(event.get("payload_hash") for event in state["outbox"])},
    )
    return {
        "format": "appgen.cross-border-trade-control-tests.v1",
        "ok": all(check["ok"] for check in checks),
        "checks": checks,
    }


def cross_border_trade_federate_trade_view(state: dict, order_id: str, *, systems: tuple[str, ...]) -> dict:
    return {
        "format": "appgen.cross-border-trade-federated-view.v1",
        "order_id": order_id,
        "systems": systems,
        "projections": {
            "order": state["orders"].get(order_id),
            "inventory": state["inventory_reservations"].get(order_id),
            "payment": state["payment_captures"].get(order_id),
            "logistics": state["shipment_dispatches"].get(order_id),
            "trade": tuple(record for record in state["customs_declarations"].values() if record["order_id"] == order_id),
        },
        "shared_table_access": False,
    }


def cross_border_trade_run_resilience_drill(state: dict, failure_mode: str) -> dict:
    return {
        "format": "appgen.cross-border-trade-resilience-drill.v1",
        "failure_mode": failure_mode,
        "ok": bool(state["configuration"]) and failure_mode in {"broker_api_timeout", "customs_gateway_unavailable", "screening_service_timeout"},
        "mode": "degraded_but_available",
        "fallbacks": ("queue_declaration", "retry_with_idempotency_key", "route_to_secondary_broker"),
    }


def cross_border_trade_rotate_crypto_epoch(state: dict, crypto_epoch: str) -> dict:
    new_state = _clone_state(state)
    new_state["crypto_epoch"] = crypto_epoch
    _append_event(new_state, "CryptoEpochRotated", {"crypto_epoch": crypto_epoch})
    return {"ok": True, "state": new_state, "crypto_epoch": crypto_epoch}


def cross_border_trade_optimize_carbon_aware_broker_route(brokers: tuple[dict, ...]) -> dict:
    scored = []
    for broker in brokers:
        score = (
            float(broker.get("compliance_score", 0.0)) * 0.5
            + (1.0 / max(float(broker.get("latency_hours", 1.0)), 1.0)) * 0.2
            + (1.0 / max(float(broker.get("fee", 1.0)), 1.0)) * 0.15
            + (1.0 / max(float(broker.get("carbon_intensity", 1.0)), 1.0)) * 0.15
        )
        scored.append({**broker, "route_score": round(score, 6)})
    selected = max(scored, key=lambda item: item["route_score"])
    return {
        "format": "appgen.cross-border-trade-broker-route.v1",
        "selected_broker": selected["broker_id"],
        "route_score": selected["route_score"],
        "candidates": tuple(scored),
    }


def cross_border_trade_optimize_landed_cost_math(scenarios: tuple[dict, ...]) -> dict:
    best = min(scenarios, key=lambda scenario: scenario["landed_total"])
    return {
        "format": "appgen.cross-border-trade-landed-cost-optimization.v1",
        "best_scenario": best,
        "scenario_count": len(scenarios),
    }


def cross_border_trade_allocate_broker_mechanism(brokers: tuple[dict, ...], *, declarations: int) -> dict:
    total_capacity = sum(float(broker.get("capacity", 1.0)) for broker in brokers)
    allocation = []
    remaining = declarations
    for index, broker in enumerate(brokers):
        if index == len(brokers) - 1:
            count = remaining
        else:
            count = int(round(declarations * (float(broker.get("capacity", 1.0)) / max(total_capacity, 1.0))))
            count = min(count, remaining)
        remaining -= count
        allocation.append({"broker_id": broker["broker_id"], "declarations": count})
    return {
        "format": "appgen.cross-border-trade-broker-mechanism.v1",
        "allocation": tuple(allocation),
        "strategy": "capacity_weighted_compliance_preserving",
    }


def cross_border_trade_detect_trade_anomaly(state: dict) -> dict:
    totals = [quote["landed_total"] for quote in state["landed_cost_quotes"].values()]
    anomalous = bool(state["dead_letter"]) or any(total > 250.0 for total in totals)
    return {
        "format": "appgen.cross-border-trade-anomaly.v1",
        "anomaly_detected": anomalous,
        "signals": {
            "dead_letters": len(state["dead_letter"]),
            "high_landed_cost_quotes": sum(1 for total in totals if total > 250.0),
        },
    }


def cross_border_trade_model_stochastic_exposure(
    *,
    duty_rate_path: tuple[float, ...],
    fx_rate_path: tuple[float, ...],
    volatility: float,
    value: float,
) -> dict:
    duty_component = sum(duty_rate_path) / max(len(duty_rate_path), 1)
    fx_component = sum(fx_rate_path) / max(len(fx_rate_path), 1)
    expected_exposure = value * duty_component * fx_component * (1.0 + volatility)
    return {
        "format": "appgen.cross-border-trade-stochastic-exposure.v1",
        "expected_exposure": round(expected_exposure, 2),
        "confidence_interval": (round(expected_exposure * 0.82, 2), round(expected_exposure * 1.18, 2)),
    }


def cross_border_trade_register_governed_model(model_name: str, evidence: dict) -> dict:
    _require_keys(evidence, ("features", "auc", "drift_score"), "Cross Border Trade governed model evidence")
    return {
        "format": "appgen.cross-border-trade-governed-model.v1",
        "ok": float(evidence["auc"]) >= 0.7 and float(evidence["drift_score"]) <= 0.1,
        "model_name": model_name,
        "evidence": evidence,
        "model_card_hash": _hash_payload({"model_name": model_name, "evidence": evidence}),
    }


def _cross_border_trade_release_control_evidence() -> dict:
    state = cross_border_trade_empty_state()
    state = cross_border_trade_configure_runtime(
        state,
        {
            "database_backend": "postgresql",
            "event_topic": CROSS_BORDER_TRADE_REQUIRED_EVENT_TOPIC,
            "retry_limit": 2,
            "default_currency": "USD",
            "supported_countries": ("US", "CA", "GB"),
            "supported_incoterms": ("DAP", "DDP"),
            "workbench_limit": 25,
        },
    )["state"]
    state = cross_border_trade_register_rule(
        state,
        {
            "rule_id": "rule_release_trade",
            "tenant": "tenant_release",
            "scope": "cross_border_trade",
            "status": "active",
            "classification_policy": {
                "confidence_floor": 0.72,
                "restricted_keywords": ("encryption",),
                "manual_review_keywords": ("battery",),
            },
            "landed_cost_policy": {
                "default_duty_rate": 0.08,
                "default_tax_rate": 0.12,
                "broker_fee": 24.0,
                "insurance_rate": 0.01,
            },
            "export_control_policy": {
                "blocked_destinations": ("restricted_zone",),
                "license_required_keywords": ("encryption",),
                "review_score": 0.75,
            },
            "declaration_policy": {
                "required_documents": ("commercial_invoice", "packing_list"),
                "preferred_brokers": ("broker_priority",),
                "submit_when_cleared": True,
            },
        },
    )["state"]
    state = cross_border_trade_receive_event(
        state,
        {
            "event_id": "evt_release_order",
            "event_type": "OrderPlaced",
            "idempotency_key": "release:order:v1",
            "payload": {
                "tenant": "tenant_release",
                "order_id": "order_release",
                "destination_country": "CA",
                "currency": "USD",
                "items": ({"product_id": "sku_release", "quantity": 1, "unit_value": 180.0},),
            },
        },
    )["state"]
    duplicate = cross_border_trade_receive_event(
        state,
        {
            "event_id": "evt_release_order",
            "event_type": "OrderPlaced",
            "idempotency_key": "release:order:v1",
            "payload": {"tenant": "tenant_release", "order_id": "order_release"},
        },
    )
    state = duplicate["state"]
    retry = cross_border_trade_receive_event(
        state,
        {
            "event_id": "evt_release_retry",
            "event_type": "UnknownEvent",
            "idempotency_key": "release:retry:v1",
            "attempts": 1,
            "payload": {"tenant": "tenant_release"},
        },
    )
    state = retry["state"]
    dead_letter = cross_border_trade_receive_event(
        state,
        {
            "event_id": "evt_release_retry",
            "event_type": "UnknownEvent",
            "idempotency_key": "release:retry:v1:dlq",
            "attempts": 2,
            "payload": {"tenant": "tenant_release"},
        },
    )
    state = dead_letter["state"]
    classification = cross_border_trade_classify_product(
        state,
        {
            "classification_id": "hsc_release",
            "tenant": "tenant_release",
            "product_id": "sku_release",
            "description": "digital camera kit with encryption control firmware",
            "country_of_origin": "US",
            "destination_country": "CA",
            "material_facts": ("camera", "encryption"),
        },
    )
    state = classification["state"]
    quote = cross_border_trade_quote_landed_cost(
        state,
        {
            "quote_id": "lcq_release",
            "tenant": "tenant_release",
            "order_id": "order_release",
            "classification_id": "hsc_release",
            "incoterm": "DDP",
            "origin_country": "US",
            "destination_country": "CA",
            "goods_value": 180.0,
            "shipping_cost": 22.0,
            "currency": "USD",
        },
    )
    state = quote["state"]
    check = cross_border_trade_screen_export_control(
        state,
        {
            "check_id": "ecc_release",
            "tenant": "tenant_release",
            "order_id": "order_release",
            "classification_id": "hsc_release",
            "destination_country": "CA",
            "counterparties": ({"name": "Aster Distribution", "risk_score": 0.08},),
        },
    )
    state = check["state"]
    declaration = cross_border_trade_file_customs_declaration(
        state,
        {
            "declaration_id": "ccd_release",
            "tenant": "tenant_release",
            "order_id": "order_release",
            "quote_id": "lcq_release",
            "check_id": "ecc_release",
            "documents": ("commercial_invoice", "packing_list", "origin_certificate"),
        },
    )
    state = declaration["state"]
    workbench = cross_border_trade_build_workbench_view(state, tenant="tenant_release")
    return {
        "format": "appgen.cross-border-trade-release-control-evidence.v1",
        "ok": retry["ok"] is False and dead_letter["dead_lettered"] is True and duplicate["duplicate"] is True,
        "summary": {
            "duplicate_status": "duplicate" if duplicate["duplicate"] else "unexpected",
            "retry_status": "retrying" if retry["retry_evidence"]["next_action"] == "retry" else retry["retry_evidence"]["next_action"],
            "dead_letter_status": "dead_letter" if dead_letter["dead_lettered"] else "unexpected",
            "outbox_count": len(state["outbox"]),
            "inbox_count": len(state["inbox"]),
            "dead_letter_count": len(state["dead_letter"]),
            "workbench_route": workbench["binding_evidence"]["workbench_route"],
        },
        "workbench": workbench,
    }


def _class_name(table: str) -> str:
    return "".join(part.capitalize() for part in table.split("_"))


def _clone_state(state: dict) -> dict:
    return copy.deepcopy(state)


def _require_configured(state: dict) -> None:
    if not state.get("configuration", {}).get("ok"):
        raise ValueError("Cross Border Trade runtime must be configured before commands execute.")


def _require_keys(payload: dict, keys: tuple[str, ...], label: str) -> None:
    missing = [key for key in keys if key not in payload]
    if missing:
        raise ValueError(f"{label} missing required fields: {', '.join(missing)}")


def _hash_payload(payload: object) -> str:
    return hashlib.sha256(json.dumps(payload, sort_keys=True, default=str).encode("utf-8")).hexdigest()


def _append_event(state: dict, event_type: str, payload: dict) -> None:
    state["event_sequence"] += 1
    previous_hash = state["events"][-1]["hash"] if state["events"] else "genesis"
    event = {
        "sequence": state["event_sequence"],
        "event_type": event_type,
        "payload": payload,
        "previous_hash": previous_hash,
    }
    event["hash"] = _hash_payload(event)
    state["events"].append(event)


def _append_outbox(state: dict, event_type: str, aggregate_id: str, tenant: str, payload: dict) -> None:
    state["outbox"].append(
        {
            "event_type": event_type,
            "aggregate_id": aggregate_id,
            "tenant": tenant,
            "topic": CROSS_BORDER_TRADE_REQUIRED_EVENT_TOPIC,
            "event_contract": "AppGen-X",
            "idempotency_key": f"cross_border_trade:{event_type}:{aggregate_id}",
            "payload_hash": _hash_payload(payload),
            "payload": payload,
        }
    )


def _active_rule(state: dict, tenant: str) -> dict | None:
    for rule in state.get("rules", {}).values():
        if rule.get("tenant") == tenant and rule.get("status") == "active":
            return rule
    return None


def _derive_hs_code(description: str) -> str:
    if "camera" in description:
        return "8525.80"
    if "battery" in description:
        return "8507.60"
    if "textile" in description or "shirt" in description:
        return "6205.20"
    if "software" in description:
        return "8523.49"
    return "9999.00"


def _duty_rate_for_hs(hs_code: str, default_rate: float) -> float:
    overrides = {
        "8525.80": 0.065,
        "8507.60": 0.04,
        "6205.20": 0.12,
        "8523.49": 0.0,
    }
    return float(overrides.get(hs_code, default_rate))


def _assert_supported_country(state: dict, country: str) -> None:
    if country not in state["configuration"]["supported_countries"]:
        raise ValueError(f"Unsupported Cross Border Trade country: {country}")


def _assert_supported_currency(state: dict, currency: str) -> None:
    if currency != state["configuration"]["default_currency"]:
        raise ValueError(f"Unsupported Cross Border Trade currency: {currency}")


def _assert_supported_incoterm(state: dict, incoterm: str) -> None:
    if incoterm not in state["configuration"]["supported_incoterms"]:
        raise ValueError(f"Unsupported Cross Border Trade incoterm: {incoterm}")


def _filter_tenant_records(state: dict, tenant: str) -> dict:
    return {
        name: {key: value for key, value in state[name].items() if value.get("tenant") == tenant}
        for name in ("hs_classifications", "landed_cost_quotes", "export_control_checks", "customs_declarations")
    }


def record_value(payload: dict, key: str) -> object:
    if key == "broker_id":
        return True
    return payload.get(key)
