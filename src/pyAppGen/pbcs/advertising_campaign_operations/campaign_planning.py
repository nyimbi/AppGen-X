"""Planning and launch-readiness helpers for advertising campaign operations."""
from __future__ import annotations

from collections.abc import Iterable, Mapping
import hashlib

PBC_KEY = "advertising_campaign_operations"

REQUIRED_BRIEF_FIELDS = (
    "objective",
    "offer",
    "audience_promise",
    "channels",
    "primary_kpi",
    "guardrails",
    "launch_dependencies",
)

READINESS_CHECKS = (
    ("budget_approved", "Approved budget"),
    ("creative_approved", "Approved creative"),
    ("audience_ready", "Audience ready"),
    ("placements_ready", "Placements trafficked"),
    ("tracking_ready", "Tracking ready"),
    ("suppliers_eligible", "Eligible suppliers"),
    ("policy_compliant", "Policy compliant"),
)


def _digest(value: object) -> str:
    return hashlib.sha256(repr(value).encode("utf-8")).hexdigest()


def _clean_text(value: object) -> str:
    return " ".join(str(value or "").strip().split())


def _clean_token(value: object) -> str:
    return _clean_text(value).lower()


def _iterable(value: object) -> Iterable[object]:
    if value is None:
        return ()
    if isinstance(value, (str, bytes)):
        return (value,)
    if isinstance(value, Iterable):
        return value
    return (value,)


def _normalize_string_list(value: object) -> tuple[str, ...]:
    values = {_clean_token(item) for item in _iterable(value) if _clean_text(item)}
    return tuple(sorted(values))


def _normalize_guardrails(value: object) -> tuple[dict[str, object], ...]:
    guardrails = {}
    for item in _iterable(value):
        if isinstance(item, Mapping):
            metric = _clean_token(item.get("metric"))
            operator = _clean_token(item.get("operator") or "inform")
            window = _clean_token(item.get("window") or "flight")
            severity = _clean_token(item.get("severity") or "warning")
            normalized = {
                "metric": metric,
                "operator": operator,
                "value": item.get("value"),
                "window": window,
                "severity": severity,
            }
        else:
            metric = _clean_token(item)
            normalized = {
                "metric": metric,
                "operator": "inform",
                "value": None,
                "window": "flight",
                "severity": "warning",
            }
        if metric:
            key = (
                metric,
                normalized["operator"],
                repr(normalized["value"]),
                normalized["window"],
                normalized["severity"],
            )
            guardrails[key] = normalized
    return tuple(guardrails[key] for key in sorted(guardrails))


def _normalize_dependency_status(value: object) -> dict[str, dict[str, object]]:
    normalized: dict[str, dict[str, object]] = {}
    if isinstance(value, Mapping):
        items = list(value.items())
    else:
        items = []
        for item in _iterable(value):
            if isinstance(item, Mapping):
                items.append((item.get("name") or item.get("dependency"), item))
    for raw_name, raw_status in items:
        name = _clean_token(raw_name)
        if not name:
            continue
        if isinstance(raw_status, Mapping):
            ready = _as_bool(raw_status.get("ready"))
            detail = _clean_text(raw_status.get("detail"))
        else:
            ready = _as_bool(raw_status)
            detail = ""
        normalized[name] = {"ready": ready, "detail": detail}
    return normalized


def _as_bool(value: object) -> bool:
    if isinstance(value, bool):
        return value
    if isinstance(value, (int, float)):
        return bool(value)
    return _clean_token(value) in {
        "1",
        "true",
        "yes",
        "y",
        "ready",
        "approved",
        "complete",
        "completed",
        "passed",
    }


def normalize_campaign_brief(brief: Mapping[str, object] | None) -> dict[str, object]:
    source = dict(brief or {})
    normalized = {
        "objective": _clean_text(source.get("objective")),
        "offer": _clean_text(source.get("offer")),
        "audience_promise": _clean_text(source.get("audience_promise")),
        "channels": _normalize_string_list(source.get("channels")),
        "primary_kpi": _clean_text(source.get("primary_kpi")),
        "guardrails": _normalize_guardrails(source.get("guardrails")),
        "launch_dependencies": _normalize_string_list(source.get("launch_dependencies")),
    }
    missing_fields = tuple(
        field
        for field in REQUIRED_BRIEF_FIELDS
        if not normalized[field]
    )
    return {
        "ok": not missing_fields,
        "brief": normalized,
        "missing_fields": missing_fields,
        "side_effects": (),
    }


def review_launch_readiness(payload: Mapping[str, object] | None) -> dict[str, object]:
    source = dict(payload or {})
    plan = dict(source.get("campaign_plan") or {})
    if not plan and source.get("brief"):
        plan_result = build_campaign_plan(source)
        plan = dict(plan_result.get("campaign_plan") or {})
    brief_result = normalize_campaign_brief(plan.get("brief"))
    readiness = dict(source.get("readiness") or source.get("launch_readiness") or {})
    dependency_status = _normalize_dependency_status(
        readiness.get("dependency_status") or readiness.get("launch_dependencies")
    )

    checklist = []
    blockers = []
    for key, label in READINESS_CHECKS:
        ready = _as_bool(readiness.get(key))
        detail = _clean_text(readiness.get(f"{key}_detail"))
        checklist.append(
            {
                "check": key,
                "label": label,
                "ready": ready,
                "detail": detail,
            }
        )
        if not ready:
            blockers.append(
                {
                    "check": key,
                    "label": label,
                    "reason": detail or f"{label} is required before launch.",
                }
            )

    for dependency in brief_result["brief"]["launch_dependencies"]:
        dependency_state = dependency_status.get(dependency, {"ready": False, "detail": ""})
        checklist.append(
            {
                "check": f"dependency:{dependency}",
                "label": dependency,
                "ready": dependency_state["ready"],
                "detail": dependency_state["detail"],
            }
        )
        if not dependency_state["ready"]:
            blockers.append(
                {
                    "check": f"dependency:{dependency}",
                    "label": dependency,
                    "reason": dependency_state["detail"]
                    or f"Launch dependency '{dependency}' is still open.",
                }
            )

    if brief_result["missing_fields"]:
        blockers.append(
            {
                "check": "campaign_brief",
                "label": "Campaign brief",
                "reason": "Missing brief fields: "
                + ", ".join(brief_result["missing_fields"]),
            }
        )

    report = {
        "campaign_id": plan.get("campaign_id") or source.get("campaign_id") or source.get("id"),
        "ready": not blockers,
        "checklist": tuple(checklist),
        "blockers": tuple(blockers),
        "summary": {
            "ready_count": sum(1 for item in checklist if item["ready"]),
            "blocked_count": len(blockers),
            "dependency_count": len(brief_result["brief"]["launch_dependencies"]),
        },
    }
    return {"ok": True, "launch_report": report, "side_effects": ()}


def build_campaign_plan(payload: Mapping[str, object] | None) -> dict[str, object]:
    source = dict(payload or {})
    brief_result = normalize_campaign_brief(source.get("brief"))
    if not brief_result["ok"]:
        return {
            "ok": False,
            "reason": "incomplete_campaign_brief",
            "missing_fields": brief_result["missing_fields"],
            "brief": brief_result["brief"],
            "side_effects": (),
        }

    tenant = _clean_text(source.get("tenant") or "default")
    brief = brief_result["brief"]
    fingerprint = _digest(brief)
    code = _clean_text(source.get("code")) or f"CAMPAIGN-{fingerprint[:8].upper()}"
    campaign_id = _clean_text(source.get("id") or code)

    plan = {
        "campaign_id": campaign_id,
        "tenant": tenant,
        "code": code,
        "status": _clean_text(source.get("status") or "draft"),
        "brief": brief,
        "brief_fingerprint": fingerprint,
        "primary_channel": brief["channels"][0],
        "planning_summary": {
            "channel_count": len(brief["channels"]),
            "guardrail_count": len(brief["guardrails"]),
            "launch_dependency_count": len(brief["launch_dependencies"]),
            "primary_kpi": brief["primary_kpi"],
        },
    }
    plan["launch_gate"] = review_launch_readiness(
        {
            "campaign_plan": plan,
            "readiness": source.get("readiness") or source.get("launch_readiness") or {},
        }
    )["launch_report"]
    return {"ok": True, "campaign_plan": plan, "side_effects": ()}


def build_command_center_summary(plans: Iterable[Mapping[str, object]] | None) -> dict[str, object]:
    queue = []
    ready_count = 0
    blocked_count = 0
    for item in _iterable(plans):
        plan = dict(item or {})
        review = plan.get("launch_gate") or review_launch_readiness({"campaign_plan": plan})["launch_report"]
        ready = bool(review["ready"])
        ready_count += int(ready)
        blocked_count += int(not ready)
        queue.append(
            {
                "campaign_id": plan.get("campaign_id"),
                "code": plan.get("code"),
                "status": plan.get("status"),
                "ready": ready,
                "blocked_count": review["summary"]["blocked_count"],
                "primary_kpi": plan.get("planning_summary", {}).get("primary_kpi"),
            }
        )
    queue.sort(key=lambda item: (item["ready"], item["blocked_count"], item["code"] or ""))
    return {
        "ok": True,
        "summary": {
            "campaign_count": len(queue),
            "ready_count": ready_count,
            "blocked_count": blocked_count,
        },
        "launch_queue": tuple(queue),
        "side_effects": (),
    }
