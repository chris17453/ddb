# cython: linetrace=True

def yamlf_load(data=None,file=None):
    factory=factory_yaml()
    return factory.load(data=data,in_file=file)

def yamlf_dump(data=None,file=None):
    factory=factory_yaml()
    return factory.dump(data=data,out_file=file)

class factory_yaml:
    debug=True
    def __init__(self,debug=None):
        self.debug=debug
    
    def info(self,msg,data):
        if self.debug:
            print("{0} : {1}".format(msg,data))

    # ##########################################################################
    # Encode Yaml
    # ##########################################################################


    def walk_path(self,path,root):
        obj=root

        # walk the path
        if path and len(path)>0:
            for trail in path:
                if hasattr(obj, '__dict__'):
                    obj=getattr(obj,trail)
                else:
                    obj=obj[trail]

        return obj
        
    def get_parent_obj(self,path,root): 
        if len(path)<2:
            return None
        sub_path=path[0:-1]
        #print (".".join([str(i) for i in sub_path]),"--",".".join([str(i) for i in path]))
        fragment=self.walk_path(sub_path,root)

        if isinstance(fragment,list):
            if len(sub_path)<1:
                return None
            sub_path=sub_path[0:-1]
            #print (".".join([str(i) for i in sub_path]),"--",".".join([str(i) for i in path]))
            fragment=self.walk_path(sub_path,root)


        key=""#sub_path[-1]
        if isinstance(fragment,list):
            self.info("Yaml-Get Parent Object","In List")
            return {'key':key,'type':'list','obj':fragment,'depth':len(sub_path)}
        elif isinstance(fragment,dict):
            self.info("Yaml-Get Parent Object","In Dict")
            return {'key':key,'type':'dict','obj':fragment,'depth':len(sub_path)}
        elif hasattr(fragment, '__dict__'):
            self.info("Yaml-Get Parent Object","In Class")
            return {'key':key,'type':'dict','obj':fragment,'depth':len(sub_path)}
            
        return None        
                    
    def get_next_obj_path(self,path,root):
        self.info("Yaml","Walking")
        fragment=self.walk_path(path,root)
        self.info("Path", ".".join([ str(arr) for arr in path]))
        #last_path=path.pop()
        # get next object in path
        # this is where we walk forward
        if isinstance(fragment,list):
            #if len(fragment)==0:
            #    path.append(None)
            #    return {'key':None,'type':'list','obj':[],'depth':len(path)}
            for i,value in enumerate(fragment):
                self.info("Yaml","List:{0}".format(i))
                path.append(i)
                return {'key':i,'type':'list','obj':value,'depth':len(path)}

        elif isinstance(fragment,dict):
            for i in fragment:
                self.info("Yaml","Dict:{0}".format(i))
                path.append(i)
                return {'key':i,'type':'dict','obj':fragment[i],'depth':len(path)}

        elif hasattr(fragment, '__dict__'):
            self.info("Yaml","In Class")
            
            for key in fragment.__dict__.keys():
                self.info("Yaml","Class:{0}".format(key))
                value=getattr(fragment,key)

                path.append(key)
                return {'key':key,'type':'class','obj': value,'depth':len(path)}
        
        # this is where we back up
        # is this a simple entity?
        # if so, backup 1 level, and proceed to the next item
        #remove this last bit of path
        self.info("Yaml","Cant go deeper")
        while len(path)>0:
            self.info("Yaml","loop - looking {0}".format(len(path)))
        
            last_path=path.pop()
            
            if len(path)==0:
                temp_obj=root
            else:
                temp_obj=self.walk_path(path,root)
            
            # get the next path
            grab_next=None
            if isinstance(temp_obj,list):
                self.info("Yaml","Next - In List")
                for i,value in enumerate(temp_obj):
                    if grab_next:
                        path.append(i)
                        return {'key':i,'type':'list','obj':value,'depth':len(path)}

                    if i==last_path:
                        grab_next=True


            elif isinstance(temp_obj,dict):
                self.info("Yaml","Next - In Dict")
                for i in temp_obj:
                    value=temp_obj[i]
                    if grab_next:
                        path.append(i)
                        return {'key':i,'type':'dict','obj':value,'depth':len(path)}

                    if i==last_path:
                        grab_next=True


            elif hasattr(temp_obj, '__dict__'):
                self.info("Yaml","Next - In Class")
                
                for key in temp_obj.__dict__.keys():
                    self.info("Yaml","Attr:{0}".format(key))
                    value=getattr(temp_obj,key)

                    if grab_next:
                        path.append(key)
                        return {'key':key,'type':'class','obj':value,'depth':len(path)}

                    if key==last_path:
                        grab_next=True
            self.info("Yaml","Didnt find it")
        return None

    def padding(self,indent,indent_spacing,array_depth=0):
        padding=""
        indent=indent-1
        if indent_spacing<=0:
            indent_spacing=1
        column_indent=(indent-array_depth)
        if column_indent<0:
            column_indent=0
        pad_len=column_indent*indent_spacing+array_depth*2
        for i in range(0,pad_len):
            padding+=" "
        return padding

    def render(self,data_obj,indent=0):
        obj=data_obj
        root=data_obj
        path=[]
        line=""
        lines=[]
        last_fragment={'depth':0}
        arr_depth=0
        newline=False
        fragment=True
        while fragment!=None:
            self.info("Yaml-Render","Start Loop")

            fragment=self.get_next_obj_path(path,root)
            parent_fragment=self.get_parent_obj(path,root)

            # end of decoding            
            if None ==fragment:
                self.info("Yaml-Render","NONE skipping")
                continue

            if  fragment['type']!='list':
                arr_depth=0
            if parent_fragment:
                if  parent_fragment['type']!='list':
                    arr_depth=0
                if  parent_fragment['type']=='list' and fragment['type']=='list' and last_fragment['depth']<fragment['depth']:
                    arr_depth+=1
                if  parent_fragment['type']=='list' and fragment['type']=='list' and last_fragment['depth']>fragment['depth']:
                    arr_depth-=1

            obj=fragment['obj']
            if fragment['type']=='class':
                self.info("Yaml-Render",'Its a class')
                if newline==0:
                    if len(line)>0:
                       lines.append(line)
                    line=self.padding(len(path),indent,arr_depth)
                else:
                    newline=0
                line+="{0}: ".format(fragment['key'])#+""+str(arr_depth)+'-'+str(len(path))+"-"+str(indent)

            if fragment['type']=='dict':
                if newline==0:
                    if len(line)>0:
                       lines.append(line)
                    line=self.padding(len(path),indent,arr_depth)
                else:
                    newline=0
                if not fragment['key']:
                    line+="{0}: -{1}".format(fragment['key'],'{'+'}')#+""+str(arr_depth)+'-'+str(len(path))+"-"+str(indent)
                else:
                    line+="{0}: ".format(fragment['key'])#+""+str(arr_depth)+'-'+str(len(path))+"-"+str(indent)
                
            if fragment['type']=='list':
                if parent_fragment and fragment:
                    if parent_fragment['type']!='list' and  fragment['key']==0:
                        if len(line)>0:
                            lines.append(line)
                        line=self.padding(len(path)-1,indent,arr_depth)#+"("+str(arr_depth)+'-'+str(len(path))+"-"+str(indent)+")"

                    elif  fragment['key']!=0:
                        if len(line)>0:
                            lines.append(line)
                        line=self.padding(len(path)-1,indent,arr_depth)#+"("+str(arr_depth)+'-'+str(len(path))+"-"+str(indent)+")"

                line+="- "
                newline=1
            # can't handle in object walker because the container is empty
            if isinstance(obj,list) and len(obj)==0:
               line+="[]"
            if isinstance(obj,dict) and not obj:
               line+="{}"
            #else:
            if not isinstance(obj,list) and not  isinstance(obj,dict) and not hasattr(obj,'__dict__'):
                if obj==None:
                    line+="null"
                elif isinstance(obj,int):
                    line+="{0}".format(obj)
                elif obj==True:
                    line+="true"
                elif obj==False:
                    line+="false"
                elif isinstance(obj,str):
                    obj=obj.replace("'","''")
                    obj=obj.replace("\"","\\\"")
                    
                    line+="'{0}'".format(obj)
                else:
                    line+="{0}".format(obj)

                if len(line)>0:
                    lines.append(line)
                line=""
                newline=0
            last_fragment=fragment
        if line: 
            lines.append(line)
        document='\n'.join(lines)
        #print(document)
        return document


    # ##########################################################################
    # Decode Yaml
    # ##########################################################################

 
    def get_indent(self,line):
        index_of=line.find('- ')

        cleaned_line=line
        index=len(line)-len(cleaned_line.lstrip())
        if index_of!=-1:
            index+=1
        
        return index

    def is_start(self,line):
        # the beginning
        if line=='---':
            return True
        return None

    def is_end(self,line):
        if line=='...':
            return True
        return None

    def is_array(self,line_cleaned):
        """determine if a string begins with an array identifyer '- '"""
        if None==line_cleaned:
            return False
        # we need a dash and a space. double dashes dont work etc...
        if len(line_cleaned)>1:
            if line_cleaned[0]=='-' and line_cleaned[1]==' ':
                return True
        return False
        
    def strip_array(self,line):
        """Strip array elements from string '- '"""
        index_of=line.find('- ')
        if index_of!=-1:
            str1=list(line)
            str1[index_of]=' '
            line="".join(str1)
        return line

    def is_comment(self,line):
        cleaned=line.lstrip()
        if len(cleaned)>0:
            if cleaned[0]=='#':
                return True
        return False

    def get_tuple(self,line):
        if self.is_comment(line):
            return None
        """Get key value pair from string with a colon delimiter"""
        index=line.find(':')
        if index==-1:
            return None
        
        key=self.return_data(line[0:index])
        data_index=index+1
        if data_index<len(line):
            data=line[data_index:].strip()
        else:
            data=None
        return {'key':key,'data':data}

    def return_data(self,data):
        
        data=data.strip()
        #maybe its quoted
        if len(data)>2:
            quoted=None
            if data[0]=="'" and data[-1]=="'":
                quoted=True
            if data[0]=='"' and data[-1]=='"':
                quoted=True
            if quoted:
                return data[1:-1]
        try:
            return int(data)
        except ValueError:
            pass
        try:
            return float(data)
        except ValueError:
            pass
        if data=="true" or data== 'yes' or data== 'Yes':
            return True
        if data=="false" or data== 'no' or data== 'No':
            return False
        if data=="null":
            return None
        if data=="[]":
            return []
        if data=="{}":
            return {}
        return data
        
    def dump(self,data=None,out_file=None):
        if isinstance(data,str):
            raise Exception ("yaml dump requires an object, not a string")
        yaml_data=self.render(data)

        if out_file:
            yaml_file=open(out_file, 'w')
            try:
                yaml_file.write(yaml_data)
            finally:
                yaml_file.close()
        else:
            return yaml_data

        #print(data)

    def load(self,data=None,in_file=None):
        if in_file:
            content=open(in_file)
            try:
                data=content.read()
            finally:
                content.close()

        lines=data.splitlines()
        root={}
        last_indent=None
        obj=root
        hash_map=[{'indent':0,'obj':obj}]
        obj_parent=root
        obj_parent_key=None
        obj_hash={}
        for line in lines:
            if self.is_start(line):
                continue
            if self.is_end(line):
                break
            indent=self.get_indent(line)

            line_cleaned=line
            is_array=self.is_array(line_cleaned.strip())
        
            
            # I handle array creation            
            if  is_array:
                self.info("Encode","Create Array Index")
                line_cleaned=self.strip_array(line_cleaned)
                line=line_cleaned
                arr_index=0
                while is_array:
                    make_new_array=True
                    if None==obj:
                        self.info("Encode-Array","made a new object at start (root index) @ {0}".format(len(hash_map)))
                        obj_parent[obj_parent_key]=[]
                        obj=obj_parent[obj_parent_key]
                        obj_hash['obj']=obj
                        obj_hash['indent']=indent
                        make_new_array=None
                        
                    elif arr_index==0:
                        for index in range(len(hash_map)-1,-1,-1):
                            # the search can only fall coreward, never grow.
                            if hash_map[index]['indent']==indent and isinstance(hash_map[index]['obj'],list):
                                obj=hash_map[index]['obj']
                                make_new_array=None
                                self.info("Encode-Array","Found  object")
                        
                                break
                    if make_new_array:
                        if isinstance(obj,list):
                            self.info("Encode","Made a new object")
                        
                            new_list=[]
                            obj.append(new_list)
                            obj=new_list
                            hash_map.append({'indent':indent,'obj':obj})
                        # TODO this may never happen. 
                        else:
                            obj=[]
                    line_cleaned=line
                    indent=self.get_indent(line)
                    is_array=self.is_array(line_cleaned.strip())
                    if is_array:
                        line_cleaned=self.strip_array(line_cleaned)
                        line=line_cleaned
                    arr_index+=1
                indent=self.get_indent(line)
            else:
                # I handle indent shrinkage, loading the last indent level object
                # shrinkage requires object location....
                if last_indent and  last_indent>indent:
                    found=None
                    for index in range(len(hash_map)-1,-1,-1):
                        if hash_map[index]['indent']<=indent:
                            obj=hash_map[index]['obj']
                            self.info("Encode","Found it: {0}".format(index))
                            found=True
                            break
                    if None==found:
                        self.info("Encode","Didn't Find it")
                
                    
                            
            # i handle object creation
            # is it a tuple?
            line_tuple=self.get_tuple(line_cleaned)
            if line_tuple:
                self.info("Encode","In Tuple :{0}".format(line_tuple['key']))
                if None == obj:
                    self.info("Encode","OBJ needs ")
                    obj_parent[obj_parent_key]={}
                    obj=obj_parent[obj_parent_key]
                    obj_hash['obj']=obj
                    obj_hash['indent']=indent

                if isinstance(obj,list):
                    new_obj={}
                    obj.append(new_obj)
                    obj_parent=obj
                    obj_parent_key=len(obj)-1
                    obj=new_obj
                    obj_hash={'indent':indent,'obj':obj}
                    hash_map.append(obj_hash)

                # ok its a tuple... and it has data. lets just add it.
                if line_tuple['data']:
                    value=self.return_data(line_tuple['data'])
                    obj[line_tuple['key']]=value
                # well darn, no data. guess the next object is the data...
                else:
                    if  not isinstance(obj,list):
                        self.info("Encode","no tuble value")
                        obj[line_tuple['key']]=None
                        obj_parent=obj
                        obj_parent_key=line_tuple['key']
                        obj=obj[line_tuple['key']]
                        obj_hash={'indent':indent,'obj':obj}
                        hash_map.append(obj_hash)
            else:
                # skip comments
                if self.is_comment(line):
                    continue

                if isinstance(obj,list):
                    value=self.return_data(line_cleaned)
                    obj.append(value)
            last_indent=indent
        return root











#from pprint import pprint
##if __name__ == "__main__":
#pprint( yamlf_load(file="/home/nd/.ddb/main/test.ddb.yaml"))

#class sub:
#    def __init__(self):
#        self.su1=1
#        self.s2=1
#        self.s3="domo"
#        
#class test:
#
#    def __init__(self):
#        self.pizza=1
#        self.beer=1
#        self.s4=sub()
#        self.a3=sub()
#        self.aouse="domo"
#print "--"
#pprint(test().__dict__)
#
#
#data={}
#data['arr_empty']=[]
#data['dict_empty']={}
#data['arr']=[1,2,3,4]
#data['arr2']=[[1,2,3,4],[5,6,7,8]]
#data['dict']=[{'sam':'bob'}]
#data['class']=test()
#yaml_data=yamlf_dump(data=data)
#pprint( yamlf_load(data=yaml_data))

