import sys
import tempfile  # from table import table
from .record_core import process_line3, query_results, get_table, file_writer
from ..file_io.locking import temp_path_from_file


            

def method_insert(context, meta):

    meta.table=get_table(context,meta)

    line_number = 1
    affected_rows = 0
    # process file
    requires_new_line = False
    
    column_count      = meta.table.column_count()
    delimiter         = meta.table.delimiters.field
    visible_whitespace= meta.table.visible.whitespace
    visible_comments  = meta.table.visible.comments
    visible_errors    = meta.table.visible.errors
    
    temp_data_file=context.get_data_file(meta.table,"SRC_INSERT")
    diff=[]

    requires_new_line=False
    content_file=file_writer(temp_data_file,'a')
    try:
        results = create_single(context,meta, content_file, requires_new_line)
        if True == results['success']:
            diff.append(results['line'])
            affected_rows += 1
    finally:
        content_file.close()
    context.autocommit_write(meta.table,temp_data_file)
    context.auto_commit(meta.table)
    return query_results(success=True,affected_rows=affected_rows,diff=diff)
    
        

def create_single(context, meta, temp_file, requires_new_line):
    err = False
    ###
    # insert new data at end of file
    new_line = ''
    if len(meta.columns) != meta.table.column_count():
        context.add_error("Cannot insert, column count does not match table column count")
    else:
    
        if len(meta.values) != meta.table.column_count():
            context.add_error("Cannot insert, column value count does not match table column count")
        else:
            err = False
            for c in range(0, len(meta.columns)):
                column_name =meta.table.get_column_at_data_ordinal(c)
                found = False
                for c2 in range(0, len(meta.columns)):
                    if meta.columns[c2].column == column_name:
                        #print("Column {} at table index {} located at query index {}".format(column_name,c, c2))
                        found = True
                        if c > 0:
                            new_line += '{0}'.format(meta.table.delimiters.field)
                        new_line += '{0}'.format(meta.values[c2].value)
                if False == found:
                    context.add_error("Cannot insert, column in query not found in table: {0}".format(column_name))
                    err = True
                    break
            if False == err:
                #print new_line
                if True == requires_new_line:
                    temp_file.write(meta.table.delimiters.get_new_line())
                temp_file.write(new_line)
                temp_file.write(meta.table.delimiters.get_new_line())
    if False == err:
        return {'success':True,'line':new_line}
    else:
        return {'success':False,'line':new_line}


    

