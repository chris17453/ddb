from .record_core import query_results

def method_system_set(context, query_object):
    context.info("set")
    try:
        #print query_object
        for item in query_object['meta']['set']:
            variable=item['variable']
            value=item['value']
            if variable in context.system:
                context.system[variable]=value
            else:
                raise Exception("Cannot set {0}, not a system variable".format(variable))
        return query_results(success=True)
    except Exception as ex:
        print(ex)
        return query_results(success=False,error=ex)
