import os
import sys
import threading
import logging
import argparse
import signal
import ddb
from ddb.output.factory import output_factory

logging.basicConfig(level=logging.DEBUG,format='(%(threadName)-10s) %(message)s')

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
            os.mkfifo(FIFO)
        
        
        while True:
            logging.debug("{0} Looping".format(thread_name))
            e=ddb.engine(output='raw',field_delimiter=self.kwargs['delimiter'])
            res=e.query("SELECT * FROM {0}".format(self.kwargs['table']))
            results=output_factory(res,output='raw',output_stream='STRING')
            
            logging.debug("{0} grabbing data".format(thread_name))

            with open(FIFO,"wr") as fifo:
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
        
        logging.debug("{0} finished".format(thread_name))



# Launches the threads per table
class pipe_runner:
    def __init__(self):
        self.pidfile = "/tmp/ddb_fiforunner.pid"

    def start(self):
        pid = str(os.getpid())
        if os.path.isfile(self.pidfile):
            print("{0} already exists, exiting" .format( self.pidfile))
            sys.exit()
        file(self.pidfile, 'w').write(pid)
        
        try:
                        
            e=ddb.engine()
            for table in e.database.tables:
                print table.data.name
                if table.data.fifo:
                    thread = ddb_passthrough(kwargs = {'src':table.data.fifo,'table':"'{0}'.'{1}'".format(table.data.database,table.data.name),'delimiter':table.delimiters.field} )
                    thread.start()
                    thread.join()
        finally:
            os.unlink(self.pidfile)
    
    def stop(self):
        if os.path.isfile(self.pidfile):
            with  open(self.pidfile) as pid_file:
                pid=pid_file.read()
            try:
                os.kill(int(pid), signal.SIGTERM)
            except OSError as ex:
                error ="Failed to terminate {0:d}: {1}".format(pid,ex)
                raise error                
            os.unlink(self.pidfile)
        else:
            raise Exception("service not running")
            os.unlink(self.pidfile)
            return

        

if __name__=='__main__':
    parser = argparse.ArgumentParser("ddb_fifo", usage='%(prog)s [options]', description="""fifo service for ddb""", epilog="")
    parser.add_argument('action', help='start, stop', nargs= "?")
    args = parser.parse_args()
   
    p=pipe_runner()

    if args.action=='start':
        p.start()
    elif args.action=='stop':
        p.stop()
    elif args.action=='restart':
        p.stop()
        p.start()
    else:
        print ("Usage: ddb_fifo [start|stop|restart]")

