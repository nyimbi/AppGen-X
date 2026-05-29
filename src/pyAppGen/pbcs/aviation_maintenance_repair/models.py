"""Package-local model contracts for aviation maintenance repair."""
from __future__ import annotations

PBC_KEY = "aviation_maintenance_repair"


def _field(
    name: str,
    field_type: str,
    *,
    required: bool = False,
    description: str = "",
    enum: tuple[str, ...] | None = None,
) -> dict:
    field = {
        "name": name,
        "type": field_type,
        "required": required,
        "description": description,
    }
    if enum:
        field["enum"] = tuple(enum)
    return field


BUSINESS_MODEL_DEFINITIONS = (
    {
        "entity": "aircraft",
        "class_name": "AircraftRecord",
        "table": f"{PBC_KEY}_aircraft",
        "description": "Tail-level maintenance release planning baseline.",
        "required_fields": ("id", "tenant", "tail_number", "aircraft_type"),
        "status_values": ("active", "maintenance", "grounded", "released"),
        "fields": (
            _field("id", "text", required=True, description="Package-local aircraft identifier."),
            _field("tenant", "text", required=True, description="Tenant or operator boundary."),
            _field("tail_number", "text", required=True, description="Aircraft tail number."),
            _field("aircraft_type", "text", required=True, description="Fleet type used for task authorization."),
            _field("fleet_subtype", "text", description="Subtype or effectivity marker."),
            _field("status", "text", description="Aircraft operational status."),
            _field("utilization_hours", "number", description="Current flight hour accrual."),
            _field("utilization_cycles", "number", description="Current flight cycle accrual."),
            _field("grounded", "boolean", description="Whether the aircraft is currently grounded."),
            _field("payload", "json", description="Additional governed evidence."),
            _field("created_at", "datetime", description="Creation timestamp."),
            _field("updated_at", "datetime", description="Last update timestamp."),
        ),
    },
    {
        "entity": "component",
        "class_name": "ComponentRecord",
        "table": f"{PBC_KEY}_component",
        "description": "Serialized component with traceability and life limits.",
        "required_fields": ("id", "tenant", "component_id", "serial_number"),
        "status_values": ("serviceable", "installed", "quarantined", "removed"),
        "fields": (
            _field("id", "text", required=True, description="Package-local component identifier."),
            _field("tenant", "text", required=True, description="Tenant or operator boundary."),
            _field("component_id", "text", required=True, description="Operational component identifier."),
            _field("serial_number", "text", required=True, description="Serialized unit identifier."),
            _field("part_number", "text", description="Part number."),
            _field("aircraft_id", "text", description="Installed aircraft reference."),
            _field("aircraft_type", "text", description="Aircraft type currently served."),
            _field("status", "text", description="Component service state."),
            _field("remaining_hours", "number", description="Remaining hour life."),
            _field("remaining_cycles", "number", description="Remaining cycle life."),
            _field("quarantine_state", "text", description="Quarantine or suspect state."),
            _field("release_certificate", "text", description="Authorized release certificate identifier."),
            _field("shelf_life_expiry", "date", description="Shelf or certification expiry."),
            _field("effectivity_aircraft_types", "tuple[text]", description="Allowed aircraft types."),
            _field("effectivity_tail_numbers", "tuple[text]", description="Allowed tail numbers."),
            _field("payload", "json", description="Additional governed evidence."),
            _field("created_at", "datetime", description="Creation timestamp."),
            _field("updated_at", "datetime", description="Last update timestamp."),
        ),
    },
    {
        "entity": "work_card",
        "class_name": "WorkCardRecord",
        "table": f"{PBC_KEY}_work_card",
        "description": "Executable work-card closeout evidence and signoff state.",
        "required_fields": ("id", "tenant", "work_card_id", "aircraft_type", "task_family"),
        "status_values": ("open", "in_progress", "closed", "signed", "complete"),
        "fields": (
            _field("id", "text", required=True, description="Package-local work-card identifier."),
            _field("tenant", "text", required=True, description="Tenant or operator boundary."),
            _field("work_card_id", "text", required=True, description="Operational work-card identifier."),
            _field("aircraft_id", "text", description="Aircraft reference."),
            _field("aircraft_type", "text", required=True, description="Aircraft type for authorization matching."),
            _field("task_family", "text", required=True, description="Task family used in authorization checks."),
            _field("status", "text", description="Execution state."),
            _field("required_signoff_roles", "tuple[text]", description="Roles required before closeout."),
            _field("duplicate_inspection_required", "boolean", description="Whether duplicate inspection is required."),
            _field("signoffs", "tuple[json]", description="Technician signoff evidence."),
            _field("controlled_tools", "tuple[json]", description="Controlled tooling evidence."),
            _field("consumables", "tuple[json]", description="Consumable usage evidence."),
            _field("open_non_routine_count", "integer", description="Open linked non-routine work."),
            _field("payload", "json", description="Additional governed evidence."),
            _field("created_at", "datetime", description="Creation timestamp."),
            _field("updated_at", "datetime", description="Last update timestamp."),
        ),
    },
    {
        "entity": "maintenance_visit",
        "class_name": "MaintenanceVisitRecord",
        "table": f"{PBC_KEY}_maintenance_visit",
        "description": "Visit-level planning and release milestone state.",
        "required_fields": ("id", "tenant", "visit_id", "tail_number"),
        "status_values": ("planned", "active", "ready_for_release", "released"),
        "fields": (
            _field("id", "text", required=True, description="Package-local visit identifier."),
            _field("tenant", "text", required=True, description="Tenant or operator boundary."),
            _field("visit_id", "text", required=True, description="Maintenance visit identifier."),
            _field("tail_number", "text", required=True, description="Aircraft tail number."),
            _field("visit_type", "text", description="Line, overnight, or base visit type."),
            _field("status", "text", description="Visit lifecycle state."),
            _field("planned_release_at", "datetime", description="Planned return-to-service time."),
            _field("critical_path_cards", "tuple[text]", description="Critical-path work-card references."),
            _field("payload", "json", description="Additional governed evidence."),
            _field("created_at", "datetime", description="Creation timestamp."),
            _field("updated_at", "datetime", description="Last update timestamp."),
        ),
    },
    {
        "entity": "airworthiness_directive",
        "class_name": "AirworthinessDirectiveRecord",
        "table": f"{PBC_KEY}_airworthiness_directive",
        "description": "Applicability and compliance evidence for an AD.",
        "required_fields": ("id", "tenant", "ad_id", "status"),
        "status_values": ("open", "planned", "complied", "terminated", "not_applicable"),
        "fields": (
            _field("id", "text", required=True, description="Package-local AD identifier."),
            _field("tenant", "text", required=True, description="Tenant or operator boundary."),
            _field("ad_id", "text", required=True, description="Operational airworthiness directive identifier."),
            _field("status", "text", required=True, description="Compliance status."),
            _field("applicable", "boolean", description="Whether the AD applies to the release candidate."),
            _field("repeat_interval", "text", description="Repeat interval when applicable."),
            _field("compliance_method", "text", description="Compliance method."),
            _field("payload", "json", description="Additional governed evidence."),
            _field("created_at", "datetime", description="Creation timestamp."),
            _field("updated_at", "datetime", description="Last update timestamp."),
        ),
    },
    {
        "entity": "deferred_defect",
        "class_name": "DeferredDefectRecord",
        "table": f"{PBC_KEY}_deferred_defect",
        "description": "Deferred defect or MEL/CDL item with expiry evidence.",
        "required_fields": ("id", "tenant", "defect_id", "status"),
        "status_values": ("open", "deferred", "cleared", "closed"),
        "fields": (
            _field("id", "text", required=True, description="Package-local defect identifier."),
            _field("tenant", "text", required=True, description="Tenant or operator boundary."),
            _field("defect_id", "text", required=True, description="Operational defect identifier."),
            _field("status", "text", required=True, description="Defect lifecycle state."),
            _field("mel_category", "text", description="MEL/CDL deferment category."),
            _field("expiry_date", "date", description="Allowed expiry date."),
            _field("rectification_reference", "text", description="Closeout or rectification reference."),
            _field("payload", "json", description="Additional governed evidence."),
            _field("created_at", "datetime", description="Creation timestamp."),
            _field("updated_at", "datetime", description="Last update timestamp."),
        ),
    },
    {
        "entity": "compliance_release",
        "class_name": "ComplianceReleaseRecord",
        "table": f"{PBC_KEY}_compliance_release",
        "description": "Release-to-service assessment and evidence pack summary.",
        "required_fields": ("id", "tenant", "release_id", "tail_number", "status"),
        "status_values": ("draft", "blocked", "release_ready", "released"),
        "fields": (
            _field("id", "text", required=True, description="Package-local release record identifier."),
            _field("tenant", "text", required=True, description="Tenant or operator boundary."),
            _field("release_id", "text", required=True, description="Release assessment identifier."),
            _field("tail_number", "text", required=True, description="Aircraft tail number."),
            _field("status", "text", required=True, description="Release status."),
            _field("passed_checks", "tuple[text]", description="Completed release gates."),
            _field("pending_checks", "tuple[text]", description="Remaining release gates."),
            _field("blockers", "tuple[json]", description="Blocking evidence items."),
            _field("payload", "json", description="Additional governed evidence."),
            _field("created_at", "datetime", description="Creation timestamp."),
            _field("updated_at", "datetime", description="Last update timestamp."),
        ),
    },
)


SUPPORT_MODEL_DEFINITIONS = (
    {
        "entity": "policy_rule",
        "class_name": "PolicyRuleRecord",
        "table": f"{PBC_KEY}_{PBC_KEY}_policy_rule",
        "description": "Compiled policy or release rule.",
        "required_fields": ("id", "tenant", "rule_id"),
        "status_values": ("draft", "active", "retired"),
        "fields": (
            _field("id", "text", required=True, description="Policy identifier."),
            _field("tenant", "text", required=True, description="Tenant boundary."),
            _field("rule_id", "text", required=True, description="Rule identifier."),
            _field("status", "text", description="Rule status."),
            _field("compiled_hash", "text", description="Compiled rule hash."),
            _field("payload", "json", description="Rule metadata."),
        ),
    },
    {
        "entity": "runtime_parameter",
        "class_name": "RuntimeParameterRecord",
        "table": f"{PBC_KEY}_{PBC_KEY}_runtime_parameter",
        "description": "Bounded runtime parameter values.",
        "required_fields": ("id", "tenant", "name"),
        "status_values": ("active",),
        "fields": (
            _field("id", "text", required=True, description="Parameter identifier."),
            _field("tenant", "text", required=True, description="Tenant boundary."),
            _field("name", "text", required=True, description="Parameter name."),
            _field("value", "json", description="Parameter value."),
            _field("payload", "json", description="Parameter metadata."),
        ),
    },
    {
        "entity": "schema_extension",
        "class_name": "SchemaExtensionRecord",
        "table": f"{PBC_KEY}_{PBC_KEY}_schema_extension",
        "description": "Governed schema extension evidence.",
        "required_fields": ("id", "tenant", "table"),
        "status_values": ("draft", "active", "rejected"),
        "fields": (
            _field("id", "text", required=True, description="Schema extension identifier."),
            _field("tenant", "text", required=True, description="Tenant boundary."),
            _field("table", "text", required=True, description="Owned table being extended."),
            _field("fields", "json", description="Requested additional fields."),
            _field("payload", "json", description="Extension metadata."),
        ),
    },
    {
        "entity": "control_assertion",
        "class_name": "ControlAssertionRecord",
        "table": f"{PBC_KEY}_{PBC_KEY}_control_assertion",
        "description": "Continuous control test result.",
        "required_fields": ("id", "tenant", "assertion_id"),
        "status_values": ("pending", "passed", "failed"),
        "fields": (
            _field("id", "text", required=True, description="Assertion identifier."),
            _field("tenant", "text", required=True, description="Tenant boundary."),
            _field("assertion_id", "text", required=True, description="Assertion identifier."),
            _field("status", "text", description="Assertion status."),
            _field("payload", "json", description="Assertion evidence."),
        ),
    },
    {
        "entity": "governed_model",
        "class_name": "GovernedModelRecord",
        "table": f"{PBC_KEY}_{PBC_KEY}_governed_model",
        "description": "Governed AI model registration metadata.",
        "required_fields": ("id", "tenant", "model_id"),
        "status_values": ("candidate", "approved", "retired"),
        "fields": (
            _field("id", "text", required=True, description="Governed model identifier."),
            _field("tenant", "text", required=True, description="Tenant boundary."),
            _field("model_id", "text", required=True, description="Model identifier."),
            _field("status", "text", description="Model governance state."),
            _field("payload", "json", description="Model metadata."),
        ),
    },
    {
        "entity": "appgen_outbox_event",
        "class_name": "OutboxEventRecord",
        "table": f"{PBC_KEY}_appgen_outbox_event",
        "description": "Package-local AppGen-X outbox event.",
        "required_fields": ("id", "tenant", "event_type"),
        "status_values": ("pending", "published"),
        "fields": (
            _field("id", "text", required=True, description="Outbox event identifier."),
            _field("tenant", "text", required=True, description="Tenant boundary."),
            _field("event_type", "text", required=True, description="Event type."),
            _field("payload", "json", description="Event payload."),
            _field("status", "text", description="Dispatch state."),
        ),
    },
    {
        "entity": "appgen_inbox_event",
        "class_name": "InboxEventRecord",
        "table": f"{PBC_KEY}_appgen_inbox_event",
        "description": "Package-local AppGen-X inbox event.",
        "required_fields": ("id", "tenant", "event_type"),
        "status_values": ("received", "handled", "dead_lettered"),
        "fields": (
            _field("id", "text", required=True, description="Inbox event identifier."),
            _field("tenant", "text", required=True, description="Tenant boundary."),
            _field("event_type", "text", required=True, description="Event type."),
            _field("payload", "json", description="Event payload."),
            _field("status", "text", description="Handling state."),
        ),
    },
    {
        "entity": "appgen_dead_letter_event",
        "class_name": "DeadLetterEventRecord",
        "table": f"{PBC_KEY}_appgen_dead_letter_event",
        "description": "Package-local AppGen-X dead-letter event.",
        "required_fields": ("id", "tenant", "event_type"),
        "status_values": ("queued", "resolved"),
        "fields": (
            _field("id", "text", required=True, description="Dead-letter event identifier."),
            _field("tenant", "text", required=True, description="Tenant boundary."),
            _field("event_type", "text", required=True, description="Event type."),
            _field("payload", "json", description="Event payload."),
            _field("status", "text", description="Resolution state."),
        ),
    },
)


MODEL_DEFINITIONS = BUSINESS_MODEL_DEFINITIONS + SUPPORT_MODEL_DEFINITIONS
MODEL_BY_ENTITY = {model["entity"]: model for model in MODEL_DEFINITIONS}
MODEL_BY_TABLE = {model["table"]: model for model in MODEL_DEFINITIONS}
BUSINESS_TABLES = tuple(model["table"] for model in BUSINESS_MODEL_DEFINITIONS)
OWNED_TABLES = tuple(model["table"] for model in MODEL_DEFINITIONS)


def build_model_contracts() -> dict:
    models = []
    tables = []
    for model in MODEL_DEFINITIONS:
        field_names = tuple(field["name"] for field in model["fields"])
        models.append(
            {
                "class_name": model["class_name"],
                "entity": model["entity"],
                "table": model["table"],
                "description": model["description"],
                "required_fields": model["required_fields"],
                "status_values": model["status_values"],
                "fields": model["fields"],
            }
        )
        tables.append(
            {
                "table": model["table"],
                "entity": model["entity"],
                "description": model["description"],
                "fields": field_names,
                "field_specs": model["fields"],
                "primary_key": ("id",),
                "owned_by": PBC_KEY,
            }
        )
    return {
        "ok": True,
        "pbc": PBC_KEY,
        "models": tuple(models),
        "tables": tuple(tables),
        "business_tables": BUSINESS_TABLES,
        "owned_tables": OWNED_TABLES,
        "side_effects": (),
    }


def entity_blueprint(entity: str) -> dict:
    model = MODEL_BY_ENTITY.get(entity)
    if not model:
        return {"ok": False, "entity": entity, "reason": "unknown_entity", "side_effects": ()}
    return {
        "ok": True,
        "pbc": PBC_KEY,
        "entity": entity,
        "table": model["table"],
        "required_fields": model["required_fields"],
        "field_names": tuple(field["name"] for field in model["fields"]),
        "side_effects": (),
    }


def model_contracts():
    return build_model_contracts()["models"]
