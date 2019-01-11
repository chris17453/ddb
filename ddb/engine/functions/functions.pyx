
import datetime


def enum(**enums):
    return type('Enum', (), enums)


data_type = enum(COMMENT=1, ERROR=2, DATA=3, WHITESPACE=4)


def f_show_columns(database, query_object):
    table = database.get(query_object['meta']['from']['table'])
    temp_table = database.temp_table(columns=['table', 'column'])

    for c in table.columns:
        columns = {'data': [table.data.name, c.data.name], 'type': data_type.DATA, 'error': None}
        temp_table.append_data(columns)
    return temp_table


def f_show_tables(database):
    temp_table = database.temp_table(columns=['database', 'table'])
    for t in database.tables:
        columns = [t.data.database, t .data.name]
        temp_table.append_data({'data': columns, 'type': data_type.DATA, 'error': None})
    #print temp_table
    return temp_table


def f_show_errors(database, table):
    temp_table = database.temp_table(columns=['error'])
    for e in table.errors:
        columns = [e]
        temp_table.append_data({'data': columns, 'type': data_type.DATA, 'error': None})
    return temp_table


def f_database(database):
    return database.get_curent_database()

def f_upper(arg):
    if not arg:
        return None
    return arg.upper()

def f_lower(arg):
    if not arg:
        return None
    return arg.lower()

def f_datetime(arg=None):
    return datetime.datetime.now()

def f_time(arg=None):
    return datetime.datetime.now().strftime('%H:%M:%S')

def f_date(arg=None):
    return datetime.datetime.now().strftime('%Y-%m-%d')

def f_version(version=None):
    if None==version:
        return 'GA.BB.LE'
    return version
        
def f_cat(arg1,arg2):
    if None ==arg1:
        arg1=''
    if None ==arg2:
        arg2=''
    return '{0}{1}'.format(arg1,arg2)

