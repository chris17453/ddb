import sys
from .record_core import query_results, get_table

def method_use(context, meta):
    context.info("Use")
    try:
        target_db=meta.database

        temp_table = context.database.temp_table()
        temp_table.add_column('changed_db')
        data = {'data': [target_db], 'type': context.data_type.DATA, 'error': None}
        temp_table.append_data(data)
        # TODO so.. is this how we want to handle actions not preformed?
        return query_results(success=True,data=temp_table)
    except:
        err = sys.exc_info()[1]
        ex = err.args[0]
        context.error (__name__,ex)
        return query_results(success=False,error=str(ex))   
        