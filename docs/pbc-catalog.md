# Built-In PBC Catalog

The specific built-in Packaged Business Capabilities are **not part of the AppGen-X language grammar**. The language provides generic `pbc` and `composition` constructs; the concrete catalog is platform metadata.

The executable source of truth is `PBC_CATALOG` in `src/pyAppGen/pbc.py`, with implementation manifests under `src/pyAppGen/pbcs/<pbc_key>/manifest.py`. This document is the human-readable declaration of that catalog for planning, review, and agent handoff.

Total built-in PBCs currently declared: **67**.

## Declaration Rules

- The grammar must stay generic: it should know how to parse `pbc`, `composition`, `include pbc`, `connect`, `expose`, and `require`; it should not hard-code any concrete PBC name.
- Concrete PBC keys, labels, meshes, tables, APIs, events, package locations, and selectability are catalog metadata.
- Built-in PBCs belong in the executable catalog and package manifests, then are surfaced in this document and the IDE catalog.
- External PBCs should self-register through their package manifest instead of requiring a grammar change.
- Compositions should reference PBC keys from the catalog, while custom PBCs must declare or register their own manifest before composition.

## Mesh Summary

| Mesh | Label | PBC Count | Description |
| --- | --- | ---: | --- |
| `commerce` | Advanced Commerce and Fulfillment | 8 | Checkout, order routing, payments, subscriptions, returns, and cross-border commerce. |
| `content` | Product Content, Information, and Assets | 3 | Product information, digital assets, pricing, promotions, and content governance. |
| `cx` | Commerce and Customer Experience | 3 | Demand capture, order orchestration, catalog, and customer capabilities. |
| `finops` | Financial Operations | 12 | Monetary, compliance, accounting, and treasury capabilities. |
| `hcm` | Human Capital Management | 5 | Personnel, identity, labor, payroll, and talent capabilities. |
| `intelligence` | Analytics, Business Intelligence, and Artificial Intelligence | 4 | Streaming analytics, search, forecasting, fraud, and predictive intelligence. |
| `opsmfg` | Operations and Manufacturing | 7 | Planning, production, quality, and asset maintenance capabilities. |
| `platform` | Core Platform, Integration, and Governance | 10 | Identity, gateway, contract validation, workflow, audit, and composition fabric. |
| `relationship` | Relationship, Support, and Marketing | 10 | Pipeline, support, notifications, customer segmentation, and loyalty capabilities. |
| `scl` | Supply Chain and Logistics | 5 | Physical movement, storage, sourcing, and fulfillment capabilities. |

## Catalog

### Advanced Commerce and Fulfillment (`commerce`)

| PBC Key | Label | Description | Datastore | Package | Selectable |
| --- | --- | --- | --- | --- | --- |
| `checkout_processing` | Headless Cart and Checkout Processing | Cart state, pricing, promotions, coupons, and checkout persistence. | `postgresql` | `pbcs/checkout_processing` | `True` |
| `cross_border_trade` | Cross-Border Trade and Customs Compliance | HS code assignment, landed cost, export controls, and customs declarations. | `postgresql` | `pbcs/cross_border_trade` | `True` |
| `global_inventory_visibility` | Global Inventory Visibility and Pool Management | Unified availability across locations, in-transit cargo, vendors, and third-party logistics. | `postgresql` | `pbcs/global_inventory_visibility` | `True` |
| `multi_sided_market` | Multi-Sided Market Exchange | Participant, listing, exchange, booking, rental, loan, escrow, settlement, reputation, and dispute orchestration for goods and services. | `postgresql` | `pbcs/multi_sided_market` | `True` |
| `order_routing_optimization` | Distributed Order Routing and Optimization | Fulfillment route optimization by distance, cost, tax, and node capacity. | `postgresql` | `pbcs/order_routing_optimization` | `True` |
| `payment_orchestration` | Multi-Gateway Payment Orchestration | Gateway routing, fee optimization, localized checks, and payment token controls. | `postgresql` | `pbcs/payment_orchestration` | `True` |
| `returns_reverse_logistics` | Returns RMA and Reverse Logistics | Return authorizations, labels, inspection grading, and credit adjustments. | `postgresql` | `pbcs/returns_reverse_logistics` | `True` |
| `subscription_billing` | Subscription and Recurring Billing Management | Subscriptions, metering, dunning, renewals, and deferred revenue support. | `postgresql` | `pbcs/subscription_billing` | `True` |

### Product Content, Information, and Assets (`content`)

| PBC Key | Label | Description | Datastore | Package | Selectable |
| --- | --- | --- | --- | --- | --- |
| `dam_core` | Digital Asset Management Core | Media storage, transformation, transcoding, metadata tagging, and rights controls. | `postgresql` | `pbcs/dam_core` | `True` |
| `enterprise_pim` | Enterprise Product Information Management | Taxonomies, multilingual attributes, inheritance, localization, validation, dependency projections, publication readiness, and master-data governance. | `postgresql` | `pbcs/enterprise_pim` | `True` |
| `price_promotion_engine` | Dynamic Price Optimization and Promotion Engine | Context pricing, loyalty tiers, volume breaks, demand signals, and promotions. | `postgresql` | `pbcs/price_promotion_engine` | `True` |

### Commerce and Customer Experience (`cx`)

| PBC Key | Label | Description | Datastore | Package | Selectable |
| --- | --- | --- | --- | --- | --- |
| `customer_360` | Customer 360 and Engagement Registry | Profiles, touchpoints, preferences, channel history, and customer read models. | `postgresql` | `pbcs/customer_360` | `True` |
| `dom` | Distributed Order Management | Order verification, fraud screening, allocation, and fulfillment orchestration. | `postgresql` | `pbcs/dom` | `True` |
| `product_catalog_pim` | Enterprise Product Catalog and PIM | Product schemas, pricing, localized descriptions, media, and read models. | `postgresql` | `pbcs/product_catalog_pim` | `True` |

### Financial Operations (`finops`)

| PBC Key | Label | Description | Datastore | Package | Selectable |
| --- | --- | --- | --- | --- | --- |
| `ap_automation` | Accounts Payable Automation | Vendor obligations, OCR intake, invoice matching, approval, and withholding. | `postgresql` | `pbcs/ap_automation` | `True` |
| `ar_credit` | Accounts Receivable and Credit | Customer credit, receivables, invoicing, cash application, collections, revenue schedules, and AR controls. | `postgresql` | `pbcs/ar_credit` | `True` |
| `asset_lifecycle` | Asset Lifecycle and Depreciation | Fixed assets, acquisitions, books, depreciation, transfers, valuation, maintenance, insurance, retirement, verification, and asset controls. | `postgresql` | `pbcs/asset_lifecycle` | `True` |
| `expense_management` | Expense Management | Employee expenses, receipts, card feeds, policies, approvals, reimbursements, fraud checks, and AP/GL events. | `postgresql` | `pbcs/expense_management` | `True` |
| `gl_core` | General Ledger Core | Immutable financial truth, journal orchestration, chart of accounts, and balances. | `postgresql` | `pbcs/gl_core` | `True` |
| `grant_fund_accounting` | Grant and Fund Accounting | Restricted funds, grant budgets, donor rules, allowable costs, reimbursement claims, compliance reporting, and audit trails. | `postgresql` | `pbcs/grant_fund_accounting` | `True` |
| `insurance_claims_policy` | Insurance Claims and Policy | Policies, claims intake, coverage validation, reserves, adjuster workflows, fraud signals, settlement, and audit evidence. | `postgresql` | `pbcs/insurance_claims_policy` | `True` |
| `planning_budgeting_forecasting` | Planning Budgeting and Forecasting | Budgets, forecasts, scenarios, driver models, allocations, approvals, variance analytics, and rolling plans. | `postgresql` | `pbcs/planning_budgeting_forecasting` | `True` |
| `revenue_recognition` | Revenue Recognition | Performance obligations, contract modifications, allocation rules, revenue schedules, compliance evidence, and GL posting events. | `postgresql` | `pbcs/revenue_recognition` | `True` |
| `sustainability_esg_reporting` | Sustainability ESG Reporting | Emissions factors, activity data, carbon ledgers, ESG metrics, assurance evidence, supplier disclosures, and regulatory reporting. | `postgresql` | `pbcs/sustainability_esg_reporting` | `True` |
| `tax_localization` | Tax Compliance and Localization | Regional tax, product taxability, nexus, quote calculation, invoice tax, exemptions, duties, filings, remittance, and tax controls. | `postgresql` | `pbcs/tax_localization` | `True` |
| `treasury_cash` | Treasury and Cash Management | Multi-currency cash, bank connectivity, liquidity planning, funding, investments, debt, FX exposure, and treasury controls. | `postgresql` | `pbcs/treasury_cash` | `True` |

### Human Capital Management (`hcm`)

| PBC Key | Label | Description | Datastore | Package | Selectable |
| --- | --- | --- | --- | --- | --- |
| `payroll_engine` | Compensation and Payroll Engine | Gross-to-net payroll, worker pay profiles, earnings, deductions, benefits, filings, payment and journal handoffs, corrections, controls, and payroll-risk evidence. | `postgresql` | `pbcs/payroll_engine` | `True` |
| `personnel_identity` | Personnel Directory and Identity | Workforce identity, organization topology, lifecycle, roles, attributes, assurance, provisioning, and policy evidence. | `postgresql` | `pbcs/personnel_identity` | `True` |
| `talent_onboarding` | Talent Acquisition and Onboarding | Requisitions, sourcing, candidates, screening, interviews, offers, onboarding tasks, provisioning handoffs, controls, and talent-risk evidence. | `postgresql` | `pbcs/talent_onboarding` | `True` |
| `time_labor` | Time Attendance and Labor Tracking | Schedules, clock events, time entries, absences, approvals, labor costing, payroll-ready summaries, and labor-risk evidence. | `postgresql` | `pbcs/time_labor` | `True` |
| `travel_management` | Travel Management | Travel requests, bookings, itineraries, policy compliance, duty of care, expense handoff, supplier feeds, and carbon tracking. | `postgresql` | `pbcs/travel_management` | `True` |

### Analytics, Business Intelligence, and Artificial Intelligence (`intelligence`)

| PBC Key | Label | Description | Datastore | Package | Selectable |
| --- | --- | --- | --- | --- | --- |
| `enterprise_search_vector` | Enterprise Search and Vector Discovery | Semantic search across products, customers, transactions, and knowledge sources. | `postgresql` | `pbcs/enterprise_search_vector` | `True` |
| `fraud_anomaly_detection` | Anomalous Activity and Fraud Detection | Behavior baselines, identity graph risk, anomaly scores, fraud rules, decision explanations, loss exposure, analyst queues, and operational risk flags. | `postgresql` | `pbcs/fraud_anomaly_detection` | `True` |
| `predictive_demand` | Predictive Demand Forecasting | Time-series prediction for demand, depletion, cash flow, and resource constraints. | `postgresql` | `pbcs/predictive_demand` | `True` |
| `streaming_analytics` | Streaming Analytics and Real-Time Aggregation | Operational metric streams, event ingestion, aggregation windows, KPI snapshots, dashboards, replay, quality, controls, forecasting, risk, and governed analytics models. | `postgresql` | `pbcs/streaming_analytics` | `True` |

### Operations and Manufacturing (`opsmfg`)

| PBC Key | Label | Description | Datastore | Package | Selectable |
| --- | --- | --- | --- | --- | --- |
| `eam` | Enterprise Asset Management | Asset hierarchy, preventive and predictive maintenance, condition monitoring, work orders, safety permits, spares, vendor service, reliability analytics, and governed maintenance automation. | `postgresql` | `pbcs/eam` | `True` |
| `facilities_space_management` | Facilities and Space Management | Sites, buildings, rooms, occupancy, reservations, maintenance links, lease metadata, space planning, and utilization analytics. | `postgresql` | `pbcs/facilities_space_management` | `True` |
| `field_service_management` | Field Service Management | Work orders, dispatch, technicians, mobile tasks, parts usage, SLA tracking, service history, and customer updates. | `postgresql` | `pbcs/field_service_management` | `True` |
| `mrp_engine` | Material Requirements Planning Engine | BOM graph analysis, demand/supply/capacity projections, planning runs, shortages, pegging, release routes, and governed material plans. | `postgresql` | `pbcs/mrp_engine` | `True` |
| `production_control` | Production Scheduling and Floor Control | Routings, work centers, capacity, assembly sequencing, OEE, downtime, execution records, and completion evidence. | `postgresql` | `pbcs/production_control` | `True` |
| `project_portfolio_management` | Project Portfolio Management | Projects, programs, milestones, budgets, resources, risks, dependencies, benefits tracking, and portfolio prioritization. | `postgresql` | `pbcs/project_portfolio_management` | `True` |
| `quality_assurance` | Quality Assurance and Compliance | Inspection checklists, SPC sampling, non-conformance, and quality holds. | `postgresql` | `pbcs/quality_assurance` | `True` |

### Core Platform, Integration, and Governance (`platform`)

| PBC Key | Label | Description | Datastore | Package | Selectable |
| --- | --- | --- | --- | --- | --- |
| `api_gateway_mesh` | Dynamic API Gateway and Service Mesh | Service registration, endpoint catalog, route publication, traffic policy, rate limiting, mTLS identity, health, telemetry, resilience, proofs, optimization, and AppGen-X gateway event orchestration. | `postgresql` | `pbcs/api_gateway_mesh` | `True` |
| `audit_ledger` | Unified Audit Trail and Cryptographic Ledger | Append-only signed mutation, security, and user-action evidence. | `postgresql` | `pbcs/audit_ledger` | `True` |
| `composition_engine` | Low-Code Composition Engine | Drag-and-drop PBC assembly, component registry, layout engine, and experience composition. | `postgresql` | `pbcs/composition_engine` | `True` |
| `data_product_catalog` | Data Product Catalog | Data products, ownership, contracts, quality SLAs, lineage, access requests, governance rules, and publication workflows. | `postgresql` | `pbcs/data_product_catalog` | `True` |
| `enterprise_risk_controls` | Enterprise Risk and Controls | Risk registers, control libraries, attestations, control testing, issue remediation, evidence, and policy mapping. | `postgresql` | `pbcs/enterprise_risk_controls` | `True` |
| `federated_iam` | Federated Identity and Access Management | Tenant, principal, identity provider, identity link, role, policy, token, session, credential verification, privileged access, rules, parameters, configuration, and AppGen-X identity event orchestration. | `postgresql` | `pbcs/federated_iam` | `True` |
| `master_data_governance` | Master Data Governance | Golden records, stewardship workflows, match and merge, validation rules, survivorship, change approvals, and downstream sync events. | `postgresql` | `pbcs/master_data_governance` | `True` |
| `privacy_consent_governance` | Privacy Consent Governance | Data subject rights, consent, retention policies, processing purposes, disclosure logs, impact assessments, and compliance evidence. | `postgresql` | `pbcs/privacy_consent_governance` | `True` |
| `schema_registry` | Schema Registry and Contract Validation | Contract-first subject catalog, schema versioning, compatibility gates, payload validation, impact analysis, projection publication, and governed schema evolution. | `postgresql` | `pbcs/schema_registry` | `True` |
| `workflow_orchestration` | Distributed Workflow Orchestration Engine | Workflow definitions, instances, signals, timers, sagas, compensations, human tasks, rules, parameters, configuration, AppGen-X eventing, and governed orchestration telemetry. | `postgresql` | `pbcs/workflow_orchestration` | `True` |

### Relationship, Support, and Marketing (`relationship`)

| PBC Key | Label | Description | Datastore | Package | Selectable |
| --- | --- | --- | --- | --- | --- |
| `case_knowledge_management` | Case and Knowledge Management | Knowledge articles, semantic search, case deflection, authoring workflows, approvals, content freshness, and agent-assist guidance. | `postgresql` | `pbcs/case_knowledge_management` | `True` |
| `cdp_segmentation` | Customer Data Platform Segmentation | Clickstream, transactions, profiles, and real-time segment activation. | `postgresql` | `pbcs/cdp_segmentation` | `True` |
| `contract_lifecycle` | Contract Lifecycle Management | Contract authoring, clauses, obligations, approvals, renewals, risk scoring, documents, and transaction events. | `postgresql` | `pbcs/contract_lifecycle` | `True` |
| `customer_success_management` | Customer Success Management | Health scores, onboarding plans, adoption telemetry, renewals, expansion signals, playbooks, and churn risk workflows. | `postgresql` | `pbcs/customer_success_management` | `True` |
| `lead_opportunity` | Enterprise Lead and Opportunity Management | Pipeline, deal velocity, account hierarchy, and interaction history. | `postgresql` | `pbcs/lead_opportunity` | `True` |
| `legal_matter_management` | Legal Matter Management | Matters, outside counsel, budgets, documents, deadlines, holds, invoices, outcomes, and legal risk dashboards. | `postgresql` | `pbcs/legal_matter_management` | `True` |
| `loyalty_rewards` | Customer Loyalty Points and Rewards | Rewards, tiers, point balances, earning rules, redemptions, referrals, partner accrual, liability, fraud controls, and reward intelligence. | `postgresql` | `pbcs/loyalty_rewards` | `True` |
| `notifications` | Omni-Channel Communication and Notifications | Omnichannel templates, localized variants, channels, recipients, consent, schedules, throttles, provider routing, delivery lifecycle, campaigns, transactional notifications, audit, analytics, and governed notification operations. | `postgresql` | `pbcs/notifications` | `True` |
| `professional_services_automation` | Professional Services Automation | Engagements, scopes, staffing, time, billing milestones, utilization, project margin, and client delivery workflows. | `postgresql` | `pbcs/professional_services_automation` | `True` |
| `service_ticketing` | Customer Service Ticketing and SLA Orchestration | Omnichannel service case intake, queues, priorities, SLA policy, assignment, field handoff, customer updates, resolution, satisfaction, audit, automation, and governed service operations. | `postgresql` | `pbcs/service_ticketing` | `True` |

### Supply Chain and Logistics (`scl`)

| PBC Key | Label | Description | Datastore | Package | Selectable |
| --- | --- | --- | --- | --- | --- |
| `inventory_positioning` | Inventory Positioning and State | Inventory truth for items, nodes, lots, positions, receipts, adjustments, reservations, allocations, holds, in-transit projections, replenishment, and stock risk. | `postgresql` | `pbcs/inventory_positioning` | `True` |
| `procurement_sourcing` | Procurement and Strategic Sourcing | Requisitions, RFQs, contracts, purchase orders, and vendor performance. | `postgresql` | `pbcs/procurement_sourcing` | `True` |
| `transportation_management` | Transportation Management | Freight routing, carrier choice, shipment tracking, telematics, and ETA updates. | `postgresql` | `pbcs/transportation_management` | `True` |
| `vendor_supplier_360` | Vendor and Supplier 360 | Supplier master, onboarding, qualification, certifications, bank validation, ESG data, risk, and scorecards. | `postgresql` | `pbcs/vendor_supplier_360` | `True` |
| `wms_core` | Warehouse Management Core | Putaway, picking, packing, cross-docking, and warehouse edge workflows. | `postgresql` | `pbcs/wms_core` | `True` |

## How The DSL Uses This Catalog

A composition references catalog keys, but the language does not reserve those keys. For example:

```appgen
composition FinanceSuite {
  include pbc gl_core version 1.0.0
  include pbc ap_automation version 1.0.0
  require database postgresql
  connect ap_automation event InvoiceApproved -> gl_core command PostJournal
}
```

The parser accepts the generic shape. The linter and composition planner validate that `gl_core`, `ap_automation`, `InvoiceApproved`, and `PostJournal` exist in the registered catalog/contracts.
