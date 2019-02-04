
import datetime


class functions():
    # TODO Central spot for this
    COMMENT=1
    ERROR=2
    DATA=3
    WHITESPACE=4


    def f_show_columns(self,database, query_object):
        table = database.get(query_object['meta']['from']['table'])
        temp_table = database.temp_table(columns=['table', 'column'])

        for c in table.columns:
            columns = {'data': [table.data.name, c.data.name], 'type': self.DATA, 'error': None}
            temp_table.append_data(columns)
        return temp_table


    def f_show_tables(self,database):
        temp_table = database.temp_table(columns=['database', 'table'])
        for t in database.tables:
            columns = [t.data.database, t .data.name]
            temp_table.append_data({'data': columns, 'type': self.DATA, 'error': None})
        #print temp_table
        return temp_table


    def f_show_errors(self,database, table):
        temp_table = database.temp_table(columns=['error'])
        for e in table.errors:
            columns = [e]
            temp_table.append_data({'data': columns, 'type': self.DATA, 'error': None})
        return temp_table


    def f_database(self,database):
        return database.get_curent_database()

    def f_upper(self,arg):
        if not arg:
            return None
        return arg.upper()

    def f_lower(self,arg):
        if not arg:
            return None
        return arg.lower()

    def f_datetime(self,arg=None):
        return datetime.datetime.now()

    def f_time(self,arg=None):
        return datetime.datetime.now().strftime('%H:%M:%S')

    def f_date(self,arg=None):
        return datetime.datetime.now().strftime('%Y-%m-%d')

    def f_version(self,version=None):
        if None==version:
            return 'GA.BB.LE'
        return version
            
    def f_cat(self,arg1,arg2):
        if None ==arg1:
            arg1=''
        if None ==arg2:
            arg2=''
        return '{0}{1}'.format(arg1,arg2)

