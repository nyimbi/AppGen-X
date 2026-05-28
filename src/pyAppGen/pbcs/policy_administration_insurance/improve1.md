# Insurance Policy Administration PBC Manual Improvement Backlog

## Purpose

This hand-crafted backlog replaces generic roadmap text for `policy_administration_insurance` with insurance-policy-administration-specific improvements for policy issuance, coverage schedules, endorsements, renewals, cancellations, reinstatements, billing status, documents, compliance notices, workbench operations, and governed agent assistance.

## Current Domain Evidence Used

- Stable PBC key: `policy_administration_insurance`.
- Domain purpose: insurance policy lifecycle, endorsements, renewals, cancellations, billing status, coverage changes, and documents.
- Owned records include `insurance_policy`, `coverage_item`, `endorsement`, `renewal_notice`, `cancellation_event`, `billing_status`, `policy_document`, policy rules, runtime parameters, schema extensions, control assertions, and governed models.
- Public APIs include `POST /insurance-policys`, `POST /coverage-items`, `POST /endorsements`, `POST /renewal-notices`, `POST /cancellation-events`, and `GET /policy-administration-insurance-workbench`.
- Workbench surfaces include `PolicyAdministrationInsuranceWorkbench`, `PolicyAdministrationInsuranceDetail`, and `PolicyAdministrationInsuranceAssistantPanel`.
- AppGen-X events include `PolicyAdministrationInsuranceCreated`, `PolicyAdministrationInsuranceUpdated`, `PolicyAdministrationInsuranceApproved`, and `PolicyAdministrationInsuranceExceptionOpened`.

## 50 High-Impact Improvements

### 1. Policy issuance readiness gate

**Justification:** Issuing a policy requires bound quote evidence, insured details, coverage schedule, effective dates, billing status, required documents, and authority.

**Improvement:** Add issuance checks that validate required policy facts, coverage items, document templates, billing projection, underwriting decision projection, and approval evidence.

**Acceptance evidence:** Tests must block active policy state until all issuance prerequisites are present and visible in `PolicyAdministrationInsuranceWorkbench`.

### 2. Insurance policy lifecycle state machine

**Justification:** Policies move through quoted, issued, active, endorsed, renewed, pending cancel, cancelled, reinstated, expired, non-renewed, and archived states.

**Improvement:** Add explicit `insurance_policy` states with transition reasons, effective dates, allowed commands, approval rules, and AppGen-X event emission.

**Acceptance evidence:** Invalid transition tests must fail and the workbench must show next allowed actions by policy state.

### 3. Policy term and version governance

**Justification:** Policy administration must preserve every term, renewal, rewrite, mid-term change, and correction without overwriting historical obligations.

**Improvement:** Add term versions with policy period, transaction type, predecessor, successor, transaction effective date, processing date, and supersession reason.

**Acceptance evidence:** Tests must reconstruct policy coverage as of any date across endorsements and renewals.

### 4. Coverage item schedule depth

**Justification:** Coverage details include limits, deductibles, forms, exclusions, rating attributes, locations, vehicles, assets, or insured interests.

**Improvement:** Expand `coverage_item` with coverage type, covered object, limit structure, deductible, form reference, effective window, and coverage status.

**Acceptance evidence:** Tests must validate coverage schedules and reject active policies with incomplete required coverage fields.

### 5. Named insured and additional interest handling

**Justification:** Policies need accurate named insureds, additional insureds, lienholders, mortgagees, loss payees, and certificate holders.

**Improvement:** Store party role projections, role effective dates, interest type, document requirements, and communication eligibility without owning external party records.

**Acceptance evidence:** Boundary tests must prove party data is consumed as projection evidence and no external party table is mutated.

### 6. Endorsement transaction model

**Justification:** Mid-term changes require request, quote, approval, effective date, premium impact, forms, documents, and policy versioning.

**Improvement:** Expand `endorsement` with change set, requested effective date, accepted effective date, changed coverage items, premium delta, approval, and document output.

**Acceptance evidence:** Tests must create endorsement transactions and show before/after coverage comparisons.

### 7. Endorsement eligibility rules

**Justification:** Some changes are prohibited after cancellation, outside policy period, during nonpayment, or without underwriting approval.

**Improvement:** Add eligibility rules by transaction type, policy status, product, jurisdiction, underwriting projection, billing status, and effective date.

**Acceptance evidence:** Tests must reject ineligible endorsements with cited rule versions.

### 8. Premium-impact handoff boundary

**Justification:** Policy administration needs premium deltas and billing status but should not own rating or accounts receivable.

**Improvement:** Store premium-impact projections, billing-account status, invoice readiness, and receivable handoff events through declared APIs/events.

**Acceptance evidence:** Boundary tests must show no mutation of rating or billing tables while preserving premium impact evidence.

### 9. Cancellation workflow

**Justification:** Cancellation requires reason, notice period, effective date, refund calculation projection, legal basis, and stop conditions.

**Improvement:** Expand `cancellation_event` with initiator, reason, notice deadline, rescission window, required approvals, proof of mailing, and cancellation outcome.

**Acceptance evidence:** Tests must block cancellation finalization before required notice and approval evidence.

### 10. Nonpayment cancellation controls

**Justification:** Nonpayment cancellation is sensitive because billing, grace periods, protected status, and reinstatement rules interact.

**Improvement:** Add nonpayment cancellation checklist with billing status projection, grace date, notice sequence, payment cure evidence, and suppression reason.

**Acceptance evidence:** Tests must cancel only when grace and notice conditions are satisfied.

### 11. Flat cancellation and rescission handling

**Justification:** Some policies are voided from inception or rescinded due to misrepresentation, duplicate issuance, or legal requirement.

**Improvement:** Add flat-cancel and rescission transaction types with authority, evidence, effective handling, document set, and downstream event contract.

**Acceptance evidence:** Tests must distinguish flat cancellation from earned-premium cancellation and preserve reason evidence.

### 12. Reinstatement workflow

**Justification:** Reinstatement needs payment cure, no-loss statements, underwriting approval, lapse handling, and document reissue.

**Improvement:** Add reinstatement records with request date, cure evidence, lapse period, required statements, approval, new effective status, and document output.

**Acceptance evidence:** Tests must prevent reinstatement when configured prerequisites are missing.

### 13. Renewal preparation timeline

**Justification:** Renewals need underwriting review, updated exposure data, billing status, offer terms, notices, and non-renewal decisions.

**Improvement:** Expand `renewal_notice` with renewal cycle, review status, data refresh requirements, offer terms, non-renewal option, and mailing evidence.

**Acceptance evidence:** Tests must generate renewal work queues and block late notices.

### 14. Non-renewal governance

**Justification:** Non-renewal decisions are jurisdiction-sensitive and require reasons, notice timing, approval, and documentation.

**Improvement:** Add non-renewal records with reason, allowed basis, notice deadline, approval authority, delivery proof, and appeal/reconsideration status.

**Acceptance evidence:** Tests must reject non-renewal without valid reason and timely notice evidence.

### 15. Lapse and expiration handling

**Justification:** Expired or lapsed policies must stop endorsements, renewal offers, certificates, and coverage confirmations unless reinstatement applies.

**Improvement:** Add lapse and expiration controls that update allowed actions, document availability, coverage status, and downstream event emissions.

**Acceptance evidence:** Tests must block coverage-confirming actions on expired or lapsed policies.

### 16. Billing status projection

**Justification:** Billing determines active, nonpayment, cancellation, reinstatement, and renewal eligibility but belongs outside this PBC.

**Improvement:** Expand `billing_status` as a projection with account state, amount due, delinquency date, last payment, invoice status, and freshness.

**Acceptance evidence:** Tests must reject stale billing projections for nonpayment decisions.

### 17. Policy document generation package

**Justification:** Policies require declarations, forms, endorsements, notices, certificates, binders, and evidence of delivery.

**Improvement:** Expand `policy_document` with document type, template version, included forms, jurisdiction, language, render hash, delivery status, and correction link.

**Acceptance evidence:** Tests must generate required document manifests for new policy, endorsement, renewal, cancellation, and reinstatement.

### 18. Forms library and edition control

**Justification:** Wrong form editions create coverage, regulatory, and dispute risk.

**Improvement:** Add form edition projections with effective dates, jurisdiction, product, coverage applicability, replacement, and mandatory/optional status.

**Acceptance evidence:** Tests must reject policy issuance when required forms are missing or obsolete.

### 19. Certificate and evidence of insurance workflow

**Justification:** Insureds and third parties frequently request certificates that must reflect current coverage without altering policy terms.

**Improvement:** Add certificate requests with requester, holder, purpose, coverage snapshot, delivery method, disclaimer, and expiration.

**Acceptance evidence:** Tests must generate certificates from current policy state and block certificates on inactive policies.

### 20. Binder management

**Justification:** Temporary binders need precise duration, terms, subjectivities, authority, and conversion to policy documents.

**Improvement:** Add binder records with effective window, coverage summary, conditions, conversion deadline, issuer, and cancellation behavior.

**Acceptance evidence:** Tests must expire binders automatically and prevent overlap with issued policy terms unless linked.

### 21. Audit trail for policy transactions

**Justification:** Disputes and regulator reviews require tamper-evident reconstruction of every transaction.

**Improvement:** Add event-sourced transaction history with command, actor, role, effective date, processing date, source document, and projection checkpoint.

**Acceptance evidence:** Tests must replay owned events to reconstruct historical policy state.

### 22. Backdated transaction controls

**Justification:** Backdating endorsements, cancellations, and corrections can alter coverage and notices retroactively.

**Improvement:** Add backdate rules with allowed transaction types, maximum days, authority, affected downstream records, and impact simulation.

**Acceptance evidence:** Tests must block unauthorized backdated transactions and show impact evidence for approved ones.

### 23. Correction versus endorsement distinction

**Justification:** Data correction should not be confused with a contractual coverage change.

**Improvement:** Add correction transaction type with non-contractual field scope, reason, approval, audit note, and document reissue option.

**Acceptance evidence:** Tests must preserve original contractual terms while correcting administrative fields.

### 24. Coverage gap detection

**Justification:** Policy changes can accidentally create uncovered periods, duplicate coverage, or inconsistent effective dates.

**Improvement:** Add coverage timeline validation across terms, endorsements, cancellations, reinstatements, and renewals.

**Acceptance evidence:** Tests must flag gaps, overlaps, and conflicting effective dates.

### 25. Jurisdiction-specific notice rules

**Justification:** Cancellation, non-renewal, renewal, and material-change notices vary by jurisdiction and product.

**Improvement:** Add rule tables for notice lead times, delivery proof, required reason, template, language, and exception handling.

**Acceptance evidence:** Tests must generate different notice requirements by jurisdiction and policy type.

### 26. Communication preference controls

**Justification:** Policyholders may have preferences or consent restrictions for electronic delivery, language, accessibility, and authorized contacts.

**Improvement:** Store communication projections with consent, language, accessibility, delivery channel, and authorized-contact constraints.

**Acceptance evidence:** Tests must choose delivery channels based on preference and block unauthorized contact updates.

### 27. Producer and broker boundary

**Justification:** Policy administration needs producer-of-record and commission impact context without becoming broker management.

**Improvement:** Store producer projection, appointment status, effective period, servicing role, and producer-change evidence through declared dependencies.

**Acceptance evidence:** Boundary tests must prove producer data remains a projection and policy events carry only declared handoff data.

### 28. Claims impact projection

**Justification:** Open claims can affect cancellation, non-renewal, reinstatement, renewals, and document requests.

**Improvement:** Store claims-status projections with open claim count, loss date, coverage affected, claim hold, and freshness.

**Acceptance evidence:** Tests must block configured transactions when claims projection shows prohibited open claims.

### 29. Underwriting referral projection

**Justification:** Certain endorsements, renewals, reinstatements, and non-renewals require underwriting approval.

**Improvement:** Store underwriting decision projections with approval status, conditions, authority, expiration, and linked transaction.

**Acceptance evidence:** Tests must block transaction finalization when required underwriting approval is missing or expired.

### 30. Policy search and servicing workbench

**Justification:** Servicing teams need rapid lookup by policy, insured, coverage, document, cancellation, renewal, and exception status.

**Improvement:** Add workbench filters, saved queues, role-specific views, transaction timeline, coverage snapshot, and next-best-action panel.

**Acceptance evidence:** UI tests must expose queues for pending issuance, endorsement, renewal, cancellation, document, and exception work.

### 31. Exception taxonomy

**Justification:** Issuance, coverage, billing, document, cancellation, renewal, compliance, and data-quality exceptions need different ownership.

**Improvement:** Add exception categories, severity, blocked action, owner, SLA, escalation, closure evidence, and reopen reason.

**Acceptance evidence:** Tests must route exception types to correct workbench queues and emit exception events.

### 32. Renewal offer comparison

**Justification:** Renewal specialists need to compare expiring terms, proposed terms, premium projection, forms, and conditions.

**Improvement:** Add renewal comparison view with changed coverages, forms, deductibles, limits, premium impact, and required policyholder action.

**Acceptance evidence:** Tests must generate comparison evidence for renewal offer, non-renewal, and rewrite scenarios.

### 33. Bulk renewal batch controls

**Justification:** Renewal cycles can involve thousands of policies and require throttling, exception handling, and reproducible evidence.

**Improvement:** Add renewal batches with selection criteria, dry-run counts, excluded policies, approval, execution progress, and rollback plan.

**Acceptance evidence:** Tests must simulate renewal batches and show per-policy outcomes.

### 34. Regulatory hold and moratorium support

**Justification:** Disasters, market exits, legal orders, or regulatory directives may pause cancellations or non-renewals.

**Improvement:** Add hold rules by jurisdiction, peril, policy type, effective dates, blocked actions, and release criteria.

**Acceptance evidence:** Tests must block transactions during active holds and require release evidence.

### 35. Product configuration boundary

**Justification:** Policy administration applies product rules but should not own product catalog or rating definitions.

**Improvement:** Store product version projections with allowed coverages, forms, transaction types, and effective dates from declared dependencies.

**Acceptance evidence:** Boundary tests must prove product data is projected and not mutated.

### 36. Policyholder service request intake

**Justification:** Address changes, coverage questions, document requests, cancellations, and endorsement requests arrive through service channels.

**Improvement:** Add request intake with type, requester authority, requested change, source channel, linked policy, and governed command preview.

**Acceptance evidence:** Tests must require authorization checks before converting service requests into policy transactions.

### 37. Agent-assisted document interpretation

**Justification:** Signed forms, cancellation requests, reinstatement evidence, and policyholder instructions arrive as unstructured documents.

**Improvement:** Add assistant extraction for request type, effective date, party role, coverage changes, signatures, and missing fields with confidence scores.

**Acceptance evidence:** Tests must require human confirmation and retain source-page evidence for accepted fields.

### 38. Agent-guided policy transaction drafting

**Justification:** Users need help creating accurate endorsements, cancellations, renewals, and document requests without raw datastore access.

**Improvement:** Add assistant skills that propose transaction drafts, cite rules, show document requirements, and produce governed CRUD previews.

**Acceptance evidence:** Tests must reject agent proposals that lack affected record, rule version, and approval requirement.

### 39. Agent safety restrictions

**Justification:** AI must not silently cancel coverage, issue policies, non-renew policies, or alter contractual terms.

**Improvement:** Require high-impact agent proposals to be explicitly labeled, approval-routed, and blocked until authorized by a permitted user.

**Acceptance evidence:** Tests must block unapproved AI writes for cancellation, issuance, endorsement, and renewal actions.

### 40. Transaction impact simulation

**Justification:** Users need to understand downstream effects before changing coverage or status.

**Improvement:** Add simulation for coverage timeline, documents, premium projection, billing status, notices, renewal eligibility, and dependency events.

**Acceptance evidence:** Tests must show simulation outputs and prove simulations do not mutate owned records.

### 41. AppGen-X event specialization

**Justification:** Policy administration composes with underwriting, billing, claims, documents, producers, product, and compliance by events.

**Improvement:** Define typed events for policy issued, coverage changed, endorsement approved, renewal offered, cancellation noticed, reinstatement approved, and document rendered.

**Acceptance evidence:** Event tests must verify idempotency keys, retry behavior, dead-letter evidence, and declared dependency usage.

### 42. Policy document correction and reissue

**Justification:** Document errors require corrected output without changing underlying contractual transaction unless needed.

**Improvement:** Add reissue records with reason, affected document, corrected template, delivery proof, supersession, and audit note.

**Acceptance evidence:** Tests must preserve superseded document hashes and show current document status.

### 43. Data-quality score for policies

**Justification:** Missing insured roles, stale projections, invalid coverage dates, and document mismatches create service and compliance risk.

**Improvement:** Add data-quality scoring by policy with issue type, severity, owner, remediation task, and trend.

**Acceptance evidence:** Tests must flag incomplete policies and show remediation queues.

### 44. Portfolio operation analytics

**Justification:** Managers need insight into renewal workload, cancellation risk, document defects, endorsement volume, and exception aging.

**Improvement:** Add analytics for transaction throughput, SLA, backlog, exception age, renewal retention, cancellation reasons, and document delivery success.

**Acceptance evidence:** UI tests must expose metric cards and drilldowns tied to owned records.

### 45. Cryptographic policy evidence packet

**Justification:** Policy disputes require tamper-evident evidence of terms, notices, transactions, and documents.

**Improvement:** Add hash-linked packets for issuance, endorsement, renewal, cancellation, reinstatement, and document delivery evidence.

**Acceptance evidence:** Tests must detect altered packet contents and verify packet generation from owned records.

### 46. Tenant and book-of-business isolation

**Justification:** Carriers, programs, products, and managing agencies may need separated rules, permissions, templates, and data visibility.

**Improvement:** Add tenant, program, and book-of-business scoping to policy actions, workbench queues, rules, documents, and projections.

**Acceptance evidence:** Tests must prevent cross-tenant policy reads or transaction commands.

### 47. Release smoke scenarios

**Justification:** Generated apps need evidence that realistic policy administration workflows execute after composition.

**Improvement:** Add smoke scenarios for policy issuance, endorsement, renewal, cancellation, reinstatement, document generation, and non-renewal.

**Acceptance evidence:** Release evidence must show owned records, AppGen-X events, UI artifacts, and boundary checks for every scenario.

### 48. Cross-PBC boundary proof

**Justification:** Policy administration touches underwriting, claims, billing, product, documents, producers, compliance, and customer domains without owning them.

**Improvement:** Add automated proof that generated models, services, routes, handlers, projections, and agent commands use only owned tables plus declared APIs/events.

**Acceptance evidence:** Tests must fail on undeclared table references and pass for declared projection or event dependency references.

### 49. Cancellation and reinstatement dashboard

**Justification:** Operations teams need a focused surface for high-risk policy status changes.

**Improvement:** Add dashboard queues for pending notices, cure windows, moratorium holds, reinstatement requests, proof of delivery, and blocked cancellations.

**Acceptance evidence:** UI tests must show countdowns, blockers, and next actions for cancellation and reinstatement cases.

### 50. Renewal command center

**Justification:** Renewal teams need one surface for data refresh, underwriting review, offers, notices, non-renewals, and exceptions.

**Improvement:** Add renewal command center with cycle filters, policy cohorts, offer status, required actions, document status, and assistant-guided review.

**Acceptance evidence:** UI tests must expose renewal cycle queues and allow governed renewal actions without raw datastore access.
