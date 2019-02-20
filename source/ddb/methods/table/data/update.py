def update_single(context, query_object, temp_file, temp_table, requires_new_line, processed_line):
    err = False
    ###
    # insert new data at end of file
    new_line = ''
    err = False
    #print query_object

    # make sure the inserted columns exist
    for c2 in range(0, len(query_object['meta']['set'])):
        column_name = query_object['meta']['set'][c2]['column']
        if None == query_object['table'].get_column_by_name(column_name):
            temp_table.add_error("column in update statement does not exist in table: {}".format(column_name))
            #print "no column"
            err = True

    if False == err:
        for c in range(0, query_object['table'].column_count()):
            column_name = query_object['table'].get_column_at_data_ordinal(c)
            value = processed_line['data'][c]
            for c2 in range(0, len(query_object['meta']['set'])):
                #print column_name,query_object['meta']['set']
                if query_object['meta']['set'][c2]['column'] == column_name:
                    #print("Column {} at table index {} located at query index {}".format(column_name,c, c2))
                    value = query_object['meta']['set'][c2]['expression']
            if c > 0:
                new_line += '{}'.format(query_object['table'].delimiters.field)
            new_line += '{}'.format(value)

    if False == err:
        #print new_line
        if True == requires_new_line:
            temp_file.write(query_object['table'].delimiters.get_new_line())
        temp_file.write(new_line)
        temp_file.write(query_object['table'].delimiters.get_new_line())
    if False == err:
        return True
    else:
        return False

def method_update(context, query_object):
    table_name = query_object['meta']['update']['table']
    query_object['table'] = context.database.get(table_name)
    if None == query_object['table']:
        raise Exception("Table '{0}' does not exist.".format(table_name))


    temp_table = context.database.temp_table()
    temp_table.add_column('updated')

    temp_file_name = "UP_" + next(tempfile._get_candidate_names())
    line_number = 1
    updated = 0
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
                    results = context.update_single(query_object, temp_file, temp_table, False, processed_line)
                    if True == results:
                        updated += 1
                    continue
                temp_file.write(processed_line['raw'])
                temp_file.write(query_object['table'].delimiters.get_new_line())
    data = {'data': [updated], 'type': context.data_type.DATA, 'error': None}

    temp_table.append_data(data)
    context.swap_files(query_object['table'].data.path, temp_file_name)

    return temp_table

