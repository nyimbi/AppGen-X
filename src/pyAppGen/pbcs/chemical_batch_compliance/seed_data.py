"""Package-local seed data for the implemented chemical batch slice."""

from __future__ import annotations

from .slice_app import BATCH_TABLE
from .slice_app import FORMULA_TABLE
from .slice_app import GOVERNED_MODEL_TABLE
from .slice_app import HAZARDOUS_MATERIAL_TABLE
from .slice_app import PBC_KEY
from .slice_app import SDS_TABLE


def seed_plan() -> dict:
    return {
        "ok": True,
        "pbc": PBC_KEY,
        "records": (
            {
                "table": SDS_TABLE,
                "id": "sds-SOLV-100-7",
                "tenant": "demo",
                "material_code": "SOLV-100",
                "revision": "7",
                "status": "approved",
            },
            {
                "table": HAZARDOUS_MATERIAL_TABLE,
                "id": "hazmat-SOLV-100",
                "tenant": "demo",
                "material_code": "SOLV-100",
                "status": "qualified",
            },
            {
                "table": FORMULA_TABLE,
                "id": "formula-CBR-77-rev-A",
                "tenant": "demo",
                "formula_code": "CBR-77",
                "revision": "A",
                "lifecycle_state": "effective",
            },
            {
                "table": BATCH_TABLE,
                "id": "batch-BATCH-1001",
                "tenant": "demo",
                "batch_number": "BATCH-1001",
                "formula_id": "formula-CBR-77-rev-A",
                "release_decision": "pending_quality",
            },
            {
                "table": GOVERNED_MODEL_TABLE,
                "id": "instruction-0001",
                "tenant": "demo",
                "artifact_type": "document_instruction",
                "status": "draft",
            },
        ),
        "side_effects": (),
    }


def validate_seed_data() -> dict:
    records = seed_plan()["records"]
    invalid_tables = tuple(record["table"] for record in records if not record["table"].startswith(f"{PBC_KEY}_"))
    return {"ok": not invalid_tables, "pbc": PBC_KEY, "invalid_tables": invalid_tables, "side_effects": ()}


def smoke_test() -> dict:
    return {"ok": seed_plan()["ok"] and validate_seed_data()["ok"], "side_effects": ()}
