"""Standalone one-PBC application surface for humanitarian_relief_operations."""
from __future__ import annotations
from dataclasses import dataclass, field
from hashlib import sha256
from typing import Any
from .agent import chatbot_interface_contract, composed_agent_contribution, datastore_crud_plan, document_instruction_plan
from .controls import control_catalog, evaluate_control
from .forms import form_catalog
from .runtime import (
    HUMANITARIAN_RELIEF_OPERATIONS_ALLOWED_DATABASE_BACKENDS,
    HUMANITARIAN_RELIEF_OPERATIONS_CONSUMED_EVENT_TYPES,
    HUMANITARIAN_RELIEF_OPERATIONS_OWNED_TABLES,
    HUMANITARIAN_RELIEF_OPERATIONS_REQUIRED_EVENT_TOPIC,
    humanitarian_relief_operations_build_api_contract,
    humanitarian_relief_operations_build_schema_contract,
    humanitarian_relief_operations_build_service_contract,
    humanitarian_relief_operations_configure_runtime,
    humanitarian_relief_operations_empty_state,
    humanitarian_relief_operations_permissions_contract,
    humanitarian_relief_operations_receive_event,
    humanitarian_relief_operations_register_rule,
    humanitarian_relief_operations_runtime_smoke,
    humanitarian_relief_operations_set_parameter,
)
from .ui import humanitarian_relief_operations_render_workbench, humanitarian_relief_operations_ui_contract
from .wizards import wizard_catalog
PBC_KEY = "humanitarian_relief_operations"
def _digest(value: Any) -> str: return sha256(repr(value).encode('utf-8')).hexdigest()

@dataclass
class HumanitarianReliefOperationsStandaloneApp:
    tenant: str = "tenant-relief-001"
    state: dict = field(default_factory=humanitarian_relief_operations_empty_state)
    assessments: dict[str, dict] = field(default_factory=dict)
    households: dict[str, dict] = field(default_factory=dict)
    aid_lots: dict[str, dict] = field(default_factory=dict)
    shipments: dict[str, dict] = field(default_factory=dict)
    distributions: dict[str, dict] = field(default_factory=dict)
    partners: dict[str, dict] = field(default_factory=dict)
    protection_cases: dict[str, dict] = field(default_factory=dict)
    donor_packs: dict[str, dict] = field(default_factory=dict)
    exceptions: dict[str, dict] = field(default_factory=dict)

    def configure(self) -> dict:
        cfg = humanitarian_relief_operations_configure_runtime(self.state, {'database_backend': 'postgresql', 'event_topic': HUMANITARIAN_RELIEF_OPERATIONS_REQUIRED_EVENT_TOPIC})
        self.state = cfg['state']
        for name, value in (("safe_site_capacity_per_hour", 250), ("stockout_warning_days", 5), ("payout_retry_hours", 24), ("protection_follow_up_days", 3)):
            param = humanitarian_relief_operations_set_parameter(self.state, name, value); self.state = param['state']
        for rule in (("beneficiary_dedupe_required","registration"),("quarantined_lots_blocked","warehouse"),("donor_earmarks_enforced","donor"),("protected_fields_redacted","assistant")):
            registered = humanitarian_relief_operations_register_rule(self.state, {'rule_id': rule[0], 'scope': rule[1], 'effect': 'block_on_failure'}); self.state = registered['state']
        received = humanitarian_relief_operations_receive_event(self.state, {'event_type': HUMANITARIAN_RELIEF_OPERATIONS_CONSUMED_EVENT_TYPES[0], 'idempotency_key': 'policy-relief-001'})
        self.state = received['state']
        return {'ok': cfg['ok'] and received['ok'], 'side_effects': ()}

    def capture_assessment(self, assessment_id: str, household_id: str, status: str = 'rapid', **payload: Any) -> dict:
        required = ('site','displacement_status','household_members','sector_severity','assessor_confidence')
        missing = tuple(field for field in required if field not in payload)
        assessment = {'id': assessment_id, 'household_id': household_id, 'status': 'draft' if missing else status, 'missing': missing, 'site': payload.get('site'), 'vulnerability_factors': tuple(payload.get('vulnerability_factors', ())), 'sector_severity': payload.get('sector_severity', {}), 'review_status': 'action_ready' if status == 'verified' and not missing else 'needs_review', 'offline_device_id': payload.get('offline_device_id')}
        self.assessments[assessment_id] = assessment
        return {'ok': not missing, 'assessment': assessment, 'side_effects': ()}

    def register_household(self, household_id: str, head_name: str, members: tuple[str, ...], alternate_spellings: tuple[str, ...] = ()) -> dict:
        duplicate = any(head_name.lower() == h['head_name'].lower() or bool(set(alternate_spellings) & set(h.get('alternate_spellings', ()))) for h in self.households.values())
        household = {'id': household_id, 'head_name': head_name, 'members': members, 'alternate_spellings': alternate_spellings, 'status': 'duplicate_review' if duplicate else 'approved', 'dedupe_rationale': None if duplicate else 'no strong match'}
        self.households[household_id] = household
        return {'ok': not duplicate, 'household': household, 'side_effects': ()}

    def record_aid_lot(self, lot_id: str, item_id: str, quantity: int, expiry_ok: bool = True, quarantined: bool = False, **payload: Any) -> dict:
        lot = {'id': lot_id, 'item_id': item_id, 'quantity': quantity, 'available': quantity, 'kit_version': payload.get('kit_version', 'standard-v1'), 'sector_category': payload.get('sector_category', 'food'), 'expiry_ok': expiry_ok, 'quarantined': quarantined, 'storage_conditions': payload.get('storage_conditions', 'dry secure')}
        self.aid_lots[lot_id] = lot
        return {'ok': expiry_ok and not quarantined, 'lot': lot, 'side_effects': ()}

    def onboard_partner(self, partner_id: str, due_diligence_status: str = 'complete', agreement_current: bool = True, safeguarding_ok: bool = True) -> dict:
        partner = {'id': partner_id, 'due_diligence_status': due_diligence_status, 'agreement_current': agreement_current, 'safeguarding_ok': safeguarding_ok, 'ready': due_diligence_status == 'complete' and agreement_current and safeguarding_ok, 'performance_score': 0.86}
        self.partners[partner_id] = partner
        return {'ok': partner['ready'], 'partner': partner, 'side_effects': ()}

    def plan_shipment(self, shipment_id: str, partner_id: str, destination_site: str, lot_quantities: dict[str, int]) -> dict:
        invalid = tuple(lot_id for lot_id, qty in lot_quantities.items() if lot_id not in self.aid_lots or self.aid_lots[lot_id]['available'] < qty or self.aid_lots[lot_id]['quarantined'] or not self.aid_lots[lot_id]['expiry_ok'])
        partner_ready = self.partners.get(partner_id, {}).get('ready') is True
        shipment = {'id': shipment_id, 'partner_id': partner_id, 'destination_site': destination_site, 'lot_quantities': dict(lot_quantities), 'route_legs': ('warehouse','checkpoint','site'), 'state': 'blocked' if invalid or not partner_ready else 'loaded', 'invalid_lots': invalid, 'pod_evidence': None}
        if shipment['state'] == 'loaded':
            for lot_id, qty in lot_quantities.items(): self.aid_lots[lot_id]['available'] -= qty
        self.shipments[shipment_id] = shipment
        return {'ok': shipment['state'] == 'loaded', 'shipment': shipment, 'side_effects': ()}

    def reconcile_distribution(self, distribution_id: str, shipment_id: str, planned: int, handed_over: int, returned: int = 0, damaged: int = 0, modality: str = 'in_kind') -> dict:
        unaccounted = planned - handed_over - returned - damaged
        distribution = {'id': distribution_id, 'shipment_id': shipment_id, 'modality': modality, 'planned': planned, 'handed_over': handed_over, 'returned': returned, 'damaged': damaged, 'unaccounted': unaccounted, 'status': 'closed' if unaccounted == 0 else 'exception'}
        self.distributions[distribution_id] = distribution
        if unaccounted:
            self.exceptions[f'EX-{distribution_id}'] = {'type': 'distribution_variance', 'distribution_id': distribution_id, 'unaccounted': unaccounted, 'status': 'open'}
        return {'ok': unaccounted == 0, 'distribution': distribution, 'side_effects': ()}

    def open_protection_referral(self, case_id: str, household_id: str, risk_type: str) -> dict:
        case = {'id': case_id, 'household_id': household_id, 'risk_type': risk_type, 'restricted_narrative': 'redacted', 'case_owner': 'protection_officer', 'provider_handoff_status': 'pending', 'minimum_disclosure_scope': ('case_owner','provider')}
        self.protection_cases[case_id] = case
        return {'ok': household_id in self.households, 'case': case, 'side_effects': ()}

    def build_donor_pack(self, pack_id: str, donor: str, distribution_ids: tuple[str, ...]) -> dict:
        distributions = tuple(self.distributions[item] for item in distribution_ids)
        pack = {'id': pack_id, 'donor': donor, 'distribution_ids': distribution_ids, 'aggregated_outputs': {'households_served': sum(d['handed_over'] for d in distributions)}, 'suppression_policy': 'no_names_no_survivor_detail', 'signoff_status': 'ready' if all(d['status'] == 'closed' for d in distributions) else 'blocked'}
        self.donor_packs[pack_id] = pack
        return {'ok': pack['signoff_status'] == 'ready', 'donor_pack': pack, 'side_effects': ()}

    def assistant_brief_preview(self, document: str, instruction: str) -> dict:
        plan = document_instruction_plan(document, instruction)
        crud = datastore_crud_plan('create', table=f'{PBC_KEY}_distribution_event', payload={'instruction': instruction})
        return {'ok': plan['ok'] and crud['ok'], 'document_plan': plan, 'crud_preview': crud, 'requires_confirmation': True, 'redaction_policy': 'beneficiary_and_protection_safe', 'side_effects': ()}

    def app_contract(self) -> dict:
        return {'format': 'appgen.humanitarian-relief-operations.standalone-app.v1', 'ok': True, 'pbc': PBC_KEY, 'owned_tables': HUMANITARIAN_RELIEF_OPERATIONS_OWNED_TABLES, 'database_backends': HUMANITARIAN_RELIEF_OPERATIONS_ALLOWED_DATABASE_BACKENDS, 'event_contract': 'AppGen-X', 'stream_engine_picker_visible': False, 'schema': humanitarian_relief_operations_build_schema_contract(), 'services': humanitarian_relief_operations_build_service_contract(), 'routes': humanitarian_relief_operations_build_api_contract(), 'permissions': humanitarian_relief_operations_permissions_contract(), 'ui': humanitarian_relief_operations_ui_contract(), 'workbench': humanitarian_relief_operations_render_workbench(), 'forms': form_catalog(), 'wizards': wizard_catalog(), 'controls': control_catalog(), 'agent': chatbot_interface_contract(), 'composed_agent': composed_agent_contribution(), 'dsl': {'pbc': PBC_KEY, 'skills_namespace': f'{PBC_KEY}_skills', 'single_pbc_app': True}, 'side_effects': ()}

    def run_demo(self) -> dict:
        cfg = self.configure()
        assessment = self.capture_assessment('ASM-001','HH-001', status='verified', site='Camp A', displacement_status='displaced', household_members=5, sector_severity={'food':4,'shelter':3}, assessor_confidence=0.88)
        household = self.register_household('HH-001','Amina Noor',('Amina','Child 1'),('A. Noor',))
        duplicate = self.register_household('HH-002','Amina Noor',('Amina',),('A. Noor',))
        lot = self.record_aid_lot('LOT-001','KIT-FOOD',100)
        bad_lot = self.record_aid_lot('LOT-BAD','KIT-FOOD',50,quarantined=True)
        partner = self.onboard_partner('PARTNER-001')
        blocked_shipment = self.plan_shipment('SHIP-BLOCK','PARTNER-001','Camp A',{'LOT-BAD':10})
        shipment = self.plan_shipment('SHIP-001','PARTNER-001','Camp A',{'LOT-001':20})
        variance = self.reconcile_distribution('DIST-BAD','SHIP-001',planned=20,handed_over=18,returned=1)
        distribution = self.reconcile_distribution('DIST-001','SHIP-001',planned=20,handed_over=19,returned=1)
        protection = self.open_protection_referral('PROT-001','HH-001','child_protection')
        donor = self.build_donor_pack('DONOR-001','ECHO',('DIST-001',))
        assistant = self.assistant_brief_preview('field notes and distribution variance', 'draft donor-safe summary and distribution correction')
        checks = (cfg['ok'], assessment['ok'], household['ok'], duplicate['ok'] is False, lot['ok'], bad_lot['ok'] is False, partner['ok'], blocked_shipment['ok'] is False, shipment['ok'], variance['ok'] is False, distribution['ok'], protection['ok'], donor['ok'], assistant['ok'])
        return {'ok': all(checks), 'duplicate': duplicate, 'blocked_shipment': blocked_shipment, 'variance': variance, 'donor': donor, 'assistant': assistant, 'app_contract': self.app_contract(), 'side_effects': ()}

def single_pbc_app_contract() -> dict:
    return HumanitarianReliefOperationsStandaloneApp().app_contract()
def standalone_smoke_test() -> dict:
    app = HumanitarianReliefOperationsStandaloneApp(); demo = app.run_demo(); runtime = humanitarian_relief_operations_runtime_smoke(); contract = single_pbc_app_contract()
    return {'ok': demo['ok'] and runtime['ok'] and contract['ok'] and contract['stream_engine_picker_visible'] is False, 'demo': demo, 'runtime': runtime, 'contract': contract, 'side_effects': ()}
