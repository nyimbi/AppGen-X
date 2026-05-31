from .runtime import trade_finance_operations_build_release_evidence


def build_release_evidence():
    return trade_finance_operations_build_release_evidence()


def release_readiness_manifest():
    evidence = build_release_evidence()
    return {
        "ok": evidence["ok"],
        "pbc": evidence["pbc"],
        "sections": ("schema", "services", "events", "handlers", "ui", "agent", "governance", "forms", "wizards", "controls", "standalone"),
        "blocking_gaps": tuple(evidence.get("blocking_gaps", ())),
        "boundary_gaps": (),
        "evidence": evidence,
        "side_effects": (),
    }


def validate_release_evidence():
    manifest = release_readiness_manifest()
    return {
        "ok": manifest["ok"],
        "pbc": manifest["pbc"],
        "missing_sections": (),
        "failed_checks": tuple(item for item in manifest["evidence"].get("checks", ()) if not item.get("ok")),
        "boundary_gaps": (),
        "side_effects": (),
    }


def smoke_test():
    manifest = release_readiness_manifest()
    validation = validate_release_evidence()
    return {"ok": manifest["ok"] and validation["ok"], "manifest": manifest, "validation": validation, "side_effects": ()}


# Improve1 trade finance operations control release extension.
from .trade_finance_operations_control import improve1_trade_finance_operations_control_contract as _improve1_trade_finance_operations_control_contract

_TRADE_CONTROL_BASE_BUILD_RELEASE_EVIDENCE = build_release_evidence
_TRADE_CONTROL_BASE_VALIDATE_RELEASE_EVIDENCE = validate_release_evidence


def build_release_evidence() -> dict:
    evidence = dict(_TRADE_CONTROL_BASE_BUILD_RELEASE_EVIDENCE())
    control = _improve1_trade_finance_operations_control_contract()
    checks = tuple(evidence.get("checks", ())) + ({"id": "improve1_trade_finance_operations_control", "ok": control["ok"]},)
    evidence.update({
        "ok": bool(evidence.get("ok")) and control["ok"],
        "checks": checks,
        "trade_finance_operations_control": control,
        "blocking_gaps": tuple(evidence.get("blocking_gaps", ())) + tuple(control.get("blocking_gaps", ())),
    })
    return evidence


def validate_release_evidence() -> dict:
    validation = dict(_TRADE_CONTROL_BASE_VALIDATE_RELEASE_EVIDENCE())
    control = _improve1_trade_finance_operations_control_contract()
    validation["ok"] = validation.get("ok") is True and control["ok"]
    validation["trade_finance_operations_control"] = control
    validation["blocking_gaps"] = tuple(validation.get("blocking_gaps", ())) + tuple(control.get("blocking_gaps", ()))
    return validation
