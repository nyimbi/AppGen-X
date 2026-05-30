from __future__ import annotations

from .core import (
    CONTROLS,
    FORMS,
    PBC_KEY,
    WIZARDS,
    construction_contracts_commercials_build_workbench_view,
    construction_contracts_commercials_render_workbench as _construction_contracts_commercials_render_workbench,
    construction_contracts_commercials_ui_contract as _construction_contracts_commercials_ui_contract,
)


def construction_contracts_commercials_form_contracts() -> dict:
    contracts = (
        {
            "key": "construction_contract_create_form",
            "table": "construction_contracts_commercials_construction_contract",
            "operation": "create_contract",
            "fields": ("tenant", "contract_code", "title", "contract_value", "pricing_basis", "jurisdiction", "schedule_of_values"),
        },
        {
            "key": "pay_application_intake_form",
            "table": "construction_contracts_commercials_pay_application",
            "operation": "record_pay_application",
            "fields": ("contract_code", "application_number", "period_start", "period_end", "attachments", "lines"),
        },
        {
            "key": "retainage_release_form",
            "table": "construction_contracts_commercials_retainage",
            "operation": "release_retainage",
            "fields": ("retainage_id", "pay_application_id", "completion_percent"),
        },
        {
            "key": "variation_order_review_form",
            "table": "construction_contracts_commercials_variation_order",
            "operation": "approve_variation_order",
            "fields": ("contract_code", "variation_number", "event_date", "notice_date", "quoted_amount", "approved_amount"),
        },
        {
            "key": "commercial_claim_notice_form",
            "table": "construction_contracts_commercials_commercial_claim",
            "operation": "register_commercial_claim",
            "fields": ("contract_code", "claim_number", "claim_type", "event_date", "notice_date", "claimed_amount"),
        },
        {
            "key": "lien_waiver_review_form",
            "table": "construction_contracts_commercials_lien_waiver",
            "operation": "create_lien_waiver",
            "fields": ("contract_code", "pay_application_id", "waiver_number", "covered_amount", "signed_date"),
        },
        {
            "key": "subcontract_package_compliance_form",
            "table": "construction_contracts_commercials_subcontract_package",
            "operation": "record_subcontract_package",
            "fields": ("contract_code", "package_code", "subcontractor_name", "contract_value", "insurance_status", "bond_status"),
        },
    )
    return {
        "format": "appgen.construction-contracts-commercials-form-contract.v1",
        "ok": set(FORMS).issubset({item["key"] for item in contracts}),
        "pbc": PBC_KEY,
        "contracts": contracts,
        "side_effects": (),
    }


def construction_contracts_commercials_wizard_contracts() -> dict:
    contracts = (
        {
            "key": "contract_award_wizard",
            "steps": ("contract_setup", "schedule_of_values", "guarantees", "award_review"),
            "forms": ("construction_contract_create_form",),
            "keywords": ("contract", "award", "commercial setup"),
        },
        {
            "key": "pay_application_certification_wizard",
            "steps": ("intake", "evidence_review", "waiver_review", "certification"),
            "forms": ("pay_application_intake_form", "lien_waiver_review_form"),
            "keywords": ("pay application", "certificate", "waiver"),
        },
        {
            "key": "variation_negotiation_wizard",
            "steps": ("notice_check", "quote_review", "approval", "valuation_update"),
            "forms": ("variation_order_review_form",),
            "keywords": ("variation", "change order", "quotation"),
        },
        {
            "key": "claim_entitlement_wizard",
            "steps": ("notice", "entitlement", "quantum", "settlement"),
            "forms": ("commercial_claim_notice_form",),
            "keywords": ("claim", "delay", "disruption"),
        },
        {
            "key": "final_account_closeout_wizard",
            "steps": ("retainage", "claims", "waivers", "subcontract_closeout", "closeout_packet"),
            "forms": ("retainage_release_form", "commercial_claim_notice_form", "lien_waiver_review_form", "subcontract_package_compliance_form"),
            "keywords": ("final account", "closeout", "retainage", "subcontract"),
        },
    )
    return {
        "format": "appgen.construction-contracts-commercials-wizard-contract.v1",
        "ok": set(WIZARDS).issubset({item["key"] for item in contracts}),
        "pbc": PBC_KEY,
        "contracts": contracts,
        "side_effects": (),
    }


def construction_contracts_commercials_control_catalog() -> dict:
    contracts = (
        {"key": "overclaim_guard", "type": "rule", "binds_to": ("construction_contracts_commercials_pay_application",)},
        {"key": "waiver_gate", "type": "gate", "binds_to": ("construction_contracts_commercials_pay_application", "construction_contracts_commercials_lien_waiver")},
        {"key": "retainage_release_gate", "type": "gate", "binds_to": ("construction_contracts_commercials_retainage",)},
        {"key": "notice_time_bar_monitor", "type": "monitor", "binds_to": ("construction_contracts_commercials_variation_order", "construction_contracts_commercials_commercial_claim")},
        {"key": "final_account_blocker_panel", "type": "panel", "binds_to": ("construction_contracts_commercials_construction_contract",)},
        {"key": "event_replay_console", "type": "console", "binds_to": ("construction_contracts_commercials_appgen_dead_letter_event",)},
    )
    return {
        "format": "appgen.construction-contracts-commercials-control-catalog.v1",
        "ok": set(CONTROLS).issubset({item["key"] for item in contracts}),
        "pbc": PBC_KEY,
        "contracts": contracts,
        "side_effects": (),
    }


def construction_contracts_commercials_ui_contract():
    contract = _construction_contracts_commercials_ui_contract()
    return {
        **contract,
        "configuration_editor": contract.get("configuration_editor", {"event_contract": "AppGen-X"}),
        "stream_engine_picker_visible": False,
        "action_permissions": contract.get("action_permissions", {}),
        "form_contracts": construction_contracts_commercials_form_contracts()["contracts"],
        "wizard_contracts": construction_contracts_commercials_wizard_contracts()["contracts"],
        "control_contracts": construction_contracts_commercials_control_catalog()["contracts"],
    }


def construction_contracts_commercials_render_workbench(state=None, tenant="default", actor=None):
    rendered = _construction_contracts_commercials_render_workbench(state=state, tenant=tenant, actor=actor)
    return {**rendered, "pbc": PBC_KEY}


def construction_contracts_commercials_standalone_workbench_blueprint() -> dict:
    from .routes import standalone_route_contracts

    route_manifest = standalone_route_contracts()
    return {
        "format": "appgen.construction-contracts-commercials-standalone-workbench-blueprint.v1",
        "ok": route_manifest["ok"]
        and construction_contracts_commercials_form_contracts()["ok"]
        and construction_contracts_commercials_wizard_contracts()["ok"]
        and construction_contracts_commercials_control_catalog()["ok"],
        "pbc": PBC_KEY,
        "routes": route_manifest["routes"],
        "forms": tuple(item["key"] for item in construction_contracts_commercials_form_contracts()["contracts"]),
        "wizards": tuple(item["key"] for item in construction_contracts_commercials_wizard_contracts()["contracts"]),
        "controls": tuple(item["key"] for item in construction_contracts_commercials_control_catalog()["contracts"]),
        "side_effects": (),
    }


def construction_contracts_commercials_render_standalone_workbench(summary: dict | None = None, tenant: str = "default") -> dict:
    summary = dict(summary or {})
    workbench = summary.get("result") if isinstance(summary.get("result"), dict) else summary
    if not workbench:
        workbench = construction_contracts_commercials_build_workbench_view(tenant=tenant)
    blueprint = construction_contracts_commercials_standalone_workbench_blueprint()
    metrics = workbench.get("metrics", {})
    queues = workbench.get("queues", {})
    return {
        "format": "appgen.construction-contracts-commercials-standalone-workbench-render.v1",
        "ok": blueprint["ok"] and workbench.get("ok") is True,
        "pbc": PBC_KEY,
        "tenant": workbench.get("tenant", tenant),
        "cards": (
            {"key": "contracts", "value": metrics.get("contract_count", 0), "label": "Contracts"},
            {"key": "certified_but_unpaid", "value": metrics.get("certified_but_unpaid", 0), "label": "Certified Net Due"},
            {"key": "active_claim_exposure", "value": metrics.get("active_claim_exposure", 0.0), "label": "Claim Exposure"},
            {"key": "retainage_held", "value": metrics.get("retainage_held", 0.0), "label": "Retainage Held"},
        ),
        "queue_sizes": {name: len(items) for name, items in queues.items()},
        "visible_actions": tuple(action["operation"] for action in workbench.get("actions", ()) if action.get("enabled")),
        "forms": blueprint["forms"],
        "wizards": blueprint["wizards"],
        "controls": blueprint["controls"],
        "routes": blueprint["routes"],
        "side_effects": (),
    }


def smoke_test():
    view = construction_contracts_commercials_build_workbench_view()
    rendered = construction_contracts_commercials_render_workbench()
    standalone = construction_contracts_commercials_render_standalone_workbench(view)
    contract = construction_contracts_commercials_ui_contract()
    return {
        "ok": contract["ok"] and view["ok"] and rendered["ok"] and standalone["ok"],
        "side_effects": (),
    }
