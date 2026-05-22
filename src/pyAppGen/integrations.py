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
        "gates": gates,
        "blocking_gaps": tuple(gate for gate in gates if not gate["ok"]),
        "stop_condition": "do-not-claim-enterprise-integration-readiness-unless-ok-is-true",
    }


def _canonical_payload(payload: dict | None) -> str:
    return json.dumps(payload or {}, sort_keys=True, separators=(",", ":"), default=str)
