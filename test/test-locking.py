import unittest
import os
import sys
import datetime
from .context import  ddb
from pprint import pprint
import cProfile as profile
import pstats
import time

class test_engine(unittest.TestCase):
    temp_config = 'temp_config.yaml'
    temp_data = 'MOCK_DATA_LOCKING.csv'
    basedir = os.path.dirname(os.path.abspath(__file__))+"/data/"
    basedir_svn = os.path.dirname(os.path.abspath(__file__))
    database_name= 'test'
    table_name = 'locking'
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
                self.temp_data)
            file_name=os.path.join(self.basedir_svn,'svn_test',self.temp_data)
        else:
            repo=''
            file_name=os.path.join(self.basedir, self.temp_data)

        if os.path.exists(file_name)==False:
            open(file_name, 'w').close()
        else:
            open(file_name, 'w').truncate()


        query="create temporary table {0}.{1} ('id','pid','value','timestamp') file='{2}' {3} data_starts_on=1".format(self.database_name,self.table_name, file_name,repo)
        #print query
        results = engine.query(query)
        self.assertEqual(True, results.success)

    def test_locking(self,mode=None):
        """Test inserting values in a table with locking"""
        #try:
        print("Locking")
        engine = ddb.engine(config_dir=None,debug=None)
        # fail on existing table
        newpid = os.fork()

        if newpid==0:
            newpid = os.fork()

        if newpid==0:
            newpid = os.fork()

        if newpid==0:
            newpid = os.fork()

        if newpid==0:
            self.cleanup()
        
        self.create_table(engine,mode)
        start_time=time.time()

        run_length=10
        ellapsed_time=0

        id=0
        pid=os.getpid()
        value=1

        
        
         # test results length
        for i in range(0,100):
            print ("Ellapsed: {0},{1}".format(ellapsed_time,i))
            curent_time=time.time()
            ellapsed_time=curent_time-start_time
            timestamp=datetime.datetime.now()

            query="INSERT INTO {0}.{1} (`id`,`pid`,`value`,`timestamp`) values ('{2}','{3}','{4}','{5}')".format(
                    self.database_name,
                    self.table_name,
                    i,
                    pid,
                    value,
                    timestamp
                    )
            results = engine.query(query)
            self.assertEqual(True, results.success)



if __name__ == '__main__':
    unittest.main()
