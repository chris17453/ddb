import os

def process_line(context, query_object, line, line_number=0):
        err = None
        column_len = query_object['table'].column_count()
        line_cleaned = line.rstrip()
        line_data = None
        if query_object['table'].data.starts_on_line > line_number:
            line_type = context.data_type.COMMENT
            line_data = line
            #print query_object['table'].data.starts_on_line,line_number
        else:
            line_type = context.data_type.DATA
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
                match_results = context.match.evaluate_match(query_object['meta']['where'], line_data, query_object['table'])
            else:
                match_results = False
        if query_object['table'].visible.whitespace is False and line_type==context.data_type.WHITESPACE:
            match_results=False
        elif query_object['table'].visible.comments is False and line_type==context.data_type.COMMENT:
            match_results=False
        elif query_object['table'].visible.errors is False and line_type==context.data_type.ERROR:
            match_results=False


        # raw has rstrip for line.. maybe configuration option? Extra data anyway...
        return {'data': line_data, 'type': line_type, 'raw': line_cleaned, 'line_number': line_number, 'match': match_results, 'error': err}

  
def swap_files(target, temp):
    os.remove(target)
    if os.path.exists(target):
        raise Exception("Deleting target file {} failed".format(target))
    os.rename(temp, target)
    if os.path.exists(temp):
        raise Exception("Renaming temp file {} failed".format(temp))

class query_results:
    def __init__(self,success=False,affected_rows=0,data=None,error=None):
        self.success=success
        self.affected_rows=affected_rows
        self.data=data
        print(data)
        self.error=None
        print("Success: {0} Error:{1}".format(success,error))