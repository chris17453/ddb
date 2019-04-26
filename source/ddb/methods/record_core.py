import os
import tempfile, shutil
from ..file_io.locking import lock
from pprint import pprint


def process_line(context, query_object, line, line_number=0):
    err = None
    column_len = query_object['table'].column_count()
    line_cleaned = line.rstrip()
    line_data = None
    match_results=False
    if query_object['table'].data.starts_on_line > line_number:
        line_type = context.data_type.COMMENT
        line_data = line
        match=False
        #print query_object['table'].data.starts_on_line,line_number
    else:
        line_type = context.data_type.DATA
        match=True
    if match:

        if not line_cleaned:
            if True == query_object['table'].visible.whitespace:
                line_data = ['']
            line_type = context.data_type.WHITESPACE
        else:
            if line_cleaned[0] in query_object['table'].delimiters.comment:
                if True == query_object['table'].visible.comments:
                    line_data = [line_cleaned]
                line_type = context.data_type.COMMENT
            else:
                line_data = line_cleaned.split(query_object['table'].delimiters.field)
                cur_column_len = len(line_data)
                if cur_column_len != column_len:
                    if cur_column_len > column_len:
                        err = "Table {2}: Line #{0}, {1} extra Column(s)".format(line_number, cur_column_len - column_len, query_object['table'].data.name)
                    else:
                        err = "Table {2}: Line #{0}, missing {1} Column(s)".format(line_number, column_len - cur_column_len, query_object['table'].data.name)
                    # query_object['table'].add_error(err)
                    line_type = context.data_type.ERROR

                    # turn error into coment
                    if True == query_object['table'].visible.errors:
                        line_data = line_cleaned
                    else:
                        line_data = None
                    line_type = context.data_type.ERROR
                # fields are surrounded by something... trim
                #print context.table.delimiters.block_quote
                if None != query_object['table'].delimiters.block_quote:
                    line_data_cleaned = []
                    for d in line_data:
                        line_data_cleaned.append(d[1:-1])
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
        if query_object['table'].visible.whitespace is False and line_type==context.data_type.WHITESPACE:
            match_results=False
        elif query_object['table'].visible.comments is False and line_type==context.data_type.COMMENT:
            match_results=False
        elif query_object['table'].visible.errors is False and line_type==context.data_type.ERROR:
            match_results=False


    # raw has rstrip for line.. maybe configuration option? Extra data anyway...
    return {'data': line_data, 
            'type': line_type, 
            'raw': line_cleaned, 
            'line_number': line_number, 
            'match': match_results, 
            'error': err}

  
def create_temporary_copy(path,prefix):
    """ Create a copy of a regular file in a temporary directory """
    try:
        # dont over look this
        # it checks for a lock file in the temp dir
        # and blocks this thread/.process until MAX timout occures
        # or the lock ages and is deleted
        lock.aquire(path)



        temp_dir = tempfile.gettempdir()
        temp_base_name=next(tempfile._get_candidate_names())
        if prefix:
            temp_file_name="{0}".format(temp_base_name)
        else:
            temp_file_name="{0}_{1}".format(prefix,temp_base_name)
        
        temp_path = os.path.join(temp_dir, temp_file_name)
        shutil.copy2(normalize_path(path), temp_path)
         #print("Deleting: {0} Copying to Deleted: {1}".format(path,temp_path))
        return temp_path
    except Exception as ex:
        raise Exception("Temp File Error: {0}".format(ex))

def remove_temp_file(path):
    try:
        #print "Removing temp copy"
        os.remove(path)
        if os.path.exists(path):
            raise Exception("Failed to delete: {0}".format(path))    
    except Exception as ex:
        raise Exception("Temp File Error: {0}".format(ex))

        
# todo move into context with a manager flag        
def swap_files(path, temp):
    """ Swap a temporary file with a regular file, by deleting the regular file, and copying the temp to its location """
    try:
        #print("Swap File1")
        if None == lock.is_locked(path):
            raise Exception("Cannot swap files, expected lock. Didnt find one {0}".format(path))

        # DELETE ORIGINAL
        norm_path=normalize_path(path)
        if os.path.exists(norm_path):
            os.remove(norm_path)
        
        if os.path.exists(norm_path):
            raise Exception("Deleting file {0} failed".format(norm_path))
        
        # REMOVE LOCK FROM ORIGINAL PATH
        #print("Swap File2")
        lock.release(path)

        #if os.path.exists(temp):
        #    print ("Exists")
        shutil.copy2(temp, norm_path)
        #print  temp,path
        
        #os.remove(temp)
        #print("$Removed")
        #if os.path.exists(temp):
        #    raise Exception("Deleting temp file {0} failed".format(temp))
        
    except Exception as ex:
        raise Exception("File Error: {0}".format(ex))
 
def normalize_path(path):
    """Update a relative or user absed path to an ABS path"""
    normalized_path=os.path.abspath(os.path.expanduser(path))
    return normalized_path





class query_results:
    def __init__(self,success=False,affected_rows=0,data=None,error=None,diff=None,total_data_length=0):
        self.success=success
        self.affected_rows=affected_rows
        self.data=[]
        self.diff=diff
        self.error=error
        self.data_length=0
        self.column_length=0
        self.total_data_length=0
        
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
        #pprint(data)
        #print("Success: {0} Error:{1}".format(success,error))