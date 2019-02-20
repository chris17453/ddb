def method_use(context, query_object):
    context.info("Use")
    target_db = query_object['meta']['use']['table']
    if context.database.get_curent_database()!=target_db:
        context.database.set_database(target_db)
        temp_table = context.database.temp_table()
        temp_table.add_column('changed_db')
        data = {'data': [target_db], 'type': context.data_type.DATA, 'error': None}
        temp_table.append_data(data)
        return temp_table
    # TODO so.. is this how we want to handle actions not preformed?
    return None