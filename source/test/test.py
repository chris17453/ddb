import unittest
import os
import sys
from .context import  ddb
from pprint import pprint

class test_engine(unittest.TestCase):
    temp_config = 'temp_config.yaml'
    temp_data = 'MOCK_DATA.csv'
    basedir = os.path.dirname(os.path.abspath(__file__))
    table_name = 'test'
    debug=False
    def cleanup(self):
        # print ("#--->Fresh init")
        config_file = os.path.join(self.basedir, self.temp_config)
        if os.path.exists(config_file):
           #print "Config file: {}".format(config_file)
           os.remove(config_file)
        #if os.path.exists(config_file):
            #print("Still here")

    def t1est_use(self):
        """Test changing database context"""
        try:
            # single db change from default
            self.cleanup()
            engine = ddb.engine(config_file=False)
            test_db_name = self.table_name
            results = engine.query("use {}".format(test_db_name))
            self.assertEqual(True, results.success)
            results = engine.query("select database()")
            self.assertEqual(True, results.success)
        except Exception as ex:
            self.fail(ex)
    
    def t1est_show_output_modules(self):
        """Test showint output modules and styles"""
        try:
            # single db change from default
            self.cleanup()
            engine = ddb.engine(config_file=False,debug=False)
            results = engine.query("show output modules")
            ddb.output.factory.output_factory(query_results=results,output='TERM')
            self.assertEqual(True, results.success)
        except Exception as ex: 
            print(ex)
            self.fail(ex)

    def t1est_create_table(self):
        """Test creating a table"""
        try:
            self.cleanup()
            engine = ddb.engine(config_file=os.path.join(self.basedir, self.temp_config))
            # new on existing table
            results = engine.query("create table {} ('id','first_name','last_name','email','gender','ip_address') file='{}' data_starts_on=2".format(self.table_name, os.path.join(self.basedir, self.temp_data)))
            self.assertEqual(True, results.success)
        except Exception as ex:
            self.fail(ex)

        # fail on existing table
        results=engine.query("create table {} ('id','first_name','last_name','email','gender','ip_address') file='{}' data_starts_on=2".format(self.table_name, os.path.join(self.basedir, self.temp_data)))
        self.assertEqual(False, results.success)

    def t1est_drop_table(self):
        """Test dropping a table"""
        self.cleanup()
        engine = ddb.engine(config_file=os.path.join(self.basedir, self.temp_config))
        results = engine.query("create table {} ('id','first_name','last_name','email','gender','ip_address') file='{}' data_starts_on=2".format(self.table_name, os.path.join(self.basedir, self.temp_data)))
        self.assertEqual(True, results.success)
        try:
        
            # fail on existing table
            results = engine.query('drop table {}'.format(self.table_name))
            self.assertEqual(True, results.success)
            
            # fail on dropping non existant table
            results=engine.query('drop table {}'.format(self.table_name))
            self.assertEqual(False, results.success)
        except Exception as ex:
            self.fail(ex)

    def test_select(self):
        """Test selecting results using various clauses a table"""
        try:
            self.cleanup()
            engine = ddb.engine(config_file=os.path.join(self.basedir, self.temp_config),debug=None)
            # fail on existing table
            results = engine.query("create table {0}('id','first_name','last_name','email','gender','ip_address') file='{1}' data_starts_on=2".format(self.table_name, os.path.join(self.basedir, self.temp_data)))
            self.assertEqual(True, results.success)
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
        except Exception as ex:
            self.fail(ex)

    def t1est_update(self):
        """Update a row in the test file"""
        try:
            self.cleanup()
            engine = ddb.engine(config_file=os.path.join(self.basedir, self.temp_config),debug=None)
            # fail on existing table
            results = engine.query("create table {}('id','first_name','last_name','email','gender','ip_address') file='{}' data_starts_on=2".format(self.table_name, os.path.join(self.basedir, self.temp_data)))
            self.assertEqual(True, results.success)
            
            results = engine.query("insert into {} ('id','first_name','last_name','email','gender','ip_address') values (1002,test_name,test_lname,'bop@bob.com','m','0.0.0.0')".format(self.table_name))
            self.assertEqual(True, results.success)
            # update
            results = engine.query('update {} set email="test@test.com" where id="1002"'.format(self.table_name))
            self.assertEqual(True, results.success)
            
            results = engine.query("delete from {} where id='1002'".format(self.table_name))
            self.assertEqual(True, results.success)

        except Exception as ex:
            print(ex)
            self.fail(ex)

    def test_insert(self):
        """Insert a row in the test file"""
        try:
            self.cleanup()
            engine = ddb.engine(config_file=os.path.join(self.basedir, self.temp_config),debug=self.debug)
            self.cleanup()
            # fail on existing table
            results = engine.query("create table {} ('id','first_name','last_name','email','gender','ip_address') file='{}' data_starts_on=2".format(self.table_name, os.path.join(self.basedir, self.temp_data)))
            self.assertEqual(True, results.success)

            # update
            results = engine.query("insert into {} ('id','first_name','last_name','email','gender','ip_address') values (1001,test_name,test_lname,'bop@bob.com','m','0.0.0.0')".format(self.table_name))
            self.assertEqual(True, results.success)
            # Delete
            results = engine.query("delete from {} where id='1001'".format(self.table_name))
            self.assertEqual(True, results.success)

        except Exception as ex:
            self.fail(ex)

    def t1est_delete(self):
        """Delete a test row in the test file"""
        self.cleanup()
        try:
            engine = ddb.engine(config_file=os.path.join(self.basedir, self.temp_config))
            results = engine.query("create table {} ('id','first_name','last_name','email','gender','ip_address') file='{}' data_starts_on=2".format(self.table_name, os.path.join(self.basedir, self.temp_data)))
            self.assertEqual(True, results.success)

            results = engine.query("insert into {} ('id','first_name','last_name','email','gender','ip_address') values (1003,test_name,test_lname,'bop@bob.com','m','0.0.0.0')".format(self.table_name))
            self.assertEqual(True, results.success)
            # delete just inserted
            results = engine.query("delete from {} where id='1003'".format(self.table_name))
            self.assertEqual(True, results.success)

            # delete non existing
            results = engine.query("delete from {} where email like 'bop@%'".format(self.table_name))
            self.assertEqual(True, results.success)
     
        except Exception as ex:
            print(ex)
            self.fail(ex)

    def t1est_show_tables(self):
        """Show all tables in the database"""
        self.cleanup()
        try:
            engine = ddb.engine(config_file=os.path.join(self.basedir, self.temp_config))
            results = engine.query("create table {} ('id','first_name','last_name','email','gender','ip_address') file='{}' data_starts_on=2".format(self.table_name, os.path.join(self.basedir, self.temp_data)))
            self.assertEqual(True, results.success)

            results = engine.query("SHOW TABLES")
            self.assertEqual(True, results.success)
            
            ddb.output.factory.output_factory(query_results=results,output='term')
        except Exception as ex:
            print(ex)
            self.fail(ex)

    def t1est_describe_table(self):
        """Show table configuration"""
        self.cleanup()
        try:
            engine = ddb.engine(config_file=os.path.join(self.basedir, self.temp_config))
            results = engine.query("create table {} ('id','first_name','last_name','email','gender','ip_address') file='{}' data_starts_on=2".format(self.table_name, os.path.join(self.basedir, self.temp_data)))
            self.assertEqual(True, results.success)

            results = engine.query("DESCRIBE TABLE {0}".format(self.table_name))
            ddb.output.factory.output_factory(query_results=results,output='term')
            self.assertEqual(True, results.success)
        except Exception as ex:
            print(ex)
            self.fail(ex)
    
    def t1est_upsert(self):
        """Show all tables in the database"""
        self.cleanup()
        #try:
        engine = ddb.engine(config_file=os.path.join(self.basedir, self.temp_config),debug=None)
        results = engine.query("create table {} ('id','first_name','last_name','email','gender','ip_address') file='{}' data_starts_on=2".format(self.table_name, os.path.join(self.basedir, self.temp_data)))
        self.assertEqual(True, results.success)

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

    def t1est_set(self):
        """Set a database variable """
        self.cleanup()
        try:
            engine = ddb.engine(config_file=os.path.join(self.basedir, self.temp_config))

            
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
            self.fail(ex)

if __name__ == '__main__':
    unittest.main()






