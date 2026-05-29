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
| tax_localization | `pbc/tax-localization-standalone` | `8e7035ad` | Compile, 13 tests, spec/source/release/smoke true. |
| treasury_cash | `pbc/treasury-cash-standalone` | `85904689` | Compile, 13 tests, spec/source/release/smoke true. |
| api_gateway_mesh | `pbc/api-gateway-mesh-standalone` | `2b87e526` | Compile, 16 tests, spec/source/release/smoke true. |
| audit_ledger | `pbc/audit-ledger-standalone` | `fd33958c` | Compile, 14 tests, spec/source/release/smoke true. |
| composition_engine | `pbc/composition-engine-standalone` | `15b94ed2` | Compile, 16 tests, spec/source/release/smoke true. |
| schema_registry | `pbc/schema-registry-standalone` | `4ef03c66` | Compile, 13 tests, spec/source/release/smoke true. |
| workflow_orchestration | `pbc/workflow-orchestration-standalone` | `d51b6db5` | Compile, 20 tests, spec/source/release/smoke true. |
| data_product_catalog | `pbc/data-product-catalog-standalone` | `0a93b815` | Previously pushed. |
| dom | `pbc/dom-standalone` | `2c21573a` | Compile, 19 tests, spec/source/release/smoke true. |
| eam | `pbc/eam-standalone` | `27a1665f` | Compile, 9 tests, spec/source/release/smoke true. |
| education_student_lifecycle | `pbc/education-student-lifecycle-standalone` | `dd0b0a6c` | Compile, 15 tests, spec/source/release/smoke true. |
| electronic_health_records_core | `pbc/electronic-health-records-core-standalone` | `390e70a8` | Compile, 11 tests, spec/source/release/smoke true. |
| energy_grid_operations | `pbc/energy-grid-operations-standalone` | `9ddf1e59` | Compile, 10 tests, spec/source/release/smoke true. |
| energy_trading_risk | `pbc/energy-trading-risk-standalone` | `cd222843` | Compile, 13 tests, spec/source/release/smoke true. |
| enterprise_pim | `pbc/enterprise-pim-standalone` | `38063c5b` | Compile, 13 tests, spec/source/release/smoke true. |
| enterprise_risk_controls | `pbc/enterprise-risk-controls-standalone` | `e6f662f8` | Compile, 11 tests, spec/source/release/smoke true. |
| enterprise_search_vector | `pbc/enterprise-search-vector-standalone` | `1cd7729d` | Compile, 12 tests, spec/source/release/smoke true. |
| expense_management | `pbc/expense-management-standalone` | `d9abfac1` | Compile, 7 tests, spec/source/release/smoke true. |
| facilities_space_management | `pbc/facilities-space-management-standalone` | `eace636f` | Compile, 7 tests, spec/source/release true; generation smoke hung and is documented in branch evidence. |
| federated_iam | `pbc/federated-iam-standalone` | `8e57b2f4` | Compile, 14 tests, spec/source/release/smoke true. |
| inventory_positioning | `pbc/inventory-positioning-standalone` | `5fa432ae` | Compile, 8 tests, spec/source/release/smoke true. |
| quality_assurance | `pbc/quality-assurance-standalone` | `63171cb9` | Compile, 11 tests, spec/source/release/smoke true. |
| production_control | `pbc/production-control-standalone` | `29677a7b` | Compile, 12 tests, spec/source/release/smoke true. |
| procurement_sourcing | `pbc/procurement-sourcing-standalone` | `ed99321e` | Compile, 13 tests, spec/source/release/smoke true. |
| personnel_identity | `pbc/personnel-identity-standalone` | `702e305c` | Compile, 10 tests, spec/source/release/smoke true. |
| product_catalog_pim | `pbc/product-catalog-pim-standalone` | `68cb9615` | Compile, 11 tests, spec/source/release/smoke true. |
| price_promotion_engine | `pbc/price-promotion-engine-standalone` | `fc1f33db` | Compile, 13 tests, spec/source/release/smoke true. |
| checkout_processing | `pbc/checkout-processing-standalone` | `dee3836d` | Compile, 18 tests, spec/source/release/smoke true. |
| payment_orchestration | `pbc/payment-orchestration-standalone` | `d40508f2` | Compile, 13 tests, spec/source/release/smoke true. |
| subscription_billing | `pbc/subscription-billing-standalone` | `6eea93d8` | Compile, 13 tests, spec/source/release/smoke true. |
| talent_onboarding | `pbc/talent-onboarding-standalone` | `bb438e42` | Compile, 11 tests, spec/source/release/smoke true. |
| time_labor | `pbc/time-labor-standalone` | `cdadd9fc` | Compile, 10 tests, spec/source/release/smoke true. |
| mrp_engine | `pbc/mrp-engine-standalone` | `58e3e2bc` | Compile, 11 tests, spec/source/release/smoke true. |
| payroll_engine | `pbc/payroll-engine-standalone` | `91db28ac` | Compile, 10 tests, spec/source/release/smoke true. |
| transportation_management | `pbc/transportation-management-standalone` | `17f7e4fe` | Compile, 13 tests, spec/source/release/smoke true. |
| wms_core | `pbc/wms-core-standalone` | `7574fcc3` | Compile, 13 tests, spec/source/release/smoke true. |

## In Flight

Supply-chain/HCM standalone pass is continuing. `wms_core`, `procurement_sourcing`, `transportation_management`, `dom`, `global_inventory_visibility`, `personnel_identity`, `time_labor`, and `payroll_engine` are pushed; quality_assurance is pushed; mrp_engine is pushed; asset_lifecycle, production_control, talent_onboarding, product_catalog_pim, price_promotion_engine, checkout_processing, payment_orchestration, and subscription_billing are pushed; next slices continue through commerce/content/relationship and intelligence PBCs.

## Next Selection Rule

Continue in batches of five independent PBCs. Prefer platform and core shared capabilities first, then finance, supply chain, HCM/payroll, manufacturing, commerce/content/relationship, intelligence, and industry-specific PBCs. Skip PBCs that already have pushed standalone branches unless a later merge review identifies gaps.
