from .slice_app import chatbot_interface_contract
from .slice_app import composed_agent_contribution
from .slice_app import datastore_crud_plan
from .slice_app import document_instruction_plan
from .slice_app import agent_skill_manifest
from .slice_app import PBC_KEY

OWNED_TABLES = (
    "food_safety_quality_compliance_haccp_plan",
    "food_safety_quality_compliance_critical_control_point",
    "food_safety_quality_compliance_inspection",
    "food_safety_quality_compliance_nonconformance",
    "food_safety_quality_compliance_recall_event",
    "food_safety_quality_compliance_supplier_audit",
    "food_safety_quality_compliance_quality_hold",
    "food_safety_quality_compliance_food_safety_quality_compliance_policy_rule",
    "food_safety_quality_compliance_food_safety_quality_compliance_runtime_parameter",
    "food_safety_quality_compliance_food_safety_quality_compliance_schema_extension",
    "food_safety_quality_compliance_food_safety_quality_compliance_control_assertion",
    "food_safety_quality_compliance_food_safety_quality_compliance_governed_model",
    "food_safety_quality_compliance_appgen_outbox_event",
    "food_safety_quality_compliance_appgen_inbox_event",
    "food_safety_quality_compliance_appgen_dead_letter_event",
)


def smoke_test():
    return {
        "ok": agent_skill_manifest()["ok"]
        and chatbot_interface_contract()["ok"]
        and document_instruction_plan("doc", "create")["ok"]
        and datastore_crud_plan("create")["ok"]
        and datastore_crud_plan("update", table="foreign_table")["ok"] is False
        and composed_agent_contribution()["ok"],
        "side_effects": (),
    }
