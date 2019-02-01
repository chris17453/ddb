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

