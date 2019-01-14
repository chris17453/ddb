
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
