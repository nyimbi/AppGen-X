"""Workbench, forms, wizards, and controls for the healthcare claims adjudication slice."""

from __future__ import annotations

from typing import Any

from .config import PARAMETERS
from .config import PERMISSIONS
from .config import RULES
from .domain_depth import DOMAIN_ADVANCED_CAPABILITIES
from .domain_depth import DOMAIN_EDGE_CASES
from .domain_depth import DOMAIN_OPERATIONS
from .models import BUSINESS_TABLES
from .models import PBC_KEY
from .runtime import CLAIMS_ADJUDICATION_HEALTHCARE_UI_FRAGMENT_KEYS
from .runtime import claims_adjudication_healthcare_build_workbench_view

FORMS = (
    {
        "name": "claim_intake_form",
        "entity": "health_claim",
        "fields": ("claim_number", "claim_type", "source_format", "member_id", "provider_id", "plan_id", "received_date"),
    },
    {
        "name": "claim_line_form",
        "entity": "claim_line",
        "fields": ("claim_id", "line_number", "service_date", "procedure_code", "diagnosis_code", "units", "charge_amount"),
    },
    {
        "name": "denial_form",
        "entity": "denial",
        "fields": ("claim_id", "line_ids", "denial_code", "rationale", "policy_rule_id", "notice_deadline"),
    },
    {
        "name": "appeal_form",
        "entity": "appeal",
        "fields": ("denial_id", "level", "requester", "evidence_summary", "determination"),
    },
)

WIZARDS = (
    {
        "name": "claim_intake_wizard",
        "steps": ("normalize intake", "validate projections", "create claim", "route to queue"),
    },
    {
        "name": "duplicate_review_wizard",
        "steps": ("compare canonical identity", "assess correction lineage", "pend or continue"),
    },
    {
        "name": "appeal_packet_wizard",
        "steps": ("capture denial", "attach evidence", "assign reviewer", "record determination"),
    },
)

CONTROLS = (
    {"name": "pend_queue", "purpose": "Resolve stale projections and missing evidence."},
    {"name": "denial_reason_matrix", "purpose": "Author precise denial rationale by policy rule."},
    {"name": "payment_integrity_triage", "purpose": "Review high-dollar or suspicious claims."},
    {"name": "document_instruction_console", "purpose": "Preview governed CRUD from assistant instructions."},
)


def claims_adjudication_healthcare_ui_contract() -> dict[str, Any]:
    return {
        "ok": True,
        "pbc": PBC_KEY,
        "fragments": CLAIMS_ADJUDICATION_HEALTHCARE_UI_FRAGMENT_KEYS,
        "configuration_editor": True,
        "stream_engine_picker_visible": False,
        "action_permissions": PERMISSIONS,
        "forms": FORMS,
        "wizards": WIZARDS,
        "controls": CONTROLS,
        "full_capability_surface": {
            "operation_actions": DOMAIN_OPERATIONS,
            "rule_editors": RULES,
            "parameter_editors": PARAMETERS,
            "advanced_panels": DOMAIN_ADVANCED_CAPABILITIES,
            "table_browsers": BUSINESS_TABLES,
            "edge_case_queues": DOMAIN_EDGE_CASES,
            "agent_tools": tuple(f"{PBC_KEY}_skills.{op}" for op in DOMAIN_OPERATIONS),
            "navigation_sections": (
                "overview",
                "intake",
                "line_adjudication",
                "coding_and_denials",
                "appeals",
                "payment_integrity",
                "configuration",
                "release_evidence",
            ),
            "coverage": {"event_contract": "AppGen-X", "shared_table_access": False},
        },
        "side_effects": (),
    }


def claims_adjudication_healthcare_render_workbench(tenant: str = "default") -> dict[str, Any]:
    view = claims_adjudication_healthcare_build_workbench_view(tenant=tenant)
    return {
        "ok": True,
        "pbc": PBC_KEY,
        "route": view["route"],
        "operation_actions": view["actions"],
        "table_browsers": view["tables"],
        "forms": FORMS,
        "wizards": WIZARDS,
        "controls": CONTROLS,
        "side_effects": (),
    }


def smoke_test() -> dict[str, Any]:
    return {
        "ok": claims_adjudication_healthcare_ui_contract()["ok"] and claims_adjudication_healthcare_render_workbench()["ok"],
        "side_effects": (),
    }
