# cython: profile=True
# cython: profile=True


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
                context.info("Commit {0}".format(table_key))
                tmp=context.internal['TEMP_FILES'][table_key]
                # no need to swap files if nothing was written yea? Just delete the temp data
                if None== tmp['written']:
                    context.info("Release Lock for {0}".format(tmp['temp_source']))

                    remove_temp_file(tmp['temp_source'])
                    context.info("Commit NOT Written..")
                    lock.release(table_key)
                else:
                    context.info("File was written {0}".format(table_key))
                    context.info("Commit Written..")
                    swap_files(tmp['origin'],tmp['temp_source'],context.system['UUID'])
                    context.info("Swap Files finished {0}->{1}".format(tmp['origin'],tmp['temp_source']))
                
                    if tmp['table'].data.repo_type=='svn':
                       context.svn_commit_file(tmp['table'])

            # clear
            context.internal['TEMP_FILES']={}
            #print ("Temp Flags Files Cleared")
        else:
            #print("Not in transaction")
            raise Exception("Cannot commit, not in a transaction")
            
            
        return query_results(success=True)
    except Exception as ex:
        context.error (__name__,ex)
        return query_results(success=False,error=ex)
