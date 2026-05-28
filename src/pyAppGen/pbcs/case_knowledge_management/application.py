"""Executable one-PBC application runtime for case_knowledge_management."""

from __future__ import annotations

from copy import deepcopy
from datetime import UTC
from datetime import datetime
from datetime import timedelta
import hashlib

from .config import DEFAULT_CONFIGURATION
from .config import compile_rule
from .config import default_parameters
from .config import default_rules
from .config import evaluate_rule
from .config import set_parameter as validate_parameter_value
from .config import validate_configuration
from .domain_depth import ALLOWED_DATABASE_BACKENDS
from .domain_depth import DOMAIN_CONSUMED_EVENTS
from .domain_depth import DOMAIN_EVENTS
from .domain_depth import DOMAIN_OPERATIONS
from .domain_depth import OPERATION_EVENT_MAP
from .domain_depth import PBC_KEY
from .domain_depth import QUERY_OPERATIONS
from .domain_depth import REQUIRED_EVENT_TOPIC
from .events import build_event_envelope
from .models import OWNED_TABLES
from .models import resolve_owned_table
from .models import resolve_table_spec
from .permissions import authorize
from .seed_data import seed_plan


def _now() -> str:
    return datetime.now(UTC).replace(microsecond=0).isoformat()


def _score_impact(payload: dict) -> float:
    affected_users = float(payload.get("affected_users", 1))
    tier_weight = {"strategic": 1.0, "enterprise": 0.9, "standard": 0.6}.get(
        payload.get("customer_tier", "standard"),
        0.5,
    )
    declared = {"critical": 1.0, "high": 0.8, "medium": 0.55, "low": 0.25}.get(
        payload.get("severity", "medium"),
        0.5,
    )
    impact = min(1.0, declared * 0.55 + tier_weight * 0.25 + min(1.0, affected_users / 1000.0) * 0.20)
    return round(impact, 3)


def _classify_text(text: str) -> tuple[str, str, str, float, str]:
    normalized = text.lower()
    if any(term in normalized for term in ("invoice", "billing", "refund", "payment")):
        return ("billing.issue", "billing", "invoice mismatch", 0.88, "Matched finance and billing keywords.")
    if any(term in normalized for term in ("api", "token", "latency", "timeout", "500")):
        return ("platform.api", "platform", "api reliability", 0.9, "Matched platform incident keywords.")
    if any(term in normalized for term in ("login", "access", "permission", "sso")):
        return ("identity.access", "identity", "authentication problem", 0.84, "Matched identity and access keywords.")
    return ("general.support", "general", "general assistance", 0.67, "Fallback classification applied.")


def _article_keywords(title: str, body: str, product_area: str) -> list[str]:
    keywords = {product_area.lower()}
    for token in f"{title} {body}".lower().replace("/", " ").replace("-", " ").split():
        if len(token) >= 4:
            keywords.add(token.strip(".,:;()[]{}"))
    return sorted(keywords)


class CaseKnowledgeManagementApp:
    """Simple, stateful app slice that keeps all records inside PBC-owned tables."""

    def __init__(self, state: dict | None = None) -> None:
        if state is None:
            self.state = self._new_state()
            self.install_defaults()
        else:
            self.state = deepcopy(state)
            self._normalize_state()

    def _new_state(self) -> dict:
        return {
            "pbc": PBC_KEY,
            "configuration": dict(DEFAULT_CONFIGURATION),
            "tables": {table: {} for table in OWNED_TABLES},
            "counters": {},
            "outbox": [],
            "inbox": [],
            "dead_letter": [],
            "idempotency_keys": set(),
            "release_notes": [],
        }

    def _normalize_state(self) -> None:
        self.state.setdefault("pbc", PBC_KEY)
        self.state.setdefault("configuration", dict(DEFAULT_CONFIGURATION))
        self.state.setdefault("tables", {})
        for table in OWNED_TABLES:
            self.state["tables"].setdefault(table, {})
        self.state.setdefault("counters", {})
        self.state.setdefault("outbox", [])
        self.state.setdefault("inbox", [])
        self.state.setdefault("dead_letter", [])
        self.state.setdefault("idempotency_keys", set())
        self.state.setdefault("release_notes", [])

    def snapshot(self) -> dict:
        return deepcopy(self.state)

    def install_defaults(self) -> None:
        for row in seed_plan()["rows"]:
            self._insert(row["table"], row["values"])
        for parameter in default_parameters():
            self._insert(
                "case_runtime_parameter",
                {
                    "id": f"parameter-{parameter['key']}",
                    "tenant": "default",
                    **parameter,
                },
            )
        for rule in default_rules():
            self._insert(
                "case_policy_rule",
                {
                    "id": f"rule-{rule['rule_id']}",
                    "tenant": "default",
                    "code": rule["rule_id"],
                    "scope": rule["scope"],
                    "status": "active",
                    "condition": rule["condition"],
                    "outcome": rule["outcome"],
                    "compiled_hash": rule["compiled_hash"],
                },
            )
        starter_article = self._insert(
            "knowledge_article",
            {
                "id": "article-api-timeout-playbook",
                "tenant": "default",
                "code": "KB-API-TIMEOUT",
                "title": "Investigating public API timeout incidents",
                "audience": "support_agent",
                "product_area": "platform",
                "lifecycle_state": "published",
                "freshness_state": "current",
                "current_version": 1,
                "quality_score": 0.84,
            },
        )
        self._insert(
            "article_version",
            {
                "id": "article-version-api-timeout-1",
                "tenant": "default",
                "article_id": starter_article["id"],
                "version_number": 1,
                "change_summary": "Initial troubleshooting workflow for API timeouts.",
                "body": "Check status page, inspect token validity, compare regional error rates, and confirm mitigation window.",
                "reviewer": "support-approver",
                "published_at": _now(),
            },
        )
        self._insert(
            "semantic_knowledge_index",
            {
                "id": "semantic-api-timeout-1",
                "tenant": "default",
                "article_id": starter_article["id"],
                "embedding_key": "kb-api-timeout-v1",
                "keywords": _article_keywords(
                    starter_article["title"],
                    "Check status page, inspect token validity, compare regional error rates, and confirm mitigation window.",
                    starter_article["product_area"],
                ),
                "quality_band": "trusted",
            },
        )
        self._insert(
            "content_freshness_signal",
            {
                "id": "freshness-api-timeout-1",
                "tenant": "default",
                "article_id": starter_article["id"],
                "signal_type": "publish",
                "state": "current",
                "review_due_at": self._future(days=30),
            },
        )

    def _future(self, *, hours: int = 0, days: int = 0) -> str:
        return (datetime.now(UTC).replace(microsecond=0) + timedelta(hours=hours, days=days)).isoformat()

    def _next_id(self, prefix: str) -> str:
        counters = self.state["counters"]
        counters[prefix] = counters.get(prefix, 0) + 1
        return f"{prefix}-{counters[prefix]:04d}"

    def _table_rows(self, table: str) -> dict:
        return self.state["tables"][resolve_owned_table(table)]

    def _insert(self, table: str, values: dict) -> dict:
        spec = resolve_table_spec(table)
        row = {}
        now = _now()
        for field in spec["fields"]:
            name = field["name"]
            if name in values:
                row[name] = deepcopy(values[name])
            elif name == "id":
                row[name] = self._next_id(spec["logical_table"])
            elif name == "created_at" or name == "updated_at":
                row[name] = now
            elif "default" in field:
                row[name] = deepcopy(field["default"])
            elif field.get("required") or field.get("nullable") is False:
                raise ValueError(f"Missing required field {name} for {spec['owned_table']}")
        owned_table = spec["owned_table"]
        self.state["tables"][owned_table][row["id"]] = row
        return row

    def _update(self, table: str, row_id: str, **changes: object) -> dict:
        rows = self._table_rows(table)
        row = rows[row_id]
        row.update(changes)
        row["updated_at"] = _now()
        return row

    def _emit(self, event_type: str, aggregate_id: str, payload: dict) -> dict:
        envelope = build_event_envelope(event_type, payload, aggregate_id=aggregate_id)
        event_row = self._insert(
            "appgen_outbox_event",
            {
                "tenant": payload.get("tenant", "default"),
                "event_type": event_type,
                "aggregate_id": aggregate_id,
                "status": "pending",
                "idempotency_key": envelope["idempotency_key"],
                "payload": payload,
            },
        )
        self.state["outbox"].append(event_row)
        return event_row

    def _queue_by_code(self, code: str) -> dict | None:
        for row in self._table_rows("case_queue").values():
            if row["code"] == code:
                return row
        return None

    def _article(self, article_id: str) -> dict:
        return self._table_rows("knowledge_article")[article_id]

    def _support_case(self, case_id: str) -> dict:
        return self._table_rows("support_case")[case_id]

    def _parameter_value(self, key: str, default: object | None = None) -> object:
        for row in self._table_rows("case_runtime_parameter").values():
            if row["key"] == key:
                return row["value"]
        return default

    def _open_case_count_for_assignee(self, assignee_id: str) -> int:
        assignments = self._table_rows("case_assignment").values()
        return sum(1 for row in assignments if row["assignee_id"] == assignee_id and row["status"] != "closed")

    def _current_quality_score(self, article_id: str) -> float:
        scores = [
            row["overall_score"]
            for row in self._table_rows("article_quality_score").values()
            if row["article_id"] == article_id
        ]
        return round(scores[-1], 3) if scores else self._article(article_id)["quality_score"]

    def configure_runtime(self, config: dict) -> dict:
        validation = validate_configuration(config)
        self.state["configuration"] = validation["config"]
        return {
            "ok": validation["ok"],
            "state": self.snapshot(),
            "configuration": validation["config"],
            "side_effects": (),
        }

    def set_parameter(self, key: str, value: object) -> dict:
        validated = validate_parameter_value(self.state, key, value)
        if not validated["ok"]:
            return {**validated, "state": self.snapshot()}
        existing = next(
            (row for row in self._table_rows("case_runtime_parameter").values() if row["key"] == key),
            None,
        )
        if existing is None:
            parameter = self._insert(
                "case_runtime_parameter",
                {
                    "tenant": "default",
                    "key": key,
                    "scope": validated["parameter_scope"],
                    "value": value,
                    "value_type": type(value).__name__,
                    "bounded": True,
                },
            )
        else:
            parameter = self._update(
                "case_runtime_parameter",
                existing["id"],
                value=value,
                value_type=type(value).__name__,
            )
        return {"ok": True, "state": self.snapshot(), "parameter": parameter, "side_effects": ()}

    def register_rule(self, rule: dict) -> dict:
        compiled = compile_rule(rule)
        if not compiled["ok"]:
            return {**compiled, "state": self.snapshot()}
        existing = next(
            (row for row in self._table_rows("case_policy_rule").values() if row["code"] == rule["rule_id"]),
            None,
        )
        payload = {
            "tenant": "default",
            "code": rule["rule_id"],
            "scope": rule["scope"],
            "status": "active",
            "condition": rule["condition"],
            "outcome": rule["outcome"],
            "compiled_hash": compiled["rule"]["compiled_hash"],
        }
        stored = self._insert("case_policy_rule", payload) if existing is None else self._update("case_policy_rule", existing["id"], **payload)
        return {"ok": True, "state": self.snapshot(), "rule": stored, "side_effects": ()}

    def register_schema_extension(self, table: str, fields: dict) -> dict:
        owned_table = resolve_owned_table(table)
        if owned_table not in OWNED_TABLES:
            return {
                "ok": False,
                "reason": "unknown_owned_table",
                "state": self.snapshot(),
                "side_effects": (),
            }
        records = []
        for field_name, field_type in dict(fields).items():
            records.append(
                self._insert(
                    "case_schema_extension",
                    {
                        "tenant": "default",
                        "table_name": owned_table,
                        "field_name": field_name,
                        "field_type": str(field_type),
                        "reason": "package_local_extension",
                    },
                )
            )
        return {
            "ok": True,
            "state": self.snapshot(),
            "table": owned_table,
            "fields": tuple(records),
            "side_effects": (),
        }

    def create_support_case(self, payload: dict) -> dict:
        title = payload.get("title") or payload.get("subject") or "Untitled support issue"
        summary = payload.get("summary") or payload.get("description") or title
        severity = payload.get("severity", "medium")
        product_area = payload.get("product_area", "general")
        case_record = self._insert(
            "support_case",
            {
                "tenant": payload.get("tenant", "default"),
                "code": payload.get("code", f"CASE-{self._next_id('case-code')}"),
                "channel": payload.get("channel", "portal"),
                "status": "open",
                "title": title,
                "summary": summary,
                "customer_ref": payload.get("customer_ref", "anonymous"),
                "product_area": product_area,
                "severity": severity,
                "impact_score": _score_impact(payload),
                "queue_code": payload.get("queue_code"),
                "owner_id": payload.get("owner_id"),
                "duplicate_of": payload.get("duplicate_of"),
                "knowledge_gap": bool(payload.get("knowledge_gap", False)),
            },
        )
        contact = None
        if payload.get("contact"):
            contact = self._insert(
                "case_contact",
                {
                    "tenant": case_record["tenant"],
                    "case_id": case_record["id"],
                    "role": payload["contact"].get("role", "requester"),
                    "name": payload["contact"].get("name", "Unknown"),
                    "email": payload["contact"].get("email", "unknown@example.com"),
                    "authority_level": payload["contact"].get("authority_level", "requester"),
                    "notification_preference": payload["contact"].get("notification_preference", "email"),
                    "language": payload["contact"].get("language", "en"),
                    "status": "active",
                },
            )
        self._emit("CaseCreated", case_record["id"], {"tenant": case_record["tenant"], "case_id": case_record["id"], "severity": severity})
        self.state["release_notes"].append(f"Created support case {case_record['code']} for {product_area}.")
        return {
            "ok": True,
            "state": self.snapshot(),
            "record": case_record,
            "contact": contact,
            "next_actions": ("classify_case", "route_case_queue", "start_sla_timer"),
            "side_effects": (),
        }

    def classify_case(self, payload: dict) -> dict:
        case_record = self._support_case(payload["case_id"])
        taxonomy, component, symptom, confidence, rationale = _classify_text(
            f"{case_record['title']} {case_record['summary']} {payload.get('extra_text', '')}"
        )
        classification = self._insert(
            "case_classification",
            {
                "tenant": case_record["tenant"],
                "case_id": case_record["id"],
                "taxonomy_code": payload.get("taxonomy_code", taxonomy),
                "product_component": payload.get("product_component", component),
                "symptom": payload.get("symptom", symptom),
                "confidence": payload.get("confidence", confidence),
                "rationale": payload.get("rationale", rationale),
            },
        )
        self._update("support_case", case_record["id"], product_area=classification["product_component"])
        self._emit("CaseClassified", case_record["id"], {"tenant": case_record["tenant"], "case_id": case_record["id"], "taxonomy_code": classification["taxonomy_code"]})
        return {"ok": True, "state": self.snapshot(), "record": classification, "side_effects": ()}

    def route_case_queue(self, payload: dict) -> dict:
        case_record = self._support_case(payload["case_id"])
        queue_code = payload.get("queue_code")
        if not queue_code:
            if case_record["severity"] in {"critical", "high"}:
                queue_code = "api-platform" if case_record["product_area"] == "platform" else "triage-global"
            elif case_record["product_area"] == "billing":
                queue_code = "billing-escalations"
            else:
                queue_code = "triage-global"
        queue = self._queue_by_code(queue_code)
        if queue is None:
            return {"ok": False, "reason": "queue_not_found", "state": self.snapshot(), "side_effects": ()}
        active_load = queue["active_load"] + 1
        health = "at_capacity" if active_load >= queue["capacity_limit"] else "healthy"
        queue = self._update("case_queue", queue["id"], active_load=active_load, health=health)
        case_record = self._update("support_case", case_record["id"], queue_code=queue["code"])
        return {"ok": True, "state": self.snapshot(), "queue": queue, "record": case_record, "side_effects": ()}

    def assign_case(self, payload: dict) -> dict:
        case_record = self._support_case(payload["case_id"])
        queue = self._queue_by_code(case_record["queue_code"] or "triage-global")
        if queue is None:
            return {"ok": False, "reason": "queue_not_routed", "state": self.snapshot(), "side_effects": ()}
        candidates = tuple(payload.get("candidate_agents", ())) or ("agent-alex", "agent-nia", "agent-tendo")
        assignee = min(candidates, key=self._open_case_count_for_assignee)
        workload = round(0.2 + self._open_case_count_for_assignee(assignee) * 0.15, 3)
        assignment = self._insert(
            "case_assignment",
            {
                "tenant": case_record["tenant"],
                "case_id": case_record["id"],
                "queue_id": queue["id"],
                "assignee_id": assignee,
                "status": "assigned",
                "rationale": f"Selected {assignee} from {queue['code']} using workload-aware routing.",
                "workload_score": workload,
            },
        )
        self._update("support_case", case_record["id"], owner_id=assignee, status="assigned")
        self._emit("CaseAssigned", case_record["id"], {"tenant": case_record["tenant"], "case_id": case_record["id"], "assignee_id": assignee})
        return {"ok": True, "state": self.snapshot(), "record": assignment, "side_effects": ()}

    def start_sla_timer(self, payload: dict) -> dict:
        case_record = self._support_case(payload["case_id"])
        severity = case_record["severity"]
        response_hours = {"critical": 1, "high": 2, "medium": 4, "low": 8}[severity]
        resolution_hours = {"critical": 4, "high": 8, "medium": 24, "low": 72}[severity]
        queue = self._queue_by_code(case_record["queue_code"] or "triage-global")
        queue_pressure = 0 if queue is None else queue["active_load"] / max(queue["capacity_limit"], 1)
        risk_score = round(min(1.0, case_record["impact_score"] * 0.65 + queue_pressure * 0.35), 3)
        if severity == "critical":
            risk_score = max(risk_score, 0.82)
        elif severity == "high":
            risk_score = max(risk_score, 0.58)
        risk_level = "high" if risk_score >= 0.8 else "watch" if risk_score >= 0.55 else "stable"
        sla = self._insert(
            "case_sla",
            {
                "tenant": case_record["tenant"],
                "case_id": case_record["id"],
                "policy_code": payload.get("policy_code", "default-sla"),
                "first_response_due_at": self._future(hours=response_hours),
                "resolution_due_at": self._future(hours=resolution_hours),
                "paused": False,
                "risk_level": risk_level,
                "risk_score": risk_score,
            },
        )
        timer_event = self._insert(
            "sla_timer_event",
            {
                "tenant": case_record["tenant"],
                "case_id": case_record["id"],
                "sla_id": sla["id"],
                "timer_kind": "response_and_resolution",
                "event_kind": "started",
                "reason": "case_created",
                "event_at": _now(),
            },
        )
        self._emit("SlaRiskChanged", case_record["id"], {"tenant": case_record["tenant"], "case_id": case_record["id"], "risk_level": risk_level, "risk_score": risk_score})
        return {"ok": True, "state": self.snapshot(), "record": sla, "timer_event": timer_event, "side_effects": ()}

    def record_case_interaction(self, payload: dict) -> dict:
        case_record = self._support_case(payload["case_id"])
        interaction = self._insert(
            "case_interaction",
            {
                "tenant": case_record["tenant"],
                "case_id": case_record["id"],
                "channel": payload.get("channel", "email"),
                "visibility": payload.get("visibility", "external"),
                "author_role": payload.get("author_role", "support_agent"),
                "sentiment": payload.get("sentiment", "neutral"),
                "summary": payload.get("summary", "Interaction recorded."),
                "requires_follow_up": bool(payload.get("requires_follow_up", False)),
            },
        )
        if interaction["sentiment"] in {"frustrated", "angry"}:
            self._insert(
                "case_control_assertion",
                {
                    "tenant": case_record["tenant"],
                    "control_code": "friction_detected",
                    "subject_ref": case_record["id"],
                    "status": "active",
                    "evidence": interaction["summary"],
                },
            )
        return {"ok": True, "state": self.snapshot(), "record": interaction, "side_effects": ()}

    def open_case_escalation(self, payload: dict) -> dict:
        case_record = self._support_case(payload["case_id"])
        escalation = self._insert(
            "case_escalation",
            {
                "tenant": case_record["tenant"],
                "case_id": case_record["id"],
                "level": payload.get("level", "L2"),
                "reason": payload.get("reason", "SLA or business risk escalation."),
                "target_team": payload.get("target_team", "product-engineering"),
                "status": "open",
                "opened_at": _now(),
            },
        )
        self._update("support_case", case_record["id"], status="escalated")
        self._emit("CaseEscalated", case_record["id"], {"tenant": case_record["tenant"], "case_id": case_record["id"], "level": escalation["level"]})
        return {"ok": True, "state": self.snapshot(), "record": escalation, "side_effects": ()}

    def resolve_case(self, payload: dict) -> dict:
        case_record = self._support_case(payload["case_id"])
        resolution = self._insert(
            "case_resolution",
            {
                "tenant": case_record["tenant"],
                "case_id": case_record["id"],
                "resolution_type": payload.get("resolution_type", "knowledge_guided_fix"),
                "summary": payload.get("summary", "Issue resolved."),
                "workaround": payload.get("workaround"),
                "confirmed": bool(payload.get("confirmed", True)),
                "resolved_at": _now(),
            },
        )
        self._update("support_case", case_record["id"], status="resolved", knowledge_gap=bool(payload.get("knowledge_gap", False)))
        self._emit("CaseResolved", case_record["id"], {"tenant": case_record["tenant"], "case_id": case_record["id"], "resolution_type": resolution["resolution_type"]})
        return {"ok": True, "state": self.snapshot(), "record": resolution, "side_effects": ()}

    def publish_knowledge_article(self, payload: dict) -> dict:
        sensitive = bool(payload.get("sensitive", False))
        approved_by = payload.get("approved_by")
        approval_gate = evaluate_rule(
            compile_rule(
                {
                    "rule_id": "knowledge_publish_policy",
                    "scope": "knowledge",
                    "condition": "approval_required_for_sensitive_publish",
                    "outcome": "publish_gate",
                }
            ),
            {"sensitive": sensitive, "approved_by": approved_by},
        )
        lifecycle_state = "published" if approval_gate["allowed"] else "pending_approval"
        article = self._insert(
            "knowledge_article",
            {
                "tenant": payload.get("tenant", "default"),
                "code": payload.get("code", f"KB-{self._next_id('kb-code')}"),
                "title": payload.get("title", "Untitled knowledge article"),
                "audience": payload.get("audience", "support_agent"),
                "product_area": payload.get("product_area", "general"),
                "lifecycle_state": lifecycle_state,
                "freshness_state": "current",
                "current_version": 1,
                "quality_score": 0.82,
            },
        )
        version = self._insert(
            "article_version",
            {
                "tenant": article["tenant"],
                "article_id": article["id"],
                "version_number": 1,
                "change_summary": payload.get("change_summary", "Initial release"),
                "body": payload.get("body", payload.get("summary", "Knowledge content pending.")),
                "reviewer": approved_by,
                "published_at": _now() if lifecycle_state == "published" else None,
            },
        )
        approval = self._insert(
            "knowledge_approval",
            {
                "tenant": article["tenant"],
                "article_id": article["id"],
                "approver_id": approved_by or "approval-queue",
                "decision": "approved" if lifecycle_state == "published" else "pending",
                "reason": payload.get("approval_reason"),
                "decided_at": _now(),
            },
        )
        self._insert(
            "semantic_knowledge_index",
            {
                "tenant": article["tenant"],
                "article_id": article["id"],
                "embedding_key": f"{article['code'].lower()}-v1",
                "keywords": _article_keywords(article["title"], version["body"], article["product_area"]),
                "quality_band": "trusted" if lifecycle_state == "published" else "draft",
            },
        )
        self._insert(
            "content_freshness_signal",
            {
                "tenant": article["tenant"],
                "article_id": article["id"],
                "signal_type": "publish",
                "state": "current" if lifecycle_state == "published" else "awaiting_review",
                "review_due_at": self._future(days=int(self._parameter_value("freshness_review_days", 30))),
            },
        )
        if lifecycle_state == "published":
            self._emit("KnowledgeArticlePublished", article["id"], {"tenant": article["tenant"], "article_id": article["id"], "title": article["title"]})
        return {
            "ok": True,
            "state": self.snapshot(),
            "record": article,
            "version": version,
            "approval": approval,
            "side_effects": (),
        }

    def approve_knowledge_article(self, payload: dict) -> dict:
        article = self._article(payload["article_id"])
        approval = self._insert(
            "knowledge_approval",
            {
                "tenant": article["tenant"],
                "article_id": article["id"],
                "approver_id": payload.get("approver_id", "approver"),
                "decision": payload.get("decision", "approved"),
                "reason": payload.get("reason"),
                "decided_at": _now(),
            },
        )
        if approval["decision"] == "approved":
            article = self._update("knowledge_article", article["id"], lifecycle_state="published")
            self._emit("KnowledgeArticleApproved", article["id"], {"tenant": article["tenant"], "article_id": article["id"]})
        return {"ok": True, "state": self.snapshot(), "record": approval, "article": article, "side_effects": ()}

    def version_article(self, payload: dict) -> dict:
        article = self._article(payload["article_id"])
        next_version = int(article["current_version"]) + 1
        version = self._insert(
            "article_version",
            {
                "tenant": article["tenant"],
                "article_id": article["id"],
                "version_number": next_version,
                "change_summary": payload.get("change_summary", "Revision"),
                "body": payload.get("body", "Updated knowledge content."),
                "reviewer": payload.get("reviewer"),
                "published_at": _now() if payload.get("publish_now", True) else None,
            },
        )
        self._update("knowledge_article", article["id"], current_version=next_version, freshness_state="current")
        self._emit("KnowledgeArticleVersioned", article["id"], {"tenant": article["tenant"], "article_id": article["id"], "version_number": next_version})
        return {"ok": True, "state": self.snapshot(), "record": version, "side_effects": ()}

    def capture_article_feedback(self, payload: dict) -> dict:
        feedback = self._insert(
            "article_feedback",
            {
                "tenant": payload.get("tenant", "default"),
                "article_id": payload["article_id"],
                "source_case_id": payload.get("source_case_id"),
                "rating": int(payload.get("rating", 4)),
                "theme": payload.get("theme", "helpful"),
                "comment": payload.get("comment"),
            },
        )
        self._emit("ArticleFeedbackCaptured", feedback["article_id"], {"tenant": feedback["tenant"], "article_id": feedback["article_id"], "rating": feedback["rating"]})
        return {"ok": True, "state": self.snapshot(), "record": feedback, "side_effects": ()}

    def score_article_quality(self, payload: dict) -> dict:
        article_id = payload["article_id"]
        feedback = [row for row in self._table_rows("article_feedback").values() if row["article_id"] == article_id]
        average_rating = sum(row["rating"] for row in feedback) / max(len(feedback), 1)
        readability = payload.get("readability", 0.82)
        success_rate = round(min(1.0, average_rating / 5.0), 3)
        deflection_rate = payload.get("deflection_rate", 0.45)
        overall_score = round(readability * 0.35 + success_rate * 0.45 + deflection_rate * 0.20, 3)
        score = self._insert(
            "article_quality_score",
            {
                "tenant": payload.get("tenant", "default"),
                "article_id": article_id,
                "readability": readability,
                "success_rate": success_rate,
                "deflection_rate": deflection_rate,
                "overall_score": overall_score,
                "calculated_at": _now(),
            },
        )
        article = self._update("knowledge_article", article_id, quality_score=overall_score)
        quality_floor = float(self._parameter_value("article_quality_floor", 0.76))
        signal = None
        if overall_score < quality_floor:
            signal = self._insert(
                "content_freshness_signal",
                {
                    "tenant": article["tenant"],
                    "article_id": article_id,
                    "signal_type": "quality_drop",
                    "state": "review_required",
                    "review_due_at": self._future(days=2),
                },
            )
            self._emit("ContentFreshnessFlagged", article_id, {"tenant": article["tenant"], "article_id": article_id, "overall_score": overall_score})
        return {"ok": True, "state": self.snapshot(), "record": score, "article": article, "signal": signal, "side_effects": ()}

    def identify_root_cause(self, payload: dict) -> dict:
        case_record = self._support_case(payload["case_id"])
        root_cause = self._insert(
            "root_cause",
            {
                "tenant": case_record["tenant"],
                "case_id": case_record["id"],
                "category": payload.get("category", "configuration"),
                "hypothesis": payload.get("hypothesis", "Likely caused by misconfigured dependency."),
                "confidence": payload.get("confidence", 0.76),
                "corrective_action": payload.get("corrective_action", "Apply corrective config and monitor."),
            },
        )
        return {"ok": True, "state": self.snapshot(), "record": root_cause, "side_effects": ()}

    def link_duplicate_case(self, payload: dict) -> dict:
        case_record = self._support_case(payload["case_id"])
        duplicate = self._insert(
            "case_duplicate_link",
            {
                "tenant": case_record["tenant"],
                "case_id": case_record["id"],
                "duplicate_case_id": payload["duplicate_case_id"],
                "confidence": payload.get("confidence", 0.9),
                "disposition": payload.get("disposition", "linked"),
            },
        )
        self._update("support_case", case_record["id"], duplicate_of=payload["duplicate_case_id"])
        return {"ok": True, "state": self.snapshot(), "record": duplicate, "side_effects": ()}

    def resolve_case_exception(self, payload: dict) -> dict:
        case_record = self._support_case(payload["case_id"])
        exception = self._insert(
            "case_exception_case",
            {
                "tenant": case_record["tenant"],
                "case_id": case_record["id"],
                "exception_type": payload.get("exception_type", "policy_override"),
                "reason": payload.get("reason", "Exception documented."),
                "disposition": payload.get("disposition", "resolved"),
            },
        )
        return {"ok": True, "state": self.snapshot(), "record": exception, "side_effects": ()}

    def record_case_deflection(self, payload: dict) -> dict:
        record = self._insert(
            "case_deflection_event",
            {
                "tenant": payload.get("tenant", "default"),
                "article_id": payload.get("article_id"),
                "search_query": payload.get("search_query", "unknown"),
                "outcome": payload.get("outcome", "self_service_success"),
                "elapsed_minutes": int(payload.get("elapsed_minutes", 5)),
            },
        )
        self._emit("CaseDeflected", record["id"], {"tenant": record["tenant"], "article_id": record.get("article_id"), "search_query": record["search_query"]})
        return {"ok": True, "state": self.snapshot(), "record": record, "side_effects": ()}

    def recommend_next_best_resolution(self, payload: dict) -> dict:
        case_record = self._support_case(payload["case_id"])
        relevant_articles = [
            row
            for row in self._table_rows("knowledge_article").values()
            if row["product_area"] in {case_record["product_area"], "general"}
        ]
        relevant_articles.sort(key=lambda row: row["quality_score"], reverse=True)
        citations = []
        recommended_actions = []
        for article in relevant_articles[:2]:
            citations.append({"table": f"{PBC_KEY}_knowledge_article", "id": article["id"], "title": article["title"]})
            recommended_actions.append(
                {
                    "action": "share_or_apply_article",
                    "article_id": article["id"],
                    "reason": f"Best matching article for {case_record['product_area']} with score {article['quality_score']}.",
                }
            )
        if case_record["severity"] in {"critical", "high"}:
            recommended_actions.insert(
                0,
                {
                    "action": "keep_engineering_bridge_open",
                    "reason": "High-severity case should retain active escalation oversight.",
                },
            )
        recommendation = self._insert(
            "agent_assist_recommendation",
            {
                "tenant": case_record["tenant"],
                "case_id": case_record["id"],
                "recommendation_type": "next_best_resolution",
                "confidence": 0.81 if citations else 0.55,
                "citations": citations,
                "recommended_actions": recommended_actions or [{"action": "collect_more_signal", "reason": "No relevant article found."}],
                "accepted": False,
            },
        )
        self._emit("AgentAssistRecommended", case_record["id"], {"tenant": case_record["tenant"], "case_id": case_record["id"], "recommendation_id": recommendation["id"]})
        return {"ok": True, "state": self.snapshot(), "record": recommendation, "side_effects": ()}

    def governed_datastore_crud(self, action: str, table: str, payload: dict, *, confirmed: bool = False) -> dict:
        owned_table = resolve_owned_table(table)
        if owned_table not in OWNED_TABLES:
            return {"ok": False, "reason": "foreign_table_rejected", "state": self.snapshot(), "side_effects": ()}
        if action in {"create", "update", "delete"} and not confirmed:
            return {"ok": False, "reason": "confirmation_required", "state": self.snapshot(), "side_effects": ()}
        if action == "create":
            record = self._insert(owned_table, payload)
        elif action == "update":
            record = self._update(owned_table, payload["id"], **{k: v for k, v in payload.items() if k != "id"})
        elif action == "delete":
            record = self._table_rows(owned_table).pop(payload["id"])
        elif action == "read":
            record = self._table_rows(owned_table).get(payload["id"])
        else:
            return {"ok": False, "reason": "unsupported_action", "state": self.snapshot(), "side_effects": ()}
        return {"ok": True, "state": self.snapshot(), "record": record, "side_effects": ()}

    def run_advanced_assessment(self, payload: dict | None = None) -> dict:
        open_cases = [row for row in self._table_rows("support_case").values() if row["status"] != "resolved"]
        stale_articles = [
            row for row in self._table_rows("content_freshness_signal").values() if row["state"] != "current"
        ]
        score = round(max(0.0, 0.96 - len(open_cases) * 0.03 - len(stale_articles) * 0.05), 3)
        explanations = []
        if any(row["severity"] in {"critical", "high"} for row in open_cases):
            explanations.append("high_severity_case_present")
        if stale_articles:
            explanations.append("freshness_watch_items_present")
        if not explanations:
            explanations.append("operational_load_stable")
        return {"ok": True, "score": score, "explanations": tuple(explanations), "payload": dict(payload or {}), "side_effects": ()}

    def query_workbench(self, filters: dict | None = None) -> dict:
        filters = dict(filters or {})
        cases = tuple(self._table_rows("support_case").values())
        articles = tuple(self._table_rows("knowledge_article").values())
        queues = tuple(self._table_rows("case_queue").values())
        return {
            "ok": True,
            "read_only": True,
            "filters": filters,
            "records": {
                "cases": cases[: int(self._parameter_value("workbench_case_limit", 25))],
                "articles": articles,
                "queues": queues,
            },
            "metrics": {
                "open_cases": sum(1 for row in cases if row["status"] != "resolved"),
                "high_risk_cases": sum(1 for row in self._table_rows("case_sla").values() if row["risk_level"] == "high"),
                "stale_articles": sum(1 for row in self._table_rows("content_freshness_signal").values() if row["state"] != "current"),
                "pending_approvals": sum(1 for row in self._table_rows("knowledge_approval").values() if row["decision"] == "pending"),
            },
            "side_effects": (),
        }

    def list_table_rows(self, table: str) -> dict:
        owned_table = resolve_owned_table(table)
        return {
            "ok": owned_table in OWNED_TABLES,
            "table": owned_table,
            "rows": tuple(self._table_rows(owned_table).values()) if owned_table in OWNED_TABLES else (),
            "side_effects": (),
        }

    def receive_event(self, event: dict) -> dict:
        envelope = build_event_envelope(
            event.get("event_type", ""),
            event.get("payload", {}),
            external_id=event.get("event_id"),
        )
        idempotency_key = event.get("idempotency_key") or envelope["idempotency_key"]
        if idempotency_key in self.state["idempotency_keys"]:
            return {"ok": True, "duplicate": True, "state": self.snapshot(), "side_effects": ()}
        self.state["idempotency_keys"].add(idempotency_key)
        if event.get("event_type") not in DOMAIN_CONSUMED_EVENTS:
            dead_letter = self._insert(
                "appgen_dead_letter_event",
                {
                    "tenant": event.get("payload", {}).get("tenant", "default"),
                    "event_type": event.get("event_type", "unknown"),
                    "external_id": event.get("event_id", "missing"),
                    "status": "dead_letter",
                    "idempotency_key": idempotency_key,
                    "payload": event.get("payload", {}),
                    "reason": "unsupported_event_type",
                },
            )
            self.state["dead_letter"].append(dead_letter)
            return {"ok": False, "duplicate": False, "state": self.snapshot(), "dead_letter": dead_letter, "side_effects": ()}
        inbox_row = self._insert(
            "appgen_inbox_event",
            {
                "tenant": event.get("payload", {}).get("tenant", "default"),
                "event_type": event["event_type"],
                "external_id": event.get("event_id", self._next_id("event")),
                "status": "processed",
                "idempotency_key": idempotency_key,
                "payload": event.get("payload", {}),
            },
        )
        self.state["inbox"].append(inbox_row)
        payload = event.get("payload", {})
        if event["event_type"] == "ServiceTicketOpened":
            self.create_support_case(
                {
                    "tenant": payload.get("tenant", "default"),
                    "title": payload.get("title", "Imported service ticket"),
                    "summary": payload.get("summary", "Imported from external ticketing system."),
                    "severity": payload.get("severity", "medium"),
                    "product_area": payload.get("product_area", "general"),
                    "customer_ref": payload.get("customer_ref", "external-customer"),
                    "channel": "service_ticket",
                }
            )
        elif event["event_type"] == "CustomerUpdated" and payload.get("case_id") in self._table_rows("support_case"):
            self.record_case_interaction(
                {
                    "case_id": payload["case_id"],
                    "channel": "system",
                    "visibility": "internal",
                    "author_role": "system",
                    "sentiment": "neutral",
                    "summary": payload.get("summary", "Customer profile updated."),
                }
            )
        elif event["event_type"] == "SearchIndexRefreshed" and payload.get("article_id"):
            self._insert(
                "content_freshness_signal",
                {
                    "tenant": payload.get("tenant", "default"),
                    "article_id": payload["article_id"],
                    "signal_type": "search_index_refresh",
                    "state": "current",
                    "review_due_at": self._future(days=30),
                },
            )
        elif event["event_type"] == "ProductPublished":
            for article in self._table_rows("knowledge_article").values():
                if article["product_area"] == payload.get("product_area"):
                    self._update("knowledge_article", article["id"], freshness_state="review_required")
        elif event["event_type"] == "PolicyChanged":
            self.register_rule(
                {
                    "rule_id": payload.get("rule_id", "policy-change"),
                    "scope": payload.get("scope", "knowledge"),
                    "condition": payload.get("condition", "approval_required_for_sensitive_publish"),
                    "outcome": payload.get("outcome", "publish_gate"),
                }
            )
        elif event["event_type"] == "WorkflowTaskCompleted" and payload.get("case_id") in self._table_rows("support_case"):
            self.resolve_case_exception(
                {
                    "case_id": payload["case_id"],
                    "exception_type": "workflow_completion",
                    "reason": payload.get("summary", "External workflow task completed."),
                    "disposition": "closed",
                }
            )
        return {"ok": True, "duplicate": False, "state": self.snapshot(), "record": inbox_row, "side_effects": ()}

    def execute_command(self, operation: str, payload: dict | None = None) -> dict:
        payload = dict(payload or {})
        commands = {
            "configure_runtime": lambda: self.configure_runtime(payload),
            "set_parameter": lambda: self.set_parameter(payload["key"], payload["value"]),
            "register_rule": lambda: self.register_rule(payload),
            "register_schema_extension": lambda: self.register_schema_extension(payload["table"], payload["fields"]),
            "receive_event": lambda: self.receive_event(payload),
            "governed_datastore_crud": lambda: self.governed_datastore_crud(
                payload["action"],
                payload["table"],
                payload.get("payload", {}),
                confirmed=bool(payload.get("confirmed", False)),
            ),
            "run_advanced_assessment": lambda: self.run_advanced_assessment(payload),
            "create_support_case": lambda: self.create_support_case(payload),
            "classify_case": lambda: self.classify_case(payload),
            "route_case_queue": lambda: self.route_case_queue(payload),
            "assign_case": lambda: self.assign_case(payload),
            "start_sla_timer": lambda: self.start_sla_timer(payload),
            "record_case_interaction": lambda: self.record_case_interaction(payload),
            "open_case_escalation": lambda: self.open_case_escalation(payload),
            "resolve_case": lambda: self.resolve_case(payload),
            "publish_knowledge_article": lambda: self.publish_knowledge_article(payload),
            "approve_knowledge_article": lambda: self.approve_knowledge_article(payload),
            "version_article": lambda: self.version_article(payload),
            "capture_article_feedback": lambda: self.capture_article_feedback(payload),
            "score_article_quality": lambda: self.score_article_quality(payload),
            "identify_root_cause": lambda: self.identify_root_cause(payload),
            "link_duplicate_case": lambda: self.link_duplicate_case(payload),
            "resolve_case_exception": lambda: self.resolve_case_exception(payload),
            "record_case_deflection": lambda: self.record_case_deflection(payload),
            "recommend_next_best_resolution": lambda: self.recommend_next_best_resolution(payload),
        }
        if operation not in commands:
            return {"ok": False, "reason": "unknown_operation", "operation": operation, "state": self.snapshot(), "side_effects": ()}
        result = commands[operation]()
        if "state" not in result:
            result["state"] = self.snapshot()
        return result

    def execute_query(self, operation: str, payload: dict | None = None) -> dict:
        payload = dict(payload or {})
        if operation == "query_workbench":
            return self.query_workbench(payload)
        if operation == "build_workbench_view":
            return self.query_workbench(payload)
        if operation == "list_table_rows":
            return self.list_table_rows(payload["table"])
        return {"ok": False, "reason": "unknown_query", "operation": operation, "side_effects": ()}

    def runtime_smoke(self) -> dict:
        case_result = self.create_support_case(
            {
                "tenant": "tenant-smoke",
                "title": "Public API requests are timing out",
                "summary": "Customers see repeated 504 responses from the public API.",
                "severity": "high",
                "product_area": "platform",
                "customer_ref": "cust-001",
                "contact": {"name": "Amina", "email": "amina@example.com"},
            }
        )
        case_id = case_result["record"]["id"]
        steps = (
            self.classify_case({"case_id": case_id}),
            self.route_case_queue({"case_id": case_id}),
            self.assign_case({"case_id": case_id}),
            self.start_sla_timer({"case_id": case_id}),
            self.record_case_interaction({"case_id": case_id, "summary": "Collected API trace IDs.", "channel": "chat"}),
            self.identify_root_cause({"case_id": case_id}),
            self.resolve_case({"case_id": case_id, "summary": "Mitigated by rotating the failing edge token."}),
        )
        article = self.publish_knowledge_article(
            {
                "tenant": "tenant-smoke",
                "title": "Handling edge token failures on the public API",
                "product_area": "platform",
                "body": "Rotate the failing edge token, confirm regional health, and re-run the auth health check.",
                "approved_by": "support-approver",
            }
        )
        feedback = self.capture_article_feedback({"tenant": "tenant-smoke", "article_id": article["record"]["id"], "rating": 5, "theme": "resolved_fast"})
        quality = self.score_article_quality({"tenant": "tenant-smoke", "article_id": article["record"]["id"], "readability": 0.86, "deflection_rate": 0.52})
        recommendation = self.recommend_next_best_resolution({"case_id": case_id})
        handled = self.receive_event({"event_type": "SearchIndexRefreshed", "event_id": "evt-1", "payload": {"tenant": "tenant-smoke", "article_id": article["record"]["id"]}})
        duplicate = self.receive_event({"event_type": "SearchIndexRefreshed", "event_id": "evt-1", "payload": {"tenant": "tenant-smoke", "article_id": article["record"]["id"]}})
        dead = self.receive_event({"event_type": "UnexpectedEvent", "event_id": "evt-bad", "payload": {"tenant": "tenant-smoke"}})
        return {
            "ok": case_result["ok"]
            and all(step["ok"] for step in steps)
            and article["ok"]
            and feedback["ok"]
            and quality["ok"]
            and recommendation["ok"]
            and handled["ok"]
            and duplicate["duplicate"] is True
            and dead["ok"] is False,
            "case_id": case_id,
            "article_id": article["record"]["id"],
            "events_emitted": tuple(row["event_type"] for row in self.state["outbox"]),
            "tables_with_rows": tuple(
                table for table, rows in self.state["tables"].items() if rows
            ),
            "side_effects": (),
        }


def create_app(state: dict | None = None) -> CaseKnowledgeManagementApp:
    return CaseKnowledgeManagementApp(state)
