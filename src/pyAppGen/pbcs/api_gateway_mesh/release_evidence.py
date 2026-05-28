"""Generated release evidence for the api_gateway_mesh PBC."""

from __future__ import annotations

from pathlib import Path

from . import agent
from . import events
from . import services
from . import ui
from .runtime import API_GATEWAY_MESH_REQUIRED_EVENT_TOPIC
from .runtime import api_gateway_mesh_analyze_route_collisions
from .runtime import api_gateway_mesh_build_api_contract
from .runtime import api_gateway_mesh_build_release_evidence as runtime_release_evidence
from .runtime import api_gateway_mesh_build_route_publication_safety_case
from .runtime import api_gateway_mesh_build_schema_contract
from .runtime import api_gateway_mesh_build_service_contract
from .runtime import api_gateway_mesh_configure_runtime
from .runtime import api_gateway_mesh_empty_state
from .runtime import api_gateway_mesh_permissions_contract
from .runtime import api_gateway_mesh_publish_route
from .runtime import api_gateway_mesh_register_mtls_identity
from .runtime import api_gateway_mesh_register_rule
from .runtime import api_gateway_mesh_register_service
from .runtime import api_gateway_mesh_set_parameter


PBC_KEY = "api_gateway_mesh"


def _documentation_manifest() -> dict:
    base = Path(__file__).resolve().parent
    files = {
        "readme": base / "README.md",
        "implementation_plan": base / "implementation-plan.md",
        "implementation_status": base / "implementation-status.md",
    }
    present = {name: path.exists() for name, path in files.items()}
    return {
        "ok": all(present.values()),
        "files": {name: str(path) for name, path in files.items()},
        "present": present,
    }


def _execution_evidence() -> dict:
    state = api_gateway_mesh_empty_state()
    state = api_gateway_mesh_configure_runtime(
        state,
        {
            "database_backend": "postgresql",
            "event_topic": API_GATEWAY_MESH_REQUIRED_EVENT_TOPIC,
            "retry_limit": 3,
            "allowed_methods": ("GET", "POST"),
            "allowed_protocols": ("http",),
            "allowed_regions": ("us-east",),
            "default_timezone": "UTC",
            "workbench_limit": 50,
        },
    )["state"]
    state = api_gateway_mesh_set_parameter(state, "default_rate_limit_per_minute", 1000)["state"]
    state = api_gateway_mesh_register_rule(
        state,
        {
            "rule_id": "release_gate_rule",
            "tenant": "tenant_release",
            "rule_type": "routing",
            "allowed_methods": ("GET", "POST"),
            "allowed_protocols": ("http",),
            "required_identity": True,
            "blocked_paths": (),
            "status": "active",
        },
    )["state"]
    state = api_gateway_mesh_register_service(
        state,
        {
            "service_id": "svc_release",
            "tenant": "tenant_release",
            "pbc": "product_catalog_pim",
            "name": "catalog-api",
            "version": "v1",
            "region": "us-east",
            "upstreams": ("https://catalog-v1",),
        },
    )["state"]
    state = api_gateway_mesh_register_mtls_identity(
        state,
        {
            "identity_id": "mtls_release",
            "tenant": "tenant_release",
            "service_id": "svc_release",
            "spiffe_id": "spiffe://tenant/catalog",
            "issuer": "trusted_registry",
            "status": "active",
        },
    )["state"]
    published = api_gateway_mesh_publish_route(
        state,
        {
            "route_id": "route_primary",
            "tenant": "tenant_release",
            "service_id": "svc_release",
            "host": "api.example.com",
            "path": "/catalog",
            "method": "POST",
            "protocol": "http",
            "version": "v1",
            "canary_percent": 10,
        },
    )
    state = published["state"]
    conflicting_route = {
        "route_id": "route_conflict",
        "tenant": "tenant_release",
        "service_id": "svc_release",
        "host": "api.example.com",
        "path": "/catalog",
        "method": "POST",
        "protocol": "http",
        "version": "v2",
        "canary_percent": 15,
    }
    service_execution = services.ApiGatewayMeshService().build_route_publication_safety_case(
        {"state": state, **conflicting_route}
    )
    collision = api_gateway_mesh_analyze_route_collisions(state, conflicting_route)
    safety_case = api_gateway_mesh_build_route_publication_safety_case(state, conflicting_route)
    triage = agent.incident_triage_preview(state, tenant="tenant_release")
    return {
        "published": published,
        "service_execution": service_execution,
        "collision": collision,
        "safety_case": safety_case,
        "triage": triage,
    }


def build_release_evidence():
    """Return generated release audit evidence for this PBC."""
    runtime_evidence = runtime_release_evidence()
    ui_contract = ui.api_gateway_mesh_ui_contract()
    event_contract = events.event_contract_manifest()
    docs = _documentation_manifest()
    execution = _execution_evidence()
    checks = tuple(runtime_evidence.get("checks", ())) + (
        {
            "id": "service_execution_surface",
            "ok": execution["service_execution"]["executed"] is True
            and execution["service_execution"].get("runtime_result", {}).get("ready_to_publish") is False,
        },
        {"id": "route_publication_safety_case", "ok": execution["collision"]["blocking"] is True and "route_collision_free" in execution["safety_case"]["blocking_items"]},
        {"id": "ui_route_safety_binding", "ok": "RouteSafetyCasePanel" in ui_contract["fragments"] and "GatewayIncidentTriagePanel" in ui_contract["fragments"]},
        {"id": "appgen_x_contract_alignment", "ok": event_contract["required_event_topic"] == API_GATEWAY_MESH_REQUIRED_EVENT_TOPIC and event_contract["dead_letter_table"] == "api_gateway_mesh_dead_letter_event"},
        {"id": "implementation_documentation_present", "ok": docs["ok"]},
    )
    return {
        **runtime_evidence,
        "pbc": PBC_KEY,
        "schema": api_gateway_mesh_build_schema_contract(),
        "service": api_gateway_mesh_build_service_contract(),
        "api": api_gateway_mesh_build_api_contract(),
        "permissions": api_gateway_mesh_permissions_contract(),
        "ui_binding": ui_contract,
        "events": event_contract,
        "agent": {
            "skills": agent.agent_skill_manifest(),
            "chatbot": agent.chatbot_interface_contract(),
        },
        "documentation": docs,
        "execution": execution,
        "checks": checks,
        "ok": all(check["ok"] for check in checks),
        "blocking_gaps": tuple(check for check in checks if not check["ok"]),
    }


RELEASE_EVIDENCE = build_release_evidence()


def release_readiness_manifest():
    """Return side-effect-free release evidence coverage and gate metadata."""
    evidence = build_release_evidence()
    sections = tuple(
        name
        for name in ("schema", "service", "api", "permissions", "ui_binding", "events", "agent", "documentation")
        if isinstance(evidence.get(name), dict)
    )
    checks = tuple(evidence.get("checks", ()))
    return {
        "ok": evidence.get("ok") is True and bool(checks),
        "pbc": PBC_KEY,
        "format": evidence.get("format"),
        "sections": sections,
        "checks": checks,
        "blocking_gaps": tuple(evidence.get("blocking_gaps", ())),
        "required_sections": ("schema", "service", "api", "permissions", "ui_binding", "events", "documentation"),
        "evidence": evidence,
        "side_effects": (),
    }


def validate_release_evidence():
    """Validate release evidence, blocking gaps, and owned-boundary proof."""
    evidence = build_release_evidence()
    manifest = release_readiness_manifest()
    missing_sections = tuple(section for section in manifest["required_sections"] if section not in manifest["sections"])
    failed_checks = tuple(check for check in manifest["checks"] if check.get("ok") is not True)
    schema = evidence.get("schema", {}) if isinstance(evidence.get("schema"), dict) else {}
    service = evidence.get("service", {}) if isinstance(evidence.get("service"), dict) else {}
    ui_binding = evidence.get("ui_binding", {}) if isinstance(evidence.get("ui_binding"), dict) else {}
    docs = evidence.get("documentation", {}) if isinstance(evidence.get("documentation"), dict) else {}
    boundary_gaps = tuple(
        gap
        for gap, failed in (
            ("schema_shared_table_access", schema.get("shared_table_access") is not False),
            ("service_missing_command_methods", not bool(service.get("command_methods"))),
            ("ui_missing_route_safety_panel", "RouteSafetyCasePanel" not in tuple(ui_binding.get("fragments", ()))),
            ("documentation_missing", docs.get("ok") is not True),
        )
        if failed
    )
    return {
        "ok": manifest["ok"]
        and evidence.get("pbc") == manifest["pbc"]
        and not manifest["blocking_gaps"]
        and not missing_sections
        and not failed_checks
        and not boundary_gaps,
        "pbc": PBC_KEY,
        "manifest": manifest,
        "missing_sections": missing_sections,
        "failed_checks": failed_checks,
        "boundary_gaps": boundary_gaps,
        "side_effects": (),
    }


def smoke_test():
    """Exercise release evidence readiness validation side-effect-free."""
    validation = validate_release_evidence()
    evidence = build_release_evidence()
    return {
        "ok": validation["ok"] and evidence.get("ok") is True,
        "validation": validation,
        "evidence": evidence,
        "side_effects": (),
    }
