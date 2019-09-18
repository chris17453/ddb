import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..','builds')))

try:
    from standalone import ddb
except Exception as ex:
    print ex
    exit(1)
print ("DDB STANDALONE")
