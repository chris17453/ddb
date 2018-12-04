from ..tokenizer.sql_tokenize import *
from ..structure.table import *
from .language import query_matrix
import copy 

debug_on=False



class sql_parser:
    ##
    #     -- [] denotes array, comma seperated
    #     -- () denotes optional element
    #     -- {} denotes a variable element, such as column name
    #     -- |  denotes a choice 
    #     -- EXPRESSION is a column from the select, a function, or a value
    #     -- CONDITION  is an evaluation condition   (=,equals,is,!=,<>,not,>,<,>=,<=)
    #     -- elements must appear in order of index



    #  QUERIES
    #   1 SHOW
    #   2    TABLES

    #   1 SHOW
    #   2    COLUMNS
    #   3 FROM
    #   4   {TABLE}
    
    #  1  SELECT                                           
    #  2     [{COLUMN} 
    #  3      (AS {DISPLAY_NAME})] 
    #  4  FROM 
    #  5     {TABLE} 
    #  6   (WHERE 
    #  7           {EXPRESSION} CONDITION {EXPRESSION} 
    #  8     (AND  {EXPRESSION} CONDITION {EXPRESSION})
    #  9     (OR   {EXPRESSION} CONDITION {EXPRESSION})
    #     )
    #  10   (ORDER BY 
    #  11        [{COLUMN} DIRECTION])
    #  12  (LIMIT ({START_INDEX},{LENGTH}) | ({LENGTH})
    #        )
    #
    #  1  DELETE
    #  4  FROM 
    #  5     {TABLE} 
    #  6   (WHERE 
    #  7           {EXPRESSION} CONDITION {EXPRESSION} 
    #  8     (AND  {EXPRESSION} CONDITION {EXPRESSION})
    #  9     (OR   {EXPRESSION} CONDITION {EXPRESSION})
    #     )

    #  1  UPDATE 
    #  5     {TABLE} 
    #     SET
    #        [{COLUMN}={EXPRESSION}]
    #  6   (WHERE 
    #  7           {EXPRESSION} CONDITION {EXPRESSION} 
    #  8     (AND  {EXPRESSION} CONDITION {EXPRESSION})
    #  9     (OR   {EXPRESSION} CONDITION {EXPRESSION})
    #     )

    # -- BELOW all () are litteral and must appear
    # -- Column count must match expression count
    #  1  INSERT
    #     INTO
    #  5      {TABLE} 
    #         ([{COLUMN}])
    #     VALUES
    #         ({EXPRESSION}])

    def __init__(self,query,debug=False):
        # select * from table where x=y and y=2 order by x,y limit 10,2
        # select c1,c2,c3,c4 as x,* from table where x=y and y=2 order by x,y limit 10,2
        # select top 10 * from table where x=y and y=2 order by x,y 
        # insert into table () values ()
        # delete from table where x=y and y=2


        global debug_on
        self.debug=debug
        self.debug_on=debug
        tokens=tokenize(query,discard_whitespace=True,debug=debug)
        self.query_object=self.parse(tokens)
        if None == self.query_object:
            raise Exception("Object failed to decode")

    def parse(self,tokens):


        sql_object=[]
        # SOME TODO!
        # loop through types
        debug=True
        query_object={}
        for query in query_matrix:
            # loop through switches
            token_index=0
            info("-----",query['query'])

            keyword_found=False
            switch_index=0
            query_mode=None
            while switch_index<len(query['switch']) and token_index<len(tokens):
                
                info("token",token_index,tokens[token_index])
                switch=query['switch'][switch_index]
                switch_index+=1
                curent_object={}
                if 'dispose' in switch:
                    dispose=switch['dispose']
                else:
                    dispose=False
                if 'no_keyword' in switch:
                    no_keyword=switch['no_keyword']
                else:
                    no_keyword=False
                if 'store_array' in switch:
                    store_array=switch['store_array']
                else:
                    store_array=False

                if 'parent' in switch:
                    parent=switch['parent']
                else:
                    parent=None
                if 'optional' in switch:
                    optional=switch['optional']
                else:
                    optional=False


                if isinstance(switch['name'],list):
                    object_id=' '.join([str(x) for x in switch['name'] ])
                    object_id=object_id.lower()
                else:
                    object_id=switch['name']
                    object_id=object_id.lower()
                info("------",object_id,token_index)
                if False == no_keyword:
                    keyword_compare=self.get_sub_array(switch,'name')
                    haystack=self.get_sub_array_sub_key(tokens[token_index:],'data')
                    info( keyword_compare)
                    if True == self.single_array_match(keyword_compare,haystack):
                        info("match", keyword_compare,haystack)
                        # we use name because it may be a list. and its simpler to hash by name
                        # as long as the compare is good, we dont care
                        curent_object['mode']=object_id
                        if switch_index==1:
                            query_mode=query['query']
                        keyword_found=True
                    else:
                        if False == optional:
                            if True == debug:
                                info("Exiting")
                            break
                        else:
                            continue
                    if False == keyword_found:
                        info("Keywords exhausted")
                        break

                    token_index+=len(keyword_compare)
                    info("advance token index ",token_index,switch['data'])
                else:
                    curent_object['mode']=object_id

                if None == switch['data'] or False == switch['data']:
                    info("No data to match")
                    # only append object after argument collection is done
                    #query_object.append(curent_object)
                    if dispose != True:
                        info("----------Adding",curent_object['mode'])
                        query_object[curent_object['mode']]=None
                    
                    
                # This is where data colection happens
                else:
                    in_argument=True
                    argument_index=0
                    while True==in_argument:

                        info("---in argument")

                        ## DEPENDENCY
                        ## DEPENDENCY
                        ## DEPENDENCY

                        if 'depends_on' in switch:
                            depends_on=switch['depends_on']
                        else:
                            info("--- Depends on nothing")
                            depends_on=None

                        # if there is a dependency, enforce
                        if None != depends_on:

                            depends_oncompare=self.get_sub_array(depends_on)
                                                        
                            dependency_found=False
                            for q_o in query_object:
                                info( depends_on,q_o)
                                haystack=self.get_sub_array(q_o)
                                if True == self.single_array_match(depends_oncompare,haystack):
                                    dependency_found=True
                            if False == dependency_found:
                                info("Missing", depends_on)
                                break
                            else:
                                info("Dependency found", depends_on)



                        info("data",switch['data'])
                        if 'arguments' in switch:
                            arguments=switch['arguments']
                        else:
                            arguments=1
                        info("Number of arguments",arguments)

                        data=self.get_sub_array(switch,'data')
                        match_len=0
                        match=None
                        for sig  in data:
                            signature_compare=self.get_sub_array(sig,'sig')
                            haystack=self.get_sub_array_sub_key(tokens[token_index:],'data')
                            if True == self.single_array_match(signature_compare,haystack):
                                if True == debug:
                                    info("match", signature_compare,haystack)
                                if len(signature_compare)>match_len:
                                    match_len=len(signature_compare)
                                    match=signature_compare
                                    info( "Best Match",match_len)
                        if None == match:
                            info("No match")
                            break 
                        else:
                            w_index=0
                            argument={}
                            for word in match:
                                if word[0:1]=='{' and word[-1]=='}':
                                    # variable
                                    if word[1]=='#':
                                        try:
                                            argument[word[2:-1]]=tokens[token_index+w_index]['data']=int(tokens[token_index+w_index]['data'])
                                        except:
                                            argument[word[2:-1]]=tokens[token_index+w_index]['data']
                                    else:
                                        argument[word[1:-1]]=tokens[token_index+w_index]['data']
                                else:
                                    ## normal keyword
                                    argument[word]=tokens[token_index+w_index]['data']                                
                                w_index+=1
                            if 'arguments' not in curent_object:
                                curent_object['arguments']=[]

                            if arguments==1:
                                curent_object['arguments']=argument
                            else:
                            # add the arguments to curent object
                                curent_object['arguments'].append(argument)

                            info("match", match)
                            token_index+=len(match)
                            if arguments!=0:
                                info("print not in list")
                                argument_index+=1
                                if argument_index>=arguments:

                                    info("----------Adding",curent_object['mode'])
                                    if True == store_array:
                                        if curent_object['mode'] not in query_object:
                                            query_object[curent_object['mode']]=[]

                                        query_object[curent_object['mode']].append({curent_object['mode']:curent_object['arguments']})
                                    else:
                                        if None == parent:
                                            query_object[curent_object['mode']]=curent_object['arguments']
                                            info( "NO APPEND")
                                        else:
                                            info( "APPEND")
                                            query_object[parent].append({curent_object['mode']:curent_object['arguments']})
                                    jump=None
                                    if 'jump' in switch:
                                        info( "JUMP")
                                        jump=switch['jump']
                                    if None != jump:
                                        tsi=0
                                        for ts in query['switch']:
                                            if ts['name']==jump:
                                                info("Jumpping from ",switch_index,tsi+1)
                                                switch_index=tsi+1
                                                break
                                            tsi+=1
                                    in_argument=False

                                    in_argument=False
                            else:
                                info("in list")

                                # look ahead to see if its a list ","
                                if len(tokens)>token_index:
                                    info("--looking ahead")
                                    # if its not exit
                                    info("----" ,tokens[token_index]['data'])
                                    if tokens[token_index]['data']!=',':
                                        info("---not list")
                                        # only append object after argument collection is done
                                        info("----------Adding",curent_object['mode'])
                                        if True == store_array:
                                            if curent_object['mode'] not in query_object:
                                                query_object[curent_object['mode']]=[]

                                            query_object[curent_object['mode']].append({curent_object['mode']:curent_object['arguments']})
                                        else:
                                            if None == parent:
                                                #print curent_object
                                                query_object[curent_object['mode']]=curent_object['arguments']
                                                info("NO APPEND")
                                            
                                            else:
                                                info("APPEND")
                                                query_object[parent].append({curent_object['mode']:curent_object['arguments']})
                                        jump=None
                                        if 'jump' in switch:
                                            jump=switch['jump']
                                        if None != jump:
                                            tsi=0
                                            for ts in query['switch']:
                                                if ts['name']==jump:
                                                    info("Jumpping from ",switch_index,tsi+1)
                                                    switch_index=tsi+1
                                                    break
                                                tsi+=1
                                        in_argument=False
                                    else:
                                        info("------more list")
                                        token_index+=1
            
            # This is where we exit if we reached the end of processing with a full length
            #print token_index,len(tokens) 
            info(switch_index,token_index,len(tokens))
            
            info (query_object)
            #so we have run out of text to match and everything is good so far
            if token_index==len(tokens):
                info("############################think its a match")
               
                if 'arguments' not in curent_object and 'arguments' in switch:
                    info("Missing argument in last element")
                    bad=True
                    break

                #lets make sure the rest are optional
                if len(query['switch'])>=switch_index:
                    info("still checking")
                    bad=False
                    for t in  range(switch_index,len(query['switch'])):
                        if 'optional' not in query['switch'][t]:
                            bad=True
                            break
                        else:
                            if  query['switch'][t]['optional']!=True:
                                bad=True
                                break
                        
                    

                    if True == bad:
                        info("Not successful. required arguments missing")
                        break
                  
                    
                info("SUCCESS")
                sql_object={'mode':query_mode,'meta':query_object}
                return sql_object
        return False
    
    #expand columns
    # TODO null trapping
    def expand_columns(self,columns):
        if self.query_object['mode']=="select":
            expanded_select=[]
            for item in self.query_object['meta']['select']:
                if item['column']=='*':
                    for column in columns:
                        expanded_select.append({'column':column})    
                else:
                    expanded_select.append(item)
            self.query_object['meta']['select']=expanded_select
        #?? needed

    
    # support funcitons


    def get_sub_array(self,array,key=None):
        if None == key:
            if isinstance(array,str):
                return [array]
            else:
                return array
        if True == isinstance(array[key],list):
            return array[key]
        else:
            return [array[key]]


    # for tokens ['data']
    def get_sub_array_sub_key(self,array,key):
        temp_array=[]

        for item in array:
            temp_array.append(item[key])

        return temp_array

    
    def single_array_match(self,needles,haystacks):
        """ Match a single or array of strings with with another string or array of strings"""
        
        # make needels an array, with or without a sub key
        if isinstance(needles,str):
            temp_needles=[needles]
        else:
            temp_needles=needles

        
        # make haystacks an array
        if isinstance(haystacks,str):
            temp_haystacks=[haystacks]
        else:
            temp_haystacks=haystacks

        # now we have 2 plain array/lists to compare

        index=0
        for needle in temp_needles:
            # ran out of haystack to test. not a match
            if index>=len(temp_haystacks):
                return False
            haystack=temp_haystacks[index]
            # not a match
            if needle[0:1]!='{' and needle[-1]!='}':
                if needle.lower()!=haystack.lower():
                    return False
            index+=1
        # if we got here it must match
        return  True
         
