from ..core import query_results

def method_drop_table(context, query_object):
    context.info("Drop Table")
    try:
        results = context.database.drop_table(table_name=query_object['meta']['drop']['table'])
        return query_results(success=results)
    except Exception as ex:
        print("EHG",ex)
        return query_results(success=False,error=ex)
