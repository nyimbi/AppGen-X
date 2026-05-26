from sqlalchemy_utils import create_view
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.associationproxy import association_proxy

from utils import map_dbml_datatypes, snake_to_pascal
from headers import MODEL_HEADER, MODEL_FOOTER, MODEL_EXT


def gen_model_header(table_name):
    model_name = snake_to_pascal(table_name)
    return f'class {model_name}(Model):\n' \
           f'    __tablename__ = "{table_name}"\n\n'


def gen_model_columns(columns):
    res = ''
    for col_name, col_data in columns.items():
        col_type_str = map_dbml_datatypes(col_data['type'])
        res += f'    {col_name} = Column({col_type_str}'
        if col_data['nullable']:
            res += ', nullable=True'
        if col_data['unique']:
            res += ', unique=True'
        if col_data['primary_key']:
            res += ', primary_key=True'
        res += ')\n'
    return res + '\n'


# def gen_model_rels(table_name, relationships, tables):
#     res = ''
#     for relationship in relationships:
#         # if not relationship['bi_directional']:
#         #     continue
#         name = relationship['name']
#         col1 = relationship['col1']
#         table1 = relationship['table1']
#         col2 = relationship['col2']
#         table2 = relationship['table2']
#
#         ref_table = next(filter(lambda t: t['table_name'] == table2, tables), None)
#         if not ref_table:
#             continue
#
#         col2_type_str = map_dbml_datatypes(ref_table['columns'][col2]['type'])
#
#         if len(ref_table['relationships']) > 1:
#             relationship_name = f"{name}_{table1}"
#             ref_view_name = f"{table2.title().replace('_', '')}View"
#         else:
#             relationship_name = name
#             ref_view_name = f"{table2.title().replace('_', '')}MasterView"
#
#         if relationship['is_many']:
#             rel_type = 'relationship'
#             rel_args = f'"{table2}", back_populates="{relationship_name}", '
#         else:
#             rel_type = 'association_proxy'
#             rel_args = f'"{relationship_name}", "{table2}", ' \
#                        f'creator=lambda {table2}: {table_name}(**{table2})'
#
#         res += f'    {relationship_name} = {rel_type}(' \
#                f'{rel_args}' \
#                f'primaryjoin=foreign({table_name}.{col1}) == remote({table2}.{col2}), ' \
#                f'secondaryjoin=foreign({table2}.{col2}) == remote({table_name}.{col1}), ' \
#                f'viewonly=True)\n'
#
#         res += f'    {relationship_name}_list = association_proxy(' \
#                f'"{relationship_name}", "{col2}")\n'
#
#         res += f'    {table2} = relationship("{ref_view_name}", ' \
#                f'back_populates="{relationship_name}_list")\n\n'
#
#     return res
#
# def gen_model_rels(table_name, relationships, tables):
#     res = ''
#     for relationship in relationships:
#         if not relationship['bi_directional']:
#             continue
#         name = relationship['name']
#         col1 = relationship['col1']
#         table1 = relationship['table1']
#         col2 = relationship['col2']
#         table2 = relationship['table2']
#
#         ref_table = next(filter(lambda t: t['table_name'] == table2, tables), None)
#         # if not ref_table:
#         #     continue
#
#         if any(rel['table2'] == table2 for rel in relationships):
#             relationship_name = f"{name}_{table1}"
#         else:
#             relationship_name = name
#
#         if table_name != table2:
#             assoc_table = f"{table2}_{table_name}"
#         else:
#             assoc_table = f"{table_name}_{table2}"
#
#         if any(t['table_name'] == assoc_table for t in tables):
#             assoc_table_exists = True
#         else:
#             assoc_table_exists = False
#
#         if assoc_table_exists:
#             res += f'    {table2} = relationship("{table2.title().replace("_", "")}", '
#             res += f'secondary="{assoc_table}", primaryjoin="{table_name}.id == {assoc_table}.{table_name}_id", '
#             res += f'secondaryjoin="{table2}.id == {assoc_table}.{table2}_id", back_populates="{table_name}")\n'
#         else:
#             if relationship['is_many']:
#                 rel_type = 'relationship'
#                 rel_args = f'"{table2}", back_populates="{relationship_name}", '
#             else:
#                 rel_type = 'association_proxy'
#                 rel_args = f'"{relationship_name}", "{table2}", ' \
#                            f'creator=lambda {table2}: {table_name}(**{table2})'
#
#             res += f'    {relationship_name} = {rel_type}(' \
#                    f'{rel_args}' \
#                    f'primaryjoin=foreign({table_name}.{col1}) == remote({table2}.{col2}), ' \
#                    f'secondaryjoin=foreign({table2}.{col2}) == remote({table_name}.{col1}), ' \
#                    f'viewonly=True)\n'
#
#             res += f'    {relationship_name}_list = association_proxy(' \
#                    f'"{relationship_name}", "{col2}")\n'
#
#             res += f'    {table2} = relationship("{table2.title().replace("_", "")}", ' \
#                    f'back_populates="{relationship_name}_list")\n\n'
#
#     return res
#
# def gen_model_rels(table_name, relationships, tables):
#     res = ''
#     for relationship in relationships:
#         name = relationship['name']
#         col1 = relationship['col1']
#         table1 = relationship['table1']
#         col2 = relationship['col2']
#         table2 = relationship['table2']
#         bi_directional = relationship['bi_directional']
#
#         ref_table = next(filter(lambda t: t['table_name'] == table2, tables), None)
#         print(table_name, relationship, ref_table)
#         if not ref_table:
#             continue
#
#         col2_type_str = map_dbml_datatypes(ref_table['columns'][col2]['type'])
#
#         rel_type = ''
#         relationship_str = name
#         if bi_directional:
#             if table_name == table1:
#                 if table_name == table2:
#                     rel_type = 'relationship'
#                     relationship_str = '<-> ' + name
#                 else:
#                     rel_type = 'relationship'
#                     relationship_str = '<- ' + name
#             elif table_name == table2:
#                 if table_name == table1:
#                     rel_type = 'relationship'
#                     relationship_str = '<-> ' + name
#                 else:
#                     rel_type = 'relationship'
#                     relationship_str = '-> ' + name
#
#         if not rel_type:
#             if table_name == table1:
#                 if table_name == table2:
#                     rel_type = 'relationship'
#                     relationship_str = '- ' + name
#                 else:
#                     rel_type = 'relationship'
#                     relationship_str = '<- ' + name
#             elif table_name == table2:
#                 if table_name == table1:
#                     rel_type = 'relationship'
#                     relationship_str = '- ' + name
#                 else:
#                     rel_type = 'relationship'
#                     relationship_str = '-> ' + name
#
#         if relationship_str == name:
#             if relationship['is_many']:
#                 rel_args = f'"{table2}", back_populates="{name}"'
#                 if ref_table.get('is_association', False):
#                     rel_type = 'association_proxy'
#                     relationship_str = '<> ' + name
#                     rel_args = f'"{name}", "{table2}", ' \
#                                f'creator=lambda {table2}: {table_name}(**{table2})'
#
#                 else:
#                     rel_type = 'relationship'
#                     relationship_str = '<: ' + name
#             else:
#                 rel_type = 'relationship'
#                 relationship_str = '> ' + name
#                 rel_args = f'"{table2}", uselist=False, back_populates="{name}"'
#
#         res += f'    {relationship_str} = {rel_type}(' \
#                f'{rel_args}, ' \
#                f'primaryjoin=foreign({table_name}.{col1}) == remote({table2}.{col2}), ' \
#                f'secondaryjoin=foreign({table2}.{col2}) == remote({table_name}.{col1}), ' \
#                f'viewonly=True)\n\n'
#
#     return res

def gen_model_rels(table_name, relationships, tables):
    res = ''
    for relationship in relationships:
        name = relationship['name']
        col1 = relationship['col1']
        table1 = relationship['table1']
        col2 = relationship['col2']
        table2 = relationship['table2']

        ref_table = table2
        if not ref_table:
            continue

        col2_type_str = map_dbml_datatypes(ref_table['columns'][col2]['type'])

        relationship_type = get_relationship_type(name)

        if relationship_type == '<':
            res += f'    {table_name}.{col1}.reflected_foreign_keys.append(ForeignKey("{ref_table["table_name"]}.{col2}"))\n\n'
        elif relationship_type == '>':
            res += f'    {table_name}.{col1}.append_foreign_key(ForeignKey("{ref_table["table_name"]}.{col2}"))\n\n'
        elif relationship_type == ':':
            res += f'    {table_name}.{col1}.reflected_foreign_keys.append(ForeignKey("{ref_table["table_name"]}.{col2}"))\n\n'
            res += f'    {table_name}.{col1}.append_foreign_key(ForeignKey("{ref_table["table_name"]}.{col2}"))\n\n'

    return res


def gen_model_ext():
    return MODEL_EXT


def generate_models(tables):
    res = ''
    # res += MODEL_HEADER
    res += 'from flask_appbuilder import Model\n'
    res += 'from sqlalchemy import Column, Integer, String, ForeignKey\n\n'

    for table_data in tables:
        table_name = table_data['table_name']
        columns = table_data['columns']
        relationships = table_data['relationships']

        res += gen_model_header(table_name)
        res += gen_model_columns(columns)
        res += gen_model_rels(table_name, relationships, tables)
        # res += gen_model_ext()

    # res += MODEL_FOOTER
    return res
