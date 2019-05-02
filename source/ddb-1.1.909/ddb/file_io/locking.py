import os
import datetime
import tempfile
import time
import tempfile, shutil


class lock:
    max_lock_time=60
    sleep_time=0.02
    LOCK_NONE=0
    LOCK_OWNER=1
    LOCK_OTHER=2
    @staticmethod
    def info(msg,data):
        if 1==1:
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
    def is_locked(path,key_uuid):
        lock_path=lock.get_lock_filename(path)
        if os.path.exists(lock_path):
            with open(lock_path,'r') as lockfile:
                try:
                    file_data=lockfile.readline()
                    timestamp,temp_file_path,owner_uuid=file_data.split('|')
                    # print(timestamp,temp_file_path,owner_uuid)
                    file_lock_time=datetime.datetime.strptime(timestamp,'%Y-%m-%d %H:%M:%S.%f')
                    curent_datetime =datetime.datetime.now()
                    elapsed_time=curent_datetime-file_lock_time
                    # it's an old lock thats failed. time to long. remove it
                    # print curent_datetime,file_lock_time,elapsed_time, elapsed_time.seconds,lock.max_lock_time
                    
                    if elapsed_time.seconds>lock.max_lock_time:
                        lock.info("Lock","Releasing, lock aged out")
                        lock.release(path)
                        return lock.LOCK_NONE
                    if owner_uuid==key_uuid:
                        lock.info("Lock","owned by current process")
                        return lock.LOCK_OWNER
                    else:
                        lock.info("Lock","owned by other process")
                        # print(owner_uuid,key_uuid)
                        return lock.LOCK_OTHER
                except Exception as ex:
                    lock.info("Lock","error".format(ex))
                    lock.release(path)
                    pass
        lock.info("Lock","No Lock")
        return lock.LOCK_NONE

    @staticmethod
    def release(path):
        lock_path=lock.get_lock_filename(path)
        if os.path.exists(lock_path)==False:
            raise Exception ("Lockfile cannot be removed, it doesnt exist. {0}".format(lock_path))
        
        #print ("Removing {0}".format(lock_path))
        os.remove(lock_path)
        if os.path.exists(lock_path):
            raise Exception ("Lockfile cannot be removed. {0}".format(lock_path))
        lock.info("Lock","removed")

    @staticmethod
    def aquire(path,key_uuid):
        lock_time=0
        lock_cycle=0
        while 1:
            lock_status=lock.is_locked(path,key_uuid)
            if lock_status<lock.LOCK_OTHER:
                break
            lock.info("Lock","File locked, waiting till file timeout, or max lock retry time, {0},{1},{2}".format(path,lock_time,lock_status))

            time.sleep(lock.sleep_time)
            lock_time+=lock.sleep_time
            lock_cycle+=1
            if lock_time>lock.max_lock_time:
                lock.info("Lock","Cannot aquire lock, timeout")
                raise Exception( "Cannot aquire lock, max timeout of {0} seconds reached. Aproxomatly '{1}' cycles".format(lock.max_lock_time,lock_cycle))

        lock_path=lock.get_lock_filename(path)
        #if os.path.exists(lock_path):
        #    lock.info("Lock","Already Exists")
        #    raise Exception ("Lockfile already exists. {0}".format(lock_path))

        with open(lock_path,'w') as lockfile:
            lock_time=datetime.datetime.now()
            lock_time_str="{0}".format(lock_time)
            
            lock.info("Lock Time",lock_time_str)
            # print("writing",key_uuid)
            lockfile.write("{0}|{1}|{2}".format(lock_time_str,path,key_uuid))
            lockfile.flush()
        if os.path.exists(lock_path)==False:
            lock.info("Lock","Failed to create")
            raise Exception ("Lockfile failed to create {0}".format(lock_path))

  
def create_temporary_copy(path,uuid,prefix='ddb_'):
    """ Create a copy of a regular file in a temporary directory """
    try:
        # dont over look this
        # it checks for a lock file in the temp dir
        # and blocks this thread/.process until MAX timout occures
        # or the lock ages and is deleted
        lock.aquire(path,uuid)
        temp_dir = tempfile.gettempdir()
        temp_base_name=next(tempfile._get_candidate_names())
        if prefix:
            temp_file_name="{0}_{1}".format(prefix,temp_base_name)
        else:
            temp_file_name="{0}".format(temp_base_name)
        
        temp_path = os.path.join(temp_dir, temp_file_name)
        shutil.copy2(normalize_path(path), temp_path)
         #print("Deleting: {0} Copying to Deleted: {1}".format(path,temp_path))
        return temp_path
    except Exception as ex:
        raise Exception("Temp File Error: {0}".format(ex))

def remove_temp_file(path):
    try:
        #print "Removing temp copy"
        os.remove(path)
        if os.path.exists(path):
            raise Exception("Failed to delete: {0}".format(path))    
    except Exception as ex:
        raise Exception("Temp File Error: {0}".format(ex))

        
# todo move into context with a manager flag        
def swap_files(path, temp,key_uuid):
    """ Swap a temporary file with a regular file, by deleting the regular file, and copying the temp to its location """
    try:
        #print("Swap File1")
        if lock.LOCK_OWNER != lock.is_locked(path,key_uuid):
            raise Exception("Cannot swap files, expected lock. Didnt find one {0}".format(path))

        # DELETE ORIGINAL
        norm_path=normalize_path(path)
        if os.path.exists(norm_path):
            os.remove(norm_path)
        
        if os.path.exists(norm_path):
            raise Exception("Deleting file {0} failed".format(norm_path))
        
        # REMOVE LOCK FROM ORIGINAL PATH
        #print("Swap File2")
        lock.release(path)

        #if os.path.exists(temp):
        #    print ("Exists")
        shutil.copy2(temp, norm_path)
        #print  temp,path
        
        os.remove(temp)
        #print("$Removed")
        if os.path.exists(temp):
            raise Exception("Deleting temp file {0} failed".format(temp))
        
    except Exception as ex:
        raise Exception("File Error: {0}".format(ex))
 
def normalize_path(path):
    """Update a relative or user absed path to an ABS path"""
    normalized_path=os.path.abspath(os.path.expanduser(path))
    return normalized_path

        