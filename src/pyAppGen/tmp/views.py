
import calendar
from flask import redirect, flash, url_for, Markup, g
from flask import render_template
from flask_appbuilder.models.sqla.interface import SQLAInterface
from flask_appbuilder.views import ModelView, BaseView, MasterDetailView, MultipleView, RestCRUDView, CompactCRUDMixin
from flask_appbuilder import ModelView, ModelRestApi, CompactCRUDMixin, aggregate_count, action, expose, BaseView, has_access
from flask_appbuilder.charts.views import ChartView, TimeChartView, GroupByChartView
from flask_appbuilder.models.group import aggregate_count
from flask_appbuilder.widgets import ListThumbnail, ListWidget
from flask_appbuilder.widgets import FormVerticalWidget, FormInlineWidget, FormHorizontalWidget, ShowBlockWidget
from flask_appbuilder.models.sqla.filters import FilterStartsWith, FilterEqualFunction as FA
from flask import g
# If you want to enable search
# from elasticsearch import Elasticsearch

from app import appbuilder, db

from .models import *
from .mixins import *

##########
# Various Utilities
hide_list = ['created_by', 'changed_by', 'created_on', 'changed_on']

#To pretty Print from PersonMixin
def pretty_month_year(value):
    return calendar.month_name[value.month] + ' ' + str(value.year)


def pretty_year(value):
    return str(value.year)


# def fill_gender():
#   try:
#       db.session.add(Gender(name='Male'))
#       db.session.add(Gender(name='Female'))
#       db.session.commit()
#   except:
#       db.session.rollback()
#############

def get_user():
    return g.user

# SIMPLEVIEW
class UserxView(ModelView):
    datamodel=SQLAInterface(Userx, db.session)
    related_views = []
    base_permissions = ['can_list', 'can_show', 'can_edit', 'can_delete', 'can_add']
    search_exclude_columns= []
    search_columns = ['id']
    default_sort = [('id', True)]
    list_title= 'Userx List'
    show_title='Userx Detail'
    add_title ='Add Userx'
    edit_title = 'Edit Userx'
#    label_columns=  [{column.name: column.name} for column in table.columns]
    list_columns = ['id']
    add_columns= ['id']
    edit_columns = ['id']
    show_columns = ['id']
#    description_columns = [<generator object gen_views3.<locals>.gen_simple_view.<locals>.<genexpr> at 0x10d7f5430>]
#    description_columns_editable = [<generator object gen_views3.<locals>.gen_simple_view.<locals>.<genexpr> at 0x10d7f5430>]
    show_template =  'appbuilder/general/model/show_cascade.html'
    list_template = 'appbuilder/general/model/list.html'
    add_template = 'appbuilder/general/model/add.html'
    edit_template = 'appbuilder/general/model/edit.html'
    list_widget= 'list_widget'
    show_widget = 'show_widget'
    add_widget = 'add_widget'
    edit_widget=  'edit_widget'


# MASTERVIEW
class UserxMasterView(MasterDetailView):
    datamodel = SQLAInterface(Userx)
    related_views = []
    list_columns = ['id']
    show_columns = ['id']
    search_columns = ['id']
    default_view = 'list'

# SIMPLEVIEW
class IndividualView(ModelView):
    datamodel=SQLAInterface(Individual, db.session)
    related_views = []
    base_permissions = ['can_list', 'can_show', 'can_edit', 'can_delete', 'can_add']
    search_exclude_columns= []
    search_columns = ['id', 'userx', 'is_individual', 'is_institution', 'is_company', 'is_government', 'is_online']
    default_sort = [('id', True)]
    list_title= 'Individual List'
    show_title='Individual Detail'
    add_title ='Add Individual'
    edit_title = 'Edit Individual'
#    label_columns=  [{column.name: column.name} for column in table.columns]
    list_columns = ['id', 'userx', 'is_individual', 'is_institution', 'is_company', 'is_government', 'is_online']
    add_columns= ['id', 'userx', 'is_individual', 'is_institution', 'is_company', 'is_government', 'is_online']
    edit_columns = ['id', 'userx', 'is_individual', 'is_institution', 'is_company', 'is_government', 'is_online']
    show_columns = ['id', 'userx', 'is_individual', 'is_institution', 'is_company', 'is_government', 'is_online']
#    description_columns = [<generator object gen_views3.<locals>.gen_simple_view.<locals>.<genexpr> at 0x10d7f5430>]
#    description_columns_editable = [<generator object gen_views3.<locals>.gen_simple_view.<locals>.<genexpr> at 0x10d7f5430>]
    show_template =  'appbuilder/general/model/show_cascade.html'
    list_template = 'appbuilder/general/model/list.html'
    add_template = 'appbuilder/general/model/add.html'
    edit_template = 'appbuilder/general/model/edit.html'
    list_widget= 'list_widget'
    show_widget = 'show_widget'
    add_widget = 'add_widget'
    edit_widget=  'edit_widget'


# MASTERVIEW
class IndividualMasterView(MasterDetailView):
    datamodel = SQLAInterface(Individual)
    related_views = [UserxDetailView]
    list_columns = ['id', 'userx', 'is_individual', 'is_institution', 'is_company', 'is_government', 'is_online']
    show_columns = ['id', 'userx', 'is_individual', 'is_institution', 'is_company', 'is_government', 'is_online']
    search_columns = ['id', 'userx', 'is_individual', 'is_institution', 'is_company', 'is_government', 'is_online']
    default_view = 'list'

# SIMPLEVIEW
class IndustryView(ModelView):
    datamodel=SQLAInterface(Industry, db.session)
    related_views = []
    base_permissions = ['can_list', 'can_show', 'can_edit', 'can_delete', 'can_add']
    search_exclude_columns= []
    search_columns = ['id', 'industry_code']
    default_sort = [('id', True)]
    list_title= 'Industry List'
    show_title='Industry Detail'
    add_title ='Add Industry'
    edit_title = 'Edit Industry'
#    label_columns=  [{column.name: column.name} for column in table.columns]
    list_columns = ['id', 'industry_code']
    add_columns= ['id', 'industry_code']
    edit_columns = ['id', 'industry_code']
    show_columns = ['id', 'industry_code']
#    description_columns = [<generator object gen_views3.<locals>.gen_simple_view.<locals>.<genexpr> at 0x10d7f5430>]
#    description_columns_editable = [<generator object gen_views3.<locals>.gen_simple_view.<locals>.<genexpr> at 0x10d7f5430>]
    show_template =  'appbuilder/general/model/show_cascade.html'
    list_template = 'appbuilder/general/model/list.html'
    add_template = 'appbuilder/general/model/add.html'
    edit_template = 'appbuilder/general/model/edit.html'
    list_widget= 'list_widget'
    show_widget = 'show_widget'
    add_widget = 'add_widget'
    edit_widget=  'edit_widget'


# MASTERVIEW
class IndustryMasterView(MasterDetailView):
    datamodel = SQLAInterface(Industry)
    related_views = []
    list_columns = ['id', 'industry_code']
    show_columns = ['id', 'industry_code']
    search_columns = ['id', 'industry_code']
    default_view = 'list'

# SIMPLEVIEW
class IndustryJobView(ModelView):
    datamodel=SQLAInterface(IndustryJob, db.session)
    related_views = []
    base_permissions = ['can_list', 'can_show', 'can_edit', 'can_delete', 'can_add']
    search_exclude_columns= []
    search_columns = ['industry', 'job']
    default_sort = [('id', True)]
    list_title= 'IndustryJob List'
    show_title='IndustryJob Detail'
    add_title ='Add IndustryJob'
    edit_title = 'Edit IndustryJob'
#    label_columns=  [{column.name: column.name} for column in table.columns]
    list_columns = ['industry', 'job']
    add_columns= ['industry', 'job']
    edit_columns = ['industry', 'job']
    show_columns = ['industry', 'job']
#    description_columns = [<generator object gen_views3.<locals>.gen_simple_view.<locals>.<genexpr> at 0x10d7f5430>]
#    description_columns_editable = [<generator object gen_views3.<locals>.gen_simple_view.<locals>.<genexpr> at 0x10d7f5430>]
    show_template =  'appbuilder/general/model/show_cascade.html'
    list_template = 'appbuilder/general/model/list.html'
    add_template = 'appbuilder/general/model/add.html'
    edit_template = 'appbuilder/general/model/edit.html'
    list_widget= 'list_widget'
    show_widget = 'show_widget'
    add_widget = 'add_widget'
    edit_widget=  'edit_widget'


# MASTERVIEW
class IndustryJobMultiView(MultipleView):
    datamodel = SQLAInterface(IndustryJob)
    views = [IndustryDetailView, JobDetailView]
    list_columns = ['industry', 'job']
    show_columns = ['industry', 'job']
    search_columns = ['industry', 'job']
    default_view = 'list'

# SIMPLEVIEW
class JobView(ModelView):
    datamodel=SQLAInterface(Job, db.session)
    related_views = []
    base_permissions = ['can_list', 'can_show', 'can_edit', 'can_delete', 'can_add']
    search_exclude_columns= []
    search_columns = ['id', 'company_profile', 'about_job', 'responsibilities', 'salary', 'equity', 'offers_healthcare', 'offers_vision', 'offers_401k', 'offers_dental', 'paid_time_off', 'vacation_days', 'location', 'is_remote', 'applicant_count', 'job_filled']
    default_sort = [('id', True)]
    list_title= 'Job List'
    show_title='Job Detail'
    add_title ='Add Job'
    edit_title = 'Edit Job'
#    label_columns=  [{column.name: column.name} for column in table.columns]
    list_columns = ['id', 'company_profile', 'about_job', 'responsibilities', 'salary', 'equity', 'offers_healthcare', 'offers_vision', 'offers_401k', 'offers_dental', 'paid_time_off', 'vacation_days', 'location', 'is_remote', 'applicant_count', 'job_filled']
    add_columns= ['id', 'company_profile', 'about_job', 'responsibilities', 'salary', 'equity', 'offers_healthcare', 'offers_vision', 'offers_401k', 'offers_dental', 'paid_time_off', 'vacation_days', 'location', 'is_remote', 'applicant_count', 'job_filled']
    edit_columns = ['id', 'company_profile', 'about_job', 'responsibilities', 'salary', 'equity', 'offers_healthcare', 'offers_vision', 'offers_401k', 'offers_dental', 'paid_time_off', 'vacation_days', 'location', 'is_remote', 'applicant_count', 'job_filled']
    show_columns = ['id', 'company_profile', 'about_job', 'responsibilities', 'salary', 'equity', 'offers_healthcare', 'offers_vision', 'offers_401k', 'offers_dental', 'paid_time_off', 'vacation_days', 'location', 'is_remote', 'applicant_count', 'job_filled']
#    description_columns = [<generator object gen_views3.<locals>.gen_simple_view.<locals>.<genexpr> at 0x10d7f5430>]
#    description_columns_editable = [<generator object gen_views3.<locals>.gen_simple_view.<locals>.<genexpr> at 0x10d7f5430>]
    show_template =  'appbuilder/general/model/show_cascade.html'
    list_template = 'appbuilder/general/model/list.html'
    add_template = 'appbuilder/general/model/add.html'
    edit_template = 'appbuilder/general/model/edit.html'
    list_widget= 'list_widget'
    show_widget = 'show_widget'
    add_widget = 'add_widget'
    edit_widget=  'edit_widget'


# MASTERVIEW
class JobMasterView(MasterDetailView):
    datamodel = SQLAInterface(Job)
    related_views = []
    list_columns = ['id', 'company_profile', 'about_job', 'responsibilities', 'salary', 'equity', 'offers_healthcare', 'offers_vision', 'offers_401k', 'offers_dental', 'paid_time_off', 'vacation_days', 'location', 'is_remote', 'applicant_count', 'job_filled']
    show_columns = ['id', 'company_profile', 'about_job', 'responsibilities', 'salary', 'equity', 'offers_healthcare', 'offers_vision', 'offers_401k', 'offers_dental', 'paid_time_off', 'vacation_days', 'location', 'is_remote', 'applicant_count', 'job_filled']
    search_columns = ['id', 'company_profile', 'about_job', 'responsibilities', 'salary', 'equity', 'offers_healthcare', 'offers_vision', 'offers_401k', 'offers_dental', 'paid_time_off', 'vacation_days', 'location', 'is_remote', 'applicant_count', 'job_filled']
    default_view = 'list'

# SIMPLEVIEW
class JobSkillView(ModelView):
    datamodel=SQLAInterface(JobSkill, db.session)
    related_views = []
    base_permissions = ['can_list', 'can_show', 'can_edit', 'can_delete', 'can_add']
    search_exclude_columns= []
    search_columns = ['skills', 'jobs']
    default_sort = [('id', True)]
    list_title= 'JobSkill List'
    show_title='JobSkill Detail'
    add_title ='Add JobSkill'
    edit_title = 'Edit JobSkill'
#    label_columns=  [{column.name: column.name} for column in table.columns]
    list_columns = ['skills', 'jobs']
    add_columns= ['skills', 'jobs']
    edit_columns = ['skills', 'jobs']
    show_columns = ['skills', 'jobs']
#    description_columns = [<generator object gen_views3.<locals>.gen_simple_view.<locals>.<genexpr> at 0x10d7f5430>]
#    description_columns_editable = [<generator object gen_views3.<locals>.gen_simple_view.<locals>.<genexpr> at 0x10d7f5430>]
    show_template =  'appbuilder/general/model/show_cascade.html'
    list_template = 'appbuilder/general/model/list.html'
    add_template = 'appbuilder/general/model/add.html'
    edit_template = 'appbuilder/general/model/edit.html'
    list_widget= 'list_widget'
    show_widget = 'show_widget'
    add_widget = 'add_widget'
    edit_widget=  'edit_widget'


# MASTERVIEW
class JobSkillMultiView(MultipleView):
    datamodel = SQLAInterface(JobSkill)
    views = [SkillDetailView, JobDetailView]
    list_columns = ['skills', 'jobs']
    show_columns = ['skills', 'jobs']
    search_columns = ['skills', 'jobs']
    default_view = 'list'

# SIMPLEVIEW
class SkillView(ModelView):
    datamodel=SQLAInterface(Skill, db.session)
    related_views = []
    base_permissions = ['can_list', 'can_show', 'can_edit', 'can_delete', 'can_add']
    search_exclude_columns= []
    search_columns = ['id', 'skill_value']
    default_sort = [('id', True)]
    list_title= 'Skill List'
    show_title='Skill Detail'
    add_title ='Add Skill'
    edit_title = 'Edit Skill'
#    label_columns=  [{column.name: column.name} for column in table.columns]
    list_columns = ['id', 'skill_value']
    add_columns= ['id', 'skill_value']
    edit_columns = ['id', 'skill_value']
    show_columns = ['id', 'skill_value']
#    description_columns = [<generator object gen_views3.<locals>.gen_simple_view.<locals>.<genexpr> at 0x10d7f5430>]
#    description_columns_editable = [<generator object gen_views3.<locals>.gen_simple_view.<locals>.<genexpr> at 0x10d7f5430>]
    show_template =  'appbuilder/general/model/show_cascade.html'
    list_template = 'appbuilder/general/model/list.html'
    add_template = 'appbuilder/general/model/add.html'
    edit_template = 'appbuilder/general/model/edit.html'
    list_widget= 'list_widget'
    show_widget = 'show_widget'
    add_widget = 'add_widget'
    edit_widget=  'edit_widget'


# MASTERVIEW
class SkillMasterView(MasterDetailView):
    datamodel = SQLAInterface(Skill)
    related_views = []
    list_columns = ['id', 'skill_value']
    show_columns = ['id', 'skill_value']
    search_columns = ['id', 'skill_value']
    default_view = 'list'

# SIMPLEVIEW
class EducationView(ModelView):
    datamodel=SQLAInterface(Education, db.session)
    related_views = []
    base_permissions = ['can_list', 'can_show', 'can_edit', 'can_delete', 'can_add']
    search_exclude_columns= []
    search_columns = ['id', 'individual', 'qualification', 'qual_class', 'verified', 'verification_code', 'verified_by', 'verification_date', 'verification_doc']
    default_sort = [('id', True)]
    list_title= 'Education List'
    show_title='Education Detail'
    add_title ='Add Education'
    edit_title = 'Edit Education'
#    label_columns=  [{column.name: column.name} for column in table.columns]
    list_columns = ['id', 'individual', 'qualification', 'qual_class', 'verified', 'verification_code', 'verified_by', 'verification_date', 'verification_doc']
    add_columns= ['id', 'individual', 'qualification', 'qual_class', 'verified', 'verification_code', 'verified_by', 'verification_date', 'verification_doc']
    edit_columns = ['id', 'individual', 'qualification', 'qual_class', 'verified', 'verification_code', 'verified_by', 'verification_date', 'verification_doc']
    show_columns = ['id', 'individual', 'qualification', 'qual_class', 'verified', 'verification_code', 'verified_by', 'verification_date', 'verification_doc']
#    description_columns = [<generator object gen_views3.<locals>.gen_simple_view.<locals>.<genexpr> at 0x10d7f5430>]
#    description_columns_editable = [<generator object gen_views3.<locals>.gen_simple_view.<locals>.<genexpr> at 0x10d7f5430>]
    show_template =  'appbuilder/general/model/show_cascade.html'
    list_template = 'appbuilder/general/model/list.html'
    add_template = 'appbuilder/general/model/add.html'
    edit_template = 'appbuilder/general/model/edit.html'
    list_widget= 'list_widget'
    show_widget = 'show_widget'
    add_widget = 'add_widget'
    edit_widget=  'edit_widget'


# MASTERVIEW
class EducationMasterView(MasterDetailView):
    datamodel = SQLAInterface(Education)
    related_views = [IndividualDetailView]
    list_columns = ['id', 'individual', 'qualification', 'qual_class', 'verified', 'verification_code', 'verified_by', 'verification_date', 'verification_doc']
    show_columns = ['id', 'individual', 'qualification', 'qual_class', 'verified', 'verification_code', 'verified_by', 'verification_date', 'verification_doc']
    search_columns = ['id', 'individual', 'qualification', 'qual_class', 'verified', 'verification_code', 'verified_by', 'verification_date', 'verification_doc']
    default_view = 'list'

# SIMPLEVIEW
class IndividualJobView(ModelView):
    datamodel=SQLAInterface(IndividualJob, db.session)
    related_views = []
    base_permissions = ['can_list', 'can_show', 'can_edit', 'can_delete', 'can_add']
    search_exclude_columns= []
    search_columns = ['individual', 'job']
    default_sort = [('id', True)]
    list_title= 'IndividualJob List'
    show_title='IndividualJob Detail'
    add_title ='Add IndividualJob'
    edit_title = 'Edit IndividualJob'
#    label_columns=  [{column.name: column.name} for column in table.columns]
    list_columns = ['individual', 'job']
    add_columns= ['individual', 'job']
    edit_columns = ['individual', 'job']
    show_columns = ['individual', 'job']
#    description_columns = [<generator object gen_views3.<locals>.gen_simple_view.<locals>.<genexpr> at 0x10d7f5430>]
#    description_columns_editable = [<generator object gen_views3.<locals>.gen_simple_view.<locals>.<genexpr> at 0x10d7f5430>]
    show_template =  'appbuilder/general/model/show_cascade.html'
    list_template = 'appbuilder/general/model/list.html'
    add_template = 'appbuilder/general/model/add.html'
    edit_template = 'appbuilder/general/model/edit.html'
    list_widget= 'list_widget'
    show_widget = 'show_widget'
    add_widget = 'add_widget'
    edit_widget=  'edit_widget'


# MASTERVIEW
class IndividualJobMultiView(MultipleView):
    datamodel = SQLAInterface(IndividualJob)
    views = [IndividualDetailView, JobDetailView]
    list_columns = ['individual', 'job']
    show_columns = ['individual', 'job']
    search_columns = ['individual', 'job']
    default_view = 'list'

# SIMPLEVIEW
class ProfilesourceView(ModelView):
    datamodel=SQLAInterface(Profilesource, db.session)
    related_views = []
    base_permissions = ['can_list', 'can_show', 'can_edit', 'can_delete', 'can_add']
    search_exclude_columns= []
    search_columns = ['id', 'import_script']
    default_sort = [('id', True)]
    list_title= 'Profilesource List'
    show_title='Profilesource Detail'
    add_title ='Add Profilesource'
    edit_title = 'Edit Profilesource'
#    label_columns=  [{column.name: column.name} for column in table.columns]
    list_columns = ['id', 'import_script']
    add_columns= ['id', 'import_script']
    edit_columns = ['id', 'import_script']
    show_columns = ['id', 'import_script']
#    description_columns = [<generator object gen_views3.<locals>.gen_simple_view.<locals>.<genexpr> at 0x10d7f5430>]
#    description_columns_editable = [<generator object gen_views3.<locals>.gen_simple_view.<locals>.<genexpr> at 0x10d7f5430>]
    show_template =  'appbuilder/general/model/show_cascade.html'
    list_template = 'appbuilder/general/model/list.html'
    add_template = 'appbuilder/general/model/add.html'
    edit_template = 'appbuilder/general/model/edit.html'
    list_widget= 'list_widget'
    show_widget = 'show_widget'
    add_widget = 'add_widget'
    edit_widget=  'edit_widget'


# MASTERVIEW
class ProfilesourceMasterView(MasterDetailView):
    datamodel = SQLAInterface(Profilesource)
    related_views = []
    list_columns = ['id', 'import_script']
    show_columns = ['id', 'import_script']
    search_columns = ['id', 'import_script']
    default_view = 'list'

# SIMPLEVIEW
class LocationView(ModelView):
    datamodel=SQLAInterface(Location, db.session)
    related_views = []
    base_permissions = ['can_list', 'can_show', 'can_edit', 'can_delete', 'can_add']
    search_exclude_columns= []
    search_columns = ['id', 'individual']
    default_sort = [('id', True)]
    list_title= 'Location List'
    show_title='Location Detail'
    add_title ='Add Location'
    edit_title = 'Edit Location'
#    label_columns=  [{column.name: column.name} for column in table.columns]
    list_columns = ['id', 'individual']
    add_columns= ['id', 'individual']
    edit_columns = ['id', 'individual']
    show_columns = ['id', 'individual']
#    description_columns = [<generator object gen_views3.<locals>.gen_simple_view.<locals>.<genexpr> at 0x10d7f5430>]
#    description_columns_editable = [<generator object gen_views3.<locals>.gen_simple_view.<locals>.<genexpr> at 0x10d7f5430>]
    show_template =  'appbuilder/general/model/show_cascade.html'
    list_template = 'appbuilder/general/model/list.html'
    add_template = 'appbuilder/general/model/add.html'
    edit_template = 'appbuilder/general/model/edit.html'
    list_widget= 'list_widget'
    show_widget = 'show_widget'
    add_widget = 'add_widget'
    edit_widget=  'edit_widget'


# MASTERVIEW
class LocationMasterView(MasterDetailView):
    datamodel = SQLAInterface(Location)
    related_views = [IndividualDetailView]
    list_columns = ['id', 'individual']
    show_columns = ['id', 'individual']
    search_columns = ['id', 'individual']
    default_view = 'list'

# SIMPLEVIEW
class PortalView(ModelView):
    datamodel=SQLAInterface(Portal, db.session)
    related_views = []
    base_permissions = ['can_list', 'can_show', 'can_edit', 'can_delete', 'can_add']
    search_exclude_columns= []
    search_columns = ['id', 'portal_url', 'is_primary', 'portal_state', 'individual', 'has_custom_domain', 'domain', 'header_text', 'slug', 'automatic_fulfillment_digital_products', 'default_digital_max_downloads', 'default_digital_url_valid_days', 'default_mail_sender_name', 'default_mail_sender_address', 'fulfillment_auto_approve', 'fulfillment_allow_unpaid', 'reserve_stock_duration_anonymous_user', 'reserve_stock_duration_authenticated_user', 'limit_quantity_per_checkout', 'gift_card_expiry_type', 'gift_card_expiry_period_type', 'gift_card_expiry_period', 'charge_taxes_on_shipping', 'include_taxes_in_prices', 'display_gross_prices', 'language']
    default_sort = [('id', True)]
    list_title= 'Portal List'
    show_title='Portal Detail'
    add_title ='Add Portal'
    edit_title = 'Edit Portal'
#    label_columns=  [{column.name: column.name} for column in table.columns]
    list_columns = ['id', 'portal_url', 'is_primary', 'portal_state', 'individual', 'has_custom_domain', 'domain', 'header_text', 'slug', 'automatic_fulfillment_digital_products', 'default_digital_max_downloads', 'default_digital_url_valid_days', 'default_mail_sender_name', 'default_mail_sender_address', 'fulfillment_auto_approve', 'fulfillment_allow_unpaid', 'reserve_stock_duration_anonymous_user', 'reserve_stock_duration_authenticated_user', 'limit_quantity_per_checkout', 'gift_card_expiry_type', 'gift_card_expiry_period_type', 'gift_card_expiry_period', 'charge_taxes_on_shipping', 'include_taxes_in_prices', 'display_gross_prices', 'language']
    add_columns= ['id', 'portal_url', 'is_primary', 'portal_state', 'individual', 'has_custom_domain', 'domain', 'header_text', 'slug', 'automatic_fulfillment_digital_products', 'default_digital_max_downloads', 'default_digital_url_valid_days', 'default_mail_sender_name', 'default_mail_sender_address', 'fulfillment_auto_approve', 'fulfillment_allow_unpaid', 'reserve_stock_duration_anonymous_user', 'reserve_stock_duration_authenticated_user', 'limit_quantity_per_checkout', 'gift_card_expiry_type', 'gift_card_expiry_period_type', 'gift_card_expiry_period', 'charge_taxes_on_shipping', 'include_taxes_in_prices', 'display_gross_prices', 'language']
    edit_columns = ['id', 'portal_url', 'is_primary', 'portal_state', 'individual', 'has_custom_domain', 'domain', 'header_text', 'slug', 'automatic_fulfillment_digital_products', 'default_digital_max_downloads', 'default_digital_url_valid_days', 'default_mail_sender_name', 'default_mail_sender_address', 'fulfillment_auto_approve', 'fulfillment_allow_unpaid', 'reserve_stock_duration_anonymous_user', 'reserve_stock_duration_authenticated_user', 'limit_quantity_per_checkout', 'gift_card_expiry_type', 'gift_card_expiry_period_type', 'gift_card_expiry_period', 'charge_taxes_on_shipping', 'include_taxes_in_prices', 'display_gross_prices', 'language']
    show_columns = ['id', 'portal_url', 'is_primary', 'portal_state', 'individual', 'has_custom_domain', 'domain', 'header_text', 'slug', 'automatic_fulfillment_digital_products', 'default_digital_max_downloads', 'default_digital_url_valid_days', 'default_mail_sender_name', 'default_mail_sender_address', 'fulfillment_auto_approve', 'fulfillment_allow_unpaid', 'reserve_stock_duration_anonymous_user', 'reserve_stock_duration_authenticated_user', 'limit_quantity_per_checkout', 'gift_card_expiry_type', 'gift_card_expiry_period_type', 'gift_card_expiry_period', 'charge_taxes_on_shipping', 'include_taxes_in_prices', 'display_gross_prices', 'language']
#    description_columns = [<generator object gen_views3.<locals>.gen_simple_view.<locals>.<genexpr> at 0x10d7f5430>]
#    description_columns_editable = [<generator object gen_views3.<locals>.gen_simple_view.<locals>.<genexpr> at 0x10d7f5430>]
    show_template =  'appbuilder/general/model/show_cascade.html'
    list_template = 'appbuilder/general/model/list.html'
    add_template = 'appbuilder/general/model/add.html'
    edit_template = 'appbuilder/general/model/edit.html'
    list_widget= 'list_widget'
    show_widget = 'show_widget'
    add_widget = 'add_widget'
    edit_widget=  'edit_widget'


# MASTERVIEW
class PortalMasterView(MasterDetailView):
    datamodel = SQLAInterface(Portal)
    related_views = [IndividualDetailView]
    list_columns = ['id', 'portal_url', 'is_primary', 'portal_state', 'individual', 'has_custom_domain', 'domain', 'header_text', 'slug', 'automatic_fulfillment_digital_products', 'default_digital_max_downloads', 'default_digital_url_valid_days', 'default_mail_sender_name', 'default_mail_sender_address', 'fulfillment_auto_approve', 'fulfillment_allow_unpaid', 'reserve_stock_duration_anonymous_user', 'reserve_stock_duration_authenticated_user', 'limit_quantity_per_checkout', 'gift_card_expiry_type', 'gift_card_expiry_period_type', 'gift_card_expiry_period', 'charge_taxes_on_shipping', 'include_taxes_in_prices', 'display_gross_prices', 'language']
    show_columns = ['id', 'portal_url', 'is_primary', 'portal_state', 'individual', 'has_custom_domain', 'domain', 'header_text', 'slug', 'automatic_fulfillment_digital_products', 'default_digital_max_downloads', 'default_digital_url_valid_days', 'default_mail_sender_name', 'default_mail_sender_address', 'fulfillment_auto_approve', 'fulfillment_allow_unpaid', 'reserve_stock_duration_anonymous_user', 'reserve_stock_duration_authenticated_user', 'limit_quantity_per_checkout', 'gift_card_expiry_type', 'gift_card_expiry_period_type', 'gift_card_expiry_period', 'charge_taxes_on_shipping', 'include_taxes_in_prices', 'display_gross_prices', 'language']
    search_columns = ['id', 'portal_url', 'is_primary', 'portal_state', 'individual', 'has_custom_domain', 'domain', 'header_text', 'slug', 'automatic_fulfillment_digital_products', 'default_digital_max_downloads', 'default_digital_url_valid_days', 'default_mail_sender_name', 'default_mail_sender_address', 'fulfillment_auto_approve', 'fulfillment_allow_unpaid', 'reserve_stock_duration_anonymous_user', 'reserve_stock_duration_authenticated_user', 'limit_quantity_per_checkout', 'gift_card_expiry_type', 'gift_card_expiry_period_type', 'gift_card_expiry_period', 'charge_taxes_on_shipping', 'include_taxes_in_prices', 'display_gross_prices', 'language']
    default_view = 'list'

# SIMPLEVIEW
class PageView(ModelView):
    datamodel=SQLAInterface(Page, db.session)
    related_views = []
    base_permissions = ['can_list', 'can_show', 'can_edit', 'can_delete', 'can_add']
    search_exclude_columns= []
    search_columns = ['id', 'portal', 'header', 'slug', 'page_type']
    default_sort = [('id', True)]
    list_title= 'Page List'
    show_title='Page Detail'
    add_title ='Add Page'
    edit_title = 'Edit Page'
#    label_columns=  [{column.name: column.name} for column in table.columns]
    list_columns = ['id', 'portal', 'header', 'slug', 'page_type']
    add_columns= ['id', 'portal', 'header', 'slug', 'page_type']
    edit_columns = ['id', 'portal', 'header', 'slug', 'page_type']
    show_columns = ['id', 'portal', 'header', 'slug', 'page_type']
#    description_columns = [<generator object gen_views3.<locals>.gen_simple_view.<locals>.<genexpr> at 0x10d7f5430>]
#    description_columns_editable = [<generator object gen_views3.<locals>.gen_simple_view.<locals>.<genexpr> at 0x10d7f5430>]
    show_template =  'appbuilder/general/model/show_cascade.html'
    list_template = 'appbuilder/general/model/list.html'
    add_template = 'appbuilder/general/model/add.html'
    edit_template = 'appbuilder/general/model/edit.html'
    list_widget= 'list_widget'
    show_widget = 'show_widget'
    add_widget = 'add_widget'
    edit_widget=  'edit_widget'


# MASTERVIEW
class PageMasterView(MasterDetailView):
    datamodel = SQLAInterface(Page)
    related_views = [PortalDetailView]
    list_columns = ['id', 'portal', 'header', 'slug', 'page_type']
    show_columns = ['id', 'portal', 'header', 'slug', 'page_type']
    search_columns = ['id', 'portal', 'header', 'slug', 'page_type']
    default_view = 'list'

# SIMPLEVIEW
class ProfileView(ModelView):
    datamodel=SQLAInterface(Profile, db.session)
    related_views = []
    base_permissions = ['can_list', 'can_show', 'can_edit', 'can_delete', 'can_add']
    search_exclude_columns= []
    search_columns = ['id', 'individual', 'import_address', 'profile_username', 'profile_password', 'has_been_imported', 'import_data', 'import_date', 'profilesource']
    default_sort = [('id', True)]
    list_title= 'Profile List'
    show_title='Profile Detail'
    add_title ='Add Profile'
    edit_title = 'Edit Profile'
#    label_columns=  [{column.name: column.name} for column in table.columns]
    list_columns = ['id', 'individual', 'import_address', 'profile_username', 'profile_password', 'has_been_imported', 'import_data', 'import_date', 'profilesource']
    add_columns= ['id', 'individual', 'import_address', 'profile_username', 'profile_password', 'has_been_imported', 'import_data', 'import_date', 'profilesource']
    edit_columns = ['id', 'individual', 'import_address', 'profile_username', 'profile_password', 'has_been_imported', 'import_data', 'import_date', 'profilesource']
    show_columns = ['id', 'individual', 'import_address', 'profile_username', 'profile_password', 'has_been_imported', 'import_data', 'import_date', 'profilesource']
#    description_columns = [<generator object gen_views3.<locals>.gen_simple_view.<locals>.<genexpr> at 0x10d7f5430>]
#    description_columns_editable = [<generator object gen_views3.<locals>.gen_simple_view.<locals>.<genexpr> at 0x10d7f5430>]
    show_template =  'appbuilder/general/model/show_cascade.html'
    list_template = 'appbuilder/general/model/list.html'
    add_template = 'appbuilder/general/model/add.html'
    edit_template = 'appbuilder/general/model/edit.html'
    list_widget= 'list_widget'
    show_widget = 'show_widget'
    add_widget = 'add_widget'
    edit_widget=  'edit_widget'


# MASTERVIEW
class ProfileMultiView(MultipleView):
    datamodel = SQLAInterface(Profile)
    views = [IndividualDetailView, ProfilesourceDetailView]
    list_columns = ['id', 'individual', 'import_address', 'profile_username', 'profile_password', 'has_been_imported', 'import_data', 'import_date', 'profilesource']
    show_columns = ['id', 'individual', 'import_address', 'profile_username', 'profile_password', 'has_been_imported', 'import_data', 'import_date', 'profilesource']
    search_columns = ['id', 'individual', 'import_address', 'profile_username', 'profile_password', 'has_been_imported', 'import_data', 'import_date', 'profilesource']
    default_view = 'list'

# SIMPLEVIEW
class ResumeView(ModelView):
    datamodel=SQLAInterface(Resume, db.session)
    related_views = []
    base_permissions = ['can_list', 'can_show', 'can_edit', 'can_delete', 'can_add']
    search_exclude_columns= []
    search_columns = ['id', 'individual', 'template', 'header', 'color', 'location', 'summary_text', 'has_been_generated', 'preferred']
    default_sort = [('id', True)]
    list_title= 'Resume List'
    show_title='Resume Detail'
    add_title ='Add Resume'
    edit_title = 'Edit Resume'
#    label_columns=  [{column.name: column.name} for column in table.columns]
    list_columns = ['id', 'individual', 'template', 'header', 'color', 'location', 'summary_text', 'has_been_generated', 'preferred']
    add_columns= ['id', 'individual', 'template', 'header', 'color', 'location', 'summary_text', 'has_been_generated', 'preferred']
    edit_columns = ['id', 'individual', 'template', 'header', 'color', 'location', 'summary_text', 'has_been_generated', 'preferred']
    show_columns = ['id', 'individual', 'template', 'header', 'color', 'location', 'summary_text', 'has_been_generated', 'preferred']
#    description_columns = [<generator object gen_views3.<locals>.gen_simple_view.<locals>.<genexpr> at 0x10d7f5430>]
#    description_columns_editable = [<generator object gen_views3.<locals>.gen_simple_view.<locals>.<genexpr> at 0x10d7f5430>]
    show_template =  'appbuilder/general/model/show_cascade.html'
    list_template = 'appbuilder/general/model/list.html'
    add_template = 'appbuilder/general/model/add.html'
    edit_template = 'appbuilder/general/model/edit.html'
    list_widget= 'list_widget'
    show_widget = 'show_widget'
    add_widget = 'add_widget'
    edit_widget=  'edit_widget'


# MASTERVIEW
class ResumeMultiView(MultipleView):
    datamodel = SQLAInterface(Resume)
    views = [IndividualDetailView, LocationDetailView]
    list_columns = ['id', 'individual', 'template', 'header', 'color', 'location', 'summary_text', 'has_been_generated', 'preferred']
    show_columns = ['id', 'individual', 'template', 'header', 'color', 'location', 'summary_text', 'has_been_generated', 'preferred']
    search_columns = ['id', 'individual', 'template', 'header', 'color', 'location', 'summary_text', 'has_been_generated', 'preferred']
    default_view = 'list'

# SIMPLEVIEW
class SwarmView(ModelView):
    datamodel=SQLAInterface(Swarm, db.session)
    related_views = []
    base_permissions = ['can_list', 'can_show', 'can_edit', 'can_delete', 'can_add']
    search_exclude_columns= []
    search_columns = ['id', 'portal']
    default_sort = [('id', True)]
    list_title= 'Swarm List'
    show_title='Swarm Detail'
    add_title ='Add Swarm'
    edit_title = 'Edit Swarm'
#    label_columns=  [{column.name: column.name} for column in table.columns]
    list_columns = ['id', 'portal']
    add_columns= ['id', 'portal']
    edit_columns = ['id', 'portal']
    show_columns = ['id', 'portal']
#    description_columns = [<generator object gen_views3.<locals>.gen_simple_view.<locals>.<genexpr> at 0x10d7f5430>]
#    description_columns_editable = [<generator object gen_views3.<locals>.gen_simple_view.<locals>.<genexpr> at 0x10d7f5430>]
    show_template =  'appbuilder/general/model/show_cascade.html'
    list_template = 'appbuilder/general/model/list.html'
    add_template = 'appbuilder/general/model/add.html'
    edit_template = 'appbuilder/general/model/edit.html'
    list_widget= 'list_widget'
    show_widget = 'show_widget'
    add_widget = 'add_widget'
    edit_widget=  'edit_widget'


# MASTERVIEW
class SwarmMasterView(MasterDetailView):
    datamodel = SQLAInterface(Swarm)
    related_views = [PortalDetailView]
    list_columns = ['id', 'portal']
    show_columns = ['id', 'portal']
    search_columns = ['id', 'portal']
    default_view = 'list'

# SIMPLEVIEW
class IndividualSwarmView(ModelView):
    datamodel=SQLAInterface(IndividualSwarm, db.session)
    related_views = []
    base_permissions = ['can_list', 'can_show', 'can_edit', 'can_delete', 'can_add']
    search_exclude_columns= []
    search_columns = ['individual', 'swarm']
    default_sort = [('id', True)]
    list_title= 'IndividualSwarm List'
    show_title='IndividualSwarm Detail'
    add_title ='Add IndividualSwarm'
    edit_title = 'Edit IndividualSwarm'
#    label_columns=  [{column.name: column.name} for column in table.columns]
    list_columns = ['individual', 'swarm']
    add_columns= ['individual', 'swarm']
    edit_columns = ['individual', 'swarm']
    show_columns = ['individual', 'swarm']
#    description_columns = [<generator object gen_views3.<locals>.gen_simple_view.<locals>.<genexpr> at 0x10d7f5430>]
#    description_columns_editable = [<generator object gen_views3.<locals>.gen_simple_view.<locals>.<genexpr> at 0x10d7f5430>]
    show_template =  'appbuilder/general/model/show_cascade.html'
    list_template = 'appbuilder/general/model/list.html'
    add_template = 'appbuilder/general/model/add.html'
    edit_template = 'appbuilder/general/model/edit.html'
    list_widget= 'list_widget'
    show_widget = 'show_widget'
    add_widget = 'add_widget'
    edit_widget=  'edit_widget'


# MASTERVIEW
class IndividualSwarmMultiView(MultipleView):
    datamodel = SQLAInterface(IndividualSwarm)
    views = [IndividualDetailView, SwarmDetailView]
    list_columns = ['individual', 'swarm']
    show_columns = ['individual', 'swarm']
    search_columns = ['individual', 'swarm']
    default_view = 'list'

# SIMPLEVIEW
class UserSkillView(ModelView):
    datamodel=SQLAInterface(UserSkill, db.session)
    related_views = []
    base_permissions = ['can_list', 'can_show', 'can_edit', 'can_delete', 'can_add']
    search_exclude_columns= []
    search_columns = ['skills', 'user_details']
    default_sort = [('id', True)]
    list_title= 'UserSkill List'
    show_title='UserSkill Detail'
    add_title ='Add UserSkill'
    edit_title = 'Edit UserSkill'
#    label_columns=  [{column.name: column.name} for column in table.columns]
    list_columns = ['skills', 'user_details']
    add_columns= ['skills', 'user_details']
    edit_columns = ['skills', 'user_details']
    show_columns = ['skills', 'user_details']
#    description_columns = [<generator object gen_views3.<locals>.gen_simple_view.<locals>.<genexpr> at 0x10d7f5430>]
#    description_columns_editable = [<generator object gen_views3.<locals>.gen_simple_view.<locals>.<genexpr> at 0x10d7f5430>]
    show_template =  'appbuilder/general/model/show_cascade.html'
    list_template = 'appbuilder/general/model/list.html'
    add_template = 'appbuilder/general/model/add.html'
    edit_template = 'appbuilder/general/model/edit.html'
    list_widget= 'list_widget'
    show_widget = 'show_widget'
    add_widget = 'add_widget'
    edit_widget=  'edit_widget'


# MASTERVIEW
class UserSkillMultiView(MultipleView):
    datamodel = SQLAInterface(UserSkill)
    views = [SkillDetailView, IndividualDetailView]
    list_columns = ['skills', 'user_details']
    show_columns = ['skills', 'user_details']
    search_columns = ['skills', 'user_details']
    default_view = 'list'

# SIMPLEVIEW
class WorkHistoryView(ModelView):
    datamodel=SQLAInterface(WorkHistory, db.session)
    related_views = []
    base_permissions = ['can_list', 'can_show', 'can_edit', 'can_delete', 'can_add']
    search_exclude_columns= []
    search_columns = ['id', 'individual', 'resume']
    default_sort = [('id', True)]
    list_title= 'WorkHistory List'
    show_title='WorkHistory Detail'
    add_title ='Add WorkHistory'
    edit_title = 'Edit WorkHistory'
#    label_columns=  [{column.name: column.name} for column in table.columns]
    list_columns = ['id', 'individual', 'resume']
    add_columns= ['id', 'individual', 'resume']
    edit_columns = ['id', 'individual', 'resume']
    show_columns = ['id', 'individual', 'resume']
#    description_columns = [<generator object gen_views3.<locals>.gen_simple_view.<locals>.<genexpr> at 0x10d7f5430>]
#    description_columns_editable = [<generator object gen_views3.<locals>.gen_simple_view.<locals>.<genexpr> at 0x10d7f5430>]
    show_template =  'appbuilder/general/model/show_cascade.html'
    list_template = 'appbuilder/general/model/list.html'
    add_template = 'appbuilder/general/model/add.html'
    edit_template = 'appbuilder/general/model/edit.html'
    list_widget= 'list_widget'
    show_widget = 'show_widget'
    add_widget = 'add_widget'
    edit_widget=  'edit_widget'


# MASTERVIEW
class WorkHistoryMultiView(MultipleView):
    datamodel = SQLAInterface(WorkHistory)
    views = [IndividualDetailView, ResumeDetailView]
    list_columns = ['id', 'individual', 'resume']
    show_columns = ['id', 'individual', 'resume']
    search_columns = ['id', 'individual', 'resume']
    default_view = 'list'

# REGVIEWS
appbuilder.add_view_no_menu(UserxDetailView, 'userxdetailview')
appbuilder.add_view_no_menu(ResumeDetailView, 'resumedetailview')
appbuilder.add_view_no_menu(SwarmDetailView, 'swarmdetailview')
appbuilder.add_view_no_menu(IndividualDetailView, 'individualdetailview')
appbuilder.add_view_no_menu(PortalDetailView, 'portaldetailview')
appbuilder.add_view_no_menu(LocationDetailView, 'locationdetailview')
appbuilder.add_view_no_menu(ProfilesourceDetailView, 'profilesourcedetailview')
appbuilder.add_view_no_menu(JobDetailView, 'jobdetailview')
appbuilder.add_view_no_menu(IndustryDetailView, 'industrydetailview')
appbuilder.add_view_no_menu(SkillDetailView, 'skilldetailview')
appbuilder.add_view(WorkHistoryMultiView, 'workhistorymultiview', category='Overview')
appbuilder.add_view(JobSkillMultiView, 'jobskillmultiview', category='Overview')
appbuilder.add_view(EducationMasterView, 'educationmasterview', category='Overview')
appbuilder.add_view(LocationMasterView, 'locationmasterview', category='Overview')
appbuilder.add_view(IndividualJobMultiView, 'individualjobmultiview', category='Overview')
appbuilder.add_view(UserxMasterView, 'userxmasterview', category='Overview')
appbuilder.add_view(SkillMasterView, 'skillmasterview', category='Overview')
appbuilder.add_view(ProfileMultiView, 'profilemultiview', category='Overview')
appbuilder.add_view(IndustryMasterView, 'industrymasterview', category='Overview')
appbuilder.add_view(ResumeMultiView, 'resumemultiview', category='Overview')
appbuilder.add_view(IndividualMasterView, 'individualmasterview', category='Overview')
appbuilder.add_view(SwarmMasterView, 'swarmmasterview', category='Overview')
appbuilder.add_view(PageMasterView, 'pagemasterview', category='Overview')
appbuilder.add_view(JobMasterView, 'jobmasterview', category='Overview')
appbuilder.add_view(PortalMasterView, 'portalmasterview', category='Overview')
appbuilder.add_view(IndustryJobMultiView, 'industryjobmultiview', category='Overview')
appbuilder.add_view(IndividualSwarmMultiView, 'individualswarmmultiview', category='Overview')
appbuilder.add_view(UserSkillMultiView, 'userskillmultiview', category='Overview')
appbuilder.add_view(ProfilesourceMasterView, 'profilesourcemasterview', category='Overview')
appbuilder.add_view(IndividualJobView, 'individualjobview', category='Setup')
appbuilder.add_view(ProfilesourceView, 'profilesourceview', category='Setup')
appbuilder.add_view(PortalView, 'portalview', category='Setup')
appbuilder.add_view(SwarmView, 'swarmview', category='Setup')
appbuilder.add_view(ProfileView, 'profileview', category='Setup')
appbuilder.add_view(IndustryView, 'industryview', category='Setup')
appbuilder.add_view(IndividualView, 'individualview', category='Setup')
appbuilder.add_view(SkillView, 'skillview', category='Setup')
appbuilder.add_view(PageView, 'pageview', category='Setup')
appbuilder.add_view(IndustryJobView, 'industryjobview', category='Setup')
appbuilder.add_view(WorkHistoryView, 'workhistoryview', category='Setup')
appbuilder.add_view(UserSkillView, 'userskillview', category='Setup')
appbuilder.add_view(UserxView, 'userxview', category='Setup')
appbuilder.add_view(JobView, 'jobview', category='Setup')
appbuilder.add_view(ResumeView, 'resumeview', category='Setup')
appbuilder.add_view(LocationView, 'locationview', category='Setup')
appbuilder.add_view(EducationView, 'educationview', category='Setup')
appbuilder.add_view(IndividualSwarmView, 'individualswarmview', category='Setup')
appbuilder.add_view(JobSkillView, 'jobskillview', category='Setup')

appbuilder.add_link("rest_api", href="/swagger/v1", icon="fa-sliders", label="REST Api", category="Utilities")
appbuilder.add_link("graphql", href="/graphql", icon="fa-wrench", label="GraphQL", category="Utilities")

#appbuilder.add_separator("Setup")
#appbuilder.add_separator("My Views")
#appbuilder.add_link(name, href, icon='', label='', category='', category_icon='', category_label='', baseview=None)

'''
     Application wide 404 error handler
'''
 
@appbuilder.app.errorhandler(404)
def page_not_found(e):
    return (
        render_template(
           "404.html", base_template=appbuilder.base_template, appbuilder=appbuilder
        ),
        404,
     )


db.create_all()
