# NOcython: linetrace=True

from .record_core import query_results

def method_show_errors(context, query_object):
    context.info("Use")
    try:
        return query_results(success=True)
    except Exception as ex:
        return query_results(success=False,error=ex)



