import unittest
import os
import sys
from .context import  ddb
from pprint import pprint
import cProfile as profile
import pstats
import time

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
       
        query="create temporary table {0} ('id','first_name','last_name','email','gender','ip_address') file='{1}' {2} data_starts_on=2".format(self.table_name, file_name,repo)
        #print query
        results = engine.query(query)
        self.assertEqual(True, results.success)
        query="create temporary table {0} ('id','first_name','last_name','email','gender','ip_address') file='{1}' {2} data_starts_on=2".format(self.table_name2, file_name,repo)
        #print ""
        #print query
        #print ""
        results = engine.query(query)
        self.assertEqual(True, results.success)

    def test_select(self,mode=None):
        """Test selecting results using various clauses a table"""
        #try:
        print("SELECT")
        engine = ddb.engine(config_dir=None,debug=None)
        # fail on existing table
        self.cleanup()
        self.create_table(engine,mode)
        start_time=time.time()

        run_length=10
        ellapsed_time=0
         # test results length
        while ellapsed_time<run_length:
            curent_time=time.time()
            ellapsed_time=curent_time-start_time

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


if __name__ == '__main__':
    unittest.main()
