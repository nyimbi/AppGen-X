"""Standalone one-PBC app composition for cybersecurity_operations_center."""

from __future__ import annotations

from typing import Any

from . import agent, events, permissions, routes, seed_data, services, ui
from .manifest import PBC_MANIFEST
from .models import default_parameter_records, default_policy_bundle
from .release_evidence import build_release_evidence
from .runtime import (
    CYBERSECURITY_OPERATIONS_CENTER_REQUIRED_EVENT_TOPIC,
    cybersecurity_operations_center_empty_state,
)

PBC_KEY = "cybersecurity_operations_center"
DEFAULT_CONFIGURATION = {
    "database_backend": "postgresql",
    "event_topic": CYBERSECURITY_OPERATIONS_CENTER_REQUIRED_EVENT_TOPIC,
    "retry_limit": 5,
    "default_policy": "soc_default",
    "workbench_limit": 100,
    "suppression_review_days": 14,
}


def _default_parameter_values() -> dict[str, Any]:
    return {record["parameter_name"]: record["value"] for record in default_parameter_records()}


def standalone_workflow_catalog() -> tuple[dict[str, Any], ...]:
    return (
        {
            "workflow_id": "bootstrap_soc_workspace",
            "label": "Bootstrap SOC Workspace",
            "steps": ("configure_runtime", "set_parameter", "register_rule", "record_governed_model"),
            "outcome": "workspace_ready",
        },
        {
            "workflow_id": "alert_to_incident",
            "label": "Alert to Incident",
            "steps": ("command_security_alert", "enrich_security_alert", "transition_alert", "record_security_incident"),
            "outcome": "incident_opened",
        },
        {
            "workflow_id": "evidence_and_containment",
            "label": "Evidence and Containment",
            "steps": ("record_response_evidence", "create_containment_action", "simulate_playbook_run"),
            "outcome": "response_in_progress",
        },
        {
            "workflow_id": "shift_handoff",
            "label": "Shift Handoff",
            "steps": ("build_case_detail", "query_workbench", "generate_handoff_packet"),
            "outcome": "handoff_packet_ready",
        },
    )


class CybersecurityOperationsCenterStandaloneApp:
    """Package-local standalone app that owns SOC runtime state."""

    def __init__(self, state: dict[str, Any] | None = None) -> None:
        self.service = services.CybersecurityOperationsCenterService(state=state or cybersecurity_operations_center_empty_state())

    @property
    def state(self) -> dict[str, Any]:
        return self.service.state

    def dispatch(self, route: str, payload: dict[str, Any] | None = None) -> dict[str, Any]:
        return routes.dispatch_route(route, payload, service=self.service)

    def bootstrap(self, *, tenant: str = "tenant_demo") -> dict[str, Any]:
        configuration = dict(DEFAULT_CONFIGURATION)
        configure = self.service.configure_runtime(configuration)
        parameter_results = []
        for name, value in _default_parameter_values().items():
            parameter_results.append(
                self.service.set_parameter(name, value, actor="standalone-bootstrap", rationale="Standalone bootstrap")
            )
        alert_policy = self.service.register_rule(
            {
                "tenant": tenant,
                "rule_name": "security_alert_policy",
                "policy": {**default_policy_bundle(), "dedup_window_hours": 6, "promotion_cluster_threshold": 1},
            },
            actor="standalone-bootstrap",
        )
        containment_policy = self.service.register_rule(
            {
                "tenant": tenant,
                "rule_name": "containment_action_policy",
                "policy": {"high_risk_requires_approval": True, "breakpoint_required_actions": ("host_isolation",)},
            },
            actor="standalone-bootstrap",
        )
        governed_model = self.service.record_governed_model(
            {
                "tenant": tenant,
                "model_name": "soc-triage-assistant",
                "intended_use": "Draft cited triage summaries and handoff packets.",
                "guardrails": {"requires_human_confirmation": True, "cites_sources": True, "owned_tables_only": True},
            }
        )
        return {
            "ok": configure["ok"] and all(result["ok"] for result in parameter_results) and alert_policy["ok"] and containment_policy["ok"] and governed_model["ok"],
            "tenant": tenant,
            "configuration": configure,
            "parameters": tuple(parameter_results),
            "rules": (alert_policy, containment_policy),
            "governed_model": governed_model,
            "side_effects": (),
        }

    def load_demo_workspace(self, *, tenant: str = "tenant_demo") -> dict[str, Any]:
        bootstrap = self.bootstrap(tenant=tenant)
        created = self.service.command_security_alert(
            {
                "tenant": tenant,
                "severity": "critical",
                "confidence": 0.94,
                "asset_ref": "srv-edge-01",
                "principal_ref": "alice",
                "indicator_value": "198.51.100.42",
                "actor": "sensor",
                "detection_context": {
                    "source_event_id": f"evt-{tenant}-001",
                    "detection_timestamp": "2026-05-29T00:00:00+00:00",
                    "detection_rule_id": "sigma-ransomware-001",
                    "evidence_checksum": "sha256:standalone-alert",
                    "confidence": 0.94,
                    "tactic_tags": ("execution", "impact"),
                },
            }
        )
        alert = created["result"]["created"][0]
        self.service.enrich_security_alert(
            alert["id"],
            {
                "asset_criticality": "critical",
                "network_exposure": "internet_facing",
                "user_sensitivity": "privileged_admin",
                "prior_incident_links": ["INC-2026-0001"],
            },
            "analyst",
        )
        self.service.transition_alert(alert["id"], "triaged", "analyst", "Validated likely credential theft")
        incident = self.service.record_security_incident(
            {
                "tenant": tenant,
                "alert_ids": [alert["id"]],
                "asset_criticality": "critical",
                "containment_required": True,
                "commander": "soc-lead",
                "communications_owner": "comms-lead",
                "evidence_owner": "forensics-lead",
                "actor": "analyst",
                "title": "Credential theft on internet-facing server",
            }
        )
        incident_id = incident["result"]["record"]["id"]
        evidence = self.service.record_response_evidence(
            {
                "tenant": tenant,
                "case_id": incident_id,
                "source_system": "edr",
                "storage_reference": f"vault://{tenant}/evidence/alert-001",
                "admissibility_notes": "Preserved from EDR with immutable checksum.",
                "actor": "forensics",
            }
        )
        evidence_id = evidence["result"]["record"]["id"]
        containment = self.service.create_containment_action(
            {
                "tenant": tenant,
                "incident_id": incident_id,
                "action_type": "host_isolation",
                "approved_by": "supervisor",
                "actor": "responder",
                "rollback_instructions": "Remove network isolation after clean-image validation.",
            }
        )
        playbook = self.service.simulate_playbook_run(
            {
                "tenant": tenant,
                "template_name": "host-isolation",
                "stage": "analyst_approval",
                "related_incident_id": incident_id,
                "notes": ("Pause before isolation to notify business owner.",),
            }
        )
        asset = self.service.review_asset_exposure(
            {
                "tenant": tenant,
                "asset_ref": "srv-edge-01",
                "criticality": "critical",
                "internet_exposed": True,
            }
        )
        intel = self.service.approve_threat_intel(
            {
                "tenant": tenant,
                "indicator_value": "198.51.100.42",
                "observed_fact": {"sensor": "edr", "indicator_type": "ip"},
                "assessed_relationship": {"campaign": "credential-theft", "confidence": 0.82},
                "campaign_context": {"target_profile": "internet-facing linux hosts"},
                "analyst_inference": {"recommended_playbooks": ("host-isolation", "credential-reset")},
                "confidence": 0.82,
                "source_provenance": "internal+commercial",
                "candidate_playbooks": ("host-isolation", "credential-reset"),
            }
        )
        control = self.service.create_control_assertion(
            {
                "tenant": tenant,
                "control_name": "high_risk_containment_approval",
                "control_status": "passing",
                "evidence": {"containment_action_id": containment["result"]["record"]["id"]},
            }
        )
        seal = self.service.receive_event(
            {
                "tenant": tenant,
                "event_type": "AuditEventSealed",
                "idempotency_key": f"seal-{tenant}-{evidence_id}",
                "payload": {"evidence_id": evidence_id, "sealed_bundle_id": f"bundle-{tenant}-001"},
            }
        )
        metrics = self.service.receive_event(
            {
                "tenant": tenant,
                "event_type": "OperationalKpiChanged",
                "idempotency_key": f"metrics-{tenant}",
                "payload": {"tenant": tenant},
            }
        )
        workbench = self.render_workbench(tenant=tenant)
        detail = self.render_case_detail(incident_id)
        handoff = self.service.generate_handoff_packet(tenant=tenant)
        return {
            "ok": all(
                result["ok"]
                for result in (bootstrap, created, incident, evidence, containment, playbook, asset, intel, control, seal, metrics, workbench, detail, handoff)
            ),
            "tenant": tenant,
            "alert_id": alert["id"],
            "incident_id": incident_id,
            "evidence_id": evidence_id,
            "workbench": workbench,
            "detail": detail,
            "handoff": handoff,
            "side_effects": (),
        }

    def render_workbench(self, *, tenant: str = "tenant_demo") -> dict[str, Any]:
        rendered = ui.cybersecurity_operations_center_render_workbench(self.state, tenant=tenant)
        return {
            "ok": rendered["ok"],
            "pbc": PBC_KEY,
            "shell": {
                "app_id": f"{PBC_KEY}_one_pbc_app",
                "mode": "standalone_one_pbc_app",
                "required_permissions": permissions.permission_manifest()["permissions"],
            },
            **rendered,
        }

    def render_case_detail(self, case_id: str) -> dict[str, Any]:
        rendered = ui.cybersecurity_operations_center_render_detail(self.state, case_id)
        return {
            "ok": rendered["ok"],
            "pbc": PBC_KEY,
            "shell": {"app_id": f"{PBC_KEY}_one_pbc_app", "mode": "standalone_one_pbc_app"},
            **rendered,
        }

    def release_snapshot(self) -> dict[str, Any]:
        return build_release_evidence()


def standalone_application_manifest() -> dict[str, Any]:
    app = CybersecurityOperationsCenterStandaloneApp()
    demo = app.load_demo_workspace()
    workbench = demo["workbench"]["workbench"]
    detail = demo["detail"]["detail"]
    return {
        "format": "appgen.cybersecurity-operations-center-standalone-app.v1",
        "ok": demo["ok"],
        "pbc": PBC_KEY,
        "mode": "standalone_one_pbc_app",
        "manifest": PBC_MANIFEST,
        "routes": routes.api_route_contracts(),
        "services": services.service_operation_manifest(),
        "permissions": permissions.permission_manifest(),
        "events": events.event_contract_manifest(),
        "ui": ui.cybersecurity_operations_center_ui_contract(),
        "agent": agent.composed_agent_contribution(),
        "release": build_release_evidence(),
        "seed": seed_data.seed_plan(),
        "workflows": standalone_workflow_catalog(),
        "bootstrap": {
            "tenant": demo["tenant"],
            "urgent_lane_count": len(workbench["lanes"]["urgent"]),
            "incident_card_count": len(workbench["incident_cards"]),
            "detail_case_type": detail["case_type"],
            "handoff_summary": demo["handoff"]["result"]["packet"]["summary"],
        },
        "side_effects": (),
    }


def validate_standalone_application() -> dict[str, Any]:
    app = standalone_application_manifest()
    workflow_ids = tuple(item["workflow_id"] for item in app["workflows"])
    missing_workflows = tuple(
        workflow_id
        for workflow_id in ("bootstrap_soc_workspace", "alert_to_incident", "evidence_and_containment", "shift_handoff")
        if workflow_id not in workflow_ids
    )
    missing_sections = tuple(
        section
        for section in ("routes", "services", "permissions", "events", "ui", "agent", "release", "seed")
        if not app.get(section)
    )
    bootstrap = app["bootstrap"]
    return {
        "ok": app["ok"]
        and not missing_workflows
        and not missing_sections
        and bootstrap["urgent_lane_count"] >= 1
        and bootstrap["incident_card_count"] >= 1
        and bootstrap["detail_case_type"] == "incident",
        "pbc": PBC_KEY,
        "missing_workflows": missing_workflows,
        "missing_sections": missing_sections,
        "app": app,
        "side_effects": (),
    }


def smoke_test() -> dict[str, Any]:
    validation = validate_standalone_application()
    app = validation["app"]
    return {
        "ok": validation["ok"]
        and app["release"]["ok"]
        and bool(app["ui"]["full_capability_surface"]["forms"])
        and bool(app["workflows"]),
        "validation": validation,
        "side_effects": (),
    }
