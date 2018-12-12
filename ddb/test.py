import unittest
import os
from engine.sql_engine  import sql_engine




class test_engine(unittest.TestCase):
    temp_config='test/temp_config.yaml'
    temp_data='test/MOCK_DATA.csv'
    basedir=os.path.dirname(os.path.abspath(__file__))

    def test_init(self):
        config_dir=os.path.join(self.basedir,self.temp_config)
        if os.path.exists(config_dir):
            os.remove(config_dir) 
        

    def test_use(self):
        """Test changing database context"""
        print("Use")

        # single db change from default
        engine=sql_engine(config_file=False)
        test_db_name="TEST"
        results=engine.query("use {}".format(test_db_name))
        results=engine.query("select database()")
        self.assertEqual(results[0][0],test_db_name)
    
        # default context check
        engine=sql_engine(config_file=False)
        results=engine.query("select database()")
        self.assertEqual("main",results[0][0])


    def test_create_table(self):
        """Test creating a table"""
        print("Create Table")
        engine=sql_engine(config_file=os.path.join(self.basedir,self.temp_config))
        #new on existing table
        results=engine.query("create table test('id','first_name','last_name','email','gender','ip_address') file='{}'".format(os.path.join(self.basedir,self.temp_data)) )
        self.assertEqual(1,results[0][0])

        #fail on existing table
        with self.assertRaises(Exception) :
            engine.query("create table test('id','first_name','last_name','email','gender','ip_address') file='{}'".format(os.path.join(self.basedir,self.temp_data)) )
        #drop test table
        engine.query("drop table test")
            

    def test_drop_table(self):
        """Test dropping a table"""
        print("Drop Table")
        engine=sql_engine(config_file=os.path.join(self.basedir,self.temp_config))
        results=engine.query("create table test('id','first_name','last_name','email','gender','ip_address') file='{}'".format(os.path.join(self.basedir,self.temp_data)) )
                #fail on existing table
        results=engine.query('drop table test')
        self.assertEqual(1,results[0][0])
        
        #fail on dropping non existant table
        with self.assertRaises(Exception) :
            engine.query('drop table test')
        


    def test_select(self):
        """Test selecting results using various clauses a table"""
        engine=sql_engine(config_file=os.path.join(self.basedir,self.temp_config))
        print("Select")
        #fail on existing table
        results=engine.query("create table test('id','first_name','last_name','email','gender','ip_address') file='{}'".format(os.path.join(self.basedir,self.temp_data)) )
        
        # test results length
        results=engine.query('select * from test LIMIT 10')
        self.assertEqual(10,len(results))
        results=engine.query('select * from test LIMIT 1')
        self.assertEqual(1,len(results))
        results=engine.query('select * from test LIMIT 0')
        self.assertEqual(0,len(results))
        
        #WHERE/LIMIT
        results=engine.query('select * from test where id="1" order by id LIMIT 100;')
        self.assertEqual(1,len(results))
        
        #WHERE AND/LIMIT
        results=engine.query('select * from test where id="1" and id not "2" order by id LIMIT 100;')
        self.assertEqual(1,len(results))

        #WHERE / AND / OR/LIMIT
        results=engine.query('select * from test where id="1" and id not "2" or id="3" order by id LIMIT 100;')
        self.assertEqual(2,len(results))

        engine.query("drop table test")



    def test_update(self):
        print("Update")
        engine=sql_engine(config_file=os.path.join(self.basedir,self.temp_config))
        #fail on existing table
        results=engine.query("create table test('id','first_name','last_name','email','gender','ip_address') file='{}'".format(os.path.join(self.basedir,self.temp_data)) )
        
        #update
        results=engine.query('update test set email="bob@pizza" where id="1" and id not "2" or id="3"')
        self.assertEqual(2,results[0][0])
             
        engine.query("drop table test")
    
    def test_insert(self):
        print("Insert")
        engine=sql_engine(config_file=os.path.join(self.basedir,self.temp_config))
        #fail on existing table
        results=engine.query("create table test('id','first_name','last_name','email','gender','ip_address') file='{}'".format(os.path.join(self.basedir,self.temp_data)) )
        
        #update
        results=engine.query("insert into test ('id','first_name','last_name','email','gender','ip_address') values (1001,test_name,test_lname,'bop@bob.com','m','0.0.0.0')")
        self.assertEqual(1,results[0][0])
            
        engine.query("drop table test")

    def test_delete(self):
        print("Delete")
        engine=sql_engine(config_file=os.path.join(self.basedir,self.temp_config))
        #fail on existing table
        results=engine.query("create table test('id','first_name','last_name','email','gender','ip_address') file='{}'".format(os.path.join(self.basedir,self.temp_data)) )
        
        #update non existant
        results=engine.query("delete from test where id='sam'")
        self.assertEqual(0,results[0][0])
            
        #update existing
        results=engine.query("delete from test where email like 'bop@%'")
        self.assertEqual(1,results[0][0])

        engine.query("drop table test")


if __name__=='__main__':
    unittest.main()