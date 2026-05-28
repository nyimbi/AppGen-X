"""Owned model definitions for the executable BIM operations slice."""
from __future__ import annotations

from dataclasses import dataclass

PBC_KEY = "building_information_modeling_ops"


@dataclass(frozen=True)
class OwnedModelDefinition:
    class_name: str
    table: str
    fields: tuple[str, ...]
    primary_key: tuple[str, ...] = ("id",)
    database_backed: bool = True


OWNED_MODELS = (
    OwnedModelDefinition(
        class_name="BuildingInformationModelingOpsBimModel",
        table=f"{PBC_KEY}_bim_model",
        fields=(
            "id",
            "tenant",
            "model_code",
            "discipline",
            "authoring_party",
            "status",
            "payload",
            "created_at",
            "updated_at",
        ),
    ),
    OwnedModelDefinition(
        class_name="BuildingInformationModelingOpsModelVersion",
        table=f"{PBC_KEY}_model_version",
        fields=(
            "id",
            "model_id",
            "tenant",
            "discipline",
            "issue_purpose",
            "approval_state",
            "coordinate_basis",
            "survey_point_json",
            "project_base_point_json",
            "true_north_degrees",
            "elevation_datum",
            "unit_scale",
            "lod_target",
            "checksum",
            "superseded_by_version_id",
            "payload",
            "created_at",
            "updated_at",
        ),
    ),
    OwnedModelDefinition(
        class_name="BuildingInformationModelingOpsClashIssue",
        table=f"{PBC_KEY}_clash_issue",
        fields=(
            "id",
            "tenant",
            "version_id",
            "severity",
            "status",
            "payload",
            "created_at",
            "updated_at",
        ),
    ),
    OwnedModelDefinition(
        class_name="BuildingInformationModelingOpsAssetObject",
        table=f"{PBC_KEY}_asset_object",
        fields=(
            "id",
            "tenant",
            "version_id",
            "asset_tag",
            "system_name",
            "location_code",
            "status",
            "payload",
            "created_at",
            "updated_at",
        ),
    ),
    OwnedModelDefinition(
        class_name="BuildingInformationModelingOpsHandoverPackage",
        table=f"{PBC_KEY}_handover_package",
        fields=(
            "id",
            "tenant",
            "federation_id",
            "status",
            "payload",
            "created_at",
            "updated_at",
        ),
    ),
    OwnedModelDefinition(
        class_name="BuildingInformationModelingOpsModelReview",
        table=f"{PBC_KEY}_model_review",
        fields=(
            "id",
            "tenant",
            "version_id",
            "review_type",
            "status",
            "payload",
            "created_at",
            "updated_at",
        ),
    ),
    OwnedModelDefinition(
        class_name="BuildingInformationModelingOpsDigitalTwinLink",
        table=f"{PBC_KEY}_digital_twin_link",
        fields=(
            "id",
            "tenant",
            "version_id",
            "status",
            "payload",
            "created_at",
            "updated_at",
        ),
    ),
    OwnedModelDefinition(
        class_name="BuildingInformationModelingOpsPolicyRule",
        table=f"{PBC_KEY}_building_information_modeling_ops_policy_rule",
        fields=(
            "id",
            "tenant",
            "rule_code",
            "rule_scope",
            "status",
            "payload",
            "created_at",
            "updated_at",
        ),
    ),
    OwnedModelDefinition(
        class_name="BuildingInformationModelingOpsRuntimeParameter",
        table=f"{PBC_KEY}_building_information_modeling_ops_runtime_parameter",
        fields=(
            "id",
            "tenant",
            "parameter_name",
            "parameter_value",
            "status",
            "payload",
            "created_at",
            "updated_at",
        ),
    ),
    OwnedModelDefinition(
        class_name="BuildingInformationModelingOpsSchemaExtension",
        table=f"{PBC_KEY}_building_information_modeling_ops_schema_extension",
        fields=(
            "id",
            "tenant",
            "table_name",
            "field_name",
            "status",
            "payload",
            "created_at",
            "updated_at",
        ),
    ),
    OwnedModelDefinition(
        class_name="BuildingInformationModelingOpsControlAssertion",
        table=f"{PBC_KEY}_building_information_modeling_ops_control_assertion",
        fields=(
            "id",
            "tenant",
            "control_code",
            "target_scope",
            "status",
            "payload",
            "created_at",
            "updated_at",
        ),
    ),
    OwnedModelDefinition(
        class_name="BuildingInformationModelingOpsGovernedModel",
        table=f"{PBC_KEY}_building_information_modeling_ops_governed_model",
        fields=(
            "id",
            "tenant",
            "federation_id",
            "release_status",
            "payload",
            "created_at",
            "updated_at",
        ),
    ),
    OwnedModelDefinition(
        class_name="BuildingInformationModelingOpsAppGenOutboxEvent",
        table=f"{PBC_KEY}_appgen_outbox_event",
        fields=(
            "id",
            "tenant",
            "event_type",
            "topic",
            "payload",
            "created_at",
        ),
    ),
    OwnedModelDefinition(
        class_name="BuildingInformationModelingOpsAppGenInboxEvent",
        table=f"{PBC_KEY}_appgen_inbox_event",
        fields=(
            "id",
            "tenant",
            "event_type",
            "topic",
            "payload",
            "created_at",
        ),
    ),
    OwnedModelDefinition(
        class_name="BuildingInformationModelingOpsAppGenDeadLetterEvent",
        table=f"{PBC_KEY}_appgen_dead_letter_event",
        fields=(
            "id",
            "tenant",
            "event_type",
            "topic",
            "payload",
            "failure_reason",
            "created_at",
        ),
    ),
)


def model_contracts() -> tuple[dict, ...]:
    return tuple(
        {
            "class_name": model.class_name,
            "table": model.table,
            "fields": model.fields,
            "primary_key": model.primary_key,
            "database_backed": model.database_backed,
        }
        for model in OWNED_MODELS
    )


def owned_model_registry() -> dict:
    return {
        "ok": True,
        "pbc": PBC_KEY,
        "models": model_contracts(),
        "database_backed": True,
        "migration": "migrations/001_initial.sql",
        "side_effects": (),
    }
