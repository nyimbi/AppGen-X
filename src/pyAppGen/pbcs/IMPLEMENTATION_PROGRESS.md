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
| data_product_catalog | `pbc/data-product-catalog-standalone` | `0a93b815` | Previously pushed. |
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

## In Flight

| PBC | Worktree | Branch | Owner |
| --- | --- | --- | --- |
| schema_registry | `/private/tmp/appgen-pbc-schema-registry` | `pbc/schema-registry-standalone` | child agent |
| api_gateway_mesh | `/private/tmp/appgen-pbc-api-gateway-mesh` | `pbc/api-gateway-mesh-standalone` | child agent |
| workflow_orchestration | `/private/tmp/appgen-pbc-workflow-orchestration` | `pbc/workflow-orchestration-standalone` | child agent |
| audit_ledger | `/private/tmp/appgen-pbc-audit-ledger` | `pbc/audit-ledger-standalone` | child agent |
| composition_engine | `/private/tmp/appgen-pbc-composition-engine` | `pbc/composition-engine-standalone` | child agent |

## Next Selection Rule

Continue in batches of five independent PBCs. Prefer platform and core shared capabilities first, then finance, supply chain, HCM/payroll, manufacturing, commerce/content/relationship, intelligence, and industry-specific PBCs. Skip PBCs that already have pushed standalone branches unless a later merge review identifies gaps.
