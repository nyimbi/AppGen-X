#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#vi: set ai sta et ts=8 sts=4 sw=4 tw=79 wm=0 cc=+1 lbr fo=croq :
# Copyright (C) Nyimbi Odero,2023

""" This generates Views and Models for a flask builder app by


"""
import sqlalchemy
from sqlalchemy import Column
from sqlalchemy import ForeignKey
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import Table
from sqlalchemy.orm import Mapped
# from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship
from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy.ext.associationproxy import AssociationProxy
from sqlalchemy import create_engine, MetaData, Table, Column, Integer, ForeignKey, String
from sqlalchemy.orm import mapper, class_mapper
from sqlalchemy.schema import PrimaryKeyConstraint
from sqlalchemy.ext.declarative import declarative_base
from flask_appbuilder import Model
from flask_appbuilder import ModelView, MasterDetailView, MultipleView, ModelRestApi
from flask_appbuilder.models.sqla.interface import SQLAInterface
import graphene
from sqlalchemy.ext.automap import automap_base

import graphene
import click, shutil
import urllib.parse
# from graphene_sqlalchemy import SQLAlchemyObjectType

from utils import snake_to_pascal, pg_to_fabtypes
from headers import MODEL_HEADER, MODEL_FOOTER, MODEL_EXT, VIEW_HEADER, VIEW_FOOTER, API_HEADER

generated_views_set = set()
detail_views_set = set()
master_views_set = set()

def gen_models(metadata):
    Base = declarative_base()
    model_code = ''
    model_code += MODEL_HEADER

    for table_name, table in metadata.tables.items():
        if table_name.startswith('ab_') or table_name.endswith('join'):
            continue
        table_code = f"""
class {snake_to_pascal(table_name)}(Model, AuditMixin): # RefTypeMixin, TransientMixin, PlaceMixin, DocMixin, PersonMixin
    __tablename__ = '{table_name}'  """ + "\n\n"
        # TODO Spacing of 2+ columns
        column_code = ''
        for column in table.columns:
            column_code = "{} = Column({}".format(column.name, pg_to_fabtypes(str(column.type)))
            if column.foreign_keys:
                if len(column.foreign_keys) == 1:
                    column_code += f", ForeignKey('{list(column.foreign_keys)[0].column.table.name}.{list(column.foreign_keys)[0].column.name}')"
                elif len(column.foreign_keys) == 2:
                    assoc_table_name = f"{table_name}_{column.name}_join"
                    assoc_table = Table(assoc_table_name, metadata,
                                        Column(f"{table_name}_id", Integer, ForeignKey(f"{table_name}.id"), primary_key=True),
                                        Column(f"{column.foreign_keys[0].column.table.name}_id", Integer, ForeignKey(f"{column.foreign_keys[0].column.table.name}.id"), primary_key=True)
                                        )
                    assoc_name = f"{snake_to_pascal(table_name)}{snake_to_pascal(column.foreign_keys[0].column.table.name)}Association"
                    assoc_object = association_proxy(f"{column.name}_assoc", f"{column.foreign_keys[0].column.name}")
                    table_code += f"    {column.name}_assoc = relationship('{assoc_name}', back_populates='{column.name}_cols')\n"
                    table_code += f"    {column.name}_cols = association_proxy('{column.name}_assoc', '{column.foreign_keys[0].column.name}')\n"
                    assoc_code = f"""
    class {assoc_name}(Base):
        __tablename__ = '{assoc_table_name}'
        {table_name}_id = Column(Integer, ForeignKey(f'{table_name}.id'), primary_key=True)
        {column.foreign_keys[0].column.table.name}_id = Column(Integer, ForeignKey(f'{column.foreign_keys[0].column.table.name}.id'), primary_key=True)
        {column.foreign_keys[0].column.name} = relationship('{column.foreign_keys[0].column.table.name}')
        {table_name} = relationship('{table_name}')\n\n"""
                    model_code += assoc_code
            if column.primary_key:
                column_code += ", primary_key=True"
            column_code += ")\n"
            column_code = '    ' + column_code
            table_code += column_code
        table_code += MODEL_EXT
        model_code += table_code
    model_code += MODEL_FOOTER
    return(model_code)


def generate_field_sets(table_name, metadata):
    # Get the table object from the metadata
    table = metadata.tables[table_name]

    # Initialize empty field sets
    edit_fields = []
    show_fields = []
    list_fields = []
    add_fields = []

    # Loop over the columns in the table and add them to the field sets
    for column in table.columns:
        # Determine the appropriate field type based on the column type
        # You can customize this based on your own requirements
        field_type = 'TextField' if isinstance(column.type, String) else 'IntegerField'

        # Create a field object with the appropriate attributes
        field = {
            'name': column.name,
            'label': column.name.capitalize(),
            'type': field_type,
            'required': not column.nullable
        }

        # Add the field to the appropriate field set
        edit_fields.append(field)
        show_fields.append(field)
        list_fields.append(field)
        add_fields.append(field)

    # Return a dictionary of the field sets
    return {
        'edit': edit_fields,
        'show': show_fields,
        'list': list_fields,
        'add': add_fields
    }



def gen_views3(metadata):
    global generated_views_set, detail_views_set, master_views_set

    def gen_master_detail_views(table_name: object, table: object) -> object:
        global generated_views_set, detail_views_set, master_views_set
        if table_name.startswith('ab_') or table_name.endswith('join'):
            return ''

        # def gen_detail_view(table_name, referred_table):
        #     s = ''
        #     if table_name.startswith('ab_') or table_name.endswith('join'):
        #         return s
        #     # class_name = f"{snake_to_pascal(referred_table.name)}DetailView"
        #     class_name = f"{snake_to_pascal(table_name)}DetailView"
        #     if class_name not in generated_views_set:
        #         generated_views_set.add(class_name)
        #         detail_views_set.add(class_name)
        #         s = f"class {class_name}('DetailView'):\n" +\
        #                         f"    datamodel = SQLAInterface({snake_to_pascal(referred_table.name)})\n" +\
        #                         f"    show_columns = {[column.name for column in referred_table.columns]}\n"+\
        #                         f"    list_columns = {[column.name for column in referred_table.columns]}\n" +\
        #                         f"    search_columns = {[column.name for column in referred_table.columns]}\n" +\
        #                         f"    default_view = 'list'\n" +\
        #                         f"    base_filters = [['id', FilterEqual, '$id']]\n" +\
        #                         f"    label_columns = {{{{column.name: column.name for column in referred_table.columns}}}}\n\n"
        #
        #     return s

        def gen_master_view(table_name, table):
            global generated_views_set, detail_views_set, master_views_set
            s =''
            ref_tbls =set()
            suffix = 'MasterView'
            super_class = 'MasterDetailView'
            rel_name = 'related_views'

            if table_name.startswith('ab_') or table_name.endswith('join'):
                return ''
            fkeys = []
            for column in table.columns:
                if column.foreign_keys:
                    fkeys.append(column)
                    ref_tbls.add(list(column.foreign_keys)[0].column.table.name)
            fkey_count = len(fkeys)

            # Logic:
            # For every ref_tbl -> generate a DetailView
            # if len(fkeys) > 0 -> generate a masterView:
            # then if len(fkeys) > 1 generate a MultiView
            mview_count = 0
            dvc_lst =[]
            if fkey_count == 0:
                return s
            if fkey_count > 0:
                # Generate a MasterView & DetailView for every ref_tbl
                for detail_v in ref_tbls:
                    s += gen_simple_view(detail_v, table, suffix='DetailView')
                    dvc = f"{snake_to_pascal(table_name)}DetailView"
                    dvc_lst.append(dvc)
                    s += gen_simple_view(f"{table_name}{detail_v}", suffix='MasterView', mclass='MasterDetailView',rel_name='related_views',rel_list=dvc)
                if fkey_count > 1:
                    s += gen_simple_view(table_name, suffix='MultiView', mclass='MultipleView', rel_name='views', rel_list=", ".join(dvc_lst))










            class_name = f"{snake_to_pascal(table_name)}{suffix}"

            if class_name in generated_views_set:
                return s
            generated_views_set.add(class_name)
            master_views_set.add(class_name)


            # Now Generate the detail/ChildViews
            for column in table.columns:
                if column.foreign_keys:
                    referred_table_name = list(column.foreign_keys)[0].column.table.name
                    if referred_table_name.startswith('ab_') or referred_table_name.endswith('join'):
                        continue
                    referred_table_class_name = f"{snake_to_pascal(referred_table_name)}DetailView"
                    # referred_table_class_name = f"{snake_to_pascal(table_name)}{snake_to_pascal(referred_table_name)}DetailView"
                    ref_tbls.add(referred_table_class_name)
                    if referred_table_class_name not in generated_views_set:
                        generated_views_set.add(referred_table_class_name)
                        detail_views_set.add(referred_table_class_name)
                        s += gen_detail_view(referred_table_name, list(column.foreign_keys)[0].column.table)

            # Generate the MasterView/MultipleView
            s += f"class {class_name}({super_class}):\n" + \
                 f"    datamodel = SQLAInterface({snake_to_pascal(table_name)})\n" + \
                 f"    {rel_name} = [{', '.join(ref_tbls)}]\n" + \
                 f"    list_columns = {[column.name for column in table.columns]}\n" + \
                 f"    show_columns = {[column.name for column in table.columns]}\n" + \
                 f"    search_columns = {[column.name for column in table.columns]}\n" + \
                 f"    default_view = 'list'\n\n"

            return s
        s = gen_master_view(table_name, table)
        return '# MASTERVIEW\n' + s

    def gen_simple_view(table_name, table, mclass='ModelView', suffix ='View',rel_name='related_views', rel_list=''):
        global generated_views_set, detail_views_set, master_views_set
        code = []
        s = ''
        if table_name.startswith('ab_') or table_name.endswith('join'):
            return ''
        class_name = f"{snake_to_pascal(table_name)}{suffix}"
        if class_name not in generated_views_set:
            generated_views_set.add(class_name)
            s  = f"class {class_name}({mclass}):\n" +\
                f"    datamodel=SQLAInterface({snake_to_pascal(table_name)}, db.session)\n" +\
                f"    {rel_name} = [{rel_list}]\n" +\
                f"    base_permissions = ['can_list', 'can_show', 'can_edit', 'can_delete', 'can_add']\n" +\
                f"    search_exclude_columns= []\n" +\
                f"    search_columns = {[column.name for column in table.columns]}\n" +\
                f"    default_sort = [('id', True)]\n" +\
                f"    list_title= '{snake_to_pascal(table_name)} List'\n" +\
                f"    show_title='{snake_to_pascal(table_name)} Detail'\n" +\
                f"    add_title ='Add {snake_to_pascal(table_name)}'\n" +\
                f"    edit_title = 'Edit {snake_to_pascal(table_name)}'\n" +\
                f"#    label_columns=  [{{column.name: column.name}} for column in table.columns]\n" +\
                f"    list_columns = {[column.name for column in table.columns]}\n" +\
                f"    add_columns= {[column.name for column in table.columns]}\n" +\
                f"    edit_columns = {[column.name for column in table.columns]}\n" +\
                f"    show_columns = {[column.name for column in table.columns]}\n" +\
                f"#    description_columns = [{ {column.name: column.name} for column in table.columns}]\n" + \
                f"#    description_columns_editable = [{ {column.name: False} for column in table.columns}]\n" + \
                f"    show_template =  'appbuilder/general/model/show_cascade.html'\n" +\
                f"    list_template = 'appbuilder/general/model/list.html'\n" +\
                f"    add_template = 'appbuilder/general/model/add.html'\n" +\
                f"    edit_template = 'appbuilder/general/model/edit.html'\n" +\
                f"    list_widget= 'list_widget'\n" +\
                f"    show_widget = 'show_widget'\n" +\
                f"    add_widget = 'add_widget'\n" +\
                f"    edit_widget=  'edit_widget'\n\n\n"
                # f"    show_fieldsets= [('{{table_name.capitalize()}} Details', {'fields': [column.name for column in table.columns]})]\n" +\
                # f"    edit_fieldsets = [('Edit {table_name.capitalize()}', {'fields': [column.name for column in table.columns]})]\n" +\
                # f"    add_fieldsets = [('Add {table_name.capitalize()}', {'fields': [column.name for column in table.columns]})]\n" +\

        return s



    def gen_view_registrations():
        global generated_views_set, detail_views_set, master_views_set
        code = []

        # Register DetailViews first
        for detail_view_name in detail_views_set:
            code.append(f"appbuilder.add_view_no_menu({detail_view_name}, '{detail_view_name.lower()}')")

        # Register MasterViews
        for master_view_name in master_views_set:
            code.append(
                f"appbuilder.add_view({master_view_name}, '{master_view_name.lower()}', category='Overview')")

        # Register remaining views
        for view_name in generated_views_set:
            if (view_name not in detail_views_set) and (view_name not in master_views_set):
                code.append(f"appbuilder.add_view({view_name}, '{view_name.lower()}', category='Setup')")

        code.append("")
        s = "\n".join(code)
        return '# REGVIEWS\n' +s


## Generate all views
    views_code = ''
    views_code += VIEW_HEADER
    for table_name, table in metadata.tables.items():
        if table_name.startswith('ab_') or table_name.endswith('join'):
            continue
        views_code += gen_simple_view(table_name, table)
        views_code += gen_master_detail_views(table_name, table)


    views_code += gen_view_registrations()
    views_code +=  VIEW_FOOTER
    # print(views_code)
    return views_code





def gen_rest_code(metadata):
    Base = declarative_base()
    # Define the Flask-AppBuilder REST APIs for each SQLAlchemy model
    rest_code = []
    for table_name, table in metadata.tables.items():
        if table_name.startswith('ab_') or table_name.endswith('join'):
            continue
        class_name = f"{snake_to_pascal(table_name)}RestApi"
        table_class = type(table_name, (Base,), {'__tablename__': table_name, '__table__': table})
        if not class_mapper(table_class, False).primary_mapper:
            mapper(table_class, table)
        api_class_attributes = {
            "datamodel": f'SQLAInterface({snake_to_pascal(table_name)})',
            "include_columns": [column.name for column in table.columns],
            "exclude_columns": [],
            "allowed_filters": []
        }
        api_class = type(class_name, (ModelRestApi,), api_class_attributes)
        globals()[class_name] = api_class
        rest_code.append(f"class {api_class.__name__}({api_class.__bases__[0].__name__}):")
        for key, value in api_class_attributes.items():
            if value:
                rest_code.append(f"    {key} = {value}")
        rest_code.append("\n")
        rest_code.append(f'appbuilder.add_api({class_name})')
        rest_code.append("\n")
    full_code =API_HEADER
    full_code += "\n".join(rest_code)

    # print(full_code)
    return full_code




import graphene
# from graphene_sqlalchemy import SQLAlchemyObjectType
from sqlalchemy.orm import class_mapper
from sqlalchemy.ext.declarative import declarative_base


def gen_graphql_code(metadata):
    Base = declarative_base()

    # Define the GraphQL schema for each SQLAlchemy model
    graphql_code = []
    for table_name, table in metadata.tables.items():
        if table_name.startswith('ab_') or table_name.endswith('join'):
            continue
        class_name = f"{snake_to_pascal(table_name)}GraphQL"
        table_class = type(table_name, (Base,), {'__tablename__': table_name, '__table__': table})
        if not class_mapper(table_class, False).primary_mapper:
            mapper(table_class, table)
        graphql_fields = {}
        for column in table.columns:
            column_name = column.name
            column_type = column.type
            if isinstance(column_type, sqlalchemy.types.Integer):
                graphql_fields[column_name] = graphene.Int()
            elif isinstance(column_type, sqlalchemy.types.Float):
                graphql_fields[column_name] = graphene.Float()
            elif isinstance(column_type, sqlalchemy.types.String):
                graphql_fields[column_name] = graphene.String()
            elif isinstance(column_type, sqlalchemy.types.Boolean):
                graphql_fields[column_name] = graphene.Boolean()
            elif isinstance(column_type, sqlalchemy.types.DateTime):
                graphql_fields[column_name] = graphene.DateTime()
            elif isinstance(column_type, sqlalchemy.types.Date):
                graphql_fields[column_name] = graphene.Date()
            elif isinstance(column_type, sqlalchemy.types.Time):
                graphql_fields[column_name] = graphene.Time()
            else:
                graphql_fields[column_name] = graphene.String()

        graphql_object = type(f"{table_name}ObjectType", (graphene.ObjectType,), graphql_fields)
        graphql_object_name = f"{snake_to_pascal(table_name)}Object"
        globals()[graphql_object_name] = graphql_object
        graphql_code.append(f"class {snake_to_pascal(class_name)}(graphene.ObjectType):")
        graphql_code.append(f"    {table_name.lower()} = graphene.List({graphql_object_name})")
        graphql_code.append("")

    # Define the root query type for the GraphQL schema
    root_query_code = []
    root_query_code.append("class Query(graphene.ObjectType):")
    for table_name, table in metadata.tables.items():
        root_query_code.append(f"    {table_name.lower()} = graphene.List({table_name}Object)")
    root_query_code.append("")

    # Add resolvers to the GraphQL schema
    resolvers_code = []
    for table_name, table in metadata.tables.items():
        resolvers_code.append(f"    def resolve_{table_name.lower()}(self, info):")
        resolvers_code.append(f"        return {table_name}.query.all()")
        resolvers_code.append("")

    # Build the full GraphQL schema code
    full_code = "\n".join(graphql_code + root_query_code + resolvers_code)
    return full_code


def gen_code(metadata):
    # First we generate model code
    model_code = gen_models(metadata)
    view_code = gen_views3(metadata)
    graphql_code = gen_graphql_code(metadata)
    rest_code = gen_rest_code(metadata)

    ## Ideally we have taken the output directory from the command line





@click.command()
@click.option("-w", "--dir", default="./", help="your flask-appbuilder app directory to write the files to")
@click.option("-f", "--filename", default="myfile.txt", help="the name of the file to write")
# @click.option("-h", "--host", default="localhost", help="the database host IP address or name")
# @click.option("-p","--port", default=5432, help="The port on whihc the db server is listening")
# @click.option("-U","--user", default="", help="the database user name to connect to the server")
# @click.option("-pw","--pass", default="", help="password for the database server")
@click.option("-db","--database", default="plat", help="The name of the database to introspect")
# @click.option("--dbengine", default="postgresql", help="The name of the database engine, defaults to postgresql")
def main(dir, filename, database):
    # First we create a connection string with the commandline parameters
    # conn_str = f'{dbengine}://{user}:{urllib.parse.quote_plus("pass")}@{host}:{port}/{database}'
    conn_str = f'postgresql:///{database}'
    print(conn_str)
    print(f"{dir}")

    # Define the SQLAlchemy engine and metadata
    engine = create_engine(conn_str)
    metadata = MetaData(bind=engine)
    # Reflect the database schema
    metadata.reflect()

    model_code = gen_models(metadata)
    view_code = gen_views3(metadata)
    rest_code = gen_rest_code(metadata)
    graphql_code = gen_graphql_code(metadata)

    with open(f"{dir}/models.py", "w") as f:
        f.write(model_code)

    with open(f"{dir}/views.py", "w") as f:
        f.write(view_code)

    with open(f"{dir}/api.py", "w") as f:
        f.write(rest_code)

    with open(f"{dir}/gql.py", "w") as f:
        f.write(graphql_code)

    shutil.copyfile('mixins.py',f"{dir}/mixins.py" )
    shutil.copyfile('custom_types.py',f"{dir}/custom_types.py")

if __name__ == "__main__":
    main()