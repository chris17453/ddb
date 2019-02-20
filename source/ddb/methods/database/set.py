def method_set(context, query_object):
    context.info("set")
    temp_table = context.database.temp_table()
    temp_table.add_column('changed_db')
    data = {'data': [], 'type': context.data_type.DATA, 'error': None}
    temp_table.append_data(data)
    return temp_table
