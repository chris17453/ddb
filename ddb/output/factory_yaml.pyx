


def yamlf_load(data=None,file=None):
    factory=factory_yaml()
    return factory.load(data=data,file=file)

def yamlf_dump(data=None,file=None):
    factory=factory_yaml()
    factory.dump(data=data,file=file)

def yamlf_dumps(data=None,file=None):
    factory=factory_yaml()
    result=factory.dumps(data=data,file=file)
    return result

class factory_yaml:
    debug=False
    def __init__(self,debug=None):
        self.debug=debug
    
    def info(self,data,msg):
        if self.debug:
            print("{0} : {1}".format(msg,data))

    # ##########################################################################
    # Encode Yaml
    # ##########################################################################
    TODO So got dump and dumps wrong fix so file either loads or saves.....
    def dumps(self,data=None,file=None):
        if None == data:
            data_obj=self.load(data=None,file=file)
            output_string=self.render(data_obj)
            return output_string

        # pass an object, return yaml string
        if not isinstance(data,str):
            output_string=self.render(data)
            return output_string
        else:  
            # pass a string, decode to an object, re-encode to yaml string
            data_obj=self.load(data,file)
            output_string=self.render(data_obj)
            return output_string


    def walk_path(self,path,root):
        obj=root

        # walk the path
        if path and len(path)>0:
            for trail in path:
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
                    return {'key':key,'type':'list','obj':fragment,'depth':len(sub_path)}
        elif isinstance(fragment,dict):
                    return {'key':key,'type':'dict','obj':fragment,'depth':len(sub_path)}
        return None        
                    
    def get_next_obj_path(self,path,root):
        fragment=self.walk_path(path,root)
        
        #last_path=path.pop()
        # get next object in path
        if isinstance(fragment,list):
            for i,value in enumerate(fragment):
                path.append(i)
                return {'key':i,'type':'list','obj':value,'depth':len(path)}

        elif isinstance(fragment,dict):
            for i in fragment:
                path.append(i)
                return {'key':i,'type':'dict','obj':fragment[i],'depth':len(path)}
            

        # is this a simple entity?
        # if so, backup 1 level, and proceed to the next item
        #remove this last bit of path
        while len(path)>0:
            last_path=path.pop()
            
            if len(path)==0:
                temp_obj=root
            else:
                temp_obj=self.walk_path(path,root)
            
            # get the next path
            grab_next=None
            if isinstance(temp_obj,list):
                for i,value in enumerate(temp_obj):
                    if grab_next:
                        path.append(i)
                        return {'key':i,'type':'list','obj':value,'depth':len(path)}

                    if i==last_path:
                        grab_next=True


            elif isinstance(temp_obj,dict):
                for i in temp_obj:
                    value=temp_obj[i]
                    if grab_next:
                        path.append(i)
                        return {'key':i,'type':'dict','obj':value,'depth':len(path)}

                    if i==last_path:
                        grab_next=True
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
        last_fragment=None
        arr_depth=0
        newline=False
        fragment=True
        while fragment!=None:
            fragment=self.get_next_obj_path(path,root)
            parent_fragment=self.get_parent_obj(path,root)

            # end of decoding            
            if None ==fragment:
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
            if fragment['type']=='dict':
                if newline==0:
                    if len(line)>0:
                       lines.append(line)
                    line=self.padding(len(path),indent,arr_depth)
                else:
                    newline=0
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
            
            if not isinstance(obj,list) and not  isinstance(obj,dict):
                if obj==None:
                    line+="null"
                elif obj==True:
                    line+="True"
                elif obj==False:
                    line+="False"
                else:
                    line+="{0}".format(obj)

                if len(line)>0:
                    lines.append(line)
                line=""
                newline=0
            last_fragment=fragment

        return '\n'.join(lines)


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
        if data=="true" or data== 'True':
            return True
        if data=="false" or data== 'False':
            return False
        if data=="null" or data== 'Null':
            return None
        if data=="[]":
            return None
        if data=="{}":
            return None
        return data
        
    def dump(self,data=None,file=None):
        if not isinstance(data,str):
            data=self.render(data)
        else:  
            data=self.load(data,file)
        #print(data)

    def load(self,data=None,file=None):
        if file:
            with open(file) as content:
                data=content.read()

        lines=data.splitlines()
        root={}
        last_indent=None
        obj=root
        hash_map=[{'indent':0,'obj':obj}]
        obj_parent=root
        obj_parent_key=None
        obj_hash=[]
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