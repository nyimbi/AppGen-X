# PBC Implementation Progress

This file tracks the branch-isolated implementation pass for standalone Packaged Business Capabilities. It is intentionally kept under `src/pyAppGen/pbcs` so it stays inside the PBC-only work boundary.

## Operating Constraints

- Each PBC is implemented in its own directory under `src/pyAppGen/pbcs/<pbc_key>`.
- Each PBC branch is isolated in a separate git worktree and is pushed for later merge.
- No work in this pass should touch application language/runtime files outside `src/pyAppGen/pbcs`.
- Each standalone PBC must include executable domain code, datastore-backed models, services, routes, workflows, UI/forms/wizards/controls, AI assistant capabilities, configuration, permissions, events/handlers, release evidence, tests, and domain-specific documentation.
- Validation evidence must include focused tests plus AppGen-X PBC contract/release/generation smoke gates when available.

## Pushed Standalone Branches

| PBC | Branch | Commit | Validation |
| --- | --- | --- | --- |
| ap_automation | `pbc/ap-automation-standalone` | `4fcec336` | Compile, 16 tests, spec/source/release/smoke true. |
| ar_credit | `pbc/ar-credit-standalone` | `72ea8fe9` | Compile, 8 tests, spec/source/release/smoke true. |
| asset_lifecycle | `pbc/asset-lifecycle-standalone` | `3cbc4a4b` | Compile, 11 tests, spec/source/release/smoke true. |
| global_inventory_visibility | `pbc/global-inventory-visibility-standalone` | `705516f6` | Compile, 14 tests, spec/source/release/smoke true. |
| gl_core | `pbc/gl-core-standalone` | `d59473d4` | Compile, 11 tests, spec/source/release/smoke true. |
| grant_fund_accounting | `pbc/grant-fund-accounting-standalone` | `aecad332` | Compile, 11 tests, source/package/spec/agent/implementation/capability/generation audits true; standalone award-to-closeout grant accounting app with forms/wizards/controls and agent extraction previews added. |
| tax_localization | `pbc/tax-localization-standalone` | `8e7035ad` | Compile, 13 tests, spec/source/release/smoke true. |
| treasury_cash | `pbc/treasury-cash-standalone` | `85904689` | Compile, 13 tests, spec/source/release/smoke true. |
| api_gateway_mesh | `pbc/api-gateway-mesh-standalone` | `2b87e526` | Compile, 16 tests, spec/source/release/smoke true. |
| audit_ledger | `pbc/audit-ledger-standalone` | `fd33958c` | Compile, 14 tests, spec/source/release/smoke true. |
| composition_engine | `pbc/composition-engine-standalone` | `15b94ed2` | Compile, 16 tests, spec/source/release/smoke true. |
| schema_registry | `pbc/schema-registry-standalone` | `4ef03c66` | Compile, 13 tests, spec/source/release/smoke true. |
| workflow_orchestration | `pbc/workflow-orchestration-standalone` | `d51b6db5` | Compile, 20 tests, spec/source/release/smoke true. |
| actuarial_pricing_reserving | `pbc/actuarial-pricing-reserving-standalone` | `34cb09ee` | Compile, 15 tests, source/package/spec/agent/implementation/capability/generation audits true; standalone actuarial app surface and full release simulation added. |
| agri_supply_chain_traceability | `pbc/agri-supply-chain-traceability-standalone` | `16698645` | Compile, 14 tests total, source/implementation/generation/release validation true; standalone app surface added; worker noted split/merge lineage and custody-transfer depth remain for refinement. |
| advertising_campaign_operations | `pbc/advertising-campaign-operations-standalone` | `398fa79b` | Compile, 9 direct tests, package/routes/services/standalone/workflows/release evidence true; worker noted flight-plan versioning, media-buying hold ledger, reserve/billing reconciliation, and pacing normalization remain for refinement. |
| agriculture_farm_operations | `pbc/agriculture-farm-operations-standalone` | `9ed3aef7` | Compile, 20 tests, implementation/capability audits true; worker noted broader irrigation, scouting, harvest, soil-health, and persisted relational execution remain for refinement. |
| airline_operations_control | `pbc/airline-operations-control-standalone` | `11ae12bd` | Compile, 9 direct tests, package-local capability/routes/release/runtime/standalone audits true; worker noted crew legality, slot/curfew, ATC/weather/NOTAM, reaccommodation, and cancellation-economics depth remain for refinement. |
| airport_operations_management | `pbc/airport-operations-management-standalone` | `28750bef` | Compile, 14 tests, source/package/spec/agent/implementation/capability/generation audits true; standalone airport operations center app, drills, forms/wizards/controls, and assistant guardrails added. |
| claims_adjudication_healthcare | `pbc/claims-adjudication-healthcare-standalone` | `af4cc5a3` | Compile, 16 tests, source/package/spec/agent/implementation/capability/generation audits true; standalone claims adjudication app surface and simulation added. |
| clinical_care_coordination | `pbc/clinical-care-coordination-standalone` | `5b59064b` | Py compile, 16 tests, implementation/generation audits true; worker noted social barriers, guideline impact, richer timeline replay, caregiver revocation, and referral analytics remain for refinement. |
| clinical_trials_management | `pbc/clinical-trials-management-standalone` | `16718527` | Compile, 13 tests, source/package/spec/agent/implementation/capability/generation audits true; standalone clinical trials app, trial-to-lock workflow, forms/wizards/controls, and agent surface added. |
| construction_contracts_commercials | `pbc/construction-contracts-commercials-standalone` | `9881ebf4` | Compile, 15 direct harness tests, standalone/release/capability/package smokes true; one-PBC app surface with store/model/service/route/UI/agent/release contracts added. |
| construction_project_controls | `pbc/construction-project-controls-standalone` | `4b6e4548` | Compile, 13 direct package tests, package-local/implementation/capability audits true; full 15-table model registry, model manifest, instantiation, and runtime artifact alignment added. |
| court_case_management | `pbc/court-case-management-standalone` | `d353e0ab` | Compile, 17 package tests, local/repo implementation and generation audits true; standalone court operations app with case lifecycle, service/UI/agent, schema, audit, docs, and release evidence added. |
| cybersecurity_operations_center | `pbc/cybersecurity-operations-center-standalone` | `e656cbb8` | Compile, 13 unittest tests, runtime/route/standalone smokes true; standalone SOC app, service/route operation alignment, workflow catalog, workbench/detail helpers, docs, and release evidence added. |
| customer_success_management | `pbc/customer-success-management-standalone` | `193bea0f` | Compile, 11 tests, source/implementation/generation audits true; standalone touchpoint-owned table, migration, service operation, route, kickoff touchpoint, workbench/forms/wizards/controls, and docs added. |
| building_information_modeling_ops | `pbc/building-information-modeling-ops-standalone` | `b5060410` | Compile, 16 unittest tests, standalone smoke true, package audit 12/12 true; worker noted slice is narrow relative to improve1 backlog and needs refinement before strict completion. |
| aviation_maintenance_repair | `pbc/aviation-maintenance-repair-standalone` | `8b78e74c` | Compile, 11 unittest tests, package/runtime/release/capability smoke true; worker noted package-local/in-memory runtime, JSON-envelope migration columns, and no live API/browser session. |
| bank_payments_clearing | `pbc/bank-payments-clearing-standalone` | `8a83eb10` | Compile, 13 direct harness tests, package-local runtime/service/route/ui/config/event/handler/agent/capability/standalone/release smokes true; pytest CLI and live DB execution not exercised. |
| banking_core_accounts | `pbc/banking-core-accounts-standalone` | `d2d53487` | Compile, 12 tests, runtime smoke true, capability assurance/release evidence true; worker noted balance decomposition, hold waterfalls, overdraft behavior, statements, and shared-auth integration remain for refinement. |
| capital_projects_delivery | `pbc/capital-projects-delivery-standalone` | `3700c479` | Compile, 18 focused package tests, source artifact, implementation release, and generation smoke audits true; standalone capital projects delivery shell and refreshed runtime/service/route/UI/agent contracts added. |
| capital_markets_trading_ops | `pbc/capital-markets-trading-ops-standalone` | `5205ee02` | Compile, 18 tests, source/package/spec/agent/implementation/capability/generation audits true; standalone order-to-settlement trading operations app, post-trade flow, forms/wizards/controls, workflows, and agent surface added. |
| data_product_catalog | `pbc/data-product-catalog-standalone` | `0a93b815` | Previously pushed. |
| dom | `pbc/dom-standalone` | `2c21573a` | Compile, 19 tests, spec/source/release/smoke true. |
| donor_grant_fundraising | `pbc/donor-grant-fundraising-standalone` | `434effbd` | Compile, 20 direct harness tests, package/runtime/standalone smokes true; standalone fundraising/grant app, owned-table schema/runtime alignment, route/service expansion, assistant/workbench surfaces, docs, and release evidence added. |
| eam | `pbc/eam-improve1-standalone` | `9e25db84` | Compile, 13 tests, source/package/spec/agent/implementation/capability/generation audits true; improve1 forms/wizards/controls and single-PBC app surface added. |
| education_student_lifecycle | `pbc/education-student-lifecycle-standalone` | `dd0b0a6c` | Compile, 15 tests, spec/source/release/smoke true. |
| electronic_health_records_core | `pbc/electronic-health-records-core-standalone` | `390e70a8` | Compile, 11 tests, spec/source/release/smoke true. |
| energy_grid_operations | `pbc/energy-grid-operations-standalone` | `9ddf1e59` | Compile, 10 tests, spec/source/release/smoke true. |
| energy_trading_risk | `pbc/energy-trading-risk-standalone` | `cd222843` | Compile, 13 tests, spec/source/release/smoke true. |
| environment_health_safety | `pbc/environment-health-safety-standalone` | `a0a87323` | Compile, 12 direct harness tests, package/runtime/service/route/handler/release/capability/schema/boundary smokes true; standalone EHS app, domain contracts, services/routes/events/handlers/UI/agent/docs/tests added. |
| enterprise_pim | `pbc/enterprise-pim-standalone` | `38063c5b` | Compile, 13 tests, spec/source/release/smoke true. |
| enterprise_risk_controls | `pbc/enterprise-risk-controls-standalone` | `e6f662f8` | Compile, 11 tests, spec/source/release/smoke true. |
| enterprise_search_vector | `pbc/enterprise-search-vector-standalone` | `1cd7729d` | Compile, 12 tests, spec/source/release/smoke true. |
| expense_management | `pbc/expense-management-standalone` | `d9abfac1` | Compile, 7 tests, spec/source/release/smoke true. |
| facility_energy_management | `pbc/facility-energy-management-standalone` | `1b4e59dd` | Compile, 11 tests, source/package/spec/agent/implementation/capability/generation audits true; standalone facility energy app with meter topology, interval reads, tariffs, HVAC schedules, baselines, demand response, controls, forms/wizards, and agent previews added. |
| facilities_space_management | `pbc/facilities-space-management-standalone` | `eace636f` | Compile, 7 tests, spec/source/release true; generation smoke hung and is documented in branch evidence. |
| federated_iam | `pbc/federated-iam-standalone` | `8e57b2f4` | Compile, 14 tests, spec/source/release/smoke true. |
| field_service_management | `pbc/field-service-management-standalone` | `00658b71` | Compile, 11 tests, spec/source/release/smoke true. |
| fleet_mobility_operations | `pbc/fleet-mobility-operations-standalone` | `57d8082a` | Compile, 11 tests, source/package/spec/agent/implementation/capability/generation audits true; standalone fleet control tower with readiness, assignment, telematics quarantine, route ETA, maintenance horizon, fuel/EV checks, incident command, forms/wizards/controls, and agent replans added. |
| inventory_positioning | `pbc/inventory-positioning-standalone` | `5fa432ae` | Compile, 8 tests, spec/source/release/smoke true. |
| quality_assurance | `pbc/quality-assurance-standalone` | `63171cb9` | Compile, 11 tests, spec/source/release/smoke true. |
| production_control | `pbc/production-control-standalone` | `29677a7b` | Compile, 12 tests, spec/source/release/smoke true. |
| procurement_sourcing | `pbc/procurement-sourcing-standalone` | `ed99321e` | Compile, 13 tests, spec/source/release/smoke true. |
| personnel_identity | `pbc/personnel-identity-standalone` | `702e305c` | Compile, 10 tests, spec/source/release/smoke true. |
| privacy_consent_governance | `pbc/privacy-consent-governance-standalone` | `cc18026b` | Compile, 10 direct harness tests, spec/source/implementation/generation audits true; live PostgreSQL/MySQL/MariaDB execution not exercised. |
| product_catalog_pim | `pbc/product-catalog-pim-standalone` | `68cb9615` | Compile, 11 tests, spec/source/release/smoke true. |
| price_promotion_engine | `pbc/price-promotion-engine-standalone` | `fc1f33db` | Compile, 13 tests, spec/source/release/smoke true. |
| checkout_processing | `pbc/checkout-processing-standalone` | `dee3836d` | Compile, 18 tests, spec/source/release/smoke true. |
| chemical_batch_compliance | `pbc/chemical-batch-compliance-standalone` | `e14751a2` | Compile, 14 tests, source/package/spec/agent/implementation/capability/generation audits true; standalone one-PBC chemical compliance app, workbench, forms/wizards/controls, and agent document-instruction surface added. |
| payment_orchestration | `pbc/payment-orchestration-standalone` | `d40508f2` | Compile, 13 tests, spec/source/release/smoke true. |
| subscription_billing | `pbc/subscription-billing-standalone` | `6eea93d8` | Compile, 13 tests, spec/source/release/smoke true. |
| revenue_recognition | `pbc/revenue-recognition-standalone` | `839b71ee` | Compile, 12 tests, source/package/spec/agent/implementation/capability/generation audits true. |
| returns_reverse_logistics | `pbc/returns-reverse-logistics-standalone` | `0c9bc46f` | Compile, 16 tests, spec/source/release/smoke true. |
| contract_lifecycle | `pbc/contract-lifecycle-standalone` | `a43f6669` | Compile, 15 tests, source/package/spec/agent/implementation/capability/generation audits true. |
| cross_border_trade | `pbc/cross-border-trade-standalone` | `5d7ceb09` | Compile, 14 tests, spec/source/release/smoke true. |
| order_routing_optimization | `pbc/order-routing-optimization-standalone` | `44a80fbd` | Compile, 14 tests, spec/source/release/smoke true. |
| customer_360 | `pbc/customer-360-standalone` | `f838821d` | Compile, 11 tests, spec/source/release/smoke true. |
| case_knowledge_management | `pbc/case-knowledge-management-standalone` | `cbcc01b3` | Compile, 15 tests, source/package/spec/agent/implementation/capability/generation audits true. |
| cdp_segmentation | `pbc/cdp-segmentation-standalone` | `de76c716` | Compile, 18 direct tests, spec/source/release/smoke true. |
| dam_core | `pbc/dam-core-standalone` | `ec976c9e` | Compile, 16 tests, spec/source/release/smoke true. |
| lead_opportunity | `pbc/lead-opportunity-standalone` | `1d0b2cc4` | Compile, 12 tests, spec/source/release/smoke true. |
| loyalty_rewards | `pbc/loyalty-rewards-standalone` | `b6b54f69` | Compile, 13 harness tests, source/release/generation smoke true. |
| service_ticketing | `pbc/service-ticketing-standalone` | `6952f1e9` | Compile, 12 tests, spec/source/release/smoke true. |
| streaming_analytics | `pbc/streaming-analytics-standalone` | `53608606` | Compile, 13 tests, spec/source/release/generation audits true. |
| notifications | `pbc/notifications-standalone` | `4f48b505` | Compile, 12 tests, spec/source/release/smoke true. |
| predictive_demand | `pbc/predictive-demand-standalone` | `226a460e` | Compile, 12 tests, spec/source/release/smoke true. |
| fraud_anomaly_detection | `pbc/fraud-anomaly-detection-standalone` | `bb6fedf7` | Compile, 12 tests, spec/source/release/smoke true. |
| talent_onboarding | `pbc/talent-onboarding-standalone` | `bb438e42` | Compile, 11 tests, spec/source/release/smoke true. |
| time_labor | `pbc/time-labor-standalone` | `cdadd9fc` | Compile, 10 tests, spec/source/release/smoke true. |
| mrp_engine | `pbc/mrp-engine-standalone` | `58e3e2bc` | Compile, 11 tests, spec/source/release/smoke true. |
| multi_sided_market | `pbc/multi-sided-market-standalone` | `073d9b72` | Compile, 13 tests, spec/source/release/smoke true. |
| payroll_engine | `pbc/payroll-engine-standalone` | `91db28ac` | Compile, 10 tests, spec/source/release/smoke true. |
| planning_budgeting_forecasting | `pbc/planning-budgeting-forecasting-standalone` | `e718f233` | Compile, 10 tests, spec/source/release/smoke true. |
| transportation_management | `pbc/transportation-management-standalone` | `17f7e4fe` | Compile, 13 tests, spec/source/release/smoke true. |
| vendor_supplier_360 | `pbc/vendor-supplier-360-standalone` | `05aa391c` | Compile, 10 tests, spec/source/release/smoke true. |
| wms_core | `pbc/wms-core-standalone` | `7574fcc3` | Compile, 13 tests, spec/source/release/smoke true. |
| master_data_governance | `pbc/master-data-governance-standalone` | `88aba9e3` | Compile, 9 direct harness tests, spec/source/release/generation smoke true. |

## In Flight

Supply-chain/HCM standalone pass is continuing. `wms_core`, `procurement_sourcing`, `transportation_management`, `dom`, `global_inventory_visibility`, `personnel_identity`, `time_labor`, and `payroll_engine` are pushed; quality_assurance is pushed; mrp_engine is pushed; asset_lifecycle, production_control, talent_onboarding, product_catalog_pim, price_promotion_engine, checkout_processing, payment_orchestration, subscription_billing, returns_reverse_logistics, cross_border_trade, order_routing_optimization, customer_360, cdp_segmentation, lead_opportunity, loyalty_rewards, service_ticketing, notifications, predictive_demand, fraud_anomaly_detection, dam_core, multi_sided_market, vendor_supplier_360, field_service_management, privacy_consent_governance, streaming_analytics, actuarial_pricing_reserving, agri_supply_chain_traceability, airline_operations_control, advertising_campaign_operations, agriculture_farm_operations, airport_operations_management, building_information_modeling_ops, banking_core_accounts, aviation_maintenance_repair, bank_payments_clearing, claims_adjudication_healthcare, clinical_care_coordination, chemical_batch_compliance, capital_projects_delivery, capital_markets_trading_ops, clinical_trials_management, construction_contracts_commercials, construction_project_controls, court_case_management, cybersecurity_operations_center, customer_success_management, donor_grant_fundraising, environment_health_safety, facility_energy_management, fleet_mobility_operations, grant_fund_accounting, and the EAM improve1 standalone surface are pushed; next slices continue through content, relationship, intelligence, finance, governance, and industry PBCs.

## Next Selection Rule

Continue in batches of five independent PBCs. Prefer platform and core shared capabilities first, then finance, supply chain, HCM/payroll, manufacturing, commerce/content/relationship, intelligence, and industry-specific PBCs. Skip PBCs that already have pushed standalone branches unless a later merge review identifies gaps.
