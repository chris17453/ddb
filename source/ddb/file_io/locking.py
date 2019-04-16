import os
import datetime
import tempfile
import time

class lock:
    
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
                    file_lock_time=datetime.datetime.strptime(lockfile.readline(),'%Y-%m-%d %H:%M:%S.%f')
                    curent_datetime =datetime.datetime.now()
                    elapsed_time=curent_datetime-file_lock_time
                    # its an old lock thats failed. time to long. remove it
                    if elapsed_time.seconds()>10*1:
                        lock.release(path)
                        return None
                    return True
                except Exception as ex:
                    print(ex)
        return None

    @staticmethod
    def release(path):
        lock_path=lock.get_lock_filename(path)
        if os.path.exists(lock_path)==False:
            raise Exception ("Lockfile cannot be removed, it doesnt exist. {0}".format(lock_path))
        os.remove(lock_path)
        if os.path.exists(lock_path):
            raise Exception ("Lockfile cannot be removed. {0}".format(lock_path))

    @staticmethod
    def aquire(path):
        max_lock_time=60
        lock_time=0
        sleep_time=0.02
        lock_cycle=0
        while lock.is_locked(path):
            time.sleep(sleep_time)
            lock_time+=sleep_time
            lock_cycle+=1
            if lock_time>max_lock_time:
                raise Exception( "Canot aquire lock, max timeout of {0} seconds reached. Aproxomatly '{1}' cycles".format( max_lock_time,lock_cycle))

        lock_path=lock.get_lock_filename(path)
        if os.path.exists(lock_path):
            raise Exception ("Lockfile already exists. {0}".format(lock_path))
        with open(lock_path,'w') as lockfile:
            lockfile.write(datetime.datetime.now())
        if os.path.exists(lock_path)==False:
            raise Exception ("Lockfile failed to create {0}".format(lock_path))
        