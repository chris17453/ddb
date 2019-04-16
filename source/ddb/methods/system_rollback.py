from .record_core import query_results

def method_system_rollback(context, query_object):
    context.info("set")
    try:
        if context.internal['IN_TRANSACTION']==1:
            # TODO ROLLBACK
            context.internal['IN_TRANSACTION']=0
            context.system['AUTOCOMMIT']=context.internal['AUTOCOMMIT_HOLODER']=True
        else:
            raise Exception("Cannot rollback, not in a transaction")
        return query_results(success=True)
    except Exception as ex:
        return query_results(success=False,error=ex)
