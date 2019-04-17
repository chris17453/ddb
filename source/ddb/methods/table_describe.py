from .record_core import query_results

def method_describe_table(context, query_object):
    """Populates metadata related to a table
    returns: table"""
    context.info("Describe Table")
    try:
        print query_object
        temp_table = context.database.temp_table()
        if 'database' in query_object['meta']['describe table']:
            context.info('Database specified')
            database_name = query_object['meta']['describe table']['database']
        else:
            context.info('Using curent database context')
            database_name = context.database.get_curent_database()

        table_name=query_object['meta']['describe table']['table']
        target_table= context.database.get(table_name,database_name=database_name)
        if None ==target_table:
            raise Exception("Table not found")
        temp_table.add_column('option')
        temp_table.add_column('value')
        
        
        temp_table.append_data({'data':['active',target_table.active], 'type': context.data_type.DATA, 'error': None})
        temp_table.append_data({'data':['table_name',target_table.data.name], 'type': context.data_type.DATA, 'error': None})
        temp_table.append_data({'data':['database',target_table.data.database], 'type': context.data_type.DATA, 'error': None})
        temp_table.append_data({'data':['data_file',target_table.data.path], 'type': context.data_type.DATA, 'error': None})
        temp_table.append_data({'data':['type',target_table.data.type], 'type': context.data_type.DATA, 'error': None})
        temp_table.append_data({'data':['config_file',target_table.data.config], 'type': context.data_type.DATA, 'error': None})
        temp_table.append_data({'data':['data_starts_on',target_table.data.starts_on_line], 'type': context.data_type.DATA, 'error': None})
        temp_table.append_data({'data':['field_delimiter'  ,target_table.delimiters.field], 'type': context.data_type.DATA, 'error': None})
        temp_table.append_data({'data':['comments_visible',target_table.visible.comments], 'type': context.data_type.DATA, 'error': None})
        temp_table.append_data({'data':['errors_visible',target_table.visible.errors], 'type': context.data_type.DATA, 'error': None})
        temp_table.append_data({'data':['whitespace_visible',target_table.visible.whitespace], 'type': context.data_type.DATA, 'error': None})
        return query_results(success=True,data=temp_table)
    except Exception as ex:
        #print ex
        return query_results(success=False,error=ex)



