
def enum(**enums):
    return type('Enum', (), enums)


data_type = enum(COMMENT=1, ERROR=2, DATA=3, WHITESPACE=4)


def show_columns(database, query_object):
    table = database.get(query_object['meta']['from']['table'])
    temp_table = database.temp_table(columns=['table', 'column'])

    for c in table.columns:
        columns = {'data': [table.data.name, c.data.name], 'type': data_type.DATA, 'error': None}
        temp_table.append_data(columns)
    return temp_table


def show_tables(database):
    temp_table = database.temp_table(columns=['database', 'table'])
    for t in database.tables:
        columns = [t.data.database, t.data.name]
        temp_table.append_data({'data': columns, 'type': data_type.DATA, 'error': None})
    #print temp_table
    return temp_table


def show_errors(database, table):
    temp_table = database.temp_table(columns=['error'])
    for e in table.errors:
        columns = [e]
        temp_table.append_data({'data': columns, 'type': data_type.DATA, 'error': None})
    return temp_table


def database(database):
    return database.get_curent_database()

