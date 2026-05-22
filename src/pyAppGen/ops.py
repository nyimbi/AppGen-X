"""Package-level operations roadmap release contracts.

Generated apps emit deployment, search, Node-RED, HTTPS, and database-ops
artifacts.  This module makes those roadmap promises auditable before
generation.
"""

from __future__ import annotations


OPS_SAMPLE_DSL = """
app OpsAudit { targets: web, mobile, desktop }

table WorkOrder {
  id: int pk
  title: string required search
  status: string default "open" search
}
"""

DEPLOYMENT_ARTIFACTS = (
    "Dockerfile",
    "docker-compose.yml",
    "deploy/k8s.yaml",
    "deploy/k8s-autoscale.yaml",
    "deploy/terraform-aws.tf",
    "deploy/terraform-gcp.tf",
    "deploy/terraform-azure.tf",
    "deploy/Caddyfile",
    "deploy/appgen_https.py",
)

SEARCH_ARTIFACTS = (
    "app/search.py",
    "app/templates/appgen_search.html",
    "docker-compose.yml",
)

NODE_RED_ARTIFACTS = (
    "automation/appgen_node_red.py",
    "automation/node-red/flows.json",
    "docker-compose.yml",
)

DATABASE_OPS_ARTIFACTS = (
    "app/database_ops.py",
    "app/templates/appgen_database_ops.html",
    "docker-compose.yml",
    "deploy/k8s.yaml",
)


def deployment_contract() -> dict:
    """Return deployment targets and required artifact contracts."""
    return {
        "format": "appgen.package-deployment-contract.v1",
        "targets": ("docker_compose", "kubernetes", "aws", "gcp", "azure", "onprem", "https"),
        "database_engines": ("postgresql", "mysql"),
        "artifacts": DEPLOYMENT_ARTIFACTS,
        "cloud_secret_stores": {
            "aws": "AWS Secrets Manager",
            "gcp": "Secret Manager",
            "azure": "Key Vault",
        },
        "runtime_checks": ("healthcheck", "readiness_probe", "rollback_plan", "autoscale_plan"),
    }


def search_contract() -> dict:
    """Return Elasticsearch and Whoosh search readiness contracts."""
    return {
        "format": "appgen.package-search-contract.v1",
        "providers": ("elasticsearch", "whoosh"),
        "artifacts": SEARCH_ARTIFACTS,
        "provider_env": {
            "elasticsearch": ("ELASTICSEARCH_URL",),
            "whoosh": ("WHOOSH_INDEX_DIR",),
        },
        "index_contracts": ("mapping", "schema", "reindex_plan", "row_matching"),
    }


def node_red_contract() -> dict:
    """Return default Node-RED automation runtime contracts."""
    return {
        "format": "appgen.package-node-red-contract.v1",
        "service": "node-red",
        "image": "nodered/node-red:3.1",
        "artifacts": NODE_RED_ARTIFACTS,
        "run": "docker compose up node-red",
        "flow_contracts": ("http_in", "http_response", "appgen_event_topics"),
    }


def database_ops_contract() -> dict:
    """Return database operations evidence for search and HA roadmap items."""
    return {
        "format": "appgen.package-database-ops-contract.v1",
        "artifacts": DATABASE_OPS_ARTIFACTS,
        "engines": ("postgresql", "mysql"),
        "ha_components": ("patroni", "zombodb", "postgraphile"),
        "search_components": ("elasticsearch",),
        "kubernetes_resources": ("StatefulSet", "Service", "PersistentVolumeClaim"),
    }


def ops_generation_smoke_audit(source: str = OPS_SAMPLE_DSL) -> dict:
    """Generate a temporary app and exercise generated operations contracts."""
    import importlib.util
    import json
    import py_compile
    import tempfile
    from pathlib import Path

    from .dsl import schema_from_dsl
    from .gen import generate_app_from_schema

    required_artifacts = tuple(
        dict.fromkeys(
            DEPLOYMENT_ARTIFACTS
            + SEARCH_ARTIFACTS
            + NODE_RED_ARTIFACTS
            + DATABASE_OPS_ARTIFACTS
            + (
                "deploy/appgen_deploy.py",
                "app/models.py",
                "app/views.py",
            )
        )
    )
    compile_artifacts = (
        "deploy/appgen_deploy.py",
        "deploy/appgen_https.py",
        "app/search.py",
        "app/database_ops.py",
        "automation/appgen_node_red.py",
        "app/models.py",
        "app/views.py",
    )

    with tempfile.TemporaryDirectory(prefix="appgen-ops-smoke-") as tmp:
        project_dir = Path(tmp) / "ops-smoke"
        output_dir = project_dir / "app"
        schema = schema_from_dsl(source, source_name="ops-smoke.appgen")
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
            ("deployment", "deploy/appgen_deploy.py"),
            ("https", "deploy/appgen_https.py"),
            ("search", "app/search.py"),
            ("database_ops", "app/database_ops.py"),
            ("node_red", "automation/appgen_node_red.py"),
        ):
            module_path = project_dir / artifact
            spec = importlib.util.spec_from_file_location(
                f"generated_ops_smoke_{name}",
                module_path,
            )
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
            modules[name] = module

        deployment = modules["deployment"]
        https = modules["https"]
        search = modules["search"]
        database_ops = modules["database_ops"]
        node_red = modules["node_red"]

        deployment_env = deployment.sample_deployment_environment()
        deployment_gate = deployment.deployment_release_gate(deployment_env, existing_paths)
        deployment_workbench = deployment.deployment_workbench(deployment_env, existing_paths)
        kubernetes_runbook = deployment.deployment_runbook(
            "kubernetes",
            image_tag="appgen:test",
            base_url="https://app.example.test",
        )
        scaling = deployment.infrastructure_scaling_plan(
            "kubernetes",
            {"replicas": 2, "cpu_percent": 91, "p95_ms": 900},
        )

        https_env = {"APPGEN_DOMAIN": "app.example.test", "APPGEN_TLS_EMAIL": "ops@example.test"}
        https_paths = {"deploy/Caddyfile", "docker-compose.yml", "deploy/appgen_https.py"}
        https_gate = https.https_release_gate(https_env, https_paths)
        https_workbench = https.https_workbench(https_env, https_paths)

        search_env = {
            "DATABASE_URL": "postgresql://appgen:appgen@db/appgen",
            "WHOOSH_INDEX_DIR": "/tmp/appgen-whoosh",
            "ELASTICSEARCH_URL": "http://elasticsearch:9200",
        }
        search_paths = {"app/search.py", "app/templates/appgen_search.html"}
        search_gate = search.search_release_gate(
            search_env,
            search_paths,
            required_provider="elasticsearch",
        )
        search_workbench = search.search_workbench(
            search_env,
            search_paths,
            required_provider="elasticsearch",
        )
        search_payload = search.search_payload(
            {"WorkOrder": ({"id": 1, "title": "Pump repair", "status": "open"},)},
            "pump",
        )
        elasticsearch_mapping = search.elasticsearch_mapping("WorkOrder")
        whoosh_schema = search.whoosh_schema("WorkOrder")

        database_paths = {
            "app/database_ops.py",
            "app/templates/appgen_database_ops.html",
            "docker-compose.yml",
            "deploy/k8s.yaml",
        }
        database_gate = database_ops.database_addon_release_gate(database_paths)
        database_workbench = database_ops.database_ops_workbench(database_paths)
        patroni = database_ops.patroni_cluster_plan()
        postgraphile = database_ops.postgraphile_schema_plan()
        zombodb = database_ops.zombodb_index_plan()
        migration = database_ops.migration_cutover_plan()
        nosql = database_ops.document_projection_matrix()

        flow_export = json.loads(
            (project_dir / "automation/node-red/flows.json").read_text(encoding="utf-8")
        )
        node_red_paths = {
            "automation/appgen_node_red.py",
            "automation/node-red/flows.json",
            "docker-compose.yml",
        }
        flow_validation = node_red.validate_flow_export(flow_export)
        node_red_gate = node_red.node_red_release_gate(node_red_paths, flow_export)
        node_red_workbench = node_red.node_red_workbench(node_red_paths, flow_export)
        runtime = node_red.node_red_runtime_service()

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
            "id": "deployment_and_https_gates",
            "ok": deployment_gate["ok"] is True
            and deployment_workbench["ok"] is True
            and kubernetes_runbook["review_required"] is True
            and scaling["profile"]["desired_replicas"] > scaling["profile"]["current_replicas"]
            and https_gate["ok"] is True
            and https_workbench["ok"] is True
            and https_gate["base_url"] == "https://app.example.test",
            "deployment_gate": deployment_gate,
            "https_gate": https_gate,
            "scaling": scaling,
        },
        {
            "id": "search_provider_contracts",
            "ok": search_gate["ok"] is True
            and search_workbench["ok"] is True
            and search_payload["results"][0]["matches"][0]["fields"]["title"] == "Pump repair"
            and elasticsearch_mapping["mappings"]["dynamic"] == "strict"
            and bool(whoosh_schema["fields"]),
            "search_gate": search_gate,
            "workbench": search_workbench,
            "elasticsearch_mapping": elasticsearch_mapping,
            "whoosh_schema": whoosh_schema,
        },
        {
            "id": "database_ops_contracts",
            "ok": database_gate["ok"] is True
            and database_workbench["ok"] is True
            and len(patroni["members"]) >= 3
            and postgraphile["rls_required"] is True
            and bool(zombodb["indexes"])
            and migration["requires_review"] is True
            and bool(nosql),
            "database_gate": database_gate,
            "workbench": database_workbench,
            "patroni": patroni,
            "postgraphile": postgraphile,
            "zombodb": zombodb,
            "migration": migration,
        },
        {
            "id": "node_red_runtime_contracts",
            "ok": flow_validation["ok"] is True
            and node_red_gate["ok"] is True
            and node_red_workbench["ok"] is True
            and runtime["service"] == "node-red"
            and runtime["image"] == "nodered/node-red:3.1",
            "flow_validation": flow_validation,
            "release_gate": node_red_gate,
            "workbench": node_red_workbench,
            "runtime": runtime,
        },
    )
    ok = all(check["ok"] for check in checks)
    return {
        "format": "appgen.ops-generation-smoke-audit.v1",
        "scope": "generated-app",
        "ok": ok,
        "decision": "approved" if ok else "blocked",
        "required_artifacts": required_artifacts,
        "compiled_artifacts": tuple(compiled),
        "checks": checks,
        "blocking_gaps": tuple(check for check in checks if not check["ok"]),
        "stop_condition": "do-not-claim-generated-ops-readiness-unless-ok-is-true",
    }


def ops_release_audit(existing_paths: set[str] | None = None) -> dict:
    """Return package-level proof for deployment, search, and automation ops."""
    existing = existing_paths or set(
        DEPLOYMENT_ARTIFACTS + SEARCH_ARTIFACTS + NODE_RED_ARTIFACTS + DATABASE_OPS_ARTIFACTS
    )
    deployment = deployment_contract()
    search = search_contract()
    node_red = node_red_contract()
    database_ops = database_ops_contract()
    generation_smoke = ops_generation_smoke_audit()
    gates = (
        {
            "id": "docker_kubernetes",
            "ok": {"Dockerfile", "docker-compose.yml", "deploy/k8s.yaml", "deploy/k8s-autoscale.yaml"} <= existing,
            "targets": ("docker_compose", "kubernetes"),
        },
        {
            "id": "terraform_clouds",
            "ok": {"deploy/terraform-aws.tf", "deploy/terraform-gcp.tf", "deploy/terraform-azure.tf"} <= existing,
            "clouds": ("aws", "gcp", "azure"),
        },
        {
            "id": "automatic_https",
            "ok": {"deploy/Caddyfile", "deploy/appgen_https.py"} <= existing and "https" in deployment["targets"],
        },
        {
            "id": "search_providers",
            "ok": set(SEARCH_ARTIFACTS) <= existing and {"elasticsearch", "whoosh"} <= set(search["providers"]),
        },
        {
            "id": "node_red_default",
            "ok": set(NODE_RED_ARTIFACTS) <= existing and node_red["image"] == "nodered/node-red:3.1",
        },
        {
            "id": "database_ops",
            "ok": set(DATABASE_OPS_ARTIFACTS) <= existing
            and {"patroni", "zombodb", "postgraphile"} <= set(database_ops["ha_components"]),
        },
        {
            "id": "generation_smoke",
            "ok": generation_smoke["ok"],
            "checks": tuple(check["id"] for check in generation_smoke["checks"]),
        },
    )
    ok = all(gate["ok"] for gate in gates)
    return {
        "format": "appgen.package-ops-release-audit.v1",
        "scope": "package",
        "ok": ok,
        "decision": "approved" if ok else "blocked",
        "contracts": {
            "deployment": deployment,
            "search": search,
            "node_red": node_red,
            "database_ops": database_ops,
        },
        "generation_smoke": generation_smoke,
        "gates": gates,
        "blocking_gaps": tuple(gate for gate in gates if not gate["ok"]),
        "stop_condition": "do-not-claim-ops-deployment-search-readiness-unless-ok-is-true",
    }
