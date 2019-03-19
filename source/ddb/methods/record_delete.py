from .record_core import process_line, swap_files, query_results,create_temporary_copy


def method_delete(context, query_object):
    try:
        table_name = query_object['meta']['from']['table']
        query_object['table'] = context.database.get(table_name)
        if None == query_object['table']:
            raise Exception("Table '{0}' does not exist.".format(table_name))


        line_number = 1
        affected_rows = 0
        temp_file_prefix = "DELETE" 
        data_file=query_object['table'].data.path
        temp_data_file=create_temporary_copy(data_file,temp_file_prefix)
        print ("Writing..")

        with open(temp_data_file, 'r') as content_file:
            print("opened file")
            temp_file=tempfile.NamedTemporaryFile(mode='w', prefix=temp_file_prefix,delete=True) 
            print (temp_file)
            print("opened other file")
            for line in content_file:
                processed_line = process_line(context,query_object, line, line_number)
                if None != processed_line['error']:
                    context.add_error(processed_line['error'])
                line_number += 1
                # skip matches
                if True == processed_line['match']:
                    affected_rows += 1
                    continue
                print ("Writing TO FILE")
                temp_file.write(processed_line['raw'])
                temp_file.write(query_object['table'].delimiters.get_new_line())
            swap_files(data_file, temp_file.name)
        return  query_results(success=True,affected_rows=affected_rows)
    except Exception as ex:
        print(ex)
        return  query_results(success=False, error=ex)


