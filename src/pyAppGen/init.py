import logging

from flask import Flask
from flask_appbuilder import AppBuilder, SQLA

# from flask_graphql import GraphQLView
# from graphql_server.flask import GraphQLView
# from graphql import GraphQLSchema
# from graphene import Schema

from app.index import MyIndexView

# from .gql_schema import schema
"""
 Logging configuration
"""

logging.basicConfig(format="%(asctime)s:%(levelname)s:%(name)s:%(message)s")
logging.getLogger().setLevel(logging.DEBUG)

app = Flask(__name__)
app.config.from_object("config")
db = SQLA(app)
# appbuilder = AppBuilder(app, db.session)
appbuilder = AppBuilder(app, db.session, indexview=MyIndexView)


"""
from sqlalchemy.engine import Engine
from sqlalchemy import event

#Only include this for SQLLite constraints
@event.listens_for(Engine, "connect")
def set_sqlite_pragma(dbapi_connection, connection_record):
    # Will force sqllite contraint foreign keys
    cursor = dbapi_connection.cursor()
    cursor.execute("PRAGMA foreign_keys=ON")
    cursor.close()
"""

from . import models, views, api, openapi, workflow, rules, designer, view_composition, tabbed_views, form_designer, nl_evolution, dsl_reference, view_experience, support_center, low_code_features, prototyping, config_admin, integrations, productivity, lifecycle, emerging, tenancy, rls, identity, compliance, assistant, intelligence, chatbot, voice, agents, text_quality, notifications, platforms, microservices, collaboration, version_control, realtime, events, rpa, diagnostics, api_testing, components, erp_templates, project_management, devtools, studio, wizards, branding, extensions, reports, report_delivery, dashboards, usage_analytics, search, media, documents, inventory_ops, finance_ops, manufacturing_ops, data_access, data_exchange, database_ops, runtime_security, backup, monitoring, resilience, performance  # , gql_schema

from app.views import init_views
from app.security import seed_roles
from app.runtime_security import register_runtime_security, register_runtime_security_view
from app.openapi import register_openapi
from app.designer import register_designer
from app.view_composition import register_view_composition
from app.tabbed_views import register_tabbed_views
from app.form_designer import register_form_designer
from app.nl_evolution import register_nl_evolution
from app.dsl_reference import register_dsl_reference
from app.view_experience import register_view_experience
from app.support_center import register_support_center
from app.low_code_features import register_low_code_features
from app.prototyping import register_prototyping
from app.config_admin import register_config_admin
from app.integrations import register_integrations
from app.productivity import register_productivity
from app.lifecycle import register_lifecycle
from app.emerging import register_emerging
from app.tenancy import register_tenancy
from app.rls import register_rls
from app.identity import register_identity
from app.compliance import register_compliance
from app.assistant import register_assistant
from app.intelligence import register_intelligence
from app.chatbot import register_chatbot
from app.voice import register_voice
from app.agents import register_agents
from app.text_quality import register_text_quality
from app.notifications import register_notifications
from app.platforms import register_platforms
from app.microservices import register_microservices
from app.collaboration import register_collaboration
from app.version_control import register_version_control
from app.realtime import register_realtime
from app.events import register_events
from app.rpa import register_rpa
from app.diagnostics import register_diagnostics
from app.api_testing import register_api_testing
from app.components import register_components
from app.erp_templates import register_erp_templates
from app.project_management import register_project_management
from app.devtools import register_devtools
from app.studio import register_studio
from app.wizards import register_wizards
from app.branding import register_branding
from app.extensions import register_extensions
from app.reports import register_reports
from app.report_delivery import register_report_delivery
from app.dashboards import register_dashboards
from app.usage_analytics import register_usage_analytics
from app.search import register_search
from app.media import register_media
from app.documents import register_documents
from app.inventory_ops import register_inventory_ops
from app.finance_ops import register_finance_ops
from app.manufacturing_ops import register_manufacturing_ops
from app.data_access import register_data_access
from app.data_exchange import register_data_exchange
from app.database_ops import register_database_ops
from app.backup import register_backup
from app.workflow import register_workflows
from app.rules import register_rules
from app.monitoring import register_error_handlers, register_monitoring
from app.resilience import register_resilience
from app.performance import register_performance


# app.add_url_rule(
#     "/graphql", view_func=GraphQLView.as_view("graphql", graphql_schema=schema, graphiql=True))
#
#
# app.add_url_rule('/graphql', view_func=GraphQLView.as_view(
#     'graphql',
#     schema=schema,
#     graphiql=True,
# ))
# #
# # Optional, for adding batch query support (used in Apollo-Client)
# app.add_url_rule('/graphql/batch', view_func=GraphQLView.as_view(
#     'graphql',
#     schema=schema,
#     batch=True
# ))

init_views(appbuilder)  # Call init_views to register the views
register_error_handlers(app)
register_runtime_security(app)
register_runtime_security_view(appbuilder)
register_openapi(appbuilder)
register_designer(appbuilder)
register_view_composition(appbuilder)
register_tabbed_views(appbuilder)
register_form_designer(appbuilder)
register_nl_evolution(appbuilder)
register_dsl_reference(appbuilder)
register_view_experience(appbuilder)
register_support_center(appbuilder)
register_low_code_features(appbuilder)
register_prototyping(appbuilder)
register_config_admin(appbuilder)
register_integrations(appbuilder)
register_productivity(appbuilder)
register_lifecycle(appbuilder)
register_emerging(appbuilder)
register_tenancy(appbuilder)
register_rls(appbuilder)
register_identity(appbuilder)
register_compliance(appbuilder)
register_assistant(appbuilder)
register_intelligence(appbuilder)
register_chatbot(appbuilder)
register_voice(appbuilder)
register_agents(appbuilder)
register_text_quality(appbuilder)
register_notifications(appbuilder)
register_platforms(appbuilder)
register_microservices(appbuilder)
register_collaboration(appbuilder)
register_version_control(appbuilder)
register_realtime(appbuilder)
register_events(appbuilder)
register_rpa(appbuilder)
register_diagnostics(appbuilder)
register_api_testing(appbuilder)
register_components(appbuilder)
register_erp_templates(appbuilder)
register_project_management(appbuilder)
register_devtools(appbuilder)
register_studio(appbuilder)
register_wizards(appbuilder)
register_branding(appbuilder)
register_extensions(appbuilder)
register_monitoring(appbuilder)
register_resilience(appbuilder)
register_performance(appbuilder)
register_workflows(appbuilder)
register_rules(appbuilder)
register_reports(appbuilder)
register_report_delivery(appbuilder)
register_dashboards(appbuilder)
register_usage_analytics(appbuilder)
register_search(appbuilder)
register_media(appbuilder)
register_documents(appbuilder)
register_inventory_ops(appbuilder)
register_finance_ops(appbuilder)
register_manufacturing_ops(appbuilder)
register_data_access(appbuilder)
register_data_exchange(appbuilder)
register_database_ops(appbuilder)
register_backup(appbuilder)
seed_roles(appbuilder)
