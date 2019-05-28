# cython: linetrace=True

from ..functions.functions import *
from .record_core import process_line, query_results
from ..file_io.locking import lock
from ..version import __version__
import os
import tempfile


#used for order by a HACK to be fixed
context_sort=[]

def method_select(context, query_object, parser):
    #try:
        context.info(query_object)
        # make sure columns are valid, and from is good
        select_validate_columns_and_from(context,query_object,parser)

        #create data destinaton
        temp_table = context.database.temp_table()
        
        # add columns, as renamed
        add_table_columns(context,query_object,temp_table)
       
        # setup column ordinals
        set_ordinals(context,query_object)

        # TODO Unique column names, no ambiguious index, name, alias,functions
        # TODO Columns with the same name can be renamed, but fail. Key issue?

        # scan the table for matches and collect the data
        temp_data=select_process_file(context,query_object)
        
        all_records_count=len(temp_data)

        # TODO Join code here.....

        # order the data by columns, aliases or indexes
        temp_data=order_by(context,query_object,temp_data)

        # Distinct, a custom grouping
        temp_data=distinct(context,query_object,temp_data)
        
        # Grouping
        # group(context, data)
        
        # Limit / Filter the data
        temp_data = limit(context, query_object, temp_data)

        # assign matched and transformed data to temp table
        temp_table.results=temp_data

        return query_results(success=True,data=temp_table,total_data_length=all_records_count)
    #except Exception as ex:
        # something blew up. Bail!
        #print ex
    #    return query_results(success=False,error=ex)   


def select_process_file(context,query_object):
    has_columns = select_has_columns(context,query_object)
    has_functions = select_has_functions(context,query_object)
    table=None
    line_number = 1
    data=[]
    if True == has_columns:
        if 'table' in  query_object:
            table= query_object['table']
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
                processed_line = process_line(context,query_object, line, line_number,column_count,delimiter,visible_whitespace,visible_comments, visible_errors)


                # not a match, skip
                if False == processed_line['match']:
                    line_number += 1
                    continue
                
                # there is data, rebuild and add
                if None != processed_line['data']:
                    restructured_line = process_select_row(context,query_object,processed_line) 
                    data+=[restructured_line]
                line_number += 1
        
        # release lock ans swap files if need be.
        context.auto_commit(table)
    # file is closed at this point, proccess the no "FROM" statement
    if False == has_columns and True == has_functions:
        row=process_select_row(context,query_object,None)
        data+=[row]

    # return the acumulated data
    return data



def select_validate_columns_and_from(context, query_object, parser):
    has_functions = select_has_functions(context,query_object)
    has_columns = select_has_columns(context,query_object)

    if False == has_columns and 'from' in query_object['meta']:
        raise Exception("Invalid FROM, all columns are functions")

    if False == has_columns and False == has_functions:
        raise Exception("no columns defined in query")


    # if has functions, tables may not be needed
    if True == has_columns:
        if 'from' in query_object['meta']:
            # get DB name
            if 'database' in query_object['meta']['from']:
                context.info('Database specified')
                database_name=query_object['meta']['from']['database']
            else:
                context.info('Using curent database context')
                database_name=context.database.get_curent_database()

            table_name = query_object['meta']['from']['table']
            table= context.database.get(table_name,database_name)
            if None == table:
                except_str="Table '{0}' does not exist.".format(table_name)
                raise Exception(except_str)
            query_object['table']= table
            table_columns = table.get_columns()
            parser.expand_columns(query_object, table_columns)
            column_len = table.column_count()
            if column_len == 0:
                raise Exception("No defined columns in configuration")
        else:
            raise Exception("Missing FROM in select")



def select_has_columns(context,query_object):
    for c in query_object['meta']['columns']:
        if 'column' in c:
            context.info("Has columns, needs a table")
            return  True
    return False
            
def select_has_functions(context,query_object):
    for c in query_object['meta']['columns']:
        if 'function' in c:
            context.info("Has functions, doesnt need a table")
            return True
    return False


def add_table_columns(context,query_object,temp_table):
    for column in query_object['meta']['columns']:
        display = None
        if 'display' in column:
            display = column['display']
            context.info("RENAME COLUMN", display)

        if 'column' in column:
            context.info("adding data column")
            temp_table.add_column(column['column'], display)
        if 'function' in column:
            context.info("adding function column")
            temp_table.add_column(column['function'], display)    

def set_ordinals(context,query_object):
    ordinals={}
    index=0
    for column in query_object['meta']['columns']:
        if 'display' in column:
            name=column['display']
            if '{0}'.format(name) in ordinals:
                raise Exception("ambigious column {0}".format(name))
            ordinals['{0}'.format(name)]=index                
        if  'function' in column:
            name=column['function']
            if '{0}'.format(name) in ordinals:
                raise Exception("ambigious column {0}".format(name))
            ordinals['{0}'.format(name)]=index                
        if 'column' in column:
            name=column['column']
            if '{0}'.format(name) in ordinals:
                raise Exception("ambigious column {0}".format(name))
            ordinals['{0}'.format(name)]=index                
        else:
            # TODO ERROR
            continue
        ordinals['{0}'.format(name)]=index                
        index+=1
    query_object['meta']['ordinals']=ordinals

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

def order_by(context,query_object,data):
    global context_sort

    if 'order by' not in query_object['meta']:
        return data
    context.info("Select has Order By")
    context_sort = []
    for c in query_object['meta']['order by']:
        if c['column'] not in query_object['meta']['ordinals']:
            raise Exception ("ORDER BY column not present in the result set")
        ordinal = query_object['meta']['ordinals'][c['column']]
        direction = 1
        if 'asc' in c:
            direction = 1
        elif 'desc' in c:
            direction = -1
        context_sort.append([ordinal, direction])
    
    context.info(context_sort)
    try:
      # the python2 way
      ordered_data = sorted(data, sort_cmp)
    except:
      # the python3 way
      ordered_data = sorted(data,key=cmp_to_key(sort_cmp))
      pass

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
       

def distinct(context,query_object,data):
    if 'distinct' not in query_object['meta']:
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


def process_select_row(context,query_object,processed_line):
    row=[]
    # has_columns = select_has_columns(context,query_object)
    if 'table' in query_object:
        ordinals=query_object['table'].ordinals
    else:
        ordinals=None
    if None == processed_line:
        line_type=context.data_type.DATA
        error= None
        raw= None
        for c in query_object['meta']['columns']:
            if 'function' in c:
                if c['function'] == 'database':
                    row.append(f_database(context))
                elif c['function'] == 'datetime':
                        row.append(f_datetime(context))
                elif c['function'] == 'date':
                        row.append(f_date(context))
                elif c['function'] == 'time':
                        row.append(f_time(context))
                elif c['function'] == 'version':
                        row.append(f_version(context,__version__))
                elif c['function'] == 'row_number':
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
            for c in query_object['meta']['columns']:
                if 'column' in c:
                    row.append(processed_line['data'][ordinals[c['column']]])
                elif 'function' in c:
                    if c['function'] == 'database':
                        row.append(f_database(context))
                    elif c['function'] == 'datetime':
                            row.append(f_datetime(context))
                    elif c['function'] == 'date':
                            row.append(f_date(context))
                    elif c['function'] == 'time':
                            row.append(f_time(context))
                    elif c['function'] == 'version':
                            row.append(f_version(context,__version__))
                    elif c['function'] == 'row_number':
                            row.append(f_row_number(context))
                    #elif c['function'] == 'lower':
                    #     row.append(context.functions.lower(c['column']))
                    #elif c['function'] == 'upper':
                    #     row.append(context.functions.upper(c['column']))
                    #elif c['function'] == 'cat':
                    #     row.append(context.functions.cat(c['arg1'],c['arg2']))
        
    return {'data': row, 'type': line_type, 'error': error,'raw':raw} 


def sort_cmp( x, y):
    #print("Sort", context_sort)
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
    
def limit(context, query_object, data):
    index = 0
    length = None

    if 'limit' in query_object['meta']:
        if 'start' in query_object['meta']['limit']:
            index = query_object['meta']['limit']['start']
            # index=index-1
        if 'length' in query_object['meta']['limit']:
            length = query_object['meta']['limit']['length']
            if length<0:
                raise Exception("Limit: range index invalid, Value:'{0}'".format(index))


    context.info("Limit:{0},Length:{1}".format(index, length))
    if index<0:
        raise Exception("Limit: range index invalid, Value:'{0}'".format(index))

    if None == index:
        index = 0
    if None == length:
        length = len(data) - index

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


