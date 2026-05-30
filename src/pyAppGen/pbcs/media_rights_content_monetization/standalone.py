"""Standalone one-PBC application surface for media rights and content monetization."""

from __future__ import annotations

from copy import deepcopy
from datetime import date, timedelta
from typing import Any

from . import agent
from . import runtime
from . import ui
from .controls import media_rights_content_monetization_control_center
from .controls import media_rights_content_monetization_mutation_preview
from .forms import media_rights_content_monetization_form_catalog
from .wizards import media_rights_content_monetization_plan_wizard
from .wizards import media_rights_content_monetization_wizard_catalog

PBC_KEY = "media_rights_content_monetization"

REGION_GROUPS = {
    "worldwide": {"us", "ca", "mx", "br", "ar", "cl", "co", "gb", "fr", "de", "za", "ke", "ng", "in", "jp", "au"},
    "latam": {"mx", "br", "ar", "cl", "co", "pe"},
    "emea": {"gb", "fr", "de", "za", "ke", "ng"},
    "north_america": {"us", "ca", "mx"},
}

DEFAULT_CONFIGURATION = {
    "database_backend": "postgresql",
    "event_topic": runtime.MEDIA_RIGHTS_CONTENT_MONETIZATION_REQUIRED_EVENT_TOPIC,
    "retry_limit": 5,
    "default_currency": "USD",
    "workbench_limit": 100,
    "default_notice_window_days": 30,
    "allowed_platform_families": ("svod", "avod", "fast", "tvod", "linear", "social", "owned_app"),
    "allowed_ad_modes": ("none", "pre_roll", "mid_roll", "dynamic_ad_insertion", "programmatic"),
}

DEFAULT_PARAMETERS = {
    "quality_score_floor": 0.85,
    "materiality_threshold": 5000,
    "approval_sla_hours": 24,
    "risk_threshold": 0.3,
    "forecast_horizon_days": 90,
    "workbench_limit": 100,
}

DEFAULT_RULES = (
    {
        "rule_id": "rights.clearance.default",
        "scope": "rights_clearance",
        "require_chain_of_title": True,
        "require_active_window": True,
        "require_territory_resolution": True,
        "status": "active",
    },
    {
        "rule_id": "rights.exclusivity.default",
        "scope": "exclusivity_overlap",
        "check_asset_lineage": True,
        "check_platform_family": True,
        "check_territory_overlap": True,
        "status": "active",
    },
    {
        "rule_id": "rights.royalty.default",
        "scope": "royalty_waterfall",
        "require_usage_approval": True,
        "require_recoupment_trace": True,
        "status": "active",
    },
)


def _copy_payload(payload: dict[str, Any] | None) -> dict[str, Any]:
    return deepcopy(dict(payload or {}))



def _as_date(value: str | None, fallback: date | None = None) -> date:
    if value:
        return date.fromisoformat(str(value))
    if fallback is not None:
        return fallback
    return date.today()



def _overlaps(start_a: str, end_a: str, start_b: str, end_b: str) -> bool:
    a_start = _as_date(start_a)
    a_end = _as_date(end_a)
    b_start = _as_date(start_b)
    b_end = _as_date(end_b)
    return a_start <= b_end and b_start <= a_end



def _territory_set(values: tuple[str, ...] | list[str] | None) -> set[str]:
    normalized = {str(item).lower() for item in (values or ())}
    expanded = set(normalized)
    for item in tuple(normalized):
        expanded.update(REGION_GROUPS.get(item, set()))
    return expanded



def _territory_matches(target: str, included: tuple[str, ...], excluded: tuple[str, ...]) -> bool:
    normalized_target = str(target).lower()
    included_set = _territory_set(included)
    excluded_set = _territory_set(excluded)
    if normalized_target in excluded_set:
        return False
    if "worldwide" in included_set or normalized_target in included_set:
        return True
    return False



def _append_outbox(state: dict[str, Any], event_type: str, payload: dict[str, Any]) -> dict[str, Any]:
    outbox = list(state.get("outbox", ()))
    outbox.append(
        {
            "event_type": event_type,
            "topic": runtime.MEDIA_RIGHTS_CONTENT_MONETIZATION_REQUIRED_EVENT_TOPIC,
            "payload": deepcopy(payload),
        }
    )
    state["outbox"] = tuple(outbox)
    return state



def _ensure_state(state: dict[str, Any]) -> dict[str, Any]:
    base = deepcopy(state)
    defaults = {
        "rights_assets": {},
        "license_agreements": {},
        "distribution_windows": {},
        "usage_records": {},
        "royalty_statements": {},
        "revenue_shares": {},
        "territory_restrictions": {},
        "conflicts": {},
        "assistant_reviews": (),
        "availability_checks": (),
    }
    for key, value in defaults.items():
        if key not in base:
            base[key] = deepcopy(value)
    return base


class MediaRightsContentMonetizationStandaloneApplication:
    """Executable standalone application for package-local rights operations."""

    def __init__(self, tenant: str = "default") -> None:
        self.tenant = tenant
        self.state = _ensure_state(runtime.media_rights_content_monetization_empty_state())

    def configure(self, payload: dict[str, Any] | None = None) -> dict[str, Any]:
        merged = {**DEFAULT_CONFIGURATION, **_copy_payload(payload), "tenant": self.tenant}
        result = runtime.media_rights_content_monetization_configure_runtime(self.state, merged)
        self.state = _ensure_state(result["state"])
        return {
            "ok": result["ok"],
            "configuration": self.state["configuration"],
            "side_effects": (),
        }

    def register_defaults(self) -> dict[str, Any]:
        if not self.state.get("configuration"):
            self.configure()
        parameters = []
        for name, value in DEFAULT_PARAMETERS.items():
            result = runtime.media_rights_content_monetization_set_parameter(self.state, name, value)
            self.state = _ensure_state(result["state"])
            parameters.append(result["parameter"])
        rules = []
        for rule in DEFAULT_RULES:
            result = runtime.media_rights_content_monetization_register_rule(self.state, rule)
            self.state = _ensure_state(result["state"])
            rules.append(result["rule"])
        return {
            "ok": bool(parameters) and bool(rules),
            "parameters": tuple(parameters),
            "rules": tuple(rules),
            "side_effects": (),
        }

    def create_rights_asset(self, payload: dict[str, Any]) -> dict[str, Any]:
        supplied = _copy_payload(payload)
        asset_id = supplied.get("asset_id") or supplied.get("id")
        if not asset_id:
            return {"ok": False, "reason": "asset_id_required", "side_effects": ()}
        record = {
            "asset_id": asset_id,
            "tenant": supplied.get("tenant", self.tenant),
            "title": supplied.get("title", asset_id),
            "asset_class": supplied.get("asset_class", "film"),
            "rights_type": supplied.get("rights_type", "primary_exploitation"),
            "grantor": supplied.get("grantor", "unknown_grantor"),
            "grantee": supplied.get("grantee", "unknown_grantee"),
            "exclusive": bool(supplied.get("exclusive", False)),
            "languages": tuple(supplied.get("languages", ("any",))),
            "edit_type": supplied.get("edit_type", "standard"),
            "marketing_use": bool(supplied.get("marketing_use", supplied.get("rights_type") == "marketing_use")),
            "derivative_packaging": bool(supplied.get("derivative_packaging", supplied.get("rights_type") == "derivative_packaging")),
            "chain_of_title_complete": bool(supplied.get("chain_of_title_complete", False)),
            "lineage_family": supplied.get("lineage_family", asset_id),
            "prohibited_sponsor_categories": tuple(supplied.get("prohibited_sponsor_categories", ())),
            "evidence": tuple(supplied.get("evidence", ())),
            "status": "release_ready" if supplied.get("chain_of_title_complete") else "awaiting_chain_of_title",
        }
        command = runtime.media_rights_content_monetization_command_rights_asset(
            self.state,
            {
                "id": asset_id,
                "tenant": record["tenant"],
                "status": record["status"],
                "title": record["title"],
            },
        )
        self.state = _ensure_state(command["state"])
        self.state["rights_assets"][asset_id] = record
        self.state = _append_outbox(self.state, "MediaRightsAssetGrantCaptured", record)
        return {
            "ok": True,
            "asset": record,
            "command": command,
            "side_effects": (),
        }

    def record_license_agreement(self, payload: dict[str, Any]) -> dict[str, Any]:
        supplied = _copy_payload(payload)
        agreement_id = supplied.get("agreement_id")
        asset_id = supplied.get("asset_id")
        if not agreement_id or not asset_id:
            return {"ok": False, "reason": "agreement_id_and_asset_id_required", "side_effects": ()}
        direction = supplied.get("direction", "inbound")
        source_rights_ok = direction == "inbound" or bool(supplied.get("upstream_agreement_id"))
        agreement = {
            "agreement_id": agreement_id,
            "tenant": supplied.get("tenant", self.tenant),
            "asset_id": asset_id,
            "direction": direction,
            "grantor": supplied.get("grantor", "unknown_grantor"),
            "grantee": supplied.get("grantee", "unknown_grantee"),
            "exclusive": bool(supplied.get("exclusive", False)),
            "start_on": supplied.get("start_on", date.today().isoformat()),
            "end_on": supplied.get("end_on", (date.today() + timedelta(days=365)).isoformat()),
            "territories": tuple(supplied.get("territories", ("worldwide",))),
            "platform_families": tuple(supplied.get("platform_families", ("svod",))),
            "languages": tuple(supplied.get("languages", ("any",))),
            "monetization_modes": tuple(supplied.get("monetization_modes", ("subscription",))),
            "upstream_agreement_id": supplied.get("upstream_agreement_id"),
            "minimum_guarantee": float(supplied.get("minimum_guarantee", 0.0)),
            "recoupment_balance": float(supplied.get("recoupment_balance", supplied.get("minimum_guarantee", 0.0))),
            "status": "active" if source_rights_ok else "blocked",
            "source_rights_ok": source_rights_ok,
        }
        conflicts = []
        asset = self.state.get("rights_assets", {}).get(asset_id, {})
        lineage_family = asset.get("lineage_family", asset_id)
        for other in self.state.get("license_agreements", {}).values():
            if other["asset_id"] != asset_id and self.state.get("rights_assets", {}).get(other["asset_id"], {}).get("lineage_family") != lineage_family:
                continue
            overlap = _overlaps(agreement["start_on"], agreement["end_on"], other["start_on"], other["end_on"])
            territory_overlap = bool(_territory_set(agreement["territories"]) & _territory_set(other["territories"]))
            platform_overlap = bool(set(agreement["platform_families"]) & set(other["platform_families"]))
            if other.get("exclusive") and agreement["exclusive"] and overlap and territory_overlap and platform_overlap:
                conflict_id = f"conflict_{len(self.state['conflicts']) + len(conflicts) + 1:03d}"
                conflicts.append(
                    {
                        "conflict_id": conflict_id,
                        "asset_id": asset_id,
                        "agreement_ids": (other["agreement_id"], agreement_id),
                        "reason": "exclusive_overlap",
                        "status": "open",
                    }
                )
        self.state["license_agreements"][agreement_id] = agreement
        for conflict in conflicts:
            self.state["conflicts"][conflict["conflict_id"]] = conflict
        plan = runtime.media_rights_content_monetization_execute_domain_operation(
            "record_license_agreement",
            {"tenant": agreement["tenant"], "agreement_id": agreement_id},
        )
        self.state = _append_outbox(self.state, "MediaRightsLicenseAgreementCaptured", agreement)
        return {
            "ok": source_rights_ok,
            "agreement": agreement,
            "conflicts": tuple(conflicts),
            "domain_plan": plan,
            "side_effects": (),
        }

    def review_distribution_window(self, payload: dict[str, Any]) -> dict[str, Any]:
        supplied = _copy_payload(payload)
        window_id = supplied.get("window_id")
        asset_id = supplied.get("asset_id")
        agreement_id = supplied.get("agreement_id")
        if not window_id or not asset_id or not agreement_id:
            return {"ok": False, "reason": "window_id_asset_id_agreement_id_required", "side_effects": ()}
        amendment_target = supplied.get("amend_window_id")
        version = 1
        lineage_id = window_id
        if amendment_target:
            prior = self.state.get("distribution_windows", {}).get(amendment_target)
            if prior:
                version = int(prior.get("version", 1)) + 1
                lineage_id = prior.get("lineage_id", amendment_target)
                self.state["distribution_windows"][amendment_target] = {
                    **prior,
                    "superseded_by": window_id,
                    "status": "superseded",
                }
        record = {
            "window_id": window_id,
            "lineage_id": lineage_id,
            "version": version,
            "asset_id": asset_id,
            "agreement_id": agreement_id,
            "start_on": supplied.get("start_on", date.today().isoformat()),
            "end_on": supplied.get("end_on", (date.today() + timedelta(days=30)).isoformat()),
            "availability_state": supplied.get("availability_state", "ready"),
            "territories": tuple(supplied.get("territories", ("worldwide",))),
            "platform_families": tuple(supplied.get("platform_families", ("svod",))),
            "languages": tuple(supplied.get("languages", ("any",))),
            "ad_modes": tuple(supplied.get("ad_modes", ("none",))),
            "holdbacks": tuple(supplied.get("holdbacks", ())),
            "amendment_reason": supplied.get("amendment_reason"),
            "status": "active",
        }
        self.state["distribution_windows"][window_id] = record
        plan = runtime.media_rights_content_monetization_execute_domain_operation(
            "review_distribution_window",
            {"asset_id": asset_id, "window_id": window_id},
        )
        self.state = _append_outbox(self.state, "MediaRightsWindowReviewed", record)
        return {
            "ok": True,
            "window": record,
            "domain_plan": plan,
            "side_effects": (),
        }

    def record_territory_restriction(self, payload: dict[str, Any]) -> dict[str, Any]:
        supplied = _copy_payload(payload)
        restriction_id = supplied.get("restriction_id")
        asset_id = supplied.get("asset_id")
        if not restriction_id or not asset_id:
            return {"ok": False, "reason": "restriction_id_and_asset_id_required", "side_effects": ()}
        restriction = {
            "restriction_id": restriction_id,
            "asset_id": asset_id,
            "included_territories": tuple(supplied.get("included_territories", ("worldwide",))),
            "excluded_territories": tuple(supplied.get("excluded_territories", ())),
            "parent_scope": supplied.get("parent_scope"),
            "reason": supplied.get("reason", "territory_override"),
        }
        self.state["territory_restrictions"][restriction_id] = restriction
        plan = runtime.media_rights_content_monetization_execute_domain_operation(
            "record_territory_restriction",
            {"asset_id": asset_id, "restriction_id": restriction_id},
        )
        self.state = _append_outbox(self.state, "MediaRightsTerritoryRestrictionCaptured", restriction)
        return {
            "ok": True,
            "restriction": restriction,
            "domain_plan": plan,
            "side_effects": (),
        }

    def create_revenue_share(self, payload: dict[str, Any]) -> dict[str, Any]:
        supplied = _copy_payload(payload)
        share_id = supplied.get("share_id")
        agreement_id = supplied.get("agreement_id")
        if not share_id or not agreement_id:
            return {"ok": False, "reason": "share_id_and_agreement_id_required", "side_effects": ()}
        share = {
            "share_id": share_id,
            "agreement_id": agreement_id,
            "waterfall_stages": tuple(
                supplied.get(
                    "waterfall_stages",
                    (
                        {"stage": "gross_revenue", "type": "pass_through"},
                        {"stage": "platform_commission", "type": "percent", "rate": 0.2},
                        {"stage": "partner_share", "type": "percent", "rate": 0.5},
                    ),
                )
            ),
            "status": supplied.get("status", "active"),
        }
        self.state["revenue_shares"][share_id] = share
        plan = runtime.media_rights_content_monetization_execute_domain_operation(
            "create_revenue_share",
            {"agreement_id": agreement_id, "share_id": share_id},
        )
        self.state = _append_outbox(self.state, "MediaRightsRevenueShareConfigured", share)
        return {
            "ok": True,
            "revenue_share": share,
            "domain_plan": plan,
            "side_effects": (),
        }

    def assess_availability(self, payload: dict[str, Any]) -> dict[str, Any]:
        supplied = _copy_payload(payload)
        asset_id = supplied.get("asset_id")
        territory = str(supplied.get("territory", "worldwide")).lower()
        platform_family = str(supplied.get("platform_family", "svod")).lower()
        as_of = supplied.get("as_of", date.today().isoformat())
        language = supplied.get("language", "any")
        ad_mode = supplied.get("ad_mode", "none")
        sponsor_category = supplied.get("sponsor_category")
        asset = self.state.get("rights_assets", {}).get(asset_id)
        if asset is None:
            return {"ok": False, "eligible": False, "reasons": ("unknown_asset",), "side_effects": ()}

        matching_windows = []
        reasons = []
        restriction_rows = [
            item for item in self.state.get("territory_restrictions", {}).values() if item.get("asset_id") == asset_id
        ]
        territory_restricted = False
        for restriction in restriction_rows:
            included = tuple(restriction.get("included_territories", ("worldwide",)))
            excluded = tuple(restriction.get("excluded_territories", ()))
            if not _territory_matches(territory, included, excluded):
                territory_restricted = True
                break
        for window in self.state.get("distribution_windows", {}).values():
            if window["asset_id"] != asset_id:
                continue
            in_term = _overlaps(window["start_on"], window["end_on"], as_of, as_of)
            territory_ok = _territory_matches(territory, window["territories"], ()) and not territory_restricted
            platform_ok = platform_family in {item.lower() for item in window["platform_families"]}
            language_ok = "any" in asset["languages"] or language in asset["languages"]
            ad_mode_ok = ad_mode == "none" or ad_mode in {item.lower() for item in window["ad_modes"]}
            active_holdback = next(
                (
                    holdback
                    for holdback in window["holdbacks"]
                    if _territory_matches(territory, tuple(holdback.get("territories", ("worldwide",))), ())
                    and platform_family in {item.lower() for item in holdback.get("platform_families", (platform_family,))}
                    and _overlaps(holdback.get("start_on", window["start_on"]), holdback.get("end_on", window["end_on"]), as_of, as_of)
                ),
                None,
            )
            if in_term and territory_ok and platform_ok and language_ok and ad_mode_ok and not active_holdback:
                matching_windows.append(window)
        if not asset.get("chain_of_title_complete"):
            reasons.append("missing_chain_of_title")
        if territory_restricted:
            reasons.append("territory_restricted")
        if sponsor_category and sponsor_category in asset.get("prohibited_sponsor_categories", ()):
            reasons.append("sponsor_restricted")
        if not matching_windows:
            reasons.append("no_matching_window")
        if any(item.get("status") == "open" and item.get("asset_id") == asset_id for item in self.state.get("conflicts", {}).values()):
            reasons.append("open_conflict")
        decision = {
            "asset_id": asset_id,
            "territory": territory,
            "platform_family": platform_family,
            "as_of": as_of,
            "eligible": not reasons,
            "matching_window_ids": tuple(item["window_id"] for item in matching_windows),
            "reasons": tuple(reasons),
        }
        self.state["availability_checks"] = tuple(self.state.get("availability_checks", ())) + (decision,)
        return {"ok": True, **decision, "side_effects": ()}

    def approve_usage_record(self, payload: dict[str, Any]) -> dict[str, Any]:
        supplied = _copy_payload(payload)
        usage_id = supplied.get("usage_id")
        asset_id = supplied.get("asset_id")
        if not usage_id or not asset_id:
            return {"ok": False, "reason": "usage_id_and_asset_id_required", "side_effects": ()}
        availability = self.assess_availability(
            {
                "asset_id": asset_id,
                "territory": supplied.get("territory", "worldwide"),
                "platform_family": supplied.get("platform_family", "svod"),
                "as_of": supplied.get("reported_on", date.today().isoformat()),
                "language": supplied.get("language", "any"),
                "ad_mode": supplied.get("ad_mode", "none"),
            }
        )
        if not availability["eligible"]:
            return {
                "ok": False,
                "usage_id": usage_id,
                "availability": availability,
                "side_effects": (),
            }
        metric_map = {
            "subscription": "subscriber_month",
            "ad_supported": "ad_impression",
            "transactional": "transaction",
            "linear": "linear_minute",
        }
        record = {
            "usage_id": usage_id,
            "asset_id": asset_id,
            "territory": supplied.get("territory", "worldwide"),
            "platform_family": supplied.get("platform_family", "svod"),
            "report_type": supplied.get("report_type", "subscription"),
            "canonical_metric": metric_map.get(supplied.get("report_type", "subscription"), "unit"),
            "usage_quantity": float(supplied.get("usage_quantity", 0)),
            "recognized_revenue": float(supplied.get("recognized_revenue", 0)),
            "status": "approved",
        }
        self.state["usage_records"][usage_id] = record
        plan = runtime.media_rights_content_monetization_execute_domain_operation(
            "approve_usage_record",
            {"usage_id": usage_id, "asset_id": asset_id},
        )
        self.state = _append_outbox(self.state, "MediaRightsUsageApproved", record)
        return {
            "ok": True,
            "usage_record": record,
            "availability": availability,
            "domain_plan": plan,
            "side_effects": (),
        }

    def simulate_royalty_statement(self, payload: dict[str, Any]) -> dict[str, Any]:
        supplied = _copy_payload(payload)
        statement_id = supplied.get("statement_id")
        share_id = supplied.get("share_id")
        agreement_id = supplied.get("agreement_id")
        if not statement_id or not share_id or not agreement_id:
            return {"ok": False, "reason": "statement_id_share_id_agreement_id_required", "side_effects": ()}
        share = self.state.get("revenue_shares", {}).get(share_id)
        agreement = self.state.get("license_agreements", {}).get(agreement_id)
        if share is None or agreement is None:
            return {"ok": False, "reason": "missing_share_or_agreement", "side_effects": ()}
        selected_ids = tuple(supplied.get("usage_ids", ())) or tuple(self.state.get("usage_records", {}).keys())
        usage_rows = [self.state["usage_records"][usage_id] for usage_id in selected_ids if usage_id in self.state.get("usage_records", {})]
        gross_revenue = round(sum(item["recognized_revenue"] for item in usage_rows), 2)
        remaining = gross_revenue
        lines = []
        for stage in share["waterfall_stages"]:
            if stage["type"] == "percent":
                amount = round(remaining * float(stage.get("rate", 0)), 2)
            else:
                amount = remaining
            if stage["stage"] == "platform_commission":
                remaining = round(remaining - amount, 2)
            elif stage["stage"] == "partner_share":
                remaining = amount
            lines.append({"stage": stage["stage"], "amount": amount})
        recoupment_draw = round(min(remaining, agreement.get("recoupment_balance", 0.0)), 2)
        partner_payable = round(max(remaining - recoupment_draw, 0.0), 2)
        agreement["recoupment_balance"] = round(max(agreement.get("recoupment_balance", 0.0) - recoupment_draw, 0.0), 2)
        statement = {
            "statement_id": statement_id,
            "share_id": share_id,
            "agreement_id": agreement_id,
            "gross_revenue": gross_revenue,
            "lines": tuple(lines),
            "recoupment_draw": recoupment_draw,
            "partner_payable": partner_payable,
            "status": "simulated",
        }
        self.state["royalty_statements"][statement_id] = statement
        plan = runtime.media_rights_content_monetization_execute_domain_operation(
            "simulate_royalty_statement",
            {"statement_id": statement_id, "share_id": share_id},
        )
        self.state = _append_outbox(self.state, "MediaRightsRoyaltySimulated", statement)
        return {
            "ok": True,
            "royalty_statement": statement,
            "domain_plan": plan,
            "side_effects": (),
        }

    def assistant_preview(self, payload: dict[str, Any]) -> dict[str, Any]:
        supplied = _copy_payload(payload)
        target_entity = supplied.get("target_entity", "rights_asset")
        target_table = {
            "rights_asset": "media_rights_content_monetization_rights_asset",
            "license_agreement": "media_rights_content_monetization_license_agreement",
            "distribution_window": "media_rights_content_monetization_distribution_window",
            "territory_restriction": "media_rights_content_monetization_territory_restriction",
            "revenue_share": "media_rights_content_monetization_revenue_share",
        }.get(target_entity, "media_rights_content_monetization_rights_asset")
        document_plan = agent.document_instruction_plan(
            supplied.get("document_text", ""),
            supplied.get("instructions", ""),
        )
        mutation_preview = media_rights_content_monetization_mutation_preview(
            supplied.get("requested_action", "read"),
            target_table,
            supplied.get("payload", {}),
        )
        relevant_forms = tuple(
            form["form_id"]
            for form in media_rights_content_monetization_form_catalog()["forms"]
            if target_table in form["owned_tables"]
        )
        relevant_wizards = tuple(
            wizard["wizard_id"]
            for wizard in media_rights_content_monetization_wizard_catalog()["wizards"]
            if any(step["form_id"] in relevant_forms for step in wizard["steps"])
        )
        preview = {
            "preview_id": f"preview_{len(self.state.get('assistant_reviews', ())) + 1:03d}",
            "target_entity": target_entity,
            "document_plan": document_plan,
            "mutation_preview": mutation_preview,
            "recommended_forms": relevant_forms,
            "recommended_wizards": relevant_wizards,
            "requires_confirmation": True,
        }
        self.state["assistant_reviews"] = tuple(self.state.get("assistant_reviews", ())) + (preview,)
        return {"ok": True, **preview, "side_effects": ()}

    def workbench(self, as_of: str | None = None) -> dict[str, Any]:
        effective_as_of = as_of or date.today().isoformat()
        expiring_cutoff = (_as_date(effective_as_of) + timedelta(days=30)).isoformat()
        expiring_windows = tuple(
            window
            for window in self.state.get("distribution_windows", {}).values()
            if window["end_on"] <= expiring_cutoff and window.get("status") == "active"
        )
        return {
            "ok": True,
            "pbc": PBC_KEY,
            "as_of": effective_as_of,
            "metrics": {
                "rights_assets": len(self.state.get("rights_assets", {})),
                "active_licenses": sum(1 for item in self.state.get("license_agreements", {}).values() if item.get("status") == "active"),
                "open_conflicts": sum(1 for item in self.state.get("conflicts", {}).values() if item.get("status") == "open"),
                "approved_usage_records": sum(1 for item in self.state.get("usage_records", {}).values() if item.get("status") == "approved"),
                "expiring_windows": len(expiring_windows),
            },
            "availability_calendar": tuple(
                {
                    "asset_id": window["asset_id"],
                    "window_id": window["window_id"],
                    "territories": window["territories"],
                    "platform_families": window["platform_families"],
                    "start_on": window["start_on"],
                    "end_on": window["end_on"],
                    "availability_state": window["availability_state"],
                }
                for window in self.state.get("distribution_windows", {}).values()
            ),
            "conflict_queue": tuple(self.state.get("conflicts", {}).values()),
            "expiring_windows": expiring_windows,
            "assistant_queue": tuple(self.state.get("assistant_reviews", ())),
            "side_effects": (),
        }

    def control_center(self) -> dict[str, Any]:
        return media_rights_content_monetization_control_center(self.snapshot())

    def snapshot(self) -> dict[str, Any]:
        return deepcopy(self.state)



def media_rights_content_monetization_standalone_app_contract() -> dict[str, Any]:
    """Return the composed standalone-app surface for this one-PBC package."""
    forms = media_rights_content_monetization_form_catalog()
    wizards = media_rights_content_monetization_wizard_catalog()
    ui_contract = ui.media_rights_content_monetization_ui_contract()
    return {
        "format": "appgen.media-rights-content-monetization-standalone-app.v1",
        "ok": forms["ok"] and wizards["ok"] and ui_contract["ok"],
        "pbc": PBC_KEY,
        "app_class": "MediaRightsContentMonetizationStandaloneApplication",
        "implementation_directory": f"src/pyAppGen/pbcs/{PBC_KEY}",
        "service_methods": (
            "configure",
            "register_defaults",
            "create_rights_asset",
            "record_license_agreement",
            "review_distribution_window",
            "record_territory_restriction",
            "create_revenue_share",
            "assess_availability",
            "approve_usage_record",
            "simulate_royalty_statement",
            "assistant_preview",
            "workbench",
            "control_center",
            "snapshot",
        ),
        "ui_surfaces": ("forms", "wizards", "controls", "workbench", "availability_calendar", "assistant_preview"),
        "docs": ("implementation-plan.md", "RELEASE_EVIDENCE.md"),
        "event_contract": "AppGen-X",
        "event_topic": runtime.MEDIA_RIGHTS_CONTENT_MONETIZATION_REQUIRED_EVENT_TOPIC,
        "allowed_backends": runtime.MEDIA_RIGHTS_CONTENT_MONETIZATION_ALLOWED_DATABASE_BACKENDS,
        "stream_engine_picker_visible": False,
        "side_effects": (),
    }



def bootstrap_media_rights_content_monetization_standalone_app(tenant: str = "default") -> dict[str, Any]:
    """Create a live standalone app and register package defaults."""
    app = MediaRightsContentMonetizationStandaloneApplication(tenant=tenant)
    configuration = app.configure()
    defaults = app.register_defaults()
    return {
        "ok": configuration["ok"] and defaults["ok"],
        "pbc": PBC_KEY,
        "app": app,
        "contract": media_rights_content_monetization_standalone_app_contract(),
        "configuration": configuration,
        "defaults": defaults,
        "side_effects": (),
    }



def media_rights_content_monetization_standalone_smoke() -> dict[str, Any]:
    """Exercise the standalone app through a focused rights-monetization scenario."""
    bundle = bootstrap_media_rights_content_monetization_standalone_app(tenant="tenant_media")
    app = bundle["app"]
    asset = app.create_rights_asset(
        {
            "asset_id": "asset_movie_001",
            "title": "Atlas of Rights",
            "asset_class": "film",
            "rights_type": "primary_exploitation",
            "grantor": "Studio Alpha",
            "grantee": "StreamCo",
            "chain_of_title_complete": True,
            "languages": ("en", "es"),
            "prohibited_sponsor_categories": ("gambling",),
        }
    )
    agreement = app.record_license_agreement(
        {
            "agreement_id": "lic_in_001",
            "asset_id": "asset_movie_001",
            "direction": "inbound",
            "grantor": "Studio Alpha",
            "grantee": "StreamCo",
            "exclusive": True,
            "territories": ("worldwide",),
            "platform_families": ("svod", "avod"),
            "start_on": "2026-01-01",
            "end_on": "2026-12-31",
            "minimum_guarantee": 25000,
        }
    )
    territory = app.record_territory_restriction(
        {
            "restriction_id": "terr_001",
            "asset_id": "asset_movie_001",
            "included_territories": ("worldwide",),
            "excluded_territories": ("ca",),
            "reason": "worldwide_except_canada",
        }
    )
    window = app.review_distribution_window(
        {
            "window_id": "win_001",
            "asset_id": "asset_movie_001",
            "agreement_id": "lic_in_001",
            "start_on": "2026-03-01",
            "end_on": "2026-10-31",
            "availability_state": "live",
            "territories": ("worldwide",),
            "platform_families": ("svod",),
            "ad_modes": ("none",),
            "holdbacks": (
                {
                    "holdback_id": "hold_001",
                    "territories": ("latam",),
                    "platform_families": ("avod",),
                    "start_on": "2026-03-01",
                    "end_on": "2026-05-31",
                },
            ),
        }
    )
    share = app.create_revenue_share({"share_id": "share_001", "agreement_id": "lic_in_001"})
    availability = app.assess_availability(
        {
            "asset_id": "asset_movie_001",
            "territory": "us",
            "platform_family": "svod",
            "as_of": "2026-06-15",
            "language": "en",
        }
    )
    usage = app.approve_usage_record(
        {
            "usage_id": "usage_001",
            "asset_id": "asset_movie_001",
            "territory": "us",
            "platform_family": "svod",
            "report_type": "subscription",
            "recognized_revenue": 120000,
            "usage_quantity": 4500,
            "reported_on": "2026-06-15",
            "language": "en",
        }
    )
    statement = app.simulate_royalty_statement(
        {
            "statement_id": "stmt_001",
            "share_id": "share_001",
            "agreement_id": "lic_in_001",
            "usage_ids": ("usage_001",),
            "period_start": "2026-06-01",
            "period_end": "2026-06-30",
        }
    )
    preview = app.assistant_preview(
        {
            "document_text": "Legal memo: Canada remains excluded pending amendment, LATAM AVOD holdback ends June 1.",
            "instructions": "Prepare a preview-only amendment plan.",
            "target_entity": "distribution_window",
            "requested_action": "update",
            "payload": {"window_id": "win_001"},
        }
    )
    workbench = app.workbench(as_of="2026-06-15")
    rendered = ui.media_rights_content_monetization_render_standalone_workbench(workbench)
    controls = app.control_center()
    return {
        "ok": bundle["ok"]
        and asset["ok"]
        and agreement["ok"]
        and territory["ok"]
        and window["ok"]
        and share["ok"]
        and availability["eligible"]
        and usage["ok"]
        and statement["ok"]
        and preview["ok"]
        and workbench["ok"]
        and rendered["ok"]
        and controls["ok"],
        "contract": bundle["contract"],
        "asset": asset,
        "agreement": agreement,
        "territory": territory,
        "window": window,
        "revenue_share": share,
        "availability": availability,
        "usage": usage,
        "statement": statement,
        "preview": preview,
        "wizard_plan": media_rights_content_monetization_plan_wizard(
            "rights_clearance_launch",
            {"asset_id": "asset_movie_001", "agreement_id": "lic_in_001"},
        ),
        "workbench": workbench,
        "rendered": rendered,
        "controls": controls,
        "side_effects": (),
    }
