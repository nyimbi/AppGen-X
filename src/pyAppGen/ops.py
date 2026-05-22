"""Package-level operations roadmap release contracts.

Generated apps emit deployment, search, Node-RED, HTTPS, and database-ops
artifacts.  This module makes those roadmap promises auditable before
generation.
"""

from __future__ import annotations


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


def ops_release_audit(existing_paths: set[str] | None = None) -> dict:
    """Return package-level proof for deployment, search, and automation ops."""
    existing = existing_paths or set(
        DEPLOYMENT_ARTIFACTS + SEARCH_ARTIFACTS + NODE_RED_ARTIFACTS + DATABASE_OPS_ARTIFACTS
    )
    deployment = deployment_contract()
    search = search_contract()
    node_red = node_red_contract()
    database_ops = database_ops_contract()
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
        "gates": gates,
        "blocking_gaps": tuple(gate for gate in gates if not gate["ok"]),
        "stop_condition": "do-not-claim-ops-deployment-search-readiness-unless-ok-is-true",
    }
