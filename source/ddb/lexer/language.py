# cython: linetrace=True

#  name: "name"
#  segments: signature to match against 
#     arguments: optional, 1 or 0 for unlimited (comma seperated)
#     data: optional
#          vars: variabls to manually set
#          signature: signaturenature to match, {viariable} places any data in that position into that variable, ** array not supported yet[ ] 
#                 makes it an array plain strings are dropped, "$" classifies it as an internal variable of that name, : will store in alternate variable location
#     name: initial string to match against to enter this name, this is the index of the object
#     optional: can we skip this
#     key: override name key
#     depends_on: do not match unless the other variable is present in same scope . will drop to root scope
#     jump: goto an ealier command for matching, to repeat a loop set for multiple matches
#     parent: override the name, and place data on this index
#     store_array: allow multiple keys in an array at this index
#     specs :{'variable_name': {'type': 'int', 'default': 1, values:[1,2]} }, # values contains must match possible values
#     no_keyword:True ...?

language={'commands': [{'name': 'show columns',
               'segments': [{'data': [{'signature': ['show', 'columns']}],
                             'name': 'show columns'},
                            {'data': [{'signature': ['from', '{table}']},
                                      {'signature': ['from',
                                               '{database}',
                                               '.',
                                               '{table}']}],
                             'name': 'source'}]},
              {'name': 'show tables',
               'segments': [{'data': [{'signature': ['show', 'tables']}],
                             'name': 'show tables'}]},
              {'name': 'show variables',
               'segments': [{'data': [{'signature': ['show', 'variables']}],
                             'name': 'show variables'}]},
              {'name': 'select',
              'vars':{'table':None },
               'segments': [{'data': [{'signature': ['select']}],
                             'name': 'select',
                             'optional': False},
                            {'data': [{'signature': ['distinct']}],
                             'name': 'distinct',
                             'optional': True},
                            {'arguments': 0,
                             'data': [{'signature': ['{column}']},
                                      {'signature': ['{column}',
                                               'as',
                                               '{display}']},
                                      {'signature': ['{function}', '(', ')']},
                                      {'signature': ['{function}',
                                               '(',
                                               '{argument1}',
                                               ')']},
                                      {'signature': ['{function}',
                                               '(',
                                               '{argument1}',
                                               ',',
                                               '{argument2}',
                                               ')']},
                                      {'signature': ['{function}',
                                               '(',
                                               '{argument1}',
                                               ',',
                                               '{argument2}',
                                               ',',
                                               '{argument3}',
                                               ')']},
                                      {'signature': ['{function}',
                                               '(',
                                               ')',
                                               'as',
                                               '{display}']},
                                      {'signature': ['{function}',
                                               '(',
                                               '{argument1}',
                                               ')',
                                               'as',
                                               '{display}']},
                                      {'signature': ['{function}',
                                               '(',
                                               '{argument1}',
                                               ',',
                                               '{argument2}',
                                               ')',
                                               'as',
                                               '{display}']},
                                      {'signature': ['{function}',
                                               '(',
                                               '{argument1}',
                                               ',',
                                               '{argument2}',
                                               ',',
                                               '{argument3}',
                                               ')',
                                               'as',
                                               '{display}']}],
                             'depends_on': 'select',
                             'name': 'columns',
                             },
                            {'data': [{'signature': ['from', '{table}']},
                                      {'signature': ['from',
                                               '{table}',
                                               'as',
                                               '{display}']},
                                      {'signature': ['from',
                                               '{database}',
                                               '.',
                                               '{table}']},
                                      {'signature': ['from',
                                               '{database}',
                                               '.',
                                               '{table}',
                                               'as',
                                               '{display}']}],
                             'name': 'source',
                             'optional': True},

                            {'data': [
                                {'signature': ['where','{e1}','$operators:c','{e2}'] ,'vars':{'condition':'where'}} ] ,
                             'depends_on': 'source',
                             'name': 'where',
                             'optional': True,
                             'store_array': True},
                            {'data': [{'signature': ['and','{e1}','$operators:c','{e2}'] ,'vars':{'condition':'and'}} ] ,
                             'depends_on': 'where',
                             'jump': 'where',
                             'name': 'and',
                             'optional': True,
                             'parent': 'where'},
                            {'data': [{'signature': ['or','{e1}','$operators:c','{e2}'] ,'vars':{'condition':'or'}} ] ,
                             'depends_on': 'where',
                             'jump': 'where',
                             'name': 'or',
                             'optional': True,
                             'parent': 'where'},
                           
                           #  {'array': True,
                           # 'data': [{'signature': ['union']}],
                           #  'jump': 'select',
                           #  'name': 'union',
                           #  'optional': True},
                       
                            {'data': [{'signature': ['group', 'by']}],
                             'name': 'group by header',
                             'optional': True},
                            {'arguments': 0,
                             'data': [{'signature': ['{column}']}],
                             'name': 'group by',
                             'depends_on':'group by header',
                             'optional': True},
                            {'data': [{'signature': ['order', 'by']}],
                             'name': 'order by header',
                             'optional': True},
                            {'arguments': 0,
                             'data': [
                                      {'signature': ['{column}'],
                                       'vars': {'direction': 1}},
                                      {'signature': ['{column}', 'asc'],
                                       'vars': {'direction': 1}},
                                      {'signature': ['{column}', 'desc'],
                                       'vars': {'direction': -1}}],
                             'name': 'order by',
                             'depends_on':'order by header',
                             'optional': True},
                            {'data': [{'signature': ['limit', '{length}']},
                                      {'signature': ['limit',
                                               '{start}',
                                               ',',
                                               '{length}']}],
                             'name': 'limit',
                             'optional': True,
                             'specs': {'length': {'default': 0,
                                                  'type': 'int'},
                                       'start': {'default': 0,
                                                 'type': 'int'}}}]},
              {'name': 'set',
               'segments': [{'data':[{'signature':['set']}],
                            'name':'set header',
                            'optional':True
                            },
                            {'name':'set header',
                             'optional':True,
                             'data': [{'signature': ['set']}],},


                            {'arguments': 0,
                             'data': [{'signature': ['{variable}',
                                               '=',
                                               '{value}'],
                                       'vars': {'type': 'all'}}],
                             'name': 'set',
                             'optional':True,
                             'depends_on':'set header'}]},
              {'name': 'create procedure',
               'segments': [{'arguments': None,
                             'data': [{'signature': ['create',
                                               'procedure',
                                               '(']}],
                             'dispose': True,
                             'name': 'create procedure',
                             'optional': False},
                            {'arguments': 0,
                             'data': [{'signature': ['{parameter}']}],
                             'name': 'parameters',
                             'optional': True},
                            {'data': [{'signature': [')']}],
                             'dispose': True,
                             'name': ')',
                             'optional': False}]},
              {'name': 'delimiter',
               'segments': [{'data': [{'signature': ['delimiter',
                                               '{delimiter}']}],
                             'name': 'delimiter'}]},
              {'name': 'end',
               'segments': [{'data': [{'signature': ['end']}], 'name': 'end'}]},
              {'name': 'begin',
               'segments': [    {'data': [{'signature': ['begin']}], 
                                 'name': 'begin'}]},
              {'name': 'commit', 
                    'segments': [
                                {
                                'data': [{'signature': ['commit']}],
                                'name': 'commit'}
                                ]
              },
              {'name': 'rollback',
               'segments': [{'data': [{'signature': ['rollback']}],
                             'name': 'rollback'}]},
              {'name': 'show output modules',
               'segments': [{'data': [{'signature': ['show',
                                               'output',
                                               'modules']}],
                             'name': 'show output modules'}]},
              {'name': 'delete',
               'segments': [{'data': [{'signature': ['delete']}],
                             'name': 'delete'},
                            {'data': [{'signature': ['from', '{table}']},
                                      {'signature': ['from',
                                               '{database}',
                                               '.',
                                               '{table}']}],
                             'name': 'source'},
                            {'data': [{'signature': ['where','{e1}','$operators:c','{e2}'] , 'vars':{ 'condition':'where' }} ] ,
                             'name': 'where',
                             'optional': True,
                             'store_array': True},
                            {'data': [{'signature': ['and','{e1}','$operators:c','{e2}'] , 'vars':{ 'condition':'and' } } ] ,
                             'depends_on': 'where',
                             'jump': 'where',
                             'name': 'and',
                             'optional': True,
                             'parent': 'where'
                             },
                            {'data': [{'signature': ['or','{e1}','$operators:c','{e2}']  , 'vars':{ 'condition':'or' }} ] ,
                             'depends_on': 'where',
                             'jump': 'where',
                             'name': 'or',
                             'optional': True,
                             'parent': 'where'}]},
              {'name': 'insert',
               'segments': [{'data': [{'signature': ['insert']}],
                             'name': 'insert'},
                            {'data': [{'signature': ['into', '{table}']},
                                      {'signature': ['into',
                                               '{database}',
                                               '.',
                                               '{table}']}],
                             'name': 'source'},
                            {'data': [{'signature': ['(']}],
                             'dispose': True,
                             'name': '('},
                            {'arguments': 0,
                             'data': [{'signature': ['{column}']}],
                             'name': 'columns',
                             },
                            {'data': [{'signature': [')']}],
                             'dispose': True,
                             'name': ')'},
                            {'data': [{'signature': ['values']}],
                             'dispose': True,
                             'name': 'values'},
                            {'data': [{'signature': ['(']}],
                             'dispose': True,
                             'name': '('},
                            
                            {'arguments': 0,
                             'data': [{'signature': ['{value}']}],
                             'name': 'values',
                             },
                            {'data': [{'signature': [')']}],
                             'dispose': True,
                             'name': ')'}]},
              {'name': 'update',
               'segments': [{'data': [{'signature': ['update', '{table}']},
                                      {'signature': ['update',
                                               '{database}',
                                               '.',
                                               '{table}']}],
                            'name': 'source'},
                            {'name':'set header',
                             'data': [{'signature': ['set']}],},
                            {'arguments': 0,
                             'data': [{'signature': ['{column}',
                                               '=',
                                               '{expression}']}],
                             'name': 'set',
                             'depends_on':'set header'},
                            {'data': [{'signature': ['where','{e1}','$operators:c','{e2}'] ,'vars':{'condition':'where'}} ] ,
                             'name': 'where',
                             'optional': True,
                             'store_array': True},
                            {'data': [{'signature': ['and','{e1}','$operators:c','{e2}'] ,'vars':{'condition':'and'}} ] ,
                             'depends_on': 'where',
                             'jump': 'where',
                             'name': 'and',
                             'optional': True,
                             'parent': 'where'},
                            {'data': [{'signature': ['or','{e1}','$operators:c','{e2}'] ,'vars':{'condition':'or'}} ] ,
                             'depends_on': 'where',
                             'jump': 'where',
                             'name': 'or',
                             'optional': True,
                             'parent': 'where'}]},
              {'name': 'upsert',
               'segments': [{'data': [{'signature': ['upsert']}],
                             'name': 'upsert'},
                            {'data': [{'signature': ['into', '{table}']},
                                      {'signature': ['into',
                                               '{database}',
                                               '.',
                                               '{table}']}],
                             'name': 'source'},
                            {'data': [{'signature': ['(']}],
                             'dispose': True,
                             'name': '('},
                            {'arguments': 0,
                             'data': [{'signature': ['{column}']}],
                             'name': 'columns',
                             },
                            {'data': [{'signature': [')']}],
                             'dispose': True,
                             'name': ')'},
                            {'data': [{'signature': ['values']}],
                             'dispose': True,
                             'name': 'values'},
                            {'data': [{'signature': ['(']}],
                             'dispose': True,
                             'name': '('},
                            {'arguments': 0,
                             'data': [{'signature': ['{value}']}],
                             'name': 'values',
                             },
                            {'data': [{'signature': [')']}],
                             'dispose': True,
                             'name': ')'},
                            {
                             'data': [{'signature': ['on', 'duplicate', 'key']}],
                             'name': 'on duplicate key header',
                             },
                            {'arguments': 0,
                             'data': [{'signature': ['{column}']}],
                             'name': 'on duplicate key',
                             'depends_on':'on duplicate key header'},
                            {
                             'data': [{'signature': ['update']}],
                             'key':'set',
                             'name':'update header'
                             },
                            {'arguments': 0,
                             'data': [{'signature': ['{column}',
                                               '=',
                                               '{expression}']}],
                             'key': 'set',
                             'name': 'update',
                             'depends_on':'set'
                             
                             }]},
              {'name': 'use table',
               'segments': [{'data': [{'signature': ['use',
                                               '{table}']},
                                      {'signature': ['use',
                                               '{database}',
                                               '.',
                                               '{table}']}],
                             'name': 'source'}]},
              {'name': 'drop table',
               'segments': [{'data': [{'signature': ['drop',
                                               'table',
                                               '{table}']},
                                      {'signature': ['drop',
                                               'table',
                                               '{database}',
                                               '.',
                                               '{table}']}],
                             'name': 'source'}]},
              {'name': 'create table',
               'segments': [{'data': [{'signature': ['create']}],
                             'name': 'create',
                             'optional': False},
                            {'data': [{'signature': ['temporary']}],
                             'name': 'temporary',
                             'optional': True},
                            {'data': [{'signature': ['table', '{table}']},
                                      {'signature': ['table',
                                               '{database}',
                                               '.',
                                               '{table}']}],
                             'name': 'source',
                             'optional': False,
                             'type': 'single'},
                            {'data': [{'signature': ['(']}],
                             'dispose': True,
                             'name': '('},
                            {'arguments': 0,
                             'data': [{'signature': ['{column}']}],
                             'name': 'columns',
                             },
                            {'data': [{'signature': [')']}],
                             'dispose': True,
                             'name': ')'},
                            {'data': [{'signature': ['file', '=', '{file}']}],
                             'name': 'file',
                             'type': 'single'},
                            {'data': [{'signature': ['fifo', '=', '{fifo}']}],
                             'name': 'fifo',
                             'optional': True,
                             'type': 'single'},
                            {'data': [{'signature': ['repo',
                                               '=',
                                               '{protocol}',
                                               'url',
                                               '=',
                                               '{url}',
                                               'user',
                                               '=',
                                               '{user}',
                                               'password',
                                               '=',
                                               '{password}',
                                               'repo_dir',
                                               '=',
                                               '{directory}',
                                               'repo_file',
                                               '=',
                                               '{file}']}],
                             'specs': {'protocol': {'default': 'svn','type': 'string','values':['svn','git']}},
                             'name': 'repo',
                             'optional': True,
                             'type': 'single'},
                            {'data': [{'signature': ['mode',
                                               '=',
                                               '{mode}']}],
                             'name': 'mode',
                             'optional': True,
                             'specs': {'mode': {'default': 'delimited','type': 'string','values':['delimited','ini']}},
                             'type': 'single'},
                            {'data': [{'signature': ['delimiter',
                                               '=',
                                               '{delimiter}']}],
                             'name': 'delimiter',
                             'optional': True,
                             'specs': {'delimiter': {'default': ',',
                                                 'type': 'char'}},
                             'type': 'single'},
                            {'data': [{'signature': ['whitespace',
                                               '=',
                                               '{whitespace}']}],
                             'name': 'whitespace',
                             'optional': True,
                             'specs': {'whitespace': {'type': 'bool'}},
                             'type': 'single'},
                            {'data': [{'signature': ['errors',
                                               '=',
                                               '{errors}']}],
                             'name': 'errors',
                             'optional': True,
                             'specs': {'errors': {'type': 'bool'}},
                             'type': 'single'},
                            {'data': [{'signature': ['comments',
                                               '=',
                                               '{comments}']}],
                             'name': 'comments',
                             'optional': True,
                             'specs': {'comments': {'type': 'bool','default': None}},
                             'type': 'single'},
                            {'data': [{'signature': ['strict',
                                               '=',
                                               '{strict}']}],
                             'name': 'strict',
                             'optional': True,
                             'specs': {'strict': {'type': 'bool','default': True}},
                             'type': 'single'},
                            {'data': [{'signature': ['data_starts_on',
                                               '=',
                                               '{data_starts_on}']}],
                             'name': 'data_starts_on',
                             'optional': True,
                             'specs': {'data_starts_on': {'default': 1,
                                                          'type': 'int'}},
                             'type': 'single'}]},
              {'name': 'update table',
               'segments': [{'data': [{'signature': ['update',
                                               'table',
                                               '{table}']},
                                      {'signature': ['update',
                                               'table',
                                               '{database}',
                                               '.',
                                               '{table}']}],
                             'name': 'source'},
                            {'data': [{'signature': ['(']}],
                             'dispose': True,
                             'name': '(',
                             'optional': True},
                            {'arguments': 0,
                             'data': [{'signature': ['{column}']}],
                             'depends_on': '(',
                             'name': 'columns',
                             'optional': True},
                            {'data': [{'signature': [')']}],
                             'depends_on': '(',
                             'dispose': True,
                             'name': ')',
                             'optional': True},
                            {'data': [{'signature': ['file', '=', '{file}']}],
                             'name': 'file',
                             'optional': True},
                            {'data': [{'signature': ['delimiter',
                                               '=',
                                               '{field}']}],
                             'name': 'delimiter',
                             'optional': True,
                             'specs': {'field': {'default': ',',
                                                 'type': 'char'}}},
                            {'data': [{'signature': ['whitespace',
                                               '=',
                                               '{whitespace}']}],
                             'name': 'whitespace',
                             'optional': True,
                             'specs': {'whitespace': {'type': 'bool'}}},
                            {'data': [{'signature': ['errors',
                                               '=',
                                               '{errors}']}],
                             'name': 'errors',
                             'optional': True,
                             'specs': {'errors': {'type': 'bool'}}},
                            {'data': [{'signature': ['comments',
                                               '=',
                                               '{comments}']}],
                             'name': 'comments',
                             'optional': True,
                             'specs': {'comments': {'type': 'bool'}}},
                            {'data': [{'signature': ['data_starts_on',
                                               '=',
                                               '{data_starts_on}']}],
                             'name': 'data_starts_on',
                             'optional': True,
                             'specs': {'data_starts_on': {'type': 'int'}}}]},
              {'name': 'describe table',
               'segments': [{'data': [{'signature': ['describe',
                                               'table',
                                               '{table}']},
                                      {'signature': ['describe',
                                               'table',
                                               '{database}',
                                               '.',
                                               '{table}']}],
                             'name': 'source'}]}
                             ],
'operators':['>','<','>=','<=','!=','<>','not','is','like','=','in'],
'functions': [{'arguments': None, 'name': 'database'},
               {'arguments': None, 'name': 'row_number'},
               {'arguments': [{'name': 'where', 'required': True}],
                'name': 'count'},
               {'arguments': [{'name': 'column', 'required': True}],
                'name': 'sum'},
               {'arguments': None, 'name': 'version'},
               {'arguments': [{'name': 'column', 'required': True}],
                'name': 'upper'},
               {'arguments': [{'name': 'column', 'required': True}],
                'name': 'lower'},
               {'arguments': [{'name': 'arg1', 'required': True},
                              {'name': 'arg2', 'required': True}],
                'name': 'cat'},
               {'arguments': None, 'name': 'date'},
               {'arguments': None, 'name': 'time'},
               {'arguments': None, 'name': 'datetime'}]}


#     {'data': [{'signature': ['join', '{table}']},
#                                      {'signature': ['join',
#                                               '{table}',
#                                               'as',
#                                               '{display}']}],
#                             'depends_on': 'from_',
#                             'name': 'join',
#                             'optional': True},
#                            {'data': [{'signature': ['left join', '{table}']},
#                                      {'signature': ['left join',
#                                               '{table}',
#                                               'as',
#                                               '{display}']}],
#                             'depends_on': 'from_',
#                             'name': 'left join',
#                             'optional': True},
#                            {'data': [{'signature': ['right join', '{table}']},
#                                      {'signature': ['right join',
#                                               '{table}',
#                                               'as',
#                                               '{display}']}],
#                             'depends_on': 'from_',
#                             'name': 'right join',
#                             'optional': True},
#                            {'data': [{'signature': ['full join', '{table}']},
#                                      {'signature': ['full join',
#                                               '{table}',
#                                               'as',
#                                               '{display}']}],
#                             'depends_on': 'from_',order
#                             'name': 'full join',
#                             'optional': True},
#                            {'data': [{'signature': ['on','{e1}','$operators:c','{e2}'] } ] ,
#                             'depends_on': 'join',
#                             'name': 'on',
#                             'optional': True,
#                             'store_array': True},
#                             {'data': [{'signature': ['and','{e1}','$operators:c','{e2}'] } ] ,
#                             'depends_on': 'on',
#                             'jump': 'on',
#                             'name': 'and',
#                             'optional': True,
#                             'parent': 'on'},
#                            {'data': [{'signature': ['or','{e1}','$operators:c','{e2}'] } ] ,
#                             'depends_on': 'on',
#                             'jump': 'on',
#                             'name': 'or',
#                             'optional': True,
#                             'parent': 'on'},
#                           
#                             
#
