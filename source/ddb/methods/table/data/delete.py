
def method_delete(context, query_object):
    table_name = query_object['meta']['from']['table']
    query_object['table'] = context.database.get(table_name)
    if None == query_object['table']:
        raise Exception("Table '{0}' does not exist.".format(table_name))


    temp_table = context.database.temp_table()
    temp_table.add_column('deleted')

    temp_file_name = "DEL" + next(tempfile._get_candidate_names())
    line_number = 1
    deleted = 0
    # process file
    with open(query_object['table'].data.path, 'r') as content_file:
        with open(temp_file_name, 'w') as temp_file:
            for line in content_file:
                processed_line = context.process_line(query_object, line, line_number)
                if None != processed_line['error']:
                    temp_table.add_error(processed_line['error'])
                line_number += 1
                # skip matches
                if True == processed_line['match']:
                    deleted += 1
                    continue
                temp_file.write(processed_line['raw'])
                temp_file.write(query_object['table'].delimiters.get_new_line())

    data = {'data': [deleted], 'type': context.data_type.DATA, 'error': None}
    temp_table.append_data(data)
    context.swap_files(query_object['table'].data.path, temp_file_name)
    return temp_table
