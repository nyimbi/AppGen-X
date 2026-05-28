# IT Service Management Improvement Backlog

## Current Domain Evidence Used

- Stable package key: `it_service_management`.
- Manifest label and purpose: IT Service Management for incidents, service requests, change requests, problem records, configuration items, service levels, knowledge, rules, parameters, and operations controls.
- Owned tables named in the manifest: `it_incident`, `service_request`, `change_request`, `problem_record`, `configuration_item`, `sla_clock`, `knowledge_article`, `it_service_management_policy_rule`, `it_service_management_runtime_parameter`, `it_service_management_schema_extension`, `it_service_management_control_assertion`, `it_service_management_governed_model`.
- Public routes already declared: `POST /it-incidents`, `POST /service-requests`, `POST /change-requests`, `POST /problem-records`, `POST /configuration-items`, `GET /it-service-management-workbench`.
- Emitted events already declared: `ItServiceManagementCreated`, `ItServiceManagementUpdated`, `ItServiceManagementApproved`, `ItServiceManagementExceptionOpened`.
- Consumed events already declared: `PolicyChanged`, `AuditEventSealed`, `OperationalKpiChanged`.
- Workbench and assistant surfaces already declared: `ItServiceManagementWorkbench`, `ItServiceManagementDetail`, `ItServiceManagementAssistantPanel`.
- Domain operations in the package specification include `create_it_incident`, `record_service_request`, `review_change_request`, `approve_problem_record`, `simulate_configuration_item`, and `create_sla_clock`.

### 1. Major incident declaration model

**Justification:** The package owns `it_incident`, but the current evidence does not show a formal major-incident path with explicit command authority, impact thresholds, or communications discipline.

**Improvement:** Add a major-incident state overlay for `it_incident` with severity matrix rules, commander assignment, declaration timestamp, affected business service list, bridge details, and exit criteria that differ from routine incident handling.

**Acceptance evidence:** Tests prove declaration, downgrade, and closure rules; the workbench shows commander, severity, and blast radius; emitted events distinguish routine incidents from major incidents.

### 2. Impact and urgency matrix for incident prioritization

**Justification:** Priority needs to be calculated from business impact and urgency rather than left to free-text operator judgment, or queues become noisy and SLA clocks become unreliable.

**Improvement:** Introduce an impact-by-urgency matrix for `it_incident` that derives priority, target response, escalation path, and customer communication cadence from business service criticality, user count, revenue exposure, and regulatory exposure.

**Acceptance evidence:** Rule fixtures cover P1 through low-priority cases; `sla_clock` targets are derived from the matrix; queue views expose why a ticket reached its assigned priority.

### 3. Duplicate incident correlation and outage rollup

**Justification:** During outages, dozens of near-identical tickets can flood intake and obscure the parent issue that operators actually need to restore.

**Improvement:** Add duplicate and related-incident correlation for `it_incident`, including parent outage records, child symptom tickets, merge history, and rules for preserving separate VIP or regulated-customer cases when they require distinct handling.

**Acceptance evidence:** Correlation tests show child tickets rolling into a parent outage; the workbench displays parent-child relationships; merged tickets retain audit history and requester notifications.

### 4. Incident timeline and evidence freeze

**Justification:** Operators and auditors need a reliable chronology of detection, triage, escalation, mitigation, recovery, and closure, especially when problem management follows later.

**Improvement:** Record structured timeline entries on `it_incident` for every material action, with source, actor, timestamp, before/after state, linked artifacts, and an evidence-freeze marker when the record moves into review or dispute.

**Acceptance evidence:** Replay tests reconstruct the full incident timeline; detail views render a chronological ledger; late edits after evidence freeze require explicit exception approval.

### 5. Service restoration milestones inside SLA handling

**Justification:** Incident SLAs usually depend on restoring service first and closing paperwork later; one clock cannot accurately represent both outcomes.

**Improvement:** Expand `sla_clock` to track acknowledgement, restoration, workaround, and final-resolution milestones for incident records, with distinct pause and breach rules for each milestone.

**Acceptance evidence:** SLA tests cover acknowledgement-only, workaround, and full-resolution paths; dashboards show which milestone is at risk; breach events reference the breached milestone, not just the ticket.

### 6. Swarming and resolver-group handoff rules

**Justification:** Practical incident response depends on coordinated resolver groups and fast handoffs; uncontrolled reassignment causes ownership gaps and missed updates.

**Improvement:** Add swarming support to `it_incident` with primary owner, active resolver groups, paging status, handoff reason, and transfer safeguards that block silent reassignment when no accepting team is recorded.

**Acceptance evidence:** Workflow tests prove safe handoff behavior; workbench queues show active swarm participants; audit history records every ownership transfer and acknowledgment.

### 7. Service request catalog structure

**Justification:** `service_request` needs to distinguish catalog-backed fulfillment from ad hoc ticketing, or approvals, entitlements, and fulfillment steps remain inconsistent.

**Improvement:** Model service catalog entries for `service_request` with request type, required form fields, fulfillment template, approval policy, expected lead time, and entitlement checks tied to the requested service.

**Acceptance evidence:** Catalog fixtures create repeatable request types; request forms render required fields by catalog item; fulfillment metrics compare actual completion time against the catalog promise.

### 8. Access request entitlement validation

**Justification:** Access-related service requests carry segregation-of-duties and least-privilege risk that ordinary fulfillment logic does not cover.

**Improvement:** Add entitlement-aware validation for access-oriented `service_request` records, including requester identity, manager chain, target system, access level, segregation-of-duties conflicts, and time-bounded access expiry.

**Acceptance evidence:** Rule tests reject conflicting access combinations; approvals capture manager and system-owner decisions; fulfilled requests include expiry or recertification evidence where required.

### 9. Multi-step fulfillment task orchestration

**Justification:** Many requests require several internal tasks across service desk, infrastructure, security, and application teams before the customer sees completion.

**Improvement:** Break `service_request` fulfillment into ordered or parallel tasks with prerequisites, due dates, owning group, completion evidence, and customer-visible progress markers.

**Acceptance evidence:** End-to-end tests show task fan-out and completion gates; request detail views expose open tasks and blockers; SLA pause rules reflect waiting-on-customer versus waiting-on-fulfiller states.

### 10. Request closure with requester confirmation

**Justification:** Closing a request without validating delivery quality produces reopen churn and undermines service catalog trust.

**Improvement:** Add post-fulfillment verification to `service_request` so closures can require requester confirmation, proof-of-delivery artifacts, or timed auto-close after a configurable observation period.

**Acceptance evidence:** Tests cover confirmed closure, timeout closure, and reopen cases; queue views highlight pending customer confirmation; closure analytics track reopen rates by catalog item.

### 11. Standard, normal, and emergency change paths

**Justification:** `change_request` should not force every change through the same governance path because low-risk standard changes and urgent emergency changes have different control expectations.

**Improvement:** Split `change_request` into standard, normal, and emergency modes with separate risk checks, evidence requirements, approval counts, implementation windows, and post-change review expectations.

**Acceptance evidence:** Rule fixtures prove route selection by change type; workbench views expose change class and required approvals; emergency changes require expedited review evidence after implementation.

### 12. Change risk scoring and blast-radius estimation

**Justification:** Change approval quality depends on likely impact to business services, technical dependencies, customer-facing uptime, and rollback complexity.

**Improvement:** Add a risk model for `change_request` that considers affected `configuration_item` records, service tier, dependency count, maintenance-window timing, previous failure history, and presence of a tested backout plan.

**Acceptance evidence:** Test cases show low-, medium-, and high-risk scoring outcomes; approvers can inspect the scoring factors; analytics correlate predicted risk with post-implementation incidents.

### 13. Maintenance windows and blackout calendar enforcement

**Justification:** Change scheduling needs to respect freeze periods, regional business calendars, payroll or quarter-end deadlines, and service-specific blackout periods.

**Improvement:** Enforce maintenance windows for `change_request` with calendar-aware validation against business freezes, service blackouts, and local holidays, while allowing governed exceptions with written justification.

**Acceptance evidence:** Scheduling tests reject blocked windows; simulation previews show the violated calendar rule; approved exceptions are visible with approver, justification, and expiration date.

### 14. CAB agenda, quorum, and decision capture

**Justification:** Advisory review becomes untrustworthy when meeting decisions are lost in notes or reflected only as a status change.

**Improvement:** Add CAB support for `change_request` with agenda order, attendee roles, quorum rules, discussion summary, requested follow-ups, decision outcome, and linked evidence from risk review.

**Acceptance evidence:** CAB workflow tests require quorum before approval; detail views show the exact CAB decision package; rejected changes retain reasons and required resubmission actions.

### 15. Backout plan and validation checklist enforcement

**Justification:** A change without a realistic backout plan and clear validation steps is a preventable production risk.

**Improvement:** Require `change_request` records to capture implementation checklist items, validation steps, success criteria, backout triggers, estimated rollback time, and responsible rollback owner before approval.

**Acceptance evidence:** Approval tests fail when backout content is incomplete; workbench detail pages show the implementation and rollback checklists; post-change review confirms whether the plan was used.

### 16. Post-implementation review workflow

**Justification:** Learning from failed or risky changes is core ITSM behavior and should be first-class instead of being left to ad hoc follow-up.

**Improvement:** Add a post-implementation review lifecycle for `change_request` that records actual outcome, unexpected impact, remediation work, follow-on incidents, and policy feedback for future changes.

**Acceptance evidence:** Changes that trigger incidents automatically require review; review forms capture outcome classifications; metrics show failed-change rate and overdue reviews.

### 17. Problem record linkage to incidents and changes

**Justification:** `problem_record` is most valuable when it connects recurring incidents and unsuccessful changes into a single root-cause effort.

**Improvement:** Add many-to-many linkage among `problem_record`, `it_incident`, and `change_request`, with distinction between symptom tickets, suspected causes, confirmed causes, and change-introduced faults.

**Acceptance evidence:** Tests prove linked records stay consistent through closure and reopen events; detail pages show related incidents and changes; analytics identify top recurring symptoms by problem record.

### 18. Root-cause analysis template library

**Justification:** Problem management quality rises when investigators use repeatable methods such as timeline reconstruction, five-whys, fault tree reasoning, and contributing-factor capture.

**Improvement:** Equip `problem_record` with RCA templates, contributing-factor categories, hypothesis tracking, evidence links, and explicit status values for suspected, validated, and disproven causes.

**Acceptance evidence:** RCA fixtures cover multiple methods; workbench detail pages render structured root-cause evidence; closure rules require approved corrective or preventive actions.

### 19. Known error database and workaround publication

**Justification:** Service desk agents need approved workarounds before the permanent fix is ready, or incident queues keep rediscovering the same temporary steps.

**Improvement:** Connect `problem_record` and `knowledge_article` so confirmed known errors can publish controlled workarounds, customer-facing guidance, and internal resolver notes with separate visibility rules.

**Acceptance evidence:** Tests prove knowledge visibility rules for internal versus customer-safe content; incidents can attach the approved workaround; metrics track workaround usage before permanent remediation.

### 20. Recurrence detection across incident history

**Justification:** A problem candidate should surface from patterns in the package’s own incident stream rather than waiting for manual recognition.

**Improvement:** Add recurrence detection across `it_incident` history using service, CI, symptom signature, time window, and workaround reuse to propose new `problem_record` creation or reopening.

**Acceptance evidence:** Detection tests generate candidate problems from repeated incidents; workbench panels show recurrence scores and linked evidence; analysts can accept or dismiss the recommendation with rationale.

### 21. Configuration item relationship graph

**Justification:** Impact analysis is weak without service maps showing how infrastructure, applications, integrations, and business services depend on each other.

**Improvement:** Expand `configuration_item` to model relationships such as runs-on, depends-on, provides, supports, hosted-in, and owned-by, with directional semantics for incident impact and change risk analysis.

**Acceptance evidence:** Graph tests prove relationship traversal; change and incident views show upstream and downstream affected services; import or update flows block invalid circular relationships where policy forbids them.

### 22. CI ownership and support model

**Justification:** A CI record without service owner, support group, business criticality, or maintenance contact cannot drive escalation or approval routing.

**Improvement:** Require `configuration_item` records to capture technical owner, service owner, support group, criticality tier, maintenance calendar, and after-hours contact model.

**Acceptance evidence:** Validation tests reject incomplete operational ownership; workbench detail pages display owner and support context; major-incident escalation can resolve contacts from the CI record.

### 23. CI drift and stale-data detection

**Justification:** CMDB value collapses when records are outdated, duplicated, or no longer reflect production reality.

**Improvement:** Add drift detection for `configuration_item` using event history, change completion data, last verification date, and mismatch rules that flag stale ownership, missing relationships, or unverified decommission states.

**Acceptance evidence:** Drift fixtures open exceptions on stale CIs; dashboards show stale-data percentages by service; approved remediation updates clear the exception with timestamped evidence.

### 24. Service dependency impact preview before change approval

**Justification:** Approvers need to know which business services, customer journeys, and support teams could be affected by a proposed change.

**Improvement:** Use the `configuration_item` graph to generate an impact preview for `change_request`, including directly touched components, dependent services, support groups to notify, and likely monitoring signals to watch.

**Acceptance evidence:** Approval screens include an impact preview panel; simulation tests match expected service dependencies; post-change reviews compare predicted versus observed impact.

### 25. SLA, OLA, and underpinning commitment separation

**Justification:** External customer commitments and internal support obligations should not share the same policy object or the same breach semantics.

**Improvement:** Extend `sla_clock` and related rules to distinguish customer SLAs, internal OLAs, and supplier or underpinning commitments, with separate breach logic, clock ownership, and evidence expectations.

**Acceptance evidence:** Tests show different breach handling for SLA, OLA, and underpinning cases; analytics report each clock type separately; incident and request detail views show the active clock category.

### 26. Calendar-aware pause and resume logic

**Justification:** Timers that ignore waiting-on-customer states, after-hours coverage, or approved maintenance windows misreport performance and drive the wrong escalations.

**Improvement:** Add explicit pause reasons for `sla_clock`, including waiting on requester, vendor action pending, CAB review pending, planned implementation window, and emergency freeze review, with business-calendar awareness.

**Acceptance evidence:** Timer tests cover pause/resume transitions and elapsed-time calculations; workbench views show current pause reason; breaches never occur while an approved pause is active.

### 27. Role-based operational queues in the workbench

**Justification:** The same record set must answer different questions for service desk agents, major-incident commanders, change managers, problem managers, and auditors.

**Improvement:** Rework `ItServiceManagementWorkbench` into role-based queue presets for incident triage, request fulfillment, change governance, problem backlog, SLA risk, and audit exceptions.

**Acceptance evidence:** Route and permission tests show role-appropriate queue visibility; saved views include queue definitions and sort logic; operators can move from queue to detail without losing context.

### 28. Aging, load, and attention routing

**Justification:** ITSM operations need to surface what deserves attention now, not just what was opened most recently.

**Improvement:** Add attention scores across `it_incident`, `service_request`, `change_request`, and `problem_record` using age, SLA risk, customer tier, recent updates, blocked status, and missing-owner conditions.

**Acceptance evidence:** Queue ordering tests prove high-attention records float to the top; workbench cards show the factors behind the score; analysts can filter by blocked or neglected items.

### 29. Knowledge article lifecycle and quality checks

**Justification:** `knowledge_article` should support operational knowledge that is reviewed, current, and easy to trust during active incidents and routine requests.

**Improvement:** Add draft, review, published, retired, and superseded states for `knowledge_article`, along with review cadence, owner, approved audience, linked service, and article quality score.

**Acceptance evidence:** Publication tests enforce required review before release; article detail pages show review due date and service linkage; stale articles appear in a dedicated workbench queue.

### 30. Contextual knowledge suggestion during ticket work

**Justification:** Agents and analysts should see likely fixes or procedures while working the ticket, not only after a separate knowledge search.

**Improvement:** Use symptom, service, CI, request type, and problem linkage to suggest relevant `knowledge_article` records in incident, request, and change detail views, while requiring confidence thresholds and visible source rationale.

**Acceptance evidence:** Suggestion tests rank the expected articles first; UI evidence shows why an article was suggested; analysts can mark suggestions as helpful or irrelevant to improve future ranking.

### 31. Structured intake from documents and operator notes

**Justification:** The package already declares document-instruction understanding, but the domain benefit comes from extracting actionable ITSM signals, not just generic text spans.

**Improvement:** Parse emails, outage summaries, handoff notes, and implementation plans into draft `it_incident`, `service_request`, or `change_request` records with extracted service, CI, urgency, proposed window, affected users, and missing-information prompts.

**Acceptance evidence:** Extraction fixtures cover incident mail, access request text, and change plans; the assistant shows a draft preview with confidence and gaps; writes still require explicit human confirmation.

### 32. Policy-rule sandbox and dry-run evaluation

**Justification:** Operations teams need to tune rule behavior without discovering unintended consequences in live tickets.

**Improvement:** Add a sandbox for `it_service_management_policy_rule` that runs candidate rules against representative incidents, requests, changes, problems, and SLA cases before publication.

**Acceptance evidence:** Dry-run reports show which records would change outcome; rule publication requires reviewed simulation output; rollback restores the prior rule version with provenance intact.

### 33. Runtime parameter guardrails and safe ranges

**Justification:** Parameters such as risk thresholds, workbench limits, and approval SLAs can destabilize operations if set outside practical bounds.

**Improvement:** Add bounded range validation and change-impact notes for `it_service_management_runtime_parameter`, including tenant overrides, effective dates, and rollback checkpoints for operational tuning.

**Acceptance evidence:** Parameter tests reject unsafe values; detail pages show active value, source, and effective period; audit evidence links each change to approver and rationale.

### 34. Event-sourced ticket history and replay

**Justification:** The manifest already claims event-sourced operational history, but operators need replayable evidence that explains how a record reached its current state.

**Improvement:** Persist immutable lifecycle events for `it_incident`, `service_request`, `change_request`, `problem_record`, and `configuration_item` so the package can rebuild read models and compare replayed versus stored state.

**Acceptance evidence:** Replay tests rebuild target records deterministically; checksum evidence shows projection parity; detail views can render an event-by-event operational history.

### 35. Dead-letter triage tailored to ITSM workflows

**Justification:** Failed event handling in this package can leave approvals, queue metrics, or exception states out of sync with real operations.

**Improvement:** Add dead-letter tooling for package event failures with reason taxonomy, retry eligibility, owner assignment, linked record lookup, and workbench actions for safe replay or controlled discard.

**Acceptance evidence:** Duplicate, poison-message, and exhausted-retry tests open the expected dead-letter records; operators can inspect the failed payload context; replay actions produce new lineage entries.

### 36. Consumed-event lineage and dependency freshness

**Justification:** `PolicyChanged`, `AuditEventSealed`, and `OperationalKpiChanged` should influence local behavior in a traceable way, or downstream decisions become hard to defend.

**Improvement:** Track which consumed events affected local rules, clocks, queue metrics, and exception states, including freshness windows and alerts when dependent data becomes stale.

**Acceptance evidence:** Handler tests prove lineage is recorded on local state changes; dashboards highlight stale dependency inputs; auditors can trace a decision back to the consumed event version.

### 37. Predictive breach and backlog risk scoring

**Justification:** ITSM teams need early warning on likely SLA misses, overloaded resolver groups, and risky pending changes before the failure becomes visible to customers.

**Improvement:** Expand `it_service_management_risk_score` to forecast incident breach risk, request aging risk, failed-change likelihood, and problem backlog escalation using queue depth, historical performance, and dependency signals.

**Acceptance evidence:** Risk fixtures produce expected high-risk alerts; workbench cards explain the scoring factors; calibration reports compare predicted versus observed breaches and failures.

### 38. Counterfactual simulation for change timing and staffing

**Justification:** Change managers often need to decide whether to move a window, add resolvers, or split scope before approval.

**Improvement:** Use `simulate_configuration_item` and package-local scenario tooling to compare alternate implementation windows, staffing plans, rollout scope, and backout thresholds for `change_request`.

**Acceptance evidence:** Simulation outputs compare risk, service impact, and calendar conflicts across scenarios; the workbench presents side-by-side options; accepted plans retain a reference to the evaluated scenarios.

### 39. Continuous control testing for approvals and segregation of duties

**Justification:** Approval misuse, self-approval, and missing evidence are control failures that should surface immediately rather than during release review.

**Improvement:** Add continuous assertions in `it_service_management_control_assertion` for self-approval, missing manager review, emergency change without post-review, access request without entitlement check, and unresolved major-incident action items.

**Acceptance evidence:** Control tests raise exceptions on each failure mode; dashboards show open control findings by severity; closure requires linked remediation evidence and reviewer signoff.

### 40. Cryptographic sealing for high-value operational evidence

**Justification:** Major incidents, emergency changes, and disputed SLA outcomes may require stronger proof that operational evidence was not altered after the fact.

**Improvement:** Hash and seal critical evidence packages for `it_incident`, `change_request`, `problem_record`, and `sla_clock`, including attached timelines, approvals, and exported audit packets.

**Acceptance evidence:** Verification APIs confirm the hash chain; tamper tests detect altered evidence; exported audit packets include proof metadata without exposing restricted payloads.

### 41. Tenant isolation across queues, policies, and evidence

**Justification:** The manifest claims multi-tenant policy isolation, but the operational risk is in queue leakage, cross-tenant suggestions, and incorrect evidence visibility.

**Improvement:** Enforce tenant scoping across `ItServiceManagementWorkbench`, event handlers, knowledge suggestions, rule evaluation, and export flows so no record, metric, or recommendation crosses tenant boundaries.

**Acceptance evidence:** Negative tests prove one tenant cannot see another tenant’s tickets or analytics; handler tests enforce tenant ownership on incoming events; exports are watermarked with tenant scope.

### 42. Tenant-specific calendars, support hours, and service tiers

**Justification:** SLA policies and maintenance windows vary materially by tenant, service tier, and geography.

**Improvement:** Let each tenant define support hours, service tiers, holiday calendars, priority targets, and blackout periods that feed `sla_clock`, incident priority, and change scheduling rules.

**Acceptance evidence:** Tenant policy fixtures produce different due dates from the same ticket inputs; workbench views show the active service tier; calendar changes create versioned policy history.

### 43. Carbon-aware scheduling for non-urgent changes

**Justification:** The package already cites sustainability awareness, and non-urgent maintenance can sometimes move to lower-impact windows without harming service quality.

**Improvement:** Add optional sustainability guidance to `change_request` that compares proposed windows by estimated energy profile, region, and workload type, while keeping risk and service commitments as the primary decision factors.

**Acceptance evidence:** Simulation evidence shows when a lower-impact window is available; approvers can compare operational risk and sustainability notes together; the feature is clearly advisory, not mandatory.

### 44. Service continuity and disaster-recovery readiness checks

**Justification:** Changes and incidents affecting critical services should expose whether failover plans, runbooks, and restore evidence are current before a crisis deepens.

**Improvement:** Link `configuration_item`, `knowledge_article`, and `change_request` to continuity metadata such as recovery tier, failover pattern, test date, and restoration runbook currency.

**Acceptance evidence:** Critical-service records show continuity readiness in detail pages; change approvals warn when DR evidence is stale; major-incident screens surface the latest validated recovery steps.

### 45. Release-assurance coverage for routes, events, and UI fragments

**Justification:** The package should prove that its declared routes, events, and workbench fragments remain aligned as the backlog is implemented.

**Improvement:** Expand package release assurance so each declared route, emitted event, consumed event handler, permission, and UI fragment has traceable verification coverage tied to the ITSM domain scenarios it serves.

**Acceptance evidence:** Release evidence references `POST /it-incidents`, `POST /service-requests`, `POST /change-requests`, `POST /problem-records`, `POST /configuration-items`, and `GET /it-service-management-workbench`; missing coverage fails package verification.

### 46. Metrics dictionary for operational analytics

**Justification:** Analytics become hard to trust when teams interpret “breach,” “restoration,” or “failed change” differently.

**Improvement:** Publish a package-local metrics dictionary covering incident response, restoration, request fulfillment, change success, problem recurrence, SLA compliance, queue attention, and control findings.

**Acceptance evidence:** Every workbench metric links to a definition; tests prove metric calculations for representative scenarios; exported analytics include metric version and calculation notes.

### 47. Audit packet and regulator-ready export flow

**Justification:** High-friction evidence gathering wastes time during audits, customer reviews, and post-outage investigations.

**Improvement:** Add export flows that assemble ticket history, approvals, SLA milestones, knowledge references, change evidence, and control findings into a governed audit packet for a selected incident, request, change, problem, or service.

**Acceptance evidence:** Export tests generate redacted and full-detail packets; audit packets include lineage to events and approvals; access rules prevent unauthorized export of restricted evidence.

### 48. Operator ergonomics for high-volume service desk work

**Justification:** ITSM effectiveness depends on how quickly analysts can triage, update, and close records during heavy load, not only on correctness of the data model.

**Improvement:** Improve `ItServiceManagementWorkbench` for keyboard-heavy triage, bulk safe actions, inline status updates, recent-context panels, and visible next-best-action cues for incident and request queues.

**Acceptance evidence:** UI tests cover bulk safe actions and keyboard flows; analysts can update status without leaving the queue; queue views preserve filters and scroll position during rapid triage.

### 49. API completeness, idempotency, and correction commands

**Justification:** Create-only routes are insufficient for mature ITSM operations that must reopen, correct, simulate, and close records without duplicating state.

**Improvement:** Extend the package API surface with correction, reopen, approve, reject, simulate, export, and acknowledge commands for the core record types while preserving idempotency keys and permission checks.

**Acceptance evidence:** Contract tests prove duplicate submissions are safe; route manifests show command coverage across incidents, requests, changes, problems, and CIs; emitted events reflect the true action taken.

### 50. End-to-end domain scenario harness

**Justification:** The backlog needs a package-local proving ground that exercises realistic ITSM journeys rather than isolated table behavior.

**Improvement:** Create seeded acceptance scenarios that walk through major incident response, catalog request fulfillment, emergency change, recurring problem creation, CI impact analysis, and SLA breach handling using only package-declared routes, events, rules, and UI surfaces.

**Acceptance evidence:** Scenario runs produce deterministic evidence bundles; release verification reports each scenario outcome by name; maintainers can trace every scenario step back to package-owned capabilities.
