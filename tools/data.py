
from .language import language

def safe_name(name,no_match=None):
    forbidden=[ 'False', 'None', 'True', 'and', 'as', 'assert', 'break', 'class', 'continue', 'def', 'del', 'elif', 'else', 'except', 'finally', 'for', 
                'from', 'global', 'if', 'import', 'in', 'is', 'lambda', 'nonlocal', 'not', 'or', 'pass', 'raise', 'return', 'try', 'while', 'with', 'yield'
                'abs','divmod','input','open','staticmethod','all','enumerate','int','ord','str','any','eval','isinstance','pow','sum','basestring','execfile',
                'issubclass','template_add','super','bin','file','iter','property','tuple','bool','filter','len','range','type','bytearray','float','list','raw_input',
                'unichr','callable','format','locals','reduce','unicode','chr','frozenset','long','reload','vars','classmethod','getattr','map','repr','xrange',
                'cmp','globals','max','reversed','zip','compile','hasattr','memoryview','round','__import__','complex','hash','min','set','delattr','help','next',
                'setattr','dict','hex','object','slice','dir','id','oct','sorted']
    name=name.replace(" ","_")
    if no_match:
        return name
    if name in forbidden:
        name=name.title()
    return name

output=""
def template_add(data,pad=True):
    global output


    lines=data.split('\n')
    if pad:
        for line in lines:
            output+="    "+line+"\n"
    else:
        for line in lines:
            output+=line+"\n"


def template_get():
    global output
    return output

def get_data(command,classes,class_spec):
    command_name=safe_name(command['name'])
    template_add("class {0}:".format(command_name))
    
    for segment in command['segments']:
        segment_name=safe_name(segment['name'],1)
        optional=None
        if 'optional' in segment:
                optional=segment['optional']
        seg_type=None
        if 'type' in segment:
                seg_type=segment['type']
        storage=None
        if 'store_array' in segment:
                storage='array'
        no_keyword=None
        if 'no_keyword' in segment:
                no_keyword=True 

        if no_keyword:
             seg_type='single'
        parent=None
        if 'parent' in segment:
            parent=segment['parent']
        #template_add class_spec,segment_name
        class_spec[segment_name]={'optional':optional,'storage':storage,'parent':parent,'type':seg_type,'no_keyword':no_keyword,'key':segment['name']}
        optional=None

        for fragment in segment['data']:
            storage=None
            if 'type' in fragment:
                storage=fragment['type']

            for word in fragment['signature']:
                first_char=word[0:1]
                last_char=word[-1]
                if first_char == '{' and last_char == '}':
                    if segment_name not in classes:
                        classes[segment_name]={}
                    if word[1:-1] not in classes[segment_name]:
                        classes[segment_name][word[1:-1]]={'count':1,'default':None,'type':'string','values':None,'optional':optional,'storage':storage}
                    else:
                        classes[segment_name][word[1:-1]]['count']+=1
                if first_char=='$':
                    variable=word[1:]
                    index_of_colon=variable.find(':')
                    if index_of_colon!=-1:
                        #variable=word[0:index_of_colon-1]
                        key=variable[index_of_colon+1:].lower()
                    else:
                        key=variable.lower()
                    if key not in classes[segment_name]:
                        classes[segment_name][key]={'count':1,'default':None,'type':'string','values':None,'optional':optional,'storage':storage}
                    else:
                        classes[segment_name][key]['count']+=1

            if 'vars' in fragment:
                for word in fragment['vars']:
                    if segment_name not in classes:
                        classes[segment_name]={}
                    if word not in classes[segment_name]:
                        classes[segment_name][word]={'count':1,'default':None,'type':'string','values':None,'optional':optional,'storage':storage}
                    else:
                        classes[segment_name][word]['count']+=1

            if 'arguments' in segment:
                if segment['arguments']!=1 and segment['arguments']!=None:
                    classes[segment_name]['_arguments']=segment['arguments']

            if 'specs' in segment:
                fragment=segment
                #template_add segment
                for variable in fragment['specs']:
                    if variable[0]=='_':
                            continue
                    #template_add variable
                    default=None
                    if 'default' in fragment['specs'][variable]:
                        default=fragment['specs'][variable]['default']
                    _type='string'
                    if 'type' in fragment['specs'][variable]:
                       _type=fragment['specs'][variable]['type']
                    values=None
                    if 'values' in fragment['specs'][variable]:
                        values=fragment['specs'][variable]['values']
                        
                    if variable not in classes[segment_name]:
                        classes[segment_name][variable]={'count':1,'default':default,'type':_type,'values':values,'optional':optional,'storage':storage}
                    else:
                       classes[segment_name][variable]['optional']=optional
                       classes[segment_name][variable]['default']=default
                       classes[segment_name][variable]['type']=_type
                       classes[segment_name][variable]['values']=values




def sub_class (command,classes,class_spec):
    for _class in classes:
        class_name=_class.replace(" ","_")
        if len(classes[_class])<2:
            continue

        template_add ("")
        template_add ("    class _{0}:".format(_class.replace(" ","_")))
        


        slot_vars=[]
        for variable in classes[_class]:
            if variable[0]=='_':
                continue
            if len(classes[_class])<2:
                continue
            var=classes[_class][variable]
        
            slot_vars.append("'"+variable+"'")
        
        template_add ("        __slots__=[{0}]".format(",".join(slot_vars)))


        #for variable in classes[_class]:
        #    if variable[0]=='_':
        #        continue
        #    if len(classes[_class])<2:
        #        continue
        #    pad='    '
        #    var=classes[_class][variable]
        #  #  template_add var
        #    value=var['default']
#
        #    if var['type']=='string' or var['type']=='char':
        #        if var['default']!=None:
        #            value="'{0}'".format(var['default'])
        #    template_add ("{2}    {0} = {1}".format(variable,value,pad))
        
        args=[]
        if len(classes[_class])>1:
            for variable in classes[_class]:
                if '_arguments' in variable:
                        continue
                args.append(variable+"=None")
            template_add ("")
            template_add ("        def __init__(self,{0}):".format(",".join(args)))
            for variable in classes[_class]:
                if '_arguments' in variable:
                        continue
                template_add ("            if {0}:  self.{0}={0}".format(variable))


     
#        if len(classes[_class])>1 and  class_spec[_class]['parent']!=None:
#        template_add("\n        def debug(self):")
#        template_add("            template_add('  Debug Info: {0}')".format(class_name))
#        for variable in classes[_class]:
#            if variable[0]=='_':
#                continue
#            template_add ("            template_add('  {1:<20} {{0}}'.format(self.{0}))".format(variable,variable+':'))



def variable_def (command,classes,class_spec):
    template_add ("    #variable_def")
    return
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
          #  template_add var
            value=var['default']

            if var['type']=='string' or var['type']=='char':
                if var['default']!=None:
                    value="'{0}'".format(var['default'])
            template_add ("{2}    {0} = {1}".format(variable,value,pad))
        
        args=[]


 #template_add(classes)
    #template_add(class_spec)  
    template_add ("")
    template_add ("    #variable_class_def")
    for _class in classes:

        if len(classes[_class])>1:
            class_name="_{0}()".format(_class)
        else:
            class_name=''

        if class_spec[_class]['parent']!=None:
                continue

        #if class_spec[_class]['optional']:
        #    if '_arguments' in classes[_class] or  class_spec[_class]['storage']=='array':
        #        class_name='[ {0} ]'.format(class_name)
        #    template_add ("    {0:<20} = None        # optional {1}".format(_class.replace(" ","_"),class_name))
        #    continue
#
        ##template_add classes[_class]
        #if '_arguments' in classes[_class]:
        #        template_add ("    {0:<20} = []          #          {1}".format(_class.replace(" ","_"),class_name))
        #        continue
#
        #if len(classes[_class])>1:
        #    template_add ("    {0:<20} = _{0}()".format(_class.replace(" ","_")))
        #    continue
#
        #for variable in classes[_class]:
        #    pad=''
        #    var=classes[_class][variable]
        #    value=var['default']
#
        #    if var['type']=='string' or var['type']=='char':
        #        if var['default']!=None:
        #            value="'{0}'".format(var['default'])
        #    template_add ("{2}    {0:<20} = {1}".format(variable,value,pad))



def init(command,classes,class_spec):
    command_name=safe_name(command['name'])
    if len(classes)>0:
        template_add("\n    def __init__(self,so):")
        for _class in classes:
            safe_class=class_spec[_class]['key']
            if len(classes[_class])==1:
                for variable in classes[_class]:
                    if '_arguments' == variable or  class_spec[_class]['parent']!=None:
                        continue;

                    if classes[_class][variable]['storage']=='single' or class_spec[_class]['type']=='single':
                        sqo="meta.gv(so,['meta','{0}'])".format(variable)
                        template_add ("            self.{0} = {1}".format(variable,sqo))
                    else:
                        sqo="meta.gv(so,['meta','{0}','{1}'])".format(safe_class,variable)
                        template_add ("            self.{0} = {1}".format(variable,sqo))
            else:
                var=[]
                var_dict=[]
                if '_arguments' in classes[_class]  or class_spec[_class]['storage']=='array':
                    for variable in classes[_class]:
                            if variable[0]=='_':
                                    continue
                            #template_add classes[_class],variable
                            if class_spec[_class]['storage']=='array':
                                sqo="meta.gv(item,['{1}','{0}'])".format(variable,safe_class)
                                sqo2="meta.gv(item,[instance_type,'{0}'])".format(variable)
                            else:
                                sqo="meta.gv(item,['{0}'])".format(variable)
                                sqo2="meta.gv(item,['{0}'])".format(variable)
                            var.append("{1} = {0}".format(sqo,variable))    
                            var_dict.append("'{1}': {0}".format(sqo2,variable))    
                else:
                    for variable in classes[_class]:
                        if variable[0]=='_':
                                continue
                        #template_add classes[_class],variable
                        
                       # if classes[_class][variable]['storage']=='single' or class_spec[_class]['type']=='single':
                       #     sqo="meta.gv(so,['{2}','{1}'])".format(_class,variable,'meta')
                       # else:
                        sqo="meta.gv(so,['{2}','{0}','{1}'])".format(safe_class,variable,'meta')
                        sqo2="meta.gv(so,[{1},instance_type,'{0}'])".format(variable,'meta')
                        var.append("{1} = {0}".format(sqo,variable))    
                        var_dict.append("'{1}' : {0}".format(sqo2,variable))    

                if '_arguments' in classes[_class]  or class_spec[_class]['storage']=='array':
                        #template_add ("            template_add(so)")
                        if class_spec[_class]['type']=='single':
                            template_add ("            if meta.gv(so,['meta','{0}']):".format(safe_class))
                        else:
                            template_add ("            if meta.gv(so,['meta','{0}']):".format(safe_class))
                        template_add ("                self.{0}=[]".format(_class.replace(" ","_")))
                        template_add ("                for item in meta.gv(so,['meta','{0}']):".format(safe_class))
                        template_add ("                    instance_type=item.__slots__[0]")
                        template_add ("                    safe_instance_type='_'+instance_type")
#                        template_add ("                    template_add('*'+safe_instance_type+'*')")
#                        template_add ("                    template_add('*'+instance_type+'*')")
#                        template_add ("                    template_add(item)")
                        template_add ("                    self.{0}.append( type(safe_instance_type,(),{{ {1} }}) )".format(_class.replace(" ","_"),",".join(var_dict)))
                else:
                    if class_spec[_class]['parent']==None:
                        template_add ("            if meta.gv(so,['meta','{0}']):".format(safe_class))
                        template_add ("                self.{0}= self._{0}({1})".format(_class.replace(" ","_"),",".join(var)))
    else:
        template_add("\n    def __init__(self,so):")
        template_add("        a=0 # holder")
        template_add("")
                



def debug(command,classes,class_spec):  
    template_add("    def debug(self):")
    template_add("        meta.debugger(self,'{0}')".format(command['name']))

    #command_name=command['name'].replace(' ','_')
    #if len(classes)>0:
    #    template_add("")
    #    template_add("    def debug(self):")
    #    template_add("        template_add('Debug Info: {0}')".format(command_name))
    #    for _class in classes:
    #        class_name=_class.replace(' ',"_")
    #        #$template_add len(classes[_class])
    #        if len(classes[_class])<2:
    #            for variable in classes[_class]:
    #                if '_arguments' == variable or  class_spec[_class]['parent']==None:
    #                    if variable[0]=='_':
    #                        continue
    #                    template_add ("        template_add('{1:<20} {{0}}'.format(self.{0}))".format(variable,variable+':'))
    #        else:
    #            #template_add class_spec
    #            if class_spec[_class]['parent']:
    #                continue
    #            template_add("        if self.{0}:".format(class_name))
    #            if class_spec[_class]['storage']=='array' or  '_arguments' in classes[_class]:
    #                pad="    "
    #                name='item'
    #                template_add("            for item in self.{0}:".format(class_name))
    #                template_add("{1}            {0}.debug()".format(name,pad))
    #            else:
    #                name=class_name
    #                pad=""
    #                template_add("{1}            self.{0}.debug()".format(name,pad))
    #            template_add("        else:".format(pad))
    #            template_add("            template_add('{1:<20} {{0}}'.format(self.{0}))".format(class_name,class_name+':',pad))
    #else:
    #    template_add("\n    def __init__(self,so=None):")
    #    template_add("          a=1")
    #    template_add("")
    #    template_add("    def debug(self):")
    #    template_add("        template_add('Debug Info: {0}')".format(command_name))
    #    template_add("        template_add('No variables')")



def meta_str():
    template_add("""
def convert_to_class(self,o):
    """)

    index=0
    for command in language['commands']:
        if index==0:
            el=""
        else:
            el="el"
        index+=1
        command_name=command['name'].replace(' ','_')
        template_add ("    {1}if o['mode']=='{0}': return self.{2}(o)".format(command['name'],el,safe_name(command_name)))
        

    template_add("""
    return None
""")
