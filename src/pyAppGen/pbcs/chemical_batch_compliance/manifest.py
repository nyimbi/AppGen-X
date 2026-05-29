"""Package manifest for the chemical_batch_compliance PBC."""

# Audit trace key: 'chemical_batch_compliance'

from .slice_app import COMMAND_METHODS
from .slice_app import CONSUMED_EVENT_TYPES
from .slice_app import EMITTED_EVENT_TYPES
from .slice_app import PBC_KEY
from .slice_app import ROUTES
from .slice_app import RUNTIME_CAPABILITY_KEYS
from .slice_app import STANDARD_FEATURE_KEYS
from .slice_app import UI_FRAGMENT_KEYS

PBC_MANIFEST = {
    "pbc": PBC_KEY,
    "label": "Chemical Batch Compliance",
    "mesh": "opsmfg",
    "description": (
        "Controlled formula revisions, batch execution evidence, SDS and hazardous material "
        "qualification, quality holds, regulatory dossiers, and governed document instructions."
    ),
    "datastore_backend": "postgresql",
    "template": "asset",
    "version": "1.1.0",
    "tables": (
        "chemical_formula",
        "batch_record",
        "sds_document",
        "hazardous_material",
        "regulatory_submission",
        "quality_test",
        "compliance_hold",
        "chemical_batch_compliance_policy_rule",
        "chemical_batch_compliance_runtime_parameter",
        "chemical_batch_compliance_schema_extension",
        "chemical_batch_compliance_control_assertion",
        "chemical_batch_compliance_governed_model",
    ),
    "apis": ROUTES,
    "emits": EMITTED_EVENT_TYPES,
    "consumes": CONSUMED_EVENT_TYPES,
    "permissions": (
        "chemical_batch_compliance.read",
        "chemical_batch_compliance.create",
        "chemical_batch_compliance.update",
        "chemical_batch_compliance.approve",
        "chemical_batch_compliance.admin",
    ),
    "configuration": (
        "CHEMICAL_BATCH_COMPLIANCE_DATABASE_URL",
        "CHEMICAL_BATCH_COMPLIANCE_EVENT_TOPIC",
        "CHEMICAL_BATCH_COMPLIANCE_RETRY_LIMIT",
        "CHEMICAL_BATCH_COMPLIANCE_DEFAULT_POLICY",
    ),
    "migrations": ("migrations/001_initial.sql",),
    "seed_data": ("seed_data.py",),
    "tests": ("tests/test_contract.py", "tests/test_slice_app.py", "tests/test_standalone_app.py"),
    "docs": ("SPECIFICATION.md", "RELEASE_EVIDENCE.md"),
    "ui_fragments": UI_FRAGMENT_KEYS,
    "standard_features": STANDARD_FEATURE_KEYS,
    "advanced_capabilities": RUNTIME_CAPABILITY_KEYS,
    "capabilities": STANDARD_FEATURE_KEYS + RUNTIME_CAPABILITY_KEYS,
    "workflows": (
        "chemical_batch_compliance_formula_release_workflow",
        "chemical_batch_compliance_batch_review_workflow",
        "chemical_batch_compliance_document_instruction_workflow",
    ),
    "analytics": ("chemical_batch_compliance_risk_score", "chemical_batch_compliance_workbench_metric"),
}
