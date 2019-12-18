# cython: linetrace=True

from .record_core import query_results

def method_system_set(context, meta):
    context.info("set")
    try:
        # meta.debug()
        for item in meta.set:
            
            variable=item.variable.upper()
            value=item.value
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
                        context.system_trigger[variable]()
                else:
                    raise Exception("Cannot set {0}, not a system variable".format(variable))
            elif var_type=='user':
                context.user[variable]=value

        return query_results(success=True)
    except Exception as ex:
        context.error (meta.__class__.__name__,ex)
        return query_results(success=False,error=ex)
