from .context import ddb
from .data import meta_str, get_data, variable_def,init,debug,sub_class

# meta file header
print ("# This is an auto generated assembly ")
print ("# dont edit this, edit the template generator, in tools ")
print ("")

for command in ddb.lexer.language.language['commands']:
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


    