

def src_build():
    core_files=[
        # base class
        {'name':'version','file':'ddb/engine/version.pyx'},
        {'name':'language','file':'ddb/engine/parser/language.pyx'},
        {'name':'parser','file':'ddb/engine/parser/sql_parser.pyx'},
        {'name':'tokenize','file':'ddb/engine/tokenizer/sql_tokenize.pyx'},
        {'name':'column','file':'ddb/engine/structure/column.pyx'},
        {'name':'table','file':'ddb/engine/structure/table.pyx'},
        {'name':'database','file':'ddb/engine/structure/database.pyx'},
        {'name':'match','file':'ddb/engine/evaluate/match.pyx'},
        {'name':'functions','file':'ddb/engine/functions/functions.pyx'},
        {'name':'sql_engine','file':'ddb/engine/sql_engine.pyx'},
        # formatting
        #{'name':'output','file':'ddb/engine/output/output.pyx'},
        # cli stuff
        #{'name':'interactive','file':'ddb/engine/interactive.pyx'},
        #{'name':'cli','file':'ddb/cli.py'},
    ]
    standalone_files=[
        # base class
        {'name':'version','file':'ddb/engine/version.pyx'},
        {'name':'language','file':'ddb/engine/parser/language.pyx'},
        {'name':'parser','file':'ddb/engine/parser/sql_parser.pyx'},
        {'name':'tokenize','file':'ddb/engine/tokenizer/sql_tokenize.pyx'},
        {'name':'column','file':'ddb/engine/structure/column.pyx'},
        {'name':'table','file':'ddb/engine/structure/table.pyx'},
        {'name':'database','file':'ddb/engine/structure/database.pyx'},
        {'name':'match','file':'ddb/engine/evaluate/match.pyx'},
        {'name':'functions','file':'ddb/engine/functions/functions.pyx'},
        {'name':'sql_engine','file':'ddb/engine/sql_engine.pyx'},
        # formatting
        {'name':'output','file':'ddb/engine/output/output.pyx'},
        # cli stuff
        {'name':'interactive','file':'ddb/engine/interactive.pyx'},
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
import lazyxml
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