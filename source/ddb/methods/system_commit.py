from .record_core import query_results

def method_system_commit(context, query_object):
    context.info("set")
    try:
        if context.internal['IN_TRANSACTION']==1:
            # TODO COMIT
            context.internal['IN_TRANSACTION']=0
        else:
            raise Exception("Cannot commit, not in a transaction")
        return query_results(success=True)
    except Exception as ex:
        return query_results(success=False,error=ex)
