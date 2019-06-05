# cython: linetrace=True

from .record_core import process_line, query_results
import tempfile

def method_delete(context, query_object):
    try:
        if 'database' in query_object['meta']['source']:
            context.info('Database specified')
            database_name = query_object['meta']['source']['database']
        else:
            context.info('Using curent database context')
            database_name = context.database.get_curent_database()

        table_name = query_object['meta']['source']['table']
        table= context.database.get(table_name,database_name)
        query_object['table']=table

        if None == query_object['table']:
            raise Exception("Table '{0}' does not exist.".format(table_name))


        line_number = 1
        affected_rows = 0
        # if autocommit... create a temp copy everytime
        # if batch transaction, make 1 copy, always pull from that
        temp_data_file=context.get_data_file(table)
        diff=[]

        column_count=table.column_count()
        delimiter=table.delimiters.field
        visible_whitespace=table.visible.whitespace
        visible_comments=table.visible.comments
        visible_errors=table.visible.errors
        
        with open(temp_data_file, 'r') as content_file:
            temp_file=tempfile.NamedTemporaryFile(mode='w', prefix="DST_DELETE",delete=False) 
            for line in content_file:
                 
                processed_line = process_line(context,query_object, line, line_number,column_count,delimiter,visible_whitespace,visible_comments, visible_errors)
                if None != processed_line['error']:
                    context.add_error(processed_line['error'])
                line_number += 1
                # skip matches
                if True == processed_line['match']:
                    affected_rows += 1
                    diff.append("Deleted Line: {0}, {1}".format(line_number-1,line))
                    continue
                temp_file.write(processed_line['raw'])
                temp_file.write(query_object['table'].delimiters.get_new_line())
            temp_file.close()
            context.autocommit_write(table,temp_file.name)
        context.auto_commit(table)
        return  query_results(success=True,affected_rows=affected_rows,diff=diff)
    except Exception as ex:
        print(ex)
        return  query_results(success=False, error=ex)


