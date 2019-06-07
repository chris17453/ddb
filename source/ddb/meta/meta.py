
class debugger:
    def __init__(self,obj,depth=0):
        print ("Debug:")
        variables = [i for i in dir(obj) if not i.startswith('__')]
        empty=[]
        pad=''
        for i in range(0,depth):
            pad+=' '

        for var in variables:
            value=getattr(obj,var)
            if  isinstance(value,str):
                print("{2}{0:<20}{1}".format(var+':',value,pad))
            elif isinstance(value,list):
                for item in value:
                    debugger(item,depth+1)
            elif value!=None:
                print("{2}{0:<20}{1}".format(var+':','class',pad))
                debugger(value,depth+1)
            else:
                empty.append(var)
        if len(empty)>0:
            print ("{1}Empty Vars: {0}".format(",".join(empty),pad))

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
            if gv(so,['meta','source']):
                self.source              = self._source(table = gv(so,['meta','source','table']),database = gv(so,['meta','source','database']))
    def debug(self):
        debugger(self)


class show_tables:
    __slots__=()

    def debug(self):
        debugger(self)


class show_variables:
    __slots__=()

    def debug(self):
        debugger(self)


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
            if gv(so,['meta','select','group by']):
                self.group_by            =[]
                for item in gv(so,['meta','group by']):
                    self.group_by            .append( self._group_by(column = gv(item,['column'])) )
            if gv(so,['meta','source']):
                self.source              = self._source(table = gv(so,['meta','source','table']),display = gv(so,['meta','source','display']),database = gv(so,['meta','source','database']))
            if gv(so,['meta','limit']):
                self.limit               = self._limit(start = gv(so,['meta','limit','start']),length = gv(so,['meta','limit','length']))
            if gv(so,['meta','select','where']):
                self.where               =[]
                for item in gv(so,['meta','where']):
                    self.where               .append( self._where(c = gv(item,['c']),e1 = gv(item,['e1']),e2 = gv(item,['e2'])) )
            if gv(so,['meta','columns']):
                self.columns             =[]
                for item in gv(so,['meta','columns']):
                    self.columns             .append( self._columns(function = gv(item,['function']),column = gv(item,['column']),argument2 = gv(item,['argument2']),argument3 = gv(item,['argument3']),argument1 = gv(item,['argument1']),display = gv(item,['display'])) )
            if gv(so,['meta','select','order by']):
                self.order_by            =[]
                for item in gv(so,['meta','order by']):
                    self.order_by            .append( self._order_by(column = gv(item,['column']),direction = gv(item,['direction'])) )
    def debug(self):
        debugger(self)


class set:
    __slots__=()

    class _set:
        __slots__=()
        variable             = None
        type                 = None
        value                = None

        def __init__(self,variable=None,type=None,value=None):
            if variable            :  self.variable=variable
            if type                :  self.type=type
            if value               :  self.value=value

        def debug(self):
            print('  Debug Info: set')
            print('  variable:            {0}'.format(self.variable))
            print('  type:                {0}'.format(self.type))
            print('  value:               {0}'.format(self.value))

    set                  = None        # optional [ set() ]

    def __init__(self,so):
            if gv(so,['meta','set','set']):
                self.set                 =[]
                for item in gv(so,['meta','set']):
                    self.set                 .append( self._set(variable = gv(item,['variable']),type = gv(item,['type']),value = gv(item,['value'])) )
    def debug(self):
        debugger(self)


class create_procedure:
    __slots__=()

    class _parameters:
        __slots__=()
        parameter            = None

        def __init__(self,parameter=None):
            if parameter           :  self.parameter=parameter

        def debug(self):
            print('  Debug Info: parameters')
            print('  parameter:           {0}'.format(self.parameter))

    parameters           = None        # optional [ parameters() ]

    def __init__(self,so):
            if gv(so,['meta','create_procedure','parameters']):
                self.parameters          =[]
                for item in gv(so,['meta','parameters']):
                    self.parameters          .append( self._parameters(parameter = gv(item,['parameter'])) )
    def debug(self):
        debugger(self)


class delimiter:
    __slots__=()

    delimiter            = None

    def __init__(self,so):
            self.delimiter            = gv(so,['meta','delimiter','delimiter'])
    def debug(self):
        debugger(self)


class end:
    __slots__=()

    def debug(self):
        debugger(self)


class begin:
    __slots__=()

    def debug(self):
        debugger(self)


class commit:
    __slots__=()

    def debug(self):
        debugger(self)


class rollback:
    __slots__=()

    def debug(self):
        debugger(self)


class show_output_modules:
    __slots__=()

    def debug(self):
        debugger(self)


class delete:
    __slots__=()

    class _and:
        __slots__=()
        type                 = None
        c                    = None
        e1                   = None
        e2                   = None

        def __init__(self,type=None,c=None,e1=None,e2=None):
            if type                :  self.type=type
            if c                   :  self.c=c
            if e1                  :  self.e1=e1
            if e2                  :  self.e2=e2

        def debug(self):
            print('  Debug Info: and')
            print('  type:                {0}'.format(self.type))
            print('  c:                   {0}'.format(self.c))
            print('  e1:                  {0}'.format(self.e1))
            print('  e2:                  {0}'.format(self.e2))

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

    class _where:
        __slots__=()
        type                 = None
        c                    = None
        e1                   = None
        e2                   = None

        def __init__(self,type=None,c=None,e1=None,e2=None):
            if type                :  self.type=type
            if c                   :  self.c=c
            if e1                  :  self.e1=e1
            if e2                  :  self.e2=e2

        def debug(self):
            print('  Debug Info: where')
            print('  type:                {0}'.format(self.type))
            print('  c:                   {0}'.format(self.c))
            print('  e1:                  {0}'.format(self.e1))
            print('  e2:                  {0}'.format(self.e2))

    class _or:
        __slots__=()
        type                 = None
        c                    = None
        e1                   = None
        e2                   = None

        def __init__(self,type=None,c=None,e1=None,e2=None):
            if type                :  self.type=type
            if c                   :  self.c=c
            if e1                  :  self.e1=e1
            if e2                  :  self.e2=e2

        def debug(self):
            print('  Debug Info: or')
            print('  type:                {0}'.format(self.type))
            print('  c:                   {0}'.format(self.c))
            print('  e1:                  {0}'.format(self.e1))
            print('  e2:                  {0}'.format(self.e2))

    source               = _source()
    where                = None        # optional [ where() ]

    def __init__(self,so):
            if gv(so,['meta','source']):
                self.source              = self._source(table = gv(so,['meta','source','table']),database = gv(so,['meta','source','database']))
            if gv(so,['meta','delete','where']):
                self.where               =[]
                for item in gv(so,['meta','where']):
                    self.where               .append( self._where(type = gv(item,['type']),c = gv(item,['c']),e1 = gv(item,['e1']),e2 = gv(item,['e2'])) )
    def debug(self):
        debugger(self)


class insert:
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

    class _values:
        __slots__=()
        value                = None

        def __init__(self,value=None):
            if value               :  self.value=value

        def debug(self):
            print('  Debug Info: values')
            print('  value:               {0}'.format(self.value))

    class _columns:
        __slots__=()
        column               = None

        def __init__(self,column=None):
            if column              :  self.column=column

        def debug(self):
            print('  Debug Info: columns')
            print('  column:              {0}'.format(self.column))

    source               = _source()
    values               = []          #          values()
    columns              = []          #          columns()

    def __init__(self,so):
            if gv(so,['meta','source']):
                self.source              = self._source(table = gv(so,['meta','source','table']),database = gv(so,['meta','source','database']))
            if gv(so,['meta','values']):
                self.values              =[]
                for item in gv(so,['meta','values']):
                    self.values              .append( self._values(value = gv(item,['value'])) )
            if gv(so,['meta','insert','columns']):
                self.columns             =[]
                for item in gv(so,['meta','columns']):
                    self.columns             .append( self._columns(column = gv(item,['column'])) )
    def debug(self):
        debugger(self)


class update:
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

    class _set:
        __slots__=()
        column               = None
        expression           = None

        def __init__(self,column=None,expression=None):
            if column              :  self.column=column
            if expression          :  self.expression=expression

        def debug(self):
            print('  Debug Info: set')
            print('  column:              {0}'.format(self.column))
            print('  expression:          {0}'.format(self.expression))

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

    source               = _source()
    set                  = []          #          set()
    where                = None        # optional [ where() ]

    def __init__(self,so):
            if gv(so,['meta','source']):
                self.source              = self._source(table = gv(so,['meta','source','table']),database = gv(so,['meta','source','database']))
            if gv(so,['meta','update','set']):
                self.set                 =[]
                for item in gv(so,['meta','set']):
                    self.set                 .append( self._set(column = gv(item,['column']),expression = gv(item,['expression'])) )
            if gv(so,['meta','update','where']):
                self.where               =[]
                for item in gv(so,['meta','where']):
                    self.where               .append( self._where(c = gv(item,['c']),e1 = gv(item,['e1']),e2 = gv(item,['e2'])) )
    def debug(self):
        debugger(self)


class upsert:
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

    class _values:
        __slots__=()
        value                = None

        def __init__(self,value=None):
            if value               :  self.value=value

        def debug(self):
            print('  Debug Info: values')
            print('  value:               {0}'.format(self.value))

    class _update:
        __slots__=()
        column               = None
        expression           = None

        def __init__(self,column=None,expression=None):
            if column              :  self.column=column
            if expression          :  self.expression=expression

        def debug(self):
            print('  Debug Info: update')
            print('  column:              {0}'.format(self.column))
            print('  expression:          {0}'.format(self.expression))

    class _columns:
        __slots__=()
        column               = None

        def __init__(self,column=None):
            if column              :  self.column=column

        def debug(self):
            print('  Debug Info: columns')
            print('  column:              {0}'.format(self.column))

    class _on_duplicate_key:
        __slots__=()
        column               = None

        def __init__(self,column=None):
            if column              :  self.column=column

        def debug(self):
            print('  Debug Info: on_duplicate_key')
            print('  column:              {0}'.format(self.column))

    source               = _source()
    values               = []          #          values()
    update               = []          #          update()
    columns              = []          #          columns()
    on_duplicate_key     = []          #          on duplicate key()

    def __init__(self,so):
            if gv(so,['meta','source']):
                self.source              = self._source(table = gv(so,['meta','source','table']),database = gv(so,['meta','source','database']))
            if gv(so,['meta','values']):
                self.values              =[]
                for item in gv(so,['meta','values']):
                    self.values              .append( self._values(value = gv(item,['value'])) )
            if gv(so,['meta','upsert','update']):
                self.update              =[]
                for item in gv(so,['meta','update']):
                    self.update              .append( self._update(column = gv(item,['column']),expression = gv(item,['expression'])) )
            if gv(so,['meta','columns']):
                self.columns             =[]
                for item in gv(so,['meta','columns']):
                    self.columns             .append( self._columns(column = gv(item,['column'])) )
            if gv(so,['meta','upsert','on duplicate key']):
                self.on_duplicate_key    =[]
                for item in gv(so,['meta','on duplicate key']):
                    self.on_duplicate_key    .append( self._on_duplicate_key(column = gv(item,['column'])) )
    def debug(self):
        debugger(self)


class use_table:
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
            if gv(so,['meta','source']):
                self.source              = self._source(table = gv(so,['meta','source','table']),database = gv(so,['meta','source','database']))
    def debug(self):
        debugger(self)


class drop_table:
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
            if gv(so,['meta','source']):
                self.source              = self._source(table = gv(so,['meta','source','table']),database = gv(so,['meta','source','database']))
    def debug(self):
        debugger(self)


class create_table:
    __slots__=()

    class _repo:
        __slots__=()
        protocol             = 'svn'
        url                  = None
        user                 = None
        file                 = None
        directory            = None
        password             = None

        def __init__(self,protocol=None,url=None,user=None,file=None,directory=None,password=None):
            if protocol            :  self.protocol=protocol
            if url                 :  self.url=url
            if user                :  self.user=user
            if file                :  self.file=file
            if directory           :  self.directory=directory
            if password            :  self.password=password

        def debug(self):
            print('  Debug Info: repo')
            print('  protocol:            {0}'.format(self.protocol))
            print('  url:                 {0}'.format(self.url))
            print('  user:                {0}'.format(self.user))
            print('  file:                {0}'.format(self.file))
            print('  directory:           {0}'.format(self.directory))
            print('  password:            {0}'.format(self.password))

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

    class _columns:
        __slots__=()
        column               = None

        def __init__(self,column=None):
            if column              :  self.column=column

        def debug(self):
            print('  Debug Info: columns')
            print('  column:              {0}'.format(self.column))

    errors               = None        # optional 
    whitespace           = None        # optional 
    strict               = None        # optional 
    data_starts_on       = None        # optional 
    fifo                 = None        # optional 
    repo                 = None        # optional repo()
    source               = _source()
    delimiter            = None        # optional 
    mode                 = None        # optional 
    file                 = None
    columns              = []          #          columns()
    comments             = None        # optional 

    def __init__(self,so):
            self.errors               = gv(so,['meta','errors'])
            self.whitespace           = gv(so,['meta','whitespace'])
            self.strict               = gv(so,['meta','strict'])
            self.data_starts_on       = gv(so,['meta','data_starts_on'])
            self.fifo                 = gv(so,['meta','fifo'])
            if gv(so,['meta','repo']):
                self.repo                = self._repo(protocol = gv(so,['meta','repo','protocol']),url = gv(so,['meta','repo','url']),user = gv(so,['meta','repo','user']),file = gv(so,['meta','repo','file']),directory = gv(so,['meta','repo','directory']),password = gv(so,['meta','repo','password']))
            if gv(so,['meta','source']):
                self.source              = self._source(table = gv(so,['meta','source','table']),database = gv(so,['meta','source','database']))
            self.delimiter            = gv(so,['meta','delimiter'])
            self.mode                 = gv(so,['meta','mode'])
            self.file                 = gv(so,['meta','file'])
            if gv(so,['meta','columns']):
                self.columns             =[]
                for item in gv(so,['meta','columns']):
                    self.columns             .append( self._columns(column = gv(item,['column'])) )
            self.comments             = gv(so,['meta','comments'])
    def debug(self):
        debugger(self)


class update_table:
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

    class _columns:
        __slots__=()
        column               = None

        def __init__(self,column=None):
            if column              :  self.column=column

        def debug(self):
            print('  Debug Info: columns')
            print('  column:              {0}'.format(self.column))

    errors               = None        # optional 
    whitespace           = None        # optional 
    data_starts_on       = None        # optional 
    comments             = None        # optional 
    source               = _source()
    delimiter            = None        # optional 
    file                 = None        # optional 
    columns              = None        # optional [ columns() ]

    def __init__(self,so):
            self.errors               = gv(so,['meta','errors','errors'])
            self.whitespace           = gv(so,['meta','whitespace','whitespace'])
            self.data_starts_on       = gv(so,['meta','data_starts_on','data_starts_on'])
            self.comments             = gv(so,['meta','comments','comments'])
            if gv(so,['meta','source']):
                self.source              = self._source(table = gv(so,['meta','source','table']),database = gv(so,['meta','source','database']))
            self.field                = gv(so,['meta','delimiter','field'])
            self.file                 = gv(so,['meta','file','file'])
            if gv(so,['meta','columns']):
                self.columns             =[]
                for item in gv(so,['meta','columns']):
                    self.columns             .append( self._columns(column = gv(item,['column'])) )
    def debug(self):
        debugger(self)


class describe_table:
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
            if gv(so,['meta','source']):
                self.source              = self._source(table = gv(so,['meta','source','table']),database = gv(so,['meta','source','database']))
    def debug(self):
        debugger(self)



def convert_to_class(o):
    
    if o['mode']=='show columns': return show_columns(o)
    elif o['mode']=='show tables': return show_tables(o)
    elif o['mode']=='show variables': return show_variables(o)
    elif o['mode']=='select': return select(o)
    elif o['mode']=='set': return set(o)
    elif o['mode']=='create procedure': return create_procedure(o)
    elif o['mode']=='delimiter': return delimiter(o)
    elif o['mode']=='end': return end(o)
    elif o['mode']=='begin': return begin(o)
    elif o['mode']=='commit': return commit(o)
    elif o['mode']=='rollback': return rollback(o)
    elif o['mode']=='show output modules': return show_output_modules(o)
    elif o['mode']=='delete': return delete(o)
    elif o['mode']=='insert': return insert(o)
    elif o['mode']=='update': return update(o)
    elif o['mode']=='upsert': return upsert(o)
    elif o['mode']=='use table': return use_table(o)
    elif o['mode']=='drop table': return drop_table(o)
    elif o['mode']=='create table': return create_table(o)
    elif o['mode']=='update table': return update_table(o)
    elif o['mode']=='describe table': return describe_table(o)

    return None


