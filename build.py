def build_standalone():
    build=[]
    headers=[]
    files=[
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
        
    with  open('ansible/ddb.py',"w") as target:
        #for item in headers:
        #    target.write(item+"\n")
        target.write("""# ############################################################################
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


""")


        for item in build:
            target.write(item)

build_standalone()