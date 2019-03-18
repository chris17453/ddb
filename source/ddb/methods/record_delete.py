from .record_core import process_line, swap_files, query_results
import tempfile, shutil, os


def create_temporary_copy(path,prefix):
    try:
        temp_dir = tempfile.gettempdir()
        temp_base_name=next(tempfile._get_candidate_names())
        if prefix:
            temp_file_name="{0}".format(temp_base_name)
        else:
            temp_file_name="{0}_{1}".format(prefix,temp_base_name)
        
        temp_path = os.path.join(temp_dir, temp_file_name)
        shutil.copy2(path, temp_path)
        
        return temp_path
    except Exception as ex:
        raise Exception("Temp File Error: {0}".format(ex))
        
def swap_files(target, temp):
    try:
        if os.path.exists(target):
            os.remove(target)
        
        if os.path.exists(target):
            raise Exception("Deleting target file {0} failed".format(target))
        
        shutil.copy2(temp, target)

    except Exceptopn as ex:
        raise Exception("File Error: {0}".format(ex))

def method_delete(context, query_object):
    try:
        table_name = query_object['meta']['from']['table']
        query_object['table'] = context.database.get(table_name)
        if None == query_object['table']:
            raise Exception("Table '{0}' does not exist.".format(table_name))


        line_number = 1
        affected_rows = 0
        temp_file_prefix = "del" 

        # process file
        #copy soure file to temp file...
       data_file=query_object['table'].data.path
       temp_data_file=create_temporary_copy(data_file,temp_file_prefix)

        with open(temp_data_file, 'r') as content_file:
            with temp_file=tempfile.NamedTemporaryFile(mode='w+b', prefix=temp_file_prefix,delete=True)
                for line in content_file:
                    processed_line = process_line(context,query_object, line, line_number)
                    if None != processed_line['error']:
                        context.add_error(processed_line['error'])
                    line_number += 1
                    # skip matches
                    if True == processed_line['match']:
                        affected_rows += 1
                        continue
                    temp_file.write(processed_line['raw'])
                    temp_file.write(query_object['table'].delimiters.get_new_line())
        swap_files(query_object['table'].data.path, temp_file_name)
        return  query_results(success=True,affected_rows=affected_rows)
    except Exception as ex:
        return  query_results(success=False, error=ex)

    