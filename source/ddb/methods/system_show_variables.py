from .record_core import query_results

def method_system_show_variables(context, query_object):
    context.info("show variables")
    try:
         
        temp_table = context.database.temp_table(columns=['name','value'])

        for c in context.system:
            columns = {'data': [c,context.system[c]], 'type': context.data_type.DATA, 'error': None}
            temp_table.append_data(columns)
        
        return query_results(success=True,data=temp_table)
    except Exception as ex:
        print (ex)
        return query_results(success=False,error=ex)
