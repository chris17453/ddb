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
        print "LP",lock_path
        if os.path.exists(lock_path):
            with open(lock_path,'r') as lockfile:
                try:
                    print ("2")
                    file_data=lockfile.readline()
                    print ("3")
                    file_lock_time=datetime.datetime.strptime(file_data,'%Y-%m-%d %H:%M:%S.%f')
                    print ("4")
                    curent_datetime =datetime.datetime.now()
                    print ("5")
                    elapsed_time=curent_datetime-file_lock_time
                    print ("6")
                    # its an old lock thats failed. time to long. remove it
                    if elapsed_time.seconds>10*1:
                        print ("7")
                        lock.release(path)
                        return None
                    print ("9")
                    return True
                except Exception as ex:
                    print(ex)
                    print ":33s"
                    lock.release(path)
                    pass
                print ":YI"
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
            lock_time=datetime.datetime.now()
            lock_time_str="{0}".format(lock_time)
            print("Lock Time: {0}".format(lock_time_str))
            lockfile.write(lock_time_str)
            lockfile.flush()
        if os.path.exists(lock_path)==False:
            raise Exception ("Lockfile failed to create {0}".format(lock_path))
        