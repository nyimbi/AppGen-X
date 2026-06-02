"""Guided workflows for the Utilities Metering and Billing standalone PBC app."""
from .slice_app import PBC_KEY, WIZARD_DEFINITIONS

def wizard_catalog(): return {"ok": True, "pbc": PBC_KEY, "wizards": WIZARD_DEFINITIONS, "side_effects": ()}
def wizard_for(key):
    wizard = next((item for item in WIZARD_DEFINITIONS if item.get("id") == key or item.get("key") == key), None)
    return {"ok": wizard is not None, "wizard": wizard, "side_effects": ()}
