import sys
from .record_core import process_line3, query_results, get_table
from ..file_io.locking import temp_path_from_file
import tempfile

def method_delete(context, meta):
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
        
        content_file=open(temp_data_file, 'rb', buffering=0)
        try:
            dst_temp_filename=temp_path_from_file(meta.table.data.path,"ddb_DST_DELETE",unique=True)
            temp_file=open (dst_temp_filename,"wb", buffering=0)
            try:
#
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
                    
                    temp_file.write(str.encode(processed_line['raw']))
                    temp_file.write(str.encode(meta.table.delimiters.get_new_line()))
            finally:
                temp_file.close()
        finally:
            content_file.close()
            
        context.autocommit_write(meta.table,dst_temp_filename)
        context.auto_commit(meta.table)
        return  query_results(success=True,affected_rows=affected_rows,diff=diff)
    except:
        err = sys.exc_info()[1]
        ex = err.args[0]

        context.error (__name__,ex)
        return query_results(success=False,error=str(ex))   


