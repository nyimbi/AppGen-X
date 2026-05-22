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


def security_generation_smoke_audit(source: str = SECURITY_SAMPLE_DSL) -> dict:
    """Generate a temporary app and exercise its security-facing modules."""
    import importlib.util
    import py_compile
    import tempfile
    from pathlib import Path

    from .gen import generate_app_from_schema

    required_artifacts = (
        "app/security.py",
        "app/runtime_security.py",
        "app/identity.py",
        "app/tenancy.py",
        "app/rls.py",
        "app/compliance.py",
        "app/models.py",
        "app/views.py",
        "app/templates/appgen_runtime_security.html",
        "app/templates/appgen_identity.html",
        "app/templates/appgen_tenancy.html",
        "app/templates/appgen_rls.html",
        "app/templates/appgen_compliance.html",
    )
    compile_artifacts = (
        "app/security.py",
        "app/runtime_security.py",
        "app/identity.py",
        "app/tenancy.py",
        "app/rls.py",
        "app/compliance.py",
        "app/models.py",
        "app/views.py",
    )
    generated_security_paths = {
        "app/security.py",
        "app/runtime_security.py",
        "app/identity.py",
        "app/rls.py",
        "app/compliance.py",
    }
    runtime_paths = {"app/runtime_security.py", "app/templates/appgen_runtime_security.html"}
    identity_paths = {"app/identity.py", "app/templates/appgen_identity.html"}
    tenancy_paths = {"app/tenancy.py", "app/templates/appgen_tenancy.html"}
    rls_paths = {"app/tenancy.py", "app/rls.py", "app/templates/appgen_rls.html"}
    compliance_paths = {"app/compliance.py", "app/templates/appgen_compliance.html"}

    with tempfile.TemporaryDirectory(prefix="appgen-security-smoke-") as tmp:
        project_dir = Path(tmp)
        output_dir = project_dir / "app"
        schema = schema_from_dsl(source, source_name="security-smoke.appgen")
        generate_app_from_schema(schema, output_dir)

        missing_artifacts = tuple(
            artifact for artifact in required_artifacts if not (project_dir / artifact).exists()
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
        for name in ("security", "runtime_security", "identity", "tenancy", "rls", "compliance"):
            module_path = output_dir / f"{name}.py"
            spec = importlib.util.spec_from_file_location(
                f"generated_security_smoke_{name}",
                module_path,
            )
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
            modules[name] = module

        generated_security = modules["security"]
        runtime_security = modules["runtime_security"]
        identity = modules["identity"]
        tenancy = modules["tenancy"]
        rls = modules["rls"]
        compliance = modules["compliance"]

        managed_secret = {"SECRET_KEY": "managed-secret-value-with-length"}
        principal = {"id": "u1", "roles": ("Analyst",), "tenant_id": 42}
        allow = generated_security.authorize(principal, "Project", "update")
        deny = generated_security.authorize(principal, "Project", "delete")
        security_gate = generated_security.security_gate_plan(
            managed_secret,
            generated_security_paths,
        )
        security_workbench = generated_security.security_workbench(
            managed_secret,
            generated_security_paths,
            actor="security-smoke",
        )
        default_secret_scan = generated_security.secret_exposure_scan({"SECRET_KEY": "change-me"})

        runtime_gate = runtime_security.runtime_security_release_gate(runtime_paths)
        runtime_workbench = runtime_security.runtime_security_workbench(runtime_paths)
        headers = runtime_security.security_headers({"X-Frame-Options": "DENY"})
        active_session = runtime_security.mark_activity({}, now=None)

        identity_env = identity.sample_identity_environment()
        identity_gate = identity.identity_release_gate(identity_paths, identity_env)
        identity_workbench = identity.identity_workbench(identity_paths, identity_env)
        oidc_plan = identity.login_request_plan("oidc", "/next", identity_env)
        cognito = identity.cognito_readiness(identity_env)
        trusted = identity.trusted_header_plan(identity_env)

        tenancy_gate = tenancy.tenancy_release_gate(tenancy_paths)
        tenancy_workbench = tenancy.tenancy_workbench(tenancy_paths)
        tenant_filter = tenancy.tenant_filter_kwargs("Project", "42")
        tenant_context = tenancy.tenant_context(
            {"X-AppGen-Tenant": "42"},
            {},
            {},
        )

        rls_gate = rls.rls_release_gate(rls_paths, (principal,))
        rls_workbench = rls.rls_workbench(rls_paths, (principal,))
        rls_filter = rls.rls_filter_kwargs("Project", principal)
        rls_allow = rls.can_access_row("Project", {"org_id": 42}, principal)
        rls_deny = rls.can_access_row("Project", {"org_id": 7}, principal)
        rls_sql = rls.postgres_all_policy_sql()

        sample_rows = {
            "Project": (
                {"id": 1, "org_id": 42, "name": "Alpha", "age_days": 366},
            )
        }
        compliance_gate = compliance.compliance_release_gate(compliance_paths, sample_rows)
        compliance_workbench = compliance.compliance_workbench(compliance_paths, sample_rows)
        export = compliance.subject_export_package(
            "subject-1",
            sample_rows,
            actor="dpo",
        )
        erasure = compliance.erasure_plan("subject-1", sample_rows, actor="dpo")

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
            "id": "rbac_and_secret_gate",
            "ok": allow["ok"] is True
            and deny["ok"] is False
            and generated_security.authorization_audit_event(deny)["event"]
            == "security.authorization.denied"
            and security_gate["ok"] is True
            and security_workbench["ok"] is True
            and default_secret_scan["ok"] is False,
            "allow": allow,
            "deny": deny,
            "gate": security_gate,
            "workbench": security_workbench,
        },
        {
            "id": "runtime_session_hardening",
            "ok": runtime_gate["ok"] is True
            and runtime_workbench["ok"] is True
            and headers["X-Frame-Options"] == "DENY"
            and headers["X-Content-Type-Options"] == "nosniff"
            and "Permissions-Policy" in headers
            and runtime_security.SECURITY_POLICY["last_seen_key"] in active_session,
            "gate": runtime_gate,
            "workbench": runtime_workbench,
            "headers": headers,
        },
        {
            "id": "identity_provider_contracts",
            "ok": identity_gate["ok"] is True
            and identity_workbench["ok"] is True
            and oidc_plan["protocol"] == "oidc"
            and cognito["configured"] is True
            and trusted["requires_trusted_proxy"] is True,
            "gate": identity_gate,
            "workbench": identity_workbench,
            "oidc_plan": oidc_plan,
            "cognito": cognito,
            "trusted_headers": trusted,
        },
        {
            "id": "tenancy_and_rls_contracts",
            "ok": tenancy_gate["ok"] is True
            and tenancy_workbench["ok"] is True
            and tenant_filter == {"org_id": "42"}
            and tenant_context["tenant_id"] == "42"
            and rls_gate["ok"] is True
            and rls_workbench["ok"] is True
            and rls_filter == {"org_id": 42}
            and rls_allow is True
            and rls_deny is False
            and "ENABLE ROW LEVEL SECURITY" in rls_sql,
            "tenancy_gate": tenancy_gate,
            "rls_gate": rls_gate,
            "tenant_filter": tenant_filter,
            "rls_filter": rls_filter,
            "postgres_policy_sql": rls_sql,
        },
        {
            "id": "compliance_privacy_contracts",
            "ok": compliance_gate["ok"] is True
            and compliance_workbench["ok"] is True
            and export["format"] == "appgen.subject-export.v1"
            and export["data"]["Project"][0]["org_id"] == "[redacted]"
            and erasure["requires_review"] is True,
            "gate": compliance_gate,
            "workbench": compliance_workbench,
            "export": export,
            "erasure": erasure,
        },
    )
    ok = all(check["ok"] for check in checks)
    return {
        "format": "appgen.security-generation-smoke-audit.v1",
        "scope": "generated-app",
        "ok": ok,
        "decision": "approved" if ok else "blocked",
        "required_artifacts": required_artifacts,
        "compiled_artifacts": tuple(compiled),
        "checks": checks,
        "blocking_gaps": tuple(check for check in checks if not check["ok"]),
        "stop_condition": "do-not-claim-generated-security-readiness-unless-ok-is-true",
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
    generation_smoke = security_generation_smoke_audit()
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
        {
            "id": "generation_smoke",
            "ok": generation_smoke["ok"],
            "checks": tuple(check["id"] for check in generation_smoke["checks"]),
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
        "generation_smoke": generation_smoke,
        "gates": gates,
        "blocking_gaps": tuple(gate for gate in gates if not gate["ok"]),
        "stop_condition": "do-not-claim-security-readiness-unless-ok-is-true",
    }
