from typing import List, Dict, Any
from utils import snake_to_pascal

API_HD = """
from flask_restful import Resource
from flask_restful import Api

"""



def generate_api(tables: List[dict]) -> str:
    result = ''
    result += API_HD
    for table in tables:
        table_name = table['table_name']
        model_name = snake_to_pascal(table_name)
        api_name = f"{model_name}API"
        result += f"class {api_name}(Resource):\n"
        result += f"    def get(self):\n"
        result += f"        return {{'message': '{model_name} endpoint works'}}\n\n"
        result += "    def get(self, id):\n"
        result += f"        {model_name} = {model_name}.query.get(id)\n"
        result += "        if {model_name}:\n"
        result += "            return {model_name}.as_dict()\n"
        result += "        else:\n"
        result += "            return {'error': '{model_name} not found'}, 404\n"
        result += "\n"

        result += "    def put(self, id):\n"
        result += f"        {model_name} = {model_name}.query.get(id)\n"
        result += "        if {model_name}:\n"
        result += "            parser = reqparse.RequestParser()\n"
        for column_name, column_info in columns.items():
            if not column_info['primary_key']:
                result += f"            parser.add_argument('{column_name}', type={get_python_type(column_info['type'])})\n"
        result += "            args = parser.parse_args()\n"
        for column_name, column_info in columns.items():
            if not column_info['primary_key']:
                result += f"            {model_name}.{column_name} = args['{column_name}']\n"
        result += "            db.session.commit()\n"
        result += "            return {model_name}.as_dict(), 201\n"
        result += "        else:\n"
        result += "            return {'error': '{model_name} not found'}, 404\n"
        result += "\n"

        result += "    def post(self):\n"
        result += f"        parser = reqparse.RequestParser()\n"
        for column_name, column_info in columns.items():
            if not column_info['primary_key']:
                result += f"        parser.add_argument('{column_name}', type={get_python_type(column_info['type'])})\n"
        result += "        args = parser.parse_args()\n"
        result += f"        {model_name} = {model_name}("
        for column_name, column_info in columns.items():
            if not column_info['primary_key']:
                result += f"{column_name}=args['{column_name}'],"
        result = result[:-1]
        result += ")\n"
        result += "        db.session.add({model_name})\n"
        result += "        db.session.commit()\n"
        result += "        return {model_name}.as_dict(), 201\n"
    return result

def register_api(app, api: Api, tables: List[dict]):
    for table in tables:
        table_name = table['table_name']
        model_name = snake_to_pascal(table_name)
        api_name = f"{model_name}API"
        api.add_resource(eval(api_name), f'/{table_name}')


def generate_api(table_name: str, columns: Dict[str, Dict[str, Any]]):
    model_name = snake_to_pascal(table_name)
    resource_name = model_name + "Resource"

    result = f"class {resource_name}(Resource):\n"
    result += "    def get(self, id):\n"
    result += f"        {model_name} = {model_name}.query.get(id)\n"
    result += "        if {model_name}:\n"
    result += "            return {model_name}.as_dict()\n"
    result += "        else:\n"
    result += "            return {'error': '{model_name} not found'}, 404\n"
    result += "\n"

    result += "    def put(self, id):\n"
    result += f"        {model_name} = {model_name}.query.get(id)\n"
    result += "        if {model_name}:\n"
    result += "            parser = reqparse.RequestParser()\n"
    for column_name, column_info in columns.items():
        if not column_info['primary_key']:
            result += f"            parser.add_argument('{column_name}', type={column_info['type']})\n"
    result += "            args = parser.parse_args()\n"
    for column_name, column_info in columns.items():
        if not column_info['primary_key']:
            result += f"            {model_name}.{column_name} = args['{column_name}']\n"
    result += "            db.session.commit()\n"
    result += "            return {model_name}.as_dict(), 201\n"
    result += "        else:\n"
    result += "            return {'error': '{model_name} not found'}, 404\n"
    result += "\n"

    result += "    def post(self):\n"
    result += f"        parser = reqparse.RequestParser()\n"
    for column_name, column_info in columns.items():
        if not column_info['primary_key']:
            result += f"        parser.add_argument('{column_name}', type={get_python_type(column_info['type'])})\n"
    result += "        args = parser.parse_args()\n"
    result += f"        {model_name} = {model_name}("
    for column_name, column_info in columns.items():
        if not column_info['primary_key']:
            result += f"{column_name}=args['{column_name}'],"
    result = result[:-1]
    result += ")\n"
    result += "        db.session.add({model_name})\n"
    result += "        db.session.commit()\n"
    result += "        return {model_name}.as_dict(), 201\n"

    return result
