
class debugger:
    def __init__(self,obj,name,depth=0):
        pad=''
        for i in range(0,depth):
            pad+=' '
        if depth==0:
            print ("\n\033[31;1;4mDebug: {0}\033[0m".format(name))

        variables = [i for i in dir(obj) if not i.startswith('__')]
        empty=[]
        var_count=0
        for var in variables:
            value=getattr(obj,var)
            if  isinstance(value,str):
                print("{2}{0} {1}".format(var+':',value,pad))
                var_count+=1
            elif  isinstance(value,int):
                print("{2}{0} {1}".format(var+':',value,pad))
                var_count+=1
            elif  isinstance(value,float):
                print("{2}{0} {1}".format(var+':',value,pad))
                var_count+=1
            elif isinstance(value,list):
                print ("{0}- {1} :".format(pad,var))
                for item in value:
                    var_count+=1
                    debugger(item,var,depth+4)
            elif callable(value):
                continue
            elif value==None:
                var_count+=1
                empty.append(var)
            else:
                var_count+=1
                print ("{0}- {1} :".format(pad,var))
                debugger(value,var,depth+4)
                
        if len(empty)>0:
            print ("{1}Empty Vars: {0}".format(",".join(empty),pad))
        #print variables
        if var_count==0:
            print("{2}{0} {1}".format("No attributes"+':',"",pad))


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


def safe_name(name):
    forbidden=[ 'False', 'None', 'True', 'and', 'as', 'assert', 'break', 'class', 'continue', 'def', 'del', 'elif', 'else', 'except', 'finally', 'for', 
                'from', 'global', 'if', 'import', 'in', 'is', 'lambda', 'nonlocal', 'not', 'or', 'pass', 'raise', 'return', 'try', 'while', 'with', 'yield'
                'abs','divmod','input','open','staticmethod','all','enumerate','int','ord','str','any','eval','isinstance','pow','sum','basestring','execfile',
                'issubclass','print','super','bin','file','iter','property','tuple','bool','filter','len','range','type','bytearray','float','list','raw_input',
                'unichr','callable','format','locals','reduce','unicode','chr','frozenset','long','reload','vars','classmethod','getattr','map','repr','xrange',
                'cmp','globals','max','reversed','zip','compile','hasattr','memoryview','round','__import__','complex','hash','min','set','delattr','help','next',
                'setattr','dict','hex','object','slice','dir','id','oct','sorted']
    name=name.replace(" ","_")
    if name in forbidden:
        name=name+"_"
    return name


class show_columns:

    class _source:
        __slots__=()
        table = None
        database = None

        def __init__(self,table=None,database=None):
            if table:  self.table=table
            if database:  self.database=database
    #variable_def

    #variable_class_def
    source               = _source()

    def __init__(self,so):
            if gv(so,['meta','source']):
                self.source= self.source(table = gv(so,['meta','source','table']),database = gv(so,['meta','source','database']))
    def debug(self):
        debugger(self,'show columns')


class show_tables:
    #variable_def

    #variable_class_def

    def __init__(self,so):
        a=0 # holder

    def debug(self):
        debugger(self,'show tables')


class show_variables:
    #variable_def

    #variable_class_def

    def __init__(self,so):
        a=0 # holder

    def debug(self):
        debugger(self,'show variables')


class select:

    class _or_:
        __slots__=()
        c = None
        e1 = None
        condition = None
        e2 = None

        def __init__(self,c=None,e1=None,condition=None,e2=None):
            if c:  self.c=c
            if e1:  self.e1=e1
            if condition:  self.condition=condition
            if e2:  self.e2=e2

    class _order_by:
        __slots__=()
        column = None
        direction = None

        def __init__(self,column=None,direction=None):
            if column:  self.column=column
            if direction:  self.direction=direction

    class _source:
        __slots__=()
        table = None
        display = None
        database = None

        def __init__(self,table=None,display=None,database=None):
            if table:  self.table=table
            if display:  self.display=display
            if database:  self.database=database

    class _and_:
        __slots__=()
        c = None
        e1 = None
        condition = None
        e2 = None

        def __init__(self,c=None,e1=None,condition=None,e2=None):
            if c:  self.c=c
            if e1:  self.e1=e1
            if condition:  self.condition=condition
            if e2:  self.e2=e2

    class _group_by:
        __slots__=()
        column = None

        def __init__(self,column=None):
            if column:  self.column=column

    class _limit:
        __slots__=()
        start = 0
        length = 0

        def __init__(self,start=None,length=None):
            if start:  self.start=start
            if length:  self.length=length

    class _where:
        __slots__=()
        c = None
        e1 = None
        condition = None
        e2 = None

        def __init__(self,c=None,e1=None,condition=None,e2=None):
            if c:  self.c=c
            if e1:  self.e1=e1
            if condition:  self.condition=condition
            if e2:  self.e2=e2

    class _columns:
        __slots__=()
        function = None
        column = None
        argument2 = None
        argument3 = None
        argument1 = None
        display = None

        def __init__(self,function=None,column=None,argument2=None,argument3=None,argument1=None,display=None):
            if function:  self.function=function
            if column:  self.column=column
            if argument2:  self.argument2=argument2
            if argument3:  self.argument3=argument3
            if argument1:  self.argument1=argument1
            if display:  self.display=display
    #variable_def

    #variable_class_def
    order_by             = None        # optional [ _order_by() ]
    source               = None        # optional _source()
    group_by             = None        # optional [ _group_by() ]
    limit                = None        # optional _limit()
    where                = None        # optional [ _where() ]
    columns              = []          #          _columns()

    def __init__(self,so):
            if gv(so,['meta','order_by']):
                self.order_by=[]
                for item in gv(so,['meta','order_by']):
                    instance_type=safe_name(item.keys()[0])
                    print(instance_type)
                    self.order_by.append( type('_'+instance_type,(),{ 'column': gv(item,['column']),'direction': gv(item,['direction']) }) )
            if gv(so,['meta','source']):
                self.source= self.source(table = gv(so,['meta','source','table']),display = gv(so,['meta','source','display']),database = gv(so,['meta','source','database']))
            if gv(so,['meta','group_by']):
                self.group_by=[]
                for item in gv(so,['meta','group_by']):
                    instance_type=safe_name(item.keys()[0])
                    print(instance_type)
                    self.group_by.append( type('_'+instance_type,(),{ 'column': gv(item,['column']) }) )
            if gv(so,['meta','limit']):
                self.limit= self.limit(start = gv(so,['meta','limit','start']),length = gv(so,['meta','limit','length']))
            if gv(so,['meta','where']):
                self.where=[]
                for item in gv(so,['meta','where']):
                    instance_type=safe_name(item.keys()[0])
                    print(instance_type)
                    self.where.append( type('_'+instance_type,(),{ 'c': gv(item,[instance_type,'c']),'e1': gv(item,[instance_type,'e1']),'condition': gv(item,[instance_type,'condition']),'e2': gv(item,[instance_type,'e2']) }) )
            if gv(so,['meta','columns']):
                self.columns=[]
                for item in gv(so,['meta','columns']):
                    instance_type=safe_name(item.keys()[0])
                    print(instance_type)
                    self.columns.append( type('_'+instance_type,(),{ 'function': gv(item,['function']),'column': gv(item,['column']),'argument2': gv(item,['argument2']),'argument3': gv(item,['argument3']),'argument1': gv(item,['argument1']),'display': gv(item,['display']) }) )
    def debug(self):
        debugger(self,'select')


class set_:

    class _set_:
        __slots__=()
        variable = None
        value = None

        def __init__(self,variable=None,value=None):
            if variable:  self.variable=variable
            if value:  self.value=value
    #variable_def

    #variable_class_def
    set_                 = None        # optional [ _set_() ]

    def __init__(self,so):
            if gv(so,['meta','set_']):
                self.set_=[]
                for item in gv(so,['meta','set_']):
                    instance_type=safe_name(item.keys()[0])
                    print(instance_type)
                    self.set_.append( type('_'+instance_type,(),{ 'variable': gv(item,['variable']),'value': gv(item,['value']) }) )
    def debug(self):
        debugger(self,'set')


class create_procedure:

    class _parameters:
        __slots__=()
        parameter = None

        def __init__(self,parameter=None):
            if parameter:  self.parameter=parameter
    #variable_def

    #variable_class_def
    parameters           = None        # optional [ _parameters() ]

    def __init__(self,so):
            if gv(so,['meta','parameters']):
                self.parameters=[]
                for item in gv(so,['meta','parameters']):
                    instance_type=safe_name(item.keys()[0])
                    print(instance_type)
                    self.parameters.append( type('_'+instance_type,(),{ 'parameter': gv(item,['parameter']) }) )
    def debug(self):
        debugger(self,'create procedure')


class delimiter:
    #variable_def

    #variable_class_def
    delimiter            = None

    def __init__(self,so):
            self.delimiter = gv(so,['meta','delimiter','delimiter'])
    def debug(self):
        debugger(self,'delimiter')


class end:
    #variable_def

    #variable_class_def

    def __init__(self,so):
        a=0 # holder

    def debug(self):
        debugger(self,'end')


class begin:
    #variable_def

    #variable_class_def

    def __init__(self,so):
        a=0 # holder

    def debug(self):
        debugger(self,'begin')


class commit:
    #variable_def

    #variable_class_def

    def __init__(self,so):
        a=0 # holder

    def debug(self):
        debugger(self,'commit')


class rollback:
    #variable_def

    #variable_class_def

    def __init__(self,so):
        a=0 # holder

    def debug(self):
        debugger(self,'rollback')


class show_output_modules:
    #variable_def

    #variable_class_def

    def __init__(self,so):
        a=0 # holder

    def debug(self):
        debugger(self,'show output modules')


class delete:

    class _source:
        __slots__=()
        table = None
        database = None

        def __init__(self,table=None,database=None):
            if table:  self.table=table
            if database:  self.database=database

    class _and_:
        __slots__=()
        c = None
        e1 = None
        condition = None
        e2 = None

        def __init__(self,c=None,e1=None,condition=None,e2=None):
            if c:  self.c=c
            if e1:  self.e1=e1
            if condition:  self.condition=condition
            if e2:  self.e2=e2

    class _where:
        __slots__=()
        c = None
        e1 = None
        condition = None
        e2 = None

        def __init__(self,c=None,e1=None,condition=None,e2=None):
            if c:  self.c=c
            if e1:  self.e1=e1
            if condition:  self.condition=condition
            if e2:  self.e2=e2

    class _or_:
        __slots__=()
        c = None
        e1 = None
        condition = None
        e2 = None

        def __init__(self,c=None,e1=None,condition=None,e2=None):
            if c:  self.c=c
            if e1:  self.e1=e1
            if condition:  self.condition=condition
            if e2:  self.e2=e2
    #variable_def

    #variable_class_def
    source               = _source()
    where                = None        # optional [ _where() ]

    def __init__(self,so):
            if gv(so,['meta','source']):
                self.source= self.source(table = gv(so,['meta','source','table']),database = gv(so,['meta','source','database']))
            if gv(so,['meta','where']):
                self.where=[]
                for item in gv(so,['meta','where']):
                    instance_type=safe_name(item.keys()[0])
                    print(instance_type)
                    self.where.append( type('_'+instance_type,(),{ 'c': gv(item,[instance_type,'c']),'e1': gv(item,[instance_type,'e1']),'condition': gv(item,[instance_type,'condition']),'e2': gv(item,[instance_type,'e2']) }) )
    def debug(self):
        debugger(self,'delete')


class insert:

    class _source:
        __slots__=()
        table = None
        database = None

        def __init__(self,table=None,database=None):
            if table:  self.table=table
            if database:  self.database=database

    class _values:
        __slots__=()
        value = None

        def __init__(self,value=None):
            if value:  self.value=value

    class _columns:
        __slots__=()
        column = None

        def __init__(self,column=None):
            if column:  self.column=column
    #variable_def

    #variable_class_def
    source               = _source()
    values               = []          #          _values()
    columns              = []          #          _columns()

    def __init__(self,so):
            if gv(so,['meta','source']):
                self.source= self.source(table = gv(so,['meta','source','table']),database = gv(so,['meta','source','database']))
            if gv(so,['meta','values']):
                self.values=[]
                for item in gv(so,['meta','values']):
                    instance_type=safe_name(item.keys()[0])
                    print(instance_type)
                    self.values.append( type('_'+instance_type,(),{ 'value': gv(item,['value']) }) )
            if gv(so,['meta','columns']):
                self.columns=[]
                for item in gv(so,['meta','columns']):
                    instance_type=safe_name(item.keys()[0])
                    print(instance_type)
                    self.columns.append( type('_'+instance_type,(),{ 'column': gv(item,['column']) }) )
    def debug(self):
        debugger(self,'insert')


class update:

    class _source:
        __slots__=()
        table = None
        database = None

        def __init__(self,table=None,database=None):
            if table:  self.table=table
            if database:  self.database=database

    class _and_:
        __slots__=()
        c = None
        e1 = None
        condition = None
        e2 = None

        def __init__(self,c=None,e1=None,condition=None,e2=None):
            if c:  self.c=c
            if e1:  self.e1=e1
            if condition:  self.condition=condition
            if e2:  self.e2=e2

    class _set_:
        __slots__=()
        column = None
        expression = None

        def __init__(self,column=None,expression=None):
            if column:  self.column=column
            if expression:  self.expression=expression

    class _where:
        __slots__=()
        c = None
        e1 = None
        condition = None
        e2 = None

        def __init__(self,c=None,e1=None,condition=None,e2=None):
            if c:  self.c=c
            if e1:  self.e1=e1
            if condition:  self.condition=condition
            if e2:  self.e2=e2

    class _or_:
        __slots__=()
        c = None
        e1 = None
        condition = None
        e2 = None

        def __init__(self,c=None,e1=None,condition=None,e2=None):
            if c:  self.c=c
            if e1:  self.e1=e1
            if condition:  self.condition=condition
            if e2:  self.e2=e2
    #variable_def

    #variable_class_def
    source               = _source()
    set_                 = []          #          _set_()
    where                = None        # optional [ _where() ]

    def __init__(self,so):
            if gv(so,['meta','source']):
                self.source= self.source(table = gv(so,['meta','source','table']),database = gv(so,['meta','source','database']))
            if gv(so,['meta','set_']):
                self.set_=[]
                for item in gv(so,['meta','set_']):
                    instance_type=safe_name(item.keys()[0])
                    print(instance_type)
                    self.set_.append( type('_'+instance_type,(),{ 'column': gv(item,['column']),'expression': gv(item,['expression']) }) )
            if gv(so,['meta','where']):
                self.where=[]
                for item in gv(so,['meta','where']):
                    instance_type=safe_name(item.keys()[0])
                    print(instance_type)
                    self.where.append( type('_'+instance_type,(),{ 'c': gv(item,[instance_type,'c']),'e1': gv(item,[instance_type,'e1']),'condition': gv(item,[instance_type,'condition']),'e2': gv(item,[instance_type,'e2']) }) )
    def debug(self):
        debugger(self,'update')


class upsert:

    class _source:
        __slots__=()
        table = None
        database = None

        def __init__(self,table=None,database=None):
            if table:  self.table=table
            if database:  self.database=database

    class _values:
        __slots__=()
        value = None

        def __init__(self,value=None):
            if value:  self.value=value

    class _update:
        __slots__=()
        column = None
        expression = None

        def __init__(self,column=None,expression=None):
            if column:  self.column=column
            if expression:  self.expression=expression

    class _columns:
        __slots__=()
        column = None

        def __init__(self,column=None):
            if column:  self.column=column

    class _on_duplicate_key:
        __slots__=()
        column = None

        def __init__(self,column=None):
            if column:  self.column=column
    #variable_def

    #variable_class_def
    source               = _source()
    values               = []          #          _values()
    update               = []          #          _update()
    columns              = []          #          _columns()
    on_duplicate_key     = []          #          _on_duplicate_key()

    def __init__(self,so):
            if gv(so,['meta','source']):
                self.source= self.source(table = gv(so,['meta','source','table']),database = gv(so,['meta','source','database']))
            if gv(so,['meta','values']):
                self.values=[]
                for item in gv(so,['meta','values']):
                    instance_type=safe_name(item.keys()[0])
                    print(instance_type)
                    self.values.append( type('_'+instance_type,(),{ 'value': gv(item,['value']) }) )
            if gv(so,['meta','update']):
                self.update=[]
                for item in gv(so,['meta','update']):
                    instance_type=safe_name(item.keys()[0])
                    print(instance_type)
                    self.update.append( type('_'+instance_type,(),{ 'column': gv(item,['column']),'expression': gv(item,['expression']) }) )
            if gv(so,['meta','columns']):
                self.columns=[]
                for item in gv(so,['meta','columns']):
                    instance_type=safe_name(item.keys()[0])
                    print(instance_type)
                    self.columns.append( type('_'+instance_type,(),{ 'column': gv(item,['column']) }) )
            if gv(so,['meta','on_duplicate_key']):
                self.on_duplicate_key=[]
                for item in gv(so,['meta','on_duplicate_key']):
                    instance_type=safe_name(item.keys()[0])
                    print(instance_type)
                    self.on_duplicate_key.append( type('_'+instance_type,(),{ 'column': gv(item,['column']) }) )
    def debug(self):
        debugger(self,'upsert')


class use_table:

    class _source:
        __slots__=()
        table = None
        database = None

        def __init__(self,table=None,database=None):
            if table:  self.table=table
            if database:  self.database=database
    #variable_def

    #variable_class_def
    source               = _source()

    def __init__(self,so):
            if gv(so,['meta','source']):
                self.source= self.source(table = gv(so,['meta','source','table']),database = gv(so,['meta','source','database']))
    def debug(self):
        debugger(self,'use table')


class drop_table:

    class _source:
        __slots__=()
        table = None
        database = None

        def __init__(self,table=None,database=None):
            if table:  self.table=table
            if database:  self.database=database
    #variable_def

    #variable_class_def
    source               = _source()

    def __init__(self,so):
            if gv(so,['meta','source']):
                self.source= self.source(table = gv(so,['meta','source','table']),database = gv(so,['meta','source','database']))
    def debug(self):
        debugger(self,'drop table')


class create_table:

    class _repo:
        __slots__=()
        protocol = 'svn'
        url = None
        user = None
        file = None
        directory = None
        password = None

        def __init__(self,protocol=None,url=None,user=None,file=None,directory=None,password=None):
            if protocol:  self.protocol=protocol
            if url:  self.url=url
            if user:  self.user=user
            if file:  self.file=file
            if directory:  self.directory=directory
            if password:  self.password=password

    class _source:
        __slots__=()
        table = None
        database = None

        def __init__(self,table=None,database=None):
            if table:  self.table=table
            if database:  self.database=database

    class _columns:
        __slots__=()
        column = None

        def __init__(self,column=None):
            if column:  self.column=column
    #variable_def

    #variable_class_def
    errors               = None        # optional 
    temporary            = None        # optional 
    whitespace           = None        # optional 
    strict               = None        # optional 
    data_starts_on       = None        # optional 
    file                 = None
    fifo                 = None        # optional 
    repo                 = None        # optional _repo()
    source               = _source()
    delimiter            = None        # optional 
    mode                 = None        # optional 
    columns              = []          #          _columns()
    comments             = None        # optional 

    def __init__(self,so):
            self.errors = gv(so,['meta','errors'])
            self.temporary = gv(so,['meta','temporary','temporary'])
            self.whitespace = gv(so,['meta','whitespace'])
            self.strict = gv(so,['meta','strict'])
            self.data_starts_on = gv(so,['meta','data_starts_on'])
            self.file = gv(so,['meta','file'])
            self.fifo = gv(so,['meta','fifo'])
            if gv(so,['meta','repo']):
                self.repo= self.repo(protocol = gv(so,['meta','repo','protocol']),url = gv(so,['meta','repo','url']),user = gv(so,['meta','repo','user']),file = gv(so,['meta','repo','file']),directory = gv(so,['meta','repo','directory']),password = gv(so,['meta','repo','password']))
            if gv(so,['meta','source']):
                self.source= self.source(table = gv(so,['meta','source','table']),database = gv(so,['meta','source','database']))
            self.delimiter = gv(so,['meta','delimiter'])
            self.mode = gv(so,['meta','mode'])
            if gv(so,['meta','columns']):
                self.columns=[]
                for item in gv(so,['meta','columns']):
                    instance_type=safe_name(item.keys()[0])
                    print(instance_type)
                    self.columns.append( type('_'+instance_type,(),{ 'column': gv(item,['column']) }) )
            self.comments = gv(so,['meta','comments'])
    def debug(self):
        debugger(self,'create table')


class update_table:

    class _source:
        __slots__=()
        table = None
        database = None

        def __init__(self,table=None,database=None):
            if table:  self.table=table
            if database:  self.database=database

    class _columns:
        __slots__=()
        column = None

        def __init__(self,column=None):
            if column:  self.column=column
    #variable_def

    #variable_class_def
    errors               = None        # optional 
    whitespace           = None        # optional 
    data_starts_on       = None        # optional 
    file_                = None        # optional 
    comments             = None        # optional 
    source               = _source()
    delimiter            = None        # optional 
    columns              = None        # optional [ _columns() ]

    def __init__(self,so):
            self.errors = gv(so,['meta','errors','errors'])
            self.whitespace = gv(so,['meta','whitespace','whitespace'])
            self.data_starts_on = gv(so,['meta','data_starts_on','data_starts_on'])
            self.file = gv(so,['meta','file_','file'])
            self.comments = gv(so,['meta','comments','comments'])
            if gv(so,['meta','source']):
                self.source= self.source(table = gv(so,['meta','source','table']),database = gv(so,['meta','source','database']))
            self.field = gv(so,['meta','delimiter','field'])
            if gv(so,['meta','columns']):
                self.columns=[]
                for item in gv(so,['meta','columns']):
                    instance_type=safe_name(item.keys()[0])
                    print(instance_type)
                    self.columns.append( type('_'+instance_type,(),{ 'column': gv(item,['column']) }) )
    def debug(self):
        debugger(self,'update table')


class describe_table:

    class _source:
        __slots__=()
        table = None
        database = None

        def __init__(self,table=None,database=None):
            if table:  self.table=table
            if database:  self.database=database
    #variable_def

    #variable_class_def
    source               = _source()

    def __init__(self,so):
            if gv(so,['meta','source']):
                self.source= self.source(table = gv(so,['meta','source','table']),database = gv(so,['meta','source','database']))
    def debug(self):
        debugger(self,'describe table')



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


