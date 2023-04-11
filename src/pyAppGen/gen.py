#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#vi: set ai sta et ts=8 sts=4 sw=4 tw=79 wm=0 cc=+1 lbr fo=croq :
# Copyright (C) Nyimbi Odero,2023

"""A one line summary of the gen1

"""

import os, sys, shutil, click, glob
from flask import flash
from sqlalchemy import create_engine, inspect, MetaData, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.schema import ForeignKeyConstraint
from sqlalchemy import create_engine, inspect, MetaData
from inflection import underscore, camelize
from utils import *
from headers import  *
from model_mixins import *
from view_mixins import *
from datetime import datetime

# Global Variable
metadata =''
Base = ''
engine = ''


def generate_view_code():
    global metadata, engine
    output = []

    def generate_chart_view_code():
        global metadata, engine
        s = f"{[(table.name, snake_to_label(table.name)) for table in metadata.tables.values()]}"
        print(s)
        return CHART_VIEW_BODY.format(tbls=s)

    def get_foreign_keys(table):
        return [fk for fk in table.foreign_keys]

    def generate_view(table_name, table):
        class_name = snake_to_pascal(table_name)
        snk_table_name = snake_to_pascal(table_name)
        tbl_columns = [column_name for column_name in table.columns.keys() if column_name != 'id']
        rt_cols = str(RefTypeMixin.mixin_fields())
        rt_fld_set = str(RefTypeMixin.mixin_fieldset())
        lbl_cols = f"{{" + ', '.join([f'"{column.name}": "{column.name}"' for column in table.columns if not column.name.startswith('id') ]) + "}"
        output.append(VIEW_BODY.format(
                                   class_name = class_name,
                                   snk_table_name = snk_table_name,
                                   tbl_columns = tbl_columns,
                                   rt_cols = rt_cols,
                                   rt_fld_set = rt_fld_set,
                                   lbl_cols = lbl_cols))

    def generate_master_detail_view(table_name, table, foreign_key):
        related_table_name = foreign_key.column.table.name
        related_class_name = snake_to_pascal(related_table_name)
        class_name = snake_to_pascal(table_name)
        output.append(VIEW_MASTER_DETAIL.format(
            related_table_name  = related_table_name,
            related_class_name = related_class_name,
            class_name = class_name
        ))


    def generate_multiple_view(table_name, table):
        class_name = snake_to_pascal(table_name)
        output.append(f"class {class_name}MultipleModelView(MultipleView):")
        output.append(
            f"    views = [{class_name}ModelView, " + ', '.join(
                [f"{class_name}{snake_to_pascal(related_class)}ModelView" for related_class in related_classes]) + "]"
        )
        output.append("\n")

    for table_name, table in metadata.tables.items():
        foreign_keys = get_foreign_keys(table)
        generate_view(table_name, table)

        if len(foreign_keys) == 1:
            generate_master_detail_view(
                table_name, table, foreign_keys[0]
            )
        elif len(foreign_keys) > 1:
            related_classes = [
                fk.column.table.name for fk in foreign_keys
            ]
            for fk in foreign_keys:
                generate_master_detail_view(table_name, table, fk)

            generate_multiple_view(table_name, table)

    # Now append chart form code
    output.append(generate_chart_view_code())
    output.append("\n")
    output.append(VIEW_SCHEMA_CODE)

    # Now register the views generated
    output.append("def init_views(appbuilder):")
    for table_name, table in metadata.tables.items():
        class_name = snake_to_pascal(table_name)
        view_name = f"{class_name}ModelView"
        output.append(f"    appbuilder.add_view({view_name}, '{class_name}', icon='fa-table', category='Tables')")

        foreign_keys = get_foreign_keys(table)
        if len(foreign_keys) == 1:
            related_class_name = snake_to_pascal(foreign_keys[0].column.table.name)
            view_name = f"{class_name}{related_class_name}ModelView"
            output.append(
                f"    appbuilder.add_view({view_name}, '{class_name} {related_class_name} Master Detail', icon='fa-table', category='Master Detail')")

        elif len(foreign_keys) > 1:
            view_name = f"{class_name}MultipleModelView"
            output.append(
                f"    appbuilder.add_view({view_name}, '{class_name} Multiple', icon='fa-table', category='Multiple')")

    output.append("    appbuilder.add_separator('Tables')")
    output.append("    appbuilder.add_view(ChartView, 'Draw Chart', icon='fa-bar-chart', category='Charts')")
    output.append('    appbuilder.add_view(SchemaView, "Schema View", category="Database")')


    return "\n".join(output)


def generate_model_code():
    output = []

    def get_foreign_keys(table):
        return [fk for fk in table.foreign_keys]

    def is_association_table(table):
        foreign_keys = [c for c in table.columns if c.foreign_keys]
        return len(foreign_keys) == 2 and all([fk.primary_key for fk in foreign_keys])

    def get_relationship_type(table, column):
        for constraint in table.constraints:
            if isinstance(constraint, ForeignKeyConstraint) and column.name in constraint.columns.keys():
                foreign_table = constraint.elements[0].column.table
                if is_association_table(table):
                    return "Many-to-Many", foreign_table.name
                return (
                    "One-to-Many" if foreign_table != table else "One-to-One",
                    foreign_table.name,
                )
        return None, None

    def render_column(column):
        column_type = column.type.compile(engine.dialect)
        fab_column_type = map_pgsql_datatypes(column_type.lower())
        fk, remote_table = get_relationship_type(column.table, column)

        if fk == "One-to-Many":
            return f"Column({fab_column_type}, ForeignKey('{remote_table}.id'), nullable={column.nullable})", f"{remote_table}"
        elif fk == "One-to-One":
            return f"Column({fab_column_type}, ForeignKey('{remote_table}.id'), nullable={column.nullable}, unique=True)", f"{remote_table}"
        elif fk == "Many-to-Many":
            return f"Column({fab_column_type}, ForeignKey('{remote_table}.id'), primary_key=True, nullable={column.nullable})", f"{remote_table}"
        elif column.primary_key:
            return f"Column({fab_column_type}, primary_key=True, nullable={column.nullable}, autoincrement=True)", None
        else:
            return f"Column({fab_column_type}, nullable={column.nullable})", None

    for table_name, table in metadata.tables.items():
        class_name = snake_to_pascal(table_name)

        output.append(f"class {class_name}(RefTypeMixin, Model):  # RefTypeMixin, TransientMixin, PlaceMixin, DocMixin, PersonMixin")
        output.append(f"    __tablename__ = '{table_name}'")

        primary_key_exists = any(column.primary_key for column in table.columns)
        if not primary_key_exists:
            print(table_name, 'NO PRIMARY KEY')
            output.append("    id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)")

        for column in table.columns:
            column_name = underscore(column.name)
            column_def, col_type = render_column(column)
            if col_type is not None:
                column_name = col_type
            output.append(f"    {column_name} = {column_def}")

        m2m_relationships = [
            fk for fk in table.foreign_keys if fk.column.table != table
        ]

        if len(m2m_relationships) == 2:
            related_table = m2m_relationships[1].column.table.name
            related_class = snake_to_pascal(related_table)
            output.append(
                f"    {related_class.lower()}_assoc = association_proxy('{snake_to_pascal(m2m_relationships[0].parent.name)}', '{related_class}')"
            )

        output.append("\n")

    return "\n".join(output)

def write_model_file(dir):
    model_code = generate_model_code()   # TODO change this to a template
    with open(f"{dir}/models.py", "w") as f:
        f.write("from sqlalchemy import (Column, Integer, String, ForeignKey, DateTime, Boolean, Float, Text, Date, Numeric, Interval, Enum)\n")
        f.write("from sqlalchemy.orm import relationship, backref\n")
        f.write("from sqlalchemy.ext.associationproxy import association_proxy\n")
        f.write("from flask_appbuilder import Model\n\n")
        f.write("from app.model_mixins import *\n")
        f.write("Base = Model\n\n")
        f.write(model_code)

def write_view_file(dir):
    view_code = generate_view_code() # TODO change this to a template
    with open(f"{dir}/views.py", "w") as f:
        f.write("import sys, os\n")
        f.write("from flask_appbuilder import (ModelView, MultipleView, MasterDetailView, SimpleFormView, BaseView, expose)\n")
        f.write("from flask_appbuilder.models.sqla.interface import SQLAInterface\n")
        f.write("from sqlalchemy import create_engine, inspect, MetaData, ForeignKeyConstraint\n")
        f.write("from wtforms import Form, SelectField, SubmitField\n")
        f.write("from wtforms.validators import DataRequired\n")
        f.write("from flask import current_app, flash\n")
        f.write("from app.models import *\n")
        f.write("from app.model_mixins import *\n")
        f.write("from app.view_mixins import *\n")
        f.write("from app import appbuilder\n")
        f.write("# For the chart drawing module\n")
        f.write("engine = create_engine(appbuilder.app.config['SQLALCHEMY_DATABASE_URI'])\n")
        f.write("metadata = MetaData(bind=engine)\n")
        f.write("metadata.reflect()\n\n\n")
        f.write(view_code)

def get_metadata(idb):
    global metadata, Base, engine

    engine = create_engine(idb)
    metadata = MetaData(bind=engine)
    metadata.reflect()
    Base = declarative_base()
    return metadata, Base, engine




@click.command()
@click.option("-w", "--writedir", default="./",help="your flask-appbuilder 'app' directory to write the files to",)
@click.option( "-i", "--idatabase", default="tt", help="The name of the database to introspect")
@click.option( "-c", "--wdatabase", default="plat", help="The name of the database to create")
def main(writedir, idatabase, wdatabase):
    # First we create a connection string with the commandline parameters
    # conn_str = f'{dbengine}://{user}:{urllib.parse.quote_plus("pass")}@{host}:{port}/{database}'idatabase
    idb = f"{idatabase}"
    wdb = f"{wdatabase}"
    print(idb, wdb)

    # Not cool, we are setting a global variable
    print(f"{writedir}")
    get_metadata(f"postgresql:///{idatabase}")
    write_model_file(f"{writedir}")
    write_view_file(f"{writedir}")
    shutil.copyfile("model_mixins.py", f"{writedir}/model_mixins.py")
    shutil.copyfile("view_mixins.py", f"{writedir}/view_mixins.py")
    shutil.copyfile("index.py", f"{writedir}/index.py")
    shutil.copyfile("utils.py", f"{writedir}/utils.py")
    shutil.copyfile("my_index.html", f"{writedir}/templates/my_index.html")
    shutil.copyfile("search_template.html", f"{writedir}/templates/search_template.html")
    shutil.copyfile("tabbed_edit.html", f"{writedir}/templates/tabbed_edit.html")
    shutil.copyfile("with_print_button.html", f"{writedir}/templates/with_print_button.html")
    shutil.copyfile("schema_view.html", f"{writedir}/templates/schema_view.html")
    shutil.copyfile("init.py", f"{writedir}/__init__.py")  # we are overwriting the init file

    # Create the destination directory if it doesn't exist
    tmplt_dir = f"{dir}/templates"
    if not os.path.exists(tmplt_dir):
        os.makedirs(tmplt_dir)
    # Iterate through all HTML files in the source directory
    for html_file in glob.glob(os.path.join('./', '*.html')):
        # Copy each HTML file to the destination directory
        shutil.copy2(html_file, tmplt_dir+'/')

    update_config_setting(f"{writedir}/../config.py", "SQLALCHEMY_DATABASE_URI", f"postgresql:///{wdb}")
    # update_config_setting(f"{writedir}/../config.py", "LANGUAGES", AFRICAN_LANGS)

    print('Generated at: ' + str(datetime.now()))

if __name__ == "__main__":
    main()





