from .record_core import query_results

def method_system_show_columns(context,database, query_object):
    try:
        if 'database' in query_object['meta']['from']:
            context.info('Database specified')
            database_name = query_object['meta']['from']['database']
        else:
            context.info('Using curent database context')
            database_name = context.database.get_curent_database()
        table = database.get(query_object['meta']['from']['table'],database_name=database_name)
        
        temp_table = database.temp_table(columns=['database','table', 'column'])

        for c in table.columns:
            columns = {'data': [table.data.database,table.data.name, c.data.name], 'type': context.data_type.DATA, 'error': None}
            temp_table.append_data(columns)
        
        return query_results(success=True,data=temp_table)
    except Exception as ex:
        print ex
        return query_results(success=False,error=ex)

