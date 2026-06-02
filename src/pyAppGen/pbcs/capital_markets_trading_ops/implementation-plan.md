# Capital Markets Trading Operations Implementation Plan

## Target Outcome

Make `capital_markets_trading_ops` usable as a standalone trading-operations PBC, not just a catalog entry. A composed app containing only this PBC should expose trade-order intake, post-trade operations, workbench UI, forms, wizards, controls, agent guidance, owned persistence contracts, AppGen-X events, release evidence, and focused tests.

## Implementation Slices

1. Trade order intake and release readiness
   - validate instrument, account, desk, trader, book, broker, venue, settlement model, regulatory classification, side, quantity, timestamp, and product-specific fields
   - enforce quantity, notional, duplicate, restricted-book, blocked-counterparty, settlement-model, and four-eyes gates
   - emit AppGen-X create/approve/exception events based on release readiness

2. Execution and allocation operations
   - capture partial and final fills with broker/venue timestamps, source channel, economic notional, fees, and correction type
   - prevent executions above parent order quantity
   - split executions across accounts with residual policies, eligibility, mandate gates, and block-child lineage

3. Confirmation, settlement, and break management
   - normalize confirmations from API, file, or document extraction channels
   - compare price, quantity, side, account, settlement date, commission, tax, and counterparty details with tolerances
   - govern effective-dated settlement instructions with market/currency/custodian/place-of-settlement fields
   - track settlement fails, penalties, buy-ins, owners, and open breaks with domain taxonomy

4. Position and projection evidence
   - build position snapshots from executions, allocations, and settlement status
   - record provenance fields for source cut, completeness, correction status, and provisional/final state

5. UI, workflow, and agent surface
   - expose forms for order, execution, allocation, confirmation, settlement instruction, break resolution, position review, and document-instruction intake
   - expose wizards for order release, execution allocation, confirmation affirmation, settlement fail/buy-in handling, break resolution, and release evidence
   - expose controls for reference data, risk gates, allocation eligibility, economic matching, SSI effectivity, settlement fails, and agent mutation confirmation
   - expose agent tools for triage, break explanation, allocation drafting, confirmation summaries, settlement repair, and document-instruction CRUD preview

## Constraints

- Stay inside `src/pyAppGen/pbcs/capital_markets_trading_ops`
- Keep AppGen-X as the only event contract
- Keep all table references owned by `capital_markets_trading_ops`
- Keep backend declarations limited to PostgreSQL, MySQL, and MariaDB
- Do not alter shared language/generator files in this slice

## Acceptance Checks

- Clean equity order reaches `risk_passed` and emits create/approve events
- Blocked order remains visible with actionable remediation
- Execution, allocation, confirmation, SSI, settlement fail, trade break, and position snapshot smoke test passes
- Standalone app surfaces at least eight forms, six wizards, eight controls, and the `capital_markets_trading_ops_skills` namespace
- Package tests, compile, diff check, and focused PBC audits pass
