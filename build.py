

def src_build():
    core_files=[
        # base class
        {'name':'version','file':'ddb/engine/version.pyx'},
        {'name':'language','file':'ddb/parser/language.pyx'},
        {'name':'parser','file':'ddb/parser/sql_parser.pyx'},
        {'name':'tokenize','file':'ddb/tokenizer/sql_tokenize.pyx'},
        {'name':'column','file':'ddb/structure/column.pyx'},
        {'name':'table','file':'ddb/structure/table.pyx'},
        {'name':'database','file':'ddb/structure/database.pyx'},
        {'name':'match','file':'ddb/evaluate/match.pyx'},
        {'name':'functions','file':'ddb/functions/functions.pyx'},
        {'name':'sql_engine','file':'ddb/sql_engine.pyx'},
        # formatting
        #{'name':'output','file':'ddb/output/factory.pyx'},
        # cli stuff
        #{'name':'interactive','file':'ddb/interactive.pyx'},
        #{'name':'cli','file':'ddb/cli.py'},
    ]
    standalone_files=[
        # base class
        {'name':'version','file':'ddb//version.pyx'},
        {'name':'language','file':'ddb/parser/language.pyx'},
        {'name':'parser','file':'ddb/parser/sql_parser.pyx'},
        {'name':'tokenize','file':'ddb/tokenizer/sql_tokenize.pyx'},
        {'name':'column','file':'ddb/structure/column.pyx'},
        {'name':'table','file':'ddb/structure/table.pyx'},
        {'name':'database','file':'ddb/structure/database.pyx'},
        {'name':'match','file':'ddb/evaluate/match.pyx'},
        {'name':'functions','file':'ddb/functions/functions.pyx'},
        {'name':'sql_engine','file':'ddb/sql_engine.pyx'},
        # formatting
        {'name':'output','file':'ddb/output/factory.pyx'},
        {'name':'factory_yaml','file':'ddb/output/factory_yaml.pyx'},
        {'name':'factory_xml','file':'ddb/output/factory_xml.pyx'},
        {'name':'factory_json','file':'ddb/output/factory_json.pyx'},
        # cli stuff
        {'name':'interactive','file':'ddb/interactive.pyx'},
        {'name':'cli','file':'ddb/cli.py'},
    ]    
    core_headers="""# ############################################################################
# 
# This file is automagically generated
# dont edit it, because it will be erased next build
# 
# ############################################################################
        
import sys
import os
import json
import yaml
import warnings
import datetime
import tempfile


"""
    standalone_headers="""# ############################################################################
# 
# This file is automagically generated
# dont edit it, because it will be erased next build
# 
# ############################################################################
        
import sys
import os
import json
import yaml
import warnings
import datetime
import tempfile
import time
import flextable
from cmd import Cmd
import argparse
from os.path import expanduser



"""
    build_standalone(core_files,core_headers,'ansible/ddb.py')
    build_standalone(core_files,core_headers,'src_build/core/ddb_core.py')
    build_standalone(standalone_files,standalone_headers,'src_build/standalone/ddb_standalone.py')


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