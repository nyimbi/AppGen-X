"""Packaged Business Capability catalog and composition contracts.

Composable enterprise apps are assembled from independently owned business
capabilities instead of one large shared module.  This module keeps that
catalog executable: every entry declares its datastore boundary, API surface,
event contracts, generated tables, and dependency evidence.
"""

from __future__ import annotations

import contextlib
import importlib
import importlib.util
import json
import py_compile
import re
import sys
import tempfile
from datetime import date, datetime, timezone
from functools import lru_cache
from pathlib import Path

from . import pbc_schema


_MUTATING_CRUD_ACTIONS = frozenset({"create", "update", "delete"})


PBC_MANIFEST_REQUIRED_FIELDS = (
    "pbc",
    "label",
    "mesh",
    "description",
    "datastore_backend",
    "tables",
    "apis",
    "emits",
    "consumes",
)
PBC_MANIFEST_OPTIONAL_FIELDS = (
    "template",
    "owner",
    "version",
    "stream_processor",
    "stream_exception_evidence",
    "ui_fragments",
    "permissions",
    "configuration",
    "migrations",
    "seed_data",
    "tests",
    "docs",
    "capabilities",
    "standard_features",
    "advanced_capabilities",
    "workflows",
    "analytics",
)
PBC_IMPLEMENTATION_REQUIRED_ARTIFACTS = (
    "__init__.py",
    "manifest.py",
    "models.py",
    "services.py",
    "routes.py",
    "events.py",
    "handlers.py",
    "schema_contract.py",
    "service_contract.py",
    "release_evidence.py",
    "ui.py",
    "permissions.py",
    "config.py",
    "seed_data.py",
    "migrations/001_initial.sql",
    "agent.py",
    "tests/__init__.py",
    "tests/test_contract.py",
    "RELEASE_EVIDENCE.md",
)
PBC_SOURCE_PACKAGE_REQUIRED_ARTIFACTS = (
    *PBC_IMPLEMENTATION_REQUIRED_ARTIFACTS,
    "capability_assurance.py",
)
PBC_DOMAIN_DEPTH_REQUIRED_DIMENSIONS = (
    "capability_modules",
    "workflow_implementations",
    "policy_controls",
    "automation_loops",
    "analytics",
    "integration_contracts",
    "workbench_actions",
    "release_gates",
)
PBC_DOMAIN_DEPTH_LEVEL = "enterprise_suite_displacement"
PBC_SPECIFICATION_MIN_WORDS = 650
PBC_SPECIFICATION_REQUIRED_CONCEPTS = (
    {
        "id": "stable_identity",
        "terms": (("pbc",),),
    },
    {
        "id": "owned_boundary",
        "terms": (("owned",), ("table",), ("shared", "foreign")),
    },
    {
        "id": "schema_generation",
        "terms": (("schema",), ("migration",), ("model",)),
    },
    {
        "id": "service_api_contract",
        "terms": (("service",), ("api", "route"), ("command", "query")),
    },
    {
        "id": "events_handlers",
        "terms": (("event",), ("outbox",), ("inbox",), ("dead-letter",), ("idempot",), ("retry",)),
    },
    {
        "id": "ui_permissions",
        "terms": (("ui",), ("workbench",), ("permission", "rbac")),
    },
    {
        "id": "rules_parameters_configuration",
        "terms": (("rule",), ("parameter",), ("configuration",)),
    },
    {
        "id": "agent_chatbot_skills",
        "terms": (("agent", "assistant", "chatbot"), ("skill",), ("document", "instruction"), ("crud", "datastore", "mutation")),
    },
    {
        "id": "side_effect_free_self_registration",
        "terms": (("registration", "register"), ("side-effect-free", "side effect free", "discovery")),
    },
    {
        "id": "standard_and_advanced_capabilities",
        "terms": (("standard",), ("advanced",)),
    },
    {
        "id": "package_release_evidence",
        "terms": (("release",), ("test",), ("seed",)),
    },
    {
        "id": "datastore_and_event_policy",
        "terms": (("postgresql",), ("mysql",), ("mariadb",), ("appgen-x",)),
    },
)
PBC_SPECIFICATION_TRACEABILITY_FIELDS = (
    "tables",
    "apis",
    "emits",
    "consumes",
    "ui_fragments",
    "permissions",
    "configuration",
    "standard_features",
    "advanced_capabilities",
)
PBC_RESTRICTED_LEGACY_REFERENCES = (
    r"\b" + "S" + "AP" + r"\b",
    r"\b" + "S" + r"/4\b",
    r"\b" + "S" + "4" + r"\b",
    r"\b" + "Sales" + "force" + r"\b",
    r"\b" + "Quick" + "Books" + r"\b",
)
PBC_TABLE_STAKES_REQUIRED_EVIDENCE = (
    "owned_schema_migrations_models",
    "service_api_route_contracts",
    "appgen_event_contract",
    "idempotent_handlers",
    "retry_dead_letter_policy",
    "ui_workbench",
    "permissions_rbac",
    "configuration_schema",
    "rule_engine",
    "parameter_engine",
    "seed_data",
)
PBC_ADVANCED_RUNTIME_REQUIRED_OPERATION_GROUPS = (
    ("configure_runtime",),
    ("set_parameter",),
    ("register_rule",),
    ("receive_event", "handle_event", "ingest_event"),
    ("build_workbench_view",),
    ("build_schema_contract",),
    ("build_service_contract",),
    ("build_release_evidence",),
)
PBC_LIFECYCLE_DOCUMENTATION_FILES = (
    "README.md",
    "docs/pbc-specification.md",
    "docs/composable-pbc-apps.md",
    "docs/kafka-alternatives.md",
)
PBC_LIFECYCLE_DOCUMENTATION_TOPICS = (
    "build",
    "test",
    "package",
    "register",
    "compose",
)
PBC_LIFECYCLE_DOCUMENTATION_APIS = (
    "pbc_manifest_schema",
    "validate_pbc_manifest",
    "register_pbc_manifest",
    "pbc_package_contract",
    "load_pbc_package",
    "discover_pbc_packages",
    "pbc_package_index_schema",
    "discover_pbc_package_index",
    "pbc_selection_from_prompt",
    "pbc_composition_plan",
    "pbc_composition_dsl",
    "pbc_generation_smoke_audit",
    "pbc_release_audit",
)
PBC_LIFECYCLE_DOCUMENTATION_ARTIFACTS = (
    "SPECIFICATION.md",
    "manifest.py",
    "models.py",
    "services.py",
    "routes.py",
    "events.py",
    "handlers.py",
    "schema_contract.py",
    "service_contract.py",
    "release_evidence.py",
    "ui.py",
    "permissions.py",
    "config.py",
    "seed_data.py",
    "migrations/001_initial.sql",
    "tests/test_contract.py",
    "RELEASE_EVIDENCE.md",
)
PBC_SOURCE_RUNTIME_TEST_REQUIRED_CONCEPTS = (
    {
        "id": "runtime_capabilities",
        "terms": (("runtime_capabilities",),),
    },
    {
        "id": "runtime_smoke",
        "terms": (("runtime_smoke",),),
    },
    {
        "id": "schema_service_release_contracts",
        "terms": (("build_schema_contract",), ("build_service_contract",), ("build_release_evidence",)),
    },
    {
        "id": "implementation_contract",
        "terms": (("implementation_contract",),),
    },
    {
        "id": "event_handling",
        "terms": (("receive_event", "handle_event", "ingest_event"),),
    },
    {
        "id": "ui_workbench",
        "terms": (("workbench", "ui_contract"),),
    },
    {
        "id": "boundary_validation",
        "terms": (("verify_owned_table_boundary", "foreign"),),
    },
    {
        "id": "configuration_rules_parameters",
        "terms": (("configure_runtime",), ("set_parameter",), ("register_rule",)),
    },
)
PBC_ADVANCED_DOMAIN_REQUIRED_AREAS = (
    "foundational_architecture",
    "computational_analytics",
    "intelligence_automation",
    "compliance_governance",
    "integration_ecosystem",
    "operational_resilience",
    "theoretical_constructs",
    "implementation_prerequisites",
)
GL_CORE_ADVANCED_CAPABILITY_KEYS = (
    "event_sourced_ledger_core",
    "distributed_consensus_protocol",
    "schema_on_read_extensibility",
    "multi_tenant_isolation",
    "real_time_olap_oltp_convergence",
    "probabilistic_accounting_primitives",
    "continuous_close_architecture",
    "causal_inference_engine",
    "autonomous_reconciliation",
    "semantic_transaction_understanding",
    "regulatory_logic_compilation",
    "predictive_posting_validation",
    "zero_knowledge_audit_proofs",
    "dynamic_policy_enforcement",
    "immutable_regulatory_trail",
    "automated_control_testing",
    "universal_api_contract",
    "cross_system_ledger_federation",
    "event_driven_subledger_synchronization",
    "decentralized_identity_integration",
    "chaos_engineered_fault_tolerance",
    "quantum_resistant_cryptography",
    "carbon_aware_processing",
    "temporal_accounting_algebra",
    "homomorphic_encryption_for_consolidation",
    "game_theoretic_reconciliation",
    "information_theoretic_auditability",
    "formal_methods_ledger_invariants",
    "distributed_systems_runtime",
    "cryptographic_engineering",
    "financial_mlops",
)
AP_AUTOMATION_ADVANCED_CAPABILITY_KEYS = (
    "event_sourced_invoice_lifecycle",
    "graph_relational_vendor_data_model",
    "multi_tenant_liquidity_isolation",
    "schema_evolution_resilient_invoice_schema",
    "probabilistic_three_way_matching",
    "real_time_liquidity_aware_payment_scheduling",
    "counterfactual_discount_analysis",
    "temporal_cash_flow_forecasting",
    "autonomous_exception_resolution",
    "semantic_contract_to_invoice_alignment",
    "predictive_vendor_risk_scoring",
    "self_healing_payment_routing",
    "zero_knowledge_tax_validation",
    "immutable_regulatory_e_invoicing",
    "dynamic_sanction_aml_screening",
    "automated_control_testing",
    "universal_api_async_streaming",
    "cross_border_payment_federation",
    "supply_chain_finance_network_integration",
    "decentralized_vendor_identity",
    "chaos_engineered_payment_rail_tolerance",
    "quantum_resistant_payment_authentication",
    "carbon_aware_settlement_scheduling",
    "algebraic_payment_routing_optimization",
    "mechanism_design_dynamic_discounting",
    "information_theoretic_fraud_detection",
    "temporal_liquidity_forecasting_construct",
    "distributed_systems_engineering",
    "probabilistic_ml_vendor_risk",
    "cryptographic_engineering",
    "mathematical_optimization",
    "financial_mlops_governance",
)
AR_CREDIT_ADVANCED_CAPABILITY_KEYS = (
    "event_sourced_receivable_lifecycle",
    "graph_relational_customer_topology",
    "multi_tenant_cash_application_isolation",
    "schema_evolution_resilient_receivable_schema",
    "probabilistic_cash_application",
    "real_time_liquidity_aware_credit_extension",
    "counterfactual_collection_strategy_optimization",
    "temporal_revenue_to_cash_forecasting",
    "autonomous_dispute_resolution",
    "semantic_remittance_parsing",
    "predictive_customer_default_scoring",
    "self_healing_collection_routing",
    "zero_knowledge_revenue_verification",
    "immutable_e_invoicing_tax_audit",
    "dynamic_sanction_fraud_screening",
    "automated_control_testing",
    "universal_api_async_streaming",
    "cross_border_receivable_federation",
    "supply_chain_finance_network_integration",
    "decentralized_customer_identity",
    "chaos_engineered_payment_rail_tolerance",
    "quantum_resistant_payment_authentication",
    "carbon_aware_collection_scheduling",
    "algebraic_collection_optimization",
    "mechanism_design_payment_term_negotiation",
    "information_theoretic_cash_application_anomaly_detection",
    "temporal_receivable_stochastic_modeling",
    "distributed_systems_engineering",
    "probabilistic_ml_customer_risk",
    "cryptographic_engineering",
    "mathematical_optimization",
    "financial_mlops_governance",
)
TREASURY_CASH_ADVANCED_CAPABILITY_KEYS = (
    "event_sourced_cash_lifecycle",
    "graph_relational_bank_topology",
    "multi_tenant_liquidity_isolation",
    "schema_evolution_resilient_cash_schema",
    "probabilistic_cash_forecasting",
    "real_time_liquidity_optimization",
    "counterfactual_funding_analysis",
    "temporal_cash_flow_stochastic_modeling",
    "autonomous_bank_reconciliation",
    "semantic_bank_narrative_parsing",
    "predictive_counterparty_liquidity_risk",
    "self_healing_payment_rail_routing",
    "zero_knowledge_liquidity_covenant_proof",
    "immutable_bank_connectivity_audit",
    "dynamic_sanction_fraud_screening",
    "automated_treasury_control_testing",
    "universal_api_async_streaming",
    "cross_border_liquidity_federation",
    "working_capital_finance_integration",
    "decentralized_counterparty_identity",
    "chaos_engineered_bank_rail_tolerance",
    "quantum_resistant_treasury_authentication",
    "carbon_aware_liquidity_scheduling",
    "algebraic_liquidity_optimization",
    "mechanism_design_funding_allocation",
    "information_theoretic_cash_anomaly_detection",
    "temporal_liquidity_forecasting_construct",
    "distributed_systems_engineering",
    "probabilistic_ml_liquidity_risk",
    "cryptographic_engineering",
    "mathematical_optimization",
    "financial_mlops_governance",
)
ASSET_LIFECYCLE_ADVANCED_CAPABILITY_KEYS = (
    "event_sourced_asset_lifecycle",
    "graph_relational_asset_topology",
    "multi_tenant_asset_book_isolation",
    "schema_evolution_resilient_asset_schema",
    "probabilistic_useful_life_estimation",
    "real_time_depreciation_valuation_projection",
    "counterfactual_lifecycle_optimization",
    "temporal_asset_value_risk_forecasting",
    "autonomous_impairment_revaluation",
    "semantic_capitalization_parsing",
    "predictive_maintenance_asset_risk",
    "self_healing_depreciation_journal_routing",
    "zero_knowledge_asset_audit_proof",
    "immutable_asset_regulatory_trail",
    "dynamic_policy_compliance_screening",
    "automated_fixed_asset_control_testing",
    "universal_api_async_streaming",
    "cross_system_asset_federation",
    "insurance_warranty_network_integration",
    "decentralized_asset_identity",
    "chaos_engineered_depreciation_tolerance",
    "quantum_resistant_asset_authorization",
    "carbon_aware_asset_scheduling",
    "algebraic_asset_portfolio_optimization",
    "mechanism_design_asset_allocation",
    "information_theoretic_asset_anomaly_detection",
    "temporal_asset_valuation_stochastic_modeling",
    "distributed_systems_engineering",
    "probabilistic_ml_asset_risk",
    "cryptographic_engineering",
    "mathematical_optimization",
    "financial_mlops_governance",
)
TAX_LOCALIZATION_ADVANCED_CAPABILITY_KEYS = (
    "event_sourced_tax_lifecycle",
    "graph_relational_jurisdiction_topology",
    "multi_tenant_compliance_isolation",
    "schema_evolution_resilient_tax_schema",
    "probabilistic_taxability_classification",
    "real_time_tax_quote_convergence",
    "counterfactual_tax_policy_simulation",
    "temporal_tax_liability_forecasting",
    "autonomous_filing_reconciliation",
    "semantic_tax_document_parsing",
    "predictive_jurisdiction_risk_scoring",
    "self_healing_filing_route_selection",
    "zero_knowledge_tax_audit_proof",
    "immutable_regulatory_trail",
    "dynamic_tax_policy_screening",
    "automated_tax_control_testing",
    "universal_api_async_streaming",
    "cross_border_tax_federation",
    "digital_document_network_integration",
    "decentralized_tax_identity",
    "chaos_engineered_authority_tolerance",
    "quantum_resistant_tax_authorization",
    "carbon_aware_filing_scheduling",
    "algebraic_tax_remittance_optimization",
    "mechanism_design_tax_allocation",
    "information_theoretic_tax_anomaly_detection",
    "temporal_tax_exposure_stochastic_modeling",
    "distributed_systems_engineering",
    "probabilistic_ml_tax_risk",
    "cryptographic_engineering",
    "mathematical_optimization",
    "tax_mlops_governance",
)
INVENTORY_POSITIONING_ADVANCED_CAPABILITY_KEYS = (
    "event_sourced_inventory_lifecycle",
    "graph_relational_inventory_topology",
    "multi_tenant_stock_isolation",
    "schema_evolution_resilient_inventory_schema",
    "probabilistic_availability_projection",
    "real_time_atp_ctp_convergence",
    "counterfactual_allocation_policy_simulation",
    "temporal_demand_stockout_forecasting",
    "autonomous_inventory_reconciliation",
    "semantic_inventory_event_parsing",
    "predictive_stockout_spoilage_risk",
    "self_healing_allocation_route_selection",
    "zero_knowledge_stock_proof",
    "immutable_inventory_traceability_trail",
    "dynamic_inventory_policy_screening",
    "automated_inventory_control_testing",
    "universal_api_async_streaming",
    "cross_node_inventory_federation",
    "warehouse_order_quality_integration",
    "decentralized_node_lot_identity",
    "chaos_engineered_node_tolerance",
    "quantum_resistant_inventory_authorization",
    "carbon_aware_fulfillment_scheduling",
    "algebraic_allocation_optimization",
    "mechanism_design_channel_allocation",
    "information_theoretic_inventory_anomaly_detection",
    "temporal_stock_exposure_stochastic_modeling",
    "distributed_systems_engineering",
    "probabilistic_ml_stock_risk",
    "cryptographic_engineering",
    "mathematical_optimization",
    "inventory_mlops_governance",
)
WMS_CORE_ADVANCED_CAPABILITY_KEYS = (
    "event_sourced_warehouse_lifecycle",
    "graph_relational_warehouse_topology",
    "multi_tenant_warehouse_isolation",
    "schema_evolution_resilient_warehouse_schema",
    "probabilistic_putaway_pick_estimation",
    "real_time_warehouse_execution_analytics",
    "counterfactual_wave_labor_simulation",
    "temporal_throughput_dock_forecasting",
    "autonomous_exception_resolution",
    "semantic_warehouse_event_parsing",
    "predictive_congestion_damage_risk",
    "self_healing_edge_route_selection",
    "zero_knowledge_shipment_proof",
    "immutable_warehouse_traceability_trail",
    "dynamic_warehouse_policy_screening",
    "automated_warehouse_control_testing",
    "universal_api_async_streaming",
    "cross_system_warehouse_federation",
    "edge_device_network_integration",
    "decentralized_warehouse_identity",
    "chaos_engineered_edge_tolerance",
    "quantum_resistant_warehouse_authorization",
    "carbon_aware_wave_scheduling",
    "algebraic_pick_path_optimization",
    "mechanism_design_labor_allocation",
    "information_theoretic_warehouse_anomaly_detection",
    "temporal_throughput_stochastic_modeling",
    "distributed_systems_engineering",
    "probabilistic_ml_warehouse_risk",
    "cryptographic_engineering",
    "mathematical_optimization",
    "warehouse_mlops_governance",
)
PROCUREMENT_SOURCING_ADVANCED_CAPABILITY_KEYS = (
    "event_sourced_source_to_order_lifecycle",
    "graph_relational_supplier_topology",
    "multi_tenant_procurement_isolation",
    "schema_evolution_resilient_procurement_schema",
    "probabilistic_supplier_award_confidence",
    "real_time_sourcing_spend_analytics",
    "counterfactual_sourcing_strategy_simulation",
    "temporal_price_lead_time_forecasting",
    "autonomous_supplier_selection",
    "semantic_procurement_document_parsing",
    "predictive_supplier_disruption_risk",
    "self_healing_po_route_selection",
    "zero_knowledge_supplier_compliance_proof",
    "immutable_procurement_audit_trail",
    "dynamic_procurement_policy_screening",
    "automated_procurement_control_testing",
    "universal_api_async_streaming",
    "cross_system_procurement_federation",
    "supplier_network_integration",
    "decentralized_supplier_identity",
    "chaos_engineered_supplier_route_tolerance",
    "quantum_resistant_procurement_authorization",
    "carbon_aware_sourcing_selection",
    "algebraic_sourcing_award_optimization",
    "mechanism_design_rfq_allocation",
    "information_theoretic_bid_anomaly_detection",
    "temporal_supply_exposure_stochastic_modeling",
    "distributed_systems_engineering",
    "probabilistic_ml_supplier_risk",
    "cryptographic_engineering",
    "mathematical_optimization",
    "procurement_mlops_governance",
)
TRANSPORTATION_MANAGEMENT_ADVANCED_CAPABILITY_KEYS = (
    "event_sourced_shipment_lifecycle",
    "graph_relational_freight_topology",
    "multi_tenant_transportation_isolation",
    "schema_evolution_resilient_transportation_schema",
    "probabilistic_eta_delivery_confidence",
    "real_time_freight_execution_analytics",
    "counterfactual_carrier_route_simulation",
    "temporal_eta_cost_delay_forecasting",
    "autonomous_transport_exception_resolution",
    "semantic_transport_event_parsing",
    "predictive_delay_damage_carrier_risk",
    "self_healing_carrier_telematics_route_selection",
    "zero_knowledge_delivery_proof",
    "immutable_transportation_traceability_trail",
    "dynamic_transportation_policy_screening",
    "automated_transportation_control_testing",
    "universal_api_async_streaming",
    "cross_system_transportation_federation",
    "carrier_network_telematics_integration",
    "decentralized_carrier_identity",
    "chaos_engineered_carrier_telematics_tolerance",
    "quantum_resistant_transportation_authorization",
    "carbon_aware_carrier_route_selection",
    "algebraic_route_carrier_optimization",
    "mechanism_design_carrier_tender_allocation",
    "information_theoretic_tracking_anomaly_detection",
    "temporal_transit_exposure_stochastic_modeling",
    "distributed_systems_engineering",
    "probabilistic_ml_transportation_risk",
    "cryptographic_engineering",
    "mathematical_optimization",
    "transportation_mlops_governance",
)
DOM_ADVANCED_CAPABILITY_KEYS = (
    "event_sourced_order_lifecycle",
    "graph_relational_order_topology",
    "multi_tenant_order_isolation",
    "schema_evolution_resilient_order_schema",
    "probabilistic_fraud_allocation_confidence",
    "real_time_order_orchestration_analytics",
    "counterfactual_sourcing_fulfillment_simulation",
    "temporal_promise_demand_forecasting",
    "autonomous_order_exception_resolution",
    "semantic_order_event_parsing",
    "predictive_cancellation_fulfillment_risk",
    "self_healing_fulfillment_route_selection",
    "zero_knowledge_order_verification_proof",
    "immutable_order_audit_trail",
    "dynamic_order_policy_screening",
    "automated_order_control_testing",
    "universal_api_async_streaming",
    "cross_system_order_federation",
    "commerce_service_channel_integration",
    "decentralized_order_identity",
    "chaos_engineered_orchestration_tolerance",
    "quantum_resistant_order_authorization",
    "carbon_aware_fulfillment_planning",
    "algebraic_fulfillment_optimization",
    "mechanism_design_node_allocation",
    "information_theoretic_order_anomaly_detection",
    "temporal_fulfillment_exposure_stochastic_modeling",
    "distributed_systems_engineering",
    "probabilistic_ml_order_risk",
    "cryptographic_engineering",
    "mathematical_optimization",
    "order_mlops_governance",
)
PERSONNEL_IDENTITY_ADVANCED_CAPABILITY_KEYS = (
    "event_sourced_workforce_identity_lifecycle",
    "graph_relational_org_identity_topology",
    "multi_tenant_workforce_identity_isolation",
    "schema_evolution_resilient_identity_schema",
    "probabilistic_identity_assurance_access_risk",
    "real_time_directory_org_access_analytics",
    "counterfactual_org_access_policy_simulation",
    "temporal_workforce_access_risk_forecasting",
    "autonomous_role_access_exception_recommendations",
    "semantic_personnel_event_parsing",
    "predictive_attrition_access_compliance_risk",
    "self_healing_provisioning_route_selection",
    "zero_knowledge_personnel_eligibility_proof",
    "immutable_workforce_identity_audit_trail",
    "dynamic_personnel_policy_screening",
    "automated_identity_control_testing",
    "universal_api_async_streaming",
    "cross_system_people_federation",
    "identity_provider_directory_integration",
    "decentralized_employee_identity",
    "chaos_engineered_provisioning_tolerance",
    "quantum_resistant_identity_authorization",
    "carbon_aware_identity_processing",
    "algebraic_role_access_optimization",
    "mechanism_design_manager_role_allocation",
    "information_theoretic_identity_anomaly_detection",
    "temporal_workforce_risk_stochastic_modeling",
    "distributed_systems_engineering",
    "probabilistic_ml_workforce_risk",
    "cryptographic_engineering",
    "mathematical_optimization",
    "people_mlops_governance",
)
TIME_LABOR_ADVANCED_CAPABILITY_KEYS = (
    "event_sourced_labor_lifecycle",
    "graph_relational_labor_topology",
    "multi_tenant_time_isolation",
    "schema_evolution_resilient_time_schema",
    "probabilistic_time_fraud_exception_scoring",
    "real_time_labor_execution_analytics",
    "counterfactual_schedule_overtime_simulation",
    "temporal_labor_demand_overtime_forecasting",
    "autonomous_time_exception_resolution",
    "semantic_clock_absence_event_parsing",
    "predictive_burnout_absence_compliance_risk",
    "self_healing_clock_source_route_selection",
    "zero_knowledge_payroll_ready_hours_proof",
    "immutable_labor_audit_trail",
    "dynamic_labor_policy_screening",
    "automated_time_control_testing",
    "universal_api_async_streaming",
    "cross_system_labor_federation",
    "workforce_device_integration",
    "decentralized_employee_time_identity",
    "chaos_engineered_clock_approval_tolerance",
    "quantum_resistant_time_authorization",
    "carbon_aware_schedule_planning",
    "algebraic_schedule_labor_optimization",
    "mechanism_design_shift_allocation",
    "information_theoretic_time_anomaly_detection",
    "temporal_labor_exposure_stochastic_modeling",
    "distributed_systems_engineering",
    "probabilistic_ml_labor_risk",
    "cryptographic_engineering",
    "mathematical_optimization",
    "labor_mlops_governance",
)
PAYROLL_ENGINE_ADVANCED_CAPABILITY_KEYS = (
    "event_sourced_payroll_lifecycle",
    "graph_relational_compensation_topology",
    "multi_tenant_payroll_isolation",
    "schema_evolution_resilient_payroll_schema",
    "probabilistic_payroll_anomaly_compliance_scoring",
    "real_time_gross_to_net_analytics",
    "counterfactual_pay_policy_simulation",
    "temporal_payroll_cash_forecasting",
    "autonomous_payroll_exception_resolution",
    "semantic_payroll_instruction_parsing",
    "predictive_payroll_compliance_liquidity_risk",
    "self_healing_payment_filing_route_selection",
    "zero_knowledge_net_pay_filing_proof",
    "immutable_payroll_audit_trail",
    "dynamic_payroll_policy_screening",
    "automated_payroll_control_testing",
    "universal_api_async_streaming",
    "cross_system_payroll_federation",
    "treasury_tax_ledger_integration",
    "decentralized_worker_pay_identity",
    "chaos_engineered_payroll_tolerance",
    "quantum_resistant_payroll_authorization",
    "carbon_aware_payroll_batching",
    "algebraic_payroll_batch_optimization",
    "mechanism_design_cash_allocation",
    "information_theoretic_payroll_anomaly_detection",
    "temporal_payroll_exposure_stochastic_modeling",
    "distributed_systems_engineering",
    "probabilistic_ml_payroll_risk",
    "cryptographic_engineering",
    "mathematical_optimization",
    "payroll_mlops_governance",
)
TALENT_ONBOARDING_ADVANCED_CAPABILITY_KEYS = (
    "event_sourced_talent_lifecycle",
    "graph_relational_hiring_topology",
    "multi_tenant_talent_isolation",
    "schema_evolution_resilient_talent_schema",
    "probabilistic_candidate_match_compliance_scoring",
    "real_time_pipeline_onboarding_analytics",
    "counterfactual_hiring_policy_simulation",
    "temporal_hiring_demand_cycle_forecasting",
    "autonomous_candidate_exception_resolution",
    "semantic_candidate_instruction_parsing",
    "predictive_candidate_attrition_compliance_risk",
    "self_healing_screening_provisioning_route_selection",
    "zero_knowledge_candidate_eligibility_proof",
    "immutable_talent_audit_trail",
    "dynamic_talent_policy_screening",
    "automated_talent_control_testing",
    "universal_api_async_streaming",
    "cross_system_talent_federation",
    "identity_access_notification_integration",
    "decentralized_candidate_identity",
    "chaos_engineered_onboarding_tolerance",
    "quantum_resistant_candidate_authorization",
    "carbon_aware_interview_onboarding_scheduling",
    "algebraic_pipeline_optimization",
    "mechanism_design_interview_allocation",
    "information_theoretic_hiring_anomaly_detection",
    "temporal_hiring_exposure_stochastic_modeling",
    "distributed_systems_engineering",
    "probabilistic_ml_candidate_risk",
    "cryptographic_engineering",
    "mathematical_optimization",
    "talent_mlops_governance",
)
MRP_ENGINE_ADVANCED_CAPABILITY_KEYS = (
    "event_sourced_planning_lifecycle",
    "graph_relational_bom_topology",
    "multi_tenant_site_planning_isolation",
    "schema_evolution_resilient_planning_schema",
    "probabilistic_shortage_capacity_risk_scoring",
    "real_time_material_plan_analytics",
    "counterfactual_planning_policy_simulation",
    "temporal_demand_shortage_forecasting",
    "autonomous_planning_exception_resolution",
    "semantic_demand_bom_instruction_parsing",
    "predictive_material_capacity_compliance_risk",
    "self_healing_supply_route_selection",
    "zero_knowledge_supply_availability_proof",
    "immutable_planning_audit_trail",
    "dynamic_mrp_policy_screening",
    "automated_mrp_control_testing",
    "universal_api_async_streaming",
    "cross_system_mrp_federation",
    "inventory_order_forecast_integration",
    "decentralized_item_source_identity",
    "chaos_engineered_planning_tolerance",
    "quantum_resistant_planning_authorization",
    "carbon_aware_planning_batching",
    "algebraic_material_allocation_optimization",
    "mechanism_design_capacity_allocation",
    "information_theoretic_shortage_anomaly_detection",
    "temporal_material_exposure_stochastic_modeling",
    "distributed_systems_engineering",
    "probabilistic_ml_shortage_risk",
    "cryptographic_engineering",
    "mathematical_optimization",
    "planning_mlops_governance",
)
PRODUCTION_CONTROL_ADVANCED_CAPABILITY_KEYS = (
    "event_sourced_production_lifecycle",
    "graph_relational_routing_work_center_topology",
    "multi_tenant_site_execution_isolation",
    "schema_evolution_resilient_production_schema",
    "probabilistic_downtime_yield_schedule_risk_scoring",
    "real_time_oee_execution_analytics",
    "counterfactual_dispatch_capacity_simulation",
    "temporal_throughput_downtime_forecasting",
    "autonomous_production_exception_resolution",
    "semantic_shop_floor_instruction_parsing",
    "predictive_schedule_quality_maintenance_risk",
    "self_healing_execution_route_selection",
    "zero_knowledge_completion_proof",
    "immutable_production_audit_trail",
    "dynamic_production_policy_screening",
    "automated_production_control_testing",
    "universal_api_async_streaming",
    "cross_system_production_federation",
    "mrp_inventory_quality_asset_integration",
    "decentralized_work_center_asset_identity",
    "chaos_engineered_shop_floor_tolerance",
    "quantum_resistant_production_authorization",
    "carbon_aware_production_scheduling",
    "algebraic_schedule_optimization",
    "mechanism_design_capacity_allocation",
    "information_theoretic_downtime_anomaly_detection",
    "temporal_production_exposure_stochastic_modeling",
    "distributed_systems_engineering",
    "probabilistic_ml_production_risk",
    "cryptographic_engineering",
    "mathematical_optimization",
    "production_mlops_governance",
    "standard_table_stakes_execution_records",
)
QUALITY_ASSURANCE_ADVANCED_CAPABILITY_KEYS = (
    "event_sourced_quality_lifecycle",
    "graph_relational_quality_topology",
    "multi_tenant_quality_isolation",
    "schema_evolution_resilient_quality_schema",
    "probabilistic_defect_escape_compliance_scoring",
    "real_time_spc_quality_analytics",
    "counterfactual_sampling_release_simulation",
    "temporal_defect_escape_forecasting",
    "autonomous_quality_exception_resolution",
    "semantic_inspection_instruction_parsing",
    "predictive_quality_compliance_risk",
    "self_healing_quality_route_selection",
    "zero_knowledge_quality_compliance_proof",
    "immutable_quality_audit_trail",
    "dynamic_quality_policy_screening",
    "automated_quality_control_testing",
    "universal_api_async_streaming",
    "cross_system_quality_federation",
    "production_inventory_supplier_integration",
    "decentralized_lot_item_identity",
    "chaos_engineered_quality_tolerance",
    "quantum_resistant_quality_authorization",
    "carbon_aware_inspection_scheduling",
    "algebraic_inspection_allocation",
    "mechanism_design_disposition_allocation",
    "information_theoretic_defect_anomaly_detection",
    "temporal_quality_exposure_stochastic_modeling",
    "distributed_systems_engineering",
    "probabilistic_ml_quality_risk",
    "cryptographic_engineering",
    "mathematical_optimization",
    "quality_mlops_governance",
)
EAM_ADVANCED_CAPABILITY_KEYS = (
    "event_sourced_maintenance_lifecycle",
    "graph_relational_asset_topology",
    "multi_tenant_maintenance_isolation",
    "schema_evolution_resilient_maintenance_schema",
    "probabilistic_failure_safety_cost_scoring",
    "real_time_reliability_analytics",
    "counterfactual_strategy_simulation",
    "temporal_failure_forecasting",
    "autonomous_maintenance_exception_resolution",
    "semantic_maintenance_instruction_parsing",
    "predictive_maintenance_risk_scoring",
    "self_healing_maintenance_route_selection",
    "zero_knowledge_maintenance_compliance_proof",
    "immutable_maintenance_audit_trail",
    "dynamic_maintenance_policy_screening",
    "automated_maintenance_control_testing",
    "universal_api_async_streaming",
    "cross_system_maintenance_federation",
    "production_quality_inventory_procurement_integration",
    "decentralized_equipment_identity",
    "chaos_engineered_maintenance_tolerance",
    "quantum_resistant_maintenance_authorization",
    "carbon_aware_maintenance_scheduling",
    "algebraic_maintenance_schedule_optimization",
    "mechanism_design_labor_spare_allocation",
    "information_theoretic_failure_anomaly_detection",
    "temporal_maintenance_exposure_stochastic_modeling",
    "distributed_systems_engineering",
    "probabilistic_ml_maintenance_risk",
    "cryptographic_engineering",
    "mathematical_optimization",
    "maintenance_mlops_governance",
)
PRODUCT_CATALOG_PIM_ADVANCED_CAPABILITY_KEYS = (
    "event_sourced_product_lifecycle",
    "graph_relational_product_topology",
    "multi_tenant_catalog_isolation",
    "schema_evolution_resilient_attribute_schema",
    "probabilistic_sellability_compliance_scoring",
    "real_time_catalog_readiness_analytics",
    "counterfactual_publication_simulation",
    "temporal_content_sellability_forecasting",
    "autonomous_enrichment_exception_resolution",
    "semantic_product_instruction_parsing",
    "predictive_product_readiness_risk",
    "self_healing_publication_route_selection",
    "zero_knowledge_catalog_publication_proof",
    "immutable_catalog_audit_trail",
    "dynamic_product_policy_screening",
    "automated_catalog_control_testing",
    "universal_api_async_streaming",
    "cross_system_product_federation",
    "commerce_inventory_tax_content_integration",
    "decentralized_product_identity",
    "chaos_engineered_catalog_tolerance",
    "quantum_resistant_product_authorization",
    "carbon_aware_catalog_publication",
    "algebraic_catalog_optimization",
    "mechanism_design_channel_allocation",
    "information_theoretic_content_anomaly_detection",
    "temporal_sellability_exposure_stochastic_modeling",
    "distributed_systems_engineering",
    "probabilistic_ml_product_readiness",
    "cryptographic_engineering",
    "mathematical_optimization",
    "product_mlops_governance",
)
CUSTOMER_360_ADVANCED_CAPABILITY_KEYS = (
    "event_sourced_customer_lifecycle",
    "graph_relational_customer_topology",
    "multi_tenant_customer_isolation",
    "schema_evolution_resilient_customer_schema",
    "probabilistic_identity_consent_engagement_scoring",
    "real_time_customer_timeline_analytics",
    "counterfactual_preference_segment_simulation",
    "temporal_customer_value_churn_forecasting",
    "autonomous_customer_data_exception_resolution",
    "semantic_customer_instruction_parsing",
    "predictive_customer_health_risk",
    "self_healing_customer_event_route_selection",
    "zero_knowledge_customer_profile_proof",
    "immutable_customer_audit_trail",
    "dynamic_customer_privacy_policy_screening",
    "automated_customer_control_testing",
    "universal_api_async_streaming",
    "cross_system_customer_federation",
    "commerce_billing_service_loyalty_integration",
    "decentralized_customer_identity",
    "chaos_engineered_customer_tolerance",
    "quantum_resistant_customer_authorization",
    "carbon_aware_customer_processing",
    "algebraic_customer_segment_optimization",
    "mechanism_design_channel_allocation",
    "information_theoretic_engagement_anomaly_detection",
    "temporal_customer_exposure_stochastic_modeling",
    "distributed_systems_engineering",
    "probabilistic_ml_customer_health",
    "cryptographic_engineering",
    "mathematical_optimization",
    "customer_mlops_governance",
)
FEDERATED_IAM_ADVANCED_CAPABILITY_KEYS = (
    "event_sourced_identity_lifecycle",
    "graph_relational_trust_topology",
    "multi_tenant_access_isolation",
    "schema_evolution_resilient_claim_schema",
    "probabilistic_identity_session_policy_scoring",
    "real_time_access_analytics",
    "counterfactual_policy_simulation",
    "temporal_access_risk_forecasting",
    "autonomous_identity_exception_resolution",
    "semantic_access_request_parsing",
    "predictive_access_risk_scoring",
    "self_healing_authorization_route_selection",
    "zero_knowledge_policy_decision_proof",
    "immutable_identity_audit_trail",
    "dynamic_access_policy_screening",
    "automated_identity_control_testing",
    "universal_api_async_streaming",
    "cross_system_identity_federation",
    "workforce_customer_service_account_integration",
    "decentralized_principal_identity",
    "chaos_engineered_identity_tolerance",
    "quantum_resistant_token_authorization",
    "carbon_aware_access_processing",
    "algebraic_role_optimization",
    "mechanism_design_privileged_access_allocation",
    "information_theoretic_access_anomaly_detection",
    "temporal_access_exposure_stochastic_modeling",
    "distributed_systems_engineering",
    "probabilistic_ml_access_risk",
    "cryptographic_engineering",
    "mathematical_optimization",
    "identity_mlops_governance",
)
API_GATEWAY_MESH_ADVANCED_CAPABILITY_KEYS = (
    "event_sourced_gateway_lifecycle",
    "graph_relational_service_topology",
    "multi_tenant_gateway_isolation",
    "schema_evolution_resilient_route_schema",
    "probabilistic_latency_saturation_failure_scoring",
    "real_time_mesh_analytics",
    "counterfactual_traffic_policy_simulation",
    "temporal_route_health_forecasting",
    "autonomous_gateway_exception_resolution",
    "semantic_route_request_parsing",
    "predictive_route_risk_scoring",
    "self_healing_mesh_route_selection",
    "zero_knowledge_route_publication_proof",
    "immutable_gateway_audit_trail",
    "dynamic_gateway_policy_screening",
    "automated_gateway_control_testing",
    "universal_api_async_streaming",
    "cross_system_gateway_federation",
    "identity_schema_audit_composition_integration",
    "decentralized_service_identity",
    "chaos_engineered_gateway_tolerance",
    "quantum_resistant_route_authorization",
    "carbon_aware_gateway_routing",
    "algebraic_route_optimization",
    "mechanism_design_traffic_allocation",
    "information_theoretic_traffic_anomaly_detection",
    "temporal_traffic_exposure_stochastic_modeling",
    "distributed_systems_engineering",
    "probabilistic_ml_route_risk",
    "cryptographic_engineering",
    "mathematical_optimization",
    "gateway_mlops_governance",
)
SCHEMA_REGISTRY_ADVANCED_CAPABILITY_KEYS = (
    "event_sourced_schema_lifecycle",
    "graph_relational_contract_topology",
    "multi_tenant_contract_isolation",
    "schema_on_read_contract_extensibility",
    "probabilistic_breaking_change_scoring",
    "real_time_contract_analytics",
    "counterfactual_schema_evolution_simulation",
    "temporal_compatibility_health_forecasting",
    "autonomous_contract_remediation",
    "semantic_schema_intent_parsing",
    "predictive_contract_risk_scoring",
    "self_healing_contract_validation_route_selection",
    "zero_knowledge_schema_acceptance_proof",
    "immutable_contract_audit_trail",
    "dynamic_contract_policy_screening",
    "automated_contract_control_testing",
    "universal_api_async_contract_surface",
    "cross_system_schema_federation",
    "gateway_identity_audit_workflow_composition_integration",
    "decentralized_producer_consumer_identity",
    "chaos_engineered_contract_validation_tolerance",
    "quantum_resistant_schema_signing",
    "carbon_aware_contract_validation",
    "algebraic_schema_diff_minimization",
    "mechanism_design_consumer_impact_allocation",
    "information_theoretic_validation_anomaly_detection",
    "temporal_contract_exposure_stochastic_modeling",
    "distributed_systems_engineering",
    "probabilistic_ml_contract_risk",
    "cryptographic_engineering",
    "mathematical_optimization",
    "contract_mlops_governance",
)
WORKFLOW_ORCHESTRATION_ADVANCED_CAPABILITY_KEYS = (
    "event_sourced_workflow_lifecycle",
    "graph_relational_saga_topology",
    "multi_tenant_workflow_isolation",
    "schema_on_read_workflow_context",
    "probabilistic_sla_breach_scoring",
    "real_time_workflow_analytics",
    "counterfactual_saga_policy_simulation",
    "temporal_workflow_forecasting",
    "autonomous_compensation_recommendation",
    "semantic_workflow_intent_parsing",
    "predictive_saga_risk_scoring",
    "self_healing_workflow_route_selection",
    "zero_knowledge_workflow_completion_proof",
    "immutable_workflow_audit_trail",
    "dynamic_workflow_policy_screening",
    "automated_workflow_control_testing",
    "universal_api_async_workflow_surface",
    "cross_system_workflow_federation",
    "gateway_schema_audit_identity_composition_integration",
    "decentralized_workflow_actor_identity",
    "chaos_engineered_workflow_tolerance",
    "quantum_resistant_workflow_authorization",
    "carbon_aware_workflow_scheduling",
    "algebraic_state_machine_minimization",
    "mechanism_design_saga_resource_allocation",
    "information_theoretic_workflow_anomaly_detection",
    "temporal_workflow_exposure_stochastic_modeling",
    "distributed_systems_engineering",
    "probabilistic_ml_workflow_risk",
    "cryptographic_engineering",
    "mathematical_optimization",
    "workflow_mlops_governance",
)
AUDIT_LEDGER_ADVANCED_CAPABILITY_KEYS = (
    "event_sourced_audit_lifecycle",
    "graph_relational_evidence_topology",
    "multi_tenant_audit_isolation",
    "schema_on_read_evidence_envelope",
    "probabilistic_tamper_control_risk_scoring",
    "real_time_audit_analytics",
    "counterfactual_retention_disclosure_simulation",
    "temporal_evidence_health_forecasting",
    "autonomous_control_remediation",
    "semantic_audit_query_parsing",
    "predictive_audit_risk_scoring",
    "self_healing_audit_ingestion_route_selection",
    "zero_knowledge_event_disclosure_proof",
    "immutable_regulatory_trail",
    "dynamic_audit_policy_screening",
    "automated_audit_control_testing",
    "universal_api_async_audit_surface",
    "cross_system_audit_federation",
    "identity_gateway_schema_workflow_composition_integration",
    "decentralized_actor_identity",
    "chaos_engineered_audit_tolerance",
    "quantum_resistant_audit_signing",
    "carbon_aware_audit_processing",
    "algebraic_evidence_minimization",
    "mechanism_design_export_reviewer_allocation",
    "information_theoretic_audit_anomaly_detection",
    "temporal_evidence_exposure_stochastic_modeling",
    "distributed_systems_engineering",
    "probabilistic_ml_audit_risk",
    "cryptographic_engineering",
    "mathematical_optimization",
    "audit_mlops_governance",
)
COMPOSITION_ENGINE_ADVANCED_CAPABILITY_KEYS = (
    "event_sourced_composition_lifecycle",
    "graph_relational_component_topology",
    "multi_tenant_workspace_isolation",
    "schema_on_read_layout_extension",
    "probabilistic_release_risk_scoring",
    "real_time_composition_analytics",
    "counterfactual_layout_simulation",
    "temporal_release_readiness_forecasting",
    "autonomous_layout_remediation",
    "semantic_composition_intent_parsing",
    "predictive_composition_risk_scoring",
    "self_healing_publication_route_selection",
    "zero_knowledge_publication_proof",
    "immutable_composition_audit_trail",
    "dynamic_composition_policy_screening",
    "automated_composition_control_testing",
    "universal_api_async_composition_surface",
    "cross_system_composition_federation",
    "identity_gateway_schema_workflow_audit_integration",
    "decentralized_publisher_identity",
    "chaos_engineered_composition_tolerance",
    "quantum_resistant_publication_signing",
    "carbon_aware_composition_build",
    "algebraic_layout_optimization",
    "mechanism_design_fragment_slot_allocation",
    "information_theoretic_composition_anomaly_detection",
    "temporal_release_exposure_stochastic_modeling",
    "distributed_systems_engineering",
    "probabilistic_ml_composition_risk",
    "cryptographic_engineering",
    "mathematical_optimization",
    "composition_mlops_governance",
)
IMPLEMENTED_PBC_KEYS = (
    "gl_core",
    "ap_automation",
    "ar_credit",
    "treasury_cash",
    "asset_lifecycle",
    "tax_localization",
    "inventory_positioning",
    "wms_core",
    "procurement_sourcing",
    "transportation_management",
    "personnel_identity",
    "time_labor",
    "payroll_engine",
    "talent_onboarding",
    "mrp_engine",
    "production_control",
    "quality_assurance",
    "eam",
    "dom",
    "product_catalog_pim",
    "customer_360",
    "federated_iam",
    "api_gateway_mesh",
    "schema_registry",
    "workflow_orchestration",
    "audit_ledger",
    "composition_engine",
    "global_inventory_visibility",
    "order_routing_optimization",
    "checkout_processing",
    "payment_orchestration",
    "subscription_billing",
    "returns_reverse_logistics",
    "cross_border_trade",
    "multi_sided_market",
    "enterprise_pim",
    "dam_core",
    "price_promotion_engine",
    "lead_opportunity",
    "service_ticketing",
    "notifications",
    "cdp_segmentation",
    "loyalty_rewards",
    "streaming_analytics",
    "enterprise_search_vector",
    "predictive_demand",
    "fraud_anomaly_detection",
)
PBC_ALLOWED_DATASTORE_BACKENDS = (
    "postgresql",
    "mysql",
    "mariadb",
)
ACP_STREAM_PROCESSORS: dict[str, dict] = {
    "faust_streaming": {
        "label": "Faust-Streaming",
        "core_architecture": "pure_python_asyncio_actor_mesh",
        "state_preservation": "embedded_rocksdb_or_in_memory",
        "primary_use_case": "event_driven_microservices_and_asynchronous_workflows",
        "concurrency_model": "asyncio_event_loops",
        "best_for": ("event_driven_service", "async_workflow", "saga_orchestration"),
    },
    "quix_streams": {
        "label": "Quix Streams",
        "core_architecture": "pure_python_rocksdb_state_backend",
        "state_preservation": "embedded_rocksdb_on_disk",
        "primary_use_case": "high_throughput_time_series_and_event_data_processing",
        "concurrency_model": "python_multiprocessing_threads",
        "best_for": ("time_series", "event_processing", "high_throughput_ingestion"),
    },
    "bytewax": {
        "label": "Bytewax",
        "core_architecture": "rust_core_python_dataflow_api",
        "state_preservation": "local_in_memory_distributed_recovery",
        "primary_use_case": "complex_parallel_transformations_and_stateful_pipelines",
        "concurrency_model": "rust_multithreaded_execution_threads",
        "best_for": ("parallel_dataflow", "stateful_pipeline", "complex_transform"),
    },
}
ACP_DEFAULT_STREAM_PROCESSOR = "faust_streaming"
ACP_STREAM_PROCESSOR_DECISION_RULES = (
    {
        "processor": "faust_streaming",
        "decision": "default",
        "use_when": (
            "event-driven PBC service",
            "asynchronous workflow",
            "saga orchestration",
            "service-owned local state",
        ),
    },
    {
        "processor": "quix_streams",
        "decision": "exception",
        "use_when": (
            "high-throughput telemetry",
            "time-series stream",
            "large event ingestion",
            "windowed operational metrics",
        ),
    },
    {
        "processor": "bytewax",
        "decision": "exception",
        "use_when": (
            "complex parallel dataflow",
            "stateful transformation graph",
            "CPU-heavy stream transform",
            "multi-stage analytical pipeline",
        ),
    },
)
ACP_STREAM_PROCESSING_POLICY = {
    "default": ACP_DEFAULT_STREAM_PROCESSOR,
    "allowed_processors": tuple(ACP_STREAM_PROCESSORS),
    "developer_guidance": {
        "standard_answer": (
            "Use the generated AppGen-X event contract: transactional "
            "outbox/inbox tables, typed handlers, retries, idempotency, "
            "dead-letter flows, and the platform event adapter. Do not choose "
            "a stream engine for ordinary work."
        ),
        "prescriptive_choice": "appgen_event_contract_only",
        "developer_decision_count": 1,
        "visible_developer_choice": "appgen_event_contract",
        "visible_choice_count": 1,
        "hidden_runtime_profile": ACP_DEFAULT_STREAM_PROCESSOR,
        "public_contract": (
            "AppGen-X event contract with generated transactional outbox/inbox, "
            "typed handlers, retry, idempotency, dead-letter, and release evidence."
        ),
        "runtime_owner": "platform_event_adapter",
        "choice_limit_reason": (
            "Every extra visible stream option multiplies generated-app "
            "validation across datastore, adapter, target package, deployment, "
            "PBC ownership, and release-audit surfaces."
        ),
        "implementation_recipe": (
            "declare_commands_and_events",
            "generate_owned_tables",
            "generate_transactional_outbox_inbox",
            "generate_typed_handlers",
            "wire_handlers_through_appgen_event_adapter",
            "prove_retry_idempotency_dead_letter_and_release_audit",
        ),
        "normal_workloads": (
            "ERP, CRM, HR, finance, inventory, commerce, approvals, workflow "
            "sagas, chatbot events, agent task routing, and PBC integration "
            "handlers."
        ),
        "manifest_rule": (
            "Omit stream_processor for ordinary PBCs; validation normalizes "
            "the manifest to faust_streaming."
        ),
        "ide_rule": (
            "Do not render a stream-engine picker for ordinary app generation; "
            "show the selected profile as read-only generated metadata."
        ),
        "agent_rule": (
            "Coding agents must generate event contracts and adapter calls, "
            "not direct stream-library imports."
        ),
        "exception_gate": (
            "Open the exception workflow only for telemetry/time-series "
            "ingestion or complex parallel dataflow workloads with evidence."
        ),
        "exception_policy": "two_audited_exception_profiles_not_user_preferences",
        "split_rule": (
            "If a PBC needs both ordinary domain events and specialized stream "
            "processing, split the specialized workload into its own PBC."
        ),
    },
    "developer_guidance_contract": {
        "question": "What should a developer actually use?",
        "answer": "Use appgen_event_contract.",
        "visible_options": ("appgen_event_contract",),
        "visible_option_count": 1,
        "ordinary_manifest_instruction": "Omit stream_processor.",
        "ordinary_datastore_instruction": "Use PostgreSQL by default, or MySQL/MariaDB when that is the project standard.",
        "ordinary_generation_instruction": (
            "Generate owned tables, appgen_outbox_event, appgen_inbox_event, "
            "typed handlers, idempotency keys, retry policies, dead-letter "
            "envelopes, and release evidence through the AppGen-X event adapter."
        ),
        "small_model_instruction": (
            "Use appgen_event_contract. Omit stream_processor. Generate "
            "outbox/inbox tables and typed handlers through the AppGen-X "
            "event adapter. Open an exception only for telemetry/time-series "
            "or complex parallel dataflow with evidence."
        ),
        "exception_options": ("quix_streams", "bytewax"),
        "exception_rule": (
            "Exception profiles are audit workflows, not developer preferences; "
            "split the specialized workload into its own PBC and require "
            "stream_exception_evidence."
        ),
        "hard_limits": {
            "ordinary_visible_choices": 1,
            "stream_profiles_per_pbc": 1,
            "ordinary_stream_engine_picker": False,
            "direct_profile_imports_in_generated_business_logic": False,
        },
        "developer_choice_lock": {
            "default_action": "generate_appgen_event_contract",
            "ordinary_manifest": {"stream_processor": "omit"},
            "ordinary_runtime_selection": "not_developer_selectable",
            "ide_surface": "show_event_contract_controls_only",
            "natural_language_surface": "do_not_expand_into_stream_runtime_comparison",
            "exception_unlocks": (
                "telemetry_time_series_high_volume_windowing_with_evidence",
                "complex_parallel_dataflow_with_evidence",
            ),
        },
        "stop_generating_options_when": (
            "The workload is ordinary business, ERP, workflow, chatbot, agent, "
            "integration, approval, or PBC event handling."
        ),
        "route_to_exception_workflow_when": (
            "The prompt names telemetry/time-series/high-volume windowing or "
            "complex parallel dataflow/CPU-heavy transformation and includes "
            "evidence."
        ),
        "developer_facing_apis": (
            "acp_event_processing_developer_guidance",
            "resolve_acp_event_processing_choice",
            "lint_pbc_eventing_choice",
        ),
        "platform_internal_apis": (
            "acp_stream_processor_catalog",
            "select_acp_stream_processor",
        ),
        "api_rule": (
            "Studio, DSL generation, package templates, and external coding "
            "agents use the developer-facing APIs. They must not expose the "
            "stream processor catalog or selector as an ordinary app choice."
        ),
    },
    "developer_action_contract": {
        "id": "appgen.event-processing.developer-action.v1",
        "question": "What should platform developers actually use?",
        "answer": "Use appgen_event_contract.",
        "use_this_stack": (
            "postgresql_default_or_mysql_mariadb_project_standard",
            "appgen_event_contract",
            "appgen_outbox_event",
            "appgen_inbox_event",
            "typed_command_handlers",
            "typed_event_handlers",
            "appgen_event_adapter",
            "generated_retry_idempotency_dead_letter_release_evidence",
        ),
        "ordinary_manifest_rule": "omit_stream_processor",
        "ordinary_codegen_rule": (
            "Generate owned tables, appgen_outbox_event, appgen_inbox_event, "
            "typed handlers, retry, idempotency, dead-letter, and release "
            "evidence through the AppGen-X event adapter."
        ),
        "ordinary_backend_rule": "postgresql_default_mysql_or_mariadb_project_standard",
        "developer_visible_options": ("appgen_event_contract",),
        "do_not_expose": (
            "stream_engine_picker",
            "runtime_profile_picker",
            "broker_picker",
            "state_store_picker",
            "per_pbc_runtime_preference",
        ),
        "do_not_generate": (
            "direct_stream_library_imports",
            "developer_selected_broker_clients",
            "per_pbc_stream_runtime_branches",
            "runtime_comparison_prompts",
            "custom_event_state_stores_for_ordinary_pbc_logic",
        ),
        "ordinary_path": (
            "declare_commands_and_events",
            "generate_owned_tables",
            "generate_appgen_outbox_event",
            "generate_appgen_inbox_event",
            "generate_typed_handlers",
            "wire_handlers_through_appgen_event_adapter",
            "prove_retry_idempotency_dead_letter_and_release_evidence",
        ),
        "exception_paths": (
            {
                "profile": "quix_streams",
                "only_for": "telemetry_time_series_high_volume_windowed_metrics",
                "requires": "stream_exception_evidence",
            },
            {
                "profile": "bytewax",
                "only_for": "complex_parallel_dataflow_cpu_heavy_transformations",
                "requires": "stream_exception_evidence",
            },
        ),
        "choice_budget": {
            "ordinary_visible_event_contracts": 1,
            "ordinary_visible_stream_engine_choices": 0,
            "ordinary_visible_runtime_profile_choices": 0,
            "exception_profiles": 2,
            "stream_profiles_per_pbc": 1,
        },
        "fallback_rule": (
            "If the exception workload and evidence are not explicit, generate "
            "appgen_event_contract and omit stream_processor."
        ),
        "api_call_order": (
            "acp_event_processing_developer_guidance",
            "resolve_acp_event_processing_choice",
            "lint_pbc_eventing_choice",
        ),
        "internal_api_boundary": (
            "Do not call select_acp_stream_processor from ordinary generated-app "
            "templates or Studio controls; it is platform-runtime metadata for "
            "exception validation."
        ),
        "token_efficient_prompt": (
            "Use appgen_event_contract. Omit stream_processor. Generate "
            "outbox/inbox tables and typed handlers through the AppGen-X event "
            "adapter. Do not compare runtimes. Open an exception only for "
            "telemetry/time-series or complex dataflow with evidence."
        ),
    },
    "developer_use_card": {
        "id": "appgen.event-processing.use-this.v1",
        "title": "Use appgen_event_contract for ordinary generated applications.",
        "decision": "mandatory_default",
        "use": "appgen_event_contract",
        "ordinary_manifest": {"stream_processor": "omit"},
        "ordinary_datastores": ("postgresql", "mysql", "mariadb"),
        "developer_writes": (
            "commands",
            "domain_events",
            "owned_tables",
            "handler_functions",
            "retry_policy_names",
            "idempotency_key_fields",
            "dead_letter_ownership_notes",
        ),
        "platform_generates": (
            "appgen_outbox_event",
            "appgen_inbox_event",
            "typed_command_handlers",
            "typed_event_handlers",
            "event_adapter_bindings",
            "release_audit_evidence",
        ),
        "studio_exposes": (
            "event_contract_designer",
            "handler_registry_editor",
            "retry_idempotency_dead_letter_editor",
            "read_only_runtime_profile_badge",
        ),
        "studio_hides": (
            "stream_engine_picker",
            "broker_picker",
            "state_store_picker",
            "per_pbc_runtime_profile_picker",
        ),
        "ordinary_stop_rule": (
            "For ERP, workflow, chatbot, agent, integration, approval, and "
            "ordinary PBC events, stop at appgen_event_contract and do not "
            "generate a runtime comparison."
        ),
        "exception_unlocks": (
            "telemetry_time_series_high_volume_windowing_with_stream_exception_evidence",
            "complex_parallel_dataflow_with_stream_exception_evidence",
        ),
        "fallback": "When uncertain, use appgen_event_contract and omit stream_processor.",
    },
    "developer_decision_brief": {
        "headline": "Use appgen_event_contract.",
        "ordinary_answer": (
            "Generate the AppGen-X event contract with transactional "
            "outbox/inbox tables, typed handlers, retries, idempotency, "
            "dead-letter handling, and release evidence."
        ),
        "ordinary_manifest_rule": "Omit stream_processor.",
        "ordinary_codegen_prompt": (
            "Generate AppGen-X outbox/inbox events through the platform "
            "adapter. Omit stream_processor. Do not compare stream engines."
        ),
        "developer_visible_options": ("appgen_event_contract",),
        "developer_visible_option_count": 1,
        "default_runtime_profile_visibility": "read_only_generated_metadata",
        "studio_controls": (
            "event_contract_designer",
            "handler_registry_editor",
            "retry_idempotency_dead_letter_editor",
            "read_only_runtime_profile_badge",
        ),
        "studio_controls_to_hide": ("stream_engine_picker", "per_pbc_runtime_preference"),
        "linter_rules": (
            "ordinary_pbc_manifest_omits_stream_processor",
            "generated_business_logic_imports_appgen_event_adapter_only",
            "exception_profiles_require_stream_exception_evidence",
            "one_stream_profile_per_pbc",
        ),
        "allowed_exceptions": ("quix_streams", "bytewax"),
        "exception_gate": (
            "Use an exception profile only for telemetry/time-series/high-volume "
            "windowing or complex parallel dataflow with evidence."
        ),
        "small_model_stop_rule": (
            "When the request is ordinary business, ERP, workflow, chatbot, "
            "agent, integration, or PBC event handling, stop branching and use "
            "the ordinary answer."
        ),
        "api_contract": (
            "Call resolve_acp_event_processing_choice for generation decisions; "
            "render acp_event_processing_developer_guidance for help text; run "
            "lint_pbc_eventing_choice before release."
        ),
    },
    "developer_implementation_playbook": {
        "id": "appgen.event-processing.implementation-playbook.v1",
        "purpose": "tell platform developers exactly what to build for ordinary evented apps",
        "studio": (
            "show_event_contract_designer",
            "show_handler_registry_editor",
            "show_retry_idempotency_dead_letter_editor",
            "show_read_only_runtime_profile_badge",
            "hide_stream_engine_picker",
            "hide_per_pbc_runtime_preference",
        ),
        "dsl_linter": (
            "require_ordinary_manifests_to_omit_stream_processor",
            "offer_remove_stream_processor_quick_fix",
            "block_exception_profiles_without_stream_exception_evidence",
            "block_profile_specific_imports_in_generated_business_logic",
        ),
        "natural_language_generation": (
            "map_ordinary_business_prompts_to_appgen_event_contract",
            "generate_outbox_inbox_tables_and_typed_handlers",
            "avoid_runtime_comparison_prompts",
            "open_exception_workflow_only_with_named_evidence",
        ),
        "package_templates": (
            "include_appgen_outbox_event",
            "include_appgen_inbox_event",
            "include_event_adapter_bindings",
            "include_retry_policy",
            "include_idempotency_keys",
            "include_dead_letter_contract",
            "include_release_audit_evidence",
        ),
        "coding_agent_prompt": (
            "Use appgen_event_contract. Omit stream_processor. Generate "
            "outbox/inbox tables, typed handlers, retry, idempotency, "
            "dead-letter, and release evidence through the AppGen-X event "
            "adapter. Do not compare runtimes."
        ),
        "acceptance_criteria": (
            "ordinary_manifest_has_no_stream_processor",
            "generated_business_logic_imports_only_appgen_event_adapter",
            "studio_has_no_stream_runtime_picker",
            "exception_profiles_require_stream_exception_evidence",
            "release_audit_records_event_contract_outputs",
            "ordinary_generators_do_not_call_stream_processor_selector",
        ),
    },
    "developer_decision_runbook": {
        "id": "appgen.event-processing.decision-runbook.v1",
        "audience": (
            "human_developers",
            "studio_builders",
            "dsl_authors",
            "natural_language_generators",
            "external_coding_agents",
        ),
        "answer": "Use appgen_event_contract. Omit stream_processor.",
        "step_order": (
            "classify_workload",
            "if_ordinary_stop_branching",
            "generate_event_contract",
            "generate_outbox_inbox_tables",
            "generate_typed_handlers",
            "wire_platform_event_adapter",
            "run_eventing_linter",
            "record_release_evidence",
        ),
        "ordinary_workload_terms": (
            "erp",
            "finance",
            "hr",
            "inventory",
            "procurement",
            "commerce",
            "workflow",
            "approval",
            "chatbot",
            "agent",
            "integration",
            "pbc_event_handling",
        ),
        "ordinary_stop_condition": (
            "When the workload matches ordinary business or application "
            "events, return the single answer and do not generate a runtime "
            "comparison, picker, or matrix."
        ),
        "bounded_datastores": ("postgresql", "mysql", "mariadb"),
        "hidden_axes": (
            "stream_engine",
            "broker",
            "state_store",
            "runtime_profile",
            "per_pbc_runtime_preference",
        ),
        "exception_request_shape": {
            "allowed_profiles": ("quix_streams", "bytewax"),
            "requires": (
                "split_specialized_pbc",
                "stream_exception_evidence",
                "release_audit_gate",
            ),
        },
        "machine_checks": (
            "lint_pbc_eventing_choice",
            "resolve_acp_event_processing_choice",
            "pbc_release_audit",
        ),
        "small_model_prompt": (
            "Use appgen_event_contract. Omit stream_processor. Generate "
            "outbox/inbox tables, typed handlers, retry, idempotency, "
            "dead-letter, and release evidence through the AppGen-X event "
            "adapter. Do not compare runtimes."
        ),
        "fail_closed_rule": (
            "If classification or exception evidence is unclear, generate the "
            "ordinary event contract and omit stream_processor."
        ),
    },
    "developer_choice_algorithm": (
        {
            "step": 1,
            "if": "ordinary business, ERP, workflow, chatbot, agent, integration, or PBC event handling",
            "then": "generate the AppGen-X event contract",
            "manifest": "omit stream_processor",
            "runtime_profile": ACP_DEFAULT_STREAM_PROCESSOR,
            "requires_evidence": False,
        },
        {
            "step": 2,
            "if": "telemetry, time-series ingestion, high-volume ingestion, or windowed operational metrics",
            "then": "split into a specialized PBC and request the telemetry exception profile",
            "manifest": "stream_processor=quix_streams",
            "runtime_profile": "quix_streams",
            "requires_evidence": True,
        },
        {
            "step": 3,
            "if": "complex parallel dataflow, CPU-heavy stream transformation, or multi-stage analytical pipeline",
            "then": "split into a specialized PBC and request the dataflow exception profile",
            "manifest": "stream_processor=bytewax",
            "runtime_profile": "bytewax",
            "requires_evidence": True,
        },
        {
            "step": 4,
            "if": "anything else or unclear",
            "then": "generate the AppGen-X event contract",
            "manifest": "omit stream_processor",
            "runtime_profile": ACP_DEFAULT_STREAM_PROCESSOR,
            "requires_evidence": False,
        },
    ),
    "developer_use_policy": {
        "ordinary_applications": {
            "use": "appgen_event_contract",
            "developer_instruction": (
                "Generate transactional outbox/inbox tables and typed handlers "
                "through the AppGen-X event adapter."
            ),
            "manifest_rule": "omit_stream_processor",
            "datastore_rule": "postgresql_by_default_mysql_or_mariadb_when_project_standard",
            "generated_stack": (
                "owned_tables",
                "appgen_outbox_event",
                "appgen_inbox_event",
                "typed_event_handlers",
                "retry_policy",
                "idempotency_keys",
                "dead_letter_contract",
                "release_audit_evidence",
            ),
            "visible_developer_options": ("appgen_event_contract",),
        },
        "telemetry_exception": {
            "use": "quix_streams_exception_workflow",
            "developer_instruction": (
                "Split telemetry, time-series, high-volume ingestion, or "
                "windowed metrics into a specialized PBC and provide evidence."
            ),
            "manifest_rule": "stream_processor=quix_streams_with_stream_exception_evidence",
            "requires_evidence": True,
        },
        "dataflow_exception": {
            "use": "bytewax_exception_workflow",
            "developer_instruction": (
                "Split complex parallel dataflow, CPU-heavy transforms, or "
                "multi-stage analytical pipelines into a specialized PBC and "
                "provide evidence."
            ),
            "manifest_rule": "stream_processor=bytewax_with_stream_exception_evidence",
            "requires_evidence": True,
        },
    },
    "choice_budget": {
        "ordinary_public_event_contracts": 1,
        "ordinary_visible_stream_engine_choices": 0,
        "ordinary_visible_runtime_choices": ("appgen_event_contract",),
        "exception_profiles": ("quix_streams", "bytewax"),
        "exception_profile_count": 2,
        "stream_profiles_per_pbc": 1,
        "additional_profile_requires": (
            "architecture_decision",
            "executable_policy",
            "manifest_validation",
            "release_audit_gate",
            "generated_tests",
            "developer_documentation",
        ),
    },
    "ordinary_workload_contract": {
        "public_choice": "appgen_event_contract",
        "developer_prompt": (
            "Generate commands, events, transactional outbox/inbox tables, "
            "typed handlers, idempotency, retry, dead-letter, and release "
            "evidence through the AppGen-X event adapter."
        ),
        "manifest_fields": ("commands", "events", "tables", "apis", "emits", "consumes"),
        "manifest_fields_to_omit": ("stream_processor",),
        "generated_files": ("models.py", "events.py", "services.py", "api.py", "pbc_runtime.py"),
        "forbidden_imports": ("faust_streaming", "quix_streams", "bytewax"),
        "studio_control": "read_only_runtime_profile_badge",
    },
    "developer_default_stack": {
        "id": "appgen.event-processing.default-stack.v1",
        "scope": "ordinary_generated_applications_and_pbcs",
        "use": "appgen_event_contract",
        "database": "postgresql_default_mysql_or_mariadb_when_project_standard",
        "durability": ("appgen_outbox_event", "appgen_inbox_event"),
        "handler_api": "appgen_event_adapter",
        "handler_shape": ("typed_command_handlers", "typed_event_handlers"),
        "operations": (
            "idempotency_keys",
            "retry_policy",
            "dead_letter_contract",
            "release_audit_evidence",
        ),
        "ordinary_manifest": {"stream_processor": "omit"},
        "runtime_visibility": "read_only_platform_metadata",
        "developer_choice_count": 1,
        "small_model_prompt": (
            "Use appgen_event_contract with generated outbox/inbox tables and "
            "typed handlers through the AppGen-X event adapter. Omit "
            "stream_processor. Do not compare runtimes."
        ),
        "blocked_expansion_axes": (
            "stream_engine",
            "broker_client",
            "state_store",
            "per_pbc_runtime",
            "direct_stream_library_import",
        ),
    },
    "developer_recommendation_card": {
        "id": "appgen.event-processing.recommendation-card.v1",
        "title": "Use appgen_event_contract.",
        "status": "mandatory_for_ordinary_generated_work",
        "recommendation": (
            "Use the AppGen-X event contract with generated outbox/inbox "
            "tables and typed handlers. Developers author commands, events, "
            "and handlers; the platform owns the runtime adapter."
        ),
        "developer_writes": (
            "commands",
            "events",
            "handler_functions",
            "business_tables",
        ),
        "platform_generates": (
            "appgen_outbox_event",
            "appgen_inbox_event",
            "event_adapter_bindings",
            "retry_policy",
            "idempotency_keys",
            "dead_letter_contract",
            "release_audit_evidence",
        ),
        "ordinary_manifest": {"stream_processor": "omit"},
        "ordinary_database_backends": ("postgresql", "mysql", "mariadb"),
        "hidden_runtime_profile": ACP_DEFAULT_STREAM_PROCESSOR,
        "visible_developer_options": ("appgen_event_contract",),
        "visible_choice_count": 1,
        "not_a_question_for_developers": (
            "stream_engine",
            "broker_client",
            "state_store",
            "per_pbc_runtime_profile",
        ),
        "exception_exit_criteria": (
            "telemetry_time_series_high_volume_windowing_with_stream_exception_evidence",
            "complex_parallel_dataflow_with_stream_exception_evidence",
        ),
        "fallback": "Use appgen_event_contract and omit stream_processor.",
    },
    "decision_card": {
        "answer": "Use the AppGen-X generated outbox/inbox event contract; the platform keeps faust_streaming behind the adapter for ordinary work.",
        "default_profile": ACP_DEFAULT_STREAM_PROCESSOR,
        "choice_contract": "one_default_two_audited_exceptions",
        "public_contract": "appgen_event_contract",
        "do_this": (
            "model commands and events",
            "generate transactional outbox/inbox tables",
            "write typed handlers behind the AppGen-X event adapter",
            "prove retry, idempotency, dead-letter, and release-audit coverage",
        ),
        "do_not_do_this": (
            "compare Kafka alternatives for ordinary generated work",
            "render a stream-engine picker",
            "generate per-PBC runtime preferences",
            "import stream-processing libraries directly from generated business logic",
        ),
        "ordinary_developer_choices": ("appgen_event_contract",),
        "ordinary_developer_choice_count": 1,
        "selection_mode": "read_only_default_with_audited_exceptions",
        "do_not_ask_users_to_choose": True,
        "developer_selection": "not_user_selectable_for_ordinary_app_generation",
        "ide_behavior": "show the generated default profile and open an exception request only when evidence is supplied",
        "nl_generator_behavior": "choose the default for ordinary business, workflow, chatbot, agent, and ERP prompts",
        "business_logic_rule": "generated business logic imports the AppGen-X event adapter, not profile-specific stream libraries",
        "selection_algorithm": "first_matching_rule_from_developer_choice_algorithm",
    },
    "developer_choice_lock": {
        "id": "appgen.event-processing.choice-lock.v1",
        "purpose": "limit_exponential_stream_runtime_choice_growth",
        "ordinary_answer": "appgen_event_contract",
        "ordinary_manifest_fields": {"stream_processor": "omit"},
        "ordinary_visible_choices": ("appgen_event_contract",),
        "ordinary_visible_choice_count": 1,
        "developer_selectable_runtime_profiles": (),
        "platform_owned_runtime_profile": ACP_DEFAULT_STREAM_PROCESSOR,
        "exception_profiles": ("quix_streams", "bytewax"),
        "exception_requires": "stream_exception_evidence",
        "stop_rule": (
            "If the prompt is ordinary business, ERP, workflow, chatbot, "
            "agent, integration, approval, or PBC event handling, stop at "
            "appgen_event_contract and do not compare stream runtimes."
        ),
    },
    "developer_decision_record": {
        "id": "appgen.event-processing.standard.v1",
        "status": "mandatory",
        "decision": "ordinary_generated_applications_use_appgen_event_contract",
        "developer_answer": "Use appgen_event_contract and omit stream_processor.",
        "reason": (
            "The platform can validate one ordinary event path across PBCs, "
            "datastores, generated targets, adapters, tests, and release "
            "audits. A user-facing stream-engine choice would multiply that "
            "support matrix for every generated capability."
        ),
        "ordinary_path": (
            "generate_owned_tables",
            "generate_transactional_outbox_inbox",
            "generate_typed_handlers",
            "route_through_platform_event_adapter",
            "record_runtime_profile_as_read_only_metadata",
        ),
        "support_matrix_cap": {
            "ordinary_event_contracts": 1,
            "ordinary_visible_stream_engines": 0,
            "ordinary_visible_runtime_profiles": 0,
            "exception_profiles": 2,
            "profiles_per_pbc": 1,
        },
        "exception_gate": (
            "Only telemetry/time-series or complex parallel dataflow workloads "
            "may request an exception, and only with stream_exception_evidence."
        ),
        "tooling_obligations": (
            "hide_stream_engine_picker",
            "lint_ordinary_manifests_that_set_stream_processor",
            "block_exception_profiles_without_evidence",
            "fail_generated_business_logic_with_profile_specific_imports",
            "route_generators_through_event_choice_resolver",
        ),
    },
    "opinionated_stack": {
        "default_event_adapter": "appgen_outbox_inbox_faust_streaming",
        "development": "appgen_in_memory_event_bus_with_generated_outbox_inbox",
        "production": "appgen_event_backbone_adapter_with_generated_outbox_inbox",
        "service_runtime": ACP_DEFAULT_STREAM_PROCESSOR,
        "state_boundary": "owned_by_one_pbc_datastore",
        "selection_mode": "platform_default_unless_exception_evidence_is_present",
        "visible_runtime_choices": ("appgen_event_contract",),
    },
    "developer_rule": (
        "Do not choose a stream engine for ordinary generated applications. "
        "Use the platform event contract, generated outbox/inbox adapters, "
        "and the default processor. Select an exception processor only when "
        "the workload matches a documented exception profile and includes "
        "machine-checkable evidence."
    ),
    "generation_rule": (
        "Generated manifests omit stream_processor unless they need an "
        "exception. Validation normalizes missing values to the default."
    ),
    "implementation_directive": (
        "Generate transactional outbox/inbox tables, typed event handlers, "
        "idempotency keys, retry policies, dead-letter contracts, and release "
        "audit evidence. Do not generate direct imports of faust_streaming, "
        "quix_streams, or bytewax in PBC business logic; profile-specific code "
        "belongs only in platform adapter modules."
    ),
    "generator_outputs": (
        "transactional_outbox",
        "transactional_inbox",
        "typed_event_handlers",
        "idempotency_keys",
        "retry_policy_names",
        "dead_letter_contracts",
        "release_audit_evidence",
    ),
    "decision_ladder": (
        "omit_stream_processor_for_ordinary_apps",
        "normalize_missing_profile_to_faust_streaming",
        "require_exception_evidence_for_quix_streams_or_bytewax",
        "split_specialized_stream_workloads_into_their_own_pbc",
        "block_release_when_exception_evidence_is_missing",
    ),
    "workload_defaults": (
        {"workload": "erp_crm_hr_finance_inventory_commerce", "processor": ACP_DEFAULT_STREAM_PROCESSOR, "decision": "default"},
        {"workload": "workflow_saga_approval_agent_task_routing", "processor": ACP_DEFAULT_STREAM_PROCESSOR, "decision": "default"},
        {"workload": "chatbot_agentic_application_events", "processor": ACP_DEFAULT_STREAM_PROCESSOR, "decision": "default"},
        {"workload": "telemetry_time_series_large_ingestion", "processor": "quix_streams", "decision": "exception"},
        {"workload": "complex_parallel_dataflow_cpu_heavy_transform", "processor": "bytewax", "decision": "exception"},
    ),
    "exception_prompts": (
        "What named workload requires the exception?",
        "What throughput, latency, state, or recovery constraint makes the default insufficient?",
        "Who owns runtime operations and incidents for this specialized workload?",
    ),
    "exception_required_evidence": (
        "workload_name",
        "throughput_or_latency_reason",
        "state_shape",
        "operational_owner",
    ),
    "prohibited": (
        "per-PBC custom stream engines",
        "mixing multiple processors inside one PBC",
        "shared stream-state stores across PBC datastore boundaries",
        "adding a fourth processor without a platform architecture decision",
        "asking natural-language generation to compare stream libraries",
        "exposing a free-form stream-engine selector in the IDE",
        "importing profile-specific stream libraries from generated business logic",
    ),
    "decision_tree": (
        {
            "when": "ordinary domain events, commands, sagas, outbox handlers, workflow services, or agent tasks",
            "use": ACP_DEFAULT_STREAM_PROCESSOR,
        },
        {
            "when": "high-throughput telemetry, time-series streams, large ingestion, or windowed operational metrics",
            "use": "quix_streams",
        },
        {
            "when": "complex parallel dataflows, CPU-heavy transforms, stateful transformation graphs, or analytical pipelines",
            "use": "bytewax",
        },
    ),
}


PBC_MESHES: dict[str, dict] = {
    "finops": {
        "label": "Financial Operations",
        "description": "Monetary, compliance, accounting, and treasury capabilities.",
    },
    "scl": {
        "label": "Supply Chain and Logistics",
        "description": "Physical movement, storage, sourcing, and fulfillment capabilities.",
    },
    "hcm": {
        "label": "Human Capital Management",
        "description": "Personnel, identity, labor, payroll, and talent capabilities.",
    },
    "opsmfg": {
        "label": "Operations and Manufacturing",
        "description": "Planning, production, quality, and asset maintenance capabilities.",
    },
    "cx": {
        "label": "Commerce and Customer Experience",
        "description": "Demand capture, order orchestration, catalog, and customer capabilities.",
    },
    "platform": {
        "label": "Core Platform, Integration, and Governance",
        "description": "Identity, gateway, contract validation, workflow, audit, and composition fabric.",
    },
    "commerce": {
        "label": "Advanced Commerce and Fulfillment",
        "description": "Checkout, order routing, payments, subscriptions, returns, and cross-border commerce.",
    },
    "content": {
        "label": "Product Content, Information, and Assets",
        "description": "Product information, digital assets, pricing, promotions, and content governance.",
    },
    "relationship": {
        "label": "Relationship, Support, and Marketing",
        "description": "Pipeline, support, notifications, customer segmentation, and loyalty capabilities.",
    },
    "intelligence": {
        "label": "Analytics, Business Intelligence, and Artificial Intelligence",
        "description": "Streaming analytics, search, forecasting, fraud, and predictive intelligence.",
    },
}


PBC_CATALOG: dict[str, dict] = {
    "gl_core": {
        "label": "General Ledger Core",
        "mesh": "finops",
        "description": "Immutable financial truth, journal orchestration, chart of accounts, and balances.",
        "apis": (
            "POST /journals",
            "GET /trial-balance",
            "GET /chart-of-accounts",
            "GET /ledger-events",
            "POST /ledger-projections",
            "POST /consensus-commits",
            "POST /schema-extensions",
            "GET /temporal-ledger",
            "POST /probabilistic-postings",
            "POST /continuous-close-snapshots",
            "POST /causal-scenarios",
            "POST /reconciliation-cases",
            "POST /semantic-documents",
            "POST /regulatory-rules",
            "POST /predictive-validations",
            "POST /audit-proofs",
            "POST /control-tests",
            "POST /ledger-federation-links",
            "POST /resilience-drills",
            "POST /carbon-execution-windows",
        ),
        "template": "general_ledger",
    },
    "ap_automation": {
        "label": "Accounts Payable Automation",
        "mesh": "finops",
        "description": "Vendor obligations, OCR intake, invoice matching, approval, and withholding.",
        "apis": (
            "POST /ap/vendors",
            "POST /ap/vendor-bank-accounts",
            "POST /ap/vendor-tax-profiles",
            "POST /ap/purchase-orders",
            "POST /ap/goods-receipts",
            "POST /ap/invoices",
            "POST /ap/invoices/{invoice_id}/match",
            "POST /ap/exceptions",
            "POST /ap/approval-tasks",
            "POST /ap/payment-schedules",
            "POST /ap/payment-batches",
            "POST /ap/payments",
            "POST /ap/e-invoices",
            "POST /ap/vendor-statements/reconcile",
            "GET /ap/workbench",
        ),
        "template": "accounts_payable",
    },
    "ar_credit": {
        "label": "Accounts Receivable and Credit",
        "mesh": "finops",
        "description": "Customer credit, receivables, invoicing, cash application, collections, revenue schedules, and AR controls.",
        "apis": (
            "POST /ar/customers",
            "POST /ar/invoices",
            "POST /ar/deliveries",
            "POST /ar/remittances/parse",
            "POST /ar/cash-applications",
            "POST /ar/unapplied-cash",
            "POST /ar/credit-memos",
            "POST /ar/write-offs",
            "POST /ar/refunds",
            "POST /ar/disputes",
            "POST /ar/collections",
            "POST /ar/e-invoices",
            "GET /ar/aging",
            "GET /ar/statements/{customer_id}",
            "GET /ar/revenue-schedules/{invoice_id}",
            "GET /ar/workbench",
        ),
        "template": "accounts_receivable",
    },
    "treasury_cash": {
        "label": "Treasury and Cash Management",
        "mesh": "finops",
        "description": "Multi-currency cash, bank connectivity, liquidity planning, funding, investments, debt, FX exposure, and treasury controls.",
        "apis": (
            "POST /treasury/bank-accounts",
            "POST /treasury/balances",
            "POST /treasury/statements",
            "POST /treasury/statements/{id}/reconcile",
            "GET /treasury/cash-position",
            "POST /treasury/forecasts",
            "POST /treasury/liquidity/optimize",
            "POST /treasury/payment-rails/route",
            "POST /treasury/investments",
            "POST /treasury/debt-draws",
            "POST /treasury/fx/hedge-recommendations",
            "POST /treasury/events/inbox",
            "GET /treasury/workbench",
        ),
        "template": None,
    },
    "asset_lifecycle": {
        "label": "Asset Lifecycle and Depreciation",
        "mesh": "finops",
        "description": "Fixed assets, acquisitions, books, depreciation, transfers, valuation, maintenance, insurance, retirement, verification, and asset controls.",
        "apis": (
            "POST /assets",
            "POST /assets/{asset_id}/service",
            "POST /assets/{asset_id}/depreciation-schedules",
            "POST /depreciation-runs",
            "POST /assets/{asset_id}/transfers",
            "POST /assets/{asset_id}/revaluations",
            "POST /assets/{asset_id}/impairments",
            "POST /assets/{asset_id}/maintenance-adjustments",
            "POST /assets/{asset_id}/retirements",
            "POST /assets/events/inbox",
            "GET /assets",
            "GET /assets/{asset_id}/risk",
        ),
        "template": None,
    },
    "tax_localization": {
        "label": "Tax Compliance and Localization",
        "mesh": "finops",
        "description": "Regional tax, product taxability, nexus, quote calculation, invoice tax, exemptions, duties, filings, remittance, and tax controls.",
        "apis": (
            "POST /tax/jurisdictions",
            "POST /tax/rules",
            "POST /tax/quotes",
            "POST /tax/invoices/{id}/tax-records",
            "POST /tax/filings",
            "POST /tax/events/inbox",
            "GET /tax/workbench",
        ),
        "template": None,
    },
    "inventory_positioning": {
        "label": "Inventory Positioning and State",
        "mesh": "scl",
        "description": "Inventory truth for items, nodes, lots, positions, receipts, adjustments, reservations, allocations, holds, in-transit projections, replenishment, and stock risk.",
        "apis": (
            "POST /inventory/items",
            "POST /inventory/nodes",
            "POST /inventory/receipts",
            "POST /inventory/adjustments",
            "GET /inventory/availability",
            "POST /inventory/allocations",
            "POST /inventory/allocations/{id}/release",
            "POST /inventory/quality-holds",
            "POST /inventory/events/inbox",
            "GET /inventory/workbench",
        ),
        "template": "inventory",
    },
    "wms_core": {
        "label": "Warehouse Management Core",
        "mesh": "scl",
        "description": "Putaway, picking, packing, cross-docking, and warehouse edge workflows.",
        "apis": ("POST /wms/warehouses", "POST /wms/inbound", "POST /wms/putaway", "POST /wms/pick-waves", "POST /wms/pack-tasks", "POST /wms/shipments", "GET /wms/workbench"),
        "template": "warehouse_management",
    },
    "procurement_sourcing": {
        "label": "Procurement and Strategic Sourcing",
        "mesh": "scl",
        "description": "Requisitions, RFQs, contracts, purchase orders, and vendor performance.",
        "apis": ("POST /procurement/requisitions", "POST /procurement/rfqs", "POST /procurement/rfqs/{id}/bids", "POST /procurement/awards", "POST /procurement/contracts", "POST /procurement/purchase-orders", "GET /procurement/workbench"),
        "template": "purchasing",
    },
    "transportation_management": {
        "label": "Transportation Management",
        "mesh": "scl",
        "description": "Freight routing, carrier choice, shipment tracking, telematics, and ETA updates.",
        "apis": ("POST /transportation/shipments", "POST /transportation/carriers", "POST /transportation/shipments/{id}/carrier-selection", "POST /transportation/routes", "POST /transportation/tracking-events", "POST /transportation/shipments/{id}/delivery", "GET /transportation/workbench"),
        "template": None,
    },
    "personnel_identity": {
        "label": "Personnel Directory and Identity",
        "mesh": "hcm",
        "description": "Workforce identity, organization topology, lifecycle, roles, attributes, assurance, provisioning, and policy evidence.",
        "apis": (
            "POST /personnel/departments",
            "POST /personnel/departments/{id}/hierarchy",
            "POST /personnel/employees",
            "POST /personnel/employees/{id}/contacts",
            "POST /personnel/employees/{id}/documents",
            "POST /personnel/employees/{id}/status",
            "POST /personnel/employees/{id}/roles",
            "POST /personnel/employees/{id}/attributes",
            "POST /personnel/employees/{id}/verification",
            "POST /personnel/employees/{id}/proofs",
            "POST /personnel/provisioning/routes",
            "POST /personnel/events/inbox",
            "POST /personnel/rules",
            "POST /personnel/parameters",
            "POST /personnel/configuration",
            "GET /personnel/org-chart",
            "GET /personnel/workbench",
        ),
        "template": "human_resources",
    },
    "time_labor": {
        "label": "Time Attendance and Labor Tracking",
        "mesh": "hcm",
        "description": "Schedules, clock events, time entries, absences, approvals, labor costing, payroll-ready summaries, and labor-risk evidence.",
        "apis": (
            "POST /shifts",
            "POST /shift-patterns",
            "POST /shift-swaps",
            "POST /clock-events",
            "POST /time-entries/calculate",
            "POST /absences",
            "POST /labor-summaries/{id}/approve",
            "POST /time/events/inbox",
            "POST /time/rules",
            "POST /time/parameters",
            "POST /time/configuration",
            "GET /labor-summaries",
            "GET /time-workbench",
        ),
        "template": None,
    },
    "payroll_engine": {
        "label": "Compensation and Payroll Engine",
        "mesh": "hcm",
        "description": "Gross-to-net payroll, worker pay profiles, earnings, deductions, benefits, filings, payment and journal handoffs, corrections, controls, and payroll-risk evidence.",
        "apis": (
            "POST /payroll-runs",
            "POST /payroll-runs/{id}/workers",
            "POST /payroll-runs/{id}/payslips",
            "POST /payslips/{id}/deductions",
            "POST /payslips/{id}/benefits",
            "POST /payroll-runs/{id}/post",
            "POST /payroll-filings",
            "POST /payroll/events/inbox",
            "POST /payroll-rules",
            "POST /payroll-parameters",
            "POST /payroll-configuration",
            "GET /payslips",
            "GET /payroll-workbench",
        ),
        "template": "payroll",
    },
    "talent_onboarding": {
        "label": "Talent Acquisition and Onboarding",
        "mesh": "hcm",
        "description": "Requisitions, sourcing, candidates, screening, interviews, offers, onboarding tasks, provisioning handoffs, controls, and talent-risk evidence.",
        "apis": (
            "POST /job-requisitions",
            "POST /job-requisitions/{id}/approvals",
            "POST /candidates",
            "POST /candidates/{id}/stage",
            "POST /interviews",
            "POST /background-checks",
            "POST /offers",
            "POST /offers/{id}/acceptance",
            "POST /onboarding/tasks",
            "POST /onboarding/provision",
            "POST /talent/events/inbox",
            "POST /talent-rules",
            "POST /talent-parameters",
            "POST /talent-configuration",
            "GET /talent-workbench",
        ),
        "template": None,
    },
    "mrp_engine": {
        "label": "Material Requirements Planning Engine",
        "mesh": "opsmfg",
        "description": "BOM graph analysis, demand/supply/capacity projections, planning runs, shortages, pegging, release routes, and governed material plans.",
        "apis": (
            "POST /mrp/boms",
            "POST /mrp/demand-projections",
            "POST /mrp/inventory-projections",
            "POST /mrp/runs",
            "POST /mrp/runs/{id}/calculate",
            "POST /mrp/planned-orders/{id}/release",
            "POST /mrp/events/inbox",
            "GET /mrp/workbench",
        ),
        "template": "manufacturing",
    },
    "production_control": {
        "label": "Production Scheduling and Floor Control",
        "mesh": "opsmfg",
        "description": "Routings, work centers, capacity, assembly sequencing, OEE, downtime, execution records, and completion evidence.",
        "apis": (
            "POST /production/work-centers",
            "POST /production/orders",
            "POST /production/routing-steps",
            "POST /production/orders/{id}/schedule",
            "POST /production/operations/{id}/start",
            "POST /production/material-consumptions",
            "POST /production/labor-time",
            "POST /production/machine-time",
            "POST /production/downtime",
            "POST /production/quality-gates",
            "POST /production/scrap-rework",
            "POST /production/operations/{id}/confirm",
            "POST /production/orders/{id}/complete",
            "POST /production/oee-snapshots",
            "POST /production/exception-cases",
            "POST /production/capacity-allocations",
            "POST /production/completion-proofs",
            "POST /production/audit-entries",
            "POST /production/events/inbox",
            "POST /production/rules",
            "POST /production/parameters",
            "POST /production/configuration",
            "GET /production/workbench",
            "GET /production/schema-contract",
            "GET /production/service-contract",
            "GET /production/release-evidence",
        ),
        "template": "manufacturing",
    },
    "quality_assurance": {
        "label": "Quality Assurance and Compliance",
        "mesh": "opsmfg",
        "description": "Inspection checklists, SPC sampling, non-conformance, and quality holds.",
        "apis": ("POST /inspections", "POST /non-conformances", "POST /quality-holds", "GET /quality-assurance-workbench"),
        "template": "quality_management",
    },
    "eam": {
        "label": "Enterprise Asset Management",
        "mesh": "opsmfg",
        "description": "Asset hierarchy, preventive and predictive maintenance, condition monitoring, work orders, safety permits, spares, vendor service, reliability analytics, and governed maintenance automation.",
        "apis": (
            "POST /equipment",
            "POST /maintenance-plans",
            "POST /work-orders",
            "POST /work-orders/{id}/schedule",
            "POST /work-orders/{id}/complete",
            "POST /condition-readings",
            "POST /meter-readings",
            "POST /spare-usage",
            "POST /safety-permits",
            "GET /maintenance-workbench",
            "POST /maintenance-rules",
            "POST /maintenance-parameters",
            "POST /maintenance-configuration",
        ),
        "template": None,
    },
    "dom": {
        "label": "Distributed Order Management",
        "mesh": "cx",
        "description": "Order verification, fraud screening, allocation, and fulfillment orchestration.",
        "apis": ("POST /dom/orders", "POST /dom/orders/{id}/verify", "POST /dom/orders/{id}/price", "POST /dom/orders/{id}/allocation", "POST /dom/fulfillment-plans", "POST /dom/shipments", "GET /dom/workbench"),
        "template": "sales",
    },
    "product_catalog_pim": {
        "label": "Enterprise Product Catalog and PIM",
        "mesh": "cx",
        "description": "Product schemas, pricing, localized descriptions, media, and read models.",
        "apis": ("POST /products", "GET /product-read-models", "POST /prices"),
        "template": "crm",
    },
    "customer_360": {
        "label": "Customer 360 and Engagement Registry",
        "mesh": "cx",
        "description": "Profiles, touchpoints, preferences, channel history, and customer read models.",
        "apis": ("POST /profiles", "POST /touchpoints", "GET /customer-timeline"),
        "template": "crm",
    },
}

PBC_CATALOG.update(
    {
        "federated_iam": {
            "label": "Federated Identity and Access Management",
            "mesh": "platform",
            "description": "Tenant, principal, identity provider, identity link, role, policy, token, session, credential verification, privileged access, rules, parameters, configuration, and AppGen-X identity event orchestration.",
            "apis": (
                "PUT /iam/configuration",
                "POST /iam/parameters",
                "POST /iam/rules",
                "POST /iam/schema-extensions",
                "POST /tenants",
                "POST /principals",
                "POST /identity-providers",
                "POST /identity-links",
                "POST /credential-verifications",
                "POST /role-assignments",
                "POST /policy-decisions",
                "POST /token-grants",
                "POST /privileged-access-requests",
                "POST /iam/events/inbox",
                "GET /iam-workbench",
                "GET /iam/schema-contract",
                "GET /iam/service-contract",
                "GET /iam/release-evidence",
            ),
            "template": None,
        },
        "api_gateway_mesh": {
            "label": "Dynamic API Gateway and Service Mesh",
            "mesh": "platform",
            "description": "Service registration, endpoint catalog, route publication, traffic policy, rate limiting, mTLS identity, health, telemetry, resilience, proofs, optimization, and AppGen-X gateway event orchestration.",
            "apis": (
                "POST /services",
                "POST /routes",
                "POST /rate-limits",
                "POST /mtls-identities",
                "POST /service-health",
                "POST /traffic-samples",
                "POST /gateway/events/inbox",
                "POST /gateway-rules",
                "POST /gateway-parameters",
                "POST /gateway-configuration",
                "GET /service-map",
                "GET /gateway/contracts/schema",
                "GET /gateway/contracts/service",
                "GET /gateway/release-evidence",
                "GET /gateway-workbench",
            ),
            "template": None,
        },
        "schema_registry": {
            "label": "Schema Registry and Contract Validation",
            "mesh": "platform",
            "description": "Contract-first subject catalog, schema versioning, compatibility gates, payload validation, impact analysis, projection publication, and governed schema evolution.",
            "apis": (
                "POST /schemas/subjects",
                "POST /schemas/versions",
                "POST /schemas/compatibility-rules",
                "POST /schemas/consumer-bindings",
                "POST /schemas/compatibility-checks",
                "POST /schemas/payload-validations",
                "POST /schemas/violations",
                "POST /schemas/projections",
                "POST /schemas/events/inbox",
                "GET /schemas/subjects",
                "GET /schemas/schema-contract",
                "GET /schemas/service-contract",
                "GET /schemas/release-evidence",
            ),
            "template": None,
        },
        "workflow_orchestration": {
            "label": "Distributed Workflow Orchestration Engine",
            "mesh": "platform",
            "description": "Workflow definitions, instances, signals, timers, sagas, compensations, human tasks, rules, parameters, configuration, AppGen-X eventing, and governed orchestration telemetry.",
            "apis": (
                "PUT /workflows/configuration",
                "POST /workflows/parameters",
                "POST /workflows/rules",
                "POST /workflows/definitions",
                "POST /workflows/versions",
                "POST /workflows/transition-guards",
                "POST /workflows/retry-policies",
                "POST /workflows/sla-policies",
                "POST /workflows/escalation-rules",
                "POST /workflows/instances",
                "POST /workflows/instances/{id}/signals",
                "POST /workflows/timers",
                "POST /workflows/instances/{id}/steps",
                "POST /workflows/instances/{id}/compensations",
                "POST /workflows/human-task-assignments",
                "POST /workflows/approval-decisions",
                "POST /workflows/integration-endpoints",
                "POST /workflows/event-correlations",
                "POST /workflows/metric-snapshots",
                "POST /workflows/exception-cases",
                "POST /workflows/simulation-runs",
                "POST /workflows/policy-screenings",
                "POST /workflows/completion-proofs",
                "POST /workflows/audit-entries",
                "POST /workflows/governed-model-evidence",
                "POST /workflows/events/inbox",
                "GET /workflows/workbench",
                "GET /workflows/schema-contract",
                "GET /workflows/service-contract",
                "GET /workflows/release-evidence",
            ),
            "template": None,
        },
        "audit_ledger": {
            "label": "Unified Audit Trail and Cryptographic Ledger",
            "mesh": "platform",
            "description": "Append-only signed mutation, security, and user-action evidence.",
            "apis": (
                "POST /audit-events",
                "POST /audit-events/access-evidence",
                "POST /audit-events/verify-chain",
                "POST /retention-policies",
                "POST /forensic-exports",
                "POST /control-assertions",
                "POST /audit-projections",
                "POST /audit-events/inbox",
                "GET /audit-workbench",
            ),
            "template": None,
        },
        "composition_engine": {
            "label": "Low-Code Composition Engine",
            "mesh": "platform",
            "description": "Drag-and-drop PBC assembly, component registry, layout engine, and experience composition.",
            "apis": (
                "POST /composition-workspaces",
                "POST /composition-workspaces/{id}/pbcs",
                "POST /component-registry",
                "POST /ui-fragments",
                "POST /layout-bindings",
                "POST /composition-plans/validate",
                "POST /package-registration-plans",
                "POST /composition-dsl",
                "POST /composition-publications",
                "POST /composition/events/inbox",
                "GET /composition-workbench",
                "GET /composition/schema-contract",
                "GET /composition/service-contract",
                "GET /composition/release-evidence",
            ),
            "template": None,
        },
        "global_inventory_visibility": {
            "label": "Global Inventory Visibility and Pool Management",
            "mesh": "commerce",
            "description": "Unified availability across locations, in-transit cargo, vendors, and third-party logistics.",
            "apis": ("GET /global-availability", "POST /pool-rules", "GET /supply-nodes"),
            "template": "inventory",
        },
        "order_routing_optimization": {
            "label": "Distributed Order Routing and Optimization",
            "mesh": "commerce",
            "description": "Fulfillment route optimization by distance, cost, tax, and node capacity.",
            "apis": ("POST /route-orders", "GET /route-candidates", "POST /capacity"),
            "template": "sales",
        },
        "checkout_processing": {
            "label": "Headless Cart and Checkout Processing",
            "mesh": "commerce",
            "description": "Cart state, pricing, promotions, coupons, and checkout persistence.",
            "apis": (
                "POST /carts",
                "POST /cart-lines",
                "POST /checkout",
                "POST /coupons",
                "POST /checkout/inventory-confirmations",
                "POST /checkout/payment-authorizations",
                "POST /checkout/payment-captures",
                "POST /checkout-processing/events/inbox",
                "GET /checkout-processing-workbench",
            ),
            "template": "sales",
        },
        "payment_orchestration": {
            "label": "Multi-Gateway Payment Orchestration",
            "mesh": "commerce",
            "description": "Gateway routing, fee optimization, localized checks, and payment token controls.",
            "apis": ("POST /payment-intents", "POST /gateway-routes", "POST /tokens", "GET /payment-orchestration-workbench"),
            "template": None,
        },
        "subscription_billing": {
            "label": "Subscription and Recurring Billing Management",
            "mesh": "commerce",
            "description": "Subscriptions, metering, dunning, renewals, and deferred revenue support.",
            "apis": ("POST /subscriptions", "POST /usage", "POST /renewals", "GET /subscription-billing-workbench"),
            "template": "invoicing",
        },
        "returns_reverse_logistics": {
            "label": "Returns RMA and Reverse Logistics",
            "mesh": "commerce",
            "description": "Return authorizations, labels, inspection grading, and credit adjustments.",
            "apis": ("POST /returns", "POST /labels", "POST /inspection-grades", "GET /returns-reverse-logistics-workbench"),
            "template": None,
        },
        "cross_border_trade": {
            "label": "Cross-Border Trade and Customs Compliance",
            "mesh": "commerce",
            "description": "HS code assignment, landed cost, export controls, and customs declarations.",
            "apis": ("POST /landed-cost", "POST /export-checks", "POST /declarations", "GET /cross-border-trade-workbench"),
            "template": None,
        },
        "multi_sided_market": {
            "label": "Multi-Sided Market Exchange",
            "mesh": "commerce",
            "description": "Participant, listing, exchange, booking, rental, loan, escrow, settlement, reputation, and dispute orchestration for goods and services.",
            "apis": (
                "POST /market/participants",
                "POST /market/listings",
                "POST /market/listing-assets",
                "POST /market/service-offers",
                "POST /market/availability-windows",
                "POST /market/trade-orders",
                "POST /market/barter-offers",
                "POST /market/exchange-proposals",
                "POST /market/sale-orders",
                "POST /market/bookings",
                "POST /market/rentals",
                "POST /market/loans",
                "POST /market/escrow",
                "POST /market/escrow-release-policies",
                "POST /market/escrow-releases",
                "POST /market/settlements",
                "POST /market/reputation-signals",
                "POST /market/disputes",
                "POST /market/dispute-resolutions",
                "POST /market/clearing-projections",
                "GET /market-workbench",
                "GET /market/exchange-match",
                "GET /market/counterfactual-terms",
                "GET /market/collusion-anomaly",
                "GET /market/reputation-proof",
                "GET /market/carbon-fulfillment",
            ),
            "template": "sales",
        },
        "enterprise_pim": {
            "label": "Enterprise Product Information Management",
            "mesh": "content",
            "description": "Taxonomies, multilingual attributes, inheritance, localization, validation, dependency projections, publication readiness, and master-data governance.",
            "apis": (
                "POST /product-taxonomies",
                "POST /product-attributes",
                "POST /localized-content",
                "POST /validation-workflows",
                "POST /validation-workflows/{id}/approve",
                "POST /dependency-schemas",
                "POST /pim-events",
                "POST /pim-publications",
                "GET /pim-workbench",
            ),
            "template": "crm",
        },
        "dam_core": {
            "label": "Digital Asset Management Core",
            "mesh": "content",
            "description": "Media storage, transformation, transcoding, metadata tagging, and rights controls.",
            "apis": ("POST /assets", "POST /renditions", "GET /rights"),
            "template": None,
        },
        "price_promotion_engine": {
            "label": "Dynamic Price Optimization and Promotion Engine",
            "mesh": "content",
            "description": "Context pricing, loyalty tiers, volume breaks, demand signals, and promotions.",
            "apis": ("POST /price-quotes", "POST /promotions", "GET /price-decisions"),
            "template": None,
        },
        "lead_opportunity": {
            "label": "Enterprise Lead and Opportunity Management",
            "mesh": "relationship",
            "description": "Pipeline, deal velocity, account hierarchy, and interaction history.",
            "apis": ("POST /leads", "POST /opportunities", "GET /pipeline"),
            "template": "crm",
        },
        "service_ticketing": {
            "label": "Customer Service Ticketing and SLA Orchestration",
            "mesh": "relationship",
            "description": "Omnichannel service case intake, queues, priorities, SLA policy, assignment, field handoff, customer updates, resolution, satisfaction, audit, automation, and governed service operations.",
            "apis": (
                "PUT /service-ticketing/configuration",
                "POST /service-ticketing/parameters",
                "POST /service-ticketing/rules",
                "POST /sla-policies",
                "POST /tickets",
                "POST /assignments",
                "POST /escalations",
                "POST /resolutions",
                "POST /service-ticketing/events/inbox",
                "GET /service-ticketing/workbench",
                "GET /service-ticketing/schema-contract",
                "GET /service-ticketing/service-contract",
                "GET /service-ticketing/release-evidence",
            ),
            "template": None,
        },
        "notifications": {
            "label": "Omni-Channel Communication and Notifications",
            "mesh": "relationship",
            "description": "Omnichannel templates, localized variants, channels, recipients, consent, schedules, throttles, provider routing, delivery lifecycle, campaigns, transactional notifications, audit, analytics, and governed notification operations.",
            "apis": (
                "POST /templates",
                "POST /delivery-channels",
                "POST /notifications/rules",
                "POST /notifications/parameters",
                "POST /notifications/configuration",
                "POST /messages",
                "POST /delivery-attempts",
                "POST /notifications/events/inbox",
                "GET /notifications/contracts/schema",
                "GET /notifications/contracts/service",
                "GET /notifications/release-evidence",
                "GET /notifications-workbench",
            ),
            "template": None,
        },
        "cdp_segmentation": {
            "label": "Customer Data Platform Segmentation",
            "mesh": "relationship",
            "description": "Clickstream, transactions, profiles, and real-time segment activation.",
            "apis": ("POST /events", "POST /segments", "GET /memberships"),
            "template": "crm",
        },
        "loyalty_rewards": {
            "label": "Customer Loyalty Points and Rewards",
            "mesh": "relationship",
            "description": "Rewards, tiers, point balances, earning rules, redemptions, referrals, partner accrual, liability, fraud controls, and reward intelligence.",
            "apis": (
                "POST /reward-accounts",
                "POST /points",
                "POST /points/adjustments",
                "POST /redemptions",
                "POST /tiers/qualification",
                "POST /referrals",
                "POST /partner-accruals",
                "POST /offers/eligibility",
                "POST /expirations/schedules",
                "POST /liability/snapshots",
                "POST /risk/fraud-reviews",
                "POST /risk/churn-scores",
                "POST /intelligence/breakage-forecasts",
                "POST /intelligence/offer-simulations",
                "POST /exceptions/resolutions",
                "POST /balances/reconciliations",
                "POST /balances/proofs",
                "POST /policy/screenings",
                "POST /liability/controls",
                "POST /federation/views",
                "POST /governed-models",
                "POST /loyalty-rewards/events/inbox",
                "GET /reward-accounts",
                "GET /loyalty-rewards/schema-contract",
                "GET /loyalty-rewards/service-contract",
                "GET /loyalty-rewards/release-evidence",
            ),
            "template": None,
        },
        "streaming_analytics": {
            "label": "Streaming Analytics and Real-Time Aggregation",
            "mesh": "intelligence",
            "description": "Operational metric streams, event ingestion, aggregation windows, KPI snapshots, dashboards, replay, quality, controls, forecasting, risk, and governed analytics models.",
            "apis": (
                "POST /metric-streams",
                "POST /aggregation-windows",
                "POST /metric-events",
                "POST /ingestion-checkpoints",
                "POST /quality/evaluations",
                "POST /replay-jobs",
                "POST /watermarks",
                "POST /retention-policies",
                "POST /threshold-alerts",
                "POST /forecasts",
                "POST /risk-scores",
                "POST /exceptions/resolutions",
                "POST /windows/recomputations",
                "POST /kpi-controls",
                "POST /snapshot-proofs",
                "POST /policy-screenings",
                "POST /federation-views",
                "POST /governed-models",
                "GET /kpis",
                "GET /projections",
                "GET /streaming-analytics/workbench",
                "GET /streaming-analytics/schema-contract",
                "GET /streaming-analytics/service-contract",
                "GET /streaming-analytics/release-evidence",
            ),
            "template": "reporting",
        },
        "enterprise_search_vector": {
            "label": "Enterprise Search and Vector Discovery",
            "mesh": "intelligence",
            "description": "Semantic search across products, customers, transactions, and knowledge sources.",
            "apis": (
                "POST /indexes",
                "POST /embeddings",
                "POST /search",
                "POST /ranking-simulations",
                "POST /quality-remediations",
                "GET /enterprise-search-vector-workbench",
            ),
            "template": None,
        },
        "predictive_demand": {
            "label": "Predictive Demand Forecasting",
            "mesh": "intelligence",
            "description": "Time-series prediction for demand, depletion, cash flow, and resource constraints.",
            "apis": (
                "POST /forecast-models",
                "POST /forecast-runs",
                "POST /demand-signals",
                "POST /forecast-results",
                "POST /planning-horizons",
                "POST /forecast-drivers",
                "POST /consensus-adjustments",
                "POST /scenario-versions",
                "POST /shortage-risks",
                "POST /replenishment-recommendations",
                "POST /forecast-exceptions",
                "POST /forecast-exceptions/resolve",
                "POST /model-drift-signals",
                "POST /governed-model-evidence",
                "POST /forecast-audit-proofs",
                "POST /predictive-demand/events/inbox",
                "GET /forecast-results",
                "GET /predictive-demand/schema-contract",
                "GET /predictive-demand/service-contract",
                "GET /predictive-demand/release-evidence",
            ),
            "template": None,
        },
        "fraud_anomaly_detection": {
            "label": "Anomalous Activity and Fraud Detection",
            "mesh": "intelligence",
            "description": "Behavior baselines, identity graph risk, anomaly scores, fraud rules, decision explanations, loss exposure, analyst queues, and operational risk flags.",
            "apis": (
                "POST /risk-events",
                "POST /fraud-checks",
                "GET /risk-cases",
                "GET /risk-workbench",
                "POST /fraud-rules",
                "POST /risk-signals/{id}/score",
                "POST /risk-cases",
                "POST /fraud-configuration",
                "POST /fraud-parameters",
            ),
            "template": None,
        },
    }
)

# High-value enterprise extension PBCs proposed for the AppGen-X market expansion.
PBC_CATALOG.update(
    {'contract_lifecycle': {'label': 'Contract Lifecycle Management',
                        'mesh': 'relationship',
                        'description': 'Contract authoring, clauses, obligations, approvals, renewals, risk scoring, '
                                       'documents, and transaction events.',
                        'apis': ('POST /contracts',
                                 'POST /contracts/{id}/clauses',
                                 'POST /contracts/{id}/obligations',
                                 'POST /contracts/{id}/approvals',
                                 'POST /contracts/{id}/renewals',
                                 'GET /contract-lifecycle-workbench'),
                        'template': 'workflow',
},
 'vendor_supplier_360': {'label': 'Vendor and Supplier 360',
                         'mesh': 'scl',
                         'description': 'Supplier master, onboarding, qualification, certifications, bank validation, '
                                        'ESG data, risk, and scorecards.',
                         'apis': ('POST /suppliers',
                                  'POST /suppliers/{id}/sites',
                                  'POST /suppliers/{id}/certifications',
                                  'POST /suppliers/{id}/bank-validations',
                                  'GET /supplier-360-workbench'),
                         'template': 'procurement',
},
 'enterprise_risk_controls': {'label': 'Enterprise Risk and Controls',
                              'mesh': 'platform',
                              'description': 'Risk registers, control libraries, attestations, control testing, issue '
                                             'remediation, evidence, and policy mapping.',
                              'apis': ('POST /risks',
                                       'POST /controls',
                                       'POST /control-tests',
                                       'POST /attestations',
                                       'POST /remediations',
                                       'GET /risk-controls-workbench'),
                              'template': None,
},
 'planning_budgeting_forecasting': {'label': 'Planning Budgeting and Forecasting',
                                    'mesh': 'finops',
                                    'description': 'Budgets, forecasts, scenarios, driver models, allocations, '
                                                   'approvals, variance analytics, and rolling plans.',
                                    'apis': ('POST /plans',
                                             'POST /budgets',
                                             'POST /forecasts',
                                             'POST /scenarios',
                                             'POST /variance-analyses',
                                             'GET /planning-workbench'),
                                    'template': 'reporting',
},
 'revenue_recognition': {'label': 'Revenue Recognition',
                         'mesh': 'finops',
                         'description': 'Performance obligations, contract modifications, allocation rules, revenue '
                                        'schedules, compliance evidence, and GL posting events.',
                         'apis': ('POST /revenue-contracts',
                                  'POST /performance-obligations',
                                  'POST /revenue-schedules',
                                  'POST /recognition-runs',
                                  'GET /revenue-recognition-workbench'),
                         'template': 'invoicing',
},
 'expense_management': {'label': 'Expense Management',
                        'mesh': 'finops',
                        'description': 'Employee expenses, receipts, card feeds, policies, approvals, reimbursements, '
                                       'fraud checks, and AP/GL events.',
                        'apis': ('POST /expense-reports',
                                 'POST /expense-lines',
                                 'POST /receipt-documents',
                                 'POST /expense-approvals',
                                 'GET /expense-workbench'),
                        'template': 'workflow',
},
 'travel_management': {'label': 'Travel Management',
                       'mesh': 'hcm',
                       'description': 'Travel requests, bookings, itineraries, policy compliance, duty of care, '
                                      'expense handoff, supplier feeds, and carbon tracking.',
                       'apis': ('POST /travel-requests',
                                'POST /travel-bookings',
                                'POST /itineraries',
                                'POST /policy-checks',
                                'GET /travel-workbench'),
                       'template': 'workflow',
},
 'grant_fund_accounting': {'label': 'Grant and Fund Accounting',
                           'mesh': 'finops',
                           'description': 'Restricted funds, grant budgets, donor rules, allowable costs, '
                                          'reimbursement claims, compliance reporting, and audit trails.',
                           'apis': ('POST /grant-awards',
                                    'POST /fund-restrictions',
                                    'POST /grant-budgets',
                                    'POST /reimbursement-claims',
                                    'GET /grant-fund-workbench'),
                           'template': 'accounting',
},
 'project_portfolio_management': {'label': 'Project Portfolio Management',
                                  'mesh': 'opsmfg',
                                  'description': 'Projects, programs, milestones, budgets, resources, risks, '
                                                 'dependencies, benefits tracking, and portfolio prioritization.',
                                  'apis': ('POST /portfolios',
                                           'POST /programs',
                                           'POST /projects',
                                           'POST /milestones',
                                           'POST /benefits',
                                           'GET /portfolio-workbench'),
                                  'template': 'project',
},
 'professional_services_automation': {'label': 'Professional Services Automation',
                                      'mesh': 'relationship',
                                      'description': 'Engagements, scopes, staffing, time, billing milestones, '
                                                     'utilization, project margin, and client delivery workflows.',
                                      'apis': ('POST /engagements',
                                               'POST /statements-of-work',
                                               'POST /staffing',
                                               'POST /billing-milestones',
                                               'GET /services-automation-workbench'),
                                      'template': 'project',
},
 'field_service_management': {'label': 'Field Service Management',
                              'mesh': 'opsmfg',
                              'description': 'Work orders, dispatch, technicians, mobile tasks, parts usage, SLA '
                                             'tracking, service history, and customer updates.',
                              'apis': ('POST /field-work-orders',
                                       'POST /dispatch-assignments',
                                       'POST /mobile-tasks',
                                       'POST /parts-usage',
                                       'GET /field-service-workbench'),
                              'template': 'service',
},
 'customer_success_management': {'label': 'Customer Success Management',
                                 'mesh': 'relationship',
                                 'description': 'Health scores, onboarding plans, adoption telemetry, renewals, '
                                                'expansion signals, playbooks, and churn risk workflows.',
                                 'apis': ('POST /success-accounts',
                                          'POST /health-scores',
                                          'POST /onboarding-plans',
                                          'POST /renewal-plans',
                                          'GET /customer-success-workbench'),
                                 'template': 'crm',
},
 'case_knowledge_management': {'label': 'Case and Knowledge Management',
                               'mesh': 'relationship',
                               'description': 'Knowledge articles, semantic search, case deflection, authoring '
                                              'workflows, approvals, content freshness, and agent-assist guidance.',
                               'apis': ('POST /support-cases',
                                        'POST /knowledge-articles',
                                        'POST /article-approvals',
                                        'POST /case-deflections',
                                        'GET /knowledge-workbench'),
                               'template': 'service',
},
 'privacy_consent_governance': {'label': 'Privacy Consent Governance',
                                'mesh': 'platform',
                                'description': 'Data subject rights, consent, retention policies, processing purposes, '
                                               'disclosure logs, impact assessments, and compliance evidence.',
                                'apis': ('POST /privacy-requests',
                                         'POST /consents',
                                         'POST /processing-purposes',
                                         'POST /retention-policies',
                                         'GET /privacy-governance-workbench'),
                                'template': None,
},
 'data_product_catalog': {'label': 'Data Product Catalog',
                          'mesh': 'platform',
                          'description': 'Data products, ownership, contracts, quality SLAs, lineage, access requests, '
                                         'governance rules, and publication workflows.',
                          'apis': ('POST /data-products',
                                   'POST /data-contracts',
                                   'POST /quality-slas',
                                   'POST /access-requests',
                                   'GET /data-product-catalog-workbench'),
                          'template': None,
},
 'master_data_governance': {'label': 'Master Data Governance',
                            'mesh': 'platform',
                            'description': 'Golden records, stewardship workflows, match and merge, validation rules, '
                                           'survivorship, change approvals, and downstream sync events.',
                            'apis': ('POST /master-records',
                                     'POST /match-candidates',
                                     'POST /merge-decisions',
                                     'POST /stewardship-tasks',
                                     'GET /master-data-workbench'),
                            'template': None,
},
 'sustainability_esg_reporting': {'label': 'Sustainability ESG Reporting',
                                  'mesh': 'finops',
                                  'description': 'Emissions factors, activity data, carbon ledgers, ESG metrics, '
                                                 'assurance evidence, supplier disclosures, and regulatory reporting.',
                                  'apis': ('POST /emissions-factors',
                                           'POST /activity-data',
                                           'POST /carbon-ledger',
                                           'POST /sustainability-reports',
                                           'GET /esg-workbench'),
                                  'template': 'reporting',
},
 'facilities_space_management': {'label': 'Facilities and Space Management',
                                 'mesh': 'opsmfg',
                                 'description': 'Sites, buildings, rooms, occupancy, reservations, maintenance links, '
                                                'lease metadata, space planning, and utilization analytics.',
                                 'apis': ('POST /facility-sites',
                                          'POST /buildings',
                                          'POST /spaces',
                                          'POST /space-reservations',
                                          'GET /facilities-workbench'),
                                 'template': 'asset',
},
 'legal_matter_management': {'label': 'Legal Matter Management',
                             'mesh': 'relationship',
                             'description': 'Matters, outside counsel, budgets, documents, deadlines, holds, invoices, '
                                            'outcomes, and legal risk dashboards.',
                             'apis': ('POST /legal-matters',
                                      'POST /outside-counsel',
                                      'POST /matter-budgets',
                                      'POST /legal-holds',
                                      'GET /legal-matter-workbench'),
                             'template': 'workflow',
},
 'insurance_claims_policy': {'label': 'Insurance Claims and Policy',
                             'mesh': 'finops',
                             'description': 'Policies, claims intake, coverage validation, reserves, adjuster '
                                            'workflows, fraud signals, settlement, and audit evidence.',
                             'apis': ('POST /insurance-policies',
                                      'POST /claims',
                                      'POST /coverage-validations',
                                      'POST /claim-settlements',
                                      'GET /insurance-workbench'),
                             'template': 'workflow',
}}
)

IMPLEMENTED_PBC_KEYS = (
    *IMPLEMENTED_PBC_KEYS,
    'contract_lifecycle',
    'vendor_supplier_360',
    'enterprise_risk_controls',
    'planning_budgeting_forecasting',
    'revenue_recognition',
    'expense_management',
    'travel_management',
    'grant_fund_accounting',
    'project_portfolio_management',
    'professional_services_automation',
    'field_service_management',
    'customer_success_management',
    'case_knowledge_management',
    'privacy_consent_governance',
    'data_product_catalog',
    'master_data_governance',
    'sustainability_esg_reporting',
    'facilities_space_management',
    'legal_matter_management',
    'insurance_claims_policy',
)


# Broad industry coverage PBCs screened for overlap against the existing catalog.
PBC_INDUSTRY_EXPANSION_CANDIDATES = ('clinical_care_coordination',
 'claims_adjudication_healthcare',
 'pharmacy_benefits_management',
 'banking_core_accounts',
 'lending_origination_servicing',
 'insurance_underwriting',
 'capital_markets_trading_ops',
 'energy_grid_operations',
 'utilities_metering_billing',
 'telecom_network_operations',
 'telecom_subscription_lifecycle',
 'real_estate_property_management',
 'construction_project_controls',
 'hospitality_property_operations',
 'restaurant_operations',
 'agriculture_farm_operations',
 'mining_operations_management',
 'oil_gas_field_operations',
 'airline_operations_control',
 'port_terminal_operations',
 'public_sector_case_management',
 'education_student_lifecycle',
 'research_grants_management',
 'media_rights_content_monetization',
 'advertising_campaign_operations',
 'cybersecurity_operations_center',
 'it_service_management',
 'environment_health_safety',
 'donor_grant_fundraising',
 'fleet_mobility_operations',
 'provider_revenue_cycle',
 'electronic_health_records_core',
 'clinical_trials_management',
 'laboratory_information_management',
 'medical_device_lifecycle',
 'bank_payments_clearing',
 'wealth_portfolio_management',
 'trade_finance_operations',
 'mortgage_servicing',
 'lease_lending_equipment_finance',
 'policy_administration_insurance',
 'reinsurance_management',
 'actuarial_pricing_reserving',
 'utility_outage_restoration',
 'energy_trading_risk',
 'renewables_asset_operations',
 'water_wastewater_operations',
 'waste_recycling_operations',
 'rail_operations_management',
 'maritime_shipping_operations',
 'aviation_maintenance_repair',
 'airport_operations_management',
 'smart_city_mobility_operations',
 'construction_contracts_commercials',
 'building_information_modeling_ops',
 'capital_projects_delivery',
 'land_real_estate_development',
 'facility_energy_management',
 'hotel_revenue_management',
 'gaming_casino_operations',
 'sports_venue_event_operations',
 'media_production_management',
 'music_royalties_rights',
 'publishing_editorial_operations',
 'agri_supply_chain_traceability',
 'livestock_herd_management',
 'food_safety_quality_compliance',
 'mining_safety_permits',
 'chemical_batch_compliance',
 'pharma_manufacturing_quality',
 'public_safety_dispatch',
 'court_case_management',
 'tax_administration_public_sector',
 'permitting_licensing_inspections',
 'student_financial_aid',
 'library_archives_management',
 'nonprofit_program_impact',
 'humanitarian_relief_operations',
 'defense_readiness_logistics',
 'identity_kyc_aml_compliance')

PBC_INDUSTRY_EXPANSION_OVERLAP_DECISIONS = {'actuarial_pricing_reserving': {'adjacent_existing_pbc': None,
                                 'decision': 'create_new_pbc',
                                 'rationale': 'bounded context is distinct from existing PBCs'},
 'advertising_campaign_operations': {'adjacent_existing_pbc': None,
                                     'decision': 'create_new_pbc',
                                     'rationale': 'bounded context is distinct from existing PBCs'},
 'agri_supply_chain_traceability': {'adjacent_existing_pbc': None,
                                    'decision': 'create_new_pbc',
                                    'rationale': 'bounded context is distinct from existing PBCs'},
 'agriculture_farm_operations': {'adjacent_existing_pbc': None,
                                 'decision': 'create_new_pbc',
                                 'rationale': 'bounded context is distinct from existing PBCs'},
 'airline_operations_control': {'adjacent_existing_pbc': None,
                                'decision': 'create_new_pbc',
                                'rationale': 'bounded context is distinct from existing PBCs'},
 'airport_operations_management': {'adjacent_existing_pbc': None,
                                   'decision': 'create_new_pbc',
                                   'rationale': 'bounded context is distinct from existing PBCs'},
 'aviation_maintenance_repair': {'adjacent_existing_pbc': 'eam',
                                 'decision': 'create_new_pbc',
                                 'rationale': 'aviation airworthiness and MRO compliance is a regulated vertical specialization'},
 'bank_payments_clearing': {'adjacent_existing_pbc': 'payment_orchestration',
                            'decision': 'create_new_pbc',
                            'rationale': 'bank clearing/settlement operations are separate from commerce payment orchestration'},
 'banking_core_accounts': {'adjacent_existing_pbc': None,
                           'decision': 'create_new_pbc',
                           'rationale': 'bounded context is distinct from existing PBCs'},
 'building_information_modeling_ops': {'adjacent_existing_pbc': None,
                                       'decision': 'create_new_pbc',
                                       'rationale': 'bounded context is distinct from existing PBCs'},
 'capital_markets_trading_ops': {'adjacent_existing_pbc': None,
                                 'decision': 'create_new_pbc',
                                 'rationale': 'bounded context is distinct from existing PBCs'},
 'capital_projects_delivery': {'adjacent_existing_pbc': None,
                               'decision': 'create_new_pbc',
                               'rationale': 'bounded context is distinct from existing PBCs'},
 'chemical_batch_compliance': {'adjacent_existing_pbc': None,
                               'decision': 'create_new_pbc',
                               'rationale': 'bounded context is distinct from existing PBCs'},
 'claims_adjudication_healthcare': {'adjacent_existing_pbc': 'insurance_claims_policy',
                                    'decision': 'create_new_pbc',
                                    'rationale': 'health claims/payer adjudication is separate from insurance policy and P&C claims '
                                                 'operations'},
 'clinical_care_coordination': {'adjacent_existing_pbc': None,
                                'decision': 'create_new_pbc',
                                'rationale': 'bounded context is distinct from existing PBCs'},
 'clinical_trials_management': {'adjacent_existing_pbc': None,
                                'decision': 'create_new_pbc',
                                'rationale': 'bounded context is distinct from existing PBCs'},
 'construction_contracts_commercials': {'adjacent_existing_pbc': 'contract_lifecycle',
                                        'decision': 'create_new_pbc',
                                        'rationale': 'construction pay applications, retainage, claims, and lien waivers are vertical '
                                                     'commercial controls'},
 'construction_project_controls': {'adjacent_existing_pbc': None,
                                   'decision': 'create_new_pbc',
                                   'rationale': 'bounded context is distinct from existing PBCs'},
 'court_case_management': {'adjacent_existing_pbc': None,
                           'decision': 'create_new_pbc',
                           'rationale': 'bounded context is distinct from existing PBCs'},
 'cybersecurity_operations_center': {'adjacent_existing_pbc': None,
                                     'decision': 'create_new_pbc',
                                     'rationale': 'bounded context is distinct from existing PBCs'},
 'defense_readiness_logistics': {'adjacent_existing_pbc': None,
                                 'decision': 'create_new_pbc',
                                 'rationale': 'bounded context is distinct from existing PBCs'},
 'donor_grant_fundraising': {'adjacent_existing_pbc': None,
                             'decision': 'create_new_pbc',
                             'rationale': 'bounded context is distinct from existing PBCs'},
 'education_student_lifecycle': {'adjacent_existing_pbc': None,
                                 'decision': 'create_new_pbc',
                                 'rationale': 'bounded context is distinct from existing PBCs'},
 'electronic_health_records_core': {'adjacent_existing_pbc': None,
                                    'decision': 'create_new_pbc',
                                    'rationale': 'bounded context is distinct from existing PBCs'},
 'energy_grid_operations': {'adjacent_existing_pbc': None,
                            'decision': 'create_new_pbc',
                            'rationale': 'bounded context is distinct from existing PBCs'},
 'energy_trading_risk': {'adjacent_existing_pbc': None,
                         'decision': 'create_new_pbc',
                         'rationale': 'bounded context is distinct from existing PBCs'},
 'environment_health_safety': {'adjacent_existing_pbc': 'sustainability_esg_reporting',
                               'decision': 'create_new_pbc',
                               'rationale': 'EHS incidents and permits are operational controls; ESG reporting consumes summarized '
                                            'evidence'},
 'facility_energy_management': {'adjacent_existing_pbc': 'facilities_space_management',
                                'decision': 'create_new_pbc',
                                'rationale': 'energy optimization is separate from occupancy and space operations'},
 'fleet_mobility_operations': {'adjacent_existing_pbc': None,
                               'decision': 'create_new_pbc',
                               'rationale': 'bounded context is distinct from existing PBCs'},
 'food_safety_quality_compliance': {'adjacent_existing_pbc': None,
                                    'decision': 'create_new_pbc',
                                    'rationale': 'bounded context is distinct from existing PBCs'},
 'gaming_casino_operations': {'adjacent_existing_pbc': None,
                              'decision': 'create_new_pbc',
                              'rationale': 'bounded context is distinct from existing PBCs'},
 'hospitality_property_operations': {'adjacent_existing_pbc': None,
                                     'decision': 'create_new_pbc',
                                     'rationale': 'bounded context is distinct from existing PBCs'},
 'hotel_revenue_management': {'adjacent_existing_pbc': None,
                              'decision': 'create_new_pbc',
                              'rationale': 'bounded context is distinct from existing PBCs'},
 'humanitarian_relief_operations': {'adjacent_existing_pbc': None,
                                    'decision': 'create_new_pbc',
                                    'rationale': 'bounded context is distinct from existing PBCs'},
 'identity_kyc_aml_compliance': {'adjacent_existing_pbc': 'federated_iam',
                                 'decision': 'create_new_pbc',
                                 'rationale': 'KYC/AML customer compliance is separate from platform identity access management'},
 'insurance_underwriting': {'adjacent_existing_pbc': None,
                            'decision': 'create_new_pbc',
                            'rationale': 'bounded context is distinct from existing PBCs'},
 'it_service_management': {'adjacent_existing_pbc': None,
                           'decision': 'create_new_pbc',
                           'rationale': 'bounded context is distinct from existing PBCs'},
 'laboratory_information_management': {'adjacent_existing_pbc': None,
                                       'decision': 'create_new_pbc',
                                       'rationale': 'bounded context is distinct from existing PBCs'},
 'land_real_estate_development': {'adjacent_existing_pbc': None,
                                  'decision': 'create_new_pbc',
                                  'rationale': 'bounded context is distinct from existing PBCs'},
 'lease_lending_equipment_finance': {'adjacent_existing_pbc': None,
                                     'decision': 'create_new_pbc',
                                     'rationale': 'bounded context is distinct from existing PBCs'},
 'lending_origination_servicing': {'adjacent_existing_pbc': None,
                                   'decision': 'create_new_pbc',
                                   'rationale': 'bounded context is distinct from existing PBCs'},
 'library_archives_management': {'adjacent_existing_pbc': None,
                                 'decision': 'create_new_pbc',
                                 'rationale': 'bounded context is distinct from existing PBCs'},
 'livestock_herd_management': {'adjacent_existing_pbc': None,
                               'decision': 'create_new_pbc',
                               'rationale': 'bounded context is distinct from existing PBCs'},
 'maritime_shipping_operations': {'adjacent_existing_pbc': None,
                                  'decision': 'create_new_pbc',
                                  'rationale': 'bounded context is distinct from existing PBCs'},
 'media_production_management': {'adjacent_existing_pbc': None,
                                 'decision': 'create_new_pbc',
                                 'rationale': 'bounded context is distinct from existing PBCs'},
 'media_rights_content_monetization': {'adjacent_existing_pbc': None,
                                       'decision': 'create_new_pbc',
                                       'rationale': 'bounded context is distinct from existing PBCs'},
 'medical_device_lifecycle': {'adjacent_existing_pbc': None,
                              'decision': 'create_new_pbc',
                              'rationale': 'bounded context is distinct from existing PBCs'},
 'mining_operations_management': {'adjacent_existing_pbc': None,
                                  'decision': 'create_new_pbc',
                                  'rationale': 'bounded context is distinct from existing PBCs'},
 'mining_safety_permits': {'adjacent_existing_pbc': None,
                           'decision': 'create_new_pbc',
                           'rationale': 'bounded context is distinct from existing PBCs'},
 'mortgage_servicing': {'adjacent_existing_pbc': None,
                        'decision': 'create_new_pbc',
                        'rationale': 'bounded context is distinct from existing PBCs'},
 'music_royalties_rights': {'adjacent_existing_pbc': None,
                            'decision': 'create_new_pbc',
                            'rationale': 'bounded context is distinct from existing PBCs'},
 'nonprofit_program_impact': {'adjacent_existing_pbc': None,
                              'decision': 'create_new_pbc',
                              'rationale': 'bounded context is distinct from existing PBCs'},
 'oil_gas_field_operations': {'adjacent_existing_pbc': None,
                              'decision': 'create_new_pbc',
                              'rationale': 'bounded context is distinct from existing PBCs'},
 'permitting_licensing_inspections': {'adjacent_existing_pbc': None,
                                      'decision': 'create_new_pbc',
                                      'rationale': 'bounded context is distinct from existing PBCs'},
 'pharma_manufacturing_quality': {'adjacent_existing_pbc': None,
                                  'decision': 'create_new_pbc',
                                  'rationale': 'bounded context is distinct from existing PBCs'},
 'pharmacy_benefits_management': {'adjacent_existing_pbc': None,
                                  'decision': 'create_new_pbc',
                                  'rationale': 'bounded context is distinct from existing PBCs'},
 'policy_administration_insurance': {'adjacent_existing_pbc': None,
                                     'decision': 'create_new_pbc',
                                     'rationale': 'bounded context is distinct from existing PBCs'},
 'port_terminal_operations': {'adjacent_existing_pbc': None,
                              'decision': 'create_new_pbc',
                              'rationale': 'bounded context is distinct from existing PBCs'},
 'provider_revenue_cycle': {'adjacent_existing_pbc': None,
                            'decision': 'create_new_pbc',
                            'rationale': 'bounded context is distinct from existing PBCs'},
 'public_safety_dispatch': {'adjacent_existing_pbc': None,
                            'decision': 'create_new_pbc',
                            'rationale': 'bounded context is distinct from existing PBCs'},
 'public_sector_case_management': {'adjacent_existing_pbc': None,
                                   'decision': 'create_new_pbc',
                                   'rationale': 'bounded context is distinct from existing PBCs'},
 'publishing_editorial_operations': {'adjacent_existing_pbc': None,
                                     'decision': 'create_new_pbc',
                                     'rationale': 'bounded context is distinct from existing PBCs'},
 'rail_operations_management': {'adjacent_existing_pbc': None,
                                'decision': 'create_new_pbc',
                                'rationale': 'bounded context is distinct from existing PBCs'},
 'real_estate_property_management': {'adjacent_existing_pbc': None,
                                     'decision': 'create_new_pbc',
                                     'rationale': 'bounded context is distinct from existing PBCs'},
 'reinsurance_management': {'adjacent_existing_pbc': None,
                            'decision': 'create_new_pbc',
                            'rationale': 'bounded context is distinct from existing PBCs'},
 'renewables_asset_operations': {'adjacent_existing_pbc': None,
                                 'decision': 'create_new_pbc',
                                 'rationale': 'bounded context is distinct from existing PBCs'},
 'research_grants_management': {'adjacent_existing_pbc': 'grant_fund_accounting',
                                'decision': 'create_new_pbc',
                                'rationale': 'pre-award/post-award research administration is separate from restricted fund accounting'},
 'restaurant_operations': {'adjacent_existing_pbc': None,
                           'decision': 'create_new_pbc',
                           'rationale': 'bounded context is distinct from existing PBCs'},
 'smart_city_mobility_operations': {'adjacent_existing_pbc': None,
                                    'decision': 'create_new_pbc',
                                    'rationale': 'bounded context is distinct from existing PBCs'},
 'sports_venue_event_operations': {'adjacent_existing_pbc': None,
                                   'decision': 'create_new_pbc',
                                   'rationale': 'bounded context is distinct from existing PBCs'},
 'student_financial_aid': {'adjacent_existing_pbc': None,
                           'decision': 'create_new_pbc',
                           'rationale': 'bounded context is distinct from existing PBCs'},
 'tax_administration_public_sector': {'adjacent_existing_pbc': None,
                                      'decision': 'create_new_pbc',
                                      'rationale': 'bounded context is distinct from existing PBCs'},
 'telecom_network_operations': {'adjacent_existing_pbc': None,
                                'decision': 'create_new_pbc',
                                'rationale': 'bounded context is distinct from existing PBCs'},
 'telecom_subscription_lifecycle': {'adjacent_existing_pbc': None,
                                    'decision': 'create_new_pbc',
                                    'rationale': 'bounded context is distinct from existing PBCs'},
 'trade_finance_operations': {'adjacent_existing_pbc': None,
                              'decision': 'create_new_pbc',
                              'rationale': 'bounded context is distinct from existing PBCs'},
 'utilities_metering_billing': {'adjacent_existing_pbc': None,
                                'decision': 'create_new_pbc',
                                'rationale': 'bounded context is distinct from existing PBCs'},
 'utility_outage_restoration': {'adjacent_existing_pbc': None,
                                'decision': 'create_new_pbc',
                                'rationale': 'bounded context is distinct from existing PBCs'},
 'waste_recycling_operations': {'adjacent_existing_pbc': None,
                                'decision': 'create_new_pbc',
                                'rationale': 'bounded context is distinct from existing PBCs'},
 'water_wastewater_operations': {'adjacent_existing_pbc': None,
                                 'decision': 'create_new_pbc',
                                 'rationale': 'bounded context is distinct from existing PBCs'},
 'wealth_portfolio_management': {'adjacent_existing_pbc': None,
                                 'decision': 'create_new_pbc',
                                 'rationale': 'bounded context is distinct from existing PBCs'}}

PBC_CATALOG.update(
{'actuarial_pricing_reserving': {
                                 'apis': ('POST /rating-models',
                                          'POST /actuarial-assumptions',
                                          'POST /experience-studys',
                                          'POST /reserve-estimates',
                                          'POST /loss-triangles',
                                          'GET /actuarial-pricing-reserving-workbench'),
                                 'description': 'Rating models, assumptions, experience studies, reserves, loss '
                                                'triangles, capital scenarios, and actuarial controls',
                                 'label': 'Actuarial Pricing and Reserving',
                                 'mesh': 'finops',
                                 'template': 'reporting',
},
 'advertising_campaign_operations': {
                                     'apis': ('POST /ad-campaigns',
                                              'POST /audience-segments',
                                              'POST /media-placements',
                                              'POST /creative-assets',
                                              'POST /campaign-budgets',
                                              'GET /advertising-campaign-operations-workbench'),
                                     'description': 'Campaigns, budgets, audiences, placements, creative approvals, '
                                                    'performance, billing, and optimization',
                                     'label': 'Advertising Campaign Operations',
                                     'mesh': 'relationship',
                                     'template': 'workflow',
},
 'agri_supply_chain_traceability': {
                                    'apis': ('POST /farm-lots',
                                             'POST /input-batchs',
                                             'POST /certifications',
                                             'POST /storage-events',
                                             'POST /transport-legs',
                                             'GET /agri-supply-chain-traceability-workbench'),
                                    'description': 'Farm lots, inputs, certifications, storage, transport, recalls, '
                                                   'provenance, and food traceability',
                                    'label': 'Agriculture Supply Chain Traceability',
                                    'mesh': 'scl',
                                    'template': 'logistics',
},
 'agriculture_farm_operations': {
                                 'apis': ('POST /fields',
                                          'POST /crop-plans',
                                          'POST /input-applications',
                                          'POST /irrigation-events',
                                          'POST /equipment-uses',
                                          'GET /agriculture-farm-operations-workbench'),
                                 'description': 'Fields, crops, inputs, equipment, irrigation, harvest, yield, '
                                                'certifications, and farm compliance',
                                 'label': 'Agriculture Farm Operations',
                                 'mesh': 'opsmfg',
                                 'template': 'asset',
},
 'airline_operations_control': {
                                'apis': ('POST /flight-legs',
                                         'POST /aircraft-rotations',
                                         'POST /crew-pairings',
                                         'POST /disruption-events',
                                         'POST /reaccommodation-plans',
                                         'GET /airline-operations-control-workbench'),
                                'description': 'Fleet rotations, crew legality, disruptions, passenger '
                                               'reaccommodation, operational control, and recovery planning',
                                'label': 'Airline Operations Control',
                                'mesh': 'opsmfg',
                                'template': 'asset',
},
 'airport_operations_management': {
                                   'apis': ('POST /gate-assignments',
                                            'POST /stand-allocations',
                                            'POST /slots',
                                            'POST /turndown-tasks',
                                            'POST /baggage-belts',
                                            'GET /airport-operations-management-workbench'),
                                   'description': 'Gates, stands, slots, turnaround, baggage, passenger flows, '
                                                  'disruptions, and airport coordination',
                                   'label': 'Airport Operations Management',
                                   'mesh': 'opsmfg',
                                   'template': 'asset',
},
 'aviation_maintenance_repair': {
                                 'apis': ('POST /aircrafts',
                                          'POST /components',
                                          'POST /work-cards',
                                          'POST /maintenance-visits',
                                          'POST /airworthiness-directives',
                                          'GET /aviation-maintenance-repair-workbench'),
                                 'description': 'Aircraft maintenance, components, work cards, compliance, '
                                                'airworthiness, deferred defects, and MRO operations',
                                 'label': 'Aviation Maintenance and Repair',
                                 'mesh': 'opsmfg',
                                 'template': 'asset',
},
 'bank_payments_clearing': {
                            'apis': ('POST /payment-instructions',
                                     'POST /clearing-batchs',
                                     'POST /settlement-files',
                                     'POST /return-items',
                                     'POST /exception-cases',
                                     'GET /bank-payments-clearing-workbench'),
                            'description': 'ACH, wire, real-time payment, card settlement, clearing files, exceptions, '
                                           'and bank reconciliation',
                            'label': 'Bank Payments Clearing',
                            'mesh': 'finops',
                            'template': 'reporting',
},
 'banking_core_accounts': {
                           'apis': ('POST /deposit-accounts',
                                    'POST /account-balances',
                                    'POST /account-holds',
                                    'POST /interest-accruals',
                                    'POST /fee-assessments',
                                    'GET /banking-core-accounts-workbench'),
                           'description': 'Deposit accounts, balances, holds, interest, fees, statements, customer '
                                          'account servicing, and account controls',
                           'label': 'Banking Core Accounts',
                           'mesh': 'finops',
                           'template': 'reporting',
},
 'building_information_modeling_ops': {
                                       'apis': ('POST /bim-models',
                                                'POST /model-versions',
                                                'POST /clash-issues',
                                                'POST /asset-objects',
                                                'POST /handover-packages',
                                                'GET /building-information-modeling-ops-workbench'),
                                       'description': 'BIM models, versions, clashes, assets, handover data, model '
                                                      'governance, and digital twin operations',
                                       'label': 'Building Information Modeling Operations',
                                       'mesh': 'content',
                                       'template': 'crm',
},
 'capital_markets_trading_ops': {
                                 'apis': ('POST /trade-orders',
                                          'POST /executions',
                                          'POST /allocations',
                                          'POST /confirmations',
                                          'POST /settlement-instructions',
                                          'GET /capital-markets-trading-ops-workbench'),
                                 'description': 'Trade orders, executions, allocations, confirmations, settlement, '
                                                'breaks, positions, and trading operations controls',
                                 'label': 'Capital Markets Trading Operations',
                                 'mesh': 'finops',
                                 'template': 'reporting',
},
 'capital_projects_delivery': {
                               'apis': ('POST /capital-projects',
                                        'POST /epc-packages',
                                        'POST /permit-milestones',
                                        'POST /progress-measurements',
                                        'POST /commissioning-systems',
                                        'GET /capital-projects-delivery-workbench'),
                               'description': 'Megaproject governance, EPC packages, permits, progress, commissioning, '
                                              'risk, and capital delivery controls',
                               'label': 'Capital Projects Delivery',
                               'mesh': 'opsmfg',
                               'template': 'asset',
},
 'chemical_batch_compliance': {
                               'apis': ('POST /chemical-formulas',
                                        'POST /batch-records',
                                        'POST /sds-documents',
                                        'POST /hazardous-materials',
                                        'POST /regulatory-submissions',
                                        'GET /chemical-batch-compliance-workbench'),
                               'description': 'Chemical formulas, batches, SDS, hazardous materials, regulatory '
                                              'submissions, quality, and compliance controls',
                               'label': 'Chemical Batch Compliance',
                               'mesh': 'opsmfg',
                               'template': 'asset',
},
 'claims_adjudication_healthcare': {
                                    'apis': ('POST /health-claims',
                                             'POST /claim-lines',
                                             'POST /coding-reviews',
                                             'POST /benefit-rules',
                                             'POST /denials',
                                             'GET /claims-adjudication-healthcare-workbench'),
                                    'description': 'Healthcare claim intake, coding validation, benefit rules, '
                                                   'denials, appeals, payment integrity, and payer adjudication',
                                    'label': 'Healthcare Claims Adjudication',
                                    'mesh': 'finops',
                                    'template': 'reporting',
},
 'clinical_care_coordination': {
                                'apis': ('POST /patient-care-plans',
                                         'POST /care-teams',
                                         'POST /referrals',
                                         'POST /encounters',
                                         'POST /care-gaps',
                                         'GET /clinical-care-coordination-workbench'),
                                'description': 'Care plans, referrals, encounters, care teams, transitions, outcomes, '
                                               'and patient coordination workflows',
                                'label': 'Clinical Care Coordination',
                                'mesh': 'relationship',
                                'template': 'workflow',
},
 'clinical_trials_management': {
                                'apis': ('POST /trial-protocols',
                                         'POST /study-sites',
                                         'POST /subjects',
                                         'POST /consent-records',
                                         'POST /visit-schedules',
                                         'GET /clinical-trials-management-workbench'),
                                'description': 'Protocols, trial sites, subjects, consent, visits, adverse events, '
                                               'monitoring, and trial data operations',
                                'label': 'Clinical Trials Management',
                                'mesh': 'relationship',
                                'template': 'workflow',
},
 'construction_contracts_commercials': {
                                        'apis': ('POST /construction-contracts',
                                                 'POST /pay-applications',
                                                 'POST /retainages',
                                                 'POST /variation-orders',
                                                 'POST /commercial-claims',
                                                 'GET /construction-contracts-commercials-workbench'),
                                        'description': 'Construction contracts, pay applications, retainage, claims, '
                                                       'variations, lien waivers, and commercial controls',
                                        'label': 'Construction Contracts and Commercials',
                                        'mesh': 'finops',
                                        'template': 'reporting',
},
 'construction_project_controls': {
                                   'apis': ('POST /construction-projects',
                                            'POST /work-packages',
                                            'POST /rfis',
                                            'POST /submittals',
                                            'POST /site-progresss',
                                            'GET /construction-project-controls-workbench'),
                                   'description': 'Construction budgets, schedules, RFIs, submittals, change events, '
                                                  'field progress, and site risk controls',
                                   'label': 'Construction Project Controls',
                                   'mesh': 'opsmfg',
                                   'template': 'asset',
},
 'court_case_management': {
                           'apis': ('POST /court-cases',
                                    'POST /filings',
                                    'POST /hearings',
                                    'POST /docket-entrys',
                                    'POST /partys',
                                    'GET /court-case-management-workbench'),
                           'description': 'Filings, hearings, dockets, parties, judgments, orders, calendars, and '
                                          'court operations',
                           'label': 'Court Case Management',
                           'mesh': 'relationship',
                           'template': 'workflow',
},
 'cybersecurity_operations_center': {
                                     'apis': ('POST /security-alerts',
                                              'POST /security-incidents',
                                              'POST /asset-exposures',
                                              'POST /threat-intels',
                                              'POST /playbook-runs',
                                              'GET /cybersecurity-operations-center-workbench'),
                                     'description': 'Security alerts, incidents, assets, threat intelligence, '
                                                    'playbooks, containment, and response evidence',
                                     'label': 'Cybersecurity Operations Center',
                                     'mesh': 'platform',
                                     'template': None,
},
 'defense_readiness_logistics': {
                                 'apis': ('POST /unit-readinesss',
                                          'POST /mission-assets',
                                          'POST /supply-requests',
                                          'POST /maintenance-statuss',
                                          'POST /deployment-plans',
                                          'GET /defense-readiness-logistics-workbench'),
                                 'description': 'Units, readiness, assets, maintenance, supply, mission planning, '
                                                'deployment, and defense logistics',
                                 'label': 'Defense Readiness Logistics',
                                 'mesh': 'scl',
                                 'template': 'logistics',
},
 'donor_grant_fundraising': {
                             'apis': ('POST /donors',
                                      'POST /campaigns',
                                      'POST /pledges',
                                      'POST /gifts',
                                      'POST /restrictions',
                                      'GET /donor-grant-fundraising-workbench'),
                             'description': 'Donors, campaigns, pledges, restrictions, gifts, grant applications, '
                                            'stewardship, and impact reporting',
                             'label': 'Donor Grant and Fundraising',
                             'mesh': 'relationship',
                             'template': 'workflow',
},
 'education_student_lifecycle': {
                                 'apis': ('POST /student-applicants',
                                          'POST /enrollments',
                                          'POST /curriculum-plans',
                                          'POST /advising-cases',
                                          'POST /course-attempts',
                                          'GET /education-student-lifecycle-workbench'),
                                 'description': 'Admissions, enrollment, curriculum, advising, progression, '
                                                'assessment, credentials, and student outcomes',
                                 'label': 'Education Student Lifecycle',
                                 'mesh': 'relationship',
                                 'template': 'workflow',
},
 'electronic_health_records_core': {
                                    'apis': ('POST /patient-charts',
                                             'POST /clinical-encounters',
                                             'POST /clinical-orders',
                                             'POST /observations',
                                             'POST /allergys',
                                             'GET /electronic-health-records-core-workbench'),
                                    'description': 'Clinical encounters, orders, observations, allergies, medication '
                                                   'lists, care notes, and patient summaries',
                                    'label': 'Electronic Health Records Core',
                                    'mesh': 'relationship',
                                    'template': 'workflow',
},
 'energy_grid_operations': {
                            'apis': ('POST /grid-assets',
                                     'POST /load-forecasts',
                                     'POST /switching-orders',
                                     'POST /dispatch-instructions',
                                     'POST /outage-events',
                                     'GET /energy-grid-operations-workbench'),
                            'description': 'Grid assets, load forecasts, switching, dispatch, outage state, '
                                           'reliability events, and grid operating constraints',
                            'label': 'Energy Grid Operations',
                            'mesh': 'opsmfg',
                            'template': 'asset',
},
 'energy_trading_risk': {
                         'apis': ('POST /energy-contracts',
                                  'POST /trade-positions',
                                  'POST /nominations',
                                  'POST /schedules',
                                  'POST /settlements',
                                  'GET /energy-trading-risk-workbench'),
                         'description': 'Energy contracts, positions, nominations, settlement, mark-to-market, '
                                        'exposure, and risk limits',
                         'label': 'Energy Trading and Risk',
                         'mesh': 'finops',
                         'template': 'reporting',
},
 'environment_health_safety': {
                               'apis': ('POST /ehs-incidents',
                                        'POST /hazards',
                                        'POST /inspections',
                                        'POST /permits',
                                        'POST /corrective-actions',
                                        'GET /environment-health-safety-workbench'),
                               'description': 'EHS incidents, inspections, permits, hazards, corrective actions, '
                                              'training, audits, and compliance evidence',
                               'label': 'Environment Health and Safety',
                               'mesh': 'opsmfg',
                               'template': 'asset',
},
 'facility_energy_management': {
                                'apis': ('POST /energy-meters',
                                         'POST /load-profiles',
                                         'POST /equipment-schedules',
                                         'POST /demand-response-events',
                                         'POST /energy-optimizations',
                                         'GET /facility-energy-management-workbench'),
                                'description': 'Facility meters, loads, equipment schedules, demand response, '
                                               'optimization, tariffs, and energy performance',
                                'label': 'Facility Energy Management',
                                'mesh': 'opsmfg',
                                'template': 'asset',
},
 'fleet_mobility_operations': {
                               'apis': ('POST /vehicles',
                                        'POST /driver-assignments',
                                        'POST /telematics-events',
                                        'POST /route-plans',
                                        'POST /fuel-transactions',
                                        'GET /fleet-mobility-operations-workbench'),
                               'description': 'Vehicles, drivers, telematics, routing, maintenance, utilization, fuel, '
                                              'safety, and fleet compliance',
                               'label': 'Fleet and Mobility Operations',
                               'mesh': 'scl',
                               'template': 'logistics',
},
 'food_safety_quality_compliance': {
                                    'apis': ('POST /haccp-plans',
                                             'POST /critical-control-points',
                                             'POST /inspections',
                                             'POST /nonconformances',
                                             'POST /recall-events',
                                             'GET /food-safety-quality-compliance-workbench'),
                                    'description': 'HACCP plans, inspections, nonconformance, recalls, supplier '
                                                   'audits, food quality, and regulatory evidence',
                                    'label': 'Food Safety Quality Compliance',
                                    'mesh': 'opsmfg',
                                    'template': 'asset',
},
 'gaming_casino_operations': {
                              'apis': ('POST /player-profiles',
                                       'POST /table-games',
                                       'POST /slot-machines',
                                       'POST /wager-sessions',
                                       'POST /payouts',
                                       'GET /gaming-casino-operations-workbench'),
                              'description': 'Players, tables, slots, compliance, responsible gaming, loyalty, '
                                             'payouts, and gaming floor operations',
                              'label': 'Gaming and Casino Operations',
                              'mesh': 'relationship',
                              'template': 'workflow',
},
 'hospitality_property_operations': {
                                     'apis': ('POST /room-inventorys',
                                              'POST /reservations',
                                              'POST /guest-stays',
                                              'POST /housekeeping-tasks',
                                              'POST /guest-requests',
                                              'GET /hospitality-property-operations-workbench'),
                                     'description': 'Rooms, reservations, housekeeping, guest service, occupancy, '
                                                    'revenue controls, and property operations',
                                     'label': 'Hospitality Property Operations',
                                     'mesh': 'cx',
                                     'template': 'crm',
},
 'hotel_revenue_management': {
                              'apis': ('POST /room-types',
                                       'POST /rate-plans',
                                       'POST /channel-inventorys',
                                       'POST /demand-forecasts',
                                       'POST /overbooking-policys',
                                       'GET /hotel-revenue-management-workbench'),
                              'description': 'Room inventory, rates, channels, demand forecasts, overbooking, yield, '
                                             'and hotel revenue controls',
                              'label': 'Hotel Revenue Management',
                              'mesh': 'finops',
                              'template': 'reporting',
},
 'humanitarian_relief_operations': {
                                    'apis': ('POST /needs-assessments',
                                             'POST /aid-items',
                                             'POST /distribution-events',
                                             'POST /field-partners',
                                             'POST /protection-cases',
                                             'GET /humanitarian-relief-operations-workbench'),
                                    'description': 'Needs assessment, aid distribution, logistics, protection, field '
                                                   'partners, donor reporting, and relief accountability',
                                    'label': 'Humanitarian Relief Operations',
                                    'mesh': 'scl',
                                    'template': 'logistics',
},
 'identity_kyc_aml_compliance': {
                                 'apis': ('POST /kyc-profiles',
                                          'POST /identity-documents',
                                          'POST /beneficial-owners',
                                          'POST /screening-hits',
                                          'POST /monitoring-alerts',
                                          'GET /identity-kyc-aml-compliance-workbench'),
                                 'description': 'Customer onboarding, identity proofing, beneficial ownership, '
                                                'screening, transaction monitoring, suspicious activity, and '
                                                'compliance cases',
                                 'label': 'Identity KYC AML Compliance',
                                 'mesh': 'platform',
                                 'template': None,
},
 'insurance_underwriting': {
                            'apis': ('POST /underwriting-submissions',
                                     'POST /risk-profiles',
                                     'POST /rating-factors',
                                     'POST /quotes',
                                     'POST /underwriting-decisions',
                                     'GET /insurance-underwriting-workbench'),
                            'description': 'Risk submissions, rating, quote generation, underwriting decisions, bind '
                                           'packages, exclusions, and referral workflows',
                            'label': 'Insurance Underwriting',
                            'mesh': 'finops',
                            'template': 'reporting',
},
 'it_service_management': {
                           'apis': ('POST /it-incidents',
                                    'POST /service-requests',
                                    'POST /change-requests',
                                    'POST /problem-records',
                                    'POST /configuration-items',
                                    'GET /it-service-management-workbench'),
                           'description': 'Incidents, requests, changes, problems, configuration items, service '
                                          'levels, and IT operations controls',
                           'label': 'IT Service Management',
                           'mesh': 'platform',
                           'template': None,
},
 'laboratory_information_management': {
                                       'apis': ('POST /lab-samples',
                                                'POST /test-orders',
                                                'POST /instrument-runs',
                                                'POST /results',
                                                'POST /quality-controls',
                                                'GET /laboratory-information-management-workbench'),
                                       'description': 'Samples, tests, instruments, results, quality control, chain of '
                                                      'custody, and laboratory workflows',
                                       'label': 'Laboratory Information Management',
                                       'mesh': 'opsmfg',
                                       'template': 'asset',
},
 'land_real_estate_development': {
                                  'apis': ('POST /land-parcels',
                                           'POST /zoning-cases',
                                           'POST /entitlements',
                                           'POST /feasibility-models',
                                           'POST /permit-applications',
                                           'GET /land-real-estate-development-workbench'),
                                  'description': 'Parcels, entitlements, zoning, feasibility, permits, development '
                                                 'milestones, and land economics',
                                  'label': 'Land and Real Estate Development',
                                  'mesh': 'relationship',
                                  'template': 'workflow',
},
 'lease_lending_equipment_finance': {
                                     'apis': ('POST /equipment-leases',
                                              'POST /leased-assets',
                                              'POST /payment-schedules',
                                              'POST /residual-values',
                                              'POST /buyout-quotes',
                                              'GET /lease-lending-equipment-finance-workbench'),
                                     'description': 'Equipment leases, assets, schedules, residuals, buyouts, '
                                                    'repossession, and finance servicing',
                                     'label': 'Lease Lending and Equipment Finance',
                                     'mesh': 'finops',
                                     'template': 'reporting',
},
 'lending_origination_servicing': {
                                   'apis': ('POST /loan-applications',
                                            'POST /borrower-profiles',
                                            'POST /underwriting-decisions',
                                            'POST /loan-offers',
                                            'POST /disbursements',
                                            'GET /lending-origination-servicing-workbench'),
                                   'description': 'Loan applications, underwriting, offers, disbursement, repayment, '
                                                  'servicing, collections, and covenant monitoring',
                                   'label': 'Lending Origination and Servicing',
                                   'mesh': 'finops',
                                   'template': 'reporting',
},
 'library_archives_management': {
                                 'apis': ('POST /collection-items',
                                          'POST /catalog-records',
                                          'POST /circulation-loans',
                                          'POST /digitization-jobs',
                                          'POST /rights-statements',
                                          'GET /library-archives-management-workbench'),
                                 'description': 'Collections, circulation, cataloging, digitization, rights, '
                                                'preservation, and archival access',
                                 'label': 'Library and Archives Management',
                                 'mesh': 'content',
                                 'template': 'crm',
},
 'livestock_herd_management': {
                               'apis': ('POST /animals',
                                        'POST /herd-groups',
                                        'POST /health-events',
                                        'POST /breeding-records',
                                        'POST /feed-rations',
                                        'GET /livestock-herd-management-workbench'),
                               'description': 'Animals, health, breeding, feed, movements, treatments, compliance, and '
                                              'herd productivity',
                               'label': 'Livestock Herd Management',
                               'mesh': 'opsmfg',
                               'template': 'asset',
},
 'maritime_shipping_operations': {
                                  'apis': ('POST /voyages',
                                           'POST /vessels',
                                           'POST /cargo-bookings',
                                           'POST /charter-partys',
                                           'POST /port-calls',
                                           'GET /maritime-shipping-operations-workbench'),
                                  'description': 'Voyages, vessels, cargo, charter parties, port calls, demurrage, '
                                                 'bunkers, and marine operations',
                                  'label': 'Maritime Shipping Operations',
                                  'mesh': 'scl',
                                  'template': 'logistics',
},
 'media_production_management': {
                                 'apis': ('POST /productions',
                                          'POST /budget-lines',
                                          'POST /crew-bookings',
                                          'POST /location-permits',
                                          'POST /shoot-days',
                                          'GET /media-production-management-workbench'),
                                 'description': 'Productions, budgets, crews, locations, shoots, post-production, '
                                                'assets, and delivery milestones',
                                 'label': 'Media Production Management',
                                 'mesh': 'content',
                                 'template': 'crm',
},
 'media_rights_content_monetization': {
                                       'apis': ('POST /rights-assets',
                                                'POST /license-agreements',
                                                'POST /distribution-windows',
                                                'POST /usage-records',
                                                'POST /royalty-statements',
                                                'GET /media-rights-content-monetization-workbench'),
                                       'description': 'Rights, licensing, distribution windows, royalties, usage '
                                                      'tracking, revenue share, and content monetization',
                                       'label': 'Media Rights and Content Monetization',
                                       'mesh': 'content',
                                       'template': 'crm',
},
 'medical_device_lifecycle': {
                              'apis': ('POST /medical-devices',
                                       'POST /device-assignments',
                                       'POST /calibrations',
                                       'POST /maintenance-events',
                                       'POST /recall-notices',
                                       'GET /medical-device-lifecycle-workbench'),
                              'description': 'Medical device registry, maintenance, calibration, recalls, usage '
                                             'traceability, and regulatory evidence',
                              'label': 'Medical Device Lifecycle',
                              'mesh': 'opsmfg',
                              'template': 'asset',
},
 'mining_operations_management': {
                                  'apis': ('POST /mine-plans',
                                           'POST /pit-blocks',
                                           'POST /extraction-shifts',
                                           'POST /haulage-cycles',
                                           'POST /fleet-assets',
                                           'GET /mining-operations-management-workbench'),
                                  'description': 'Mine plans, extraction, haulage, fleet, ore quality, safety, '
                                                 'stockpiles, and rehabilitation operations',
                                  'label': 'Mining Operations Management',
                                  'mesh': 'opsmfg',
                                  'template': 'asset',
},
 'mining_safety_permits': {
                           'apis': ('POST /mine-permits',
                                    'POST /shift-rosters',
                                    'POST /blast-plans',
                                    'POST /safety-inspections',
                                    'POST /incident-reports',
                                    'GET /mining-safety-permits-workbench'),
                           'description': 'Mine permits, shifts, blasts, inspections, incidents, safety controls, and '
                                          'regulatory evidence',
                           'label': 'Mining Safety and Permits',
                           'mesh': 'opsmfg',
                           'template': 'asset',
},
 'mortgage_servicing': {
                        'apis': ('POST /mortgage-loans',
                                 'POST /escrow-accounts',
                                 'POST /payment-events',
                                 'POST /servicing-statements',
                                 'POST /loss-mitigation-cases',
                                 'GET /mortgage-servicing-workbench'),
                        'description': 'Mortgage accounts, escrow, payments, statements, loss mitigation, investor '
                                       'reporting, and foreclosure controls',
                        'label': 'Mortgage Servicing',
                        'mesh': 'finops',
                        'template': 'reporting',
},
 'music_royalties_rights': {
                            'apis': ('POST /musical-works',
                                     'POST /recordings',
                                     'POST /rights-splits',
                                     'POST /licenses',
                                     'POST /usage-reports',
                                     'GET /music-royalties-rights-workbench'),
                            'description': 'Works, recordings, splits, licenses, statements, usage, royalty payments, '
                                           'and rights disputes',
                            'label': 'Music Royalties and Rights',
                            'mesh': 'content',
                            'template': 'crm',
},
 'nonprofit_program_impact': {
                              'apis': ('POST /programs',
                                       'POST /beneficiarys',
                                       'POST /service-episodes',
                                       'POST /outcome-measures',
                                       'POST /grant-restrictions',
                                       'GET /nonprofit-program-impact-workbench'),
                              'description': 'Programs, beneficiaries, outcomes, grants, services, restrictions, '
                                             'impact evidence, and donor reporting',
                              'label': 'Nonprofit Program Impact',
                              'mesh': 'relationship',
                              'template': 'workflow',
},
 'oil_gas_field_operations': {
                              'apis': ('POST /wells',
                                       'POST /production-readings',
                                       'POST /field-tickets',
                                       'POST /workover-plans',
                                       'POST /hse-events',
                                       'GET /oil-gas-field-operations-workbench'),
                              'description': 'Wells, production, maintenance, field logistics, HSE, reserves, lifting '
                                             'costs, and operating events',
                              'label': 'Oil and Gas Field Operations',
                              'mesh': 'opsmfg',
                              'template': 'asset',
},
 'permitting_licensing_inspections': {
                                      'apis': ('POST /applications',
                                               'POST /permits',
                                               'POST /licenses',
                                               'POST /review-tasks',
                                               'POST /fee-assessments',
                                               'GET /permitting-licensing-inspections-workbench'),
                                      'description': 'Applications, reviews, permits, licenses, fees, inspections, '
                                                     'violations, renewals, and citizen workflows',
                                      'label': 'Permitting Licensing and Inspections',
                                      'mesh': 'relationship',
                                      'template': 'workflow',
},
 'pharma_manufacturing_quality': {
                                  'apis': ('POST /pharma-batchs',
                                           'POST /master-batch-records',
                                           'POST /validation-protocols',
                                           'POST /deviations',
                                           'POST /capas',
                                           'GET /pharma-manufacturing-quality-workbench'),
                                  'description': 'Batch records, validation, deviations, CAPA, release, serialization, '
                                                 'and regulated manufacturing quality',
                                  'label': 'Pharma Manufacturing Quality',
                                  'mesh': 'opsmfg',
                                  'template': 'asset',
},
 'pharmacy_benefits_management': {
                                  'apis': ('POST /formularys',
                                           'POST /drug-coverage-rules',
                                           'POST /prior-authorizations',
                                           'POST /pharmacy-claims',
                                           'POST /rebate-contracts',
                                           'GET /pharmacy-benefits-management-workbench'),
                                  'description': 'Formulary, prior authorization, pharmacy network, claims, rebates, '
                                                 'utilization controls, and medication affordability',
                                  'label': 'Pharmacy Benefits Management',
                                  'mesh': 'relationship',
                                  'template': 'workflow',
},
 'policy_administration_insurance': {
                                     'apis': ('POST /insurance-policys',
                                              'POST /coverage-items',
                                              'POST /endorsements',
                                              'POST /renewal-notices',
                                              'POST /cancellation-events',
                                              'GET /policy-administration-insurance-workbench'),
                                     'description': 'Insurance policy lifecycle, endorsements, renewals, '
                                                    'cancellations, billing status, coverage changes, and documents',
                                     'label': 'Insurance Policy Administration',
                                     'mesh': 'finops',
                                     'template': 'reporting',
},
 'port_terminal_operations': {
                              'apis': ('POST /vessel-calls',
                                       'POST /berth-plans',
                                       'POST /container-moves',
                                       'POST /yard-slots',
                                       'POST /gate-transactions',
                                       'GET /port-terminal-operations-workbench'),
                              'description': 'Vessel calls, berths, yard moves, containers, equipment, customs '
                                             'handoffs, and terminal productivity',
                              'label': 'Port Terminal Operations',
                              'mesh': 'scl',
                              'template': 'logistics',
},
 'provider_revenue_cycle': {
                            'apis': ('POST /patient-accounts',
                                     'POST /charge-captures',
                                     'POST /coding-workqueues',
                                     'POST /claim-batchs',
                                     'POST /denial-cases',
                                     'GET /provider-revenue-cycle-workbench'),
                            'description': 'Healthcare registration, charge capture, coding, claims, denials, payment '
                                           'posting, collections, and revenue integrity',
                            'label': 'Provider Revenue Cycle',
                            'mesh': 'finops',
                            'template': 'reporting',
},
 'public_safety_dispatch': {
                            'apis': ('POST /emergency-calls',
                                     'POST /response-units',
                                     'POST /incidents',
                                     'POST /dispatch-assignments',
                                     'POST /mutual-aids',
                                     'GET /public-safety-dispatch-workbench'),
                            'description': 'Emergency calls, units, incidents, dispatch, mutual aid, response times, '
                                           'and public safety operations',
                            'label': 'Public Safety Dispatch',
                            'mesh': 'relationship',
                            'template': 'workflow',
},
 'public_sector_case_management': {
                                   'apis': ('POST /citizen-cases',
                                            'POST /eligibility-determinations',
                                            'POST /benefit-decisions',
                                            'POST /inspections',
                                            'POST /notices',
                                            'GET /public-sector-case-management-workbench'),
                                   'description': 'Citizen cases, eligibility, benefits, inspections, notices, '
                                                  'appeals, service levels, and public outcomes',
                                   'label': 'Public Sector Case Management',
                                   'mesh': 'relationship',
                                   'template': 'workflow',
},
 'publishing_editorial_operations': {
                                     'apis': ('POST /manuscripts',
                                              'POST /editorial-tasks',
                                              'POST /author-contracts',
                                              'POST /editions',
                                              'POST /production-schedules',
                                              'GET /publishing-editorial-operations-workbench'),
                                     'description': 'Manuscripts, editorial workflow, rights, editions, production '
                                                    'schedules, distribution, and publishing analytics',
                                     'label': 'Publishing Editorial Operations',
                                     'mesh': 'content',
                                     'template': 'crm',
},
 'rail_operations_management': {
                                'apis': ('POST /train-plans',
                                         'POST /consists',
                                         'POST /track-windows',
                                         'POST /yard-moves',
                                         'POST /crew-assignments',
                                         'GET /rail-operations-management-workbench'),
                                'description': 'Train plans, consists, track windows, yards, crews, incidents, and '
                                               'rail service performance',
                                'label': 'Rail Operations Management',
                                'mesh': 'scl',
                                'template': 'logistics',
},
 'real_estate_property_management': {
                                     'apis': ('POST /propertys',
                                              'POST /tenants',
                                              'POST /leases',
                                              'POST /rent-charges',
                                              'POST /maintenance-requests',
                                              'GET /real-estate-property-management-workbench'),
                                     'description': 'Properties, leases, tenants, rent, maintenance, inspections, '
                                                    'deposits, and property compliance',
                                     'label': 'Real Estate Property Management',
                                     'mesh': 'relationship',
                                     'template': 'workflow',
},
 'reinsurance_management': {
                            'apis': ('POST /reinsurance-treatys',
                                     'POST /facultative-placements',
                                     'POST /cessions',
                                     'POST /bordereaus',
                                     'POST /recoverables',
                                     'GET /reinsurance-management-workbench'),
                            'description': 'Treaties, facultative placements, cessions, recoverables, bordereaux, '
                                           'claims recoveries, and exposure',
                            'label': 'Reinsurance Management',
                            'mesh': 'finops',
                            'template': 'reporting',
},
 'renewables_asset_operations': {
                                 'apis': ('POST /renewable-assets',
                                          'POST /generation-readings',
                                          'POST /curtailment-events',
                                          'POST /availability-records',
                                          'POST /ppa-obligations',
                                          'GET /renewables-asset-operations-workbench'),
                                 'description': 'Solar and wind assets, generation, curtailment, maintenance, PPAs, '
                                                'availability, and renewable performance',
                                 'label': 'Renewables Asset Operations',
                                 'mesh': 'opsmfg',
                                 'template': 'asset',
},
 'research_grants_management': {
                                'apis': ('POST /grant-proposals',
                                         'POST /research-awards',
                                         'POST /sponsor-budgets',
                                         'POST /compliance-requirements',
                                         'POST /subawards',
                                         'GET /research-grants-management-workbench'),
                                'description': 'Research proposals, awards, budgets, compliance, milestones, '
                                               'subawards, effort, and sponsor reporting',
                                'label': 'Research Grants Management',
                                'mesh': 'finops',
                                'template': 'reporting',
},
 'restaurant_operations': {
                           'apis': ('POST /menu-items',
                                    'POST /recipes',
                                    'POST /kitchen-tickets',
                                    'POST /reservations',
                                    'POST /inventory-preps',
                                    'GET /restaurant-operations-workbench'),
                           'description': 'Menus, recipes, kitchen production, reservations, food cost, labor, waste, '
                                          'and service execution',
                           'label': 'Restaurant Operations',
                           'mesh': 'opsmfg',
                           'template': 'asset',
},
 'smart_city_mobility_operations': {
                                    'apis': ('POST /transit-services',
                                             'POST /parking-assets',
                                             'POST /signal-plans',
                                             'POST /traffic-incidents',
                                             'POST /curb-allocations',
                                             'GET /smart-city-mobility-operations-workbench'),
                                    'description': 'Transit, parking, traffic signals, incidents, curb management, '
                                                   'multimodal services, and city mobility analytics',
                                    'label': 'Smart City Mobility Operations',
                                    'mesh': 'opsmfg',
                                    'template': 'asset',
},
 'sports_venue_event_operations': {
                                   'apis': ('POST /venue-events',
                                            'POST /seating-manifests',
                                            'POST /concession-plans',
                                            'POST /security-posts',
                                            'POST /event-staffs',
                                            'GET /sports-venue-event-operations-workbench'),
                                   'description': 'Venue events, seating, concessions, security, staffing, fan '
                                                  'experience, and event operations',
                                   'label': 'Sports Venue Event Operations',
                                   'mesh': 'opsmfg',
                                   'template': 'asset',
},
 'student_financial_aid': {
                           'apis': ('POST /aid-applications',
                                    'POST /eligibility-reviews',
                                    'POST /award-packages',
                                    'POST /verification-items',
                                    'POST /disbursements',
                                    'GET /student-financial-aid-workbench'),
                           'description': 'Aid eligibility, awards, verification, disbursement, satisfactory progress, '
                                          'compliance, and student funding',
                           'label': 'Student Financial Aid',
                           'mesh': 'finops',
                           'template': 'reporting',
},
 'tax_administration_public_sector': {
                                      'apis': ('POST /taxpayer-accounts',
                                               'POST /tax-filings',
                                               'POST /assessments',
                                               'POST /audit-cases',
                                               'POST /collection-actions',
                                               'GET /tax-administration-public-sector-workbench'),
                                      'description': 'Taxpayer accounts, filings, assessments, audits, collections, '
                                                     'appeals, and public revenue administration',
                                      'label': 'Public Sector Tax Administration',
                                      'mesh': 'finops',
                                      'template': 'reporting',
},
 'telecom_network_operations': {
                                'apis': ('POST /network-elements',
                                         'POST /capacity-segments',
                                         'POST /network-incidents',
                                         'POST /alarm-events',
                                         'POST /service-assurance-cases',
                                         'GET /telecom-network-operations-workbench'),
                                'description': 'Network inventory, capacity, incidents, alarms, service assurance, '
                                               'maintenance windows, and SLA impact',
                                'label': 'Telecom Network Operations',
                                'mesh': 'opsmfg',
                                'template': 'asset',
},
 'telecom_subscription_lifecycle': {
                                    'apis': ('POST /subscriber-accounts',
                                             'POST /service-plans',
                                             'POST /sim-profiles',
                                             'POST /activation-requests',
                                             'POST /usage-sessions',
                                             'GET /telecom-subscription-lifecycle-workbench'),
                                    'description': 'Plans, activations, SIM and eSIM lifecycle, usage, roaming, plan '
                                                   'changes, churn controls, and service entitlements',
                                    'label': 'Telecom Subscription Lifecycle',
                                    'mesh': 'commerce',
                                    'template': 'sales',
},
 'trade_finance_operations': {
                              'apis': ('POST /letter-of-credits',
                                       'POST /bank-guarantees',
                                       'POST /documentary-collections',
                                       'POST /trade-documents',
                                       'POST /sanctions-checks',
                                       'GET /trade-finance-operations-workbench'),
                              'description': 'Letters of credit, guarantees, documentary collections, sanctions '
                                             'checks, shipment documents, and trade settlement',
                              'label': 'Trade Finance Operations',
                              'mesh': 'finops',
                              'template': 'reporting',
},
 'utilities_metering_billing': {
                                'apis': ('POST /meter-reads',
                                         'POST /usage-intervals',
                                         'POST /tariffs',
                                         'POST /service-orders',
                                         'POST /utility-bills',
                                         'GET /utilities-metering-billing-workbench'),
                                'description': 'Meter reads, usage validation, tariffs, service orders, bills, '
                                               'adjustments, collections, and customer utility billing',
                                'label': 'Utilities Metering and Billing',
                                'mesh': 'finops',
                                'template': 'reporting',
},
 'utility_outage_restoration': {
                                'apis': ('POST /outage-incidents',
                                         'POST /device-interruptions',
                                         'POST /switching-steps',
                                         'POST /crew-assignments',
                                         'POST /restoration-estimates',
                                         'GET /utility-outage-restoration-workbench'),
                                'description': 'Outage detection, switching, crew dispatch, restoration estimates, '
                                               'customer impact, and reliability reporting',
                                'label': 'Utility Outage Restoration',
                                'mesh': 'opsmfg',
                                'template': 'asset',
},
 'waste_recycling_operations': {
                                'apis': ('POST /waste-routes',
                                         'POST /bin-assets',
                                         'POST /pickup-events',
                                         'POST /material-streams',
                                         'POST /contamination-findings',
                                         'GET /waste-recycling-operations-workbench'),
                                'description': 'Routes, bins, pickups, materials, contamination, disposal sites, '
                                               'recycling yields, and compliance',
                                'label': 'Waste and Recycling Operations',
                                'mesh': 'scl',
                                'template': 'logistics',
},
 'water_wastewater_operations': {
                                 'apis': ('POST /treatment-plants',
                                          'POST /water-quality-samples',
                                          'POST /permit-limits',
                                          'POST /pump-assets',
                                          'POST /service-interruptions',
                                          'GET /water-wastewater-operations-workbench'),
                                 'description': 'Treatment plants, water quality, permits, assets, service '
                                                'interruptions, field work, and compliance reporting',
                                 'label': 'Water and Wastewater Operations',
                                 'mesh': 'opsmfg',
                                 'template': 'asset',
},
 'wealth_portfolio_management': {
                                 'apis': ('POST /client-portfolios',
                                          'POST /investment-mandates',
                                          'POST /suitability-profiles',
                                          'POST /rebalance-orders',
                                          'POST /performance-snapshots',
                                          'GET /wealth-portfolio-management-workbench'),
                                 'description': 'Client portfolios, mandates, suitability, rebalancing, performance, '
                                                'fees, and advisory controls',
                                 'label': 'Wealth Portfolio Management',
                                 'mesh': 'finops',
                                 'template': 'reporting',
}}
)

PBC_INDUSTRY_STANDARD_FEATURE_EXTENSIONS = (
    'ai_agent_task_assistance',
    'configuration_workbench',
    'continuous_release_assurance',
)

# The loop that used to write those three extensions back into each candidate's
# catalog row is gone. It wrote `standard_features` and `capabilities` onto the
# row, and since the descriptor migration the descriptor reads every declared
# surface from the package (`_package_declared_surface`: runtime constant, else
# manifest), so no reader ever saw the write. Canaried before deleting: poisoning
# this constant left `pbc_catalog()` byte-identical, which is only possible if
# the loop's output is unread. The extensions now live where the descriptor
# finds them, in each package's `*_STANDARD_FEATURE_KEYS`; all 80 candidates
# carry all three, verified across the full set.

IMPLEMENTED_PBC_KEYS = (
    *IMPLEMENTED_PBC_KEYS,
    'clinical_care_coordination',
    'claims_adjudication_healthcare',
    'pharmacy_benefits_management',
    'banking_core_accounts',
    'lending_origination_servicing',
    'insurance_underwriting',
    'capital_markets_trading_ops',
    'energy_grid_operations',
    'utilities_metering_billing',
    'telecom_network_operations',
    'telecom_subscription_lifecycle',
    'real_estate_property_management',
    'construction_project_controls',
    'hospitality_property_operations',
    'restaurant_operations',
    'agriculture_farm_operations',
    'mining_operations_management',
    'oil_gas_field_operations',
    'airline_operations_control',
    'port_terminal_operations',
    'public_sector_case_management',
    'education_student_lifecycle',
    'research_grants_management',
    'media_rights_content_monetization',
    'advertising_campaign_operations',
    'cybersecurity_operations_center',
    'it_service_management',
    'environment_health_safety',
    'donor_grant_fundraising',
    'fleet_mobility_operations',
    'provider_revenue_cycle',
    'electronic_health_records_core',
    'clinical_trials_management',
    'laboratory_information_management',
    'medical_device_lifecycle',
    'bank_payments_clearing',
    'wealth_portfolio_management',
    'trade_finance_operations',
    'mortgage_servicing',
    'lease_lending_equipment_finance',
    'policy_administration_insurance',
    'reinsurance_management',
    'actuarial_pricing_reserving',
    'utility_outage_restoration',
    'energy_trading_risk',
    'renewables_asset_operations',
    'water_wastewater_operations',
    'waste_recycling_operations',
    'rail_operations_management',
    'maritime_shipping_operations',
    'aviation_maintenance_repair',
    'airport_operations_management',
    'smart_city_mobility_operations',
    'construction_contracts_commercials',
    'building_information_modeling_ops',
    'capital_projects_delivery',
    'land_real_estate_development',
    'facility_energy_management',
    'hotel_revenue_management',
    'gaming_casino_operations',
    'sports_venue_event_operations',
    'media_production_management',
    'music_royalties_rights',
    'publishing_editorial_operations',
    'agri_supply_chain_traceability',
    'livestock_herd_management',
    'food_safety_quality_compliance',
    'mining_safety_permits',
    'chemical_batch_compliance',
    'pharma_manufacturing_quality',
    'public_safety_dispatch',
    'court_case_management',
    'tax_administration_public_sector',
    'permitting_licensing_inspections',
    'student_financial_aid',
    'library_archives_management',
    'nonprofit_program_impact',
    'humanitarian_relief_operations',
    'defense_readiness_logistics',
    'identity_kyc_aml_compliance',
)

PBC_STARTER_STACKS = {
    "finance_mesh": ("gl_core", "ap_automation", "ar_credit", "treasury_cash", "tax_localization"),
    "distribution_mesh": ("inventory_positioning", "wms_core", "transportation_management", "dom"),
    "people_mesh": ("personnel_identity", "time_labor", "payroll_engine", "talent_onboarding"),
    "manufacturing_mesh": ("mrp_engine", "production_control", "quality_assurance", "eam"),
    "customer_order_mesh": ("customer_360", "product_catalog_pim", "dom", "ar_credit", "tax_localization"),
    "enterprise_core": ("gl_core", "ap_automation", "ar_credit", "inventory_positioning", "personnel_identity", "dom"),
    "application_composition_platform": (
        "federated_iam",
        "api_gateway_mesh",
        "schema_registry",
        "workflow_orchestration",
        "audit_ledger",
        "composition_engine",
    ),
    "digital_commerce_platform": (
        "checkout_processing",
        "payment_orchestration",
        "order_routing_optimization",
        "global_inventory_visibility",
        "returns_reverse_logistics",
        "cross_border_trade",
    ),
    "customer_intelligence_platform": (
        "customer_360",
        "cdp_segmentation",
        "loyalty_rewards",
        "streaming_analytics",
        "enterprise_search_vector",
        "fraud_anomaly_detection",
    ),
}


def pbc_mesh_catalog() -> tuple[dict, ...]:
    """Return enterprise mesh groups with catalog counts."""
    return tuple(
        {
            "mesh": key,
            **value,
            "pbc_count": sum(1 for item in PBC_CATALOG.values() if item["mesh"] == key),
        }
        for key, value in PBC_MESHES.items()
    )


@lru_cache(maxsize=None)
def pbc_catalog(mesh: str | None = None) -> tuple[dict, ...]:
    """Return selectable PBC descriptors for the IDE catalog.

    The catalog is built once per mesh and reused. Every descriptor folds in its
    package's runtime capabilities, and the LSP calls this by key on the order of
    fifty times per request, so rebuilding it each time cost 27s for a result
    that is a pure function of a module-level dict. `pbc_catalog.cache_clear()`
    is the one way to force a rebuild after a runtime mutation.
    """
    selected = tuple(
        (key, value)
        for key, value in PBC_CATALOG.items()
        if mesh is None or value["mesh"] == mesh
    )
    return tuple(_pbc_descriptor(key, value) for key, value in selected)


def pbc_starter_stacks() -> tuple[dict, ...]:
    """Return recommended multi-PBC stacks users can select as app starters."""
    return tuple(
        {
            "stack": name,
            "pbcs": pbcs,
            "meshes": tuple(sorted({PBC_CATALOG[key]["mesh"] for key in pbcs})),
        }
        for name, pbcs in PBC_STARTER_STACKS.items()
    )


def acp_stream_processor_catalog() -> tuple[dict, ...]:
    """Return supported Python-native stream/event processing profiles."""
    return tuple(
        {
            "processor": key,
            **value,
        }
        for key, value in ACP_STREAM_PROCESSORS.items()
    )


def acp_stream_processing_policy() -> dict:
    """Return the platform's opinionated stream-processing choice policy."""
    return {
        "format": "appgen.acp-stream-processing-policy.v1",
        "ok": True,
        "default": ACP_STREAM_PROCESSING_POLICY["default"],
        "allowed_processors": ACP_STREAM_PROCESSING_POLICY["allowed_processors"],
        "developer_guidance": ACP_STREAM_PROCESSING_POLICY["developer_guidance"],
        "developer_guidance_contract": ACP_STREAM_PROCESSING_POLICY["developer_guidance_contract"],
        "developer_action_contract": ACP_STREAM_PROCESSING_POLICY["developer_action_contract"],
        "developer_use_card": ACP_STREAM_PROCESSING_POLICY["developer_use_card"],
        "developer_decision_brief": ACP_STREAM_PROCESSING_POLICY["developer_decision_brief"],
        "developer_implementation_playbook": ACP_STREAM_PROCESSING_POLICY["developer_implementation_playbook"],
        "developer_decision_runbook": ACP_STREAM_PROCESSING_POLICY["developer_decision_runbook"],
        "decision_card": ACP_STREAM_PROCESSING_POLICY["decision_card"],
        "developer_choice_lock": ACP_STREAM_PROCESSING_POLICY["developer_choice_lock"],
        "developer_decision_record": ACP_STREAM_PROCESSING_POLICY["developer_decision_record"],
        "developer_choice_algorithm": ACP_STREAM_PROCESSING_POLICY["developer_choice_algorithm"],
        "developer_use_policy": ACP_STREAM_PROCESSING_POLICY["developer_use_policy"],
        "choice_budget": ACP_STREAM_PROCESSING_POLICY["choice_budget"],
        "ordinary_workload_contract": ACP_STREAM_PROCESSING_POLICY["ordinary_workload_contract"],
        "developer_default_stack": ACP_STREAM_PROCESSING_POLICY["developer_default_stack"],
        "developer_recommendation_card": ACP_STREAM_PROCESSING_POLICY["developer_recommendation_card"],
        "developer_rule": ACP_STREAM_PROCESSING_POLICY["developer_rule"],
        "generation_rule": ACP_STREAM_PROCESSING_POLICY["generation_rule"],
        "implementation_directive": ACP_STREAM_PROCESSING_POLICY["implementation_directive"],
        "opinionated_stack": ACP_STREAM_PROCESSING_POLICY["opinionated_stack"],
        "generator_outputs": ACP_STREAM_PROCESSING_POLICY["generator_outputs"],
        "decision_ladder": ACP_STREAM_PROCESSING_POLICY["decision_ladder"],
        "workload_defaults": ACP_STREAM_PROCESSING_POLICY["workload_defaults"],
        "exception_prompts": ACP_STREAM_PROCESSING_POLICY["exception_prompts"],
        "exception_required_evidence": ACP_STREAM_PROCESSING_POLICY["exception_required_evidence"],
        "prohibited": ACP_STREAM_PROCESSING_POLICY["prohibited"],
        "decision_tree": ACP_STREAM_PROCESSING_POLICY["decision_tree"],
        "profiles": acp_stream_processor_catalog(),
        "rules": ACP_STREAM_PROCESSOR_DECISION_RULES,
    }


def acp_event_processing_developer_guidance() -> dict:
    """Return the one-answer event-processing guidance for app developers."""
    contract = ACP_STREAM_PROCESSING_POLICY["developer_guidance_contract"]
    return {
        "format": "appgen.acp-event-processing-developer-guidance.v1",
        "ok": True,
        **contract,
        "developer_action_contract": ACP_STREAM_PROCESSING_POLICY["developer_action_contract"],
        "developer_use_card": ACP_STREAM_PROCESSING_POLICY["developer_use_card"],
        "decision_brief": ACP_STREAM_PROCESSING_POLICY["developer_decision_brief"],
        "implementation_playbook": ACP_STREAM_PROCESSING_POLICY["developer_implementation_playbook"],
        "decision_runbook": ACP_STREAM_PROCESSING_POLICY["developer_decision_runbook"],
        "choice_lock": ACP_STREAM_PROCESSING_POLICY["developer_choice_lock"],
        "developer_default_stack": ACP_STREAM_PROCESSING_POLICY["developer_default_stack"],
        "developer_recommendation_card": ACP_STREAM_PROCESSING_POLICY["developer_recommendation_card"],
        "policy_format": acp_stream_processing_policy()["format"],
        "default_runtime_profile": ACP_DEFAULT_STREAM_PROCESSOR,
    }


def lint_pbc_eventing_choice(manifest: dict, *, generated_imports: tuple[str, ...] = ()) -> dict:
    """Lint the developer-facing PBC eventing choice before generation."""
    validation = validate_pbc_manifest(manifest, existing_catalog={})
    stream_processor = manifest.get("stream_processor")
    exception_profiles = set(ACP_STREAM_PROCESSING_POLICY["developer_guidance_contract"]["exception_options"])
    forbidden_imports = ACP_STREAM_PROCESSING_POLICY["ordinary_workload_contract"]["forbidden_imports"]
    diagnostics = []
    quick_fixes = []
    if stream_processor == ACP_DEFAULT_STREAM_PROCESSOR:
        diagnostics.append(
            {
                "severity": "error",
                "rule": "ordinary_pbc_manifest_omits_stream_processor",
                "message": "Ordinary PBC manifests must omit stream_processor; the platform records the default profile as read-only metadata.",
            }
        )
        quick_fixes.append(
            {
                "id": "remove_stream_processor",
                "field": "stream_processor",
                "replacement": None,
            }
        )
    elif stream_processor and stream_processor not in exception_profiles:
        diagnostics.append(
            {
                "severity": "error",
                "rule": "unsupported_stream_processor",
                "message": "Use appgen_event_contract for ordinary work; only audited exception profiles are accepted.",
            }
        )
    elif stream_processor in exception_profiles and validation["missing_stream_exception_evidence"]:
        diagnostics.append(
            {
                "severity": "error",
                "rule": "exception_profiles_require_stream_exception_evidence",
                "message": (
                    "Exception profiles require workload_name, throughput_or_latency_reason, "
                    "state_shape, and operational_owner."
                ),
            }
        )
    import_violations = tuple(
        module
        for module in generated_imports
        if module.split(".", 1)[0] in forbidden_imports
    )
    if import_violations:
        diagnostics.append(
            {
                "severity": "error",
                "rule": "generated_business_logic_imports_appgen_event_adapter_only",
                "message": "Generated business logic must import the AppGen-X event adapter, not profile-specific stream libraries.",
                "imports": import_violations,
            }
        )
    normal_form = dict(manifest)
    if not stream_processor or stream_processor == ACP_DEFAULT_STREAM_PROCESSOR:
        normal_form.pop("stream_processor", None)
    return {
        "format": "appgen.pbc-eventing-choice-lint.v1",
        "ok": validation["ok"] and not diagnostics,
        "developer_answer": "Use appgen_event_contract.",
        "ordinary_manifest_rule": "omit_stream_processor",
        "choice_budget": ACP_STREAM_PROCESSING_POLICY["choice_budget"],
        "decision_ladder": ACP_STREAM_PROCESSING_POLICY["decision_ladder"],
        "choice_lock": ACP_STREAM_PROCESSING_POLICY["developer_choice_lock"],
        "validation": validation,
        "diagnostics": tuple(diagnostics),
        "quick_fixes": tuple(quick_fixes),
        "normal_form_manifest": normal_form,
        "generated_imports": generated_imports,
    }


def select_acp_stream_processor(workload: str) -> dict:
    """Select the platform-owned runtime profile for an APC workload description."""
    text = workload.lower().replace("-", "_")
    if any(term in text for term in ("time_series", "telemetry", "high_throughput", "event_data", "ingestion")):
        selected = "quix_streams"
    elif any(term in text for term in ("parallel", "dataflow", "transform", "pipeline")):
        selected = "bytewax"
    else:
        selected = ACP_DEFAULT_STREAM_PROCESSOR
    profile = ACP_STREAM_PROCESSORS[selected]
    return {
        "format": "appgen.acp-stream-processor-selection.v1",
        "ok": True,
        "workload": workload,
        "selected": selected,
        "default": ACP_DEFAULT_STREAM_PROCESSOR,
        "decision": "default" if selected == ACP_DEFAULT_STREAM_PROCESSOR else "exception",
        "profile": {"processor": selected, **profile},
        "reason": profile["primary_use_case"],
        "rules": ACP_STREAM_PROCESSOR_DECISION_RULES,
        "developer_visible": False,
        "selection_owner": "platform_runtime",
        "ordinary_generator_api": "resolve_acp_event_processing_choice",
        "ordinary_developer_answer": "Use appgen_event_contract.",
    }


def resolve_acp_event_processing_choice(workload: str, *, has_stream_exception_evidence: bool = False) -> dict:
    """Return the developer-facing event-processing action for generation."""
    candidate = select_acp_stream_processor(workload)
    is_exception_candidate = candidate["decision"] == "exception"
    exception_allowed = is_exception_candidate and has_stream_exception_evidence
    if exception_allowed:
        selected_profile = candidate["selected"]
        return {
            "format": "appgen.acp-event-processing-choice-resolution.v1",
            "ok": True,
            "workload": workload,
            "action": "generate_exception_pbc",
            "developer_answer": f"Use the {selected_profile} exception profile only for this split specialized PBC.",
            "public_contract": "specialized_exception_pbc",
            "manifest_rule": f"stream_processor={selected_profile}",
            "selected_runtime_profile": selected_profile,
            "candidate_profile": selected_profile,
            "requires_stream_exception_evidence": True,
            "missing_stream_exception_evidence": False,
            "must_split_workload": True,
            "developer_visible_options": ("appgen_event_contract",),
            "choice_budget": ACP_STREAM_PROCESSING_POLICY["choice_budget"],
            "do_not_compare_runtimes": True,
            "generated_business_logic_import_rule": "appgen_event_adapter_only",
            "api_call_order": ACP_STREAM_PROCESSING_POLICY["developer_action_contract"]["api_call_order"],
            "stream_selector_exposed_to_developer": False,
        }
    action = "fallback_to_appgen_event_contract" if is_exception_candidate else "generate_appgen_event_contract"
    return {
        "format": "appgen.acp-event-processing-choice-resolution.v1",
        "ok": True,
        "workload": workload,
        "action": action,
        "developer_answer": "Use appgen_event_contract.",
        "public_contract": "appgen_event_contract",
        "manifest_rule": "omit_stream_processor",
        "selected_runtime_profile": ACP_DEFAULT_STREAM_PROCESSOR,
        "candidate_profile": candidate["selected"],
        "blocked_exception_profile": candidate["selected"] if is_exception_candidate else None,
        "requires_stream_exception_evidence": is_exception_candidate,
        "missing_stream_exception_evidence": is_exception_candidate,
        "must_split_workload": False,
        "developer_visible_options": ("appgen_event_contract",),
        "choice_budget": ACP_STREAM_PROCESSING_POLICY["choice_budget"],
        "do_not_compare_runtimes": True,
        "generated_business_logic_import_rule": "appgen_event_adapter_only",
        "api_call_order": ACP_STREAM_PROCESSING_POLICY["developer_action_contract"]["api_call_order"],
        "stream_selector_exposed_to_developer": False,
    }


def pbc_manifest_schema() -> dict:
    """Return the contract every self-registering PBC package must implement."""
    return {
        "format": "appgen.pbc-manifest-schema.v1",
        "required_fields": PBC_MANIFEST_REQUIRED_FIELDS,
        "optional_fields": PBC_MANIFEST_OPTIONAL_FIELDS,
        "field_contracts": {
            "pbc": "Stable lowercase snake_case key. Used in routes, datastore, topics, and generated tables.",
            "label": "Human-facing catalog label.",
            "mesh": f"One of: {', '.join(sorted(PBC_MESHES))}.",
            "description": "One-sentence bounded-context purpose.",
            "datastore_backend": (
                "One of the approved open-source relational datastore backends: "
                + ", ".join(PBC_ALLOWED_DATASTORE_BACKENDS)
                + "."
            ),
            "tables": "Tuple of owned table names. Do not list tables owned by another PBC.",
            "apis": "Tuple of command/query route contracts, for example POST /orders.",
            "emits": "Tuple of domain events emitted by this PBC.",
            "consumes": "Tuple of domain events consumed from other PBCs or external systems.",
            "template": "Optional ERP template bridge key.",
            "stream_processor": (
                "Optional event processing backend key. One of: "
                + ", ".join(sorted(ACP_STREAM_PROCESSORS))
                + "."
            ),
            "stream_exception_evidence": (
                "Required only when stream_processor is an exception profile. "
                "Must include workload_name, throughput_or_latency_reason, "
                "state_shape, and operational_owner."
            ),
            "ui_fragments": "Optional generated UI fragment descriptors for the composition canvas.",
            "permissions": "Optional RBAC/ABAC permission strings exposed by the PBC.",
            "configuration": "Optional environment/configuration keys required at install time.",
            "migrations": "Optional migration artifact paths owned by the PBC package.",
            "seed_data": "Optional seed artifact paths owned by the PBC package.",
            "tests": "Optional test artifact paths that prove the PBC package contract.",
            "docs": "Optional documentation artifact paths for builders and operators.",
            "capabilities": "Optional domain capability module names implemented by the PBC.",
            "standard_features": "Optional standard table-stakes features implemented by the PBC runtime.",
            "advanced_capabilities": "Optional advanced differentiating capabilities implemented by the PBC runtime.",
            "workflows": "Optional workflow/service method names implemented by the PBC.",
            "analytics": "Optional metrics/projections implemented by the PBC.",
        },
        "self_registration_entrypoint": "register_pbc() -> dict",
        "stream_processing_policy": acp_stream_processing_policy(),
        "registration_rules": (
            "Return a manifest matching this schema.",
            "Never share a datastore key with another PBC.",
            "Expose at least one API, one emitted event, and one owned table.",
            "Use event contracts for cross-PBC integration.",
            "Include tests and docs before publishing a reusable PBC package.",
        ),
    }


def validate_pbc_manifest(manifest: dict, *, existing_catalog: dict[str, dict] | None = None) -> dict:
    """Validate one PBC manifest before catalog registration."""
    catalog = existing_catalog if existing_catalog is not None else PBC_CATALOG
    missing = tuple(field for field in PBC_MANIFEST_REQUIRED_FIELDS if not manifest.get(field))
    key = manifest.get("pbc")
    mesh = manifest.get("mesh")
    invalid = []
    if key and not re.fullmatch(r"[a-z][a-z0-9_]*", str(key)):
        invalid.append("pbc must be lowercase snake_case")
    if mesh and mesh not in PBC_MESHES:
        invalid.append(f"mesh must be one of {', '.join(sorted(PBC_MESHES))}")
    backend = manifest.get("datastore_backend")
    if backend and backend not in PBC_ALLOWED_DATASTORE_BACKENDS:
        invalid.append(
            "datastore_backend must be one of "
            + ", ".join(PBC_ALLOWED_DATASTORE_BACKENDS)
        )
    stream_processor = manifest.get("stream_processor")
    if stream_processor and stream_processor not in ACP_STREAM_PROCESSORS:
        invalid.append(
            "stream_processor must be one of "
            + ", ".join(sorted(ACP_STREAM_PROCESSORS))
        )
    normalized_stream_processor = stream_processor or ACP_DEFAULT_STREAM_PROCESSOR
    exception_required = normalized_stream_processor != ACP_DEFAULT_STREAM_PROCESSOR
    evidence = manifest.get("stream_exception_evidence", {})
    if exception_required:
        if not isinstance(evidence, dict):
            invalid.append("stream_exception_evidence must be an object for exception stream processors")
            missing_exception_evidence = ACP_STREAM_PROCESSING_POLICY["exception_required_evidence"]
        else:
            missing_exception_evidence = tuple(
                field
                for field in ACP_STREAM_PROCESSING_POLICY["exception_required_evidence"]
                if not evidence.get(field)
            )
            if missing_exception_evidence:
                invalid.append(
                    "stream_exception_evidence missing required fields: "
                    + ", ".join(missing_exception_evidence)
                )
    else:
        missing_exception_evidence = ()
    if key and key in catalog:
        invalid.append(f"pbc key already registered: {key}")
    for field in ("tables", "apis", "emits", "consumes"):
        value = manifest.get(field, ())
        if value and (not isinstance(value, (tuple, list)) or not all(isinstance(item, str) and item for item in value)):
            invalid.append(f"{field} must be a tuple/list of strings")
    datastore = f"{key}_store" if key else None
    existing_datastores = {f"{name}_store" for name in catalog}
    if datastore and datastore in existing_datastores:
        invalid.append(f"datastore already exists: {datastore}")
    required_artifacts = ("tests", "docs")
    missing_publish_artifacts = tuple(field for field in required_artifacts if not manifest.get(field))
    return {
        "format": "appgen.pbc-manifest-validation.v1",
        "ok": not missing and not invalid,
        "publishable": not missing and not invalid and not missing_publish_artifacts,
        "manifest": manifest,
        "missing_fields": missing,
        "invalid": tuple(invalid),
        "stream_processor_decision": "default" if not exception_required else "exception",
        "missing_stream_exception_evidence": missing_exception_evidence,
        "missing_publish_artifacts": missing_publish_artifacts,
        "datastore": datastore,
        "normalized_descriptor": _pbc_descriptor_from_manifest(manifest) if not missing and not invalid else None,
    }


def register_pbc_manifest(manifest: dict, *, existing_catalog: dict[str, dict] | None = None) -> dict:
    """Return a side-effect-free self-registration plan for a PBC package."""
    validation = validate_pbc_manifest(manifest, existing_catalog=existing_catalog)
    if not validation["ok"]:
        return {
            "format": "appgen.pbc-registration-plan.v1",
            "ok": False,
            "decision": "blocked",
            "validation": validation,
            "catalog_patch": None,
            "next_actions": ("Fix manifest validation errors before registering.",),
        }
    descriptor = validation["normalized_descriptor"]
    return {
        "format": "appgen.pbc-registration-plan.v1",
        "ok": True,
        "decision": "approved" if validation["publishable"] else "draft",
        "validation": validation,
        "catalog_patch": {
            descriptor["pbc"]: {
                "label": descriptor["label"],
                "mesh": descriptor["mesh"],
                "description": descriptor["description"],
                "tables": descriptor["tables"],
                "datastore_backend": descriptor["datastore_backend"],
                "stream_processor": descriptor["stream_processor"],
                "stream_exception_evidence": descriptor["stream_exception_evidence"],
                "apis": descriptor["apis"],
                "emits": descriptor["emits"],
                "consumes": descriptor["consumes"],
                "template": descriptor["template"],
            }
        },
        "registration_steps": (
            "Load package register_pbc() entrypoint.",
            "Validate returned manifest.",
            "Add descriptor to the catalog registry.",
            "Expose API routes, event topics, UI fragments, permissions, docs, and tests.",
            "Run pbc_release_audit() before publishing.",
        ),
        "next_actions": ()
        if validation["publishable"]
        else ("Add tests and docs before publishing as a reusable PBC.",),
    }


def pbc_package_contract(package_name: str, manifest: dict) -> dict:
    """Return the installable package contract for a third-party PBC."""
    registration = register_pbc_manifest(manifest)
    descriptor = registration["validation"].get("normalized_descriptor")
    return {
        "format": "appgen.pbc-package-contract.v1",
        "ok": registration["ok"],
        "package": package_name,
        "entrypoint": f"{package_name}:register_pbc",
        "registration": registration,
        "descriptor": descriptor,
        "install_surfaces": (
            "catalog",
            "datastore",
            "api_routes",
            "event_topics",
            "ui_fragments",
            "permissions",
            "configuration",
            "docs",
            "tests",
        ),
        "usable": registration["ok"] and descriptor is not None,
    }


def load_pbc_package(package_ref: str | Path, *, existing_catalog: dict[str, dict] | None = None) -> dict:
    """Load a PBC package entrypoint from an importable module or local path."""
    ref = Path(package_ref) if not isinstance(package_ref, Path) else package_ref
    source_kind = "module"
    entrypoint = str(package_ref)
    try:
        if ref.exists():
            source_kind = "directory" if ref.is_dir() else "file"
            entry_file = ref / "__init__.py" if ref.is_dir() else ref
            if not entry_file.exists():
                return {
                    "format": "appgen.pbc-package-load-report.v1",
                    "ok": False,
                    "source": str(package_ref),
                    "source_kind": source_kind,
                    "error": f"missing entry file: {entry_file}",
                }
            module_name = f"appgen_pbc_package_{abs(hash(str(entry_file.resolve())))}"
            spec = importlib.util.spec_from_file_location(module_name, entry_file)
            if spec is None or spec.loader is None:
                raise ImportError(f"cannot create import spec for {entry_file}")
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
            entrypoint = f"{entry_file}:register_pbc"
        else:
            module = importlib.import_module(str(package_ref))
            entrypoint = f"{package_ref}:register_pbc"
        register = getattr(module, "register_pbc", None)
        if not callable(register):
            return {
                "format": "appgen.pbc-package-load-report.v1",
                "ok": False,
                "source": str(package_ref),
                "source_kind": source_kind,
                "entrypoint": entrypoint,
                "error": "register_pbc entrypoint is missing or not callable",
            }
        manifest = register()
        if not isinstance(manifest, dict):
            return {
                "format": "appgen.pbc-package-load-report.v1",
                "ok": False,
                "source": str(package_ref),
                "source_kind": source_kind,
                "entrypoint": entrypoint,
                "error": "register_pbc must return a manifest dict",
            }
        registration = register_pbc_manifest(manifest, existing_catalog=existing_catalog)
        contract = pbc_package_contract(str(package_ref), manifest)
        return {
            "format": "appgen.pbc-package-load-report.v1",
            "ok": registration["ok"],
            "source": str(package_ref),
            "source_kind": source_kind,
            "entrypoint": entrypoint,
            "manifest": manifest,
            "registration": registration,
            "contract": contract,
            "descriptor": registration["validation"].get("normalized_descriptor"),
        }
    except Exception as exc:  # pragma: no cover - surfaced in returned report
        return {
            "format": "appgen.pbc-package-load-report.v1",
            "ok": False,
            "source": str(package_ref),
            "source_kind": source_kind,
            "entrypoint": entrypoint,
            "error": str(exc),
        }


def discover_pbc_packages(package_refs: tuple[str | Path, ...] | list[str | Path]) -> dict:
    """Load multiple PBC packages without mutating the built-in catalog."""
    reports = tuple(load_pbc_package(ref) for ref in package_refs)
    return {
        "format": "appgen.pbc-package-discovery-report.v1",
        "ok": all(report["ok"] for report in reports),
        "loaded": reports,
        "catalog_patches": tuple(
            report["registration"]["catalog_patch"]
            for report in reports
            if report.get("registration", {}).get("catalog_patch")
        ),
        "blocking_gaps": tuple(report for report in reports if not report["ok"]),
    }


def pbc_package_index_schema() -> dict:
    """Return the package index contract for reusable PBC packages."""
    return {
        "format": "appgen.pbc-package-index-schema.v1",
        "required_fields": ("packages",),
        "package_fields": {
            "name": "Stable package name shown in the package catalog.",
            "source": "Optional local directory or file path containing register_pbc().",
            "module": "Optional importable module path exposing register_pbc().",
            "version": "Optional semantic package version.",
            "publisher": "Optional package publisher or owning team.",
        },
        "rules": (
            "Each package entry must provide either source or module.",
            "Relative source paths resolve from the index file directory.",
            "Loading an index returns validation reports and catalog patches without mutating the built-in catalog.",
        ),
    }


def discover_pbc_package_index(index_path: str | Path) -> dict:
    """Load a package index file and validate each referenced PBC package."""
    path = Path(index_path)
    try:
        index = json.loads(path.read_text(encoding="utf-8"))
    except Exception as exc:
        return {
            "format": "appgen.pbc-package-index-discovery-report.v1",
            "ok": False,
            "index": str(index_path),
            "schema": pbc_package_index_schema(),
            "error": str(exc),
            "loaded": (),
            "blocking_gaps": ({"id": "index_read", "ok": False, "error": str(exc)},),
        }
    packages = index.get("packages", ())
    if not isinstance(packages, list):
        return {
            "format": "appgen.pbc-package-index-discovery-report.v1",
            "ok": False,
            "index": str(index_path),
            "schema": pbc_package_index_schema(),
            "error": "packages must be a list",
            "loaded": (),
            "blocking_gaps": ({"id": "packages_list", "ok": False},),
        }
    loaded = []
    invalid_entries = []
    for position, entry in enumerate(packages):
        if not isinstance(entry, dict) or (not entry.get("source") and not entry.get("module")):
            invalid_entries.append({"position": position, "entry": entry, "error": "entry must provide source or module"})
            continue
        raw_ref = entry.get("source") or entry["module"]
        if entry.get("source"):
            candidate = Path(raw_ref)
            package_ref = candidate if candidate.is_absolute() else path.parent / candidate
        else:
            package_ref = raw_ref
        report = load_pbc_package(package_ref)
        loaded.append(
            {
                "name": entry.get("name") or str(raw_ref),
                "version": entry.get("version"),
                "publisher": entry.get("publisher"),
                "source_kind": "source" if entry.get("source") else "module",
                "report": report,
            }
        )
    blocking = tuple(invalid_entries) + tuple(item for item in loaded if not item["report"]["ok"])
    return {
        "format": "appgen.pbc-package-index-discovery-report.v1",
        "ok": not blocking and bool(loaded),
        "index": str(index_path),
        "schema": pbc_package_index_schema(),
        "loaded": tuple(loaded),
        "catalog_patches": tuple(
            item["report"]["registration"]["catalog_patch"]
            for item in loaded
            if item["report"].get("registration", {}).get("catalog_patch")
        ),
        "blocking_gaps": blocking,
    }


def pbc_package_loading_smoke_audit() -> dict:
    """Prove PBC packages can be loaded from local source and import paths."""
    source_manifest = {**example_pbc_manifest(), "pbc": "source_warranty_claims"}
    module_manifest = {**example_pbc_manifest(), "pbc": "module_warranty_claims"}
    with tempfile.TemporaryDirectory(prefix="appgen-pbc-package-load-") as raw_tmp:
        root = Path(raw_tmp)
        source_pkg = root / "source_claims_pbc"
        source_pkg.mkdir()
        source_pkg.joinpath("__init__.py").write_text(
            "def register_pbc():\n"
            f"    return {source_manifest!r}\n",
            encoding="utf-8",
        )
        module_pkg = root / "module_claims_pbc"
        module_pkg.mkdir()
        module_pkg.joinpath("__init__.py").write_text(
            "def register_pbc():\n"
            f"    return {module_manifest!r}\n",
            encoding="utf-8",
        )
        source_report = load_pbc_package(source_pkg)
        sys.path.insert(0, str(root))
        try:
            sys.modules.pop("module_claims_pbc", None)
            module_report = load_pbc_package("module_claims_pbc")
            index_path = root / "pbc-packages.json"
            index_path.write_text(
                json.dumps(
                    {
                        "packages": [
                            {
                                "name": "Source Claims",
                                "source": "source_claims_pbc",
                                "version": "1.0.0",
                                "publisher": "appgen-tests",
                            },
                            {
                                "name": "Module Claims",
                                "module": "module_claims_pbc",
                                "version": "1.0.0",
                                "publisher": "appgen-tests",
                            },
                        ]
                    },
                    indent=2,
                ),
                encoding="utf-8",
            )
            index_discovery = discover_pbc_package_index(index_path)
        finally:
            try:
                sys.path.remove(str(root))
            except ValueError:
                pass
            sys.modules.pop("module_claims_pbc", None)
        discovery = discover_pbc_packages((source_pkg,))
    checks = (
        {"id": "local_source_directory", "ok": source_report["ok"] and source_report["source_kind"] == "directory"},
        {"id": "importable_module", "ok": module_report["ok"] and module_report["source_kind"] == "module"},
        {"id": "discovery_aggregate", "ok": discovery["ok"] and bool(discovery["catalog_patches"])},
        {"id": "package_index_discovery", "ok": index_discovery["ok"] and len(index_discovery["loaded"]) == 2},
        {
            "id": "side_effect_free_registration",
            "ok": source_report.get("registration", {}).get("decision") == "approved"
            and module_report.get("registration", {}).get("decision") == "approved",
        },
    )
    return {
        "format": "appgen.pbc-package-loading-smoke-audit.v1",
        "ok": all(check["ok"] for check in checks),
        "source_report": source_report,
        "module_report": module_report,
        "discovery": discovery,
        "index_discovery": index_discovery,
        "checks": checks,
        "blocking_gaps": tuple(check for check in checks if not check["ok"]),
    }


def pbc_lifecycle_documentation_audit() -> dict:
    """Verify PBC docs explain build, test, package, registration, and composition flows."""
    repo_root = Path(__file__).resolve().parents[2]
    documents = []
    for relative in PBC_LIFECYCLE_DOCUMENTATION_FILES:
        path = repo_root / relative
        try:
            text = path.read_text(encoding="utf-8")
        except OSError as exc:
            documents.append(
                {
                    "path": relative,
                    "ok": False,
                    "error": str(exc),
                    "text": "",
                }
            )
        else:
            documents.append(
                {
                    "path": relative,
                    "ok": True,
                    "word_count": len(re.findall(r"\b[\w-]+\b", text)),
                    "text": text,
                }
            )
    combined = "\n".join(document["text"] for document in documents).lower()
    missing_topics = tuple(
        topic for topic in PBC_LIFECYCLE_DOCUMENTATION_TOPICS if topic not in combined
    )
    missing_apis = tuple(
        api for api in PBC_LIFECYCLE_DOCUMENTATION_APIS if api.lower() not in combined
    )
    missing_artifacts = tuple(
        artifact for artifact in PBC_LIFECYCLE_DOCUMENTATION_ARTIFACTS if artifact.lower() not in combined
    )
    required_policy_terms = (
        "postgresql",
        "mysql",
        "mariadb",
        "appgen-x event",
        "stream-engine",
        "side-effect-free",
        "owned datastore",
        "dead-letter",
    )
    missing_policy_terms = tuple(term for term in required_policy_terms if term not in combined)
    checks = (
        {
            "id": "documents_present",
            "ok": all(document["ok"] for document in documents),
            "documents": tuple(
                {
                    "path": document["path"],
                    "ok": document["ok"],
                    "word_count": document.get("word_count", 0),
                    "error": document.get("error"),
                }
                for document in documents
            ),
        },
        {
            "id": "lifecycle_topics",
            "ok": not missing_topics,
            "missing": missing_topics,
            "required": PBC_LIFECYCLE_DOCUMENTATION_TOPICS,
        },
        {
            "id": "package_and_composition_apis",
            "ok": not missing_apis,
            "missing": missing_apis,
            "required": PBC_LIFECYCLE_DOCUMENTATION_APIS,
        },
        {
            "id": "generated_artifacts",
            "ok": not missing_artifacts,
            "missing": missing_artifacts,
            "required": PBC_LIFECYCLE_DOCUMENTATION_ARTIFACTS,
        },
        {
            "id": "policy_constraints",
            "ok": not missing_policy_terms,
            "missing": missing_policy_terms,
            "required": required_policy_terms,
        },
    )
    return {
        "format": "appgen.pbc-lifecycle-documentation-audit.v1",
        "ok": all(check["ok"] for check in checks),
        "documents": tuple(
            {
                "path": document["path"],
                "ok": document["ok"],
                "word_count": document.get("word_count", 0),
                "error": document.get("error"),
            }
            for document in documents
        ),
        "required_topics": PBC_LIFECYCLE_DOCUMENTATION_TOPICS,
        "required_apis": PBC_LIFECYCLE_DOCUMENTATION_APIS,
        "required_artifacts": PBC_LIFECYCLE_DOCUMENTATION_ARTIFACTS,
        "checks": checks,
        "blocking_gaps": tuple(check for check in checks if not check["ok"]),
    }


def pbc_source_runtime_test_coverage_audit(
    selected_pbcs: tuple[str, ...] | list[str] | None = None,
) -> dict:
    """Verify every built-in PBC has focused source runtime tests for required behavior."""
    selected = tuple(dict.fromkeys(selected_pbcs or IMPLEMENTED_PBC_KEYS))
    repo_root = Path(__file__).resolve().parents[2]
    contracts = []
    for key in selected:
        relative_path = f"tests/test_pbc_{key}_runtime.py"
        path = repo_root / relative_path
        try:
            text = path.read_text(encoding="utf-8")
        except OSError as exc:
            contracts.append(
                {
                    "pbc": key,
                    "ok": False,
                    "path": relative_path,
                    "error": str(exc),
                    "checks": (
                        {"id": "file_exists", "ok": False, "error": str(exc)},
                    ),
                    "blocking_gaps": (
                        {"id": "file_exists", "ok": False, "error": str(exc)},
                    ),
                }
            )
            continue
        lowered = text.lower()
        test_functions = tuple(re.findall(r"^def\s+(test_[a-zA-Z0-9_]+)\s*\(", text, flags=re.MULTILINE))
        concept_checks = []
        for concept in PBC_SOURCE_RUNTIME_TEST_REQUIRED_CONCEPTS:
            missing_terms = tuple(
                alternatives
                for alternatives in concept["terms"]
                if not any(term.lower() in lowered for term in alternatives)
            )
            concept_checks.append(
                {
                    "id": concept["id"],
                    "ok": not missing_terms,
                    "missing_terms": missing_terms,
                }
            )
        checks = (
            {
                "id": "file_exists",
                "ok": path.is_file(),
            },
            {
                "id": "stable_pbc_key_reference",
                "ok": key in lowered,
            },
            {
                "id": "focused_test_depth",
                "ok": len(test_functions) >= 2,
                "test_functions": test_functions,
            },
            *concept_checks,
        )
        contracts.append(
            {
                "pbc": key,
                "ok": all(check["ok"] for check in checks),
                "path": relative_path,
                "test_function_count": len(test_functions),
                "test_functions": test_functions,
                "checks": checks,
                "blocking_gaps": tuple(check for check in checks if not check["ok"]),
            }
        )
    return {
        "format": "appgen.pbc-source-runtime-test-coverage-audit.v1",
        "ok": bool(contracts) and all(contract["ok"] for contract in contracts),
        "pbc_count": len(contracts),
        "required_concepts": PBC_SOURCE_RUNTIME_TEST_REQUIRED_CONCEPTS,
        "contracts": tuple(contracts),
        "blocking_gaps": tuple(contract for contract in contracts if not contract["ok"]),
    }


def _pbc_runtime_capabilities(key: str) -> dict:
    """Return the package's advanced runtime capabilities, or raise.

    The package is the only source of truth for advanced capabilities. A
    missing entrypoint or an empty payload is a package defect, not an absent
    feature, so it must not degrade into an empty dict that silently passes
    the implementation contract.
    """
    package = importlib.import_module(f"pyAppGen.pbcs.{key}")
    entrypoint = getattr(package, f"{key}_runtime_capabilities", None)
    if not callable(entrypoint):
        raise AttributeError(
            f"PBC package {key!r} must export {key}_runtime_capabilities()"
        )
    capabilities = entrypoint()
    if not isinstance(capabilities, dict) or not capabilities:
        raise ValueError(
            f"PBC package {key!r} returned empty or non-dict runtime capabilities"
        )
    return capabilities


_PBC_FROZEN_CLOCK = datetime(2026, 1, 1, tzinfo=timezone.utc)


class _FrozenDateTime(datetime):
    """A `datetime` whose `now`/`utcnow` return a fixed instant."""

    @classmethod
    def now(cls, tz=None):
        return _PBC_FROZEN_CLOCK.astimezone(tz) if tz is not None else _PBC_FROZEN_CLOCK.replace(tzinfo=None)

    @classmethod
    def utcnow(cls):
        return _PBC_FROZEN_CLOCK.replace(tzinfo=None)


class _FrozenDate(date):
    """A `date` whose `today` returns the frozen instant's date."""

    @classmethod
    def today(cls):
        return _PBC_FROZEN_CLOCK.date()


@contextlib.contextmanager
def _pbc_frozen_clock(key: str):
    """Pin a package's wall clock for the duration of its contract build.

    Four packages (`contract_lifecycle`, `customer_success_management`,
    `case_knowledge_management`, `construction_contracts_commercials`) build their
    release evidence by *running* a scenario, and that scenario stamps rows with
    `datetime.now()`/`date.today()`. The emitter writes the resulting evidence
    verbatim into the generated `release_evidence.py`, so the generated artifact
    changed bytes every second and could not be reproduced. Rebinding the
    `datetime` and `date` names those modules imported (not the stdlib classes)
    keeps the scenario executable while making its output a function of its input.
    """
    prefix = f"pyAppGen.pbcs.{key}"
    patched: list[tuple[object, str, object]] = []
    for name, module in list(sys.modules.items()):
        if name != prefix and not name.startswith(f"{prefix}."):
            continue
        if getattr(module, "datetime", None) is datetime:
            patched.append((module, "datetime", datetime))
            setattr(module, "datetime", _FrozenDateTime)
        if getattr(module, "date", None) is date:
            patched.append((module, "date", date))
            setattr(module, "date", _FrozenDate)
    try:
        yield
    finally:
        for module, attribute, original in patched:
            setattr(module, attribute, original)


def _pbc_source_package_contract(key: str) -> dict:
    try:
        module = importlib.import_module(f"pyAppGen.pbcs.{key}")
        # The build runs the package's scenario, which stamps rows with the wall
        # clock; freeze it so the emitted artifact is a function of the source.
        with _pbc_frozen_clock(key):
            contract = module.implementation_contract()
            register = getattr(module, "register_pbc", None)
            registration_plan = getattr(module, "registration_plan", None)
            package_metadata_manifest = getattr(module, "package_metadata_manifest", None)
            validate_package_metadata = getattr(module, "validate_package_metadata", None)
            package_discovery_plan = getattr(module, "package_discovery_plan", None)
            manifest = register() if callable(register) else None
            registration = (
                registration_plan()
                if callable(registration_plan)
                else {
                    "format": "appgen.pbc-registration-plan.v1",
                    "ok": False,
                    "decision": "blocked",
                    "error": "registration_plan entrypoint is missing or not callable",
                }
            )
            metadata = package_metadata_manifest() if callable(package_metadata_manifest) else None
            metadata_validation = validate_package_metadata() if callable(validate_package_metadata) else None
            discovery = package_discovery_plan() if callable(package_discovery_plan) else None
    except Exception as exc:  # pragma: no cover - exercised by release audit failures
        return {
            "format": "appgen.pbc-source-package.v1",
            "ok": False,
            "pbc": key,
            "error": str(exc),
        }
    expected_directory = f"src/pyAppGen/pbcs/{key}"
    ok = (
        getattr(module, "PBC_KEY", None) == key
        and contract.get("pbc") == key
        and contract.get("implementation_directory") == expected_directory
        and contract.get("owns_code") is True
        and contract.get("side_effect_free") is True
        and isinstance(manifest, dict)
        and manifest.get("pbc") == key
        and tuple(manifest.get("standard_features", ())) == tuple(contract.get("standard_features", ()))
        and tuple(manifest.get("advanced_capabilities", ())) == tuple(contract.get("advanced_runtime", {}).get("capabilities", ()))
        and registration.get("ok") is True
        and registration.get("decision") in {"approved", "draft"}
        and key in (registration.get("catalog_patch") or {})
        and isinstance(metadata, dict)
        and metadata.get("pbc") == key
        and metadata.get("stream_engine_picker_visible") is False
        and metadata.get("event_contract") == "AppGen-X"
        and isinstance(metadata_validation, dict)
        and metadata_validation.get("ok") is True
        and isinstance(discovery, dict)
        and discovery.get("ok") is True
        and discovery.get("side_effects") == ()
    )
    return {
        **contract,
        "ok": ok,
        "module": module.__name__,
        "expected_directory": expected_directory,
        "manifest": manifest,
        "registration": registration,
        "package_metadata": metadata,
        "package_metadata_validation": metadata_validation,
        "package_discovery": discovery,
    }


def pbc_source_artifact_contract(key: str) -> dict:
    """Verify the source PBC directory contains the real package artifacts."""
    if key not in PBC_CATALOG:
        return {
            "format": "appgen.pbc-source-artifact-contract.v1",
            "ok": False,
            "pbc": key,
            "error": "unknown PBC",
        }
    source_dir = Path(__file__).resolve().parent / "pbcs" / key
    relative_dir = f"src/pyAppGen/pbcs/{key}"
    files = []
    missing = []
    compile_failures = []
    for artifact in PBC_SOURCE_PACKAGE_REQUIRED_ARTIFACTS:
        path = source_dir / artifact
        exists = path.is_file()
        files.append(
            {
                "artifact": artifact,
                "path": f"{relative_dir}/{artifact}",
                "exists": exists,
            }
        )
        if not exists:
            missing.append(artifact)
            continue
        if artifact.endswith(".py"):
            try:
                py_compile.compile(str(path), doraise=True)
            except py_compile.PyCompileError as exc:
                compile_failures.append(
                    {
                        "artifact": artifact,
                        "path": f"{relative_dir}/{artifact}",
                        "error": str(exc),
                    }
                )
    migration_path = source_dir / "migrations" / "001_initial.sql"
    migration_text = migration_path.read_text(encoding="utf-8") if migration_path.is_file() else ""
    manifest_text = (source_dir / "manifest.py").read_text(encoding="utf-8") if (source_dir / "manifest.py").is_file() else ""
    service_text = (source_dir / "services.py").read_text(encoding="utf-8") if (source_dir / "services.py").is_file() else ""
    route_text = (source_dir / "routes.py").read_text(encoding="utf-8") if (source_dir / "routes.py").is_file() else ""
    events_text = (source_dir / "events.py").read_text(encoding="utf-8") if (source_dir / "events.py").is_file() else ""
    handler_text = (source_dir / "handlers.py").read_text(encoding="utf-8") if (source_dir / "handlers.py").is_file() else ""
    release_evidence_py_text = (
        (source_dir / "release_evidence.py").read_text(encoding="utf-8")
        if (source_dir / "release_evidence.py").is_file()
        else ""
    )
    ui_text = (source_dir / "ui.py").read_text(encoding="utf-8") if (source_dir / "ui.py").is_file() else ""
    config_text = (source_dir / "config.py").read_text(encoding="utf-8") if (source_dir / "config.py").is_file() else ""
    permissions_text = (
        (source_dir / "permissions.py").read_text(encoding="utf-8")
        if (source_dir / "permissions.py").is_file()
        else ""
    )
    seed_text = (source_dir / "seed_data.py").read_text(encoding="utf-8") if (source_dir / "seed_data.py").is_file() else ""
    release_text = (source_dir / "RELEASE_EVIDENCE.md").read_text(encoding="utf-8") if (source_dir / "RELEASE_EVIDENCE.md").is_file() else ""
    tests_text = (
        (source_dir / "tests" / "test_contract.py").read_text(encoding="utf-8")
        if (source_dir / "tests" / "test_contract.py").is_file()
        else ""
    )
    init_text = (source_dir / "__init__.py").read_text(encoding="utf-8") if (source_dir / "__init__.py").is_file() else ""
    capability_assurance_text = (
        (source_dir / "capability_assurance.py").read_text(encoding="utf-8")
        if (source_dir / "capability_assurance.py").is_file()
        else ""
    )
    agent_text = (
        (source_dir / "agent.py").read_text(encoding="utf-8")
        if (source_dir / "agent.py").is_file()
        else ""
    )
    checks = (
        {
            "id": "required_source_artifacts_exist",
            "ok": not missing,
            "missing": tuple(missing),
        },
        {
            "id": "source_python_artifacts_compile",
            "ok": not compile_failures,
            "failures": tuple(compile_failures),
        },
        {
            "id": "owned_migration_materialized",
            "ok": "CREATE TABLE" in migration_text and f"{key}_" in migration_text,
            "path": f"{relative_dir}/migrations/001_initial.sql",
        },
        {
            "id": "manifest_materialized",
            "ok": "PBC_MANIFEST" in manifest_text and repr(key) in manifest_text,
            "path": f"{relative_dir}/manifest.py",
        },
        {
            "id": "manifest_capability_surface_materialized",
            "ok": "standard_features" in manifest_text
            and "advanced_capabilities" in manifest_text
            and "advanced_capabilities': ()" not in manifest_text
            and '"advanced_capabilities": ()' not in manifest_text,
            "path": f"{relative_dir}/manifest.py",
        },
        {
            "id": "capability_assurance_materialized",
            "ok": "def table_stakes_capability_manifest(" in capability_assurance_text
            and "def validate_table_stakes_capability_coverage(" in capability_assurance_text
            and "def smoke_test(" in capability_assurance_text
            and "event_contract" in capability_assurance_text
            and "stream_picker_visible" in capability_assurance_text
            and "invalid_backends" in capability_assurance_text,
            "path": f"{relative_dir}/capability_assurance.py",
        },
        {
            "id": "agent_chatbot_skills_materialized",
            "ok": "def agent_skill_manifest(" in agent_text
            and "def chatbot_interface_contract(" in agent_text
            and "def document_instruction_plan(" in agent_text
            and "def datastore_crud_plan(" in agent_text
            and "def composed_agent_contribution(" in agent_text
            and "def smoke_test(" in agent_text
            and "stream_engine_picker_visible" in agent_text
            and "single_agent_skill_namespace" in agent_text,
            "path": f"{relative_dir}/agent.py",
        },
        {
            "id": "self_registration_entrypoints_materialized",
            "ok": "def register_pbc(" in init_text
            and "def registration_plan(" in init_text
            and "def package_metadata_manifest(" in init_text
            and "def validate_package_metadata(" in init_text
            and "def package_discovery_plan(" in init_text
            and "source_registration_plan" in init_text,
            "path": f"{relative_dir}/__init__.py",
        },
        {
            "id": "service_layer_materialized",
            "ok": "class " in service_text
            and "transaction_boundary" in service_text
            and "owned_datastore_plus_outbox" in service_text,
            "path": f"{relative_dir}/services.py",
        },
        {
            "id": "service_route_runtime_surface_materialized",
            "ok": "def service_operation_manifest(" in service_text
            and "def service_operation_contracts(" in service_text
            and "def operation_plan(" in service_text
            and "operation_contract" in service_text
            and "def api_route_contracts(" in route_text
            and "def validate_api_route_contracts(" in route_text
            and "idempotency_key" in route_text
            and "stream_engine_picker_visible" in route_text
            and "def smoke_test(" in service_text
            and "def dispatch_route(" in route_text
            and "def smoke_test(" in route_text,
            "paths": (
                f"{relative_dir}/services.py",
                f"{relative_dir}/routes.py",
            ),
        },
        {
            "id": "handler_runtime_surface_materialized",
            "ok": "def handler_manifest(" in handler_text
            and "def dispatch_event(" in handler_text
            and "def smoke_test(" in handler_text
            and "idempotency_key" in handler_text
            and "retry_policy" in handler_text
            and "dead_letter_table" in handler_text,
            "path": f"{relative_dir}/handlers.py",
        },
        {
            "id": "event_contract_runtime_surface_materialized",
            "ok": "def event_contract_manifest(" in events_text
            and "def validate_event_contract(" in events_text
            and "def build_event_envelope(" in events_text
            and "def event_dispatch_plan(" in events_text
            and "def smoke_test(" in events_text
            and "stream_engine_picker_visible" in events_text
            and "dead_letter_table" in events_text
            and "idempotency" in events_text,
            "path": f"{relative_dir}/events.py",
        },
        {
            "id": "governance_hooks_materialized",
            "ok": "def validate_configuration(" in config_text
            and "def configuration_manifest(" in config_text
            and "def parameter_manifest(" in config_text
            and "def set_parameter(" in config_text
            and "def rule_manifest(" in config_text
            and "def compile_rule(" in config_text
            and "def evaluate_rule(" in config_text
            and "def governance_smoke_test(" in config_text
            and "def authorize(" in permissions_text
            and "def permission_manifest(" in permissions_text
            and "def validate_seed_data(" in seed_text
            and "def seed_plan(" in seed_text
            and "def smoke_test(" in config_text
            and "def smoke_test(" in permissions_text
            and "def smoke_test(" in seed_text,
            "paths": (
                f"{relative_dir}/config.py",
                f"{relative_dir}/permissions.py",
                f"{relative_dir}/seed_data.py",
            ),
        },
        {
            "id": "ui_workbench_surface_materialized",
            "ok": f"def {key}_ui_contract(" in ui_text
            and f"def {key}_render_workbench(" in ui_text
            and "def smoke_test(" in ui_text
            and "configuration_editor" in ui_text
            and "stream_engine_picker_visible" in ui_text
            and "action_permissions" in ui_text,
            "path": f"{relative_dir}/ui.py",
        },
        {
            "id": "contract_tests_materialized",
            "ok": "test_generated_schema_service_and_release_evidence" in tests_text
            and "test_manifest_and_event_contract" in tests_text
            and "validate_event_contract" in tests_text
            and "event_contract_manifest" in tests_text
            and "release_readiness_manifest" in tests_text
            and "validate_release_evidence" in tests_text
            and "test_registration_plan_is_side_effect_free" in tests_text
            and "package_metadata_manifest" in tests_text
            and "validate_package_metadata" in tests_text
            and "package_discovery_plan" in tests_text
            and "test_service_and_route_surface_are_executable" in tests_text
            and "service_operation_contracts" in tests_text
            and "api_route_contracts" in tests_text
            and "validate_api_route_contracts" in tests_text
            and "operation_contract" in tests_text
            and "test_configuration_permissions_and_seed_hooks_are_executable" in tests_text
            and "governance_smoke_test" in tests_text,
            "path": f"{relative_dir}/tests/test_contract.py",
        },
        {
            "id": "handler_contract_tests_materialized",
            "ok": "test_event_handlers_are_idempotent_and_retryable" in tests_text,
            "path": f"{relative_dir}/tests/test_contract.py",
        },
        {
            "id": "release_evidence_materialized",
            "ok": "Release Evidence" in release_text
            and f"pbcs/{key}" in release_text
            and "def release_readiness_manifest(" in release_evidence_py_text
            and "def validate_release_evidence(" in release_evidence_py_text
            and "def smoke_test(" in release_evidence_py_text
            and "blocking_gaps" in release_evidence_py_text
            and "boundary_gaps" in release_evidence_py_text,
            "paths": (
                f"{relative_dir}/RELEASE_EVIDENCE.md",
                f"{relative_dir}/release_evidence.py",
            ),
        },
    )
    return {
        "format": "appgen.pbc-source-artifact-contract.v1",
        "ok": source_dir.is_dir() and all(check["ok"] for check in checks),
        "pbc": key,
        "directory": relative_dir,
        "required_artifacts": PBC_SOURCE_PACKAGE_REQUIRED_ARTIFACTS,
        "files": tuple(files),
        "checks": checks,
        "blocking_gaps": tuple(check for check in checks if not check["ok"]),
    }


def pbc_source_artifact_release_audit(selected_pbcs: tuple[str, ...] | list[str] | None = None) -> dict:
    """Verify every built-in PBC has materialized package files in source control."""
    selected = tuple(dict.fromkeys(selected_pbcs or tuple(PBC_CATALOG)))
    contracts = tuple(pbc_source_artifact_contract(key) for key in selected)
    return {
        "format": "appgen.pbc-source-artifact-release-audit.v1",
        "ok": bool(contracts) and all(contract["ok"] for contract in contracts),
        "pbc_count": len(contracts),
        "required_artifacts": PBC_SOURCE_PACKAGE_REQUIRED_ARTIFACTS,
        "contracts": contracts,
        "blocking_gaps": tuple(contract for contract in contracts if not contract["ok"]),
    }


def pbc_package_local_assurance_contract(key: str) -> dict:
    """Execute package-local assurance evidence for one built-in PBC."""
    source_dir = Path(__file__).resolve().parent / "pbcs" / key
    relative_dir = f"src/pyAppGen/pbcs/{key}"
    assurance_path = source_dir / "capability_assurance.py"
    runtime_test_path = source_dir / "tests" / "test_runtime_capabilities.py"
    checks = [
        {
            "id": "source_directory_exists",
            "ok": source_dir.is_dir(),
            "path": relative_dir,
        },
        {
            "id": "package_local_assurance_artifact_exists",
            "ok": assurance_path.is_file(),
            "capability_assurance": f"{relative_dir}/capability_assurance.py",
            "runtime_capability_tests": f"{relative_dir}/tests/test_runtime_capabilities.py",
        },
    ]
    evidence: dict[str, object] = {
        "mode": "capability_assurance" if assurance_path.is_file() else "missing_capability_assurance",
    }
    if assurance_path.is_file():
        try:
            py_compile.compile(str(assurance_path), doraise=True)
            module = importlib.import_module(f"pyAppGen.pbcs.{key}.capability_assurance")
            manifest = module.table_stakes_capability_manifest()
            validation = module.validate_table_stakes_capability_coverage()
            smoke = module.smoke_test()
            evidence.update(
                {
                    "manifest": manifest,
                    "validation": validation,
                    "smoke": smoke,
                }
            )
            checks.extend(
                (
                    {
                        "id": "capability_assurance_compiles",
                        "ok": True,
                        "path": f"{relative_dir}/capability_assurance.py",
                    },
                    {
                        "id": "table_stakes_manifest_executes",
                        "ok": manifest.get("ok") is True
                        and bool(manifest.get("standard_features"))
                        and bool(manifest.get("advanced_capabilities")),
                    },
                    {
                        "id": "capability_validation_executes",
                        "ok": validation.get("ok") is True
                        and not validation.get("missing_standard")
                        and not validation.get("missing_advanced")
                        and not validation.get("missing_operations")
                        and not validation.get("uncovered_features")
                        and not validation.get("invalid_tables")
                        and not validation.get("invalid_backends")
                        and validation.get("event_contract") == "AppGen-X"
                        and validation.get("stream_picker_visible") is False,
                    },
                    {
                        "id": "assurance_smoke_side_effect_free",
                        "ok": smoke.get("ok") is True and not smoke.get("side_effects"),
                    },
                )
            )
        except Exception as exc:  # pragma: no cover - surfaced by audit output
            checks.append(
                {
                    "id": "capability_assurance_executes",
                    "ok": False,
                    "path": f"{relative_dir}/capability_assurance.py",
                    "error": str(exc),
                }
            )
    elif runtime_test_path.is_file():
        try:
            py_compile.compile(str(runtime_test_path), doraise=True)
            text = runtime_test_path.read_text(encoding="utf-8")
            lowered = text.lower()
            runtime = importlib.import_module(f"pyAppGen.pbcs.{key}.runtime")
            runtime_capabilities = getattr(runtime, f"{key}_runtime_capabilities")()
            runtime_smoke = getattr(runtime, f"{key}_runtime_smoke")()
            evidence.update(
                {
                    "runtime_capabilities": runtime_capabilities,
                    "runtime_smoke": runtime_smoke,
                    "test_path": f"{relative_dir}/tests/test_runtime_capabilities.py",
                }
            )
            checks.extend(
                (
                    {
                        "id": "runtime_capability_test_compiles",
                        "ok": True,
                        "path": f"{relative_dir}/tests/test_runtime_capabilities.py",
                    },
                    {
                        "id": "runtime_capability_test_covers_table_stakes",
                        "ok": "standard" in lowered
                        and "advanced" in lowered
                        and "configuration" in lowered
                        and "rule" in lowered
                        and "parameter" in lowered
                        and "appgen-x" in lowered
                        and "boundary" in lowered,
                    },
                    {
                        "id": "runtime_capabilities_execute",
                        "ok": runtime_capabilities.get("ok") is True
                        and bool(runtime_capabilities.get("standard_features"))
                        and bool(runtime_capabilities.get("capabilities")),
                    },
                    {
                        "id": "runtime_smoke_executes",
                        "ok": runtime_smoke.get("ok") is True
                        and not tuple(runtime_smoke.get("blocking_gaps", ())),
                    },
                )
            )
        except Exception as exc:  # pragma: no cover - surfaced by audit output
            checks.append(
                {
                    "id": "runtime_capability_assurance_executes",
                    "ok": False,
                    "path": f"{relative_dir}/tests/test_runtime_capabilities.py",
                    "error": str(exc),
                }
            )
    return {
        "format": "appgen.pbc-package-local-assurance-contract.v1",
        "ok": all(check["ok"] for check in checks),
        "pbc": key,
        "directory": relative_dir,
        "assurance_artifact": (
            f"{relative_dir}/capability_assurance.py"
            if assurance_path.is_file()
            else f"{relative_dir}/tests/test_runtime_capabilities.py"
        ),
        "checks": tuple(checks),
        "evidence": evidence,
        "blocking_gaps": tuple(check for check in checks if not check["ok"]),
    }


def pbc_package_local_assurance_audit(selected_pbcs: tuple[str, ...] | list[str] | None = None) -> dict:
    """Verify every implemented PBC has executable package-local capability assurance."""
    selected = tuple(dict.fromkeys(selected_pbcs or IMPLEMENTED_PBC_KEYS))
    contracts = tuple(pbc_package_local_assurance_contract(key) for key in selected)
    return {
        "format": "appgen.pbc-package-local-assurance-audit.v1",
        "ok": bool(contracts) and all(contract["ok"] for contract in contracts),
        "pbc_count": len(contracts),
        "contracts": contracts,
        "blocking_gaps": tuple(contract for contract in contracts if not contract["ok"]),
    }


def _pbc_specification_path(key: str) -> Path:
    return Path(__file__).resolve().parent / "pbcs" / key / "SPECIFICATION.md"


def _missing_specification_concepts(text: str, key: str) -> tuple[dict, ...]:
    lowered = text.lower()
    missing = []
    for concept in PBC_SPECIFICATION_REQUIRED_CONCEPTS:
        missing_terms = tuple(
            alternatives
            for alternatives in concept["terms"]
            if not any(term.lower() in lowered for term in alternatives)
        )
        if missing_terms:
            missing.append(
                {
                    "id": concept["id"],
                    "missing_terms": missing_terms,
                }
            )
    if key.lower() not in lowered:
        missing.append({"id": "stable_pbc_key", "missing_terms": ((key,),)})
    return tuple(missing)


def _normalized_specification_token(value: object) -> str:
    return re.sub(r"[^a-z0-9]+", "_", str(value).lower()).strip("_")


def _pbc_specification_manifest_traceability(text: str, key: str) -> dict:
    manifest = PBC_CATALOG[key]
    # All nine traceability fields now come from the descriptor, which reads each
    # one from the package. Before, only four did, and the other five
    # (`ui_fragments`, `permissions`, `configuration`, `standard_features`,
    # `advanced_capabilities`) were read from the catalog literal -- which the
    # descriptor migration had emptied. That made the check vacuous twice over:
    # the three reference PBCs' `tables`/`emits`/`consumes` literals were deleted,
    # so the loop ran over an empty set and certified a specification against
    # nothing (`gl_core` passed while its appendix and its package were never
    # compared), and the five literal-only fields were empty for every package, so
    # the sectioned appendices said "None declared" while the packages declared
    # thirteen fragments. A check that loops over a deleted literal is the "gate
    # that never ran" again. The literal survives only as the fallback for an
    # entry whose package cannot be imported, which the descriptor also falls back
    # to, so a package that imports is checked against itself.
    descriptor = _pbc_descriptor(key, manifest)
    normalized_text = _normalized_specification_token(text)
    field_results = []
    for field in PBC_SPECIFICATION_TRACEABILITY_FIELDS:
        source = descriptor.get(field) if field in descriptor else manifest.get(field, ())
        values = tuple(source or ())
        missing = []
        for value in values:
            normalized = _normalized_specification_token(value)
            alternatives = {normalized}
            if field == "tables":
                alternatives.add(_normalized_specification_token(f"{key}_{value}"))
            if not any(alternative and alternative in normalized_text for alternative in alternatives):
                missing.append(value)
        field_results.append(
            {
                "field": field,
                "ok": not missing,
                "declared_count": len(values),
                "missing": tuple(missing),
            }
        )
    appendix_present = "manifest traceability appendix" in text.lower()
    return {
        "format": "appgen.pbc-specification-manifest-traceability.v1",
        "ok": appendix_present and all(result["ok"] for result in field_results),
        "pbc": key,
        "appendix_present": appendix_present,
        "fields": tuple(field_results),
        "blocking_gaps": tuple(result for result in field_results if not result["ok"]),
    }


def pbc_specification_contract(key: str) -> dict:
    """Return release evidence for the package-local PBC specification."""
    path = _pbc_specification_path(key)
    relative_path = f"src/pyAppGen/pbcs/{key}/SPECIFICATION.md"
    if key not in PBC_CATALOG:
        return {
            "format": "appgen.pbc-specification-contract.v1",
            "ok": False,
            "pbc": key,
            "path": relative_path,
            "error": "unknown PBC",
        }
    try:
        text = path.read_text(encoding="utf-8")
    except OSError as exc:
        return {
            "format": "appgen.pbc-specification-contract.v1",
            "ok": False,
            "pbc": key,
            "path": relative_path,
            "error": str(exc),
        }
    word_count = len(re.findall(r"\b[\w-]+\b", text))
    heading_count = len(re.findall(r"^##\s+", text, flags=re.MULTILINE))
    missing_concepts = _missing_specification_concepts(text, key)
    restricted_references = tuple(
        pattern
        for pattern in PBC_RESTRICTED_LEGACY_REFERENCES
        if re.search(pattern, text)
    )
    manifest_traceability = _pbc_specification_manifest_traceability(text, key)
    checks = (
        {
            "id": "file_exists",
            "ok": path.is_file(),
        },
        {
            "id": "minimum_depth",
            "ok": word_count >= PBC_SPECIFICATION_MIN_WORDS and heading_count >= 6,
            "word_count": word_count,
            "heading_count": heading_count,
            "minimum_words": PBC_SPECIFICATION_MIN_WORDS,
        },
        {
            "id": "implementation_concepts",
            "ok": not missing_concepts,
            "missing_concepts": missing_concepts,
        },
        {
            "id": "restricted_legacy_references",
            "ok": not restricted_references,
            "references": restricted_references,
        },
        {
            "id": "manifest_traceability",
            "ok": manifest_traceability["ok"],
            "traceability": manifest_traceability,
        },
    )
    ok = all(check["ok"] for check in checks)
    return {
        "format": "appgen.pbc-specification-contract.v1",
        "ok": ok,
        "pbc": key,
        "path": relative_path,
        "word_count": word_count,
        "heading_count": heading_count,
        "required_concepts": PBC_SPECIFICATION_REQUIRED_CONCEPTS,
        "missing_concepts": missing_concepts,
        "manifest_traceability": manifest_traceability,
        "restricted_legacy_references": restricted_references,
        "checks": checks,
        "blocking_gaps": tuple(check for check in checks if not check["ok"]),
    }


def pbc_specification_release_audit(selected_pbcs: tuple[str, ...] | list[str] | None = None) -> dict:
    """Verify every requested built-in PBC has a comprehensive package-local specification."""
    selected = tuple(dict.fromkeys(selected_pbcs or tuple(PBC_CATALOG)))
    contracts = tuple(pbc_specification_contract(key) for key in selected)
    return {
        "format": "appgen.pbc-specification-release-audit.v1",
        "ok": bool(contracts) and all(contract["ok"] for contract in contracts),
        "pbc_count": len(contracts),
        "minimum_words": PBC_SPECIFICATION_MIN_WORDS,
        "required_concepts": PBC_SPECIFICATION_REQUIRED_CONCEPTS,
        "contracts": contracts,
        "blocking_gaps": tuple(contract for contract in contracts if not contract["ok"]),
    }


def pbc_agent_capability_contract(key: str) -> dict:
    """Verify a PBC contributes executable agent, chatbot, skill, and CRUD evidence."""
    if key not in PBC_CATALOG:
        return {
            "format": "appgen.pbc-agent-capability-contract.v1",
            "ok": False,
            "pbc": key,
            "error": "unknown PBC",
        }
    try:
        agent_module = importlib.import_module(f"pyAppGen.pbcs.{key}.agent")
        skills = agent_module.agent_skill_manifest()
        chatbot = agent_module.chatbot_interface_contract()
        document = agent_module.document_instruction_plan("release evidence document", "create governed market record")
        read_plan = agent_module.datastore_crud_plan("read")
        create_plan = agent_module.datastore_crud_plan("create", payload={"status": "draft"})
        rejected_plan = agent_module.datastore_crud_plan("update", table="foreign_operational_table")
        contribution = agent_module.composed_agent_contribution()
        smoke = agent_module.smoke_test()
    except Exception as exc:  # pragma: no cover - returned as release evidence
        return {
            "format": "appgen.pbc-agent-capability-contract.v1",
            "ok": False,
            "pbc": key,
            "error": str(exc),
            "blocking_gaps": ({"id": "agent_module_import_or_execution", "ok": False, "error": str(exc)},),
        }
    skill_rows = tuple(skills.get("skills", ()))
    namespace = f"{key}_skills"
    checks = (
        {
            "id": "agent_skill_manifest",
            "ok": skills.get("ok") is True
            and bool(skill_rows)
            and all(row.get("scope") == key for row in skill_rows)
            and all(
                isinstance(row.get("requires_confirmation_for_mutation"), bool)
                for row in skill_rows
            )
            and all(
                row.get("requires_confirmation_for_mutation") is True
                for row in skill_rows
                if set(row.get("allowed_crud_actions") or ()) & _MUTATING_CRUD_ACTIONS
            )
            and all(row.get("uses_appgen_event_contract") is True for row in skill_rows),
        },
        {
            "id": "chatbot_interface_contract",
            "ok": chatbot.get("ok") is True
            and chatbot.get("entrypoint") == f"/assistant/pbc/{key}"
            and chatbot.get("single_agent_contribution") == namespace
            and "governed_datastore_crud" in tuple(chatbot.get("capabilities", ())),
        },
        {
            "id": "document_instruction_intake",
            "ok": document.get("ok") is True
            and document.get("requires_human_confirmation") is True
            and bool(_document_candidate_tables(document))
            and all(
                _is_owned_table_reference(key, str(table))
                for table in _document_candidate_tables(document)
            ),
        },
        {
            "id": "governed_crud_plans",
            "ok": read_plan.get("ok") is True
            and create_plan.get("ok") is True
            and create_plan.get("requires_confirmation") is True
            and rejected_plan.get("ok") is False
            and create_plan.get("event_contract") == "AppGen-X",
        },
        {
            "id": "composed_agent_contribution",
            "ok": contribution.get("ok") is True
            and contribution.get("single_agent_skill_namespace") == namespace
            and namespace in tuple(contribution.get("dsl_tools", ())),
        },
        {
            "id": "agent_smoke",
            "ok": smoke.get("ok") is True and smoke.get("side_effects") == (),
        },
    )
    return {
        "format": "appgen.pbc-agent-capability-contract.v1",
        "ok": all(check["ok"] for check in checks),
        "pbc": key,
        "namespace": namespace,
        "skills": skills,
        "chatbot": chatbot,
        "document": document,
        "read_plan": read_plan,
        "create_plan": create_plan,
        "rejected_plan": rejected_plan,
        "contribution": contribution,
        "smoke": smoke,
        "checks": checks,
        "blocking_gaps": tuple(check for check in checks if not check["ok"]),
        "side_effects": (),
    }


def pbc_agent_capability_release_audit(selected_pbcs: tuple[str, ...] | list[str] | None = None) -> dict:
    """Verify every requested PBC contributes executable composed-agent skills."""
    selected = tuple(dict.fromkeys(selected_pbcs or tuple(PBC_CATALOG)))
    contracts = tuple(pbc_agent_capability_contract(key) for key in selected)
    return {
        "format": "appgen.pbc-agent-capability-release-audit.v1",
        "ok": bool(contracts) and all(contract["ok"] for contract in contracts),
        "pbc_count": len(contracts),
        "contracts": contracts,
        "blocking_gaps": tuple(contract for contract in contracts if not contract["ok"]),
    }


def pbc_implementation_contract(key: str) -> dict:
    """Return the generated implementation contract for one built-in PBC."""
    if key not in PBC_CATALOG:
        return {
            "format": "appgen.pbc-implementation-contract.v1",
            "ok": False,
            "pbc": key,
            "error": "unknown PBC",
        }
    service = _service_contract(key)
    primary_table = service["tables"][0]
    # Packages disagree on whether `_owned_tables` reports logical or physical
    # names (`dam_core` reports `asset`, `gl_core` reports
    # `gl_core_ledger_event_log`). It is passed on its own so the suffix match
    # in `_owned_table_name` stays unambiguous; the migration's own names are
    # matched separately in `_table_fields`.
    owned = _owned_tables(key)
    table_contracts = tuple(
        _table_contract(key, table, primary_table, position, owned)
        for position, table in enumerate(service["tables"])
    )
    event_contract = _event_contract(key, service)
    # The package's own route surface is the authority for the app's routes. It
    # replaces `_api_contract` over the catalog literal, which invented numbered
    # permissions (`dam_core.command.1`) and had no per-operation table scope or
    # event. `_package_route_records` reads the package's `routes.py` and falls
    # back to the literal only for an unimportable package.
    service_methods = _package_route_records(key)
    # The package's own UI contract is the authority for its fragments and
    # panels. The catalog literal and the `ClassWorkbench`/`ClassDetail`
    # fallback both under-report: for `dam_core` they yield two fragment names
    # against a package that declares six, and `ar_credit` sixteen. Reading the
    # package here is what makes the generated workbench render the capability
    # the block actually carries rather than a placeholder pair. It is read
    # once and reused below, since building it re-executes the package's
    # contract surface.
    source_package = _pbc_source_package_contract(key)
    package_ui = source_package.get("ui_contract") or {}
    ui_fragments = tuple(
        package_ui.get("fragments", ())
        or service.get("ui_fragments", ())
        or (
            f"{service['class_name']}Workbench",
            f"{service['class_name']}Detail",
        )
    )
    permissions = tuple(
        service.get("permissions", ())
        or tuple(
            f"{key}.{verb}"
            for verb in ("read", "create", "update", "approve", "admin")
        )
    )
    configuration = tuple(
        service.get("configuration", ())
        or (
            f"{key.upper()}_DATABASE_URL",
            f"{key.upper()}_EVENT_TOPIC",
            f"{key.upper()}_RETRY_LIMIT",
        )
    )
    migration_sql = _migration_sql(key, table_contracts, event_contract)
    domain_functionality = _domain_functionality_contract(
        key,
        service,
        table_contracts,
        event_contract,
        service_methods,
    )
    advanced_blueprint = _advanced_domain_blueprint(key, service, table_contracts, event_contract, service_methods)
    advanced_runtime = _pbc_runtime_capabilities(key)
    release_checks = (
        "stable_manifest",
        "source_package_directory",
        "owned_schema_only",
        "migration_artifact",
        "model_artifact",
        "domain_capability_depth",
        "workflow_coverage",
        "policy_control_coverage",
        "automation_loop_coverage",
        "analytics_coverage",
        "advanced_domain_blueprint" if advanced_blueprint else "advanced_domain_not_required",
        "service_commands",
        "api_routes",
        "event_outbox_inbox",
        "typed_emitted_events",
        "typed_consumed_events",
        "idempotent_handlers",
        "retry_dead_letter_policy",
        "ui_fragments",
        "permissions",
        "configuration_schema",
        "seed_data",
        "self_registration_metadata",
        "contract_tests",
    )
    return {
        "format": "appgen.pbc-implementation-contract.v1",
        "ok": True,
        "pbc": key,
        "directory": f"pbcs/{key}",
        "manifest": {
            "pbc": key,
            "label": service["label"],
            "mesh": service["mesh"],
            "description": service["description"],
            "datastore_backend": service["datastore_backend"],
            "tables": service["tables"],
            "apis": service["apis"],
            "emits": service["emits"],
            "consumes": service["consumes"],
            "template": service["template"],
            "ui_fragments": ui_fragments,
            "permissions": permissions,
            "configuration": configuration,
            "capabilities": tuple(item["capability"] for item in domain_functionality["capability_modules"]),
            "standard_features": tuple(advanced_runtime.get("standard_features", ())),
            "workflows": tuple(item["workflow"] for item in domain_functionality["workflow_implementations"]),
            "analytics": tuple(item["metric"] for item in domain_functionality["analytics"]),
            "advanced_capabilities": tuple(advanced_runtime.get("capabilities", ()))
            or tuple(item["capability"] for item in advanced_blueprint.get("capabilities", ())),
            "migrations": ("migrations/001_initial.sql",),
            "seed_data": ("seed_data.py",),
            "tests": ("tests/test_contract.py",),
            "docs": ("RELEASE_EVIDENCE.md",),
        },
        "mesh": service["mesh"],
        "datastore": service["datastore"],
        "datastore_backend": service["datastore_backend"],
        "owned_schema": {
            "schema": key,
            "table_prefix": f"{key}_",
            "tables": table_contracts,
            "relationships": tuple(
                relationship
                for table in table_contracts
                for relationship in table["relationships"]
            ),
            "allowed_external_access": "apis_events_or_projections_only",
            "unresolved_tables": _unresolved_manifest_tables(key),
        },
        "migrations": (
            {
                "path": "migrations/001_initial.sql",
                "operation": "create_owned_schema",
                "sql": migration_sql,
            },
        ),
        "domain_functionality": domain_functionality,
        "advanced_domain_blueprint": advanced_blueprint,
        "advanced_runtime": advanced_runtime,
        "source_package": source_package,
        "models": tuple(
            {
                "class_name": "".join(part.capitalize() for part in table["owned_table"].split("_")),
                "table": table["owned_table"],
                "fields": table["fields"],
                "relationships": table["relationships"],
            }
            for table in table_contracts
        ),
        "services": {
            "class_name": f"{service['class_name']}Service",
            "command_methods": service_methods,
            "transaction_boundary": "owned_datastore_plus_outbox",
            "mutates_only": tuple(table["owned_table"] for table in table_contracts),
        },
        "apis": service_methods,
        "events": event_contract,
        "handlers": tuple(
            {
                "event_type": event["event_type"],
                "function": f"handle_{_snake(event['event_type'])}",
                "idempotency_key": f"{key}:{event['event_type']}:{{event_id}}",
                "retry_policy": event_contract["retry_policy"],
                "dead_letter_table": event_contract["dead_letter_table"],
                "side_effect_boundary": "owned_tables_or_declared_api_calls",
            }
            for event in event_contract["consumed"]
        ),
        "ui": {
            "fragments": ui_fragments,
            "panels": tuple(package_ui.get("panels", ())),
            "routes": tuple(package_ui.get("routes", ())) or (f"/workbench/pbcs/{key}",),
            "workbench_view": f"{service['class_name']}Workbench",
            "route": f"/workbench/pbcs/{key}",
            # The package declares what each panel binds to; the outbox table is
            # only the fallback when a package declares no binding at all.
            "binds_to": tuple(package_ui.get("panels", ())[0].get("binds_to", ()))
            if package_ui.get("panels")
            else event_contract["outbox_table"],
            # The package's editors and event surfaces, so the generated
            # workbench renders the configuration a `dam_core` installer must
            # supply and the events the block actually emits, instead of three
            # cards describing the contract's own shape.
            #
            # A package declares this surface in one of three shapes: the rich
            # dict (`dam_core` names its required keys and rule types), a bare
            # `True` meaning "I have an editor" with no content, or `None`. 48
            # of 147 packages carry the dict; the other 99 would otherwise
            # render an empty card, so each editor falls back to the contract's
            # own configuration, event, and permission surface, which every
            # package carries. `action_permissions` is a dict in 49 packages and
            # a flat permission tuple in 98, so the tuple form is keyed by the
            # permission's own verb to stay readable.
            "configuration_editor": {
                "required_fields": tuple(
                    (package_ui.get("configuration_editor") or {}).get("required_fields")
                    or configuration
                )
                if isinstance(package_ui.get("configuration_editor"), dict)
                else tuple(configuration),
                "allowed_database_backends": tuple(
                    (package_ui.get("configuration_editor") or {}).get("allowed_database_backends")
                    or (service["datastore_backend"],)
                )
                if isinstance(package_ui.get("configuration_editor"), dict)
                else (service["datastore_backend"],),
                "required_event_topic": (package_ui.get("configuration_editor") or {}).get("required_event_topic")
                if isinstance(package_ui.get("configuration_editor"), dict)
                else event_contract["topic"],
                "stream_engine_picker_visible": bool(
                    (package_ui.get("configuration_editor") or {}).get("stream_engine_picker_visible", False)
                )
                if isinstance(package_ui.get("configuration_editor"), dict)
                else False,
            },
            "rule_editor": {
                "rule_types": tuple((package_ui.get("rule_editor") or {}).get("rule_types") or ("configuration", "parameter", "release_gate"))
                if isinstance(package_ui.get("rule_editor"), dict)
                else ("configuration", "parameter", "release_gate"),
                "required_fields": tuple(
                    (package_ui.get("rule_editor") or {}).get("required_fields")
                    or ("rule_id", "tenant", "scope", "status", "condition", "effect")
                )
                if isinstance(package_ui.get("rule_editor"), dict)
                else ("rule_id", "tenant", "scope", "status", "condition", "effect"),
                "compiled_evidence_required": bool(
                    (package_ui.get("rule_editor") or {}).get("compiled_evidence_required", True)
                )
                if isinstance(package_ui.get("rule_editor"), dict)
                else True,
            },
            "event_surfaces": {
                "emits": tuple(
                    (package_ui.get("event_surfaces") or {}).get("emits")
                    or (event["event_type"] for event in event_contract["emitted"])
                ),
                "consumes": tuple(
                    (package_ui.get("event_surfaces") or {}).get("consumes")
                    or (event["event_type"] for event in event_contract["consumed"])
                ),
                "outbox_status": (package_ui.get("event_surfaces") or {}).get("outbox_status", "visible")
                if isinstance(package_ui.get("event_surfaces"), dict)
                else "visible",
                "inbox_status": (package_ui.get("event_surfaces") or {}).get("inbox_status", "visible")
                if isinstance(package_ui.get("event_surfaces"), dict)
                else "visible",
                "dead_letter_status": (package_ui.get("event_surfaces") or {}).get("dead_letter_status", "visible")
                if isinstance(package_ui.get("event_surfaces"), dict)
                else "visible",
            },
            "action_permissions": dict(package_ui["action_permissions"])
            if isinstance(package_ui.get("action_permissions"), dict)
            else {
                permission.rsplit(".", 1)[-1]: permission
                for permission in (package_ui.get("action_permissions") or permissions)
            },
            "workflow_actions": tuple(package_ui.get("workflow_actions") or ()),
        },
        "permissions": permissions,
        "configuration": tuple(
            {
                "key": name,
                "required": name.endswith("_DATABASE_URL") or name.endswith("_EVENT_TOPIC"),
                "source": "environment",
            }
            for name in configuration
        ),
        "seed_data": tuple(
            {
                "table": table["owned_table"],
                "rows": (
                    {
                        "code": f"{key.upper()}-{position + 1:03d}",
                        "status": "active",
                    },
                ),
            }
            for position, table in enumerate(table_contracts[:2])
        ),
        "package_metadata": {
            "entrypoint": "register_pbc",
            "directory": f"pbcs/{key}",
            "registration_mode": "side_effect_free_plan",
            "artifacts": PBC_IMPLEMENTATION_REQUIRED_ARTIFACTS,
        },
        "release_evidence": {
            "checks": release_checks,
            "generated_files": PBC_IMPLEMENTATION_REQUIRED_ARTIFACTS,
            "cross_pbc_boundary": "no_shared_tables",
            "dependency_style": "apis_events_projections",
        },
    }


def pbc_implementation_contracts(selected_pbcs: tuple[str, ...] | list[str] | None = None) -> tuple[dict, ...]:
    """Return implementation contracts for selected or all built-in PBCs."""
    selected = tuple(dict.fromkeys(selected_pbcs or tuple(PBC_CATALOG)))
    return tuple(pbc_implementation_contract(key) for key in selected)


def _pbc_table_stakes_evidence(contract: dict) -> dict:
    runtime = contract.get("advanced_runtime", {})
    source = contract.get("source_package", {})
    standard_features = tuple(runtime.get("standard_features") or source.get("standard_features") or ())
    feature_text = " ".join(standard_features).lower()
    source_service = source.get("service_contract", {})
    command_text = " ".join(source_service.get("command_methods", ())).lower()
    checks = (
        {
            "id": "owned_schema_migrations_models",
            "ok": bool(contract.get("owned_schema", {}).get("tables"))
            and bool(contract.get("migrations"))
            and bool(contract.get("models")),
        },
        {
            "id": "service_api_route_contracts",
            "ok": bool(contract.get("services", {}).get("command_methods"))
            and bool(contract.get("apis")),
        },
        {
            "id": "appgen_event_contract",
            "ok": contract.get("events", {}).get("contract") == "appgen_event_contract"
            and bool(contract.get("events", {}).get("outbox_table"))
            and bool(contract.get("events", {}).get("inbox_table")),
        },
        {
            "id": "idempotent_handlers",
            "ok": bool(contract.get("handlers"))
            and all(
                handler.get("idempotency_key", "").startswith(f"{contract['pbc']}:")
                for handler in contract.get("handlers", ())
            ),
        },
        {
            "id": "retry_dead_letter_policy",
            "ok": contract.get("events", {}).get("retry_policy", {}).get("max_attempts", 0) >= 3
            and bool(contract.get("events", {}).get("dead_letter_table")),
        },
        {
            "id": "ui_workbench",
            "ok": bool(contract.get("ui", {}).get("fragments"))
            and bool(contract.get("ui", {}).get("workbench_view"))
            and "workbench" in feature_text,
        },
        {
            "id": "permissions_rbac",
            "ok": bool(contract.get("permissions"))
            and ("permission" in feature_text or "rbac" in feature_text),
        },
        {
            "id": "configuration_schema",
            "ok": bool(contract.get("configuration"))
            and ("configuration" in feature_text or "configure_runtime" in command_text),
        },
        {
            "id": "rule_engine",
            "ok": "rule" in feature_text or "register_rule" in command_text,
        },
        {
            "id": "parameter_engine",
            "ok": "parameter" in feature_text or "set_parameter" in command_text,
        },
        {
            "id": "seed_data",
            "ok": bool(contract.get("seed_data"))
            and bool(contract.get("manifest", {}).get("seed_data")),
        },
    )
    return {
        "format": "appgen.pbc-table-stakes-evidence.v1",
        "ok": all(check["ok"] for check in checks),
        "pbc": contract["pbc"],
        "required_evidence": PBC_TABLE_STAKES_REQUIRED_EVIDENCE,
        "checks": checks,
        "blocking_gaps": tuple(check for check in checks if not check["ok"]),
    }


def _pbc_advanced_runtime_evidence(contract: dict, *, minimum_capabilities: int = 1) -> dict:
    runtime = contract.get("advanced_runtime", {})
    smoke = runtime.get("smoke", {})
    operations = tuple(runtime.get("operations", ()))
    operation_set = set(operations)
    capabilities = tuple(runtime.get("capabilities", ()))
    smoke_checks = tuple(smoke.get("checks", ()))
    missing_operation_groups = tuple(
        group
        for group in PBC_ADVANCED_RUNTIME_REQUIRED_OPERATION_GROUPS
        if not any(operation in operation_set for operation in group)
    )
    checks = (
        {
            "id": "runtime_identity",
            "ok": runtime.get("ok") is True
            and runtime.get("pbc") == contract["pbc"]
            and runtime.get("implementation_directory") == f"src/pyAppGen/pbcs/{contract['pbc']}",
        },
        {
            "id": "advanced_capability_depth",
            "ok": len(capabilities) >= minimum_capabilities
            and len(set(capabilities)) == len(capabilities),
            "capability_count": len(capabilities),
            "minimum_capabilities": minimum_capabilities,
        },
        {
            "id": "advanced_operation_surface",
            "ok": len(operations) >= len(PBC_ADVANCED_RUNTIME_REQUIRED_OPERATION_GROUPS)
            and not missing_operation_groups,
            "operation_count": len(operations),
            "missing_operation_groups": missing_operation_groups,
        },
        {
            "id": "advanced_smoke_execution",
            "ok": smoke.get("ok") is True
            and bool(smoke_checks)
            and all(bool(check.get("ok")) for check in smoke_checks)
            and not tuple(smoke.get("blocking_gaps", ())),
            "smoke_check_count": len(smoke_checks),
        },
        {
            "id": "runtime_schema_service_release_linkage",
            "ok": {"build_schema_contract", "build_service_contract", "build_release_evidence"}
            <= operation_set,
        },
    )
    return {
        "format": "appgen.pbc-advanced-runtime-evidence.v1",
        "ok": all(check["ok"] for check in checks),
        "pbc": contract["pbc"],
        "required_operation_groups": PBC_ADVANCED_RUNTIME_REQUIRED_OPERATION_GROUPS,
        "operations": operations,
        "capabilities": capabilities,
        "checks": checks,
        "blocking_gaps": tuple(check for check in checks if not check["ok"]),
    }


def pbc_implementation_release_audit(selected_pbcs: tuple[str, ...] | list[str] | None = None) -> dict:
    """Verify every requested PBC has concrete generated implementation evidence."""
    contracts = pbc_implementation_contracts(selected_pbcs)
    required_artifacts = set(PBC_IMPLEMENTATION_REQUIRED_ARTIFACTS)
    checks = []
    for contract in contracts:
        if not contract["ok"]:
            checks.append({"id": f"{contract['pbc']}:known_pbc", "ok": False, "contract": contract})
            continue
        artifact_set = set(contract["package_metadata"]["artifacts"])
        owned_tables = {
            table["owned_table"]
            for table in contract["owned_schema"]["tables"]
        }
        relationship_tables = {
            relationship["target_table"]
            for relationship in contract["owned_schema"]["relationships"]
        }
        event_tables = {
            contract["events"]["outbox_table"],
            contract["events"]["inbox_table"],
            contract["events"]["dead_letter_table"],
        }
        specification = pbc_specification_contract(contract["pbc"])
        source_artifacts = pbc_source_artifact_contract(contract["pbc"])
        table_stakes = _pbc_table_stakes_evidence(contract)
        advanced_runtime = _pbc_advanced_runtime_evidence(contract)
        source_package = contract["source_package"]
        source_schema = source_package.get("schema_contract", {})
        source_service = source_package.get("service_contract", {})
        source_release = source_package.get("release_evidence") or source_package.get("release_evidence_contract") or {}
        schema_shared_boundary_ok = source_schema.get("shared_table_access") is False or not tuple(
            source_schema.get("dependencies", {}).get("shared_tables", ())
        )
        service_commands = tuple(source_service.get("command_methods", ()))
        release_checks = tuple(source_release.get("checks", ()))
        release_blocking_gaps = tuple(source_release.get("blocking_gaps", ()))
        checks.extend(
            (
                {
                    "id": f"{contract['pbc']}:required_artifacts",
                    "ok": required_artifacts <= artifact_set,
                },
                {
                    "id": f"{contract['pbc']}:source_package_directory",
                    "ok": source_package["ok"],
                },
                {
                    "id": f"{contract['pbc']}:source_artifacts_materialized",
                    "ok": source_artifacts["ok"],
                    "source_artifacts": source_artifacts,
                },
                {
                    "id": f"{contract['pbc']}:specification_completeness",
                    "ok": specification["ok"],
                    "specification": specification,
                },
                {
                    "id": f"{contract['pbc']}:table_stakes_evidence",
                    "ok": table_stakes["ok"],
                    "table_stakes": table_stakes,
                },
                {
                    "id": f"{contract['pbc']}:source_package_schema_service_release",
                    "ok": source_schema.get("ok") is True
                    and source_service.get("ok") is True
                    and source_release.get("ok") is True
                    and bool(source_schema.get("tables"))
                    and bool(source_schema.get("migrations"))
                    and bool(source_schema.get("models"))
                    and schema_shared_boundary_ok
                    and bool(service_commands)
                    and bool(release_checks)
                    and not release_blocking_gaps,
                },
                {
                    "id": f"{contract['pbc']}:owned_tables",
                    "ok": bool(owned_tables)
                    and all(table.startswith(f"{contract['pbc']}_") for table in owned_tables | event_tables)
                    and relationship_tables <= owned_tables,
                },
                {
                    "id": f"{contract['pbc']}:service_api_event_surface",
                    "ok": bool(contract["services"]["command_methods"])
                    and bool(contract["apis"])
                    and bool(contract["events"]["emitted"])
                    and contract["events"]["contract"] == "appgen_event_contract",
                },
                {
                    "id": f"{contract['pbc']}:handler_retry_dead_letter",
                    "ok": bool(contract["handlers"])
                    and all(handler["idempotency_key"].startswith(f"{contract['pbc']}:") for handler in contract["handlers"])
                    and contract["events"]["retry_policy"]["max_attempts"] >= 3
                    and contract["events"]["dead_letter_table"].startswith(f"{contract['pbc']}_"),
                },
                {
                    "id": f"{contract['pbc']}:domain_depth",
                    "ok": contract["domain_functionality"]["ok"]
                    and contract["domain_functionality"]["depth_level"] == PBC_DOMAIN_DEPTH_LEVEL
                    and set(PBC_DOMAIN_DEPTH_REQUIRED_DIMENSIONS)
                    <= set(contract["domain_functionality"]["dimensions"])
                    and not contract["domain_functionality"]["legacy_product_references"],
                },
                {
                    "id": f"{contract['pbc']}:advanced_domain_blueprint",
                    "ok": (
                        contract["pbc"] != "gl_core"
                        or (
                            contract["advanced_domain_blueprint"]["ok"]
                            and contract["advanced_runtime"]["ok"]
                            and set(PBC_ADVANCED_DOMAIN_REQUIRED_AREAS)
                            <= set(contract["advanced_domain_blueprint"]["areas"])
                            and set(GL_CORE_ADVANCED_CAPABILITY_KEYS)
                            <= {
                                item["capability"]
                                for item in contract["advanced_domain_blueprint"]["capabilities"]
                            }
                            and not contract["advanced_domain_blueprint"]["legacy_product_references"]
                        )
                    ),
                },
                {
                    "id": f"{contract['pbc']}:advanced_runtime",
                    "ok": (
                        contract["advanced_runtime"]
                        and advanced_runtime["ok"]
                    ),
                    "advanced_runtime": advanced_runtime,
                },
                {
                    "id": f"{contract['pbc']}:package_metadata",
                    "ok": contract["directory"] == f"pbcs/{contract['pbc']}"
                    and contract["package_metadata"]["entrypoint"] == "register_pbc"
                    and contract["release_evidence"]["cross_pbc_boundary"] == "no_shared_tables",
                },
            )
        )
    ok = bool(contracts) and all(check["ok"] for check in checks)
    return {
        "format": "appgen.pbc-implementation-release-audit.v1",
        "ok": ok,
        "pbc_count": len(contracts),
        "required_artifacts": PBC_IMPLEMENTATION_REQUIRED_ARTIFACTS,
        "required_domain_dimensions": PBC_DOMAIN_DEPTH_REQUIRED_DIMENSIONS,
        "advanced_domain_required_areas": PBC_ADVANCED_DOMAIN_REQUIRED_AREAS,
        "depth_level": PBC_DOMAIN_DEPTH_LEVEL,
        "contracts": contracts,
        "checks": tuple(checks),
        "blocking_gaps": tuple(check for check in checks if not check["ok"]),
    }


def pbc_implemented_capability_audit(selected_pbcs: tuple[str, ...] | list[str] | None = None) -> dict:
    """Verify implemented PBCs expose standard table-stakes and advanced runtime evidence."""
    selected = tuple(dict.fromkeys(selected_pbcs or IMPLEMENTED_PBC_KEYS))
    minimum_standard_features = 18
    minimum_advanced_capabilities = {
        "gl_core": len(GL_CORE_ADVANCED_CAPABILITY_KEYS),
        "ap_automation": len(AP_AUTOMATION_ADVANCED_CAPABILITY_KEYS),
        "ar_credit": len(AR_CREDIT_ADVANCED_CAPABILITY_KEYS),
        "treasury_cash": len(TREASURY_CASH_ADVANCED_CAPABILITY_KEYS),
        "asset_lifecycle": len(ASSET_LIFECYCLE_ADVANCED_CAPABILITY_KEYS),
        "tax_localization": len(TAX_LOCALIZATION_ADVANCED_CAPABILITY_KEYS),
        "inventory_positioning": len(INVENTORY_POSITIONING_ADVANCED_CAPABILITY_KEYS),
        "wms_core": len(WMS_CORE_ADVANCED_CAPABILITY_KEYS),
        "procurement_sourcing": len(PROCUREMENT_SOURCING_ADVANCED_CAPABILITY_KEYS),
        "transportation_management": len(TRANSPORTATION_MANAGEMENT_ADVANCED_CAPABILITY_KEYS),
        "dom": len(DOM_ADVANCED_CAPABILITY_KEYS),
        "personnel_identity": len(PERSONNEL_IDENTITY_ADVANCED_CAPABILITY_KEYS),
        "time_labor": len(TIME_LABOR_ADVANCED_CAPABILITY_KEYS),
        "payroll_engine": len(PAYROLL_ENGINE_ADVANCED_CAPABILITY_KEYS),
        "talent_onboarding": len(TALENT_ONBOARDING_ADVANCED_CAPABILITY_KEYS),
        "mrp_engine": len(MRP_ENGINE_ADVANCED_CAPABILITY_KEYS),
        "production_control": len(PRODUCTION_CONTROL_ADVANCED_CAPABILITY_KEYS),
        "quality_assurance": len(QUALITY_ASSURANCE_ADVANCED_CAPABILITY_KEYS),
        "eam": len(EAM_ADVANCED_CAPABILITY_KEYS),
        "product_catalog_pim": len(PRODUCT_CATALOG_PIM_ADVANCED_CAPABILITY_KEYS),
        "customer_360": len(CUSTOMER_360_ADVANCED_CAPABILITY_KEYS),
        "enterprise_pim": len(ENTERPRISE_PIM_RUNTIME_CAPABILITY_KEYS),
        "global_inventory_visibility": len(GLOBAL_INVENTORY_VISIBILITY_RUNTIME_CAPABILITY_KEYS),
        "order_routing_optimization": len(ORDER_ROUTING_OPTIMIZATION_RUNTIME_CAPABILITY_KEYS),
        "checkout_processing": len(CHECKOUT_PROCESSING_RUNTIME_CAPABILITY_KEYS),
        "payment_orchestration": len(PAYMENT_ORCHESTRATION_RUNTIME_CAPABILITY_KEYS),
        "subscription_billing": len(SUBSCRIPTION_BILLING_RUNTIME_CAPABILITY_KEYS),
        "returns_reverse_logistics": len(RETURNS_REVERSE_LOGISTICS_RUNTIME_CAPABILITY_KEYS),
        "cross_border_trade": len(CROSS_BORDER_TRADE_RUNTIME_CAPABILITY_KEYS),
        "dam_core": len(DAM_CORE_RUNTIME_CAPABILITY_KEYS),
        "price_promotion_engine": len(PRICE_PROMOTION_ENGINE_RUNTIME_CAPABILITY_KEYS),
        "lead_opportunity": len(LEAD_OPPORTUNITY_RUNTIME_CAPABILITY_KEYS),
        "service_ticketing": len(SERVICE_TICKETING_RUNTIME_CAPABILITY_KEYS),
        "notifications": len(NOTIFICATIONS_RUNTIME_CAPABILITY_KEYS),
        "cdp_segmentation": len(CDP_SEGMENTATION_RUNTIME_CAPABILITY_KEYS),
        "loyalty_rewards": len(LOYALTY_REWARDS_RUNTIME_CAPABILITY_KEYS),
        "streaming_analytics": len(STREAMING_ANALYTICS_RUNTIME_CAPABILITY_KEYS),
        "enterprise_search_vector": len(ENTERPRISE_SEARCH_VECTOR_RUNTIME_CAPABILITY_KEYS),
        "predictive_demand": len(PREDICTIVE_DEMAND_RUNTIME_CAPABILITY_KEYS),
        "fraud_anomaly_detection": len(FRAUD_ANOMALY_DETECTION_RUNTIME_CAPABILITY_KEYS),
        "federated_iam": len(FEDERATED_IAM_ADVANCED_CAPABILITY_KEYS),
        "api_gateway_mesh": len(API_GATEWAY_MESH_ADVANCED_CAPABILITY_KEYS),
        "schema_registry": len(SCHEMA_REGISTRY_ADVANCED_CAPABILITY_KEYS),
        "workflow_orchestration": len(WORKFLOW_ORCHESTRATION_ADVANCED_CAPABILITY_KEYS),
        "audit_ledger": len(AUDIT_LEDGER_ADVANCED_CAPABILITY_KEYS),
        "composition_engine": len(COMPOSITION_ENGINE_ADVANCED_CAPABILITY_KEYS),
    }
    checks = []
    contracts = pbc_implementation_contracts(selected)
    for contract in contracts:
        key = contract["pbc"]
        runtime = contract.get("advanced_runtime", {})
        source = contract.get("source_package", {})
        table_stakes = _pbc_table_stakes_evidence(contract)
        package_local_assurance = pbc_package_local_assurance_contract(key)
        standard_features = tuple(runtime.get("standard_features") or source.get("standard_features") or ())
        advanced_capabilities = tuple(runtime.get("capabilities", ()))
        advanced_runtime = _pbc_advanced_runtime_evidence(
            contract,
            minimum_capabilities=minimum_advanced_capabilities.get(key, 1),
        )
        checks.extend(
            (
                {
                    "id": f"{key}:source_package_owned",
                    "ok": source.get("ok") is True
                    and source.get("implementation_directory") == f"src/pyAppGen/pbcs/{key}",
                },
                {
                    "id": f"{key}:standard_table_stakes",
                    "ok": len(standard_features) >= minimum_standard_features
                    and len(set(standard_features)) == len(standard_features),
                    "standard_feature_count": len(standard_features),
                    "standard_features": standard_features,
                },
                {
                    "id": f"{key}:advanced_runtime_complete",
                    "ok": advanced_runtime["ok"],
                    "advanced_capability_count": len(advanced_capabilities),
                    "advanced_runtime": advanced_runtime,
                },
                {
                    "id": f"{key}:table_stakes_evidence",
                    "ok": table_stakes["ok"],
                    "required_evidence": PBC_TABLE_STAKES_REQUIRED_EVIDENCE,
                    "checks": table_stakes["checks"],
                },
                {
                    "id": f"{key}:package_local_assurance",
                    "ok": package_local_assurance["ok"],
                    "package_local_assurance": package_local_assurance,
                },
                {
                    "id": f"{key}:release_audit_ready",
                    "ok": pbc_implementation_release_audit((key,))["ok"],
                },
            )
        )
    return {
        "format": "appgen.implemented-pbc-capability-audit.v1",
        "ok": bool(contracts) and all(check["ok"] for check in checks),
        "implemented_pbcs": selected,
        "minimum_standard_features": minimum_standard_features,
        "required_table_stakes_evidence": PBC_TABLE_STAKES_REQUIRED_EVIDENCE,
        "contracts": contracts,
        "checks": tuple(checks),
        "blocking_gaps": tuple(check for check in checks if not check["ok"]),
    }


def example_pbc_manifest() -> dict:
    """Return a minimal publishable PBC manifest for documentation and tests."""
    return {
        "pbc": "warranty_claims",
        "label": "Warranty Claims",
        "mesh": "relationship",
        "description": "Manage warranty intake, eligibility, adjudication, and claim resolution.",
        "datastore_backend": "postgresql",
        "stream_processor": "faust_streaming",
        "tables": ("warranty_claim", "claim_line", "eligibility_check"),
        "apis": ("POST /warranty-claims", "POST /eligibility-checks", "GET /claim-status"),
        "emits": ("WarrantyClaimOpened", "WarrantyClaimApproved"),
        "consumes": ("ProductPublished", "CustomerUpdated", "OrderShipped"),
        "template": None,
        "ui_fragments": ("WarrantyClaimsWorkbench", "WarrantyClaimDetail"),
        "permissions": ("warranty_claim.read", "warranty_claim.create", "warranty_claim.approve"),
        "configuration": ("WARRANTY_DEFAULT_REGION",),
        "migrations": ("migrations/001_warranty_claims.sql",),
        "seed_data": ("seed/warranty_reasons.json",),
        "tests": ("tests/test_warranty_claims_contract.py",),
        "docs": ("docs/warranty-claims.md",),
    }


def example_stream_exception_manifest() -> dict:
    """Return a valid PBC manifest that uses a stream-processing exception profile."""
    return {
        **example_pbc_manifest(),
        "pbc": "machine_telemetry",
        "label": "Machine Telemetry",
        "mesh": "opsmfg",
        "description": "Ingest and aggregate equipment telemetry windows.",
        "stream_processor": "quix_streams",
        "tables": ("telemetry_sample", "telemetry_window"),
        "apis": ("POST /telemetry", "GET /telemetry-windows"),
        "emits": ("TelemetryWindowCalculated",),
        "consumes": ("MachineSignalReceived",),
        "stream_exception_evidence": {
            "workload_name": "equipment telemetry windows",
            "throughput_or_latency_reason": "high-volume time-series ingestion with windowed operational metrics",
            "state_shape": "per-machine rolling windows persisted by watermark",
            "operational_owner": "opsmfg telemetry platform team",
        },
        "tests": ("tests/test_machine_telemetry_contract.py",),
        "docs": ("docs/machine-telemetry.md",),
    }


def application_composition_topology() -> dict:
    """Return the ACP runtime topology required for composable apps."""
    layers = (
        {
            "layer": "composed_digital_experience",
            "purpose": "Assemble UI fragments and channel experiences from selected PBCs.",
            "required_pbcs": ("composition_engine",),
        },
        {
            "layer": "composition_layer",
            "purpose": "Coordinate low-code composition, BFF endpoints, GraphQL mesh, and orchestration.",
            "required_pbcs": ("composition_engine", "workflow_orchestration", "federated_iam"),
        },
        {
            "layer": "event_backbone_gateway_fabric",
            "purpose": "Provide routing, service discovery, event contracts, schema compatibility, and audit.",
            "required_pbcs": ("api_gateway_mesh", "schema_registry", "audit_ledger"),
        },
        {
            "layer": "domain_meshes",
            "purpose": "Host independently deployable business capabilities across enterprise domains.",
            "required_meshes": ("finops", "scl", "hcm", "opsmfg", "cx", "commerce", "content", "relationship", "intelligence"),
        },
    )
    return {
        "format": "appgen.application-composition-topology.v1",
        "ok": all(
            set(layer.get("required_pbcs", ())) <= set(PBC_CATALOG)
            and set(layer.get("required_meshes", ())) <= set(PBC_MESHES)
            for layer in layers
        ),
        "layers": layers,
        "runtime_fabric": (
            "low_code_composition",
            "bff_graphql_mesh",
            "event_backbone",
            "python_stream_processor_abstraction",
            "schema_registry",
            "gateway_service_mesh",
            "domain_pbc_meshes",
        ),
        "stream_processors": acp_stream_processor_catalog(),
        "stream_processor_default": ACP_DEFAULT_STREAM_PROCESSOR,
        "stream_processor_rules": ACP_STREAM_PROCESSOR_DECISION_RULES,
    }


def acp_capability_coverage() -> dict:
    """Return coverage evidence for the ACP component catalog."""
    required = {
        "platform": {
            "federated_iam",
            "api_gateway_mesh",
            "schema_registry",
            "workflow_orchestration",
            "audit_ledger",
            "composition_engine",
        },
        "commerce": {
            "global_inventory_visibility",
            "order_routing_optimization",
            "checkout_processing",
            "payment_orchestration",
            "subscription_billing",
            "returns_reverse_logistics",
            "cross_border_trade",
        },
        "content": {"enterprise_pim", "dam_core", "price_promotion_engine"},
        "relationship": {
            "lead_opportunity",
            "service_ticketing",
            "notifications",
            "cdp_segmentation",
            "loyalty_rewards",
        },
        "intelligence": {
            "streaming_analytics",
            "enterprise_search_vector",
            "predictive_demand",
            "fraud_anomaly_detection",
        },
    }
    coverage = tuple(
        {
            "mesh": mesh,
            "required": tuple(sorted(keys)),
            "missing": tuple(sorted(key for key in keys if key not in PBC_CATALOG)),
            "ok": all(key in PBC_CATALOG for key in keys),
        }
        for mesh, keys in required.items()
    )
    return {
        "format": "appgen.acp-capability-coverage.v1",
        "ok": all(item["ok"] for item in coverage),
        "coverage": coverage,
    }


def pbc_selection_from_prompt(prompt: str) -> dict:
    """Resolve a natural-language app request to a composable PBC selection."""
    text = prompt.lower()
    explicit = [
        key
        for key, pbc in PBC_CATALOG.items()
        if key.replace("_", " ") in text
        or pbc["label"].lower() in text
        or any(word in text for word in _selection_terms(key, pbc))
    ]
    if any(term in text for term in ("application composition platform", "acp", "apc")):
        explicit.extend(PBC_STARTER_STACKS["application_composition_platform"])
    for stack, pbcs in PBC_STARTER_STACKS.items():
        if stack.replace("_", " ") in text:
            explicit.extend(pbcs)
    if not explicit and any(term in text for term in ("erp", "enterprise", "back office")):
        explicit.extend(PBC_STARTER_STACKS["enterprise_core"])
    selection = tuple(dict.fromkeys(explicit))
    return {
        "format": "appgen.pbc-natural-language-selection.v1",
        "prompt": prompt,
        "pbcs": selection,
        "matched": bool(selection),
        "composition": pbc_composition_plan(selection, app_name=_app_name_from_prompt(prompt)) if selection else None,
    }


def pbc_composition_plan(
    selected_pbcs: tuple[str, ...] | list[str],
    *,
    app_name: str = "ComposableEnterprise",
    targets: tuple[str, ...] = ("web", "pwa", "mobile", "desktop"),
) -> dict:
    """Return a bounded-context composition plan for selected PBCs.

    Three buckets, and the distinction between them is the point. A dependency
    is an event one selected PBC consumes and a *different* selected PBC emits,
    so it resolves inside the composition. An external event contract is one no
    selected PBC emits, so it is an integration obligation the app must satisfy
    from outside. An internal event loop is one a PBC consumes and emits itself:
    the outbox-to-own-inbox projection pattern, which is neither.

    The provider list is a tuple rather than a single key. `emitted` was a dict
    built by comprehension, so an event two selected PBCs both emit silently
    kept whichever came last in selection order and the plan asserted one
    provider as fact. Thirteen events are emitted by more than one package in
    the catalog and 46 consumer rows depend on one of them, so the choice was
    arbitrary wherever it was made.
    """
    selected = tuple(dict.fromkeys(selected_pbcs))
    missing = tuple(key for key in selected if key not in PBC_CATALOG)
    services = tuple(_service_contract(key) for key in selected if key in PBC_CATALOG)
    emitted: dict[str, list[str]] = {}
    for service in services:
        for event in service["emits"]:
            providers = emitted.setdefault(event, [])
            if service["pbc"] not in providers:
                providers.append(service["pbc"])
    dependencies = tuple(
        {
            "from": service["pbc"],
            "event": event,
            "provider": others[0],
            "providers": tuple(others),
            "resolved": True,
        }
        for service in services
        for event in service["consumes"]
        if (others := _external_providers(emitted, event, service["pbc"]))
    )
    unresolved_external_events = tuple(
        {
            "pbc": service["pbc"],
            "event": event,
            "policy": "external-event-contract",
        }
        for service in services
        for event in service["consumes"]
        if event not in emitted
    )
    internal_event_loops = tuple(
        {
            "pbc": service["pbc"],
            "event": event,
            "policy": "outbox-to-own-inbox-projection",
        }
        for service in services
        for event in service["consumes"]
        if emitted.get(event) == [service["pbc"]]
    )
    datastores = tuple(service["datastore"] for service in services)
    shared_datastores = tuple(
        datastore for datastore in datastores if datastores.count(datastore) > 1
    )
    shared_tables = _composition_shared_tables(services)
    return {
        "format": "appgen.pbc-composition-plan.v1",
        "ok": not missing and not shared_datastores and not shared_tables and bool(services),
        "app_name": app_name,
        "targets": targets,
        "pbcs": selected,
        "services": services,
        "dependencies": dependencies,
        "external_event_contracts": unresolved_external_events,
        "internal_event_loops": internal_event_loops,
        "missing_pbcs": missing,
        "shared_datastores": tuple(dict.fromkeys(shared_datastores)),
        "shared_tables": shared_tables,
        "integration_style": "event-first-with-api-command-surface",
        "deployment_units": tuple(f"services/{service['pbc']}" for service in services),
        "stop_condition": "do-not-compose-pbcs-unless-each-selected-capability-has-an-owned-datastore",
    }


def _external_providers(emitted: dict[str, list[str]], event: str, consumer: str) -> list[str]:
    """Return the selected PBCs that emit `event` other than the consumer.

    A PBC that consumes an event it also emits is projecting its own outbox into
    its own inbox, which is the platform's normal pattern and not a dependency
    on anyone. Excluding the consumer is what separates a real interlock from
    that loop: `ar_credit` emits `DeliveryConfirmed` when it records a delivery
    and subscribes to it to build its delivery projection, and the plan reported
    `ar_credit` as its own provider.
    """
    return [provider for provider in emitted.get(event, ()) if provider != consumer]


def _composition_shared_tables(services: tuple[dict, ...]) -> tuple[dict, ...]:
    """Return physical tables claimed by more than one selected PBC.

    Generated apps name every owned table ``{pbc}_{logical}``, so two PBCs
    collide only if one PBC's key prefixes another's table name. Keys are
    unique today and no key prefixes another, so this is empty for every
    current composition; it is checked rather than assumed because a future
    key that does prefix another would silently merge two owned datastores.
    """
    owners: dict[str, list[str]] = {}
    for service in services:
        for table in service["tables"]:
            owners.setdefault(f"{service['pbc']}_{table}", []).append(service["pbc"])
    return tuple(
        {"table": table, "owners": tuple(sorted(set(table_owners)))}
        for table, table_owners in sorted(owners.items())
        if len(set(table_owners)) > 1
    )


def pbc_composition_dsl(
    selected_pbcs: tuple[str, ...] | list[str],
    *,
    app_name: str = "ComposableEnterprise",
    targets: tuple[str, ...] = ("web", "pwa", "mobile", "desktop"),
) -> str:
    """Render a compact AppGen DSL starter for a selected PBC composition."""
    plan = pbc_composition_plan(tuple(selected_pbcs), app_name=app_name, targets=targets)
    if not plan["ok"]:
        raise ValueError(f"Invalid PBC composition: {plan['missing_pbcs'] or plan['shared_datastores']}")
    lines = [f"app {app_name} {{ targets: {', '.join(targets)} }}"]
    lines.extend(
        (
            "",
            "llm AppGenXLocalModel {",
            "  provider: local",
            "  mode: governed",
            "  model: appgen-x-composed-assistant",
            "}",
            "",
            f"agent {app_name}Assistant {{",
            "  provider: AppGenXLocalModel",
            '  goal: "Guide users through selected PBC tasks, documents, and governed datastore changes"',
            "  tools: " + ", ".join(f"{service['pbc']}_skills" for service in plan["services"]),
            "  memory: tenant_session",
            "  max_steps: 12",
            "}",
        )
    )
    for service in plan["services"]:
        for table_name, body in _composition_table_bodies(service["pbc"]):
            lines.extend(("", f"table {table_name} {{", *body, "}"))
        lines.extend(_composition_workbench_view(service))
    return "\n".join(lines).rstrip() + "\n"


def _composition_table_bodies(key: str) -> tuple[tuple[str, tuple[str, ...]], ...]:
    """Return every owned table of a PBC as DSL lines, from its real columns.

    The composition DSL declared three tables per PBC with the same
    `code`/`status`/`updated_at` body, so a three-PBC app declared eighteen
    tables and described none of them: `gl_core_journal_entry` had no journal,
    no debit, and no credit.

    The source is the package's migration rather than the manifest, because the
    migration is the physical inventory: `gl_core`'s manifest names 24 tables
    and its migration declares 31, and the seven the manifest omits include the
    outbox the workbench view binds to. A table the app does not declare cannot
    be rendered, so the union is the migration's set.
    """
    tables = pbc_schema.owned_schema(key)
    if not tables:
        return ()
    return tuple(
        (table_name, tuple(_dsl_field_lines(table["fields"])))
        for table_name, table in tables.items()
        if table["fields"]
    )


def _composition_workbench_view(service: dict) -> tuple[str, ...]:
    """Return the DSL for a PBC's workbench view, bound to its real outbox.

    The view was written against four columns (`event_type`, `status`,
    `payload`, `published_at`) that exist together in no package. `gl_core` and
    `ar_credit` have no `status` or `published_at` on the outbox at all, so the
    view referenced columns the table did not have and the DSL could not be
    parsed, let alone generated. The columns come from the table's own
    declaration, and the first four that are worth showing are placed.
    """
    key = service["pbc"]
    outbox = f"{key}_appgen_outbox_event"
    fields = (pbc_schema.owned_schema(key).get(outbox) or {}).get("fields") or ()
    if not fields:
        return ()
    shown = _workbench_view_fields(fields)
    if not shown:
        return ()
    return (
        "",
        f"view {service['class_name']}Workbench for {outbox} {{",
        "  Main: " + ", ".join(field["name"] for field, _x, _y, _w in shown),
        *(
            f"  @ {field['name']} {_view_control(field)} {x} {y} {w} 1"
            for field, x, y, w in shown
        ),
        "}",
    )


def _workbench_view_fields(fields: tuple[dict, ...]) -> tuple[tuple[dict, int, int, int], ...]:
    """Pick the outbox columns a workbench shows, with their grid placement.

    Bookkeeping columns are skipped: a primary key and the tenant are the
    record's identity, not something a workbench screen edits. The event type,
    the payload, and the outcome of the attempt are what the screen is for, and
    they are found by name so a package that spells them differently still gets
    a view over the columns it actually has.
    """
    preferred = ("event_type", "status", "payload", "attempts", "reason", "published_at", "created_at")
    hidden = {"id", "tenant"}
    picked = [field for name in preferred for field in fields if field["name"] == name and name not in hidden]
    if not picked:
        picked = [field for field in fields if field["name"] not in hidden][:4]
    widths = (6, 3, 12, 3, 6, 6, 6)
    placed = []
    x = y = 0
    for field, width in zip(picked, widths):
        if x + width > 12:
            x, y = 0, y + 1
        placed.append((field, x, y, width))
        x += width
    return tuple(placed)


def _view_control(field: dict) -> str:
    """Return the form control a column's type is edited with."""
    return {
        "text": "TextBox",
        "string": "TextBox",
        "integer": "NumberInput",
        "int": "NumberInput",
        "float": "NumberInput",
        "decimal": "NumberInput",
        "boolean": "Checkbox",
        "bool": "Checkbox",
        "date": "DatePicker",
        "datetime": "DateTimePicker",
        "json": "TextArea",
    }.get(field["type"], "TextBox")


def _dsl_field_lines(fields: tuple[dict, ...]) -> list[str]:
    """Render a contract's fields as DSL column declarations.

    The migration types are the generator's own vocabulary already, so the
    only work is the keyword suffix: `pk` for the primary key, `required` for
    a NOT NULL column, and `search` for the text columns a list screen filters
    on. The index's unique columns are left to the migration, since the DSL
    declares indexes separately and a wrong `unique` here would reject a
    package that permits duplicates.

    Only the first primary key is declared. Some packages write
    `PRIMARY KEY` on several columns of one table (`gl_core_journal_entry`
    marks `id`, `journal_id`, and `period_id`), which is invalid SQL and would
    be a second `pk` the grammar rejects; the extras become `required`, which
    is what they are in practice.
    """
    lines = []
    declared_pk = False
    for field in fields:
        parts = [f"{field['name']}:", field["type"]]
        if field.get("primary_key") and not declared_pk:
            parts.append("pk")
            declared_pk = True
        elif field.get("required"):
            parts.append("required")
        if field["type"] == "text" and not field.get("primary_key"):
            parts.append("search")
        lines.append("  " + " ".join(parts))
    return lines


def pbc_release_audit() -> dict:
    """Return package-level proof for composable PBC app generation."""
    sample = PBC_STARTER_STACKS["enterprise_core"]
    composition = pbc_composition_plan(sample, app_name="EnterpriseCore")
    acp_composition = pbc_composition_plan(PBC_STARTER_STACKS["application_composition_platform"], app_name="AppCompositionPlatform")
    topology = application_composition_topology()
    acp_coverage = acp_capability_coverage()
    stream_policy = acp_stream_processing_policy()
    invalid_exception = validate_pbc_manifest(
        {
            **example_pbc_manifest(),
            "pbc": "machine_telemetry_missing_evidence",
            "stream_processor": "quix_streams",
        }
    )
    valid_exception = validate_pbc_manifest(example_stream_exception_manifest())
    ordinary_manifest = dict(example_pbc_manifest())
    ordinary_manifest.pop("stream_processor", None)
    ordinary_eventing_lint = lint_pbc_eventing_choice(ordinary_manifest)
    branching_eventing_lint = lint_pbc_eventing_choice(
        {
            **example_pbc_manifest(),
            "stream_processor": ACP_DEFAULT_STREAM_PROCESSOR,
        },
        generated_imports=("faust_streaming",),
    )
    package_loading = pbc_package_loading_smoke_audit()
    lifecycle_docs = pbc_lifecycle_documentation_audit()
    specification_audit = pbc_specification_release_audit()
    source_artifact_audit = pbc_source_artifact_release_audit()
    source_test_coverage = pbc_source_runtime_test_coverage_audit()
    package_local_assurance = pbc_package_local_assurance_audit()
    agent_capability_audit = pbc_agent_capability_release_audit()
    implementation_audit = pbc_implementation_release_audit()
    nl_selection = pbc_selection_from_prompt(
        "Build an enterprise ERP back office with GL, AP, AR, inventory, people, and order management"
    )
    starter_smoke = pbc_generation_smoke_audit(sample)
    smoke = pbc_generation_smoke_audit(IMPLEMENTED_PBC_KEYS)
    required_meshes = {"finops", "scl", "hcm", "opsmfg", "cx", "platform", "commerce", "content", "relationship", "intelligence"}
    gates = (
        {
            "id": "catalog_depth",
            "ok": len(PBC_CATALOG) >= 46 and required_meshes <= {item["mesh"] for item in PBC_CATALOG.values()},
            "count": len(PBC_CATALOG),
            "meshes": tuple(sorted({item["mesh"] for item in PBC_CATALOG.values()})),
        },
        {
            "id": "bounded_context_contracts",
            "ok": all(
                item["datastore"]
                and item["datastore_backend"] in PBC_ALLOWED_DATASTORE_BACKENDS
                and item["apis"]
                and item["emits"]
                and item["tables"]
                and item["package_directory"] == f"pbcs/{item['pbc']}"
                for item in pbc_catalog()
            ),
        },
        {
            "id": "pbc_implementation_contracts",
            "ok": specification_audit["ok"]
            and source_artifact_audit["ok"]
            and source_test_coverage["ok"]
            and package_local_assurance["ok"]
            and agent_capability_audit["ok"]
            and implementation_audit["ok"]
            and implementation_audit["pbc_count"] == len(PBC_CATALOG),
            "specification_checks": tuple(
                {
                    "pbc": contract["pbc"],
                    "ok": contract["ok"],
                    "word_count": contract["word_count"],
                    "missing_concepts": contract["missing_concepts"],
                }
                for contract in specification_audit["contracts"]
            ),
            "source_artifacts": source_artifact_audit,
            "source_test_coverage": source_test_coverage,
            "package_local_assurance": package_local_assurance,
            "agent_capability": agent_capability_audit,
            "checks": implementation_audit["checks"],
        },
        {
            "id": "starter_stacks",
            "ok": {"finance_mesh", "distribution_mesh", "people_mesh", "manufacturing_mesh", "enterprise_core", "application_composition_platform"}
            <= {item["stack"] for item in pbc_starter_stacks()},
        },
        {
            "id": "acp_platform_fabric",
            "ok": topology["ok"]
            and acp_coverage["ok"]
            and acp_composition["ok"]
            and len(acp_composition["services"]) == 6,
            "topology": topology["format"],
            "coverage": acp_coverage["format"],
        },
        {
            "id": "self_registering_pbc_spec",
            "ok": register_pbc_manifest(example_pbc_manifest())["ok"]
            and pbc_package_contract("warranty_claims_pbc", example_pbc_manifest())["usable"],
            "schema": pbc_manifest_schema()["format"],
        },
        {
            "id": "pbc_package_loader",
            "ok": package_loading["ok"] and lifecycle_docs["ok"],
            "checks": package_loading["checks"],
            "lifecycle_docs": lifecycle_docs,
        },
        {
            "id": "open_source_datastore_backends",
            "ok": all(item["datastore_backend"] in PBC_ALLOWED_DATASTORE_BACKENDS for item in pbc_catalog()),
            "allowed": PBC_ALLOWED_DATASTORE_BACKENDS,
        },
        {
            "id": "stream_processor_abstraction",
            "ok": {
                "bytewax",
                "quix_streams",
                "faust_streaming",
            }
            == {item["processor"] for item in acp_stream_processor_catalog()}
            and ACP_DEFAULT_STREAM_PROCESSOR == "faust_streaming"
            and select_acp_stream_processor("async workflow saga")["selected"] == "faust_streaming"
            and select_acp_stream_processor("high throughput telemetry")["selected"] == "quix_streams"
            and select_acp_stream_processor("parallel transformation pipeline")["selected"] == "bytewax",
            "processors": tuple(item["processor"] for item in acp_stream_processor_catalog()),
            "default": ACP_DEFAULT_STREAM_PROCESSOR,
            "decision_rules": ACP_STREAM_PROCESSOR_DECISION_RULES,
        },
        {
            "id": "opinionated_stream_processing_policy",
            "ok": stream_policy["default"] == "faust_streaming"
            and stream_policy["allowed_processors"] == ("faust_streaming", "quix_streams", "bytewax")
            and stream_policy["decision_card"]["choice_contract"] == "one_default_two_audited_exceptions"
            and stream_policy["developer_decision_brief"]["developer_visible_options"] == ("appgen_event_contract",)
            and "stream_engine_picker" in stream_policy["developer_decision_brief"]["studio_controls_to_hide"]
            and stream_policy["opinionated_stack"]["default_event_adapter"] == "appgen_outbox_inbox_faust_streaming"
            and stream_policy["decision_ladder"][0] == "omit_stream_processor_for_ordinary_apps"
            and all(item["use"] in stream_policy["allowed_processors"] for item in stream_policy["decision_tree"])
            and "adding a fourth processor without a platform architecture decision" in stream_policy["prohibited"]
            and not invalid_exception["ok"]
            and valid_exception["ok"]
            and valid_exception["stream_processor_decision"] == "exception",
            "default": stream_policy["default"],
            "allowed_processors": stream_policy["allowed_processors"],
            "decision_tree": stream_policy["decision_tree"],
            "invalid_exception": invalid_exception,
            "valid_exception": valid_exception,
        },
        {
            "id": "eventing_choice_linter",
            "ok": ordinary_eventing_lint["ok"]
            and not branching_eventing_lint["ok"]
            and branching_eventing_lint["quick_fixes"][0]["id"] == "remove_stream_processor"
            and branching_eventing_lint["diagnostics"][0]["rule"] == "ordinary_pbc_manifest_omits_stream_processor",
            "ordinary": ordinary_eventing_lint,
            "branching": branching_eventing_lint,
        },
        {
            "id": "composition_plan",
            "ok": composition["ok"]
            and not composition["shared_datastores"]
            and not composition["shared_tables"]
            and len(composition["services"]) == len(sample),
        },
        {
            "id": "natural_language_selection",
            "ok": nl_selection["matched"]
            and {"gl_core", "ap_automation", "ar_credit", "inventory_positioning", "personnel_identity", "dom"}
            <= set(nl_selection["pbcs"]),
        },
        {
            "id": "generation_smoke",
            "ok": starter_smoke["ok"]
            and smoke["ok"]
            and smoke["selected_pbcs"] == IMPLEMENTED_PBC_KEYS,
            "starter_checks": starter_smoke["checks"],
            "selected_pbcs": smoke["selected_pbcs"],
            "checks": smoke["checks"],
        },
    )
    ok = all(gate["ok"] for gate in gates)
    return {
        "format": "appgen.pbc-release-audit.v1",
        "scope": "package",
        "ok": ok,
        "decision": "approved" if ok else "blocked",
        "meshes": pbc_mesh_catalog(),
        "catalog": pbc_catalog(),
        "starter_stacks": pbc_starter_stacks(),
        "topology": topology,
        "acp_coverage": acp_coverage,
        "acp_composition": acp_composition,
        "stream_processors": acp_stream_processor_catalog(),
        "manifest_schema": pbc_manifest_schema(),
        "example_registration": register_pbc_manifest(example_pbc_manifest()),
        "package_loading": package_loading,
        "lifecycle_documentation": lifecycle_docs,
        "specification_audit": specification_audit,
        "source_artifacts": source_artifact_audit,
        "source_test_coverage": source_test_coverage,
        "package_local_assurance": package_local_assurance,
        "agent_capability": agent_capability_audit,
        "implementation_audit": implementation_audit,
        "sample_composition": composition,
        "nl_selection": nl_selection,
        "starter_generation_smoke": starter_smoke,
        "generation_smoke": smoke,
        "gates": gates,
        "blocking_gaps": tuple(gate for gate in gates if not gate["ok"]),
    }


def pbc_generation_smoke_audit(selected_pbcs: tuple[str, ...] | list[str] | None = None) -> dict:
    """Generate and compile a small app from a PBC composition DSL."""
    from .dsl import schema_from_dsl
    from .gen import generate_app_from_schema

    selected = tuple(selected_pbcs or PBC_STARTER_STACKS["enterprise_core"])
    dsl = pbc_composition_dsl(selected, app_name="PbcSmoke")
    schema = schema_from_dsl(dsl, source_name="pbc-composition.appgen")
    with tempfile.TemporaryDirectory(prefix="appgen-pbc-composition-") as raw_workdir:
        project_dir = Path(raw_workdir) / "pbc-smoke"
        output_dir = project_dir / "app"
        generate_app_from_schema(schema, output_dir)
        artifacts = ("app/models.py", "app/views.py", "app/pbc_runtime.py", "app/appgen.json", "docs/schema.md")
        missing = tuple(path for path in artifacts if not (project_dir / path).exists())
        pbc_artifact_missing = []
        for key in selected:
            for artifact in PBC_IMPLEMENTATION_REQUIRED_ARTIFACTS:
                path = project_dir / "app" / "pbcs" / key / artifact
                if not path.exists():
                    pbc_artifact_missing.append(str(Path("app") / "pbcs" / key / artifact))
        pbc_directories_exist = all((project_dir / "app" / "pbcs" / key).is_dir() for key in selected)
        compiled = []
        compile_failures = []
        compile_targets = [Path("app/models.py"), Path("app/views.py"), Path("app/pbc_runtime.py")]
        for key in selected:
            pbc_dir = project_dir / "app" / "pbcs" / key
            compile_targets.extend(
                path.relative_to(project_dir)
                for path in sorted(pbc_dir.rglob("*.py"))
                if path.exists()
            )
        for relative_path in compile_targets:
            relative = str(relative_path)
            path = project_dir / relative
            try:
                py_compile.compile(str(path), doraise=True)
            except py_compile.PyCompileError as exc:
                compile_failures.append({"path": relative, "error": str(exc)})
            else:
                compiled.append(relative)
        runtime_smoke = {"ok": False, "error": "app/pbc_runtime.py was not loaded"}
        runtime_manifest = {}
        runtime_workbench = {}
        runtime_registration = {}
        generated_contract_test_results = []
        runtime_path = output_dir / "pbc_runtime.py"
        if runtime_path.exists() and not any(item["path"] == "app/pbc_runtime.py" for item in compile_failures):
            try:
                spec = importlib.util.spec_from_file_location("generated_pbc_runtime_smoke", runtime_path)
                generated_pbc_runtime = importlib.util.module_from_spec(spec)
                assert spec.loader is not None
                spec.loader.exec_module(generated_pbc_runtime)
                runtime_manifest = generated_pbc_runtime.pbc_runtime_manifest()
                runtime_workbench = generated_pbc_runtime.pbc_composition_runtime_workbench()
                runtime_registration = generated_pbc_runtime.register_generated_pbc_package(
                    {
                        **example_pbc_manifest(),
                        "pbc": "generated_warranty_claims",
                        "tests": ("tests/test_generated_warranty_claims.py",),
                        "docs": ("README.md",),
                    }
                )
                runtime_smoke = generated_pbc_runtime.smoke_test()
            except Exception as exc:  # pragma: no cover - reported in audit payload
                runtime_smoke = {"ok": False, "error": str(exc)}
        for key in selected:
            test_path = output_dir / "pbcs" / key / "tests" / "test_contract.py"
            if not test_path.exists():
                generated_contract_test_results.append(
                    {
                        "pbc": key,
                        "ok": False,
                        "path": str(Path("app") / "pbcs" / key / "tests" / "test_contract.py"),
                        "error": "missing generated contract test",
                    }
                )
                continue
            before_modules = set(sys.modules)
            sys.path.insert(0, str(output_dir))
            try:
                module = importlib.import_module(f"pbcs.{key}.tests.test_contract")
                executed = []
                for name in sorted(item for item in dir(module) if item.startswith("test_")):
                    getattr(module, name)()
                    executed.append(name)
                generated_contract_test_results.append(
                    {
                        "pbc": key,
                        "ok": bool(executed),
                        "path": str(Path("app") / "pbcs" / key / "tests" / "test_contract.py"),
                        "executed": tuple(executed),
                    }
                )
            except Exception as exc:  # pragma: no cover - reported in audit payload
                generated_contract_test_results.append(
                    {
                        "pbc": key,
                        "ok": False,
                        "path": str(Path("app") / "pbcs" / key / "tests" / "test_contract.py"),
                        "error": str(exc),
                    }
                )
            finally:
                sys.path.remove(str(output_dir))
                for module_name in tuple(sys.modules):
                    if module_name not in before_modules and (module_name == "pbcs" or module_name.startswith("pbcs.")):
                        sys.modules.pop(module_name, None)
    checks = (
        {
            "id": "dsl_tables",
            "ok": len(schema.tables) >= len(selected) * 2,
            "table_count": len(schema.tables),
        },
        {
            "id": "required_artifacts",
            "ok": not missing,
            "missing": missing,
        },
        {
            "id": "compiled_artifacts",
            "ok": not compile_failures
            and {"app/models.py", "app/views.py", "app/pbc_runtime.py"} <= set(compiled)
            and all(f"app/pbcs/{key}/manifest.py" in compiled for key in selected),
            "compiled": tuple(compiled),
            "failures": tuple(compile_failures),
        },
        {
            "id": "generated_pbc_directories",
            "ok": not pbc_artifact_missing
            and pbc_directories_exist,
            "missing": tuple(pbc_artifact_missing),
            "directories": tuple(str(Path("app") / "pbcs" / key) for key in selected),
            "required_artifacts": PBC_IMPLEMENTATION_REQUIRED_ARTIFACTS,
        },
        {
            "id": "generated_pbc_runtime",
            "ok": runtime_smoke["ok"]
            and runtime_manifest.get("format") == "appgen.generated-pbc-runtime-manifest.v1"
            and tuple(selected) == tuple(runtime_manifest.get("selected_pbcs", ()))
            and runtime_workbench.get("ok") is True
            and runtime_registration.get("ok") is True,
            "manifest": runtime_manifest,
            "workbench": runtime_workbench,
            "registration": runtime_registration,
            "smoke": runtime_smoke,
        },
        {
            "id": "generated_pbc_contract_tests",
            "ok": len(generated_contract_test_results) == len(selected)
            and all(result["ok"] for result in generated_contract_test_results),
            "results": tuple(generated_contract_test_results),
        },
    )
    return {
        "format": "appgen.pbc-generation-smoke-audit.v1",
        "ok": all(check["ok"] for check in checks),
        "selected_pbcs": selected,
        "dsl": dsl,
        "checks": checks,
    }


def _package_manifest(key: str) -> dict:
    """Return the package's declared manifest, or an empty dict.

    The package is the single source of truth for a PBC's tables, events, and
    datastore. The catalog literal is a fallback for entries whose package
    cannot be imported; when it can, the package wins so the two cannot drift.
    """
    try:
        module = importlib.import_module(f"pyAppGen.pbcs.{key}.manifest")
    except ImportError:
        return {}
    manifest = getattr(module, "PBC_MANIFEST", None)
    return manifest if isinstance(manifest, dict) else {}


def _package_event_types(key: str) -> tuple[tuple[str, ...], tuple[str, ...]]:
    """Return the events a PBC package's runtime declares it emits and consumes.

    The package publishes its event surface twice: as ``*_EMITTED_EVENT_TYPES``
    and ``*_CONSUMED_EVENT_TYPES`` in ``runtime.py``, and again as ``emits`` and
    ``consumes`` in its manifest. They are both hand-maintained and had drifted
    apart in a dozen packages, in both directions, so the descriptor was reading
    whichever the manifest happened to say. The runtime constants are what the
    package's own api and service contracts are built from, so they win; a
    package that publishes none falls back to its manifest.
    """
    try:
        module = importlib.import_module(f"pyAppGen.pbcs.{key}.runtime")
    except ImportError:
        return (), ()
    prefix = key.upper()
    emits = tuple(getattr(module, f"{prefix}_EMITTED_EVENT_TYPES", None) or ())
    consumes = tuple(getattr(module, f"{prefix}_CONSUMED_EVENT_TYPES", None) or ())
    return emits, consumes


# The declared surfaces whose runtime constant, where it exists, is the package's
# own statement of them. `permissions` and `configuration` have no runtime
# constant in any of the 147 packages, so the manifest is their only source and
# they are absent here.
#
# All three listed surfaces now agree with the manifest in 147 of 147. They did
# not always: `field_service_management`'s `*_RUNTIME_CAPABILITY_KEYS` was a
# stale 12 against a manifest and runtime function of 17, and
# `clinical_trials_management`'s manifest listed 9 fragments against a runtime
# constant of 13. Both packages were fixed rather than papered over, because the
# runtime is the surface the code exposes and the manifest is a hand-copy of it.
# An earlier version of this comment had the direction backwards, claiming the
# manifest was the smaller side; it was the runtime constant. Where the two
# disagree, treat the runtime as authoritative and fix the other side.
_PBC_SURFACE_RUNTIME_CONSTANTS = {
    "ui_fragments": "UI_FRAGMENT_KEYS",
    "standard_features": "STANDARD_FEATURE_KEYS",
    "advanced_capabilities": "RUNTIME_CAPABILITY_KEYS",
}


def _package_declared_surface(
    key: str, field: str, manifest: dict, runtime: object | None
) -> tuple:
    """Return a declared surface from the package: runtime constant, else manifest.

    These five surfaces are what the specification's traceability appendix claims
    to cover, and the appendix must be checked against the package, not against
    the catalog literal. The literal was the only source the check used to read,
    and the descriptor migration had emptied it, so the check passed while the
    appendix said "None declared" for a package with thirteen fragments. Reading
    the package makes that vacuity impossible: an empty declared set can only mean
    the package really declares nothing.
    """
    suffix = _PBC_SURFACE_RUNTIME_CONSTANTS.get(field)
    if suffix and runtime is not None:
        values = getattr(runtime, f"{key.upper()}_{suffix}", None)
        if values:
            return tuple(values)
    return tuple(manifest.get(field, ()) or ())


def _pbc_descriptor(key: str, pbc: dict) -> dict:
    manifest = _package_manifest(key)
    tables = tuple(manifest.get("tables", ()) or pbc.get("tables", ()))
    runtime_emits, runtime_consumes = _package_event_types(key)
    try:
        runtime = importlib.import_module(f"pyAppGen.pbcs.{key}.runtime")
    except ImportError:
        runtime = None
    emits = runtime_emits or tuple(manifest.get("emits", ()) or pbc.get("emits", ()))
    consumes = runtime_consumes or tuple(manifest.get("consumes", ()) or pbc.get("consumes", ()))
    # `tables` is the manifest's declared inventory in logical spelling, which
    # `_table_contract` consumes. It is not the whole story: a package's
    # `*_OWNED_TABLES` names every physical table it owns, and for `gl_core` and
    # `ar_credit` that set is larger than the manifest's (event plumbing, plus
    # domain tables the manifest never declared). The package is authoritative,
    # so its inventory is carried alongside rather than overwriting the
    # declared view, and a test asserts the two agree so drift fails CI.
    owned = _owned_tables(key)
    route_records = _package_route_records(key)
    return {
        "pbc": key,
        # Every descriptive field comes from the package, which is the source of
        # truth, with the catalog literal as the fallback for an entry whose
        # package cannot be imported. `label` and `mesh` happen to agree in all
        # 147 today, but reading them from the package anyway means the literal
        # is never consulted for a fact the package already carries, so there is
        # one fewer place for the two to drift. `description` had drifted in 22
        # packages and `template` in 3, each time because the package grew and
        # the literal did not.
        #
        # `apis` now comes from the package's own `routes.py` too. It feeds
        # `_api_contract`, which generates the app's real routes, and the literal
        # was the last surface still hand-maintained: for `dam_core` it named 3
        # routes against a package that dispatches 34, and for `gl_core` it named
        # advanced-capability endpoints (`/temporal-ledger`, `/audit-proofs`) that
        # no runtime command implements. The package's `routes.py` is the surface
        # its own `dispatch_route` walks, so it is the one the emitted app must
        # carry. `_package_route_records` falls back to the literal only when the
        # package declares no routes or cannot be imported.
        "label": manifest.get("label") or pbc["label"],
        "mesh": manifest.get("mesh") or pbc["mesh"],
        "mesh_label": PBC_MESHES[manifest.get("mesh") or pbc["mesh"]]["label"],
        "description": manifest.get("description") or pbc["description"],
        "datastore": f"{key}_store",
        "datastore_backend": manifest.get("datastore_backend")
        or pbc.get("datastore_backend", "postgresql"),
        "stream_processor": manifest.get("stream_processor")
        or pbc.get("stream_processor"),
        "stream_exception_evidence": dict(
            manifest.get("stream_exception_evidence")
            or pbc.get("stream_exception_evidence", {})
        ),
        "tables": tables,
        "owned_tables": owned,
        "apis": tuple(f"{record['method']} {record['path']}" for record in route_records),
        "emits": emits,
        "consumes": consumes,
        # `template` stays on the literal too. It is an optional ERP bridge key,
        # and the drift runs both ways: `streaming_analytics` says `None` where
        # the literal says `reporting`, so there is no superset to adopt. Which
        # bridge a PBC maps to is a routing decision, not a stale copy.
        "template": pbc["template"],
        "package_directory": f"pbcs/{key}",
        "selectable": True,
        # The five declared surfaces the specification's traceability appendix
        # claims to cover. They live on the descriptor so the check reads the
        # package's own statement of them rather than the catalog literal, which
        # the descriptor migration emptied. Carried here rather than read
        # directly in the check because the descriptor is the one place a PBC's
        # declared surface is assembled, and the check must not grow a second
        # path to the package that can drift from this one.
        **{
            field: _package_declared_surface(key, field, manifest, runtime)
            for field in (
                "ui_fragments",
                "permissions",
                "configuration",
                "standard_features",
                "advanced_capabilities",
            )
        },
    }


def _pbc_descriptor_from_manifest(manifest: dict) -> dict:
    key = manifest["pbc"]
    return {
        "pbc": key,
        "label": manifest["label"],
        "mesh": manifest["mesh"],
        "mesh_label": PBC_MESHES[manifest["mesh"]]["label"],
        "description": manifest["description"],
        "datastore": f"{key}_store",
        "datastore_backend": manifest["datastore_backend"],
        "stream_processor": manifest.get("stream_processor", "faust_streaming"),
        "stream_exception_evidence": dict(manifest.get("stream_exception_evidence", {})),
        "tables": tuple(manifest["tables"]),
        "apis": tuple(manifest["apis"]),
        "emits": tuple(manifest["emits"]),
        "consumes": tuple(manifest["consumes"]),
        "template": manifest.get("template"),
        "ui_fragments": tuple(manifest.get("ui_fragments", ())),
        "permissions": tuple(manifest.get("permissions", ())),
        "configuration": tuple(manifest.get("configuration", ())),
        "migrations": tuple(manifest.get("migrations", ())),
        "seed_data": tuple(manifest.get("seed_data", ())),
        "tests": tuple(manifest.get("tests", ())),
        "docs": tuple(manifest.get("docs", ())),
        "package_directory": f"pbcs/{key}",
        "selectable": True,
    }


def _service_contract(key: str) -> dict:
    pbc = PBC_CATALOG[key]
    class_name = "".join(part.capitalize() for part in key.split("_"))
    return {
        **_pbc_descriptor(key, pbc),
        "class_name": class_name,
        "api_base": f"/api/pbc/{key}",
        "event_topic": f"pbc.{key}.events",
        "inbox_topic": f"pbc.{key}.inbox",
        "owner": key,
    }


def _snake(value: str) -> str:
    words = re.findall(r"[A-Z]?[a-z0-9]+|[A-Z]+(?=[A-Z]|$)", value)
    return "_".join(word.lower() for word in words) or value.lower()


# A permission the generator invented (`dam_core.command.1`) rather than one the
# package declares (`dam_core.customer`). Seventeen packages carry the numbered
# form in their own `routes.py`; it is a placeholder, not a real grant.
_NUMBERED_ROUTE_PERMISSION = re.compile(r"\.(command|query)\.\d+$")


def _declared_route_permission(key: str, operation_kind: str) -> str:
    """Return a permission from the package's own declared vocabulary.

    Seventeen packages write a numbered placeholder into their own `routes.py`
    (`ar_credit.command.4`) for routes their `build_api_contract()` does not also
    name, so no semantic permission is available to join. Inventing a new numbered
    string is what this change exists to remove, and a permission the package
    never declared would not be grantable, so the fallback is drawn from the verbs
    the package itself publishes: `read` for a query, and `create` (else `operate`)
    for a command. Every one of the seventeen declares `read`; the generic-verb
    packages declare `create`, and a package that declares neither keeps the
    numbered form rather than a fabricated one.
    """
    try:
        runtime = importlib.import_module(f"pyAppGen.pbcs.{key}.runtime")
    except ImportError:
        runtime = None
    declared = tuple(
        _package_declared_surface(key, "permissions", _package_manifest(key), runtime) or ()
    )
    if operation_kind == "query":
        for verb in ("read", "operate"):
            if f"{key}.{verb}" in declared:
                return f"{key}.{verb}"
    else:
        for verb in ("create", "operate", "admin"):
            if f"{key}.{verb}" in declared:
                return f"{key}.{verb}"
    return f"{key}.{'read' if operation_kind == 'query' else 'operate'}"


def _owned_tables(key: str) -> tuple[str, ...]:
    """Return the physical tables a PBC package owns.

    Three surfaces describe the same inventory and none is complete on its own.
    ``*_OWNED_TABLES`` is the base declaration; ``*_RUNTIME_TABLES`` adds the
    outbox, inbox, and dead-letter tables that live in the PBC's schema; and
    ``*_runtime_capabilities()`` is where a package that extends itself past the
    base declaration (a ``domain_depth`` or ``slice_app`` layer) reports the
    union. Reading only the constant under-reports those extended packages, so
    all three are folded together and the package's own capability surface wins.
    """
    try:
        module = importlib.import_module(f"pyAppGen.pbcs.{key}")
    except ImportError:
        return ()
    owned = getattr(module, f"{key.upper()}_OWNED_TABLES", None) or ()
    runtime = getattr(module, f"{key.upper()}_RUNTIME_TABLES", None) or ()
    try:
        capabilities = tuple(_pbc_runtime_capabilities(key).get("owned_tables") or ())
    except (AttributeError, ValueError, ImportError):
        capabilities = ()
    return tuple(dict.fromkeys((*owned, *runtime, *capabilities)))


def _unresolved_manifest_tables(key: str) -> tuple[str, ...]:
    """Return manifest-declared tables that the package does not own.

    The manifest is the package's public table contract and the owned-table
    constants are its physical inventory; a name that appears in the first and
    not the second is drift. Either spelling counts as owned, because some
    manifests declare the physical name and others the generated key-prefixed
    one.
    """
    manifest = _package_manifest(key)
    owned = _owned_tables(key)
    return tuple(
        table
        for table in manifest.get("tables", ()) or ()
        if _owned_table_name(key, str(table), owned) not in owned
    )


def _document_candidate_tables(document: dict) -> tuple[str, ...]:
    """Return the tables a document-instruction plan proposes to touch.

    Packages publish the plural ``candidate_tables``; two older packages publish
    a singular ``candidate_table`` instead. Both describe the same obligation, so
    the plan is read from whichever key is present.
    """
    plural = tuple(document.get("candidate_tables") or ())
    if plural:
        return plural
    singular = document.get("candidate_table")
    return (singular,) if singular else ()


def _is_owned_table_reference(key: str, table: str) -> bool:
    """Return whether a table reference names a table the package owns.

    Packages expose candidate tables under either the physical name (``asset``
    for ``dam_core``) or the generated key-prefixed name
    (``api_gateway_mesh_service_registration`` for an owned
    ``service_registration``). Both name the package's own tables, so the check
    accepts either rather than assuming one prefix.
    """
    owned = _owned_tables(key)
    if table in owned:
        return True
    prefix = f"{key}_"
    return table.startswith(prefix) and table[len(prefix) :] in owned


def _owned_table_name(key: str, logical: str, owned: tuple[str, ...]) -> str:
    """Resolve a logical table to its physical name in the package.

    Packages name owned tables with a domain prefix that is not always the PBC
    key: ``ar_credit`` owns ``ar_customer``, ``gl_core`` owns
    ``gl_core_ledger_event_log``, and ``dam_core`` owns ``asset`` unprefixed.
    The package is authoritative, so the physical name is looked up rather than
    reconstructed. A logical name that resolves to nothing falls back to the
    key-prefixed form, which the owned-table check then rejects.
    """
    if logical in owned:
        return logical
    suffixed = tuple(name for name in owned if name.endswith(f"_{logical}"))
    if len(suffixed) == 1:
        return suffixed[0]
    return f"{key}_{logical}"


def _route_method_name(key: str, operation_kind: str, path: str) -> str:
    """Return the generated service method a route dispatches to.

    The emitted `services.py` facade exposes one method per route and routes the
    call by the `command_`/`query_` prefix (`gen.py`), so the name is derived from
    the operation kind and path rather than the package's operation label. That
    keeps the handler a unique dispatch key: nine packages reuse an operation name
    across two routes (`gl_core`'s `build_projection` serves both `/gl/projections`
    and `/gl/trial-balance`), and the operation name is carried alongside as data.
    The prefix follows `operation_kind`, not the HTTP verb, because a POST the
    package declares read-only must still route to `_query`.
    """
    path_name = re.sub(r"[^a-zA-Z0-9]+", "_", path).strip("_").lower() or key
    return f"{'query' if operation_kind == 'query' else 'command'}_{path_name}"


def _first_event(value: object) -> str | None:
    """Normalize an emitted-event field that packages spell as a string or tuple."""
    if not value:
        return None
    if isinstance(value, (tuple, list)):
        return next((str(item) for item in value if item), None)
    return str(value)


def _package_route_records(key: str) -> tuple[dict, ...]:
    """Return the route surface the package itself declares, one record per route.

    A PBC publishes its routes three ways and only the third is both complete and
    executable: the catalog literal `PBC_CATALOG[key]["apis"]` (hand-maintained),
    the runtime's `<key>_build_api_contract()["routes"]` (rich dicts for 45
    packages, bare `"METHOD /path"` strings for 102), and the package's own
    `routes.py`, whose `API_ROUTE_CONTRACTS` / `api_route_contracts()` is the
    surface its `dispatch_route` walks. Reading the package is what makes the
    emitted app's route surface the block's real operations rather than a
    literal's shadow: `dam_core`'s literal names 3 routes with invented
    `dam_core.command.1` permissions, while its package declares 34 with
    `dam_core.configure`-style ones, and `gl_core`'s literal names
    advanced-capability endpoints (`/temporal-ledger`, `/audit-proofs`) that no
    runtime command implements.

    Precedence is `API_ROUTE_CONTRACTS` (full per-route metadata, 48 packages),
    then `api_route_contracts()` (the route set for all 147), then the runtime's
    dict routes. A package that declares no routes, or one that cannot be
    imported at all, falls back to the catalog literal through `_api_contract`, so
    a package is checked against itself wherever it can be.
    """
    owned = _owned_tables(key)
    runtime_permissions = _runtime_route_permissions(key)
    service_scope = _package_service_scope(key)
    raw: tuple = ()
    try:
        module = importlib.import_module(f"pyAppGen.pbcs.{key}.routes")
    except ImportError:
        module = None
    if module is not None:
        raw = tuple(getattr(module, "API_ROUTE_CONTRACTS", ()) or ())
        if not raw:
            builder = getattr(module, "api_route_contracts", None)
            if callable(builder):
                try:
                    contract = builder()
                except Exception:
                    contract = {}
                raw = tuple(contract.get("contracts") or contract.get("routes") or ())
    if not raw:
        runtime_routes = _runtime_dict_routes(key)
        raw = runtime_routes
    if not raw:
        return tuple(
            _api_contract(key, api, position)
            for position, api in enumerate(PBC_CATALOG[key].get("apis", ()))
        )
    records = []
    for position, entry in enumerate(raw):
        record = _normalize_package_route(
            key, entry, position, owned, runtime_permissions, service_scope
        )
        if record is not None:
            records.append(record)
    return tuple(records)


def _runtime_route_permissions(key: str) -> dict[tuple[str, str], str]:
    """Map `(method, bare path)` to the semantic permission the runtime declares.

    Seventeen packages write a numbered placeholder into their `routes.py`
    (`ar_credit.command.1`) while their `build_api_contract()` carries the real
    one (`ar_credit.customer`). The runtime is the richer statement of intent, so
    its permission is joined in by route rather than the placeholder shipped.
    """
    try:
        runtime = importlib.import_module(f"pyAppGen.pbcs.{key}.runtime")
    except ImportError:
        return {}
    builder = getattr(runtime, f"{key}_build_api_contract", None)
    if not callable(builder):
        return {}
    try:
        routes = tuple(builder().get("routes", ()) or ())
    except Exception:
        return {}
    mapping: dict[tuple[str, str], str] = {}
    for route in routes:
        if not isinstance(route, dict):
            continue
        permission = route.get("requires_permission")
        route_text = str(route.get("route") or "")
        method, _, path = route_text.partition(" ")
        if permission and method and path:
            mapping[(method.upper(), path)] = str(permission)
    return mapping


def _package_service_scope(key: str) -> dict[tuple[str, str], dict]:
    """Map `(method, bare path)` to the scope and event the package's service layer declares.

    A package states each route's table scope twice: coarsely in `routes.py` and
    precisely in its executable `services.py`. `ar_credit`'s `routes.py` gives
    every command all 34 owned tables, while its `services.py` names the four to
    seven tables the operation actually writes; `gl_core`'s `routes.py` gives its
    inbox command nothing, while `services.py` gives it the inbox table. The
    emitted `services.py` is a structural copy of the source one, so the service
    layer is the authority for per-operation scope and the event it emits, and
    `routes.py` remains the authority for which routes exist.

    Only entries carrying a `method` and `path` are joined; some packages publish
    a service contract of a different shape (`contract_lifecycle`'s form-bound
    operations), and those are left to the route record's own fields.
    """
    try:
        module = importlib.import_module(f"pyAppGen.pbcs.{key}.services")
    except ImportError:
        return {}
    builder = getattr(module, "service_operation_contracts", None)
    if not callable(builder):
        return {}
    try:
        contracts = tuple(builder().get("contracts") or ())
    except Exception:
        return {}
    prefix = f"/api/pbc/{key}"
    mapping: dict[tuple[str, str], dict] = {}
    for contract in contracts:
        if not isinstance(contract, dict):
            continue
        method = str(contract.get("method") or "").upper()
        path = str(contract.get("path") or "")
        if not method or not path:
            continue
        bare = path[len(prefix):] if path.startswith(prefix) else path
        if not bare.startswith("/"):
            bare = f"/{bare}"
        mapping[(method, bare)] = contract
    return mapping


def _runtime_dict_routes(key: str) -> tuple[dict, ...]:
    """Return the runtime's own route dicts, if it declares them as dicts."""
    try:
        runtime = importlib.import_module(f"pyAppGen.pbcs.{key}.runtime")
    except ImportError:
        return ()
    builder = getattr(runtime, f"{key}_build_api_contract", None)
    if not callable(builder):
        return ()
    try:
        routes = tuple(builder().get("routes", ()) or ())
    except Exception:
        return ()
    return routes if routes and isinstance(routes[0], dict) else ()


def _normalize_package_route(
    key: str,
    entry: object,
    position: int,
    owned: tuple[str, ...],
    runtime_permissions: dict[tuple[str, str], str] | None = None,
    service_scope: dict[tuple[str, str], dict] | None = None,
) -> dict | None:
    """Normalize one package route record into the contract's route shape.

    The record keeps the same keys `_api_contract` produces (`path` bare, `route`
    prefixed) so every downstream reader is unchanged, and adds the real
    `permission`, `owned_tables`, `read_tables`, `emitted_event`, `operation`, and
    `operation_kind` the package declares. A package that omits the table scope or
    the event (the 99 thin packages) falls back to the package's own owned tables
    and emitted-event list, never to the numbered permissions the literal forced.
    A permission the package wrote as a numbered placeholder is replaced by the
    runtime's semantic one for the same route.
    """
    if isinstance(entry, str):
        method, _, path = entry.partition(" ")
        entry = {"method": method, "path": path}
    if not isinstance(entry, dict):
        return None
    method = str(entry.get("method") or "").upper()
    path = str(entry.get("path") or "")
    if not method and entry.get("route"):
        method, _, path = str(entry["route"]).partition(" ")
        method = method.upper()
    if not method or not path:
        return None
    prefix = f"/api/pbc/{key}"
    bare = path[len(prefix):] if path.startswith(prefix) else path
    if not bare.startswith("/"):
        bare = f"/{bare}"
    operation = (
        entry.get("operation")
        or entry.get("command")
        or entry.get("query")
        or entry.get("handler")
    )
    operation_kind = "query" if method == "GET" else str(entry.get("operation_kind") or "command")
    permission = (
        entry.get("permission")
        or entry.get("required_permission")
        or f"{key}.{'read' if operation_kind == 'query' else 'operate'}"
    )
    if _NUMBERED_ROUTE_PERMISSION.search(permission) and runtime_permissions:
        permission = runtime_permissions.get((method, bare), permission)
    if _NUMBERED_ROUTE_PERMISSION.search(permission):
        permission = _declared_route_permission(key, operation_kind)
    # The package states each route's scope twice: coarsely in `routes.py` and
    # precisely in its executable `services.py`. `ar_credit`'s `routes.py` gives
    # every command all 34 owned tables while its `services.py` names the four to
    # seven the operation writes, and `gl_core`'s inbox command is empty in
    # `routes.py` but the inbox table in `services.py`. The emitted `services.py`
    # is a structural copy of the source one, so the service layer wins whenever
    # it declares a scope, and the route's own scope is the fallback.
    service_entry = (service_scope or {}).get((method, bare))
    route_owned = _resolve_route_tables(key, entry.get("owned_tables"), owned)
    route_read = _resolve_route_tables(key, entry.get("read_tables"), owned)
    owned_tables = route_owned
    read_tables = route_read
    if isinstance(service_entry, dict):
        svc_owned = _resolve_route_tables(key, service_entry.get("owned_tables"), owned)
        svc_read = _resolve_route_tables(key, service_entry.get("read_tables"), owned)
        if svc_owned or svc_read:
            owned_tables, read_tables = svc_owned, svc_read
    if not owned_tables and not read_tables:
        # 627 routes across 105 packages declare no scope at all, so the fallback
        # is the package's whole owned set. It is spelled physically here for the
        # same reason the declared scope is: six packages publish short logical
        # names in `_owned_tables`, and the emitted app rejects any scope entry
        # that does not start with `<key>_`.
        every = _resolve_route_tables(key, owned, owned)
        if operation_kind == "query":
            read_tables = every
        else:
            owned_tables = every
    # A package's kind decides which side of the scope the tables land on: the
    # facade validates that a command owns tables and reads none, and a query the
    # reverse. A package that puts tables on the wrong side (a query declaring
    # `owned_tables`) is read on the side its kind requires.
    if operation_kind == "query":
        if not read_tables:
            read_tables = owned_tables
        owned_tables = ()
    else:
        if not owned_tables:
            owned_tables = read_tables
        read_tables = ()
    emitted_event = _first_event(
        (service_entry or {}).get("emitted_event") if isinstance(service_entry, dict) else None
    ) or _first_event(entry.get("emitted_event") or entry.get("emits"))
    if emitted_event is None and operation_kind == "command":
        emitted = _package_event_types(key)[0]
        emitted_event = emitted[position % len(emitted)] if emitted else None
    path_name = re.sub(r"[^a-zA-Z0-9]+", "_", bare).strip("_").lower() or key
    # The dispatch name's prefix must match `operation_kind`, because the emitted
    # facade routes a call to `_query`/`_command` by that prefix and validates the
    # kind against the table scope. Seven routes are a POST the package itself
    # declares read-only (`gl_core`'s `verify_journal_invariants`, the assistant
    # document previews), so the prefix follows the declared kind, not the verb.
    method_name = _route_method_name(key, operation_kind, bare)
    return {
        "method": method,
        "path": bare,
        "route": f"{prefix}{bare}",
        "handler": method_name,
        "service_method": method_name,
        "operation": operation or method_name,
        "operation_kind": operation_kind,
        "permission": permission,
        "owned_tables": owned_tables,
        "read_tables": read_tables,
        "emitted_event": emitted_event,
        "idempotency_key": entry.get("idempotency_key"),
        "request_schema": f"{key}.{path_name}.request.v1",
        "response_schema": f"{key}.{path_name}.response.v1",
    }


def _resolve_route_tables(
    key: str,
    value: object,
    owned: tuple[str, ...],
) -> tuple[str, ...]:
    """Resolve a route's table names to the physical spelling the app emits.

    A package names its routes' tables four ways and only one is usable as an
    emitted scope: the physical name (`dam_core`'s `dam_core_dam_configuration`,
    absent from `_owned_tables`, whose short names are `asset`,
    `dam_configuration`), the key-prefixed physical name, the short logical name
    (`ar_credit`'s `ar_customer`, `time_labor`'s `shift`), and a name carrying no
    prefix at all (`payroll_engine`'s `payroll_calendar`). The generated app
    validates that every scope entry starts with `<key>_`, and its migration
    creates only the service contract's tables, so a scope must name a table the
    app actually emits.

    A name is therefore kept only when it is already emitted, or when it is
    owned *and* key-prefixed (a physical name the service contract omits, which
    the package still owns). Everything else is resolved through
    `_physical_table_name`, which reads the migration and the owned set rather
    than reconstructing a name. Reading only `owned` was not enough: six packages
    publish short logical names there, so `shift` and `payroll_calendar` passed
    the owned check and shipped unprefixed.
    """
    if not value:
        return ()
    if isinstance(value, str):
        value = (value,)
    emitted = _contract_table_names(key, owned)
    resolved = []
    for table in value:
        name = str(table)
        # A package can double its own prefix by accident: `dam_core`'s routes
        # declare `dam_core_dam_core_appgen_outbox_event` for an owned
        # `dam_core_appgen_outbox_event`. Collapse one prefix when the result is
        # a table the package really owns, so the emitted scope names a real
        # table rather than a misspelling of one.
        doubled = f"{key}_{key}_"
        if name.startswith(doubled):
            collapsed = f"{key}_{name[len(doubled):]}"
            if collapsed in owned or collapsed in emitted:
                name = collapsed
        if name not in emitted and not (name in owned and name.startswith(f"{key}_")):
            name = _physical_table_name(key, name, owned)
        if name and name not in resolved:
            resolved.append(name)
    return tuple(resolved)


def _table_contract(
    key: str,
    table: str,
    primary_table: str,
    position: int,
    owned: tuple[str, ...] = (),
) -> dict:
    """Return the owned-table contract for one logical table.

    Columns, foreign keys and unique constraints all come from the package's own
    migration, which is the one place a PBC states its real schema and is uniform
    across all 147 packages. The contract used to invent them: every table at
    `position > 0` was given a synthetic `<primary_table>_id INTEGER` foreign key
    pointing at `service["tables"][0].id`, whether or not the package had such a
    column and whatever type the real one carried. `dam_core_asset_version`
    declares `asset_id` as `VARCHAR(255)` referencing `dam_core_asset.asset_id`
    (a unique business key), and the emitter pointed it at `dam_core_asset.id`
    (an `INTEGER` surrogate) instead, so the generated migration failed to apply
    for 117 of 147 packages.

    The package's own names are adopted rather than reconstructed. `ar_credit`
    migrates `ar_credit_ar_customer` and declares `ar_customer`; prefixing the
    logical name gave `ar_credit_customer`, a table no migration creates. The
    migration is looked up by logical name, by the package's own resolved name,
    and by the key-prefixed form, and the first match wins.

    A relationship whose target is outside the tables this contract emits is
    dropped: the generated migration creates only the service contract's tables,
    and Postgres rejects a foreign key to a table that is not there.
    """
    owned_table = _physical_table_name(key, table, owned)
    fields = _table_fields(key, table, owned, primary_table, position)
    schema = pbc_schema.owned_schema(key).get(owned_table) or {}
    emitted = _contract_table_names(key, owned)
    relationships = tuple(
        relationship
        for relationship in schema.get("relationships", ())
        if relationship["target_table"] in emitted
    )
    return {
        "logical_table": table,
        "owned_table": owned_table,
        "fields": tuple(fields),
        "relationships": relationships,
        "composite_primary_key": tuple(schema.get("composite_primary_key", ())),
        "unique": tuple(schema.get("unique", ())),
    }


def _contract_table_names(key: str, owned: tuple[str, ...]) -> frozenset[str]:
    """Return the physical names of every table this contract emits.

    The emitted set is the physical spelling of the manifest's declared tables
    (`_service_contract`'s `tables`, which `_pbc_descriptor` also carries). It is
    read from the manifest directly rather than through `_service_contract`, which
    would re-enter `_pbc_descriptor` and, from there, `_package_route_records` and
    this resolver, looping forever.
    """
    manifest = _package_manifest(key)
    declared = tuple(manifest.get("tables", ()) or PBC_CATALOG[key].get("tables", ()))
    return frozenset(
        _physical_table_name(key, table, owned) for table in declared
    )


def _physical_table_name(key: str, logical: str, owned: tuple[str, ...] = ()) -> str:
    """Return the name the package's migration uses for one logical table.

    The migration is authoritative: a package that migrates
    `ar_credit_ar_customer` owns that table under that name, and a contract that
    calls it `ar_credit_customer` describes a table nothing creates. The logical
    name, the package's own resolved name, and the key-prefixed form are tried in
    turn, then a suffix match, and only a name no migration declares falls back
    to the key-prefixed form.
    """
    schema = pbc_schema.owned_schema(key)
    resolved = _owned_table_name(key, logical, owned or _owned_tables(key))
    for candidate in (logical, resolved, f"{key}_{logical}", f"{key}_{resolved}"):
        if candidate in schema:
            return candidate
    suffixed = tuple(name for name in schema if name.endswith(f"_{logical}"))
    if len(suffixed) == 1:
        return suffixed[0]
    return logical if logical.startswith(f"{key}_") else f"{key}_{logical}"


def _table_fields(
    key: str,
    table: str,
    owned: tuple[str, ...],
    primary_table: str,
    position: int,
) -> list[dict]:
    """Return the columns for one table, from the migration when it matches.

    A package names a table with a prefix that is not always the PBC key, and
    its runtime and its migration do not always agree on the name (`ar_credit`
    migrates `ar_credit_ar_customer` but declares `ar_customer`). Each of the
    two known names is therefore offered both bare and key-prefixed, and the
    first that the migration declares wins.
    """
    migration_names = tuple(pbc_schema.owned_schema(key))
    resolved = _physical_table_name(key, table, owned or migration_names)
    candidates = (
        table,
        resolved,
        f"{key}_{table}",
        f"{key}_{resolved}",
    )
    parsed = pbc_schema.fields_for(key, candidates)
    if parsed:
        return [dict(field) for field in parsed]
    contract_fields = _package_schema_fields(key, candidates)
    if contract_fields:
        return contract_fields
    return _fallback_table_fields(key, primary_table, position)


def _package_schema_fields(key: str, candidates: tuple[str, ...]) -> list[dict]:
    """Return a table's columns from the package's own schema contract.

    The migration is the first source, and for 112 of 147 packages it is also
    the only one needed. Fourteen packages declare owned tables their migration
    never creates, and the descriptor answered those with the generic
    `code`/`status`/`version` envelope, so the generated app declared a
    `field_service_management_technician_live_location` with no technician and
    no location. The package's `build_schema_contract()` names the columns for
    every table it owns, including those the migration omits, so it is a truer
    fallback than the envelope. Its `fields` are bare column names in most
    packages and typed dicts in a few, so both shapes are read.

    The column *names* come from the package; the types are inferred from the
    name, because the contract does not carry them. That is a weaker claim than
    the migration's, which is why the migration is still tried first: an
    inferred type can be wrong, and only the package's SQL is authoritative.
    """
    try:
        module = importlib.import_module(f"pyAppGen.pbcs.{key}.runtime")
    except ImportError:
        return []
    build = getattr(module, f"{key}_build_schema_contract", None)
    if build is None:
        return []
    try:
        contract = build()
    except Exception:
        return []
    wanted = set(candidates)
    for collection in ("tables", "runtime_tables"):
        for table in contract.get(collection) or ():
            if not isinstance(table, dict) or str(table.get("table")) not in wanted:
                continue
            return _contract_fields(key, table.get("fields") or ())
    return []


def _contract_fields(key: str, fields: tuple) -> list[dict]:
    """Type a package schema contract's field list.

    A typed entry (`{"name": ..., "type": ...}`) is used as written. A bare
    column name is typed from its own spelling: the suffixes and names a PBC
    convention gives a fixed meaning (`*_at` is a timestamp, `attempts` a
    count, `payload` structured data). The first field is the primary key,
    which is the package's own convention, and every other column is required,
    which is how the packages declare their envelope.
    """
    typed: list[dict] = []
    for position, field in enumerate(fields):
        if isinstance(field, dict) and field.get("name"):
            entry = dict(field)
            entry.setdefault("required", not entry.get("nullable", True))
            typed.append(entry)
            continue
        name = str(field)
        entry = {
            "name": name,
            "type": _contract_field_type(name),
            "required": True,
            "nullable": False,
        }
        if position == 0:
            entry["primary_key"] = True
        typed.append(entry)
    return typed


def _contract_field_type(name: str) -> str:
    """Infer a canonical column type from a PBC column name."""
    if name.endswith("_at") or name in {"created_at", "updated_at", "occurred_at", "published_at", "processed_at"}:
        return "datetime"
    if name in {"payload", "payload_json", "data", "metadata", "context", "history", "states", "transitions"}:
        return "json"
    if name in {"attempts", "retry_count", "version", "capacity_minutes", "sample_size", "duration_ms", "retry_budget", "deadline_seconds"}:
        return "integer"
    if name.endswith("_id") and name not in {"id"}:
        return "string"
    return "string"


def _fallback_table_fields(key: str, primary_table: str, position: int) -> list[dict]:
    """Generic column set for a table whose migration could not be matched."""
    fields = [
        {"name": "id", "type": "integer", "primary_key": True, "nullable": False},
        {"name": "code", "type": "string", "required": True, "searchable": True},
        {"name": "status", "type": "string", "required": True, "default": "draft"},
        {"name": "version", "type": "integer", "required": True, "default": 1},
        {"name": "created_at", "type": "datetime", "required": True},
        {"name": "updated_at", "type": "datetime", "required": True},
    ]
    if position > 0:
        fields.insert(
            1,
            {
                "name": f"{primary_table}_id",
                "type": "integer",
                "required": True,
                "references": f"{key}_{primary_table}.id",
            },
        )
    return fields


def _api_contract(key: str, api: str, position: int) -> dict:
    parts = api.split(maxsplit=1)
    method = parts[0] if parts else "POST"
    path = parts[1] if len(parts) > 1 else f"/{key}"
    path_name = re.sub(r"[^a-zA-Z0-9]+", "_", path).strip("_").lower() or key
    verb = {
        "GET": "query",
        "POST": "command",
        "PUT": "command",
        "PATCH": "command",
        "DELETE": "command",
    }.get(method.upper(), "command")
    return {
        "method": method.upper(),
        "path": path,
        "route": f"/api/pbc/{key}{path}",
        "handler": f"{verb}_{path_name}",
        "service_method": f"{verb}_{path_name}",
        "permission": f"{key}.{verb}.{position + 1}",
        "request_schema": f"{key}.{path_name}.request.v1",
        "response_schema": f"{key}.{path_name}.response.v1",
    }


def _domain_functionality_contract(
    key: str,
    service: dict,
    table_contracts: tuple[dict, ...],
    event_contract: dict,
    service_methods: tuple[dict, ...],
) -> dict:
    mesh_profile = {
        "finops": {
            "controls": ("segregation_of_duties", "period_locking", "variance_thresholds", "statutory_evidence"),
            "optimization": "continuous_working_capital_optimization",
            "kpis": ("accuracy_rate", "close_cycle_time", "cash_impact", "compliance_exceptions"),
        },
        "scl": {
            "controls": ("allocation_policy", "lot_traceability", "node_capacity_guard", "exception_quarantine"),
            "optimization": "multi_node_fulfillment_optimization",
            "kpis": ("availability_accuracy", "cycle_time", "service_level", "exception_backlog"),
        },
        "hcm": {
            "controls": ("role_based_access", "eligibility_policy", "approval_chain", "privacy_minimization"),
            "optimization": "skills_capacity_and_pay_accuracy_optimization",
            "kpis": ("cycle_time", "policy_exceptions", "pay_accuracy", "workforce_readiness"),
        },
        "opsmfg": {
            "controls": ("routing_policy", "quality_gate", "asset_safety_guard", "capacity_constraint"),
            "optimization": "closed_loop_plan_to_produce_optimization",
            "kpis": ("plan_adherence", "yield_rate", "downtime_minutes", "quality_escape_rate"),
        },
        "cx": {
            "controls": ("customer_consent", "price_guard", "fulfillment_guard", "credit_policy"),
            "optimization": "customer_order_lifecycle_optimization",
            "kpis": ("conversion_quality", "fulfillment_accuracy", "customer_health", "margin_impact"),
        },
        "platform": {
            "controls": ("tenant_isolation", "contract_compatibility", "policy_as_code", "signed_audit_trail"),
            "optimization": "composition_fabric_self_optimization",
            "kpis": ("policy_latency", "contract_break_rate", "deployment_safety", "audit_completeness"),
        },
        "commerce": {
            "controls": ("checkout_integrity", "payment_risk_policy", "return_policy", "cross_border_compliance"),
            "optimization": "headless_commerce_profitability_optimization",
            "kpis": ("authorization_rate", "route_margin", "return_cycle_time", "landed_cost_accuracy"),
        },
        "content": {
            "controls": ("taxonomy_governance", "rights_policy", "publication_gate", "localization_quality"),
            "optimization": "content_readiness_and_price_optimization",
            "kpis": ("content_completeness", "publication_velocity", "rights_exceptions", "price_effectiveness"),
        },
        "relationship": {
            "controls": ("preference_enforcement", "sla_policy", "consent_boundary", "loyalty_liability_guard"),
            "optimization": "relationship_lifecycle_optimization",
            "kpis": ("response_time", "engagement_quality", "segment_lift", "retention_signal"),
        },
        "intelligence": {
            "controls": ("model_governance", "feature_lineage", "explainability_gate", "drift_guard"),
            "optimization": "real_time_decision_intelligence_optimization",
            "kpis": ("prediction_quality", "drift_score", "decision_latency", "risk_precision"),
        },
    }[service["mesh"]]
    capability_modules = tuple(
        {
            "capability": f"{key}.{table['logical_table']}",
            "owned_table": table["owned_table"],
            "operations": (
                f"capture_{table['logical_table']}",
                f"validate_{table['logical_table']}",
                f"approve_{table['logical_table']}",
                f"optimize_{table['logical_table']}",
                f"audit_{table['logical_table']}",
            ),
            "state_model": ("draft", "validated", "approved", "optimized", "closed"),
            "policy_hooks": mesh_profile["controls"],
            "analytics_hooks": mesh_profile["kpis"],
        }
        for table in table_contracts
    )
    workflow_implementations = tuple(
        {
            "workflow": method["service_method"],
            "route": method["route"],
            "permission": method["permission"],
            "steps": (
                "authorize_actor",
                "validate_request_contract",
                "load_owned_state",
                "run_policy_controls",
                "execute_domain_decision",
                "persist_owned_state",
                "append_outbox_event",
                "record_release_evidence",
            ),
            "compensation": f"compensate_{method['service_method']}",
            "idempotency_key": f"{key}:{method['service_method']}:{{request_id}}",
        }
        for method in service_methods
    )
    policy_controls = tuple(
        {
            "control": control,
            "mode": "policy_as_code",
            "evidence": f"{key}.{control}.evidence.v1",
            "blocks_release": True,
        }
        for control in mesh_profile["controls"]
    )
    automation_loops = (
        {
            "loop": "exception_to_resolution",
            "trigger": "policy_exception_detected",
            "actions": ("classify_exception", "recommend_resolution", "route_approval", "verify_closeout"),
        },
        {
            "loop": "continuous_optimization",
            "trigger": mesh_profile["optimization"],
            "actions": ("simulate_options", "score_tradeoffs", "apply_guarded_decision", "measure_outcome"),
        },
        {
            "loop": "release_evidence_feedback",
            "trigger": "audit_gap_detected",
            "actions": ("capture_gap", "generate_fix_plan", "rerun_contract_tests", "seal_evidence"),
        },
    )
    analytics = tuple(
        {
            "metric": metric,
            "source": "owned_tables_and_event_contracts",
            "grain": "pbc_instance",
            "projection": f"{key}_{metric}_projection",
        }
        for metric in mesh_profile["kpis"]
    ) + tuple(
        {
            "metric": f"{_snake(event['event_type'])}_throughput",
            "source": event["outbox_table"],
            "grain": "event_type",
            "projection": f"{key}_{_snake(event['event_type'])}_projection",
        }
        for event in event_contract["emitted"][:2]
    )
    integration_contracts = tuple(
        {
            "type": "emits",
            "event": event["event_type"],
            "schema": event["schema"],
            "boundary": "outbox_contract",
        }
        for event in event_contract["emitted"]
    ) + tuple(
        {
            "type": "consumes",
            "event": event["event_type"],
            "schema": event["schema"],
            "boundary": "inbox_contract",
        }
        for event in event_contract["consumed"]
    )
    workbench_actions = tuple(
        {
            "action": f"{key}.{verb}",
            "surface": service.get("ui_fragments", (f"{service['class_name']}Workbench",))[0],
            "requires_permission": f"{key}.{verb}",
        }
        for verb in ("inspect", "simulate", "approve", "optimize", "audit")
    )
    release_gates = tuple(
        {
            "gate": dimension,
            "ok_when": f"{dimension}_has_generated_evidence",
        }
        for dimension in PBC_DOMAIN_DEPTH_REQUIRED_DIMENSIONS
    )
    generated_text = repr(
        (
            capability_modules,
            workflow_implementations,
            policy_controls,
            automation_loops,
            analytics,
            integration_contracts,
            workbench_actions,
        )
    ).lower()
    legacy_product_references = tuple(
        term
        for term in ("sap", "salesforce", "quickbooks")
        if re.search(rf"(?<![a-z0-9_]){term}(?![a-z0-9_])", generated_text)
    )
    dimensions = {
        "capability_modules": capability_modules,
        "workflow_implementations": workflow_implementations,
        "policy_controls": policy_controls,
        "automation_loops": automation_loops,
        "analytics": analytics,
        "integration_contracts": integration_contracts,
        "workbench_actions": workbench_actions,
        "release_gates": release_gates,
    }
    return {
        "format": "appgen.pbc-domain-functionality-contract.v1",
        "ok": all(dimensions.values()) and not legacy_product_references,
        "depth_level": PBC_DOMAIN_DEPTH_LEVEL,
        "pbc": key,
        "mesh": service["mesh"],
        "dimensions": tuple(dimensions),
        **dimensions,
        "differentiators": (
            "owned_operational_schema",
            "event_first_composition",
            "policy_as_code_controls",
            "closed_loop_automation",
            "embedded_decision_analytics",
            "side_effect_free_package_registration",
            "release_evidence_by_capability",
        ),
        "legacy_product_references": legacy_product_references,
    }


def _advanced_domain_blueprint(
    key: str,
    service: dict,
    table_contracts: tuple[dict, ...],
    event_contract: dict,
    service_methods: tuple[dict, ...],
) -> dict:
    if key != "gl_core":
        return {}
    owned_tables = {table["logical_table"]: table["owned_table"] for table in table_contracts}
    api_routes = tuple(method["route"] for method in service_methods)
    emitted_events = tuple(event["event_type"] for event in event_contract["emitted"])

    def capability(area: str, name: str, tables: tuple[str, ...], apis: tuple[str, ...], events: tuple[str, ...], evidence: tuple[str, ...]) -> dict:
        return {
            "area": area,
            "capability": name,
            "owned_tables": tuple(owned_tables[table] for table in tables if table in owned_tables),
            "apis": tuple(route for route in api_routes if any(api in route for api in apis)),
            "events": tuple(event for event in emitted_events if event in events),
            "implementation_evidence": evidence,
            "release_gate": f"gl_core.{name}.release_gate",
        }

    capabilities = (
        capability(
            "foundational_architecture",
            "event_sourced_ledger_core",
            ("ledger_event_log", "journal_entry", "journal_line", "ledger_projection"),
            ("/ledger-events", "/ledger-projections", "/journals"),
            ("LedgerEventAppended", "LedgerProjectionRebuilt", "JournalPosted"),
            ("append_only_event_log", "projection_rebuild_plan", "temporal_replay_tests"),
        ),
        capability(
            "foundational_architecture",
            "distributed_consensus_protocol",
            ("consensus_replica", "ledger_event_log"),
            ("/consensus-commits",),
            ("ConsensusCommitted",),
            ("replica_quorum_plan", "leader_election_trace", "sub_second_recovery_objective"),
        ),
        capability(
            "foundational_architecture",
            "schema_on_read_extensibility",
            ("schema_extension", "ledger_projection"),
            ("/schema-extensions", "/ledger-projections"),
            ("LedgerProjectionRebuilt",),
            ("jsonb_extension_registry", "backward_compatible_projection", "zero_downtime_schema_plan"),
        ),
        capability(
            "foundational_architecture",
            "multi_tenant_isolation",
            ("tenant_ledger_partition", "policy_decision", "crypto_key_epoch"),
            ("/ledger-events",),
            ("LedgerEventAppended",),
            ("tenant_partition_keys", "per_tenant_encryption_epoch", "independent_scaling_plan"),
        ),
        capability(
            "computational_analytics",
            "real_time_olap_oltp_convergence",
            ("ledger_event_log", "ledger_projection", "close_snapshot"),
            ("/temporal-ledger", "/trial-balance"),
            ("TrialBalanceCalculated", "LedgerProjectionRebuilt"),
            ("transactional_projection_fanout", "columnar_query_projection", "no_etl_latency_gate"),
        ),
        capability(
            "computational_analytics",
            "probabilistic_accounting_primitives",
            ("probabilistic_posting", "journal_entry"),
            ("/probabilistic-postings",),
            ("PostingValidationPredicted",),
            ("confidence_interval_fields", "statement_uncertainty_propagation", "materiality_policy_gate"),
        ),
        capability(
            "computational_analytics",
            "continuous_close_architecture",
            ("close_snapshot", "control_assertion", "ledger_projection"),
            ("/continuous-close-snapshots",),
            ("ContinuousCloseSnapshotCreated", "PeriodClosed"),
            ("always_audit_ready_projection", "snapshot_generation_plan", "manual_reconciliation_zero_target"),
        ),
        capability(
            "computational_analytics",
            "causal_inference_engine",
            ("causal_scenario", "ledger_projection"),
            ("/causal-scenarios",),
            ("TrialBalanceCalculated",),
            ("counterfactual_scenario_graph", "forecast_linkage", "effect_attribution_report"),
        ),
        capability(
            "intelligence_automation",
            "autonomous_reconciliation",
            ("reconciliation_case", "ledger_event_log"),
            ("/reconciliation-cases",),
            ("ReconciliationSuggested",),
            ("ml_match_candidates", "explainable_exception_reason", "self_correcting_posting_suggestion"),
        ),
        capability(
            "intelligence_automation",
            "semantic_transaction_understanding",
            ("semantic_source_document", "ledger_account"),
            ("/semantic-documents",),
            ("JournalPosted",),
            ("document_semantic_parse", "account_derivation_trace", "source_to_posting_audit_link"),
        ),
        capability(
            "intelligence_automation",
            "regulatory_logic_compilation",
            ("regulatory_rule_version", "policy_decision"),
            ("/regulatory-rules",),
            ("RegulatoryRuleCompiled",),
            ("declarative_rule_versioning", "impact_analysis_plan", "jurisdictional_effective_dates"),
        ),
        capability(
            "intelligence_automation",
            "predictive_posting_validation",
            ("predictive_validation_run", "journal_entry"),
            ("/predictive-validations",),
            ("PostingValidationPredicted",),
            ("pre_execution_simulation", "cash_flow_constraint_check", "compliance_risk_score"),
        ),
        capability(
            "compliance_governance",
            "zero_knowledge_audit_proofs",
            ("audit_proof", "crypto_key_epoch"),
            ("/audit-proofs",),
            ("AuditProofGenerated",),
            ("proof_channel", "sensitive_data_minimization", "verifier_transcript_hash"),
        ),
        capability(
            "compliance_governance",
            "dynamic_policy_enforcement",
            ("policy_decision", "tenant_ledger_partition"),
            ("/journals", "/predictive-validations"),
            ("JournalPosted", "PostingValidationPredicted"),
            ("attribute_policy_context", "real_time_posting_restriction", "policy_decision_audit"),
        ),
        capability(
            "compliance_governance",
            "immutable_regulatory_trail",
            ("ledger_event_log", "audit_proof"),
            ("/ledger-events", "/audit-proofs"),
            ("LedgerEventAppended", "AuditProofGenerated"),
            ("hash_chained_mutations", "cryptographic_timestamp", "tamper_evidence_gate"),
        ),
        capability(
            "compliance_governance",
            "automated_control_testing",
            ("control_assertion", "policy_decision"),
            ("/control-tests",),
            ("RegulatoryRuleCompiled",),
            ("continuous_control_assertions", "real_time_effectiveness_report", "control_failure_route"),
        ),
        capability(
            "integration_ecosystem",
            "universal_api_contract",
            ("ledger_event_log", "ledger_projection"),
            ("/ledger-events", "/temporal-ledger"),
            ("LedgerEventAppended", "LedgerProjectionRebuilt"),
            ("graphql_query_shape", "asyncapi_event_shape", "schema_federation_boundary"),
        ),
        capability(
            "integration_ecosystem",
            "cross_system_ledger_federation",
            ("ledger_federation_link", "ledger_projection"),
            ("/ledger-federation-links", "/temporal-ledger"),
            ("LedgerProjectionRebuilt",),
            ("virtual_ledger_view", "external_ledger_mapping", "unified_query_plan"),
        ),
        capability(
            "integration_ecosystem",
            "event_driven_subledger_synchronization",
            ("ledger_event_log", "ledger_federation_link"),
            ("/ledger-events",),
            ("LedgerEventAppended", "JournalPosted"),
            ("cdc_contract", "exactly_once_idempotency", "downstream_projection_checkpoint"),
        ),
        capability(
            "integration_ecosystem",
            "decentralized_identity_integration",
            ("identity_credential", "policy_decision"),
            ("/journals",),
            ("JournalPosted",),
            ("did_counterparty_binding", "verifiable_credential_check", "signed_inter_entity_transaction"),
        ),
        capability(
            "operational_resilience",
            "chaos_engineered_fault_tolerance",
            ("resilience_drill", "consensus_replica"),
            ("/resilience-drills", "/consensus-commits"),
            ("ConsensusCommitted",),
            ("fault_injection_schedule", "consensus_reconfiguration_plan", "graceful_degradation_mode"),
        ),
        capability(
            "operational_resilience",
            "quantum_resistant_cryptography",
            ("crypto_key_epoch", "audit_proof"),
            ("/audit-proofs",),
            ("AuditProofGenerated",),
            ("post_quantum_signature_profile", "crypto_agility_epoch", "key_rotation_evidence"),
        ),
        capability(
            "operational_resilience",
            "carbon_aware_processing",
            ("carbon_execution_window", "ledger_event_log"),
            ("/carbon-execution-windows",),
            ("LedgerEventAppended",),
            ("renewable_window_scheduler", "emissions_metadata", "carbon_policy_override_log"),
        ),
        capability(
            "theoretical_constructs",
            "temporal_accounting_algebra",
            ("ledger_event_log", "ledger_projection", "close_snapshot"),
            ("/temporal-ledger",),
            ("LedgerProjectionRebuilt",),
            ("transaction_valid_processing_time_axes", "lattice_consistency_rules", "temporal_query_laws"),
        ),
        capability(
            "theoretical_constructs",
            "homomorphic_encryption_for_consolidation",
            ("audit_proof", "crypto_key_epoch", "ledger_projection"),
            ("/audit-proofs", "/trial-balance"),
            ("AuditProofGenerated", "TrialBalanceCalculated"),
            ("encrypted_consolidation_inputs", "secure_aggregation_protocol", "entity_privacy_boundary"),
        ),
        capability(
            "theoretical_constructs",
            "game_theoretic_reconciliation",
            ("reconciliation_case", "ledger_federation_link"),
            ("/reconciliation-cases",),
            ("ReconciliationSuggested",),
            ("settlement_mechanism_design", "equilibrium_score", "dispute_resolution_strategy"),
        ),
        capability(
            "theoretical_constructs",
            "information_theoretic_auditability",
            ("audit_proof", "ledger_event_log"),
            ("/audit-proofs", "/ledger-events"),
            ("AuditProofGenerated", "LedgerEventAppended"),
            ("mutation_entropy_metric", "divergence_detection", "information_flow_baseline"),
        ),
        capability(
            "implementation_prerequisites",
            "formal_methods_ledger_invariants",
            ("ledger_event_log", "control_assertion"),
            ("/control-tests",),
            ("LedgerEventAppended",),
            ("tla_invariant_catalog", "machine_checked_balance_rules", "counterexample_trace_storage"),
        ),
        capability(
            "implementation_prerequisites",
            "distributed_systems_runtime",
            ("consensus_replica", "resilience_drill"),
            ("/consensus-commits", "/resilience-drills"),
            ("ConsensusCommitted",),
            ("consensus_test_harness", "conflict_free_projection_plan", "geo_partition_recovery_runbook"),
        ),
        capability(
            "implementation_prerequisites",
            "cryptographic_engineering",
            ("audit_proof", "crypto_key_epoch", "identity_credential"),
            ("/audit-proofs",),
            ("AuditProofGenerated",),
            ("zero_knowledge_circuit_registry", "secure_enclave_attestation", "crypto_agility_tests"),
        ),
        capability(
            "implementation_prerequisites",
            "financial_mlops",
            ("predictive_validation_run", "causal_scenario", "reconciliation_case"),
            ("/predictive-validations", "/causal-scenarios", "/reconciliation-cases"),
            ("PostingValidationPredicted", "ReconciliationSuggested"),
            ("regulated_model_registry", "feature_lineage", "drift_and_materiality_monitoring"),
        ),
    )
    areas = tuple(dict.fromkeys(item["area"] for item in capabilities))
    generated_text = repr(capabilities).lower()
    legacy_product_references = tuple(
        term
        for term in ("sap", "s4hana", "salesforce", "quickbooks")
        if re.search(rf"(?<![a-z0-9_]){term}(?![a-z0-9_])", generated_text)
    )
    checks = (
        {
            "id": "all_required_areas",
            "ok": set(PBC_ADVANCED_DOMAIN_REQUIRED_AREAS) <= set(areas),
        },
        {
            "id": "all_required_capabilities",
            "ok": set(GL_CORE_ADVANCED_CAPABILITY_KEYS) <= {item["capability"] for item in capabilities},
        },
        {
            "id": "owned_table_evidence",
            "ok": all(item["owned_tables"] for item in capabilities),
        },
        {
            "id": "api_or_event_evidence",
            "ok": all(item["apis"] or item["events"] for item in capabilities),
        },
        {
            "id": "release_gate_per_capability",
            "ok": all(item["release_gate"].startswith("gl_core.") for item in capabilities),
        },
        {
            "id": "no_legacy_product_references",
            "ok": not legacy_product_references,
        },
    )
    return {
        "format": "appgen.gl-core-advanced-ledger-blueprint.v1",
        "ok": all(check["ok"] for check in checks),
        "pbc": key,
        "depth_level": PBC_DOMAIN_DEPTH_LEVEL,
        "areas": areas,
        "required_areas": PBC_ADVANCED_DOMAIN_REQUIRED_AREAS,
        "required_capabilities": GL_CORE_ADVANCED_CAPABILITY_KEYS,
        "capabilities": capabilities,
        "architecture_principles": (
            "event_log_primary_persistence",
            "projection_derived_state",
            "temporal_queryability",
            "consensus_backed_replication",
            "schema_on_read_extension",
            "tenant_isolated_scaling_and_keys",
            "cryptographic_auditability",
            "closed_loop_financial_automation",
        ),
        "checks": checks,
        "legacy_product_references": legacy_product_references,
        "blocking_gaps": tuple(check for check in checks if not check["ok"]),
    }


def _event_contract(key: str, service: dict) -> dict:
    topic = f"pbc.{key}.events"
    inbox_topic = f"pbc.{key}.inbox"
    outbox_table = f"{key}_appgen_outbox_event"
    inbox_table = f"{key}_appgen_inbox_event"
    dead_letter_table = f"{key}_appgen_dead_letter_event"
    return {
        "contract": "appgen_event_contract",
        "runtime_profile_visibility": "read_only_platform_metadata",
        "adapter": "appgen_event_adapter",
        "topic": topic,
        "inbox_topic": inbox_topic,
        "outbox_table": outbox_table,
        "inbox_table": inbox_table,
        "dead_letter_table": dead_letter_table,
        "emitted": tuple(
            {
                "event_type": event,
                "schema": f"{key}.{_snake(event)}.emitted.v1",
                "topic": topic,
                "outbox_table": outbox_table,
                "payload_fields": ("event_id", "occurred_at", "pbc", "data"),
            }
            for event in service["emits"]
        ),
        "consumed": tuple(
            {
                "event_type": event,
                "schema": f"{key}.{_snake(event)}.consumed.v1",
                "topic": inbox_topic,
                "inbox_table": inbox_table,
                "payload_fields": ("event_id", "occurred_at", "source_pbc", "data"),
            }
            for event in service["consumes"]
        ),
        "retry_policy": {
            "name": f"{key}_default_retry",
            "max_attempts": 5,
            "backoff": "exponential",
        },
        "idempotency": {
            "key_fields": ("event_type", "event_id", "handler"),
            "storage": inbox_table,
        },
    }


def _sql_type(field: dict) -> str:
    """Return the SQL type for one contract field.

    The migration's own `sql_type` is preferred when the parser recorded one: it
    is the package's real declaration, including a width the canonical vocabulary
    drops (`DECIMAL(18, 4)`), and re-emitting it keeps the generated migration
    identical to the package's own. A field the parser never saw, or one from the
    package's schema contract, is rendered from the canonical type instead.
    """
    declared = field.get("sql_type")
    if declared:
        return declared
    field_type = field["type"]
    if field_type == "integer":
        return "INTEGER"
    if field_type == "datetime":
        return "TIMESTAMP"
    if field_type == "text":
        return "TEXT"
    if field_type == "boolean":
        return "BOOLEAN"
    if field_type == "json":
        return "JSONB"
    if field_type == "decimal":
        return "NUMERIC(18, 4)"
    return "VARCHAR(255)"


def _migration_sql(key: str, table_contracts: tuple[dict, ...], event_contract: dict) -> str:
    """Render the package's schema as one migration, in dependency order.

    Three properties matter for the SQL to apply to Postgres, and each was
    missing:

    * A table is created after every table it references. `gl_core_journal_entry`
      carries a foreign key to `gl_core_accounting_period`, which the service
      contract lists later, so declaration order alone fails with
      `relation "gl_core_accounting_period" does not exist`.
    * A composite primary key is one table-level constraint. `audit_ledger`'s
      `audit_event` keys on `(audit_id, aggregate_id)`; writing the inline
      `PRIMARY KEY` clause on both columns is `multiple primary keys for table`.
    * A foreign key needs a unique index on its target. 787 parsed foreign keys
      point at a business key the migration marks `UNIQUE` but not primary, so
      that constraint has to be re-emitted or Postgres refuses the reference.
    """
    statements = [f"CREATE SCHEMA IF NOT EXISTS {key};"]
    for table in _dependency_ordered(table_contracts):
        column_lines = []
        composite = set(table.get("composite_primary_key", ()))
        for field in table["fields"]:
            name = pbc_schema.quote_identifier(field["name"])
            line = f"  {name} {_sql_type(field)}"
            if field.get("primary_key") and field["name"] not in composite:
                line += " PRIMARY KEY"
            if field.get("required") or field.get("primary_key"):
                line += " NOT NULL"
            column_lines.append(line)
        if composite:
            members = ", ".join(
                pbc_schema.quote_identifier(name)
                for name in table.get("composite_primary_key", ())
            )
            column_lines.append(f"  PRIMARY KEY ({members})")
        for unique in table.get("unique", ()):
            members = ", ".join(pbc_schema.quote_identifier(name) for name in unique)
            column_lines.append(f"  UNIQUE ({members})")
        # A column declared `... UNIQUE` inline is the same constraint written
        # differently, and a foreign key may target it (`service_ticketing`'s
        # `ticket_id`). The parser records it per field, so it is lifted to a
        # table-level constraint here unless it is already covered.
        covered = {tuple(unique) for unique in table.get("unique", ())}
        covered |= {(name,) for name in table.get("composite_primary_key", ())}
        for field in table["fields"]:
            if field.get("unique") and (field["name"],) not in covered:
                column_lines.append(f"  UNIQUE ({pbc_schema.quote_identifier(field['name'])})")
        for relationship in table["relationships"]:
            column_lines.append(
                "  FOREIGN KEY "
                f"({pbc_schema.quote_identifier(relationship['field'])}) "
                f"REFERENCES {relationship['target_table']}"
                f"({pbc_schema.quote_identifier(relationship['target_column'])})"
            )
        statements.append(
            f"CREATE TABLE {table['owned_table']} (\n"
            + ",\n".join(column_lines)
            + "\n);"
        )
    emitted = {table["owned_table"] for table in table_contracts}
    for table_name in (
        event_contract["outbox_table"],
        event_contract["inbox_table"],
        event_contract["dead_letter_table"],
    ):
        # Some packages list the event trio in their own service contract, so it
        # arrives here as a parsed table with the package's real columns. Emitting
        # the generic form as well is `relation already exists`.
        if table_name in emitted:
            continue
        statements.append(
            f"CREATE TABLE {table_name} (\n"
            "  id INTEGER PRIMARY KEY,\n"
            "  event_id VARCHAR(255) NOT NULL,\n"
            "  event_type VARCHAR(255) NOT NULL,\n"
            "  payload TEXT NOT NULL,\n"
            "  attempts INTEGER NOT NULL,\n"
            "  status VARCHAR(255) NOT NULL,\n"
            "  created_at TIMESTAMP NOT NULL,\n"
            "  processed_at TIMESTAMP\n"
            ");"
        )
    return "\n\n".join(statements)


def _dependency_ordered(table_contracts: tuple[dict, ...]) -> tuple[dict, ...]:
    """Order table contracts so every referenced table precedes its referrer.

    A package's service contract lists tables in domain order, not dependency
    order, so a foreign key can point forward. Only relationships whose target is
    one of the emitted tables create an edge; a self-reference is ignored because
    the table is created before its own constraint is added. A cycle, which a
    schema with mutually-referencing tables can have, is emitted in declaration
    order rather than dropped, and the constraint fails loudly at apply time
    instead of a table vanishing from the migration.
    """
    by_name = {table["owned_table"]: table for table in table_contracts}
    edges = {
        name: {
            relationship["target_table"]
            for relationship in table["relationships"]
            if relationship["target_table"] in by_name and relationship["target_table"] != name
        }
        for name, table in by_name.items()
    }
    ordered: list[dict] = []
    placed: set[str] = set()
    while len(ordered) < len(by_name):
        progressed = False
        for table in table_contracts:
            name = table["owned_table"]
            if name in placed or edges[name] - placed:
                continue
            ordered.append(table)
            placed.add(name)
            progressed = True
        if not progressed:
            ordered.extend(table for table in table_contracts if table["owned_table"] not in placed)
            break
    return tuple(ordered)


def _selection_terms(key: str, pbc: dict) -> tuple[str, ...]:
    terms = set(key.split("_"))
    terms.update(word.lower() for word in re.findall(r"[A-Za-z]+", pbc["label"]) if len(word) > 2)
    terms.update(
        word.lower()
        for table in _pbc_descriptor(key, pbc)["tables"]
        for word in table.split("_")
        if len(word) > 2
    )
    aliases = {
        "gl_core": ("gl", "ledger"),
        "ap_automation": ("ap", "payable", "vendor"),
        "ar_credit": ("ar", "receivable", "credit"),
        "inventory_positioning": ("inventory", "stock"),
        "personnel_identity": ("people", "hr", "employee"),
        "dom": ("order", "orders", "fulfillment"),
    }
    terms.update(aliases.get(key, ()))
    return tuple(sorted(terms))


def _app_name_from_prompt(prompt: str) -> str:
    match = re.search(r"\b(?:app|application|system)\s+(?P<name>[A-Za-z][A-Za-z0-9_]*)", prompt, re.I)
    if not match:
        return "ComposableEnterprise"
    raw = match.group("name")
    return raw[:1].upper() + raw[1:]


# PBC-owned executable implementations live under src/pyAppGen/pbcs/<pbc_key>/.
# These imports keep the historical pyAppGen.pbc API while implementation stays
# inside the owning PBC package directory.
from .pbcs.gl_core import GL_CORE_STANDARD_FEATURE_KEYS  # noqa: E402,F401
from .pbcs.gl_core import GL_CORE_UI_FRAGMENT_KEYS  # noqa: E402,F401
from .pbcs.gl_core import gl_core_append_ledger_event  # noqa: E402,F401
from .pbcs.gl_core import gl_core_build_federated_view  # noqa: E402,F401
from .pbcs.gl_core import gl_core_build_projection  # noqa: E402,F401
from .pbcs.gl_core import gl_core_build_workbench_view  # noqa: E402,F401
from .pbcs.gl_core import gl_core_chart_governance_contract  # noqa: E402,F401
from .pbcs.gl_core import gl_core_compile_regulatory_rules  # noqa: E402,F401
from .pbcs.gl_core import gl_core_configure_runtime  # noqa: E402,F401
from .pbcs.gl_core import gl_core_consolidate_private_balances  # noqa: E402,F401
from .pbcs.gl_core import gl_core_create_continuous_close_snapshot  # noqa: E402,F401
from .pbcs.gl_core import gl_core_derive_account_from_semantics  # noqa: E402,F401
from .pbcs.gl_core import gl_core_empty_state  # noqa: E402,F401
from .pbcs.gl_core import gl_core_evaluate_policy  # noqa: E402,F401
from .pbcs.gl_core import gl_core_generate_audit_proof  # noqa: E402,F401
from .pbcs.gl_core import gl_core_measure_information_auditability  # noqa: E402,F401
from .pbcs.gl_core import gl_core_open_accounting_period  # noqa: E402,F401
from .pbcs.gl_core import gl_core_predict_posting_validation  # noqa: E402,F401
from .pbcs.gl_core import gl_core_query_temporal_ledger  # noqa: E402,F401
from .pbcs.gl_core import gl_core_register_account  # noqa: E402,F401
from .pbcs.gl_core import gl_core_register_financial_model  # noqa: E402,F401
from .pbcs.gl_core import gl_core_register_journal  # noqa: E402,F401
from .pbcs.gl_core import gl_core_register_rule  # noqa: E402,F401
from .pbcs.gl_core import gl_core_register_schema_extension  # noqa: E402,F401
from .pbcs.gl_core import gl_core_replicate_consensus  # noqa: E402,F401
from .pbcs.gl_core import gl_core_resolve_reconciliation_game  # noqa: E402,F401
from .pbcs.gl_core import gl_core_rotate_crypto_epoch  # noqa: E402,F401
from .pbcs.gl_core import gl_core_run_causal_scenario  # noqa: E402,F401
from .pbcs.gl_core import gl_core_run_control_tests  # noqa: E402,F401
from .pbcs.gl_core import gl_core_run_resilience_drill  # noqa: E402,F401
from .pbcs.gl_core import GL_CORE_ALLOWED_DATABASE_BACKENDS  # noqa: E402,F401
from .pbcs.gl_core import GL_CORE_CONSUMED_EVENT_TYPES  # noqa: E402,F401
from .pbcs.gl_core import GL_CORE_EMITTED_EVENT_TYPES  # noqa: E402,F401
from .pbcs.gl_core import GL_CORE_OWNED_TABLES  # noqa: E402,F401
from .pbcs.gl_core import GL_CORE_REQUIRED_EVENT_TOPIC  # noqa: E402,F401
from .pbcs.gl_core import gl_core_build_api_contract  # noqa: E402,F401
from .pbcs.gl_core import gl_core_build_release_evidence  # noqa: E402,F401
from .pbcs.gl_core import gl_core_build_schema_contract  # noqa: E402,F401
from .pbcs.gl_core import gl_core_build_service_contract  # noqa: E402,F401
from .pbcs.gl_core import gl_core_permissions_contract  # noqa: E402,F401
from .pbcs.gl_core import gl_core_receive_event  # noqa: E402,F401
from .pbcs.gl_core import gl_core_runtime_capabilities  # noqa: E402,F401
from .pbcs.gl_core import gl_core_runtime_smoke  # noqa: E402,F401
from .pbcs.gl_core import gl_core_schedule_carbon_aware_execution  # noqa: E402,F401
from .pbcs.gl_core import gl_core_set_parameter  # noqa: E402,F401
from .pbcs.gl_core import gl_core_simulate_probabilistic_posting  # noqa: E402,F401
from .pbcs.gl_core import gl_core_suggest_reconciliation  # noqa: E402,F401
from .pbcs.gl_core import gl_core_transition_account_state  # noqa: E402,F401
from .pbcs.gl_core import gl_core_transition_journal_state  # noqa: E402,F401
from .pbcs.gl_core import gl_core_transition_period_state  # noqa: E402,F401
from .pbcs.gl_core import gl_core_verify_journal_invariants  # noqa: E402,F401
from .pbcs.gl_core import gl_core_render_workbench  # noqa: E402,F401
from .pbcs.gl_core import gl_core_ui_contract  # noqa: E402,F401
from .pbcs.gl_core import gl_core_verify_formal_invariants  # noqa: E402,F401
from .pbcs.gl_core import gl_core_verify_identity_credential  # noqa: E402,F401
from .pbcs.gl_core import gl_core_verify_owned_table_boundary  # noqa: E402,F401
from .pbcs.ap_automation import AP_AUTOMATION_ALLOWED_DATABASE_BACKENDS  # noqa: E402,F401
from .pbcs.ap_automation import AP_AUTOMATION_CONSUMED_EVENT_TYPES  # noqa: E402,F401
from .pbcs.ap_automation import AP_AUTOMATION_EMITTED_EVENT_TYPES  # noqa: E402,F401
from .pbcs.ap_automation import AP_AUTOMATION_OWNED_TABLES  # noqa: E402,F401
from .pbcs.ap_automation import AP_AUTOMATION_REQUIRED_EVENT_TOPIC  # noqa: E402,F401
from .pbcs.ap_automation import AP_AUTOMATION_STANDARD_FEATURE_KEYS  # noqa: E402,F401
from .pbcs.ap_automation import AP_AUTOMATION_RUNTIME_CAPABILITY_KEYS  # noqa: E402,F401
from .pbcs.ap_automation import AP_AUTOMATION_UI_FRAGMENT_KEYS  # noqa: E402,F401
from .pbcs.ap_automation import ap_automation_align_contract_terms  # noqa: E402,F401
from .pbcs.ap_automation import ap_automation_analyze_discount_counterfactual  # noqa: E402,F401
from .pbcs.ap_automation import ap_automation_build_api_contract  # noqa: E402,F401
from .pbcs.ap_automation import ap_automation_build_release_evidence  # noqa: E402,F401
from .pbcs.ap_automation import ap_automation_build_schema_contract  # noqa: E402,F401
from .pbcs.ap_automation import ap_automation_build_service_contract  # noqa: E402,F401
from .pbcs.ap_automation import ap_automation_build_workbench_view  # noqa: E402,F401
from .pbcs.ap_automation import ap_automation_capture_invoice  # noqa: E402,F401
from .pbcs.ap_automation import ap_automation_configure_runtime  # noqa: E402,F401
from .pbcs.ap_automation import ap_automation_empty_state  # noqa: E402,F401
from .pbcs.ap_automation import ap_automation_execute_payment  # noqa: E402,F401
from .pbcs.ap_automation import ap_automation_issue_purchase_order  # noqa: E402,F401
from .pbcs.ap_automation import ap_automation_match_invoice  # noqa: E402,F401
from .pbcs.ap_automation import ap_automation_onboard_vendor  # noqa: E402,F401
from .pbcs.ap_automation import ap_automation_record_goods_receipt  # noqa: E402,F401
from .pbcs.ap_automation import ap_automation_permissions_contract  # noqa: E402,F401
from .pbcs.ap_automation import ap_automation_receive_event  # noqa: E402,F401
from .pbcs.ap_automation import ap_automation_register_rule  # noqa: E402,F401
from .pbcs.ap_automation import ap_automation_register_schema_extension  # noqa: E402,F401
from .pbcs.ap_automation import ap_automation_render_workbench  # noqa: E402,F401
from .pbcs.ap_automation import ap_automation_runtime_capabilities  # noqa: E402,F401
from .pbcs.ap_automation import ap_automation_runtime_smoke  # noqa: E402,F401
from .pbcs.ap_automation import ap_automation_schedule_payments  # noqa: E402,F401
from .pbcs.ap_automation import ap_automation_set_parameter  # noqa: E402,F401
from .pbcs.ap_automation import ap_automation_ui_contract  # noqa: E402,F401
from .pbcs.ap_automation import ap_automation_verify_owned_table_boundary  # noqa: E402,F401
from .pbcs.ar_credit import AR_CREDIT_ALLOWED_DATABASE_BACKENDS  # noqa: E402,F401
from .pbcs.ar_credit import AR_CREDIT_APPROVER_AUTHORITY  # noqa: E402,F401
from .pbcs.ar_credit import AR_CREDIT_CONSUMED_EVENT_TYPES  # noqa: E402,F401
from .pbcs.ar_credit import AR_CREDIT_CREDIT_DECISIONS  # noqa: E402,F401
from .pbcs.ar_credit import AR_CREDIT_EMITTED_EVENT_TYPES  # noqa: E402,F401
from .pbcs.ar_credit import AR_CREDIT_INVOICE_LIFECYCLE_TRANSITIONS  # noqa: E402,F401
from .pbcs.ar_credit import AR_CREDIT_INVOICE_SEALED_STATES  # noqa: E402,F401
from .pbcs.ar_credit import AR_CREDIT_INVOICE_TERMINAL_STATES  # noqa: E402,F401
from .pbcs.ar_credit import AR_CREDIT_OWNED_TABLES  # noqa: E402,F401
from .pbcs.ar_credit import AR_CREDIT_REQUIRED_EVENT_TOPIC  # noqa: E402,F401
from .pbcs.ar_credit import AR_CREDIT_STANDARD_FEATURE_KEYS  # noqa: E402,F401
from .pbcs.ar_credit import AR_CREDIT_RUNTIME_CAPABILITY_KEYS  # noqa: E402,F401
from .pbcs.ar_credit import AR_CREDIT_UI_FRAGMENT_KEYS  # noqa: E402,F401
from .pbcs.ar_credit import ar_credit_apply_cash  # noqa: E402,F401
from .pbcs.ar_credit import ar_credit_build_api_contract  # noqa: E402,F401
from .pbcs.ar_credit import ar_credit_build_release_evidence  # noqa: E402,F401
from .pbcs.ar_credit import ar_credit_build_schema_contract  # noqa: E402,F401
from .pbcs.ar_credit import ar_credit_build_service_contract  # noqa: E402,F401
from .pbcs.ar_credit import ar_credit_build_workbench_view  # noqa: E402,F401
from .pbcs.ar_credit import ar_credit_calculate_aging  # noqa: E402,F401
from .pbcs.ar_credit import ar_credit_configure_runtime  # noqa: E402,F401
from .pbcs.ar_credit import ar_credit_create_credit_memo  # noqa: E402,F401
from .pbcs.ar_credit import ar_credit_create_dunning_plan  # noqa: E402,F401
from .pbcs.ar_credit import ar_credit_customer_exposure  # noqa: E402,F401
from .pbcs.ar_credit import ar_credit_empty_state  # noqa: E402,F401
from .pbcs.ar_credit import ar_credit_generate_customer_statement  # noqa: E402,F401
from .pbcs.ar_credit import ar_credit_issue_invoice  # noqa: E402,F401
from .pbcs.ar_credit import ar_credit_issue_refund  # noqa: E402,F401
from .pbcs.ar_credit import ar_credit_invoice_correction_contract  # noqa: E402,F401
from .pbcs.ar_credit import ar_credit_onboard_customer  # noqa: E402,F401
from .pbcs.ar_credit import ar_credit_parse_remittance  # noqa: E402,F401
from .pbcs.ar_credit import ar_credit_permissions_contract  # noqa: E402,F401
from .pbcs.ar_credit import ar_credit_record_delivery_confirmation  # noqa: E402,F401
from .pbcs.ar_credit import ar_credit_record_credit_decision  # noqa: E402,F401
from .pbcs.ar_credit import ar_credit_record_unapplied_cash  # noqa: E402,F401
from .pbcs.ar_credit import ar_credit_receive_event  # noqa: E402,F401
from .pbcs.ar_credit import ar_credit_recognize_revenue_schedule  # noqa: E402,F401
from .pbcs.ar_credit import ar_credit_register_rule  # noqa: E402,F401
from .pbcs.ar_credit import ar_credit_register_schema_extension  # noqa: E402,F401
from .pbcs.ar_credit import ar_credit_render_workbench  # noqa: E402,F401
from .pbcs.ar_credit import ar_credit_runtime_capabilities  # noqa: E402,F401
from .pbcs.ar_credit import ar_credit_runtime_smoke  # noqa: E402,F401
from .pbcs.ar_credit import ar_credit_schedule_collection_action  # noqa: E402,F401
from .pbcs.ar_credit import ar_credit_set_parameter  # noqa: E402,F401
from .pbcs.ar_credit import ar_credit_transition_invoice_state  # noqa: E402,F401
from .pbcs.ar_credit import ar_credit_ui_contract  # noqa: E402,F401
from .pbcs.ar_credit import ar_credit_verify_owned_table_boundary  # noqa: E402,F401
from .pbcs.ar_credit import ar_credit_write_off_receivable  # noqa: E402,F401
from .pbcs.treasury_cash import TREASURY_CASH_ALLOWED_DATABASE_BACKENDS  # noqa: E402,F401
from .pbcs.treasury_cash import TREASURY_CASH_CONSUMED_EVENT_TYPES  # noqa: E402,F401
from .pbcs.treasury_cash import TREASURY_CASH_EMITTED_EVENT_TYPES  # noqa: E402,F401
from .pbcs.treasury_cash import TREASURY_CASH_OWNED_TABLES  # noqa: E402,F401
from .pbcs.treasury_cash import TREASURY_CASH_REQUIRED_EVENT_TOPIC  # noqa: E402,F401
from .pbcs.treasury_cash import TREASURY_CASH_RUNTIME_CAPABILITY_KEYS  # noqa: E402,F401
from .pbcs.treasury_cash import TREASURY_CASH_STANDARD_FEATURE_KEYS  # noqa: E402,F401
from .pbcs.treasury_cash import TREASURY_CASH_UI_FRAGMENT_KEYS  # noqa: E402,F401
from .pbcs.treasury_cash import treasury_cash_build_api_contract  # noqa: E402,F401
from .pbcs.treasury_cash import treasury_cash_build_cash_position  # noqa: E402,F401
from .pbcs.treasury_cash import treasury_cash_build_release_evidence  # noqa: E402,F401
from .pbcs.treasury_cash import treasury_cash_build_schema_contract  # noqa: E402,F401
from .pbcs.treasury_cash import treasury_cash_build_service_contract  # noqa: E402,F401
from .pbcs.treasury_cash import treasury_cash_build_workbench_view  # noqa: E402,F401
from .pbcs.treasury_cash import treasury_cash_capture_bank_balance  # noqa: E402,F401
from .pbcs.treasury_cash import treasury_cash_configure_runtime  # noqa: E402,F401
from .pbcs.treasury_cash import treasury_cash_empty_state  # noqa: E402,F401
from .pbcs.treasury_cash import treasury_cash_forecast_cash  # noqa: E402,F401
from .pbcs.treasury_cash import treasury_cash_ingest_bank_statement  # noqa: E402,F401
from .pbcs.treasury_cash import treasury_cash_optimize_liquidity  # noqa: E402,F401
from .pbcs.treasury_cash import treasury_cash_permissions_contract  # noqa: E402,F401
from .pbcs.treasury_cash import treasury_cash_receive_event  # noqa: E402,F401
from .pbcs.treasury_cash import treasury_cash_reconcile_statement  # noqa: E402,F401
from .pbcs.treasury_cash import treasury_cash_register_bank_account  # noqa: E402,F401
from .pbcs.treasury_cash import treasury_cash_register_rule  # noqa: E402,F401
from .pbcs.treasury_cash import treasury_cash_register_schema_extension  # noqa: E402,F401
from .pbcs.treasury_cash import treasury_cash_render_workbench  # noqa: E402,F401
from .pbcs.treasury_cash import treasury_cash_runtime_capabilities  # noqa: E402,F401
from .pbcs.treasury_cash import treasury_cash_runtime_smoke  # noqa: E402,F401
from .pbcs.treasury_cash import treasury_cash_set_parameter  # noqa: E402,F401
from .pbcs.treasury_cash import treasury_cash_ui_contract  # noqa: E402,F401
from .pbcs.treasury_cash import treasury_cash_verify_owned_table_boundary  # noqa: E402,F401
from .pbcs.asset_lifecycle import ASSET_LIFECYCLE_ALLOWED_DATABASE_BACKENDS  # noqa: E402,F401
from .pbcs.asset_lifecycle import ASSET_LIFECYCLE_CONSUMED_EVENT_TYPES  # noqa: E402,F401
from .pbcs.asset_lifecycle import ASSET_LIFECYCLE_EMITTED_EVENT_TYPES  # noqa: E402,F401
from .pbcs.asset_lifecycle import ASSET_LIFECYCLE_OWNED_TABLES  # noqa: E402,F401
from .pbcs.asset_lifecycle import ASSET_LIFECYCLE_REQUIRED_EVENT_TOPIC  # noqa: E402,F401
from .pbcs.asset_lifecycle import ASSET_LIFECYCLE_RUNTIME_CAPABILITY_KEYS  # noqa: E402,F401
from .pbcs.asset_lifecycle import ASSET_LIFECYCLE_STANDARD_FEATURE_KEYS  # noqa: E402,F401
from .pbcs.asset_lifecycle import ASSET_LIFECYCLE_UI_FRAGMENT_KEYS  # noqa: E402,F401
from .pbcs.asset_lifecycle import asset_lifecycle_build_api_contract  # noqa: E402,F401
from .pbcs.asset_lifecycle import asset_lifecycle_build_depreciation_schedule  # noqa: E402,F401
from .pbcs.asset_lifecycle import asset_lifecycle_build_release_evidence  # noqa: E402,F401
from .pbcs.asset_lifecycle import asset_lifecycle_build_schema_contract  # noqa: E402,F401
from .pbcs.asset_lifecycle import asset_lifecycle_build_service_contract  # noqa: E402,F401
from .pbcs.asset_lifecycle import asset_lifecycle_build_workbench_view  # noqa: E402,F401
from .pbcs.asset_lifecycle import asset_lifecycle_configure_runtime  # noqa: E402,F401
from .pbcs.asset_lifecycle import asset_lifecycle_empty_state  # noqa: E402,F401
from .pbcs.asset_lifecycle import asset_lifecycle_place_asset_in_service  # noqa: E402,F401
from .pbcs.asset_lifecycle import asset_lifecycle_permissions_contract  # noqa: E402,F401
from .pbcs.asset_lifecycle import asset_lifecycle_receive_event  # noqa: E402,F401
from .pbcs.asset_lifecycle import asset_lifecycle_register_asset  # noqa: E402,F401
from .pbcs.asset_lifecycle import asset_lifecycle_register_rule  # noqa: E402,F401
from .pbcs.asset_lifecycle import asset_lifecycle_register_schema_extension  # noqa: E402,F401
from .pbcs.asset_lifecycle import asset_lifecycle_render_workbench  # noqa: E402,F401
from .pbcs.asset_lifecycle import asset_lifecycle_retire_asset  # noqa: E402,F401
from .pbcs.asset_lifecycle import asset_lifecycle_run_depreciation  # noqa: E402,F401
from .pbcs.asset_lifecycle import asset_lifecycle_runtime_capabilities  # noqa: E402,F401
from .pbcs.asset_lifecycle import asset_lifecycle_runtime_smoke  # noqa: E402,F401
from .pbcs.asset_lifecycle import asset_lifecycle_set_parameter  # noqa: E402,F401
from .pbcs.asset_lifecycle import asset_lifecycle_transfer_asset  # noqa: E402,F401
from .pbcs.asset_lifecycle import asset_lifecycle_ui_contract  # noqa: E402,F401
from .pbcs.asset_lifecycle import asset_lifecycle_verify_owned_table_boundary  # noqa: E402,F401
from .pbcs.tax_localization import TAX_LOCALIZATION_ALLOWED_DATABASE_BACKENDS  # noqa: E402,F401
from .pbcs.tax_localization import TAX_LOCALIZATION_CONSUMED_EVENT_TYPES  # noqa: E402,F401
from .pbcs.tax_localization import TAX_LOCALIZATION_EMITTED_EVENT_TYPES  # noqa: E402,F401
from .pbcs.tax_localization import TAX_LOCALIZATION_OWNED_TABLES  # noqa: E402,F401
from .pbcs.tax_localization import TAX_LOCALIZATION_REQUIRED_EVENT_TOPIC  # noqa: E402,F401
from .pbcs.tax_localization import TAX_LOCALIZATION_RUNTIME_CAPABILITY_KEYS  # noqa: E402,F401
from .pbcs.tax_localization import TAX_LOCALIZATION_STANDARD_FEATURE_KEYS  # noqa: E402,F401
from .pbcs.tax_localization import TAX_LOCALIZATION_UI_FRAGMENT_KEYS  # noqa: E402,F401
from .pbcs.tax_localization import tax_localization_build_api_contract  # noqa: E402,F401
from .pbcs.tax_localization import tax_localization_build_release_evidence  # noqa: E402,F401
from .pbcs.tax_localization import tax_localization_build_schema_contract  # noqa: E402,F401
from .pbcs.tax_localization import tax_localization_build_service_contract  # noqa: E402,F401
from .pbcs.tax_localization import tax_localization_build_workbench_view  # noqa: E402,F401
from .pbcs.tax_localization import tax_localization_calculate_tax_quote  # noqa: E402,F401
from .pbcs.tax_localization import tax_localization_classify_product  # noqa: E402,F401
from .pbcs.tax_localization import tax_localization_configure_runtime  # noqa: E402,F401
from .pbcs.tax_localization import tax_localization_empty_state  # noqa: E402,F401
from .pbcs.tax_localization import tax_localization_permissions_contract  # noqa: E402,F401
from .pbcs.tax_localization import tax_localization_prepare_tax_filing  # noqa: E402,F401
from .pbcs.tax_localization import tax_localization_receive_event  # noqa: E402,F401
from .pbcs.tax_localization import tax_localization_record_invoice_tax  # noqa: E402,F401
from .pbcs.tax_localization import tax_localization_register_jurisdiction  # noqa: E402,F401
from .pbcs.tax_localization import tax_localization_register_rule  # noqa: E402,F401
from .pbcs.tax_localization import tax_localization_register_schema_extension  # noqa: E402,F401
from .pbcs.tax_localization import tax_localization_render_workbench  # noqa: E402,F401
from .pbcs.tax_localization import tax_localization_register_tax_rule  # noqa: E402,F401
from .pbcs.tax_localization import tax_localization_runtime_capabilities  # noqa: E402,F401
from .pbcs.tax_localization import tax_localization_runtime_smoke  # noqa: E402,F401
from .pbcs.tax_localization import tax_localization_set_parameter  # noqa: E402,F401
from .pbcs.tax_localization import tax_localization_ui_contract  # noqa: E402,F401
from .pbcs.tax_localization import tax_localization_validate_exemption_certificate  # noqa: E402,F401
from .pbcs.tax_localization import tax_localization_verify_owned_table_boundary  # noqa: E402,F401
from .pbcs.inventory_positioning import INVENTORY_POSITIONING_ALLOWED_DATABASE_BACKENDS  # noqa: E402,F401
from .pbcs.inventory_positioning import INVENTORY_POSITIONING_CONSUMED_EVENT_TYPES  # noqa: E402,F401
from .pbcs.inventory_positioning import INVENTORY_POSITIONING_EMITTED_EVENT_TYPES  # noqa: E402,F401
from .pbcs.inventory_positioning import INVENTORY_POSITIONING_OWNED_TABLES  # noqa: E402,F401
from .pbcs.inventory_positioning import INVENTORY_POSITIONING_REQUIRED_EVENT_TOPIC  # noqa: E402,F401
from .pbcs.inventory_positioning import INVENTORY_POSITIONING_RUNTIME_CAPABILITY_KEYS  # noqa: E402,F401
from .pbcs.inventory_positioning import INVENTORY_POSITIONING_STANDARD_FEATURE_KEYS  # noqa: E402,F401
from .pbcs.inventory_positioning import INVENTORY_POSITIONING_UI_FRAGMENT_KEYS  # noqa: E402,F401
from .pbcs.inventory_positioning import inventory_positioning_allocate_inventory  # noqa: E402,F401
from .pbcs.inventory_positioning import inventory_positioning_build_api_contract  # noqa: E402,F401
from .pbcs.inventory_positioning import inventory_positioning_build_release_evidence  # noqa: E402,F401
from .pbcs.inventory_positioning import inventory_positioning_build_schema_contract  # noqa: E402,F401
from .pbcs.inventory_positioning import inventory_positioning_build_service_contract  # noqa: E402,F401
from .pbcs.inventory_positioning import inventory_positioning_build_workbench_view  # noqa: E402,F401
from .pbcs.inventory_positioning import inventory_positioning_calculate_availability  # noqa: E402,F401
from .pbcs.inventory_positioning import inventory_positioning_configure_runtime  # noqa: E402,F401
from .pbcs.inventory_positioning import inventory_positioning_empty_state  # noqa: E402,F401
from .pbcs.inventory_positioning import inventory_positioning_permissions_contract  # noqa: E402,F401
from .pbcs.inventory_positioning import inventory_positioning_post_goods_receipt  # noqa: E402,F401
from .pbcs.inventory_positioning import inventory_positioning_receive_event  # noqa: E402,F401
from .pbcs.inventory_positioning import inventory_positioning_release_allocation  # noqa: E402,F401
from .pbcs.inventory_positioning import inventory_positioning_register_item  # noqa: E402,F401
from .pbcs.inventory_positioning import inventory_positioning_register_node  # noqa: E402,F401
from .pbcs.inventory_positioning import inventory_positioning_register_rule  # noqa: E402,F401
from .pbcs.inventory_positioning import inventory_positioning_register_schema_extension  # noqa: E402,F401
from .pbcs.inventory_positioning import inventory_positioning_render_workbench  # noqa: E402,F401
from .pbcs.inventory_positioning import inventory_positioning_runtime_capabilities  # noqa: E402,F401
from .pbcs.inventory_positioning import inventory_positioning_runtime_smoke  # noqa: E402,F401
from .pbcs.inventory_positioning import inventory_positioning_set_parameter  # noqa: E402,F401
from .pbcs.inventory_positioning import inventory_positioning_ui_contract  # noqa: E402,F401
from .pbcs.inventory_positioning import inventory_positioning_verify_owned_table_boundary  # noqa: E402,F401
from .pbcs.wms_core import WMS_CORE_ALLOWED_DATABASE_BACKENDS  # noqa: E402,F401
from .pbcs.wms_core import WMS_CORE_CONSUMED_EVENT_TYPES  # noqa: E402,F401
from .pbcs.wms_core import WMS_CORE_EMITTED_EVENT_TYPES  # noqa: E402,F401
from .pbcs.wms_core import WMS_CORE_OWNED_TABLES  # noqa: E402,F401
from .pbcs.wms_core import WMS_CORE_REQUIRED_EVENT_TOPIC  # noqa: E402,F401
from .pbcs.wms_core import WMS_CORE_RUNTIME_CAPABILITY_KEYS  # noqa: E402,F401
from .pbcs.wms_core import WMS_CORE_STANDARD_FEATURE_KEYS  # noqa: E402,F401
from .pbcs.wms_core import WMS_CORE_UI_FRAGMENT_KEYS  # noqa: E402,F401
from .pbcs.wms_core import wms_core_build_api_contract  # noqa: E402,F401
from .pbcs.wms_core import wms_core_build_release_evidence  # noqa: E402,F401
from .pbcs.wms_core import wms_core_build_schema_contract  # noqa: E402,F401
from .pbcs.wms_core import wms_core_build_service_contract  # noqa: E402,F401
from .pbcs.wms_core import wms_core_build_workbench_view  # noqa: E402,F401
from .pbcs.wms_core import wms_core_configure_runtime  # noqa: E402,F401
from .pbcs.wms_core import wms_core_confirm_pack  # noqa: E402,F401
from .pbcs.wms_core import wms_core_confirm_putaway  # noqa: E402,F401
from .pbcs.wms_core import wms_core_confirm_shipment  # noqa: E402,F401
from .pbcs.wms_core import wms_core_create_pack_task  # noqa: E402,F401
from .pbcs.wms_core import wms_core_create_pick_wave  # noqa: E402,F401
from .pbcs.wms_core import wms_core_create_putaway_task  # noqa: E402,F401
from .pbcs.wms_core import wms_core_empty_state  # noqa: E402,F401
from .pbcs.wms_core import wms_core_execute_pick  # noqa: E402,F401
from .pbcs.wms_core import wms_core_receive_inbound  # noqa: E402,F401
from .pbcs.wms_core import wms_core_register_bin  # noqa: E402,F401
from .pbcs.wms_core import wms_core_permissions_contract  # noqa: E402,F401
from .pbcs.wms_core import wms_core_receive_event  # noqa: E402,F401
from .pbcs.wms_core import wms_core_register_rule  # noqa: E402,F401
from .pbcs.wms_core import wms_core_register_schema_extension  # noqa: E402,F401
from .pbcs.wms_core import wms_core_register_warehouse  # noqa: E402,F401
from .pbcs.wms_core import wms_core_render_workbench  # noqa: E402,F401
from .pbcs.wms_core import wms_core_runtime_capabilities  # noqa: E402,F401
from .pbcs.wms_core import wms_core_runtime_smoke  # noqa: E402,F401
from .pbcs.wms_core import wms_core_set_parameter  # noqa: E402,F401
from .pbcs.wms_core import wms_core_ui_contract  # noqa: E402,F401
from .pbcs.wms_core import wms_core_verify_owned_table_boundary  # noqa: E402,F401
from .pbcs.procurement_sourcing import PROCUREMENT_SOURCING_ALLOWED_DATABASE_BACKENDS  # noqa: E402,F401
from .pbcs.procurement_sourcing import PROCUREMENT_SOURCING_CONSUMED_EVENT_TYPES  # noqa: E402,F401
from .pbcs.procurement_sourcing import PROCUREMENT_SOURCING_EMITTED_EVENT_TYPES  # noqa: E402,F401
from .pbcs.procurement_sourcing import PROCUREMENT_SOURCING_OWNED_TABLES  # noqa: E402,F401
from .pbcs.procurement_sourcing import PROCUREMENT_SOURCING_REQUIRED_EVENT_TOPIC  # noqa: E402,F401
from .pbcs.procurement_sourcing import PROCUREMENT_SOURCING_RUNTIME_CAPABILITY_KEYS  # noqa: E402,F401
from .pbcs.procurement_sourcing import PROCUREMENT_SOURCING_STANDARD_FEATURE_KEYS  # noqa: E402,F401
from .pbcs.procurement_sourcing import PROCUREMENT_SOURCING_UI_FRAGMENT_KEYS  # noqa: E402,F401
from .pbcs.procurement_sourcing import procurement_sourcing_approve_requisition  # noqa: E402,F401
from .pbcs.procurement_sourcing import procurement_sourcing_build_api_contract  # noqa: E402,F401
from .pbcs.procurement_sourcing import procurement_sourcing_build_release_evidence  # noqa: E402,F401
from .pbcs.procurement_sourcing import procurement_sourcing_build_schema_contract  # noqa: E402,F401
from .pbcs.procurement_sourcing import procurement_sourcing_build_service_contract  # noqa: E402,F401
from .pbcs.procurement_sourcing import procurement_sourcing_build_workbench_view  # noqa: E402,F401
from .pbcs.procurement_sourcing import procurement_sourcing_capture_bid  # noqa: E402,F401
from .pbcs.procurement_sourcing import procurement_sourcing_configure_runtime  # noqa: E402,F401
from .pbcs.procurement_sourcing import procurement_sourcing_create_contract  # noqa: E402,F401
from .pbcs.procurement_sourcing import procurement_sourcing_create_requisition  # noqa: E402,F401
from .pbcs.procurement_sourcing import procurement_sourcing_create_rfq  # noqa: E402,F401
from .pbcs.procurement_sourcing import procurement_sourcing_empty_state  # noqa: E402,F401
from .pbcs.procurement_sourcing import procurement_sourcing_issue_purchase_order  # noqa: E402,F401
from .pbcs.procurement_sourcing import procurement_sourcing_permissions_contract  # noqa: E402,F401
from .pbcs.procurement_sourcing import procurement_sourcing_receive_event  # noqa: E402,F401
from .pbcs.procurement_sourcing import procurement_sourcing_register_rule  # noqa: E402,F401
from .pbcs.procurement_sourcing import procurement_sourcing_register_schema_extension  # noqa: E402,F401
from .pbcs.procurement_sourcing import procurement_sourcing_render_workbench  # noqa: E402,F401
from .pbcs.procurement_sourcing import procurement_sourcing_runtime_capabilities  # noqa: E402,F401
from .pbcs.procurement_sourcing import procurement_sourcing_runtime_smoke  # noqa: E402,F401
from .pbcs.procurement_sourcing import procurement_sourcing_score_suppliers  # noqa: E402,F401
from .pbcs.procurement_sourcing import procurement_sourcing_select_supplier  # noqa: E402,F401
from .pbcs.procurement_sourcing import procurement_sourcing_set_parameter  # noqa: E402,F401
from .pbcs.procurement_sourcing import procurement_sourcing_ui_contract  # noqa: E402,F401
from .pbcs.procurement_sourcing import procurement_sourcing_verify_owned_table_boundary  # noqa: E402,F401
from .pbcs.transportation_management import TRANSPORTATION_MANAGEMENT_ALLOWED_DATABASE_BACKENDS  # noqa: E402,F401
from .pbcs.transportation_management import TRANSPORTATION_MANAGEMENT_CONSUMED_EVENT_TYPES  # noqa: E402,F401
from .pbcs.transportation_management import TRANSPORTATION_MANAGEMENT_EMITTED_EVENT_TYPES  # noqa: E402,F401
from .pbcs.transportation_management import TRANSPORTATION_MANAGEMENT_OWNED_TABLES  # noqa: E402,F401
from .pbcs.transportation_management import TRANSPORTATION_MANAGEMENT_REQUIRED_EVENT_TOPIC  # noqa: E402,F401
from .pbcs.transportation_management import TRANSPORTATION_MANAGEMENT_RUNTIME_CAPABILITY_KEYS  # noqa: E402,F401
from .pbcs.transportation_management import TRANSPORTATION_MANAGEMENT_STANDARD_FEATURE_KEYS  # noqa: E402,F401
from .pbcs.transportation_management import TRANSPORTATION_MANAGEMENT_UI_FRAGMENT_KEYS  # noqa: E402,F401
from .pbcs.transportation_management import transportation_management_build_api_contract  # noqa: E402,F401
from .pbcs.transportation_management import transportation_management_build_release_evidence  # noqa: E402,F401
from .pbcs.transportation_management import transportation_management_build_schema_contract  # noqa: E402,F401
from .pbcs.transportation_management import transportation_management_build_service_contract  # noqa: E402,F401
from .pbcs.transportation_management import transportation_management_build_workbench_view  # noqa: E402,F401
from .pbcs.transportation_management import transportation_management_calculate_eta  # noqa: E402,F401
from .pbcs.transportation_management import transportation_management_configure_runtime  # noqa: E402,F401
from .pbcs.transportation_management import transportation_management_confirm_delivery  # noqa: E402,F401
from .pbcs.transportation_management import transportation_management_create_shipment  # noqa: E402,F401
from .pbcs.transportation_management import transportation_management_dispatch_shipment  # noqa: E402,F401
from .pbcs.transportation_management import transportation_management_empty_state  # noqa: E402,F401
from .pbcs.transportation_management import transportation_management_plan_route  # noqa: E402,F401
from .pbcs.transportation_management import transportation_management_record_tracking_event  # noqa: E402,F401
from .pbcs.transportation_management import transportation_management_permissions_contract  # noqa: E402,F401
from .pbcs.transportation_management import transportation_management_receive_event  # noqa: E402,F401
from .pbcs.transportation_management import transportation_management_register_carrier  # noqa: E402,F401
from .pbcs.transportation_management import transportation_management_register_rule  # noqa: E402,F401
from .pbcs.transportation_management import transportation_management_register_schema_extension  # noqa: E402,F401
from .pbcs.transportation_management import transportation_management_render_workbench  # noqa: E402,F401
from .pbcs.transportation_management import transportation_management_runtime_capabilities  # noqa: E402,F401
from .pbcs.transportation_management import transportation_management_runtime_smoke  # noqa: E402,F401
from .pbcs.transportation_management import transportation_management_select_carrier  # noqa: E402,F401
from .pbcs.transportation_management import transportation_management_set_parameter  # noqa: E402,F401
from .pbcs.transportation_management import transportation_management_ui_contract  # noqa: E402,F401
from .pbcs.transportation_management import transportation_management_verify_owned_table_boundary  # noqa: E402,F401
from .pbcs.dom import DOM_ALLOWED_DATABASE_BACKENDS  # noqa: E402,F401
from .pbcs.dom import DOM_CONSUMED_EVENT_TYPES  # noqa: E402,F401
from .pbcs.dom import DOM_EMITTED_EVENT_TYPES  # noqa: E402,F401
from .pbcs.dom import DOM_OWNED_TABLES  # noqa: E402,F401
from .pbcs.dom import DOM_REQUIRED_EVENT_TOPIC  # noqa: E402,F401
from .pbcs.dom import DOM_RUNTIME_CAPABILITY_KEYS  # noqa: E402,F401
from .pbcs.dom import DOM_STANDARD_FEATURE_KEYS  # noqa: E402,F401
from .pbcs.dom import DOM_UI_FRAGMENT_KEYS  # noqa: E402,F401
from .pbcs.dom import dom_apply_inventory_allocation  # noqa: E402,F401
from .pbcs.dom import dom_apply_tax_projection  # noqa: E402,F401
from .pbcs.dom import dom_build_api_contract  # noqa: E402,F401
from .pbcs.dom import dom_build_release_evidence  # noqa: E402,F401
from .pbcs.dom import dom_build_schema_contract  # noqa: E402,F401
from .pbcs.dom import dom_build_service_contract  # noqa: E402,F401
from .pbcs.dom import dom_build_workbench_view  # noqa: E402,F401
from .pbcs.dom import dom_capture_order  # noqa: E402,F401
from .pbcs.dom import dom_configure_runtime  # noqa: E402,F401
from .pbcs.dom import dom_confirm_order_shipped  # noqa: E402,F401
from .pbcs.dom import dom_create_fulfillment_plan  # noqa: E402,F401
from .pbcs.dom import dom_empty_state  # noqa: E402,F401
from .pbcs.dom import dom_permissions_contract  # noqa: E402,F401
from .pbcs.dom import dom_price_order  # noqa: E402,F401
from .pbcs.dom import dom_receive_event  # noqa: E402,F401
from .pbcs.dom import dom_register_rule  # noqa: E402,F401
from .pbcs.dom import dom_register_schema_extension  # noqa: E402,F401
from .pbcs.dom import dom_render_workbench  # noqa: E402,F401
from .pbcs.dom import dom_runtime_capabilities  # noqa: E402,F401
from .pbcs.dom import dom_runtime_smoke  # noqa: E402,F401
from .pbcs.dom import dom_screen_fraud  # noqa: E402,F401
from .pbcs.dom import dom_set_parameter  # noqa: E402,F401
from .pbcs.dom import dom_ui_contract  # noqa: E402,F401
from .pbcs.dom import dom_upsert_customer_projection  # noqa: E402,F401
from .pbcs.dom import dom_verify_order  # noqa: E402,F401
from .pbcs.dom import dom_verify_owned_table_boundary  # noqa: E402,F401
from .pbcs.personnel_identity import PERSONNEL_IDENTITY_ALLOWED_DATABASE_BACKENDS  # noqa: E402,F401
from .pbcs.personnel_identity import PERSONNEL_IDENTITY_CONSUMED_EVENT_TYPES  # noqa: E402,F401
from .pbcs.personnel_identity import PERSONNEL_IDENTITY_EMITTED_EVENT_TYPES  # noqa: E402,F401
from .pbcs.personnel_identity import PERSONNEL_IDENTITY_OWNED_TABLES  # noqa: E402,F401
from .pbcs.personnel_identity import PERSONNEL_IDENTITY_REQUIRED_EVENT_TOPIC  # noqa: E402,F401
from .pbcs.personnel_identity import PERSONNEL_IDENTITY_RUNTIME_CAPABILITY_KEYS  # noqa: E402,F401
from .pbcs.personnel_identity import PERSONNEL_IDENTITY_STANDARD_FEATURE_KEYS  # noqa: E402,F401
from .pbcs.personnel_identity import PERSONNEL_IDENTITY_UI_FRAGMENT_KEYS  # noqa: E402,F401
from .pbcs.personnel_identity import personnel_identity_assign_role  # noqa: E402,F401
from .pbcs.personnel_identity import personnel_identity_build_api_contract  # noqa: E402,F401
from .pbcs.personnel_identity import personnel_identity_build_org_chart  # noqa: E402,F401
from .pbcs.personnel_identity import personnel_identity_build_release_evidence  # noqa: E402,F401
from .pbcs.personnel_identity import personnel_identity_build_schema_contract  # noqa: E402,F401
from .pbcs.personnel_identity import personnel_identity_build_service_contract  # noqa: E402,F401
from .pbcs.personnel_identity import personnel_identity_build_workbench_view  # noqa: E402,F401
from .pbcs.personnel_identity import personnel_identity_configure_runtime  # noqa: E402,F401
from .pbcs.personnel_identity import personnel_identity_create_employee  # noqa: E402,F401
from .pbcs.personnel_identity import personnel_identity_empty_state  # noqa: E402,F401
from .pbcs.personnel_identity import personnel_identity_permissions_contract  # noqa: E402,F401
from .pbcs.personnel_identity import personnel_identity_receive_event  # noqa: E402,F401
from .pbcs.personnel_identity import personnel_identity_register_department  # noqa: E402,F401
from .pbcs.personnel_identity import personnel_identity_register_rule  # noqa: E402,F401
from .pbcs.personnel_identity import personnel_identity_register_schema_extension  # noqa: E402,F401
from .pbcs.personnel_identity import personnel_identity_render_workbench  # noqa: E402,F401
from .pbcs.personnel_identity import personnel_identity_runtime_capabilities  # noqa: E402,F401
from .pbcs.personnel_identity import personnel_identity_runtime_smoke  # noqa: E402,F401
from .pbcs.personnel_identity import personnel_identity_set_parameter  # noqa: E402,F401
from .pbcs.personnel_identity import personnel_identity_transition_employee_status  # noqa: E402,F401
from .pbcs.personnel_identity import personnel_identity_ui_contract  # noqa: E402,F401
from .pbcs.personnel_identity import personnel_identity_upsert_identity_attribute  # noqa: E402,F401
from .pbcs.personnel_identity import personnel_identity_verify_owned_table_boundary  # noqa: E402,F401
from .pbcs.time_labor import TIME_LABOR_ALLOWED_DATABASE_BACKENDS  # noqa: E402,F401
from .pbcs.time_labor import TIME_LABOR_CONSUMED_EVENT_TYPES  # noqa: E402,F401
from .pbcs.time_labor import TIME_LABOR_EMITTED_EVENT_TYPES  # noqa: E402,F401
from .pbcs.time_labor import TIME_LABOR_OWNED_TABLES  # noqa: E402,F401
from .pbcs.time_labor import TIME_LABOR_REQUIRED_EVENT_TOPIC  # noqa: E402,F401
from .pbcs.time_labor import TIME_LABOR_RUNTIME_CAPABILITY_KEYS  # noqa: E402,F401
from .pbcs.time_labor import TIME_LABOR_STANDARD_FEATURE_KEYS  # noqa: E402,F401
from .pbcs.time_labor import TIME_LABOR_UI_FRAGMENT_KEYS  # noqa: E402,F401
from .pbcs.time_labor import time_labor_approve_labor_summary  # noqa: E402,F401
from .pbcs.time_labor import time_labor_build_api_contract  # noqa: E402,F401
from .pbcs.time_labor import time_labor_build_release_evidence  # noqa: E402,F401
from .pbcs.time_labor import time_labor_build_schema_contract  # noqa: E402,F401
from .pbcs.time_labor import time_labor_build_service_contract  # noqa: E402,F401
from .pbcs.time_labor import time_labor_build_workbench_view  # noqa: E402,F401
from .pbcs.time_labor import time_labor_calculate_time_entry  # noqa: E402,F401
from .pbcs.time_labor import time_labor_configure_runtime  # noqa: E402,F401
from .pbcs.time_labor import time_labor_create_shift  # noqa: E402,F401
from .pbcs.time_labor import time_labor_empty_state  # noqa: E402,F401
from .pbcs.time_labor import time_labor_permissions_contract  # noqa: E402,F401
from .pbcs.time_labor import time_labor_record_absence  # noqa: E402,F401
from .pbcs.time_labor import time_labor_record_clock_event  # noqa: E402,F401
from .pbcs.time_labor import time_labor_receive_event  # noqa: E402,F401
from .pbcs.time_labor import time_labor_register_rule  # noqa: E402,F401
from .pbcs.time_labor import time_labor_register_schema_extension  # noqa: E402,F401
from .pbcs.time_labor import time_labor_render_workbench  # noqa: E402,F401
from .pbcs.time_labor import time_labor_runtime_capabilities  # noqa: E402,F401
from .pbcs.time_labor import time_labor_runtime_smoke  # noqa: E402,F401
from .pbcs.time_labor import time_labor_set_parameter  # noqa: E402,F401
from .pbcs.time_labor import time_labor_ui_contract  # noqa: E402,F401
from .pbcs.time_labor import time_labor_upsert_employee_projection  # noqa: E402,F401
from .pbcs.time_labor import time_labor_verify_owned_table_boundary  # noqa: E402,F401
from .pbcs.payroll_engine import PAYROLL_ENGINE_ALLOWED_DATABASE_BACKENDS  # noqa: E402,F401
from .pbcs.payroll_engine import PAYROLL_ENGINE_CONSUMED_EVENT_TYPES  # noqa: E402,F401
from .pbcs.payroll_engine import PAYROLL_ENGINE_EMITTED_EVENT_TYPES  # noqa: E402,F401
from .pbcs.payroll_engine import PAYROLL_ENGINE_OWNED_TABLES  # noqa: E402,F401
from .pbcs.payroll_engine import PAYROLL_ENGINE_REQUIRED_EVENT_TOPIC  # noqa: E402,F401
from .pbcs.payroll_engine import PAYROLL_ENGINE_RUNTIME_CAPABILITY_KEYS  # noqa: E402,F401
from .pbcs.payroll_engine import PAYROLL_ENGINE_STANDARD_FEATURE_KEYS  # noqa: E402,F401
from .pbcs.payroll_engine import PAYROLL_ENGINE_UI_FRAGMENT_KEYS  # noqa: E402,F401
from .pbcs.payroll_engine import payroll_engine_allocate_benefit  # noqa: E402,F401
from .pbcs.payroll_engine import payroll_engine_apply_deduction  # noqa: E402,F401
from .pbcs.payroll_engine import payroll_engine_build_api_contract  # noqa: E402,F401
from .pbcs.payroll_engine import payroll_engine_build_release_evidence  # noqa: E402,F401
from .pbcs.payroll_engine import payroll_engine_build_schema_contract  # noqa: E402,F401
from .pbcs.payroll_engine import payroll_engine_build_service_contract  # noqa: E402,F401
from .pbcs.payroll_engine import payroll_engine_build_workbench_view  # noqa: E402,F401
from .pbcs.payroll_engine import payroll_engine_calculate_payslip  # noqa: E402,F401
from .pbcs.payroll_engine import payroll_engine_configure_runtime  # noqa: E402,F401
from .pbcs.payroll_engine import payroll_engine_create_payroll_run  # noqa: E402,F401
from .pbcs.payroll_engine import payroll_engine_empty_state  # noqa: E402,F401
from .pbcs.payroll_engine import payroll_engine_ingest_labor_hours  # noqa: E402,F401
from .pbcs.payroll_engine import payroll_engine_post_payroll_run  # noqa: E402,F401
from .pbcs.payroll_engine import payroll_engine_prepare_payroll_filing  # noqa: E402,F401
from .pbcs.payroll_engine import payroll_engine_permissions_contract  # noqa: E402,F401
from .pbcs.payroll_engine import payroll_engine_receive_event  # noqa: E402,F401
from .pbcs.payroll_engine import payroll_engine_register_rule  # noqa: E402,F401
from .pbcs.payroll_engine import payroll_engine_register_schema_extension  # noqa: E402,F401
from .pbcs.payroll_engine import payroll_engine_render_workbench  # noqa: E402,F401
from .pbcs.payroll_engine import payroll_engine_runtime_capabilities  # noqa: E402,F401
from .pbcs.payroll_engine import payroll_engine_runtime_smoke  # noqa: E402,F401
from .pbcs.payroll_engine import payroll_engine_set_parameter  # noqa: E402,F401
from .pbcs.payroll_engine import payroll_engine_ui_contract  # noqa: E402,F401
from .pbcs.payroll_engine import payroll_engine_upsert_worker_projection  # noqa: E402,F401
from .pbcs.payroll_engine import payroll_engine_verify_owned_table_boundary  # noqa: E402,F401
from .pbcs.talent_onboarding import TALENT_ONBOARDING_ALLOWED_DATABASE_BACKENDS  # noqa: E402,F401
from .pbcs.talent_onboarding import TALENT_ONBOARDING_CONSUMED_EVENT_TYPES  # noqa: E402,F401
from .pbcs.talent_onboarding import TALENT_ONBOARDING_EMITTED_EVENT_TYPES  # noqa: E402,F401
from .pbcs.talent_onboarding import TALENT_ONBOARDING_OWNED_TABLES  # noqa: E402,F401
from .pbcs.talent_onboarding import TALENT_ONBOARDING_REQUIRED_EVENT_TOPIC  # noqa: E402,F401
from .pbcs.talent_onboarding import TALENT_ONBOARDING_RUNTIME_CAPABILITY_KEYS  # noqa: E402,F401
from .pbcs.talent_onboarding import TALENT_ONBOARDING_STANDARD_FEATURE_KEYS  # noqa: E402,F401
from .pbcs.talent_onboarding import TALENT_ONBOARDING_UI_FRAGMENT_KEYS  # noqa: E402,F401
from .pbcs.talent_onboarding import talent_onboarding_accept_offer  # noqa: E402,F401
from .pbcs.talent_onboarding import talent_onboarding_advance_candidate_stage  # noqa: E402,F401
from .pbcs.talent_onboarding import talent_onboarding_build_api_contract  # noqa: E402,F401
from .pbcs.talent_onboarding import talent_onboarding_build_release_evidence  # noqa: E402,F401
from .pbcs.talent_onboarding import talent_onboarding_build_schema_contract  # noqa: E402,F401
from .pbcs.talent_onboarding import talent_onboarding_build_service_contract  # noqa: E402,F401
from .pbcs.talent_onboarding import talent_onboarding_build_workbench_view  # noqa: E402,F401
from .pbcs.talent_onboarding import talent_onboarding_complete_onboarding_task  # noqa: E402,F401
from .pbcs.talent_onboarding import talent_onboarding_configure_runtime  # noqa: E402,F401
from .pbcs.talent_onboarding import talent_onboarding_create_candidate  # noqa: E402,F401
from .pbcs.talent_onboarding import talent_onboarding_create_job_requisition  # noqa: E402,F401
from .pbcs.talent_onboarding import talent_onboarding_create_onboarding_task  # noqa: E402,F401
from .pbcs.talent_onboarding import talent_onboarding_empty_state  # noqa: E402,F401
from .pbcs.talent_onboarding import talent_onboarding_extend_offer  # noqa: E402,F401
from .pbcs.talent_onboarding import talent_onboarding_provision_employee  # noqa: E402,F401
from .pbcs.talent_onboarding import talent_onboarding_permissions_contract  # noqa: E402,F401
from .pbcs.talent_onboarding import talent_onboarding_receive_event  # noqa: E402,F401
from .pbcs.talent_onboarding import talent_onboarding_record_background_check  # noqa: E402,F401
from .pbcs.talent_onboarding import talent_onboarding_register_rule  # noqa: E402,F401
from .pbcs.talent_onboarding import talent_onboarding_register_schema_extension  # noqa: E402,F401
from .pbcs.talent_onboarding import talent_onboarding_render_workbench  # noqa: E402,F401
from .pbcs.talent_onboarding import talent_onboarding_runtime_capabilities  # noqa: E402,F401
from .pbcs.talent_onboarding import talent_onboarding_runtime_smoke  # noqa: E402,F401
from .pbcs.talent_onboarding import talent_onboarding_set_parameter  # noqa: E402,F401
from .pbcs.talent_onboarding import talent_onboarding_ui_contract  # noqa: E402,F401
from .pbcs.talent_onboarding import talent_onboarding_verify_owned_table_boundary  # noqa: E402,F401
from .pbcs.mrp_engine import MRP_ENGINE_ALLOWED_DATABASE_BACKENDS  # noqa: E402,F401
from .pbcs.mrp_engine import MRP_ENGINE_CONSUMED_EVENT_TYPES  # noqa: E402,F401
from .pbcs.mrp_engine import MRP_ENGINE_EMITTED_EVENT_TYPES  # noqa: E402,F401
from .pbcs.mrp_engine import MRP_ENGINE_OWNED_TABLES  # noqa: E402,F401
from .pbcs.mrp_engine import MRP_ENGINE_REQUIRED_EVENT_TOPIC  # noqa: E402,F401
from .pbcs.mrp_engine import MRP_ENGINE_RUNTIME_CAPABILITY_KEYS  # noqa: E402,F401
from .pbcs.mrp_engine import MRP_ENGINE_STANDARD_FEATURE_KEYS  # noqa: E402,F401
from .pbcs.mrp_engine import MRP_ENGINE_UI_FRAGMENT_KEYS  # noqa: E402,F401
from .pbcs.mrp_engine import mrp_engine_build_api_contract  # noqa: E402,F401
from .pbcs.mrp_engine import mrp_engine_build_release_evidence  # noqa: E402,F401
from .pbcs.mrp_engine import mrp_engine_build_schema_contract  # noqa: E402,F401
from .pbcs.mrp_engine import mrp_engine_build_service_contract  # noqa: E402,F401
from .pbcs.mrp_engine import mrp_engine_build_workbench_view  # noqa: E402,F401
from .pbcs.mrp_engine import mrp_engine_calculate_material_plan  # noqa: E402,F401
from .pbcs.mrp_engine import mrp_engine_configure_runtime  # noqa: E402,F401
from .pbcs.mrp_engine import mrp_engine_create_mrp_run  # noqa: E402,F401
from .pbcs.mrp_engine import mrp_engine_empty_state  # noqa: E402,F401
from .pbcs.mrp_engine import mrp_engine_explode_bom  # noqa: E402,F401
from .pbcs.mrp_engine import mrp_engine_ingest_demand_projection  # noqa: E402,F401
from .pbcs.mrp_engine import mrp_engine_ingest_inventory_projection  # noqa: E402,F401
from .pbcs.mrp_engine import mrp_engine_permissions_contract  # noqa: E402,F401
from .pbcs.mrp_engine import mrp_engine_receive_event  # noqa: E402,F401
from .pbcs.mrp_engine import mrp_engine_register_bom  # noqa: E402,F401
from .pbcs.mrp_engine import mrp_engine_register_rule  # noqa: E402,F401
from .pbcs.mrp_engine import mrp_engine_register_schema_extension  # noqa: E402,F401
from .pbcs.mrp_engine import mrp_engine_release_planned_order  # noqa: E402,F401
from .pbcs.mrp_engine import mrp_engine_render_workbench  # noqa: E402,F401
from .pbcs.mrp_engine import mrp_engine_runtime_capabilities  # noqa: E402,F401
from .pbcs.mrp_engine import mrp_engine_runtime_smoke  # noqa: E402,F401
from .pbcs.mrp_engine import mrp_engine_set_parameter  # noqa: E402,F401
from .pbcs.mrp_engine import mrp_engine_ui_contract  # noqa: E402,F401
from .pbcs.mrp_engine import mrp_engine_verify_owned_table_boundary  # noqa: E402,F401
from .pbcs.production_control import PRODUCTION_CONTROL_ALLOWED_DATABASE_BACKENDS  # noqa: E402,F401
from .pbcs.production_control import PRODUCTION_CONTROL_CONSUMED_EVENT_TYPES  # noqa: E402,F401
from .pbcs.production_control import PRODUCTION_CONTROL_EMITTED_EVENT_TYPES  # noqa: E402,F401
from .pbcs.production_control import PRODUCTION_CONTROL_OWNED_TABLES  # noqa: E402,F401
from .pbcs.production_control import PRODUCTION_CONTROL_REQUIRED_EVENT_TOPIC  # noqa: E402,F401
from .pbcs.production_control import PRODUCTION_CONTROL_RUNTIME_CAPABILITY_KEYS  # noqa: E402,F401
from .pbcs.production_control import PRODUCTION_CONTROL_STANDARD_FEATURE_KEYS  # noqa: E402,F401
from .pbcs.production_control import PRODUCTION_CONTROL_UI_FRAGMENT_KEYS  # noqa: E402,F401
from .pbcs.production_control import production_control_build_api_contract  # noqa: E402,F401
from .pbcs.production_control import production_control_allocate_capacity_plan  # noqa: E402,F401
from .pbcs.production_control import production_control_append_audit_entry  # noqa: E402,F401
from .pbcs.production_control import production_control_book_labor_time  # noqa: E402,F401
from .pbcs.production_control import production_control_book_machine_time  # noqa: E402,F401
from .pbcs.production_control import production_control_capture_oee_snapshot  # noqa: E402,F401
from .pbcs.production_control import production_control_build_workbench_view  # noqa: E402,F401
from .pbcs.production_control import production_control_complete_production_order  # noqa: E402,F401
from .pbcs.production_control import production_control_configure_runtime  # noqa: E402,F401
from .pbcs.production_control import production_control_confirm_operation  # noqa: E402,F401
from .pbcs.production_control import production_control_create_production_order  # noqa: E402,F401
from .pbcs.production_control import production_control_define_routing_step  # noqa: E402,F401
from .pbcs.production_control import production_control_empty_state  # noqa: E402,F401
from .pbcs.production_control import production_control_open_exception_case  # noqa: E402,F401
from .pbcs.production_control import production_control_permissions_contract  # noqa: E402,F401
from .pbcs.production_control import production_control_record_completion_proof  # noqa: E402,F401
from .pbcs.production_control import production_control_record_downtime  # noqa: E402,F401
from .pbcs.production_control import production_control_record_material_consumption  # noqa: E402,F401
from .pbcs.production_control import production_control_record_quality_gate_result  # noqa: E402,F401
from .pbcs.production_control import production_control_record_scrap_rework  # noqa: E402,F401
from .pbcs.production_control import production_control_receive_event  # noqa: E402,F401
from .pbcs.production_control import production_control_register_rule  # noqa: E402,F401
from .pbcs.production_control import production_control_register_schema_extension  # noqa: E402,F401
from .pbcs.production_control import production_control_register_work_center  # noqa: E402,F401
from .pbcs.production_control import production_control_render_workbench  # noqa: E402,F401
from .pbcs.production_control import production_control_runtime_capabilities  # noqa: E402,F401
from .pbcs.production_control import production_control_runtime_smoke  # noqa: E402,F401
from .pbcs.production_control import production_control_schedule_order  # noqa: E402,F401
from .pbcs.production_control import production_control_set_parameter  # noqa: E402,F401
from .pbcs.production_control import production_control_start_operation  # noqa: E402,F401
from .pbcs.production_control import production_control_ui_contract  # noqa: E402,F401
from .pbcs.production_control import production_control_verify_owned_table_boundary  # noqa: E402,F401
from .pbcs.quality_assurance import QUALITY_ASSURANCE_ALLOWED_DATABASE_BACKENDS  # noqa: E402,F401
from .pbcs.quality_assurance import QUALITY_ASSURANCE_CONSUMED_EVENT_TYPES  # noqa: E402,F401
from .pbcs.quality_assurance import QUALITY_ASSURANCE_EMITTED_EVENT_TYPES  # noqa: E402,F401
from .pbcs.quality_assurance import QUALITY_ASSURANCE_OWNED_TABLES  # noqa: E402,F401
from .pbcs.quality_assurance import QUALITY_ASSURANCE_REQUIRED_EVENT_TOPIC  # noqa: E402,F401
from .pbcs.quality_assurance import QUALITY_ASSURANCE_RUNTIME_CAPABILITY_KEYS  # noqa: E402,F401
from .pbcs.quality_assurance import QUALITY_ASSURANCE_STANDARD_FEATURE_KEYS  # noqa: E402,F401
from .pbcs.quality_assurance import QUALITY_ASSURANCE_UI_FRAGMENT_KEYS  # noqa: E402,F401
from .pbcs.quality_assurance import quality_assurance_build_api_contract  # noqa: E402,F401
from .pbcs.quality_assurance import quality_assurance_build_release_evidence  # noqa: E402,F401
from .pbcs.quality_assurance import quality_assurance_build_schema_contract  # noqa: E402,F401
from .pbcs.quality_assurance import quality_assurance_build_service_contract  # noqa: E402,F401
from .pbcs.quality_assurance import quality_assurance_build_workbench_view  # noqa: E402,F401
from .pbcs.quality_assurance import quality_assurance_configure_runtime  # noqa: E402,F401
from .pbcs.quality_assurance import quality_assurance_create_inspection_plan  # noqa: E402,F401
from .pbcs.quality_assurance import quality_assurance_create_quality_hold  # noqa: E402,F401
from .pbcs.quality_assurance import quality_assurance_disposition_nonconformance  # noqa: E402,F401
from .pbcs.quality_assurance import quality_assurance_empty_state  # noqa: E402,F401
from .pbcs.quality_assurance import quality_assurance_permissions_contract  # noqa: E402,F401
from .pbcs.quality_assurance import quality_assurance_raise_nonconformance  # noqa: E402,F401
from .pbcs.quality_assurance import quality_assurance_receive_event  # noqa: E402,F401
from .pbcs.quality_assurance import quality_assurance_record_inspection_result  # noqa: E402,F401
from .pbcs.quality_assurance import quality_assurance_register_rule  # noqa: E402,F401
from .pbcs.quality_assurance import quality_assurance_register_schema_extension  # noqa: E402,F401
from .pbcs.quality_assurance import quality_assurance_release_quality_hold  # noqa: E402,F401
from .pbcs.quality_assurance import quality_assurance_render_workbench  # noqa: E402,F401
from .pbcs.quality_assurance import quality_assurance_runtime_capabilities  # noqa: E402,F401
from .pbcs.quality_assurance import quality_assurance_runtime_smoke  # noqa: E402,F401
from .pbcs.quality_assurance import quality_assurance_set_parameter  # noqa: E402,F401
from .pbcs.quality_assurance import quality_assurance_ui_contract  # noqa: E402,F401
from .pbcs.quality_assurance import quality_assurance_verify_owned_table_boundary  # noqa: E402,F401
from .pbcs.eam import EAM_ALLOWED_DATABASE_BACKENDS  # noqa: E402,F401
from .pbcs.eam import EAM_CONSUMED_EVENT_TYPES  # noqa: E402,F401
from .pbcs.eam import EAM_EMITTED_EVENT_TYPES  # noqa: E402,F401
from .pbcs.eam import EAM_OWNED_TABLES  # noqa: E402,F401
from .pbcs.eam import EAM_REQUIRED_EVENT_TOPIC  # noqa: E402,F401
from .pbcs.eam import EAM_RUNTIME_CAPABILITY_KEYS  # noqa: E402,F401
from .pbcs.eam import EAM_STANDARD_FEATURE_KEYS  # noqa: E402,F401
from .pbcs.eam import EAM_UI_FRAGMENT_KEYS  # noqa: E402,F401
from .pbcs.eam import eam_build_api_contract  # noqa: E402,F401
from .pbcs.eam import eam_build_workbench_view  # noqa: E402,F401
from .pbcs.eam import eam_complete_work_order  # noqa: E402,F401
from .pbcs.eam import eam_configure_runtime  # noqa: E402,F401
from .pbcs.eam import eam_create_maintenance_plan  # noqa: E402,F401
from .pbcs.eam import eam_create_safety_permit  # noqa: E402,F401
from .pbcs.eam import eam_create_work_order  # noqa: E402,F401
from .pbcs.eam import eam_empty_state  # noqa: E402,F401
from .pbcs.eam import eam_issue_spare_part  # noqa: E402,F401
from .pbcs.eam import eam_permissions_contract  # noqa: E402,F401
from .pbcs.eam import eam_record_condition_reading  # noqa: E402,F401
from .pbcs.eam import eam_record_meter_reading  # noqa: E402,F401
from .pbcs.eam import eam_receive_event  # noqa: E402,F401
from .pbcs.eam import eam_register_equipment  # noqa: E402,F401
from .pbcs.eam import eam_register_rule  # noqa: E402,F401
from .pbcs.eam import eam_register_schema_extension  # noqa: E402,F401
from .pbcs.eam import eam_render_workbench  # noqa: E402,F401
from .pbcs.eam import eam_runtime_capabilities  # noqa: E402,F401
from .pbcs.eam import eam_runtime_smoke  # noqa: E402,F401
from .pbcs.eam import eam_schedule_work_order  # noqa: E402,F401
from .pbcs.eam import eam_set_parameter  # noqa: E402,F401
from .pbcs.eam import eam_ui_contract  # noqa: E402,F401
from .pbcs.eam import eam_verify_owned_table_boundary  # noqa: E402,F401
from .pbcs.product_catalog_pim import PRODUCT_CATALOG_PIM_ALLOWED_DATABASE_BACKENDS  # noqa: E402,F401
from .pbcs.product_catalog_pim import PRODUCT_CATALOG_PIM_CONSUMED_EVENT_TYPES  # noqa: E402,F401
from .pbcs.product_catalog_pim import PRODUCT_CATALOG_PIM_EMITTED_EVENT_TYPES  # noqa: E402,F401
from .pbcs.product_catalog_pim import PRODUCT_CATALOG_PIM_OWNED_TABLES  # noqa: E402,F401
from .pbcs.product_catalog_pim import PRODUCT_CATALOG_PIM_REQUIRED_EVENT_TOPIC  # noqa: E402,F401
from .pbcs.product_catalog_pim import PRODUCT_CATALOG_PIM_RUNTIME_CAPABILITY_KEYS  # noqa: E402,F401
from .pbcs.product_catalog_pim import PRODUCT_CATALOG_PIM_STANDARD_FEATURE_KEYS  # noqa: E402,F401
from .pbcs.product_catalog_pim import PRODUCT_CATALOG_PIM_UI_FRAGMENT_KEYS  # noqa: E402,F401
from .pbcs.product_catalog_pim import product_catalog_pim_add_compliance_claim  # noqa: E402,F401
from .pbcs.product_catalog_pim import product_catalog_pim_add_localized_content  # noqa: E402,F401
from .pbcs.product_catalog_pim import product_catalog_pim_add_price_metadata  # noqa: E402,F401
from .pbcs.product_catalog_pim import product_catalog_pim_attach_product_media  # noqa: E402,F401
from .pbcs.product_catalog_pim import product_catalog_pim_build_api_contract  # noqa: E402,F401
from .pbcs.product_catalog_pim import product_catalog_pim_build_release_evidence  # noqa: E402,F401
from .pbcs.product_catalog_pim import product_catalog_pim_build_schema_contract  # noqa: E402,F401
from .pbcs.product_catalog_pim import product_catalog_pim_build_service_contract  # noqa: E402,F401
from .pbcs.product_catalog_pim import product_catalog_pim_build_workbench_view  # noqa: E402,F401
from .pbcs.product_catalog_pim import product_catalog_pim_configure_runtime  # noqa: E402,F401
from .pbcs.product_catalog_pim import product_catalog_pim_create_product_family  # noqa: E402,F401
from .pbcs.product_catalog_pim import product_catalog_pim_define_attribute_schema  # noqa: E402,F401
from .pbcs.product_catalog_pim import product_catalog_pim_empty_state  # noqa: E402,F401
from .pbcs.product_catalog_pim import product_catalog_pim_permissions_contract  # noqa: E402,F401
from .pbcs.product_catalog_pim import product_catalog_pim_publish_product  # noqa: E402,F401
from .pbcs.product_catalog_pim import product_catalog_pim_receive_event  # noqa: E402,F401
from .pbcs.product_catalog_pim import product_catalog_pim_register_product  # noqa: E402,F401
from .pbcs.product_catalog_pim import product_catalog_pim_register_rule  # noqa: E402,F401
from .pbcs.product_catalog_pim import product_catalog_pim_register_schema_extension  # noqa: E402,F401
from .pbcs.product_catalog_pim import product_catalog_pim_render_workbench  # noqa: E402,F401
from .pbcs.product_catalog_pim import product_catalog_pim_runtime_capabilities  # noqa: E402,F401
from .pbcs.product_catalog_pim import product_catalog_pim_runtime_smoke  # noqa: E402,F401
from .pbcs.product_catalog_pim import product_catalog_pim_set_parameter  # noqa: E402,F401
from .pbcs.product_catalog_pim import product_catalog_pim_set_product_attribute  # noqa: E402,F401
from .pbcs.product_catalog_pim import product_catalog_pim_ui_contract  # noqa: E402,F401
from .pbcs.product_catalog_pim import product_catalog_pim_verify_owned_table_boundary  # noqa: E402,F401
from .pbcs.customer_360 import CUSTOMER_360_ALLOWED_DATABASE_BACKENDS  # noqa: E402,F401
from .pbcs.customer_360 import CUSTOMER_360_CONSUMED_EVENT_TYPES  # noqa: E402,F401
from .pbcs.customer_360 import CUSTOMER_360_EMITTED_EVENT_TYPES  # noqa: E402,F401
from .pbcs.customer_360 import CUSTOMER_360_OWNED_TABLES  # noqa: E402,F401
from .pbcs.customer_360 import CUSTOMER_360_REQUIRED_EVENT_TOPIC  # noqa: E402,F401
from .pbcs.customer_360 import CUSTOMER_360_RUNTIME_CAPABILITY_KEYS  # noqa: E402,F401
from .pbcs.customer_360 import CUSTOMER_360_STANDARD_FEATURE_KEYS  # noqa: E402,F401
from .pbcs.customer_360 import CUSTOMER_360_UI_FRAGMENT_KEYS  # noqa: E402,F401
from .pbcs.customer_360 import customer_360_build_api_contract  # noqa: E402,F401
from .pbcs.customer_360 import customer_360_build_release_evidence  # noqa: E402,F401
from .pbcs.customer_360 import customer_360_build_schema_contract  # noqa: E402,F401
from .pbcs.customer_360 import customer_360_build_service_contract  # noqa: E402,F401
from .pbcs.customer_360 import customer_360_build_timeline  # noqa: E402,F401
from .pbcs.customer_360 import customer_360_build_workbench_view  # noqa: E402,F401
from .pbcs.customer_360 import customer_360_capture_touchpoint  # noqa: E402,F401
from .pbcs.customer_360 import customer_360_configure_runtime  # noqa: E402,F401
from .pbcs.customer_360 import customer_360_create_profile  # noqa: E402,F401
from .pbcs.customer_360 import customer_360_empty_state  # noqa: E402,F401
from .pbcs.customer_360 import customer_360_ingest_engagement_event  # noqa: E402,F401
from .pbcs.customer_360 import customer_360_link_identity  # noqa: E402,F401
from .pbcs.customer_360 import customer_360_open_merge_case  # noqa: E402,F401
from .pbcs.customer_360 import customer_360_permissions_contract  # noqa: E402,F401
from .pbcs.customer_360 import customer_360_receive_event  # noqa: E402,F401
from .pbcs.customer_360 import customer_360_record_consent  # noqa: E402,F401
from .pbcs.customer_360 import customer_360_register_rule  # noqa: E402,F401
from .pbcs.customer_360 import customer_360_register_schema_extension  # noqa: E402,F401
from .pbcs.customer_360 import customer_360_render_workbench  # noqa: E402,F401
from .pbcs.customer_360 import customer_360_resolve_merge_case  # noqa: E402,F401
from .pbcs.customer_360 import customer_360_runtime_capabilities  # noqa: E402,F401
from .pbcs.customer_360 import customer_360_runtime_smoke  # noqa: E402,F401
from .pbcs.customer_360 import customer_360_set_parameter  # noqa: E402,F401
from .pbcs.customer_360 import customer_360_set_preference  # noqa: E402,F401
from .pbcs.customer_360 import customer_360_ui_contract  # noqa: E402,F401
from .pbcs.customer_360 import customer_360_verify_owned_table_boundary  # noqa: E402,F401
from .pbcs.global_inventory_visibility import GLOBAL_INVENTORY_VISIBILITY_ALLOWED_DATABASE_BACKENDS  # noqa: E402,F401
from .pbcs.global_inventory_visibility import GLOBAL_INVENTORY_VISIBILITY_CONSUMED_EVENT_TYPES  # noqa: E402,F401
from .pbcs.global_inventory_visibility import GLOBAL_INVENTORY_VISIBILITY_EMITTED_EVENT_TYPES  # noqa: E402,F401
from .pbcs.global_inventory_visibility import GLOBAL_INVENTORY_VISIBILITY_OWNED_TABLES  # noqa: E402,F401
from .pbcs.global_inventory_visibility import GLOBAL_INVENTORY_VISIBILITY_REQUIRED_EVENT_TOPIC  # noqa: E402,F401
from .pbcs.global_inventory_visibility import GLOBAL_INVENTORY_VISIBILITY_RUNTIME_CAPABILITY_KEYS  # noqa: E402,F401
from .pbcs.global_inventory_visibility import GLOBAL_INVENTORY_VISIBILITY_STANDARD_FEATURE_KEYS  # noqa: E402,F401
from .pbcs.global_inventory_visibility import GLOBAL_INVENTORY_VISIBILITY_UI_FRAGMENT_KEYS  # noqa: E402,F401
from .pbcs.global_inventory_visibility import global_inventory_visibility_build_api_contract  # noqa: E402,F401
from .pbcs.global_inventory_visibility import global_inventory_visibility_build_release_evidence  # noqa: E402,F401
from .pbcs.global_inventory_visibility import global_inventory_visibility_build_schema_contract  # noqa: E402,F401
from .pbcs.global_inventory_visibility import global_inventory_visibility_build_service_contract  # noqa: E402,F401
from .pbcs.global_inventory_visibility import global_inventory_visibility_build_workbench_view  # noqa: E402,F401
from .pbcs.global_inventory_visibility import global_inventory_visibility_configure_runtime  # noqa: E402,F401
from .pbcs.global_inventory_visibility import global_inventory_visibility_empty_state  # noqa: E402,F401
from .pbcs.global_inventory_visibility import global_inventory_visibility_get_global_availability  # noqa: E402,F401
from .pbcs.global_inventory_visibility import global_inventory_visibility_ingest_event  # noqa: E402,F401
from .pbcs.global_inventory_visibility import global_inventory_visibility_permissions_contract  # noqa: E402,F401
from .pbcs.global_inventory_visibility import global_inventory_visibility_project_availability  # noqa: E402,F401
from .pbcs.global_inventory_visibility import global_inventory_visibility_record_availability_snapshot  # noqa: E402,F401
from .pbcs.global_inventory_visibility import global_inventory_visibility_register_inventory_pool  # noqa: E402,F401
from .pbcs.global_inventory_visibility import global_inventory_visibility_register_rule  # noqa: E402,F401
from .pbcs.global_inventory_visibility import global_inventory_visibility_register_schema_extension  # noqa: E402,F401
from .pbcs.global_inventory_visibility import global_inventory_visibility_register_supply_node  # noqa: E402,F401
from .pbcs.global_inventory_visibility import global_inventory_visibility_render_workbench  # noqa: E402,F401
from .pbcs.global_inventory_visibility import global_inventory_visibility_reserve_inventory  # noqa: E402,F401
from .pbcs.global_inventory_visibility import global_inventory_visibility_runtime_capabilities  # noqa: E402,F401
from .pbcs.global_inventory_visibility import global_inventory_visibility_runtime_smoke  # noqa: E402,F401
from .pbcs.global_inventory_visibility import global_inventory_visibility_set_parameter  # noqa: E402,F401
from .pbcs.global_inventory_visibility import global_inventory_visibility_ui_contract  # noqa: E402,F401
from .pbcs.global_inventory_visibility import global_inventory_visibility_verify_owned_table_boundary  # noqa: E402,F401
from .pbcs.order_routing_optimization import ORDER_ROUTING_OPTIMIZATION_ALLOWED_DATABASE_BACKENDS  # noqa: E402,F401
from .pbcs.order_routing_optimization import ORDER_ROUTING_OPTIMIZATION_CONSUMED_EVENT_TYPES  # noqa: E402,F401
from .pbcs.order_routing_optimization import ORDER_ROUTING_OPTIMIZATION_EMITTED_EVENT_TYPES  # noqa: E402,F401
from .pbcs.order_routing_optimization import ORDER_ROUTING_OPTIMIZATION_OWNED_TABLES  # noqa: E402,F401
from .pbcs.order_routing_optimization import ORDER_ROUTING_OPTIMIZATION_REQUIRED_EVENT_TOPIC  # noqa: E402,F401
from .pbcs.order_routing_optimization import ORDER_ROUTING_OPTIMIZATION_RUNTIME_CAPABILITY_KEYS  # noqa: E402,F401
from .pbcs.order_routing_optimization import ORDER_ROUTING_OPTIMIZATION_STANDARD_FEATURE_KEYS  # noqa: E402,F401
from .pbcs.order_routing_optimization import ORDER_ROUTING_OPTIMIZATION_UI_FRAGMENT_KEYS  # noqa: E402,F401
from .pbcs.order_routing_optimization import order_routing_optimization_build_api_contract  # noqa: E402,F401
from .pbcs.order_routing_optimization import order_routing_optimization_build_release_evidence  # noqa: E402,F401
from .pbcs.order_routing_optimization import order_routing_optimization_build_schema_contract  # noqa: E402,F401
from .pbcs.order_routing_optimization import order_routing_optimization_build_service_contract  # noqa: E402,F401
from .pbcs.order_routing_optimization import order_routing_optimization_build_workbench_view  # noqa: E402,F401
from .pbcs.order_routing_optimization import order_routing_optimization_configure_runtime  # noqa: E402,F401
from .pbcs.order_routing_optimization import order_routing_optimization_empty_state  # noqa: E402,F401
from .pbcs.order_routing_optimization import order_routing_optimization_handle_event  # noqa: E402,F401
from .pbcs.order_routing_optimization import order_routing_optimization_ingest_capacity_snapshot  # noqa: E402,F401
from .pbcs.order_routing_optimization import order_routing_optimization_permissions_contract  # noqa: E402,F401
from .pbcs.order_routing_optimization import order_routing_optimization_register_rule  # noqa: E402,F401
from .pbcs.order_routing_optimization import order_routing_optimization_register_schema_extension  # noqa: E402,F401
from .pbcs.order_routing_optimization import order_routing_optimization_render_workbench  # noqa: E402,F401
from .pbcs.order_routing_optimization import order_routing_optimization_route_orders  # noqa: E402,F401
from .pbcs.order_routing_optimization import order_routing_optimization_runtime_capabilities  # noqa: E402,F401
from .pbcs.order_routing_optimization import order_routing_optimization_runtime_smoke  # noqa: E402,F401
from .pbcs.order_routing_optimization import order_routing_optimization_set_parameter  # noqa: E402,F401
from .pbcs.order_routing_optimization import order_routing_optimization_ui_contract  # noqa: E402,F401
from .pbcs.order_routing_optimization import order_routing_optimization_upsert_route_candidate  # noqa: E402,F401
from .pbcs.order_routing_optimization import order_routing_optimization_verify_owned_table_boundary  # noqa: E402,F401
from .pbcs.checkout_processing import CHECKOUT_PROCESSING_RUNTIME_CAPABILITY_KEYS  # noqa: E402,F401
from .pbcs.checkout_processing import CHECKOUT_PROCESSING_STANDARD_FEATURE_KEYS  # noqa: E402,F401
from .pbcs.checkout_processing import CHECKOUT_PROCESSING_UI_FRAGMENT_KEYS  # noqa: E402,F401
from .pbcs.checkout_processing import CHECKOUT_PROCESSING_ALLOWED_DATABASE_BACKENDS  # noqa: E402,F401
from .pbcs.checkout_processing import CHECKOUT_PROCESSING_CONSUMED_EVENT_TYPES  # noqa: E402,F401
from .pbcs.checkout_processing import CHECKOUT_PROCESSING_EMITTED_EVENT_TYPES  # noqa: E402,F401
from .pbcs.checkout_processing import CHECKOUT_PROCESSING_OWNED_TABLES  # noqa: E402,F401
from .pbcs.checkout_processing import CHECKOUT_PROCESSING_REQUIRED_EVENT_TOPIC  # noqa: E402,F401
from .pbcs.checkout_processing import checkout_processing_add_cart_line  # noqa: E402,F401
from .pbcs.checkout_processing import checkout_processing_apply_coupon  # noqa: E402,F401
from .pbcs.checkout_processing import checkout_processing_authorize_payment_intent  # noqa: E402,F401
from .pbcs.checkout_processing import checkout_processing_build_api_contract  # noqa: E402,F401
from .pbcs.checkout_processing import checkout_processing_build_workbench_view  # noqa: E402,F401
from .pbcs.checkout_processing import checkout_processing_capture_payment_intent  # noqa: E402,F401
from .pbcs.checkout_processing import checkout_processing_complete_checkout  # noqa: E402,F401
from .pbcs.checkout_processing import checkout_processing_confirm_inventory_reservation  # noqa: E402,F401
from .pbcs.checkout_processing import checkout_processing_configure_runtime  # noqa: E402,F401
from .pbcs.checkout_processing import checkout_processing_create_cart  # noqa: E402,F401
from .pbcs.checkout_processing import checkout_processing_empty_state  # noqa: E402,F401
from .pbcs.checkout_processing import checkout_processing_open_checkout_session  # noqa: E402,F401
from .pbcs.checkout_processing import checkout_processing_permissions_contract  # noqa: E402,F401
from .pbcs.checkout_processing import checkout_processing_receive_event  # noqa: E402,F401
from .pbcs.checkout_processing import checkout_processing_register_schema_extension  # noqa: E402,F401
from .pbcs.checkout_processing import checkout_processing_register_rule  # noqa: E402,F401
from .pbcs.checkout_processing import checkout_processing_render_workbench  # noqa: E402,F401
from .pbcs.checkout_processing import checkout_processing_runtime_capabilities  # noqa: E402,F401
from .pbcs.checkout_processing import checkout_processing_runtime_smoke  # noqa: E402,F401
from .pbcs.checkout_processing import checkout_processing_set_parameter  # noqa: E402,F401
from .pbcs.checkout_processing import checkout_processing_ui_contract  # noqa: E402,F401
from .pbcs.checkout_processing import checkout_processing_verify_owned_table_boundary  # noqa: E402,F401
from .pbcs.payment_orchestration import PAYMENT_ORCHESTRATION_ALLOWED_DATABASE_BACKENDS  # noqa: E402,F401
from .pbcs.payment_orchestration import PAYMENT_ORCHESTRATION_CONSUMED_EVENT_TYPES  # noqa: E402,F401
from .pbcs.payment_orchestration import PAYMENT_ORCHESTRATION_EMITTED_EVENT_TYPES  # noqa: E402,F401
from .pbcs.payment_orchestration import PAYMENT_ORCHESTRATION_OWNED_TABLES  # noqa: E402,F401
from .pbcs.payment_orchestration import PAYMENT_ORCHESTRATION_REQUIRED_EVENT_TOPIC  # noqa: E402,F401
from .pbcs.payment_orchestration import PAYMENT_ORCHESTRATION_RUNTIME_CAPABILITY_KEYS  # noqa: E402,F401
from .pbcs.payment_orchestration import PAYMENT_ORCHESTRATION_STANDARD_FEATURE_KEYS  # noqa: E402,F401
from .pbcs.payment_orchestration import PAYMENT_ORCHESTRATION_UI_FRAGMENT_KEYS  # noqa: E402,F401
from .pbcs.payment_orchestration import payment_orchestration_build_api_contract  # noqa: E402,F401
from .pbcs.payment_orchestration import payment_orchestration_build_workbench_view  # noqa: E402,F401
from .pbcs.payment_orchestration import payment_orchestration_capture_payment  # noqa: E402,F401
from .pbcs.payment_orchestration import payment_orchestration_configure_runtime  # noqa: E402,F401
from .pbcs.payment_orchestration import payment_orchestration_create_payment_intent  # noqa: E402,F401
from .pbcs.payment_orchestration import payment_orchestration_empty_state  # noqa: E402,F401
from .pbcs.payment_orchestration import payment_orchestration_permissions_contract  # noqa: E402,F401
from .pbcs.payment_orchestration import payment_orchestration_receive_event  # noqa: E402,F401
from .pbcs.payment_orchestration import payment_orchestration_refund_payment  # noqa: E402,F401
from .pbcs.payment_orchestration import payment_orchestration_register_gateway  # noqa: E402,F401
from .pbcs.payment_orchestration import payment_orchestration_register_rule  # noqa: E402,F401
from .pbcs.payment_orchestration import payment_orchestration_register_schema_extension  # noqa: E402,F401
from .pbcs.payment_orchestration import payment_orchestration_render_workbench  # noqa: E402,F401
from .pbcs.payment_orchestration import payment_orchestration_request_fraud_check  # noqa: E402,F401
from .pbcs.payment_orchestration import payment_orchestration_route_gateway  # noqa: E402,F401
from .pbcs.payment_orchestration import payment_orchestration_runtime_capabilities  # noqa: E402,F401
from .pbcs.payment_orchestration import payment_orchestration_runtime_smoke  # noqa: E402,F401
from .pbcs.payment_orchestration import payment_orchestration_set_parameter  # noqa: E402,F401
from .pbcs.payment_orchestration import payment_orchestration_tokenize_payment_method  # noqa: E402,F401
from .pbcs.payment_orchestration import payment_orchestration_ui_contract  # noqa: E402,F401
from .pbcs.payment_orchestration import payment_orchestration_verify_owned_table_boundary  # noqa: E402,F401
from .pbcs.payment_orchestration import payment_orchestration_void_payment  # noqa: E402,F401
from .pbcs.subscription_billing import SUBSCRIPTION_BILLING_RUNTIME_CAPABILITY_KEYS  # noqa: E402,F401
from .pbcs.subscription_billing import SUBSCRIPTION_BILLING_STANDARD_FEATURE_KEYS  # noqa: E402,F401
from .pbcs.subscription_billing import SUBSCRIPTION_BILLING_UI_FRAGMENT_KEYS  # noqa: E402,F401
from .pbcs.subscription_billing import subscription_billing_build_api_contract  # noqa: E402,F401
from .pbcs.subscription_billing import subscription_billing_build_workbench_view  # noqa: E402,F401
from .pbcs.subscription_billing import subscription_billing_configure_runtime  # noqa: E402,F401
from .pbcs.subscription_billing import subscription_billing_create_dunning_notice  # noqa: E402,F401
from .pbcs.subscription_billing import subscription_billing_create_subscription  # noqa: E402,F401
from .pbcs.subscription_billing import subscription_billing_empty_state  # noqa: E402,F401
from .pbcs.subscription_billing import subscription_billing_generate_invoice  # noqa: E402,F401
from .pbcs.subscription_billing import subscription_billing_receive_event  # noqa: E402,F401
from .pbcs.subscription_billing import subscription_billing_record_usage  # noqa: E402,F401
from .pbcs.subscription_billing import subscription_billing_register_plan  # noqa: E402,F401
from .pbcs.subscription_billing import subscription_billing_register_rule  # noqa: E402,F401
from .pbcs.subscription_billing import subscription_billing_register_schema_extension  # noqa: E402,F401
from .pbcs.subscription_billing import subscription_billing_render_workbench  # noqa: E402,F401
from .pbcs.subscription_billing import subscription_billing_renew_subscription  # noqa: E402,F401
from .pbcs.subscription_billing import subscription_billing_permissions_contract  # noqa: E402,F401
from .pbcs.subscription_billing import subscription_billing_runtime_capabilities  # noqa: E402,F401
from .pbcs.subscription_billing import subscription_billing_runtime_smoke  # noqa: E402,F401
from .pbcs.subscription_billing import subscription_billing_set_parameter  # noqa: E402,F401
from .pbcs.subscription_billing import subscription_billing_ui_contract  # noqa: E402,F401
from .pbcs.subscription_billing import subscription_billing_verify_owned_table_boundary  # noqa: E402,F401
from .pbcs.cross_border_trade import CROSS_BORDER_TRADE_RUNTIME_CAPABILITY_KEYS  # noqa: E402,F401
from .pbcs.cross_border_trade import CROSS_BORDER_TRADE_STANDARD_FEATURE_KEYS  # noqa: E402,F401
from .pbcs.cross_border_trade import CROSS_BORDER_TRADE_UI_FRAGMENT_KEYS  # noqa: E402,F401
from .pbcs.cross_border_trade import CROSS_BORDER_TRADE_ALLOWED_DATABASE_BACKENDS  # noqa: E402,F401
from .pbcs.cross_border_trade import CROSS_BORDER_TRADE_OWNED_TABLES  # noqa: E402,F401
from .pbcs.cross_border_trade import cross_border_trade_build_api_contract  # noqa: E402,F401
from .pbcs.cross_border_trade import cross_border_trade_build_release_evidence  # noqa: E402,F401
from .pbcs.cross_border_trade import cross_border_trade_build_schema_contract  # noqa: E402,F401
from .pbcs.cross_border_trade import cross_border_trade_build_service_contract  # noqa: E402,F401
from .pbcs.cross_border_trade import cross_border_trade_build_workbench_view  # noqa: E402,F401
from .pbcs.cross_border_trade import cross_border_trade_classify_product  # noqa: E402,F401
from .pbcs.cross_border_trade import cross_border_trade_configure_runtime  # noqa: E402,F401
from .pbcs.cross_border_trade import cross_border_trade_empty_state  # noqa: E402,F401
from .pbcs.cross_border_trade import cross_border_trade_file_customs_declaration  # noqa: E402,F401
from .pbcs.cross_border_trade import cross_border_trade_permissions_contract  # noqa: E402,F401
from .pbcs.cross_border_trade import cross_border_trade_quote_landed_cost  # noqa: E402,F401
from .pbcs.cross_border_trade import cross_border_trade_receive_event  # noqa: E402,F401
from .pbcs.cross_border_trade import cross_border_trade_register_rule  # noqa: E402,F401
from .pbcs.cross_border_trade import cross_border_trade_register_schema_extension  # noqa: E402,F401
from .pbcs.cross_border_trade import cross_border_trade_render_workbench  # noqa: E402,F401
from .pbcs.cross_border_trade import cross_border_trade_runtime_capabilities  # noqa: E402,F401
from .pbcs.cross_border_trade import cross_border_trade_runtime_smoke  # noqa: E402,F401
from .pbcs.cross_border_trade import cross_border_trade_screen_export_control  # noqa: E402,F401
from .pbcs.cross_border_trade import cross_border_trade_set_parameter  # noqa: E402,F401
from .pbcs.cross_border_trade import cross_border_trade_ui_contract  # noqa: E402,F401
from .pbcs.cross_border_trade import cross_border_trade_verify_owned_table_boundary  # noqa: E402,F401
from .pbcs.multi_sided_market import MULTI_SIDED_MARKET_ALLOWED_DATABASE_BACKENDS  # noqa: E402,F401
from .pbcs.multi_sided_market import MULTI_SIDED_MARKET_CONSUMED_EVENT_TYPES  # noqa: E402,F401
from .pbcs.multi_sided_market import MULTI_SIDED_MARKET_EMITTED_EVENT_TYPES  # noqa: E402,F401
from .pbcs.multi_sided_market import MULTI_SIDED_MARKET_OWNED_TABLES  # noqa: E402,F401
from .pbcs.multi_sided_market import MULTI_SIDED_MARKET_REQUIRED_EVENT_TOPIC  # noqa: E402,F401
from .pbcs.multi_sided_market import MULTI_SIDED_MARKET_RUNTIME_CAPABILITY_KEYS  # noqa: E402,F401
from .pbcs.multi_sided_market import MULTI_SIDED_MARKET_STANDARD_FEATURE_KEYS  # noqa: E402,F401
from .pbcs.multi_sided_market import multi_sided_market_build_api_contract  # noqa: E402,F401
from .pbcs.multi_sided_market import multi_sided_market_build_release_evidence  # noqa: E402,F401
from .pbcs.multi_sided_market import multi_sided_market_build_schema_contract  # noqa: E402,F401
from .pbcs.multi_sided_market import multi_sided_market_build_service_contract  # noqa: E402,F401
from .pbcs.multi_sided_market import multi_sided_market_build_workbench_view  # noqa: E402,F401
from .pbcs.multi_sided_market import multi_sided_market_configure_runtime  # noqa: E402,F401
from .pbcs.multi_sided_market import multi_sided_market_create_service_offer  # noqa: E402,F401
from .pbcs.multi_sided_market import multi_sided_market_compile_escrow_release_policy  # noqa: E402,F401
from .pbcs.multi_sided_market import multi_sided_market_detect_collusion_anomaly  # noqa: E402,F401
from .pbcs.multi_sided_market import multi_sided_market_empty_state  # noqa: E402,F401
from .pbcs.multi_sided_market import multi_sided_market_execute_sale  # noqa: E402,F401
from .pbcs.multi_sided_market import multi_sided_market_generate_reputation_proof  # noqa: E402,F401
from .pbcs.multi_sided_market import multi_sided_market_issue_loan  # noqa: E402,F401
from .pbcs.multi_sided_market import multi_sided_market_match_barter_offer  # noqa: E402,F401
from .pbcs.multi_sided_market import multi_sided_market_open_dispute  # noqa: E402,F401
from .pbcs.multi_sided_market import multi_sided_market_open_escrow  # noqa: E402,F401
from .pbcs.multi_sided_market import multi_sided_market_optimize_exchange_match  # noqa: E402,F401
from .pbcs.multi_sided_market import multi_sided_market_parse_market_instruction  # noqa: E402,F401
from .pbcs.multi_sided_market import multi_sided_market_permissions_contract  # noqa: E402,F401
from .pbcs.multi_sided_market import multi_sided_market_place_trade_order  # noqa: E402,F401
from .pbcs.multi_sided_market import multi_sided_market_prepare_exchange_proposal  # noqa: E402,F401
from .pbcs.multi_sided_market import multi_sided_market_prepare_settlement  # noqa: E402,F401
from .pbcs.multi_sided_market import multi_sided_market_publish_availability_window  # noqa: E402,F401
from .pbcs.multi_sided_market import multi_sided_market_publish_listing  # noqa: E402,F401
from .pbcs.multi_sided_market import multi_sided_market_publish_market_clearing_projection  # noqa: E402,F401
from .pbcs.multi_sided_market import multi_sided_market_receive_event  # noqa: E402,F401
from .pbcs.multi_sided_market import multi_sided_market_record_reputation_signal  # noqa: E402,F401
from .pbcs.multi_sided_market import multi_sided_market_register_listing_asset  # noqa: E402,F401
from .pbcs.multi_sided_market import multi_sided_market_register_rule  # noqa: E402,F401
from .pbcs.multi_sided_market import multi_sided_market_register_schema_extension  # noqa: E402,F401
from .pbcs.multi_sided_market import multi_sided_market_release_escrow  # noqa: E402,F401
from .pbcs.multi_sided_market import multi_sided_market_render_workbench  # noqa: E402,F401
from .pbcs.multi_sided_market import multi_sided_market_reserve_booking  # noqa: E402,F401
from .pbcs.multi_sided_market import multi_sided_market_resolve_dispute  # noqa: E402,F401
from .pbcs.multi_sided_market import multi_sided_market_runtime_capabilities  # noqa: E402,F401
from .pbcs.multi_sided_market import multi_sided_market_runtime_smoke  # noqa: E402,F401
from .pbcs.multi_sided_market import multi_sided_market_score_reputation  # noqa: E402,F401
from .pbcs.multi_sided_market import multi_sided_market_select_carbon_fulfillment  # noqa: E402,F401
from .pbcs.multi_sided_market import multi_sided_market_set_parameter  # noqa: E402,F401
from .pbcs.multi_sided_market import multi_sided_market_simulate_counterfactual_terms  # noqa: E402,F401
from .pbcs.multi_sided_market import multi_sided_market_start_rental  # noqa: E402,F401
from .pbcs.multi_sided_market import multi_sided_market_ui_contract  # noqa: E402,F401
from .pbcs.multi_sided_market import multi_sided_market_verify_owned_table_boundary  # noqa: E402,F401
from .pbcs.multi_sided_market import multi_sided_market_verify_participant  # noqa: E402,F401
from .pbcs.returns_reverse_logistics import RETURNS_REVERSE_LOGISTICS_ALLOWED_DATABASE_BACKENDS  # noqa: E402,F401
from .pbcs.returns_reverse_logistics import RETURNS_REVERSE_LOGISTICS_OWNED_TABLES  # noqa: E402,F401
from .pbcs.returns_reverse_logistics import RETURNS_REVERSE_LOGISTICS_RUNTIME_CAPABILITY_KEYS  # noqa: E402,F401
from .pbcs.returns_reverse_logistics import RETURNS_REVERSE_LOGISTICS_STANDARD_FEATURE_KEYS  # noqa: E402,F401
from .pbcs.returns_reverse_logistics import RETURNS_REVERSE_LOGISTICS_UI_FRAGMENT_KEYS  # noqa: E402,F401
from .pbcs.returns_reverse_logistics import returns_reverse_logistics_authorize_return  # noqa: E402,F401
from .pbcs.returns_reverse_logistics import returns_reverse_logistics_build_api_contract  # noqa: E402,F401
from .pbcs.returns_reverse_logistics import returns_reverse_logistics_build_release_evidence  # noqa: E402,F401
from .pbcs.returns_reverse_logistics import returns_reverse_logistics_build_schema_contract  # noqa: E402,F401
from .pbcs.returns_reverse_logistics import returns_reverse_logistics_build_service_contract  # noqa: E402,F401
from .pbcs.returns_reverse_logistics import returns_reverse_logistics_build_workbench_view  # noqa: E402,F401
from .pbcs.returns_reverse_logistics import returns_reverse_logistics_configure_runtime  # noqa: E402,F401
from .pbcs.returns_reverse_logistics import returns_reverse_logistics_create_return_label  # noqa: E402,F401
from .pbcs.returns_reverse_logistics import returns_reverse_logistics_empty_state  # noqa: E402,F401
from .pbcs.returns_reverse_logistics import returns_reverse_logistics_issue_credit_adjustment  # noqa: E402,F401
from .pbcs.returns_reverse_logistics import returns_reverse_logistics_permissions_contract  # noqa: E402,F401
from .pbcs.returns_reverse_logistics import returns_reverse_logistics_receive_event  # noqa: E402,F401
from .pbcs.returns_reverse_logistics import returns_reverse_logistics_record_inspection_grade  # noqa: E402,F401
from .pbcs.returns_reverse_logistics import returns_reverse_logistics_register_rule  # noqa: E402,F401
from .pbcs.returns_reverse_logistics import returns_reverse_logistics_register_schema_extension  # noqa: E402,F401
from .pbcs.returns_reverse_logistics import returns_reverse_logistics_render_workbench  # noqa: E402,F401
from .pbcs.returns_reverse_logistics import returns_reverse_logistics_runtime_capabilities  # noqa: E402,F401
from .pbcs.returns_reverse_logistics import returns_reverse_logistics_runtime_smoke  # noqa: E402,F401
from .pbcs.returns_reverse_logistics import returns_reverse_logistics_set_parameter  # noqa: E402,F401
from .pbcs.returns_reverse_logistics import returns_reverse_logistics_ui_contract  # noqa: E402,F401
from .pbcs.returns_reverse_logistics import returns_reverse_logistics_verify_owned_table_boundary  # noqa: E402,F401
from .pbcs.enterprise_pim import ENTERPRISE_PIM_ALLOWED_DATABASE_BACKENDS  # noqa: E402,F401
from .pbcs.enterprise_pim import ENTERPRISE_PIM_CONSUMED_EVENT_TYPES  # noqa: E402,F401
from .pbcs.enterprise_pim import ENTERPRISE_PIM_EMITTED_EVENT_TYPES  # noqa: E402,F401
from .pbcs.enterprise_pim import ENTERPRISE_PIM_OWNED_TABLES  # noqa: E402,F401
from .pbcs.enterprise_pim import ENTERPRISE_PIM_RUNTIME_CAPABILITY_KEYS  # noqa: E402,F401
from .pbcs.enterprise_pim import ENTERPRISE_PIM_STANDARD_FEATURE_KEYS  # noqa: E402,F401
from .pbcs.enterprise_pim import ENTERPRISE_PIM_UI_FRAGMENT_KEYS  # noqa: E402,F401
from .pbcs.enterprise_pim import enterprise_pim_accept_dependency_schema  # noqa: E402,F401
from .pbcs.enterprise_pim import enterprise_pim_approve_validation_workflow  # noqa: E402,F401
from .pbcs.enterprise_pim import enterprise_pim_build_api_contract  # noqa: E402,F401
from .pbcs.enterprise_pim import enterprise_pim_build_release_evidence  # noqa: E402,F401
from .pbcs.enterprise_pim import enterprise_pim_build_schema_contract  # noqa: E402,F401
from .pbcs.enterprise_pim import enterprise_pim_build_service_contract  # noqa: E402,F401
from .pbcs.enterprise_pim import enterprise_pim_build_workbench_view  # noqa: E402,F401
from .pbcs.enterprise_pim import enterprise_pim_configure_runtime  # noqa: E402,F401
from .pbcs.enterprise_pim import enterprise_pim_create_taxonomy  # noqa: E402,F401
from .pbcs.enterprise_pim import enterprise_pim_define_attribute  # noqa: E402,F401
from .pbcs.enterprise_pim import enterprise_pim_empty_state  # noqa: E402,F401
from .pbcs.enterprise_pim import enterprise_pim_permissions_contract  # noqa: E402,F401
from .pbcs.enterprise_pim import enterprise_pim_receive_event  # noqa: E402,F401
from .pbcs.enterprise_pim import enterprise_pim_register_rule  # noqa: E402,F401
from .pbcs.enterprise_pim import enterprise_pim_register_schema_extension  # noqa: E402,F401
from .pbcs.enterprise_pim import enterprise_pim_render_workbench  # noqa: E402,F401
from .pbcs.enterprise_pim import enterprise_pim_runtime_capabilities  # noqa: E402,F401
from .pbcs.enterprise_pim import enterprise_pim_runtime_smoke  # noqa: E402,F401
from .pbcs.enterprise_pim import enterprise_pim_set_parameter  # noqa: E402,F401
from .pbcs.enterprise_pim import enterprise_pim_start_validation_workflow  # noqa: E402,F401
from .pbcs.enterprise_pim import enterprise_pim_ui_contract  # noqa: E402,F401
from .pbcs.enterprise_pim import enterprise_pim_upsert_localized_content  # noqa: E402,F401
from .pbcs.enterprise_pim import enterprise_pim_verify_owned_table_boundary  # noqa: E402,F401
from .pbcs.dam_core import DAM_CORE_RUNTIME_CAPABILITY_KEYS  # noqa: E402,F401
from .pbcs.dam_core import DAM_CORE_STANDARD_FEATURE_KEYS  # noqa: E402,F401
from .pbcs.dam_core import DAM_CORE_UI_FRAGMENT_KEYS  # noqa: E402,F401
from .pbcs.dam_core import dam_core_add_metadata_tag  # noqa: E402,F401
from .pbcs.dam_core import dam_core_attach_rights_policy  # noqa: E402,F401
from .pbcs.dam_core import dam_core_build_api_contract  # noqa: E402,F401
from .pbcs.dam_core import dam_core_build_release_evidence  # noqa: E402,F401
from .pbcs.dam_core import dam_core_build_schema_contract  # noqa: E402,F401
from .pbcs.dam_core import dam_core_build_service_contract  # noqa: E402,F401
from .pbcs.dam_core import dam_core_build_workbench_view  # noqa: E402,F401
from .pbcs.dam_core import dam_core_complete_rendition  # noqa: E402,F401
from .pbcs.dam_core import dam_core_configure_runtime  # noqa: E402,F401
from .pbcs.dam_core import dam_core_empty_state  # noqa: E402,F401
from .pbcs.dam_core import dam_core_enforce_rights  # noqa: E402,F401
from .pbcs.dam_core import dam_core_receive_event  # noqa: E402,F401
from .pbcs.dam_core import dam_core_register_asset  # noqa: E402,F401
from .pbcs.dam_core import dam_core_register_rule  # noqa: E402,F401
from .pbcs.dam_core import dam_core_register_schema_extension  # noqa: E402,F401
from .pbcs.dam_core import dam_core_render_workbench  # noqa: E402,F401
from .pbcs.dam_core import dam_core_request_rendition  # noqa: E402,F401
from .pbcs.dam_core import dam_core_runtime_capabilities  # noqa: E402,F401
from .pbcs.dam_core import dam_core_runtime_smoke  # noqa: E402,F401
from .pbcs.dam_core import dam_core_set_parameter  # noqa: E402,F401
from .pbcs.dam_core import dam_core_ui_contract  # noqa: E402,F401
from .pbcs.dam_core import dam_core_verify_owned_table_boundary  # noqa: E402,F401
from .pbcs.price_promotion_engine import PRICE_PROMOTION_ENGINE_RUNTIME_CAPABILITY_KEYS  # noqa: E402,F401
from .pbcs.price_promotion_engine import PRICE_PROMOTION_ENGINE_STANDARD_FEATURE_KEYS  # noqa: E402,F401
from .pbcs.price_promotion_engine import PRICE_PROMOTION_ENGINE_UI_FRAGMENT_KEYS  # noqa: E402,F401
from .pbcs.price_promotion_engine import price_promotion_engine_apply_promotion  # noqa: E402,F401
from .pbcs.price_promotion_engine import price_promotion_engine_approve_promotion  # noqa: E402,F401
from .pbcs.price_promotion_engine import price_promotion_engine_build_api_contract  # noqa: E402,F401
from .pbcs.price_promotion_engine import price_promotion_engine_build_release_evidence  # noqa: E402,F401
from .pbcs.price_promotion_engine import price_promotion_engine_build_schema_contract  # noqa: E402,F401
from .pbcs.price_promotion_engine import price_promotion_engine_build_service_contract  # noqa: E402,F401
from .pbcs.price_promotion_engine import price_promotion_engine_build_workbench_view  # noqa: E402,F401
from .pbcs.price_promotion_engine import price_promotion_engine_configure_runtime  # noqa: E402,F401
from .pbcs.price_promotion_engine import price_promotion_engine_empty_state  # noqa: E402,F401
from .pbcs.price_promotion_engine import price_promotion_engine_permissions_contract  # noqa: E402,F401
from .pbcs.price_promotion_engine import price_promotion_engine_quote_price  # noqa: E402,F401
from .pbcs.price_promotion_engine import price_promotion_engine_receive_event  # noqa: E402,F401
from .pbcs.price_promotion_engine import price_promotion_engine_redeem_coupon  # noqa: E402,F401
from .pbcs.price_promotion_engine import price_promotion_engine_register_loyalty_tier  # noqa: E402,F401
from .pbcs.price_promotion_engine import price_promotion_engine_register_price_rule  # noqa: E402,F401
from .pbcs.price_promotion_engine import price_promotion_engine_register_promotion  # noqa: E402,F401
from .pbcs.price_promotion_engine import price_promotion_engine_register_rule  # noqa: E402,F401
from .pbcs.price_promotion_engine import price_promotion_engine_render_workbench  # noqa: E402,F401
from .pbcs.price_promotion_engine import price_promotion_engine_runtime_capabilities  # noqa: E402,F401
from .pbcs.price_promotion_engine import price_promotion_engine_runtime_smoke  # noqa: E402,F401
from .pbcs.price_promotion_engine import price_promotion_engine_set_parameter  # noqa: E402,F401
from .pbcs.price_promotion_engine import price_promotion_engine_ui_contract  # noqa: E402,F401
from .pbcs.price_promotion_engine import price_promotion_engine_verify_owned_table_boundary  # noqa: E402,F401
from .pbcs.lead_opportunity import LEAD_OPPORTUNITY_RUNTIME_CAPABILITY_KEYS  # noqa: E402,F401
from .pbcs.lead_opportunity import LEAD_OPPORTUNITY_STANDARD_FEATURE_KEYS  # noqa: E402,F401
from .pbcs.lead_opportunity import LEAD_OPPORTUNITY_UI_FRAGMENT_KEYS  # noqa: E402,F401
from .pbcs.lead_opportunity import lead_opportunity_advance_opportunity  # noqa: E402,F401
from .pbcs.lead_opportunity import lead_opportunity_build_api_contract  # noqa: E402,F401
from .pbcs.lead_opportunity import lead_opportunity_build_release_evidence  # noqa: E402,F401
from .pbcs.lead_opportunity import lead_opportunity_build_schema_contract  # noqa: E402,F401
from .pbcs.lead_opportunity import lead_opportunity_build_service_contract  # noqa: E402,F401
from .pbcs.lead_opportunity import lead_opportunity_build_workbench_view  # noqa: E402,F401
from .pbcs.lead_opportunity import lead_opportunity_configure_runtime  # noqa: E402,F401
from .pbcs.lead_opportunity import lead_opportunity_create_account_hierarchy  # noqa: E402,F401
from .pbcs.lead_opportunity import lead_opportunity_create_lead  # noqa: E402,F401
from .pbcs.lead_opportunity import lead_opportunity_create_opportunity  # noqa: E402,F401
from .pbcs.lead_opportunity import lead_opportunity_empty_state  # noqa: E402,F401
from .pbcs.lead_opportunity import lead_opportunity_permissions_contract  # noqa: E402,F401
from .pbcs.lead_opportunity import lead_opportunity_qualify_lead  # noqa: E402,F401
from .pbcs.lead_opportunity import lead_opportunity_receive_event  # noqa: E402,F401
from .pbcs.lead_opportunity import lead_opportunity_record_sales_activity  # noqa: E402,F401
from .pbcs.lead_opportunity import lead_opportunity_register_rule  # noqa: E402,F401
from .pbcs.lead_opportunity import lead_opportunity_register_schema_extension  # noqa: E402,F401
from .pbcs.lead_opportunity import lead_opportunity_render_workbench  # noqa: E402,F401
from .pbcs.lead_opportunity import lead_opportunity_runtime_capabilities  # noqa: E402,F401
from .pbcs.lead_opportunity import lead_opportunity_runtime_smoke  # noqa: E402,F401
from .pbcs.lead_opportunity import lead_opportunity_set_parameter  # noqa: E402,F401
from .pbcs.lead_opportunity import lead_opportunity_ui_contract  # noqa: E402,F401
from .pbcs.lead_opportunity import lead_opportunity_verify_owned_table_boundary  # noqa: E402,F401
from .pbcs.lead_opportunity import lead_opportunity_win_opportunity  # noqa: E402,F401
from .pbcs.service_ticketing import SERVICE_TICKETING_RUNTIME_CAPABILITY_KEYS  # noqa: E402,F401
from .pbcs.service_ticketing import SERVICE_TICKETING_STANDARD_FEATURE_KEYS  # noqa: E402,F401
from .pbcs.service_ticketing import SERVICE_TICKETING_UI_FRAGMENT_KEYS  # noqa: E402,F401
from .pbcs.service_ticketing import service_ticketing_assign_ticket  # noqa: E402,F401
from .pbcs.service_ticketing import service_ticketing_build_api_contract  # noqa: E402,F401
from .pbcs.service_ticketing import service_ticketing_build_release_evidence  # noqa: E402,F401
from .pbcs.service_ticketing import service_ticketing_build_schema_contract  # noqa: E402,F401
from .pbcs.service_ticketing import service_ticketing_build_service_contract  # noqa: E402,F401
from .pbcs.service_ticketing import service_ticketing_build_workbench_view  # noqa: E402,F401
from .pbcs.service_ticketing import service_ticketing_configure_runtime  # noqa: E402,F401
from .pbcs.service_ticketing import service_ticketing_create_sla_policy  # noqa: E402,F401
from .pbcs.service_ticketing import service_ticketing_empty_state  # noqa: E402,F401
from .pbcs.service_ticketing import service_ticketing_open_ticket  # noqa: E402,F401
from .pbcs.service_ticketing import service_ticketing_permissions_contract  # noqa: E402,F401
from .pbcs.service_ticketing import service_ticketing_receive_event  # noqa: E402,F401
from .pbcs.service_ticketing import service_ticketing_record_escalation  # noqa: E402,F401
from .pbcs.service_ticketing import service_ticketing_register_rule  # noqa: E402,F401
from .pbcs.service_ticketing import service_ticketing_register_schema_extension  # noqa: E402,F401
from .pbcs.service_ticketing import service_ticketing_render_workbench  # noqa: E402,F401
from .pbcs.service_ticketing import service_ticketing_resolve_ticket  # noqa: E402,F401
from .pbcs.service_ticketing import service_ticketing_runtime_capabilities  # noqa: E402,F401
from .pbcs.service_ticketing import service_ticketing_runtime_smoke  # noqa: E402,F401
from .pbcs.service_ticketing import service_ticketing_set_parameter  # noqa: E402,F401
from .pbcs.service_ticketing import service_ticketing_ui_contract  # noqa: E402,F401
from .pbcs.service_ticketing import service_ticketing_verify_owned_table_boundary  # noqa: E402,F401
PBC_CATALOG["service_ticketing"].update(
    {
        "apis": tuple(route["route"] for route in service_ticketing_build_api_contract()["routes"]),
    }
)
from .pbcs.notifications import NOTIFICATIONS_RUNTIME_CAPABILITY_KEYS  # noqa: E402,F401
from .pbcs.notifications import NOTIFICATIONS_STANDARD_FEATURE_KEYS  # noqa: E402,F401
from .pbcs.notifications import NOTIFICATIONS_UI_FRAGMENT_KEYS  # noqa: E402,F401
from .pbcs.notifications import notifications_build_api_contract  # noqa: E402,F401
from .pbcs.notifications import notifications_build_release_evidence  # noqa: E402,F401
from .pbcs.notifications import notifications_build_schema_contract  # noqa: E402,F401
from .pbcs.notifications import notifications_build_service_contract  # noqa: E402,F401
from .pbcs.notifications import notifications_build_workbench_view  # noqa: E402,F401
from .pbcs.notifications import notifications_configure_runtime  # noqa: E402,F401
from .pbcs.notifications import notifications_empty_state  # noqa: E402,F401
from .pbcs.notifications import notifications_permissions_contract  # noqa: E402,F401
from .pbcs.notifications import notifications_receive_event  # noqa: E402,F401
from .pbcs.notifications import notifications_record_delivery_attempt  # noqa: E402,F401
from .pbcs.notifications import notifications_register_channel  # noqa: E402,F401
from .pbcs.notifications import notifications_register_rule  # noqa: E402,F401
from .pbcs.notifications import notifications_register_schema_extension  # noqa: E402,F401
from .pbcs.notifications import notifications_register_template  # noqa: E402,F401
from .pbcs.notifications import notifications_render_workbench  # noqa: E402,F401
from .pbcs.notifications import notifications_runtime_capabilities  # noqa: E402,F401
from .pbcs.notifications import notifications_runtime_smoke  # noqa: E402,F401
from .pbcs.notifications import notifications_send_message  # noqa: E402,F401
from .pbcs.notifications import notifications_set_parameter  # noqa: E402,F401
from .pbcs.notifications import notifications_ui_contract  # noqa: E402,F401
from .pbcs.notifications import notifications_verify_owned_table_boundary  # noqa: E402,F401
PBC_CATALOG["notifications"].update(
    {
        "apis": tuple(route["route"] for route in notifications_build_api_contract()["routes"]),
    }
)
from .pbcs.cdp_segmentation import CDP_SEGMENTATION_RUNTIME_CAPABILITY_KEYS  # noqa: E402,F401
from .pbcs.cdp_segmentation import CDP_SEGMENTATION_STANDARD_FEATURE_KEYS  # noqa: E402,F401
from .pbcs.cdp_segmentation import CDP_SEGMENTATION_UI_FRAGMENT_KEYS  # noqa: E402,F401
from .pbcs.cdp_segmentation import cdp_segmentation_activate_segment  # noqa: E402,F401
from .pbcs.cdp_segmentation import cdp_segmentation_build_api_contract  # noqa: E402,F401
from .pbcs.cdp_segmentation import cdp_segmentation_build_release_evidence  # noqa: E402,F401
from .pbcs.cdp_segmentation import cdp_segmentation_build_schema_contract  # noqa: E402,F401
from .pbcs.cdp_segmentation import cdp_segmentation_build_service_contract  # noqa: E402,F401
from .pbcs.cdp_segmentation import cdp_segmentation_build_workbench_view  # noqa: E402,F401
from .pbcs.cdp_segmentation import cdp_segmentation_configure_runtime  # noqa: E402,F401
from .pbcs.cdp_segmentation import cdp_segmentation_define_segment  # noqa: E402,F401
from .pbcs.cdp_segmentation import cdp_segmentation_empty_state  # noqa: E402,F401
from .pbcs.cdp_segmentation import cdp_segmentation_evaluate_segments  # noqa: E402,F401
from .pbcs.cdp_segmentation import cdp_segmentation_ingest_customer_event  # noqa: E402,F401
from .pbcs.cdp_segmentation import cdp_segmentation_permissions_contract  # noqa: E402,F401
from .pbcs.cdp_segmentation import cdp_segmentation_receive_event  # noqa: E402,F401
from .pbcs.cdp_segmentation import cdp_segmentation_register_rule  # noqa: E402,F401
from .pbcs.cdp_segmentation import cdp_segmentation_register_schema_extension  # noqa: E402,F401
from .pbcs.cdp_segmentation import cdp_segmentation_render_workbench  # noqa: E402,F401
from .pbcs.cdp_segmentation import cdp_segmentation_runtime_capabilities  # noqa: E402,F401
from .pbcs.cdp_segmentation import cdp_segmentation_runtime_smoke  # noqa: E402,F401
from .pbcs.cdp_segmentation import cdp_segmentation_set_parameter  # noqa: E402,F401
from .pbcs.cdp_segmentation import cdp_segmentation_ui_contract  # noqa: E402,F401
from .pbcs.cdp_segmentation import cdp_segmentation_upsert_profile_property  # noqa: E402,F401
from .pbcs.cdp_segmentation import cdp_segmentation_verify_owned_table_boundary  # noqa: E402,F401
PBC_CATALOG["cdp_segmentation"].update(
    {
        "apis": tuple(route["route"] for route in cdp_segmentation_build_api_contract()["routes"]),
    }
)
from .pbcs.loyalty_rewards import LOYALTY_REWARDS_RUNTIME_CAPABILITY_KEYS  # noqa: E402,F401
from .pbcs.loyalty_rewards import LOYALTY_REWARDS_RUNTIME_TABLES  # noqa: E402,F401
from .pbcs.loyalty_rewards import LOYALTY_REWARDS_STANDARD_FEATURE_KEYS  # noqa: E402,F401
from .pbcs.loyalty_rewards import LOYALTY_REWARDS_UI_FRAGMENT_KEYS  # noqa: E402,F401
from .pbcs.loyalty_rewards import loyalty_rewards_adjust_points  # noqa: E402,F401
from .pbcs.loyalty_rewards import loyalty_rewards_build_api_contract  # noqa: E402,F401
from .pbcs.loyalty_rewards import loyalty_rewards_build_release_evidence  # noqa: E402,F401
from .pbcs.loyalty_rewards import loyalty_rewards_build_schema_contract  # noqa: E402,F401
from .pbcs.loyalty_rewards import loyalty_rewards_build_service_contract  # noqa: E402,F401
from .pbcs.loyalty_rewards import loyalty_rewards_build_workbench_view  # noqa: E402,F401
from .pbcs.loyalty_rewards import loyalty_rewards_configure_runtime  # noqa: E402,F401
from .pbcs.loyalty_rewards import loyalty_rewards_create_redemption  # noqa: E402,F401
from .pbcs.loyalty_rewards import loyalty_rewards_empty_state  # noqa: E402,F401
from .pbcs.loyalty_rewards import loyalty_rewards_enroll_member  # noqa: E402,F401
from .pbcs.loyalty_rewards import loyalty_rewards_expire_points  # noqa: E402,F401
from .pbcs.loyalty_rewards import loyalty_rewards_issue_points  # noqa: E402,F401
from .pbcs.loyalty_rewards import loyalty_rewards_permissions_contract  # noqa: E402,F401
from .pbcs.loyalty_rewards import loyalty_rewards_receive_event  # noqa: E402,F401
from .pbcs.loyalty_rewards import loyalty_rewards_register_earning_rule  # noqa: E402,F401
from .pbcs.loyalty_rewards import loyalty_rewards_register_rule  # noqa: E402,F401
from .pbcs.loyalty_rewards import loyalty_rewards_register_schema_extension  # noqa: E402,F401
from .pbcs.loyalty_rewards import loyalty_rewards_render_workbench  # noqa: E402,F401
from .pbcs.loyalty_rewards import loyalty_rewards_runtime_capabilities  # noqa: E402,F401
from .pbcs.loyalty_rewards import loyalty_rewards_runtime_smoke  # noqa: E402,F401
from .pbcs.loyalty_rewards import loyalty_rewards_set_parameter  # noqa: E402,F401
from .pbcs.loyalty_rewards import loyalty_rewards_ui_contract  # noqa: E402,F401
from .pbcs.loyalty_rewards import loyalty_rewards_verify_owned_table_boundary  # noqa: E402,F401
PBC_CATALOG["loyalty_rewards"].update(
    {
        "apis": tuple(route["route"] for route in loyalty_rewards_build_api_contract()["routes"]),
    }
)
from .pbcs.streaming_analytics import STREAMING_ANALYTICS_RUNTIME_CAPABILITY_KEYS  # noqa: E402,F401
from .pbcs.streaming_analytics import STREAMING_ANALYTICS_RUNTIME_TABLES  # noqa: E402,F401
from .pbcs.streaming_analytics import STREAMING_ANALYTICS_STANDARD_FEATURE_KEYS  # noqa: E402,F401
from .pbcs.streaming_analytics import STREAMING_ANALYTICS_UI_FRAGMENT_KEYS  # noqa: E402,F401
from .pbcs.streaming_analytics import streaming_analytics_build_api_contract  # noqa: E402,F401
from .pbcs.streaming_analytics import streaming_analytics_build_analytics_federation_view  # noqa: E402,F401
from .pbcs.streaming_analytics import streaming_analytics_build_release_evidence  # noqa: E402,F401
from .pbcs.streaming_analytics import streaming_analytics_build_schema_contract  # noqa: E402,F401
from .pbcs.streaming_analytics import streaming_analytics_build_service_contract  # noqa: E402,F401
from .pbcs.streaming_analytics import streaming_analytics_build_workbench_view  # noqa: E402,F401
from .pbcs.streaming_analytics import streaming_analytics_advance_watermark  # noqa: E402,F401
from .pbcs.streaming_analytics import streaming_analytics_apply_retention_policy  # noqa: E402,F401
from .pbcs.streaming_analytics import streaming_analytics_configure_runtime  # noqa: E402,F401
from .pbcs.streaming_analytics import streaming_analytics_create_dashboard_projection  # noqa: E402,F401
from .pbcs.streaming_analytics import streaming_analytics_define_window  # noqa: E402,F401
from .pbcs.streaming_analytics import streaming_analytics_empty_state  # noqa: E402,F401
from .pbcs.streaming_analytics import streaming_analytics_evaluate_data_quality  # noqa: E402,F401
from .pbcs.streaming_analytics import streaming_analytics_evaluate_threshold_alert  # noqa: E402,F401
from .pbcs.streaming_analytics import streaming_analytics_forecast_metric  # noqa: E402,F401
from .pbcs.streaming_analytics import streaming_analytics_generate_snapshot_proof  # noqa: E402,F401
from .pbcs.streaming_analytics import streaming_analytics_ingest_metric_event  # noqa: E402,F401
from .pbcs.streaming_analytics import streaming_analytics_open_replay_job  # noqa: E402,F401
from .pbcs.streaming_analytics import streaming_analytics_permissions_contract  # noqa: E402,F401
from .pbcs.streaming_analytics import streaming_analytics_receive_event  # noqa: E402,F401
from .pbcs.streaming_analytics import streaming_analytics_recompute_window  # noqa: E402,F401
from .pbcs.streaming_analytics import streaming_analytics_record_ingestion_checkpoint  # noqa: E402,F401
from .pbcs.streaming_analytics import streaming_analytics_register_metric_stream  # noqa: E402,F401
from .pbcs.streaming_analytics import streaming_analytics_register_governed_model  # noqa: E402,F401
from .pbcs.streaming_analytics import streaming_analytics_register_rule  # noqa: E402,F401
from .pbcs.streaming_analytics import streaming_analytics_register_schema_extension  # noqa: E402,F401
from .pbcs.streaming_analytics import streaming_analytics_render_workbench  # noqa: E402,F401
from .pbcs.streaming_analytics import streaming_analytics_resolve_metric_exception  # noqa: E402,F401
from .pbcs.streaming_analytics import streaming_analytics_run_kpi_controls  # noqa: E402,F401
from .pbcs.streaming_analytics import streaming_analytics_runtime_capabilities  # noqa: E402,F401
from .pbcs.streaming_analytics import streaming_analytics_runtime_smoke  # noqa: E402,F401
from .pbcs.streaming_analytics import streaming_analytics_score_operational_risk  # noqa: E402,F401
from .pbcs.streaming_analytics import streaming_analytics_screen_metric_policy  # noqa: E402,F401
from .pbcs.streaming_analytics import streaming_analytics_set_parameter  # noqa: E402,F401
from .pbcs.streaming_analytics import streaming_analytics_ui_contract  # noqa: E402,F401
from .pbcs.streaming_analytics import streaming_analytics_verify_owned_table_boundary  # noqa: E402,F401
PBC_CATALOG["streaming_analytics"].update(
    {
        "apis": tuple(route["route"] for route in streaming_analytics_build_api_contract()["routes"]),
    }
)
from .pbcs.enterprise_search_vector import ENTERPRISE_SEARCH_VECTOR_RUNTIME_CAPABILITY_KEYS  # noqa: E402,F401
from .pbcs.enterprise_search_vector import ENTERPRISE_SEARCH_VECTOR_RUNTIME_TABLES  # noqa: E402,F401
from .pbcs.enterprise_search_vector import ENTERPRISE_SEARCH_VECTOR_STANDARD_FEATURE_KEYS  # noqa: E402,F401
from .pbcs.enterprise_search_vector import ENTERPRISE_SEARCH_VECTOR_UI_FRAGMENT_KEYS  # noqa: E402,F401
from .pbcs.enterprise_search_vector import enterprise_search_vector_build_api_contract  # noqa: E402,F401
from .pbcs.enterprise_search_vector import enterprise_search_vector_build_release_evidence  # noqa: E402,F401
from .pbcs.enterprise_search_vector import enterprise_search_vector_build_schema_contract  # noqa: E402,F401
from .pbcs.enterprise_search_vector import enterprise_search_vector_build_service_contract  # noqa: E402,F401
from .pbcs.enterprise_search_vector import enterprise_search_vector_build_workbench_view  # noqa: E402,F401
from .pbcs.enterprise_search_vector import enterprise_search_vector_configure_runtime  # noqa: E402,F401
from .pbcs.enterprise_search_vector import enterprise_search_vector_create_index  # noqa: E402,F401
from .pbcs.enterprise_search_vector import enterprise_search_vector_empty_state  # noqa: E402,F401
from .pbcs.enterprise_search_vector import enterprise_search_vector_ingest_document  # noqa: E402,F401
from .pbcs.enterprise_search_vector import enterprise_search_vector_permissions_contract  # noqa: E402,F401
from .pbcs.enterprise_search_vector import enterprise_search_vector_query  # noqa: E402,F401
from .pbcs.enterprise_search_vector import enterprise_search_vector_receive_event  # noqa: E402,F401
from .pbcs.enterprise_search_vector import enterprise_search_vector_refresh_index  # noqa: E402,F401
from .pbcs.enterprise_search_vector import enterprise_search_vector_record_feedback  # noqa: E402,F401
from .pbcs.enterprise_search_vector import enterprise_search_vector_register_rule  # noqa: E402,F401
from .pbcs.enterprise_search_vector import enterprise_search_vector_register_schema_extension  # noqa: E402,F401
from .pbcs.enterprise_search_vector import enterprise_search_vector_render_workbench  # noqa: E402,F401
from .pbcs.enterprise_search_vector import enterprise_search_vector_run_embedding_job  # noqa: E402,F401
from .pbcs.enterprise_search_vector import enterprise_search_vector_runtime_capabilities  # noqa: E402,F401
from .pbcs.enterprise_search_vector import enterprise_search_vector_runtime_smoke  # noqa: E402,F401
from .pbcs.enterprise_search_vector import enterprise_search_vector_set_parameter  # noqa: E402,F401
from .pbcs.enterprise_search_vector import enterprise_search_vector_ui_contract  # noqa: E402,F401
from .pbcs.enterprise_search_vector import enterprise_search_vector_verify_owned_table_boundary  # noqa: E402,F401
PBC_CATALOG["enterprise_search_vector"].update(
    {
        "apis": (
            "POST /indexes",
            "POST /indexes/{id}/refresh",
            "POST /documents",
            "POST /embeddings",
            "POST /search",
            "POST /query-feedback",
            "POST /ranking-simulations",
            "POST /freshness-forecasts",
            "POST /quality-remediations",
            "POST /policy-screenings",
            "POST /relevance-controls",
            "POST /index-proofs",
            "POST /federated-source-views",
            "POST /query-intent-risks",
            "POST /retention-deletions",
            "POST /governed-models",
            "POST /enterprise-search-vector/events/inbox",
            "GET /query-traces",
            "GET /enterprise-search-vector-workbench",
            "GET /enterprise-search-vector/schema-contract",
            "GET /enterprise-search-vector/service-contract",
            "GET /enterprise-search-vector/release-evidence",
        ),
    }
)
from .pbcs.predictive_demand import PREDICTIVE_DEMAND_RUNTIME_CAPABILITY_KEYS  # noqa: E402,F401
from .pbcs.predictive_demand import PREDICTIVE_DEMAND_RUNTIME_TABLES  # noqa: E402,F401
from .pbcs.predictive_demand import PREDICTIVE_DEMAND_STANDARD_FEATURE_KEYS  # noqa: E402,F401
from .pbcs.predictive_demand import PREDICTIVE_DEMAND_UI_FRAGMENT_KEYS  # noqa: E402,F401
from .pbcs.predictive_demand import predictive_demand_build_api_contract  # noqa: E402,F401
from .pbcs.predictive_demand import predictive_demand_build_release_evidence  # noqa: E402,F401
from .pbcs.predictive_demand import predictive_demand_build_schema_contract  # noqa: E402,F401
from .pbcs.predictive_demand import predictive_demand_build_service_contract  # noqa: E402,F401
from .pbcs.predictive_demand import predictive_demand_build_workbench_view  # noqa: E402,F401
from .pbcs.predictive_demand import predictive_demand_assess_shortage_risk  # noqa: E402,F401
from .pbcs.predictive_demand import predictive_demand_configure_runtime  # noqa: E402,F401
from .pbcs.predictive_demand import predictive_demand_create_forecast_run  # noqa: E402,F401
from .pbcs.predictive_demand import predictive_demand_create_scenario_version  # noqa: E402,F401
from .pbcs.predictive_demand import predictive_demand_empty_state  # noqa: E402,F401
from .pbcs.predictive_demand import predictive_demand_ingest_demand_signal  # noqa: E402,F401
from .pbcs.predictive_demand import predictive_demand_open_forecast_exception  # noqa: E402,F401
from .pbcs.predictive_demand import predictive_demand_permissions_contract  # noqa: E402,F401
from .pbcs.predictive_demand import predictive_demand_prepare_replenishment_recommendation  # noqa: E402,F401
from .pbcs.predictive_demand import predictive_demand_publish_forecast_result  # noqa: E402,F401
from .pbcs.predictive_demand import predictive_demand_receive_event  # noqa: E402,F401
from .pbcs.predictive_demand import predictive_demand_record_consensus_adjustment  # noqa: E402,F401
from .pbcs.predictive_demand import predictive_demand_record_model_drift_signal  # noqa: E402,F401
from .pbcs.predictive_demand import predictive_demand_register_forecast_model  # noqa: E402,F401
from .pbcs.predictive_demand import predictive_demand_register_forecast_driver  # noqa: E402,F401
from .pbcs.predictive_demand import predictive_demand_register_governed_model_evidence  # noqa: E402,F401
from .pbcs.predictive_demand import predictive_demand_register_planning_horizon  # noqa: E402,F401
from .pbcs.predictive_demand import predictive_demand_register_rule  # noqa: E402,F401
from .pbcs.predictive_demand import predictive_demand_register_schema_extension  # noqa: E402,F401
from .pbcs.predictive_demand import predictive_demand_render_workbench  # noqa: E402,F401
from .pbcs.predictive_demand import predictive_demand_resolve_forecast_exception  # noqa: E402,F401
from .pbcs.predictive_demand import predictive_demand_runtime_capabilities  # noqa: E402,F401
from .pbcs.predictive_demand import predictive_demand_runtime_smoke  # noqa: E402,F401
from .pbcs.predictive_demand import predictive_demand_seal_forecast_audit_proof  # noqa: E402,F401
from .pbcs.predictive_demand import predictive_demand_set_parameter  # noqa: E402,F401
from .pbcs.predictive_demand import predictive_demand_ui_contract  # noqa: E402,F401
from .pbcs.predictive_demand import predictive_demand_verify_owned_table_boundary  # noqa: E402,F401
from .pbcs.fraud_anomaly_detection import FRAUD_ANOMALY_DETECTION_RUNTIME_CAPABILITY_KEYS  # noqa: E402,F401
from .pbcs.fraud_anomaly_detection import FRAUD_ANOMALY_DETECTION_RUNTIME_TABLES  # noqa: E402,F401
from .pbcs.fraud_anomaly_detection import FRAUD_ANOMALY_DETECTION_STANDARD_FEATURE_KEYS  # noqa: E402,F401
from .pbcs.fraud_anomaly_detection import FRAUD_ANOMALY_DETECTION_UI_FRAGMENT_KEYS  # noqa: E402,F401
from .pbcs.fraud_anomaly_detection import fraud_anomaly_detection_build_api_contract  # noqa: E402,F401
from .pbcs.fraud_anomaly_detection import fraud_anomaly_detection_build_release_evidence  # noqa: E402,F401
from .pbcs.fraud_anomaly_detection import fraud_anomaly_detection_build_schema_contract  # noqa: E402,F401
from .pbcs.fraud_anomaly_detection import fraud_anomaly_detection_build_service_contract  # noqa: E402,F401
from .pbcs.fraud_anomaly_detection import fraud_anomaly_detection_build_workbench_view  # noqa: E402,F401
from .pbcs.fraud_anomaly_detection import fraud_anomaly_detection_calculate_velocity_window  # noqa: E402,F401
from .pbcs.fraud_anomaly_detection import fraud_anomaly_detection_configure_runtime  # noqa: E402,F401
from .pbcs.fraud_anomaly_detection import fraud_anomaly_detection_empty_state  # noqa: E402,F401
from .pbcs.fraud_anomaly_detection import fraud_anomaly_detection_enqueue_analyst_case  # noqa: E402,F401
from .pbcs.fraud_anomaly_detection import fraud_anomaly_detection_explain_decision  # noqa: E402,F401
from .pbcs.fraud_anomaly_detection import fraud_anomaly_detection_ingest_risk_signal  # noqa: E402,F401
from .pbcs.fraud_anomaly_detection import fraud_anomaly_detection_link_identity  # noqa: E402,F401
from .pbcs.fraud_anomaly_detection import fraud_anomaly_detection_open_risk_case  # noqa: E402,F401
from .pbcs.fraud_anomaly_detection import fraud_anomaly_detection_permissions_contract  # noqa: E402,F401
from .pbcs.fraud_anomaly_detection import fraud_anomaly_detection_project_loss_exposure  # noqa: E402,F401
from .pbcs.fraud_anomaly_detection import fraud_anomaly_detection_receive_event  # noqa: E402,F401
from .pbcs.fraud_anomaly_detection import fraud_anomaly_detection_record_device_fingerprint  # noqa: E402,F401
from .pbcs.fraud_anomaly_detection import fraud_anomaly_detection_record_network_indicator  # noqa: E402,F401
from .pbcs.fraud_anomaly_detection import fraud_anomaly_detection_register_fraud_rule  # noqa: E402,F401
from .pbcs.fraud_anomaly_detection import fraud_anomaly_detection_register_rule  # noqa: E402,F401
from .pbcs.fraud_anomaly_detection import fraud_anomaly_detection_register_schema_extension  # noqa: E402,F401
from .pbcs.fraud_anomaly_detection import fraud_anomaly_detection_render_workbench  # noqa: E402,F401
from .pbcs.fraud_anomaly_detection import fraud_anomaly_detection_runtime_capabilities  # noqa: E402,F401
from .pbcs.fraud_anomaly_detection import fraud_anomaly_detection_runtime_smoke  # noqa: E402,F401
from .pbcs.fraud_anomaly_detection import fraud_anomaly_detection_score_anomaly  # noqa: E402,F401
from .pbcs.fraud_anomaly_detection import fraud_anomaly_detection_set_parameter  # noqa: E402,F401
from .pbcs.fraud_anomaly_detection import fraud_anomaly_detection_ui_contract  # noqa: E402,F401
from .pbcs.fraud_anomaly_detection import fraud_anomaly_detection_update_behavior_baseline  # noqa: E402,F401
from .pbcs.fraud_anomaly_detection import fraud_anomaly_detection_verify_owned_table_boundary  # noqa: E402,F401
from .pbcs.federated_iam import FEDERATED_IAM_ALLOWED_DATABASE_BACKENDS  # noqa: E402,F401
from .pbcs.federated_iam import FEDERATED_IAM_CONSUMED_EVENT_TYPES  # noqa: E402,F401
from .pbcs.federated_iam import FEDERATED_IAM_EMITTED_EVENT_TYPES  # noqa: E402,F401
from .pbcs.federated_iam import FEDERATED_IAM_OWNED_TABLES  # noqa: E402,F401
from .pbcs.federated_iam import FEDERATED_IAM_REQUIRED_EVENT_TOPIC  # noqa: E402,F401
from .pbcs.federated_iam import FEDERATED_IAM_RUNTIME_CAPABILITY_KEYS  # noqa: E402,F401
from .pbcs.federated_iam import FEDERATED_IAM_STANDARD_FEATURE_KEYS  # noqa: E402,F401
from .pbcs.federated_iam import FEDERATED_IAM_UI_FRAGMENT_KEYS  # noqa: E402,F401
from .pbcs.federated_iam import federated_iam_approve_privileged_access  # noqa: E402,F401
from .pbcs.federated_iam import federated_iam_assign_role  # noqa: E402,F401
from .pbcs.federated_iam import federated_iam_build_api_contract  # noqa: E402,F401
from .pbcs.federated_iam import federated_iam_build_release_evidence  # noqa: E402,F401
from .pbcs.federated_iam import federated_iam_build_schema_contract  # noqa: E402,F401
from .pbcs.federated_iam import federated_iam_build_service_contract  # noqa: E402,F401
from .pbcs.federated_iam import federated_iam_build_workbench_view  # noqa: E402,F401
from .pbcs.federated_iam import federated_iam_configure_runtime  # noqa: E402,F401
from .pbcs.federated_iam import federated_iam_empty_state  # noqa: E402,F401
from .pbcs.federated_iam import federated_iam_evaluate_policy  # noqa: E402,F401
from .pbcs.federated_iam import federated_iam_grant_token  # noqa: E402,F401
from .pbcs.federated_iam import federated_iam_link_identity  # noqa: E402,F401
from .pbcs.federated_iam import federated_iam_permissions_contract  # noqa: E402,F401
from .pbcs.federated_iam import federated_iam_provision_tenant  # noqa: E402,F401
from .pbcs.federated_iam import federated_iam_receive_event  # noqa: E402,F401
from .pbcs.federated_iam import federated_iam_register_identity_provider  # noqa: E402,F401
from .pbcs.federated_iam import federated_iam_register_principal  # noqa: E402,F401
from .pbcs.federated_iam import federated_iam_register_rule  # noqa: E402,F401
from .pbcs.federated_iam import federated_iam_register_schema_extension  # noqa: E402,F401
from .pbcs.federated_iam import federated_iam_render_workbench  # noqa: E402,F401
from .pbcs.federated_iam import federated_iam_runtime_capabilities  # noqa: E402,F401
from .pbcs.federated_iam import federated_iam_runtime_smoke  # noqa: E402,F401
from .pbcs.federated_iam import federated_iam_set_parameter  # noqa: E402,F401
from .pbcs.federated_iam import federated_iam_ui_contract  # noqa: E402,F401
from .pbcs.federated_iam import federated_iam_verify_owned_table_boundary  # noqa: E402,F401
from .pbcs.federated_iam import federated_iam_verify_credential  # noqa: E402,F401
from .pbcs.api_gateway_mesh import API_GATEWAY_MESH_ALLOWED_DATABASE_BACKENDS  # noqa: E402,F401
from .pbcs.api_gateway_mesh import API_GATEWAY_MESH_CONSUMED_EVENT_TYPES  # noqa: E402,F401
from .pbcs.api_gateway_mesh import API_GATEWAY_MESH_EMITTED_EVENT_TYPES  # noqa: E402,F401
from .pbcs.api_gateway_mesh import API_GATEWAY_MESH_OWNED_TABLES  # noqa: E402,F401
from .pbcs.api_gateway_mesh import API_GATEWAY_MESH_REQUIRED_EVENT_TOPIC  # noqa: E402,F401
from .pbcs.api_gateway_mesh import API_GATEWAY_MESH_RUNTIME_CAPABILITY_KEYS  # noqa: E402,F401
from .pbcs.api_gateway_mesh import API_GATEWAY_MESH_STANDARD_FEATURE_KEYS  # noqa: E402,F401
from .pbcs.api_gateway_mesh import API_GATEWAY_MESH_UI_FRAGMENT_KEYS  # noqa: E402,F401
from .pbcs.api_gateway_mesh import api_gateway_mesh_apply_rate_limit  # noqa: E402,F401
from .pbcs.api_gateway_mesh import api_gateway_mesh_build_api_contract  # noqa: E402,F401
from .pbcs.api_gateway_mesh import api_gateway_mesh_build_release_evidence  # noqa: E402,F401
from .pbcs.api_gateway_mesh import api_gateway_mesh_build_schema_contract  # noqa: E402,F401
from .pbcs.api_gateway_mesh import api_gateway_mesh_build_service_map  # noqa: E402,F401
from .pbcs.api_gateway_mesh import api_gateway_mesh_build_service_contract  # noqa: E402,F401
from .pbcs.api_gateway_mesh import api_gateway_mesh_build_workbench_view  # noqa: E402,F401
from .pbcs.api_gateway_mesh import api_gateway_mesh_configure_runtime  # noqa: E402,F401
from .pbcs.api_gateway_mesh import api_gateway_mesh_empty_state  # noqa: E402,F401
from .pbcs.api_gateway_mesh import api_gateway_mesh_permissions_contract  # noqa: E402,F401
from .pbcs.api_gateway_mesh import api_gateway_mesh_publish_route  # noqa: E402,F401
from .pbcs.api_gateway_mesh import api_gateway_mesh_receive_event  # noqa: E402,F401
from .pbcs.api_gateway_mesh import api_gateway_mesh_record_health  # noqa: E402,F401
from .pbcs.api_gateway_mesh import api_gateway_mesh_record_traffic_sample  # noqa: E402,F401
from .pbcs.api_gateway_mesh import api_gateway_mesh_register_mtls_identity  # noqa: E402,F401
from .pbcs.api_gateway_mesh import api_gateway_mesh_register_rule  # noqa: E402,F401
from .pbcs.api_gateway_mesh import api_gateway_mesh_register_schema_extension  # noqa: E402,F401
from .pbcs.api_gateway_mesh import api_gateway_mesh_register_service  # noqa: E402,F401
from .pbcs.api_gateway_mesh import api_gateway_mesh_render_workbench  # noqa: E402,F401
from .pbcs.api_gateway_mesh import api_gateway_mesh_runtime_capabilities  # noqa: E402,F401
from .pbcs.api_gateway_mesh import api_gateway_mesh_runtime_smoke  # noqa: E402,F401
from .pbcs.api_gateway_mesh import api_gateway_mesh_set_parameter  # noqa: E402,F401
from .pbcs.api_gateway_mesh import api_gateway_mesh_ui_contract  # noqa: E402,F401
from .pbcs.api_gateway_mesh import api_gateway_mesh_verify_owned_table_boundary  # noqa: E402,F401
from .pbcs.schema_registry import SCHEMA_REGISTRY_ALLOWED_DATABASE_BACKENDS  # noqa: E402,F401
from .pbcs.schema_registry import SCHEMA_REGISTRY_CONSUMED_EVENT_TYPES  # noqa: E402,F401
from .pbcs.schema_registry import SCHEMA_REGISTRY_EMITTED_EVENT_TYPES  # noqa: E402,F401
from .pbcs.schema_registry import SCHEMA_REGISTRY_OWNED_TABLES  # noqa: E402,F401
from .pbcs.schema_registry import SCHEMA_REGISTRY_REQUIRED_EVENT_TOPIC  # noqa: E402,F401
from .pbcs.schema_registry import SCHEMA_REGISTRY_RUNTIME_CAPABILITY_KEYS  # noqa: E402,F401
from .pbcs.schema_registry import SCHEMA_REGISTRY_STANDARD_FEATURE_KEYS  # noqa: E402,F401
from .pbcs.schema_registry import SCHEMA_REGISTRY_UI_FRAGMENT_KEYS  # noqa: E402,F401
from .pbcs.schema_registry import schema_registry_build_api_contract  # noqa: E402,F401
from .pbcs.schema_registry import schema_registry_build_release_evidence  # noqa: E402,F401
from .pbcs.schema_registry import schema_registry_build_schema_contract  # noqa: E402,F401
from .pbcs.schema_registry import schema_registry_build_service_contract  # noqa: E402,F401
from .pbcs.schema_registry import schema_registry_build_workbench_view  # noqa: E402,F401
from .pbcs.schema_registry import schema_registry_configure_runtime  # noqa: E402,F401
from .pbcs.schema_registry import schema_registry_define_compatibility_rule  # noqa: E402,F401
from .pbcs.schema_registry import schema_registry_empty_state  # noqa: E402,F401
from .pbcs.schema_registry import schema_registry_permissions_contract  # noqa: E402,F401
from .pbcs.schema_registry import schema_registry_publish_contract_projection  # noqa: E402,F401
from .pbcs.schema_registry import schema_registry_receive_event  # noqa: E402,F401
from .pbcs.schema_registry import schema_registry_record_contract_violation  # noqa: E402,F401
from .pbcs.schema_registry import schema_registry_register_consumer_binding  # noqa: E402,F401
from .pbcs.schema_registry import schema_registry_register_rule  # noqa: E402,F401
from .pbcs.schema_registry import schema_registry_register_schema_extension  # noqa: E402,F401
from .pbcs.schema_registry import schema_registry_register_subject  # noqa: E402,F401
from .pbcs.schema_registry import schema_registry_render_workbench  # noqa: E402,F401
from .pbcs.schema_registry import schema_registry_run_compatibility_check  # noqa: E402,F401
from .pbcs.schema_registry import schema_registry_runtime_capabilities  # noqa: E402,F401
from .pbcs.schema_registry import schema_registry_runtime_smoke  # noqa: E402,F401
from .pbcs.schema_registry import schema_registry_set_parameter  # noqa: E402,F401
from .pbcs.schema_registry import schema_registry_submit_schema_version  # noqa: E402,F401
from .pbcs.schema_registry import schema_registry_ui_contract  # noqa: E402,F401
from .pbcs.schema_registry import schema_registry_validate_payload  # noqa: E402,F401
from .pbcs.schema_registry import schema_registry_verify_owned_table_boundary  # noqa: E402,F401
from .pbcs.workflow_orchestration import WORKFLOW_ORCHESTRATION_RUNTIME_CAPABILITY_KEYS  # noqa: E402,F401
from .pbcs.workflow_orchestration import WORKFLOW_ORCHESTRATION_STANDARD_FEATURE_KEYS  # noqa: E402,F401
from .pbcs.workflow_orchestration import WORKFLOW_ORCHESTRATION_UI_FRAGMENT_KEYS  # noqa: E402,F401
from .pbcs.workflow_orchestration import WORKFLOW_ORCHESTRATION_ALLOWED_DATABASE_BACKENDS  # noqa: E402,F401
from .pbcs.workflow_orchestration import WORKFLOW_ORCHESTRATION_CONSUMED_EVENT_TYPES  # noqa: E402,F401
from .pbcs.workflow_orchestration import WORKFLOW_ORCHESTRATION_EMITTED_EVENT_TYPES  # noqa: E402,F401
from .pbcs.workflow_orchestration import WORKFLOW_ORCHESTRATION_OWNED_TABLES  # noqa: E402,F401
from .pbcs.workflow_orchestration import WORKFLOW_ORCHESTRATION_REQUIRED_EVENT_TOPIC  # noqa: E402,F401
from .pbcs.workflow_orchestration import workflow_orchestration_build_api_contract  # noqa: E402,F401
from .pbcs.workflow_orchestration import workflow_orchestration_build_release_evidence  # noqa: E402,F401
from .pbcs.workflow_orchestration import workflow_orchestration_build_schema_contract  # noqa: E402,F401
from .pbcs.workflow_orchestration import workflow_orchestration_build_service_contract  # noqa: E402,F401
from .pbcs.workflow_orchestration import workflow_orchestration_build_workbench_view  # noqa: E402,F401
from .pbcs.workflow_orchestration import workflow_orchestration_complete_workflow  # noqa: E402,F401
from .pbcs.workflow_orchestration import workflow_orchestration_configure_runtime  # noqa: E402,F401
from .pbcs.workflow_orchestration import workflow_orchestration_define_workflow  # noqa: E402,F401
from .pbcs.workflow_orchestration import workflow_orchestration_empty_state  # noqa: E402,F401
from .pbcs.workflow_orchestration import workflow_orchestration_execute_compensation  # noqa: E402,F401
from .pbcs.workflow_orchestration import workflow_orchestration_permissions_contract  # noqa: E402,F401
from .pbcs.workflow_orchestration import workflow_orchestration_record_step_result  # noqa: E402,F401
from .pbcs.workflow_orchestration import workflow_orchestration_receive_event  # noqa: E402,F401
from .pbcs.workflow_orchestration import workflow_orchestration_register_rule  # noqa: E402,F401
from .pbcs.workflow_orchestration import workflow_orchestration_register_schema_extension  # noqa: E402,F401
from .pbcs.workflow_orchestration import workflow_orchestration_render_workbench  # noqa: E402,F401
from .pbcs.workflow_orchestration import workflow_orchestration_runtime_capabilities  # noqa: E402,F401
from .pbcs.workflow_orchestration import workflow_orchestration_runtime_smoke  # noqa: E402,F401
from .pbcs.workflow_orchestration import workflow_orchestration_schedule_timer  # noqa: E402,F401
from .pbcs.workflow_orchestration import workflow_orchestration_set_parameter  # noqa: E402,F401
from .pbcs.workflow_orchestration import workflow_orchestration_signal_instance  # noqa: E402,F401
from .pbcs.workflow_orchestration import workflow_orchestration_start_instance  # noqa: E402,F401
from .pbcs.workflow_orchestration import workflow_orchestration_ui_contract  # noqa: E402,F401
from .pbcs.workflow_orchestration import workflow_orchestration_verify_owned_table_boundary  # noqa: E402,F401
from .pbcs.audit_ledger import AUDIT_LEDGER_ALLOWED_DATABASE_BACKENDS  # noqa: E402,F401
from .pbcs.audit_ledger import AUDIT_LEDGER_CONSUMED_EVENT_TYPES  # noqa: E402,F401
from .pbcs.audit_ledger import AUDIT_LEDGER_EMITTED_EVENT_TYPES  # noqa: E402,F401
from .pbcs.audit_ledger import AUDIT_LEDGER_OWNED_TABLES  # noqa: E402,F401
from .pbcs.audit_ledger import AUDIT_LEDGER_REQUIRED_EVENT_TOPIC  # noqa: E402,F401
from .pbcs.audit_ledger import AUDIT_LEDGER_RUNTIME_CAPABILITY_KEYS  # noqa: E402,F401
from .pbcs.audit_ledger import AUDIT_LEDGER_STANDARD_FEATURE_KEYS  # noqa: E402,F401
from .pbcs.audit_ledger import AUDIT_LEDGER_UI_FRAGMENT_KEYS  # noqa: E402,F401
from .pbcs.audit_ledger import audit_ledger_assert_control  # noqa: E402,F401
from .pbcs.audit_ledger import audit_ledger_build_api_contract  # noqa: E402,F401
from .pbcs.audit_ledger import audit_ledger_build_release_evidence  # noqa: E402,F401
from .pbcs.audit_ledger import audit_ledger_build_schema_contract  # noqa: E402,F401
from .pbcs.audit_ledger import audit_ledger_build_service_contract  # noqa: E402,F401
from .pbcs.audit_ledger import audit_ledger_build_workbench_view  # noqa: E402,F401
from .pbcs.audit_ledger import audit_ledger_configure_runtime  # noqa: E402,F401
from .pbcs.audit_ledger import audit_ledger_define_retention_policy  # noqa: E402,F401
from .pbcs.audit_ledger import audit_ledger_empty_state  # noqa: E402,F401
from .pbcs.audit_ledger import audit_ledger_permissions_contract  # noqa: E402,F401
from .pbcs.audit_ledger import audit_ledger_prepare_forensic_export  # noqa: E402,F401
from .pbcs.audit_ledger import audit_ledger_publish_audit_projection  # noqa: E402,F401
from .pbcs.audit_ledger import audit_ledger_receive_event  # noqa: E402,F401
from .pbcs.audit_ledger import audit_ledger_record_access_evidence  # noqa: E402,F401
from .pbcs.audit_ledger import audit_ledger_record_audit_event  # noqa: E402,F401
from .pbcs.audit_ledger import audit_ledger_register_rule  # noqa: E402,F401
from .pbcs.audit_ledger import audit_ledger_register_schema_extension  # noqa: E402,F401
from .pbcs.audit_ledger import audit_ledger_render_workbench  # noqa: E402,F401
from .pbcs.audit_ledger import audit_ledger_runtime_capabilities  # noqa: E402,F401
from .pbcs.audit_ledger import audit_ledger_runtime_smoke  # noqa: E402,F401
from .pbcs.audit_ledger import audit_ledger_set_parameter  # noqa: E402,F401
from .pbcs.audit_ledger import audit_ledger_ui_contract  # noqa: E402,F401
from .pbcs.audit_ledger import audit_ledger_verify_owned_table_boundary  # noqa: E402,F401
from .pbcs.audit_ledger import audit_ledger_verify_signature_chain  # noqa: E402,F401
from .pbcs.composition_engine import COMPOSITION_ENGINE_ALLOWED_DATABASE_BACKENDS  # noqa: E402,F401
from .pbcs.composition_engine import COMPOSITION_ENGINE_CONSUMED_EVENT_TYPES  # noqa: E402,F401
from .pbcs.composition_engine import COMPOSITION_ENGINE_EMITTED_EVENT_TYPES  # noqa: E402,F401
from .pbcs.composition_engine import COMPOSITION_ENGINE_OWNED_TABLES  # noqa: E402,F401
from .pbcs.composition_engine import COMPOSITION_ENGINE_REQUIRED_EVENT_TOPIC  # noqa: E402,F401
from .pbcs.composition_engine import COMPOSITION_ENGINE_RUNTIME_CAPABILITY_KEYS  # noqa: E402,F401
from .pbcs.composition_engine import COMPOSITION_ENGINE_STANDARD_FEATURE_KEYS  # noqa: E402,F401
from .pbcs.composition_engine import COMPOSITION_ENGINE_UI_FRAGMENT_KEYS  # noqa: E402,F401
from .pbcs.composition_engine import composition_engine_bind_layout  # noqa: E402,F401
from .pbcs.composition_engine import composition_engine_build_api_contract  # noqa: E402,F401
from .pbcs.composition_engine import composition_engine_build_release_evidence  # noqa: E402,F401
from .pbcs.composition_engine import composition_engine_build_schema_contract  # noqa: E402,F401
from .pbcs.composition_engine import composition_engine_build_service_contract  # noqa: E402,F401
from .pbcs.composition_engine import composition_engine_build_workbench_view  # noqa: E402,F401
from .pbcs.composition_engine import composition_engine_configure_runtime  # noqa: E402,F401
from .pbcs.composition_engine import composition_engine_create_workspace  # noqa: E402,F401
from .pbcs.composition_engine import composition_engine_empty_state  # noqa: E402,F401
from .pbcs.composition_engine import composition_engine_generate_composition_dsl  # noqa: E402,F401
from .pbcs.composition_engine import composition_engine_permissions_contract  # noqa: E402,F401
from .pbcs.composition_engine import composition_engine_plan_package_registration  # noqa: E402,F401
from .pbcs.composition_engine import composition_engine_publish_composition  # noqa: E402,F401
from .pbcs.composition_engine import composition_engine_receive_event  # noqa: E402,F401
from .pbcs.composition_engine import composition_engine_register_component  # noqa: E402,F401
from .pbcs.composition_engine import composition_engine_register_rule  # noqa: E402,F401
from .pbcs.composition_engine import composition_engine_register_schema_extension  # noqa: E402,F401
from .pbcs.composition_engine import composition_engine_register_ui_fragment  # noqa: E402,F401
from .pbcs.composition_engine import composition_engine_render_workbench  # noqa: E402,F401
from .pbcs.composition_engine import composition_engine_runtime_capabilities  # noqa: E402,F401
from .pbcs.composition_engine import composition_engine_runtime_smoke  # noqa: E402,F401
from .pbcs.composition_engine import composition_engine_select_pbc  # noqa: E402,F401
from .pbcs.composition_engine import composition_engine_set_parameter  # noqa: E402,F401
from .pbcs.composition_engine import composition_engine_ui_contract  # noqa: E402,F401
from .pbcs.composition_engine import composition_engine_validate_composition_plan  # noqa: E402,F401
from .pbcs.composition_engine import composition_engine_verify_owned_table_boundary  # noqa: E402,F401
