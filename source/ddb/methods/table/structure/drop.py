
def method_drop_table(context, query_object):
    context.info("Drop Table")
    temp_table = context.database.temp_table()
    #print "dropping",parser.query_object['meta']['drop']['table']
    dropped = 0
    results = context.database.drop_table(table_name=query_object['meta']['drop']['table'])
    if True == results:
        dropped += 1

    temp_table.add_column('dropped')
    data = {'data': [dropped], 'type': context.data_type.DATA, 'error': None}
    temp_table.append_data(data)
    return temp_table
