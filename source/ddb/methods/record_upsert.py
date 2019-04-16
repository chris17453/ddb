
import tempfile  # from table import table
from .record_core import process_line, swap_files, query_results, create_temporary_copy,remove_temp_file
from .record_update  import update_single
from .record_insert  import create_single
def method_upsert(context, query_object):
    try:
        if 'database' in query_object['meta']['into']:
            context.info('Database specified')
            database_name = query_object['meta']['into']['database']
        else:
            context.info('Using curent database context')
            database_name = context.database.get_curent_database()

        table_name = query_object['meta']['into']['table']
        query_object['table'] = context.database.get(table_name,database_name)
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
        temp_file_prefix="UPSERT"
        data_file=query_object['table'].data.path
        temp_data_file=create_temporary_copy(data_file,temp_file_prefix)
        #print data_file,temp_data_file
        
        with open(temp_data_file, 'r') as content_file:
            with tempfile.NamedTemporaryFile(mode='w', prefix=temp_file_prefix,delete=True) as temp_file:
      
                for line in content_file:
                    #print line
                    processed_line = process_line(context,query_object, line, line_number)
                    if None != processed_line['error']:
                        context.add_error(processed_line['error'])
                    line_number += 1
                    # skip matches
                    if True == processed_line['match']:
                        results = update_single(context,query_object, temp_file,  False, processed_line)
                        if True == results:
                            affected_rows += 1
                        continue
                    temp_file.write(processed_line['raw'])
                    temp_file.write(query_object['table'].delimiters.get_new_line())
                # NO update occured.. Lets Insert...
                if affected_rows==0:
                    context.info("No row found in upsert, creating")
                    results = create_single(context,query_object, temp_file,False)
                else:
                    context.info("row found in upsert")

                temp_file.flush()
                swap_files(data_file, temp_file.name)
        
        #remove_temp_file(temp_data_file)      
                

        return query_results(affected_rows=affected_rows,success=True)
    except Exception as ex:
        print (ex)
        remove_temp_file(temp_data_file)      
        return query_results(success=False,error=ex)



