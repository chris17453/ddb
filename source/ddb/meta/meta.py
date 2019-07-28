
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



class show_columns:

    class _source:
        __slots__=()
        table = None
        database = None

        def __init__(self,table=None,database=None):
            if table:  self.table=table
            if database:  self.database=database

    source               = _source()

    def __init__(self,so):
            if gv(so,['meta','source']):
                self.source= self._source(table = gv(so,['meta','source','table']),database = gv(so,['meta','source','database']))
    def debug(self):
        debugger(self,'show columns')


class show_tables:


    def __init__(self,so):
        a=0 # holder

    def debug(self):
        debugger(self,'show tables')


class show_variables:


    def __init__(self,so):
        a=0 # holder

    def debug(self):
        debugger(self,'show variables')


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

    class _group_by:
        __slots__=()
        column = None

        def __init__(self,column=None):
            if column:  self.column=column

    class _source:
        __slots__=()
        table = None
        display = None
        database = None

        def __init__(self,table=None,display=None,database=None):
            if table:  self.table=table
            if display:  self.display=display
            if database:  self.database=database

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

    class _order_by:
        __slots__=()
        column = None
        direction = None

        def __init__(self,column=None,direction=None):
            if column:  self.column=column
            if direction:  self.direction=direction
