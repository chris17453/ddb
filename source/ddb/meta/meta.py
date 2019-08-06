# This is an auto generated assembly 
# dont edit this, edit the template generator, in tools 


class meta:

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
                        meta.debugger(item,var,depth+4)
                elif callable(value):
                    continue
                elif value==None:
                    var_count+=1
                    empty.append(var)
                else:
                    var_count+=1
                    print ("{0}- {1} :".format(pad,var))
                    meta.debugger(value,var,depth+4)
                    
            if len(empty)>0:
                print ("{1}Empty Vars: {0}".format(",".join(empty),pad))
            #print variables
            if var_count==0:
                print("{2}{0} {1}".format("No attributes"+':',"",pad))

    @staticmethod
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

    @staticmethod
    def safe_name(name,no_match=None):
        forbidden=[ 'False', 'None', 'True', 'and', 'as', 'assert', 'break', 'class', 'continue', 'def', 'del', 'elif', 'else', 'except', 'finally', 'for', 
                    'from', 'global', 'if', 'import', 'in', 'is', 'lambda', 'nonlocal', 'not', 'or', 'pass', 'raise', 'return', 'try', 'while', 'with', 'yield'
                    'abs','divmod','input','open','staticmethod','all','enumerate','int','ord','str','any','eval','isinstance','pow','sum','basestring','execfile',
                    'issubclass','print','super','bin','file','iter','property','tuple','bool','filter','len','range','type','bytearray','float','list','raw_input',
                    'unichr','callable','format','locals','reduce','unicode','chr','frozenset','long','reload','vars','classmethod','getattr','map','repr','xrange',
                    'cmp','globals','max','reversed','zip','compile','hasattr','memoryview','round','__import__','complex','hash','min','set','delattr','help','next',
                    'setattr','dict','hex','object','slice','dir','id','oct','sorted']
        name=name.replace(" ","_")
        if no_match:
            return name
        if name in forbidden:
            name=name.title()
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
                if meta.gv(so,['meta','source']):
                    self.source= self._source(table = meta.gv(so,['meta','source','table']),database = meta.gv(so,['meta','source','database']))
        def debug(self):
            meta.debugger(self,'show columns')
    # ****
    class show_tables:
        #variable_def
    
        #variable_class_def
    
        def __init__(self,so):
            a=0 # holder
    
        def debug(self):
            meta.debugger(self,'show tables')
    # ****
    class show_variables:
        #variable_def
    
        #variable_class_def
    
        def __init__(self,so):
            a=0 # holder
    
        def debug(self):
            meta.debugger(self,'show variables')
    # ****
    class select:
    
        class _and:
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
    
        class _or:
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
        distinct             = None        # optional 
        source               = None        # optional _source()
        group_by             = None        # optional [ _group_by() ]
        limit                = None        # optional _limit()
        where                = None        # optional [ _where() ]
        columns              = []          #          _columns()
    
        def __init__(self,so):
                if meta.gv(so,['meta','order by']):
                    self.order_by=[]
                    for item in meta.gv(so,['meta','order by']):
                        instance_type=item.keys()[0]
                        safe_instance_type='_'+instance_type
                        self.order_by.append( type(safe_instance_type,(),{ 'column': meta.gv(item,['column']),'direction': meta.gv(item,['direction']) }) )
                self.distinct = meta.gv(so,['meta','distinct','distinct'])
                if meta.gv(so,['meta','source']):
                    self.source= self._source(table = meta.gv(so,['meta','source','table']),display = meta.gv(so,['meta','source','display']),database = meta.gv(so,['meta','source','database']))
                if meta.gv(so,['meta','group by']):
                    self.group_by=[]
                    for item in meta.gv(so,['meta','group by']):
                        instance_type=item.keys()[0]
                        safe_instance_type='_'+instance_type
                        self.group_by.append( type(safe_instance_type,(),{ 'column': meta.gv(item,['column']) }) )
                if meta.gv(so,['meta','limit']):
                    self.limit= self._limit(start = meta.gv(so,['meta','limit','start']),length = meta.gv(so,['meta','limit','length']))
                if meta.gv(so,['meta','where']):
                    self.where=[]
                    for item in meta.gv(so,['meta','where']):
                        instance_type=item.keys()[0]
                        safe_instance_type='_'+instance_type
                        self.where.append( type(safe_instance_type,(),{ 'c': meta.gv(item,[instance_type,'c']),'e1': meta.gv(item,[instance_type,'e1']),'condition': meta.gv(item,[instance_type,'condition']),'e2': meta.gv(item,[instance_type,'e2']) }) )
                if meta.gv(so,['meta','columns']):
                    self.columns=[]
                    for item in meta.gv(so,['meta','columns']):
                        instance_type=item.keys()[0]
                        safe_instance_type='_'+instance_type
                        self.columns.append( type(safe_instance_type,(),{ 'function': meta.gv(item,['function']),'column': meta.gv(item,['column']),'argument2': meta.gv(item,['argument2']),'argument3': meta.gv(item,['argument3']),'argument1': meta.gv(item,['argument1']),'display': meta.gv(item,['display']) }) )
        def debug(self):
            meta.debugger(self,'select')
    # ****
    class Set:
    
        class _set:
            __slots__=()
            variable = None
            value = None
    
            def __init__(self,variable=None,value=None):
                if variable:  self.variable=variable
                if value:  self.value=value
        #variable_def
    
        #variable_class_def
        set                  = None        # optional [ _set() ]
    
        def __init__(self,so):
                if meta.gv(so,['meta','set']):
                    self.set=[]
                    for item in meta.gv(so,['meta','set']):
                        instance_type=item.keys()[0]
                        safe_instance_type='_'+instance_type
                        self.set.append( type(safe_instance_type,(),{ 'variable': meta.gv(item,['variable']),'value': meta.gv(item,['value']) }) )
        def debug(self):
            meta.debugger(self,'set')
    # ****
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
                if meta.gv(so,['meta','parameters']):
                    self.parameters=[]
                    for item in meta.gv(so,['meta','parameters']):
                        instance_type=item.keys()[0]
                        safe_instance_type='_'+instance_type
                        self.parameters.append( type(safe_instance_type,(),{ 'parameter': meta.gv(item,['parameter']) }) )
        def debug(self):
            meta.debugger(self,'create procedure')
    # ****
    class delimiter:
        #variable_def
    
        #variable_class_def
        delimiter            = None
    
        def __init__(self,so):
                self.delimiter = meta.gv(so,['meta','delimiter','delimiter'])
        def debug(self):
            meta.debugger(self,'delimiter')
    # ****
    class end:
        #variable_def
    
        #variable_class_def
    
        def __init__(self,so):
            a=0 # holder
    
        def debug(self):
            meta.debugger(self,'end')
    # ****
    class begin:
        #variable_def
    
        #variable_class_def
    
        def __init__(self,so):
            a=0 # holder
    
        def debug(self):
            meta.debugger(self,'begin')
    # ****
    class commit:
        #variable_def
    
        #variable_class_def
    
        def __init__(self,so):
            a=0 # holder
    
        def debug(self):
            meta.debugger(self,'commit')
    # ****
    class rollback:
        #variable_def
    
        #variable_class_def
    
        def __init__(self,so):
            a=0 # holder
    
        def debug(self):
            meta.debugger(self,'rollback')
    # ****
    class show_output_modules:
        #variable_def
    
        #variable_class_def
    
        def __init__(self,so):
            a=0 # holder
    
        def debug(self):
            meta.debugger(self,'show output modules')
    # ****
    class delete:
    
        class _and:
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
    
        class _source:
            __slots__=()
            table = None
            database = None
    
            def __init__(self,table=None,database=None):
                if table:  self.table=table
                if database:  self.database=database
    
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
    
        class _or:
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
                if meta.gv(so,['meta','source']):
                    self.source= self._source(table = meta.gv(so,['meta','source','table']),database = meta.gv(so,['meta','source','database']))
                if meta.gv(so,['meta','where']):
                    self.where=[]
                    for item in meta.gv(so,['meta','where']):
                        instance_type=item.keys()[0]
                        safe_instance_type='_'+instance_type
                        self.where.append( type(safe_instance_type,(),{ 'c': meta.gv(item,[instance_type,'c']),'e1': meta.gv(item,[instance_type,'e1']),'condition': meta.gv(item,[instance_type,'condition']),'e2': meta.gv(item,[instance_type,'e2']) }) )
        def debug(self):
            meta.debugger(self,'delete')
    # ****
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
                if meta.gv(so,['meta','source']):
                    self.source= self._source(table = meta.gv(so,['meta','source','table']),database = meta.gv(so,['meta','source','database']))
                if meta.gv(so,['meta','values']):
                    self.values=[]
                    for item in meta.gv(so,['meta','values']):
                        instance_type=item.keys()[0]
                        safe_instance_type='_'+instance_type
                        self.values.append( type(safe_instance_type,(),{ 'value': meta.gv(item,['value']) }) )
                if meta.gv(so,['meta','columns']):
                    self.columns=[]
                    for item in meta.gv(so,['meta','columns']):
                        instance_type=item.keys()[0]
                        safe_instance_type='_'+instance_type
                        self.columns.append( type(safe_instance_type,(),{ 'column': meta.gv(item,['column']) }) )
        def debug(self):
            meta.debugger(self,'insert')
    # ****
    class update:
    
        class _and:
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
    
        class _source:
            __slots__=()
            table = None
            database = None
    
            def __init__(self,table=None,database=None):
                if table:  self.table=table
                if database:  self.database=database
    
        class _set:
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
    
        class _or:
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
        set                  = []          #          _set()
        where                = None        # optional [ _where() ]
    
        def __init__(self,so):
                if meta.gv(so,['meta','source']):
                    self.source= self._source(table = meta.gv(so,['meta','source','table']),database = meta.gv(so,['meta','source','database']))
                if meta.gv(so,['meta','set']):
                    self.set=[]
                    for item in meta.gv(so,['meta','set']):
                        instance_type=item.keys()[0]
                        safe_instance_type='_'+instance_type
                        self.set.append( type(safe_instance_type,(),{ 'column': meta.gv(item,['column']),'expression': meta.gv(item,['expression']) }) )
                if meta.gv(so,['meta','where']):
                    self.where=[]
                    for item in meta.gv(so,['meta','where']):
                        instance_type=item.keys()[0]
                        safe_instance_type='_'+instance_type
                        self.where.append( type(safe_instance_type,(),{ 'c': meta.gv(item,[instance_type,'c']),'e1': meta.gv(item,[instance_type,'e1']),'condition': meta.gv(item,[instance_type,'condition']),'e2': meta.gv(item,[instance_type,'e2']) }) )
        def debug(self):
            meta.debugger(self,'update')
    # ****
    class upsert:
    
        class _source:
            __slots__=()
            table = None
            database = None
    
            def __init__(self,table=None,database=None):
                if table:  self.table=table
                if database:  self.database=database
    
        class _set:
            __slots__=()
            column = None
            expression = None
    
            def __init__(self,column=None,expression=None):
                if column:  self.column=column
                if expression:  self.expression=expression
    
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
    
        class _on_duplicate_key:
            __slots__=()
            column = None
    
            def __init__(self,column=None):
                if column:  self.column=column
        #variable_def
    
        #variable_class_def
        source               = _source()
        set                  = []          #          _set()
        values               = []          #          _values()
        columns              = []          #          _columns()
        on_duplicate_key     = []          #          _on_duplicate_key()
    
        def __init__(self,so):
                if meta.gv(so,['meta','source']):
                    self.source= self._source(table = meta.gv(so,['meta','source','table']),database = meta.gv(so,['meta','source','database']))
                if meta.gv(so,['meta','set']):
                    self.set=[]
                    for item in meta.gv(so,['meta','set']):
                        instance_type=item.keys()[0]
                        safe_instance_type='_'+instance_type
                        self.set.append( type(safe_instance_type,(),{ 'column': meta.gv(item,['column']),'expression': meta.gv(item,['expression']) }) )
                if meta.gv(so,['meta','values']):
                    self.values=[]
                    for item in meta.gv(so,['meta','values']):
                        instance_type=item.keys()[0]
                        safe_instance_type='_'+instance_type
                        self.values.append( type(safe_instance_type,(),{ 'value': meta.gv(item,['value']) }) )
                if meta.gv(so,['meta','columns']):
                    self.columns=[]
                    for item in meta.gv(so,['meta','columns']):
                        instance_type=item.keys()[0]
                        safe_instance_type='_'+instance_type
                        self.columns.append( type(safe_instance_type,(),{ 'column': meta.gv(item,['column']) }) )
                if meta.gv(so,['meta','on duplicate key']):
                    self.on_duplicate_key=[]
                    for item in meta.gv(so,['meta','on duplicate key']):
                        instance_type=item.keys()[0]
                        safe_instance_type='_'+instance_type
                        self.on_duplicate_key.append( type(safe_instance_type,(),{ 'column': meta.gv(item,['column']) }) )
        def debug(self):
            meta.debugger(self,'upsert')
    # ****
    class use:
        #variable_def
    
        #variable_class_def
        database             = None
    
        def __init__(self,so):
                self.database = meta.gv(so,['meta','source','database'])
        def debug(self):
            meta.debugger(self,'use')
    # ****
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
                if meta.gv(so,['meta','source']):
                    self.source= self._source(table = meta.gv(so,['meta','source','table']),database = meta.gv(so,['meta','source','database']))
        def debug(self):
            meta.debugger(self,'drop table')
    # ****
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
        fifo                 = None        # optional 
        repo                 = None        # optional _repo()
        source               = _source()
        delimiter            = None        # optional 
        mode                 = None        # optional 
        file                 = None        # optional 
        columns              = []          #          _columns()
        comments             = None        # optional 
    
        def __init__(self,so):
                self.errors = meta.gv(so,['meta','errors'])
                self.temporary = meta.gv(so,['meta','temporary','temporary'])
                self.whitespace = meta.gv(so,['meta','whitespace'])
                self.strict = meta.gv(so,['meta','strict'])
                self.data_starts_on = meta.gv(so,['meta','data_starts_on'])
                self.fifo = meta.gv(so,['meta','fifo'])
                if meta.gv(so,['meta','repo']):
                    self.repo= self._repo(protocol = meta.gv(so,['meta','repo','protocol']),url = meta.gv(so,['meta','repo','url']),user = meta.gv(so,['meta','repo','user']),file = meta.gv(so,['meta','repo','file']),directory = meta.gv(so,['meta','repo','directory']),password = meta.gv(so,['meta','repo','password']))
                if meta.gv(so,['meta','source']):
                    self.source= self._source(table = meta.gv(so,['meta','source','table']),database = meta.gv(so,['meta','source','database']))
                self.delimiter = meta.gv(so,['meta','delimiter'])
                self.mode = meta.gv(so,['meta','mode'])
                self.file = meta.gv(so,['meta','file'])
                if meta.gv(so,['meta','columns']):
                    self.columns=[]
                    for item in meta.gv(so,['meta','columns']):
                        instance_type=item.keys()[0]
                        safe_instance_type='_'+instance_type
                        self.columns.append( type(safe_instance_type,(),{ 'column': meta.gv(item,['column']) }) )
                self.comments = meta.gv(so,['meta','comments'])
        def debug(self):
            meta.debugger(self,'create table')
    # ****
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
        comments             = None        # optional 
        source               = _source()
        delimiter            = None        # optional 
        file                 = None        # optional 
        columns              = None        # optional [ _columns() ]
    
        def __init__(self,so):
                self.errors = meta.gv(so,['meta','errors','errors'])
                self.whitespace = meta.gv(so,['meta','whitespace','whitespace'])
                self.data_starts_on = meta.gv(so,['meta','data_starts_on','data_starts_on'])
                self.comments = meta.gv(so,['meta','comments','comments'])
                if meta.gv(so,['meta','source']):
                    self.source= self._source(table = meta.gv(so,['meta','source','table']),database = meta.gv(so,['meta','source','database']))
                self.field = meta.gv(so,['meta','delimiter','field'])
                self.file = meta.gv(so,['meta','file','file'])
                if meta.gv(so,['meta','columns']):
                    self.columns=[]
                    for item in meta.gv(so,['meta','columns']):
                        instance_type=item.keys()[0]
                        safe_instance_type='_'+instance_type
                        self.columns.append( type(safe_instance_type,(),{ 'column': meta.gv(item,['column']) }) )
        def debug(self):
            meta.debugger(self,'update table')
    # ****
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
                if meta.gv(so,['meta','source']):
                    self.source= self._source(table = meta.gv(so,['meta','source','table']),database = meta.gv(so,['meta','source','database']))
        def debug(self):
            meta.debugger(self,'describe table')
    # ****
    
    def convert_to_class(self,o):
        
        if o['mode']=='show columns': return self.show_columns(o)
        elif o['mode']=='show tables': return self.show_tables(o)
        elif o['mode']=='show variables': return self.show_variables(o)
        elif o['mode']=='select': return self.select(o)
        elif o['mode']=='set': return self.Set(o)
        elif o['mode']=='create procedure': return self.create_procedure(o)
        elif o['mode']=='delimiter': return self.delimiter(o)
        elif o['mode']=='end': return self.end(o)
        elif o['mode']=='begin': return self.begin(o)
        elif o['mode']=='commit': return self.commit(o)
        elif o['mode']=='rollback': return self.rollback(o)
        elif o['mode']=='show output modules': return self.show_output_modules(o)
        elif o['mode']=='delete': return self.delete(o)
        elif o['mode']=='insert': return self.insert(o)
        elif o['mode']=='update': return self.update(o)
        elif o['mode']=='upsert': return self.upsert(o)
        elif o['mode']=='use': return self.use(o)
        elif o['mode']=='drop table': return self.drop_table(o)
        elif o['mode']=='create table': return self.create_table(o)
        elif o['mode']=='update table': return self.update_table(o)
        elif o['mode']=='describe table': return self.describe_table(o)
    
        return None
    

