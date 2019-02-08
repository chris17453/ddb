

def src_build():
    core_files=[
        # base class
        {'name':'version','file':'ddb/version.py'},
        {'name':'lexer-language','file':'ddb/lexer/language.py'},
        {'name':'lexer-parse','file':'ddb/lexer/lexer.py'},
        {'name':'lexer-token','file':'ddb/lexer/tokenize.py'},
        {'name':'column','file':'ddb/structure/column.py'},
        {'name':'table','file':'ddb/structure/table.py'},
        {'name':'database','file':'ddb/structure/database.py'},
        {'name':'match','file':'ddb/evaluate/match.py'},
        {'name':'functions','file':'ddb/functions/functions.py'},
        {'name':'sql_engine','file':'ddb/engine.py'},
        # formatting
        {'name':'output','file':'ddb/output/factory.py'},
        {'name':'factory_yaml','file':'ddb/output/factory_yaml.py'},
        {'name':'factory_xml','file':'ddb/output/factory_xml.py'},
        {'name':'factory_json','file':'ddb/output/factory_json.py'},
        # cli stuff
        #{'name':'interactive','file':'ddb/interactive.py'},
        #{'name':'cli','file':'ddb/cli.py'},
    ]
    standalone_files=[
        # base class
        {'name':'version','file':'ddb/version.py'},
        {'name':'lexer-language','file':'ddb/lexer/language.py'},
        {'name':'lexer-parse','file':'ddb/lexer/lexer.py'},
        {'name':'lexer-token','file':'ddb/lexer/tokenize.py'},
        {'name':'column','file':'ddb/structure/column.py'},
        {'name':'table','file':'ddb/structure/table.py'},
        {'name':'database','file':'ddb/structure/database.py'},
        {'name':'match','file':'ddb/evaluate/match.py'},
        {'name':'functions','file':'ddb/functions/functions.py'},
        {'name':'sql_engine','file':'ddb/engine.py'},
        # formatting
        {'name':'output','file':'ddb/output/factory.py'},
        {'name':'factory_yaml','file':'ddb/output/factory_yaml.py'},
        {'name':'factory_xml','file':'ddb/output/factory_xml.py'},
        {'name':'factory_json','file':'ddb/output/factory_json.py'},
        # cli stuff
        {'name':'interactive','file':'ddb/interactive.py'},
        {'name':'cli','file':'ddb/cli.py'},
    ]    
    core_headers="""# ############################################################################
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
import json
import warnings
import datetime
import tempfile
try:
    import flextable
except Exception as ex:
    pass


"""
    standalone_headers="""# ############################################################################
# 
# :########::'########::'########::
# :##.... ##: ##.... ##: ##.... ##:
# :##:::: ##: ##:::: ##: ##:::: ##:
# :##:::: ##: ##:::: ##: ########::
# :##:::: ##: ##:::: ##: ##.... ##:
# :##:::: ##: ##:::: ##: ##:::: ##:
# :########:: ########:: ########::
# :.......:::........:::........:::
# 
# Author: Charles Watkins
# This file is automagically generated
# dont edit it, because it will be erased next build
# 
# ############################################################################
        
import sys
import os
import json
import warnings
import datetime
import tempfile
import time
from cmd import Cmd
import argparse
from os.path import expanduser
try:
    import flextable
except Exception as ex:
    pass



"""
    build_standalone(core_files,core_headers,'ansible/ddb.py')
    build_standalone(core_files,core_headers,'src_build/python/core/ddb_core.py')
    build_standalone(standalone_files,standalone_headers,'src_build/python/standalone/ddb_standalone.py')


def build_standalone(files,headers,dest_file):
    build=[]
    for item in files:
        seperator='''
        
        
# ############################################################################
# Module : {0}
# File   : {1}
# ############################################################################



'''.format(item['name'],item['file'])
    
        build.append(seperator)
        with  open(item['file']) as content:
            for line in content:
                part=line[0:4]
                l=line.strip()
                if len(l) >0 and l[0]=='#':
                    continue
                if part=='impo' or part=='from':
                    l=line.strip()
                    if l in headers:
                        continue
                    #headers.append(l)
                    continue
                build.append(line)
    print dest_file
    with  open(dest_file,"w") as target:
        target.write(headers)

        for item in build:
            target.write(item)

src_build()