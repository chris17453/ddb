# cython: linetrace=True

from .record_core import query_results, get_table

def method_describe_table(context, meta):
    """Populates metadata related to a table
    returns: table"""
    context.info("Describe Table")
    try:

        target_table=get_table(context,meta)
        if None ==target_table:
            raise Exception("Table not found")
        temp_table = context.database.temp_table(columns=['option','value'])

        
        temp_table.append_data( { 'data': [ 'active'             , target_table.active              ], 'type': context.data_type.DATA, 'error': None} )
        temp_table.append_data( { 'data': [ 'table_name'         , target_table.data.name           ], 'type': context.data_type.DATA, 'error': None} )
        temp_table.append_data( { 'data': [ 'database'           , target_table.data.database       ], 'type': context.data_type.DATA, 'error': None} )
        temp_table.append_data( { 'data': [ 'data_file'          , target_table.data.path           ], 'type': context.data_type.DATA, 'error': None} )
        temp_table.append_data( { 'data': [ 'fifo'               , target_table.data.fifo           ], 'type': context.data_type.DATA, 'error': None} )
        temp_table.append_data( { 'data': [ 'type'               , target_table.data.type           ], 'type': context.data_type.DATA, 'error': None} )
        temp_table.append_data( { 'data': [ 'config_file'        , target_table.data.config         ], 'type': context.data_type.DATA, 'error': None} )
        temp_table.append_data( { 'data': [ 'data_starts_on'     , target_table.data.starts_on_line ], 'type': context.data_type.DATA, 'error': None} )
        temp_table.append_data( { 'data': [ 'field_delimiter'    , target_table.delimiters.field    ], 'type': context.data_type.DATA, 'error': None} )
        temp_table.append_data( { 'data': [ 'comments_visible'   , target_table.visible.comments    ], 'type': context.data_type.DATA, 'error': None} )
        temp_table.append_data( { 'data': [ 'errors_visible'     , target_table.visible.errors      ], 'type': context.data_type.DATA, 'error': None} )
        temp_table.append_data( { 'data': [ 'whitespace_visible' , target_table.visible.whitespace  ], 'type': context.data_type.DATA, 'error': None} )
        temp_table.append_data( { 'data': [ 'strict_columns'     , target_table.data.strict_columns ], 'type': context.data_type.DATA, 'error': None} )
        temp_table.append_data( { 'data': [ 'repo_type'          , target_table.data.repo_type      ], 'type': context.data_type.DATA, 'error': None} )
        temp_table.append_data( { 'data': [ 'repo_url'           , target_table.data.repo_url       ], 'type': context.data_type.DATA, 'error': None} )
        temp_table.append_data( { 'data': [ 'repo_dir'           , target_table.data.repo_dir       ], 'type': context.data_type.DATA, 'error': None} )
        temp_table.append_data( { 'data': [ 'repo_file'          , target_table.data.repo_file      ], 'type': context.data_type.DATA, 'error': None} )
        temp_table.append_data( { 'data': [ 'user'               , target_table.data.repo_user      ], 'type': context.data_type.DATA, 'error': None} )
        temp_table.append_data( { 'data': [ 'password'           , target_table.data.repo_password  ], 'type': context.data_type.DATA, 'error': None} )

        return query_results(success=True,data=temp_table)
    except Exception as ex:
       print ex
        return query_results(success=False,error=ex)



