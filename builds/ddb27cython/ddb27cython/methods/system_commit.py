import sys
import pprint
from .record_core import query_results
from ..file_io.locking import swap_files, lock, remove_temp_file

def method_system_commit(context):
    if context.internal['IN_TRANSACTION']==1:
        # TODO COMIT
        context.internal['IN_TRANSACTION']=0
        context.system['AUTOCOMMIT']=context.internal['AUTOCOMMIT_HOLODER']=True
        #pprint.pprint(context.internal['TEMP_FILES'])

        # First commit NON REPO FILES and copy temp files back to REPOS
        repos_to_commit={}

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
             # old way svn commit .. 1 at a time            
#            if tmp['table'].data.repo_type=='svn':
#                    context.svn_commit_file(tmp['table'])

        # not commit all REPO type files at once...
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
            context.info("Commit {0}".format(repo_dir))
            # individually commit each repo directory and all of its changed files
            context.svn_commit_files(svn_repos_by_dir[repo_dir])


                

        # clear
        context.internal['TEMP_FILES']={}
        #print ("Temp Flags Files Cleared")
    else:
        #print("Not in transaction")
        raise Exception("Cannot commit, not in a transaction")
        
        
    return query_results(success=True)
