# cython: linetrace=True

from .record_core import query_results, get_table

def method_system_show_columns(context, meta):
    try:
        table =get_table(context,meta)
        
        temp_table = context.database.temp_table(columns=['database','table', 'column'])
        if table:
            for c in table.columns:
                columns = {'data': [table.data.database,table.data.name, c.data.name], 'type': context.data_type.DATA, 'error': None}
                temp_table.append_data(columns)
            
        return query_results(success=True,data=temp_table)
    except Exception as ex:
        context.info (meta.mode,ex)
        return query_results(success=False,error=ex)

