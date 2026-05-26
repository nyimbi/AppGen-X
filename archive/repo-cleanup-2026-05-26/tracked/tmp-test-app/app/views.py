
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

from . import appbuilder, db

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

class UserxView(ModelView):
    datamodel=SQLAInterface(Userx, db.session)
    related_views = []
    show_title='Userx Detail'
    add_title ='Add Userx'
    list_title= 'Userx List'
    edit_title = 'Edit Userx'
    show_columns = ['id']
#    show_exclude_columns = [] #= ['id']
#
#    add_columns = ['id']
#    add_exclude_columns = [hide_list] #['id']
#
#    edit_columns = ['id']
#    edit_exclude_columns =[hide_list] # ['id']
#
#    list_columns = ['id']
#    list_exclude_columns = [] # ['id']
#
#    search_columns = ['id']
#    search_exclude_columns= [] # ['id']
#
#    default_sort = [('id', True)]
#    base_permissions = ['can_list', 'can_show', 'can_edit', 'can_delete', 'can_add']
#    label_columns=   [{column.name: column.name for column in table.columns} ]
#    show_template =  'appbuilder/general/model/show_cascade.html'
#    list_template = 'appbuilder/general/model/list.html'
#    add_template = 'appbuilder/general/model/add.html'
#    edit_template = 'appbuilder/general/model/edit.html'
#    add_widget = (FormVerticalWidget|FormInlineWidget)
#    show_widget = ShowBlockWidget
#    list_widget = (ListThumbnail|ListWidget)
#    base_order = ('name', 'asc')
#    list_widget= 'list_widget'


class IndividualView(ModelView):
    datamodel=SQLAInterface(Individual, db.session)
    related_views = []
    show_title='Individual Detail'
    add_title ='Add Individual'
    list_title= 'Individual List'
    edit_title = 'Edit Individual'
    show_columns = ['id', 'userx', 'is_individual', 'is_institution', 'is_company', 'is_government', 'is_online']
#    show_exclude_columns = [] #= ['id', 'userx', 'is_individual', 'is_institution', 'is_company', 'is_government', 'is_online']
#
#    add_columns = ['id', 'userx', 'is_individual', 'is_institution', 'is_company', 'is_government', 'is_online']
#    add_exclude_columns = [hide_list] #['id', 'userx', 'is_individual', 'is_institution', 'is_company', 'is_government', 'is_online']
#
#    edit_columns = ['id', 'userx', 'is_individual', 'is_institution', 'is_company', 'is_government', 'is_online']
#    edit_exclude_columns =[hide_list] # ['id', 'userx', 'is_individual', 'is_institution', 'is_company', 'is_government', 'is_online']
#
#    list_columns = ['id', 'userx', 'is_individual', 'is_institution', 'is_company', 'is_government', 'is_online']
#    list_exclude_columns = [] # ['id', 'userx', 'is_individual', 'is_institution', 'is_company', 'is_government', 'is_online']
#
#    search_columns = ['id', 'userx', 'is_individual', 'is_institution', 'is_company', 'is_government', 'is_online']
#    search_exclude_columns= [] # ['id', 'userx', 'is_individual', 'is_institution', 'is_company', 'is_government', 'is_online']
#
#    default_sort = [('id', True)]
#    base_permissions = ['can_list', 'can_show', 'can_edit', 'can_delete', 'can_add']
#    label_columns=   [{column.name: column.name for column in table.columns} ]
#    show_template =  'appbuilder/general/model/show_cascade.html'
#    list_template = 'appbuilder/general/model/list.html'
#    add_template = 'appbuilder/general/model/add.html'
#    edit_template = 'appbuilder/general/model/edit.html'
#    add_widget = (FormVerticalWidget|FormInlineWidget)
#    show_widget = ShowBlockWidget
#    list_widget = (ListThumbnail|ListWidget)
#    base_order = ('name', 'asc')
#    list_widget= 'list_widget'


class UserxDetailView(ModelView):
    datamodel=SQLAInterface(Userx, db.session)
    related_views = []
    show_title='Userx Detail'
    add_title ='Add Userx'
    list_title= 'Userx List'
    edit_title = 'Edit Userx'
    show_columns = ['id', 'userx', 'is_individual', 'is_institution', 'is_company', 'is_government', 'is_online']
#    show_exclude_columns = [] #= ['id', 'userx', 'is_individual', 'is_institution', 'is_company', 'is_government', 'is_online']
#
#    add_columns = ['id', 'userx', 'is_individual', 'is_institution', 'is_company', 'is_government', 'is_online']
#    add_exclude_columns = [hide_list] #['id', 'userx', 'is_individual', 'is_institution', 'is_company', 'is_government', 'is_online']
#
#    edit_columns = ['id', 'userx', 'is_individual', 'is_institution', 'is_company', 'is_government', 'is_online']
#    edit_exclude_columns =[hide_list] # ['id', 'userx', 'is_individual', 'is_institution', 'is_company', 'is_government', 'is_online']
#
#    list_columns = ['id', 'userx', 'is_individual', 'is_institution', 'is_company', 'is_government', 'is_online']
#    list_exclude_columns = [] # ['id', 'userx', 'is_individual', 'is_institution', 'is_company', 'is_government', 'is_online']
#
#    search_columns = ['id', 'userx', 'is_individual', 'is_institution', 'is_company', 'is_government', 'is_online']
#    search_exclude_columns= [] # ['id', 'userx', 'is_individual', 'is_institution', 'is_company', 'is_government', 'is_online']
#
#    default_sort = [('id', True)]
#    base_permissions = ['can_list', 'can_show', 'can_edit', 'can_delete', 'can_add']
#    label_columns=   [{column.name: column.name for column in table.columns} ]
#    show_template =  'appbuilder/general/model/show_cascade.html'
#    list_template = 'appbuilder/general/model/list.html'
#    add_template = 'appbuilder/general/model/add.html'
#    edit_template = 'appbuilder/general/model/edit.html'
#    add_widget = (FormVerticalWidget|FormInlineWidget)
#    show_widget = ShowBlockWidget
#    list_widget = (ListThumbnail|ListWidget)
#    base_order = ('name', 'asc')
#    list_widget= 'list_widget'


class IndividualDetailView(ModelView):
    datamodel=SQLAInterface(Individual, db.session)
    related_views = []
    show_title='Individual Detail'
    add_title ='Add Individual'
    list_title= 'Individual List'
    edit_title = 'Edit Individual'
    show_columns = ['id', 'userx', 'is_individual', 'is_institution', 'is_company', 'is_government', 'is_online']
#    show_exclude_columns = [] #= ['id', 'userx', 'is_individual', 'is_institution', 'is_company', 'is_government', 'is_online']
#
#    add_columns = ['id', 'userx', 'is_individual', 'is_institution', 'is_company', 'is_government', 'is_online']
#    add_exclude_columns = [hide_list] #['id', 'userx', 'is_individual', 'is_institution', 'is_company', 'is_government', 'is_online']
#
#    edit_columns = ['id', 'userx', 'is_individual', 'is_institution', 'is_company', 'is_government', 'is_online']
#    edit_exclude_columns =[hide_list] # ['id', 'userx', 'is_individual', 'is_institution', 'is_company', 'is_government', 'is_online']
#
#    list_columns = ['id', 'userx', 'is_individual', 'is_institution', 'is_company', 'is_government', 'is_online']
#    list_exclude_columns = [] # ['id', 'userx', 'is_individual', 'is_institution', 'is_company', 'is_government', 'is_online']
#
#    search_columns = ['id', 'userx', 'is_individual', 'is_institution', 'is_company', 'is_government', 'is_online']
#    search_exclude_columns= [] # ['id', 'userx', 'is_individual', 'is_institution', 'is_company', 'is_government', 'is_online']
#
#    default_sort = [('id', True)]
#    base_permissions = ['can_list', 'can_show', 'can_edit', 'can_delete', 'can_add']
#    label_columns=   [{column.name: column.name for column in table.columns} ]
#    show_template =  'appbuilder/general/model/show_cascade.html'
#    list_template = 'appbuilder/general/model/list.html'
#    add_template = 'appbuilder/general/model/add.html'
#    edit_template = 'appbuilder/general/model/edit.html'
#    add_widget = (FormVerticalWidget|FormInlineWidget)
#    show_widget = ShowBlockWidget
#    list_widget = (ListThumbnail|ListWidget)
#    base_order = ('name', 'asc')
#    list_widget= 'list_widget'


class IndividualMasterView(MasterDetailView):
    datamodel=SQLAInterface(Individual, db.session)
    related_views = [UserxDetailView]
    show_title='Individual Detail'
    add_title ='Add Individual'
    list_title= 'Individual List'
    edit_title = 'Edit Individual'
    show_columns = ['id', 'userx', 'is_individual', 'is_institution', 'is_company', 'is_government', 'is_online']
#    show_exclude_columns = [] #= ['id', 'userx', 'is_individual', 'is_institution', 'is_company', 'is_government', 'is_online']
#
#    add_columns = ['id', 'userx', 'is_individual', 'is_institution', 'is_company', 'is_government', 'is_online']
#    add_exclude_columns = [hide_list] #['id', 'userx', 'is_individual', 'is_institution', 'is_company', 'is_government', 'is_online']
#
#    edit_columns = ['id', 'userx', 'is_individual', 'is_institution', 'is_company', 'is_government', 'is_online']
#    edit_exclude_columns =[hide_list] # ['id', 'userx', 'is_individual', 'is_institution', 'is_company', 'is_government', 'is_online']
#
#    list_columns = ['id', 'userx', 'is_individual', 'is_institution', 'is_company', 'is_government', 'is_online']
#    list_exclude_columns = [] # ['id', 'userx', 'is_individual', 'is_institution', 'is_company', 'is_government', 'is_online']
#
#    search_columns = ['id', 'userx', 'is_individual', 'is_institution', 'is_company', 'is_government', 'is_online']
#    search_exclude_columns= [] # ['id', 'userx', 'is_individual', 'is_institution', 'is_company', 'is_government', 'is_online']
#
#    default_sort = [('id', True)]
#    base_permissions = ['can_list', 'can_show', 'can_edit', 'can_delete', 'can_add']
#    label_columns=   [{column.name: column.name for column in table.columns} ]
#    show_template =  'appbuilder/general/model/show_cascade.html'
#    list_template = 'appbuilder/general/model/list.html'
#    add_template = 'appbuilder/general/model/add.html'
#    edit_template = 'appbuilder/general/model/edit.html'
#    add_widget = (FormVerticalWidget|FormInlineWidget)
#    show_widget = ShowBlockWidget
#    list_widget = (ListThumbnail|ListWidget)
#    base_order = ('name', 'asc')
#    list_widget= 'list_widget'


class IndustryView(ModelView):
    datamodel=SQLAInterface(Industry, db.session)
    related_views = []
    show_title='Industry Detail'
    add_title ='Add Industry'
    list_title= 'Industry List'
    edit_title = 'Edit Industry'
    show_columns = ['id', 'industry_code']
#    show_exclude_columns = [] #= ['id', 'industry_code']
#
#    add_columns = ['id', 'industry_code']
#    add_exclude_columns = [hide_list] #['id', 'industry_code']
#
#    edit_columns = ['id', 'industry_code']
#    edit_exclude_columns =[hide_list] # ['id', 'industry_code']
#
#    list_columns = ['id', 'industry_code']
#    list_exclude_columns = [] # ['id', 'industry_code']
#
#    search_columns = ['id', 'industry_code']
#    search_exclude_columns= [] # ['id', 'industry_code']
#
#    default_sort = [('id', True)]
#    base_permissions = ['can_list', 'can_show', 'can_edit', 'can_delete', 'can_add']
#    label_columns=   [{column.name: column.name for column in table.columns} ]
#    show_template =  'appbuilder/general/model/show_cascade.html'
#    list_template = 'appbuilder/general/model/list.html'
#    add_template = 'appbuilder/general/model/add.html'
#    edit_template = 'appbuilder/general/model/edit.html'
#    add_widget = (FormVerticalWidget|FormInlineWidget)
#    show_widget = ShowBlockWidget
#    list_widget = (ListThumbnail|ListWidget)
#    base_order = ('name', 'asc')
#    list_widget= 'list_widget'


class IndustryJobView(ModelView):
    datamodel=SQLAInterface(IndustryJob, db.session)
    related_views = []
    show_title='IndustryJob Detail'
    add_title ='Add IndustryJob'
    list_title= 'IndustryJob List'
    edit_title = 'Edit IndustryJob'
    show_columns = ['industry', 'job']
#    show_exclude_columns = [] #= ['industry', 'job']
#
#    add_columns = ['industry', 'job']
#    add_exclude_columns = [hide_list] #['industry', 'job']
#
#    edit_columns = ['industry', 'job']
#    edit_exclude_columns =[hide_list] # ['industry', 'job']
#
#    list_columns = ['industry', 'job']
#    list_exclude_columns = [] # ['industry', 'job']
#
#    search_columns = ['industry', 'job']
#    search_exclude_columns= [] # ['industry', 'job']
#
#    default_sort = [('id', True)]
#    base_permissions = ['can_list', 'can_show', 'can_edit', 'can_delete', 'can_add']
#    label_columns=   [{column.name: column.name for column in table.columns} ]
#    show_template =  'appbuilder/general/model/show_cascade.html'
#    list_template = 'appbuilder/general/model/list.html'
#    add_template = 'appbuilder/general/model/add.html'
#    edit_template = 'appbuilder/general/model/edit.html'
#    add_widget = (FormVerticalWidget|FormInlineWidget)
#    show_widget = ShowBlockWidget
#    list_widget = (ListThumbnail|ListWidget)
#    base_order = ('name', 'asc')
#    list_widget= 'list_widget'


class UserxDetailView(ModelView):
    datamodel=SQLAInterface(Userx, db.session)
    related_views = []
    show_title='Userx Detail'
    add_title ='Add Userx'
    list_title= 'Userx List'
    edit_title = 'Edit Userx'
    show_columns = ['id', 'userx', 'is_individual', 'is_institution', 'is_company', 'is_government', 'is_online']
#    show_exclude_columns = [] #= ['id', 'userx', 'is_individual', 'is_institution', 'is_company', 'is_government', 'is_online']
#
#    add_columns = ['id', 'userx', 'is_individual', 'is_institution', 'is_company', 'is_government', 'is_online']
#    add_exclude_columns = [hide_list] #['id', 'userx', 'is_individual', 'is_institution', 'is_company', 'is_government', 'is_online']
#
#    edit_columns = ['id', 'userx', 'is_individual', 'is_institution', 'is_company', 'is_government', 'is_online']
#    edit_exclude_columns =[hide_list] # ['id', 'userx', 'is_individual', 'is_institution', 'is_company', 'is_government', 'is_online']
#
#    list_columns = ['id', 'userx', 'is_individual', 'is_institution', 'is_company', 'is_government', 'is_online']
#    list_exclude_columns = [] # ['id', 'userx', 'is_individual', 'is_institution', 'is_company', 'is_government', 'is_online']
#
#    search_columns = ['id', 'userx', 'is_individual', 'is_institution', 'is_company', 'is_government', 'is_online']
#    search_exclude_columns= [] # ['id', 'userx', 'is_individual', 'is_institution', 'is_company', 'is_government', 'is_online']
#
#    default_sort = [('id', True)]
#    base_permissions = ['can_list', 'can_show', 'can_edit', 'can_delete', 'can_add']
#    label_columns=   [{column.name: column.name for column in table.columns} ]
#    show_template =  'appbuilder/general/model/show_cascade.html'
#    list_template = 'appbuilder/general/model/list.html'
#    add_template = 'appbuilder/general/model/add.html'
#    edit_template = 'appbuilder/general/model/edit.html'
#    add_widget = (FormVerticalWidget|FormInlineWidget)
#    show_widget = ShowBlockWidget
#    list_widget = (ListThumbnail|ListWidget)
#    base_order = ('name', 'asc')
#    list_widget= 'list_widget'


class IndividualDetailView(ModelView):
    datamodel=SQLAInterface(Individual, db.session)
    related_views = []
    show_title='Individual Detail'
    add_title ='Add Individual'
    list_title= 'Individual List'
    edit_title = 'Edit Individual'
    show_columns = ['id', 'userx', 'is_individual', 'is_institution', 'is_company', 'is_government', 'is_online']
#    show_exclude_columns = [] #= ['id', 'userx', 'is_individual', 'is_institution', 'is_company', 'is_government', 'is_online']
#
#    add_columns = ['id', 'userx', 'is_individual', 'is_institution', 'is_company', 'is_government', 'is_online']
#    add_exclude_columns = [hide_list] #['id', 'userx', 'is_individual', 'is_institution', 'is_company', 'is_government', 'is_online']
#
#    edit_columns = ['id', 'userx', 'is_individual', 'is_institution', 'is_company', 'is_government', 'is_online']
#    edit_exclude_columns =[hide_list] # ['id', 'userx', 'is_individual', 'is_institution', 'is_company', 'is_government', 'is_online']
#
#    list_columns = ['id', 'userx', 'is_individual', 'is_institution', 'is_company', 'is_government', 'is_online']
#    list_exclude_columns = [] # ['id', 'userx', 'is_individual', 'is_institution', 'is_company', 'is_government', 'is_online']
#
#    search_columns = ['id', 'userx', 'is_individual', 'is_institution', 'is_company', 'is_government', 'is_online']
#    search_exclude_columns= [] # ['id', 'userx', 'is_individual', 'is_institution', 'is_company', 'is_government', 'is_online']
#
#    default_sort = [('id', True)]
#    base_permissions = ['can_list', 'can_show', 'can_edit', 'can_delete', 'can_add']
#    label_columns=   [{column.name: column.name for column in table.columns} ]
#    show_template =  'appbuilder/general/model/show_cascade.html'
#    list_template = 'appbuilder/general/model/list.html'
#    add_template = 'appbuilder/general/model/add.html'
#    edit_template = 'appbuilder/general/model/edit.html'
#    add_widget = (FormVerticalWidget|FormInlineWidget)
#    show_widget = ShowBlockWidget
#    list_widget = (ListThumbnail|ListWidget)
#    base_order = ('name', 'asc')
#    list_widget= 'list_widget'


class IndustryDetailView(ModelView):
    datamodel=SQLAInterface(Industry, db.session)
    related_views = []
    show_title='Industry Detail'
    add_title ='Add Industry'
    list_title= 'Industry List'
    edit_title = 'Edit Industry'
    show_columns = ['industry', 'job']
#    show_exclude_columns = [] #= ['industry', 'job']
#
#    add_columns = ['industry', 'job']
#    add_exclude_columns = [hide_list] #['industry', 'job']
#
#    edit_columns = ['industry', 'job']
#    edit_exclude_columns =[hide_list] # ['industry', 'job']
#
#    list_columns = ['industry', 'job']
#    list_exclude_columns = [] # ['industry', 'job']
#
#    search_columns = ['industry', 'job']
#    search_exclude_columns= [] # ['industry', 'job']
#
#    default_sort = [('id', True)]
#    base_permissions = ['can_list', 'can_show', 'can_edit', 'can_delete', 'can_add']
#    label_columns=   [{column.name: column.name for column in table.columns} ]
#    show_template =  'appbuilder/general/model/show_cascade.html'
#    list_template = 'appbuilder/general/model/list.html'
#    add_template = 'appbuilder/general/model/add.html'
#    edit_template = 'appbuilder/general/model/edit.html'
#    add_widget = (FormVerticalWidget|FormInlineWidget)
#    show_widget = ShowBlockWidget
#    list_widget = (ListThumbnail|ListWidget)
#    base_order = ('name', 'asc')
#    list_widget= 'list_widget'


class IndustryJobDetailView(ModelView):
    datamodel=SQLAInterface(IndustryJob, db.session)
    related_views = []
    show_title='IndustryJob Detail'
    add_title ='Add IndustryJob'
    list_title= 'IndustryJob List'
    edit_title = 'Edit IndustryJob'
    show_columns = ['industry', 'job']
#    show_exclude_columns = [] #= ['industry', 'job']
#
#    add_columns = ['industry', 'job']
#    add_exclude_columns = [hide_list] #['industry', 'job']
#
#    edit_columns = ['industry', 'job']
#    edit_exclude_columns =[hide_list] # ['industry', 'job']
#
#    list_columns = ['industry', 'job']
#    list_exclude_columns = [] # ['industry', 'job']
#
#    search_columns = ['industry', 'job']
#    search_exclude_columns= [] # ['industry', 'job']
#
#    default_sort = [('id', True)]
#    base_permissions = ['can_list', 'can_show', 'can_edit', 'can_delete', 'can_add']
#    label_columns=   [{column.name: column.name for column in table.columns} ]
#    show_template =  'appbuilder/general/model/show_cascade.html'
#    list_template = 'appbuilder/general/model/list.html'
#    add_template = 'appbuilder/general/model/add.html'
#    edit_template = 'appbuilder/general/model/edit.html'
#    add_widget = (FormVerticalWidget|FormInlineWidget)
#    show_widget = ShowBlockWidget
#    list_widget = (ListThumbnail|ListWidget)
#    base_order = ('name', 'asc')
#    list_widget= 'list_widget'


class JobDetailView(ModelView):
    datamodel=SQLAInterface(Job, db.session)
    related_views = []
    show_title='Job Detail'
    add_title ='Add Job'
    list_title= 'Job List'
    edit_title = 'Edit Job'
    show_columns = ['industry', 'job']
#    show_exclude_columns = [] #= ['industry', 'job']
#
#    add_columns = ['industry', 'job']
#    add_exclude_columns = [hide_list] #['industry', 'job']
#
#    edit_columns = ['industry', 'job']
#    edit_exclude_columns =[hide_list] # ['industry', 'job']
#
#    list_columns = ['industry', 'job']
#    list_exclude_columns = [] # ['industry', 'job']
#
#    search_columns = ['industry', 'job']
#    search_exclude_columns= [] # ['industry', 'job']
#
#    default_sort = [('id', True)]
#    base_permissions = ['can_list', 'can_show', 'can_edit', 'can_delete', 'can_add']
#    label_columns=   [{column.name: column.name for column in table.columns} ]
#    show_template =  'appbuilder/general/model/show_cascade.html'
#    list_template = 'appbuilder/general/model/list.html'
#    add_template = 'appbuilder/general/model/add.html'
#    edit_template = 'appbuilder/general/model/edit.html'
#    add_widget = (FormVerticalWidget|FormInlineWidget)
#    show_widget = ShowBlockWidget
#    list_widget = (ListThumbnail|ListWidget)
#    base_order = ('name', 'asc')
#    list_widget= 'list_widget'




class IndividualMasterView(MasterDetailView):
    datamodel=SQLAInterface(Individual, db.session)
    related_views = [UserxDetailView]
    show_title='Individual Detail'
    add_title ='Add Individual'
    list_title= 'Individual List'
    edit_title = 'Edit Individual'
    show_columns = ['id', 'userx', 'is_individual', 'is_institution', 'is_company', 'is_government', 'is_online']
#    show_exclude_columns = [] #= ['id', 'userx', 'is_individual', 'is_institution', 'is_company', 'is_government', 'is_online']
#
#    add_columns = ['id', 'userx', 'is_individual', 'is_institution', 'is_company', 'is_government', 'is_online']
#    add_exclude_columns = [hide_list] #['id', 'userx', 'is_individual', 'is_institution', 'is_company', 'is_government', 'is_online']
#
#    edit_columns = ['id', 'userx', 'is_individual', 'is_institution', 'is_company', 'is_government', 'is_online']
#    edit_exclude_columns =[hide_list] # ['id', 'userx', 'is_individual', 'is_institution', 'is_company', 'is_government', 'is_online']
#
#    list_columns = ['id', 'userx', 'is_individual', 'is_institution', 'is_company', 'is_government', 'is_online']
#    list_exclude_columns = [] # ['id', 'userx', 'is_individual', 'is_institution', 'is_company', 'is_government', 'is_online']
#
#    search_columns = ['id', 'userx', 'is_individual', 'is_institution', 'is_company', 'is_government', 'is_online']
#    search_exclude_columns= [] # ['id', 'userx', 'is_individual', 'is_institution', 'is_company', 'is_government', 'is_online']
#
#    default_sort = [('id', True)]
#    base_permissions = ['can_list', 'can_show', 'can_edit', 'can_delete', 'can_add']
#    label_columns=   [{column.name: column.name for column in table.columns} ]
#    show_template =  'appbuilder/general/model/show_cascade.html'
#    list_template = 'appbuilder/general/model/list.html'
#    add_template = 'appbuilder/general/model/add.html'
#    edit_template = 'appbuilder/general/model/edit.html'
#    add_widget = (FormVerticalWidget|FormInlineWidget)
#    show_widget = ShowBlockWidget
#    list_widget = (ListThumbnail|ListWidget)
#    base_order = ('name', 'asc')
#    list_widget= 'list_widget'


class IndustryJobMasterView(MasterDetailView):
    datamodel=SQLAInterface(IndustryJob, db.session)
    related_views = [IndustryDetailView]
    show_title='IndustryJob Detail'
    add_title ='Add IndustryJob'
    list_title= 'IndustryJob List'
    edit_title = 'Edit IndustryJob'
    show_columns = ['industry', 'job']
#    show_exclude_columns = [] #= ['industry', 'job']
#
#    add_columns = ['industry', 'job']
#    add_exclude_columns = [hide_list] #['industry', 'job']
#
#    edit_columns = ['industry', 'job']
#    edit_exclude_columns =[hide_list] # ['industry', 'job']
#
#    list_columns = ['industry', 'job']
#    list_exclude_columns = [] # ['industry', 'job']
#
#    search_columns = ['industry', 'job']
#    search_exclude_columns= [] # ['industry', 'job']
#
#    default_sort = [('id', True)]
#    base_permissions = ['can_list', 'can_show', 'can_edit', 'can_delete', 'can_add']
#    label_columns=   [{column.name: column.name for column in table.columns} ]
#    show_template =  'appbuilder/general/model/show_cascade.html'
#    list_template = 'appbuilder/general/model/list.html'
#    add_template = 'appbuilder/general/model/add.html'
#    edit_template = 'appbuilder/general/model/edit.html'
#    add_widget = (FormVerticalWidget|FormInlineWidget)
#    show_widget = ShowBlockWidget
#    list_widget = (ListThumbnail|ListWidget)
#    base_order = ('name', 'asc')
#    list_widget= 'list_widget'


class IndustryJobMultiView(MultipleView):
    datamodel=SQLAInterface(IndustryJob, db.session)
    views = [IndustryDetailView, JobDetailView]
    show_title='IndustryJob Detail'
    add_title ='Add IndustryJob'
    list_title= 'IndustryJob List'
    edit_title = 'Edit IndustryJob'
    show_columns = ['industry', 'job']
#    show_exclude_columns = [] #= ['industry', 'job']
#
#    add_columns = ['industry', 'job']
#    add_exclude_columns = [hide_list] #['industry', 'job']
#
#    edit_columns = ['industry', 'job']
#    edit_exclude_columns =[hide_list] # ['industry', 'job']
#
#    list_columns = ['industry', 'job']
#    list_exclude_columns = [] # ['industry', 'job']
#
#    search_columns = ['industry', 'job']
#    search_exclude_columns= [] # ['industry', 'job']
#
#    default_sort = [('id', True)]
#    base_permissions = ['can_list', 'can_show', 'can_edit', 'can_delete', 'can_add']
#    label_columns=   [{column.name: column.name for column in table.columns} ]
#    show_template =  'appbuilder/general/model/show_cascade.html'
#    list_template = 'appbuilder/general/model/list.html'
#    add_template = 'appbuilder/general/model/add.html'
#    edit_template = 'appbuilder/general/model/edit.html'
#    add_widget = (FormVerticalWidget|FormInlineWidget)
#    show_widget = ShowBlockWidget
#    list_widget = (ListThumbnail|ListWidget)
#    base_order = ('name', 'asc')
#    list_widget= 'list_widget'


class JobView(ModelView):
    datamodel=SQLAInterface(Job, db.session)
    related_views = []
    show_title='Job Detail'
    add_title ='Add Job'
    list_title= 'Job List'
    edit_title = 'Edit Job'
    show_columns = ['id', 'company_profile', 'about_job', 'responsibilities', 'salary', 'equity', 'offers_healthcare', 'offers_vision', 'offers_401k', 'offers_dental', 'paid_time_off', 'vacation_days', 'location', 'is_remote', 'applicant_count', 'job_filled']
#    show_exclude_columns = [] #= ['id', 'company_profile', 'about_job', 'responsibilities', 'salary', 'equity', 'offers_healthcare', 'offers_vision', 'offers_401k', 'offers_dental', 'paid_time_off', 'vacation_days', 'location', 'is_remote', 'applicant_count', 'job_filled']
#
#    add_columns = ['id', 'company_profile', 'about_job', 'responsibilities', 'salary', 'equity', 'offers_healthcare', 'offers_vision', 'offers_401k', 'offers_dental', 'paid_time_off', 'vacation_days', 'location', 'is_remote', 'applicant_count', 'job_filled']
#    add_exclude_columns = [hide_list] #['id', 'company_profile', 'about_job', 'responsibilities', 'salary', 'equity', 'offers_healthcare', 'offers_vision', 'offers_401k', 'offers_dental', 'paid_time_off', 'vacation_days', 'location', 'is_remote', 'applicant_count', 'job_filled']
#
#    edit_columns = ['id', 'company_profile', 'about_job', 'responsibilities', 'salary', 'equity', 'offers_healthcare', 'offers_vision', 'offers_401k', 'offers_dental', 'paid_time_off', 'vacation_days', 'location', 'is_remote', 'applicant_count', 'job_filled']
#    edit_exclude_columns =[hide_list] # ['id', 'company_profile', 'about_job', 'responsibilities', 'salary', 'equity', 'offers_healthcare', 'offers_vision', 'offers_401k', 'offers_dental', 'paid_time_off', 'vacation_days', 'location', 'is_remote', 'applicant_count', 'job_filled']
#
#    list_columns = ['id', 'company_profile', 'about_job', 'responsibilities', 'salary', 'equity', 'offers_healthcare', 'offers_vision', 'offers_401k', 'offers_dental', 'paid_time_off', 'vacation_days', 'location', 'is_remote', 'applicant_count', 'job_filled']
#    list_exclude_columns = [] # ['id', 'company_profile', 'about_job', 'responsibilities', 'salary', 'equity', 'offers_healthcare', 'offers_vision', 'offers_401k', 'offers_dental', 'paid_time_off', 'vacation_days', 'location', 'is_remote', 'applicant_count', 'job_filled']
#
#    search_columns = ['id', 'company_profile', 'about_job', 'responsibilities', 'salary', 'equity', 'offers_healthcare', 'offers_vision', 'offers_401k', 'offers_dental', 'paid_time_off', 'vacation_days', 'location', 'is_remote', 'applicant_count', 'job_filled']
#    search_exclude_columns= [] # ['id', 'company_profile', 'about_job', 'responsibilities', 'salary', 'equity', 'offers_healthcare', 'offers_vision', 'offers_401k', 'offers_dental', 'paid_time_off', 'vacation_days', 'location', 'is_remote', 'applicant_count', 'job_filled']
#
#    default_sort = [('id', True)]
#    base_permissions = ['can_list', 'can_show', 'can_edit', 'can_delete', 'can_add']
#    label_columns=   [{column.name: column.name for column in table.columns} ]
#    show_template =  'appbuilder/general/model/show_cascade.html'
#    list_template = 'appbuilder/general/model/list.html'
#    add_template = 'appbuilder/general/model/add.html'
#    edit_template = 'appbuilder/general/model/edit.html'
#    add_widget = (FormVerticalWidget|FormInlineWidget)
#    show_widget = ShowBlockWidget
#    list_widget = (ListThumbnail|ListWidget)
#    base_order = ('name', 'asc')
#    list_widget= 'list_widget'


class JobSkillView(ModelView):
    datamodel=SQLAInterface(JobSkill, db.session)
    related_views = []
    show_title='JobSkill Detail'
    add_title ='Add JobSkill'
    list_title= 'JobSkill List'
    edit_title = 'Edit JobSkill'
    show_columns = ['skills', 'jobs']
#    show_exclude_columns = [] #= ['skills', 'jobs']
#
#    add_columns = ['skills', 'jobs']
#    add_exclude_columns = [hide_list] #['skills', 'jobs']
#
#    edit_columns = ['skills', 'jobs']
#    edit_exclude_columns =[hide_list] # ['skills', 'jobs']
#
#    list_columns = ['skills', 'jobs']
#    list_exclude_columns = [] # ['skills', 'jobs']
#
#    search_columns = ['skills', 'jobs']
#    search_exclude_columns= [] # ['skills', 'jobs']
#
#    default_sort = [('id', True)]
#    base_permissions = ['can_list', 'can_show', 'can_edit', 'can_delete', 'can_add']
#    label_columns=   [{column.name: column.name for column in table.columns} ]
#    show_template =  'appbuilder/general/model/show_cascade.html'
#    list_template = 'appbuilder/general/model/list.html'
#    add_template = 'appbuilder/general/model/add.html'
#    edit_template = 'appbuilder/general/model/edit.html'
#    add_widget = (FormVerticalWidget|FormInlineWidget)
#    show_widget = ShowBlockWidget
#    list_widget = (ListThumbnail|ListWidget)
#    base_order = ('name', 'asc')
#    list_widget= 'list_widget'


class UserxDetailView(ModelView):
    datamodel=SQLAInterface(Userx, db.session)
    related_views = []
    show_title='Userx Detail'
    add_title ='Add Userx'
    list_title= 'Userx List'
    edit_title = 'Edit Userx'
    show_columns = ['id', 'userx', 'is_individual', 'is_institution', 'is_company', 'is_government', 'is_online']
#    show_exclude_columns = [] #= ['id', 'userx', 'is_individual', 'is_institution', 'is_company', 'is_government', 'is_online']
#
#    add_columns = ['id', 'userx', 'is_individual', 'is_institution', 'is_company', 'is_government', 'is_online']
#    add_exclude_columns = [hide_list] #['id', 'userx', 'is_individual', 'is_institution', 'is_company', 'is_government', 'is_online']
#
#    edit_columns = ['id', 'userx', 'is_individual', 'is_institution', 'is_company', 'is_government', 'is_online']
#    edit_exclude_columns =[hide_list] # ['id', 'userx', 'is_individual', 'is_institution', 'is_company', 'is_government', 'is_online']
#
#    list_columns = ['id', 'userx', 'is_individual', 'is_institution', 'is_company', 'is_government', 'is_online']
#    list_exclude_columns = [] # ['id', 'userx', 'is_individual', 'is_institution', 'is_company', 'is_government', 'is_online']
#
#    search_columns = ['id', 'userx', 'is_individual', 'is_institution', 'is_company', 'is_government', 'is_online']
#    search_exclude_columns= [] # ['id', 'userx', 'is_individual', 'is_institution', 'is_company', 'is_government', 'is_online']
#
#    default_sort = [('id', True)]
#    base_permissions = ['can_list', 'can_show', 'can_edit', 'can_delete', 'can_add']
#    label_columns=   [{column.name: column.name for column in table.columns} ]
#    show_template =  'appbuilder/general/model/show_cascade.html'
#    list_template = 'appbuilder/general/model/list.html'
#    add_template = 'appbuilder/general/model/add.html'
#    edit_template = 'appbuilder/general/model/edit.html'
#    add_widget = (FormVerticalWidget|FormInlineWidget)
#    show_widget = ShowBlockWidget
#    list_widget = (ListThumbnail|ListWidget)
#    base_order = ('name', 'asc')
#    list_widget= 'list_widget'


class IndividualDetailView(ModelView):
    datamodel=SQLAInterface(Individual, db.session)
    related_views = []
    show_title='Individual Detail'
    add_title ='Add Individual'
    list_title= 'Individual List'
    edit_title = 'Edit Individual'
    show_columns = ['id', 'userx', 'is_individual', 'is_institution', 'is_company', 'is_government', 'is_online']
#    show_exclude_columns = [] #= ['id', 'userx', 'is_individual', 'is_institution', 'is_company', 'is_government', 'is_online']
#
#    add_columns = ['id', 'userx', 'is_individual', 'is_institution', 'is_company', 'is_government', 'is_online']
#    add_exclude_columns = [hide_list] #['id', 'userx', 'is_individual', 'is_institution', 'is_company', 'is_government', 'is_online']
#
#    edit_columns = ['id', 'userx', 'is_individual', 'is_institution', 'is_company', 'is_government', 'is_online']
#    edit_exclude_columns =[hide_list] # ['id', 'userx', 'is_individual', 'is_institution', 'is_company', 'is_government', 'is_online']
#
#    list_columns = ['id', 'userx', 'is_individual', 'is_institution', 'is_company', 'is_government', 'is_online']
#    list_exclude_columns = [] # ['id', 'userx', 'is_individual', 'is_institution', 'is_company', 'is_government', 'is_online']
#
#    search_columns = ['id', 'userx', 'is_individual', 'is_institution', 'is_company', 'is_government', 'is_online']
#    search_exclude_columns= [] # ['id', 'userx', 'is_individual', 'is_institution', 'is_company', 'is_government', 'is_online']
#
#    default_sort = [('id', True)]
#    base_permissions = ['can_list', 'can_show', 'can_edit', 'can_delete', 'can_add']
#    label_columns=   [{column.name: column.name for column in table.columns} ]
#    show_template =  'appbuilder/general/model/show_cascade.html'
#    list_template = 'appbuilder/general/model/list.html'
#    add_template = 'appbuilder/general/model/add.html'
#    edit_template = 'appbuilder/general/model/edit.html'
#    add_widget = (FormVerticalWidget|FormInlineWidget)
#    show_widget = ShowBlockWidget
#    list_widget = (ListThumbnail|ListWidget)
#    base_order = ('name', 'asc')
#    list_widget= 'list_widget'


class IndustryDetailView(ModelView):
    datamodel=SQLAInterface(Industry, db.session)
    related_views = []
    show_title='Industry Detail'
    add_title ='Add Industry'
    list_title= 'Industry List'
    edit_title = 'Edit Industry'
    show_columns = ['industry', 'job']
#    show_exclude_columns = [] #= ['industry', 'job']
#
#    add_columns = ['industry', 'job']
#    add_exclude_columns = [hide_list] #['industry', 'job']
#
#    edit_columns = ['industry', 'job']
#    edit_exclude_columns =[hide_list] # ['industry', 'job']
#
#    list_columns = ['industry', 'job']
#    list_exclude_columns = [] # ['industry', 'job']
#
#    search_columns = ['industry', 'job']
#    search_exclude_columns= [] # ['industry', 'job']
#
#    default_sort = [('id', True)]
#    base_permissions = ['can_list', 'can_show', 'can_edit', 'can_delete', 'can_add']
#    label_columns=   [{column.name: column.name for column in table.columns} ]
#    show_template =  'appbuilder/general/model/show_cascade.html'
#    list_template = 'appbuilder/general/model/list.html'
#    add_template = 'appbuilder/general/model/add.html'
#    edit_template = 'appbuilder/general/model/edit.html'
#    add_widget = (FormVerticalWidget|FormInlineWidget)
#    show_widget = ShowBlockWidget
#    list_widget = (ListThumbnail|ListWidget)
#    base_order = ('name', 'asc')
#    list_widget= 'list_widget'


class IndustryJobDetailView(ModelView):
    datamodel=SQLAInterface(IndustryJob, db.session)
    related_views = []
    show_title='IndustryJob Detail'
    add_title ='Add IndustryJob'
    list_title= 'IndustryJob List'
    edit_title = 'Edit IndustryJob'
    show_columns = ['industry', 'job']
#    show_exclude_columns = [] #= ['industry', 'job']
#
#    add_columns = ['industry', 'job']
#    add_exclude_columns = [hide_list] #['industry', 'job']
#
#    edit_columns = ['industry', 'job']
#    edit_exclude_columns =[hide_list] # ['industry', 'job']
#
#    list_columns = ['industry', 'job']
#    list_exclude_columns = [] # ['industry', 'job']
#
#    search_columns = ['industry', 'job']
#    search_exclude_columns= [] # ['industry', 'job']
#
#    default_sort = [('id', True)]
#    base_permissions = ['can_list', 'can_show', 'can_edit', 'can_delete', 'can_add']
#    label_columns=   [{column.name: column.name for column in table.columns} ]
#    show_template =  'appbuilder/general/model/show_cascade.html'
#    list_template = 'appbuilder/general/model/list.html'
#    add_template = 'appbuilder/general/model/add.html'
#    edit_template = 'appbuilder/general/model/edit.html'
#    add_widget = (FormVerticalWidget|FormInlineWidget)
#    show_widget = ShowBlockWidget
#    list_widget = (ListThumbnail|ListWidget)
#    base_order = ('name', 'asc')
#    list_widget= 'list_widget'


class JobDetailView(ModelView):
    datamodel=SQLAInterface(Job, db.session)
    related_views = []
    show_title='Job Detail'
    add_title ='Add Job'
    list_title= 'Job List'
    edit_title = 'Edit Job'
    show_columns = ['industry', 'job']
#    show_exclude_columns = [] #= ['industry', 'job']
#
#    add_columns = ['industry', 'job']
#    add_exclude_columns = [hide_list] #['industry', 'job']
#
#    edit_columns = ['industry', 'job']
#    edit_exclude_columns =[hide_list] # ['industry', 'job']
#
#    list_columns = ['industry', 'job']
#    list_exclude_columns = [] # ['industry', 'job']
#
#    search_columns = ['industry', 'job']
#    search_exclude_columns= [] # ['industry', 'job']
#
#    default_sort = [('id', True)]
#    base_permissions = ['can_list', 'can_show', 'can_edit', 'can_delete', 'can_add']
#    label_columns=   [{column.name: column.name for column in table.columns} ]
#    show_template =  'appbuilder/general/model/show_cascade.html'
#    list_template = 'appbuilder/general/model/list.html'
#    add_template = 'appbuilder/general/model/add.html'
#    edit_template = 'appbuilder/general/model/edit.html'
#    add_widget = (FormVerticalWidget|FormInlineWidget)
#    show_widget = ShowBlockWidget
#    list_widget = (ListThumbnail|ListWidget)
#    base_order = ('name', 'asc')
#    list_widget= 'list_widget'




class SkillDetailView(ModelView):
    datamodel=SQLAInterface(Skill, db.session)
    related_views = []
    show_title='Skill Detail'
    add_title ='Add Skill'
    list_title= 'Skill List'
    edit_title = 'Edit Skill'
    show_columns = ['skills', 'jobs']
#    show_exclude_columns = [] #= ['skills', 'jobs']
#
#    add_columns = ['skills', 'jobs']
#    add_exclude_columns = [hide_list] #['skills', 'jobs']
#
#    edit_columns = ['skills', 'jobs']
#    edit_exclude_columns =[hide_list] # ['skills', 'jobs']
#
#    list_columns = ['skills', 'jobs']
#    list_exclude_columns = [] # ['skills', 'jobs']
#
#    search_columns = ['skills', 'jobs']
#    search_exclude_columns= [] # ['skills', 'jobs']
#
#    default_sort = [('id', True)]
#    base_permissions = ['can_list', 'can_show', 'can_edit', 'can_delete', 'can_add']
#    label_columns=   [{column.name: column.name for column in table.columns} ]
#    show_template =  'appbuilder/general/model/show_cascade.html'
#    list_template = 'appbuilder/general/model/list.html'
#    add_template = 'appbuilder/general/model/add.html'
#    edit_template = 'appbuilder/general/model/edit.html'
#    add_widget = (FormVerticalWidget|FormInlineWidget)
#    show_widget = ShowBlockWidget
#    list_widget = (ListThumbnail|ListWidget)
#    base_order = ('name', 'asc')
#    list_widget= 'list_widget'


class JobSkillDetailView(ModelView):
    datamodel=SQLAInterface(JobSkill, db.session)
    related_views = []
    show_title='JobSkill Detail'
    add_title ='Add JobSkill'
    list_title= 'JobSkill List'
    edit_title = 'Edit JobSkill'
    show_columns = ['skills', 'jobs']
#    show_exclude_columns = [] #= ['skills', 'jobs']
#
#    add_columns = ['skills', 'jobs']
#    add_exclude_columns = [hide_list] #['skills', 'jobs']
#
#    edit_columns = ['skills', 'jobs']
#    edit_exclude_columns =[hide_list] # ['skills', 'jobs']
#
#    list_columns = ['skills', 'jobs']
#    list_exclude_columns = [] # ['skills', 'jobs']
#
#    search_columns = ['skills', 'jobs']
#    search_exclude_columns= [] # ['skills', 'jobs']
#
#    default_sort = [('id', True)]
#    base_permissions = ['can_list', 'can_show', 'can_edit', 'can_delete', 'can_add']
#    label_columns=   [{column.name: column.name for column in table.columns} ]
#    show_template =  'appbuilder/general/model/show_cascade.html'
#    list_template = 'appbuilder/general/model/list.html'
#    add_template = 'appbuilder/general/model/add.html'
#    edit_template = 'appbuilder/general/model/edit.html'
#    add_widget = (FormVerticalWidget|FormInlineWidget)
#    show_widget = ShowBlockWidget
#    list_widget = (ListThumbnail|ListWidget)
#    base_order = ('name', 'asc')
#    list_widget= 'list_widget'


class IndividualMasterView(MasterDetailView):
    datamodel=SQLAInterface(Individual, db.session)
    related_views = [UserxDetailView]
    show_title='Individual Detail'
    add_title ='Add Individual'
    list_title= 'Individual List'
    edit_title = 'Edit Individual'
    show_columns = ['id', 'userx', 'is_individual', 'is_institution', 'is_company', 'is_government', 'is_online']
#    show_exclude_columns = [] #= ['id', 'userx', 'is_individual', 'is_institution', 'is_company', 'is_government', 'is_online']
#
#    add_columns = ['id', 'userx', 'is_individual', 'is_institution', 'is_company', 'is_government', 'is_online']
#    add_exclude_columns = [hide_list] #['id', 'userx', 'is_individual', 'is_institution', 'is_company', 'is_government', 'is_online']
#
#    edit_columns = ['id', 'userx', 'is_individual', 'is_institution', 'is_company', 'is_government', 'is_online']
#    edit_exclude_columns =[hide_list] # ['id', 'userx', 'is_individual', 'is_institution', 'is_company', 'is_government', 'is_online']
#
#    list_columns = ['id', 'userx', 'is_individual', 'is_institution', 'is_company', 'is_government', 'is_online']
#    list_exclude_columns = [] # ['id', 'userx', 'is_individual', 'is_institution', 'is_company', 'is_government', 'is_online']
#
#    search_columns = ['id', 'userx', 'is_individual', 'is_institution', 'is_company', 'is_government', 'is_online']
#    search_exclude_columns= [] # ['id', 'userx', 'is_individual', 'is_institution', 'is_company', 'is_government', 'is_online']
#
#    default_sort = [('id', True)]
#    base_permissions = ['can_list', 'can_show', 'can_edit', 'can_delete', 'can_add']
#    label_columns=   [{column.name: column.name for column in table.columns} ]
#    show_template =  'appbuilder/general/model/show_cascade.html'
#    list_template = 'appbuilder/general/model/list.html'
#    add_template = 'appbuilder/general/model/add.html'
#    edit_template = 'appbuilder/general/model/edit.html'
#    add_widget = (FormVerticalWidget|FormInlineWidget)
#    show_widget = ShowBlockWidget
#    list_widget = (ListThumbnail|ListWidget)
#    base_order = ('name', 'asc')
#    list_widget= 'list_widget'


class IndustryJobMasterView(MasterDetailView):
    datamodel=SQLAInterface(IndustryJob, db.session)
    related_views = [IndustryDetailView]
    show_title='IndustryJob Detail'
    add_title ='Add IndustryJob'
    list_title= 'IndustryJob List'
    edit_title = 'Edit IndustryJob'
    show_columns = ['industry', 'job']
#    show_exclude_columns = [] #= ['industry', 'job']
#
#    add_columns = ['industry', 'job']
#    add_exclude_columns = [hide_list] #['industry', 'job']
#
#    edit_columns = ['industry', 'job']
#    edit_exclude_columns =[hide_list] # ['industry', 'job']
#
#    list_columns = ['industry', 'job']
#    list_exclude_columns = [] # ['industry', 'job']
#
#    search_columns = ['industry', 'job']
#    search_exclude_columns= [] # ['industry', 'job']
#
#    default_sort = [('id', True)]
#    base_permissions = ['can_list', 'can_show', 'can_edit', 'can_delete', 'can_add']
#    label_columns=   [{column.name: column.name for column in table.columns} ]
#    show_template =  'appbuilder/general/model/show_cascade.html'
#    list_template = 'appbuilder/general/model/list.html'
#    add_template = 'appbuilder/general/model/add.html'
#    edit_template = 'appbuilder/general/model/edit.html'
#    add_widget = (FormVerticalWidget|FormInlineWidget)
#    show_widget = ShowBlockWidget
#    list_widget = (ListThumbnail|ListWidget)
#    base_order = ('name', 'asc')
#    list_widget= 'list_widget'


class IndustryJobMultiView(MultipleView):
    datamodel=SQLAInterface(IndustryJob, db.session)
    views = [IndustryDetailView, JobDetailView]
    show_title='IndustryJob Detail'
    add_title ='Add IndustryJob'
    list_title= 'IndustryJob List'
    edit_title = 'Edit IndustryJob'
    show_columns = ['industry', 'job']
#    show_exclude_columns = [] #= ['industry', 'job']
#
#    add_columns = ['industry', 'job']
#    add_exclude_columns = [hide_list] #['industry', 'job']
#
#    edit_columns = ['industry', 'job']
#    edit_exclude_columns =[hide_list] # ['industry', 'job']
#
#    list_columns = ['industry', 'job']
#    list_exclude_columns = [] # ['industry', 'job']
#
#    search_columns = ['industry', 'job']
#    search_exclude_columns= [] # ['industry', 'job']
#
#    default_sort = [('id', True)]
#    base_permissions = ['can_list', 'can_show', 'can_edit', 'can_delete', 'can_add']
#    label_columns=   [{column.name: column.name for column in table.columns} ]
#    show_template =  'appbuilder/general/model/show_cascade.html'
#    list_template = 'appbuilder/general/model/list.html'
#    add_template = 'appbuilder/general/model/add.html'
#    edit_template = 'appbuilder/general/model/edit.html'
#    add_widget = (FormVerticalWidget|FormInlineWidget)
#    show_widget = ShowBlockWidget
#    list_widget = (ListThumbnail|ListWidget)
#    base_order = ('name', 'asc')
#    list_widget= 'list_widget'


class JobSkillMasterView(MasterDetailView):
    datamodel=SQLAInterface(JobSkill, db.session)
    related_views = [JobDetailView]
    show_title='JobSkill Detail'
    add_title ='Add JobSkill'
    list_title= 'JobSkill List'
    edit_title = 'Edit JobSkill'
    show_columns = ['skills', 'jobs']
#    show_exclude_columns = [] #= ['skills', 'jobs']
#
#    add_columns = ['skills', 'jobs']
#    add_exclude_columns = [hide_list] #['skills', 'jobs']
#
#    edit_columns = ['skills', 'jobs']
#    edit_exclude_columns =[hide_list] # ['skills', 'jobs']
#
#    list_columns = ['skills', 'jobs']
#    list_exclude_columns = [] # ['skills', 'jobs']
#
#    search_columns = ['skills', 'jobs']
#    search_exclude_columns= [] # ['skills', 'jobs']
#
#    default_sort = [('id', True)]
#    base_permissions = ['can_list', 'can_show', 'can_edit', 'can_delete', 'can_add']
#    label_columns=   [{column.name: column.name for column in table.columns} ]
#    show_template =  'appbuilder/general/model/show_cascade.html'
#    list_template = 'appbuilder/general/model/list.html'
#    add_template = 'appbuilder/general/model/add.html'
#    edit_template = 'appbuilder/general/model/edit.html'
#    add_widget = (FormVerticalWidget|FormInlineWidget)
#    show_widget = ShowBlockWidget
#    list_widget = (ListThumbnail|ListWidget)
#    base_order = ('name', 'asc')
#    list_widget= 'list_widget'


class JobSkillMultiView(MultipleView):
    datamodel=SQLAInterface(JobSkill, db.session)
    views = [SkillDetailView]
    show_title='JobSkill Detail'
    add_title ='Add JobSkill'
    list_title= 'JobSkill List'
    edit_title = 'Edit JobSkill'
    show_columns = ['skills', 'jobs']
#    show_exclude_columns = [] #= ['skills', 'jobs']
#
#    add_columns = ['skills', 'jobs']
#    add_exclude_columns = [hide_list] #['skills', 'jobs']
#
#    edit_columns = ['skills', 'jobs']
#    edit_exclude_columns =[hide_list] # ['skills', 'jobs']
#
#    list_columns = ['skills', 'jobs']
#    list_exclude_columns = [] # ['skills', 'jobs']
#
#    search_columns = ['skills', 'jobs']
#    search_exclude_columns= [] # ['skills', 'jobs']
#
#    default_sort = [('id', True)]
#    base_permissions = ['can_list', 'can_show', 'can_edit', 'can_delete', 'can_add']
#    label_columns=   [{column.name: column.name for column in table.columns} ]
#    show_template =  'appbuilder/general/model/show_cascade.html'
#    list_template = 'appbuilder/general/model/list.html'
#    add_template = 'appbuilder/general/model/add.html'
#    edit_template = 'appbuilder/general/model/edit.html'
#    add_widget = (FormVerticalWidget|FormInlineWidget)
#    show_widget = ShowBlockWidget
#    list_widget = (ListThumbnail|ListWidget)
#    base_order = ('name', 'asc')
#    list_widget= 'list_widget'


class SkillView(ModelView):
    datamodel=SQLAInterface(Skill, db.session)
    related_views = []
    show_title='Skill Detail'
    add_title ='Add Skill'
    list_title= 'Skill List'
    edit_title = 'Edit Skill'
    show_columns = ['id', 'skill_value']
#    show_exclude_columns = [] #= ['id', 'skill_value']
#
#    add_columns = ['id', 'skill_value']
#    add_exclude_columns = [hide_list] #['id', 'skill_value']
#
#    edit_columns = ['id', 'skill_value']
#    edit_exclude_columns =[hide_list] # ['id', 'skill_value']
#
#    list_columns = ['id', 'skill_value']
#    list_exclude_columns = [] # ['id', 'skill_value']
#
#    search_columns = ['id', 'skill_value']
#    search_exclude_columns= [] # ['id', 'skill_value']
#
#    default_sort = [('id', True)]
#    base_permissions = ['can_list', 'can_show', 'can_edit', 'can_delete', 'can_add']
#    label_columns=   [{column.name: column.name for column in table.columns} ]
#    show_template =  'appbuilder/general/model/show_cascade.html'
#    list_template = 'appbuilder/general/model/list.html'
#    add_template = 'appbuilder/general/model/add.html'
#    edit_template = 'appbuilder/general/model/edit.html'
#    add_widget = (FormVerticalWidget|FormInlineWidget)
#    show_widget = ShowBlockWidget
#    list_widget = (ListThumbnail|ListWidget)
#    base_order = ('name', 'asc')
#    list_widget= 'list_widget'


class EducationView(ModelView):
    datamodel=SQLAInterface(Education, db.session)
    related_views = []
    show_title='Education Detail'
    add_title ='Add Education'
    list_title= 'Education List'
    edit_title = 'Edit Education'
    show_columns = ['id', 'individual', 'qualification', 'qual_class', 'verified', 'verification_code', 'verified_by', 'verification_date', 'verification_doc']
#    show_exclude_columns = [] #= ['id', 'individual', 'qualification', 'qual_class', 'verified', 'verification_code', 'verified_by', 'verification_date', 'verification_doc']
#
#    add_columns = ['id', 'individual', 'qualification', 'qual_class', 'verified', 'verification_code', 'verified_by', 'verification_date', 'verification_doc']
#    add_exclude_columns = [hide_list] #['id', 'individual', 'qualification', 'qual_class', 'verified', 'verification_code', 'verified_by', 'verification_date', 'verification_doc']
#
#    edit_columns = ['id', 'individual', 'qualification', 'qual_class', 'verified', 'verification_code', 'verified_by', 'verification_date', 'verification_doc']
#    edit_exclude_columns =[hide_list] # ['id', 'individual', 'qualification', 'qual_class', 'verified', 'verification_code', 'verified_by', 'verification_date', 'verification_doc']
#
#    list_columns = ['id', 'individual', 'qualification', 'qual_class', 'verified', 'verification_code', 'verified_by', 'verification_date', 'verification_doc']
#    list_exclude_columns = [] # ['id', 'individual', 'qualification', 'qual_class', 'verified', 'verification_code', 'verified_by', 'verification_date', 'verification_doc']
#
#    search_columns = ['id', 'individual', 'qualification', 'qual_class', 'verified', 'verification_code', 'verified_by', 'verification_date', 'verification_doc']
#    search_exclude_columns= [] # ['id', 'individual', 'qualification', 'qual_class', 'verified', 'verification_code', 'verified_by', 'verification_date', 'verification_doc']
#
#    default_sort = [('id', True)]
#    base_permissions = ['can_list', 'can_show', 'can_edit', 'can_delete', 'can_add']
#    label_columns=   [{column.name: column.name for column in table.columns} ]
#    show_template =  'appbuilder/general/model/show_cascade.html'
#    list_template = 'appbuilder/general/model/list.html'
#    add_template = 'appbuilder/general/model/add.html'
#    edit_template = 'appbuilder/general/model/edit.html'
#    add_widget = (FormVerticalWidget|FormInlineWidget)
#    show_widget = ShowBlockWidget
#    list_widget = (ListThumbnail|ListWidget)
#    base_order = ('name', 'asc')
#    list_widget= 'list_widget'


class UserxDetailView(ModelView):
    datamodel=SQLAInterface(Userx, db.session)
    related_views = []
    show_title='Userx Detail'
    add_title ='Add Userx'
    list_title= 'Userx List'
    edit_title = 'Edit Userx'
    show_columns = ['id', 'userx', 'is_individual', 'is_institution', 'is_company', 'is_government', 'is_online']
#    show_exclude_columns = [] #= ['id', 'userx', 'is_individual', 'is_institution', 'is_company', 'is_government', 'is_online']
#
#    add_columns = ['id', 'userx', 'is_individual', 'is_institution', 'is_company', 'is_government', 'is_online']
#    add_exclude_columns = [hide_list] #['id', 'userx', 'is_individual', 'is_institution', 'is_company', 'is_government', 'is_online']
#
#    edit_columns = ['id', 'userx', 'is_individual', 'is_institution', 'is_company', 'is_government', 'is_online']
#    edit_exclude_columns =[hide_list] # ['id', 'userx', 'is_individual', 'is_institution', 'is_company', 'is_government', 'is_online']
#
#    list_columns = ['id', 'userx', 'is_individual', 'is_institution', 'is_company', 'is_government', 'is_online']
#    list_exclude_columns = [] # ['id', 'userx', 'is_individual', 'is_institution', 'is_company', 'is_government', 'is_online']
#
#    search_columns = ['id', 'userx', 'is_individual', 'is_institution', 'is_company', 'is_government', 'is_online']
#    search_exclude_columns= [] # ['id', 'userx', 'is_individual', 'is_institution', 'is_company', 'is_government', 'is_online']
#
#    default_sort = [('id', True)]
#    base_permissions = ['can_list', 'can_show', 'can_edit', 'can_delete', 'can_add']
#    label_columns=   [{column.name: column.name for column in table.columns} ]
#    show_template =  'appbuilder/general/model/show_cascade.html'
#    list_template = 'appbuilder/general/model/list.html'
#    add_template = 'appbuilder/general/model/add.html'
#    edit_template = 'appbuilder/general/model/edit.html'
#    add_widget = (FormVerticalWidget|FormInlineWidget)
#    show_widget = ShowBlockWidget
#    list_widget = (ListThumbnail|ListWidget)
#    base_order = ('name', 'asc')
#    list_widget= 'list_widget'


class IndividualDetailView(ModelView):
    datamodel=SQLAInterface(Individual, db.session)
    related_views = []
    show_title='Individual Detail'
    add_title ='Add Individual'
    list_title= 'Individual List'
    edit_title = 'Edit Individual'
    show_columns = ['id', 'userx', 'is_individual', 'is_institution', 'is_company', 'is_government', 'is_online']
#    show_exclude_columns = [] #= ['id', 'userx', 'is_individual', 'is_institution', 'is_company', 'is_government', 'is_online']
#
#    add_columns = ['id', 'userx', 'is_individual', 'is_institution', 'is_company', 'is_government', 'is_online']
#    add_exclude_columns = [hide_list] #['id', 'userx', 'is_individual', 'is_institution', 'is_company', 'is_government', 'is_online']
#
#    edit_columns = ['id', 'userx', 'is_individual', 'is_institution', 'is_company', 'is_government', 'is_online']
#    edit_exclude_columns =[hide_list] # ['id', 'userx', 'is_individual', 'is_institution', 'is_company', 'is_government', 'is_online']
#
#    list_columns = ['id', 'userx', 'is_individual', 'is_institution', 'is_company', 'is_government', 'is_online']
#    list_exclude_columns = [] # ['id', 'userx', 'is_individual', 'is_institution', 'is_company', 'is_government', 'is_online']
#
#    search_columns = ['id', 'userx', 'is_individual', 'is_institution', 'is_company', 'is_government', 'is_online']
#    search_exclude_columns= [] # ['id', 'userx', 'is_individual', 'is_institution', 'is_company', 'is_government', 'is_online']
#
#    default_sort = [('id', True)]
#    base_permissions = ['can_list', 'can_show', 'can_edit', 'can_delete', 'can_add']
#    label_columns=   [{column.name: column.name for column in table.columns} ]
#    show_template =  'appbuilder/general/model/show_cascade.html'
#    list_template = 'appbuilder/general/model/list.html'
#    add_template = 'appbuilder/general/model/add.html'
#    edit_template = 'appbuilder/general/model/edit.html'
#    add_widget = (FormVerticalWidget|FormInlineWidget)
#    show_widget = ShowBlockWidget
#    list_widget = (ListThumbnail|ListWidget)
#    base_order = ('name', 'asc')
#    list_widget= 'list_widget'


class IndustryDetailView(ModelView):
    datamodel=SQLAInterface(Industry, db.session)
    related_views = []
    show_title='Industry Detail'
    add_title ='Add Industry'
    list_title= 'Industry List'
    edit_title = 'Edit Industry'
    show_columns = ['industry', 'job']
#    show_exclude_columns = [] #= ['industry', 'job']
#
#    add_columns = ['industry', 'job']
#    add_exclude_columns = [hide_list] #['industry', 'job']
#
#    edit_columns = ['industry', 'job']
#    edit_exclude_columns =[hide_list] # ['industry', 'job']
#
#    list_columns = ['industry', 'job']
#    list_exclude_columns = [] # ['industry', 'job']
#
#    search_columns = ['industry', 'job']
#    search_exclude_columns= [] # ['industry', 'job']
#
#    default_sort = [('id', True)]
#    base_permissions = ['can_list', 'can_show', 'can_edit', 'can_delete', 'can_add']
#    label_columns=   [{column.name: column.name for column in table.columns} ]
#    show_template =  'appbuilder/general/model/show_cascade.html'
#    list_template = 'appbuilder/general/model/list.html'
#    add_template = 'appbuilder/general/model/add.html'
#    edit_template = 'appbuilder/general/model/edit.html'
#    add_widget = (FormVerticalWidget|FormInlineWidget)
#    show_widget = ShowBlockWidget
#    list_widget = (ListThumbnail|ListWidget)
#    base_order = ('name', 'asc')
#    list_widget= 'list_widget'


class IndustryJobDetailView(ModelView):
    datamodel=SQLAInterface(IndustryJob, db.session)
    related_views = []
    show_title='IndustryJob Detail'
    add_title ='Add IndustryJob'
    list_title= 'IndustryJob List'
    edit_title = 'Edit IndustryJob'
    show_columns = ['industry', 'job']
#    show_exclude_columns = [] #= ['industry', 'job']
#
#    add_columns = ['industry', 'job']
#    add_exclude_columns = [hide_list] #['industry', 'job']
#
#    edit_columns = ['industry', 'job']
#    edit_exclude_columns =[hide_list] # ['industry', 'job']
#
#    list_columns = ['industry', 'job']
#    list_exclude_columns = [] # ['industry', 'job']
#
#    search_columns = ['industry', 'job']
#    search_exclude_columns= [] # ['industry', 'job']
#
#    default_sort = [('id', True)]
#    base_permissions = ['can_list', 'can_show', 'can_edit', 'can_delete', 'can_add']
#    label_columns=   [{column.name: column.name for column in table.columns} ]
#    show_template =  'appbuilder/general/model/show_cascade.html'
#    list_template = 'appbuilder/general/model/list.html'
#    add_template = 'appbuilder/general/model/add.html'
#    edit_template = 'appbuilder/general/model/edit.html'
#    add_widget = (FormVerticalWidget|FormInlineWidget)
#    show_widget = ShowBlockWidget
#    list_widget = (ListThumbnail|ListWidget)
#    base_order = ('name', 'asc')
#    list_widget= 'list_widget'


class JobDetailView(ModelView):
    datamodel=SQLAInterface(Job, db.session)
    related_views = []
    show_title='Job Detail'
    add_title ='Add Job'
    list_title= 'Job List'
    edit_title = 'Edit Job'
    show_columns = ['industry', 'job']
#    show_exclude_columns = [] #= ['industry', 'job']
#
#    add_columns = ['industry', 'job']
#    add_exclude_columns = [hide_list] #['industry', 'job']
#
#    edit_columns = ['industry', 'job']
#    edit_exclude_columns =[hide_list] # ['industry', 'job']
#
#    list_columns = ['industry', 'job']
#    list_exclude_columns = [] # ['industry', 'job']
#
#    search_columns = ['industry', 'job']
#    search_exclude_columns= [] # ['industry', 'job']
#
#    default_sort = [('id', True)]
#    base_permissions = ['can_list', 'can_show', 'can_edit', 'can_delete', 'can_add']
#    label_columns=   [{column.name: column.name for column in table.columns} ]
#    show_template =  'appbuilder/general/model/show_cascade.html'
#    list_template = 'appbuilder/general/model/list.html'
#    add_template = 'appbuilder/general/model/add.html'
#    edit_template = 'appbuilder/general/model/edit.html'
#    add_widget = (FormVerticalWidget|FormInlineWidget)
#    show_widget = ShowBlockWidget
#    list_widget = (ListThumbnail|ListWidget)
#    base_order = ('name', 'asc')
#    list_widget= 'list_widget'




class SkillDetailView(ModelView):
    datamodel=SQLAInterface(Skill, db.session)
    related_views = []
    show_title='Skill Detail'
    add_title ='Add Skill'
    list_title= 'Skill List'
    edit_title = 'Edit Skill'
    show_columns = ['skills', 'jobs']
#    show_exclude_columns = [] #= ['skills', 'jobs']
#
#    add_columns = ['skills', 'jobs']
#    add_exclude_columns = [hide_list] #['skills', 'jobs']
#
#    edit_columns = ['skills', 'jobs']
#    edit_exclude_columns =[hide_list] # ['skills', 'jobs']
#
#    list_columns = ['skills', 'jobs']
#    list_exclude_columns = [] # ['skills', 'jobs']
#
#    search_columns = ['skills', 'jobs']
#    search_exclude_columns= [] # ['skills', 'jobs']
#
#    default_sort = [('id', True)]
#    base_permissions = ['can_list', 'can_show', 'can_edit', 'can_delete', 'can_add']
#    label_columns=   [{column.name: column.name for column in table.columns} ]
#    show_template =  'appbuilder/general/model/show_cascade.html'
#    list_template = 'appbuilder/general/model/list.html'
#    add_template = 'appbuilder/general/model/add.html'
#    edit_template = 'appbuilder/general/model/edit.html'
#    add_widget = (FormVerticalWidget|FormInlineWidget)
#    show_widget = ShowBlockWidget
#    list_widget = (ListThumbnail|ListWidget)
#    base_order = ('name', 'asc')
#    list_widget= 'list_widget'


class JobSkillDetailView(ModelView):
    datamodel=SQLAInterface(JobSkill, db.session)
    related_views = []
    show_title='JobSkill Detail'
    add_title ='Add JobSkill'
    list_title= 'JobSkill List'
    edit_title = 'Edit JobSkill'
    show_columns = ['skills', 'jobs']
#    show_exclude_columns = [] #= ['skills', 'jobs']
#
#    add_columns = ['skills', 'jobs']
#    add_exclude_columns = [hide_list] #['skills', 'jobs']
#
#    edit_columns = ['skills', 'jobs']
#    edit_exclude_columns =[hide_list] # ['skills', 'jobs']
#
#    list_columns = ['skills', 'jobs']
#    list_exclude_columns = [] # ['skills', 'jobs']
#
#    search_columns = ['skills', 'jobs']
#    search_exclude_columns= [] # ['skills', 'jobs']
#
#    default_sort = [('id', True)]
#    base_permissions = ['can_list', 'can_show', 'can_edit', 'can_delete', 'can_add']
#    label_columns=   [{column.name: column.name for column in table.columns} ]
#    show_template =  'appbuilder/general/model/show_cascade.html'
#    list_template = 'appbuilder/general/model/list.html'
#    add_template = 'appbuilder/general/model/add.html'
#    edit_template = 'appbuilder/general/model/edit.html'
#    add_widget = (FormVerticalWidget|FormInlineWidget)
#    show_widget = ShowBlockWidget
#    list_widget = (ListThumbnail|ListWidget)
#    base_order = ('name', 'asc')
#    list_widget= 'list_widget'


class IndividualMasterView(MasterDetailView):
    datamodel=SQLAInterface(Individual, db.session)
    related_views = [UserxDetailView]
    show_title='Individual Detail'
    add_title ='Add Individual'
    list_title= 'Individual List'
    edit_title = 'Edit Individual'
    show_columns = ['id', 'userx', 'is_individual', 'is_institution', 'is_company', 'is_government', 'is_online']
#    show_exclude_columns = [] #= ['id', 'userx', 'is_individual', 'is_institution', 'is_company', 'is_government', 'is_online']
#
#    add_columns = ['id', 'userx', 'is_individual', 'is_institution', 'is_company', 'is_government', 'is_online']
#    add_exclude_columns = [hide_list] #['id', 'userx', 'is_individual', 'is_institution', 'is_company', 'is_government', 'is_online']
#
#    edit_columns = ['id', 'userx', 'is_individual', 'is_institution', 'is_company', 'is_government', 'is_online']
#    edit_exclude_columns =[hide_list] # ['id', 'userx', 'is_individual', 'is_institution', 'is_company', 'is_government', 'is_online']
#
#    list_columns = ['id', 'userx', 'is_individual', 'is_institution', 'is_company', 'is_government', 'is_online']
#    list_exclude_columns = [] # ['id', 'userx', 'is_individual', 'is_institution', 'is_company', 'is_government', 'is_online']
#
#    search_columns = ['id', 'userx', 'is_individual', 'is_institution', 'is_company', 'is_government', 'is_online']
#    search_exclude_columns= [] # ['id', 'userx', 'is_individual', 'is_institution', 'is_company', 'is_government', 'is_online']
#
#    default_sort = [('id', True)]
#    base_permissions = ['can_list', 'can_show', 'can_edit', 'can_delete', 'can_add']
#    label_columns=   [{column.name: column.name for column in table.columns} ]
#    show_template =  'appbuilder/general/model/show_cascade.html'
#    list_template = 'appbuilder/general/model/list.html'
#    add_template = 'appbuilder/general/model/add.html'
#    edit_template = 'appbuilder/general/model/edit.html'
#    add_widget = (FormVerticalWidget|FormInlineWidget)
#    show_widget = ShowBlockWidget
#    list_widget = (ListThumbnail|ListWidget)
#    base_order = ('name', 'asc')
#    list_widget= 'list_widget'


class IndustryJobMasterView(MasterDetailView):
    datamodel=SQLAInterface(IndustryJob, db.session)
    related_views = [IndustryDetailView]
    show_title='IndustryJob Detail'
    add_title ='Add IndustryJob'
    list_title= 'IndustryJob List'
    edit_title = 'Edit IndustryJob'
    show_columns = ['industry', 'job']
#    show_exclude_columns = [] #= ['industry', 'job']
#
#    add_columns = ['industry', 'job']
#    add_exclude_columns = [hide_list] #['industry', 'job']
#
#    edit_columns = ['industry', 'job']
#    edit_exclude_columns =[hide_list] # ['industry', 'job']
#
#    list_columns = ['industry', 'job']
#    list_exclude_columns = [] # ['industry', 'job']
#
#    search_columns = ['industry', 'job']
#    search_exclude_columns= [] # ['industry', 'job']
#
#    default_sort = [('id', True)]
#    base_permissions = ['can_list', 'can_show', 'can_edit', 'can_delete', 'can_add']
#    label_columns=   [{column.name: column.name for column in table.columns} ]
#    show_template =  'appbuilder/general/model/show_cascade.html'
#    list_template = 'appbuilder/general/model/list.html'
#    add_template = 'appbuilder/general/model/add.html'
#    edit_template = 'appbuilder/general/model/edit.html'
#    add_widget = (FormVerticalWidget|FormInlineWidget)
#    show_widget = ShowBlockWidget
#    list_widget = (ListThumbnail|ListWidget)
#    base_order = ('name', 'asc')
#    list_widget= 'list_widget'


class IndustryJobMultiView(MultipleView):
    datamodel=SQLAInterface(IndustryJob, db.session)
    views = [IndustryDetailView, JobDetailView]
    show_title='IndustryJob Detail'
    add_title ='Add IndustryJob'
    list_title= 'IndustryJob List'
    edit_title = 'Edit IndustryJob'
    show_columns = ['industry', 'job']
#    show_exclude_columns = [] #= ['industry', 'job']
#
#    add_columns = ['industry', 'job']
#    add_exclude_columns = [hide_list] #['industry', 'job']
#
#    edit_columns = ['industry', 'job']
#    edit_exclude_columns =[hide_list] # ['industry', 'job']
#
#    list_columns = ['industry', 'job']
#    list_exclude_columns = [] # ['industry', 'job']
#
#    search_columns = ['industry', 'job']
#    search_exclude_columns= [] # ['industry', 'job']
#
#    default_sort = [('id', True)]
#    base_permissions = ['can_list', 'can_show', 'can_edit', 'can_delete', 'can_add']
#    label_columns=   [{column.name: column.name for column in table.columns} ]
#    show_template =  'appbuilder/general/model/show_cascade.html'
#    list_template = 'appbuilder/general/model/list.html'
#    add_template = 'appbuilder/general/model/add.html'
#    edit_template = 'appbuilder/general/model/edit.html'
#    add_widget = (FormVerticalWidget|FormInlineWidget)
#    show_widget = ShowBlockWidget
#    list_widget = (ListThumbnail|ListWidget)
#    base_order = ('name', 'asc')
#    list_widget= 'list_widget'


class JobSkillMasterView(MasterDetailView):
    datamodel=SQLAInterface(JobSkill, db.session)
    related_views = [JobDetailView]
    show_title='JobSkill Detail'
    add_title ='Add JobSkill'
    list_title= 'JobSkill List'
    edit_title = 'Edit JobSkill'
    show_columns = ['skills', 'jobs']
#    show_exclude_columns = [] #= ['skills', 'jobs']
#
#    add_columns = ['skills', 'jobs']
#    add_exclude_columns = [hide_list] #['skills', 'jobs']
#
#    edit_columns = ['skills', 'jobs']
#    edit_exclude_columns =[hide_list] # ['skills', 'jobs']
#
#    list_columns = ['skills', 'jobs']
#    list_exclude_columns = [] # ['skills', 'jobs']
#
#    search_columns = ['skills', 'jobs']
#    search_exclude_columns= [] # ['skills', 'jobs']
#
#    default_sort = [('id', True)]
#    base_permissions = ['can_list', 'can_show', 'can_edit', 'can_delete', 'can_add']
#    label_columns=   [{column.name: column.name for column in table.columns} ]
#    show_template =  'appbuilder/general/model/show_cascade.html'
#    list_template = 'appbuilder/general/model/list.html'
#    add_template = 'appbuilder/general/model/add.html'
#    edit_template = 'appbuilder/general/model/edit.html'
#    add_widget = (FormVerticalWidget|FormInlineWidget)
#    show_widget = ShowBlockWidget
#    list_widget = (ListThumbnail|ListWidget)
#    base_order = ('name', 'asc')
#    list_widget= 'list_widget'


class JobSkillMultiView(MultipleView):
    datamodel=SQLAInterface(JobSkill, db.session)
    views = [SkillDetailView]
    show_title='JobSkill Detail'
    add_title ='Add JobSkill'
    list_title= 'JobSkill List'
    edit_title = 'Edit JobSkill'
    show_columns = ['skills', 'jobs']
#    show_exclude_columns = [] #= ['skills', 'jobs']
#
#    add_columns = ['skills', 'jobs']
#    add_exclude_columns = [hide_list] #['skills', 'jobs']
#
#    edit_columns = ['skills', 'jobs']
#    edit_exclude_columns =[hide_list] # ['skills', 'jobs']
#
#    list_columns = ['skills', 'jobs']
#    list_exclude_columns = [] # ['skills', 'jobs']
#
#    search_columns = ['skills', 'jobs']
#    search_exclude_columns= [] # ['skills', 'jobs']
#
#    default_sort = [('id', True)]
#    base_permissions = ['can_list', 'can_show', 'can_edit', 'can_delete', 'can_add']
#    label_columns=   [{column.name: column.name for column in table.columns} ]
#    show_template =  'appbuilder/general/model/show_cascade.html'
#    list_template = 'appbuilder/general/model/list.html'
#    add_template = 'appbuilder/general/model/add.html'
#    edit_template = 'appbuilder/general/model/edit.html'
#    add_widget = (FormVerticalWidget|FormInlineWidget)
#    show_widget = ShowBlockWidget
#    list_widget = (ListThumbnail|ListWidget)
#    base_order = ('name', 'asc')
#    list_widget= 'list_widget'


class EducationMasterView(MasterDetailView):
    datamodel=SQLAInterface(Education, db.session)
    related_views = [IndividualDetailView]
    show_title='Education Detail'
    add_title ='Add Education'
    list_title= 'Education List'
    edit_title = 'Edit Education'
    show_columns = ['id', 'individual', 'qualification', 'qual_class', 'verified', 'verification_code', 'verified_by', 'verification_date', 'verification_doc']
#    show_exclude_columns = [] #= ['id', 'individual', 'qualification', 'qual_class', 'verified', 'verification_code', 'verified_by', 'verification_date', 'verification_doc']
#
#    add_columns = ['id', 'individual', 'qualification', 'qual_class', 'verified', 'verification_code', 'verified_by', 'verification_date', 'verification_doc']
#    add_exclude_columns = [hide_list] #['id', 'individual', 'qualification', 'qual_class', 'verified', 'verification_code', 'verified_by', 'verification_date', 'verification_doc']
#
#    edit_columns = ['id', 'individual', 'qualification', 'qual_class', 'verified', 'verification_code', 'verified_by', 'verification_date', 'verification_doc']
#    edit_exclude_columns =[hide_list] # ['id', 'individual', 'qualification', 'qual_class', 'verified', 'verification_code', 'verified_by', 'verification_date', 'verification_doc']
#
#    list_columns = ['id', 'individual', 'qualification', 'qual_class', 'verified', 'verification_code', 'verified_by', 'verification_date', 'verification_doc']
#    list_exclude_columns = [] # ['id', 'individual', 'qualification', 'qual_class', 'verified', 'verification_code', 'verified_by', 'verification_date', 'verification_doc']
#
#    search_columns = ['id', 'individual', 'qualification', 'qual_class', 'verified', 'verification_code', 'verified_by', 'verification_date', 'verification_doc']
#    search_exclude_columns= [] # ['id', 'individual', 'qualification', 'qual_class', 'verified', 'verification_code', 'verified_by', 'verification_date', 'verification_doc']
#
#    default_sort = [('id', True)]
#    base_permissions = ['can_list', 'can_show', 'can_edit', 'can_delete', 'can_add']
#    label_columns=   [{column.name: column.name for column in table.columns} ]
#    show_template =  'appbuilder/general/model/show_cascade.html'
#    list_template = 'appbuilder/general/model/list.html'
#    add_template = 'appbuilder/general/model/add.html'
#    edit_template = 'appbuilder/general/model/edit.html'
#    add_widget = (FormVerticalWidget|FormInlineWidget)
#    show_widget = ShowBlockWidget
#    list_widget = (ListThumbnail|ListWidget)
#    base_order = ('name', 'asc')
#    list_widget= 'list_widget'


class IndividualJobView(ModelView):
    datamodel=SQLAInterface(IndividualJob, db.session)
    related_views = []
    show_title='IndividualJob Detail'
    add_title ='Add IndividualJob'
    list_title= 'IndividualJob List'
    edit_title = 'Edit IndividualJob'
    show_columns = ['individual', 'job']
#    show_exclude_columns = [] #= ['individual', 'job']
#
#    add_columns = ['individual', 'job']
#    add_exclude_columns = [hide_list] #['individual', 'job']
#
#    edit_columns = ['individual', 'job']
#    edit_exclude_columns =[hide_list] # ['individual', 'job']
#
#    list_columns = ['individual', 'job']
#    list_exclude_columns = [] # ['individual', 'job']
#
#    search_columns = ['individual', 'job']
#    search_exclude_columns= [] # ['individual', 'job']
#
#    default_sort = [('id', True)]
#    base_permissions = ['can_list', 'can_show', 'can_edit', 'can_delete', 'can_add']
#    label_columns=   [{column.name: column.name for column in table.columns} ]
#    show_template =  'appbuilder/general/model/show_cascade.html'
#    list_template = 'appbuilder/general/model/list.html'
#    add_template = 'appbuilder/general/model/add.html'
#    edit_template = 'appbuilder/general/model/edit.html'
#    add_widget = (FormVerticalWidget|FormInlineWidget)
#    show_widget = ShowBlockWidget
#    list_widget = (ListThumbnail|ListWidget)
#    base_order = ('name', 'asc')
#    list_widget= 'list_widget'


class UserxDetailView(ModelView):
    datamodel=SQLAInterface(Userx, db.session)
    related_views = []
    show_title='Userx Detail'
    add_title ='Add Userx'
    list_title= 'Userx List'
    edit_title = 'Edit Userx'
    show_columns = ['id', 'userx', 'is_individual', 'is_institution', 'is_company', 'is_government', 'is_online']
#    show_exclude_columns = [] #= ['id', 'userx', 'is_individual', 'is_institution', 'is_company', 'is_government', 'is_online']
#
#    add_columns = ['id', 'userx', 'is_individual', 'is_institution', 'is_company', 'is_government', 'is_online']
#    add_exclude_columns = [hide_list] #['id', 'userx', 'is_individual', 'is_institution', 'is_company', 'is_government', 'is_online']
#
#    edit_columns = ['id', 'userx', 'is_individual', 'is_institution', 'is_company', 'is_government', 'is_online']
#    edit_exclude_columns =[hide_list] # ['id', 'userx', 'is_individual', 'is_institution', 'is_company', 'is_government', 'is_online']
#
#    list_columns = ['id', 'userx', 'is_individual', 'is_institution', 'is_company', 'is_government', 'is_online']
#    list_exclude_columns = [] # ['id', 'userx', 'is_individual', 'is_institution', 'is_company', 'is_government', 'is_online']
#
#    search_columns = ['id', 'userx', 'is_individual', 'is_institution', 'is_company', 'is_government', 'is_online']
#    search_exclude_columns= [] # ['id', 'userx', 'is_individual', 'is_institution', 'is_company', 'is_government', 'is_online']
#
#    default_sort = [('id', True)]
#    base_permissions = ['can_list', 'can_show', 'can_edit', 'can_delete', 'can_add']
#    label_columns=   [{column.name: column.name for column in table.columns} ]
#    show_template =  'appbuilder/general/model/show_cascade.html'
#    list_template = 'appbuilder/general/model/list.html'
#    add_template = 'appbuilder/general/model/add.html'
#    edit_template = 'appbuilder/general/model/edit.html'
#    add_widget = (FormVerticalWidget|FormInlineWidget)
#    show_widget = ShowBlockWidget
#    list_widget = (ListThumbnail|ListWidget)
#    base_order = ('name', 'asc')
#    list_widget= 'list_widget'


class IndividualDetailView(ModelView):
    datamodel=SQLAInterface(Individual, db.session)
    related_views = []
    show_title='Individual Detail'
    add_title ='Add Individual'
    list_title= 'Individual List'
    edit_title = 'Edit Individual'
    show_columns = ['id', 'userx', 'is_individual', 'is_institution', 'is_company', 'is_government', 'is_online']
#    show_exclude_columns = [] #= ['id', 'userx', 'is_individual', 'is_institution', 'is_company', 'is_government', 'is_online']
#
#    add_columns = ['id', 'userx', 'is_individual', 'is_institution', 'is_company', 'is_government', 'is_online']
#    add_exclude_columns = [hide_list] #['id', 'userx', 'is_individual', 'is_institution', 'is_company', 'is_government', 'is_online']
#
#    edit_columns = ['id', 'userx', 'is_individual', 'is_institution', 'is_company', 'is_government', 'is_online']
#    edit_exclude_columns =[hide_list] # ['id', 'userx', 'is_individual', 'is_institution', 'is_company', 'is_government', 'is_online']
#
#    list_columns = ['id', 'userx', 'is_individual', 'is_institution', 'is_company', 'is_government', 'is_online']
#    list_exclude_columns = [] # ['id', 'userx', 'is_individual', 'is_institution', 'is_company', 'is_government', 'is_online']
#
#    search_columns = ['id', 'userx', 'is_individual', 'is_institution', 'is_company', 'is_government', 'is_online']
#    search_exclude_columns= [] # ['id', 'userx', 'is_individual', 'is_institution', 'is_company', 'is_government', 'is_online']
#
#    default_sort = [('id', True)]
#    base_permissions = ['can_list', 'can_show', 'can_edit', 'can_delete', 'can_add']
#    label_columns=   [{column.name: column.name for column in table.columns} ]
#    show_template =  'appbuilder/general/model/show_cascade.html'
#    list_template = 'appbuilder/general/model/list.html'
#    add_template = 'appbuilder/general/model/add.html'
#    edit_template = 'appbuilder/general/model/edit.html'
#    add_widget = (FormVerticalWidget|FormInlineWidget)
#    show_widget = ShowBlockWidget
#    list_widget = (ListThumbnail|ListWidget)
#    base_order = ('name', 'asc')
#    list_widget= 'list_widget'


class IndustryDetailView(ModelView):
    datamodel=SQLAInterface(Industry, db.session)
    related_views = []
    show_title='Industry Detail'
    add_title ='Add Industry'
    list_title= 'Industry List'
    edit_title = 'Edit Industry'
    show_columns = ['industry', 'job']
#    show_exclude_columns = [] #= ['industry', 'job']
#
#    add_columns = ['industry', 'job']
#    add_exclude_columns = [hide_list] #['industry', 'job']
#
#    edit_columns = ['industry', 'job']
#    edit_exclude_columns =[hide_list] # ['industry', 'job']
#
#    list_columns = ['industry', 'job']
#    list_exclude_columns = [] # ['industry', 'job']
#
#    search_columns = ['industry', 'job']
#    search_exclude_columns= [] # ['industry', 'job']
#
#    default_sort = [('id', True)]
#    base_permissions = ['can_list', 'can_show', 'can_edit', 'can_delete', 'can_add']
#    label_columns=   [{column.name: column.name for column in table.columns} ]
#    show_template =  'appbuilder/general/model/show_cascade.html'
#    list_template = 'appbuilder/general/model/list.html'
#    add_template = 'appbuilder/general/model/add.html'
#    edit_template = 'appbuilder/general/model/edit.html'
#    add_widget = (FormVerticalWidget|FormInlineWidget)
#    show_widget = ShowBlockWidget
#    list_widget = (ListThumbnail|ListWidget)
#    base_order = ('name', 'asc')
#    list_widget= 'list_widget'


class IndustryJobDetailView(ModelView):
    datamodel=SQLAInterface(IndustryJob, db.session)
    related_views = []
    show_title='IndustryJob Detail'
    add_title ='Add IndustryJob'
    list_title= 'IndustryJob List'
    edit_title = 'Edit IndustryJob'
    show_columns = ['industry', 'job']
#    show_exclude_columns = [] #= ['industry', 'job']
#
#    add_columns = ['industry', 'job']
#    add_exclude_columns = [hide_list] #['industry', 'job']
#
#    edit_columns = ['industry', 'job']
#    edit_exclude_columns =[hide_list] # ['industry', 'job']
#
#    list_columns = ['industry', 'job']
#    list_exclude_columns = [] # ['industry', 'job']
#
#    search_columns = ['industry', 'job']
#    search_exclude_columns= [] # ['industry', 'job']
#
#    default_sort = [('id', True)]
#    base_permissions = ['can_list', 'can_show', 'can_edit', 'can_delete', 'can_add']
#    label_columns=   [{column.name: column.name for column in table.columns} ]
#    show_template =  'appbuilder/general/model/show_cascade.html'
#    list_template = 'appbuilder/general/model/list.html'
#    add_template = 'appbuilder/general/model/add.html'
#    edit_template = 'appbuilder/general/model/edit.html'
#    add_widget = (FormVerticalWidget|FormInlineWidget)
#    show_widget = ShowBlockWidget
#    list_widget = (ListThumbnail|ListWidget)
#    base_order = ('name', 'asc')
#    list_widget= 'list_widget'


class JobDetailView(ModelView):
    datamodel=SQLAInterface(Job, db.session)
    related_views = []
    show_title='Job Detail'
    add_title ='Add Job'
    list_title= 'Job List'
    edit_title = 'Edit Job'
    show_columns = ['industry', 'job']
#    show_exclude_columns = [] #= ['industry', 'job']
#
#    add_columns = ['industry', 'job']
#    add_exclude_columns = [hide_list] #['industry', 'job']
#
#    edit_columns = ['industry', 'job']
#    edit_exclude_columns =[hide_list] # ['industry', 'job']
#
#    list_columns = ['industry', 'job']
#    list_exclude_columns = [] # ['industry', 'job']
#
#    search_columns = ['industry', 'job']
#    search_exclude_columns= [] # ['industry', 'job']
#
#    default_sort = [('id', True)]
#    base_permissions = ['can_list', 'can_show', 'can_edit', 'can_delete', 'can_add']
#    label_columns=   [{column.name: column.name for column in table.columns} ]
#    show_template =  'appbuilder/general/model/show_cascade.html'
#    list_template = 'appbuilder/general/model/list.html'
#    add_template = 'appbuilder/general/model/add.html'
#    edit_template = 'appbuilder/general/model/edit.html'
#    add_widget = (FormVerticalWidget|FormInlineWidget)
#    show_widget = ShowBlockWidget
#    list_widget = (ListThumbnail|ListWidget)
#    base_order = ('name', 'asc')
#    list_widget= 'list_widget'




class SkillDetailView(ModelView):
    datamodel=SQLAInterface(Skill, db.session)
    related_views = []
    show_title='Skill Detail'
    add_title ='Add Skill'
    list_title= 'Skill List'
    edit_title = 'Edit Skill'
    show_columns = ['skills', 'jobs']
#    show_exclude_columns = [] #= ['skills', 'jobs']
#
#    add_columns = ['skills', 'jobs']
#    add_exclude_columns = [hide_list] #['skills', 'jobs']
#
#    edit_columns = ['skills', 'jobs']
#    edit_exclude_columns =[hide_list] # ['skills', 'jobs']
#
#    list_columns = ['skills', 'jobs']
#    list_exclude_columns = [] # ['skills', 'jobs']
#
#    search_columns = ['skills', 'jobs']
#    search_exclude_columns= [] # ['skills', 'jobs']
#
#    default_sort = [('id', True)]
#    base_permissions = ['can_list', 'can_show', 'can_edit', 'can_delete', 'can_add']
#    label_columns=   [{column.name: column.name for column in table.columns} ]
#    show_template =  'appbuilder/general/model/show_cascade.html'
#    list_template = 'appbuilder/general/model/list.html'
#    add_template = 'appbuilder/general/model/add.html'
#    edit_template = 'appbuilder/general/model/edit.html'
#    add_widget = (FormVerticalWidget|FormInlineWidget)
#    show_widget = ShowBlockWidget
#    list_widget = (ListThumbnail|ListWidget)
#    base_order = ('name', 'asc')
#    list_widget= 'list_widget'


class JobSkillDetailView(ModelView):
    datamodel=SQLAInterface(JobSkill, db.session)
    related_views = []
    show_title='JobSkill Detail'
    add_title ='Add JobSkill'
    list_title= 'JobSkill List'
    edit_title = 'Edit JobSkill'
    show_columns = ['skills', 'jobs']
#    show_exclude_columns = [] #= ['skills', 'jobs']
#
#    add_columns = ['skills', 'jobs']
#    add_exclude_columns = [hide_list] #['skills', 'jobs']
#
#    edit_columns = ['skills', 'jobs']
#    edit_exclude_columns =[hide_list] # ['skills', 'jobs']
#
#    list_columns = ['skills', 'jobs']
#    list_exclude_columns = [] # ['skills', 'jobs']
#
#    search_columns = ['skills', 'jobs']
#    search_exclude_columns= [] # ['skills', 'jobs']
#
#    default_sort = [('id', True)]
#    base_permissions = ['can_list', 'can_show', 'can_edit', 'can_delete', 'can_add']
#    label_columns=   [{column.name: column.name for column in table.columns} ]
#    show_template =  'appbuilder/general/model/show_cascade.html'
#    list_template = 'appbuilder/general/model/list.html'
#    add_template = 'appbuilder/general/model/add.html'
#    edit_template = 'appbuilder/general/model/edit.html'
#    add_widget = (FormVerticalWidget|FormInlineWidget)
#    show_widget = ShowBlockWidget
#    list_widget = (ListThumbnail|ListWidget)
#    base_order = ('name', 'asc')
#    list_widget= 'list_widget'


class IndividualMasterView(MasterDetailView):
    datamodel=SQLAInterface(Individual, db.session)
    related_views = [UserxDetailView]
    show_title='Individual Detail'
    add_title ='Add Individual'
    list_title= 'Individual List'
    edit_title = 'Edit Individual'
    show_columns = ['id', 'userx', 'is_individual', 'is_institution', 'is_company', 'is_government', 'is_online']
#    show_exclude_columns = [] #= ['id', 'userx', 'is_individual', 'is_institution', 'is_company', 'is_government', 'is_online']
#
#    add_columns = ['id', 'userx', 'is_individual', 'is_institution', 'is_company', 'is_government', 'is_online']
#    add_exclude_columns = [hide_list] #['id', 'userx', 'is_individual', 'is_institution', 'is_company', 'is_government', 'is_online']
#
#    edit_columns = ['id', 'userx', 'is_individual', 'is_institution', 'is_company', 'is_government', 'is_online']
#    edit_exclude_columns =[hide_list] # ['id', 'userx', 'is_individual', 'is_institution', 'is_company', 'is_government', 'is_online']
#
#    list_columns = ['id', 'userx', 'is_individual', 'is_institution', 'is_company', 'is_government', 'is_online']
#    list_exclude_columns = [] # ['id', 'userx', 'is_individual', 'is_institution', 'is_company', 'is_government', 'is_online']
#
#    search_columns = ['id', 'userx', 'is_individual', 'is_institution', 'is_company', 'is_government', 'is_online']
#    search_exclude_columns= [] # ['id', 'userx', 'is_individual', 'is_institution', 'is_company', 'is_government', 'is_online']
#
#    default_sort = [('id', True)]
#    base_permissions = ['can_list', 'can_show', 'can_edit', 'can_delete', 'can_add']
#    label_columns=   [{column.name: column.name for column in table.columns} ]
#    show_template =  'appbuilder/general/model/show_cascade.html'
#    list_template = 'appbuilder/general/model/list.html'
#    add_template = 'appbuilder/general/model/add.html'
#    edit_template = 'appbuilder/general/model/edit.html'
#    add_widget = (FormVerticalWidget|FormInlineWidget)
#    show_widget = ShowBlockWidget
#    list_widget = (ListThumbnail|ListWidget)
#    base_order = ('name', 'asc')
#    list_widget= 'list_widget'


class IndustryJobMasterView(MasterDetailView):
    datamodel=SQLAInterface(IndustryJob, db.session)
    related_views = [IndustryDetailView]
    show_title='IndustryJob Detail'
    add_title ='Add IndustryJob'
    list_title= 'IndustryJob List'
    edit_title = 'Edit IndustryJob'
    show_columns = ['industry', 'job']
#    show_exclude_columns = [] #= ['industry', 'job']
#
#    add_columns = ['industry', 'job']
#    add_exclude_columns = [hide_list] #['industry', 'job']
#
#    edit_columns = ['industry', 'job']
#    edit_exclude_columns =[hide_list] # ['industry', 'job']
#
#    list_columns = ['industry', 'job']
#    list_exclude_columns = [] # ['industry', 'job']
#
#    search_columns = ['industry', 'job']
#    search_exclude_columns= [] # ['industry', 'job']
#
#    default_sort = [('id', True)]
#    base_permissions = ['can_list', 'can_show', 'can_edit', 'can_delete', 'can_add']
#    label_columns=   [{column.name: column.name for column in table.columns} ]
#    show_template =  'appbuilder/general/model/show_cascade.html'
#    list_template = 'appbuilder/general/model/list.html'
#    add_template = 'appbuilder/general/model/add.html'
#    edit_template = 'appbuilder/general/model/edit.html'
#    add_widget = (FormVerticalWidget|FormInlineWidget)
#    show_widget = ShowBlockWidget
#    list_widget = (ListThumbnail|ListWidget)
#    base_order = ('name', 'asc')
#    list_widget= 'list_widget'


class IndustryJobMultiView(MultipleView):
    datamodel=SQLAInterface(IndustryJob, db.session)
    views = [IndustryDetailView, JobDetailView]
    show_title='IndustryJob Detail'
    add_title ='Add IndustryJob'
    list_title= 'IndustryJob List'
    edit_title = 'Edit IndustryJob'
    show_columns = ['industry', 'job']
#    show_exclude_columns = [] #= ['industry', 'job']
#
#    add_columns = ['industry', 'job']
#    add_exclude_columns = [hide_list] #['industry', 'job']
#
#    edit_columns = ['industry', 'job']
#    edit_exclude_columns =[hide_list] # ['industry', 'job']
#
#    list_columns = ['industry', 'job']
#    list_exclude_columns = [] # ['industry', 'job']
#
#    search_columns = ['industry', 'job']
#    search_exclude_columns= [] # ['industry', 'job']
#
#    default_sort = [('id', True)]
#    base_permissions = ['can_list', 'can_show', 'can_edit', 'can_delete', 'can_add']
#    label_columns=   [{column.name: column.name for column in table.columns} ]
#    show_template =  'appbuilder/general/model/show_cascade.html'
#    list_template = 'appbuilder/general/model/list.html'
#    add_template = 'appbuilder/general/model/add.html'
#    edit_template = 'appbuilder/general/model/edit.html'
#    add_widget = (FormVerticalWidget|FormInlineWidget)
#    show_widget = ShowBlockWidget
#    list_widget = (ListThumbnail|ListWidget)
#    base_order = ('name', 'asc')
#    list_widget= 'list_widget'


class JobSkillMasterView(MasterDetailView):
    datamodel=SQLAInterface(JobSkill, db.session)
    related_views = [JobDetailView]
    show_title='JobSkill Detail'
    add_title ='Add JobSkill'
    list_title= 'JobSkill List'
    edit_title = 'Edit JobSkill'
    show_columns = ['skills', 'jobs']
#    show_exclude_columns = [] #= ['skills', 'jobs']
#
#    add_columns = ['skills', 'jobs']
#    add_exclude_columns = [hide_list] #['skills', 'jobs']
#
#    edit_columns = ['skills', 'jobs']
#    edit_exclude_columns =[hide_list] # ['skills', 'jobs']
#
#    list_columns = ['skills', 'jobs']
#    list_exclude_columns = [] # ['skills', 'jobs']
#
#    search_columns = ['skills', 'jobs']
#    search_exclude_columns= [] # ['skills', 'jobs']
#
#    default_sort = [('id', True)]
#    base_permissions = ['can_list', 'can_show', 'can_edit', 'can_delete', 'can_add']
#    label_columns=   [{column.name: column.name for column in table.columns} ]
#    show_template =  'appbuilder/general/model/show_cascade.html'
#    list_template = 'appbuilder/general/model/list.html'
#    add_template = 'appbuilder/general/model/add.html'
#    edit_template = 'appbuilder/general/model/edit.html'
#    add_widget = (FormVerticalWidget|FormInlineWidget)
#    show_widget = ShowBlockWidget
#    list_widget = (ListThumbnail|ListWidget)
#    base_order = ('name', 'asc')
#    list_widget= 'list_widget'


class JobSkillMultiView(MultipleView):
    datamodel=SQLAInterface(JobSkill, db.session)
    views = [SkillDetailView]
    show_title='JobSkill Detail'
    add_title ='Add JobSkill'
    list_title= 'JobSkill List'
    edit_title = 'Edit JobSkill'
    show_columns = ['skills', 'jobs']
#    show_exclude_columns = [] #= ['skills', 'jobs']
#
#    add_columns = ['skills', 'jobs']
#    add_exclude_columns = [hide_list] #['skills', 'jobs']
#
#    edit_columns = ['skills', 'jobs']
#    edit_exclude_columns =[hide_list] # ['skills', 'jobs']
#
#    list_columns = ['skills', 'jobs']
#    list_exclude_columns = [] # ['skills', 'jobs']
#
#    search_columns = ['skills', 'jobs']
#    search_exclude_columns= [] # ['skills', 'jobs']
#
#    default_sort = [('id', True)]
#    base_permissions = ['can_list', 'can_show', 'can_edit', 'can_delete', 'can_add']
#    label_columns=   [{column.name: column.name for column in table.columns} ]
#    show_template =  'appbuilder/general/model/show_cascade.html'
#    list_template = 'appbuilder/general/model/list.html'
#    add_template = 'appbuilder/general/model/add.html'
#    edit_template = 'appbuilder/general/model/edit.html'
#    add_widget = (FormVerticalWidget|FormInlineWidget)
#    show_widget = ShowBlockWidget
#    list_widget = (ListThumbnail|ListWidget)
#    base_order = ('name', 'asc')
#    list_widget= 'list_widget'


class EducationMasterView(MasterDetailView):
    datamodel=SQLAInterface(Education, db.session)
    related_views = [IndividualDetailView]
    show_title='Education Detail'
    add_title ='Add Education'
    list_title= 'Education List'
    edit_title = 'Edit Education'
    show_columns = ['id', 'individual', 'qualification', 'qual_class', 'verified', 'verification_code', 'verified_by', 'verification_date', 'verification_doc']
#    show_exclude_columns = [] #= ['id', 'individual', 'qualification', 'qual_class', 'verified', 'verification_code', 'verified_by', 'verification_date', 'verification_doc']
#
#    add_columns = ['id', 'individual', 'qualification', 'qual_class', 'verified', 'verification_code', 'verified_by', 'verification_date', 'verification_doc']
#    add_exclude_columns = [hide_list] #['id', 'individual', 'qualification', 'qual_class', 'verified', 'verification_code', 'verified_by', 'verification_date', 'verification_doc']
#
#    edit_columns = ['id', 'individual', 'qualification', 'qual_class', 'verified', 'verification_code', 'verified_by', 'verification_date', 'verification_doc']
#    edit_exclude_columns =[hide_list] # ['id', 'individual', 'qualification', 'qual_class', 'verified', 'verification_code', 'verified_by', 'verification_date', 'verification_doc']
#
#    list_columns = ['id', 'individual', 'qualification', 'qual_class', 'verified', 'verification_code', 'verified_by', 'verification_date', 'verification_doc']
#    list_exclude_columns = [] # ['id', 'individual', 'qualification', 'qual_class', 'verified', 'verification_code', 'verified_by', 'verification_date', 'verification_doc']
#
#    search_columns = ['id', 'individual', 'qualification', 'qual_class', 'verified', 'verification_code', 'verified_by', 'verification_date', 'verification_doc']
#    search_exclude_columns= [] # ['id', 'individual', 'qualification', 'qual_class', 'verified', 'verification_code', 'verified_by', 'verification_date', 'verification_doc']
#
#    default_sort = [('id', True)]
#    base_permissions = ['can_list', 'can_show', 'can_edit', 'can_delete', 'can_add']
#    label_columns=   [{column.name: column.name for column in table.columns} ]
#    show_template =  'appbuilder/general/model/show_cascade.html'
#    list_template = 'appbuilder/general/model/list.html'
#    add_template = 'appbuilder/general/model/add.html'
#    edit_template = 'appbuilder/general/model/edit.html'
#    add_widget = (FormVerticalWidget|FormInlineWidget)
#    show_widget = ShowBlockWidget
#    list_widget = (ListThumbnail|ListWidget)
#    base_order = ('name', 'asc')
#    list_widget= 'list_widget'


class IndividualJobMasterView(MasterDetailView):
    datamodel=SQLAInterface(IndividualJob, db.session)
    related_views = [IndividualDetailView]
    show_title='IndividualJob Detail'
    add_title ='Add IndividualJob'
    list_title= 'IndividualJob List'
    edit_title = 'Edit IndividualJob'
    show_columns = ['individual', 'job']
#    show_exclude_columns = [] #= ['individual', 'job']
#
#    add_columns = ['individual', 'job']
#    add_exclude_columns = [hide_list] #['individual', 'job']
#
#    edit_columns = ['individual', 'job']
#    edit_exclude_columns =[hide_list] # ['individual', 'job']
#
#    list_columns = ['individual', 'job']
#    list_exclude_columns = [] # ['individual', 'job']
#
#    search_columns = ['individual', 'job']
#    search_exclude_columns= [] # ['individual', 'job']
#
#    default_sort = [('id', True)]
#    base_permissions = ['can_list', 'can_show', 'can_edit', 'can_delete', 'can_add']
#    label_columns=   [{column.name: column.name for column in table.columns} ]
#    show_template =  'appbuilder/general/model/show_cascade.html'
#    list_template = 'appbuilder/general/model/list.html'
#    add_template = 'appbuilder/general/model/add.html'
#    edit_template = 'appbuilder/general/model/edit.html'
#    add_widget = (FormVerticalWidget|FormInlineWidget)
#    show_widget = ShowBlockWidget
#    list_widget = (ListThumbnail|ListWidget)
#    base_order = ('name', 'asc')
#    list_widget= 'list_widget'


class IndividualJobMultiView(MultipleView):
    datamodel=SQLAInterface(IndividualJob, db.session)
    views = []
    show_title='IndividualJob Detail'
    add_title ='Add IndividualJob'
    list_title= 'IndividualJob List'
    edit_title = 'Edit IndividualJob'
    show_columns = ['individual', 'job']
#    show_exclude_columns = [] #= ['individual', 'job']
#
#    add_columns = ['individual', 'job']
#    add_exclude_columns = [hide_list] #['individual', 'job']
#
#    edit_columns = ['individual', 'job']
#    edit_exclude_columns =[hide_list] # ['individual', 'job']
#
#    list_columns = ['individual', 'job']
#    list_exclude_columns = [] # ['individual', 'job']
#
#    search_columns = ['individual', 'job']
#    search_exclude_columns= [] # ['individual', 'job']
#
#    default_sort = [('id', True)]
#    base_permissions = ['can_list', 'can_show', 'can_edit', 'can_delete', 'can_add']
#    label_columns=   [{column.name: column.name for column in table.columns} ]
#    show_template =  'appbuilder/general/model/show_cascade.html'
#    list_template = 'appbuilder/general/model/list.html'
#    add_template = 'appbuilder/general/model/add.html'
#    edit_template = 'appbuilder/general/model/edit.html'
#    add_widget = (FormVerticalWidget|FormInlineWidget)
#    show_widget = ShowBlockWidget
#    list_widget = (ListThumbnail|ListWidget)
#    base_order = ('name', 'asc')
#    list_widget= 'list_widget'


class ProfilesourceView(ModelView):
    datamodel=SQLAInterface(Profilesource, db.session)
    related_views = []
    show_title='Profilesource Detail'
    add_title ='Add Profilesource'
    list_title= 'Profilesource List'
    edit_title = 'Edit Profilesource'
    show_columns = ['id', 'import_script']
#    show_exclude_columns = [] #= ['id', 'import_script']
#
#    add_columns = ['id', 'import_script']
#    add_exclude_columns = [hide_list] #['id', 'import_script']
#
#    edit_columns = ['id', 'import_script']
#    edit_exclude_columns =[hide_list] # ['id', 'import_script']
#
#    list_columns = ['id', 'import_script']
#    list_exclude_columns = [] # ['id', 'import_script']
#
#    search_columns = ['id', 'import_script']
#    search_exclude_columns= [] # ['id', 'import_script']
#
#    default_sort = [('id', True)]
#    base_permissions = ['can_list', 'can_show', 'can_edit', 'can_delete', 'can_add']
#    label_columns=   [{column.name: column.name for column in table.columns} ]
#    show_template =  'appbuilder/general/model/show_cascade.html'
#    list_template = 'appbuilder/general/model/list.html'
#    add_template = 'appbuilder/general/model/add.html'
#    edit_template = 'appbuilder/general/model/edit.html'
#    add_widget = (FormVerticalWidget|FormInlineWidget)
#    show_widget = ShowBlockWidget
#    list_widget = (ListThumbnail|ListWidget)
#    base_order = ('name', 'asc')
#    list_widget= 'list_widget'


class LocationView(ModelView):
    datamodel=SQLAInterface(Location, db.session)
    related_views = []
    show_title='Location Detail'
    add_title ='Add Location'
    list_title= 'Location List'
    edit_title = 'Edit Location'
    show_columns = ['id', 'individual']
#    show_exclude_columns = [] #= ['id', 'individual']
#
#    add_columns = ['id', 'individual']
#    add_exclude_columns = [hide_list] #['id', 'individual']
#
#    edit_columns = ['id', 'individual']
#    edit_exclude_columns =[hide_list] # ['id', 'individual']
#
#    list_columns = ['id', 'individual']
#    list_exclude_columns = [] # ['id', 'individual']
#
#    search_columns = ['id', 'individual']
#    search_exclude_columns= [] # ['id', 'individual']
#
#    default_sort = [('id', True)]
#    base_permissions = ['can_list', 'can_show', 'can_edit', 'can_delete', 'can_add']
#    label_columns=   [{column.name: column.name for column in table.columns} ]
#    show_template =  'appbuilder/general/model/show_cascade.html'
#    list_template = 'appbuilder/general/model/list.html'
#    add_template = 'appbuilder/general/model/add.html'
#    edit_template = 'appbuilder/general/model/edit.html'
#    add_widget = (FormVerticalWidget|FormInlineWidget)
#    show_widget = ShowBlockWidget
#    list_widget = (ListThumbnail|ListWidget)
#    base_order = ('name', 'asc')
#    list_widget= 'list_widget'


class UserxDetailView(ModelView):
    datamodel=SQLAInterface(Userx, db.session)
    related_views = []
    show_title='Userx Detail'
    add_title ='Add Userx'
    list_title= 'Userx List'
    edit_title = 'Edit Userx'
    show_columns = ['id', 'userx', 'is_individual', 'is_institution', 'is_company', 'is_government', 'is_online']
#    show_exclude_columns = [] #= ['id', 'userx', 'is_individual', 'is_institution', 'is_company', 'is_government', 'is_online']
#
#    add_columns = ['id', 'userx', 'is_individual', 'is_institution', 'is_company', 'is_government', 'is_online']
#    add_exclude_columns = [hide_list] #['id', 'userx', 'is_individual', 'is_institution', 'is_company', 'is_government', 'is_online']
#
#    edit_columns = ['id', 'userx', 'is_individual', 'is_institution', 'is_company', 'is_government', 'is_online']
#    edit_exclude_columns =[hide_list] # ['id', 'userx', 'is_individual', 'is_institution', 'is_company', 'is_government', 'is_online']
#
#    list_columns = ['id', 'userx', 'is_individual', 'is_institution', 'is_company', 'is_government', 'is_online']
#    list_exclude_columns = [] # ['id', 'userx', 'is_individual', 'is_institution', 'is_company', 'is_government', 'is_online']
#
#    search_columns = ['id', 'userx', 'is_individual', 'is_institution', 'is_company', 'is_government', 'is_online']
#    search_exclude_columns= [] # ['id', 'userx', 'is_individual', 'is_institution', 'is_company', 'is_government', 'is_online']
#
#    default_sort = [('id', True)]
#    base_permissions = ['can_list', 'can_show', 'can_edit', 'can_delete', 'can_add']
#    label_columns=   [{column.name: column.name for column in table.columns} ]
#    show_template =  'appbuilder/general/model/show_cascade.html'
#    list_template = 'appbuilder/general/model/list.html'
#    add_template = 'appbuilder/general/model/add.html'
#    edit_template = 'appbuilder/general/model/edit.html'
#    add_widget = (FormVerticalWidget|FormInlineWidget)
#    show_widget = ShowBlockWidget
#    list_widget = (ListThumbnail|ListWidget)
#    base_order = ('name', 'asc')
#    list_widget= 'list_widget'


class IndividualDetailView(ModelView):
    datamodel=SQLAInterface(Individual, db.session)
    related_views = []
    show_title='Individual Detail'
    add_title ='Add Individual'
    list_title= 'Individual List'
    edit_title = 'Edit Individual'
    show_columns = ['id', 'userx', 'is_individual', 'is_institution', 'is_company', 'is_government', 'is_online']
#    show_exclude_columns = [] #= ['id', 'userx', 'is_individual', 'is_institution', 'is_company', 'is_government', 'is_online']
#
#    add_columns = ['id', 'userx', 'is_individual', 'is_institution', 'is_company', 'is_government', 'is_online']
#    add_exclude_columns = [hide_list] #['id', 'userx', 'is_individual', 'is_institution', 'is_company', 'is_government', 'is_online']
#
#    edit_columns = ['id', 'userx', 'is_individual', 'is_institution', 'is_company', 'is_government', 'is_online']
#    edit_exclude_columns =[hide_list] # ['id', 'userx', 'is_individual', 'is_institution', 'is_company', 'is_government', 'is_online']
#
#    list_columns = ['id', 'userx', 'is_individual', 'is_institution', 'is_company', 'is_government', 'is_online']
#    list_exclude_columns = [] # ['id', 'userx', 'is_individual', 'is_institution', 'is_company', 'is_government', 'is_online']
#
#    search_columns = ['id', 'userx', 'is_individual', 'is_institution', 'is_company', 'is_government', 'is_online']
#    search_exclude_columns= [] # ['id', 'userx', 'is_individual', 'is_institution', 'is_company', 'is_government', 'is_online']
#
#    default_sort = [('id', True)]
#    base_permissions = ['can_list', 'can_show', 'can_edit', 'can_delete', 'can_add']
#    label_columns=   [{column.name: column.name for column in table.columns} ]
#    show_template =  'appbuilder/general/model/show_cascade.html'
#    list_template = 'appbuilder/general/model/list.html'
#    add_template = 'appbuilder/general/model/add.html'
#    edit_template = 'appbuilder/general/model/edit.html'
#    add_widget = (FormVerticalWidget|FormInlineWidget)
#    show_widget = ShowBlockWidget
#    list_widget = (ListThumbnail|ListWidget)
#    base_order = ('name', 'asc')
#    list_widget= 'list_widget'


class IndustryDetailView(ModelView):
    datamodel=SQLAInterface(Industry, db.session)
    related_views = []
    show_title='Industry Detail'
    add_title ='Add Industry'
    list_title= 'Industry List'
    edit_title = 'Edit Industry'
    show_columns = ['industry', 'job']
#    show_exclude_columns = [] #= ['industry', 'job']
#
#    add_columns = ['industry', 'job']
#    add_exclude_columns = [hide_list] #['industry', 'job']
#
#    edit_columns = ['industry', 'job']
#    edit_exclude_columns =[hide_list] # ['industry', 'job']
#
#    list_columns = ['industry', 'job']
#    list_exclude_columns = [] # ['industry', 'job']
#
#    search_columns = ['industry', 'job']
#    search_exclude_columns= [] # ['industry', 'job']
#
#    default_sort = [('id', True)]
#    base_permissions = ['can_list', 'can_show', 'can_edit', 'can_delete', 'can_add']
#    label_columns=   [{column.name: column.name for column in table.columns} ]
#    show_template =  'appbuilder/general/model/show_cascade.html'
#    list_template = 'appbuilder/general/model/list.html'
#    add_template = 'appbuilder/general/model/add.html'
#    edit_template = 'appbuilder/general/model/edit.html'
#    add_widget = (FormVerticalWidget|FormInlineWidget)
#    show_widget = ShowBlockWidget
#    list_widget = (ListThumbnail|ListWidget)
#    base_order = ('name', 'asc')
#    list_widget= 'list_widget'


class IndustryJobDetailView(ModelView):
    datamodel=SQLAInterface(IndustryJob, db.session)
    related_views = []
    show_title='IndustryJob Detail'
    add_title ='Add IndustryJob'
    list_title= 'IndustryJob List'
    edit_title = 'Edit IndustryJob'
    show_columns = ['industry', 'job']
#    show_exclude_columns = [] #= ['industry', 'job']
#
#    add_columns = ['industry', 'job']
#    add_exclude_columns = [hide_list] #['industry', 'job']
#
#    edit_columns = ['industry', 'job']
#    edit_exclude_columns =[hide_list] # ['industry', 'job']
#
#    list_columns = ['industry', 'job']
#    list_exclude_columns = [] # ['industry', 'job']
#
#    search_columns = ['industry', 'job']
#    search_exclude_columns= [] # ['industry', 'job']
#
#    default_sort = [('id', True)]
#    base_permissions = ['can_list', 'can_show', 'can_edit', 'can_delete', 'can_add']
#    label_columns=   [{column.name: column.name for column in table.columns} ]
#    show_template =  'appbuilder/general/model/show_cascade.html'
#    list_template = 'appbuilder/general/model/list.html'
#    add_template = 'appbuilder/general/model/add.html'
#    edit_template = 'appbuilder/general/model/edit.html'
#    add_widget = (FormVerticalWidget|FormInlineWidget)
#    show_widget = ShowBlockWidget
#    list_widget = (ListThumbnail|ListWidget)
#    base_order = ('name', 'asc')
#    list_widget= 'list_widget'


class JobDetailView(ModelView):
    datamodel=SQLAInterface(Job, db.session)
    related_views = []
    show_title='Job Detail'
    add_title ='Add Job'
    list_title= 'Job List'
    edit_title = 'Edit Job'
    show_columns = ['industry', 'job']
#    show_exclude_columns = [] #= ['industry', 'job']
#
#    add_columns = ['industry', 'job']
#    add_exclude_columns = [hide_list] #['industry', 'job']
#
#    edit_columns = ['industry', 'job']
#    edit_exclude_columns =[hide_list] # ['industry', 'job']
#
#    list_columns = ['industry', 'job']
#    list_exclude_columns = [] # ['industry', 'job']
#
#    search_columns = ['industry', 'job']
#    search_exclude_columns= [] # ['industry', 'job']
#
#    default_sort = [('id', True)]
#    base_permissions = ['can_list', 'can_show', 'can_edit', 'can_delete', 'can_add']
#    label_columns=   [{column.name: column.name for column in table.columns} ]
#    show_template =  'appbuilder/general/model/show_cascade.html'
#    list_template = 'appbuilder/general/model/list.html'
#    add_template = 'appbuilder/general/model/add.html'
#    edit_template = 'appbuilder/general/model/edit.html'
#    add_widget = (FormVerticalWidget|FormInlineWidget)
#    show_widget = ShowBlockWidget
#    list_widget = (ListThumbnail|ListWidget)
#    base_order = ('name', 'asc')
#    list_widget= 'list_widget'




class SkillDetailView(ModelView):
    datamodel=SQLAInterface(Skill, db.session)
    related_views = []
    show_title='Skill Detail'
    add_title ='Add Skill'
    list_title= 'Skill List'
    edit_title = 'Edit Skill'
    show_columns = ['skills', 'jobs']
#    show_exclude_columns = [] #= ['skills', 'jobs']
#
#    add_columns = ['skills', 'jobs']
#    add_exclude_columns = [hide_list] #['skills', 'jobs']
#
#    edit_columns = ['skills', 'jobs']
#    edit_exclude_columns =[hide_list] # ['skills', 'jobs']
#
#    list_columns = ['skills', 'jobs']
#    list_exclude_columns = [] # ['skills', 'jobs']
#
#    search_columns = ['skills', 'jobs']
#    search_exclude_columns= [] # ['skills', 'jobs']
#
#    default_sort = [('id', True)]
#    base_permissions = ['can_list', 'can_show', 'can_edit', 'can_delete', 'can_add']
#    label_columns=   [{column.name: column.name for column in table.columns} ]
#    show_template =  'appbuilder/general/model/show_cascade.html'
#    list_template = 'appbuilder/general/model/list.html'
#    add_template = 'appbuilder/general/model/add.html'
#    edit_template = 'appbuilder/general/model/edit.html'
#    add_widget = (FormVerticalWidget|FormInlineWidget)
#    show_widget = ShowBlockWidget
#    list_widget = (ListThumbnail|ListWidget)
#    base_order = ('name', 'asc')
#    list_widget= 'list_widget'


class JobSkillDetailView(ModelView):
    datamodel=SQLAInterface(JobSkill, db.session)
    related_views = []
    show_title='JobSkill Detail'
    add_title ='Add JobSkill'
    list_title= 'JobSkill List'
    edit_title = 'Edit JobSkill'
    show_columns = ['skills', 'jobs']
#    show_exclude_columns = [] #= ['skills', 'jobs']
#
#    add_columns = ['skills', 'jobs']
#    add_exclude_columns = [hide_list] #['skills', 'jobs']
#
#    edit_columns = ['skills', 'jobs']
#    edit_exclude_columns =[hide_list] # ['skills', 'jobs']
#
#    list_columns = ['skills', 'jobs']
#    list_exclude_columns = [] # ['skills', 'jobs']
#
#    search_columns = ['skills', 'jobs']
#    search_exclude_columns= [] # ['skills', 'jobs']
#
#    default_sort = [('id', True)]
#    base_permissions = ['can_list', 'can_show', 'can_edit', 'can_delete', 'can_add']
#    label_columns=   [{column.name: column.name for column in table.columns} ]
#    show_template =  'appbuilder/general/model/show_cascade.html'
#    list_template = 'appbuilder/general/model/list.html'
#    add_template = 'appbuilder/general/model/add.html'
#    edit_template = 'appbuilder/general/model/edit.html'
#    add_widget = (FormVerticalWidget|FormInlineWidget)
#    show_widget = ShowBlockWidget
#    list_widget = (ListThumbnail|ListWidget)
#    base_order = ('name', 'asc')
#    list_widget= 'list_widget'


class IndividualMasterView(MasterDetailView):
    datamodel=SQLAInterface(Individual, db.session)
    related_views = [UserxDetailView]
    show_title='Individual Detail'
    add_title ='Add Individual'
    list_title= 'Individual List'
    edit_title = 'Edit Individual'
    show_columns = ['id', 'userx', 'is_individual', 'is_institution', 'is_company', 'is_government', 'is_online']
#    show_exclude_columns = [] #= ['id', 'userx', 'is_individual', 'is_institution', 'is_company', 'is_government', 'is_online']
#
#    add_columns = ['id', 'userx', 'is_individual', 'is_institution', 'is_company', 'is_government', 'is_online']
#    add_exclude_columns = [hide_list] #['id', 'userx', 'is_individual', 'is_institution', 'is_company', 'is_government', 'is_online']
#
#    edit_columns = ['id', 'userx', 'is_individual', 'is_institution', 'is_company', 'is_government', 'is_online']
#    edit_exclude_columns =[hide_list] # ['id', 'userx', 'is_individual', 'is_institution', 'is_company', 'is_government', 'is_online']
#
#    list_columns = ['id', 'userx', 'is_individual', 'is_institution', 'is_company', 'is_government', 'is_online']
#    list_exclude_columns = [] # ['id', 'userx', 'is_individual', 'is_institution', 'is_company', 'is_government', 'is_online']
#
#    search_columns = ['id', 'userx', 'is_individual', 'is_institution', 'is_company', 'is_government', 'is_online']
#    search_exclude_columns= [] # ['id', 'userx', 'is_individual', 'is_institution', 'is_company', 'is_government', 'is_online']
#
#    default_sort = [('id', True)]
#    base_permissions = ['can_list', 'can_show', 'can_edit', 'can_delete', 'can_add']
#    label_columns=   [{column.name: column.name for column in table.columns} ]
#    show_template =  'appbuilder/general/model/show_cascade.html'
#    list_template = 'appbuilder/general/model/list.html'
#    add_template = 'appbuilder/general/model/add.html'
#    edit_template = 'appbuilder/general/model/edit.html'
#    add_widget = (FormVerticalWidget|FormInlineWidget)
#    show_widget = ShowBlockWidget
#    list_widget = (ListThumbnail|ListWidget)
#    base_order = ('name', 'asc')
#    list_widget= 'list_widget'


class IndustryJobMasterView(MasterDetailView):
    datamodel=SQLAInterface(IndustryJob, db.session)
    related_views = [IndustryDetailView]
    show_title='IndustryJob Detail'
    add_title ='Add IndustryJob'
    list_title= 'IndustryJob List'
    edit_title = 'Edit IndustryJob'
    show_columns = ['industry', 'job']
#    show_exclude_columns = [] #= ['industry', 'job']
#
#    add_columns = ['industry', 'job']
#    add_exclude_columns = [hide_list] #['industry', 'job']
#
#    edit_columns = ['industry', 'job']
#    edit_exclude_columns =[hide_list] # ['industry', 'job']
#
#    list_columns = ['industry', 'job']
#    list_exclude_columns = [] # ['industry', 'job']
#
#    search_columns = ['industry', 'job']
#    search_exclude_columns= [] # ['industry', 'job']
#
#    default_sort = [('id', True)]
#    base_permissions = ['can_list', 'can_show', 'can_edit', 'can_delete', 'can_add']
#    label_columns=   [{column.name: column.name for column in table.columns} ]
#    show_template =  'appbuilder/general/model/show_cascade.html'
#    list_template = 'appbuilder/general/model/list.html'
#    add_template = 'appbuilder/general/model/add.html'
#    edit_template = 'appbuilder/general/model/edit.html'
#    add_widget = (FormVerticalWidget|FormInlineWidget)
#    show_widget = ShowBlockWidget
#    list_widget = (ListThumbnail|ListWidget)
#    base_order = ('name', 'asc')
#    list_widget= 'list_widget'


class IndustryJobMultiView(MultipleView):
    datamodel=SQLAInterface(IndustryJob, db.session)
    views = [IndustryDetailView, JobDetailView]
    show_title='IndustryJob Detail'
    add_title ='Add IndustryJob'
    list_title= 'IndustryJob List'
    edit_title = 'Edit IndustryJob'
    show_columns = ['industry', 'job']
#    show_exclude_columns = [] #= ['industry', 'job']
#
#    add_columns = ['industry', 'job']
#    add_exclude_columns = [hide_list] #['industry', 'job']
#
#    edit_columns = ['industry', 'job']
#    edit_exclude_columns =[hide_list] # ['industry', 'job']
#
#    list_columns = ['industry', 'job']
#    list_exclude_columns = [] # ['industry', 'job']
#
#    search_columns = ['industry', 'job']
#    search_exclude_columns= [] # ['industry', 'job']
#
#    default_sort = [('id', True)]
#    base_permissions = ['can_list', 'can_show', 'can_edit', 'can_delete', 'can_add']
#    label_columns=   [{column.name: column.name for column in table.columns} ]
#    show_template =  'appbuilder/general/model/show_cascade.html'
#    list_template = 'appbuilder/general/model/list.html'
#    add_template = 'appbuilder/general/model/add.html'
#    edit_template = 'appbuilder/general/model/edit.html'
#    add_widget = (FormVerticalWidget|FormInlineWidget)
#    show_widget = ShowBlockWidget
#    list_widget = (ListThumbnail|ListWidget)
#    base_order = ('name', 'asc')
#    list_widget= 'list_widget'


class JobSkillMasterView(MasterDetailView):
    datamodel=SQLAInterface(JobSkill, db.session)
    related_views = [JobDetailView]
    show_title='JobSkill Detail'
    add_title ='Add JobSkill'
    list_title= 'JobSkill List'
    edit_title = 'Edit JobSkill'
    show_columns = ['skills', 'jobs']
#    show_exclude_columns = [] #= ['skills', 'jobs']
#
#    add_columns = ['skills', 'jobs']
#    add_exclude_columns = [hide_list] #['skills', 'jobs']
#
#    edit_columns = ['skills', 'jobs']
#    edit_exclude_columns =[hide_list] # ['skills', 'jobs']
#
#    list_columns = ['skills', 'jobs']
#    list_exclude_columns = [] # ['skills', 'jobs']
#
#    search_columns = ['skills', 'jobs']
#    search_exclude_columns= [] # ['skills', 'jobs']
#
#    default_sort = [('id', True)]
#    base_permissions = ['can_list', 'can_show', 'can_edit', 'can_delete', 'can_add']
#    label_columns=   [{column.name: column.name for column in table.columns} ]
#    show_template =  'appbuilder/general/model/show_cascade.html'
#    list_template = 'appbuilder/general/model/list.html'
#    add_template = 'appbuilder/general/model/add.html'
#    edit_template = 'appbuilder/general/model/edit.html'
#    add_widget = (FormVerticalWidget|FormInlineWidget)
#    show_widget = ShowBlockWidget
#    list_widget = (ListThumbnail|ListWidget)
#    base_order = ('name', 'asc')
#    list_widget= 'list_widget'


class JobSkillMultiView(MultipleView):
    datamodel=SQLAInterface(JobSkill, db.session)
    views = [SkillDetailView]
    show_title='JobSkill Detail'
    add_title ='Add JobSkill'
    list_title= 'JobSkill List'
    edit_title = 'Edit JobSkill'
    show_columns = ['skills', 'jobs']
#    show_exclude_columns = [] #= ['skills', 'jobs']
#
#    add_columns = ['skills', 'jobs']
#    add_exclude_columns = [hide_list] #['skills', 'jobs']
#
#    edit_columns = ['skills', 'jobs']
#    edit_exclude_columns =[hide_list] # ['skills', 'jobs']
#
#    list_columns = ['skills', 'jobs']
#    list_exclude_columns = [] # ['skills', 'jobs']
#
#    search_columns = ['skills', 'jobs']
#    search_exclude_columns= [] # ['skills', 'jobs']
#
#    default_sort = [('id', True)]
#    base_permissions = ['can_list', 'can_show', 'can_edit', 'can_delete', 'can_add']
#    label_columns=   [{column.name: column.name for column in table.columns} ]
#    show_template =  'appbuilder/general/model/show_cascade.html'
#    list_template = 'appbuilder/general/model/list.html'
#    add_template = 'appbuilder/general/model/add.html'
#    edit_template = 'appbuilder/general/model/edit.html'
#    add_widget = (FormVerticalWidget|FormInlineWidget)
#    show_widget = ShowBlockWidget
#    list_widget = (ListThumbnail|ListWidget)
#    base_order = ('name', 'asc')
#    list_widget= 'list_widget'


class EducationMasterView(MasterDetailView):
    datamodel=SQLAInterface(Education, db.session)
    related_views = [IndividualDetailView]
    show_title='Education Detail'
    add_title ='Add Education'
    list_title= 'Education List'
    edit_title = 'Edit Education'
    show_columns = ['id', 'individual', 'qualification', 'qual_class', 'verified', 'verification_code', 'verified_by', 'verification_date', 'verification_doc']
#    show_exclude_columns = [] #= ['id', 'individual', 'qualification', 'qual_class', 'verified', 'verification_code', 'verified_by', 'verification_date', 'verification_doc']
#
#    add_columns = ['id', 'individual', 'qualification', 'qual_class', 'verified', 'verification_code', 'verified_by', 'verification_date', 'verification_doc']
#    add_exclude_columns = [hide_list] #['id', 'individual', 'qualification', 'qual_class', 'verified', 'verification_code', 'verified_by', 'verification_date', 'verification_doc']
#
#    edit_columns = ['id', 'individual', 'qualification', 'qual_class', 'verified', 'verification_code', 'verified_by', 'verification_date', 'verification_doc']
#    edit_exclude_columns =[hide_list] # ['id', 'individual', 'qualification', 'qual_class', 'verified', 'verification_code', 'verified_by', 'verification_date', 'verification_doc']
#
#    list_columns = ['id', 'individual', 'qualification', 'qual_class', 'verified', 'verification_code', 'verified_by', 'verification_date', 'verification_doc']
#    list_exclude_columns = [] # ['id', 'individual', 'qualification', 'qual_class', 'verified', 'verification_code', 'verified_by', 'verification_date', 'verification_doc']
#
#    search_columns = ['id', 'individual', 'qualification', 'qual_class', 'verified', 'verification_code', 'verified_by', 'verification_date', 'verification_doc']
#    search_exclude_columns= [] # ['id', 'individual', 'qualification', 'qual_class', 'verified', 'verification_code', 'verified_by', 'verification_date', 'verification_doc']
#
#    default_sort = [('id', True)]
#    base_permissions = ['can_list', 'can_show', 'can_edit', 'can_delete', 'can_add']
#    label_columns=   [{column.name: column.name for column in table.columns} ]
#    show_template =  'appbuilder/general/model/show_cascade.html'
#    list_template = 'appbuilder/general/model/list.html'
#    add_template = 'appbuilder/general/model/add.html'
#    edit_template = 'appbuilder/general/model/edit.html'
#    add_widget = (FormVerticalWidget|FormInlineWidget)
#    show_widget = ShowBlockWidget
#    list_widget = (ListThumbnail|ListWidget)
#    base_order = ('name', 'asc')
#    list_widget= 'list_widget'


class IndividualJobMasterView(MasterDetailView):
    datamodel=SQLAInterface(IndividualJob, db.session)
    related_views = [IndividualDetailView]
    show_title='IndividualJob Detail'
    add_title ='Add IndividualJob'
    list_title= 'IndividualJob List'
    edit_title = 'Edit IndividualJob'
    show_columns = ['individual', 'job']
#    show_exclude_columns = [] #= ['individual', 'job']
#
#    add_columns = ['individual', 'job']
#    add_exclude_columns = [hide_list] #['individual', 'job']
#
#    edit_columns = ['individual', 'job']
#    edit_exclude_columns =[hide_list] # ['individual', 'job']
#
#    list_columns = ['individual', 'job']
#    list_exclude_columns = [] # ['individual', 'job']
#
#    search_columns = ['individual', 'job']
#    search_exclude_columns= [] # ['individual', 'job']
#
#    default_sort = [('id', True)]
#    base_permissions = ['can_list', 'can_show', 'can_edit', 'can_delete', 'can_add']
#    label_columns=   [{column.name: column.name for column in table.columns} ]
#    show_template =  'appbuilder/general/model/show_cascade.html'
#    list_template = 'appbuilder/general/model/list.html'
#    add_template = 'appbuilder/general/model/add.html'
#    edit_template = 'appbuilder/general/model/edit.html'
#    add_widget = (FormVerticalWidget|FormInlineWidget)
#    show_widget = ShowBlockWidget
#    list_widget = (ListThumbnail|ListWidget)
#    base_order = ('name', 'asc')
#    list_widget= 'list_widget'


class IndividualJobMultiView(MultipleView):
    datamodel=SQLAInterface(IndividualJob, db.session)
    views = []
    show_title='IndividualJob Detail'
    add_title ='Add IndividualJob'
    list_title= 'IndividualJob List'
    edit_title = 'Edit IndividualJob'
    show_columns = ['individual', 'job']
#    show_exclude_columns = [] #= ['individual', 'job']
#
#    add_columns = ['individual', 'job']
#    add_exclude_columns = [hide_list] #['individual', 'job']
#
#    edit_columns = ['individual', 'job']
#    edit_exclude_columns =[hide_list] # ['individual', 'job']
#
#    list_columns = ['individual', 'job']
#    list_exclude_columns = [] # ['individual', 'job']
#
#    search_columns = ['individual', 'job']
#    search_exclude_columns= [] # ['individual', 'job']
#
#    default_sort = [('id', True)]
#    base_permissions = ['can_list', 'can_show', 'can_edit', 'can_delete', 'can_add']
#    label_columns=   [{column.name: column.name for column in table.columns} ]
#    show_template =  'appbuilder/general/model/show_cascade.html'
#    list_template = 'appbuilder/general/model/list.html'
#    add_template = 'appbuilder/general/model/add.html'
#    edit_template = 'appbuilder/general/model/edit.html'
#    add_widget = (FormVerticalWidget|FormInlineWidget)
#    show_widget = ShowBlockWidget
#    list_widget = (ListThumbnail|ListWidget)
#    base_order = ('name', 'asc')
#    list_widget= 'list_widget'


class LocationMasterView(MasterDetailView):
    datamodel=SQLAInterface(Location, db.session)
    related_views = [IndividualDetailView]
    show_title='Location Detail'
    add_title ='Add Location'
    list_title= 'Location List'
    edit_title = 'Edit Location'
    show_columns = ['id', 'individual']
#    show_exclude_columns = [] #= ['id', 'individual']
#
#    add_columns = ['id', 'individual']
#    add_exclude_columns = [hide_list] #['id', 'individual']
#
#    edit_columns = ['id', 'individual']
#    edit_exclude_columns =[hide_list] # ['id', 'individual']
#
#    list_columns = ['id', 'individual']
#    list_exclude_columns = [] # ['id', 'individual']
#
#    search_columns = ['id', 'individual']
#    search_exclude_columns= [] # ['id', 'individual']
#
#    default_sort = [('id', True)]
#    base_permissions = ['can_list', 'can_show', 'can_edit', 'can_delete', 'can_add']
#    label_columns=   [{column.name: column.name for column in table.columns} ]
#    show_template =  'appbuilder/general/model/show_cascade.html'
#    list_template = 'appbuilder/general/model/list.html'
#    add_template = 'appbuilder/general/model/add.html'
#    edit_template = 'appbuilder/general/model/edit.html'
#    add_widget = (FormVerticalWidget|FormInlineWidget)
#    show_widget = ShowBlockWidget
#    list_widget = (ListThumbnail|ListWidget)
#    base_order = ('name', 'asc')
#    list_widget= 'list_widget'


class PortalView(ModelView):
    datamodel=SQLAInterface(Portal, db.session)
    related_views = []
    show_title='Portal Detail'
    add_title ='Add Portal'
    list_title= 'Portal List'
    edit_title = 'Edit Portal'
    show_columns = ['id', 'portal_url', 'is_primary', 'portal_state', 'individual', 'has_custom_domain', 'domain', 'header_text', 'slug', 'automatic_fulfillment_digital_products', 'default_digital_max_downloads', 'default_digital_url_valid_days', 'default_mail_sender_name', 'default_mail_sender_address', 'fulfillment_auto_approve', 'fulfillment_allow_unpaid', 'reserve_stock_duration_anonymous_user', 'reserve_stock_duration_authenticated_user', 'limit_quantity_per_checkout', 'gift_card_expiry_type', 'gift_card_expiry_period_type', 'gift_card_expiry_period', 'charge_taxes_on_shipping', 'include_taxes_in_prices', 'display_gross_prices', 'language']
#    show_exclude_columns = [] #= ['id', 'portal_url', 'is_primary', 'portal_state', 'individual', 'has_custom_domain', 'domain', 'header_text', 'slug', 'automatic_fulfillment_digital_products', 'default_digital_max_downloads', 'default_digital_url_valid_days', 'default_mail_sender_name', 'default_mail_sender_address', 'fulfillment_auto_approve', 'fulfillment_allow_unpaid', 'reserve_stock_duration_anonymous_user', 'reserve_stock_duration_authenticated_user', 'limit_quantity_per_checkout', 'gift_card_expiry_type', 'gift_card_expiry_period_type', 'gift_card_expiry_period', 'charge_taxes_on_shipping', 'include_taxes_in_prices', 'display_gross_prices', 'language']
#
#    add_columns = ['id', 'portal_url', 'is_primary', 'portal_state', 'individual', 'has_custom_domain', 'domain', 'header_text', 'slug', 'automatic_fulfillment_digital_products', 'default_digital_max_downloads', 'default_digital_url_valid_days', 'default_mail_sender_name', 'default_mail_sender_address', 'fulfillment_auto_approve', 'fulfillment_allow_unpaid', 'reserve_stock_duration_anonymous_user', 'reserve_stock_duration_authenticated_user', 'limit_quantity_per_checkout', 'gift_card_expiry_type', 'gift_card_expiry_period_type', 'gift_card_expiry_period', 'charge_taxes_on_shipping', 'include_taxes_in_prices', 'display_gross_prices', 'language']
#    add_exclude_columns = [hide_list] #['id', 'portal_url', 'is_primary', 'portal_state', 'individual', 'has_custom_domain', 'domain', 'header_text', 'slug', 'automatic_fulfillment_digital_products', 'default_digital_max_downloads', 'default_digital_url_valid_days', 'default_mail_sender_name', 'default_mail_sender_address', 'fulfillment_auto_approve', 'fulfillment_allow_unpaid', 'reserve_stock_duration_anonymous_user', 'reserve_stock_duration_authenticated_user', 'limit_quantity_per_checkout', 'gift_card_expiry_type', 'gift_card_expiry_period_type', 'gift_card_expiry_period', 'charge_taxes_on_shipping', 'include_taxes_in_prices', 'display_gross_prices', 'language']
#
#    edit_columns = ['id', 'portal_url', 'is_primary', 'portal_state', 'individual', 'has_custom_domain', 'domain', 'header_text', 'slug', 'automatic_fulfillment_digital_products', 'default_digital_max_downloads', 'default_digital_url_valid_days', 'default_mail_sender_name', 'default_mail_sender_address', 'fulfillment_auto_approve', 'fulfillment_allow_unpaid', 'reserve_stock_duration_anonymous_user', 'reserve_stock_duration_authenticated_user', 'limit_quantity_per_checkout', 'gift_card_expiry_type', 'gift_card_expiry_period_type', 'gift_card_expiry_period', 'charge_taxes_on_shipping', 'include_taxes_in_prices', 'display_gross_prices', 'language']
#    edit_exclude_columns =[hide_list] # ['id', 'portal_url', 'is_primary', 'portal_state', 'individual', 'has_custom_domain', 'domain', 'header_text', 'slug', 'automatic_fulfillment_digital_products', 'default_digital_max_downloads', 'default_digital_url_valid_days', 'default_mail_sender_name', 'default_mail_sender_address', 'fulfillment_auto_approve', 'fulfillment_allow_unpaid', 'reserve_stock_duration_anonymous_user', 'reserve_stock_duration_authenticated_user', 'limit_quantity_per_checkout', 'gift_card_expiry_type', 'gift_card_expiry_period_type', 'gift_card_expiry_period', 'charge_taxes_on_shipping', 'include_taxes_in_prices', 'display_gross_prices', 'language']
#
#    list_columns = ['id', 'portal_url', 'is_primary', 'portal_state', 'individual', 'has_custom_domain', 'domain', 'header_text', 'slug', 'automatic_fulfillment_digital_products', 'default_digital_max_downloads', 'default_digital_url_valid_days', 'default_mail_sender_name', 'default_mail_sender_address', 'fulfillment_auto_approve', 'fulfillment_allow_unpaid', 'reserve_stock_duration_anonymous_user', 'reserve_stock_duration_authenticated_user', 'limit_quantity_per_checkout', 'gift_card_expiry_type', 'gift_card_expiry_period_type', 'gift_card_expiry_period', 'charge_taxes_on_shipping', 'include_taxes_in_prices', 'display_gross_prices', 'language']
#    list_exclude_columns = [] # ['id', 'portal_url', 'is_primary', 'portal_state', 'individual', 'has_custom_domain', 'domain', 'header_text', 'slug', 'automatic_fulfillment_digital_products', 'default_digital_max_downloads', 'default_digital_url_valid_days', 'default_mail_sender_name', 'default_mail_sender_address', 'fulfillment_auto_approve', 'fulfillment_allow_unpaid', 'reserve_stock_duration_anonymous_user', 'reserve_stock_duration_authenticated_user', 'limit_quantity_per_checkout', 'gift_card_expiry_type', 'gift_card_expiry_period_type', 'gift_card_expiry_period', 'charge_taxes_on_shipping', 'include_taxes_in_prices', 'display_gross_prices', 'language']
#
#    search_columns = ['id', 'portal_url', 'is_primary', 'portal_state', 'individual', 'has_custom_domain', 'domain', 'header_text', 'slug', 'automatic_fulfillment_digital_products', 'default_digital_max_downloads', 'default_digital_url_valid_days', 'default_mail_sender_name', 'default_mail_sender_address', 'fulfillment_auto_approve', 'fulfillment_allow_unpaid', 'reserve_stock_duration_anonymous_user', 'reserve_stock_duration_authenticated_user', 'limit_quantity_per_checkout', 'gift_card_expiry_type', 'gift_card_expiry_period_type', 'gift_card_expiry_period', 'charge_taxes_on_shipping', 'include_taxes_in_prices', 'display_gross_prices', 'language']
#    search_exclude_columns= [] # ['id', 'portal_url', 'is_primary', 'portal_state', 'individual', 'has_custom_domain', 'domain', 'header_text', 'slug', 'automatic_fulfillment_digital_products', 'default_digital_max_downloads', 'default_digital_url_valid_days', 'default_mail_sender_name', 'default_mail_sender_address', 'fulfillment_auto_approve', 'fulfillment_allow_unpaid', 'reserve_stock_duration_anonymous_user', 'reserve_stock_duration_authenticated_user', 'limit_quantity_per_checkout', 'gift_card_expiry_type', 'gift_card_expiry_period_type', 'gift_card_expiry_period', 'charge_taxes_on_shipping', 'include_taxes_in_prices', 'display_gross_prices', 'language']
#
#    default_sort = [('id', True)]
#    base_permissions = ['can_list', 'can_show', 'can_edit', 'can_delete', 'can_add']
#    label_columns=   [{column.name: column.name for column in table.columns} ]
#    show_template =  'appbuilder/general/model/show_cascade.html'
#    list_template = 'appbuilder/general/model/list.html'
#    add_template = 'appbuilder/general/model/add.html'
#    edit_template = 'appbuilder/general/model/edit.html'
#    add_widget = (FormVerticalWidget|FormInlineWidget)
#    show_widget = ShowBlockWidget
#    list_widget = (ListThumbnail|ListWidget)
#    base_order = ('name', 'asc')
#    list_widget= 'list_widget'


class UserxDetailView(ModelView):
    datamodel=SQLAInterface(Userx, db.session)
    related_views = []
    show_title='Userx Detail'
    add_title ='Add Userx'
    list_title= 'Userx List'
    edit_title = 'Edit Userx'
    show_columns = ['id', 'userx', 'is_individual', 'is_institution', 'is_company', 'is_government', 'is_online']
#    show_exclude_columns = [] #= ['id', 'userx', 'is_individual', 'is_institution', 'is_company', 'is_government', 'is_online']
#
#    add_columns = ['id', 'userx', 'is_individual', 'is_institution', 'is_company', 'is_government', 'is_online']
#    add_exclude_columns = [hide_list] #['id', 'userx', 'is_individual', 'is_institution', 'is_company', 'is_government', 'is_online']
#
#    edit_columns = ['id', 'userx', 'is_individual', 'is_institution', 'is_company', 'is_government', 'is_online']
#    edit_exclude_columns =[hide_list] # ['id', 'userx', 'is_individual', 'is_institution', 'is_company', 'is_government', 'is_online']
#
#    list_columns = ['id', 'userx', 'is_individual', 'is_institution', 'is_company', 'is_government', 'is_online']
#    list_exclude_columns = [] # ['id', 'userx', 'is_individual', 'is_institution', 'is_company', 'is_government', 'is_online']
#
#    search_columns = ['id', 'userx', 'is_individual', 'is_institution', 'is_company', 'is_government', 'is_online']
#    search_exclude_columns= [] # ['id', 'userx', 'is_individual', 'is_institution', 'is_company', 'is_government', 'is_online']
#
#    default_sort = [('id', True)]
#    base_permissions = ['can_list', 'can_show', 'can_edit', 'can_delete', 'can_add']
#    label_columns=   [{column.name: column.name for column in table.columns} ]
#    show_template =  'appbuilder/general/model/show_cascade.html'
#    list_template = 'appbuilder/general/model/list.html'
#    add_template = 'appbuilder/general/model/add.html'
#    edit_template = 'appbuilder/general/model/edit.html'
#    add_widget = (FormVerticalWidget|FormInlineWidget)
#    show_widget = ShowBlockWidget
#    list_widget = (ListThumbnail|ListWidget)
#    base_order = ('name', 'asc')
#    list_widget= 'list_widget'


class IndividualDetailView(ModelView):
    datamodel=SQLAInterface(Individual, db.session)
    related_views = []
    show_title='Individual Detail'
    add_title ='Add Individual'
    list_title= 'Individual List'
    edit_title = 'Edit Individual'
    show_columns = ['id', 'userx', 'is_individual', 'is_institution', 'is_company', 'is_government', 'is_online']
#    show_exclude_columns = [] #= ['id', 'userx', 'is_individual', 'is_institution', 'is_company', 'is_government', 'is_online']
#
#    add_columns = ['id', 'userx', 'is_individual', 'is_institution', 'is_company', 'is_government', 'is_online']
#    add_exclude_columns = [hide_list] #['id', 'userx', 'is_individual', 'is_institution', 'is_company', 'is_government', 'is_online']
#
#    edit_columns = ['id', 'userx', 'is_individual', 'is_institution', 'is_company', 'is_government', 'is_online']
#    edit_exclude_columns =[hide_list] # ['id', 'userx', 'is_individual', 'is_institution', 'is_company', 'is_government', 'is_online']
#
#    list_columns = ['id', 'userx', 'is_individual', 'is_institution', 'is_company', 'is_government', 'is_online']
#    list_exclude_columns = [] # ['id', 'userx', 'is_individual', 'is_institution', 'is_company', 'is_government', 'is_online']
#
#    search_columns = ['id', 'userx', 'is_individual', 'is_institution', 'is_company', 'is_government', 'is_online']
#    search_exclude_columns= [] # ['id', 'userx', 'is_individual', 'is_institution', 'is_company', 'is_government', 'is_online']
#
#    default_sort = [('id', True)]
#    base_permissions = ['can_list', 'can_show', 'can_edit', 'can_delete', 'can_add']
#    label_columns=   [{column.name: column.name for column in table.columns} ]
#    show_template =  'appbuilder/general/model/show_cascade.html'
#    list_template = 'appbuilder/general/model/list.html'
#    add_template = 'appbuilder/general/model/add.html'
#    edit_template = 'appbuilder/general/model/edit.html'
#    add_widget = (FormVerticalWidget|FormInlineWidget)
#    show_widget = ShowBlockWidget
#    list_widget = (ListThumbnail|ListWidget)
#    base_order = ('name', 'asc')
#    list_widget= 'list_widget'


class IndustryDetailView(ModelView):
    datamodel=SQLAInterface(Industry, db.session)
    related_views = []
    show_title='Industry Detail'
    add_title ='Add Industry'
    list_title= 'Industry List'
    edit_title = 'Edit Industry'
    show_columns = ['industry', 'job']
#    show_exclude_columns = [] #= ['industry', 'job']
#
#    add_columns = ['industry', 'job']
#    add_exclude_columns = [hide_list] #['industry', 'job']
#
#    edit_columns = ['industry', 'job']
#    edit_exclude_columns =[hide_list] # ['industry', 'job']
#
#    list_columns = ['industry', 'job']
#    list_exclude_columns = [] # ['industry', 'job']
#
#    search_columns = ['industry', 'job']
#    search_exclude_columns= [] # ['industry', 'job']
#
#    default_sort = [('id', True)]
#    base_permissions = ['can_list', 'can_show', 'can_edit', 'can_delete', 'can_add']
#    label_columns=   [{column.name: column.name for column in table.columns} ]
#    show_template =  'appbuilder/general/model/show_cascade.html'
#    list_template = 'appbuilder/general/model/list.html'
#    add_template = 'appbuilder/general/model/add.html'
#    edit_template = 'appbuilder/general/model/edit.html'
#    add_widget = (FormVerticalWidget|FormInlineWidget)
#    show_widget = ShowBlockWidget
#    list_widget = (ListThumbnail|ListWidget)
#    base_order = ('name', 'asc')
#    list_widget= 'list_widget'


class IndustryJobDetailView(ModelView):
    datamodel=SQLAInterface(IndustryJob, db.session)
    related_views = []
    show_title='IndustryJob Detail'
    add_title ='Add IndustryJob'
    list_title= 'IndustryJob List'
    edit_title = 'Edit IndustryJob'
    show_columns = ['industry', 'job']
#    show_exclude_columns = [] #= ['industry', 'job']
#
#    add_columns = ['industry', 'job']
#    add_exclude_columns = [hide_list] #['industry', 'job']
#
#    edit_columns = ['industry', 'job']
#    edit_exclude_columns =[hide_list] # ['industry', 'job']
#
#    list_columns = ['industry', 'job']
#    list_exclude_columns = [] # ['industry', 'job']
#
#    search_columns = ['industry', 'job']
#    search_exclude_columns= [] # ['industry', 'job']
#
#    default_sort = [('id', True)]
#    base_permissions = ['can_list', 'can_show', 'can_edit', 'can_delete', 'can_add']
#    label_columns=   [{column.name: column.name for column in table.columns} ]
#    show_template =  'appbuilder/general/model/show_cascade.html'
#    list_template = 'appbuilder/general/model/list.html'
#    add_template = 'appbuilder/general/model/add.html'
#    edit_template = 'appbuilder/general/model/edit.html'
#    add_widget = (FormVerticalWidget|FormInlineWidget)
#    show_widget = ShowBlockWidget
#    list_widget = (ListThumbnail|ListWidget)
#    base_order = ('name', 'asc')
#    list_widget= 'list_widget'


class JobDetailView(ModelView):
    datamodel=SQLAInterface(Job, db.session)
    related_views = []
    show_title='Job Detail'
    add_title ='Add Job'
    list_title= 'Job List'
    edit_title = 'Edit Job'
    show_columns = ['industry', 'job']
#    show_exclude_columns = [] #= ['industry', 'job']
#
#    add_columns = ['industry', 'job']
#    add_exclude_columns = [hide_list] #['industry', 'job']
#
#    edit_columns = ['industry', 'job']
#    edit_exclude_columns =[hide_list] # ['industry', 'job']
#
#    list_columns = ['industry', 'job']
#    list_exclude_columns = [] # ['industry', 'job']
#
#    search_columns = ['industry', 'job']
#    search_exclude_columns= [] # ['industry', 'job']
#
#    default_sort = [('id', True)]
#    base_permissions = ['can_list', 'can_show', 'can_edit', 'can_delete', 'can_add']
#    label_columns=   [{column.name: column.name for column in table.columns} ]
#    show_template =  'appbuilder/general/model/show_cascade.html'
#    list_template = 'appbuilder/general/model/list.html'
#    add_template = 'appbuilder/general/model/add.html'
#    edit_template = 'appbuilder/general/model/edit.html'
#    add_widget = (FormVerticalWidget|FormInlineWidget)
#    show_widget = ShowBlockWidget
#    list_widget = (ListThumbnail|ListWidget)
#    base_order = ('name', 'asc')
#    list_widget= 'list_widget'




class SkillDetailView(ModelView):
    datamodel=SQLAInterface(Skill, db.session)
    related_views = []
    show_title='Skill Detail'
    add_title ='Add Skill'
    list_title= 'Skill List'
    edit_title = 'Edit Skill'
    show_columns = ['skills', 'jobs']
#    show_exclude_columns = [] #= ['skills', 'jobs']
#
#    add_columns = ['skills', 'jobs']
#    add_exclude_columns = [hide_list] #['skills', 'jobs']
#
#    edit_columns = ['skills', 'jobs']
#    edit_exclude_columns =[hide_list] # ['skills', 'jobs']
#
#    list_columns = ['skills', 'jobs']
#    list_exclude_columns = [] # ['skills', 'jobs']
#
#    search_columns = ['skills', 'jobs']
#    search_exclude_columns= [] # ['skills', 'jobs']
#
#    default_sort = [('id', True)]
#    base_permissions = ['can_list', 'can_show', 'can_edit', 'can_delete', 'can_add']
#    label_columns=   [{column.name: column.name for column in table.columns} ]
#    show_template =  'appbuilder/general/model/show_cascade.html'
#    list_template = 'appbuilder/general/model/list.html'
#    add_template = 'appbuilder/general/model/add.html'
#    edit_template = 'appbuilder/general/model/edit.html'
#    add_widget = (FormVerticalWidget|FormInlineWidget)
#    show_widget = ShowBlockWidget
#    list_widget = (ListThumbnail|ListWidget)
#    base_order = ('name', 'asc')
#    list_widget= 'list_widget'


class JobSkillDetailView(ModelView):
    datamodel=SQLAInterface(JobSkill, db.session)
    related_views = []
    show_title='JobSkill Detail'
    add_title ='Add JobSkill'
    list_title= 'JobSkill List'
    edit_title = 'Edit JobSkill'
    show_columns = ['skills', 'jobs']
#    show_exclude_columns = [] #= ['skills', 'jobs']
#
#    add_columns = ['skills', 'jobs']
#    add_exclude_columns = [hide_list] #['skills', 'jobs']
#
#    edit_columns = ['skills', 'jobs']
#    edit_exclude_columns =[hide_list] # ['skills', 'jobs']
#
#    list_columns = ['skills', 'jobs']
#    list_exclude_columns = [] # ['skills', 'jobs']
#
#    search_columns = ['skills', 'jobs']
#    search_exclude_columns= [] # ['skills', 'jobs']
#
#    default_sort = [('id', True)]
#    base_permissions = ['can_list', 'can_show', 'can_edit', 'can_delete', 'can_add']
#    label_columns=   [{column.name: column.name for column in table.columns} ]
#    show_template =  'appbuilder/general/model/show_cascade.html'
#    list_template = 'appbuilder/general/model/list.html'
#    add_template = 'appbuilder/general/model/add.html'
#    edit_template = 'appbuilder/general/model/edit.html'
#    add_widget = (FormVerticalWidget|FormInlineWidget)
#    show_widget = ShowBlockWidget
#    list_widget = (ListThumbnail|ListWidget)
#    base_order = ('name', 'asc')
#    list_widget= 'list_widget'


class IndividualMasterView(MasterDetailView):
    datamodel=SQLAInterface(Individual, db.session)
    related_views = [UserxDetailView]
    show_title='Individual Detail'
    add_title ='Add Individual'
    list_title= 'Individual List'
    edit_title = 'Edit Individual'
    show_columns = ['id', 'userx', 'is_individual', 'is_institution', 'is_company', 'is_government', 'is_online']
#    show_exclude_columns = [] #= ['id', 'userx', 'is_individual', 'is_institution', 'is_company', 'is_government', 'is_online']
#
#    add_columns = ['id', 'userx', 'is_individual', 'is_institution', 'is_company', 'is_government', 'is_online']
#    add_exclude_columns = [hide_list] #['id', 'userx', 'is_individual', 'is_institution', 'is_company', 'is_government', 'is_online']
#
#    edit_columns = ['id', 'userx', 'is_individual', 'is_institution', 'is_company', 'is_government', 'is_online']
#    edit_exclude_columns =[hide_list] # ['id', 'userx', 'is_individual', 'is_institution', 'is_company', 'is_government', 'is_online']
#
#    list_columns = ['id', 'userx', 'is_individual', 'is_institution', 'is_company', 'is_government', 'is_online']
#    list_exclude_columns = [] # ['id', 'userx', 'is_individual', 'is_institution', 'is_company', 'is_government', 'is_online']
#
#    search_columns = ['id', 'userx', 'is_individual', 'is_institution', 'is_company', 'is_government', 'is_online']
#    search_exclude_columns= [] # ['id', 'userx', 'is_individual', 'is_institution', 'is_company', 'is_government', 'is_online']
#
#    default_sort = [('id', True)]
#    base_permissions = ['can_list', 'can_show', 'can_edit', 'can_delete', 'can_add']
#    label_columns=   [{column.name: column.name for column in table.columns} ]
#    show_template =  'appbuilder/general/model/show_cascade.html'
#    list_template = 'appbuilder/general/model/list.html'
#    add_template = 'appbuilder/general/model/add.html'
#    edit_template = 'appbuilder/general/model/edit.html'
#    add_widget = (FormVerticalWidget|FormInlineWidget)
#    show_widget = ShowBlockWidget
#    list_widget = (ListThumbnail|ListWidget)
#    base_order = ('name', 'asc')
#    list_widget= 'list_widget'


class IndustryJobMasterView(MasterDetailView):
    datamodel=SQLAInterface(IndustryJob, db.session)
    related_views = [IndustryDetailView]
    show_title='IndustryJob Detail'
    add_title ='Add IndustryJob'
    list_title= 'IndustryJob List'
    edit_title = 'Edit IndustryJob'
    show_columns = ['industry', 'job']
#    show_exclude_columns = [] #= ['industry', 'job']
#
#    add_columns = ['industry', 'job']
#    add_exclude_columns = [hide_list] #['industry', 'job']
#
#    edit_columns = ['industry', 'job']
#    edit_exclude_columns =[hide_list] # ['industry', 'job']
#
#    list_columns = ['industry', 'job']
#    list_exclude_columns = [] # ['industry', 'job']
#
#    search_columns = ['industry', 'job']
#    search_exclude_columns= [] # ['industry', 'job']
#
#    default_sort = [('id', True)]
#    base_permissions = ['can_list', 'can_show', 'can_edit', 'can_delete', 'can_add']
#    label_columns=   [{column.name: column.name for column in table.columns} ]
#    show_template =  'appbuilder/general/model/show_cascade.html'
#    list_template = 'appbuilder/general/model/list.html'
#    add_template = 'appbuilder/general/model/add.html'
#    edit_template = 'appbuilder/general/model/edit.html'
#    add_widget = (FormVerticalWidget|FormInlineWidget)
#    show_widget = ShowBlockWidget
#    list_widget = (ListThumbnail|ListWidget)
#    base_order = ('name', 'asc')
#    list_widget= 'list_widget'


class IndustryJobMultiView(MultipleView):
    datamodel=SQLAInterface(IndustryJob, db.session)
    views = [IndustryDetailView, JobDetailView]
    show_title='IndustryJob Detail'
    add_title ='Add IndustryJob'
    list_title= 'IndustryJob List'
    edit_title = 'Edit IndustryJob'
    show_columns = ['industry', 'job']
#    show_exclude_columns = [] #= ['industry', 'job']
#
#    add_columns = ['industry', 'job']
#    add_exclude_columns = [hide_list] #['industry', 'job']
#
#    edit_columns = ['industry', 'job']
#    edit_exclude_columns =[hide_list] # ['industry', 'job']
#
#    list_columns = ['industry', 'job']
#    list_exclude_columns = [] # ['industry', 'job']
#
#    search_columns = ['industry', 'job']
#    search_exclude_columns= [] # ['industry', 'job']
#
#    default_sort = [('id', True)]
#    base_permissions = ['can_list', 'can_show', 'can_edit', 'can_delete', 'can_add']
#    label_columns=   [{column.name: column.name for column in table.columns} ]
#    show_template =  'appbuilder/general/model/show_cascade.html'
#    list_template = 'appbuilder/general/model/list.html'
#    add_template = 'appbuilder/general/model/add.html'
#    edit_template = 'appbuilder/general/model/edit.html'
#    add_widget = (FormVerticalWidget|FormInlineWidget)
#    show_widget = ShowBlockWidget
#    list_widget = (ListThumbnail|ListWidget)
#    base_order = ('name', 'asc')
#    list_widget= 'list_widget'


class JobSkillMasterView(MasterDetailView):
    datamodel=SQLAInterface(JobSkill, db.session)
    related_views = [JobDetailView]
    show_title='JobSkill Detail'
    add_title ='Add JobSkill'
    list_title= 'JobSkill List'
    edit_title = 'Edit JobSkill'
    show_columns = ['skills', 'jobs']
#    show_exclude_columns = [] #= ['skills', 'jobs']
#
#    add_columns = ['skills', 'jobs']
#    add_exclude_columns = [hide_list] #['skills', 'jobs']
#
#    edit_columns = ['skills', 'jobs']
#    edit_exclude_columns =[hide_list] # ['skills', 'jobs']
#
#    list_columns = ['skills', 'jobs']
#    list_exclude_columns = [] # ['skills', 'jobs']
#
#    search_columns = ['skills', 'jobs']
#    search_exclude_columns= [] # ['skills', 'jobs']
#
#    default_sort = [('id', True)]
#    base_permissions = ['can_list', 'can_show', 'can_edit', 'can_delete', 'can_add']
#    label_columns=   [{column.name: column.name for column in table.columns} ]
#    show_template =  'appbuilder/general/model/show_cascade.html'
#    list_template = 'appbuilder/general/model/list.html'
#    add_template = 'appbuilder/general/model/add.html'
#    edit_template = 'appbuilder/general/model/edit.html'
#    add_widget = (FormVerticalWidget|FormInlineWidget)
#    show_widget = ShowBlockWidget
#    list_widget = (ListThumbnail|ListWidget)
#    base_order = ('name', 'asc')
#    list_widget= 'list_widget'


class JobSkillMultiView(MultipleView):
    datamodel=SQLAInterface(JobSkill, db.session)
    views = [SkillDetailView]
    show_title='JobSkill Detail'
    add_title ='Add JobSkill'
    list_title= 'JobSkill List'
    edit_title = 'Edit JobSkill'
    show_columns = ['skills', 'jobs']
#    show_exclude_columns = [] #= ['skills', 'jobs']
#
#    add_columns = ['skills', 'jobs']
#    add_exclude_columns = [hide_list] #['skills', 'jobs']
#
#    edit_columns = ['skills', 'jobs']
#    edit_exclude_columns =[hide_list] # ['skills', 'jobs']
#
#    list_columns = ['skills', 'jobs']
#    list_exclude_columns = [] # ['skills', 'jobs']
#
#    search_columns = ['skills', 'jobs']
#    search_exclude_columns= [] # ['skills', 'jobs']
#
#    default_sort = [('id', True)]
#    base_permissions = ['can_list', 'can_show', 'can_edit', 'can_delete', 'can_add']
#    label_columns=   [{column.name: column.name for column in table.columns} ]
#    show_template =  'appbuilder/general/model/show_cascade.html'
#    list_template = 'appbuilder/general/model/list.html'
#    add_template = 'appbuilder/general/model/add.html'
#    edit_template = 'appbuilder/general/model/edit.html'
#    add_widget = (FormVerticalWidget|FormInlineWidget)
#    show_widget = ShowBlockWidget
#    list_widget = (ListThumbnail|ListWidget)
#    base_order = ('name', 'asc')
#    list_widget= 'list_widget'


class EducationMasterView(MasterDetailView):
    datamodel=SQLAInterface(Education, db.session)
    related_views = [IndividualDetailView]
    show_title='Education Detail'
    add_title ='Add Education'
    list_title= 'Education List'
    edit_title = 'Edit Education'
    show_columns = ['id', 'individual', 'qualification', 'qual_class', 'verified', 'verification_code', 'verified_by', 'verification_date', 'verification_doc']
#    show_exclude_columns = [] #= ['id', 'individual', 'qualification', 'qual_class', 'verified', 'verification_code', 'verified_by', 'verification_date', 'verification_doc']
#
#    add_columns = ['id', 'individual', 'qualification', 'qual_class', 'verified', 'verification_code', 'verified_by', 'verification_date', 'verification_doc']
#    add_exclude_columns = [hide_list] #['id', 'individual', 'qualification', 'qual_class', 'verified', 'verification_code', 'verified_by', 'verification_date', 'verification_doc']
#
#    edit_columns = ['id', 'individual', 'qualification', 'qual_class', 'verified', 'verification_code', 'verified_by', 'verification_date', 'verification_doc']
#    edit_exclude_columns =[hide_list] # ['id', 'individual', 'qualification', 'qual_class', 'verified', 'verification_code', 'verified_by', 'verification_date', 'verification_doc']
#
#    list_columns = ['id', 'individual', 'qualification', 'qual_class', 'verified', 'verification_code', 'verified_by', 'verification_date', 'verification_doc']
#    list_exclude_columns = [] # ['id', 'individual', 'qualification', 'qual_class', 'verified', 'verification_code', 'verified_by', 'verification_date', 'verification_doc']
#
#    search_columns = ['id', 'individual', 'qualification', 'qual_class', 'verified', 'verification_code', 'verified_by', 'verification_date', 'verification_doc']
#    search_exclude_columns= [] # ['id', 'individual', 'qualification', 'qual_class', 'verified', 'verification_code', 'verified_by', 'verification_date', 'verification_doc']
#
#    default_sort = [('id', True)]
#    base_permissions = ['can_list', 'can_show', 'can_edit', 'can_delete', 'can_add']
#    label_columns=   [{column.name: column.name for column in table.columns} ]
#    show_template =  'appbuilder/general/model/show_cascade.html'
#    list_template = 'appbuilder/general/model/list.html'
#    add_template = 'appbuilder/general/model/add.html'
#    edit_template = 'appbuilder/general/model/edit.html'
#    add_widget = (FormVerticalWidget|FormInlineWidget)
#    show_widget = ShowBlockWidget
#    list_widget = (ListThumbnail|ListWidget)
#    base_order = ('name', 'asc')
#    list_widget= 'list_widget'


class IndividualJobMasterView(MasterDetailView):
    datamodel=SQLAInterface(IndividualJob, db.session)
    related_views = [IndividualDetailView]
    show_title='IndividualJob Detail'
    add_title ='Add IndividualJob'
    list_title= 'IndividualJob List'
    edit_title = 'Edit IndividualJob'
    show_columns = ['individual', 'job']
#    show_exclude_columns = [] #= ['individual', 'job']
#
#    add_columns = ['individual', 'job']
#    add_exclude_columns = [hide_list] #['individual', 'job']
#
#    edit_columns = ['individual', 'job']
#    edit_exclude_columns =[hide_list] # ['individual', 'job']
#
#    list_columns = ['individual', 'job']
#    list_exclude_columns = [] # ['individual', 'job']
#
#    search_columns = ['individual', 'job']
#    search_exclude_columns= [] # ['individual', 'job']
#
#    default_sort = [('id', True)]
#    base_permissions = ['can_list', 'can_show', 'can_edit', 'can_delete', 'can_add']
#    label_columns=   [{column.name: column.name for column in table.columns} ]
#    show_template =  'appbuilder/general/model/show_cascade.html'
#    list_template = 'appbuilder/general/model/list.html'
#    add_template = 'appbuilder/general/model/add.html'
#    edit_template = 'appbuilder/general/model/edit.html'
#    add_widget = (FormVerticalWidget|FormInlineWidget)
#    show_widget = ShowBlockWidget
#    list_widget = (ListThumbnail|ListWidget)
#    base_order = ('name', 'asc')
#    list_widget= 'list_widget'


class IndividualJobMultiView(MultipleView):
    datamodel=SQLAInterface(IndividualJob, db.session)
    views = []
    show_title='IndividualJob Detail'
    add_title ='Add IndividualJob'
    list_title= 'IndividualJob List'
    edit_title = 'Edit IndividualJob'
    show_columns = ['individual', 'job']
#    show_exclude_columns = [] #= ['individual', 'job']
#
#    add_columns = ['individual', 'job']
#    add_exclude_columns = [hide_list] #['individual', 'job']
#
#    edit_columns = ['individual', 'job']
#    edit_exclude_columns =[hide_list] # ['individual', 'job']
#
#    list_columns = ['individual', 'job']
#    list_exclude_columns = [] # ['individual', 'job']
#
#    search_columns = ['individual', 'job']
#    search_exclude_columns= [] # ['individual', 'job']
#
#    default_sort = [('id', True)]
#    base_permissions = ['can_list', 'can_show', 'can_edit', 'can_delete', 'can_add']
#    label_columns=   [{column.name: column.name for column in table.columns} ]
#    show_template =  'appbuilder/general/model/show_cascade.html'
#    list_template = 'appbuilder/general/model/list.html'
#    add_template = 'appbuilder/general/model/add.html'
#    edit_template = 'appbuilder/general/model/edit.html'
#    add_widget = (FormVerticalWidget|FormInlineWidget)
#    show_widget = ShowBlockWidget
#    list_widget = (ListThumbnail|ListWidget)
#    base_order = ('name', 'asc')
#    list_widget= 'list_widget'


class LocationMasterView(MasterDetailView):
    datamodel=SQLAInterface(Location, db.session)
    related_views = [IndividualDetailView]
    show_title='Location Detail'
    add_title ='Add Location'
    list_title= 'Location List'
    edit_title = 'Edit Location'
    show_columns = ['id', 'individual']
#    show_exclude_columns = [] #= ['id', 'individual']
#
#    add_columns = ['id', 'individual']
#    add_exclude_columns = [hide_list] #['id', 'individual']
#
#    edit_columns = ['id', 'individual']
#    edit_exclude_columns =[hide_list] # ['id', 'individual']
#
#    list_columns = ['id', 'individual']
#    list_exclude_columns = [] # ['id', 'individual']
#
#    search_columns = ['id', 'individual']
#    search_exclude_columns= [] # ['id', 'individual']
#
#    default_sort = [('id', True)]
#    base_permissions = ['can_list', 'can_show', 'can_edit', 'can_delete', 'can_add']
#    label_columns=   [{column.name: column.name for column in table.columns} ]
#    show_template =  'appbuilder/general/model/show_cascade.html'
#    list_template = 'appbuilder/general/model/list.html'
#    add_template = 'appbuilder/general/model/add.html'
#    edit_template = 'appbuilder/general/model/edit.html'
#    add_widget = (FormVerticalWidget|FormInlineWidget)
#    show_widget = ShowBlockWidget
#    list_widget = (ListThumbnail|ListWidget)
#    base_order = ('name', 'asc')
#    list_widget= 'list_widget'


class PortalMasterView(MasterDetailView):
    datamodel=SQLAInterface(Portal, db.session)
    related_views = [IndividualDetailView]
    show_title='Portal Detail'
    add_title ='Add Portal'
    list_title= 'Portal List'
    edit_title = 'Edit Portal'
    show_columns = ['id', 'portal_url', 'is_primary', 'portal_state', 'individual', 'has_custom_domain', 'domain', 'header_text', 'slug', 'automatic_fulfillment_digital_products', 'default_digital_max_downloads', 'default_digital_url_valid_days', 'default_mail_sender_name', 'default_mail_sender_address', 'fulfillment_auto_approve', 'fulfillment_allow_unpaid', 'reserve_stock_duration_anonymous_user', 'reserve_stock_duration_authenticated_user', 'limit_quantity_per_checkout', 'gift_card_expiry_type', 'gift_card_expiry_period_type', 'gift_card_expiry_period', 'charge_taxes_on_shipping', 'include_taxes_in_prices', 'display_gross_prices', 'language']
#    show_exclude_columns = [] #= ['id', 'portal_url', 'is_primary', 'portal_state', 'individual', 'has_custom_domain', 'domain', 'header_text', 'slug', 'automatic_fulfillment_digital_products', 'default_digital_max_downloads', 'default_digital_url_valid_days', 'default_mail_sender_name', 'default_mail_sender_address', 'fulfillment_auto_approve', 'fulfillment_allow_unpaid', 'reserve_stock_duration_anonymous_user', 'reserve_stock_duration_authenticated_user', 'limit_quantity_per_checkout', 'gift_card_expiry_type', 'gift_card_expiry_period_type', 'gift_card_expiry_period', 'charge_taxes_on_shipping', 'include_taxes_in_prices', 'display_gross_prices', 'language']
#
#    add_columns = ['id', 'portal_url', 'is_primary', 'portal_state', 'individual', 'has_custom_domain', 'domain', 'header_text', 'slug', 'automatic_fulfillment_digital_products', 'default_digital_max_downloads', 'default_digital_url_valid_days', 'default_mail_sender_name', 'default_mail_sender_address', 'fulfillment_auto_approve', 'fulfillment_allow_unpaid', 'reserve_stock_duration_anonymous_user', 'reserve_stock_duration_authenticated_user', 'limit_quantity_per_checkout', 'gift_card_expiry_type', 'gift_card_expiry_period_type', 'gift_card_expiry_period', 'charge_taxes_on_shipping', 'include_taxes_in_prices', 'display_gross_prices', 'language']
#    add_exclude_columns = [hide_list] #['id', 'portal_url', 'is_primary', 'portal_state', 'individual', 'has_custom_domain', 'domain', 'header_text', 'slug', 'automatic_fulfillment_digital_products', 'default_digital_max_downloads', 'default_digital_url_valid_days', 'default_mail_sender_name', 'default_mail_sender_address', 'fulfillment_auto_approve', 'fulfillment_allow_unpaid', 'reserve_stock_duration_anonymous_user', 'reserve_stock_duration_authenticated_user', 'limit_quantity_per_checkout', 'gift_card_expiry_type', 'gift_card_expiry_period_type', 'gift_card_expiry_period', 'charge_taxes_on_shipping', 'include_taxes_in_prices', 'display_gross_prices', 'language']
#
#    edit_columns = ['id', 'portal_url', 'is_primary', 'portal_state', 'individual', 'has_custom_domain', 'domain', 'header_text', 'slug', 'automatic_fulfillment_digital_products', 'default_digital_max_downloads', 'default_digital_url_valid_days', 'default_mail_sender_name', 'default_mail_sender_address', 'fulfillment_auto_approve', 'fulfillment_allow_unpaid', 'reserve_stock_duration_anonymous_user', 'reserve_stock_duration_authenticated_user', 'limit_quantity_per_checkout', 'gift_card_expiry_type', 'gift_card_expiry_period_type', 'gift_card_expiry_period', 'charge_taxes_on_shipping', 'include_taxes_in_prices', 'display_gross_prices', 'language']
#    edit_exclude_columns =[hide_list] # ['id', 'portal_url', 'is_primary', 'portal_state', 'individual', 'has_custom_domain', 'domain', 'header_text', 'slug', 'automatic_fulfillment_digital_products', 'default_digital_max_downloads', 'default_digital_url_valid_days', 'default_mail_sender_name', 'default_mail_sender_address', 'fulfillment_auto_approve', 'fulfillment_allow_unpaid', 'reserve_stock_duration_anonymous_user', 'reserve_stock_duration_authenticated_user', 'limit_quantity_per_checkout', 'gift_card_expiry_type', 'gift_card_expiry_period_type', 'gift_card_expiry_period', 'charge_taxes_on_shipping', 'include_taxes_in_prices', 'display_gross_prices', 'language']
#
#    list_columns = ['id', 'portal_url', 'is_primary', 'portal_state', 'individual', 'has_custom_domain', 'domain', 'header_text', 'slug', 'automatic_fulfillment_digital_products', 'default_digital_max_downloads', 'default_digital_url_valid_days', 'default_mail_sender_name', 'default_mail_sender_address', 'fulfillment_auto_approve', 'fulfillment_allow_unpaid', 'reserve_stock_duration_anonymous_user', 'reserve_stock_duration_authenticated_user', 'limit_quantity_per_checkout', 'gift_card_expiry_type', 'gift_card_expiry_period_type', 'gift_card_expiry_period', 'charge_taxes_on_shipping', 'include_taxes_in_prices', 'display_gross_prices', 'language']
#    list_exclude_columns = [] # ['id', 'portal_url', 'is_primary', 'portal_state', 'individual', 'has_custom_domain', 'domain', 'header_text', 'slug', 'automatic_fulfillment_digital_products', 'default_digital_max_downloads', 'default_digital_url_valid_days', 'default_mail_sender_name', 'default_mail_sender_address', 'fulfillment_auto_approve', 'fulfillment_allow_unpaid', 'reserve_stock_duration_anonymous_user', 'reserve_stock_duration_authenticated_user', 'limit_quantity_per_checkout', 'gift_card_expiry_type', 'gift_card_expiry_period_type', 'gift_card_expiry_period', 'charge_taxes_on_shipping', 'include_taxes_in_prices', 'display_gross_prices', 'language']
#
#    search_columns = ['id', 'portal_url', 'is_primary', 'portal_state', 'individual', 'has_custom_domain', 'domain', 'header_text', 'slug', 'automatic_fulfillment_digital_products', 'default_digital_max_downloads', 'default_digital_url_valid_days', 'default_mail_sender_name', 'default_mail_sender_address', 'fulfillment_auto_approve', 'fulfillment_allow_unpaid', 'reserve_stock_duration_anonymous_user', 'reserve_stock_duration_authenticated_user', 'limit_quantity_per_checkout', 'gift_card_expiry_type', 'gift_card_expiry_period_type', 'gift_card_expiry_period', 'charge_taxes_on_shipping', 'include_taxes_in_prices', 'display_gross_prices', 'language']
#    search_exclude_columns= [] # ['id', 'portal_url', 'is_primary', 'portal_state', 'individual', 'has_custom_domain', 'domain', 'header_text', 'slug', 'automatic_fulfillment_digital_products', 'default_digital_max_downloads', 'default_digital_url_valid_days', 'default_mail_sender_name', 'default_mail_sender_address', 'fulfillment_auto_approve', 'fulfillment_allow_unpaid', 'reserve_stock_duration_anonymous_user', 'reserve_stock_duration_authenticated_user', 'limit_quantity_per_checkout', 'gift_card_expiry_type', 'gift_card_expiry_period_type', 'gift_card_expiry_period', 'charge_taxes_on_shipping', 'include_taxes_in_prices', 'display_gross_prices', 'language']
#
#    default_sort = [('id', True)]
#    base_permissions = ['can_list', 'can_show', 'can_edit', 'can_delete', 'can_add']
#    label_columns=   [{column.name: column.name for column in table.columns} ]
#    show_template =  'appbuilder/general/model/show_cascade.html'
#    list_template = 'appbuilder/general/model/list.html'
#    add_template = 'appbuilder/general/model/add.html'
#    edit_template = 'appbuilder/general/model/edit.html'
#    add_widget = (FormVerticalWidget|FormInlineWidget)
#    show_widget = ShowBlockWidget
#    list_widget = (ListThumbnail|ListWidget)
#    base_order = ('name', 'asc')
#    list_widget= 'list_widget'


class PageView(ModelView):
    datamodel=SQLAInterface(Page, db.session)
    related_views = []
    show_title='Page Detail'
    add_title ='Add Page'
    list_title= 'Page List'
    edit_title = 'Edit Page'
    show_columns = ['id', 'portal', 'header', 'slug', 'page_type']
#    show_exclude_columns = [] #= ['id', 'portal', 'header', 'slug', 'page_type']
#
#    add_columns = ['id', 'portal', 'header', 'slug', 'page_type']
#    add_exclude_columns = [hide_list] #['id', 'portal', 'header', 'slug', 'page_type']
#
#    edit_columns = ['id', 'portal', 'header', 'slug', 'page_type']
#    edit_exclude_columns =[hide_list] # ['id', 'portal', 'header', 'slug', 'page_type']
#
#    list_columns = ['id', 'portal', 'header', 'slug', 'page_type']
#    list_exclude_columns = [] # ['id', 'portal', 'header', 'slug', 'page_type']
#
#    search_columns = ['id', 'portal', 'header', 'slug', 'page_type']
#    search_exclude_columns= [] # ['id', 'portal', 'header', 'slug', 'page_type']
#
#    default_sort = [('id', True)]
#    base_permissions = ['can_list', 'can_show', 'can_edit', 'can_delete', 'can_add']
#    label_columns=   [{column.name: column.name for column in table.columns} ]
#    show_template =  'appbuilder/general/model/show_cascade.html'
#    list_template = 'appbuilder/general/model/list.html'
#    add_template = 'appbuilder/general/model/add.html'
#    edit_template = 'appbuilder/general/model/edit.html'
#    add_widget = (FormVerticalWidget|FormInlineWidget)
#    show_widget = ShowBlockWidget
#    list_widget = (ListThumbnail|ListWidget)
#    base_order = ('name', 'asc')
#    list_widget= 'list_widget'


class UserxDetailView(ModelView):
    datamodel=SQLAInterface(Userx, db.session)
    related_views = []
    show_title='Userx Detail'
    add_title ='Add Userx'
    list_title= 'Userx List'
    edit_title = 'Edit Userx'
    show_columns = ['id', 'userx', 'is_individual', 'is_institution', 'is_company', 'is_government', 'is_online']
#    show_exclude_columns = [] #= ['id', 'userx', 'is_individual', 'is_institution', 'is_company', 'is_government', 'is_online']
#
#    add_columns = ['id', 'userx', 'is_individual', 'is_institution', 'is_company', 'is_government', 'is_online']
#    add_exclude_columns = [hide_list] #['id', 'userx', 'is_individual', 'is_institution', 'is_company', 'is_government', 'is_online']
#
#    edit_columns = ['id', 'userx', 'is_individual', 'is_institution', 'is_company', 'is_government', 'is_online']
#    edit_exclude_columns =[hide_list] # ['id', 'userx', 'is_individual', 'is_institution', 'is_company', 'is_government', 'is_online']
#
#    list_columns = ['id', 'userx', 'is_individual', 'is_institution', 'is_company', 'is_government', 'is_online']
#    list_exclude_columns = [] # ['id', 'userx', 'is_individual', 'is_institution', 'is_company', 'is_government', 'is_online']
#
#    search_columns = ['id', 'userx', 'is_individual', 'is_institution', 'is_company', 'is_government', 'is_online']
#    search_exclude_columns= [] # ['id', 'userx', 'is_individual', 'is_institution', 'is_company', 'is_government', 'is_online']
#
#    default_sort = [('id', True)]
#    base_permissions = ['can_list', 'can_show', 'can_edit', 'can_delete', 'can_add']
#    label_columns=   [{column.name: column.name for column in table.columns} ]
#    show_template =  'appbuilder/general/model/show_cascade.html'
#    list_template = 'appbuilder/general/model/list.html'
#    add_template = 'appbuilder/general/model/add.html'
#    edit_template = 'appbuilder/general/model/edit.html'
#    add_widget = (FormVerticalWidget|FormInlineWidget)
#    show_widget = ShowBlockWidget
#    list_widget = (ListThumbnail|ListWidget)
#    base_order = ('name', 'asc')
#    list_widget= 'list_widget'


class IndividualDetailView(ModelView):
    datamodel=SQLAInterface(Individual, db.session)
    related_views = []
    show_title='Individual Detail'
    add_title ='Add Individual'
    list_title= 'Individual List'
    edit_title = 'Edit Individual'
    show_columns = ['id', 'userx', 'is_individual', 'is_institution', 'is_company', 'is_government', 'is_online']
#    show_exclude_columns = [] #= ['id', 'userx', 'is_individual', 'is_institution', 'is_company', 'is_government', 'is_online']
#
#    add_columns = ['id', 'userx', 'is_individual', 'is_institution', 'is_company', 'is_government', 'is_online']
#    add_exclude_columns = [hide_list] #['id', 'userx', 'is_individual', 'is_institution', 'is_company', 'is_government', 'is_online']
#
#    edit_columns = ['id', 'userx', 'is_individual', 'is_institution', 'is_company', 'is_government', 'is_online']
#    edit_exclude_columns =[hide_list] # ['id', 'userx', 'is_individual', 'is_institution', 'is_company', 'is_government', 'is_online']
#
#    list_columns = ['id', 'userx', 'is_individual', 'is_institution', 'is_company', 'is_government', 'is_online']
#    list_exclude_columns = [] # ['id', 'userx', 'is_individual', 'is_institution', 'is_company', 'is_government', 'is_online']
#
#    search_columns = ['id', 'userx', 'is_individual', 'is_institution', 'is_company', 'is_government', 'is_online']
#    search_exclude_columns= [] # ['id', 'userx', 'is_individual', 'is_institution', 'is_company', 'is_government', 'is_online']
#
#    default_sort = [('id', True)]
#    base_permissions = ['can_list', 'can_show', 'can_edit', 'can_delete', 'can_add']
#    label_columns=   [{column.name: column.name for column in table.columns} ]
#    show_template =  'appbuilder/general/model/show_cascade.html'
#    list_template = 'appbuilder/general/model/list.html'
#    add_template = 'appbuilder/general/model/add.html'
#    edit_template = 'appbuilder/general/model/edit.html'
#    add_widget = (FormVerticalWidget|FormInlineWidget)
#    show_widget = ShowBlockWidget
#    list_widget = (ListThumbnail|ListWidget)
#    base_order = ('name', 'asc')
#    list_widget= 'list_widget'


class IndustryDetailView(ModelView):
    datamodel=SQLAInterface(Industry, db.session)
    related_views = []
    show_title='Industry Detail'
    add_title ='Add Industry'
    list_title= 'Industry List'
    edit_title = 'Edit Industry'
    show_columns = ['industry', 'job']
#    show_exclude_columns = [] #= ['industry', 'job']
#
#    add_columns = ['industry', 'job']
#    add_exclude_columns = [hide_list] #['industry', 'job']
#
#    edit_columns = ['industry', 'job']
#    edit_exclude_columns =[hide_list] # ['industry', 'job']
#
#    list_columns = ['industry', 'job']
#    list_exclude_columns = [] # ['industry', 'job']
#
#    search_columns = ['industry', 'job']
#    search_exclude_columns= [] # ['industry', 'job']
#
#    default_sort = [('id', True)]
#    base_permissions = ['can_list', 'can_show', 'can_edit', 'can_delete', 'can_add']
#    label_columns=   [{column.name: column.name for column in table.columns} ]
#    show_template =  'appbuilder/general/model/show_cascade.html'
#    list_template = 'appbuilder/general/model/list.html'
#    add_template = 'appbuilder/general/model/add.html'
#    edit_template = 'appbuilder/general/model/edit.html'
#    add_widget = (FormVerticalWidget|FormInlineWidget)
#    show_widget = ShowBlockWidget
#    list_widget = (ListThumbnail|ListWidget)
#    base_order = ('name', 'asc')
#    list_widget= 'list_widget'


class IndustryJobDetailView(ModelView):
    datamodel=SQLAInterface(IndustryJob, db.session)
    related_views = []
    show_title='IndustryJob Detail'
    add_title ='Add IndustryJob'
    list_title= 'IndustryJob List'
    edit_title = 'Edit IndustryJob'
    show_columns = ['industry', 'job']
#    show_exclude_columns = [] #= ['industry', 'job']
#
#    add_columns = ['industry', 'job']
#    add_exclude_columns = [hide_list] #['industry', 'job']
#
#    edit_columns = ['industry', 'job']
#    edit_exclude_columns =[hide_list] # ['industry', 'job']
#
#    list_columns = ['industry', 'job']
#    list_exclude_columns = [] # ['industry', 'job']
#
#    search_columns = ['industry', 'job']
#    search_exclude_columns= [] # ['industry', 'job']
#
#    default_sort = [('id', True)]
#    base_permissions = ['can_list', 'can_show', 'can_edit', 'can_delete', 'can_add']
#    label_columns=   [{column.name: column.name for column in table.columns} ]
#    show_template =  'appbuilder/general/model/show_cascade.html'
#    list_template = 'appbuilder/general/model/list.html'
#    add_template = 'appbuilder/general/model/add.html'
#    edit_template = 'appbuilder/general/model/edit.html'
#    add_widget = (FormVerticalWidget|FormInlineWidget)
#    show_widget = ShowBlockWidget
#    list_widget = (ListThumbnail|ListWidget)
#    base_order = ('name', 'asc')
#    list_widget= 'list_widget'


class JobDetailView(ModelView):
    datamodel=SQLAInterface(Job, db.session)
    related_views = []
    show_title='Job Detail'
    add_title ='Add Job'
    list_title= 'Job List'
    edit_title = 'Edit Job'
    show_columns = ['industry', 'job']
#    show_exclude_columns = [] #= ['industry', 'job']
#
#    add_columns = ['industry', 'job']
#    add_exclude_columns = [hide_list] #['industry', 'job']
#
#    edit_columns = ['industry', 'job']
#    edit_exclude_columns =[hide_list] # ['industry', 'job']
#
#    list_columns = ['industry', 'job']
#    list_exclude_columns = [] # ['industry', 'job']
#
#    search_columns = ['industry', 'job']
#    search_exclude_columns= [] # ['industry', 'job']
#
#    default_sort = [('id', True)]
#    base_permissions = ['can_list', 'can_show', 'can_edit', 'can_delete', 'can_add']
#    label_columns=   [{column.name: column.name for column in table.columns} ]
#    show_template =  'appbuilder/general/model/show_cascade.html'
#    list_template = 'appbuilder/general/model/list.html'
#    add_template = 'appbuilder/general/model/add.html'
#    edit_template = 'appbuilder/general/model/edit.html'
#    add_widget = (FormVerticalWidget|FormInlineWidget)
#    show_widget = ShowBlockWidget
#    list_widget = (ListThumbnail|ListWidget)
#    base_order = ('name', 'asc')
#    list_widget= 'list_widget'




class SkillDetailView(ModelView):
    datamodel=SQLAInterface(Skill, db.session)
    related_views = []
    show_title='Skill Detail'
    add_title ='Add Skill'
    list_title= 'Skill List'
    edit_title = 'Edit Skill'
    show_columns = ['skills', 'jobs']
#    show_exclude_columns = [] #= ['skills', 'jobs']
#
#    add_columns = ['skills', 'jobs']
#    add_exclude_columns = [hide_list] #['skills', 'jobs']
#
#    edit_columns = ['skills', 'jobs']
#    edit_exclude_columns =[hide_list] # ['skills', 'jobs']
#
#    list_columns = ['skills', 'jobs']
#    list_exclude_columns = [] # ['skills', 'jobs']
#
#    search_columns = ['skills', 'jobs']
#    search_exclude_columns= [] # ['skills', 'jobs']
#
#    default_sort = [('id', True)]
#    base_permissions = ['can_list', 'can_show', 'can_edit', 'can_delete', 'can_add']
#    label_columns=   [{column.name: column.name for column in table.columns} ]
#    show_template =  'appbuilder/general/model/show_cascade.html'
#    list_template = 'appbuilder/general/model/list.html'
#    add_template = 'appbuilder/general/model/add.html'
#    edit_template = 'appbuilder/general/model/edit.html'
#    add_widget = (FormVerticalWidget|FormInlineWidget)
#    show_widget = ShowBlockWidget
#    list_widget = (ListThumbnail|ListWidget)
#    base_order = ('name', 'asc')
#    list_widget= 'list_widget'


class JobSkillDetailView(ModelView):
    datamodel=SQLAInterface(JobSkill, db.session)
    related_views = []
    show_title='JobSkill Detail'
    add_title ='Add JobSkill'
    list_title= 'JobSkill List'
    edit_title = 'Edit JobSkill'
    show_columns = ['skills', 'jobs']
#    show_exclude_columns = [] #= ['skills', 'jobs']
#
#    add_columns = ['skills', 'jobs']
#    add_exclude_columns = [hide_list] #['skills', 'jobs']
#
#    edit_columns = ['skills', 'jobs']
#    edit_exclude_columns =[hide_list] # ['skills', 'jobs']
#
#    list_columns = ['skills', 'jobs']
#    list_exclude_columns = [] # ['skills', 'jobs']
#
#    search_columns = ['skills', 'jobs']
#    search_exclude_columns= [] # ['skills', 'jobs']
#
#    default_sort = [('id', True)]
#    base_permissions = ['can_list', 'can_show', 'can_edit', 'can_delete', 'can_add']
#    label_columns=   [{column.name: column.name for column in table.columns} ]
#    show_template =  'appbuilder/general/model/show_cascade.html'
#    list_template = 'appbuilder/general/model/list.html'
#    add_template = 'appbuilder/general/model/add.html'
#    edit_template = 'appbuilder/general/model/edit.html'
#    add_widget = (FormVerticalWidget|FormInlineWidget)
#    show_widget = ShowBlockWidget
#    list_widget = (ListThumbnail|ListWidget)
#    base_order = ('name', 'asc')
#    list_widget= 'list_widget'


class PortalDetailView(ModelView):
    datamodel=SQLAInterface(Portal, db.session)
    related_views = []
    show_title='Portal Detail'
    add_title ='Add Portal'
    list_title= 'Portal List'
    edit_title = 'Edit Portal'
    show_columns = ['id', 'portal', 'header', 'slug', 'page_type']
#    show_exclude_columns = [] #= ['id', 'portal', 'header', 'slug', 'page_type']
#
#    add_columns = ['id', 'portal', 'header', 'slug', 'page_type']
#    add_exclude_columns = [hide_list] #['id', 'portal', 'header', 'slug', 'page_type']
#
#    edit_columns = ['id', 'portal', 'header', 'slug', 'page_type']
#    edit_exclude_columns =[hide_list] # ['id', 'portal', 'header', 'slug', 'page_type']
#
#    list_columns = ['id', 'portal', 'header', 'slug', 'page_type']
#    list_exclude_columns = [] # ['id', 'portal', 'header', 'slug', 'page_type']
#
#    search_columns = ['id', 'portal', 'header', 'slug', 'page_type']
#    search_exclude_columns= [] # ['id', 'portal', 'header', 'slug', 'page_type']
#
#    default_sort = [('id', True)]
#    base_permissions = ['can_list', 'can_show', 'can_edit', 'can_delete', 'can_add']
#    label_columns=   [{column.name: column.name for column in table.columns} ]
#    show_template =  'appbuilder/general/model/show_cascade.html'
#    list_template = 'appbuilder/general/model/list.html'
#    add_template = 'appbuilder/general/model/add.html'
#    edit_template = 'appbuilder/general/model/edit.html'
#    add_widget = (FormVerticalWidget|FormInlineWidget)
#    show_widget = ShowBlockWidget
#    list_widget = (ListThumbnail|ListWidget)
#    base_order = ('name', 'asc')
#    list_widget= 'list_widget'


class PageDetailView(ModelView):
    datamodel=SQLAInterface(Page, db.session)
    related_views = []
    show_title='Page Detail'
    add_title ='Add Page'
    list_title= 'Page List'
    edit_title = 'Edit Page'
    show_columns = ['id', 'portal', 'header', 'slug', 'page_type']
#    show_exclude_columns = [] #= ['id', 'portal', 'header', 'slug', 'page_type']
#
#    add_columns = ['id', 'portal', 'header', 'slug', 'page_type']
#    add_exclude_columns = [hide_list] #['id', 'portal', 'header', 'slug', 'page_type']
#
#    edit_columns = ['id', 'portal', 'header', 'slug', 'page_type']
#    edit_exclude_columns =[hide_list] # ['id', 'portal', 'header', 'slug', 'page_type']
#
#    list_columns = ['id', 'portal', 'header', 'slug', 'page_type']
#    list_exclude_columns = [] # ['id', 'portal', 'header', 'slug', 'page_type']
#
#    search_columns = ['id', 'portal', 'header', 'slug', 'page_type']
#    search_exclude_columns= [] # ['id', 'portal', 'header', 'slug', 'page_type']
#
#    default_sort = [('id', True)]
#    base_permissions = ['can_list', 'can_show', 'can_edit', 'can_delete', 'can_add']
#    label_columns=   [{column.name: column.name for column in table.columns} ]
#    show_template =  'appbuilder/general/model/show_cascade.html'
#    list_template = 'appbuilder/general/model/list.html'
#    add_template = 'appbuilder/general/model/add.html'
#    edit_template = 'appbuilder/general/model/edit.html'
#    add_widget = (FormVerticalWidget|FormInlineWidget)
#    show_widget = ShowBlockWidget
#    list_widget = (ListThumbnail|ListWidget)
#    base_order = ('name', 'asc')
#    list_widget= 'list_widget'


class IndividualMasterView(MasterDetailView):
    datamodel=SQLAInterface(Individual, db.session)
    related_views = [UserxDetailView]
    show_title='Individual Detail'
    add_title ='Add Individual'
    list_title= 'Individual List'
    edit_title = 'Edit Individual'
    show_columns = ['id', 'userx', 'is_individual', 'is_institution', 'is_company', 'is_government', 'is_online']
#    show_exclude_columns = [] #= ['id', 'userx', 'is_individual', 'is_institution', 'is_company', 'is_government', 'is_online']
#
#    add_columns = ['id', 'userx', 'is_individual', 'is_institution', 'is_company', 'is_government', 'is_online']
#    add_exclude_columns = [hide_list] #['id', 'userx', 'is_individual', 'is_institution', 'is_company', 'is_government', 'is_online']
#
#    edit_columns = ['id', 'userx', 'is_individual', 'is_institution', 'is_company', 'is_government', 'is_online']
#    edit_exclude_columns =[hide_list] # ['id', 'userx', 'is_individual', 'is_institution', 'is_company', 'is_government', 'is_online']
#
#    list_columns = ['id', 'userx', 'is_individual', 'is_institution', 'is_company', 'is_government', 'is_online']
#    list_exclude_columns = [] # ['id', 'userx', 'is_individual', 'is_institution', 'is_company', 'is_government', 'is_online']
#
#    search_columns = ['id', 'userx', 'is_individual', 'is_institution', 'is_company', 'is_government', 'is_online']
#    search_exclude_columns= [] # ['id', 'userx', 'is_individual', 'is_institution', 'is_company', 'is_government', 'is_online']
#
#    default_sort = [('id', True)]
#    base_permissions = ['can_list', 'can_show', 'can_edit', 'can_delete', 'can_add']
#    label_columns=   [{column.name: column.name for column in table.columns} ]
#    show_template =  'appbuilder/general/model/show_cascade.html'
#    list_template = 'appbuilder/general/model/list.html'
#    add_template = 'appbuilder/general/model/add.html'
#    edit_template = 'appbuilder/general/model/edit.html'
#    add_widget = (FormVerticalWidget|FormInlineWidget)
#    show_widget = ShowBlockWidget
#    list_widget = (ListThumbnail|ListWidget)
#    base_order = ('name', 'asc')
#    list_widget= 'list_widget'


class IndustryJobMasterView(MasterDetailView):
    datamodel=SQLAInterface(IndustryJob, db.session)
    related_views = [IndustryDetailView]
    show_title='IndustryJob Detail'
    add_title ='Add IndustryJob'
    list_title= 'IndustryJob List'
    edit_title = 'Edit IndustryJob'
    show_columns = ['industry', 'job']
#    show_exclude_columns = [] #= ['industry', 'job']
#
#    add_columns = ['industry', 'job']
#    add_exclude_columns = [hide_list] #['industry', 'job']
#
#    edit_columns = ['industry', 'job']
#    edit_exclude_columns =[hide_list] # ['industry', 'job']
#
#    list_columns = ['industry', 'job']
#    list_exclude_columns = [] # ['industry', 'job']
#
#    search_columns = ['industry', 'job']
#    search_exclude_columns= [] # ['industry', 'job']
#
#    default_sort = [('id', True)]
#    base_permissions = ['can_list', 'can_show', 'can_edit', 'can_delete', 'can_add']
#    label_columns=   [{column.name: column.name for column in table.columns} ]
#    show_template =  'appbuilder/general/model/show_cascade.html'
#    list_template = 'appbuilder/general/model/list.html'
#    add_template = 'appbuilder/general/model/add.html'
#    edit_template = 'appbuilder/general/model/edit.html'
#    add_widget = (FormVerticalWidget|FormInlineWidget)
#    show_widget = ShowBlockWidget
#    list_widget = (ListThumbnail|ListWidget)
#    base_order = ('name', 'asc')
#    list_widget= 'list_widget'


class IndustryJobMultiView(MultipleView):
    datamodel=SQLAInterface(IndustryJob, db.session)
    views = [IndustryDetailView, JobDetailView]
    show_title='IndustryJob Detail'
    add_title ='Add IndustryJob'
    list_title= 'IndustryJob List'
    edit_title = 'Edit IndustryJob'
    show_columns = ['industry', 'job']
#    show_exclude_columns = [] #= ['industry', 'job']
#
#    add_columns = ['industry', 'job']
#    add_exclude_columns = [hide_list] #['industry', 'job']
#
#    edit_columns = ['industry', 'job']
#    edit_exclude_columns =[hide_list] # ['industry', 'job']
#
#    list_columns = ['industry', 'job']
#    list_exclude_columns = [] # ['industry', 'job']
#
#    search_columns = ['industry', 'job']
#    search_exclude_columns= [] # ['industry', 'job']
#
#    default_sort = [('id', True)]
#    base_permissions = ['can_list', 'can_show', 'can_edit', 'can_delete', 'can_add']
#    label_columns=   [{column.name: column.name for column in table.columns} ]
#    show_template =  'appbuilder/general/model/show_cascade.html'
#    list_template = 'appbuilder/general/model/list.html'
#    add_template = 'appbuilder/general/model/add.html'
#    edit_template = 'appbuilder/general/model/edit.html'
#    add_widget = (FormVerticalWidget|FormInlineWidget)
#    show_widget = ShowBlockWidget
#    list_widget = (ListThumbnail|ListWidget)
#    base_order = ('name', 'asc')
#    list_widget= 'list_widget'


class JobSkillMasterView(MasterDetailView):
    datamodel=SQLAInterface(JobSkill, db.session)
    related_views = [JobDetailView]
    show_title='JobSkill Detail'
    add_title ='Add JobSkill'
    list_title= 'JobSkill List'
    edit_title = 'Edit JobSkill'
    show_columns = ['skills', 'jobs']
#    show_exclude_columns = [] #= ['skills', 'jobs']
#
#    add_columns = ['skills', 'jobs']
#    add_exclude_columns = [hide_list] #['skills', 'jobs']
#
#    edit_columns = ['skills', 'jobs']
#    edit_exclude_columns =[hide_list] # ['skills', 'jobs']
#
#    list_columns = ['skills', 'jobs']
#    list_exclude_columns = [] # ['skills', 'jobs']
#
#    search_columns = ['skills', 'jobs']
#    search_exclude_columns= [] # ['skills', 'jobs']
#
#    default_sort = [('id', True)]
#    base_permissions = ['can_list', 'can_show', 'can_edit', 'can_delete', 'can_add']
#    label_columns=   [{column.name: column.name for column in table.columns} ]
#    show_template =  'appbuilder/general/model/show_cascade.html'
#    list_template = 'appbuilder/general/model/list.html'
#    add_template = 'appbuilder/general/model/add.html'
#    edit_template = 'appbuilder/general/model/edit.html'
#    add_widget = (FormVerticalWidget|FormInlineWidget)
#    show_widget = ShowBlockWidget
#    list_widget = (ListThumbnail|ListWidget)
#    base_order = ('name', 'asc')
#    list_widget= 'list_widget'


class JobSkillMultiView(MultipleView):
    datamodel=SQLAInterface(JobSkill, db.session)
    views = [SkillDetailView]
    show_title='JobSkill Detail'
    add_title ='Add JobSkill'
    list_title= 'JobSkill List'
    edit_title = 'Edit JobSkill'
    show_columns = ['skills', 'jobs']
#    show_exclude_columns = [] #= ['skills', 'jobs']
#
#    add_columns = ['skills', 'jobs']
#    add_exclude_columns = [hide_list] #['skills', 'jobs']
#
#    edit_columns = ['skills', 'jobs']
#    edit_exclude_columns =[hide_list] # ['skills', 'jobs']
#
#    list_columns = ['skills', 'jobs']
#    list_exclude_columns = [] # ['skills', 'jobs']
#
#    search_columns = ['skills', 'jobs']
#    search_exclude_columns= [] # ['skills', 'jobs']
#
#    default_sort = [('id', True)]
#    base_permissions = ['can_list', 'can_show', 'can_edit', 'can_delete', 'can_add']
#    label_columns=   [{column.name: column.name for column in table.columns} ]
#    show_template =  'appbuilder/general/model/show_cascade.html'
#    list_template = 'appbuilder/general/model/list.html'
#    add_template = 'appbuilder/general/model/add.html'
#    edit_template = 'appbuilder/general/model/edit.html'
#    add_widget = (FormVerticalWidget|FormInlineWidget)
#    show_widget = ShowBlockWidget
#    list_widget = (ListThumbnail|ListWidget)
#    base_order = ('name', 'asc')
#    list_widget= 'list_widget'


class EducationMasterView(MasterDetailView):
    datamodel=SQLAInterface(Education, db.session)
    related_views = [IndividualDetailView]
    show_title='Education Detail'
    add_title ='Add Education'
    list_title= 'Education List'
    edit_title = 'Edit Education'
    show_columns = ['id', 'individual', 'qualification', 'qual_class', 'verified', 'verification_code', 'verified_by', 'verification_date', 'verification_doc']
#    show_exclude_columns = [] #= ['id', 'individual', 'qualification', 'qual_class', 'verified', 'verification_code', 'verified_by', 'verification_date', 'verification_doc']
#
#    add_columns = ['id', 'individual', 'qualification', 'qual_class', 'verified', 'verification_code', 'verified_by', 'verification_date', 'verification_doc']
#    add_exclude_columns = [hide_list] #['id', 'individual', 'qualification', 'qual_class', 'verified', 'verification_code', 'verified_by', 'verification_date', 'verification_doc']
#
#    edit_columns = ['id', 'individual', 'qualification', 'qual_class', 'verified', 'verification_code', 'verified_by', 'verification_date', 'verification_doc']
#    edit_exclude_columns =[hide_list] # ['id', 'individual', 'qualification', 'qual_class', 'verified', 'verification_code', 'verified_by', 'verification_date', 'verification_doc']
#
#    list_columns = ['id', 'individual', 'qualification', 'qual_class', 'verified', 'verification_code', 'verified_by', 'verification_date', 'verification_doc']
#    list_exclude_columns = [] # ['id', 'individual', 'qualification', 'qual_class', 'verified', 'verification_code', 'verified_by', 'verification_date', 'verification_doc']
#
#    search_columns = ['id', 'individual', 'qualification', 'qual_class', 'verified', 'verification_code', 'verified_by', 'verification_date', 'verification_doc']
#    search_exclude_columns= [] # ['id', 'individual', 'qualification', 'qual_class', 'verified', 'verification_code', 'verified_by', 'verification_date', 'verification_doc']
#
#    default_sort = [('id', True)]
#    base_permissions = ['can_list', 'can_show', 'can_edit', 'can_delete', 'can_add']
#    label_columns=   [{column.name: column.name for column in table.columns} ]
#    show_template =  'appbuilder/general/model/show_cascade.html'
#    list_template = 'appbuilder/general/model/list.html'
#    add_template = 'appbuilder/general/model/add.html'
#    edit_template = 'appbuilder/general/model/edit.html'
#    add_widget = (FormVerticalWidget|FormInlineWidget)
#    show_widget = ShowBlockWidget
#    list_widget = (ListThumbnail|ListWidget)
#    base_order = ('name', 'asc')
#    list_widget= 'list_widget'


class IndividualJobMasterView(MasterDetailView):
    datamodel=SQLAInterface(IndividualJob, db.session)
    related_views = [IndividualDetailView]
    show_title='IndividualJob Detail'
    add_title ='Add IndividualJob'
    list_title= 'IndividualJob List'
    edit_title = 'Edit IndividualJob'
    show_columns = ['individual', 'job']
#    show_exclude_columns = [] #= ['individual', 'job']
#
#    add_columns = ['individual', 'job']
#    add_exclude_columns = [hide_list] #['individual', 'job']
#
#    edit_columns = ['individual', 'job']
#    edit_exclude_columns =[hide_list] # ['individual', 'job']
#
#    list_columns = ['individual', 'job']
#    list_exclude_columns = [] # ['individual', 'job']
#
#    search_columns = ['individual', 'job']
#    search_exclude_columns= [] # ['individual', 'job']
#
#    default_sort = [('id', True)]
#    base_permissions = ['can_list', 'can_show', 'can_edit', 'can_delete', 'can_add']
#    label_columns=   [{column.name: column.name for column in table.columns} ]
#    show_template =  'appbuilder/general/model/show_cascade.html'
#    list_template = 'appbuilder/general/model/list.html'
#    add_template = 'appbuilder/general/model/add.html'
#    edit_template = 'appbuilder/general/model/edit.html'
#    add_widget = (FormVerticalWidget|FormInlineWidget)
#    show_widget = ShowBlockWidget
#    list_widget = (ListThumbnail|ListWidget)
#    base_order = ('name', 'asc')
#    list_widget= 'list_widget'


class IndividualJobMultiView(MultipleView):
    datamodel=SQLAInterface(IndividualJob, db.session)
    views = []
    show_title='IndividualJob Detail'
    add_title ='Add IndividualJob'
    list_title= 'IndividualJob List'
    edit_title = 'Edit IndividualJob'
    show_columns = ['individual', 'job']
#    show_exclude_columns = [] #= ['individual', 'job']
#
#    add_columns = ['individual', 'job']
#    add_exclude_columns = [hide_list] #['individual', 'job']
#
#    edit_columns = ['individual', 'job']
#    edit_exclude_columns =[hide_list] # ['individual', 'job']
#
#    list_columns = ['individual', 'job']
#    list_exclude_columns = [] # ['individual', 'job']
#
#    search_columns = ['individual', 'job']
#    search_exclude_columns= [] # ['individual', 'job']
#
#    default_sort = [('id', True)]
#    base_permissions = ['can_list', 'can_show', 'can_edit', 'can_delete', 'can_add']
#    label_columns=   [{column.name: column.name for column in table.columns} ]
#    show_template =  'appbuilder/general/model/show_cascade.html'
#    list_template = 'appbuilder/general/model/list.html'
#    add_template = 'appbuilder/general/model/add.html'
#    edit_template = 'appbuilder/general/model/edit.html'
#    add_widget = (FormVerticalWidget|FormInlineWidget)
#    show_widget = ShowBlockWidget
#    list_widget = (ListThumbnail|ListWidget)
#    base_order = ('name', 'asc')
#    list_widget= 'list_widget'


class LocationMasterView(MasterDetailView):
    datamodel=SQLAInterface(Location, db.session)
    related_views = [IndividualDetailView]
    show_title='Location Detail'
    add_title ='Add Location'
    list_title= 'Location List'
    edit_title = 'Edit Location'
    show_columns = ['id', 'individual']
#    show_exclude_columns = [] #= ['id', 'individual']
#
#    add_columns = ['id', 'individual']
#    add_exclude_columns = [hide_list] #['id', 'individual']
#
#    edit_columns = ['id', 'individual']
#    edit_exclude_columns =[hide_list] # ['id', 'individual']
#
#    list_columns = ['id', 'individual']
#    list_exclude_columns = [] # ['id', 'individual']
#
#    search_columns = ['id', 'individual']
#    search_exclude_columns= [] # ['id', 'individual']
#
#    default_sort = [('id', True)]
#    base_permissions = ['can_list', 'can_show', 'can_edit', 'can_delete', 'can_add']
#    label_columns=   [{column.name: column.name for column in table.columns} ]
#    show_template =  'appbuilder/general/model/show_cascade.html'
#    list_template = 'appbuilder/general/model/list.html'
#    add_template = 'appbuilder/general/model/add.html'
#    edit_template = 'appbuilder/general/model/edit.html'
#    add_widget = (FormVerticalWidget|FormInlineWidget)
#    show_widget = ShowBlockWidget
#    list_widget = (ListThumbnail|ListWidget)
#    base_order = ('name', 'asc')
#    list_widget= 'list_widget'


class PortalMasterView(MasterDetailView):
    datamodel=SQLAInterface(Portal, db.session)
    related_views = [IndividualDetailView]
    show_title='Portal Detail'
    add_title ='Add Portal'
    list_title= 'Portal List'
    edit_title = 'Edit Portal'
    show_columns = ['id', 'portal_url', 'is_primary', 'portal_state', 'individual', 'has_custom_domain', 'domain', 'header_text', 'slug', 'automatic_fulfillment_digital_products', 'default_digital_max_downloads', 'default_digital_url_valid_days', 'default_mail_sender_name', 'default_mail_sender_address', 'fulfillment_auto_approve', 'fulfillment_allow_unpaid', 'reserve_stock_duration_anonymous_user', 'reserve_stock_duration_authenticated_user', 'limit_quantity_per_checkout', 'gift_card_expiry_type', 'gift_card_expiry_period_type', 'gift_card_expiry_period', 'charge_taxes_on_shipping', 'include_taxes_in_prices', 'display_gross_prices', 'language']
#    show_exclude_columns = [] #= ['id', 'portal_url', 'is_primary', 'portal_state', 'individual', 'has_custom_domain', 'domain', 'header_text', 'slug', 'automatic_fulfillment_digital_products', 'default_digital_max_downloads', 'default_digital_url_valid_days', 'default_mail_sender_name', 'default_mail_sender_address', 'fulfillment_auto_approve', 'fulfillment_allow_unpaid', 'reserve_stock_duration_anonymous_user', 'reserve_stock_duration_authenticated_user', 'limit_quantity_per_checkout', 'gift_card_expiry_type', 'gift_card_expiry_period_type', 'gift_card_expiry_period', 'charge_taxes_on_shipping', 'include_taxes_in_prices', 'display_gross_prices', 'language']
#
#    add_columns = ['id', 'portal_url', 'is_primary', 'portal_state', 'individual', 'has_custom_domain', 'domain', 'header_text', 'slug', 'automatic_fulfillment_digital_products', 'default_digital_max_downloads', 'default_digital_url_valid_days', 'default_mail_sender_name', 'default_mail_sender_address', 'fulfillment_auto_approve', 'fulfillment_allow_unpaid', 'reserve_stock_duration_anonymous_user', 'reserve_stock_duration_authenticated_user', 'limit_quantity_per_checkout', 'gift_card_expiry_type', 'gift_card_expiry_period_type', 'gift_card_expiry_period', 'charge_taxes_on_shipping', 'include_taxes_in_prices', 'display_gross_prices', 'language']
#    add_exclude_columns = [hide_list] #['id', 'portal_url', 'is_primary', 'portal_state', 'individual', 'has_custom_domain', 'domain', 'header_text', 'slug', 'automatic_fulfillment_digital_products', 'default_digital_max_downloads', 'default_digital_url_valid_days', 'default_mail_sender_name', 'default_mail_sender_address', 'fulfillment_auto_approve', 'fulfillment_allow_unpaid', 'reserve_stock_duration_anonymous_user', 'reserve_stock_duration_authenticated_user', 'limit_quantity_per_checkout', 'gift_card_expiry_type', 'gift_card_expiry_period_type', 'gift_card_expiry_period', 'charge_taxes_on_shipping', 'include_taxes_in_prices', 'display_gross_prices', 'language']
#
#    edit_columns = ['id', 'portal_url', 'is_primary', 'portal_state', 'individual', 'has_custom_domain', 'domain', 'header_text', 'slug', 'automatic_fulfillment_digital_products', 'default_digital_max_downloads', 'default_digital_url_valid_days', 'default_mail_sender_name', 'default_mail_sender_address', 'fulfillment_auto_approve', 'fulfillment_allow_unpaid', 'reserve_stock_duration_anonymous_user', 'reserve_stock_duration_authenticated_user', 'limit_quantity_per_checkout', 'gift_card_expiry_type', 'gift_card_expiry_period_type', 'gift_card_expiry_period', 'charge_taxes_on_shipping', 'include_taxes_in_prices', 'display_gross_prices', 'language']
#    edit_exclude_columns =[hide_list] # ['id', 'portal_url', 'is_primary', 'portal_state', 'individual', 'has_custom_domain', 'domain', 'header_text', 'slug', 'automatic_fulfillment_digital_products', 'default_digital_max_downloads', 'default_digital_url_valid_days', 'default_mail_sender_name', 'default_mail_sender_address', 'fulfillment_auto_approve', 'fulfillment_allow_unpaid', 'reserve_stock_duration_anonymous_user', 'reserve_stock_duration_authenticated_user', 'limit_quantity_per_checkout', 'gift_card_expiry_type', 'gift_card_expiry_period_type', 'gift_card_expiry_period', 'charge_taxes_on_shipping', 'include_taxes_in_prices', 'display_gross_prices', 'language']
#
#    list_columns = ['id', 'portal_url', 'is_primary', 'portal_state', 'individual', 'has_custom_domain', 'domain', 'header_text', 'slug', 'automatic_fulfillment_digital_products', 'default_digital_max_downloads', 'default_digital_url_valid_days', 'default_mail_sender_name', 'default_mail_sender_address', 'fulfillment_auto_approve', 'fulfillment_allow_unpaid', 'reserve_stock_duration_anonymous_user', 'reserve_stock_duration_authenticated_user', 'limit_quantity_per_checkout', 'gift_card_expiry_type', 'gift_card_expiry_period_type', 'gift_card_expiry_period', 'charge_taxes_on_shipping', 'include_taxes_in_prices', 'display_gross_prices', 'language']
#    list_exclude_columns = [] # ['id', 'portal_url', 'is_primary', 'portal_state', 'individual', 'has_custom_domain', 'domain', 'header_text', 'slug', 'automatic_fulfillment_digital_products', 'default_digital_max_downloads', 'default_digital_url_valid_days', 'default_mail_sender_name', 'default_mail_sender_address', 'fulfillment_auto_approve', 'fulfillment_allow_unpaid', 'reserve_stock_duration_anonymous_user', 'reserve_stock_duration_authenticated_user', 'limit_quantity_per_checkout', 'gift_card_expiry_type', 'gift_card_expiry_period_type', 'gift_card_expiry_period', 'charge_taxes_on_shipping', 'include_taxes_in_prices', 'display_gross_prices', 'language']
#
#    search_columns = ['id', 'portal_url', 'is_primary', 'portal_state', 'individual', 'has_custom_domain', 'domain', 'header_text', 'slug', 'automatic_fulfillment_digital_products', 'default_digital_max_downloads', 'default_digital_url_valid_days', 'default_mail_sender_name', 'default_mail_sender_address', 'fulfillment_auto_approve', 'fulfillment_allow_unpaid', 'reserve_stock_duration_anonymous_user', 'reserve_stock_duration_authenticated_user', 'limit_quantity_per_checkout', 'gift_card_expiry_type', 'gift_card_expiry_period_type', 'gift_card_expiry_period', 'charge_taxes_on_shipping', 'include_taxes_in_prices', 'display_gross_prices', 'language']
#    search_exclude_columns= [] # ['id', 'portal_url', 'is_primary', 'portal_state', 'individual', 'has_custom_domain', 'domain', 'header_text', 'slug', 'automatic_fulfillment_digital_products', 'default_digital_max_downloads', 'default_digital_url_valid_days', 'default_mail_sender_name', 'default_mail_sender_address', 'fulfillment_auto_approve', 'fulfillment_allow_unpaid', 'reserve_stock_duration_anonymous_user', 'reserve_stock_duration_authenticated_user', 'limit_quantity_per_checkout', 'gift_card_expiry_type', 'gift_card_expiry_period_type', 'gift_card_expiry_period', 'charge_taxes_on_shipping', 'include_taxes_in_prices', 'display_gross_prices', 'language']
#
#    default_sort = [('id', True)]
#    base_permissions = ['can_list', 'can_show', 'can_edit', 'can_delete', 'can_add']
#    label_columns=   [{column.name: column.name for column in table.columns} ]
#    show_template =  'appbuilder/general/model/show_cascade.html'
#    list_template = 'appbuilder/general/model/list.html'
#    add_template = 'appbuilder/general/model/add.html'
#    edit_template = 'appbuilder/general/model/edit.html'
#    add_widget = (FormVerticalWidget|FormInlineWidget)
#    show_widget = ShowBlockWidget
#    list_widget = (ListThumbnail|ListWidget)
#    base_order = ('name', 'asc')
#    list_widget= 'list_widget'


class PageMasterView(MasterDetailView):
    datamodel=SQLAInterface(Page, db.session)
    related_views = [PortalDetailView]
    show_title='Page Detail'
    add_title ='Add Page'
    list_title= 'Page List'
    edit_title = 'Edit Page'
    show_columns = ['id', 'portal', 'header', 'slug', 'page_type']
#    show_exclude_columns = [] #= ['id', 'portal', 'header', 'slug', 'page_type']
#
#    add_columns = ['id', 'portal', 'header', 'slug', 'page_type']
#    add_exclude_columns = [hide_list] #['id', 'portal', 'header', 'slug', 'page_type']
#
#    edit_columns = ['id', 'portal', 'header', 'slug', 'page_type']
#    edit_exclude_columns =[hide_list] # ['id', 'portal', 'header', 'slug', 'page_type']
#
#    list_columns = ['id', 'portal', 'header', 'slug', 'page_type']
#    list_exclude_columns = [] # ['id', 'portal', 'header', 'slug', 'page_type']
#
#    search_columns = ['id', 'portal', 'header', 'slug', 'page_type']
#    search_exclude_columns= [] # ['id', 'portal', 'header', 'slug', 'page_type']
#
#    default_sort = [('id', True)]
#    base_permissions = ['can_list', 'can_show', 'can_edit', 'can_delete', 'can_add']
#    label_columns=   [{column.name: column.name for column in table.columns} ]
#    show_template =  'appbuilder/general/model/show_cascade.html'
#    list_template = 'appbuilder/general/model/list.html'
#    add_template = 'appbuilder/general/model/add.html'
#    edit_template = 'appbuilder/general/model/edit.html'
#    add_widget = (FormVerticalWidget|FormInlineWidget)
#    show_widget = ShowBlockWidget
#    list_widget = (ListThumbnail|ListWidget)
#    base_order = ('name', 'asc')
#    list_widget= 'list_widget'


class ProfileView(ModelView):
    datamodel=SQLAInterface(Profile, db.session)
    related_views = []
    show_title='Profile Detail'
    add_title ='Add Profile'
    list_title= 'Profile List'
    edit_title = 'Edit Profile'
    show_columns = ['id', 'individual', 'import_address', 'profile_username', 'profile_password', 'has_been_imported', 'import_data', 'import_date', 'profilesource']
#    show_exclude_columns = [] #= ['id', 'individual', 'import_address', 'profile_username', 'profile_password', 'has_been_imported', 'import_data', 'import_date', 'profilesource']
#
#    add_columns = ['id', 'individual', 'import_address', 'profile_username', 'profile_password', 'has_been_imported', 'import_data', 'import_date', 'profilesource']
#    add_exclude_columns = [hide_list] #['id', 'individual', 'import_address', 'profile_username', 'profile_password', 'has_been_imported', 'import_data', 'import_date', 'profilesource']
#
#    edit_columns = ['id', 'individual', 'import_address', 'profile_username', 'profile_password', 'has_been_imported', 'import_data', 'import_date', 'profilesource']
#    edit_exclude_columns =[hide_list] # ['id', 'individual', 'import_address', 'profile_username', 'profile_password', 'has_been_imported', 'import_data', 'import_date', 'profilesource']
#
#    list_columns = ['id', 'individual', 'import_address', 'profile_username', 'profile_password', 'has_been_imported', 'import_data', 'import_date', 'profilesource']
#    list_exclude_columns = [] # ['id', 'individual', 'import_address', 'profile_username', 'profile_password', 'has_been_imported', 'import_data', 'import_date', 'profilesource']
#
#    search_columns = ['id', 'individual', 'import_address', 'profile_username', 'profile_password', 'has_been_imported', 'import_data', 'import_date', 'profilesource']
#    search_exclude_columns= [] # ['id', 'individual', 'import_address', 'profile_username', 'profile_password', 'has_been_imported', 'import_data', 'import_date', 'profilesource']
#
#    default_sort = [('id', True)]
#    base_permissions = ['can_list', 'can_show', 'can_edit', 'can_delete', 'can_add']
#    label_columns=   [{column.name: column.name for column in table.columns} ]
#    show_template =  'appbuilder/general/model/show_cascade.html'
#    list_template = 'appbuilder/general/model/list.html'
#    add_template = 'appbuilder/general/model/add.html'
#    edit_template = 'appbuilder/general/model/edit.html'
#    add_widget = (FormVerticalWidget|FormInlineWidget)
#    show_widget = ShowBlockWidget
#    list_widget = (ListThumbnail|ListWidget)
#    base_order = ('name', 'asc')
#    list_widget= 'list_widget'


class UserxDetailView(ModelView):
    datamodel=SQLAInterface(Userx, db.session)
    related_views = []
    show_title='Userx Detail'
    add_title ='Add Userx'
    list_title= 'Userx List'
    edit_title = 'Edit Userx'
    show_columns = ['id', 'userx', 'is_individual', 'is_institution', 'is_company', 'is_government', 'is_online']
#    show_exclude_columns = [] #= ['id', 'userx', 'is_individual', 'is_institution', 'is_company', 'is_government', 'is_online']
#
#    add_columns = ['id', 'userx', 'is_individual', 'is_institution', 'is_company', 'is_government', 'is_online']
#    add_exclude_columns = [hide_list] #['id', 'userx', 'is_individual', 'is_institution', 'is_company', 'is_government', 'is_online']
#
#    edit_columns = ['id', 'userx', 'is_individual', 'is_institution', 'is_company', 'is_government', 'is_online']
#    edit_exclude_columns =[hide_list] # ['id', 'userx', 'is_individual', 'is_institution', 'is_company', 'is_government', 'is_online']
#
#    list_columns = ['id', 'userx', 'is_individual', 'is_institution', 'is_company', 'is_government', 'is_online']
#    list_exclude_columns = [] # ['id', 'userx', 'is_individual', 'is_institution', 'is_company', 'is_government', 'is_online']
#
#    search_columns = ['id', 'userx', 'is_individual', 'is_institution', 'is_company', 'is_government', 'is_online']
#    search_exclude_columns= [] # ['id', 'userx', 'is_individual', 'is_institution', 'is_company', 'is_government', 'is_online']
#
#    default_sort = [('id', True)]
#    base_permissions = ['can_list', 'can_show', 'can_edit', 'can_delete', 'can_add']
#    label_columns=   [{column.name: column.name for column in table.columns} ]
#    show_template =  'appbuilder/general/model/show_cascade.html'
#    list_template = 'appbuilder/general/model/list.html'
#    add_template = 'appbuilder/general/model/add.html'
#    edit_template = 'appbuilder/general/model/edit.html'
#    add_widget = (FormVerticalWidget|FormInlineWidget)
#    show_widget = ShowBlockWidget
#    list_widget = (ListThumbnail|ListWidget)
#    base_order = ('name', 'asc')
#    list_widget= 'list_widget'


class IndividualDetailView(ModelView):
    datamodel=SQLAInterface(Individual, db.session)
    related_views = []
    show_title='Individual Detail'
    add_title ='Add Individual'
    list_title= 'Individual List'
    edit_title = 'Edit Individual'
    show_columns = ['id', 'userx', 'is_individual', 'is_institution', 'is_company', 'is_government', 'is_online']
#    show_exclude_columns = [] #= ['id', 'userx', 'is_individual', 'is_institution', 'is_company', 'is_government', 'is_online']
#
#    add_columns = ['id', 'userx', 'is_individual', 'is_institution', 'is_company', 'is_government', 'is_online']
#    add_exclude_columns = [hide_list] #['id', 'userx', 'is_individual', 'is_institution', 'is_company', 'is_government', 'is_online']
#
#    edit_columns = ['id', 'userx', 'is_individual', 'is_institution', 'is_company', 'is_government', 'is_online']
#    edit_exclude_columns =[hide_list] # ['id', 'userx', 'is_individual', 'is_institution', 'is_company', 'is_government', 'is_online']
#
#    list_columns = ['id', 'userx', 'is_individual', 'is_institution', 'is_company', 'is_government', 'is_online']
#    list_exclude_columns = [] # ['id', 'userx', 'is_individual', 'is_institution', 'is_company', 'is_government', 'is_online']
#
#    search_columns = ['id', 'userx', 'is_individual', 'is_institution', 'is_company', 'is_government', 'is_online']
#    search_exclude_columns= [] # ['id', 'userx', 'is_individual', 'is_institution', 'is_company', 'is_government', 'is_online']
#
#    default_sort = [('id', True)]
#    base_permissions = ['can_list', 'can_show', 'can_edit', 'can_delete', 'can_add']
#    label_columns=   [{column.name: column.name for column in table.columns} ]
#    show_template =  'appbuilder/general/model/show_cascade.html'
#    list_template = 'appbuilder/general/model/list.html'
#    add_template = 'appbuilder/general/model/add.html'
#    edit_template = 'appbuilder/general/model/edit.html'
#    add_widget = (FormVerticalWidget|FormInlineWidget)
#    show_widget = ShowBlockWidget
#    list_widget = (ListThumbnail|ListWidget)
#    base_order = ('name', 'asc')
#    list_widget= 'list_widget'


class IndustryDetailView(ModelView):
    datamodel=SQLAInterface(Industry, db.session)
    related_views = []
    show_title='Industry Detail'
    add_title ='Add Industry'
    list_title= 'Industry List'
    edit_title = 'Edit Industry'
    show_columns = ['industry', 'job']
#    show_exclude_columns = [] #= ['industry', 'job']
#
#    add_columns = ['industry', 'job']
#    add_exclude_columns = [hide_list] #['industry', 'job']
#
#    edit_columns = ['industry', 'job']
#    edit_exclude_columns =[hide_list] # ['industry', 'job']
#
#    list_columns = ['industry', 'job']
#    list_exclude_columns = [] # ['industry', 'job']
#
#    search_columns = ['industry', 'job']
#    search_exclude_columns= [] # ['industry', 'job']
#
#    default_sort = [('id', True)]
#    base_permissions = ['can_list', 'can_show', 'can_edit', 'can_delete', 'can_add']
#    label_columns=   [{column.name: column.name for column in table.columns} ]
#    show_template =  'appbuilder/general/model/show_cascade.html'
#    list_template = 'appbuilder/general/model/list.html'
#    add_template = 'appbuilder/general/model/add.html'
#    edit_template = 'appbuilder/general/model/edit.html'
#    add_widget = (FormVerticalWidget|FormInlineWidget)
#    show_widget = ShowBlockWidget
#    list_widget = (ListThumbnail|ListWidget)
#    base_order = ('name', 'asc')
#    list_widget= 'list_widget'


class IndustryJobDetailView(ModelView):
    datamodel=SQLAInterface(IndustryJob, db.session)
    related_views = []
    show_title='IndustryJob Detail'
    add_title ='Add IndustryJob'
    list_title= 'IndustryJob List'
    edit_title = 'Edit IndustryJob'
    show_columns = ['industry', 'job']
#    show_exclude_columns = [] #= ['industry', 'job']
#
#    add_columns = ['industry', 'job']
#    add_exclude_columns = [hide_list] #['industry', 'job']
#
#    edit_columns = ['industry', 'job']
#    edit_exclude_columns =[hide_list] # ['industry', 'job']
#
#    list_columns = ['industry', 'job']
#    list_exclude_columns = [] # ['industry', 'job']
#
#    search_columns = ['industry', 'job']
#    search_exclude_columns= [] # ['industry', 'job']
#
#    default_sort = [('id', True)]
#    base_permissions = ['can_list', 'can_show', 'can_edit', 'can_delete', 'can_add']
#    label_columns=   [{column.name: column.name for column in table.columns} ]
#    show_template =  'appbuilder/general/model/show_cascade.html'
#    list_template = 'appbuilder/general/model/list.html'
#    add_template = 'appbuilder/general/model/add.html'
#    edit_template = 'appbuilder/general/model/edit.html'
#    add_widget = (FormVerticalWidget|FormInlineWidget)
#    show_widget = ShowBlockWidget
#    list_widget = (ListThumbnail|ListWidget)
#    base_order = ('name', 'asc')
#    list_widget= 'list_widget'


class JobDetailView(ModelView):
    datamodel=SQLAInterface(Job, db.session)
    related_views = []
    show_title='Job Detail'
    add_title ='Add Job'
    list_title= 'Job List'
    edit_title = 'Edit Job'
    show_columns = ['industry', 'job']
#    show_exclude_columns = [] #= ['industry', 'job']
#
#    add_columns = ['industry', 'job']
#    add_exclude_columns = [hide_list] #['industry', 'job']
#
#    edit_columns = ['industry', 'job']
#    edit_exclude_columns =[hide_list] # ['industry', 'job']
#
#    list_columns = ['industry', 'job']
#    list_exclude_columns = [] # ['industry', 'job']
#
#    search_columns = ['industry', 'job']
#    search_exclude_columns= [] # ['industry', 'job']
#
#    default_sort = [('id', True)]
#    base_permissions = ['can_list', 'can_show', 'can_edit', 'can_delete', 'can_add']
#    label_columns=   [{column.name: column.name for column in table.columns} ]
#    show_template =  'appbuilder/general/model/show_cascade.html'
#    list_template = 'appbuilder/general/model/list.html'
#    add_template = 'appbuilder/general/model/add.html'
#    edit_template = 'appbuilder/general/model/edit.html'
#    add_widget = (FormVerticalWidget|FormInlineWidget)
#    show_widget = ShowBlockWidget
#    list_widget = (ListThumbnail|ListWidget)
#    base_order = ('name', 'asc')
#    list_widget= 'list_widget'




class SkillDetailView(ModelView):
    datamodel=SQLAInterface(Skill, db.session)
    related_views = []
    show_title='Skill Detail'
    add_title ='Add Skill'
    list_title= 'Skill List'
    edit_title = 'Edit Skill'
    show_columns = ['skills', 'jobs']
#    show_exclude_columns = [] #= ['skills', 'jobs']
#
#    add_columns = ['skills', 'jobs']
#    add_exclude_columns = [hide_list] #['skills', 'jobs']
#
#    edit_columns = ['skills', 'jobs']
#    edit_exclude_columns =[hide_list] # ['skills', 'jobs']
#
#    list_columns = ['skills', 'jobs']
#    list_exclude_columns = [] # ['skills', 'jobs']
#
#    search_columns = ['skills', 'jobs']
#    search_exclude_columns= [] # ['skills', 'jobs']
#
#    default_sort = [('id', True)]
#    base_permissions = ['can_list', 'can_show', 'can_edit', 'can_delete', 'can_add']
#    label_columns=   [{column.name: column.name for column in table.columns} ]
#    show_template =  'appbuilder/general/model/show_cascade.html'
#    list_template = 'appbuilder/general/model/list.html'
#    add_template = 'appbuilder/general/model/add.html'
#    edit_template = 'appbuilder/general/model/edit.html'
#    add_widget = (FormVerticalWidget|FormInlineWidget)
#    show_widget = ShowBlockWidget
#    list_widget = (ListThumbnail|ListWidget)
#    base_order = ('name', 'asc')
#    list_widget= 'list_widget'


class JobSkillDetailView(ModelView):
    datamodel=SQLAInterface(JobSkill, db.session)
    related_views = []
    show_title='JobSkill Detail'
    add_title ='Add JobSkill'
    list_title= 'JobSkill List'
    edit_title = 'Edit JobSkill'
    show_columns = ['skills', 'jobs']
#    show_exclude_columns = [] #= ['skills', 'jobs']
#
#    add_columns = ['skills', 'jobs']
#    add_exclude_columns = [hide_list] #['skills', 'jobs']
#
#    edit_columns = ['skills', 'jobs']
#    edit_exclude_columns =[hide_list] # ['skills', 'jobs']
#
#    list_columns = ['skills', 'jobs']
#    list_exclude_columns = [] # ['skills', 'jobs']
#
#    search_columns = ['skills', 'jobs']
#    search_exclude_columns= [] # ['skills', 'jobs']
#
#    default_sort = [('id', True)]
#    base_permissions = ['can_list', 'can_show', 'can_edit', 'can_delete', 'can_add']
#    label_columns=   [{column.name: column.name for column in table.columns} ]
#    show_template =  'appbuilder/general/model/show_cascade.html'
#    list_template = 'appbuilder/general/model/list.html'
#    add_template = 'appbuilder/general/model/add.html'
#    edit_template = 'appbuilder/general/model/edit.html'
#    add_widget = (FormVerticalWidget|FormInlineWidget)
#    show_widget = ShowBlockWidget
#    list_widget = (ListThumbnail|ListWidget)
#    base_order = ('name', 'asc')
#    list_widget= 'list_widget'


class PortalDetailView(ModelView):
    datamodel=SQLAInterface(Portal, db.session)
    related_views = []
    show_title='Portal Detail'
    add_title ='Add Portal'
    list_title= 'Portal List'
    edit_title = 'Edit Portal'
    show_columns = ['id', 'portal', 'header', 'slug', 'page_type']
#    show_exclude_columns = [] #= ['id', 'portal', 'header', 'slug', 'page_type']
#
#    add_columns = ['id', 'portal', 'header', 'slug', 'page_type']
#    add_exclude_columns = [hide_list] #['id', 'portal', 'header', 'slug', 'page_type']
#
#    edit_columns = ['id', 'portal', 'header', 'slug', 'page_type']
#    edit_exclude_columns =[hide_list] # ['id', 'portal', 'header', 'slug', 'page_type']
#
#    list_columns = ['id', 'portal', 'header', 'slug', 'page_type']
#    list_exclude_columns = [] # ['id', 'portal', 'header', 'slug', 'page_type']
#
#    search_columns = ['id', 'portal', 'header', 'slug', 'page_type']
#    search_exclude_columns= [] # ['id', 'portal', 'header', 'slug', 'page_type']
#
#    default_sort = [('id', True)]
#    base_permissions = ['can_list', 'can_show', 'can_edit', 'can_delete', 'can_add']
#    label_columns=   [{column.name: column.name for column in table.columns} ]
#    show_template =  'appbuilder/general/model/show_cascade.html'
#    list_template = 'appbuilder/general/model/list.html'
#    add_template = 'appbuilder/general/model/add.html'
#    edit_template = 'appbuilder/general/model/edit.html'
#    add_widget = (FormVerticalWidget|FormInlineWidget)
#    show_widget = ShowBlockWidget
#    list_widget = (ListThumbnail|ListWidget)
#    base_order = ('name', 'asc')
#    list_widget= 'list_widget'


class PageDetailView(ModelView):
    datamodel=SQLAInterface(Page, db.session)
    related_views = []
    show_title='Page Detail'
    add_title ='Add Page'
    list_title= 'Page List'
    edit_title = 'Edit Page'
    show_columns = ['id', 'portal', 'header', 'slug', 'page_type']
#    show_exclude_columns = [] #= ['id', 'portal', 'header', 'slug', 'page_type']
#
#    add_columns = ['id', 'portal', 'header', 'slug', 'page_type']
#    add_exclude_columns = [hide_list] #['id', 'portal', 'header', 'slug', 'page_type']
#
#    edit_columns = ['id', 'portal', 'header', 'slug', 'page_type']
#    edit_exclude_columns =[hide_list] # ['id', 'portal', 'header', 'slug', 'page_type']
#
#    list_columns = ['id', 'portal', 'header', 'slug', 'page_type']
#    list_exclude_columns = [] # ['id', 'portal', 'header', 'slug', 'page_type']
#
#    search_columns = ['id', 'portal', 'header', 'slug', 'page_type']
#    search_exclude_columns= [] # ['id', 'portal', 'header', 'slug', 'page_type']
#
#    default_sort = [('id', True)]
#    base_permissions = ['can_list', 'can_show', 'can_edit', 'can_delete', 'can_add']
#    label_columns=   [{column.name: column.name for column in table.columns} ]
#    show_template =  'appbuilder/general/model/show_cascade.html'
#    list_template = 'appbuilder/general/model/list.html'
#    add_template = 'appbuilder/general/model/add.html'
#    edit_template = 'appbuilder/general/model/edit.html'
#    add_widget = (FormVerticalWidget|FormInlineWidget)
#    show_widget = ShowBlockWidget
#    list_widget = (ListThumbnail|ListWidget)
#    base_order = ('name', 'asc')
#    list_widget= 'list_widget'


class ProfilesourceDetailView(ModelView):
    datamodel=SQLAInterface(Profilesource, db.session)
    related_views = []
    show_title='Profilesource Detail'
    add_title ='Add Profilesource'
    list_title= 'Profilesource List'
    edit_title = 'Edit Profilesource'
    show_columns = ['id', 'individual', 'import_address', 'profile_username', 'profile_password', 'has_been_imported', 'import_data', 'import_date', 'profilesource']
#    show_exclude_columns = [] #= ['id', 'individual', 'import_address', 'profile_username', 'profile_password', 'has_been_imported', 'import_data', 'import_date', 'profilesource']
#
#    add_columns = ['id', 'individual', 'import_address', 'profile_username', 'profile_password', 'has_been_imported', 'import_data', 'import_date', 'profilesource']
#    add_exclude_columns = [hide_list] #['id', 'individual', 'import_address', 'profile_username', 'profile_password', 'has_been_imported', 'import_data', 'import_date', 'profilesource']
#
#    edit_columns = ['id', 'individual', 'import_address', 'profile_username', 'profile_password', 'has_been_imported', 'import_data', 'import_date', 'profilesource']
#    edit_exclude_columns =[hide_list] # ['id', 'individual', 'import_address', 'profile_username', 'profile_password', 'has_been_imported', 'import_data', 'import_date', 'profilesource']
#
#    list_columns = ['id', 'individual', 'import_address', 'profile_username', 'profile_password', 'has_been_imported', 'import_data', 'import_date', 'profilesource']
#    list_exclude_columns = [] # ['id', 'individual', 'import_address', 'profile_username', 'profile_password', 'has_been_imported', 'import_data', 'import_date', 'profilesource']
#
#    search_columns = ['id', 'individual', 'import_address', 'profile_username', 'profile_password', 'has_been_imported', 'import_data', 'import_date', 'profilesource']
#    search_exclude_columns= [] # ['id', 'individual', 'import_address', 'profile_username', 'profile_password', 'has_been_imported', 'import_data', 'import_date', 'profilesource']
#
#    default_sort = [('id', True)]
#    base_permissions = ['can_list', 'can_show', 'can_edit', 'can_delete', 'can_add']
#    label_columns=   [{column.name: column.name for column in table.columns} ]
#    show_template =  'appbuilder/general/model/show_cascade.html'
#    list_template = 'appbuilder/general/model/list.html'
#    add_template = 'appbuilder/general/model/add.html'
#    edit_template = 'appbuilder/general/model/edit.html'
#    add_widget = (FormVerticalWidget|FormInlineWidget)
#    show_widget = ShowBlockWidget
#    list_widget = (ListThumbnail|ListWidget)
#    base_order = ('name', 'asc')
#    list_widget= 'list_widget'


class ProfileDetailView(ModelView):
    datamodel=SQLAInterface(Profile, db.session)
    related_views = []
    show_title='Profile Detail'
    add_title ='Add Profile'
    list_title= 'Profile List'
    edit_title = 'Edit Profile'
    show_columns = ['id', 'individual', 'import_address', 'profile_username', 'profile_password', 'has_been_imported', 'import_data', 'import_date', 'profilesource']
#    show_exclude_columns = [] #= ['id', 'individual', 'import_address', 'profile_username', 'profile_password', 'has_been_imported', 'import_data', 'import_date', 'profilesource']
#
#    add_columns = ['id', 'individual', 'import_address', 'profile_username', 'profile_password', 'has_been_imported', 'import_data', 'import_date', 'profilesource']
#    add_exclude_columns = [hide_list] #['id', 'individual', 'import_address', 'profile_username', 'profile_password', 'has_been_imported', 'import_data', 'import_date', 'profilesource']
#
#    edit_columns = ['id', 'individual', 'import_address', 'profile_username', 'profile_password', 'has_been_imported', 'import_data', 'import_date', 'profilesource']
#    edit_exclude_columns =[hide_list] # ['id', 'individual', 'import_address', 'profile_username', 'profile_password', 'has_been_imported', 'import_data', 'import_date', 'profilesource']
#
#    list_columns = ['id', 'individual', 'import_address', 'profile_username', 'profile_password', 'has_been_imported', 'import_data', 'import_date', 'profilesource']
#    list_exclude_columns = [] # ['id', 'individual', 'import_address', 'profile_username', 'profile_password', 'has_been_imported', 'import_data', 'import_date', 'profilesource']
#
#    search_columns = ['id', 'individual', 'import_address', 'profile_username', 'profile_password', 'has_been_imported', 'import_data', 'import_date', 'profilesource']
#    search_exclude_columns= [] # ['id', 'individual', 'import_address', 'profile_username', 'profile_password', 'has_been_imported', 'import_data', 'import_date', 'profilesource']
#
#    default_sort = [('id', True)]
#    base_permissions = ['can_list', 'can_show', 'can_edit', 'can_delete', 'can_add']
#    label_columns=   [{column.name: column.name for column in table.columns} ]
#    show_template =  'appbuilder/general/model/show_cascade.html'
#    list_template = 'appbuilder/general/model/list.html'
#    add_template = 'appbuilder/general/model/add.html'
#    edit_template = 'appbuilder/general/model/edit.html'
#    add_widget = (FormVerticalWidget|FormInlineWidget)
#    show_widget = ShowBlockWidget
#    list_widget = (ListThumbnail|ListWidget)
#    base_order = ('name', 'asc')
#    list_widget= 'list_widget'


class IndividualMasterView(MasterDetailView):
    datamodel=SQLAInterface(Individual, db.session)
    related_views = [UserxDetailView]
    show_title='Individual Detail'
    add_title ='Add Individual'
    list_title= 'Individual List'
    edit_title = 'Edit Individual'
    show_columns = ['id', 'userx', 'is_individual', 'is_institution', 'is_company', 'is_government', 'is_online']
#    show_exclude_columns = [] #= ['id', 'userx', 'is_individual', 'is_institution', 'is_company', 'is_government', 'is_online']
#
#    add_columns = ['id', 'userx', 'is_individual', 'is_institution', 'is_company', 'is_government', 'is_online']
#    add_exclude_columns = [hide_list] #['id', 'userx', 'is_individual', 'is_institution', 'is_company', 'is_government', 'is_online']
#
#    edit_columns = ['id', 'userx', 'is_individual', 'is_institution', 'is_company', 'is_government', 'is_online']
#    edit_exclude_columns =[hide_list] # ['id', 'userx', 'is_individual', 'is_institution', 'is_company', 'is_government', 'is_online']
#
#    list_columns = ['id', 'userx', 'is_individual', 'is_institution', 'is_company', 'is_government', 'is_online']
#    list_exclude_columns = [] # ['id', 'userx', 'is_individual', 'is_institution', 'is_company', 'is_government', 'is_online']
#
#    search_columns = ['id', 'userx', 'is_individual', 'is_institution', 'is_company', 'is_government', 'is_online']
#    search_exclude_columns= [] # ['id', 'userx', 'is_individual', 'is_institution', 'is_company', 'is_government', 'is_online']
#
#    default_sort = [('id', True)]
#    base_permissions = ['can_list', 'can_show', 'can_edit', 'can_delete', 'can_add']
#    label_columns=   [{column.name: column.name for column in table.columns} ]
#    show_template =  'appbuilder/general/model/show_cascade.html'
#    list_template = 'appbuilder/general/model/list.html'
#    add_template = 'appbuilder/general/model/add.html'
#    edit_template = 'appbuilder/general/model/edit.html'
#    add_widget = (FormVerticalWidget|FormInlineWidget)
#    show_widget = ShowBlockWidget
#    list_widget = (ListThumbnail|ListWidget)
#    base_order = ('name', 'asc')
#    list_widget= 'list_widget'


class IndustryJobMasterView(MasterDetailView):
    datamodel=SQLAInterface(IndustryJob, db.session)
    related_views = [IndustryDetailView]
    show_title='IndustryJob Detail'
    add_title ='Add IndustryJob'
    list_title= 'IndustryJob List'
    edit_title = 'Edit IndustryJob'
    show_columns = ['industry', 'job']
#    show_exclude_columns = [] #= ['industry', 'job']
#
#    add_columns = ['industry', 'job']
#    add_exclude_columns = [hide_list] #['industry', 'job']
#
#    edit_columns = ['industry', 'job']
#    edit_exclude_columns =[hide_list] # ['industry', 'job']
#
#    list_columns = ['industry', 'job']
#    list_exclude_columns = [] # ['industry', 'job']
#
#    search_columns = ['industry', 'job']
#    search_exclude_columns= [] # ['industry', 'job']
#
#    default_sort = [('id', True)]
#    base_permissions = ['can_list', 'can_show', 'can_edit', 'can_delete', 'can_add']
#    label_columns=   [{column.name: column.name for column in table.columns} ]
#    show_template =  'appbuilder/general/model/show_cascade.html'
#    list_template = 'appbuilder/general/model/list.html'
#    add_template = 'appbuilder/general/model/add.html'
#    edit_template = 'appbuilder/general/model/edit.html'
#    add_widget = (FormVerticalWidget|FormInlineWidget)
#    show_widget = ShowBlockWidget
#    list_widget = (ListThumbnail|ListWidget)
#    base_order = ('name', 'asc')
#    list_widget= 'list_widget'


class IndustryJobMultiView(MultipleView):
    datamodel=SQLAInterface(IndustryJob, db.session)
    views = [IndustryDetailView, JobDetailView]
    show_title='IndustryJob Detail'
    add_title ='Add IndustryJob'
    list_title= 'IndustryJob List'
    edit_title = 'Edit IndustryJob'
    show_columns = ['industry', 'job']
#    show_exclude_columns = [] #= ['industry', 'job']
#
#    add_columns = ['industry', 'job']
#    add_exclude_columns = [hide_list] #['industry', 'job']
#
#    edit_columns = ['industry', 'job']
#    edit_exclude_columns =[hide_list] # ['industry', 'job']
#
#    list_columns = ['industry', 'job']
#    list_exclude_columns = [] # ['industry', 'job']
#
#    search_columns = ['industry', 'job']
#    search_exclude_columns= [] # ['industry', 'job']
#
#    default_sort = [('id', True)]
#    base_permissions = ['can_list', 'can_show', 'can_edit', 'can_delete', 'can_add']
#    label_columns=   [{column.name: column.name for column in table.columns} ]
#    show_template =  'appbuilder/general/model/show_cascade.html'
#    list_template = 'appbuilder/general/model/list.html'
#    add_template = 'appbuilder/general/model/add.html'
#    edit_template = 'appbuilder/general/model/edit.html'
#    add_widget = (FormVerticalWidget|FormInlineWidget)
#    show_widget = ShowBlockWidget
#    list_widget = (ListThumbnail|ListWidget)
#    base_order = ('name', 'asc')
#    list_widget= 'list_widget'


class JobSkillMasterView(MasterDetailView):
    datamodel=SQLAInterface(JobSkill, db.session)
    related_views = [JobDetailView]
    show_title='JobSkill Detail'
    add_title ='Add JobSkill'
    list_title= 'JobSkill List'
    edit_title = 'Edit JobSkill'
    show_columns = ['skills', 'jobs']
#    show_exclude_columns = [] #= ['skills', 'jobs']
#
#    add_columns = ['skills', 'jobs']
#    add_exclude_columns = [hide_list] #['skills', 'jobs']
#
#    edit_columns = ['skills', 'jobs']
#    edit_exclude_columns =[hide_list] # ['skills', 'jobs']
#
#    list_columns = ['skills', 'jobs']
#    list_exclude_columns = [] # ['skills', 'jobs']
#
#    search_columns = ['skills', 'jobs']
#    search_exclude_columns= [] # ['skills', 'jobs']
#
#    default_sort = [('id', True)]
#    base_permissions = ['can_list', 'can_show', 'can_edit', 'can_delete', 'can_add']
#    label_columns=   [{column.name: column.name for column in table.columns} ]
#    show_template =  'appbuilder/general/model/show_cascade.html'
#    list_template = 'appbuilder/general/model/list.html'
#    add_template = 'appbuilder/general/model/add.html'
#    edit_template = 'appbuilder/general/model/edit.html'
#    add_widget = (FormVerticalWidget|FormInlineWidget)
#    show_widget = ShowBlockWidget
#    list_widget = (ListThumbnail|ListWidget)
#    base_order = ('name', 'asc')
#    list_widget= 'list_widget'


class JobSkillMultiView(MultipleView):
    datamodel=SQLAInterface(JobSkill, db.session)
    views = [SkillDetailView]
    show_title='JobSkill Detail'
    add_title ='Add JobSkill'
    list_title= 'JobSkill List'
    edit_title = 'Edit JobSkill'
    show_columns = ['skills', 'jobs']
#    show_exclude_columns = [] #= ['skills', 'jobs']
#
#    add_columns = ['skills', 'jobs']
#    add_exclude_columns = [hide_list] #['skills', 'jobs']
#
#    edit_columns = ['skills', 'jobs']
#    edit_exclude_columns =[hide_list] # ['skills', 'jobs']
#
#    list_columns = ['skills', 'jobs']
#    list_exclude_columns = [] # ['skills', 'jobs']
#
#    search_columns = ['skills', 'jobs']
#    search_exclude_columns= [] # ['skills', 'jobs']
#
#    default_sort = [('id', True)]
#    base_permissions = ['can_list', 'can_show', 'can_edit', 'can_delete', 'can_add']
#    label_columns=   [{column.name: column.name for column in table.columns} ]
#    show_template =  'appbuilder/general/model/show_cascade.html'
#    list_template = 'appbuilder/general/model/list.html'
#    add_template = 'appbuilder/general/model/add.html'
#    edit_template = 'appbuilder/general/model/edit.html'
#    add_widget = (FormVerticalWidget|FormInlineWidget)
#    show_widget = ShowBlockWidget
#    list_widget = (ListThumbnail|ListWidget)
#    base_order = ('name', 'asc')
#    list_widget= 'list_widget'


class EducationMasterView(MasterDetailView):
    datamodel=SQLAInterface(Education, db.session)
    related_views = [IndividualDetailView]
    show_title='Education Detail'
    add_title ='Add Education'
    list_title= 'Education List'
    edit_title = 'Edit Education'
    show_columns = ['id', 'individual', 'qualification', 'qual_class', 'verified', 'verification_code', 'verified_by', 'verification_date', 'verification_doc']
#    show_exclude_columns = [] #= ['id', 'individual', 'qualification', 'qual_class', 'verified', 'verification_code', 'verified_by', 'verification_date', 'verification_doc']
#
#    add_columns = ['id', 'individual', 'qualification', 'qual_class', 'verified', 'verification_code', 'verified_by', 'verification_date', 'verification_doc']
#    add_exclude_columns = [hide_list] #['id', 'individual', 'qualification', 'qual_class', 'verified', 'verification_code', 'verified_by', 'verification_date', 'verification_doc']
#
#    edit_columns = ['id', 'individual', 'qualification', 'qual_class', 'verified', 'verification_code', 'verified_by', 'verification_date', 'verification_doc']
#    edit_exclude_columns =[hide_list] # ['id', 'individual', 'qualification', 'qual_class', 'verified', 'verification_code', 'verified_by', 'verification_date', 'verification_doc']
#
#    list_columns = ['id', 'individual', 'qualification', 'qual_class', 'verified', 'verification_code', 'verified_by', 'verification_date', 'verification_doc']
#    list_exclude_columns = [] # ['id', 'individual', 'qualification', 'qual_class', 'verified', 'verification_code', 'verified_by', 'verification_date', 'verification_doc']
#
#    search_columns = ['id', 'individual', 'qualification', 'qual_class', 'verified', 'verification_code', 'verified_by', 'verification_date', 'verification_doc']
#    search_exclude_columns= [] # ['id', 'individual', 'qualification', 'qual_class', 'verified', 'verification_code', 'verified_by', 'verification_date', 'verification_doc']
#
#    default_sort = [('id', True)]
#    base_permissions = ['can_list', 'can_show', 'can_edit', 'can_delete', 'can_add']
#    label_columns=   [{column.name: column.name for column in table.columns} ]
#    show_template =  'appbuilder/general/model/show_cascade.html'
#    list_template = 'appbuilder/general/model/list.html'
#    add_template = 'appbuilder/general/model/add.html'
#    edit_template = 'appbuilder/general/model/edit.html'
#    add_widget = (FormVerticalWidget|FormInlineWidget)
#    show_widget = ShowBlockWidget
#    list_widget = (ListThumbnail|ListWidget)
#    base_order = ('name', 'asc')
#    list_widget= 'list_widget'


class IndividualJobMasterView(MasterDetailView):
    datamodel=SQLAInterface(IndividualJob, db.session)
    related_views = [IndividualDetailView]
    show_title='IndividualJob Detail'
    add_title ='Add IndividualJob'
    list_title= 'IndividualJob List'
    edit_title = 'Edit IndividualJob'
    show_columns = ['individual', 'job']
#    show_exclude_columns = [] #= ['individual', 'job']
#
#    add_columns = ['individual', 'job']
#    add_exclude_columns = [hide_list] #['individual', 'job']
#
#    edit_columns = ['individual', 'job']
#    edit_exclude_columns =[hide_list] # ['individual', 'job']
#
#    list_columns = ['individual', 'job']
#    list_exclude_columns = [] # ['individual', 'job']
#
#    search_columns = ['individual', 'job']
#    search_exclude_columns= [] # ['individual', 'job']
#
#    default_sort = [('id', True)]
#    base_permissions = ['can_list', 'can_show', 'can_edit', 'can_delete', 'can_add']
#    label_columns=   [{column.name: column.name for column in table.columns} ]
#    show_template =  'appbuilder/general/model/show_cascade.html'
#    list_template = 'appbuilder/general/model/list.html'
#    add_template = 'appbuilder/general/model/add.html'
#    edit_template = 'appbuilder/general/model/edit.html'
#    add_widget = (FormVerticalWidget|FormInlineWidget)
#    show_widget = ShowBlockWidget
#    list_widget = (ListThumbnail|ListWidget)
#    base_order = ('name', 'asc')
#    list_widget= 'list_widget'


class IndividualJobMultiView(MultipleView):
    datamodel=SQLAInterface(IndividualJob, db.session)
    views = []
    show_title='IndividualJob Detail'
    add_title ='Add IndividualJob'
    list_title= 'IndividualJob List'
    edit_title = 'Edit IndividualJob'
    show_columns = ['individual', 'job']
#    show_exclude_columns = [] #= ['individual', 'job']
#
#    add_columns = ['individual', 'job']
#    add_exclude_columns = [hide_list] #['individual', 'job']
#
#    edit_columns = ['individual', 'job']
#    edit_exclude_columns =[hide_list] # ['individual', 'job']
#
#    list_columns = ['individual', 'job']
#    list_exclude_columns = [] # ['individual', 'job']
#
#    search_columns = ['individual', 'job']
#    search_exclude_columns= [] # ['individual', 'job']
#
#    default_sort = [('id', True)]
#    base_permissions = ['can_list', 'can_show', 'can_edit', 'can_delete', 'can_add']
#    label_columns=   [{column.name: column.name for column in table.columns} ]
#    show_template =  'appbuilder/general/model/show_cascade.html'
#    list_template = 'appbuilder/general/model/list.html'
#    add_template = 'appbuilder/general/model/add.html'
#    edit_template = 'appbuilder/general/model/edit.html'
#    add_widget = (FormVerticalWidget|FormInlineWidget)
#    show_widget = ShowBlockWidget
#    list_widget = (ListThumbnail|ListWidget)
#    base_order = ('name', 'asc')
#    list_widget= 'list_widget'


class LocationMasterView(MasterDetailView):
    datamodel=SQLAInterface(Location, db.session)
    related_views = [IndividualDetailView]
    show_title='Location Detail'
    add_title ='Add Location'
    list_title= 'Location List'
    edit_title = 'Edit Location'
    show_columns = ['id', 'individual']
#    show_exclude_columns = [] #= ['id', 'individual']
#
#    add_columns = ['id', 'individual']
#    add_exclude_columns = [hide_list] #['id', 'individual']
#
#    edit_columns = ['id', 'individual']
#    edit_exclude_columns =[hide_list] # ['id', 'individual']
#
#    list_columns = ['id', 'individual']
#    list_exclude_columns = [] # ['id', 'individual']
#
#    search_columns = ['id', 'individual']
#    search_exclude_columns= [] # ['id', 'individual']
#
#    default_sort = [('id', True)]
#    base_permissions = ['can_list', 'can_show', 'can_edit', 'can_delete', 'can_add']
#    label_columns=   [{column.name: column.name for column in table.columns} ]
#    show_template =  'appbuilder/general/model/show_cascade.html'
#    list_template = 'appbuilder/general/model/list.html'
#    add_template = 'appbuilder/general/model/add.html'
#    edit_template = 'appbuilder/general/model/edit.html'
#    add_widget = (FormVerticalWidget|FormInlineWidget)
#    show_widget = ShowBlockWidget
#    list_widget = (ListThumbnail|ListWidget)
#    base_order = ('name', 'asc')
#    list_widget= 'list_widget'


class PortalMasterView(MasterDetailView):
    datamodel=SQLAInterface(Portal, db.session)
    related_views = [IndividualDetailView]
    show_title='Portal Detail'
    add_title ='Add Portal'
    list_title= 'Portal List'
    edit_title = 'Edit Portal'
    show_columns = ['id', 'portal_url', 'is_primary', 'portal_state', 'individual', 'has_custom_domain', 'domain', 'header_text', 'slug', 'automatic_fulfillment_digital_products', 'default_digital_max_downloads', 'default_digital_url_valid_days', 'default_mail_sender_name', 'default_mail_sender_address', 'fulfillment_auto_approve', 'fulfillment_allow_unpaid', 'reserve_stock_duration_anonymous_user', 'reserve_stock_duration_authenticated_user', 'limit_quantity_per_checkout', 'gift_card_expiry_type', 'gift_card_expiry_period_type', 'gift_card_expiry_period', 'charge_taxes_on_shipping', 'include_taxes_in_prices', 'display_gross_prices', 'language']
#    show_exclude_columns = [] #= ['id', 'portal_url', 'is_primary', 'portal_state', 'individual', 'has_custom_domain', 'domain', 'header_text', 'slug', 'automatic_fulfillment_digital_products', 'default_digital_max_downloads', 'default_digital_url_valid_days', 'default_mail_sender_name', 'default_mail_sender_address', 'fulfillment_auto_approve', 'fulfillment_allow_unpaid', 'reserve_stock_duration_anonymous_user', 'reserve_stock_duration_authenticated_user', 'limit_quantity_per_checkout', 'gift_card_expiry_type', 'gift_card_expiry_period_type', 'gift_card_expiry_period', 'charge_taxes_on_shipping', 'include_taxes_in_prices', 'display_gross_prices', 'language']
#
#    add_columns = ['id', 'portal_url', 'is_primary', 'portal_state', 'individual', 'has_custom_domain', 'domain', 'header_text', 'slug', 'automatic_fulfillment_digital_products', 'default_digital_max_downloads', 'default_digital_url_valid_days', 'default_mail_sender_name', 'default_mail_sender_address', 'fulfillment_auto_approve', 'fulfillment_allow_unpaid', 'reserve_stock_duration_anonymous_user', 'reserve_stock_duration_authenticated_user', 'limit_quantity_per_checkout', 'gift_card_expiry_type', 'gift_card_expiry_period_type', 'gift_card_expiry_period', 'charge_taxes_on_shipping', 'include_taxes_in_prices', 'display_gross_prices', 'language']
#    add_exclude_columns = [hide_list] #['id', 'portal_url', 'is_primary', 'portal_state', 'individual', 'has_custom_domain', 'domain', 'header_text', 'slug', 'automatic_fulfillment_digital_products', 'default_digital_max_downloads', 'default_digital_url_valid_days', 'default_mail_sender_name', 'default_mail_sender_address', 'fulfillment_auto_approve', 'fulfillment_allow_unpaid', 'reserve_stock_duration_anonymous_user', 'reserve_stock_duration_authenticated_user', 'limit_quantity_per_checkout', 'gift_card_expiry_type', 'gift_card_expiry_period_type', 'gift_card_expiry_period', 'charge_taxes_on_shipping', 'include_taxes_in_prices', 'display_gross_prices', 'language']
#
#    edit_columns = ['id', 'portal_url', 'is_primary', 'portal_state', 'individual', 'has_custom_domain', 'domain', 'header_text', 'slug', 'automatic_fulfillment_digital_products', 'default_digital_max_downloads', 'default_digital_url_valid_days', 'default_mail_sender_name', 'default_mail_sender_address', 'fulfillment_auto_approve', 'fulfillment_allow_unpaid', 'reserve_stock_duration_anonymous_user', 'reserve_stock_duration_authenticated_user', 'limit_quantity_per_checkout', 'gift_card_expiry_type', 'gift_card_expiry_period_type', 'gift_card_expiry_period', 'charge_taxes_on_shipping', 'include_taxes_in_prices', 'display_gross_prices', 'language']
#    edit_exclude_columns =[hide_list] # ['id', 'portal_url', 'is_primary', 'portal_state', 'individual', 'has_custom_domain', 'domain', 'header_text', 'slug', 'automatic_fulfillment_digital_products', 'default_digital_max_downloads', 'default_digital_url_valid_days', 'default_mail_sender_name', 'default_mail_sender_address', 'fulfillment_auto_approve', 'fulfillment_allow_unpaid', 'reserve_stock_duration_anonymous_user', 'reserve_stock_duration_authenticated_user', 'limit_quantity_per_checkout', 'gift_card_expiry_type', 'gift_card_expiry_period_type', 'gift_card_expiry_period', 'charge_taxes_on_shipping', 'include_taxes_in_prices', 'display_gross_prices', 'language']
#
#    list_columns = ['id', 'portal_url', 'is_primary', 'portal_state', 'individual', 'has_custom_domain', 'domain', 'header_text', 'slug', 'automatic_fulfillment_digital_products', 'default_digital_max_downloads', 'default_digital_url_valid_days', 'default_mail_sender_name', 'default_mail_sender_address', 'fulfillment_auto_approve', 'fulfillment_allow_unpaid', 'reserve_stock_duration_anonymous_user', 'reserve_stock_duration_authenticated_user', 'limit_quantity_per_checkout', 'gift_card_expiry_type', 'gift_card_expiry_period_type', 'gift_card_expiry_period', 'charge_taxes_on_shipping', 'include_taxes_in_prices', 'display_gross_prices', 'language']
#    list_exclude_columns = [] # ['id', 'portal_url', 'is_primary', 'portal_state', 'individual', 'has_custom_domain', 'domain', 'header_text', 'slug', 'automatic_fulfillment_digital_products', 'default_digital_max_downloads', 'default_digital_url_valid_days', 'default_mail_sender_name', 'default_mail_sender_address', 'fulfillment_auto_approve', 'fulfillment_allow_unpaid', 'reserve_stock_duration_anonymous_user', 'reserve_stock_duration_authenticated_user', 'limit_quantity_per_checkout', 'gift_card_expiry_type', 'gift_card_expiry_period_type', 'gift_card_expiry_period', 'charge_taxes_on_shipping', 'include_taxes_in_prices', 'display_gross_prices', 'language']
#
#    search_columns = ['id', 'portal_url', 'is_primary', 'portal_state', 'individual', 'has_custom_domain', 'domain', 'header_text', 'slug', 'automatic_fulfillment_digital_products', 'default_digital_max_downloads', 'default_digital_url_valid_days', 'default_mail_sender_name', 'default_mail_sender_address', 'fulfillment_auto_approve', 'fulfillment_allow_unpaid', 'reserve_stock_duration_anonymous_user', 'reserve_stock_duration_authenticated_user', 'limit_quantity_per_checkout', 'gift_card_expiry_type', 'gift_card_expiry_period_type', 'gift_card_expiry_period', 'charge_taxes_on_shipping', 'include_taxes_in_prices', 'display_gross_prices', 'language']
#    search_exclude_columns= [] # ['id', 'portal_url', 'is_primary', 'portal_state', 'individual', 'has_custom_domain', 'domain', 'header_text', 'slug', 'automatic_fulfillment_digital_products', 'default_digital_max_downloads', 'default_digital_url_valid_days', 'default_mail_sender_name', 'default_mail_sender_address', 'fulfillment_auto_approve', 'fulfillment_allow_unpaid', 'reserve_stock_duration_anonymous_user', 'reserve_stock_duration_authenticated_user', 'limit_quantity_per_checkout', 'gift_card_expiry_type', 'gift_card_expiry_period_type', 'gift_card_expiry_period', 'charge_taxes_on_shipping', 'include_taxes_in_prices', 'display_gross_prices', 'language']
#
#    default_sort = [('id', True)]
#    base_permissions = ['can_list', 'can_show', 'can_edit', 'can_delete', 'can_add']
#    label_columns=   [{column.name: column.name for column in table.columns} ]
#    show_template =  'appbuilder/general/model/show_cascade.html'
#    list_template = 'appbuilder/general/model/list.html'
#    add_template = 'appbuilder/general/model/add.html'
#    edit_template = 'appbuilder/general/model/edit.html'
#    add_widget = (FormVerticalWidget|FormInlineWidget)
#    show_widget = ShowBlockWidget
#    list_widget = (ListThumbnail|ListWidget)
#    base_order = ('name', 'asc')
#    list_widget= 'list_widget'


class PageMasterView(MasterDetailView):
    datamodel=SQLAInterface(Page, db.session)
    related_views = [PortalDetailView]
    show_title='Page Detail'
    add_title ='Add Page'
    list_title= 'Page List'
    edit_title = 'Edit Page'
    show_columns = ['id', 'portal', 'header', 'slug', 'page_type']
#    show_exclude_columns = [] #= ['id', 'portal', 'header', 'slug', 'page_type']
#
#    add_columns = ['id', 'portal', 'header', 'slug', 'page_type']
#    add_exclude_columns = [hide_list] #['id', 'portal', 'header', 'slug', 'page_type']
#
#    edit_columns = ['id', 'portal', 'header', 'slug', 'page_type']
#    edit_exclude_columns =[hide_list] # ['id', 'portal', 'header', 'slug', 'page_type']
#
#    list_columns = ['id', 'portal', 'header', 'slug', 'page_type']
#    list_exclude_columns = [] # ['id', 'portal', 'header', 'slug', 'page_type']
#
#    search_columns = ['id', 'portal', 'header', 'slug', 'page_type']
#    search_exclude_columns= [] # ['id', 'portal', 'header', 'slug', 'page_type']
#
#    default_sort = [('id', True)]
#    base_permissions = ['can_list', 'can_show', 'can_edit', 'can_delete', 'can_add']
#    label_columns=   [{column.name: column.name for column in table.columns} ]
#    show_template =  'appbuilder/general/model/show_cascade.html'
#    list_template = 'appbuilder/general/model/list.html'
#    add_template = 'appbuilder/general/model/add.html'
#    edit_template = 'appbuilder/general/model/edit.html'
#    add_widget = (FormVerticalWidget|FormInlineWidget)
#    show_widget = ShowBlockWidget
#    list_widget = (ListThumbnail|ListWidget)
#    base_order = ('name', 'asc')
#    list_widget= 'list_widget'


class ProfileMasterView(MasterDetailView):
    datamodel=SQLAInterface(Profile, db.session)
    related_views = [IndividualDetailView]
    show_title='Profile Detail'
    add_title ='Add Profile'
    list_title= 'Profile List'
    edit_title = 'Edit Profile'
    show_columns = ['id', 'individual', 'import_address', 'profile_username', 'profile_password', 'has_been_imported', 'import_data', 'import_date', 'profilesource']
#    show_exclude_columns = [] #= ['id', 'individual', 'import_address', 'profile_username', 'profile_password', 'has_been_imported', 'import_data', 'import_date', 'profilesource']
#
#    add_columns = ['id', 'individual', 'import_address', 'profile_username', 'profile_password', 'has_been_imported', 'import_data', 'import_date', 'profilesource']
#    add_exclude_columns = [hide_list] #['id', 'individual', 'import_address', 'profile_username', 'profile_password', 'has_been_imported', 'import_data', 'import_date', 'profilesource']
#
#    edit_columns = ['id', 'individual', 'import_address', 'profile_username', 'profile_password', 'has_been_imported', 'import_data', 'import_date', 'profilesource']
#    edit_exclude_columns =[hide_list] # ['id', 'individual', 'import_address', 'profile_username', 'profile_password', 'has_been_imported', 'import_data', 'import_date', 'profilesource']
#
#    list_columns = ['id', 'individual', 'import_address', 'profile_username', 'profile_password', 'has_been_imported', 'import_data', 'import_date', 'profilesource']
#    list_exclude_columns = [] # ['id', 'individual', 'import_address', 'profile_username', 'profile_password', 'has_been_imported', 'import_data', 'import_date', 'profilesource']
#
#    search_columns = ['id', 'individual', 'import_address', 'profile_username', 'profile_password', 'has_been_imported', 'import_data', 'import_date', 'profilesource']
#    search_exclude_columns= [] # ['id', 'individual', 'import_address', 'profile_username', 'profile_password', 'has_been_imported', 'import_data', 'import_date', 'profilesource']
#
#    default_sort = [('id', True)]
#    base_permissions = ['can_list', 'can_show', 'can_edit', 'can_delete', 'can_add']
#    label_columns=   [{column.name: column.name for column in table.columns} ]
#    show_template =  'appbuilder/general/model/show_cascade.html'
#    list_template = 'appbuilder/general/model/list.html'
#    add_template = 'appbuilder/general/model/add.html'
#    edit_template = 'appbuilder/general/model/edit.html'
#    add_widget = (FormVerticalWidget|FormInlineWidget)
#    show_widget = ShowBlockWidget
#    list_widget = (ListThumbnail|ListWidget)
#    base_order = ('name', 'asc')
#    list_widget= 'list_widget'


class ProfileMultiView(MultipleView):
    datamodel=SQLAInterface(Profile, db.session)
    views = [ProfilesourceDetailView]
    show_title='Profile Detail'
    add_title ='Add Profile'
    list_title= 'Profile List'
    edit_title = 'Edit Profile'
    show_columns = ['id', 'individual', 'import_address', 'profile_username', 'profile_password', 'has_been_imported', 'import_data', 'import_date', 'profilesource']
#    show_exclude_columns = [] #= ['id', 'individual', 'import_address', 'profile_username', 'profile_password', 'has_been_imported', 'import_data', 'import_date', 'profilesource']
#
#    add_columns = ['id', 'individual', 'import_address', 'profile_username', 'profile_password', 'has_been_imported', 'import_data', 'import_date', 'profilesource']
#    add_exclude_columns = [hide_list] #['id', 'individual', 'import_address', 'profile_username', 'profile_password', 'has_been_imported', 'import_data', 'import_date', 'profilesource']
#
#    edit_columns = ['id', 'individual', 'import_address', 'profile_username', 'profile_password', 'has_been_imported', 'import_data', 'import_date', 'profilesource']
#    edit_exclude_columns =[hide_list] # ['id', 'individual', 'import_address', 'profile_username', 'profile_password', 'has_been_imported', 'import_data', 'import_date', 'profilesource']
#
#    list_columns = ['id', 'individual', 'import_address', 'profile_username', 'profile_password', 'has_been_imported', 'import_data', 'import_date', 'profilesource']
#    list_exclude_columns = [] # ['id', 'individual', 'import_address', 'profile_username', 'profile_password', 'has_been_imported', 'import_data', 'import_date', 'profilesource']
#
#    search_columns = ['id', 'individual', 'import_address', 'profile_username', 'profile_password', 'has_been_imported', 'import_data', 'import_date', 'profilesource']
#    search_exclude_columns= [] # ['id', 'individual', 'import_address', 'profile_username', 'profile_password', 'has_been_imported', 'import_data', 'import_date', 'profilesource']
#
#    default_sort = [('id', True)]
#    base_permissions = ['can_list', 'can_show', 'can_edit', 'can_delete', 'can_add']
#    label_columns=   [{column.name: column.name for column in table.columns} ]
#    show_template =  'appbuilder/general/model/show_cascade.html'
#    list_template = 'appbuilder/general/model/list.html'
#    add_template = 'appbuilder/general/model/add.html'
#    edit_template = 'appbuilder/general/model/edit.html'
#    add_widget = (FormVerticalWidget|FormInlineWidget)
#    show_widget = ShowBlockWidget
#    list_widget = (ListThumbnail|ListWidget)
#    base_order = ('name', 'asc')
#    list_widget= 'list_widget'


class ResumeView(ModelView):
    datamodel=SQLAInterface(Resume, db.session)
    related_views = []
    show_title='Resume Detail'
    add_title ='Add Resume'
    list_title= 'Resume List'
    edit_title = 'Edit Resume'
    show_columns = ['id', 'individual', 'template', 'header', 'color', 'location', 'summary_text', 'has_been_generated', 'preferred']
#    show_exclude_columns = [] #= ['id', 'individual', 'template', 'header', 'color', 'location', 'summary_text', 'has_been_generated', 'preferred']
#
#    add_columns = ['id', 'individual', 'template', 'header', 'color', 'location', 'summary_text', 'has_been_generated', 'preferred']
#    add_exclude_columns = [hide_list] #['id', 'individual', 'template', 'header', 'color', 'location', 'summary_text', 'has_been_generated', 'preferred']
#
#    edit_columns = ['id', 'individual', 'template', 'header', 'color', 'location', 'summary_text', 'has_been_generated', 'preferred']
#    edit_exclude_columns =[hide_list] # ['id', 'individual', 'template', 'header', 'color', 'location', 'summary_text', 'has_been_generated', 'preferred']
#
#    list_columns = ['id', 'individual', 'template', 'header', 'color', 'location', 'summary_text', 'has_been_generated', 'preferred']
#    list_exclude_columns = [] # ['id', 'individual', 'template', 'header', 'color', 'location', 'summary_text', 'has_been_generated', 'preferred']
#
#    search_columns = ['id', 'individual', 'template', 'header', 'color', 'location', 'summary_text', 'has_been_generated', 'preferred']
#    search_exclude_columns= [] # ['id', 'individual', 'template', 'header', 'color', 'location', 'summary_text', 'has_been_generated', 'preferred']
#
#    default_sort = [('id', True)]
#    base_permissions = ['can_list', 'can_show', 'can_edit', 'can_delete', 'can_add']
#    label_columns=   [{column.name: column.name for column in table.columns} ]
#    show_template =  'appbuilder/general/model/show_cascade.html'
#    list_template = 'appbuilder/general/model/list.html'
#    add_template = 'appbuilder/general/model/add.html'
#    edit_template = 'appbuilder/general/model/edit.html'
#    add_widget = (FormVerticalWidget|FormInlineWidget)
#    show_widget = ShowBlockWidget
#    list_widget = (ListThumbnail|ListWidget)
#    base_order = ('name', 'asc')
#    list_widget= 'list_widget'


class UserxDetailView(ModelView):
    datamodel=SQLAInterface(Userx, db.session)
    related_views = []
    show_title='Userx Detail'
    add_title ='Add Userx'
    list_title= 'Userx List'
    edit_title = 'Edit Userx'
    show_columns = ['id', 'userx', 'is_individual', 'is_institution', 'is_company', 'is_government', 'is_online']
#    show_exclude_columns = [] #= ['id', 'userx', 'is_individual', 'is_institution', 'is_company', 'is_government', 'is_online']
#
#    add_columns = ['id', 'userx', 'is_individual', 'is_institution', 'is_company', 'is_government', 'is_online']
#    add_exclude_columns = [hide_list] #['id', 'userx', 'is_individual', 'is_institution', 'is_company', 'is_government', 'is_online']
#
#    edit_columns = ['id', 'userx', 'is_individual', 'is_institution', 'is_company', 'is_government', 'is_online']
#    edit_exclude_columns =[hide_list] # ['id', 'userx', 'is_individual', 'is_institution', 'is_company', 'is_government', 'is_online']
#
#    list_columns = ['id', 'userx', 'is_individual', 'is_institution', 'is_company', 'is_government', 'is_online']
#    list_exclude_columns = [] # ['id', 'userx', 'is_individual', 'is_institution', 'is_company', 'is_government', 'is_online']
#
#    search_columns = ['id', 'userx', 'is_individual', 'is_institution', 'is_company', 'is_government', 'is_online']
#    search_exclude_columns= [] # ['id', 'userx', 'is_individual', 'is_institution', 'is_company', 'is_government', 'is_online']
#
#    default_sort = [('id', True)]
#    base_permissions = ['can_list', 'can_show', 'can_edit', 'can_delete', 'can_add']
#    label_columns=   [{column.name: column.name for column in table.columns} ]
#    show_template =  'appbuilder/general/model/show_cascade.html'
#    list_template = 'appbuilder/general/model/list.html'
#    add_template = 'appbuilder/general/model/add.html'
#    edit_template = 'appbuilder/general/model/edit.html'
#    add_widget = (FormVerticalWidget|FormInlineWidget)
#    show_widget = ShowBlockWidget
#    list_widget = (ListThumbnail|ListWidget)
#    base_order = ('name', 'asc')
#    list_widget= 'list_widget'


class IndividualDetailView(ModelView):
    datamodel=SQLAInterface(Individual, db.session)
    related_views = []
    show_title='Individual Detail'
    add_title ='Add Individual'
    list_title= 'Individual List'
    edit_title = 'Edit Individual'
    show_columns = ['id', 'userx', 'is_individual', 'is_institution', 'is_company', 'is_government', 'is_online']
#    show_exclude_columns = [] #= ['id', 'userx', 'is_individual', 'is_institution', 'is_company', 'is_government', 'is_online']
#
#    add_columns = ['id', 'userx', 'is_individual', 'is_institution', 'is_company', 'is_government', 'is_online']
#    add_exclude_columns = [hide_list] #['id', 'userx', 'is_individual', 'is_institution', 'is_company', 'is_government', 'is_online']
#
#    edit_columns = ['id', 'userx', 'is_individual', 'is_institution', 'is_company', 'is_government', 'is_online']
#    edit_exclude_columns =[hide_list] # ['id', 'userx', 'is_individual', 'is_institution', 'is_company', 'is_government', 'is_online']
#
#    list_columns = ['id', 'userx', 'is_individual', 'is_institution', 'is_company', 'is_government', 'is_online']
#    list_exclude_columns = [] # ['id', 'userx', 'is_individual', 'is_institution', 'is_company', 'is_government', 'is_online']
#
#    search_columns = ['id', 'userx', 'is_individual', 'is_institution', 'is_company', 'is_government', 'is_online']
#    search_exclude_columns= [] # ['id', 'userx', 'is_individual', 'is_institution', 'is_company', 'is_government', 'is_online']
#
#    default_sort = [('id', True)]
#    base_permissions = ['can_list', 'can_show', 'can_edit', 'can_delete', 'can_add']
#    label_columns=   [{column.name: column.name for column in table.columns} ]
#    show_template =  'appbuilder/general/model/show_cascade.html'
#    list_template = 'appbuilder/general/model/list.html'
#    add_template = 'appbuilder/general/model/add.html'
#    edit_template = 'appbuilder/general/model/edit.html'
#    add_widget = (FormVerticalWidget|FormInlineWidget)
#    show_widget = ShowBlockWidget
#    list_widget = (ListThumbnail|ListWidget)
#    base_order = ('name', 'asc')
#    list_widget= 'list_widget'


class IndustryDetailView(ModelView):
    datamodel=SQLAInterface(Industry, db.session)
    related_views = []
    show_title='Industry Detail'
    add_title ='Add Industry'
    list_title= 'Industry List'
    edit_title = 'Edit Industry'
    show_columns = ['industry', 'job']
#    show_exclude_columns = [] #= ['industry', 'job']
#
#    add_columns = ['industry', 'job']
#    add_exclude_columns = [hide_list] #['industry', 'job']
#
#    edit_columns = ['industry', 'job']
#    edit_exclude_columns =[hide_list] # ['industry', 'job']
#
#    list_columns = ['industry', 'job']
#    list_exclude_columns = [] # ['industry', 'job']
#
#    search_columns = ['industry', 'job']
#    search_exclude_columns= [] # ['industry', 'job']
#
#    default_sort = [('id', True)]
#    base_permissions = ['can_list', 'can_show', 'can_edit', 'can_delete', 'can_add']
#    label_columns=   [{column.name: column.name for column in table.columns} ]
#    show_template =  'appbuilder/general/model/show_cascade.html'
#    list_template = 'appbuilder/general/model/list.html'
#    add_template = 'appbuilder/general/model/add.html'
#    edit_template = 'appbuilder/general/model/edit.html'
#    add_widget = (FormVerticalWidget|FormInlineWidget)
#    show_widget = ShowBlockWidget
#    list_widget = (ListThumbnail|ListWidget)
#    base_order = ('name', 'asc')
#    list_widget= 'list_widget'


class IndustryJobDetailView(ModelView):
    datamodel=SQLAInterface(IndustryJob, db.session)
    related_views = []
    show_title='IndustryJob Detail'
    add_title ='Add IndustryJob'
    list_title= 'IndustryJob List'
    edit_title = 'Edit IndustryJob'
    show_columns = ['industry', 'job']
#    show_exclude_columns = [] #= ['industry', 'job']
#
#    add_columns = ['industry', 'job']
#    add_exclude_columns = [hide_list] #['industry', 'job']
#
#    edit_columns = ['industry', 'job']
#    edit_exclude_columns =[hide_list] # ['industry', 'job']
#
#    list_columns = ['industry', 'job']
#    list_exclude_columns = [] # ['industry', 'job']
#
#    search_columns = ['industry', 'job']
#    search_exclude_columns= [] # ['industry', 'job']
#
#    default_sort = [('id', True)]
#    base_permissions = ['can_list', 'can_show', 'can_edit', 'can_delete', 'can_add']
#    label_columns=   [{column.name: column.name for column in table.columns} ]
#    show_template =  'appbuilder/general/model/show_cascade.html'
#    list_template = 'appbuilder/general/model/list.html'
#    add_template = 'appbuilder/general/model/add.html'
#    edit_template = 'appbuilder/general/model/edit.html'
#    add_widget = (FormVerticalWidget|FormInlineWidget)
#    show_widget = ShowBlockWidget
#    list_widget = (ListThumbnail|ListWidget)
#    base_order = ('name', 'asc')
#    list_widget= 'list_widget'


class JobDetailView(ModelView):
    datamodel=SQLAInterface(Job, db.session)
    related_views = []
    show_title='Job Detail'
    add_title ='Add Job'
    list_title= 'Job List'
    edit_title = 'Edit Job'
    show_columns = ['industry', 'job']
#    show_exclude_columns = [] #= ['industry', 'job']
#
#    add_columns = ['industry', 'job']
#    add_exclude_columns = [hide_list] #['industry', 'job']
#
#    edit_columns = ['industry', 'job']
#    edit_exclude_columns =[hide_list] # ['industry', 'job']
#
#    list_columns = ['industry', 'job']
#    list_exclude_columns = [] # ['industry', 'job']
#
#    search_columns = ['industry', 'job']
#    search_exclude_columns= [] # ['industry', 'job']
#
#    default_sort = [('id', True)]
#    base_permissions = ['can_list', 'can_show', 'can_edit', 'can_delete', 'can_add']
#    label_columns=   [{column.name: column.name for column in table.columns} ]
#    show_template =  'appbuilder/general/model/show_cascade.html'
#    list_template = 'appbuilder/general/model/list.html'
#    add_template = 'appbuilder/general/model/add.html'
#    edit_template = 'appbuilder/general/model/edit.html'
#    add_widget = (FormVerticalWidget|FormInlineWidget)
#    show_widget = ShowBlockWidget
#    list_widget = (ListThumbnail|ListWidget)
#    base_order = ('name', 'asc')
#    list_widget= 'list_widget'




class SkillDetailView(ModelView):
    datamodel=SQLAInterface(Skill, db.session)
    related_views = []
    show_title='Skill Detail'
    add_title ='Add Skill'
    list_title= 'Skill List'
    edit_title = 'Edit Skill'
    show_columns = ['skills', 'jobs']
#    show_exclude_columns = [] #= ['skills', 'jobs']
#
#    add_columns = ['skills', 'jobs']
#    add_exclude_columns = [hide_list] #['skills', 'jobs']
#
#    edit_columns = ['skills', 'jobs']
#    edit_exclude_columns =[hide_list] # ['skills', 'jobs']
#
#    list_columns = ['skills', 'jobs']
#    list_exclude_columns = [] # ['skills', 'jobs']
#
#    search_columns = ['skills', 'jobs']
#    search_exclude_columns= [] # ['skills', 'jobs']
#
#    default_sort = [('id', True)]
#    base_permissions = ['can_list', 'can_show', 'can_edit', 'can_delete', 'can_add']
#    label_columns=   [{column.name: column.name for column in table.columns} ]
#    show_template =  'appbuilder/general/model/show_cascade.html'
#    list_template = 'appbuilder/general/model/list.html'
#    add_template = 'appbuilder/general/model/add.html'
#    edit_template = 'appbuilder/general/model/edit.html'
#    add_widget = (FormVerticalWidget|FormInlineWidget)
#    show_widget = ShowBlockWidget
#    list_widget = (ListThumbnail|ListWidget)
#    base_order = ('name', 'asc')
#    list_widget= 'list_widget'


class JobSkillDetailView(ModelView):
    datamodel=SQLAInterface(JobSkill, db.session)
    related_views = []
    show_title='JobSkill Detail'
    add_title ='Add JobSkill'
    list_title= 'JobSkill List'
    edit_title = 'Edit JobSkill'
    show_columns = ['skills', 'jobs']
#    show_exclude_columns = [] #= ['skills', 'jobs']
#
#    add_columns = ['skills', 'jobs']
#    add_exclude_columns = [hide_list] #['skills', 'jobs']
#
#    edit_columns = ['skills', 'jobs']
#    edit_exclude_columns =[hide_list] # ['skills', 'jobs']
#
#    list_columns = ['skills', 'jobs']
#    list_exclude_columns = [] # ['skills', 'jobs']
#
#    search_columns = ['skills', 'jobs']
#    search_exclude_columns= [] # ['skills', 'jobs']
#
#    default_sort = [('id', True)]
#    base_permissions = ['can_list', 'can_show', 'can_edit', 'can_delete', 'can_add']
#    label_columns=   [{column.name: column.name for column in table.columns} ]
#    show_template =  'appbuilder/general/model/show_cascade.html'
#    list_template = 'appbuilder/general/model/list.html'
#    add_template = 'appbuilder/general/model/add.html'
#    edit_template = 'appbuilder/general/model/edit.html'
#    add_widget = (FormVerticalWidget|FormInlineWidget)
#    show_widget = ShowBlockWidget
#    list_widget = (ListThumbnail|ListWidget)
#    base_order = ('name', 'asc')
#    list_widget= 'list_widget'


class PortalDetailView(ModelView):
    datamodel=SQLAInterface(Portal, db.session)
    related_views = []
    show_title='Portal Detail'
    add_title ='Add Portal'
    list_title= 'Portal List'
    edit_title = 'Edit Portal'
    show_columns = ['id', 'portal', 'header', 'slug', 'page_type']
#    show_exclude_columns = [] #= ['id', 'portal', 'header', 'slug', 'page_type']
#
#    add_columns = ['id', 'portal', 'header', 'slug', 'page_type']
#    add_exclude_columns = [hide_list] #['id', 'portal', 'header', 'slug', 'page_type']
#
#    edit_columns = ['id', 'portal', 'header', 'slug', 'page_type']
#    edit_exclude_columns =[hide_list] # ['id', 'portal', 'header', 'slug', 'page_type']
#
#    list_columns = ['id', 'portal', 'header', 'slug', 'page_type']
#    list_exclude_columns = [] # ['id', 'portal', 'header', 'slug', 'page_type']
#
#    search_columns = ['id', 'portal', 'header', 'slug', 'page_type']
#    search_exclude_columns= [] # ['id', 'portal', 'header', 'slug', 'page_type']
#
#    default_sort = [('id', True)]
#    base_permissions = ['can_list', 'can_show', 'can_edit', 'can_delete', 'can_add']
#    label_columns=   [{column.name: column.name for column in table.columns} ]
#    show_template =  'appbuilder/general/model/show_cascade.html'
#    list_template = 'appbuilder/general/model/list.html'
#    add_template = 'appbuilder/general/model/add.html'
#    edit_template = 'appbuilder/general/model/edit.html'
#    add_widget = (FormVerticalWidget|FormInlineWidget)
#    show_widget = ShowBlockWidget
#    list_widget = (ListThumbnail|ListWidget)
#    base_order = ('name', 'asc')
#    list_widget= 'list_widget'


class PageDetailView(ModelView):
    datamodel=SQLAInterface(Page, db.session)
    related_views = []
    show_title='Page Detail'
    add_title ='Add Page'
    list_title= 'Page List'
    edit_title = 'Edit Page'
    show_columns = ['id', 'portal', 'header', 'slug', 'page_type']
#    show_exclude_columns = [] #= ['id', 'portal', 'header', 'slug', 'page_type']
#
#    add_columns = ['id', 'portal', 'header', 'slug', 'page_type']
#    add_exclude_columns = [hide_list] #['id', 'portal', 'header', 'slug', 'page_type']
#
#    edit_columns = ['id', 'portal', 'header', 'slug', 'page_type']
#    edit_exclude_columns =[hide_list] # ['id', 'portal', 'header', 'slug', 'page_type']
#
#    list_columns = ['id', 'portal', 'header', 'slug', 'page_type']
#    list_exclude_columns = [] # ['id', 'portal', 'header', 'slug', 'page_type']
#
#    search_columns = ['id', 'portal', 'header', 'slug', 'page_type']
#    search_exclude_columns= [] # ['id', 'portal', 'header', 'slug', 'page_type']
#
#    default_sort = [('id', True)]
#    base_permissions = ['can_list', 'can_show', 'can_edit', 'can_delete', 'can_add']
#    label_columns=   [{column.name: column.name for column in table.columns} ]
#    show_template =  'appbuilder/general/model/show_cascade.html'
#    list_template = 'appbuilder/general/model/list.html'
#    add_template = 'appbuilder/general/model/add.html'
#    edit_template = 'appbuilder/general/model/edit.html'
#    add_widget = (FormVerticalWidget|FormInlineWidget)
#    show_widget = ShowBlockWidget
#    list_widget = (ListThumbnail|ListWidget)
#    base_order = ('name', 'asc')
#    list_widget= 'list_widget'


class ProfilesourceDetailView(ModelView):
    datamodel=SQLAInterface(Profilesource, db.session)
    related_views = []
    show_title='Profilesource Detail'
    add_title ='Add Profilesource'
    list_title= 'Profilesource List'
    edit_title = 'Edit Profilesource'
    show_columns = ['id', 'individual', 'import_address', 'profile_username', 'profile_password', 'has_been_imported', 'import_data', 'import_date', 'profilesource']
#    show_exclude_columns = [] #= ['id', 'individual', 'import_address', 'profile_username', 'profile_password', 'has_been_imported', 'import_data', 'import_date', 'profilesource']
#
#    add_columns = ['id', 'individual', 'import_address', 'profile_username', 'profile_password', 'has_been_imported', 'import_data', 'import_date', 'profilesource']
#    add_exclude_columns = [hide_list] #['id', 'individual', 'import_address', 'profile_username', 'profile_password', 'has_been_imported', 'import_data', 'import_date', 'profilesource']
#
#    edit_columns = ['id', 'individual', 'import_address', 'profile_username', 'profile_password', 'has_been_imported', 'import_data', 'import_date', 'profilesource']
#    edit_exclude_columns =[hide_list] # ['id', 'individual', 'import_address', 'profile_username', 'profile_password', 'has_been_imported', 'import_data', 'import_date', 'profilesource']
#
#    list_columns = ['id', 'individual', 'import_address', 'profile_username', 'profile_password', 'has_been_imported', 'import_data', 'import_date', 'profilesource']
#    list_exclude_columns = [] # ['id', 'individual', 'import_address', 'profile_username', 'profile_password', 'has_been_imported', 'import_data', 'import_date', 'profilesource']
#
#    search_columns = ['id', 'individual', 'import_address', 'profile_username', 'profile_password', 'has_been_imported', 'import_data', 'import_date', 'profilesource']
#    search_exclude_columns= [] # ['id', 'individual', 'import_address', 'profile_username', 'profile_password', 'has_been_imported', 'import_data', 'import_date', 'profilesource']
#
#    default_sort = [('id', True)]
#    base_permissions = ['can_list', 'can_show', 'can_edit', 'can_delete', 'can_add']
#    label_columns=   [{column.name: column.name for column in table.columns} ]
#    show_template =  'appbuilder/general/model/show_cascade.html'
#    list_template = 'appbuilder/general/model/list.html'
#    add_template = 'appbuilder/general/model/add.html'
#    edit_template = 'appbuilder/general/model/edit.html'
#    add_widget = (FormVerticalWidget|FormInlineWidget)
#    show_widget = ShowBlockWidget
#    list_widget = (ListThumbnail|ListWidget)
#    base_order = ('name', 'asc')
#    list_widget= 'list_widget'


class ProfileDetailView(ModelView):
    datamodel=SQLAInterface(Profile, db.session)
    related_views = []
    show_title='Profile Detail'
    add_title ='Add Profile'
    list_title= 'Profile List'
    edit_title = 'Edit Profile'
    show_columns = ['id', 'individual', 'import_address', 'profile_username', 'profile_password', 'has_been_imported', 'import_data', 'import_date', 'profilesource']
#    show_exclude_columns = [] #= ['id', 'individual', 'import_address', 'profile_username', 'profile_password', 'has_been_imported', 'import_data', 'import_date', 'profilesource']
#
#    add_columns = ['id', 'individual', 'import_address', 'profile_username', 'profile_password', 'has_been_imported', 'import_data', 'import_date', 'profilesource']
#    add_exclude_columns = [hide_list] #['id', 'individual', 'import_address', 'profile_username', 'profile_password', 'has_been_imported', 'import_data', 'import_date', 'profilesource']
#
#    edit_columns = ['id', 'individual', 'import_address', 'profile_username', 'profile_password', 'has_been_imported', 'import_data', 'import_date', 'profilesource']
#    edit_exclude_columns =[hide_list] # ['id', 'individual', 'import_address', 'profile_username', 'profile_password', 'has_been_imported', 'import_data', 'import_date', 'profilesource']
#
#    list_columns = ['id', 'individual', 'import_address', 'profile_username', 'profile_password', 'has_been_imported', 'import_data', 'import_date', 'profilesource']
#    list_exclude_columns = [] # ['id', 'individual', 'import_address', 'profile_username', 'profile_password', 'has_been_imported', 'import_data', 'import_date', 'profilesource']
#
#    search_columns = ['id', 'individual', 'import_address', 'profile_username', 'profile_password', 'has_been_imported', 'import_data', 'import_date', 'profilesource']
#    search_exclude_columns= [] # ['id', 'individual', 'import_address', 'profile_username', 'profile_password', 'has_been_imported', 'import_data', 'import_date', 'profilesource']
#
#    default_sort = [('id', True)]
#    base_permissions = ['can_list', 'can_show', 'can_edit', 'can_delete', 'can_add']
#    label_columns=   [{column.name: column.name for column in table.columns} ]
#    show_template =  'appbuilder/general/model/show_cascade.html'
#    list_template = 'appbuilder/general/model/list.html'
#    add_template = 'appbuilder/general/model/add.html'
#    edit_template = 'appbuilder/general/model/edit.html'
#    add_widget = (FormVerticalWidget|FormInlineWidget)
#    show_widget = ShowBlockWidget
#    list_widget = (ListThumbnail|ListWidget)
#    base_order = ('name', 'asc')
#    list_widget= 'list_widget'


class LocationDetailView(ModelView):
    datamodel=SQLAInterface(Location, db.session)
    related_views = []
    show_title='Location Detail'
    add_title ='Add Location'
    list_title= 'Location List'
    edit_title = 'Edit Location'
    show_columns = ['id', 'individual', 'template', 'header', 'color', 'location', 'summary_text', 'has_been_generated', 'preferred']
#    show_exclude_columns = [] #= ['id', 'individual', 'template', 'header', 'color', 'location', 'summary_text', 'has_been_generated', 'preferred']
#
#    add_columns = ['id', 'individual', 'template', 'header', 'color', 'location', 'summary_text', 'has_been_generated', 'preferred']
#    add_exclude_columns = [hide_list] #['id', 'individual', 'template', 'header', 'color', 'location', 'summary_text', 'has_been_generated', 'preferred']
#
#    edit_columns = ['id', 'individual', 'template', 'header', 'color', 'location', 'summary_text', 'has_been_generated', 'preferred']
#    edit_exclude_columns =[hide_list] # ['id', 'individual', 'template', 'header', 'color', 'location', 'summary_text', 'has_been_generated', 'preferred']
#
#    list_columns = ['id', 'individual', 'template', 'header', 'color', 'location', 'summary_text', 'has_been_generated', 'preferred']
#    list_exclude_columns = [] # ['id', 'individual', 'template', 'header', 'color', 'location', 'summary_text', 'has_been_generated', 'preferred']
#
#    search_columns = ['id', 'individual', 'template', 'header', 'color', 'location', 'summary_text', 'has_been_generated', 'preferred']
#    search_exclude_columns= [] # ['id', 'individual', 'template', 'header', 'color', 'location', 'summary_text', 'has_been_generated', 'preferred']
#
#    default_sort = [('id', True)]
#    base_permissions = ['can_list', 'can_show', 'can_edit', 'can_delete', 'can_add']
#    label_columns=   [{column.name: column.name for column in table.columns} ]
#    show_template =  'appbuilder/general/model/show_cascade.html'
#    list_template = 'appbuilder/general/model/list.html'
#    add_template = 'appbuilder/general/model/add.html'
#    edit_template = 'appbuilder/general/model/edit.html'
#    add_widget = (FormVerticalWidget|FormInlineWidget)
#    show_widget = ShowBlockWidget
#    list_widget = (ListThumbnail|ListWidget)
#    base_order = ('name', 'asc')
#    list_widget= 'list_widget'


class ResumeDetailView(ModelView):
    datamodel=SQLAInterface(Resume, db.session)
    related_views = []
    show_title='Resume Detail'
    add_title ='Add Resume'
    list_title= 'Resume List'
    edit_title = 'Edit Resume'
    show_columns = ['id', 'individual', 'template', 'header', 'color', 'location', 'summary_text', 'has_been_generated', 'preferred']
#    show_exclude_columns = [] #= ['id', 'individual', 'template', 'header', 'color', 'location', 'summary_text', 'has_been_generated', 'preferred']
#
#    add_columns = ['id', 'individual', 'template', 'header', 'color', 'location', 'summary_text', 'has_been_generated', 'preferred']
#    add_exclude_columns = [hide_list] #['id', 'individual', 'template', 'header', 'color', 'location', 'summary_text', 'has_been_generated', 'preferred']
#
#    edit_columns = ['id', 'individual', 'template', 'header', 'color', 'location', 'summary_text', 'has_been_generated', 'preferred']
#    edit_exclude_columns =[hide_list] # ['id', 'individual', 'template', 'header', 'color', 'location', 'summary_text', 'has_been_generated', 'preferred']
#
#    list_columns = ['id', 'individual', 'template', 'header', 'color', 'location', 'summary_text', 'has_been_generated', 'preferred']
#    list_exclude_columns = [] # ['id', 'individual', 'template', 'header', 'color', 'location', 'summary_text', 'has_been_generated', 'preferred']
#
#    search_columns = ['id', 'individual', 'template', 'header', 'color', 'location', 'summary_text', 'has_been_generated', 'preferred']
#    search_exclude_columns= [] # ['id', 'individual', 'template', 'header', 'color', 'location', 'summary_text', 'has_been_generated', 'preferred']
#
#    default_sort = [('id', True)]
#    base_permissions = ['can_list', 'can_show', 'can_edit', 'can_delete', 'can_add']
#    label_columns=   [{column.name: column.name for column in table.columns} ]
#    show_template =  'appbuilder/general/model/show_cascade.html'
#    list_template = 'appbuilder/general/model/list.html'
#    add_template = 'appbuilder/general/model/add.html'
#    edit_template = 'appbuilder/general/model/edit.html'
#    add_widget = (FormVerticalWidget|FormInlineWidget)
#    show_widget = ShowBlockWidget
#    list_widget = (ListThumbnail|ListWidget)
#    base_order = ('name', 'asc')
#    list_widget= 'list_widget'


class IndividualMasterView(MasterDetailView):
    datamodel=SQLAInterface(Individual, db.session)
    related_views = [UserxDetailView]
    show_title='Individual Detail'
    add_title ='Add Individual'
    list_title= 'Individual List'
    edit_title = 'Edit Individual'
    show_columns = ['id', 'userx', 'is_individual', 'is_institution', 'is_company', 'is_government', 'is_online']
#    show_exclude_columns = [] #= ['id', 'userx', 'is_individual', 'is_institution', 'is_company', 'is_government', 'is_online']
#
#    add_columns = ['id', 'userx', 'is_individual', 'is_institution', 'is_company', 'is_government', 'is_online']
#    add_exclude_columns = [hide_list] #['id', 'userx', 'is_individual', 'is_institution', 'is_company', 'is_government', 'is_online']
#
#    edit_columns = ['id', 'userx', 'is_individual', 'is_institution', 'is_company', 'is_government', 'is_online']
#    edit_exclude_columns =[hide_list] # ['id', 'userx', 'is_individual', 'is_institution', 'is_company', 'is_government', 'is_online']
#
#    list_columns = ['id', 'userx', 'is_individual', 'is_institution', 'is_company', 'is_government', 'is_online']
#    list_exclude_columns = [] # ['id', 'userx', 'is_individual', 'is_institution', 'is_company', 'is_government', 'is_online']
#
#    search_columns = ['id', 'userx', 'is_individual', 'is_institution', 'is_company', 'is_government', 'is_online']
#    search_exclude_columns= [] # ['id', 'userx', 'is_individual', 'is_institution', 'is_company', 'is_government', 'is_online']
#
#    default_sort = [('id', True)]
#    base_permissions = ['can_list', 'can_show', 'can_edit', 'can_delete', 'can_add']
#    label_columns=   [{column.name: column.name for column in table.columns} ]
#    show_template =  'appbuilder/general/model/show_cascade.html'
#    list_template = 'appbuilder/general/model/list.html'
#    add_template = 'appbuilder/general/model/add.html'
#    edit_template = 'appbuilder/general/model/edit.html'
#    add_widget = (FormVerticalWidget|FormInlineWidget)
#    show_widget = ShowBlockWidget
#    list_widget = (ListThumbnail|ListWidget)
#    base_order = ('name', 'asc')
#    list_widget= 'list_widget'


class IndustryJobMasterView(MasterDetailView):
    datamodel=SQLAInterface(IndustryJob, db.session)
    related_views = [IndustryDetailView]
    show_title='IndustryJob Detail'
    add_title ='Add IndustryJob'
    list_title= 'IndustryJob List'
    edit_title = 'Edit IndustryJob'
    show_columns = ['industry', 'job']
#    show_exclude_columns = [] #= ['industry', 'job']
#
#    add_columns = ['industry', 'job']
#    add_exclude_columns = [hide_list] #['industry', 'job']
#
#    edit_columns = ['industry', 'job']
#    edit_exclude_columns =[hide_list] # ['industry', 'job']
#
#    list_columns = ['industry', 'job']
#    list_exclude_columns = [] # ['industry', 'job']
#
#    search_columns = ['industry', 'job']
#    search_exclude_columns= [] # ['industry', 'job']
#
#    default_sort = [('id', True)]
#    base_permissions = ['can_list', 'can_show', 'can_edit', 'can_delete', 'can_add']
#    label_columns=   [{column.name: column.name for column in table.columns} ]
#    show_template =  'appbuilder/general/model/show_cascade.html'
#    list_template = 'appbuilder/general/model/list.html'
#    add_template = 'appbuilder/general/model/add.html'
#    edit_template = 'appbuilder/general/model/edit.html'
#    add_widget = (FormVerticalWidget|FormInlineWidget)
#    show_widget = ShowBlockWidget
#    list_widget = (ListThumbnail|ListWidget)
#    base_order = ('name', 'asc')
#    list_widget= 'list_widget'


class IndustryJobMultiView(MultipleView):
    datamodel=SQLAInterface(IndustryJob, db.session)
    views = [IndustryDetailView, JobDetailView]
    show_title='IndustryJob Detail'
    add_title ='Add IndustryJob'
    list_title= 'IndustryJob List'
    edit_title = 'Edit IndustryJob'
    show_columns = ['industry', 'job']
#    show_exclude_columns = [] #= ['industry', 'job']
#
#    add_columns = ['industry', 'job']
#    add_exclude_columns = [hide_list] #['industry', 'job']
#
#    edit_columns = ['industry', 'job']
#    edit_exclude_columns =[hide_list] # ['industry', 'job']
#
#    list_columns = ['industry', 'job']
#    list_exclude_columns = [] # ['industry', 'job']
#
#    search_columns = ['industry', 'job']
#    search_exclude_columns= [] # ['industry', 'job']
#
#    default_sort = [('id', True)]
#    base_permissions = ['can_list', 'can_show', 'can_edit', 'can_delete', 'can_add']
#    label_columns=   [{column.name: column.name for column in table.columns} ]
#    show_template =  'appbuilder/general/model/show_cascade.html'
#    list_template = 'appbuilder/general/model/list.html'
#    add_template = 'appbuilder/general/model/add.html'
#    edit_template = 'appbuilder/general/model/edit.html'
#    add_widget = (FormVerticalWidget|FormInlineWidget)
#    show_widget = ShowBlockWidget
#    list_widget = (ListThumbnail|ListWidget)
#    base_order = ('name', 'asc')
#    list_widget= 'list_widget'


class JobSkillMasterView(MasterDetailView):
    datamodel=SQLAInterface(JobSkill, db.session)
    related_views = [JobDetailView]
    show_title='JobSkill Detail'
    add_title ='Add JobSkill'
    list_title= 'JobSkill List'
    edit_title = 'Edit JobSkill'
    show_columns = ['skills', 'jobs']
#    show_exclude_columns = [] #= ['skills', 'jobs']
#
#    add_columns = ['skills', 'jobs']
#    add_exclude_columns = [hide_list] #['skills', 'jobs']
#
#    edit_columns = ['skills', 'jobs']
#    edit_exclude_columns =[hide_list] # ['skills', 'jobs']
#
#    list_columns = ['skills', 'jobs']
#    list_exclude_columns = [] # ['skills', 'jobs']
#
#    search_columns = ['skills', 'jobs']
#    search_exclude_columns= [] # ['skills', 'jobs']
#
#    default_sort = [('id', True)]
#    base_permissions = ['can_list', 'can_show', 'can_edit', 'can_delete', 'can_add']
#    label_columns=   [{column.name: column.name for column in table.columns} ]
#    show_template =  'appbuilder/general/model/show_cascade.html'
#    list_template = 'appbuilder/general/model/list.html'
#    add_template = 'appbuilder/general/model/add.html'
#    edit_template = 'appbuilder/general/model/edit.html'
#    add_widget = (FormVerticalWidget|FormInlineWidget)
#    show_widget = ShowBlockWidget
#    list_widget = (ListThumbnail|ListWidget)
#    base_order = ('name', 'asc')
#    list_widget= 'list_widget'


class JobSkillMultiView(MultipleView):
    datamodel=SQLAInterface(JobSkill, db.session)
    views = [SkillDetailView]
    show_title='JobSkill Detail'
    add_title ='Add JobSkill'
    list_title= 'JobSkill List'
    edit_title = 'Edit JobSkill'
    show_columns = ['skills', 'jobs']
#    show_exclude_columns = [] #= ['skills', 'jobs']
#
#    add_columns = ['skills', 'jobs']
#    add_exclude_columns = [hide_list] #['skills', 'jobs']
#
#    edit_columns = ['skills', 'jobs']
#    edit_exclude_columns =[hide_list] # ['skills', 'jobs']
#
#    list_columns = ['skills', 'jobs']
#    list_exclude_columns = [] # ['skills', 'jobs']
#
#    search_columns = ['skills', 'jobs']
#    search_exclude_columns= [] # ['skills', 'jobs']
#
#    default_sort = [('id', True)]
#    base_permissions = ['can_list', 'can_show', 'can_edit', 'can_delete', 'can_add']
#    label_columns=   [{column.name: column.name for column in table.columns} ]
#    show_template =  'appbuilder/general/model/show_cascade.html'
#    list_template = 'appbuilder/general/model/list.html'
#    add_template = 'appbuilder/general/model/add.html'
#    edit_template = 'appbuilder/general/model/edit.html'
#    add_widget = (FormVerticalWidget|FormInlineWidget)
#    show_widget = ShowBlockWidget
#    list_widget = (ListThumbnail|ListWidget)
#    base_order = ('name', 'asc')
#    list_widget= 'list_widget'


class EducationMasterView(MasterDetailView):
    datamodel=SQLAInterface(Education, db.session)
    related_views = [IndividualDetailView]
    show_title='Education Detail'
    add_title ='Add Education'
    list_title= 'Education List'
    edit_title = 'Edit Education'
    show_columns = ['id', 'individual', 'qualification', 'qual_class', 'verified', 'verification_code', 'verified_by', 'verification_date', 'verification_doc']
#    show_exclude_columns = [] #= ['id', 'individual', 'qualification', 'qual_class', 'verified', 'verification_code', 'verified_by', 'verification_date', 'verification_doc']
#
#    add_columns = ['id', 'individual', 'qualification', 'qual_class', 'verified', 'verification_code', 'verified_by', 'verification_date', 'verification_doc']
#    add_exclude_columns = [hide_list] #['id', 'individual', 'qualification', 'qual_class', 'verified', 'verification_code', 'verified_by', 'verification_date', 'verification_doc']
#
#    edit_columns = ['id', 'individual', 'qualification', 'qual_class', 'verified', 'verification_code', 'verified_by', 'verification_date', 'verification_doc']
#    edit_exclude_columns =[hide_list] # ['id', 'individual', 'qualification', 'qual_class', 'verified', 'verification_code', 'verified_by', 'verification_date', 'verification_doc']
#
#    list_columns = ['id', 'individual', 'qualification', 'qual_class', 'verified', 'verification_code', 'verified_by', 'verification_date', 'verification_doc']
#    list_exclude_columns = [] # ['id', 'individual', 'qualification', 'qual_class', 'verified', 'verification_code', 'verified_by', 'verification_date', 'verification_doc']
#
#    search_columns = ['id', 'individual', 'qualification', 'qual_class', 'verified', 'verification_code', 'verified_by', 'verification_date', 'verification_doc']
#    search_exclude_columns= [] # ['id', 'individual', 'qualification', 'qual_class', 'verified', 'verification_code', 'verified_by', 'verification_date', 'verification_doc']
#
#    default_sort = [('id', True)]
#    base_permissions = ['can_list', 'can_show', 'can_edit', 'can_delete', 'can_add']
#    label_columns=   [{column.name: column.name for column in table.columns} ]
#    show_template =  'appbuilder/general/model/show_cascade.html'
#    list_template = 'appbuilder/general/model/list.html'
#    add_template = 'appbuilder/general/model/add.html'
#    edit_template = 'appbuilder/general/model/edit.html'
#    add_widget = (FormVerticalWidget|FormInlineWidget)
#    show_widget = ShowBlockWidget
#    list_widget = (ListThumbnail|ListWidget)
#    base_order = ('name', 'asc')
#    list_widget= 'list_widget'


class IndividualJobMasterView(MasterDetailView):
    datamodel=SQLAInterface(IndividualJob, db.session)
    related_views = [IndividualDetailView]
    show_title='IndividualJob Detail'
    add_title ='Add IndividualJob'
    list_title= 'IndividualJob List'
    edit_title = 'Edit IndividualJob'
    show_columns = ['individual', 'job']
#    show_exclude_columns = [] #= ['individual', 'job']
#
#    add_columns = ['individual', 'job']
#    add_exclude_columns = [hide_list] #['individual', 'job']
#
#    edit_columns = ['individual', 'job']
#    edit_exclude_columns =[hide_list] # ['individual', 'job']
#
#    list_columns = ['individual', 'job']
#    list_exclude_columns = [] # ['individual', 'job']
#
#    search_columns = ['individual', 'job']
#    search_exclude_columns= [] # ['individual', 'job']
#
#    default_sort = [('id', True)]
#    base_permissions = ['can_list', 'can_show', 'can_edit', 'can_delete', 'can_add']
#    label_columns=   [{column.name: column.name for column in table.columns} ]
#    show_template =  'appbuilder/general/model/show_cascade.html'
#    list_template = 'appbuilder/general/model/list.html'
#    add_template = 'appbuilder/general/model/add.html'
#    edit_template = 'appbuilder/general/model/edit.html'
#    add_widget = (FormVerticalWidget|FormInlineWidget)
#    show_widget = ShowBlockWidget
#    list_widget = (ListThumbnail|ListWidget)
#    base_order = ('name', 'asc')
#    list_widget= 'list_widget'


class IndividualJobMultiView(MultipleView):
    datamodel=SQLAInterface(IndividualJob, db.session)
    views = []
    show_title='IndividualJob Detail'
    add_title ='Add IndividualJob'
    list_title= 'IndividualJob List'
    edit_title = 'Edit IndividualJob'
    show_columns = ['individual', 'job']
#    show_exclude_columns = [] #= ['individual', 'job']
#
#    add_columns = ['individual', 'job']
#    add_exclude_columns = [hide_list] #['individual', 'job']
#
#    edit_columns = ['individual', 'job']
#    edit_exclude_columns =[hide_list] # ['individual', 'job']
#
#    list_columns = ['individual', 'job']
#    list_exclude_columns = [] # ['individual', 'job']
#
#    search_columns = ['individual', 'job']
#    search_exclude_columns= [] # ['individual', 'job']
#
#    default_sort = [('id', True)]
#    base_permissions = ['can_list', 'can_show', 'can_edit', 'can_delete', 'can_add']
#    label_columns=   [{column.name: column.name for column in table.columns} ]
#    show_template =  'appbuilder/general/model/show_cascade.html'
#    list_template = 'appbuilder/general/model/list.html'
#    add_template = 'appbuilder/general/model/add.html'
#    edit_template = 'appbuilder/general/model/edit.html'
#    add_widget = (FormVerticalWidget|FormInlineWidget)
#    show_widget = ShowBlockWidget
#    list_widget = (ListThumbnail|ListWidget)
#    base_order = ('name', 'asc')
#    list_widget= 'list_widget'


class LocationMasterView(MasterDetailView):
    datamodel=SQLAInterface(Location, db.session)
    related_views = [IndividualDetailView]
    show_title='Location Detail'
    add_title ='Add Location'
    list_title= 'Location List'
    edit_title = 'Edit Location'
    show_columns = ['id', 'individual']
#    show_exclude_columns = [] #= ['id', 'individual']
#
#    add_columns = ['id', 'individual']
#    add_exclude_columns = [hide_list] #['id', 'individual']
#
#    edit_columns = ['id', 'individual']
#    edit_exclude_columns =[hide_list] # ['id', 'individual']
#
#    list_columns = ['id', 'individual']
#    list_exclude_columns = [] # ['id', 'individual']
#
#    search_columns = ['id', 'individual']
#    search_exclude_columns= [] # ['id', 'individual']
#
#    default_sort = [('id', True)]
#    base_permissions = ['can_list', 'can_show', 'can_edit', 'can_delete', 'can_add']
#    label_columns=   [{column.name: column.name for column in table.columns} ]
#    show_template =  'appbuilder/general/model/show_cascade.html'
#    list_template = 'appbuilder/general/model/list.html'
#    add_template = 'appbuilder/general/model/add.html'
#    edit_template = 'appbuilder/general/model/edit.html'
#    add_widget = (FormVerticalWidget|FormInlineWidget)
#    show_widget = ShowBlockWidget
#    list_widget = (ListThumbnail|ListWidget)
#    base_order = ('name', 'asc')
#    list_widget= 'list_widget'


class PortalMasterView(MasterDetailView):
    datamodel=SQLAInterface(Portal, db.session)
    related_views = [IndividualDetailView]
    show_title='Portal Detail'
    add_title ='Add Portal'
    list_title= 'Portal List'
    edit_title = 'Edit Portal'
    show_columns = ['id', 'portal_url', 'is_primary', 'portal_state', 'individual', 'has_custom_domain', 'domain', 'header_text', 'slug', 'automatic_fulfillment_digital_products', 'default_digital_max_downloads', 'default_digital_url_valid_days', 'default_mail_sender_name', 'default_mail_sender_address', 'fulfillment_auto_approve', 'fulfillment_allow_unpaid', 'reserve_stock_duration_anonymous_user', 'reserve_stock_duration_authenticated_user', 'limit_quantity_per_checkout', 'gift_card_expiry_type', 'gift_card_expiry_period_type', 'gift_card_expiry_period', 'charge_taxes_on_shipping', 'include_taxes_in_prices', 'display_gross_prices', 'language']
#    show_exclude_columns = [] #= ['id', 'portal_url', 'is_primary', 'portal_state', 'individual', 'has_custom_domain', 'domain', 'header_text', 'slug', 'automatic_fulfillment_digital_products', 'default_digital_max_downloads', 'default_digital_url_valid_days', 'default_mail_sender_name', 'default_mail_sender_address', 'fulfillment_auto_approve', 'fulfillment_allow_unpaid', 'reserve_stock_duration_anonymous_user', 'reserve_stock_duration_authenticated_user', 'limit_quantity_per_checkout', 'gift_card_expiry_type', 'gift_card_expiry_period_type', 'gift_card_expiry_period', 'charge_taxes_on_shipping', 'include_taxes_in_prices', 'display_gross_prices', 'language']
#
#    add_columns = ['id', 'portal_url', 'is_primary', 'portal_state', 'individual', 'has_custom_domain', 'domain', 'header_text', 'slug', 'automatic_fulfillment_digital_products', 'default_digital_max_downloads', 'default_digital_url_valid_days', 'default_mail_sender_name', 'default_mail_sender_address', 'fulfillment_auto_approve', 'fulfillment_allow_unpaid', 'reserve_stock_duration_anonymous_user', 'reserve_stock_duration_authenticated_user', 'limit_quantity_per_checkout', 'gift_card_expiry_type', 'gift_card_expiry_period_type', 'gift_card_expiry_period', 'charge_taxes_on_shipping', 'include_taxes_in_prices', 'display_gross_prices', 'language']
#    add_exclude_columns = [hide_list] #['id', 'portal_url', 'is_primary', 'portal_state', 'individual', 'has_custom_domain', 'domain', 'header_text', 'slug', 'automatic_fulfillment_digital_products', 'default_digital_max_downloads', 'default_digital_url_valid_days', 'default_mail_sender_name', 'default_mail_sender_address', 'fulfillment_auto_approve', 'fulfillment_allow_unpaid', 'reserve_stock_duration_anonymous_user', 'reserve_stock_duration_authenticated_user', 'limit_quantity_per_checkout', 'gift_card_expiry_type', 'gift_card_expiry_period_type', 'gift_card_expiry_period', 'charge_taxes_on_shipping', 'include_taxes_in_prices', 'display_gross_prices', 'language']
#
#    edit_columns = ['id', 'portal_url', 'is_primary', 'portal_state', 'individual', 'has_custom_domain', 'domain', 'header_text', 'slug', 'automatic_fulfillment_digital_products', 'default_digital_max_downloads', 'default_digital_url_valid_days', 'default_mail_sender_name', 'default_mail_sender_address', 'fulfillment_auto_approve', 'fulfillment_allow_unpaid', 'reserve_stock_duration_anonymous_user', 'reserve_stock_duration_authenticated_user', 'limit_quantity_per_checkout', 'gift_card_expiry_type', 'gift_card_expiry_period_type', 'gift_card_expiry_period', 'charge_taxes_on_shipping', 'include_taxes_in_prices', 'display_gross_prices', 'language']
#    edit_exclude_columns =[hide_list] # ['id', 'portal_url', 'is_primary', 'portal_state', 'individual', 'has_custom_domain', 'domain', 'header_text', 'slug', 'automatic_fulfillment_digital_products', 'default_digital_max_downloads', 'default_digital_url_valid_days', 'default_mail_sender_name', 'default_mail_sender_address', 'fulfillment_auto_approve', 'fulfillment_allow_unpaid', 'reserve_stock_duration_anonymous_user', 'reserve_stock_duration_authenticated_user', 'limit_quantity_per_checkout', 'gift_card_expiry_type', 'gift_card_expiry_period_type', 'gift_card_expiry_period', 'charge_taxes_on_shipping', 'include_taxes_in_prices', 'display_gross_prices', 'language']
#
#    list_columns = ['id', 'portal_url', 'is_primary', 'portal_state', 'individual', 'has_custom_domain', 'domain', 'header_text', 'slug', 'automatic_fulfillment_digital_products', 'default_digital_max_downloads', 'default_digital_url_valid_days', 'default_mail_sender_name', 'default_mail_sender_address', 'fulfillment_auto_approve', 'fulfillment_allow_unpaid', 'reserve_stock_duration_anonymous_user', 'reserve_stock_duration_authenticated_user', 'limit_quantity_per_checkout', 'gift_card_expiry_type', 'gift_card_expiry_period_type', 'gift_card_expiry_period', 'charge_taxes_on_shipping', 'include_taxes_in_prices', 'display_gross_prices', 'language']
#    list_exclude_columns = [] # ['id', 'portal_url', 'is_primary', 'portal_state', 'individual', 'has_custom_domain', 'domain', 'header_text', 'slug', 'automatic_fulfillment_digital_products', 'default_digital_max_downloads', 'default_digital_url_valid_days', 'default_mail_sender_name', 'default_mail_sender_address', 'fulfillment_auto_approve', 'fulfillment_allow_unpaid', 'reserve_stock_duration_anonymous_user', 'reserve_stock_duration_authenticated_user', 'limit_quantity_per_checkout', 'gift_card_expiry_type', 'gift_card_expiry_period_type', 'gift_card_expiry_period', 'charge_taxes_on_shipping', 'include_taxes_in_prices', 'display_gross_prices', 'language']
#
#    search_columns = ['id', 'portal_url', 'is_primary', 'portal_state', 'individual', 'has_custom_domain', 'domain', 'header_text', 'slug', 'automatic_fulfillment_digital_products', 'default_digital_max_downloads', 'default_digital_url_valid_days', 'default_mail_sender_name', 'default_mail_sender_address', 'fulfillment_auto_approve', 'fulfillment_allow_unpaid', 'reserve_stock_duration_anonymous_user', 'reserve_stock_duration_authenticated_user', 'limit_quantity_per_checkout', 'gift_card_expiry_type', 'gift_card_expiry_period_type', 'gift_card_expiry_period', 'charge_taxes_on_shipping', 'include_taxes_in_prices', 'display_gross_prices', 'language']
#    search_exclude_columns= [] # ['id', 'portal_url', 'is_primary', 'portal_state', 'individual', 'has_custom_domain', 'domain', 'header_text', 'slug', 'automatic_fulfillment_digital_products', 'default_digital_max_downloads', 'default_digital_url_valid_days', 'default_mail_sender_name', 'default_mail_sender_address', 'fulfillment_auto_approve', 'fulfillment_allow_unpaid', 'reserve_stock_duration_anonymous_user', 'reserve_stock_duration_authenticated_user', 'limit_quantity_per_checkout', 'gift_card_expiry_type', 'gift_card_expiry_period_type', 'gift_card_expiry_period', 'charge_taxes_on_shipping', 'include_taxes_in_prices', 'display_gross_prices', 'language']
#
#    default_sort = [('id', True)]
#    base_permissions = ['can_list', 'can_show', 'can_edit', 'can_delete', 'can_add']
#    label_columns=   [{column.name: column.name for column in table.columns} ]
#    show_template =  'appbuilder/general/model/show_cascade.html'
#    list_template = 'appbuilder/general/model/list.html'
#    add_template = 'appbuilder/general/model/add.html'
#    edit_template = 'appbuilder/general/model/edit.html'
#    add_widget = (FormVerticalWidget|FormInlineWidget)
#    show_widget = ShowBlockWidget
#    list_widget = (ListThumbnail|ListWidget)
#    base_order = ('name', 'asc')
#    list_widget= 'list_widget'


class PageMasterView(MasterDetailView):
    datamodel=SQLAInterface(Page, db.session)
    related_views = [PortalDetailView]
    show_title='Page Detail'
    add_title ='Add Page'
    list_title= 'Page List'
    edit_title = 'Edit Page'
    show_columns = ['id', 'portal', 'header', 'slug', 'page_type']
#    show_exclude_columns = [] #= ['id', 'portal', 'header', 'slug', 'page_type']
#
#    add_columns = ['id', 'portal', 'header', 'slug', 'page_type']
#    add_exclude_columns = [hide_list] #['id', 'portal', 'header', 'slug', 'page_type']
#
#    edit_columns = ['id', 'portal', 'header', 'slug', 'page_type']
#    edit_exclude_columns =[hide_list] # ['id', 'portal', 'header', 'slug', 'page_type']
#
#    list_columns = ['id', 'portal', 'header', 'slug', 'page_type']
#    list_exclude_columns = [] # ['id', 'portal', 'header', 'slug', 'page_type']
#
#    search_columns = ['id', 'portal', 'header', 'slug', 'page_type']
#    search_exclude_columns= [] # ['id', 'portal', 'header', 'slug', 'page_type']
#
#    default_sort = [('id', True)]
#    base_permissions = ['can_list', 'can_show', 'can_edit', 'can_delete', 'can_add']
#    label_columns=   [{column.name: column.name for column in table.columns} ]
#    show_template =  'appbuilder/general/model/show_cascade.html'
#    list_template = 'appbuilder/general/model/list.html'
#    add_template = 'appbuilder/general/model/add.html'
#    edit_template = 'appbuilder/general/model/edit.html'
#    add_widget = (FormVerticalWidget|FormInlineWidget)
#    show_widget = ShowBlockWidget
#    list_widget = (ListThumbnail|ListWidget)
#    base_order = ('name', 'asc')
#    list_widget= 'list_widget'


class ProfileMasterView(MasterDetailView):
    datamodel=SQLAInterface(Profile, db.session)
    related_views = [IndividualDetailView]
    show_title='Profile Detail'
    add_title ='Add Profile'
    list_title= 'Profile List'
    edit_title = 'Edit Profile'
    show_columns = ['id', 'individual', 'import_address', 'profile_username', 'profile_password', 'has_been_imported', 'import_data', 'import_date', 'profilesource']
#    show_exclude_columns = [] #= ['id', 'individual', 'import_address', 'profile_username', 'profile_password', 'has_been_imported', 'import_data', 'import_date', 'profilesource']
#
#    add_columns = ['id', 'individual', 'import_address', 'profile_username', 'profile_password', 'has_been_imported', 'import_data', 'import_date', 'profilesource']
#    add_exclude_columns = [hide_list] #['id', 'individual', 'import_address', 'profile_username', 'profile_password', 'has_been_imported', 'import_data', 'import_date', 'profilesource']
#
#    edit_columns = ['id', 'individual', 'import_address', 'profile_username', 'profile_password', 'has_been_imported', 'import_data', 'import_date', 'profilesource']
#    edit_exclude_columns =[hide_list] # ['id', 'individual', 'import_address', 'profile_username', 'profile_password', 'has_been_imported', 'import_data', 'import_date', 'profilesource']
#
#    list_columns = ['id', 'individual', 'import_address', 'profile_username', 'profile_password', 'has_been_imported', 'import_data', 'import_date', 'profilesource']
#    list_exclude_columns = [] # ['id', 'individual', 'import_address', 'profile_username', 'profile_password', 'has_been_imported', 'import_data', 'import_date', 'profilesource']
#
#    search_columns = ['id', 'individual', 'import_address', 'profile_username', 'profile_password', 'has_been_imported', 'import_data', 'import_date', 'profilesource']
#    search_exclude_columns= [] # ['id', 'individual', 'import_address', 'profile_username', 'profile_password', 'has_been_imported', 'import_data', 'import_date', 'profilesource']
#
#    default_sort = [('id', True)]
#    base_permissions = ['can_list', 'can_show', 'can_edit', 'can_delete', 'can_add']
#    label_columns=   [{column.name: column.name for column in table.columns} ]
#    show_template =  'appbuilder/general/model/show_cascade.html'
#    list_template = 'appbuilder/general/model/list.html'
#    add_template = 'appbuilder/general/model/add.html'
#    edit_template = 'appbuilder/general/model/edit.html'
#    add_widget = (FormVerticalWidget|FormInlineWidget)
#    show_widget = ShowBlockWidget
#    list_widget = (ListThumbnail|ListWidget)
#    base_order = ('name', 'asc')
#    list_widget= 'list_widget'


class ProfileMultiView(MultipleView):
    datamodel=SQLAInterface(Profile, db.session)
    views = [ProfilesourceDetailView]
    show_title='Profile Detail'
    add_title ='Add Profile'
    list_title= 'Profile List'
    edit_title = 'Edit Profile'
    show_columns = ['id', 'individual', 'import_address', 'profile_username', 'profile_password', 'has_been_imported', 'import_data', 'import_date', 'profilesource']
#    show_exclude_columns = [] #= ['id', 'individual', 'import_address', 'profile_username', 'profile_password', 'has_been_imported', 'import_data', 'import_date', 'profilesource']
#
#    add_columns = ['id', 'individual', 'import_address', 'profile_username', 'profile_password', 'has_been_imported', 'import_data', 'import_date', 'profilesource']
#    add_exclude_columns = [hide_list] #['id', 'individual', 'import_address', 'profile_username', 'profile_password', 'has_been_imported', 'import_data', 'import_date', 'profilesource']
#
#    edit_columns = ['id', 'individual', 'import_address', 'profile_username', 'profile_password', 'has_been_imported', 'import_data', 'import_date', 'profilesource']
#    edit_exclude_columns =[hide_list] # ['id', 'individual', 'import_address', 'profile_username', 'profile_password', 'has_been_imported', 'import_data', 'import_date', 'profilesource']
#
#    list_columns = ['id', 'individual', 'import_address', 'profile_username', 'profile_password', 'has_been_imported', 'import_data', 'import_date', 'profilesource']
#    list_exclude_columns = [] # ['id', 'individual', 'import_address', 'profile_username', 'profile_password', 'has_been_imported', 'import_data', 'import_date', 'profilesource']
#
#    search_columns = ['id', 'individual', 'import_address', 'profile_username', 'profile_password', 'has_been_imported', 'import_data', 'import_date', 'profilesource']
#    search_exclude_columns= [] # ['id', 'individual', 'import_address', 'profile_username', 'profile_password', 'has_been_imported', 'import_data', 'import_date', 'profilesource']
#
#    default_sort = [('id', True)]
#    base_permissions = ['can_list', 'can_show', 'can_edit', 'can_delete', 'can_add']
#    label_columns=   [{column.name: column.name for column in table.columns} ]
#    show_template =  'appbuilder/general/model/show_cascade.html'
#    list_template = 'appbuilder/general/model/list.html'
#    add_template = 'appbuilder/general/model/add.html'
#    edit_template = 'appbuilder/general/model/edit.html'
#    add_widget = (FormVerticalWidget|FormInlineWidget)
#    show_widget = ShowBlockWidget
#    list_widget = (ListThumbnail|ListWidget)
#    base_order = ('name', 'asc')
#    list_widget= 'list_widget'


class ResumeMasterView(MasterDetailView):
    datamodel=SQLAInterface(Resume, db.session)
    related_views = [IndividualDetailView]
    show_title='Resume Detail'
    add_title ='Add Resume'
    list_title= 'Resume List'
    edit_title = 'Edit Resume'
    show_columns = ['id', 'individual', 'template', 'header', 'color', 'location', 'summary_text', 'has_been_generated', 'preferred']
#    show_exclude_columns = [] #= ['id', 'individual', 'template', 'header', 'color', 'location', 'summary_text', 'has_been_generated', 'preferred']
#
#    add_columns = ['id', 'individual', 'template', 'header', 'color', 'location', 'summary_text', 'has_been_generated', 'preferred']
#    add_exclude_columns = [hide_list] #['id', 'individual', 'template', 'header', 'color', 'location', 'summary_text', 'has_been_generated', 'preferred']
#
#    edit_columns = ['id', 'individual', 'template', 'header', 'color', 'location', 'summary_text', 'has_been_generated', 'preferred']
#    edit_exclude_columns =[hide_list] # ['id', 'individual', 'template', 'header', 'color', 'location', 'summary_text', 'has_been_generated', 'preferred']
#
#    list_columns = ['id', 'individual', 'template', 'header', 'color', 'location', 'summary_text', 'has_been_generated', 'preferred']
#    list_exclude_columns = [] # ['id', 'individual', 'template', 'header', 'color', 'location', 'summary_text', 'has_been_generated', 'preferred']
#
#    search_columns = ['id', 'individual', 'template', 'header', 'color', 'location', 'summary_text', 'has_been_generated', 'preferred']
#    search_exclude_columns= [] # ['id', 'individual', 'template', 'header', 'color', 'location', 'summary_text', 'has_been_generated', 'preferred']
#
#    default_sort = [('id', True)]
#    base_permissions = ['can_list', 'can_show', 'can_edit', 'can_delete', 'can_add']
#    label_columns=   [{column.name: column.name for column in table.columns} ]
#    show_template =  'appbuilder/general/model/show_cascade.html'
#    list_template = 'appbuilder/general/model/list.html'
#    add_template = 'appbuilder/general/model/add.html'
#    edit_template = 'appbuilder/general/model/edit.html'
#    add_widget = (FormVerticalWidget|FormInlineWidget)
#    show_widget = ShowBlockWidget
#    list_widget = (ListThumbnail|ListWidget)
#    base_order = ('name', 'asc')
#    list_widget= 'list_widget'


class ResumeMultiView(MultipleView):
    datamodel=SQLAInterface(Resume, db.session)
    views = [LocationDetailView]
    show_title='Resume Detail'
    add_title ='Add Resume'
    list_title= 'Resume List'
    edit_title = 'Edit Resume'
    show_columns = ['id', 'individual', 'template', 'header', 'color', 'location', 'summary_text', 'has_been_generated', 'preferred']
#    show_exclude_columns = [] #= ['id', 'individual', 'template', 'header', 'color', 'location', 'summary_text', 'has_been_generated', 'preferred']
#
#    add_columns = ['id', 'individual', 'template', 'header', 'color', 'location', 'summary_text', 'has_been_generated', 'preferred']
#    add_exclude_columns = [hide_list] #['id', 'individual', 'template', 'header', 'color', 'location', 'summary_text', 'has_been_generated', 'preferred']
#
#    edit_columns = ['id', 'individual', 'template', 'header', 'color', 'location', 'summary_text', 'has_been_generated', 'preferred']
#    edit_exclude_columns =[hide_list] # ['id', 'individual', 'template', 'header', 'color', 'location', 'summary_text', 'has_been_generated', 'preferred']
#
#    list_columns = ['id', 'individual', 'template', 'header', 'color', 'location', 'summary_text', 'has_been_generated', 'preferred']
#    list_exclude_columns = [] # ['id', 'individual', 'template', 'header', 'color', 'location', 'summary_text', 'has_been_generated', 'preferred']
#
#    search_columns = ['id', 'individual', 'template', 'header', 'color', 'location', 'summary_text', 'has_been_generated', 'preferred']
#    search_exclude_columns= [] # ['id', 'individual', 'template', 'header', 'color', 'location', 'summary_text', 'has_been_generated', 'preferred']
#
#    default_sort = [('id', True)]
#    base_permissions = ['can_list', 'can_show', 'can_edit', 'can_delete', 'can_add']
#    label_columns=   [{column.name: column.name for column in table.columns} ]
#    show_template =  'appbuilder/general/model/show_cascade.html'
#    list_template = 'appbuilder/general/model/list.html'
#    add_template = 'appbuilder/general/model/add.html'
#    edit_template = 'appbuilder/general/model/edit.html'
#    add_widget = (FormVerticalWidget|FormInlineWidget)
#    show_widget = ShowBlockWidget
#    list_widget = (ListThumbnail|ListWidget)
#    base_order = ('name', 'asc')
#    list_widget= 'list_widget'


class SwarmView(ModelView):
    datamodel=SQLAInterface(Swarm, db.session)
    related_views = []
    show_title='Swarm Detail'
    add_title ='Add Swarm'
    list_title= 'Swarm List'
    edit_title = 'Edit Swarm'
    show_columns = ['id', 'portal']
#    show_exclude_columns = [] #= ['id', 'portal']
#
#    add_columns = ['id', 'portal']
#    add_exclude_columns = [hide_list] #['id', 'portal']
#
#    edit_columns = ['id', 'portal']
#    edit_exclude_columns =[hide_list] # ['id', 'portal']
#
#    list_columns = ['id', 'portal']
#    list_exclude_columns = [] # ['id', 'portal']
#
#    search_columns = ['id', 'portal']
#    search_exclude_columns= [] # ['id', 'portal']
#
#    default_sort = [('id', True)]
#    base_permissions = ['can_list', 'can_show', 'can_edit', 'can_delete', 'can_add']
#    label_columns=   [{column.name: column.name for column in table.columns} ]
#    show_template =  'appbuilder/general/model/show_cascade.html'
#    list_template = 'appbuilder/general/model/list.html'
#    add_template = 'appbuilder/general/model/add.html'
#    edit_template = 'appbuilder/general/model/edit.html'
#    add_widget = (FormVerticalWidget|FormInlineWidget)
#    show_widget = ShowBlockWidget
#    list_widget = (ListThumbnail|ListWidget)
#    base_order = ('name', 'asc')
#    list_widget= 'list_widget'


class UserxDetailView(ModelView):
    datamodel=SQLAInterface(Userx, db.session)
    related_views = []
    show_title='Userx Detail'
    add_title ='Add Userx'
    list_title= 'Userx List'
    edit_title = 'Edit Userx'
    show_columns = ['id', 'userx', 'is_individual', 'is_institution', 'is_company', 'is_government', 'is_online']
#    show_exclude_columns = [] #= ['id', 'userx', 'is_individual', 'is_institution', 'is_company', 'is_government', 'is_online']
#
#    add_columns = ['id', 'userx', 'is_individual', 'is_institution', 'is_company', 'is_government', 'is_online']
#    add_exclude_columns = [hide_list] #['id', 'userx', 'is_individual', 'is_institution', 'is_company', 'is_government', 'is_online']
#
#    edit_columns = ['id', 'userx', 'is_individual', 'is_institution', 'is_company', 'is_government', 'is_online']
#    edit_exclude_columns =[hide_list] # ['id', 'userx', 'is_individual', 'is_institution', 'is_company', 'is_government', 'is_online']
#
#    list_columns = ['id', 'userx', 'is_individual', 'is_institution', 'is_company', 'is_government', 'is_online']
#    list_exclude_columns = [] # ['id', 'userx', 'is_individual', 'is_institution', 'is_company', 'is_government', 'is_online']
#
#    search_columns = ['id', 'userx', 'is_individual', 'is_institution', 'is_company', 'is_government', 'is_online']
#    search_exclude_columns= [] # ['id', 'userx', 'is_individual', 'is_institution', 'is_company', 'is_government', 'is_online']
#
#    default_sort = [('id', True)]
#    base_permissions = ['can_list', 'can_show', 'can_edit', 'can_delete', 'can_add']
#    label_columns=   [{column.name: column.name for column in table.columns} ]
#    show_template =  'appbuilder/general/model/show_cascade.html'
#    list_template = 'appbuilder/general/model/list.html'
#    add_template = 'appbuilder/general/model/add.html'
#    edit_template = 'appbuilder/general/model/edit.html'
#    add_widget = (FormVerticalWidget|FormInlineWidget)
#    show_widget = ShowBlockWidget
#    list_widget = (ListThumbnail|ListWidget)
#    base_order = ('name', 'asc')
#    list_widget= 'list_widget'


class IndividualDetailView(ModelView):
    datamodel=SQLAInterface(Individual, db.session)
    related_views = []
    show_title='Individual Detail'
    add_title ='Add Individual'
    list_title= 'Individual List'
    edit_title = 'Edit Individual'
    show_columns = ['id', 'userx', 'is_individual', 'is_institution', 'is_company', 'is_government', 'is_online']
#    show_exclude_columns = [] #= ['id', 'userx', 'is_individual', 'is_institution', 'is_company', 'is_government', 'is_online']
#
#    add_columns = ['id', 'userx', 'is_individual', 'is_institution', 'is_company', 'is_government', 'is_online']
#    add_exclude_columns = [hide_list] #['id', 'userx', 'is_individual', 'is_institution', 'is_company', 'is_government', 'is_online']
#
#    edit_columns = ['id', 'userx', 'is_individual', 'is_institution', 'is_company', 'is_government', 'is_online']
#    edit_exclude_columns =[hide_list] # ['id', 'userx', 'is_individual', 'is_institution', 'is_company', 'is_government', 'is_online']
#
#    list_columns = ['id', 'userx', 'is_individual', 'is_institution', 'is_company', 'is_government', 'is_online']
#    list_exclude_columns = [] # ['id', 'userx', 'is_individual', 'is_institution', 'is_company', 'is_government', 'is_online']
#
#    search_columns = ['id', 'userx', 'is_individual', 'is_institution', 'is_company', 'is_government', 'is_online']
#    search_exclude_columns= [] # ['id', 'userx', 'is_individual', 'is_institution', 'is_company', 'is_government', 'is_online']
#
#    default_sort = [('id', True)]
#    base_permissions = ['can_list', 'can_show', 'can_edit', 'can_delete', 'can_add']
#    label_columns=   [{column.name: column.name for column in table.columns} ]
#    show_template =  'appbuilder/general/model/show_cascade.html'
#    list_template = 'appbuilder/general/model/list.html'
#    add_template = 'appbuilder/general/model/add.html'
#    edit_template = 'appbuilder/general/model/edit.html'
#    add_widget = (FormVerticalWidget|FormInlineWidget)
#    show_widget = ShowBlockWidget
#    list_widget = (ListThumbnail|ListWidget)
#    base_order = ('name', 'asc')
#    list_widget= 'list_widget'


class IndustryDetailView(ModelView):
    datamodel=SQLAInterface(Industry, db.session)
    related_views = []
    show_title='Industry Detail'
    add_title ='Add Industry'
    list_title= 'Industry List'
    edit_title = 'Edit Industry'
    show_columns = ['industry', 'job']
#    show_exclude_columns = [] #= ['industry', 'job']
#
#    add_columns = ['industry', 'job']
#    add_exclude_columns = [hide_list] #['industry', 'job']
#
#    edit_columns = ['industry', 'job']
#    edit_exclude_columns =[hide_list] # ['industry', 'job']
#
#    list_columns = ['industry', 'job']
#    list_exclude_columns = [] # ['industry', 'job']
#
#    search_columns = ['industry', 'job']
#    search_exclude_columns= [] # ['industry', 'job']
#
#    default_sort = [('id', True)]
#    base_permissions = ['can_list', 'can_show', 'can_edit', 'can_delete', 'can_add']
#    label_columns=   [{column.name: column.name for column in table.columns} ]
#    show_template =  'appbuilder/general/model/show_cascade.html'
#    list_template = 'appbuilder/general/model/list.html'
#    add_template = 'appbuilder/general/model/add.html'
#    edit_template = 'appbuilder/general/model/edit.html'
#    add_widget = (FormVerticalWidget|FormInlineWidget)
#    show_widget = ShowBlockWidget
#    list_widget = (ListThumbnail|ListWidget)
#    base_order = ('name', 'asc')
#    list_widget= 'list_widget'


class IndustryJobDetailView(ModelView):
    datamodel=SQLAInterface(IndustryJob, db.session)
    related_views = []
    show_title='IndustryJob Detail'
    add_title ='Add IndustryJob'
    list_title= 'IndustryJob List'
    edit_title = 'Edit IndustryJob'
    show_columns = ['industry', 'job']
#    show_exclude_columns = [] #= ['industry', 'job']
#
#    add_columns = ['industry', 'job']
#    add_exclude_columns = [hide_list] #['industry', 'job']
#
#    edit_columns = ['industry', 'job']
#    edit_exclude_columns =[hide_list] # ['industry', 'job']
#
#    list_columns = ['industry', 'job']
#    list_exclude_columns = [] # ['industry', 'job']
#
#    search_columns = ['industry', 'job']
#    search_exclude_columns= [] # ['industry', 'job']
#
#    default_sort = [('id', True)]
#    base_permissions = ['can_list', 'can_show', 'can_edit', 'can_delete', 'can_add']
#    label_columns=   [{column.name: column.name for column in table.columns} ]
#    show_template =  'appbuilder/general/model/show_cascade.html'
#    list_template = 'appbuilder/general/model/list.html'
#    add_template = 'appbuilder/general/model/add.html'
#    edit_template = 'appbuilder/general/model/edit.html'
#    add_widget = (FormVerticalWidget|FormInlineWidget)
#    show_widget = ShowBlockWidget
#    list_widget = (ListThumbnail|ListWidget)
#    base_order = ('name', 'asc')
#    list_widget= 'list_widget'


class JobDetailView(ModelView):
    datamodel=SQLAInterface(Job, db.session)
    related_views = []
    show_title='Job Detail'
    add_title ='Add Job'
    list_title= 'Job List'
    edit_title = 'Edit Job'
    show_columns = ['industry', 'job']
#    show_exclude_columns = [] #= ['industry', 'job']
#
#    add_columns = ['industry', 'job']
#    add_exclude_columns = [hide_list] #['industry', 'job']
#
#    edit_columns = ['industry', 'job']
#    edit_exclude_columns =[hide_list] # ['industry', 'job']
#
#    list_columns = ['industry', 'job']
#    list_exclude_columns = [] # ['industry', 'job']
#
#    search_columns = ['industry', 'job']
#    search_exclude_columns= [] # ['industry', 'job']
#
#    default_sort = [('id', True)]
#    base_permissions = ['can_list', 'can_show', 'can_edit', 'can_delete', 'can_add']
#    label_columns=   [{column.name: column.name for column in table.columns} ]
#    show_template =  'appbuilder/general/model/show_cascade.html'
#    list_template = 'appbuilder/general/model/list.html'
#    add_template = 'appbuilder/general/model/add.html'
#    edit_template = 'appbuilder/general/model/edit.html'
#    add_widget = (FormVerticalWidget|FormInlineWidget)
#    show_widget = ShowBlockWidget
#    list_widget = (ListThumbnail|ListWidget)
#    base_order = ('name', 'asc')
#    list_widget= 'list_widget'




class SkillDetailView(ModelView):
    datamodel=SQLAInterface(Skill, db.session)
    related_views = []
    show_title='Skill Detail'
    add_title ='Add Skill'
    list_title= 'Skill List'
    edit_title = 'Edit Skill'
    show_columns = ['skills', 'jobs']
#    show_exclude_columns = [] #= ['skills', 'jobs']
#
#    add_columns = ['skills', 'jobs']
#    add_exclude_columns = [hide_list] #['skills', 'jobs']
#
#    edit_columns = ['skills', 'jobs']
#    edit_exclude_columns =[hide_list] # ['skills', 'jobs']
#
#    list_columns = ['skills', 'jobs']
#    list_exclude_columns = [] # ['skills', 'jobs']
#
#    search_columns = ['skills', 'jobs']
#    search_exclude_columns= [] # ['skills', 'jobs']
#
#    default_sort = [('id', True)]
#    base_permissions = ['can_list', 'can_show', 'can_edit', 'can_delete', 'can_add']
#    label_columns=   [{column.name: column.name for column in table.columns} ]
#    show_template =  'appbuilder/general/model/show_cascade.html'
#    list_template = 'appbuilder/general/model/list.html'
#    add_template = 'appbuilder/general/model/add.html'
#    edit_template = 'appbuilder/general/model/edit.html'
#    add_widget = (FormVerticalWidget|FormInlineWidget)
#    show_widget = ShowBlockWidget
#    list_widget = (ListThumbnail|ListWidget)
#    base_order = ('name', 'asc')
#    list_widget= 'list_widget'


class JobSkillDetailView(ModelView):
    datamodel=SQLAInterface(JobSkill, db.session)
    related_views = []
    show_title='JobSkill Detail'
    add_title ='Add JobSkill'
    list_title= 'JobSkill List'
    edit_title = 'Edit JobSkill'
    show_columns = ['skills', 'jobs']
#    show_exclude_columns = [] #= ['skills', 'jobs']
#
#    add_columns = ['skills', 'jobs']
#    add_exclude_columns = [hide_list] #['skills', 'jobs']
#
#    edit_columns = ['skills', 'jobs']
#    edit_exclude_columns =[hide_list] # ['skills', 'jobs']
#
#    list_columns = ['skills', 'jobs']
#    list_exclude_columns = [] # ['skills', 'jobs']
#
#    search_columns = ['skills', 'jobs']
#    search_exclude_columns= [] # ['skills', 'jobs']
#
#    default_sort = [('id', True)]
#    base_permissions = ['can_list', 'can_show', 'can_edit', 'can_delete', 'can_add']
#    label_columns=   [{column.name: column.name for column in table.columns} ]
#    show_template =  'appbuilder/general/model/show_cascade.html'
#    list_template = 'appbuilder/general/model/list.html'
#    add_template = 'appbuilder/general/model/add.html'
#    edit_template = 'appbuilder/general/model/edit.html'
#    add_widget = (FormVerticalWidget|FormInlineWidget)
#    show_widget = ShowBlockWidget
#    list_widget = (ListThumbnail|ListWidget)
#    base_order = ('name', 'asc')
#    list_widget= 'list_widget'


class PortalDetailView(ModelView):
    datamodel=SQLAInterface(Portal, db.session)
    related_views = []
    show_title='Portal Detail'
    add_title ='Add Portal'
    list_title= 'Portal List'
    edit_title = 'Edit Portal'
    show_columns = ['id', 'portal', 'header', 'slug', 'page_type']
#    show_exclude_columns = [] #= ['id', 'portal', 'header', 'slug', 'page_type']
#
#    add_columns = ['id', 'portal', 'header', 'slug', 'page_type']
#    add_exclude_columns = [hide_list] #['id', 'portal', 'header', 'slug', 'page_type']
#
#    edit_columns = ['id', 'portal', 'header', 'slug', 'page_type']
#    edit_exclude_columns =[hide_list] # ['id', 'portal', 'header', 'slug', 'page_type']
#
#    list_columns = ['id', 'portal', 'header', 'slug', 'page_type']
#    list_exclude_columns = [] # ['id', 'portal', 'header', 'slug', 'page_type']
#
#    search_columns = ['id', 'portal', 'header', 'slug', 'page_type']
#    search_exclude_columns= [] # ['id', 'portal', 'header', 'slug', 'page_type']
#
#    default_sort = [('id', True)]
#    base_permissions = ['can_list', 'can_show', 'can_edit', 'can_delete', 'can_add']
#    label_columns=   [{column.name: column.name for column in table.columns} ]
#    show_template =  'appbuilder/general/model/show_cascade.html'
#    list_template = 'appbuilder/general/model/list.html'
#    add_template = 'appbuilder/general/model/add.html'
#    edit_template = 'appbuilder/general/model/edit.html'
#    add_widget = (FormVerticalWidget|FormInlineWidget)
#    show_widget = ShowBlockWidget
#    list_widget = (ListThumbnail|ListWidget)
#    base_order = ('name', 'asc')
#    list_widget= 'list_widget'


class PageDetailView(ModelView):
    datamodel=SQLAInterface(Page, db.session)
    related_views = []
    show_title='Page Detail'
    add_title ='Add Page'
    list_title= 'Page List'
    edit_title = 'Edit Page'
    show_columns = ['id', 'portal', 'header', 'slug', 'page_type']
#    show_exclude_columns = [] #= ['id', 'portal', 'header', 'slug', 'page_type']
#
#    add_columns = ['id', 'portal', 'header', 'slug', 'page_type']
#    add_exclude_columns = [hide_list] #['id', 'portal', 'header', 'slug', 'page_type']
#
#    edit_columns = ['id', 'portal', 'header', 'slug', 'page_type']
#    edit_exclude_columns =[hide_list] # ['id', 'portal', 'header', 'slug', 'page_type']
#
#    list_columns = ['id', 'portal', 'header', 'slug', 'page_type']
#    list_exclude_columns = [] # ['id', 'portal', 'header', 'slug', 'page_type']
#
#    search_columns = ['id', 'portal', 'header', 'slug', 'page_type']
#    search_exclude_columns= [] # ['id', 'portal', 'header', 'slug', 'page_type']
#
#    default_sort = [('id', True)]
#    base_permissions = ['can_list', 'can_show', 'can_edit', 'can_delete', 'can_add']
#    label_columns=   [{column.name: column.name for column in table.columns} ]
#    show_template =  'appbuilder/general/model/show_cascade.html'
#    list_template = 'appbuilder/general/model/list.html'
#    add_template = 'appbuilder/general/model/add.html'
#    edit_template = 'appbuilder/general/model/edit.html'
#    add_widget = (FormVerticalWidget|FormInlineWidget)
#    show_widget = ShowBlockWidget
#    list_widget = (ListThumbnail|ListWidget)
#    base_order = ('name', 'asc')
#    list_widget= 'list_widget'


class ProfilesourceDetailView(ModelView):
    datamodel=SQLAInterface(Profilesource, db.session)
    related_views = []
    show_title='Profilesource Detail'
    add_title ='Add Profilesource'
    list_title= 'Profilesource List'
    edit_title = 'Edit Profilesource'
    show_columns = ['id', 'individual', 'import_address', 'profile_username', 'profile_password', 'has_been_imported', 'import_data', 'import_date', 'profilesource']
#    show_exclude_columns = [] #= ['id', 'individual', 'import_address', 'profile_username', 'profile_password', 'has_been_imported', 'import_data', 'import_date', 'profilesource']
#
#    add_columns = ['id', 'individual', 'import_address', 'profile_username', 'profile_password', 'has_been_imported', 'import_data', 'import_date', 'profilesource']
#    add_exclude_columns = [hide_list] #['id', 'individual', 'import_address', 'profile_username', 'profile_password', 'has_been_imported', 'import_data', 'import_date', 'profilesource']
#
#    edit_columns = ['id', 'individual', 'import_address', 'profile_username', 'profile_password', 'has_been_imported', 'import_data', 'import_date', 'profilesource']
#    edit_exclude_columns =[hide_list] # ['id', 'individual', 'import_address', 'profile_username', 'profile_password', 'has_been_imported', 'import_data', 'import_date', 'profilesource']
#
#    list_columns = ['id', 'individual', 'import_address', 'profile_username', 'profile_password', 'has_been_imported', 'import_data', 'import_date', 'profilesource']
#    list_exclude_columns = [] # ['id', 'individual', 'import_address', 'profile_username', 'profile_password', 'has_been_imported', 'import_data', 'import_date', 'profilesource']
#
#    search_columns = ['id', 'individual', 'import_address', 'profile_username', 'profile_password', 'has_been_imported', 'import_data', 'import_date', 'profilesource']
#    search_exclude_columns= [] # ['id', 'individual', 'import_address', 'profile_username', 'profile_password', 'has_been_imported', 'import_data', 'import_date', 'profilesource']
#
#    default_sort = [('id', True)]
#    base_permissions = ['can_list', 'can_show', 'can_edit', 'can_delete', 'can_add']
#    label_columns=   [{column.name: column.name for column in table.columns} ]
#    show_template =  'appbuilder/general/model/show_cascade.html'
#    list_template = 'appbuilder/general/model/list.html'
#    add_template = 'appbuilder/general/model/add.html'
#    edit_template = 'appbuilder/general/model/edit.html'
#    add_widget = (FormVerticalWidget|FormInlineWidget)
#    show_widget = ShowBlockWidget
#    list_widget = (ListThumbnail|ListWidget)
#    base_order = ('name', 'asc')
#    list_widget= 'list_widget'


class ProfileDetailView(ModelView):
    datamodel=SQLAInterface(Profile, db.session)
    related_views = []
    show_title='Profile Detail'
    add_title ='Add Profile'
    list_title= 'Profile List'
    edit_title = 'Edit Profile'
    show_columns = ['id', 'individual', 'import_address', 'profile_username', 'profile_password', 'has_been_imported', 'import_data', 'import_date', 'profilesource']
#    show_exclude_columns = [] #= ['id', 'individual', 'import_address', 'profile_username', 'profile_password', 'has_been_imported', 'import_data', 'import_date', 'profilesource']
#
#    add_columns = ['id', 'individual', 'import_address', 'profile_username', 'profile_password', 'has_been_imported', 'import_data', 'import_date', 'profilesource']
#    add_exclude_columns = [hide_list] #['id', 'individual', 'import_address', 'profile_username', 'profile_password', 'has_been_imported', 'import_data', 'import_date', 'profilesource']
#
#    edit_columns = ['id', 'individual', 'import_address', 'profile_username', 'profile_password', 'has_been_imported', 'import_data', 'import_date', 'profilesource']
#    edit_exclude_columns =[hide_list] # ['id', 'individual', 'import_address', 'profile_username', 'profile_password', 'has_been_imported', 'import_data', 'import_date', 'profilesource']
#
#    list_columns = ['id', 'individual', 'import_address', 'profile_username', 'profile_password', 'has_been_imported', 'import_data', 'import_date', 'profilesource']
#    list_exclude_columns = [] # ['id', 'individual', 'import_address', 'profile_username', 'profile_password', 'has_been_imported', 'import_data', 'import_date', 'profilesource']
#
#    search_columns = ['id', 'individual', 'import_address', 'profile_username', 'profile_password', 'has_been_imported', 'import_data', 'import_date', 'profilesource']
#    search_exclude_columns= [] # ['id', 'individual', 'import_address', 'profile_username', 'profile_password', 'has_been_imported', 'import_data', 'import_date', 'profilesource']
#
#    default_sort = [('id', True)]
#    base_permissions = ['can_list', 'can_show', 'can_edit', 'can_delete', 'can_add']
#    label_columns=   [{column.name: column.name for column in table.columns} ]
#    show_template =  'appbuilder/general/model/show_cascade.html'
#    list_template = 'appbuilder/general/model/list.html'
#    add_template = 'appbuilder/general/model/add.html'
#    edit_template = 'appbuilder/general/model/edit.html'
#    add_widget = (FormVerticalWidget|FormInlineWidget)
#    show_widget = ShowBlockWidget
#    list_widget = (ListThumbnail|ListWidget)
#    base_order = ('name', 'asc')
#    list_widget= 'list_widget'


class LocationDetailView(ModelView):
    datamodel=SQLAInterface(Location, db.session)
    related_views = []
    show_title='Location Detail'
    add_title ='Add Location'
    list_title= 'Location List'
    edit_title = 'Edit Location'
    show_columns = ['id', 'individual', 'template', 'header', 'color', 'location', 'summary_text', 'has_been_generated', 'preferred']
#    show_exclude_columns = [] #= ['id', 'individual', 'template', 'header', 'color', 'location', 'summary_text', 'has_been_generated', 'preferred']
#
#    add_columns = ['id', 'individual', 'template', 'header', 'color', 'location', 'summary_text', 'has_been_generated', 'preferred']
#    add_exclude_columns = [hide_list] #['id', 'individual', 'template', 'header', 'color', 'location', 'summary_text', 'has_been_generated', 'preferred']
#
#    edit_columns = ['id', 'individual', 'template', 'header', 'color', 'location', 'summary_text', 'has_been_generated', 'preferred']
#    edit_exclude_columns =[hide_list] # ['id', 'individual', 'template', 'header', 'color', 'location', 'summary_text', 'has_been_generated', 'preferred']
#
#    list_columns = ['id', 'individual', 'template', 'header', 'color', 'location', 'summary_text', 'has_been_generated', 'preferred']
#    list_exclude_columns = [] # ['id', 'individual', 'template', 'header', 'color', 'location', 'summary_text', 'has_been_generated', 'preferred']
#
#    search_columns = ['id', 'individual', 'template', 'header', 'color', 'location', 'summary_text', 'has_been_generated', 'preferred']
#    search_exclude_columns= [] # ['id', 'individual', 'template', 'header', 'color', 'location', 'summary_text', 'has_been_generated', 'preferred']
#
#    default_sort = [('id', True)]
#    base_permissions = ['can_list', 'can_show', 'can_edit', 'can_delete', 'can_add']
#    label_columns=   [{column.name: column.name for column in table.columns} ]
#    show_template =  'appbuilder/general/model/show_cascade.html'
#    list_template = 'appbuilder/general/model/list.html'
#    add_template = 'appbuilder/general/model/add.html'
#    edit_template = 'appbuilder/general/model/edit.html'
#    add_widget = (FormVerticalWidget|FormInlineWidget)
#    show_widget = ShowBlockWidget
#    list_widget = (ListThumbnail|ListWidget)
#    base_order = ('name', 'asc')
#    list_widget= 'list_widget'


class ResumeDetailView(ModelView):
    datamodel=SQLAInterface(Resume, db.session)
    related_views = []
    show_title='Resume Detail'
    add_title ='Add Resume'
    list_title= 'Resume List'
    edit_title = 'Edit Resume'
    show_columns = ['id', 'individual', 'template', 'header', 'color', 'location', 'summary_text', 'has_been_generated', 'preferred']
#    show_exclude_columns = [] #= ['id', 'individual', 'template', 'header', 'color', 'location', 'summary_text', 'has_been_generated', 'preferred']
#
#    add_columns = ['id', 'individual', 'template', 'header', 'color', 'location', 'summary_text', 'has_been_generated', 'preferred']
#    add_exclude_columns = [hide_list] #['id', 'individual', 'template', 'header', 'color', 'location', 'summary_text', 'has_been_generated', 'preferred']
#
#    edit_columns = ['id', 'individual', 'template', 'header', 'color', 'location', 'summary_text', 'has_been_generated', 'preferred']
#    edit_exclude_columns =[hide_list] # ['id', 'individual', 'template', 'header', 'color', 'location', 'summary_text', 'has_been_generated', 'preferred']
#
#    list_columns = ['id', 'individual', 'template', 'header', 'color', 'location', 'summary_text', 'has_been_generated', 'preferred']
#    list_exclude_columns = [] # ['id', 'individual', 'template', 'header', 'color', 'location', 'summary_text', 'has_been_generated', 'preferred']
#
#    search_columns = ['id', 'individual', 'template', 'header', 'color', 'location', 'summary_text', 'has_been_generated', 'preferred']
#    search_exclude_columns= [] # ['id', 'individual', 'template', 'header', 'color', 'location', 'summary_text', 'has_been_generated', 'preferred']
#
#    default_sort = [('id', True)]
#    base_permissions = ['can_list', 'can_show', 'can_edit', 'can_delete', 'can_add']
#    label_columns=   [{column.name: column.name for column in table.columns} ]
#    show_template =  'appbuilder/general/model/show_cascade.html'
#    list_template = 'appbuilder/general/model/list.html'
#    add_template = 'appbuilder/general/model/add.html'
#    edit_template = 'appbuilder/general/model/edit.html'
#    add_widget = (FormVerticalWidget|FormInlineWidget)
#    show_widget = ShowBlockWidget
#    list_widget = (ListThumbnail|ListWidget)
#    base_order = ('name', 'asc')
#    list_widget= 'list_widget'


class IndividualMasterView(MasterDetailView):
    datamodel=SQLAInterface(Individual, db.session)
    related_views = [UserxDetailView]
    show_title='Individual Detail'
    add_title ='Add Individual'
    list_title= 'Individual List'
    edit_title = 'Edit Individual'
    show_columns = ['id', 'userx', 'is_individual', 'is_institution', 'is_company', 'is_government', 'is_online']
#    show_exclude_columns = [] #= ['id', 'userx', 'is_individual', 'is_institution', 'is_company', 'is_government', 'is_online']
#
#    add_columns = ['id', 'userx', 'is_individual', 'is_institution', 'is_company', 'is_government', 'is_online']
#    add_exclude_columns = [hide_list] #['id', 'userx', 'is_individual', 'is_institution', 'is_company', 'is_government', 'is_online']
#
#    edit_columns = ['id', 'userx', 'is_individual', 'is_institution', 'is_company', 'is_government', 'is_online']
#    edit_exclude_columns =[hide_list] # ['id', 'userx', 'is_individual', 'is_institution', 'is_company', 'is_government', 'is_online']
#
#    list_columns = ['id', 'userx', 'is_individual', 'is_institution', 'is_company', 'is_government', 'is_online']
#    list_exclude_columns = [] # ['id', 'userx', 'is_individual', 'is_institution', 'is_company', 'is_government', 'is_online']
#
#    search_columns = ['id', 'userx', 'is_individual', 'is_institution', 'is_company', 'is_government', 'is_online']
#    search_exclude_columns= [] # ['id', 'userx', 'is_individual', 'is_institution', 'is_company', 'is_government', 'is_online']
#
#    default_sort = [('id', True)]
#    base_permissions = ['can_list', 'can_show', 'can_edit', 'can_delete', 'can_add']
#    label_columns=   [{column.name: column.name for column in table.columns} ]
#    show_template =  'appbuilder/general/model/show_cascade.html'
#    list_template = 'appbuilder/general/model/list.html'
#    add_template = 'appbuilder/general/model/add.html'
#    edit_template = 'appbuilder/general/model/edit.html'
#    add_widget = (FormVerticalWidget|FormInlineWidget)
#    show_widget = ShowBlockWidget
#    list_widget = (ListThumbnail|ListWidget)
#    base_order = ('name', 'asc')
#    list_widget= 'list_widget'


class IndustryJobMasterView(MasterDetailView):
    datamodel=SQLAInterface(IndustryJob, db.session)
    related_views = [IndustryDetailView]
    show_title='IndustryJob Detail'
    add_title ='Add IndustryJob'
    list_title= 'IndustryJob List'
    edit_title = 'Edit IndustryJob'
    show_columns = ['industry', 'job']
#    show_exclude_columns = [] #= ['industry', 'job']
#
#    add_columns = ['industry', 'job']
#    add_exclude_columns = [hide_list] #['industry', 'job']
#
#    edit_columns = ['industry', 'job']
#    edit_exclude_columns =[hide_list] # ['industry', 'job']
#
#    list_columns = ['industry', 'job']
#    list_exclude_columns = [] # ['industry', 'job']
#
#    search_columns = ['industry', 'job']
#    search_exclude_columns= [] # ['industry', 'job']
#
#    default_sort = [('id', True)]
#    base_permissions = ['can_list', 'can_show', 'can_edit', 'can_delete', 'can_add']
#    label_columns=   [{column.name: column.name for column in table.columns} ]
#    show_template =  'appbuilder/general/model/show_cascade.html'
#    list_template = 'appbuilder/general/model/list.html'
#    add_template = 'appbuilder/general/model/add.html'
#    edit_template = 'appbuilder/general/model/edit.html'
#    add_widget = (FormVerticalWidget|FormInlineWidget)
#    show_widget = ShowBlockWidget
#    list_widget = (ListThumbnail|ListWidget)
#    base_order = ('name', 'asc')
#    list_widget= 'list_widget'


class IndustryJobMultiView(MultipleView):
    datamodel=SQLAInterface(IndustryJob, db.session)
    views = [IndustryDetailView, JobDetailView]
    show_title='IndustryJob Detail'
    add_title ='Add IndustryJob'
    list_title= 'IndustryJob List'
    edit_title = 'Edit IndustryJob'
    show_columns = ['industry', 'job']
#    show_exclude_columns = [] #= ['industry', 'job']
#
#    add_columns = ['industry', 'job']
#    add_exclude_columns = [hide_list] #['industry', 'job']
#
#    edit_columns = ['industry', 'job']
#    edit_exclude_columns =[hide_list] # ['industry', 'job']
#
#    list_columns = ['industry', 'job']
#    list_exclude_columns = [] # ['industry', 'job']
#
#    search_columns = ['industry', 'job']
#    search_exclude_columns= [] # ['industry', 'job']
#
#    default_sort = [('id', True)]
#    base_permissions = ['can_list', 'can_show', 'can_edit', 'can_delete', 'can_add']
#    label_columns=   [{column.name: column.name for column in table.columns} ]
#    show_template =  'appbuilder/general/model/show_cascade.html'
#    list_template = 'appbuilder/general/model/list.html'
#    add_template = 'appbuilder/general/model/add.html'
#    edit_template = 'appbuilder/general/model/edit.html'
#    add_widget = (FormVerticalWidget|FormInlineWidget)
#    show_widget = ShowBlockWidget
#    list_widget = (ListThumbnail|ListWidget)
#    base_order = ('name', 'asc')
#    list_widget= 'list_widget'


class JobSkillMasterView(MasterDetailView):
    datamodel=SQLAInterface(JobSkill, db.session)
    related_views = [JobDetailView]
    show_title='JobSkill Detail'
    add_title ='Add JobSkill'
    list_title= 'JobSkill List'
    edit_title = 'Edit JobSkill'
    show_columns = ['skills', 'jobs']
#    show_exclude_columns = [] #= ['skills', 'jobs']
#
#    add_columns = ['skills', 'jobs']
#    add_exclude_columns = [hide_list] #['skills', 'jobs']
#
#    edit_columns = ['skills', 'jobs']
#    edit_exclude_columns =[hide_list] # ['skills', 'jobs']
#
#    list_columns = ['skills', 'jobs']
#    list_exclude_columns = [] # ['skills', 'jobs']
#
#    search_columns = ['skills', 'jobs']
#    search_exclude_columns= [] # ['skills', 'jobs']
#
#    default_sort = [('id', True)]
#    base_permissions = ['can_list', 'can_show', 'can_edit', 'can_delete', 'can_add']
#    label_columns=   [{column.name: column.name for column in table.columns} ]
#    show_template =  'appbuilder/general/model/show_cascade.html'
#    list_template = 'appbuilder/general/model/list.html'
#    add_template = 'appbuilder/general/model/add.html'
#    edit_template = 'appbuilder/general/model/edit.html'
#    add_widget = (FormVerticalWidget|FormInlineWidget)
#    show_widget = ShowBlockWidget
#    list_widget = (ListThumbnail|ListWidget)
#    base_order = ('name', 'asc')
#    list_widget= 'list_widget'


class JobSkillMultiView(MultipleView):
    datamodel=SQLAInterface(JobSkill, db.session)
    views = [SkillDetailView]
    show_title='JobSkill Detail'
    add_title ='Add JobSkill'
    list_title= 'JobSkill List'
    edit_title = 'Edit JobSkill'
    show_columns = ['skills', 'jobs']
#    show_exclude_columns = [] #= ['skills', 'jobs']
#
#    add_columns = ['skills', 'jobs']
#    add_exclude_columns = [hide_list] #['skills', 'jobs']
#
#    edit_columns = ['skills', 'jobs']
#    edit_exclude_columns =[hide_list] # ['skills', 'jobs']
#
#    list_columns = ['skills', 'jobs']
#    list_exclude_columns = [] # ['skills', 'jobs']
#
#    search_columns = ['skills', 'jobs']
#    search_exclude_columns= [] # ['skills', 'jobs']
#
#    default_sort = [('id', True)]
#    base_permissions = ['can_list', 'can_show', 'can_edit', 'can_delete', 'can_add']
#    label_columns=   [{column.name: column.name for column in table.columns} ]
#    show_template =  'appbuilder/general/model/show_cascade.html'
#    list_template = 'appbuilder/general/model/list.html'
#    add_template = 'appbuilder/general/model/add.html'
#    edit_template = 'appbuilder/general/model/edit.html'
#    add_widget = (FormVerticalWidget|FormInlineWidget)
#    show_widget = ShowBlockWidget
#    list_widget = (ListThumbnail|ListWidget)
#    base_order = ('name', 'asc')
#    list_widget= 'list_widget'


class EducationMasterView(MasterDetailView):
    datamodel=SQLAInterface(Education, db.session)
    related_views = [IndividualDetailView]
    show_title='Education Detail'
    add_title ='Add Education'
    list_title= 'Education List'
    edit_title = 'Edit Education'
    show_columns = ['id', 'individual', 'qualification', 'qual_class', 'verified', 'verification_code', 'verified_by', 'verification_date', 'verification_doc']
#    show_exclude_columns = [] #= ['id', 'individual', 'qualification', 'qual_class', 'verified', 'verification_code', 'verified_by', 'verification_date', 'verification_doc']
#
#    add_columns = ['id', 'individual', 'qualification', 'qual_class', 'verified', 'verification_code', 'verified_by', 'verification_date', 'verification_doc']
#    add_exclude_columns = [hide_list] #['id', 'individual', 'qualification', 'qual_class', 'verified', 'verification_code', 'verified_by', 'verification_date', 'verification_doc']
#
#    edit_columns = ['id', 'individual', 'qualification', 'qual_class', 'verified', 'verification_code', 'verified_by', 'verification_date', 'verification_doc']
#    edit_exclude_columns =[hide_list] # ['id', 'individual', 'qualification', 'qual_class', 'verified', 'verification_code', 'verified_by', 'verification_date', 'verification_doc']
#
#    list_columns = ['id', 'individual', 'qualification', 'qual_class', 'verified', 'verification_code', 'verified_by', 'verification_date', 'verification_doc']
#    list_exclude_columns = [] # ['id', 'individual', 'qualification', 'qual_class', 'verified', 'verification_code', 'verified_by', 'verification_date', 'verification_doc']
#
#    search_columns = ['id', 'individual', 'qualification', 'qual_class', 'verified', 'verification_code', 'verified_by', 'verification_date', 'verification_doc']
#    search_exclude_columns= [] # ['id', 'individual', 'qualification', 'qual_class', 'verified', 'verification_code', 'verified_by', 'verification_date', 'verification_doc']
#
#    default_sort = [('id', True)]
#    base_permissions = ['can_list', 'can_show', 'can_edit', 'can_delete', 'can_add']
#    label_columns=   [{column.name: column.name for column in table.columns} ]
#    show_template =  'appbuilder/general/model/show_cascade.html'
#    list_template = 'appbuilder/general/model/list.html'
#    add_template = 'appbuilder/general/model/add.html'
#    edit_template = 'appbuilder/general/model/edit.html'
#    add_widget = (FormVerticalWidget|FormInlineWidget)
#    show_widget = ShowBlockWidget
#    list_widget = (ListThumbnail|ListWidget)
#    base_order = ('name', 'asc')
#    list_widget= 'list_widget'


class IndividualJobMasterView(MasterDetailView):
    datamodel=SQLAInterface(IndividualJob, db.session)
    related_views = [IndividualDetailView]
    show_title='IndividualJob Detail'
    add_title ='Add IndividualJob'
    list_title= 'IndividualJob List'
    edit_title = 'Edit IndividualJob'
    show_columns = ['individual', 'job']
#    show_exclude_columns = [] #= ['individual', 'job']
#
#    add_columns = ['individual', 'job']
#    add_exclude_columns = [hide_list] #['individual', 'job']
#
#    edit_columns = ['individual', 'job']
#    edit_exclude_columns =[hide_list] # ['individual', 'job']
#
#    list_columns = ['individual', 'job']
#    list_exclude_columns = [] # ['individual', 'job']
#
#    search_columns = ['individual', 'job']
#    search_exclude_columns= [] # ['individual', 'job']
#
#    default_sort = [('id', True)]
#    base_permissions = ['can_list', 'can_show', 'can_edit', 'can_delete', 'can_add']
#    label_columns=   [{column.name: column.name for column in table.columns} ]
#    show_template =  'appbuilder/general/model/show_cascade.html'
#    list_template = 'appbuilder/general/model/list.html'
#    add_template = 'appbuilder/general/model/add.html'
#    edit_template = 'appbuilder/general/model/edit.html'
#    add_widget = (FormVerticalWidget|FormInlineWidget)
#    show_widget = ShowBlockWidget
#    list_widget = (ListThumbnail|ListWidget)
#    base_order = ('name', 'asc')
#    list_widget= 'list_widget'


class IndividualJobMultiView(MultipleView):
    datamodel=SQLAInterface(IndividualJob, db.session)
    views = []
    show_title='IndividualJob Detail'
    add_title ='Add IndividualJob'
    list_title= 'IndividualJob List'
    edit_title = 'Edit IndividualJob'
    show_columns = ['individual', 'job']
#    show_exclude_columns = [] #= ['individual', 'job']
#
#    add_columns = ['individual', 'job']
#    add_exclude_columns = [hide_list] #['individual', 'job']
#
#    edit_columns = ['individual', 'job']
#    edit_exclude_columns =[hide_list] # ['individual', 'job']
#
#    list_columns = ['individual', 'job']
#    list_exclude_columns = [] # ['individual', 'job']
#
#    search_columns = ['individual', 'job']
#    search_exclude_columns= [] # ['individual', 'job']
#
#    default_sort = [('id', True)]
#    base_permissions = ['can_list', 'can_show', 'can_edit', 'can_delete', 'can_add']
#    label_columns=   [{column.name: column.name for column in table.columns} ]
#    show_template =  'appbuilder/general/model/show_cascade.html'
#    list_template = 'appbuilder/general/model/list.html'
#    add_template = 'appbuilder/general/model/add.html'
#    edit_template = 'appbuilder/general/model/edit.html'
#    add_widget = (FormVerticalWidget|FormInlineWidget)
#    show_widget = ShowBlockWidget
#    list_widget = (ListThumbnail|ListWidget)
#    base_order = ('name', 'asc')
#    list_widget= 'list_widget'


class LocationMasterView(MasterDetailView):
    datamodel=SQLAInterface(Location, db.session)
    related_views = [IndividualDetailView]
    show_title='Location Detail'
    add_title ='Add Location'
    list_title= 'Location List'
    edit_title = 'Edit Location'
    show_columns = ['id', 'individual']
#    show_exclude_columns = [] #= ['id', 'individual']
#
#    add_columns = ['id', 'individual']
#    add_exclude_columns = [hide_list] #['id', 'individual']
#
#    edit_columns = ['id', 'individual']
#    edit_exclude_columns =[hide_list] # ['id', 'individual']
#
#    list_columns = ['id', 'individual']
#    list_exclude_columns = [] # ['id', 'individual']
#
#    search_columns = ['id', 'individual']
#    search_exclude_columns= [] # ['id', 'individual']
#
#    default_sort = [('id', True)]
#    base_permissions = ['can_list', 'can_show', 'can_edit', 'can_delete', 'can_add']
#    label_columns=   [{column.name: column.name for column in table.columns} ]
#    show_template =  'appbuilder/general/model/show_cascade.html'
#    list_template = 'appbuilder/general/model/list.html'
#    add_template = 'appbuilder/general/model/add.html'
#    edit_template = 'appbuilder/general/model/edit.html'
#    add_widget = (FormVerticalWidget|FormInlineWidget)
#    show_widget = ShowBlockWidget
#    list_widget = (ListThumbnail|ListWidget)
#    base_order = ('name', 'asc')
#    list_widget= 'list_widget'


class PortalMasterView(MasterDetailView):
    datamodel=SQLAInterface(Portal, db.session)
    related_views = [IndividualDetailView]
    show_title='Portal Detail'
    add_title ='Add Portal'
    list_title= 'Portal List'
    edit_title = 'Edit Portal'
    show_columns = ['id', 'portal_url', 'is_primary', 'portal_state', 'individual', 'has_custom_domain', 'domain', 'header_text', 'slug', 'automatic_fulfillment_digital_products', 'default_digital_max_downloads', 'default_digital_url_valid_days', 'default_mail_sender_name', 'default_mail_sender_address', 'fulfillment_auto_approve', 'fulfillment_allow_unpaid', 'reserve_stock_duration_anonymous_user', 'reserve_stock_duration_authenticated_user', 'limit_quantity_per_checkout', 'gift_card_expiry_type', 'gift_card_expiry_period_type', 'gift_card_expiry_period', 'charge_taxes_on_shipping', 'include_taxes_in_prices', 'display_gross_prices', 'language']
#    show_exclude_columns = [] #= ['id', 'portal_url', 'is_primary', 'portal_state', 'individual', 'has_custom_domain', 'domain', 'header_text', 'slug', 'automatic_fulfillment_digital_products', 'default_digital_max_downloads', 'default_digital_url_valid_days', 'default_mail_sender_name', 'default_mail_sender_address', 'fulfillment_auto_approve', 'fulfillment_allow_unpaid', 'reserve_stock_duration_anonymous_user', 'reserve_stock_duration_authenticated_user', 'limit_quantity_per_checkout', 'gift_card_expiry_type', 'gift_card_expiry_period_type', 'gift_card_expiry_period', 'charge_taxes_on_shipping', 'include_taxes_in_prices', 'display_gross_prices', 'language']
#
#    add_columns = ['id', 'portal_url', 'is_primary', 'portal_state', 'individual', 'has_custom_domain', 'domain', 'header_text', 'slug', 'automatic_fulfillment_digital_products', 'default_digital_max_downloads', 'default_digital_url_valid_days', 'default_mail_sender_name', 'default_mail_sender_address', 'fulfillment_auto_approve', 'fulfillment_allow_unpaid', 'reserve_stock_duration_anonymous_user', 'reserve_stock_duration_authenticated_user', 'limit_quantity_per_checkout', 'gift_card_expiry_type', 'gift_card_expiry_period_type', 'gift_card_expiry_period', 'charge_taxes_on_shipping', 'include_taxes_in_prices', 'display_gross_prices', 'language']
#    add_exclude_columns = [hide_list] #['id', 'portal_url', 'is_primary', 'portal_state', 'individual', 'has_custom_domain', 'domain', 'header_text', 'slug', 'automatic_fulfillment_digital_products', 'default_digital_max_downloads', 'default_digital_url_valid_days', 'default_mail_sender_name', 'default_mail_sender_address', 'fulfillment_auto_approve', 'fulfillment_allow_unpaid', 'reserve_stock_duration_anonymous_user', 'reserve_stock_duration_authenticated_user', 'limit_quantity_per_checkout', 'gift_card_expiry_type', 'gift_card_expiry_period_type', 'gift_card_expiry_period', 'charge_taxes_on_shipping', 'include_taxes_in_prices', 'display_gross_prices', 'language']
#
#    edit_columns = ['id', 'portal_url', 'is_primary', 'portal_state', 'individual', 'has_custom_domain', 'domain', 'header_text', 'slug', 'automatic_fulfillment_digital_products', 'default_digital_max_downloads', 'default_digital_url_valid_days', 'default_mail_sender_name', 'default_mail_sender_address', 'fulfillment_auto_approve', 'fulfillment_allow_unpaid', 'reserve_stock_duration_anonymous_user', 'reserve_stock_duration_authenticated_user', 'limit_quantity_per_checkout', 'gift_card_expiry_type', 'gift_card_expiry_period_type', 'gift_card_expiry_period', 'charge_taxes_on_shipping', 'include_taxes_in_prices', 'display_gross_prices', 'language']
#    edit_exclude_columns =[hide_list] # ['id', 'portal_url', 'is_primary', 'portal_state', 'individual', 'has_custom_domain', 'domain', 'header_text', 'slug', 'automatic_fulfillment_digital_products', 'default_digital_max_downloads', 'default_digital_url_valid_days', 'default_mail_sender_name', 'default_mail_sender_address', 'fulfillment_auto_approve', 'fulfillment_allow_unpaid', 'reserve_stock_duration_anonymous_user', 'reserve_stock_duration_authenticated_user', 'limit_quantity_per_checkout', 'gift_card_expiry_type', 'gift_card_expiry_period_type', 'gift_card_expiry_period', 'charge_taxes_on_shipping', 'include_taxes_in_prices', 'display_gross_prices', 'language']
#
#    list_columns = ['id', 'portal_url', 'is_primary', 'portal_state', 'individual', 'has_custom_domain', 'domain', 'header_text', 'slug', 'automatic_fulfillment_digital_products', 'default_digital_max_downloads', 'default_digital_url_valid_days', 'default_mail_sender_name', 'default_mail_sender_address', 'fulfillment_auto_approve', 'fulfillment_allow_unpaid', 'reserve_stock_duration_anonymous_user', 'reserve_stock_duration_authenticated_user', 'limit_quantity_per_checkout', 'gift_card_expiry_type', 'gift_card_expiry_period_type', 'gift_card_expiry_period', 'charge_taxes_on_shipping', 'include_taxes_in_prices', 'display_gross_prices', 'language']
#    list_exclude_columns = [] # ['id', 'portal_url', 'is_primary', 'portal_state', 'individual', 'has_custom_domain', 'domain', 'header_text', 'slug', 'automatic_fulfillment_digital_products', 'default_digital_max_downloads', 'default_digital_url_valid_days', 'default_mail_sender_name', 'default_mail_sender_address', 'fulfillment_auto_approve', 'fulfillment_allow_unpaid', 'reserve_stock_duration_anonymous_user', 'reserve_stock_duration_authenticated_user', 'limit_quantity_per_checkout', 'gift_card_expiry_type', 'gift_card_expiry_period_type', 'gift_card_expiry_period', 'charge_taxes_on_shipping', 'include_taxes_in_prices', 'display_gross_prices', 'language']
#
#    search_columns = ['id', 'portal_url', 'is_primary', 'portal_state', 'individual', 'has_custom_domain', 'domain', 'header_text', 'slug', 'automatic_fulfillment_digital_products', 'default_digital_max_downloads', 'default_digital_url_valid_days', 'default_mail_sender_name', 'default_mail_sender_address', 'fulfillment_auto_approve', 'fulfillment_allow_unpaid', 'reserve_stock_duration_anonymous_user', 'reserve_stock_duration_authenticated_user', 'limit_quantity_per_checkout', 'gift_card_expiry_type', 'gift_card_expiry_period_type', 'gift_card_expiry_period', 'charge_taxes_on_shipping', 'include_taxes_in_prices', 'display_gross_prices', 'language']
#    search_exclude_columns= [] # ['id', 'portal_url', 'is_primary', 'portal_state', 'individual', 'has_custom_domain', 'domain', 'header_text', 'slug', 'automatic_fulfillment_digital_products', 'default_digital_max_downloads', 'default_digital_url_valid_days', 'default_mail_sender_name', 'default_mail_sender_address', 'fulfillment_auto_approve', 'fulfillment_allow_unpaid', 'reserve_stock_duration_anonymous_user', 'reserve_stock_duration_authenticated_user', 'limit_quantity_per_checkout', 'gift_card_expiry_type', 'gift_card_expiry_period_type', 'gift_card_expiry_period', 'charge_taxes_on_shipping', 'include_taxes_in_prices', 'display_gross_prices', 'language']
#
#    default_sort = [('id', True)]
#    base_permissions = ['can_list', 'can_show', 'can_edit', 'can_delete', 'can_add']
#    label_columns=   [{column.name: column.name for column in table.columns} ]
#    show_template =  'appbuilder/general/model/show_cascade.html'
#    list_template = 'appbuilder/general/model/list.html'
#    add_template = 'appbuilder/general/model/add.html'
#    edit_template = 'appbuilder/general/model/edit.html'
#    add_widget = (FormVerticalWidget|FormInlineWidget)
#    show_widget = ShowBlockWidget
#    list_widget = (ListThumbnail|ListWidget)
#    base_order = ('name', 'asc')
#    list_widget= 'list_widget'


class PageMasterView(MasterDetailView):
    datamodel=SQLAInterface(Page, db.session)
    related_views = [PortalDetailView]
    show_title='Page Detail'
    add_title ='Add Page'
    list_title= 'Page List'
    edit_title = 'Edit Page'
    show_columns = ['id', 'portal', 'header', 'slug', 'page_type']
#    show_exclude_columns = [] #= ['id', 'portal', 'header', 'slug', 'page_type']
#
#    add_columns = ['id', 'portal', 'header', 'slug', 'page_type']
#    add_exclude_columns = [hide_list] #['id', 'portal', 'header', 'slug', 'page_type']
#
#    edit_columns = ['id', 'portal', 'header', 'slug', 'page_type']
#    edit_exclude_columns =[hide_list] # ['id', 'portal', 'header', 'slug', 'page_type']
#
#    list_columns = ['id', 'portal', 'header', 'slug', 'page_type']
#    list_exclude_columns = [] # ['id', 'portal', 'header', 'slug', 'page_type']
#
#    search_columns = ['id', 'portal', 'header', 'slug', 'page_type']
#    search_exclude_columns= [] # ['id', 'portal', 'header', 'slug', 'page_type']
#
#    default_sort = [('id', True)]
#    base_permissions = ['can_list', 'can_show', 'can_edit', 'can_delete', 'can_add']
#    label_columns=   [{column.name: column.name for column in table.columns} ]
#    show_template =  'appbuilder/general/model/show_cascade.html'
#    list_template = 'appbuilder/general/model/list.html'
#    add_template = 'appbuilder/general/model/add.html'
#    edit_template = 'appbuilder/general/model/edit.html'
#    add_widget = (FormVerticalWidget|FormInlineWidget)
#    show_widget = ShowBlockWidget
#    list_widget = (ListThumbnail|ListWidget)
#    base_order = ('name', 'asc')
#    list_widget= 'list_widget'


class ProfileMasterView(MasterDetailView):
    datamodel=SQLAInterface(Profile, db.session)
    related_views = [IndividualDetailView]
    show_title='Profile Detail'
    add_title ='Add Profile'
    list_title= 'Profile List'
    edit_title = 'Edit Profile'
    show_columns = ['id', 'individual', 'import_address', 'profile_username', 'profile_password', 'has_been_imported', 'import_data', 'import_date', 'profilesource']
#    show_exclude_columns = [] #= ['id', 'individual', 'import_address', 'profile_username', 'profile_password', 'has_been_imported', 'import_data', 'import_date', 'profilesource']
#
#    add_columns = ['id', 'individual', 'import_address', 'profile_username', 'profile_password', 'has_been_imported', 'import_data', 'import_date', 'profilesource']
#    add_exclude_columns = [hide_list] #['id', 'individual', 'import_address', 'profile_username', 'profile_password', 'has_been_imported', 'import_data', 'import_date', 'profilesource']
#
#    edit_columns = ['id', 'individual', 'import_address', 'profile_username', 'profile_password', 'has_been_imported', 'import_data', 'import_date', 'profilesource']
#    edit_exclude_columns =[hide_list] # ['id', 'individual', 'import_address', 'profile_username', 'profile_password', 'has_been_imported', 'import_data', 'import_date', 'profilesource']
#
#    list_columns = ['id', 'individual', 'import_address', 'profile_username', 'profile_password', 'has_been_imported', 'import_data', 'import_date', 'profilesource']
#    list_exclude_columns = [] # ['id', 'individual', 'import_address', 'profile_username', 'profile_password', 'has_been_imported', 'import_data', 'import_date', 'profilesource']
#
#    search_columns = ['id', 'individual', 'import_address', 'profile_username', 'profile_password', 'has_been_imported', 'import_data', 'import_date', 'profilesource']
#    search_exclude_columns= [] # ['id', 'individual', 'import_address', 'profile_username', 'profile_password', 'has_been_imported', 'import_data', 'import_date', 'profilesource']
#
#    default_sort = [('id', True)]
#    base_permissions = ['can_list', 'can_show', 'can_edit', 'can_delete', 'can_add']
#    label_columns=   [{column.name: column.name for column in table.columns} ]
#    show_template =  'appbuilder/general/model/show_cascade.html'
#    list_template = 'appbuilder/general/model/list.html'
#    add_template = 'appbuilder/general/model/add.html'
#    edit_template = 'appbuilder/general/model/edit.html'
#    add_widget = (FormVerticalWidget|FormInlineWidget)
#    show_widget = ShowBlockWidget
#    list_widget = (ListThumbnail|ListWidget)
#    base_order = ('name', 'asc')
#    list_widget= 'list_widget'


class ProfileMultiView(MultipleView):
    datamodel=SQLAInterface(Profile, db.session)
    views = [ProfilesourceDetailView]
    show_title='Profile Detail'
    add_title ='Add Profile'
    list_title= 'Profile List'
    edit_title = 'Edit Profile'
    show_columns = ['id', 'individual', 'import_address', 'profile_username', 'profile_password', 'has_been_imported', 'import_data', 'import_date', 'profilesource']
#    show_exclude_columns = [] #= ['id', 'individual', 'import_address', 'profile_username', 'profile_password', 'has_been_imported', 'import_data', 'import_date', 'profilesource']
#
#    add_columns = ['id', 'individual', 'import_address', 'profile_username', 'profile_password', 'has_been_imported', 'import_data', 'import_date', 'profilesource']
#    add_exclude_columns = [hide_list] #['id', 'individual', 'import_address', 'profile_username', 'profile_password', 'has_been_imported', 'import_data', 'import_date', 'profilesource']
#
#    edit_columns = ['id', 'individual', 'import_address', 'profile_username', 'profile_password', 'has_been_imported', 'import_data', 'import_date', 'profilesource']
#    edit_exclude_columns =[hide_list] # ['id', 'individual', 'import_address', 'profile_username', 'profile_password', 'has_been_imported', 'import_data', 'import_date', 'profilesource']
#
#    list_columns = ['id', 'individual', 'import_address', 'profile_username', 'profile_password', 'has_been_imported', 'import_data', 'import_date', 'profilesource']
#    list_exclude_columns = [] # ['id', 'individual', 'import_address', 'profile_username', 'profile_password', 'has_been_imported', 'import_data', 'import_date', 'profilesource']
#
#    search_columns = ['id', 'individual', 'import_address', 'profile_username', 'profile_password', 'has_been_imported', 'import_data', 'import_date', 'profilesource']
#    search_exclude_columns= [] # ['id', 'individual', 'import_address', 'profile_username', 'profile_password', 'has_been_imported', 'import_data', 'import_date', 'profilesource']
#
#    default_sort = [('id', True)]
#    base_permissions = ['can_list', 'can_show', 'can_edit', 'can_delete', 'can_add']
#    label_columns=   [{column.name: column.name for column in table.columns} ]
#    show_template =  'appbuilder/general/model/show_cascade.html'
#    list_template = 'appbuilder/general/model/list.html'
#    add_template = 'appbuilder/general/model/add.html'
#    edit_template = 'appbuilder/general/model/edit.html'
#    add_widget = (FormVerticalWidget|FormInlineWidget)
#    show_widget = ShowBlockWidget
#    list_widget = (ListThumbnail|ListWidget)
#    base_order = ('name', 'asc')
#    list_widget= 'list_widget'


class ResumeMasterView(MasterDetailView):
    datamodel=SQLAInterface(Resume, db.session)
    related_views = [IndividualDetailView]
    show_title='Resume Detail'
    add_title ='Add Resume'
    list_title= 'Resume List'
    edit_title = 'Edit Resume'
    show_columns = ['id', 'individual', 'template', 'header', 'color', 'location', 'summary_text', 'has_been_generated', 'preferred']
#    show_exclude_columns = [] #= ['id', 'individual', 'template', 'header', 'color', 'location', 'summary_text', 'has_been_generated', 'preferred']
#
#    add_columns = ['id', 'individual', 'template', 'header', 'color', 'location', 'summary_text', 'has_been_generated', 'preferred']
#    add_exclude_columns = [hide_list] #['id', 'individual', 'template', 'header', 'color', 'location', 'summary_text', 'has_been_generated', 'preferred']
#
#    edit_columns = ['id', 'individual', 'template', 'header', 'color', 'location', 'summary_text', 'has_been_generated', 'preferred']
#    edit_exclude_columns =[hide_list] # ['id', 'individual', 'template', 'header', 'color', 'location', 'summary_text', 'has_been_generated', 'preferred']
#
#    list_columns = ['id', 'individual', 'template', 'header', 'color', 'location', 'summary_text', 'has_been_generated', 'preferred']
#    list_exclude_columns = [] # ['id', 'individual', 'template', 'header', 'color', 'location', 'summary_text', 'has_been_generated', 'preferred']
#
#    search_columns = ['id', 'individual', 'template', 'header', 'color', 'location', 'summary_text', 'has_been_generated', 'preferred']
#    search_exclude_columns= [] # ['id', 'individual', 'template', 'header', 'color', 'location', 'summary_text', 'has_been_generated', 'preferred']
#
#    default_sort = [('id', True)]
#    base_permissions = ['can_list', 'can_show', 'can_edit', 'can_delete', 'can_add']
#    label_columns=   [{column.name: column.name for column in table.columns} ]
#    show_template =  'appbuilder/general/model/show_cascade.html'
#    list_template = 'appbuilder/general/model/list.html'
#    add_template = 'appbuilder/general/model/add.html'
#    edit_template = 'appbuilder/general/model/edit.html'
#    add_widget = (FormVerticalWidget|FormInlineWidget)
#    show_widget = ShowBlockWidget
#    list_widget = (ListThumbnail|ListWidget)
#    base_order = ('name', 'asc')
#    list_widget= 'list_widget'


class ResumeMultiView(MultipleView):
    datamodel=SQLAInterface(Resume, db.session)
    views = [LocationDetailView]
    show_title='Resume Detail'
    add_title ='Add Resume'
    list_title= 'Resume List'
    edit_title = 'Edit Resume'
    show_columns = ['id', 'individual', 'template', 'header', 'color', 'location', 'summary_text', 'has_been_generated', 'preferred']
#    show_exclude_columns = [] #= ['id', 'individual', 'template', 'header', 'color', 'location', 'summary_text', 'has_been_generated', 'preferred']
#
#    add_columns = ['id', 'individual', 'template', 'header', 'color', 'location', 'summary_text', 'has_been_generated', 'preferred']
#    add_exclude_columns = [hide_list] #['id', 'individual', 'template', 'header', 'color', 'location', 'summary_text', 'has_been_generated', 'preferred']
#
#    edit_columns = ['id', 'individual', 'template', 'header', 'color', 'location', 'summary_text', 'has_been_generated', 'preferred']
#    edit_exclude_columns =[hide_list] # ['id', 'individual', 'template', 'header', 'color', 'location', 'summary_text', 'has_been_generated', 'preferred']
#
#    list_columns = ['id', 'individual', 'template', 'header', 'color', 'location', 'summary_text', 'has_been_generated', 'preferred']
#    list_exclude_columns = [] # ['id', 'individual', 'template', 'header', 'color', 'location', 'summary_text', 'has_been_generated', 'preferred']
#
#    search_columns = ['id', 'individual', 'template', 'header', 'color', 'location', 'summary_text', 'has_been_generated', 'preferred']
#    search_exclude_columns= [] # ['id', 'individual', 'template', 'header', 'color', 'location', 'summary_text', 'has_been_generated', 'preferred']
#
#    default_sort = [('id', True)]
#    base_permissions = ['can_list', 'can_show', 'can_edit', 'can_delete', 'can_add']
#    label_columns=   [{column.name: column.name for column in table.columns} ]
#    show_template =  'appbuilder/general/model/show_cascade.html'
#    list_template = 'appbuilder/general/model/list.html'
#    add_template = 'appbuilder/general/model/add.html'
#    edit_template = 'appbuilder/general/model/edit.html'
#    add_widget = (FormVerticalWidget|FormInlineWidget)
#    show_widget = ShowBlockWidget
#    list_widget = (ListThumbnail|ListWidget)
#    base_order = ('name', 'asc')
#    list_widget= 'list_widget'


class SwarmMasterView(MasterDetailView):
    datamodel=SQLAInterface(Swarm, db.session)
    related_views = [PortalDetailView]
    show_title='Swarm Detail'
    add_title ='Add Swarm'
    list_title= 'Swarm List'
    edit_title = 'Edit Swarm'
    show_columns = ['id', 'portal']
#    show_exclude_columns = [] #= ['id', 'portal']
#
#    add_columns = ['id', 'portal']
#    add_exclude_columns = [hide_list] #['id', 'portal']
#
#    edit_columns = ['id', 'portal']
#    edit_exclude_columns =[hide_list] # ['id', 'portal']
#
#    list_columns = ['id', 'portal']
#    list_exclude_columns = [] # ['id', 'portal']
#
#    search_columns = ['id', 'portal']
#    search_exclude_columns= [] # ['id', 'portal']
#
#    default_sort = [('id', True)]
#    base_permissions = ['can_list', 'can_show', 'can_edit', 'can_delete', 'can_add']
#    label_columns=   [{column.name: column.name for column in table.columns} ]
#    show_template =  'appbuilder/general/model/show_cascade.html'
#    list_template = 'appbuilder/general/model/list.html'
#    add_template = 'appbuilder/general/model/add.html'
#    edit_template = 'appbuilder/general/model/edit.html'
#    add_widget = (FormVerticalWidget|FormInlineWidget)
#    show_widget = ShowBlockWidget
#    list_widget = (ListThumbnail|ListWidget)
#    base_order = ('name', 'asc')
#    list_widget= 'list_widget'


class IndividualSwarmView(ModelView):
    datamodel=SQLAInterface(IndividualSwarm, db.session)
    related_views = []
    show_title='IndividualSwarm Detail'
    add_title ='Add IndividualSwarm'
    list_title= 'IndividualSwarm List'
    edit_title = 'Edit IndividualSwarm'
    show_columns = ['individual', 'swarm']
#    show_exclude_columns = [] #= ['individual', 'swarm']
#
#    add_columns = ['individual', 'swarm']
#    add_exclude_columns = [hide_list] #['individual', 'swarm']
#
#    edit_columns = ['individual', 'swarm']
#    edit_exclude_columns =[hide_list] # ['individual', 'swarm']
#
#    list_columns = ['individual', 'swarm']
#    list_exclude_columns = [] # ['individual', 'swarm']
#
#    search_columns = ['individual', 'swarm']
#    search_exclude_columns= [] # ['individual', 'swarm']
#
#    default_sort = [('id', True)]
#    base_permissions = ['can_list', 'can_show', 'can_edit', 'can_delete', 'can_add']
#    label_columns=   [{column.name: column.name for column in table.columns} ]
#    show_template =  'appbuilder/general/model/show_cascade.html'
#    list_template = 'appbuilder/general/model/list.html'
#    add_template = 'appbuilder/general/model/add.html'
#    edit_template = 'appbuilder/general/model/edit.html'
#    add_widget = (FormVerticalWidget|FormInlineWidget)
#    show_widget = ShowBlockWidget
#    list_widget = (ListThumbnail|ListWidget)
#    base_order = ('name', 'asc')
#    list_widget= 'list_widget'


class UserxDetailView(ModelView):
    datamodel=SQLAInterface(Userx, db.session)
    related_views = []
    show_title='Userx Detail'
    add_title ='Add Userx'
    list_title= 'Userx List'
    edit_title = 'Edit Userx'
    show_columns = ['id', 'userx', 'is_individual', 'is_institution', 'is_company', 'is_government', 'is_online']
#    show_exclude_columns = [] #= ['id', 'userx', 'is_individual', 'is_institution', 'is_company', 'is_government', 'is_online']
#
#    add_columns = ['id', 'userx', 'is_individual', 'is_institution', 'is_company', 'is_government', 'is_online']
#    add_exclude_columns = [hide_list] #['id', 'userx', 'is_individual', 'is_institution', 'is_company', 'is_government', 'is_online']
#
#    edit_columns = ['id', 'userx', 'is_individual', 'is_institution', 'is_company', 'is_government', 'is_online']
#    edit_exclude_columns =[hide_list] # ['id', 'userx', 'is_individual', 'is_institution', 'is_company', 'is_government', 'is_online']
#
#    list_columns = ['id', 'userx', 'is_individual', 'is_institution', 'is_company', 'is_government', 'is_online']
#    list_exclude_columns = [] # ['id', 'userx', 'is_individual', 'is_institution', 'is_company', 'is_government', 'is_online']
#
#    search_columns = ['id', 'userx', 'is_individual', 'is_institution', 'is_company', 'is_government', 'is_online']
#    search_exclude_columns= [] # ['id', 'userx', 'is_individual', 'is_institution', 'is_company', 'is_government', 'is_online']
#
#    default_sort = [('id', True)]
#    base_permissions = ['can_list', 'can_show', 'can_edit', 'can_delete', 'can_add']
#    label_columns=   [{column.name: column.name for column in table.columns} ]
#    show_template =  'appbuilder/general/model/show_cascade.html'
#    list_template = 'appbuilder/general/model/list.html'
#    add_template = 'appbuilder/general/model/add.html'
#    edit_template = 'appbuilder/general/model/edit.html'
#    add_widget = (FormVerticalWidget|FormInlineWidget)
#    show_widget = ShowBlockWidget
#    list_widget = (ListThumbnail|ListWidget)
#    base_order = ('name', 'asc')
#    list_widget= 'list_widget'


class IndividualDetailView(ModelView):
    datamodel=SQLAInterface(Individual, db.session)
    related_views = []
    show_title='Individual Detail'
    add_title ='Add Individual'
    list_title= 'Individual List'
    edit_title = 'Edit Individual'
    show_columns = ['id', 'userx', 'is_individual', 'is_institution', 'is_company', 'is_government', 'is_online']
#    show_exclude_columns = [] #= ['id', 'userx', 'is_individual', 'is_institution', 'is_company', 'is_government', 'is_online']
#
#    add_columns = ['id', 'userx', 'is_individual', 'is_institution', 'is_company', 'is_government', 'is_online']
#    add_exclude_columns = [hide_list] #['id', 'userx', 'is_individual', 'is_institution', 'is_company', 'is_government', 'is_online']
#
#    edit_columns = ['id', 'userx', 'is_individual', 'is_institution', 'is_company', 'is_government', 'is_online']
#    edit_exclude_columns =[hide_list] # ['id', 'userx', 'is_individual', 'is_institution', 'is_company', 'is_government', 'is_online']
#
#    list_columns = ['id', 'userx', 'is_individual', 'is_institution', 'is_company', 'is_government', 'is_online']
#    list_exclude_columns = [] # ['id', 'userx', 'is_individual', 'is_institution', 'is_company', 'is_government', 'is_online']
#
#    search_columns = ['id', 'userx', 'is_individual', 'is_institution', 'is_company', 'is_government', 'is_online']
#    search_exclude_columns= [] # ['id', 'userx', 'is_individual', 'is_institution', 'is_company', 'is_government', 'is_online']
#
#    default_sort = [('id', True)]
#    base_permissions = ['can_list', 'can_show', 'can_edit', 'can_delete', 'can_add']
#    label_columns=   [{column.name: column.name for column in table.columns} ]
#    show_template =  'appbuilder/general/model/show_cascade.html'
#    list_template = 'appbuilder/general/model/list.html'
#    add_template = 'appbuilder/general/model/add.html'
#    edit_template = 'appbuilder/general/model/edit.html'
#    add_widget = (FormVerticalWidget|FormInlineWidget)
#    show_widget = ShowBlockWidget
#    list_widget = (ListThumbnail|ListWidget)
#    base_order = ('name', 'asc')
#    list_widget= 'list_widget'


class IndustryDetailView(ModelView):
    datamodel=SQLAInterface(Industry, db.session)
    related_views = []
    show_title='Industry Detail'
    add_title ='Add Industry'
    list_title= 'Industry List'
    edit_title = 'Edit Industry'
    show_columns = ['industry', 'job']
#    show_exclude_columns = [] #= ['industry', 'job']
#
#    add_columns = ['industry', 'job']
#    add_exclude_columns = [hide_list] #['industry', 'job']
#
#    edit_columns = ['industry', 'job']
#    edit_exclude_columns =[hide_list] # ['industry', 'job']
#
#    list_columns = ['industry', 'job']
#    list_exclude_columns = [] # ['industry', 'job']
#
#    search_columns = ['industry', 'job']
#    search_exclude_columns= [] # ['industry', 'job']
#
#    default_sort = [('id', True)]
#    base_permissions = ['can_list', 'can_show', 'can_edit', 'can_delete', 'can_add']
#    label_columns=   [{column.name: column.name for column in table.columns} ]
#    show_template =  'appbuilder/general/model/show_cascade.html'
#    list_template = 'appbuilder/general/model/list.html'
#    add_template = 'appbuilder/general/model/add.html'
#    edit_template = 'appbuilder/general/model/edit.html'
#    add_widget = (FormVerticalWidget|FormInlineWidget)
#    show_widget = ShowBlockWidget
#    list_widget = (ListThumbnail|ListWidget)
#    base_order = ('name', 'asc')
#    list_widget= 'list_widget'


class IndustryJobDetailView(ModelView):
    datamodel=SQLAInterface(IndustryJob, db.session)
    related_views = []
    show_title='IndustryJob Detail'
    add_title ='Add IndustryJob'
    list_title= 'IndustryJob List'
    edit_title = 'Edit IndustryJob'
    show_columns = ['industry', 'job']
#    show_exclude_columns = [] #= ['industry', 'job']
#
#    add_columns = ['industry', 'job']
#    add_exclude_columns = [hide_list] #['industry', 'job']
#
#    edit_columns = ['industry', 'job']
#    edit_exclude_columns =[hide_list] # ['industry', 'job']
#
#    list_columns = ['industry', 'job']
#    list_exclude_columns = [] # ['industry', 'job']
#
#    search_columns = ['industry', 'job']
#    search_exclude_columns= [] # ['industry', 'job']
#
#    default_sort = [('id', True)]
#    base_permissions = ['can_list', 'can_show', 'can_edit', 'can_delete', 'can_add']
#    label_columns=   [{column.name: column.name for column in table.columns} ]
#    show_template =  'appbuilder/general/model/show_cascade.html'
#    list_template = 'appbuilder/general/model/list.html'
#    add_template = 'appbuilder/general/model/add.html'
#    edit_template = 'appbuilder/general/model/edit.html'
#    add_widget = (FormVerticalWidget|FormInlineWidget)
#    show_widget = ShowBlockWidget
#    list_widget = (ListThumbnail|ListWidget)
#    base_order = ('name', 'asc')
#    list_widget= 'list_widget'


class JobDetailView(ModelView):
    datamodel=SQLAInterface(Job, db.session)
    related_views = []
    show_title='Job Detail'
    add_title ='Add Job'
    list_title= 'Job List'
    edit_title = 'Edit Job'
    show_columns = ['industry', 'job']
#    show_exclude_columns = [] #= ['industry', 'job']
#
#    add_columns = ['industry', 'job']
#    add_exclude_columns = [hide_list] #['industry', 'job']
#
#    edit_columns = ['industry', 'job']
#    edit_exclude_columns =[hide_list] # ['industry', 'job']
#
#    list_columns = ['industry', 'job']
#    list_exclude_columns = [] # ['industry', 'job']
#
#    search_columns = ['industry', 'job']
#    search_exclude_columns= [] # ['industry', 'job']
#
#    default_sort = [('id', True)]
#    base_permissions = ['can_list', 'can_show', 'can_edit', 'can_delete', 'can_add']
#    label_columns=   [{column.name: column.name for column in table.columns} ]
#    show_template =  'appbuilder/general/model/show_cascade.html'
#    list_template = 'appbuilder/general/model/list.html'
#    add_template = 'appbuilder/general/model/add.html'
#    edit_template = 'appbuilder/general/model/edit.html'
#    add_widget = (FormVerticalWidget|FormInlineWidget)
#    show_widget = ShowBlockWidget
#    list_widget = (ListThumbnail|ListWidget)
#    base_order = ('name', 'asc')
#    list_widget= 'list_widget'




class SkillDetailView(ModelView):
    datamodel=SQLAInterface(Skill, db.session)
    related_views = []
    show_title='Skill Detail'
    add_title ='Add Skill'
    list_title= 'Skill List'
    edit_title = 'Edit Skill'
    show_columns = ['skills', 'jobs']
#    show_exclude_columns = [] #= ['skills', 'jobs']
#
#    add_columns = ['skills', 'jobs']
#    add_exclude_columns = [hide_list] #['skills', 'jobs']
#
#    edit_columns = ['skills', 'jobs']
#    edit_exclude_columns =[hide_list] # ['skills', 'jobs']
#
#    list_columns = ['skills', 'jobs']
#    list_exclude_columns = [] # ['skills', 'jobs']
#
#    search_columns = ['skills', 'jobs']
#    search_exclude_columns= [] # ['skills', 'jobs']
#
#    default_sort = [('id', True)]
#    base_permissions = ['can_list', 'can_show', 'can_edit', 'can_delete', 'can_add']
#    label_columns=   [{column.name: column.name for column in table.columns} ]
#    show_template =  'appbuilder/general/model/show_cascade.html'
#    list_template = 'appbuilder/general/model/list.html'
#    add_template = 'appbuilder/general/model/add.html'
#    edit_template = 'appbuilder/general/model/edit.html'
#    add_widget = (FormVerticalWidget|FormInlineWidget)
#    show_widget = ShowBlockWidget
#    list_widget = (ListThumbnail|ListWidget)
#    base_order = ('name', 'asc')
#    list_widget= 'list_widget'


class JobSkillDetailView(ModelView):
    datamodel=SQLAInterface(JobSkill, db.session)
    related_views = []
    show_title='JobSkill Detail'
    add_title ='Add JobSkill'
    list_title= 'JobSkill List'
    edit_title = 'Edit JobSkill'
    show_columns = ['skills', 'jobs']
#    show_exclude_columns = [] #= ['skills', 'jobs']
#
#    add_columns = ['skills', 'jobs']
#    add_exclude_columns = [hide_list] #['skills', 'jobs']
#
#    edit_columns = ['skills', 'jobs']
#    edit_exclude_columns =[hide_list] # ['skills', 'jobs']
#
#    list_columns = ['skills', 'jobs']
#    list_exclude_columns = [] # ['skills', 'jobs']
#
#    search_columns = ['skills', 'jobs']
#    search_exclude_columns= [] # ['skills', 'jobs']
#
#    default_sort = [('id', True)]
#    base_permissions = ['can_list', 'can_show', 'can_edit', 'can_delete', 'can_add']
#    label_columns=   [{column.name: column.name for column in table.columns} ]
#    show_template =  'appbuilder/general/model/show_cascade.html'
#    list_template = 'appbuilder/general/model/list.html'
#    add_template = 'appbuilder/general/model/add.html'
#    edit_template = 'appbuilder/general/model/edit.html'
#    add_widget = (FormVerticalWidget|FormInlineWidget)
#    show_widget = ShowBlockWidget
#    list_widget = (ListThumbnail|ListWidget)
#    base_order = ('name', 'asc')
#    list_widget= 'list_widget'


class PortalDetailView(ModelView):
    datamodel=SQLAInterface(Portal, db.session)
    related_views = []
    show_title='Portal Detail'
    add_title ='Add Portal'
    list_title= 'Portal List'
    edit_title = 'Edit Portal'
    show_columns = ['id', 'portal', 'header', 'slug', 'page_type']
#    show_exclude_columns = [] #= ['id', 'portal', 'header', 'slug', 'page_type']
#
#    add_columns = ['id', 'portal', 'header', 'slug', 'page_type']
#    add_exclude_columns = [hide_list] #['id', 'portal', 'header', 'slug', 'page_type']
#
#    edit_columns = ['id', 'portal', 'header', 'slug', 'page_type']
#    edit_exclude_columns =[hide_list] # ['id', 'portal', 'header', 'slug', 'page_type']
#
#    list_columns = ['id', 'portal', 'header', 'slug', 'page_type']
#    list_exclude_columns = [] # ['id', 'portal', 'header', 'slug', 'page_type']
#
#    search_columns = ['id', 'portal', 'header', 'slug', 'page_type']
#    search_exclude_columns= [] # ['id', 'portal', 'header', 'slug', 'page_type']
#
#    default_sort = [('id', True)]
#    base_permissions = ['can_list', 'can_show', 'can_edit', 'can_delete', 'can_add']
#    label_columns=   [{column.name: column.name for column in table.columns} ]
#    show_template =  'appbuilder/general/model/show_cascade.html'
#    list_template = 'appbuilder/general/model/list.html'
#    add_template = 'appbuilder/general/model/add.html'
#    edit_template = 'appbuilder/general/model/edit.html'
#    add_widget = (FormVerticalWidget|FormInlineWidget)
#    show_widget = ShowBlockWidget
#    list_widget = (ListThumbnail|ListWidget)
#    base_order = ('name', 'asc')
#    list_widget= 'list_widget'


class PageDetailView(ModelView):
    datamodel=SQLAInterface(Page, db.session)
    related_views = []
    show_title='Page Detail'
    add_title ='Add Page'
    list_title= 'Page List'
    edit_title = 'Edit Page'
    show_columns = ['id', 'portal', 'header', 'slug', 'page_type']
#    show_exclude_columns = [] #= ['id', 'portal', 'header', 'slug', 'page_type']
#
#    add_columns = ['id', 'portal', 'header', 'slug', 'page_type']
#    add_exclude_columns = [hide_list] #['id', 'portal', 'header', 'slug', 'page_type']
#
#    edit_columns = ['id', 'portal', 'header', 'slug', 'page_type']
#    edit_exclude_columns =[hide_list] # ['id', 'portal', 'header', 'slug', 'page_type']
#
#    list_columns = ['id', 'portal', 'header', 'slug', 'page_type']
#    list_exclude_columns = [] # ['id', 'portal', 'header', 'slug', 'page_type']
#
#    search_columns = ['id', 'portal', 'header', 'slug', 'page_type']
#    search_exclude_columns= [] # ['id', 'portal', 'header', 'slug', 'page_type']
#
#    default_sort = [('id', True)]
#    base_permissions = ['can_list', 'can_show', 'can_edit', 'can_delete', 'can_add']
#    label_columns=   [{column.name: column.name for column in table.columns} ]
#    show_template =  'appbuilder/general/model/show_cascade.html'
#    list_template = 'appbuilder/general/model/list.html'
#    add_template = 'appbuilder/general/model/add.html'
#    edit_template = 'appbuilder/general/model/edit.html'
#    add_widget = (FormVerticalWidget|FormInlineWidget)
#    show_widget = ShowBlockWidget
#    list_widget = (ListThumbnail|ListWidget)
#    base_order = ('name', 'asc')
#    list_widget= 'list_widget'


class ProfilesourceDetailView(ModelView):
    datamodel=SQLAInterface(Profilesource, db.session)
    related_views = []
    show_title='Profilesource Detail'
    add_title ='Add Profilesource'
    list_title= 'Profilesource List'
    edit_title = 'Edit Profilesource'
    show_columns = ['id', 'individual', 'import_address', 'profile_username', 'profile_password', 'has_been_imported', 'import_data', 'import_date', 'profilesource']
#    show_exclude_columns = [] #= ['id', 'individual', 'import_address', 'profile_username', 'profile_password', 'has_been_imported', 'import_data', 'import_date', 'profilesource']
#
#    add_columns = ['id', 'individual', 'import_address', 'profile_username', 'profile_password', 'has_been_imported', 'import_data', 'import_date', 'profilesource']
#    add_exclude_columns = [hide_list] #['id', 'individual', 'import_address', 'profile_username', 'profile_password', 'has_been_imported', 'import_data', 'import_date', 'profilesource']
#
#    edit_columns = ['id', 'individual', 'import_address', 'profile_username', 'profile_password', 'has_been_imported', 'import_data', 'import_date', 'profilesource']
#    edit_exclude_columns =[hide_list] # ['id', 'individual', 'import_address', 'profile_username', 'profile_password', 'has_been_imported', 'import_data', 'import_date', 'profilesource']
#
#    list_columns = ['id', 'individual', 'import_address', 'profile_username', 'profile_password', 'has_been_imported', 'import_data', 'import_date', 'profilesource']
#    list_exclude_columns = [] # ['id', 'individual', 'import_address', 'profile_username', 'profile_password', 'has_been_imported', 'import_data', 'import_date', 'profilesource']
#
#    search_columns = ['id', 'individual', 'import_address', 'profile_username', 'profile_password', 'has_been_imported', 'import_data', 'import_date', 'profilesource']
#    search_exclude_columns= [] # ['id', 'individual', 'import_address', 'profile_username', 'profile_password', 'has_been_imported', 'import_data', 'import_date', 'profilesource']
#
#    default_sort = [('id', True)]
#    base_permissions = ['can_list', 'can_show', 'can_edit', 'can_delete', 'can_add']
#    label_columns=   [{column.name: column.name for column in table.columns} ]
#    show_template =  'appbuilder/general/model/show_cascade.html'
#    list_template = 'appbuilder/general/model/list.html'
#    add_template = 'appbuilder/general/model/add.html'
#    edit_template = 'appbuilder/general/model/edit.html'
#    add_widget = (FormVerticalWidget|FormInlineWidget)
#    show_widget = ShowBlockWidget
#    list_widget = (ListThumbnail|ListWidget)
#    base_order = ('name', 'asc')
#    list_widget= 'list_widget'


class ProfileDetailView(ModelView):
    datamodel=SQLAInterface(Profile, db.session)
    related_views = []
    show_title='Profile Detail'
    add_title ='Add Profile'
    list_title= 'Profile List'
    edit_title = 'Edit Profile'
    show_columns = ['id', 'individual', 'import_address', 'profile_username', 'profile_password', 'has_been_imported', 'import_data', 'import_date', 'profilesource']
#    show_exclude_columns = [] #= ['id', 'individual', 'import_address', 'profile_username', 'profile_password', 'has_been_imported', 'import_data', 'import_date', 'profilesource']
#
#    add_columns = ['id', 'individual', 'import_address', 'profile_username', 'profile_password', 'has_been_imported', 'import_data', 'import_date', 'profilesource']
#    add_exclude_columns = [hide_list] #['id', 'individual', 'import_address', 'profile_username', 'profile_password', 'has_been_imported', 'import_data', 'import_date', 'profilesource']
#
#    edit_columns = ['id', 'individual', 'import_address', 'profile_username', 'profile_password', 'has_been_imported', 'import_data', 'import_date', 'profilesource']
#    edit_exclude_columns =[hide_list] # ['id', 'individual', 'import_address', 'profile_username', 'profile_password', 'has_been_imported', 'import_data', 'import_date', 'profilesource']
#
#    list_columns = ['id', 'individual', 'import_address', 'profile_username', 'profile_password', 'has_been_imported', 'import_data', 'import_date', 'profilesource']
#    list_exclude_columns = [] # ['id', 'individual', 'import_address', 'profile_username', 'profile_password', 'has_been_imported', 'import_data', 'import_date', 'profilesource']
#
#    search_columns = ['id', 'individual', 'import_address', 'profile_username', 'profile_password', 'has_been_imported', 'import_data', 'import_date', 'profilesource']
#    search_exclude_columns= [] # ['id', 'individual', 'import_address', 'profile_username', 'profile_password', 'has_been_imported', 'import_data', 'import_date', 'profilesource']
#
#    default_sort = [('id', True)]
#    base_permissions = ['can_list', 'can_show', 'can_edit', 'can_delete', 'can_add']
#    label_columns=   [{column.name: column.name for column in table.columns} ]
#    show_template =  'appbuilder/general/model/show_cascade.html'
#    list_template = 'appbuilder/general/model/list.html'
#    add_template = 'appbuilder/general/model/add.html'
#    edit_template = 'appbuilder/general/model/edit.html'
#    add_widget = (FormVerticalWidget|FormInlineWidget)
#    show_widget = ShowBlockWidget
#    list_widget = (ListThumbnail|ListWidget)
#    base_order = ('name', 'asc')
#    list_widget= 'list_widget'


class LocationDetailView(ModelView):
    datamodel=SQLAInterface(Location, db.session)
    related_views = []
    show_title='Location Detail'
    add_title ='Add Location'
    list_title= 'Location List'
    edit_title = 'Edit Location'
    show_columns = ['id', 'individual', 'template', 'header', 'color', 'location', 'summary_text', 'has_been_generated', 'preferred']
#    show_exclude_columns = [] #= ['id', 'individual', 'template', 'header', 'color', 'location', 'summary_text', 'has_been_generated', 'preferred']
#
#    add_columns = ['id', 'individual', 'template', 'header', 'color', 'location', 'summary_text', 'has_been_generated', 'preferred']
#    add_exclude_columns = [hide_list] #['id', 'individual', 'template', 'header', 'color', 'location', 'summary_text', 'has_been_generated', 'preferred']
#
#    edit_columns = ['id', 'individual', 'template', 'header', 'color', 'location', 'summary_text', 'has_been_generated', 'preferred']
#    edit_exclude_columns =[hide_list] # ['id', 'individual', 'template', 'header', 'color', 'location', 'summary_text', 'has_been_generated', 'preferred']
#
#    list_columns = ['id', 'individual', 'template', 'header', 'color', 'location', 'summary_text', 'has_been_generated', 'preferred']
#    list_exclude_columns = [] # ['id', 'individual', 'template', 'header', 'color', 'location', 'summary_text', 'has_been_generated', 'preferred']
#
#    search_columns = ['id', 'individual', 'template', 'header', 'color', 'location', 'summary_text', 'has_been_generated', 'preferred']
#    search_exclude_columns= [] # ['id', 'individual', 'template', 'header', 'color', 'location', 'summary_text', 'has_been_generated', 'preferred']
#
#    default_sort = [('id', True)]
#    base_permissions = ['can_list', 'can_show', 'can_edit', 'can_delete', 'can_add']
#    label_columns=   [{column.name: column.name for column in table.columns} ]
#    show_template =  'appbuilder/general/model/show_cascade.html'
#    list_template = 'appbuilder/general/model/list.html'
#    add_template = 'appbuilder/general/model/add.html'
#    edit_template = 'appbuilder/general/model/edit.html'
#    add_widget = (FormVerticalWidget|FormInlineWidget)
#    show_widget = ShowBlockWidget
#    list_widget = (ListThumbnail|ListWidget)
#    base_order = ('name', 'asc')
#    list_widget= 'list_widget'


class ResumeDetailView(ModelView):
    datamodel=SQLAInterface(Resume, db.session)
    related_views = []
    show_title='Resume Detail'
    add_title ='Add Resume'
    list_title= 'Resume List'
    edit_title = 'Edit Resume'
    show_columns = ['id', 'individual', 'template', 'header', 'color', 'location', 'summary_text', 'has_been_generated', 'preferred']
#    show_exclude_columns = [] #= ['id', 'individual', 'template', 'header', 'color', 'location', 'summary_text', 'has_been_generated', 'preferred']
#
#    add_columns = ['id', 'individual', 'template', 'header', 'color', 'location', 'summary_text', 'has_been_generated', 'preferred']
#    add_exclude_columns = [hide_list] #['id', 'individual', 'template', 'header', 'color', 'location', 'summary_text', 'has_been_generated', 'preferred']
#
#    edit_columns = ['id', 'individual', 'template', 'header', 'color', 'location', 'summary_text', 'has_been_generated', 'preferred']
#    edit_exclude_columns =[hide_list] # ['id', 'individual', 'template', 'header', 'color', 'location', 'summary_text', 'has_been_generated', 'preferred']
#
#    list_columns = ['id', 'individual', 'template', 'header', 'color', 'location', 'summary_text', 'has_been_generated', 'preferred']
#    list_exclude_columns = [] # ['id', 'individual', 'template', 'header', 'color', 'location', 'summary_text', 'has_been_generated', 'preferred']
#
#    search_columns = ['id', 'individual', 'template', 'header', 'color', 'location', 'summary_text', 'has_been_generated', 'preferred']
#    search_exclude_columns= [] # ['id', 'individual', 'template', 'header', 'color', 'location', 'summary_text', 'has_been_generated', 'preferred']
#
#    default_sort = [('id', True)]
#    base_permissions = ['can_list', 'can_show', 'can_edit', 'can_delete', 'can_add']
#    label_columns=   [{column.name: column.name for column in table.columns} ]
#    show_template =  'appbuilder/general/model/show_cascade.html'
#    list_template = 'appbuilder/general/model/list.html'
#    add_template = 'appbuilder/general/model/add.html'
#    edit_template = 'appbuilder/general/model/edit.html'
#    add_widget = (FormVerticalWidget|FormInlineWidget)
#    show_widget = ShowBlockWidget
#    list_widget = (ListThumbnail|ListWidget)
#    base_order = ('name', 'asc')
#    list_widget= 'list_widget'


class SwarmDetailView(ModelView):
    datamodel=SQLAInterface(Swarm, db.session)
    related_views = []
    show_title='Swarm Detail'
    add_title ='Add Swarm'
    list_title= 'Swarm List'
    edit_title = 'Edit Swarm'
    show_columns = ['individual', 'swarm']
#    show_exclude_columns = [] #= ['individual', 'swarm']
#
#    add_columns = ['individual', 'swarm']
#    add_exclude_columns = [hide_list] #['individual', 'swarm']
#
#    edit_columns = ['individual', 'swarm']
#    edit_exclude_columns =[hide_list] # ['individual', 'swarm']
#
#    list_columns = ['individual', 'swarm']
#    list_exclude_columns = [] # ['individual', 'swarm']
#
#    search_columns = ['individual', 'swarm']
#    search_exclude_columns= [] # ['individual', 'swarm']
#
#    default_sort = [('id', True)]
#    base_permissions = ['can_list', 'can_show', 'can_edit', 'can_delete', 'can_add']
#    label_columns=   [{column.name: column.name for column in table.columns} ]
#    show_template =  'appbuilder/general/model/show_cascade.html'
#    list_template = 'appbuilder/general/model/list.html'
#    add_template = 'appbuilder/general/model/add.html'
#    edit_template = 'appbuilder/general/model/edit.html'
#    add_widget = (FormVerticalWidget|FormInlineWidget)
#    show_widget = ShowBlockWidget
#    list_widget = (ListThumbnail|ListWidget)
#    base_order = ('name', 'asc')
#    list_widget= 'list_widget'


class IndividualSwarmDetailView(ModelView):
    datamodel=SQLAInterface(IndividualSwarm, db.session)
    related_views = []
    show_title='IndividualSwarm Detail'
    add_title ='Add IndividualSwarm'
    list_title= 'IndividualSwarm List'
    edit_title = 'Edit IndividualSwarm'
    show_columns = ['individual', 'swarm']
#    show_exclude_columns = [] #= ['individual', 'swarm']
#
#    add_columns = ['individual', 'swarm']
#    add_exclude_columns = [hide_list] #['individual', 'swarm']
#
#    edit_columns = ['individual', 'swarm']
#    edit_exclude_columns =[hide_list] # ['individual', 'swarm']
#
#    list_columns = ['individual', 'swarm']
#    list_exclude_columns = [] # ['individual', 'swarm']
#
#    search_columns = ['individual', 'swarm']
#    search_exclude_columns= [] # ['individual', 'swarm']
#
#    default_sort = [('id', True)]
#    base_permissions = ['can_list', 'can_show', 'can_edit', 'can_delete', 'can_add']
#    label_columns=   [{column.name: column.name for column in table.columns} ]
#    show_template =  'appbuilder/general/model/show_cascade.html'
#    list_template = 'appbuilder/general/model/list.html'
#    add_template = 'appbuilder/general/model/add.html'
#    edit_template = 'appbuilder/general/model/edit.html'
#    add_widget = (FormVerticalWidget|FormInlineWidget)
#    show_widget = ShowBlockWidget
#    list_widget = (ListThumbnail|ListWidget)
#    base_order = ('name', 'asc')
#    list_widget= 'list_widget'


class IndividualMasterView(MasterDetailView):
    datamodel=SQLAInterface(Individual, db.session)
    related_views = [UserxDetailView]
    show_title='Individual Detail'
    add_title ='Add Individual'
    list_title= 'Individual List'
    edit_title = 'Edit Individual'
    show_columns = ['id', 'userx', 'is_individual', 'is_institution', 'is_company', 'is_government', 'is_online']
#    show_exclude_columns = [] #= ['id', 'userx', 'is_individual', 'is_institution', 'is_company', 'is_government', 'is_online']
#
#    add_columns = ['id', 'userx', 'is_individual', 'is_institution', 'is_company', 'is_government', 'is_online']
#    add_exclude_columns = [hide_list] #['id', 'userx', 'is_individual', 'is_institution', 'is_company', 'is_government', 'is_online']
#
#    edit_columns = ['id', 'userx', 'is_individual', 'is_institution', 'is_company', 'is_government', 'is_online']
#    edit_exclude_columns =[hide_list] # ['id', 'userx', 'is_individual', 'is_institution', 'is_company', 'is_government', 'is_online']
#
#    list_columns = ['id', 'userx', 'is_individual', 'is_institution', 'is_company', 'is_government', 'is_online']
#    list_exclude_columns = [] # ['id', 'userx', 'is_individual', 'is_institution', 'is_company', 'is_government', 'is_online']
#
#    search_columns = ['id', 'userx', 'is_individual', 'is_institution', 'is_company', 'is_government', 'is_online']
#    search_exclude_columns= [] # ['id', 'userx', 'is_individual', 'is_institution', 'is_company', 'is_government', 'is_online']
#
#    default_sort = [('id', True)]
#    base_permissions = ['can_list', 'can_show', 'can_edit', 'can_delete', 'can_add']
#    label_columns=   [{column.name: column.name for column in table.columns} ]
#    show_template =  'appbuilder/general/model/show_cascade.html'
#    list_template = 'appbuilder/general/model/list.html'
#    add_template = 'appbuilder/general/model/add.html'
#    edit_template = 'appbuilder/general/model/edit.html'
#    add_widget = (FormVerticalWidget|FormInlineWidget)
#    show_widget = ShowBlockWidget
#    list_widget = (ListThumbnail|ListWidget)
#    base_order = ('name', 'asc')
#    list_widget= 'list_widget'


class IndustryJobMasterView(MasterDetailView):
    datamodel=SQLAInterface(IndustryJob, db.session)
    related_views = [IndustryDetailView]
    show_title='IndustryJob Detail'
    add_title ='Add IndustryJob'
    list_title= 'IndustryJob List'
    edit_title = 'Edit IndustryJob'
    show_columns = ['industry', 'job']
#    show_exclude_columns = [] #= ['industry', 'job']
#
#    add_columns = ['industry', 'job']
#    add_exclude_columns = [hide_list] #['industry', 'job']
#
#    edit_columns = ['industry', 'job']
#    edit_exclude_columns =[hide_list] # ['industry', 'job']
#
#    list_columns = ['industry', 'job']
#    list_exclude_columns = [] # ['industry', 'job']
#
#    search_columns = ['industry', 'job']
#    search_exclude_columns= [] # ['industry', 'job']
#
#    default_sort = [('id', True)]
#    base_permissions = ['can_list', 'can_show', 'can_edit', 'can_delete', 'can_add']
#    label_columns=   [{column.name: column.name for column in table.columns} ]
#    show_template =  'appbuilder/general/model/show_cascade.html'
#    list_template = 'appbuilder/general/model/list.html'
#    add_template = 'appbuilder/general/model/add.html'
#    edit_template = 'appbuilder/general/model/edit.html'
#    add_widget = (FormVerticalWidget|FormInlineWidget)
#    show_widget = ShowBlockWidget
#    list_widget = (ListThumbnail|ListWidget)
#    base_order = ('name', 'asc')
#    list_widget= 'list_widget'


class IndustryJobMultiView(MultipleView):
    datamodel=SQLAInterface(IndustryJob, db.session)
    views = [IndustryDetailView, JobDetailView]
    show_title='IndustryJob Detail'
    add_title ='Add IndustryJob'
    list_title= 'IndustryJob List'
    edit_title = 'Edit IndustryJob'
    show_columns = ['industry', 'job']
#    show_exclude_columns = [] #= ['industry', 'job']
#
#    add_columns = ['industry', 'job']
#    add_exclude_columns = [hide_list] #['industry', 'job']
#
#    edit_columns = ['industry', 'job']
#    edit_exclude_columns =[hide_list] # ['industry', 'job']
#
#    list_columns = ['industry', 'job']
#    list_exclude_columns = [] # ['industry', 'job']
#
#    search_columns = ['industry', 'job']
#    search_exclude_columns= [] # ['industry', 'job']
#
#    default_sort = [('id', True)]
#    base_permissions = ['can_list', 'can_show', 'can_edit', 'can_delete', 'can_add']
#    label_columns=   [{column.name: column.name for column in table.columns} ]
#    show_template =  'appbuilder/general/model/show_cascade.html'
#    list_template = 'appbuilder/general/model/list.html'
#    add_template = 'appbuilder/general/model/add.html'
#    edit_template = 'appbuilder/general/model/edit.html'
#    add_widget = (FormVerticalWidget|FormInlineWidget)
#    show_widget = ShowBlockWidget
#    list_widget = (ListThumbnail|ListWidget)
#    base_order = ('name', 'asc')
#    list_widget= 'list_widget'


class JobSkillMasterView(MasterDetailView):
    datamodel=SQLAInterface(JobSkill, db.session)
    related_views = [JobDetailView]
    show_title='JobSkill Detail'
    add_title ='Add JobSkill'
    list_title= 'JobSkill List'
    edit_title = 'Edit JobSkill'
    show_columns = ['skills', 'jobs']
#    show_exclude_columns = [] #= ['skills', 'jobs']
#
#    add_columns = ['skills', 'jobs']
#    add_exclude_columns = [hide_list] #['skills', 'jobs']
#
#    edit_columns = ['skills', 'jobs']
#    edit_exclude_columns =[hide_list] # ['skills', 'jobs']
#
#    list_columns = ['skills', 'jobs']
#    list_exclude_columns = [] # ['skills', 'jobs']
#
#    search_columns = ['skills', 'jobs']
#    search_exclude_columns= [] # ['skills', 'jobs']
#
#    default_sort = [('id', True)]
#    base_permissions = ['can_list', 'can_show', 'can_edit', 'can_delete', 'can_add']
#    label_columns=   [{column.name: column.name for column in table.columns} ]
#    show_template =  'appbuilder/general/model/show_cascade.html'
#    list_template = 'appbuilder/general/model/list.html'
#    add_template = 'appbuilder/general/model/add.html'
#    edit_template = 'appbuilder/general/model/edit.html'
#    add_widget = (FormVerticalWidget|FormInlineWidget)
#    show_widget = ShowBlockWidget
#    list_widget = (ListThumbnail|ListWidget)
#    base_order = ('name', 'asc')
#    list_widget= 'list_widget'


class JobSkillMultiView(MultipleView):
    datamodel=SQLAInterface(JobSkill, db.session)
    views = [SkillDetailView]
    show_title='JobSkill Detail'
    add_title ='Add JobSkill'
    list_title= 'JobSkill List'
    edit_title = 'Edit JobSkill'
    show_columns = ['skills', 'jobs']
#    show_exclude_columns = [] #= ['skills', 'jobs']
#
#    add_columns = ['skills', 'jobs']
#    add_exclude_columns = [hide_list] #['skills', 'jobs']
#
#    edit_columns = ['skills', 'jobs']
#    edit_exclude_columns =[hide_list] # ['skills', 'jobs']
#
#    list_columns = ['skills', 'jobs']
#    list_exclude_columns = [] # ['skills', 'jobs']
#
#    search_columns = ['skills', 'jobs']
#    search_exclude_columns= [] # ['skills', 'jobs']
#
#    default_sort = [('id', True)]
#    base_permissions = ['can_list', 'can_show', 'can_edit', 'can_delete', 'can_add']
#    label_columns=   [{column.name: column.name for column in table.columns} ]
#    show_template =  'appbuilder/general/model/show_cascade.html'
#    list_template = 'appbuilder/general/model/list.html'
#    add_template = 'appbuilder/general/model/add.html'
#    edit_template = 'appbuilder/general/model/edit.html'
#    add_widget = (FormVerticalWidget|FormInlineWidget)
#    show_widget = ShowBlockWidget
#    list_widget = (ListThumbnail|ListWidget)
#    base_order = ('name', 'asc')
#    list_widget= 'list_widget'


class EducationMasterView(MasterDetailView):
    datamodel=SQLAInterface(Education, db.session)
    related_views = [IndividualDetailView]
    show_title='Education Detail'
    add_title ='Add Education'
    list_title= 'Education List'
    edit_title = 'Edit Education'
    show_columns = ['id', 'individual', 'qualification', 'qual_class', 'verified', 'verification_code', 'verified_by', 'verification_date', 'verification_doc']
#    show_exclude_columns = [] #= ['id', 'individual', 'qualification', 'qual_class', 'verified', 'verification_code', 'verified_by', 'verification_date', 'verification_doc']
#
#    add_columns = ['id', 'individual', 'qualification', 'qual_class', 'verified', 'verification_code', 'verified_by', 'verification_date', 'verification_doc']
#    add_exclude_columns = [hide_list] #['id', 'individual', 'qualification', 'qual_class', 'verified', 'verification_code', 'verified_by', 'verification_date', 'verification_doc']
#
#    edit_columns = ['id', 'individual', 'qualification', 'qual_class', 'verified', 'verification_code', 'verified_by', 'verification_date', 'verification_doc']
#    edit_exclude_columns =[hide_list] # ['id', 'individual', 'qualification', 'qual_class', 'verified', 'verification_code', 'verified_by', 'verification_date', 'verification_doc']
#
#    list_columns = ['id', 'individual', 'qualification', 'qual_class', 'verified', 'verification_code', 'verified_by', 'verification_date', 'verification_doc']
#    list_exclude_columns = [] # ['id', 'individual', 'qualification', 'qual_class', 'verified', 'verification_code', 'verified_by', 'verification_date', 'verification_doc']
#
#    search_columns = ['id', 'individual', 'qualification', 'qual_class', 'verified', 'verification_code', 'verified_by', 'verification_date', 'verification_doc']
#    search_exclude_columns= [] # ['id', 'individual', 'qualification', 'qual_class', 'verified', 'verification_code', 'verified_by', 'verification_date', 'verification_doc']
#
#    default_sort = [('id', True)]
#    base_permissions = ['can_list', 'can_show', 'can_edit', 'can_delete', 'can_add']
#    label_columns=   [{column.name: column.name for column in table.columns} ]
#    show_template =  'appbuilder/general/model/show_cascade.html'
#    list_template = 'appbuilder/general/model/list.html'
#    add_template = 'appbuilder/general/model/add.html'
#    edit_template = 'appbuilder/general/model/edit.html'
#    add_widget = (FormVerticalWidget|FormInlineWidget)
#    show_widget = ShowBlockWidget
#    list_widget = (ListThumbnail|ListWidget)
#    base_order = ('name', 'asc')
#    list_widget= 'list_widget'


class IndividualJobMasterView(MasterDetailView):
    datamodel=SQLAInterface(IndividualJob, db.session)
    related_views = [IndividualDetailView]
    show_title='IndividualJob Detail'
    add_title ='Add IndividualJob'
    list_title= 'IndividualJob List'
    edit_title = 'Edit IndividualJob'
    show_columns = ['individual', 'job']
#    show_exclude_columns = [] #= ['individual', 'job']
#
#    add_columns = ['individual', 'job']
#    add_exclude_columns = [hide_list] #['individual', 'job']
#
#    edit_columns = ['individual', 'job']
#    edit_exclude_columns =[hide_list] # ['individual', 'job']
#
#    list_columns = ['individual', 'job']
#    list_exclude_columns = [] # ['individual', 'job']
#
#    search_columns = ['individual', 'job']
#    search_exclude_columns= [] # ['individual', 'job']
#
#    default_sort = [('id', True)]
#    base_permissions = ['can_list', 'can_show', 'can_edit', 'can_delete', 'can_add']
#    label_columns=   [{column.name: column.name for column in table.columns} ]
#    show_template =  'appbuilder/general/model/show_cascade.html'
#    list_template = 'appbuilder/general/model/list.html'
#    add_template = 'appbuilder/general/model/add.html'
#    edit_template = 'appbuilder/general/model/edit.html'
#    add_widget = (FormVerticalWidget|FormInlineWidget)
#    show_widget = ShowBlockWidget
#    list_widget = (ListThumbnail|ListWidget)
#    base_order = ('name', 'asc')
#    list_widget= 'list_widget'


class IndividualJobMultiView(MultipleView):
    datamodel=SQLAInterface(IndividualJob, db.session)
    views = []
    show_title='IndividualJob Detail'
    add_title ='Add IndividualJob'
    list_title= 'IndividualJob List'
    edit_title = 'Edit IndividualJob'
    show_columns = ['individual', 'job']
#    show_exclude_columns = [] #= ['individual', 'job']
#
#    add_columns = ['individual', 'job']
#    add_exclude_columns = [hide_list] #['individual', 'job']
#
#    edit_columns = ['individual', 'job']
#    edit_exclude_columns =[hide_list] # ['individual', 'job']
#
#    list_columns = ['individual', 'job']
#    list_exclude_columns = [] # ['individual', 'job']
#
#    search_columns = ['individual', 'job']
#    search_exclude_columns= [] # ['individual', 'job']
#
#    default_sort = [('id', True)]
#    base_permissions = ['can_list', 'can_show', 'can_edit', 'can_delete', 'can_add']
#    label_columns=   [{column.name: column.name for column in table.columns} ]
#    show_template =  'appbuilder/general/model/show_cascade.html'
#    list_template = 'appbuilder/general/model/list.html'
#    add_template = 'appbuilder/general/model/add.html'
#    edit_template = 'appbuilder/general/model/edit.html'
#    add_widget = (FormVerticalWidget|FormInlineWidget)
#    show_widget = ShowBlockWidget
#    list_widget = (ListThumbnail|ListWidget)
#    base_order = ('name', 'asc')
#    list_widget= 'list_widget'


class LocationMasterView(MasterDetailView):
    datamodel=SQLAInterface(Location, db.session)
    related_views = [IndividualDetailView]
    show_title='Location Detail'
    add_title ='Add Location'
    list_title= 'Location List'
    edit_title = 'Edit Location'
    show_columns = ['id', 'individual']
#    show_exclude_columns = [] #= ['id', 'individual']
#
#    add_columns = ['id', 'individual']
#    add_exclude_columns = [hide_list] #['id', 'individual']
#
#    edit_columns = ['id', 'individual']
#    edit_exclude_columns =[hide_list] # ['id', 'individual']
#
#    list_columns = ['id', 'individual']
#    list_exclude_columns = [] # ['id', 'individual']
#
#    search_columns = ['id', 'individual']
#    search_exclude_columns= [] # ['id', 'individual']
#
#    default_sort = [('id', True)]
#    base_permissions = ['can_list', 'can_show', 'can_edit', 'can_delete', 'can_add']
#    label_columns=   [{column.name: column.name for column in table.columns} ]
#    show_template =  'appbuilder/general/model/show_cascade.html'
#    list_template = 'appbuilder/general/model/list.html'
#    add_template = 'appbuilder/general/model/add.html'
#    edit_template = 'appbuilder/general/model/edit.html'
#    add_widget = (FormVerticalWidget|FormInlineWidget)
#    show_widget = ShowBlockWidget
#    list_widget = (ListThumbnail|ListWidget)
#    base_order = ('name', 'asc')
#    list_widget= 'list_widget'


class PortalMasterView(MasterDetailView):
    datamodel=SQLAInterface(Portal, db.session)
    related_views = [IndividualDetailView]
    show_title='Portal Detail'
    add_title ='Add Portal'
    list_title= 'Portal List'
    edit_title = 'Edit Portal'
    show_columns = ['id', 'portal_url', 'is_primary', 'portal_state', 'individual', 'has_custom_domain', 'domain', 'header_text', 'slug', 'automatic_fulfillment_digital_products', 'default_digital_max_downloads', 'default_digital_url_valid_days', 'default_mail_sender_name', 'default_mail_sender_address', 'fulfillment_auto_approve', 'fulfillment_allow_unpaid', 'reserve_stock_duration_anonymous_user', 'reserve_stock_duration_authenticated_user', 'limit_quantity_per_checkout', 'gift_card_expiry_type', 'gift_card_expiry_period_type', 'gift_card_expiry_period', 'charge_taxes_on_shipping', 'include_taxes_in_prices', 'display_gross_prices', 'language']
#    show_exclude_columns = [] #= ['id', 'portal_url', 'is_primary', 'portal_state', 'individual', 'has_custom_domain', 'domain', 'header_text', 'slug', 'automatic_fulfillment_digital_products', 'default_digital_max_downloads', 'default_digital_url_valid_days', 'default_mail_sender_name', 'default_mail_sender_address', 'fulfillment_auto_approve', 'fulfillment_allow_unpaid', 'reserve_stock_duration_anonymous_user', 'reserve_stock_duration_authenticated_user', 'limit_quantity_per_checkout', 'gift_card_expiry_type', 'gift_card_expiry_period_type', 'gift_card_expiry_period', 'charge_taxes_on_shipping', 'include_taxes_in_prices', 'display_gross_prices', 'language']
#
#    add_columns = ['id', 'portal_url', 'is_primary', 'portal_state', 'individual', 'has_custom_domain', 'domain', 'header_text', 'slug', 'automatic_fulfillment_digital_products', 'default_digital_max_downloads', 'default_digital_url_valid_days', 'default_mail_sender_name', 'default_mail_sender_address', 'fulfillment_auto_approve', 'fulfillment_allow_unpaid', 'reserve_stock_duration_anonymous_user', 'reserve_stock_duration_authenticated_user', 'limit_quantity_per_checkout', 'gift_card_expiry_type', 'gift_card_expiry_period_type', 'gift_card_expiry_period', 'charge_taxes_on_shipping', 'include_taxes_in_prices', 'display_gross_prices', 'language']
#    add_exclude_columns = [hide_list] #['id', 'portal_url', 'is_primary', 'portal_state', 'individual', 'has_custom_domain', 'domain', 'header_text', 'slug', 'automatic_fulfillment_digital_products', 'default_digital_max_downloads', 'default_digital_url_valid_days', 'default_mail_sender_name', 'default_mail_sender_address', 'fulfillment_auto_approve', 'fulfillment_allow_unpaid', 'reserve_stock_duration_anonymous_user', 'reserve_stock_duration_authenticated_user', 'limit_quantity_per_checkout', 'gift_card_expiry_type', 'gift_card_expiry_period_type', 'gift_card_expiry_period', 'charge_taxes_on_shipping', 'include_taxes_in_prices', 'display_gross_prices', 'language']
#
#    edit_columns = ['id', 'portal_url', 'is_primary', 'portal_state', 'individual', 'has_custom_domain', 'domain', 'header_text', 'slug', 'automatic_fulfillment_digital_products', 'default_digital_max_downloads', 'default_digital_url_valid_days', 'default_mail_sender_name', 'default_mail_sender_address', 'fulfillment_auto_approve', 'fulfillment_allow_unpaid', 'reserve_stock_duration_anonymous_user', 'reserve_stock_duration_authenticated_user', 'limit_quantity_per_checkout', 'gift_card_expiry_type', 'gift_card_expiry_period_type', 'gift_card_expiry_period', 'charge_taxes_on_shipping', 'include_taxes_in_prices', 'display_gross_prices', 'language']
#    edit_exclude_columns =[hide_list] # ['id', 'portal_url', 'is_primary', 'portal_state', 'individual', 'has_custom_domain', 'domain', 'header_text', 'slug', 'automatic_fulfillment_digital_products', 'default_digital_max_downloads', 'default_digital_url_valid_days', 'default_mail_sender_name', 'default_mail_sender_address', 'fulfillment_auto_approve', 'fulfillment_allow_unpaid', 'reserve_stock_duration_anonymous_user', 'reserve_stock_duration_authenticated_user', 'limit_quantity_per_checkout', 'gift_card_expiry_type', 'gift_card_expiry_period_type', 'gift_card_expiry_period', 'charge_taxes_on_shipping', 'include_taxes_in_prices', 'display_gross_prices', 'language']
#
#    list_columns = ['id', 'portal_url', 'is_primary', 'portal_state', 'individual', 'has_custom_domain', 'domain', 'header_text', 'slug', 'automatic_fulfillment_digital_products', 'default_digital_max_downloads', 'default_digital_url_valid_days', 'default_mail_sender_name', 'default_mail_sender_address', 'fulfillment_auto_approve', 'fulfillment_allow_unpaid', 'reserve_stock_duration_anonymous_user', 'reserve_stock_duration_authenticated_user', 'limit_quantity_per_checkout', 'gift_card_expiry_type', 'gift_card_expiry_period_type', 'gift_card_expiry_period', 'charge_taxes_on_shipping', 'include_taxes_in_prices', 'display_gross_prices', 'language']
#    list_exclude_columns = [] # ['id', 'portal_url', 'is_primary', 'portal_state', 'individual', 'has_custom_domain', 'domain', 'header_text', 'slug', 'automatic_fulfillment_digital_products', 'default_digital_max_downloads', 'default_digital_url_valid_days', 'default_mail_sender_name', 'default_mail_sender_address', 'fulfillment_auto_approve', 'fulfillment_allow_unpaid', 'reserve_stock_duration_anonymous_user', 'reserve_stock_duration_authenticated_user', 'limit_quantity_per_checkout', 'gift_card_expiry_type', 'gift_card_expiry_period_type', 'gift_card_expiry_period', 'charge_taxes_on_shipping', 'include_taxes_in_prices', 'display_gross_prices', 'language']
#
#    search_columns = ['id', 'portal_url', 'is_primary', 'portal_state', 'individual', 'has_custom_domain', 'domain', 'header_text', 'slug', 'automatic_fulfillment_digital_products', 'default_digital_max_downloads', 'default_digital_url_valid_days', 'default_mail_sender_name', 'default_mail_sender_address', 'fulfillment_auto_approve', 'fulfillment_allow_unpaid', 'reserve_stock_duration_anonymous_user', 'reserve_stock_duration_authenticated_user', 'limit_quantity_per_checkout', 'gift_card_expiry_type', 'gift_card_expiry_period_type', 'gift_card_expiry_period', 'charge_taxes_on_shipping', 'include_taxes_in_prices', 'display_gross_prices', 'language']
#    search_exclude_columns= [] # ['id', 'portal_url', 'is_primary', 'portal_state', 'individual', 'has_custom_domain', 'domain', 'header_text', 'slug', 'automatic_fulfillment_digital_products', 'default_digital_max_downloads', 'default_digital_url_valid_days', 'default_mail_sender_name', 'default_mail_sender_address', 'fulfillment_auto_approve', 'fulfillment_allow_unpaid', 'reserve_stock_duration_anonymous_user', 'reserve_stock_duration_authenticated_user', 'limit_quantity_per_checkout', 'gift_card_expiry_type', 'gift_card_expiry_period_type', 'gift_card_expiry_period', 'charge_taxes_on_shipping', 'include_taxes_in_prices', 'display_gross_prices', 'language']
#
#    default_sort = [('id', True)]
#    base_permissions = ['can_list', 'can_show', 'can_edit', 'can_delete', 'can_add']
#    label_columns=   [{column.name: column.name for column in table.columns} ]
#    show_template =  'appbuilder/general/model/show_cascade.html'
#    list_template = 'appbuilder/general/model/list.html'
#    add_template = 'appbuilder/general/model/add.html'
#    edit_template = 'appbuilder/general/model/edit.html'
#    add_widget = (FormVerticalWidget|FormInlineWidget)
#    show_widget = ShowBlockWidget
#    list_widget = (ListThumbnail|ListWidget)
#    base_order = ('name', 'asc')
#    list_widget= 'list_widget'


class PageMasterView(MasterDetailView):
    datamodel=SQLAInterface(Page, db.session)
    related_views = [PortalDetailView]
    show_title='Page Detail'
    add_title ='Add Page'
    list_title= 'Page List'
    edit_title = 'Edit Page'
    show_columns = ['id', 'portal', 'header', 'slug', 'page_type']
#    show_exclude_columns = [] #= ['id', 'portal', 'header', 'slug', 'page_type']
#
#    add_columns = ['id', 'portal', 'header', 'slug', 'page_type']
#    add_exclude_columns = [hide_list] #['id', 'portal', 'header', 'slug', 'page_type']
#
#    edit_columns = ['id', 'portal', 'header', 'slug', 'page_type']
#    edit_exclude_columns =[hide_list] # ['id', 'portal', 'header', 'slug', 'page_type']
#
#    list_columns = ['id', 'portal', 'header', 'slug', 'page_type']
#    list_exclude_columns = [] # ['id', 'portal', 'header', 'slug', 'page_type']
#
#    search_columns = ['id', 'portal', 'header', 'slug', 'page_type']
#    search_exclude_columns= [] # ['id', 'portal', 'header', 'slug', 'page_type']
#
#    default_sort = [('id', True)]
#    base_permissions = ['can_list', 'can_show', 'can_edit', 'can_delete', 'can_add']
#    label_columns=   [{column.name: column.name for column in table.columns} ]
#    show_template =  'appbuilder/general/model/show_cascade.html'
#    list_template = 'appbuilder/general/model/list.html'
#    add_template = 'appbuilder/general/model/add.html'
#    edit_template = 'appbuilder/general/model/edit.html'
#    add_widget = (FormVerticalWidget|FormInlineWidget)
#    show_widget = ShowBlockWidget
#    list_widget = (ListThumbnail|ListWidget)
#    base_order = ('name', 'asc')
#    list_widget= 'list_widget'


class ProfileMasterView(MasterDetailView):
    datamodel=SQLAInterface(Profile, db.session)
    related_views = [IndividualDetailView]
    show_title='Profile Detail'
    add_title ='Add Profile'
    list_title= 'Profile List'
    edit_title = 'Edit Profile'
    show_columns = ['id', 'individual', 'import_address', 'profile_username', 'profile_password', 'has_been_imported', 'import_data', 'import_date', 'profilesource']
#    show_exclude_columns = [] #= ['id', 'individual', 'import_address', 'profile_username', 'profile_password', 'has_been_imported', 'import_data', 'import_date', 'profilesource']
#
#    add_columns = ['id', 'individual', 'import_address', 'profile_username', 'profile_password', 'has_been_imported', 'import_data', 'import_date', 'profilesource']
#    add_exclude_columns = [hide_list] #['id', 'individual', 'import_address', 'profile_username', 'profile_password', 'has_been_imported', 'import_data', 'import_date', 'profilesource']
#
#    edit_columns = ['id', 'individual', 'import_address', 'profile_username', 'profile_password', 'has_been_imported', 'import_data', 'import_date', 'profilesource']
#    edit_exclude_columns =[hide_list] # ['id', 'individual', 'import_address', 'profile_username', 'profile_password', 'has_been_imported', 'import_data', 'import_date', 'profilesource']
#
#    list_columns = ['id', 'individual', 'import_address', 'profile_username', 'profile_password', 'has_been_imported', 'import_data', 'import_date', 'profilesource']
#    list_exclude_columns = [] # ['id', 'individual', 'import_address', 'profile_username', 'profile_password', 'has_been_imported', 'import_data', 'import_date', 'profilesource']
#
#    search_columns = ['id', 'individual', 'import_address', 'profile_username', 'profile_password', 'has_been_imported', 'import_data', 'import_date', 'profilesource']
#    search_exclude_columns= [] # ['id', 'individual', 'import_address', 'profile_username', 'profile_password', 'has_been_imported', 'import_data', 'import_date', 'profilesource']
#
#    default_sort = [('id', True)]
#    base_permissions = ['can_list', 'can_show', 'can_edit', 'can_delete', 'can_add']
#    label_columns=   [{column.name: column.name for column in table.columns} ]
#    show_template =  'appbuilder/general/model/show_cascade.html'
#    list_template = 'appbuilder/general/model/list.html'
#    add_template = 'appbuilder/general/model/add.html'
#    edit_template = 'appbuilder/general/model/edit.html'
#    add_widget = (FormVerticalWidget|FormInlineWidget)
#    show_widget = ShowBlockWidget
#    list_widget = (ListThumbnail|ListWidget)
#    base_order = ('name', 'asc')
#    list_widget= 'list_widget'


class ProfileMultiView(MultipleView):
    datamodel=SQLAInterface(Profile, db.session)
    views = [ProfilesourceDetailView]
    show_title='Profile Detail'
    add_title ='Add Profile'
    list_title= 'Profile List'
    edit_title = 'Edit Profile'
    show_columns = ['id', 'individual', 'import_address', 'profile_username', 'profile_password', 'has_been_imported', 'import_data', 'import_date', 'profilesource']
#    show_exclude_columns = [] #= ['id', 'individual', 'import_address', 'profile_username', 'profile_password', 'has_been_imported', 'import_data', 'import_date', 'profilesource']
#
#    add_columns = ['id', 'individual', 'import_address', 'profile_username', 'profile_password', 'has_been_imported', 'import_data', 'import_date', 'profilesource']
#    add_exclude_columns = [hide_list] #['id', 'individual', 'import_address', 'profile_username', 'profile_password', 'has_been_imported', 'import_data', 'import_date', 'profilesource']
#
#    edit_columns = ['id', 'individual', 'import_address', 'profile_username', 'profile_password', 'has_been_imported', 'import_data', 'import_date', 'profilesource']
#    edit_exclude_columns =[hide_list] # ['id', 'individual', 'import_address', 'profile_username', 'profile_password', 'has_been_imported', 'import_data', 'import_date', 'profilesource']
#
#    list_columns = ['id', 'individual', 'import_address', 'profile_username', 'profile_password', 'has_been_imported', 'import_data', 'import_date', 'profilesource']
#    list_exclude_columns = [] # ['id', 'individual', 'import_address', 'profile_username', 'profile_password', 'has_been_imported', 'import_data', 'import_date', 'profilesource']
#
#    search_columns = ['id', 'individual', 'import_address', 'profile_username', 'profile_password', 'has_been_imported', 'import_data', 'import_date', 'profilesource']
#    search_exclude_columns= [] # ['id', 'individual', 'import_address', 'profile_username', 'profile_password', 'has_been_imported', 'import_data', 'import_date', 'profilesource']
#
#    default_sort = [('id', True)]
#    base_permissions = ['can_list', 'can_show', 'can_edit', 'can_delete', 'can_add']
#    label_columns=   [{column.name: column.name for column in table.columns} ]
#    show_template =  'appbuilder/general/model/show_cascade.html'
#    list_template = 'appbuilder/general/model/list.html'
#    add_template = 'appbuilder/general/model/add.html'
#    edit_template = 'appbuilder/general/model/edit.html'
#    add_widget = (FormVerticalWidget|FormInlineWidget)
#    show_widget = ShowBlockWidget
#    list_widget = (ListThumbnail|ListWidget)
#    base_order = ('name', 'asc')
#    list_widget= 'list_widget'


class ResumeMasterView(MasterDetailView):
    datamodel=SQLAInterface(Resume, db.session)
    related_views = [IndividualDetailView]
    show_title='Resume Detail'
    add_title ='Add Resume'
    list_title= 'Resume List'
    edit_title = 'Edit Resume'
    show_columns = ['id', 'individual', 'template', 'header', 'color', 'location', 'summary_text', 'has_been_generated', 'preferred']
#    show_exclude_columns = [] #= ['id', 'individual', 'template', 'header', 'color', 'location', 'summary_text', 'has_been_generated', 'preferred']
#
#    add_columns = ['id', 'individual', 'template', 'header', 'color', 'location', 'summary_text', 'has_been_generated', 'preferred']
#    add_exclude_columns = [hide_list] #['id', 'individual', 'template', 'header', 'color', 'location', 'summary_text', 'has_been_generated', 'preferred']
#
#    edit_columns = ['id', 'individual', 'template', 'header', 'color', 'location', 'summary_text', 'has_been_generated', 'preferred']
#    edit_exclude_columns =[hide_list] # ['id', 'individual', 'template', 'header', 'color', 'location', 'summary_text', 'has_been_generated', 'preferred']
#
#    list_columns = ['id', 'individual', 'template', 'header', 'color', 'location', 'summary_text', 'has_been_generated', 'preferred']
#    list_exclude_columns = [] # ['id', 'individual', 'template', 'header', 'color', 'location', 'summary_text', 'has_been_generated', 'preferred']
#
#    search_columns = ['id', 'individual', 'template', 'header', 'color', 'location', 'summary_text', 'has_been_generated', 'preferred']
#    search_exclude_columns= [] # ['id', 'individual', 'template', 'header', 'color', 'location', 'summary_text', 'has_been_generated', 'preferred']
#
#    default_sort = [('id', True)]
#    base_permissions = ['can_list', 'can_show', 'can_edit', 'can_delete', 'can_add']
#    label_columns=   [{column.name: column.name for column in table.columns} ]
#    show_template =  'appbuilder/general/model/show_cascade.html'
#    list_template = 'appbuilder/general/model/list.html'
#    add_template = 'appbuilder/general/model/add.html'
#    edit_template = 'appbuilder/general/model/edit.html'
#    add_widget = (FormVerticalWidget|FormInlineWidget)
#    show_widget = ShowBlockWidget
#    list_widget = (ListThumbnail|ListWidget)
#    base_order = ('name', 'asc')
#    list_widget= 'list_widget'


class ResumeMultiView(MultipleView):
    datamodel=SQLAInterface(Resume, db.session)
    views = [LocationDetailView]
    show_title='Resume Detail'
    add_title ='Add Resume'
    list_title= 'Resume List'
    edit_title = 'Edit Resume'
    show_columns = ['id', 'individual', 'template', 'header', 'color', 'location', 'summary_text', 'has_been_generated', 'preferred']
#    show_exclude_columns = [] #= ['id', 'individual', 'template', 'header', 'color', 'location', 'summary_text', 'has_been_generated', 'preferred']
#
#    add_columns = ['id', 'individual', 'template', 'header', 'color', 'location', 'summary_text', 'has_been_generated', 'preferred']
#    add_exclude_columns = [hide_list] #['id', 'individual', 'template', 'header', 'color', 'location', 'summary_text', 'has_been_generated', 'preferred']
#
#    edit_columns = ['id', 'individual', 'template', 'header', 'color', 'location', 'summary_text', 'has_been_generated', 'preferred']
#    edit_exclude_columns =[hide_list] # ['id', 'individual', 'template', 'header', 'color', 'location', 'summary_text', 'has_been_generated', 'preferred']
#
#    list_columns = ['id', 'individual', 'template', 'header', 'color', 'location', 'summary_text', 'has_been_generated', 'preferred']
#    list_exclude_columns = [] # ['id', 'individual', 'template', 'header', 'color', 'location', 'summary_text', 'has_been_generated', 'preferred']
#
#    search_columns = ['id', 'individual', 'template', 'header', 'color', 'location', 'summary_text', 'has_been_generated', 'preferred']
#    search_exclude_columns= [] # ['id', 'individual', 'template', 'header', 'color', 'location', 'summary_text', 'has_been_generated', 'preferred']
#
#    default_sort = [('id', True)]
#    base_permissions = ['can_list', 'can_show', 'can_edit', 'can_delete', 'can_add']
#    label_columns=   [{column.name: column.name for column in table.columns} ]
#    show_template =  'appbuilder/general/model/show_cascade.html'
#    list_template = 'appbuilder/general/model/list.html'
#    add_template = 'appbuilder/general/model/add.html'
#    edit_template = 'appbuilder/general/model/edit.html'
#    add_widget = (FormVerticalWidget|FormInlineWidget)
#    show_widget = ShowBlockWidget
#    list_widget = (ListThumbnail|ListWidget)
#    base_order = ('name', 'asc')
#    list_widget= 'list_widget'


class SwarmMasterView(MasterDetailView):
    datamodel=SQLAInterface(Swarm, db.session)
    related_views = [PortalDetailView]
    show_title='Swarm Detail'
    add_title ='Add Swarm'
    list_title= 'Swarm List'
    edit_title = 'Edit Swarm'
    show_columns = ['id', 'portal']
#    show_exclude_columns = [] #= ['id', 'portal']
#
#    add_columns = ['id', 'portal']
#    add_exclude_columns = [hide_list] #['id', 'portal']
#
#    edit_columns = ['id', 'portal']
#    edit_exclude_columns =[hide_list] # ['id', 'portal']
#
#    list_columns = ['id', 'portal']
#    list_exclude_columns = [] # ['id', 'portal']
#
#    search_columns = ['id', 'portal']
#    search_exclude_columns= [] # ['id', 'portal']
#
#    default_sort = [('id', True)]
#    base_permissions = ['can_list', 'can_show', 'can_edit', 'can_delete', 'can_add']
#    label_columns=   [{column.name: column.name for column in table.columns} ]
#    show_template =  'appbuilder/general/model/show_cascade.html'
#    list_template = 'appbuilder/general/model/list.html'
#    add_template = 'appbuilder/general/model/add.html'
#    edit_template = 'appbuilder/general/model/edit.html'
#    add_widget = (FormVerticalWidget|FormInlineWidget)
#    show_widget = ShowBlockWidget
#    list_widget = (ListThumbnail|ListWidget)
#    base_order = ('name', 'asc')
#    list_widget= 'list_widget'


class IndividualSwarmMasterView(MasterDetailView):
    datamodel=SQLAInterface(IndividualSwarm, db.session)
    related_views = [IndividualDetailView]
    show_title='IndividualSwarm Detail'
    add_title ='Add IndividualSwarm'
    list_title= 'IndividualSwarm List'
    edit_title = 'Edit IndividualSwarm'
    show_columns = ['individual', 'swarm']
#    show_exclude_columns = [] #= ['individual', 'swarm']
#
#    add_columns = ['individual', 'swarm']
#    add_exclude_columns = [hide_list] #['individual', 'swarm']
#
#    edit_columns = ['individual', 'swarm']
#    edit_exclude_columns =[hide_list] # ['individual', 'swarm']
#
#    list_columns = ['individual', 'swarm']
#    list_exclude_columns = [] # ['individual', 'swarm']
#
#    search_columns = ['individual', 'swarm']
#    search_exclude_columns= [] # ['individual', 'swarm']
#
#    default_sort = [('id', True)]
#    base_permissions = ['can_list', 'can_show', 'can_edit', 'can_delete', 'can_add']
#    label_columns=   [{column.name: column.name for column in table.columns} ]
#    show_template =  'appbuilder/general/model/show_cascade.html'
#    list_template = 'appbuilder/general/model/list.html'
#    add_template = 'appbuilder/general/model/add.html'
#    edit_template = 'appbuilder/general/model/edit.html'
#    add_widget = (FormVerticalWidget|FormInlineWidget)
#    show_widget = ShowBlockWidget
#    list_widget = (ListThumbnail|ListWidget)
#    base_order = ('name', 'asc')
#    list_widget= 'list_widget'


class IndividualSwarmMultiView(MultipleView):
    datamodel=SQLAInterface(IndividualSwarm, db.session)
    views = [SwarmDetailView]
    show_title='IndividualSwarm Detail'
    add_title ='Add IndividualSwarm'
    list_title= 'IndividualSwarm List'
    edit_title = 'Edit IndividualSwarm'
    show_columns = ['individual', 'swarm']
#    show_exclude_columns = [] #= ['individual', 'swarm']
#
#    add_columns = ['individual', 'swarm']
#    add_exclude_columns = [hide_list] #['individual', 'swarm']
#
#    edit_columns = ['individual', 'swarm']
#    edit_exclude_columns =[hide_list] # ['individual', 'swarm']
#
#    list_columns = ['individual', 'swarm']
#    list_exclude_columns = [] # ['individual', 'swarm']
#
#    search_columns = ['individual', 'swarm']
#    search_exclude_columns= [] # ['individual', 'swarm']
#
#    default_sort = [('id', True)]
#    base_permissions = ['can_list', 'can_show', 'can_edit', 'can_delete', 'can_add']
#    label_columns=   [{column.name: column.name for column in table.columns} ]
#    show_template =  'appbuilder/general/model/show_cascade.html'
#    list_template = 'appbuilder/general/model/list.html'
#    add_template = 'appbuilder/general/model/add.html'
#    edit_template = 'appbuilder/general/model/edit.html'
#    add_widget = (FormVerticalWidget|FormInlineWidget)
#    show_widget = ShowBlockWidget
#    list_widget = (ListThumbnail|ListWidget)
#    base_order = ('name', 'asc')
#    list_widget= 'list_widget'


class UserSkillView(ModelView):
    datamodel=SQLAInterface(UserSkill, db.session)
    related_views = []
    show_title='UserSkill Detail'
    add_title ='Add UserSkill'
    list_title= 'UserSkill List'
    edit_title = 'Edit UserSkill'
    show_columns = ['skills', 'user_details']
#    show_exclude_columns = [] #= ['skills', 'user_details']
#
#    add_columns = ['skills', 'user_details']
#    add_exclude_columns = [hide_list] #['skills', 'user_details']
#
#    edit_columns = ['skills', 'user_details']
#    edit_exclude_columns =[hide_list] # ['skills', 'user_details']
#
#    list_columns = ['skills', 'user_details']
#    list_exclude_columns = [] # ['skills', 'user_details']
#
#    search_columns = ['skills', 'user_details']
#    search_exclude_columns= [] # ['skills', 'user_details']
#
#    default_sort = [('id', True)]
#    base_permissions = ['can_list', 'can_show', 'can_edit', 'can_delete', 'can_add']
#    label_columns=   [{column.name: column.name for column in table.columns} ]
#    show_template =  'appbuilder/general/model/show_cascade.html'
#    list_template = 'appbuilder/general/model/list.html'
#    add_template = 'appbuilder/general/model/add.html'
#    edit_template = 'appbuilder/general/model/edit.html'
#    add_widget = (FormVerticalWidget|FormInlineWidget)
#    show_widget = ShowBlockWidget
#    list_widget = (ListThumbnail|ListWidget)
#    base_order = ('name', 'asc')
#    list_widget= 'list_widget'


class UserxDetailView(ModelView):
    datamodel=SQLAInterface(Userx, db.session)
    related_views = []
    show_title='Userx Detail'
    add_title ='Add Userx'
    list_title= 'Userx List'
    edit_title = 'Edit Userx'
    show_columns = ['id', 'userx', 'is_individual', 'is_institution', 'is_company', 'is_government', 'is_online']
#    show_exclude_columns = [] #= ['id', 'userx', 'is_individual', 'is_institution', 'is_company', 'is_government', 'is_online']
#
#    add_columns = ['id', 'userx', 'is_individual', 'is_institution', 'is_company', 'is_government', 'is_online']
#    add_exclude_columns = [hide_list] #['id', 'userx', 'is_individual', 'is_institution', 'is_company', 'is_government', 'is_online']
#
#    edit_columns = ['id', 'userx', 'is_individual', 'is_institution', 'is_company', 'is_government', 'is_online']
#    edit_exclude_columns =[hide_list] # ['id', 'userx', 'is_individual', 'is_institution', 'is_company', 'is_government', 'is_online']
#
#    list_columns = ['id', 'userx', 'is_individual', 'is_institution', 'is_company', 'is_government', 'is_online']
#    list_exclude_columns = [] # ['id', 'userx', 'is_individual', 'is_institution', 'is_company', 'is_government', 'is_online']
#
#    search_columns = ['id', 'userx', 'is_individual', 'is_institution', 'is_company', 'is_government', 'is_online']
#    search_exclude_columns= [] # ['id', 'userx', 'is_individual', 'is_institution', 'is_company', 'is_government', 'is_online']
#
#    default_sort = [('id', True)]
#    base_permissions = ['can_list', 'can_show', 'can_edit', 'can_delete', 'can_add']
#    label_columns=   [{column.name: column.name for column in table.columns} ]
#    show_template =  'appbuilder/general/model/show_cascade.html'
#    list_template = 'appbuilder/general/model/list.html'
#    add_template = 'appbuilder/general/model/add.html'
#    edit_template = 'appbuilder/general/model/edit.html'
#    add_widget = (FormVerticalWidget|FormInlineWidget)
#    show_widget = ShowBlockWidget
#    list_widget = (ListThumbnail|ListWidget)
#    base_order = ('name', 'asc')
#    list_widget= 'list_widget'


class IndividualDetailView(ModelView):
    datamodel=SQLAInterface(Individual, db.session)
    related_views = []
    show_title='Individual Detail'
    add_title ='Add Individual'
    list_title= 'Individual List'
    edit_title = 'Edit Individual'
    show_columns = ['id', 'userx', 'is_individual', 'is_institution', 'is_company', 'is_government', 'is_online']
#    show_exclude_columns = [] #= ['id', 'userx', 'is_individual', 'is_institution', 'is_company', 'is_government', 'is_online']
#
#    add_columns = ['id', 'userx', 'is_individual', 'is_institution', 'is_company', 'is_government', 'is_online']
#    add_exclude_columns = [hide_list] #['id', 'userx', 'is_individual', 'is_institution', 'is_company', 'is_government', 'is_online']
#
#    edit_columns = ['id', 'userx', 'is_individual', 'is_institution', 'is_company', 'is_government', 'is_online']
#    edit_exclude_columns =[hide_list] # ['id', 'userx', 'is_individual', 'is_institution', 'is_company', 'is_government', 'is_online']
#
#    list_columns = ['id', 'userx', 'is_individual', 'is_institution', 'is_company', 'is_government', 'is_online']
#    list_exclude_columns = [] # ['id', 'userx', 'is_individual', 'is_institution', 'is_company', 'is_government', 'is_online']
#
#    search_columns = ['id', 'userx', 'is_individual', 'is_institution', 'is_company', 'is_government', 'is_online']
#    search_exclude_columns= [] # ['id', 'userx', 'is_individual', 'is_institution', 'is_company', 'is_government', 'is_online']
#
#    default_sort = [('id', True)]
#    base_permissions = ['can_list', 'can_show', 'can_edit', 'can_delete', 'can_add']
#    label_columns=   [{column.name: column.name for column in table.columns} ]
#    show_template =  'appbuilder/general/model/show_cascade.html'
#    list_template = 'appbuilder/general/model/list.html'
#    add_template = 'appbuilder/general/model/add.html'
#    edit_template = 'appbuilder/general/model/edit.html'
#    add_widget = (FormVerticalWidget|FormInlineWidget)
#    show_widget = ShowBlockWidget
#    list_widget = (ListThumbnail|ListWidget)
#    base_order = ('name', 'asc')
#    list_widget= 'list_widget'


class IndustryDetailView(ModelView):
    datamodel=SQLAInterface(Industry, db.session)
    related_views = []
    show_title='Industry Detail'
    add_title ='Add Industry'
    list_title= 'Industry List'
    edit_title = 'Edit Industry'
    show_columns = ['industry', 'job']
#    show_exclude_columns = [] #= ['industry', 'job']
#
#    add_columns = ['industry', 'job']
#    add_exclude_columns = [hide_list] #['industry', 'job']
#
#    edit_columns = ['industry', 'job']
#    edit_exclude_columns =[hide_list] # ['industry', 'job']
#
#    list_columns = ['industry', 'job']
#    list_exclude_columns = [] # ['industry', 'job']
#
#    search_columns = ['industry', 'job']
#    search_exclude_columns= [] # ['industry', 'job']
#
#    default_sort = [('id', True)]
#    base_permissions = ['can_list', 'can_show', 'can_edit', 'can_delete', 'can_add']
#    label_columns=   [{column.name: column.name for column in table.columns} ]
#    show_template =  'appbuilder/general/model/show_cascade.html'
#    list_template = 'appbuilder/general/model/list.html'
#    add_template = 'appbuilder/general/model/add.html'
#    edit_template = 'appbuilder/general/model/edit.html'
#    add_widget = (FormVerticalWidget|FormInlineWidget)
#    show_widget = ShowBlockWidget
#    list_widget = (ListThumbnail|ListWidget)
#    base_order = ('name', 'asc')
#    list_widget= 'list_widget'


class IndustryJobDetailView(ModelView):
    datamodel=SQLAInterface(IndustryJob, db.session)
    related_views = []
    show_title='IndustryJob Detail'
    add_title ='Add IndustryJob'
    list_title= 'IndustryJob List'
    edit_title = 'Edit IndustryJob'
    show_columns = ['industry', 'job']
#    show_exclude_columns = [] #= ['industry', 'job']
#
#    add_columns = ['industry', 'job']
#    add_exclude_columns = [hide_list] #['industry', 'job']
#
#    edit_columns = ['industry', 'job']
#    edit_exclude_columns =[hide_list] # ['industry', 'job']
#
#    list_columns = ['industry', 'job']
#    list_exclude_columns = [] # ['industry', 'job']
#
#    search_columns = ['industry', 'job']
#    search_exclude_columns= [] # ['industry', 'job']
#
#    default_sort = [('id', True)]
#    base_permissions = ['can_list', 'can_show', 'can_edit', 'can_delete', 'can_add']
#    label_columns=   [{column.name: column.name for column in table.columns} ]
#    show_template =  'appbuilder/general/model/show_cascade.html'
#    list_template = 'appbuilder/general/model/list.html'
#    add_template = 'appbuilder/general/model/add.html'
#    edit_template = 'appbuilder/general/model/edit.html'
#    add_widget = (FormVerticalWidget|FormInlineWidget)
#    show_widget = ShowBlockWidget
#    list_widget = (ListThumbnail|ListWidget)
#    base_order = ('name', 'asc')
#    list_widget= 'list_widget'


class JobDetailView(ModelView):
    datamodel=SQLAInterface(Job, db.session)
    related_views = []
    show_title='Job Detail'
    add_title ='Add Job'
    list_title= 'Job List'
    edit_title = 'Edit Job'
    show_columns = ['industry', 'job']
#    show_exclude_columns = [] #= ['industry', 'job']
#
#    add_columns = ['industry', 'job']
#    add_exclude_columns = [hide_list] #['industry', 'job']
#
#    edit_columns = ['industry', 'job']
#    edit_exclude_columns =[hide_list] # ['industry', 'job']
#
#    list_columns = ['industry', 'job']
#    list_exclude_columns = [] # ['industry', 'job']
#
#    search_columns = ['industry', 'job']
#    search_exclude_columns= [] # ['industry', 'job']
#
#    default_sort = [('id', True)]
#    base_permissions = ['can_list', 'can_show', 'can_edit', 'can_delete', 'can_add']
#    label_columns=   [{column.name: column.name for column in table.columns} ]
#    show_template =  'appbuilder/general/model/show_cascade.html'
#    list_template = 'appbuilder/general/model/list.html'
#    add_template = 'appbuilder/general/model/add.html'
#    edit_template = 'appbuilder/general/model/edit.html'
#    add_widget = (FormVerticalWidget|FormInlineWidget)
#    show_widget = ShowBlockWidget
#    list_widget = (ListThumbnail|ListWidget)
#    base_order = ('name', 'asc')
#    list_widget= 'list_widget'




class SkillDetailView(ModelView):
    datamodel=SQLAInterface(Skill, db.session)
    related_views = []
    show_title='Skill Detail'
    add_title ='Add Skill'
    list_title= 'Skill List'
    edit_title = 'Edit Skill'
    show_columns = ['skills', 'jobs']
#    show_exclude_columns = [] #= ['skills', 'jobs']
#
#    add_columns = ['skills', 'jobs']
#    add_exclude_columns = [hide_list] #['skills', 'jobs']
#
#    edit_columns = ['skills', 'jobs']
#    edit_exclude_columns =[hide_list] # ['skills', 'jobs']
#
#    list_columns = ['skills', 'jobs']
#    list_exclude_columns = [] # ['skills', 'jobs']
#
#    search_columns = ['skills', 'jobs']
#    search_exclude_columns= [] # ['skills', 'jobs']
#
#    default_sort = [('id', True)]
#    base_permissions = ['can_list', 'can_show', 'can_edit', 'can_delete', 'can_add']
#    label_columns=   [{column.name: column.name for column in table.columns} ]
#    show_template =  'appbuilder/general/model/show_cascade.html'
#    list_template = 'appbuilder/general/model/list.html'
#    add_template = 'appbuilder/general/model/add.html'
#    edit_template = 'appbuilder/general/model/edit.html'
#    add_widget = (FormVerticalWidget|FormInlineWidget)
#    show_widget = ShowBlockWidget
#    list_widget = (ListThumbnail|ListWidget)
#    base_order = ('name', 'asc')
#    list_widget= 'list_widget'


class JobSkillDetailView(ModelView):
    datamodel=SQLAInterface(JobSkill, db.session)
    related_views = []
    show_title='JobSkill Detail'
    add_title ='Add JobSkill'
    list_title= 'JobSkill List'
    edit_title = 'Edit JobSkill'
    show_columns = ['skills', 'jobs']
#    show_exclude_columns = [] #= ['skills', 'jobs']
#
#    add_columns = ['skills', 'jobs']
#    add_exclude_columns = [hide_list] #['skills', 'jobs']
#
#    edit_columns = ['skills', 'jobs']
#    edit_exclude_columns =[hide_list] # ['skills', 'jobs']
#
#    list_columns = ['skills', 'jobs']
#    list_exclude_columns = [] # ['skills', 'jobs']
#
#    search_columns = ['skills', 'jobs']
#    search_exclude_columns= [] # ['skills', 'jobs']
#
#    default_sort = [('id', True)]
#    base_permissions = ['can_list', 'can_show', 'can_edit', 'can_delete', 'can_add']
#    label_columns=   [{column.name: column.name for column in table.columns} ]
#    show_template =  'appbuilder/general/model/show_cascade.html'
#    list_template = 'appbuilder/general/model/list.html'
#    add_template = 'appbuilder/general/model/add.html'
#    edit_template = 'appbuilder/general/model/edit.html'
#    add_widget = (FormVerticalWidget|FormInlineWidget)
#    show_widget = ShowBlockWidget
#    list_widget = (ListThumbnail|ListWidget)
#    base_order = ('name', 'asc')
#    list_widget= 'list_widget'


class PortalDetailView(ModelView):
    datamodel=SQLAInterface(Portal, db.session)
    related_views = []
    show_title='Portal Detail'
    add_title ='Add Portal'
    list_title= 'Portal List'
    edit_title = 'Edit Portal'
    show_columns = ['id', 'portal', 'header', 'slug', 'page_type']
#    show_exclude_columns = [] #= ['id', 'portal', 'header', 'slug', 'page_type']
#
#    add_columns = ['id', 'portal', 'header', 'slug', 'page_type']
#    add_exclude_columns = [hide_list] #['id', 'portal', 'header', 'slug', 'page_type']
#
#    edit_columns = ['id', 'portal', 'header', 'slug', 'page_type']
#    edit_exclude_columns =[hide_list] # ['id', 'portal', 'header', 'slug', 'page_type']
#
#    list_columns = ['id', 'portal', 'header', 'slug', 'page_type']
#    list_exclude_columns = [] # ['id', 'portal', 'header', 'slug', 'page_type']
#
#    search_columns = ['id', 'portal', 'header', 'slug', 'page_type']
#    search_exclude_columns= [] # ['id', 'portal', 'header', 'slug', 'page_type']
#
#    default_sort = [('id', True)]
#    base_permissions = ['can_list', 'can_show', 'can_edit', 'can_delete', 'can_add']
#    label_columns=   [{column.name: column.name for column in table.columns} ]
#    show_template =  'appbuilder/general/model/show_cascade.html'
#    list_template = 'appbuilder/general/model/list.html'
#    add_template = 'appbuilder/general/model/add.html'
#    edit_template = 'appbuilder/general/model/edit.html'
#    add_widget = (FormVerticalWidget|FormInlineWidget)
#    show_widget = ShowBlockWidget
#    list_widget = (ListThumbnail|ListWidget)
#    base_order = ('name', 'asc')
#    list_widget= 'list_widget'


class PageDetailView(ModelView):
    datamodel=SQLAInterface(Page, db.session)
    related_views = []
    show_title='Page Detail'
    add_title ='Add Page'
    list_title= 'Page List'
    edit_title = 'Edit Page'
    show_columns = ['id', 'portal', 'header', 'slug', 'page_type']
#    show_exclude_columns = [] #= ['id', 'portal', 'header', 'slug', 'page_type']
#
#    add_columns = ['id', 'portal', 'header', 'slug', 'page_type']
#    add_exclude_columns = [hide_list] #['id', 'portal', 'header', 'slug', 'page_type']
#
#    edit_columns = ['id', 'portal', 'header', 'slug', 'page_type']
#    edit_exclude_columns =[hide_list] # ['id', 'portal', 'header', 'slug', 'page_type']
#
#    list_columns = ['id', 'portal', 'header', 'slug', 'page_type']
#    list_exclude_columns = [] # ['id', 'portal', 'header', 'slug', 'page_type']
#
#    search_columns = ['id', 'portal', 'header', 'slug', 'page_type']
#    search_exclude_columns= [] # ['id', 'portal', 'header', 'slug', 'page_type']
#
#    default_sort = [('id', True)]
#    base_permissions = ['can_list', 'can_show', 'can_edit', 'can_delete', 'can_add']
#    label_columns=   [{column.name: column.name for column in table.columns} ]
#    show_template =  'appbuilder/general/model/show_cascade.html'
#    list_template = 'appbuilder/general/model/list.html'
#    add_template = 'appbuilder/general/model/add.html'
#    edit_template = 'appbuilder/general/model/edit.html'
#    add_widget = (FormVerticalWidget|FormInlineWidget)
#    show_widget = ShowBlockWidget
#    list_widget = (ListThumbnail|ListWidget)
#    base_order = ('name', 'asc')
#    list_widget= 'list_widget'


class ProfilesourceDetailView(ModelView):
    datamodel=SQLAInterface(Profilesource, db.session)
    related_views = []
    show_title='Profilesource Detail'
    add_title ='Add Profilesource'
    list_title= 'Profilesource List'
    edit_title = 'Edit Profilesource'
    show_columns = ['id', 'individual', 'import_address', 'profile_username', 'profile_password', 'has_been_imported', 'import_data', 'import_date', 'profilesource']
#    show_exclude_columns = [] #= ['id', 'individual', 'import_address', 'profile_username', 'profile_password', 'has_been_imported', 'import_data', 'import_date', 'profilesource']
#
#    add_columns = ['id', 'individual', 'import_address', 'profile_username', 'profile_password', 'has_been_imported', 'import_data', 'import_date', 'profilesource']
#    add_exclude_columns = [hide_list] #['id', 'individual', 'import_address', 'profile_username', 'profile_password', 'has_been_imported', 'import_data', 'import_date', 'profilesource']
#
#    edit_columns = ['id', 'individual', 'import_address', 'profile_username', 'profile_password', 'has_been_imported', 'import_data', 'import_date', 'profilesource']
#    edit_exclude_columns =[hide_list] # ['id', 'individual', 'import_address', 'profile_username', 'profile_password', 'has_been_imported', 'import_data', 'import_date', 'profilesource']
#
#    list_columns = ['id', 'individual', 'import_address', 'profile_username', 'profile_password', 'has_been_imported', 'import_data', 'import_date', 'profilesource']
#    list_exclude_columns = [] # ['id', 'individual', 'import_address', 'profile_username', 'profile_password', 'has_been_imported', 'import_data', 'import_date', 'profilesource']
#
#    search_columns = ['id', 'individual', 'import_address', 'profile_username', 'profile_password', 'has_been_imported', 'import_data', 'import_date', 'profilesource']
#    search_exclude_columns= [] # ['id', 'individual', 'import_address', 'profile_username', 'profile_password', 'has_been_imported', 'import_data', 'import_date', 'profilesource']
#
#    default_sort = [('id', True)]
#    base_permissions = ['can_list', 'can_show', 'can_edit', 'can_delete', 'can_add']
#    label_columns=   [{column.name: column.name for column in table.columns} ]
#    show_template =  'appbuilder/general/model/show_cascade.html'
#    list_template = 'appbuilder/general/model/list.html'
#    add_template = 'appbuilder/general/model/add.html'
#    edit_template = 'appbuilder/general/model/edit.html'
#    add_widget = (FormVerticalWidget|FormInlineWidget)
#    show_widget = ShowBlockWidget
#    list_widget = (ListThumbnail|ListWidget)
#    base_order = ('name', 'asc')
#    list_widget= 'list_widget'


class ProfileDetailView(ModelView):
    datamodel=SQLAInterface(Profile, db.session)
    related_views = []
    show_title='Profile Detail'
    add_title ='Add Profile'
    list_title= 'Profile List'
    edit_title = 'Edit Profile'
    show_columns = ['id', 'individual', 'import_address', 'profile_username', 'profile_password', 'has_been_imported', 'import_data', 'import_date', 'profilesource']
#    show_exclude_columns = [] #= ['id', 'individual', 'import_address', 'profile_username', 'profile_password', 'has_been_imported', 'import_data', 'import_date', 'profilesource']
#
#    add_columns = ['id', 'individual', 'import_address', 'profile_username', 'profile_password', 'has_been_imported', 'import_data', 'import_date', 'profilesource']
#    add_exclude_columns = [hide_list] #['id', 'individual', 'import_address', 'profile_username', 'profile_password', 'has_been_imported', 'import_data', 'import_date', 'profilesource']
#
#    edit_columns = ['id', 'individual', 'import_address', 'profile_username', 'profile_password', 'has_been_imported', 'import_data', 'import_date', 'profilesource']
#    edit_exclude_columns =[hide_list] # ['id', 'individual', 'import_address', 'profile_username', 'profile_password', 'has_been_imported', 'import_data', 'import_date', 'profilesource']
#
#    list_columns = ['id', 'individual', 'import_address', 'profile_username', 'profile_password', 'has_been_imported', 'import_data', 'import_date', 'profilesource']
#    list_exclude_columns = [] # ['id', 'individual', 'import_address', 'profile_username', 'profile_password', 'has_been_imported', 'import_data', 'import_date', 'profilesource']
#
#    search_columns = ['id', 'individual', 'import_address', 'profile_username', 'profile_password', 'has_been_imported', 'import_data', 'import_date', 'profilesource']
#    search_exclude_columns= [] # ['id', 'individual', 'import_address', 'profile_username', 'profile_password', 'has_been_imported', 'import_data', 'import_date', 'profilesource']
#
#    default_sort = [('id', True)]
#    base_permissions = ['can_list', 'can_show', 'can_edit', 'can_delete', 'can_add']
#    label_columns=   [{column.name: column.name for column in table.columns} ]
#    show_template =  'appbuilder/general/model/show_cascade.html'
#    list_template = 'appbuilder/general/model/list.html'
#    add_template = 'appbuilder/general/model/add.html'
#    edit_template = 'appbuilder/general/model/edit.html'
#    add_widget = (FormVerticalWidget|FormInlineWidget)
#    show_widget = ShowBlockWidget
#    list_widget = (ListThumbnail|ListWidget)
#    base_order = ('name', 'asc')
#    list_widget= 'list_widget'


class LocationDetailView(ModelView):
    datamodel=SQLAInterface(Location, db.session)
    related_views = []
    show_title='Location Detail'
    add_title ='Add Location'
    list_title= 'Location List'
    edit_title = 'Edit Location'
    show_columns = ['id', 'individual', 'template', 'header', 'color', 'location', 'summary_text', 'has_been_generated', 'preferred']
#    show_exclude_columns = [] #= ['id', 'individual', 'template', 'header', 'color', 'location', 'summary_text', 'has_been_generated', 'preferred']
#
#    add_columns = ['id', 'individual', 'template', 'header', 'color', 'location', 'summary_text', 'has_been_generated', 'preferred']
#    add_exclude_columns = [hide_list] #['id', 'individual', 'template', 'header', 'color', 'location', 'summary_text', 'has_been_generated', 'preferred']
#
#    edit_columns = ['id', 'individual', 'template', 'header', 'color', 'location', 'summary_text', 'has_been_generated', 'preferred']
#    edit_exclude_columns =[hide_list] # ['id', 'individual', 'template', 'header', 'color', 'location', 'summary_text', 'has_been_generated', 'preferred']
#
#    list_columns = ['id', 'individual', 'template', 'header', 'color', 'location', 'summary_text', 'has_been_generated', 'preferred']
#    list_exclude_columns = [] # ['id', 'individual', 'template', 'header', 'color', 'location', 'summary_text', 'has_been_generated', 'preferred']
#
#    search_columns = ['id', 'individual', 'template', 'header', 'color', 'location', 'summary_text', 'has_been_generated', 'preferred']
#    search_exclude_columns= [] # ['id', 'individual', 'template', 'header', 'color', 'location', 'summary_text', 'has_been_generated', 'preferred']
#
#    default_sort = [('id', True)]
#    base_permissions = ['can_list', 'can_show', 'can_edit', 'can_delete', 'can_add']
#    label_columns=   [{column.name: column.name for column in table.columns} ]
#    show_template =  'appbuilder/general/model/show_cascade.html'
#    list_template = 'appbuilder/general/model/list.html'
#    add_template = 'appbuilder/general/model/add.html'
#    edit_template = 'appbuilder/general/model/edit.html'
#    add_widget = (FormVerticalWidget|FormInlineWidget)
#    show_widget = ShowBlockWidget
#    list_widget = (ListThumbnail|ListWidget)
#    base_order = ('name', 'asc')
#    list_widget= 'list_widget'


class ResumeDetailView(ModelView):
    datamodel=SQLAInterface(Resume, db.session)
    related_views = []
    show_title='Resume Detail'
    add_title ='Add Resume'
    list_title= 'Resume List'
    edit_title = 'Edit Resume'
    show_columns = ['id', 'individual', 'template', 'header', 'color', 'location', 'summary_text', 'has_been_generated', 'preferred']
#    show_exclude_columns = [] #= ['id', 'individual', 'template', 'header', 'color', 'location', 'summary_text', 'has_been_generated', 'preferred']
#
#    add_columns = ['id', 'individual', 'template', 'header', 'color', 'location', 'summary_text', 'has_been_generated', 'preferred']
#    add_exclude_columns = [hide_list] #['id', 'individual', 'template', 'header', 'color', 'location', 'summary_text', 'has_been_generated', 'preferred']
#
#    edit_columns = ['id', 'individual', 'template', 'header', 'color', 'location', 'summary_text', 'has_been_generated', 'preferred']
#    edit_exclude_columns =[hide_list] # ['id', 'individual', 'template', 'header', 'color', 'location', 'summary_text', 'has_been_generated', 'preferred']
#
#    list_columns = ['id', 'individual', 'template', 'header', 'color', 'location', 'summary_text', 'has_been_generated', 'preferred']
#    list_exclude_columns = [] # ['id', 'individual', 'template', 'header', 'color', 'location', 'summary_text', 'has_been_generated', 'preferred']
#
#    search_columns = ['id', 'individual', 'template', 'header', 'color', 'location', 'summary_text', 'has_been_generated', 'preferred']
#    search_exclude_columns= [] # ['id', 'individual', 'template', 'header', 'color', 'location', 'summary_text', 'has_been_generated', 'preferred']
#
#    default_sort = [('id', True)]
#    base_permissions = ['can_list', 'can_show', 'can_edit', 'can_delete', 'can_add']
#    label_columns=   [{column.name: column.name for column in table.columns} ]
#    show_template =  'appbuilder/general/model/show_cascade.html'
#    list_template = 'appbuilder/general/model/list.html'
#    add_template = 'appbuilder/general/model/add.html'
#    edit_template = 'appbuilder/general/model/edit.html'
#    add_widget = (FormVerticalWidget|FormInlineWidget)
#    show_widget = ShowBlockWidget
#    list_widget = (ListThumbnail|ListWidget)
#    base_order = ('name', 'asc')
#    list_widget= 'list_widget'


class SwarmDetailView(ModelView):
    datamodel=SQLAInterface(Swarm, db.session)
    related_views = []
    show_title='Swarm Detail'
    add_title ='Add Swarm'
    list_title= 'Swarm List'
    edit_title = 'Edit Swarm'
    show_columns = ['individual', 'swarm']
#    show_exclude_columns = [] #= ['individual', 'swarm']
#
#    add_columns = ['individual', 'swarm']
#    add_exclude_columns = [hide_list] #['individual', 'swarm']
#
#    edit_columns = ['individual', 'swarm']
#    edit_exclude_columns =[hide_list] # ['individual', 'swarm']
#
#    list_columns = ['individual', 'swarm']
#    list_exclude_columns = [] # ['individual', 'swarm']
#
#    search_columns = ['individual', 'swarm']
#    search_exclude_columns= [] # ['individual', 'swarm']
#
#    default_sort = [('id', True)]
#    base_permissions = ['can_list', 'can_show', 'can_edit', 'can_delete', 'can_add']
#    label_columns=   [{column.name: column.name for column in table.columns} ]
#    show_template =  'appbuilder/general/model/show_cascade.html'
#    list_template = 'appbuilder/general/model/list.html'
#    add_template = 'appbuilder/general/model/add.html'
#    edit_template = 'appbuilder/general/model/edit.html'
#    add_widget = (FormVerticalWidget|FormInlineWidget)
#    show_widget = ShowBlockWidget
#    list_widget = (ListThumbnail|ListWidget)
#    base_order = ('name', 'asc')
#    list_widget= 'list_widget'


class IndividualSwarmDetailView(ModelView):
    datamodel=SQLAInterface(IndividualSwarm, db.session)
    related_views = []
    show_title='IndividualSwarm Detail'
    add_title ='Add IndividualSwarm'
    list_title= 'IndividualSwarm List'
    edit_title = 'Edit IndividualSwarm'
    show_columns = ['individual', 'swarm']
#    show_exclude_columns = [] #= ['individual', 'swarm']
#
#    add_columns = ['individual', 'swarm']
#    add_exclude_columns = [hide_list] #['individual', 'swarm']
#
#    edit_columns = ['individual', 'swarm']
#    edit_exclude_columns =[hide_list] # ['individual', 'swarm']
#
#    list_columns = ['individual', 'swarm']
#    list_exclude_columns = [] # ['individual', 'swarm']
#
#    search_columns = ['individual', 'swarm']
#    search_exclude_columns= [] # ['individual', 'swarm']
#
#    default_sort = [('id', True)]
#    base_permissions = ['can_list', 'can_show', 'can_edit', 'can_delete', 'can_add']
#    label_columns=   [{column.name: column.name for column in table.columns} ]
#    show_template =  'appbuilder/general/model/show_cascade.html'
#    list_template = 'appbuilder/general/model/list.html'
#    add_template = 'appbuilder/general/model/add.html'
#    edit_template = 'appbuilder/general/model/edit.html'
#    add_widget = (FormVerticalWidget|FormInlineWidget)
#    show_widget = ShowBlockWidget
#    list_widget = (ListThumbnail|ListWidget)
#    base_order = ('name', 'asc')
#    list_widget= 'list_widget'


class IndividualMasterView(MasterDetailView):
    datamodel=SQLAInterface(Individual, db.session)
    related_views = [UserxDetailView]
    show_title='Individual Detail'
    add_title ='Add Individual'
    list_title= 'Individual List'
    edit_title = 'Edit Individual'
    show_columns = ['id', 'userx', 'is_individual', 'is_institution', 'is_company', 'is_government', 'is_online']
#    show_exclude_columns = [] #= ['id', 'userx', 'is_individual', 'is_institution', 'is_company', 'is_government', 'is_online']
#
#    add_columns = ['id', 'userx', 'is_individual', 'is_institution', 'is_company', 'is_government', 'is_online']
#    add_exclude_columns = [hide_list] #['id', 'userx', 'is_individual', 'is_institution', 'is_company', 'is_government', 'is_online']
#
#    edit_columns = ['id', 'userx', 'is_individual', 'is_institution', 'is_company', 'is_government', 'is_online']
#    edit_exclude_columns =[hide_list] # ['id', 'userx', 'is_individual', 'is_institution', 'is_company', 'is_government', 'is_online']
#
#    list_columns = ['id', 'userx', 'is_individual', 'is_institution', 'is_company', 'is_government', 'is_online']
#    list_exclude_columns = [] # ['id', 'userx', 'is_individual', 'is_institution', 'is_company', 'is_government', 'is_online']
#
#    search_columns = ['id', 'userx', 'is_individual', 'is_institution', 'is_company', 'is_government', 'is_online']
#    search_exclude_columns= [] # ['id', 'userx', 'is_individual', 'is_institution', 'is_company', 'is_government', 'is_online']
#
#    default_sort = [('id', True)]
#    base_permissions = ['can_list', 'can_show', 'can_edit', 'can_delete', 'can_add']
#    label_columns=   [{column.name: column.name for column in table.columns} ]
#    show_template =  'appbuilder/general/model/show_cascade.html'
#    list_template = 'appbuilder/general/model/list.html'
#    add_template = 'appbuilder/general/model/add.html'
#    edit_template = 'appbuilder/general/model/edit.html'
#    add_widget = (FormVerticalWidget|FormInlineWidget)
#    show_widget = ShowBlockWidget
#    list_widget = (ListThumbnail|ListWidget)
#    base_order = ('name', 'asc')
#    list_widget= 'list_widget'


class IndustryJobMasterView(MasterDetailView):
    datamodel=SQLAInterface(IndustryJob, db.session)
    related_views = [IndustryDetailView]
    show_title='IndustryJob Detail'
    add_title ='Add IndustryJob'
    list_title= 'IndustryJob List'
    edit_title = 'Edit IndustryJob'
    show_columns = ['industry', 'job']
#    show_exclude_columns = [] #= ['industry', 'job']
#
#    add_columns = ['industry', 'job']
#    add_exclude_columns = [hide_list] #['industry', 'job']
#
#    edit_columns = ['industry', 'job']
#    edit_exclude_columns =[hide_list] # ['industry', 'job']
#
#    list_columns = ['industry', 'job']
#    list_exclude_columns = [] # ['industry', 'job']
#
#    search_columns = ['industry', 'job']
#    search_exclude_columns= [] # ['industry', 'job']
#
#    default_sort = [('id', True)]
#    base_permissions = ['can_list', 'can_show', 'can_edit', 'can_delete', 'can_add']
#    label_columns=   [{column.name: column.name for column in table.columns} ]
#    show_template =  'appbuilder/general/model/show_cascade.html'
#    list_template = 'appbuilder/general/model/list.html'
#    add_template = 'appbuilder/general/model/add.html'
#    edit_template = 'appbuilder/general/model/edit.html'
#    add_widget = (FormVerticalWidget|FormInlineWidget)
#    show_widget = ShowBlockWidget
#    list_widget = (ListThumbnail|ListWidget)
#    base_order = ('name', 'asc')
#    list_widget= 'list_widget'


class IndustryJobMultiView(MultipleView):
    datamodel=SQLAInterface(IndustryJob, db.session)
    views = [IndustryDetailView, JobDetailView]
    show_title='IndustryJob Detail'
    add_title ='Add IndustryJob'
    list_title= 'IndustryJob List'
    edit_title = 'Edit IndustryJob'
    show_columns = ['industry', 'job']
#    show_exclude_columns = [] #= ['industry', 'job']
#
#    add_columns = ['industry', 'job']
#    add_exclude_columns = [hide_list] #['industry', 'job']
#
#    edit_columns = ['industry', 'job']
#    edit_exclude_columns =[hide_list] # ['industry', 'job']
#
#    list_columns = ['industry', 'job']
#    list_exclude_columns = [] # ['industry', 'job']
#
#    search_columns = ['industry', 'job']
#    search_exclude_columns= [] # ['industry', 'job']
#
#    default_sort = [('id', True)]
#    base_permissions = ['can_list', 'can_show', 'can_edit', 'can_delete', 'can_add']
#    label_columns=   [{column.name: column.name for column in table.columns} ]
#    show_template =  'appbuilder/general/model/show_cascade.html'
#    list_template = 'appbuilder/general/model/list.html'
#    add_template = 'appbuilder/general/model/add.html'
#    edit_template = 'appbuilder/general/model/edit.html'
#    add_widget = (FormVerticalWidget|FormInlineWidget)
#    show_widget = ShowBlockWidget
#    list_widget = (ListThumbnail|ListWidget)
#    base_order = ('name', 'asc')
#    list_widget= 'list_widget'


class JobSkillMasterView(MasterDetailView):
    datamodel=SQLAInterface(JobSkill, db.session)
    related_views = [JobDetailView]
    show_title='JobSkill Detail'
    add_title ='Add JobSkill'
    list_title= 'JobSkill List'
    edit_title = 'Edit JobSkill'
    show_columns = ['skills', 'jobs']
#    show_exclude_columns = [] #= ['skills', 'jobs']
#
#    add_columns = ['skills', 'jobs']
#    add_exclude_columns = [hide_list] #['skills', 'jobs']
#
#    edit_columns = ['skills', 'jobs']
#    edit_exclude_columns =[hide_list] # ['skills', 'jobs']
#
#    list_columns = ['skills', 'jobs']
#    list_exclude_columns = [] # ['skills', 'jobs']
#
#    search_columns = ['skills', 'jobs']
#    search_exclude_columns= [] # ['skills', 'jobs']
#
#    default_sort = [('id', True)]
#    base_permissions = ['can_list', 'can_show', 'can_edit', 'can_delete', 'can_add']
#    label_columns=   [{column.name: column.name for column in table.columns} ]
#    show_template =  'appbuilder/general/model/show_cascade.html'
#    list_template = 'appbuilder/general/model/list.html'
#    add_template = 'appbuilder/general/model/add.html'
#    edit_template = 'appbuilder/general/model/edit.html'
#    add_widget = (FormVerticalWidget|FormInlineWidget)
#    show_widget = ShowBlockWidget
#    list_widget = (ListThumbnail|ListWidget)
#    base_order = ('name', 'asc')
#    list_widget= 'list_widget'


class JobSkillMultiView(MultipleView):
    datamodel=SQLAInterface(JobSkill, db.session)
    views = [SkillDetailView]
    show_title='JobSkill Detail'
    add_title ='Add JobSkill'
    list_title= 'JobSkill List'
    edit_title = 'Edit JobSkill'
    show_columns = ['skills', 'jobs']
#    show_exclude_columns = [] #= ['skills', 'jobs']
#
#    add_columns = ['skills', 'jobs']
#    add_exclude_columns = [hide_list] #['skills', 'jobs']
#
#    edit_columns = ['skills', 'jobs']
#    edit_exclude_columns =[hide_list] # ['skills', 'jobs']
#
#    list_columns = ['skills', 'jobs']
#    list_exclude_columns = [] # ['skills', 'jobs']
#
#    search_columns = ['skills', 'jobs']
#    search_exclude_columns= [] # ['skills', 'jobs']
#
#    default_sort = [('id', True)]
#    base_permissions = ['can_list', 'can_show', 'can_edit', 'can_delete', 'can_add']
#    label_columns=   [{column.name: column.name for column in table.columns} ]
#    show_template =  'appbuilder/general/model/show_cascade.html'
#    list_template = 'appbuilder/general/model/list.html'
#    add_template = 'appbuilder/general/model/add.html'
#    edit_template = 'appbuilder/general/model/edit.html'
#    add_widget = (FormVerticalWidget|FormInlineWidget)
#    show_widget = ShowBlockWidget
#    list_widget = (ListThumbnail|ListWidget)
#    base_order = ('name', 'asc')
#    list_widget= 'list_widget'


class EducationMasterView(MasterDetailView):
    datamodel=SQLAInterface(Education, db.session)
    related_views = [IndividualDetailView]
    show_title='Education Detail'
    add_title ='Add Education'
    list_title= 'Education List'
    edit_title = 'Edit Education'
    show_columns = ['id', 'individual', 'qualification', 'qual_class', 'verified', 'verification_code', 'verified_by', 'verification_date', 'verification_doc']
#    show_exclude_columns = [] #= ['id', 'individual', 'qualification', 'qual_class', 'verified', 'verification_code', 'verified_by', 'verification_date', 'verification_doc']
#
#    add_columns = ['id', 'individual', 'qualification', 'qual_class', 'verified', 'verification_code', 'verified_by', 'verification_date', 'verification_doc']
#    add_exclude_columns = [hide_list] #['id', 'individual', 'qualification', 'qual_class', 'verified', 'verification_code', 'verified_by', 'verification_date', 'verification_doc']
#
#    edit_columns = ['id', 'individual', 'qualification', 'qual_class', 'verified', 'verification_code', 'verified_by', 'verification_date', 'verification_doc']
#    edit_exclude_columns =[hide_list] # ['id', 'individual', 'qualification', 'qual_class', 'verified', 'verification_code', 'verified_by', 'verification_date', 'verification_doc']
#
#    list_columns = ['id', 'individual', 'qualification', 'qual_class', 'verified', 'verification_code', 'verified_by', 'verification_date', 'verification_doc']
#    list_exclude_columns = [] # ['id', 'individual', 'qualification', 'qual_class', 'verified', 'verification_code', 'verified_by', 'verification_date', 'verification_doc']
#
#    search_columns = ['id', 'individual', 'qualification', 'qual_class', 'verified', 'verification_code', 'verified_by', 'verification_date', 'verification_doc']
#    search_exclude_columns= [] # ['id', 'individual', 'qualification', 'qual_class', 'verified', 'verification_code', 'verified_by', 'verification_date', 'verification_doc']
#
#    default_sort = [('id', True)]
#    base_permissions = ['can_list', 'can_show', 'can_edit', 'can_delete', 'can_add']
#    label_columns=   [{column.name: column.name for column in table.columns} ]
#    show_template =  'appbuilder/general/model/show_cascade.html'
#    list_template = 'appbuilder/general/model/list.html'
#    add_template = 'appbuilder/general/model/add.html'
#    edit_template = 'appbuilder/general/model/edit.html'
#    add_widget = (FormVerticalWidget|FormInlineWidget)
#    show_widget = ShowBlockWidget
#    list_widget = (ListThumbnail|ListWidget)
#    base_order = ('name', 'asc')
#    list_widget= 'list_widget'


class IndividualJobMasterView(MasterDetailView):
    datamodel=SQLAInterface(IndividualJob, db.session)
    related_views = [IndividualDetailView]
    show_title='IndividualJob Detail'
    add_title ='Add IndividualJob'
    list_title= 'IndividualJob List'
    edit_title = 'Edit IndividualJob'
    show_columns = ['individual', 'job']
#    show_exclude_columns = [] #= ['individual', 'job']
#
#    add_columns = ['individual', 'job']
#    add_exclude_columns = [hide_list] #['individual', 'job']
#
#    edit_columns = ['individual', 'job']
#    edit_exclude_columns =[hide_list] # ['individual', 'job']
#
#    list_columns = ['individual', 'job']
#    list_exclude_columns = [] # ['individual', 'job']
#
#    search_columns = ['individual', 'job']
#    search_exclude_columns= [] # ['individual', 'job']
#
#    default_sort = [('id', True)]
#    base_permissions = ['can_list', 'can_show', 'can_edit', 'can_delete', 'can_add']
#    label_columns=   [{column.name: column.name for column in table.columns} ]
#    show_template =  'appbuilder/general/model/show_cascade.html'
#    list_template = 'appbuilder/general/model/list.html'
#    add_template = 'appbuilder/general/model/add.html'
#    edit_template = 'appbuilder/general/model/edit.html'
#    add_widget = (FormVerticalWidget|FormInlineWidget)
#    show_widget = ShowBlockWidget
#    list_widget = (ListThumbnail|ListWidget)
#    base_order = ('name', 'asc')
#    list_widget= 'list_widget'


class IndividualJobMultiView(MultipleView):
    datamodel=SQLAInterface(IndividualJob, db.session)
    views = []
    show_title='IndividualJob Detail'
    add_title ='Add IndividualJob'
    list_title= 'IndividualJob List'
    edit_title = 'Edit IndividualJob'
    show_columns = ['individual', 'job']
#    show_exclude_columns = [] #= ['individual', 'job']
#
#    add_columns = ['individual', 'job']
#    add_exclude_columns = [hide_list] #['individual', 'job']
#
#    edit_columns = ['individual', 'job']
#    edit_exclude_columns =[hide_list] # ['individual', 'job']
#
#    list_columns = ['individual', 'job']
#    list_exclude_columns = [] # ['individual', 'job']
#
#    search_columns = ['individual', 'job']
#    search_exclude_columns= [] # ['individual', 'job']
#
#    default_sort = [('id', True)]
#    base_permissions = ['can_list', 'can_show', 'can_edit', 'can_delete', 'can_add']
#    label_columns=   [{column.name: column.name for column in table.columns} ]
#    show_template =  'appbuilder/general/model/show_cascade.html'
#    list_template = 'appbuilder/general/model/list.html'
#    add_template = 'appbuilder/general/model/add.html'
#    edit_template = 'appbuilder/general/model/edit.html'
#    add_widget = (FormVerticalWidget|FormInlineWidget)
#    show_widget = ShowBlockWidget
#    list_widget = (ListThumbnail|ListWidget)
#    base_order = ('name', 'asc')
#    list_widget= 'list_widget'


class LocationMasterView(MasterDetailView):
    datamodel=SQLAInterface(Location, db.session)
    related_views = [IndividualDetailView]
    show_title='Location Detail'
    add_title ='Add Location'
    list_title= 'Location List'
    edit_title = 'Edit Location'
    show_columns = ['id', 'individual']
#    show_exclude_columns = [] #= ['id', 'individual']
#
#    add_columns = ['id', 'individual']
#    add_exclude_columns = [hide_list] #['id', 'individual']
#
#    edit_columns = ['id', 'individual']
#    edit_exclude_columns =[hide_list] # ['id', 'individual']
#
#    list_columns = ['id', 'individual']
#    list_exclude_columns = [] # ['id', 'individual']
#
#    search_columns = ['id', 'individual']
#    search_exclude_columns= [] # ['id', 'individual']
#
#    default_sort = [('id', True)]
#    base_permissions = ['can_list', 'can_show', 'can_edit', 'can_delete', 'can_add']
#    label_columns=   [{column.name: column.name for column in table.columns} ]
#    show_template =  'appbuilder/general/model/show_cascade.html'
#    list_template = 'appbuilder/general/model/list.html'
#    add_template = 'appbuilder/general/model/add.html'
#    edit_template = 'appbuilder/general/model/edit.html'
#    add_widget = (FormVerticalWidget|FormInlineWidget)
#    show_widget = ShowBlockWidget
#    list_widget = (ListThumbnail|ListWidget)
#    base_order = ('name', 'asc')
#    list_widget= 'list_widget'


class PortalMasterView(MasterDetailView):
    datamodel=SQLAInterface(Portal, db.session)
    related_views = [IndividualDetailView]
    show_title='Portal Detail'
    add_title ='Add Portal'
    list_title= 'Portal List'
    edit_title = 'Edit Portal'
    show_columns = ['id', 'portal_url', 'is_primary', 'portal_state', 'individual', 'has_custom_domain', 'domain', 'header_text', 'slug', 'automatic_fulfillment_digital_products', 'default_digital_max_downloads', 'default_digital_url_valid_days', 'default_mail_sender_name', 'default_mail_sender_address', 'fulfillment_auto_approve', 'fulfillment_allow_unpaid', 'reserve_stock_duration_anonymous_user', 'reserve_stock_duration_authenticated_user', 'limit_quantity_per_checkout', 'gift_card_expiry_type', 'gift_card_expiry_period_type', 'gift_card_expiry_period', 'charge_taxes_on_shipping', 'include_taxes_in_prices', 'display_gross_prices', 'language']
#    show_exclude_columns = [] #= ['id', 'portal_url', 'is_primary', 'portal_state', 'individual', 'has_custom_domain', 'domain', 'header_text', 'slug', 'automatic_fulfillment_digital_products', 'default_digital_max_downloads', 'default_digital_url_valid_days', 'default_mail_sender_name', 'default_mail_sender_address', 'fulfillment_auto_approve', 'fulfillment_allow_unpaid', 'reserve_stock_duration_anonymous_user', 'reserve_stock_duration_authenticated_user', 'limit_quantity_per_checkout', 'gift_card_expiry_type', 'gift_card_expiry_period_type', 'gift_card_expiry_period', 'charge_taxes_on_shipping', 'include_taxes_in_prices', 'display_gross_prices', 'language']
#
#    add_columns = ['id', 'portal_url', 'is_primary', 'portal_state', 'individual', 'has_custom_domain', 'domain', 'header_text', 'slug', 'automatic_fulfillment_digital_products', 'default_digital_max_downloads', 'default_digital_url_valid_days', 'default_mail_sender_name', 'default_mail_sender_address', 'fulfillment_auto_approve', 'fulfillment_allow_unpaid', 'reserve_stock_duration_anonymous_user', 'reserve_stock_duration_authenticated_user', 'limit_quantity_per_checkout', 'gift_card_expiry_type', 'gift_card_expiry_period_type', 'gift_card_expiry_period', 'charge_taxes_on_shipping', 'include_taxes_in_prices', 'display_gross_prices', 'language']
#    add_exclude_columns = [hide_list] #['id', 'portal_url', 'is_primary', 'portal_state', 'individual', 'has_custom_domain', 'domain', 'header_text', 'slug', 'automatic_fulfillment_digital_products', 'default_digital_max_downloads', 'default_digital_url_valid_days', 'default_mail_sender_name', 'default_mail_sender_address', 'fulfillment_auto_approve', 'fulfillment_allow_unpaid', 'reserve_stock_duration_anonymous_user', 'reserve_stock_duration_authenticated_user', 'limit_quantity_per_checkout', 'gift_card_expiry_type', 'gift_card_expiry_period_type', 'gift_card_expiry_period', 'charge_taxes_on_shipping', 'include_taxes_in_prices', 'display_gross_prices', 'language']
#
#    edit_columns = ['id', 'portal_url', 'is_primary', 'portal_state', 'individual', 'has_custom_domain', 'domain', 'header_text', 'slug', 'automatic_fulfillment_digital_products', 'default_digital_max_downloads', 'default_digital_url_valid_days', 'default_mail_sender_name', 'default_mail_sender_address', 'fulfillment_auto_approve', 'fulfillment_allow_unpaid', 'reserve_stock_duration_anonymous_user', 'reserve_stock_duration_authenticated_user', 'limit_quantity_per_checkout', 'gift_card_expiry_type', 'gift_card_expiry_period_type', 'gift_card_expiry_period', 'charge_taxes_on_shipping', 'include_taxes_in_prices', 'display_gross_prices', 'language']
#    edit_exclude_columns =[hide_list] # ['id', 'portal_url', 'is_primary', 'portal_state', 'individual', 'has_custom_domain', 'domain', 'header_text', 'slug', 'automatic_fulfillment_digital_products', 'default_digital_max_downloads', 'default_digital_url_valid_days', 'default_mail_sender_name', 'default_mail_sender_address', 'fulfillment_auto_approve', 'fulfillment_allow_unpaid', 'reserve_stock_duration_anonymous_user', 'reserve_stock_duration_authenticated_user', 'limit_quantity_per_checkout', 'gift_card_expiry_type', 'gift_card_expiry_period_type', 'gift_card_expiry_period', 'charge_taxes_on_shipping', 'include_taxes_in_prices', 'display_gross_prices', 'language']
#
#    list_columns = ['id', 'portal_url', 'is_primary', 'portal_state', 'individual', 'has_custom_domain', 'domain', 'header_text', 'slug', 'automatic_fulfillment_digital_products', 'default_digital_max_downloads', 'default_digital_url_valid_days', 'default_mail_sender_name', 'default_mail_sender_address', 'fulfillment_auto_approve', 'fulfillment_allow_unpaid', 'reserve_stock_duration_anonymous_user', 'reserve_stock_duration_authenticated_user', 'limit_quantity_per_checkout', 'gift_card_expiry_type', 'gift_card_expiry_period_type', 'gift_card_expiry_period', 'charge_taxes_on_shipping', 'include_taxes_in_prices', 'display_gross_prices', 'language']
#    list_exclude_columns = [] # ['id', 'portal_url', 'is_primary', 'portal_state', 'individual', 'has_custom_domain', 'domain', 'header_text', 'slug', 'automatic_fulfillment_digital_products', 'default_digital_max_downloads', 'default_digital_url_valid_days', 'default_mail_sender_name', 'default_mail_sender_address', 'fulfillment_auto_approve', 'fulfillment_allow_unpaid', 'reserve_stock_duration_anonymous_user', 'reserve_stock_duration_authenticated_user', 'limit_quantity_per_checkout', 'gift_card_expiry_type', 'gift_card_expiry_period_type', 'gift_card_expiry_period', 'charge_taxes_on_shipping', 'include_taxes_in_prices', 'display_gross_prices', 'language']
#
#    search_columns = ['id', 'portal_url', 'is_primary', 'portal_state', 'individual', 'has_custom_domain', 'domain', 'header_text', 'slug', 'automatic_fulfillment_digital_products', 'default_digital_max_downloads', 'default_digital_url_valid_days', 'default_mail_sender_name', 'default_mail_sender_address', 'fulfillment_auto_approve', 'fulfillment_allow_unpaid', 'reserve_stock_duration_anonymous_user', 'reserve_stock_duration_authenticated_user', 'limit_quantity_per_checkout', 'gift_card_expiry_type', 'gift_card_expiry_period_type', 'gift_card_expiry_period', 'charge_taxes_on_shipping', 'include_taxes_in_prices', 'display_gross_prices', 'language']
#    search_exclude_columns= [] # ['id', 'portal_url', 'is_primary', 'portal_state', 'individual', 'has_custom_domain', 'domain', 'header_text', 'slug', 'automatic_fulfillment_digital_products', 'default_digital_max_downloads', 'default_digital_url_valid_days', 'default_mail_sender_name', 'default_mail_sender_address', 'fulfillment_auto_approve', 'fulfillment_allow_unpaid', 'reserve_stock_duration_anonymous_user', 'reserve_stock_duration_authenticated_user', 'limit_quantity_per_checkout', 'gift_card_expiry_type', 'gift_card_expiry_period_type', 'gift_card_expiry_period', 'charge_taxes_on_shipping', 'include_taxes_in_prices', 'display_gross_prices', 'language']
#
#    default_sort = [('id', True)]
#    base_permissions = ['can_list', 'can_show', 'can_edit', 'can_delete', 'can_add']
#    label_columns=   [{column.name: column.name for column in table.columns} ]
#    show_template =  'appbuilder/general/model/show_cascade.html'
#    list_template = 'appbuilder/general/model/list.html'
#    add_template = 'appbuilder/general/model/add.html'
#    edit_template = 'appbuilder/general/model/edit.html'
#    add_widget = (FormVerticalWidget|FormInlineWidget)
#    show_widget = ShowBlockWidget
#    list_widget = (ListThumbnail|ListWidget)
#    base_order = ('name', 'asc')
#    list_widget= 'list_widget'


class PageMasterView(MasterDetailView):
    datamodel=SQLAInterface(Page, db.session)
    related_views = [PortalDetailView]
    show_title='Page Detail'
    add_title ='Add Page'
    list_title= 'Page List'
    edit_title = 'Edit Page'
    show_columns = ['id', 'portal', 'header', 'slug', 'page_type']
#    show_exclude_columns = [] #= ['id', 'portal', 'header', 'slug', 'page_type']
#
#    add_columns = ['id', 'portal', 'header', 'slug', 'page_type']
#    add_exclude_columns = [hide_list] #['id', 'portal', 'header', 'slug', 'page_type']
#
#    edit_columns = ['id', 'portal', 'header', 'slug', 'page_type']
#    edit_exclude_columns =[hide_list] # ['id', 'portal', 'header', 'slug', 'page_type']
#
#    list_columns = ['id', 'portal', 'header', 'slug', 'page_type']
#    list_exclude_columns = [] # ['id', 'portal', 'header', 'slug', 'page_type']
#
#    search_columns = ['id', 'portal', 'header', 'slug', 'page_type']
#    search_exclude_columns= [] # ['id', 'portal', 'header', 'slug', 'page_type']
#
#    default_sort = [('id', True)]
#    base_permissions = ['can_list', 'can_show', 'can_edit', 'can_delete', 'can_add']
#    label_columns=   [{column.name: column.name for column in table.columns} ]
#    show_template =  'appbuilder/general/model/show_cascade.html'
#    list_template = 'appbuilder/general/model/list.html'
#    add_template = 'appbuilder/general/model/add.html'
#    edit_template = 'appbuilder/general/model/edit.html'
#    add_widget = (FormVerticalWidget|FormInlineWidget)
#    show_widget = ShowBlockWidget
#    list_widget = (ListThumbnail|ListWidget)
#    base_order = ('name', 'asc')
#    list_widget= 'list_widget'


class ProfileMasterView(MasterDetailView):
    datamodel=SQLAInterface(Profile, db.session)
    related_views = [IndividualDetailView]
    show_title='Profile Detail'
    add_title ='Add Profile'
    list_title= 'Profile List'
    edit_title = 'Edit Profile'
    show_columns = ['id', 'individual', 'import_address', 'profile_username', 'profile_password', 'has_been_imported', 'import_data', 'import_date', 'profilesource']
#    show_exclude_columns = [] #= ['id', 'individual', 'import_address', 'profile_username', 'profile_password', 'has_been_imported', 'import_data', 'import_date', 'profilesource']
#
#    add_columns = ['id', 'individual', 'import_address', 'profile_username', 'profile_password', 'has_been_imported', 'import_data', 'import_date', 'profilesource']
#    add_exclude_columns = [hide_list] #['id', 'individual', 'import_address', 'profile_username', 'profile_password', 'has_been_imported', 'import_data', 'import_date', 'profilesource']
#
#    edit_columns = ['id', 'individual', 'import_address', 'profile_username', 'profile_password', 'has_been_imported', 'import_data', 'import_date', 'profilesource']
#    edit_exclude_columns =[hide_list] # ['id', 'individual', 'import_address', 'profile_username', 'profile_password', 'has_been_imported', 'import_data', 'import_date', 'profilesource']
#
#    list_columns = ['id', 'individual', 'import_address', 'profile_username', 'profile_password', 'has_been_imported', 'import_data', 'import_date', 'profilesource']
#    list_exclude_columns = [] # ['id', 'individual', 'import_address', 'profile_username', 'profile_password', 'has_been_imported', 'import_data', 'import_date', 'profilesource']
#
#    search_columns = ['id', 'individual', 'import_address', 'profile_username', 'profile_password', 'has_been_imported', 'import_data', 'import_date', 'profilesource']
#    search_exclude_columns= [] # ['id', 'individual', 'import_address', 'profile_username', 'profile_password', 'has_been_imported', 'import_data', 'import_date', 'profilesource']
#
#    default_sort = [('id', True)]
#    base_permissions = ['can_list', 'can_show', 'can_edit', 'can_delete', 'can_add']
#    label_columns=   [{column.name: column.name for column in table.columns} ]
#    show_template =  'appbuilder/general/model/show_cascade.html'
#    list_template = 'appbuilder/general/model/list.html'
#    add_template = 'appbuilder/general/model/add.html'
#    edit_template = 'appbuilder/general/model/edit.html'
#    add_widget = (FormVerticalWidget|FormInlineWidget)
#    show_widget = ShowBlockWidget
#    list_widget = (ListThumbnail|ListWidget)
#    base_order = ('name', 'asc')
#    list_widget= 'list_widget'


class ProfileMultiView(MultipleView):
    datamodel=SQLAInterface(Profile, db.session)
    views = [ProfilesourceDetailView]
    show_title='Profile Detail'
    add_title ='Add Profile'
    list_title= 'Profile List'
    edit_title = 'Edit Profile'
    show_columns = ['id', 'individual', 'import_address', 'profile_username', 'profile_password', 'has_been_imported', 'import_data', 'import_date', 'profilesource']
#    show_exclude_columns = [] #= ['id', 'individual', 'import_address', 'profile_username', 'profile_password', 'has_been_imported', 'import_data', 'import_date', 'profilesource']
#
#    add_columns = ['id', 'individual', 'import_address', 'profile_username', 'profile_password', 'has_been_imported', 'import_data', 'import_date', 'profilesource']
#    add_exclude_columns = [hide_list] #['id', 'individual', 'import_address', 'profile_username', 'profile_password', 'has_been_imported', 'import_data', 'import_date', 'profilesource']
#
#    edit_columns = ['id', 'individual', 'import_address', 'profile_username', 'profile_password', 'has_been_imported', 'import_data', 'import_date', 'profilesource']
#    edit_exclude_columns =[hide_list] # ['id', 'individual', 'import_address', 'profile_username', 'profile_password', 'has_been_imported', 'import_data', 'import_date', 'profilesource']
#
#    list_columns = ['id', 'individual', 'import_address', 'profile_username', 'profile_password', 'has_been_imported', 'import_data', 'import_date', 'profilesource']
#    list_exclude_columns = [] # ['id', 'individual', 'import_address', 'profile_username', 'profile_password', 'has_been_imported', 'import_data', 'import_date', 'profilesource']
#
#    search_columns = ['id', 'individual', 'import_address', 'profile_username', 'profile_password', 'has_been_imported', 'import_data', 'import_date', 'profilesource']
#    search_exclude_columns= [] # ['id', 'individual', 'import_address', 'profile_username', 'profile_password', 'has_been_imported', 'import_data', 'import_date', 'profilesource']
#
#    default_sort = [('id', True)]
#    base_permissions = ['can_list', 'can_show', 'can_edit', 'can_delete', 'can_add']
#    label_columns=   [{column.name: column.name for column in table.columns} ]
#    show_template =  'appbuilder/general/model/show_cascade.html'
#    list_template = 'appbuilder/general/model/list.html'
#    add_template = 'appbuilder/general/model/add.html'
#    edit_template = 'appbuilder/general/model/edit.html'
#    add_widget = (FormVerticalWidget|FormInlineWidget)
#    show_widget = ShowBlockWidget
#    list_widget = (ListThumbnail|ListWidget)
#    base_order = ('name', 'asc')
#    list_widget= 'list_widget'


class ResumeMasterView(MasterDetailView):
    datamodel=SQLAInterface(Resume, db.session)
    related_views = [IndividualDetailView]
    show_title='Resume Detail'
    add_title ='Add Resume'
    list_title= 'Resume List'
    edit_title = 'Edit Resume'
    show_columns = ['id', 'individual', 'template', 'header', 'color', 'location', 'summary_text', 'has_been_generated', 'preferred']
#    show_exclude_columns = [] #= ['id', 'individual', 'template', 'header', 'color', 'location', 'summary_text', 'has_been_generated', 'preferred']
#
#    add_columns = ['id', 'individual', 'template', 'header', 'color', 'location', 'summary_text', 'has_been_generated', 'preferred']
#    add_exclude_columns = [hide_list] #['id', 'individual', 'template', 'header', 'color', 'location', 'summary_text', 'has_been_generated', 'preferred']
#
#    edit_columns = ['id', 'individual', 'template', 'header', 'color', 'location', 'summary_text', 'has_been_generated', 'preferred']
#    edit_exclude_columns =[hide_list] # ['id', 'individual', 'template', 'header', 'color', 'location', 'summary_text', 'has_been_generated', 'preferred']
#
#    list_columns = ['id', 'individual', 'template', 'header', 'color', 'location', 'summary_text', 'has_been_generated', 'preferred']
#    list_exclude_columns = [] # ['id', 'individual', 'template', 'header', 'color', 'location', 'summary_text', 'has_been_generated', 'preferred']
#
#    search_columns = ['id', 'individual', 'template', 'header', 'color', 'location', 'summary_text', 'has_been_generated', 'preferred']
#    search_exclude_columns= [] # ['id', 'individual', 'template', 'header', 'color', 'location', 'summary_text', 'has_been_generated', 'preferred']
#
#    default_sort = [('id', True)]
#    base_permissions = ['can_list', 'can_show', 'can_edit', 'can_delete', 'can_add']
#    label_columns=   [{column.name: column.name for column in table.columns} ]
#    show_template =  'appbuilder/general/model/show_cascade.html'
#    list_template = 'appbuilder/general/model/list.html'
#    add_template = 'appbuilder/general/model/add.html'
#    edit_template = 'appbuilder/general/model/edit.html'
#    add_widget = (FormVerticalWidget|FormInlineWidget)
#    show_widget = ShowBlockWidget
#    list_widget = (ListThumbnail|ListWidget)
#    base_order = ('name', 'asc')
#    list_widget= 'list_widget'


class ResumeMultiView(MultipleView):
    datamodel=SQLAInterface(Resume, db.session)
    views = [LocationDetailView]
    show_title='Resume Detail'
    add_title ='Add Resume'
    list_title= 'Resume List'
    edit_title = 'Edit Resume'
    show_columns = ['id', 'individual', 'template', 'header', 'color', 'location', 'summary_text', 'has_been_generated', 'preferred']
#    show_exclude_columns = [] #= ['id', 'individual', 'template', 'header', 'color', 'location', 'summary_text', 'has_been_generated', 'preferred']
#
#    add_columns = ['id', 'individual', 'template', 'header', 'color', 'location', 'summary_text', 'has_been_generated', 'preferred']
#    add_exclude_columns = [hide_list] #['id', 'individual', 'template', 'header', 'color', 'location', 'summary_text', 'has_been_generated', 'preferred']
#
#    edit_columns = ['id', 'individual', 'template', 'header', 'color', 'location', 'summary_text', 'has_been_generated', 'preferred']
#    edit_exclude_columns =[hide_list] # ['id', 'individual', 'template', 'header', 'color', 'location', 'summary_text', 'has_been_generated', 'preferred']
#
#    list_columns = ['id', 'individual', 'template', 'header', 'color', 'location', 'summary_text', 'has_been_generated', 'preferred']
#    list_exclude_columns = [] # ['id', 'individual', 'template', 'header', 'color', 'location', 'summary_text', 'has_been_generated', 'preferred']
#
#    search_columns = ['id', 'individual', 'template', 'header', 'color', 'location', 'summary_text', 'has_been_generated', 'preferred']
#    search_exclude_columns= [] # ['id', 'individual', 'template', 'header', 'color', 'location', 'summary_text', 'has_been_generated', 'preferred']
#
#    default_sort = [('id', True)]
#    base_permissions = ['can_list', 'can_show', 'can_edit', 'can_delete', 'can_add']
#    label_columns=   [{column.name: column.name for column in table.columns} ]
#    show_template =  'appbuilder/general/model/show_cascade.html'
#    list_template = 'appbuilder/general/model/list.html'
#    add_template = 'appbuilder/general/model/add.html'
#    edit_template = 'appbuilder/general/model/edit.html'
#    add_widget = (FormVerticalWidget|FormInlineWidget)
#    show_widget = ShowBlockWidget
#    list_widget = (ListThumbnail|ListWidget)
#    base_order = ('name', 'asc')
#    list_widget= 'list_widget'


class SwarmMasterView(MasterDetailView):
    datamodel=SQLAInterface(Swarm, db.session)
    related_views = [PortalDetailView]
    show_title='Swarm Detail'
    add_title ='Add Swarm'
    list_title= 'Swarm List'
    edit_title = 'Edit Swarm'
    show_columns = ['id', 'portal']
#    show_exclude_columns = [] #= ['id', 'portal']
#
#    add_columns = ['id', 'portal']
#    add_exclude_columns = [hide_list] #['id', 'portal']
#
#    edit_columns = ['id', 'portal']
#    edit_exclude_columns =[hide_list] # ['id', 'portal']
#
#    list_columns = ['id', 'portal']
#    list_exclude_columns = [] # ['id', 'portal']
#
#    search_columns = ['id', 'portal']
#    search_exclude_columns= [] # ['id', 'portal']
#
#    default_sort = [('id', True)]
#    base_permissions = ['can_list', 'can_show', 'can_edit', 'can_delete', 'can_add']
#    label_columns=   [{column.name: column.name for column in table.columns} ]
#    show_template =  'appbuilder/general/model/show_cascade.html'
#    list_template = 'appbuilder/general/model/list.html'
#    add_template = 'appbuilder/general/model/add.html'
#    edit_template = 'appbuilder/general/model/edit.html'
#    add_widget = (FormVerticalWidget|FormInlineWidget)
#    show_widget = ShowBlockWidget
#    list_widget = (ListThumbnail|ListWidget)
#    base_order = ('name', 'asc')
#    list_widget= 'list_widget'


class IndividualSwarmMasterView(MasterDetailView):
    datamodel=SQLAInterface(IndividualSwarm, db.session)
    related_views = [IndividualDetailView]
    show_title='IndividualSwarm Detail'
    add_title ='Add IndividualSwarm'
    list_title= 'IndividualSwarm List'
    edit_title = 'Edit IndividualSwarm'
    show_columns = ['individual', 'swarm']
#    show_exclude_columns = [] #= ['individual', 'swarm']
#
#    add_columns = ['individual', 'swarm']
#    add_exclude_columns = [hide_list] #['individual', 'swarm']
#
#    edit_columns = ['individual', 'swarm']
#    edit_exclude_columns =[hide_list] # ['individual', 'swarm']
#
#    list_columns = ['individual', 'swarm']
#    list_exclude_columns = [] # ['individual', 'swarm']
#
#    search_columns = ['individual', 'swarm']
#    search_exclude_columns= [] # ['individual', 'swarm']
#
#    default_sort = [('id', True)]
#    base_permissions = ['can_list', 'can_show', 'can_edit', 'can_delete', 'can_add']
#    label_columns=   [{column.name: column.name for column in table.columns} ]
#    show_template =  'appbuilder/general/model/show_cascade.html'
#    list_template = 'appbuilder/general/model/list.html'
#    add_template = 'appbuilder/general/model/add.html'
#    edit_template = 'appbuilder/general/model/edit.html'
#    add_widget = (FormVerticalWidget|FormInlineWidget)
#    show_widget = ShowBlockWidget
#    list_widget = (ListThumbnail|ListWidget)
#    base_order = ('name', 'asc')
#    list_widget= 'list_widget'


class IndividualSwarmMultiView(MultipleView):
    datamodel=SQLAInterface(IndividualSwarm, db.session)
    views = [SwarmDetailView]
    show_title='IndividualSwarm Detail'
    add_title ='Add IndividualSwarm'
    list_title= 'IndividualSwarm List'
    edit_title = 'Edit IndividualSwarm'
    show_columns = ['individual', 'swarm']
#    show_exclude_columns = [] #= ['individual', 'swarm']
#
#    add_columns = ['individual', 'swarm']
#    add_exclude_columns = [hide_list] #['individual', 'swarm']
#
#    edit_columns = ['individual', 'swarm']
#    edit_exclude_columns =[hide_list] # ['individual', 'swarm']
#
#    list_columns = ['individual', 'swarm']
#    list_exclude_columns = [] # ['individual', 'swarm']
#
#    search_columns = ['individual', 'swarm']
#    search_exclude_columns= [] # ['individual', 'swarm']
#
#    default_sort = [('id', True)]
#    base_permissions = ['can_list', 'can_show', 'can_edit', 'can_delete', 'can_add']
#    label_columns=   [{column.name: column.name for column in table.columns} ]
#    show_template =  'appbuilder/general/model/show_cascade.html'
#    list_template = 'appbuilder/general/model/list.html'
#    add_template = 'appbuilder/general/model/add.html'
#    edit_template = 'appbuilder/general/model/edit.html'
#    add_widget = (FormVerticalWidget|FormInlineWidget)
#    show_widget = ShowBlockWidget
#    list_widget = (ListThumbnail|ListWidget)
#    base_order = ('name', 'asc')
#    list_widget= 'list_widget'


class UserSkillMasterView(MasterDetailView):
    datamodel=SQLAInterface(UserSkill, db.session)
    related_views = [IndividualDetailView]
    show_title='UserSkill Detail'
    add_title ='Add UserSkill'
    list_title= 'UserSkill List'
    edit_title = 'Edit UserSkill'
    show_columns = ['skills', 'user_details']
#    show_exclude_columns = [] #= ['skills', 'user_details']
#
#    add_columns = ['skills', 'user_details']
#    add_exclude_columns = [hide_list] #['skills', 'user_details']
#
#    edit_columns = ['skills', 'user_details']
#    edit_exclude_columns =[hide_list] # ['skills', 'user_details']
#
#    list_columns = ['skills', 'user_details']
#    list_exclude_columns = [] # ['skills', 'user_details']
#
#    search_columns = ['skills', 'user_details']
#    search_exclude_columns= [] # ['skills', 'user_details']
#
#    default_sort = [('id', True)]
#    base_permissions = ['can_list', 'can_show', 'can_edit', 'can_delete', 'can_add']
#    label_columns=   [{column.name: column.name for column in table.columns} ]
#    show_template =  'appbuilder/general/model/show_cascade.html'
#    list_template = 'appbuilder/general/model/list.html'
#    add_template = 'appbuilder/general/model/add.html'
#    edit_template = 'appbuilder/general/model/edit.html'
#    add_widget = (FormVerticalWidget|FormInlineWidget)
#    show_widget = ShowBlockWidget
#    list_widget = (ListThumbnail|ListWidget)
#    base_order = ('name', 'asc')
#    list_widget= 'list_widget'


class UserSkillMultiView(MultipleView):
    datamodel=SQLAInterface(UserSkill, db.session)
    views = []
    show_title='UserSkill Detail'
    add_title ='Add UserSkill'
    list_title= 'UserSkill List'
    edit_title = 'Edit UserSkill'
    show_columns = ['skills', 'user_details']
#    show_exclude_columns = [] #= ['skills', 'user_details']
#
#    add_columns = ['skills', 'user_details']
#    add_exclude_columns = [hide_list] #['skills', 'user_details']
#
#    edit_columns = ['skills', 'user_details']
#    edit_exclude_columns =[hide_list] # ['skills', 'user_details']
#
#    list_columns = ['skills', 'user_details']
#    list_exclude_columns = [] # ['skills', 'user_details']
#
#    search_columns = ['skills', 'user_details']
#    search_exclude_columns= [] # ['skills', 'user_details']
#
#    default_sort = [('id', True)]
#    base_permissions = ['can_list', 'can_show', 'can_edit', 'can_delete', 'can_add']
#    label_columns=   [{column.name: column.name for column in table.columns} ]
#    show_template =  'appbuilder/general/model/show_cascade.html'
#    list_template = 'appbuilder/general/model/list.html'
#    add_template = 'appbuilder/general/model/add.html'
#    edit_template = 'appbuilder/general/model/edit.html'
#    add_widget = (FormVerticalWidget|FormInlineWidget)
#    show_widget = ShowBlockWidget
#    list_widget = (ListThumbnail|ListWidget)
#    base_order = ('name', 'asc')
#    list_widget= 'list_widget'


class WorkHistoryView(ModelView):
    datamodel=SQLAInterface(WorkHistory, db.session)
    related_views = []
    show_title='WorkHistory Detail'
    add_title ='Add WorkHistory'
    list_title= 'WorkHistory List'
    edit_title = 'Edit WorkHistory'
    show_columns = ['id', 'individual', 'resume']
#    show_exclude_columns = [] #= ['id', 'individual', 'resume']
#
#    add_columns = ['id', 'individual', 'resume']
#    add_exclude_columns = [hide_list] #['id', 'individual', 'resume']
#
#    edit_columns = ['id', 'individual', 'resume']
#    edit_exclude_columns =[hide_list] # ['id', 'individual', 'resume']
#
#    list_columns = ['id', 'individual', 'resume']
#    list_exclude_columns = [] # ['id', 'individual', 'resume']
#
#    search_columns = ['id', 'individual', 'resume']
#    search_exclude_columns= [] # ['id', 'individual', 'resume']
#
#    default_sort = [('id', True)]
#    base_permissions = ['can_list', 'can_show', 'can_edit', 'can_delete', 'can_add']
#    label_columns=   [{column.name: column.name for column in table.columns} ]
#    show_template =  'appbuilder/general/model/show_cascade.html'
#    list_template = 'appbuilder/general/model/list.html'
#    add_template = 'appbuilder/general/model/add.html'
#    edit_template = 'appbuilder/general/model/edit.html'
#    add_widget = (FormVerticalWidget|FormInlineWidget)
#    show_widget = ShowBlockWidget
#    list_widget = (ListThumbnail|ListWidget)
#    base_order = ('name', 'asc')
#    list_widget= 'list_widget'


class UserxDetailView(ModelView):
    datamodel=SQLAInterface(Userx, db.session)
    related_views = []
    show_title='Userx Detail'
    add_title ='Add Userx'
    list_title= 'Userx List'
    edit_title = 'Edit Userx'
    show_columns = ['id', 'userx', 'is_individual', 'is_institution', 'is_company', 'is_government', 'is_online']
#    show_exclude_columns = [] #= ['id', 'userx', 'is_individual', 'is_institution', 'is_company', 'is_government', 'is_online']
#
#    add_columns = ['id', 'userx', 'is_individual', 'is_institution', 'is_company', 'is_government', 'is_online']
#    add_exclude_columns = [hide_list] #['id', 'userx', 'is_individual', 'is_institution', 'is_company', 'is_government', 'is_online']
#
#    edit_columns = ['id', 'userx', 'is_individual', 'is_institution', 'is_company', 'is_government', 'is_online']
#    edit_exclude_columns =[hide_list] # ['id', 'userx', 'is_individual', 'is_institution', 'is_company', 'is_government', 'is_online']
#
#    list_columns = ['id', 'userx', 'is_individual', 'is_institution', 'is_company', 'is_government', 'is_online']
#    list_exclude_columns = [] # ['id', 'userx', 'is_individual', 'is_institution', 'is_company', 'is_government', 'is_online']
#
#    search_columns = ['id', 'userx', 'is_individual', 'is_institution', 'is_company', 'is_government', 'is_online']
#    search_exclude_columns= [] # ['id', 'userx', 'is_individual', 'is_institution', 'is_company', 'is_government', 'is_online']
#
#    default_sort = [('id', True)]
#    base_permissions = ['can_list', 'can_show', 'can_edit', 'can_delete', 'can_add']
#    label_columns=   [{column.name: column.name for column in table.columns} ]
#    show_template =  'appbuilder/general/model/show_cascade.html'
#    list_template = 'appbuilder/general/model/list.html'
#    add_template = 'appbuilder/general/model/add.html'
#    edit_template = 'appbuilder/general/model/edit.html'
#    add_widget = (FormVerticalWidget|FormInlineWidget)
#    show_widget = ShowBlockWidget
#    list_widget = (ListThumbnail|ListWidget)
#    base_order = ('name', 'asc')
#    list_widget= 'list_widget'


class IndividualDetailView(ModelView):
    datamodel=SQLAInterface(Individual, db.session)
    related_views = []
    show_title='Individual Detail'
    add_title ='Add Individual'
    list_title= 'Individual List'
    edit_title = 'Edit Individual'
    show_columns = ['id', 'userx', 'is_individual', 'is_institution', 'is_company', 'is_government', 'is_online']
#    show_exclude_columns = [] #= ['id', 'userx', 'is_individual', 'is_institution', 'is_company', 'is_government', 'is_online']
#
#    add_columns = ['id', 'userx', 'is_individual', 'is_institution', 'is_company', 'is_government', 'is_online']
#    add_exclude_columns = [hide_list] #['id', 'userx', 'is_individual', 'is_institution', 'is_company', 'is_government', 'is_online']
#
#    edit_columns = ['id', 'userx', 'is_individual', 'is_institution', 'is_company', 'is_government', 'is_online']
#    edit_exclude_columns =[hide_list] # ['id', 'userx', 'is_individual', 'is_institution', 'is_company', 'is_government', 'is_online']
#
#    list_columns = ['id', 'userx', 'is_individual', 'is_institution', 'is_company', 'is_government', 'is_online']
#    list_exclude_columns = [] # ['id', 'userx', 'is_individual', 'is_institution', 'is_company', 'is_government', 'is_online']
#
#    search_columns = ['id', 'userx', 'is_individual', 'is_institution', 'is_company', 'is_government', 'is_online']
#    search_exclude_columns= [] # ['id', 'userx', 'is_individual', 'is_institution', 'is_company', 'is_government', 'is_online']
#
#    default_sort = [('id', True)]
#    base_permissions = ['can_list', 'can_show', 'can_edit', 'can_delete', 'can_add']
#    label_columns=   [{column.name: column.name for column in table.columns} ]
#    show_template =  'appbuilder/general/model/show_cascade.html'
#    list_template = 'appbuilder/general/model/list.html'
#    add_template = 'appbuilder/general/model/add.html'
#    edit_template = 'appbuilder/general/model/edit.html'
#    add_widget = (FormVerticalWidget|FormInlineWidget)
#    show_widget = ShowBlockWidget
#    list_widget = (ListThumbnail|ListWidget)
#    base_order = ('name', 'asc')
#    list_widget= 'list_widget'


class IndustryDetailView(ModelView):
    datamodel=SQLAInterface(Industry, db.session)
    related_views = []
    show_title='Industry Detail'
    add_title ='Add Industry'
    list_title= 'Industry List'
    edit_title = 'Edit Industry'
    show_columns = ['industry', 'job']
#    show_exclude_columns = [] #= ['industry', 'job']
#
#    add_columns = ['industry', 'job']
#    add_exclude_columns = [hide_list] #['industry', 'job']
#
#    edit_columns = ['industry', 'job']
#    edit_exclude_columns =[hide_list] # ['industry', 'job']
#
#    list_columns = ['industry', 'job']
#    list_exclude_columns = [] # ['industry', 'job']
#
#    search_columns = ['industry', 'job']
#    search_exclude_columns= [] # ['industry', 'job']
#
#    default_sort = [('id', True)]
#    base_permissions = ['can_list', 'can_show', 'can_edit', 'can_delete', 'can_add']
#    label_columns=   [{column.name: column.name for column in table.columns} ]
#    show_template =  'appbuilder/general/model/show_cascade.html'
#    list_template = 'appbuilder/general/model/list.html'
#    add_template = 'appbuilder/general/model/add.html'
#    edit_template = 'appbuilder/general/model/edit.html'
#    add_widget = (FormVerticalWidget|FormInlineWidget)
#    show_widget = ShowBlockWidget
#    list_widget = (ListThumbnail|ListWidget)
#    base_order = ('name', 'asc')
#    list_widget= 'list_widget'


class IndustryJobDetailView(ModelView):
    datamodel=SQLAInterface(IndustryJob, db.session)
    related_views = []
    show_title='IndustryJob Detail'
    add_title ='Add IndustryJob'
    list_title= 'IndustryJob List'
    edit_title = 'Edit IndustryJob'
    show_columns = ['industry', 'job']
#    show_exclude_columns = [] #= ['industry', 'job']
#
#    add_columns = ['industry', 'job']
#    add_exclude_columns = [hide_list] #['industry', 'job']
#
#    edit_columns = ['industry', 'job']
#    edit_exclude_columns =[hide_list] # ['industry', 'job']
#
#    list_columns = ['industry', 'job']
#    list_exclude_columns = [] # ['industry', 'job']
#
#    search_columns = ['industry', 'job']
#    search_exclude_columns= [] # ['industry', 'job']
#
#    default_sort = [('id', True)]
#    base_permissions = ['can_list', 'can_show', 'can_edit', 'can_delete', 'can_add']
#    label_columns=   [{column.name: column.name for column in table.columns} ]
#    show_template =  'appbuilder/general/model/show_cascade.html'
#    list_template = 'appbuilder/general/model/list.html'
#    add_template = 'appbuilder/general/model/add.html'
#    edit_template = 'appbuilder/general/model/edit.html'
#    add_widget = (FormVerticalWidget|FormInlineWidget)
#    show_widget = ShowBlockWidget
#    list_widget = (ListThumbnail|ListWidget)
#    base_order = ('name', 'asc')
#    list_widget= 'list_widget'


class JobDetailView(ModelView):
    datamodel=SQLAInterface(Job, db.session)
    related_views = []
    show_title='Job Detail'
    add_title ='Add Job'
    list_title= 'Job List'
    edit_title = 'Edit Job'
    show_columns = ['industry', 'job']
#    show_exclude_columns = [] #= ['industry', 'job']
#
#    add_columns = ['industry', 'job']
#    add_exclude_columns = [hide_list] #['industry', 'job']
#
#    edit_columns = ['industry', 'job']
#    edit_exclude_columns =[hide_list] # ['industry', 'job']
#
#    list_columns = ['industry', 'job']
#    list_exclude_columns = [] # ['industry', 'job']
#
#    search_columns = ['industry', 'job']
#    search_exclude_columns= [] # ['industry', 'job']
#
#    default_sort = [('id', True)]
#    base_permissions = ['can_list', 'can_show', 'can_edit', 'can_delete', 'can_add']
#    label_columns=   [{column.name: column.name for column in table.columns} ]
#    show_template =  'appbuilder/general/model/show_cascade.html'
#    list_template = 'appbuilder/general/model/list.html'
#    add_template = 'appbuilder/general/model/add.html'
#    edit_template = 'appbuilder/general/model/edit.html'
#    add_widget = (FormVerticalWidget|FormInlineWidget)
#    show_widget = ShowBlockWidget
#    list_widget = (ListThumbnail|ListWidget)
#    base_order = ('name', 'asc')
#    list_widget= 'list_widget'




class SkillDetailView(ModelView):
    datamodel=SQLAInterface(Skill, db.session)
    related_views = []
    show_title='Skill Detail'
    add_title ='Add Skill'
    list_title= 'Skill List'
    edit_title = 'Edit Skill'
    show_columns = ['skills', 'jobs']
#    show_exclude_columns = [] #= ['skills', 'jobs']
#
#    add_columns = ['skills', 'jobs']
#    add_exclude_columns = [hide_list] #['skills', 'jobs']
#
#    edit_columns = ['skills', 'jobs']
#    edit_exclude_columns =[hide_list] # ['skills', 'jobs']
#
#    list_columns = ['skills', 'jobs']
#    list_exclude_columns = [] # ['skills', 'jobs']
#
#    search_columns = ['skills', 'jobs']
#    search_exclude_columns= [] # ['skills', 'jobs']
#
#    default_sort = [('id', True)]
#    base_permissions = ['can_list', 'can_show', 'can_edit', 'can_delete', 'can_add']
#    label_columns=   [{column.name: column.name for column in table.columns} ]
#    show_template =  'appbuilder/general/model/show_cascade.html'
#    list_template = 'appbuilder/general/model/list.html'
#    add_template = 'appbuilder/general/model/add.html'
#    edit_template = 'appbuilder/general/model/edit.html'
#    add_widget = (FormVerticalWidget|FormInlineWidget)
#    show_widget = ShowBlockWidget
#    list_widget = (ListThumbnail|ListWidget)
#    base_order = ('name', 'asc')
#    list_widget= 'list_widget'


class JobSkillDetailView(ModelView):
    datamodel=SQLAInterface(JobSkill, db.session)
    related_views = []
    show_title='JobSkill Detail'
    add_title ='Add JobSkill'
    list_title= 'JobSkill List'
    edit_title = 'Edit JobSkill'
    show_columns = ['skills', 'jobs']
#    show_exclude_columns = [] #= ['skills', 'jobs']
#
#    add_columns = ['skills', 'jobs']
#    add_exclude_columns = [hide_list] #['skills', 'jobs']
#
#    edit_columns = ['skills', 'jobs']
#    edit_exclude_columns =[hide_list] # ['skills', 'jobs']
#
#    list_columns = ['skills', 'jobs']
#    list_exclude_columns = [] # ['skills', 'jobs']
#
#    search_columns = ['skills', 'jobs']
#    search_exclude_columns= [] # ['skills', 'jobs']
#
#    default_sort = [('id', True)]
#    base_permissions = ['can_list', 'can_show', 'can_edit', 'can_delete', 'can_add']
#    label_columns=   [{column.name: column.name for column in table.columns} ]
#    show_template =  'appbuilder/general/model/show_cascade.html'
#    list_template = 'appbuilder/general/model/list.html'
#    add_template = 'appbuilder/general/model/add.html'
#    edit_template = 'appbuilder/general/model/edit.html'
#    add_widget = (FormVerticalWidget|FormInlineWidget)
#    show_widget = ShowBlockWidget
#    list_widget = (ListThumbnail|ListWidget)
#    base_order = ('name', 'asc')
#    list_widget= 'list_widget'


class PortalDetailView(ModelView):
    datamodel=SQLAInterface(Portal, db.session)
    related_views = []
    show_title='Portal Detail'
    add_title ='Add Portal'
    list_title= 'Portal List'
    edit_title = 'Edit Portal'
    show_columns = ['id', 'portal', 'header', 'slug', 'page_type']
#    show_exclude_columns = [] #= ['id', 'portal', 'header', 'slug', 'page_type']
#
#    add_columns = ['id', 'portal', 'header', 'slug', 'page_type']
#    add_exclude_columns = [hide_list] #['id', 'portal', 'header', 'slug', 'page_type']
#
#    edit_columns = ['id', 'portal', 'header', 'slug', 'page_type']
#    edit_exclude_columns =[hide_list] # ['id', 'portal', 'header', 'slug', 'page_type']
#
#    list_columns = ['id', 'portal', 'header', 'slug', 'page_type']
#    list_exclude_columns = [] # ['id', 'portal', 'header', 'slug', 'page_type']
#
#    search_columns = ['id', 'portal', 'header', 'slug', 'page_type']
#    search_exclude_columns= [] # ['id', 'portal', 'header', 'slug', 'page_type']
#
#    default_sort = [('id', True)]
#    base_permissions = ['can_list', 'can_show', 'can_edit', 'can_delete', 'can_add']
#    label_columns=   [{column.name: column.name for column in table.columns} ]
#    show_template =  'appbuilder/general/model/show_cascade.html'
#    list_template = 'appbuilder/general/model/list.html'
#    add_template = 'appbuilder/general/model/add.html'
#    edit_template = 'appbuilder/general/model/edit.html'
#    add_widget = (FormVerticalWidget|FormInlineWidget)
#    show_widget = ShowBlockWidget
#    list_widget = (ListThumbnail|ListWidget)
#    base_order = ('name', 'asc')
#    list_widget= 'list_widget'


class PageDetailView(ModelView):
    datamodel=SQLAInterface(Page, db.session)
    related_views = []
    show_title='Page Detail'
    add_title ='Add Page'
    list_title= 'Page List'
    edit_title = 'Edit Page'
    show_columns = ['id', 'portal', 'header', 'slug', 'page_type']
#    show_exclude_columns = [] #= ['id', 'portal', 'header', 'slug', 'page_type']
#
#    add_columns = ['id', 'portal', 'header', 'slug', 'page_type']
#    add_exclude_columns = [hide_list] #['id', 'portal', 'header', 'slug', 'page_type']
#
#    edit_columns = ['id', 'portal', 'header', 'slug', 'page_type']
#    edit_exclude_columns =[hide_list] # ['id', 'portal', 'header', 'slug', 'page_type']
#
#    list_columns = ['id', 'portal', 'header', 'slug', 'page_type']
#    list_exclude_columns = [] # ['id', 'portal', 'header', 'slug', 'page_type']
#
#    search_columns = ['id', 'portal', 'header', 'slug', 'page_type']
#    search_exclude_columns= [] # ['id', 'portal', 'header', 'slug', 'page_type']
#
#    default_sort = [('id', True)]
#    base_permissions = ['can_list', 'can_show', 'can_edit', 'can_delete', 'can_add']
#    label_columns=   [{column.name: column.name for column in table.columns} ]
#    show_template =  'appbuilder/general/model/show_cascade.html'
#    list_template = 'appbuilder/general/model/list.html'
#    add_template = 'appbuilder/general/model/add.html'
#    edit_template = 'appbuilder/general/model/edit.html'
#    add_widget = (FormVerticalWidget|FormInlineWidget)
#    show_widget = ShowBlockWidget
#    list_widget = (ListThumbnail|ListWidget)
#    base_order = ('name', 'asc')
#    list_widget= 'list_widget'


class ProfilesourceDetailView(ModelView):
    datamodel=SQLAInterface(Profilesource, db.session)
    related_views = []
    show_title='Profilesource Detail'
    add_title ='Add Profilesource'
    list_title= 'Profilesource List'
    edit_title = 'Edit Profilesource'
    show_columns = ['id', 'individual', 'import_address', 'profile_username', 'profile_password', 'has_been_imported', 'import_data', 'import_date', 'profilesource']
#    show_exclude_columns = [] #= ['id', 'individual', 'import_address', 'profile_username', 'profile_password', 'has_been_imported', 'import_data', 'import_date', 'profilesource']
#
#    add_columns = ['id', 'individual', 'import_address', 'profile_username', 'profile_password', 'has_been_imported', 'import_data', 'import_date', 'profilesource']
#    add_exclude_columns = [hide_list] #['id', 'individual', 'import_address', 'profile_username', 'profile_password', 'has_been_imported', 'import_data', 'import_date', 'profilesource']
#
#    edit_columns = ['id', 'individual', 'import_address', 'profile_username', 'profile_password', 'has_been_imported', 'import_data', 'import_date', 'profilesource']
#    edit_exclude_columns =[hide_list] # ['id', 'individual', 'import_address', 'profile_username', 'profile_password', 'has_been_imported', 'import_data', 'import_date', 'profilesource']
#
#    list_columns = ['id', 'individual', 'import_address', 'profile_username', 'profile_password', 'has_been_imported', 'import_data', 'import_date', 'profilesource']
#    list_exclude_columns = [] # ['id', 'individual', 'import_address', 'profile_username', 'profile_password', 'has_been_imported', 'import_data', 'import_date', 'profilesource']
#
#    search_columns = ['id', 'individual', 'import_address', 'profile_username', 'profile_password', 'has_been_imported', 'import_data', 'import_date', 'profilesource']
#    search_exclude_columns= [] # ['id', 'individual', 'import_address', 'profile_username', 'profile_password', 'has_been_imported', 'import_data', 'import_date', 'profilesource']
#
#    default_sort = [('id', True)]
#    base_permissions = ['can_list', 'can_show', 'can_edit', 'can_delete', 'can_add']
#    label_columns=   [{column.name: column.name for column in table.columns} ]
#    show_template =  'appbuilder/general/model/show_cascade.html'
#    list_template = 'appbuilder/general/model/list.html'
#    add_template = 'appbuilder/general/model/add.html'
#    edit_template = 'appbuilder/general/model/edit.html'
#    add_widget = (FormVerticalWidget|FormInlineWidget)
#    show_widget = ShowBlockWidget
#    list_widget = (ListThumbnail|ListWidget)
#    base_order = ('name', 'asc')
#    list_widget= 'list_widget'


class ProfileDetailView(ModelView):
    datamodel=SQLAInterface(Profile, db.session)
    related_views = []
    show_title='Profile Detail'
    add_title ='Add Profile'
    list_title= 'Profile List'
    edit_title = 'Edit Profile'
    show_columns = ['id', 'individual', 'import_address', 'profile_username', 'profile_password', 'has_been_imported', 'import_data', 'import_date', 'profilesource']
#    show_exclude_columns = [] #= ['id', 'individual', 'import_address', 'profile_username', 'profile_password', 'has_been_imported', 'import_data', 'import_date', 'profilesource']
#
#    add_columns = ['id', 'individual', 'import_address', 'profile_username', 'profile_password', 'has_been_imported', 'import_data', 'import_date', 'profilesource']
#    add_exclude_columns = [hide_list] #['id', 'individual', 'import_address', 'profile_username', 'profile_password', 'has_been_imported', 'import_data', 'import_date', 'profilesource']
#
#    edit_columns = ['id', 'individual', 'import_address', 'profile_username', 'profile_password', 'has_been_imported', 'import_data', 'import_date', 'profilesource']
#    edit_exclude_columns =[hide_list] # ['id', 'individual', 'import_address', 'profile_username', 'profile_password', 'has_been_imported', 'import_data', 'import_date', 'profilesource']
#
#    list_columns = ['id', 'individual', 'import_address', 'profile_username', 'profile_password', 'has_been_imported', 'import_data', 'import_date', 'profilesource']
#    list_exclude_columns = [] # ['id', 'individual', 'import_address', 'profile_username', 'profile_password', 'has_been_imported', 'import_data', 'import_date', 'profilesource']
#
#    search_columns = ['id', 'individual', 'import_address', 'profile_username', 'profile_password', 'has_been_imported', 'import_data', 'import_date', 'profilesource']
#    search_exclude_columns= [] # ['id', 'individual', 'import_address', 'profile_username', 'profile_password', 'has_been_imported', 'import_data', 'import_date', 'profilesource']
#
#    default_sort = [('id', True)]
#    base_permissions = ['can_list', 'can_show', 'can_edit', 'can_delete', 'can_add']
#    label_columns=   [{column.name: column.name for column in table.columns} ]
#    show_template =  'appbuilder/general/model/show_cascade.html'
#    list_template = 'appbuilder/general/model/list.html'
#    add_template = 'appbuilder/general/model/add.html'
#    edit_template = 'appbuilder/general/model/edit.html'
#    add_widget = (FormVerticalWidget|FormInlineWidget)
#    show_widget = ShowBlockWidget
#    list_widget = (ListThumbnail|ListWidget)
#    base_order = ('name', 'asc')
#    list_widget= 'list_widget'


class LocationDetailView(ModelView):
    datamodel=SQLAInterface(Location, db.session)
    related_views = []
    show_title='Location Detail'
    add_title ='Add Location'
    list_title= 'Location List'
    edit_title = 'Edit Location'
    show_columns = ['id', 'individual', 'template', 'header', 'color', 'location', 'summary_text', 'has_been_generated', 'preferred']
#    show_exclude_columns = [] #= ['id', 'individual', 'template', 'header', 'color', 'location', 'summary_text', 'has_been_generated', 'preferred']
#
#    add_columns = ['id', 'individual', 'template', 'header', 'color', 'location', 'summary_text', 'has_been_generated', 'preferred']
#    add_exclude_columns = [hide_list] #['id', 'individual', 'template', 'header', 'color', 'location', 'summary_text', 'has_been_generated', 'preferred']
#
#    edit_columns = ['id', 'individual', 'template', 'header', 'color', 'location', 'summary_text', 'has_been_generated', 'preferred']
#    edit_exclude_columns =[hide_list] # ['id', 'individual', 'template', 'header', 'color', 'location', 'summary_text', 'has_been_generated', 'preferred']
#
#    list_columns = ['id', 'individual', 'template', 'header', 'color', 'location', 'summary_text', 'has_been_generated', 'preferred']
#    list_exclude_columns = [] # ['id', 'individual', 'template', 'header', 'color', 'location', 'summary_text', 'has_been_generated', 'preferred']
#
#    search_columns = ['id', 'individual', 'template', 'header', 'color', 'location', 'summary_text', 'has_been_generated', 'preferred']
#    search_exclude_columns= [] # ['id', 'individual', 'template', 'header', 'color', 'location', 'summary_text', 'has_been_generated', 'preferred']
#
#    default_sort = [('id', True)]
#    base_permissions = ['can_list', 'can_show', 'can_edit', 'can_delete', 'can_add']
#    label_columns=   [{column.name: column.name for column in table.columns} ]
#    show_template =  'appbuilder/general/model/show_cascade.html'
#    list_template = 'appbuilder/general/model/list.html'
#    add_template = 'appbuilder/general/model/add.html'
#    edit_template = 'appbuilder/general/model/edit.html'
#    add_widget = (FormVerticalWidget|FormInlineWidget)
#    show_widget = ShowBlockWidget
#    list_widget = (ListThumbnail|ListWidget)
#    base_order = ('name', 'asc')
#    list_widget= 'list_widget'


class ResumeDetailView(ModelView):
    datamodel=SQLAInterface(Resume, db.session)
    related_views = []
    show_title='Resume Detail'
    add_title ='Add Resume'
    list_title= 'Resume List'
    edit_title = 'Edit Resume'
    show_columns = ['id', 'individual', 'template', 'header', 'color', 'location', 'summary_text', 'has_been_generated', 'preferred']
#    show_exclude_columns = [] #= ['id', 'individual', 'template', 'header', 'color', 'location', 'summary_text', 'has_been_generated', 'preferred']
#
#    add_columns = ['id', 'individual', 'template', 'header', 'color', 'location', 'summary_text', 'has_been_generated', 'preferred']
#    add_exclude_columns = [hide_list] #['id', 'individual', 'template', 'header', 'color', 'location', 'summary_text', 'has_been_generated', 'preferred']
#
#    edit_columns = ['id', 'individual', 'template', 'header', 'color', 'location', 'summary_text', 'has_been_generated', 'preferred']
#    edit_exclude_columns =[hide_list] # ['id', 'individual', 'template', 'header', 'color', 'location', 'summary_text', 'has_been_generated', 'preferred']
#
#    list_columns = ['id', 'individual', 'template', 'header', 'color', 'location', 'summary_text', 'has_been_generated', 'preferred']
#    list_exclude_columns = [] # ['id', 'individual', 'template', 'header', 'color', 'location', 'summary_text', 'has_been_generated', 'preferred']
#
#    search_columns = ['id', 'individual', 'template', 'header', 'color', 'location', 'summary_text', 'has_been_generated', 'preferred']
#    search_exclude_columns= [] # ['id', 'individual', 'template', 'header', 'color', 'location', 'summary_text', 'has_been_generated', 'preferred']
#
#    default_sort = [('id', True)]
#    base_permissions = ['can_list', 'can_show', 'can_edit', 'can_delete', 'can_add']
#    label_columns=   [{column.name: column.name for column in table.columns} ]
#    show_template =  'appbuilder/general/model/show_cascade.html'
#    list_template = 'appbuilder/general/model/list.html'
#    add_template = 'appbuilder/general/model/add.html'
#    edit_template = 'appbuilder/general/model/edit.html'
#    add_widget = (FormVerticalWidget|FormInlineWidget)
#    show_widget = ShowBlockWidget
#    list_widget = (ListThumbnail|ListWidget)
#    base_order = ('name', 'asc')
#    list_widget= 'list_widget'


class SwarmDetailView(ModelView):
    datamodel=SQLAInterface(Swarm, db.session)
    related_views = []
    show_title='Swarm Detail'
    add_title ='Add Swarm'
    list_title= 'Swarm List'
    edit_title = 'Edit Swarm'
    show_columns = ['individual', 'swarm']
#    show_exclude_columns = [] #= ['individual', 'swarm']
#
#    add_columns = ['individual', 'swarm']
#    add_exclude_columns = [hide_list] #['individual', 'swarm']
#
#    edit_columns = ['individual', 'swarm']
#    edit_exclude_columns =[hide_list] # ['individual', 'swarm']
#
#    list_columns = ['individual', 'swarm']
#    list_exclude_columns = [] # ['individual', 'swarm']
#
#    search_columns = ['individual', 'swarm']
#    search_exclude_columns= [] # ['individual', 'swarm']
#
#    default_sort = [('id', True)]
#    base_permissions = ['can_list', 'can_show', 'can_edit', 'can_delete', 'can_add']
#    label_columns=   [{column.name: column.name for column in table.columns} ]
#    show_template =  'appbuilder/general/model/show_cascade.html'
#    list_template = 'appbuilder/general/model/list.html'
#    add_template = 'appbuilder/general/model/add.html'
#    edit_template = 'appbuilder/general/model/edit.html'
#    add_widget = (FormVerticalWidget|FormInlineWidget)
#    show_widget = ShowBlockWidget
#    list_widget = (ListThumbnail|ListWidget)
#    base_order = ('name', 'asc')
#    list_widget= 'list_widget'


class IndividualSwarmDetailView(ModelView):
    datamodel=SQLAInterface(IndividualSwarm, db.session)
    related_views = []
    show_title='IndividualSwarm Detail'
    add_title ='Add IndividualSwarm'
    list_title= 'IndividualSwarm List'
    edit_title = 'Edit IndividualSwarm'
    show_columns = ['individual', 'swarm']
#    show_exclude_columns = [] #= ['individual', 'swarm']
#
#    add_columns = ['individual', 'swarm']
#    add_exclude_columns = [hide_list] #['individual', 'swarm']
#
#    edit_columns = ['individual', 'swarm']
#    edit_exclude_columns =[hide_list] # ['individual', 'swarm']
#
#    list_columns = ['individual', 'swarm']
#    list_exclude_columns = [] # ['individual', 'swarm']
#
#    search_columns = ['individual', 'swarm']
#    search_exclude_columns= [] # ['individual', 'swarm']
#
#    default_sort = [('id', True)]
#    base_permissions = ['can_list', 'can_show', 'can_edit', 'can_delete', 'can_add']
#    label_columns=   [{column.name: column.name for column in table.columns} ]
#    show_template =  'appbuilder/general/model/show_cascade.html'
#    list_template = 'appbuilder/general/model/list.html'
#    add_template = 'appbuilder/general/model/add.html'
#    edit_template = 'appbuilder/general/model/edit.html'
#    add_widget = (FormVerticalWidget|FormInlineWidget)
#    show_widget = ShowBlockWidget
#    list_widget = (ListThumbnail|ListWidget)
#    base_order = ('name', 'asc')
#    list_widget= 'list_widget'


class IndividualMasterView(MasterDetailView):
    datamodel=SQLAInterface(Individual, db.session)
    related_views = [UserxDetailView]
    show_title='Individual Detail'
    add_title ='Add Individual'
    list_title= 'Individual List'
    edit_title = 'Edit Individual'
    show_columns = ['id', 'userx', 'is_individual', 'is_institution', 'is_company', 'is_government', 'is_online']
#    show_exclude_columns = [] #= ['id', 'userx', 'is_individual', 'is_institution', 'is_company', 'is_government', 'is_online']
#
#    add_columns = ['id', 'userx', 'is_individual', 'is_institution', 'is_company', 'is_government', 'is_online']
#    add_exclude_columns = [hide_list] #['id', 'userx', 'is_individual', 'is_institution', 'is_company', 'is_government', 'is_online']
#
#    edit_columns = ['id', 'userx', 'is_individual', 'is_institution', 'is_company', 'is_government', 'is_online']
#    edit_exclude_columns =[hide_list] # ['id', 'userx', 'is_individual', 'is_institution', 'is_company', 'is_government', 'is_online']
#
#    list_columns = ['id', 'userx', 'is_individual', 'is_institution', 'is_company', 'is_government', 'is_online']
#    list_exclude_columns = [] # ['id', 'userx', 'is_individual', 'is_institution', 'is_company', 'is_government', 'is_online']
#
#    search_columns = ['id', 'userx', 'is_individual', 'is_institution', 'is_company', 'is_government', 'is_online']
#    search_exclude_columns= [] # ['id', 'userx', 'is_individual', 'is_institution', 'is_company', 'is_government', 'is_online']
#
#    default_sort = [('id', True)]
#    base_permissions = ['can_list', 'can_show', 'can_edit', 'can_delete', 'can_add']
#    label_columns=   [{column.name: column.name for column in table.columns} ]
#    show_template =  'appbuilder/general/model/show_cascade.html'
#    list_template = 'appbuilder/general/model/list.html'
#    add_template = 'appbuilder/general/model/add.html'
#    edit_template = 'appbuilder/general/model/edit.html'
#    add_widget = (FormVerticalWidget|FormInlineWidget)
#    show_widget = ShowBlockWidget
#    list_widget = (ListThumbnail|ListWidget)
#    base_order = ('name', 'asc')
#    list_widget= 'list_widget'


class IndustryJobMasterView(MasterDetailView):
    datamodel=SQLAInterface(IndustryJob, db.session)
    related_views = [IndustryDetailView]
    show_title='IndustryJob Detail'
    add_title ='Add IndustryJob'
    list_title= 'IndustryJob List'
    edit_title = 'Edit IndustryJob'
    show_columns = ['industry', 'job']
#    show_exclude_columns = [] #= ['industry', 'job']
#
#    add_columns = ['industry', 'job']
#    add_exclude_columns = [hide_list] #['industry', 'job']
#
#    edit_columns = ['industry', 'job']
#    edit_exclude_columns =[hide_list] # ['industry', 'job']
#
#    list_columns = ['industry', 'job']
#    list_exclude_columns = [] # ['industry', 'job']
#
#    search_columns = ['industry', 'job']
#    search_exclude_columns= [] # ['industry', 'job']
#
#    default_sort = [('id', True)]
#    base_permissions = ['can_list', 'can_show', 'can_edit', 'can_delete', 'can_add']
#    label_columns=   [{column.name: column.name for column in table.columns} ]
#    show_template =  'appbuilder/general/model/show_cascade.html'
#    list_template = 'appbuilder/general/model/list.html'
#    add_template = 'appbuilder/general/model/add.html'
#    edit_template = 'appbuilder/general/model/edit.html'
#    add_widget = (FormVerticalWidget|FormInlineWidget)
#    show_widget = ShowBlockWidget
#    list_widget = (ListThumbnail|ListWidget)
#    base_order = ('name', 'asc')
#    list_widget= 'list_widget'


class IndustryJobMultiView(MultipleView):
    datamodel=SQLAInterface(IndustryJob, db.session)
    views = [IndustryDetailView, JobDetailView]
    show_title='IndustryJob Detail'
    add_title ='Add IndustryJob'
    list_title= 'IndustryJob List'
    edit_title = 'Edit IndustryJob'
    show_columns = ['industry', 'job']
#    show_exclude_columns = [] #= ['industry', 'job']
#
#    add_columns = ['industry', 'job']
#    add_exclude_columns = [hide_list] #['industry', 'job']
#
#    edit_columns = ['industry', 'job']
#    edit_exclude_columns =[hide_list] # ['industry', 'job']
#
#    list_columns = ['industry', 'job']
#    list_exclude_columns = [] # ['industry', 'job']
#
#    search_columns = ['industry', 'job']
#    search_exclude_columns= [] # ['industry', 'job']
#
#    default_sort = [('id', True)]
#    base_permissions = ['can_list', 'can_show', 'can_edit', 'can_delete', 'can_add']
#    label_columns=   [{column.name: column.name for column in table.columns} ]
#    show_template =  'appbuilder/general/model/show_cascade.html'
#    list_template = 'appbuilder/general/model/list.html'
#    add_template = 'appbuilder/general/model/add.html'
#    edit_template = 'appbuilder/general/model/edit.html'
#    add_widget = (FormVerticalWidget|FormInlineWidget)
#    show_widget = ShowBlockWidget
#    list_widget = (ListThumbnail|ListWidget)
#    base_order = ('name', 'asc')
#    list_widget= 'list_widget'


class JobSkillMasterView(MasterDetailView):
    datamodel=SQLAInterface(JobSkill, db.session)
    related_views = [JobDetailView]
    show_title='JobSkill Detail'
    add_title ='Add JobSkill'
    list_title= 'JobSkill List'
    edit_title = 'Edit JobSkill'
    show_columns = ['skills', 'jobs']
#    show_exclude_columns = [] #= ['skills', 'jobs']
#
#    add_columns = ['skills', 'jobs']
#    add_exclude_columns = [hide_list] #['skills', 'jobs']
#
#    edit_columns = ['skills', 'jobs']
#    edit_exclude_columns =[hide_list] # ['skills', 'jobs']
#
#    list_columns = ['skills', 'jobs']
#    list_exclude_columns = [] # ['skills', 'jobs']
#
#    search_columns = ['skills', 'jobs']
#    search_exclude_columns= [] # ['skills', 'jobs']
#
#    default_sort = [('id', True)]
#    base_permissions = ['can_list', 'can_show', 'can_edit', 'can_delete', 'can_add']
#    label_columns=   [{column.name: column.name for column in table.columns} ]
#    show_template =  'appbuilder/general/model/show_cascade.html'
#    list_template = 'appbuilder/general/model/list.html'
#    add_template = 'appbuilder/general/model/add.html'
#    edit_template = 'appbuilder/general/model/edit.html'
#    add_widget = (FormVerticalWidget|FormInlineWidget)
#    show_widget = ShowBlockWidget
#    list_widget = (ListThumbnail|ListWidget)
#    base_order = ('name', 'asc')
#    list_widget= 'list_widget'


class JobSkillMultiView(MultipleView):
    datamodel=SQLAInterface(JobSkill, db.session)
    views = [SkillDetailView]
    show_title='JobSkill Detail'
    add_title ='Add JobSkill'
    list_title= 'JobSkill List'
    edit_title = 'Edit JobSkill'
    show_columns = ['skills', 'jobs']
#    show_exclude_columns = [] #= ['skills', 'jobs']
#
#    add_columns = ['skills', 'jobs']
#    add_exclude_columns = [hide_list] #['skills', 'jobs']
#
#    edit_columns = ['skills', 'jobs']
#    edit_exclude_columns =[hide_list] # ['skills', 'jobs']
#
#    list_columns = ['skills', 'jobs']
#    list_exclude_columns = [] # ['skills', 'jobs']
#
#    search_columns = ['skills', 'jobs']
#    search_exclude_columns= [] # ['skills', 'jobs']
#
#    default_sort = [('id', True)]
#    base_permissions = ['can_list', 'can_show', 'can_edit', 'can_delete', 'can_add']
#    label_columns=   [{column.name: column.name for column in table.columns} ]
#    show_template =  'appbuilder/general/model/show_cascade.html'
#    list_template = 'appbuilder/general/model/list.html'
#    add_template = 'appbuilder/general/model/add.html'
#    edit_template = 'appbuilder/general/model/edit.html'
#    add_widget = (FormVerticalWidget|FormInlineWidget)
#    show_widget = ShowBlockWidget
#    list_widget = (ListThumbnail|ListWidget)
#    base_order = ('name', 'asc')
#    list_widget= 'list_widget'


class EducationMasterView(MasterDetailView):
    datamodel=SQLAInterface(Education, db.session)
    related_views = [IndividualDetailView]
    show_title='Education Detail'
    add_title ='Add Education'
    list_title= 'Education List'
    edit_title = 'Edit Education'
    show_columns = ['id', 'individual', 'qualification', 'qual_class', 'verified', 'verification_code', 'verified_by', 'verification_date', 'verification_doc']
#    show_exclude_columns = [] #= ['id', 'individual', 'qualification', 'qual_class', 'verified', 'verification_code', 'verified_by', 'verification_date', 'verification_doc']
#
#    add_columns = ['id', 'individual', 'qualification', 'qual_class', 'verified', 'verification_code', 'verified_by', 'verification_date', 'verification_doc']
#    add_exclude_columns = [hide_list] #['id', 'individual', 'qualification', 'qual_class', 'verified', 'verification_code', 'verified_by', 'verification_date', 'verification_doc']
#
#    edit_columns = ['id', 'individual', 'qualification', 'qual_class', 'verified', 'verification_code', 'verified_by', 'verification_date', 'verification_doc']
#    edit_exclude_columns =[hide_list] # ['id', 'individual', 'qualification', 'qual_class', 'verified', 'verification_code', 'verified_by', 'verification_date', 'verification_doc']
#
#    list_columns = ['id', 'individual', 'qualification', 'qual_class', 'verified', 'verification_code', 'verified_by', 'verification_date', 'verification_doc']
#    list_exclude_columns = [] # ['id', 'individual', 'qualification', 'qual_class', 'verified', 'verification_code', 'verified_by', 'verification_date', 'verification_doc']
#
#    search_columns = ['id', 'individual', 'qualification', 'qual_class', 'verified', 'verification_code', 'verified_by', 'verification_date', 'verification_doc']
#    search_exclude_columns= [] # ['id', 'individual', 'qualification', 'qual_class', 'verified', 'verification_code', 'verified_by', 'verification_date', 'verification_doc']
#
#    default_sort = [('id', True)]
#    base_permissions = ['can_list', 'can_show', 'can_edit', 'can_delete', 'can_add']
#    label_columns=   [{column.name: column.name for column in table.columns} ]
#    show_template =  'appbuilder/general/model/show_cascade.html'
#    list_template = 'appbuilder/general/model/list.html'
#    add_template = 'appbuilder/general/model/add.html'
#    edit_template = 'appbuilder/general/model/edit.html'
#    add_widget = (FormVerticalWidget|FormInlineWidget)
#    show_widget = ShowBlockWidget
#    list_widget = (ListThumbnail|ListWidget)
#    base_order = ('name', 'asc')
#    list_widget= 'list_widget'


class IndividualJobMasterView(MasterDetailView):
    datamodel=SQLAInterface(IndividualJob, db.session)
    related_views = [IndividualDetailView]
    show_title='IndividualJob Detail'
    add_title ='Add IndividualJob'
    list_title= 'IndividualJob List'
    edit_title = 'Edit IndividualJob'
    show_columns = ['individual', 'job']
#    show_exclude_columns = [] #= ['individual', 'job']
#
#    add_columns = ['individual', 'job']
#    add_exclude_columns = [hide_list] #['individual', 'job']
#
#    edit_columns = ['individual', 'job']
#    edit_exclude_columns =[hide_list] # ['individual', 'job']
#
#    list_columns = ['individual', 'job']
#    list_exclude_columns = [] # ['individual', 'job']
#
#    search_columns = ['individual', 'job']
#    search_exclude_columns= [] # ['individual', 'job']
#
#    default_sort = [('id', True)]
#    base_permissions = ['can_list', 'can_show', 'can_edit', 'can_delete', 'can_add']
#    label_columns=   [{column.name: column.name for column in table.columns} ]
#    show_template =  'appbuilder/general/model/show_cascade.html'
#    list_template = 'appbuilder/general/model/list.html'
#    add_template = 'appbuilder/general/model/add.html'
#    edit_template = 'appbuilder/general/model/edit.html'
#    add_widget = (FormVerticalWidget|FormInlineWidget)
#    show_widget = ShowBlockWidget
#    list_widget = (ListThumbnail|ListWidget)
#    base_order = ('name', 'asc')
#    list_widget= 'list_widget'


class IndividualJobMultiView(MultipleView):
    datamodel=SQLAInterface(IndividualJob, db.session)
    views = []
    show_title='IndividualJob Detail'
    add_title ='Add IndividualJob'
    list_title= 'IndividualJob List'
    edit_title = 'Edit IndividualJob'
    show_columns = ['individual', 'job']
#    show_exclude_columns = [] #= ['individual', 'job']
#
#    add_columns = ['individual', 'job']
#    add_exclude_columns = [hide_list] #['individual', 'job']
#
#    edit_columns = ['individual', 'job']
#    edit_exclude_columns =[hide_list] # ['individual', 'job']
#
#    list_columns = ['individual', 'job']
#    list_exclude_columns = [] # ['individual', 'job']
#
#    search_columns = ['individual', 'job']
#    search_exclude_columns= [] # ['individual', 'job']
#
#    default_sort = [('id', True)]
#    base_permissions = ['can_list', 'can_show', 'can_edit', 'can_delete', 'can_add']
#    label_columns=   [{column.name: column.name for column in table.columns} ]
#    show_template =  'appbuilder/general/model/show_cascade.html'
#    list_template = 'appbuilder/general/model/list.html'
#    add_template = 'appbuilder/general/model/add.html'
#    edit_template = 'appbuilder/general/model/edit.html'
#    add_widget = (FormVerticalWidget|FormInlineWidget)
#    show_widget = ShowBlockWidget
#    list_widget = (ListThumbnail|ListWidget)
#    base_order = ('name', 'asc')
#    list_widget= 'list_widget'


class LocationMasterView(MasterDetailView):
    datamodel=SQLAInterface(Location, db.session)
    related_views = [IndividualDetailView]
    show_title='Location Detail'
    add_title ='Add Location'
    list_title= 'Location List'
    edit_title = 'Edit Location'
    show_columns = ['id', 'individual']
#    show_exclude_columns = [] #= ['id', 'individual']
#
#    add_columns = ['id', 'individual']
#    add_exclude_columns = [hide_list] #['id', 'individual']
#
#    edit_columns = ['id', 'individual']
#    edit_exclude_columns =[hide_list] # ['id', 'individual']
#
#    list_columns = ['id', 'individual']
#    list_exclude_columns = [] # ['id', 'individual']
#
#    search_columns = ['id', 'individual']
#    search_exclude_columns= [] # ['id', 'individual']
#
#    default_sort = [('id', True)]
#    base_permissions = ['can_list', 'can_show', 'can_edit', 'can_delete', 'can_add']
#    label_columns=   [{column.name: column.name for column in table.columns} ]
#    show_template =  'appbuilder/general/model/show_cascade.html'
#    list_template = 'appbuilder/general/model/list.html'
#    add_template = 'appbuilder/general/model/add.html'
#    edit_template = 'appbuilder/general/model/edit.html'
#    add_widget = (FormVerticalWidget|FormInlineWidget)
#    show_widget = ShowBlockWidget
#    list_widget = (ListThumbnail|ListWidget)
#    base_order = ('name', 'asc')
#    list_widget= 'list_widget'


class PortalMasterView(MasterDetailView):
    datamodel=SQLAInterface(Portal, db.session)
    related_views = [IndividualDetailView]
    show_title='Portal Detail'
    add_title ='Add Portal'
    list_title= 'Portal List'
    edit_title = 'Edit Portal'
    show_columns = ['id', 'portal_url', 'is_primary', 'portal_state', 'individual', 'has_custom_domain', 'domain', 'header_text', 'slug', 'automatic_fulfillment_digital_products', 'default_digital_max_downloads', 'default_digital_url_valid_days', 'default_mail_sender_name', 'default_mail_sender_address', 'fulfillment_auto_approve', 'fulfillment_allow_unpaid', 'reserve_stock_duration_anonymous_user', 'reserve_stock_duration_authenticated_user', 'limit_quantity_per_checkout', 'gift_card_expiry_type', 'gift_card_expiry_period_type', 'gift_card_expiry_period', 'charge_taxes_on_shipping', 'include_taxes_in_prices', 'display_gross_prices', 'language']
#    show_exclude_columns = [] #= ['id', 'portal_url', 'is_primary', 'portal_state', 'individual', 'has_custom_domain', 'domain', 'header_text', 'slug', 'automatic_fulfillment_digital_products', 'default_digital_max_downloads', 'default_digital_url_valid_days', 'default_mail_sender_name', 'default_mail_sender_address', 'fulfillment_auto_approve', 'fulfillment_allow_unpaid', 'reserve_stock_duration_anonymous_user', 'reserve_stock_duration_authenticated_user', 'limit_quantity_per_checkout', 'gift_card_expiry_type', 'gift_card_expiry_period_type', 'gift_card_expiry_period', 'charge_taxes_on_shipping', 'include_taxes_in_prices', 'display_gross_prices', 'language']
#
#    add_columns = ['id', 'portal_url', 'is_primary', 'portal_state', 'individual', 'has_custom_domain', 'domain', 'header_text', 'slug', 'automatic_fulfillment_digital_products', 'default_digital_max_downloads', 'default_digital_url_valid_days', 'default_mail_sender_name', 'default_mail_sender_address', 'fulfillment_auto_approve', 'fulfillment_allow_unpaid', 'reserve_stock_duration_anonymous_user', 'reserve_stock_duration_authenticated_user', 'limit_quantity_per_checkout', 'gift_card_expiry_type', 'gift_card_expiry_period_type', 'gift_card_expiry_period', 'charge_taxes_on_shipping', 'include_taxes_in_prices', 'display_gross_prices', 'language']
#    add_exclude_columns = [hide_list] #['id', 'portal_url', 'is_primary', 'portal_state', 'individual', 'has_custom_domain', 'domain', 'header_text', 'slug', 'automatic_fulfillment_digital_products', 'default_digital_max_downloads', 'default_digital_url_valid_days', 'default_mail_sender_name', 'default_mail_sender_address', 'fulfillment_auto_approve', 'fulfillment_allow_unpaid', 'reserve_stock_duration_anonymous_user', 'reserve_stock_duration_authenticated_user', 'limit_quantity_per_checkout', 'gift_card_expiry_type', 'gift_card_expiry_period_type', 'gift_card_expiry_period', 'charge_taxes_on_shipping', 'include_taxes_in_prices', 'display_gross_prices', 'language']
#
#    edit_columns = ['id', 'portal_url', 'is_primary', 'portal_state', 'individual', 'has_custom_domain', 'domain', 'header_text', 'slug', 'automatic_fulfillment_digital_products', 'default_digital_max_downloads', 'default_digital_url_valid_days', 'default_mail_sender_name', 'default_mail_sender_address', 'fulfillment_auto_approve', 'fulfillment_allow_unpaid', 'reserve_stock_duration_anonymous_user', 'reserve_stock_duration_authenticated_user', 'limit_quantity_per_checkout', 'gift_card_expiry_type', 'gift_card_expiry_period_type', 'gift_card_expiry_period', 'charge_taxes_on_shipping', 'include_taxes_in_prices', 'display_gross_prices', 'language']
#    edit_exclude_columns =[hide_list] # ['id', 'portal_url', 'is_primary', 'portal_state', 'individual', 'has_custom_domain', 'domain', 'header_text', 'slug', 'automatic_fulfillment_digital_products', 'default_digital_max_downloads', 'default_digital_url_valid_days', 'default_mail_sender_name', 'default_mail_sender_address', 'fulfillment_auto_approve', 'fulfillment_allow_unpaid', 'reserve_stock_duration_anonymous_user', 'reserve_stock_duration_authenticated_user', 'limit_quantity_per_checkout', 'gift_card_expiry_type', 'gift_card_expiry_period_type', 'gift_card_expiry_period', 'charge_taxes_on_shipping', 'include_taxes_in_prices', 'display_gross_prices', 'language']
#
#    list_columns = ['id', 'portal_url', 'is_primary', 'portal_state', 'individual', 'has_custom_domain', 'domain', 'header_text', 'slug', 'automatic_fulfillment_digital_products', 'default_digital_max_downloads', 'default_digital_url_valid_days', 'default_mail_sender_name', 'default_mail_sender_address', 'fulfillment_auto_approve', 'fulfillment_allow_unpaid', 'reserve_stock_duration_anonymous_user', 'reserve_stock_duration_authenticated_user', 'limit_quantity_per_checkout', 'gift_card_expiry_type', 'gift_card_expiry_period_type', 'gift_card_expiry_period', 'charge_taxes_on_shipping', 'include_taxes_in_prices', 'display_gross_prices', 'language']
#    list_exclude_columns = [] # ['id', 'portal_url', 'is_primary', 'portal_state', 'individual', 'has_custom_domain', 'domain', 'header_text', 'slug', 'automatic_fulfillment_digital_products', 'default_digital_max_downloads', 'default_digital_url_valid_days', 'default_mail_sender_name', 'default_mail_sender_address', 'fulfillment_auto_approve', 'fulfillment_allow_unpaid', 'reserve_stock_duration_anonymous_user', 'reserve_stock_duration_authenticated_user', 'limit_quantity_per_checkout', 'gift_card_expiry_type', 'gift_card_expiry_period_type', 'gift_card_expiry_period', 'charge_taxes_on_shipping', 'include_taxes_in_prices', 'display_gross_prices', 'language']
#
#    search_columns = ['id', 'portal_url', 'is_primary', 'portal_state', 'individual', 'has_custom_domain', 'domain', 'header_text', 'slug', 'automatic_fulfillment_digital_products', 'default_digital_max_downloads', 'default_digital_url_valid_days', 'default_mail_sender_name', 'default_mail_sender_address', 'fulfillment_auto_approve', 'fulfillment_allow_unpaid', 'reserve_stock_duration_anonymous_user', 'reserve_stock_duration_authenticated_user', 'limit_quantity_per_checkout', 'gift_card_expiry_type', 'gift_card_expiry_period_type', 'gift_card_expiry_period', 'charge_taxes_on_shipping', 'include_taxes_in_prices', 'display_gross_prices', 'language']
#    search_exclude_columns= [] # ['id', 'portal_url', 'is_primary', 'portal_state', 'individual', 'has_custom_domain', 'domain', 'header_text', 'slug', 'automatic_fulfillment_digital_products', 'default_digital_max_downloads', 'default_digital_url_valid_days', 'default_mail_sender_name', 'default_mail_sender_address', 'fulfillment_auto_approve', 'fulfillment_allow_unpaid', 'reserve_stock_duration_anonymous_user', 'reserve_stock_duration_authenticated_user', 'limit_quantity_per_checkout', 'gift_card_expiry_type', 'gift_card_expiry_period_type', 'gift_card_expiry_period', 'charge_taxes_on_shipping', 'include_taxes_in_prices', 'display_gross_prices', 'language']
#
#    default_sort = [('id', True)]
#    base_permissions = ['can_list', 'can_show', 'can_edit', 'can_delete', 'can_add']
#    label_columns=   [{column.name: column.name for column in table.columns} ]
#    show_template =  'appbuilder/general/model/show_cascade.html'
#    list_template = 'appbuilder/general/model/list.html'
#    add_template = 'appbuilder/general/model/add.html'
#    edit_template = 'appbuilder/general/model/edit.html'
#    add_widget = (FormVerticalWidget|FormInlineWidget)
#    show_widget = ShowBlockWidget
#    list_widget = (ListThumbnail|ListWidget)
#    base_order = ('name', 'asc')
#    list_widget= 'list_widget'


class PageMasterView(MasterDetailView):
    datamodel=SQLAInterface(Page, db.session)
    related_views = [PortalDetailView]
    show_title='Page Detail'
    add_title ='Add Page'
    list_title= 'Page List'
    edit_title = 'Edit Page'
    show_columns = ['id', 'portal', 'header', 'slug', 'page_type']
#    show_exclude_columns = [] #= ['id', 'portal', 'header', 'slug', 'page_type']
#
#    add_columns = ['id', 'portal', 'header', 'slug', 'page_type']
#    add_exclude_columns = [hide_list] #['id', 'portal', 'header', 'slug', 'page_type']
#
#    edit_columns = ['id', 'portal', 'header', 'slug', 'page_type']
#    edit_exclude_columns =[hide_list] # ['id', 'portal', 'header', 'slug', 'page_type']
#
#    list_columns = ['id', 'portal', 'header', 'slug', 'page_type']
#    list_exclude_columns = [] # ['id', 'portal', 'header', 'slug', 'page_type']
#
#    search_columns = ['id', 'portal', 'header', 'slug', 'page_type']
#    search_exclude_columns= [] # ['id', 'portal', 'header', 'slug', 'page_type']
#
#    default_sort = [('id', True)]
#    base_permissions = ['can_list', 'can_show', 'can_edit', 'can_delete', 'can_add']
#    label_columns=   [{column.name: column.name for column in table.columns} ]
#    show_template =  'appbuilder/general/model/show_cascade.html'
#    list_template = 'appbuilder/general/model/list.html'
#    add_template = 'appbuilder/general/model/add.html'
#    edit_template = 'appbuilder/general/model/edit.html'
#    add_widget = (FormVerticalWidget|FormInlineWidget)
#    show_widget = ShowBlockWidget
#    list_widget = (ListThumbnail|ListWidget)
#    base_order = ('name', 'asc')
#    list_widget= 'list_widget'


class ProfileMasterView(MasterDetailView):
    datamodel=SQLAInterface(Profile, db.session)
    related_views = [IndividualDetailView]
    show_title='Profile Detail'
    add_title ='Add Profile'
    list_title= 'Profile List'
    edit_title = 'Edit Profile'
    show_columns = ['id', 'individual', 'import_address', 'profile_username', 'profile_password', 'has_been_imported', 'import_data', 'import_date', 'profilesource']
#    show_exclude_columns = [] #= ['id', 'individual', 'import_address', 'profile_username', 'profile_password', 'has_been_imported', 'import_data', 'import_date', 'profilesource']
#
#    add_columns = ['id', 'individual', 'import_address', 'profile_username', 'profile_password', 'has_been_imported', 'import_data', 'import_date', 'profilesource']
#    add_exclude_columns = [hide_list] #['id', 'individual', 'import_address', 'profile_username', 'profile_password', 'has_been_imported', 'import_data', 'import_date', 'profilesource']
#
#    edit_columns = ['id', 'individual', 'import_address', 'profile_username', 'profile_password', 'has_been_imported', 'import_data', 'import_date', 'profilesource']
#    edit_exclude_columns =[hide_list] # ['id', 'individual', 'import_address', 'profile_username', 'profile_password', 'has_been_imported', 'import_data', 'import_date', 'profilesource']
#
#    list_columns = ['id', 'individual', 'import_address', 'profile_username', 'profile_password', 'has_been_imported', 'import_data', 'import_date', 'profilesource']
#    list_exclude_columns = [] # ['id', 'individual', 'import_address', 'profile_username', 'profile_password', 'has_been_imported', 'import_data', 'import_date', 'profilesource']
#
#    search_columns = ['id', 'individual', 'import_address', 'profile_username', 'profile_password', 'has_been_imported', 'import_data', 'import_date', 'profilesource']
#    search_exclude_columns= [] # ['id', 'individual', 'import_address', 'profile_username', 'profile_password', 'has_been_imported', 'import_data', 'import_date', 'profilesource']
#
#    default_sort = [('id', True)]
#    base_permissions = ['can_list', 'can_show', 'can_edit', 'can_delete', 'can_add']
#    label_columns=   [{column.name: column.name for column in table.columns} ]
#    show_template =  'appbuilder/general/model/show_cascade.html'
#    list_template = 'appbuilder/general/model/list.html'
#    add_template = 'appbuilder/general/model/add.html'
#    edit_template = 'appbuilder/general/model/edit.html'
#    add_widget = (FormVerticalWidget|FormInlineWidget)
#    show_widget = ShowBlockWidget
#    list_widget = (ListThumbnail|ListWidget)
#    base_order = ('name', 'asc')
#    list_widget= 'list_widget'


class ProfileMultiView(MultipleView):
    datamodel=SQLAInterface(Profile, db.session)
    views = [ProfilesourceDetailView]
    show_title='Profile Detail'
    add_title ='Add Profile'
    list_title= 'Profile List'
    edit_title = 'Edit Profile'
    show_columns = ['id', 'individual', 'import_address', 'profile_username', 'profile_password', 'has_been_imported', 'import_data', 'import_date', 'profilesource']
#    show_exclude_columns = [] #= ['id', 'individual', 'import_address', 'profile_username', 'profile_password', 'has_been_imported', 'import_data', 'import_date', 'profilesource']
#
#    add_columns = ['id', 'individual', 'import_address', 'profile_username', 'profile_password', 'has_been_imported', 'import_data', 'import_date', 'profilesource']
#    add_exclude_columns = [hide_list] #['id', 'individual', 'import_address', 'profile_username', 'profile_password', 'has_been_imported', 'import_data', 'import_date', 'profilesource']
#
#    edit_columns = ['id', 'individual', 'import_address', 'profile_username', 'profile_password', 'has_been_imported', 'import_data', 'import_date', 'profilesource']
#    edit_exclude_columns =[hide_list] # ['id', 'individual', 'import_address', 'profile_username', 'profile_password', 'has_been_imported', 'import_data', 'import_date', 'profilesource']
#
#    list_columns = ['id', 'individual', 'import_address', 'profile_username', 'profile_password', 'has_been_imported', 'import_data', 'import_date', 'profilesource']
#    list_exclude_columns = [] # ['id', 'individual', 'import_address', 'profile_username', 'profile_password', 'has_been_imported', 'import_data', 'import_date', 'profilesource']
#
#    search_columns = ['id', 'individual', 'import_address', 'profile_username', 'profile_password', 'has_been_imported', 'import_data', 'import_date', 'profilesource']
#    search_exclude_columns= [] # ['id', 'individual', 'import_address', 'profile_username', 'profile_password', 'has_been_imported', 'import_data', 'import_date', 'profilesource']
#
#    default_sort = [('id', True)]
#    base_permissions = ['can_list', 'can_show', 'can_edit', 'can_delete', 'can_add']
#    label_columns=   [{column.name: column.name for column in table.columns} ]
#    show_template =  'appbuilder/general/model/show_cascade.html'
#    list_template = 'appbuilder/general/model/list.html'
#    add_template = 'appbuilder/general/model/add.html'
#    edit_template = 'appbuilder/general/model/edit.html'
#    add_widget = (FormVerticalWidget|FormInlineWidget)
#    show_widget = ShowBlockWidget
#    list_widget = (ListThumbnail|ListWidget)
#    base_order = ('name', 'asc')
#    list_widget= 'list_widget'


class ResumeMasterView(MasterDetailView):
    datamodel=SQLAInterface(Resume, db.session)
    related_views = [IndividualDetailView]
    show_title='Resume Detail'
    add_title ='Add Resume'
    list_title= 'Resume List'
    edit_title = 'Edit Resume'
    show_columns = ['id', 'individual', 'template', 'header', 'color', 'location', 'summary_text', 'has_been_generated', 'preferred']
#    show_exclude_columns = [] #= ['id', 'individual', 'template', 'header', 'color', 'location', 'summary_text', 'has_been_generated', 'preferred']
#
#    add_columns = ['id', 'individual', 'template', 'header', 'color', 'location', 'summary_text', 'has_been_generated', 'preferred']
#    add_exclude_columns = [hide_list] #['id', 'individual', 'template', 'header', 'color', 'location', 'summary_text', 'has_been_generated', 'preferred']
#
#    edit_columns = ['id', 'individual', 'template', 'header', 'color', 'location', 'summary_text', 'has_been_generated', 'preferred']
#    edit_exclude_columns =[hide_list] # ['id', 'individual', 'template', 'header', 'color', 'location', 'summary_text', 'has_been_generated', 'preferred']
#
#    list_columns = ['id', 'individual', 'template', 'header', 'color', 'location', 'summary_text', 'has_been_generated', 'preferred']
#    list_exclude_columns = [] # ['id', 'individual', 'template', 'header', 'color', 'location', 'summary_text', 'has_been_generated', 'preferred']
#
#    search_columns = ['id', 'individual', 'template', 'header', 'color', 'location', 'summary_text', 'has_been_generated', 'preferred']
#    search_exclude_columns= [] # ['id', 'individual', 'template', 'header', 'color', 'location', 'summary_text', 'has_been_generated', 'preferred']
#
#    default_sort = [('id', True)]
#    base_permissions = ['can_list', 'can_show', 'can_edit', 'can_delete', 'can_add']
#    label_columns=   [{column.name: column.name for column in table.columns} ]
#    show_template =  'appbuilder/general/model/show_cascade.html'
#    list_template = 'appbuilder/general/model/list.html'
#    add_template = 'appbuilder/general/model/add.html'
#    edit_template = 'appbuilder/general/model/edit.html'
#    add_widget = (FormVerticalWidget|FormInlineWidget)
#    show_widget = ShowBlockWidget
#    list_widget = (ListThumbnail|ListWidget)
#    base_order = ('name', 'asc')
#    list_widget= 'list_widget'


class ResumeMultiView(MultipleView):
    datamodel=SQLAInterface(Resume, db.session)
    views = [LocationDetailView]
    show_title='Resume Detail'
    add_title ='Add Resume'
    list_title= 'Resume List'
    edit_title = 'Edit Resume'
    show_columns = ['id', 'individual', 'template', 'header', 'color', 'location', 'summary_text', 'has_been_generated', 'preferred']
#    show_exclude_columns = [] #= ['id', 'individual', 'template', 'header', 'color', 'location', 'summary_text', 'has_been_generated', 'preferred']
#
#    add_columns = ['id', 'individual', 'template', 'header', 'color', 'location', 'summary_text', 'has_been_generated', 'preferred']
#    add_exclude_columns = [hide_list] #['id', 'individual', 'template', 'header', 'color', 'location', 'summary_text', 'has_been_generated', 'preferred']
#
#    edit_columns = ['id', 'individual', 'template', 'header', 'color', 'location', 'summary_text', 'has_been_generated', 'preferred']
#    edit_exclude_columns =[hide_list] # ['id', 'individual', 'template', 'header', 'color', 'location', 'summary_text', 'has_been_generated', 'preferred']
#
#    list_columns = ['id', 'individual', 'template', 'header', 'color', 'location', 'summary_text', 'has_been_generated', 'preferred']
#    list_exclude_columns = [] # ['id', 'individual', 'template', 'header', 'color', 'location', 'summary_text', 'has_been_generated', 'preferred']
#
#    search_columns = ['id', 'individual', 'template', 'header', 'color', 'location', 'summary_text', 'has_been_generated', 'preferred']
#    search_exclude_columns= [] # ['id', 'individual', 'template', 'header', 'color', 'location', 'summary_text', 'has_been_generated', 'preferred']
#
#    default_sort = [('id', True)]
#    base_permissions = ['can_list', 'can_show', 'can_edit', 'can_delete', 'can_add']
#    label_columns=   [{column.name: column.name for column in table.columns} ]
#    show_template =  'appbuilder/general/model/show_cascade.html'
#    list_template = 'appbuilder/general/model/list.html'
#    add_template = 'appbuilder/general/model/add.html'
#    edit_template = 'appbuilder/general/model/edit.html'
#    add_widget = (FormVerticalWidget|FormInlineWidget)
#    show_widget = ShowBlockWidget
#    list_widget = (ListThumbnail|ListWidget)
#    base_order = ('name', 'asc')
#    list_widget= 'list_widget'


class SwarmMasterView(MasterDetailView):
    datamodel=SQLAInterface(Swarm, db.session)
    related_views = [PortalDetailView]
    show_title='Swarm Detail'
    add_title ='Add Swarm'
    list_title= 'Swarm List'
    edit_title = 'Edit Swarm'
    show_columns = ['id', 'portal']
#    show_exclude_columns = [] #= ['id', 'portal']
#
#    add_columns = ['id', 'portal']
#    add_exclude_columns = [hide_list] #['id', 'portal']
#
#    edit_columns = ['id', 'portal']
#    edit_exclude_columns =[hide_list] # ['id', 'portal']
#
#    list_columns = ['id', 'portal']
#    list_exclude_columns = [] # ['id', 'portal']
#
#    search_columns = ['id', 'portal']
#    search_exclude_columns= [] # ['id', 'portal']
#
#    default_sort = [('id', True)]
#    base_permissions = ['can_list', 'can_show', 'can_edit', 'can_delete', 'can_add']
#    label_columns=   [{column.name: column.name for column in table.columns} ]
#    show_template =  'appbuilder/general/model/show_cascade.html'
#    list_template = 'appbuilder/general/model/list.html'
#    add_template = 'appbuilder/general/model/add.html'
#    edit_template = 'appbuilder/general/model/edit.html'
#    add_widget = (FormVerticalWidget|FormInlineWidget)
#    show_widget = ShowBlockWidget
#    list_widget = (ListThumbnail|ListWidget)
#    base_order = ('name', 'asc')
#    list_widget= 'list_widget'


class IndividualSwarmMasterView(MasterDetailView):
    datamodel=SQLAInterface(IndividualSwarm, db.session)
    related_views = [IndividualDetailView]
    show_title='IndividualSwarm Detail'
    add_title ='Add IndividualSwarm'
    list_title= 'IndividualSwarm List'
    edit_title = 'Edit IndividualSwarm'
    show_columns = ['individual', 'swarm']
#    show_exclude_columns = [] #= ['individual', 'swarm']
#
#    add_columns = ['individual', 'swarm']
#    add_exclude_columns = [hide_list] #['individual', 'swarm']
#
#    edit_columns = ['individual', 'swarm']
#    edit_exclude_columns =[hide_list] # ['individual', 'swarm']
#
#    list_columns = ['individual', 'swarm']
#    list_exclude_columns = [] # ['individual', 'swarm']
#
#    search_columns = ['individual', 'swarm']
#    search_exclude_columns= [] # ['individual', 'swarm']
#
#    default_sort = [('id', True)]
#    base_permissions = ['can_list', 'can_show', 'can_edit', 'can_delete', 'can_add']
#    label_columns=   [{column.name: column.name for column in table.columns} ]
#    show_template =  'appbuilder/general/model/show_cascade.html'
#    list_template = 'appbuilder/general/model/list.html'
#    add_template = 'appbuilder/general/model/add.html'
#    edit_template = 'appbuilder/general/model/edit.html'
#    add_widget = (FormVerticalWidget|FormInlineWidget)
#    show_widget = ShowBlockWidget
#    list_widget = (ListThumbnail|ListWidget)
#    base_order = ('name', 'asc')
#    list_widget= 'list_widget'


class IndividualSwarmMultiView(MultipleView):
    datamodel=SQLAInterface(IndividualSwarm, db.session)
    views = [SwarmDetailView]
    show_title='IndividualSwarm Detail'
    add_title ='Add IndividualSwarm'
    list_title= 'IndividualSwarm List'
    edit_title = 'Edit IndividualSwarm'
    show_columns = ['individual', 'swarm']
#    show_exclude_columns = [] #= ['individual', 'swarm']
#
#    add_columns = ['individual', 'swarm']
#    add_exclude_columns = [hide_list] #['individual', 'swarm']
#
#    edit_columns = ['individual', 'swarm']
#    edit_exclude_columns =[hide_list] # ['individual', 'swarm']
#
#    list_columns = ['individual', 'swarm']
#    list_exclude_columns = [] # ['individual', 'swarm']
#
#    search_columns = ['individual', 'swarm']
#    search_exclude_columns= [] # ['individual', 'swarm']
#
#    default_sort = [('id', True)]
#    base_permissions = ['can_list', 'can_show', 'can_edit', 'can_delete', 'can_add']
#    label_columns=   [{column.name: column.name for column in table.columns} ]
#    show_template =  'appbuilder/general/model/show_cascade.html'
#    list_template = 'appbuilder/general/model/list.html'
#    add_template = 'appbuilder/general/model/add.html'
#    edit_template = 'appbuilder/general/model/edit.html'
#    add_widget = (FormVerticalWidget|FormInlineWidget)
#    show_widget = ShowBlockWidget
#    list_widget = (ListThumbnail|ListWidget)
#    base_order = ('name', 'asc')
#    list_widget= 'list_widget'


class UserSkillMasterView(MasterDetailView):
    datamodel=SQLAInterface(UserSkill, db.session)
    related_views = [IndividualDetailView]
    show_title='UserSkill Detail'
    add_title ='Add UserSkill'
    list_title= 'UserSkill List'
    edit_title = 'Edit UserSkill'
    show_columns = ['skills', 'user_details']
#    show_exclude_columns = [] #= ['skills', 'user_details']
#
#    add_columns = ['skills', 'user_details']
#    add_exclude_columns = [hide_list] #['skills', 'user_details']
#
#    edit_columns = ['skills', 'user_details']
#    edit_exclude_columns =[hide_list] # ['skills', 'user_details']
#
#    list_columns = ['skills', 'user_details']
#    list_exclude_columns = [] # ['skills', 'user_details']
#
#    search_columns = ['skills', 'user_details']
#    search_exclude_columns= [] # ['skills', 'user_details']
#
#    default_sort = [('id', True)]
#    base_permissions = ['can_list', 'can_show', 'can_edit', 'can_delete', 'can_add']
#    label_columns=   [{column.name: column.name for column in table.columns} ]
#    show_template =  'appbuilder/general/model/show_cascade.html'
#    list_template = 'appbuilder/general/model/list.html'
#    add_template = 'appbuilder/general/model/add.html'
#    edit_template = 'appbuilder/general/model/edit.html'
#    add_widget = (FormVerticalWidget|FormInlineWidget)
#    show_widget = ShowBlockWidget
#    list_widget = (ListThumbnail|ListWidget)
#    base_order = ('name', 'asc')
#    list_widget= 'list_widget'


class UserSkillMultiView(MultipleView):
    datamodel=SQLAInterface(UserSkill, db.session)
    views = []
    show_title='UserSkill Detail'
    add_title ='Add UserSkill'
    list_title= 'UserSkill List'
    edit_title = 'Edit UserSkill'
    show_columns = ['skills', 'user_details']
#    show_exclude_columns = [] #= ['skills', 'user_details']
#
#    add_columns = ['skills', 'user_details']
#    add_exclude_columns = [hide_list] #['skills', 'user_details']
#
#    edit_columns = ['skills', 'user_details']
#    edit_exclude_columns =[hide_list] # ['skills', 'user_details']
#
#    list_columns = ['skills', 'user_details']
#    list_exclude_columns = [] # ['skills', 'user_details']
#
#    search_columns = ['skills', 'user_details']
#    search_exclude_columns= [] # ['skills', 'user_details']
#
#    default_sort = [('id', True)]
#    base_permissions = ['can_list', 'can_show', 'can_edit', 'can_delete', 'can_add']
#    label_columns=   [{column.name: column.name for column in table.columns} ]
#    show_template =  'appbuilder/general/model/show_cascade.html'
#    list_template = 'appbuilder/general/model/list.html'
#    add_template = 'appbuilder/general/model/add.html'
#    edit_template = 'appbuilder/general/model/edit.html'
#    add_widget = (FormVerticalWidget|FormInlineWidget)
#    show_widget = ShowBlockWidget
#    list_widget = (ListThumbnail|ListWidget)
#    base_order = ('name', 'asc')
#    list_widget= 'list_widget'


class WorkHistoryMasterView(MasterDetailView):
    datamodel=SQLAInterface(WorkHistory, db.session)
    related_views = [IndividualDetailView]
    show_title='WorkHistory Detail'
    add_title ='Add WorkHistory'
    list_title= 'WorkHistory List'
    edit_title = 'Edit WorkHistory'
    show_columns = ['id', 'individual', 'resume']
#    show_exclude_columns = [] #= ['id', 'individual', 'resume']
#
#    add_columns = ['id', 'individual', 'resume']
#    add_exclude_columns = [hide_list] #['id', 'individual', 'resume']
#
#    edit_columns = ['id', 'individual', 'resume']
#    edit_exclude_columns =[hide_list] # ['id', 'individual', 'resume']
#
#    list_columns = ['id', 'individual', 'resume']
#    list_exclude_columns = [] # ['id', 'individual', 'resume']
#
#    search_columns = ['id', 'individual', 'resume']
#    search_exclude_columns= [] # ['id', 'individual', 'resume']
#
#    default_sort = [('id', True)]
#    base_permissions = ['can_list', 'can_show', 'can_edit', 'can_delete', 'can_add']
#    label_columns=   [{column.name: column.name for column in table.columns} ]
#    show_template =  'appbuilder/general/model/show_cascade.html'
#    list_template = 'appbuilder/general/model/list.html'
#    add_template = 'appbuilder/general/model/add.html'
#    edit_template = 'appbuilder/general/model/edit.html'
#    add_widget = (FormVerticalWidget|FormInlineWidget)
#    show_widget = ShowBlockWidget
#    list_widget = (ListThumbnail|ListWidget)
#    base_order = ('name', 'asc')
#    list_widget= 'list_widget'


class WorkHistoryMultiView(MultipleView):
    datamodel=SQLAInterface(WorkHistory, db.session)
    views = []
    show_title='WorkHistory Detail'
    add_title ='Add WorkHistory'
    list_title= 'WorkHistory List'
    edit_title = 'Edit WorkHistory'
    show_columns = ['id', 'individual', 'resume']
#    show_exclude_columns = [] #= ['id', 'individual', 'resume']
#
#    add_columns = ['id', 'individual', 'resume']
#    add_exclude_columns = [hide_list] #['id', 'individual', 'resume']
#
#    edit_columns = ['id', 'individual', 'resume']
#    edit_exclude_columns =[hide_list] # ['id', 'individual', 'resume']
#
#    list_columns = ['id', 'individual', 'resume']
#    list_exclude_columns = [] # ['id', 'individual', 'resume']
#
#    search_columns = ['id', 'individual', 'resume']
#    search_exclude_columns= [] # ['id', 'individual', 'resume']
#
#    default_sort = [('id', True)]
#    base_permissions = ['can_list', 'can_show', 'can_edit', 'can_delete', 'can_add']
#    label_columns=   [{column.name: column.name for column in table.columns} ]
#    show_template =  'appbuilder/general/model/show_cascade.html'
#    list_template = 'appbuilder/general/model/list.html'
#    add_template = 'appbuilder/general/model/add.html'
#    edit_template = 'appbuilder/general/model/edit.html'
#    add_widget = (FormVerticalWidget|FormInlineWidget)
#    show_widget = ShowBlockWidget
#    list_widget = (ListThumbnail|ListWidget)
#    base_order = ('name', 'asc')
#    list_widget= 'list_widget'


# REGVIEWS
appbuilder.add_view_no_menu(IndustryDetailView, 'IndustryDetailView')
appbuilder.add_view_no_menu(ProfilesourceDetailView, 'ProfilesourceDetailView')
appbuilder.add_view_no_menu(PortalDetailView, 'PortalDetailView')
appbuilder.add_view_no_menu(JobSkillDetailView, 'JobSkillDetailView')
appbuilder.add_view_no_menu(UserxDetailView, 'UserxDetailView')
appbuilder.add_view_no_menu(SkillDetailView, 'SkillDetailView')
appbuilder.add_view_no_menu(IndividualDetailView, 'IndividualDetailView')
appbuilder.add_view_no_menu(SwarmDetailView, 'SwarmDetailView')
appbuilder.add_view_no_menu(IndustryJobDetailView, 'IndustryJobDetailView')
appbuilder.add_view_no_menu(PageDetailView, 'PageDetailView')
appbuilder.add_view_no_menu(IndividualSwarmDetailView, 'IndividualSwarmDetailView')
appbuilder.add_view_no_menu(ProfileDetailView, 'ProfileDetailView')
appbuilder.add_view_no_menu(JobDetailView, 'JobDetailView')
appbuilder.add_view_no_menu(ResumeDetailView, 'ResumeDetailView')
appbuilder.add_view_no_menu(LocationDetailView, 'LocationDetailView')
appbuilder.add_view(IndividualMasterView, 'IndividualMasterView', category='Overview')
appbuilder.add_view(JobSkillMultiView, 'JobSkillMultiView', category='Overview')
appbuilder.add_view(WorkHistoryMasterView, 'WorkHistoryMasterView', category='Overview')
appbuilder.add_view(IndividualJobMultiView, 'IndividualJobMultiView', category='Overview')
appbuilder.add_view(PortalMasterView, 'PortalMasterView', category='Overview')
appbuilder.add_view(SwarmMasterView, 'SwarmMasterView', category='Overview')
appbuilder.add_view(PageMasterView, 'PageMasterView', category='Overview')
appbuilder.add_view(IndividualSwarmMultiView, 'IndividualSwarmMultiView', category='Overview')
appbuilder.add_view(IndustryJobMasterView, 'IndustryJobMasterView', category='Overview')
appbuilder.add_view(LocationMasterView, 'LocationMasterView', category='Overview')
appbuilder.add_view(IndustryJobMultiView, 'IndustryJobMultiView', category='Overview')
appbuilder.add_view(EducationMasterView, 'EducationMasterView', category='Overview')
appbuilder.add_view(IndividualJobMasterView, 'IndividualJobMasterView', category='Overview')
appbuilder.add_view(IndividualSwarmMasterView, 'IndividualSwarmMasterView', category='Overview')
appbuilder.add_view(WorkHistoryMultiView, 'WorkHistoryMultiView', category='Overview')
appbuilder.add_view(UserSkillMasterView, 'UserSkillMasterView', category='Overview')
appbuilder.add_view(ProfileMultiView, 'ProfileMultiView', category='Overview')
appbuilder.add_view(JobSkillMasterView, 'JobSkillMasterView', category='Overview')
appbuilder.add_view(UserSkillMultiView, 'UserSkillMultiView', category='Overview')
appbuilder.add_view(ResumeMultiView, 'ResumeMultiView', category='Overview')
appbuilder.add_view(ResumeMasterView, 'ResumeMasterView', category='Overview')
appbuilder.add_view(ProfileMasterView, 'ProfileMasterView', category='Overview')
appbuilder.add_view(UserxView, 'UserxView', category='Setup')
appbuilder.add_view(ProfilesourceView, 'ProfilesourceView', category='Setup')
appbuilder.add_view(WorkHistoryView, 'WorkHistoryView', category='Setup')
appbuilder.add_view(IndustryJobView, 'IndustryJobView', category='Setup')
appbuilder.add_view(LocationView, 'LocationView', category='Setup')
appbuilder.add_view(ProfileView, 'ProfileView', category='Setup')
appbuilder.add_view(IndividualView, 'IndividualView', category='Setup')
appbuilder.add_view(PortalView, 'PortalView', category='Setup')
appbuilder.add_view(EducationView, 'EducationView', category='Setup')
appbuilder.add_view(IndividualJobView, 'IndividualJobView', category='Setup')
appbuilder.add_view(IndividualSwarmView, 'IndividualSwarmView', category='Setup')
appbuilder.add_view(IndustryView, 'IndustryView', category='Setup')
appbuilder.add_view(SkillView, 'SkillView', category='Setup')
appbuilder.add_view(JobView, 'JobView', category='Setup')
appbuilder.add_view(SwarmView, 'SwarmView', category='Setup')
appbuilder.add_view(JobSkillView, 'JobSkillView', category='Setup')
appbuilder.add_view(ResumeView, 'ResumeView', category='Setup')
appbuilder.add_view(PageView, 'PageView', category='Setup')
appbuilder.add_view(UserSkillView, 'UserSkillView', category='Setup')

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
