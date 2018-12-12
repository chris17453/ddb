import os
import json
import copy
import operator
import flextable
import tempfile  #from table import table
from parser.sql_parser  import sql_parser
from structure.table import table
from structure.database import database
from structure.column import column_v2
from evaluate.match import evaluate_match
from functions import functions


#

debug_on=False
def info(msg,arg1=None,arg2=None,arg3=None):
    if True == debug_on:
        print(msg,arg1,arg2,arg3)

# Fix delete
# Add insert
# Fix errors
# Add Update

def enum(**enums):
    return type('Enum', (), enums)


class sql_engine:
    data_type=enum(COMMENT=1,ERROR=2,DATA=3,WHITESPACE=4)

    def __init__(self,database_dir=None,config_file=None,query=None,debug=False,mode='array'):
        global debug_on
        debug_on=debug
        self.debug=debug
        self.results=None
        self.mode=mode
        self.database=database(directory=database_dir,config_file=config_file)
        self.current_database=self.database.get_default_database()
        if None !=query:
            self.query(query)
    
    #def set_configuration(self,database_instance):
    #    self.database=database
    #    if False == self.has_configuration():
    #        raise Exception("No configuration data")


    def debugging(self,debug=False):
        self.debug=debug
    
    
    def define_table(self,table_name,database_name,columns,data_file,field_delimiter=None):
        """Progromatically define a table. Not saved to a configuration file, unless manualy activated"""
        t=table(database=database_name,columns=columns,name=table_name,data_file=data_file,field_delimiter=field_delimiter)
        self.database.tables.append(t)


    def has_configuration(self):
        if None==self.database:
            return False
        # table count invalid.. we may add some
        #table_count=self.database.count()
        #if table_count==0:
        #    return False
        return True

    def query(self,sql_query):
        if False==self.has_configuration():
            raise Exception("No table found")
        self.results=None
        
        # update table info...
        # it may have changed...
        self.database.reload_config()
        
        parser=sql_parser(sql_query,self.debug)
        if False == parser.query_objects:
            raise Exception ("Invalid SQL")
      
        for query_object in parser.query_objects:
            
            info("query_object",query_object)
            #print  query_object
            #exit(9)
            #get columns, doesnt need a table
            #print query_object['mode']
            if query_object['mode']=="show tables":

                self.results=functions.show_tables(self.database)    
            if query_object['mode']=="show columns":
                self.results=functions.show_columns(self.database,query_object)
            #if query_object['mode']=="show errors":
            #    self.results=show_errors(self.database,self.table)
            #print query_object
            if query_object['mode']=='select':
                self.results=self.select(query_object,parser)

            if query_object['mode']=='insert':
                self.results=self.insert(query_object)

            if query_object['mode']=='update':
                self.results=self.update(query_object)
            
            if query_object['mode']=='delete':
                self.results=self.delete(query_object)

            if query_object['mode']=='use':
                self.results=self.use(query_object)

            if query_object['mode']=='drop table':
                self.results=self.drop_table(query_object)

            if query_object['mode']=='create table':
                self.results=self.create_table(query_object)
        
        #only return last command
        if None != self.results:
            if self.mode=='full':
                return self.results 
            
            #if the result set it not empty
            if None !=self.results.results:
                if self.mode=='array':
                    new_array=[]
                    for line in self.results.results:
                        new_array.append(line['data'])
                    return new_array

                if self.mode=='object':
                    new_array=[]
                    columns=self.results.get_columns()
                    len_col=len(columns)
                    for line in self.results.results:
                        new_dict={}
                        for i in range(0,len_col):
                            if len(line['data'])<i:
                                break
                            new_dict[columns[i]]=line['data'][i]
                        new_array.append(new_dict)
                    return new_array 

        return None
    

    def change_database(self,database_name):
        query="use {}".format(database_name)
        results=self.query(query)
        if None==results:
            return False
        return True


    def limit(self,data_stream,index,length):
        try:
            if None == index:
                index=0
            if None == length:
                length=len(data_stream)-index
                
            data_stream_lenght=len(data_stream)
            if index>=data_stream_lenght:
                #print("-Index is out of range for query. {} of {}".format(index,data_stream_lenght))
                return []
            if index+length>data_stream_lenght:
                #print("Length is out of range for query. {} of {}".format(length,data_stream_lenght))
                length=data_stream_lenght-index
            return data_stream[index:index+length]
        except Exception as ex:
            info("Limit",ex)

    def process_line(self,query_object,line,line_number=0):
        err=None
        column_len=query_object['table'].column_count()
        line_cleaned=line.rstrip()
        line_data=None
        if query_object['table'].data.starts_on_line>line_number:
            line_type=self.data_type.COMMENT
            line_data=line
            #print query_object['table'].data.starts_on_line,line_number
        else:
            line_type=self.data_type.DATA
        if not line_cleaned:
            if True == query_object['table'].visible.whitespace:
                line_data=['']
            line_type=self.data_type.WHITESPACE
        else:
            if line_cleaned[0] in query_object['table'].delimiters.comment:
                if True == query_object['table'].visible.comments:
                    line_data=[line_cleaned]
                line_type=self.data_type.COMMENT
            else:
                line_data=line_cleaned.split(query_object['table'].delimiters.field)
                cur_column_len=len(line_data)
                if cur_column_len!=column_len:
                    if cur_column_len>column_len:
                        err="Table {2}: Line #{0}, {1} extra Column(s)".format(line_number,cur_column_len-column_len,query_object['table'].data.name)
                    else:
                        err="Table {2}: Line #{0}, missing {1} Column(s)".format(line_number,column_len-cur_column_len,query_object['table'].data.name)
                    #query_object['table'].add_error(err)
                    line_type=self.data_type.ERROR
                    
                    #turn error into coment
                    if True == query_object['table'].visible.errors:
                        line_data=line_cleaned
                    else:
                        line_data=None
                    line_type=self.data_type.ERROR
                # fields are surrounded by something... trim
                #print self.table.delimiters.block_quote
                if None != query_object['table'].delimiters.block_quote:
                    line_data_cleaned=[]
                    for d in line_data:
                        line_data_cleaned.append(d[1:-1])
                    line_data=line_data_cleaned

        #If no where. return everything
        if 'where' not in query_object['meta']:
            match_results=True
        else:
            # if a where, only return data, comments/whites/space/errors are ignored
            if line_type==self.data_type.DATA:
                match_results=evaluate_match(query_object['meta']['where'],line_data,query_object['table'])
            else:
                match_results=False
        
        return {'data':line_data,'type':line_type,'raw':line,'line_number':line_number,'match':match_results,'error':err}
   
    def select(self,query_object,parser):
        #try:
            temp_data=[]
            #if has columns, then it needs a table
            
            has_functions=False
            has_columns=False
            for c in query_object['meta']['select']:
                if 'function' in  c:
                    info("Has functions, doesnt need a table")
                    has_functions=True
                if 'column' in c:
                    info("Has columns, needs a table")
                    has_columns=True
            if False == has_columns and 'from' in query_object['meta']:
                raise Exception("Invalid FROM, all columns are functions")

                
            # if has functions, tables may not be needed
            if True == has_columns:
                if 'from' in  query_object['meta']:
                    table_name=query_object['meta']['from']['table']
                    query_object['table']=self.database.get(table_name)
                    if None ==query_object['table']:
                        raise Exception("invalid table {}".format(table_name))
                    table_columns=query_object['table'].get_columns()                      
                    parser.expand_columns(query_object,table_columns)
                    column_len=query_object['table'].column_count()
                    if column_len==0:
                        raise Exception("No defined columns in configuration")
                else:
                    raise Exception("Missing FROM in select")

            temp_table=self.database.temp_table()
            for column in  query_object['meta']['select']:
                display=None
                if 'display' in column:
                    display=column['display']
                
                if 'column' in column:
                    temp_table.add_column(column['column'],display)
                if 'function' in column:
                    temp_table.add_column(column['function'],display)
                

            
            line_number=1
        
            # create temp table structure
            # process file
            if True == has_columns:
                with open(query_object['table'].data.path, 'r') as content_file:
                    for line in content_file:
                        processed_line=self.process_line(query_object,line,line_number)
                        if None != processed_line['error']:
                            temp_table.add_error(processed_line['error'])
                        line_number+=1
                        
                        #print processed_line
                        if False == processed_line['match']:
                            continue

                        # add to temp table
                        if None != processed_line['data']:
                            restructured_line=[]
                            for c in query_object['meta']['select']:
                                if 'column' in c:
                                    restructured_line.append(query_object['table'].get_data_by_name(c['column'],processed_line['data']))
                                if 'function' in c:
                                    if c['function']=='database':
                                        restructured_line.append(functions.database(self.database))

                            temp_data.append({'data':restructured_line,'type':processed_line['type'],'error':processed_line['error'],'raw':processed_line['raw']})
                
            # file is closed at this point

            if False==has_columns and True == has_functions:
                row=[]
                for c in query_object['meta']['select']:
                    if 'function' in c:
                        if c['function']=='database':
                            row.append(functions.database(self.database))
                temp_data=[row]

            if 'order by' in  query_object['meta']:
                self.sort=[]
                for c in  query_object['meta']['order by']:
                    ordinal=query_object['table'].get_ordinal_by_name(c['column'])
                    direction=1
                    if 'asc' in c:
                        direction=1
                    if 'desc' in c:
                        direction=-1 
                    self.sort.append([ordinal,direction])
                temp_data=sorted(temp_data,self.sort_cmp)
                #print temp_data

            limit_start=0
            limit_length=None
            #print query_object['meta']
            #exit(1)

            if 'limit' in query_object['meta']:
                if 'start' in query_object['meta']['limit']:
                    limit_start=query_object['meta']['limit']['start']
                if 'length' in query_object['meta']['limit']:
                    limit_length=query_object['meta']['limit']['length']


            
            temp_table.results=self.limit(temp_data,limit_start,limit_length)
            return temp_table
        #except Exception as ex:
            
        #    print ("Select",ex)
            #exit(1)
    
    
    def sort_cmp(self,x,y):

        for c in self.sort:
            ordinal=c[0]
            direction=c[1]

            #convert = lambda text: int(text) if text.isdigit() else text
            #alphanum_key = lambda key: [convert(c) for c in re.split('([0-9]+)', key)]


            #%print x[ordinal],y[ordinal],-1
            if x['data'][ordinal]==y['data'][ordinal]:
                continue
            
            if x['data'][ordinal]<y['data'][ordinal]:
                return -1*direction
            else:
                return 1*direction
        return 0




    # creates a tempfile 
    # puts the raw original lines in temp file
    # ignores matches
    # File is as untouched as possible
    def delete(self,query_object):
        try:
            table_name=query_object['meta']['from']['table']
            query_object['table']=self.database.get(table_name)

            temp_table=self.database.temp_table()
            temp_table.add_column('deleted')

            temp_file_name = next(tempfile._get_candidate_names())
            line_number=1
            deleted=0
            # process file
            with open(query_object['table'].data.path, 'r') as content_file:
                with open(temp_file_name, 'w') as temp_file:
                    for line in content_file:
                        processed_line=self.process_line(query_object,line,line_number)
                        if None != processed_line['error']:
                            temp_table.add_error(processed_line['error'])
                        line_number+=1
                        #skip matches
                        if True  == processed_line['match']:
                            deleted+=1
                            continue
                        temp_file.write(processed_line['raw'])
            
            data= {'data':[deleted],'type':self.data_type.DATA,'error':None}
            temp_table.append_data(data)
            os.remove(query_object['table'].data.path)
            os.rename(temp_file_name,query_object['table'].data.path)
            return temp_table
        
        except Exception as ex:
            
            print (ex)

    
    # creates a tempfile 
    # puts the raw original lines in temp file
    # File is as untouched as possible
    # new lines are joined at the end
    def insert(self,query_object):
        try:
            table_name=query_object['meta']['into']['table']
            query_object['table']=self.database.get(table_name)

            temp_table=self.database.temp_table()
            temp_table.add_column('inserted')

            temp_file_name = next(tempfile._get_candidate_names())
            line_number=1
            inserted=0
            # process file
            requires_new_line=False
            with open(query_object['table'].data.path, 'r') as content_file:
                with open(temp_file_name, 'w') as temp_file:
                    for line in content_file:
                        processed_line=self.process_line(query_object,line,line_number)
                        if None != processed_line['error']:
                            temp_table.add_error(processed_line['error'])
                        line_number+=1
                        temp_file.write(processed_line['raw'])
                        if processed_line['raw'][-1]==query_object['table'].delimiters.new_line:
                            requires_new_line=False
                        else: 
                            requires_new_line=True

                    results=self.create_single(query_object,temp_file,temp_table,requires_new_line)
                    if True==results:
                        inserted+=1

            
            data= {'data':[inserted],'type':self.data_type.DATA,'error':None}
            temp_table.append_data(data)
            os.remove(query_object['table'].data.path)
            os.rename(temp_file_name,query_object['table'].data.path)
            #print temp_table.errors
            return temp_table
        
        except Exception as ex:
            
            print (ex)    


    def create_single(self,query_object,temp_file,temp_table,requires_new_line):
        err=False
        ### 
        # insert new data at end of file
        if len(query_object['meta']['columns']) != query_object['table'].column_count():
            temp_table.add_error("Cannot insert, column count does not match table column count")
        else:
            if len(query_object['meta']['values']) != query_object['table'].column_count():
                temp_table.add_error("Cannot insert, column value count does not match table column count")
            else:
                new_line=''
                err=False
                #print query_object['meta']['columns']
                for c in range(0,len(query_object['meta']['columns'])):
                    column_name=query_object['table'].get_column_at_data_ordinal(c)
                    found=False
                    for c2 in range(0,len(query_object['meta']['columns'])):
                        if query_object['meta']['columns'][c2]['column']==column_name:
                            #print("Column {} at table index {} located at query index {}".format(column_name,c, c2))
                            found=True
                            if c>0:
                                new_line+='{}'.format(query_object['table'].delimiters.field)    
                            new_line+='{}'.format(query_object['meta']['values'][c2]['value'])
                    if False==found:
                        temp_table.add_error("Cannot insert, column in query not found in table: {}".format(column_name))
                        err=True
                        break
                if False == err:
                    #print new_line
                    if True == requires_new_line:
                        temp_file.write(query_object['table'].delimiters.new_line)
                    temp_file.write(new_line+query_object['table'].delimiters.new_line)
        if False==err:
            return True
        else:
            return False
        

    def update_single(self,query_object,temp_file,temp_table,requires_new_line,processed_line):
        err=False
        ### 
        # insert new data at end of file
        new_line=''
        err=False
        #print query_object['meta']['columns']

        # make sure the inserted columns exist
        for c2 in range(0,len(query_object['meta']['set'])):
            column_name=query_object['meta']['set'][c2]['column']
            if None == query_object['table'].get_column_by_name(column_name):
                temp_table.add_error("column in update statement does not exist in table: {}".format(column_name))
                #print "no column"
                err=True
                
        if False==err:
            for c in range(0,query_object['table'].column_count()):
                column_name=query_object['table'].get_column_at_data_ordinal(c)
                value=processed_line['data'][c]
                for c2 in range(0,len(query_object['meta']['set'])):
                    #print column_name,query_object['meta']['set']
                    if query_object['meta']['set'][c2]['column']==column_name:
                        #print("Column {} at table index {} located at query index {}".format(column_name,c, c2))
                        value=query_object['meta']['set'][c2]['expression']
                if c>0:
                    new_line+='{}'.format(query_object['table'].delimiters.field)    
                new_line+='{}'.format(value)
            #print new_line,value

         
        if False == err:
            #print new_line
            if True == requires_new_line:
                temp_file.write(query_object['table'].delimiters.new_line)
            temp_file.write(new_line+query_object['table'].delimiters.new_line)
        if False==err:
            return True
        else:
            return False
        



    # creates a tempfile 
    # puts the raw original lines in temp file
    # ignores matches
    # File is as untouched as possible
    def update(self,query_object):
        try:
            table_name=query_object['meta']['update']['table']
            query_object['table']=self.database.get(table_name)

            temp_table=self.database.temp_table()
            temp_table.add_column('updated')

            temp_file_name = next(tempfile._get_candidate_names())
            line_number=1
            updated=0
            # process file
            with open(query_object['table'].data.path, 'r') as content_file:
                with open(temp_file_name, 'w') as temp_file:
                    for line in content_file:
                        processed_line=self.process_line(query_object,line,line_number)
                        if None != processed_line['error']:
                            temp_table.add_error(processed_line['error'])
                        line_number+=1
                        #skip matches
                        if True  == processed_line['match']:
                            results=self.update_single(query_object,temp_file,temp_table,False,processed_line)
                            if True==results:
                                updated+=1
                            continue
                        temp_file.write(processed_line['raw'])
            data= {'data':[updated],'type':self.data_type.DATA,'error':None}

            temp_table.append_data(data)
            os.remove(query_object['table'].data.path)
            os.rename(temp_file_name,query_object['table'].data.path)
            return temp_table
        
        except Exception as ex:
            
            print (ex)


    def use(self,query_object):
        info("Use")
        target_db=query_object['meta']['use']['table']
        self.database.set_database(target_db)
        temp_table=self.database.temp_table()
        temp_table.add_column('changed_db')
        data= {'data':[target_db],'type':self.data_type.DATA,'error':None}
        temp_table.append_data(data)
        return temp_table                

    
    def create_table(self,query_object):
        info("Create Table")
        temp_table=self.database.temp_table()
        
        columns=[]
        for c in query_object['meta']['columns']:
            columns.append(c['column'])
        info("Columns to create",columns)
        created=0
        results=self.database.create_table( table_name=query_object['meta']['create']['table'],
                                            columns=columns,
                                            data_file=query_object['meta']['file']['file'])
        if True == results:
            created+=1

        temp_table.add_column('create table')
        data= {'data':[created],'type':self.data_type.DATA,'error':None}
        temp_table.append_data(data)
        return temp_table


    def drop_table(self,query_object):
        info("Drop Table")
        temp_table=self.database.temp_table()
        #print "dropping",parser.query_object['meta']['drop']['table']
        dropped=0
        results=self.database.drop_table(table_name=query_object['meta']['drop']['table'])
        if True==results:
            dropped+=1
        
        temp_table.add_column('dropped')
        data= {'data':[dropped],'type':self.data_type.DATA,'error':None}
        temp_table.append_data(data)
        return temp_table
  
                





    
