#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# vi: set ai sta et ts=8 sts=4 sw=4 tw=79 wm=0 cc=+1 lbr fo=croq :
# Copyright (C) Nyimbi Odero,2023

""" This generates Views and Models for a flask builder app by


"""
import os
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
from sqlalchemy import (
    create_engine,
    MetaData,
    Table,
    Column,
    Integer,
    ForeignKey,
    String,
)
from sqlalchemy.orm import mapper, class_mapper
from sqlalchemy.schema import PrimaryKeyConstraint
from sqlalchemy.ext.declarative import declarative_base
from flask_appbuilder import Model
from flask_appbuilder import ModelView, MasterDetailView, MultipleView, ModelRestApi
from flask_appbuilder.models.sqla.interface import SQLAInterface
import graphene
from sqlalchemy.ext.automap import automap_base
from sqlalchemy import (
    MetaData,
    Table,
    Column,
    Integer,
    String,
    ForeignKey,
    create_engine,
    and_,
)
from sqlalchemy.orm import relationship, backref
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql.schema import Index

import graphene
import click, shutil
import urllib.parse

# from graphene_sqlalchemy import SQLAlchemyObjectType

from utils import snake_to_pascal, pg_to_fabtypes
from headers import (
    MODEL_HEADER,
    MODEL_FOOTER,
    MODEL_EXT,
    VIEW_HEADER,
    VIEW_FOOTER,
    API_HEADER,
)

generated_views_set = set()
detail_views_set = set()
master_views_set = set()

Base = declarative_base()


def generate_models(metadata: MetaData) -> str:
    model_dict = {}

    def generate_columns(table: Table) -> dict:
        columns_dict = {}

        for column in table.columns:
            column_kwargs = {
                "nullable": column.nullable,
                "default": column.default,
                "server_default": column.server_default,
                "onupdate": column.onupdate,
            }

            column_comment = column.comment
            column_type = str(column.type)
            if column_type.startswith("VARCHAR"):
                column_length = column.type.length
                column_kwargs["max_length"] = column_length
            elif column_type.startswith("DECIMAL"):
                column_kwargs["precision"] = column.type.precision
                column_kwargs["scale"] = column.type.scale
            elif column_type.startswith("ENUM"):
                column_kwargs["choices"] = column.type.enums
            elif column_type.startswith("TIMESTAMP"):
                column_kwargs["timezone"] = True
            elif column_type.startswith("JSON"):
                column_kwargs["json_format"] = True

            columns_dict[column.name] = Column(
                column_type, **column_kwargs, doc=column_comment
            )

        return columns_dict

    def generate_model_class(table: Table, columns_dict: dict) -> type:
        table_comment = table.comment
        indexes = table.indexes

        model_name = table.name.capitalize()
        model_class = type(
            model_name,
            (Base,),
            {
                "__tablename__": table.name,
                "__table_args__": {"comment": table_comment},
                "id": Column(Integer, primary_key=True),
                **columns_dict,
            },
        )

        for index in indexes:
            index_columns = [column.name for column in index.columns]
            index_name = index.name
            unique = index.unique
            model_class.__table__.append_constraint(
                Index(index_name, *index_columns, unique=unique)
            )

        return model_class

    def generate_relationship(
        parent_table: Table, child_table: Table, foreign_key: ForeignKey
    ) -> None:
        parent_relationship_kwargs = {
            "uselist": False,
            "backref": backref(child_table.name, uselist=False),
            "lazy": "select",
        }
        child_relationship_kwargs = {
            "uselist": True,
            "backref": backref(parent_table.name, uselist=True),
            "lazy": "select",
        }

        if len(foreign_key.column.foreign_keys) == 1:
            parent_relationship_kwargs["cascade"] = "all, delete-orphan"
            parent_relationship_kwargs["single_parent"] = True
            child_relationship_kwargs["cascade"] = "all, delete"

            parent_relationship = relationship(
                child_table.name, **parent_relationship_kwargs
            )
            child_relationship = relationship(
                parent_table.name, **child_relationship_kwargs
            )

            setattr(parent_table, child_table.name, parent_relationship)
            setattr(child_table, parent_table.name, child_relationship)
        else:
            association_table_name = f"{parent_table.name}_{child_table.name}"
            association_table = Table(
                association_table_name,
                Base.metadata,
                Column(
                    f"{parent_table.name}_id", ForeignKey(f"{parent_table.name}.id")
                ),
                Column(f"{child_table.name}_id", ForeignKey(f"{child_table.name}.id")),
            )

            parent_relationship_kwargs["secondary"] = association_table
            child_relationship_kwargs["secondary"] = association_table

            parent_relationship = relationship(
                child_table.name, **parent_relationship_kwargs
            )
            child_relationship = relationship(
                parent_table.name, **child_relationship_kwargs
            )

            setattr(parent_table, child_table.name, parent_relationship)
            setattr(child_table, parent_table.name, child_relationship)

    # Generate the model classes for each table
    for table in metadata.tables.values():
        columns_dict = generate_columns(table)
        model_class = generate_model_class(table, columns_dict)
        model_dict[table.name] = model_class

    # Generate the relationships between tables
    for table_name, model_class in model_dict.items():
        table = metadata.tables[table_name]

        for foreign_key in table.foreign_keys:
            referred_table_name = foreign_key.column.table.name
            referred_table = metadata.tables[referred_table_name]

            if referred_table_name == table_name:
                continue

            if referred_table_name in model_dict:
                referred_model_class = model_dict[referred_table_name]
                generate_relationship(referred_table, model_class, foreign_key)
            else:
                # Handle self-referential foreign keys
                parent_column = referred_table.columns[foreign_key.column.name]
                child_column = table.columns[foreign_key.parent.name]
                parent_relationship = relationship(
                    model_class.__name__,
                    backref=backref(table_name, lazy="select"),
                    uselist=False,
                    remote_side=parent_column,
                    cascade="all, delete",
                    single_parent=True,
                )
                child_relationship = relationship(
                    model_class.__name__,
                    backref=backref(referred_table_name, lazy="select"),
                    uselist=True,
                    remote_side=child_column,
                    cascade="all, delete",
                )

                setattr(model_class, referred_table_name, child_relationship)
                setattr(referred_model_class, table_name, parent_relationship)

    # Generate the code for each model class
    model_code = ""
    for model_class in model_dict.values():
        model_code += f"class {model_class.__name__}Model(Base):\n"
        for column_name, column in model_class.__table__.columns.items():
            column_type = column.type.python_type.__name__
            column_kwargs = ", ".join(
                [f"{key}={value}" for key, value in column.info.items()]
            )
            model_code += (
                f"    {column_name} = Column({column_type}, {column_kwargs})\n"
            )
        model_code += "\n"

    return model_code


def gen_models(metadata):
    Base = declarative_base()
    model_code = ""
    model_code += MODEL_HEADER

    preamble = (
        """
class {}(Model, RefTypeMixin, AuditMixinNullable): # RefTypeMixin, TransientMixin, PlaceMixin, DocMixin, PersonMixin
    __tablename__ = '{}'  """
        + "\n\n"
    )

    for table_name, table in metadata.tables.items():
        if table.name.startswith("ab_") or table.name.endswith("join"):
            continue
        table_code = preamble.format(f"{snake_to_pascal(table_name)}", f"{table_name}")
        # TODO Spacing of 2+ columns
        column_code = ""
        first_pass = False  # TODO Need to clean this up, some error why it repeats for every column
        if not first_pass:
            first_pass = True
            for column in table.columns:
                if column.name.startswith("ab_"):
                    continue
                if column.primary_key:
                    column_code = (
                        "    "
                        + "{} = Column({} , primary_key=True)\n".format(
                            column.name, pg_to_fabtypes(str(column.type))
                        )
                    )
                elif column.foreign_keys:
                    column_code += (
                        "    "
                        + f"{list(column.foreign_keys)[0].column.table.name}_id  = Column({pg_to_fabtypes(str(column.type))},ForeignKey('{list(column.foreign_keys)[0].column.table.name}.id'))\n"
                    )
                    column_code += (
                        "    "
                        + f"{list(column.foreign_keys)[0].column.table.name}  = relationship('{snake_to_pascal(list(column.foreign_keys)[0].column.table.name)}')\n"
                    )  # , back_populates='{table_name}')\n"
                elif not (column.primary_key or column.foreign_keys):
                    column_code += "    " + "{} = Column({} )\n".format(
                        column.name, pg_to_fabtypes(str(column.type))
                    )
                else:
                    column_code = ""

            table_code += column_code
        table_code += MODEL_EXT
        model_code += table_code
    model_code += MODEL_FOOTER
    return model_code


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
        field_type = "TextField" if isinstance(column.type, String) else "IntegerField"

        # Create a field object with the appropriate attributes
        field = {
            "name": column.name,
            "label": column.name.capitalize(),
            "type": field_type,
            "required": not column.nullable,
        }

        # Add the field to the appropriate field set
        edit_fields.append(field)
        show_fields.append(field)
        list_fields.append(field)
        add_fields.append(field)

    # Return a dictionary of the field sets
    return {
        "edit": edit_fields,
        "show": show_fields,
        "list": list_fields,
        "add": add_fields,
    }


def gen_views(metadata: object) -> object:
    global generated_views_set, detail_views_set, master_views_set

    def gen_master_detail_views(table_name, table):
        # global generated_views_set, detail_views_set, master_views_set
        dv_str = ""
        mv_str = ""
        s = ""
        ref_tbls = set()

        if table_name.startswith("ab_") or table_name.endswith("join"):
            return ""
        fkeys = []
        for column in table.columns:
            if column.name.startswith("ab_"):
                continue
            if column.foreign_keys:
                fkeys.append(column)
                ref_tbls.add(list(column.foreign_keys)[0].column.table.name)
        fkey_count = len(fkeys)

        # Logic:
        # For every ref_tbl -> generate a DetailView
        # if len(fkeys) > 0 -> generate a masterView:
        # then if len(fkeys) > 1 generate a MultiView

        dvt_lst = set()
        if fkey_count == 0:
            return s
        if fkey_count > 0:
            # Generate all the DetailViews for every ref_tbl
            for d_tbl in ref_tbls:
                dvt_name = f"{snake_to_pascal(d_tbl)}DetailView"
                if dvt_name not in generated_views_set:
                    dv_str += gen_simple_view(d_tbl, table, suffix="DetailView")
                    generated_views_set.add(dvt_name)
                    detail_views_set.add(dvt_name)
                    dvt_lst.add(dvt_name)
                    print(table_name, d_tbl, dvt_name)

            #  For each DetailView we create a MasterView
            for dv in list(ref_tbls):
                mview_name = (
                    f"{snake_to_pascal(table_name)}{snake_to_pascal(dv)}MasterView"
                )
                dvt_name = f"{snake_to_pascal(dv)}DetailView"
                if mview_name not in generated_views_set:
                    mv_str += gen_simple_view(
                        table_name,
                        table,
                        cls_name=mview_name,
                        mclass="MasterDetailView",
                        rel_name="related_views",
                        rel_list=dvt_name,
                    )
                    generated_views_set.add(mview_name)
                    master_views_set.add(mview_name)

            if fkey_count > 1:
                mltv_name = f"{snake_to_pascal(table_name)}MultiView"
                if mltv_name not in generated_views_set:
                    mv_str += gen_simple_view(
                        table_name,
                        table,
                        suffix="MultiView",
                        mclass="MultipleView",
                        rel_name="views",
                        rel_list=", ".join(dvt_lst),
                    )
                    generated_views_set.add(mltv_name)
                    master_views_set.add(mltv_name)

        s = dv_str + mv_str
        return s

    def gen_simple_view(
        table_name,
        table,
        mclass="ModelView",
        suffix="View",
        rel_name="related_views",
        rel_list="",
        cls_name="",
    ):
        # global generated_views_set, detail_views_set, master_views_set
        code = []
        s = ""

        if table_name.startswith("ab_") or table_name.endswith("join"):
            return ""

        if len(cls_name) == 0:
            class_name = f"{snake_to_pascal(table_name)}{suffix}"
        else:
            class_name = cls_name

        # fld_list = f"{[column.name for column in table.columns]}"
        fld_list = ""
        # for column in table.columns:
        #     if column.foreign_keys:
        #         fld_list = f"['{list(column.foreign_keys)[0].column.table.name}'] +" + fld_list
        if class_name not in generated_views_set:
            generated_views_set.add(class_name)

            s += (
                f"class {class_name}({mclass}):\n"
                + f"    datamodel=SQLAInterface({snake_to_pascal(table_name)}, db.session)\n"
                + f"    {rel_name} = [{rel_list}]\n"
                + f"    show_title='{snake_to_pascal(table_name)} Detail'\n"
                + f"    add_title ='Add {snake_to_pascal(table_name)}'\n"
                + f"    list_title= '{snake_to_pascal(table_name)} List'\n"
                + f"    edit_title = 'Edit {snake_to_pascal(table_name)}'\n"
                + f"#    show_columns = {list(table.columns.keys())}\n"
                + f"    show_exclude_columns = hide_list #[] #= {list(table.columns.keys())}\n#\n"
                + f"#    add_columns = {list(table.columns.keys())}\n"
                + f"    add_exclude_columns = hide_list #{list(table.columns.keys())}\n#\n"
                + f"#    edit_columns = {list(table.columns.keys())}\n"
                + f"    edit_exclude_columns = hide_list # {list(table.columns.keys())}\n#\n"
                + f"#    list_columns = {list(table.columns.keys())}\n"
                + f"    list_exclude_columns = [] # {list(table.columns.keys())}\n#\n"
                + f"#    default_sort = [('id', True)]\n"
                + f"#    search_columns = {list(table.columns.keys())}\n"
                + f"#    search_exclude_columns = [] # {list(table.columns.keys())} \n#\n"
                + f"#    base_permissions = ['can_list', 'can_show', 'can_edit', 'can_delete', 'can_add']\n"
                + f"#    label_columns = {{" + ', '.join([f'{column.name}: "{column.name}"' for column in table.columns]) + "}}\n"
                # + f"#    label_columns=   [{{column.name: column.name for column in table.columns}} ]\n"
                + f"#    show_template =  'appbuilder/general/model/show_cascade.html'\n"
                + f"#    list_template = 'appbuilder/general/model/list.html'\n"
                + f"#    add_template = 'appbuilder/general/model/add.html'\n"
                + f"#    edit_template = 'appbuilder/general/model/edit.html'\n"
                + f"#    add_widget = (FormVerticalWidget|FormInlineWidget)\n"
                + f"#    show_widget = ShowBlockWidget\n"
                + f"#    list_widget = (ListThumbnail|ListWidget)\n"
                + f"#    base_order = ('name', 'asc')\n"
                + f"#    list_widget= 'list_widget'\n"
            )

            # f"#    label_columns=   [('{ {column.name}', '{column.name for column in table.columns}}]\n" + \
            # f"#    description_columns = [{ {column.name: column.name} for column in table.columns}]\n" + \
            # f"#    description_columns_editable = [{ {column.name: False} for column in table.columns}]\n" + \
            # f"#    show_fieldsets= [('{{table_name.capitalize()}} Details', {'fields': [column.name for column in table.columns]})]\n" + \
            # f"#    edit_fieldsets = [('Edit {table_name.capitalize()}', {'fields': [column.name for column in table.columns]})]\n" + \
            # f"#    add_fieldsets = [('Add {table_name.capitalize()}', {'fields': [column.name for column in table.columns]})]\n"

        return s + "\n\n"

    def gen_view_registrations():
        global generated_views_set, detail_views_set, master_views_set
        code = []

        # Register DetailViews first
        for detail_view_name in detail_views_set:
            code.append(
                f"appbuilder.add_view_no_menu({detail_view_name}, '{detail_view_name}')"
            )

        # Register MasterViews
        for master_view_name in master_views_set:
            code.append(
                f"appbuilder.add_view({master_view_name}, '{master_view_name}', category='Overview')"
            )

        # Register remaining views
        for view_name in generated_views_set:
            if (view_name not in detail_views_set) and (
                view_name not in master_views_set
            ):
                code.append(
                    f"appbuilder.add_view({view_name}, '{view_name}', category='Setup')"
                )

        code.append("")
        s = "\n".join(code)
        return "# REGVIEWS\n" + s

    ## Generate all views
    views_code = ""
    views_code += VIEW_HEADER
    for table_name, table in metadata.tables.items():
        if table_name.startswith("ab_") or table_name.endswith("join"):
            continue
        views_code += gen_simple_view(table_name, table)
        views_code += gen_master_detail_views(table_name, table)

    views_code += gen_view_registrations()
    views_code += VIEW_FOOTER
    return views_code


def gen_rest_code(metadata):
    Base = declarative_base()
    # Define the Flask-AppBuilder REST APIs for each SQLAlchemy model
    rest_code = []
    for table_name, table in metadata.tables.items():
        if table_name.startswith("ab_") or table_name.endswith("join"):
            continue
        class_name = f"{snake_to_pascal(table_name)}RestApi"
        table_class = type(
            table_name, (Base,), {"__tablename__": table_name, "__table__": table}
        )
        if not class_mapper(table_class, False).primary_mapper:
            mapper(table_class, table)
        api_class_attributes = {
            "datamodel": f"SQLAInterface({snake_to_pascal(table_name)})",
            "include_columns": [column.name for column in table.columns],
            "exclude_columns": [],
            "allowed_filters": [],
        }
        api_class = type(class_name, (ModelRestApi,), api_class_attributes)
        globals()[class_name] = api_class
        rest_code.append(
            f"class {api_class.__name__}({api_class.__bases__[0].__name__}):"
        )
        for key, value in api_class_attributes.items():
            if value:
                rest_code.append(f"    {key} = {value}")
        rest_code.append("\n")
        rest_code.append(f"appbuilder.add_api({class_name})")
        rest_code.append("\n")
    full_code = API_HEADER
    full_code += "\n".join(rest_code)

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
        if table_name.startswith("ab_") or table_name.endswith("join"):
            continue
        class_name = f"{snake_to_pascal(table_name)}GraphQL"
        table_class = type(
            table_name, (Base,), {"__tablename__": table_name, "__table__": table}
        )
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

        graphql_object = type(
            f"{table_name}ObjectType", (graphene.ObjectType,), graphql_fields
        )
        graphql_object_name = f"{snake_to_pascal(table_name)}Object"
        globals()[graphql_object_name] = graphql_object
        graphql_code.append(
            f"class {snake_to_pascal(class_name)}(graphene.ObjectType):"
        )
        graphql_code.append(
            f"    {table_name.lower()} = graphene.List({graphql_object_name})"
        )
        graphql_code.append("")

    # Define the root query type for the GraphQL schema
    root_query_code = []
    root_query_code.append("class Query(graphene.ObjectType):")
    for table_name, table in metadata.tables.items():
        root_query_code.append(
            f"    {table_name.lower()} = graphene.List({table_name}Object)"
        )
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


# @click.option("-h", "--host", default="localhost", help="the database host IP address or name")
# @click.option("-p","--port", default=5432, help="The port on whihc the db server is listening")
# @click.option("-U","--user", default="", help="the database user name to connect to the server")
# @click.option("-pw","--pass", default="", help="password for the database server")
# @click.option("--dbengine", default="postgresql", help="The name of the database engine, defaults to postgresql")


@click.command()
@click.option(
    "-w",
    "--dir",
    default="./",
    help="your flask-appbuilder 'app' directory to write the files to",
)
@click.option(
    "-f",
    "--filename",
    default="sql_file.sql",
    help="the name of the SQL file to import",
)
@click.option(
    "-s", "--sqlfile", default="sql_file.sql", help="the name of the SQL file to import"
)
@click.option(
    "-i", "--idatabase", default="tt", help="The name of the database to introspect"
)
@click.option(
    "-c", "--wdatabase", default="plat", help="The name of the database to create"
)
def main(dir, filename, idatabase, wdatabase, sqlfile):
    # First we create a connection string with the commandline parameters
    # conn_str = f'{dbengine}://{user}:{urllib.parse.quote_plus("pass")}@{host}:{port}/{database}'idatabase
    idb = f"{idatabase}"
    wdb = f"{wdatabase}"
    print(idb, wdb)

    # Copy to destination dir
    first_file = f"""
# Convert dbml to sql_file.sql?
dropdb {idb}
createdb {idb}
# Now we create the first version of the database
psql -d {idb} -a -f {sqlfile}
# Introspect this database {idb} and write the {idb}x
# Now we create the second version of the database after manually editing the models.py
# now we create database
dropdb {idb}x
createdb {idb}x
chmod +x first.sh third.sh
export SQLALCHEMY_DATABASE_URI='postgresql:///{idb}'
flask fab create-db
    """
    with open(f"{dir}/../first.sh", "w") as file:
        file.write(first_file)

    # write here near gen.py
    second_file = f"""
# Introspect this database {idb} and write the {idb}x
# Now we create the second version of the database after manually editing the models.py
# now we create database
chmod +x second.sh fourth.sh
dropdb {idb}x
createdb {idb}x
python3 gen.py -w {dir} -i {idb} -c {idb}x 
    """
    with open(f"second.sh", "w") as file:
        file.write(second_file)

    # Write locally
    third_file = f"""
####----
# Introspect this file and generate the final version of the database
export SQLALCHEMY_DATABASE_URI='postgresql:///{idb}x'
flask fab create-db
"""
    with open(f"{dir}/../third.sh", "w") as file:
        file.write(third_file)

    fourth_file = f"""
python3 gen.py -w {dir} -i {idb}x -c {wdb} 
"""
    with open(f"fourth.sh", "w") as file:
        file.write(fourth_file)

    fifth_file = f"""
# Finally we create the final db
dropdb {wdb}
createdb {wdb}
flask fab create-db
flask fab create-admin
flask run --host 0.0.0.0 --port 5000 --with-threads --reload
        """
    with open(f"{dir}/../fifth.sh", "w") as file:
        file.write(fifth_file)

    conn_str = f"postgresql:///{idatabase}"
    print(conn_str)
    print(f"{dir}")

    # Define the SQLAlchemy engine and metadata
    engine = create_engine(conn_str)
    metadata = MetaData(bind=engine)
    # Reflect the database schema
    metadata.reflect()

    model_code = gen_models(metadata)
    # model_code = generate_models(metadata)
    # print(model_code)
    view_code = gen_views(metadata)
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

    if os.path.isfile(f"sqlfile"):
        # Copy the file to the destination directory
        shutil.copyfile(f"sqlfile", f"{dir}/../{sqlfile}")
    shutil.copyfile("model_mixins.py", f"{dir}/mixins.py")
    shutil.copyfile("custom_types.py", f"{dir}/custom_types.py")
    shutil.copyfile("index.py", f"{dir}/index.py")
    shutil.copyfile("push_to_linode.sh", f"{dir}/../push_to_linode.sh")
    shutil.copyfile("my_index.html", f"{dir}/templates/my_index.html")
    shutil.copyfile("init.py", f"{dir}/__init__.py")  # we are overwriting the init file


if __name__ == "__main__":
    main()
