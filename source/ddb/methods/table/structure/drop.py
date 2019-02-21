
def method_drop_table(context, query_object):
    context.info("Drop Table")
    results = context.database.drop_table(table_name=query_object['meta']['drop']['table'])
    return results
