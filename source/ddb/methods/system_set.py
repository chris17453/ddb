from .record_core import query_results

def method_system_set(context, query_object):
    context.info("set")
    try:
        #print query_object
        for item in query_object['meta']['set']:
            
            variable=item['variable'].upper()
            value=item['value']
            value_up=value.upper()
            
            if len(variable)>0 and variable[0]=='@':
                var_type='user'
            else:
                var_type='system'

            if value_up in ['FALSE','NO',"OFF"]:
                value=False
            elif value_up in ['TRUE','YES',"ON"]:
                value=True

            elif value_up in ['NULL','NILL','NONE']:
                value=None

            if var_type=='system':
                if variable in context.system:
                    context.system[variable]=value
                    # if it has an auto trigger, lets call it...
                    if variable in context.system_trigger:
                        context.system_trigger[context.system_trigger]()
                else:
                    print ("EH")
                    raise Exception("Cannot set {0}, not a system variable".format(variable))
            elif var_type=='user':
                context.user[variable]=value

        return query_results(success=True)
    except Exception as ex:
        #print(ex)
        return query_results(success=False,error=ex)
