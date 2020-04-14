# cython: profile=True
# NOcython: linetrace=True
import os
import sys
import datetime
import time
import tempfile, shutil
import hashlib
import random
import base64



class lock:
    #max_lock_time=60
    #max_lock_wait_time=max_lock_time+1
    sleep_time_min=0.0001
    sleep_time_max=0.001
    LOCK_NONE=0
    LOCK_OWNER=1
    LOCK_OTHER=2
    LOCK_PARTIAL=3
    debug=None
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

        #if lock.debug: lock.info("Lock","\n".join(f.readlines()))
        
        if(perserveFileDate):
            shutil.copystat(src, dst)
        
    @staticmethod
    def info(msg,data="Empty"):
        pid=os.getpid()
        dt = datetime.datetime.now()
        log_line="{3}-{2}-[ERROR]-{0}: {1}\n".format(msg,data,dt,pid)
        sys.stdout.write(log_line+"\n")
        pass

        #pid=os.getpid()
        #dt = datetime.datetime.now()
        #log_line="{3}-{2}-[INFO]-{0}: {1}\n".format(msg,data,dt,pid)
        #file=open("/tmp/ddb.log","a+")
        #file.write(log_line)
        #file.close()
            
    @staticmethod
    def error(msg,data):
        pid=os.getpid()
        dt = datetime.datetime.now()
        log_line="{3}-{2}-[ERROR]-{0}: {1}\n".format(msg,data,dt,pid)
        sys.stderr.write(log_line+"\n")
        pass
        
        #file=open("/tmp/ddb.log","a+")
        #file.write(log_line)
        #file.close()
    
    @staticmethod
    def normalize_path(path):
        """Update a relative or user absed path to an ABS path"""
        normalized_path=os.path.abspath(os.path.expanduser(path))
        return normalized_path

    @staticmethod
    def get_lock_filename(path):
        """Generate a unique name for a given file path so that if the same file name is used with a different path, the lock file is unique.
        Possible errors with linked files."""
        try:
            norm_path=lock.normalize_path(path)
            temp_dir = tempfile.gettempdir()
            basename="{0}_{1}".format( os.path.basename(norm_path),"TEMP" )
            temp_file_name='ddb_{0}.lock'.format(basename)
            norm_lock_path = os.path.join(temp_dir, temp_file_name)
            return norm_lock_path
        except:
            err = sys.exc_info()[1]
            ex = err.args[0]
            lock.info("Get Lock Filname: {0}".format(ex))
            exit(1)
            
    @staticmethod
    def check_pid(pid):        
        """ Check For the existence of a unix pid. """
        try:
            os.kill(pid, 0)
        except:
            return False
        
        return True

    @staticmethod
    def is_locked(path,key_uuid,lock_path=None):
        try:
            if None==lock_path:
                lock_path=lock.get_lock_filename(path)
            if os.path.exists(lock_path)==True:
                lockfile=open(lock_path,'r',) 
                try:
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
                        elif os.getpid()==owner_pid:
                            if lock.debug: lock.info("Lock","owned by this process, but another instance of ddb: {0}:{1}".format(owner_uuid,key_uuid))
                            return lock.LOCK_OTHER
                        if lock.debug: lock.info("Lock","owned by other process: {0}:{1}".format(owner_uuid,key_uuid))
                        # print(owner_uuid,key_uuid)
                        return lock.LOCK_OTHER
                    except:
                        err = sys.exc_info()[1]
                        ex = err.args[0]
                        if lock.debug: lock.error("Lock","error {0}".format(ex))
                        # because of mid write glitch
                        return lock.LOCK_OTHER
                        #lock.release(path)
                        pass
                finally:
                    lockfile.close()
            if lock.debug: lock.info("Lock","None-Fall Through")
            return lock.LOCK_NONE
        except:
            err = sys.exc_info()[1]
            ex = err.args[0]
            if lock.debug: lock.error("Lock","Failed to validate file lock: {0}".format(ex))
            return lock.LOCK_OTHER

    @staticmethod
    def release(path):
        lock_path=lock.get_lock_filename(path)
        if lock.debug: lock.info ("Lock", "Releasing Lock file: {0}".format(lock_path))
        
        if os.path.exists(lock_path)==False:
            raise Exception ("Lockfile cannot be removed, it doesnt exist. {0}".format(lock_path))
        
        try: 
            os.remove(lock_path)
            if lock.debug: lock.info('lock',"% s removed successfully" % path) 
        except:
            err = sys.exc_info()[1]
            ex = err.args[0]
            if lock.debug: lock.error('Lock',"File path can not be removed {0}".format(ex))
            exit(1)

            
        if lock.debug: lock.info("Lock","removed")

    @staticmethod
    def aquire(path,key_uuid):
        try:
            path="{0}".format(path)
            key_uuid="{0}".format(key_uuid)

            lock_path =lock.get_lock_filename(path)
            pid       =os.getpid()
            lock_contents="{0}|{1}|x".format(key_uuid,pid)
            
            if lock.debug: lock.info("LOCK","{0},{1},TRYING LOCK".format(pid,datetime.datetime.now()))

            if lock.debug: lock.info("Lock","Creating Lock for {0}".format(path))
            error=0
            while 1:
                lock_status=lock.is_locked(path,key_uuid,lock_path)
                #if lock_status==lock.LOCK_NONE:
                try:
                    fd=os.open(lock_path, os.O_WRONLY | os.O_CREAT | os.O_EXCL,int("666",base=8) )
                    os.write(fd,str.encode(lock_contents))
                    os.close(fd)
                    #os.chmod(lock_path, )

                    if lock.debug: lock.info("Lock","{0},{1},GOT LOCK".format(pid,datetime.datetime.now()))
                    
                    
                    break
                except:
                    err = sys.exc_info()[1]
                    ex = err.args[0]
                    error+=1
                    if error==1:
                        if lock.debug: lock.info("Lock","error!:{0}".format(ex))
                    pass
                #if lock.debug: lock.info("Lock","File locked, waiting till file timeout, or max lock retry time, {0}".format(path))
                time.sleep(random.uniform(lock.sleep_time_min,lock.sleep_time_max))
                    

                    


            if lock.debug: lock.info("Lock","Aquired {0}".format(lock_path))
            if os.path.exists(lock_path)==False:
                if lock.debug: lock.error("Lock","Failed to create")
                raise Exception ("Lockfile failed to create {0}".format(lock_path))
        except:
            err = sys.exc_info()[1]
            ex = err.args[0]
            lock.info("Aquire Lock: {0}".format(ex))


def get_uuid():
    seed = random.getrandbits(32)
    while True:
       yield str(seed)
       seed += 1
  
def temp_path_from_file(path,prefix='',unique=None):
    norm_path = normalize_path(path)
    base_dir  = os.path.dirname(norm_path)
    base_file = os.path.basename(norm_path)
    unique_id=''
    if unique:
        uuid_str=get_uuid()
        unique_id="_{0}:{1}".format(uuid_str,os.getpid())
    temp_file_name="~{1}{0}{2}.swp".format(base_file,prefix,unique_id)
    temp_path = os.path.join(base_dir, temp_file_name.encode("ascii") )
    return temp_path
        

def create_temporary_copy(path,uuid='',prefix='ddb_'):
    """ Create a copy of a regular file in a temporary directory """
    try:
        # dont over look this
        # it checks for a lock file in the temp dir
        # and blocks this thread/.process until MAX timout occures
        # or the lock ages and is deleted
        lock.aquire(path,uuid)
        #time.sleep(.001)
        if lock.debug: lock.info("LOCK Modified",os.stat(path).st_mtime)
        
        temp_path=temp_path_from_file(path,"{0}{1}".format(prefix,uuid) )
        
        norm_path=normalize_path(path)
        
        if lock.debug: lock.info("Lock","Creating temporary file: {0}-> {1}".format(norm_path, temp_path))
        #lock.copy_file( norm_path, temp_path)
        
        shutil.copy2(norm_path, temp_path)
        
         #print("Deleting: {0} Copying to Deleted: {1}".format(path,temp_path))
        if lock.debug: lock.info("Lock","Created temporary file: {0}".format( temp_path))
        return temp_path
    except:
        err = sys.exc_info()[1]
        ex = err.args[0]
        
        if lock.debug: lock.error("Lock Error Create Temp Copy","{0}".format(ex ))
        exit(1)
        raise Exception("Temp File Create Copy Error: {0}".format(ex))

def remove_temp_file(path):
    try:
        if lock.debug: lock.info("Lock","Removing temp copy: {0}".format(path))
        os.remove(path)
    except: 
        err = sys.exc_info()[1]
        ex = err.args[0]
        if lock.debug: lock.error("Lock Remove Temp File","{0}".format(ex))
        exit(1)
        raise Exception("Lock, Delete file  failed: {0}".format(ex))
        
#def compare_files(file1,file2):
#    
#    content1=open(file1,'r').read()
#    content2=open(file2,'r').read()
#    
#    hash1=hashlib.md5(content1).hexdigest()
#    hash2=hashlib.md5(content2).hexdigest()
#    if lock.debug: lock.info("Lock","FileHash for {0}: {1}".format(file1,hash1))
#    if lock.debug: lock.info("Lock","FileHash for {0}: {1}".format(file2,hash2))
#    if hash1!=hash2:
#        return None
#    return True
#
        
# todo move into context with a manager flag        
def swap_files(path, temp,key_uuid):
    """ Swap a temporary file with a regular file, by deleting the regular file, and copying the temp to its location """
    if lock.debug: lock.info("Lock","SWAP")

    norm_path=normalize_path(path)
    if lock.debug: lock.info("Lock","Removing master {0} ".format(norm_path))
    

    if lock.debug: lock.info("Lock","Renaming temp to master {0} <- {1}".format(norm_path,temp))
    os.rename(temp,norm_path)

    lock.release(path)


 
def normalize_path(path):
    """Update a relative or user absed path to an ABS path"""
    normalized_path=os.path.abspath(os.path.expanduser(path))
    return normalized_path.encode('ascii')

        