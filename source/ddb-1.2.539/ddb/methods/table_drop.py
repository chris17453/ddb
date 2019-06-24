# cython: linetrace=True

from .record_core import query_results

def method_drop_table(context, query_object):
    context.info("Drop Table")
    try:
        table_name=query_object['meta']['source']['table']
        if 'database' in query_object['meta']['source']:
            context.info('Database specified')
            database_name = query_object['meta']['source']['database']
        else:
            context.info('Using curent database context')
            database_name = context.database.get_curent_database()

        results = context.database.drop_table(table_name=table_name,database_name=database_name)
        return query_results(success=results)
    except Exception as ex:
        return query_results(success=False,error=ex)
