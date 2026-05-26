from flask import Flask
from flask_appbuilder import AppBuilder, SQLA
from sqlalchemy import Column, Integer, String, JSON, ForeignKey, inspect, Boolean, Text
from flask_appbuilder import AppBuilder, SQLA
from sqlalchemy import create_engine, MetaData, Table, ForeignKey
# from sqlalchemy.schema import Inspector
# from sqlalchemy.orm import class_mapper
from utils import snake_to_camel, camel_to_pascal, pascal_to_snake, snake_to_pascal



mem_app = Flask(__name__)
mem_app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///:memory:"
mem_db = SQLA(mem_app)

intro_app = Flask(__name__)
# intro_app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://user:password@localhost/db'
intro_app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://nyimbi@localhost/plat'
intro_app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
intro_db = SQLA(intro_app)


# Define your models
class AppModel(mem_db.Model):
    __tablename__ = 'app_model'
    id = Column(Integer, primary_key=True)
    table_name = Column(String(255))
    model_name = Column(String(255))
    table_schema = Column(String(255))
    table_comment = Column(String(255))
    columns = Column(Text)
    column_list = Column(String)
    pk_column_list = Column(String)
    fk_column_list = Column(String)
    pk_column_count = Column(Integer)
    fk_column_count = Column(Integer)

class AppColumn(mem_db.Model):
    __tablename__ = 'app_column'
    id = Column(Integer, primary_key=True)
    model_id = Column(Integer, ForeignKey('app_model.id'))
    table_name = Column(String(255))
    column_name = Column(String(255))
    column_comment = Column(String(255))
    data_type = Column(String(50), nullable=False)
    hint = Column(String(255))
    description = Column(String(255))
    check_constraints = Column(String(255))
    default = Column(String(255))
    server_default = Column(String(255))
    length = Column(Integer)
    precision = Column(Integer)
    scale = Column(Integer)
    nullable = Column(Boolean)
    computed = Column(Boolean)
    sql_text = Column(String(255))
    dialect_options = Column(String(255))
    persisted = Column(Boolean, default=True)
    auto_increment = Column(Boolean)
    primary_key = Column(Boolean)
    unique = Column(Boolean)
    is_foreign_key = Column(Boolean, nullable=False)
    fk_dict = Column(String)
    fk_tables = Column(String(255))
    fk_columns = Column(String(255))

class AppRelations(mem_db.Model):
    __tablename__ = 'app_relation'
    id = Column(Integer, primary_key=True)
    table_name = Column(String(255), nullable=False)
    comment = Column(String(255))
    model_id = Column(Integer, ForeignKey('app_model.id'))
    parent_model_id = Column(Integer, ForeignKey('app_model.id'))
    referred_table_id = Column(Integer, ForeignKey('app_model.id'))
    referred_table = Column(String(255), nullable=False)
    referred_columns = Column(String(255), nullable=False)
    constrained_columns = Column(String(255), nullable=False)
    referred_columns_count = Column(Integer, default=1)
    constrained_columns_count = Column(Integer, default=1)
    ondelete = Column(String(50))
    onupdate = Column(String(50))


# Create the tables in the in-memory database
mem_db.create_all()

# Inspect the PostgreSQL database and populate the in-memory tables
# Define the SQLAlchemy engine and inspector
intro_engine = create_engine('postgresql://nyimbi@localhost/plat')
inspector = inspect(intro_engine)
metadata = MetaData()

with intro_engine.connect() as conn:
    for table_name in inspector.get_table_names():
        table = Table(table_name, metadata, autoload=True, autoload_with=intro_engine)
        table_comment = inspector.get_table_comment(table_name)
        schema = inspector.default_schema_name
        # column_names = inspector.get_columns(table_name)
        # foreign_keys = inspector.get_foreign_keys(table_name)
        # model_name = table.name.capitalize()
        model_name = snake_to_pascal(table_name)
        col_lst = []
        pk_lst = []
        fk_lst = []
        for column in table.columns:
            col_lst.append({"name":column.name, "type": str(column.type)})
            if column.primary_key:
                pk_lst.append(column.name)
            if column.foreign_keys:
                fk_lst.append(column.name)

        # Populate AppModel
        app_model = AppModel(
            table_name=table.name,
            model_name = model_name,
            table_schema = schema,
            table_comment = table.comment,
            columns = str(table.columns),
            column_list = str(col_lst),
            pk_column_list = str(pk_lst),
            fk_column_list = str(fk_lst),
            fk_column_count = len(fk_lst),
            pk_column_count = len(pk_lst)
        )
        mem_db.session.add(app_model)
        mem_db.session.commit()


        # Populate AppColumns
        is_foreign_key = False
        fk_col_lst = []
        fk_tbls = []
        fk_cols = []
        for column in table.columns:
            if column.foreign_keys:
                is_foreign_key = True
                fk_col_lst = []
                fk_tbls = []
                fk_cols = []
                for fk in column.foreign_keys:
                    fk_tbls.append(fk.column.table.name) # the referred table
                    fk_cols.append(fk.column.name) # the referred column
                    fk_col_lst.append({
                                    'table':fk.column.table.name,
                                    'column': fk.column.name,
                                    'ondelete': fk.ondelete,
                                    'onupdate' : fk.onupdate,
                                    'cardinality':  '1:1' if column.unique and not column.nullable else '1:N'
                                      })
            if column.computed:
                persisted = column.type.computed.persisted
                sql_text = column.type.computed.sql_text
            else:
                persisted = True
                sql_text =''

            app_column = AppColumn(
                table_name = table_name,
                column_name = column.name,
                data_type = str(column.type),
                column_comment = column.comment,
                description = " ",
                check_constraints = ', '.join(column.constraints),
                default = column.default,
                # server_default = column.server_default,
                length = column.type.length if hasattr(column.type, 'length') else None,
                precision = column.type.precision if hasattr(column.type, 'precision') else None,
                scale = column.type.scale if hasattr(column.type, 'scale') else None,
                nullable = column.nullable,
                computed = column.type.computed if hasattr(column.type, 'computed') else False,
                dialect_options='dialect', #str(column.dialect_options),
                auto_increment = column.autoincrement,
                primary_key = column.primary_key,
                unique = column.unique,
                is_foreign_key = is_foreign_key,
                fk_dict = str(fk_col_lst),
                fk_tables = str(fk_tbls),
                fk_columns = str(fk_cols),
            )

            mem_db.session.add(app_column)
            mem_db.session.commit()


        # Populate AppRelations
        for for_key in inspector.get_foreign_keys(table.name):
            referred_table = for_key['referred_table']
            referred_columns = for_key['referred_columns']
            constrained_columns = for_key['constrained_columns']
            foreign_keys = [
                {'column': for_key['constrained_columns'][i], 'referred_column': for_key['referred_columns'][i]}
                for i in range(len(for_key['constrained_columns']))
                ]
            comment = for_key['options'].get('comment')
            ondelete = for_key['options'].get('ondelete')
            onupdate = for_key['options'].get('onupdate')

            app_relation = AppRelations(
                table_name=table_name,
                referred_table=fk.column.table.name,
                referred_columns=fk.column.name,
                constrained_columns=str(constrained_columns),
                ondelete=ondelete,
                onupdate=onupdate
            )
            mem_db.session.add(app_relation)
            mem_db.session.commit()

        print(table.name, ' Desc: ', table.description, ' cols:' ,len(table.columns), ' PKs: ',len(table.primary_key.columns),' FKs:  ', len(table.foreign_keys))


# mem_db.session.commit()

# Use the Flask-AppBuilder to manage the application
appbuilder = AppBuilder(mem_app, mem_db.session)
