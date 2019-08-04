# cython: linetrace=True

from .record_core import query_results, get_table

def method_drop_table(context, meta):
    context.info("Drop Table")
    try:
        table=get_table(context,meta)
        
        results = context.database.drop_table(table_name=table.data.name,database_name=table.data.database)
        # TODO Error Handeling
        return query_results(success=results)
    except Exception as ex:
        print ex
        return query_results(success=False,error=ex)
