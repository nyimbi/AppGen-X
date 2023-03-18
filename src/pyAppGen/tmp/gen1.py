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

# # Generate Python code for all the tables
# def gen_models(metadata):
#     Base = declarative_base()
#     model_code = ''
#     model_code += MODEL_HEADER
#
#     for table_name, table in metadata.tables.items():
#         table_code = f"""
#     class {snake_to_pascal(table_name)}(Model, AuditMixin):
#         __tablename__ = '{table_name}'  """ + "\n\n"
#         # TODO Spacing of 2+ columns
#         column_code = ''
#         for column in table.columns:
#             column_code = "{} = Column({}".format(column.name, pg_to_fabtypes(str(column.type)))
#             if column.foreign_keys:
#                 column_code += f", ForeignKey('{list(column.foreign_keys)[0].column.table.name}.{list(column.foreign_keys)[0].column.name}')"
#             if column.primary_key:
#                 column_code += ", primary_key=True"
#             column_code += ")\n"
#             column_code = '        ' + column_code
#             table_code += column_code
#         print(table_code)
#         model_code += table_code
#     model_code += MODEL_FOOTER
#     return(model_code)


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
        # print(table_code)
        model_code += table_code
    model_code += MODEL_FOOTER
    return(model_code)



# def gen_simple_view(metadata):
#     Base = declarative_base()
#     views_code = ""
#     for table_name, table in metadata.tables.items():
#         # Check if the table has a primary key
#         primary_key = None
#         for constraint in table.constraints:
#             if isinstance(constraint, PrimaryKeyConstraint):
#                 primary_key = constraint.columns.keys()
#                 break
#         # Define a primary key if none is present
#         if not primary_key:
#             primary_key = [column.name for column in table.columns]
#             table.append_constraint(PrimaryKeyConstraint(*primary_key))
#         class_name = f"{snake_to_pascal(table_name)}View"
#         table_class = type(table_name, (Base,), {'__tablename__': table_name, '__table__': table})
#         view_class_attributes = {
#             "datamodel": f"SQLAInterface({table_name}, db.session)",
#             "related_views": [],
#             "edit_columns": [column.name for column in table.columns],
#             "list_columns": [column.name for column in table.columns],
#             "add_columns": [column.name for column in table.columns],
#             "show_columns": [column.name for column in table.columns],
#             "search_columns": [column.name for column in table.columns]
#         }
#         view_class = type(class_name, (ModelView,), view_class_attributes)
#         globals()[class_name] = view_class
#         views_code += f"class {snake_to_pascal(view_class.__name__)}({view_class.__bases__[0].__name__}):\n"
#         for key, value in view_class_attributes.items():
#             if key != 'related_views':
#                 views_code += f"    {key} = {value}\n"
#         if view_class_attributes['related_views']:
#             views_code += f"    related_views = {view_class_attributes['related_views']}\n"
#         views_code += "\n"
#
#     return views_code


def gen_simple_view(metadata):
    global generated_views
    Base = declarative_base()
    views_code = ""
    for table_name, table in metadata.tables.items():
        if table_name.startswith('ab_') or table_name.endswith('join'):
            continue
        # Check if the table has a primary key
        primary_key = None
        for constraint in table.constraints:
            if isinstance(constraint, PrimaryKeyConstraint):
                primary_key = constraint.columns.keys()
                break
        # Define a primary key if none is present
        if not primary_key:
            primary_key = [column.name for column in table.columns]
            table.append_constraint(PrimaryKeyConstraint(*primary_key))
        class_name = f"{snake_to_pascal(table_name)}View"
        generated_views.add(class_name)
        table_class = type(table_name, (Base,), {'__tablename__': table_name, '__table__': table})
        # Define the view_class_attributes with default values
        view_class_attributes = {
            "datamodel": f"SQLAInterface({snake_to_pascal(table_name)}, db.session)",
            "related_views": [],
            "base_permissions": ['can_list', 'can_show', 'can_edit', 'can_delete', 'can_add'],
            "search_exclude_columns": [],
            "search_columns": [column.name for column in table.columns],
            "default_sort": [('id', True)],
            "list_title": f"'{snake_to_pascal(table_name)} List'",
            "show_title": f"'{snake_to_pascal(table_name)} Detail'",
            "add_title": f"'Add {snake_to_pascal(table_name)}'",
            "edit_title": f"'Edit {snake_to_pascal(table_name)}'",
            "label_columns": {column.name: column.name for column in table.columns},
            "list_columns": [column.name for column in table.columns],
            "add_columns": [column.name for column in table.columns],
            "edit_columns": [column.name for column in table.columns],
            "show_columns": [column.name for column in table.columns],
            "description_columns": {column.name: '' for column in table.columns},
            "description_columns_editable": {column.name: False for column in table.columns},
            "show_fieldsets": [(f"{table_name.capitalize()} Details", {'fields': [column.name for column in table.columns]})],
            "edit_fieldsets": [(f"Edit {table_name.capitalize()}", {'fields': [column.name for column in table.columns]})],
            "add_fieldsets": [(f"Add {table_name.capitalize()}", {'fields': [column.name for column in table.columns]})],
            "show_template": f"'appbuilder/general/model/show_cascade.html'",
            "list_template": f"'appbuilder/general/model/list.html'",
            "add_template": f"'appbuilder/general/model/add.html'",
            "edit_template": f"'appbuilder/general/model/edit.html'",
            # "list_widget": list_widget,
            # "show_widget": show_widget,
            # "add_widget": add_widget,
            # "edit_widget": edit_widget,
        }
        view_class = type(class_name, (ModelView,), view_class_attributes)
        globals()[class_name] = view_class
        # views_code += f"class {snake_to_pascal(view_class.__name__)}({view_class.__bases__[0].__name__}):\n"
        views_code += f"class {class_name}({view_class.__bases__[0].__name__}):\n"
        for key, value in view_class_attributes.items():
            if key != 'related_views':
                views_code += f"    {key} = {value}\n"
        if view_class_attributes['related_views']:
            views_code += f"    related_views = {view_class_attributes['related_views']}\n"
        views_code += "\n"

    return views_code


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

#
# def gen_masterdetail_views(metadata):
#     Base = declarative_base()
#     # Define the Flask-AppBuilder views for each foreign key
#     views_code = []
#     for table_name, table in metadata.tables.items():
#         class_name = f"{snake_to_pascal(table_name)}View"
#         table_class = type(table_name, (Base,), {'__tablename__': table_name, '__table__': table})
#         if not class_mapper(table_class, False).primary_mapper:
#             mapper(table_class, table)
#         view_class_attributes = {
#             "datamodel": f'SQLAInterface({table_name})',
#             "related_views": [],
#             "edit_columns": [column.name for column in table.columns],
#             "list_columns": [column.name for column in table.columns],
#             "add_columns": [column.name for column in table.columns],
#             "show_columns": [column.name for column in table.columns],
#             "search_columns": [column.name for column in table.columns]
#         }
#
#         # Define the MasterDetailView for each ForeignKey
#         for column in table.columns:
#             if column.foreign_keys:
#                 referred_table_name = list(column.foreign_keys)[0].column.table.name
#                 referred_table_class_name = f"{snake_to_pascal(referred_table_name)}DetailView"
#                 referred_table_class = globals().get(referred_table_class_name, None)
#                 if referred_table_class:
#                     master_detail_view_class_name = f"{snake_to_pascal(class_name)}{snake_to_pascal(referred_table_name)}MasterView"
#                     master_detail_view_class_attributes = {
#                         "datamodel": f'SQLAInterface({table_name})',
#                         "related_views": f'[{referred_table_class}]',
#                         "list_columns": [column.name for column in table.columns],
#                         "show_columns": [column.name for column in table.columns],
#                         "search_columns": [column.name for column in table.columns],
#                         "default_view": "list"
#                     }
#                     master_detail_view_class = type(master_detail_view_class_name, (MasterDetailView,),
#                                                     master_detail_view_class_attributes)
#                     globals()[master_detail_view_class_name] = master_detail_view_class
#                     view_class_attributes['related_views'].append(master_detail_view_class)
#
#         view_class = type(class_name, (ModelView,), view_class_attributes)
#         globals()[class_name] = view_class
#         views_code.append(f"class {snake_to_pascal(view_class.__name__)}({view_class.__bases__[0].__name__}):")
#         for key, value in view_class_attributes.items():
#             if key != 'related_views':
#                 views_code.append(f"    {key} = {value}")
#         if view_class_attributes['related_views']:
#             views_code.append(f"    related_views = {view_class_attributes['related_views']}")
#         views_code.append("")
#
#     return "\n".join(views_code)



def gen_masterdetail_views(metadata):
    global generated_views
    Base = declarative_base()
    # Define the Flask-AppBuilder views for each foreign key
    views_code = []
    for table_name, table in metadata.tables.items():
        if table_name.startswith('ab_') or table_name.endswith('join'):
            continue
        class_name = f"{snake_to_pascal(table_name)}View"
        table_class = type(table_name, (Base,), {'__tablename__': table_name, '__table__': table})
        if not class_mapper(table_class, False).primary_mapper:
            mapper(table_class, table)
        view_class_attributes = {
            "datamodel": f'SQLAInterface({snake_to_pascal(table_name)})',
            "related_views": [],
            "edit_columns": [column.name for column in table.columns],
            "list_columns": [column.name for column in table.columns],
            "add_columns": [column.name for column in table.columns],
            "show_columns": [column.name for column in table.columns],
            "search_columns": [column.name for column in table.columns]
        }

        # Define the MasterDetailView for each ForeignKey
        for column in table.columns:
            if column.foreign_keys:
                referred_table_name = list(column.foreign_keys)[0].column.table.name
                referred_table_class_name = f"{snake_to_pascal(referred_table_name)}DetailView"
                referred_table_class = globals().get(referred_table_class_name, None)
                if referred_table_class:
                    master_detail_view_class_name = f"{snake_to_pascal(class_name)}{snake_to_pascal(referred_table_name)}MasterView"
                    if master_detail_view_class_name not in generated_views:
                        generated_views.add(master_detail_view_class_name)
                        master_detail_view_class_attributes = {
                            "datamodel": f'SQLAInterface({snake_to_pascal(table_name)})',
                            "related_views": f'[{referred_table_class}]',
                            "list_columns": [column.name for column in table.columns],
                            "show_columns": [column.name for column in table.columns],
                            "search_columns": [column.name for column in table.columns],
                            "default_view": "list"
                        }
                        master_detail_view_class = type(master_detail_view_class_name, (MasterDetailView,),
                                                        master_detail_view_class_attributes)
                        globals()[master_detail_view_class_name] = master_detail_view_class
                        views_code.append(
                            f"class {snake_to_pascal(master_detail_view_class.__name__)}({master_detail_view_class.__bases__[0].__name__}):")
                        for key, value in master_detail_view_class_attributes.items():
                            if key != 'related_views':
                                views_code.append(f"    {key} = {value}")
                        if master_detail_view_class_attributes['related_views']:
                            views_code.append(
                                f"    related_views = {master_detail_view_class_attributes['related_views']}")
                        views_code.append("")
                    view_class_attributes['related_views'].append(globals().get(master_detail_view_class_name))

        view_class = type(class_name, (ModelView,), view_class_attributes)
        if class_name not in generated_views:
            generated_views.add(class_name)
            globals()[class_name] = view_class
            views_code.append(f"class {snake_to_pascal(view_class.__name__)}({view_class.__bases__[0].__name__}):")
            for key, value in view_class_attributes.items():
                if key != 'related_views':
                    views_code.append(f"    {key} = {value}")
            if view_class_attributes['related_views']:
                views_code.append(f"    related_views = {view_class_attributes['related_views']}")
            views_code.append("")

    return "\n".join(views_code)



def gen_multi_view(metadata):
    Base = declarative_base()
    # Define the Flask-AppBuilder MultipleView for tables with more than one ForeignKey
    multiple_views_code = []
    for table_name, table in metadata.tables.items():
        if table_name.startswith('ab_') or table_name.endswith('join'):
            continue
        foreign_keys = []
        for column in table.columns:
            if column.foreign_keys:
                foreign_keys.append(column)

        if len(foreign_keys) > 1:
            table_class = type(table_name, (Base,), {'__tablename__': table_name, '__table__': table})
            if not class_mapper(table_class, False).primary_mapper:
                mapper(table_class, table)
            multiple_view_class_name = f"{snake_to_pascal(table_name)}MultiView"
            multiple_view_class_attributes = {
                "datamodel": f'SQLAInterface({snake_to_pascal(table_name)})',
                "base_filters": [],
                "search_columns": [column.name for column in table.columns]
            }
            related_views = []
            for column in foreign_keys:
                referred_table_name = list(column.foreign_keys)[0].column.table.name
                referred_table_class_name = f"{referred_table_name}View"
                referred_table_class = globals().get(referred_table_class_name, None)
                if referred_table_class:
                    related_views.append(referred_table_class)
            multiple_view_class_attributes['related_views'] = related_views
            multiple_view_class = type(multiple_view_class_name, (MultipleView,), multiple_view_class_attributes)
            globals()[multiple_view_class_name] = multiple_view_class
            multiple_views_code.append(
                f"class {multiple_view_class.__name__}({multiple_view_class.__bases__[0].__name__}):")
            for key, value in multiple_view_class_attributes.items():
                if key != 'related_views':
                    multiple_views_code.append(f"    {key} = {value}")
            if related_views:
                multiple_views_code.append(f"    related_views = {related_views}")
            multiple_views_code.append("")

    return "\n".join(multiple_views_code)

def gen_views(metadata):
    vcode =''
    vcode += VIEW_HEADER

    vcode += gen_simple_view(metadata)
    vcode += gen_masterdetail_views(metadata)
    vcode += gen_multi_view(metadata)
    vcode += gen_register_views(metadata)

    vcode += VIEW_FOOTER
    # print(vcode)
    return vcode

def gen_register_views(metadata):
    code = ""
    for table_name, table in metadata.tables.items():
        if (table_name.startswith('ab_') or table_name.endswith('join')):
            continue
        class_name = f"{snake_to_pascal(table_name)}View"
        code += f"appbuilder.add_view({class_name}(), '{table_name}', icon='fa-folder-open-o', category='Tables')\n"
        for column in table.columns:
            if column.foreign_keys:
                referred_table_name = list(column.foreign_keys)[0].column.table.name
                if (referred_table_name.startswith('ab_') or referred_table_name.endswith('join')):
                    continue
                referred_table_class_name = f"{snake_to_pascal(referred_table_name)}View"
                referred_table_class = globals().get(referred_table_class_name, None)
                if referred_table_class:
                    master_detail_view_class_name = f"{snake_to_pascal(class_name)}{snake_to_pascal(referred_table_name)}View"
                    code += f"appbuilder.add_view({master_detail_view_class_name}(), '{table_name}', icon='fa-folder-open-o', category='MasterDetail', category_icon='fa-envelope')\n"

                if referred_table_name != table_name:
                    code += f"appbuilder.add_related_view({class_name}(), {referred_table_class_name}, '{table_name}', '{column.name}', icon='{referred_table_name}')\n"
                else:
                    code += f"appbuilder.add_link('{table_name} {column.name}', icon='{referred_table_name}', href='/view/{table_name}/{{id}}/{column.name}')\n"
    return code






def gen_views3(metadata):
    nonlocal generated_views_set, detail_views_set, master_views_set

    def gen_master_detail_views(table_name, table):
        nonlocal generated_views_set, detail_views_set, master_views_set
        code = []

        def gen_detail_view(table_name, referred_table):
            s = ''
            class_name = f"{snake_to_pascal(table_name)}{snake_to_pascal(referred_table.name)}DetailView"
            if class_name not in generated_views:
                generated_views_set.add(class_name)
                detail_views_set.add(class_name)
                s = f"class {class_name}('DetailView'):\n" +\
                                f"    datamodel = SQLAInterface({snake_to_pascal(referred_table.name)})\n" +\
                                f"    related_views = []\n" +\
                                f"    show_columns = {[column.name for column in referred_table.columns]}\n"+\
                                f"    list_columns = {[column.name for column in referred_table.columns]}\n" +\
                                f"    search_columns = {[column.name for column in referred_table.columns]}\n" +\
                                f"    default_view = 'show'\n" +\
                                f"    base_filters = [['id', FilterEqual, '$id']]\n" +\
                                f"    label_columns = {{{{column.name: column.name for column in referred_table.columns}}}}\n\n"

                return s

        def gen_master_view(table_name, table):
            nonlocal generated_views_set, detail_views_set, master_views_set
            s =''
            class_name = f"{snake_to_pascal(table_name)}MasterView"
            if class_name in generated_views_set:
                return s
            generated_views.add(class_name)
            master_views_set.add(class_name)
            s=  f"class {class_name}(MasterView):\n" +\
                        f"    datamodel = SQLAInterface({snake_to_pascal(table_name)})\n" +\
                        f"    related_views = [{', '.join([gen_detail_view(referred_table_name, table).__name__ for referred_table_name, column in table.foreign_keys])}]\n" +\
                        f"    list_columns = {[column.name for column in table.columns]}\n" +\
                        f"    show_columns = {[column.name for column in table.columns]}\n" +\
                        f"    search_columns = {[column.name for column in table.columns]}\n" +\
                        f"    default_view = 'list'\n\n"

        for column in table.columns:
            if column.foreign_keys:
                code.append(gen_master_view(table_name, table))
                code.append(gen_detail_view(column.column.table.name, column.column.table))
        return "\n".join(code)

    def gen_simple_view(table_name, table):
        nonlocal generated_views_set, detail_views_set, master_views_set
        code = []
        s = ''
        class_name = f"{snake_to_pascal(table_name)}View"
        if class_name not in generated_views_set:
            generated_views_set.add(class_name)
            s = f"class {class_name}(ModelView)" +\
                "    datamodel = SQLAInterface({table_name})" +\
                "    edit_columns = {[column.name for column in table.columns]}" +\
                "    list_columns = {[column.name for column in table.columns]}" +\
                "    add_columns = {[column.name for column in table.columns]}" +\
                "    show_columns = {[column.name for column in table.columns]}" +\
                "    search_columns = {[column.name for column in table.columns]}"

        return 'SIMPLEVIEW\n' + s

    def gen_master_view(table_name, table):
        nonlocal generated_views_set, detail_views_set, master_views_set
        code = []

        # Define the MasterDetailView for each ForeignKey
        for column in table.columns:
            if column.foreign_keys:
                referred_table_name = list(column.foreign_keys)[0].column.table.name
                if referred_table_name.startswith('ab_') or referred_table_name.endswith('join'):
                    continue
                referred_table_class_name = f"{snake_to_pascal(referred_table_name)}DetailView"
                detail_views_set.add(referred_table_class_name)
                # referred_table_class = globals().get(referred_table_class_name, None)
                if referred_table_class_name:
                    master_detail_view_class_name = f"{snake_to_pascal(table_name)}{snake_to_pascal(referred_table_name)}MasterView"
                    if master_detail_view_class_name not in generated_views_set:
                        generated_views_set.add(master_detail_view_class_name)
                        master_views_set.add(master_detail_view_class_name)
                        master_detail_view_class_attributes = {
                            "datamodel": f'SQLAInterface({snake_to_pascal(table_name)})',
                            "related_views": f'[{referred_table_class_name}]',
                            "list_columns": [column.name for column in table.columns],
                            "show_columns": [column.name for column in table.columns],
                            "search_columns": [column.name for column in table.columns],
                            "default_view": "list"
                        }
                        master_detail_view_class = type(master_detail_view_class_name, (MasterDetailView,),
                                                        master_detail_view_class_attributes)
                        # code.append("")
                        code.append(
                            f"class {snake_to_pascal(master_detail_view_class_name)}({master_detail_view_class.__bases__[0].__name__}):")
                        for key, value in master_detail_view_class_attributes.items():
                            if key != 'related_views':
                                code.append(f"    {key} = {value}")
                        if master_detail_view_class_attributes['related_views']:
                            detail_views_set.add("{master_detail_view_class_attributes['related_views']}")
                            code.append(
                                f"    related_views = {master_detail_view_class_attributes['related_views']}")

        s = "\n".join(code)
        # print(s)
        return 'MASTERVIEW\n' + s

    def gen_detail_view1(table_name, column):
        nonlocal generated_views_set, detail_views_set
        referred_table_name = list(column.foreign_keys)[0].column.table.name
        class_name = f"{snake_to_pascal(referred_table_name)}DetailView"

        if class_name in generated_views_set:
            return ""

        generated_views_set.add(class_name)
        detail_views_set.add(class_name)
        view_class_attributes = {
            "datamodel": f'SQLAInterface({referred_table_name})',
            "related_views": [],
            "show_columns": [column.name for column in column.table.columns],
            "search_columns": [column.name for column in column.table.columns]
        }

        for col in column.table.columns:
            if col.foreign_keys:
                referred_table_name = list(col.foreign_keys)[0].column.table.name
                referred_table_class_name = f"{snake_to_pascal(referred_table_name)}View"
                referred_table_class = globals().get(referred_table_class_name, None)

                if referred_table_class:
                    detail_views_set.add(referred_table_class_name)
                    view_class_attributes['related_views'].append(referred_table_class)

        view_class = type(class_name, (ModelView,), view_class_attributes)
        code = []
        code.append(f"class {snake_to_pascal(view_class.__name__)}({view_class.__bases__[0].__name__}):")
        for key, value in view_class_attributes.items():
            if key != 'related_views':
                code.append(f"    {key} = {value}")
        if view_class_attributes['related_views']:
            code.append(f"    related_views = {view_class_attributes['related_views']}")
        code.append("")
        s = "\n".join(code)
        # print(s)
        return s

    def gen_detail_view(table_name, column):
        nonlocal generated_views_set, detail_views_set, master_views_set
        class_name = f"{snake_to_pascal(table_name)}DetailView"
        view_class_attributes = {
            "datamodel": f'SQLAInterface({snake_to_pascal(table_name)})',
            "related_views": [],
            "show_columns": [column.name for column in column.column.table.columns],
            "search_columns": [column.name for column in column.column.table.columns]
        }

        # Define the related views for each ForeignKey
        referred_table_name = column.column.table.name
        referred_table_class_name = f"{snake_to_pascal(referred_table_name)}View"
        referred_table_class = globals().get(referred_table_class_name, None)

        if referred_table_class:
            if referred_table_class_name not in generated_views_set:
                generated_views_set.add(referred_table_class_name)
                detail_views_set[referred_table_class_name] = gen_detail_view(referred_table_name,
                                                                              column.column.table.columns[0])

            detail_views_set[referred_table_class_name] = gen_detail_view(referred_table_name,
                                                                          column.column.table.columns[0])
            view_class_attributes['related_views'].append(referred_table_class)

        view_class = type(class_name, (ModelView,), view_class_attributes)
        s = f"class {snake_to_pascal(view_class.__name__)}({view_class.__bases__[0].__name__}):" + "\n" + \
            f"    datamodel = SQLAInterface({snake_to_pascal(table_name)})" + "\n" + \
            f"    related_views = [{','.join([referred_table_class.__name__ for referred_table_class in view_class_attributes['related_views']])}]" + "\n" + \
            f"    show_columns = {[column.name for column in column.column.table.columns]}" + "\n" + \
            f"    search_columns = {[column.name for column in column.column.table.columns]}" + "\n\n"
        # print(s)
        return 'DETAILVIEW \n' +s



    def gen_multi_view(table_name, table):
        nonlocal generated_views_set, detail_views_set, master_views_set
        code = []
        related_views = []
        for column in table.columns:
            if column.foreign_keys:
                referred_table_name = list(column.foreign_keys)[0].column.table.name
                referred_table_class_name = f"{snake_to_pascal(referred_table_name)}View"
                referred_table_class = globals().get(referred_table_class_name, None)
                if not referred_table_class:
                    continue

                # Check if the detail view has been generated for the foreign key
                if referred_table_name not in detail_views_set:
                    detail_views_set[referred_table_name] = gen_detail_view(referred_table_name, column)

                # Add the detail view to the related_views list
                related_views.append(globals()[f"{snake_to_pascal(referred_table_name)}DetailView"])

        class_name = f"{snake_to_pascal(table_name)}MultiView"

        if class_name not in generated_views_set:
            generated_views_set.add(class_name)
            view_class_attributes = {
                "datamodel": f'SQLAInterface({table_name})',
                "related_views": related_views,
                "default_view": "list"
            }
            view_class = type(class_name, (MultipleView,), view_class_attributes)
            code.append(f"class {snake_to_pascal(view_class.__name__)}({view_class.__bases__[0].__name__}):")
            for key, value in view_class_attributes.items():
                if key != 'related_views':
                    code.append(f"    {key} = {value}")
            if view_class_attributes['related_views']:
                code.append(f"    related_views = {view_class_attributes['related_views']}")
            code.append("")
        s = "\n".join(code)
        return 'MULTIVIEW\n' +s

    def gen_view_registrations():
        nonlocal generated_views_set, detail_views_set, master_views_set
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
            if view_name not in detail_views_set and view_name not in master_views_set:
                code.append(f"appbuilder.add_view({view_name}, '{view_name.lower()}', category='Setup')")

        code.append("")
        s = "\n".join(code)
        # print(s)
        return 'REGVIEWS\n' +s

    views_code = []
    do_multi_view = False
    for table_name, table in metadata.tables.items():
        if table_name.startswith('ab_') or table_name.endswith('join'):
            continue

        detail_views_dict = {}
        # master_views_set = set()

        fkeys = []
        for column in table.columns:
            if column.foreign_keys:
                fkeys.append(column)
        if len(fkeys) > 1:
            do_multi_view = True

        # Generate views for the current table
        views_code.append(gen_simple_view(table_name, table))
        master_views_code = gen_master_view(table_name, table)
        if master_views_code:
            views_code.append(master_views_code)

        for column in table.columns:
            if column.foreign_keys:
                foreign_key = list(column.foreign_keys)[0]
                referred_table_name = foreign_key.column.table.name
                detail_views_dict[referred_table_name] = []
                if referred_table_name not in generated_views_set:
                    detail_views_code = gen_detail_view(table_name, foreign_key)
                    if detail_views_code:
                        detail_views_dict[referred_table_name].append(detail_views_code)

                    multi_views_code = gen_multi_view(table_name, table)
                    if multi_views_code:
                        master_views_set.add(
                            f"{snake_to_pascal(table_name)}{snake_to_pascal(referred_table_name)}MasterView")
                        # detail_views.setdefault(referred_table_name, [])
                        detail_views_dict[referred_table_name].append(multi_views_code)

            # Generate view registrations for the current table
            views_code.append(gen_view_registrations())

        # Append the generated detail views and master views
        for detail_view_name, detail_view_codes in detail_views.items():
            if detail_view_name in generated_views_set:
                continue
            generated_views_set.add(detail_view_name)
            views_code.append("\n".join(detail_view_codes))
            views_code.append(gen_view_registrations())

        for master_view_name in master_views_set:
            if master_view_name in generated_views_set:
                continue
            generated_views_set.add(master_view_name)
            views_code.append(master_view_name)
            views_code.append(gen_view_registrations())

        # Append the remaining generated views
    for view_name in generated_views_set:
        if view_name in detail_views_set or view_name in master_views_set:
            continue
        # views_code_set.append(view_name)
        views_code.append(gen_view_registrations())
    s = "\n".join(views_code)
    return s





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
    view_code = gen_views(metadata)
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
# @click.option("-db","--database", default="plat", help="The name of the database to introspect")
# @click.option("--dbengine", default="postgresql", help="The name of the database engine, defaults to postgresql")
def main(dir, filename):
    # First we create a connection string with the commandline parameters
    # conn_str = f'{dbengine}://{user}:{urllib.parse.quote_plus("pass")}@{host}:{port}/{database}'
    conn_str = f'postgresql:///plat'

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