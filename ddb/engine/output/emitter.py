
from pprint import pprint



class obj_formatter():
    def render_xml(self,obj,root='root',depth=0):
        """xml like output for python objects, very loose"""
        template="""<{0}>{1}</{0}>"""
        fragment=""
        if isinstance(obj,str):
            fragment+=template.format(root,obj)

        elif isinstance(obj,int):
            fragment+=template.format(root,obj)

        elif isinstance(obj,float):
            fragment+=template.format(root,obj)
        
        elif isinstance(obj,bool):
            fragment+=template.format(root,obj)
        elif  isinstance(obj,list):
            for item in obj:
                fragment+=self.render_xml(item,root=root,depth=depth+1)
        elif isinstance(obj,object):
            for item in obj:
                fragment+=self.render_xml(obj[item],root=item,depth=depth+1)
        else:
            fragment+=template.format("UNK",obj)

        if depth==0:
            fragment=template.format("root",fragment)
        return fragment


    def render_json(self,obj,depth=0):
        """json like output for python objects, very loose"""
        str_template='"{0}"'
        int_template="{0}"
        float_template="{0}"
        bool_template="{0}"
        array_template='['+'{0}'+']'
        tuple_template='"{0}":{1}'
        object_template='{{'+'{0}'+'}}'
        fragment=""
        if isinstance(obj,str):
            fragment+=str_template.format(obj)

        elif isinstance(obj,int):
            fragment+=int_template.format(obj)

        elif isinstance(obj,float):
            fragment+=float_template.format(obj)
        
        elif isinstance(obj,bool):
            fragment+=bool_template.format(obj)
        elif  isinstance(obj,list):
            partial=[]
            for item in obj:
                partial.append(self.render_json(item,depth=depth+1))
            if len(partial)>0:
                fragment+=array_template.format(",".join(map(str, partial)))
        elif isinstance(obj,object):
            partial=[]
            for item in obj:
                partial.append(tuple_template.format(item,self.render_json(obj[item],depth=depth+1)))
            if len(partial)>0:
                fragment+=object_template.format(",".join(map(str, partial))) 
        else:
            fragment+=template.format("UNK",obj)
        return fragment


    def render_yaml(self,obj,depth=0,indent=1):
        """Yaml like output for python objects, very loose"""
        padding=''
        for i in range(0,depth*1):
            padding+=' '

        str_template="{0}"
        int_template="{0}"
        float_template="{0}"
        bool_template="{0}"
        array_template='- {0}'
        tuple_template='{0}: {1}'
        object_template='{0}'
        yaml_template='---\n{0}\n...'
        fragments=[]
        no_padding=False
        if isinstance(obj,str):
            no_padding=True
            fragments.append(str_template.format(obj))
        elif isinstance(obj,int):
            no_padding=True
            fragments.append(int_template.format(obj))
        elif isinstance(obj,float):
            no_padding=True
            fragments.append(float_template.format(obj))
        elif isinstance(obj,bool):
            no_padding=True
            fragments.append(bool_template.format(obj))
        elif  isinstance(obj,list):
            for item in obj:
                fragment=self.render_yaml(item,depth=depth+1,indent=indent)
                if len(fragment)==1:
                    fragments.append(array_template.format(item,fragment[0]))
                else:
                    index=0
                    for partial in fragment:
                        if index==0:
                            fragments.append(array_template.format(partial.lstrip(),""))
                            index+=1
                        else:
                            fragments.append(partial)
                            
        elif isinstance(obj,object):
            for item in obj:
                fragment=self.render_yaml(obj[item],depth=depth+1,indent=indent)
                if len(fragment)==1:
                    fragments.append(tuple_template.format(item,fragment[0]))
                else:
                    fragments.append(tuple_template.format(item,""))
                    for partial in fragment:
                        fragments.append(partial)
        else:
            fragments.append(template.format("UNK",obj))

        if depth==0:
            return yaml_template.format("\n".join(fragments))

        if no_padding==False:
            padding=""
            for i in range(0,indent): 
                padding+=" "
            padded_fragments=[]
            for f in fragments:
                padded_fragments.append(padding+f)
            return padded_fragments

        return fragments

    def get_indent(self,line):
        index_of=line.find('-')
        if index_of!=-1:
            str1=list(line)
            str1[index_of]=' '
            cleaned_line="".join(str1)
        else:
            cleaned_line=line
        index=len(line)-len(cleaned_line.lstrip())
        return index

    def yaml_is_start(self,line):
        # the beginning
        if line=='---':
            print("New object")
            return True
        return None

    def yaml_is_end(self,line):
        if line=='...':
            print ("Exit recursion. Explicit EOL")
            return True
        return None

    
    def yaml_is_array(self,line_cleaned):
        if line_cleaned[0]=='-':
            return True
        return False
        
    def yaml_strip_array(self,line):
        index_of=line.find('-')
        if index_of!=-1:
            str1=list(line)
            str1[index_of]=' '
            line="".join(str1)
        return line

    def yaml_indent_changed(self,s):
        if s['indent']>s['curent_indent']:
            print("Exit recursion. Indent dropped")
            return True
        if s['indent']<s['curent_indent'] and s['changed']==1:
            print("Exit recursion. Indent increased")
            return True
        return None


    def yaml_get_tuple(self,line):
        index=line.find(':')
        if index==-1:
            return None
        
        key=line[0:index]
        data_index=index+1
        if data_index<len(line):
            data=line[data_index:].strip()
        else:
            data=None
        return {'key':key,'data':data}

    def recurse(self,s):
        temp_s=s
        if isinstance(s['obj'],list):
            temp_s['in_array']=True
        else:
            temp_s['in_array']=None
        
        yaml_data=self.yaml_load(temp_s)
        
        if isinstance(s['obj'],list):
            print("Its a list")
            s['obj'].append(yaml_data['results'])
        elif isinstance(s['obj'],object):
            if s['tuple']==None:
                raise Exception("tuple key needed: {0}".format(yaml_data['results']))
            s['obj'][s['tuple']['key']]=yaml_data
        return s


    def update_indent(self,s):
        if s['indent']==None or (s['indent']!=s['curent_indent'] and s['changed']==0):
                s['changed']=1
                s['indent']=s['curent_indent']
        return s

    # initally pass a string,
    # after which it becomes a dict holding eveything
    
    def yaml_load(self,s):
        #print("Recursion: depth: {0},indent:{1}, index:{2}".format(depth,indent,start_index))
        if isinstance(s,str):
            lines=s.splitlines()
            s={}
            s['lines']=lines
            s['length']=len(s['lines'])
            s['index']=0
            s['indent']=0
            s['process_objects']=True
            s['process_arrays']=True
        s['changed']=0
        s['tuple']=None
        s['line_cleaned']=None
        s['obj']={}


        while s['index']  < s['length']:
            recurse=None
            s['line']=s['lines'][s['index']]
            s['line_cleaned']=s['line'].strip()
            s['curent_indent']=self.get_indent(s['line'])

            if self.yaml_is_start(s['line']):
                s['index']+=1
                continue

            if self.yaml_is_end(s['line']):
                return s

       
            if s['process_objects']:
                if ':' in s['line_cleaned']:
                    s['tuple']=self.yaml_get_tuple(s['line_cleaned'])
                    print(s['tuple'])

                    # cat get here/.. just sayin
                    if s['tuple']==None:
                        raise Exception("Tuple invalid")

                    # No value in the tuple, lets recurse and populate with sub object
                    if s['tuple']['data']:
                        if isinstance(s['obj'],list):
                            print("Its a list")
                            s['obj'].append(s['tuple']['data'])
                        elif isinstance(s['obj'],object):
                            s['obj'][s['tuple']['key']]=s['tuple']['data']
                    else:
                        recurse=True
                    s['index']+=1
                
                
                # print "*",key,data,"*"
                # its not an list or object, its a simple element of a list
                else:
                    s['index']+=1
                    #if isinstance(obj,list):
                    #    print ("Exit recursion. single entity")
                    #   obj.append(line_cleaned)
                    s['results']=s['line_cleaned']
                    return s
                    #    return obj
                    #elif isinstance(obj,object):
                    #    obj[key]=data
                #    if not data:        

            # if anything has happened above, an object has been created.
            # now we search for the object and append it...

            s=self.update_indent(s)
            #    recurse=True

            if self.yaml_indent_changed(s) or recurse:
                s=self.recurse(s)
        # end of loop 

        print ("Exit recursion. END")
        return s
 
 
        
#            # this is reached after a recursion from a tuple. so no key
#            # always make it a list override and ignore all else    
#            if 1==1:
#                if self.yaml_is_array(line_cleaned):
#                    #if in_array and start_index!=index:
#                    #    print("Exit recursion. next item in list")
#                    #    self.temp_yaml_index=index
#                    #    return obj
#                    #print("in array")
#                    
#                    #curent_indent=self.get_indent(line)
#                    
#                    lines[index]=self.yaml_strip_array(line)
#                    line_cleaned=lines[index].strip()
#                    
#                    if not isinstance(obj,list):
#                        print ("reset list")
#                        obj=[]
#
#                    obj=self.recurse(lines,index,depth+1,curent_indent,recurse,yaml_tuple,obj)
#                    continue
#
#                          
#            #    #index+=01
#            #    #print "KEY",key
#            #    obj.append(self.yaml_load(lines,index=index,indent=curent_indent+1,depth=depth+1,list_depth=list_depth+1))
#            #    index=self.temp_yaml_index
#            #    #return obj
#            #    list_skip=True
#            
#            
#            
#            #if list_skip:
#            #    print("depth: {0},indent:{1}, index:{2}: cur_indent:{3}, changed:{4}".format(depth,indent,index,curent_indent,changed))
#            #curent_indent=self.get_indent(line)
#            
#            # because i dont want to put the above code in twice...
#            #if list_skip:
#            #    continue
#            
#            if 1==1:
#                if ':' in line_cleaned:
#                    yaml_tuple=self.yaml_get_tuple(line_cleaned)
#
#                    print yaml_tuple
#
#                    # cat get here/.. just sayin
#                    if yaml_tuple==None:
#                        raise Exception("Tuple invalid")
#
#                    # No value in the tuple, lets recurse and populate with sub object
#                    if yaml_tuple['data']:
#                        if isinstance(obj,list):
#                            print("Its a list")
#                            obj.append(yaml_tuple['data'])
#                        elif isinstance(obj,object):
#                            obj[yaml_tuple['key']]=yaml_tuple['data']
#                    else:
#                        recurse=True
#                    index+=1
#                
#                
#                # print "*",key,data,"*"
#                # its not an list or object, its a simple element of a list
#                else:
#                    index+=1
#                    #if isinstance(obj,list):
#                    self.temp_yaml_index=index+1
#                    #    print ("Exit recursion. single entity")
#                    #   obj.append(line_cleaned)
#                    return line_cleaned
#                    #    return obj
#                    #elif isinstance(obj,object):
#                    #    obj[key]=data
#                #    if not data:
#
#
#            # if anything has happened above, an object has been created.
#            # now we search for the object and append it...
#
#            if indent==None or (indent!=curent_indent and changed==0):
#                changed=1
#                indent=curent_indent
#            #    recurse=True
#
#            if self.yaml_indent_changed(s) or recurse:
#                temp_s=self.recurse(s)
#                
#                return s
            

data={}
#data['array']=[0,2,3,4]
data['group']={}
#data['sam']['fred']=[6,7,8]
#data['sam']['sam']=[9,8,7,6,5,4,3,2,1,0,3,4,3]
op={}
op['sddc']='roc'
op['vcenter']="1"
op['cloudgw']=1.2
#data['group']['operations']=op
data['list']=[]
o={}
o['key']='data'
o['key2']='data2'
data['list'].append(o)
data['list'].append(o)

#data['o']['lo'].append(o)


of=obj_formatter()
#json_data = of.render_json(data)
#xml_data  = of.render_xml(data,root='object')
yaml_data = of.render_yaml(data,indent=2)
#print json_data
#print xml_data
print yaml_data

yaml_object=of.yaml_load(yaml_data)

print "----------"
print "----------"


pprint(yaml_object)

