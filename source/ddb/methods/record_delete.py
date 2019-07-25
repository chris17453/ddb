# cython: linetrace=True

from .record_core import process_line3, query_results, get_table
import tempfile

def method_delete(context, query_object):
    try:
        meta.table=get_table(context,meta)

        line_number = 1
        affected_rows = 0
        # if autocommit... create a temp copy everytime
        # if batch transaction, make 1 copy, always pull from that
        temp_data_file=context.get_data_file(meta.table)
        diff=[]

        column_count      =meta.table.column_count()
        delimiter         =meta.table.delimiters.field
        visible_whitespace=meta.table.visible.whitespace
        visible_comments  =meta.table.visible.comments
        visible_errors    =meta.table.visible.errors
        
        with open(temp_data_file, 'r') as content_file:
            temp_file=tempfile.NamedTemporaryFile(mode='w', prefix="DST_DELETE",delete=False) 
            for line in content_file:
                 
                processed_line = process_line3(context,meta, line, line_number,column_count,delimiter,visible_whitespace,visible_comments, visible_errors)
                if None != processed_line['error']:
                    context.add_error(processed_line['error'])
                line_number += 1
                # skip matches
                if True == processed_line['match']:
                    affected_rows += 1
                    diff.append("Deleted Line: {0}, {1}".format(line_number-1,line))
                    continue
                temp_file.write(processed_line['raw'])
                temp_file.write(meta.table.delimiters.get_new_line())
            temp_file.close()
            context.autocommit_write(meta.table,temp_file.name)
        context.auto_commit(meta.table)
        return  query_results(success=True,affected_rows=affected_rows,diff=diff)
    except Exception as ex:
        print(ex)
        return  query_results(success=False, error=ex)


