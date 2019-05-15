#!/usr/bin/python
# -*- coding: utf-8 -*-

# # ############################################################################
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
import shutil
import time
import pprint
import uuid
import logging



from slackclient import SlackClient

import logging
logging.basicConfig()


        
# ############################################################################
# Module : version
# File   : ./source/ddb/version.py
# ############################################################################

__version__='1.2.49'

        
# ############################################################################
# Module : lexer-language
# File   : ./source/ddb/lexer/language.py
# ############################################################################

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
                            {'data': [{'sig': ['on',
                                               '{e1}',
                                               '<',
                                               '{e2}'],
                                       'vars': {'c': '<'}},
                                      {'sig': ['on',
                                               '{e1}',
                                               '>',
                                               '{e2}'],
                                       'vars': {'c': '>'}},
                                      {'sig': ['on',
                                               '{e1}',
                                               '>=',
                                               '{e2}'],
                                       'vars': {'c': '>='}},
                                      {'sig': ['on',
                                               '{e1}',
                                               '<=',
                                               '{e2}'],
                                       'vars': {'c': '<='}},
                                      {'sig': ['on',
                                               '{e1}',
                                               '!=',
                                               '{e2}'],
                                       'vars': {'c': '!='}},
                                      {'sig': ['on',
                                               '{e1}',
                                               '<>',
                                               '{e2}'],
                                       'vars': {'c': '<>'}},
                                      {'sig': ['on',
                                               '{e1}',
                                               'not',
                                               '{e2}'],
                                       'vars': {'c': 'not'}},
                                      {'sig': ['on',
                                               '{e1}',
                                               'is',
                                               '{e2}'],
                                       'vars': {'c': 'is'}},
                                      {'sig': ['on',
                                               '{e1}',
                                               'like',
                                               '{e2}'],
                                       'vars': {'c': 'like'}},
                                      {'sig': ['on',
                                               '{e1}',
                                               '=',
                                               '{e2}'],
                                       'vars': {'c': '='}},
                                      {'sig': ['on',
                                               '{e1}',
                                               'in',
                                               '(',
                                               '[e2]',
                                               ')'],
                                       'vars': {'c': 'in'}}],
                             'depends_on': 'join',
                             'name': 'on',
                             'optional': True,
                             'store_array': True},
                            {'data': [{'sig': ['and',
                                               '{e1}',
                                               '<',
                                               '{e2}'],
                                       'vars': {'c': '<'}},
                                      {'sig': ['and',
                                               '{e1}',
                                               '>',
                                               '{e2}'],
                                       'vars': {'c': '>'}},
                                      {'sig': ['and',
                                               '{e1}',
                                               '>=',
                                               '{e2}'],
                                       'vars': {'c': '>='}},
                                      {'sig': ['and',
                                               '{e1}',
                                               '<=',
                                               '{e2}'],
                                       'vars': {'c': '<='}},
                                      {'sig': ['and',
                                               '{e1}',
                                               '!=',
                                               '{e2}'],
                                       'vars': {'c': '!='}},
                                      {'sig': ['and',
                                               '{e1}',
                                               '<>',
                                               '{e2}'],
                                       'vars': {'c': '<>'}},
                                      {'sig': ['and',
                                               '{e1}',
                                               'not',
                                               '{e2}'],
                                       'vars': {'c': 'not'}},
                                      {'sig': ['and',
                                               '{e1}',
                                               'is',
                                               '{e2}'],
                                       'vars': {'c': 'is'}},
                                      {'sig': ['and',
                                               '{e1}',
                                               'like',
                                               '{e2}'],
                                       'vars': {'c': 'like'}},
                                      {'sig': ['and',
                                               '{e1}',
                                               '=',
                                               '{e2}'],
                                       'vars': {'c': '='}},
                                      {'sig': ['and',
                                               '{e1}',
                                               'in',
                                               '(',
                                               '[e2]',
                                               ')'],
                                       'vars': {'c': 'in'}}],
                             'depends_on': 'on',
                             'jump': 'on',
                             'name': 'and',
                             'optional': True,
                             'parent': 'on'},
                            {'data': [{'sig': ['or',
                                               '{e1}',
                                               '<',
                                               '{e2}'],
                                       'vars': {'c': '<'}},
                                      {'sig': ['or',
                                               '{e1}',
                                               '>',
                                               '{e2}'],
                                       'vars': {'c': '>'}},
                                      {'sig': ['or',
                                               '{e1}',
                                               '>=',
                                               '{e2}'],
                                       'vars': {'c': '>='}},
                                      {'sig': ['or',
                                               '{e1}',
                                               '<=',
                                               '{e2}'],
                                       'vars': {'c': '<='}},
                                      {'sig': ['or',
                                               '{e1}',
                                               '!=',
                                               '{e2}'],
                                       'vars': {'c': '!='}},
                                      {'sig': ['or',
                                               '{e1}',
                                               '<>',
                                               '{e2}'],
                                       'vars': {'c': '<>'}},
                                      {'sig': ['or',
                                               '{e1}',
                                               'not',
                                               '{e2}'],
                                       'vars': {'c': 'not'}},
                                      {'sig': ['or',
                                               '{e1}',
                                               'is',
                                               '{e2}'],
                                       'vars': {'c': 'is'}},
                                      {'sig': ['or',
                                               '{e1}',
                                               'like',
                                               '{e2}'],
                                       'vars': {'c': 'like'}},
                                      {'sig': ['or',
                                               '{e1}',
                                               '=',
                                               '{e2}'],
                                       'vars': {'c': '='}},
                                      {'sig': ['or',
                                               '{e1}',
                                               'in',
                                               '(',
                                               '[e2]',
                                               ')'],
                                       'vars': {'c': 'in'}}],
                             'depends_on': 'on',
                             'jump': 'on',
                             'name': 'or',
                             'optional': True,
                             'parent': 'on'},
                            {'data': [{'sig': ['where',
                                               '{e1}',
                                               '<',
                                               '{e2}'],
                                       'vars': {'c': '<'}},
                                      {'sig': ['where',
                                               '{e1}',
                                               '>',
                                               '{e2}'],
                                       'vars': {'c': '>'}},
                                      {'sig': ['where',
                                               '{e1}',
                                               '>=',
                                               '{e2}'],
                                       'vars': {'c': '>='}},
                                      {'sig': ['where',
                                               '{e1}',
                                               '<=',
                                               '{e2}'],
                                       'vars': {'c': '<='}},
                                      {'sig': ['where',
                                               '{e1}',
                                               '!=',
                                               '{e2}'],
                                       'vars': {'c': '!='}},
                                      {'sig': ['where',
                                               '{e1}',
                                               '<>',
                                               '{e2}'],
                                       'vars': {'c': '<>'}},
                                      {'sig': ['where',
                                               '{e1}',
                                               'not',
                                               '{e2}'],
                                       'vars': {'c': 'not'}},
                                      {'sig': ['where',
                                               '{e1}',
                                               'is',
                                               '{e2}'],
                                       'vars': {'c': 'is'}},
                                      {'sig': ['where',
                                               '{e1}',
                                               'like',
                                               '{e2}'],
                                       'vars': {'c': 'like'}},
                                      {'sig': ['where',
                                               '{e1}',
                                               '=',
                                               '{e2}'],
                                       'vars': {'c': '='}},
                                      {'sig': ['where',
                                               '{e1}',
                                               'in',
                                               '(',
                                               '[e2]',
                                               ')'],
                                       'vars': {'c': 'in'}}],
                             'depends_on': 'from',
                             'name': 'where',
                             'optional': True,
                             'store_array': True},
                            {'data': [{'sig': ['and',
                                               '{e1}',
                                               '<',
                                               '{e2}'],
                                       'vars': {'c': '<'}},
                                      {'sig': ['and',
                                               '{e1}',
                                               '>',
                                               '{e2}'],
                                       'vars': {'c': '>'}},
                                      {'sig': ['and',
                                               '{e1}',
                                               '>=',
                                               '{e2}'],
                                       'vars': {'c': '>='}},
                                      {'sig': ['and',
                                               '{e1}',
                                               '<=',
                                               '{e2}'],
                                       'vars': {'c': '<='}},
                                      {'sig': ['and',
                                               '{e1}',
                                               '!=',
                                               '{e2}'],
                                       'vars': {'c': '!='}},
                                      {'sig': ['and',
                                               '{e1}',
                                               '<>',
                                               '{e2}'],
                                       'vars': {'c': '<>'}},
                                      {'sig': ['and',
                                               '{e1}',
                                               'not',
                                               '{e2}'],
                                       'vars': {'c': 'not'}},
                                      {'sig': ['and',
                                               '{e1}',
                                               'is',
                                               '{e2}'],
                                       'vars': {'c': 'is'}},
                                      {'sig': ['and',
                                               '{e1}',
                                               'like',
                                               '{e2}'],
                                       'vars': {'c': 'like'}},
                                      {'sig': ['and',
                                               '{e1}',
                                               '=',
                                               '{e2}'],
                                       'vars': {'c': '='}},
                                      {'sig': ['and',
                                               '{e1}',
                                               'in',
                                               '(',
                                               '[e2]',
                                               ')'],
                                       'vars': {'c': 'in'}}],
                             'depends_on': 'where',
                             'jump': 'where',
                             'name': 'and',
                             'optional': True,
                             'parent': 'where'},
                            {'data': [{'sig': ['or',
                                               '{e1}',
                                               '<',
                                               '{e2}'],
                                       'vars': {'c': '<'}},
                                      {'sig': ['or',
                                               '{e1}',
                                               '>',
                                               '{e2}'],
                                       'vars': {'c': '>'}},
                                      {'sig': ['or',
                                               '{e1}',
                                               '>=',
                                               '{e2}'],
                                       'vars': {'c': '>='}},
                                      {'sig': ['or',
                                               '{e1}',
                                               '<=',
                                               '{e2}'],
                                       'vars': {'c': '<='}},
                                      {'sig': ['or',
                                               '{e1}',
                                               '!=',
                                               '{e2}'],
                                       'vars': {'c': '!='}},
                                      {'sig': ['or',
                                               '{e1}',
                                               '<>',
                                               '{e2}'],
                                       'vars': {'c': '<>'}},
                                      {'sig': ['or',
                                               '{e1}',
                                               'not',
                                               '{e2}'],
                                       'vars': {'c': 'not'}},
                                      {'sig': ['or',
                                               '{e1}',
                                               'is',
                                               '{e2}'],
                                       'vars': {'c': 'is'}},
                                      {'sig': ['or',
                                               '{e1}',
                                               'like',
                                               '{e2}'],
                                       'vars': {'c': 'like'}},
                                      {'sig': ['or',
                                               '{e1}',
                                               '=',
                                               '{e2}'],
                                       'vars': {'c': '='}},
                                      {'sig': ['or',
                                               '{e1}',
                                               'in',
                                               '(',
                                               '[e2]',
                                               ')'],
                                       'vars': {'c': 'in'}}],
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
               'segments': [{'data': [{'sig': ['begin']}], 'name': 'begin'}]},
              {'name': 'commit',
               'segments': [{'data': [{'sig': ['commit']}],
                             'depends_on': 'begin',
                             'name': 'commit'}]},
              {'name': 'rollback',
               'segments': [{'data': [{'sig': ['rollback']}],
                             'depends_on': 'begin',
                             'name': 'rollback'}]},
              {'name': 'show output modules',
               'segments': [{'data': [{'sig': ['show',
                                               'output',
                                               'modules']}],
                             'name': ['show', 'output', 'modules']}]},
              {'name': 'delete',
               'segments': [{'data': [{'sig': ['delete']}],
                             'name': 'delete'},
                            {'data': [{'sig': ['from', '{table}']}],
                             'name': 'from'},
                            {'data': [{'sig': ['where',
                                               '{e1}',
                                               '{c}',
                                               '{e2}']}],
                             'name': 'where',
                             'optional': True,
                             'store_array': True},
                            {'arguments': 0,
                             'data': [{'sig': ['where','{e1}', '{c}', '{e2}']}],
                             'depends_on': 'where',
                             'jump': 'where',
                             'name': 'and',
                             'optional': True,
                             'parent': 'where'},
                            {'data': [{'sig': ['or',
                                               '{e1}',
                                               '{c}',
                                               '{e2}']}],
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
                            {'data': [{'sig': ['where',
                                               '{e1}',
                                               '{c}',
                                               '{e2}']}],
                             'name': 'where',
                             'optional': True,
                             'store_array': True},
                            {
                             'data': [{'sig': ['and','{e1}', '{c}', '{e2}']}],
                             'depends_on': 'where',
                             'jump': 'where',
                             'name': 'and',
                             'optional': True,
                             'parent': 'where'},
                            {'data': [{'sig': ['or',
                                               '{e1}',
                                               '{c}',
                                               '{e2}']}],
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
                                               '{type}',
                                               'url',
                                               '=',
                                               '{url}',
                                               'user',
                                               '=',
                                               '{user}',
                                               'password',
                                               '=',
                                               '{password}',
                                               'dir',
                                               '=',
                                               '{dir}',
                                               'file',
                                               '{file}']}],
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
                             'specs': {'comments': {'type': 'bool'}},
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

        
# ############################################################################
# Module : lexer-parse
# File   : ./source/ddb/lexer/lexer.py
# ############################################################################

class lexer:
    def __init__(self, query, debug=False):
        self.keep_non_keywords=True
        self.debug = True
        self.query_objects = []
        if  query==None:
            raise Exception("Invalid Syntax")
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
            if None == parsed['success']:
                raise Exception(parsed['msg'])
            else:
                self.query_objects.append(parsed['results'])
        if None == self.query_objects:
            raise Exception("Invalid Syntax")
    def parse(self, tokens):
        highest_match=-1
        recent_match=None
        for command in language['commands']:
            res=self.test_syntax(command,tokens)
            if res['success']:
                return res
            else:
                if res['match']>highest_match:
                    highest_match=res['match']
                    recent_match=res
        return recent_match
    class flags:
        def __init__(self,command_fragment):
            if 'dispose' in command_fragment:
                self.dispose = command_fragment['dispose']
            else:
                self.dispose = False
            if 'no_keyword' in command_fragment:
                self.no_keyword = command_fragment['no_keyword']
            else:
                self.no_keyword = False
            if 'store_array' in command_fragment:
                self.store_array = command_fragment['store_array']
            else:
                self.store_array = False
            if 'key' in command_fragment:
                self.arg_key=command_fragment['key']
            else: 
                self.arg_key=None
            if 'parent' in command_fragment:
                self.parent = command_fragment['parent']
            else:
                self.parent = None
            if 'type' in command_fragment:
                self.meta_type = command_fragment['type']
            else:
                self.meta_type = None
            if 'optional' in command_fragment:
                self.optional = command_fragment['optional']
            else:
                self.optional = False
            if isinstance(command_fragment['name'], list):
                self.object_id = ' '.join([str(x) for x in command_fragment['name']])
                self.object_id = self.object_id.lower()
            else:
                self.object_id = command_fragment['name'].lower()
            if self.arg_key:
                self.object_id=self.arg_key
    def test_syntax(self,command,tokens):
        query_object = {}
        token_index = 0
        self.info("-----", command['name'])
        segment_index = 0
        query_mode = None
        curent_object = {}
        segment = {}
        while segment_index < len(command['segments']) and token_index < len(tokens):
            segment = command['segments'][segment_index]
            self.info("############# TESTING : {0}.{1}".format(command['name'],segment['name']))
            segment_index += 1
            curent_object = {}
            base_argument={}
            in_argument = True
            argument_index = 0
            flags=lexer.flags(segment)
            curent_object['mode'] = flags.object_id
            query_mode = command['name']
            self.info("Object Id:", flags.object_id, "Token Id:", token_index)
            while True == in_argument:
                if 'depends_on' in segment:
                    depends_on = segment['depends_on']
                    self.info("Depends on {0}".format(depends_on))
                else:
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
                if 'arguments' in segment:
                    arguments = segment['arguments']
                else:
                    arguments = 1
                if arguments == None:
                    arguments = 1
                self.info("Number of arguments", arguments)
                data = self.get_sub_array(segment, 'data')
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
                            if 'specs' in segment:
                                if variable in segment['specs']:
                                    if 'type' in segment['specs'][variable]:
                                        variable_type=segment['specs'][variable]['type']
                            if variable_type=='int':
                                try:
                                    argument[variable] = tokens[token_index + w_index]['data'] = int(variable_data)
                                except BaseException:
                                    pass
                                    break
                            elif variable_type=='bool':
                                if variable_data.lower()=='true':
                                    argument[variable] =True
                                elif variable_data.lower()=='false':
                                    argument[variable] =False
                                else:
                                    pass
                                    break
                            elif variable_type=='char':
                                if len(variable_data)!=1:
                                    pass
                                    break
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
                            if True == flags.store_array:
                                if curent_object['mode'] not in query_object:
                                    query_object[curent_object['mode']] = []
                                query_object[curent_object['mode']].append({curent_object['mode']: curent_object['arguments']})
                            else:
                                if None == flags.parent:
                                    if flags.meta_type=='single':
                                        for flags.arg_key in curent_object['arguments']:
                                            query_object[flags.arg_key] = curent_object['arguments'][flags.arg_key]
                                    else:    
                                        query_object[curent_object['mode']] = curent_object['arguments']
                                    self.info("NO APPEND")
                                else:
                                    self.info("APPEND")
                                    if flags.parent not in query_object:
                                        query_object[flags.parent]=[]
                                    query_object[flags.parent].append({curent_object['mode']: curent_object['arguments']})
                            jump = None
                            if 'jump' in segment:
                                self.info("JUMP")
                                jump = segment['jump']
                            if None != jump:
                                tsi = 0
                                for ts in command['segments']:
                                    if ts['name'] == jump:
                                        self.info("Jumping from ", segment_index, tsi + 1)
                                        segment_index = tsi + 1
                                        break
                                    tsi += 1
                            in_argument = False
                    else:
                        self.info("in list")
                        if len(tokens) <= token_index:
                            self.info("at the end")
                            if True == flags.store_array:
                                if curent_object['mode'] not in query_object:
                                    query_object[curent_object['mode']] = []
                                query_object[curent_object['mode']].append({curent_object['mode']: curent_object['arguments']})
                            else:
                                if None == flags.parent:
                                    query_object[curent_object['mode']] = curent_object['arguments']
                                    self.info("NO APPEND")
                                else:
                                    self.info("APPEND")
                                    if flags.parent not in query_object:
                                        query_object[flags.parent]=[]
                                    query_object[flags.parent].append({curent_object['mode']: curent_object['arguments']})
                        if len(tokens) > token_index:
                            self.info("--looking ahead")
                            self.info("----", tokens[token_index]['data'])
                            if tokens[token_index]['data'] != ',':
                                self.info("---not list")
                                self.info("----------Adding", curent_object['mode'])
                                if True == flags.store_array:
                                    if curent_object['mode'] not in query_object:
                                        query_object[curent_object['mode']] = []
                                    query_object[curent_object['mode']].append({curent_object['mode']: curent_object['arguments']})
                                else:
                                    if None == flags.parent:
                                        query_object[curent_object['mode']] = curent_object['arguments']
                                        self.info("NO APPEND")
                                    else:
                                        self.info("APPEND")
                                        if flags.parent not in query_object:
                                            query_object[flags.parent]=[]
                                        query_object[flags.parent].append({curent_object['mode']: curent_object['arguments']})
                                jump = None
                                if 'jump' in segment:
                                    jump = segment['jump']
                                if None != jump:
                                    tsi = 0
                                    for ts in command['segments']:
                                        if ts['name'] == jump:
                                            self.info("Jumping from ", segment_index, tsi + 1)
                                            segment_index = tsi + 1
                                            break
                                        tsi += 1
                                in_argument = False
                            else:
                                self.info("------more list")
                                token_index += 1
        self.info(segment_index, token_index, len(tokens))
        self.info(curent_object)
        if token_index == len(tokens):
            result=self.validate(curent_object,tokens,token_index,segment,command,segment_index,query_object,query_mode)
            if False == result:
                return {'success':False,'results':None,'match':token_index,'msg':"Validation failed"}
            else:
                return {'success':True,'results':result,'match':token_index,'msg':None}
        query_err=[]
        for index in range(0,len(tokens)):
            if index==token_index:
                query_err.append(" >>> ")    
                query_err.append(tokens[index]['data'])
                query_err.append(" <<< ")    
            else:
                query_err.append(tokens[index]['data'])
        query_err.append("\n Syntax error near word {0}".format(token_index))
        err_msg=" ".join(query_err)
        return {'success':None,'results':None,'match':token_index,'msg':err_msg}
    def validate(self,curent_object,tokens,token_index,segment,command,segment_index,query_object,query_mode):
        self.info(curent_object)
        self.info("############################think its a match")
        if 'arguments' not in curent_object and 'arguments' in segment:
            self.info("Missing argument in last element")
            bad = True
            return False
        if len(command['segments']) >= segment_index:
            self.info("still checking")
            bad = False
            for t in range(segment_index, len(command['segments'])):
                if 'optional' not in command['segments'][t]:
                    bad = True
                    return False
                else:
                    if not command['segments'][t]['optional']:
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
                        for f in language['functions']:
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
    def chomp(self,text, discard_delimiters=False, discard_whitespace=True, debug=None):
        self.debug_on = None
        tokens = []
        text = text.strip()
        whitespace = [' ', '\t', '\n', '\r' ]
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
                 data_on=None,
                 fifo=None,
                 repo_type=None,
                 repo_url=None,
                 repo_user=None,
                 repo_password=None,
                 repo_dir=None,
                 repo_file=None,
                 ):
        self.version = 1
        self.ownership = table_ownership()
        self.delimiters = table_delimiters()
        self.visible = table_visible_attributes()
        self.data = table_data(name=name, database=database)
        self.columns = []
        self.active = True
        self.ordinals = {}
        self.ordinal_lookup = {}
        self.errors = []
        self.results = []
        self.config_directory = config_directory
        self.update(data_file=data_file,
                    columns=columns,
                    field_delimiter=field_delimiter,
                    comments=comments,
                    whitespace=whitespace,
                    errors=errors,
                    data_on=data_on,
                    fifo=fifo,
                    repo_type=repo_type,
                    repo_url=repo_url,
                    repo_user=repo_user,
                    repo_password=repo_password,
                    repo_dir=repo_dir,
                    repo_file=repo_file,
                    )
        self.update_ordinals()
        if self.data.path:
            if False == os.path.exists(normalize_path(self.data.path)):
                self.active = False
    def update( self,
                columns=None,
                data_file=None,
                field_delimiter=None,
                comments=None,
                whitespace=None,
                errors=None,
                data_on=None,
                fifo=None,
                repo_type=None,
                repo_url=None,
                repo_user=None,
                repo_password=None,
                repo_dir=None,
                repo_file=None):
        if repo_type:
            if repo_type=='svn':
                self.data.repo_type=repo_type
                self.data.repo_url=repo_url
                self.data.repo_user=repo_user
                self.data.repo_password=repo_password
                self.data.repo_dir=repo_dir
                self.data.repo_file=repo_file
        if fifo:
            self.data.fifo=fifo
        if data_on:
            self.data.starts_on_line = data_on
        if comments:
            self.visible.comments = comments
        if whitespace:
            self.visible.whitespace = whitespace
        if errors:
            self.visible.errors = errors
        if field_delimiter:
            self.set_field_delimiter(field_delimiter)
        if data_file:
            self.data.path = data_file
        if columns:
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
        return self.column_length
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
        self.column_length=len(self.columns)
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
        try:
            index=self.ordinals[name]
            return row[index]
        except:
            raise Exception("Data Error")
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
        if None == self.data.config:
            self.data.config = os.path.join(home, "{0}.{1}.create.sql".format(self.data.database,self.data.name))
        if len(self.columns)==0:
            raise Exception("No columns in the table. Cant save")
        column_str=[]
        for column in self.columns:
            column_str.append("'{0}'".format(column.data.name))
        column_str=",".join(column_str)
        fifo=""
        if self.data.fifo:
            fifo="fifo='{0}'".format(self.data.fifo)
        if self.data.repo_type:
            repo="repo='{0}' url='{1}' user='{2}' password='{3}' dir='{4}' file='{5}'".format(
            self.data.repo_type,
            self.data.repo_url,
            self.data.repo_user,
            self.data.repo_password,
            self.data.repo_dir,
            self.data.repo_file)
        else:
            repo=""
        sql="create table '{0}'.'{1}' ({2}) file='{3}' {9} {10} delimiter='{4}' whitespace={5} errors={6} comments={7} data_starts_on={8} ".format(
                self.data.database,
                self.data.name,
                column_str,
                self.data.path,
                self.delimiters.field,
                self.visible.whitespace,
                self.visible.errors,
                self.visible.comments,
                self.data.starts_on_line,
                fifo,
                repo)
        with open(self.data.config,"w") as config_file:
            config_file.write(sql)
        return True
class table_visible_attributes:
    def __init__(self, yaml=None):
        self.comments = False
        self.errors = True
        self.whitespace = False
class table_data:
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
        self.fifo=None
        self.repo_type=None
        self.repo_url=None
        self.repo_user=None
        self.repo_password=None
        self.repo_dir=None
        self.repo_file=None
        if None != name:
            self.name = name
        if None != database:
            self.database = database
class table_ownership:
    def __init__(self, yaml=None):
        self.group = None
        self.entity = None
        self.location = None
class table_delimiters:
    def __init__(self, yaml=None):
        self.field = ","
        self.array = "|"
        self.error = "#"
        self.block_quote = None
        self.comment = ["#", ";", "/"]
        self.new_line = "\n"
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
    def __init__(self, config_file=None):
        self.curent_database = None
        self.tables = []
        self.config_file = None
        is_file = False
        if None != config_file and config_file != False:
            self.config_file = config_file
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
            print("Cant create configuration file: {0}".format(ex))
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
                     temporary=None,
                     fifo=None,
                     repo_type=None,
                     repo_url=None,
                     repo_user=None,
                     repo_password=None,
                     repo_dir=None,
                     repo_file=None,
                    ):
        if None == database_name:
            database_name = self.get_curent_database()
        exists = self.get(table_name, database_name)
        if None != exists:
            raise Exception("table already exists")
        if False == os.path.isfile(normalize_path(data_file)):
            raise Exception("Data file does not exist")
        if not temporary:
            if None == self.config_file:
                raise Exception("Not using a config file")
            config_directory = os.path.dirname(self.config_file)
        else:
            config_directory = None
        t = table(  name=table_name,
                    database=database_name,
                    columns=columns,
                    config_directory=config_directory,
                    field_delimiter=delimiter,
                    data_on=data_on,
                    comments=comments,
                    whitespace=whitespace,
                    errors=errors,
                    fifo=fifo,
                    repo_type=None,
                    repo_url=None,
                    repo_user=None,
                    repo_password=None,
                    repo_dir=None,
                    repo_file=None,)
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
    def get_db_sql(self):
        temp_tables = self.get_tables()
        queries=[]
        for t in temp_tables:
            with open(t,'r') as table_config:
                queries.append(table_config.read())
        return ";".join(queries)
    def get_tables(self):
        if None == self.config_file:
            return []
        if False == os.path.exists(self.config_file):
            return []
        tables = []
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
    def evaluate_single_match(self,context,test, row, table):
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
    def evaluate_match(self,context,query_object, row):
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
            success = self.evaluate_single_match(context,test_operation, row, table)
        if success is None:
            return False
        return success

        
# ############################################################################
# Module : functions
# File   : ./source/ddb/functions/functions.py
# ############################################################################

def f_row_number(context):
    if None==context:
        raise Exception("No engine instance. ")
    try:
        row=context.internal['row']
    except:
        row=0
    row+=1
    row=context.internal['row']=row
    return row
def f_database(context):
    if None==context:
        raise Exception("No engine instance. ")
    return context.database.get_curent_database()
def f_upper(context,arg):
    if None==context:
        raise Exception("No engine instance. ")
    if not arg:
        return None
    return arg.upper()
def f_lower(context,arg):
    if None==context:
        raise Exception("No engine instance. ")
    if not arg:
        return None
    return arg.lower()
def f_datetime(context,arg=None):
    if None==context:
        raise Exception("No engine instance. ")
    return datetime.datetime.now()
def f_time(context,arg=None):
    if None==context:
        raise Exception("No engine instance. ")
    return datetime.datetime.now().strftime('%H:%M:%S')
def f_date(context,arg=None):
    if None==context:
        raise Exception("No engine instance. ")
    return datetime.datetime.now().strftime('%Y-%m-%d')
def f_version(context,version=None):
    if None==context:
        raise Exception("No engine instance. ")
    if None==version:
        return 'GA.BB.LE'
    return version
def f_cat(context,arg1,arg2):
    if None==context:
        raise Exception("No engine instance. ")
    if None ==arg1:
        arg1=''
    if None ==arg2:
        arg2=''
    return '{0}{1}'.format(arg1,arg2)

        
# ############################################################################
# Module : sql_engine
# File   : ./source/ddb/engine.py
# ############################################################################

logging.basicConfig(filename='/tmp/ddb.log', filemode='a',level=logging.INFO,format='(%(threadName)-10s) %(message)s')
logging.propagate = False
def enum(**enums):
    return type('Enum', (), enums)
class engine:
    """A serverless flat file database engine"""
    def info(self,msg, arg1=None, arg2=None, arg3=None):
        if True == self.debug:
            if isinstance(arg1,str) :
                print(msg, arg1, arg2, arg3)
            elif isinstance(arg1,object) :
                print(msg, arg2, arg3)
                pp = pprint.PrettyPrinter(indent=4)
                pp.pprint(arg1)
            else:    
                print(msg, arg1, arg2, arg3)
    def __init__(self, config_file=None, query=None, debug=False, mode='array',output='TERM',output_style='single',readonly=None,output_file=None,field_delimiter=',',new_line='\n'):
        self.pid=os.getpid()
        if config_file is None:
            home = os.path.expanduser("~")
            config_file = os.path.join(os.path.join(home, '.ddb'), 'ddb.conf')
        self.data_type = enum(COMMENT=1, ERROR=2, DATA=3, WHITESPACE=4)
        self.debug = debug
        self.results = None
        self.mode = mode
        self.output=output
        self.output_file=output_file
        self.match=match()
        self.system={}
        self.system_trigger={}
        self.internal={}
        self.internal={'READONLY':readonly,'TEMP_FILES':{},'FIELD_DELIMITER':field_delimiter,'NEW_LINE':'\n'}
        uuid_str=uuid.uuid1()
        self.system['UUID']= uuid_str.urn[9:]
        self.system['DEBUG']=False
        self.system['AUTOCOMMIT']=True
        self.system['OUTPUT_MODULE']=output
        self.system['VERSION']=__version__
        try:
            self.system['PYTHON_MAJOR']=sys.version_info.major
            self.system['PYTHON_MINOR']=sys.version_info.minor 
            self.system['PYTHON_MICRO']=sys.version_info.micro
            self.system['PYTHON_RELEASELEVEL']=sys.version_info.releaselevel
            self.system['PYTHON_SERIAL']=sys.version_info.serial
        except:
            self.system['PYTHON_MAJOR']=sys.version_info[0]
            self.system['PYTHON_MINOR']=sys.version_info[1]
            self.system['PYTHON_MICRO']=sys.version_info[2]
            self.system['PYTHON_RELEASELEVEL']=sys.version_info[3]
            self.system['PYTHON_SERIAL']=sys.version_info[4]
            pass
        self.system['OUTPUT_STYLE']=output_style
        self.internal['OUTPUT_MODULES']=[
            {'name':'bash','styles':[]},
            {'name':'term','styles':['single','double','rst','time']},
            {'name':'raw' ,'styles':[]},
            {'name':'yaml','styles':[]},
            {'name':'json','styles':[]},
            {'name':'xml' ,'styles':[]}]
        self.system_trigger['DEBUG']=self.trigger_debug
        self.system['DELIMITER']=';'
        self.user={}
        self.internal['IN_TRANSACTION']=0
        try:        
            self.database = database(config_file=config_file)
            self.current_database = self.database.get_default_database()
            if config_file!=False:
                queries=self.database.get_db_sql()
                logging.disabled = True
                if queries:
                    self.query(queries)
                logging.disabled = False
        except Exception as ex:
            pass
        if None != query:
            self.query(query)
    def init_state_variables(self):
        self.internal['row']=0
    def trigger_debug(self):
        self.debug=self.system['DEBUG']
        self.database.debug=self.debug
    def debugging(self, debug=False):
        self.debug = debug
    def define_table(self, table_name, database_name, columns, data_file, field_delimiter=None,data_starts_on=None):
        """Progromatically define a table. Not saved to a configuration file, unless manualy activated"""
        t = table(database=database_name, columns=columns, name=table_name, data_file=data_file, field_delimiter=field_delimiter,data_on=data_starts_on)
        self.database.tables.append(t)
    def has_configuration(self):
        if None == self.database:
            return False
        return True
    def query(self, sql_query):
        try:
            start = time.perf_counter()
            wall_start = time.perf_counter()
        except:
            start = time.clock()
            wall_start = time.time()
            pass
        self.results = None
        if False == self.has_configuration():
            raise Exception("No table found")
        parser = lexer(sql_query,debug=True)
        if False == parser.query_objects:
            raise Exception("Invalid SQL")
        for query_object in parser.query_objects:
            self.init_state_variables()
            self.info("Engine: query_object", query_object)
            mode=query_object['mode']
            logging.info("PID:{1} : {0}".format(sql_query,self.pid))
            if mode == 'select':
                self.results = method_select(self,query_object, parser)
            elif mode == 'insert' and self.internal['READONLY']==None:
                self.results = method_insert(self,query_object)
            elif mode == 'update' and self.internal['READONLY']==None:
                self.results = method_update(self,query_object)
            elif mode == 'upsert' and self.internal['READONLY']==None:
                self.results = method_upsert(self,query_object)
            elif mode == 'delete' and self.internal['READONLY']==None:
                self.results = method_delete(self,query_object)
            elif mode == 'use':
                self.results = method_use(self,query_object)
            elif mode == 'drop' and self.internal['READONLY']==None:
                self.results = method_drop_table(self,query_object)
            elif mode == 'create' and self.internal['READONLY']==None:
                self.results = method_create_table(self,query_object)
            elif mode == 'update table' and self.internal['READONLY']==None:
                self.results = method_update_table(self,query_object)
            elif mode == 'set':
                self.results = method_system_set(self,query_object)
            elif mode == 'begin':
                self.results = method_system_begin(self,query_object)
            elif mode == 'rollback':
                self.results = method_system_rollback(self,query_object)
            elif mode == 'commit':
                self.results = method_system_commit(self)
            elif mode == "show tables":
                self.results = method_system_show_tables(self,self.database)
            elif mode == "show output modules":
                self.results = method_system_show_output_modules(self,query_object)
            elif mode == "show columns":
                self.results = method_system_show_columns(self,self.database, query_object)
            elif mode == "show variables":
                self.results = method_system_show_variables(self, query_object)
            elif mode == "describe table":
                self.results = method_describe_table(self, query_object)
            if False==self.results.success:
                break
        if self.results:
            self.results.delimiter=self.internal['FIELD_DELIMITER']
            self.results.new_line=self.internal['NEW_LINE']
            if self.results.data:
                if self.mode == 'object':
                    columns = self.results.columns
                    len_col = len(columns)
                    for line in self.results.data:
                        if line['type']==self.data_type.DATA:
                            new_dict = {}
                            for i in range(0, len_col):
                                if len(line['data']) < i:
                                    break
                                new_dict[columns[i]] = line['data'][i]
                            line['data']=new_dict
        if None == self.results:
            self.results=query_results()
        try:
            end = time.perf_counter()
            self.results.wall_end = time.time()
        except:
            end = time.clock()
            self.results.wall_end = time.time()
            pass
        self.results.start_time=start
        self.results.end_time=end
        self.results.time=end-start
        self.results.wall_start=wall_start
        self.results.wall_time=self.results.wall_start-self.results.wall_end
        return self.results
    def change_database(self, database_name):
        query = "use {0}".format(database_name)
        results = self.query(query)
        if None == results:
            return False
        return True
    def add_error(self,error):
        self.info(error)
    def os_cmd(self,cmd,err_msg):
        p = Popen(cmd, stdin=PIPE, stdout=PIPE, stderr=PIPE)
        output, err = p.communicate()
        rc = p.returncode
        if rc!=0:
            self.info(output)
            self.info(err)
            raise Exception("{0}: Exit Code {1}".format(err_msg,rc))
        return output
    def svn_get_file(self,table):
        c=1
    def svn_put_file(self,table):
        d=1
    def get_data_file(self,table,prefix="ddb_"):
        self.internal['IN_TRANSACTION']=1
        data_file=table.data.path
        if data_file not in self.internal['TEMP_FILES']:
            temp_data_file=create_temporary_copy(data_file,self.system['UUID'],prefix)
            self.internal['TEMP_FILES'][data_file]={'origin':data_file,'temp_source':temp_data_file,'written':None}
        return self.internal['TEMP_FILES'][data_file]['temp_source']
    def autocommit_write(self,table,dest_file):
        table_key=table.data.path
        if table_key in self.internal['TEMP_FILES']:
            self.internal['TEMP_FILES'][table_key]['written']=True
            if dest_file and dest_file!=self.internal['TEMP_FILES'][table_key]['temp_source']:
                remove_temp_file(self.internal['TEMP_FILES'][table_key]['temp_source'])
                self.internal['TEMP_FILES'][table_key]['temp_source']=dest_file
    def auto_commit(self,table):
        if self.system['AUTOCOMMIT']==True:
            method_system_commit(self)

        
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
    if query_object['table'].data.starts_on_line > line_number:
        line_type = context.data_type.COMMENT
        line_data = line
        match=False
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
                line_data = line_cleaned.split(query_object['table'].delimiters.field,column_len)
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
                match_results = context.match.evaluate_match(context,query_object, line_data)
            else:
                match_results = False
        if query_object['table'].visible.whitespace is False and line_type==context.data_type.WHITESPACE:
            match_results=False
        elif query_object['table'].visible.comments is False and line_type==context.data_type.COMMENT:
            match_results=False
        elif query_object['table'].visible.errors is False and line_type==context.data_type.ERROR:
            match_results=False
    return {'data': line_data, 
            'type': line_type, 
            'raw': line_cleaned, 
            'line_number': line_number, 
            'match': match_results, 
            'error': err}
class query_results:
    def __init__(self,success=False,affected_rows=0,data=None,error=None,diff=None,total_data_length=0,delimiter=None,new_line=None):
        self.success=success
        self.affected_rows=affected_rows
        self.data=[]
        self.diff=diff
        self.error=error
        self.data_length=0
        self.column_length=0
        self.total_data_length=0
        self.delimiter=delimiter
        self.new_line=new_line
        self.columns=[]
        if data and data.results:
            self.data=data.results
            self.data_length=len(data.results)
        if data:
            self.columns = data.get_columns_display()
            self.column_length=len(self.columns)
    def get_first(self):
        try:
            return self.data[0]['data'][0]
        except:
            pass
        return None
    def is_single(self):
        try:
            if len(self.data)==1:
                return True
        except:
            pass
        return None
    def debug(self):
        pprint.pprint(self.error)
        pprint.pprint(self.data)

        
# ############################################################################
# Module : methods-records-delete
# File   : ./source/ddb/methods/record_delete.py
# ############################################################################

def method_delete(context, query_object):
    try:
        if 'database' in query_object['meta']['from']:
            context.info('Database specified')
            database_name = query_object['meta']['from']['database']
        else:
            context.info('Using curent database context')
            database_name = context.database.get_curent_database()
        table_name = query_object['meta']['from']['table']
        table= context.database.get(table_name,database_name)
        query_object['table']=table
        if None == query_object['table']:
            raise Exception("Table '{0}' does not exist.".format(table_name))
        line_number = 1
        affected_rows = 0
        temp_data_file=context.get_data_file(table)
        diff=[]
        with open(temp_data_file, 'r') as content_file:
            temp_file=tempfile.NamedTemporaryFile(mode='w', prefix="DST_DELETE",delete=False) 
            for line in content_file:
                processed_line = process_line(context,query_object, line, line_number)
                if None != processed_line['error']:
                    context.add_error(processed_line['error'])
                line_number += 1
                if True == processed_line['match']:
                    affected_rows += 1
                    diff.append("Deleted Line: {0}, {1}".format(line_number-1,line))
                    continue
                temp_file.write(processed_line['raw'])
                temp_file.write(query_object['table'].delimiters.get_new_line())
            temp_file.close()
            context.autocommit_write(table,temp_file.name)
        context.auto_commit(table)
        return  query_results(success=True,affected_rows=affected_rows,diff=diff)
    except Exception as ex:
        print(ex)
        return  query_results(success=False, error=ex)

        
# ############################################################################
# Module : methods-records-insert
# File   : ./source/ddb/methods/record_insert.py
# ############################################################################

def method_insert(context, query_object):
        if 'database' in query_object['meta']['into']:
            context.info('Database specified')
            database_name = query_object['meta']['into']['database']
        else:
            context.info('Using curent database context')
            database_name = context.database.get_curent_database()
        table_name = query_object['meta']['into']['table']
        table= context.database.get(table_name,database_name)
        query_object['table']=table
        if None == query_object['table']:
            raise Exception("Table '{0}' does not exist.".format(table_name))
        line_number = 1
        affected_rows = 0
        requires_new_line = False
        temp_data_file=context.get_data_file(table,"SRC_INSERT")
        diff=[]
        with open(temp_data_file, 'r') as content_file:
            with tempfile.NamedTemporaryFile(mode='w', prefix="DST_INSERT",delete=False) as temp_file:
                for line in content_file:
                    processed_line = process_line(context,query_object, line, line_number)
                    if None != processed_line['error']:
                        context.add_error(processed_line['error'])
                    line_number += 1
                    temp_file.write(processed_line['raw'])
                    temp_file.write(query_object['table'].delimiters.get_new_line())
                    requires_new_line = False
                results = create_single(context,query_object, temp_file, requires_new_line)
                if True == results['success']:
                    diff.append(results['line'])
                    affected_rows += 1
                temp_file.close()
                context.autocommit_write(table,temp_file.name)
        context.auto_commit(table)
        return query_results(success=True,affected_rows=affected_rows,diff=diff)
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
        return {'success':True,'line':new_line}
    else:
        return {'success':False,'line':new_line}

        
# ############################################################################
# Module : methods-records-select
# File   : ./source/ddb/methods/record_select.py
# ############################################################################

context_sort=[]
def method_select(context, query_object, parser):
        context.info(query_object)
        select_validate_columns_and_from(context,query_object,parser)
        temp_table = context.database.temp_table()
        add_table_columns(context,query_object,temp_table)
        set_ordinals(context,query_object)
        temp_data=select_process_file(context,query_object)
        all_records_count=len(temp_data)
        temp_data=order_by(context,query_object,temp_data)
        temp_data=distinct(context,query_object,temp_data)
        temp_data = limit(context, query_object, temp_data)
        temp_table.results=temp_data
        return query_results(success=True,data=temp_table,total_data_length=all_records_count)
def select_process_file(context,query_object):
    has_columns = select_has_columns(context,query_object)
    has_functions = select_has_functions(context,query_object)
    table=None
    line_number = 1
    data=[]
    if True == has_columns:
        if 'table' in  query_object:
            table= query_object['table']
        else:
            raise Exception ('table configuration has no data file')
        temp_data_file=context.get_data_file(table)
        with open(temp_data_file, 'r') as content_file:
            for line in content_file:
                processed_line = process_line(context,query_object, line, line_number)
                if False == processed_line['match']:
                    line_number += 1
                    continue
                if None != processed_line['data']:
                    restructured_line = process_select_row(context,query_object,processed_line) 
                    data.append(restructured_line)
                line_number += 1
        context.auto_commit(table)
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
            table= context.database.get(table_name,database_name)
            if None == table:
                except_str="Table '{0}' does not exist.".format(table_name)
                raise Exception(except_str)
            query_object['table']= table
            table_columns = table.get_columns()
            parser.expand_columns(query_object, table_columns)
            column_len = table.column_count()
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
    if 'table' in query_object:
        ordinals=query_object['table'].ordinals
    else:
        ordinals=None
    if None == processed_line:
        line_type=context.data_type.DATA
        error= None
        raw= None
        for c in query_object['meta']['columns']:
            if 'function' in c:
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
                elif c['function'] == 'row_number':
                        row.append(f_row_number(context))
    else:
        line_type=processed_line['type']
        error= processed_line['error']
        raw= processed_line['raw']
        if line_type!=context.data_type.ERROR:
            for c in query_object['meta']['columns']:
                if 'column' in c:
                    row.append(processed_line['data'][ordinals[c['column']]])
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
                    elif c['function'] == 'row_number':
                            row.append(f_row_number(context))
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
            if length<0:
                raise Exception("Limit: range index invalid, Value:'{0}'".format(index))
    context.info("Limit:{0},Length:{1}".format(index, length))
    if index<0:
        raise Exception("Limit: range index invalid, Value:'{0}'".format(index))
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
        return {'success':True,'line':new_line}
    else:
        return {'success':False,'line':new_line}
def method_update(context, query_object):
    try:
        if 'database' in query_object['meta']['update']:
            context.info('Database specified')
            database_name = query_object['meta']['update']['database']
        else:
            context.info('Using curent database context')
            database_name = context.database.get_curent_database()
        table_name = query_object['meta']['update']['table']
        table= context.database.get(table_name,database_name)
        query_object['table']=table
        if None == query_object['table']:
            raise Exception("Table '{0}' does not exist.".format(table_name))
        line_number = 1
        affected_rows = 0
        temp_data_file=context.get_data_file(table)
        diff=[]
        with open(temp_data_file, 'r') as content_file:
            with tempfile.NamedTemporaryFile(mode='w', prefix="UPDATE",delete=False) as temp_file:
                for line in content_file:
                    processed_line = process_line(context,query_object, line, line_number)
                    if None != processed_line['error']:
                        context.add_error(processed_line['error'])
                    line_number += 1
                    if True == processed_line['match']:
                        results = update_single(context,query_object, temp_file,  False, processed_line)
                        if True == results['success']:
                            diff.append(results['line'])
                            affected_rows += 1
                        continue
                    temp_file.write(processed_line['raw'])
                    temp_file.write(query_object['table'].delimiters.get_new_line())
                temp_file.close()
                context.autocommit_write(table,temp_file.name)
        context.auto_commit(table)
        return query_results(affected_rows=affected_rows,success=True,diff=[])
    except Exception as ex:
        return query_results(success=False,error=ex)

        
# ############################################################################
# Module : methods-records-upsert
# File   : ./source/ddb/methods/record_upsert.py
# ############################################################################

def method_upsert(context, query_object):
    try:
        if 'database' in query_object['meta']['into']:
            context.info('Database specified')
            database_name = query_object['meta']['into']['database']
        else:
            context.info('Using curent database context')
            database_name = context.database.get_curent_database()
        table_name = query_object['meta']['into']['table']
        table= context.database.get(table_name,database_name)
        query_object['table']=table
        if None == query_object['table']:
            raise Exception("Table '{0}' does not exist.".format(table_name))
        if 'on duplicate key' not in query_object['meta']:
            raise Exception("Upsert missing duplicate keys")
        where=[]
        for item in query_object['meta']['on duplicate key']:
            column=item['column']
            for index in range(0,len(query_object['meta']['columns'])):
                column_compare=query_object['meta']['columns'][index]['column']
                if column_compare==column:
                    value=query_object['meta']['values'][index]['value']
                    if len(where)==0:
                        mode='where'
                    else:
                        mode='and'
                    where.append({mode:{'e1':column,'c':'=','=':'=','e2':value}})
        query_object['meta']['where']=where
        context.info("Query object",query_object)
        line_number = 1
        affected_rows = 0
        temp_data_file=context.get_data_file(table)
        diff=[]
        with open(temp_data_file, 'r') as content_file:
            with tempfile.NamedTemporaryFile(mode='w', prefix="UPSERT",delete=False) as temp_file:
                for line in content_file:
                    processed_line = process_line(context,query_object, line, line_number)
                    if None != processed_line['error']:
                        context.add_error(processed_line['error'])
                    line_number += 1
                    if True == processed_line['match']:
                        results = update_single(context,query_object, temp_file,  False, processed_line)
                        if True == results['success']:
                            diff.append(results['line'])
                            affected_rows += 1
                        continue
                    temp_file.write(processed_line['raw'])
                    temp_file.write(query_object['table'].delimiters.get_new_line())
                if affected_rows==0:
                    context.info("No row found in upsert, creating")
                    results = create_single(context,query_object, temp_file,False)
                    if True==results['success']:
                        diff.append(results['line'])
                else:
                    context.info("row found in upsert")
                temp_file.close()
                context.autocommit_write(table,temp_file.name)
        context.auto_commit(table)                
        return query_results(affected_rows=affected_rows,success=True,diff=diff)
    except Exception as ex:
        print ("ERR",ex)
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
        print (ex)
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
        fifo = None
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
        if 'fifo' in query_object['meta']:
            fifo = query_object['meta']['fifo']
        if 'repo' in query_object['meta']:
            repo=query_object['meta']['repo']
            if 'type' in repo:
                repo_type=repo['type']
            if 'url' in repo:
                repo_url=repo['url']
            if 'user' in repo:
                repo_user=repo['user']
            if 'password' in repo:
                repo_password=repo['password']
            if 'dir' in repo:
                repo_dir=repo['dir']
            if 'file' in repo:
                repo_file=repo['file']
        else:
            repo_type=None
            repo_url=None
            repo_user=None
            repo_password=None
            repo_dir=None
            repo_file=None
        results = context.database.create_table(table_name=query_object['meta']['table'],
                                                database_name=database_name,
                                                columns=columns,
                                                data_file=query_object['meta']['file'],
                                                delimiter=found_delimiter,
                                                comments=found_comments,
                                                errors=found_errors,
                                                whitespace=found_whitespace,
                                                data_on=found_data_on,
                                                temporary=temporary,
                                                fifo=fifo,
                                                repo_type=repo_type,
                                                repo_url=repo_url,
                                                repo_user=repo_user,
                                                repo_password=repo_password,
                                                repo_dir=repo_dir,
                                                repo_file=repo_file,                                                
                                                )
        return query_results(success=results)
    except Exception as ex:
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
        if 'database' in query_object['meta']['describe table']:
            context.info('Database specified')
            database_name = query_object['meta']['describe table']['database']
        else:
            context.info('Using curent database context')
            database_name = context.database.get_curent_database()
        table_name=query_object['meta']['describe table']['table']
        target_table= context.database.get(table_name,database_name=database_name)
        if None ==target_table:
            raise Exception("Table not found")
        temp_table.add_column('option')
        temp_table.add_column('value')
        temp_table.append_data({'data':['active',target_table.active], 'type': context.data_type.DATA, 'error': None})
        temp_table.append_data({'data':['table_name',target_table.data.name], 'type': context.data_type.DATA, 'error': None})
        temp_table.append_data({'data':['database',target_table.data.database], 'type': context.data_type.DATA, 'error': None})
        temp_table.append_data({'data':['data_file',target_table.data.path], 'type': context.data_type.DATA, 'error': None})
        temp_table.append_data({'data':['fifo',target_table.data.fifo], 'type': context.data_type.DATA, 'error': None})
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
# Module : methods-system-set
# File   : ./source/ddb/methods/system_set.py
# ############################################################################

def method_system_set(context, query_object):
    context.info("set")
    try:
        for item in query_object['meta']['set']:
            variable=item['variable'].upper()
            value=item['value']
            value_up=value.upper()
            if len(variable)>0 and variable[0]=='@':
                var_type='user'
            else:
                var_type='system'
            if value_up in ['FALSE','NO',"OFF"]:
                value=False
            elif value_up in ['TRUE','YES',"ON"]:
                value=True
            elif value_up in ['NULL','NILL','NONE']:
                value=None
            if var_type=='system':
                if variable in context.system:
                    context.system[variable]=value
                    if variable in context.system_trigger:
                        context.system_trigger[variable]()
                else:
                    raise Exception("Cannot set {0}, not a system variable".format(variable))
            elif var_type=='user':
                context.user[variable]=value
        return query_results(success=True)
    except Exception as ex:
        return query_results(success=False,error=ex)

        
# ############################################################################
# Module : methods-system-begin
# File   : ./source/ddb/methods/system_begin.py
# ############################################################################

def method_system_begin(context, query_object):
    context.info("set")
    try:
        if context.internal['IN_TRANSACTION']==1:
            raise Exception("Already in a Batch Transaction")
        else:
            context.internal['AUTOCOMMIT_HOLODER']=context.system['AUTOCOMMIT']
            context.system['AUTOCOMMIT']=False
            context.internal['IN_TRANSACTION']=1
        return query_results(success=True)
    except Exception as ex:
        return query_results(success=False,error=ex)

        
# ############################################################################
# Module : methods-system-commit
# File   : ./source/ddb/methods/system_commit.py
# ############################################################################

def method_system_commit(context):
    """Move temp files to source files"""
    context.info("Commit")
    try:
        if context.internal['IN_TRANSACTION']==1:
            context.internal['IN_TRANSACTION']=0
            context.system['AUTOCOMMIT']=context.internal['AUTOCOMMIT_HOLODER']=True
            for table_key in context.internal['TEMP_FILES']:
                tmp=context.internal['TEMP_FILES'][table_key]
                if None== tmp['written']:
                    remove_temp_file(tmp['temp_source'])
                    lock.release(table_key)
                else:
                    swap_files(tmp['origin'],tmp['temp_source'],context.system['UUID'])
            context.internal['TEMP_FILES']={}
        else:
            raise Exception("Cannot commit, not in a transaction")
        return query_results(success=True)
    except Exception as ex:
        return query_results(success=False,error=ex)

        
# ############################################################################
# Module : methods-system-rollback
# File   : ./source/ddb/methods/system_rollback.py
# ############################################################################

def method_system_rollback(context, query_object):
    context.info("set")
    try:
        if context.internal['IN_TRANSACTION']==1:
            context.internal['IN_TRANSACTION']=0
            context.system['AUTOCOMMIT']=context.internal['AUTOCOMMIT_HOLODER']=True
            for table_key in context.internal['TEMP_FILES']:
                tmp=context.internal['TEMP_FILES'][table_key]
                remove_temp_file(tmp['temp_source'])
                lock.release(table_key)
            context.internal['TEMP_FILES']={}
        else:
            raise Exception("Cannot rollback, not in a transaction")
        return query_results(success=True)
    except Exception as ex:
        return query_results(success=False,error=ex)

        
# ############################################################################
# Module : methods-system-show-columns
# File   : ./source/ddb/methods/system_show_columns.py
# ############################################################################

def method_system_show_columns(context,database, query_object):
    try:
        if 'database' in query_object['meta']['from']:
            context.info('Database specified')
            database_name = query_object['meta']['from']['database']
        else:
            context.info('Using curent database context')
            database_name = context.database.get_curent_database()
        table = database.get(query_object['meta']['from']['table'],database_name=database_name)
        temp_table = database.temp_table(columns=['database','table', 'column'])
        if table:
            for c in table.columns:
                columns = {'data': [table.data.database,table.data.name, c.data.name], 'type': context.data_type.DATA, 'error': None}
                temp_table.append_data(columns)
        return query_results(success=True,data=temp_table)
    except Exception as ex:
        print (ex)
        return query_results(success=False,error=ex)

        
# ############################################################################
# Module : methods-system-show-tables
# File   : ./source/ddb/methods/system_show_tables.py
# ############################################################################

def method_system_show_tables(context,database):
    try:
        temp_table = database.temp_table(columns=['database', 'table'])
        for t in database.tables:
            columns = [t.data.database, t .data.name]
            temp_table.append_data({'data': columns, 'type': context.data_type.DATA, 'error': None})
        return query_results(success=True,data=temp_table)
    except Exception as ex:
        return query_results(success=False,error=ex)

        
# ############################################################################
# Module : methods-system-show-variables
# File   : ./source/ddb/methods/system_show_variables.py
# ############################################################################

def method_system_show_variables(context, query_object):
    context.info("show variables")
    try:
        temp_table = context.database.temp_table(columns=['type','name','value'])
        for c in context.system:
            columns = {'data': ['system',c,context.system[c]], 'type': context.data_type.DATA, 'error': None}
            temp_table.append_data(columns)
        for c in context.user:
            columns = {'data': ['user',c,context.user[c]], 'type': context.data_type.DATA, 'error': None}
            temp_table.append_data(columns)
        return query_results(success=True,data=temp_table)
    except Exception as ex:
        print (ex)
        return query_results(success=False,error=ex)

        
# ############################################################################
# Module : methods-system-show-output-modules
# File   : ./source/ddb/methods/system_show_output_modules.py
# ############################################################################

def method_system_show_output_modules(context,query_object):
    try:
        temp_table = context.database.temp_table(columns=['output_module', 'output_style'])
        for t in context.internal['OUTPUT_MODULES']:
            styles=""
            if len(t['styles'])>0:
                styles=", ".join(t['styles'])
            columns = [t['name'], styles]
            temp_table.append_data({'data': columns, 'type': context.data_type.DATA, 'error': None})
        return query_results(success=True,data=temp_table)
    except Exception as ex:
        return query_results(success=False,error=ex)

        
# ############################################################################
# Module : file_io-lock
# File   : ./source/ddb/file_io/locking.py
# ############################################################################

class lock:
    max_lock_time=2
    sleep_time=0.02
    LOCK_NONE=0
    LOCK_OWNER=1
    LOCK_OTHER=2
    @staticmethod
    def info(msg,data):
        if 1==2:
            print("{0}: {1}".format(msg,data))
    @staticmethod
    def normalize_path(path):
        """Update a relative or user absed path to an ABS path"""
        normalized_path=os.path.abspath(os.path.expanduser(path))
        return normalized_path
    @staticmethod
    def get_lock_filename(path):
        norm_path=lock.normalize_path(path)
        temp_dir = tempfile.gettempdir()
        basename=os.path.basename(norm_path)
        temp_file_name='{0}.lock'.format(basename)
        norm_lock_path = os.path.join(temp_dir, temp_file_name)
        return norm_lock_path
    @staticmethod
    def is_locked(path,key_uuid):
        lock_path=lock.get_lock_filename(path)
        if os.path.exists(lock_path):
            with open(lock_path,'r') as lockfile:
                try:
                    file_data=lockfile.readline()
                    timestamp,temp_file_path,owner_uuid=file_data.split('|')
                    file_lock_time=datetime.datetime.strptime(timestamp,'%Y-%m-%d %H:%M:%S.%f')
                    curent_datetime =datetime.datetime.now()
                    elapsed_time=curent_datetime-file_lock_time
                    if elapsed_time.seconds>lock.max_lock_time:
                        lock.info("Lock","Releasing, lock aged out")
                        lock.release(path)
                        return lock.LOCK_NONE
                    if owner_uuid==key_uuid:
                        lock.info("Lock","owned by current process")
                        return lock.LOCK_OWNER
                    else:
                        lock.info("Lock","owned by other process")
                        return lock.LOCK_OTHER
                except Exception as ex:
                    lock.info("Lock","error".format(ex))
                    lock.release(path)
                    pass
        lock.info("Lock","No Lock")
        return lock.LOCK_NONE
    @staticmethod
    def release(path):
        lock_path=lock.get_lock_filename(path)
        if os.path.exists(lock_path)==False:
            raise Exception ("Lockfile cannot be removed, it doesnt exist. {0}".format(lock_path))
        os.remove(lock_path)
        if os.path.exists(lock_path):
            raise Exception ("Lockfile cannot be removed. {0}".format(lock_path))
        lock.info("Lock","removed")
    @staticmethod
    def aquire(path,key_uuid):
        lock_time=0
        lock_cycle=0
        while 1:
            lock_status=lock.is_locked(path,key_uuid)
            if lock_status<lock.LOCK_OTHER:
                break
            lock.info("Lock","File locked, waiting till file timeout, or max lock retry time, {0},{1},{2}".format(path,lock_time,lock_status))
            time.sleep(lock.sleep_time)
            lock_time+=lock.sleep_time
            lock_cycle+=1
            if lock_time>lock.max_lock_time:
                lock.info("Lock","Cannot aquire lock, timeout")
                raise Exception( "Cannot aquire lock, max timeout of {0} seconds reached. Aproxomatly '{1}' cycles".format(lock.max_lock_time,lock_cycle))
        lock_path=lock.get_lock_filename(path)
        with open(lock_path,'w') as lockfile:
            lock_time=datetime.datetime.now()
            lock_time_str="{0}".format(lock_time)
            lock.info("Lock Time",lock_time_str)
            lockfile.write("{0}|{1}|{2}".format(lock_time_str,path,key_uuid))
            lockfile.flush()
        if os.path.exists(lock_path)==False:
            lock.info("Lock","Failed to create")
            raise Exception ("Lockfile failed to create {0}".format(lock_path))
def create_temporary_copy(path,uuid,prefix='ddb_'):
    """ Create a copy of a regular file in a temporary directory """
    try:
        lock.aquire(path,uuid)
        temp_dir = tempfile.gettempdir()
        temp_base_name=next(tempfile._get_candidate_names())
        if prefix:
            temp_file_name="{0}_{1}".format(prefix,temp_base_name)
        else:
            temp_file_name="{0}".format(temp_base_name)
        temp_path = os.path.join(temp_dir, temp_file_name)
        shutil.copy2(normalize_path(path), temp_path)
        return temp_path
    except Exception as ex:
        raise Exception("Temp File Error: {0}".format(ex))
def remove_temp_file(path):
    try:
        os.remove(path)
        if os.path.exists(path):
            raise Exception("Failed to delete: {0}".format(path))    
    except Exception as ex:
        raise Exception("Temp File Error: {0}".format(ex))
def swap_files(path, temp,key_uuid):
    """ Swap a temporary file with a regular file, by deleting the regular file, and copying the temp to its location """
    try:
        if lock.LOCK_OWNER != lock.is_locked(path,key_uuid):
            raise Exception("Cannot swap files, expected lock. Didnt find one {0}".format(path))
        norm_path=normalize_path(path)
        if os.path.exists(norm_path):
            os.remove(norm_path)
        if os.path.exists(norm_path):
            raise Exception("Deleting file {0} failed".format(norm_path))
        lock.release(path)
        shutil.copy2(temp, norm_path)
        os.remove(temp)
        if os.path.exists(temp):
            raise Exception("Deleting temp file {0} failed".format(temp))
    except Exception as ex:
        raise Exception("File Error: {0}".format(ex))
def normalize_path(path):
    """Update a relative or user absed path to an ABS path"""
    normalized_path=os.path.abspath(os.path.expanduser(path))
    return normalized_path

        
# ############################################################################
# Module : output
# File   : ./source/ddb/output/factory.py
# ############################################################################

class output_factory:
    def __init__(self,query_results,output='term',output_style="flextable",output_file=None,output_stream='STDIO',color=True): # style single double rst
            """display results in different formats
            if output_file==None then everything is directed to stdio
            output=(bash|term|yaml|json|xml)
            output_file= None or file to write to
            """        
            if None==query_results:
                return
            self.output=None
            mode=output.lower()
            if 'bash'==mode:
                self.output=self.format_bash(query_results)
            elif 'term'==mode:
                self.output=self.format_term(query_results,output_style,output_stream=output_stream,color=color)
            elif 'raw'==mode:
                self.output=self.format_raw(query_results,output_stream)
            elif 'yaml'==mode:
                self.output=self.format_yaml(query_results)
            elif 'json'==mode:
                self.output=self.format_json(query_results)
            elif 'xml'==mode:
                self.output=self.format_xml(query_results)
            elif 'time'==mode:
                self.output ="User Time:Start:{0}, End:{1}, Elapsed:{2}".format(query_results.start_time,query_results.end_time,query_results.time)
                self.output+="Wall Time:Start:{0}, End:{1}, Elapsed:{2}".format(query_results.wall_start,query_results.wall_end,query_results.wall_time)            #default
            else: 
                self.output=self.format_term(query_results)
    def format_term(self,query_results,output_style=None,output_stream=None,color=True):
        """ouput results data in the term format"""
        if query_results.columns:
            ft=flextable(data=query_results.data,columns=query_results.columns,display_style=output_style,output_stream=output_stream,render_color=color)
            res=ft.output_destination
        else:
            res=None
        if True == query_results.success:
            if res:
                res.append("executed in {0:.6f}, {1} rows returned".format(query_results.time,query_results.data_length))
            else:
                print("executed in {0:.6f}, {1} rows returned".format(query_results.time,query_results.data_length))
        else:
            if res:
                res.append("Query Failed")
            else:
                print("Query Failed")
        return res
    def format_bash(self,query_results):
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
    def format_raw(self,query_results,output_stream):
        """ouput results data in the yaml format"""
        delimiter=query_results.delimiter
        res=[]
        for row in query_results.data:
            if 'data' in row:
                raw=delimiter.join(row['data'])
                if output_stream=='STDIO':
                    print(raw)
                else:
                    res.append(raw)
        if output_stream=='STRING':
            return res
    def format_yaml(self,query_results):
        """ouput results data in the yaml format"""
        results=query_results.data
        factory=factory_yaml()
        dump=factory.dump(results)
        print(dump)
    def format_json(self,query_results):
        """ouput results data in the json format"""
        results=query_results.data
        factory=factory_json()
        dump=factory.dumps(results)
        print(dump)
    def format_xml(self,query_results):
        """ouput results data in the xml format"""
        results=query_results.data
        factory=factory_xml()
        dump=factory.dumps({'data':results})
        print(dump)

        
# ############################################################################
# Module : factory_term
# File   : ./source/ddb/output/factory_term.py
# ############################################################################

class flextable:
    def escape(c):
        return '\033[{0}m'.format(c)
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
        def __init__(self,style='rst'):
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
                if text.isspace(): 
                    text=None
            self.text=text
        def render(self,text=None, length=None,fill_character=' ',override=None,use_color=True):
            if text==None:
                text=self.text
            if None == text:
                text=''
            if not isinstance(text,unicode):
                text=str(text)
            if text.find('\t')>-1:
                text=text.replace('\t','       ')
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
            def __init__(self,default=None,style='rst'):
                if style=='single':
                    l=u'│'
                    r=u'│'
                    t=u'─'
                    b=u'─'
                elif style=='double':
                    l=u'║'
                    r=u'║'
                    t=u'═'
                    b=u'═'
                elif style=='rst':
                    l=u'|'
                    r=u'|'
                    t=u'-'
                    b=u'-'
                self.left   =flextable.color(text=l,default=default)
                self.right  =flextable.color(text=r,default=default)
                self.top    =flextable.color(text=t,default=default)
                self.bottom =flextable.color(text=b,default=default)
        class char_center:
            def __init__(self,default=None,style='rst'):
                if style=='single':
                    l=u'├'
                    c=u'┼'
                    r=u'┤'
                elif style=='double':
                    l=u'╠'
                    c=u'╬'
                    r=u'╣'
                elif style=='rst':
                    l=u'|'
                    c=u'|'
                    r=u'|'
                self.center = flextable.color(text=c,default=default)
                self.left   = flextable.color(text=l,default=default)
                self.right  = flextable.color(text=r,default=default)
        class char_rst:
            def __init__(self,default=None):
                self.edge   =flextable.color(text='+',default=default)
                self.space  =flextable.color(text=' ',default=default)
                self.header =flextable.color(text='=',default=default)
                self.row    =flextable.color(text='-',default=default)
        class char_bottom:
            def __init__(self,default=None,style='rst'):
                if style=='single':
                    l=u'└'
                    c=u'┴'
                    r=u'┘'
                elif style=='double':
                    l=u'╚'
                    c=u'╩'
                    r=u'╝'
                elif style=='rst':
                    l=u'+'
                    c=u'+'
                    r=u'+'
                self.left   = flextable.color(text=l,default=default)
                self.center = flextable.color(text=c,default=default)
                self.right  = flextable.color(text=r,default=default)
        class char_top:
            def __init__(self,default=None,style='rst'):
                if style == 'single':
                    l=u'┌'
                    c=u'┬'
                    r=u'┐'
                elif style=='double':
                    l=u'╔'
                    c=u'╦'
                    r=u'╗'
                elif style=='rst':
                    l=u'|'
                    c=u'|'
                    r=u'|'
                self.left   = flextable.color(text=l,default=default)
                self.right  = flextable.color(text=r,default=default)
                self.center = flextable.color(text=c,default=default)
        class char_header:
            def __init__(self,default=None,style='rst'):
                if style=='single':
                    l=u'┤'
                    c=u' '
                    r=u'├'
                elif style=='double':
                    l=u'╡'
                    c=u' '
                    r=u'╞'
                elif style=='rst':
                    l=u''
                    c=u' '
                    r=u''
                self.left   = flextable.color(text=l,default=default,foreground='White')
                self.right  = flextable.color(text=r,default=default,foreground='White')
                self.center = flextable.color(text=c,default=default,foreground='green')
        class char_mid_header:
            def __init__(self,default=None,style='rst'):
                if style == 'single':
                    l=u'-'
                    c=u' '
                    r=u'-'
                elif style== 'double':
                    l=u'-'
                    r=u'-'
                    c=u' '
                elif style=='rst':
                    l=u'-'
                    c=u' '
                    r=u'-'
                self.left   = flextable.color(text=l,default=default,foreground='White')
                self.right  = flextable.color(text=r,default=default,foreground='White')
                self.center = flextable.color(text=c,default=default,foreground='green')
        class char_footer:
            def __init__(self,default=None,style='rst'):
                if style=='single':
                    l=u'['
                    c=u' '
                    r=u']'
                elif style=='double':
                    l=u'['
                    c=u' '
                    r=u']'
                elif style=='rst':
                    l=None
                    c=u' '
                    r=None
                self.left   = flextable.color(text=l,default=default,foreground='White') #╡
                self.right  = flextable.color(text=r,default=default,foreground='White') #╞
                self.center = flextable.color(text=c,default=default,foreground='green')
        def __init__(self,default=None,style='rst'):
            self.walls      =self.char_walls(default=default,style=style)
            self.center     =self.char_center(default=default,style=style)
            self.bottom     =self.char_bottom(default=default,style=style)
            self.top        =self.char_top(default=default,style=style)
            self.mid_header =self.char_mid_header(default=default,style=style)
            self.header     =self.char_header(default=default,style=style)
            self.footer     =self.char_footer(default=default,style=style)
            self.rst        =self.char_rst(default=default)
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
                            render_color=True,
                            output_stream='STDIO'
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
        if display_style not in ['single','double','rst']:
            display_style='single'    
        self.display_style=display_style
        if output_stream=='STDIO':
            self.output_destination=None
        elif output_stream=='STRING':
            self.output_destination=[]
        else:
            self.output_destination=None
        if self.column_width==-1:
            try:
                self.row_height,self.column_width = os.popen('stty -F /dev/tty size', 'r').read().split()
            except:
                self.row_height=25
                self.column_width=80
                pass
        if column_count>-1 and columns == None:
            self.columns=[]
            for n in range(0,self.column_count):
                self.columns.append("column{0}".format(n+1))
        else:
            self.column_count=len(columns)
        if page>-1 and length:
            if length>0:
                self.starts_on=page*length+1
        if self.line>-1:
            self.starts_on=line
        if display_style=='rst':
            self.footer=False
            self.header_every=0
        self.style=self.flextable_style(style=self.display_style)
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
        if column.left.text:
            column_pad+=1
        if column.right.text:
            column_pad+=1
        if None != self.columns:
            index=0
            for c in self.columns:
                column_display=''
                if column.left.text:
                    column_display=column.left.render(use_color=self.render_color)
                column_display+=column.center.render(use_color=self.render_color,text=c,length=self.column_character_width-column_pad)
                if column.right.text:
                    column_display+=column.right.render(use_color=self.render_color)
                header+=column_display
                if index<len(self.columns)-1:
                    if len('{0}'.format(c))>self.column_character_width-2:
                        header+=base.center.render(use_color=self.render_color,override=self.style.color.overflow)
                    else:
                        header+=base.center.render(use_color=self.render_color)
                index+=1
        header+=base.right.render(use_color=self.render_color)
        if self.render_color==True:
            header+='{0}'.format(flextable.reset.ALL)
        return header
    def build_rows(self,buffer):
        rows=[]
        index=0
        if True == isinstance(buffer,list):
            for line in buffer:
                data_len=len(line['data'])
                columns=self.style.characters.walls.left.render(use_color=self.render_color)
                if self.data_type.DATA == line['type']:
                    for c in line['data']:
                        columns+=self.style.color.data.render(c,use_color=self.render_color,length=self.column_character_width)
                        if len('{0}'.format(c))>self.column_character_width:
                            columns+=self.style.characters.walls.right.render(use_color=self.render_color,override=self.style.color.overflow)
                        else:
                            columns+=self.style.characters.walls.right.render(use_color=self.render_color)
                    if data_len < self.column_count:
                        wall_color=flextable.bg.LIGHT_BLUE
                        for c in range(data_len,self.column_count):
                            columns+=self.style.color.comment.render('',use_color=self.render_color,length=self.column_character_width)
                            columns+=self.style.characters.walls.right.render(use_color=self.render_color,override=self.style.color.error)
                elif self.data_type.COMMENT ==  line['type'] or self.data_type.WHITESPACE==line['type']:
                    left  =self.style.characters.walls.left.render(use_color=self.render_color)
                    center=self.style.color.comment.render(line['raw'],use_color=self.render_color,length=self.total_width)
                    right =self.style.characters.walls.right.render(use_color=self.render_color)
                    columns=u"{0}{1}{2}".format( left,
                                                center,
                                                right)
                elif self.data_type.ERROR ==  line['type']:
                    left  =self.style.characters.walls.left.render(use_color=self.render_color)
                    center=self.style.color.error.render(line['raw'],use_color=self.render_color,length=self.total_width)
                    right =self.style.characters.walls.right.render(use_color=self.render_color)
                    columns=u"{0}{1}{2}".format( left,
                                                center,
                                                right)
                if self.render_color==True:
                    columns+='{0}'.format(flextable.reset.ALL)
                rows.append(columns)
                index+=1
        else:
            raise Exception ("data is invalid: ->".format(buffer))
        return rows
    def build_row_seperator(self,header=None):
        index=0
        if header:
            char=self.style.characters.rst.header.text
        else:
            char=self.style.characters.rst.row.text
        row=self.style.characters.rst.edge.render()
        for i in range(0,self.column_count):
            row+=self.style.characters.rst.row.render('',fill_character=char,use_color=self.render_color,length=self.column_character_width)
            row+=self.style.characters.rst.edge.render()
        if self.render_color==True:
            row+='{0}'.format(flextable.reset.ALL)
        return row
    def output(self,text,encode):
        if isinstance(self.output_destination,list):
            if encode:
                self.output_destination.append(text.encode('utf-8'))
            else:
                self.output_destination.append(text)
        else:
            if encode:
                print(text.encode('utf-8'))
            else:
                print (text)
    def print_errors(self,table):
        for e in table.errors:
            print(e.encode('utf-8'))
    def format(self):
        self.calculate_limits()
        header=self.build_header()
        mid_header=self.build_header(mid=True)
        footer=self.build_header(footer=True)
        rows=self.build_rows(self.data)
        row_seperator=self.build_row_seperator()
        row_header_seperator=self.build_row_seperator(header=True)
        index=1
        try:
            if sys.version_info.major>2:
                encode=False
            else:
                encode=True
        except:
            encode=False
            pass
        self.output('',encode)
        if self.header==True:
            if self.display_style=='rst':
                self.output(row_seperator,encode)
            self.output(header,encode)
            if self.display_style=='rst':
                self.output(row_header_seperator,encode)
        for row in rows:
            self.output(row,encode)
            if self.display_style=='rst':
                self.output(row_seperator,encode)
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

        
# ############################################################################
# Module : ddb-slack
# File   : ./source/slack/ddb-slack-bot.py
# ############################################################################

class ddb_bot:
  EXCEPTIONS={}
  EXCEPTIONS['NO_BOT_TOKEN']='No Slack Bot Token'
  EXCEPTIONS['CONNECTION_FAILED']='Connection to slack failed'
  RTM_READ_DELAY=.03 
  RTM_FAIL_TIMEOUT=1
  RTM_MAX_FAILS=10
  def __init__(self):
    try:
      SLACK_BOT_TOKEN= os.environ["SLACK_BOT_TOKEN"]
    except:
      raise Exception(ddb_bot.EXCEPTIONS['NO_BOT_TOKEN'])
    try:
      self.DDB_CONFIG=os.environ["DDB_CONFIG"]
    except:
      self.DDB_CONFIG=None
      pass
    SLACK_PROXIES=None
    try:
      SLACK_HTTP_PROXY=os.environ["SLACK_HTTP_PROXY"]
      SLACK_HTTPS_PROXY=os.environ["SLACK_HTTPS_PROXY"]
      SLACK_PROXIES={'http':SLACK_HTTP_PROXY,'https':SLACK_HTTPS_PROXY}
    except:
      pass
    self.slack_client= SlackClient(SLACK_BOT_TOKEN,proxies=SLACK_PROXIES)
  def is_direct_message(self,msg):
    if 'channel' in msg:
      if msg['channel']:
        if msg['channel'][0]=='D':
          return True
    return None
  def is_mesage_to(self,msg):
    if 'text' in msg:
      if msg['text']!=None:
        if msg['text'].find("<@{0}>".format(self.bot_id))>-1:
          return True
    return None
  def return_my_message(self,msg):
      if 'text' in msg:
        msg=msg['text']
        pre,post=msg.split("<@{0}>".format(self.bot_id))
        return post
      return None
  def ddb_query(self,msg):
    print("Preforming query:{0}".format(msg))
    e=engine(config_file=self.DDB_CONFIG)
    query=self.return_my_message(msg)
    try:
      results=e.query(query)
      o=output_factory(results,output=e.system['OUTPUT_MODULE'],output_style=e.system['OUTPUT_STYLE'],output_file=None,output_stream="STRING",color=None)
      res=o.output
      if None == res:
        res=['No Output']
    except Exception as ex:
      res=[ex.message]
      pass
    output_text="```\r\n"+"\r\n".join(res)+"\r\n```"
    print (msg)
    self.slack_client.api_call(
      "chat.postMessage",
      channel=msg['channel'],
      text=output_text,
      thread_ts=msg['ts'],
      reply_broadcast=True
    )
  def go(self):
    fails=0
    while True:
      if self.slack_client.rtm_connect(with_team_state=False):
        fails=0
        self.bot_id = self.slack_client.api_call("auth.test")["user_id"]
        logging.log(20,"ddb-bot-id: {0}".format(self.bot_id))
        while True:
          rtm_res=self.slack_client.rtm_read()
          for msg in rtm_res:
            if 'type' in msg:
              if self.is_mesage_to(msg):
                self.ddb_query(msg)
              elif self.is_direct_message(msg):
                self.ddb_query(msg)
          time.sleep(ddb_bot.RTM_READ_DELAY)
      else:
         time.sleep(ddb_bot.RTM_FAIL_TIMEOUT)
         fails+=1
         if fails>=ddb_bot.RTM_MAX_FAILS:
            raise Exception(ddb_bot.EXCEPTIONS['CONNECTION_FAILED'])

if __name__ == "__main__":
  d=ddb_bot()
  d.go()
    