# Nonprofit Program Impact Improvement Backlog

## Current Domain Evidence Used

- Manifest key: `nonprofit_program_impact`.
- Current purpose: programs, beneficiaries, outcomes, grants, services, restrictions, impact evidence, and donor reporting.
- Owned tables named in `manifest.py`: `program`, `beneficiary`, `service_episode`, `outcome_measure`, `grant_restriction`, `impact_evidence`, `donor_report`, `nonprofit_program_impact_policy_rule`, `nonprofit_program_impact_runtime_parameter`, `nonprofit_program_impact_schema_extension`, `nonprofit_program_impact_control_assertion`, `nonprofit_program_impact_governed_model`.
- Current APIs named in `manifest.py`: `POST /programs`, `POST /beneficiarys`, `POST /service-episodes`, `POST /outcome-measures`, `POST /grant-restrictions`, `GET /nonprofit-program-impact-workbench`.
- Current docs named in `manifest.py`: `SPECIFICATION.md` and `RELEASE_EVIDENCE.md`.
- Current UI fragments named in `manifest.py`: `NonprofitProgramImpactWorkbench`, `NonprofitProgramImpactDetail`, and `NonprofitProgramImpactAssistantPanel`.
- Current emitted events named in `manifest.py`: `NonprofitProgramImpactCreated`, `NonprofitProgramImpactUpdated`, `NonprofitProgramImpactApproved`, and `NonprofitProgramImpactExceptionOpened`.
- Current consumed events named in `manifest.py`: `PolicyChanged`, `CustomerUpdated`, and `SupplierQualified`.

### 1. Theory of change model per program
**Justification:** Impact claims are weak when a program record does not show the causal chain from activities to outputs, outcomes, and longer-term change.
**Improvement:** Add a first-class theory-of-change structure on `program` with assumptions, risk factors, target population, intervention components, expected outputs, short-term outcomes, medium-term outcomes, and impact horizon.
**Acceptance evidence:** Program detail shows a theory-of-change map; contract tests require every approved program to link services, outputs, and outcomes; `RELEASE_EVIDENCE.md` includes screenshots and sample records.

### 2. Outcome hierarchy and results chain linking
**Justification:** Nonprofit teams need to see whether an output actually contributes to a named outcome instead of storing disconnected counts.
**Improvement:** Link `service_episode`, output records, and `outcome_measure` entries through a results-chain model that supports one-to-many and many-to-one mappings, with explicit contribution logic.
**Acceptance evidence:** Tests cover output-to-outcome linking rules, UI drill-through from outcome to supporting services works, and release evidence shows traceability from one beneficiary interaction to one reported outcome.

### 3. Beneficiary identity, household, and cohort structure
**Justification:** Programs often serve people as individuals, households, or community groups, and impact analysis breaks when only a flat beneficiary record exists.
**Improvement:** Extend `beneficiary` to support person, household, caregiver-child pair, group, and institution-level beneficiary types, plus cohort membership and deduplication rules.
**Acceptance evidence:** Seed data includes mixed beneficiary types, duplicate detection tests pass, and the workbench can filter by individual, household, and cohort.

### 4. Beneficiary eligibility and targeting rules
**Justification:** Eligibility logic is part of program integrity, donor compliance, and fairness to intended participants.
**Improvement:** Model eligibility criteria on `program` and enforce them at `POST /beneficiarys` and service enrollment, including age bands, geography, vulnerability criteria, referral source, and exclusion rules.
**Acceptance evidence:** Validation tests reject ineligible enrollment, override flows require approval and rationale, and release evidence shows eligible and blocked examples.

### 5. Service catalog and intervention taxonomy
**Justification:** Service episodes are hard to analyze if the platform cannot distinguish counseling, training, cash transfer, referral, mentoring, and community outreach.
**Improvement:** Add a governed intervention taxonomy with service type, delivery channel, dosage unit, session length, recurrence, and implementing team or partner.
**Acceptance evidence:** Service forms use controlled vocabularies, analytics group by intervention family, and tests prove unknown service types cannot be used in approved programs.

### 6. Service fidelity and dosage tracking
**Justification:** Counting that a service happened is not enough when program quality depends on how much service was delivered and whether core components were completed.
**Improvement:** Extend `service_episode` with planned dosage, delivered dosage, attendance, completion markers, fidelity checklist results, and missed-session reasons.
**Acceptance evidence:** Detail pages show planned-versus-delivered dosage, dashboards expose fidelity gaps, and regression tests verify missed dosage affects outcome interpretation.

### 7. Output register for immediate deliverables
**Justification:** Many donor reports need verified outputs such as people reached, kits distributed, sessions completed, or referrals closed before outcome results mature.
**Improvement:** Introduce an output register linked to `service_episode` and `program`, with unit definitions, counting rules, de-duplication rules, and evidence attachments.
**Acceptance evidence:** Output totals reconcile with service records, counting-rule tests prevent double counting, and release evidence includes one output register export.

### 8. Outcome registry with temporal windows
**Justification:** Outcome measurement becomes inconsistent when each team interprets "improved wellbeing" or "increased income" differently.
**Improvement:** Strengthen `outcome_measure` with outcome definition, measurement window, unit of analysis, expected direction, data source, minimum evidence threshold, and attributable intervention scope.
**Acceptance evidence:** Outcome registry pages expose definitions and timing rules, tests enforce required fields before approval, and sample release evidence shows two outcomes with different follow-up windows.

### 9. Indicator dictionary and calculation logic
**Justification:** Indicators need precise numerators, denominators, disaggregation, and aggregation rules or dashboards will drift from donor reports.
**Improvement:** Add an indicator dictionary that defines calculation formulas, rollup rules, missing-data treatment, rounding rules, and allowed disaggregations for every reported indicator.
**Acceptance evidence:** Calculation tests cover numerator and denominator edge cases, indicator definitions render in the UI, and exported donor packs quote the same values as the dashboard.

### 10. Baselines, targets, and revision history
**Justification:** Programs need a defensible record of what they expected to achieve, when targets changed, and why.
**Improvement:** Store baseline values, target values, target periods, target revision reasons, and approval history on the program-outcome pair.
**Acceptance evidence:** Target history is visible in `NonprofitProgramImpactDetail`, unauthorized target edits are blocked, and release evidence shows one mid-year target revision with sign-off.

### 11. Survey instrument library
**Justification:** Survey-based outcomes need managed instruments, versioning, and question metadata rather than loose attachments.
**Improvement:** Add a survey library with instrument version, language, question type, answer options, skip logic, scoring rules, and linkages to outcomes and indicators.
**Acceptance evidence:** Survey metadata persists across versions, tests cover versioned scoring, and the assistant can cite which instrument version produced an outcome score.

### 12. Sampling, respondent selection, and survey cadence
**Justification:** Outcome credibility depends on who was surveyed, when, and how respondents were selected.
**Improvement:** Model sampling frame, sample size target, respondent selection rules, survey wave schedule, response status, and attrition reasons.
**Acceptance evidence:** Survey dashboards show target versus actual response counts, tests validate wave scheduling, and release evidence includes a sample completion report.

### 13. Consent capture and respondent rights
**Justification:** Outcome measurement and case evidence collection require explicit consent, withdrawal handling, and visibility into use restrictions.
**Improvement:** Add consent records on `beneficiary` and survey participation covering data use, photo or story use, contact follow-up, withdrawal date, and guardian consent where applicable.
**Acceptance evidence:** Blocked workflows prevent use of withdrawn responses, UI shows consent state before evidence assembly, and tests cover guardian and withdrawal scenarios.

### 14. Safeguarding risk flags on beneficiary and service records
**Justification:** Programs serving vulnerable populations need safeguarding signals embedded in operational workflows, not hidden in a separate narrative.
**Improvement:** Add safeguarding concern flags, risk level, immediate action needed, referral status, and restricted-view notes on `beneficiary` and `service_episode`.
**Acceptance evidence:** Sensitive fields are permission-gated, open safeguarding concerns appear in supervisor queues, and release evidence shows redacted screenshots and audit logs.

### 15. Safeguarding incident workflow and escalation
**Justification:** Recording a concern without escalation ownership or closure evidence creates operational and ethical risk.
**Improvement:** Build a safeguarding incident flow with intake, triage, assignment, action log, escalation timers, closure criteria, and survivor-centered access controls.
**Acceptance evidence:** Incident state transitions are tested, overdue escalations trigger events, and release evidence includes incident timeline evidence with protected details redacted.

### 16. Referral network and external service follow-through
**Justification:** Many nonprofit outcomes depend on referrals being completed outside the immediate program boundary.
**Improvement:** Extend `service_episode` to support referral issuance, receiving organization, appointment status, completion confirmation, and referral outcome.
**Acceptance evidence:** Referral completion rates are visible on dashboards, tests cover pending and completed referrals, and donor evidence can show referrals separate from direct service delivery.

### 17. Case evidence pack for qualitative proof
**Justification:** Donors and evaluators often need stories of change and supporting case evidence alongside numeric indicators.
**Improvement:** Structure `impact_evidence` to support case narratives, before-and-after snapshots, corroborating documents, quotes, photos, and confidentiality level.
**Acceptance evidence:** Evidence packs render with source citations, confidentiality labels control visibility, and release evidence includes one redacted case evidence example.

### 18. Evidence quality scoring and verification status
**Justification:** Numeric counts, survey results, and case stories should not be treated as equally strong evidence by default.
**Improvement:** Add evidence quality dimensions for source type, verification status, completeness, timeliness, triangulation, and reviewer confidence to `impact_evidence`.
**Acceptance evidence:** Quality scores recalculate when evidence changes, weak evidence is flagged in dashboards, and tests cover scoring across survey, case, and administrative sources.

### 19. Partner delivery structure and subaward boundaries
**Justification:** Program delivery often flows through local partners, and the PBC must show which results came from which delivery entity.
**Improvement:** Add partner organization, site, subaward, and delivery responsibility fields to `program`, `service_episode`, and `impact_evidence`, with clear ownership boundaries.
**Acceptance evidence:** Dashboards can segment results by partner, tests prove partner attribution persists through donor reporting, and release evidence includes one partner-level scorecard.

### 20. Partner data submission and verification workflow
**Justification:** Partner-supplied data needs controlled intake, review, and correction loops before it enters official reporting.
**Improvement:** Build partner submission queues with batch upload status, schema validation, discrepancy comments, approval checkpoints, and resubmission handling.
**Acceptance evidence:** Invalid partner uploads land in a review queue, accepted submissions create auditable records, and release evidence shows one rejected-then-corrected partner submission.

### 21. Grant restriction to program activity boundary
**Justification:** Restricted funding must be separated from unrestricted activity or impact claims can cross the wrong financial boundary.
**Improvement:** Make `grant_restriction` enforce allowed programs, service types, locations, date windows, and beneficiary categories, with explicit boundary checks before activity approval.
**Acceptance evidence:** Tests prevent disallowed services from being charged to a restricted grant, UI shows boundary failures clearly, and evidence includes one compliant and one blocked scenario.

### 22. Donor reporting boundary and attribution rules
**Justification:** One beneficiary may receive several services funded by different donors, so donor reports need defensible attribution logic.
**Improvement:** Add attribution rules on `donor_report` for direct funding, co-funding, proportional allocation, time-bound eligibility, and excluded evidence types.
**Acceptance evidence:** Attribution calculations are test-covered, donor report previews show allocation rationale, and release evidence includes a report with mixed funding sources.

### 23. Results reporting period and freeze controls
**Justification:** Donor reports should not silently change after review without a clear reopened-cycle record.
**Improvement:** Add reporting periods, freeze dates, reopen reasons, and locked indicator snapshots for `donor_report`.
**Acceptance evidence:** Frozen reports reject mutation without authorized reopen flow, snapshots can be reproduced, and release evidence includes period lock and reopen audit history.

### 24. Indicator disaggregation for equity analysis
**Justification:** Impact dashboards need to show who benefits, not only how many outcomes were recorded.
**Improvement:** Add governed disaggregation dimensions such as age band, gender, disability, geography, cohort, partner, and service channel to indicators and outcomes.
**Acceptance evidence:** Dashboard filters and exports support approved disaggregations, privacy rules suppress unsafe small-cell views, and tests validate rollup consistency.

### 25. Longitudinal follow-up and outcome persistence
**Justification:** Many nonprofit outcomes decay or strengthen over time, so a one-off measurement can misstate lasting impact.
**Improvement:** Support repeated follow-up waves on `outcome_measure` with scheduled reassessment dates, persistence classification, and loss-to-follow-up reasons.
**Acceptance evidence:** Timelines show baseline and follow-up values, attrition is reported explicitly, and tests verify persistence calculations over multiple waves.

### 26. Negative outcomes and unintended effects register
**Justification:** Responsible impact management requires tracking harm, dropout, stigma, conflict, or other unintended effects rather than publishing only positive results.
**Improvement:** Add an adverse-effects register linked to program, beneficiary, service, and partner records, with severity, source, mitigation action, and reporting rules.
**Acceptance evidence:** Dashboards include negative outcome trends, mitigation tasks are visible, and release evidence documents one resolved unintended-effect case.

### 27. Baseline context and comparison group support
**Justification:** Some programs need stronger causal interpretation than before-and-after snapshots alone.
**Improvement:** Add optional comparison-group, matched-cohort, and counterfactual metadata to outcomes and indicators, including methodological notes and use restrictions.
**Acceptance evidence:** Outcome detail shows method flags, unsupported attribution claims are blocked in donor reporting, and tests cover comparison-group availability and absence.

### 28. Community, site, and geography model
**Justification:** Programs commonly operate across communities and sites, and impact patterns are often geographic.
**Improvement:** Extend `program`, `beneficiary`, and `service_episode` with site, district, catchment area, and community hierarchy, including service coverage maps.
**Acceptance evidence:** Workbench filters by geography, partner delivery can be grouped by site, and release evidence includes one geographic heatmap export.

### 29. Impact dashboard for executive and M&E users
**Justification:** Executives and monitoring teams need different views of the same evidence without rebuilding metrics outside the PBC.
**Improvement:** Create dashboard modes for executive summary, program management, and M&E analysis, each with throughput, outputs, outcomes, survey completion, safeguarding, and partner performance panels.
**Acceptance evidence:** Role-based dashboards render from the same governed metrics, stale data warnings appear when projections lag, and release evidence includes screenshots for each mode.

### 30. Program detail UI tuned for causal review
**Justification:** Program reviewers need to inspect theory of change, target values, services, and outcome evidence on one screen.
**Improvement:** Redesign `NonprofitProgramImpactDetail` so a program page surfaces results chain, target status, partner mix, grant restrictions, and recent evidence without forcing spreadsheet export.
**Acceptance evidence:** UI tests cover navigation between theory, services, and outcomes, page load states are handled, and release evidence includes desktop and mobile screenshots.

### 31. Beneficiary timeline UI
**Justification:** Staff need a single timeline to understand what a participant received, when follow-up happened, and what outcomes were recorded.
**Improvement:** Add a beneficiary timeline showing enrollment, services, referrals, surveys, outcome observations, safeguarding actions, and case evidence milestones.
**Acceptance evidence:** Timeline ordering tests pass, sensitive entries respect permissions, and release evidence shows one full beneficiary journey with redactions where required.

### 32. Donor report review UI
**Justification:** Donor reporting is a distinct workflow from daily service operations and needs its own review surface.
**Improvement:** Add a `donor_report` review workspace with indicator previews, attribution explanations, evidence quality warnings, narrative sections, and approval checkpoints.
**Acceptance evidence:** Reviewers can drill from a reported number to its source evidence, freeze controls are visible, and release evidence includes a reviewed report snapshot.

### 33. Assistant skill for theory-of-change drafting
**Justification:** Program teams often start with narrative proposals, and converting them into a structured results chain is repetitive and error-prone.
**Improvement:** Add an assistant skill that reads proposals and drafts a theory of change, service taxonomy, outputs, and candidate outcomes into reviewable program fields.
**Acceptance evidence:** Assistant drafts cite source passages, human approval is required before save, and tests verify the skill cannot bypass policy or approval gates.

### 34. Assistant skill for survey and indicator QA
**Justification:** Measurement plans fail when questions do not map cleanly to indicators or when skip logic conflicts with scoring.
**Improvement:** Add an assistant skill that checks survey instruments against indicator definitions, flags missing questions, inconsistent scales, and weak disaggregation coverage.
**Acceptance evidence:** QA findings appear in `NonprofitProgramImpactAssistantPanel`, each finding links to the underlying survey field, and release evidence includes a resolved QA issue.

### 35. Assistant skill for case evidence assembly
**Justification:** High-quality case evidence packs require consistent redaction, structure, and linkage to outputs and outcomes.
**Improvement:** Add an assistant skill that assembles draft case evidence packs from approved notes, survey excerpts, media, and outcome observations while enforcing confidentiality rules.
**Acceptance evidence:** Draft evidence packs include provenance and redaction markers, reviewers approve before publication, and tests cover blocked use of non-consented materials.

### 36. Domain event expansion for service and outcome lifecycle
**Justification:** The current event list is too coarse to support replayable operational history for nonprofit impact work.
**Improvement:** Define finer-grained events for beneficiary enrolled, service completed, output verified, survey submitted, outcome observed, safeguarding incident opened, donor report frozen, and partner submission approved.
**Acceptance evidence:** Event schemas are documented, replay tests rebuild key projections, and `RELEASE_EVIDENCE.md` includes emitted examples and ordering checks.

### 37. Event lineage from source evidence to reported result
**Justification:** Users should be able to trace a reported number back to the exact records and review actions that produced it.
**Improvement:** Link emitted events, `impact_evidence`, `outcome_measure`, and `donor_report` snapshots through lineage metadata and projection checkpoints.
**Acceptance evidence:** One-click lineage view works from dashboard to source records, tests confirm replay consistency, and release evidence includes a lineage trail example.

### 38. Consumed-event handling for upstream policy and supplier changes
**Justification:** Upstream policy or supplier events can affect service delivery, safeguarding posture, and donor eligibility.
**Improvement:** Make `PolicyChanged`, `CustomerUpdated`, and `SupplierQualified` handlers map into program policy reviews, beneficiary contact updates, and partner verification or risk flags where relevant.
**Acceptance evidence:** Handler tests are idempotent, affected records enter the correct review queues, and release evidence shows one consumed-event driven recalculation.

### 39. Partner performance scorecards
**Justification:** Delivery partners need comparable views of timeliness, data quality, safeguarding responsiveness, and outcome performance.
**Improvement:** Build partner scorecards with service volume, output verification rate, survey response rate, evidence quality score, safeguarding closure time, and reporting punctuality.
**Acceptance evidence:** Scorecards can be filtered by grant and period, tests verify score formulas, and release evidence includes one partner comparison view.

### 40. Release evidence matrix by domain promise
**Justification:** Release claims should be backed by domain-specific proof, not only generic build artifacts.
**Improvement:** Structure `RELEASE_EVIDENCE.md` around theory of change, beneficiary management, service delivery, outputs, outcomes, indicators, surveys, safeguarding, donor reporting, partner delivery, dashboards, and events.
**Acceptance evidence:** Every release item links to a test, screenshot, seed dataset, or event sample; missing evidence blocks approval; and the matrix is referenced from the package docs.

### 41. Exception taxonomy for impact operations
**Justification:** Staff need a precise vocabulary for data-quality failures, late follow-up, attribution conflict, partner discrepancy, and safeguarding escalation.
**Improvement:** Add exception types, severity, owner, due date, and closure proof across `impact_evidence`, `donor_report`, and related queues.
**Acceptance evidence:** Exceptions appear in dedicated queues, overdue items emit alerts, and tests cover creation, reassignment, and closure with evidence.

### 42. Data retention, privacy, and story-use boundaries
**Justification:** Case evidence, survey responses, and beneficiary history have different retention and sharing constraints.
**Improvement:** Add retention schedules, field masking, export controls, and story-use restrictions by evidence type, consent state, and safeguarding risk.
**Acceptance evidence:** Expired data is hidden or purged according to policy, exports redact protected fields, and release evidence includes retention-policy verification.

### 43. Role and attribute-based access for sensitive impact data
**Justification:** Program staff, M&E analysts, safeguarding leads, and donor reviewers should not see the same data or controls.
**Improvement:** Extend the current permission set with role and attribute checks for safeguarding notes, survey raw responses, case media, donor freeze controls, and partner correction rights.
**Acceptance evidence:** Permission matrix tests pass, UI hides unavailable actions cleanly, and assistant commands fail safely when the actor lacks access.

### 44. Predictive underperformance and follow-up risk scoring
**Justification:** Teams need early warning when outputs are on track but outcomes, survey completion, or safeguarding closure are at risk.
**Improvement:** Add predictive scoring for low response rates, missed follow-ups, declining outcome trends, weak evidence quality, and partner submission delays.
**Acceptance evidence:** Risk cards explain main drivers, calibration reports are stored with release evidence, and tests cover low-, medium-, and high-risk examples.

### 45. Scenario simulation for target and funding changes
**Justification:** Program managers often need to ask what happens to expected impact if target populations, service dosage, or grant coverage changes.
**Improvement:** Add non-mutating simulations that estimate output and outcome shifts under changed budget, partner capacity, service mix, or follow-up completion assumptions.
**Acceptance evidence:** Scenario views compare baseline and proposed plans side by side, assumptions are visible, and release evidence includes one budget-reduction scenario.

### 46. Offline and low-connectivity field workflow
**Justification:** Surveys and service capture often happen in low-connectivity environments, and delayed sync must not corrupt evidence lineage.
**Improvement:** Support offline drafts for service episodes, survey submissions, and case evidence capture with local validation, sync reconciliation, and conflict handling.
**Acceptance evidence:** Sync tests cover duplicate upload prevention and conflict review, timestamps preserve capture and sync time, and release evidence includes offline-to-sync proof.

### 47. Localization and culturally appropriate measurement support
**Justification:** Programs frequently span multiple languages and communities, and meaning can shift across translations.
**Improvement:** Add localized labels, survey translations, culturally adapted answer options, and language-specific guidance for case evidence and safeguarding prompts.
**Acceptance evidence:** Instrument versions can be linked across languages, UI locale switching works for core screens, and release evidence includes one translated survey flow.

### 48. Accessibility and inclusive UI for field and review users
**Justification:** Impact systems should be usable by staff with different abilities and in stressful operational contexts.
**Improvement:** Improve `NonprofitProgramImpactWorkbench` and related screens for keyboard access, clear focus states, high-contrast charts, readable tables, and mobile-friendly evidence review.
**Acceptance evidence:** Accessibility checks pass for modified screens, manual keyboard walkthrough evidence is captured, and release evidence includes accessible dashboard screenshots.

### 49. Seed data and test fixtures that reflect real nonprofit impact operations
**Justification:** Thin fixtures miss the edge cases that matter in programs, surveys, safeguarding, and donor reporting.
**Improvement:** Expand package seed data to cover multiple programs, partners, grants, beneficiary types, survey waves, safeguarding incidents, negative outcomes, and frozen donor reports.
**Acceptance evidence:** `seed_data.py` produces a realistic demo environment, contract tests use domain-rich fixtures, and release evidence references the fixture set used in screenshots.

### 50. Go-live readiness gate for nonprofit impact releases
**Justification:** A release should not be approved until domain-critical flows, controls, and evidence are all proven together.
**Improvement:** Add a package-local release gate that requires passing evidence for theory-of-change setup, beneficiary enrollment, service capture, output verification, outcome measurement, safeguarding handling, donor reporting, partner submission review, event replay, and dashboard correctness.
**Acceptance evidence:** Approval is blocked when any domain gate is incomplete, the final release checklist is attached to `RELEASE_EVIDENCE.md`, and the package can show one fully evidenced end-to-end release record.
