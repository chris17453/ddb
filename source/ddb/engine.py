import sys
import os
import time
import signal
import pprint
import random
import logging
import datetime
import time
import tempfile
import random
from subprocess import Popen,PIPE
from .lexer.lexer import lexer
from .configuration.table import table
from .configuration.database import database
from .version import __version__
import traceback 
from .methods.record import record, record_configuration  # converting After the fact...
try:
    import cython
except:
    pass
try:
    import boto3
    import botocore
except:
    pass


temp_dir=tempfile.gettempdir()


#logfile=os.path.join(temp_dir,'ddb.log')
#logging.basicConfig(filename=logfile, filemode='a',level=logging.INFO,format='(%(threadName)-10s) %(message)s')
#logging.propagate = False


#try:
#    if os.path.exists(logfile)==True:
#        os.chmod(logfile,0o666)
#except Exception, ex:
#    print (ex)
#    pass


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
from .meta.meta import meta 



class engine:
    """A serverless flat file database engine"""
    

    class data_type:
        COMMENT=1
        ERROR=2
        DATA=3
        WHITESPACE=4

    def error(self,msg, arg1=None, arg2=None, arg3=None):
        self.info(msg, arg1, arg2, arg3,level=logging.ERROR)
        exc_type, exc_value, exc_tb = sys.exc_info()
        traceback.print_exception(exc_type, exc_value, exc_tb)

    
    def info(self,msg, arg1=None, arg2=None, arg3=None,level=logging.INFO):
        pass
        #ts = time.time()
        #timestamp = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')

        #if level==logging.INFO:
        #    logging.info("PID:{0}: {4}: {1}, {2}, {3}".format(self.pid,msg,pprint.pformat(arg1,indent=4),arg2,timestamp))
        #elif  level==logging.ERROR:
        #    logging.error("PID:{0}: {4}: {1}, {2}, {3}".format(self.pid,msg,pprint.pformat(arg1,indent=4),arg2,timestamp))

        #if True == logging.disable:
        #    if isinstance(arg1,str) :
        #        print(msg, arg1, arg2, arg3)
        #    elif isinstance(arg1,object) :
        #        print(msg, arg2, arg3)
        #        pp = pprint.PrettyPrinter(indent=4)
        #        pp.pprint(arg1)
        #    else:    
        #        print(msg, arg1, arg2, arg3)

    
    @staticmethod
    def generate_uuid():
        try: # TODO unix/linux specific UUID generation
            f=open('/proc/sys/kernel/random/uuid') 
            uuid=f.read()
            f.close()
            return uuid.strip('\n')
        except:
            pass

    #def generate_uuid(self):
    #    random_string = ''
    #    random_str_seq = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
    #    uuid_format = [8, 4, 4, 4, 12]
    #    for n in uuid_format:
    #        for i in range(0,n):
    #            random_string += str(random_str_seq[random.randint(0, len(random_str_seq) - 1)])
    #        if n != 12:
    #            random_string += '-'
    #    return random_string

    # mode nested: row.data [ { data,error,raw } ]
    def signal_handler(self,sig, frame):

        print('ddb forcefully exited. Temp file cleanup needs to happen.')
        sys.exit(0)


    def __init__(self, config_dir=None, debug=None, mode='array',output='TERM',output_style='single',readonly=None,output_file=None,field_delimiter=',',new_line='\n'):
        signal.signal(signal.SIGINT, self.signal_handler)

        self.pid=os.getpid()
        # if false, load nothing, if true, load form user dir
        #if debug==True:
        #    logging.getLogger().setLevel(logging.INFO)
        #else:
        #    logging.getLogger().setLevel(logging.CRITICAL)
        self.debug = debug
        self.results = None
        self.mode = mode
        self.output=output
        self.output_file=output_file
        self.system={}
        self.system_trigger={}
        self.internal={}
        self.parameter={}

        self.internal={'READONLY':readonly,'TEMP_FILES':{},'FIELD_DELIMITER':field_delimiter,'NEW_LINE':'\n'}
        # variables that can be set by the system
        uuid_str=self.generate_uuid()
        self.system['UUID']= "{1}:{0}".format(uuid_str,os.getpid())
        self.system['DEBUG']=False
        self.system['AUTOCOMMIT']=True
        self.system['OUTPUT_MODULE']=output
        self.system['OUTPUT_CODE']='UTF-8'
        self.system['DATA_DIRECTORY']=config_dir
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
        
        self.system['CYTHON_ENABLED']=False
        try:
            if cython.compiled:
                self.system['CYTHON_ENABLED']=True
        except:
            pass
        

        self.system['OUTPUT_STYLE']=output_style
        self.internal['OUTPUT_MODULES']=[
            {'name':'bash','styles':[]},
            {'name':'term','styles':['ascii','single','double','rst','time']},
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
        self.database = database(config_dir=config_dir)
        self.current_database = self.database.get_default_database()
        # load tables
        # dont load empty stuff
        try:
            if config_dir:
                queries=self.database.get_db_sql()
                
                if queries:
                    self.query(queries)
        except:
            err = sys.exc_info()[1]
            ex = err.args[0]
            self.error(ex)
            pass

        
    # def set_configuration(self,database_instance):
    #    self.database=database
    #    if False == self.has_configuration():
    #        raise Exception("No configuration data")
    def init_state_variables(self):
        self.internal['row']=0

    def trigger_debug(self):
        self.debug=self.system['DEBUG']
        self.database.debug=self.debug
        
    def reset_parameters(self):
        self.parameter={}
        
    def set_param(self,parameter,value):
        # note make safe, strip delimiters quotes that stuff..
        self.parameter[parameter]="'{0}'".format(value)

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
        

    #UNSAFE !!! TODO
    def prepare_sql(self,sql,parameters=None):
        if parameters==None:
            param_list=self.parameter
        else:
            param_list=parameters

        for param in param_list:
            if self.debug:
                self.info("Setting Parameter: {0}:{1}".format(param,param_list[param]))
            
            #param=param.replace("\","\\")
            #param=param.replace("'","\'")
            #param=param.replace("\r","\\r")
            #param=param.replace("\n","\\n")
            #param=param.replace("\t","\\t")
            #param=param.replace("\b","\\b")
            #param=param.replace("\a","\\a")
            #param=param.replace("\"","\\\"")
           #
            key=param
            try:
                if isinstance(key,bytes)==True:
                    key=param.decode('ascii')
            except:
                pass

            val=param_list[param]
            try:
                if isinstance(val,bytes)==True:
                    val=param_list[param].decode('ascii')
            except:
                pass
                
                
            sql=sql.replace(key,val)
        #print(sql)
        
        return sql
    
    def execute(self, sql_query,parameters=None):
        return self.query(sql_query,parameters)
    
            

    def query(self, sql_query,parameters=None):
        try:
            start = time.perf_counter()
            wall_start = time.perf_counter()
        except:
            start = time.clock()
            wall_start = time.time()
            
            pass
        self.results = None

        if parameters:
            for param in parameters:
                #print ("SET {0}.{1}".format(param,parameters[param]))
                self.set_param(param,parameters[param])
        
        # this performs parameter substitution before lexing/parsing
        # it should only replace whole words, not within quotes and only starting with @
        # this is a TODO HOT feature. UNSAFE

        
        sql_query=self.prepare_sql(sql_query)
        self.excuted_query=sql_query
        
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
            # print query_object
            # todo safe_name

            mode=query_object['mode']

            
            #logging.info("PID:{1} : {0}".format(sql_query,self.pid))
            meta_class=meta().convert_to_class(query_object)
            
            if meta_class==None:
                err="Meta class failed to init. [{0}]".format(mode)
                raise Exception(err)
            
            if self.debug:
                meta_class.debug()
            
            
            
                        
            try:
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
                elif mode == 'use':
                    self.results = method_use(self,meta_class)

                elif mode == 'drop table' and self.internal['READONLY']==None:
                    self.results = method_drop_table(self,meta_class)

                elif mode == 'create table' and self.internal['READONLY']==None:
                    self.results = method_create_table(self,meta_class)

                elif mode == 'update table' and self.internal['READONLY']==None:
                    self.results = method_update_table(self,meta_class)

                # SYSTEM 
                elif mode == 'set':
                    self.results = method_system_set(self,meta_class)

                elif mode == 'begin':
                    self.results = method_system_begin(self,meta_class)

                elif mode == 'rollback':
                    self.results = method_system_rollback(self,meta_class)

                elif mode == 'commit':
                    self.results = method_system_commit(self)

                elif mode == "show tables":
                    self.results = method_system_show_tables(self,meta_class)

                elif mode == "show output modules":
                    self.results = method_system_show_output_modules(self,meta_class)

                elif mode == "show columns":
                    self.results = method_system_show_columns(self, meta_class)

                elif mode == "show variables":
                    self.results = method_system_show_variables(self,meta_class)

                elif mode == "describe table":
                    self.results = method_describe_table(self, meta_class)

            except:
                ex = sys.exc_info()[1]
                self.error (mode,ex)
                self.results=query_results(success=False,error=str(ex))   



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
            self.results.excuted_query=self.excuted_query
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
                elif self.mode=='v2':
                    try:
                        table                 =self.results.table
                        config=record_configuration()
                        config.columns        = self.results.columns
                        column_count          = len(self.results.columns)
                        line_number           = 0
                        remove_block_quotes   = True
                        if table:
                            data_starts_on_line   = table.data.starts_on_line
                            render_whitespace     = table.visible.whitespace
                            render_comment        = table.visible.comments
                            comment_delimiter     = table.delimiters.comment
                            field_delimiter       = table.delimiters.field
                            block_quote_delimiter = table.delimiters.block_quote
                        data=[]
                        for line in self.results.data:
                            if 'line_number' in line:
                                ln=line['line_number']
                            else:
                                ln=-1
                            r=record(data=line['data'],config=config,line_number=ln)
                            
                            data.append(r)
                        self.results.data=data
                        #for row in self.results.data:
                        #    print("DB-:{0}".format(row.to_json()))
                    except:
                        ex = sys.exc_info()[1]
                        self.error(ex)
                else:
                    pass

        #except Exception, Ex:
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
        self.reset_parameters()
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
        self.info("OSCMD INFO","{0}".format(" ".join(cmd)))
        p = Popen(cmd, stdin=PIPE, stdout=PIPE, stderr=PIPE)
        output, err = p.communicate()
        rc = p.returncode
        self.info("OSCMD INFO","{0}".format(output),"{0}".format(err))
        if rc!=0:
            self.info(output)
            self.info(err)
            self.info("OS CMD"," ".join(cmd))
            raise Exception("{0}: Exit Code {1}".format(err_msg,rc))
        return output
    
    def svn_checkout_file(self,table):
        self.info("IN SVN PULL")
        if table.data.repo_type=='svn':

            os.chdir(table.data.repo_dir)
            cmd=[   'svn','info']
            repo_url=None
            try:
                response=self.os_cmd(cmd,"SVN Repo Test").strip()
                url_index=response.find("URL:")
                url_index+=4
                tokens=response[url_index:].split("\n")
                repo_url=tokens[0].strip()
            except:
                err = sys.exc_info()[1]
                ex = err.args[0]
                self.info("SVN INFO -Initial Check","{0}".format(ex))
                pass
            #print "?",repo_url
            if None==repo_url:
                self.info("SVN INFO","No repo present attempt, init")

                cmd=[   'svn',
                        '--no-auth-cache',
                        '--username','{0}'.format(table.data.repo_user),
                        '--password','{0}'.format(table.data.repo_password),
                        'co',
                        table.data.repo_url,
                        table.data.repo_dir,
                        '--depth','empty',
                        '--non-interactive','--trust-server-cert']
                self.os_cmd(cmd,"SVN Repo Err")

            else:
                if table.data.repo_url!=repo_url and table.data.repo_url!=repo_url+"/" :
                    err_msg="SVN Repo is already initialized to a different location Want:{0},Have:{1}".format(table.data.repo_url, repo_url)
                    self.info("SVN ERROR",err_msg)
                    raise Exception (err_msg)

            self.info("SVN INFO","SVN Present, update file {0}".format(table.data.repo_file))
            os.chdir(table.data.repo_dir)
            self.info("SVN INFO","CHDIR  {0}".format(table.data.repo_dir))

            cmd=[   'svn',
                    'revert',
                    table.data.repo_file,
                    '--no-auth-cache',
                    '--username','{0}'.format(table.data.repo_user),
                    '--password','{0}'.format(table.data.repo_password),
                    '--non-interactive','--trust-server-cert'
                    ]
            self.os_cmd(cmd,"SVN Revert File Err")



            cmd=[   'svn',
                    'up',
                    table.data.repo_file,
                    '--no-auth-cache',
                    '--username','{0}'.format(table.data.repo_user),
                    '--password','{0}'.format(table.data.repo_password),
                    '--non-interactive','--trust-server-cert'
                    ]
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
                '--password','{0}'.format(table.data.repo_password),
                '--non-interactive','--trust-server-cert'
                ]
        self.os_cmd(cmd,"SVN Commit File Err")        
    

    def svn_commit_files(self,tables):
        """
          repo_files is a list of files in the repo_dir that need to be committed
        """
        self.info("IN SVN MULTI-COMMIT")

        base_dir     ={}
        files        =[]
        repo_dir     =None
        repo_user    =None
        repo_password=None
        
        # validate directory
        # create file list
        # realy dumb way to do this.. need a unified cred committing sequence
        # blackhole/fencepost errors could occur
        for table in tables:
            if False==os.path.exists(table.data.repo_dir):
                raise Exception("SVN Repo Directory not found {0}".format(table.data.repo_dir))
            base_dir[table.data.repo_dir]=1
            files.append(table.data.repo_file)
            repo_dir      =table.data.repo_dir
            repo_user     =table.data.repo_user
            repo_password =table.data.repo_password
        
        # only 1 directory at a time
        if len(base_dir)!=1:
                raise Exception("SVN Cannot commit multiple SVN directories at once '{0}'".format(",".join(base_dir)))

        self.info("SVN Committing {0}".format(",".join(files)))

        os.chdir(repo_dir)
        cmd=[   'svn',
                'commit',
                ' '.join(files),
                '-m','ddb',
                '--no-auth-cache',
                '--username','{0}'.format(repo_user),
                '--password','{0}'.format(repo_password),
                '--non-interactive','--trust-server-cert'
                ]
        self.os_cmd(cmd,"SVN Commit File Err")



    def s3_checkout_file(self,table):
        self.info("IN S3 PULL")
        if table.data.repo_type!='s3':
            raise Exception ("Not a s3 bucket")
        
        uuid_str=self.generate_uuid()
        temp_file="/tmp/ddb_s3_"+uuid_str
        BUCKET_NAME = table.data.repo_url
        
        s3 = boto3.resource('s3')

        try:
            
            s3_file=os.path.join(table.data.repo_dir,table.data.repo_file)
            s3.Bucket(BUCKET_NAME).download_file(s3_file,temp_file)
            return temp_file
        except botocore.exceptions.ClientError as e:
            if e.response['Error']['Code'] == "404":
                raise Exception("The object does not exist. "+s3_file)
            else:
                raise Exception(e)


    def get_data_file(self,table,prefix="ddb_"):
        self.internal['IN_TRANSACTION']=1
        data_file=table.data.path
        if data_file not in self.internal['TEMP_FILES']:
            if table.data.repo_type=='svn':
                self.svn_checkout_file(table)
                temp_data_file=create_temporary_copy(data_file,"ddb_"+self.system['UUID'],prefix)
            elif table.data.repo_type=='s3':
                temp_data_file=self.s3_checkout_file(table)
                
            else:
                temp_data_file=create_temporary_copy(data_file,"ddb_"+self.system['UUID'],prefix)

            self.internal['TEMP_FILES'][data_file]={'origin':data_file,'temp_source':temp_data_file,'written':None,'table':table}
        temp_source=self.internal['TEMP_FILES'][data_file]['temp_source']
        #print ("Temp File {0}".format(temp_source))
        return temp_source 
    
    def autocommit_write(self,table,dest_file):
        table_key=table.data.path
        if table_key in self.internal['TEMP_FILES']:
            self.internal['TEMP_FILES'][table_key]['written']=True
            src=self.internal['TEMP_FILES'][table_key]['temp_source']
            # remove the previous source
            if dest_file and dest_file!=src:
                lock.info("Lock Remove","Removing Intermediate Source file: {0}->{1}".format(src,dest_file))
                remove_temp_file(src)
                self.internal['TEMP_FILES'][table_key]['temp_source']=dest_file
        
    def auto_commit(self,table):
        self.info("AUTO COMMIT",self.internal['TEMP_FILES'])
        if self.system['AUTOCOMMIT']==True:
            self.info("AUTOCOMMIT")
            method_system_commit(self)




