
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



    # initally pass a string,
    # after which it becomes a dict holding eveything
    

    def yaml_load(self,data):
        print("Loading")
        lines=data.splitlines()
        
        root={}
        last_indent=None
        group={}
        line_number=1
        obj=root
        hash_map=[{'indent':0,'obj':obj}]
        in_array=False
        feed_me_an_object=None

        for line in lines:
            if self.yaml_is_start(line):
                print("Starting")
                continue
            if self.yaml_is_end(line):
                print("End")
                break
            indent=self.get_indent(line)

            if feed_me_an_object and last_indent==indent:
                raise Exception("Empty tuple before: {0}:{1}".format(line_number,line))

            print("THIS  indent {0}: last indent: {1}".format(indent,last_indent))
            line_cleaned=line.strip()
            is_array=self.yaml_is_array(line_cleaned)
            line_cleaned=self.yaml_strip_array(line_cleaned)
            

            # ok, forward walking is automatic, and requires no map.
            # when an indernt drops, the map is popped

            if  not isinstance(obj,list) and is_array:
                print ("In new array setup")
                in_array=True
                print obj
                obj[last_tuple['key']]=[]
                # now the mind warp, take me back to some linked list action here
                # repoint the object brah
                obj=obj[last_tuple['key']]
                
                hash_map.append({'indent':indent,'obj':obj})
                


            if 0==0:
                if last_indent and  last_indent>indent or is_array:
                    #    obj={}
                    #else:
                    #    obj={}
                    found_it=None
                    #print "Hash"
                    #print hash_map
                    #print "ROOT"
                    #print (root)
                    print "*",line
                    for index in range(len(hash_map)-1,-1,-1):
                        #print index
                        offset=0
                        if is_array:
                            print("is array")
                            if hash_map[index]['indent']==indent:
                                #print(hash_map)
                                print("Found indent {0}".format(hash_map[index]['indent']))
                                obj=hash_map[index]['obj']
                                print (obj)
                                found_it=True
                                break;
                        else:
                            print("is not array")
                            if hash_map[index]['indent']<=indent:
                                #print(hash_map)
                                print("Found indent {0}".format(hash_map[index]['indent']))
                                obj=hash_map[index]['obj']
                                print (obj)
                                found_it=True
                                break;
                    if isinstance(obj,list):
                        print("its a list, make array")
                        in_array=True
                    else:
                        print("its a list, REMOVE array")
                        in_array=None
                    if found_it == None:
                        print ("Didnt Find it")
                        pprint(root)
                    else:
                        feed_me_an_object=None



            

                            
   
            # is it a tuple?
            line_tuple=self.yaml_get_tuple(line_cleaned)
            if line_tuple:
                if None == obj:
                    raise Exception("Object leak")
                print (line_tuple)

                if line_tuple['data'] and isinstance(obj,list):
                   feed_me_an_object=True 

                if feed_me_an_object:
                    if isinstance(obj,list):
                        a={}
                        obj.append(a)
                        # now the mind warp, take me back to some linked list action here
                        # repoint the object brah
                        obj=a
                    else:
                        print last_tuple
                        obj[last_tuple['key']]={}
                        # now the mind warp, take me back to some linked list action here
                        # repoint the object brah
                        obj=obj[last_tuple['key']]
                    hash_map.append({'indent':indent,'obj':obj})
                    feed_me_an_object=None


                # ok its a tuple... and it has data. lets just add it.
                if line_tuple['data']:
                    print (line_tuple['key'])
                    obj[line_tuple['key']]=line_tuple['data'].strip()
                    feed_me_an_object=None

                 #well darn, no data. guess the next object is the data...
                else:
                     
                     feed_me_an_object=True
                last_tuple=line_tuple
            else:
                print("Not tuple")
                if isinstance(obj,list):
                    print ("adding thing")
                    obj.append(line_cleaned.strip())
                    feed_me_an_object=None
                else:
                    raise Exception("Cant have free standing data with no parent")


            line_number+=1
            last_indent=indent
            
        print ("Exit recursion. END")
        return root
 


data={}
data['array']=[0,2,3,4]
data['group']={}
data['array2']={}
data['array2']['arr1']=[6,7,8]
data['array2']['arr2']=[9,8,7,6,"number",4,3,2,1,0,3,4,3]
op={}
op['sddc']='roc'
op['vcenter']="1"
op['cloudgw']=1.2
data['group']['operations']=op
#data['arr']=[]
#data['arr'].append([2,3,4])
#data['arr'].append([5,6,7])
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
yaml_data = of.render_yaml(data,indent=5)
#print json_data
#print xml_data
print yaml_data

yaml_object=of.yaml_load(yaml_data)

print "----------X"
print "----------X"


pprint(yaml_object)

