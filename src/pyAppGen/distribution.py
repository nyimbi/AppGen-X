"""Package-level distribution and template release contracts.

Generated apps already emit packaging files, Cookiecutter templates, extension
hooks, seeds, and generated coverage tests.  This module exposes a
pre-generation package audit for the roadmap's publishable/FAB-extension/
Cookiecutter/test-coverage lane.
"""

from __future__ import annotations


DISTRIBUTION_SAMPLE_DSL = """
app DistributionAudit { targets: web, mobile, desktop }

table Customer {
  id: int pk
  name: string required search
  email: email search
}

table Invoice {
  id: int pk
  customer_id: int required -> Customer.id [many-to-one]
  invoice_no: string required unique search
  total_amount: decimal required
}

flow PublishInvoice {
  draft -> approved
  approved -> sent
}
"""

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


def distribution_generation_smoke_audit(source: str = DISTRIBUTION_SAMPLE_DSL) -> dict:
    """Generate a temporary app and exercise publish/template release contracts."""
    import importlib.util
    import json
    import py_compile
    import subprocess
    import sys
    import tempfile
    from pathlib import Path

    from .dsl import schema_from_dsl
    from .gen import generate_app_from_schema

    required_artifacts = tuple(
        dict.fromkeys(
            PUBLISHABLE_ARTIFACTS
            + COOKIECUTTER_ARTIFACTS
            + FAB_EXTENSION_ARTIFACTS
            + QUALITY_ARTIFACTS
            + ("MANIFEST.in", "requirements.txt")
        )
    )
    compile_artifacts = (
        "appgen_package.py",
        "seed.py",
        "config.py",
        "tests/test_generated_coverage.py",
        "scripts/appgen_quality.py",
        "app/models.py",
        "app/views.py",
        "app_custom/extensions.py",
    )

    with tempfile.TemporaryDirectory(prefix="appgen-distribution-smoke-") as tmp:
        project_dir = Path(tmp) / "distribution-smoke"
        output_dir = project_dir / "app"
        schema = schema_from_dsl(source, source_name="distribution-smoke.appgen")
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

        modules = {}
        for name, artifact in (
            ("package", "appgen_package.py"),
            ("coverage", "tests/test_generated_coverage.py"),
            ("seed", "seed.py"),
        ):
            module_path = project_dir / artifact
            spec = importlib.util.spec_from_file_location(
                f"generated_distribution_smoke_{name}",
                module_path,
            )
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
            modules[name] = module

        appgen_package = modules["package"]
        generated_coverage = modules["coverage"]
        seed = modules["seed"]

        package_metadata = appgen_package.package_metadata()
        extension = appgen_package.fab_extension_contract()
        cookiecutter = appgen_package.cookiecutter_context()
        packaging_gate = appgen_package.packaging_release_gate(existing_paths)
        packaging_workbench = appgen_package.packaging_workbench(existing_paths)
        cookiecutter_json = json.loads(
            (project_dir / "cookiecutter/cookiecutter.json").read_text(encoding="utf-8")
        )
        pyproject_text = (project_dir / "pyproject.toml").read_text(encoding="utf-8")
        manifest_text = (project_dir / "MANIFEST.in").read_text(encoding="utf-8")
        cookie_pyproject = (
            project_dir / "cookiecutter/{{cookiecutter.project_slug}}/pyproject.toml"
        ).read_text(encoding="utf-8")

        coverage_summary = generated_coverage.coverage_summary()
        coverage_gate = generated_coverage.coverage_release_gate(existing_paths)
        coverage_workbench = generated_coverage.coverage_workbench(existing_paths)
        uncovered_tables = generated_coverage.uncovered_requirements()
        uncovered_workflows = generated_coverage.uncovered_workflow_requirements()

        seed_gate = seed.seed_release_gate(existing_paths)
        seed_workbench = seed.seed_workbench(existing_paths)
        seed_fixture = seed.seed_fixture_export("smoke")
        seed_validation = seed.validate_seed_data()
        seed_sql = seed.seed_sql()

        quality = subprocess.run(
            [sys.executable, str(project_dir / "scripts/appgen_quality.py")],
            cwd=project_dir,
            text=True,
            capture_output=True,
            check=False,
        )

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
            "id": "publishable_package_contract",
            "ok": package_metadata["package_name"].startswith("appgen-")
            and package_metadata["build_command"] == "python -m build"
            and "appgen-quality" in pyproject_text
            and "recursive-include cookiecutter" in manifest_text
            and packaging_gate["ok"] is True
            and packaging_workbench["ok"] is True,
            "metadata": package_metadata,
            "gate": packaging_gate,
            "workbench": packaging_workbench,
        },
        {
            "id": "cookiecutter_and_fab_extension",
            "ok": "project_slug" in cookiecutter_json
            and cookiecutter["project_slug"].startswith("appgen_")
            and "{{ cookiecutter.package_name }}" in cookie_pyproject
            and extension["custom_hooks"] == "app_custom.extensions"
            and extension["templates"] == "app/templates",
            "cookiecutter": cookiecutter,
            "extension": extension,
            "cookiecutter_json": cookiecutter_json,
        },
        {
            "id": "generated_coverage_contracts",
            "ok": coverage_summary["ok"] is True
            and coverage_summary["tables"] == 2
            and coverage_summary["workflows"] == 1
            and coverage_gate["ok"] is True
            and coverage_workbench["ok"] is True
            and not uncovered_tables
            and not uncovered_workflows,
            "summary": coverage_summary,
            "gate": coverage_gate,
            "workbench": coverage_workbench,
        },
        {
            "id": "seed_fixture_contracts",
            "ok": seed_gate["ok"] is True
            and seed_workbench["ok"] is True
            and seed_fixture["format"] == "appgen.seed-fixture.v1"
            and seed_fixture["validation"]["ok"] is True
            and seed_validation["ok"] is True
            and bool(seed_sql),
            "gate": seed_gate,
            "workbench": seed_workbench,
            "fixture": seed_fixture,
        },
        {
            "id": "generated_quality_entrypoint",
            "ok": quality.returncode == 0 and "appgen quality passed" in quality.stdout,
            "returncode": quality.returncode,
            "stdout": quality.stdout.strip(),
            "stderr": quality.stderr.strip(),
        },
    )
    ok = all(check["ok"] for check in checks)
    return {
        "format": "appgen.distribution-generation-smoke-audit.v1",
        "scope": "generated-app",
        "ok": ok,
        "decision": "approved" if ok else "blocked",
        "required_artifacts": required_artifacts,
        "compiled_artifacts": tuple(compiled),
        "checks": checks,
        "blocking_gaps": tuple(check for check in checks if not check["ok"]),
        "stop_condition": "do-not-claim-generated-distribution-readiness-unless-ok-is-true",
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
    generation_smoke = distribution_generation_smoke_audit()
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
        {
            "id": "generation_smoke",
            "ok": generation_smoke["ok"],
            "checks": tuple(check["id"] for check in generation_smoke["checks"]),
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
        "generation_smoke": generation_smoke,
        "gates": gates,
        "blocking_gaps": tuple(gate for gate in gates if not gate["ok"]),
        "stop_condition": "do-not-claim-publishable-template-readiness-unless-ok-is-true",
    }
