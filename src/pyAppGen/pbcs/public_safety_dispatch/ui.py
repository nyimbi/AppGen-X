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
