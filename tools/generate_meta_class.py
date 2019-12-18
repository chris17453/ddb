import sys
import os

from .language import language
from .data import meta_str, get_data, variable_def,init,debug,sub_class, template_add, template_get

# meta file header
template_add ("# This is an auto generated assembly ",None)
template_add ("# dont edit this, edit the template generator, in tools ",None)
template_add("""

class meta:

    class debugger:
        def __init__(self,obj,name,depth=0):
            pad=''
            for i in range(0,depth):
                pad+=' '
            if depth==0:
                print ("\\n\\033[31;1;4mDebug: {0}\\033[0m".format(name))

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
""",None)




for command in language['commands']:
    command_name=command['name'].replace(' ','_')
    classes={}
    class_spec={}
    
    #load data about the curent class
    get_data(command,classes,class_spec)
    
    # create the sub classes
    sub_class (command,classes,class_spec)

    # create the other class header and class vars
    variable_def (command,classes,class_spec)
    
    # create the init for the outer class
    init(command,classes,class_spec)
    
    #create the debug for the outer class
    debug(command,classes,class_spec)

    # gap between classes
    template_add("# ****")
# generate selector for classes
meta_str()

print ( template_get() )


    