# cython: linetrace=True
import os
import sys
import datetime
import tempfile
import time
import tempfile, shutil
import hashlib
import random



class lock:
    #max_lock_time=60
    #max_lock_wait_time=max_lock_time+1
    sleep_time_min=0.0001
    sleep_time_max=0.001
    LOCK_NONE=0
    LOCK_OWNER=1
    LOCK_OTHER=2
    LOCK_PARTIAL=3
    debug=True
    BUFFER_SIZE=4096
    
    @staticmethod
    def copy_file(src, dst, buffer_size=10485760, perserveFileDate=None):
        '''
        Copies a file to a new location. Much faster performance than Apache Commons due to use of larger buffer
        @param src:    Source File
        @param dst:    Destination File (not file path)
        @param buffer_size:    Buffer size to use during copy
        @param perserveFileDate:    Preserve the original file date
        '''
        #    Check to make sure destination directory exists. If it doesn't create the directory
        dstParent, dstFileName = os.path.split(dst)
        if(not(os.path.exists(dstParent))):
            os.makedirs(dstParent)
    
        #    Optimize the buffer for small files
        buffer_size = min(buffer_size,os.path.getsize(src))
        if(buffer_size == 0):
            buffer_size = 1024
    
        if shutil._samefile(src, dst):
            raise shutil.Error("`%s` and `%s` are the same file" % (src, dst))
        for fn in [src, dst]:
            try:
                st = os.stat(fn)
            except OSError:
                # File most likely does not exist
                pass
            else:
                # XXX What about other special files? (sockets, devices...)
                if shutil.stat.S_ISFIFO(st.st_mode):
                    raise shutil.SpecialFileError("`%s` is a named pipe" % fn)
        #with open(src, 'rb',buffering=0) as fsrc:
         #   with open(dst, 'wb',buffering=0) as fdst:
        src_fh = os.open(src, os.O_RDONLY | os.O_SYNC)
        dst_fh = os.open(dst, os.O_CREAT | os.O_SYNC|  os.O_TRUNC | os.O_WRONLY )
        if src_fh!=None and dst_fh!=None:
            while True:
                buffer=os.read(src_fh, lock.BUFFER_SIZE)
                if buffer=='':
                    break
                os.write(dst_fh, buffer)


        if src_fh:
            os.close(src_fh)
        if dst_fh:
            os.close(dst_fh)

          #      shutil.copyfileobj(fsrc, fdst, buffer_size)

        f=open(src, 'rb',buffering=0)
        lock.info("Lock","\n".join(f.readlines()))
        f.close()
    
        if(perserveFileDate):
            shutil.copystat(src, dst)
        
    @staticmethod
    def info(msg,data):
        pid=os.getpid()
        dt = datetime.datetime.now()
        log_line="{3}-{2}-[INFO]-{0}: {1}\n".format(msg,data,dt,pid)
        file=open("/tmp/ddb.log","a+")
        file.write(log_line)
        file.close()
            
    @staticmethod
    def error(msg,data):
        pid=os.getpid()
        dt = datetime.datetime.now()
        log_line="{3}-{2}-[ERROR]-{0}: {1}\n".format(msg,data,dt,pid)
        file=open("/tmp/ddb.log","a+")
        file.write(log_line)
        file.close()
    
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
        if os.getpid()==pid:
            lock.info("Lock","This Thread {0}".format(pid))
            return True
        try:
            os.kill(pid, 0)
        except OSError:
            return False
        
        return True

    @staticmethod
    def is_locked(path,key_uuid,lock_path=None):
        try:
            if None==lock_path:
                lock_path=lock.get_lock_filename(path)
            if os.path.exists(lock_path)==True:
                with open(lock_path,'r',buffering=0) as lockfile:
                    try:
                        file_data=lockfile.readline()
                        #timestamp,temp_file_path,
                        try:
                            owner_uuid,owner_pid,terminator=file_data.split('|')
                        except:
                            if lock.debug: lock.info("Lock","lockfile incomplete, likely in progress")
                            return lock.LOCK_PARTIAL
                        

                        if owner_uuid==key_uuid:
                            if lock.debug: lock.info("Lock","owned by current process: {0}".format(owner_uuid))
                            return lock.LOCK_OWNER
                        elif lock.check_pid(int(owner_pid))==False:
                            if lock.debug: lock.info("Lock","invalid owner : {0}".format(owner_pid))
                            lock.release(path)
                            return lock.LOCK_NONE
                    
                        if lock.debug: lock.info("Lock","owned by other process: {0}".format(owner_uuid))
                        # print(owner_uuid,key_uuid)
                        return lock.LOCK_OTHER
                    except Exception as ex:
                        if lock.debug: lock.error("Lock","error {0}".format(ex))
                        # because of mid write glitch
                        return lock.LOCK_OTHER
                        #lock.release(path)
                        pass
            if lock.debug: lock.info("Lock","None-Fall Through")
            return lock.LOCK_NONE
        except Exception as ex:
            return lock.LOCK_OTHER
            if lock.debug: lock.error("Lock","Failed to validate file lock: {0}".format(ex))

    @staticmethod
    def release(path):
        lock_path=lock.get_lock_filename(path)
        if lock.debug: lock.info ("Lock", "Releasing Lock file: {0}".format(lock_path))
        
        if os.path.exists(lock_path)==False:
            raise Exception ("Lockfile cannot be removed, it doesnt exist. {0}".format(lock_path))
        
        
        
        try: 
            os.remove(lock_path)
            if lock.debug: lock.info('lock',"% s removed successfully" % path) 
        except : 
            ex = sys.exc_info()
            if lock.debug: lock.error('Lock',"File path can not be removed {0}:{1}:{2}".format(ex[0] , ex[1] , ex[2]))
            if lock.debug: lock.error('Lock release',ex)
            exit(1)

            
        if lock.debug: lock.info("Lock","removed")

    @staticmethod
    def aquire(path,key_uuid):
        
        lock_path =lock.get_lock_filename(path)
        pid       =os.getpid()
        lock_contents="{0}|{1}|x".format(key_uuid,pid)
        lock.info("LOCK","{0},{1},TRYING LOCK".format(pid,datetime.datetime.now()))

        #if lock.debug: lock.info("Lock","Creating Lock for {0}".format(path))
        while 1:
            lock_status=lock.is_locked(path,key_uuid,lock_path)
            if lock_status==lock.LOCK_NONE:
                try:
                    fd=os.open(lock_path, os.O_WRONLY | os.O_CREAT | os.O_EXCL,0o666 )
                    os.write(fd,lock_contents)
                    os.close(fd)
                    lock.info("Lock","{0},{1},GOT LOCK".format(pid,datetime.datetime.now()))
                    
                    
                    break
                except OSError as ex:
                    if lock.debug: lock.info("Lock","error!:{0}".format(ex))
                    pass
            #if lock.debug: lock.info("Lock","File locked, waiting till file timeout, or max lock retry time, {0}".format(path))
            time.sleep(random.uniform(lock.sleep_time_min,lock.sleep_time_max))
                



        if lock.debug: lock.info("Lock","Aquired {0}".format(lock_path))
        if os.path.exists(lock_path)==False:
            if lock.debug: lock.error("Lock","Failed to create")
            raise Exception ("Lockfile failed to create {0}".format(lock_path))

  
def create_temporary_copy(path,uuid,prefix='ddb_'):
    """ Create a copy of a regular file in a temporary directory """
    try:
        # dont over look this
        # it checks for a lock file in the temp dir
        # and blocks this thread/.process until MAX timout occures
        # or the lock ages and is deleted
        lock.aquire(path,uuid)
        time.sleep(.001)
        lock.info("LOCK Modified",os.stat(path).st_mtime)
        norm_path = normalize_path(path)
        
        base_dir  = os.path.dirname(norm_path)
        base_file = os.path.basename(norm_path)

        temp_dir = tempfile.gettempdir()
        #temp_base_name=next(tempfile._get_candidate_names())+"UUID-"+uuid
        #if prefix:
        #    temp_file_name="{0}_{1}".format(prefix,temp_base_name)
        #else:
        #    temp_file_name="{0}".format(temp_base_name)
        temp_file_name="~{0}.swp".format(base_file)
        temp_path = os.path.join(base_dir, temp_file_name)
        if lock.debug: lock.info("Lock","Creating temporary file: {0}-> {1}".format(normalize_path(path), temp_path))
        lock.copy_file(normalize_path(path), temp_path)
         #print("Deleting: {0} Copying to Deleted: {1}".format(path,temp_path))
        return temp_path
    except:
        ex = sys.exc_info()
        if lock.debug: lock.error("Lock Error","{0}:{1}:{2}".format(ex[0] , ex[1] , ex[2]))
        exit(1)
        raise Exception("Temp File Create Copy Error: {0}".format(ex))

def remove_temp_file(path):
    try:
        if lock.debug: lock.info("Lock","Removing temp copy: {0}".format(path))
        os.remove(path)
    except: 
        ex = sys.exc_info()
        if lock.debug: lock.error("Lock Error","{0}:{1}:{2}".format(ex[0], ex[1] , ex[2]))
        exit(1)
        raise Exception("Lock, Delete file  failed: {0}".format(ex))
        
def compare_files(file1,file2):
    hash1=hashlib.md5(open(file1,'rb').read()).hexdigest()
    hash2=hashlib.md5(open(file2,'rb').read()).hexdigest()
    lock.info("Lock","FileHash for {0}: {1}".format(file1,hash1))
    lock.info("Lock","FileHash for {0}: {1}".format(file2,hash2))
    if hash1!=hash2:
        return None
    return True

        
# todo move into context with a manager flag        
def swap_files(path, temp,key_uuid):
    """ Swap a temporary file with a regular file, by deleting the regular file, and copying the temp to its location """
    #lock_status=lock.is_locked(path,key_uuid)
    #if lock.debug: lock.info("Lock","Status: {0}".format(lock_status))
    
    #if lock.LOCK_OWNER != lock_status:
    #    if lock.debug: lock.error("Lock","Lock has wrong owner")
    #    exit(1)
    #    raise Exception("Cannot swap files, expected lock. Didnt find one {0}".format(path))

    # DELETE ORIGINAL
    norm_path=normalize_path(path)
    #if os.path.exists(norm_path)==True:
    #    remove_temp_file(norm_path)

    #if os.path.exists(norm_path)==True:
    #    lock.error("Lock","MASTER FILE WONT DELETE")
    #    exit(1)
    if lock.debug: lock.info("Lock","Copying temp to master {0} <- {1}".format(norm_path,temp))
    
    while compare_files(temp,norm_path)==None:
        os.unlink(norm_path)
        os.rename(temp,norm_path)
        
#        lock.error("Lock HASH","Files do not match: {0},{1}".format(temp,norm_path))
        time.sleep(.001)
#
    #    exit (1)

    #remove_temp_file(temp)
    lock.release(path)



    #if os.path.exists(temp)==True:
     #   if lock.debug: lock.error("Lock Error","Temp file not deleted")
     #   exit(1)

     #   raise Exception("Deleting temp file {0} failed".format(temp))


 
def normalize_path(path):
    """Update a relative or user absed path to an ABS path"""
    normalized_path=os.path.abspath(os.path.expanduser(path))
    return normalized_path

        