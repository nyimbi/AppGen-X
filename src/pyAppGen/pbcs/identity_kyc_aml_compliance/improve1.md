# Identity KYC AML Compliance Improvement Backlog

This backlog is grounded in `manifest.py` and the current package boundary for `identity_kyc_aml_compliance`. Every item is specific to KYC, AML, sanctions, PEP, beneficial ownership, ongoing monitoring, suspicious activity handling, privacy, governed agent assistance, and release evidence.

## Current Domain Evidence Used

- PBC key: `identity_kyc_aml_compliance`
- Description: `Customer onboarding, identity proofing, beneficial ownership, screening, transaction monitoring, suspicious activity, and compliance cases`
- Owned tables: `kyc_profile`, `identity_document`, `beneficial_owner`, `screening_hit`, `monitoring_alert`, `suspicious_activity_case`, `compliance_review`, `identity_kyc_aml_compliance_policy_rule`, `identity_kyc_aml_compliance_runtime_parameter`, `identity_kyc_aml_compliance_schema_extension`, `identity_kyc_aml_compliance_control_assertion`, `identity_kyc_aml_compliance_governed_model`
- APIs: `POST /kyc-profiles`, `POST /identity-documents`, `POST /beneficial-owners`, `POST /screening-hits`, `POST /monitoring-alerts`, `GET /identity-kyc-aml-compliance-workbench`
- Emits: `IdentityKycAmlComplianceCreated`, `IdentityKycAmlComplianceUpdated`, `IdentityKycAmlComplianceApproved`, `IdentityKycAmlComplianceExceptionOpened`
- Consumes: `PolicyChanged`, `AuditEventSealed`, `OperationalKpiChanged`
- UI fragments: `IdentityKycAmlComplianceWorkbench`, `IdentityKycAmlComplianceDetail`, `IdentityKycAmlComplianceAssistantPanel`
- Docs: `SPECIFICATION.md`, `RELEASE_EVIDENCE.md`
- Capability surfaces: `identity_kyc_aml_compliance_event_sourced_operational_history`, `identity_kyc_aml_compliance_multi_tenant_policy_isolation`, `identity_kyc_aml_compliance_schema_evolution_resilience`, `identity_kyc_aml_compliance_autonomous_anomaly_detection`, `identity_kyc_aml_compliance_semantic_document_instruction_understanding`, `identity_kyc_aml_compliance_predictive_risk_scoring`, `identity_kyc_aml_compliance_counterfactual_scenario_simulation`, `identity_kyc_aml_compliance_cryptographic_audit_proofs`, `identity_kyc_aml_compliance_continuous_control_testing`, `identity_kyc_aml_compliance_governed_ai_agent_execution`, `appgen_x_outbox_inbox_eventing`, `idempotent_handlers`, `retry_dead_letter_evidence`, `agentic_document_instruction_intake`, `ai_agent_task_assistance`, `continuous_release_assurance`

### 1. KYC profile lifecycle evidence

**Key:** `identity_kyc_aml_compliance_kyc_profile_lifecycle_evidence`

**Justification:** KYC programs need explicit lifecycle states for intake, verification, approval, remediation, restriction, exit, and re-review or analysts cannot explain why a customer was onboarded, paused, or declined.

**Improvement:** Add a governed lifecycle for `kyc_profile` covering draft, pending verification, pending screening, pending EDD, approved, restricted, exited, and archived states with allowed transitions, mandatory evidence, and jurisdiction-aware reason codes.

**Acceptance evidence:** Lifecycle tests proving invalid transitions are blocked, visible status badges and reason history in `IdentityKycAmlComplianceWorkbench`, and release evidence linking each approval or exception path to emitted lifecycle events.

**Current Domain Evidence Used:** `kyc_profile`, `POST /kyc-profiles`, `IdentityKycAmlComplianceWorkbench`, `IdentityKycAmlComplianceCreated`, `IdentityKycAmlComplianceApproved`, `IdentityKycAmlComplianceExceptionOpened`

### 2. Onboarding classification gate

**Key:** `identity_kyc_aml_compliance_onboarding_classification_gate`

**Justification:** Individual, business, trust, correspondent, and high-risk customer types need different KYC and AML obligations; a flat onboarding path causes missing evidence and inconsistent approvals.

**Improvement:** Require `kyc_profile` creation to classify customer type, jurisdiction, product exposure, channel, and expected activity so the package can branch into the correct KYC, screening, beneficial ownership, and EDD obligations at intake time.

**Acceptance evidence:** Intake fixtures for individual and entity onboarding variants, blocked profile creation when mandatory classification fields are absent, and workbench panels showing which obligation set was attached to the profile.

**Current Domain Evidence Used:** `kyc_profile`, `POST /kyc-profiles`, `identity_kyc_aml_compliance_policy_rule`, `identity_kyc_aml_compliance_runtime_parameter`, `IdentityKycAmlComplianceWorkbench`

### 3. Duplicate identity resolution

**Key:** `identity_kyc_aml_compliance_duplicate_identity_resolution`

**Justification:** AML controls fail when the same person or entity is onboarded multiple times under slightly different identifiers, names, or documents.

**Improvement:** Add duplicate detection and merge review for `kyc_profile` using normalized names, dates of birth, national identifiers, registration numbers, and linked `identity_document` evidence, with analyst-controlled merge and split actions.

**Acceptance evidence:** Duplicate-match fixtures with true positive and false positive outcomes, merge review screens in `IdentityKycAmlComplianceDetail`, and audit-ready lineage showing which profiles were merged or separated.

**Current Domain Evidence Used:** `kyc_profile`, `identity_document`, `IdentityKycAmlComplianceDetail`, `identity_kyc_aml_compliance_event_sourced_operational_history`, `IdentityKycAmlComplianceUpdated`

### 4. Document capture completeness

**Key:** `identity_kyc_aml_compliance_document_capture_completeness`

**Justification:** Identity proofing starts with complete document capture; missing issuer, issue date, expiry date, or document type should block downstream verification and screening decisions.

**Improvement:** Extend `identity_document` intake so `POST /identity-documents` requires document class, jurisdiction, issuing authority, identifier, issue and expiry dates, capture method, and linkage to the owning `kyc_profile`.

**Acceptance evidence:** API tests rejecting incomplete document submissions, operator-visible completeness indicators in `IdentityKycAmlComplianceWorkbench`, and release evidence proving approved profiles do not bypass mandatory document fields.

**Current Domain Evidence Used:** `identity_document`, `kyc_profile`, `POST /identity-documents`, `IdentityKycAmlComplianceWorkbench`, `IdentityKycAmlComplianceExceptionOpened`

### 5. Document authenticity and expiry controls

**Key:** `identity_kyc_aml_compliance_document_authenticity_and_expiry_controls`

**Justification:** A captured document is not enough; KYC decisions depend on whether the document is valid, unexpired, and consistent with the claimed identity.

**Improvement:** Add authenticity, tamper, and expiry evaluation states to `identity_document` so analysts can distinguish accepted documents, suspected forgeries, expired documents, and documents requiring replacement before approval.

**Acceptance evidence:** Verification scenarios for valid, expired, mismatched, and suspicious documents, document-status history in `IdentityKycAmlComplianceDetail`, and exception events when authenticity or expiry rules fail.

**Current Domain Evidence Used:** `identity_document`, `kyc_profile`, `IdentityKycAmlComplianceDetail`, `IdentityKycAmlComplianceUpdated`, `IdentityKycAmlComplianceExceptionOpened`

### 6. Selfie liveness and face-match evidence

**Key:** `identity_kyc_aml_compliance_selfie_liveness_and_face_match_evidence`

**Justification:** Remote onboarding often depends on liveness and face-match checks; without explicit evidence the package cannot defend non-face-to-face identity verification.

**Improvement:** Add biometric verification evidence linked to `identity_document` and `kyc_profile`, including liveness outcome, face-match confidence, capture timestamp, retry count, and fallback manual review path.

**Acceptance evidence:** Remote-onboarding test packs showing successful and failed liveness journeys, analyst review screens with confidence and retry history, and release evidence that high-risk remote profiles cannot approve without biometric or equivalent substitute evidence.

**Current Domain Evidence Used:** `identity_document`, `kyc_profile`, `IdentityKycAmlComplianceDetail`, `identity_kyc_aml_compliance_control_assertion`, `RELEASE_EVIDENCE.md`

### 7. Sanctions screening match model

**Key:** `identity_kyc_aml_compliance_sanctions_screening_match_model`

**Justification:** Sanctions screening needs structured match evidence, alias handling, jurisdiction context, and severity so operations can separate exact matches from weak fuzzy hits.

**Improvement:** Expand `screening_hit` to store watchlist source, match basis, alias or transliteration pathway, country or program context, confidence, disposition requirement, and blocking severity for sanctions reviews.

**Acceptance evidence:** Screening fixtures covering exact, fuzzy, and false positive sanctions hits, workbench views that show why a hit matched, and exception opening when a blocking sanctions hit remains unresolved.

**Current Domain Evidence Used:** `screening_hit`, `POST /screening-hits`, `IdentityKycAmlComplianceWorkbench`, `IdentityKycAmlComplianceExceptionOpened`, `identity_kyc_aml_compliance_workflow`

### 8. PEP and RCA screening boundary

**Key:** `identity_kyc_aml_compliance_pep_and_rca_screening_boundary`

**Justification:** PEP and related-close-associate screening should not be handled as ordinary sanctions logic because escalation, review depth, and approval standards differ.

**Improvement:** Add explicit screening categories and review tracks so `screening_hit` can distinguish sanctions, PEP, RCA, adverse media, and internal deny-list outcomes with different thresholds, reviewers, and resolution paths.

**Acceptance evidence:** Rule-driven routing of PEP and RCA hits into separate analyst queues, distinct severity and approval requirements in the detail UI, and release evidence proving PEP hits do not close through the sanctions-only workflow.

**Current Domain Evidence Used:** `screening_hit`, `identity_kyc_aml_compliance_policy_rule`, `IdentityKycAmlComplianceWorkbench`, `IdentityKycAmlComplianceDetail`, `IdentityKycAmlComplianceApproved`

### 9. Screening disposition and reason taxonomy

**Key:** `identity_kyc_aml_compliance_screening_disposition_and_reason_taxonomy`

**Justification:** Analysts need consistent reason codes to explain false positives, escalations, dismissals, and true matches across sanctions and PEP programs.

**Improvement:** Add a governed disposition taxonomy for `screening_hit` covering false positive, escalated, matched and restricted, matched and approved with EDD, duplicate, and pending external evidence, each with mandatory rationale and reviewer evidence.

**Acceptance evidence:** Disposition tests enforcing mandatory reasons, analytics showing top disposition causes, and detail screens that preserve reviewer, time, and evidence for each screening resolution.

**Current Domain Evidence Used:** `screening_hit`, `compliance_review`, `IdentityKycAmlComplianceDetail`, `identity_kyc_aml_compliance_analytics`, `IdentityKycAmlComplianceUpdated`

### 10. Beneficial ownership graph

**Key:** `identity_kyc_aml_compliance_beneficial_ownership_graph`

**Justification:** Entity onboarding requires a traceable ownership and control structure; flat owner rows cannot explain layered ownership, indirect interests, or controlling persons.

**Improvement:** Model `beneficial_owner` as a graph with direct and indirect ownership percentages, control relationships, entity-to-entity links, and effective dates so entity KYC can reconstruct ultimate beneficial ownership.

**Acceptance evidence:** Ownership graph fixtures for simple and layered structures, graph views in `IdentityKycAmlComplianceDetail`, and release evidence showing approval is blocked when the graph cannot reach a declared ultimate owner or controller.

**Current Domain Evidence Used:** `beneficial_owner`, `kyc_profile`, `POST /beneficial-owners`, `IdentityKycAmlComplianceDetail`, `IdentityKycAmlComplianceApproved`

### 11. Beneficial owner threshold policy

**Key:** `identity_kyc_aml_compliance_beneficial_owner_threshold_policy`

**Justification:** Threshold rules vary by jurisdiction and product; hard-coded ownership percentages create under-screening or unnecessary review.

**Improvement:** Drive beneficial ownership obligations through `identity_kyc_aml_compliance_policy_rule` and `identity_kyc_aml_compliance_runtime_parameter` so the package can apply jurisdiction-specific thresholds for ownership, voting control, and other control indicators.

**Acceptance evidence:** Policy simulations showing threshold changes without code changes, blocked approvals when declared owners fall below configured evidence coverage, and a configuration workbench view showing the active threshold set.

**Current Domain Evidence Used:** `beneficial_owner`, `identity_kyc_aml_compliance_policy_rule`, `identity_kyc_aml_compliance_runtime_parameter`, `configuration_workbench`, `identity_kyc_aml_compliance_counterfactual_scenario_simulation`

### 12. Nominee and control-person handling

**Key:** `identity_kyc_aml_compliance_nominee_and_control_person_handling`

**Justification:** AML reviews need to capture nominees, signatories, and controlling persons even when they do not cross ownership thresholds.

**Improvement:** Extend `beneficial_owner` and `compliance_review` so the package can separately track legal owners, nominee owners, authorized signers, board controllers, and other control persons with explicit role types and screening requirements.

**Acceptance evidence:** Entity-review examples where a low-ownership controller still triggers screening and approval steps, analyst-visible role-type badges in the detail view, and release evidence proving control-person screening is not skipped on entity cases.

**Current Domain Evidence Used:** `beneficial_owner`, `compliance_review`, `screening_hit`, `IdentityKycAmlComplianceDetail`, `IdentityKycAmlComplianceExceptionOpened`

### 13. Source of funds and source of wealth evidence

**Key:** `identity_kyc_aml_compliance_source_of_funds_and_source_of_wealth_evidence`

**Justification:** Higher-risk KYC and AML programs need structured source-of-funds and source-of-wealth evidence rather than free-text notes that cannot be tested or reviewed.

**Improvement:** Add evidence capture for source of funds, source of wealth, expected activity, declared occupation or business, and supporting documentation within `compliance_review` and linked `identity_document` records.

**Acceptance evidence:** EDD review packs showing source evidence and supporting documents, mandatory-review tests for higher-risk profiles, and workbench warnings when approval is attempted without the required source evidence.

**Current Domain Evidence Used:** `compliance_review`, `identity_document`, `kyc_profile`, `IdentityKycAmlComplianceWorkbench`, `IdentityKycAmlComplianceApproved`

### 14. Enhanced due diligence trigger matrix

**Key:** `identity_kyc_aml_compliance_enhanced_due_diligence_trigger_matrix`

**Justification:** EDD should activate consistently for PEP exposure, high-risk geographies, complex ownership, adverse media, and unusual activity, not only when an analyst remembers to escalate.

**Improvement:** Create a trigger matrix in `identity_kyc_aml_compliance_policy_rule` that promotes `kyc_profile` or `screening_hit` outcomes into mandatory EDD review paths with required evidence and approval levels.

**Acceptance evidence:** Trigger tests for PEP, geography, ownership complexity, and adverse-media scenarios, automatic EDD badges in `IdentityKycAmlComplianceWorkbench`, and exception creation when required EDD steps remain incomplete.

**Current Domain Evidence Used:** `kyc_profile`, `screening_hit`, `identity_kyc_aml_compliance_policy_rule`, `IdentityKycAmlComplianceWorkbench`, `IdentityKycAmlComplianceExceptionOpened`

### 15. Enhanced due diligence review packet

**Key:** `identity_kyc_aml_compliance_enhanced_due_diligence_review_packet`

**Justification:** EDD requires a single review packet that brings together identity, ownership, screening, expected activity, and analyst findings for final decisions.

**Improvement:** Build an EDD packet view on `compliance_review` that assembles identity documents, beneficial owners, unresolved screening hits, expected activity, source evidence, and reviewer commentary into one decision surface.

**Acceptance evidence:** Decision packets accessible from `IdentityKycAmlComplianceDetail`, side-by-side review evidence before approval, and release evidence confirming EDD-required profiles cannot approve without a completed packet.

**Current Domain Evidence Used:** `compliance_review`, `identity_document`, `beneficial_owner`, `screening_hit`, `IdentityKycAmlComplianceDetail`, `RELEASE_EVIDENCE.md`

### 16. Risk score factor model

**Key:** `identity_kyc_aml_compliance_risk_score_factor_model`

**Justification:** Risk scoring needs explicit factors for customer type, geography, product, ownership complexity, screening outcomes, and activity expectations or it becomes opaque and hard to challenge.

**Improvement:** Expand `identity_kyc_aml_compliance_risk_score` into a factor model that records the contribution of geography, customer type, product risk, ownership risk, screening severity, and monitoring history at the `kyc_profile` level.

**Acceptance evidence:** Factor-level score explanations in the workbench, calibration tests for low, medium, and high-risk profiles, and release evidence showing the active factor model version.

**Current Domain Evidence Used:** `kyc_profile`, `identity_kyc_aml_compliance_risk_score`, `identity_kyc_aml_compliance_predictive_risk_scoring`, `IdentityKycAmlComplianceWorkbench`, `RELEASE_EVIDENCE.md`

### 17. Risk score explainability and challenge flow

**Key:** `identity_kyc_aml_compliance_risk_score_explainability_and_challenge_flow`

**Justification:** Compliance teams need to challenge or override risk scores with explicit rationale, especially when a profile is escalated or declined.

**Improvement:** Add explainability and challenge controls so `compliance_review` can show factor contributions, analyst challenge notes, supervisor decisions, and the final approved score with override lineage.

**Acceptance evidence:** Override tests proving no score challenge can close without reviewer evidence, detail views that show original and challenged scores, and release evidence listing open challenged-risk cases.

**Current Domain Evidence Used:** `compliance_review`, `identity_kyc_aml_compliance_risk_score`, `IdentityKycAmlComplianceDetail`, `IdentityKycAmlComplianceApproved`, `IdentityKycAmlComplianceUpdated`

### 18. Periodic rescreening policy

**Key:** `identity_kyc_aml_compliance_periodic_rescreening_policy`

**Justification:** Ongoing monitoring is not only transaction-triggered; customers, owners, and controllers need periodic rescreening based on risk and jurisdiction.

**Improvement:** Add periodic rescreening schedules to `kyc_profile` and `beneficial_owner` records so the package can compute next-screening due dates by risk tier, customer type, and screening category.

**Acceptance evidence:** Due-date calculations for low, medium, and high-risk profiles, workbench aging queues for overdue rescreens, and control failures when overdue profiles remain active without rescreening evidence.

**Current Domain Evidence Used:** `kyc_profile`, `beneficial_owner`, `screening_hit`, `identity_kyc_aml_compliance_runtime_parameter`, `IdentityKycAmlComplianceWorkbench`, `identity_kyc_aml_compliance_continuous_control_testing`

### 19. Event-driven rescreening handlers

**Key:** `identity_kyc_aml_compliance_event_driven_rescreening_handlers`

**Justification:** Policy changes, audit findings, and operational risk shifts should trigger targeted rescreening without relying on manual spreadsheets.

**Improvement:** Implement inbox handlers that react to `PolicyChanged`, `AuditEventSealed`, and `OperationalKpiChanged` by recalculating screening obligations, opening monitoring alerts, or scheduling immediate rescreening where required.

**Acceptance evidence:** Idempotent handler tests for repeated inbound events, event lineage from inbox to alert or review action, and release evidence mapping active rescreening triggers to the consumed events that caused them.

**Current Domain Evidence Used:** `PolicyChanged`, `AuditEventSealed`, `OperationalKpiChanged`, `appgen_x_outbox_inbox_eventing`, `idempotent_handlers`, `monitoring_alert`

### 20. Monitoring alert intake and triage

**Key:** `identity_kyc_aml_compliance_monitoring_alert_intake_and_triage`

**Justification:** Ongoing AML monitoring generates alerts that need structured triage rather than free-text queues or email handoffs.

**Improvement:** Expand `monitoring_alert` with source type, typology, severity, related profile, related owner, review SLA, analyst assignment, and preliminary disposition so alert operations can prioritize work consistently.

**Acceptance evidence:** Alert triage queues in `IdentityKycAmlComplianceWorkbench`, SLA and severity tests for generated alerts, and exception evidence when high-severity alerts remain unassigned past their due window.

**Current Domain Evidence Used:** `monitoring_alert`, `POST /monitoring-alerts`, `GET /identity-kyc-aml-compliance-workbench`, `IdentityKycAmlComplianceWorkbench`, `IdentityKycAmlComplianceExceptionOpened`

### 21. Alert-to-case promotion boundary

**Key:** `identity_kyc_aml_compliance_alert_to_case_promotion_boundary`

**Justification:** Not every monitoring alert becomes a suspicious activity case; the package needs explicit promotion rules and evidence to explain when that threshold was crossed.

**Improvement:** Add promotion controls between `monitoring_alert` and `suspicious_activity_case` so analysts must record typology, materiality, related evidence, and reviewer confirmation when opening a case from an alert.

**Acceptance evidence:** Promotion tests that distinguish closed alerts from case-worthy alerts, detail views showing the alert-to-case lineage, and release evidence confirming that every open suspicious activity case traces back to a trigger path.

**Current Domain Evidence Used:** `monitoring_alert`, `suspicious_activity_case`, `IdentityKycAmlComplianceDetail`, `IdentityKycAmlComplianceExceptionOpened`, `identity_kyc_aml_compliance_event_sourced_operational_history`

### 22. Suspicious activity case lifecycle

**Key:** `identity_kyc_aml_compliance_suspicious_activity_case_lifecycle`

**Justification:** AML casework needs explicit states for investigation, escalation, filing preparation, hold, closure, and post-filing review so teams can prove why action was or was not taken.

**Improvement:** Add a lifecycle for `suspicious_activity_case` covering opened, under investigation, pending filing decision, filed, no-file with rationale, law-enforcement hold, and closed states with required evidence at each stage.

**Acceptance evidence:** Case-state transition tests, visible timeline views in `IdentityKycAmlComplianceDetail`, and release evidence showing open-case counts by state and aging.

**Current Domain Evidence Used:** `suspicious_activity_case`, `compliance_review`, `IdentityKycAmlComplianceDetail`, `IdentityKycAmlComplianceUpdated`, `RELEASE_EVIDENCE.md`

### 23. SAR and STR narrative plus filing boundary

**Key:** `identity_kyc_aml_compliance_sar_and_str_narrative_plus_filing_boundary`

**Justification:** Suspicious activity narratives are sensitive and should be prepared, reviewed, and disclosed through a tightly controlled filing boundary distinct from general analyst notes.

**Improvement:** Add a restricted filing workspace on `suspicious_activity_case` for narrative drafting, supporting evidence selection, filing status, supervisory approval, and post-filing access controls without exposing the narrative to ordinary workbench roles.

**Acceptance evidence:** Restricted-access UI states for case narratives, filing decision tests that enforce supervisory approval, and release evidence proving filing artifacts are excluded from broad analyst exports unless explicitly authorized.

**Current Domain Evidence Used:** `suspicious_activity_case`, `compliance_review`, `IdentityKycAmlComplianceDetail`, `permissions`, `RELEASE_EVIDENCE.md`

### 24. Maker-checker and approval chain

**Key:** `identity_kyc_aml_compliance_maker_checker_and_approval_chain`

**Justification:** KYC approvals, EDD signoff, sanctions resolution, and suspicious activity filing decisions need dual control to reduce error and misconduct risk.

**Improvement:** Expand `compliance_review` so the package records preparer, reviewer, approver, approval level, delegated authority, and segregation-of-duties checks for high-impact decisions.

**Acceptance evidence:** Approval-chain tests preventing self-approval on high-risk decisions, review history in `IdentityKycAmlComplianceDetail`, and control assertions that fail when approvals violate policy.

**Current Domain Evidence Used:** `compliance_review`, `permissions`, `identity_kyc_aml_compliance_control_assertion`, `IdentityKycAmlComplianceDetail`, `IdentityKycAmlComplianceApproved`

### 25. Privacy, consent, and lawful basis tracking

**Key:** `identity_kyc_aml_compliance_privacy_consent_and_lawful_basis_tracking`

**Justification:** KYC and AML processing is legally justified but still needs explicit data-use basis, consent capture where relevant, and purpose boundaries for personal data handling.

**Improvement:** Add purpose, lawful basis, consent status where applicable, and disclosure restrictions to `kyc_profile` and `identity_document` handling so operators can distinguish mandatory compliance processing from optional outreach or enrichment.

**Acceptance evidence:** Data-use tests for mandatory compliance versus optional processing, masked views for consent-restricted fields, and release evidence showing lawful-basis coverage for all stored customer identity fields.

**Current Domain Evidence Used:** `kyc_profile`, `identity_document`, `permissions`, `IdentityKycAmlComplianceWorkbench`, `RELEASE_EVIDENCE.md`

### 26. Retention and purge controls

**Key:** `identity_kyc_aml_compliance_retention_and_purge_controls`

**Justification:** KYC and AML records often have long retention windows, but expired records still need governed purge or archive actions with hold support.

**Improvement:** Add retention schedules and purge-readiness controls across `kyc_profile`, `identity_document`, `screening_hit`, `monitoring_alert`, and `suspicious_activity_case`, including legal-hold and investigation-hold blockers.

**Acceptance evidence:** Retention-rule tests across active, closed, and held records, purge-readiness dashboards in the workbench, and release evidence showing records under hold are excluded from purge jobs.

**Current Domain Evidence Used:** `kyc_profile`, `identity_document`, `screening_hit`, `monitoring_alert`, `suspicious_activity_case`, `identity_kyc_aml_compliance_control_assertion`

### 27. Redaction and need-to-know exports

**Key:** `identity_kyc_aml_compliance_redaction_and_need_to_know_exports`

**Justification:** Compliance teams need to share screening, monitoring, and case evidence while minimizing exposure of identity data, narrative text, and restricted filing information.

**Improvement:** Add export profiles with role-based redaction for `identity_document`, `screening_hit`, `monitoring_alert`, and `suspicious_activity_case`, preserving traceability while masking fields outside the recipient's need-to-know scope.

**Acceptance evidence:** Export previews showing masked and unmasked variants, permission tests for restricted case data, and release evidence proving exported packets preserve references without leaking redacted values.

**Current Domain Evidence Used:** `identity_document`, `screening_hit`, `monitoring_alert`, `suspicious_activity_case`, `permissions`, `RELEASE_EVIDENCE.md`

### 28. Jurisdiction and country-risk matrix

**Key:** `identity_kyc_aml_compliance_jurisdiction_and_country_risk_matrix`

**Justification:** Geography drives onboarding requirements, EDD thresholds, sanctions interpretation, and ongoing monitoring intensity.

**Improvement:** Add a jurisdiction and country-risk matrix in `identity_kyc_aml_compliance_policy_rule` so `kyc_profile` and `beneficial_owner` reviews can apply geography-specific KYC requirements, screening strictness, and monitoring cadences.

**Acceptance evidence:** Policy simulations for low and high-risk geographies, profile detail views showing which geography rules applied, and control failures when a profile lacks the jurisdiction data needed for the active matrix.

**Current Domain Evidence Used:** `kyc_profile`, `beneficial_owner`, `identity_kyc_aml_compliance_policy_rule`, `identity_kyc_aml_compliance_runtime_parameter`, `identity_kyc_aml_compliance_counterfactual_scenario_simulation`

### 29. Onboarding API idempotency

**Key:** `identity_kyc_aml_compliance_onboarding_api_idempotency`

**Justification:** Upstream onboarding systems retry requests; duplicate profile or document creation is unacceptable in a KYC boundary.

**Improvement:** Enforce idempotent request handling across `POST /kyc-profiles`, `POST /identity-documents`, and `POST /beneficial-owners`, including request fingerprints, duplicate suppression, and conflict responses when a key is reused with different content.

**Acceptance evidence:** API tests proving safe retries and conflict detection, audit traces for deduplicated requests, and release evidence summarizing idempotency coverage for the write surface.

**Current Domain Evidence Used:** `POST /kyc-profiles`, `POST /identity-documents`, `POST /beneficial-owners`, `idempotent_handlers`, `continuous_release_assurance`, `RELEASE_EVIDENCE.md`

### 30. Document submission file-safety gate

**Key:** `identity_kyc_aml_compliance_document_submission_file_safety_gate`

**Justification:** Identity-document uploads are a common path for malformed, duplicated, or unsafe files that can pollute evidence or create operational risk.

**Improvement:** Add file-safety checks around `POST /identity-documents` for allowed types, duplicate uploads, hash tracking, page completeness, and quarantine states before a document can participate in KYC decisions.

**Acceptance evidence:** Upload fixtures for valid, duplicate, incomplete, and quarantined files, detail views showing file-safety status, and release evidence proving quarantined files cannot satisfy approval requirements.

**Current Domain Evidence Used:** `POST /identity-documents`, `identity_document`, `IdentityKycAmlComplianceDetail`, `IdentityKycAmlComplianceExceptionOpened`, `RELEASE_EVIDENCE.md`

### 31. Beneficial owner bulk update lineage

**Key:** `identity_kyc_aml_compliance_beneficial_owner_bulk_update_lineage`

**Justification:** Entity structures change in batches during annual reviews, reorganizations, and remediation; bulk updates need row-level lineage and partial-failure handling.

**Improvement:** Add governed bulk operations for `beneficial_owner` that preserve who changed each owner record, what percentage or control fact changed, and which downstream screening or review tasks were reopened.

**Acceptance evidence:** Bulk update fixtures with mixed success and failure rows, lineage views for before and after ownership structures, and release evidence showing reopened screening obligations after a bulk change.

**Current Domain Evidence Used:** `beneficial_owner`, `POST /beneficial-owners`, `IdentityKycAmlComplianceDetail`, `IdentityKycAmlComplianceUpdated`, `identity_kyc_aml_compliance_event_sourced_operational_history`

### 32. Screening-hit event contracts

**Key:** `identity_kyc_aml_compliance_screening_hit_event_contracts`

**Justification:** Downstream consumers need precise signals when a screening result is created, updated, resolved, or escalated; generic package-level events are too coarse for operational routing.

**Improvement:** Extend emitted-event coverage so `screening_hit` changes produce typed, versioned payloads tied back to the package-level event stream without leaking fields that belong only inside the KYC boundary.

**Acceptance evidence:** Event-schema compatibility tests, release evidence with example emitted payloads and version notes, and proof that screening lifecycle changes can be reconstructed without direct table reads.

**Current Domain Evidence Used:** `screening_hit`, `IdentityKycAmlComplianceCreated`, `IdentityKycAmlComplianceUpdated`, `IdentityKycAmlComplianceExceptionOpened`, `RELEASE_EVIDENCE.md`

### 33. Ongoing monitoring events and projections

**Key:** `identity_kyc_aml_compliance_ongoing_monitoring_events_and_projections`

**Justification:** Monitoring programs need fresh projections for queue operations, trend review, and executive oversight rather than direct reads against raw alerts and cases.

**Improvement:** Build dedicated projections for `monitoring_alert` and `suspicious_activity_case` covering queue state, severity, aging, typology, filing stage, and backlog risk while preserving event-sourced lineage.

**Acceptance evidence:** Projection freshness indicators in `IdentityKycAmlComplianceWorkbench`, replay tests validating projection rebuilds, and release evidence showing the current projection lag and coverage.

**Current Domain Evidence Used:** `monitoring_alert`, `suspicious_activity_case`, `IdentityKycAmlComplianceWorkbench`, `identity_kyc_aml_compliance_event_sourced_operational_history`, `OperationalKpiChanged`

### 34. Inbound policy, audit, and KPI boundary

**Key:** `identity_kyc_aml_compliance_inbound_policy_audit_and_kpi_boundary`

**Justification:** This package should consume policy, audit, and KPI signals through declared event boundaries only, not hidden foreign-table dependencies.

**Improvement:** Harden inbound handlers so policy changes, sealed audit events, and KPI changes enter through `appgen_x_outbox_inbox_eventing`, update local projections, and create local review tasks or alerts without crossing the owned boundary.

**Acceptance evidence:** Boundary tests failing on direct foreign-table access, inbox reprocessing tests for repeated events, and release evidence documenting each consumed event contract and handler side effect.

**Current Domain Evidence Used:** `PolicyChanged`, `AuditEventSealed`, `OperationalKpiChanged`, `appgen_x_outbox_inbox_eventing`, `idempotent_handlers`, `retry_dead_letter_evidence`

### 35. Dead-letter recovery console

**Key:** `identity_kyc_aml_compliance_dead_letter_recovery_console`

**Justification:** Failed inbound handlers can silently stop rescreening, alert creation, or control updates unless operations have a recovery surface tied to the KYC domain.

**Improvement:** Add a recovery console for dead-lettered KYC or AML events with root-cause tagging, replay safety, related profile or case context, and post-replay verification of local projections.

**Acceptance evidence:** Replay tests for failed policy and KPI events, workbench visibility into pending dead letters, and release evidence listing unresolved dead-letter items before package approval.

**Current Domain Evidence Used:** `retry_dead_letter_evidence`, `IdentityKycAmlComplianceWorkbench`, `IdentityKycAmlComplianceAssistantPanel`, `PolicyChanged`, `OperationalKpiChanged`

### 36. Rule simulation and impact preview

**Key:** `identity_kyc_aml_compliance_rule_simulation_and_impact_preview`

**Justification:** Screening thresholds, EDD triggers, and risk-score factors change often; operations need to see how many profiles, alerts, and cases a rule change would affect before activation.

**Improvement:** Use `identity_kyc_aml_compliance_counterfactual_scenario_simulation` to preview policy-rule changes against existing `kyc_profile`, `screening_hit`, and `monitoring_alert` records, including projected backlog and approval effects.

**Acceptance evidence:** Policy simulations with before and after counts, configuration workbench diff views, and release evidence requiring approved previews for high-impact rule changes.

**Current Domain Evidence Used:** `identity_kyc_aml_compliance_policy_rule`, `identity_kyc_aml_compliance_counterfactual_scenario_simulation`, `kyc_profile`, `screening_hit`, `monitoring_alert`, `configuration_workbench`

### 37. Runtime parameter guardrails

**Key:** `identity_kyc_aml_compliance_runtime_parameter_guardrails`

**Justification:** Alert thresholds, risk-score bands, and screening match tolerances are operationally sensitive; unsafe parameter edits can flood queues or suppress real risk.

**Improvement:** Add bounded parameter ranges, approval requirements, simulation-before-activation, and rollback metadata for `identity_kyc_aml_compliance_runtime_parameter` so operators can tune the system without creating unbounded effects.

**Acceptance evidence:** Parameter validation tests for unsafe edits, approval-chain evidence for high-impact changes, and workbench views showing the active and prior parameter set with rollback options.

**Current Domain Evidence Used:** `identity_kyc_aml_compliance_runtime_parameter`, `configuration_workbench`, `identity_kyc_aml_compliance_counterfactual_scenario_simulation`, `IdentityKycAmlComplianceApproved`, `IdentityKycAmlComplianceWorkbench`

### 38. Continuous control assertions

**Key:** `identity_kyc_aml_compliance_continuous_control_assertions`

**Justification:** KYC and AML controls should continuously test for overdue rescreens, unresolved sanctions hits, missing EDD evidence, stale monitoring queues, and broken approval chains.

**Improvement:** Expand `identity_kyc_aml_compliance_control_assertion` into a reusable control library that evaluates onboarding completeness, screening closure, monitoring aging, case segregation of duties, and release readiness.

**Acceptance evidence:** Scheduled control runs with failing and passing examples, workbench surfacing of active control failures, and release evidence blocking shipment when critical compliance controls are red.

**Current Domain Evidence Used:** `identity_kyc_aml_compliance_control_assertion`, `identity_kyc_aml_compliance_continuous_control_testing`, `IdentityKycAmlComplianceWorkbench`, `continuous_release_assurance`, `RELEASE_EVIDENCE.md`

### 39. Cryptographic audit proofs

**Key:** `identity_kyc_aml_compliance_cryptographic_audit_proofs`

**Justification:** Sensitive KYC and AML actions need tamper-evident proof for documents, screening decisions, monitoring alerts, and suspicious activity case handling.

**Improvement:** Apply `identity_kyc_aml_compliance_cryptographic_audit_proofs` to high-impact mutations so the package can verify the integrity of identity, screening, and case evidence without exposing the full underlying payload.

**Acceptance evidence:** Proof verification flows for sample approvals and case updates, release evidence showing proof generation for regulated actions, and control failures when proof coverage is missing from required action types.

**Current Domain Evidence Used:** `identity_kyc_aml_compliance_cryptographic_audit_proofs`, `identity_document`, `screening_hit`, `monitoring_alert`, `suspicious_activity_case`, `RELEASE_EVIDENCE.md`

### 40. Release evidence pack

**Key:** `identity_kyc_aml_compliance_release_evidence_pack`

**Justification:** A compliance package needs a release pack that proves policy versions, event contracts, control status, dead-letter health, and UI coverage at release time.

**Improvement:** Extend `RELEASE_EVIDENCE.md` so every release records active policy and parameter versions, event schema compatibility, control status, unresolved alerts or cases, and screenshots or route checks for the analyst surfaces.

**Acceptance evidence:** A complete release packet with policy, control, queue, and event evidence, automated failure when mandatory release sections are missing, and signoff linkage to `continuous_release_assurance`.

**Current Domain Evidence Used:** `RELEASE_EVIDENCE.md`, `continuous_release_assurance`, `identity_kyc_aml_compliance_policy_rule`, `identity_kyc_aml_compliance_runtime_parameter`, `identity_kyc_aml_compliance_control_assertion`

### 41. Analyst queue workbench

**Key:** `identity_kyc_aml_compliance_analyst_queue_workbench`

**Justification:** KYC and AML analysts need prioritized queues for onboarding reviews, screening hits, overdue rescreens, and monitoring alerts instead of a generic single list.

**Improvement:** Expand `IdentityKycAmlComplianceWorkbench` into role-specific queue views for new profiles, unresolved screening hits, EDD-required reviews, overdue periodic reviews, and high-severity alerts.

**Acceptance evidence:** Role-specific queue screenshots or route tests, sorting and filtering evidence by severity and SLA, and release evidence proving each queue surface is shipped and permission-aware.

**Current Domain Evidence Used:** `IdentityKycAmlComplianceWorkbench`, `kyc_profile`, `screening_hit`, `monitoring_alert`, `identity_kyc_aml_compliance_workbench_metric`, `RELEASE_EVIDENCE.md`

### 42. Profile detail decision workspace

**Key:** `identity_kyc_aml_compliance_profile_detail_decision_workspace`

**Justification:** Profile decisions require one place to review identity documents, ownership, screening, risk score, controls, and review notes before approval.

**Improvement:** Turn `IdentityKycAmlComplianceDetail` into a decision workspace that assembles `kyc_profile`, `identity_document`, `beneficial_owner`, `screening_hit`, and `compliance_review` evidence with approval and escalation actions.

**Acceptance evidence:** Detail route tests showing all core evidence on one page, approval-button gating when required panels are incomplete, and release evidence proving the detail workspace reflects the current decision checklist.

**Current Domain Evidence Used:** `IdentityKycAmlComplianceDetail`, `kyc_profile`, `identity_document`, `beneficial_owner`, `screening_hit`, `compliance_review`

### 43. Monitoring operations workbench

**Key:** `identity_kyc_aml_compliance_monitoring_operations_workbench`

**Justification:** Ongoing AML monitoring teams need a separate operational view centered on alerts, typologies, SLA breaches, and escalation health.

**Improvement:** Add a monitoring-operations surface within `IdentityKycAmlComplianceWorkbench` focused on `monitoring_alert` severity, typology, aging, analyst load, and alert-to-case conversion rates.

**Acceptance evidence:** Monitoring dashboards with aging buckets and conversion funnels, queue tests for high-severity filtering, and release evidence covering the shipped monitoring operations surface.

**Current Domain Evidence Used:** `IdentityKycAmlComplianceWorkbench`, `monitoring_alert`, `identity_kyc_aml_compliance_workbench_metric`, `OperationalKpiChanged`, `RELEASE_EVIDENCE.md`

### 44. Suspicious activity case workbench

**Key:** `identity_kyc_aml_compliance_suspicious_activity_case_workbench`

**Justification:** Suspicious activity cases are a specialized workflow that needs case-state, filing-decision, and evidence-centric tooling beyond generic profile detail pages.

**Improvement:** Add a case-management surface for `suspicious_activity_case` with investigation timeline, linked alerts, filing decision status, restricted narrative access, and case aging metrics.

**Acceptance evidence:** Case-route coverage in the UI, state and aging filters for open investigations, and release evidence proving the case workbench respects restricted-access boundaries.

**Current Domain Evidence Used:** `suspicious_activity_case`, `IdentityKycAmlComplianceWorkbench`, `IdentityKycAmlComplianceDetail`, `permissions`, `RELEASE_EVIDENCE.md`

### 45. Document intake agent skill

**Key:** `identity_kyc_aml_compliance_document_intake_agent_skill`

**Justification:** Analysts spend time transcribing documents and checking completeness; the assistant should help prepare evidence without writing directly to governed data stores.

**Improvement:** Add a governed document-intake skill in `IdentityKycAmlComplianceAssistantPanel` that uses `agentic_document_instruction_intake` and `identity_kyc_aml_compliance_semantic_document_instruction_understanding` to draft document metadata and missing-field prompts.

**Acceptance evidence:** Assistant previews that show extracted fields before submission, permission tests proving no automatic mutation occurs without operator confirmation, and release evidence listing the document-intake skill and its guardrails.

**Current Domain Evidence Used:** `IdentityKycAmlComplianceAssistantPanel`, `agentic_document_instruction_intake`, `identity_kyc_aml_compliance_semantic_document_instruction_understanding`, `ai_agent_task_assistance`, `identity_document`

### 46. Screening triage agent skill

**Key:** `identity_kyc_aml_compliance_screening_triage_agent_skill`

**Justification:** Screening triage is repetitive but high-risk; the assistant should summarize matches, aliases, and prior decisions without being able to clear a hit by itself.

**Improvement:** Add a triage skill that prepares `screening_hit` summaries, compares current and prior match evidence, and drafts analyst notes while requiring human confirmation for any disposition change.

**Acceptance evidence:** Assistant-generated screening summaries linked from the workbench, tests proving the assistant cannot resolve a hit without an authorized reviewer, and release evidence documenting the skill's allowed and blocked actions.

**Current Domain Evidence Used:** `IdentityKycAmlComplianceAssistantPanel`, `screening_hit`, `ai_agent_task_assistance`, `permissions`, `IdentityKycAmlComplianceExceptionOpened`

### 47. Case-summary agent skill

**Key:** `identity_kyc_aml_compliance_case_summary_agent_skill`

**Justification:** Suspicious activity investigations need concise case summaries, but narrative preparation must stay within governed boundaries and restricted-access rules.

**Improvement:** Add a case-summary skill that compiles alert lineage, profile context, ownership complexity, screening history, and review notes into a draft case brief for `suspicious_activity_case` without auto-filing or disclosing restricted narrative text.

**Acceptance evidence:** Draft case briefs visible in `IdentityKycAmlComplianceAssistantPanel`, blocked-action tests for filing or closure attempts, and release evidence proving case-summary outputs remain review artifacts until approved.

**Current Domain Evidence Used:** `IdentityKycAmlComplianceAssistantPanel`, `suspicious_activity_case`, `monitoring_alert`, `screening_hit`, `ai_agent_task_assistance`, `identity_kyc_aml_compliance_governed_ai_agent_execution`

### 48. Governed model drift and feedback loop

**Key:** `identity_kyc_aml_compliance_governed_model_drift_and_feedback_loop`

**Justification:** Screening and risk models can drift, raising false positives or missing emerging risk patterns unless analyst feedback is captured and evaluated.

**Improvement:** Use `identity_kyc_aml_compliance_governed_model` to track model version, drift indicators, analyst feedback, false positive rates, and retraining or rollback decisions for predictive risk and anomaly features.

**Acceptance evidence:** Model-governance views showing version and drift status, feedback-linked tests for rollback triggers, and release evidence recording the active governed-model versions used in production.

**Current Domain Evidence Used:** `identity_kyc_aml_compliance_governed_model`, `identity_kyc_aml_compliance_predictive_risk_scoring`, `identity_kyc_aml_compliance_autonomous_anomaly_detection`, `compliance_review`, `RELEASE_EVIDENCE.md`

### 49. Multi-tenant policy isolation and residency

**Key:** `identity_kyc_aml_compliance_multi_tenant_policy_isolation_and_residency`

**Justification:** Compliance platforms serving multiple tenants need strict isolation for policy rules, runtime parameters, customer data, and jurisdiction-specific evidence.

**Improvement:** Apply `identity_kyc_aml_compliance_multi_tenant_policy_isolation` so tenant policy sets, screening rules, runtime parameters, and profile data remain isolated, residency-aware, and separately auditable.

**Acceptance evidence:** Cross-tenant negative tests for queue access and policy leakage, tenant-scoped configuration views, and release evidence showing isolation checks passed for data, policy, and assistant actions.

**Current Domain Evidence Used:** `identity_kyc_aml_compliance_multi_tenant_policy_isolation`, `identity_kyc_aml_compliance_policy_rule`, `identity_kyc_aml_compliance_runtime_parameter`, `kyc_profile`, `permissions`, `RELEASE_EVIDENCE.md`

### 50. End-to-end KYC and AML control test

**Key:** `identity_kyc_aml_compliance_end_to_end_kyc_and_aml_control_test`

**Justification:** The package should prove that a realistic onboarding flow can move from profile creation through document verification, ownership capture, screening, risk scoring, monitoring, and case promotion with evidence at each step.

**Improvement:** Add a release-gated control test that runs a representative individual and entity scenario through `POST /kyc-profiles`, `POST /identity-documents`, `POST /beneficial-owners`, `POST /screening-hits`, `POST /monitoring-alerts`, the workbench surfaces, and the final approval or exception path.

**Acceptance evidence:** Reproducible end-to-end control packs with emitted event traces, screenshots or route checks for `IdentityKycAmlComplianceWorkbench` and `IdentityKycAmlComplianceDetail`, and a final signoff entry in `RELEASE_EVIDENCE.md`.

**Current Domain Evidence Used:** `POST /kyc-profiles`, `POST /identity-documents`, `POST /beneficial-owners`, `POST /screening-hits`, `POST /monitoring-alerts`, `IdentityKycAmlComplianceWorkbench`, `IdentityKycAmlComplianceDetail`, `RELEASE_EVIDENCE.md`
