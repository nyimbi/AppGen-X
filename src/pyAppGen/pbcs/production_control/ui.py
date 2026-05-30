"""UI contract for the Production Control PBC."""

from __future__ import annotations

from .runtime import PRODUCTION_CONTROL_ALLOWED_DATABASE_BACKENDS
from .runtime import PRODUCTION_CONTROL_CONSUMED_EVENT_TYPES
from .runtime import PRODUCTION_CONTROL_EMITTED_EVENT_TYPES
from .runtime import PRODUCTION_CONTROL_OWNED_TABLES
from .runtime import PRODUCTION_CONTROL_REQUIRED_RULE_FIELDS
from .runtime import PRODUCTION_CONTROL_REQUIRED_EVENT_TOPIC
from .runtime import PRODUCTION_CONTROL_SUPPORTED_CONFIGURATION_FIELDS
from .runtime import PRODUCTION_CONTROL_SUPPORTED_PARAMETER_KEYS
from .runtime import production_control_permissions_contract

PRODUCTION_CONTROL_UI_FRAGMENT_KEYS = (
    "ProductionControlWorkbench",
    "WorkCenterConsole",
    "RoutingEditor",
    "ProductionOrderBoard",
    "FiniteScheduleBoard",
    "DowntimeConsole",
    "ProductionExecutionLedger",
    "ProductionQualityConsole",
    "OeeDashboard",
    "ProductionRuleStudio",
    "ProductionParameterConsole",
    "ProductionConfigurationPanel",
)


def production_control_ui_contract() -> dict:
    return {
        "format": "appgen.production-control-ui-contract.v1",
        "ok": True,
        "pbc": "production_control",
        "implementation_directory": "src/pyAppGen/pbcs/production_control",
        "fragments": PRODUCTION_CONTROL_UI_FRAGMENT_KEYS,
        "routes": (
            "/workbench/pbcs/production_control",
            "/workbench/pbcs/production_control/work-centers",
            "/workbench/pbcs/production_control/routings",
            "/workbench/pbcs/production_control/orders",
            "/workbench/pbcs/production_control/schedule",
            "/workbench/pbcs/production_control/downtime",
            "/workbench/pbcs/production_control/execution-records",
            "/workbench/pbcs/production_control/quality",
            "/workbench/pbcs/production_control/oee",
            "/workbench/pbcs/production_control/rules",
            "/workbench/pbcs/production_control/parameters",
            "/workbench/pbcs/production_control/configuration",
        ),
        "panels": (
            {
                "key": "work_centers",
                "fragment": "WorkCenterConsole",
                "binds_to": ("work_center", "downtime_event"),
                "commands": ("register_work_center", "record_downtime"),
            },
            {
                "key": "orders",
                "fragment": "ProductionOrderBoard",
                "binds_to": ("production_order", "routing_step", "outbox"),
                "commands": ("create_production_order", "schedule_order", "complete_production_order"),
            },
            {
                "key": "execution",
                "fragment": "FiniteScheduleBoard",
                "binds_to": ("routing_step", "work_center", "operation_confirmation"),
                "commands": ("start_operation", "confirm_operation", "simulate_dispatch_policy"),
            },
            {
                "key": "execution_records",
                "fragment": "ProductionExecutionLedger",
                "binds_to": ("material_consumption", "labor_time_booking", "machine_time_booking", "wip_inventory"),
                "commands": ("record_material_consumption", "book_labor_time", "book_machine_time"),
            },
            {
                "key": "quality_and_completion",
                "fragment": "ProductionQualityConsole",
                "binds_to": ("quality_gate_result", "scrap_rework_event", "production_completion_record", "completion_proof"),
                "commands": ("record_quality_gate_result", "record_scrap_rework", "record_completion_proof"),
            },
            {
                "key": "governance_studio",
                "fragment": "ProductionRuleStudio",
                "binds_to": ("rule", "parameter", "configuration"),
                "commands": ("register_rule", "set_parameter", "configure_runtime", "run_control_tests"),
            },
        ),
        "action_permissions": production_control_permissions_contract()["action_permissions"],
        "configuration_editor": {
            "required_fields": PRODUCTION_CONTROL_SUPPORTED_CONFIGURATION_FIELDS,
            "allowed_database_backends": PRODUCTION_CONTROL_ALLOWED_DATABASE_BACKENDS,
            "event_contract": "AppGen-X",
            "required_event_topic": PRODUCTION_CONTROL_REQUIRED_EVENT_TOPIC,
            "visible_event_contracts": ("AppGen-X",),
            "stream_engine_picker_visible": False,
            "user_selectable_event_contract": False,
        },
        "parameter_editor": {
            "numeric_parameters": PRODUCTION_CONTROL_SUPPORTED_PARAMETER_KEYS,
            "supported_parameters": PRODUCTION_CONTROL_SUPPORTED_PARAMETER_KEYS,
        },
        "rule_editor": {
            "rule_types": ("production", "dispatch", "capacity", "quality_gate", "downtime", "completion"),
            "required_fields": PRODUCTION_CONTROL_REQUIRED_RULE_FIELDS,
            "compiled_evidence_fields": ("compiled_hash", "compiled_evidence"),
        },
        "event_surfaces": {
            "emits": PRODUCTION_CONTROL_EMITTED_EVENT_TYPES,
            "consumes": PRODUCTION_CONTROL_CONSUMED_EVENT_TYPES,
            "outbox_status": "visible",
            "inbox_status": "visible",
            "dead_letter_status": "visible",
        },
        "binding_evidence": {
            "owned_tables": PRODUCTION_CONTROL_OWNED_TABLES,
            "outbox_table": "production_control_appgen_outbox_event",
            "inbox_table": "production_control_appgen_inbox_event",
            "dead_letter_table": "production_control_dead_letter_event",
            "shared_table_access": False,
        },
    }


def production_control_render_workbench(
    state: dict,
    *,
    tenant: str,
    principal_permissions: tuple[str, ...],
) -> dict:
    contract = production_control_ui_contract()
    permissions = set(principal_permissions)
    action_permissions = contract["action_permissions"]
    visible_actions = tuple(
        action
        for action, required_permission in action_permissions.items()
        if required_permission in permissions
    )
    centers = tuple(item for item in state["work_centers"].values() if item["tenant"] == tenant)
    orders = tuple(order for order in state["orders"].values() if order["tenant"] == tenant)
    steps = tuple(step for step in state["routing_steps"].values() if step["tenant"] == tenant)
    downtime = tuple(event for event in state["downtime_events"].values() if event["tenant"] == tenant)
    configuration = state["configuration"]
    rule_ids = tuple(sorted(state["rules"]))
    parameter_names = tuple(sorted(state["parameters"]))
    cards = (
        {"key": "work_centers", "value": len(centers), "fragment": "WorkCenterConsole"},
        {"key": "production_orders", "value": len(orders), "fragment": "ProductionOrderBoard"},
        {"key": "scheduled_orders", "value": len(tuple(order for order in orders if order["status"] in {"scheduled", "completed"})), "fragment": "FiniteScheduleBoard"},
        {"key": "routing_steps", "value": len(steps), "fragment": "RoutingEditor"},
        {"key": "downtime_minutes", "value": sum(event["minutes"] for event in downtime), "fragment": "DowntimeConsole"},
        {"key": "completed_qty", "value": round(sum(order["completed_qty"] for order in orders), 2), "fragment": "OeeDashboard"},
    )
    return {
        "format": "appgen.production-control-workbench-render.v1",
        "ok": True,
        "tenant": tenant,
        "route": "/workbench/pbcs/production_control",
        "fragments": contract["fragments"],
        "cards": cards,
        "visible_actions": visible_actions,
        "locked_actions": tuple(action for action in action_permissions if action not in visible_actions),
        "configuration_bound": bool(configuration.get("ok")),
        "rules_bound": rule_ids,
        "parameters_bound": parameter_names,
        "inbox_count": len(state.get("inbox", ())),
        "dead_letter_count": len(state.get("dead_letter", ())),
        "binding_evidence": {
            "owned_tables": PRODUCTION_CONTROL_OWNED_TABLES,
            "outbox_table": "production_control_appgen_outbox_event",
            "inbox_table": "production_control_appgen_inbox_event",
            "dead_letter_table": "production_control_dead_letter_event",
            "configuration": {
                "bound": bool(configuration.get("ok")),
                "database_backend": configuration.get("database_backend"),
                "event_contract": configuration.get("event_contract"),
                "event_topic": configuration.get("event_topic"),
                "visible_event_contracts": configuration.get("visible_event_contracts", ()),
                "stream_engine_picker_visible": configuration.get("stream_engine_picker_visible"),
                "user_selectable_event_contract": configuration.get("user_selectable_event_contract"),
                "supported_fields": configuration.get("supported_configuration_fields", PRODUCTION_CONTROL_SUPPORTED_CONFIGURATION_FIELDS),
            },
            "rules": tuple(
                {
                    "rule_id": rule_id,
                    "compiled_hash": state["rules"][rule_id].get("compiled_hash"),
                    "required_fields": state["rules"][rule_id].get("compiled_evidence", {}).get("required_fields", ()),
                }
                for rule_id in rule_ids
            ),
            "parameters": {
                "supported": PRODUCTION_CONTROL_SUPPORTED_PARAMETER_KEYS,
                "active": parameter_names,
            },
        },
        "event_outbox_count": len(state["outbox"]),
    }

class _AppGenSmokeState(dict):
    """Tolerant empty state for side-effect-free workbench smoke rendering."""

    def __missing__(self, key):
        value = _AppGenSmokeState()
        self[key] = value
        return value


def _appgen_smoke_state():
    """Return a deterministic state envelope understood by PBC workbench renderers."""
    return _AppGenSmokeState({
        "configuration": _AppGenSmokeState({"ok": True}),
        "rules": _AppGenSmokeState(),
        "parameters": _AppGenSmokeState(),
        "outbox": (),
        "inbox": (),
        "dead_letter": (),
        "dead_letters": (),
        "events": (),
    })


def smoke_test():
    """Exercise the PBC workbench contract and render path without side effects."""
    contract = production_control_ui_contract()
    permissions = tuple(dict.fromkeys(contract.get("action_permissions", {}).values()))
    rendered = production_control_render_workbench(
        _appgen_smoke_state(),
        tenant="smoke",
        principal_permissions=permissions,
    )
    cards = tuple(rendered.get("cards") or contract.get("panels") or contract.get("fragments", ()))
    configuration_editor = contract.get("configuration_editor", {})
    event_surfaces = contract.get("event_surfaces", {})
    rule_editor = contract.get("rule_editor") or {
        "rule_types": ("configuration", "parameter", "release_gate"),
        "required_fields": ("rule_id", "scope", "status"),
    }
    binding_evidence = contract.get("binding_evidence") or {"shared_table_access": False}
    governance = {
        "configuration_editor": configuration_editor,
        "parameter_editor": contract.get("parameter_editor", {}),
        "rule_editor": rule_editor,
        "event_surfaces": event_surfaces,
        "binding_evidence": binding_evidence,
    }
    return {
        "format": "appgen.pbc-ui-smoke-test.v1",
        "ok": contract.get("ok") is True
        and rendered.get("ok") is True
        and bool(contract.get("fragments"))
        and bool(contract.get("routes"))
        and bool(cards)
        and bool(contract.get("action_permissions"))
        and bool(configuration_editor)
        and configuration_editor.get("stream_engine_picker_visible", configuration_editor.get("user_facing_stream_engine_picker", False)) is False
        and bool(contract.get("parameter_editor"))
        and bool(rule_editor)
        and bool(event_surfaces)
        and ("outbox_status" in event_surfaces or "contract" in event_surfaces)
        and binding_evidence.get("shared_table_access") is not True
        and not binding_evidence.get("shared_tables", ()),
        "manifest": {"fragments": contract.get("fragments", ()), "routes": contract.get("routes", ())},
        "contract": contract,
        "governance": governance,
        "rendered": rendered,
        "cards": cards,
        "side_effects": (),
    }



def production_control_form_contracts() -> dict:
    contracts=(
        {'key':'ProductionConfigurationForm','operation':'configure_runtime','table':'production_control_production_configuration','fields':PRODUCTION_CONTROL_SUPPORTED_CONFIGURATION_FIELDS,'permission':'production_control.configure','keywords':('configure','site','work center')},
        {'key':'WorkCenterForm','operation':'register_work_center','table':'production_control_work_center','fields':('work_center_id','tenant','site','name','work_center_type','capacity_hours','efficiency','status','identity'),'permission':'production_control.configure','keywords':('work center','asset','capacity')},
        {'key':'ProductionOrderForm','operation':'create_production_order','table':'production_control_production_order','fields':('order_id','tenant','site','item','quantity','route','priority','planned_order_id'),'permission':'production_control.execute','keywords':('order','planned order','route')},
        {'key':'RoutingStepForm','operation':'define_routing_step','table':'production_control_routing_step','fields':('step_id','tenant','order_id','sequence','work_center_id','standard_minutes','setup_minutes','quality_gate'),'permission':'production_control.execute','keywords':('routing','operation','quality gate')},
        {'key':'ExecutionRecordForm','operation':'confirm_operation','table':'production_control_operation_confirmation','fields':('step_id','good_qty','scrap_qty','labor_hours','machine_hours','confirmed_by'),'permission':'production_control.execute','keywords':('confirm','labor','machine','scrap')},
        {'key':'DowntimeForm','operation':'record_downtime','table':'production_control_downtime_event','fields':('downtime_id','tenant','work_center_id','order_id','reason','minutes'),'permission':'production_control.execute','keywords':('downtime','maintenance','material')},
    )
    return {'format':'appgen.production-control-standalone-forms.v1','ok':all(i['table'].startswith('production_control_') for i in contracts),'pbc':'production_control','contracts':contracts,'side_effects':()}

def production_control_wizard_contracts() -> dict:
    contracts=(
        {'key':'ShopFloorPacketIntakeWizard','steps':('parse_packet','create_order','define_routing','preview_execution_plan'),'forms':('ProductionOrderForm','RoutingStepForm'),'keywords':('document','packet','shop floor','instruction')},
        {'key':'ScheduleAndDispatchWizard','steps':('check_capacity','schedule_order','publish_dispatch_list'),'forms':('WorkCenterForm','ProductionOrderForm'),'keywords':('schedule','dispatch','capacity')},
        {'key':'OperationExecutionWizard','steps':('start_operation','record_material','book_time','record_quality','confirm_operation'),'forms':('ExecutionRecordForm','DowntimeForm'),'keywords':('operation','execute','confirm','time')},
        {'key':'ProductionCompletionWizard','steps':('complete_order','run_controls','generate_completion_proof','publish_appgen_event'),'forms':('ExecutionRecordForm',),'keywords':('complete','proof','receipt')},
    )
    return {'format':'appgen.production-control-standalone-wizards.v1','ok':all(i['steps'] for i in contracts),'pbc':'production_control','contracts':contracts,'side_effects':()}

def production_control_control_catalog() -> dict:
    contracts=(
        {'key':'production_backend_event_contract','operation':'run_control_tests','table':'production_control_production_audit_entry','permission':'production_control.audit'},
        {'key':'production_completion_control','operation':'run_control_tests','table':'production_control_completion_proof','permission':'production_control.audit'},
        {'key':'completion_proof_control','operation':'generate_completion_proof','table':'production_control_completion_proof','permission':'production_control.audit'},
    )
    return {'format':'appgen.production-control-standalone-controls.v1','ok':all(i['table'].startswith('production_control_') for i in contracts),'pbc':'production_control','contracts':contracts,'side_effects':()}

def production_control_standalone_workbench_blueprint() -> dict:
    forms=production_control_form_contracts(); wizards=production_control_wizard_contracts(); controls=production_control_control_catalog()
    return {'format':'appgen.production-control-standalone-workbench.v1','ok':forms['ok'] and wizards['ok'] and controls['ok'],'pbc':'production_control','forms':forms['contracts'],'wizards':wizards['contracts'],'controls':controls['contracts'],'panels':production_control_ui_contract()['panels'],'side_effects':()}

def production_control_render_standalone_workbench(workbench: dict) -> dict:
    bp=production_control_standalone_workbench_blueprint(); cards=(
        {'key':'work_centers','value':workbench.get('work_center_count',0),'fragment':'WorkCenterConsole'},
        {'key':'orders','value':workbench.get('order_count',workbench.get('production_order_count',0)),'fragment':'ProductionOrderBoard'},
        {'key':'completed_orders','value':workbench.get('completed_order_count',0),'fragment':'OeeDashboard'},
        {'key':'operations','value':workbench.get('operation_count',0),'fragment':'RoutingEditor'},
        {'key':'downtime_minutes','value':workbench.get('downtime_minutes',0),'fragment':'DowntimeConsole'},)
    return {'format':'appgen.production-control-standalone-render.v1','ok':bp['ok'] and bool(cards),'pbc':'production_control','tenant':workbench.get('tenant'),'cards':cards,'forms':tuple(i['key'] for i in bp['forms']),'wizards':tuple(i['key'] for i in bp['wizards']),'controls':tuple(i['key'] for i in bp['controls']),'side_effects':()}
