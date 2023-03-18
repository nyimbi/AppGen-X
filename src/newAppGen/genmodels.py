from typing import List, Dict
from utils import snake_to_pascal
from headers import MODEL_HEADER, MODEL_FOOTER


def gen_model_header(table_name: str) -> str:
    model_name = snake_to_pascal(table_name)
    return f'''
class {model_name}(Model, AuditMixin): # RefTypeMixin, TransientMixin, DocMixin
     __tablename__ = "{table_name}"
'''

def gen_model_columns(table_name: str, columns: Dict[str, dict]) -> str:
    result = ""
    for column_name, column_info in columns.items():
        if column_info['is_foreign']:
            continue
        column_type = column_info['type']
        nullable = column_info['is_nullable']
        unique = column_info['is_unique']
        primary_key = column_info['is_primary_key']
        result += f"    {column_name} = Column({column_type}"
        if not nullable:
            result += ", nullable=False"
        if unique:
            result += ", unique=True"
        if primary_key:
            result += ", primary_key=True"
        result += ")\n"
    return result



def gen_model_rels(table_name: str, relationships: List[dict]) -> str:
    result = ""
    added_relationships = set()
    for relationship in relationships:
        name = relationship.get('name') or f'{relationship["table2"].name}_{relationship["col2"].name}'
        if name not in added_relationships:
            table2 = relationship['table2'].name
            col2 = relationship['col2'].name
            result += f"    {name} = Column(Integer, ForeignKey({table2}.id))\n"
            result += f"    fk_{name} = relationship({table2}, backref='{table_name}', lazy='dynamic')\n"
            added_relationships.add(name)
    return result



def generate_models(tables: List[dict]):
    model_code = ''
    model_code += MODEL_HEADER

    for table in tables:
        table_name = table['table_name']
        columns = table['columns']
        relationships = table['relationships']

        model_code += gen_model_header(table_name)
        model_code += gen_model_columns(table_name, columns)
        model_code += gen_model_rels(table_name, relationships)

    model_code += MODEL_FOOTER
    with open("models.py", "w") as f:
        f.write(model_code + '\n\n')

    return model_code