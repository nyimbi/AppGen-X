"""Idempotent event handler stubs for agriculture_farm_operations."""

from __future__ import annotations

from .events import EVENT_CONTRACT

_HANDLED = set()


def handler_manifest() -> dict:
    return {
        "ok": True,
        "pbc": "agriculture_farm_operations",
        "handlers": tuple(
            {"event_type": event_type, "handler": f"handle_{event_type.lower()}"}
            for event_type in EVENT_CONTRACT["consumed"]
        ),
        "consumes": EVENT_CONTRACT["consumed"],
        "idempotency_key": "required",
        "retry_policy": EVENT_CONTRACT["retry_policy"],
        "dead_letter_table": EVENT_CONTRACT["dead_letter_table"],
        "side_effects": (),
    }


def dispatch_event(event: dict) -> dict:
    idem = event.get("idempotency_key") or event.get("event_id") or repr(event)
    if idem in _HANDLED:
        return {"ok": True, "handled": True, "duplicate": True, "idempotency_key": idem, "side_effects": ()}
    _HANDLED.add(idem)
    if event.get("event_type") not in EVENT_CONTRACT["consumed"]:
        return {
            "ok": False,
            "handled": False,
            "dead_letter_table": EVENT_CONTRACT["dead_letter_table"],
            "retry_policy": EVENT_CONTRACT["retry_policy"],
            "idempotency_key": idem,
            "side_effects": (),
        }
    return {
        "ok": True,
        "handled": True,
        "duplicate": False,
        "dead_letter_table": EVENT_CONTRACT["dead_letter_table"],
        "retry_policy": EVENT_CONTRACT["retry_policy"],
        "idempotency_key": idem,
        "side_effects": (),
    }


def smoke_test() -> dict:
    manifest = handler_manifest()
    first = dispatch_event({"event_type": EVENT_CONTRACT["consumed"][0], "idempotency_key": "agri:smoke"})
    duplicate = dispatch_event({"event_type": EVENT_CONTRACT["consumed"][0], "idempotency_key": "agri:smoke"})
    unknown = dispatch_event({"event_type": "Unexpected", "idempotency_key": "agri:bad"})
    return {
        "ok": manifest["ok"] and first["ok"] and duplicate["duplicate"] and unknown["handled"] is False,
        "manifest": manifest,
        "first_result": first,
        "duplicate_result": duplicate,
        "unknown_result": unknown,
        "side_effects": (),
    }
