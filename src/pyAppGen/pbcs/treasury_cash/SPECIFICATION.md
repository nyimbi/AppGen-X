# Treasury Cash PBC Specification

## Purpose

`treasury_cash` owns cash positioning, liquidity planning, bank connectivity,
payment funding, FX exposure, intercompany cash movement, investment and debt
operations, treasury controls, and resilience evidence. It is a composable PBC:
it exposes APIs, events, projections, and risk signals, but it does not share
tables with payables, receivables, ledger, or banking adapters.

## Standard Table-Stakes Capabilities

- Bank account master data with account ownership, currency, legal entity, and
  signatory metadata.
- Opening and intraday bank balance capture.
- Cash position projection by tenant, currency, account, and value date.
- Bank statement ingestion and reconciliation.
- Cash forecast from payables, receivables, payroll, tax, and manual flows.
- Liquidity pool management and target balance policy.
- Cash concentration and sweep planning.
- Payment funding proposal and release authorization.
- Intercompany netting and in-house bank settlement.
- FX exposure capture, hedge recommendation, and hedge accounting evidence.
- Debt facility drawdown, repayment, covenant, and interest schedule tracking.
- Short-term investment placement and maturity tracking.
- Bank fee analysis and anomaly detection.
- Signatory, approval, and segregation-of-duties controls.
- Counterparty and bank risk scoring.
- Treasury workbench summary with cash, risk, funding, and exception metrics.
- Audit trail, idempotency keys, retry/dead-letter evidence, and immutable
  event contracts.
- Configuration for currencies, calendars, liquidity thresholds, and risk
  appetite.

## Advanced Capabilities

- Event-sourced cash lifecycle across balances, forecasts, funding,
  investments, debt, hedges, sweeps, and settlements.
- Graph-relational bank and counterparty topology with exposure propagation.
- Multi-tenant liquidity isolation with independent pools and policies.
- Schema-evolution resilient cash-flow schema for dynamic source attributes.
- Probabilistic cash forecasting with confidence bands.
- Real-time liquidity optimization across available cash, working-capital
  obligations, target balances, and funding cost.
- Counterfactual funding and investment scenario analysis.
- Temporal cash-flow stochastic modeling.
- Autonomous bank-statement reconciliation and exception suggestions.
- Semantic bank narrative parsing for unstructured statement references.
- Predictive counterparty, bank, and liquidity risk scoring.
- Self-healing payment rail and bank-channel routing.
- Zero-knowledge liquidity covenant proof.
- Immutable bank connectivity and regulatory audit trail.
- Dynamic sanction, fraud, and bank-network screening.
- Automated treasury control testing.
- Universal API and async event contracts for cash, funding, hedge, and
  statement flows.
- Cross-border liquidity federation using ISO 20022-style message evidence.
- Supply-chain and working-capital finance integration evidence.
- Decentralized counterparty identity verification.
- Chaos-engineered bank-rail tolerance.
- Crypto-agile payment and treasury authorization.
- Carbon-aware liquidity movement scheduling.
- Algebraic liquidity optimization with multi-objective scoring.
- Mechanism-design funding allocation across entities and counterparties.
- Information-theoretic cash-flow anomaly detection.
- Temporal liquidity stochastic modeling.
- Distributed systems engineering for idempotent multi-region cash state.
- Probabilistic ML for liquidity and counterparty risk.
- Cryptographic engineering for proofs and signatures.
- Mathematical optimization for funding, sweeping, and hedging.
- Financial MLOps governance for regulated treasury models.

## Owned Runtime Boundary

All executable implementation lives in this directory. The catalog may re-export
stable helpers for compatibility, but cash state, runtime smoke evidence,
standard feature inventory, and advanced capability evidence are owned here.

