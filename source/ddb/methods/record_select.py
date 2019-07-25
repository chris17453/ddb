# cython: profile=True
# cython: linetrace=True
# cython: binding=True

from ..functions.functions import *
from .record_core import  query_results
from ..file_io.locking import lock
from ..version import __version__
import os
import tempfile



class match2:

    def evaluate_single_match(self,test, row, table):
        
        compare1 = None
        compare2 = None
        compare1_is_column = False
        compare2_is_column = False

        comparitor = test.c
        #cdef int index 
        #cdef str like = None
        #cdef str data = None

        # if None !=comparitor:
        #   comparitor=comparitor.lower()
        for column in table.columns:
            #print column.data.name
            if column.data.name == test.e1:
                index = table.ordinals[column.data.name]
                #print "found1", column.data.name
                compare1 = row[index]  # table.ordinals[].get_data_from_column(column,row)
                # compare1=table.get_data_from_column(column,row)
                compare1_is_column = True
            elif column.data.name == test.e2:
                index = table.ordinals[column.data.name]
                #print "found2", column.data.name
                compare2 = row[index]  # table.get_data_from_column(column,row)
                # compare2=table.get_data_from_column(column,row)
                compare2_is_column = True
            if None != compare1 and None != compare2:
                break

        if not compare1_is_column and not compare2_is_column:
            raise Exception("expression invalid {0}".format(test))
                

        if None == compare1:
            compare1 = test.e1
        if None == compare2:
            compare2 = test.e2
        
        if comparitor == '=' or comparitor == 'is':
            if compare1 == compare2:
                #print compare1,compare2
                return True
        elif comparitor == 'like':  # paritial match

            if True == compare1_is_column and True == compare2_is_column:
                raise Exception("Where invalid {0}, like cant be between 2 columns".format(test))

            if True == compare1_is_column:
                like = compare2
                data = compare1
            else:
                like = compare1
                data = compare2

            if None == like:
                return False
            # if len(like)==0:
            #    return False
            #print "--"
            #print compare1,compare2,like
            if like[0] == '%':
                like_left = True
            else:
                like_left = False

            if like[-1] == '%':
                like_right = True
            else:
                like_right = False

            # compare middle of search
            if True == like_right and True == like_left:
                if data.find(like[1:-1]) > -1:
                    return True
                else:
                    return False

            # if not found at end bail
            if True == like_left:
                if data[-(len(like) - 1):] == like[1:]:
                    return True
                else:
                    return False

            # if not found at start, bail
            if True == like_right:
                if data[0:(len(like) - 1)] == like[0:-1]:
                    return True
                else:
                    return False

            return False
        elif comparitor == '<':
            if compare1 < compare2:
                return True
        elif comparitor == '>':
            if compare1 > compare2:
                return True
        elif comparitor == '>=':
            if compare1 >= compare2:
                return True
        elif comparitor == '<=':
            if compare1 <= compare2:
                return True
        elif comparitor == '!=' or comparitor == '<>' or comparitor == 'not':
            if compare1 != compare2:
                return True

        return False


    def evaluate_match(self,meta, row):
        if None == row:
            return False
        #print where
        table=meta.table
        
        success = None
        skip_section = False
        operation = ""
        for test in meta.where:

            test.condition=test.condition.lower()
            #print test
            # if a evaluation chain failed, continue until out of that section
            if test.condition=='and' and skip_section:
                continue
            else:
                skip_section = False

            operation = None
            if test.condition=='where':
                operation = 'where'

            elif test.condition=='or':
                operation = 'or'
                if success:
                    return True

            elif test.condition=='and':

                operation = 'and'
                if not success:
                    skip_section = True
                    continue
            #print test
            #if test.condition=='where':
            #    test_operation = getattr(test,'where')
            #elif hasattr( test,'and'):
            #    test_operation = getattr(test,'and')
            #elif hasattr( test,'or'):
            #    test_operation = getattr(test,'or')
            #test.debug()
            success = self.evaluate_single_match(test, row, table)

        # never matched anytthing...
        if success is None:
            return False
        return success

#used for order by a HACK to be fixed
context_sort=[]

def method_select(context, meta, parser):
    #try:
        #meta.debug()
        context.info(meta)
        # make sure columns are valid, and from is good
        select_validate_columns_and_from(context,meta,parser)

        #create data destinaton
        temp_table = context.database.temp_table()
        
        # add columns, as renamed
        add_table_columns(context,meta,temp_table)
       
        # setup column ordinals
        set_ordinals(context,meta)

        # TODO Unique column names, no ambiguious index, name, alias,functions
        # TODO Columns with the same name can be renamed, but fail. Key issue?

        # scan the table for matches and collect the data
        temp_data=select_process_file(context,meta)
        
        all_records_count=len(temp_data)

        # TODO Join code here.....

        # order the data by columns, aliases or indexes
        temp_data=order_by(context,meta,temp_data)

        # Distinct, a custom grouping
        #temp_data=distinct(context,meta,temp_data)
        
        # Grouping
        # group(context, data)
        
        # Limit / Filter the data
        temp_data = limit(context, meta, temp_data)

        # assign matched and transformed data to temp table
        temp_table.results=temp_data

        return query_results(success=True,data=temp_table,total_data_length=all_records_count)
    #except Exception as ex:
        # something blew up. Bail!
        #print ex
    #    return query_results(success=False,error=ex)   


def select_process_file(context,meta):
    has_columns = select_has_columns(context,meta)
    has_functions = select_has_functions(context,meta)
    table=None
    line_number = 1
    data=[]
    if True == has_columns:
        if meta.table:
            table= meta.table
        else:
            raise Exception ('table configuration has no data file')
        
        
        # if autocommit... create a temp copy everytime
        # if batch transaction, make 1 copy, always pull from that
        temp_data_file=context.get_data_file(table)

        column_count=table.column_count()
        delimiter=table.delimiters.field
        visible_whitespace=table.visible.whitespace
        visible_comments=table.visible.comments
        visible_errors=table.visible.errors

        with open(temp_data_file, 'r') as content_file:
            for line in content_file:
                processed_line = process_line3(context, meta, line, line_number,column_count,delimiter,visible_whitespace,visible_comments, visible_errors)


                # not a match, skip
                if False == processed_line['match']:
                    line_number += 1
                    continue
                
                # there is data, rebuild and add
                if None != processed_line['data']:
                    restructured_line = process_select_row(context,meta,processed_line) 
                    data+=[restructured_line]
                line_number += 1
        
        # release lock ans swap files if need be.
        context.auto_commit(table)
    # file is closed at this point, proccess the no "FROM" statement
    if False == has_columns and True == has_functions:
        row=process_select_row(context,meta,None)
        data+=[row]

    # return the acumulated data
    return data



def select_validate_columns_and_from(context, meta, parser):
    has_functions = select_has_functions(context,meta)
    has_columns = select_has_columns(context,meta)

    if False == has_columns and meta.source:
        err_msg="Invalid FROM, all columns are functions. Columns:{0}, Functions:{1}, Source:{2}".format(has_columns,has_functions,meta.source)
        raise Exception(err_msg)

    if False == has_columns and False == has_functions:
        err_msg="No columns defined in query. Columns:{0}, Functions:{1}, Source:{2}".format(has_columns,has_functions,meta.source)
        raise Exception(err_msg)
        


    # if has functions, tables may not be needed
    if True == has_columns:
        if meta.source:
            meta.table = get_table(context,meta)
            expand_columns(meta)
            column_len = meta.table.column_count()
            if column_len == 0:
                raise Exception("No defined columns in configuration")
        else:
            raise Exception("Missing FROM in select")



def get_table(context,meta):
    if meta.source:
        if meta.source.database:
            context.info('Database specified')
            database_name=meta.source.database
        else:
            context.info('Using curent database context')
            database_name=context.database.get_curent_database()
        table_name = meta.source.table
        table= context.database.get(table_name,database_name)
        if None == table:
            except_str="Table '{0}' does not exist.".format(table_name)
            raise Exception(except_str)
        return table
    return None

    

def expand_columns(meta):
    #print meta
    table_columns = meta.table.get_columns()
    if meta.columns:
        expanded_select = []
        for item in meta.columns:
            # TODO:leftover stuff cleanup for configuration.TABLE
            if item.column:
                if item.column == '*':
                    for column in table_columns:
                        expanded_select.append(meta._columns(column=column))
                else:
                    expanded_select.append(item)
            if item.function:
                expanded_select.append(item)

        meta.columns = expanded_select
    # ?? needed



def select_has_columns(context,meta):
    for c in meta.columns:
        if c.column:
            context.info("Has columns, needs a table")
            return  True
    return False
            
def select_has_functions(context,meta):
    for c in meta.columns:
        if c.function:
            context.info("Has functions, doesnt need a table")
            return True
    return False


def add_table_columns(context,meta,temp_table):
    #print meta
    for column in meta.columns:
        display = None
        #print meta.columns
        if column.display:
            display = column.display
            context.info("RENAME COLUMN", display)

        if column.column:
            context.info("adding data column")
            temp_table.add_column(column.column, display)
        if  column.function:
            context.info("adding function column")
            temp_table.add_column(column.function, display)    

def set_ordinals(context,meta):
    ordinals={}
    index=0
    for column in meta.columns:
        if  column.display:
            name=column.display
            if '{0}'.format(name) in ordinals:
                raise Exception("ambigious column {0}".format(name))
            ordinals['{0}'.format(name)]=index                
        if  column.function:
            name=column.function
            if '{0}'.format(name) in ordinals:
                raise Exception("ambigious column {0}".format(name))
            ordinals['{0}'.format(name)]=index                
        if  column.column:
            name=column.column
            if '{0}'.format(name) in ordinals:
                raise Exception("ambigious column {0}".format(name))
            ordinals['{0}'.format(name)]=index                
        else:
            # TODO ERROR
            continue
        ordinals['{0}'.format(name)]=index                
        index+=1
    meta.ordinals=ordinals ##################################################

def cmp_to_key(mycmp):
    'Convert a cmp= function into a key= function'
    class K:
        def __init__(self, obj, *args):
            self.obj = obj
        def __lt__(self, other):
            return mycmp(self.obj, other.obj) < 0
        def __gt__(self, other):
            return mycmp(self.obj, other.obj) > 0
        def __eq__(self, other):
            return mycmp(self.obj, other.obj) == 0
        def __le__(self, other):
            return mycmp(self.obj, other.obj) <= 0
        def __ge__(self, other):
            return mycmp(self.obj, other.obj) >= 0
        def __ne__(self, other):
            return mycmp(self.obj, other.obj) != 0
    return K

def order_by(context,meta,data):
    global context_sort
    
    if not meta.order_by:
        context.info("NO order by")
        return data
    context.info("Select has Order By")
    context_sort = []
    for c in meta.order_by:
        if c.column not in meta.ordinals:
            err="ORDER BY column not present in the result set '{0}'".format(c.column)
            raise Exception (err)
        ordinal =meta.ordinals[c.column]
        context_sort.append([ordinal, c.direction])
    
    context.info(context_sort)
    try:
      # the python2 way
      ordered_data = sorted(data, sort_cmp)
    except  Exception as ex:
        raise Exception ("Error sorting. {0}".format(ex))
      # the python3 way
      #ordered_data = sorted(data,key=cmp_to_key(sort_cmp))
      #pass

    return ordered_data


def group(context,data):
        ## TODO grouping happens after ordering and before limiting
        #if 'group by' in query_object['meta']:
        #    group=[]
        #    for item in temp_data:
        #        no_item=True
        #        for group_item in group:
        #            if context.compare_data(group_item['data'],item['data']):
        #                no_item=None
        #                break
        #        if no_item:
        #            group.append(item)
        #    temp_data=group
    return data
       

def distinct(context,meta,data):
    if not meta.distinct:
        return data

    context.info("Select has Distinct")
    group=[]
    for item in data:
        no_item=True
        for group_item in group:
            if compare_data(context,group_item['data'],item['data']):
                no_item=None
                break
        if no_item:
            group.append(item)
    return group    


def process_select_row(context,meta,processed_line):
    row=[]
    #meta.debug()
    if meta.source:
    
        ordinals=meta.table.ordinals
    else:
        ordinals=None
    if None == processed_line:
        line_type=context.data_type.DATA
        error= None
        raw= None
        for c in meta.columns:
            if c.function:
                if c.function == 'database':
                    row.append(f_database(context))
                elif c.function == 'datetime':
                        row.append(f_datetime(context))
                elif c.function == 'date':
                        row.append(f_date(context))
                elif c.function == 'time':
                        row.append(f_time(context))
                elif c.function == 'version':
                        row.append(f_version(context,__version__))
                elif c.function == 'row_number':
                        row.append(f_row_number(context))
                #elif c['function'] == 'lower':
                #     row.append(context.functions.lower(c['column']))
                #elif c['function'] == 'upper':
                #     row.append(context.functions.upper(c['column']))
                #elif c['function'] == 'cat':
                #     row.append(context.functions.cat(c['arg1'],c['arg2']))
    else:
        line_type=processed_line['type']
        error= processed_line['error']
        raw= processed_line['raw']
        if line_type!=context.data_type.ERROR:
            for c in meta.columns:
                if c.column:
                    row.append(processed_line['data'][ordinals[c.column]])
                elif c.function:
                    if c.function == 'database':
                        row.append(f_database(context))
                    elif c.function == 'datetime':
                            row.append(f_datetime(context))
                    elif c.function == 'date':
                            row.append(f_date(context))
                    elif c.function == 'time':
                            row.append(f_time(context))
                    elif c.function == 'version':
                            row.append(f_version(context,__version__))
                    elif c.function == 'row_number':
                            row.append(f_row_number(context))
                    #elif c['function'] == 'lower':
                    #     row.append(context.functions.lower(c['column']))
                    #elif c['function'] == 'upper':
                    #     row.append(context.functions.upper(c['column']))
                    #elif c['function'] == 'cat':
                    #     row.append(context.functions.cat(c['arg1'],c['arg2']))
        
    return {'data': row, 'type': line_type, 'error': error,'raw':raw} 


def sort_cmp( x, y):
    for c in context_sort:
        ordinal = c[0]
        direction = c[1]
        #convert = lambda text: int(text) if text.isdigit() else text
        #alphanum_key = lambda key: [convert(c) for c in re.split('([0-9]+)', key)]
        # %print x[ordinal],y[ordinal],-1
        if x['data'][ordinal] == y['data'][ordinal]:
            continue

        if x['data'][ordinal] < y['data'][ordinal]:
            return -1 * direction
        else:
            return 1 * direction
    return 0
    
def limit(context, meta, data):
    index = 0
    length = None

    if meta.limit:
        if meta.limit.start:
            index = meta.limit.start
            # index=index-1
        if meta.limit.length:
            length = meta.limit.length
            if length<0:
                raise Exception("Limit: range index invalid, Value:'{0}'".format(index))
    else:
        # no limit...
        return data


    context.info("Limit:{0},Length:{1}".format(index, length))
    if index<0:
        raise Exception("Limit: range index invalid, Value:'{0}'".format(index))

    # only 1 variable and its 0, so its really a 0 length query.

    if meta.limit.start==0 and meta.limit.length==None:
        return []

    # its 0 length
    if meta.limit.length==0:
        return []


    if None == index:
        index = 0
    if None == length:
        length = len(data) - index

    #print index,length
    data_length = len(data)
    if index >= data_length:
        #print("-Index is out of range for query. {} of {}".format(index,data_stream_lenght))
        return []
    if index + length > data_length:
        #print("Length is out of range for query. {} of {}".format(length,data_stream_lenght))
        length = data_length - index
    return data[index:index + length]

def compare_data(context,data1, data2):
    if data1 is None or data2 is None:
        return None
    if (not isinstance(data1, dict)) or (not isinstance(data2, dict)):
        if len(data1)!=len(data2):
            return None
        for index in range(0,len(data1)):
            if data1[index]!=data2[index]:
                return None
    else:
        shared_keys = set(data2.keys()) & set(data2.keys())
        if not ( len(shared_keys) == len(data1.keys()) and len(shared_keys) == len(data2.keys())):
            return None

        for key in data1.keys():
            if data1[key] != data2[key]:
                return None
    return True




def process_line3(context,meta, line, line_number=0,column_count=0,delimiter=',',visible_whitespace=None,visible_comments=None, visible_errors=None):
    err = None
    table=meta.table
    # TODO move rstrip to after split for limited data copy operations
    line_cleaned = line.rstrip()
    line_data = None
    match_results=False
    if table.data.starts_on_line > line_number:
        line_type = context.data_type.COMMENT
        line_data = line
        try_match=False
        #print table.data.starts_on_line,line_number
    else:
        line_type = context.data_type.DATA
        try_match=True
    if try_match:
        if not line_cleaned:
            if True == visible_whitespace:
                line_data = ['']
            line_type = context.data_type.WHITESPACE
        else:
            if line_cleaned[0] in table.delimiters.comment:
                if True == visible_comments:
                    line_data = [line_cleaned]
                line_type = context.data_type.COMMENT
            else:
                line_data = line_cleaned.split(table.delimiters.field,column_count)
                #cur_column_len = len(line_data)
                
                #line_data[-1]=line_data[-1].rstrip()
                cur_column_len = len(line_data)
                
                if table.data.strict_columns==True:
                    if  cur_column_len != column_count:
                        if cur_column_len > column_count:
                            err = "Table {2}: Line #{0}, {1} extra Column(s)".format(line_number, cur_column_len -column_count, table.data.name)
                        else:
                            err = "Table {2}: Line #{0}, missing {1} Column(s)".format(line_number, column_count - cur_column_len, table.data.name)
                        # table.add_error(err)
                        line_type = context.data_type.ERROR

                        # turn error into coment
                        if True == visible_errors:
                            line_data = line_cleaned
                        else:
                            line_data = None
                        line_type = context.data_type.ERROR
                else:
                    # add empty columns
                    if  cur_column_len != column_count:
                        i=cur_column_len
                        while i<column_count:
                            line_data+=['']
                            i+=1


                # fields are surrounded by something... trim
                #print context.table.delimiters.block_quote
                if None != table.delimiters.block_quote:
                    line_data_cleaned = []
                    for d in line_data:
                        line_data_cleaned+=d[1:-1]
                    line_data = line_data_cleaned

        # If no where. return everything
        if not meta.where:
            match_results = True
        else:
            # if a where, only return data, comments/whites/space/errors are ignored
            
            if line_type == context.data_type.DATA:
                match_results = match2().evaluate_match(meta=meta, row=line_data)
            else:
                match_results = False
        if visible_whitespace is False and line_type==context.data_type.WHITESPACE:
            match_results=False
        elif visible_comments is False and line_type==context.data_type.COMMENT:
            match_results=False
        elif visible_errors is False and line_type==context.data_type.ERROR:
            match_results=False


    # raw has rstrip for line.. maybe configuration option? Extra data anyway...
    return {'data': line_data, 
            'type': line_type, 
            'raw': line_cleaned, 
            'line_number': line_number, 
            'match': match_results, 
            'error': err}




