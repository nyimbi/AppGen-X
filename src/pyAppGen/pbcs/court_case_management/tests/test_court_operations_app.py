from pyAppGen.pbcs.court_case_management.agent import document_instruction_plan
from pyAppGen.pbcs.court_case_management.audit import run_court_case_management_pbc_audit
from pyAppGen.pbcs.court_case_management.court_operations_app import (
    add_docket_entry,
    case_detail,
    complete_task,
    controls_contract,
    court_operations_smoke_test,
    court_workbench,
    create_court_case,
    create_task,
    cure_filing,
    document_instruction_mutation_plan,
    draft_order,
    empty_court_state,
    forms_contract,
    receive_filing,
    register_evidence,
    schedule_hearing,
    sign_and_enter_order,
    single_pbc_app_contract,
    wizards_contract,
)
from pyAppGen.pbcs.court_case_management.routes import dispatch_route, dispatch_standalone_route
from pyAppGen.pbcs.court_case_management.services import CourtCaseManagementService, CourtCaseManagementStandaloneService
from pyAppGen.pbcs.court_case_management.ui import court_case_management_ui_contract


def _case_payload(**overrides):
    payload = {
        'court': 'CIV',
        'division': 'LAW',
        'filing_year': 2026,
        'case_type': 'civil',
        'caption': 'Roe v. Example',
        'assigned_judge': 'Judge Lane',
    }
    payload.update(overrides)
    return payload


def test_case_numbering_is_unique_and_preserves_venue():
    created = create_court_case(empty_court_state(), _case_payload())
    assert created['ok'] is True
    assert created['court_case']['case_number'] == 'CIV-LAW-2026-000001'
    duplicate = create_court_case(created['state'], _case_payload(sequence=1))
    assert duplicate['ok'] is False
    assert duplicate['reason'] == 'duplicate_case_number'


def test_filing_deficiency_flow_creates_review_task_and_docket_after_cure():
    created = create_court_case(empty_court_state(), _case_payload())
    filing = receive_filing(
        created['state'],
        {
            'case_id': created['court_case']['id'],
            'filing_type': 'motion',
            'document_title': 'Motion to Compel',
            'received_at': '2026-01-02',
            'deficiency_codes': ('missing_signature',),
            'cure_deadline': '2026-01-09',
        },
    )
    assert filing['filing']['state'] == 'deficient'
    assert filing['task']['queue'] == 'clerk_intake'
    cured = cure_filing(filing['state'], filing['filing']['id'], {'defects_cured': True, 'evidence': 'signed'})
    assert cured['filing']['state'] == 'accepted'
    assert cured['docket_entry']['source_type'] == 'filing'


def test_evidence_intake_updates_detail_timeline_and_creates_review_task():
    created = create_court_case(empty_court_state(), _case_payload())
    evidence = register_evidence(
        created['state'],
        {
            'case_id': created['court_case']['id'],
            'description': 'Exhibit A',
            'submitted_by': 'Jane Roe',
            'submitted_at': '2026-01-03',
        },
    )
    detail = case_detail(evidence['state'], created['court_case']['id'], permissions=('court_case_management.admin',))
    assert evidence['evidence_item']['exhibit_number'] == 'EX-001'
    assert evidence['task']['task_type'] == 'evidence_review'
    assert any(item['entity_type'] == 'evidence_item' for item in detail['timeline'])


def test_docket_sequence_hearing_calendar_and_order_controls_block_bad_operations():
    created = create_court_case(empty_court_state(), _case_payload())
    bad_sequence = add_docket_entry(created['state'], {'case_id': created['court_case']['id'], 'sequence': 3, 'entry_text': 'bad'})
    assert bad_sequence['ok'] is False
    assert bad_sequence['reason'] == 'docket_sequence_gap'

    hearing = schedule_hearing(
        created['state'],
        {
            'case_id': created['court_case']['id'],
            'hearing_type': 'motion',
            'scheduled_at': '2026-01-20T09:00:00',
            'courtroom': '4A',
            'session_block': 'AM',
            'assigned_judge': 'Judge Lane',
        },
    )
    conflict = schedule_hearing(
        hearing['state'],
        {
            'case_id': created['court_case']['id'],
            'hearing_type': 'status',
            'scheduled_at': '2026-01-20T09:00:00',
            'courtroom': '4A',
            'session_block': 'AM',
            'assigned_judge': 'Judge Lane',
        },
    )
    assert conflict['ok'] is False
    assert conflict['reason'] == 'courtroom_double_booked'

    order = draft_order(created['state'], {'case_id': created['court_case']['id'], 'title': 'Scheduling Order', 'draft_text': 'Set deadlines.'})
    blocked = sign_and_enter_order(order['state'], order['court_order']['id'], {'signed_at': '2026-01-03'})
    assert blocked['ok'] is False
    assert blocked['reason'] == 'signature_required'


def test_task_completion_workbench_and_assistant_contracts_are_executable():
    created = create_court_case(empty_court_state(), _case_payload())
    task = create_task(
        created['state'],
        {
            'case_id': created['court_case']['id'],
            'title': 'Serve order',
            'task_type': 'service',
            'assignee': 'clerk.one',
        },
    )
    done = complete_task(task['state'], task['task']['id'], {'completed_by': 'clerk.one', 'completion_notes': 'Served all parties.'})
    workbench = court_workbench(done['state'], permissions=('court_case_management.admin',))
    plan = document_instruction_plan('Exhibit packet', 'log evidence')
    mutation = document_instruction_mutation_plan('follow up on service', 'create task')
    assert done['task']['status'] == 'completed'
    assert workbench['queue_counts']['pending_tasks'] == 0
    assert plan['domain_plan']['proposed_action'] == 'register_evidence'
    assert mutation['proposed_action'] == 'create_task'


def test_single_pbc_app_services_routes_ui_and_audit_are_executable():
    app = single_pbc_app_contract()
    assert app['ok'] is True
    assert len(app['forms']) >= 7
    assert len(app['wizards']) >= 6
    assert len(app['controls']) >= 8

    service = CourtCaseManagementService()
    created = service.create_court_case(_case_payload())
    assert created['ok'] is True
    assert service.query_workbench({'permissions': ('court_case_management.admin',)})['queue_counts']['open_cases'] == 1
    assert dispatch_route('POST /court-cases', _case_payload())['operation'] == 'create_court_case'
    assert court_case_management_ui_contract()['single_pbc_app']['single_pbc_app'] is True
    assert run_court_case_management_pbc_audit()['ok'] is True

    standalone = CourtCaseManagementStandaloneService(tenant='tenant-alpha')
    standalone.configure()
    standalone.register_defaults()
    routed = dispatch_standalone_route('GET', '/court-case-management-workbench', {'permissions': ('court_case_management.admin',)}, app=standalone.app)
    assert routed['ok'] is True


def test_release_smoke_contracts_are_green():
    assert forms_contract()['ok'] is True
    assert wizards_contract()['ok'] is True
    assert controls_contract()['ok'] is True
    assert court_operations_smoke_test()['ok'] is True
