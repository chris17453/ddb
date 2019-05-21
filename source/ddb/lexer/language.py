

#  name: "name"
#  segments: signatures to match against 
#     arguments: optional, 1 or 0 for unlimited (comma seperated)
#     data: optional
#          vars: variabls to manually set
#          sig: signature to match, {viariable} places any data in that position into that variable, ** array not supported yet[ ] 
#                 makes it an array plain strings are dropped, "$" classifies it as an internal variable of that name, : will store in alternate variable location
#     name: initial string to match against to enter this name, this is the index of the object
#     optional: can we skip this
#     key: override name key
#     depends_on: do not match unless the other variable is present in same scope . will drop to root scope
#     jump: goto an ealier command for matching, to repeat a loop set for multiple matches
#     parent: override the name, and place data on this index
#     store_array: allow multiple keys in an array at this index
#     specs :{'variable_name': {'type': 'int', 'default': 0} },
#     no_keyword:True ...?

language={'commands': [{'name': 'show columns',
               'segments': [{'data': [{'sig': ['show', 'columns']}],
                             'name': ['show', 'columns']},
                            {'data': [{'sig': ['from', '{table}']},
                                      {'sig': ['from',
                                               '{database}',
                                               '.',
                                               '{table}']}],
                             'name': 'from'}]},
              {'name': 'show tables',
               'segments': [{'data': [{'sig': ['show', 'tables']}],
                             'name': ['show', 'tables']}]},
              {'name': 'show variables',
               'segments': [{'data': [{'sig': ['show', 'variables']}],
                             'name': ['show', 'variables']}]},
              {'name': 'select',
               'segments': [{'data': [{'sig': ['select']}],
                             'name': 'select',
                             'optional': False},
                            {'data': [{'sig': ['distinct']}],
                             'name': 'distinct',
                             'optional': True},
                            {'arguments': 0,
                             'data': [{'sig': ['{column}']},
                                      {'sig': ['{column}',
                                               'as',
                                               '{display}']},
                                      {'sig': ['{function}', '(', ')']},
                                      {'sig': ['{function}',
                                               '(',
                                               '{argument1}',
                                               ')']},
                                      {'sig': ['{function}',
                                               '(',
                                               '{argument1}',
                                               ',',
                                               '{argument2}',
                                               ')']},
                                      {'sig': ['{function}',
                                               '(',
                                               '{argument1}',
                                               ',',
                                               '{argument2}',
                                               ',',
                                               '{argument3}',
                                               ')']},
                                      {'sig': ['{function}',
                                               '(',
                                               ')',
                                               'as',
                                               '{display}']},
                                      {'sig': ['{function}',
                                               '(',
                                               '{argument1}',
                                               ')',
                                               'as',
                                               '{display}']},
                                      {'sig': ['{function}',
                                               '(',
                                               '{argument1}',
                                               ',',
                                               '{argument2}',
                                               ')',
                                               'as',
                                               '{display}']},
                                      {'sig': ['{function}',
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
                             'no_keyword': True},
                            {'data': [{'sig': ['from', '{table}']},
                                      {'sig': ['from',
                                               '{table}',
                                               'as',
                                               '{display}']},
                                      {'sig': ['from',
                                               '{database}',
                                               '.',
                                               '{table}']},
                                      {'sig': ['from',
                                               '{database}',
                                               '.',
                                               '{table}',
                                               'as',
                                               '{display}']}],
                             'name': 'from',
                             'optional': True},
                            {'data': [{'sig': ['join', '{table}']},
                                      {'sig': ['join',
                                               '{table}',
                                               'as',
                                               '{display}']}],
                             'depends_on': 'from',
                             'name': 'join',
                             'optional': True},
                            {'data': [{'sig': ['left join', '{table}']},
                                      {'sig': ['left join',
                                               '{table}',
                                               'as',
                                               '{display}']}],
                             'depends_on': 'from',
                             'name': 'left join',
                             'optional': True},
                            {'data': [{'sig': ['right join', '{table}']},
                                      {'sig': ['right join',
                                               '{table}',
                                               'as',
                                               '{display}']}],
                             'depends_on': 'from',
                             'name': 'right join',
                             'optional': True},
                            {'data': [{'sig': ['full join', '{table}']},
                                      {'sig': ['full join',
                                               '{table}',
                                               'as',
                                               '{display}']}],
                             'depends_on': 'from',
                             'name': 'full join',
                             'optional': True},
                            {'data': [{'sig': ['on','{e1}','$operators:c','{e2}'] } ] ,
                             'depends_on': 'join',
                             'name': 'on',
                             'optional': True,
                             'store_array': True},
                             {'data': [{'sig': ['and','{e1}','$operators:c','{e2}'] } ] ,
                             'depends_on': 'on',
                             'jump': 'on',
                             'name': 'and',
                             'optional': True,
                             'parent': 'on'},
                            {'data': [{'sig': ['or','{e1}','$operators:c','{e2}'] } ] ,
                             'depends_on': 'on',
                             'jump': 'on',
                             'name': 'or',
                             'optional': True,
                             'parent': 'on'},
                            {'data': [{'sig': ['where','{e1}','$operators:c','{e2}'] } ] ,
                             'depends_on': 'from',
                             'name': 'where',
                             'optional': True,
                             'store_array': True},
                            {'data': [{'sig': ['and','{e1}','$operators:c','{e2}'] } ] ,
                             'depends_on': 'where',
                             'jump': 'where',
                             'name': 'and',
                             'optional': True,
                             'parent': 'where'},
                            {'data': [{'sig': ['or','{e1}','$operators:c','{e2}'] } ] ,
                             'depends_on': 'where',
                             'jump': 'where',
                             'name': 'or',
                             'optional': True,
                             'parent': 'where'},
                            {'array': True,
                             'data': [{'sig': ['union']}],
                             'jump': 'select',
                             'name': 'union',
                             'optional': True},
                            {'data': [{'sig': ['group', 'by']}],
                             'name': 'group by header',
                             'optional': True},
                            {'arguments': 0,
                             'data': [{'sig': ['{column}']}],
                             'name': 'group by',
                             'depends_on':'group by header',
                             'optional': True},
                            {'data': [{'sig': ['order', 'by']}],
                             'name': 'order by header',
                             'optional': True},
                            {'arguments': 0,
                             'data': [{'sig': ['{column}']},
                                      {'sig': ['{column}', 'asc'],
                                       'vars': {'direction': 1}},
                                      {'sig': ['{column}', 'desc'],
                                       'vars': {'direction': -1}}],
                             'name': 'order by',
                             'depends_on':'order by header',
                             'optional': True},
                            {'data': [{'sig': ['limit', '{length}']},
                                      {'sig': ['limit',
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
               'segments': [{'data':[{'sig':['set']}],
                            'name':'set header',
                            'optional':True
                            },
                            {'name':'set header',
                             'optional':True,
                             'data': [{'sig': ['set']}],},


                            {'arguments': 0,
                             'data': [{'sig': ['{variable}',
                                               '=',
                                               '{value}'],
                                       'vars': {'type': 'all'}}],
                             'name': 'set',
                             'optional':True,
                             'depends_on':'set header'}]},
              {'name': 'create procedure',
               'segments': [{'arguments': None,
                             'data': [{'sig': ['create',
                                               'procedure',
                                               '(']}],
                             'dispose': True,
                             'name': ['create', 'procedure'],
                             'optional': False},
                            {'arguments': 0,
                             'data': [{'sig': ['{parameter}']}],
                             'name': ['parameters'],
                             'optional': True},
                            {'data': [{'sig': [')']}],
                             'dispose': True,
                             'name': [')'],
                             'optional': False}]},
              {'name': 'delimiter',
               'segments': [{'data': [{'sig': ['delimiter',
                                               '{delimiter}']}],
                             'name': 'delimiter'}]},
              {'name': 'end',
               'segments': [{'data': [{'sig': ['end']}], 'name': 'end'}]},
              {'name': 'begin',
               'segments': [    {'data': [{'sig': ['begin']}], 
                                 'name': 'begin'}]},
              {'name': 'commit', 
                    'segments': [
                                {
                                'data': [{'sig': ['commit']}],
                                'name': 'commit'}
                                ]
              },
              {'name': 'rollback',
               'segments': [{'data': [{'sig': ['rollback']}],
                             'name': 'rollback'}]},
              {'name': 'show output modules',
               'segments': [{'data': [{'sig': ['show',
                                               'output',
                                               'modules']}],
                             'name': 'show output modules'}]},
              {'name': 'delete',
               'segments': [{'data': [{'sig': ['delete']}],
                             'name': 'delete'},
                            {'data': [{'sig': ['from', '{table}']}],
                             'name': 'from'},
                            {'data': [{'sig': ['where','{e1}','$operators:c','{e2}'] } ] ,
                             'name': 'where',
                             'optional': True,
                             'store_array': True},
                            {'arguments': 0,
                            {'data': [{'sig': ['and','{e1}','$operators:c','{e2}'] } ] ,
                             'depends_on': 'where',
                             'jump': 'where',
                             'name': 'and',
                             'optional': True,
                             'parent': 'where'
                             },
                            {'data': [{'sig': ['or','{e1}','$operators:c','{e2}'] } ] ,
                             'depends_on': 'where',
                             'jump': 'where',
                             'name': 'or',
                             'optional': True,
                             'parent': 'where'}]},
              {'name': 'insert',
               'segments': [{'data': [{'sig': ['insert']}],
                             'name': 'insert'},
                            {'data': [{'sig': ['into', '{table}']},
                                      {'sig': ['into',
                                               '{database}',
                                               '.',
                                               '{table}']}],
                             'name': 'into'},
                            {'data': [{'sig': ['(']}],
                             'dispose': True,
                             'name': '('},
                            {'arguments': 0,
                             'data': [{'sig': ['{column}']}],
                             'name': 'columns',
                             },
                            {'data': [{'sig': [')']}],
                             'dispose': True,
                             'name': ')'},
                            {'data': [{'sig': ['values']}],
                             'dispose': True,
                             'name': 'values'},
                            {'data': [{'sig': ['(']}],
                             'dispose': True,
                             'name': '('},
                            
                            {'arguments': 0,
                             'data': [{'sig': ['{value}']}],
                             'name': 'values',
                             'no_keyword': True},
                            {'data': [{'sig': [')']}],
                             'dispose': True,
                             'name': ')'}]},
              {'name': 'update',
               'segments': [{'data': [{'sig': ['update', '{table}']},
                                      {'sig': ['update',
                                               '{database}',
                                               '.',
                                               '{table}']}],
                            'name': 'update'},
                            {'name':'set header',
                             'data': [{'sig': ['set']}],},
                            {'arguments': 0,
                             'data': [{'sig': ['{column}',
                                               '=',
                                               '{expression}']}],
                             'name': 'set',
                             'depends_on':'set header'},
                            {'data': [{'sig': ['where','{e1}','$operators:c','{e2}'] } ] ,
                             'name': 'where',
                             'optional': True,
                             'store_array': True},
                            {
                            {'data': [{'sig': ['and','{e1}','$operators:c','{e2}'] } ] ,
                             'depends_on': 'where',
                             'jump': 'where',
                             'name': 'and',
                             'optional': True,
                             'parent': 'where'},
                            {'data': [{'sig': ['or','{e1}','$operators:c','{e2}'] } ] ,
                             'depends_on': 'where',
                             'jump': 'where',
                             'name': 'or',
                             'optional': True,
                             'parent': 'where'}]},
              {'name': 'upsert',
               'segments': [{'data': [{'sig': ['upsert']}],
                             'name': 'upsert'},
                            {'data': [{'sig': ['into', '{table}']},
                                      {'sig': ['into',
                                               '{database}',
                                               '.',
                                               '{table}']}],
                             'name': 'into'},
                            {'data': [{'sig': ['(']}],
                             'dispose': True,
                             'name': '('},
                            {'arguments': 0,
                             'data': [{'sig': ['{column}']}],
                             'name': 'columns',
                             'no_keyword': True},
                            {'data': [{'sig': [')']}],
                             'dispose': True,
                             'name': ')'},
                            {'data': [{'sig': ['values']}],
                             'dispose': True,
                             'name': 'values'},
                            {'data': [{'sig': ['(']}],
                             'dispose': True,
                             'name': '('},
                            {'arguments': 0,
                             'data': [{'sig': ['{value}']}],
                             'name': 'values',
                             'no_keyword': True},
                            {'data': [{'sig': [')']}],
                             'dispose': True,
                             'name': ')'},
                            {
                             'data': [{'sig': ['on', 'duplicate', 'key']}],
                             'name': 'on duplicate key header',
                             },
                            {'arguments': 0,
                             'data': [{'sig': ['{column}']}],
                             'name': 'on duplicate key',
                             'depends_on':'on duplicate key header'},
                            {
                             'data': [{'sig': ['update']}],
                             'key':'set',
                             'name':'update header'
                             },
                            {'arguments': 0,
                             'data': [{'sig': ['{column}',
                                               '=',
                                               '{expression}']}],
                             'key': 'set',
                             'name': 'update',
                             'depends_on':'set'
                             
                             }]},
              {'name': 'use',
               'segments': [{'data': [{'sig': ['use', '{table}']}],
                             'name': 'use'}]},
              {'name': 'drop',
               'segments': [{'data': [{'sig': ['drop',
                                               'table',
                                               '{table}']},
                                      {'sig': ['drop',
                                               'table',
                                               '{database}',
                                               '.',
                                               '{table}']}],
                             'name': 'drop'}]},
              {'name': 'create',
               'segments': [{'data': [{'sig': ['create']}],
                             'name': 'create',
                             'optional': False},
                            {'data': [{'sig': ['temporary']}],
                             'name': 'temporary',
                             'optional': True},
                            {'data': [{'sig': ['table', '{table}']},
                                      {'sig': ['table',
                                               '{database}',
                                               '.',
                                               '{table}']}],
                             'name': 'table',
                             'optional': False,
                             'type': 'single'},
                            {'data': [{'sig': ['(']}],
                             'dispose': True,
                             'name': '('},
                            {'arguments': 0,
                             'data': [{'sig': ['{column}']}],
                             'name': 'columns',
                             'no_keyword': True},
                            {'data': [{'sig': [')']}],
                             'dispose': True,
                             'name': ')'},
                            {'data': [{'sig': ['file', '=', '{file}']}],
                             'name': 'file',
                             'type': 'single'},
                            {'data': [{'sig': ['fifo', '=', '{fifo}']}],
                             'name': 'fifo',
                             'optional': True,
                             'type': 'single'},
                            {'data': [{'sig': ['repo',
                                               '=',
                                               '{repo_type}',
                                               'url',
                                               '=',
                                               '{repo_url}',
                                               'user',
                                               '=',
                                               '{repo_user}',
                                               'password',
                                               '=',
                                               '{repo_password}',
                                               'repo_dir',
                                               '=',
                                               '{repo_dir}',
                                               'repo_file',
                                               '=',
                                               '{repo_file}']}],
                             'name': 'repo',
                             'optional': True,
                             'type': 'single'},
                            {'data': [{'sig': ['delimiter',
                                               '=',
                                               '{delimiter}']}],
                             'name': 'delimiter',
                             'optional': True,
                             'specs': {'field': {'default': ',',
                                                 'type': 'char'}},
                             'type': 'single'},
                            {'data': [{'sig': ['whitespace',
                                               '=',
                                               '{whitespace}']}],
                             'name': 'whitespace',
                             'optional': True,
                             'specs': {'whitespace': {'type': 'bool'}},
                             'type': 'single'},
                            {'data': [{'sig': ['errors',
                                               '=',
                                               '{errors}']}],
                             'name': 'errors',
                             'optional': True,
                             'specs': {'errors': {'type': 'bool'}},
                             'type': 'single'},
                            {'data': [{'sig': ['comments',
                                               '=',
                                               '{comments}']}],
                             'name': 'comments',
                             'optional': True,
                             'specs': {'comments': {'type': 'bool','default': None}},
                             'type': 'single'},
                            {'data': [{'sig': ['strict',
                                               '=',
                                               '{strict}']}],
                             'name': 'strict',
                             'optional': True,
                             'specs': {'strict': {'type': 'bool','default': True}},
                             'type': 'single'},
                            {'data': [{'sig': ['data_starts_on',
                                               '=',
                                               '{data_starts_on}']}],
                             'name': 'data_starts_on',
                             'optional': True,
                             'specs': {'data_starts_on': {'default': 1,
                                                          'type': 'int'}},
                             'type': 'single'}]},
              {'name': 'update table',
               'segments': [{'data': [{'sig': ['update',
                                               'table',
                                               '{table}']}],
                             'name': 'update'},
                            {'data': [{'sig': ['(']}],
                             'dispose': True,
                             'name': '(',
                             'optional': True},
                            {'arguments': 0,
                             'data': [{'sig': ['{column}']}],
                             'depends_on': '(',
                             'name': 'columns',
                             'no_keyword': True,
                             'optional': True},
                            {'data': [{'sig': [')']}],
                             'depends_on': '(',
                             'dispose': True,
                             'name': ')',
                             'optional': True},
                            {'data': [{'sig': ['file', '=', '{file}']}],
                             'name': 'file',
                             'optional': True},
                            {'data': [{'sig': ['delimiter',
                                               '=',
                                               '{field}']}],
                             'name': 'delimiter',
                             'optional': True,
                             'specs': {'field': {'default': ',',
                                                 'type': 'char'}}},
                            {'data': [{'sig': ['whitespace',
                                               '=',
                                               '{whitespace}']}],
                             'name': 'whitespace',
                             'optional': True,
                             'specs': {'whitespace': {'type': 'bool'}}},
                            {'data': [{'sig': ['errors',
                                               '=',
                                               '{whitespace}']}],
                             'name': 'errors',
                             'optional': True,
                             'specs': {'errors': {'type': 'bool'}}},
                            {'data': [{'sig': ['comments',
                                               '=',
                                               '{comments}']}],
                             'name': 'comments',
                             'optional': True,
                             'specs': {'comments': {'type': 'bool'}}},
                            {'data': [{'sig': ['data_starts_on',
                                               '=',
                                               '{data_starts_on}']}],
                             'name': 'data_starts_on',
                             'optional': True,
                             'specs': {'data_starts_on': {'type': 'int'}}}]},
              {'name': 'describe table',
               'segments': [{'data': [{'sig': ['describe',
                                               'table',
                                               '{table}']},
                                      {'sig': ['describe',
                                               'table',
                                               '{database}',
                                               '.',
                                               '{table}']}],
                             'name': ['describe', 'table']}]}],
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


if 1==0 :
        for command in language['commands']:
            syn="## {0}\n".format(command['name'])
            optional=None
            if 'optional' in command:
                if command['optional']==True:
                        optional=True
                if optional:
                        syn+="["
                for segment in command['segments']:
                        for pattern in segment['data']:
                                for part in pattern['sig']:
                                        syn+=" {0} ".format(part)
                                syn+=" | "
                if optional:
                        syn+="]"
                print( syn)
        







# INSERT INTO [database.] table (column [, column ...]) VALUES (value [, value ...] )

                                               

                                       