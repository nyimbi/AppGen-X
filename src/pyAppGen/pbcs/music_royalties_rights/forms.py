"""Music royalties and rights forms."""
PBC_KEY="music_royalties_rights"
def form_catalog():
    forms=(
        {"id":"work_identity","owned_table":"music_royalties_rights_musical_work","fields":("canonical_title","alternate_titles","iswc","contributors","language","duration","duplicate_confidence"),"validations":("canonical title","duplicate review")},
        {"id":"contributor_chain","owned_table":"music_royalties_rights_musical_work","fields":("role","legal_name","ipi","administrator","territory","right_type","effective_dates"),"validations":("role-specific identity","admin chain")},
        {"id":"split_version","owned_table":"music_royalties_rights_rights_split","fields":("work_id","version","effective_from","writer_share","publisher_share","master_share","reason","status"),"validations":("share total","effective dating")},
        {"id":"recording_linkage","owned_table":"music_royalties_rights_recording","fields":("isrc","family","work_links","performers","producer_points","neighboring_rights"),"validations":("work match confidence","variant inheritance")},
        {"id":"license_bundle","owned_table":"music_royalties_rights_license","fields":("grant_type","media","territory","term","exclusivity","fee_basis","rate_basis","approval_authority"),"validations":("grant active","rights not over-granted")},
        {"id":"usage_ingestion","owned_table":"music_royalties_rights_usage_report","fields":("source_type","fingerprint","period","line_count","territories","currency","confidence"),"validations":("source contract","dedupe lineage")},
        {"id":"royalty_statement_run","owned_table":"music_royalties_rights_royalty_statement","fields":("period","usage_lines","rate_rules","split_versions","deductions","reserves","payees","withholding"),"validations":("line traceability","period close")},
        {"id":"rights_dispute","owned_table":"music_royalties_rights_rights_dispute","fields":("dispute_type","contested_object","evidence","sla","status","settlement_reason"),"validations":("evidence preserved","typed routing")},
    )
    return {"ok":True,"pbc":PBC_KEY,"forms":forms,"side_effects":()}
def form_for(form_id):
    return next(({"ok":True,"form":f,"side_effects":()} for f in form_catalog()["forms"] if f["id"]==form_id), {"ok":False,"reason":"unknown_form","side_effects":()})
def smoke_test(): return {"ok":len(form_catalog()["forms"])>=8 and form_for("royalty_statement_run")["ok"],"side_effects":()}
