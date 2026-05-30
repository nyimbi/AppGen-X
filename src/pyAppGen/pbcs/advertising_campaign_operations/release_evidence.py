"""Release evidence for the advertising campaign standalone slice."""

from __future__ import annotations

from .agent import chatbot_interface_contract
from .config import configuration_manifest
from .events import event_contract_manifest
from .handlers import handler_manifest
from .models import model_contracts
from .permissions import permission_manifest
from .routes import api_route_contracts
from .schema_contract import build_schema_contract
from .service_contract import build_service_contract
from .ui import advertising_campaign_operations_standalone_app_contract
from .ui import advertising_campaign_operations_ui_contract
from .workflows import workflow_catalog


def build_release_evidence(state: dict | None = None) -> dict:
    schema = build_schema_contract()
    service = build_service_contract()
    routes = api_route_contracts()
    permissions = permission_manifest()
    ui_contract = advertising_campaign_operations_ui_contract()
    assistant = chatbot_interface_contract()
    workflows = workflow_catalog()
    return {
        "format": "appgen.advertising-campaign-operations-release-evidence.v2",
        "ok": all(
            item["ok"]
            for item in (
                schema,
                service,
                routes,
                permissions,
                configuration_manifest(),
                event_contract_manifest(),
                handler_manifest(),
                ui_contract,
                assistant,
                workflows,
                model_contracts(),
                advertising_campaign_operations_standalone_app_contract(),
            )
        ),
        "pbc": "advertising_campaign_operations",
        "checks": (
            {"id": "models_schema_contracts", "ok": schema["ok"] and model_contracts()["ok"]},
            {"id": "services_and_routes", "ok": service["ok"] and routes["ok"]},
            {"id": "permissions_and_configuration", "ok": permissions["ok"] and configuration_manifest()["ok"]},
            {"id": "assistant_document_planning", "ok": assistant["ok"]},
            {"id": "ui_forms_wizards_controls", "ok": ui_contract["ok"]},
            {"id": "workflow_catalog", "ok": workflows["ok"]},
            {"id": "events_and_handlers", "ok": event_contract_manifest()["ok"] and handler_manifest()["ok"]},
        ),
        "state_summary": {
            "campaign_plan_count": len((state or {}).get("campaign_plans", {})),
            "outbox_event_count": len((state or {}).get("outbox", ())),
            "configured": bool((state or {}).get("configuration")),
        },
        "validation_commands": (
            "./.venv/bin/python -m py_compile src/pyAppGen/pbcs/advertising_campaign_operations/*.py src/pyAppGen/pbcs/advertising_campaign_operations/tests/*.py",
            "./.venv/bin/pytest src/pyAppGen/pbcs/advertising_campaign_operations/tests",
        ),
        "side_effects": (),
    }


def release_readiness_manifest() -> dict:
    evidence = build_release_evidence()
    return {
        "ok": evidence["ok"],
        "pbc": evidence["pbc"],
        "sections": (
            "models",
            "schema",
            "services",
            "routes",
            "events",
            "handlers",
            "permissions",
            "configuration",
            "ui",
            "assistant",
            "workflows",
            "standalone",
        ),
        "blocking_gaps": tuple(check["id"] for check in evidence["checks"] if not check["ok"]),
        "boundary_gaps": (),
        "evidence": evidence,
        "side_effects": (),
    }


def validate_release_evidence() -> dict:
    manifest = release_readiness_manifest()
    failed_checks = tuple(check["id"] for check in manifest["evidence"]["checks"] if not check["ok"])
    return {
        "ok": manifest["ok"] and not failed_checks,
        "pbc": manifest["pbc"],
        "missing_sections": (),
        "failed_checks": failed_checks,
        "boundary_gaps": (),
        "side_effects": (),
    }


def smoke_test() -> dict:
    manifest = release_readiness_manifest()
    validation = validate_release_evidence()
    return {
        "ok": manifest["ok"] and validation["ok"],
        "manifest": manifest,
        "validation": validation,
        "side_effects": (),
    }
