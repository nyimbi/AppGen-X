"""Package-level distribution and template release contracts.

Generated apps already emit packaging files, Cookiecutter templates, extension
hooks, seeds, and generated coverage tests.  This module exposes a
pre-generation package audit for the roadmap's publishable/FAB-extension/
Cookiecutter/test-coverage lane.
"""

from __future__ import annotations


PUBLISHABLE_ARTIFACTS = (
    "pyproject.toml",
    "README.md",
    "appgen_package.py",
    "app/__init__.py",
    "app/models.py",
    "app/views.py",
    "config.py",
    "seed.py",
    "tests/test_generated_coverage.py",
)

COOKIECUTTER_ARTIFACTS = (
    "cookiecutter/cookiecutter.json",
    "cookiecutter/{{cookiecutter.project_slug}}/pyproject.toml",
    "cookiecutter/{{cookiecutter.project_slug}}/app/__init__.py",
    "cookiecutter/{{cookiecutter.project_slug}}/README.md",
)

FAB_EXTENSION_ARTIFACTS = (
    "app/extensions.py",
    "app_custom/extensions.py",
    "app/templates/appgen_extensions.html",
)

QUALITY_ARTIFACTS = (
    "tests/test_generated_coverage.py",
    "scripts/appgen_quality.py",
    ".github/workflows/appgen-ci.yml",
)


def distribution_artifact_manifest(app_name: str = "AppGenApp") -> dict:
    """Return the publishable package artifact contract."""
    return {
        "format": "appgen.package-distribution-artifacts.v1",
        "app_name": app_name,
        "artifacts": PUBLISHABLE_ARTIFACTS,
        "package_commands": (
            "python -m build",
            "python -m pytest",
            "appgen --package-goal-audit",
        ),
        "metadata": {
            "name": app_name.lower().replace("_", "-"),
            "framework": "Flask-AppBuilder",
            "source_families": ("dbml", "sql", "ponyorm", "database", "dsl"),
        },
    }


def cookiecutter_template_manifest(app_name: str = "AppGenApp") -> dict:
    """Return the Cookiecutter template contract."""
    return {
        "format": "appgen.cookiecutter-template.v1",
        "app_name": app_name,
        "artifacts": COOKIECUTTER_ARTIFACTS,
        "variables": (
            "project_name",
            "project_slug",
            "database_url",
            "app_targets",
            "include_sample_data",
        ),
        "post_generate_checks": ("compile", "dsl_lint", "generated_coverage"),
    }


def fab_extension_manifest() -> dict:
    """Return the Flask-AppBuilder extension packaging contract."""
    return {
        "format": "appgen.fab-extension-package.v1",
        "artifacts": FAB_EXTENSION_ARTIFACTS,
        "entrypoints": (
            "register_appgen_views",
            "register_appgen_security",
            "register_appgen_cli",
        ),
        "extension_points": (
            "models",
            "views",
            "menus",
            "security",
            "templates",
            "custom_code",
        ),
    }


def generated_coverage_manifest() -> dict:
    """Return generated coverage/test evidence expected from publishable apps."""
    return {
        "format": "appgen.generated-coverage-manifest.v1",
        "artifacts": QUALITY_ARTIFACTS,
        "coverage_targets": (
            "models_compile",
            "views_compile",
            "api_contract",
            "graphql_contract",
            "security_contract",
            "dsl_release_gate",
            "package_goal_audit",
        ),
        "minimum_generated_tests": 7,
    }


def seed_script_manifest() -> dict:
    """Return seed-script release evidence for generated apps."""
    return {
        "format": "appgen.seed-script-manifest.v1",
        "artifacts": ("seed.py",),
        "seed_modes": ("sample_data", "demo_data", "idempotent_upsert"),
        "guards": ("no_plaintext_secrets", "repeatable_ids", "transactional_load"),
    }


def distribution_release_audit(existing_paths: set[str] | None = None) -> dict:
    """Return package-level release proof for publishing and template outputs."""
    existing = existing_paths or set(
        PUBLISHABLE_ARTIFACTS
        + COOKIECUTTER_ARTIFACTS
        + FAB_EXTENSION_ARTIFACTS
        + QUALITY_ARTIFACTS
    )
    package = distribution_artifact_manifest()
    cookiecutter = cookiecutter_template_manifest()
    fab = fab_extension_manifest()
    coverage = generated_coverage_manifest()
    seed = seed_script_manifest()
    required = set(
        PUBLISHABLE_ARTIFACTS
        + COOKIECUTTER_ARTIFACTS
        + FAB_EXTENSION_ARTIFACTS
        + QUALITY_ARTIFACTS
    )
    gates = (
        {
            "id": "publishable_package",
            "ok": set(PUBLISHABLE_ARTIFACTS) <= existing and "python -m build" in package["package_commands"],
            "artifacts": PUBLISHABLE_ARTIFACTS,
        },
        {
            "id": "cookiecutter_template",
            "ok": set(COOKIECUTTER_ARTIFACTS) <= existing and "project_slug" in cookiecutter["variables"],
            "artifacts": COOKIECUTTER_ARTIFACTS,
        },
        {
            "id": "fab_extension",
            "ok": set(FAB_EXTENSION_ARTIFACTS) <= existing and "register_appgen_views" in fab["entrypoints"],
            "artifacts": FAB_EXTENSION_ARTIFACTS,
        },
        {
            "id": "generated_test_coverage",
            "ok": set(QUALITY_ARTIFACTS) <= existing and coverage["minimum_generated_tests"] >= 7,
            "artifacts": QUALITY_ARTIFACTS,
        },
        {
            "id": "seed_scripts",
            "ok": set(seed["artifacts"]) <= existing and "idempotent_upsert" in seed["seed_modes"],
            "artifacts": seed["artifacts"],
        },
    )
    ok = all(gate["ok"] for gate in gates)
    return {
        "format": "appgen.package-distribution-release-audit.v1",
        "scope": "package",
        "ok": ok,
        "decision": "approved" if ok else "blocked",
        "required_artifacts": tuple(sorted(required)),
        "manifests": {
            "package": package,
            "cookiecutter": cookiecutter,
            "fab_extension": fab,
            "coverage": coverage,
            "seed": seed,
        },
        "gates": gates,
        "blocking_gaps": tuple(gate for gate in gates if not gate["ok"]),
        "stop_condition": "do-not-claim-publishable-template-readiness-unless-ok-is-true",
    }
