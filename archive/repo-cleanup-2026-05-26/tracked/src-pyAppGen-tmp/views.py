import sys, os
from flask_appbuilder import ModelView, MultipleView, MasterDetailView, SimpleFormView, BaseView
from flask_appbuilder.models.sqla.interface import SQLAInterface
from sqlalchemy import create_engine, inspect, MetaData, ForeignKeyConstraint
from wtforms import Form, SelectField, SubmitField
from wtforms.validators import DataRequired
from flask import current_app
from models import *

# For the chart drawing module
engine = create_engine(current_app.config['SQLALCHEMY_DATABASE_URI'])
metadata = MetaData(bind=engine)
metadata.reflect()


class CompanyTypeModelView(ModelView):
    datamodel = SQLAInterface(CompanyType)
    list_columns = ['id']
#     edit_template = "tabbed_edit.html"
#     tab_info = {
#      "basic_info": {
#           "title": "Basic Information",
#           "fields": ["field1", "field2", "field3"]
#            },
#      "advanced_settings": {
#           "title": "Advanced Settings",
#           "fields": ["field4", "field5", "field6"]
#            }
#      }
#     def prefill_form(self, form, pk):
#        form = super(CompanyTypeModelView, self).prefill_form(form, pk)
#        self.update_redirect()
#        return form


class CompanyModelView(ModelView):
    datamodel = SQLAInterface(Company)
    list_columns = ['id', 'country', 'company_type']
#     edit_template = "tabbed_edit.html"
#     tab_info = {
#      "basic_info": {
#           "title": "Basic Information",
#           "fields": ["field1", "field2", "field3"]
#            },
#      "advanced_settings": {
#           "title": "Advanced Settings",
#           "fields": ["field4", "field5", "field6"]
#            }
#      }
#     def prefill_form(self, form, pk):
#        form = super(CompanyModelView, self).prefill_form(form, pk)
#        self.update_redirect()
#        return form


class CompanyCountryModelView(MasterDetailView):
    datamodel = SQLAInterface(Company)
    related_views = [CountryModelView]


class CompanyCompanyTypeModelView(MasterDetailView):
    datamodel = SQLAInterface(Company)
    related_views = [CompanyTypeModelView]


class CompanyMultipleModelView(MultipleView):
    views = [CompanyModelView, CompanyCountryModelView, CompanyCompanyTypeModelView]


class CountryModelView(ModelView):
    datamodel = SQLAInterface(Country)
    list_columns = ['id', 'mapx', 'comments', 'region']
#     edit_template = "tabbed_edit.html"
#     tab_info = {
#      "basic_info": {
#           "title": "Basic Information",
#           "fields": ["field1", "field2", "field3"]
#            },
#      "advanced_settings": {
#           "title": "Advanced Settings",
#           "fields": ["field4", "field5", "field6"]
#            }
#      }
#     def prefill_form(self, form, pk):
#        form = super(CountryModelView, self).prefill_form(form, pk)
#        self.update_redirect()
#        return form


class CountryRegionModelView(MasterDetailView):
    datamodel = SQLAInterface(Country)
    related_views = [RegionModelView]


class RegionModelView(ModelView):
    datamodel = SQLAInterface(Region)
    list_columns = ['id']
#     edit_template = "tabbed_edit.html"
#     tab_info = {
#      "basic_info": {
#           "title": "Basic Information",
#           "fields": ["field1", "field2", "field3"]
#            },
#      "advanced_settings": {
#           "title": "Advanced Settings",
#           "fields": ["field4", "field5", "field6"]
#            }
#      }
#     def prefill_form(self, form, pk):
#        form = super(RegionModelView, self).prefill_form(form, pk)
#        self.update_redirect()
#        return form


class AudaInitiativeModelView(ModelView):
    datamodel = SQLAInterface(AudaInitiative)
    list_columns = ['id', 'comment']
#     edit_template = "tabbed_edit.html"
#     tab_info = {
#      "basic_info": {
#           "title": "Basic Information",
#           "fields": ["field1", "field2", "field3"]
#            },
#      "advanced_settings": {
#           "title": "Advanced Settings",
#           "fields": ["field4", "field5", "field6"]
#            }
#      }
#     def prefill_form(self, form, pk):
#        form = super(AudaInitiativeModelView, self).prefill_form(form, pk)
#        self.update_redirect()
#        return form


class AudaInitiativeCountryModelView(ModelView):
    datamodel = SQLAInterface(AudaInitiativeCountry)
    list_columns = ['auda_initiative', 'country']
#     edit_template = "tabbed_edit.html"
#     tab_info = {
#      "basic_info": {
#           "title": "Basic Information",
#           "fields": ["field1", "field2", "field3"]
#            },
#      "advanced_settings": {
#           "title": "Advanced Settings",
#           "fields": ["field4", "field5", "field6"]
#            }
#      }
#     def prefill_form(self, form, pk):
#        form = super(AudaInitiativeCountryModelView, self).prefill_form(form, pk)
#        self.update_redirect()
#        return form


class AudaInitiativeCountryAudaInitiativeModelView(MasterDetailView):
    datamodel = SQLAInterface(AudaInitiativeCountry)
    related_views = [AudaInitiativeModelView]


class AudaInitiativeCountryCountryModelView(MasterDetailView):
    datamodel = SQLAInterface(AudaInitiativeCountry)
    related_views = [CountryModelView]


class AudaInitiativeCountryMultipleModelView(MultipleView):
    views = [AudaInitiativeCountryModelView, AudaInitiativeCountryAudaInitiativeModelView, AudaInitiativeCountryCountryModelView]


class AudaPartnerModelView(ModelView):
    datamodel = SQLAInterface(AudaPartner)
    list_columns = ['id']
#     edit_template = "tabbed_edit.html"
#     tab_info = {
#      "basic_info": {
#           "title": "Basic Information",
#           "fields": ["field1", "field2", "field3"]
#            },
#      "advanced_settings": {
#           "title": "Advanced Settings",
#           "fields": ["field4", "field5", "field6"]
#            }
#      }
#     def prefill_form(self, form, pk):
#        form = super(AudaPartnerModelView, self).prefill_form(form, pk)
#        self.update_redirect()
#        return form


class AudaPartnerCountryModelView(ModelView):
    datamodel = SQLAInterface(AudaPartnerCountry)
    list_columns = ['auda_partner', 'country']
#     edit_template = "tabbed_edit.html"
#     tab_info = {
#      "basic_info": {
#           "title": "Basic Information",
#           "fields": ["field1", "field2", "field3"]
#            },
#      "advanced_settings": {
#           "title": "Advanced Settings",
#           "fields": ["field4", "field5", "field6"]
#            }
#      }
#     def prefill_form(self, form, pk):
#        form = super(AudaPartnerCountryModelView, self).prefill_form(form, pk)
#        self.update_redirect()
#        return form


class AudaPartnerCountryAudaPartnerModelView(MasterDetailView):
    datamodel = SQLAInterface(AudaPartnerCountry)
    related_views = [AudaPartnerModelView]


class AudaPartnerCountryCountryModelView(MasterDetailView):
    datamodel = SQLAInterface(AudaPartnerCountry)
    related_views = [CountryModelView]


class AudaPartnerCountryMultipleModelView(MultipleView):
    views = [AudaPartnerCountryModelView, AudaPartnerCountryAudaPartnerModelView, AudaPartnerCountryCountryModelView]


class LawModelView(ModelView):
    datamodel = SQLAInterface(Law)
    list_columns = ['id', 'country', 'date_of_enactment', 'text']
#     edit_template = "tabbed_edit.html"
#     tab_info = {
#      "basic_info": {
#           "title": "Basic Information",
#           "fields": ["field1", "field2", "field3"]
#            },
#      "advanced_settings": {
#           "title": "Advanced Settings",
#           "fields": ["field4", "field5", "field6"]
#            }
#      }
#     def prefill_form(self, form, pk):
#        form = super(LawModelView, self).prefill_form(form, pk)
#        self.update_redirect()
#        return form


class LawCountryModelView(MasterDetailView):
    datamodel = SQLAInterface(Law)
    related_views = [CountryModelView]


class ResourceTypeModelView(ModelView):
    datamodel = SQLAInterface(ResourceType)
    list_columns = ['id']
#     edit_template = "tabbed_edit.html"
#     tab_info = {
#      "basic_info": {
#           "title": "Basic Information",
#           "fields": ["field1", "field2", "field3"]
#            },
#      "advanced_settings": {
#           "title": "Advanced Settings",
#           "fields": ["field4", "field5", "field6"]
#            }
#      }
#     def prefill_form(self, form, pk):
#        form = super(ResourceTypeModelView, self).prefill_form(form, pk)
#        self.update_redirect()
#        return form


class ResourceModelView(ModelView):
    datamodel = SQLAInterface(Resource)
    list_columns = ['id', 'resource_type']
#     edit_template = "tabbed_edit.html"
#     tab_info = {
#      "basic_info": {
#           "title": "Basic Information",
#           "fields": ["field1", "field2", "field3"]
#            },
#      "advanced_settings": {
#           "title": "Advanced Settings",
#           "fields": ["field4", "field5", "field6"]
#            }
#      }
#     def prefill_form(self, form, pk):
#        form = super(ResourceModelView, self).prefill_form(form, pk)
#        self.update_redirect()
#        return form


class ResourceResourceTypeModelView(MasterDetailView):
    datamodel = SQLAInterface(Resource)
    related_views = [ResourceTypeModelView]


class CountryResourceModelView(ModelView):
    datamodel = SQLAInterface(CountryResource)
    list_columns = ['country', 'resource']
#     edit_template = "tabbed_edit.html"
#     tab_info = {
#      "basic_info": {
#           "title": "Basic Information",
#           "fields": ["field1", "field2", "field3"]
#            },
#      "advanced_settings": {
#           "title": "Advanced Settings",
#           "fields": ["field4", "field5", "field6"]
#            }
#      }
#     def prefill_form(self, form, pk):
#        form = super(CountryResourceModelView, self).prefill_form(form, pk)
#        self.update_redirect()
#        return form


class CountryResourceCountryModelView(MasterDetailView):
    datamodel = SQLAInterface(CountryResource)
    related_views = [CountryModelView]


class CountryResourceResourceModelView(MasterDetailView):
    datamodel = SQLAInterface(CountryResource)
    related_views = [ResourceModelView]


class CountryResourceMultipleModelView(MultipleView):
    views = [CountryResourceModelView, CountryResourceCountryModelView, CountryResourceResourceModelView]


class StartupModelView(ModelView):
    datamodel = SQLAInterface(Startup)
    list_columns = ['id', 'country']
#     edit_template = "tabbed_edit.html"
#     tab_info = {
#      "basic_info": {
#           "title": "Basic Information",
#           "fields": ["field1", "field2", "field3"]
#            },
#      "advanced_settings": {
#           "title": "Advanced Settings",
#           "fields": ["field4", "field5", "field6"]
#            }
#      }
#     def prefill_form(self, form, pk):
#        form = super(StartupModelView, self).prefill_form(form, pk)
#        self.update_redirect()
#        return form


class StartupCountryModelView(MasterDetailView):
    datamodel = SQLAInterface(Startup)
    related_views = [CountryModelView]


class TenderModelView(ModelView):
    datamodel = SQLAInterface(Tender)
    list_columns = ['id', 'country', 'prerequisites', 'tenderdocument', 'tender_url']
#     edit_template = "tabbed_edit.html"
#     tab_info = {
#      "basic_info": {
#           "title": "Basic Information",
#           "fields": ["field1", "field2", "field3"]
#            },
#      "advanced_settings": {
#           "title": "Advanced Settings",
#           "fields": ["field4", "field5", "field6"]
#            }
#      }
#     def prefill_form(self, form, pk):
#        form = super(TenderModelView, self).prefill_form(form, pk)
#        self.update_redirect()
#        return form


class TenderCountryModelView(MasterDetailView):
    datamodel = SQLAInterface(Tender)
    related_views = [CountryModelView]


class ChartForm(Form):
    table = SelectField('Table', choices=[], validators=[DataRequired()])
    x_axis = SelectField('X Axis', choices=[], validators=[DataRequired()])
    y_axis = SelectField('Y Axis', choices=[], validators=[DataRequired()])
    submit = SubmitField('Draw Chart')


class ChartView(SimpleFormView):
    form = ChartForm
    form_title = 'Draw Chart'
    template = 'chart_view.html'


    def form_get(self, form):
        tables = [(table.name, table.name) for table in metadata.tables.values()]
        form.table.choices = tables


    def form_post(self, form):
        table_name = form.table.data
        x_axis = form.x_axis.data
        y_axis = form.y_axis.data
        table = metadata.tables[table_name]
        # Add your chart drawing logic here


        flash(f'Drawing chart for table: {table_name}, X Axis: {x_axis}, Y Axis: {y_axis}', 'info')





class SchemaView(BaseView):
    default_view = 'schema'
    @expose('/schema/')
    def schema(self):
        tables = []
        relationships = []

        for table_name, table in metadata.tables.items():
            columns = [{'name': col.name, 'type': str(col.type)} for col in table.columns]
            tables.append({'id': hash(table_name), 'name': table_name, 'columns': columns})

            for constraint in table.constraints:
                if isinstance(constraint, ForeignKeyConstraint):
                    for col, ref_col in constraint.elements.items():
                        from_id = hash(table_name)
                        to_id = hash(str(ref_col.table.name))
                        rel_type = "one-to-many"

                        relationships.append({
                            'from': from_id,
                            'to': to_id,
                            'type': rel_type
                        })

        return self.render_template('schema_view.html', schema={'tables': tables, 'relationships': relationships})

def init_views(appbuilder):
    appbuilder.add_view(CompanyTypeModelView, 'CompanyType', icon='fa-table', category='Tables')
    appbuilder.add_view(CompanyModelView, 'Company', icon='fa-table', category='Tables')
    appbuilder.add_view(CompanyMultipleModelView, 'Company Multiple', icon='fa-table', category='Multiple')
    appbuilder.add_view(CountryModelView, 'Country', icon='fa-table', category='Tables')
    appbuilder.add_view(CountryRegionModelView, 'Country Region Master Detail', icon='fa-table', category='Master Detail')
    appbuilder.add_view(RegionModelView, 'Region', icon='fa-table', category='Tables')
    appbuilder.add_view(AudaInitiativeModelView, 'AudaInitiative', icon='fa-table', category='Tables')
    appbuilder.add_view(AudaInitiativeCountryModelView, 'AudaInitiativeCountry', icon='fa-table', category='Tables')
    appbuilder.add_view(AudaInitiativeCountryMultipleModelView, 'AudaInitiativeCountry Multiple', icon='fa-table', category='Multiple')
    appbuilder.add_view(AudaPartnerModelView, 'AudaPartner', icon='fa-table', category='Tables')
    appbuilder.add_view(AudaPartnerCountryModelView, 'AudaPartnerCountry', icon='fa-table', category='Tables')
    appbuilder.add_view(AudaPartnerCountryMultipleModelView, 'AudaPartnerCountry Multiple', icon='fa-table', category='Multiple')
    appbuilder.add_view(LawModelView, 'Law', icon='fa-table', category='Tables')
    appbuilder.add_view(LawCountryModelView, 'Law Country Master Detail', icon='fa-table', category='Master Detail')
    appbuilder.add_view(ResourceTypeModelView, 'ResourceType', icon='fa-table', category='Tables')
    appbuilder.add_view(ResourceModelView, 'Resource', icon='fa-table', category='Tables')
    appbuilder.add_view(ResourceResourceTypeModelView, 'Resource ResourceType Master Detail', icon='fa-table', category='Master Detail')
    appbuilder.add_view(CountryResourceModelView, 'CountryResource', icon='fa-table', category='Tables')
    appbuilder.add_view(CountryResourceMultipleModelView, 'CountryResource Multiple', icon='fa-table', category='Multiple')
    appbuilder.add_view(StartupModelView, 'Startup', icon='fa-table', category='Tables')
    appbuilder.add_view(StartupCountryModelView, 'Startup Country Master Detail', icon='fa-table', category='Master Detail')
    appbuilder.add_view(TenderModelView, 'Tender', icon='fa-table', category='Tables')
    appbuilder.add_view(TenderCountryModelView, 'Tender Country Master Detail', icon='fa-table', category='Master Detail')
    appbuilder.add_separator('Tables')
    appbuilder.add_view(ChartView, 'Draw Chart', icon='fa-bar-chart', category='Charts')
    appbuilder.add_view(SchemaView, "Schema View", category="Database")