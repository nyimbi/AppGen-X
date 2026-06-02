"""UI fragments for the student_financial_aid PBC."""
from __future__ import annotations

from .slice_app import BUSINESS_TABLES, DOMAIN_OPERATIONS, PARAMETER_KEYS, RULE_KEYS, build_standalone_app, build_ui_contract

PBC_KEY = 'student_financial_aid'
UI_FRAGMENTS = tuple(build_ui_contract()['fragments'])


def student_financial_aid_ui_contract() -> dict:
    contract = build_ui_contract()
    return {
        **contract,
        'configuration_editor': True,
        'stream_engine_picker_visible': False,
        'full_capability_surface': {
            'operation_actions': tuple(DOMAIN_OPERATIONS),
            'rule_editors': tuple(RULE_KEYS),
            'parameter_editors': tuple(PARAMETER_KEYS),
            'advanced_panels': tuple(contract['advanced_panels']),
            'edge_case_queues': (
                'verification_overdue',
                'sap_suspension',
                'overaward_detected',
                'return_of_funds_required',
                'appeal_pending_committee',
                'idempotency_replay',
            ),
            'table_browsers': tuple(BUSINESS_TABLES),
            'navigation_sections': (
                'aid_year_setup',
                'intake_and_verification',
                'need_and_packaging',
                'disbursement_and_returns',
                'appeals_and_compliance',
                'agent_assistant',
                'release_evidence',
            ),
        },
        'operation_actions': tuple(DOMAIN_OPERATIONS),
        'rule_editors': tuple(RULE_KEYS),
        'parameter_editors': tuple(PARAMETER_KEYS),
        'edge_case_queues': (
            'verification_overdue',
            'sap_suspension',
            'overaward_detected',
            'return_of_funds_required',
            'appeal_pending_committee',
            'idempotency_replay',
        ),
        'table_browsers': tuple(BUSINESS_TABLES),
        'navigation_sections': (
            'aid_year_setup',
            'intake_and_verification',
            'need_and_packaging',
            'disbursement_and_returns',
            'appeals_and_compliance',
            'agent_assistant',
            'release_evidence',
        ),
    }


def student_financial_aid_render_workbench(state: dict | None = None) -> dict:
    tenant = (state or {}).get('tenant', 'default')
    workbench = build_standalone_app().build_workbench_view(tenant=tenant)
    return {
        'ok': workbench['ok'],
        'pbc': PBC_KEY,
        'view': workbench['view'],
        'panels': workbench['panels'],
        'forms': workbench['forms'],
        'wizards': workbench['wizards'],
        'controls': workbench['controls'],
        'summary': workbench['summary'],
        'configuration_editor': True,
        'stream_engine_picker_visible': False,
        'action_permissions': tuple(student_financial_aid_ui_contract()['action_permissions']),
        'advanced_panels': tuple(student_financial_aid_ui_contract()['advanced_panels']),
        'agent_tools': (
            'student_financial_aid_plan_document_changes',
            'student_financial_aid_preview_mutation',
            'student_financial_aid_explain_need_analysis',
        ),
        'side_effects': (),
    }


def smoke_test() -> dict:
    contract = student_financial_aid_ui_contract()
    workbench = student_financial_aid_render_workbench({'tenant': 'tenant-smoke'})
    return {
        'ok': contract['ok'] and workbench['ok'] and bool(workbench['forms']) and bool(workbench['wizards']) and bool(workbench['controls']),
        'contract': contract,
        'workbench': workbench,
        'side_effects': (),
    }

# Improve1 student financial aid control UI extension.
from .student_financial_aid_control import improve1_student_financial_aid_control_contract as _improve1_student_financial_aid_control_contract

_AID_CONTROL_BASE_UI_CONTRACT = student_financial_aid_ui_contract
_AID_CONTROL_BASE_RENDER_WORKBENCH = student_financial_aid_render_workbench


def student_financial_aid_ui_contract() -> dict:
    ui = dict(_AID_CONTROL_BASE_UI_CONTRACT())
    control = _improve1_student_financial_aid_control_contract()
    ui.update({
        "ok": ui.get("ok") is True and control["ok"],
        "student_financial_aid_control_contract": control,
        "student_financial_aid_control_panels": tuple(item["evidence"]["ui_surface"] for item in control["capabilities"]),
        "student_financial_aid_control_service_actions": tuple(item["evidence"]["service_api"] for item in control["capabilities"]),
        "stream_engine_picker_visible": False,
    })
    return ui


def student_financial_aid_render_workbench(*args, **kwargs) -> dict:
    workbench = dict(_AID_CONTROL_BASE_RENDER_WORKBENCH(*args, **kwargs))
    control = _improve1_student_financial_aid_control_contract()
    workbench.update({
        "ok": workbench.get("ok") is True and control["ok"],
        "student_financial_aid_control_panels": tuple(item["evidence"]["ui_surface"] for item in control["capabilities"]),
        "student_financial_aid_control_service_actions": tuple(item["evidence"]["service_api"] for item in control["capabilities"]),
        "student_financial_aid_control_agent_tools": tuple(f"student_financial_aid.skills.{item['slug']}" for item in control["capabilities"]),
    })
    return workbench
