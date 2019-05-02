import os
import time
import pprint
from .lexer.lexer import lexer
from .configuration.table import table
from .configuration.database import database
from .evaluate.match import match
from .version import __version__

#methods -> actions

# system level commands
from .methods.system_set import method_system_set
from .methods.system_begin import method_system_begin
from .methods.system_commit import method_system_commit
from .methods.system_rollback import method_system_rollback
from .methods.system_show_variables  import method_system_show_variables
from .methods.system_show_tables import method_system_show_tables
from .methods.system_show_columns import method_system_show_columns
from .methods.system_show_output_modules import method_system_show_output_modules

# database level data methods
from .methods.database_use import method_use
from .methods.database_show_errors import method_show_errors

# table level structure methods
from .methods.table_create import method_create_table
from .methods.table_update import method_update_table
from .methods.table_describe import method_describe_table
from .methods.table_drop import method_drop_table

# table level data methods
from .methods.record_insert import method_insert 
from .methods.record_select import method_select
from .methods.record_update import method_update
from .methods.record_upsert import method_upsert
from .methods.record_delete import method_delete
from .methods.record_core import query_results
from .file_io.locking import lock,create_temporary_copy, swap_files, remove_temp_file

def enum(**enums):
    return type('Enum', (), enums)


class engine:
    """A serverless flat file database engine"""
    

    
    def info(self,msg, arg1=None, arg2=None, arg3=None):
        if True == self.debug:
            if isinstance(arg1,str) :
                print(msg, arg1, arg2, arg3)
            elif isinstance(arg1,object) :
                print(msg, arg2, arg3)
                pp = pprint.PrettyPrinter(indent=4)
                pp.pprint(arg1)
            else:    
                print(msg, arg1, arg2, arg3)

    
   
    def __init__(self, config_file=None, query=None, debug=False, mode='array',output='TERM',output_style='single',readonly=None,output_file=None):
        # if false, load nothing, if true, load form user dir
        if config_file is None:
            home = os.path.expanduser("~")
            config_file = os.path.join(os.path.join(home, '.ddb'), 'ddb.conf')
    

        self.data_type = enum(COMMENT=1, ERROR=2, DATA=3, WHITESPACE=4)
        self.debug = debug
        self.results = None
        self.mode = mode
        self.output=output
        self.output_file=output_file
        self.match=match()
        self.system={}
        self.system_trigger={}
        self.internal={}
        self.internal={'READONLY':readonly,'TEMP_FILES':{}}
        # variables that can be set by the system
        
        self.system['DEBUG']=False
        self.system['AUTOCOMMIT']=True
        self.system['OUTPUT_MODULE']=output
        self.system['OUTPUT_STYLE']=output_style
        self.internal['OUTPUT_MODULES']=[
            {'name':'bash','styles':[]},
            {'name':'term','styles':['single','double','rst','time']},
            {'name':'raw' ,'styles':[]},
            {'name':'yaml','styles':[]},
            {'name':'json','styles':[]},
            {'name':'xml' ,'styles':[]}]
        #auto functions ran when a variable is set
        self.system_trigger['DEBUG']=self.trigger_debug
        self.system['DELIMITER']=';'
        
        self.user={}
        self.internal['IN_TRANSACTION']=0
        try:        
            # print "Config",config_file
            self.database = database(config_file=config_file)
            self.current_database = self.database.get_default_database()
            # load tables
            # dont load empty stuff
            if config_file!=False:
                queries=self.database.get_db_sql()
                if queries:
                    self.query(queries)
        except Exception as ex:
            pass

        if None != query:
            self.query(query)
        
    # def set_configuration(self,database_instance):
    #    self.database=database
    #    if False == self.has_configuration():
    #        raise Exception("No configuration data")
    def init_state_variables(self):
        self.internal['row']=0

    def trigger_debug(self):
        self.debug=self.system['DEBUG']
        self.database.debug=self.debug
        

    def debugging(self, debug=False):
        self.debug = debug

    def define_table(self, table_name, database_name, columns, data_file, field_delimiter=None,data_starts_on=None):
        """Progromatically define a table. Not saved to a configuration file, unless manualy activated"""
        t = table(database=database_name, columns=columns, name=table_name, data_file=data_file, field_delimiter=field_delimiter,data_on=data_starts_on)
        self.database.tables.append(t)

    def has_configuration(self):
        if None == self.database:
            return False
        # table count invalid.. we may add some
        # table_count=self.database.count()
        # if table_count==0:
        #    return False
        return True

    def query(self, sql_query):
        try:
            start = time.perf_counter()
            wall_start = time.perf_counter()
        except:
            start = time.clock()
            wall_start = time.time()
            
            pass
        self.results = None
        if False == self.has_configuration():
            raise Exception("No table found")
        # update table info...
        # it may have changed...
        # self.database.reload_config()
        parser = lexer(sql_query)
        if False == parser.query_objects:
            raise Exception("Invalid SQL")

        for query_object in parser.query_objects:
            # clear all per state variables per run
            self.init_state_variables()
            
            self.info("Engine: query_object", query_object)
            #print  query_object
            # exit(9)
            # get columns, doesnt need a table
            # print query_object['mode']
            mode=query_object['mode']
            
            # RECORDS
            if mode == 'select':
                self.results = method_select(self,query_object, parser)
            
            elif mode == 'insert' and self.internal['READONLY']==None:
                self.results = method_insert(self,query_object)

            elif mode == 'update' and self.internal['READONLY']==None:
                self.results = method_update(self,query_object)

            elif mode == 'upsert' and self.internal['READONLY']==None:
                self.results = method_upsert(self,query_object)
            
            elif mode == 'delete' and self.internal['READONLY']==None:
                self.results = method_delete(self,query_object)

            elif mode == 'use':
                self.results = method_use(self,query_object)

            # TABLE 
            elif mode == 'drop' and self.internal['READONLY']==None:
                self.results = method_drop_table(self,query_object)

            elif mode == 'create' and self.internal['READONLY']==None:
                self.results = method_create_table(self,query_object)

            elif mode == 'update table' and self.internal['READONLY']==None:
                self.results = method_update_table(self,query_object)

            # SYSTEM 
            elif mode == 'set':
                self.results = method_system_set(self,query_object)

            elif mode == 'begin':
                self.results = method_system_begin(self,query_object)

            elif mode == 'rollback':
                self.results = method_system_rollback(self,query_object)

            elif mode == 'commit':
                self.results = method_system_commit(self,query_object)

            elif mode == "show tables":
                self.results = method_system_show_tables(self,self.database)

            elif mode == "show output modules":
                self.results = method_system_show_output_modules(self,query_object)

            elif mode == "show columns":
                self.results = method_system_show_columns(self,self.database, query_object)

            elif mode == "show variables":
                self.results = method_system_show_variables(self, query_object)
            elif mode == "describe table":
                self.results = method_describe_table(self, query_object)

            if False==self.results.success:

                break
            #if mode=="show errors":
            #    self.results=method_show_errors(self,self.database,self.table)
            #else:
            # TODO uncaught    
            #    print (query_object)
        # only return last command
        if self.results:
            if self.results.data:
                if self.mode == 'object':
                    columns = self.results.columns
                    len_col = len(columns)
                    for line in self.results.data:
                        # dont expand things that arn't data
                        if line['type']==self.data_type.DATA:
                            new_dict = {}
                            for i in range(0, len_col):
                                if len(line['data']) < i:
                                    break
                                new_dict[columns[i]] = line['data'][i]
                            line['data']=new_dict
        #except Exception as Ex:
        #    print  Ex
        #    pass
        if None == self.results:
            self.results=query_results()
            
            

        try:
            end = time.perf_counter()
            self.results.wall_end = time.time()
        except:
            end = time.clock()
            self.results.wall_end = time.time()
            pass
        
        self.results.start_time=start
        self.results.end_time=end
        self.results.time=end-start
        self.results.wall_start=wall_start
        self.results.wall_time=self.results.wall_start-self.results.wall_end
        #print(start,end)
        return self.results

    def change_database(self, database_name):
        query = "use {0}".format(database_name)
        results = self.query(query)
        if None == results:
            return False
        return True
        
    def add_error(self,error):
        self.info(error)
    
    def get_data_file(self,table,prefix="ddb_"):
        data_file=table.data.path
        if data_file not in self.internal['TEMP_FILES']:
            temp_data_file=create_temporary_copy(data_file,prefix)
            self.internal['TEMP_FILES'][data_file]={'origin':data_file,'temp_source':temp_data_file,'written':None,'dest':None}
        print(self.internal['TEMP_FILES'][data_file])
        return self.internal['TEMP_FILES'][data_file]['temp_source']
    
    def autocommit_write(self,table,dest_file):
        table_key=table.data.path
        if table_key in self.internal['TEMP_FILES']:
            self.internal['TEMP_FILES'][table_key]['written']=True
            self.internal['TEMP_FILES'][table_key]['dest']=dest_file
            print(self.internal['TEMP_FILES'][table_key])
        
        
    def auto_commit(self,table):
        self.commit()

    def commit(self):
        for table in self.internal['TEMP_FILES']:
            print table,self.internal['TEMP_FILES'][table]
            continue
            # every write action updates the original files and clears all temp files
            table_key=table.data.path

            if table_key in self.internal['TEMP_FILES']:
                temp_file=self.internal['TEMP_FILES'][table_key]
                destination_file=temp_file['dest']
                if self.system['AUTOCOMMIT']==True:
                    # no need to swap files if nothing was written yea? Just delete the temp data
                    if None== temp_file['written']:
                        lock.release(table_key)
                        print(self.internal['TEMP_FILES'][table_key])
                        remove_temp_file(temp_file['temp_source'])
                    else:
                        remove_temp_file(temp_file['temp_source'])
                        swap_files(table_key, destination_file)
                    del self.internal['TEMP_FILES'][table_key]
                # ok we may be doing multiple inserts to the same file or many files..
                else:
                    # swap temp READ file for newly WRITTEN file, delete the first read file
                    # if no file given do nothing... select passthrough
                    if destination_file:
                        print(self.internal['TEMP_FILES'][table_key])

                        #remove_temp_file(temp_file['path'])
                        self.internal['TEMP_FILES'][table_key]['temp_source']=self.internal['TEMP_FILES'][table_key]['dest']

            else:
                raise Exception("Temp file not logged properly in internal memory.")


        
    
    
