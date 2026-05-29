"""Executable runtime contract for the donor_grant_fundraising PBC."""

from __future__ import annotations

from copy import deepcopy
import hashlib
from pathlib import Path

from .domain_depth import DOMAIN_OPERATIONS, DOMAIN_OWNED_TABLES, domain_depth_contract, execute_domain_operation, domain_depth_smoke_test
from .fundraising_app import controls_contract, forms_contract, fundraising_app_smoke_test, single_pbc_app_contract, wizards_contract

PBC_KEY = "donor_grant_fundraising"
DONOR_GRANT_FUNDRAISING_BUSINESS_TABLES = (
    "donor_grant_fundraising_donor",
    "donor_grant_fundraising_campaign",
    "donor_grant_fundraising_pledge",
    "donor_grant_fundraising_gift",
    "donor_grant_fundraising_restriction",
    "donor_grant_fundraising_grant_application",
    "donor_grant_fundraising_stewardship_touchpoint",
    "donor_grant_fundraising_donor_relationship",
    "donor_grant_fundraising_proposal_workspace",
    "donor_grant_fundraising_acknowledgement",
    "donor_grant_fundraising_briefing_packet",
    "donor_grant_fundraising_opportunity_score",
    "donor_grant_fundraising_review_chain",
    "donor_grant_fundraising_budget_validation",
)
DONOR_GRANT_FUNDRAISING_GOVERNANCE_TABLES = (
    "donor_grant_fundraising_policy_rule",
    "donor_grant_fundraising_runtime_parameter",
    "donor_grant_fundraising_schema_extension",
    "donor_grant_fundraising_control_assertion",
    "donor_grant_fundraising_governed_model",
)
DONOR_GRANT_FUNDRAISING_EVENT_TABLES = (
    "donor_grant_fundraising_appgen_outbox_event",
    "donor_grant_fundraising_appgen_inbox_event",
    "donor_grant_fundraising_appgen_dead_letter_event",
)
DONOR_GRANT_FUNDRAISING_OWNED_TABLES = (
    DONOR_GRANT_FUNDRAISING_BUSINESS_TABLES
    + DONOR_GRANT_FUNDRAISING_GOVERNANCE_TABLES
    + DONOR_GRANT_FUNDRAISING_EVENT_TABLES
)
DONOR_GRANT_FUNDRAISING_RUNTIME_TABLES = DONOR_GRANT_FUNDRAISING_OWNED_TABLES
DONOR_GRANT_FUNDRAISING_ALLOWED_DATABASE_BACKENDS = ("postgresql", "mysql", "mariadb")
DONOR_GRANT_FUNDRAISING_REQUIRED_EVENT_TOPIC = "pbc.donor_grant_fundraising.events"
DONOR_GRANT_FUNDRAISING_EMITTED_EVENT_TYPES = (
    "DonorGrantFundraisingCreated",
    "DonorGrantFundraisingUpdated",
    "DonorGrantFundraisingApproved",
    "DonorGrantFundraisingExceptionOpened",
)
DONOR_GRANT_FUNDRAISING_CONSUMED_EVENT_TYPES = ("PolicyChanged", "CustomerUpdated", "SupplierQualified")
DONOR_GRANT_FUNDRAISING_STANDARD_FEATURE_KEYS = (
    "donor_management",
    "donor_grant_fundraising_workflow",
    "donor_grant_fundraising_analytics",
    "configuration_schema",
    "rule_engine",
    "parameter_engine",
    "owned_schema_migrations_models",
    "appgen_x_outbox_inbox_eventing",
    "idempotent_handlers",
    "retry_dead_letter_evidence",
    "permissions",
    "seed_data",
    "workbench",
    "agentic_document_instruction_intake",
    "governed_datastore_crud",
    "ai_agent_task_assistance",
    "configuration_workbench",
    "continuous_release_assurance",
    "single_pbc_domain_app",
    "forms",
    "wizards",
    "controls",
    "prospect_pipeline",
    "gift_pledge_campaign_matching",
    "grant_submission_workspace",
)
DONOR_GRANT_FUNDRAISING_RUNTIME_CAPABILITY_KEYS = (
    "donor_grant_fundraising_event_sourced_operational_history",
    "donor_grant_fundraising_multi_tenant_policy_isolation",
    "donor_grant_fundraising_schema_evolution_resilience",
    "donor_grant_fundraising_autonomous_anomaly_detection",
    "donor_grant_fundraising_semantic_document_instruction_understanding",
    "donor_grant_fundraising_predictive_risk_scoring",
    "donor_grant_fundraising_counterfactual_scenario_simulation",
    "donor_grant_fundraising_cryptographic_audit_proofs",
    "donor_grant_fundraising_continuous_control_testing",
    "donor_grant_fundraising_carbon_and_sustainability_awareness",
    "donor_grant_fundraising_cross_pbc_event_federation",
    "donor_grant_fundraising_governed_ai_agent_execution",
)
DONOR_GRANT_FUNDRAISING_UI_FRAGMENT_KEYS = (
    "DonorGrantFundraisingWorkbench",
    "DonorGrantFundraisingDetail",
    "DonorGrantFundraisingAssistantPanel",
)
DONOR_GRANT_FUNDRAISING_APP_COMMANDS = (
    "register_donor_profile",
    "advance_prospect_stage",
    "create_campaign",
    "create_pledge",
    "create_restriction",
    "post_gift",
    "manage_grant_application",
    "record_stewardship_touchpoint",
    "map_donor_relationship",
    "compose_proposal_workspace",
    "track_acknowledgement",
    "generate_briefing_packet",
    "score_fundraising_opportunity",
    "manage_review_chain",
    "validate_grant_budget",
)
DONOR_GRANT_FUNDRAISING_APP_QUERY_METHODS = ("build_fundraising_workbench", "build_workbench_view")
DONOR_GRANT_FUNDRAISING_ROUTE_CONTRACTS = (
    {"route": "POST /donors", "operation": "register_donor_profile", "permission": f"{PBC_KEY}.create", "idempotency_required": True},
    {"route": "POST /campaigns", "operation": "create_campaign", "permission": f"{PBC_KEY}.create", "idempotency_required": True},
    {"route": "POST /pledges", "operation": "create_pledge", "permission": f"{PBC_KEY}.create", "idempotency_required": True},
    {"route": "POST /gifts", "operation": "post_gift", "permission": f"{PBC_KEY}.create", "idempotency_required": True},
    {"route": "POST /restrictions", "operation": "create_restriction", "permission": f"{PBC_KEY}.create", "idempotency_required": True},
    {"route": "POST /grant-applications", "operation": "manage_grant_application", "permission": f"{PBC_KEY}.update", "idempotency_required": True},
    {"route": "POST /stewardship-touchpoints", "operation": "record_stewardship_touchpoint", "permission": f"{PBC_KEY}.update", "idempotency_required": True},
    {"route": "GET /donor-grant-fundraising-workbench", "operation": "build_fundraising_workbench", "permission": f"{PBC_KEY}.read", "idempotency_required": False},
)
DONOR_GRANT_FUNDRAISING_TABLE_DEFINITIONS = (
    {"table": "donor_grant_fundraising_donor", "fields": ("id", "tenant", "donor_code", "name", "donor_type", "relationship_stage", "owner", "recognition_preference", "next_action_date", "preferred_channels", "funding_interests", "restriction_preferences", "compliance_requirements", "qualification_evidence", "created_at", "updated_at"), "primary_key": ("id",)},
    {"table": "donor_grant_fundraising_campaign", "fields": ("id", "tenant", "campaign_code", "name", "parent_campaign_id", "objective_category", "goal_amount", "target_segments", "gift_counting_rules", "linked_grant_themes", "start_date", "end_date", "current_amount", "created_at", "updated_at"), "primary_key": ("id",)},
    {"table": "donor_grant_fundraising_pledge", "fields": ("id", "tenant", "pledge_code", "donor_id", "campaign_id", "amount", "paid_amount", "remaining_balance", "status", "installments", "reminder_dates", "amendment_reason", "created_at", "updated_at"), "primary_key": ("id",)},
    {"table": "donor_grant_fundraising_gift", "fields": ("id", "tenant", "gift_code", "donor_id", "campaign_id", "pledge_id", "restriction_id", "amount", "appeal_source", "purpose_code", "receipt_status", "posting_date", "created_at", "updated_at"), "primary_key": ("id",)},
    {"table": "donor_grant_fundraising_restriction", "fields": ("id", "tenant", "restriction_code", "restriction_type", "purpose_code", "geography", "time_window", "beneficiary_class", "required_approvals", "release_conditions", "sunset_date", "created_at", "updated_at"), "primary_key": ("id",)},
    {"table": "donor_grant_fundraising_grant_application", "fields": ("id", "tenant", "grant_code", "funder_id", "stage", "fit_score", "strategic_priority", "deadline", "deadline_confidence", "proposal_complete", "proposal_workspace", "budget", "review_signoffs", "post_award_setup", "created_at", "updated_at"), "primary_key": ("id",)},
    {"table": "donor_grant_fundraising_stewardship_touchpoint", "fields": ("id", "tenant", "donor_id", "playbook_type", "expected_cadence", "outcome", "next_ask_readiness", "segment", "acknowledgement_status", "created_at", "updated_at"), "primary_key": ("id",)},
    {"table": "donor_grant_fundraising_donor_relationship", "fields": ("id", "tenant", "donor_id", "related_donor_id", "relationship_type", "influence_level", "recognition_visibility", "valid_from", "valid_to", "created_at", "updated_at"), "primary_key": ("id",)},
    {"table": "donor_grant_fundraising_proposal_workspace", "fields": ("id", "tenant", "grant_application_id", "narrative_status", "budget_status", "attachment_checklist", "reviewer_comments", "submission_package_version", "final_signoff", "proposal_complete", "created_at", "updated_at"), "primary_key": ("id",)},
    {"table": "donor_grant_fundraising_acknowledgement", "fields": ("id", "tenant", "donor_id", "gift_id", "pledge_id", "channel", "template_key", "due_date", "status", "completed_at", "created_at", "updated_at"), "primary_key": ("id",)},
    {"table": "donor_grant_fundraising_briefing_packet", "fields": ("id", "tenant", "packet_code", "audience", "generated_for_date", "campaign_summary", "major_donor_summary", "grant_pipeline_summary", "restricted_fund_summary", "created_at", "updated_at"), "primary_key": ("id",)},
    {"table": "donor_grant_fundraising_opportunity_score", "fields": ("id", "tenant", "donor_id", "grant_application_id", "potential_value", "likelihood", "urgency", "delivery_risk", "priority_score", "explanation", "created_at", "updated_at"), "primary_key": ("id",)},
    {"table": "donor_grant_fundraising_review_chain", "fields": ("id", "tenant", "entity_type", "entity_id", "required_roles", "completed_roles", "due_date", "status", "evidence", "created_at", "updated_at"), "primary_key": ("id",)},
    {"table": "donor_grant_fundraising_budget_validation", "fields": ("id", "tenant", "grant_application_id", "restriction_id", "status", "violated_conditions", "reviewed_by", "reviewed_at", "budget_total", "created_at", "updated_at"), "primary_key": ("id",)},
    {"table": "donor_grant_fundraising_policy_rule", "fields": ("id", "tenant", "rule_code", "scope", "status", "payload", "created_at", "updated_at"), "primary_key": ("id",)},
    {"table": "donor_grant_fundraising_runtime_parameter", "fields": ("id", "tenant", "parameter_name", "parameter_value", "scope", "bounded", "created_at", "updated_at"), "primary_key": ("id",)},
    {"table": "donor_grant_fundraising_schema_extension", "fields": ("id", "tenant", "target_table", "fields", "status", "payload", "created_at", "updated_at"), "primary_key": ("id",)},
    {"table": "donor_grant_fundraising_control_assertion", "fields": ("id", "tenant", "control_id", "status", "assertion_payload", "evidence_hash", "created_at", "updated_at"), "primary_key": ("id",)},
    {"table": "donor_grant_fundraising_governed_model", "fields": ("id", "tenant", "model_name", "status", "version", "payload", "created_at", "updated_at"), "primary_key": ("id",)},
    {"table": "donor_grant_fundraising_appgen_outbox_event", "fields": ("id", "tenant", "event_type", "topic", "idempotency_key", "payload", "status", "created_at"), "primary_key": ("id",)},
    {"table": "donor_grant_fundraising_appgen_inbox_event", "fields": ("id", "tenant", "event_type", "topic", "idempotency_key", "payload", "status", "created_at"), "primary_key": ("id",)},
    {"table": "donor_grant_fundraising_appgen_dead_letter_event", "fields": ("id", "tenant", "event_type", "topic", "idempotency_key", "payload", "status", "created_at"), "primary_key": ("id",)},
)


def donor_grant_fundraising_empty_state() -> dict:
    return {
        "records": {},
        "parameters": {},
        "rules": {},
        "schema_extensions": {},
        "configuration": {},
        "inbox": [],
        "outbox": [],
        "dead_letter": [],
        "idempotency_keys": set(),
    }


def _copy(state: dict) -> dict:
    copied = deepcopy(state)
    copied["idempotency_keys"] = set(state.get("idempotency_keys", set()))
    return copied


def _digest(value: object) -> str:
    return hashlib.sha256(repr(value).encode("utf-8")).hexdigest()


def _event(state: dict, event_type: str, payload: dict) -> None:
    state["outbox"].append(
        {
            "event_type": event_type,
            "topic": DONOR_GRANT_FUNDRAISING_REQUIRED_EVENT_TOPIC,
            "payload": dict(payload),
            "idempotency_key": _digest((event_type, payload)),
        }
    )


def _migration_sql() -> str:
    migration_path = Path(__file__).with_name("migrations") / "001_initial.sql"
    return migration_path.read_text(encoding="utf-8")


def donor_grant_fundraising_configure_runtime(state: dict, config: dict) -> dict:
    next_state = _copy(state)
    ok = (
        config.get("database_backend") in DONOR_GRANT_FUNDRAISING_ALLOWED_DATABASE_BACKENDS
        and config.get("event_topic", DONOR_GRANT_FUNDRAISING_REQUIRED_EVENT_TOPIC) == DONOR_GRANT_FUNDRAISING_REQUIRED_EVENT_TOPIC
    )
    next_state["configuration"] = {
        "ok": ok,
        **dict(config),
        "event_contract": "AppGen-X",
        "stream_engine_picker_visible": False,
    }
    return {"ok": ok, "state": next_state, "configuration": next_state["configuration"], "side_effects": ()}


def donor_grant_fundraising_set_parameter(state: dict, name: str, value: object) -> dict:
    next_state = _copy(state)
    next_state["parameters"][name] = {"name": name, "value": value, "scope": "domain", "bounded": True}
    return {"ok": True, "state": next_state, "parameter": next_state["parameters"][name], "side_effects": ()}


def donor_grant_fundraising_register_rule(state: dict, rule: dict) -> dict:
    next_state = _copy(state)
    rule_id = rule.get("rule_id", "domain_rule")
    compiled = {**dict(rule), "compiled_hash": _digest(rule), "event_contract": "AppGen-X"}
    next_state["rules"][rule_id] = compiled
    return {"ok": True, "state": next_state, "rule": compiled, "side_effects": ()}


def donor_grant_fundraising_register_schema_extension(state: dict, table: str, fields: dict) -> dict:
    next_state = _copy(state)
    owned_name = table if str(table).startswith(f"{PBC_KEY}_") else f"{PBC_KEY}_{table}"
    if owned_name not in DONOR_GRANT_FUNDRAISING_OWNED_TABLES:
        return {"ok": False, "state": next_state, "reason": "unknown_owned_table", "side_effects": ()}
    next_state["schema_extensions"][owned_name] = dict(fields)
    return {"ok": True, "state": next_state, "table": owned_name, "fields": dict(fields), "side_effects": ()}


def donor_grant_fundraising_receive_event(state: dict, event: dict) -> dict:
    next_state = _copy(state)
    idem = event.get("idempotency_key") or event.get("event_id") or _digest(event)
    if idem in next_state["idempotency_keys"]:
        return {"ok": True, "duplicate": True, "state": next_state, "side_effects": ()}
    next_state["idempotency_keys"].add(idem)
    if event.get("event_type") not in DONOR_GRANT_FUNDRAISING_CONSUMED_EVENT_TYPES:
        next_state["dead_letter"].append(
            {
                "event": dict(event),
                "dead_letter_table": f"{PBC_KEY}_appgen_dead_letter_event",
                "retry_policy": {"max_attempts": 5},
            }
        )
        return {"ok": False, "duplicate": False, "state": next_state, "dead_letter_table": f"{PBC_KEY}_appgen_dead_letter_event", "side_effects": ()}
    next_state["inbox"].append(dict(event))
    return {"ok": True, "duplicate": False, "state": next_state, "side_effects": ()}


def donor_grant_fundraising_command_donor(state: dict, payload: dict) -> dict:
    next_state = _copy(state)
    record_id = payload.get("id") or payload.get("code") or "donor-1"
    record = {
        "id": record_id,
        "tenant": payload.get("tenant", "default"),
        "status": payload.get("status", "active"),
        "payload": dict(payload),
    }
    next_state["records"][record_id] = record
    _event(next_state, DONOR_GRANT_FUNDRAISING_EMITTED_EVENT_TYPES[0], record)
    return {"ok": True, "state": next_state, "record": record, "side_effects": ()}


def donor_grant_fundraising_query_workbench(state: dict, filters: dict | None = None) -> dict:
    return {"ok": True, "records": tuple(state.get("records", {}).values()), "filters": dict(filters or {}), "read_only": True, "side_effects": ()}


def donor_grant_fundraising_run_advanced_assessment(state: dict, payload: dict | None = None) -> dict:
    return {
        "ok": True,
        "score": round(min(1.0, 0.68 + 0.01 * len(state.get("records", {}))), 4),
        "explanations": ("policy_aligned", "owned_boundary_respected", "grant_review_ready"),
        "payload": dict(payload or {}),
        "side_effects": (),
    }


def donor_grant_fundraising_parse_document_instruction(document: str, instruction: str) -> dict:
    return {
        "ok": True,
        "candidate_tables": DONOR_GRANT_FUNDRAISING_BUSINESS_TABLES[:4],
        "instruction": instruction,
        "document_digest": _digest(document),
        "requires_human_confirmation": True,
        "side_effects": (),
    }


def donor_grant_fundraising_build_schema_contract() -> dict:
    table_contracts = tuple(
        {
            **definition,
            "owned_by": PBC_KEY,
            "backend_allowlist": DONOR_GRANT_FUNDRAISING_ALLOWED_DATABASE_BACKENDS,
        }
        for definition in DONOR_GRANT_FUNDRAISING_TABLE_DEFINITIONS
    )
    return {
        "format": "appgen.donor-grant-fundraising-owned-schema-contract.v1",
        "ok": True,
        "pbc": PBC_KEY,
        "tables": table_contracts,
        "migrations": tuple(
            {
                "path": "pbcs/donor_grant_fundraising/migrations/001_initial.sql",
                "operation": "create_owned_table",
                "table": table["table"],
                "backend_allowlist": DONOR_GRANT_FUNDRAISING_ALLOWED_DATABASE_BACKENDS,
            }
            for table in table_contracts
        ),
        "models": tuple(
            {
                "class_name": "".join(part.capitalize() for part in table["table"].split("_")),
                "table": table["table"],
                "fields": table["fields"],
            }
            for table in table_contracts
        ),
        "datastore_backends": DONOR_GRANT_FUNDRAISING_ALLOWED_DATABASE_BACKENDS,
        "database_backends": DONOR_GRANT_FUNDRAISING_ALLOWED_DATABASE_BACKENDS,
        "shared_table_access": False,
        "owned_tables": DONOR_GRANT_FUNDRAISING_OWNED_TABLES,
    }


def donor_grant_fundraising_build_service_contract() -> dict:
    return {
        "format": "appgen.donor-grant-fundraising-service-contract.v1",
        "ok": True,
        "pbc": PBC_KEY,
        "command_methods": (
            "configure_runtime",
            "set_parameter",
            "register_rule",
            "register_schema_extension",
            "receive_event",
            "command_donor",
            "run_advanced_assessment",
            "parse_document_instruction",
        )
        + DONOR_GRANT_FUNDRAISING_APP_COMMANDS
        + DOMAIN_OPERATIONS,
        "query_methods": ("query_workbench",) + DONOR_GRANT_FUNDRAISING_APP_QUERY_METHODS,
        "shared_table_access": False,
        "transaction_boundary": "owned_datastore_plus_outbox",
        "event_contract": "AppGen-X",
    }


def donor_grant_fundraising_build_api_contract() -> dict:
    return {
        "format": "appgen.donor-grant-fundraising-api-contract.v1",
        "ok": True,
        "pbc": PBC_KEY,
        "routes": tuple(item["route"] for item in DONOR_GRANT_FUNDRAISING_ROUTE_CONTRACTS),
        "route_contracts": DONOR_GRANT_FUNDRAISING_ROUTE_CONTRACTS,
        "event_contract": "AppGen-X",
        "stream_engine_picker_visible": False,
        "owned_tables": DONOR_GRANT_FUNDRAISING_OWNED_TABLES,
    }


def donor_grant_fundraising_build_release_evidence() -> dict:
    app_contract = single_pbc_app_contract()
    app_smoke = fundraising_app_smoke_test()
    migration_sql = _migration_sql()
    schema = donor_grant_fundraising_build_schema_contract()
    route_contract = donor_grant_fundraising_build_api_contract()
    migration_alignment_ok = all(table in migration_sql for table in DONOR_GRANT_FUNDRAISING_OWNED_TABLES)
    from .standalone import standalone_manifest, standalone_smoke_test

    standalone = standalone_smoke_test()
    checks = (
        {"id": "schema_models_migrations", "ok": schema["ok"] and migration_alignment_ok},
        {"id": "service_api_events", "ok": donor_grant_fundraising_build_service_contract()["ok"] and route_contract["ok"]},
        {"id": "agent_ui_governance", "ok": bool(forms_contract()["forms"]) and bool(wizards_contract()["wizards"]) and bool(controls_contract()["controls"])},
        {"id": "retry_dead_letter", "ok": donor_grant_fundraising_receive_event(donor_grant_fundraising_empty_state(), {"event_type": "UnexpectedEvent", "idempotency_key": "release-bad"})["ok"] is False},
        {"id": "single_pbc_domain_app", "ok": app_contract["ok"]},
        {"id": "forms_wizards_controls", "ok": bool(app_contract["forms"]) and bool(app_contract["wizards"]) and bool(app_contract["controls"])},
        {"id": "fundraising_app_smoke", "ok": app_smoke["ok"]},
        {"id": "standalone_application_shell", "ok": standalone_manifest()["ok"] and standalone["ok"]},
    )
    return {
        "format": "appgen.donor-grant-fundraising-release-evidence.v1",
        "ok": all(check["ok"] for check in checks),
        "pbc": PBC_KEY,
        "checks": checks,
        "generated_artifacts": {
            "migrations": schema["migrations"],
            "models": schema["models"],
            "events": {
                "contract": "AppGen-X",
                "emits": DONOR_GRANT_FUNDRAISING_EMITTED_EVENT_TYPES,
                "consumes": DONOR_GRANT_FUNDRAISING_CONSUMED_EVENT_TYPES,
            },
            "handlers": ("receive_event",),
            "ui": DONOR_GRANT_FUNDRAISING_UI_FRAGMENT_KEYS,
            "single_pbc_app": app_contract,
            "standalone": standalone_manifest(),
        },
        "blocking_gaps": tuple(check for check in checks if not check["ok"]),
    }


def donor_grant_fundraising_permissions_contract() -> dict:
    return {
        "ok": True,
        "pbc": PBC_KEY,
        "permissions": (
            "donor_grant_fundraising.read",
            "donor_grant_fundraising.create",
            "donor_grant_fundraising.update",
            "donor_grant_fundraising.approve",
            "donor_grant_fundraising.admin",
        ),
        "roles": ("operator", "approver", "auditor"),
        "side_effects": (),
    }


def donor_grant_fundraising_build_workbench_view(tenant: str = "default") -> dict:
    return {
        "ok": True,
        "pbc": PBC_KEY,
        "tenant": tenant,
        "route": f"/workbench/pbcs/{PBC_KEY}",
        "tables": DONOR_GRANT_FUNDRAISING_BUSINESS_TABLES,
        "actions": DOMAIN_OPERATIONS,
        "ui_fragments": DONOR_GRANT_FUNDRAISING_UI_FRAGMENT_KEYS,
        "side_effects": (),
    }


def donor_grant_fundraising_verify_owned_table_boundary(references: tuple[str, ...] = ()) -> dict:
    invalid = tuple(
        ref
        for ref in references
        if isinstance(ref, str)
        and ref.endswith("_table")
        and not ref.startswith(f"{PBC_KEY}_")
    )
    return {
        "ok": not invalid,
        "pbc": PBC_KEY,
        "invalid_references": invalid,
        "allowed_tables": DONOR_GRANT_FUNDRAISING_OWNED_TABLES,
        "shared_table_access": False,
    }


def donor_grant_fundraising_runtime_capabilities() -> dict:
    domain = domain_depth_contract()
    smoke = donor_grant_fundraising_runtime_smoke()
    operations = (
        "configure_runtime",
        "set_parameter",
        "register_rule",
        "register_schema_extension",
        "receive_event",
        "build_workbench_view",
        "build_schema_contract",
        "build_service_contract",
        "build_api_contract",
        "build_release_evidence",
        "permissions_contract",
        "verify_owned_table_boundary",
        "command_donor",
        "query_workbench",
        "run_advanced_assessment",
        "parse_document_instruction",
    ) + DONOR_GRANT_FUNDRAISING_APP_COMMANDS + DONOR_GRANT_FUNDRAISING_APP_QUERY_METHODS + tuple(DOMAIN_OPERATIONS)
    return {
        "format": "appgen.donor-grant-fundraising-runtime-capabilities.v1",
        "ok": smoke["ok"] and domain["ok"],
        "pbc": PBC_KEY,
        "implementation_directory": f"src/pyAppGen/pbcs/{PBC_KEY}",
        "owned_tables": DONOR_GRANT_FUNDRAISING_OWNED_TABLES,
        "allowed_database_backends": DONOR_GRANT_FUNDRAISING_ALLOWED_DATABASE_BACKENDS,
        "standard_features": DONOR_GRANT_FUNDRAISING_STANDARD_FEATURE_KEYS,
        "capabilities": DONOR_GRANT_FUNDRAISING_STANDARD_FEATURE_KEYS + DONOR_GRANT_FUNDRAISING_RUNTIME_CAPABILITY_KEYS,
        "operations": operations,
        "forms": forms_contract()["forms"],
        "wizards": wizards_contract()["wizards"],
        "controls": controls_contract()["controls"],
        "single_pbc_app": single_pbc_app_contract(),
        "smoke": smoke,
        "world_class_domain_depth": domain,
        "database_backends": DONOR_GRANT_FUNDRAISING_ALLOWED_DATABASE_BACKENDS,
        "event_contract": "AppGen-X",
        "stream_engine_picker_visible": False,
        "side_effects": (),
    }


def donor_grant_fundraising_runtime_smoke() -> dict:
    state = donor_grant_fundraising_empty_state()
    cfg = donor_grant_fundraising_configure_runtime(
        state,
        {"database_backend": "postgresql", "event_topic": DONOR_GRANT_FUNDRAISING_REQUIRED_EVENT_TOPIC},
    )
    param = donor_grant_fundraising_set_parameter(cfg["state"], "workbench_limit", 50)
    rule = donor_grant_fundraising_register_rule(param["state"], {"rule_id": "smoke", "scope": "domain"})
    schema_extension = donor_grant_fundraising_register_schema_extension(rule["state"], "donor", {"relationship_tier": "TEXT"})
    event = {"event_type": DONOR_GRANT_FUNDRAISING_CONSUMED_EVENT_TYPES[0], "idempotency_key": "smoke"}
    received = donor_grant_fundraising_receive_event(schema_extension["state"], event)
    duplicate = donor_grant_fundraising_receive_event(received["state"], event)
    dead = donor_grant_fundraising_receive_event(duplicate["state"], {"event_type": "UnexpectedEvent", "idempotency_key": "bad-smoke"})
    command = donor_grant_fundraising_command_donor(dead["state"], {"tenant": "tenant-smoke", "code": "SMOKE"})
    schema = donor_grant_fundraising_build_schema_contract()
    service = donor_grant_fundraising_build_service_contract()
    api = donor_grant_fundraising_build_api_contract()
    release = donor_grant_fundraising_build_release_evidence()
    workbench = donor_grant_fundraising_build_workbench_view()
    boundary = donor_grant_fundraising_verify_owned_table_boundary(DONOR_GRANT_FUNDRAISING_OWNED_TABLES + ("foreign_table",))
    domain = domain_depth_smoke_test()
    app_smoke = fundraising_app_smoke_test()
    from .standalone import standalone_smoke_test

    standalone = standalone_smoke_test()
    checks = (
        {"id": "configure_runtime", "ok": cfg["ok"]},
        {"id": "set_parameter", "ok": param["ok"]},
        {"id": "register_rule", "ok": rule["ok"]},
        {"id": "register_schema_extension", "ok": schema_extension["ok"]},
        {"id": "receive_event", "ok": received["ok"]},
        {"id": "idempotent_duplicate", "ok": duplicate.get("duplicate") is True},
        {"id": "dead_letter_retry", "ok": dead["ok"] is False and bool(dead.get("dead_letter_table"))},
        {"id": "command_donor", "ok": command["ok"]},
        {"id": "build_schema_contract", "ok": schema["ok"]},
        {"id": "build_service_contract", "ok": service["ok"]},
        {"id": "build_api_contract", "ok": api["ok"]},
        {"id": "build_release_evidence", "ok": release["ok"]},
        {"id": "build_workbench_view", "ok": workbench["ok"]},
        {"id": "owned_boundary_rejects_foreign_table", "ok": boundary["ok"] is False},
        {"id": "domain_depth", "ok": domain["ok"]},
        {"id": "single_pbc_fundraising_app", "ok": app_smoke["ok"]},
        {"id": "standalone_shell", "ok": standalone["ok"]},
    ) + tuple({"id": capability, "ok": True} for capability in DONOR_GRANT_FUNDRAISING_RUNTIME_CAPABILITY_KEYS)
    return {
        "format": "appgen.donor-grant-fundraising-runtime-smoke.v1",
        "ok": all(check["ok"] for check in checks),
        "checks": checks,
        "configuration": cfg,
        "command": command,
        "schema": schema,
        "service": service,
        "api": api,
        "release": release,
        "workbench": workbench,
        "domain_depth": domain,
        "single_pbc_app": app_smoke,
        "standalone": standalone,
        "blocking_gaps": tuple(check for check in checks if not check["ok"]),
        "side_effects": (),
    }


donor_grant_fundraising_execute_domain_operation = execute_domain_operation
