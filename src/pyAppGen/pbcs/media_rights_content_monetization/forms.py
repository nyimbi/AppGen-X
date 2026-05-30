"""Package-local forms for the Media Rights and Content Monetization workbench."""

from __future__ import annotations


MEDIA_RIGHTS_CONTENT_MONETIZATION_FORM_DEFINITIONS = (
    {
        "form_id": "rights_asset_grant_intake",
        "title": "Register rights asset and grant dimensions",
        "route": "POST /app/media-rights/rights-assets",
        "operation": "create_rights_asset",
        "permission": "media_rights_content_monetization.create",
        "owned_tables": ("media_rights_content_monetization_rights_asset",),
        "fields": (
            {"name": "tenant", "type": "string", "required": True},
            {"name": "asset_id", "type": "string", "required": True},
            {"name": "title", "type": "string", "required": True},
            {
                "name": "asset_class",
                "type": "enum",
                "required": True,
                "choices": ("film", "series_episode", "clip", "trailer", "artwork", "subtitle", "dub"),
            },
            {
                "name": "rights_type",
                "type": "enum",
                "required": True,
                "choices": ("primary_exploitation", "marketing_use", "derivative_packaging"),
            },
            {"name": "grantor", "type": "string", "required": True},
            {"name": "grantee", "type": "string", "required": True},
            {"name": "chain_of_title_complete", "type": "boolean", "required": True},
        ),
    },
    {
        "form_id": "license_agreement_scope_review",
        "title": "Capture inbound or outbound license scope",
        "route": "POST /app/media-rights/license-agreements",
        "operation": "record_license_agreement",
        "permission": "media_rights_content_monetization.update",
        "owned_tables": ("media_rights_content_monetization_license_agreement",),
        "fields": (
            {"name": "tenant", "type": "string", "required": True},
            {"name": "agreement_id", "type": "string", "required": True},
            {"name": "asset_id", "type": "string", "required": True},
            {
                "name": "direction",
                "type": "enum",
                "required": True,
                "choices": ("inbound", "outbound"),
            },
            {"name": "grantor", "type": "string", "required": True},
            {"name": "grantee", "type": "string", "required": True},
            {"name": "exclusive", "type": "boolean", "required": True},
            {"name": "start_on", "type": "string", "required": True},
            {"name": "end_on", "type": "string", "required": True},
        ),
    },
    {
        "form_id": "distribution_window_amendment",
        "title": "Review launch window and holdbacks",
        "route": "POST /app/media-rights/distribution-windows",
        "operation": "review_distribution_window",
        "permission": "media_rights_content_monetization.update",
        "owned_tables": ("media_rights_content_monetization_distribution_window",),
        "fields": (
            {"name": "window_id", "type": "string", "required": True},
            {"name": "asset_id", "type": "string", "required": True},
            {"name": "agreement_id", "type": "string", "required": True},
            {"name": "start_on", "type": "string", "required": True},
            {"name": "end_on", "type": "string", "required": True},
            {
                "name": "availability_state",
                "type": "enum",
                "required": True,
                "choices": ("pending_ingest", "awaiting_clearance", "ready", "live", "suspended", "expired"),
            },
            {"name": "territories", "type": "list", "required": True},
            {"name": "platform_families", "type": "list", "required": True},
        ),
    },
    {
        "form_id": "territory_hierarchy_override",
        "title": "Capture territory inclusion and carve-outs",
        "route": "POST /app/media-rights/territory-restrictions",
        "operation": "record_territory_restriction",
        "permission": "media_rights_content_monetization.update",
        "owned_tables": ("media_rights_content_monetization_territory_restriction",),
        "fields": (
            {"name": "restriction_id", "type": "string", "required": True},
            {"name": "asset_id", "type": "string", "required": True},
            {"name": "included_territories", "type": "list", "required": True},
            {"name": "excluded_territories", "type": "list", "required": False},
            {"name": "reason", "type": "string", "required": False},
        ),
    },
    {
        "form_id": "usage_ingestion_normalization",
        "title": "Approve normalized usage intake",
        "route": "POST /app/media-rights/usage-records",
        "operation": "approve_usage_record",
        "permission": "media_rights_content_monetization.approve",
        "owned_tables": ("media_rights_content_monetization_usage_record",),
        "fields": (
            {"name": "usage_id", "type": "string", "required": True},
            {"name": "asset_id", "type": "string", "required": True},
            {"name": "territory", "type": "string", "required": True},
            {
                "name": "platform_family",
                "type": "enum",
                "required": True,
                "choices": ("svod", "avod", "fast", "tvod", "linear", "social", "owned_app"),
            },
            {
                "name": "report_type",
                "type": "enum",
                "required": True,
                "choices": ("subscription", "ad_supported", "transactional", "linear"),
            },
            {"name": "recognized_revenue", "type": "number", "required": True},
            {"name": "usage_quantity", "type": "number", "required": True},
        ),
    },
    {
        "form_id": "royalty_waterfall_preview",
        "title": "Preview royalty waterfall and recoupment",
        "route": "POST /app/media-rights/royalty-statements/preview",
        "operation": "simulate_royalty_statement",
        "permission": "media_rights_content_monetization.approve",
        "owned_tables": (
            "media_rights_content_monetization_royalty_statement",
            "media_rights_content_monetization_revenue_share",
        ),
        "fields": (
            {"name": "statement_id", "type": "string", "required": True},
            {"name": "share_id", "type": "string", "required": True},
            {"name": "agreement_id", "type": "string", "required": True},
            {"name": "usage_ids", "type": "list", "required": False},
            {"name": "period_start", "type": "string", "required": True},
            {"name": "period_end", "type": "string", "required": True},
        ),
    },
    {
        "form_id": "assistant_document_intake",
        "title": "Assistant rights memo preview",
        "route": "POST /app/media-rights/assistant/document-preview",
        "operation": "assistant_preview",
        "permission": "media_rights_content_monetization.read",
        "owned_tables": (
            "media_rights_content_monetization_rights_asset",
            "media_rights_content_monetization_license_agreement",
            "media_rights_content_monetization_distribution_window",
            "media_rights_content_monetization_revenue_share",
            "media_rights_content_monetization_territory_restriction",
        ),
        "fields": (
            {"name": "document_text", "type": "text", "required": True},
            {"name": "instructions", "type": "text", "required": True},
            {
                "name": "target_entity",
                "type": "enum",
                "required": True,
                "choices": (
                    "rights_asset",
                    "license_agreement",
                    "distribution_window",
                    "territory_restriction",
                    "revenue_share",
                ),
            },
            {"name": "requested_action", "type": "enum", "required": True, "choices": ("create", "read", "update", "delete")},
        ),
    },
)


def media_rights_content_monetization_form_catalog() -> dict:
    """Return the package-local media rights workbench form registry."""
    forms = tuple(MEDIA_RIGHTS_CONTENT_MONETIZATION_FORM_DEFINITIONS)
    return {
        "ok": bool(forms),
        "pbc": "media_rights_content_monetization",
        "forms": forms,
        "form_ids": tuple(item["form_id"] for item in forms),
        "side_effects": (),
    }



def media_rights_content_monetization_get_form(form_id: str) -> dict:
    """Return one form definition by identifier."""
    form = next((item for item in MEDIA_RIGHTS_CONTENT_MONETIZATION_FORM_DEFINITIONS if item["form_id"] == form_id), None)
    return {
        "ok": form is not None,
        "pbc": "media_rights_content_monetization",
        "form": form,
        "side_effects": (),
    }



def media_rights_content_monetization_validate_form_payload(form_id: str, payload: dict | None = None) -> dict:
    """Validate a form payload against required fields and enum choices."""
    form = media_rights_content_monetization_get_form(form_id).get("form")
    if form is None:
        return {
            "ok": False,
            "accepted": False,
            "reason": "unknown_form",
            "form_id": form_id,
            "side_effects": (),
        }

    supplied = dict(payload or {})
    missing = tuple(
        field["name"]
        for field in form["fields"]
        if field.get("required") and supplied.get(field["name"]) in {None, ""}
    )
    invalid_choices = tuple(
        field["name"]
        for field in form["fields"]
        if field.get("type") == "enum"
        and supplied.get(field["name"]) not in {None, *field.get("choices", ())}
    )
    return {
        "ok": not missing and not invalid_choices,
        "accepted": not missing and not invalid_choices,
        "pbc": "media_rights_content_monetization",
        "form_id": form_id,
        "missing": missing,
        "invalid_choices": invalid_choices,
        "payload_keys": tuple(sorted(supplied)),
        "side_effects": (),
    }



def smoke_test() -> dict:
    """Exercise a happy-path assistant preview form validation."""
    catalog = media_rights_content_monetization_form_catalog()
    validation = media_rights_content_monetization_validate_form_payload(
        "assistant_document_intake",
        {
            "document_text": "Grant memo: AVOD LATAM window opens after SVOD holdback expires.",
            "instructions": "Create a preview-only amendment plan.",
            "target_entity": "distribution_window",
            "requested_action": "update",
        },
    )
    return {
        "ok": catalog["ok"] and validation["ok"],
        "catalog": catalog,
        "validation": validation,
        "side_effects": (),
    }
