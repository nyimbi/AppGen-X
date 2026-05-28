# Public Safety Dispatch Improvement Backlog

## Current Domain Evidence Used

- Manifest key: `public_safety_dispatch`
- Description: emergency calls, units, incidents, dispatch, mutual aid, response times, and public safety operations
- Owned tables: `emergency_call`, `response_unit`, `incident`, `dispatch_assignment`, `mutual_aid`, `response_milestone`, `case_disposition`, `public_safety_dispatch_policy_rule`, `public_safety_dispatch_runtime_parameter`, `public_safety_dispatch_schema_extension`, `public_safety_dispatch_control_assertion`, `public_safety_dispatch_governed_model`
- APIs: `POST /emergency-calls`, `POST /response-units`, `POST /incidents`, `POST /dispatch-assignments`, `POST /mutual-aids`, `GET /public-safety-dispatch-workbench`
- UI fragments: `PublicSafetyDispatchWorkbench`, `PublicSafetyDispatchDetail`, `PublicSafetyDispatchAssistantPanel`
- Workflows: `public_safety_dispatch_create_emergency_call_workflow`, `public_safety_dispatch_record_response_unit_workflow`
- Emitted events: `PublicSafetyDispatchCreated`, `PublicSafetyDispatchUpdated`, `PublicSafetyDispatchApproved`, `PublicSafetyDispatchExceptionOpened`
- Consumed events: `PolicyChanged`, `CustomerUpdated`, `SupplierQualified`
- Existing advanced capabilities already named in the manifest include event-sourced operational history, predictive risk scoring, anomaly detection, semantic document understanding, cryptographic audit proofs, and governed AI agent execution

### 1. NG911 call intake model
**Justification:** `emergency_call` needs more than caller name and narrative if it is going to support real 911 intake. Dispatchers need ANI/ALI, callback validation, call source, language, callback failure reason, phase-two wireless precision, and abandoned-call handling.
**Improvement:** Expand intake for wireline, wireless, VoIP, text-to-911, alarm company relay, and third-party transfer calls. Capture call source metadata, recontact attempts, interpreter need, TTY/TDD flags, and line disconnect behavior in the initial call workflow.
**Acceptance evidence:** Manifest-aligned field map for `emergency_call`, intake test fixtures for each call source, and workbench screenshots showing ANI/ALI, callback, and abandoned-call indicators on the call detail panel.

### 2. Structured chief complaint capture
**Justification:** Free-text narratives are not enough for downstream unit recommendation, priority assignment, or QA review. Dispatch needs coded complaint capture tied to law, fire, and EMS protocols.
**Improvement:** Add a controlled chief-complaint taxonomy with discipline, protocol family, determinant code, subdeterminant, and caller-reported hazards. Require the intake flow to store both the coded complaint and the original caller wording.
**Acceptance evidence:** Complaint taxonomy seed data, workflow validation for required complaint codes, and release evidence showing coded complaint values flowing from `POST /emergency-calls` into `incident`.

### 3. Priority triage with protocol trace
**Justification:** Priority assignment has to be explainable after the fact, especially for cardiac arrest, active violence, structure fire, overdose, and welfare checks. A bare priority label does not show why the dispatcher chose it.
**Improvement:** Record the protocol path used to assign priority, including discriminator answers, upgrade and downgrade reasons, and supervisor overrides. Keep the full triage trace in `response_milestone` so later review can replay the decision.
**Acceptance evidence:** Priority decision audit on incident detail, tests for auto-priority plus override scenarios, and QA export showing the question-and-answer path that produced the final priority.

### 4. Incident creation deduplication
**Justification:** Multiple callers often report the same crash, fire, or assault within minutes. Without duplicate controls, dispatchers split radio traffic and units across separate incidents.
**Improvement:** Add duplicate detection based on time window, geocoded proximity, phone number overlap, premise history, and complaint similarity. Let intake staff merge to an existing `incident` or intentionally keep a new one with justification.
**Acceptance evidence:** Duplicate-match scoring rules, merge-versus-keep test cases, and workbench evidence of a duplicate review drawer before a second incident is committed.

### 5. Caller safety and responder safety prompts
**Justification:** Intake needs to protect both the caller and responding officer, firefighter, or medic. High-risk scenes require prompts for weapons, smoke conditions, hazardous materials, violent behavior, and contagious exposure.
**Improvement:** Add dynamic safety prompts that branch by complaint type and agency discipline. Surface officer safety notes, EMS exposure notes, and fireground hazard notes as structured flags, not only narrative text.
**Acceptance evidence:** Protocol trees for law, fire, and EMS safety prompts, structured hazard flags on the incident view, and verification that safety flags appear on unit dispatch cards and assistant summaries.

### 6. Location confidence scoring and geocoding fallback
**Justification:** Dispatch quality depends on location confidence, especially for cell callers on highways, apartment complexes, parks, and rural roads. A single geocode result without confidence or fallback causes unit misrouting.
**Improvement:** Store primary geocode, fallback geocode, confidence score, premise type, address source, and validation status. Route low-confidence locations to an address verification step before assignment when policy requires it.
**Acceptance evidence:** Geocoding confidence fields present in call and incident payloads, tests for apartment, mile-marker, and intersection address handling, and UI markers showing verified versus unverified locations.

### 7. Premise history on intake
**Justification:** Repeating hazards at a location matter immediately: prior violence, hoarding, oxygen use, Knox box availability, gate codes, hydrant limitations, or frequent lift assists change dispatch choices.
**Improvement:** Show recent incident history, premise caution notes, access instructions, and special occupancy indicators during intake and incident creation. Keep a clear separation between durable premise knowledge and incident-specific facts.
**Acceptance evidence:** Premise-history panel in `PublicSafetyDispatchWorkbench`, tests proving premise notes attach without mutating the new incident narrative, and release evidence with premise lookups recorded in operational history.

### 8. Multi-party caller and witness tracking
**Justification:** Dispatchers often receive callbacks from a caller, a witness, an alarm company, and a field unit on the same incident. Losing party roles creates confusion and weakens later records handoff.
**Improvement:** Support multiple related contacts per `emergency_call` and `incident`, with role, callback priority, reliability, and language preference. Preserve who supplied each fact in the intake timeline.
**Acceptance evidence:** Party-role data model changes, tests for caller plus witness plus third-party relay on one incident, and detail-page evidence showing attribution of facts to each contact.

### 9. Text-to-911 workflow
**Justification:** Text sessions behave differently from voice calls: longer latency, shorter answers, weaker location precision, and silent situations where calling is unsafe. The PBC needs explicit support instead of treating text like voice.
**Improvement:** Add a text intake mode with session transcript, heartbeat checks, canned prompt library, silent-call rules, and escalation to voice when safe. Track transcript fragments as part of `emergency_call` history.
**Acceptance evidence:** Text intake fixtures, UI transcript panel, and acceptance logs showing transcript capture, location verification, and transition from text session to incident dispatch.

### 10. Pre-arrival instruction logging
**Justification:** Medical, fire, and law enforcement pre-arrival instructions carry liability and clinical value. They have to be timestamped and attributable, not buried in narrative notes.
**Improvement:** Add structured pre-arrival instruction steps with protocol code, instruction delivered, caller compliance, interruption reason, and completion timestamp. Store them in the event history tied to the active call and incident.
**Acceptance evidence:** Protocol-step timeline on incident detail, tests for CPR, bleeding control, evacuation, and shelter-in-place instructions, and release evidence showing instruction delivery events.

### 11. CAD status normalization for units
**Justification:** `response_unit` is too coarse without consistent CAD statuses. Dispatch needs a canonical ladder like available, assigned, en route, on scene, transporting, at destination, clear, out of service, and unavailable.
**Improvement:** Define a typed CAD status model with allowed transitions, timestamp requirements, and discipline-specific variants for law, fire, and EMS. Reject impossible transitions such as clear-to-en-route without assignment context.
**Acceptance evidence:** State-transition tests for `response_unit`, status badges in the workbench unit queue, and release evidence proving every dispatched unit generates a consistent status sequence.

### 12. Unit recommendation engine
**Justification:** Dispatchers need recommendations grounded in location, unit type, response area, staffing, capability, and current assignment load. Manual mental routing does not scale during high call volume.
**Improvement:** Add recommendation logic for nearest appropriate unit, first-due apparatus, ALS/BLS matching, specialty teams, and cross-discipline co-response. Keep the explanation trace visible so dispatchers can accept or override with reason.
**Acceptance evidence:** Recommendation scorecards in the dispatch assignment UI, tests for police, fire, EMS, and combined response scenarios, and audit output showing why a recommended unit ranked first.

### 13. Responder availability and staffing checks
**Justification:** A unit marked available may still be unusable if minimum staffing, certifications, apparatus readiness, or equipment availability are missing. Dispatch needs operational readiness, not only a status flag.
**Improvement:** Extend `response_unit` readiness with staffing count, role coverage, medic level, apparatus state, and temporary restrictions. Block or warn on assignments that violate readiness policy.
**Acceptance evidence:** Readiness fields on unit detail, tests for under-staffed engine and unavailable medic scenarios, and assistant prompts that explain why a unit could not be dispatched.

### 14. Cross-staffing and move-up coverage
**Justification:** Fire and EMS systems frequently cross-staff apparatus and shift units to cover depleted districts. Dispatch should model the ripple effect instead of dispatching in isolation.
**Improvement:** Add move-up recommendations, cross-staffing exclusivity rules, and district coverage projections to `dispatch_assignment`. Show when sending one unit will uncover another response area below policy minimum.
**Acceptance evidence:** Coverage simulation panel, tests for cross-staffed ladder/engine conflicts, and dispatch evidence showing the system proposed a move-up after a working fire assignment.

### 15. Incident command structure support
**Justification:** Larger incidents require command roles, tactical channels, staging, divisions, and branches. A flat incident record does not support structure fires, mass casualty incidents, or extended law enforcement operations.
**Improvement:** Allow `incident` to track command designation, staging areas, tactical channel assignments, division/group structure, and command transfers. Keep command changes in the event timeline.
**Acceptance evidence:** Incident command section in detail UI, tests for command transfer and division creation, and event log outputs showing command role changes over the life of the incident.

### 16. Mutual aid request lifecycle
**Justification:** `mutual_aid` needs a formal lifecycle because requesting, offering, en route, on-scene, cancelled, and released states have different evidence and policy needs. Mutual aid failures are operational and political issues.
**Improvement:** Create a mutual aid workflow with requesting agency, requested resource, response deadline, acknowledgment, ETA, jurisdictional conditions, and demobilization. Distinguish automatic mutual aid from discretionary requests.
**Acceptance evidence:** Mutual aid state machine tests, request and acknowledgment timestamps in detail view, and release evidence showing a full mutual aid request lifecycle from creation to release.

### 17. Interagency interoperability notes
**Justification:** Mutual aid fails when dispatch lacks common channel plans, staging instructions, and resource naming translations. Those details should be operational data, not tribal knowledge.
**Improvement:** Add structured interoperability notes for agency radio plans, unit naming aliases, common staging points, and command contact methods. Surface them automatically when a mutual aid agency is selected.
**Acceptance evidence:** Interoperability reference records, UI evidence of auto-loaded agency notes during mutual aid creation, and tests proving alias translation is present on dispatch cards.

### 18. Officer safety BOLO linkage
**Justification:** BOLOs and hazard bulletins must affect active dispatching, not live in a separate silo. Units responding to vehicle stops, domestic violence, or wanted-person incidents need immediate BOLO context.
**Improvement:** Add BOLO entities or projections that can attach to incidents, persons, vehicles, and locations. Surface hit alerts in intake, incident detail, and dispatch assignment with acknowledgment tracking.
**Acceptance evidence:** BOLO match tests, workbench hit banner on affected incidents, and audit evidence showing which dispatcher acknowledged and relayed the BOLO warning.

### 19. Radio log capture and replay
**Justification:** Radio traffic is essential dispatch evidence for officer safety, timeline reconstruction, and records handoff. Narrative summaries do not preserve the sequence of unit traffic.
**Improvement:** Add structured radio log entries with timestamp, channel, speaker, transmission type, and linked incident or unit. Support later replay by ordering radio events with CAD status changes and call milestones.
**Acceptance evidence:** Radio log timeline in `PublicSafetyDispatchDetail`, tests for linked and unlinked radio traffic, and release evidence showing replay of a sample incident from call receipt through scene clearance.

### 20. Channel assignment governance
**Justification:** Dispatchers need help assigning the right radio channel for tactical, command, mutual aid, and hospital traffic. Wrong-channel assignments delay response and create safety risk.
**Improvement:** Add channel recommendation and validation rules based on discipline, jurisdiction, incident size, and current channel load. Require explicit justification when dispatchers override a reserved or overloaded channel.
**Acceptance evidence:** Channel assignment recommendations in the dispatch workflow, policy-rule tests for reserved channels, and event history proving channel changes were tracked with justification.

### 21. Scene safety escalation triggers
**Justification:** Escalation for mayday, officer emergency, firefighter PAR failure, or medic in distress cannot depend on ad hoc notes. The PBC should trigger unmistakable dispatch behavior.
**Improvement:** Create a safety escalation model that raises priority, opens supervisory attention, and pushes preconfigured unit recommendations when distress indicators are entered. Tie escalation to radio log, unit status, and incident command data.
**Acceptance evidence:** Safety escalation test suite, UI alerting on active distress incidents, and acceptance evidence showing an emergency-button workflow opened the correct dispatch and command actions.

### 22. High-risk location and premise caution governance
**Justification:** Premise caution notes can protect responders, but stale or unverified warnings can also create bias and noise. The PBC needs provenance and review dates.
**Improvement:** Add source, verification date, review owner, expiration rule, and access restrictions to premise cautions. Differentiate violent history, hazardous material storage, animal risk, access barriers, and medical environment notes.
**Acceptance evidence:** Caution-note lifecycle tests, workbench visibility rules by permission, and release evidence showing expired cautions no longer surface without review.

### 23. EMS destination and transport tracking
**Justification:** EMS incidents often continue after on-scene care through destination choice, diversion awareness, and patient transport milestones. Dispatch needs visibility into the transport phase.
**Improvement:** Add destination recommendation inputs, hospital status references, diversion flags, and transport milestones to `response_milestone` and `case_disposition`. Keep transport events linked to the originating incident.
**Acceptance evidence:** EMS transport timeline examples, tests for destination change and diversion scenarios, and detail-page evidence showing dispatch could see transport progress and final destination.

### 24. Fireground benchmark tracking
**Justification:** Working fire operations rely on benchmarks such as water on fire, primary search complete, secondary complete, under control, and loss stopped. Those benchmarks matter for accountability and post-incident review.
**Improvement:** Add discipline-specific operational benchmarks to `response_milestone`, starting with fireground milestones and timed benchmark prompts. Show overdue benchmark gaps to command and dispatch.
**Acceptance evidence:** Fire benchmark milestone tests, incident timeline entries for benchmark completion, and workbench evidence that overdue benchmark prompts appear for active fire incidents.

### 25. Unit arrival anomaly detection
**Justification:** Dispatch should detect impossible or suspicious travel and arrival patterns, such as on-scene before dispatch, clear without arrival, or extreme response-time outliers. These patterns often reveal radio status issues or data quality faults.
**Improvement:** Use the existing anomaly-detection capability to watch `dispatch_assignment` and `response_milestone` for broken status chronology, location mismatch, and improbable travel time. Route anomalies to QA or supervisor review.
**Acceptance evidence:** Anomaly rule set, sample anomaly cards in the workbench, and tests proving impossible status order opens `PublicSafetyDispatchExceptionOpened`.

### 26. Stolen vehicle and wanted person alert handling
**Justification:** BOLO support needs operational follow-through for vehicle stops, wanted subjects, and missing persons. Alert hits must be routed into unit safety and command supervision, not only displayed.
**Improvement:** Add hit types, mandatory acknowledgment, notify-supervisor actions, and incident-link creation for stolen vehicle and wanted person alerts. Capture whether the alert influenced dispatch priority or unit staging.
**Acceptance evidence:** Alert-hit workflows in the assistant and detail UI, tests for mandatory acknowledgment, and release evidence showing alert hits propagated into the incident timeline and unit dispatch cards.

### 27. Multi-incident unit conflict resolution
**Justification:** A single unit may be recommended for multiple incidents during spikes, especially for specialty teams or supervisors. Dispatch needs explicit conflict handling rather than last-write-wins behavior.
**Improvement:** Add conflict detection when a unit is simultaneously recommended, preassigned, or actually assigned elsewhere. Present dispatchers with hold, reassign, split-resource, or supervisory override options.
**Acceptance evidence:** Conflict-resolution tests, workbench conflict banner for shared units, and acceptance evidence showing override reason capture when a conflicted unit is dispatched anyway.

### 28. Staging and standby workflows
**Justification:** Not every response is direct-to-scene; some incidents require staging, hold short, perimeter, or cover assignment. Dispatch needs structured support for these tactical choices.
**Improvement:** Add standby and staging states with location, reason, command authority, and release condition. Allow staging instructions to flow onto unit dispatch cards and radio logs.
**Acceptance evidence:** CAD status tests for staged units, UI display of staging points and reasons, and event history showing transition from staged to assigned or released.

### 29. Supervisor approval gates for exceptional dispatches
**Justification:** Some dispatch actions need explicit approval: downgraded response to high-risk complaint, mutual aid cancellation, cross-jurisdiction assignment, or out-of-service override. Those decisions should be governed, not informal.
**Improvement:** Add policy-driven approval gates in `public_safety_dispatch_policy_rule` and `public_safety_dispatch_control_assertion` for exceptional dispatch decisions. Preserve who approved, when, and against which policy version.
**Acceptance evidence:** Approval workflow tests, audit trail with policy version, and release evidence showing a supervisor-approved exceptional dispatch with full justification.

### 30. Handoff from dispatch to records
**Justification:** `case_disposition` needs a better bridge from live dispatch to records, report writing, and downstream analytics. Missing timestamps, unit lists, or disposition flags force manual cleanup.
**Improvement:** Create a structured handoff package containing final call classification, priority history, units assigned, arrival and clear times, narrative summary, radio log references, and unresolved exceptions. Mark records handoff completeness before closure.
**Acceptance evidence:** Records handoff checklist in incident closure flow, export or event payload examples, and tests proving incomplete handoff blocks final case disposition without override.

### 31. Disposition coding discipline specificity
**Justification:** A single generic disposition list does not fit law enforcement, fire, and EMS. Dispatch analytics and records quality depend on discipline-specific disposition outcomes.
**Improvement:** Support discipline-scoped disposition code sets, including transport, refusal, arrest, citation, fire contained, false alarm, cancelled en route, unable to locate, and gone on arrival. Require mapping from operational outcome to records-ready disposition.
**Acceptance evidence:** Seeded disposition code tables, closure validation tests by discipline, and workbench evidence that final disposition choices change based on the incident response discipline.

### 32. Dispatch-focused workbench queues
**Justification:** The current manifest exposes `PublicSafetyDispatchWorkbench`, but the backlog should specify queue design for actual dispatch work. Operators need focused queues, not a generic list page.
**Improvement:** Create queue views for waiting intake, active incidents, units awaiting assignment, mutual aid pending acknowledgment, safety escalations, records handoff defects, and stale active calls. Keep queue filters pinned for discipline and jurisdiction.
**Acceptance evidence:** Queue definitions, route contracts for queue filters, and UI evidence showing counts and aging indicators for each operational queue.

### 33. Incident detail timeline that unifies call, dispatch, radio, and milestones
**Justification:** Dispatch review is impossible when call notes, unit statuses, and radio entries live in separate tabs without chronology. Operators need one authoritative incident timeline.
**Improvement:** Build a single timeline in `PublicSafetyDispatchDetail` that interleaves call intake steps, priority changes, dispatch assignments, CAD status changes, radio logs, safety alerts, and records handoff milestones. Preserve source labels for each event type.
**Acceptance evidence:** Detail-page timeline render, ordering tests for concurrent events, and release evidence showing a full incident replay from intake to closure.

### 34. Dispatcher keyboard-first UI and low-latency actions
**Justification:** Dispatchers work under time pressure and cannot rely on mouse-heavy forms. The UI must favor command entry, fast tab order, and minimal round trips.
**Improvement:** Add keyboard shortcuts for call creation, dispatch recommendation acceptance, unit status update, radio log entry, and incident search. Measure and surface latency budgets for the workbench’s highest-frequency actions.
**Acceptance evidence:** Shortcut map in UI help, workflow timing benchmarks for critical actions, and release evidence proving key dispatcher actions complete within the defined latency target.

### 35. Mapping panel with discipline overlays
**Justification:** Geospatial awareness is central to dispatch, especially for hydrants, station areas, patrol beats, evacuation zones, and hospital destinations. The PBC should treat mapping as operational context, not decoration.
**Improvement:** Add a map panel showing call location confidence, unit locations, jurisdiction polygons, first-due areas, hydrants, hospitals, and staging points. Support discipline-specific overlays and route warnings for road closures or restricted access.
**Acceptance evidence:** Map overlay specifications, UI screenshots for law/fire/EMS overlays, and tests proving the selected incident and assigned units stay synchronized with map state.

### 36. Assistant skill for intake summarization without unsafe mutation
**Justification:** `PublicSafetyDispatchAssistantPanel` should reduce typing burden while respecting dispatch safety. The assistant should summarize, suggest, and structure information before it is committed.
**Improvement:** Add an agent skill that turns call transcript or dispatcher notes into a structured intake draft, suggested chief complaint, missing-question checklist, and safety-note summary. Require human confirmation before any write to `emergency_call` or `incident`.
**Acceptance evidence:** Skill manifest for intake drafting, blocked-write tests without confirmation, and side-by-side evidence showing assistant draft versus final human-approved record.

### 37. Assistant skill for dispatch recommendation explanation
**Justification:** If the assistant suggests units or priority changes, dispatchers need transparent reasoning. Hidden scoring is not acceptable in this domain.
**Improvement:** Add an assistant mode that explains why a unit recommendation was produced using travel proximity, readiness, discipline match, coverage impact, and mutual aid availability. Keep explanations linked to actual `dispatch_assignment` candidates.
**Acceptance evidence:** Recommendation explanation cards in the assistant panel, tests that explanation fields match underlying recommendation inputs, and audit events for accepted or rejected AI suggestions.

### 38. Assistant skill for radio-log summarization and records prep
**Justification:** Closing incidents and preparing records packets is slow when dispatchers manually review long radio sequences. The assistant can help if it is bounded and evidence-linked.
**Improvement:** Add a summarization skill that converts radio logs and CAD milestones into a draft incident synopsis, unresolved-question list, and records handoff checklist. Cite every summary sentence back to source radio or milestone entries.
**Acceptance evidence:** Source-linked assistant summaries, tests for hallucination blocking when evidence is missing, and release evidence showing a records handoff draft built from actual radio and CAD data.

### 39. Event taxonomy beyond generic created and updated
**Justification:** The manifest currently emits generic lifecycle events, but dispatch integrations need domain events such as call received, incident merged, unit assigned, mutual aid acknowledged, and records handoff completed.
**Improvement:** Define a richer emitted-event taxonomy for call intake, incident lifecycle, unit dispatch, safety alerts, radio milestones, mutual aid, and records closure while keeping backward compatibility with existing manifest events. Publish event schemas and examples.
**Acceptance evidence:** Event schema catalog, contract tests for new domain events, and release evidence showing consumers can subscribe to unit assignment and records handoff events without reading generic updates.

### 40. Consumed-event handling for external policy and customer changes
**Justification:** `PolicyChanged`, `CustomerUpdated`, and `SupplierQualified` are generic consumed events in the manifest, but the dispatch package needs an explicit operational interpretation. Otherwise those subscriptions are shallow placeholders.
**Improvement:** Define how external policy or customer changes affect premise data, contract service areas, alarm response rules, and mutual aid eligibility. Open review tasks when a consumed event changes live dispatch behavior.
**Acceptance evidence:** Consumed-event handler specs, tests showing downstream recalculation of dispatch policy after a consumed event, and workbench evidence of queued review tasks triggered by upstream changes.

### 41. Event-sourced chain of custody for operational edits
**Justification:** Dispatch data is often corrected under pressure. Later reviewers need to know what changed, who changed it, and whether a correction altered dispatch decisions or records output.
**Improvement:** Use the existing event-sourced operational history capability to preserve every material edit to priority, location, unit assignment, safety flags, and disposition. Show before-and-after values with correction reason and actor.
**Acceptance evidence:** Point-in-time reconstruction for an edited incident, tests verifying correction reasons are mandatory for critical fields, and operational history views in the detail page.

### 42. Release evidence for protocol compliance
**Justification:** The backlog should demand proof that dispatch workflows remain compliant after change. Release evidence has to show more than green tests.
**Improvement:** Add release evidence sections for 911 intake protocol adherence, unit status chronology, mutual aid workflow coverage, BOLO handling, records handoff completeness, and assistant write-safety. Keep the evidence bundle under the package’s documented release surfaces.
**Acceptance evidence:** `RELEASE_EVIDENCE.md` entries or generated artifacts covering each operational area, with links to tests, screenshots, and event samples for the release candidate.

### 43. QA review package for critical incidents
**Justification:** Fatalities, officer-involved shootings, multiple-alarm fires, and high-visibility EMS events require a coherent review package. Dispatch should not require manual assembly from scattered screens.
**Improvement:** Generate a critical-incident review package with call intake, triage path, assignment timeline, radio log, BOLO hits, safety alerts, and records handoff data. Support redaction for protected information while preserving event sequence.
**Acceptance evidence:** Review package export specification, redaction tests, and release evidence showing the package can be generated for a sample critical incident without manual data stitching.

### 44. Jurisdiction and boundary policy enforcement
**Justification:** Dispatch must respect city, county, tribal, campus, and special-district boundaries while still supporting mutual aid and automatic aid. Boundary errors create real operational and legal consequences.
**Improvement:** Add jurisdiction policy checks to incident creation and dispatch assignment using location, agency coverage maps, and mutual aid agreements. Require override reason when dispatching outside the default boundary rule.
**Acceptance evidence:** Boundary-policy tests, map-based boundary indicators in the workbench, and audit history showing explicit override on an out-of-jurisdiction assignment.

### 45. Shift-change handoff board
**Justification:** Dispatch continuity suffers when active incidents, out-of-service units, and unresolved cautions are passed verbally only. The system should generate a shift handoff board.
**Improvement:** Build a handoff view listing active high-priority incidents, staged units, open mutual aid commitments, safety alerts, stale premise cautions, and records handoff defects. Allow dispatch supervisors to mark review completed at shift change.
**Acceptance evidence:** Shift handoff UI panel, tests proving critical items persist until reviewed, and release evidence showing a supervisor-signed handoff snapshot.

### 46. Outage and degraded-mode dispatch operations
**Justification:** Public safety dispatch must continue during GIS degradation, CAD lag, or external event bus issues. The package should specify what degraded mode looks like and how evidence is preserved.
**Improvement:** Add degraded-mode flags, manual-entry fallbacks, delayed-sync markers, and reconciliation workflows when geocoding, mapping, or event publishing is impaired. Surface operational banners and queue impacted records for later reconciliation.
**Acceptance evidence:** Failure-mode test scenarios, UI degraded-mode banners, and release evidence showing a dispatch entered during subsystem outage can later reconcile into normal event history.

### 47. Continuous control testing for dispatch data quality
**Justification:** Control testing is already named in the manifest and should be made concrete for dispatch. Data quality failures such as missing arrival times or unmatched unit clears should open operational exceptions automatically.
**Improvement:** Implement recurring control assertions for missing priority rationale, invalid CAD status order, unresolved geocode confidence, missing mutual aid acknowledgment, and incomplete records handoff. Feed failures into the exception queue.
**Acceptance evidence:** Control assertion catalog, automated exception generation tests, and workbench evidence of active control failures tied to specific incidents or assignments.

### 48. Training and simulation mode for dispatcher practice
**Justification:** Dispatch agencies need practice environments for new protocols, severe-weather load, active assailant scenarios, and MCI operations. Training should reuse the same domain model without polluting production evidence.
**Improvement:** Add simulation mode with synthetic calls, scripted radio traffic, dispatch recommendations, and records handoff drills. Clearly isolate simulation incidents, units, and events from live operational data.
**Acceptance evidence:** Training-mode policy controls, isolated event and data tests, and release evidence showing simulated incidents cannot appear in live queues or operational analytics.

### 49. Migration and seed data upgrades for dispatch realism
**Justification:** The manifest already declares migrations and seed data, but dispatch usefulness depends on realistic seeded complaint codes, unit types, CAD statuses, milestones, and dispositions. Thin seed data produces thin behavior.
**Improvement:** Expand migrations and seed data to include discipline-specific code tables, safety prompt sets, mutual aid agency profiles, channel plans, and benchmark milestone definitions. Keep them package-owned and versioned.
**Acceptance evidence:** Migration diff review, seed data verification tests, and package-local evidence showing new environments boot with realistic dispatch reference data instead of placeholders.

### 50. Package-level release gate tied to operational evidence
**Justification:** The final release decision for this PBC should depend on operational proof, not only static generation success. Dispatch changes can look fine in code review and still fail in live workflow coverage.
**Improvement:** Make release approval require evidence for intake, incident deduplication, unit recommendation, CAD status chronology, geocoding confidence, mutual aid lifecycle, responder safety alerts, radio logging, BOLO linkage, records handoff, UI latency, and assistant guardrails. Reject release if any required evidence artifact is missing.
**Acceptance evidence:** A release checklist mapped to the manifest docs, automated verification of required artifacts, and a final evidence summary showing all operational gates passed for `public_safety_dispatch`.
