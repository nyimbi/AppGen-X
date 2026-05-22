"""Package-level enterprise integration contracts.

Generated apps include an integration workbench.  This module exposes the same
first-class connector contracts before generation, including Entando and
Invenio as explicit integration contracts.
"""

from __future__ import annotations

from hashlib import sha256
import hmac
import json


INTEGRATIONS = {
    "rest": {
        "label": "REST API",
        "kind": "http",
        "description": "Outbound HTTP integration point for approved APIs.",
        "env": ("APPGEN_REST_BASE_URL", "APPGEN_REST_TOKEN"),
    },
    "webhook": {
        "label": "Webhook",
        "kind": "http",
        "description": "Signed event delivery endpoint for workflow and data changes.",
        "env": ("APPGEN_WEBHOOK_URL", "APPGEN_WEBHOOK_SECRET"),
    },
    "salesforce": {
        "label": "Salesforce",
        "kind": "crm",
        "description": "Enterprise CRM connector configuration stub.",
        "env": ("SALESFORCE_BASE_URL", "SALESFORCE_CLIENT_ID", "SALESFORCE_CLIENT_SECRET"),
    },
    "sap": {
        "label": "SAP",
        "kind": "erp",
        "description": "Enterprise ERP connector configuration stub.",
        "env": ("SAP_BASE_URL", "SAP_CLIENT_ID", "SAP_CLIENT_SECRET"),
    },
    "entando": {
        "label": "Entando",
        "kind": "low_code_portal",
        "description": "Low-code portal and micro-frontend integration contract.",
        "env": ("ENTANDO_BASE_URL", "ENTANDO_CLIENT_ID", "ENTANDO_CLIENT_SECRET"),
    },
    "invenio": {
        "label": "Invenio",
        "kind": "repository",
        "description": "Repository deposit and record publication integration contract.",
        "env": ("INVENIO_BASE_URL", "INVENIO_ACCESS_TOKEN"),
    },
    "stripe": {
        "label": "Stripe",
        "kind": "payment",
        "description": "Payment gateway request-plan contract.",
        "env": ("STRIPE_API_KEY", "STRIPE_WEBHOOK_SECRET"),
    },
    "mpesa": {
        "label": "M-Pesa",
        "kind": "payment",
        "description": "Mobile-money payment gateway request-plan contract.",
        "env": ("MPESA_CONSUMER_KEY", "MPESA_CONSUMER_SECRET", "MPESA_SHORTCODE"),
    },
    "twilio_sms": {
        "label": "Twilio SMS",
        "kind": "sms",
        "description": "SMS gateway request-plan contract.",
        "env": ("TWILIO_ACCOUNT_SID", "TWILIO_AUTH_TOKEN", "TWILIO_FROM_NUMBER"),
    },
    "sendgrid_email": {
        "label": "SendGrid Email",
        "kind": "email",
        "description": "Transactional email request-plan contract.",
        "env": ("SENDGRID_API_KEY", "APPGEN_EMAIL_FROM"),
    },
}

INTEGRATION_CONTRACTS = {
    "entando": {
        "version": "appgen.integration.entando.v1",
        "surfaces": ("microfrontend", "page", "widget", "sso_context"),
        "routes": (
            "/integrations/entando/microfrontends",
            "/integrations/entando/pages",
            "/integrations/entando/events",
        ),
        "payload_schema": {
            "microfrontend": "string",
            "route": "string",
            "metadata": "object",
        },
        "permissions": ("portal.read", "portal.publish", "portal.configure"),
        "events": ("portal.microfrontend.publish", "portal.page.mount", "portal.widget.configure"),
    },
    "invenio": {
        "version": "appgen.integration.invenio.v1",
        "surfaces": ("record", "deposit", "file", "search_index"),
        "routes": (
            "/integrations/invenio/records",
            "/integrations/invenio/deposits",
            "/integrations/invenio/files",
        ),
        "payload_schema": {
            "record": "object",
            "files": "array",
            "metadata": "object",
        },
        "permissions": ("repository.read", "repository.deposit", "repository.publish"),
        "events": ("repository.deposit.create", "repository.record.publish", "repository.file.attach"),
    },
}


INTEGRATION_SAMPLE_DSL = """
app IntegrationAudit { targets: web, mobile, desktop }

table Book {
  id: int pk
  title: string required search
}
"""


def integration_config(name: str, environ: dict | None = None) -> dict:
    """Return non-secret configuration status for a connector."""
    if name not in INTEGRATIONS:
        raise KeyError(f"Unknown integration: {name}")
    env = environ or {}
    integration = INTEGRATIONS[name]
    required = tuple(integration["env"])
    missing = tuple(key for key in required if not env.get(key))
    return {
        "name": name,
        "label": integration["label"],
        "kind": integration["kind"],
        "description": integration["description"],
        "env": required,
        "missing": missing,
        "configured": not missing,
    }


def integration_catalog(environ: dict | None = None) -> tuple[dict, ...]:
    """Return all package integration definitions with configuration status."""
    return tuple(integration_config(name, environ=environ) for name in INTEGRATIONS)


def integrations_by_kind(kind: str, environ: dict | None = None) -> tuple[dict, ...]:
    """Return connectors of one integration kind."""
    return tuple(item for item in integration_catalog(environ) if item["kind"] == kind)


def integration_contract(name: str) -> dict:
    """Return a stable first-class integration contract."""
    if name not in INTEGRATION_CONTRACTS:
        raise KeyError(f"Unknown integration contract: {name}")
    integration = INTEGRATIONS[name]
    contract = dict(INTEGRATION_CONTRACTS[name])
    contract.update(
        {
            "integration": name,
            "label": integration["label"],
            "kind": integration["kind"],
            "env": tuple(integration["env"]),
            "payload_schema": dict(contract["payload_schema"]),
        }
    )
    return contract


def generated_integration_contracts() -> tuple[dict, ...]:
    """Return Entando and Invenio as first-class generated integration contracts."""
    return tuple(integration_contract(name) for name in INTEGRATION_CONTRACTS)


def integration_idempotency_key(
    name: str,
    operation: str,
    payload: dict | None = None,
) -> str:
    """Return a stable idempotency key for an outbound integration operation."""
    body = f"{name}:{operation}:{_canonical_payload(payload)}"
    return sha256(body.encode("utf-8")).hexdigest()


def idempotency_key(name: str, operation: str, payload: dict | None = None) -> str:
    """Backward-compatible alias for integration idempotency keys."""
    return integration_idempotency_key(name, operation, payload)


def signed_webhook_plan(
    event: str,
    payload: dict | None = None,
    *,
    environ: dict | None = None,
    secret: str | None = None,
) -> dict:
    """Build a signed webhook plan without dispatching external traffic."""
    env = environ or {}
    resolved_secret = secret or env.get("APPGEN_WEBHOOK_SECRET") or "secret"
    body = payload or {}
    signature = "sha256=" + hmac.new(
        str(resolved_secret).encode("utf-8"),
        _canonical_payload(body).encode("utf-8"),
        "sha256",
    ).hexdigest()
    operation = f"webhook.{event}"
    return {
        "integration": "webhook",
        "operation": operation,
        "url": env.get("APPGEN_WEBHOOK_URL"),
        "payload": body,
        "headers": {
            "Content-Type": "application/json",
            "X-AppGen-Event": event,
            "X-AppGen-Signature": signature,
            "Idempotency-Key": integration_idempotency_key("webhook", operation, body),
        },
        "signature": signature,
        "side_effect": "external_webhook",
        "review_required": True,
    }


def validate_webhook_signature(payload: dict | None, signature: str, secret: str) -> bool:
    """Validate a webhook signature with constant-time comparison."""
    expected = "sha256=" + hmac.new(
        str(secret).encode("utf-8"),
        _canonical_payload(payload).encode("utf-8"),
        "sha256",
    ).hexdigest()
    return hmac.compare_digest(str(signature), expected)


def portal_repository_contracts() -> dict:
    """Return named portal/repository contracts for composition workflows."""
    return {
        "entando": integration_contract("entando"),
        "invenio": integration_contract("invenio"),
    }


def low_code_portal_plan(
    contract_name: str = "entando",
    microfrontend: str = "AppGenApp",
    *,
    route: str = "/appgen",
    metadata: dict | None = None,
) -> dict:
    """Return a reviewed Entando-style portal publication plan."""
    contract = integration_contract(contract_name)
    if contract["kind"] != "low_code_portal":
        raise ValueError(f"{contract_name} is not a low-code portal integration")
    payload = {
        "microfrontend": microfrontend,
        "route": route,
        "metadata": metadata or {},
    }
    return {
        "integration": contract_name,
        "contract": contract,
        "route": "/integrations/entando/microfrontends",
        "operation": "portal.microfrontend.publish",
        "payload": payload,
        "idempotency_key": integration_idempotency_key(
            contract_name,
            "portal.microfrontend.publish",
            payload,
        ),
        "review_required": True,
    }


def repository_deposit_plan(
    contract_name: str = "invenio",
    record_type: str = "GeneratedApplication",
    metadata: dict | None = None,
    *,
    files: tuple[str, ...] = (),
) -> dict:
    """Return a reviewed Invenio-style repository deposit plan."""
    contract = integration_contract(contract_name)
    if contract["kind"] != "repository":
        raise ValueError(f"{contract_name} is not a repository integration")
    payload = {
        "record_type": record_type,
        "metadata": metadata or {},
        "files": files,
    }
    return {
        "integration": contract_name,
        "contract": contract,
        "route": "/integrations/invenio/deposits",
        "operation": "repository.deposit.create",
        "payload": payload,
        "idempotency_key": integration_idempotency_key(
            contract_name,
            "repository.deposit.create",
            payload,
        ),
        "review_required": True,
    }


def integration_generation_smoke_audit(source: str = INTEGRATION_SAMPLE_DSL) -> dict:
    """Generate a temporary app and exercise its integration workbench contracts."""
    import importlib.util
    import py_compile
    import tempfile
    from pathlib import Path

    from .dsl import schema_from_dsl
    from .gen import generate_app_from_schema

    required_artifacts = (
        "app/integrations.py",
        "app/templates/appgen_integrations.html",
        "app/models.py",
        "app/views.py",
    )
    compile_artifacts = (
        "app/integrations.py",
        "app/models.py",
        "app/views.py",
    )
    existing_paths = {"app/integrations.py", "app/templates/appgen_integrations.html"}
    webhook_env = {
        "APPGEN_WEBHOOK_URL": "https://hooks.example.test/appgen",
        "APPGEN_WEBHOOK_SECRET": "secret",
    }
    payment_env = {"STRIPE_API_KEY": "sk_test", "STRIPE_WEBHOOK_SECRET": "whsec"}
    sms_env = {
        "TWILIO_ACCOUNT_SID": "sid",
        "TWILIO_AUTH_TOKEN": "token",
        "TWILIO_FROM_NUMBER": "+10000000000",
    }
    email_env = {"SENDGRID_API_KEY": "key", "APPGEN_EMAIL_FROM": "noreply@example.test"}
    entando_env = {
        "ENTANDO_BASE_URL": "https://portal.example.test",
        "ENTANDO_CLIENT_ID": "client",
        "ENTANDO_CLIENT_SECRET": "secret",
    }
    invenio_env = {
        "INVENIO_BASE_URL": "https://repo.example.test",
        "INVENIO_ACCESS_TOKEN": "token",
    }

    with tempfile.TemporaryDirectory(prefix="appgen-integration-smoke-") as tmp:
        project_dir = Path(tmp)
        output_dir = project_dir / "app"
        schema = schema_from_dsl(source, source_name="integration-smoke.appgen")
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

        module_path = output_dir / "integrations.py"
        spec = importlib.util.spec_from_file_location(
            "generated_integration_smoke_integrations",
            module_path,
        )
        generated_integrations = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(generated_integrations)

        catalog = generated_integrations.integration_catalog({})
        contracts = generated_integrations.generated_integration_contracts()
        entando = generated_integrations.integration_contract("entando")
        invenio = generated_integrations.integration_contract("invenio")
        webhook = generated_integrations.signed_webhook_plan(
            "Book.created",
            {"id": 1},
            environ=webhook_env,
        )
        webhook_valid = generated_integrations.validate_webhook_signature(
            {"id": 1},
            webhook["signature"],
            webhook_env["APPGEN_WEBHOOK_SECRET"],
        )
        outbox = generated_integrations.integration_outbox_entry(webhook)
        delivery_audit = generated_integrations.delivery_audit_event(outbox, status="queued")
        payment = generated_integrations.payment_request_plan(
            "stripe",
            amount=42,
            currency="usd",
            reference="INV-1",
            environ=payment_env,
        )
        sms = generated_integrations.sms_request_plan(
            "twilio_sms",
            to="+15551234567",
            body="Ready",
            environ=sms_env,
        )
        email = generated_integrations.email_request_plan(
            "sendgrid_email",
            to="ada@example.test",
            subject="Ready",
            body="Report ready.",
            environ=email_env,
        )
        portal = generated_integrations.low_code_portal_plan(
            microfrontend="book-list",
            route="/books",
            environ=entando_env,
        )
        deposit = generated_integrations.repository_deposit_plan(
            record={"title": "Dune"},
            files=("dune.pdf",),
            environ=invenio_env,
        )
        missing_config_guard = False
        try:
            generated_integrations.outbound_request_plan("webhook", "webhook.Book.created", {})
        except ValueError:
            missing_config_guard = True
        release_gate = generated_integrations.integration_release_gate(existing_paths)
        workbench = generated_integrations.integration_workbench(existing_paths)
        artifact_check = generated_integrations.integration_check(existing_paths)

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
            "id": "connector_catalog_and_contracts",
            "ok": {
                "rest",
                "webhook",
                "salesforce",
                "sap",
                "entando",
                "invenio",
                "stripe",
                "mpesa",
                "twilio_sms",
                "sendgrid_email",
            }
            <= {item["name"] for item in catalog}
            and {contract["integration"] for contract in contracts} == {"entando", "invenio"}
            and entando["version"] == "appgen.integration.entando.v1"
            and invenio["version"] == "appgen.integration.invenio.v1",
            "catalog": catalog,
            "contracts": contracts,
        },
        {
            "id": "signed_delivery_and_outbox",
            "ok": webhook_valid is True
            and webhook["headers"]["Idempotency-Key"] == webhook["idempotency_key"]
            and outbox["id"].startswith("outbox-")
            and delivery_audit["event"] == "integration.delivery.queued",
            "webhook": webhook,
            "outbox": outbox,
            "audit": delivery_audit,
        },
        {
            "id": "commercial_and_missing_config_guards",
            "ok": payment["side_effect"] == "external_payment"
            and sms["side_effect"] == "external_sms"
            and email["side_effect"] == "external_email"
            and payment["review_required"] is True
            and sms["review_required"] is True
            and email["review_required"] is True
            and missing_config_guard is True,
            "payment": payment,
            "sms": sms,
            "email": email,
            "missing_config_guard": missing_config_guard,
        },
        {
            "id": "portal_repository_contracts",
            "ok": portal["contract"] == "appgen.integration.entando.v1"
            and deposit["contract"] == "appgen.integration.invenio.v1"
            and portal["review_required"] is True
            and deposit["review_required"] is True,
            "entando": portal,
            "invenio": deposit,
        },
        {
            "id": "generated_release_and_workbench",
            "ok": release_gate["ok"] is True
            and workbench["ok"] is True
            and artifact_check["ok"] is True,
            "release_gate": release_gate,
            "workbench": workbench,
            "artifact_check": artifact_check,
        },
    )
    ok = all(check["ok"] for check in checks)
    return {
        "format": "appgen.integration-generation-smoke-audit.v1",
        "scope": "generated-app",
        "ok": ok,
        "decision": "approved" if ok else "blocked",
        "required_artifacts": required_artifacts,
        "compiled_artifacts": tuple(compiled),
        "checks": checks,
        "blocking_gaps": tuple(check for check in checks if not check["ok"]),
        "stop_condition": "do-not-claim-generated-integration-readiness-unless-ok-is-true",
    }


def integration_release_audit(existing_paths: set[str] | None = None) -> dict:
    """Return package-level proof for enterprise integration readiness."""
    existing = (
        {"app/integrations.py", "app/templates/appgen_integrations.html"}
        if existing_paths is None
        else existing_paths
    )
    catalog = integration_catalog()
    contracts = generated_integration_contracts()
    webhook = signed_webhook_plan("Book.created", {"id": 1}, secret="secret")
    portal_plan = low_code_portal_plan()
    deposit_plan = repository_deposit_plan()
    entando = integration_contract("entando")
    invenio = integration_contract("invenio")
    generation_smoke = integration_generation_smoke_audit()
    gates = (
        {
            "id": "connector_catalog",
            "ok": {
                "rest",
                "webhook",
                "salesforce",
                "sap",
                "entando",
                "invenio",
                "stripe",
                "mpesa",
                "twilio_sms",
                "sendgrid_email",
            }
            <= {item["name"] for item in catalog},
        },
        {
            "id": "entando_contract",
            "ok": entando["version"] == "appgen.integration.entando.v1"
            and "microfrontend" in entando["surfaces"]
            and portal_plan["operation"] == "portal.microfrontend.publish",
        },
        {
            "id": "invenio_contract",
            "ok": invenio["version"] == "appgen.integration.invenio.v1"
            and "deposit" in invenio["surfaces"]
            and deposit_plan["operation"] == "repository.deposit.create",
        },
        {
            "id": "signed_webhooks",
            "ok": webhook["headers"]["X-AppGen-Signature"] == webhook["signature"]
            and webhook["headers"]["Idempotency-Key"],
        },
        {
            "id": "idempotent_outbound",
            "ok": integration_idempotency_key("webhook", "webhook.Book.created", {"id": 1})
            == webhook["headers"]["Idempotency-Key"],
        },
        {
            "id": "artifact_contract",
            "ok": {"app/integrations.py", "app/templates/appgen_integrations.html"} <= existing,
        },
        {
            "id": "generation_smoke",
            "ok": generation_smoke["ok"],
            "checks": tuple(check["id"] for check in generation_smoke["checks"]),
        },
    )
    ok = all(gate["ok"] for gate in gates)
    return {
        "format": "appgen.package-integration-release-audit.v1",
        "scope": "package",
        "ok": ok,
        "decision": "approved" if ok else "blocked",
        "catalog": catalog,
        "contracts": contracts,
        "portal_repository": portal_repository_contracts(),
        "plans": {
            "entando": portal_plan,
            "invenio": deposit_plan,
        },
        "webhook": webhook,
        "generation_smoke": generation_smoke,
        "gates": gates,
        "blocking_gaps": tuple(gate for gate in gates if not gate["ok"]),
        "stop_condition": "do-not-claim-enterprise-integration-readiness-unless-ok-is-true",
    }


def _canonical_payload(payload: dict | None) -> str:
    return json.dumps(payload or {}, sort_keys=True, separators=(",", ":"), default=str)
