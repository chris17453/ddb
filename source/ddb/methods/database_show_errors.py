# NOcython: linetrace=True

from .record_core import query_results

def method_show_errors(context, meta):
    context.info("Use")
    try:
        return query_results(success=True)
    except Exception as ex:
        context.error (meta.__class__.__name__,ex)
        return query_results(success=False,error=ex)



