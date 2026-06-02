"""Database-backed repository for the api_gateway_mesh standalone app."""

from __future__ import annotations

import json
import sqlite3
from pathlib import Path


PACKAGE_DIR = Path(__file__).resolve().parent
MIGRATIONS_DIR = PACKAGE_DIR / "migrations"
SNAPSHOT_TABLE = "api_gateway_mesh_runtime_snapshot"
PERSISTED_TABLES = (
    "api_gateway_mesh_service_registration",
    "api_gateway_mesh_endpoint_catalog",
    "api_gateway_mesh_service_route",
    "api_gateway_mesh_route_version",
    "api_gateway_mesh_rate_limit_policy",
    "api_gateway_mesh_mtls_identity",
    "api_gateway_mesh_service_health",
    "api_gateway_mesh_traffic_sample",
    "api_gateway_mesh_gateway_rule",
    "api_gateway_mesh_gateway_parameter",
    "api_gateway_mesh_gateway_configuration",
    "api_gateway_mesh_gateway_retry_evidence",
    "api_gateway_mesh_appgen_outbox_event",
    "api_gateway_mesh_appgen_inbox_event",
    "api_gateway_mesh_dead_letter_event",
)


def _json_dumps(value) -> str:
    return json.dumps(value, sort_keys=True)


def _json_loads(value: str | None):
    if value in (None, ""):
        return None
    return json.loads(value)


def _now() -> str:
    return "2026-05-29T00:00:00Z"


def _normalized_version(value) -> int:
    raw = str(value or "1").strip().lower()
    if raw.startswith("v") and raw[1:].isdigit():
        return int(raw[1:])
    return int(raw) if raw.isdigit() else 1


def _clean_migration_sql(text: str) -> str:
    return text.replace("CREATE SCHEMA IF NOT EXISTS api_gateway_mesh;", "")


class ApiGatewayMeshRepository:
    """Persist standalone gateway state into owned tables plus a local snapshot."""

    def __init__(self, database_path: str = ":memory:"):
        self.database_path = database_path
        self.connection = sqlite3.connect(database_path)
        self.connection.row_factory = sqlite3.Row

    def close(self) -> None:
        self.connection.close()

    def apply_migrations(self) -> tuple[str, ...]:
        applied = []
        for migration_path in sorted(MIGRATIONS_DIR.glob("*.sql")):
            self.connection.executescript(_clean_migration_sql(migration_path.read_text()))
            applied.append(migration_path.name)
        self.connection.execute(
            f"""
            CREATE TABLE IF NOT EXISTS {SNAPSHOT_TABLE} (
                snapshot_id TEXT PRIMARY KEY,
                state_json TEXT NOT NULL,
                created_at TEXT NOT NULL
            )
            """
        )
        self.connection.commit()
        return tuple(applied) + ("runtime_snapshot",)

    def clear_persisted_state(self) -> None:
        for table in reversed(PERSISTED_TABLES):
            self.connection.execute(f"DELETE FROM {table}")
        self.connection.execute(f"DELETE FROM {SNAPSHOT_TABLE}")

    def save_runtime_state(self, state: dict) -> dict:
        timestamp = _now()
        self.clear_persisted_state()
        self._save_configuration(state.get("configuration", {}), timestamp=timestamp)
        self._save_parameters(state.get("parameters", {}), timestamp=timestamp)
        self._save_rules(state.get("rules", {}), timestamp=timestamp)
        self._save_services(state.get("services", {}), timestamp=timestamp)
        self._save_routes(state.get("routes", {}), timestamp=timestamp)
        self._save_rate_limits(state.get("rate_limits", {}), timestamp=timestamp)
        self._save_identities(state.get("identities", {}), timestamp=timestamp)
        self._save_health(state.get("health", {}), timestamp=timestamp)
        self._save_traffic(state.get("traffic", {}), timestamp=timestamp)
        self._save_retry_evidence(state.get("retry_evidence", ()), timestamp=timestamp)
        self._save_outbox(state.get("outbox", ()), timestamp=timestamp)
        self._save_inbox(state.get("inbox", ()), timestamp=timestamp)
        self._save_dead_letters(
            state.get("dead_letter", state.get("dead_letters", ())),
            timestamp=timestamp,
        )
        self.connection.execute(
            f"INSERT INTO {SNAPSHOT_TABLE} (snapshot_id, state_json, created_at) VALUES (?, ?, ?)",
            ("latest", _json_dumps(state), timestamp),
        )
        self.connection.commit()
        return {
            "ok": True,
            "database_path": self.database_path,
            "persisted_tables": PERSISTED_TABLES,
            "snapshot_table": SNAPSHOT_TABLE,
            "side_effects": (),
        }

    def load_runtime_state(self) -> dict:
        row = self.connection.execute(
            f"SELECT state_json FROM {SNAPSHOT_TABLE} WHERE snapshot_id = ?",
            ("latest",),
        ).fetchone()
        if row is None:
            return {}
        return _json_loads(row["state_json"]) or {}

    def list_services(self, *, tenant: str | None = None) -> tuple[dict, ...]:
        query = """
            SELECT tenant, service_id, pbc, name, version, region, status
            FROM api_gateway_mesh_service_registration
            WHERE 1 = 1
        """
        params = []
        if tenant:
            query += " AND tenant = ?"
            params.append(tenant)
        query += " ORDER BY tenant, service_id"
        rows = self.connection.execute(query, params).fetchall()
        return tuple(dict(row) for row in rows)

    def list_routes(self, *, tenant: str | None = None) -> tuple[dict, ...]:
        query = """
            SELECT tenant, route_id, service_id, host, path, method, protocol, status
            FROM api_gateway_mesh_service_route
            WHERE 1 = 1
        """
        params = []
        if tenant:
            query += " AND tenant = ?"
            params.append(tenant)
        query += " ORDER BY tenant, route_id"
        rows = self.connection.execute(query, params).fetchall()
        return tuple(dict(row) for row in rows)

    def database_manifest(self) -> dict:
        return {
            "ok": True,
            "database_path": self.database_path,
            "owned_tables": PERSISTED_TABLES,
            "snapshot_table": SNAPSHOT_TABLE,
            "migration_dir": str(MIGRATIONS_DIR),
            "shared_table_access": False,
            "side_effects": (),
        }

    def _save_configuration(self, configuration: dict, *, timestamp: str) -> None:
        if not configuration:
            return
        self.connection.execute(
            """
            INSERT INTO api_gateway_mesh_gateway_configuration (
                tenant, configuration_id, database_backend, event_topic, retry_limit,
                event_contract, status, audit_hash, created_at, updated_at
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                configuration.get("tenant", "platform"),
                configuration.get("configuration_id", "gateway-runtime"),
                configuration.get("database_backend", "postgresql"),
                configuration.get("event_topic", "appgen.gateway.events"),
                int(configuration.get("retry_limit", 3)),
                configuration.get("event_contract", "AppGen-X"),
                configuration.get("status", "active"),
                str(configuration.get("audit_hash", "runtime-config")),
                timestamp,
                timestamp,
            ),
        )

    def _save_parameters(self, parameters: dict, *, timestamp: str) -> None:
        for name, value in parameters.items():
            self.connection.execute(
                """
                INSERT INTO api_gateway_mesh_gateway_parameter (
                    tenant, parameter_id, name, value, effective_at, status,
                    audit_hash, created_at, updated_at
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    "platform",
                    str(name),
                    str(name),
                    _json_dumps(value),
                    timestamp,
                    "active",
                    f"parameter:{name}",
                    timestamp,
                    timestamp,
                ),
            )

    def _save_rules(self, rules: dict, *, timestamp: str) -> None:
        for rule in rules.values():
            self.connection.execute(
                """
                INSERT INTO api_gateway_mesh_gateway_rule (
                    tenant, rule_id, rule_type, scope, compiled_hash, enabled,
                    status, audit_hash, created_at, updated_at
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    rule.get("tenant", "platform"),
                    rule["rule_id"],
                    rule.get("rule_type", rule.get("scope", "routing")),
                    rule.get("scope", rule.get("rule_type", "routing")),
                    rule.get("compiled_hash", f"rule:{rule['rule_id']}"),
                    1 if rule.get("enabled", False) else 0,
                    rule.get("status", "active"),
                    f"rule:{rule['rule_id']}",
                    timestamp,
                    timestamp,
                ),
            )

    def _save_services(self, services: dict, *, timestamp: str) -> None:
        for service in services.values():
            self.connection.execute(
                """
                INSERT INTO api_gateway_mesh_service_registration (
                    tenant, service_id, pbc, name, version, region, status,
                    audit_hash, created_at, updated_at
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    service.get("tenant", "platform"),
                    service["service_id"],
                    service.get("pbc", "api_gateway_mesh"),
                    service.get("name", service["service_id"]),
                    _normalized_version(service.get("version")),
                    service.get("region", "unknown"),
                    service.get("status", "registered"),
                    f"service:{service['service_id']}",
                    timestamp,
                    timestamp,
                ),
            )
            for index, upstream in enumerate(service.get("upstreams", ()), start=1):
                self.connection.execute(
                    """
                    INSERT INTO api_gateway_mesh_endpoint_catalog (
                        tenant, endpoint_id, service_id, upstream_url, protocol,
                        method, status, audit_hash, created_at, updated_at
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                    """,
                    (
                        service.get("tenant", "platform"),
                        f"{service['service_id']}-endpoint-{index}",
                        service["service_id"],
                        str(upstream),
                        service.get("protocol", "http"),
                        service.get("method", "ANY"),
                        "active",
                        f"endpoint:{service['service_id']}:{index}",
                        timestamp,
                        timestamp,
                    ),
                )

    def _save_routes(self, routes: dict, *, timestamp: str) -> None:
        for route in routes.values():
            self.connection.execute(
                """
                INSERT INTO api_gateway_mesh_service_route (
                    tenant, route_id, service_id, host, path, method, protocol,
                    status, audit_hash, created_at, updated_at
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    route.get("tenant", "platform"),
                    route["route_id"],
                    route["service_id"],
                    route.get("host", ""),
                    route.get("path", "/"),
                    route.get("method", "GET"),
                    route.get("protocol", "http"),
                    route.get("status", "draft"),
                    route.get("route_hash", f"route:{route['route_id']}"),
                    timestamp,
                    timestamp,
                ),
            )
            self.connection.execute(
                """
                INSERT INTO api_gateway_mesh_route_version (
                    tenant, route_version_id, route_id, version, route_hash,
                    canary_percent, status, audit_hash, created_at, updated_at
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    route.get("tenant", "platform"),
                    f"{route['route_id']}:{route.get('version', 'v1')}",
                    route["route_id"],
                    _normalized_version(route.get("version")),
                    route.get("route_hash", f"route:{route['route_id']}"),
                    float(route.get("canary_percent", 0)),
                    route.get("status", "draft"),
                    f"route-version:{route['route_id']}",
                    timestamp,
                    timestamp,
                ),
            )

    def _save_rate_limits(self, rate_limits: dict, *, timestamp: str) -> None:
        for policy in rate_limits.values():
            self.connection.execute(
                """
                INSERT INTO api_gateway_mesh_rate_limit_policy (
                    tenant, policy_id, route_id, limit_per_minute, burst, scope,
                    status, audit_hash, created_at, updated_at
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    policy.get("tenant", "platform"),
                    policy["policy_id"],
                    policy["route_id"],
                    int(policy.get("limit_per_minute", 0)),
                    int(policy.get("burst", 0)),
                    policy.get("scope", "tenant"),
                    policy.get("status", "active"),
                    f"rate-limit:{policy['policy_id']}",
                    timestamp,
                    timestamp,
                ),
            )

    def _save_identities(self, identities: dict, *, timestamp: str) -> None:
        for identity in identities.values():
            self.connection.execute(
                """
                INSERT INTO api_gateway_mesh_mtls_identity (
                    tenant, identity_id, service_id, spiffe_id, issuer, verified,
                    status, audit_hash, created_at, updated_at
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    identity.get("tenant", "platform"),
                    identity["identity_id"],
                    identity["service_id"],
                    identity.get("spiffe_id", ""),
                    identity.get("issuer", ""),
                    1 if identity.get("verified", False) else 0,
                    identity.get("status", "draft"),
                    f"identity:{identity['identity_id']}",
                    timestamp,
                    timestamp,
                ),
            )

    def _save_health(self, records: dict, *, timestamp: str) -> None:
        for health in records.values():
            self.connection.execute(
                """
                INSERT INTO api_gateway_mesh_service_health (
                    tenant, health_id, service_id, latency_ms, error_rate, status,
                    recorded_at, audit_hash, created_at, updated_at
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    health.get("tenant", "platform"),
                    health["health_id"],
                    health["service_id"],
                    int(health.get("latency_ms", 0)),
                    float(health.get("error_rate", 0.0)),
                    health.get("status", "unknown"),
                    health.get("recorded_at", timestamp),
                    f"health:{health['health_id']}",
                    timestamp,
                    timestamp,
                ),
            )

    def _save_traffic(self, records: dict, *, timestamp: str) -> None:
        for sample in records.values():
            self.connection.execute(
                """
                INSERT INTO api_gateway_mesh_traffic_sample (
                    tenant, sample_id, route_id, requests, p95_ms, error_rate,
                    saturation, risk_score, audit_hash, created_at, updated_at
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    sample.get("tenant", "platform"),
                    sample["sample_id"],
                    sample["route_id"],
                    int(sample.get("requests", 0)),
                    float(sample.get("p95_ms", 0.0)),
                    float(sample.get("error_rate", 0.0)),
                    float(sample.get("saturation", 0.0)),
                    float(sample.get("risk_score", 0.0)),
                    f"traffic:{sample['sample_id']}",
                    timestamp,
                    timestamp,
                ),
            )

    def _save_retry_evidence(self, evidence_rows, *, timestamp: str) -> None:
        for index, evidence in enumerate(evidence_rows, start=1):
            self.connection.execute(
                """
                INSERT INTO api_gateway_mesh_gateway_retry_evidence (
                    tenant, retry_id, event_id, event_type, idempotency_key, attempts,
                    status, audit_hash, created_at, updated_at
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    evidence.get("tenant", "platform"),
                    evidence.get("retry_id", f"retry-{index}"),
                    evidence.get("event_id", f"event-{index}"),
                    evidence.get("event_type", "UnknownEvent"),
                    evidence.get("idempotency_key", f"retry:{index}"),
                    int(evidence.get("attempts", 1)),
                    evidence.get("status", "retrying"),
                    f"retry:{index}",
                    timestamp,
                    timestamp,
                ),
            )

    def _save_outbox(self, events, *, timestamp: str) -> None:
        for event in events:
            self.connection.execute(
                """
                INSERT INTO api_gateway_mesh_appgen_outbox_event (
                    tenant, event_id, event_type, topic, idempotency_key,
                    published_at, status, audit_hash, created_at, updated_at
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    event.get("payload", {}).get("tenant", "platform"),
                    event.get("event_id", "event"),
                    event.get("event_type", "UnknownEvent"),
                    event.get("topic", "appgen.gateway.events"),
                    event.get("idempotency_key", f"outbox:{event.get('event_id', 'event')}"),
                    event.get("published_at", timestamp),
                    event.get("status", "pending"),
                    event.get("hash", f"outbox:{event.get('event_id', 'event')}"),
                    timestamp,
                    timestamp,
                ),
            )

    def _save_inbox(self, events, *, timestamp: str) -> None:
        for event in events:
            self.connection.execute(
                """
                INSERT INTO api_gateway_mesh_appgen_inbox_event (
                    tenant, event_id, event_type, idempotency_key, attempts, status,
                    received_at, audit_hash, created_at, updated_at
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    event.get("tenant", "platform"),
                    event.get("event_id", "event"),
                    event.get("event_type", "UnknownEvent"),
                    event.get("idempotency_key", f"inbox:{event.get('event_id', 'event')}"),
                    int(event.get("attempts", 1)),
                    event.get("status", "processed"),
                    event.get("received_at", timestamp),
                    f"inbox:{event.get('event_id', 'event')}",
                    timestamp,
                    timestamp,
                ),
            )

    def _save_dead_letters(self, events, *, timestamp: str) -> None:
        for event in events:
            self.connection.execute(
                """
                INSERT INTO api_gateway_mesh_dead_letter_event (
                    tenant, event_id, event_type, idempotency_key, attempts, reason,
                    status, audit_hash, created_at, updated_at
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    event.get("tenant", "platform"),
                    event.get("event_id", "event"),
                    event.get("event_type", "UnknownEvent"),
                    event.get("idempotency_key", f"dead-letter:{event.get('event_id', 'event')}"),
                    int(event.get("attempts", 1)),
                    event.get("reason", "unknown"),
                    event.get("status", "dead_letter"),
                    f"dead-letter:{event.get('event_id', 'event')}",
                    timestamp,
                    timestamp,
                ),
            )


def repository_manifest() -> dict:
    repository = ApiGatewayMeshRepository()
    try:
        applied = repository.apply_migrations()
        manifest = repository.database_manifest()
    finally:
        repository.close()
    return {
        "ok": bool(applied) and manifest["ok"],
        "migrations_applied": applied,
        "database": manifest,
        "side_effects": (),
    }


def smoke_test() -> dict:
    repository = ApiGatewayMeshRepository()
    try:
        applied = repository.apply_migrations()
        state = {
            "configuration": {
                "database_backend": "postgresql",
                "event_topic": "appgen.gateway.events",
                "retry_limit": 3,
                "event_contract": "AppGen-X",
                "status": "active",
            },
            "parameters": {"default_rate_limit_per_minute": 900},
            "rules": {
                "gateway_rule": {
                    "rule_id": "gateway_rule",
                    "tenant": "tenant_smoke",
                    "rule_type": "routing",
                    "scope": "routing",
                    "compiled_hash": "compiled",
                    "enabled": True,
                    "status": "active",
                }
            },
            "services": {
                "svc_smoke": {
                    "service_id": "svc_smoke",
                    "tenant": "tenant_smoke",
                    "pbc": "api_gateway_mesh",
                    "name": "gateway-service",
                    "version": "v1",
                    "region": "us-east",
                    "status": "registered",
                    "upstreams": ("https://gateway",),
                }
            },
            "routes": {
                "route_smoke": {
                    "route_id": "route_smoke",
                    "tenant": "tenant_smoke",
                    "service_id": "svc_smoke",
                    "host": "api.example.com",
                    "path": "/smoke",
                    "method": "POST",
                    "protocol": "http",
                    "version": "v1",
                    "status": "published",
                    "canary_percent": 10,
                    "route_hash": "route-hash",
                }
            },
            "rate_limits": {},
            "identities": {},
            "health": {},
            "traffic": {},
            "retry_evidence": (),
            "outbox": (),
            "inbox": (),
            "dead_letter": (),
        }
        persisted = repository.save_runtime_state(state)
        loaded = repository.load_runtime_state()
        services = repository.list_services(tenant="tenant_smoke")
        routes = repository.list_routes(tenant="tenant_smoke")
    finally:
        repository.close()
    return {
        "ok": bool(applied)
        and persisted["ok"]
        and loaded.get("routes", {}).get("route_smoke", {}).get("status") == "published"
        and len(services) == 1
        and len(routes) == 1,
        "applied": applied,
        "persisted": persisted,
        "loaded": loaded,
        "services": services,
        "routes": routes,
        "side_effects": (),
    }
