import os
import sys
import time
import argparse
import signal
import threading
import logging
from subprocess import Popen,PIPE
from flask import Flask, request,send_from_directory, render_template, Blueprint
import jsonpickle
import ddb
app = Flask(__name__)



logging.basicConfig(filename='/tmp/ddb-server.log', filemode='a',level=logging.INFO,format='(%(threadName)-10s) %(message)s')


@app.route('/')
def home():
    return 'Welcome to ddb'


@app.route('/ddb/api/fetch', methods=['POST'])
def fetch():
    e=ddb.engine(config_dir=ddb_config_dir,mode='array',debug=None)
    try:
        
        res=e.query(req_data['sp'])
        serialized = jsonpickle.encode( res,
                                        unpicklable=False,
                                        make_refs=False)
        return serialized
    except Exception as ex:
        return "{0} -> '{1}'".format(ex,req_data['query'])

@app.route('/ddb/api/query', methods=['POST'])
def fetch():
    e=ddb.engine(config_dir=ddb_config_dir,mode='array',debug=None)
    try:
        res=e.query(req_data['query'])
        serialized = jsonpickle.encode( res,
                                        unpicklable=False,
                                        make_refs=False)
        return serialized
    except Exception as ex:
        return "{0} -> '{1}'".format(ex,req_data['query'])


def cli_main():
    print('Starting up ...')
    ddb_ip        = '0.0.0.0'
    ddb_port      = 17453
    ddb_config_dir= None
    
    if 'DDB_PORT' in os.environ:
        try:
            ddb_port=int(os.environ['DDB_PORT'])
            if ddb_port<1024:
                print ("DDB_PORT is using a restricted port number <1024")
                exit(1)
        except:
            print ("DDB_PORT is not an integer")
            exit(1)
    if 'DDB_IP' in os.environ:
        ddb_ip=os.environ['DDB_DATA']

    if 'DDB_DATA' in os.environ:
        # expand user vars, then get the absolute
        ddb_config_dir= os.path.abspath(os.path.expanduser(os.environ['DDB_DATA']))
    else:
        home = os.path.expanduser("~")
        ddb_config_dir= os.path.join(os.path.join(home, '.ddb'))

    app.run(host=ddb_ip,port=ddb_port)


if __name__ == '__main__':
    cli_main()
    