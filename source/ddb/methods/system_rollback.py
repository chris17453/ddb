# cython: linetrace=True

from .record_core import query_results
from ..file_io.locking import lock, remove_temp_file


def method_system_rollback(context):
    context.info("set")
    try:
        if context.internal['IN_TRANSACTION']==1:
            # TODO ROLLBACK
            context.internal['IN_TRANSACTION']=0
            context.system['AUTOCOMMIT']=context.internal['AUTOCOMMIT_HOLODER']

            for table_key in context.internal['TEMP_FILES']:
                tmp=context.internal['TEMP_FILES'][table_key]
                remove_temp_file(tmp['temp_source'])
                lock.release(table_key)
            # clear
            context.internal['TEMP_FILES']={}
                    
        else:
            raise Exception("Cannot rollback, not in a transaction")
        return query_results(success=True)
    except Exception as ex:
        return query_results(success=False,error=ex)
