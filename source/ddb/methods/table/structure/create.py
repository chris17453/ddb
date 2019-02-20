def method_create_table(context, query_object):
    context.info("Create Table")
    temp_table = context.database.temp_table()

    columns = []
    if 'columns' not in  query_object['meta'] :
        raise Exception ("Missing columns, cannot create table")

    for c in query_object['meta']['columns']:
        columns.append(c['column'])
    context.info("Columns to create", columns)
    created = 0
    found_delimiter=None
    found_comments=None
    found_whitespace=None
    found_data_on=None
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

    results = context.database.create_table(table_name=query_object['meta']['create']['table'],
                                            columns=columns,
                                            data_file=query_object['meta']['file']['file'],
                                            delimiter=found_delimiter,
                                            comments=found_comments,
                                            errors=found_errors,
                                            whitespace=found_whitespace,
                                            data_on=found_data_on
                                            )
    if True == results:
        created += 1

    temp_table.add_column('create table')
    data = {'data': [created], 'type': context.data_type.DATA, 'error': None}
    temp_table.append_data(data)
    return temp_table
