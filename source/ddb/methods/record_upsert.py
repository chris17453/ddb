# cython: linetrace=True

import tempfile  # from table import table
from .record_core import process_line, query_results
from .record_update  import update_single
from .record_insert  import create_single
def method_upsert(context, query_object):
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
        
        if 'on duplicate key' not in query_object['meta']:
            raise Exception("Upsert missing duplicate keys")

        where=[]
        for item in query_object['meta']['on duplicate key']:
            column=item['column']
            for index in range(0,len(query_object['meta']['columns'])):
                column_compare=query_object['meta']['columns'][index]['column']
                if column_compare==column:
                    value=query_object['meta']['values'][index]['value']
                    if len(where)==0:
                        mode='where'
                    else:
                        mode='and'
                    where.append({mode:{'e1':column,'c':'=','=':'=','e2':value}})
        query_object['meta']['where']=where
            

        context.info("Query object",query_object)
        #return None
        
    
        line_number = 1
        affected_rows = 0
        temp_data_file=context.get_data_file(table)
        diff=[]
        column_count=table.column_count()
        delimiter=table.delimiters.field
        visible_whitespace=table.visible.whitespace
        visible_comments=table.visible.comments
        visible_errors=table.visible.errors

        with open(temp_data_file, 'r') as content_file:
            with tempfile.NamedTemporaryFile(mode='w', prefix="UPSERT",delete=False) as temp_file:
      
                for line in content_file:
                    #print line
                    processed_line = process_line(context,query_object, line, line_number,column_count,delimiter,visible_whitespace,visible_comments, visible_errors)
                    if None != processed_line['error']:
                        context.add_error(processed_line['error'])
                    line_number += 1
                    # skip matches
                    if True == processed_line['match']:
                        results = update_single(context,query_object, temp_file,  False, processed_line)
                        if True == results['success']:
                            diff.append(results['line'])
                            affected_rows += 1
                        continue
                    temp_file.write(processed_line['raw'])
                    temp_file.write(query_object['table'].delimiters.get_new_line())
                # NO update occured.. Lets Insert...
                if affected_rows==0:
                    context.info("No row found in upsert, creating")
                    results = create_single(context,query_object, temp_file,False)
                    if True==results['success']:
                        diff.append(results['line'])
                else:
                    context.info("row found in upsert")

                temp_file.close()
                context.autocommit_write(table,temp_file.name)
        context.auto_commit(table)                

        return query_results(affected_rows=affected_rows,success=True,diff=diff)
    except Exception as ex:
        print ("ERR",ex)
        #Sremove_temp_file(temp_data_file)      
        return query_results(success=False,error=ex)



