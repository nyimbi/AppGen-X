"""Music royalties and rights guided workflows."""
PBC_KEY="music_royalties_rights"
def wizard_catalog():
    wizards=(
        {"id":"repertoire_intake","steps":("match titles","capture contributors","validate admin chain","approve splits","mark statement-ready")},
        {"id":"recording_registration","steps":("capture ISRC","link works","resolve variants","capture neighboring rights","approve master participation")},
        {"id":"license_approval","steps":("classify grant","check territory and term","price rates","route approvals","activate license")},
        {"id":"usage_to_statement","steps":("ingest source","normalize and dedupe","match work/recording","apply rates and splits","close statement")},
        {"id":"recoupment_and_payment","steps":("apply advances","apply deductions","withhold tax","release reserves","route payable")},
        {"id":"dispute_to_restatement","steps":("intake dispute","preserve evidence","freeze affected lines","resolve ownership","issue correction")},
    )
    return {"ok":True,"pbc":PBC_KEY,"wizards":wizards,"side_effects":()}
def wizard_for(wizard_id):
    return next(({"ok":True,"wizard":w,"side_effects":()} for w in wizard_catalog()["wizards"] if w["id"]==wizard_id), {"ok":False,"reason":"unknown_wizard","side_effects":()})
def smoke_test(): return {"ok":len(wizard_catalog()["wizards"])>=6 and wizard_for("usage_to_statement")["ok"],"side_effects":()}
