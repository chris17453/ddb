import os
import datetime
import tempfile
import time

class lock:
    max_lock_time=60
    sleep_time=0.02

    @staticmethod
    def info(msg,data):
        print("{0}: {1}".format(msg,data))
    
    @staticmethod
    def normalize_path(path):
        """Update a relative or user absed path to an ABS path"""
        normalized_path=os.path.abspath(os.path.expanduser(path))
        return normalized_path

    @staticmethod
    def get_lock_filename(path):
        norm_path=lock.normalize_path(path)
        temp_dir = tempfile.gettempdir()
        basename=os.path.basename(norm_path)
        temp_file_name='{0}.lock'.format(basename)
        norm_lock_path = os.path.join(temp_dir, temp_file_name)
        return norm_lock_path
            
    @staticmethod
    def is_locked(path):
        lock_path=lock.get_lock_filename(path)
        if os.path.exists(lock_path):
            with open(lock_path,'r') as lockfile:
                try:
                    file_data=lockfile.readline()
                    file_lock_time=datetime.datetime.strptime(file_data,'%Y-%m-%d %H:%M:%S.%f')
                    curent_datetime =datetime.datetime.now()
                    elapsed_time=curent_datetime-file_lock_time
                    # its an old lock thats failed. time to long. remove it
                    print curent_datetime,file_lock_time,elapsed_time, elapsed_time.seconds,lock.max_lock_time
                    if elapsed_time.seconds>lock.max_lock_time:
                        lock.info("Lock","Releasing")
                        lock.release(path)
                        return None
                    return True
                except Exception as ex:
                    #print(ex)
                    lock.release(path)
                    pass
        lock.info("Lock","No Lock")
        return None

    @staticmethod
    def release(path):
        lock_path=lock.get_lock_filename(path)
        if os.path.exists(lock_path)==False:
            raise Exception ("Lockfile cannot be removed, it doesnt exist. {0}".format(lock_path))
        
        
        
        ("Removing {0}".format(path))
        os.remove(lock_path)
        if os.path.exists(lock_path):
            raise Exception ("Lockfile cannot be removed. {0}".format(lock_path))
        lock.info("Lock","removed")

    @staticmethod
    def aquire(path):
        lock_time=0
        lock_cycle=0
        while lock.is_locked(path):
            lock.info("Lock","File locked, waiting till file timeout, or max lock retry time, {0},{1}".format(path,lock_time))

            time.sleep(lock.sleep_time)
            lock_time+=lock.sleep_time
            lock_cycle+=1
            if lock_time>lock.max_lock_time:
                lock.info("Lock","Cannot aquire lock, timeout")
                raise Exception( "Cannot aquire lock, max timeout of {0} seconds reached. Aproxomatly '{1}' cycles".format(lock.max_lock_time,lock_cycle))

        lock_path=lock.get_lock_filename(path)
        if os.path.exists(lock_path):
            lock.info("Lock","Already Exists")
            raise Exception ("Lockfile already exists. {0}".format(lock_path))
        with open(lock_path,'w') as lockfile:
            lock_time=datetime.datetime.now()
            lock_time_str="{0}".format(lock_time)
            
            lock.info("Lock Time",lock_time_str)
            
            lockfile.write(lock_time_str)
            lockfile.flush()
        if os.path.exists(lock_path)==False:
            lock.info("Lock","Failed to create")
            raise Exception ("Lockfile failed to create {0}".format(lock_path))

        