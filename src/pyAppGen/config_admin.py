"""Package-level safe configuration editor contracts.

Generated apps include ``app/config_admin.py``.  This package module exposes the
same safety model before generation so roadmap-required ``config.py`` settings
and setup-screen behavior can be audited from the CLI.
"""

from __future__ import annotations

import ast


DEFAULT_CONFIG = {
    "APP_NAME": "AppGen",
    "SECRET_KEY": "replace-with-production-secret",
    "SQLALCHEMY_DATABASE_URI": "sqlite:///app.db",
    "FAB_API_SHOW_STACKTRACE": True,
    "FAB_API_SWAGGER_UI": True,
    "BABEL_DEFAULT_LOCALE": "en",
    "SESSION_COOKIE_SECURE": True,
    "REMEMBER_COOKIE_SECURE": True,
}

CONFIG_FIELDS = {
    "APP_NAME": {
        "group": "application",
        "type": "string",
        "editable": True,
        "secret": False,
        "help": "Displayed by generated setup screens and manifests.",
    },
    "SECRET_KEY": {
        "group": "security",
        "type": "secret",
        "editable": True,
        "secret": True,
        "help": "Must be replaced for production deployments.",
    },
    "SQLALCHEMY_DATABASE_URI": {
        "group": "database",
        "type": "database_url",
        "editable": True,
        "secret": True,
        "help": "SQLAlchemy URL used by generated applications.",
    },
    "FAB_API_SHOW_STACKTRACE": {
        "group": "api",
        "type": "bool",
        "editable": True,
        "secret": False,
        "help": "Roadmap-required FAB API diagnostic flag; disable outside development.",
    },
    "FAB_API_SWAGGER_UI": {
        "group": "api",
        "type": "bool",
        "editable": True,
        "secret": False,
        "help": "Roadmap-required FAB API Swagger UI flag.",
    },
    "BABEL_DEFAULT_LOCALE": {
        "group": "localization",
        "type": "string",
        "editable": True,
        "secret": False,
        "help": "Default locale for generated applications.",
    },
    "SESSION_COOKIE_SECURE": {
        "group": "security",
        "type": "bool",
        "editable": True,
        "secret": False,
        "help": "Require HTTPS for session cookies.",
    },
    "REMEMBER_COOKIE_SECURE": {
        "group": "security",
        "type": "bool",
        "editable": True,
        "secret": False,
        "help": "Require HTTPS for remember-me cookies.",
    },
}

REQUIRED_ROADMAP_FLAGS = ("FAB_API_SHOW_STACKTRACE", "FAB_API_SWAGGER_UI")

CONFIG_SAMPLE_DSL = """app ConfigSmoke { targets: web, mobile, desktop }

table SettingSubject {
  id: int pk
  name: string required search
}
"""


def config_editor_catalog() -> dict:
    """Return editable config fields grouped for a setup screen."""
    return {
        "format": "appgen.package-config-editor-catalog.v1",
        "fields": tuple(
            {"key": key, "default": DEFAULT_CONFIG[key], **metadata}
            for key, metadata in CONFIG_FIELDS.items()
        ),
        "groups": tuple(dict.fromkeys(metadata["group"] for metadata in CONFIG_FIELDS.values())),
        "editable_keys": tuple(CONFIG_FIELDS),
        "roadmap_required_flags": REQUIRED_ROADMAP_FLAGS,
        "ok": set(REQUIRED_ROADMAP_FLAGS) <= set(CONFIG_FIELDS),
    }


def parse_config_assignments(source: str) -> dict:
    """Parse top-level literal assignments from a Python config file."""
    tree = ast.parse(source)
    values = {}
    for node in tree.body:
        if not isinstance(node, ast.Assign) or len(node.targets) != 1:
            continue
        target = node.targets[0]
        if not isinstance(target, ast.Name):
            continue
        try:
            values[target.id] = ast.literal_eval(node.value)
        except (ValueError, SyntaxError):
            values[target.id] = None
    return values


def render_config(values: dict | None = None) -> str:
    """Render a deterministic Python ``config.py`` from whitelisted values."""
    merged = {**DEFAULT_CONFIG, **(values or {})}
    lines = ['"""Generated AppGen configuration."""', ""]
    for key in CONFIG_FIELDS:
        lines.append(f"{key} = {merged[key]!r}")
    return "\n".join(lines) + "\n"


def update_config_source(source: str, updates: dict) -> dict:
    """Apply whitelisted config updates and return the rendered preview."""
    current = {**DEFAULT_CONFIG, **parse_config_assignments(source)}
    rejected = tuple(sorted(key for key in updates if key not in CONFIG_FIELDS))
    accepted = {key: updates[key] for key in updates if key in CONFIG_FIELDS}
    current.update(accepted)
    rendered = render_config(current)
    return {
        "format": "appgen.package-config-update.v1",
        "ok": not rejected,
        "accepted": tuple(sorted(accepted)),
        "rejected": rejected,
        "values": current,
        "source": rendered,
        "production": production_config_status(current),
    }


def production_config_status(values: dict | None = None) -> dict:
    """Return production readiness warnings for config values."""
    merged = {**DEFAULT_CONFIG, **(values or {})}
    warnings = []
    blockers = []
    if merged.get("SECRET_KEY") == "replace-with-production-secret":
        blockers.append("Replace SECRET_KEY before production.")
    if merged.get("FAB_API_SHOW_STACKTRACE") is True:
        warnings.append("Disable FAB_API_SHOW_STACKTRACE outside development.")
    if merged.get("SESSION_COOKIE_SECURE") is not True:
        blockers.append("SESSION_COOKIE_SECURE must be true for production.")
    if merged.get("REMEMBER_COOKIE_SECURE") is not True:
        blockers.append("REMEMBER_COOKIE_SECURE must be true for production.")
    return {
        "format": "appgen.package-config-production-status.v1",
        "ok": not blockers,
        "warnings": tuple(warnings),
        "blockers": tuple(blockers),
    }


def env_export(values: dict | None = None) -> str:
    """Return shell-style environment exports for editable config values."""
    merged = {**DEFAULT_CONFIG, **(values or {})}
    lines = []
    for key in CONFIG_FIELDS:
        value = merged[key]
        if isinstance(value, bool):
            rendered = "true" if value else "false"
        else:
            rendered = str(value)
        lines.append(f"{key}={rendered}")
    return "\n".join(lines) + "\n"


def config_editor_generation_smoke_audit(source: str = CONFIG_SAMPLE_DSL) -> dict:
    """Generate a temporary app and exercise its generated config editor."""
    import importlib.util
    import py_compile
    import tempfile
    from pathlib import Path

    from .dsl import schema_from_dsl
    from .gen import generate_app_from_schema

    required_artifacts = (
        "config.py",
        "app/config_admin.py",
        "app/templates/appgen_config.html",
        "app/models.py",
        "app/views.py",
    )
    compile_artifacts = (
        "config.py",
        "app/config_admin.py",
        "app/models.py",
        "app/views.py",
    )

    with tempfile.TemporaryDirectory(prefix="appgen-config-smoke-") as tmp:
        project_dir = Path(tmp) / "config-smoke"
        output_dir = project_dir / "app"
        schema = schema_from_dsl(source, source_name="config-smoke.appgen")
        generate_app_from_schema(schema, output_dir)
        existing_paths = {
            path.relative_to(project_dir).as_posix()
            for path in project_dir.rglob("*")
            if path.is_file()
        }
        missing_artifacts = tuple(
            artifact for artifact in required_artifacts if artifact not in existing_paths
        )

        compiled = []
        compile_failures = []
        for artifact in compile_artifacts:
            path = project_dir / artifact
            if not path.exists():
                continue
            try:
                py_compile.compile(str(path), doraise=True)
            except py_compile.PyCompileError as exc:
                compile_failures.append({"artifact": artifact, "error": str(exc)})
            else:
                compiled.append(artifact)

        module_path = output_dir / "config_admin.py"
        spec = importlib.util.spec_from_file_location("generated_config_admin_smoke", module_path)
        generated_config_admin = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(generated_config_admin)

        config_source = (project_dir / "config.py").read_text(encoding="utf-8")
        generated_values = generated_config_admin.parse_config_assignments(config_source)
        generated_schema = generated_config_admin.config_schema()
        generated_sections = generated_config_admin.config_sections(generated_values)
        sample_values = generated_config_admin.sample_config_values()
        readiness = generated_config_admin.config_readiness(sample_values)
        unsafe = generated_config_admin.config_readiness(
            generated_config_admin.sample_config_values(
                {"SECRET_KEY": "change-me-before-deploy", "SQLALCHEMY_DATABASE_URI": ""}
            )
        )
        updated = generated_config_admin.replace_config_assignment(
            config_source,
            "APP_NAME",
            "Config Smoke",
        )
        try:
            generated_config_admin.replace_config_assignment(config_source, "UNKNOWN_SETTING", True)
        except KeyError:
            unknown_rejected = True
        else:
            unknown_rejected = False
        env = generated_config_admin.env_template(sample_values)
        release_paths = {
            "config.py",
            "app/config_admin.py",
            "app/templates/appgen_config.html",
        }
        release_gate = generated_config_admin.config_admin_release_gate(release_paths)
        workbench = generated_config_admin.config_admin_workbench(release_paths)

    checks = (
        {
            "id": "generated_artifacts",
            "ok": not missing_artifacts,
            "required_artifacts": required_artifacts,
            "missing": missing_artifacts,
        },
        {
            "id": "generated_python_compiles",
            "ok": not compile_failures and set(compiled) == set(compile_artifacts),
            "compiled": tuple(compiled),
            "failures": tuple(compile_failures),
        },
        {
            "id": "generated_catalog_and_flags",
            "ok": {"FAB_API_SHOW_STACKTRACE", "FAB_API_SWAGGER_UI"}
            <= set(generated_schema["keys"])
            and generated_schema["editable_count"] >= len(CONFIG_FIELDS)
            and any(section["name"] == "API" for section in generated_sections),
            "schema": generated_schema,
        },
        {
            "id": "generated_parse_readiness",
            "ok": generated_values.get("FAB_API_SHOW_STACKTRACE") is True
            and generated_values.get("FAB_API_SWAGGER_UI") is True
            and readiness["ready"] is True
            and unsafe["ready"] is False,
            "readiness": readiness,
            "unsafe": unsafe,
        },
        {
            "id": "generated_safe_rewrite_and_env",
            "ok": "APP_NAME = 'Config Smoke'" in updated
            and unknown_rejected
            and "FAB_API_SWAGGER_UI=true" in env
            and "SECRET_KEY=replace-with-production-secret" in env,
            "env": env,
        },
        {
            "id": "generated_release_contracts",
            "ok": release_gate["ok"] and workbench["ok"],
            "release_gate": release_gate["format"],
            "workbench": workbench["format"],
        },
    )
    ok = all(check["ok"] for check in checks)
    return {
        "format": "appgen.config-editor-generation-smoke-audit.v1",
        "ok": ok,
        "decision": "approved" if ok else "blocked",
        "required_artifacts": required_artifacts,
        "compiled_artifacts": tuple(compiled),
        "checks": checks,
        "blocking_gaps": tuple(check for check in checks if not check["ok"]),
        "stop_condition": "do-not-claim-generated-config-editor-readiness-unless-ok-is-true",
    }


def config_editor_release_audit(existing_paths: set[str] | None = None) -> dict:
    """Return package-level proof for safe configuration editing."""
    existing = existing_paths or {"config.py", "app/config_admin.py", "app/templates/appgen_config.html"}
    catalog = config_editor_catalog()
    source = render_config()
    parsed = parse_config_assignments(source)
    production_preview = production_config_status(
        {**parsed, "SECRET_KEY": "production-secret", "FAB_API_SHOW_STACKTRACE": False}
    )
    unsafe_preview = update_config_source(source, {"UNKNOWN_SETTING": True})
    env = env_export(parsed)
    required_paths = {"config.py", "app/config_admin.py", "app/templates/appgen_config.html"}
    generation_smoke = config_editor_generation_smoke_audit()
    gates = (
        {"id": "roadmap_flags", "ok": all(parsed.get(flag) is True for flag in REQUIRED_ROADMAP_FLAGS)},
        {"id": "editable_catalog", "ok": catalog["ok"] and len(catalog["fields"]) == len(CONFIG_FIELDS)},
        {"id": "whitelisted_updates", "ok": unsafe_preview["ok"] is False and unsafe_preview["rejected"] == ("UNKNOWN_SETTING",)},
        {"id": "production_safety", "ok": production_preview["ok"] is True},
        {"id": "env_export", "ok": "FAB_API_SWAGGER_UI=true" in env and "SECRET_KEY=replace-with-production-secret" in env},
        {"id": "artifact_contract", "ok": required_paths <= existing, "required": tuple(sorted(required_paths))},
        {
            "id": "generation_smoke",
            "ok": generation_smoke["ok"],
            "checks": tuple(check["id"] for check in generation_smoke["checks"]),
        },
    )
    ok = all(gate["ok"] for gate in gates)
    return {
        "format": "appgen.package-config-editor-release-audit.v1",
        "scope": "package",
        "ok": ok,
        "decision": "approved" if ok else "blocked",
        "catalog": catalog,
        "sample_config": source,
        "parsed": parsed,
        "production_preview": production_preview,
        "env_export": env,
        "generation_smoke": generation_smoke,
        "gates": gates,
        "blocking_gaps": tuple(gate for gate in gates if not gate["ok"]),
        "stop_condition": "do-not-claim-config-editor-readiness-unless-ok-is-true",
    }
