from pyAppGen.pbcs.environment_health_safety.standalone import (
    build_detail_view,
    build_release_evidence,
    build_seed_plan,
    capture_inspection_sync,
    create_corrective_action,
    create_ehs_incident,
    handle_consumed_event,
    issue_permit,
    promote_near_miss_cluster,
    query_workbench,
    run_control_assertions,
    seed_state,
    send_serious_incident_notice,
    advance_incident_lifecycle,
    verify_corrective_action,
)


def test_incident_closure_gate_blocks_then_allows_closure():
    state = seed_state()
    result = create_ehs_incident(
        state,
        {
            "tenant": "tenant-x",
            "code": "INC-200",
            "site": "Plant 1",
            "area": "Mixer",
            "task": "Line clear",
            "severity": "hospitalization",
            "unsafe_condition": "unguarded coupling",
        },
    )
    state = result["state"]
    blocked = advance_incident_lifecycle(state, "INC-200", "closed", actor={"name": "Closer"})
    assert blocked["ok"] is False
    state = send_serious_incident_notice(state, "INC-200", {"name": "Approver"})["state"]
    state = advance_incident_lifecycle(state, "INC-200", "triaged", actor={"name": "Lead"})["state"]
    state = advance_incident_lifecycle(state, "INC-200", "recordability_review", actor={"name": "Lead"})["state"]
    state = advance_incident_lifecycle(state, "INC-200", "regulator_notified", actor={"name": "Lead"})["state"]
    state = advance_incident_lifecycle(
        state,
        "INC-200",
        "investigation_open",
        actor={"name": "Lead"},
        dossier_updates={
            "chronology": ("start", "event"),
            "witness_statements": ("w1",),
            "equipment_state": "stopped",
            "immediate_cause": "unguarded coupling",
            "basic_cause": "inspection gap",
            "root_cause": "maintenance drift",
            "failed_controls": ("guard",),
            "evidence_links": ("ehs://proof/inc-200",),
        },
    )["state"]
    state = create_corrective_action(
        state,
        {
            "tenant": "tenant-x",
            "code": "CA-200",
            "incident_id": "INC-200",
            "owner": "Maintenance",
            "due_date": "2026-06-10T00:00:00+00:00",
            "hierarchy_of_controls": "engineering",
            "verification_step": "install_guard",
        },
    )["state"]
    state = advance_incident_lifecycle(state, "INC-200", "corrective_action_open", actor={"name": "Lead"})["state"]
    state = verify_corrective_action(state, "CA-200", {"action_id": "CA-200", "passed": True, "evidence_links": ("ehs://proof/ca-200",)})["state"]
    closed = advance_incident_lifecycle(state, "INC-200", "closed", actor={"name": "Closer"})
    assert closed["ok"] is True


def test_near_miss_cluster_promotes_hazard_with_lineage():
    state = seed_state()
    promoted = promote_near_miss_cluster(
        state,
        {"tenant": "tenant-seed", "site": "Plant 7", "area": "Coating Line", "task": "Solvent changeover"},
    )
    assert promoted["ok"] is True
    assert promoted["hazard"]["lineage_incidents"]
    assert promoted["explanation"]["cluster_size"] >= promoted["explanation"]["threshold"]


def test_permit_conflict_and_offline_sync_are_idempotent():
    state = seed_state()
    conflict = issue_permit(
        state,
        {
            "tenant": "tenant-seed",
            "code": "PERM-101",
            "permit_type": "hot_work",
            "area": "Tank Farm",
            "start_at": "2026-06-01T10:00:00+00:00",
            "end_at": "2026-06-01T11:00:00+00:00",
            "energy_source": "open_flame",
        },
    )
    assert conflict["ok"] is False
    synced = capture_inspection_sync(
        state,
        {
            "submission_id": "sync-1",
            "tenant": "tenant-seed",
            "template": "weekly-round",
            "area": "Tank Farm",
            "captured_at": "2026-06-01T09:00:00+00:00",
            "inspector": "Inspector A",
            "answers": {"housekeeping": "pass"},
        },
    )
    duplicate = capture_inspection_sync(synced["state"], {"submission_id": "sync-1", "tenant": "tenant-seed"})
    assert synced["ok"] is True
    assert duplicate["duplicate"] is True


def test_consumed_events_are_domain_specific_and_idempotent():
    state = seed_state()
    policy = handle_consumed_event(state, {"event_type": "PolicyChanged", "idempotency_key": "policy-1", "payload": {"policy_version": "ehs-policy-2026.9"}})
    duplicate = handle_consumed_event(policy["state"], {"event_type": "PolicyChanged", "idempotency_key": "policy-1", "payload": {"policy_version": "ehs-policy-2026.9"}})
    sealed = handle_consumed_event(policy["state"], {"event_type": "AuditEventSealed", "idempotency_key": "seal-1", "payload": {"bundle_id": "bundle-1", "record_ids": ("INC-100",)}})
    kpi = handle_consumed_event(policy["state"], {"event_type": "OperationalKpiChanged", "idempotency_key": "kpi-1", "payload": {"site": "Plant 7", "drivers": {"minor_injuries": 3}}})
    assert policy["ok"] is True
    assert duplicate["duplicate"] is True
    assert sealed["state"]["sealed_bundles"]["bundle-1"]["status"] == "sealed"
    assert kpi["emitted_event"]["event_type"] == "EnvironmentHealthSafetyRiskPriorityRecalculated"


def test_workbench_detail_release_and_control_assertions_expose_domain_depth():
    state = seed_state()
    overdue = create_ehs_incident(
        state,
        {
            "tenant": "tenant-y",
            "code": "INC-OVERDUE",
            "site": "Plant Y",
            "area": "Warehouse",
            "task": "Transfer",
            "severity": "fatality",
            "unsafe_condition": "vehicle strike",
            "occurred_at": "2026-05-29T00:00:00+00:00",
        },
    )["state"]
    assertions = run_control_assertions(overdue, reference_time="2026-05-31T00:00:00+00:00")
    workbench = query_workbench(assertions["state"], {"tenant": "tenant-seed"})
    detail = build_detail_view(seed_state(), "INC-100")
    release = build_release_evidence()
    seed = build_seed_plan()
    assert assertions["assertions"]
    assert workbench["queues"]["incident_cards"]
    assert detail["ok"] is True and detail["causal_chain"][0]
    assert release["ok"] is True
    assert seed["ok"] is True
