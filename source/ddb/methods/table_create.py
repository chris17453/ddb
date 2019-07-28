
# cython: profile=True
# cython: linetrace=True
# cython: binding=True


from .record_core import  query_results,get_table


def method_create_table(context, meta):
    context.info("Create Table")
    try:
        table=get_table(context,meta)

        columns = []
        if meta.column==None:
            raise Exception("Missing columns, cannot create table")

        # TODO convert to meta class
        for c in meta.columns:
            columns.append(c['column'])
        context.info("Columns to create", columns)

        if None==meta.source.database:
            meta.source.database=context.database.get_curent_database()

        results = context.database.create_table(table_name    = meta.source.table,
                                                database_name = meta.source.database,
                                                columns       = columns,
                                                data_file     = meta.file,
                                                delimiter     = meta.delimiter,
                                                comments      = meta.comments,
                                                errors        = meta.errors,
                                                whitespace    = meta.whitespace,
                                                data_on       = meta.data_on,
                                                temporary     = meta.temporary,
                                                fifo          = meta.fifo,
                                                repo_type     = meta.repo.protocol,
                                                repo_url      = meta.repo.url,
                                                repo_user     = meta.repo.user,
                                                repo_password = meta.repo.password,
                                                repo_file     = meta.repo.file,                                                
                                                repo_dir      = meta.repo.directory,
                                                strict_columns= meta.strict,
                                                mode          = meta.mode
                                                )
      
        return query_results(success=results)
    except Exception as ex:
        print ex
        return query_results(success=False, error=ex)
