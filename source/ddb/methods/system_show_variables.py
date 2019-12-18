# cython: linetrace=True

from .record_core import query_results

def method_system_show_variables(context,meta):
    context.info("show variables")
    try:
         
        temp_table = context.database.temp_table(columns=['type','name','value'])

        for c in context.system:
            columns = {'data': ['system',c,context.system[c]], 'type': context.data_type.DATA, 'error': None}
            temp_table.append_data(columns)
        for c in context.user:
            columns = {'data': ['user',c,context.user[c]], 'type': context.data_type.DATA, 'error': None}
            temp_table.append_data(columns)
        
        return query_results(success=True,data=temp_table)
    except Exception as ex:
        context.error (meta.__class__.__name__,ex)
        return query_results(success=False,error=ex)
