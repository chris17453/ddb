import os
from .lexer.lexer import lexer
from .structure.table import table
from .structure.database import database
from .evaluate.match import match
from .version import __version__

#methods -> actions

# database level data methods
from .methods.database.use import method_use
from .methods.database.set import method_set
from .methods.database.show_errors import method_show_errors

# table level structure methods
from .methods.table.structure.create import method_create_table
from .methods.table.structure.update import method_update_table
from .methods.table.structure.describe import method_describe_table
from .methods.table.structure.drop import method_drop_table

# table level data methods
from .methods.table.data.insert import method_insert 
from .methods.table.data.select import method_select
from .methods.table.data.update import method_update
from .methods.table.data.delete import method_delete
from .methods.table.data.show_tables import method_show_tables
from .methods.table.data.show_columns import method_show_columns




def enum(**enums):
    return type('Enum', (), enums)


class engine:
    """A serverless flat file database engine"""
    
    def info(self,msg, arg1=None, arg2=None, arg3=None):
        if True == self.debug:
            print(msg, arg1, arg2, arg3)

    
    data_type = enum(COMMENT=1, ERROR=2, DATA=3, WHITESPACE=4)

    def __init__(self, config_file=None, query=None, debug=False, mode='array',output='term',output_file=None):
        self.debug = debug
        self.results = None
        self.mode = mode
        self.output=output
        self.output_file=output_file
        self.match=match()
        
        # print "Config",config_file
        self.database = database(config_file=config_file)
        self.current_database = self.database.get_default_database()
        if None != query:
            self.query(query)

    # def set_configuration(self,database_instance):
    #    self.database=database
    #    if False == self.has_configuration():
    #        raise Exception("No configuration data")


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
        if False == self.has_configuration():
            raise Exception("No table found")
        self.results = None

        # update table info...
        # it may have changed...
        # self.database.reload_config()

        parser = lexer(sql_query, self.debug)
        if False == parser.query_objects:
            raise Exception("Invalid SQL")

        for query_object in parser.query_objects:

            self.info("Engine: query_object", query_object)
            #print  query_object
            # exit(9)
            # get columns, doesnt need a table
            # print query_object['mode']
            if query_object['mode'] == "show tables":
                self.results = method_show_tables(self,self.database)
            if query_object['mode'] == "show columns":
                self.results = method_show_columns(self,self.database, query_object)
            
            #if query_object['mode']=="show errors":
            #    self.results=method_show_errors(self,self.database,self.table)
            
            if query_object['mode'] == 'select':
                self.results = method_select(self,query_object, parser)
            
            if query_object['mode'] == 'insert':
                self.results = method_insert(self,query_object)

            if query_object['mode'] == 'update':
                self.results = method_update(self,query_object)

            if query_object['mode'] == 'delete':
                self.results = method_delete(self,query_object)

            if query_object['mode'] == 'use':
                self.results = method_use(self,query_object)

            if query_object['mode'] == 'set':
                self.results = method_set(self,query_object)

            if query_object['mode'] == 'drop table':
                self.results = method_drop_table(self,query_object)

            if query_object['mode'] == 'create table':
                self.results = method_create_table(self,query_object)

            if query_object['mode'] == 'update table':
                self.results = method_update_table(self,query_object)

            if query_object['mode'] == 'describe table':
                self.results = method_describe_table(self,query_object)

        # only return last command
        if None != self.results:
            # if the result set it not empty
            if None != self.results.data:
                if None != self.results.data.results:
                     # if self.mode == 'array':
                     #   new_array = []
                     #   for line in self.results.data.results:
                     #       new_array.append(line['data'])
                     #   self.results.data=
                    
                    if self.mode == 'object':
                        columns = self.results.get_columns()
                        len_col = len(columns)
                        for line in self.results.data.results:
                            new_dict = {}
                            for i in range(0, len_col):
                                if len(line['data']) < i:
                                    break
                                new_dict[columns[i]] = line['data'][i]
                            line['data']=new_dict
                    self.reesults.data=self.results.data.results

                            
            else:
                if self.mode == 'array':
                    self.results.data=[]
                if self.mode == 'object':
                    self.results.data={}

            return self.results

        return None

    def change_database(self, database_name):
        query = "use {}".format(database_name)
        results = self.query(query)
        if None == results:
            return False
        return True
        
    def add_error(self,error):
        self.info(error)
    

    
    
