# AP Automation Slice

This package now contains an executable accounts-payable automation slice centered on vendor payment readiness, invoice duplicate controls, approval-aware scheduling, payment batching/remittance, and vendor statement reconciliation.

## Executable workflows

- `ap_automation_onboard_vendor`
  Creates a vendor record with an evidence pack and payment-readiness requirements.
- `ap_automation_validate_vendor_bank_account`
  Validates vendor banking evidence and updates vendor payment readiness.
- `ap_automation_register_vendor_tax_profile`
  Validates AP tax-profile completeness and expiry before enabling payment.
- `ap_automation_screen_vendor_network`
  Applies AP screening outcomes and refreshes payment readiness.
- `ap_automation_capture_invoice`
  Captures invoices, writes a canonical artifact, scores duplicate risk, and records hold reasons.
- `ap_automation_match_invoice`
  Performs AP matching and routes held or duplicate invoices to exception handling.
- `ap_automation_create_approval_task`
  Opens AP approval work when thresholds or risk controls require human review.
- `ap_automation_schedule_payments`
  Produces liquidity-aware payment plans with explicit scheduling explanations and blocked reasons.
- `ap_automation_create_payment_batch`
  Groups scheduled payments into a batch owned by this PBC.
- `ap_automation_execute_payment`
  Executes only unblocked payments and preserves AppGen-X event evidence.
- `ap_automation_generate_remittance_advice`
  Builds remittance evidence for executed AP payments.
- `ap_automation_reconcile_vendor_statement`
  Reconciles supplier statements against owned invoices and records discrepancy evidence.

## Package wiring

- `runtime.py` contains the executable AP behaviors and state transitions.
- `services.py` exposes the new runtime-backed execution surface through `ApAutomationExecutionService`.
- `ui.py` surfaces vendor readiness, payment holds, remittance, and statement reconciliation controls.
- `agent.py` advertises the execution slice to the composed assistant.
- `release_evidence.py` now derives release evidence from live runtime, UI, agent, and execution-service surfaces.

## Boundaries

- Eventing remains AppGen-X only.
- All writes stay within `ap_automation_*` owned tables plus the package runtime state model.
- No shared-table access is introduced by this slice.
