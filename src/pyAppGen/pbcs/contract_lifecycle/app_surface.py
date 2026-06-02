"""Standalone application surface for the contract_lifecycle PBC.

This module is intentionally package-local: a generated application that selects
only contract_lifecycle can use these contracts to mount a complete workbench
with owned datastore forms, guided wizards, controls, routes, and assistant
skills without sharing another PBC table.
"""

from __future__ import annotations

from .application import (
    ADVANCED_CAPABILITIES,
    CONFIGURATION_SCHEMA,
    CONTROLS,
    FORMS,
    OPERATION_SPECS,
    OWNED_TABLES,
    PBC_KEY,
    PERMISSIONS,
    RULE_DEFINITIONS,
    WIZARDS,
    agent_skill_manifest,
    chatbot_interface_contract,
    configuration_manifest,
    document_instruction_plan,
    render_workbench,
    route_contracts,
    schema_contract,
    seed_rows,
    service_contract,
    ui_contract,
)


def contract_lifecycle_forms_contract() -> dict:
    return {
        "ok": True,
        "pbc": PBC_KEY,
        "forms": FORMS,
        "covered_operations": tuple(form["submit_operation"] for form in FORMS),
        "owned_tables": OWNED_TABLES,
        "writes_foreign_tables": False,
    }


def contract_lifecycle_wizards_contract() -> dict:
    covered = tuple(wizard["terminal_operation"] for wizard in WIZARDS)
    return {
        "ok": True,
        "pbc": PBC_KEY,
        "wizards": WIZARDS,
        "terminal_operations": covered,
        "supports_intake_to_signature": "capture_signature" in covered,
        "supports_renewals_and_amendments": "execute_amendment" in covered,
    }


def contract_lifecycle_controls_contract() -> dict:
    return {
        "ok": True,
        "pbc": PBC_KEY,
        "controls": CONTROLS,
        "control_ids": tuple(control["id"] for control in CONTROLS),
        "permission_model": PERMISSIONS,
        "configuration_schema": CONFIGURATION_SCHEMA,
        "stream_engine_picker_visible": False,
    }


def standalone_seed_bundle() -> tuple[dict, ...]:
    return seed_rows() + (
        {
            "table": "contract_lifecycle_contract_record",
            "code": "CLM-DEMO-MSA",
            "status": "intake_ready",
            "payload": {
                "contract_type": "master_services_agreement",
                "jurisdiction": "US-DE",
                "counterparty_name": "Demo Supplier LLC",
                "value_amount": 250000,
            },
        },
        {
            "table": "contract_lifecycle_contract_obligation",
            "code": "CLM-DEMO-OBLIGATION",
            "status": "active",
            "payload": {"owner": "legal.ops", "evidence_required": True},
        },
    )


def single_pbc_contract_lifecycle_app_contract(state=None) -> dict:
    ui = ui_contract()
    workbench = render_workbench(state)
    service = service_contract()
    schema = schema_contract()
    agent = agent_skill_manifest()
    chatbot = chatbot_interface_contract()
    routes = route_contracts()
    forms = contract_lifecycle_forms_contract()
    wizards = contract_lifecycle_wizards_contract()
    controls = contract_lifecycle_controls_contract()
    config = configuration_manifest()
    return {
        "ok": all(
            item["ok"]
            for item in (ui, workbench, service, schema, agent, chatbot, forms, wizards, controls, config)
        )
        and len(routes) >= 6
        and len(standalone_seed_bundle()) >= 4,
        "pbc": PBC_KEY,
        "application_mode": "single_pbc_standalone",
        "owned_tables": OWNED_TABLES,
        "schema": schema,
        "service": service,
        "routes": routes,
        "ui": ui,
        "workbench": workbench,
        "forms": forms,
        "wizards": wizards,
        "controls": controls,
        "agent": agent,
        "chatbot": chatbot,
        "configuration": config,
        "rules": RULE_DEFINITIONS,
        "advanced_capabilities": ADVANCED_CAPABILITIES,
        "seed_data": standalone_seed_bundle(),
        "crud_operations": tuple(OPERATION_SPECS),
        "dependency_boundary": {
            "writes_foreign_tables": False,
            "cross_pbc_dependencies": ("api", "event", "projection"),
            "event_contract": "AppGen-X",
        },
    }


def document_instruction_contract_lifecycle_plan(document: str, instructions: str) -> dict:
    plan = document_instruction_plan(document, instructions)
    return {
        **plan,
        "ok": plan["ok"] and all(table in OWNED_TABLES for table in plan["candidate_tables"]),
        "single_pbc_ready": True,
        "assistant_surface": "ContractLifecycleAssistantPanel",
        "allowed_mutation_boundary": OWNED_TABLES,
    }


def standalone_route_contracts() -> tuple[dict, ...]:
    app_routes = (
        {"method": "GET", "path": "/contract-lifecycle/app", "operation": "single_pbc_contract_lifecycle_app_contract"},
        {"method": "GET", "path": "/contract-lifecycle/forms", "operation": "contract_lifecycle_forms_contract"},
        {"method": "GET", "path": "/contract-lifecycle/wizards", "operation": "contract_lifecycle_wizards_contract"},
        {"method": "GET", "path": "/contract-lifecycle/controls", "operation": "contract_lifecycle_controls_contract"},
    )
    return tuple(
        {
            **route,
            "pbc": PBC_KEY,
            "required_permission": "contract_lifecycle.read",
            "idempotency_key": f"{PBC_KEY}:{route['method']}:{route['path']}",
            "shared_table_access": False,
            "stream_engine_picker_visible": False,
        }
        for route in app_routes
    ) + route_contracts()


def app_surface_smoke_test() -> dict:
    app = single_pbc_contract_lifecycle_app_contract()
    instruction = document_instruction_contract_lifecycle_plan(
        "Renew the supplier agreement, update obligation evidence, and prepare signature packet.",
        "update renewal, obligation, and signature records after legal review",
    )
    route_paths = tuple(route["path"] for route in standalone_route_contracts())
    return {
        "ok": app["ok"]
        and instruction["ok"]
        and "/contract-lifecycle/app" in route_paths
        and not app["dependency_boundary"]["writes_foreign_tables"],
        "app": app,
        "instruction": instruction,
        "route_paths": route_paths,
    }
