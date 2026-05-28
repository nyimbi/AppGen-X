# Gaming and Casino Operations PBC Manual Improvement Backlog

## Purpose

This manual backlog for `gaming_casino_operations` focuses the PBC on auditable casino-floor execution: patron enrollment, table and slot activity, cage controls, jackpots, player ratings, compliance, responsible gaming, governed agent support, workbench operations, event boundaries, and release readiness.

## Current Domain Evidence Used

- Stable PBC key: `gaming_casino_operations`.
- Domain purpose: players, tables, slots, compliance, responsible gaming, loyalty, payouts, and gaming floor operations.
- Owned domain tables: `player_profile`, `table_game`, `slot_machine`, `wager_session`, `payout`, `responsible_gaming_case`, `gaming_compliance`, `gaming_casino_operations_policy_rule`, `gaming_casino_operations_runtime_parameter`, `gaming_casino_operations_schema_extension`, `gaming_casino_operations_control_assertion`, `gaming_casino_operations_governed_model`.
- Public APIs: `POST /player-profiles`, `POST /table-games`, `POST /slot-machines`, `POST /wager-sessions`, `POST /payouts`, `GET /gaming-casino-operations-workbench`.
- Emitted AppGen-X events: `GamingCasinoOperationsCreated`, `GamingCasinoOperationsUpdated`, `GamingCasinoOperationsApproved`, `GamingCasinoOperationsExceptionOpened`.
- Consumed AppGen-X events: `PolicyChanged`, `CustomerUpdated`, `SupplierQualified`.
- Workflow surfaces: `gaming_casino_operations_create_player_profile_workflow` and `gaming_casino_operations_record_table_game_workflow`.
- UI fragments: `GamingCasinoOperationsWorkbench`, `GamingCasinoOperationsDetail`, and `GamingCasinoOperationsAssistantPanel`.
- Release documents: `SPECIFICATION.md` and `RELEASE_EVIDENCE.md`.

## 50 High-Impact Improvements

### 1. Patron Identity Confidence and Enrollment Review

**Justification:** Casino floors cannot tolerate duplicate patron identities, missing age checks, or silent merges that blur exclusion, tax, and rating history.

**Improvement:** Extend `player_profile` with identity confidence, duplicate-candidate review, government-ID evidence, age-verification status, property enrollment state, and reversible merge decisions before a patron becomes active on the floor.

**Acceptance evidence:** Tests must flag duplicate patrons without auto-merging them, require reviewer evidence for a merge or rejection, and show identity uncertainty in `GamingCasinoOperationsDetail`.

### 2. Patron Status, Restrictions, and Floor Access Semantics

**Justification:** A patron can be active for play while blocked from markers, barred from a property, cooling off under responsible-gaming policy, or restricted to specific game types.

**Improvement:** Add `player_profile` states and flags for active, VIP, self-excluded, barred, suspicious-activity-review, payment-restricted, ratings-suppressed, and reinstatement-pending, with effective dates and issuing authority.

**Acceptance evidence:** Tests must block table or slot session creation when patron restrictions apply, preserve who applied the restriction, and surface the exact floor-access reason in workbench queues.

### 3. Table Opening, Closing, and Shift Ownership

**Justification:** Pit operations depend on knowing exactly when a table opened, who owned it, what inventory it started with, and whether it closed cleanly at shift end.

**Improvement:** Expand `table_game` with pit, table number, game variant, opening bankroll, dealer assignment, supervisor assignment, shift window, open-close checklist, and closure exception reason.

**Acceptance evidence:** Tests must reject a table close when inventory reconciliation or shift signoff is missing and must reconstruct the table's shift ownership from stored events.

### 4. Table Fill, Credit, Buy-In, and Color-Up Evidence

**Justification:** Table inventory changes are high-risk events that need a precise chain from pit request to cage fulfillment to supervisor confirmation.

**Improvement:** Add table inventory event records under `table_game` for fills, credits, player buy-ins, marker redemptions, color-ups, and emergency inventory adjustments with dual-control evidence.

**Acceptance evidence:** Tests must trace each inventory movement to the initiating actor, approval, and resulting table balance and must open an exception when one link is missing.

### 5. Slot Asset Configuration and Conversion Governance

**Justification:** Slot revenue and compliance depend on accurate denomination, paytable, progressive link, cabinet location, and conversion history.

**Improvement:** Extend `slot_machine` with cabinet identifier, bank location, denomination set, paytable version, progressive participation, conversion history, floor-move history, and jurisdiction approval state.

**Acceptance evidence:** Tests must show a conversion cannot activate without the required approval set and must preserve prior configuration history for audit replay.

### 6. Slot Tilt, Offline, and Meter Snapshot Recovery

**Justification:** Slot devices fail in ways that create dispute, jackpot, and drop-count risk if meter state is not captured at the moment of interruption.

**Improvement:** Add `slot_machine` outage events for tilt, offline, door-open, printer fault, bill validator fault, and communication loss, each with captured meter snapshots and recovery workflow state.

**Acceptance evidence:** Tests must preserve the last accepted meter reading before recovery, block reopening a machine with unresolved fault evidence, and route the issue to slot ops queues.

### 7. Unified Wager Session Context Across Tables and Slots

**Justification:** Hosts, surveillance, and compliance need one canonical play session lens even though tables and slots generate very different operational signals.

**Improvement:** Make `wager_session` the shared session envelope for patron, asset, start-stop time, host touchpoint, rating status, dispute flag, and loyalty-earn evidence while preserving table-versus-slot detail.

**Acceptance evidence:** Tests must prove a session can represent table or slot play without mixing the two event models and that workbench session views cite the owning asset.

### 8. Table Player Rating Capture and Theoretical Win Review

**Justification:** Manual ratings drive host decisions, comps, and revenue estimates, so weak controls here distort both guest treatment and floor profitability.

**Improvement:** Add `wager_session` rating evidence for average bet, game pace, time played, skill adjustment, rating source, supervisor override, and host-facing comp justification.

**Acceptance evidence:** Tests must preserve the original rating alongside any correction, require reason capture for overrides, and show when a host acted on provisional rather than final ratings.

### 9. Slot Card-In and Card-Out Loyalty Evidence Boundary

**Justification:** Slot play commonly starts with a card-in event, but the PBC should own session evidence rather than an enterprise loyalty balance ledger.

**Improvement:** Record loyalty-related evidence in `wager_session` for card-in, card-out, linked offer, promotional multiplier, and earning basis while emitting clean handoff events for downstream loyalty accounting.

**Acceptance evidence:** Tests must prove the PBC can explain why a session qualified for an offer without owning external points balances or campaign ledgers.

### 10. Cage Transaction Journal and Patron Verification

**Justification:** Cage operations need a complete journal for chip redemption, front money, marker activity, check cashing, and large cash payouts tied back to the patron and source event.

**Improvement:** Expand `payout` into a cage-facing journal with transaction class, patron verification level, chip-versus-cash breakdown, initiating source, cashier, supervisor, and document packet status.

**Acceptance evidence:** Tests must show every cage transaction has a journal trail from request through completion or void and must reject incomplete patron-verification states when policy requires stronger checks.

### 11. Jackpot and Hand-Pay Lifecycle

**Justification:** Jackpot handling crosses slot operations, cage procedures, tax forms, surveillance review, and patron experience in a single time-sensitive workflow.

**Improvement:** Add jackpot-specific `payout` states for pending-verification, hand-pay-in-progress, tax-review, withheld, paid, disputed, voided, and closed, with meter snapshot, witness evidence, and payout split details.

**Acceptance evidence:** Tests must prove a jackpot cannot close without its meter snapshot, reviewer evidence, and patron disposition and must show where the hand-pay stalled if it breaches SLA.

### 12. Drop Schedule and Sealed Container Chain of Custody

**Justification:** Table drops and slot canister removals are only credible when each transfer is sealed, witnessed, timed, and reconciled to the floor source.

**Improvement:** Add drop-cycle records to `gaming_compliance` for asset, scheduled window, seal number, collector pair, route completion, count-room receipt, and broken-seal exception handling.

**Acceptance evidence:** Tests must reconstruct the custody chain from floor pickup to count-room receipt and open an exception immediately when a seal mismatch occurs.

### 13. Count Room Reconciliation and Variance Classification

**Justification:** Count operations need more than a final total; they need to distinguish expected variance, suspect variance, and unresolved variance tied to its source asset.

**Improvement:** Add count packets under `gaming_compliance` with expected amount, counted amount, variance class, recount evidence, witness set, and downstream disposition for cage, slots, or tables.

**Acceptance evidence:** Tests must classify variance severity, require a recount when thresholds are crossed, and show whether the issue originated from a table drop, slot canister, or cage transfer.

### 14. Variance Investigation Queue Across Floor, Cage, and Count

**Justification:** When a variance appears, the PBC should present one investigation record rather than leaving teams to stitch together table, slot, cage, and count facts manually.

**Improvement:** Create variance investigations in `gaming_compliance` with owner, linked source events, surveillance-review-needed flag, patron-impact flag, remediation task list, and closure evidence.

**Acceptance evidence:** Tests must open one linked investigation per variance root issue, track cross-team task completion, and prevent closure without documented disposition.

### 15. Responsible-Gaming Trigger Registry

**Justification:** Operators need explainable, governed triggers for intervention instead of ad hoc judgment after harm signals have already escalated.

**Improvement:** Add trigger definitions for `responsible_gaming_case` covering time-on-device, loss velocity, frequent ATM/cashier trips, manual observation, repeated self-limit changes, and host concern escalation.

**Acceptance evidence:** Tests must show which trigger opened a case, what evidence it used, and whether the trigger came from table play, slot play, cage behavior, or manual staff observation.

### 16. Self-Exclusion, Cool-Off, and Reinstatement Flow

**Justification:** Self-exclusion programs fail if entry, enforcement, and reinstatement steps are not consistent at every player touchpoint.

**Improvement:** Extend `responsible_gaming_case` with self-exclusion intake, effective period, property scope, reinstatement prerequisites, acknowledgment documents, and re-entry decision evidence.

**Acceptance evidence:** Tests must block new play sessions during active exclusion, route reinstatement requests through review, and preserve the original exclusion evidence after reinstatement.

### 17. Responsible-Gaming Intervention Logging

**Justification:** Staff warnings, host outreach, welfare checks, and escorted removals need a single case narrative that survives shift changes and later review.

**Improvement:** Add intervention events to `responsible_gaming_case` for conversation, resource handoff, play suspension, check-in reminder, escorted departure, and external referral.

**Acceptance evidence:** Tests must preserve intervention chronology, show who performed each action, and require follow-up scheduling when policy says an intervention cannot be one-and-done.

### 18. Suspicious Activity and Large-Transaction Case Assembly

**Justification:** Compliance analysts need candidate cases assembled from play, cage, and identity evidence before they can decide whether a regulatory filing is warranted.

**Improvement:** Add `gaming_compliance` case types for large cash activity, structuring indicators, source-of-funds concern, unusual redemption pattern, and repeated manual override activity.

**Acceptance evidence:** Tests must gather linked patron, session, and payout evidence into one candidate case, preserve analyst notes, and keep the actual filing workflow outside undeclared external systems.

### 19. Jurisdiction-Specific Rule Registry for Games and Payouts

**Justification:** Table spread limits, jackpot holds, ID checks, and exclusion procedures vary by jurisdiction and property agreement.

**Improvement:** Use `gaming_casino_operations_policy_rule` to version jurisdiction, property, game, and payout rules with effective dates, approval source, and operational impact summaries.

**Acceptance evidence:** Rule-evaluation tests must show the same transaction can pass in one jurisdiction and fail in another and must preserve which rule version drove the outcome.

### 20. Progressive Jackpot Contribution and Liability Evidence

**Justification:** Progressive jackpots create a liability trail that starts with device contribution and ends with patron payout, reset, and floor communication.

**Improvement:** Add progressive-jackpot evidence to `payout` and `slot_machine` for contribution source, liability amount, winning meter snapshot, reset approval, and linked communication to the floor team.

**Acceptance evidence:** Tests must reconcile progressive contributions to the winning event and must fail if a jackpot reset occurs without a completed payout trail.

### 21. Table Call and Payout Dispute Resolution

**Justification:** Disputed table outcomes are common flashpoints where supervisors, dealers, surveillance, and patrons need a durable fact pattern.

**Improvement:** Add dispute records under `payout` and `table_game` for called outcome, alternate claim, witness set, surveillance-review-request flag, ruling authority, and patron communication result.

**Acceptance evidence:** Tests must preserve both the original call and final ruling, require reviewer evidence for any reversal, and show whether the patron accepted the resolution.

### 22. Surveillance Review Request Boundary

**Justification:** Casino operations need to request surveillance review often, but this PBC should own request metadata and disposition, not the video archive itself.

**Improvement:** Add `gaming_compliance` review-request records with request reason, incident time window, asset, patron, urgency, requestor, disposition, and restricted redaction notes.

**Acceptance evidence:** Boundary tests must prove the PBC stores request and outcome metadata only and never assumes ownership of surveillance media storage or retrieval tables.

### 23. Cheat, Collusion, and Device Malfunction Incident Command

**Justification:** Pit scams, suspected collusion, and device malfunctions need one command record that coordinates operations, surveillance, compliance, and cage impact.

**Improvement:** Add incident command cases in `gaming_compliance` with incident type, live-floor containment steps, linked sessions, linked payouts, linked surveillance request, and post-incident review.

**Acceptance evidence:** Tests must route incidents by severity, hold related payouts when required, and keep every containment action visible to the assigned command owner.

### 24. Supplier Qualification Gating for Floor Asset Changes

**Justification:** Slot conversions and table-equipment changes should not proceed if the manufacturer, parts source, or service provider is not approved.

**Improvement:** Consume `SupplierQualified` into `slot_machine` and `table_game` readiness checks so conversions, installs, and repairs are blocked or flagged when supplier qualification changes.

**Acceptance evidence:** Tests must show a later supplier disqualification reopens affected floor-change tasks and that the stored reasoning cites the source event lineage.

### 25. Customer Update Reconciliation for Patron Profiles

**Justification:** Patron contact and identity details can change outside the gaming floor, but floor risk decisions still depend on keeping the local patron profile synchronized.

**Improvement:** Consume `CustomerUpdated` into `player_profile` reconciliation workflows with field-level diff review, merge-decision capture, and downstream refresh of open sessions and cases.

**Acceptance evidence:** Tests must show a customer update can create a review task instead of silently overwriting local risk-critical data and that approved changes refresh dependent workbench views.

### 26. Policy Change Propagation to Live Floor Work

**Justification:** New payout thresholds or responsible-gaming rules are dangerous if open sessions and pending jackpots keep operating under retired policy.

**Improvement:** Consume `PolicyChanged` to recalculate affected `wager_session`, `payout`, `responsible_gaming_case`, and `gaming_compliance` records and to flag which live work needs re-review.

**Acceptance evidence:** Tests must show policy propagation identifies impacted records, preserves the prior rule version for history, and queues re-review rather than mutating closed history.

### 27. Event-Sourced Gaming Floor Timeline

**Justification:** Casino disputes and audits often hinge on the exact order of floor events across players, devices, cash movement, and reviews.

**Improvement:** Use `gaming_casino_operations_event_sourced_operational_history` to record play, payout, exception, policy, and review events with deterministic ordering and replay checkpoints.

**Acceptance evidence:** Replay tests must rebuild table, slot, and patron timelines at a requested time and must expose any gaps or late-arriving events instead of hiding them.

### 28. Idempotent Device and Floor Event Ingestion

**Justification:** Meter readings, session starts, jackpot notices, and cashier actions can be retransmitted or arrive out of order, especially during outages.

**Improvement:** Strengthen `idempotent_handlers` around `slot_machine`, `wager_session`, and `payout` ingestion with asset-scoped idempotency keys, sequence expectations, and late-event quarantine.

**Acceptance evidence:** Tests must prove duplicate device or cashier events cannot double-create payouts or sessions and that late arrivals are visible for manual review.

### 29. Dead-Letter Workbench for Floor Event Failures

**Justification:** When floor events fail processing, supervisors need a recoverable operational queue rather than opaque transport errors.

**Improvement:** Add a dead-letter queue view in `GamingCasinoOperationsWorkbench` for failed play, payout, compliance, and policy events with replay eligibility, impact summary, and remediation ownership.

**Acceptance evidence:** Tests must show dead-letter entries explain business impact, allow safe replay when preconditions are met, and preserve the original payload and failure reason.

### 30. Floor Supervisor Workbench

**Justification:** Floor supervisors need one place to see spread changes, table exceptions, pending disputes, hand-pays waiting for witness, and patron restrictions before they escalate.

**Improvement:** Add a floor-supervisor persona to `GamingCasinoOperationsWorkbench` with pit heat, open incidents, pending approvals, rating-review alerts, and unresolved inventory movements.

**Acceptance evidence:** UI contract tests must show supervisor actions are permission-aware and that each queue item drills into owned records rather than hidden external state.

### 31. Slot Operations Workbench

**Justification:** Slot leads need rapid visibility into outages, jackpots, meter drift, printer failures, conversions, and unreconciled machine movements.

**Improvement:** Add a slot-ops view to `GamingCasinoOperationsWorkbench` with bank map status, machine fault filters, jackpot timers, conversion tasks, and meter-anomaly cards sourced from `slot_machine`.

**Acceptance evidence:** Tests must prove the view groups machines by bank and status, highlights stale meter snapshots, and links every anomaly to an owned machine record or event.

### 32. Cage Workbench

**Justification:** Cage cashiers and supervisors need to manage payouts, voids, escalations, and document packets without losing the floor event that triggered them.

**Improvement:** Add a cage persona to `GamingCasinoOperationsWorkbench` with pending payouts, large-transaction review, cashier handoff, void requests, and missing-document alerts from `payout`.

**Acceptance evidence:** UI tests must show dual-control actions require the correct permissions and that each payout card exposes its linked patron, source session, and review state.

### 33. Compliance Analyst Workbench

**Justification:** Compliance analysts need cross-cutting queues for suspicious activity, count variances, review requests, and policy breaches with lineage back to floor facts.

**Improvement:** Add a compliance persona to `GamingCasinoOperationsWorkbench` with case aging, severity filters, filing-candidate queues, custody-break alerts, and unresolved review requests from `gaming_compliance`.

**Acceptance evidence:** Tests must show the compliance queue can pivot from case to source session, payout, or asset and must surface lineage to `PolicyChanged`, `CustomerUpdated`, or `SupplierQualified` when relevant.

### 34. Responsible-Gaming Workbench

**Justification:** Responsible-gaming staff need to triage open cases, active exclusions, pending interventions, and reinstatement requests without searching across unrelated screens.

**Improvement:** Add a responsible-gaming persona to `GamingCasinoOperationsWorkbench` with trigger severity, next action due, active restrictions, intervention history, and reinstatement review panels from `responsible_gaming_case`.

**Acceptance evidence:** UI tests must prove the queue highlights immediate-intervention cases first and keeps historical interventions visible even after a case is closed.

### 35. Shift Briefing Agent Skill

**Justification:** Shift handoffs lose critical context when supervisors rely on memory or free-form notes instead of a governed summary.

**Improvement:** Add an assistant skill in `GamingCasinoOperationsAssistantPanel` that drafts shift briefings from open incidents, jackpots in progress, count issues, active exclusions, and priority machine outages.

**Acceptance evidence:** Tests must prove each briefing sentence cites owned records or emitted events, and the skill must label any inference instead of presenting it as a fact.

### 36. Rating Correction and Host Review Agent Skill

**Justification:** Hosts and supervisors need help spotting questionable ratings, but agent suggestions must never silently change patron worth or comp posture.

**Improvement:** Add an assistant skill that proposes `wager_session` rating corrections, identifies missing rating inputs, and prepares host review packets with visible diffs and supporting evidence.

**Acceptance evidence:** Tests must require explicit confirmation before a rating mutation, preserve the original rating, and record the agent suggestion alongside the approving human actor.

### 37. Regulator Notice and Internal Control Memo Intake

**Justification:** Casinos receive rule bulletins, internal-control revisions, and regulator directives that need structured translation into operational policy.

**Improvement:** Use `gaming_casino_operations_semantic_document_instruction_understanding` to parse notices into candidate `gaming_casino_operations_policy_rule` or `gaming_casino_operations_runtime_parameter` changes with cited source spans.

**Acceptance evidence:** Tests must keep extracted obligations in draft until approved, show the source span for each proposed rule, and reject ambiguous instructions that lack enough evidence.

### 38. Governed Agent Mutation Guardrails

**Justification:** The floor assistant should help operators move faster without becoming an unchecked backdoor into payouts, exclusions, or compliance cases.

**Improvement:** Use `gaming_casino_operations_governed_ai_agent_execution` so create, update, approve, and exception-close actions run only through previewed commands, permission checks, and policy gates.

**Acceptance evidence:** Tests must block restricted agent actions, require preview-and-confirm on allowed mutations, and write an audit trail for both accepted and rejected commands.

### 39. API Surface Expansion for Search, Review, and Correction

**Justification:** Casino operations need query and correction endpoints, not only create endpoints, to handle disputes, shift review, and midstream operational repair.

**Improvement:** Extend the API set around `POST /player-profiles`, `POST /table-games`, `POST /slot-machines`, `POST /wager-sessions`, and `POST /payouts` with search, replay-safe correction, validation-only, and evidence-export routes.

**Acceptance evidence:** Contract tests must prove new routes are versioned, idempotent where required, and scoped to owned records and declared dependencies only.

### 40. Explicit Event and External-System Boundaries

**Justification:** The PBC must be clear about what it owns versus what it references so surveillance, finance, tax reporting, and enterprise loyalty are not silently pulled inside.

**Improvement:** Document and enforce boundary rules in handlers, services, and `GamingCasinoOperationsDetail` so the PBC owns gaming-floor records, emits handoff events, and stores only metadata for external domains.

**Acceptance evidence:** Boundary tests must fail if generated artifacts reference undeclared foreign tables and must show emitted events carry enough context for downstream consumers.

### 41. Runtime Parameter Governance for Floor Thresholds

**Justification:** Properties need to tune thresholds for large payouts, review holds, count variance escalation, and intervention timing without code edits.

**Improvement:** Expand `gaming_casino_operations_runtime_parameter` with bounded knobs for jackpot hold amounts, dual-control thresholds, review SLAs, alert suppression rules, and peak-night staffing assumptions.

**Acceptance evidence:** Tests must validate parameter bounds, tenant-specific overrides, approval history, and visible rollback from `GamingCasinoOperationsWorkbench`.

### 42. Schema Extension Registry for New Game Types and Jurisdiction Fields

**Justification:** Casinos add side bets, new devices, and local compliance fields over time, and the PBC must evolve without breaking existing sessions or workbench views.

**Improvement:** Use `gaming_casino_operations_schema_extension` to register new game attributes, jurisdiction fields, and UI placements with compatibility checks and projection backfill plans.

**Acceptance evidence:** Tests must add and deprecate an extension safely, preserve existing records, and show backfilled projections before the extension is activated on live data.

### 43. Continuous Control Testing for Segregation of Duties

**Justification:** The riskiest casino failures happen when the same person can initiate, approve, and settle a sensitive action without a second control point.

**Improvement:** Add `gaming_casino_operations_control_assertion` checks for payout dual control, count witness requirements, cage override approval, rating-change approval, and self-exclusion enforcement.

**Acceptance evidence:** Control tests must open exceptions when duty segregation is violated and must keep the failing evidence linked to the affected payout, case, or session.

### 44. Cryptographic Proof Chains for Count and Jackpot Evidence

**Justification:** High-stakes evidence packets should be tamper-evident even when the underlying documents are redacted for privacy or investigation sensitivity.

**Improvement:** Use `gaming_casino_operations_cryptographic_audit_proofs` to hash-chain count packets, jackpot documents, review decisions, and release evidence snapshots.

**Acceptance evidence:** Tests must verify proof chains, fail on altered event order or payload digests, and support redacted proof exports for auditors.

### 45. Release Evidence Pack for Floor Readiness

**Justification:** Releasing a casino-ops PBC without explicit evidence around floor workflows, controls, and assistant guardrails creates audit and operational exposure.

**Improvement:** Expand `RELEASE_EVIDENCE.md` coverage to include jackpot flow tests, count custody tests, exclusion enforcement, workbench persona evidence, agent-skill guardrails, and boundary checks.

**Acceptance evidence:** Release verification must fail if any required casino-floor evidence set is missing and must summarize pass-fail state by floor, cage, compliance, and responsible-gaming lanes.

### 46. Peak-Night and Disruption Scenario Simulation

**Justification:** Weekend peaks, headline events, system outages, and sudden jackpot clusters stress staffing and controls differently than ordinary operations.

**Improvement:** Use `gaming_casino_operations_counterfactual_scenario_simulation` to model table spread changes, cage queue spikes, machine-bank outages, surge jackpots, and responsible-gaming case bursts.

**Acceptance evidence:** Simulation tests must compare before-after queue load, approval demand, and SLA risk without mutating live records.

### 47. Multi-Property and Tenant Isolation

**Justification:** A casino group can share platform code while keeping separate policies, patron restrictions, and operating practices by property and jurisdiction.

**Improvement:** Strengthen `gaming_casino_operations_multi_tenant_policy_isolation` so workbench queues, parameters, rules, and assistant responses stay scoped to the property or tenant in context.

**Acceptance evidence:** Tests must prove two tenants can hold different payout thresholds and exclusion rules for identical events without any queue or data leakage.

### 48. Certification and Authority Gates for Sensitive Actions

**Justification:** Not every approved user should be able to approve a jackpot, clear a variance, or reinstate an excluded patron just because they have broad package access.

**Improvement:** Add authority and certification requirements to `gaming_casino_operations_governed_model` for sensitive approvals, tying allowed actions to role, training status, jurisdiction, and recency of certification.

**Acceptance evidence:** Tests must deny sensitive actions when training or authority is expired and must show the exact missing qualification in the rejection reason.

### 49. Offline Floor Operation and Replay Recovery

**Justification:** Casino floors keep moving during partial outages, so the PBC needs safe capture and replay rather than assuming uninterrupted connectivity.

**Improvement:** Add offline capture states for table events, machine exceptions, and cage requests with local sequence numbers, replay status, and conflict-review rules when connectivity returns.

**Acceptance evidence:** Tests must replay offline actions deterministically, prevent duplicate settlement, and route conflicting replays into a manual review queue.

### 50. End-to-End Operating Stories for Release Rehearsal

**Justification:** The final proof of quality is whether the package can run realistic casino stories from patron enrollment through play, payout, controls, intervention, and audit review.

**Improvement:** Add release rehearsal stories that seed `player_profile`, `table_game`, `slot_machine`, `wager_session`, `payout`, `responsible_gaming_case`, and `gaming_compliance` through realistic scenarios such as jackpot hand-pay, count variance, disputed table ruling, and self-exclusion interception.

**Acceptance evidence:** Release rehearsal tests must prove the stories drive APIs, events, workbench queues, assistant summaries, control assertions, and release documents end to end.
