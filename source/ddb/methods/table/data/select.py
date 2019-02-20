from ....functions.functions import *
from ..core import *

def method_select(context, query_object, parser):
        # print ("in select")
        if 'distinct' in query_object['meta']:
            distinct=True
           # query_object['meta']['select']=query_object['meta']['select distinct']
        else:
            distinct=None
        context.info(query_object)
        temp_data = []
        hash_dict={}
        # if has columns, then it needs a table

        has_functions = False
        has_columns = False
        for c in query_object['meta']['columns']:
            if 'function' in c:
                context.info("Has functions, doesnt need a table")
                has_functions = True
            if 'column' in c:
                context.info("Has columns, needs a table")
                has_columns = True
        if False == has_columns and 'from' in query_object['meta']:
            raise Exception("Invalid FROM, all columns are functions")

        # if has functions, tables may not be needed
        if True == has_columns:
            if 'from' in query_object['meta']:
                table_name = query_object['meta']['from']['table']
                query_object['table'] = context.database.get(table_name)
                if None == query_object['table']:
                    raise Exception("Table '{0}' does not exist.".format(table_name))
                table_columns = query_object['table'].get_columns()
                parser.expand_columns(query_object, table_columns)
                column_len = query_object['table'].column_count()
                if column_len == 0:
                    raise Exception("No defined columns in configuration")
            else:
                raise Exception("Missing FROM in select")

        temp_table = context.database.temp_table()
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

        # TODO Columns with the same name can be renamed, but fail. Key issue?
        line_number = 1

        # create temp table structure
        # process file
        if True == has_columns:
            with open(query_object['table'].data.path, 'r') as content_file:
                for line in content_file:
                    processed_line = context.process_line(query_object, line, line_number)
                    if None != processed_line['error']:
                        temp_table.add_error(processed_line['error'])
                    line_number += 1

                    #print processed_line
                    if False == processed_line['match']:
                        continue
                    # line is added as is
                    if None != processed_line['data']:
                        temp_data.append( processed_line)

        # file is closed at this point
        if False == has_columns and True == has_functions:
            row=context.process_select_row(query_object,None)
            temp_data.append(row)


        if 'order by' in query_object['meta']:
            context.sort = []
            for c in query_object['meta']['order by']:
                ordinal = query_object['table'].get_ordinal_by_name(c['column'])
                direction = 1
                if 'asc' in c:
                    direction = 1
                elif 'desc' in c:
                    direction = -1
                context.sort.append([ordinal, direction])
            context.info(context.sort)
            temp_data = sorted(temp_data, context.sort_cmp)
            #print temp_data
        limit_start = 0
        limit_length = None
        #print query_object['meta']
        # exit(1)
        
        # now convert the columns into the correct format/order as in the select
        restructured_data=[]
        for line in temp_data:
            restructured_line = context.process_select_row(query_object,line) 
            restructured_data.append(restructured_line)
        temp_data=restructured_data

        # grouping happens after ordering and before limiting
        if distinct:
            group=[]
            for item in temp_data:
                no_item=True
                for group_item in group:
                    if context.compare_data(group_item['data'],item['data']):
                        no_item=None
                        break
                if no_item:
                    group.append(item)
            temp_data=group

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
       #
       

        if 'limit' in query_object['meta']:
            if 'start' in query_object['meta']['limit']:
                limit_start = query_object['meta']['limit']['start']
            if 'length' in query_object['meta']['limit']:
                limit_length = query_object['meta']['limit']['length']

        context.info("Limit:{0},Length:{1}".format(limit_start, limit_length))
        temp_table.results = context.limit(temp_data, limit_start, limit_length)
        return temp_table


def process_select_row(context,query_object,processed_line):
    row=[]
    for c in query_object['meta']['columns']:
        if 'column' in c:
            if None != processed_line:
                row.append(query_object['table'].get_data_by_name(c['column'], processed_line['data']))
        elif 'function' in c:
            if c['function'] == 'database':
                row.append(f_database(context.database))
            elif c['function'] == 'datetime':
                    row.append(f_datetime(context))
            elif c['function'] == 'date':
                    row.append(f_date(context))
            elif c['function'] == 'time':
                    row.append(f_time(context))
            elif c['function'] == 'version':
                    row.append(f_version(context,__version__))
            #elif c['function'] == 'lower':
            #     row.append(context.functions.lower(c['column']))
            #elif c['function'] == 'upper':
            #     row.append(context.functions.upper(c['column']))
            #elif c['function'] == 'cat':
            #     row.append(context.functions.cat(c['arg1'],c['arg2']))
    if None != processed_line:                    
        line_type=processed_line['type']
        error= processed_line['error']
        raw= processed_line['raw']
    else:
        line_type=context.data_type.DATA
        error= None
        raw= None
    return {'data': row, 'type': line_type, 'error': error, 'raw': raw}


def sort_cmp(context, x, y):

    for c in context.sort:
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
def limit(context, data_stream, index, length):
    if None == index:
        index = 0
    if None == length:
        length = len(data_stream) - index

    data_stream_lenght = len(data_stream)
    if index >= data_stream_lenght:
        #print("-Index is out of range for query. {} of {}".format(index,data_stream_lenght))
        return []
    if index + length > data_stream_lenght:
        #print("Length is out of range for query. {} of {}".format(length,data_stream_lenght))
        length = data_stream_lenght - index
    return data_stream[index:index + length]

def compare_data(context,data1, data2):
    if data1 is None or data2 is None:
        return None
    if (not isinstance(data1, dict)) or (not isinstance(data2, dict)):
        if len(data1)!=len(data2):
            return None;
        for index in range(0,len(data1)):
            if data1[index]!=data2[index]:
                return None
    else:
        shared_keys = set(data2.keys()) & set(data2.keys())
        if not ( len(shared_keys) == len(data1.keys()) and len(shared_keys) == len(data2.keys())):
            return None

        dicts_are_equal = True
        for key in data1.keys():
            if data1[key] != data2[key]:
                return None
    return True


