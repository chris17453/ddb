import sys

def src_build():
    source_dir='./source'
    core_files=[
        # base class
        {'name':'version','file':source_dir+'/ddb/version.py'},
        {'name':'lexer-language','file':source_dir+'/ddb/lexer/language.py'},
        {'name':'lexer-parse','file':source_dir+'/ddb/lexer/lexer.py'},
        {'name':'lexer-token','file':source_dir+'/ddb/lexer/tokenize.py'},
        {'name':'meta','file':source_dir+'/ddb/meta/meta.py'},
        {'name':'column','file':source_dir+'/ddb/configuration/column.py'},
        {'name':'table','file':source_dir+'/ddb/configuration/table.py'},
        {'name':'database','file':source_dir+'/ddb/configuration/database.py'},
        {'name':'functions','file':source_dir+'/ddb/functions/functions.py'},
        {'name':'methods-record','file':source_dir+'/ddb/methods/record.py'},
        {'name':'sql_engine','file':source_dir+'/ddb/engine.py'},
        {'name':'methods-records_core','file':source_dir+'/ddb/methods/record_core.py'},
        {'name':'methods-records-delete','file':source_dir+'/ddb/methods/record_delete.py'},
        {'name':'methods-records-insert','file':source_dir+'/ddb/methods/record_insert.py'},
        {'name':'methods-records-select','file':source_dir+'/ddb/methods/record_select.py'},
        {'name':'methods-records-update','file':source_dir+'/ddb/methods/record_update.py'},
        {'name':'methods-records-upsert','file':source_dir+'/ddb/methods/record_upsert.py'},
        {'name':'methods-database-use','file':source_dir+'/ddb/methods/database_use.py'},
        {'name':'methods-table-structure-create','file':source_dir+'/ddb/methods/table_create.py'},
        {'name':'methods-table-structure-describe','file':source_dir+'/ddb/methods/table_describe.py'},
        {'name':'methods-table-structure-drop','file':source_dir+'/ddb/methods/table_drop.py'},
        {'name':'methods-table-structure-update','file':source_dir+'/ddb/methods/table_update.py'},
        {'name':'methods-system-set','file':source_dir+'/ddb/methods/system_set.py'},
        {'name':'methods-system-begin','file':source_dir+'/ddb/methods/system_begin.py'},
        {'name':'methods-system-commit','file':source_dir+'/ddb/methods/system_commit.py'},
        {'name':'methods-system-rollback','file':source_dir+'/ddb/methods/system_rollback.py'},
        {'name':'methods-system-show-columns','file':source_dir+'/ddb/methods/system_show_columns.py'},
        {'name':'methods-system-show-tables','file':source_dir+'/ddb/methods/system_show_tables.py'},
        {'name':'methods-system-show-variables','file':source_dir+'/ddb/methods/system_show_variables.py'},
        {'name':'methods-system-show-output-modules','file':source_dir+'/ddb/methods/system_show_output_modules.py'},
        {'name':'file_io-lock','file':source_dir+'/ddb/file_io/locking.py'},
        # formatting
        {'name':'output','file':source_dir+'/ddb/output/factory.py'},
        {'name':'factory_term','file':source_dir+'/ddb/output/factory_term.py'},
        {'name':'factory_yaml','file':source_dir+'/ddb/output/factory_yaml.py'},
        {'name':'factory_xml','file':source_dir+'/ddb/output/factory_xml.py'},
        {'name':'factory_json','file':source_dir+'/ddb/output/factory_json.py'},

        # cli stuff
        #{'name':'interactive','file':source_dir+'/ddb/interactive.py'},
        #{'name':'cli','file':source_dir+'/ddb/cli.py'},
    ]
    standalone_files=core_files+[
        # cli stuff
        {'name':'interactive','file':source_dir+'/ddb/interactive.py'},
        {'name':'cli','file':source_dir+'/ddb/cli.py'},
    ]    


    ansible_files=[{'name':'ddb-ansible-module','file':source_dir+'/ansible/ddb-ansible.py'}]+core_files
    slack_files=core_files+[{'name':'ddb-slack','file':source_dir+'/slack/ddb-slack-bot.py'}]

    core_headers="""# -*- coding: utf-8 -*-
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
import signal
import os
import stat
import fileinput
import warnings
import datetime
import base64
import tempfile
import shutil
import time
import pprint
import logging
import socket
from subprocess import Popen,PIPE
import random
import traceback
import copy
import base64
try:
    from collections import OrderedDict
except:
    try:
        from ordereddict import OrderedDict
    except:
        pass


sys.dont_write_bytecode = True




"""
    standalone_headers="""# -*- coding: utf-8 -*-
# ############################################################################
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
import signal
import os
import stat
import fileinput
import warnings
import datetime
import base64
import tempfile
import shutil
import time
import pprint
import logging
import socket
from subprocess import Popen,PIPE
import random
import traceback
import copy
import base64
try:
    from collections import OrderedDict
except:
    try:
        from ordereddict import OrderedDict
    except:
        pass


sys.dont_write_bytecode = True


from cmd import Cmd
import argparse
from os.path import expanduser



"""

    ansible_headers="""#!/usr/bin/python
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
import signal
import os
import stat
import fileinput
import warnings
import datetime
import base64
import tempfile
import shutil
import time
import pprint
import logging
import socket
from subprocess import Popen,PIPE
import random
import traceback
import base64
try:
    from collections import OrderedDict
except:
    try:
        from ordereddict import OrderedDict
    except:
        pass

sys.dont_write_bytecode = True


from ansible.module_utils.basic import AnsibleModule


"""

    ansible_tail="""

def main():
    run_module()

if __name__ == '__main__':
    main()
"""

    slack_headers="""#!/usr/bin/python
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
import signal
import os
import stat
import fileinput
import warnings
import datetime
import base64
import tempfile
import shutil
import time
import pprint
import logging
import socket
from subprocess import Popen,PIPE
import random
import traceback
import base64
try:
    from collections import OrderedDict
except:
    try:
        from ordereddict import OrderedDict
    except:
        pass

sys.dont_write_bytecode = True


from slackclient import SlackClient

import logging
logging.basicConfig()

"""
    slack_tail="""
if __name__ == "__main__":
  d=ddb_bot()
  d.go()
    """
    build_standalone(core_files,core_headers,None,'builds/standalone/ddb-core.py')
    build_standalone(standalone_files,standalone_headers,None,'builds/standalone/ddb.py')
    build_standalone(ansible_files,ansible_headers,ansible_tail,'builds/ansible/ddb-ansible.py')
    build_standalone(slack_files,slack_headers,slack_tail,'builds/slack/ddb-slack-bot.py')


def build_standalone(files,headers,footer,dest_file):
    build=[]
    for item in files:
        seperator='''
        
# ############################################################################
# Module : %(name)s
# File   : %(file)s
# ############################################################################

''' % item
    
        build.append(seperator)
        try:
            #print(sys.version_info)
            content=open(item['file'],mode='rt') #,encoding="utf-8"
        
            for line in content:
                line=line
                part=line[0:4]
                l=line.strip()
                if len(l) >0 and l[0]=='#':
                    continue
                if line.isspace():
                    continue

                if part=='impo' or part=='from':
                    l=line.strip()
                    if l in headers:
                        continue
                    #headers.append(l)
                    continue
                build.append(line)
            content.close()
        except:
            print(sys.exc_info()[1])
            pass
    print ("Writing: %(file)s" % {'file':dest_file} )
    try:
        target=open(dest_file,mode="wt") # ,encoding="utf-8"
        if headers:
            target.write(headers)

        for item in build:
            target.write(item)
        
        if footer:
            target.write(footer)
        target.close()
    except:
        pass

src_build()