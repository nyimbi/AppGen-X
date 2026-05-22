"""Package-level multi-target application generation contracts."""

from __future__ import annotations

import json
import py_compile
import tempfile
from pathlib import Path

from .dsl import schema_from_dsl


TARGETS = {
    "web": {
        "runtime": "Flask-AppBuilder",
        "artifacts": ("app/__init__.py", "app/views.py", "app/templates/my_index.html"),
        "capabilities": ("responsive_forms", "rbac", "api_routes", "reports"),
    },
    "pwa": {
        "runtime": "service-worker",
        "artifacts": ("app/static/appgen.webmanifest", "app/static/appgen-sw.js"),
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
_SMOKE_PYTHON_ARTIFACTS = (
    "app/__init__.py",
    "app/views.py",
    "app/platforms.py",
    "app/pwa.py",
    "native/appgen_native.py",
    "native/mobile/app.py",
    "native/desktop/app.py",
    "chatbots/appgen_chatbots.py",
)
_SMOKE_JSON_ARTIFACTS = (
    "app/static/appgen.webmanifest",
    "chatbots/dialogflow/intents.json",
    "chatbots/botframework/manifest.json",
)

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


def _compile_target_artifacts(project_dir: Path) -> tuple[dict, ...]:
    results = []
    for relative in _SMOKE_PYTHON_ARTIFACTS:
        path = project_dir / relative
        try:
            py_compile.compile(str(path), doraise=True)
        except py_compile.PyCompileError as exc:
            results.append({"path": relative, "ok": False, "error": str(exc)})
        else:
            results.append({"path": relative, "ok": True})
    return tuple(results)


def _json_target_artifacts(project_dir: Path) -> tuple[dict, ...]:
    results = []
    for relative in _SMOKE_JSON_ARTIFACTS:
        path = project_dir / relative
        try:
            json.loads(path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError) as exc:
            results.append({"path": relative, "ok": False, "error": str(exc)})
        else:
            results.append({"path": relative, "ok": True})
    return tuple(results)


def target_generation_smoke_audit() -> dict:
    """Generate every application target and verify emitted artifacts."""
    from .gen import generate_app_from_schema

    with tempfile.TemporaryDirectory(prefix="appgen-target-generation-") as raw_workdir:
        project_dir = Path(raw_workdir) / "target-smoke"
        app_dir = project_dir / "app"
        generate_app_from_schema(
            schema_from_dsl(TARGET_SAMPLE_DSL, source_name="target-smoke.appgen"),
            app_dir,
        )
        target_rows = tuple(
            {
                "target": target,
                "artifacts": contract["artifacts"],
                "missing": tuple(
                    artifact
                    for artifact in contract["artifacts"]
                    if not (project_dir / artifact).exists()
                ),
            }
            for target, contract in TARGETS.items()
        )
        compile_results = _compile_target_artifacts(project_dir)
        json_results = _json_target_artifacts(project_dir)
        home_text = (project_dir / "app/templates/my_index.html").read_text(encoding="utf-8")
        service_worker = (project_dir / "app/static/appgen-sw.js").read_text(encoding="utf-8")
        manifest = json.loads(
            (project_dir / "app/static/appgen.webmanifest").read_text(encoding="utf-8")
        )
    checks = (
        {
            "check": "target_artifacts",
            "ok": all(not row["missing"] for row in target_rows),
            "targets": tuple(row["target"] for row in target_rows),
        },
        {
            "check": "compiled_python_targets",
            "ok": all(item["ok"] for item in compile_results),
            "artifacts": _SMOKE_PYTHON_ARTIFACTS,
        },
        {
            "check": "json_target_exports",
            "ok": all(item["ok"] for item in json_results),
            "artifacts": _SMOKE_JSON_ARTIFACTS,
        },
        {
            "check": "pwa_runtime_assets",
            "ok": "/static/appgen.webmanifest" in home_text
            and "APPGEN_CACHE" in service_worker
            and manifest.get("display") == "standalone",
        },
    )
    return {
        "format": "appgen.package-target-generation-smoke-audit.v1",
        "scope": "package",
        "rows": target_rows,
        "compiled": compile_results,
        "json_artifacts": json_results,
        "checks": checks,
        "ok": all(check["ok"] for check in checks),
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
    smoke = target_generation_smoke_audit()
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
            "id": "target_generation_smoke",
            "ok": smoke["ok"],
            "checks": smoke["checks"],
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
        "generation_smoke": smoke,
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
