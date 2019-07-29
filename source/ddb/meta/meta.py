
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


class Show_Columns:

    class _Source:
        __slots__=()
        table = None
        database = None

        def __init__(self,table=None,database=None):
            if table:  self.table=table
            if database:  self.database=database
    #variable_def

    #variable_class_def
    Source               = _Source()

    def __init__(self,so):
            if gv(so,['meta','Source']):
                self.Source= self._Source(table = gv(so,['meta','Source','table']),database = gv(so,['meta','Source','database']))
    def debug(self):
        debugger(self,'show columns')


class Show_Tables:
    #variable_def

    #variable_class_def

    def __init__(self,so):
        a=0 # holder

    def debug(self):
        debugger(self,'show tables')


class Show_Variables:
    #variable_def

    #variable_class_def

    def __init__(self,so):
        a=0 # holder

    def debug(self):
        debugger(self,'show variables')


class Select:

    class _And:
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

    class _Order_By:
        __slots__=()
        column = None
        direction = None

        def __init__(self,column=None,direction=None):
            if column:  self.column=column
            if direction:  self.direction=direction

    class _Source:
        __slots__=()
        table = None
        display = None
        database = None

        def __init__(self,table=None,display=None,database=None):
            if table:  self.table=table
            if display:  self.display=display
            if database:  self.database=database

    class _Group_By:
        __slots__=()
        column = None

        def __init__(self,column=None):
            if column:  self.column=column

    class _Limit:
        __slots__=()
        start = 0
        length = 0

        def __init__(self,start=None,length=None):
            if start:  self.start=start
            if length:  self.length=length

    class _Where:
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

    class _Or:
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

    class _Columns:
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
    Order_By             = None        # optional [ _Order_By() ]
    Source               = None        # optional _Source()
    Group_By             = None        # optional [ _Group_By() ]
    Limit                = None        # optional _Limit()
    Where                = None        # optional [ _Where() ]
    Columns              = []          #          _Columns()

    def __init__(self,so):
            if gv(so,['meta','Order_By']):
                self.Order_By=[]
                for item in gv(so,['meta','Order_By']):
                    instance_type=item.keys()[0]
                    safe_instance_type=safe_name(instance_type)
                    self.Order_By.append( type('_'+safe_instance_type,(),{ 'column': gv(item,['column']),'direction': gv(item,['direction']) }) )
            if gv(so,['meta','Source']):
                self.Source= self._Source(table = gv(so,['meta','Source','table']),display = gv(so,['meta','Source','display']),database = gv(so,['meta','Source','database']))
            if gv(so,['meta','Group_By']):
                self.Group_By=[]
                for item in gv(so,['meta','Group_By']):
                    instance_type=item.keys()[0]
                    safe_instance_type=safe_name(instance_type)
                    self.Group_By.append( type('_'+safe_instance_type,(),{ 'column': gv(item,['column']) }) )
            if gv(so,['meta','Limit']):
                self.Limit= self._Limit(start = gv(so,['meta','Limit','start']),length = gv(so,['meta','Limit','length']))
            if gv(so,['meta','Where']):
                self.Where=[]
                for item in gv(so,['meta','Where']):
                    instance_type=item.keys()[0]
                    safe_instance_type=safe_name(instance_type)
                    self.Where.append( type('_'+safe_instance_type,(),{ 'c': gv(item,[instance_type,'c']),'e1': gv(item,[instance_type,'e1']),'condition': gv(item,[instance_type,'condition']),'e2': gv(item,[instance_type,'e2']) }) )
            if gv(so,['meta','Columns']):
                self.Columns=[]
                for item in gv(so,['meta','Columns']):
                    instance_type=item.keys()[0]
                    safe_instance_type=safe_name(instance_type)
                    self.Columns.append( type('_'+safe_instance_type,(),{ 'function': gv(item,['function']),'column': gv(item,['column']),'argument2': gv(item,['argument2']),'argument3': gv(item,['argument3']),'argument1': gv(item,['argument1']),'display': gv(item,['display']) }) )
    def debug(self):
        debugger(self,'select')


class Set:

    class _Set:
        __slots__=()
        variable = None
        value = None

        def __init__(self,variable=None,value=None):
            if variable:  self.variable=variable
            if value:  self.value=value
    #variable_def

    #variable_class_def
    Set                  = None        # optional [ _Set() ]

    def __init__(self,so):
            if gv(so,['meta','Set']):
                self.Set=[]
                for item in gv(so,['meta','Set']):
                    instance_type=item.keys()[0]
                    safe_instance_type=safe_name(instance_type)
                    self.Set.append( type('_'+safe_instance_type,(),{ 'variable': gv(item,['variable']),'value': gv(item,['value']) }) )
    def debug(self):
        debugger(self,'set')


class Create_Procedure:

    class _Parameters:
        __slots__=()
        parameter = None

        def __init__(self,parameter=None):
            if parameter:  self.parameter=parameter
    #variable_def

    #variable_class_def
    Parameters           = None        # optional [ _Parameters() ]

    def __init__(self,so):
            if gv(so,['meta','Parameters']):
                self.Parameters=[]
                for item in gv(so,['meta','Parameters']):
                    instance_type=item.keys()[0]
                    safe_instance_type=safe_name(instance_type)
                    self.Parameters.append( type('_'+safe_instance_type,(),{ 'parameter': gv(item,['parameter']) }) )
    def debug(self):
        debugger(self,'create procedure')


class Delimiter:
    #variable_def

    #variable_class_def
    delimiter            = None

    def __init__(self,so):
            self.delimiter = gv(so,['meta','Delimiter','delimiter'])
    def debug(self):
        debugger(self,'delimiter')


class End:
    #variable_def

    #variable_class_def

    def __init__(self,so):
        a=0 # holder

    def debug(self):
        debugger(self,'end')


class Begin:
    #variable_def

    #variable_class_def

    def __init__(self,so):
        a=0 # holder

    def debug(self):
        debugger(self,'begin')


class Commit:
    #variable_def

    #variable_class_def

    def __init__(self,so):
        a=0 # holder

    def debug(self):
        debugger(self,'commit')


class Rollback:
    #variable_def

    #variable_class_def

    def __init__(self,so):
        a=0 # holder

    def debug(self):
        debugger(self,'rollback')


class Show_Output_Modules:
    #variable_def

    #variable_class_def

    def __init__(self,so):
        a=0 # holder

    def debug(self):
        debugger(self,'show output modules')


class Delete:

    class _And:
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

    class _Source:
        __slots__=()
        table = None
        database = None

        def __init__(self,table=None,database=None):
            if table:  self.table=table
            if database:  self.database=database

    class _Where:
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

    class _Or:
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
    Source               = _Source()
    Where                = None        # optional [ _Where() ]

    def __init__(self,so):
            if gv(so,['meta','Source']):
                self.Source= self._Source(table = gv(so,['meta','Source','table']),database = gv(so,['meta','Source','database']))
            if gv(so,['meta','Where']):
                self.Where=[]
                for item in gv(so,['meta','Where']):
                    instance_type=item.keys()[0]
                    safe_instance_type=safe_name(instance_type)
                    self.Where.append( type('_'+safe_instance_type,(),{ 'c': gv(item,[instance_type,'c']),'e1': gv(item,[instance_type,'e1']),'condition': gv(item,[instance_type,'condition']),'e2': gv(item,[instance_type,'e2']) }) )
    def debug(self):
        debugger(self,'delete')


class Insert:

    class _Source:
        __slots__=()
        table = None
        database = None

        def __init__(self,table=None,database=None):
            if table:  self.table=table
            if database:  self.database=database

    class _Values:
        __slots__=()
        value = None

        def __init__(self,value=None):
            if value:  self.value=value

    class _Columns:
        __slots__=()
        column = None

        def __init__(self,column=None):
            if column:  self.column=column
    #variable_def

    #variable_class_def
    Source               = _Source()
    Values               = []          #          _Values()
    Columns              = []          #          _Columns()

    def __init__(self,so):
            if gv(so,['meta','Source']):
                self.Source= self._Source(table = gv(so,['meta','Source','table']),database = gv(so,['meta','Source','database']))
            if gv(so,['meta','Values']):
                self.Values=[]
                for item in gv(so,['meta','Values']):
                    instance_type=item.keys()[0]
                    safe_instance_type=safe_name(instance_type)
                    self.Values.append( type('_'+safe_instance_type,(),{ 'value': gv(item,['value']) }) )
            if gv(so,['meta','Columns']):
                self.Columns=[]
                for item in gv(so,['meta','Columns']):
                    instance_type=item.keys()[0]
                    safe_instance_type=safe_name(instance_type)
                    self.Columns.append( type('_'+safe_instance_type,(),{ 'column': gv(item,['column']) }) )
    def debug(self):
        debugger(self,'insert')


class Update:

    class _And:
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

    class _Source:
        __slots__=()
        table = None
        database = None

        def __init__(self,table=None,database=None):
            if table:  self.table=table
            if database:  self.database=database

    class _Set:
        __slots__=()
        column = None
        expression = None

        def __init__(self,column=None,expression=None):
            if column:  self.column=column
            if expression:  self.expression=expression

    class _Where:
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

    class _Or:
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
    Source               = _Source()
    Set                  = []          #          _Set()
    Where                = None        # optional [ _Where() ]

    def __init__(self,so):
            if gv(so,['meta','Source']):
                self.Source= self._Source(table = gv(so,['meta','Source','table']),database = gv(so,['meta','Source','database']))
            if gv(so,['meta','Set']):
                self.Set=[]
                for item in gv(so,['meta','Set']):
                    instance_type=item.keys()[0]
                    safe_instance_type=safe_name(instance_type)
                    self.Set.append( type('_'+safe_instance_type,(),{ 'column': gv(item,['column']),'expression': gv(item,['expression']) }) )
            if gv(so,['meta','Where']):
                self.Where=[]
                for item in gv(so,['meta','Where']):
                    instance_type=item.keys()[0]
                    safe_instance_type=safe_name(instance_type)
                    self.Where.append( type('_'+safe_instance_type,(),{ 'c': gv(item,[instance_type,'c']),'e1': gv(item,[instance_type,'e1']),'condition': gv(item,[instance_type,'condition']),'e2': gv(item,[instance_type,'e2']) }) )
    def debug(self):
        debugger(self,'update')


class Upsert:

    class _Source:
        __slots__=()
        table = None
        database = None

        def __init__(self,table=None,database=None):
            if table:  self.table=table
            if database:  self.database=database

    class _Values:
        __slots__=()
        value = None

        def __init__(self,value=None):
            if value:  self.value=value

    class _Update:
        __slots__=()
        column = None
        expression = None

        def __init__(self,column=None,expression=None):
            if column:  self.column=column
            if expression:  self.expression=expression

    class _Columns:
        __slots__=()
        column = None

        def __init__(self,column=None):
            if column:  self.column=column

    class _On_Duplicate_Key:
        __slots__=()
        column = None

        def __init__(self,column=None):
            if column:  self.column=column
    #variable_def

    #variable_class_def
    Source               = _Source()
    Values               = []          #          _Values()
    Update               = []          #          _Update()
    Columns              = []          #          _Columns()
    On_Duplicate_Key     = []          #          _On_Duplicate_Key()

    def __init__(self,so):
            if gv(so,['meta','Source']):
                self.Source= self._Source(table = gv(so,['meta','Source','table']),database = gv(so,['meta','Source','database']))
            if gv(so,['meta','Values']):
                self.Values=[]
                for item in gv(so,['meta','Values']):
                    instance_type=item.keys()[0]
                    safe_instance_type=safe_name(instance_type)
                    self.Values.append( type('_'+safe_instance_type,(),{ 'value': gv(item,['value']) }) )
            if gv(so,['meta','Update']):
                self.Update=[]
                for item in gv(so,['meta','Update']):
                    instance_type=item.keys()[0]
                    safe_instance_type=safe_name(instance_type)
                    self.Update.append( type('_'+safe_instance_type,(),{ 'column': gv(item,['column']),'expression': gv(item,['expression']) }) )
            if gv(so,['meta','Columns']):
                self.Columns=[]
                for item in gv(so,['meta','Columns']):
                    instance_type=item.keys()[0]
                    safe_instance_type=safe_name(instance_type)
                    self.Columns.append( type('_'+safe_instance_type,(),{ 'column': gv(item,['column']) }) )
            if gv(so,['meta','On_Duplicate_Key']):
                self.On_Duplicate_Key=[]
                for item in gv(so,['meta','On_Duplicate_Key']):
                    instance_type=item.keys()[0]
                    safe_instance_type=safe_name(instance_type)
                    self.On_Duplicate_Key.append( type('_'+safe_instance_type,(),{ 'column': gv(item,['column']) }) )
    def debug(self):
        debugger(self,'upsert')


class Use_Table:

    class _Source:
        __slots__=()
        table = None
        database = None

        def __init__(self,table=None,database=None):
            if table:  self.table=table
            if database:  self.database=database
    #variable_def

    #variable_class_def
    Source               = _Source()

    def __init__(self,so):
            if gv(so,['meta','Source']):
                self.Source= self._Source(table = gv(so,['meta','Source','table']),database = gv(so,['meta','Source','database']))
    def debug(self):
        debugger(self,'use table')


class Drop_Table:

    class _Source:
        __slots__=()
        table = None
        database = None

        def __init__(self,table=None,database=None):
            if table:  self.table=table
            if database:  self.database=database
    #variable_def

    #variable_class_def
    Source               = _Source()

    def __init__(self,so):
            if gv(so,['meta','Source']):
                self.Source= self._Source(table = gv(so,['meta','Source','table']),database = gv(so,['meta','Source','database']))
    def debug(self):
        debugger(self,'drop table')


class Create_Table:

    class _Repo:
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

    class _Source:
        __slots__=()
        table = None
        database = None

        def __init__(self,table=None,database=None):
            if table:  self.table=table
            if database:  self.database=database

    class _Columns:
        __slots__=()
        column = None

        def __init__(self,column=None):
            if column:  self.column=column
    #variable_def

    #variable_class_def
    Errors               = None        # optional 
    Temporary            = None        # optional 
    Whitespace           = None        # optional 
    Strict               = None        # optional 
    Comments             = None        # optional 
    Fifo                 = None        # optional 
    Repo                 = None        # optional _Repo()
    Source               = _Source()
    Delimiter            = None        # optional 
    Mode                 = None        # optional 
    file                 = None
    Data_Starts_On       = None        # optional 
    Columns              = []          #          _Columns()

    def __init__(self,so):
            self.errors = gv(so,['meta','errors'])
            self.temporary = gv(so,['meta','Temporary','temporary'])
            self.whitespace = gv(so,['meta','whitespace'])
            self.strict = gv(so,['meta','strict'])
            self.comments = gv(so,['meta','comments'])
            self.fifo = gv(so,['meta','fifo'])
            if gv(so,['meta','Repo']):
                self.Repo= self._Repo(protocol = gv(so,['meta','Repo','protocol']),url = gv(so,['meta','Repo','url']),user = gv(so,['meta','Repo','user']),file = gv(so,['meta','Repo','file']),directory = gv(so,['meta','Repo','directory']),password = gv(so,['meta','Repo','password']))
            if gv(so,['meta','Source']):
                self.Source= self._Source(table = gv(so,['meta','Source','table']),database = gv(so,['meta','Source','database']))
            self.delimiter = gv(so,['meta','delimiter'])
            self.mode = gv(so,['meta','mode'])
            self.file = gv(so,['meta','file'])
            self.data_starts_on = gv(so,['meta','data_starts_on'])
            if gv(so,['meta','Columns']):
                self.Columns=[]
                for item in gv(so,['meta','Columns']):
                    instance_type=item.keys()[0]
                    safe_instance_type=safe_name(instance_type)
                    self.Columns.append( type('_'+safe_instance_type,(),{ 'column': gv(item,['column']) }) )
    def debug(self):
        debugger(self,'create table')


class Update_Table:

    class _Source:
        __slots__=()
        table = None
        database = None

        def __init__(self,table=None,database=None):
            if table:  self.table=table
            if database:  self.database=database

    class _Columns:
        __slots__=()
        column = None

        def __init__(self,column=None):
            if column:  self.column=column
    #variable_def

    #variable_class_def
    Errors               = None        # optional 
    Whitespace           = None        # optional 
    Data_Starts_On       = None        # optional 
    Comments             = None        # optional 
    Source               = _Source()
    Delimiter            = None        # optional 
    File                 = None        # optional 
    Columns              = None        # optional [ _Columns() ]

    def __init__(self,so):
            self.errors = gv(so,['meta','Errors','errors'])
            self.whitespace = gv(so,['meta','Whitespace','whitespace'])
            self.data_starts_on = gv(so,['meta','Data_Starts_On','data_starts_on'])
            self.comments = gv(so,['meta','Comments','comments'])
            if gv(so,['meta','Source']):
                self.Source= self._Source(table = gv(so,['meta','Source','table']),database = gv(so,['meta','Source','database']))
            self.field = gv(so,['meta','Delimiter','field'])
            self.file = gv(so,['meta','File','file'])
            if gv(so,['meta','Columns']):
                self.Columns=[]
                for item in gv(so,['meta','Columns']):
                    instance_type=item.keys()[0]
                    safe_instance_type=safe_name(instance_type)
                    self.Columns.append( type('_'+safe_instance_type,(),{ 'column': gv(item,['column']) }) )
    def debug(self):
        debugger(self,'update table')


class Describe_Table:

    class _Source:
        __slots__=()
        table = None
        database = None

        def __init__(self,table=None,database=None):
            if table:  self.table=table
            if database:  self.database=database
    #variable_def

    #variable_class_def
    Source               = _Source()

    def __init__(self,so):
            if gv(so,['meta','Source']):
                self.Source= self._Source(table = gv(so,['meta','Source','table']),database = gv(so,['meta','Source','database']))
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


