from .account_control import ACCOUNT_CONTROL_CAPABILITIES, improve1_account_control_contract
from .runtime import (
    BANKING_CORE_ACCOUNTS_CONTROLS,
    BANKING_CORE_ACCOUNTS_FORMS,
    BANKING_CORE_ACCOUNTS_WIZARDS,
    banking_core_accounts_build_app_surface,
    banking_core_accounts_build_control_surface,
    banking_core_accounts_build_workbench_view,
    banking_core_accounts_build_workflow_surface,
)

PBC_KEY = "banking_core_accounts"


def banking_core_accounts_ui_contract():
    app_surface = banking_core_accounts_build_app_surface()
    control_surface = banking_core_accounts_build_control_surface()
    workflow_surface = banking_core_accounts_build_workflow_surface()
    return {
        "ok": True,
        "pbc": PBC_KEY,
        "fragments": (
            "BankingCoreAccountsWorkbench",
            "BankingCoreAccountsDetail",
            "BankingCoreAccountsAssistantPanel",
        ),
        "configuration_editor": True,
        "stream_engine_picker_visible": False,
        "action_permissions": (
            "banking_core_accounts.read",
            "banking_core_accounts.create",
            "banking_core_accounts.update",
            "banking_core_accounts.approve",
            "banking_core_accounts.admin",
        ),
        "forms": BANKING_CORE_ACCOUNTS_FORMS,
        "wizards": BANKING_CORE_ACCOUNTS_WIZARDS,
        "controls": BANKING_CORE_ACCOUNTS_CONTROLS,
        "full_capability_surface": {
            "operation_actions": ("open_deposit_account", "transition_deposit_account"),
            "rule_editors": ("deposit_account_policy",),
            "parameter_editors": ("workbench_limit", "approval_sla_hours"),
            "advanced_panels": ("lifecycle_state_machine", "control_assertions") + ACCOUNT_CONTROL_CAPABILITIES,
            "account_control_panels": tuple(f"account_control_{capability}" for capability in ACCOUNT_CONTROL_CAPABILITIES),
            "account_control_contract": improve1_account_control_contract(),
            "table_browsers": app_surface["tables"],
            "workflow_ids": tuple(item["workflow_id"] for item in workflow_surface["workflows"]),
            "edge_case_queues": ("maker_checker_failures", "invalid_transition_attempts"),
            "navigation_sections": (
                "overview",
                "forms",
                "wizards",
                "controls",
                "workflows",
                "workbench",
                "release_evidence",
            ),
            "coverage": {
                "event_contract": "AppGen-X",
                "stream_engine_picker_visible": False,
                "shared_table_access": False,
                "single_pbc_app": True,
            },
        },
        "control_surface": control_surface,
        "workflow_surface": workflow_surface,
        "side_effects": (),
    }


def banking_core_accounts_render_workbench(state=None, tenant="default"):
    return banking_core_accounts_build_workbench_view(state=state, tenant=tenant)


def smoke_test():
    contract = banking_core_accounts_ui_contract()
    workbench = banking_core_accounts_render_workbench()
    return {
        "ok": contract["ok"]
        and workbench["ok"]
        and contract["full_capability_surface"]["coverage"]["single_pbc_app"],
        "side_effects": (),
    }
