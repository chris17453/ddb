# -*- coding: utf-8 -*-
# ############################################################################
# :########::'########::'########::
# :##.... ##: ##.... ##: ##.... ##:
# :##:::: ##: ##:::: ##: ##:::: ##:
# :##:::: ##: ##:::: ##: ########::
# :##:::: ##: ##:::: ##: ##.... ##:
# :##:::: ##: ##:::: ##: ##:::: ##:
# :########:: ########:: ########::
# :.......:::........:::........:::
# Author: Charles Watkins
# This file is automagically generated
# dont edit it, because it will be erased next build
# 
# ############################################################################
        
import sys
import os
import fileinput
import warnings
import datetime
import tempfile
try:
    import flextable
except Exception as ex:
    pass



        
        
# ############################################################################
# Module : version
# File   : ./source/ddb/version.py
# ############################################################################



__version__='1.1.102'

        
        
# ############################################################################
# Module : lexer-language
# File   : ./source/ddb/lexer/language.py
# ############################################################################








sql_syntax = {
    'functions': [{'name': 'database', 'arguments': None},
                  {'name': 'count', 'arguments': [
                      {'name': 'where', 'required': True}]},
                  {'name': 'sum', 'arguments': [
                      {'name': 'column', 'required': True}]},
                  {'name': 'version', 'arguments': None},
                  {'name': 'upper', 'arguments': [
                      {'name': 'column', 'required': True}]},
                  {'name': 'lower', 'arguments': [
                      {'name': 'column', 'required': True}]},
                  {'name': 'cat', 'arguments':  [
                      {'name': 'arg1', 'required': True}, {'name': 'arg2', 'required': True}]},
                  {'name': 'date', 'arguments': None},
                  {'name': 'time', 'arguments': None},
                  {'name': 'datetime', 'arguments': None},
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
         'arguments': 1,
         'switch': [
             {'data': None,
              'name': 'select',
              'optional': False
              },
             {'data': None,
              'name': 'distinct',
              'optional': True
              },

             {'arguments': 0,
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
              'name': 'columns',
              'no_keyword': True,

              'depends_on':'select'
              },

             {'arguments': 1,
              'data': [ {'sig': ['{table}']},
                        {'sig': ['{table}', 'as', '{display}']},
                        {'sig': ['{database}','.','{table}']},
                        {'sig': ['{database}','.','{table}', 'as', '{display}']}
                        ],
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
              'data': [
                    {'vars':{'c':'<'   }, 'sig': ['{e1}', '<',    '{e2}']},
                    {'vars':{'c':'>'   }, 'sig': ['{e1}', '>',    '{e2}']},
                    {'vars':{'c':'>='  }, 'sig': ['{e1}', '>=',   '{e2}']},
                    {'vars':{'c':'<='  }, 'sig': ['{e1}', '<=',   '{e2}']},
                    {'vars':{'c':'!='  }, 'sig': ['{e1}', '!=',   '{e2}']},
                    {'vars':{'c':'<>'  }, 'sig': ['{e1}', '<>',   '{e2}']},
                    {'vars':{'c':'not' }, 'sig': ['{e1}', 'not',  '{e2}']},
                    {'vars':{'c':'is'  }, 'sig': ['{e1}', 'is',   '{e2}']},
                    {'vars':{'c':'like'}, 'sig': ['{e1}', 'like', '{e2}']},
                    {'vars':{'c':'='   }, 'sig': ['{e1}', '=',    '{e2}']},
                    {'vars':{'c':'in'  }, 'sig': ['{e1}', 'in',   '(','[e2]',')']},
                  ],
              'name': 'on',
              'optional': True,
              'depends_on': 'join',
              'store_array': True},
             {'arguments': 1,
              'data': [
                    {'vars':{'c':'<'   }, 'sig': ['{e1}', '<',    '{e2}']},
                    {'vars':{'c':'>'   }, 'sig': ['{e1}', '>',    '{e2}']},
                    {'vars':{'c':'>='  }, 'sig': ['{e1}', '>=',   '{e2}']},
                    {'vars':{'c':'<='  }, 'sig': ['{e1}', '<=',   '{e2}']},
                    {'vars':{'c':'!='  }, 'sig': ['{e1}', '!=',   '{e2}']},
                    {'vars':{'c':'<>'  }, 'sig': ['{e1}', '<>',   '{e2}']},
                    {'vars':{'c':'not' }, 'sig': ['{e1}', 'not',  '{e2}']},
                    {'vars':{'c':'is'  }, 'sig': ['{e1}', 'is',   '{e2}']},
                    {'vars':{'c':'like'}, 'sig': ['{e1}', 'like', '{e2}']},
                    {'vars':{'c':'='   }, 'sig': ['{e1}', '=',    '{e2}']},
                    {'vars':{'c':'in'  }, 'sig': ['{e1}', 'in',   '(','[e2]',')']},
                  ],              'depends_on': 'on',
              'jump': 'on',
              'name': 'and',
              'optional': True,
              'parent': 'on'},
             {'arguments': 1,
              'data': [
                    {'vars':{'c':'<'   }, 'sig': ['{e1}', '<',    '{e2}']},
                    {'vars':{'c':'>'   }, 'sig': ['{e1}', '>',    '{e2}']},
                    {'vars':{'c':'>='  }, 'sig': ['{e1}', '>=',   '{e2}']},
                    {'vars':{'c':'<='  }, 'sig': ['{e1}', '<=',   '{e2}']},
                    {'vars':{'c':'!='  }, 'sig': ['{e1}', '!=',   '{e2}']},
                    {'vars':{'c':'<>'  }, 'sig': ['{e1}', '<>',   '{e2}']},
                    {'vars':{'c':'not' }, 'sig': ['{e1}', 'not',  '{e2}']},
                    {'vars':{'c':'is'  }, 'sig': ['{e1}', 'is',   '{e2}']},
                    {'vars':{'c':'like'}, 'sig': ['{e1}', 'like', '{e2}']},
                    {'vars':{'c':'='   }, 'sig': ['{e1}', '=',    '{e2}']},
                    {'vars':{'c':'in'  }, 'sig': ['{e1}', 'in',   '(','[e2]',')']},
                  ],              'depends_on': 'on',
              'jump': 'on',
              'name': 'or',
              'optional': True,
              'parent': 'on'},


             {'arguments': 1,
              'data': [
                    {'vars':{'c':'<'   }, 'sig': ['{e1}', '<',    '{e2}']},
                    {'vars':{'c':'>'   }, 'sig': ['{e1}', '>',    '{e2}']},
                    {'vars':{'c':'>='  }, 'sig': ['{e1}', '>=',   '{e2}']},
                    {'vars':{'c':'<='  }, 'sig': ['{e1}', '<=',   '{e2}']},
                    {'vars':{'c':'!='  }, 'sig': ['{e1}', '!=',   '{e2}']},
                    {'vars':{'c':'<>'  }, 'sig': ['{e1}', '<>',   '{e2}']},
                    {'vars':{'c':'not' }, 'sig': ['{e1}', 'not',  '{e2}']},
                    {'vars':{'c':'is'  }, 'sig': ['{e1}', 'is',   '{e2}']},
                    {'vars':{'c':'like'}, 'sig': ['{e1}', 'like', '{e2}']},
                    {'vars':{'c':'='   }, 'sig': ['{e1}', '=',    '{e2}']},
                    {'vars':{'c':'in'  }, 'sig': ['{e1}', 'in',   '(','[e2]',')']},
                  ],              'name': 'where',
              'optional': True,
              'depends_on': 'from',
              'store_array': True},
             {'arguments': 1,
              'data': [
                    {'vars':{'c':'<'   }, 'sig': ['{e1}', '<',    '{e2}']},
                    {'vars':{'c':'>'   }, 'sig': ['{e1}', '>',    '{e2}']},
                    {'vars':{'c':'>='  }, 'sig': ['{e1}', '>=',   '{e2}']},
                    {'vars':{'c':'<='  }, 'sig': ['{e1}', '<=',   '{e2}']},
                    {'vars':{'c':'!='  }, 'sig': ['{e1}', '!=',   '{e2}']},
                    {'vars':{'c':'<>'  }, 'sig': ['{e1}', '<>',   '{e2}']},
                    {'vars':{'c':'not' }, 'sig': ['{e1}', 'not',  '{e2}']},
                    {'vars':{'c':'is'  }, 'sig': ['{e1}', 'is',   '{e2}']},
                    {'vars':{'c':'like'}, 'sig': ['{e1}', 'like', '{e2}']},
                    {'vars':{'c':'='   }, 'sig': ['{e1}', '=',    '{e2}']},
                    {'vars':{'c':'in'  }, 'sig': ['{e1}', 'in',   '(','[e2]',')']},
                  ],              'depends_on': 'where',
              'jump': 'where',
              'name': 'and',
              'optional': True,
              'parent': 'where'},
             {'arguments': 1,
              'data': [
                    {'vars':{'c':'<'   }, 'sig': ['{e1}', '<',    '{e2}']},
                    {'vars':{'c':'>'   }, 'sig': ['{e1}', '>',    '{e2}']},
                    {'vars':{'c':'>='  }, 'sig': ['{e1}', '>=',   '{e2}']},
                    {'vars':{'c':'<='  }, 'sig': ['{e1}', '<=',   '{e2}']},
                    {'vars':{'c':'!='  }, 'sig': ['{e1}', '!=',   '{e2}']},
                    {'vars':{'c':'<>'  }, 'sig': ['{e1}', '<>',   '{e2}']},
                    {'vars':{'c':'not' }, 'sig': ['{e1}', 'not',  '{e2}']},
                    {'vars':{'c':'is'  }, 'sig': ['{e1}', 'is',   '{e2}']},
                    {'vars':{'c':'like'}, 'sig': ['{e1}', 'like', '{e2}']},
                    {'vars':{'c':'='   }, 'sig': ['{e1}', '=',    '{e2}']},
                    {'vars':{'c':'in'  }, 'sig': ['{e1}', 'in',   '(','[e2]',')']},
                  ],              'depends_on': 'where',
              'jump': 'where',
              'name': 'or',
              'optional': True,
              'parent': 'where'},

             {'arguments': 0,
              'data': [{'sig': ['{column}']}],
              'name': ['group', 'by'],
              'optional': True},


             {'arguments': 0,
              'data': [{'sig': ['{column}']},
                       {'vars':{'direction':1},'sig': ['{column}', 'asc']},
                       {'vars':{'direction':-1},'sig': ['{column}', 'desc']}],
              'name': ['order', 'by'],
              'optional': True},
             {'data': [{'sig': ['{length}']},
                       {'sig': ['{start}',
                                ',',
                                '{length}']}],
              'specs':{'length': {'type': 'int', 'default': 0}, 'start': {'type': 'int', 'default': 0}},

              'name': 'limit',
              'optional': True}]},



        {'query': 'set',
         'switch': [{
             'name': 'set',
             'arguments': 0,
             'data': [{'sig': ['{variable}', '=', '{value}']}],
         }]
         },
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
                        'data': [ {'sig': ['{table}']},
                                    {'sig': ['{database}','.','{table}']},
                                    ],
                        'name': 'into',
                        },
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
                     'data': [{'sig': ['{table}']},
                              {'sig': ['{database}','.','{table}']},
                     ],
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
        {'query': 'drop',
         'switch': [{'arguments': 1,
                     'data': [ {'sig': ['table','{table}']},
                               {'sig': ['table','{database}','.','{table}']}],

                     'name': 'drop'}]},
        {'query': 'create',
         'switch': [

             {'data': None,
              'name': 'create',
              'optional': False
              },
             {'data': None,
              'name': 'temporary',
              'optional': True
              },

             {'arguments': 1,
              'data': [ {'sig': ['{table}']},
                        {'sig': ['{database}','.','{table}']},
                        ],
              'name': 'table',
              'type': 'single',
              'optional': False },

             {'data': False, 'dispose': True, 'name': '('},
             {'arguments': 0,
              'data': [{'sig': ['{column}']}],
              'name': 'columns',
              'no_keyword': True},
             {'data': False, 'dispose': True, 'name': ')'},
             {'arguments': 1,
              'data': [{'sig': ['=', '{file}']}],
              'type':'single',
              'name': 'file'},
             {'arguments': 1,
              'data': [{'sig': ['=', '{delimiter}']}],
              'type':'single',
              'optional': True,
              'specs':{'field': {'type': 'char', 'default': ','}},
              'name': 'delimiter'},
             {'arguments': 1,
              'data': [{'sig': ['=', '{whitespace}']}],
              'type':'single',
              'optional': True,
              'specs':{'whitespace': {'type': 'bool'}},
              'name': 'whitespace'},
             {'arguments': 1,
              'data': [{'sig': ['=', '{errors}']}],
              'type':'single',
              'optional': True,
              'specs':{'errors': {'type': 'bool'}},
              'name': 'errors'},
             {'arguments': 1,
              'data': [{'sig': ['=', '{comments}']}],
              'type':'single',
              'optional': True,
              'specs':{'comments': {'type': 'bool'}},
              'name': 'comments'},
             {'arguments': 1,
              'data': [{'sig': ['=', '{data_starts_on}']}],
              'type':'single',
              'optional': True,
              'specs':{'data_starts_on': {'type': 'int', 'default': 1}},
              'name': 'data_starts_on'}, ]},


        {'query': 'update table',
         'switch': [{'arguments': 1,
                     'data': [{'sig': ['table', '{table}']}],
                     'name': 'update'},
                    {'data': False, 'dispose': True,
                        'name': '(', 'optional': True},
                    {'arguments': 0,
                     'data': [{'sig': ['{column}']}],
                     'name': 'columns',
                     'no_keyword': True,
                     'depends_on':'(',
                     'optional': True},
                    {'data': False, 'dispose': True,
                        'name': ')', 'optional': True, 'depends_on': '('},
                    {'arguments': 1,
                     'data': [{'sig': ['=', '{file}']}],
                     'name': 'file',
                     'optional': True},
                    {'arguments': 1,
                     'data': [{'sig': ['=', '{field}']}],
                     'optional': True,
                     'specs':{'field': {'type': 'char', 'default': ','}},
                     'name': 'delimiter'},
                    {'arguments': 1,
                     'data': [{'sig': ['=', '{whitespace}']}],
                     'optional': True,
                     'specs':{'whitespace': {'type': 'bool'}},
                     'name': 'whitespace'},
                    {'arguments': 1,
                     'data': [{'sig': ['=', '{whitespace}']}],
                     'optional': True,
                     'specs':{'errors': {'type': 'bool'}},
                     'name': 'errors'},
                    {'arguments': 1,
                     'data': [{'sig': ['=', '{comments}']}],
                     'optional': True,
                     'specs':{'comments': {'type': 'bool'}},
                     'name': 'comments'},
                    {'arguments': 1,
                     'data': [{'sig': ['=', '{data_starts_on}']}],
                     'optional': True,
                     'specs':{'data_starts_on': {'type': 'int'}},
                     'name': 'data_starts_on'}
                    ]
         },
        {'query': 'describe table',
         'switch': [{'arguments': 1,
                     'data': [{'sig': ['table', '{table}']}],
                     'name': 'describe'}]},


    ]  # query matrix array
}  # sql_syntax

        
        
# ############################################################################
# Module : lexer-parse
# File   : ./source/ddb/lexer/lexer.py
# ############################################################################





class lexer:
   

    def __init__(self, query, debug=False):

        self.keep_non_keywords=True
        self.debug = debug
        self.query_objects = []
        querys = query.split(';')
        self.info("Queries", querys)
        for q in querys:
            self.info("-----------------------------------")
            tokens = tokenizer().chomp(q, discard_whitespace=True, debug=debug)
            token_length = 0
            for token in tokens:
                if token['data'] != '':
                    token_length += 1

            self.info("Token Length", token_length)
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
        debug = True
        query_object = {}
        for query in sql_syntax['query_matrix']:
            token_index = 0
            self.info("-----", query['query'])

            keyword_found = False
            switch_index = 0
            query_mode = None
            curent_object = {}
            switch = {}
            while switch_index < len(query['switch']) and token_index < len(tokens):

                self.info("Token Index", token_index, "token", tokens[token_index])
                self.info("Token Length", len(tokens))
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
                if 'type' in switch:
                    meta_type = switch['type']
                else:
                    meta_type = None

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
                self.info("Object Id:", object_id, "Token Id:", token_index)
                if False == no_keyword:
                    keyword_compare = self.get_sub_array(switch, 'name')
                    haystack = self.get_sub_array_sub_key(tokens[token_index:], 'data')
                    self.info(keyword_compare)
                    if True == self.single_array_match(keyword_compare, haystack):
                        self.info("match", keyword_compare, haystack)
                        curent_object['mode'] = object_id
                        if switch_index == 1:
                            query_mode = query['query']
                        keyword_found = True
                    else:
                        if False == optional:
                            if True == debug:
                                self.info("Exiting")
                            break
                        else:
                            continue
                    if False == keyword_found:
                        self.info("Keywords exhausted")
                        break

                    token_index += len(keyword_compare)
                    self.info("advance token index ", token_index, switch['data'])
                else:
                    curent_object['mode'] = object_id

                base_argument={}

                if None == switch['data'] or False == switch['data']:
                    self.info("No data to match")
                    if not dispose:
                        self.info("----------Adding", curent_object['mode'])
                        query_object[curent_object['mode']] = None

                else:
                    in_argument = True
                    argument_index = 0
                    while True == in_argument:

                        self.info("---in argument")


                        if 'depends_on' in switch:
                            depends_on = switch['depends_on']
                        else:
                            self.info("--- Depends on nothing")
                            depends_on = None

                        if None != depends_on:

                            depends_oncompare = self.get_sub_array(depends_on)

                            dependency_found = False
                            for q_o in query_object:
                                haystack = self.get_sub_array(q_o)
                                if True == self.single_array_match(depends_oncompare, haystack):
                                    dependency_found = True
                            if False == dependency_found:
                                self.info("Missing", depends_on)
                                break
                            else:
                                self.info("Dependency found", depends_on)

                        if 'arguments' in switch:
                            arguments = switch['arguments']
                        else:
                            arguments = 1
                        self.info("Number of arguments", arguments)

                        data = self.get_sub_array(switch, 'data')
                        match_len = 0
                        match = None
                        for sig in data:
                            signature_compare = self.get_sub_array(sig, 'sig')
                            haystack = self.get_sub_array_sub_key(tokens[token_index:], 'data')
                            if True == self.single_array_match(signature_compare, haystack):
                                if len(signature_compare) > match_len:
                                    match_len = len(signature_compare)
                                    match = signature_compare
                                    signature=sig
                                    self.info("Best Match", match_len)
                        if None == match:
                            self.info("No match")
                            break
                        else:
                            base_argument={}
                            if 'vars' in signature:
                                for var_name in signature['vars']:
                                    self.info("var","'{0}'='{1}'".format(var_name,signature['vars'][var_name]))
                                    base_argument[var_name]=signature['vars'][var_name]

                            w_index = 0
                            argument = base_argument
                            for word in match:
                                variable_data=tokens[token_index + w_index]['data']
                                if word[0:1] == '[' and word[-1] == ']': 
                                    definition='array'
                                elif word[0:1] == '{' and word[-1] == '}':
                                     definition='single'
                                else:
                                    definition=None

                                if definition:
                                    variable=word[1:-1]
                                    variable_type='string'
                                    if 'specs' in switch:
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
                                    if self.keep_non_keywords:
                                        argument[word] = variable_data
                                w_index += 1
                            if 'arguments' not in curent_object:
                                curent_object['arguments'] = []

                            if arguments == 1:
                                curent_object['arguments'] = argument
                            else:
                                curent_object['arguments'].append(argument)

                            self.info("match", match)
                            token_index += len(match)
                            if arguments != 0:
                                self.info("print not in list")
                                argument_index += 1
                                if argument_index >= arguments:
                                    self.info("----------Adding", curent_object['mode'])
                                    if True == store_array:
                                        if curent_object['mode'] not in query_object:
                                            query_object[curent_object['mode']] = []

                                        query_object[curent_object['mode']].append({curent_object['mode']: curent_object['arguments']})
                                    else:
                                        if None == parent:
                                            if meta_type=='single':
                                                for arg_key in curent_object['arguments']:
                                                    query_object[arg_key] = curent_object['arguments'][arg_key]
                                            else:    
                                                query_object[curent_object['mode']] = curent_object['arguments']
                                            self.info("NO APPEND")
                                        else:
                                            self.info("APPEND")
                                            query_object[parent].append({curent_object['mode']: curent_object['arguments']})
                                    jump = None
                                    if 'jump' in switch:
                                        self.info("JUMP")
                                        jump = switch['jump']
                                    if None != jump:
                                        tsi = 0
                                        for ts in query['switch']:
                                            if ts['name'] == jump:
                                                self.info("Jumping from ", switch_index, tsi + 1)
                                                switch_index = tsi + 1
                                                break
                                            tsi += 1
                                    in_argument = False

                                    in_argument = False
                            else:
                                self.info("in list")

                                if len(tokens) <= token_index:
                                    self.info("at the end")
                                    if True == store_array:
                                        if curent_object['mode'] not in query_object:
                                            query_object[curent_object['mode']] = []

                                        query_object[curent_object['mode']].append({curent_object['mode']: curent_object['arguments']})
                                    else:
                                        if None == parent:
                                            query_object[curent_object['mode']] = curent_object['arguments']
                                            self.info("NO APPEND")

                                        else:
                                            self.info("APPEND")
                                            query_object[parent].append({curent_object['mode']: curent_object['arguments']})

                                if len(tokens) > token_index:
                                    self.info("--looking ahead")
                                    self.info("----", tokens[token_index]['data'])
                                    if tokens[token_index]['data'] != ',':
                                        self.info("---not list")
                                        self.info("----------Adding", curent_object['mode'])
                                        if True == store_array:
                                            if curent_object['mode'] not in query_object:
                                                query_object[curent_object['mode']] = []

                                            query_object[curent_object['mode']].append({curent_object['mode']: curent_object['arguments']})
                                        else:
                                            if None == parent:
                                                query_object[curent_object['mode']] = curent_object['arguments']
                                                self.info("NO APPEND")

                                            else:
                                                self.info("APPEND")
                                                query_object[parent].append({curent_object['mode']: curent_object['arguments']})
                                        jump = None
                                        if 'jump' in switch:
                                            jump = switch['jump']
                                        if None != jump:
                                            tsi = 0
                                            for ts in query['switch']:
                                                if ts['name'] == jump:
                                                    self.info("Jumping from ", switch_index, tsi + 1)
                                                    switch_index = tsi + 1
                                                    break
                                                tsi += 1
                                        in_argument = False
                                    else:
                                        self.info("------more list")
                                        token_index += 1

            self.info(switch_index, token_index, len(tokens))


            self.info(curent_object)
            if token_index == len(tokens):

                result=self.validate(curent_object,tokens,token_index,switch,query,switch_index,query_object,query_mode)
                if False == result:
                    break
                else:
                    return result

        
        
        return False





    def validate(self,curent_object,tokens,token_index,switch,query,switch_index,query_object,query_mode):
        self.info(curent_object)
        self.info("############################think its a match")

        if 'arguments' not in curent_object and 'arguments' in switch:
            self.info("Missing argument in last element")
            bad = True
            return False

        if len(query['switch']) >= switch_index:
            self.info("still checking")
            bad = False
            for t in range(switch_index, len(query['switch'])):
                if 'optional' not in query['switch'][t]:
                    bad = True
                    return False

                else:
                    if not query['switch'][t]['optional']:
                        bad = True
                        return False

            if True == bad:
                self.info("Not successful. required arguments missing")
                return False

        self.info("Query object", query_object)
        if query_mode == 'select':
            self.info("Validating Select Functions")
            if 'columns' in query_object:
                for node in query_object['columns']:
                    valid_function_name = False
                    is_function = False
                    if 'function' in node:
                        is_function = True
                        self.info("It's a function!")
                        for f in sql_syntax['functions']:
                            if f['name'] == node['function']:
                                argindex = 1
                                if f['arguments'] is not None:
                                    for arg in f['arguments']:
                                        if arg['required']:
                                            if 'argument{0}'.format(argindex) not in node:
                                                self.info("Missing arguments")
                                                return False
                                        argindex += 1

                                else:
                                    argindex = 0
                                if 'argument{0}'.format(argindex + 1) in node:
                                    self.info("Too many arguments")
                                    return False

                            valid_function_name = True
                            break
                    if False == valid_function_name and True == is_function:
                        self.info("FAIL", "This isnt a valid function", node['function'])
                        return False
            else:
                self.info("No columns in select")
                return False

        self.info("SUCCESS")
        sql_object = {'mode': query_mode, 'meta': query_object}
        return sql_object

    def expand_columns(self, query_object, columns):
        if 'columns' in query_object['meta']:
            expanded_select = []
            for item in query_object['meta']['columns']:
                if 'column' in item:
                    if item['column'] == '*':
                        for column in columns:
                            expanded_select.append({'column': column})
                    else:
                        expanded_select.append(item)
                if 'function' in item:
                    expanded_select.append(item)

            query_object['meta']['columns'] = expanded_select


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


    def get_sub_array_sub_key(self, array, key):
        temp_array = []

        for item in array:
            temp_array.append(item[key])

        return temp_array

    def single_array_match(self, needles, haystacks):
        """ Match a single or array of strings with with another string or array of strings"""

        if isinstance(needles, str):
            temp_needles = [needles]
        else:
            temp_needles = needles

        if isinstance(haystacks, str):
            temp_haystacks = [haystacks]
        else:
            temp_haystacks = haystacks


        index = 0
        for needle in temp_needles:
            if index >= len(temp_haystacks):
                return False
            haystack = temp_haystacks[index]
            if needle[0:1] != '{' and needle[-1] != '}':
                if needle.lower() != haystack.lower():
                    return False
            index += 1
        return True

    def info(self,msg, arg1=None, arg2=None, arg3=None):
        if True == self.debug:
            if arg3 is None and arg2 is None:
                print("{0} {1}".format(msg, arg1))
                return
            if arg3 is None:
                print("{0} {1} {2}".format(msg, arg1, arg2))
                return
            if arg2 is None:
                print("{0} {1}".format(msg, arg1))
                return

            print("[{0}]".format(msg))


        
        
# ############################################################################
# Module : lexer-token
# File   : ./source/ddb/lexer/tokenize.py
# ############################################################################



class tokenizer():

    def chomp(self,text, discard_delimiters=False, discard_whitespace=True, debug=False):
        self.debug_on = debug
        tokens = []

        text = text.strip()
        whitespace = {' ', '\t', '\n', '\r'}
        blocks = [
            ['\'', '\'', 'quote'],   # string block
            ['"', '"', 'quote'],   # string block
            ['[', ']', 'db'],   # mssql column
            ['`', '`', 'db'],   # mysql column
        ]


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


            '+',  # addition
            '-',  # subtraction
            '/',  # divide
            '*',  # multiple
            '(',  # left paren   (grouping)
            ')',  # right paren  (grouping)
        ]

        delimiters = [',', '.', ';']

        for token in whitespace:
            delimiters.append(token)

        for token in operators:
            delimiters.append(token)

        for b in blocks:
            if b[0] not in delimiters:
                delimiters.append(b[0])
            if b[1] not in delimiters:
                delimiters.append(b[1])

        delimiters_sorted = self.sort_array_by_length(delimiters)

        text_length = len(text)
        word_start = 0
        tokens = []
        c = 0
        delimter_len = 1
        in_block = None
        block = None

        while c < text_length:

            self.info("-", c)
            just_crossed_block = False
            for b in blocks:
                delimter_len = len(b[0])
                fragment = text[c:c + delimter_len]
                if None == in_block:
                    if True == self.compare_text_fragment(fragment, b[0]):
                        just_crossed_block = True
                        self.info("IN BLOCK", c)
                        in_block = b
                        block = b
                        c += delimter_len
                        self.info("IN BLOCK", c)
                        break
                if True == self.compare_text_fragment(fragment, b[1]) or c >= text_length - 1:
                    just_crossed_block = True
                    self.info("NOT IN BLOCK", c)
                    in_block = None
                    c += delimter_len
                    break
            if None != in_block:
                self.info("in block skip")
                if not just_crossed_block:
                    c += 1
                continue
            self.info("position1", c, text_length)
            if c > text_length:
                self.info("Greater than length of text. exiting")

                break
            for d in delimiters_sorted:
                delimter_len = len(d)
                fragment = text[c:c + delimter_len]



                if True == self.compare_text_fragment(fragment, d) or c >= text_length - 1:
                    self.info("Delemiter found", c, fragment)
                    if c - word_start > 0:
                        self.info("Data word found", c - word_start)
                        word_end = c
                        if word_end >= text_length:
                            self.info("word ends on last character", word_end, text_length)
                            word_end = text_length
                        not_delimiter = text[word_start:word_end]
                        token_type = 'data'
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
                        self.info("POSITION", c, not_delimiter)

                        tokens.append({'type': token_type, 'data': not_delimiter, 'block_left': block_left, 'block_right': block_right, 'block_type': block_type})

                    self.info("After Data Append, Position", c, 'of', text_length)

                    word_start = c + delimter_len

                    if not fragment or fragment == '':
                        break
                    if True == discard_whitespace and fragment in whitespace:
                        break


                    delimiter_type = "delimiter"
                    if fragment in operators:
                        delimiter_type = 'operator'
                    else:
                        if fragment in whitespace:
                            delimiter_type = 'whitespace'

                    self.info("delemiter c/fragment- ", c, fragment)
                    tokens.append({'type': delimiter_type, 'data': fragment.lower()})

                    break
            c += delimter_len

        if True == self.debug_on:
            self.info("-[Tokens]----------------")
            for t in tokens:
                self.info(t)
            self.info("-[End-Tokens]------------")
        return tokens


    def compare_text_fragment(self,x, y):
        if None == x or None == y:
            return False
        if x == y:
            return True
        return False


    def sort_array_by_length(self,data):
        max_len = -1
        for d in data:
            del_len = len(d)
            if del_len > max_len:
                max_len = del_len

        data_sorted = []
        for i in reversed(range(1, max_len + 1)):
            for d in data:
                if d not in data_sorted:
                    if len(d) == i:
                        data_sorted.append(d)
        return data

    def info(self,msg, arg1=None, arg2=None, arg3=None):
        if True == self.debug_on:
            if arg3 is None and arg2 is None:
                print("{0} {1}".format(msg, arg1))
                return
            if arg3 is None:
                print("{0} {1} {2}".format(msg, arg1, arg2))
                return
            if arg2 is None:
                print("{0} {1}".format(msg, arg1))
                return

            print("[{0}]".format(msg))


        
        
# ############################################################################
# Module : column
# File   : ./source/ddb/configuration/column.py
# ############################################################################




class column_v1:

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

        
        
# ############################################################################
# Module : table
# File   : ./source/ddb/configuration/table.py
# ############################################################################






class table:
    def __init__(self,
                 table_config_file=None,
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
        self.active = True

        self.update(data_file=data_file,
                    columns=columns,
                    field_delimiter=field_delimiter,
                    comments=comments,
                    whitespace=whitespace,
                    errors=errors,
                    data_on=data_on)

        if None != table_config_file:
            if os.path.exists(table_config_file):
                yaml_data = yamlf_load(file=table_config_file)
                if None == yaml_data:
                    raise Exception("Table configuration empty")
                for key in yaml_data:
                    if 'version' == key:
                        self.version = yaml_data[key]

                    if 'ownership' == key:
                        self.ownership = table_ownership(yaml=yaml_data[key])

                    if 'delimiters' == key:
                        self.delimiters = table_delimiters(yaml=yaml_data[key])

                    if 'visible' == key:
                        self.visible = table_visible_attributes(
                            yaml=yaml_data[key])

                    if 'data' == key:
                        self.data = table_data(yaml=yaml_data[key])

                    if 'columns' == key:
                        for c in yaml_data['columns']:
                            self.columns.append(column_v2(c))

                    if 'active' == key:
                        self.active = yaml_data[key]


        self.update_ordinals()
        if None != self.data.path:
            if False == os.path.exists(self.data.path):
                self.active = False

    def update(self,
               columns=None,
               data_file=None,
               field_delimiter=None,
               comments=None,
               whitespace=None,
               errors=None,
               data_on=None):
        if None != data_on:
            self.data.starts_on_line = data_on
        if None != comments:
            self.visible.comments = comments

        if None != whitespace:
            self.visible.whitespace = whitespace

        if None != errors:
            self.visible.errors = errors

        if None != field_delimiter:
            self.set_field_delimiter(field_delimiter)

        if None != data_file:
            self.data.path = data_file

        if None != columns:
            self.columns = []
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
        columns = self.get_columns_display()
        return {'columns': columns, 'results': self.results}

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
                temp_columns.append(
                    {'data': c.data.ordinal, 'display': c.display.ordinal})

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

        self.ordinals = {}
        for k, v in enumerate(self.columns):
            if None == v.data.ordinal or -1 == v.data.ordinal:

                self.columns[k].data.ordinal = self.get_lowest_available_ordinal()
                self.ordinals[v.data.name] = self.columns[k].data.ordinal
            else:
                self.ordinals[v.data.name] = v.data.ordinal


    def save(self):
        if None == self.data.name:
            raise Exception("Cannot save a table without a name")

        if None == self.data.database:
            raise Exception("Cannot save a table without a database name")
        self.data.type = "LOCAL"
        if None == self.config_directory:
            home = os.path.expanduser("~")
            if not os.path.exists(os.path.join(home, '.ddb')):
                os.makedirs(os.path.join(home, '.ddb'))
            home = os.path.join(home, '.ddb')
        else:
            home = self.config_directory

        dest_dir = os.path.join(home, self.data.database)
        if not os.path.exists(dest_dir):
            os.makedirs(dest_dir)

        if None == self.data.config:
            self.data.config = os.path.join(
                dest_dir, "{0}.ddb.yaml".format(self.data.name))
        yamlf_dump(data=self, file=self.data.config)
        return True


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
            if 'type' in yaml:
                self.type = yaml['type']
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

    def get_new_line(self):
        '''Return the correct line ending for the file format'''
        if self.new_line == 'UNIX':
            return '\n'
        elif self.new_line == 'WINDOWS':
            return '\r\n'
        else:
            return '\n'

        
        
# ############################################################################
# Module : database
# File   : ./source/ddb/configuration/database.py
# ############################################################################





class database:
    tables = []

    def __init__(self, config_file=None, show_config=False):
        self.curent_database = None
        self.tables = []
        is_file = False
        self.config_file = None
        if None != config_file and config_file != False:
            self.config_file = config_file
            self.reload_config()
            return

    def set_database(self, database_name):
        self.curent_database = database_name

    def get(self, table_name, database_name=None):
        """Get a Table structure in the database."""
        if None == database_name:
            database_name = self.get_curent_database()
        for c in self.tables:
            if c.data.name == table_name and database_name == c.data.database:
                return c
        return None

    def count(self):
        """Return a count ot tables in the database"""
        return len(self.tables)

    def temp_table(self, name=None, columns=[], delimiter=None):
        """Create a temporary table to preform operations in"""
        if None == name:
            name = "#table_temp"  # TODO make unique random name
        return table(name=name, columns=columns, database=self.get_curent_database(), field_delimiter=delimiter)

    def create_config(self, config_file):
        try:
            if False == os.path.exists(config_file):
                dirname = os.path.dirname(config_file)
                if False == os.path.exists(dirname):
                    os.makedirs(dirname)
            yaml_data = {}
            yamlf_dump(yaml_data, file=config_file)
            return
        except Exception as ex:
            print "Cant create configuration file: {0}".format(ex)

    def create_table_config(self, name, db, columns, delimiter=None):
        if None == self.config_file:
            raise Exception("Not using a config file")

        t = table(name=name, database=db, columns=columns,
                  field_delimiter=delimiter)
        t.save()
        self.add_config(t.data.path)

    def add_config(self, table_config=None, table=None):
        if None == self.config_file:
            raise Exception("Not using a config file")
        if not os.path.exists(self.config_file):
            self.create_config(self.config_file)

        if None != table_config:
            self.create_config(self.config_file)
            config = table(table_config)
            yaml_data = yamlf_load(file=self.config_file)
            db = config.data.database
            if None == db:
                db = self.get_default_database()

            if db not in yaml_data:
                yaml_data[db] = {}

            yaml_data[db][config.data.name] = {
                'name': config.data.name, 'path': table_config}
            yamlf_dump(yaml_data, file=self.config_file)

        if table is not None:
            yaml_data = yamlf_load(file=self.config_file)
            if None == yaml_data:
                yaml_data = {}
            db = table.data.database
            if None == db:
                db = self.get_default_database()

            if db not in yaml_data:
                yaml_data[db] = {}

            yaml_data[db][table.data.name] = {
                'name': table.data.name, 'path': table.data.config}
            yamlf_dump(yaml_data, file=self.config_file)
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
                     data_on=None,
                     temporary=None):
        if None == database_name:
            database_name = self.get_curent_database()
        exists = self.get(table_name, database_name)
        if None != exists:
            raise Exception("table already exists")

        if False == os.path.isfile(data_file):
            raise Exception("Data file does not exist")

        if not temporary:
            if None == self.config_file:
                raise Exception("Not using a config file")
            config_directory = os.path.dirname(self.config_file)
        else:
            config_directory = None


        t = table(name=table_name,
                  database=database_name,
                  columns=columns,
                  config_directory=config_directory,
                  field_delimiter=delimiter,
                  data_on=data_on,
                  comments=comments,
                  whitespace=whitespace,
                  errors=errors)
        t.data.path = data_file
        self.tables.append(t)
        if not temporary:
            res = t.save()
            self.add_config(table=t)
            if False == res:
                raise Exception("Couldn't save table configuation")
        return True

    def drop_table(self, table_name, database_name=None):
        if None == database_name:
            database_name = self.get_curent_database()
        for index in range(0, len(self.tables)):
            if self.tables[index].data.name == table_name and self.tables[index].data.database == database_name:
                if self.tables[index].data.type=="Temp":
                    self.tables.pop(index)
                    return True
                res = self.remove_config(table_object=self.tables[index])
                if False == res:
                    raise Exception("Failed to remove configuration for table")
                self.tables.pop(index)
                return True
                break
        raise Exception("Failed to drop table. Does not exist")

    def remove_config(self, table_config=None, table_object=None):
        try:
            if not os.path.exists(self.config_file):
                self.create_config(self.config_file)
            if table_object is None:
                config = table(table_config)
            else:
                config = table_object
            yaml_data = yamlf_load(file=self.config_file)
            db = config.data.database
            if None == db:
                db = self.get_default_database()

            if db not in yaml_data:
                yaml_data[db] = {}

            table_name = config.data.name
            if table_name in yaml_data[db]:
                yaml_data[db].pop(table_name, None)

            yamlf_dump(yaml_data, file=self.config_file)
            return True
        except Exception as ex:
            raise Exception("failed to remove table from db configuration")

    def reload_config(self):
        temp_tables = self.get_tables()
        table_swap = []
        for t in self.tables:
            if t.data.type == 'Temp':
                table_swap.append(t)

        for t in temp_tables:
            temp_table = table(table_config_file=t)
            if temp_table.active == False:
                warnings.warn("Table not loaded {0}.{1}".format(
                    temp_table.data.database, temp_table.data.name))
                continue
            table_swap.append(temp_table)

        self.tables = table_swap

    def get_tables(self):
        if None == self.config_file:
            return []

        if False == os.path.exists(self.config_file):
            self.create_config(self.config_file)

        tables = []

        if self.config_file:
            if False == os.path.exists(self.config_file):
                return tables
        else:
            return tables
        yaml_data = yamlf_load(file=self.config_file)
        if yaml_data != None:
            for db in yaml_data:
                if yaml_data[db] != None:
                    for table in yaml_data[db]:
                        tables.append(yaml_data[db][table]['path'])

        return tables

        
        
# ############################################################################
# Module : match
# File   : ./source/ddb/evaluate/match.py
# ############################################################################





class match():

    def evaluate_single_match(self,test, row, table):
        
        compare1 = None
        compare2 = None
        compare1_is_column = False
        compare2_is_column = False

        comparitor = test['c'].lower()

        for column in table.columns:
            if column.data.name == test['e1']:
                index = table.ordinals[column.data.name]
                compare1 = row[index]  # table.ordinals[].get_data_from_column(column,row)
                compare1_is_column = True
            if column.data.name == test['e2']:
                index = table.ordinals[column.data.name]
                compare2 = row[index]  # table.get_data_from_column(column,row)
                compare2_is_column = True
            if None != compare1 and None != compare2:
                break

        if not compare1_is_column and not compare2_is_column:
            raise Exception("expression invalid {0}".format(test))
                

        if None == compare1:
            compare1 = test['e1']
        if None == compare2:
            compare2 = test['e2']
        if None == compare1 and None == compare2:
            raise Exception("Where invalid {0}".format(test))

        if comparitor == '=' or comparitor == 'is':
            if compare1 == compare2:
                return True
        if comparitor == 'like':  # paritial match

            if True == compare1_is_column and True == compare2_is_column:
                raise Exception("Where invalid {0}, like cant be between 2 columns".format(test))

            if True == compare1_is_column:
                like = compare2
                data = compare1
            else:
                like = compare1
                data = compare2

            if None == like:
                return False
            if like[0] == '%':
                like_left = True
            else:
                like_left = False

            if like[-1] == '%':
                like_right = True
            else:
                like_right = False

            if True == like_right and True == like_left:
                if data.find(like[1:-1]) > -1:
                    return True
                else:
                    return False

            if True == like_left:
                if data[-(len(like) - 1):] == like[1:]:
                    return True
                else:
                    return False

            if True == like_right:
                if data[0:(len(like) - 1)] == like[0:-1]:
                    return True
                else:
                    return False

            return False
        if comparitor == '<':
            if compare1 < compare2:
                return True
        elif comparitor == '>':
            if compare1 > compare2:
                return True
        elif comparitor == '>=':
            if compare1 >= compare2:
                return True
        elif comparitor == '<=':
            if compare1 <= compare2:
                return True
        elif comparitor == '!=' or comparitor == '<>' or comparitor == 'not':
            if compare1 != compare2:
                return True

        return False


    def evaluate_match(self,query_object, row):
        table=query_object['table']
        where=query_object['meta']['where']
        if None == row:
            return False

        if 0 == len(where):
            return True
        success = None
        skip_section = False
        operation = ""
        for test in where:
            if 'and' in test and skip_section:
                continue
            else:
                skip_section = False

            operation = None
            if 'where' in test:
                operation = 'where'

            elif 'or' in test:
                operation = 'or'
                if success:
                    return True

            elif 'and' in test:

                operation = 'and'
                if not success:
                    skip_section = True
                    continue

            test_operation = test[operation]
            success = self.evaluate_single_match(test_operation, row, table)

        if success is None:
            return False
        return success

        
        
# ############################################################################
# Module : functions
# File   : ./source/ddb/functions/functions.py
# ############################################################################







def f_database(context):
    if None==context:
        raise Exception("No database instance. ")
    return context.database.get_curent_database()

def f_upper(context,arg):
    if None==context:
        raise Exception("No database instance. ")
    if not arg:
        return None
    return arg.upper()

def f_lower(context,arg):
    if None==context:
        raise Exception("No database instance. ")
    if not arg:
        return None
    return arg.lower()

def f_datetime(context,arg=None):
    if None==context:
        raise Exception("No database instance. ")
    return datetime.datetime.now()

def f_time(context,arg=None):
    if None==context:
        raise Exception("No database instance. ")
    return datetime.datetime.now().strftime('%H:%M:%S')

def f_date(context,arg=None):
    if None==context:
        raise Exception("No database instance. ")
    return datetime.datetime.now().strftime('%Y-%m-%d')

def f_version(context,version=None):
    if None==context:
        raise Exception("No database instance. ")
    if None==version:
        return 'GA.BB.LE'
    return version
        
def f_cat(context,arg1,arg2):
    if None==context:
        raise Exception("No database instance. ")
    if None ==arg1:
        arg1=''
    if None ==arg2:
        arg2=''
    return '{0}{1}'.format(arg1,arg2)


        
        
# ############################################################################
# Module : sql_engine
# File   : ./source/ddb/engine.py
# ############################################################################











def enum(**enums):
    return type('Enum', (), enums)


class engine:
    """A serverless flat file database engine"""
    
    def info(self,msg, arg1=None, arg2=None, arg3=None):
        if True == self.debug:
            print(msg, arg1, arg2, arg3)

    
    data_type = enum(COMMENT=1, ERROR=2, DATA=3, WHITESPACE=4)

    def __init__(self, config_file=None, query=None, debug=False, mode='array',output='term',output_file=None):
        self.debug = debug
        self.results = None
        self.mode = mode
        self.output=output
        self.output_file=output_file
        self.match=match()
        
        self.database = database(config_file=config_file)
        self.current_database = self.database.get_default_database()
        if None != query:
            self.query(query)
        


    def debugging(self, debug=False):
        self.debug = debug

    def define_table(self, table_name, database_name, columns, data_file, field_delimiter=None):
        """Progromatically define a table. Not saved to a configuration file, unless manualy activated"""
        t = table(database=database_name, columns=columns, name=table_name, data_file=data_file, field_delimiter=field_delimiter)
        self.database.tables.append(t)

    def has_configuration(self):
        if None == self.database:
            return False
        return True

    def query(self, sql_query):
        if False == self.has_configuration():
            raise Exception("No table found")
        self.results = None

        parser = lexer(sql_query, self.debug)
        if False == parser.query_objects:
            raise Exception("Invalid SQL")

        start = time.clock()
        for query_object in parser.query_objects:
            self.info("Engine: query_object", query_object)
            if query_object['mode'] == "show tables":
                self.results = method_show_tables(self,self.database)
            elif query_object['mode'] == "show columns":
                self.results = method_show_columns(self,self.database, query_object)
            
            
            elif query_object['mode'] == 'select':
                self.results = method_select(self,query_object, parser)
            
            elif query_object['mode'] == 'insert':
                self.results = method_insert(self,query_object)

            elif query_object['mode'] == 'update':
                self.results = method_update(self,query_object)

            elif query_object['mode'] == 'delete':
                self.results = method_delete(self,query_object)

            elif query_object['mode'] == 'use':
                self.results = method_use(self,query_object)

            elif query_object['mode'] == 'set':
                self.results = method_set(self,query_object)

            elif query_object['mode'] == 'drop':
                self.results = method_drop_table(self,query_object)

            elif query_object['mode'] == 'create':
                self.results = method_create_table(self,query_object)

            elif query_object['mode'] == 'update table':
                self.results = method_update_table(self,query_object)

            elif query_object['mode'] == 'describe table':
                self.results = method_describe_table(self,query_object)
                    
        end = time.clock()
        self.results.start_time=start
        self.results.end_time=end
        self.results.time=end-start
        return self.results

    def change_database(self, database_name):
        query = "use {0}".format(database_name)
        results = self.query(query)
        if None == results:
            return False
        return True
        
    def add_error(self,error):
        self.info(error)
    

    
    

        
        
# ############################################################################
# Module : methods-records_core
# File   : ./source/ddb/methods/record_core.py
# ############################################################################



def process_line(context, query_object, line, line_number=0):
        err = None
        column_len = query_object['table'].column_count()
        line_cleaned = line.rstrip()
        line_data = None
        match_results=False
        if query_object['table'].data.starts_on_line >= line_number:
            line_type = context.data_type.COMMENT
            line_data = line
            match=None
        else:
            line_type = context.data_type.DATA
            match=True
        if match:

            if not line_cleaned:
                if True == query_object['table'].visible.whitespace:
                    line_data = ['']
                line_type = context.data_type.WHITESPACE
            else:
                if line_cleaned[0] in query_object['table'].delimiters.comment:
                    if True == query_object['table'].visible.comments:
                        line_data = [line_cleaned]
                    line_type = context.data_type.COMMENT
                else:
                    line_data = line_cleaned.split(query_object['table'].delimiters.field)
                    cur_column_len = len(line_data)
                    if cur_column_len != column_len:
                        if cur_column_len > column_len:
                            err = "Table {2}: Line #{0}, {1} extra Column(s)".format(line_number, cur_column_len - column_len, query_object['table'].data.name)
                        else:
                            err = "Table {2}: Line #{0}, missing {1} Column(s)".format(line_number, column_len - cur_column_len, query_object['table'].data.name)
                        line_type = context.data_type.ERROR

                        if True == query_object['table'].visible.errors:
                            line_data = line_cleaned
                        else:
                            line_data = None
                        line_type = context.data_type.ERROR
                    if None != query_object['table'].delimiters.block_quote:
                        line_data_cleaned = []
                        for d in line_data:
                            line_data_cleaned.append(d[1:-1])
                        line_data = line_data_cleaned

            if 'where' not in query_object['meta']:
                match_results = True
            else:
                if line_type == context.data_type.DATA:
                    match_results = context.match.evaluate_match(query_object, line_data,)
                else:
                    match_results = False
            if query_object['table'].visible.whitespace is False and line_type==context.data_type.WHITESPACE:
                match_results=False
            elif query_object['table'].visible.comments is False and line_type==context.data_type.COMMENT:
                match_results=False
            elif query_object['table'].visible.errors is False and line_type==context.data_type.ERROR:
                match_results=False


    return {'data': line_data, 'type': line_type, 'raw': line_cleaned, 'line_number': line_number, 'match': match_results, 'error': err}

  
def swap_files(target, temp):
    os.remove(target)
    if os.path.exists(target):
        raise Exception("Deleting target file {0} failed".format(target))
    os.rename(temp, target)
    if os.path.exists(temp):
        raise Exception("Renaming temp file {0} failed".format(temp))

class query_results:
    def __init__(self,success=False,affected_rows=0,data=None,error=None):
        self.success=success
        self.affected_rows=affected_rows
        self.data=[]
        self.error=None
        self.data_length=0
        self.columns=[]

        if data and data.results:
            self.data=data.results
            self.data_length=len(data.results)

        if data:
            self.columns = data.get_columns_display()
            


        
        
# ############################################################################
# Module : methods-records-delete
# File   : ./source/ddb/methods/record_delete.py
# ############################################################################




def method_delete(context, query_object):
    try:
        table_name = query_object['meta']['from']['table']
        query_object['table'] = context.database.get(table_name)
        if None == query_object['table']:
            raise Exception("Table '{0}' does not exist.".format(table_name))


        line_number = 1
        affected_rows = 0
        temp_file_name = "del_" + next(tempfile._get_candidate_names())
        with open(query_object['table'].data.path, 'r') as content_file:
            with open(temp_file_name, 'w') as temp_file:
                for line in content_file:
                    processed_line = process_line(context,query_object, line, line_number)
                    if None != processed_line['error']:
                        context.add_error(processed_line['error'])
                    line_number += 1
                    if True == processed_line['match']:
                        affected_rows += 1
                        continue
                    temp_file.write(processed_line['raw'])
                    temp_file.write(query_object['table'].delimiters.get_new_line())
        swap_files(query_object['table'].data.path, temp_file_name)
        return  query_results(success=True,affected_rows=affected_rows)
    except Exception as ex:
        return  query_results(success=False, error=ex)

    
        
        
# ############################################################################
# Module : methods-records-insert
# File   : ./source/ddb/methods/record_insert.py
# ############################################################################




def method_insert(context, query_object):
    try:
        if 'database' in query_object['meta']['into']:
            context.info('Database specified')
            database_name = query_object['meta']['into']['database']
        else:
            context.info('Using curent database context')
            database_name = context.database.get_curent_database()

        table_name = query_object['meta']['into']['table']
        query_object['table'] = context.database.get(table_name,database_name)
        if None == query_object['table']:
            raise Exception("Table '{0}' does not exist.".format(table_name))

        line_number = 1
        affected_rows = 0
        requires_new_line = False
        temp_file_name = "INS_" + next(tempfile._get_candidate_names())
        
        with open(query_object['table'].data.path, 'r') as content_file:
            with open(temp_file_name, 'w') as temp_file:
                for line in content_file:
                    processed_line = process_line(context,query_object, line, line_number)
                    if None != processed_line['error']:
                        context.add_error(processed_line['error'])
                    line_number += 1
                    temp_file.write(processed_line['raw'])
                    temp_file.write(query_object['table'].delimiters.get_new_line())

                    requires_new_line = False

                results = create_single(context,query_object, temp_file, requires_new_line)
                if True == results:
                    affected_rows += 1
        swap_files(query_object['table'].data.path, temp_file_name)
        return query_results(success=True,affected_rows=affected_rows)
    except Exception as ex:
        print(ex)
        return query_results(success=False, error=ex)
    
        

def create_single(context, query_object, temp_file, requires_new_line):
    err = False
    if len(query_object['meta']['columns']) != query_object['table'].column_count():
        context.add_error("Cannot insert, column count does not match table column count")
    else:
        if len(query_object['meta']['values']) != query_object['table'].column_count():
            context.add_error("Cannot insert, column value count does not match table column count")
        else:
            new_line = ''
            err = False
            for c in range(0, len(query_object['meta']['columns'])):
                column_name = query_object['table'].get_column_at_data_ordinal(c)
                found = False
                for c2 in range(0, len(query_object['meta']['columns'])):
                    if query_object['meta']['columns'][c2]['column'] == column_name:
                        found = True
                        if c > 0:
                            new_line += '{0}'.format(query_object['table'].delimiters.field)
                        new_line += '{0}'.format(query_object['meta']['values'][c2]['value'])
                if False == found:
                    context.add_error("Cannot insert, column in query not found in table: {0}".format(column_name))
                    err = True
                    break
            if False == err:
                if True == requires_new_line:
                    temp_file.write(query_object['table'].delimiters.get_new_line())
                temp_file.write(new_line)
                temp_file.write(query_object['table'].delimiters.get_new_line())
    if False == err:
        return True
    else:
        return False

        
        
# ############################################################################
# Module : methods-records-select
# File   : ./source/ddb/methods/record_select.py
# ############################################################################





context_sort=[]

def method_select(context, query_object, parser):
    try:
        context.info(query_object)
        select_validate_columns_and_from(context,query_object,parser)

        temp_table = context.database.temp_table()
        
        add_table_columns(context,query_object,temp_table)
       
        set_ordinals(context,query_object)


        temp_data=select_process_file(context,query_object)


        temp_data=order_by(context,query_object,temp_data)

        temp_data=distinct(context,query_object,temp_data)
        
        
        temp_data = limit(context, query_object, temp_data)

        temp_table.results=temp_data

        return query_results(success=True,data=temp_table)
    except Exception as ex:
        print ex
        return query_results(success=False,error=ex)   


def select_process_file(context,query_object):
    has_columns = select_has_columns(context,query_object)
    has_functions = select_has_functions(context,query_object)
    table=None
    line_number = 1
    data=[]
    if True == has_columns:
        if 'table' in  query_object:
            table= query_object['table']
            file_path =table.data.path
        else:
            raise Exception ('table configuration has no data file')
        with open(file_path, 'r') as content_file:
            for line in content_file:
                processed_line = process_line(context,query_object, line, line_number)

                if False == processed_line['match']:
                    continue
                
                if None != processed_line['data']:
                    restructured_line = process_select_row(context,query_object,processed_line) 
                    data.append(restructured_line)

                line_number += 1

    if False == has_columns and True == has_functions:
        row=process_select_row(context,query_object,None)
        data.append(row)

    return data



def select_validate_columns_and_from(context, query_object, parser):
    has_functions = select_has_functions(context,query_object)
    has_columns = select_has_columns(context,query_object)

    if False == has_columns and 'from' in query_object['meta']:
        raise Exception("Invalid FROM, all columns are functions")

    if False == has_columns and False == has_functions:
        raise Exception("no columns defined in query")


    if True == has_columns:
        if 'from' in query_object['meta']:
            if 'database' in query_object['meta']['from']:
                context.info('Database specified')
                database_name=query_object['meta']['from']['database']
            else:
                context.info('Using curent database context')
                database_name=context.database.get_curent_database()

            table_name = query_object['meta']['from']['table']
            query_object['table'] = context.database.get(table_name,database_name)
            if None == query_object['table']:
                raise Exception("Table '{0}' does not exist.".format(table_name))
            table_columns = query_object['table'].get_columns()
            parser.expand_columns(query_object, table_columns)
            column_len = query_object['table'].column_count()
            if column_len == 0:
                raise Exception("No defined columns in configuration")
        else:
            raise Exception("Missing FROM in select")



def select_has_columns(context,query_object):
    for c in query_object['meta']['columns']:
        if 'column' in c:
            context.info("Has columns, needs a table")
            return  True
    return False
            
def select_has_functions(context,query_object):
    for c in query_object['meta']['columns']:
        if 'function' in c:
            context.info("Has functions, doesnt need a table")
            return True
    return False


def add_table_columns(context,query_object,temp_table):
    for column in query_object['meta']['columns']:
        display = None
        if 'display' in column:
            display = column['display']
            context.info("RENAME COLUMN", display)

        if 'column' in column:
            context.info("adding data column")
            temp_table.add_column(column['column'], display)
        if 'function' in column:
            context.info("adding function column")
            temp_table.add_column(column['function'], display)    

def set_ordinals(context,query_object):
    ordinals={}
    index=0
    for column in query_object['meta']['columns']:
        if 'display' in column:
            name=column['display']
            if '{0}'.format(name) in ordinals:
                raise Exception("ambigious column {0}".format(name))
            ordinals['{0}'.format(name)]=index                
        if  'function' in column:
            name=column['function']
            if '{0}'.format(name) in ordinals:
                raise Exception("ambigious column {0}".format(name))
            ordinals['{0}'.format(name)]=index                
        if 'column' in column:
            name=column['column']
            if '{0}'.format(name) in ordinals:
                raise Exception("ambigious column {0}".format(name))
            ordinals['{0}'.format(name)]=index                
        else:
            continue
        ordinals['{0}'.format(name)]=index                
        index+=1
    query_object['meta']['ordinals']=ordinals

def order_by(context,query_object,data):
    global context_sort

    if 'order by' not in query_object['meta']:
        return data
    context.info("Select has Order By")
    context_sort = []
    for c in query_object['meta']['order by']:
        if c['column'] not in query_object['meta']['ordinals']:
            raise Exception ("ORDER BY column not present in the result set")
        ordinal = query_object['meta']['ordinals'][c['column']]
        direction = 1
        if 'asc' in c:
            direction = 1
        elif 'desc' in c:
            direction = -1
        context_sort.append([ordinal, direction])
    
    context.info(context_sort)
    ordered_data = sorted(data, sort_cmp)
    return ordered_data


def group(context,data):
    return data
       

def distinct(context,query_object,data):
    if 'distinct' not in query_object['meta']:
        return data

    context.info("Select has Distinct")
    group=[]
    for item in data:
        no_item=True
        for group_item in group:
            if compare_data(context,group_item['data'],item['data']):
                no_item=None
                break
        if no_item:
            group.append(item)
    return group    


def process_select_row(context,query_object,processed_line):
    row=[]
    has_columns = select_has_columns(context,query_object)

    for c in query_object['meta']['columns']:
        if 'column' in c:
            if None != processed_line:
                row.append(query_object['table'].get_data_by_name(c['column'], processed_line['data']))
        elif 'function' in c:
            if c['function'] == 'database':
                row.append(f_database(context))
            elif c['function'] == 'datetime':
                    row.append(f_datetime(context))
            elif c['function'] == 'date':
                    row.append(f_date(context))
            elif c['function'] == 'time':
                    row.append(f_time(context))
            elif c['function'] == 'version':
                    row.append(f_version(context,__version__))
    if None != processed_line:                    
        line_type=processed_line['type']
        error= processed_line['error']
        raw= processed_line['raw']
    else:
        line_type=context.data_type.DATA
        error= None
        raw= None
    return {'data': row, 'type': line_type, 'error': error,'raw':raw} 


def sort_cmp( x, y):
    for c in context_sort:
        ordinal = c[0]
        direction = c[1]
        if x['data'][ordinal] == y['data'][ordinal]:
            continue

        if x['data'][ordinal] < y['data'][ordinal]:
            return -1 * direction
        else:
            return 1 * direction
    return 0
    
def limit(context, query_object, data):
    index = 0
    length = None

    if 'limit' in query_object['meta']:
        if 'start' in query_object['meta']['limit']:
            index = query_object['meta']['limit']['start']
        if 'length' in query_object['meta']['limit']:
            length = query_object['meta']['limit']['length']

    context.info("Limit:{0},Length:{1}".format(index, length))    
    if None == index:
        index = 0
    if None == length:
        length = len(data) - index

    data_length = len(data)
    if index >= data_length:
        return []
    if index + length > data_length:
        length = data_length - index
    return data[index:index + length]

def compare_data(context,data1, data2):
    if data1 is None or data2 is None:
        return None
    if (not isinstance(data1, dict)) or (not isinstance(data2, dict)):
        if len(data1)!=len(data2):
            return None
        for index in range(0,len(data1)):
            if data1[index]!=data2[index]:
                return None
    else:
        shared_keys = set(data2.keys()) & set(data2.keys())
        if not ( len(shared_keys) == len(data1.keys()) and len(shared_keys) == len(data2.keys())):
            return None

        for key in data1.keys():
            if data1[key] != data2[key]:
                return None
    return True



        
        
# ############################################################################
# Module : methods-records-show-columns
# File   : ./source/ddb/methods/record_show_columns.py
# ############################################################################




def method_show_columns(context,database, query_object):
    try:
        table = database.get(query_object['meta']['from']['table'])
        temp_table = database.temp_table(columns=['table', 'column'])

        for c in table.columns:
            columns = {'data': [table.data.name, c.data.name], 'type': context.data_type.DATA, 'error': None}
            temp_table.append_data(columns)
        
        return query_results(success=True,data=temp_table)
    except Exception as ex:
        return query_results(success=False,error=ex)


        
        
# ############################################################################
# Module : methods-records-show-tables
# File   : ./source/ddb/methods/record_show_tables.py
# ############################################################################




def method_show_tables(context,database):
    try:
        temp_table = database.temp_table(columns=['database', 'table'])
        for t in database.tables:
            columns = [t.data.database, t .data.name]
            temp_table.append_data({'data': columns, 'type': context.data_type.DATA, 'error': None})
       
        return query_results(success=True,data=temp_table)
    except Exception as ex:
        return query_results(success=False,error=ex)

        
        
# ############################################################################
# Module : methods-records-update
# File   : ./source/ddb/methods/record_update.py
# ############################################################################




def update_single(context,query_object, temp_file, requires_new_line, processed_line):
    err = False
    new_line = ''
    err = False

    for c2 in range(0, len(query_object['meta']['set'])):
        column_name = query_object['meta']['set'][c2]['column']
        if None == query_object['table'].get_column_by_name(column_name):
            context.add_error("column in update statement does not exist in table: {0}".format(column_name))
            err = True

    if False == err:
        for c in range(0, query_object['table'].column_count()):
            column_name = query_object['table'].get_column_at_data_ordinal(c)
            value = processed_line['data'][c]
            for c2 in range(0, len(query_object['meta']['set'])):
                if query_object['meta']['set'][c2]['column'] == column_name:
                    value = query_object['meta']['set'][c2]['expression']
            if c > 0:
                new_line += '{0}'.format(query_object['table'].delimiters.field)
            new_line += '{0}'.format(value)

    if False == err:
        if True == requires_new_line:
            temp_file.write(query_object['table'].delimiters.get_new_line())
        temp_file.write(new_line)
        temp_file.write(query_object['table'].delimiters.get_new_line())
    if False == err:
        return True
    else:
        return False

def method_update(context, query_object):
    try:
        if 'database' in query_object['meta']['update']:
            context.info('Database specified')
            database_name = query_object['meta']['update']['database']
        else:
            context.info('Using curent database context')
            database_name = context.database.get_curent_database()

        table_name = query_object['meta']['update']['table']
        query_object['table'] = context.database.get(table_name,database_name)
        if None == query_object['table']:
            raise Exception("Table '{0}' does not exist.".format(table_name))


    
        temp_file_name = "UP_" + next(tempfile._get_candidate_names())
        line_number = 1
        affected_rows = 0
        with open(query_object['table'].data.path, 'r') as content_file:
            with open(temp_file_name, 'w') as temp_file:
                for line in content_file:
                    processed_line = process_line(context,query_object, line, line_number)
                    if None != processed_line['error']:
                        context.add_error(processed_line['error'])
                    line_number += 1
                    if True == processed_line['match']:
                        results = update_single(context,query_object, temp_file,  False, processed_line)
                        if True == results:
                            affected_rows += 1
                        continue
                    temp_file.write(processed_line['raw'])
                    temp_file.write(query_object['table'].delimiters.get_new_line())
    
        swap_files(query_object['table'].data.path, temp_file_name)
        return query_results(affected_rows=affected_rows,success=True)
    except Exception as ex:
        return query_results(success=False,error=ex)




        
        
# ############################################################################
# Module : methods-database-set
# File   : ./source/ddb/methods/database_set.py
# ############################################################################




def method_set(context, query_object):
    context.info("set")
    try:
        return query_results(success=True)
    except Exception as ex:
        return query_results(success=False,error=ex)

        
        
# ############################################################################
# Module : methods-database-use
# File   : ./source/ddb/methods/database_use.py
# ############################################################################




def method_use(context, query_object):
    context.info("Use")
    try:
        target_db = query_object['meta']['use']['table']
        if context.database.get_curent_database()!=target_db:
            context.database.set_database(target_db)
            temp_table = context.database.temp_table()
            temp_table.add_column('changed_db')
            data = {'data': [target_db], 'type': context.data_type.DATA, 'error': None}
            temp_table.append_data(data)
        return query_results(success=True,data=temp_table)
    except Exception as ex:
        return query_results(success=False,error=ex)
        
        
# ############################################################################
# Module : methods-table-structure-create
# File   : ./source/ddb/methods/table_create.py
# ############################################################################





def method_create_table(context, query_object):
    context.info("Create Table")
    try:

        if 'database' in query_object['meta']:
            context.info('Database specified')
            database_name = query_object['meta']['database']
        else:
            context.info('Using curent database context')
            database_name = context.database.get_curent_database()

        columns = []
        if 'columns' not in query_object['meta']:
            raise Exception("Missing columns, cannot create table")

        for c in query_object['meta']['columns']:
            columns.append(c['column'])
        context.info("Columns to create", columns)

        if 'temporary' in query_object['meta']:
            temporary = True
            context.info("Creating temporary table")
        else:
            temporary = None

        found_delimiter = None
        found_comments = None
        found_whitespace = None
        found_data_on = None
        found_errors = None
        if 'delimiter' in query_object['meta']:
            found_delimiter = query_object['meta']['delimiter']
        if 'whitespace' in query_object['meta']:
            found_whitespace = query_object['meta']['whitespace']
        if 'comments' in query_object['meta']:
            found_comments = query_object['meta']['comments']
        if 'errors' in query_object['meta']:
            found_errors = query_object['meta']['errors']
        if 'data_starts_on' in query_object['meta']:
            found_data_on = query_object['meta']['data_starts_on']
            
        results = context.database.create_table(table_name=query_object['meta']['table'],
                                                database_name=database_name,
                                                columns=columns,
                                                data_file=query_object['meta']['file'],
                                                delimiter=found_delimiter,
                                                comments=found_comments,
                                                errors=found_errors,
                                                whitespace=found_whitespace,
                                                data_on=found_data_on,
                                                temporary=temporary
                                                )

        return query_results(success=results)
    except Exception as ex:
        print("Table Creation Error",ex)
        return query_results(success=False, error=ex)

        
        
# ############################################################################
# Module : methods-table-structure-describe
# File   : ./source/ddb/methods/table_describe.py
# ############################################################################




def method_describe_table(context, query_object):
    """Populates metadata related to a table
    returns: table"""
    context.info("Describe Table")
    try:
        temp_table = context.database.temp_table()
        table_name=query_object['meta']['describe']['table']
        target_table= context.database.get(table_name)
        temp_table.add_column('option')
        temp_table.add_column('value')
        
        
        temp_table.append_data({'data':['active',target_table.active], 'type': context.data_type.DATA, 'error': None})
        temp_table.append_data({'data':['table_name',target_table.data.name], 'type': context.data_type.DATA, 'error': None})
        temp_table.append_data({'data':['database',target_table.data.database], 'type': context.data_type.DATA, 'error': None})
        temp_table.append_data({'data':['data_file',target_table.data.path], 'type': context.data_type.DATA, 'error': None})
        temp_table.append_data({'data':['type',target_table.data.type], 'type': context.data_type.DATA, 'error': None})
        temp_table.append_data({'data':['config_file',target_table.data.config], 'type': context.data_type.DATA, 'error': None})
        temp_table.append_data({'data':['data_starts_on',target_table.data.starts_on_line], 'type': context.data_type.DATA, 'error': None})
        temp_table.append_data({'data':['field_delimiter'  ,target_table.delimiters.field], 'type': context.data_type.DATA, 'error': None})
        temp_table.append_data({'data':['comments_visible',target_table.visible.comments], 'type': context.data_type.DATA, 'error': None})
        temp_table.append_data({'data':['errors_visible',target_table.visible.errors], 'type': context.data_type.DATA, 'error': None})
        temp_table.append_data({'data':['whitespace_visible',target_table.visible.whitespace], 'type': context.data_type.DATA, 'error': None})
        return query_results(success=True,data=temp_table)
    except Exception as ex:
        return query_results(success=False,error=ex)




        
        
# ############################################################################
# Module : methods-table-structure-drop
# File   : ./source/ddb/methods/table_drop.py
# ############################################################################




def method_drop_table(context, query_object):
    context.info("Drop Table")
    try:
        table_name=query_object['meta']['drop']['table']
        if 'database' in query_object['meta']['drop']:
            context.info('Database specified')
            database_name = query_object['meta']['drop']['database']
        else:
            context.info('Using curent database context')
            database_name = context.database.get_curent_database()

        results = context.database.drop_table(table_name=table_name,database_name=database_name)
        return query_results(success=results)
    except Exception as ex:
        return query_results(success=False,error=ex)

        
        
# ############################################################################
# Module : methods-table-structure-update
# File   : ./source/ddb/methods/table_update.py
# ############################################################################




def method_update_table(context, query_object):
    context.info("Update Table")
    try:
        columns = None  
        if 'columns'  in  query_object['meta'] :
            columns = []
            for c in query_object['meta']['columns']:
                columns.append(c['column'])
        
        table_name=query_object['meta']['update']['table']

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

        target_table= context.database.get(table_name)
        target_table.update(columns=columns,
                            data_file=found_file,
                            field_delimiter=found_delimiter,
                            comments=found_comments,
                            whitespace=found_whitespace,
                            errors=found_errors,
                            data_on=found_data_on)
        results=target_table.save()
    
        return query_results(success=results)
    except Exception as ex:
        return query_object(success=False,error=ex)


        
        
# ############################################################################
# Module : output
# File   : ./source/ddb/output/factory.py
# ############################################################################





class output_factory:

    def __init__(self,query_results,output='term',output_file=None):
            """display results in different formats
            if output_file==None then everything is directed to stdio

            output=(bash|term|yaml|json|xml)
            output_file= None or file to write to
            """        
            if None==query_results:
                return
            
            mode=output.lower()
            if 'bash'==mode:
                self.format_bash(query_results,output_file)
            
            elif 'term'==mode:
                self.format_term(query_results,output_file)
            
            elif 'raw'==mode:
                self.format_raw(query_results,output_file)
            
            elif 'yaml'==mode:
                self.format_yaml(query_results,output_file)
            
            elif 'json'==mode:
                self.format_json(query_results,output_file)
            
            elif 'xml'==mode:
                self.format_xml(query_results,output_file)
            else: 
                self.format_term(query_results,output_file)


    def format_term(self,query_results,output_file):
        """ouput results data in the term format"""
        try:
            if query_results.columns:
                flextable(data=query_results.data,columns=query_results.columns)
            if True == query_results.success:
                print("executed in {0:.6f}, {1} rows returned".format(query_results.time,query_results.data_length))
            else:
                print("Query Failed")

        except Exception as ex:
            print("TERM Formatting: {0}".format(ex))

    def format_bash(self,query_results,output_file):
        """ouput results data in the bash format"""
        data=query_results.data
        
        name="ddb"

        print ("{0}_row_length={1}".format(name,len(data)))
        print ("{0}_column_length={1}".format(name,len(query_results.columns)))
        print ("")

        column_index=0
        for column in query_results.columns:
            print("{0}_columns['{1}']='{2}'".format(name,column_index,column))
            column_index+=1


        row_index=0
        for row in data:
            for column_index in range(0,len(query_results.columns)):
                print('{0}_data[{1}][{2}]="{3}"'.format(name,row_index,column_index,row['data'][column_index]))
            row_index+=1
        

    def format_raw(self,query_results,output_file):
        """ouput results data in the yaml format"""
        print(query_results.data)
        if not output_file:
            for row in query_results.data:
                if 'raw' in row:
                    print(row['raw'].rstrip())
        else:
            with open(output_file, "w") as write_file:
                for row in query_results.data:
                    if 'raw' in row:
                        write_file.write(row['raw'])

    def format_yaml(self,query_results,output_file):
        """ouput results data in the yaml format"""
        results=query_results.data
        factory=factory_yaml()
        dump=factory.dump(results)
        if not output_file:
            print dump
        else:
            with open(output_file, "w") as write_file:
                write_file.write(dump)

    def format_json(self,query_results,output_file):
        """ouput results data in the json format"""
        results=query_results.data
        factory=factory_json()
        dump=factory.dumps(results)
        if not output_file:
            print dump
        else:
            with open(output_file, "w") as write_file:
                write_file.write(dump)
        
    def format_xml(self,query_results,output_file):
        """ouput results data in the xml format"""
        results=query_results.data
        factory=factory_xml()
        dump=factory.dumps({'data':results})
        if not output_file:
            print dump
        else:
            with open(output_file, "w") as write_file:
                write_file.write(dump)
        
        
# ############################################################################
# Module : factory_term
# File   : ./source/ddb/output/factory_term.py
# ############################################################################




class flextable:

    def escape(c):
        return u'\033[{}m'.format(c)

    def enum(**enums):
        return type('Enum', (), enums)

    attributes=enum( BOLD    =escape(1),
                DIM          =escape(2),
                UNDERLINED   =escape(4),
                BLINK        =escape(5),
                REVERSE      =escape(7),
                HIDDEN       =escape(8))
        
    reset=enum( ALL          =escape(0),
                BOLD         =escape(21),
                DIM          =escape(22),
                UNDERLINED   =escape(24),
                BLINK        =escape(25),
                REVERSE      =escape(27),
                HIDDEN       =escape(28))

    fg=enum(    DEFAULT      =escape(39),
                BLACK        =escape(30),
                RED          =escape(31),
                GREEN        =escape(32),
                YELLOW       =escape(33),
                BLUE         =escape(34),
                MAGENTA      =escape(35),
                CYAN         =escape(36),
                LIGHT_GRAY   =escape(37),
                DARK_GRAY    =escape(90),
                LIGHT_RED    =escape(91),
                LIGHT_GREEN  =escape(92),
                LIGHT_YELLOW =escape(93),
                LIGHT_BLUE   =escape(94),
                LIGHT_MAGENTA=escape(95),
                LIGHT_CYAN   =escape(96),
                WHITE        =escape(97))

    bg=enum(    DEFAULT      =escape(49),
                BLACK        =escape(40),
                RED          =escape(41),
                GREEN        =escape(42),
                YELLOW       =escape(43),
                BLUE         =escape(44),
                MAGENTA      =escape(45),
                CYAN         =escape(46),
                LIGHT_GRAY   =escape(47),
                DARK_GRAY    =escape(100),
                LIGHT_RED    =escape(101),
                LIGHT_GREEN  =escape(102),
                LIGHT_YELLOW =escape(103),
                LIGHT_BLUE   =escape(104),
                LIGHT_MAGENTA=escape(105),
                LIGHT_CYAN   =escape(106),
                WHITE        =escape(107))

    @staticmethod
    def colors(foreground,background,dim=None,bold=None):
        color=''
        if dim !=None:
            color+=flextable.attributes.DIM
        if bold !=None:
            color+=flextable.attributes.BOLD
            
        if None != foreground:
            if foreground.upper() == 'DEFAULT' :
                color+=flextable.fg.DEFAULT
            if foreground.upper() == 'BLACK' :
                color+=flextable.fg.BLACK
            if foreground.upper() == 'RED' :
                color+=flextable.fg.RED
            if foreground.upper() == 'GREEN' :
                color+=flextable.fg.GREEN
            if foreground.upper() == 'YELLOW' :
                color+=flextable.fg.YELLOW
            if foreground.upper() == 'BLUE' :
                color+=flextable.fg.BLUE
            if foreground.upper() == 'MAGENTA' :
                color+=flextable.fg.MAGENTA
            if foreground.upper() == 'CYAN' :
                color+=flextable.fg.CYAN
            if foreground.upper() == 'LIGHT GRAY' :
                color+=flextable.fg.LIGHT_GRAY
            if foreground.upper() == 'DARK GRAY' :
                color+=flextable.fg.DARK_GRAY
            if foreground.upper() == 'LIGHT RED' :
                color+=flextable.fg.LIGHT_RED
            if foreground.upper() == 'LIGHT GREEN' :
                color+=flextable.fg.LIGHT_GREEN
            if foreground.upper() == 'LIGHT YELLOW' :
                color+=flextable.fg.LIGHT_YELLOW
            if foreground.upper() == 'LIGHT BLUE' :
                color+=flextable.fg.LIGHT_BLUE
            if foreground.upper() == 'LIGHT MAGENTA' :
                color+=flextable.fg.LIGHT_MAGENTA
            if foreground.upper() == 'LIGHT CYAN' :
                color+=flextable.fg.LIGHT_CYAN
            if foreground.upper() == 'WHITE' :
                color+=flextable.fg.WHITE
        if None != background:
            if  background.upper() == 'DEFAULT' :
                color+=flextable.bg.DEFAULT
            if  background.upper() == 'BLACK' :
                color+=flextable.bg.BLACK
            if  background.upper() == 'RED' :
                color+=flextable.bg.RED
            if  background.upper() == 'GREEN' :
                color+=flextable.bg.GREEN
            if  background.upper() == 'YELLOW' :
                color+=flextable.bg.YELLOW
            if  background.upper() == 'BLUE' :
                color+=flextable.bg.BLUE
            if  background.upper() == 'MAGENTA' :
                color+=flextable.bg.MAGENTA
            if  background.upper() == 'CYAN' :
                color+=flextable.bg.CYAN
            if  background.upper() == 'LIGHT GRAY' :
                color+=flextable.bg.LIGHT_GRAY
            if  background.upper() == 'DARK GRAY' :
                color+=flextable.bg.DARK_GRAY
            if  background.upper() == 'LIGHT RED' :
                color+=flextable.bg.LIGHT_RED
            if  background.upper() == 'LIGHT GREEN' :
                color+=flextable.bg.LIGHT_GREEN
            if  background.upper() == 'LIGHT YELLOW' :
                color+=flextable.bg.LIGHT_YELLOW
            if  background.upper() == 'LIGHT BLUE' :
                color+=flextable.bg.LIGHT_BLUE
            if  background.upper() == 'LIGHT MAGENTA' :
                color+=flextable.bg.LIGHT_MAGENTA
            if  background.upper() == 'LIGHT CYAN' :
                color+=flextable.bg.LIGHT_CYAN
            if  background.upper() == 'WHITE' :
                color+=flextable.bg.WHITE
        return color


    class flextable_style:
        def __init__(self,style='single'):
            self.whitespace=''
            self.line_ending='LRCF'
            self.color=flextable.modes()
            self.characters=flextable.characters(self.color.default,style)

    class color:
        def __init__(self,foreground=None,background=None,text=None,dim=None,bold=None,default=None):
            self.foreground=foreground
            self.background=background
            self.dim=dim
            self.bold=bold
            self.reset=flextable.reset.ALL
            if None != default :
                if None== foreground:
                    foreground=default.foreground
                if None== background:
                    background=default.background
                if None== dim:
                    dim=default.dim
                if None == bold:
                    bold=default.bold
                    
            self.color=flextable.colors(foreground=foreground,background=background,dim=dim,bold=bold)
            if None !=text:
                if text.rstrip()=='': 
                    text=None
            self.text=text
                    
        
        def render(self,text=None, length=None,fill_character=' ',override=None,use_color=True):
            if text==None:
                text=self.text

    
            if None == text:
                text=''
            
            text=u'{}'.format(text)
            text=text.replace(u'\t',u'       ')
            
            text=text.rstrip()
            if length!=None:
                length=int(length)
                text=text[:length].ljust(length,fill_character)
            if use_color is False or use_color is None:
                return text
            if None!=override:
                return u"{0}{1}".format(override.color,text)    
            return u"{0}{1}{2}".format(self.color,text,self.reset)

    class modes:
        def __init__(self):
            self.default  =flextable.color('blue'      )
            self.error    =flextable.color('red'        ,bold=True,default=self.default)
            self.overflow =flextable.color('yellow'     ,default=self.default)
            self.comment  =flextable.color('yellow'     ,default=self.default)
            self.data     =flextable.color('light gray' ,default=self.default)
            self.active   =flextable.color('white'      ,default=self.default)
            self.edit     =flextable.color('cyan'       ,default=self.default)
            self.disabled =flextable.color('dark gray'  ,default=self.default)


    class characters:
        class char_walls:
            
            def __init__(self,default=None,single=True):
                if single is True:
                    l=u'│'
                    r=u'│'
                    t=u'─'
                    b=u'─'
                else:
                    l=u'║'
                    r=u'║'
                    t=u'═'
                    b=u'═'
                self.left   =flextable.color(text=l,default=default)
                self.right  =flextable.color(text=r,default=default)
                self.top    =flextable.color(text=t,default=default)
                self.bottom =flextable.color(text=b,default=default)
        class char_center:
            def __init__(self,default=None,single=True):
                if single is True:
                    c=u'┼'
                    l=u'├'
                    r=u'┤'
                else:
                    c=u'╬'
                    l=u'╠'
                    r=u'╣'                        
                self.center = flextable.color(text=c,default=default)
                self.left   = flextable.color(text=l,default=default)
                self.right  = flextable.color(text=r,default=default)
        
        class char_bottom:
            def __init__(self,default=None,single=True):
                if single is True:
                    l=u'└'
                    c=u'┴'
                    r=u'┘'
                else:
                    l=u'╚'
                    c=u'╩'
                    r=u'╝'
                self.left   = flextable.color(text=l,default=default)
                self.center = flextable.color(text=c,default=default)
                self.right  = flextable.color(text=r,default=default)
        class char_top:
            def __init__(self,default=None,single=True):
                if single is True:
                    l=u'┌'
                    c=u'┐'
                    r=u'┬'
                else:
                    l=u'╔'
                    c=u'╗'
                    r=u'╦'
                self.left   = flextable.color(text=l,default=default)
                self.right  = flextable.color(text=c,default=default)
                self.center = flextable.color(text=r,default=default)
        class char_header:
            def __init__(self,default=None,single=True):
                if single is True:
                    l=u'┤'
                    r=u'├'
                    c=u' '
                else:
                    l=u'╡'
                    r=u'╞'
                    c=u' '            
                self.left   = flextable.color(text=l,default=default,foreground='White')
                self.right  = flextable.color(text=r,default=default,foreground='White')
                self.center = flextable.color(text=c,default=default,foreground='green')
        class char_mid_header:
            def __init__(self,default=None,single=True):
                if single is True:
                    l=u'-'
                    r=u'-'
                    c=u' '
                else:
                    l=u'-'
                    r=u'-'
                    c=u' '
                self.left   = flextable.color(text=l,default=default,foreground='White')
                self.right  = flextable.color(text=r,default=default,foreground='White')
                self.center = flextable.color(text=c,default=default,foreground='green')
        class char_footer:
            def __init__(self,default=None,single=True):
                if single is True:
                    l=u'['
                    r=u']'
                    c=u' '
                else:
                    l=u'['
                    r=u']'
                    c=u' '
                self.left   = flextable.color(text=l,default=default,foreground='White') #╡
                self.right  = flextable.color(text=r,default=default,foreground='White') #╞
                self.center = flextable.color(text=c,default=default,foreground='green')

        def __init__(self,default=None,style='single'):
            if style=='single':
                single=True
            else:
                single=False
            self.walls      =self.char_walls(default=default,single=single)
            self.center     =self.char_center(default=default,single=single)
            self.bottom     =self.char_bottom(default=default,single=single)
            self.top        =self.char_top(default=default,single=single)
            self.header     =self.char_header(default=default,single=single)
            self.mid_header =self.char_mid_header(default=default,single=single)
            self.footer     =self.char_footer(default=default,single=single)




    data_type=enum(COMMENT=1,ERROR=2,DATA=3,WHITESPACE=4)
    
    def __init__(self,      data,
                            display_style='single',
                            column_count=0,
                            hide_comments=False,
                            hide_errors=False,
                            hide_whitespace=False,
                            columns=None,
                            length=None,
                            line=0,
                            page=0,
                            header=True,
                            footer=True,
                            header_every=-1,
                            tab_width=4,
                            tab_stop=8,
                            row_height=-1,
                            column_width=-1,
                            render_color=True
                        ):
        self.column_count=column_count
        self.hide_comments=hide_comments
        self.hide_errors=hide_errors
        self.hide_whitespace=hide_whitespace
        self.columns=columns
        self.length=length
        self.line=line
        self.page=page
        self.header=header
        self.footer=footer
        self.header_every=header_every
        self.tab_width=tab_width
        self.tab_stop=tab_stop
        self.row_height=row_height
        self.column_width=column_width
        self.render_color=render_color
        self.is_temp_file=False


        if self.column_width==-1:
            self.row_height,self.column_width = os.popen('stty -F /dev/tty size', 'r').read().split()
        if column_count>-1 and columns == None:
            self.columns=[]
            for n in range(0,self.column_count):
                self.columns.append("column{0}".format(n+1))

        else:
            self.column_count=len(columns)
        
        
        if page>-1 and length>1:
            self.starts_on=page*length+1
        if self.line>-1:
            self.starts_on=line

        self.style=self.flextable_style(style=display_style)
        self.results=[]
        self.data=data
        self.format()



    def calculate_limits(self):
        tty_min_column_width=1
        
        
        
        data_column_count=len(self.columns)

        pad=data_column_count+1
        if data_column_count==0:
            self.column_character_width=-1
        else:
            if self.column_width!=-1:
                self.column_character_width=int((int(self.column_width)-1-pad)/data_column_count)
                if self.column_character_width<tty_min_column_width:
                    self.column_character_width=tty_min_column_width


        self.total_width=self.column_character_width*data_column_count+data_column_count-1


    def build_header(self,footer=False,mid=False):

        if False==footer:
            base=self.style.characters.top
            column=self.style.characters.header
        else:
                base=self.style.characters.bottom
                column=self.style.characters.footer
        if mid==True:
                base=self.style.characters.center
                column=self.style.characters.mid_header
        header=base.left.render(use_color=self.render_color)

        column_pad=0
        if None!=column.left.text:
            column_pad+=1
        if None!=column.right.text:
            column_pad+=1

        if None != self.columns:
            index=0
            for c in self.columns:
                column_display=u''
                if None!=column.left.text:
                    column_display=column.left.render(use_color=self.render_color)

                column_display+=column.center.render(use_color=self.render_color,text=c,length=self.column_character_width-column_pad)

                if None!=column.right.text:
                    column_display+=column.right.render(use_color=self.render_color)
                

                header+=column_display

                if index<len(self.columns)-1:
                    if len('{0}'.format(c))>self.column_character_width-2:
                        header+=base.center.render(use_color=self.render_color,override=self.style.color.overflow)
                    else:
                        header+=base.center.render(use_color=self.render_color)
                index+=1
        header+=base.right.render(use_color=self.render_color)
        header+=u'{0}'.format(flextable.reset.ALL)


        return header
            
    def build_rows(self,buffer):
        rows=[]
        index=0
        if True == isinstance(buffer,list):
            for line in buffer:
                columns=self.style.characters.walls.left.render(use_color=self.render_color)
                
                if self.data_type.DATA == line['type']:
                    for c in line['data']:
                        columns+=self.style.color.data.render(c,use_color=self.render_color,length=self.column_character_width)
                        if len('{}'.format(c))>self.column_character_width:
                            columns+=self.style.characters.walls.right.render(use_color=self.render_color,override=self.style.color.overflow)
                        else:
                            columns+=self.style.characters.walls.right.render(use_color=self.render_color)
                        
                    if len(line['data']) < self.column_count:
                        wall_color=flextable.bg.LIGHT_BLUE
                        for c in range(len(line['data']),self.column_count):
                            columns+=self.style.color.comment.render('',use_color=self.render_color,length=self.column_character_width)
                            columns+=self.style.characters.walls.right.render(use_color=self.render_color,override=self.style.color.error)
                            
                
                
                if self.data_type.COMMENT ==  line['type'] or self.data_type.WHITESPACE==line['type']:
                    left  =self.style.characters.walls.left.render(use_color=self.render_color)
                    center=self.style.color.comment.render(line['raw'],use_color=self.render_color,length=self.total_width)
                    right =self.style.characters.walls.right.render(use_color=self.render_color)
                    columns=u"{0}{1}{2}".format( left,
                                                center,
                                                right)
                
                if self.data_type.ERROR ==  line['type']:
                    left  =self.style.characters.walls.left.render(use_color=self.render_color)
                    center=self.style.color.error.render(line['raw'],use_color=self.render_color,length=self.total_width)
                    right =self.style.characters.walls.right.render(use_color=self.render_color)
                    columns=u"{0}{1}{2}".format( left,
                                                center,
                                                right)
                columns+=u'{}'.format(flextable.reset.ALL)

                rows.append(columns)
                index+=1
        else:
            raise Exception ("data is invalid: ->".format(buffer))

        return rows

     
    def output(self,text,encode):
        if encode:
            print(text.encode('utf-8'))
        else:
            print (text)

    def print_errors(table):
        for e in table.errors:
            print(e.encode('utf-8'))
                        
    def format(self):
        self.calculate_limits()
        header=self.build_header()
        mid_header=self.build_header(mid=True)
        footer=self.build_header(footer=True)
        rows=self.build_rows(self.data)
        
        index=1

        if sys.version_info.major>2:
            encode=False
        else:
            encode=True


        if self.header==True:
            self.output(header,encode)

        for row in rows:
            self.output(row,encode)
            
            if self.header_every>0:                
                if index%self.header_every==0 and len(buffer)-index>self.header_every :
                    self.output(mid_header,encode)
            index+=1
        if self.footer==True:
            self.output(footer,encode)

        
        
# ############################################################################
# Module : factory_yaml
# File   : ./source/ddb/output/factory_yaml.py
# ############################################################################



def yamlf_load(data=None,file=None):
    factory=factory_yaml()
    return factory.load(data=data,in_file=file)

def yamlf_dump(data=None,file=None):
    factory=factory_yaml()
    return factory.dump(data=data,out_file=file)

class factory_yaml:
    debug=True
    def __init__(self,debug=None):
        self.debug=debug
    
    def info(self,msg,data):
        if self.debug:
            print("{0} : {1}".format(msg,data))



    def walk_path(self,path,root):
        obj=root

        if path and len(path)>0:
            for trail in path:
                if hasattr(obj, '__dict__'):
                    obj=getattr(obj,trail)
                else:
                    obj=obj[trail]

        return obj
        
    def get_parent_obj(self,path,root): 
        if len(path)<2:
            return None
        sub_path=path[0:-1]
        fragment=self.walk_path(sub_path,root)

        if isinstance(fragment,list):
            if len(sub_path)<1:
                return None
            sub_path=sub_path[0:-1]
            fragment=self.walk_path(sub_path,root)


        key=""#sub_path[-1]
        if isinstance(fragment,list):
            self.info("Yaml-Get Parent Object","In List")
            return {'key':key,'type':'list','obj':fragment,'depth':len(sub_path)}
        elif isinstance(fragment,dict):
            self.info("Yaml-Get Parent Object","In Dict")
            return {'key':key,'type':'dict','obj':fragment,'depth':len(sub_path)}
        elif hasattr(fragment, '__dict__'):
            self.info("Yaml-Get Parent Object","In Class")
            return {'key':key,'type':'dict','obj':fragment,'depth':len(sub_path)}
            
        return None        
                    
    def get_next_obj_path(self,path,root):
        self.info("Yaml","Walking")
        fragment=self.walk_path(path,root)
        self.info("Path", ".".join([ str(arr) for arr in path]))
        if isinstance(fragment,list):
            for i,value in enumerate(fragment):
                self.info("Yaml","List:{0}".format(i))
                path.append(i)
                return {'key':i,'type':'list','obj':value,'depth':len(path)}

        elif isinstance(fragment,dict):
            for i in fragment:
                self.info("Yaml","Dict:{0}".format(i))
                path.append(i)
                return {'key':i,'type':'dict','obj':fragment[i],'depth':len(path)}

        elif hasattr(fragment, '__dict__'):
            self.info("Yaml","In Class")
            
            for key in fragment.__dict__.keys():
                self.info("Yaml","Class:{0}".format(key))
                value=getattr(fragment,key)

                path.append(key)
                return {'key':key,'type':'class','obj': value,'depth':len(path)}
        
        self.info("Yaml","Cant go deeper")
        while len(path)>0:
            self.info("Yaml","loop - looking {0}".format(len(path)))
        
            last_path=path.pop()
            
            if len(path)==0:
                temp_obj=root
            else:
                temp_obj=self.walk_path(path,root)
            
            grab_next=None
            if isinstance(temp_obj,list):
                self.info("Yaml","Next - In List")
                for i,value in enumerate(temp_obj):
                    if grab_next:
                        path.append(i)
                        return {'key':i,'type':'list','obj':value,'depth':len(path)}

                    if i==last_path:
                        grab_next=True


            elif isinstance(temp_obj,dict):
                self.info("Yaml","Next - In Dict")
                for i in temp_obj:
                    value=temp_obj[i]
                    if grab_next:
                        path.append(i)
                        return {'key':i,'type':'dict','obj':value,'depth':len(path)}

                    if i==last_path:
                        grab_next=True


            elif hasattr(temp_obj, '__dict__'):
                self.info("Yaml","Next - In Class")
                
                for key in temp_obj.__dict__.keys():
                    self.info("Yaml","Attr:{0}".format(key))
                    value=getattr(temp_obj,key)

                    if grab_next:
                        path.append(key)
                        return {'key':key,'type':'class','obj':value,'depth':len(path)}

                    if key==last_path:
                        grab_next=True
            self.info("Yaml","Didnt find it")
        return None

    def padding(self,indent,indent_spacing,array_depth=0):
        padding=""
        indent=indent-1
        if indent_spacing<=0:
            indent_spacing=1
        column_indent=(indent-array_depth)
        if column_indent<0:
            column_indent=0
        pad_len=column_indent*indent_spacing+array_depth*2
        for i in range(0,pad_len):
            padding+=" "
        return padding

    def render(self,data_obj,indent=0):
        obj=data_obj
        root=data_obj
        path=[]
        line=""
        lines=[]
        last_fragment=None
        arr_depth=0
        newline=False
        fragment=True
        while fragment!=None:
            self.info("Yaml-Render","Start Loop")

            fragment=self.get_next_obj_path(path,root)
            parent_fragment=self.get_parent_obj(path,root)

            if None ==fragment:
                self.info("Yaml-Render","NONE skipping")
                continue

            if  fragment['type']!='list':
                arr_depth=0
            if parent_fragment:
                if  parent_fragment['type']!='list':
                    arr_depth=0
                if  parent_fragment['type']=='list' and fragment['type']=='list' and last_fragment['depth']<fragment['depth']:
                    arr_depth+=1
                if  parent_fragment['type']=='list' and fragment['type']=='list' and last_fragment['depth']>fragment['depth']:
                    arr_depth-=1

            obj=fragment['obj']
            if fragment['type']=='class':
                self.info("Yaml-Render",'Its a class')
                if newline==0:
                    if len(line)>0:
                       lines.append(line)
                    line=self.padding(len(path),indent,arr_depth)
                else:
                    newline=0
                line+="{0}: ".format(fragment['key'])#+""+str(arr_depth)+'-'+str(len(path))+"-"+str(indent)

            if fragment['type']=='dict':
                if newline==0:
                    if len(line)>0:
                       lines.append(line)
                    line=self.padding(len(path),indent,arr_depth)
                else:
                    newline=0
                if not fragment['key']:
                    line+="{0}: -{1}".format(fragment['key'],'{'+'}')#+""+str(arr_depth)+'-'+str(len(path))+"-"+str(indent)
                else:
                    line+="{0}: ".format(fragment['key'])#+""+str(arr_depth)+'-'+str(len(path))+"-"+str(indent)
                
            if fragment['type']=='list':
                if parent_fragment and fragment:
                    if parent_fragment['type']!='list' and  fragment['key']==0:
                        if len(line)>0:
                            lines.append(line)
                        line=self.padding(len(path)-1,indent,arr_depth)#+"("+str(arr_depth)+'-'+str(len(path))+"-"+str(indent)+")"

                    elif  fragment['key']!=0:
                        if len(line)>0:
                            lines.append(line)
                        line=self.padding(len(path)-1,indent,arr_depth)#+"("+str(arr_depth)+'-'+str(len(path))+"-"+str(indent)+")"

                line+="- "
                newline=1
            if isinstance(obj,list) and len(obj)==0:
               line+="[]"
            if isinstance(obj,dict) and not obj:
               line+="{}"
            if not isinstance(obj,list) and not  isinstance(obj,dict) and not hasattr(obj,'__dict__'):
                if obj==None:
                    line+="null"
                elif isinstance(obj,int):
                    line+="{0}".format(obj)
                elif obj==True:
                    line+="true"
                elif obj==False:
                    line+="false"
                elif isinstance(obj,str):
                    obj=obj.replace("'","''")
                    obj=obj.replace("\"","\\\"")
                    
                    line+="'{0}'".format(obj)
                else:
                    line+="{0}".format(obj)

                if len(line)>0:
                    lines.append(line)
                line=""
                newline=0
            last_fragment=fragment
        if line: 
            lines.append(line)
        document='\n'.join(lines)
        return document



 
    def get_indent(self,line):
        index_of=line.find('- ')

        cleaned_line=line
        index=len(line)-len(cleaned_line.lstrip())
        if index_of!=-1:
            index+=1
        
        return index

    def is_start(self,line):
        if line=='---':
            return True
        return None

    def is_end(self,line):
        if line=='...':
            return True
        return None

    def is_array(self,line_cleaned):
        """determine if a string begins with an array identifyer '- '"""
        if None==line_cleaned:
            return False
        if len(line_cleaned)>1:
            if line_cleaned[0]=='-' and line_cleaned[1]==' ':
                return True
        return False
        
    def strip_array(self,line):
        """Strip array elements from string '- '"""
        index_of=line.find('- ')
        if index_of!=-1:
            str1=list(line)
            str1[index_of]=' '
            line="".join(str1)
        return line

    def is_comment(self,line):
        cleaned=line.lstrip()
        if len(cleaned)>0:
            if cleaned[0]=='#':
                return True
        return False

    def get_tuple(self,line):
        if self.is_comment(line):
            return None
        """Get key value pair from string with a colon delimiter"""
        index=line.find(':')
        if index==-1:
            return None
        
        key=self.return_data(line[0:index])
        data_index=index+1
        if data_index<len(line):
            data=line[data_index:].strip()
        else:
            data=None
        return {'key':key,'data':data}

    def return_data(self,data):
        
        data=data.strip()
        if len(data)>2:
            quoted=None
            if data[0]=="'" and data[-1]=="'":
                quoted=True
            if data[0]=='"' and data[-1]=='"':
                quoted=True
            if quoted:
                return data[1:-1]
        try:
            return int(data)
        except ValueError:
            pass
        try:
            return float(data)
        except ValueError:
            pass
        if data=="true" or data== 'yes' or data== 'Yes':
            return True
        if data=="false" or data== 'no' or data== 'No':
            return False
        if data=="null":
            return None
        if data=="[]":
            return []
        if data=="{}":
            return {}
        return data
        
    def dump(self,data=None,out_file=None):
        if isinstance(data,str):
            raise Exception ("yaml dump requires an object, not a string")
        yaml_data=self.render(data)

        if out_file:
            with open(out_file, 'w') as yaml_file:
                yaml_file.write(yaml_data)
        else:
            return yaml_data


    def load(self,data=None,in_file=None):
        if in_file:
            with open(in_file) as content:
                data=content.read()

        lines=data.splitlines()
        root={}
        last_indent=None
        obj=root
        hash_map=[{'indent':0,'obj':obj}]
        obj_parent=root
        obj_parent_key=None
        obj_hash=[]
        for line in lines:
            if self.is_start(line):
                continue
            if self.is_end(line):
                break
            indent=self.get_indent(line)

            line_cleaned=line
            is_array=self.is_array(line_cleaned.strip())
        
            
            if  is_array:
                self.info("Encode","Create Array Index")
                line_cleaned=self.strip_array(line_cleaned)
                line=line_cleaned
                arr_index=0
                while is_array:
                    make_new_array=True
                    if None==obj:
                        self.info("Encode-Array","made a new object at start (root index) @ {0}".format(len(hash_map)))
                        obj_parent[obj_parent_key]=[]
                        obj=obj_parent[obj_parent_key]
                        obj_hash['obj']=obj
                        obj_hash['indent']=indent
                        make_new_array=None
                        
                    elif arr_index==0:
                        for index in range(len(hash_map)-1,-1,-1):
                            if hash_map[index]['indent']==indent and isinstance(hash_map[index]['obj'],list):
                                obj=hash_map[index]['obj']
                                make_new_array=None
                                self.info("Encode-Array","Found  object")
                        
                                break
                    if make_new_array:
                        if isinstance(obj,list):
                            self.info("Encode","Made a new object")
                        
                            new_list=[]
                            obj.append(new_list)
                            obj=new_list
                            hash_map.append({'indent':indent,'obj':obj})
                        else:
                            obj=[]
                    line_cleaned=line
                    indent=self.get_indent(line)
                    is_array=self.is_array(line_cleaned.strip())
                    if is_array:
                        line_cleaned=self.strip_array(line_cleaned)
                        line=line_cleaned
                    arr_index+=1
                indent=self.get_indent(line)
            else:
                if last_indent and  last_indent>indent:
                    found=None
                    for index in range(len(hash_map)-1,-1,-1):
                        if hash_map[index]['indent']<=indent:
                            obj=hash_map[index]['obj']
                            self.info("Encode","Found it: {0}".format(index))
                            found=True
                            break
                    if None==found:
                        self.info("Encode","Didn't Find it")
                
                    
                            
            line_tuple=self.get_tuple(line_cleaned)
            if line_tuple:
                self.info("Encode","In Tuple :{0}".format(line_tuple['key']))
                if None == obj:
                    self.info("Encode","OBJ needs ")
                    obj_parent[obj_parent_key]={}
                    obj=obj_parent[obj_parent_key]
                    obj_hash['obj']=obj
                    obj_hash['indent']=indent

                if isinstance(obj,list):
                    new_obj={}
                    obj.append(new_obj)
                    obj_parent=obj
                    obj_parent_key=len(obj)-1
                    obj=new_obj
                    obj_hash={'indent':indent,'obj':obj}
                    hash_map.append(obj_hash)

                if line_tuple['data']:
                    value=self.return_data(line_tuple['data'])
                    obj[line_tuple['key']]=value
                else:
                    if  not isinstance(obj,list):
                        self.info("Encode","no tuble value")
                        obj[line_tuple['key']]=None
                        obj_parent=obj
                        obj_parent_key=line_tuple['key']
                        obj=obj[line_tuple['key']]
                        obj_hash={'indent':indent,'obj':obj}
                        hash_map.append(obj_hash)
            else:
                if self.is_comment(line):
                    continue

                if isinstance(obj,list):
                    value=self.return_data(line_cleaned)
                    obj.append(value)
            last_indent=indent
        return root














        
        
# ############################################################################
# Module : factory_xml
# File   : ./source/ddb/output/factory_xml.py
# ############################################################################



class factory_xml:

    def dumps(self,data):
        output_string=self.render(data)
        return output_string

    def render(self,obj,root='root',depth=0):
        """xml like output for python objects, very loose"""
        template="""<{0}>{1}</{0}>"""
        fragment=""
        if None==obj:
            return fragment

        if isinstance(obj,str):
            fragment+=template.format(root,obj)

        elif isinstance(obj,int):
            fragment+=template.format(root,obj)

        elif isinstance(obj,float):
            fragment+=template.format(root,obj)
        
        elif isinstance(obj,bool):
            fragment+=template.format(root,obj)
        elif  isinstance(obj,list):
            for item in obj:
                fragment+=self.render(item,root=root,depth=depth+1)
        elif isinstance(obj,object):
            for item in obj:
                fragment+=self.render(obj[item],root=item,depth=depth+1)
        else:
            fragment+=template.format("UNK",obj)

        if depth==0:
            fragment=template.format("root",fragment)
        return fragment

        
        
# ############################################################################
# Module : factory_json
# File   : ./source/ddb/output/factory_json.py
# ############################################################################



class factory_json:
    def dumps(self,data):
        output_string=self.render(data)
        return output_string

    def render(self,obj,depth=0):
        """json like output for python objects, very loose"""
        unk_template='"???{0}???"'
        str_template='"{0}"'
        int_template="{0}"
        float_template="{0}"
        bool_template="{0}"
        array_template='['+'{0}'+']'
        tuple_template='"{0}":{1}'
        object_template='{{'+'{0}'+'}}'
        fragment=""
        if None == obj:
            return fragment

        if isinstance(obj,str):
            fragment+=str_template.format(obj)

        elif isinstance(obj,int):
            fragment+=int_template.format(obj)

        elif isinstance(obj,float):
            fragment+=float_template.format(obj)
        
        elif isinstance(obj,bool):
            fragment+=bool_template.format(obj)
        elif  isinstance(obj,list):
            partial=[]
            for item in obj:
                partial.append(self.render(item,depth=depth+1))
            if len(partial)>0:
                fragment+=array_template.format(",".join(map(str, partial)))
        elif isinstance(obj,object):
            partial=[]
            for item in obj:
                partial.append(tuple_template.format(item,self.render(obj[item],depth=depth+1)))
            if len(partial)>0:
                fragment+=object_template.format(",".join(map(str, partial))) 
        else:
            fragment+=unk_template.format("UNK",obj)
        return fragment

