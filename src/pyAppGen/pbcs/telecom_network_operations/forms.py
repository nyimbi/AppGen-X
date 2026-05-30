"""Domain forms for the Telecom Network Operations standalone PBC."""
PBC_KEY = "telecom_network_operations"

def _field(name, kind="text", required=True, **extra):
    return {"name": name, "type": kind, "required": required, **extra}

FORMS = (
    {"key":"site_hierarchy","title":"Canonical site hierarchy","owned_table":"telecom_network_operations_network_element","fields":(_field("site_code"),_field("latitude","number"),_field("longitude","number"),_field("site_type"),_field("access_restrictions",required=False),_field("power_context","json",required=False))},
    {"key":"radio_cell_sector","title":"Cell, sector, carrier, and radio identity","owned_table":"telecom_network_operations_network_element","fields":(_field("site_id"),_field("technology","select",options=("2G","3G","4G","5G")),_field("sector"),_field("carrier"),_field("band"),_field("pci_or_psc"),_field("azimuth","number"),_field("tilt","number"))},
    {"key":"circuit_service_path","title":"Circuit and service path topology","owned_table":"telecom_network_operations_capacity_segment","fields":(_field("circuit_id"),_field("a_end"),_field("z_end"),_field("transport_type"),_field("protected","boolean"),_field("route_membership","json"),_field("service_class"))},
    {"key":"fiber_route_strand","title":"Fiber route, strand, and splice ownership","owned_table":"telecom_network_operations_capacity_segment","fields":(_field("route_code"),_field("cable"),_field("tube"),_field("strand"),_field("closure"),_field("route_diverse","boolean"),_field("otdr_trace_digest",required=False))},
    {"key":"alarm_normalization","title":"Alarm catalog normalization","owned_table":"telecom_network_operations_alarm_event","fields":(_field("raw_vendor_code"),_field("vendor"),_field("normalized_family"),_field("severity"),_field("probable_cause"),_field("object_class"),_field("clear_condition",required=False))},
    {"key":"outage_war_room","title":"Outage lifecycle and war room","owned_table":"telecom_network_operations_network_incident","fields":(_field("incident_id"),_field("state"),_field("bridge_commander"),_field("restoration_eta",required=False),_field("impacted_services","json"),_field("customer_update_due",required=False))},
    {"key":"planned_work","title":"Planned work and maintenance window","owned_table":"telecom_network_operations_maintenance_window","fields":(_field("window_id"),_field("mop_version"),_field("rollback_plan"),_field("change_owner"),_field("freeze_window","boolean"),_field("scope","json"),_field("expected_impact"))},
    {"key":"sla_clock","title":"SLA impact clock","owned_table":"telecom_network_operations_sla_impact","fields":(_field("case_id"),_field("service_class"),_field("clock_state"),_field("started_at"),_field("paused_reason",required=False),_field("exclusion_approved","boolean",required=False),_field("breach_forecast",required=False))},
    {"key":"capacity_kpi","title":"Capacity and KPI baseline","owned_table":"telecom_network_operations_capacity_segment","fields":(_field("segment_id"),_field("capacity_class"),_field("installed","number"),_field("reserved","number"),_field("used","number"),_field("forecast","number"),_field("threshold","number"))},
    {"key":"service_assurance_case","title":"Trouble ticket and next action","owned_table":"telecom_network_operations_service_assurance_case","fields":(_field("case_id"),_field("incident_id",required=False),_field("severity"),_field("customer_impact"),_field("dispatch_status"),_field("next_action"),_field("external_reference",required=False))},
    {"key":"field_evidence","title":"Field evidence capture","owned_table":"telecom_network_operations_service_assurance_case","fields":(_field("case_id"),_field("photo_digest",required=False),_field("meter_reading",required=False),_field("replaced_part",required=False),_field("splice_validation",required=False),_field("closure_note"))},
)

def form_catalog(): return {"ok": True, "pbc": PBC_KEY, "forms": FORMS, "side_effects": ()}
def form_for(key):
    for form in FORMS:
        if form["key"] == key: return {"ok": True, "form": form, "side_effects": ()}
    return {"ok": False, "reason": "unknown_form", "key": key, "side_effects": ()}
def smoke_test(): return {"ok": len(FORMS) >= 11 and all(f["owned_table"].startswith(f"{PBC_KEY}_") for f in FORMS), "side_effects": ()}
