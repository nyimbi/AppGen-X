"""Seed data for the insurance_claims_policy PBC."""

PBC_KEY = "insurance_claims_policy"
SEED_ROWS = (
    {"table": f"{PBC_KEY}_insurance_policy", "code": "POL-DEMO-001", "status": "issued", "policy_number": "POL-DEMO-001"},
    {"table": f"{PBC_KEY}_policy_coverage", "code": "COV-FIRE", "status": "active", "coverage_code": "building", "peril_code": "fire"},
    {"table": f"{PBC_KEY}_claim_record", "code": "CLM-DEMO-001", "status": "open", "claim_number": "CLM-DEMO-001"},
)


def seed_plan() -> dict:
    return {"ok": True, "pbc": PBC_KEY, "rows": SEED_ROWS, "side_effects": ()}


def validate_seed_data() -> dict:
    invalid = tuple(row for row in SEED_ROWS if not row["table"].startswith(f"{PBC_KEY}_"))
    return {"ok": not invalid, "rows": SEED_ROWS, "invalid": invalid, "side_effects": ()}


def smoke_test() -> dict:
    return {"ok": seed_plan()["ok"] and validate_seed_data()["ok"], "side_effects": ()}
