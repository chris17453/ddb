
import datetime



def f_database(context):
    if None==context:
        raise Exception("No database instance. ")
    return context.database.get_curent_database()

def f_upper(context,arg):
    if None==context:
        raise Exception("No database instance. ")
    if not arg:
        return None
    return arg.upper()

def f_lower(context,arg):
    if None==context:
        raise Exception("No database instance. ")
    if not arg:
        return None
    return arg.lower()

def f_datetime(context,arg=None):
    if None==context:
        raise Exception("No database instance. ")
    return datetime.datetime.now()

def f_time(context,arg=None):
    if None==context:
        raise Exception("No database instance. ")
    return datetime.datetime.now().strftime('%H:%M:%S')

def f_date(context,arg=None):
    if None==context:
        raise Exception("No database instance. ")
    return datetime.datetime.now().strftime('%Y-%m-%d')

def f_version(context,version=None):
    if None==context:
        raise Exception("No database instance. ")
    if None==version:
        return 'GA.BB.LE'
    return version
        
def f_cat(context,arg1,arg2):
    if None==context:
        raise Exception("No database instance. ")
    if None ==arg1:
        arg1=''
    if None ==arg2:
        arg2=''
    return '{0}{1}'.format(arg1,arg2)

