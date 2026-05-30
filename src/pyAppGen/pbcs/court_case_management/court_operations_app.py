"""Executable one-PBC court case management application surface."""
from __future__ import annotations

from copy import deepcopy
from hashlib import sha256

PBC_KEY = "court_case_management"
BUSINESS_TABLES = (
    "court_case_management_court_case",
    "court_case_management_filing",
    "court_case_management_evidence_item",
    "court_case_management_hearing",
    "court_case_management_case_task",
    "court_case_management_docket_entry",
    "court_case_management_party",
    "court_case_management_judgment",
    "court_case_management_court_order",
)
OWNED_TABLES = BUSINESS_TABLES + ("court_case_management_appgen_outbox_event",)
ROUTES = (
    "POST /court-cases",
    "POST /filings",
    "POST /evidence",
    "POST /hearings",
    "POST /tasks",
    "POST /tasks/complete",
    "POST /court-orders",
    "POST /court-orders/enter",
    "POST /docket-entrys",
    "POST /partys",
    "GET /court-case-management-workbench",
)
FILING_STATES = ("received", "under_clerk_review", "deficient", "cured", "accepted", "rejected", "stricken")
ORDER_STATES = ("draft", "under_review", "signed", "entered", "corrected", "vacated")
HEARING_STATUSES = ("tentative", "confirmed", "continued", "completed", "cancelled")
TASK_STATUSES = ("open", "in_progress", "completed", "cancelled")
ADMISSION_STATUSES = ("pending", "admitted", "excluded", "withdrawn")
ACCESS_CLASSES = ("public", "restricted", "sealed", "redacted")
TIMELINE_ORDER = {
    "court_case": 0,
    "filing": 1,
    "evidence_item": 2,
    "hearing": 3,
    "court_order": 4,
    "case_task": 5,
    "docket_entry": 6,
}
TASK_QUEUE_BY_TYPE = {
    "filing_review": "clerk_intake",
    "evidence_review": "evidence",
    "hearing_prep": "hearing_prep",
    "order_review": "chambers",
    "service": "docketing",
    "follow_up": "operations",
}


def _digest(value: object) -> str:
    return sha256(repr(value).encode("utf-8")).hexdigest()


def _copy_state(state: dict) -> dict:
    copied = deepcopy(state)
    copied["idempotency_keys"] = set(state.get("idempotency_keys", set()))
    return copied


def _emit(state: dict, event_type: str, payload: dict) -> dict:
    envelope = {
        "event_type": event_type,
        "event_contract": "AppGen-X",
        "topic": "pbc.court_case_management.events",
        "payload": dict(payload),
        "idempotency_key": _digest((event_type, payload)),
    }
    state["outbox"].append(envelope)
    return envelope


def _case_number(court: str, division: str, year: int, sequence: int) -> str:
    return f"{court}-{division}-{year}-{sequence:06d}"


def _derive_task_queue(task_type: str | None) -> str:
    return TASK_QUEUE_BY_TYPE.get(str(task_type or "follow_up"), "operations")


def _find_case_items(items: dict, case_id: str) -> tuple[dict, ...]:
    return tuple(item for item in items.values() if item.get("case_id") == case_id)


def _close_related_tasks(state: dict, *, related_record_type: str, related_record_id: str, completed_by: str = "system") -> None:
    for task_id, task in list(state.get("tasks", {}).items()):
        if (
            task.get("related_record_type") == related_record_type
            and task.get("related_record_id") == related_record_id
            and task["status"] != "completed"
        ):
            state["tasks"][task_id] = {
                **task,
                "status": "completed",
                "completed_by": completed_by,
                "completed_at": task.get("completed_at") or "auto",
                "completion_notes": task.get("completion_notes") or f"Auto-completed after {related_record_type} update.",
            }


def _timeline_entry(kind: str, entity: dict, *, label: str, sort_value: object, restricted: bool = False) -> dict:
    return {
        "timeline_id": f"{kind}:{entity['id']}",
        "entity_type": kind,
        "entity_id": entity["id"],
        "label": label,
        "sort_order": TIMELINE_ORDER.get(kind, 99),
        "sort_value": str(sort_value or entity.get("id")),
        "restricted": restricted,
        "record": deepcopy(entity),
    }


def _visible(entity: dict, permissions: tuple[str, ...] | None) -> bool:
    permissions = permissions or ()
    access_class = entity.get("access_class", "public")
    if access_class == "public":
        return True
    return "court_case_management.admin" in permissions or "court_case_management.approve" in permissions


def empty_court_state() -> dict:
    return {
        "cases": {},
        "case_number_index": {},
        "parties": {},
        "filings": {},
        "evidence_items": {},
        "hearings": {},
        "tasks": {},
        "docket_entries": {},
        "orders": {},
        "judgments": {},
        "outbox": [],
        "idempotency_keys": set(),
    }


def create_court_case(state: dict, payload: dict) -> dict:
    next_state = _copy_state(state)
    required = ("court", "division", "filing_year", "case_type", "caption")
    missing = tuple(field for field in required if not payload.get(field))
    if missing:
        return {"ok": False, "state": next_state, "reason": "missing_required_fields", "missing": missing, "side_effects": ()}
    key = (payload["court"], payload["division"], int(payload["filing_year"]))
    sequence = int(payload.get("sequence") or next_state["case_number_index"].get(key, 0) + 1)
    number = payload.get("case_number") or _case_number(payload["court"], payload["division"], int(payload["filing_year"]), sequence)
    if any(case["case_number"] == number for case in next_state["cases"].values()):
        return {"ok": False, "state": next_state, "reason": "duplicate_case_number", "case_number": number, "side_effects": ()}
    case_id = payload.get("case_id") or f"case-{_digest((number, payload.get('caption')))[:10]}"
    court_case = {
        "id": case_id,
        "table": "court_case_management_court_case",
        "tenant": payload.get("tenant", "default"),
        "case_number": number,
        "court": payload["court"],
        "division": payload["division"],
        "original_venue": payload.get("original_venue", payload["court"]),
        "current_venue": payload.get("current_venue", payload["court"]),
        "transfer_lineage": tuple(payload.get("transfer_lineage", ())),
        "case_type": payload["case_type"],
        "caption": payload["caption"],
        "assigned_judge": payload.get("assigned_judge"),
        "opened_at": payload.get("opened_at", f"{payload['filing_year']}-01-01"),
        "access_class": payload.get("access_class", "public"),
        "status": "open",
        "docket_sequence": 0,
    }
    next_state["case_number_index"][key] = max(next_state["case_number_index"].get(key, 0), sequence)
    next_state["cases"][case_id] = court_case
    _emit(next_state, "CourtCaseManagementCreated", {"entity": "court_case", "id": case_id, "case_number": number})
    return {"ok": True, "state": next_state, "court_case": court_case, "side_effects": ()}


def add_party(state: dict, payload: dict) -> dict:
    next_state = _copy_state(state)
    if payload.get("case_id") not in next_state["cases"]:
        return {"ok": False, "state": next_state, "reason": "case_not_found", "side_effects": ()}
    required = ("case_id", "party_name", "role")
    missing = tuple(field for field in required if not payload.get(field))
    if missing:
        return {"ok": False, "state": next_state, "reason": "missing_required_fields", "missing": missing, "side_effects": ()}
    party_id = payload.get("party_id") or f"party-{_digest((payload['case_id'], payload['party_name'], payload['role']))[:10]}"
    party = {
        "id": party_id,
        "table": "court_case_management_party",
        "case_id": payload["case_id"],
        "party_name": payload["party_name"],
        "role": payload["role"],
        "lead_counsel": payload.get("lead_counsel"),
        "self_represented": bool(payload.get("self_represented", not payload.get("lead_counsel"))),
        "appearance_date": payload.get("appearance_date"),
        "withdrawal_date": payload.get("withdrawal_date"),
        "service_addresses": tuple(payload.get("service_addresses", ())),
        "aliases": tuple(payload.get("aliases", ())),
        "representation_history": tuple(payload.get("representation_history", ())),
        "access_class": payload.get("access_class", "public"),
    }
    next_state["parties"][party_id] = party
    _emit(next_state, "CourtCaseManagementUpdated", {"entity": "party", "id": party_id})
    return {"ok": True, "state": next_state, "party": party, "side_effects": ()}


def add_docket_entry(state: dict, payload: dict) -> dict:
    next_state = _copy_state(state)
    case = deepcopy(next_state["cases"].get(payload.get("case_id")))
    if not case:
        return {"ok": False, "state": next_state, "reason": "case_not_found", "side_effects": ()}
    requested_sequence = payload.get("sequence")
    expected_sequence = case["docket_sequence"] + 1
    if requested_sequence is not None and int(requested_sequence) != expected_sequence:
        return {
            "ok": False,
            "state": next_state,
            "reason": "docket_sequence_gap",
            "expected_sequence": expected_sequence,
            "side_effects": (),
        }
    entry_id = payload.get("docket_entry_id") or f"docket-{case['id']}-{expected_sequence}"
    entry = {
        "id": entry_id,
        "table": "court_case_management_docket_entry",
        "case_id": case["id"],
        "sequence": expected_sequence,
        "source_type": payload.get("source_type"),
        "source_id": payload.get("source_id"),
        "entry_text": payload.get("entry_text"),
        "recorded_at": payload.get("recorded_at") or payload.get("scheduled_at") or payload.get("submitted_at"),
        "access_class": payload.get("access_class", "public"),
        "correction_of": payload.get("correction_of"),
    }
    case["docket_sequence"] = expected_sequence
    next_state["cases"][case["id"]] = case
    next_state["docket_entries"][entry_id] = entry
    _emit(next_state, "CourtCaseManagementUpdated", {"entity": "docket_entry", "id": entry_id, "sequence": expected_sequence})
    return {"ok": True, "state": next_state, "docket_entry": entry, "side_effects": ()}


def create_task(state: dict, payload: dict) -> dict:
    next_state = _copy_state(state)
    if payload.get("case_id") not in next_state["cases"]:
        return {"ok": False, "state": next_state, "reason": "case_not_found", "side_effects": ()}
    required = ("case_id", "title")
    missing = tuple(field for field in required if not payload.get(field))
    if missing:
        return {"ok": False, "state": next_state, "reason": "missing_required_fields", "missing": missing, "side_effects": ()}
    task_id = payload.get("task_id") or f"task-{_digest((payload['case_id'], payload['title'], payload.get('task_type')))[:10]}"
    task = {
        "id": task_id,
        "table": "court_case_management_case_task",
        "case_id": payload["case_id"],
        "title": payload["title"],
        "task_type": payload.get("task_type", "follow_up"),
        "queue": payload.get("queue") or _derive_task_queue(payload.get("task_type")),
        "priority": payload.get("priority", "normal"),
        "status": payload.get("status", "open"),
        "assignee": payload.get("assignee"),
        "due_date": payload.get("due_date"),
        "related_record_type": payload.get("related_record_type"),
        "related_record_id": payload.get("related_record_id"),
        "completion_notes": None,
        "completed_by": None,
        "completed_at": None,
        "access_class": payload.get("access_class", "public"),
    }
    next_state["tasks"][task_id] = task
    _emit(next_state, "CourtCaseManagementCreated", {"entity": "case_task", "id": task_id, "queue": task["queue"]})
    return {"ok": True, "state": next_state, "task": task, "side_effects": ()}


def complete_task(state: dict, task_id: str, payload: dict) -> dict:
    next_state = _copy_state(state)
    task = deepcopy(next_state["tasks"].get(task_id))
    if not task:
        return {"ok": False, "state": next_state, "reason": "task_not_found", "side_effects": ()}
    if task["status"] == "completed":
        return {"ok": False, "state": next_state, "reason": "task_already_completed", "side_effects": ()}
    if payload.get("requires_approval") and not payload.get("completed_by"):
        return {"ok": False, "state": next_state, "reason": "completed_by_required", "side_effects": ()}
    task["status"] = "completed"
    task["completed_by"] = payload.get("completed_by", "system")
    task["completed_at"] = payload.get("completed_at", "completed")
    task["completion_notes"] = payload.get("completion_notes")
    next_state["tasks"][task_id] = task
    _emit(next_state, "CourtCaseManagementUpdated", {"entity": "case_task", "id": task_id, "status": "completed"})
    return {"ok": True, "state": next_state, "task": task, "side_effects": ()}


def receive_filing(state: dict, payload: dict) -> dict:
    next_state = _copy_state(state)
    case = next_state["cases"].get(payload.get("case_id"))
    if not case:
        return {"ok": False, "state": next_state, "reason": "case_not_found", "side_effects": ()}
    deficiency_codes = tuple(payload.get("deficiency_codes", ()))
    filing_id = payload.get("filing_id") or f"filing-{_digest((payload.get('case_id'), payload.get('document_title'), payload.get('received_at')))[:10]}"
    filing_state = "deficient" if deficiency_codes else "accepted"
    filing = {
        "id": filing_id,
        "table": "court_case_management_filing",
        "case_id": payload["case_id"],
        "filing_type": payload.get("filing_type", "pleading"),
        "document_title": payload.get("document_title"),
        "received_at": payload.get("received_at"),
        "state": filing_state,
        "deficiency_codes": deficiency_codes,
        "cure_deadline": payload.get("cure_deadline") if deficiency_codes else None,
        "parent_filing_id": payload.get("parent_filing_id"),
        "supersedes": bool(payload.get("supersedes", False)),
        "access_class": payload.get("access_class", "public"),
    }
    next_state["filings"][filing_id] = filing
    event_type = "CourtCaseManagementExceptionOpened" if deficiency_codes else "CourtCaseManagementCreated"
    _emit(next_state, event_type, {"entity": "filing", "id": filing_id, "state": filing_state})
    deficiency_task = None
    if deficiency_codes:
        task_result = create_task(
            next_state,
            {
                "case_id": payload["case_id"],
                "title": f"Review filing deficiency for {filing['document_title'] or filing['filing_type']}",
                "task_type": "filing_review",
                "due_date": filing["cure_deadline"],
                "related_record_type": "filing",
                "related_record_id": filing_id,
            },
        )
        next_state = task_result["state"]
        deficiency_task = task_result["task"]
    else:
        docket = add_docket_entry(
            next_state,
            {
                "case_id": payload["case_id"],
                "source_type": "filing",
                "source_id": filing_id,
                "entry_text": filing["document_title"] or filing["filing_type"],
                "recorded_at": filing["received_at"],
            },
        )
        next_state = docket["state"]
    return {"ok": True, "state": next_state, "filing": filing, "task": deficiency_task, "side_effects": ()}


def cure_filing(state: dict, filing_id: str, payload: dict) -> dict:
    next_state = _copy_state(state)
    filing = deepcopy(next_state["filings"].get(filing_id))
    if not filing:
        return {"ok": False, "state": next_state, "reason": "filing_not_found", "side_effects": ()}
    if filing["state"] != "deficient":
        return {"ok": False, "state": next_state, "reason": "filing_not_deficient", "side_effects": ()}
    filing["state"] = "accepted" if payload.get("defects_cured") else "rejected"
    filing["deficiency_cure_evidence"] = payload.get("evidence")
    next_state["filings"][filing_id] = filing
    _emit(next_state, "CourtCaseManagementUpdated", {"entity": "filing", "id": filing_id, "state": filing["state"]})
    _close_related_tasks(next_state, related_record_type="filing", related_record_id=filing_id)
    docket_entry = None
    if filing["state"] == "accepted":
        docket = add_docket_entry(
            next_state,
            {
                "case_id": filing["case_id"],
                "source_type": "filing",
                "source_id": filing_id,
                "entry_text": filing["document_title"] or filing["filing_type"],
                "recorded_at": payload.get("accepted_at") or filing.get("received_at"),
            },
        )
        next_state = docket["state"]
        docket_entry = docket["docket_entry"]
    return {"ok": True, "state": next_state, "filing": filing, "docket_entry": docket_entry, "side_effects": ()}


def register_evidence(state: dict, payload: dict) -> dict:
    next_state = _copy_state(state)
    case_id = payload.get("case_id")
    if case_id not in next_state["cases"]:
        return {"ok": False, "state": next_state, "reason": "case_not_found", "side_effects": ()}
    filing_id = payload.get("filing_id")
    hearing_id = payload.get("hearing_id")
    if filing_id and filing_id not in next_state["filings"]:
        return {"ok": False, "state": next_state, "reason": "filing_not_found", "side_effects": ()}
    if hearing_id and hearing_id not in next_state["hearings"]:
        return {"ok": False, "state": next_state, "reason": "hearing_not_found", "side_effects": ()}
    required = ("case_id", "description")
    missing = tuple(field for field in required if not payload.get(field))
    if missing:
        return {"ok": False, "state": next_state, "reason": "missing_required_fields", "missing": missing, "side_effects": ()}
    case_evidence = _find_case_items(next_state["evidence_items"], case_id)
    exhibit_number = payload.get("exhibit_number") or f"EX-{len(case_evidence) + 1:03d}"
    if any(item["exhibit_number"] == exhibit_number for item in case_evidence):
        return {"ok": False, "state": next_state, "reason": "duplicate_exhibit_number", "side_effects": ()}
    evidence_id = payload.get("evidence_id") or f"evidence-{_digest((case_id, exhibit_number, payload['description']))[:10]}"
    evidence_item = {
        "id": evidence_id,
        "table": "court_case_management_evidence_item",
        "case_id": case_id,
        "filing_id": filing_id,
        "hearing_id": hearing_id,
        "description": payload["description"],
        "exhibit_number": exhibit_number,
        "submitted_at": payload.get("submitted_at"),
        "submitted_by": payload.get("submitted_by"),
        "admission_status": payload.get("admission_status", "pending"),
        "storage_location": payload.get("storage_location", "clerk evidence room"),
        "custody_events": tuple(payload.get("custody_events", ())) or (
            {
                "status": "received",
                "holder": payload.get("submitted_by", "court clerk"),
                "location": payload.get("storage_location", "clerk evidence room"),
            },
        ),
        "access_class": payload.get("access_class", "public"),
    }
    next_state["evidence_items"][evidence_id] = evidence_item
    _emit(next_state, "CourtCaseManagementCreated", {"entity": "evidence_item", "id": evidence_id, "exhibit_number": exhibit_number})
    docket = add_docket_entry(
        next_state,
        {
            "case_id": case_id,
            "source_type": "evidence_item",
            "source_id": evidence_id,
            "entry_text": f"Evidence lodged {exhibit_number}: {payload['description']}",
            "recorded_at": payload.get("submitted_at"),
            "access_class": payload.get("access_class", "public"),
        },
    )
    next_state = docket["state"]
    task = None
    if evidence_item["admission_status"] == "pending":
        task_result = create_task(
            next_state,
            {
                "case_id": case_id,
                "title": f"Review evidence {exhibit_number}",
                "task_type": "evidence_review",
                "related_record_type": "evidence_item",
                "related_record_id": evidence_id,
                "due_date": payload.get("review_due_date"),
            },
        )
        next_state = task_result["state"]
        task = task_result["task"]
    return {
        "ok": True,
        "state": next_state,
        "evidence_item": evidence_item,
        "docket_entry": docket["docket_entry"],
        "task": task,
        "side_effects": (),
    }


def schedule_hearing(state: dict, payload: dict) -> dict:
    next_state = _copy_state(state)
    if payload.get("case_id") not in next_state["cases"]:
        return {"ok": False, "state": next_state, "reason": "case_not_found", "side_effects": ()}
    required = ("case_id", "hearing_type", "scheduled_at", "courtroom", "session_block", "assigned_judge")
    missing = tuple(field for field in required if not payload.get(field))
    if missing:
        return {"ok": False, "state": next_state, "reason": "missing_required_fields", "missing": missing, "side_effects": ()}
    active_hearings = tuple(
        hearing
        for hearing in next_state["hearings"].values()
        if hearing["status"] in {"tentative", "confirmed"}
    )
    if any(
        hearing["scheduled_at"] == payload["scheduled_at"] and hearing["courtroom"] == payload["courtroom"]
        for hearing in active_hearings
    ):
        return {"ok": False, "state": next_state, "reason": "courtroom_double_booked", "side_effects": ()}
    if any(
        hearing["scheduled_at"] == payload["scheduled_at"] and hearing["assigned_judge"] == payload["assigned_judge"]
        for hearing in active_hearings
    ):
        return {"ok": False, "state": next_state, "reason": "judge_double_booked", "side_effects": ()}
    hearing_id = payload.get("hearing_id") or f"hearing-{_digest((payload['case_id'], payload['scheduled_at'], payload['courtroom']))[:10]}"
    hearing = {
        "id": hearing_id,
        "table": "court_case_management_hearing",
        "case_id": payload["case_id"],
        "hearing_type": payload["hearing_type"],
        "scheduled_at": payload["scheduled_at"],
        "courtroom": payload["courtroom"],
        "session_block": payload["session_block"],
        "assigned_judge": payload["assigned_judge"],
        "calendar_status": payload.get("calendar_status", "confirmed"),
        "status": payload.get("status", "confirmed"),
        "readiness_prerequisites": tuple(payload.get("readiness_prerequisites", ())),
        "interpreter_required": bool(payload.get("interpreter_required", False)),
        "mode": payload.get("mode", "in_person"),
        "access_class": payload.get("access_class", "public"),
    }
    next_state["hearings"][hearing_id] = hearing
    _emit(next_state, "CourtCaseManagementCreated", {"entity": "hearing", "id": hearing_id})
    task_result = create_task(
        next_state,
        {
            "case_id": payload["case_id"],
            "title": f"Prepare hearing packet for {payload['hearing_type']}",
            "task_type": "hearing_prep",
            "related_record_type": "hearing",
            "related_record_id": hearing_id,
            "due_date": payload.get("prep_due_date") or payload["scheduled_at"],
        },
    )
    next_state = task_result["state"]
    return {"ok": True, "state": next_state, "hearing": hearing, "task": task_result["task"], "side_effects": ()}


def draft_order(state: dict, payload: dict) -> dict:
    next_state = _copy_state(state)
    if payload.get("case_id") not in next_state["cases"]:
        return {"ok": False, "state": next_state, "reason": "case_not_found", "side_effects": ()}
    order_id = payload.get("order_id") or f"order-{_digest((payload.get('case_id'), payload.get('title')))[:10]}"
    order = {
        "id": order_id,
        "table": "court_case_management_court_order",
        "case_id": payload["case_id"],
        "title": payload.get("title"),
        "state": "draft",
        "draft_text": payload.get("draft_text"),
        "signature_metadata": None,
        "effective_date": payload.get("effective_date"),
        "service_linkage": tuple(payload.get("service_linkage", ())),
        "version": 1,
        "access_class": payload.get("access_class", "public"),
    }
    next_state["orders"][order_id] = order
    _emit(next_state, "CourtCaseManagementCreated", {"entity": "court_order", "id": order_id, "state": "draft"})
    task_result = create_task(
        next_state,
        {
            "case_id": payload["case_id"],
            "title": f"Review draft order {payload.get('title') or order_id}",
            "task_type": "order_review",
            "related_record_type": "court_order",
            "related_record_id": order_id,
        },
    )
    next_state = task_result["state"]
    return {"ok": True, "state": next_state, "court_order": order, "task": task_result["task"], "side_effects": ()}


def sign_and_enter_order(state: dict, order_id: str, payload: dict) -> dict:
    next_state = _copy_state(state)
    order = deepcopy(next_state["orders"].get(order_id))
    if not order:
        return {"ok": False, "state": next_state, "reason": "order_not_found", "side_effects": ()}
    if not payload.get("judge_signature") or not payload.get("signed_at"):
        return {"ok": False, "state": next_state, "reason": "signature_required", "side_effects": ()}
    order["state"] = "entered"
    order["signature_metadata"] = {"judge_signature": payload["judge_signature"], "signed_at": payload["signed_at"]}
    order["version"] += 1
    next_state["orders"][order_id] = order
    _close_related_tasks(next_state, related_record_type="court_order", related_record_id=order_id)
    docket = add_docket_entry(
        next_state,
        {
            "case_id": order["case_id"],
            "source_type": "court_order",
            "source_id": order_id,
            "entry_text": order["title"],
            "access_class": payload.get("access_class", order.get("access_class", "public")),
            "recorded_at": payload["signed_at"],
        },
    )
    next_state = docket["state"]
    _emit(next_state, "CourtCaseManagementApproved", {"entity": "court_order", "id": order_id, "state": "entered"})
    return {"ok": True, "state": next_state, "court_order": order, "docket_entry": docket["docket_entry"], "side_effects": ()}


def case_detail(state: dict, case_id: str, permissions: tuple[str, ...] | None = None) -> dict:
    case = deepcopy(state.get("cases", {}).get(case_id))
    if not case:
        return {"ok": False, "reason": "case_not_found", "side_effects": ()}
    permissions = permissions or ()
    parties = tuple(item for item in _find_case_items(state.get("parties", {}), case_id) if _visible(item, permissions))
    filings = tuple(item for item in _find_case_items(state.get("filings", {}), case_id) if _visible(item, permissions))
    evidence_items = tuple(item for item in _find_case_items(state.get("evidence_items", {}), case_id) if _visible(item, permissions))
    hearings = tuple(item for item in _find_case_items(state.get("hearings", {}), case_id) if _visible(item, permissions))
    tasks = tuple(item for item in _find_case_items(state.get("tasks", {}), case_id) if _visible(item, permissions))
    orders = tuple(item for item in _find_case_items(state.get("orders", {}), case_id) if _visible(item, permissions))
    docket_entries = tuple(item for item in _find_case_items(state.get("docket_entries", {}), case_id) if _visible(item, permissions))
    timeline = []
    timeline.append(_timeline_entry("court_case", case, label=case["caption"], sort_value=case.get("opened_at")))
    for filing in filings:
        timeline.append(_timeline_entry("filing", filing, label=filing.get("document_title") or filing["filing_type"], sort_value=filing.get("received_at"), restricted=filing.get("access_class") != "public"))
    for evidence_item in evidence_items:
        timeline.append(_timeline_entry("evidence_item", evidence_item, label=f"{evidence_item['exhibit_number']} {evidence_item['description']}", sort_value=evidence_item.get("submitted_at"), restricted=evidence_item.get("access_class") != "public"))
    for hearing in hearings:
        timeline.append(_timeline_entry("hearing", hearing, label=f"{hearing['hearing_type']} hearing", sort_value=hearing.get("scheduled_at"), restricted=hearing.get("access_class") != "public"))
    for order in orders:
        timeline.append(_timeline_entry("court_order", order, label=order.get("title") or "order", sort_value=order.get("signature_metadata", {}).get("signed_at") if order.get("signature_metadata") else order.get("effective_date"), restricted=order.get("access_class") != "public"))
    for task in tasks:
        timeline.append(_timeline_entry("case_task", task, label=task["title"], sort_value=task.get("due_date") or task["id"], restricted=task.get("access_class") != "public"))
    for entry in docket_entries:
        timeline.append(_timeline_entry("docket_entry", entry, label=entry["entry_text"], sort_value=f"{entry['sequence']:06d}", restricted=entry.get("access_class") != "public"))
    timeline.sort(key=lambda item: (item["sort_value"], item["sort_order"], item["entity_id"]))
    return {
        "ok": True,
        "pbc": PBC_KEY,
        "case": case,
        "parties": parties,
        "filings": filings,
        "evidence_items": evidence_items,
        "hearings": hearings,
        "tasks": tasks,
        "orders": orders,
        "docket_entries": docket_entries,
        "timeline": tuple(timeline),
        "counts": {
            "parties": len(parties),
            "filings": len(filings),
            "evidence_items": len(evidence_items),
            "hearings": len(hearings),
            "tasks": len(tasks),
            "orders": len(orders),
            "docket_entries": len(docket_entries),
        },
        "side_effects": (),
    }


def court_workbench(state: dict, permissions: tuple[str, ...] | None = None) -> dict:
    permissions = permissions or ()
    filings = tuple(item for item in state.get("filings", {}).values() if _visible(item, permissions))
    hearings = tuple(item for item in state.get("hearings", {}).values() if _visible(item, permissions))
    orders = tuple(item for item in state.get("orders", {}).values() if _visible(item, permissions))
    cases = tuple(item for item in state.get("cases", {}).values() if _visible(item, permissions))
    tasks = tuple(item for item in state.get("tasks", {}).values() if _visible(item, permissions))
    evidence_items = tuple(item for item in state.get("evidence_items", {}).values() if _visible(item, permissions))
    queues = {
        "clerk_deficiency_queue": tuple(filing for filing in filings if filing["state"] == "deficient"),
        "accepted_filings": tuple(filing for filing in filings if filing["state"] == "accepted"),
        "evidence_review_queue": tuple(item for item in evidence_items if item["admission_status"] == "pending"),
        "chambers_order_review": tuple(order for order in orders if order["state"] in {"draft", "under_review"}),
        "courtroom_calendar": tuple(hearing for hearing in hearings if hearing["status"] in {"tentative", "confirmed"}),
        "pending_tasks": tuple(task for task in tasks if task["status"] in {"open", "in_progress"}),
        "sealed_or_restricted_items": tuple(item for item in filings + evidence_items + orders if item.get("access_class") in {"sealed", "restricted"}),
        "open_cases": tuple(case for case in cases if case["status"] == "open"),
    }
    return {
        "ok": True,
        "pbc": PBC_KEY,
        "queues": queues,
        "queue_counts": {name: len(items) for name, items in queues.items()},
        "task_queues": {
            queue: tuple(task for task in tasks if task["queue"] == queue and task["status"] != "completed")
            for queue in sorted({_derive_task_queue(task.get("task_type")) for task in tasks} | set(TASK_QUEUE_BY_TYPE.values()))
        },
        "side_effects": (),
    }


def forms_contract() -> dict:
    return {
        "ok": True,
        "forms": (
            {"form_id": "court_case_intake_form", "writes_table": "court_case_management_court_case", "fields": ("court", "division", "filing_year", "case_type", "caption", "assigned_judge", "access_class")},
            {"form_id": "party_representation_form", "writes_table": "court_case_management_party", "fields": ("case_id", "party_name", "role", "lead_counsel", "self_represented", "service_addresses", "aliases")},
            {"form_id": "filing_intake_form", "writes_table": "court_case_management_filing", "fields": ("case_id", "filing_type", "document_title", "deficiency_codes", "cure_deadline", "access_class")},
            {"form_id": "evidence_intake_form", "writes_table": "court_case_management_evidence_item", "fields": ("case_id", "filing_id", "hearing_id", "description", "submitted_by", "submitted_at", "storage_location", "admission_status")},
            {"form_id": "hearing_schedule_form", "writes_table": "court_case_management_hearing", "fields": ("case_id", "hearing_type", "scheduled_at", "courtroom", "session_block", "assigned_judge", "interpreter_required", "mode")},
            {"form_id": "order_drafting_form", "writes_table": "court_case_management_court_order", "fields": ("case_id", "title", "draft_text", "effective_date", "access_class")},
            {"form_id": "task_assignment_form", "writes_table": "court_case_management_case_task", "fields": ("case_id", "title", "task_type", "assignee", "due_date", "priority", "related_record_type", "related_record_id")},
        ),
        "side_effects": (),
    }


def wizards_contract() -> dict:
    return {
        "ok": True,
        "wizards": (
            {"wizard_id": "case_opening_wizard", "steps": ("assign_number", "capture_parties", "review_access_class", "open_case")},
            {"wizard_id": "filing_deficiency_wizard", "steps": ("receive_packet", "review_defects", "issue_notice", "accept_or_reject_cure")},
            {"wizard_id": "evidence_intake_wizard", "steps": ("log_evidence", "record_custody", "review_access_class", "queue_admission_review")},
            {"wizard_id": "hearing_calendar_wizard", "steps": ("select_case", "check_readiness", "reserve_courtroom", "confirm_setting")},
            {"wizard_id": "hearing_packet_wizard", "steps": ("collect_filings", "collect_evidence", "confirm_parties", "issue_preparation_tasks")},
            {"wizard_id": "order_entry_wizard", "steps": ("draft_order", "review_signature", "enter_on_docket", "service_linkage")},
            {"wizard_id": "task_follow_up_wizard", "steps": ("triage_case_queue", "assign_owner", "set_due_date", "record_completion")},
        ),
        "side_effects": (),
    }


def controls_contract() -> dict:
    return {
        "ok": True,
        "controls": (
            {"control_id": "case_number_uniqueness_guard", "blocks_on_failure": True, "table_scope": ("court_case_management_court_case",)},
            {"control_id": "filing_deficiency_acceptance_guard", "blocks_on_failure": True, "table_scope": ("court_case_management_filing",)},
            {"control_id": "docket_sequence_integrity_guard", "blocks_on_failure": True, "table_scope": ("court_case_management_docket_entry",)},
            {"control_id": "courtroom_double_booking_guard", "blocks_on_failure": True, "table_scope": ("court_case_management_hearing",)},
            {"control_id": "judge_double_booking_guard", "blocks_on_failure": True, "table_scope": ("court_case_management_hearing",)},
            {"control_id": "evidence_chain_of_custody_guard", "blocks_on_failure": True, "table_scope": ("court_case_management_evidence_item",)},
            {"control_id": "signed_order_entry_guard", "blocks_on_failure": True, "table_scope": ("court_case_management_court_order",)},
            {"control_id": "task_completion_authority_guard", "blocks_on_failure": True, "table_scope": ("court_case_management_case_task",)},
            {"control_id": "sealed_record_access_guard", "blocks_on_failure": True, "table_scope": OWNED_TABLES},
        ),
        "side_effects": (),
    }


def single_pbc_app_contract() -> dict:
    return {
        "ok": True,
        "pbc": PBC_KEY,
        "single_pbc_app": True,
        "database_backed": True,
        "owned_tables": OWNED_TABLES,
        "business_tables": BUSINESS_TABLES,
        "forms": forms_contract()["forms"],
        "wizards": wizards_contract()["wizards"],
        "controls": controls_contract()["controls"],
        "routes": ROUTES,
        "workbench": "CourtCaseManagementWorkbench",
        "detail_view": "CourtCaseManagementDetail",
        "assistant_panel": "CourtCaseManagementAssistantPanel",
        "service_methods": (
            "create_court_case",
            "add_party",
            "receive_filing",
            "cure_filing",
            "register_evidence",
            "schedule_hearing",
            "create_task",
            "complete_task",
            "draft_order",
            "sign_and_enter_order",
            "query_workbench",
            "query_case_detail",
        ),
        "side_effects": (),
    }


def document_instruction_mutation_plan(document: str, instruction: str) -> dict:
    text = f"{document} {instruction}".lower()
    if any(token in text for token in ("exhibit", "evidence", "custody")):
        action = "register_evidence"
        table = "court_case_management_evidence_item"
        skill = "evidence_intake"
    elif any(token in text for token in ("task", "follow up", "deadline", "queue")):
        action = "create_task"
        table = "court_case_management_case_task"
        skill = "task_assistance"
    elif "hearing" in text:
        action = "schedule_hearing"
        table = "court_case_management_hearing"
        skill = "hearing_preparation"
    elif "order" in text:
        action = "draft_order"
        table = "court_case_management_court_order"
        skill = "order_review"
    elif "party" in text or "counsel" in text:
        action = "add_party"
        table = "court_case_management_party"
        skill = "representation_update"
    elif "filing" in text or "motion" in text or "petition" in text:
        action = "receive_filing"
        table = "court_case_management_filing"
        skill = "filing_triage"
    else:
        action = "create_court_case"
        table = "court_case_management_court_case"
        skill = "case_intake"
    return {
        "ok": True,
        "pbc": PBC_KEY,
        "document_digest": _digest(document),
        "instruction": instruction,
        "proposed_action": action,
        "target_table": table,
        "assistant_skill": skill,
        "requires_human_confirmation": True,
        "crud_datastore_mutation": True,
        "event_contract": "AppGen-X",
        "side_effects": (),
    }


def court_operations_smoke_test() -> dict:
    state = empty_court_state()
    case = create_court_case(
        state,
        {
            "court": "CIV",
            "division": "LAW",
            "filing_year": 2026,
            "case_type": "civil",
            "caption": "Roe v. Example",
            "assigned_judge": "Judge Lane",
        },
    )
    party = add_party(case["state"], {"case_id": case["court_case"]["id"], "party_name": "Jane Roe", "role": "plaintiff", "lead_counsel": "A. Counsel"})
    deficient = receive_filing(
        party["state"],
        {
            "case_id": case["court_case"]["id"],
            "filing_type": "motion",
            "document_title": "Motion for Temporary Relief",
            "received_at": "2026-01-02",
            "deficiency_codes": ("missing_signature",),
            "cure_deadline": "2026-01-09",
        },
    )
    cured = cure_filing(deficient["state"], deficient["filing"]["id"], {"defects_cured": True, "evidence": "signed packet"})
    evidence = register_evidence(
        cured["state"],
        {
            "case_id": case["court_case"]["id"],
            "filing_id": deficient["filing"]["id"],
            "description": "Exhibit packet A",
            "submitted_by": "Jane Roe",
            "submitted_at": "2026-01-03",
        },
    )
    hearing = schedule_hearing(
        evidence["state"],
        {
            "case_id": case["court_case"]["id"],
            "hearing_type": "motion",
            "scheduled_at": "2026-01-20T09:00:00",
            "courtroom": "4A",
            "session_block": "AM",
            "assigned_judge": "Judge Lane",
        },
    )
    task = create_task(
        hearing["state"],
        {
            "case_id": case["court_case"]["id"],
            "title": "Serve entered order",
            "task_type": "service",
            "assignee": "clerk.one",
            "related_record_type": "hearing",
            "related_record_id": hearing["hearing"]["id"],
        },
    )
    completed_task = complete_task(task["state"], task["task"]["id"], {"completed_by": "clerk.one", "completion_notes": "Service issued."})
    order = draft_order(completed_task["state"], {"case_id": case["court_case"]["id"], "title": "Order Setting Hearing", "draft_text": "The motion is set."})
    entered = sign_and_enter_order(order["state"], order["court_order"]["id"], {"judge_signature": "Judge Lane", "signed_at": "2026-01-03T10:00:00"})
    detail = case_detail(entered["state"], case["court_case"]["id"], permissions=("court_case_management.admin",))
    workbench = court_workbench(entered["state"], permissions=("court_case_management.admin",))
    checks = (
        case["ok"],
        party["ok"],
        deficient["ok"] and deficient["filing"]["state"] == "deficient",
        cured["ok"] and cured["filing"]["state"] == "accepted",
        evidence["ok"] and evidence["evidence_item"]["exhibit_number"] == "EX-001",
        hearing["ok"],
        task["ok"],
        completed_task["ok"],
        order["ok"],
        entered["ok"],
        detail["ok"] and detail["counts"]["evidence_items"] == 1,
        workbench["ok"] and workbench["queue_counts"]["open_cases"] == 1,
        single_pbc_app_contract()["ok"],
        document_instruction_mutation_plan("Exhibit packet", "log evidence") ["proposed_action"] == "register_evidence",
    )
    return {
        "ok": all(checks),
        "state": entered["state"],
        "workbench": workbench,
        "detail": detail,
        "single_pbc_app": single_pbc_app_contract(),
        "side_effects": (),
    }
