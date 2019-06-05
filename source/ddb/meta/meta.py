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

    class _and:
        __slots__=()
        c                    = None
        e1                   = None
        e2                   = None

        def __init__(self,c=None,e1=None,e2=None):
            if c                   :  self.c=c
            if e1                  :  self.e1=e1
            if e2                  :  self.e2=e2

        def debug(self):
            print('  Debug Info: and')
            print('  c:                   {0}'.format(self.c))
            print('  e1:                  {0}'.format(self.e1))
            print('  e2:                  {0}'.format(self.e2))

    class _group_by:
        __slots__=()
        column               = None

        def __init__(self,column=None):
            if column              :  self.column=column

        def debug(self):
            print('  Debug Info: group_by')
            print('  column:              {0}'.format(self.column))

    class _source:
        __slots__=()
        table                = None
        display              = None
        database             = None

        def __init__(self,table=None,display=None,database=None):
            if table               :  self.table=table
            if display             :  self.display=display
            if database            :  self.database=database

        def debug(self):
            print('  Debug Info: source')
            print('  table:               {0}'.format(self.table))
            print('  display:             {0}'.format(self.display))
            print('  database:            {0}'.format(self.database))

    class _limit:
        __slots__=()
        start                = 0
        length               = 0

        def __init__(self,start=None,length=None):
            if start               :  self.start=start
            if length              :  self.length=length

        def debug(self):
            print('  Debug Info: limit')
            print('  start:               {0}'.format(self.start))
            print('  length:              {0}'.format(self.length))

    class _where:
        __slots__=()
        c                    = None
        e1                   = None
        e2                   = None

        def __init__(self,c=None,e1=None,e2=None):
            if c                   :  self.c=c
            if e1                  :  self.e1=e1
            if e2                  :  self.e2=e2

        def debug(self):
            print('  Debug Info: where')
            print('  c:                   {0}'.format(self.c))
            print('  e1:                  {0}'.format(self.e1))
            print('  e2:                  {0}'.format(self.e2))

    class _or:
        __slots__=()
        c                    = None
        e1                   = None
        e2                   = None

        def __init__(self,c=None,e1=None,e2=None):
            if c                   :  self.c=c
            if e1                  :  self.e1=e1
            if e2                  :  self.e2=e2

        def debug(self):
            print('  Debug Info: or')
            print('  c:                   {0}'.format(self.c))
            print('  e1:                  {0}'.format(self.e1))
            print('  e2:                  {0}'.format(self.e2))

    class _columns:
        __slots__=()
        function             = None
        column               = None
        argument2            = None
        argument3            = None
        argument1            = None
        display              = None

        def __init__(self,function=None,column=None,argument2=None,argument3=None,argument1=None,display=None):
            if function            :  self.function=function
            if column              :  self.column=column
            if argument2           :  self.argument2=argument2
            if argument3           :  self.argument3=argument3
            if argument1           :  self.argument1=argument1
            if display             :  self.display=display

        def debug(self):
            print('  Debug Info: columns')
            print('  function:            {0}'.format(self.function))
            print('  column:              {0}'.format(self.column))
            print('  argument2:           {0}'.format(self.argument2))
            print('  argument3:           {0}'.format(self.argument3))
            print('  argument1:           {0}'.format(self.argument1))
            print('  display:             {0}'.format(self.display))

    class _order_by:
        __slots__=()
        column               = None
        direction            = None

        def __init__(self,column=None,direction=None):
            if column              :  self.column=column
            if direction           :  self.direction=direction

        def debug(self):
            print('  Debug Info: order_by')
            print('  column:              {0}'.format(self.column))
            print('  direction:           {0}'.format(self.direction))

    group_by             = None        # optional [ group by() ]
    source               = None        # optional source()
    limit                = None        # optional limit()
    where                = None        # optional [ where() ]
    columns              = []          #          columns()
    order_by             = None        # optional [ order by() ]

    def __init__(self,so):
