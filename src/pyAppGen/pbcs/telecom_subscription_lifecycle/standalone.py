"""Standalone one-PBC Telecom Subscription Lifecycle app."""
from __future__ import annotations
from dataclasses import dataclass, field
from .agent import chatbot_interface_contract, composed_agent_contribution, datastore_crud_plan, document_instruction_plan
from .controls import control_catalog, evaluate_control
from .forms import form_catalog
from .runtime import *
from .ui import telecom_subscription_lifecycle_render_workbench, telecom_subscription_lifecycle_ui_contract
from .wizards import wizard_catalog

PBC_KEY = "telecom_subscription_lifecycle"

@dataclass
class TelecomSubscriptionLifecycleStandaloneApp:
    tenant: str = "tenant-telecom-sub-001"
    state: dict = field(default_factory=telecom_subscription_lifecycle_empty_state)
    subscriptions: dict = field(default_factory=dict)
    plans: dict = field(default_factory=dict)
    sims: dict = field(default_factory=dict)
    activations: dict = field(default_factory=dict)
    usage: dict = field(default_factory=dict)
    roaming: dict = field(default_factory=dict)
    churn: dict = field(default_factory=dict)

    def configure(self, database_backend="postgresql"):
        cfg = telecom_subscription_lifecycle_configure_runtime(self.state, {"database_backend": database_backend, "event_topic": TELECOM_SUBSCRIPTION_LIFECYCLE_REQUIRED_EVENT_TOPIC}); self.state = cfg["state"]
        for name, value in (("sim_swap_cooloff_hours", 24), ("roaming_spend_cap", 100), ("usage_alert_percent", 80), ("assistant_confirmation_required", True)):
            res = telecom_subscription_lifecycle_set_parameter(self.state, name, value); self.state = res["state"]
        inbound = telecom_subscription_lifecycle_receive_event(self.state, {"event_type": TELECOM_SUBSCRIPTION_LIFECYCLE_CONSUMED_EVENT_TYPES[0], "idempotency_key": "sub-policy-001"}); self.state = inbound["state"]
        return {"ok": cfg["ok"] and inbound["ok"], "side_effects": ()}

    def define_plan(self, plan_id, market, channel, effective_date, allowances, eligibility=True):
        ctl = evaluate_control("plan_version_effective_and_eligible", locals())
        row = {"id": plan_id, "tenant": self.tenant, "market": market, "channel": channel, "effective_date": effective_date, "allowances": allowances, "eligibility": eligibility, "status": "active" if ctl["ok"] else "blocked", "blockers": ctl["missing"]}
        self.plans[plan_id] = row; return {"ok": ctl["ok"], "plan": row, "side_effects": ()}

    def create_subscription(self, subscription_id, customer_ref, payer_ref, msisdn, plan_id):
        ctl = evaluate_control("subscription_has_customer_plan_and_identifier", locals())
        row = {"id": subscription_id, "tenant": self.tenant, "customer_ref": customer_ref, "payer_ref": payer_ref, "msisdn": msisdn, "plan_id": plan_id, "state": "draft" if ctl["ok"] else "blocked", "blockers": ctl["missing"]}
        self.subscriptions[subscription_id] = row; return {"ok": plan_id in self.plans and ctl["ok"], "subscription": row, "side_effects": ()}

    def assign_sim(self, sim_id, subscription_id, iccid, imsi, eid=None, profile_token=None):
        control = "esim_requires_eid_and_token" if eid or profile_token else "sim_profile_identity_complete"
        ctl = evaluate_control(control, locals())
        row = {"id": sim_id, "tenant": self.tenant, "subscription_id": subscription_id, "iccid": iccid, "imsi": imsi, "eid": eid, "profile_token": profile_token, "state": "assigned" if ctl["ok"] else "blocked", "blockers": ctl["missing"]}
        self.sims[sim_id] = row; return {"ok": subscription_id in self.subscriptions and ctl["ok"], "sim": row, "side_effects": ()}

    def request_activation(self, activation_id, subscription_id, identity_approved, plan_locked, sim_bound, provisioning_steps):
        ctl = evaluate_control("activation_ready_for_network_provisioning", locals())
        row = {"id": activation_id, "tenant": self.tenant, "subscription_id": subscription_id, "identity_approved": identity_approved, "plan_locked": plan_locked, "sim_bound": sim_bound, "provisioning_steps": tuple(provisioning_steps or ()), "state": "pending_provisioning" if ctl["ok"] else "blocked", "blockers": ctl["missing"]}
        self.activations[activation_id] = row
        if ctl["ok"] and subscription_id in self.subscriptions: self.subscriptions[subscription_id]["state"] = "pending_activation"
        return {"ok": subscription_id in self.subscriptions and ctl["ok"], "activation": row, "side_effects": ()}

    def complete_activation(self, activation_id, service_test=True):
        activation = self.activations.get(activation_id, {})
        ok = bool(activation) and service_test and activation.get("state") == "pending_provisioning"
        if ok:
            activation["state"] = "active"; self.subscriptions[activation["subscription_id"]]["state"] = "active"
        return {"ok": ok, "activation": activation, "side_effects": ()}

    def open_port_case(self, port_id, subscription_id, port_type, donor_network, authorization_proof, recent_swap_clear=True):
        ctl = evaluate_control("port_out_requires_consent_and_no_recent_swap", locals()) if port_type == "port_out" else {"ok": bool(authorization_proof), "missing": () if authorization_proof else ("authorization_proof",)}
        row = {"id": port_id, "tenant": self.tenant, "subscription_id": subscription_id, "port_type": port_type, "donor_network": donor_network, "authorization_proof": authorization_proof, "recent_swap_clear": recent_swap_clear, "state": "approved" if ctl["ok"] else "risk_hold", "blockers": ctl["missing"]}
        self.activations[port_id] = row; return {"ok": subscription_id in self.subscriptions and ctl["ok"], "port_case": row, "side_effects": ()}

    def record_usage(self, usage_id, subscription_id, usage_type, quantity, unit, threshold_state, policy_action):
        ctl = evaluate_control("usage_threshold_action_has_policy", locals())
        row = {"id": usage_id, "tenant": self.tenant, "subscription_id": subscription_id, "usage_type": usage_type, "quantity": quantity, "unit": unit, "threshold_state": threshold_state, "policy_action": policy_action, "status": "evaluated" if ctl["ok"] else "blocked", "blockers": ctl["missing"]}
        self.usage[usage_id] = row; return {"ok": subscription_id in self.subscriptions and ctl["ok"], "usage": row, "side_effects": ()}

    def enable_roaming(self, roaming_id, subscription_id, destination, partner_network, entitlement, spend_cap, confirmed=False):
        ctl = evaluate_control("roaming_high_cost_requires_confirmation", locals())
        row = {"id": roaming_id, "tenant": self.tenant, "subscription_id": subscription_id, "destination": destination, "partner_network": partner_network, "entitlement": entitlement, "spend_cap": spend_cap, "state": "enabled" if ctl["ok"] else "confirmation_required", "blockers": ctl["missing"]}
        self.roaming[roaming_id] = row; return {"ok": subscription_id in self.subscriptions and ctl["ok"], "roaming": row, "side_effects": ()}

    def evaluate_churn(self, risk_id, subscription_id, reason_codes, score, save_offer=None, approval_required=True):
        ctl = evaluate_control("retention_offer_requires_approval", locals())
        row = {"id": risk_id, "tenant": self.tenant, "subscription_id": subscription_id, "reason_codes": tuple(reason_codes or ()), "score": score, "save_offer": save_offer, "approval_required": approval_required, "state": "offer_review" if ctl["ok"] else "monitor", "blockers": ctl["missing"]}
        self.churn[risk_id] = row; return {"ok": subscription_id in self.subscriptions and bool(reason_codes), "risk": row, "side_effects": ()}

    def assistant_preview(self, document, instruction, confirmed=False):
        ctl = evaluate_control("agent_mutations_require_confirmation", {"confirmed": confirmed})
        doc = document_instruction_plan(document, instruction); crud = datastore_crud_plan("create", table="telecom_subscription_lifecycle_activation_request", payload={"instruction": instruction})
        return {"ok": doc["ok"] and crud["ok"] and ctl["ok"], "document_plan": doc, "crud_preview": crud, "requires_confirmation": not confirmed, "side_effects": ()}

    def app_contract(self):
        return {"format":"appgen.telecom-subscription-lifecycle.standalone-app.v1", "ok": True, "pbc": PBC_KEY, "database_backends": TELECOM_SUBSCRIPTION_LIFECYCLE_ALLOWED_DATABASE_BACKENDS, "event_contract":"AppGen-X", "stream_engine_picker_visible": False, "owned_tables": TELECOM_SUBSCRIPTION_LIFECYCLE_OWNED_TABLES, "schema": telecom_subscription_lifecycle_build_schema_contract(), "services": telecom_subscription_lifecycle_build_service_contract(), "routes": telecom_subscription_lifecycle_build_api_contract(), "permissions": telecom_subscription_lifecycle_permissions_contract(), "ui": telecom_subscription_lifecycle_ui_contract(), "workbench": telecom_subscription_lifecycle_render_workbench(), "forms": form_catalog(), "wizards": wizard_catalog(), "controls": control_catalog(), "agent": chatbot_interface_contract(), "composed_agent": composed_agent_contribution(), "dsl": {"pbc": PBC_KEY, "skills_namespace": f"{PBC_KEY}_skills", "single_pbc_app": True}, "side_effects": ()}

    def run_demo(self):
        checks = [self.configure()["ok"]]
        checks.append(self.define_plan("P1", "KE", "digital", "2026-06-01", {"data_gb": 20})["ok"])
        checks.append(self.create_subscription("S0", None, "payer", "254700000", "P1")["ok"] is False)
        checks.append(self.create_subscription("S1", "cust-1", "payer", "254700000", "P1")["ok"])
        checks.append(self.assign_sim("SIM0", "S1", "iccid", None)["ok"] is False)
        checks.append(self.assign_sim("SIM1", "S1", "iccid", "imsi")["ok"])
        checks.append(self.request_activation("A0", "S1", True, True, False, ("hlr",))["ok"] is False)
        checks.append(self.request_activation("A1", "S1", True, True, True, ("hlr", "data_policy"))["ok"])
        checks.append(self.complete_activation("A1")["ok"])
        checks.append(self.open_port_case("PO0", "S1", "port_out", "donor", "auth", False)["ok"] is False)
        checks.append(self.open_port_case("PI1", "S1", "port_in", "donor", "auth")["ok"])
        checks.append(self.record_usage("U1", "S1", "data", 18, "GB", "80_percent", "notify")["ok"])
        checks.append(self.enable_roaming("R0", "S1", "high_cost_zone", "partner", "daily_pass", 100, False)["ok"] is False)
        checks.append(self.enable_roaming("R1", "S1", "high_cost_zone", "partner", "daily_pass", 100, True)["ok"])
        checks.append(self.evaluate_churn("C1", "S1", ("price_pressure", "roaming_dissatisfaction"), .81, "roaming_pass_credit")["ok"])
        checks.append(self.assistant_preview("port memo", "create activation review", False)["ok"] is False)
        checks.append(self.assistant_preview("port memo", "create activation review", True)["ok"])
        return {"ok": all(checks), "contract": self.app_contract(), "side_effects": ()}

def single_pbc_app_contract(): return TelecomSubscriptionLifecycleStandaloneApp().app_contract()
def standalone_smoke_test():
    app = TelecomSubscriptionLifecycleStandaloneApp(); demo = app.run_demo(); runtime = telecom_subscription_lifecycle_runtime_smoke(); contract = single_pbc_app_contract()
    return {"ok": demo["ok"] and runtime["ok"] and contract["ok"], "demo": demo, "runtime": runtime, "contract": contract, "side_effects": ()}
