import os
import threading

import ddb



def ddb_passthrough(src,dst,table,delimiter):
        thread_name=threading.currentThread().getName()
        print("{0} started".format(thread_name))
        FIFO = src
        #os.mkfifo(FIFO)
        while True:
            e=ddb.engine(output,field_delimiter=delimiter)
            res=e.query("SELECT * FROM {0}".format(table))
            output=e.output.factory(res,output='raw',output_stream='STRING')
    
            
            with open(src) as fifo:
                fifo.write(output)
        
        print("{0} finished".format(thread_name))


class pipe_runner:
    
  
    def __init__(self,files):
        for item in files:
            thread = threading.Thread(target = ddb_passthrough, args = (item ))
            thread.start()
            thread.join()

if __name__=='__main__':
    files=[{'src':'~/chris17453/ddb/source/test/MOCK_DATA_FIFO.csv','dst':'~/chris17453/ddb/source/test/MOCK_DATA.csv','table':'test.mock','delimiter':','}]
    
    
    p=pipe_runner(files)
