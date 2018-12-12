import unittest
import os
from engine.sql_engine  import sql_engine




class test_engine(unittest.TestCase):
    temp_config='test/temp_config.yaml'
    temp_data='test/MOCK_DATA.csv'
    basedir=os.path.dirname(os.path.abspath(__file__))

    def test__init(self):
        if os.path.exists(self.temp_config):
            os.remove(self.temp_config) 
        


    def test_use(self):
        """Test changing database context"""

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
        engine=sql_engine(config_file=os.path.join(self.basedir,self.temp_config))
        #new on existing table
        results=engine.query("create table test('id','first_name','last_name','email','gender','ip_address') file='{}'".format(os.path.join(self.basedir,self.temp_data)) )
        self.assertEqual(1,results[0][0])

        #fail on existing table
        with self.assertRaises(Exception) :
            engine.query("create table test('id','first_name','last_name','email','gender','ip_address') file='{}'".format(os.path.join(self.basedir,self.temp_data)) )
            

    def test_drop_table(self):
        """Test dropping a table"""
        engine=sql_engine(config_file=os.path.join(self.basedir,self.temp_config))
        #fail on existing table
        results=engine.query('drop table test')
        self.assertEqual(1,results[0][0])
        
        #fail on dropping non existant table
        with self.assertRaises(Exception) :
            engine.query('drop table test')
        


    #def test_select(self):
    #def test_update(self):
    #def test_insert(self):

if __name__=='__main__':
    unittest.main()