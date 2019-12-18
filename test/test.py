import unittest
import os
import sys
from .context import  ddb
from pprint import pprint
import cProfile as profile
import pstats

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
        if mode=='SVN':
            repo="repo='{0}' url='{1}' user='{2}' password='{3}' repo_dir='{4}' repo_file='{5}'".format(
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
       
        query="create table {0} ('id','first_name','last_name','email','gender','ip_address') file='{1}' {2} data_starts_on=2".format(self.table_name, file_name,repo)
        #print query
        results = engine.query(query)
        results.debug()
        print ("QUERY ->")
        print (query)
        print ("---")
        
        
        self.assertEqual(True, results.success)
        query="create table {0} ('id','first_name','last_name','email','gender','ip_address') file='{1}' {2} data_starts_on=2".format(self.table_name2, file_name,repo)
        results = engine.query(query)
        self.assertEqual(True, results.success)

    def _test_set(self):
        """Set a database variable """
        print ("SET")
        self.cleanup()
        try:
            engine = ddb.engine(config_dir=self.config_dir)
            
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
            ddb.output.factory.output_factory(query_results=results,output='TERM')
            self.assertEqual(True, results.success)
            
        except Exception as ex:
            print( ex)
            self.fail(ex)
    
    def _test_use(self,mode=None):
        #"""Test changing database context"""
        #try:
            print("USE")
            # single db change from default
            self.cleanup()
            engine = ddb.engine(config_dir=self.config_dir,debug=None)
            self.create_table(engine,mode)
                 
            
            results = engine.query("use {}".format(self.table_name))
            self.assertEqual(True, results.success)
            results = engine.query("select database()")
            self.assertEqual(True, results.success)
        #except Exception as ex:
        #    self.fail(ex)
    
    def test_show_output_modules(self):
        """Test showint output modules and styles"""
        try:
            # single db change from default
            self.cleanup()
            engine = ddb.engine(config_dir=self.config_dir,debug=None)
            results = engine.query("show output modules")
            ddb.output.factory.output_factory(query_results=results,output='TERM')
            self.assertEqual(True, results.success)
        except Exception as ex: 
            print(ex)
            self.fail(ex)        

    def test_show_tables(self,mode=None):
        """Show all tables in the database"""
        self.cleanup()
        try:
            engine = ddb.engine(config_dir=self.config_dir)
            self.create_table(engine,mode)

            results = engine.query("SHOW TABLES")
            #results.debug()
            self.assertEqual(True, results.success)
            
            ddb.output.factory.output_factory(query_results=results,output='term')
        except Exception as ex:
            print(ex)
            self.fail(ex)

    def test_describe_table(self,mode=None):
        """Show table configuration"""
        print ("DESCRIBE TABLE")
        self.cleanup()
        try:

            engine = ddb.engine(config_dir=self.config_dir)
            self.create_table(engine,mode)

            results = engine.query("DESCRIBE TABLE {0}".format(self.table_name))
            ddb.output.factory.output_factory(query_results=results,output='term')
            self.assertEqual(True, results.success)
        except Exception as ex:
            print(ex)
            self.fail(ex)

    def test_create_table(self,mode=None):
        """Test creating a table"""
        try:
            self.cleanup()
            engine = ddb.engine(config_dir=self.config_dir)
        
            self.create_table(engine,mode)
        except Exception as ex:
            self.fail(ex)

        # fail on existing table
        results=engine.query("create table {} ('id','first_name','last_name','email','gender','ip_address') file='{}' data_starts_on=2".format(self.table_name, os.path.join(self.basedir, self.temp_data)))
        self.assertEqual(False, results.success)

    def test_drop_table(self,mode=None):
        """Test dropping a table"""
        self.cleanup()
        engine = ddb.engine(config_dir=self.config_dir,debug=None)
        
        self.create_table(engine,mode)
        try:
        
            # fail on existing table
            results = engine.query('drop table {}'.format(self.table_name))
            self.assertEqual(True, results.success)
            
            # fail on dropping non existant table
           # results=engine.query('drop table {}'.format(self.table_name))
           # self.assertEqual(False, results.success)
        except Exception as ex:
            print (ex)
            self.fail(ex)

    def test_select(self,mode=None):
        """Test selecting results using various clauses a table"""
        #try:
        print("SELECT")
        self.cleanup()
        engine = ddb.engine(config_dir=self.config_dir,debug=None)
        # fail on existing table
        
        self.create_table(engine,mode)
        
         # test results length
        
        results = engine.query('select * from {0} LIMIT 10'.format(self.table_name))
        self.assertEqual(True, results.success)
        self.assertEqual(10, results.data_length)

        results = engine.query('select * from {0} LIMIT 1'.format(self.table_name))
        self.assertEqual(True, results.success)
        self.assertEqual(1, results.data_length)

        results = engine.query('select * from {0} LIMIT 0'.format(self.table_name))
        self.assertEqual(True, results.success)
        self.assertEqual(0, results.data_length)
        
        # WHERE/LIMIT
        results = engine.query('select * from {0} where id="1" order by id LIMIT 100;'.format(self.table_name))
        self.assertEqual(True, results.success)
        self.assertEqual(1, results.data_length)
        
        # WHERE AND/LIMIT
        results = engine.query('select * from {0} where id="1" and id not "2" order by id LIMIT 100;'.format(self.table_name))
        self.assertEqual(True, results.success)
        self.assertEqual(1, results.data_length)

        # WHERE / AND / OR/LIMIT
        results = engine.query('select * from {0} where id="1" and id not "2" or id="3" order by id LIMIT 100;'.format(self.table_name))
        self.assertEqual(True, results.success)
        self.assertEqual(2, results.data_length)
        #except Exception as ex:
        #    self.fail(ex)

    def test_update(self,mode=None):
        """Update a row in the test file"""
        try:
            self.cleanup()
            print("UPDATE")
            engine = ddb.engine(config_dir=self.config_dir,debug=None)
            # fail on existing table
            self.create_table(engine,mode)
            
            results = engine.query("insert into {} ('id','first_name','last_name','email','gender','ip_address') values (1002,test_name,test_lname,'bop@bob.com','m','0.0.0.0')".format(self.table_name))
            print("UPDATE 1")
            self.assertEqual(True, results.success)
            # update
            results = engine.query('update {} set email="test@test.com" where id="1002"'.format(self.table_name))
            print("UPDATE 2")
            self.assertEqual(True, results.success)
            
            results = engine.query("delete from {} where id='1002'".format(self.table_name))
            print("UPDATE 3")
            self.assertEqual(True, results.success)

        except Exception as ex:
            print(ex)
            self.fail(ex)

    def test_insert(self,mode=None):
        """Insert a row in the test file"""
        #try:
        self.cleanup()
        print("INSERT")
        engine = ddb.engine(config_dir=self.config_dir,debug=self.debug)
        self.cleanup()
        # fail on existing table
        self.create_table(engine,mode)

        # update
        results = engine.query("insert into {} ('id','first_name','last_name','email','gender','ip_address') values (1001,test_name,test_lname,'bop@bob.com','m','0.0.0.0')".format(self.table_name))
        #results.debug()
        self.assertEqual(True, results.success)
        # Delete
        results = engine.query("delete from {} where id='1001'".format(self.table_name))
        self.assertEqual(True, results.success)

        #except Exception as ex:
        #    self.fail(ex)

    def test_delete(self,mode=None):
        """Delete a test row in the test file"""
        self.cleanup()
        print("DELETE")
        try:
            engine = ddb.engine(config_dir=self.config_dir)
            self.create_table(engine,mode)
            results = engine.query("insert into {} ('id','first_name','last_name','email','gender','ip_address') values (1003,test_name,test_lname,'bop@bob.com','m','0.0.0.0')".format(self.table_name))
            self.assertEqual(True, results.success)
            # delete just inserted
            print ("DELETE 2")
            results = engine.query("delete from {} where id='1003'".format(self.table_name))
            self.assertEqual(True, results.success)

            print ("DELETE 3")
            # delete non existing
            results = engine.query("delete from {} where email like 'bop@%'".format(self.table_name))
            self.assertEqual(True, results.success)
     
        except Exception as ex:
            print(ex)
            self.fail(ex)
    
    def test_upsert(self,mode=None):
        """Show all tables in the database"""
        self.cleanup()
        print("UPSERT")

        #try:
        engine = ddb.engine(config_dir=self.config_dir,debug=None)
        self.create_table(engine,mode)

        results = engine.query("upsert into {} ('id','first_name','last_name','email','gender','ip_address') values (1006,test_name,test_lname,'tag@bob.com','m','0.0.0.0') ON DUPLICATE KEY id UPDATE id='12345' ".format(self.table_name))
        self.assertEqual(True, results.success)

        results = engine.query("select * from  {} where id = 1006".format(self.table_name))
        self.assertEqual(1, results.data_length)
        
        results = engine.query("upsert into {} ('id','first_name','last_name','email','gender','ip_address') values (1006,test_name,test_lname,'tag@bob.com','m','0.0.0.0') ON DUPLICATE KEY id UPDATE id='12345' ".format(self.table_name))
        self.assertEqual(True, results.success)

        results = engine.query("select * from  {} where id = 12345".format(self.table_name))
        self.assertEqual(1, results.data_length)
        
        results = engine.query("delete from {} where id = 12345".format(self.table_name))
        self.assertEqual(1, results.affected_rows)

        ddb.output.factory.output_factory(query_results=results,output='term')
        #except Exception as ex:
        #    print(ex)
        #    self.fail(ex)

    def test_rollback(self,mode=None):
        """Rollback db changes"""
        self.cleanup()
        print("ROLLBACK")
        try:
            engine = ddb.engine(config_dir=self.config_dir)

            self.create_table(engine,mode)

            print ("Begin")
            results = engine.query("begin")
            self.assertEqual(True, results.success)
            # update
            print ("Insert")
            results = engine.query("insert into {0} ('id','first_name','last_name','email','gender','ip_address') values (1001,test_name,test_lname,'bop@bob.com','m','0.0.0.0')".format(self.table_name))
            print ("Insert")
            results = engine.query("insert into {0} ('id','first_name','last_name','email','gender','ip_address') values (1001,test_name,test_lname,'bop@bob.com','m','0.0.0.0')".format(self.table_name2))
            self.assertEqual(True, results.success)

            print ("Select")
            results = engine.query("SELECT id FROM {0}".format(self.table_name) )
            
            self.assertEqual(True, results.success)
            self.assertEqual(1002, results.data_length)
            #results.debug()

            print ("rollback")
            results = engine.query("rollback")
            self.assertEqual(True, results.success)
            
            results = engine.query("SELECT id FROM {0}".format(self.table_name) )
            #results.debug()
            self.assertEqual(True, results.success)
            self.assertEqual(1000, results.data_length)
                
            
        except Exception as ex:
            print (ex)
            self.fail(ex)

    def test_commit(self,mode=None):
        """Rollback db changes"""
        try:
            self.cleanup()
            print("COMMIT")
            engine = ddb.engine(config_dir=self.config_dir)

            self.create_table(engine,mode)

            print ("PRE BEGIN")
            results = engine.query("begin")
            self.assertEqual(True, results.success)
            
            print ("PRE DELETE")
            # clean any inserts
            results = engine.query("delete from {0} WHERE email='bop@bob.com'".format(self.table_name))
            self.assertEqual(True, results.success)

            print ("PRE INSERT")
            # update
            results = engine.query("insert into {0} ('id','first_name','last_name','email','gender','ip_address') values (1001,test_name,test_lname,'bop@bob.com','m','0.0.0.0')".format(self.table_name))
            #results.debug()
            self.assertEqual(True, results.success)

            print ("PRE SELECT")
            results = engine.query("SELECT id FROM {0}".format(self.table_name) )
            #results.debug()
            self.assertEqual(True, results.success)
            self.assertEqual(1001, results.data_length)
            #results.debug()

            print ("PRE COMMIT")
            results = engine.query("commit")
            print (results.error)
            self.assertEqual(True, results.success)
            
            print ("PRE SELECT")
            results = engine.query("SELECT id FROM {0}".format(self.table_name) )
            #results.debug()
            self.assertEqual(True, results.success)
            self.assertEqual(1001, results.data_length)
            
            print ("PRE DELETE")
            results = engine.query("delete from {} where id='1001'".format(self.table_name))
            self.assertEqual(True, results.success)
                
            
        except Exception as ex:
            self.fail(ex)

    ##### SVN
    ##### SVN
    ##### SVN

#    def _test_svn_create_table(self):
#        self.test_create_table(mode='SVN')
#
#    def _test_svn_drop_table(self):
#        self.test_drop_table(mode='SVN')
#
#    def _test_svn_select(self):
#        self.test_select(mode='SVN')
#
#    def _test_svn_update(self):
#        self.test_update(mode='SVN')
#
#    def _test_svn_insert(self):
#        self.test_insert(mode='SVN')
#
#    def _test_svn_delete(self):
#        self.test_delete(mode='SVN')
#
#    def _test_svn_upsert(self):
#        self.test_upsert(mode='SVN')
#
#    def _test_svn_rollback(self):
#        self.test_rollback(mode='SVN')
#
#    def _test_svn_commit(self):
#        self.test_commit(mode='SVN')
#
#    def _test_svn_describe_table(self):
#        self.test_describe_table(mode='SVN')
#    
#    def _test_svn_show_tables(self):
#        self.test_show_tables(mode='SVN')


if __name__ == '__main__':
    unittest.main()




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
# except Exception as ex:
#   print ex
# 
# print ("Access of data from invalid key")
# try:
#   print data.c34
# except Exception as ex:
#   print ex