# cython: profile=True
# cython: linetrace=True
# cython: binding=True

import os
import tempfile, shutil
from ..file_io.locking import lock
from pprint import pprint


class match():

    def evaluate_single_match(self,context,test, row, table):
        
        compare1 = None
        compare2 = None
        compare1_is_column = False
        compare2_is_column = False

        comparitor = test['c']
        #cdef int index 
        #cdef str like = None
        #cdef str data = None

        # if None !=comparitor:
        #   comparitor=comparitor.lower()
        for column in table.columns:
            #print column.data.name
            if column.data.name == test['e1']:
                index = table.ordinals[column.data.name]
                #print "found1", column.data.name
                compare1 = row[index]  # table.ordinals[].get_data_from_column(column,row)
                # compare1=table.get_data_from_column(column,row)
                compare1_is_column = True
            elif column.data.name == test['e2']:
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
            compare1 = test['e1']
        if None == compare2:
            compare2 = test['e2']
        
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


    def evaluate_match(self,context,query_object, row):
        #print where
        table=query_object['table']
        where=query_object['meta']['where']
        if None == row:
            return False

        success = None
        skip_section = False
        operation = ""
        for test in where:
            #print test
            # if a evaluation chain failed, continue until out of that section
            if 'and' in test and skip_section:
                continue
            else:
                skip_section = False

            operation = None
            if 'where' in test:
                operation = 'where'

            elif 'or' in test:
                operation = 'or'
                if success:
                    return True

            elif 'and' in test:

                operation = 'and'
                if not success:
                    skip_section = True
                    continue

            test_operation = test[operation]
            success = self.evaluate_single_match(context,test_operation, row, table)

        # never matched anytthing...
        if success is None:
            return False
        return success


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
        match=False
        #print table.data.starts_on_line,line_number
    else:
        line_type = context.data_type.DATA
        match=True
    if match:
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
                match_results = match().evaluate_match(context,query_object, line_data)
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




class query_results:
    def __init__(self,success=False,affected_rows=0,data=None,error=None,diff=None,total_data_length=0,delimiter=None,new_line=None):
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
        pprint.pprint(self.error)
        pprint.pprint(self.data)
        #print("Success: {0} Error:{1}".format(success,error))