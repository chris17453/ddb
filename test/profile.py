import os
import sys
import cProfile 
import pstats
from .context import ddb
from subprocess import Popen,PIPE

class test_profile:
    temp_config = 'temp_config.yaml'
    temp_data = 'MOCK_DATA_LARGE.csv'
    basedir = os.path.dirname(os.path.abspath(__file__))+"/data/"
    table_name = 'test'
    debug=None
    loop=1

    def cleanup(self):
        # print ("#--->Fresh init")
        config_dir = os.path.join(self.basedir, self.temp_config)
        if os.path.exists(config_dir):
           #print "Config file: {}".format(config_dir)
           os.remove(config_dir)
        #if os.path.exists(config_dir):
            #print("Still here")

    def create_table(self,engine,mode):
        if mode=='SVN':
            repo="repo='{0}' url='{1}' user='{2}' password='{3}' repo_dir='{4}' repo_file='{5}'".format(
                'svn',
                'http://localhost/svn/SampleProject/',
                'user',
                'password',
                os.path.join(self.basedir,'svn_test'),
                'MOCK_DATA.csv')
            file_name=os.path.join(self.basedir,'svn_test',"MOCK_DATA.csv")
            
        else:
            repo=''
            file_name=os.path.join(self.basedir, self.temp_data)
       
        query="create table {0}('id','first_name','last_name','email','gender','ip_address') file='{1}' {2} data_starts_on=2".format(self.table_name, file_name,repo)
        results = engine.query(query)
        

    def select(self,mode=None):
        self.cleanup()
        engine = ddb.engine(config_dir=self.basedir,debug=None)
        self.create_table(engine,mode)
        for a in range(0,self.loop):
            results = engine.query("select * from {0}".format(self.table_name))
    
    def select_o(self,mode=None):
        self.cleanup()
        engine = ddb.engine(config_dir=self.basedir,debug=None)
        self.create_table(engine,mode)
        for a in range(0,self.loop):
           results = engine.query("select * from {0} order by id desc".format(self.table_name))
    
    def select_w(self,mode=None):
        self.cleanup()
        engine = ddb.engine(config_dir=self.basedir,debug=None)
        self.create_table(engine,mode)
        for a in range(0,self.loop):
           results = engine.query("select * from {0} where id like '%1'".format(self.table_name))

    def select_wo(self,mode=None):
        self.cleanup()
        engine = ddb.engine(config_dir=self.basedir,debug=None)
        self.create_table(engine,mode)
        for a in range(0,self.loop):
            results = engine.query("select * from {0} where id like '%1' order by id desc".format(self.table_name))

    def select_wol(self,mode=None):
        self.cleanup()
        engine = ddb.engine(config_dir=self.basedir,debug=None)
        self.create_table(engine,mode)
        results = engine.query("select * from {0} where id like '%1' order by id desc limit 10".format(self.table_name))
    
    

def os_cmd(cmd,err_msg):
    p = Popen(cmd, stdin=PIPE, stdout=PIPE, stderr=PIPE)
    output, err = p.communicate()
    rc = p.returncode
    if rc!=0:
        print(output)
        print(err)
        raise Exception("{0}: Exit Code {1}".format(err_msg,rc))
    return output
    

run=['select','select_w','select_o','select_wo','select_wol']

dirs=[  "profile/{0}".format(ddb.version.__version__),
        "profile/{0}/proc".format(ddb.version.__version__),
        "profile/{0}/callgraph".format(ddb.version.__version__)
]
print ("Director creation")
for dir in dirs:
    if os.path.exists(dir)==False:
        os.mkdir(dir)
        print("Created Directory {0}".format(dir))

print ("Function execution")

for func in run:
    profile_name="profile/{0}/proc/{1}.prof".format(ddb.version.__version__,func)
    callgraph_name="profile/{0}/callgraph/{1}.png".format(ddb.version.__version__,func)
    if os.path.exists(profile_name)==True:
        os.remove(profile_name)
        print("Deleted {0}".format(profile_name))
    cProfile.runctx("test_profile().{0}()".format(func)   , globals(), locals(), profile_name)
    
    print profile_name
    s = pstats.Stats(profile_name)
    s.strip_dirs().sort_stats("time").print_stats()
    print "gprof2dot -f pstats {0} | dot -Tpng -o output.png".format(profile_name)
    print 'test/callgraph.sh',profile_name,callgraph_name
    os_cmd(['test/callgraph.sh',profile_name,callgraph_name],"Callgrapoh failed")

