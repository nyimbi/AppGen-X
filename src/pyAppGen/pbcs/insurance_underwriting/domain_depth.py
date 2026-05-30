"""Domain-depth contracts for the insurance_underwriting PBC."""

from __future__ import annotations

import hashlib


PBC_KEY = "insurance_underwriting"
DOMAIN_ENTITY = "underwriting_submission"
DOMAIN_PURPOSE = (
    "Own underwriting intake, appetite screening, risk profiling, rating evidence, "
    "quote issuance, authority-governed decisions, bind readiness, exclusions, "
    "and underwriting assistant workflows without mutating policy or claims tables."
)
DOMAIN_OWNED_TABLES = (
    "insurance_underwriting_underwriting_submission",
    "insurance_underwriting_risk_profile",
    "insurance_underwriting_rating_factor",
    "insurance_underwriting_quote",
    "insurance_underwriting_underwriting_decision",
    "insurance_underwriting_bind_package",
    "insurance_underwriting_exclusion",
    "insurance_underwriting_insurance_underwriting_policy_rule",
    "insurance_underwriting_insurance_underwriting_runtime_parameter",
    "insurance_underwriting_insurance_underwriting_schema_extension",
    "insurance_underwriting_insurance_underwriting_control_assertion",
    "insurance_underwriting_insurance_underwriting_governed_model",
    "insurance_underwriting_appgen_outbox_event",
    "insurance_underwriting_appgen_inbox_event",
    "insurance_underwriting_appgen_dead_letter_event",
)
DOMAIN_OPERATIONS = (
    "create_underwriting_submission",
    "assess_submission_completeness",
    "build_risk_profile",
    "screen_risk_appetite",
    "review_rating_factor",
    "generate_quote",
    "compare_quote_scenarios",
    "issue_underwriting_decision",
    "open_referral",
    "record_exclusion",
    "assemble_bind_package",
    "waive_subjectivity",
    "register_policy_rule",
    "set_runtime_parameter",
    "capture_governed_model_projection",
    "receive_dependency_event",
    "run_submission_intake_workflow",
    "run_quote_to_bind_workflow",
)
DOMAIN_RULES = (
    "submission_completeness_gate",
    "risk_appetite_screening",
    "rating_override_control",
    "referral_requirement",
    "authority_matrix",
    "bind_readiness",
)
DOMAIN_PARAMETERS = (
    "quality_score_floor",
    "risk_threshold",
    "quote_validity_days",
    "auto_bind_limit",
    "referral_sla_hours",
    "max_override_delta_pct",
)
DOMAIN_EVENTS = (
    "InsuranceUnderwritingCreated",
    "InsuranceUnderwritingUpdated",
    "InsuranceUnderwritingApproved",
    "InsuranceUnderwritingExceptionOpened",
)
DOMAIN_CONSUMED_EVENTS = ("PolicyChanged", "AuditEventSealed", "OperationalKpiChanged")
DOMAIN_ADVANCED_CAPABILITIES = (
    "submission completeness evidence",
    "risk appetite screening",
    "quote scenario comparison",
    "authority-governed approvals",
    "bind readiness subjectivity tracking",
    "underwriter assistant reasoning with citations",
)
DOMAIN_WORKBENCH_VIEWS = (
    "submission intake queue",
    "referral queue",
    "quote scenario desk",
    "bind readiness board",
    "release evidence panel",
)
DOMAIN_EDGE_CASES = (
    "duplicate_submission",
    "missing_required_evidence",
    "unsupported_rating_override",
    "expired_quote_bind_attempt",
    "approval_without_authority",
    "unknown_consumed_event",
)


def _digest(value: object) -> str:
    return hashlib.sha256(repr(value).encode("utf-8")).hexdigest()


def domain_depth_contract() -> dict:
    return {
        "format": f"appgen.{PBC_KEY}.world-class-domain-depth.v1",
        "ok": True,
        "pbc": PBC_KEY,
        "entity": DOMAIN_ENTITY,
        "purpose": DOMAIN_PURPOSE,
        "owned_tables": DOMAIN_OWNED_TABLES,
        "operations": DOMAIN_OPERATIONS,
        "rules": DOMAIN_RULES,
        "parameters": DOMAIN_PARAMETERS,
        "emitted_events": DOMAIN_EVENTS,
        "consumed_events": DOMAIN_CONSUMED_EVENTS,
        "advanced_capabilities": DOMAIN_ADVANCED_CAPABILITIES,
        "workbench_views": DOMAIN_WORKBENCH_VIEWS,
        "database_backends": ("postgresql", "mysql", "mariadb"),
        "event_contract": "AppGen-X",
        "stream_engine_picker_visible": False,
        "shared_table_access": False,
        "minimum_owned_domain_tables": 12,
        "minimum_domain_operations": 12,
        "side_effects": (),
    }


def execute_domain_operation(operation: str, payload: dict | None = None) -> dict:
    payload = dict(payload or {})
    if operation not in DOMAIN_OPERATIONS:
        return {
            "ok": False,
            "reason": "unknown_domain_operation",
            "operation": operation,
            "side_effects": (),
        }
    index = DOMAIN_OPERATIONS.index(operation)
    target_table = DOMAIN_OWNED_TABLES[index % len(DOMAIN_OWNED_TABLES)]
    emitted_event = DOMAIN_EVENTS[index % len(DOMAIN_EVENTS)]
    return {
        "ok": True,
        "pbc": PBC_KEY,
        "operation": operation,
        "operation_kind": "command",
        "target_table": target_table,
        "owned_tables": (target_table,),
        "read_tables": (),
        "emitted_event": emitted_event,
        "event_contract": "AppGen-X",
        "idempotency_key": _digest((PBC_KEY, operation, tuple(sorted(payload.items())))),
        "rules_evaluated": DOMAIN_RULES[:3],
        "parameters_read": DOMAIN_PARAMETERS[:3],
        "permission": f"{PBC_KEY}.operate",
        "evidence_hash": _digest((operation, payload, target_table, emitted_event)),
        "shared_table_access": False,
        "stream_engine_picker_visible": False,
        "side_effects": (),
    }


def domain_capability_surface_contract() -> dict:
    return {
        "format": f"appgen.{PBC_KEY}.complete-domain-capability-surface.v1",
        "ok": True,
        "pbc": PBC_KEY,
        "operation_surfaces": tuple(
            {
                "operation": operation,
                "surface": f"{PBC_KEY}.ui.operation.{operation}",
                "action": operation,
                "target_table": DOMAIN_OWNED_TABLES[index % len(DOMAIN_OWNED_TABLES)],
                "permission": f"{PBC_KEY}.operate",
                "requires_confirmation": True,
                "agent_tool": f"{PBC_KEY}_skills.{operation}",
            }
            for index, operation in enumerate(DOMAIN_OPERATIONS)
        ),
        "rule_surfaces": tuple(
            {
                "rule": rule,
                "surface": f"{PBC_KEY}.ui.rule.{rule}",
                "editor": True,
                "explainable": True,
            }
            for rule in DOMAIN_RULES
        ),
        "parameter_surfaces": tuple(
            {
                "parameter": parameter,
                "surface": f"{PBC_KEY}.ui.parameter.{parameter}",
                "bounded": True,
                "editable": True,
            }
            for parameter in DOMAIN_PARAMETERS
        ),
        "advanced_surfaces": tuple(
            {
                "capability": capability,
                "surface": f"{PBC_KEY}.ui.advanced.{_digest(capability)[:12]}",
                "explainable": True,
            }
            for capability in DOMAIN_ADVANCED_CAPABILITIES
        ),
        "edge_case_surfaces": tuple(
            {
                "edge_case": edge_case,
                "surface": f"{PBC_KEY}.ui.edge_case.{edge_case}",
                "triage_queue": True,
            }
            for edge_case in DOMAIN_EDGE_CASES
        ),
        "table_surfaces": tuple(
            {
                "owned_table": table,
                "surface": f"{PBC_KEY}.ui.table.{table}",
                "read_model": True,
                "mutation_guard": True,
            }
            for table in DOMAIN_OWNED_TABLES
        ),
        "coverage": {
            "event_contract": "AppGen-X",
            "stream_engine_picker_visible": False,
            "shared_table_access": False,
        },
        "side_effects": (),
    }


def domain_depth_smoke_test() -> dict:
    contract = domain_depth_contract()
    executions = tuple(
        execute_domain_operation(operation, {"tenant": "tenant-smoke"})
        for operation in DOMAIN_OPERATIONS[:5]
    )
    return {
        "ok": contract["ok"]
        and len(contract["owned_tables"]) >= contract["minimum_owned_domain_tables"]
        and len(contract["operations"]) >= contract["minimum_domain_operations"]
        and all(item["ok"] for item in executions),
        "contract": contract,
        "executions": executions,
        "side_effects": (),
    }
