# Lending Origination and Servicing Implementation Plan

## Intent

Make `lending_origination_servicing` viable as a one-PBC lending application spanning origination, decisioning, funding, servicing, collections, payoff, compliance, and covenants.

## Plan

1. Add domain forms for intake, stipulations, verification, collateral, underwriting, offers, disbursement, repayment, and collections.
2. Add guided wizards for application-to-decision, collateral, offer-to-funding, boarding, payment/payoff, collections/workout, and compliance/covenants.
3. Add controls for consent, stipulations, identity/fraud, underwriting lineage, funding/boarding, restricted servicing actions, and modification accounting.
4. Implement a standalone app that executes intake, verification, collateral, underwriting, offer, funding, boarding, payments, collections, modifications, payoff, special servicing, covenants, and assistant previews.
5. Wire standalone UI and release evidence into package-local contracts.
6. Add focused tests and record validation evidence.

## Boundary

All changes stay inside `src/pyAppGen/pbcs/lending_origination_servicing`, reference only owned `lending_origination_servicing_*` tables, and use AppGen-X event contracts.
