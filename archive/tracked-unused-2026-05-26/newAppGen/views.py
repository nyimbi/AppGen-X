
import calendar
from flask import redirect, flash, url_for, Markup
from flask import render_template
from flask_appbuilder.models.sqla.interface import SQLAInterface
from flask_appbuilder.views import ModelView, BaseView, MasterDetailView, MultipleView, RestCRUDView, CompactCRUDMixin
from flask_appbuilder import ModelView, CompactCRUDMixin, aggregate_count, action, expose, BaseView, has_access
from flask_appbuilder.charts.views import ChartView, TimeChartView, GroupByChartView
from flask_appbuilder.models.group import aggregate_count
from flask_appbuilder.widgets import ListThumbnail, ListWidget
from flask_appbuilder.widgets import FormVerticalWidget, FormInlineWidget, FormHorizontalWidget, ShowBlockWidget
from flask_appbuilder.models.sqla.filters import FilterStartsWith, FilterEqualFunction as FA

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


def fill_gender():
  try:
      db.session.add(Gender(name='Male'))
      db.session.add(Gender(name='Female'))
      db.session.commit()
  except:
      db.session.rollback()
#############


class IndustryView(ModelView):
    datamodel = SQLAInterface(Industry)
    list_columns = ['id, industry_code, job_id, task_id']
    add_columns = ['industry_code, job_id, task_id']
    show_columns = ['industry_code, job_id, task_id']

class JobView(ModelView):
    datamodel = SQLAInterface(Job)
    list_columns = ['id, name, company_profile, about_job, responsibilities, salary, equity, task_id']
    add_columns = ['name, company_profile, about_job, responsibilities, salary, equity, task_id']
    show_columns = ['name, company_profile, about_job, responsibilities, salary, equity, task_id']

class TaskView(ModelView):
    datamodel = SQLAInterface(Task)
    list_columns = ['id, task_name']
    add_columns = ['task_name']
    show_columns = ['task_name']

class IndustryJobMasterView(MasterDetailView):
    datamodel = SQLAInterface(Industry, Job)
    related_views = [JobView]
    add_columns = ["industry_code", "job_id", "task_id"]
    show_columns = ["industry_code", "job_id", "task_id"]
    edit_columns = ["industry_code", "job_id", "task_id"]
    add_title = 'Add Industry and Job'
    show_title = 'Show Industry and Job'
    edit_title = 'Edit Industry and Job'

    add_title = 'Add Job to Industry'
    show_title = 'Job in Industry'
    edit_title = 'Edit Job in Industry'

    add_title = 'Add Industry and Job'
    show_title = 'Show Industry and Job'
    edit_title = 'Edit Industry and Job'

class IndustryTaskMasterView(MasterDetailView):
    datamodel = SQLAInterface(Industry, Task)
    related_views = [TaskView]
    add_columns = ["industry_code", "job_id", "task_id"]
    show_columns = ["industry_code", "job_id", "task_id"]
    edit_columns = ["industry_code", "job_id", "task_id"]
    add_title = 'Add Industry and Task'
    show_title = 'Show Industry and Task'
    edit_title = 'Edit Industry and Task'

    add_title = 'Add Task to Industry'
    show_title = 'Task in Industry'
    edit_title = 'Edit Task in Industry'

    add_title = 'Add Industry and Task'
    show_title = 'Show Industry and Task'
    edit_title = 'Edit Industry and Task'

class JobTaskMasterView(MasterDetailView):
    datamodel = SQLAInterface(Job, Task)
    related_views = [TaskView]
    add_columns = ["name", "company_profile", "about_job", "responsibilities", "salary", "equity", "task_id"]
    show_columns = ["name", "company_profile", "about_job", "responsibilities", "salary", "equity", "task_id"]
    edit_columns = ["name", "company_profile", "about_job", "responsibilities", "salary", "equity", "task_id"]
    add_title = 'Add Job and Task'
    show_title = 'Show Job and Task'
    edit_title = 'Edit Job and Task'

    add_title = 'Add Task to Job'
    show_title = 'Task in Job'
    edit_title = 'Edit Task in Job'

    add_title = 'Add Job and Task'
    show_title = 'Show Job and Task'
    edit_title = 'Edit Job and Task'

appbuilder.add_view(eval(IndustryView), IndustryView, icon="fa-folder-open-o", category="Setup")
appbuilder.add_view(eval(JobView), JobView, icon="fa-folder-open-o", category="Setup")
appbuilder.add_view(eval(TaskView), TaskView, icon="fa-folder-open-o", category="Setup")
appbuilder.add_view(eval(IndustryJobMasterView), category="Master Detail Models")
appbuilder.add_view(eval(IndustryTaskMasterView), category="Master Detail Models")
appbuilder.add_view(eval(JobTaskMasterView), category="Master Detail Models")

appbuilder.add_link("rest_api", href="/swagger/v1", icon="fa-sliders", label="REST Api", category="Utilities")
appbuilder.add_link("graphql", href="/graphql", icon="fa-wrench", label="GraphQL", category="Utilities")

#appbuilder.add_separator("Setup")
#appbuilder.add_separator("My Views")
#appbuilder.add_link(name, href, icon='', label='', category='', category_icon='', category_label='', baseview=None)



