# cython: linetrace=True

import os
import sys
import threading
import logging
import argparse
import signal
import ddb
from ddb.output.factory import output_factory

logging.basicConfig(filename='/tmp/ddb_pipes.log', filemode='a',level=logging.INFO,format='(%(threadName)-10s) %(message)s')

# this file uses a named pipe
# it latches on to the pipe and when read from ddb emits the database as a processes raw file
# errors, whitespace etc removed
# it's an example of giving read only access to a file thats managed by ddb
# with event hooks on file reads
# now you can tell when anything reads from the file.
# still working out the writes tho....


class ddb_passthrough(threading.Thread):
    
    def __init__(self, group=None, target=None, name=None,args=(), kwargs=None, verbose=None):
        threading.Thread.__init__(self, group=group, target=target, name=name,verbose=verbose)
        self.daemon=True
        self.args = args
        self.kwargs = kwargs

    def run(self):

        thread_name=self.getName()
        logging.debug("{0} started".format(thread_name))
        FIFO = os.path.expanduser(self.kwargs['src'])
        if False==os.path.exists(FIFO):
            logging.info("Creating FIFO: {0}".format(FIFO))
            os.mkfifo(FIFO)
        else:
            logging.info("FIFO Exists: {0}".format(FIFO))

        
        
        while True:
            logging.debug("{0} Looping".format(thread_name))
            e=ddb.engine(output='raw',field_delimiter=self.kwargs['delimiter'])
            res=e.query("SELECT * FROM {0}".format(self.kwargs['table']))
            results=output_factory(res,output='raw',output_stream='STRING')
            
            logging.info("{0} grabbing data".format(thread_name))

            fifo=open(FIFO,"wr")
            try:
                # clear the buffer
                try:
                    res=fifo.readlines()
                except:
                    logging.debug("{0} nothing to read ".format(thread_name))            
                    pass
                try:
    
                    logging.debug("{0} writing".format(thread_name))
                    data="\n".join(results.output)
                    fifo.write(data)
                except:
                    logging.debug("{0} cant write".format(thread_name))            
                    pass
            finally:
                fifo.close()
        
        logging.debug("{0} finished".format(thread_name))



# Launches the threads per table
class ddb_pipe_runner:
    def __init__(self):
        self.pidfile = "/tmp/ddb_pipes.pid"
        self.name="ddb pipes"

    def start(self):
        print ("Starting")
        if os.path.isfile(self.pidfile):
            logging.info("{0} already exists, exiting" .format( self.pidfile))
            raise Exception("{0} service already running".format(self.name))

        pid = os.fork()
        
        logging.info("starting service: pid: {0}" .format( self.pidfile))
        
        try:
            if pid > 0:
                print("{0} Service Started".format(self.name))
                sys.exit(0)
        except OSError, e:
            logging.error("Failed to Demonize: %d, %s\n" % (e.errno,e.strerror))
            sys.exit(1)
        # TODO figure this part out? seems important brah
        # os.umask(UMASK)
        # os.setsid()
        pid=str(os.getpid())
        file(self.pidfile, 'w').write(pid)

        try:
                        
            e=ddb.engine()
            for table in e.database.tables:
                if table.data.fifo:
                    print table
                    thread = ddb_passthrough(kwargs = {'src':table.data.fifo,'table':"'{0}'.'{1}'".format(table.data.database,table.data.name),'delimiter':table.delimiters.field} )
                    thread.start()
                    thread.join()
        finally:
            os.unlink(self.pidfile)
    
    def stop(self):
        if os.path.isfile(self.pidfile):
            pid_file=open(self.pidfile)
            try:
                pid=pid_file.read()
            finally:
                pid_file.close()

            try:
                logging.info("stopping service: pid {0}".format(pid))
                os.kill(int(pid), signal.SIGTERM)
            except OSError as ex:
                error ="failed to stop service {0:d}: {1}".format(pid,ex)
                logging.info(error)
                os.unlink(self.pidfile)
                raise Exception(error)
            os.unlink(self.pidfile)
            print("{1} Service Stopped: pid {0}".format(pid,self.name))
                
        else:
            error="service cannot stop, not running"
            logging.info(error)
            os.unlink(self.pidfile)
            raise Exception(error)
            

        
def cli_main():
    parser = argparse.ArgumentParser("ddb-pipes", usage='%(prog)s [options]', description="""named pipes service for ddb""", epilog="")
    parser.add_argument('action', help='start, stop', nargs= "?")
    args = parser.parse_args()
   
    p=ddb_pipe_runner()

    try:
        if args.action=='start':
            p.start()
        elif args.action=='stop':
            p.stop()
        elif args.action=='restart':
            p.stop()
            p.start()
        else:
            print ("Usage: ddb_fifo [start|stop|restart]")
    except Exception, ex:
        print(ex)
        pass


    

if __name__=='__main__':
    cli_main()