import unittest
import os
from subprocess import Popen, PIPE
import sys
import time
from pprint import pprint
#import cProfile as profile
#import pstats


standalone_script=None

pprint(os.environ,indent=4)
print ("TESTING")
if 'DDB_RELEASE_DIR' in os.environ:
    print ("Found test dir")
    standalone_script=os.environ['DDB_RELEASE_DIR']


if standalone_script!=None:
    sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__),standalone_script)))

    try:
        from ddb import ddb
    except:
        print ("DDB STANDALONE FAILED")
        ex=sys.exc_info()[1]
        print (ex)
        sys.exit(1)
    print ("DDB STANDALONE")
else:
    sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

    try:
        from source import ddb
    except:
        print ("DDB CYTHON FAILED")
        ex=sys.exc_info()[1]
        print (ex)
        sys.exit(1)
    print ("DDB CYTHON")


def stringer(base,*args):
    index=0
    o=base
    for arg in args:
        term=u"{"+str(index)+"}"
        if isinstance(arg,float):
            replacment=u"%f" % arg
        elif isinstance(arg,int):
            replacment=u"%d" % arg
        else:
            try:
                replacment=u"%s" % arg.decode("utf-8")
            except:
                replacment=u"%s" % arg

            
        o=o.replace(term,replacment)
        index+=1
    return o


def update_stats(test,status):
    p = Popen(['git', 'log','-1'], stdin=PIPE, stdout=PIPE, stderr=PIPE)
    data, err = p.communicate(None)
    rc = p.returncode
    #print(data)
    data=data.split("\n".encode("ascii"))


    engine=ddb.engine()
    version =str(engine.system['VERSION'])
    date    =str(time.strftime('%Y-%m-%d %H:%M:%S'))
    commit  =str(data[0])
    log     =str(data[4].strip())
    py_major=str(engine.system['PYTHON_MAJOR'])
    py_minor=str(engine.system['PYTHON_MINOR'])
    py_micro=str(engine.system['PYTHON_MICRO'])
    cython  =str(engine.system['CYTHON_ENABLED'])
    row=[test,version,commit,log,status,date,py_major,py_minor,py_micro,cython]
    csv_row=",".join(row)
    
    file=open("profile/stats.csv","at")
    file.write(csv_row+"\n")
    file.close()


class test_engine(unittest.TestCase):
    temp_config = 'temp_config.yaml'
    temp_data = 'MOCK_DATA.csv'
    temp_data2 = 'MOCK_DATA2.csv'
    basedir = os.path.dirname(os.path.abspath(__file__))+"/data/"
    basedir_svn = os.path.dirname(os.path.abspath(__file__))
    table_name = 'test'
    table_name2 = 'test2'
    debug=None
    config_dir= os.path.dirname(os.path.abspath(__file__))+"/data/"

  
    def cleanup(self):
        # print ("#--->Fresh init")
        
        for file in os.listdir(self.config_dir):
            if file.endswith(".table.sql"):
                table_path=os.path.join(self.config_dir, file)
                os.remove(table_path)
    def create_table(self,engine,mode):
        print ("Create table")
        if mode=='SVN':
            repo=stringer("repo='{0}' url='{1}' user='{2}' password='{3}' repo_dir='{4}' repo_file='{5}'",
                'svn',
                'http://localhost/svn/SampleProject/',
                'user',
                'password',
                os.path.join(self.basedir_svn,'svn_test'),
                'MOCK_DATA.csv')
            file_name=os.path.join(self.basedir_svn,'svn_test',"MOCK_DATA.csv")
        else:
            repo=''
            file_name=os.path.join(self.basedir, self.temp_data)
       
        query=stringer("create table {0} ('id','first_name','last_name','email','gender','ip_address') file='{1}' {2} data_starts_on=2",self.table_name, file_name,repo)
        #print query
        results = engine.query(query)
        #results.debug()
        print ("QUERY ->")
        print (query)
        print ("---")
        
        
        self.assertEqual(True, results.success)
        query=stringer("create table {0} ('id','first_name','last_name','email','gender','ip_address') file='{1}' {2} data_starts_on=2",self.table_name2, file_name,repo)
        results = engine.query(query)
        self.assertEqual(True, results.success)
    def test_set(self):
        """Set a database variable """
        print ("SET")
        self.cleanup()
        engine = ddb.engine(config_dir=self.config_dir,debug=None)
        
        results = engine.query("set AUTOCOMMIT=False")
        self.assertEqual(True, results.success)
        results = engine.query("set OUTPUT_MODULE=YAML")
        self.assertEqual(True, results.success)
        results = engine.query("set OUTPUT_MODULE=TERM_RST")
        self.assertEqual(True, results.success)
        results = engine.query("set OUTPUT_MODULE=TERM_SINGLE")
        self.assertEqual(True, results.success)
        # Because it doesnt exist
        results = engine.query("set OUTPUT=TERM_DOUBLE")
        self.assertEqual(False, results.success)
        # User var test
        results = engine.query("set @time=1")
        self.assertEqual(True, results.success)
        results = engine.query("set @light=ON")
        self.assertEqual(True, results.success)
        results = engine.query("set @light=OFF")
        self.assertEqual(True, results.success)
        results = engine.query("set @config=FALSE")
        self.assertEqual(True, results.success)

        results = engine.query("show variables")
        try:
            ddb.output.factory.output_factory(query_results=results,output='TERM')
        except:
            ddb.output_factory(query_results=results,output='TERM')

        self.assertEqual(True, results.success)
    def test_use(self,mode=None):
        """Test changing database context"""
        print("USE")
        # single db change from default
        self.cleanup()
        engine = ddb.engine(config_dir=self.config_dir,debug=None)
        self.create_table(engine,mode)
                
        
        results = engine.query(stringer("use {0}",self.table_name))
        self.assertEqual(True, results.success)
        results = engine.query("select database()")
        self.assertEqual(True, results.success)
    def test_show_output_modules(self):
        """Test showint output modules and styles"""
        # single db change from default
        self.cleanup()
        engine = ddb.engine(config_dir=self.config_dir,debug=None)
        results = engine.query("show output modules")
        try:
            ddb.output.factory.output_factory(query_results=results,output='TERM')
        except:
            ddb.output_factory(query_results=results,output='TERM')
        self.assertEqual(True, results.success)
    def test_show_tables(self,mode=None):
        """Show all tables in the database"""
        self.cleanup()
        engine = ddb.engine(config_dir=self.config_dir,debug=None)
        self.create_table(engine,mode)

        results = engine.query("SHOW TABLES")
        #results.debug()
        self.assertEqual(True, results.success)
        try:
            ddb.output.factory.output_factory(query_results=results,output='term')
        except:
            ddb.output_factory(query_results=results,output='term')
    def test_describe_table(self,mode=None):
        """Show table configuration"""
        print ("DESCRIBE TABLE")
        self.cleanup()

        engine = ddb.engine(config_dir=self.config_dir,debug=None)
        self.create_table(engine,mode)

        results = engine.query(stringer("DESCRIBE TABLE {0}",self.table_name))
        try:
            ddb.output.factory.output_factory(query_results=results,output='term')
        except:
            ddb.output_factory(query_results=results,output='TERM')
        self.assertEqual(True, results.success)
    def test_create_table(self,mode=None):
        """Test creating a table"""
        try:
            self.cleanup()
            engine = ddb.engine(config_dir=self.config_dir,debug=None)
        
            self.create_table(engine,mode)
        except Exception:
            ex=sys.exc_info()[1]
            self.fail(ex)

        # fail on existing table
        results=engine.query(stringer("create table {0} ('id','first_name','last_name','email','gender','ip_address') file='{1}' data_starts_on=2",self.table_name, os.path.join(self.basedir, self.temp_data)))
        self.assertEqual(False, results.success)
    def test_drop_table(self,mode=None):
        """Test dropping a table"""
        self.cleanup()
        engine = ddb.engine(config_dir=self.config_dir,debug=None)
        
        self.create_table(engine,mode)
        
        # fail on existing table
        results = engine.query(stringer('drop table {0}',self.table_name))
        self.assertEqual(True, results.success)
            
            # fail on dropping non existant table
           # results=engine.query('drop table {0}'stringer(self.table_name))
           # self.assertEqual(False, results.success)
    def test_params(self,mode=None):
        """Test parameterizing a query"""
        print("PARAMS")
        self.cleanup()
        engine = ddb.engine(config_dir=self.config_dir,debug=None)
        # fail on existing table
        
        self.create_table(engine,mode)
        
        # test results length
        engine.set_param("@limit",10)
        
        results = engine.query(stringer('select * from {0} LIMIT @limit',self.table_name))
        self.assertEqual(True, results.success)
        self.assertEqual(10, results.data_length)

        engine.set_param("@limit",8)
        results = engine.query(stringer('select * from {0} LIMIT @limit',self.table_name))
        self.assertEqual(True, results.success)
        self.assertEqual(8, results.data_length)
    def test_select(self,mode=None):
        """Test selecting results using various clauses a table"""
        print("SELECT")
        self.cleanup()
        engine = ddb.engine(config_dir=self.config_dir,debug=None)
        # fail on existing table
        
        self.create_table(engine,mode)
        
        # test results length
        
        results = engine.query(stringer('select * from {0} LIMIT 10',self.table_name))
        self.assertEqual(True, results.success)
        self.assertEqual(10, results.data_length)

        results = engine.query(stringer('select * from {0} LIMIT 1',self.table_name))
        self.assertEqual(True, results.success)
        self.assertEqual(1, results.data_length)

        results = engine.query(stringer('select * from {0} LIMIT 0',self.table_name))
        self.assertEqual(True, results.success)
        self.assertEqual(0, results.data_length)
        
        # WHERE/LIMIT
        results = engine.query(stringer('select * from {0} where id="1" order by id LIMIT 100;',self.table_name))
        results.debug()
        self.assertEqual(True, results.success)
        self.assertEqual(1, results.data_length)
        
        # WHERE AND/LIMIT
        results = engine.query(stringer('select * from {0} where id="1" and id not "2" order by id LIMIT 100;',self.table_name))
        self.assertEqual(True, results.success)
        self.assertEqual(1, results.data_length)

        # WHERE / AND / OR/LIMIT
        results = engine.query(stringer('select * from {0} where id="1" and id not "2" or id="3" order by id LIMIT 100;',self.table_name))
        self.assertEqual(True, results.success)
        self.assertEqual(2, results.data_length)
    def test_update(self,mode=None):
        """Update a row in the test file"""
        self.cleanup()
        print("UPDATE")
        engine = ddb.engine(config_dir=self.config_dir,debug=None)
        # fail on existing table
        self.create_table(engine,mode)
        
        results = engine.query(stringer("insert into {0} ('id','first_name','last_name','email','gender','ip_address') values (1002,test_name,test_lname,'bop@bob.com','m','0.0.0.0')",self.table_name))
        print("UPDATE 1")
        self.assertEqual(True, results.success)
        # update
        results = engine.query(stringer('update {0} set email="test@test.com" where id="1002"',self.table_name))
        print("UPDATE 2")
        self.assertEqual(True, results.success)
        
        results = engine.query(stringer("delete from {0} where id='1002'",self.table_name))
        print("UPDATE 3")
        self.assertEqual(True, results.success)
    def test_insert(self,mode=None):
        """Insert a row in the test file"""
        self.cleanup()
        print("INSERT")
        engine = ddb.engine(config_dir=self.config_dir,debug=self.debug)
        self.cleanup()
        # fail on existing table
        self.create_table(engine,mode)

        # update
        results = engine.query(stringer("insert into {0} ('id','first_name','last_name','email','gender','ip_address') values (1001,test_name,test_lname,'bop@bob.com','m','0.0.0.0')",self.table_name))
        #results.debug()
        self.assertEqual(True, results.success)
        # Delete
        results = engine.query(stringer("delete from {0} where id='1001'",self.table_name))
        self.assertEqual(True, results.success)
    def test_delete(self,mode=None):
        """Delete a test row in the test file"""
        self.cleanup()
        print("DELETE")
        engine = ddb.engine(config_dir=self.config_dir)
        self.create_table(engine,mode)
        results = engine.query(stringer("insert into {0} ('id','first_name','last_name','email','gender','ip_address') values (1003,test_name,test_lname,'bop@bob.com','m','0.0.0.0')",self.table_name))
        self.assertEqual(True, results.success)
        # delete just inserted
        print ("DELETE 2")
        results = engine.query(stringer("delete from {0} where id='1003'",self.table_name))
        self.assertEqual(True, results.success)

        print ("DELETE 3")
        # delete non existing
        results = engine.query(stringer("delete from {0} where email like 'bop@%'",self.table_name))
        self.assertEqual(True, results.success)
    def test_upsert(self,mode=None):
        """Show all tables in the database"""
        self.cleanup()
        print("UPSERT")
        engine = ddb.engine(config_dir=self.config_dir,debug=None)
        self.create_table(engine,mode)

        results = engine.query(stringer("upsert into {0} ('id','first_name','last_name','email','gender','ip_address') values (1006,test_name,test_lname,'tag@bob.com','m','0.0.0.0') ON DUPLICATE KEY id UPDATE id='12345' ",self.table_name))
        self.assertEqual(True, results.success)

        results = engine.query(stringer("select * from  {0} where id = 1006",self.table_name))
        self.assertEqual(1, results.data_length)
        
        results = engine.query(stringer("upsert into {0} ('id','first_name','last_name','email','gender','ip_address') values (1006,test_name,test_lname,'tag@bob.com','m','0.0.0.0') ON DUPLICATE KEY id UPDATE id='12345' ",self.table_name))
        self.assertEqual(True, results.success)

        results = engine.query(stringer("select * from  {0} where id = 12345",self.table_name))
        self.assertEqual(1, results.data_length)
        
        results = engine.query(stringer("delete from {0} where id = 12345",self.table_name))
        self.assertEqual(1, results.affected_rows)

        try:
            ddb.output.factory.output_factory(query_results=results,output='term')
        except:
            ddb.output_factory(query_results=results,output='TERM')
    def test_rollback(self,mode=None):
        """Rollback db changes"""
        self.cleanup()
        print("ROLLBACK")
        engine = ddb.engine(config_dir=self.config_dir)

        self.create_table(engine,mode)

        print ("Begin")
        results = engine.query("begin")
        self.assertEqual(True, results.success)

        # get the length of all rows
        print ("Select")
        results = engine.query(stringer("SELECT id FROM {0}",self.table_name) )
        self.assertEqual(True, results.success)
        target_length=results.data_length

        # update
        print ("Insert")
        results = engine.query(stringer("insert into {0} ('id','first_name','last_name','email','gender','ip_address') values (1001,test_name,test_lname,'bop@bob.com','m','0.0.0.0')",self.table_name))
        print ("Insert")
        results = engine.query(stringer("insert into {0} ('id','first_name','last_name','email','gender','ip_address') values (1001,test_name,test_lname,'bop@bob.com','m','0.0.0.0')",self.table_name2))
        self.assertEqual(True, results.success)

        print ("Select")
        results = engine.query(stringer("SELECT id FROM {0}",self.table_name) )
        
        self.assertEqual(True, results.success)
        self.assertEqual(target_length+2, results.data_length)
        #results.debug()

        print ("rollback")
        results = engine.query("rollback")
        self.assertEqual(True, results.success)
        
        results = engine.query(stringer("SELECT id FROM {0}",self.table_name) )
        #results.debug()
        self.assertEqual(True, results.success)
        self.assertEqual(target_length, results.data_length)
    def test_commit(self,mode=None):
        """Rollback db changes"""
        self.cleanup()
        print("COMMIT")
        engine = ddb.engine(config_dir=self.config_dir)

        self.create_table(engine,mode)
        
        print ("PRE BEGIN")
        results = engine.query("begin")
        self.assertEqual(True, results.success)

        

        print ("PRE DELETE")
        # clean any inserts
        results = engine.query(stringer("delete from {0} WHERE email='bop@bob.com'",self.table_name))
        self.assertEqual(True, results.success)

        print ("Get length")
        results = engine.query(stringer("SELECT id FROM {0}",self.table_name) )
        #results.debug()
        self.assertEqual(True, results.success)
        target_length=results.data_length

        print ("PRE INSERT")
        # update
        results = engine.query(stringer("insert into {0} ('id','first_name','last_name','email','gender','ip_address') values (1001,test_name,test_lname,'bop@bob.com','m','0.0.0.0')",self.table_name))
        #results.debug()
        self.assertEqual(True, results.success)

        print ("PRE SELECT")
        results = engine.query(stringer("SELECT id FROM {0}",self.table_name) )
        #results.debug()
        self.assertEqual(True, results.success)
        self.assertEqual(target_length+1, results.data_length)
        #results.debug()

        print ("PRE COMMIT")
        results = engine.query("commit")
        print (results.error)
        self.assertEqual(True, results.success)
        
        print ("PRE SELECT")
        results = engine.query(stringer("SELECT id FROM {0}",self.table_name) )
        #results.debug()
        self.assertEqual(True, results.success)
        self.assertEqual(target_length+1, results.data_length)
        
        print ("PRE DELETE")
        results = engine.query(stringer("delete from {0} where id='1001'",self.table_name))
        self.assertEqual(True, results.success)
        

     
    ##### SVN
    ##### SVN
    ##### SVN

#    def test_svn_create_table(self):
#        self.test_create_table(mode='SVN')
#
#    def test_svn_drop_table(self):
#        self.test_drop_table(mode='SVN')
#
#    def test_svn_select(self):
#        self.test_select(mode='SVN')
#
#    def test_svn_update(self):
#        self.test_update(mode='SVN')
#
#    def test_svn_insert(self):
#        self.test_insert(mode='SVN')
#
#    def test_svn_delete(self):
#        self.test_delete(mode='SVN')
#
#    def test_svn_upsert(self):
#        self.test_upsert(mode='SVN')
#
#    def test_svn_rollback(self):
#        self.test_rollback(mode='SVN')
#
#    def test_svn_commit(self):
#        self.test_commit(mode='SVN')
#
#    def test_svn_describe_table(self):
#        self.test_describe_table(mode='SVN')
#    
#    def test_svn_show_tables(self):
#        self.test_show_tables(mode='SVN')





# str_data="bob,sam,dave,elvis,monster,pizza,car,woman"
# 
# config=record_configuration()
# config.columns               = ['c1','c2','c3','c4','c5','c6','c7','c8']
# config.column_count          = 8
# config.line_number           = 0
# config.data_starts_on_line   = 0
# 
# data=record(str_data,config)
# 
# print "Iterate through keys"
# index=0
# for key  in data:
#     print(key)
#     index+=1
# 
# print "Iterate through Ietems (tupels)"
# index=0
# for key,column in data.items():
#     print(key,column)
#     index+=1
# 
# print ("Direct Access of data")
# print data.c1
# print data.c2
# print data.c3
# 
# data.c1="loop"
# print data.c1
# 
# print ("Assignment of data to invalid key")
# try:
#   data.c31="bob"
# except Exception:
#   ex=sys.exc_info()[1]
#   print ex
# 
# print ("Access of data from invalid key")
# try:
#   print data.c34
# except Exception:
#   ex=sys.exc_info()[1]
#   print ex

def get_name(data):
    tokens=str(data).split(" ")
    return tokens[0][5:]
if __name__ == '__main__':
    print("Testing")
    
    suite = unittest.TestSuite()
    result = unittest.TestResult()
    
    suite.addTest(unittest.makeSuite(test_engine))
    test_arr=[]
    for test in suite:
        for x in  test._tests:
            test_name=get_name(x)
            test_arr.append(test_name)
    runner = unittest.TextTestRunner()
    results=runner.run(suite)
    
    #print(results.errors)
    #print(results.failures)
    test_results={}
    #print (results.failures)
    for err in results.failures:
        test=get_name(err[0])
        print(test)
        test_results[test]='Failed'
    for err in results.errors:
        test=get_name(err[0])
        test_results[test]='Failed'

    for test in test_arr:
        if test not in test_results:
            test_results[test]='Success'

    # this appends a results row to a csv per test
    for test in test_results:
        print(" %s - %s "%(test,test_results[test]))
        update_stats(test,test_results[test])

    