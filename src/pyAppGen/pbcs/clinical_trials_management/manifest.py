"""Package manifest for the clinical_trials_management PBC."""

# Audit trace key: 'clinical_trials_management'

from .runtime import CLINICAL_TRIALS_MANAGEMENT_CONSUMED_EVENT_TYPES
from .runtime import CLINICAL_TRIALS_MANAGEMENT_EMITTED_EVENT_TYPES
from .runtime import CLINICAL_TRIALS_MANAGEMENT_PERMISSIONS
from .runtime import CLINICAL_TRIALS_MANAGEMENT_RUNTIME_CAPABILITY_KEYS
from .runtime import CLINICAL_TRIALS_MANAGEMENT_STANDARD_FEATURE_KEYS

PBC_MANIFEST = {
    "pbc": "clinical_trials_management",
    "label": "Clinical Trials Management",
    "mesh": "relationship",
    "description": "Protocol governance, site activation, subject enrollment, consent control, visits, safety, monitoring, and lock readiness.",
    "datastore_backend": "postgresql",
    "tables": (
        "trial_protocol",
        "study_site",
        "subject",
        "consent_record",
        "visit_schedule",
        "adverse_event",
        "monitoring_finding",
        "clinical_trials_management_policy_rule",
        "clinical_trials_management_runtime_parameter",
        "clinical_trials_management_schema_extension",
        "clinical_trials_management_control_assertion",
        "clinical_trials_management_governed_model",
    ),
    "apis": (
        "POST /trial-protocols",
        "POST /study-sites",
        "POST /subjects",
        "POST /consent-records",
        "POST /visit-schedules",
        "POST /adverse-events",
        "POST /monitoring-findings",
        "POST /policy-rules",
        "POST /runtime-parameters",
        "GET /clinical-trials-workbench",
        "GET /controls",
        "POST /assistant/document-preview",
    ),
    "emits": CLINICAL_TRIALS_MANAGEMENT_EMITTED_EVENT_TYPES,
    "consumes": CLINICAL_TRIALS_MANAGEMENT_CONSUMED_EVENT_TYPES,
    "template": "workflow",
    "ui_fragments": (
        "ClinicalTrialsOperationsWorkbench",
        "ProtocolAmendmentBoard",
        "SiteActivationBoard",
        "ScreeningQueue",
        "ConsentAndVisitConsole",
        "SafetyReportingConsole",
        "MonitoringFindingsConsole",
        "DataLockReadinessBoard",
        "AssistantPreviewWorkbench",
    ),
    "permissions": CLINICAL_TRIALS_MANAGEMENT_PERMISSIONS,
    "configuration": (
        "CLINICAL_TRIALS_MANAGEMENT_DATABASE_URL",
        "CLINICAL_TRIALS_MANAGEMENT_EVENT_TOPIC",
        "CLINICAL_TRIALS_MANAGEMENT_DEFAULT_TIMEZONE",
        "CLINICAL_TRIALS_MANAGEMENT_DEFAULT_JURISDICTION",
    ),
    "capabilities": CLINICAL_TRIALS_MANAGEMENT_STANDARD_FEATURE_KEYS + CLINICAL_TRIALS_MANAGEMENT_RUNTIME_CAPABILITY_KEYS,
    "standard_features": CLINICAL_TRIALS_MANAGEMENT_STANDARD_FEATURE_KEYS,
    "advanced_capabilities": CLINICAL_TRIALS_MANAGEMENT_RUNTIME_CAPABILITY_KEYS,
    "workflows": (
        "clinical_trials_management_protocol_and_site_startup",
        "clinical_trials_management_subject_enrollment",
        "clinical_trials_management_visit_and_safety_follow_up",
        "clinical_trials_management_data_lock_readiness",
    ),
    "analytics": (
        "site_activation_timeliness",
        "screening_conversion",
        "visit_window_adherence",
        "serious_event_reporting_timeliness",
        "monitoring_findings_backlog",
        "lock_readiness_score",
    ),
    "migrations": ("migrations/001_initial.sql",),
    "seed_data": ("seed_data.py",),
    "tests": ("tests/test_contract.py", "tests/test_standalone_app.py"),
    "docs": (
        "README.md",
        "SPECIFICATION.md",
        "RELEASE_EVIDENCE.md",
        "implementation-plan.md",
        "implementation-status.md",
    ),
    "version": "1.0.0",
}
