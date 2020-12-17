import sys
import pprint
from .record_core import query_results
from ..file_io.locking import swap_files, lock, remove_temp_file


# creates a local copy of the already LOCAL files that are about to be commited
# incase a group transaction needs rolling back we can restore the files to 
# this state
def backup_local_source_files(context):
    context.info("ENTERING","BACKUP")
    # backup source files before attempted commit
    for table_key in context.internal['TEMP_FILES']:
        context.info("Backing up source table {0}".format(table_key))
        tmp=context.internal['TEMP_FILES'][table_key]
        table=tmp['table']
        # no need to swap files if nothing was written yea? Just delete the temp data
        if None != tmp['written']:
            context.duplicate_local_data_file(table)
            context.info("Temp Source Files backed up {0}->{1}".format(tmp['origin'],tmp['temp_local']))


def move_svn_tempo_to_repo(context):
    context.info("ENTERING","MOVE SVN FROM TEMP TO REPO")
    # backup source files before attempted commit
    for table_key in context.internal['TEMP_FILES']:
        context.info("Moving Temp to SVN REPO up source table {0}".format(table_key))
        tmp=context.internal['TEMP_FILES'][table_key]
        table=tmp['table']
        # no need to swap files if nothing was written yea? Just delete the temp data
        if None != tmp['written']:
            context.move_svn_temp_file(table)
            context.info("SVN FILE MOVED {0}->{1}".format(tmp['temp_local'],tmp['origin']))


# remove locally created temp files for backup_local_source_files
def delete_local_temp_source_files(context):
    context.info("ENTERING","DELETE LOCAL")
    for table_key in context.internal['TEMP_FILES']:
        context.info("deleting temp source table {0}".format(table_key))
        tmp=context.internal['TEMP_FILES'][table_key]
        table=tmp['table']
        # no need to swap files if nothing was written yea? Just delete the temp data
        if None != tmp['written']:
            context.delete_local_backup_data_file(table)
            context.info("Temp Source file deleted {0}".format(tmp['temp_local']))

# reverts failed transacional files created by for backup_local_source_files, DOES NOT DELETE TEMP
def revert_local_source_files(context):
    context.info("ENTERING","REVERT LOCAL")
    for table_key in context.internal['TEMP_FILES']:
        context.info("deleting temp source table {0}".format(table_key))
        tmp=context.internal['TEMP_FILES'][table_key]
        table=tmp['table']
        # no need to swap files if nothing was written yea? Just delete the temp data
        if None != tmp['written']:
            #print(tmp)
            context.revert_local_data_file(table)
            context.info("Source file restored, temp file deleted {0}->{1}".format(tmp['temp_local'],tmp['origin']))

  # commit local files
def commit_local_files(context):
    context.info("ENTERING","COMMIT LOCAL")
    for table_key in context.internal['TEMP_FILES']:
        tmp=context.internal['TEMP_FILES'][table_key]

        if tmp['table'].data.repo_type=='svn':
            continue

        # no need to swap files if nothing was written yea? Just delete the temp data
        if None== tmp['written']:
            context.info("Commit LOCAL {0}".format(table_key))
            context.info("Release Lock for {0}".format(tmp['temp_source']))
            remove_temp_file(tmp['temp_source'])
            context.info("Commit NOT Written..")
            lock.release(table_key)
        else:
            context.info("Commit LOCAL {0}".format(table_key))
            context.info("File was written {0}".format(table_key))
            context.info("Commit Written..")
            context.info("Swap Files finished {0}->{1}".format(tmp['origin'],tmp['temp_source']))

def commit_svn_files(context):
    # commit all REPO type files at once...
    context.info("ENTERING","COMMIT SVN")
    move_svn_tempo_to_repo(context)
    svn_repos_by_dir={}
    for table_key in context.internal['TEMP_FILES']:
        tmp=context.internal['TEMP_FILES'][table_key]

        if tmp['table'].data.repo_type=='svn':
            repo_dir  =tmp['table'].data.repo_dir
            table_name=tmp['table'].data.name
            # if the directory isnt in the lookup.. add it
            if repo_dir not in svn_repos_by_dir:
                svn_repos_by_dir[repo_dir]={}
            # if the table isnt in the repo dir lookup add it
            if table_name not in svn_repos_by_dir[repo_dir]:
                svn_repos_by_dir[repo_dir][table_name]=tmp['table']

    # commit files for SVN STARTS HERE
    for repo_dir in svn_repos_by_dir:
        context.info("Commit SVN {0}".format(repo_dir))
        # individually commit each repo directory and all of its changed files
        context.svn_commit_files(svn_repos_by_dir[repo_dir])


# the base system command for commiting a transaction or set of transactions from temp files back to the master source (local or remote)
def method_system_commit(context):
    debug_holder=context.debug
    context.debug=True
    if context.internal['IN_TRANSACTION']!=1:
        return query_results(success=False,error="Cannot commit, Not in transaction")


    # COMIT
    context.internal['IN_TRANSACTION']=0
    #context.system['AUTOCOMMIT']=context.internal['AUTOCOMMIT_HOLODER']
    #pprint.pprint(context.internal['TEMP_FILES'])
    
    try:
        backup_local_source_files(context)
        commit_local_files(context)

        
        commit_svn_files(context)
        delete_local_temp_source_files(context)

        # clear
        context.internal['TEMP_FILES']={}
        #print ("Temp Flags Files Cleared")
        context.debug=debug_holder
        return query_results(success=True)
    except Exception as ex:
        print(ex)
        # roll back master duplicated
        revert_local_source_files(context)
        delete_local_temp_source_files(context)
        context.debug=debug_holder
        return query_results(success=False,error=ex.message)
