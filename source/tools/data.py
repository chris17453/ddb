from .context import ddb

def get_data(command,classes,class_spec):
    command_name=command['name'].replace(' ','_')
    print ("class {0}:".format(command_name))
    print ("    __slots__=()")
    
    for segment in command['segments']:
        optional=None
        if 'optional' in segment:
                optional=segment['optional']

        storage=None
        if 'store_array' in segment:
                storage='array'
        parent=None
        if 'parent' in segment:
            parent=segment['parent']
        #print class_spec,segment['name']
        class_spec[segment['name']]={'optional':optional,'storage':storage,'parent':parent}
        optional=None

        for fragment in segment['data']:
            storage=None
            if 'type' in fragment:
                storage=fragment['type']

            for word in fragment['signature']:
                first_char=word[0:1]
                last_char=word[-1]
                if first_char == '{' and last_char == '}':
                    if segment['name'] not in classes:
                        classes[segment['name']]={}
                    if word[1:-1] not in classes[segment['name']]:
                        classes[segment['name']][word[1:-1]]={'count':1,'default':None,'type':'string','values':None,'optional':optional,'storage':storage}
                    else:
                        classes[segment['name']][word[1:-1]]['count']+=1
                if first_char=='$':
                    variable=word[1:]
                    index_of_colon=variable.find(':')
                    if index_of_colon!=-1:
                        #variable=word[0:index_of_colon-1]
                        key=variable[index_of_colon+1:].lower()
                    else:
                        key=variable.lower()
                    if key not in classes[segment['name']]:
                        classes[segment['name']][key]={'count':1,'default':None,'type':'string','values':None,'optional':optional,'storage':storage}
                    else:
                        classes[segment['name']][key]['count']+=1

            if 'vars' in fragment:
                for word in fragment['vars']:
                    if segment['name'] not in classes:
                        classes[segment['name']]={}
                    if word not in classes[segment['name']]:
                        classes[segment['name']][word]={'count':1,'default':None,'type':'string','values':None,'optional':optional,'storage':storage}
                    else:
                        classes[segment['name']][word]['count']+=1

            if 'arguments' in segment:
                if segment['arguments']!=1 and segment['arguments']!=None:
                    classes[segment['name']]['_arguments']=segment['arguments']

            if 'specs' in segment:
                fragment=segment
                #print segment
                for variable in fragment['specs']:
                    if variable[0]=='_':
                            continue
                    #print variable
                    default=None
                    if 'default' in fragment['specs'][variable]:
                        default=fragment['specs'][variable]['default']
                    _type='string'
                    if 'type' in fragment['specs'][variable]:
                       _type=fragment['specs'][variable]['type']
                    values=None
                    if 'values' in fragment['specs'][variable]:
                        values=fragment['specs'][variable]['values']
                        
                    if variable not in classes[segment['name']]:
                        classes[segment['name']][variable]={'count':1,'default':default,'type':_type,'values':values,'optional':optional,'storage':storage}
                    else:
                       classes[segment['name']][variable]['optional']=optional
                       classes[segment['name']][variable]['default']=default
                       classes[segment['name']][variable]['type']=_type
                       classes[segment['name']][variable]['values']=values




def sub_class (command,classes,class_spec):
    for _class in classes:
        class_name=_class.replace(" ","_")
        if len(classes[_class])<2:
            continue

        print ("    class _{0}:".format(_class.replace(" ","_")))
        print ("        __slots__=()")

        for variable in classes[_class]:
            if variable[0]=='_':
                continue
            if len(classes[_class])<2:
                continue
            pad='    '
            var=classes[_class][variable]
          #  print var
            value=var['default']

            if var['type']=='string' or var['type']=='char':
                if var['default']!=None:
                    value="'{0}'".format(var['default'])
            print ("{2}    {0} = {1}".format(variable,value,pad))
        
        args=[]
        if len(classes[_class])>1:
            for variable in classes[_class]:
                if '_arguments' in variable:
                        continue
                args.append(variable+"=None")
            print ("        def __init__(self,{0}):".format(",".join(args)))
            for variable in classes[_class]:
                if '_arguments' in variable:
                        continue
                print ("            if {0}:".format(variable))
                print ("                self.{0}={0}".format(variable))
                        
                


     
        if len(classes[_class])>1 and  class_spec[_class]['parent']!=None:
            print("\n        def debug(self):")
            print("            print('  Debug Info: {0}')".format(class_name))
            for variable in classes[_class]:
                if variable[0]=='_':
                    continue
                print ("            print('  {1:<20} '.format(self.{0}))".format(variable,variable+':'))



def variable_def (command,classes,class_spec):
    for _class in classes:
        class_name=_class.replace(" ","_")
        if len(classes[_class])>1:
            continue

        for variable in classes[_class]:
            if variable[0]=='_':
                continue
            if len(classes[_class])<2:
                continue
            pad='    '
            var=classes[_class][variable]
          #  print var
            value=var['default']

            if var['type']=='string' or var['type']=='char':
                if var['default']!=None:
                    value="'{0}'".format(var['default'])
            print ("{2}    {0} = {1}".format(variable,value,pad))
        
        args=[]


 #print(classes)
    #print(class_spec)  
    print ("")
    for _class in classes:

        if len(classes[_class])>1:
            class_name="{1}()".format(command['name'].replace(' ','_'),_class)
        else:
            class_name=''

        if class_spec[_class]['parent']!=None:
                continue

        if class_spec[_class]['optional']:
            if '_arguments' in classes[_class] or  class_spec[_class]['storage']=='array':
                class_name='[ {0} ]'.format(class_name)
            print ("    {0:<20} = None        # optional {1}".format(_class.replace(" ","_"),class_name))
            continue

        #print classes[_class]
        if '_arguments' in classes[_class]:
                print ("    {0:<20} = []          #          {1}".format(_class.replace(" ","_"),class_name))
                continue

        if len(classes[_class])>1:
            print ("    {1:<20} = _{1}()".format(command['name'].replace(' ','_'),_class.replace(" ","_")))
            continue

        for variable in classes[_class]:
            pad=''
            var=classes[_class][variable]
            value=var['default']

            if var['type']=='string' or var['type']=='char':
                if var['default']!=None:
                    value="'{0}'".format(var['default'])
            print ("{2}    {0:<20} = {1}".format(variable,value,pad))
        


def init(command,classes,class_spec):
    command_name=command['name'].replace(' ','_')
    if len(classes)>0:
        print("\n    def __init__(self,so):")
        for _class in classes:

            if len(classes[_class])==1:
                for variable in classes[_class]:
                    if '_arguments' == variable or  class_spec[_class]['parent']!=None:
                        continue;

                    if classes[_class][variable]['storage']=='single':
                        sqo="gv(so,['meta','{1}'])".format(_class,variable)
                        print ("            self.{0:<20} = {1}".format(variable,sqo))
                    else:
                        sqo="gv(so,['meta','{0}','{1}'])".format(_class,variable)
                        print ("            self.{0:<20} = {1}".format(variable,sqo))
            else:
                var=[]
                if '_arguments' in classes[_class]  or class_spec[_class]['storage']=='array':
                    for variable in classes[_class]:
                            if variable[0]=='_':
                                    continue
                            #print classes[_class],variable
                            sqo="gv(item,['{1}'])".format(_class,variable)
                            var.append("{1} = {0}".format(sqo,variable))    
                else:
                    for variable in classes[_class]:
                        if variable[0]=='_':
                                continue
                        #print classes[_class],variable
                        if classes[_class][variable]['storage']=='single':
                            sqo="gv(so,['{2}','{1}'])".format(_class,variable,'meta')
                        else:
                            sqo="gv(so,['{2}','{0}','{1}'])".format(_class,variable,'meta')
                        var.append("{1} = {0}".format(sqo,variable))    

                sqo="so['meta']['{0}']".format(_class)
                if '_arguments' in classes[_class]  or class_spec[_class]['storage']=='array':
                        print ("            if gv(so,['meta','{0}','{1}']):".format(command_name,_class,",".join(var)))
                        print ("                self.{1:<20}=[]".format(command_name,_class.replace(" ","_")))
                        print ("                for item in so['meta']['{0}']['{1}']:".format(command_name,_class,",".join(var)))
                        print ("                    self.{1:<20}.append( self._{1}({2}) )".format(command_name,_class.replace(" ","_"),",".join(var)))
                else:
                    if class_spec[_class]['parent']==None:
                        print ("            if gv(so,['meta','{0}','{1}']):".format(command_name,_class))
                        print ("                self.{1:<20}= self._{1}({2})".format(command_name,_class.replace(" ","_"),",".join(var)))
                


def debug(command,classes,class_spec):  
    command_name=command['name'].replace(' ','_')
    if len(classes)>0:
        print("        print('Debug Info: {0}')".format(command_name))
        for _class in classes:
            if len(classes[_class])>1:
                for variable in classes[_class]:
                    if '_arguments' == variable or  class_spec[_class]['parent']==None:
                        if variable[0]=='_':
                            continue
                        print ("        print('{1:<20} '.format(self.{0}))".format(variable,variable+':'))
            else:
                print("        self.{0}.debug()".format(_class.replace(' ',"_")))
    else:
        print("\n    def __init__(self,so=None):")
        print("          a=1")
        print("")
        print("    def debug(self):")
        print("        print('Debug Info: {0}')".format(command_name))
        print("        print('No variables')")



def meta_str():
    print """
        def get_meta(o):
    """

    index=0
    for command in ddb.lexer.language.language['commands']:
        if index==0:
            el=""
        else:
            el="el"
        index+=1
        command_name=command['name'].replace(' ','_')
        print ("    {1}if o['mode']=='{0}':".format(command['name'],el))
        print ("        return {1}(o)".format(command['name'],command_name))

    print """
        return None

    """