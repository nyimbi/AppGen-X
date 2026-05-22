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
    gates = (
        {"id": "roadmap_flags", "ok": all(parsed.get(flag) is True for flag in REQUIRED_ROADMAP_FLAGS)},
        {"id": "editable_catalog", "ok": catalog["ok"] and len(catalog["fields"]) == len(CONFIG_FIELDS)},
        {"id": "whitelisted_updates", "ok": unsafe_preview["ok"] is False and unsafe_preview["rejected"] == ("UNKNOWN_SETTING",)},
        {"id": "production_safety", "ok": production_preview["ok"] is True},
        {"id": "env_export", "ok": "FAB_API_SWAGGER_UI=true" in env and "SECRET_KEY=replace-with-production-secret" in env},
        {"id": "artifact_contract", "ok": required_paths <= existing, "required": tuple(sorted(required_paths))},
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
        "gates": gates,
        "blocking_gaps": tuple(gate for gate in gates if not gate["ok"]),
        "stop_condition": "do-not-claim-config-editor-readiness-unless-ok-is-true",
    }
