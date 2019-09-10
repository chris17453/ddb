# cython: profile=True
# cython: linetrace=True
# cython: binding=True

import os
import tempfile, shutil
from ..file_io.locking import lock
from pprint import pprint



def process_line(context, query_object, line, line_number=0,column_count=0,delimiter=',',visible_whitespace=None,visible_comments=None, visible_errors=None):
    err = None
    table=query_object['table']
    # TODO move rstrip to after split for limited data copy operations
    line_cleaned = line.rstrip()
    line_data = None
    cdef bool match_results=False
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


