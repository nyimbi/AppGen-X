"""Executable seed-data contract for the product_catalog_pim PBC."""

PBC_KEY = 'product_catalog_pim'
SEED_DATA = ({'table': 'product_catalog_pim_product', 'rows': ({'code': 'PRODUCT_CATALOG_PIM-001', 'status': 'active'},)}, {'table': 'product_catalog_pim_product_price', 'rows': ({'code': 'PRODUCT_CATALOG_PIM-002', 'status': 'active'},)})


def seed_plan():
    """Return deterministic seed rows without applying them."""
    tables = tuple(dict.fromkeys(item['table'] for item in SEED_DATA))
    return {
        'ok': bool(SEED_DATA),
        'pbc': PBC_KEY,
        'tables': tables,
        'rows': SEED_DATA,
        'side_effects': (),
    }


def validate_seed_data():
    """Validate seed ownership and minimum row shape."""
    invalid_tables = tuple(
        item['table'] for item in SEED_DATA if not item.get('table', '').startswith(f'{PBC_KEY}_')
    )
    invalid_rows = tuple(
        row
        for item in SEED_DATA
        for row in item.get('rows', ())
        if not row.get('code') or not row.get('status')
    )
    plan = seed_plan()
    return {
        'ok': plan['ok'] and not invalid_tables and not invalid_rows,
        'pbc': PBC_KEY,
        'plan': plan,
        'invalid_tables': invalid_tables,
        'invalid_rows': invalid_rows,
        'side_effects': (),
    }


def smoke_test():
    """Exercise seed validation without writing rows."""
    return validate_seed_data()



def standalone_seed_bundle(*, tenant='tenant_demo'):
    return {
        'pbc': PBC_KEY, 'tenant': tenant,
        'configuration': {'database_backend':'postgresql','event_topic':'appgen.product.events','retry_limit':3,'allowed_channels':('web','marketplace'),'allowed_locales':('en-US','fr-FR'),'allowed_media_roles':('hero','gallery'),'allowed_regions':('US','EU'),'default_timezone':'UTC','workbench_limit':100},
        'parameters': {'minimum_completeness':0.8,'minimum_margin':0.25,'max_missing_required_attributes':0,'content_quality_threshold':0.75,'publication_batch_size':25,'retention_days':365,'workbench_limit':100},
        'rules': ({'rule_id':'catalog.demo.sellability','tenant':tenant,'rule_type':'sellability','allowed_channels':('web','marketplace'),'allowed_locales':('en-US','fr-FR'),'required_attributes':('color','material'),'required_media_roles':('hero',),'restricted_regions':('restricted',),'status':'active'},),
        'events': ({'event_id':'tax_evt_demo','event_type':'TaxCalculated','payload':{'tenant':tenant,'product_id':'prod_demo_100','region':'US','tax_code':'standard'}}, {'event_id':'media_evt_demo','event_type':'MediaAssetApproved','payload':{'tenant':tenant,'product_id':'prod_demo_100','asset_ref':'dam://asset-demo-hero'}}, {'event_id':'inv_evt_demo','event_type':'InventoryPositionUpdated','payload':{'tenant':tenant,'product_id':'prod_demo_100','available_to_promise':25}}),
        'family': {'family_id':'fam_demo_100','tenant':tenant,'name':'Industrial Safety Helmet','taxonomy':'industrial/safety/head-protection','variant_axes':('color','size')},
        'product': {'product_id':'prod_demo_100','tenant':tenant,'family_id':'fam_demo_100','sku':'SAFE-HELMET-RED-M','name':'Red Industrial Safety Helmet','owner':'catalog_manager_1'},
        'attribute_schema': {'schema_id':'schema_demo_100','tenant':tenant,'family_id':'fam_demo_100','attributes':('color','material','certification'),'version':1,'status':'active'},
        'attributes': {'color':'red','material':'polycarbonate','certification':'ANSI-Z89.1'},
        'content': {'content_id':'content_demo_100','tenant':tenant,'product_id':'prod_demo_100','locale':'en-US','title':'Red Industrial Safety Helmet','description':'High-visibility red safety helmet with impact-rated shell, suspension, and certified industrial head protection.','seo_slug':'red-industrial-safety-helmet'},
        'media': {'media_id':'media_demo_100','tenant':tenant,'product_id':'prod_demo_100','role':'hero','asset_ref':'dam://asset-demo-hero','rights_status':'approved'},
        'price': {'price_id':'price_demo_100','tenant':tenant,'product_id':'prod_demo_100','currency':'USD','list_price':80.00,'cost':48.00},
        'compliance_claim': {'claim_id':'claim_demo_100','tenant':tenant,'product_id':'prod_demo_100','region':'US','claim_type':'safety_certification','status':'approved'},
        'publication': {'channels':('web','marketplace'),'locales':('en-US',)},
        'document':'Supplier onboarding sheet for prod_demo_100 with SKU, taxonomy, attributes, certified media, price, safety claim, and web publication request.',
        'instructions':'Register the product family and SKU, enrich attributes/content/media/price/compliance, publish to web and marketplace, then create a publication proof.',
    }
