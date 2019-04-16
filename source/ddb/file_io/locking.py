import os
import datetime
import tempfile


class lockfile:
    
    @staticmethod
    def normalize_path(path):
        """Update a relative or user absed path to an ABS path"""
        normalized_path=os.path.abspath(os.path.expanduser(path))
        return normalized_path

    @staticmethod
    def get_lock_filename(path):
        norm_path=lockfile.normalize_path(path)
        temp_dir = tempfile.gettempdir()
        basename=os.path.basename(norm_path)
        temp_file_name='{0}.lock'.format(basename)
        norm_lock_path = os.path.join(temp_dir, temp_file_name)
        return norm_lock_path
            
    @staticmethod
    def is_locked(path):
        lock_path=lockfile.get_lock_filename(path)
        if os.path.exists(lock_path):
            with open(lock_path,'r') as lock:
                file_lock_time=datetime.datetime.strptime(lock.readline())
                curent_datetime =datetime.datetime.now()
                elapsed_time=curent_datetime-file_lock_time
                # its an old lock thats failed. time to long. remove it
                if elapsed_time.seconds()>10*1:
                    lockfile.remove(path)
                    return None
            return True
        return None

    @staticmethod
    def remove(path):
        lock_path=lockfile.get_lock_filename(path)
        if os.path.exists(lock_path)==False:
            raise Exception ("Lockfile cannot be removed, it doesnt exist. {0}".format(lock_path))
        os.remove(lock_path)
        if os.path.exists(lock_path):
            raise Exception ("Lockfile cannot be removed. {0}".format(lock_path))

    @staticmethod
    def create(path):
        lock_path=lockfile.get_lock_filename(path)
        if os.path.exists(lock_path):
            raise Exception ("Lockfile already exists. {0}".format(lock_path))
        with open(lock_path,'w') as lock:
            lock.write(datetime.datetime.now())
        if os.path.exists(lock_path)==False:
            raise Exception ("Lockfile failed to create {0}".format(lock_path))
        