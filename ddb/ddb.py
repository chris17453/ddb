#!/bin/python
# functions
import os
import sys
import copy
import json
import yaml
import datetime
import lazyxml
import time
import tempfile  # from table import table
import argparse
import flextable
from cmd import Cmd
from os.path import expanduser

try:
    from yaml import CLoader as Loader
except ImportError:
    from yaml import Loader


# use the c based parser, or you're going to get massive lag with the python based solution

__version__='1.0.584'

# ################################################################################
#
# FUNCTIONS
#
# ################################################################################



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



# ################################################################################
#
#  Match
#
# ################################################################################



def evaluate_single_match(test, row, table):

    compare1 = None
    compare2 = None
    compare1_is_column = False
    compare2_is_column = False

    comparitor = test['c'].lower()
    index 
    like = None
    data = None

    # if None !=comparitor:
    #   comparitor=comparitor.lower()
    for column in table.columns:
        #print column.data.name
        if column.data.name == test['e1']:
            index = table.ordinals[column.data.name]
            #print "found1", column.data.name
            compare1 = row[index]  # table.ordinals[].get_data_from_column(column,row)
            # compare1=table.get_data_from_column(column,row)
            compare1_is_column = True
        if column.data.name == test['e2']:
            index = table.ordinals[column.data.name]
            #print "found2", column.data.name
            compare2 = row[index]  # table.get_data_from_column(column,row)
            # compare2=table.get_data_from_column(column,row)
            compare2_is_column = True
        if None != compare1 and None != compare2:
            break

    if None == compare1:
        compare1 = test['e1']
    if None == compare2:
        compare2 = test['e2']
    if None == compare1 and None == compare2:
        raise Exception("Where invalid {}".format(test))

    if comparitor == '=' or comparitor == 'is':
        if compare1 == compare2:
            #print compare1,compare2
            return True
    if comparitor == 'like':  # paritial match

        if True == compare1_is_column and True == compare2_is_column:
            raise Exception("Where invalid {}, like cant be between 2 columns".format(test))

        if True == compare1_is_column:
            like = compare2
            data = compare1
        else:
            like = compare1
            data = compare2

        if None == like:
            return False
        # if len(like)==0:
        #    return False
        #print "--"
        #print compare1,compare2,like
        if like[0] == '%':
            like_left = True
        else:
            like_left = False

        if like[-1] == '%':
            like_right = True
        else:
            like_right = False

        # compare middle of search
        if True == like_right and True == like_left:
            if data.find(like[1:-1]) > -1:
                return True
            else:
                return False

        # if not found at end bail
        if True == like_left:
            if data[-(len(like) - 1):] == like[1:]:
                return True
            else:
                return False

        # if not found at start, bail
        if True == like_right:
            if data[0:(len(like) - 1)] == like[0:-1]:
                return True
            else:
                return False

        return False
    if comparitor == '<':
        if compare1 < compare2:
            return True
    if comparitor == '>':
        if compare1 > compare2:
            return True
    if comparitor == '>=':
        if compare1 >= compare2:
            return True
    if comparitor == '<=':
        if compare1 <= compare2:
            return True
    if comparitor == '!=' or comparitor == '<>' or comparitor == 'not':
        if compare1 != compare2:
            return True

    return False


def evaluate_match(where, row, table):
    #print where
    if None == row:
        return False

    if 0 == len(where):
        #print "0 len"
        return True
    success = None
    skip_section = False
    operation = ""
    for test in where:
        #print test
        # if a evaluation chain failed, continue until out of that section
        if 'and' in test and skip_section:
            continue
        else:
            skip_section = False

        operation = None
        if 'where' in test:
            operation = 'where'

        if 'or' in test:
            operation = 'or'
            if success:
                return True

        if 'and' in test:

            operation = 'and'
            if not success:
                skip_section = True
                continue

        test_operation = test[operation]
        success = evaluate_single_match(test_operation, row, table)

    # never matched anytthing...
    if success is None:
        return False
    return success



# ################################################################################
#
# OUTPUT
#
# ################################################################################



def format_term(results,output_file):
    """ouput results data in the term format"""
    config = flextable.table_config()
    config.columns = results.get_columns_display()
    flextable.table(data=results.results, args=config)

def format_bash(temp_table,output_file):
    """ouput results data in the bash format"""
    data=temp_table.get_results()
    
    name="ddb"
    print ("# bash variable assignment for ddb output")
    print ("declare {0}_data -A".format(name))
    print ("declare {0}_info -A".format(name))
    print ("declare {0}_columns -A".format(name))
    print ("")

    column_index=0
    for column in data['columns']:
        print("{0}_columns[{1}]='{2}'".format(name,column_index,column))
        column_index+=1


    row_index=0
    for row in data['results']:
        column_index=0
        if not row['error']:
            row_error=''
        else:
            row_error=row['error']
        print("{0}_info[{1},error]='{2}'".format(name,row_index,row_error))
        if not row['type']:
            row_type=''
        else:
            row_type=row['type']
        print("{0}_info[{1},type]='{2}'".format(name,row_index,row_type))
        if not row['raw']:
            row_raw=''
        else:
            row_raw=row['raw']
        print("{0}_info[{1},raw]='{2}'".format(name,row_index,row_raw))
        for column in row['data']:
            print("{0}_data[{1},{2}]='{3}'".format(name,row_index,column_index,column))
            column_index+=1
        row_index+=1
    print ("# end ddb output ")
            
    

def format_raw(results,output_file):
    """ouput results data in the yaml format"""
    if not output_file:
        for row in results.results:
            print(row['raw'].rstrip())
    else:
        with open(output_file, "w") as write_file:
            for row in results.results:
                write_file.write(row['raw'])

def format_yaml(temp_table,output_file):
    """ouput results data in the yaml format"""
    results=temp_table.get_results()
    dump=yaml.safe_dump(results, default_flow_style=False)
    if not output_file:
        print dump
    else:
        with open(output_file, "w") as write_file:
            write_file.write(dump)

def format_json(temp_table,output_file):
    """ouput results data in the json format"""
    results=temp_table.get_results()
    if not output_file:
        dump=json.dumps(results)
        print dump
    else:
        with open(output_file, "w") as write_file:
            json.dump(results, write_file)
    
def format_xml(temp_table,output_file):
    """ouput results data in the xml format"""
    results=temp_table.get_results()
    dump=lazyxml.dumps({'data':results})
    if not output_file:
        print dump
    else:
        with open(output_file, "w") as write_file:
            write_file.write(dump)




# ################################################################################
#
# Language
#
# ################################################################################


sql_syntax = {
    'functions': [{'name': 'database', 'arguments': None},
                  {'name': 'count', 'arguments': [{'name': 'where', 'required': True}]},
                  {'name': 'sum', 'arguments': [{'name': 'column', 'required': True}]},
                  {'name': 'version', 'arguments': None},
                  {'name': 'upper', 'arguments': [{'name': 'column', 'required': True}]},
                  {'name': 'lower', 'arguments': [{'name': 'column', 'required': True}]},
                  {'name': 'cat', 'arguments':  [{'name': 'arg1', 'required': True}, {'name': 'arg2', 'required': True}]},
                  {'name': 'date', 'arguments': None },
                  {'name': 'time', 'arguments': None },
                  {'name': 'datetime', 'arguments': None },
                  ],
    'query_matrix': [
        {'query': 'show columns',
         'switch': [{'data': False, 'name': ['show', 'columns']},
                    {'arguments': 1,
                     'data': [{'sig': ['{table}']}],
                     'name': 'from'}]},
        {'query': 'show tables',
         'switch': [{'data': False, 'name': ['show', 'tables']},
                    ]},
        {'query': 'select',
         'argument': 1,
         'switch': [{'arguments': 0,
                     'data': [{'sig': ['{column}']},
                              {'sig': ['{column}',
                                       'as',
                                       '{display}']},
                              {'sig': ['{function}',
                                       '(',
                                       ')']},
                              {'sig': ['{function}',
                                       '(',
                                       '{argument1}',
                                       ')'
                                       ]},
                              {'sig': ['{function}',
                                       '(',
                                       '{argument1}',
                                       ',',
                                       '{argument2}',
                                       ')'
                                       ]},
                              {'sig': ['{function}',
                                       '(',
                                       '{argument1}',
                                       ',',
                                       '{argument2}',
                                       ',',
                                       '{argument3}',
                                       ')'
                                       ]},
                              {'sig': ['{function}',
                                       '(',
                                       ')',
                                       'as',
                                       '{display}'
                                       ]},
                              {'sig': ['{function}',
                                       '(',
                                       '{argument1}',
                                       ')',
                                       'as',
                                       '{display}'
                                       ]},
                              {'sig': ['{function}',
                                       '(',
                                       '{argument1}',
                                       ',',
                                       '{argument2}',
                                       ')',
                                       'as',
                                       '{display}'
                                       ]},
                              {'sig': ['{function}',
                                       '(',
                                       '{argument1}',
                                       ',',
                                       '{argument2}',
                                       ',',
                                       '{argument3}',
                                       ')',
                                       'as',
                                       '{display}'
                                       ]},

                              ],
                     'name': 'select'},
                    {'arguments': 1,
                     'data': [{'sig': ['{table}']}, {'sig': ['{table}', 'as', '{display}']}],
                     'name': 'from',
                     'optional': True},

                    {'arguments': 1,
                     'data': [{'sig': ['{table}']}, {'sig': ['{table}', 'as', '{display}']}],
                     'name': 'join',
                     'depends_on': 'from',
                     'optional': True},

                    {'arguments': 1,
                     'data': [{'sig': ['{table}']}, {'sig': ['{table}', 'as', '{display}']}],
                     'name': 'left join',
                     'depends_on': 'from',
                     'optional': True},

                    {'arguments': 1,
                     'data': [{'sig': ['{table}']}, {'sig': ['{table}', 'as', '{display}']}],
                     'name': 'right join',
                     'depends_on': 'from',
                     'optional': True},

                    {'arguments': 1,
                     'data': [{'sig': ['{table}']}, {'sig': ['{table}', 'as', '{display}']}],
                     'name': 'full join',
                     'depends_on': 'from',
                     'optional': True},

                    {'arguments': 1,
                     'data': [{'sig': ['{e1}', '{c}', '{e2}']}],
                     'name': 'on',
                     'optional': True,
                     'depends_on': 'join',
                     'store_array': True},
                    {'arguments': 1,
                     'data': [{'sig': ['{e1}', '{c}', '{e2}']}],
                     'depends_on': 'on',
                     'jump': 'on',
                     'name': 'and',
                     'optional': True,
                     'parent': 'on'},
                    {'arguments': 1,
                     'data': [{'sig': ['{e1}', '{c}', '{e2}']}],
                     'depends_on': 'on',
                     'jump': 'on',
                     'name': 'or',
                     'optional': True,
                     'parent': 'on'},


                    {'arguments': 1,
                     'data': [{'sig': ['{e1}', '{c}', '{e2}']}],
                     'name': 'where',
                     'optional': True,
                     'depends_on': 'from',
                     'store_array': True},
                    {'arguments': 1,
                     'data': [{'sig': ['{e1}', '{c}', '{e2}']}],
                     'depends_on': 'where',
                     'jump': 'where',
                     'name': 'and',
                     'optional': True,
                     'parent': 'where'},
                    {'arguments': 1,
                     'data': [{'sig': ['{e1}', '{c}', '{e2}']}],
                     'depends_on': 'where',
                     'jump': 'where',
                     'name': 'or',
                     'optional': True,
                     'parent': 'where'},
                    {'arguments': 0,
                     'data': [{'sig': ['{column}']},
                              {'sig': ['{column}', 'asc']},
                              {'sig': ['{column}', 'desc']}],
                     'name': ['order', 'by'],
                     'optional': True},
                    {'data': [{'sig': ['{length}']},
                              {'sig': ['{start}',
                                       ',',
                                       '{length}']}],
                     'specs':{'length':{'type': 'int','default': 0},'start':{'type': 'int','default': 0}},

                     'name': 'limit',
                     'optional': True}]},
        {'query': 'delete',
         'switch': [{'data': False, 'name': 'delete'},
                    {'arguments': 1,
                     'data': [{'sig': ['{table}']}],
                     'name': 'from'},
                    {'arguments': 1,
                     'data': [{'sig': ['{e1}', '{c}', '{e2}']}],
                     'name': 'where',
                     'optional': True,
                     'store_array': True},
                    {'arguments': 0,
                     'data': [{'sig': ['{e1}', '{c}', '{e2}']}],
                     'depends_on': 'where',
                     'jump': 'where',
                     'name': 'and',
                     'optional': True,
                     'parent': 'where'},
                    {'arguments': 1,
                     'data': [{'sig': ['{e1}', '{c}', '{e2}']}],
                     'depends_on': 'where',
                     'jump': 'where',
                     'name': 'or',
                     'optional': True,
                     'parent': 'where'}]},
        {'query': 'insert',
         'switch': [{'data': False, 'name': 'insert'},
                    {'arguments': 1,
                     'data': [{'sig': ['{table}']}],
                     'name': 'into'},
                    {'data': False, 'dispose': True, 'name': '('},
                    {'arguments': 0,
                     'data': [{'sig': ['{column}']}],
                     'name': 'columns',
                     'no_keyword': True},
                    {'data': False, 'dispose': True, 'name': ')'},
                    {'data': False,
                     'dispose': True,
                     'name': 'values'},
                    {'data': False, 'dispose': True, 'name': '('},
                    {'arguments': 0,
                     'data': [{'sig': ['{value}']}],
                     'name': 'values',
                     'no_keyword': True},
                    {'data': False, 'dispose': True, 'name': ')'}]},
        {'query': 'update',
         'switch': [{'arguments': 1,
                     'data': [{'sig': ['{table}']}],
                     'name': 'update'},
                    {'arguments': 0,
                     'data': [{'sig': ['{column}', '=', '{expression}']}],
                     'name': 'set'},
                    {'arguments': 1,
                     'data': [{'sig': ['{e1}', '{c}', '{e2}']}],
                     'name': 'where',
                     'optional': True,
                     'store_array': True},
                    {'arguments': 0,
                     'data': [{'sig': ['{e1}', '{c}', '{e2}']}],
                     'depends_on': 'where',
                     'jump': 'where',
                     'name': 'and',
                     'optional': True,
                     'parent': 'where'},
                    {'arguments': 1,
                     'data': [{'sig': ['{e1}', '{c}', '{e2}']}],
                     'depends_on': 'where',
                     'jump': 'where',
                     'name': 'or',
                     'optional': True,
                     'parent': 'where'}]},
        {'query': 'use',
         'switch': [{'arguments': 1,
                     'data': [{'sig': ['{table}']}],
                     'name': 'use'}]},
        {'query': 'drop table',
         'switch': [{'arguments': 1,
                     'data': [{'sig': ['table', '{table}']}],
                     'name': 'drop'}]},
        {'query': 'create table',
         'switch': [{'arguments': 1,
                     'data': [{'sig': ['table', '{table}']}],
                     'name': 'create'},
                    {'data': False, 'dispose': True, 'name': '('},
                    {'arguments': 0,
                     'data': [{'sig': ['{column}']}],
                     'name': 'columns',
                     'no_keyword': True},
                    {'data': False, 'dispose': True, 'name': ')'},
                    {'arguments': 1,
                     'data': [{'sig': ['=', '{file}']}],
                     'name': 'file'},
                     {'arguments': 1,
                     'data': [{'sig': ['=', '{field}']}],
                     'optional': True,
                     'specs':{'field':{'type': 'char','default': ','}},
                     'name': 'delimiter'},
                     {'arguments': 1,
                     'data': [{'sig': ['=', '{whitespace}']}],
                     'optional': True,
                     'specs':{'whitespace':{'type': 'bool'}},
                     'name': 'whitespace'},
                     {'arguments': 1,
                     'data': [{'sig': ['=', '{whitespace}']}],
                     'optional': True,
                     'specs':{'errors':{'type': 'bool'}},
                     'name': 'errors'},                     
                     {'arguments': 1,
                     'data': [{'sig': ['=', '{comments}']}],
                     'optional': True,
                     'specs':{'comments':{'type': 'bool'}},
                     'name': 'comments'},
                     {'arguments': 1,
                     'data': [{'sig': ['=', '{data_starts_on}']}],
                     'optional': True,
                     'specs':{'data_starts_on':{'type': 'int','default': 1}},
                     'name': 'data_starts_on'},]},
        {'query': 'update table',
         'switch': [{'arguments': 1,
                     'data': [{'sig': ['table', '{table}']}],
                     'name': 'update'},
                    {'data': False, 'dispose': True, 'name': '(','optional': True},
                    {'arguments': 0,
                     'data': [{'sig': ['{column}']}],
                     'name': 'columns',
                     'no_keyword': True,
                     'depends_on':'(',
                     'optional': True},
                    {'data': False, 'dispose': True, 'name': ')','optional': True,'depends_on':'('},
                    {'arguments': 1,
                     'data': [{'sig': ['=', '{file}']}],
                     'name': 'file',
                     'optional': True},
                     {'arguments': 1,
                     'data': [{'sig': ['=', '{field}']}],
                     'optional': True,
                     'specs':{'field':{'type': 'char','default': ','}},
                     'name': 'delimiter'},
                     {'arguments': 1,
                     'data': [{'sig': ['=', '{whitespace}']}],
                     'optional': True,
                     'specs':{'whitespace':{'type': 'bool'}},
                     'name': 'whitespace'},
                     {'arguments': 1,
                     'data': [{'sig': ['=', '{whitespace}']}],
                     'optional': True,
                     'specs':{'errors':{'type': 'bool'}},
                     'name': 'errors'},                     
                     {'arguments': 1,
                     'data': [{'sig': ['=', '{comments}']}],
                     'optional': True,
                     'specs':{'comments':{'type': 'bool'}},
                     'name': 'comments'},
                     {'arguments': 1,
                     'data': [{'sig': ['=', '{data_starts_on}']}],
                     'optional': True,
                     'specs':{'data_starts_on':{'type': 'int'}},
                     'name': 'data_starts_on'}
                     ]
                     },
        {'query': 'describe table',
         'switch': [{'arguments': 1,
                     'data': [{'sig': ['table', '{table}']}],
                     'name': 'describe'}]},
                          
 
    ]#query matrix array
}#sql_syntax


# ################################################################################
#
# TOKENIZER
#
# ################################################################################



debug_on = False


def info(msg, arg1=None, arg2=None, arg3=None):
    if True == debug_on:
        if arg3 is None and arg2 is None:
            print("{} {}".format(msg, arg1))
            return
        if arg3 is None:
            print("{} {} {}".format(msg, arg1, arg2))
            return
        if arg2 is None:
            print("{} {}".format(msg, arg1))
            return

        print("[{}]".format(msg))


# yes, this could be a giant regex, but no.
# TODO: memory optimization.. maybe not sure how wastefull this is

def tokenize(text, discard_delimiters=False, discard_whitespace=True, debug=False):
    global debug_on
    debug_on = debug
    tokens = []

    # clean leading and trailiong stuff
    text = text.strip()
    # visual formatting characters
    whitespace = {' ', '\t', '\n', '\r'}
    # these are solid non depth related blocks
    blocks = [
        ['\'', '\'', 'quote'],   # string block
        ['"', '"', 'quote'],   # string block
        ['[', ']', 'db'],   # mssql column
        ['`', '`', 'db'],   # mysql column
    ]

    keywords = ['ACCESSIBLE',
                'ADD',
                'ALL',
                'ALTER'
                'ANALYZE',
                'AND',
                'AS',
                'ASC',
                'ASENSITIVE',
                'BEFORE',
                'BETWEEN',
                'BIGINT',
                'BINARY',
                'BLOB',
                'BOTH',
                'BY',
                'CALL',
                'CASCADE',
                'CASE',
                'CHANGE',
                'CHAR',
                'CHARACTER',
                'CHECK',
                'COLLATE',
                'COLUMN',
                'CONDITION',
                'CONSTRAINT',
                'CONTINUE',
                'CONVERT',
                'CREATE',
                'CROSS',
                'CURRENT_DATE',
                'CURRENT_TIME',
                'CURRENT_TIMESTAMP',
                'CURRENT_USER',
                'CURSOR',
                'DATABASE',
                'DATABASES',
                'DAY_HOUR',
                'DAY_MICROSECOND',
                'DAY_MINUTE',
                'DAY_SECOND',
                'DEC',
                'DECIMAL',
                'DECLARE',
                'DEFAULT',
                'DELAYED',
                'DELETE',
                'DESC',
                'DESCRIBE',
                'DETERMINISTIC',
                'DISTINCT',
                'DISTINCTROW',
                'DIV',
                'DOUBLE',
                'DROP',
                'DUAL',
                'EACH',
                'ELSE',
                'ELSEIF',
                'ENCLOSED',
                'ESCAPED',
                'EXCEPT',
                'EXISTS',
                'EXIT',
                'EXPLAIN',
                'FALSE',
                'FETCH',
                'FLOAT',
                'FLOAT4',
                'FLOAT8',
                'FOR',
                'FORCE',
                'FOREIGN',
                'FROM',
                'FULLTEXT',
                'GENERAL',
                'GRANT',
                'GROUP',
                'HAVING',
                'HIGH_PRIORITY',
                'HOUR_MICROSECOND',
                'HOUR_MINUTE',
                'HOUR_SECOND',
                'IF',
                'IGNORE',
                'IGNORE_SERVER_IDS',
                'IN',
                'INDEX',
                'INFILE',
                'INNER',
                'INOUT',
                'INSENSITIVE',
                'INSERT',
                'INT',
                'INT1',
                'INT2',
                'INT3',
                'INT4',
                'INT8',
                'INTEGER',
                'INTERSECT',
                'INTERVAL',
                'INTO',
                'IS',
                'ITERATE',
                'JOIN',
                'KEY',
                'KEYS',
                'KILL',
                'LEADING',
                'LEAVE',
                'LEFT',
                'LIKE',
                'LIMIT',
                'LINEAR',
                'LINES',
                'LOAD',
                'LOCALTIME',
                'LOCALTIMESTAMP',
                'LOCK',
                'LONG',
                'LONGBLOB',
                'LONGTEXT',
                'LOOP',
                'LOW_PRIORITY',
                'MASTER_HEARTBEAT_PERIOD',
                'MASTER_SSL_VERIFY_SERVER_CERT',
                'MATCH',
                'MAXVALUE',
                'MEDIUMBLOB',
                'MEDIUMINT',
                'MEDIUMTEXT',
                'MIDDLEINT',
                'MINUTE_MICROSECOND',
                'MINUTE_SECOND',
                'MOD',
                'MODIFIES',
                'NATURAL',
                'NOT',
                'NO_WRITE_TO_BINLOG',
                'NULL',
                'NUMERIC',
                'ON',
                'OPTIMIZE',
                'OPTION',
                'OPTIONALLY',
                'OR',
                'ORDER',
                'OUT',
                'OUTER',
                'OUTFILE',
                'OVER',
                'PARTITION',
                'PRECISION',
                'PRIMARY',
                'PROCEDURE',
                'PURGE',
                'RANGE',
                'READ',
                'READS',
                'READ_WRITE',
                'REAL',
                'RECURSIVE',
                'REFERENCES',
                'REGEXP',
                'RELEASE',
                'RENAME',
                'REPEAT',
                'REPLACE',
                'REQUIRE',
                'RESIGNAL',
                'RESTRICT',
                'RETURN',
                'RETURNING',
                'REVOKE',
                'RIGHT',
                'RLIKE',
                'ROWS',
                'SCHEMA',
                'SCHEMAS',
                'SECOND_MICROSECOND',
                'SELECT',
                'SENSITIVE',
                'SEPARATOR',
                'SET',
                'SHOW',
                'SIGNAL',
                'SLOW',
                'SMALLINT',
                'SPATIAL',
                'SPECIFIC',
                'SQL',
                'SQLEXCEPTION',
                'SQLSTATE',
                'SQLWARNING',
                'SQL_BIG_RESULT',
                'SQL_CALC_FOUND_ROWS',
                'SQL_SMALL_RESULT',
                'SSL',
                'STARTING',
                'STRAIGHT_JOIN',
                'TABLE',
                'TERMINATED',
                'THEN',
                'TINYBLOB',
                'TINYINT',
                'TINYTEXT',
                'TO',
                'TRAILING',
                'TRIGGER',
                'TRUE',
                'UNDO',
                'UNION',
                'UNIQUE',
                'UNLOCK',
                'UNSIGNED',
                'UPDATE',
                'USAGE',
                'USE',
                'USING',
                'UTC_DATE',
                'UTC_TIME',
                'UTC_TIMESTAMP',
                'VALUES',
                'VARBINARY',
                'VARCHAR',
                'VARCHARACTER',
                'VARYING',
                'WHEN',
                'WHERE',
                'WHILE',
                'WINDOW',
                'WITH',
                'WRITE',
                'XOR',
                'YEAR_MONTH',
                'ZEROFILL'
                ]

    # blocks that must match depth
    # nested_block = [
    #                ['(',')']
    #              ]

    # operators # comparitors
    operators = [
        '&&',  # and short circuit
        '||',  # or short circuit
        '!=',  # Not Equal
        '<>',  # Not Equal
        '<=',  # Less than or equal
        '>=',  # Greater thanbor equal

        '>',  # Greater than
        '<',  # Less than

        '=',  # Equality
        '&',  # and
        '!',  # not
        '|',  # or

        'not',  # not
        'is',  # equality
        'like',  # partial match

        '+',  # addition
        '-',  # subtraction
        '/',  # divide
        '*',  # multiple
        '(',  # left paren   (grouping)
        ')',  # right paren  (grouping)
    ]

    # standard delimiters
    delimiters = [',', '.', ';']

    for token in whitespace:
        delimiters.append(token)

    for token in operators:
        delimiters.append(token)

    # add block identifiers to delimiters
    for b in blocks:
        if b[0] not in delimiters:
            delimiters.append(b[0])
        if b[1] not in delimiters:
            delimiters.append(b[1])

    delimiters_sorted = sort_array_by_length(delimiters)

    # padding prevents fencpost error
    #text+=" "
    text_length = len(text)
    # c is the incremental pointer to the string
    word_start = 0
    tokens = []
    c = 0
    #print delimiters_sorted
    delimter_len = 1
    in_block = None
    block = None

    while c < text_length:

        info("-", c)
        just_crossed_block = False
        for b in blocks:
            delimter_len = len(b[0])
            # info(b[0],b[1],c,delimter_len)
            fragment = text[c:c + delimter_len]
            # only check for block start if not in one
            if None == in_block:
                if True == compare_text_fragment(fragment, b[0]):
                    just_crossed_block = True
                    info("IN BLOCK", c)
                    in_block = b
                    block = b
                    c += delimter_len
                    info("IN BLOCK", c)
                    break
            # check for block end
            if True == compare_text_fragment(fragment, b[1]) or c >= text_length - 1:
                just_crossed_block = True
                info("NOT IN BLOCK", c)
                in_block = None
                c += delimter_len
                break
        # skip stuff in block
        if None != in_block:
            info("in block skip")
            if not just_crossed_block:
                c += 1
            continue
        #  equal.. greater than. we want the things on the last pass...
        info("position1", c, text_length)
        if c > text_length:
            info("Greater than length of text. exiting")

            break
        for d in delimiters_sorted:
            delimter_len = len(d)
            fragment = text[c:c + delimter_len]
            if c >= text_length - 1:
                info("Last Cycle")
            if True == compare_text_fragment(fragment, d) or c >= text_length - 1:
                info("Delemiter found", c, fragment)
                if c - word_start > 0:
                    info("Data word found", c - word_start)
                    word_end = c
                    if word_end >= text_length:
                        info("word ends on last character", word_end, text_length)
                        word_end = text_length
                    not_delimiter = text[word_start:word_end]
                    token_type = 'data'
                    if not_delimiter.upper() in keywords:
                        token_type = 'keyword'
                    if None != block:
                        block_left = block[0]
                        block_right = block[1]
                        block_type = block[2]
                        block = None
                        not_delimiter = not_delimiter[len(block_left):-len(block_right)]
                    else:
                        block_left = None
                        block_right = None
                        block_type = None
                    info("POSITION", c, not_delimiter)
                    # if not not_delimiter:
                    #    break

                    tokens.append({'type': token_type, 'data': not_delimiter, 'block_left': block_left, 'block_right': block_right, 'block_type': block_type})

                info("After Data Append, Position", c, 'of', text_length)
                # if  c>=text_length-1:
                #   info("Break, after end of string",c)
                #   break

                word_start = c + delimter_len

                if not fragment or fragment == '':
                    break
                if True == discard_whitespace and fragment in whitespace:
                    break

                # if True == discard_delimiters:
                #     continue

                delimiter_type = "delimiter"
                if fragment in operators:
                    delimiter_type = 'operator'
                else:
                    if fragment in whitespace:
                        delimiter_type = 'whitespace'

                info("delemiter c/fragment- ", c, fragment)
                tokens.append({'type': delimiter_type, 'data': fragment.lower()})

                break
        c += delimter_len

    if True == debug_on:
        info("-[Tokens]----------------")
        for t in tokens:
            info(t)
        info("-[End-Tokens]------------")
    return tokens


def compare_text_fragment(x, y):
    if None == x or None == y:
        return False
    if x == y:
        return True
    return False


def sort_array_by_length(data):
    max_len = -1
    for d in data:
        del_len = len(d)
        if del_len > max_len:
            max_len = del_len

    # make a new array, put them in from longest to shortest, remove dupes
    data_sorted = []
    for i in reversed(range(1, max_len + 1)):
        for d in data:
            if d not in data_sorted:
                if len(d) == i:
                    data_sorted.append(d)
    return data



# ################################################################################
#
# parser
#
# ################################################################################



#from .language import sql_syntax
#from ..tokenizer.sql_tokenize import info, tokenize

debug_on = False


class sql_parser:
    ##
    #     -- [] denotes array, comma seperated
    #     -- () denotes optional element
    #     -- {} denotes a variable element, such as column name
    #     -- |  denotes a choice
    #     -- EXPRESSION is a column from the select, a function, or a value
    #     -- CONDITION  is an evaluation condition   (=,equals,is,!=,<>,not,>,<,>=,<=)
    #     -- elements must appear in order of index

    #  QUERIES
    #   1 SHOW
    #   2    TABLES

    #   1 SHOW
    #   2    COLUMNS
    #   3 FROM
    #   4   {TABLE}

    #  1  SELECT
    #  2     [{COLUMN}
    #  3      (AS {DISPLAY_NAME})]
    #  4  FROM
    #  5     {TABLE}
    #  6   (WHERE
    #  7           {EXPRESSION} CONDITION {EXPRESSION}
    #  8     (AND  {EXPRESSION} CONDITION {EXPRESSION})
    #  9     (OR   {EXPRESSION} CONDITION {EXPRESSION})
    #     )
    #  10   (ORDER BY
    #  11        [{COLUMN} DIRECTION])
    #  12  (LIMIT ({START_INDEX},{LENGTH}) | ({LENGTH})
    #        )
    #
    #  1  DELETE
    #  4  FROM
    #  5     {TABLE}
    #  6   (WHERE
    #  7           {EXPRESSION} CONDITION {EXPRESSION}
    #  8     (AND  {EXPRESSION} CONDITION {EXPRESSION})
    #  9     (OR   {EXPRESSION} CONDITION {EXPRESSION})
    #     )

    #  1  UPDATE
    #  5     {TABLE}
    #     SET
    #        [{COLUMN}={EXPRESSION}]
    #  6   (WHERE
    #  7           {EXPRESSION} CONDITION {EXPRESSION}
    #  8     (AND  {EXPRESSION} CONDITION {EXPRESSION})
    #  9     (OR   {EXPRESSION} CONDITION {EXPRESSION})
    #     )

    # -- BELOW all () are litteral and must appear
    # -- Column count must match expression count
    #  1  INSERT
    #     INTO
    #  5      {TABLE}
    #         ([{COLUMN}])
    #     VALUES
    #         ({EXPRESSION}])

    def __init__(self, query, debug=False):
        # select * from table where x=y and y=2 order by x,y limit 10,2
        # select c1,c2,c3,c4 as x,* from table where x=y and y=2 order by x,y limit 10,2
        # select top 10 * from table where x=y and y=2 order by x,y
        # insert into table () values ()
        # delete from table where x=y and y=2

        global debug_on
        self.debug = debug
        self.debug_on = debug
        self.query_objects = []
        querys = query.split(';')
        info("Queries", querys)
        for q in querys:
            info("-----------------------------------")
            tokens = tokenize(q, discard_whitespace=True, debug=debug)
            # skip 0 length commands such as single ';'
            token_length = 0
            for token in tokens:
                if token['data'] != '':
                    token_length += 1

            info("Token Length", token_length)
            if token_length == 0:
                continue

            parsed = self.parse(tokens)
            if False == parsed:
                self.query_objects = None
                break
            self.query_objects.append(parsed)

        if None == self.query_objects:
            raise Exception("Invalid SQL")

    def parse(self, tokens):

        sql_object = []
        # SOME TODO!
        # loop through types
        debug = True
        query_object = {}
        for query in sql_syntax['query_matrix']:
            # loop through switches
            token_index = 0
            info("-----", query['query'])

            keyword_found = False
            switch_index = 0
            query_mode = None
            curent_object = {}
            switch = {}
            while switch_index < len(query['switch']) and token_index < len(tokens):

                info("Token Index", token_index, "token", tokens[token_index])
                info("Token Length", len(tokens))
                switch = query['switch'][switch_index]
                switch_index += 1
                curent_object = {}
                if 'dispose' in switch:
                    dispose = switch['dispose']
                else:
                    dispose = False
                if 'no_keyword' in switch:
                    no_keyword = switch['no_keyword']
                else:
                    no_keyword = False
                if 'store_array' in switch:
                    store_array = switch['store_array']
                else:
                    store_array = False

                if 'parent' in switch:
                    parent = switch['parent']
                else:
                    parent = None
                if 'optional' in switch:
                    optional = switch['optional']
                else:
                    optional = False

                if isinstance(switch['name'], list):
                    object_id = ' '.join([str(x) for x in switch['name']])
                    object_id = object_id.lower()
                else:
                    object_id = switch['name']
                    object_id = object_id.lower()
                info("Object Id:", object_id, "Token Id:", token_index)
                if False == no_keyword:
                    keyword_compare = self.get_sub_array(switch, 'name')
                    haystack = self.get_sub_array_sub_key(tokens[token_index:], 'data')
                    info(keyword_compare)
                    if True == self.single_array_match(keyword_compare, haystack):
                        info("match", keyword_compare, haystack)
                        # we use name because it may be a list. and its simpler to hash by name
                        # as long as the compare is good, we dont care
                        curent_object['mode'] = object_id
                        if switch_index == 1:
                            query_mode = query['query']
                        keyword_found = True
                    else:
                        if False == optional:
                            if True == debug:
                                info("Exiting")
                            break
                        else:
                            continue
                    if False == keyword_found:
                        info("Keywords exhausted")
                        break

                    token_index += len(keyword_compare)
                    info("advance token index ", token_index, switch['data'])
                else:
                    curent_object['mode'] = object_id

                if None == switch['data'] or False == switch['data']:
                    info("No data to match")
                    # only append object after argument collection is done
                    # query_object.append(curent_object)
                    if not dispose:
                        info("----------Adding", curent_object['mode'])
                        query_object[curent_object['mode']] = None

                # This is where data colection happens
                else:
                    in_argument = True
                    argument_index = 0
                    while True == in_argument:

                        info("---in argument")

                        # DEPENDENCY
                        # DEPENDENCY
                        # DEPENDENCY

                        if 'depends_on' in switch:
                            depends_on = switch['depends_on']
                        else:
                            info("--- Depends on nothing")
                            depends_on = None

                        # if there is a dependency, enforce
                        if None != depends_on:

                            depends_oncompare = self.get_sub_array(depends_on)

                            dependency_found = False
                            for q_o in query_object:
                                #info( depends_on,q_o)
                                haystack = self.get_sub_array(q_o)
                                if True == self.single_array_match(depends_oncompare, haystack):
                                    dependency_found = True
                            if False == dependency_found:
                                info("Missing", depends_on)
                                break
                            else:
                                info("Dependency found", depends_on)

                        # info("data",switch['data'])
                        if 'arguments' in switch:
                            arguments = switch['arguments']
                        else:
                            arguments = 1
                        info("Number of arguments", arguments)

                        data = self.get_sub_array(switch, 'data')
                        match_len = 0
                        match = None
                        for sig in data:
                            signature_compare = self.get_sub_array(sig, 'sig')
                            haystack = self.get_sub_array_sub_key(tokens[token_index:], 'data')
                            if True == self.single_array_match(signature_compare, haystack):
                                #    info("match", signature_compare,haystack)
                                if len(signature_compare) > match_len:
                                    match_len = len(signature_compare)
                                    match = signature_compare
                                    info("Best Match", match_len)
                        if None == match:
                            info("No match")
                            break
                        else:
                            w_index = 0
                            argument = {}
                            for word in match:
                                variable_data=tokens[token_index + w_index]['data']
                                if word[0:1] == '{' and word[-1] == '}':
                                    # if we have definitions
                                    variable=word[1:-1]
                                    variable_type='string'
                                    if 'specs' in switch:
                                        # if this is in or definitions
                                        if variable in switch['specs']:
                                            if 'type' in switch['specs'][variable]:
                                                variable_type=switch['specs'][variable]['type']
                                            
                                    if variable_type=='int':
                                        try:
                                            argument[variable] = tokens[token_index + w_index]['data'] = int(variable_data)
                                        except BaseException:
                                            raise Exception ("Variable data not an integer")
                                    elif variable_type=='bool':
                                        if variable_data.lower()=='true':
                                            argument[variable] =True
                                        elif variable_data.lower()=='false':
                                            argument[variable] =False
                                        else:
                                            raise Exception("Variable Data not boolean")
                                    elif variable_type=='char':
                                        if len(variable_data)!=1:
                                            raise Exception("variable data length exceeded, type char")
                                        argument[variable] =variable_data

                                    elif variable_type=='string':
                                        argument[variable] =variable_data
                                else:
                                    # normal keyword
                                    argument[word] = variable_data
                                w_index += 1
                            if 'arguments' not in curent_object:
                                curent_object['arguments'] = []

                            if arguments == 1:
                                curent_object['arguments'] = argument
                            else:
                                # add the arguments to curent object
                                curent_object['arguments'].append(argument)

                            info("match", match)
                            token_index += len(match)
                            if arguments != 0:
                                info("print not in list")
                                argument_index += 1
                                if argument_index >= arguments:
                                    info("----------Adding", curent_object['mode'])
                                    if True == store_array:
                                        if curent_object['mode'] not in query_object:
                                            query_object[curent_object['mode']] = []

                                        query_object[curent_object['mode']].append({curent_object['mode']: curent_object['arguments']})
                                    else:
                                        if None == parent:
                                            query_object[curent_object['mode']] = curent_object['arguments']
                                            info("NO APPEND")
                                        else:
                                            info("APPEND")
                                            query_object[parent].append({curent_object['mode']: curent_object['arguments']})
                                    jump = None
                                    if 'jump' in switch:
                                        info("JUMP")
                                        jump = switch['jump']
                                    if None != jump:
                                        tsi = 0
                                        for ts in query['switch']:
                                            if ts['name'] == jump:
                                                info("Jumping from ", switch_index, tsi + 1)
                                                switch_index = tsi + 1
                                                break
                                            tsi += 1
                                    in_argument = False

                                    in_argument = False
                            else:
                                info("in list")

                                if len(tokens) <= token_index:
                                    info("at the end")
                                    if True == store_array:
                                        if curent_object['mode'] not in query_object:
                                            query_object[curent_object['mode']] = []

                                        query_object[curent_object['mode']].append({curent_object['mode']: curent_object['arguments']})
                                    else:
                                        if None == parent:
                                            #print curent_object
                                            query_object[curent_object['mode']] = curent_object['arguments']
                                            info("NO APPEND")

                                        else:
                                            info("APPEND")
                                            query_object[parent].append({curent_object['mode']: curent_object['arguments']})

                                # look ahead to see if its a list ","
                                if len(tokens) > token_index:
                                    info("--looking ahead")
                                    # if its not exit
                                    info("----", tokens[token_index]['data'])
                                    if tokens[token_index]['data'] != ',':
                                        info("---not list")
                                        # only append object after argument collection is done
                                        info("----------Adding", curent_object['mode'])
                                        if True == store_array:
                                            if curent_object['mode'] not in query_object:
                                                query_object[curent_object['mode']] = []

                                            query_object[curent_object['mode']].append({curent_object['mode']: curent_object['arguments']})
                                        else:
                                            if None == parent:
                                                #print curent_object
                                                query_object[curent_object['mode']] = curent_object['arguments']
                                                info("NO APPEND")

                                            else:
                                                info("APPEND")
                                                query_object[parent].append({curent_object['mode']: curent_object['arguments']})
                                        jump = None
                                        if 'jump' in switch:
                                            jump = switch['jump']
                                        if None != jump:
                                            tsi = 0
                                            for ts in query['switch']:
                                                if ts['name'] == jump:
                                                    info("Jumping from ", switch_index, tsi + 1)
                                                    switch_index = tsi + 1
                                                    break
                                                tsi += 1
                                        in_argument = False
                                    else:
                                        info("------more list")
                                        token_index += 1

            # This is where we exit if we reached the end of processing with a full length
            #print token_index,len(tokens)
            info(switch_index, token_index, len(tokens))

            info(curent_object)
            # so we have run out of text to match and everything is good so far
            if token_index == len(tokens):
                info("############################think its a match")

                if 'arguments' not in curent_object and 'arguments' in switch:
                    info("Missing argument in last element")
                    bad = True
                    break

                # lets make sure the rest are optional
                if len(query['switch']) >= switch_index:
                    info("still checking")
                    bad = False
                    for t in range(switch_index, len(query['switch'])):
                        if 'optional' not in query['switch'][t]:
                            bad = True
                            break
                        else:
                            if not query['switch'][t]['optional']:
                                bad = True
                                break

                    if True == bad:
                        info("Not successful. required arguments missing")
                        break

                info("Query object", query_object)
                # check to make sure functions are valid
                if query_mode == 'select':
                    info("Validating Select Functions")
                    if 'select' in query_object:
                        for node in query_object['select']:
                            valid_function_name = False
                            is_function = False
                            if 'function' in node:
                                is_function = True
                                info("It's a function!")
                                for f in sql_syntax['functions']:
                                    if f['name'] == node['function']:
                                        argindex = 1
                                        if f['arguments'] is not None:
                                            for arg in f['arguments']:
                                                if arg['required']:
                                                    # if this argument key is not in the node dict
                                                    if 'argument{}'.format(argindex) not in node:
                                                        info("Missing arguments")
                                                        return False
                                                argindex += 1

                                        else:
                                            argindex = 0
                                        if 'argument{}'.format(argindex + 1) in node:
                                            info("Too many arguments")
                                            return False

                                    valid_function_name = True
                                    break
                            if False == valid_function_name and True == is_function:
                                info("FAIL", "This isnt a valid function", node['function'])
                                return False
                    else:
                        info("No columns in select")
                        return False

                info("SUCCESS")
                sql_object = {'mode': query_mode, 'meta': query_object}
                return sql_object
        return False

    # expand columns
    # TODO null trapping
    def expand_columns(self, query_object, columns):
        if query_object['mode'] == "select":
            expanded_select = []
            for item in query_object['meta']['select']:
                if 'column' in item:
                    if item['column'] == '*':
                        for column in columns:
                            expanded_select.append({'column': column})
                    else:
                        expanded_select.append(item)
                if 'function' in item:
                    expanded_select.append(item)

            query_object['meta']['select'] = expanded_select
        # ?? needed

    # support funcitons

    def get_sub_array(self, array, key=None):
        if None == key:
            if isinstance(array, str):
                return [array]
            else:
                return array
        if True == isinstance(array[key], list):
            return array[key]
        else:
            return [array[key]]

    # for tokens ['data']

    def get_sub_array_sub_key(self, array, key):
        temp_array = []

        for item in array:
            temp_array.append(item[key])

        return temp_array

    def single_array_match(self, needles, haystacks):
        """ Match a single or array of strings with with another string or array of strings"""

        # make needels an array, with or without a sub key
        if isinstance(needles, str):
            temp_needles = [needles]
        else:
            temp_needles = needles

        # make haystacks an array
        if isinstance(haystacks, str):
            temp_haystacks = [haystacks]
        else:
            temp_haystacks = haystacks

        # now we have 2 plain array/lists to compare

        index = 0
        for needle in temp_needles:
            # ran out of haystack to test. not a match
            if index >= len(temp_haystacks):
                return False
            haystack = temp_haystacks[index]
            # not a match
            if needle[0:1] != '{' and needle[-1] != '}':
                if needle.lower() != haystack.lower():
                    return False
            index += 1
        # if we got here it must match
        return True



# ################################################################################
#
# column
#
# ################################################################################



class column_v1:
    def noop(self, *args, **kw):
        pass

    def __init__(self, yaml=None):
        self.name = None
        self.display = None
        self.type = "string"
        self.default = None
        self.is_array = False
        self.has_default = False
        self.ordinal = -1
        self.visible = True
        self.fixed_width = True
        self.width = 100
        self.max_width = 0
        self.min_width = 0
        self.overflow = False
        self.search = False
        self.multi_search = False
        self.sort = False
        self.sort_ordinal = 0
        self.sort_default = False
        self.sort_default_asc = False
        self.data_ordinal = -1
        self.export = False
        self.options = {}
        if None != yaml:
            if 'name' in yaml:
                self.name = yaml['name']
            if 'display' in yaml:
                self.display = yaml['display']
            if 'type' in yaml:
                self.type = yaml['type']
            if 'default' in yaml:
                self.default = yaml['default']
            if 'is_array' in yaml:
                self.is_array = yaml['is_array']
            if 'has_default' in yaml:
                self.has_default = yaml['has_default']
            if 'ordinal' in yaml:
                self.ordinal = yaml['ordinal']
            if 'visible' in yaml:
                self.visible = yaml['visible']
            if 'fixed_width' in yaml:
                self.fixed_width = yaml['fixed_width']
            if 'width' in yaml:
                self.width = yaml['width']
            if 'max_width' in yaml:
                self.max_width = yaml['max_width']
            if 'min_width' in yaml:
                self.min_width = yaml['min_width']
            if 'overflow' in yaml:
                self.overflow = yaml['overflow']
            if 'search' in yaml:
                self.search = yaml['search']
            if 'multi_search' in yaml:
                self.multi_search = yaml['multi_search']
            if 'sort' in yaml:
                self.sort = yaml['sort']
            if 'sort_ordinal' in yaml:
                self.sort_ordinal = yaml['sort_ordinal']
            if 'sort_default' in yaml:
                self.sort_default = yaml['sort_default']
            if 'sort_default_asc' in yaml:
                self.sort_default_asc = yaml['sort_default_asc']
            if 'data_ordinal' in yaml:
                self.data_ordinal = yaml['data_ordinal']
            if 'export' in yaml:
                self.export = yaml['export']
            if 'options' in yaml:
                self.options = yaml['options']

    def to_v2(self):
        """convert a v1 column object to a v2 column object"""
        c2 = column_v2()
        c2.data   .name = self.name
        c2.data   .type = self.type
        c2.data   .is_array = self.is_array
        c2.data   .has_default = self.has_default
        c2.data   .default_value = self.default
        c2.data   .ordinal = self.data_ordinal
        c2.data   .export = self.export
        c2.data   .regex = ""
        c2.display.name = self.name
        c2.display.ordinal = self.ordinal
        c2.display.visible = self.visible
        c2.display.fixed_width = self.fixed_width
        c2.display.width = self.width
        c2.display.max_width = self.max_width
        c2.display.min_width = self.min_width
        c2.display.overflow = self.overflow
        c2.search .searchable = self.search
        c2.search .multi_search = self.multi_search
        c2.sort   .sortable = self.sort
        c2.sort   .ordinal = self.sort_ordinal
        c2.sort   .default = self.sort_default
        c2.sort   .default_asc = self.sort_default_asc
        return c2
        # not sure what i was doing with options. likely not used.


class column_v2:
    def noop(self, *args, **kw):
        pass

    def __init__(self, yaml=None):
        data_yaml = None
        search_yaml = None
        sort_yaml = None
        display_yaml = None

        if None != yaml:
            if 'data' in yaml:
                data_yaml = yaml['data']

            if 'search' in yaml:
                search_yaml = yaml['search']

            if 'sort' in yaml:
                sort_yaml = yaml['sort']

            if 'display' in yaml:
                display_yaml = yaml['display']

        self.data = column_data(yaml=data_yaml)
        self.display = column_display(yaml=display_yaml)
        self.search = column_search(yaml=search_yaml)
        self.sort = column_sort(yaml=sort_yaml)
        self.options = {}


class column_data:
    def noop(self, *args, **kw):
        pass

    def __init__(self, yaml=None):
        self.name = None
        self.type = "string"
        self.is_array = False
        self.has_default = False
        self.default_value = None
        self.ordinal = -1
        self.export = False
        self.regex = None

        if None != yaml:
            if 'name' in yaml:
                self.name = yaml['name']
            if 'type' in yaml:
                self.type = yaml['type']
            if 'is_array' in yaml:
                self.is_array = yaml['is_array']
            if 'has_default' in yaml:
                self.has_default = yaml['has_default']
            if 'default_value' in yaml:
                self.default_value = yaml['default_value']
            if 'ordinal' in yaml:
                self.ordinal = yaml['ordinal']
            if 'export' in yaml:
                self.export = yaml['export']
            if 'regex' in yaml:
                self.regex = yaml['regex']


class column_display:
    def noop(self, *args, **kw):
        pass

    def __init__(self, yaml=None):
        self.name = None
        self.ordinal = -1
        self.visible = True
        self.fixed_width = True
        self.width = 100
        self.max_width = 0
        self.min_width = 0
        self.overflow = False

        if None != yaml:
            if 'name' in yaml:
                self.name = yaml['name']
            if 'ordinal' in yaml:
                self.ordinal = yaml['ordinal']
            if 'visible' in yaml:
                self.visible = yaml['visible']
            if 'fixed_width' in yaml:
                self.fixed_width = yaml['fixed_width']
            if 'width' in yaml:
                self.width = yaml['width']
            if 'max_width' in yaml:
                self.max_width = yaml['max_width']
            if 'min_width' in yaml:
                self.min_width = yaml['min_width']
            if 'overflow' in yaml:
                self.overflow = yaml['overflow']


class column_search:
    def noop(self, *args, **kw):
        pass

    def __init__(self, yaml=None):
        self.searchable = False
        self.multi_search = False

        if None != yaml:
            if 'searchable' in yaml:
                self.searchable = yaml['searchable']
            if 'multi_search' in yaml:
                self.multi_search = yaml['multi_search']


class column_sort:
    def noop(self, *args, **kw):
        pass

    def __init__(self, yaml=None):
        self.sortable = False
        self.ordinal = 0
        self.default = False
        self.default_asc = False

        if None != yaml:
            if 'sortable' in yaml:
                self.sortable = yaml['sortable']
            if 'ordinal' in yaml:
                self.ordinal = yaml['ordinal']
            if 'default' in yaml:
                self.default = yaml['default']
            if 'default_asc' in yaml:
                self.default_asc = yaml['default_asc']



# ################################################################################
#
# table
#
# ################################################################################



class table:
    def noop(self, *args, **kw):
        pass

    def __init__(self, file=None, 
                    show_config=False, 
                    database=None, 
                    columns=None, 
                    name=None, 
                    data_file=None, 
                    field_delimiter=None, 
                    config_directory=None,
                    comments=None,
                    whitespace=None,
                    errors=None,
                    data_on=None
    ):
        self.version = 1
        self.ownership = table_ownership()
        self.delimiters = table_delimiters()
        self.visible = table_visible_attributes()
        self.data = table_data(name=name, database=database)
        self.columns = []
        self.active = True
        self.ordinals = {}
        self.errors = []
        self.results = []
        self.config_directory = config_directory
        
        self.update(data_file=data_file, 
                    columns=columns, 
                    field_delimiter=field_delimiter, 
                    comments=comments,
                    whitespace=whitespace,
                    errors=errors,
                    data_on=data_on)

        if None != file:
            if os.path.exists(file):
                with open(file, 'r') as stream:
                    yaml_data = yaml.load(stream, Loader=Loader)
                    if None == yaml_data:
                        raise Exception("Table configuration empty")
                    #print yaml_data
                    for key in yaml_data:
                        if 'version' == key:
                            self.version = yaml_data[key]

                        if 'ownership' == key:
                            self.ownership = table_ownership(yaml=yaml_data[key])

                        if 'delimiters' == key:
                            self.delimiters = table_delimiters(yaml=yaml_data[key])

                        if 'visible' == key:
                            self.visible = table_visible_attributes(yaml=yaml_data[key])

                        if 'data' == key:
                            self.data = table_data(yaml=yaml_data[key])

                        # one offs
                        if 'columns' == key:
                            for c in yaml_data['columns']:
                                # if self.version == 1:
                                #    cv1=column_v1( c )
                                #    cv2=cv1.to_v2()
                                #    self.columns.append( cv2 )
                                # if self.version == 2:
                                self.columns.append(column_v2(c))

                        if 'active' == key:
                            self.active = yaml_data[key]

                        # attr=getattr(self,key)
                        # setattr(self,key,yaml_data[key])

        self.update_ordinals()
        yaml.emitter.Emitter.process_tag = self.noop
        if True == show_config:
            yaml.dump(self, sys.stdout, indent=4, default_flow_style=False, allow_unicode=True, explicit_start=True, explicit_end=True)
        if None != self.data.path:
            if False == os.path.exists(self.data.path):
                raise Exception("Data file invalid for table: {}, path:{}".format(self.data.name, self.data.path))

    def update(self,
                    columns=None, 
                    data_file=None, 
                    field_delimiter=None, 
                    comments=None,
                    whitespace=None,
                    errors=None,
                    data_on=None):
        if None != data_on:
            self.data.starts_on_line=int(data_on)
        
        if None != comments:
            self.visible.comments=comments

        if None != whitespace:
            self.visible.whitespace=whitespace

        if None != errors:
            self.visible.errors=errors


        if None != field_delimiter:
            self.set_field_delimiter(field_delimiter)

        if None != data_file:
            self.data.path = data_file

        if None != columns:
            self.columns=[]
            for column in columns:
                self.add_column(column)

    def set_field_delimiter(self, delimiter):
        self.delimiters.field = delimiter

    def append_data(self, data):
        """Add a row to the resultset for this table"""
        self.results.append(data)

    def column_count(self):
        """Return the column count for this table"""
        return len(self.columns)

    def get_columns(self):
        """return a list of columns"""
        columns = []
        for column in self.columns:
            columns.append(column.data.name)
        return columns

    def get_columns_display(self):
        """return a list of columns with alternate display name"""
        columns = []
        for column in self.columns:
            if None != column.display.name:
                columns.append(column.display.name)
            else:
                columns.append(column.data.name)
        return columns

    def get_results(self):
        columns=self.get_columns_display()
        return {'columns':columns,'results':self.results}

    def results_length(self):
        """Return the result set length for this table"""
        return len(self.results)

    def error_count(self):
        """Return the result set length for this table"""
        return len(self.errors)

    def add_error(self, error):
        """Add an error to the list of errors processed this cycle"""
        self.errors.append(error)

    def add_column(self, name, display=None):
        """Add a column to this table"""
        column = column_v2()
        column.data.name = name
        column.display.name = display
        self.columns.append(column)
        self.update_ordinals()

    def get_column_at_data_ordinal(self, ordinal):
        for c in self.columns:
            if c.data.ordinal == int(ordinal):
                return c.data.name
        return None

    def has_column(self, column):
        """determine if a column exists by string name"""
        if column == '*':
            return True
        for c in self.columns:
            if column == c.data.name:
                return True
        return False

    def get_ordinal_by_name(self, name):
        for c in self.columns:
            if c.data.name == name:
                return c.data.ordinal
        return None

    def column_ordinals(self):
        temp_columns = []
        for c in self.columns:
            if c.display.visible:
                temp_columns.append({'data': c.data.ordinal, 'display': c.display.ordinal})

        #L = [(k,v) for (k,v) in temp_columns]
        # temp_columns=sorted(L,key=lambda (k,v): v['display'])  # change to data to sort by data
        return temp_columns

    def does_data_ordinal_exist(self, ordinal):
        for c in self.columns:
            if int(c.data.ordinal) == ordinal:
                return True
        return False

    def get_lowest_available_ordinal(self):
        for c in range(0, len(self.columns)):
            if False == self.does_data_ordinal_exist(c):
                return c
        return None

    def get_column_by_name(self, name):
        for c in self.columns:
            if c.data.name == name:
                return c

    def get_data_by_name(self, name, row):
        for c in self.columns:
            if c.data.name == name:
                i = c.data.ordinal
                if None == row:
                    return None
                if len(row) <= i:
                    return None
                return row[i]

    def get_data_from_column(self, column, row):
        i = column.data.ordinal
        if None == row:
            return None
        if len(row) <= i:
            return None
        return row[i]

    def update_ordinals(self):
        if None == self.columns:
            return

        column_count = len(self.columns)
        #has_ordinal=[i for i in range(column_count)]

        self.ordinals = {}
        for k, v in enumerate(self.columns):
            if None == v.data.ordinal or -1 == v.data.ordinal:

                #print (self.columns[k].data.ordinal)
                self.columns[k].data.ordinal = self.get_lowest_available_ordinal()
                self.ordinals[v.data.name] = self.columns[k].data.ordinal
            else:
                self.ordinals[v.data.name] = v.data.ordinal

        # create lookup hash
        # for i in range (0,column_count):
        #    has_ordinal[i]=False
#
        # index=0
        # for c in self.columns:
        #    c.data.ordinal=index
        #    display_ordinal=c.display.ordinal
        #    display_visible=c.display.visible
        #    index+=1
        #
        #    if True == display_visible and  -1 < display_ordinal and display_ordinal < column_count:
        #        has_ordinal[display_ordinal]=True
        #    else:
        #        c.display.ordinal=-1;
#
        # for oi in range(0,columns_count):
        # for c in self.columns:
        #    column=c
        #    if True == column.display.visible and column.display.ordinal==-1:
        #        for i in range (0,column_count):
        #            if False == has_ordinal[i]:
        #                print(" NEEDS {0,2} - {1} ",format(i,c.data.name))
        #                c.dispaly.ordinal=i
        #                has_ordinal[i]=True
        #                break
        #    else:
        #        print(" HAS   {0,2} - {1}".format(column.ordinal,column.data.name))

    def save(self):
        # if no config dir given, save in users home dir
        if None == self.config_directory:
            home = os.path.expanduser("~")
            # make app dir
            if not os.path.exists(os.path.join(home, '.ddb')):
                os.makedirs(os.path.join(home, '.ddb'))
            home = os.path.join(home, '.ddb')
        else:
            home = self.config_directory

        if None == self.data.name:
            raise Exception("Cannot save a table without a name")

        if None == self.data.database:
            raise Exception("Cannot save a table without a database name")

        if not os.path.exists(os.path.join(home, self.data.database)):
            os.makedirs(os.path.join(home, self.data.database))

        home = os.path.join(home, self.data.database)
        if None == self.data.config:
            self.data.config = os.path.join(home, "{}.ddb.yaml".format(self.data.name))

        with open(self.data.config, 'w') as stream:
            yaml.emitter.Emitter.process_tag = self.noop
            yaml.dump(self, indent=4, default_flow_style=False, allow_unicode=True, explicit_start=True, explicit_end=True, stream=stream)
            stream.close()


class table_visible_attributes:
    def noop(self, *args, **kw):
        pass

    def __init__(self, yaml=None):
        self.comments = False
        self.errors = True
        self.whitespace = False
        if None != yaml:

            if 'comments' in yaml:
                self.comments = yaml['comments']
            if 'errors' in yaml:
                self.errors = yaml['errors']
            if 'whitespace' in yaml:
                self.whitespace = yaml['whitespace']


class table_data:
    def noop(self, *args, **kw):
        pass

    def __init__(self, yaml=None, name=None, database=None):
        self.type = 'Temp'
        self.name = None
        self.database = 'main'
        self.display_name = None
        self.multi_search = True
        self.starts_on_line = 0
        self.uid = None
        self.path = None
        self.key = None
        self.ordinal = -1
        self.config = None
        self.retults = None
        if None != name:
            self.name = name

        if None != database:
            self.database = database

        if None != yaml:
            if 'name' in yaml:
                self.name = yaml['name']
            if 'database' in yaml:
                self.database = yaml['database']
            if 'display_name' in yaml:
                self.display_name = yaml['display_name']
            if 'multi_search' in yaml:
                self.multi_search = yaml['multi_search']
            if 'starts_on_line' in yaml:
                self.starts_on_line = int(yaml['starts_on_line'])
            if 'uid' in yaml:
                self.uid = yaml['uid']
            if 'path' in yaml:
                self.path = yaml['path']
            if 'key' in yaml:
                self.key = yaml['key']
            if 'ordinal' in yaml:
                self.ordinal = int(yaml['ordinal'])


class table_ownership:
    def noop(self, *args, **kw):
        pass

    def __init__(self, yaml=None):
        self.group = None
        self.entity = None
        self.location = None
        if None != yaml:
            if 'group' in yaml:
                self.group = yaml['group']
            if 'entity' in yaml:
                self.entity = yaml['entity']
            if 'location' in yaml:
                self.location = yaml['location']


class table_delimiters:
    def noop(self, *args, **kw):
        pass

    def __init__(self, yaml=None):
        self.field = ","
        self.array = "|"
        self.error = "#"
        self.block_quote = None
        self.comment = ["#", ";", "/"]
        # TODO hard coding this for a moment... must think
        self.new_line = "\n"
        if None != yaml:
            if 'field' in yaml:
                self.field = yaml['field']
            if 'error' in yaml:
                self.error = yaml['error']
            if 'array' in yaml:
                self.array = yaml['array']
            if 'comment' in yaml:
                self.comment = yaml['comment']
            if 'block_quote' in yaml:
                self.block_quote = yaml['block_quote']
                if isinstance(self.block_quote, str):
                    if not self.block_quote.strip():
                        self.block_quote = None
                else:
                    self.block_quote = None





# ################################################################################
#
# DATABASE
#
# ################################################################################



class database:
    tables = []

    def __init__(self, config_file=None, show_config=False):
        self.curent_database = None
        self.tables = []
        is_file = False
        self.config_file = None
        if None != config_file and config_file != False:
            self.config_file = config_file
            tables = self.get_tables()
            for table_file in tables:
                self.tables.append(table(table_file, show_config))
            return

    def set_database(self, database_name):
        # TODO validate database name
        self.curent_database = database_name

    def get(self, table_name, database_name=None):
        """Get a Table structure in the database."""
        if None == database_name:
            database_name = self.get_curent_database()
        for c in self.tables:
            if c.data.name == table_name and database_name == c.data.database:
                return c
        return None
        #raise Exception("Error: configs.get -> can't find configuration for table:{}".format(table_name))

    def count(self):
        """Return a count ot tables in the database"""
        return len(self.tables)

    def get_clone(self, table_name):
        """Clone a Table structure in the database."""
        table = self.get(table_name)
        if None == table:
            raise Exception("Table does not exist.{}".format(table_name))
        temp_table = copy.deepcopy(table)
        temp_table.columns = []
        return temp_table

    def temp_table(self, name=None, columns=[],delimiter=None):
        """Create a temporary table to preform operations in"""
        if None == name:
            name = "#table_temp"  # TODO make unique random name
        return table(name=name, columns=columns, database=self.get_curent_database(),field_delimiter=delimiter)

    def create_config(self, config_file):
        try:
            if False == os.path.exists(config_file):
                dirname = os.path.dirname(config_file)
                if False == os.path.exists(dirname):
                    os.makedirs(dirname)
                #print ("Successfully created the directory %s " % path)
            yaml_data = {}
            f = open(config_file, "w")
            yaml.dump(yaml_data, f)
            f.close()
            return
        except Exception as ex:
            print "Cant create configuration file: {}".format(ex)

    def create_table_config(self, name, db, columns,delimiter=None):
        if None == self.config_file:
            raise Exception("Not using a config file")

        t = table(name=name, database=db, columns=columns,field_delimiter=delimiter)
        t.save()
        self.add_config(t.data.path)

    def add_config(self, table_config=None, table=None):
        if None == self.config_file:
            raise Exception("Not using a config file")
        if not os.path.exists(self.config_file):
            self.create_config(self.config_file)

        # if we have a file name, lets add it
        if None != table_config:
            print "Adding table config"
            with open(self.config_file, 'r') as stream:
                config = table(table_config)
                yaml_data = yaml.load(stream)
                db = config.data.database
                if None == db:
                    db = self.get_default_database()

                if db not in yaml_data:
                    yaml_data[db] = {}

                yaml_data[db][config.data.name] = {'name': config.data.name, 'path': table_config}

                f = open(self.config_file, "w")
                yaml.dump(yaml_data, f)
                f.close()

        # if we have a table lets save it
        if table is not None:
            with open(self.config_file, 'r') as stream:
                yaml_data = yaml.load(stream)
                if None == yaml_data:
                    yaml_data = {}
                db = table.data.database
                if None == db:
                    db = self.get_default_database()

                if db not in yaml_data:
                    yaml_data[db] = {}

                yaml_data[db][table.data.name] = {'name': table.data.name, 'path': table.data.config}
                f = open(self.config_file, "w")
                yaml.dump(yaml_data, f)
                f.close()
        return True

    def get_default_database(self):
        if self.curent_database is None:
            return 'main'

    def get_curent_database(self):
        if self.curent_database is None:
            return self.get_default_database()
        return self.curent_database

    def create_table(self, table_name, columns, data_file, 
                                            database_name=None,
                                            delimiter=None,
                                            comments=None,
                                            errors=None,
                                            whitespace=None,
                                            data_on=None):
        if None == self.config_file:
            raise Exception("Not using a config file")
        if False == os.path.isfile(data_file):
            raise Exception("Data file does not exist")

        if None == database_name:
            database_name = self.get_curent_database()
        exists = self.get(table_name, database_name)
        # it exists. so no dont create it
        if None != exists:
            raise Exception("table already exists")

        config_directory = os.path.dirname(self.config_file)
        t = table(  name=table_name, 
                    database=database_name, 
                    columns=columns, 
                    config_directory=config_directory,
                    field_delimiter=delimiter,
                    data_on=data_on,
                    comments=comments,
                    whitespace=whitespace,
                    errors=errors)
        t.data.path = data_file
        res = t.save()
        if False == res:
            raise Exception("Couldn't save table configuation")
        self.add_config(table=t)

        self.reload_config()
        return True

    def drop_table(self, table_name, database_name=None):
        if None == database_name:
            database_name = self.get_curent_database()
        #print table_name,database_name
        for index in range(0, len(self.tables)):
            #print self.tables[index].data.name,self.tables[index].data.database
            if self.tables[index].data.name == table_name and self.tables[index].data.database == database_name:
                res = self.remove_config(table_object=self.tables[index])
                if False == res:
                    raise Exception("Failed to remove configuration for table")
                self.tables.pop(index)
                self.reload_config()
                return True
                break
        raise Exception("Failed to drop table. Does not exist")

    def remove_config(self, table_config=None, table_object=None):
        try:
            if not os.path.exists(self.config_file):
                self.create_config(self.config_file)
            with open(self.config_file, 'r') as stream:
                if table_object is None:
                    config = table(table_config)
                else:
                    config = table_object
                yaml_data = yaml.load(stream)
                db = config.data.database
                if None == db:
                    db = self.get_default_database()

                if db not in yaml_data:
                    yaml_data[db] = {}

                table_name = config.data.name
                #print db,table_name
                if table_name in yaml_data[db]:
                    yaml_data[db].pop(table_name, None)

                f = open(self.config_file, "w")
                yaml.dump(yaml_data, f)
                f.close()
                return True
        except Exception as ex:
            raise Exception("failed to remove table from db configuration")

    def reload_config(self):
        temp_tables = self.get_tables()
        table_swap = []
        # add temp tables to list
        for t in self.tables:
            if t.data.type == 'Temp':
                table_swap.append(t)

        for t in temp_tables:
            table_swap.append(table(t))

        self.tables = table_swap

    def get_tables(self):
        if None == self.config_file:
            return []

        if False == os.path.exists(self.config_file):
            self.create_config(self.config_file)

        tables = []
        if False == os.path.exists(self.config_file):
            raise Exception("db config invalid")

        with open(self.config_file, 'r') as stream:
            yaml_data = yaml.load(stream)
            # could be empty
            if  yaml_data != None:
                for db in yaml_data:
                    if yaml_data[db] !=None:
                        for table in yaml_data[db]:
                            tables.append(yaml_data[db][table]['path'])

        return tables



# ################################################################################
#
# INTERACTIVE
#
# ################################################################################



class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


class ddbPrompt(Cmd):
    prompt = 'ddb> '
    intro = "Welcome! Type ? to list commands. Version: {0}".format(__version__)

    def cmdloop_with_keyboard_interrupt(self):
        doQuit = False
        while doQuit != True:
            try:
                self.cmdloop()
                doQuit = True
            except KeyboardInterrupt:
                self.help_exit("")

    def set_vars(self,
                 config_file=None,
                 debug=False,
                 no_clip=False,
                 width='auto'):
        if debug is None:
            debug = False
        self.debug = debug
        self.no_clip = no_clip
        self.width = width
        self.engine = sql_engine(config_file=config_file, debug=self.debug, mode="full",output='term',output_file=None)

    def msg(self, type, name, message=''):
        if type == 'info':
            color = bcolors.OKGREEN
        if type == 'warn':
            color = bcolors.WARNING
        if type == 'error':
            color = bcolors.FAIL

        print("{2}>>>{3} {4}{0}{3} {1}".format(name, message, bcolors.OKBLUE, bcolors.ENDC, color))

    ##
    def do_exit(self, inp):
        self.msg("info", "Bye")
        return True

    def help_exit(self, inp):
        self.msg("info", 'exit the application. Shorthand: x q Ctrl-D.')

    ##
    def do_debug(self, inp):
        if not self.debug:
            self.debug = True
            self.msg("info", "Debugging ON")
        else:
            self.debug = False
            self.msg("info", "Debugging Off")
        self.engine.debugging(debug=self.debug)

    def help_debug(self, inp):
        self.msg("info", 'Toggle debugging on or off')

    ##

    def do_config(self, inp):
        try:
            self.msg("info", "configuration_file set to'{}'".format(inp))
            self.engine = sql_engine(config_file=inp, debug=self.debug)
        except Exception as ex:
            self.msg("error", "config", ex)

    def help_config(self):
        self.msg("info", "Set configuration file.")

    ##
    # def do_show_errors(self, inp):
    #    self.engine.print_errors()

    # def help_show_errors(self):
    #   self.msg("info","Show last error(s) generated")
    ##

    def default(self, inp):
        #print inp
        if inp == 'x' or inp == 'q':
            return self.do_exit("")

        try:
            if None == self.engine:
                print ("sql engin gone")
                return
            start = time.time()
            results = self.engine.query(sql_query=inp)
            end = time.time()
            self.engine.format_output(results)

            self.msg("info", "executed in {} seconds".format(end - start))
            inp = None
        except Exception as ex:
            self.msg("error", ex)

    def default_exit(self):
        self.msg("info", 'exit the application. Shorthand: x q Ctrl-D.')

    do_EOF = help_exit
    help_EOF = help_exit



# ################################################################################
#
# SQL ENGINE
#
# ################################################################################



debug_on = False


def info(msg, arg1=None, arg2=None, arg3=None):
    if True == debug_on:
        print(msg, arg1, arg2, arg3)

# Fix delete
# Add insert
# Fix errors
# Add Update


def enum(**enums):
    return type('Enum', (), enums)


class sql_engine:
    """A serverless flat file database engine"""


    data_type = enum(COMMENT=1, ERROR=2, DATA=3, WHITESPACE=4)

    def __init__(self, config_file=None, query=None, debug=False, mode='array',output='term',output_file=None):
        global debug_on
        debug_on = debug
        self.debug = debug
        self.results = None
        self.mode = mode
        self.output=output
        self.output_file=output_file

        # print "Config",config_file
        self.database = database(config_file=config_file)
        self.current_database = self.database.get_default_database()
        if None != query:
            self.query(query)

    # def set_configuration(self,database_instance):
    #    self.database=database
    #    if False == self.has_configuration():
    #        raise Exception("No configuration data")


    def format_output(self,results):
        """display results in different formats
          if output_file==None then everything is directed to stdio

          output=(bash|term|yaml|json|xml)
          output_file= None or file to write to
          """        
        if None==results:
            return
        
        mode=self.output.lower()
        if 'bash'==mode:
            format_bash(results,self.output_file)
        
        elif 'term'==mode:
            format_term(results,self.output_file)
        
        elif 'raw'==mode:
            format_raw(results,self.output_file)
        
        elif 'yaml'==mode:
            format_yaml(results,self.output_file)
        
        elif 'json'==mode:
            format_json(results,self.output_file)
        
        elif 'xml'==mode:
            format_xml(results,self.output_file)
        #default
        else: 
            format_term(results,self.output_file)



    def debugging(self, debug=False):
        self.debug = debug

    def define_table(self, table_name, database_name, columns, data_file, field_delimiter=None):
        """Progromatically define a table. Not saved to a configuration file, unless manualy activated"""
        t = table(database=database_name, columns=columns, name=table_name, data_file=data_file, field_delimiter=field_delimiter)
        self.database.tables.append(t)

    def has_configuration(self):
        if None == self.database:
            return False
        # table count invalid.. we may add some
        # table_count=self.database.count()
        # if table_count==0:
        #    return False
        return True

    def query(self, sql_query):
        if False == self.has_configuration():
            raise Exception("No table found")
        self.results = None

        # update table info...
        # it may have changed...
        # self.database.reload_config()

        parser = sql_parser(sql_query, self.debug)
        if False == parser.query_objects:
            raise Exception("Invalid SQL")

        for query_object in parser.query_objects:

            info("Engine: query_object", query_object)
            #print  query_object
            # exit(9)
            # get columns, doesnt need a table
            #print query_object['mode']
            if query_object['mode'] == "show tables":

                self.results = f_show_tables(self.database)
            if query_object['mode'] == "show columns":
                self.results = f_show_columns(self.database, query_object)
            # if query_object['mode']=="show errors":
            #    self.results=show_errors(self.database,self.table)
            #print query_object
            if query_object['mode'] == 'select':
                self.results = self.select(query_object, parser)

            if query_object['mode'] == 'insert':
                self.results = self.insert(query_object)

            if query_object['mode'] == 'update':
                self.results = self.update(query_object)

            if query_object['mode'] == 'delete':
                self.results = self.delete(query_object)

            if query_object['mode'] == 'use':
                self.results = self.use(query_object)

            if query_object['mode'] == 'drop table':
                self.results = self.drop_table(query_object)

            if query_object['mode'] == 'create table':
                self.results = self.create_table(query_object)

            if query_object['mode'] == 'update table':
                self.results = self.update_table(query_object)

            if query_object['mode'] == 'describe table':
                self.results = self.describe_table(query_object)

        # only return last command
        if None != self.results:
            if self.mode == 'full':
                return self.results

            # if the result set it not empty
            if None != self.results.results:
                if self.mode == 'array':
                    new_array = []
                    for line in self.results.results:
                        new_array.append(line['data'])
                    return new_array

                if self.mode == 'object':
                    new_array = []
                    columns = self.results.get_columns()
                    len_col = len(columns)
                    for line in self.results.results:
                        new_dict = {}
                        for i in range(0, len_col):
                            if len(line['data']) < i:
                                break
                            new_dict[columns[i]] = line['data'][i]
                        new_array.append(new_dict)
                    return new_array

        return None

    def change_database(self, database_name):
        query = "use {}".format(database_name)
        results = self.query(query)
        if None == results:
            return False
        return True

    def limit(self, data_stream, index, length):
        if None == index:
            index = 0
        if None == length:
            length = len(data_stream) - index

        data_stream_lenght = len(data_stream)
        if index >= data_stream_lenght:
            #print("-Index is out of range for query. {} of {}".format(index,data_stream_lenght))
            return []
        if index + length > data_stream_lenght:
            #print("Length is out of range for query. {} of {}".format(length,data_stream_lenght))
            length = data_stream_lenght - index
        return data_stream[index:index + length]

    def process_line(self, query_object, line, line_number=0):
        err = None
        column_len = query_object['table'].column_count()
        line_cleaned = line.rstrip()
        line_data = None
        if query_object['table'].data.starts_on_line > line_number:
            line_type = self.data_type.COMMENT
            line_data = line
            #print query_object['table'].data.starts_on_line,line_number
        else:
            line_type = self.data_type.DATA
        if not line_cleaned:
            if True == query_object['table'].visible.whitespace:
                line_data = ['']
            line_type = self.data_type.WHITESPACE
        else:
            if line_cleaned[0] in query_object['table'].delimiters.comment:
                if True == query_object['table'].visible.comments:
                    line_data = [line_cleaned]
                line_type = self.data_type.COMMENT
            else:
                line_data = line_cleaned.split(query_object['table'].delimiters.field)
                cur_column_len = len(line_data)
                if cur_column_len != column_len:
                    if cur_column_len > column_len:
                        err = "Table {2}: Line #{0}, {1} extra Column(s)".format(line_number, cur_column_len - column_len, query_object['table'].data.name)
                    else:
                        err = "Table {2}: Line #{0}, missing {1} Column(s)".format(line_number, column_len - cur_column_len, query_object['table'].data.name)
                    # query_object['table'].add_error(err)
                    line_type = self.data_type.ERROR

                    # turn error into coment
                    if True == query_object['table'].visible.errors:
                        line_data = line_cleaned
                    else:
                        line_data = None
                    line_type = self.data_type.ERROR
                # fields are surrounded by something... trim
                #print self.table.delimiters.block_quote
                if None != query_object['table'].delimiters.block_quote:
                    line_data_cleaned = []
                    for d in line_data:
                        line_data_cleaned.append(d[1:-1])
                    line_data = line_data_cleaned

        # If no where. return everything
        if 'where' not in query_object['meta']:
            match_results = True
        else:
            # if a where, only return data, comments/whites/space/errors are ignored
            if line_type == self.data_type.DATA:
                match_results = evaluate_match(query_object['meta']['where'], line_data, query_object['table'])
            else:
                match_results = False
        if query_object['table'].visible.whitespace is False and line_type==self.data_type.WHITESPACE:
            match_results=False
        elif query_object['table'].visible.comments is False and line_type==self.data_type.COMMENT:
            match_results=False
        elif query_object['table'].visible.errors is False and line_type==self.data_type.ERROR:
            match_results=False


        # raw has rstrip for line.. maybe configuration option? Extra data anyway...
        return {'data': line_data, 'type': line_type, 'raw': line_cleaned, 'line_number': line_number, 'match': match_results, 'error': err}

    def select(self, query_object, parser):
        temp_data = []
        # if has columns, then it needs a table

        has_functions = False
        has_columns = False
        for c in query_object['meta']['select']:
            if 'function' in c:
                info("Has functions, doesnt need a table")
                has_functions = True
            if 'column' in c:
                info("Has columns, needs a table")
                has_columns = True
        if False == has_columns and 'from' in query_object['meta']:
            raise Exception("Invalid FROM, all columns are functions")

        # if has functions, tables may not be needed
        if True == has_columns:
            if 'from' in query_object['meta']:
                table_name = query_object['meta']['from']['table']
                query_object['table'] = self.database.get(table_name)
                if None == query_object['table']:
                    raise Exception("Table '{0}' does not exist.".format(table_name))
                table_columns = query_object['table'].get_columns()
                parser.expand_columns(query_object, table_columns)
                column_len = query_object['table'].column_count()
                if column_len == 0:
                    raise Exception("No defined columns in configuration")
            else:
                raise Exception("Missing FROM in select")

        temp_table = self.database.temp_table()
        for column in query_object['meta']['select']:
            display = None
            if 'display' in column:
                display = column['display']
                info("RENAME COLUMN", display)

            if 'column' in column:
                info("adding data column")
                temp_table.add_column(column['column'], display)
            if 'function' in column:
                info("adding function column")
                temp_table.add_column(column['function'], display)

        # TODO Columns with the same name can be renamed, but fail. Key issue?
        line_number = 1

        # create temp table structure
        # process file
        if True == has_columns:
            with open(query_object['table'].data.path, 'r') as content_file:
                for line in content_file:
                    processed_line = self.process_line(query_object, line, line_number)
                    if None != processed_line['error']:
                        temp_table.add_error(processed_line['error'])
                    line_number += 1

                    #print processed_line
                    if False == processed_line['match']:
                        continue

                    # add to temp table
                    if None != processed_line['data']:
                        restructured_line = self.process_select_row(query_object,processed_line) 
                        temp_data.append(restructured_line)

        # file is closed at this point

        if False == has_columns and True == has_functions:
            row=self.process_select_row(query_object,None)
            temp_data.append(row)


        if 'order by' in query_object['meta']:
            self.sort = []
            for c in query_object['meta']['order by']:
                ordinal = query_object['table'].get_ordinal_by_name(c['column'])
                direction = 1
                if 'asc' in c:
                    direction = 1
                elif 'desc' in c:
                    direction = -1
                self.sort.append([ordinal, direction])
            temp_data = sorted(temp_data, self.sort_cmp)
            #print temp_data

        limit_start = 0
        limit_length = None
        #print query_object['meta']
        # exit(1)

        if 'limit' in query_object['meta']:
            if 'start' in query_object['meta']['limit']:
                limit_start = query_object['meta']['limit']['start']
            if 'length' in query_object['meta']['limit']:
                limit_length = query_object['meta']['limit']['length']

        info("Limit:{0},Length:{1}".format(limit_start, limit_length))
        temp_table.results = self.limit(temp_data, limit_start, limit_length)
        return temp_table

    def process_select_row(self,query_object,processed_line):
        row=[]
        for c in query_object['meta']['select']:
            if 'column' in c:
                if None != processed_line:
                    row.append(query_object['table'].get_data_by_name(c['column'], processed_line['data']))
            elif 'function' in c:
                if c['function'] == 'database':
                    row.append(f_database(self.database))
                elif c['function'] == 'datetime':
                     row.append(f_datetime())
                elif c['function'] == 'date':
                     row.append(f_date())
                elif c['function'] == 'time':
                     row.append(f_time())
                elif c['function'] == 'version':
                     row.append(f_version(__version__))
                #elif c['function'] == 'lower':
                #     row.append(lower(c['column']))
                #elif c['function'] == 'upper':
                #     row.append(upper(c['column']))
                #elif c['function'] == 'cat':
                #     row.append(cat(c['arg1'],c['arg2']))
        if None != processed_line:                    
            line_type=processed_line['type']
            error= processed_line['error']
            raw= processed_line['raw']
        else:
            line_type=self.data_type.DATA
            error= None
            raw= None
        return {'data': row, 'type': line_type, 'error': error, 'raw': raw}



    def sort_cmp(self, x, y):

        for c in self.sort:
            ordinal = c[0]
            direction = c[1]

            #convert = lambda text: int(text) if text.isdigit() else text
            #alphanum_key = lambda key: [convert(c) for c in re.split('([0-9]+)', key)]

            # %print x[ordinal],y[ordinal],-1
            if x['data'][ordinal] == y['data'][ordinal]:
                continue

            if x['data'][ordinal] < y['data'][ordinal]:
                return -1 * direction
            else:
                return 1 * direction
        return 0

    # creates a tempfile
    # puts the raw original lines in temp file
    # ignores matches
    # File is as untouched as possible

    def delete(self, query_object):
        table_name = query_object['meta']['from']['table']
        query_object['table'] = self.database.get(table_name)
        if None == query_object['table']:
            raise Exception("Table '{0}' does not exist.".format(table_name))


        temp_table = self.database.temp_table()
        temp_table.add_column('deleted')

        temp_file_name = "DEL" + next(tempfile._get_candidate_names())
        line_number = 1
        deleted = 0
        # process file
        with open(query_object['table'].data.path, 'r') as content_file:
            with open(temp_file_name, 'w') as temp_file:
                for line in content_file:
                    processed_line = self.process_line(query_object, line, line_number)
                    if None != processed_line['error']:
                        temp_table.add_error(processed_line['error'])
                    line_number += 1
                    # skip matches
                    if True == processed_line['match']:
                        deleted += 1
                        continue
                    temp_file.write(processed_line['raw'])
                    temp_file.write(query_object['table'].delimiters.new_line)

        data = {'data': [deleted], 'type': self.data_type.DATA, 'error': None}
        temp_table.append_data(data)
        self.swap_files(query_object['table'].data.path, temp_file_name)
        return temp_table

    # creates a tempfile
    # puts the raw original lines in temp file
    # File is as untouched as possible
    # new lines are joined at the end

    def insert(self, query_object):
        table_name = query_object['meta']['into']['table']
        query_object['table'] = self.database.get(table_name)
        if None == query_object['table']:
            raise Exception("Table '{0}' does not exist.".format(table_name))

        temp_table = self.database.temp_table()
        temp_table.add_column('inserted')

        temp_file_name = "INS_" + next(tempfile._get_candidate_names())
        line_number = 1
        inserted = 0
        # process file
        requires_new_line = False
        
        with open(query_object['table'].data.path, 'r') as content_file:
            with open(temp_file_name, 'w') as temp_file:
                for line in content_file:
                    processed_line = self.process_line(query_object, line, line_number)
                    if None != processed_line['error']:
                        temp_table.add_error(processed_line['error'])
                    line_number += 1
                    temp_file.write(processed_line['raw'])
                    temp_file.write(query_object['table'].delimiters.new_line)

                    #if processed_line['raw'][-1] == query_object['table'].delimiters.new_line:
                    q
                    requires_new_line = False
                    #else:
                    #    requires_new_line = True

                results = self.create_single(query_object, temp_file, temp_table, requires_new_line)
                if True == results:
                    inserted += 1

        data = {'data': [inserted], 'type': self.data_type.DATA, 'error': None}
        temp_table.append_data(data)
        self.swap_files(query_object['table'].data.path, temp_file_name)

        return temp_table

    def create_single(self, query_object, temp_file, temp_table, requires_new_line):
        err = False
        ###
        # insert new data at end of file
        if len(query_object['meta']['columns']) != query_object['table'].column_count():
            temp_table.add_error("Cannot insert, column count does not match table column count")
        else:
            if len(query_object['meta']['values']) != query_object['table'].column_count():
                temp_table.add_error("Cannot insert, column value count does not match table column count")
            else:
                new_line = ''
                err = False
                #print query_object['meta']['columns']
                for c in range(0, len(query_object['meta']['columns'])):
                    column_name = query_object['table'].get_column_at_data_ordinal(c)
                    found = False
                    for c2 in range(0, len(query_object['meta']['columns'])):
                        if query_object['meta']['columns'][c2]['column'] == column_name:
                            #print("Column {} at table index {} located at query index {}".format(column_name,c, c2))
                            found = True
                            if c > 0:
                                new_line += '{}'.format(query_object['table'].delimiters.field)
                            new_line += '{}'.format(query_object['meta']['values'][c2]['value'])
                    if False == found:
                        temp_table.add_error("Cannot insert, column in query not found in table: {}".format(column_name))
                        err = True
                        break
                if False == err:
                    #print new_line
                    if True == requires_new_line:
                        temp_file.write(query_object['table'].delimiters.new_line)
                    temp_file.write(new_line)
                    temp_file.write(query_object['table'].delimiters.new_line)
        if False == err:
            return True
        else:
            return False

    def update_single(self, query_object, temp_file, temp_table, requires_new_line, processed_line):
        err = False
        ###
        # insert new data at end of file
        new_line = ''
        err = False
        #print query_object

        # make sure the inserted columns exist
        for c2 in range(0, len(query_object['meta']['set'])):
            column_name = query_object['meta']['set'][c2]['column']
            if None == query_object['table'].get_column_by_name(column_name):
                temp_table.add_error("column in update statement does not exist in table: {}".format(column_name))
                #print "no column"
                err = True

        if False == err:
            for c in range(0, query_object['table'].column_count()):
                column_name = query_object['table'].get_column_at_data_ordinal(c)
                value = processed_line['data'][c]
                for c2 in range(0, len(query_object['meta']['set'])):
                    #print column_name,query_object['meta']['set']
                    if query_object['meta']['set'][c2]['column'] == column_name:
                        #print("Column {} at table index {} located at query index {}".format(column_name,c, c2))
                        value = query_object['meta']['set'][c2]['expression']
                if c > 0:
                    new_line += '{}'.format(query_object['table'].delimiters.field)
                new_line += '{}'.format(value)

        if False == err:
            #print new_line
            if True == requires_new_line:
                temp_file.write(query_object['table'].delimiters.new_line)
            temp_file.write(new_line)
            temp_file.write(query_object['table'].delimiters.new_line)
        if False == err:
            return True
        else:
            return False

    # creates a tempfile
    # puts the raw original lines in temp file
    # ignores matches
    # File is as untouched as possible

    def update(self, query_object):
        table_name = query_object['meta']['update']['table']
        query_object['table'] = self.database.get(table_name)
        if None == query_object['table']:
            raise Exception("Table '{0}' does not exist.".format(table_name))


        temp_table = self.database.temp_table()
        temp_table.add_column('updated')

        temp_file_name = "UP_" + next(tempfile._get_candidate_names())
        line_number = 1
        updated = 0
        # process file
        with open(query_object['table'].data.path, 'r') as content_file:
            with open(temp_file_name, 'w') as temp_file:
                for line in content_file:
                    processed_line = self.process_line(query_object, line, line_number)
                    if None != processed_line['error']:
                        temp_table.add_error(processed_line['error'])
                    line_number += 1
                    # skip matches
                    if True == processed_line['match']:
                        results = self.update_single(query_object, temp_file, temp_table, False, processed_line)
                        if True == results:
                            updated += 1
                        continue
                    temp_file.write(processed_line['raw'])
                    temp_file.write(query_object['table'].delimiters.new_line)
        data = {'data': [updated], 'type': self.data_type.DATA, 'error': None}

        temp_table.append_data(data)
        self.swap_files(query_object['table'].data.path, temp_file_name)

        return temp_table

    def swap_files(self, target, temp):
        os.remove(target)
        if os.path.exists(target):
            raise Exception("Deleting target file {} failed".format(target))
        os.rename(temp, target)
        if os.path.exists(temp):
            raise Exception("Renaming temp file {} failed".format(temp))

    def use(self, query_object):
        info("Use")
        target_db = query_object['meta']['use']['table']
        self.database.set_database(target_db)
        temp_table = self.database.temp_table()
        temp_table.add_column('changed_db')
        data = {'data': [target_db], 'type': self.data_type.DATA, 'error': None}
        temp_table.append_data(data)
        return temp_table

    def create_table(self, query_object):
        info("Create Table")
        temp_table = self.database.temp_table()

        columns = []
        if 'columns' not in  query_object['meta'] :
            raise Exception ("Missing columns, cannot create table")

        for c in query_object['meta']['columns']:
            columns.append(c['column'])
        info("Columns to create", columns)
        created = 0
        found_delimiter=None
        found_comments=None
        found_whitespace=None
        found_data_on=None
        found_errors=None
        if 'delimiter' in query_object['meta']:
            found_delimiter= query_object['meta']['delimiter']['field']
        if 'whitespace' in query_object['meta']:
            found_whitespace= query_object['meta']['whitespace']['whitespace']
        if 'comments' in query_object['meta']:
            found_comments= query_object['meta']['comments']['comments']
        if 'errors' in query_object['meta']:
            found_errors= query_object['meta']['errors']['errors']
        if 'data_starts_on' in query_object['meta']:
            found_data_on= query_object['meta']['data_starts_on']['data_starts_on']
    
        results = self.database.create_table(table_name=query_object['meta']['create']['table'],
                                             columns=columns,
                                             data_file=query_object['meta']['file']['file'],
                                             delimiter=found_delimiter,
                                             comments=found_comments,
                                             errors=found_errors,
                                             whitespace=found_whitespace,
                                             data_on=found_data_on
                                             )
        if True == results:
            created += 1

        temp_table.add_column('create table')
        data = {'data': [created], 'type': self.data_type.DATA, 'error': None}
        temp_table.append_data(data)
        return temp_table

    def drop_table(self, query_object):
        info("Drop Table")
        temp_table = self.database.temp_table()
        #print "dropping",parser.query_object['meta']['drop']['table']
        dropped = 0
        results = self.database.drop_table(table_name=query_object['meta']['drop']['table'])
        if True == results:
            dropped += 1

        temp_table.add_column('dropped')
        data = {'data': [dropped], 'type': self.data_type.DATA, 'error': None}
        temp_table.append_data(data)
        return temp_table

    def update_table(self, query_object):
        info("Update Table")
        temp_table = self.database.temp_table()

        columns = None  
        if 'columns'  in  query_object['meta'] :
            columns = []
            for c in query_object['meta']['columns']:
                columns.append(c['column'])
        
        table_name=query_object['meta']['update']['table']

        updated = 0
        found_delimiter=None
        found_comments=None
        found_whitespace=None
        found_data_on=None
        found_file=None
        found_errors=None
        
        if 'delimiter' in query_object['meta']:
            found_delimiter= query_object['meta']['delimiter']['field']
        if 'whitespace' in query_object['meta']:
            found_whitespace= query_object['meta']['whitespace']['whitespace']
        if 'comments' in query_object['meta']:
            found_comments= query_object['meta']['comments']['comments']
        if 'errors' in query_object['meta']:
            found_errors= query_object['meta']['errors']['errors']
        if 'data_starts_on' in query_object['meta']:
            found_data_on= query_object['meta']['data_starts_on']['data_starts_on']
        if 'file' in query_object['meta']:
            found_file=query_object['meta']['file']['file']

        target_table= self.database.get(table_name)
        target_table.update(columns=columns,
                            data_file=found_file,
                            field_delimiter=found_delimiter,
                            comments=found_comments,
                            whitespace=found_whitespace,
                            errors=found_errors,
                            data_on=found_data_on)
        #sace the update to the table
        target_table.save()
        updated=1

        temp_table.add_column('update table')
        data = {'data': [updated], 'type': self.data_type.DATA, 'error': None}
        temp_table.append_data(data)
        return temp_table


    def describe_table(self, query_object):
        info("Describe Table")
        temp_table = self.database.temp_table()
        table_name=query_object['meta']['describe']['table']
        target_table= self.database.get(table_name)
        temp_table.add_column('option')
        temp_table.add_column('value')
        
        
        temp_table.append_data({'data':['active',target_table.active], 'type': self.data_type.DATA, 'error': None})
        temp_table.append_data({'data':['table_name',target_table.data.name], 'type': self.data_type.DATA, 'error': None})
        temp_table.append_data({'data':['database',target_table.data.database], 'type': self.data_type.DATA, 'error': None})
        temp_table.append_data({'data':['data_file',target_table.data.path], 'type': self.data_type.DATA, 'error': None})
        temp_table.append_data({'data':['type',target_table.data.type], 'type': self.data_type.DATA, 'error': None})
        temp_table.append_data({'data':['config_file',target_table.data.config], 'type': self.data_type.DATA, 'error': None})
        temp_table.append_data({'data':['data_starts_on',target_table.data.starts_on_line], 'type': self.data_type.DATA, 'error': None})
        temp_table.append_data({'data':['field_delimiter'  ,target_table.delimiters.field], 'type': self.data_type.DATA, 'error': None})
        temp_table.append_data({'data':['comments_visible',target_table.visible.comments], 'type': self.data_type.DATA, 'error': None})
        temp_table.append_data({'data':['errors_visible',target_table.visible.errors], 'type': self.data_type.DATA, 'error': None})
        temp_table.append_data({'data':['whitespace_visible',target_table.visible.whitespace], 'type': self.data_type.DATA, 'error': None})
        return temp_table



# ################################################################################
#
# CLI
#
# ################################################################################



def cli_main():


    parser = argparse.ArgumentParser("ddb", usage='%(prog)s [options]', description="""flat file database access
                    """, epilog="And that's how you ddb")

    # actions
    parser.add_argument('-v', '--debug', help='show debuging statistics', action='store_true')
    parser.add_argument('-c', '--config', help='yaml configuration file')
    parser.add_argument('-o', '--output', help='output type (raw,json,yaml,xml|bash,term) defaults to "term"', default= 'term')
    parser.add_argument('-f', '--file', help='output file (if nothing, output is redirected to stdio)', default= None)
    parser.add_argument('query', help='query to return data', nargs= "?")

    args = parser.parse_args()
    
    # set the config q
    # file location
    if args.config is not None:
        config_file = args.config
    else:
        home = expanduser("~")
        config_file = os.path.join(os.path.join(home, '.ddb'), 'ddb.conf')
    
    if args.query is not None:
        e = sql_engine( config_file=config_file, 
                        debug=args.debug, 
                        mode="full",
                        output=args.output,
                        output_file=args.file)
        results = e.query(args.query)
        e.format_output(results)

    else:
        # interactive session
        prompt = ddbPrompt()
        prompt.set_vars(config_file=config_file,
                        debug=args.debug)
        prompt.cmdloop_with_keyboard_interrupt()


if __name__ == "__main__":
    cli_main()
