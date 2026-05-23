"""Packaged Business Capability catalog and composition contracts.

Composable enterprise apps are assembled from independently owned business
capabilities instead of one large shared module.  This module keeps that
catalog executable: every entry declares its datastore boundary, API surface,
event contracts, generated tables, and dependency evidence.
"""

from __future__ import annotations

import py_compile
import re
import tempfile
from pathlib import Path


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
    "ui_fragments",
    "permissions",
    "configuration",
    "migrations",
    "seed_data",
    "tests",
    "docs",
)
PBC_ALLOWED_DATASTORE_BACKENDS = (
    "postgresql",
    "mysql",
    "mariadb",
    "sqlite",
    "duckdb",
    "clickhouse",
    "mongodb",
    "opensearch",
)
ACP_STREAM_PROCESSORS: dict[str, dict] = {
    "bytewax": {
        "label": "Bytewax",
        "core_architecture": "rust_core_python_dataflow_api",
        "state_preservation": "local_in_memory_distributed_recovery",
        "primary_use_case": "complex_parallel_transformations_and_stateful_pipelines",
        "concurrency_model": "rust_multithreaded_execution_threads",
        "best_for": ("parallel_dataflow", "stateful_pipeline", "complex_transform"),
    },
    "quix_streams": {
        "label": "Quix Streams",
        "core_architecture": "pure_python_rocksdb_state_backend",
        "state_preservation": "embedded_rocksdb_on_disk",
        "primary_use_case": "high_throughput_time_series_and_event_data_processing",
        "concurrency_model": "python_multiprocessing_threads",
        "best_for": ("time_series", "event_processing", "high_throughput_ingestion"),
    },
    "faust_streaming": {
        "label": "Faust-Streaming",
        "core_architecture": "pure_python_asyncio_actor_mesh",
        "state_preservation": "embedded_rocksdb_or_in_memory",
        "primary_use_case": "event_driven_microservices_and_asynchronous_workflows",
        "concurrency_model": "asyncio_event_loops",
        "best_for": ("event_driven_service", "async_workflow", "saga_orchestration"),
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
        "tables": ("journal_entry", "journal_line", "ledger_account", "accounting_period"),
        "apis": ("POST /journals", "GET /trial-balance", "GET /chart-of-accounts"),
        "emits": ("JournalPosted", "PeriodClosed", "TrialBalanceCalculated"),
        "consumes": ("InvoiceApproved", "PaymentCaptured", "DepreciationCalculated", "OrderShipped"),
        "template": "general_ledger",
    },
    "ap_automation": {
        "label": "Accounts Payable Automation",
        "mesh": "finops",
        "description": "Vendor obligations, OCR intake, invoice matching, approval, and withholding.",
        "tables": ("vendor", "ap_bill", "ap_payment", "ap_match_exception"),
        "apis": ("POST /vendor-bills", "POST /matches", "POST /approvals"),
        "emits": ("InvoiceApproved", "VendorPaymentRequested", "MatchExceptionRaised"),
        "consumes": ("PurchaseOrderIssued", "GoodsReceiptPosted", "TaxCalculated"),
        "template": "accounts_payable",
    },
    "ar_credit": {
        "label": "Accounts Receivable and Credit",
        "mesh": "finops",
        "description": "Customer invoicing, receivables, collections, aging, and credit limits.",
        "tables": ("customer", "ar_invoice", "ar_payment", "credit_profile"),
        "apis": ("POST /customer-invoices", "GET /aging", "POST /credit-decisions"),
        "emits": ("InvoiceIssued", "PaymentCaptured", "CreditLimitChanged"),
        "consumes": ("OrderShipped", "CustomerUpdated", "TaxCalculated"),
        "template": "accounts_receivable",
    },
    "treasury_cash": {
        "label": "Treasury and Cash Management",
        "mesh": "finops",
        "description": "Multi-currency cash, forecasting, statement ingestion, and reconciliation.",
        "tables": ("bank_account", "bank_statement", "cash_forecast", "reconciliation_item"),
        "apis": ("POST /statements", "GET /cash-position", "POST /reconciliations"),
        "emits": ("CashPositionUpdated", "BankReconciled"),
        "consumes": ("VendorPaymentRequested", "PaymentCaptured", "JournalPosted"),
        "template": None,
    },
    "asset_lifecycle": {
        "label": "Asset Lifecycle and Depreciation",
        "mesh": "finops",
        "description": "Fixed assets, lifecycle state, statutory depreciation, and journal emission.",
        "tables": ("fixed_asset", "asset_event", "depreciation_schedule", "depreciation_run"),
        "apis": ("POST /assets", "POST /depreciation-runs", "GET /asset-register"),
        "emits": ("DepreciationCalculated", "AssetRetired"),
        "consumes": ("AssetPlacedInService", "MaintenanceCompleted"),
        "template": None,
    },
    "tax_localization": {
        "label": "Tax Compliance and Localization",
        "mesh": "finops",
        "description": "Regional tax, VAT, duties, product taxonomies, and jurisdiction rules.",
        "tables": ("tax_jurisdiction", "tax_rule", "tax_calculation", "tax_filing"),
        "apis": ("POST /tax-quotes", "POST /filings", "GET /jurisdictions"),
        "emits": ("TaxCalculated", "TaxFilingPrepared"),
        "consumes": ("ProductClassified", "InvoiceIssued", "OrderPriced"),
        "template": None,
    },
    "inventory_positioning": {
        "label": "Inventory Positioning and State",
        "mesh": "scl",
        "description": "Quantity, allocation, availability, quarantine, in-transit state, and node positions.",
        "tables": ("item", "inventory_node", "inventory_position", "allocation"),
        "apis": ("GET /availability", "POST /allocations", "POST /inventory-events"),
        "emits": ("InventoryAllocated", "InventoryReleased", "GoodsReceiptPosted"),
        "consumes": ("OrderVerified", "ShipmentDelivered", "QualityHoldReleased"),
        "template": "inventory",
    },
    "wms_core": {
        "label": "Warehouse Management Core",
        "mesh": "scl",
        "description": "Putaway, picking, packing, cross-docking, and warehouse edge workflows.",
        "tables": ("warehouse", "bin_location", "pick_wave", "pack_task"),
        "apis": ("POST /putaway", "POST /pick-waves", "POST /pack-tasks"),
        "emits": ("Picked", "Packed", "GoodsReceiptPosted", "OrderShipped"),
        "consumes": ("InventoryAllocated", "InboundArrived"),
        "template": "warehouse_management",
    },
    "procurement_sourcing": {
        "label": "Procurement and Strategic Sourcing",
        "mesh": "scl",
        "description": "Requisitions, RFQs, contracts, purchase orders, and vendor performance.",
        "tables": ("purchase_requisition", "rfq", "vendor_contract", "purchase_order"),
        "apis": ("POST /requisitions", "POST /rfqs", "POST /purchase-orders"),
        "emits": ("PurchaseOrderIssued", "SupplierSelected"),
        "consumes": ("MaterialShortageDetected", "VendorPerformanceUpdated"),
        "template": "purchasing",
    },
    "transportation_management": {
        "label": "Transportation Management",
        "mesh": "scl",
        "description": "Freight routing, carrier choice, shipment tracking, telematics, and ETA updates.",
        "tables": ("shipment", "carrier", "freight_route", "tracking_event"),
        "apis": ("POST /shipments", "POST /carrier-selection", "GET /eta"),
        "emits": ("InboundArrived", "ShipmentDelivered", "EtaUpdated"),
        "consumes": ("Packed", "PurchaseOrderIssued"),
        "template": None,
    },
    "personnel_identity": {
        "label": "Personnel Directory and Identity",
        "mesh": "hcm",
        "description": "Employee master data, organization charts, RBAC attributes, and identity facts.",
        "tables": ("department", "employee", "role_assignment", "identity_attribute"),
        "apis": ("POST /employees", "GET /org-chart", "GET /identity-attributes"),
        "emits": ("EmployeeCreated", "RoleChanged", "CustomerUpdated"),
        "consumes": ("EmployeeProvisioned",),
        "template": "human_resources",
    },
    "time_labor": {
        "label": "Time Attendance and Labor Tracking",
        "mesh": "hcm",
        "description": "Shifts, overtime, absence, geo-fenced clock actions, and payroll-ready hours.",
        "tables": ("shift", "time_entry", "absence", "labor_summary"),
        "apis": ("POST /clock-events", "POST /absences", "GET /labor-summaries"),
        "emits": ("LaborHoursApproved", "AbsenceRecorded"),
        "consumes": ("EmployeeCreated", "RoleChanged"),
        "template": None,
    },
    "payroll_engine": {
        "label": "Compensation and Payroll Engine",
        "mesh": "hcm",
        "description": "Gross-to-net payroll, deductions, benefits, and localized payroll filings.",
        "tables": ("payroll_run", "payslip", "deduction", "benefit_allocation"),
        "apis": ("POST /payroll-runs", "GET /payslips", "POST /payroll-filings"),
        "emits": ("PayrollPosted", "PayrollFilingPrepared"),
        "consumes": ("LaborHoursApproved", "TaxCalculated"),
        "template": "payroll",
    },
    "talent_onboarding": {
        "label": "Talent Acquisition and Onboarding",
        "mesh": "hcm",
        "description": "Applicant pipelines, checks, onboarding tasks, and day-one provisioning.",
        "tables": ("candidate", "job_requisition", "background_check", "onboarding_task"),
        "apis": ("POST /candidates", "POST /offers", "POST /onboarding"),
        "emits": ("EmployeeProvisioned", "CandidateHired"),
        "consumes": ("RoleChanged",),
        "template": None,
    },
    "mrp_engine": {
        "label": "Material Requirements Planning Engine",
        "mesh": "opsmfg",
        "description": "BOM graph analysis, inventory demand, production plans, and procurement schedules.",
        "tables": ("bill_of_material", "material_demand", "mrp_run", "planned_order"),
        "apis": ("POST /mrp-runs", "GET /planned-orders", "GET /shortages"),
        "emits": ("MaterialShortageDetected", "PlannedOrderReleased"),
        "consumes": ("InventoryReleased", "OrderVerified", "ForecastUpdated"),
        "template": "manufacturing",
    },
    "production_control": {
        "label": "Production Scheduling and Floor Control",
        "mesh": "opsmfg",
        "description": "Routings, work centers, capacity, assembly sequencing, OEE, and downtime events.",
        "tables": ("work_center", "production_order", "routing_step", "downtime_event"),
        "apis": ("POST /production-orders", "POST /downtime", "GET /schedule"),
        "emits": ("ProductionCompleted", "AssetPlacedInService", "DowntimeCaptured"),
        "consumes": ("PlannedOrderReleased", "MaintenanceCompleted"),
        "template": "manufacturing",
    },
    "quality_assurance": {
        "label": "Quality Assurance and Compliance",
        "mesh": "opsmfg",
        "description": "Inspection checklists, SPC sampling, non-conformance, and quality holds.",
        "tables": ("inspection_plan", "inspection_result", "quality_hold", "non_conformance"),
        "apis": ("POST /inspections", "POST /non-conformances", "POST /quality-holds"),
        "emits": ("QualityHoldReleased", "NonConformanceRaised"),
        "consumes": ("ProductionCompleted", "GoodsReceiptPosted"),
        "template": "quality_management",
    },
    "eam": {
        "label": "Enterprise Asset Management",
        "mesh": "opsmfg",
        "description": "Preventive and predictive maintenance, MTBF, work orders, and spare parts use.",
        "tables": ("equipment", "maintenance_plan", "work_order", "spare_part_usage"),
        "apis": ("POST /work-orders", "GET /maintenance-plan", "POST /asset-events"),
        "emits": ("MaintenanceCompleted", "VendorPerformanceUpdated"),
        "consumes": ("DowntimeCaptured", "NonConformanceRaised"),
        "template": None,
    },
    "dom": {
        "label": "Distributed Order Management",
        "mesh": "cx",
        "description": "Order verification, fraud screening, allocation, and fulfillment orchestration.",
        "tables": ("sales_order", "order_line", "fulfillment_plan", "fraud_screen"),
        "apis": ("POST /orders", "POST /allocation", "GET /fulfillment-plans"),
        "emits": ("OrderVerified", "OrderPriced", "OrderShipped"),
        "consumes": ("InventoryAllocated", "TaxCalculated", "CustomerUpdated"),
        "template": "sales",
    },
    "product_catalog_pim": {
        "label": "Enterprise Product Catalog and PIM",
        "mesh": "cx",
        "description": "Product schemas, pricing, localized descriptions, media, and read models.",
        "tables": ("product", "product_price", "product_media", "product_attribute"),
        "apis": ("POST /products", "GET /product-read-models", "POST /prices"),
        "emits": ("ProductClassified", "ProductPublished", "ForecastUpdated"),
        "consumes": ("TaxCalculated",),
        "template": "crm",
    },
    "customer_360": {
        "label": "Customer 360 and Engagement Registry",
        "mesh": "cx",
        "description": "Profiles, touchpoints, preferences, channel history, and customer read models.",
        "tables": ("customer_profile", "engagement_event", "communication_preference", "touchpoint"),
        "apis": ("POST /profiles", "POST /touchpoints", "GET /customer-timeline"),
        "emits": ("CustomerUpdated", "PreferenceChanged"),
        "consumes": ("InvoiceIssued", "PaymentCaptured", "CandidateHired"),
        "template": "crm",
    },
}

PBC_CATALOG.update(
    {
        "federated_iam": {
            "label": "Federated Identity and Access Management",
            "mesh": "platform",
            "description": "Context-aware RBAC/ABAC, tenant isolation, OIDC, verification loops, and token issuance.",
            "tables": ("tenant", "principal", "access_policy", "token_grant"),
            "apis": ("POST /tokens", "GET /principals", "POST /policy-decisions"),
            "emits": ("AccessPolicyChanged", "PrincipalVerified"),
            "consumes": ("RoleChanged", "TenantProvisioned"),
            "template": None,
        },
        "api_gateway_mesh": {
            "label": "Dynamic API Gateway and Service Mesh",
            "mesh": "platform",
            "description": "Ingress routing, rate limiting, service discovery, mTLS policy, and telemetry.",
            "tables": ("service_route", "rate_limit_policy", "mtls_identity", "traffic_sample"),
            "apis": ("POST /routes", "POST /rate-limits", "GET /service-map"),
            "emits": ("RoutePublished", "ServiceHealthChanged"),
            "consumes": ("PbcDeployed", "AccessPolicyChanged"),
            "template": None,
        },
        "schema_registry": {
            "label": "Schema Registry and Contract Validation",
            "mesh": "platform",
            "description": "Synchronous and asynchronous contract validation with compatibility gates.",
            "tables": ("schema_subject", "schema_version", "compatibility_rule", "contract_violation"),
            "apis": ("POST /schemas", "POST /compatibility-checks", "GET /subjects"),
            "emits": ("SchemaAccepted", "BreakingSchemaBlocked"),
            "consumes": ("PbcDeployed", "EventContractProposed"),
            "template": None,
        },
        "workflow_orchestration": {
            "label": "Distributed Workflow Orchestration Engine",
            "mesh": "platform",
            "description": "Visual state-machine orchestration, sagas, timers, retries, and compensation.",
            "tables": ("workflow_definition", "workflow_instance", "saga_step", "timer_task"),
            "apis": ("POST /workflows", "POST /instances", "POST /signals"),
            "emits": ("WorkflowStarted", "SagaCompensated", "WorkflowCompleted"),
            "consumes": ("InvoiceApproved", "OrderVerified", "ShipmentDelivered"),
            "template": None,
        },
        "audit_ledger": {
            "label": "Unified Audit Trail and Cryptographic Ledger",
            "mesh": "platform",
            "description": "Append-only signed mutation, security, and user-action evidence.",
            "tables": ("audit_event", "signature_chain", "retention_policy", "forensic_export"),
            "apis": ("POST /audit-events", "GET /signature-chain", "POST /exports"),
            "emits": ("AuditEventSealed", "ForensicExportPrepared"),
            "consumes": ("AccessPolicyChanged", "WorkflowCompleted", "RoutePublished"),
            "template": None,
        },
        "composition_engine": {
            "label": "Low-Code Composition Engine",
            "mesh": "platform",
            "description": "Drag-and-drop PBC assembly, component registry, layout engine, and experience composition.",
            "tables": ("composition_workspace", "ui_fragment", "component_registry", "layout_binding"),
            "apis": ("POST /compositions", "POST /fragments", "GET /component-registry"),
            "emits": ("CompositionPublished", "PbcDeployed"),
            "consumes": ("SchemaAccepted", "RoutePublished"),
            "template": None,
        },
        "global_inventory_visibility": {
            "label": "Global Inventory Visibility and Pool Management",
            "mesh": "commerce",
            "description": "Unified availability across locations, in-transit cargo, vendors, and third-party logistics.",
            "tables": ("inventory_pool", "inventory_projection", "supply_node", "availability_snapshot"),
            "apis": ("GET /global-availability", "POST /pool-rules", "GET /supply-nodes"),
            "emits": ("AvailabilityProjected", "InventoryPoolChanged"),
            "consumes": ("GoodsReceiptPosted", "ShipmentDelivered", "InventoryAllocated"),
            "template": "inventory",
        },
        "order_routing_optimization": {
            "label": "Distributed Order Routing and Optimization",
            "mesh": "commerce",
            "description": "Fulfillment route optimization by distance, cost, tax, and node capacity.",
            "tables": ("routing_rule", "route_candidate", "capacity_snapshot", "routing_decision"),
            "apis": ("POST /route-orders", "GET /route-candidates", "POST /capacity"),
            "emits": ("FulfillmentRouteSelected", "NodeCapacityReserved"),
            "consumes": ("OrderVerified", "AvailabilityProjected", "TaxCalculated"),
            "template": "sales",
        },
        "checkout_processing": {
            "label": "Headless Cart and Checkout Processing",
            "mesh": "commerce",
            "description": "Cart state, pricing, promotions, coupons, and checkout persistence.",
            "tables": ("cart", "cart_line", "checkout_session", "promotion_redemption"),
            "apis": ("POST /carts", "POST /checkout", "POST /coupons"),
            "emits": ("OrderPriced", "CheckoutCompleted"),
            "consumes": ("ProductPublished", "PriceOptimized", "TaxCalculated"),
            "template": "sales",
        },
        "payment_orchestration": {
            "label": "Multi-Gateway Payment Orchestration",
            "mesh": "commerce",
            "description": "Gateway routing, fee optimization, localized checks, and payment token controls.",
            "tables": ("payment_gateway", "payment_intent", "payment_token", "fraud_check"),
            "apis": ("POST /payment-intents", "POST /gateway-routes", "POST /tokens"),
            "emits": ("PaymentCaptured", "PaymentFailed", "FraudCheckRequested"),
            "consumes": ("CheckoutCompleted", "FraudRiskScored"),
            "template": None,
        },
        "subscription_billing": {
            "label": "Subscription and Recurring Billing Management",
            "mesh": "commerce",
            "description": "Subscriptions, metering, dunning, renewals, and deferred revenue support.",
            "tables": ("subscription", "usage_meter", "billing_schedule", "dunning_notice"),
            "apis": ("POST /subscriptions", "POST /usage", "POST /renewals"),
            "emits": ("SubscriptionRenewed", "UsageRated", "InvoiceApproved"),
            "consumes": ("PaymentCaptured", "PriceOptimized"),
            "template": "invoicing",
        },
        "returns_reverse_logistics": {
            "label": "Returns RMA and Reverse Logistics",
            "mesh": "commerce",
            "description": "Return authorizations, labels, inspection grading, and credit adjustments.",
            "tables": ("return_authorization", "return_label", "inspection_grade", "credit_adjustment"),
            "apis": ("POST /returns", "POST /labels", "POST /inspection-grades"),
            "emits": ("ReturnAuthorized", "CreditAdjustmentIssued"),
            "consumes": ("OrderShipped", "PaymentCaptured"),
            "template": None,
        },
        "cross_border_trade": {
            "label": "Cross-Border Trade and Customs Compliance",
            "mesh": "commerce",
            "description": "HS code assignment, landed cost, export controls, and customs declarations.",
            "tables": ("hs_classification", "landed_cost_quote", "export_control_check", "customs_declaration"),
            "apis": ("POST /landed-cost", "POST /export-checks", "POST /declarations"),
            "emits": ("CustomsDeclarationPrepared", "LandedCostCalculated"),
            "consumes": ("ProductClassified", "OrderPriced"),
            "template": None,
        },
        "enterprise_pim": {
            "label": "Enterprise Product Information Management",
            "mesh": "content",
            "description": "Taxonomies, multilingual attributes, inheritance, localization, and validation.",
            "tables": ("product_taxonomy", "product_attribute", "localized_content", "validation_workflow"),
            "apis": ("POST /taxonomies", "POST /attributes", "POST /localized-content"),
            "emits": ("ProductClassified", "ProductPublished"),
            "consumes": ("SchemaAccepted",),
            "template": "crm",
        },
        "dam_core": {
            "label": "Digital Asset Management Core",
            "mesh": "content",
            "description": "Media storage, transformation, transcoding, metadata tagging, and rights controls.",
            "tables": ("asset", "asset_rendition", "rights_policy", "metadata_tag"),
            "apis": ("POST /assets", "POST /renditions", "GET /rights"),
            "emits": ("AssetPublished", "RightsPolicyChanged"),
            "consumes": ("ProductPublished",),
            "template": None,
        },
        "price_promotion_engine": {
            "label": "Dynamic Price Optimization and Promotion Engine",
            "mesh": "content",
            "description": "Context pricing, loyalty tiers, volume breaks, demand signals, and promotions.",
            "tables": ("price_rule", "promotion", "loyalty_tier", "price_decision"),
            "apis": ("POST /price-quotes", "POST /promotions", "GET /price-decisions"),
            "emits": ("PriceOptimized", "PromotionApplied"),
            "consumes": ("CustomerSegmentUpdated", "ForecastUpdated"),
            "template": None,
        },
        "lead_opportunity": {
            "label": "Enterprise Lead and Opportunity Management",
            "mesh": "relationship",
            "description": "Pipeline, deal velocity, account hierarchy, and interaction history.",
            "tables": ("lead", "opportunity", "account_hierarchy", "sales_activity"),
            "apis": ("POST /leads", "POST /opportunities", "GET /pipeline"),
            "emits": ("OpportunityWon", "CustomerUpdated"),
            "consumes": ("CustomerSegmentUpdated",),
            "template": "crm",
        },
        "service_ticketing": {
            "label": "Customer Service Ticketing and SLA Orchestration",
            "mesh": "relationship",
            "description": "Multi-channel support, routing, escalation, and SLA tracking.",
            "tables": ("support_ticket", "sla_policy", "case_assignment", "escalation_event"),
            "apis": ("POST /tickets", "POST /assignments", "GET /sla-status"),
            "emits": ("SupportCaseOpened", "SlaBreached"),
            "consumes": ("CustomerUpdated", "PreferenceChanged"),
            "template": None,
        },
        "notifications": {
            "label": "Omni-Channel Communication and Notifications",
            "mesh": "relationship",
            "description": "SMS, email, chat, push, preferences, templates, and delivery abstractions.",
            "tables": ("notification_template", "delivery_channel", "message_delivery", "preference_snapshot"),
            "apis": ("POST /messages", "POST /templates", "GET /delivery-status"),
            "emits": ("MessageDelivered", "MessageFailed"),
            "consumes": ("PreferenceChanged", "SlaBreached", "WorkflowCompleted"),
            "template": None,
        },
        "cdp_segmentation": {
            "label": "Customer Data Platform Segmentation",
            "mesh": "relationship",
            "description": "Clickstream, transactions, profiles, and real-time segment activation.",
            "tables": ("customer_event", "segment_definition", "segment_membership", "profile_property"),
            "apis": ("POST /events", "POST /segments", "GET /memberships"),
            "emits": ("CustomerSegmentUpdated", "ProfileEnriched"),
            "consumes": ("CustomerUpdated", "PaymentCaptured", "OrderShipped"),
            "template": "crm",
        },
        "loyalty_rewards": {
            "label": "Customer Loyalty Points and Rewards",
            "mesh": "relationship",
            "description": "Rewards, tiers, point balances, earning rules, and redemption validation.",
            "tables": ("reward_account", "points_ledger", "earning_rule", "redemption"),
            "apis": ("POST /points", "POST /redemptions", "GET /reward-accounts"),
            "emits": ("RewardBalanceChanged", "CustomerSegmentUpdated"),
            "consumes": ("PaymentCaptured", "PromotionApplied"),
            "template": None,
        },
        "streaming_analytics": {
            "label": "Streaming Analytics and Real-Time Aggregation",
            "mesh": "intelligence",
            "description": "Windowed metrics, counts, KPI state, and operational dashboard models.",
            "tables": ("metric_stream", "aggregation_window", "kpi_snapshot", "dashboard_projection"),
            "apis": ("POST /metric-streams", "GET /kpis", "GET /projections"),
            "emits": ("ForecastUpdated", "OperationalKpiChanged"),
            "consumes": ("AuditEventSealed", "OrderShipped", "PaymentCaptured"),
            "template": "reporting",
        },
        "enterprise_search_vector": {
            "label": "Enterprise Search and Vector Discovery",
            "mesh": "intelligence",
            "description": "Semantic search across products, customers, transactions, and knowledge sources.",
            "tables": ("search_index", "embedding_job", "vector_document", "query_trace"),
            "apis": ("POST /indexes", "POST /embeddings", "POST /search"),
            "emits": ("SearchIndexUpdated", "DiscoveryInsightGenerated"),
            "consumes": ("ProductPublished", "CustomerUpdated", "AuditEventSealed"),
            "template": None,
        },
        "predictive_demand": {
            "label": "Predictive Demand Forecasting",
            "mesh": "intelligence",
            "description": "Time-series prediction for demand, depletion, cash flow, and resource constraints.",
            "tables": ("forecast_model", "forecast_run", "demand_signal", "forecast_result"),
            "apis": ("POST /forecast-runs", "GET /forecast-results", "POST /signals"),
            "emits": ("ForecastUpdated", "MaterialShortageDetected"),
            "consumes": ("OperationalKpiChanged", "OrderShipped", "InventoryPoolChanged"),
            "template": None,
        },
        "fraud_anomaly_detection": {
            "label": "Anomalous Activity and Fraud Detection",
            "mesh": "intelligence",
            "description": "Behavior baselines, anomaly scores, fraud checks, and operational risk flags.",
            "tables": ("risk_signal", "anomaly_score", "fraud_rule", "risk_case"),
            "apis": ("POST /risk-events", "POST /fraud-checks", "GET /risk-cases"),
            "emits": ("FraudRiskScored", "RiskCaseOpened"),
            "consumes": ("CheckoutCompleted", "PaymentCaptured", "AccessPolicyChanged"),
            "template": None,
        },
    }
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


def pbc_catalog(mesh: str | None = None) -> tuple[dict, ...]:
    """Return selectable PBC descriptors for the IDE catalog."""
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


def select_acp_stream_processor(workload: str) -> dict:
    """Select a stream processor profile for an APC workload description."""
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
                "One of the approved open-source datastore backends: "
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
            "ui_fragments": "Optional generated UI fragment descriptors for the composition canvas.",
            "permissions": "Optional RBAC/ABAC permission strings exposed by the PBC.",
            "configuration": "Optional environment/configuration keys required at install time.",
            "migrations": "Optional migration artifact paths owned by the PBC package.",
            "seed_data": "Optional seed artifact paths owned by the PBC package.",
            "tests": "Optional test artifact paths that prove the PBC package contract.",
            "docs": "Optional documentation artifact paths for builders and operators.",
        },
        "self_registration_entrypoint": "register_pbc() -> dict",
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
    """Return a bounded-context composition plan for selected PBCs."""
    selected = tuple(dict.fromkeys(selected_pbcs))
    missing = tuple(key for key in selected if key not in PBC_CATALOG)
    services = tuple(_service_contract(key) for key in selected if key in PBC_CATALOG)
    emitted = {
        event: service["pbc"]
        for service in services
        for event in service["emits"]
    }
    dependencies = tuple(
        {
            "from": service["pbc"],
            "event": event,
            "provider": emitted.get(event),
            "resolved": emitted.get(event) is not None,
        }
        for service in services
        for event in service["consumes"]
        if emitted.get(event) is not None
    )
    unresolved_external_events = tuple(
        {
            "pbc": service["pbc"],
            "event": event,
            "policy": "external-event-contract",
        }
        for service in services
        for event in service["consumes"]
        if emitted.get(event) is None
    )
    datastores = tuple(service["datastore"] for service in services)
    shared_datastores = tuple(
        datastore for datastore in datastores if datastores.count(datastore) > 1
    )
    return {
        "format": "appgen.pbc-composition-plan.v1",
        "ok": not missing and not shared_datastores and bool(services),
        "app_name": app_name,
        "targets": targets,
        "pbcs": selected,
        "services": services,
        "dependencies": dependencies,
        "external_event_contracts": unresolved_external_events,
        "missing_pbcs": missing,
        "shared_datastores": tuple(dict.fromkeys(shared_datastores)),
        "integration_style": "event-first-with-api-command-surface",
        "deployment_units": tuple(f"services/{service['pbc']}" for service in services),
        "stop_condition": "do-not-compose-pbcs-unless-each-selected-capability-has-an-owned-datastore",
    }


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
    for service in plan["services"]:
        for table in service["tables"][:3]:
            table_name = f"{service['pbc']}_{table}"
            lines.extend(
                (
                    "",
                    f"table {table_name} {{",
                    "  id: int pk",
                    "  code: string required search",
                    "  status: string required",
                    "  updated_at: datetime",
                    "}",
                )
            )
        event_table = f"{service['pbc']}_event_outbox"
        lines.extend(
            (
                "",
                f"table {event_table} {{",
                "  id: int pk",
                "  event_type: string required search",
                "  payload: text required",
                "  published_at: datetime",
                "}",
                "",
                f"view {service['class_name']}Workbench for {event_table} {{",
                "  Main: event_type, payload, published_at",
                "  @ event_type TextBox 0 0 6 1",
                "  @ payload TextArea 0 1 12 3",
                "  @ published_at DateTimePicker 0 4 6 1",
                "}",
            )
        )
    return "\n".join(lines).rstrip() + "\n"


def pbc_release_audit() -> dict:
    """Return package-level proof for composable PBC app generation."""
    sample = PBC_STARTER_STACKS["enterprise_core"]
    composition = pbc_composition_plan(sample, app_name="EnterpriseCore")
    acp_composition = pbc_composition_plan(PBC_STARTER_STACKS["application_composition_platform"], app_name="AppCompositionPlatform")
    topology = application_composition_topology()
    acp_coverage = acp_capability_coverage()
    nl_selection = pbc_selection_from_prompt(
        "Build an enterprise ERP back office with GL, AP, AR, inventory, people, and order management"
    )
    smoke = pbc_generation_smoke_audit(sample)
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
                for item in pbc_catalog()
            ),
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
            "id": "composition_plan",
            "ok": composition["ok"]
            and not composition["shared_datastores"]
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
            "ok": smoke["ok"],
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
        "sample_composition": composition,
        "nl_selection": nl_selection,
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
        generate_app_from_schema(schema, project_dir / "app")
        artifacts = ("app/models.py", "app/views.py", "app/appgen.json", "docs/schema.md")
        missing = tuple(path for path in artifacts if not (project_dir / path).exists())
        compiled = []
        compile_failures = []
        for relative in ("app/models.py", "app/views.py"):
            path = project_dir / relative
            try:
                py_compile.compile(str(path), doraise=True)
            except py_compile.PyCompileError as exc:
                compile_failures.append({"path": relative, "error": str(exc)})
            else:
                compiled.append(relative)
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
            "ok": not compile_failures and set(compiled) == {"app/models.py", "app/views.py"},
            "compiled": tuple(compiled),
            "failures": tuple(compile_failures),
        },
    )
    return {
        "format": "appgen.pbc-generation-smoke-audit.v1",
        "ok": all(check["ok"] for check in checks),
        "selected_pbcs": selected,
        "dsl": dsl,
        "checks": checks,
    }


def _pbc_descriptor(key: str, pbc: dict) -> dict:
    return {
        "pbc": key,
        "label": pbc["label"],
        "mesh": pbc["mesh"],
        "mesh_label": PBC_MESHES[pbc["mesh"]]["label"],
        "description": pbc["description"],
        "datastore": f"{key}_store",
        "datastore_backend": pbc.get("datastore_backend", "postgresql"),
        "stream_processor": pbc.get("stream_processor", "faust_streaming"),
        "tables": pbc["tables"],
        "apis": pbc["apis"],
        "emits": pbc["emits"],
        "consumes": pbc["consumes"],
        "template": pbc["template"],
        "selectable": True,
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


def _selection_terms(key: str, pbc: dict) -> tuple[str, ...]:
    terms = set(key.split("_"))
    terms.update(word.lower() for word in re.findall(r"[A-Za-z]+", pbc["label"]) if len(word) > 2)
    terms.update(word.lower() for table in pbc["tables"] for word in table.split("_") if len(word) > 2)
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
