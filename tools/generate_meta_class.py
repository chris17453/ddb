import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from source.ddb.lexer.language import language
from .data import meta_str, get_data, variable_def,init,debug,sub_class

# meta file header
print ("# This is an auto generated assembly ")
print ("# dont edit this, edit the template generator, in tools ")
print ("""

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
""")




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
    print("")
    print("")

# generate selector for classes
meta_str()


    