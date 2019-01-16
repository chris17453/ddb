

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

       
    def yaml_load(self,data,obj={},index=0,indent=0,depth=0):
        print("Recursion: depth: {0},indent:{1}, index:{2}".format(depth,indent,index))
        if isinstance(data,str):
            lines=data.splitlines()
        
        elif isinstance(data,list):
            lines=data
        else:
            raise Exception("No clue what that was")

        changed=0
        curent_indent=indent
        line_length=len(lines)
        key=""
        self.temp_yaml_index=0
        while index  < line_length:
            print ("loop: {0}".format(index))
            line=lines[index]
            line_cleaned=line.strip()
            # the beginning
            if line_cleaned=='---':
                print("New object")
                obj={}
                index+=1
                continue

            # the end
            if line_cleaned=='...':
                print ("Exit recursion. Explicit EOL")
                self.temp_yaml_index=index
                return obj

    
            # this is reached after a recursion from a tuple. so no key
            # always make it a list override and ignore all else    
            if line_cleaned[0]=='-':
                print("in array")
                index_of=line.index('-')
                str1=list(line)
                str1[index_of]=' '
                line="".join(str1)
                # HACK
                lines[index]=line
                line_cleaned=line.strip()
                if not isinstance(obj,list):
                    obj=[]
                
                #index+=01
                print "KEY",key
                obj.append(self.yaml_load(lines,index=index,indent=curent_indent+1,depth=depth+1))
                #index=self.temp_yaml_index
            #    is_array=True
            #    obj[key]=yaml_load(lines,index=i+1)

            curent_indent=len(line)-len(line.lstrip())
            print("depth: {0},indent:{1}, index:{2}: cur_indent:{3}, changed:{4}".format(depth,indent,index,curent_indent,changed))

            if indent<curent_indent and changed==0:
                changed=1
                indent=curent_indent
            if indent>curent_indent:
                print("Exit recursion. Indent dropped")
                self.temp_yaml_index=index
                return obj
            if indent<curent_indent and changed==1:
                print("Exit recursion. Indent increased")
                self.temp_yaml_index=index
                return obj


            if ':' in line_cleaned:
                print("In tuple")
                curent_indent=len(line)-len(line.lstrip())
                index_of=line.index(':')
                is_object=True

                #print ("tuple",line_cleaned)
                seperator_index=line_cleaned.index(':')
                key=line_cleaned[0:seperator_index]
                #print seperator_index,len(line_cleaned)
                if seperator_index and seperator_index+1<len(line_cleaned):
                    data=line_cleaned[seperator_index+1:].strip()
                else:
                    index+=1
                    print "B",key,index,key
                    print "OBJECT"
                    data=self.yaml_load(lines,index=index,indent=curent_indent+1,depth=depth+1)
                    index=self.temp_yaml_index
                    print "A",key,index
                if data:
                    print '"{0}"'.format(key)
                    if isinstance(obj,list):
                        obj.append(data)
                    elif isinstance(obj,object):
                        obj[key]=data                     
                    
            
            # print "*",key,data,"*"
            # its not an list or object, its a simple element of a list
            #else:
            #    if isinstance(obj,list):
            #        obj.append(data)
                #elif isinstance(obj,object):
                #    obj[key]=data


            last_indent=indent
            index+=1
            #    if not data:
        print ("Exit recursion. END")
        self.temp_yaml_index=index
        return obj


data={}
data['array']=[0,2,3,4]
#data['sam']={}
#data['sam']['fred']=[6,7,8]
#data['sam']['pete']={}
#data['sam']['pete']['dave']='beer'
#data['sam']['pete']['door']=1
#data['sam']['pete']['float']=1.2
#data['o']={}
#data['o']['lo']=[]
#o={}
#o['l']=3
#o['4']=5
#data['o']['lo'].append(o)
#data['o']['lo'].append(o)


of=obj_formatter()

json_data = of.render_json(data)
xml_data  = of.render_xml(data,root='object')
yaml_data = of.render_yaml(data,indent=2)

print json_data
print xml_data
print yaml_data



print of.yaml_load(yaml_data)
