"""Package-local controls for the Media Rights and Content Monetization workbench."""

from __future__ import annotations

from .runtime import media_rights_content_monetization_build_release_evidence
from .runtime import media_rights_content_monetization_runtime_smoke
from .runtime import media_rights_content_monetization_verify_owned_table_boundary


MEDIA_RIGHTS_CONTENT_MONETIZATION_CONTROLS = (
    {
        "control_id": "chain_of_title_gate",
        "title": "Chain-of-title gate",
        "description": "Requires evidence completeness before an asset can be treated as release-ready.",
        "permission": "media_rights_content_monetization.approve",
    },
    {
        "control_id": "exclusivity_overlap_guard",
        "title": "Exclusivity overlap guard",
        "description": "Flags outbound or competing grants that overlap on term, territory, platform, or lineage family.",
        "permission": "media_rights_content_monetization.approve",
    },
    {
        "control_id": "availability_resolution",
        "title": "Availability resolution",
        "description": "Verifies that territory carve-outs, holdbacks, and platform entitlements resolve to one explainable decision.",
        "permission": "media_rights_content_monetization.read",
    },
    {
        "control_id": "royalty_waterfall_control",
        "title": "Royalty waterfall control",
        "description": "Checks that deductions, recoupment, and partner share stages remain traceable to approved rules.",
        "permission": "media_rights_content_monetization.approve",
    },
    {
        "control_id": "assistant_guardrails",
        "title": "Assistant guardrails",
        "description": "Keeps rights memo automation preview-only, package-owned, and confirmation-gated.",
        "permission": "media_rights_content_monetization.read",
    },
)


def media_rights_content_monetization_control_catalog() -> dict:
    """Return package-local operational controls."""
    return {
        "ok": bool(MEDIA_RIGHTS_CONTENT_MONETIZATION_CONTROLS),
        "pbc": "media_rights_content_monetization",
        "controls": MEDIA_RIGHTS_CONTENT_MONETIZATION_CONTROLS,
        "control_ids": tuple(item["control_id"] for item in MEDIA_RIGHTS_CONTENT_MONETIZATION_CONTROLS),
        "side_effects": (),
    }



def media_rights_content_monetization_control_center(state: dict | None = None) -> dict:
    """Return executable control evidence for rights operations and release workflows."""
    source_state = dict(state or {})
    release = media_rights_content_monetization_build_release_evidence()
    runtime_smoke = media_rights_content_monetization_runtime_smoke()
    assets = source_state.get("rights_assets", {})
    agreements = source_state.get("license_agreements", {})
    windows = source_state.get("distribution_windows", {})
    conflicts = source_state.get("conflicts", {})
    territory_rules = source_state.get("territory_restrictions", {})
    revenue_shares = source_state.get("revenue_shares", {})
    chain_of_title_ready = all(asset.get("chain_of_title_complete") for asset in assets.values()) if assets else True
    no_open_conflicts = not any(item.get("status") == "open" for item in conflicts.values())
    availability_ready = bool(windows) and bool(agreements) and all(window.get("availability_state") in {"ready", "live"} for window in windows.values())
    accepted_boundary = media_rights_content_monetization_verify_owned_table_boundary(
        ("media_rights_content_monetization_rights_asset", "media_rights_content_monetization_license_agreement"),
    )
    rejected_boundary = media_rights_content_monetization_verify_owned_table_boundary(("foreign_projection_table",))
    assistant_guardrails = {
        "preview_only": True,
        "requires_confirmation_for_mutation": True,
        "boundary_ok": accepted_boundary["ok"] and not rejected_boundary["ok"],
    }
    royalty_ready = bool(revenue_shares) or not source_state.get("royalty_statements")
    territory_ready = bool(territory_rules) or not windows
    return {
        "ok": release["ok"] and runtime_smoke["ok"] and chain_of_title_ready and no_open_conflicts and assistant_guardrails["boundary_ok"] and royalty_ready and territory_ready,
        "pbc": "media_rights_content_monetization",
        "controls": media_rights_content_monetization_control_catalog()["controls"],
        "release": release,
        "runtime_smoke": runtime_smoke,
        "chain_of_title": {"ready": chain_of_title_ready, "asset_count": len(assets)},
        "exclusivity_overlap": {"ready": no_open_conflicts, "open_conflicts": tuple(conflicts.values())},
        "availability_resolution": {
            "ready": availability_ready,
            "window_count": len(windows),
            "territory_rule_count": len(territory_rules),
        },
        "royalty_waterfall": {"ready": royalty_ready, "revenue_share_count": len(revenue_shares)},
        "accepted_boundary": accepted_boundary,
        "rejected_boundary": rejected_boundary,
        "assistant_guardrails": assistant_guardrails,
        "side_effects": (),
    }



def media_rights_content_monetization_mutation_preview(action: str, table: str, payload: dict | None = None) -> dict:
    """Preview whether a mutation would stay inside the media-rights owned boundary."""
    normalized = str(action).lower()
    boundary = media_rights_content_monetization_verify_owned_table_boundary((table,))
    rights_sensitive = table in {
        "media_rights_content_monetization_license_agreement",
        "media_rights_content_monetization_distribution_window",
        "media_rights_content_monetization_royalty_statement",
    }
    return {
        "ok": boundary["ok"] and normalized in {"create", "read", "update", "delete"},
        "pbc": "media_rights_content_monetization",
        "action": normalized,
        "table": table,
        "payload_keys": tuple(sorted(dict(payload or {}))),
        "requires_confirmation": normalized != "read",
        "legal_review_recommended": rights_sensitive and normalized != "read",
        "boundary": boundary,
        "side_effects": (),
    }



def smoke_test() -> dict:
    """Exercise the control center with minimal package-local evidence."""
    preview = media_rights_content_monetization_mutation_preview(
        "update",
        "media_rights_content_monetization_distribution_window",
        {"availability_state": "live"},
    )
    control_center = media_rights_content_monetization_control_center(
        {
            "rights_assets": {"asset_001": {"chain_of_title_complete": True}},
            "license_agreements": {"lic_001": {"status": "active"}},
            "distribution_windows": {"win_001": {"availability_state": "ready"}},
            "territory_restrictions": {"terr_001": {"reason": "worldwide except CA"}},
            "revenue_shares": {"share_001": {"status": "active"}},
            "conflicts": {},
        }
    )
    return {
        "ok": preview["ok"] and control_center["ok"],
        "preview": preview,
        "control_center": control_center,
        "side_effects": (),
    }
