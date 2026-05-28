"""Event handlers for the package-local AppGen-X inbox/dead-letter slice."""

from __future__ import annotations

from typing import Any

from .events import CONSUMED
from .models import EVENT_TABLES
from .models import PBC_KEY
from .runtime import claims_adjudication_healthcare_empty_state
from .runtime import claims_adjudication_healthcare_receive_event

_STATE = claims_adjudication_healthcare_empty_state()


def handler_manifest() -> dict[str, Any]:
    return {
        "ok": True,
        "pbc": PBC_KEY,
        "consumes": CONSUMED,
        "idempotency_key": "required",
        "retry_policy": {"max_attempts": 5},
        "dead_letter_table": EVENT_TABLES[2],
        "side_effects": (),
    }


def dispatch_event(event: dict[str, Any], state: dict[str, Any] | None = None) -> dict[str, Any]:
    active_state = _STATE if state is None else state
    result = claims_adjudication_healthcare_receive_event(active_state, event)
    if state is None:
        _STATE.clear()
        _STATE.update(result["state"])
    return {
        "ok": result["ok"],
        "duplicate": result.get("duplicate", False),
        "idempotency_key": result["idempotency_key"],
        "retry_policy": result.get("retry_policy", {"max_attempts": 5}),
        "dead_letter_table": result.get("dead_letter_table"),
        "state": result["state"],
        "side_effects": (),
    }


def smoke_test() -> dict[str, Any]:
    local = claims_adjudication_healthcare_empty_state()
    first = dispatch_event({"event_type": CONSUMED[0], "idempotency_key": f"{PBC_KEY}:smoke"}, state=local)
    second = dispatch_event({"event_type": CONSUMED[0], "idempotency_key": f"{PBC_KEY}:smoke"}, state=first["state"])
    failed = dispatch_event({"event_type": "Unexpected", "idempotency_key": f"{PBC_KEY}:bad"}, state=second["state"])
    return {
        "ok": first["ok"] and second["duplicate"] and failed["dead_letter_table"] == EVENT_TABLES[2],
        "side_effects": (),
    }
