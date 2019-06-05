# This is an auto generated assembly 
# dont edit this, edit the template generator, in tools 


def gv(o,keys):
    #print ("GV")
    #print keys
    #print o
    if o:
        if isinstance(keys,str):
            #print("It's a string")
            if keys in o:
                o=o[keys]
            else:
                #print ("NO STRING")
                return None
        else:
            #print("It's not a string")
            for key in keys:
                #print ("->{0}".format(key))
                if key in o:
                    #print ("Got It")
                    o=o[key]
                else:
                    #print ("NO ARRAY")
                    return None
    else:     
        #print ("NO OBJECT")
        return None
    #print ("GV -exit ")
    #print (o)
    return o



class show_columns:
    __slots__=()

    class _source:
        __slots__=()
        table                = None
        database             = None

        def __init__(self,table=None,database=None):
            if table               :  self.table=table
            if database            :  self.database=database

        def debug(self):
            print('  Debug Info: source')
            print('  table:               {0}'.format(self.table))
            print('  database:            {0}'.format(self.database))

    source               = _source()

    def __init__(self,so):
            if gv(so,['meta','show_columns','source']):
                self.source              = self._source(table = gv(so,['meta','source','table']),database = gv(so,['meta','source','database']))

    def debug(self):
        print('Debug Info: show_columns')
        if self.source:
            self.source.debug()
        else:
            print('source:              {0}'.format(self.source))


class show_tables:
    __slots__=()


    def __init__(self,so=None):
          a=1

    def debug(self):
        print('Debug Info: show_tables')
        print('No variables')


class show_variables:
    __slots__=()


    def __init__(self,so=None):
          a=1

    def debug(self):
        print('Debug Info: show_variables')
        print('No variables')


class select:
    __slots__=()
