# cython: profile=True
# cython: profile=True

import os
import tempfile, shutil
from ..file_io.locking import lock
from pprint import pprint


class debugger:
    def __init__(self,obj,name,depth=0):
        pad=''
        for i in range(0,depth):
            pad+=' '
        if depth==0:
            print ("\n\033[31;1;4mDebug: {0}\033[0m".format(name))

        variables = [i for i in dir(obj) if not i.startswith('__')]
        empty=[]
        var_count=0
        for var in variables:
            value=getattr(obj,var)
            if  isinstance(value,str):
                print("{2}{0} {1}".format(var+':',value,pad))
                var_count+=1
            elif  isinstance(value,int):
                print("{2}{0} {1}".format(var+':',value,pad))
                var_count+=1
            elif  isinstance(value,float):
                print("{2}{0} {1}".format(var+':',value,pad))
                var_count+=1
            elif isinstance(value,list):
                print ("{0}- {1} :".format(pad,var))
                for item in value:
                    var_count+=1
                    debugger(item,var,depth+4)
            elif callable(value):
                continue
            elif value==None:
                var_count+=1
                empty.append(var)
            else:
                var_count+=1
                print ("{0}- {1} :".format(pad,var))
                debugger(value,var,depth+4)
                
        if len(empty)>0:
            print ("{1}Empty Vars: {0}".format(",".join(empty),pad))
        #print variables
        if var_count==0:
            print("{2}{0} {1}".format("No attributes"+':',"",pad))


def process_line(context, query_object, line, line_number=0,column_count=0,delimiter=',',visible_whitespace=None,visible_comments=None, visible_errors=None):
    err = None
    table=query_object['table']
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
        if 'where' not in query_object['meta']:
            match_results = True
        else:
            # if a where, only return data, comments/whites/space/errors are ignored
            
            if line_type == context.data_type.DATA:
                match_results = context.match.evaluate_match(context,query_object, line_data)
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

    



def process_line3(context,meta, line, line_number=0,column_count=0,delimiter=',',visible_whitespace=None,visible_comments=None, visible_errors=None):
    
    
    print ("is instance:{0}".format(isinstance(line,str)))
    print ("is instance:{0}".format(isinstance(line,unicode)))

    if isinstance(line,str)==False:
        line=str(line)
    else:
        line=line.decode('ascii')
        
    err = None
    table=meta.table
    # TODO move rstrip to after split for limited data copy operations
    line_cleaned = line.rstrip()
    print("Line: {0}".format( type(line) ))
    print("Cleaned: {0}".format( type(line_cleaned) ))
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
        

        # If no where. return everything, not everythin has a where
        try:
            if not meta.where:
                match_results = True
            else:
                # if a where, only return data, comments/whites/space/errors are ignored
                
                if line_type == context.data_type.DATA:
                    match_results = match2().evaluate_match(meta=meta, row=line_data)
                else:
                    match_results = False
        except Exception as ex:
            context.info(__name__,ex)
            match_results = True
            
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




class query_results:
    def __init__(self,
                success=False,
                affected_rows=0,
                data=None,
                error=None,
                diff=None,
                total_data_length=0,
                delimiter=None,
                new_line=None,
                table=None,
                executed_query=None):

        self.success=success
        self.affected_rows=affected_rows
        self.data=[]
        self.diff=diff
        self.error=error
        self.data_length=0
        self.column_length=0
        self.total_data_length=0
        self.delimiter=delimiter
        self.new_line=new_line
        self.executed_query=executed_query
        self.table=table
        
        
        self.columns=[]

        if data and data.results:
            self.data=data.results
            self.data_length=len(data.results)

        if data:
            self.columns = data.get_columns_display()
            self.column_length=len(self.columns)
            
    def get_first(self):
        try:
            return self.data[0]['data'][0]
        except:
            pass
        return None

    def is_single(self):
        try:
            if len(self.data)==1:
                return True
        except:
            pass
        return None
    def debug(self):
        print("Query Results")
        debugger(self,"Query Results")
