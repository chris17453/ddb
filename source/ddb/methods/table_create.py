from .record_core import  process_line, swap_files, query_results


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

        found_delimiter = None
        found_comments = None
        found_whitespace = None
        found_data_on = None
        found_errors = None
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
            print("FIND DATA STARTS ON",found_data_on )
            
        results = context.database.create_table(table_name=query_object['meta']['table'],
                                                database_name=database_name,
                                                columns=columns,
                                                data_file=query_object['meta']['file'],
                                                delimiter=found_delimiter,
                                                comments=found_comments,
                                                errors=found_errors,
                                                whitespace=found_whitespace,
                                                data_on=found_data_on,
                                                temporary=temporary
                                                )

        return query_results(success=results)
    except Exception as ex:
        #print(ex)
        return query_results(success=False, error=ex)
