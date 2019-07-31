# cython: linetrace=True
import pprint
from .record_core import query_results
from ..file_io.locking import swap_files, lock, remove_temp_file

def method_system_commit(context):
    """Move temp files to source files"""
    context.info("Commit")
    try:
        if context.internal['IN_TRANSACTION']==1:
            # TODO COMIT
            context.internal['IN_TRANSACTION']=0
            context.system['AUTOCOMMIT']=context.internal['AUTOCOMMIT_HOLODER']=True
            #pprint.pprint(context.internal['TEMP_FILES'])

            for table_key in context.internal['TEMP_FILES']:
                tmp=context.internal['TEMP_FILES'][table_key]
                # no need to swap files if nothing was written yea? Just delete the temp data
                if None== tmp['written']:
                    remove_temp_file(tmp['temp_source'])
                    lock.release(table_key)
                else:
                    swap_files(tmp['origin'],tmp['temp_source'],context.system['UUID'])
                    if tmp['table'].data.repo_type=='svn':
                       context.svn_commit_file(tmp['table'])

            # clear
            context.internal['TEMP_FILES']={}

        else:
            raise Exception("Cannot commit, not in a transaction")
            
            
        return query_results(success=True)
    except Exception as ex:
        return query_results(success=False,error=ex)
