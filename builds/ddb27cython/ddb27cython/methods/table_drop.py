import sys
from .record_core import query_results, get_table

def method_drop_table(context, meta):
    table=get_table(context,meta)
    if table==None:
        raise Exception("Table not found")
    
    results = context.database.drop_table(table_name=table.data.name,database_name=table.data.database)
    # TODO Error Handeling
    return query_results(success=results)
