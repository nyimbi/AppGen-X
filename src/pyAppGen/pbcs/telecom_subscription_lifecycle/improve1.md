# Telecom Subscription Lifecycle Improvement Backlog

## Current Domain Evidence Used

- Stable package key: `telecom_subscription_lifecycle`.
- Manifest and specification describe the package scope as plans, activations, SIM and eSIM lifecycle, usage, roaming, plan changes, churn controls, and service entitlements.
- Owned tables named in the package: `subscriber_account`, `service_plan`, `sim_profile`, `activation_request`, `usage_session`, `roaming_event`, `churn_risk`, `telecom_subscription_lifecycle_policy_rule`, `telecom_subscription_lifecycle_runtime_parameter`, `telecom_subscription_lifecycle_schema_extension`, `telecom_subscription_lifecycle_control_assertion`, and `telecom_subscription_lifecycle_governed_model`.
- Declared APIs: `POST /subscriber-accounts`, `POST /service-plans`, `POST /sim-profiles`, `POST /activation-requests`, `POST /usage-sessions`, and `GET /telecom-subscription-lifecycle-workbench`.
- Declared emitted events: `TelecomSubscriptionLifecycleCreated`, `TelecomSubscriptionLifecycleUpdated`, `TelecomSubscriptionLifecycleApproved`, and `TelecomSubscriptionLifecycleExceptionOpened`.
- Declared consumed events: `PolicyChanged`, `CustomerUpdated`, and `SupplierQualified`.
- UI entrypoints already called out in the package: `TelecomSubscriptionLifecycleWorkbench`, `TelecomSubscriptionLifecycleDetail`, and `TelecomSubscriptionLifecycleAssistantPanel`.
- The specification already commits the package to owned-table boundaries, AppGen-X outbox/inbox patterns, governed agent execution, release evidence, and idempotent handlers.

### 1. Canonical customer subscription aggregate
**Justification:** The current package lists separate tables for subscriber account, service plan, SIM profile, activation request, usage session, roaming event, and churn risk, but the backlog should force a single domain view of one customer subscription from order to exit.
**Improvement:** Define a canonical subscription aggregate that ties customer party, billing party reference, line or seat, MSISDN, active SIM or eSIM, current plan, active add-ons, network state, churn posture, and evidence links into one lifecycle model with explicit ownership boundaries.
**Acceptance evidence:** Data model sketches, workbench mock states, and contract examples show one subscription can be reconstructed without joining through undocumented status conventions.

### 2. Subscription lifecycle state machine
**Justification:** Telecom subscriptions move through operationally distinct states that matter for provisioning, billing boundary handoff, customer messaging, and regulatory evidence.
**Improvement:** Define lifecycle states such as draft, pending_identity, pending_sim_assignment, pending_port, pending_activation, active, partially_barred, suspended, disconnect_pending, disconnected, win_back_eligible, and archived, with allowed transitions and actor rules.
**Acceptance evidence:** A transition matrix, invalid-transition examples, and event-state mapping prove each lifecycle move is explicit and testable.

### 3. Telecom identifier model for MSISDN, ICCID, IMSI, and EID
**Justification:** Subscription lifecycle work becomes brittle when phone number, SIM card, network identity, and eSIM hardware identifiers are treated as interchangeable.
**Improvement:** Add a domain identity model that separates MSISDN, ICCID, IMSI, EID, activation code, porting reference, and customer-facing subscription reference, including current value, history, status, and assignment timestamps.
**Acceptance evidence:** Field definitions, identifier history examples, and validation rules show identifier reuse, recycling, and replacement can be audited without ambiguity.

### 4. Customer, payer, and subscription relationship rules
**Justification:** Telecom subscriptions commonly support consumer, business, family, and reseller structures where the service user is not always the paying or approving party.
**Improvement:** Model subscriber, payer, account owner, employer sponsor, and delegated administrator roles so plan changes, add-ons, suspensions, and cancellations can enforce the right approval path.
**Acceptance evidence:** Role matrices and sample account hierarchies demonstrate one customer account can hold multiple subscriptions with different payer and authority patterns.

### 5. Physical SIM inventory and fulfillment boundary
**Justification:** The package covers SIM lifecycle, so it needs a clear boundary between owning subscription-side SIM assignment and merely referencing external warehouse or courier operations.
**Improvement:** Track SIM inventory states such as available, reserved, assigned, shipped, delivered, activated, swapped_out, lost, and retired, while keeping shipping and warehouse execution outside the PBC boundary.
**Acceptance evidence:** Boundary notes, state diagrams, and example flows show which fields are owned inside the package and which statuses are mirrored from external fulfillment systems.

### 6. eSIM profile issuance and installation flow
**Justification:** eSIM activation has a different operational shape from physical SIM assignment and needs first-class treatment instead of being folded into generic SIM fields.
**Improvement:** Model EID capture, profile reservation, profile download token or QR issuance, installation attempts, confirmation callbacks, timeout handling, and fallback to assisted activation when self-service fails.
**Acceptance evidence:** Sequence diagrams and acceptance scenarios cover successful install, expired activation token, repeated download attempts, and device-incompatible eSIM requests.

### 7. SIM swap and eSIM change controls
**Justification:** SIM swap and eSIM reissue events are both high-risk and high-volume operations with fraud exposure and customer-impact risk.
**Improvement:** Add explicit swap and reissue workflows with cool-off rules, identity re-verification, fraud alerts, prior-SIM deactivation timing, and customer notification requirements before service moves to a new credential.
**Acceptance evidence:** Risk decision examples, exception reasons, and timeline evidence show the package can distinguish routine replacement from suspicious transfer patterns.

### 8. Plan catalog versioning and effective dating
**Justification:** A subscription lifecycle backlog must address how plans change over time without rewriting history for already-active subscriptions.
**Improvement:** Version `service_plan` records by market, channel, customer segment, effective date, renewal cadence, contract term, included allowances, and retirement date so older subscriptions keep their original plan semantics.
**Acceptance evidence:** Plan version examples and migration rules demonstrate future subscriptions can use a new plan version while existing lines continue against the historical version they accepted.

### 9. Plan eligibility and compatibility engine
**Justification:** Plan activation rules depend on network technology, device class, customer type, market, credit posture, and sometimes SIM or eSIM capability.
**Improvement:** Expand policy rules so plan selection checks prepaid or postpaid compatibility, 4G or 5G eligibility, eSIM support, roaming eligibility, minimum identity checks, and mutually exclusive product combinations.
**Acceptance evidence:** Rule tables and pass-fail examples show rejected plan combinations are explainable to customers and agents before activation is attempted.

### 10. Future-dated plan changes and migrations
**Justification:** Customers frequently schedule plan moves at the next renewal or billing cycle rather than changing immediately.
**Improvement:** Add future-dated plan change requests with previewed effective date, cancellation window, dependency checks, and conflict handling when another change, suspension, or port request is already pending.
**Acceptance evidence:** Timeline examples prove the package can stage, amend, cancel, and execute future plan changes without losing the original customer intent.

### 11. Add-on catalog and stacking rules
**Justification:** Telecom subscriptions rarely stop at the base plan; add-ons drive real customer behavior and often create the hardest policy conflicts.
**Improvement:** Model add-on categories such as data boosters, roaming passes, international calling packs, device insurance, content bundles, and temporary speed upgrades with stacking, exclusivity, and prerequisite rules.
**Acceptance evidence:** Catalog examples show which add-ons can coexist, which replace each other, and which expire automatically when the base plan changes.

### 12. Add-on proration, renewal, and exhaustion semantics
**Justification:** Add-ons behave differently depending on whether they are one-time, recurring, pool-based, or tied to the billing cycle.
**Improvement:** Define depletion, rollover, proration, recurring renewal, grace use, and termination behavior for each add-on type, including how usage thresholds interact with purchased boosters.
**Acceptance evidence:** Calculation examples and renewal cases show customers and agents can see why an add-on renewed, expired, or was consumed faster than expected.

### 13. Activation request decomposition
**Justification:** Activation is not one atomic event; it is a chain of validations and network actions that can fail independently.
**Improvement:** Split `activation_request` into sub-steps for identity approval, customer subscription validation, plan lock, SIM or eSIM binding, provisioning order creation, service test, welcome communication, and ready-for-billing-boundary handoff.
**Acceptance evidence:** A staged activation checklist and failure injection scenarios prove the package can stop, resume, or retry activation without losing progress.

### 14. Provisioning orchestration and network dependency tracking
**Justification:** The manifest says the package owns activation and service entitlements, so the backlog needs explicit provisioning logic rather than a generic “approved” outcome.
**Improvement:** Track provisioning work against network elements and service domains such as core subscriber registry, data policy, voice features, messaging enablement, voicemail, APN defaults, and partner entitlements, each with its own completion signal.
**Acceptance evidence:** Dependency maps and adapter contracts show provisioning outcomes are visible as structured evidence instead of unparsed vendor messages.

### 15. Activation rollback and compensation logic
**Justification:** Partial provisioning failures can leave a customer charged, assigned, or notified without actually being service-ready.
**Improvement:** Define compensation logic for partial activation failures, including unbinding SIM inventory, cancelling incomplete eSIM profiles, reversing service features, and suppressing downstream billing-boundary release until the subscription is coherent again.
**Acceptance evidence:** Failure-path scenarios prove rollback behavior is deterministic and leaves auditable evidence of what was reversed and what still needs intervention.

### 16. Number portability case model
**Justification:** Number portability is a major telecom-specific capability and should not be hidden inside a generic activation request note field.
**Improvement:** Add a dedicated portability case model with port_in, port_out, internal_transfer, donor network, recipient network, validation stage, cutover window, temporary number option, and fallback path.
**Acceptance evidence:** Sample portability cases cover successful port-in, rejected donor validation, delayed cutover, and customer-aborted port requests.

### 17. Port-in validation and donor checkpoint coverage
**Justification:** Port-in failures are often caused by data mismatch, expired authorization, locked numbers, or mistimed cutover expectations.
**Improvement:** Capture validation checkpoints for customer identity match, account number match, authorization proof, number status, desired cutover date, and donor response codes before the port moves into execution.
**Acceptance evidence:** Validation evidence and rejected-case examples show exactly why a port-in can or cannot proceed.

### 18. Port-out protection and customer authorization controls
**Justification:** Port-out operations are high-risk because they can be used for fraud or account takeover if approval is weak.
**Improvement:** Add explicit port-out protections such as transfer lock flags, recent SIM-swap cooling periods, high-risk channel detection, extra identity checks, and durable proof of customer consent before release.
**Acceptance evidence:** Risk scenarios and approval traces show the package can block or escalate suspicious port-out attempts without blocking legitimate churn events forever.

### 19. Suspension, barring, and resume lifecycle
**Justification:** Suspension is not one thing in telecom; voluntary pause, non-payment, fraud hold, lost device, and regulator-driven barring all have different consequences.
**Improvement:** Model suspension reasons and service-level impact separately so voice, SMS, data, roaming, premium services, and outbound usage can be barred or resumed in combinations that match the real operational need.
**Acceptance evidence:** Suspension matrices and restore flows demonstrate the difference between a full service stop, a partial bar, and a temporary self-service pause.

### 20. Threshold-based throttling and suspension actions
**Justification:** Usage thresholds often trigger throttling, spend protection, or temporary bars before a customer explicitly changes plan.
**Improvement:** Add domain rules for soft threshold alert, hard cap, fair-use throttle, roaming spend block, and fraud-triggered usage bar with configurable thresholds by plan and add-on.
**Acceptance evidence:** Threshold cases show 80 percent alert, 100 percent block, purchased booster recovery, and automatic unblock when policy conditions are satisfied.

### 21. Usage normalization and billing-input boundary
**Justification:** The package owns usage sessions, but it should distinguish between operational usage truth and the external rating or invoicing ledger.
**Improvement:** Normalize voice, SMS, and data usage into a common usage evidence model with time zone, session source, duplicate detection, unit conversion, and subscription linkage before emitting clean charge-advice or consumption events outward.
**Acceptance evidence:** Sample usage records and boundary notes prove the package can explain raw usage while avoiding ownership of invoice totals or tax calculations.

### 22. Real-time usage threshold notifications
**Justification:** Customers and agents need timely visibility into threshold crossings to prevent bill shock and avoid unnecessary churn.
**Improvement:** Add near-real-time threshold evaluation for data, voice, SMS, and roaming usage with customer notification preferences, in-app workbench alerts, and agent-facing intervention recommendations.
**Acceptance evidence:** Notification timing examples and preference handling prove the same threshold event can drive customer messaging, agent queueing, and release evidence without duplicate alerts.

### 23. Shared pools and family-plan allowance allocation
**Justification:** A telecom subscription backlog is incomplete if it only models single-line consumption and ignores pooled allowances or sponsored lines.
**Improvement:** Support shared data or service pools with owner line, member lines, allocation policy, reserve capacity, priority rules, and member-level throttling when the shared pool is exhausted.
**Acceptance evidence:** Family-plan and business-pool scenarios show one member can be restricted without forcing a full pool suspension unless policy requires it.

### 24. Roaming entitlement catalog
**Justification:** Roaming behavior depends on destination, partner agreements, pass purchases, and plan-specific inclusion, not just a Boolean roaming flag.
**Improvement:** Model roaming zones, destination groups, included countries, daily passes, monthly passes, permanent roaming restrictions, and partner-specific eligibility as plan or add-on entitlements.
**Acceptance evidence:** Destination examples show why the same subscription is included in one country, barred in another, and offered a paid roaming pass in a third.

### 25. Roaming shock prevention and spend protection
**Justification:** Roaming is one of the fastest ways to create customer complaints, involuntary churn, and support escalation if controls are vague.
**Improvement:** Add roaming spend caps, data session cutoffs, default-off policies for high-risk destinations, and explicit customer confirmation requirements before high-cost roaming usage is enabled.
**Acceptance evidence:** Spend-cap scenarios and control evidence show roaming can be paused, re-enabled, or upgraded without confusing ownership of actual billing calculations.

### 26. Roaming provisioning and partner exception handling
**Justification:** Even when a customer is entitled to roam, partner outages, attach failures, and stale partner configuration create operational exceptions.
**Improvement:** Track roaming provisioning status, visited network failures, partner enablement mismatches, manual override paths, and remediation ownership for roaming exceptions.
**Acceptance evidence:** Exception examples demonstrate how an agent can see whether the problem is plan entitlement, provisioning lag, destination policy, or partner failure.

### 27. Billing boundary and charge-advice handoff
**Justification:** The package description includes plan changes, usage, roaming, and entitlements, but it still must respect a clean billing boundary.
**Improvement:** Define exactly which financial artifacts this PBC owns, such as charge advice, proration preview, allowance consumption evidence, and effective-date decisions, while keeping invoicing, taxation, collections, and ledger posting outside the boundary.
**Acceptance evidence:** Boundary documentation and event payload examples show downstream billing systems receive structured facts without the package taking ownership of invoices or payments.

### 28. Prepaid, postpaid, and hybrid subscription semantics
**Justification:** Subscription lifecycle logic differs sharply between prepaid, postpaid, and hybrid offers, especially around activation gating and threshold actions.
**Improvement:** Model balance buckets, credit exposure flags, recharge dependency, grace periods, reserve thresholds, and hybrid rules where some entitlements are prepaid-controlled and others are billed later.
**Acceptance evidence:** Product examples prove activation, suspension, and add-on purchase rules differ correctly by commercial model.

### 29. Mid-cycle charge-impact previews
**Justification:** Customers and agents need a believable preview before changing plans, adding features, or resuming service mid-cycle.
**Improvement:** Add preview logic for proration direction, one-time fees, contract impacts, add-on carryover, and next-cycle effect, while clearly labeling what is an estimated billing-boundary output versus a final invoice amount.
**Acceptance evidence:** Preview screens and scenario tables show the package can explain likely financial impact without pretending to own the final bill.

### 30. Billing dispute linkage without billing ownership
**Justification:** Customers challenge charges using usage, activation, roaming, and add-on evidence that lives in this PBC even though the official bill is elsewhere.
**Improvement:** Create dispute-support evidence bundles that link invoice references to subscription events, usage sessions, roaming activity, threshold notifications, and provisioning timelines for agent review.
**Acceptance evidence:** Evidence bundle examples show an agent can answer “why was this charged” from package-owned facts without mutating the external billing ledger.

### 31. Churn reason taxonomy and exit intelligence
**Justification:** Churn controls in the manifest should translate into specific telecom reasons instead of a generic risk score with no operational meaning.
**Improvement:** Expand `churn_risk` into reason codes such as price pressure, coverage issues, repeated provisioning failure, roaming dissatisfaction, bill shock, add-on confusion, device loss, and competitor portability intent.
**Acceptance evidence:** Reason-code examples and scoring notes show the same churn score can be decomposed into actionable drivers for product, care, and retention teams.

### 32. Retention offer governance and save journeys
**Justification:** Retention actions affect margin and customer trust, so they need domain controls rather than ad hoc agent discretion.
**Improvement:** Model save offers such as temporary discount, add-on waiver, roaming pass credit, plan downgrade recommendation, suspension instead of cancellation, and contract reset with clear eligibility rules and approval thresholds.
**Acceptance evidence:** Offer decision traces show why a subscription qualified, who approved the offer, and what post-offer outcome was recorded.

### 33. Cancellation, grace, and win-back lifecycle
**Justification:** Customer subscriptions often pass through a grace period, temporary disconnect, number quarantine, or win-back window rather than an immediate permanent end state.
**Improvement:** Add explicit states and timers for cancel_requested, grace_active, disconnected, number_quarantine, and win_back_eligible with rules for reactivation, number recovery, and evidence retention.
**Acceptance evidence:** Cancellation timelines show a line can be stopped, recovered, or finally closed with customer-visible and agent-visible milestones.

### 34. Customer self-service workbench improvements
**Justification:** The current UI fragments need backlog items that make the telecom lifecycle understandable to customers without agent intervention.
**Improvement:** Extend the customer-facing portion of `TelecomSubscriptionLifecycleWorkbench` so users can see plan details, active add-ons, SIM or eSIM status, usage thresholds, roaming controls, pending changes, and churn-sensitive cancellation options from one place.
**Acceptance evidence:** UI acceptance notes and journey maps prove a customer can complete common lifecycle actions without navigating contradictory screens.

### 35. Agent operations console and queue design
**Justification:** Telecom operations teams need queue-based work across activation, portability, suspension, roaming, and churn events rather than a single generic record detail page.
**Improvement:** Add agent queues for pending activation, provisioning exception, SIM swap review, portability exception, threshold intervention, roaming failure, and retention outreach with domain-specific sort keys and SLA badges.
**Acceptance evidence:** Queue definitions and sample cards show each work item exposes the next action, blocking dependency, and required skill level.

### 36. Governed agent skills and mutation playbooks
**Justification:** The package already calls out AI agent task assistance, but telecom lifecycle actions need tightly bounded skills that reflect real operational authority.
**Improvement:** Define agent skills such as explain_plan_change, review_port_request, propose_add_on_recovery, prepare_sim_swap_case, classify_roaming_exception, and assemble_release_evidence, each with read scope, allowed mutations, and mandatory human confirmation points.
**Acceptance evidence:** Skill specs and preview payloads show the assistant can help an operator without bypassing approval, boundary, or evidence requirements.

### 37. Event taxonomy across the subscription journey
**Justification:** Four generic package events are not enough to express telecom operational milestones that other PBCs or audit tooling care about.
**Improvement:** Extend the domain event catalog with lifecycle-specific events such as SubscriptionRequested, PlanCommitted, SimAssigned, EsimProfileIssued, ActivationProvisioningStarted, ActivationCompleted, PortingRequested, SuspensionApplied, RoamingEntitlementChanged, UsageThresholdBreached, and RetentionOfferAccepted.
**Acceptance evidence:** Event definitions and sample payloads show external consumers can reason about business milestones without scraping record snapshots.

### 38. Outbox, inbox, idempotency, and causal ordering
**Justification:** Telecom lifecycle flows receive duplicates, retries, and out-of-order updates from network and partner systems, so event discipline is essential.
**Improvement:** Add domain-level idempotency keys, correlation IDs, causation IDs, replay-safe handlers, and ordering rules for activation, portability, roaming, and threshold events.
**Acceptance evidence:** Duplicate and out-of-order event scenarios prove the package preserves a coherent subscription history under repeated delivery.

### 39. Exception taxonomy and remediation evidence
**Justification:** A generic exception queue hides whether the problem is plan policy, provisioning failure, portability rejection, roaming mismatch, or billing-boundary drift.
**Improvement:** Define exception categories, severity, owner role, retry policy, customer-impact flag, and closure evidence requirements for each telecom failure mode.
**Acceptance evidence:** Exception examples show agents can distinguish auto-retry candidates from cases that require customer contact or policy approval.

### 40. Release evidence for telecom end-to-end flows
**Justification:** Release evidence should prove more than package import success; it should prove the hardest telecom journeys still behave correctly.
**Improvement:** Require release evidence packs for new activation, eSIM install, SIM swap, port-in, roaming enablement, threshold breach, add-on purchase, suspension and resume, cancellation, and win-back scenarios.
**Acceptance evidence:** A release matrix maps each critical journey to tests, screenshots, event traces, and rollback notes stored in `RELEASE_EVIDENCE.md`.

### 41. Operational SLA and aging metrics
**Justification:** Telecom lifecycle quality is measured in elapsed time as much as in correctness because delays trigger churn and regulator complaints.
**Improvement:** Add SLA targets and aging buckets for activation completion, eSIM install success, portability cutover, suspension clearance, roaming restoration, and churn-save outreach.
**Acceptance evidence:** Metric definitions and dashboard examples show aging can be measured at subscription, queue, and exception level.

### 42. Policy rules and runtime parameter governance
**Justification:** The manifest already includes policy-rule and runtime-parameter tables, so the backlog should force telecom-specific governance rather than generic knobs.
**Improvement:** Define governed parameters for fraud hold duration, porting cutover windows, threshold percentages, roaming caps, plan-change notice periods, save-offer limits, and agent approval thresholds with change control and impact preview.
**Acceptance evidence:** Parameter history and simulation examples show policy changes can be reviewed before they affect live customer subscriptions.

### 43. Audit trail with actor, channel, and device evidence
**Justification:** Telecom disputes often hinge on who performed an action, through which channel, and from which customer device or assisted session.
**Improvement:** Expand audit evidence to capture actor type, channel, session provenance, device fingerprint or assisted-channel identifier, approval path, and customer notification linkage for every critical mutation.
**Acceptance evidence:** Audit examples show the package can prove whether a change came from self-service, call center, retail agent, or automated workflow.

### 44. Tenant, brand, and market isolation
**Justification:** Telecom catalogs, numbering rules, roaming policies, and regulatory steps differ by brand and market even when the underlying package is reused.
**Improvement:** Isolate plan catalogs, portability rules, number formats, roaming zones, suspension policies, and UI labels by tenant and market without letting cross-tenant defaults leak into another operator context.
**Acceptance evidence:** Multi-market examples show one deployment can operate multiple brands or countries with independent policy and release evidence.

### 45. Document intake for portability and customer consent
**Justification:** Portability, business account changes, and fraud-sensitive SIM operations often require customer-supplied documents or recorded consents.
**Improvement:** Add structured intake for authorization forms, identity documents, signed corporate approvals, and consent artifacts so the agent and workbench can classify, validate, and reference them during activation, porting, and dispute handling.
**Acceptance evidence:** Intake examples show document-derived facts become traceable evidence instead of free-text attachments that operators must interpret manually.

### 46. Test data factory for telecom lifecycle edge cases
**Justification:** Release confidence will stay shallow unless test assets cover realistic identifier formats, plan structures, and failure modes.
**Improvement:** Build synthetic test fixtures for MSISDN pools, ICCID and EID values, prepaid and postpaid plans, roaming destinations, pooled allowances, porting cases, and fraudulent SIM-swap patterns.
**Acceptance evidence:** Fixture catalogs show teams can spin up repeatable scenarios for activation, roaming, threshold, churn, and UI evidence generation.

### 47. Scenario simulation for plan, roaming, and churn outcomes
**Justification:** The package advertises counterfactual simulation, and telecom operations need that capability where plan or roaming changes have customer-impact risk.
**Improvement:** Add what-if simulation for future plan migrations, add-on purchases, roaming enablement, threshold changes, save offers, and suspensions so operators can see projected lifecycle effects before committing.
**Acceptance evidence:** Simulation reports compare current path versus proposed path and clearly label which outcomes are predictions versus confirmed state.

### 48. Data quality controls and cross-boundary reconciliation
**Justification:** Subscription truth can drift when provisioning, SIM status, usage evidence, and billing references are updated by different systems at different times.
**Improvement:** Add reconciliation jobs and exception reports that compare active subscriptions, active SIM or eSIM assignments, network provisioning confirmations, latest usage evidence, and downstream billing references for mismatch detection.
**Acceptance evidence:** Reconciliation outputs and triage rules show stale or contradictory records are surfaced before they create customer harm.

### 49. API contract hardening for lifecycle endpoints
**Justification:** The declared APIs are the package boundary, so the backlog needs precise contracts for telecom-grade failure handling and idempotency.
**Improvement:** Tighten request and response contracts for subscriber creation, plan creation, SIM profile handling, activation requests, usage-session intake, and workbench retrieval with idempotency keys, async operation status, domain error codes, and evidence links.
**Acceptance evidence:** Contract examples and negative cases show API consumers can distinguish validation failure, pending async work, duplicate submission, and external dependency delay.

### 50. Production readiness scorecard and go-live evidence
**Justification:** The package should not be considered ready until domain behavior, UI, agent skills, events, and release evidence line up across the whole telecom subscription lifecycle.
**Improvement:** Add a go-live scorecard that measures readiness across customer subscriptions, SIM and eSIM flows, plans, activation, provisioning, portability, add-ons, suspensions, thresholds, roaming, billing boundary, churn and retention, UI, agent skills, events, and release evidence.
**Acceptance evidence:** A final readiness checklist ties each domain area to named tests, workbench evidence, event traces, and operational runbooks required before release approval.
