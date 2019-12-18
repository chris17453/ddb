import re

language_data={
    'segments':[
        {'name':'operators'  , 'single': True, 'store_single': True,'optional' : True, 'children':[
                { 'name' : 'greater_than'       , 'match' : '>'   , 'single' : True, 'store_single' : True },
                { 'name' : 'less_than'          , 'match' : '<'   , 'single' : True, 'store_single' : True },
                { 'name' : 'greater_than_equal' , 'match' : '>='  , 'single' : True, 'store_single' : True },
                { 'name' : 'less_than_equal'    , 'match' : '<='  , 'single' : True, 'store_single' : True },
                { 'name' : 'not_equal'          , 'match' : '!='  , 'single' : True, 'store_single' : True },
                { 'name' : 'not_equal'          , 'match' : '<>'  , 'single' : True, 'store_single' : True },
                { 'name' : 'not'                , 'match' : 'not' , 'single' : True, 'store_single' : True },
                { 'name' : 'equal'              , 'match' : 'is'  , 'single' : True, 'store_single' : True },
                { 'name' : 'like'               , 'match' : 'like', 'single' : True, 'store_single' : True },
                { 'name' : 'equal'              , 'match' : '='   , 'single' : True, 'store_single' : True },
                { 'name' : 'in'                 , 'match' : 'in'  , 'single' : True, 'store_single' : True },
            ]
        },

        {'name':'functions'  , 'single':True,'store_single':True,'children':[
                { 'name' : 'version'  , 'match' : 'version()'       , 'single':True , 'store_single' : True },
                { 'name' : 'date'     , 'match' : 'date()'          , 'single':True , 'store_single' : True },
                { 'name' : 'time'     , 'match' : 'time()'          , 'single':True , 'store_single' : True },
                { 'name' : 'datetime' , 'match' : 'datetime()'      , 'single':True , 'store_single' : True },
                { 'name' : 'count'    , 'match' : 'count()'         , 'single':True , 'store_single' : True },
                { 'name' : 'sum'      , 'match' : 'sum( {column} )' , 'single':True , 'store_single' : True },
                { 'name' : 'avg'      , 'match' : 'avg( {column} )' , 'single':True , 'store_single' : True },
                { 'name' : 'min'      , 'match' : 'min( {column} )' , 'single':True , 'store_single' : True },
                { 'name' : 'max'      , 'match' : 'max( {column} )' , 'single':True , 'store_single' : True },
            ]
        },

        {'name':'data_type' , 'single':True,'optional':True,'children':[
                { 'name' : 'int'      , 'match' : 'int'       , 'single' : True } ,
                { 'name' : 'bool'     , 'match' : 'bool'      , 'single' : True } ,
                { 'name' : 'long'     , 'match' : 'long'      , 'single' : True } ,
                { 'name' : 'float'    , 'match' : 'float'     , 'single' : True } ,
                { 'name' : 'text'     , 'match' : 'text'      , 'single' : True } ,
                { 'name' : 'date'     , 'match' : 'date'      , 'single' : True } ,
                { 'name' : 'time'     , 'match' : 'time'      , 'single' : True } ,
                { 'name' : 'datetime' , 'match' : 'datetime'  , 'single' : True } ,
                { 'name' : 'uuid'     , 'match' : 'uuid'      , 'single' : True } ,
                { 'name' : 'varchar'  , 'match' : '{varchar}' , 'single' : True } ,
            ]
        },


        { 'name': 'table'           , 'match' : '$table' ,'single': True},
        { 'name': 'database'        , 'match' : '$database.', 'single': True, 'optional': True},
        { 'name': 'column'          , 'match' : '$column','single': True},
        { 'name': 'columns'         , 'match' : '{column}'},
        { 'name': 'from'            , 'match' : 'from {db_context}' , 'depends_on': None , 'single': True, 'optional': True},
        { 'name': 'evaluation'      , 'match' : '$expression {operators} $value' , 'single': True},
        { 'name': 'variable'        , 'match' : "@variable", 'single': True},
        { 'name': 'distinct'        , 'match' : "distinct", 'single': True, 'optional': True},
        { 'name': 'db_context'      , 'match':  '{database} {table} {rename}', 'single': True  },

        { 'name': 'sql_expression'  , 'single': True, 'optional': True, 'children' : [ 
                {  'name': 'column '   ,'match': '{column}'                , 'single': True } ,
                {  'name': 'function'  ,'match': '{functions}'             , 'single': True } ,
            ]
        },

        { 'name': 'condition'  , 'single': True, 'optional': True, 'children' : [ 
                {  'name': 'or '  ,'match': 'or'   , 'single': True },
                {  'name': 'and'  ,'match': 'and'  , 'single': True },
                {  'name': 'in'   ,'match': 'in'   , 'single': True },
                {  'name': 'like' ,'match': 'like' , 'single': True },
                {  'name': 'not'  ,'match': 'not'  , 'single': True },
            ]
        },

        { 'name': 'where_condition'  ,'match': '{evaluation}' , 'single': True,'doc_depth': None, 'children' : [
                {  'name': 'where_condition'  ,'match': '{condition}  {evaluation}' }
            ]
        },


        { 'name': 'where'  ,'match': 'where' , 'depends_on': 'from' , 'single': True, 'optional': True, 'children' : [
                {  'name': 'where_condition'  ,'match': '{where_condition}','single': True}
            ]
        },

        { 'name': 'limit'  ,'match': 'limit', 'single': True, 'optional': True, 'children' : [
                { 'name': 'row_count'  ,'match': '$row_count'           , 'single': True, 'optional': True },
                { 'name': 'offset, row_count'  ,'match': '$offset , $row_count'  , 'single': True, 'optional': True },
            ]
        },

        { 'name': 'order'  , 'single': True, 'optional': True, 'children' : [
                {  'name': 'ascending'   ,'match': 'ASC' , 'single': True },
                {  'name': 'descending'  ,'match': 'DESC' , 'single': True },
            ]
        },
            

        { 'name': 'order_by'  ,'match': "order by ", 'single': True, 'optional': True, 'children' : [
                {  'name': 'order_by'  ,'match': '{columns} {order}'}
            ]
        },

        { 'name': 'rename'  ,'match': "as $alias", 'single': True, 'optional': True},

        { 'name': 'select'  ,'match': "select {distinct}", 'single': True, 'children' : [
                { 'name': 'sql_expression'  ,'match': '{sql_expression} {rename}' }
            ]
        },

        { 'name': 'join_type'  , 'single': True, 'children' : [
                {  'name': 'full'   ,'match': 'full'  ,'single': True,  'optional': True},
                {  'name': 'inner'  ,'match': 'inner' ,'single': True,  'optional': True},
                {  'name': 'outer'  ,'match': 'outer' ,'single': True,  'optional': True},
            ]
        },

        { 'name': 'join'  ,'match': "{join_type} join {db_context} on {where_condition}" },
        { 'name': 'value'  ,'match': "$value",'single': True },
        { 'name': 'values'  ,'match': "$values" },
        { 'name': 'assignment_list'  ,'match': "{column} :  {value}" },
        { 'name': 'on_duplicate_key'  ,'match': "on duplicate key {columns} UPDATE {assignment_list}",'single': True, 'optional': True },


        { 'name': 'varchar_options' , 'single': True, 'children' : [
                {  'name': 'max'        ,'match': 'max'     ,'single': True },
                {  'name': 'value'      ,'match': '{value}' ,'single': True },
            ]
        },

        { 'name': 'varchar' ,'match': "varchar ( {varchar_options} )" , 'single': True },
        { 'name': 'column_definition'  ,'match': '{column} {data_type} $default ', 'single': True },


        { 'name': 'boolean' , 'single': True, 'optional': True, 'children' : [
            {  'name': 'true'   ,'match': 'true'  ,'single': True,  'optional': None},
            {  'name': 'false'  ,'match': 'false' ,'single': True,  'optional': None},     
            ]
        },

        { 'name': 'repo'               , 'match':  "repo = $protocol url=$url user=$user password=$password  repo_dir=$directory repo_file=$file", 'single': True,  'optional': True},
        { 'name': 'file'               , 'match':  "file = $file"          , 'single': True,  'optional': True },
        { 'name': 'fifo'               , 'match':  "fifo = $fifo"          , 'single': True,  'optional': True },
        { 'name': 'mode'               , 'match':  "mode = $repo"          , 'single': True,  'optional': True },
        { 'name': 'whitespace'         , 'match':  "whitespace = {$whitespace|boolean}"      , 'single': True,  'optional': True },
        { 'name': 'comments'           , 'match':  "comments = {$comments|boolean}"      , 'single': True,  'optional': True },
        { 'name': 'errors'             , 'match':  "errors = {$errors|boolean}"      , 'single': True,  'optional': True },
        { 'name': 'delimiter'          , 'match':  "delimiter = $delimiter"     , 'single': True,  'optional': True },
        { 'name': 'strict'             , 'match':  "strict = {$strict|boolean}"      , 'single': True,  'optional': True },
        { 'name': 'data_starts_on'     , 'match':  "data_starts_on = $data_starts_on", 'single': True,  'optional': True },
        { 'name': 'assignment'         , 'match':  "{variable} = {value}"},
                
    ],


    'commands':[
        { 'name':'select'              ,'group':'record','match':'{select} \n {from} \n {join} \n {where} \n {order_by} \n {limit}'},
        { 'name':'insert'              ,'group':'record','match':'insert into {db_context} \n ( {columns} ) VALUES ( {values} ) \n {on_duplicate_key}'},
        { 'name':'delete'              ,'group':'record','match':'delete from {db_context} \n where {where_condition}'},
        { 'name':'update'              ,'group':'record','match':'update {db_context} \n set  {assignment_list} \n {where}'},
        { 'name':'begin'               ,'group':'batch' ,'match':'begin'},
        { 'name':'commit'              ,'group':'batch' ,'match':'commit'},
        { 'name':'rollback'            ,'group':'batch' ,'match':'rollback'},
        { 'name':'drop_table'          ,'group':'table' ,'match':'drop {db_context}'},
        { 'name':'create table'        ,'group':'table' ,'match':'create table {db_context} ( {column_definition} ) \n {file} \n {fifo} \n {repo} \n {mode} \n {whitespace} \n {comments} \n {errors} \n {delimiter} \n {strict} \n {data_starts_on} '},
        { 'name':'update table'        ,'group':'table' ,'match':'update table {db_context} ( {column_definition} ) \n {file} \n {fifo} \n {repo} \n {mode} \n {whitespace} \n {comments} \n {errors} \n {delimiter} \n {strict} \n {data_starts_on} '},
        { 'name':'describe table'      ,'group':'table' ,'match':'describe table {db_context}'},        
        { 'name':'show columns'        ,'group':'system','match':'show columns \n from {db_context}'},
        { 'name':'show tables'         ,'group':'system','match':'show tables from {database}'},
        { 'name':'show databases'      ,'group':'system','match':'show databases'},
        { 'name':'show variables'      ,'group':'system','match':'show variables'},
        { 'name':'use'                 ,'group':'system','match':'use database'},
        { 'name':'set'                 ,'group':'system','match':'set {assignment}'},
        { 'name':'show_output_modules' ,'group':'system','match':'show_output_modules'},
    ]
}



class variable:
    name   =None
    db_type=None
    default=None
    options=None
    def __init__(self,name,db_type,default,options):
        self.name     =name
        self.db_type  =db_type
        self.default  =default
        self.options  =options

class segment:
    name         =None
    depends_on   =None
    single       =None
    store_single =None
    optional     =None
    match        =None
    variables    =None
    children     =None
    doc_depth    =None
    group        =None
            
    def __init__(self,name,group=None,match=None,depends_on=None,single=None,store_single=None,optional=None,doc_depth=True):
        self.name         =name
        self.group        =group
        self.depends_on   =depends_on
        self.store_single =store_single
        self.optional      =optional
        self.single        =single
        self.match         =self.create_patern(match)
        self.doc_depth     =doc_depth
    
    def create_patern(self,data):
        if not data:
            return None
        match=re.split('( |,|=|[(]|[)])',data)
        #@print match
        
    
                
        
        return match
    
    def add_children(self,child):
        if self.children==None:
            self.children=[]
        self.children.append(child)
            


                        

class language:
    commands={}
    segments={}
    
    def __init__(self):
       
        for command in language_data['segments']:
            
            self.add_segment( command )    

        ## Commands
        for command in language_data['commands']:
            self.add_command( segment( name=command['name'],group=command['group'],match=command['match'],single=True) )    
        

                        
    def add_command(self,command):
        self.commands[command.name]=command

    
    def make_segment(self,command):
        if 'name'       in command:
            name      =command['name']        
        else: name=None
        if 'group'      in command:
            group     =command['group']       
        else: group=None
        if 'match'      in command:
            match     =command['match']       
        else: match=None
        if 'single'     in command:
            single    =command['single']      
        else: single=None
        if 'optional'   in command:
            optional  =command['optional']    
        else: optional=None
        if 'depends_on' in command:
            depends_on=command['depends_on']  
        else: depends_on=None
        if 'doc_depth' in command:
            doc_depth=command['doc_depth']  
        else: doc_depth=True

        seg=segment( name=name,group=group,match=match,single=single,optional=optional,depends_on=depends_on,doc_depth=doc_depth)
        if 'children' in command:
            if command['children']!=None:
                for child in command['children']:
                    seg.add_children(self.make_segment(child))
        return seg
    
    def add_segment(self,command):
        seg=self.make_segment(command)
        self.segments[seg.name]=seg
        
    def permutate(self,command,is_segment=None,depth=0):
        output=[]
        if command.doc_depth==None:
            return command.name

        if not command.single:
            output.append( "{ ")

        if command.optional:
            output.append("[")

        if command.match:
            last_command=True
            for a in command.match:
                
                if a==None:
                    continue
                if len(a)>=2 and a[0]=='{' and a[-1]=='}':
                    
                    segment=a[1:-1]
                    variable=segment
                    if segment.find('|')>0:
                        variable,segment=a[1:-1].split("|")
                    
                    output.append( self.permutate(self.segments[segment],True,depth+1) )
                    last_command=None
            
                elif len(a)>0 and  a[0]=='$':
                    output.append( "{0}".format(a[1:]) )
                    last_command=True
                else:
                    output.append( "{0}".format(a.upper() ))
                    last_command=True
    
        if command.children:
            options=[]
            delim=" | "

            for child in command.children:
                prefix=" "
                suffix=" "
            
                options.append(prefix+ self.permutate(child,True,depth+1)+suffix )
            output.append(delim.join(options) )

        if command.optional:
            output.append( "]")
        

        if is_segment:
            if not command.single:
                output.append( "} ")
         

        return " ".join(output).replace("  "," ").replace('[ ','[').replace(' ]',']').replace('{ ','{').replace(' }','}')

    def get_variables(self,target,path=None):
        variables=[]
        if path==None:
            path=target.name+"."
        else:
            path+="."
        
        #print target.match
        if target.match:
            for item in target.match:
                #print item
                if len(item)>=2 and item[0]=='{' and item[-1]=='}':
                    token=item[1:-1]
                    
                    if token.find('|')>0:
                        variable,segment=token.split("|")
                        variables.append(path+variable)
                        #print "getting ",segment
                    else:
                        segment=token
                        variable=segment
                    res=self.get_variables(self.segments[segment],path+variable)
                    if res:
                        variables.append(res)

                elif len(item)>0 and  item[0]=='$':
                    variables.append(path+item[1:])
        if target.children:
            for child in target.children:
                res=self.get_variables(child,path+child.name)
                if res:
                    variables.append(res)

        return variables
                
    def get_variable_info(self,item):
        variable=''
        segment=''
        if len(item)>=2 and item[0]=='{' and item[-1]=='}':
            token=item[1:-1]
        
            if token.find('|')>0:
                variable,segment=token.split("|")
            else:
                variable=token
                segment=token

        return {'name':variable,'class':segment}


    def build_class(self,target):
        variables={}
        

        if target.match: 
            for item in target.match:
                info=self.get_variable_info(item)
                variables[info['name']]=info
        if target.children: 
            for child  in target.children:
                info=self.segments[child.name]
                variables[child.name]= {'name':child.name,'class':child.name}
        
        defines=[]
        var_list=[]
        name='x'
        for var in variables:
            var_list.append(  "{0}=None".format(var,name ))

        
        pad="    "
        template="""
        class {0}:
            {1}
            
            def __init__(self)
                {2}
            
                def debug(self):
                print(self)
        
        """.format(var_list,pad.join(defines))

    


def build_rst():
    l=language()
    groups=['system','record','table']
    for group in groups:
        print "# SECTION: {0}".format(group)
        for command in l.commands:
            cmd=l.commands[command]
            if cmd.group==group:
                print l.permutate(cmd)
                print ""


def build_meta():
    l=language()
    for seg in l.segments :
        segment=l.segments[seg]
        print segment.name
        variables=l.get_variables(segment)
        print variables


def build_class():
    l=language()
    for seg in l.segments :
        segment=l.segments[seg]
        print segment.name
        class_tpl=l.build_class(segment)
        print class_tpl

build_class()
        
#    for subclass in l.segments:
#        name         =None
#        depends_on   =None
#        single  =None
#        store_single =None
#        optional     =None
#        match      =None
#        variables    =None
#        children     =None
#        doc_depth    =None
#        group        =None
#
#
#
#
#
#                
#
#
#                class _join_or:
#                    __slots__=()
#                    c = None
#                    e1 = None
#                    condition = None
#                    e2 = None
#            
#                    def __init__(self,c=None,e1=None,condition=None,e2=None):
#                        if c:  self.c=c
#                        if e1:  self.e1=e1
#                        if condition:  self.condition=condition
#                        if e2:  self.e2=e2
                            