import unittest
from engine.sql_engine  import sql_engine




class test_engine(unittest.TestCase):
    #def __init__(self):
        
    def test_use(self):
        engine=sql_engine(config_file=False)
        test_db_name="TEST"
        results=engine.query("use {}".format(test_db_name))
        results=engine.query("select database()")
        self.assertEqual(results[0][0],test_db_name)
    
    #def test_create_table(self):
    #    engine=sql_engine(database_dir=None,config_file=None,query=None,debug=False,mode='array')

    #def test_drop_table(self):
    #def test_select(self):
    #def test_update(self):
    #def test_insert(self):

if __name__=='__main__':
    unittest.main()