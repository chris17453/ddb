# cython: linetrace=True

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
    except Exception as ex:
        context.info (meta.mode,ex)
        return query_results(success=False,error=ex)
