import os
import json
import copy
from .parser.sql_parser  import sql_parser
from .formatting.colors import bcolors
from .structure.table import table
from .structure.database import database
from .structure.column import column_v2
from .evaluate.match import evaluate_match
from .functions import *
#from table import table
import tempfile


#
# Fix delete
# Add insert
# Fix errors
# Add Update

class sql_engine:
    def __init__(self,database_dir,query=None,debug=False):
     
        self.debug=debug
        self.results=None
        self.database=database(database_dir)
        if None !=query:
            self.query(query)
    
    #def set_configuration(self,database_instance):
    #    self.database=database
    #    if False == self.has_configuration():
    #        raise Exception("No configuration data")
    
    def has_configuration(self):
        if None==self.database:
            return False
        table_count=self.database.count()
        if table_count==0:
            return False
        return True

    def query(self,sql_query):
        if False==self.has_configuration():
            raise Exception("No table found")
        
        query_object=sql_parser(self.database,sql_query,self.debug)
        if None == query_object.mode:
            raise Exception ("Invalid SQL")
        
        if query_object.source!=None:
            self.table=self.database.get(query_object.source)

        
        
        #get columns, doesnt need a table
        if query_object.mode=="show":
            if query_object.show=="tables":
                self.results=show_tables(self.database)    
            if query_object.show=="columns":
            # items below need a table
                self.results=show_columns(self.database,self.table)
            if query_object.show=="errors":
                self.results=show_errors(self.database,self.table)

        if query_object.mode=='select':
            self.results=self.select(query_object)
           
        if query_object.mode=='delete':
            self.results=self.delete(query_object)
        if None != self.results:
            return self.results #TODO Fix
        return []
    


    def limit(self,data_stream,index,length):
        if None == index:
            index=0
        if None == length:
            length=len(data_stream)-index
            
        data_stream_lenght=len(data_stream)
        if index>=data_stream_lenght:
            print("Index is out of range for query. {} of {}".format(index,data_stream_lenght))
            return []
        if index+length>=data_stream_lenght:
            print("Length is out of range for query. {} of {}".format(length,data_stream_lenght))
            length=data_stream_lenght-index
        return data_stream[index:index+length]

    def process_line(self,query_object,line,line_number=0):
        column_len=len(self.table.columns)
        line_cleaned=line.rstrip()
        line_data=None
        if self.table.data.starts_on_line<line_number:
            line_type='comment'
        else:
            line_type='data'
        if not line_cleaned.rstrip():
            if True == self.table.visible.whitespace:
                line_data=['']
            line_type='whitespace'
        else:
            if line_cleaned[0] in self.table.delimiters.comment:
                if True == self.table.visible.comments:
                    line_data=[line_cleaned]
                line_type='comments'
            else:
                line_data=line_cleaned.split(self.table.delimiters.field)
                cur_column_len=len(line_data)
                if cur_column_len!=column_len:
                    if cur_column_len>column_len:
                        err="Table {2}: Line #{0}, {1} extra Column(s)".format(line_number,cur_column_len-column_len,self.table.data.name)
                    else:
                        err="Table {2}: Line #{0}, missing {1} Column(s)".format(line_number,column_len-cur_column_len,self.table.data.name)
                    self.table.add_error(err)
                    
                    #turn error into coment
                    if True == self.table.visible.errors:
                        line_data=line_cleaned
                    else:
                        line_data=None
                    line_type='error'
                # fields are surrounded by something... trim
                #print self.table.delimiters.block_quote
                if None != self.table.delimiters.block_quote:
                    line_data_cleaned=[]
                    for d in line_data:
                        line_data_cleaned.append(d[1:-1])
                    line_data=line_data_cleaned

        match_results=evaluate_match(query_object.where,line_data,self.table)
                    
        return {'data':line_data,'type':line_type,'raw':line,'line_number':line_number,'match':match_results}
   
    def select(self,query_object):
        try:
            #where_count=len(query_object.where)
            temp_data=[]
            column_len=self.table.column_count()
            if column_len==0:
                raise Exception("No defined columns in configuration")
         
            temp_table=self.database.temp_table()
            for c in  query_object.columns:
                temp_table.add_column(c['name'],c['display'])

               
            line_number=1
        
            # create temp table structure
            # process file
            with open(self.table.data.path, 'r') as content_file:
                for line in content_file:
                    processed_line=self.process_line(query_object,line,line_number)
                    line_number+=1
                    
                    #print processed_line
                    if False == processed_line['match']:
                        continue

                    # add to temp table
                    if None != processed_line['data']:
                        restructured_line=[]
                        for c in query_object.columns:
                            restructured_line.append(self.table.get_data_by_name(c['name'],processed_line['data']))
                        temp_data.append(restructured_line)
            
        
            # filter temp table
            temp_table.results=self.limit(temp_data,query_object.limit_start,query_object.limit_length)
            return temp_table
        except Exception as ex:
            
            print (ex)
            #exit(1)


    # creates a tempfile 
    # puts the raw original lines in temp file
    # ignores matches
    # File is as untouched as possible
    def delete(self,query_object):
        try:
            column_len=self.table.column_count()
            if column_len==0:
                raise Exception("No defined columns in configuration")
            temp_file_name = next(tempfile._get_candidate_names())
            line_number=1
            # process file
            with open(self.table.data.path, 'r') as content_file:
                with open(temp_file_name, 'w') as temp_file:
                    for line in content_file:
                        processed_line=self.process_line(query_object,line,line_number)
                        line_number+=1
                        #skip matches
                        if True  == processed_line['match']:
                            continue
                        temp_file.write(processed_line['raw'])
            
            
            os.remove(self.table.data.path)
            os.rename(temp_file_name,self.table.data.path)
        
        except Exception as ex:
            
            print (ex)
            #exit(1)

    
    


  
                





    
