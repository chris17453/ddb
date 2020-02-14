# NOcython: linetrace=True

from .record_core import query_results

def method_show_errors(context, meta):
    context.info("Use")
    try:
        return query_results(success=True)
    except Exception, ex:
        context.error (__name__,ex)
        return query_results(success=False,error=str(ex))   
        


