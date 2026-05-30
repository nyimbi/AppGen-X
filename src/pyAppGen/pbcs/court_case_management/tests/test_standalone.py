from pyAppGen.pbcs.court_case_management.audit import run_court_case_management_pbc_audit
from pyAppGen.pbcs.court_case_management.routes import dispatch_standalone_route
from pyAppGen.pbcs.court_case_management.services import CourtCaseManagementStandaloneService
from pyAppGen.pbcs.court_case_management.standalone import build_standalone_app, documentation_presence, pbc_generation_smoke_audit, pbc_implementation_release_audit, standalone_smoke_test


def test_standalone_case_journey_runs_end_to_end():
    app = build_standalone_app(tenant='tenant-alpha')
    app.configure()
    app.register_defaults()
    created = app.create_court_case(
        {
            'court': 'CIV',
            'division': 'LAW',
            'filing_year': 2026,
            'case_type': 'civil',
            'caption': 'Roe v. Example',
            'assigned_judge': 'Judge Lane',
        }
    )
    app.add_party({'case_id': created['court_case']['id'], 'party_name': 'Jane Roe', 'role': 'plaintiff', 'lead_counsel': 'A. Counsel'})
    filing = app.receive_filing(
        {
            'case_id': created['court_case']['id'],
            'filing_type': 'motion',
            'document_title': 'Motion to Compel',
            'received_at': '2026-01-02',
            'deficiency_codes': ('missing_signature',),
            'cure_deadline': '2026-01-09',
        }
    )
    app.cure_filing(filing['filing']['id'], {'defects_cured': True, 'evidence': 'signed'})
    evidence = app.register_evidence({'case_id': created['court_case']['id'], 'description': 'Exhibit A', 'submitted_by': 'Jane Roe', 'submitted_at': '2026-01-03'})
    hearing = app.schedule_hearing(
        {
            'case_id': created['court_case']['id'],
            'hearing_type': 'motion',
            'scheduled_at': '2026-01-20T09:00:00',
            'courtroom': '4A',
            'session_block': 'AM',
            'assigned_judge': 'Judge Lane',
        }
    )
    task = app.create_task({'case_id': created['court_case']['id'], 'title': 'Serve order', 'task_type': 'service', 'assignee': 'clerk.one'})
    completed = app.complete_task(task['task']['id'], {'completed_by': 'clerk.one', 'completion_notes': 'Served.'})
    order = app.draft_order({'case_id': created['court_case']['id'], 'title': 'Scheduling Order', 'draft_text': 'Set deadlines.'})
    entered = app.sign_and_enter_order(order['court_order']['id'], {'judge_signature': 'Judge Lane', 'signed_at': '2026-01-03'})
    detail = app.query_case_detail(created['court_case']['id'], permissions=('court_case_management.admin',))
    workbench = app.query_workbench(permissions=('court_case_management.admin',))

    assert evidence['ok'] is True
    assert hearing['ok'] is True
    assert completed['ok'] is True
    assert entered['ok'] is True
    assert detail['counts']['evidence_items'] == 1
    assert workbench['queue_counts']['open_cases'] == 1


def test_standalone_service_and_routes_are_executable():
    service = CourtCaseManagementStandaloneService(tenant='tenant-beta')
    service.configure()
    service.register_defaults()
    dispatch = dispatch_standalone_route(
        'POST',
        '/court-cases',
        {
            'court': 'CIV',
            'division': 'LAW',
            'filing_year': 2026,
            'case_type': 'civil',
            'caption': 'Smith v. Example',
        },
        app=service.app,
    )
    workbench = dispatch_standalone_route('GET', '/court-case-management-workbench', {'permissions': ('court_case_management.admin',)}, app=service.app)
    assert dispatch['ok'] is True
    assert workbench['ok'] is True


def test_standalone_smoke_docs_and_audits_are_green():
    assert standalone_smoke_test()['ok'] is True
    assert documentation_presence()['ok'] is True
    assert pbc_implementation_release_audit()['ok'] is True
    assert pbc_generation_smoke_audit()['ok'] is True
    assert run_court_case_management_pbc_audit()['ok'] is True
