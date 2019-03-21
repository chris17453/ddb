import os
import time
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
from .methods.record_delete import method_delete
from .methods.record_core import query_results




def enum(**enums):
    return type('Enum', (), enums)


class engine:
    """A serverless flat file database engine"""
    

    
    def info(self,msg, arg1=None, arg2=None, arg3=None):
        if True == self.debug:
            print(msg, arg1, arg2, arg3)

    
   
    def __init__(self, config_file=None, query=None, debug=False, mode='array',output='TERM',output_file=None):
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
        # variables that can be set by the system
        
        self.system['DEBUG']=False
        self.system['AUTOCOMMIT']=True
        self.system['OUTPUT_MODULE']=output
        self.system['OUTPUT_STYLE']='RST'

        #auto functions ran when a variable is set
        self.system_trigger['DEBUG']=self.trigger_debug
        
        self.user={}
        self.internal['IN_TRANSACTION']=0
        
        # print "Config",config_file
        self.database = database(config_file=config_file)
        self.current_database = self.database.get_default_database()
        if None != query:
            self.query(query)
        
    # def set_configuration(self,database_instance):
    #    self.database=database
    #    if False == self.has_configuration():
    #        raise Exception("No configuration data")

    def trigger_debug(self):
        self.debug=self.system['DEBUG']
        self.database.debug=self.debug
        

    def debugging(self, debug=False):
        self.debug = debug

    def define_table(self, table_name, database_name, columns, data_file, field_delimiter=None):
        """Progromatically define a table. Not saved to a configuration file, unless manualy activated"""
        t = table(database=database_name, columns=columns, name=table_name, data_file=data_file, field_delimiter=field_delimiter)
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
            self.results = None
            if False == self.has_configuration():
                raise Exception("No table found")
            # update table info...
            # it may have changed...
            # self.database.reload_config()

            parser = lexer(sql_query, self.debug)
            if False == parser.query_objects:
                raise Exception("Invalid SQL")

            start = time.clock()
            for query_object in parser.query_objects:
                self.info("Engine: query_object", query_object)
                #print  query_object
                # exit(9)
                # get columns, doesnt need a table
                # print query_object['mode']
                mode=query_object['mode']
                
                # RECORDS
                if mode == 'select':
                    self.results = method_select(self,query_object, parser)
                
                elif mode == 'insert':
                    self.results = method_insert(self,query_object)

                elif mode == 'update':
                    self.results = method_update(self,query_object)
                
                elif mode == 'delete':
                    self.results = method_delete(self,query_object)

                elif mode == 'use':
                    self.results = method_use(self,query_object)

                # TABLE 
                elif mode == 'drop':
                    self.results = method_drop_table(self,query_object)

                elif mode == 'create':
                    self.results = method_create_table(self,query_object)

                elif mode == 'update table':
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

                elif mode == "show columns":
                    self.results = method_system_show_columns(self,self.database, query_object)

                elif mode == "show variables":
                    self.results = method_system_show_variables(self, query_object)

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
        except Exception as Ex:
            if None == self.results:
                self.results=query_results()
                self.results.error=Ex
            pass
        
            

            # timing
        end = time.clock()
        self.results.start_time=start
        self.results.end_time=end
        self.results.time=end-start
        return self.results

    def change_database(self, database_name):
        query = "use {0}".format(database_name)
        results = self.query(query)
        if None == results:
            return False
        return True
        
    def add_error(self,error):
        self.info(error)
    

    
    
