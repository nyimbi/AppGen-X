"""Executable deposit-account lifecycle helpers for banking_core_accounts."""
from __future__ import annotations

from copy import deepcopy
import hashlib

PBC_KEY = "banking_core_accounts"
EVENT_CONTRACT = "AppGen-X"
EVENT_TOPIC = f"pbc.{PBC_KEY}.events"
OWNED_DEPOSIT_ACCOUNT_TABLE = f"{PBC_KEY}_deposit_account"

LIFECYCLE_STATES = (
    "pending",
    "approved",
    "active",
    "restricted",
    "dormant",
    "closed",
    "reopened",
)

ALLOWED_TRANSITIONS = {
    "pending": ("approved", "closed"),
    "approved": ("active", "closed"),
    "active": ("restricted", "dormant", "closed"),
    "restricted": ("active", "closed"),
    "dormant": ("active", "closed"),
    "closed": ("reopened",),
    "reopened": ("active",),
}

APPROVAL_REQUIRED_STATES = frozenset(("approved", "closed", "reopened"))
REASON_REQUIRED_STATES = frozenset(("restricted", "closed", "reopened"))
ACTION_BY_TRANSITION = {
    ("pending", "approved"): "approve",
    ("pending", "closed"): "close",
    ("approved", "active"): "activate",
    ("approved", "closed"): "close",
    ("active", "restricted"): "restrict",
    ("active", "dormant"): "mark_dormant",
    ("active", "closed"): "close",
    ("restricted", "active"): "activate",
    ("restricted", "closed"): "close",
    ("dormant", "active"): "reactivate",
    ("dormant", "closed"): "close",
    ("closed", "reopened"): "reopen",
    ("reopened", "active"): "activate",
}

DOMAIN_EVENT_BY_STATE = {
    "pending": "DepositAccountOpened",
    "approved": "DepositAccountApproved",
    "active": "DepositAccountActivated",
    "restricted": "DepositAccountRestricted",
    "dormant": "DepositAccountDormant",
    "closed": "DepositAccountClosed",
    "reopened": "DepositAccountReopened",
}

COMPATIBILITY_EVENT_BY_STATE = {
    "pending": "BankingCoreAccountsCreated",
    "approved": "BankingCoreAccountsApproved",
    "active": "BankingCoreAccountsUpdated",
    "restricted": "BankingCoreAccountsExceptionOpened",
    "dormant": "BankingCoreAccountsUpdated",
    "closed": "BankingCoreAccountsUpdated",
    "reopened": "BankingCoreAccountsUpdated",
}


def _digest(value: object) -> str:
    return hashlib.sha256(repr(value).encode("utf-8")).hexdigest()


def _copy_state(state: dict) -> dict:
    next_state = deepcopy(state)
    next_state["idempotency_keys"] = set(state.get("idempotency_keys", set()))
    next_state["command_receipts"] = dict(state.get("command_receipts", {}))
    return next_state


def _receipt_key(payload: dict, operation: str) -> str:
    explicit = payload.get("idempotency_key")
    if explicit:
        return str(explicit)
    stable_bits = (
        operation,
        payload.get("tenant", "default"),
        payload.get("account_id") or payload.get("id") or payload.get("code"),
        payload.get("target_state"),
        payload.get("source_reference"),
        payload.get("reason"),
    )
    return _digest(stable_bits)


def _allowed_next_states(state_name: str) -> tuple[str, ...]:
    return tuple(ALLOWED_TRANSITIONS.get(state_name, ()))


def _allowed_next_actions(state_name: str) -> tuple[str, ...]:
    next_states = _allowed_next_states(state_name)
    return tuple(ACTION_BY_TRANSITION[(state_name, target)] for target in next_states)


def _detail_projection(record: dict) -> dict:
    lifecycle_state = record["lifecycle_state"]
    transition_history = tuple(record.get("lifecycle_history", ()))
    return {
        "account_id": record["id"],
        "tenant": record["tenant"],
        "account_number": record["account_number"],
        "customer_id": record["customer_id"],
        "product_code": record["product_code"],
        "currency": record["currency"],
        "lifecycle_state": lifecycle_state,
        "status": lifecycle_state,
        "maker_checker_required": record["maker_checker_required"],
        "allowed_next_states": _allowed_next_states(lifecycle_state),
        "allowed_next_actions": _allowed_next_actions(lifecycle_state),
        "transition_count": len(transition_history),
        "transition_history": transition_history,
        "current_restriction_reason": record.get("current_restriction_reason"),
        "last_transition_reason": record.get("last_transition_reason"),
        "version": record["version"],
        "shared_table_access": False,
        "event_contract": EVENT_CONTRACT,
    }


def lifecycle_contract() -> dict:
    return {
        "ok": True,
        "pbc": PBC_KEY,
        "lifecycle_states": LIFECYCLE_STATES,
        "allowed_transitions": tuple(
            {
                "from_state": state_name,
                "to_states": targets,
                "actions": _allowed_next_actions(state_name),
            }
            for state_name, targets in ALLOWED_TRANSITIONS.items()
        ),
        "approval_required_states": tuple(APPROVAL_REQUIRED_STATES),
        "reason_required_states": tuple(REASON_REQUIRED_STATES),
        "owned_table": OWNED_DEPOSIT_ACCOUNT_TABLE,
        "event_contract": EVENT_CONTRACT,
        "stream_engine_picker_visible": False,
        "shared_table_access": False,
        "side_effects": (),
    }


def _append_outbox_event(next_state: dict, account: dict, transition: dict) -> dict:
    lifecycle_state = account["lifecycle_state"]
    outbox_event = {
        "event_type": COMPATIBILITY_EVENT_BY_STATE[lifecycle_state],
        "domain_event_type": DOMAIN_EVENT_BY_STATE[lifecycle_state],
        "topic": EVENT_TOPIC,
        "payload": {
            "account_id": account["id"],
            "tenant": account["tenant"],
            "lifecycle_state": lifecycle_state,
            "transition": dict(transition),
            "allowed_next_actions": _allowed_next_actions(lifecycle_state),
        },
        "idempotency_key": transition["idempotency_key"],
        "event_contract": EVENT_CONTRACT,
    }
    next_state.setdefault("outbox", []).append(outbox_event)
    return outbox_event


def _duplicate_response(next_state: dict, receipt: dict) -> dict:
    record = next_state.get("records", {}).get(receipt["account_id"])
    return {
        "ok": record is not None,
        "duplicate": True,
        "state": next_state,
        "account": _detail_projection(record) if record else None,
        "idempotency_key": receipt["idempotency_key"],
        "operation": receipt["operation"],
        "event_contract": EVENT_CONTRACT,
        "shared_table_access": False,
        "side_effects": (),
    }


def open_deposit_account(state: dict, payload: dict | None = None) -> dict:
    payload = dict(payload or {})
    next_state = _copy_state(state)
    idempotency_key = _receipt_key(payload, "open_deposit_account")
    receipt = next_state["command_receipts"].get(idempotency_key)
    if receipt:
        return _duplicate_response(next_state, receipt)

    account_id = payload.get("account_id") or payload.get("id") or payload.get("code")
    if not account_id:
        account_id = f"deposit-account-{len(next_state.get('records', {})) + 1}"
    if account_id in next_state.get("records", {}):
        return {
            "ok": False,
            "state": next_state,
            "reason": "account_already_exists",
            "account_id": account_id,
            "shared_table_access": False,
            "side_effects": (),
        }

    actor_id = payload.get("actor_id") or payload.get("maker_id") or "system"
    transition = {
        "from_state": None,
        "to_state": "pending",
        "action": "open",
        "actor_id": actor_id,
        "approver_id": None,
        "reason": payload.get("reason", "account_opening"),
        "effective_at": payload.get("effective_at", "logical-now"),
        "source_reference": payload.get("source_reference"),
        "idempotency_key": idempotency_key,
    }
    record = {
        "id": account_id,
        "tenant": payload.get("tenant", "default"),
        "account_number": payload.get("account_number", account_id),
        "customer_id": payload.get("customer_id", "customer-unknown"),
        "product_code": payload.get("product_code", "generic-deposit"),
        "currency": payload.get("currency", "USD"),
        "lifecycle_state": "pending",
        "status": "pending",
        "maker_checker_required": bool(payload.get("maker_checker_required", True)),
        "current_restriction_reason": None,
        "last_transition_reason": transition["reason"],
        "payload": payload,
        "lifecycle_history": [transition],
        "version": 1,
    }
    next_state.setdefault("records", {})[account_id] = record
    emitted_event = _append_outbox_event(next_state, record, transition)
    next_state["command_receipts"][idempotency_key] = {
        "operation": "open_deposit_account",
        "account_id": account_id,
        "idempotency_key": idempotency_key,
    }
    return {
        "ok": True,
        "duplicate": False,
        "state": next_state,
        "account": _detail_projection(record),
        "transition": transition,
        "emitted_event": emitted_event,
        "transaction_boundary": "owned_datastore_plus_outbox",
        "event_contract": EVENT_CONTRACT,
        "shared_table_access": False,
        "side_effects": (),
    }


def transition_deposit_account(state: dict, payload: dict | None = None) -> dict:
    payload = dict(payload or {})
    next_state = _copy_state(state)
    idempotency_key = _receipt_key(payload, "transition_deposit_account")
    receipt = next_state["command_receipts"].get(idempotency_key)
    if receipt:
        return _duplicate_response(next_state, receipt)

    account_id = payload.get("account_id") or payload.get("id")
    record = next_state.get("records", {}).get(account_id)
    if record is None:
        return {
            "ok": False,
            "state": next_state,
            "reason": "account_not_found",
            "account_id": account_id,
            "shared_table_access": False,
            "side_effects": (),
        }

    target_state = payload.get("target_state")
    if target_state not in LIFECYCLE_STATES:
        return {
            "ok": False,
            "state": next_state,
            "reason": "invalid_target_state",
            "target_state": target_state,
            "shared_table_access": False,
            "side_effects": (),
        }

    current_state = record["lifecycle_state"]
    if target_state not in ALLOWED_TRANSITIONS.get(current_state, ()):
        return {
            "ok": False,
            "state": next_state,
            "reason": "invalid_lifecycle_transition",
            "account": _detail_projection(record),
            "attempted_target_state": target_state,
            "shared_table_access": False,
            "side_effects": (),
        }

    reason = payload.get("reason")
    if target_state in REASON_REQUIRED_STATES and not reason:
        return {
            "ok": False,
            "state": next_state,
            "reason": "transition_reason_required",
            "attempted_target_state": target_state,
            "shared_table_access": False,
            "side_effects": (),
        }

    actor_id = payload.get("actor_id") or payload.get("maker_id") or "system"
    approver_id = payload.get("approver_id")
    maker_checker_required = bool(
        payload.get("maker_checker_required", record.get("maker_checker_required", True))
    )
    if maker_checker_required and target_state in APPROVAL_REQUIRED_STATES:
        if not approver_id or approver_id == actor_id:
            return {
                "ok": False,
                "state": next_state,
                "reason": "maker_checker_violation",
                "attempted_target_state": target_state,
                "shared_table_access": False,
                "side_effects": (),
            }

    transition = {
        "from_state": current_state,
        "to_state": target_state,
        "action": ACTION_BY_TRANSITION[(current_state, target_state)],
        "actor_id": actor_id,
        "approver_id": approver_id,
        "reason": reason,
        "effective_at": payload.get("effective_at", "logical-now"),
        "source_reference": payload.get("source_reference"),
        "idempotency_key": idempotency_key,
    }
    record["lifecycle_state"] = target_state
    record["status"] = target_state
    record["maker_checker_required"] = maker_checker_required
    record["last_transition_reason"] = reason
    record["current_restriction_reason"] = (
        reason if target_state == "restricted" else None
    )
    record["version"] = int(record.get("version", 1)) + 1
    record.setdefault("lifecycle_history", []).append(transition)
    emitted_event = _append_outbox_event(next_state, record, transition)
    next_state["command_receipts"][idempotency_key] = {
        "operation": "transition_deposit_account",
        "account_id": account_id,
        "idempotency_key": idempotency_key,
    }
    return {
        "ok": True,
        "duplicate": False,
        "state": next_state,
        "account": _detail_projection(record),
        "transition": transition,
        "emitted_event": emitted_event,
        "transaction_boundary": "owned_datastore_plus_outbox",
        "event_contract": EVENT_CONTRACT,
        "shared_table_access": False,
        "side_effects": (),
    }


def query_account_detail(state: dict, account_id: str) -> dict:
    record = state.get("records", {}).get(account_id)
    if record is None:
        return {
            "ok": False,
            "reason": "account_not_found",
            "account_id": account_id,
            "read_only": True,
            "shared_table_access": False,
            "side_effects": (),
        }
    return {
        "ok": True,
        "account": _detail_projection(record),
        "read_only": True,
        "event_contract": EVENT_CONTRACT,
        "shared_table_access": False,
        "side_effects": (),
    }


def query_workbench(state: dict, filters: dict | None = None) -> dict:
    filters = dict(filters or {})
    tenant = filters.get("tenant")
    lifecycle_state = filters.get("lifecycle_state")
    customer_id = filters.get("customer_id")
    projected_accounts = []
    for record in state.get("records", {}).values():
        if tenant and record["tenant"] != tenant:
            continue
        if lifecycle_state and record["lifecycle_state"] != lifecycle_state:
            continue
        if customer_id and record["customer_id"] != customer_id:
            continue
        projected_accounts.append(_detail_projection(record))
    projected_accounts.sort(key=lambda item: item["account_id"])

    counts = []
    for state_name in LIFECYCLE_STATES:
        count = sum(1 for item in projected_accounts if item["lifecycle_state"] == state_name)
        if count:
            counts.append({"lifecycle_state": state_name, "count": count})

    return {
        "ok": True,
        "records": tuple(projected_accounts),
        "filters": filters,
        "summary": {
            "total_accounts": len(projected_accounts),
            "lifecycle_counts": tuple(counts),
            "customer_id": customer_id,
        },
        "read_only": True,
        "event_contract": EVENT_CONTRACT,
        "shared_table_access": False,
        "side_effects": (),
    }
