import os
import threading
import logging
import ddb
from ddb.output.factory import output_factory

logging.basicConfig(level=logging.DEBUG,format='(%(threadName)-10s) %(message)s')

class ddb_passthrough(threading.Thread):
    
    def __init__(self, group=None, target=None, name=None,args=(), kwargs=None, verbose=None):
        threading.Thread.__init__(self, group=group, target=target, name=name,verbose=verbose)
        self.setDaemon(True)
        self.args = args
        self.kwargs = kwargs
        return

    def run(self):
        print(self.args)
        thread_name=self.getName()
        logging.debug("{0} started".format(thread_name))
        FIFO = self.kwargs['src']
        #os.mkfifo(FIFO)
        while True:
            e=ddb.engine(output='raw',field_delimiter=self.kwargs['delimiter'])
            res=e.query("SELECT * FROM {0}".format(self.kwargs['table']))
            results=output_factory(res,output='raw',output_stream='STRING')
            with open(FIFO) as fifo:
                fifo.write(results)
        
        logging.debug("{0} finished".format(thread_name))



# Launches the threads per table
class pipe_runner:
    def __init__(self,files):
        for item in files:
            print item
            thread = ddb_passthrough(kwargs = {'src':item['src'],'table':item['table'],'delimiter':item['delimiter']} )
            thread.start()
            thread.join()

if __name__=='__main__':
    files=[{'src':'~/chris17453/ddb/source/test/MOCK_DATA_FIFO.csv','dst':'~/chris17453/ddb/source/test/MOCK_DATA.csv','table':'test.mock','delimiter':','}]
    p=pipe_runner(files)
