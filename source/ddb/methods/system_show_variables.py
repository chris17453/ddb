from .record_core import query_results

def method_system_show_variables(context, query_object):
    context.info("show variables")
    try:
        variable=query_object['meta']['variable']
        value=query_object['meta']['value']
        if variable in context.system:
            context.system[variable]=value
        else:
            raise Exception("Cannot set {0}, not a system variable".format(variable))
        return query_results(success=True)
    except Exception as ex:
        return query_results(success=False,error=ex)
