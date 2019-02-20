

def src_build():
    source_dir='./source'
    core_files=[
        # base class
        {'name':'version','file':source_dir+'/ddb/version.py'},
        {'name':'lexer-language','file':source_dir+'/ddb/lexer/language.py'},
        {'name':'lexer-parse','file':source_dir+'/ddb/lexer/lexer.py'},
        {'name':'lexer-token','file':source_dir+'/ddb/lexer/tokenize.py'},
        {'name':'column','file':source_dir+'/ddb/structure/column.py'},
        {'name':'table','file':source_dir+'/ddb/structure/table.py'},
        {'name':'database','file':source_dir+'/ddb/structure/database.py'},
        {'name':'match','file':source_dir+'/ddb/evaluate/match.py'},
        {'name':'functions','file':source_dir+'/ddb/functions/functions.py'},
        {'name':'sql_engine','file':source_dir+'/ddb/engine.py'},
        {'name':'methods-database-set','file':source_dir+'/ddb/methods/database/set.py'},
        {'name':'methods-database-use','file':source_dir+'/ddb/methods/database/use.py'},
        {'name':'methods-table-data-delete','file':source_dir+'/ddb/methods/table/data/delete.py'},
        {'name':'methods-table-data-insert','file':source_dir+'/ddb/methods/table/data/insert.py'},
        {'name':'methods-table-data-select','file':source_dir+'/ddb/methods/table/data/select.py'},
        {'name':'methods-table-data-show-columns','file':source_dir+'/ddb/methods/table/data/show_columns.py'},
        {'name':'methods-table-data-show-tables','file':source_dir+'/ddb/methods/table/data/show_tables.py'},
        {'name':'methods-table-data-update','file':source_dir+'/ddb/methods/table/data/update.py'},
        {'name':'methods-table-structure-create','file':source_dir+'/ddb/methods/table/structure/create.py'},
        {'name':'methods-table-structure-describe','file':source_dir+'/ddb/methods/table/structure/describe.py'},
        {'name':'methods-table-structure-drop','file':source_dir+'/ddb/methods/table/structure/drop.py'},
        {'name':'methods-table-structure-update','file':source_dir+'/ddb/methods/table/structure/update.py'},
        # formatting
        {'name':'output','file':source_dir+'/ddb/output/factory.py'},
        {'name':'factory_yaml','file':source_dir+'/ddb/output/factory_yaml.py'},
        {'name':'factory_xml','file':source_dir+'/ddb/output/factory_xml.py'},
        {'name':'factory_json','file':source_dir+'/ddb/output/factory_json.py'},
        # cli stuff
        #{'name':'interactive','file':source_dir+'/ddb/interactive.py'},
        #{'name':'cli','file':source_dir+'/ddb/cli.py'},
    ]
    standalone_files=[
        # base class
        {'name':'version','file':source_dir+'/ddb/version.py'},
        {'name':'lexer-language','file':source_dir+'/ddb/lexer/language.py'},
        {'name':'lexer-parse','file':source_dir+'/ddb/lexer/lexer.py'},
        {'name':'lexer-token','file':source_dir+'/ddb/lexer/tokenize.py'},
        {'name':'column','file':source_dir+'/ddb/structure/column.py'},
        {'name':'table','file':source_dir+'/ddb/structure/table.py'},
        {'name':'database','file':source_dir+'/ddb/structure/database.py'},
        {'name':'match','file':source_dir+'/ddb/evaluate/match.py'},
        {'name':'functions','file':source_dir+'/ddb/functions/functions.py'},
        {'name':'sql_engine','file':source_dir+'/ddb/engine.py'},
        {'name':'methods-database-set','file':source_dir+'/ddb/methods/database/set.py'},
        {'name':'methods-database-use','file':source_dir+'/ddb/methods/database/use.py'},
        {'name':'methods-table-data-delete','file':source_dir+'/ddb/methods/table/data/delete.py'},
        {'name':'methods-table-data-insert','file':source_dir+'/ddb/methods/table/data/insert.py'},
        {'name':'methods-table-data-select','file':source_dir+'/ddb/methods/table/data/select.py'},
        {'name':'methods-table-data-show-columns','file':source_dir+'/ddb/methods/table/data/show_columns.py'},
        {'name':'methods-table-data-show-tables','file':source_dir+'/ddb/methods/table/data/show_tables.py'},
        {'name':'methods-table-data-update','file':source_dir+'/ddb/methods/table/data/update.py'},
        {'name':'methods-table-structure-create','file':source_dir+'/ddb/methods/table/structure/create.py'},
        {'name':'methods-table-structure-describe','file':source_dir+'/ddb/methods/table/structure/describe.py'},
        {'name':'methods-table-structure-drop','file':source_dir+'/ddb/methods/table/structure/drop.py'},
        {'name':'methods-table-structure-update','file':source_dir+'/ddb/methods/table/structure/update.py'},
        # formatting
        {'name':'output','file':source_dir+'/ddb/output/factory.py'},
        {'name':'factory_yaml','file':source_dir+'/ddb/output/factory_yaml.py'},
        {'name':'factory_xml','file':source_dir+'/ddb/output/factory_xml.py'},
        {'name':'factory_json','file':source_dir+'/ddb/output/factory_json.py'},
        # cli stuff
        {'name':'interactive','file':source_dir+'/ddb/interactive.py'},
        {'name':'cli','file':source_dir+'/ddb/cli.py'},
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
    build_standalone(core_files,core_headers,'builds/standalone/ddb-core.py')
    build_standalone(standalone_files,standalone_headers,'builds/standalone/ddb.py')


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