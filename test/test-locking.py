import unittest
import os
import sys
import datetime
from pprint import pprint
import cProfile 
import pstats
import time


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

        
        if repo=="":
            query="create table @db.@table (`id`,`pid`,`value`,`timestamp`) file='@path' data_starts_on=1"
        else:
            query="create table @db.@table (`id`,`pid`,`value`,`timestamp`) file='/ddb/bb' @repo data_starts_on=1"
        params={'@db':self.database_name,
                '@table':self.table_name, 
                '@path':file_name,
                '@repo':repo}
        #print query
        print(engine.prepare_sql(query,params))
        results = engine.query(query,params)
        
        results.debug()
        #self.assertEqual(True, results.success)

    def test_threads(self,mode=None):
        """Test inserting values in a table with locking"""
        #try:
        process_count=90
        pid=os.getpid()
        print("Locking: %d"% pid)
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
        try:
            engine = ddb.engine(config_dir=None,debug=None)
            self.create_table(engine,None)
            start_time=time.time()
            ellapsed_time=0
            pid=os.getpid()
            value=1
            
            # test results length
            for i in range(0,100):
                timestamp=datetime.datetime.now()

                query="INSERT INTO @db.@table (`id`,`pid`,`value`,`timestamp`) values ('@id','@pid','@value','@timestamp')"
                params={
                        '@db'       :self.database_name,
                        '@table'    :self.table_name,
                        '@id'       :i,
                        '@pid'      :pid,
                        '@value'    :value,
                        '@timestamp':timestamp
                        }
                        
                results = engine.query(query,params)
                #self.assertEqual(True, results.success)

            curent_time=time.time()
            ellapsed_time=curent_time-start_time
            print ("Ellapsed: %d ,%d" % (ellapsed_time,i))
        except:
            ex=sys.exc_info()[1]
            print (ex)


if __name__ == '__main__':
    e=test_engine()
    e.test_threads()
    #cProfile.run('test_engine().lock()', 'restats')
    #p = pstats.Stats('restats')
    #p.strip_dirs().sort_stats(-1).print_stats()

