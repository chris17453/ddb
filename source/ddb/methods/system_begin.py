# cython: linetrace=True
import sys
from .record_core import query_results

def method_system_begin(context,meta):
    context.info("begin")
    try:
        if context.internal['IN_TRANSACTION']==1:
            raise Exception("Already in a Batch Transaction")
        else:
            context.internal['AUTOCOMMIT_HOLODER']=context.system['AUTOCOMMIT']
            context.system['AUTOCOMMIT']=False
            context.internal['IN_TRANSACTION']=1
        return query_results(success=True)
    except:
        err = sys.exc_info()[1]
        ex = err.args[0]
        context.error (__name__,ex)
        return query_results(success=False,error=str(ex))   
