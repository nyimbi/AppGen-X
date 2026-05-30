# Legal Matter Management Implementation Plan

## Intent

Make `legal_matter_management` viable as a one-PBC legal operating system with executable intake, conflicts, hold, deadline, filing, evidence, spend, settlement, and assistant behavior.

## Plan

1. Add legal-domain forms for intake, conflicts, counsel, holds, deadlines, documents, invoices, and settlement.
2. Add guided wizards for intake/playbook, conflicts/counsel, preservation, deadlines/filings, privilege/evidence, spend/reserves, and settlement/closure.
3. Add legal controls that block unsafe work until required evidence and approvals exist.
4. Implement a standalone app that exercises matter opening, duplicate detection, conflict screening, counsel assignment, legal holds, custodian acknowledgement, critical deadlines, filings, documents, privilege review, budgets, invoice compliance, exposure simulation, settlement approvals, closure, and assistant previews.
5. Wire standalone UI and release evidence into package-local contracts.
6. Add focused tests and record validation evidence.

## Boundary

All changes stay inside `src/pyAppGen/pbcs/legal_matter_management`, reference only owned `legal_matter_management_*` tables, and use AppGen-X events.
