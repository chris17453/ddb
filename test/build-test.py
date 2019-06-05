from subprocess import Popen, PIPE, STDOUT

from .context import ddb
import os
import time
import random

temp_dir='/tmp/temp_ddb'
base_dir='~/repos/chris17453/ddb/source/test/cast'
tar="/home/cwatkin1/repos/chris17453/ddb/builds/pypi/ddb-1.1.326.tar.gz"
exit_sleep=5



def send_cmd(process,cmd):
    process.stdin.write(cmd['input'])
    if None == cmd['no_return']:
        process.stdin.write("\n")
    print(cmd['input'])
    time.sleep(cmd['delay'])

def def_cmd(cmd,delay=0,no_return=None):
    return {'input':cmd,'delay':delay,'no_return':no_return}

def build_test_function(name,query):
    bash="ddb '{0}'".format(query)
    p = Popen(['bash'], shell=True,stdin=PIPE,stdout=PIPE)

    commands=[
        def_cmd("cd {0}".format(temp_dir)),
        def_cmd("rm {0}/{1}.cast".format(base_dir,name)),
        
        def_cmd("pipenv run asciinema rec {0}/{1}.cast".format(base_dir,name),.5),
        ]



    lines=bash.split(";")
    for line in lines:
        for c in line:
            if c==' ':
                delay=.2
            else: 
                delay=.1+random.randrange(0,1)/10
            commands.append(def_cmd(c,delay,no_return=True))
        commands.append(def_cmd('\n',.1,no_return=True))
    commands.append(def_cmd('exit',.1))
    commands.append(def_cmd('exit',.1))

    #send the commands
    for cmd in commands:
        send_cmd(p,cmd)


        

    


def create_test_environment():
    bash="mkdir {1};cd {1};pipenv install {0}".format(tar,temp_dir)
    os.system("gnome-terminal -e 'bash -c \"{0} \"; exit'".format(bash))
    time.sleep(3)
    

def destroy_test_environment():
    bash="cd {0};pipenv --rm;rm {0}/* -f;cd ..;rmdir {0} -f".format(temp_dir)
    os.system("gnome-terminal -e 'bash -c \"{0} \"; exit'".format(bash))


def build_test():

    # FUNCITONS TEST 
    for function in ddb.lexer.language.sql_syntax['functions']:
        name=function['name']
        query="SELECT {0}()".format(name)
        build_test_function(name,query)
        renamed_name="renamed_"+name
        query="SELECT {0}() as 'renamed_{1}'".format(name,renamed_name)
        build_test_function(renamed_name,query)
        break

    # functions
    # db='testdb'
    # table='mock_data'
    # q={}
    # q["SELECT"]="SELECT * FROM {0}.{1} ".format(db,table)
    # q["SELECT"]="SELECT date(),* FROM {0}.{1} ".format(db,table)






if __name__== '__main__':
    #create_test_environment()
    build_test()
   # destroy_test_environment()
