"""Generated contract smoke tests for dam_core."""

from ..manifest import PBC_MANIFEST
from ..events import EVENT_CONTRACT
from ..schema_contract import SCHEMA_CONTRACT
from ..service_contract import SERVICE_CONTRACT
from ..release_evidence import RELEASE_EVIDENCE


def test_generated_schema_service_and_release_evidence():
    from .. import models, release_evidence, schema_contract

    assert SCHEMA_CONTRACT['pbc'] == 'dam_core'
    assert SCHEMA_CONTRACT['ok'] is True
    assert SCHEMA_CONTRACT['owned_tables']
    schema_smoke = schema_contract.smoke_test()
    model_smoke = models.smoke_test()
    assert schema_smoke['ok'] is True
    assert model_smoke['ok'] is True
    assert not schema_smoke['side_effects']
    assert not model_smoke['side_effects']
    assert SERVICE_CONTRACT['pbc'] == 'dam_core'
    assert SERVICE_CONTRACT['ok'] is True
    assert SERVICE_CONTRACT.get('shared_table_access') is False
    assert RELEASE_EVIDENCE['pbc'] == 'dam_core'
    assert RELEASE_EVIDENCE['ok'] is True


    release_manifest = release_evidence.release_readiness_manifest()
    release_validation = release_evidence.validate_release_evidence()
    release_smoke = release_evidence.smoke_test()
    assert release_manifest['ok'] is True
    assert release_validation['ok'] is True
    assert release_smoke['ok'] is True
    assert not release_manifest['blocking_gaps']
    assert not release_validation['missing_sections']
    assert not release_validation['failed_checks']
    assert not release_validation['boundary_gaps']
    assert not release_manifest['side_effects']
    assert not release_validation['side_effects']
    assert not release_smoke['side_effects']


def test_manifest_and_event_contract():
    from .. import events

    assert PBC_MANIFEST['pbc'] == 'dam_core'
    assert PBC_MANIFEST['standard_features']
    assert PBC_MANIFEST['advanced_capabilities']
    assert EVENT_CONTRACT['contract'] == 'appgen_event_contract'
    assert EVENT_CONTRACT['outbox_table'].startswith('dam_core_')
    assert EVENT_CONTRACT['inbox_table'].startswith('dam_core_')
    manifest = events.event_contract_manifest()
    validation = events.validate_event_contract()
    smoke = events.smoke_test()
    assert manifest['ok'] is True
    assert validation['ok'] is True
    assert smoke['ok'] is True
    assert manifest['stream_engine_picker_visible'] is False
    assert not validation['invalid_tables']
    assert not validation['invalid_emitted']
    assert not validation['invalid_consumed']
    assert smoke['emitted']['table'] == EVENT_CONTRACT['outbox_table']
    assert smoke['consumed']['table'] == EVENT_CONTRACT['inbox_table']
    assert smoke['emitted']['retry_policy']['max_attempts'] >= 3
    assert smoke['consumed']['dead_letter_table'].startswith(PBC_MANIFEST['pbc'] + '_')
    assert not manifest['side_effects']
    assert not validation['side_effects']
    assert not smoke['side_effects']


def test_registration_plan_is_side_effect_free():
    from .. import package_discovery_plan, package_metadata_manifest, register_pbc, registration_plan, validate_package_metadata

    assert register_pbc()['pbc'] == 'dam_core'
    plan = registration_plan()
    assert plan['ok'] is True
    assert plan['catalog_patch']
    metadata = package_metadata_manifest()
    metadata_validation = validate_package_metadata()
    discovery = package_discovery_plan()
    assert metadata['ok'] is True
    assert metadata_validation['ok'] is True
    assert discovery['ok'] is True
    assert metadata['stream_engine_picker_visible'] is False
    assert metadata['event_contract'] == 'AppGen-X'
    assert not metadata_validation['missing_entrypoints']
    assert not metadata_validation['missing_publish_artifacts']
    assert not metadata_validation['missing_capability_evidence']
    assert not metadata_validation['invalid']
    assert not discovery['side_effects']


def test_service_and_route_surface_are_executable():
    from .. import routes, services

    service_smoke = services.smoke_test()
    operation_contracts = services.service_operation_contracts()
    route_contracts = routes.api_route_contracts()
    route_validation = routes.validate_api_route_contracts()
    route_smoke = routes.smoke_test()
    assert service_smoke['ok'] is True
    assert operation_contracts['ok'] is True
    assert route_contracts['ok'] is True
    assert route_validation['ok'] is True
    assert route_contracts['contracts']
    assert all(item['permission'] for item in route_contracts['contracts'])
    assert all(item['event_contract'] == 'AppGen-X' for item in route_contracts['contracts'])
    assert all(item['stream_engine_picker_visible'] is False for item in route_contracts['contracts'])
    assert all(item['shared_table_access'] is False for item in route_contracts['contracts'])
    assert not route_validation['service_mismatches']
    assert not route_validation['missing_idempotency']
    assert not route_validation['invalid_table_scope']
    assert service_smoke['result']['operation_contract']['route']['path']
    assert service_smoke['result']['operation_contract']['permission']
    assert service_smoke['result']['operation_contract']['event_contract'] == 'AppGen-X'
    assert service_smoke['result']['operation_contract']['owned_tables'] or service_smoke['result']['operation_contract']['read_tables']
    assert route_smoke['ok'] is True
    assert not service_smoke['side_effects']
    assert not operation_contracts['side_effects']
    assert not route_contracts['side_effects']
    assert not route_validation['side_effects']
    assert not route_smoke['side_effects']


def test_configuration_permissions_and_seed_hooks_are_executable():
    from .. import config, permissions, seed_data

    config_smoke = config.smoke_test()
    governance_smoke = config.governance_smoke_test()
    permission_smoke = permissions.smoke_test()
    seed_smoke = seed_data.smoke_test()
    assert config_smoke['ok'] is True
    assert governance_smoke['ok'] is True
    assert governance_smoke['parameter']['accepted'] is True
    assert governance_smoke['compiled_rule']['compiled'] is True
    assert governance_smoke['rule_decision']['allowed'] is True
    assert permission_smoke['ok'] is True
    assert seed_smoke['ok'] is True
    assert not config_smoke['side_effects']
    assert not governance_smoke['side_effects']
    assert not permission_smoke['side_effects']
    assert not seed_smoke['side_effects']


def test_ui_workbench_surface_is_executable():
    from .. import ui

    if hasattr(ui, 'smoke_test'):
        smoke = ui.smoke_test()
    else:
        contract = getattr(ui, f"{PBC_MANIFEST['pbc']}_ui_contract")()
        rendered = {
            'ok': contract['ok'],
            'cards': contract.get('panels') or contract.get('fragments'),
            'route': (contract.get('routes') or (None,))[0],
        }
        smoke = {
            'ok': contract['ok'] and bool(contract.get('fragments')) and bool(rendered['cards']),
            'manifest': {'fragments': contract.get('fragments', ())},
            'rendered': rendered,
            'side_effects': (),
        }
    assert smoke['ok'] is True
    assert smoke['manifest']['fragments']
    assert smoke['rendered']['cards']
    assert not smoke['side_effects']


def test_event_handlers_are_idempotent_and_retryable():
    from .. import handlers

    smoke = handlers.smoke_test()
    assert smoke['ok'] is True
    assert smoke['manifest']['handlers']
    assert smoke['first_result']['retry_policy']
    assert smoke['first_result']['dead_letter_table'].startswith('dam_core_')
    assert smoke['duplicate_result']['duplicate'] is True
    assert smoke['unknown_result']['handled'] is False
    assert not smoke['side_effects']

def test_table_stakes_and_advanced_capability_assurance_is_executable():
    from .. import capability_assurance

    manifest = capability_assurance.table_stakes_capability_manifest()
    validation = capability_assurance.validate_table_stakes_capability_coverage()
    smoke = capability_assurance.smoke_test()
    assert manifest['ok'] is True
    assert validation['ok'] is True
    assert smoke['ok'] is True
    assert manifest['standard_features']
    assert manifest['advanced_capabilities']
    assert not validation['missing_standard']
    assert not validation['missing_advanced']
    assert not validation['missing_operations']
    assert not validation['uncovered_features']
    assert not validation['invalid_tables']
    assert not validation['invalid_backends']
    assert validation['stream_picker_visible'] is False
    assert validation['event_contract'] == 'AppGen-X'
    assert validation['owned_boundary_rejection']['ok'] is False
    assert validation['owned_boundary_rejection']['violations']
    assert not smoke['side_effects']


def test_executable_dam_lifecycle_covers_collections_rights_metadata_workflow_usage_and_lineage():
    from .. import runtime

    state = runtime.dam_core_empty_state()
    state = runtime.dam_core_configure_runtime(
        state,
        {
            "database_backend": "postgresql",
            "event_topic": runtime.DAM_CORE_REQUIRED_EVENT_TOPIC,
            "retry_limit": 3,
            "default_storage_tier": "warm",
            "allowed_mime_types": ("image/jpeg",),
            "rendition_profiles": ("web_large",),
            "rights_default_decision": "review",
            "metadata_taxonomies": ("product",),
            "default_locale": "en-US",
            "workbench_limit": 100,
        },
    )["state"]
    for name, value in (
        ("max_asset_size_mb", 1000),
        ("quality_threshold", 0.7),
        ("rights_risk_threshold", 0.6),
        ("transcode_retry_limit", 3),
        ("duplicate_similarity_threshold", 0.9),
        ("rendition_cost_weight", 0.35),
        ("carbon_cost_weight", 0.15),
        ("usage_forecast_horizon_days", 90),
        ("metadata_confidence_floor", 0.6),
        ("workbench_limit", 100),
    ):
        state = runtime.dam_core_set_parameter(state, name, value)["state"]
    state = runtime.dam_core_register_rule(
        state,
        {
            "rule_id": "rule_dam_test",
            "tenant": "tenant_test",
            "scope": "asset_governance",
            "status": "active",
            "mime_policy": {"allowed": ("image/jpeg",)},
            "rights_policy": {"blocked_markets": ("restricted",)},
            "rendition_policy": {"required_profiles": ("web_large",)},
            "metadata_policy": {"required_tags": ("product",)},
        },
    )["state"]
    state = runtime.dam_core_register_asset(
        state,
        {
            "asset_id": "asset_test",
            "tenant": "tenant_test",
            "filename": "asset.jpg",
            "mime_type": "image/jpeg",
            "size_mb": 10,
            "storage_uri": "object://asset",
            "binary": b"asset-primary",
            "created_by": "owner",
        },
    )["state"]
    state = runtime.dam_core_register_asset(
        state,
        {
            "asset_id": "asset_test_derived",
            "tenant": "tenant_test",
            "filename": "asset-derived.jpg",
            "mime_type": "image/jpeg",
            "size_mb": 5,
            "storage_uri": "object://asset-derived",
            "binary": b"asset-derived",
            "created_by": "owner",
        },
    )["state"]
    state = runtime.dam_core_create_asset_collection(
        state,
        {
            "collection_id": "coll_test",
            "tenant": "tenant_test",
            "name": "Launch",
            "purpose": "commerce",
        },
    )["state"]
    state = runtime.dam_core_add_asset_to_collection(
        state,
        {
            "member_id": "member_test",
            "collection_id": "coll_test",
            "asset_id": "asset_test",
            "tenant": "tenant_test",
        },
    )["state"]
    state = runtime.dam_core_attach_rights_policy(
        state,
        {
            "policy_id": "rights_test",
            "asset_id": "asset_test",
            "tenant": "tenant_test",
            "license_type": "commercial",
            "allowed_markets": ("US",),
            "blocked_markets": ("restricted",),
            "expires_at": "2027-01-01",
            "attribution_required": False,
            "approver": "legal",
        },
    )["state"]
    state = runtime.dam_core_register_license_agreement(
        state,
        {
            "agreement_id": "lic_test",
            "policy_id": "rights_test",
            "tenant": "tenant_test",
            "licensor": "brand",
            "licensee": "tenant_test",
            "start_date": "2026-01-01",
            "end_date": "2027-01-01",
            "terms": {"markets": ("US",)},
        },
    )["state"]
    state = runtime.dam_core_grant_usage_entitlement(
        state,
        {
            "entitlement_id": "ent_test",
            "agreement_id": "lic_test",
            "asset_id": "asset_test",
            "tenant": "tenant_test",
            "market": "US",
            "use_case": "product_detail",
        },
    )["state"]
    state = runtime.dam_core_register_metadata_taxonomy(
        state,
        {
            "taxonomy_id": "tax_test",
            "tenant": "tenant_test",
            "name": "product",
            "allowed_values": ("backpack",),
        },
    )["state"]
    state = runtime.dam_core_add_metadata_tag(
        state,
        {
            "tag_id": "tag_test",
            "asset_id": "asset_test",
            "tenant": "tenant_test",
            "taxonomy": "product",
            "value": "backpack",
            "confidence": 0.9,
            "source": "human",
        },
    )["state"]
    state = runtime.dam_core_enrich_metadata(
        state,
        {
            "enrichment_id": "enrich_test",
            "asset_id": "asset_test",
            "tenant": "tenant_test",
            "source": "vision",
            "attributes": {"object": "backpack"},
            "confidence": 0.9,
        },
    )["state"]
    state = runtime.dam_core_add_semantic_annotation(
        state,
        {
            "annotation_id": "anno_test",
            "asset_id": "asset_test",
            "tenant": "tenant_test",
            "label": "backpack",
            "confidence": 0.9,
            "span": {"x": 0, "y": 0, "w": 1, "h": 1},
        },
    )["state"]
    state = runtime.dam_core_request_rendition(
        state,
        {
            "rendition_id": "rend_test",
            "asset_id": "asset_test",
            "tenant": "tenant_test",
            "profile": "web_large",
            "target_mime_type": "image/jpeg",
            "width": 1200,
            "height": 800,
        },
    )["state"]
    state = runtime.dam_core_complete_rendition(
        state,
        "rend_test",
        {"uri": "object://asset/web.jpg", "quality_score": 0.9, "duration_ms": 100},
    )["state"]
    workflow = runtime.dam_core_start_asset_workflow(
        state,
        {
            "case_id": "case_test",
            "asset_id": "asset_test",
            "tenant": "tenant_test",
            "workflow_type": "approval",
            "requested_by": "owner",
            "reviewers": ("legal",),
        },
    )
    state = workflow["state"]
    state = runtime.dam_core_complete_asset_review_task(
        state,
        "case_test:legal",
        {"decision": "approve", "reviewed_by": "legal"},
    )["state"]
    state = runtime.dam_core_open_asset_exception(
        state,
        {
            "exception_id": "exc_test",
            "asset_id": "asset_test",
            "tenant": "tenant_test",
            "reason": "alt_text",
            "severity": "low",
        },
    )["state"]
    state = runtime.dam_core_resolve_asset_exception_case(
        state,
        "exc_test",
        {"resolution": "alt_text_added", "resolved_by": "owner"},
    )["state"]
    state = runtime.dam_core_record_asset_usage_snapshot(
        state,
        {
            "snapshot_id": "usage_test",
            "asset_id": "asset_test",
            "tenant": "tenant_test",
            "impressions": 100,
            "downloads": 10,
            "channel": "commerce",
        },
    )["state"]
    state = runtime.dam_core_detect_asset_duplicate_candidate(
        state,
        {
            "candidate_id": "dup_test",
            "asset_id": "asset_test",
            "candidate_asset_id": "asset_test_derived",
            "tenant": "tenant_test",
            "similarity": 0.95,
        },
    )["state"]
    state = runtime.dam_core_record_asset_lineage(
        state,
        {
            "lineage_id": "lineage_test",
            "asset_id": "asset_test_derived",
            "source_asset_id": "asset_test",
            "tenant": "tenant_test",
            "lineage_type": "derived",
        },
    )["state"]

    assert state["asset_collections"]["coll_test"]["member_count"] == 1
    assert state["license_agreements"]["lic_test"]["status"] == "active"
    assert state["usage_entitlements"]["ent_test"]["status"] == "active"
    assert state["metadata_taxonomies"]["tax_test"]["status"] == "active"
    assert state["metadata_enrichments"]["enrich_test"]["status"] == "accepted"
    assert state["semantic_annotations"]["anno_test"]["status"] == "active"
    assert state["asset_workflow_cases"]["case_test"]["status"] == "approved"
    assert state["asset_exceptions"]["exc_test"]["status"] == "resolved"
    assert state["asset_usage_snapshots"]["usage_test"]["engagement_score"] > 0
    assert state["asset_duplicate_candidates"]["dup_test"]["status"] == "duplicate_review"
    assert state["asset_lineage"]["lineage_test"]["status"] == "recorded"
    assert all(event["event_contract"] == "AppGen-X" for event in state["outbox"])
    assert runtime.dam_core_verify_owned_table_boundary(runtime.DAM_CORE_OWNED_TABLES)["ok"] is True
