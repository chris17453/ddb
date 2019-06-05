# cython: linetrace=True

from .record_core import query_results

def method_update_table(context, query_object):
    context.info("Update Table")
    try:
        columns = None  
        if 'columns'  in  query_object['meta'] :
            columns = []
            for c in query_object['meta']['columns']:
                columns.append(c['column'])

        table_name=query_object['meta']['source']['table']
        if 'database' in query_object['meta']['source']:
            context.info('Database specified')
            database_name = query_object['meta']['source']['database']
        else:
            context.info('Using curent database context')
            database_name = context.database.get_curent_database()

        found_delimiter=None
        found_comments=None
        found_whitespace=None
        found_data_on=None
        found_file=None
        found_errors=None
        
        if 'delimiter' in query_object['meta']:
            found_delimiter= query_object['meta']['delimiter']['field']
        if 'whitespace' in query_object['meta']:
            found_whitespace= query_object['meta']['whitespace']['whitespace']
        if 'comments' in query_object['meta']:
            found_comments= query_object['meta']['comments']['comments']
        if 'errors' in query_object['meta']:
            found_errors= query_object['meta']['errors']['errors']
        if 'data_starts_on' in query_object['meta']:
            found_data_on= query_object['meta']['data_starts_on']['data_starts_on']
        if 'file' in query_object['meta']:
            found_file=query_object['meta']['file']['file']

        target_table= context.database.get(table_name,database_name)
        target_table.update(columns=columns,
                            data_file=found_file,
                            field_delimiter=found_delimiter,
                            comments=found_comments,
                            whitespace=found_whitespace,
                            errors=found_errors,
                            data_on=found_data_on)
        #sace the update to the table
        results=target_table.save()
    
        return query_results(success=results)
    except Exception as ex:
        return query_object(success=False,error=ex)

