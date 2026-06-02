from __future__ import annotations

from .permissions import permission_manifest
from .standalone import build_standalone_app, build_ui_contract, standalone_application_manifest


def public_safety_dispatch_ui_contract() -> dict:
    ui = build_ui_contract()
    permissions = permission_manifest()
    return {
        **ui,
        "configuration_editor": True,
        "stream_engine_picker_visible": False,
        "action_permissions": permissions["action_permissions"],
    }


def public_safety_dispatch_render_workbench(tenant: str = "tenant_alpha") -> dict:
    app = build_standalone_app()
    app.load_demo_workspace(tenant)
    return app.build_workbench_view(tenant)


def public_safety_dispatch_standalone_app_contract() -> dict:
    return standalone_application_manifest()


def public_safety_dispatch_render_standalone_app(tenant: str = "tenant_alpha") -> dict:
    return public_safety_dispatch_render_workbench(tenant)


def smoke_test() -> dict:
    workbench = public_safety_dispatch_render_workbench()
    return {"ok": public_safety_dispatch_ui_contract()["ok"] and public_safety_dispatch_standalone_app_contract()["ok"] and workbench["ok"], "workbench": workbench, "side_effects": ()}

# Improve1 public safety dispatch control UI extension.
from .public_safety_dispatch_control import improve1_public_safety_dispatch_control_contract as _improve1_public_safety_dispatch_control_contract

_PUBLIC_SAFETY_DISPATCH_CONTROL_BASE_UI_CONTRACT = public_safety_dispatch_ui_contract
_PUBLIC_SAFETY_DISPATCH_CONTROL_BASE_RENDER_WORKBENCH = public_safety_dispatch_render_workbench


def public_safety_dispatch_ui_contract() -> dict:
    ui = dict(_PUBLIC_SAFETY_DISPATCH_CONTROL_BASE_UI_CONTRACT())
    control = _improve1_public_safety_dispatch_control_contract()
    ui.update({
        "ok": ui.get("ok") is True and control["ok"],
        "public_safety_dispatch_control_contract": control,
        "public_safety_dispatch_control_panels": tuple(item["evidence"]["ui_surface"] for item in control["capabilities"]),
        "public_safety_dispatch_control_service_actions": tuple(item["evidence"]["service_api"] for item in control["capabilities"]),
        "stream_engine_picker_visible": False,
    })
    return ui


def public_safety_dispatch_render_workbench(*args, **kwargs) -> dict:
    workbench = dict(_PUBLIC_SAFETY_DISPATCH_CONTROL_BASE_RENDER_WORKBENCH(*args, **kwargs))
    control = _improve1_public_safety_dispatch_control_contract()
    workbench.update({
        "ok": workbench.get("ok") is True and control["ok"],
        "public_safety_dispatch_control_panels": tuple(item["evidence"]["ui_surface"] for item in control["capabilities"]),
        "public_safety_dispatch_control_service_actions": tuple(item["evidence"]["service_api"] for item in control["capabilities"]),
        "public_safety_dispatch_control_agent_tools": tuple(f"public_safety_dispatch.skills.{item['slug']}" for item in control["capabilities"]),
    })
    return workbench
