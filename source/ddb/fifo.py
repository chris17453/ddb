import os
from  threading import Thread
import ddb



class ddb_passthrough(threading.Thread,file):
    def run(self):
        thread_name=self.getName()
        print("{0} started".format(thread_name))
        FIFO = file['src']
        #os.mkfifo(FIFO)
        while True:
            e=ddb.engine(output,field_delimiter=file['delimiter'])
            res=e.query("SELECT * FROM {0}".format(file['table']))
            output=e.output.factory(res,output='raw',stream='STRING')
    
            
            with open(file['src']) as fifo:
                fifo.write(output)
        
        print("{0} finished".format(thread_name))


class pipe_runner:
    
  
    def __init__(self,files):
        for file in files:
            thread = Thread(target = ddb_passthrough, args = (file ))
            thread.start()
            thread.join()

if __name__=='__main__':
    files=[{'src':'~/chris17453/ddb/source/test/MOCK_DATA_FIFO.csv','dst':'~/chris17453/ddb/source/test/MOCK_DATA.csv','table':'test.mock','delimiter':','}]
    
    
    p=pipe_runner(files)
