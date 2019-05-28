# cython: linetrace=True

from .record_core import query_results

def method_system_show_output_modules(context,query_object):
    try:
        temp_table = context.database.temp_table(columns=['output_module', 'output_style'])
        for t in context.internal['OUTPUT_MODULES']:
            styles=""
            if len(t['styles'])>0:
                styles=", ".join(t['styles'])
            columns = [t['name'], styles]
            temp_table.append_data({'data': columns, 'type': context.data_type.DATA, 'error': None})
       
        return query_results(success=True,data=temp_table)
    except Exception as ex:
        return query_results(success=False,error=ex)
