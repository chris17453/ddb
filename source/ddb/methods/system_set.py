from .record_core import query_results

def method_system_set(context, query_object):
    context.info("set")
    try:
        #print query_object
        for item in query_object['meta']['set']:
            var_type=query_object['meta']['set']['type']
            variable=item['variable'].upper()
            value=item['value']
            value_up=value.upper()
            null_array=['NULL','NILL','NONE']
            false_array=['FALSE','NO']
            true_array=['TRUE','YES']
            if value_up in false_array:
                value=False
            elif value_up in true_array:
                value=True

            elif value_up in null_array:
                value=None

            if var_type=='system':
                if variable in context.system:
                    context.system[variable]=value
                else:
                    raise Exception("Cannot set {0}, not a system variable".format(variable))
            elif var_type=='user':
                context.user[variable]=value

        return query_results(success=True)
    except Exception as ex:
        print(ex)
        return query_results(success=False,error=ex)
