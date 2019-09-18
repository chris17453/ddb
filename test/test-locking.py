import unittest
import os
import sys
import datetime
from .context import  ddb
from pprint import pprint
import cProfile 
import pstats
import time

class test_engine:
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

    def init(self,mode):
        if mode=='SVN':
            file_name=os.path.join(self.basedir_svn,'svn_test',self.temp_data)
        else:
            file_name=os.path.join(self.basedir, self.temp_data)

        if os.path.exists(file_name)==False:
            file=open(file_name, 'w')
            file.close()
        else:
            file=open(file_name, 'w')
            file.truncate()
            file.close()


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

        query="create temporary table {0}.{1} ('id','pid','value','timestamp') file='{2}' {3} data_starts_on=1".format(self.database_name,self.table_name, file_name,repo)
        #print query
        results = engine.query(query)
        #self.assertEqual(True, results.success)

    def test_threads(self,mode=None):
        """Test inserting values in a table with locking"""
        #try:
        process_count=30
        print("Locking: {0}".format(os.getpid()))
        # fail on existing table
        self.cleanup()
        self.init(mode)
        
        for i in range(process_count-1):
            #time.sleep(1)
            newpid = os.fork()
            if newpid!=0:
                break

        
        self.lock()
        
    def lock(self):
        engine = ddb.engine(config_dir=None,debug=None)
        self.create_table(engine,None)
        start_time=time.time()
        ellapsed_time=0
        pid=os.getpid()
        value=1
        
        # test results length
        for i in range(0,20):
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
            #self.assertEqual(True, results.success)

        curent_time=time.time()
        ellapsed_time=curent_time-start_time
        print ("Ellapsed: {0},{1}".format(ellapsed_time,i))


if __name__ == '__main__':
    #unittest.main()
    e=test_engine()
    e.test_threads()
    #cProfile.run('test_engine().lock()', 'restats')
    #p = pstats.Stats('restats')
    #p.strip_dirs().sort_stats(-1).print_stats()

