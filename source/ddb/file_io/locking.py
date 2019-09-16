# cython: linetrace=True
import os
import datetime
import tempfile
import time
import tempfile, shutil
import hashlib


class lock:
    #max_lock_time=60
    #max_lock_wait_time=max_lock_time+1
    sleep_time=0.002
    LOCK_NONE=0
    LOCK_OWNER=1
    LOCK_OTHER=2
    debug=None

    @staticmethod
    def info(msg,data):
        dt = datetime.datetime.now()
        
        if 1==1:
            print("{2}-{0}: {1}".format(msg,data,dt))
    
    @staticmethod
    def normalize_path(path):
        """Update a relative or user absed path to an ABS path"""
        normalized_path=os.path.abspath(os.path.expanduser(path))
        return normalized_path

    @staticmethod
    def get_lock_filename(path):
        """Generate a unique name for a given file path so that if the same file name is used with a different path, the lock file is unique.
        Possible errors with linked files."""
        
        norm_path=lock.normalize_path(path)
        temp_dir = tempfile.gettempdir()
        m = hashlib.md5()
        m.update(norm_path)
        basename=os.path.basename(norm_path)+"_"+m.hexdigest()
        #basename=os.path.basename(norm_path)
        temp_file_name='{0}.lock'.format(basename)
        norm_lock_path = os.path.join(temp_dir, temp_file_name)
        return norm_lock_path
            
    @staticmethod
    def check_pid(pid):        
        """ Check For the existence of a unix pid. """
        try:
            os.kill(pid, 0)
        except OSError:
            return False
        else:
            return True

    @staticmethod
    def is_locked(path,key_uuid,lock_path=None):
        try:
            if None==lock_path:
                lock_path=lock.get_lock_filename(path)
            if os.path.exists(lock_path)==True:
                with open(lock_path,'r+') as lockfile:
                    try:
                        file_data=lockfile.readline()
                        #timestamp,temp_file_path,
                        owner_uuid,owner_pid=file_data.split('|')
                        # print(timestamp,temp_file_path,owner_uuid)
                        #file_lock_time=datetime.datetime.strptime(timestamp,'%Y-%m-%d %H:%M:%S.%f')
                        #curent_datetime =datetime.datetime.now()
                        #elapsed_time=curent_datetime-file_lock_time
                        # it's an old lock thats failed. time to long. remove it
                        # print curent_datetime,file_lock_time,elapsed_time, elapsed_time.seconds,lock.max_lock_time

                        #NO lock timeout...
                        #if elapsed_time.seconds>lock.max_lock_time:
                        #    lock.info("Lock","Releasing, lock aged out")
                        #    lock.release(path)
                        #    return lock.LOCK_NONE

                        # If the lockfile owner PID does not exist
                        if lock.check_pid(int(owner_pid))==False:
                            lock.info("Lock","invalid owner")
                            lock.release(path)
                            return lock.LOCK_NONE
                        elif owner_uuid==key_uuid:
                            lock.info("Lock","owned by current process")
                            return lock.LOCK_OWNER
                        elif owner_uuid!=key_uuid:
                            lock.info("Lock","owned by other process")
                            # print(owner_uuid,key_uuid)
                            return lock.LOCK_OTHER
                        else:
                            lock.info("Lock","None-err?")
                            return lock.LOCK_NONE
                    except Exception as ex:
                        lock.info("Lock","error {0}".format(ex))
                        # because of mid write glitch
                        return lock.LOCK_OTHER
                        #lock.release(path)
                        pass
            lock.info("Lock","None-Fall Through")
            return lock.LOCK_NONE
        except Exception as ex:
            return lock.LOCK_OTHER
            lock.info("Lock","Failed to validate file lock: {0}".format(ex))

    @staticmethod
    def release(path):
        lock_path=lock.get_lock_filename(path)
        lock.info ("Lock", "Releasing Lock file: {0}".format(lock_path))
        
        if os.path.exists(lock_path)==False:
            raise Exception ("Lockfile cannot be removed, it doesnt exist. {0}".format(lock_path))
        
        
        
        try: 
            os.remove(lock_path)
            print("% s removed successfully" % path) 
        except OSError as error: 
            print(error) 
            print("File path can not be removed") 
            exit(0)

        if os.path.exists(lock_path)==True:
            print "Lockfile cannot be removed. {0}".format(lock_path)
            exit(0)
            
            raise Exception ("Lockfile cannot be removed. {0}".format(lock_path))
            
        lock.info("Lock","removed")

    @staticmethod
    def aquire(path,key_uuid):
        lock_path =lock.get_lock_filename(path)
        pid       =os.getpid()
        lock_contents="{0}|{1}".format(key_uuid,pid)
        while 1:
            lock_status=lock.is_locked(path,key_uuid,lock_path)
            if lock_status==lock.LOCK_NONE:
                lock.info("Lock","Creating Lock for {0}".format(path))
                try:
                    fd=os.open(lock_path, os.O_WRONLY | os.O_CREAT | os.O_EXCL)
                    os.write(fd,lock_contents)
                    os.close(fd)
                    break
                except Exception as ex:
                    lock.info("Lock","error!:{0}".format(ex))
            lock.info("Lock","File locked, waiting till file timeout, or max lock retry time, {0}".format(path))
            time.sleep(lock.sleep_time)


        #with open(lock_path,'w') as lockfile:
        #    lockfile.write)

        lock.info("Lock","MOD, {0}".format(path))
        # allow anyone to modify the lock file
        os.chmod(lock_path, 0o666)

        lock.info("Lock","Aquired {0}".format(lock_path))
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
        temp_base_name=next(tempfile._get_candidate_names())+"UUID-"+uuid
        if prefix:
            temp_file_name="{0}_{1}".format(prefix,temp_base_name)
        else:
            temp_file_name="{0}".format(temp_base_name)
        temp_path = os.path.join(temp_dir, temp_file_name)
        lock.info("Lock","Creating temporary file: {0}-> {1}".format(normalize_path(path), temp_path))
        shutil.copy2(normalize_path(path), temp_path)
         #print("Deleting: {0} Copying to Deleted: {1}".format(path,temp_path))
        return temp_path
    except Exception as ex:
        raise Exception("Temp File Create Copy Error: {0}".format(ex))

def remove_temp_file(path):
    try:
        lock.info("Lock","Removing temp copy: {0}".format(path))
        os.remove(path)
        if os.path.exists(path)==True:
            raise Exception("failed to delete: {0}".format(path))    
    except OSError as ex: 
        print ex
        raise Exception("Lock, Delete file  failed: {0}".format(ex))
        

        
# todo move into context with a manager flag        
def swap_files(path, temp,key_uuid):
    """ Swap a temporary file with a regular file, by deleting the regular file, and copying the temp to its location """
    lock_status=lock.is_locked(path,key_uuid)
    lock.info("Lock","Status: {0}".format(lock_status))
    if lock.LOCK_OWNER != lock_status:
        raise Exception("Cannot swap files, expected lock. Didnt find one {0}".format(path))

    # DELETE ORIGINAL
    norm_path=normalize_path(path)
    if os.path.exists(norm_path)==True:
        lock.remove_temp_file(norm_path)
    
    # REMOVE LOCK FROM ORIGINAL PATH
    #print("Swap File2")
    lock.release(path)

    #if os.path.exists(temp):
    #    print ("Exists")
    lock.info("Lock","Copying temp to master")
    shutil.copy2(temp, norm_path)
    #print  temp,path

    lock.remove_temp_file(temp)
    #print("$Removed")
    if os.path.exists(temp)==True:
        raise Exception("Deleting temp file {0} failed".format(temp))

 
def normalize_path(path):
    """Update a relative or user absed path to an ABS path"""
    normalized_path=os.path.abspath(os.path.expanduser(path))
    return normalized_path

        