"""Forms for the Utilities Metering and Billing standalone PBC app."""
from .slice_app import FORM_DEFINITIONS, PBC_KEY

def form_catalog(): return {"ok": True, "pbc": PBC_KEY, "forms": FORM_DEFINITIONS, "side_effects": ()}
def form_for(key):
    form = next((item for item in FORM_DEFINITIONS if item.get("id") == key or item.get("key") == key), None)
    return {"ok": form is not None, "form": form, "side_effects": ()}
