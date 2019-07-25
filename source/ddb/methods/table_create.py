
# cython: profile=True
# cython: linetrace=True
# cython: binding=True


from .record_core import  process_line, query_results


def method_create_table(context, query_object):
    context.info("Create Table")
    try:
        #print(query_object)
        if 'database' in query_object['meta']:
            context.info('Database specified')
            database_name = query_object['meta']['database']
        else:
            context.info('Using curent database context')
            database_name = context.database.get_curent_database()

        columns = []
        if 'columns' not in query_object['meta']:
            raise Exception("Missing columns, cannot create table")

        for c in query_object['meta']['columns']:
            columns.append(c['column'])
        context.info("Columns to create", columns)

        if 'temporary' in query_object['meta']:
            temporary = True
            context.info("Creating temporary table")
        else:
            temporary = None

        strict_columns=None
        found_delimiter = None
        found_comments = None
        found_whitespace = None
        found_data_on = None
        found_errors = None
        fifo = None
        mode = None
        if 'delimiter' in query_object['meta']:
            found_delimiter = query_object['meta']['delimiter']
        if 'whitespace' in query_object['meta']:
            found_whitespace = query_object['meta']['whitespace']
        if 'comments' in query_object['meta']:
            found_comments = query_object['meta']['comments']
        if 'errors' in query_object['meta']:
            found_errors = query_object['meta']['errors']
        if 'data_starts_on' in query_object['meta']:
            found_data_on = query_object['meta']['data_starts_on']
        if 'strict' in query_object['meta']:
            strict_columns = query_object['meta']['strict']
        if 'fifo' in query_object['meta']:
            fifo = query_object['meta']['fifo']
        if 'mode' in query_object['meta']:
            mode = query_object['meta']['mode']
        
        #print query_object
        if 'repo_type' in query_object['meta']:
            repo=query_object['meta']
            if 'repo' in repo:
                repo_type=repo['protocol']
            if 'repo_url' in repo:
                repo_url=repo['url']
            if 'repo_user' in repo:
                repo_user=repo['user']
            if 'repo_password' in repo:
                repo_password=repo['password']
            if 'repo_dir' in repo:
                repo_dir=repo['directory']
            if 'repo_file' in repo:
                repo_file=repo['file']
        else:
            repo_type=None
            repo_url=None
            repo_user=None
            repo_password=None
            repo_dir=None
            repo_file=None


        results = context.database.create_table(table_name=query_object['meta']['table'],
                                                database_name=database_name,
                                                columns=columns,
                                                data_file=query_object['meta']['file'],
                                                delimiter=found_delimiter,
                                                comments=found_comments,
                                                errors=found_errors,
                                                whitespace=found_whitespace,
                                                data_on=found_data_on,
                                                temporary=temporary,
                                                fifo=fifo,
                                                repo_type=repo_type,
                                                repo_url=repo_url,
                                                repo_user=repo_user,
                                                repo_password=repo_password,
                                                repo_dir=repo_dir,
                                                repo_file=repo_file,                                                
                                                strict_columns=strict_columns,
                                                mode=mode
                                                )

        return query_results(success=results)
    except Exception as ex:
        print ex
        return query_results(success=False, error=ex)
