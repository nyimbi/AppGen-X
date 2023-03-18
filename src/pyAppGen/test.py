from utils import parse_dbml, save_to_sqlite
from genmodels import generate_models
from genviews import generate_views



if __name__ == '__main__':
    tables = parse_dbml("test.dbml")
    save_to_sqlite(tables, 'table_defs.db')
    # mods = generate_models(tables)
    # views = generate_views(tables)
    # print('MODS \n\n', mods)
    # print ('VIEWS \n\n', views)