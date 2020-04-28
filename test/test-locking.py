import unittest
import os
import sys
import datetime
import signal
from pprint import pprint
#import cProfile 
#import pstats
import time

print ("Locking Test")

standalone_script=None

#pprint(os.environ,indent=4)
print ("TESTING")
if 'DDB_RELEASE_DIR' in os.environ:
    print ("Found test dir")
    standalone_script=os.environ['DDB_RELEASE_DIR']


if standalone_script!=None:
    path= os.path.abspath(os.path.join(os.path.dirname(__file__),standalone_script))
    sys.path.insert(0,path)
    print (path)
    try:
        from ddb import ddb
    except:
        print ("DDB STANDALONE FAILED")
        ex=sys.exc_info()[1]
        print (ex)
        sys.exit(1)
    print ("DDB STANDALONE")
else:
    path= os.path.abspath(os.path.join(os.path.dirname(__file__), '../source/'))
    #path= os.path.abspath(os.path.join(os.path.dirname(__file__), '../builds/single/ddb/'))
    print(path)
    sys.path.insert(0,path)

    try:
        import ddb
    except:
        print ("DDB CYTHON FAILED")
        ex=sys.exc_info()[1]
        print (ex)
        sys.exit(1)
    print ("DDB CYTHON")

running=0



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
            query="create temporary table @db.@table (`id`,`pid`,`value`,`timestamp`) file=@path data_starts_on=1"
        else:
            query="create temporary table @db.@table (`id`,`pid`,`value`,`timestamp`) file='@path' @repo data_starts_on=1"
        params={'@db':self.database_name,
                '@table':self.table_name, 
                '@path':file_name,
                '@repo':repo}

        results = engine.query(query,params)
        
        #results.debug()
        #self.assertEqual(True, results.success)

 
    def test_threads(self,mode=None):
        global running
        """Test inserting values in a table with locking"""
        #try:
        process_count=30
        pid=os.getpid()
        print("Locking: %d"% pid)
        # fail on existing table
        self.cleanup()
        self.init(mode)

        for i in range(process_count-1):
            #time.sleep(1)
            newpid = os.fork()
            if newpid:
                running+=1
            else:
                break
        
        if newpid==0: self.lock()
        else:
            for i in range(process_count-1):
                running -=1
                pid, status = os.wait()
                status_calc=(status >> 8)
                print('Parent got', pid, status, status_calc,running)
                if status_calc!=0:
                    print("Failed")
            
        return newpid
        
        
    def lock(self):
        engine = ddb.engine(config_dir=None,debug=None)
        self.create_table(engine,None)
        start_time=time.time()
        ellapsed_time=0
        pid=os.getpid()
        value=1
        # test results length
        insert_count=100
        for i in range(0,insert_count):
            timestamp=datetime.datetime.now()

            query="INSERT INTO @db.@table (`id`,`pid`,`value`,`timestamp`) values (@id,@pid,@value,@timestamp)"
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

        query="SELECT id FROM  @db.@table WHERE `pid`=@pid"
        params={
                '@db'       :self.database_name,
                '@table'    :self.table_name,
                '@id'       :i,
                '@pid'      :pid,
                }
                
        results = engine.query(query,params)
        if results.data_length!=insert_count:
            sys.exit(-1)
        

        curent_time=time.time()
        ellapsed_time=curent_time-start_time
        #print ("Ellapsed: %d ,%d" % (ellapsed_time,i))
    

        
if __name__ == '__main__':
    e=test_engine()
    pid=e.test_threads()

    #def chld_handler(signo, frame):
    #    global running
    #    running -= 1
    #    if running<=0:
    #        print("Lock Test Complete")
    #        sys.exit()
#
    #signal.signal(signal.SIGCHLD, chld_handler)

    #if pid!=0:
    #   while(1): time.sleep(1)



    #cProfile.run('test_engine().lock()', 'restats')
    #p = pstats.Stats('restats')
    #p.strip_dirs().sort_stats(-1).print_stats()

