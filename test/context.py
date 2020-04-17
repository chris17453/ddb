import os
import sys
from pprint import pprint

# Default mode is cython
standalone_script=None

# to run test with single file script
#    export ddb_exe=script


pprint(os.environ,indent=4)
print ("TESTING")
if 'DDB_RELEASE_DIR' in os.environ:
    print ("Found test dir")
    standalone_script=os.environ['DDB_RELEASE_DIR']


if standalone_script!=None:
    sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__),standalone_script)))

    try:
        from ddb import ddb
    except Exception as ex:
        print (ex)
        exit(1)
    print ("DDB STANDALONE")
else:
    sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

    try:
        from source import ddb
    except Exception as ex:
        print (ex)
        exit(1)
    print ("DDB CYTHON")
