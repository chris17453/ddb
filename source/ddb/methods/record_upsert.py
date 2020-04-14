import sys
import pprint
import tempfile  # from table import table
from .record_core import process_line3, query_results, get_table
from .record_update  import update_single
from .record_insert  import create_single
from ..file_io.locking import temp_path_from_file



def method_upsert(context, meta,query_object,main_meta):
    try:
        #meta.debug()
        #print(query_object)
        meta.table=get_table(context,meta)
        
        if not meta.on_duplicate_key:
            raise Exception("Upsert missing duplicate keys")

        where=[]
        for item in meta.on_duplicate_key:
            column=item.column
            for index in range(0,len(meta.columns)):
                column_compare=meta.columns[index].column
                if column_compare==column:
                    value=meta.values[index].value
                    if len(where)==0:
                        mode='where'
                    else:
                        mode='and'
                    where.append({mode:{'e1':column,'c':'=','=':'=','e2':value,'condition':mode}})
        
        query_object['meta']['where']=where
        #pprint.pprint(query_object)
        #return None
        
        query_object['mode']="update"
        meta_update=main_meta().convert_to_class(query_object)
        #meta_update.debug()
        meta_update.table=meta.table        

        line_number = 1
        affected_rows = 0
        temp_data_file=context.get_data_file(meta.table)
        diff=[]
        column_count       =meta.table.column_count()
        delimiter          =meta.table.delimiters.field
        visible_whitespace =meta.table.visible.whitespace
        visible_comments   =meta.table.visible.comments
        visible_errors     =meta.table.visible.errors

        content_file=open(temp_data_file, 'rb', buffering=0)
        try:
            dst_temp_filename=temp_path_from_file(meta.table.data.path,"ddb_DST_UPSERT",unique=True)
            temp_file=open (dst_temp_filename,"wb", buffering=0)
            try:
                for line in content_file:
                    #print line
                    processed_line = process_line3(context,meta_update, line, line_number,column_count,delimiter,visible_whitespace,visible_comments, visible_errors)
                    if None != processed_line['error']:
                        context.add_error(processed_line['error'])
                    line_number += 1
                    # skip matches
                    if True == processed_line['match']:
                        meta_class=main_meta().convert_to_class(query_object)
                      
                        results = update_single(context,meta_update, temp_file,  False, processed_line)
                        if True == results['success']:
                            diff.append(results['line'])
                            affected_rows += 1
                        continue
                    temp_file.write(str.encode(processed_line['raw']) )
                    temp_file.write(str.encode(meta.table.delimiters.get_new_line()) )
                # NO update occured.. Lets Insert...
                if affected_rows==0:
                    context.info("No row found in upsert, creating")
                    query_object['mode']="insert"
                    meta_class=main_meta().convert_to_class(query_object)
                    meta_class.table=meta.table

                    results = create_single(context,meta_class, temp_file,False)
                    affected_rows+=1
                    if True==results['success']:
                        diff.append(results['line'])
                else:
                    context.info("row found in upsert")

            finally:
                temp_file.close()
        finally:
            content_file.close()
        context.autocommit_write(meta.table,dst_temp_filename)
        context.auto_commit(meta.table)                

        return query_results(affected_rows=affected_rows,success=True,diff=diff)
    except:
        err = sys.exc_info()[1]
        ex = err.args[0]
        context.error (__name__,ex)
        return query_results(success=False,error=str(ex))   



