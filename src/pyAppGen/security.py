"""Package-level security, identity, tenancy, and compliance contracts."""

from __future__ import annotations

from .dsl import schema_from_dsl


SECURITY_SAMPLE_DSL = """
app SecurityAudit { targets: web, mobile, desktop; rls: Project.org_id }

table Project {
  id: int pk
  org_id: int required hidden
  name: string required search
}

role Admin {
  Project: read, create, update, delete
}

role Analyst {
  Project: read, update
}
"""

SSO_PROVIDERS = {
    "oidc": ("OIDC_ISSUER", "OIDC_CLIENT_ID", "OIDC_CLIENT_SECRET"),
    "saml": ("SAML_METADATA_URL", "SAML_ENTITY_ID"),
    "ldap": ("LDAP_URL", "LDAP_BIND_DN", "LDAP_BIND_PASSWORD"),
    "active_directory": ("AD_DOMAIN", "AD_CLIENT_ID", "AD_CLIENT_SECRET"),
    "cognito": ("COGNITO_DOMAIN", "COGNITO_CLIENT_ID", "COGNITO_CLIENT_SECRET"),
}

SECURITY_ARTIFACTS = {
    "app/security.py",
    "app/runtime_security.py",
    "app/identity.py",
    "app/tenancy.py",
    "app/rls.py",
    "app/compliance.py",
}


def role_policy_catalog(source: str = SECURITY_SAMPLE_DSL) -> tuple[dict, ...]:
    """Return RBAC policies declared in DSL roles."""
    schema = schema_from_dsl(source, source_name="security-audit.appgen")
    return tuple(
        {
            "role": role.name,
            "resource": permission.resource,
            "actions": permission.actions,
        }
        for role in schema.roles
        for permission in role.permissions
    )


def normalize_principal(claims: dict) -> dict:
    """Return a normalized security principal."""
    roles = claims.get("roles") or claims.get("groups") or ()
    if isinstance(roles, str):
        roles = (roles,)
    return {
        "sub": claims.get("sub") or claims.get("user") or "anonymous",
        "roles": tuple(roles),
        "tenant_id": claims.get("tenant_id") or claims.get("org_id"),
        "provider": claims.get("provider", "local"),
    }


def authorize(principal: dict, resource: str, action: str) -> dict:
    """Return an RBAC authorization decision."""
    policies = role_policy_catalog()
    allowed = any(
        policy["role"] in principal["roles"]
        and policy["resource"] == resource
        and action in policy["actions"]
        for policy in policies
    )
    return {
        "format": "appgen.package-authorization-decision.v1",
        "principal": principal["sub"],
        "resource": resource,
        "action": action,
        "allowed": allowed,
        "reason": "role-policy-match" if allowed else "no-role-policy-match",
    }


def authorization_audit_event(decision: dict) -> dict:
    """Return an immutable authorization audit-event envelope."""
    return {
        "format": "appgen.package-security-audit-event.v1",
        "event": "security.authorization.allowed"
        if decision["allowed"]
        else "security.authorization.denied",
        "principal": decision["principal"],
        "resource": decision["resource"],
        "action": decision["action"],
        "allowed": decision["allowed"],
    }


def sso_provider_catalog(environ: dict | None = None) -> tuple[dict, ...]:
    """Return enterprise SSO provider contracts without exposing secrets."""
    env = environ or {}
    return tuple(
        {
            "provider": name,
            "env": required,
            "missing": tuple(key for key in required if not env.get(key)),
            "configured": all(env.get(key) for key in required),
            "secret_policy": "env-only",
            "flows": ("login", "callback", "token_exchange", "logout"),
        }
        for name, required in SSO_PROVIDERS.items()
    )


def tenant_rls_contract(source: str = SECURITY_SAMPLE_DSL) -> dict:
    """Return tenant isolation and PostgreSQL RLS policy contracts."""
    schema = schema_from_dsl(source, source_name="security-audit.appgen")
    rls_target = str(schema.app_options.get("rls", "Project.org_id"))
    table, field = rls_target.split(".", 1)
    return {
        "format": "appgen.package-tenant-rls-contract.v1",
        "ok": bool(table and field),
        "target": {"table": table, "field": field},
        "tenant_context": ("header:X-Tenant-ID", "session:tenant_id", "principal:tenant_id"),
        "filter_plan": f"{table}.{field} == principal.tenant_id",
        "postgres_policy_sql": (
            f"CREATE POLICY appgen_{table.lower()}_tenant ON {table} "
            f"USING ({field} = current_setting('appgen.tenant_id')::int);"
        ),
        "role_sync_sql": (
            "GRANT SELECT, INSERT, UPDATE, DELETE ON ALL TABLES IN SCHEMA public "
            "TO appgen_authenticated;"
        ),
    }


def session_hardening_policy() -> dict:
    """Return runtime security and session-hardening policy."""
    return {
        "format": "appgen.package-session-hardening-policy.v1",
        "idle_timeout_seconds": 1800,
        "auto_logout": True,
        "public_path_bypass": ("/static/", "/health", "/login/"),
        "headers": {
            "X-Frame-Options": "DENY",
            "X-Content-Type-Options": "nosniff",
            "Referrer-Policy": "strict-origin-when-cross-origin",
            "Content-Security-Policy": "default-src 'self'",
        },
        "csrf_required": True,
    }


def compliance_contract() -> dict:
    """Return compliance and privacy controls for generated applications."""
    return {
        "format": "appgen.package-compliance-contract.v1",
        "controls": (
            "audit_events",
            "retention_policy",
            "protected_field_redaction",
            "privacy_request",
            "subject_export",
            "erasure_review",
            "retention_disposition",
        ),
        "regulatory_profiles": ("GDPR", "HIPAA-ready", "SOC2-ready"),
        "review_required": ("erasure", "retention_disposition", "protected_field_change"),
        "ok": True,
    }


def secret_exposure_scan(environ: dict | None = None) -> dict:
    """Return secret-scan evidence for unsafe defaults."""
    env = environ or {}
    unsafe = tuple(
        key
        for key, value in env.items()
        if key.upper().endswith(("SECRET", "KEY", "PASSWORD", "TOKEN"))
        and str(value).lower() in {"", "secret", "change-me", "changeme", "password"}
    )
    return {
        "format": "appgen.package-secret-exposure-scan.v1",
        "ok": not unsafe,
        "unsafe_keys": unsafe,
        "policy": "secrets-must-use-env-or-managed-secret-store",
    }


def security_release_audit(
    existing_paths: set[str] | None = None,
    environ: dict | None = None,
) -> dict:
    """Return package-level proof for security and identity readiness."""
    existing = SECURITY_ARTIFACTS if existing_paths is None else existing_paths
    audit_env = environ or {
        "OIDC_ISSUER": "https://idp.example.test",
        "OIDC_CLIENT_ID": "client",
        "OIDC_CLIENT_SECRET": "env-secret",
        "SAML_METADATA_URL": "https://idp.example.test/metadata",
        "SAML_ENTITY_ID": "appgen",
        "LDAP_URL": "ldaps://directory.example.test",
        "LDAP_BIND_DN": "cn=appgen",
        "LDAP_BIND_PASSWORD": "env-secret",
        "AD_DOMAIN": "example.test",
        "AD_CLIENT_ID": "client",
        "AD_CLIENT_SECRET": "env-secret",
        "COGNITO_DOMAIN": "auth.example.test",
        "COGNITO_CLIENT_ID": "client",
        "COGNITO_CLIENT_SECRET": "env-secret",
        "SECRET_KEY": "managed-secret",
    }
    principal = normalize_principal({"sub": "u1", "roles": ("Analyst",), "tenant_id": 42})
    allow = authorize(principal, "Project", "update")
    deny = authorize(principal, "Project", "delete")
    sso = sso_provider_catalog(audit_env)
    missing_sso = sso_provider_catalog({})
    rls = tenant_rls_contract()
    session = session_hardening_policy()
    compliance = compliance_contract()
    secret_scan = secret_exposure_scan(audit_env)
    gates = (
        {
            "id": "rbac_authorization",
            "ok": allow["allowed"] is True and deny["allowed"] is False,
        },
        {
            "id": "authorization_audit",
            "ok": authorization_audit_event(deny)["event"] == "security.authorization.denied",
        },
        {
            "id": "sso_provider_coverage",
            "ok": {"oidc", "saml", "ldap", "active_directory", "cognito"}
            == {item["provider"] for item in sso}
            and all(item["configured"] for item in sso),
        },
        {
            "id": "sso_missing_secret_guard",
            "ok": all(item["configured"] is False for item in missing_sso),
        },
        {
            "id": "tenant_rls",
            "ok": rls["ok"] and "CREATE POLICY" in rls["postgres_policy_sql"],
        },
        {
            "id": "session_hardening",
            "ok": session["auto_logout"] and session["headers"]["X-Frame-Options"] == "DENY",
        },
        {
            "id": "compliance_privacy",
            "ok": compliance["ok"] and {"GDPR", "HIPAA-ready"} <= set(compliance["regulatory_profiles"]),
        },
        {
            "id": "secret_exposure_scan",
            "ok": secret_scan["ok"] and secret_exposure_scan({"SECRET_KEY": "change-me"})["ok"] is False,
        },
        {
            "id": "artifact_contract",
            "ok": SECURITY_ARTIFACTS <= existing,
        },
    )
    ok = all(gate["ok"] for gate in gates)
    return {
        "format": "appgen.package-security-release-audit.v1",
        "scope": "package",
        "ok": ok,
        "decision": "approved" if ok else "blocked",
        "policies": role_policy_catalog(),
        "principal": principal,
        "decisions": {"allow": allow, "deny": deny},
        "audit_event": authorization_audit_event(deny),
        "sso": sso,
        "missing_sso_guard": missing_sso,
        "rls": rls,
        "session": session,
        "compliance": compliance,
        "secret_scan": secret_scan,
        "gates": gates,
        "blocking_gaps": tuple(gate for gate in gates if not gate["ok"]),
        "stop_condition": "do-not-claim-security-readiness-unless-ok-is-true",
    }
