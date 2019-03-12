from .record_core import query_results

def method_system_begin(context, query_object):
    context.info("set")
    try:
        return query_results(success=True)
    except Exception as ex:
        return query_results(success=False,error=ex)
