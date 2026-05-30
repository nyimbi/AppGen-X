from __future__ import annotations

PBC_KEY = "donor_grant_fundraising"
SEED_RECORDS = (
    {"table": "donor_grant_fundraising_donor", "code": "FOUNDATION_SEED", "name": "Evergreen Foundation", "donor_type": "foundation", "recognition_preference": "named_report"},
    {"table": "donor_grant_fundraising_campaign", "code": "CAMPAIGN_SEED", "name": "2026 Leadership Giving", "objective_category": "leadership_giving", "goal_amount": 250000},
    {"table": "donor_grant_fundraising_restriction", "code": "RESTRICTION_SEED", "restriction_type": "purpose", "purpose_code": "education"},
)


def seed_plan() -> dict:
    return {"ok": True, "pbc": PBC_KEY, "records": SEED_RECORDS, "side_effects": ()}


def validate_seed_data() -> dict:
    invalid = tuple(record for record in SEED_RECORDS if not record["table"].startswith(f"{PBC_KEY}_"))
    return {"ok": not invalid, "pbc": PBC_KEY, "invalid_records": invalid, "side_effects": ()}


def smoke_test() -> dict:
    return {"ok": seed_plan()["ok"] and validate_seed_data()["ok"], "side_effects": ()}
