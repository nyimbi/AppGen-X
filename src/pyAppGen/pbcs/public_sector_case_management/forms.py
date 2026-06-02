"""Professional form contracts for the Public Sector Case Management PBC."""
from __future__ import annotations

PBC_KEY = "public_sector_case_management"


def form_catalog() -> dict:
    forms = (
        {"id": "intake_envelope", "owned_table": "public_sector_case_management_citizen_case", "fields": ("channel", "worker", "submitted_at", "language", "program_requested", "urgency", "contactability", "rejection_reason"), "validations": ("channel captured", "contactability status", "explicit rejection reason")},
        {"id": "party_household_representation", "owned_table": "public_sector_case_management_citizen_case", "fields": ("applicant", "household_members", "caregivers", "guardians", "interpreters", "authorized_representatives", "effective_dates", "verification_status"), "validations": ("role dates", "authority verified", "household recalculation trigger")},
        {"id": "jurisdiction_and_address", "owned_table": "public_sector_case_management_citizen_case", "fields": ("residential_address", "mailing_address", "temporary_shelter", "confidential_address", "service_district", "office", "hearing_venue"), "validations": ("jurisdiction derived", "confidential display suppressed")},
        {"id": "program_screening", "owned_table": "public_sector_case_management_eligibility_determination", "fields": ("needs", "candidate_programs", "confidence", "missing_prerequisites", "incompatibilities", "referral_only_services"), "validations": ("reasoned recommendation", "rerunnable screening")},
        {"id": "evidence_intake_and_sufficiency", "owned_table": "public_sector_case_management_eligibility_determination", "fields": ("document_class", "asserted_facts", "confidence", "page_count", "linked_question", "sufficiency", "contradictions", "smallest_missing_proof"), "validations": ("chain of custody", "low-confidence review", "contradiction exception")},
        {"id": "eligibility_period", "owned_table": "public_sector_case_management_eligibility_determination", "fields": ("application_date", "incident_date", "verification_date", "effective_start", "retroactive_start", "end_date", "recertification_date", "adverse_action_lead_time"), "validations": ("date rule trace", "notice date basis")},
        {"id": "benefit_service_package", "owned_table": "public_sector_case_management_benefit_decision", "fields": ("amount", "frequency", "duration", "conditions", "service_obligations", "partial_approval", "fact_snapshot"), "validations": ("package consistency", "partial approval constrained")},
        {"id": "notice_correspondence", "owned_table": "public_sector_case_management_notice", "fields": ("notice_type", "template_language", "delivery_channel", "fact_snapshot", "rule_citations", "appeal_rights", "barcode", "response_due"), "validations": ("timely notice", "citation reuse", "delivery channel")},
        {"id": "referral_and_outcome", "owned_table": "public_sector_case_management_service_outcome", "fields": ("referral_reason", "service", "urgency", "organization", "expected_response", "accepted", "first_contact", "no_show", "completed", "closure_code"), "validations": ("allowed evidence package", "loop closure")},
        {"id": "appeal_hearing", "owned_table": "public_sector_case_management_appeal", "fields": ("standing", "filing_date", "appealed_action", "requested_remedy", "continuation_of_benefits", "issue_statement", "hearing_venue", "interpreter", "packet_status", "outcome"), "validations": ("timeliness", "scope control", "hearing logistics")},
        {"id": "privacy_and_access", "owned_table": "public_sector_case_management_public_sector_case_management_control_assertion", "fields": ("declared_purpose", "field_access", "confidentiality_markers", "audience", "redaction_level", "export_reason", "override"), "validations": ("purpose-based access", "least privilege", "protected population handling")},
        {"id": "sla_override_fraud_handoff", "owned_table": "public_sector_case_management_service_outcome", "fields": ("sla_clock", "pause_reason", "resume_trigger", "override_type", "approver", "expiry", "fraud_reason_code", "approved_evidence_excerpt"), "validations": ("clock tolling", "override governance", "fraud boundary")},
    )
    return {"ok": True, "pbc": PBC_KEY, "forms": forms, "side_effects": ()}


def form_for(form_id: str) -> dict:
    for form in form_catalog()["forms"]:
        if form["id"] == form_id:
            return {"ok": True, "form": form, "side_effects": ()}
    return {"ok": False, "reason": "unknown_form", "side_effects": ()}


def smoke_test() -> dict:
    return {"ok": len(form_catalog()["forms"]) >= 12 and form_for("appeal_hearing")["ok"], "side_effects": ()}
