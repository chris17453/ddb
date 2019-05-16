from .record_core import  process_line, query_results


def method_create_table(context, query_object):
    context.info("Create Table")
    try:
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
        print  query_object['meta']
        if 'repo' in query_object['meta']:
            repo=query_object['meta']['repo']
            if 'type' in repo:
                repo_type=repo['type']
            if 'url' in repo:
                repo_url=repo['url']
            if 'user' in repo:
                repo_user=repo['user']
            if 'password' in repo:
                repo_password=repo['password']
            if 'repo_dir' in repo:
                repo_dir=repo['repo_dir']
            if 'repo_file' in repo:
                repo_file=repo['repo_file']
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
                                                strict_columns=strict_columns
                                                )

        return query_results(success=results)
    except Exception as ex:
        print ex
        return query_results(success=False, error=ex)
