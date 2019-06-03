# This is an auto generated assembly 
# dont edit this, edit the template generator, in tools 

class show_columns:
    __slots__=()
    class _source:
        __slots__=()
        table = None
        database = None
        def __init__(self,table=None,database=None):
            if table:
                self.table=table
            if database:
                self.database=database

    source               = _source()

    def __init__(self,so):
            if gv(so,['meta','show_columns','source']):
                self.source              = self._source(table = gv(so,['meta','source','table']),database = gv(so,['meta','source','database']))

    def debug(self):
        print('Debug Info: show_columns')
        print('table:               '.format(self.table))
        print('database:            '.format(self.database))


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
    class _group_by:
        __slots__=()
        column = None
        def __init__(self,column=None):
            if column:
                self.column=column
    class _source:
        __slots__=()
        table = None
        display = None
        database = None
        def __init__(self,table=None,display=None,database=None):
            if table:
                self.table=table
            if display:
                self.display=display
            if database:
                self.database=database
    class _limit:
        __slots__=()
        start = 0
        length = 0
        def __init__(self,start=None,length=None):
            if start:
                self.start=start
            if length:
                self.length=length
    class _columns:
        __slots__=()
        function = None
        column = None
        argument2 = None
        argument3 = None
        argument1 = None
        display = None
        def __init__(self,function=None,column=None,argument2=None,argument3=None,argument1=None,display=None):
            if function:
                self.function=function
            if column:
                self.column=column
            if argument2:
                self.argument2=argument2
            if argument3:
                self.argument3=argument3
            if argument1:
                self.argument1=argument1
            if display:
                self.display=display
    class _order_by:
        __slots__=()
        column = None
        direction = None
        def __init__(self,column=None,direction=None):
            if column:
                self.column=column
            if direction:
                self.direction=direction

    group_by             = None        # optional [ group by() ]
    source               = None        # optional source()
    limit                = None        # optional limit()
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
        print('column:              '.format(self.column))
        print('table:               '.format(self.table))
        print('display:             '.format(self.display))
        print('database:            '.format(self.database))
        print('start:               '.format(self.start))
        print('length:              '.format(self.length))
        print('function:            '.format(self.function))
        print('column:              '.format(self.column))
        print('argument2:           '.format(self.argument2))
        print('argument3:           '.format(self.argument3))
        print('argument1:           '.format(self.argument1))
        print('display:             '.format(self.display))
        print('column:              '.format(self.column))
        print('direction:           '.format(self.direction))


class set:
    __slots__=()
    class _set:
        __slots__=()
        variable = None
        type = None
        value = None
        def __init__(self,variable=None,type=None,value=None):
            if variable:
                self.variable=variable
            if type:
                self.type=type
            if value:
                self.value=value

    set                  = None        # optional [ set() ]

    def __init__(self,so):
            if gv(so,['meta','set','set']):
                self.set                 =[]
                for item in so['meta']['set']['set']:
                    self.set                 .append( self._set(variable = gv(item,['variable']),type = gv(item,['type']),value = gv(item,['value'])) )

    def debug(self):
        print('Debug Info: set')
        print('variable:            '.format(self.variable))
        print('type:                '.format(self.type))
        print('value:               '.format(self.value))


class create_procedure:
    __slots__=()
    class _parameters:
        __slots__=()
        parameter = None
        def __init__(self,parameter=None):
            if parameter:
                self.parameter=parameter

    parameters           = None        # optional [ parameters() ]

    def __init__(self,so):
            if gv(so,['meta','create_procedure','parameters']):
                self.parameters          =[]
                for item in so['meta']['create_procedure']['parameters']:
                    self.parameters          .append( self._parameters(parameter = gv(item,['parameter'])) )

    def debug(self):
        print('Debug Info: create_procedure')
        print('parameter:           '.format(self.parameter))


class delimiter:
    __slots__=()

    delimiter            = None

    def __init__(self,so):
            self.delimiter            = gv(so,['meta','delimiter','delimiter'])

    def debug(self):
        print('Debug Info: delimiter')
        self.delimiter.debug()


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
        c = None
        e1 = None
        e2 = None
        def __init__(self,c=None,e1=None,e2=None):
            if c:
                self.c=c
            if e1:
                self.e1=e1
            if e2:
                self.e2=e2

        def debug(self):
            print('  Debug Info: and')
            print('  c:                   '.format(self.c))
            print('  e1:                  '.format(self.e1))
            print('  e2:                  '.format(self.e2))
    class _source:
        __slots__=()
        table = None
        database = None
        def __init__(self,table=None,database=None):
            if table:
                self.table=table
            if database:
                self.database=database
    class _where:
        __slots__=()
        c = None
        e1 = None
        e2 = None
        def __init__(self,c=None,e1=None,e2=None):
            if c:
                self.c=c
            if e1:
                self.e1=e1
            if e2:
                self.e2=e2
    class _or:
        __slots__=()
        c = None
        e1 = None
        e2 = None
        def __init__(self,c=None,e1=None,e2=None):
            if c:
                self.c=c
            if e1:
                self.e1=e1
            if e2:
                self.e2=e2

        def debug(self):
            print('  Debug Info: or')
            print('  c:                   '.format(self.c))
            print('  e1:                  '.format(self.e1))
            print('  e2:                  '.format(self.e2))

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
        print('table:               '.format(self.table))
        print('database:            '.format(self.database))
        print('c:                   '.format(self.c))
        print('e1:                  '.format(self.e1))
        print('e2:                  '.format(self.e2))


class insert:
    __slots__=()
    class _source:
        __slots__=()
        table = None
        database = None
        def __init__(self,table=None,database=None):
            if table:
                self.table=table
            if database:
                self.database=database
    class _values:
        __slots__=()
        value = None
        def __init__(self,value=None):
            if value:
                self.value=value
    class _columns:
        __slots__=()
        column = None
        def __init__(self,column=None):
            if column:
                self.column=column

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
        print('table:               '.format(self.table))
        print('database:            '.format(self.database))
        print('value:               '.format(self.value))
        print('column:              '.format(self.column))


class update:
    __slots__=()
    class _and:
        __slots__=()
        c = None
        e1 = None
        e2 = None
        def __init__(self,c=None,e1=None,e2=None):
            if c:
                self.c=c
            if e1:
                self.e1=e1
            if e2:
                self.e2=e2

        def debug(self):
            print('  Debug Info: and')
            print('  c:                   '.format(self.c))
            print('  e1:                  '.format(self.e1))
            print('  e2:                  '.format(self.e2))
    class _source:
        __slots__=()
        table = None
        database = None
        def __init__(self,table=None,database=None):
            if table:
                self.table=table
            if database:
                self.database=database
    class _set:
        __slots__=()
        column = None
        expression = None
        def __init__(self,column=None,expression=None):
            if column:
                self.column=column
            if expression:
                self.expression=expression
    class _where:
        __slots__=()
        c = None
        e1 = None
        e2 = None
        def __init__(self,c=None,e1=None,e2=None):
            if c:
                self.c=c
            if e1:
                self.e1=e1
            if e2:
                self.e2=e2
    class _or:
        __slots__=()
        c = None
        e1 = None
        e2 = None
        def __init__(self,c=None,e1=None,e2=None):
            if c:
                self.c=c
            if e1:
                self.e1=e1
            if e2:
                self.e2=e2

        def debug(self):
            print('  Debug Info: or')
            print('  c:                   '.format(self.c))
            print('  e1:                  '.format(self.e1))
            print('  e2:                  '.format(self.e2))

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
        print('table:               '.format(self.table))
        print('database:            '.format(self.database))
        print('column:              '.format(self.column))
        print('expression:          '.format(self.expression))
        print('c:                   '.format(self.c))
        print('e1:                  '.format(self.e1))
        print('e2:                  '.format(self.e2))


class upsert:
    __slots__=()
    class _source:
        __slots__=()
        table = None
        database = None
        def __init__(self,table=None,database=None):
            if table:
                self.table=table
            if database:
                self.database=database
    class _values:
        __slots__=()
        value = None
        def __init__(self,value=None):
            if value:
                self.value=value
    class _update:
        __slots__=()
        column = None
        expression = None
        def __init__(self,column=None,expression=None):
            if column:
                self.column=column
            if expression:
                self.expression=expression
    class _columns:
        __slots__=()
        column = None
        def __init__(self,column=None):
            if column:
                self.column=column
    class _on_duplicate_key:
        __slots__=()
        column = None
        def __init__(self,column=None):
            if column:
                self.column=column

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
        print('table:               '.format(self.table))
        print('database:            '.format(self.database))
        print('value:               '.format(self.value))
        print('column:              '.format(self.column))
        print('expression:          '.format(self.expression))
        print('column:              '.format(self.column))
        print('column:              '.format(self.column))


class use_table:
    __slots__=()
    class _source:
        __slots__=()
        table = None
        database = None
        def __init__(self,table=None,database=None):
            if table:
                self.table=table
            if database:
                self.database=database

    source               = _source()

    def __init__(self,so):
            if gv(so,['meta','use_table','source']):
                self.source              = self._source(table = gv(so,['meta','source','table']),database = gv(so,['meta','source','database']))

    def debug(self):
        print('Debug Info: use_table')
        print('table:               '.format(self.table))
        print('database:            '.format(self.database))


class drop_table:
    __slots__=()
    class _source:
        __slots__=()
        table = None
        database = None
        def __init__(self,table=None,database=None):
            if table:
                self.table=table
            if database:
                self.database=database

    source               = _source()

    def __init__(self,so):
            if gv(so,['meta','drop_table','source']):
                self.source              = self._source(table = gv(so,['meta','source','table']),database = gv(so,['meta','source','database']))

    def debug(self):
        print('Debug Info: drop_table')
        print('table:               '.format(self.table))
        print('database:            '.format(self.database))


class create_table:
    __slots__=()
    class _repo:
        __slots__=()
        protocol = 'svn'
        url = None
        user = None
        file = None
        directory = None
        password = None
        def __init__(self,protocol=None,url=None,user=None,file=None,directory=None,password=None):
            if protocol:
                self.protocol=protocol
            if url:
                self.url=url
            if user:
                self.user=user
            if file:
                self.file=file
            if directory:
                self.directory=directory
            if password:
                self.password=password
    class _source:
        __slots__=()
        table = None
        database = None
        def __init__(self,table=None,database=None):
            if table:
                self.table=table
            if database:
                self.database=database
    class _columns:
        __slots__=()
        column = None
        def __init__(self,column=None):
            if column:
                self.column=column

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
            self.errors               = gv(so,['meta','errors','errors'])
            self.whitespace           = gv(so,['meta','whitespace','whitespace'])
            self.strict               = gv(so,['meta','strict','strict'])
            self.data_starts_on       = gv(so,['meta','data_starts_on','data_starts_on'])
            self.fifo                 = gv(so,['meta','fifo','fifo'])
            if gv(so,['meta','create_table','repo']):
                self.repo                = self._repo(protocol = gv(so,['meta','repo','protocol']),url = gv(so,['meta','repo','url']),user = gv(so,['meta','repo','user']),file = gv(so,['meta','repo','file']),directory = gv(so,['meta','repo','directory']),password = gv(so,['meta','repo','password']))
            if gv(so,['meta','create_table','source']):
                self.source              = self._source(table = gv(so,['meta','source','table']),database = gv(so,['meta','source','database']))
            self.delimiter            = gv(so,['meta','delimiter','delimiter'])
            self.mode                 = gv(so,['meta','mode','mode'])
            self.file                 = gv(so,['meta','file','file'])
            if gv(so,['meta','create_table','columns']):
                self.columns             =[]
                for item in so['meta']['create_table']['columns']:
                    self.columns             .append( self._columns(column = gv(item,['column'])) )
            self.comments             = gv(so,['meta','comments','comments'])

    def debug(self):
        print('Debug Info: create_table')
        self.errors.debug()
        self.whitespace.debug()
        self.strict.debug()
        self.data_starts_on.debug()
        self.fifo.debug()
        print('protocol:            '.format(self.protocol))
        print('url:                 '.format(self.url))
        print('user:                '.format(self.user))
        print('file:                '.format(self.file))
        print('directory:           '.format(self.directory))
        print('password:            '.format(self.password))
        print('table:               '.format(self.table))
        print('database:            '.format(self.database))
        self.delimiter.debug()
        self.mode.debug()
        self.file.debug()
        print('column:              '.format(self.column))
        self.comments.debug()


class update_table:
    __slots__=()
    class _source:
        __slots__=()
        table = None
        database = None
        def __init__(self,table=None,database=None):
            if table:
                self.table=table
            if database:
                self.database=database
    class _columns:
        __slots__=()
        column = None
        def __init__(self,column=None):
            if column:
                self.column=column

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
        self.errors.debug()
        self.whitespace.debug()
        self.data_starts_on.debug()
        self.comments.debug()
        print('table:               '.format(self.table))
        print('database:            '.format(self.database))
        self.delimiter.debug()
        self.file.debug()
        print('column:              '.format(self.column))


class describe_table:
    __slots__=()
    class _source:
        __slots__=()
        table = None
        database = None
        def __init__(self,table=None,database=None):
            if table:
                self.table=table
            if database:
                self.database=database

    source               = _source()

    def __init__(self,so):
            if gv(so,['meta','describe_table','source']):
                self.source              = self._source(table = gv(so,['meta','source','table']),database = gv(so,['meta','source','database']))

    def debug(self):
        print('Debug Info: describe_table')
        print('table:               '.format(self.table))
        print('database:            '.format(self.database))




def get_meta(o):

    if o['mode']=='show columns':
        return show_columns(o)
    elif o['mode']=='show tables':
        return show_tables(o)
    elif o['mode']=='show variables':
        return show_variables(o)
    elif o['mode']=='select':
        return select(o)
    elif o['mode']=='set':
        return set(o)
    elif o['mode']=='create procedure':
        return create_procedure(o)
    elif o['mode']=='delimiter':
        return delimiter(o)
    elif o['mode']=='end':
        return end(o)
    elif o['mode']=='begin':
        return begin(o)
    elif o['mode']=='commit':
        return commit(o)
    elif o['mode']=='rollback':
        return rollback(o)
    elif o['mode']=='show output modules':
        return show_output_modules(o)
    elif o['mode']=='delete':
        return delete(o)
    elif o['mode']=='insert':
        return insert(o)
    elif o['mode']=='update':
        return update(o)
    elif o['mode']=='upsert':
        return upsert(o)
    elif o['mode']=='use table':
        return use_table(o)
    elif o['mode']=='drop table':
        return drop_table(o)
    elif o['mode']=='create table':
        return create_table(o)
    elif o['mode']=='update table':
        return update_table(o)
    elif o['mode']=='describe table':
        return describe_table(o)

    return None


