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
            print('source:             '.format(self.source))


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

        def debug(self):
            print('  Debug Info: and')
            print('  c:                   {0}'.format(self.c))
            print('  e1:                  {0}'.format(self.e1))
            print('  e2:                  {0}'.format(self.e2))

    class _group_by:
        __slots__=()
        column               = None

        def __init__(self,column=None):

        def debug(self):
            print('  Debug Info: group_by')
            print('  column:              {0}'.format(self.column))

    class _source:
        __slots__=()
        table                = None
        display              = None
        database             = None

        def __init__(self,table=None,display=None,database=None):

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
                for item in so['meta']['select']['group by']:
                    self.group_by            .append( self._group_by(column = gv(item,['column'])) )
            if gv(so,['meta','select','source']):
                self.source              = self._source(table = gv(so,['meta','source','table']),display = gv(so,['meta','source','display']),database = gv(so,['meta','source','database']))
            if gv(so,['meta','select','limit']):
                self.limit               = self._limit(start = gv(so,['meta','limit','start']),length = gv(so,['meta','limit','length']))
            if gv(so,['meta','select','where']):
                self.where               =[]
                for item in so['meta']['select']['where']:
                    self.where               .append( self._where(c = gv(item,['c']),e1 = gv(item,['e1']),e2 = gv(item,['e2'])) )
            if gv(so,['meta','select','columns']):
                self.columns             =[]
                for item in so['meta']['select']['columns']:
                    self.columns             .append( self._columns(function = gv(item,['function']),column = gv(item,['column']),argument2 = gv(item,['argument2']),argument3 = gv(item,['argument3']),argument1 = gv(item,['argument1']),display = gv(item,['display'])) )
            if gv(so,['meta','select','order by']):
                self.order_by            =[]
                for item in so['meta']['select']['order by']:
                    self.order_by            .append( self._order_by(column = gv(item,['column']),direction = gv(item,['direction'])) )

    def debug(self):
        print('Debug Info: select')
        if self.group_by:
            for item in self.group_by:
                self.item.debug()
        else:
            print('group_by:           '.format(self.group_by))
        if self.source:
            self.source.debug()
        else:
            print('source:             '.format(self.source))
        if self.limit:
            self.limit.debug()
        else:
            print('limit:              '.format(self.limit))
        if self.where:
            for item in self.where:
                self.item.debug()
        else:
            print('where:              '.format(self.where))
        if self.columns:
            for item in self.columns:
                self.item.debug()
        else:
            print('columns:            '.format(self.columns))
        if self.order_by:
            for item in self.order_by:
                self.item.debug()
        else:
            print('order_by:           '.format(self.order_by))


class set:
    __slots__=()

    class _set:
        __slots__=()
        variable             = None
        type                 = None
        value                = None

        def __init__(self,variable=None,type=None,value=None):

        def debug(self):
            print('  Debug Info: set')
            print('  variable:            {0}'.format(self.variable))
            print('  type:                {0}'.format(self.type))
            print('  value:               {0}'.format(self.value))

    set                  = None        # optional [ set() ]

    def __init__(self,so):
            if gv(so,['meta','set','set']):
                self.set                 =[]
                for item in so['meta']['set']['set']:
                    self.set                 .append( self._set(variable = gv(item,['variable']),type = gv(item,['type']),value = gv(item,['value'])) )

    def debug(self):
        print('Debug Info: set')
        if self.set:
            for item in self.set:
                self.item.debug()
        else:
            print('set:                '.format(self.set))


class create_procedure:
    __slots__=()

    class _parameters:
        __slots__=()
        parameter            = None

        def __init__(self,parameter=None):

        def debug(self):
            print('  Debug Info: parameters')
            print('  parameter:           {0}'.format(self.parameter))

    parameters           = None        # optional [ parameters() ]

    def __init__(self,so):
            if gv(so,['meta','create_procedure','parameters']):
                self.parameters          =[]
                for item in so['meta']['create_procedure']['parameters']:
                    self.parameters          .append( self._parameters(parameter = gv(item,['parameter'])) )

    def debug(self):
        print('Debug Info: create_procedure')
        if self.parameters:
            for item in self.parameters:
                self.item.debug()
        else:
            print('parameters:         '.format(self.parameters))


class delimiter:
    __slots__=()

    delimiter            = None

    def __init__(self,so):
            self.delimiter            = gv(so,['meta','delimiter','delimiter'])

    def debug(self):
        print('Debug Info: delimiter')
        print('delimiter:           '.format(self.delimiter))


class end:
    __slots__=()


    def __init__(self,so=None):
          a=1

    def debug(self):
        print('Debug Info: end')
        print('No variables')


class begin:
    __slots__=()


    def __init__(self,so=None):
          a=1

    def debug(self):
        print('Debug Info: begin')
        print('No variables')


class commit:
    __slots__=()


    def __init__(self,so=None):
          a=1

    def debug(self):
        print('Debug Info: commit')
        print('No variables')


class rollback:
    __slots__=()


    def __init__(self,so=None):
          a=1

    def debug(self):
        print('Debug Info: rollback')
        print('No variables')


class show_output_modules:
    __slots__=()


    def __init__(self,so=None):
          a=1

    def debug(self):
        print('Debug Info: show_output_modules')
        print('No variables')


class delete:
    __slots__=()

    class _and:
        __slots__=()
        c                    = None
        e1                   = None
        e2                   = None

        def __init__(self,c=None,e1=None,e2=None):

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

        def debug(self):
            print('  Debug Info: source')
            print('  table:               {0}'.format(self.table))
            print('  database:            {0}'.format(self.database))

    class _where:
        __slots__=()
        c                    = None
        e1                   = None
        e2                   = None

        def __init__(self,c=None,e1=None,e2=None):

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

        def debug(self):
            print('  Debug Info: or')
            print('  c:                   {0}'.format(self.c))
            print('  e1:                  {0}'.format(self.e1))
            print('  e2:                  {0}'.format(self.e2))

    source               = _source()
    where                = None        # optional [ where() ]

    def __init__(self,so):
            if gv(so,['meta','delete','source']):
                self.source              = self._source(table = gv(so,['meta','source','table']),database = gv(so,['meta','source','database']))
            if gv(so,['meta','delete','where']):
                self.where               =[]
                for item in so['meta']['delete']['where']:
                    self.where               .append( self._where(c = gv(item,['c']),e1 = gv(item,['e1']),e2 = gv(item,['e2'])) )

    def debug(self):
        print('Debug Info: delete')
        if self.source:
            self.source.debug()
        else:
            print('source:             '.format(self.source))
        if self.where:
            for item in self.where:
                self.item.debug()
        else:
            print('where:              '.format(self.where))


class insert:
    __slots__=()

    class _source:
        __slots__=()
        table                = None
        database             = None

        def __init__(self,table=None,database=None):

        def debug(self):
            print('  Debug Info: source')
            print('  table:               {0}'.format(self.table))
            print('  database:            {0}'.format(self.database))

    class _values:
        __slots__=()
        value                = None

        def __init__(self,value=None):

        def debug(self):
            print('  Debug Info: values')
            print('  value:               {0}'.format(self.value))

    class _columns:
        __slots__=()
        column               = None

        def __init__(self,column=None):

        def debug(self):
            print('  Debug Info: columns')
            print('  column:              {0}'.format(self.column))

    source               = _source()
    values               = []          #          values()
    columns              = []          #          columns()

    def __init__(self,so):
            if gv(so,['meta','insert','source']):
                self.source              = self._source(table = gv(so,['meta','source','table']),database = gv(so,['meta','source','database']))
            if gv(so,['meta','insert','values']):
                self.values              =[]
                for item in so['meta']['insert']['values']:
                    self.values              .append( self._values(value = gv(item,['value'])) )
            if gv(so,['meta','insert','columns']):
                self.columns             =[]
                for item in so['meta']['insert']['columns']:
                    self.columns             .append( self._columns(column = gv(item,['column'])) )

    def debug(self):
        print('Debug Info: insert')
        if self.source:
            self.source.debug()
        else:
            print('source:             '.format(self.source))
        if self.values:
            for item in self.values:
                self.item.debug()
        else:
            print('values:             '.format(self.values))
        if self.columns:
            for item in self.columns:
                self.item.debug()
        else:
            print('columns:            '.format(self.columns))


class update:
    __slots__=()

    class _and:
        __slots__=()
        c                    = None
        e1                   = None
        e2                   = None

        def __init__(self,c=None,e1=None,e2=None):

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

        def debug(self):
            print('  Debug Info: source')
            print('  table:               {0}'.format(self.table))
            print('  database:            {0}'.format(self.database))

    class _set:
        __slots__=()
        column               = None
        expression           = None

        def __init__(self,column=None,expression=None):

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

        def debug(self):
            print('  Debug Info: or')
            print('  c:                   {0}'.format(self.c))
            print('  e1:                  {0}'.format(self.e1))
            print('  e2:                  {0}'.format(self.e2))

    source               = _source()
    set                  = []          #          set()
    where                = None        # optional [ where() ]

    def __init__(self,so):
            if gv(so,['meta','update','source']):
                self.source              = self._source(table = gv(so,['meta','source','table']),database = gv(so,['meta','source','database']))
            if gv(so,['meta','update','set']):
                self.set                 =[]
                for item in so['meta']['update']['set']:
                    self.set                 .append( self._set(column = gv(item,['column']),expression = gv(item,['expression'])) )
            if gv(so,['meta','update','where']):
                self.where               =[]
                for item in so['meta']['update']['where']:
                    self.where               .append( self._where(c = gv(item,['c']),e1 = gv(item,['e1']),e2 = gv(item,['e2'])) )

    def debug(self):
        print('Debug Info: update')
        if self.source:
            self.source.debug()
        else:
            print('source:             '.format(self.source))
        if self.set:
            for item in self.set:
                self.item.debug()
        else:
            print('set:                '.format(self.set))
        if self.where:
            for item in self.where:
                self.item.debug()
        else:
            print('where:              '.format(self.where))


class upsert:
    __slots__=()

    class _source:
        __slots__=()
        table                = None
        database             = None

        def __init__(self,table=None,database=None):

        def debug(self):
            print('  Debug Info: source')
            print('  table:               {0}'.format(self.table))
            print('  database:            {0}'.format(self.database))

    class _values:
        __slots__=()
        value                = None

        def __init__(self,value=None):

        def debug(self):
            print('  Debug Info: values')
            print('  value:               {0}'.format(self.value))

    class _update:
        __slots__=()
        column               = None
        expression           = None

        def __init__(self,column=None,expression=None):

        def debug(self):
            print('  Debug Info: update')
            print('  column:              {0}'.format(self.column))
            print('  expression:          {0}'.format(self.expression))

    class _columns:
        __slots__=()
        column               = None

        def __init__(self,column=None):

        def debug(self):
            print('  Debug Info: columns')
            print('  column:              {0}'.format(self.column))

    class _on_duplicate_key:
        __slots__=()
        column               = None

        def __init__(self,column=None):

        def debug(self):
            print('  Debug Info: on_duplicate_key')
            print('  column:              {0}'.format(self.column))

    source               = _source()
    values               = []          #          values()
    update               = []          #          update()
    columns              = []          #          columns()
    on_duplicate_key     = []          #          on duplicate key()

    def __init__(self,so):
            if gv(so,['meta','upsert','source']):
                self.source              = self._source(table = gv(so,['meta','source','table']),database = gv(so,['meta','source','database']))
            if gv(so,['meta','upsert','values']):
                self.values              =[]
                for item in so['meta']['upsert']['values']:
                    self.values              .append( self._values(value = gv(item,['value'])) )
            if gv(so,['meta','upsert','update']):
                self.update              =[]
                for item in so['meta']['upsert']['update']:
                    self.update              .append( self._update(column = gv(item,['column']),expression = gv(item,['expression'])) )
            if gv(so,['meta','upsert','columns']):
                self.columns             =[]
                for item in so['meta']['upsert']['columns']:
                    self.columns             .append( self._columns(column = gv(item,['column'])) )
            if gv(so,['meta','upsert','on duplicate key']):
                self.on_duplicate_key    =[]
                for item in so['meta']['upsert']['on duplicate key']:
                    self.on_duplicate_key    .append( self._on_duplicate_key(column = gv(item,['column'])) )

    def debug(self):
        print('Debug Info: upsert')
        if self.source:
            self.source.debug()
        else:
            print('source:             '.format(self.source))
        if self.values:
            for item in self.values:
                self.item.debug()
        else:
            print('values:             '.format(self.values))
        if self.update:
            for item in self.update:
                self.item.debug()
        else:
            print('update:             '.format(self.update))
        if self.columns:
            for item in self.columns:
                self.item.debug()
        else:
            print('columns:            '.format(self.columns))
        if self.on_duplicate_key:
            for item in self.on_duplicate_key:
                self.item.debug()
        else:
            print('on_duplicate_key:   '.format(self.on_duplicate_key))


class use_table:
    __slots__=()

    class _source:
        __slots__=()
        table                = None
        database             = None

        def __init__(self,table=None,database=None):

        def debug(self):
            print('  Debug Info: source')
            print('  table:               {0}'.format(self.table))
            print('  database:            {0}'.format(self.database))

    source               = _source()

    def __init__(self,so):
            if gv(so,['meta','use_table','source']):
                self.source              = self._source(table = gv(so,['meta','source','table']),database = gv(so,['meta','source','database']))

    def debug(self):
        print('Debug Info: use_table')
        if self.source:
            self.source.debug()
        else:
            print('source:             '.format(self.source))


class drop_table:
    __slots__=()

    class _source:
        __slots__=()
        table                = None
        database             = None

        def __init__(self,table=None,database=None):

        def debug(self):
            print('  Debug Info: source')
            print('  table:               {0}'.format(self.table))
            print('  database:            {0}'.format(self.database))

    source               = _source()

    def __init__(self,so):
            if gv(so,['meta','drop_table','source']):
                self.source              = self._source(table = gv(so,['meta','source','table']),database = gv(so,['meta','source','database']))

    def debug(self):
        print('Debug Info: drop_table')
        if self.source:
            self.source.debug()
        else:
            print('source:             '.format(self.source))


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
            if gv(so,['meta','create_table','repo']):
                self.repo                = self._repo(protocol = gv(so,['meta','protocol']),url = gv(so,['meta','url']),user = gv(so,['meta','user']),file = gv(so,['meta','file']),directory = gv(so,['meta','directory']),password = gv(so,['meta','password']))
            if gv(so,['meta','create_table','source']):
                self.source              = self._source(table = gv(so,['meta','table']),database = gv(so,['meta','database']))
            self.delimiter            = gv(so,['meta','delimiter'])
            self.mode                 = gv(so,['meta','mode'])
            self.file                 = gv(so,['meta','file'])
            if gv(so,['meta','create_table','columns']):
                self.columns             =[]
                for item in so['meta']['create_table']['columns']:
                    self.columns             .append( self._columns(column = gv(item,['column'])) )
            self.comments             = gv(so,['meta','comments'])

    def debug(self):
        print('Debug Info: create_table')
        print('errors:              '.format(self.errors))
        print('whitespace:          '.format(self.whitespace))
        print('strict:              '.format(self.strict))
        print('data_starts_on:      '.format(self.data_starts_on))
        print('fifo:                '.format(self.fifo))
        if self.repo:
            self.repo.debug()
        else:
            print('repo:               '.format(self.repo))
        if self.source:
            self.source.debug()
        else:
            print('source:             '.format(self.source))
        print('delimiter:           '.format(self.delimiter))
        print('mode:                '.format(self.mode))
        print('file:                '.format(self.file))
        if self.columns:
            for item in self.columns:
                self.item.debug()
        else:
            print('columns:            '.format(self.columns))
        print('comments:            '.format(self.comments))


class update_table:
    __slots__=()

    class _source:
        __slots__=()
        table                = None
        database             = None

        def __init__(self,table=None,database=None):

        def debug(self):
            print('  Debug Info: source')
            print('  table:               {0}'.format(self.table))
            print('  database:            {0}'.format(self.database))

    class _columns:
        __slots__=()
        column               = None

        def __init__(self,column=None):

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
            if gv(so,['meta','update_table','source']):
                self.source              = self._source(table = gv(so,['meta','source','table']),database = gv(so,['meta','source','database']))
            self.field                = gv(so,['meta','delimiter','field'])
            self.file                 = gv(so,['meta','file','file'])
            if gv(so,['meta','update_table','columns']):
                self.columns             =[]
                for item in so['meta']['update_table']['columns']:
                    self.columns             .append( self._columns(column = gv(item,['column'])) )

    def debug(self):
        print('Debug Info: update_table')
        print('errors:              '.format(self.errors))
        print('whitespace:          '.format(self.whitespace))
        print('data_starts_on:      '.format(self.data_starts_on))
        print('comments:            '.format(self.comments))
        if self.source:
            self.source.debug()
        else:
            print('source:             '.format(self.source))
        print('field:               '.format(self.field))
        print('file:                '.format(self.file))
        if self.columns:
            for item in self.columns:
                self.item.debug()
        else:
            print('columns:            '.format(self.columns))


class describe_table:
    __slots__=()

    class _source:
        __slots__=()
        table                = None
        database             = None

        def __init__(self,table=None,database=None):

        def debug(self):
            print('  Debug Info: source')
            print('  table:               {0}'.format(self.table))
            print('  database:            {0}'.format(self.database))

    source               = _source()

    def __init__(self,so):
            if gv(so,['meta','describe_table','source']):
                self.source              = self._source(table = gv(so,['meta','source','table']),database = gv(so,['meta','source','database']))

    def debug(self):
        print('Debug Info: describe_table')
        if self.source:
            self.source.debug()
        else:
            print('source:             '.format(self.source))



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


