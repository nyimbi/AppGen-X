PBC_MANIFEST = {'pbc': 'cross_border_trade', 'label': 'Cross-Border Trade and Customs Compliance', 'mesh': 'commerce', 'description': 'HS code assignment, landed cost, export controls, and customs declarations.', 'datastore_backend': 'postgresql', 'tables': ('hs_classification', 'landed_cost_quote', 'export_control_check', 'customs_declaration'), 'apis': ('POST /landed-cost', 'POST /export-checks', 'POST /declarations', 'GET /cross-border-trade-workbench'), 'emits': ('CustomsDeclarationPrepared', 'LandedCostCalculated'), 'consumes': ('ProductClassified', 'OrderPriced'), 'template': None, 'ui_fragments': ('CrossBorderTradeWorkbench', 'CrossBorderTradeDetail'), 'permissions': ('cross_border_trade.read', 'cross_border_trade.create', 'cross_border_trade.update', 'cross_border_trade.approve', 'cross_border_trade.admin'), 'configuration': ('CROSS_BORDER_TRADE_DATABASE_URL', 'CROSS_BORDER_TRADE_EVENT_TOPIC', 'CROSS_BORDER_TRADE_RETRY_LIMIT'), 'capabilities': ('cross_border_trade.hs_classification', 'cross_border_trade.landed_cost_quote', 'cross_border_trade.export_control_check', 'cross_border_trade.customs_declaration'), 'standard_features': ('hs_classification', 'landed_cost_quote', 'export_control_check', 'customs_declaration', 'country_of_origin', 'duty_tax_fee_calculation', 'restricted_party_and_sanctions_screening', 'license_requirement_detection', 'incoterm_support', 'broker_submission_handoff', 'trade_document_evidence', 'order_inventory_payment_logistics_handoffs', 'tenant_isolation', 'appgen_x_outbox_inbox_eventing', 'idempotent_handlers', 'retry_dead_letter_evidence', 'permissions', 'configuration_schema', 'rule_engine', 'parameter_engine', 'seed_data', 'workbench', 'immutable_audit', 'governed_model_evidence', 'denied_party_screening', 'customs_documents', 'duties_taxes', 'broker_carrier_handoffs', 'country_restrictions', 'compliance_holds', 'declarations', 'audit_evidence'), 'workflows': ('command_landed_cost', 'command_export_checks', 'command_declarations', 'query_cross_border_trade_workbench'), 'analytics': ('authorization_rate', 'route_margin', 'return_cycle_time', 'landed_cost_accuracy', 'customs_declaration_prepared_throughput', 'landed_cost_calculated_throughput'), 'advanced_capabilities': ('event_sourced_trade_lifecycle', 'owned_trade_schema_boundary', 'graph_relational_trade_topology', 'multi_tenant_trade_isolation', 'schema_evolution_resilient_trade_schema', 'probabilistic_hs_classification_scoring', 'counterfactual_landed_cost_simulation', 'temporal_duty_tax_exposure_forecasting', 'autonomous_trade_exception_resolution', 'semantic_trade_document_understanding', 'predictive_export_control_risk', 'self_healing_customs_broker_route_selection', 'cryptographic_trade_proof', 'immutable_trade_audit_trail', 'dynamic_trade_policy_screening', 'automated_trade_control_testing', 'cross_system_order_inventory_payment_logistics_federation', 'appgen_x_outbox_inbox_eventing', 'idempotent_inbox_handlers', 'retry_dead_letter_evidence', 'tenant_isolation', 'chaos_tolerant_trade_operations', 'crypto_agility', 'carbon_aware_trade_route_selection', 'mathematical_landed_cost_optimization', 'broker_allocation_mechanism_design', 'trade_anomaly_detection', 'stochastic_trade_exposure_modeling', 'governed_ml_model_evidence', 'permissions_governance_evidence', 'universal_api_async_streaming', 'configuration_schema', 'parameter_engine', 'rule_engine', 'seed_data', 'workbench_ui'), 'migrations': ('migrations/001_initial.sql',), 'seed_data': ('seed_data.py',), 'tests': ('tests/test_contract.py',), 'docs': ('RELEASE_EVIDENCE.md',)}

PBC_MANIFEST = {
    **PBC_MANIFEST,
    'tables': PBC_MANIFEST['tables']
    + (
        'denied_party_screening',
        'trade_document_packet',
        'broker_handoff',
        'carrier_handoff',
        'trade_compliance_hold',
        'country_restriction_policy',
        'trade_audit_evidence',
    ),
    'apis': PBC_MANIFEST['apis']
    + (
        'POST /denied-party-screenings',
        'POST /document-packets',
        'POST /broker-handoffs',
        'POST /carrier-handoffs',
        'POST /compliance-holds',
        'POST /compliance-holds/resolve',
        'POST /country-restriction-policies',
        'POST /declaration-releases',
    ),
    'emits': PBC_MANIFEST['emits']
    + (
        'DeniedPartyScreened',
        'TradeDocumentPacketPrepared',
        'BrokerHandoffQueued',
        'CarrierHandoffPrepared',
        'TradeComplianceHoldOpened',
        'TradeComplianceHoldResolved',
        'CountryRestrictionPolicyRegistered',
        'CustomsDeclarationReleased',
    ),
    'capabilities': PBC_MANIFEST['capabilities']
    + (
        'cross_border_trade.denied_party_screening',
        'cross_border_trade.trade_document_packet',
        'cross_border_trade.broker_handoff',
        'cross_border_trade.carrier_handoff',
        'cross_border_trade.compliance_hold',
        'cross_border_trade.country_restriction_policy',
        'cross_border_trade.customs_release',
    ),
    'standard_features': PBC_MANIFEST['standard_features']
    + (
        'customs_release',
        'broker_status_tracking',
        'carrier_status_tracking',
        'document_packet_lifecycle',
        'denied_party_case_management',
    ),
    'workflows': PBC_MANIFEST['workflows']
    + (
        'command_denied_party_screenings',
        'command_document_packets',
        'command_broker_handoffs',
        'command_carrier_handoffs',
        'command_compliance_holds',
        'command_hold_resolutions',
        'command_country_restrictions',
        'command_declaration_releases',
    ),
}
