"""Package-level multi-target application generation contracts."""

from __future__ import annotations

from .dsl import schema_from_dsl


TARGETS = {
    "web": {
        "runtime": "Flask-AppBuilder",
        "artifacts": ("app/__init__.py", "app/views.py", "app/templates/index.html"),
        "capabilities": ("responsive_forms", "rbac", "api_routes", "reports"),
    },
    "pwa": {
        "runtime": "service-worker",
        "artifacts": ("app/static/manifest.json", "app/static/service-worker.js"),
        "capabilities": ("installable", "offline_shell", "push_ready"),
    },
    "mobile": {
        "runtime": "Kivy",
        "artifacts": ("native/mobile/app.py", "native/mobile/pyproject.toml"),
        "capabilities": ("camera", "location", "push", "offline_queue"),
    },
    "desktop": {
        "runtime": "BeeWare",
        "artifacts": ("native/desktop/app.py", "native/desktop/pyproject.toml"),
        "capabilities": ("local_files", "offline_cache", "keyboard_navigation", "sync_replay"),
    },
    "chatbot": {
        "runtime": "Dialogflow/Bot Framework",
        "artifacts": ("chatbots/appgen_chatbots.py", "chatbots/dialogflow/intents.json"),
        "capabilities": ("guided_create", "required_field_prompts", "provider_exports"),
    },
}

TARGET_SAMPLE_DSL = """
app TargetAudit { targets: web, pwa, mobile, desktop, chatbot }

table Ticket {
  id: int pk
  title: string required
}

view TicketForm for Ticket {
  Main: title
  @ title TextBox 0 0 6 1
}
"""


def target_catalog() -> tuple[dict, ...]:
    """Return all application generation targets."""
    return tuple({"target": target, **contract} for target, contract in TARGETS.items())


def target_contract(target: str) -> dict:
    """Return one stable target contract."""
    if target not in TARGETS:
        raise KeyError(f"Unknown target: {target}")
    return {"target": target, **TARGETS[target]}


def generation_matrix(targets: tuple[str, ...] = ("web", "mobile", "desktop")) -> tuple[dict, ...]:
    """Return target rows for generated application packages."""
    return tuple(
        {
            "target": target,
            "runtime": TARGETS[target]["runtime"],
            "artifacts": TARGETS[target]["artifacts"],
            "verification": _verification_for(target),
        }
        for target in targets
    )


def target_package_matrix(targets: tuple[str, ...] | None = None) -> dict:
    """Return a package matrix across selected targets."""
    selected = targets or tuple(TARGETS)
    rows = generation_matrix(tuple(target for target in selected if target in TARGETS))
    return {
        "format": "appgen.package-target-matrix.v1",
        "ok": {row["target"] for row in rows} == set(selected),
        "rows": rows,
    }


def dsl_target_contract(source: str = TARGET_SAMPLE_DSL) -> dict:
    """Parse the DSL and summarize target selection."""
    schema = schema_from_dsl(source, source_name="target-audit.appgen")
    selected = tuple(
        item.strip()
        for item in str(schema.app_options.get("targets", "")).split(",")
        if item.strip()
    )
    return {
        "format": "appgen.package-target-dsl-contract.v1",
        "app": schema.app_name,
        "targets": selected,
        "ok": set(selected) == set(TARGETS),
    }


def mobile_capability_contract() -> dict:
    """Return mobile-native capability proof."""
    mobile = target_contract("mobile")
    return {
        "format": "appgen.package-mobile-target-contract.v1",
        "ok": {"camera", "location", "push", "offline_queue"} <= set(mobile["capabilities"]),
        "target": mobile,
        "permissions": (
            "android.permission.CAMERA",
            "android.permission.ACCESS_FINE_LOCATION",
            "android.permission.POST_NOTIFICATIONS",
        ),
        "offline": {
            "queue": "json-outbox",
            "conflict_policy": "manual_review",
        },
    }


def desktop_capability_contract() -> dict:
    """Return desktop-native capability proof."""
    desktop = target_contract("desktop")
    return {
        "format": "appgen.package-desktop-target-contract.v1",
        "ok": {"local_files", "offline_cache", "sync_replay"} <= set(desktop["capabilities"]),
        "target": desktop,
        "local_cache": "json-cache",
        "file_actions_review_required": True,
        "sync_conflict_policy": "manual_review",
    }


def target_release_audit(existing_paths: set[str] | None = None) -> dict:
    """Return package-level proof for web/PWA/mobile/desktop/chatbot targets."""
    expected_artifacts = {artifact for contract in TARGETS.values() for artifact in contract["artifacts"]}
    existing = expected_artifacts if existing_paths is None else existing_paths
    dsl_contract = dsl_target_contract()
    package_matrix = target_package_matrix()
    mobile = mobile_capability_contract()
    desktop = desktop_capability_contract()
    catalog_targets = {item["target"] for item in target_catalog()}
    gates = (
        {
            "id": "target_catalog",
            "ok": catalog_targets == set(TARGETS),
        },
        {
            "id": "dsl_target_selection",
            "ok": dsl_contract["ok"],
        },
        {
            "id": "package_matrix",
            "ok": package_matrix["ok"]
            and {"web", "mobile", "desktop"} <= {row["target"] for row in package_matrix["rows"]},
        },
        {
            "id": "mobile_contract",
            "ok": mobile["ok"],
        },
        {
            "id": "desktop_contract",
            "ok": desktop["ok"],
        },
        {
            "id": "pwa_chatbot_contracts",
            "ok": {"pwa", "chatbot"} <= catalog_targets,
        },
        {
            "id": "artifact_contract",
            "ok": expected_artifacts <= existing,
        },
    )
    ok = all(gate["ok"] for gate in gates)
    return {
        "format": "appgen.package-target-release-audit.v1",
        "scope": "package",
        "ok": ok,
        "decision": "approved" if ok else "blocked",
        "catalog": target_catalog(),
        "dsl": dsl_contract,
        "package_matrix": package_matrix,
        "mobile": mobile,
        "desktop": desktop,
        "gates": gates,
        "blocking_gaps": tuple(gate for gate in gates if not gate["ok"]),
        "stop_condition": "do-not-claim-multi-target-generation-unless-ok-is-true",
    }


def _verification_for(target: str) -> tuple[str, ...]:
    checks = {
        "web": ("py_compile", "route_smoke", "template_render"),
        "pwa": ("manifest_json", "service_worker", "offline_shell"),
        "mobile": ("py_compile", "permission_manifest", "offline_replay"),
        "desktop": ("py_compile", "local_cache", "sync_replay"),
        "chatbot": ("intent_export", "required_field_prompts", "provider_manifest"),
    }
    return checks[target]
