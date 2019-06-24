# cython: linetrace=True

import tempfile  # from table import table
from .record_core import process_line, query_results

def update_single(context,query_object, temp_file, requires_new_line, processed_line):
    err = False
    ###
    # insert new data at end of file
    new_line = ''
    err = False
    #print query_object

    # make sure the inserted columns exist
    for c2 in range(0, len(query_object['meta']['set'])):
        column_name = query_object['meta']['set'][c2]['column']
        if None == query_object['table'].get_column_by_name(column_name):
            context.add_error("column in update statement does not exist in table: {0}".format(column_name))
            #print "no column"
            err = True

    if False == err:
        for c in range(0, query_object['table'].column_count()):
            column_name = query_object['table'].get_column_at_data_ordinal(c)
            value = processed_line['data'][c]
            for c2 in range(0, len(query_object['meta']['set'])):
                #print column_name,query_object['meta']['set']
                if query_object['meta']['set'][c2]['column'] == column_name:
                    #print("Column {} at table index {} located at query index {}".format(column_name,c, c2))
                    value = query_object['meta']['set'][c2]['expression']
            if c > 0:
                new_line += '{0}'.format(query_object['table'].delimiters.field)
            new_line += '{0}'.format(value)

    if False == err:
        #print new_line
        if True == requires_new_line:
            temp_file.write(query_object['table'].delimiters.get_new_line())
        temp_file.write(new_line)
        temp_file.write(query_object['table'].delimiters.get_new_line())
    if False == err:
        return {'success':True,'line':new_line}
    else:
        return {'success':False,'line':new_line}

def method_update(context, query_object):
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
        temp_data_file=context.get_data_file(table)
        diff=[]

        column_count=table.column_count()
        delimiter=table.delimiters.field
        visible_whitespace=table.visible.whitespace
        visible_comments=table.visible.comments
        visible_errors=table.visible.errors


        with open(temp_data_file, 'r') as content_file:
            with tempfile.NamedTemporaryFile(mode='w', prefix="UPDATE",delete=False) as temp_file:
      
                for line in content_file:
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
                temp_file.close()
                context.autocommit_write(table,temp_file.name)
        context.auto_commit(table)
        return query_results(affected_rows=affected_rows,success=True,diff=[])
    except Exception as ex:
        #print (ex)
        return query_results(success=False,error=ex)



