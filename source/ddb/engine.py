# cython: linetrace=True

import sys
import os
import time
import pprint
import uuid
import logging
from subprocess import Popen,PIPE
from .lexer.lexer import lexer
from .configuration.table import table
from .configuration.database import database
from .version import __version__


logging.basicConfig(filename='/tmp/ddb.log', filemode='a',level=logging.INFO,format='(%(threadName)-10s) %(message)s')
logging.propagate = False

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

# Dynamic metadata class abstraction layer
from .meta import meta 

class engine:
    """A serverless flat file database engine"""
    

    class data_type:
        COMMENT=1
        ERROR=2
        DATA=3
        WHITESPACE=4

    def info(self,msg, arg1=None, arg2=None, arg3=None):
        #logging.info("PID:{0} : {1}, {2}, {3}".format(self.pid,msg,arg1,arg2))
        if True == self.debug:

            if isinstance(arg1,str) :
                print(msg, arg1, arg2, arg3)
            elif isinstance(arg1,object) :
                print(msg, arg2, arg3)
                pp = pprint.PrettyPrinter(indent=4)
                pp.pprint(arg1)
            else:    
                print(msg, arg1, arg2, arg3)

    
   
    def __init__(self, config_file=None, query=None, debug=None, mode='array',output='TERM',output_style='single',readonly=None,output_file=None,field_delimiter=',',new_line='\n'):
        
        self.pid=os.getpid()
        # if false, load nothing, if true, load form user dir
        if config_file is None:
            home = os.path.expanduser("~")
            config_file = os.path.join(os.path.join(home, '.ddb'), 'ddb.conf')
    
        self.debug = debug
        self.results = None
        self.mode = mode
        self.output=output
        self.output_file=output_file
        self.system={}
        self.system_trigger={}
        self.internal={}
        
        self.internal={'READONLY':readonly,'TEMP_FILES':{},'FIELD_DELIMITER':field_delimiter,'NEW_LINE':'\n'}
        # variables that can be set by the system
        uuid_str=uuid.uuid1()
        self.system['UUID']= uuid_str.urn[9:]
        self.system['DEBUG']=False
        self.system['AUTOCOMMIT']=True
        self.system['OUTPUT_MODULE']=output
        self.system['VERSION']=__version__
        
        try:
            self.system['PYTHON_MAJOR']=sys.version_info.major
            self.system['PYTHON_MINOR']=sys.version_info.minor 
            self.system['PYTHON_MICRO']=sys.version_info.micro
            self.system['PYTHON_RELEASELEVEL']=sys.version_info.releaselevel
            self.system['PYTHON_SERIAL']=sys.version_info.serial
        except:
            self.system['PYTHON_MAJOR']=sys.version_info[0]
            self.system['PYTHON_MINOR']=sys.version_info[1]
            self.system['PYTHON_MICRO']=sys.version_info[2]
            self.system['PYTHON_RELEASELEVEL']=sys.version_info[3]
            self.system['PYTHON_SERIAL']=sys.version_info[4]
            pass
        

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
        #try:        
            # print "Config",config_file
        self.database = database(config_file=config_file)
        self.current_database = self.database.get_default_database()
        # load tables
        # dont load empty stuff
        if config_file!=False:
            queries=self.database.get_db_sql()
            logging.disabled = True
            if queries:
                self.query(queries)
            logging.disabled = False
        #except Exception as ex:
        #    pass

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
        parser = lexer(sql_query,debug=self.debug)
     

        for query_object in parser.query_objects:
            # clear all per state variables per run
            self.init_state_variables()
            
            self.info("Engine: query_object", query_object)
            #d  query_object
            # exit(9)
            # get columns, doesnt need a table
            #print query_object
            # todo safe_name

            mode=query_object['mode']

            
            logging.info("PID:{1} : {0}".format(sql_query,self.pid))
            meta_class=meta.convert_to_class(query_object)
            if meta_class==None:
                err="Meta class failed to init. [{0}]".format(mode)
                raise Exception(err)
            
            if self.debug:
                meta_class.debug()
            # RECORDS
            if mode == 'select':
                self.results = method_select(self,meta_class, parser)
            
            elif mode == 'insert' and self.internal['READONLY']==None:
                self.results = method_insert(self,meta_class)

            elif mode == 'update' and self.internal['READONLY']==None:
                self.results = method_update(self,meta_class)

            elif mode == 'upsert' and self.internal['READONLY']==None:
                self.results = method_upsert(self,meta_class,query_object,meta)
            
            elif mode == 'delete' and self.internal['READONLY']==None:
                self.results = method_delete(self,meta_class)

            # TABLE 
            elif mode == 'use table':
                self.results = method_use(self,meta_class)

            elif mode == 'drop table' and self.internal['READONLY']==None:
                self.results = method_drop_table(self,meta_class)

            elif mode == 'create table' and self.internal['READONLY']==None:
                meta_class.debug()
                self.results = method_create_table(self,meta_class)

            elif mode == 'update table' and self.internal['READONLY']==None:
                self.results = method_update_table(self,meta_class)

            # SYSTEM 
            elif mode == 'set':
                self.results = method_system_set(self,meta_class)

            elif mode == 'begin':
                self.results = method_system_begin(self)

            elif mode == 'rollback':
                self.results = method_system_rollback(self)

            elif mode == 'commit':
                self.results = method_system_commit(self)

            elif mode == "show tables":
                self.results = method_system_show_tables(self)

            elif mode == "show output modules":
                self.results = method_system_show_output_modules(self)

            elif mode == "show columns":
                self.results = method_system_show_columns(self, meta_class)

            elif mode == "show variables":
                self.results = method_system_show_variables(self)

            elif mode == "describe table":
                self.results = method_describe_table(self, meta_class)

            if False==self.results.success:

                break
            #if mode=="show errors":
            #    self.results=method_show_errors(self,self.database,self.table)
            #else:
            # TODO uncaught    
            #    print (query_object)
        # only return last command
        if self.results:
            self.results.delimiter=self.internal['FIELD_DELIMITER']
            self.results.new_line=self.internal['NEW_LINE']
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
    
    def os_cmd(self,cmd,err_msg):
        p = Popen(cmd, stdin=PIPE, stdout=PIPE, stderr=PIPE)
        output, err = p.communicate()
        rc = p.returncode
        if rc!=0:
            self.info(output)
            self.info(err)
            raise Exception("{0}: Exit Code {1}".format(err_msg,rc))
        return output
    
    def svn_checkout_file(self,table):
        self.info("IN SVN PULL")
        if table.data.repo_type=='svn':

            cmd=[   'svn','info','--show-item','url']
            repo_url=None
            try:
                repo_url=self.os_cmd(cmd,"SVN Repo Test").strip()
            except Exception as ex:
                pass
            #print "?",repo_url
            if None==repo_url:

                cmd=[   'svn',
                        '--no-auth-cache',
                        '--username','{0}'.format(table.data.repo_user),
                        '--password','{0}'.format(table.data.repo_password),
                        'co',
                        table.data.repo_url,
                        table.data.repo_dir,
                        '--depth','empty']
                #print " ".join(cmd)
                self.os_cmd(cmd,"SVN Repo Err")

            else:
                if table.data.repo_url!=repo_url:
                    err_msg="SVN Repo is already initialized to a different location Want:{0},Have:{1}".format(table.data.repo_url, repo_url)
                    raise Exception (err_msg)

            os.chdir(table.data.repo_dir)
            cmd=[   'svn',
                    'up',
                    table.data.repo_file,
                    '--no-auth-cache',
                    '--username','{0}'.format(table.data.repo_user),
                    '--password','{0}'.format(table.data.repo_password)
                    ]
            #print " ".join(cmd)
            self.os_cmd(cmd,"SVN Checkout File Err")
    
    def svn_commit_file(self,table):
        self.info("IN SVN COMMIT",table.data.name)
        if False==os.path.exists(table.data.repo_dir):
            self.info("Creating svn directory that does not exist {0}".format(table.dir.repo_dir))
            os.mkdir(table.data.repo_dir)

        os.chdir(table.data.repo_dir)
        cmd=[   'svn',
                'commit',
                table.data.repo_file,
                '-m','ddb',
                '--no-auth-cache',
                '--username','{0}'.format(table.data.repo_user),
                '--password','{0}'.format(table.data.repo_password)
                ]
        #print " ".join(cmd)
        self.os_cmd(cmd,"SVN Checkout File Err")        

    def get_data_file(self,table,prefix="ddb_"):
        self.internal['IN_TRANSACTION']=1
        data_file=table.data.path
        if data_file not in self.internal['TEMP_FILES']:
            if table.data.repo_type=='svn':
                self.svn_checkout_file(table)
            temp_data_file=create_temporary_copy(data_file,self.system['UUID'],prefix)
            #print ("CREATED: "+temp_data_file)
            self.internal['TEMP_FILES'][data_file]={'origin':data_file,'temp_source':temp_data_file,'written':None,'table':table}
        return self.internal['TEMP_FILES'][data_file]['temp_source']
    
    def autocommit_write(self,table,dest_file):
        table_key=table.data.path
        if table_key in self.internal['TEMP_FILES']:
            self.internal['TEMP_FILES'][table_key]['written']=True
            # remove the previous source
            if dest_file and dest_file!=self.internal['TEMP_FILES'][table_key]['temp_source']:
                #print ("removing "+self.internal['TEMP_FILES'][table_key]['temp_source'])
                remove_temp_file(self.internal['TEMP_FILES'][table_key]['temp_source'])
                self.internal['TEMP_FILES'][table_key]['temp_source']=dest_file
        
    def auto_commit(self,table):
        if self.system['AUTOCOMMIT']==True:
            self.info("AUTOCOMMIT")
            #print ("---Autocommit")
            method_system_commit(self)




        
    
    
