# cython: linetrace=True

class factory_json:
    def dumps(self,data):
        output_string=self.render(data)
        return output_string


    def props(cls):   
        return [i for i in cls.__dict__.keys() if i[:1] != '_']

    def render(self,obj,depth=0):
        """json like output for python objects, very loose"""
        unk_template='"???{0}???"'
        str_template='"{0}"'
        int_template="{0}"
        float_template="{0}"
        bool_template="{0}"
        array_template='['+'{0}'+']'
        tuple_template='"{0}":{1}'
        object_template='{{'+'{0}'+'}}'
        fragment=""
        if None == obj:
            return fragment

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
                partial.append(self.render(item,depth=depth+1))
            if len(partial)>0:
                fragment+=array_template.format(",".join(map(str, partial)))
        elif isinstance(obj,class):
            items=self.props(obj)
            for item in items:
                partial.append(tuple_template.format(item,self.render( obj[item],depth=depth+1)))

        elif isinstance(obj,object):
            partial=[]
            for item in obj:
                partial.append(tuple_template.format(item,self.render(obj[item],depth=depth+1)))
            if len(partial)>0:
                fragment+=object_template.format(",".join(map(str, partial))) 
        else:
            fragment+=unk_template.format("UNK",obj)
        return fragment

