
def method_show_columns(context,database, query_object):
    table = database.get(query_object['meta']['from']['table'])
    temp_table = database.temp_table(columns=['table', 'column'])

    for c in table.columns:
        columns = {'data': [table.data.name, c.data.name], 'type': context.data_type.DATA, 'error': None}
        temp_table.append_data(columns)
    return temp_table
