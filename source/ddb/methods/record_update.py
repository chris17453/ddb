# NOcython: linetrace=True

import tempfile  # from table import table
from .record_core import process_line3, query_results, get_table
from ..file_io.locking import temp_path_from_file


def update_single(context,meta, temp_file, requires_new_line, processed_line):
    err = False
    ###
    # insert new data at end of file
    new_line = ''
    err = False
    #print meta

    # make sure the inserted columns exist
    for c2 in range(0, len(meta.set)):
        column_name = meta.set[c2].column
        if None == meta.table.get_column_by_name(column_name):
            context.add_error("column in update statement does not exist in table: {0}".format(column_name))
            #print "no column"
            err = True

    if False == err:
        for c in range(0, meta.table.column_count()):
            column_name = meta.table.get_column_at_data_ordinal(c)
            value = processed_line['data'][c]
            for c2 in range(0, len(meta.set)):
                #print column_name,meta.set
                if meta.set[c2].column == column_name:
                    #print("Column {} at table index {} located at query index {}".format(column_name,c, c2))
                    value = meta.set[c2].expression
            if c > 0:
                new_line += '{0}'.format(meta.table.delimiters.field)
            new_line += '{0}'.format(value)

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

def method_update(context, meta):
    try:
        meta.table=get_table(context,meta)

        line_number = 1
        affected_rows = 0
        temp_data_file=context.get_data_file(meta.table)
        diff=[]

        column_count      =meta.table.column_count()
        delimiter         =meta.table.delimiters.field
        visible_whitespace=meta.table.visible.whitespace
        visible_comments  =meta.table.visible.comments
        visible_errors    =meta.table.visible.errors


        with open(temp_data_file, 'r', buffering=0) as content_file:
            dst_temp_filename=temp_path_from_file(meta.table.data.path,"ddb_DST_UPDATE",unique=True)
            with open (dst_temp_filename,"w", buffering=0) as  temp_file:
      
                for line in content_file:
                    processed_line = process_line3(context,meta, line, line_number,column_count,delimiter,visible_whitespace,visible_comments, visible_errors)
                    if None != processed_line['error']:
                        context.add_error(processed_line['error'])
                    line_number += 1
                    # skip matches
                    if True == processed_line['match']:
                        results = update_single(context,meta, temp_file,  False, processed_line)
                        if True == results['success']:
                            diff.append(results['line'])
                            affected_rows += 1
                        continue
                    temp_file.write(processed_line['raw'])
                    temp_file.write(meta.table.delimiters.get_new_line())

            context.autocommit_write(meta.table,dst_temp_filename)
        context.auto_commit(meta.table)
        return query_results(affected_rows=affected_rows,success=True,diff=[])
    except Exception as ex:
        context.info (meta.mode,ex)
        return query_results(success=False,error=ex)



